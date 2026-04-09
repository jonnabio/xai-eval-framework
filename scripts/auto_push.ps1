# scripts/auto_push.ps1
# Periodic git sync for experiment results and logs only.

$Interval = 900 # 15 minutes
$LogFile = "logs\auto_push.log"
$TrackedPaths = @(
    "experiments/exp2_scaled/results",
    "logs"
)

if (-not (Test-Path -Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

function Write-Log {
    param([string]$Message)
    $DateStr = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$DateStr] $Message" | Out-File -FilePath $LogFile -Append
}

while ($true) {
    Write-Log "Syncing progress with Git pool..."

    $CurrentBranch = git rev-parse --abbrev-ref HEAD
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($CurrentBranch)) {
        Write-Log "Error resolving current branch."
        Start-Sleep -Seconds $Interval
        continue
    }

    # Stage only experiment outputs and logs. This avoids sweeping in
    # locally retrained model binaries, config edits, or other workspace changes.
    git add -- $TrackedPaths 2>&1 | Out-File -FilePath $LogFile -Append

    $PendingChanges = git status --porcelain -- $TrackedPaths
    if ($LASTEXITCODE -ne 0) {
        Write-Log "Failed to inspect pending changes."
        Start-Sleep -Seconds $Interval
        continue
    }

    if ($PendingChanges) {
        git commit -m "Auto-sync queue: Results and logs checkpoint" 2>&1 | Out-File -FilePath $LogFile -Append
        if ($LASTEXITCODE -ne 0) {
            Write-Log "Commit failed; skipping pull/push for this cycle."
            Start-Sleep -Seconds $Interval
            continue
        }
    } else {
        Write-Log "No result/log changes to commit."
    }

    git pull --rebase --autostash origin $CurrentBranch 2>&1 | Out-File -FilePath $LogFile -Append
    if ($LASTEXITCODE -ne 0) {
        Write-Log "Pull --rebase failed; manual review may be required."
        Start-Sleep -Seconds $Interval
        continue
    }

    git push origin $CurrentBranch 2>&1 | Out-File -FilePath $LogFile -Append
    if ($LASTEXITCODE -ne 0) {
        Write-Log "Push failed; changes remain local for the next sync cycle."
    } else {
        Write-Log "Sync complete."
    }

    Write-Log "Sleeping for $Interval seconds..."
    Start-Sleep -Seconds $Interval
}
