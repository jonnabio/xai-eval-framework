# scripts/auto_push.ps1
# Periodic git sync for experiment results only.

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$BootstrapPaths = @(
    "C:\Program Files\Git\cmd",
    "C:\Program Files\Git\bin",
    "C:\ProgramData\anaconda3",
    "C:\ProgramData\anaconda3\Scripts"
)
foreach ($BootstrapPath in $BootstrapPaths) {
    if ((Test-Path -Path $BootstrapPath) -and -not (($env:Path -split ';') -contains $BootstrapPath)) {
        $env:Path = "$BootstrapPath;$env:Path"
    }
}

$GitExe = if (Test-Path "C:\Program Files\Git\cmd\git.exe") {
    "C:\Program Files\Git\cmd\git.exe"
} elseif (Test-Path "C:\Program Files\Git\bin\git.exe") {
    "C:\Program Files\Git\bin\git.exe"
} else {
    (Get-Command git -ErrorAction Stop).Source
}

$CommitInterval = 900 # 15 minutes
$PushInterval = 21600 # 6 hours
$LogFile = "logs\auto_push.log"
$LastPushFile = "logs\auto_push_last_push.txt"
$TrackedPaths = @(
    "experiments/exp2_scaled/results"
)
$GitMutexDir = "logs\git_mutex"

