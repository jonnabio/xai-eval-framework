# Install a Windows scheduled task for EXP3 email status reports every 3 hours.

param(
    [Parameter(Mandatory = $true)]
    [string]$GmailAppPassword,
    [string]$ToEmail = $(if ($env:XAI_REPORT_TO) { $env:XAI_REPORT_TO } else { "jonnabio@gmail.com" }),
    [string]$TaskName = "XAI EXP3 Email Report",
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if ([string]::IsNullOrWhiteSpace($PythonExe)) {
    if (Test-Path ".\.venv-exp3\Scripts\python.exe") {
        $PythonExe = (Resolve-Path ".\.venv-exp3\Scripts\python.exe").Path
    } elseif (Test-Path ".\.venv\Scripts\python.exe") {
        $PythonExe = (Resolve-Path ".\.venv\Scripts\python.exe").Path
    } else {
        $PythonExe = (Get-Command python -ErrorAction Stop).Source
    }
}

$ScriptPath = Join-Path $ProjectRoot "scripts\email_report.py"
$LogPath = Join-Path $ProjectRoot "logs\email_report_task.log"
New-Item -ItemType Directory -Path (Join-Path $ProjectRoot "logs") -Force | Out-Null

$Command = @"
`$env:GMAIL_APP_PASSWORD='$GmailAppPassword'; `$env:XAI_REPORT_TO='$ToEmail'; Set-Location '$ProjectRoot'; & '$PythonExe' '$ScriptPath' --experiment 'EXP3 Cross-Dataset' --config-dir 'configs/experiments/exp3_cross_dataset' --results-dir 'experiments/exp3_cross_dataset/results' --log-file 'logs/setup_exp3_windows.log' >> '$LogPath' 2>&1
"@

$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -Command $Command"
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) -RepetitionInterval (New-TimeSpan -Hours 3)
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description "Send EXP3 XAI framework progress report every 3 hours." `
    -Force | Out-Null

Write-Host "Success! EXP3 status email report task is scheduled every 3 hours."
Write-Host "Task: $TaskName"
Write-Host "Recipient: $ToEmail"
Write-Host "Python: $PythonExe"
Write-Host "Log: $LogPath"
