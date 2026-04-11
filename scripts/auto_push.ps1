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
$PushInterval = 10800 # 3 hours
$LogFile = "logs\auto_push.log"
$LastPushFile = "logs\auto_push_last_push.txt"
$GitMutexDir = "logs\git_mutex"

if (-not (Test-Path -Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

function Get-WorkerId {
    $RawWorkerId = if (-not [string]::IsNullOrWhiteSpace($env:XAI_WORKER_ID)) {
        $env:XAI_WORKER_ID
    } elseif (-not [string]::IsNullOrWhiteSpace($env:COMPUTERNAME)) {
        $env:COMPUTERNAME
    } else {
        [System.Net.Dns]::GetHostName()
    }

    $WorkerId = ($RawWorkerId.ToLowerInvariant() -replace '[^a-z0-9._-]', '-').Trim('-')
    if ([string]::IsNullOrWhiteSpace($WorkerId)) {
        return "windows-worker"
    }

    return $WorkerId
}

$WorkerId = Get-WorkerId
$ResultsBranch = if (-not [string]::IsNullOrWhiteSpace($env:XAI_RESULTS_BRANCH)) {
    $env:XAI_RESULTS_BRANCH
} else {
    "results/$WorkerId"
}
$ManifestRoot = "experiments/exp2_scaled/worker_manifests/$WorkerId"
$TrackedPaths = @(
    "experiments/exp2_scaled/results",
    "experiments/exp2_scaled/worker_manifests"
)

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

    $PreviousOptionalLocks = $env:GIT_OPTIONAL_LOCKS
    $env:GIT_OPTIONAL_LOCKS = "0"
    try {
        $Process = Start-Process `
            -FilePath $GitExe `
            -ArgumentList (ConvertTo-ProcessArgumentString -Arguments $Arguments) `
            -WorkingDirectory (Get-Location).Path `
            -WindowStyle Hidden `
            -RedirectStandardOutput $StdOutPath `
            -RedirectStandardError $StdErrPath `
            -Wait `
            -PassThru
    } finally {
        $env:GIT_OPTIONAL_LOCKS = $PreviousOptionalLocks
    }

    $Output = if (Test-Path $StdOutPath) { Get-Content -Path $StdOutPath -ErrorAction SilentlyContinue } else { @() }
    if ($Process.ExitCode -ne 0) {
        Write-Log "[WARN] Git command failed: git $(ConvertTo-ProcessArgumentString -Arguments $Arguments)"
        foreach ($Path in @($StdOutPath, $StdErrPath)) {
            if (Test-Path $Path) {
                Get-Content -Path $Path -ErrorAction SilentlyContinue | Out-File -FilePath $LogFile -Append
            }
        }
    }

    foreach ($Path in @($StdOutPath, $StdErrPath)) {
        Remove-Item -Path $Path -Force -ErrorAction SilentlyContinue
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

    return ,@($StatusResult.Output | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
}

function Ensure-ResultsBranch {
    $BranchResult = Get-GitCommandOutput -Arguments @("rev-parse", "--abbrev-ref", "HEAD")
    $CurrentBranch = @($BranchResult.Output)[-1]
    if ($BranchResult.ExitCode -ne 0 -or [string]::IsNullOrWhiteSpace($CurrentBranch) -or $CurrentBranch -eq "HEAD") {
        Write-Log "Error resolving current branch."
        return $false
    }

    if ($CurrentBranch -eq $ResultsBranch) {
        return $true
    }

    Write-Log "Switching from $CurrentBranch to worker result branch $ResultsBranch."
    $BranchExists = Get-GitCommandOutput -Arguments @("rev-parse", "--verify", "refs/heads/$ResultsBranch")
    if ($BranchExists.ExitCode -eq 0) {
        $SwitchExitCode = Invoke-GitLogged -Arguments @("switch", $ResultsBranch)
    } else {
        $SwitchExitCode = Invoke-GitLogged -Arguments @("switch", "-c", $ResultsBranch)
    }

    if ($SwitchExitCode -ne 0) {
        Write-Log "Failed to switch to worker result branch $ResultsBranch."
        return $false
    }

    $MergeExitCode = Invoke-GitLogged -Arguments @("merge", "--no-edit", $CurrentBranch)
    if ($MergeExitCode -ne 0) {
        Write-Log "Failed to merge $CurrentBranch into $ResultsBranch. Resolve manually before running experiments."
        return $false
    }

    return $true
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
        if (-not (Ensure-ResultsBranch)) {
            return $false
        }

        # Stage only experiment outputs. This avoids sweeping in
        # locally retrained model binaries, config edits, or other workspace changes.
        foreach ($TrackedPath in $TrackedPaths) {
            if (-not (Test-Path -Path $TrackedPath)) {
                New-Item -ItemType Directory -Path $TrackedPath -Force | Out-Null
            }
        }

        $AddArguments = @("add", "--") + $TrackedPaths
        $AddExitCode = Invoke-GitLogged -Arguments $AddArguments
        if ($AddExitCode -ne 0) {
            Write-Log "Git add failed; preserving files and retrying next cycle."
            return $false
        }

        $PendingChanges = Get-GitStatusPorcelain -TrackedPath $TrackedPaths[0]
        $PendingManifestChanges = Get-GitStatusPorcelain -TrackedPath $TrackedPaths[1]
        if ($null -eq $PendingChanges) {
            Write-Log "Failed to inspect pending changes."
            return $false
        }
        if ($null -eq $PendingManifestChanges) {
            Write-Log "Failed to inspect pending manifest changes."
            return $false
        }

        if (($PendingChanges.Count + $PendingManifestChanges.Count) -gt 0) {
            $CommitExitCode = Invoke-GitLogged -Arguments @("commit", "-m", "Auto-sync worker checkpoint: $WorkerId")
            if ($CommitExitCode -ne 0) {
                Write-Log "Commit failed; skipping fetch/push for this cycle."
                return $false
            }
        } else {
            Write-Log "No result changes to commit."
        }

        $LastPushTime = Get-LastPushTime
        $UpstreamResult = Get-GitCommandOutput -Arguments @("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
        $HasUpstream = $UpstreamResult.ExitCode -eq 0
        $PushDue = (-not $HasUpstream) -or $null -eq $LastPushTime -or ((Get-Date) - $LastPushTime).TotalSeconds -ge $PushInterval

        if (-not $PushDue) {
            $SecondsUntilPush = [math]::Max(0, $PushInterval - [int]((Get-Date) - $LastPushTime).TotalSeconds)
            Write-Log "Push not due yet. Next push window in about $SecondsUntilPush seconds."
            return $true
        }

        Write-Log "Push window reached; pushing worker branch $ResultsBranch without rebasing."
        $PushExitCode = Invoke-GitLogged -Arguments @("push", "--no-progress", "--set-upstream", "origin", "HEAD:refs/heads/$ResultsBranch")
        if ($PushExitCode -ne 0) {
            Write-Log "Push failed; worker checkpoint commits remain local for the next push window."
        } else {
            Write-Log "Worker branch sync complete: $ResultsBranch."
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
