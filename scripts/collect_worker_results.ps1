# scripts/collect_worker_results.ps1
# Consolidate worker result branches into main without switching the live checkout.

param(
    [string]$Remote = "origin",
    [string]$BaseBranch = "main",
    [string[]]$ExtraBranches = @(),
    [switch]$SkipConflicts,
    [switch]$Push,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$BootstrapPaths = @(
    "C:\Program Files\Git\cmd",
    "C:\Program Files\Git\bin"
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

$LogDir = "logs"
$LogFile = Join-Path $LogDir "collector.log"
$GitMutexDir = Join-Path $LogDir "git_mutex"
if (-not (Test-Path -Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}

function Write-Log {
    param([string]$Message)
    $DateStr = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $Line = "[$DateStr] $Message"
    Write-Host $Line
    Add-Content -Path $LogFile -Value $Line
}

function Invoke-GitProcess {
    param(
        [string[]]$Arguments,
        [bool]$LogOutput = $true
    )

    $TempPrefix = Join-Path $LogDir ("collector-git-{0}-{1}" -f $PID, ([System.Guid]::NewGuid().ToString("N")))
    $StdOutPath = "$TempPrefix.stdout.log"
    $StdErrPath = "$TempPrefix.stderr.log"
    $Process = Start-Process -FilePath $GitExe -ArgumentList $Arguments -NoNewWindow -Wait -PassThru -RedirectStandardOutput $StdOutPath -RedirectStandardError $StdErrPath
    $Output = @()
    if (Test-Path $StdOutPath) {
        $Output += Get-Content -Path $StdOutPath -ErrorAction SilentlyContinue
    }
    if (Test-Path $StdErrPath) {
        $Output += Get-Content -Path $StdErrPath -ErrorAction SilentlyContinue
    }
    Remove-Item -Path $StdOutPath, $StdErrPath -Force -ErrorAction SilentlyContinue

    if ($LogOutput -and $Output) {
        $Output | ForEach-Object { Write-Log "git: $_" }
    }

    return @{
        ExitCode = $Process.ExitCode
        Output = @($Output)
    }
}

function Invoke-GitMergeTree {
    param(
        [string]$BaseCommit,
        [string]$HeadCommit,
        [string]$Branch
    )

    $Result = Invoke-GitProcess -Arguments @("merge-tree", "--write-tree", $BaseCommit, $HeadCommit) -LogOutput $false
    $Lines = @($Result.Output | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })

    if ($Result.ExitCode -ne 0 -or $Lines.Count -ne 1 -or $Lines[0] -notmatch '^[0-9a-f]{40}$') {
        $ConflictDetailPath = Join-Path $LogDir ("collector-conflict-{0}-{1}.log" -f (($Branch -replace '[^a-zA-Z0-9._-]', '_')), (Get-Date -Format "yyyyMMdd_HHmmss"))
        $Lines | Set-Content -Path $ConflictDetailPath
        $ConflictCount = @($Lines | Where-Object { $_ -match '^[0-9]{6} [0-9a-f]{40} [0-3]\t' }).Count
        Write-Log "[CONFLICT] $Branch cannot be merged cleanly into $BaseCommit. Details: $ConflictDetailPath; conflict entries: $ConflictCount"
        return $null
    }

    return $Lines[0]
}

function Invoke-Git {
    param([string[]]$Arguments)

    $Result = Invoke-GitProcess -Arguments $Arguments
    if ($Result.ExitCode -ne 0) {
        throw "git $($Arguments -join ' ') failed with exit code $($Result.ExitCode)"
    }
    return @($Result.Output)
}

function Invoke-GitScalar {
    param([string[]]$Arguments)
    $Output = Invoke-Git -Arguments $Arguments
    return (($Output | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Last 1) -as [string]).Trim()
}

function Invoke-WithGitMutex {
    param(
        [scriptblock]$Action,
        [string]$Reason = "collect-worker-results",
        [int]$TimeoutSeconds = 300
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
        throw "Timed out waiting for Git mutex: $Reason"
    }

    try {
        & $Action
    } finally {
        Remove-Item -Path $GitMutexDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

function Convert-ToRemoteBranch {
    param([string]$Branch)

    $Clean = $Branch.Trim()
    if ([string]::IsNullOrWhiteSpace($Clean)) {
        return $null
    }
    if ($Clean -like "refs/remotes/*") {
        return $Clean.Substring("refs/remotes/".Length)
    }
    if ($Clean -like "$Remote/*") {
        return $Clean
    }
    return "$Remote/$Clean"
}

function Get-ResultJsonCount {
    param([string]$Ref)

    $Result = Invoke-GitProcess -Arguments @("ls-tree", "-r", "--name-only", $Ref, "experiments/exp2_scaled/results") -LogOutput $false
    if ($Result.ExitCode -ne 0) {
        throw "git ls-tree failed while counting results for $Ref"
    }
    $Paths = @($Result.Output)
    return @($Paths | Where-Object { $_ -match '/results\.json$' }).Count
}

Invoke-WithGitMutex -Reason "collect-worker-results" -Action {
    Write-Log "Fetching $Remote..."
    Invoke-Git -Arguments @("fetch", $Remote, "--prune") | Out-Null

    $BaseRef = "$Remote/$BaseBranch"
    $BaseCommit = Invoke-GitScalar -Arguments @("rev-parse", $BaseRef)
    $CurrentBranch = Invoke-GitScalar -Arguments @("rev-parse", "--abbrev-ref", "HEAD")
    Write-Log "Current checkout remains on $CurrentBranch."
    Write-Log "Base ref $BaseRef is $BaseCommit."

    $DiscoveredBranches = Invoke-Git -Arguments @(
        "for-each-ref",
        "--format=%(refname:short)",
        "refs/remotes/$Remote/results"
    )

    $Branches = [System.Collections.Generic.List[string]]::new()
    foreach ($Branch in $DiscoveredBranches) {
        $RemoteBranch = Convert-ToRemoteBranch -Branch $Branch
        if ($RemoteBranch) {
            $Branches.Add($RemoteBranch)
        }
    }
    foreach ($Branch in $ExtraBranches) {
        $RemoteBranch = Convert-ToRemoteBranch -Branch $Branch
        if ($RemoteBranch) {
            $Branches.Add($RemoteBranch)
        }
    }
    $Branches = @($Branches | Sort-Object -Unique)

    if ($Branches.Count -eq 0) {
        throw "No worker branches found. Expected refs like $Remote/results/<worker_id> or pass -ExtraBranches."
    }

    Write-Log "Collector branches: $($Branches -join ', ')"

    $MergeBase = $BaseCommit
    foreach ($Branch in $Branches) {
        $Head = Invoke-GitScalar -Arguments @("rev-parse", $Branch)

        $AncestorCheck = Invoke-GitProcess -Arguments @("merge-base", "--is-ancestor", $Head, $MergeBase) -LogOutput $false
        if ($AncestorCheck.ExitCode -eq 0) {
            Write-Log "Already included: $Branch ($Head)"
            continue
        }
        if ($AncestorCheck.ExitCode -ne 1) {
            throw "git merge-base --is-ancestor failed for $Branch with exit code $($AncestorCheck.ExitCode)"
        }

        Write-Log "Merging $Branch ($Head) into collector commit $MergeBase."
        if ($DryRun) {
            $DryRunTree = Invoke-GitMergeTree -BaseCommit $MergeBase -HeadCommit $Head -Branch $Branch
            if (-not $DryRunTree -and -not $SkipConflicts) {
                throw "Dry run found conflicts for $Branch. Re-run with -SkipConflicts to skip it."
            }
            if ($DryRunTree) {
                Write-Log "Dry run merge-tree succeeded for $Branch."
            } else {
                Write-Log "Dry run skipped conflicting branch $Branch."
            }
            continue
        }

        $Tree = Invoke-GitMergeTree -BaseCommit $MergeBase -HeadCommit $Head -Branch $Branch
        if (-not $Tree) {
            if ($SkipConflicts) {
                Write-Log "Skipping conflicting branch $Branch."
                continue
            }
            throw "Merge conflicts found for $Branch. Re-run with -SkipConflicts to skip it."
        }
        $Message = "Collect worker results from $Branch`n`nMerge latest checkpoint from $Branch into $BaseBranch."
        $MessagePath = Join-Path $LogDir ("collector-message-{0}.txt" -f ([System.Guid]::NewGuid().ToString("N")))
        Set-Content -Path $MessagePath -Value $Message

        $PreviousAuthorName = $env:GIT_AUTHOR_NAME
        $PreviousAuthorEmail = $env:GIT_AUTHOR_EMAIL
        $PreviousCommitterName = $env:GIT_COMMITTER_NAME
        $PreviousCommitterEmail = $env:GIT_COMMITTER_EMAIL
        try {
            $env:GIT_AUTHOR_NAME = "jonna"
            $env:GIT_AUTHOR_EMAIL = "jonna@users.noreply.github.com"
            $env:GIT_COMMITTER_NAME = "jonna"
            $env:GIT_COMMITTER_EMAIL = "jonna@users.noreply.github.com"
            $MergeBase = Invoke-GitScalar -Arguments @("commit-tree", $Tree, "-p", $MergeBase, "-p", $Head, "-F", $MessagePath)
        } finally {
            Remove-Item -Path $MessagePath -Force -ErrorAction SilentlyContinue
            $env:GIT_AUTHOR_NAME = $PreviousAuthorName
            $env:GIT_AUTHOR_EMAIL = $PreviousAuthorEmail
            $env:GIT_COMMITTER_NAME = $PreviousCommitterName
            $env:GIT_COMMITTER_EMAIL = $PreviousCommitterEmail
        }

        Write-Log "Created collector merge commit $MergeBase for $Branch."
    }

    if ($DryRun) {
        Write-Log "Dry run complete. No commit or push was made."
        return
    }

    $ResultCount = Get-ResultJsonCount -Ref $MergeBase
    Write-Log "Consolidated result count at $MergeBase is $ResultCount results.json files."

    if ($Push) {
        Write-Log "Pushing $MergeBase to refs/heads/$BaseBranch."
        Invoke-Git -Arguments @("push", $Remote, "$MergeBase`:refs/heads/$BaseBranch") | Out-Null
        Write-Log "Collector push complete: $Remote/$BaseBranch <= $MergeBase"
    } else {
        Write-Log "Push not requested. Re-run with -Push to update $Remote/$BaseBranch."
    }
}
