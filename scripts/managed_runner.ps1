# managed_runner.ps1
# Automated experiment runner for Windows (Distributed node)

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

$PythonExe = if (Test-Path "C:\ProgramData\anaconda3\python.exe") {
    "C:\ProgramData\anaconda3\python.exe"
} else {
    (Get-Command python -ErrorAction Stop).Source
}

$GitExe = if (Test-Path "C:\Program Files\Git\cmd\git.exe") {
    "C:\Program Files\Git\cmd\git.exe"
} elseif (Test-Path "C:\Program Files\Git\bin\git.exe") {
    "C:\Program Files\Git\bin\git.exe"
} else {
    (Get-Command git -ErrorAction Stop).Source
}

$LogFile = "logs\managed_runner.log"
$ResultsPath = "experiments/exp2_scaled/results"
$TempLogDir = "logs\runner_temp"
$GitMutexDir = "logs\git_mutex"
if (-not (Test-Path -Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}
if (-not (Test-Path -Path $TempLogDir)) {
    New-Item -ItemType Directory -Path $TempLogDir | Out-Null
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
    $ResultsPath,
    "experiments/exp2_scaled/worker_manifests"
)

function Write-Log {
    param([string]$Message)
    $CurrentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$CurrentDate] $Message" | Out-File -FilePath $LogFile -Append
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

function Get-GitCommandOutput {
    param([string[]]$Arguments)

    $StdOutPath = Join-Path $TempLogDir "git_cmd.stdout.log"
    $StdErrPath = Join-Path $TempLogDir "git_cmd.stderr.log"
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
        Append-ProcessLogs -StdOutPath $StdOutPath -StdErrPath $StdErrPath
        return @{
            ExitCode = $Process.ExitCode
            Output = @()
        }
    }

    Remove-Item $StdOutPath -Force -ErrorAction SilentlyContinue
    Remove-Item $StdErrPath -Force -ErrorAction SilentlyContinue
    return @{
        ExitCode = 0
        Output = $Output
    }
}

function Invoke-GitLogged {
    param([string[]]$Arguments)

    $StdOutPath = Join-Path $TempLogDir "git_run.stdout.log"
    $StdErrPath = Join-Path $TempLogDir "git_run.stderr.log"
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

    Append-ProcessLogs -StdOutPath $StdOutPath -StdErrPath $StdErrPath
    return $Process.ExitCode
}

function Invoke-GitQuiet {
    param([string[]]$Arguments)

    $StdOutPath = Join-Path $TempLogDir "git_quiet.stdout.log"
    $StdErrPath = Join-Path $TempLogDir "git_quiet.stderr.log"
    if (Test-Path $StdOutPath) { Remove-Item $StdOutPath -Force -ErrorAction SilentlyContinue }
    if (Test-Path $StdErrPath) { Remove-Item $StdErrPath -Force -ErrorAction SilentlyContinue }

    $Process = Start-Process `
        -FilePath $GitExe `
        -ArgumentList $Arguments `
        -WorkingDirectory (Get-Location).Path `
        -WindowStyle Hidden `
        -RedirectStandardOutput $StdOutPath `
        -RedirectStandardError $StdErrPath `
        -Wait `
        -PassThru

    Remove-Item $StdOutPath -Force -ErrorAction SilentlyContinue
    Remove-Item $StdErrPath -Force -ErrorAction SilentlyContinue
    return $Process.ExitCode
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
        Write-Log "[ERROR] Failed to resolve current branch."
        return $false
    }

    if ($CurrentBranch -eq $ResultsBranch) {
        return $true
    }

    Write-Log "[GIT] Switching from $CurrentBranch to worker result branch $ResultsBranch."
    $BranchExists = Get-GitCommandOutput -Arguments @("rev-parse", "--verify", "refs/heads/$ResultsBranch")
    if ($BranchExists.ExitCode -eq 0) {
        $SwitchExitCode = Invoke-GitLogged -Arguments @("switch", $ResultsBranch)
    } else {
        $SwitchExitCode = Invoke-GitLogged -Arguments @("switch", "-c", $ResultsBranch)
    }

    if ($SwitchExitCode -ne 0) {
        Write-Log "[ERROR] Failed to switch to worker result branch $ResultsBranch."
        return $false
    }

    $MergeExitCode = Invoke-GitLogged -Arguments @("merge", "--no-edit", $CurrentBranch)
    if ($MergeExitCode -ne 0) {
        Write-Log "[ERROR] Failed to merge $CurrentBranch into $ResultsBranch. Resolve manually before running experiments."
        return $false
    }

    return $true
}

