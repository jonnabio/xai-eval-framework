# managed_runner.ps1
# Automated experiment runner for Windows (Distributed node)

$LogFile = "logs\managed_runner.log"
if (-not (Test-Path -Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

$CurrentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"==========================================================" | Out-File -FilePath $LogFile -Append
"Starting Managed Experiment Runner at $CurrentDate" | Out-File -FilePath $LogFile -Append
"==========================================================" | Out-File -FilePath $LogFile -Append

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
    
    "[GIT] Pulling latest results from distributed queue..." | Out-File -FilePath $LogFile -Append
    $CurrentBranch = git rev-parse --abbrev-ref HEAD
    git pull --rebase origin $CurrentBranch

    # Run the experiment
    python -m src.experiment.runner --config "$ConfigPath" 2>&1 | Out-File -FilePath $LogFile -Append
    
    if ($LASTEXITCODE -eq 0) {
        "[SUCCESS] Finished $ExpName" | Out-File -FilePath $LogFile -Append
        
        # Automatic Git Commit
        "[GIT] Committing results for $ExpName" | Out-File -FilePath $LogFile -Append
        git add experiments/exp2_scaled/results/
        git commit -m "Auto-commit: Results for $ExpName"
        git push origin HEAD
    } else {
        "[FAILED] Experiment $ExpName failed. Check logs." | Out-File -FilePath $LogFile -Append
    }
    
    # Cooldown
    Start-Sleep -Seconds 5
}

$CurrentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"==========================================================" | Out-File -FilePath $LogFile -Append
"Managed Runner finished at $CurrentDate" | Out-File -FilePath $LogFile -Append
"==========================================================" | Out-File -FilePath $LogFile -Append
