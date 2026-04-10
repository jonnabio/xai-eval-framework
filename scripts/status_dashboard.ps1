# Launch the cross-platform terminal dashboard on Windows.

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

python .\scripts\status_dashboard.py