if (-not (Test-Path -Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

function Write-Log {
    param([string]$Message)
    $DateStr = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$DateStr] $Message" | Out-File -FilePath $LogFile -Append
}

function Invoke-WithGitMutex {
    param(
        [scriptblock]$Action,
        [string]$Reason = "git-operation",
        [int]$TimeoutSeconds = 180
    )

    $Deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    $Acquired = $false

    while ((Get-Date) -lt $Deadline) {
        try {
            New-Item -ItemType Directory -Path $GitMutexDir -ErrorAction Stop | Out-Null
            Set-Content -Path (Join-Path $GitMutexDir "owner.txt") -Value "$PID $Reason $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ErrorAction SilentlyContinue
            $Acquired = $true
            break
        } catch {
            Start-Sleep -Seconds 2
        }
    }

    if (-not $Acquired) {
        Write-Log "[WARN] Timed out waiting for Git mutex: $Reason"
        return $null
    }

    try {
        & $Action
    } finally {
        Remove-Item -Path $GitMutexDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

function ConvertTo-ProcessArgumentString {
    param([string[]]$Arguments)

    return ($Arguments | ForEach-Object {
        if ($_ -match '[\s"]') {
            '"' + ($_ -replace '"', '\"') + '"'
        } else {
            $_
        }
    }) -join ' '
}

function Invoke-GitLogged {
    param([string[]]$Arguments)

    $StdOutPath = Join-Path "logs" "auto_push.git.stdout.log"
    $StdErrPath = Join-Path "logs" "auto_push.git.stderr.log"
    if (Test-Path $StdOutPath) { Remove-Item $StdOutPath -Force -ErrorAction SilentlyContinue }
    if (Test-Path $StdErrPath) { Remove-Item $StdErrPath -Force -ErrorAction SilentlyContinue }

    $Process = Start-Process `
        -FilePath $GitExe `
        -ArgumentList (ConvertTo-ProcessArgumentString -Arguments $Arguments) `
        -WorkingDirectory (Get-Location).Path `
        -WindowStyle Hidden `
        -RedirectStandardOutput $StdOutPath `
        -RedirectStandardError $StdErrPath `
        -Wait `
        -PassThru

    foreach ($Path in @($StdOutPath, $StdErrPath)) {
        if (Test-Path $Path) {
            Get-Content -Path $Path -ErrorAction SilentlyContinue | Out-File -FilePath $LogFile -Append
            Remove-Item -Path $Path -Force -ErrorAction SilentlyContinue
        }
    }

    return $Process.ExitCode
}

function Get-GitCommandOutput {
    param([string[]]$Arguments)

    $StdOutPath = Join-Path "logs" "auto_push.git_cmd.stdout.log"
    $StdErrPath = Join-Path "logs" "auto_push.git_cmd.stderr.log"
    if (Test-Path $StdOutPath) { Remove-Item $StdOutPath -Force -ErrorAction SilentlyContinue }
    if (Test-Path $StdErrPath) { Remove-Item $StdErrPath -Force -ErrorAction SilentlyContinue }

    $Process = Start-Process `
        -FilePath $GitExe `
        -ArgumentList (ConvertTo-ProcessArgumentString -Arguments $Arguments) `
        -WorkingDirectory (Get-Location).Path `
        -WindowStyle Hidden `
        -RedirectStandardOutput $StdOutPath `
        -RedirectStandardError $StdErrPath `
        -Wait `
        -PassThru

    $Output = if (Test-Path $StdOutPath) { Get-Content -Path $StdOutPath -ErrorAction SilentlyContinue } else { @() }
    foreach ($Path in @($StdOutPath, $StdErrPath)) {
        if (Test-Path $Path) {
            Remove-Item -Path $Path -Force -ErrorAction SilentlyContinue
        }
    }

    return @{
        ExitCode = $Process.ExitCode
        Output = $Output
    }
}

function Get-GitStatusPorcelain {
    param([string]$TrackedPath)

    $StatusResult = Get-GitCommandOutput -Arguments @("status", "--porcelain", "--", $TrackedPath)
    if ($StatusResult.ExitCode -ne 0) {
        return $null
    }

    return @($StatusResult.Output | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
}

function Get-LastPushTime {
    if (-not (Test-Path $LastPushFile)) {
        return $null
    }

    try {
        return [datetime](Get-Content -Path $LastPushFile -ErrorAction Stop | Select-Object -First 1)
    } catch {
        return $null
    }
}

function Set-LastPushTime {
    (Get-Date).ToString("o") | Out-File -FilePath $LastPushFile -Encoding utf8
}

while ($true) {
    Write-Log "Checkpointing progress with Git pool..."

    $CycleOk = Invoke-WithGitMutex -Reason "auto_push_cycle" -Action {
        $BranchResult = Get-GitCommandOutput -Arguments @("rev-parse", "--abbrev-ref", "HEAD")
        $CurrentBranch = @($BranchResult.Output)[-1]
        if ($BranchResult.ExitCode -ne 0 -or [string]::IsNullOrWhiteSpace($CurrentBranch)) {
            Write-Log "Error resolving current branch."
            return $false
        }

        # Stage only experiment outputs. This avoids sweeping in
        # locally retrained model binaries, config edits, or other workspace changes.
        Invoke-GitLogged -Arguments @("add", "--", $TrackedPaths[0]) | Out-Null

        $PendingChanges = Get-GitStatusPorcelain -TrackedPath $TrackedPaths[0]
        if ($null -eq $PendingChanges) {
            Write-Log "Failed to inspect pending changes."
            return $false
        }

        if ($PendingChanges.Count -gt 0) {
            $CommitExitCode = Invoke-GitLogged -Arguments @("commit", "-m", "Auto-sync queue: Results checkpoint")
            if ($CommitExitCode -ne 0) {
                Write-Log "Commit failed; skipping fetch/push for this cycle."
                return $false
            }
        } else {
            Write-Log "No result changes to commit."
        }

        $LastPushTime = Get-LastPushTime
        $PushDue = $null -eq $LastPushTime -or ((Get-Date) - $LastPushTime).TotalSeconds -ge $PushInterval

        if (-not $PushDue) {
            $SecondsUntilPush = [math]::Max(0, $PushInterval - [int]((Get-Date) - $LastPushTime).TotalSeconds)
            Write-Log "Push not due yet. Next push window in about $SecondsUntilPush seconds."
            return $true
        }

        Write-Log "Push window reached; fetching and rebasing before push."
        $FetchExitCode = Invoke-GitLogged -Arguments @("fetch", "--no-progress", "origin", $CurrentBranch)
        if ($FetchExitCode -ne 0) {
            Write-Log "Fetch failed; changes remain committed locally."
            return $false
        }

        $RebaseExitCode = Invoke-GitLogged -Arguments @("-c", "core.editor=true", "rebase", "origin/$CurrentBranch")
        if ($RebaseExitCode -ne 0) {
            Write-Log "Rebase failed; changes remain committed locally and need manual reconciliation."
            return $false
        }

        $PushExitCode = Invoke-GitLogged -Arguments @("push", "--no-progress", "origin", "HEAD:$CurrentBranch")
        if ($PushExitCode -ne 0) {
            Write-Log "Push failed; changes remain committed locally for the next push window."
        } else {
            Write-Log "Sync complete."
            Set-LastPushTime
        }

        return $true
    }

    if ($null -eq $CycleOk) {
        Write-Log "Skipped sync cycle because Git mutex was unavailable."
    }

    Write-Log "Sleeping for $CommitInterval seconds..."
    Start-Sleep -Seconds $CommitInterval
}
