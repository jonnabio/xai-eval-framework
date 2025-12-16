# scripts/build_docs.ps1
# -----------------------------------------------------------------------------
# Documentation Build Script (PowerShell)
# -----------------------------------------------------------------------------

$ErrorActionPreference = "Stop"

Write-Host "====================================================================="
Write-Host "Building XAI Evaluation Framework Documentation"
Write-Host "====================================================================="

# 1. Generate API Docs
Write-Host "[1/4] Generating API documentation from source..."
sphinx-apidoc -f -o docs/api src/

# 2. Build HTML
Write-Host "[2/4] Building HTML documentation..."
sphinx-build -M html docs/ docs/_build

# 3. Generate Coverage
Write-Host "[3/4] Generating documentation coverage report..."
sphinx-build -b coverage docs/ docs/_build/coverage

Write-Host "====================================================================="
Write-Host "Documentation Build Complete!"
Write-Host "====================================================================="
Write-Host "HTML Report:     docs/_build/html/index.html"
Write-Host "Coverage Report: docs/_build/coverage/python.txt"
Write-Host ""
Write-Host "Coverage Summary:"
if (Test-Path docs/_build/coverage/python.txt) {
    Get-Content docs/_build/coverage/python.txt
}
Write-Host "====================================================================="
