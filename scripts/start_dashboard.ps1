# scripts/start_dashboard.ps1
# One-click launch script for XAI Eval Framework + Dashboard (Windows)
# Usage: .\scripts\start_dashboard.ps1

Write-Host "==============================================" -ForegroundColor Blue
Write-Host "   XAI EVAL FRAMEWORK - DASHBOARD LAUNCHER    " -ForegroundColor Blue
Write-Host "==============================================" -ForegroundColor Blue

$DashboardDir = "..\xai-benchmark"

if (-not (Test-Path $DashboardDir)) {
    Write-Host "Error: Dashboard directory not found at $DashboardDir" -ForegroundColor Red
    Write-Host "Please ensure xai-benchmark repo is cloned as a sibling directory."
    exit 1
}

$ApiProcess = $null
$UiProcess = $null

try {
    Write-Host "[1/2] Starting API Server (Port 8000)..." -ForegroundColor Green
    $ApiProcess = Start-Process python -ArgumentList "-m src.api.main" -PassThru -NoNewWindow
    
    Start-Sleep -Seconds 3
    
    if ($ApiProcess.HasExited) {
        Write-Host "API Server failed to start!" -ForegroundColor Red
        exit 1
    }

    Write-Host "[2/2] Starting Dashboard UI (Port 3000)..." -ForegroundColor Green
    
    if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
        Write-Host "npm could not be found. Please install Node.js." -ForegroundColor Red
        if ($ApiProcess -and -not $ApiProcess.HasExited) { Stop-Process -Id $ApiProcess.Id -Force }
        exit 1
    }

    Push-Location $DashboardDir
    $UiProcess = Start-Process npm.cmd -ArgumentList "run dev" -PassThru -NoNewWindow
    Pop-Location

    Write-Host "==============================================" -ForegroundColor Blue
    Write-Host "Services are running!" -ForegroundColor Green
    Write-Host "API:       http://localhost:8000"
    Write-Host "Dashboard: http://localhost:3000"
    Write-Host "==============================================" -ForegroundColor Blue
    Write-Host "Press Ctrl+C to stop everything."

    # Keep script running to allow Ctrl+C trap
    while ($true) {
        Start-Sleep -Seconds 1
        if ($ApiProcess.HasExited -and $UiProcess.HasExited) {
            break
        }
    }
}
finally {
    Write-Host "`nShutting down services..." -ForegroundColor Red
    if ($ApiProcess -and -not $ApiProcess.HasExited) {
        Stop-Process -Id $ApiProcess.Id -Force -ErrorAction SilentlyContinue
    }
    if ($UiProcess -and -not $UiProcess.HasExited) {
        # Taskkill /T kills the entire process tree (important for npm.cmd -> node.exe)
        taskkill.exe /PID $UiProcess.Id /T /F 2>&1 | Out-Null
    }
}