function Get-MissingExperimentList {
    try {
        $StdOutPath = Join-Path $TempLogDir "missing_results.stdout.log"
        $StdErrPath = Join-Path $TempLogDir "missing_results.stderr.log"
        if (Test-Path $StdOutPath) { Remove-Item $StdOutPath -Force -ErrorAction SilentlyContinue }
        if (Test-Path $StdErrPath) { Remove-Item $StdErrPath -Force -ErrorAction SilentlyContinue }

        $Process = Start-Process `
            -FilePath $PythonExe `
            -ArgumentList @("scripts/check_missing_results.py") `
            -WorkingDirectory (Get-Location).Path `
            -WindowStyle Hidden `
            -RedirectStandardOutput $StdOutPath `
            -RedirectStandardError $StdErrPath `
            -Wait `
            -PassThru

        if ($Process.ExitCode -ne 0) {
            Write-Log "[ERROR] Failed to compute missing experiment list."
            Append-ProcessLogs -StdOutPath $StdOutPath -StdErrPath $StdErrPath
            return @()
        }

        $MissingOutput = if (Test-Path $StdOutPath) { Get-Content -Path $StdOutPath -ErrorAction SilentlyContinue } else { @() }
        Append-ProcessLogs -StdOutPath $StdOutPath -StdErrPath $StdErrPath
        return @($MissingOutput | Select-Object -Skip 1 | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
    } catch {
        Write-Log "[ERROR] Exception while computing missing experiment list: $_"
        return @()
    }
}

function Append-ProcessLogs {
    param(
        [string]$StdOutPath,
        [string]$StdErrPath
    )

    foreach ($Path in @($StdOutPath, $StdErrPath)) {
        if (Test-Path -Path $Path) {
            Get-Content -Path $Path -ErrorAction SilentlyContinue | Out-File -FilePath $LogFile -Append
            Remove-Item -Path $Path -Force -ErrorAction SilentlyContinue
        }
    }
}

function Get-ConfigOutputDir {
    param([string]$ConfigPath)

    try {
        $Script = @"
import sys
import yaml
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
print(data.get('output_dir', ''))
"@
        $OutputDir = @($Script | & $PythonExe - $ConfigPath)[-1]
        return ($OutputDir | Out-String).Trim()
    } catch {
        return ""
    }
}

function Get-ConfigTargetInstances {
    param([string]$ConfigPath)

    try {
        $Script = @"
import sys
import yaml
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
samples_per_class = data.get('sampling', {}).get('samples_per_class')
print(int(samples_per_class) * 4 if samples_per_class else '')
"@
        $TargetInstances = @($Script | & $PythonExe - $ConfigPath)[-1]
        return ($TargetInstances | Out-String).Trim()
    } catch {
        return ""
    }
}

function Get-InstanceProgressSnapshot {
    param([string]$OutputDir)

    $InstancesDir = Join-Path $OutputDir "instances"
    if (-not (Test-Path -Path $InstancesDir)) {
        return @{
            Exists = $false
            Count = 0
            LatestWrite = $null
            InstancesDir = $InstancesDir
        }
    }

    $Files = Get-ChildItem -Path $InstancesDir -Filter *.json -ErrorAction SilentlyContinue
    $Latest = $Files | Sort-Object LastWriteTime -Descending | Select-Object -First 1

    return @{
        Exists = $true
        Count = @($Files).Count
        LatestWrite = if ($Latest) { $Latest.LastWriteTime } else { $null }
        InstancesDir = $InstancesDir
    }
}

function Write-RunManifest {
    param(
        [string]$ExperimentName,
        [string]$ConfigPath,
        [string]$OutputDir,
        [string]$Status,
        [datetime]$StartedAt,
        [Nullable[int]]$ExitCode = $null
    )

    if (-not (Test-Path -Path $ManifestRoot)) {
        New-Item -ItemType Directory -Path $ManifestRoot -Force | Out-Null
    }

    $Snapshot = if (-not [string]::IsNullOrWhiteSpace($OutputDir)) {
        Get-InstanceProgressSnapshot -OutputDir $OutputDir
    } else {
        @{
            Exists = $false
            Count = 0
            LatestWrite = $null
            InstancesDir = ""
        }
    }

    $TargetInstancesText = if (-not [string]::IsNullOrWhiteSpace($ConfigPath) -and (Test-Path -Path $ConfigPath)) {
        Get-ConfigTargetInstances -ConfigPath $ConfigPath
    } else {
        ""
    }
    $TargetInstances = if (-not [string]::IsNullOrWhiteSpace($TargetInstancesText)) {
        [int]$TargetInstancesText
    } else {
        $null
    }

    $ResultsFile = if (-not [string]::IsNullOrWhiteSpace($OutputDir)) {
        Join-Path $OutputDir "results.json"
    } else {
        ""
    }

    $Manifest = [ordered]@{
        worker_id = $WorkerId
        host = $env:COMPUTERNAME
        results_branch = $ResultsBranch
        experiment_name = $ExperimentName
        config_path = $ConfigPath
        output_dir = $OutputDir
        status = $Status
        started_at = if ($StartedAt) { $StartedAt.ToString("o") } else { $null }
        last_checkpoint_at = (Get-Date).ToString("o")
        instances_done = $Snapshot.Count
        target_instances = $TargetInstances
        latest_instance_write = if ($Snapshot.LatestWrite) { $Snapshot.LatestWrite.ToString("o") } else { $null }
        results_json_exists = if (-not [string]::IsNullOrWhiteSpace($ResultsFile)) { Test-Path -Path $ResultsFile } else { $false }
        exit_code = $ExitCode
        runner_pid = $PID
    }

    $ManifestJson = $Manifest | ConvertTo-Json -Depth 5
    $SafeName = if (-not [string]::IsNullOrWhiteSpace($ExperimentName)) {
        $ExperimentName -replace '[^A-Za-z0-9_.-]', '_'
    } else {
        "idle"
    }

    $ManifestJson | Set-Content -Path (Join-Path $ManifestRoot "current.json") -Encoding UTF8
    $ManifestJson | Set-Content -Path (Join-Path $ManifestRoot "$SafeName.json") -Encoding UTF8
}

function Invoke-ExperimentProcess {
    param(
        [string]$ConfigPath,
        [string]$ExperimentName,
        [int]$Attempt
    )

    $SafeName = ($ExperimentName -replace '[^A-Za-z0-9_.-]', '_')
    $StdOutPath = Join-Path $TempLogDir "$SafeName.attempt$Attempt.stdout.log"
    $StdErrPath = Join-Path $TempLogDir "$SafeName.attempt$Attempt.stderr.log"
    $OutputDir = Get-ConfigOutputDir -ConfigPath $ConfigPath
    $StartedAt = Get-Date

    $Process = Start-Process `
        -FilePath $PythonExe `
        -ArgumentList @("-m", "src.experiment.runner", "--config", $ConfigPath) `
        -WorkingDirectory (Get-Location).Path `
        -WindowStyle Hidden `
        -RedirectStandardOutput $StdOutPath `
        -RedirectStandardError $StdErrPath `
        -PassThru

    Write-RunManifest -ExperimentName $ExperimentName -ConfigPath $ConfigPath -OutputDir $OutputDir -Status "running" -StartedAt $StartedAt

    $LastProgressLog = Get-Date
    $LastSnapshot = if ($OutputDir) { Get-InstanceProgressSnapshot -OutputDir $OutputDir } else { $null }

    while (-not $Process.HasExited) {
        Start-Sleep -Seconds 15
        $Process.Refresh()

        if (-not $OutputDir) {
            continue
        }

        $Snapshot = Get-InstanceProgressSnapshot -OutputDir $OutputDir
        if (-not $Snapshot.Exists) {
            continue
        }

        $ShouldLog = $false
        if ($null -eq $LastSnapshot) {
            $ShouldLog = $true
        } elseif ($Snapshot.Count -ne $LastSnapshot.Count) {
            $ShouldLog = $true
        } elseif (((Get-Date) - $LastProgressLog).TotalMinutes -ge 5) {
            $ShouldLog = $true
        }

        if ($ShouldLog) {
            $AgeText = if ($Snapshot.LatestWrite) {
                [math]::Round(((Get-Date) - $Snapshot.LatestWrite).TotalMinutes, 1)
            } else {
                "n/a"
            }

            Write-Log "[PROGRESS] $ExperimentName instances=$($Snapshot.Count) latest_write_age_min=$AgeText dir=$($Snapshot.InstancesDir)"
            Write-RunManifest -ExperimentName $ExperimentName -ConfigPath $ConfigPath -OutputDir $OutputDir -Status "running" -StartedAt $StartedAt
            $LastProgressLog = Get-Date
            $LastSnapshot = $Snapshot
        }
    }

    $Process.Refresh()
    Append-ProcessLogs -StdOutPath $StdOutPath -StdErrPath $StdErrPath
    Write-RunManifest -ExperimentName $ExperimentName -ConfigPath $ConfigPath -OutputDir $OutputDir -Status "process_exited" -StartedAt $StartedAt -ExitCode $Process.ExitCode
    return $Process.ExitCode
}

$CurrentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"==========================================================" | Out-File -FilePath $LogFile -Append
"Starting Managed Experiment Runner at $CurrentDate" | Out-File -FilePath $LogFile -Append
"Worker ID: $WorkerId" | Out-File -FilePath $LogFile -Append
"Worker results branch: $ResultsBranch" | Out-File -FilePath $LogFile -Append
"==========================================================" | Out-File -FilePath $LogFile -Append

$BranchReady = Invoke-WithGitMutex -Reason "managed_runner_branch_setup" -Action {
    Ensure-ResultsBranch
}
if (-not $BranchReady) {
    Write-Log "[FATAL] Could not enter worker result branch $ResultsBranch. Exiting to protect results."
    exit 1
}

# Start background sync daemon
try {
    $SyncProcess = Start-Process powershell -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ".\scripts\auto_push.ps1") -PassThru -WindowStyle Hidden
    "Started background Git sync daemon (PID: $($SyncProcess.Id))" | Out-File -FilePath $LogFile -Append
} catch {
    "Failed to start sync daemon: $_" | Out-File -FilePath $LogFile -Append
}

try {
    while ($true) {
        $MissingList = Get-MissingExperimentList
        $ExpName = $MissingList | Select-Object -First 1
        if ([string]::IsNullOrWhiteSpace($ExpName)) {
            Write-Log "[INFO] No missing experiments remain. Exiting managed runner."
            break
        }

        $ConfigPath = "configs/experiments/exp2_scaled/$ExpName.yaml"
        
        if (-not (Test-Path -Path $ConfigPath)) {
            "[ERROR] Config not found: $ConfigPath" | Out-File -FilePath $LogFile -Append
            continue
        }

        $CurrentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        "----------------------------------------------------------" | Out-File -FilePath $LogFile -Append
        "[$CurrentDate] Starting experiment: $ExpName" | Out-File -FilePath $LogFile -Append

        $script:ManagedRunnerCurrentBranch = $null
        $RefreshOk = Invoke-WithGitMutex -Reason "managed_runner_refresh" -Action {
            $BranchResult = Get-GitCommandOutput -Arguments @("rev-parse", "--abbrev-ref", "HEAD")
            $script:ManagedRunnerCurrentBranch = @($BranchResult.Output)[-1]
            if ($BranchResult.ExitCode -ne 0 -or [string]::IsNullOrWhiteSpace($script:ManagedRunnerCurrentBranch)) {
                Write-Log "[ERROR] Failed to resolve current branch. Skipping $ExpName."
                return $false
            }

            Write-Log "[GIT] Fetching origin/main for visibility without modifying local results..."
            $FetchExitCode = Invoke-GitLogged -Arguments @("fetch", "--no-progress", "origin", "main")
            if ($FetchExitCode -eq 0) {
                Write-Log "[GIT] Fetched origin/main. Local worker results were left untouched to avoid cross-worker collisions."
            } else {
                Write-Log "[WARN] Fetch failed; continuing with local worker branch state."
            }

            return $true
        }

        $CurrentBranch = $script:ManagedRunnerCurrentBranch
        if (-not $RefreshOk -or [string]::IsNullOrWhiteSpace($CurrentBranch)) {
            Start-Sleep -Seconds 2
            continue
        }

        $OutputDir = Get-ConfigOutputDir -ConfigPath $ConfigPath
        if (-not [string]::IsNullOrWhiteSpace($OutputDir)) {
            $ResultsFile = Join-Path $OutputDir "results.json"
            if (Test-Path -Path $ResultsFile) {
                Write-Log "[SKIP] $ExpName already exists after queue refresh. Another worker likely completed it."
                Write-RunManifest -ExperimentName $ExpName -ConfigPath $ConfigPath -OutputDir $OutputDir -Status "skipped_existing_results" -StartedAt (Get-Date)
                Start-Sleep -Seconds 2
                continue
            }
        }

        # Run the experiment in an isolated child process so a console/window
        # close event does not kill the whole batch runner.
        $ExitCode = Invoke-ExperimentProcess -ConfigPath $ConfigPath -ExperimentName $ExpName -Attempt 1
        $RetryReason = $null

        if ($ExitCode -ne 0) {
            $RecentTail = if (Test-Path $LogFile) { Get-Content -Path $LogFile -Tail 80 -ErrorAction SilentlyContinue } else { @() }
            if ($RecentTail -match 'forrtl: error \(200\): program aborting due to window-CLOSE event') {
                $RetryReason = "window-close event"
                Write-Log "[WARN] Experiment $ExpName aborted due to $RetryReason. Retrying once in a detached child process..."
                Start-Sleep -Seconds 3
                $ExitCode = Invoke-ExperimentProcess -ConfigPath $ConfigPath -ExperimentName $ExpName -Attempt 2
            }
        }

        if ($ExitCode -eq 0) {
            "[SUCCESS] Finished $ExpName" | Out-File -FilePath $LogFile -Append
            Write-RunManifest -ExperimentName $ExpName -ConfigPath $ConfigPath -OutputDir $OutputDir -Status "success" -StartedAt (Get-Date) -ExitCode $ExitCode
            
            # Automatic Git Commit
            "[GIT] Committing results for $ExpName" | Out-File -FilePath $LogFile -Append
            Invoke-WithGitMutex -Reason "managed_runner_commit" -Action {
                $AddArguments = @("add", "--") + $TrackedPaths
                $AddExitCode = Invoke-GitLogged -Arguments $AddArguments
                if ($AddExitCode -ne 0) {
                    Write-Log "[WARN] Git add failed for $ExpName; preserving files for the next sync cycle."
                    return
                }

                $PendingResultChanges = Get-GitStatusPorcelain -TrackedPath $ResultsPath
                $PendingManifestChanges = Get-GitStatusPorcelain -TrackedPath "experiments/exp2_scaled/worker_manifests"

                if ($null -eq $PendingResultChanges) {
                    Write-Log "[WARN] Failed to inspect pending result changes."
                    return
                }
                if ($null -eq $PendingManifestChanges) {
                    Write-Log "[WARN] Failed to inspect pending manifest changes."
                    return
                }

                if (($PendingResultChanges.Count + $PendingManifestChanges.Count) -gt 0) {
                    $CommitExitCode = Invoke-GitLogged -Arguments @("commit", "-m", "Auto-commit: Results for $ExpName")
                    if ($CommitExitCode -eq 0) {
                        Write-Log "[GIT] Results committed locally for $ExpName. Push is handled by auto_push.ps1 on the 6-hour schedule."
                    } else {
                        Write-Log "[WARN] Commit failed for $ExpName."
                    }
                } else {
                    Write-Log "[GIT] No new result changes detected for $ExpName."
                }
            } | Out-Null
        } else {
            if ($RetryReason) {
                "[FAILED] Experiment $ExpName failed after retry. Check logs." | Out-File -FilePath $LogFile -Append
            } else {
                "[FAILED] Experiment $ExpName failed. Check logs." | Out-File -FilePath $LogFile -Append
            }
            Write-RunManifest -ExperimentName $ExpName -ConfigPath $ConfigPath -OutputDir $OutputDir -Status "failed" -StartedAt (Get-Date) -ExitCode $ExitCode
        }
        
        # Cooldown
        Start-Sleep -Seconds 5
    }
} catch {
    Write-Log "[FATAL] $_"
} finally {
    $CurrentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "==========================================================" | Out-File -FilePath $LogFile -Append
    "Managed Runner finished at $CurrentDate" | Out-File -FilePath $LogFile -Append
    "==========================================================" | Out-File -FilePath $LogFile -Append

    # Cleanup sync process
    if ($SyncProcess -and -not $SyncProcess.HasExited) {
        Stop-Process -Id $SyncProcess.Id -Force -ErrorAction SilentlyContinue
        "Stopped background Git sync daemon." | Out-File -FilePath $LogFile -Append
    }
}
