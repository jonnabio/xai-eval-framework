# managed_runner.ps1
# Automated experiment runner for Windows (Distributed node)

$LogFile = "logs\managed_runner.log"
$ResultsPath = "experiments/exp2_scaled/results"
$TempLogDir = "logs\runner_temp"
if (-not (Test-Path -Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}
if (-not (Test-Path -Path $TempLogDir)) {
    New-Item -ItemType Directory -Path $TempLogDir | Out-Null
}

function Write-Log {
    param([string]$Message)
    $CurrentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$CurrentDate] $Message" | Out-File -FilePath $LogFile -Append
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
        $OutputDir = @($Script | python - $ConfigPath)[-1]
        return ($OutputDir | Out-String).Trim()
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

    $Process = Start-Process `
        -FilePath "python" `
        -ArgumentList @("-m", "src.experiment.runner", "--config", $ConfigPath) `
        -WorkingDirectory (Get-Location).Path `
        -WindowStyle Hidden `
        -RedirectStandardOutput $StdOutPath `
        -RedirectStandardError $StdErrPath `
        -PassThru

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
            $LastProgressLog = Get-Date
            $LastSnapshot = $Snapshot
        }
    }

    $Process.Refresh()
    Append-ProcessLogs -StdOutPath $StdOutPath -StdErrPath $StdErrPath
    return $Process.ExitCode
}

$CurrentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"==========================================================" | Out-File -FilePath $LogFile -Append
"Starting Managed Experiment Runner at $CurrentDate" | Out-File -FilePath $LogFile -Append
"==========================================================" | Out-File -FilePath $LogFile -Append

# Start background sync daemon
try {
    $SyncProcess = Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File .\scripts\auto_push.ps1" -PassThru -WindowStyle Hidden
    "Started background Git sync daemon (PID: $($SyncProcess.Id))" | Out-File -FilePath $LogFile -Append
} catch {
    "Failed to start sync daemon: $_" | Out-File -FilePath $LogFile -Append
}

try {
    $MissingOutput = python scripts/check_missing_results.py
    $MissingList = $MissingOutput | Select-Object -Skip 1

    foreach ($ExpName in $MissingList) {
        if ([string]::IsNullOrWhiteSpace($ExpName)) {
            continue
        }

        $ConfigPath = "configs/experiments/exp2_scaled/$ExpName.yaml"
        
        if (-not (Test-Path -Path $ConfigPath)) {
            "[ERROR] Config not found: $ConfigPath" | Out-File -FilePath $LogFile -Append
            continue
        }

        $CurrentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        "----------------------------------------------------------" | Out-File -FilePath $LogFile -Append
        "[$CurrentDate] Starting experiment: $ExpName" | Out-File -FilePath $LogFile -Append

        $CurrentBranch = git rev-parse --abbrev-ref HEAD
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($CurrentBranch)) {
            Write-Log "[ERROR] Failed to resolve current branch. Skipping $ExpName."
            continue
        }

        Write-Log "[GIT] Fetching latest queue state for $ResultsPath..."
        git fetch --no-progress origin $CurrentBranch 2>&1 | Out-File -FilePath $LogFile -Append
        if ($LASTEXITCODE -eq 0) {
            git diff --quiet HEAD "origin/$CurrentBranch" -- $ResultsPath
            if ($LASTEXITCODE -ne 0) {
                git restore --source "origin/$CurrentBranch" --staged --worktree -- $ResultsPath 2>&1 | Out-File -FilePath $LogFile -Append
                if ($LASTEXITCODE -eq 0) {
                    Write-Log "[GIT] Updated local result queue from origin/$CurrentBranch."
                } else {
                    Write-Log "[WARN] Failed to refresh $ResultsPath from origin/$CurrentBranch."
                }
            } else {
                Write-Log "[GIT] Local result queue already matches origin/$CurrentBranch."
            }
        } else {
            Write-Log "[WARN] Fetch failed; continuing with local queue state."
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
            
            # Automatic Git Commit
            "[GIT] Committing results for $ExpName" | Out-File -FilePath $LogFile -Append
            git add -- $ResultsPath 2>&1 | Out-File -FilePath $LogFile -Append
            $PendingResultChanges = git status --porcelain -- $ResultsPath

            if ($PendingResultChanges) {
                git commit -m "Auto-commit: Results for $ExpName" 2>&1 | Out-File -FilePath $LogFile -Append
                if ($LASTEXITCODE -eq 0) {
                    git push origin "HEAD:$CurrentBranch" 2>&1 | Out-File -FilePath $LogFile -Append
                    if ($LASTEXITCODE -ne 0) {
                        Write-Log "[WARN] Push failed for $ExpName; results remain committed locally."
                    }
                } else {
                    Write-Log "[WARN] Commit failed for $ExpName."
                }
            } else {
                Write-Log "[GIT] No new result changes detected for $ExpName."
            }
        } else {
            if ($RetryReason) {
                "[FAILED] Experiment $ExpName failed after retry. Check logs." | Out-File -FilePath $LogFile -Append
            } else {
                "[FAILED] Experiment $ExpName failed. Check logs." | Out-File -FilePath $LogFile -Append
            }
        }
        
        # Cooldown
        Start-Sleep -Seconds 5
    }
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
