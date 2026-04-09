# managed_runner.ps1
# Automated experiment runner for Windows (Distributed node)

$LogFile = "logs\managed_runner.log"
$ResultsPath = "experiments/exp2_scaled/results"
if (-not (Test-Path -Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

function Write-Log {
    param([string]$Message)
    $CurrentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$CurrentDate] $Message" | Out-File -FilePath $LogFile -Append
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
        git fetch origin $CurrentBranch 2>&1 | Out-File -FilePath $LogFile -Append
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

        # Run the experiment
        python -m src.experiment.runner --config "$ConfigPath" 2>&1 | Out-File -FilePath $LogFile -Append
        
        if ($LASTEXITCODE -eq 0) {
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
            "[FAILED] Experiment $ExpName failed. Check logs." | Out-File -FilePath $LogFile -Append
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
