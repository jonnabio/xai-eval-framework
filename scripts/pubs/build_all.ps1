Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $repoRoot

python scripts/pubs/generate_fragments.py
python scripts/pubs/verify_sync.py

if (Test-Path "$repoRoot\\thesis\\render.ps1") {
    powershell -ExecutionPolicy Bypass -File "$repoRoot\\thesis\\render.ps1"
} else {
    Write-Host "WARN: thesis/render.ps1 not found; skipping thesis render" -ForegroundColor Yellow
}

Write-Host "DONE" -ForegroundColor Green

