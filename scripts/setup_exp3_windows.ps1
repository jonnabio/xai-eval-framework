# scripts/setup_exp3_windows.ps1
# Create a Windows Python 3.11 EXP3 environment, verify dependencies, and run
# the Breast Cancer RF/SHAP seed-42 smoke gate.
#
# Usage:
#   .\scripts\setup_exp3_windows.ps1
#   .\scripts\setup_exp3_windows.ps1 -RunBreastCancerPartition
#   .\scripts\setup_exp3_windows.ps1 -RecreateVenv

[CmdletBinding()]
param(
    [string]$VenvDir = ".venv-exp3",
    [string]$Requirements = "requirements.txt",
    [switch]$RecreateVenv,
    [switch]$SkipInstall,
    [switch]$RunBreastCancerPartition
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$LogDir = "logs"
if (-not (Test-Path -Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}

$LogFile = Join-Path $LogDir "setup_exp3_windows.log"

function Write-Step {
    param([string]$Message)

    $Stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $Line = "[$Stamp] $Message"
    Write-Host $Line
    $Line | Out-File -FilePath $LogFile -Append
}

function Invoke-Logged {
    param(
        [string]$FilePath,
        [string[]]$Arguments
    )

    Write-Step "RUN: $FilePath $($Arguments -join ' ')"
    & $FilePath @Arguments 2>&1 | Tee-Object -FilePath $LogFile -Append
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $FilePath $($Arguments -join ' ')"
    }
}

function Resolve-Python311 {
    $PyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($PyLauncher) {
        & $PyLauncher.Source -3.11 --version 2>&1 | Tee-Object -FilePath $LogFile -Append
        if ($LASTEXITCODE -eq 0) {
            return @{
                FilePath = $PyLauncher.Source
                Arguments = @("-3.11")
                Display = "py -3.11"
            }
        }
    }

    $Python311 = Get-Command python3.11 -ErrorAction SilentlyContinue
    if ($Python311) {
        & $Python311.Source --version 2>&1 | Tee-Object -FilePath $LogFile -Append
        if ($LASTEXITCODE -eq 0) {
            return @{
                FilePath = $Python311.Source
                Arguments = @()
                Display = $Python311.Source
            }
        }
    }

    throw "Python 3.11 was not found. Install Python 3.11, then rerun this script."
}

function Invoke-Python {
    param(
        [string]$PythonExe,
        [string[]]$Arguments
    )

    Invoke-Logged -FilePath $PythonExe -Arguments $Arguments
}

Write-Step "=========================================================="
Write-Step "EXP3 Windows setup starting"
Write-Step "Repo: $ProjectRoot"
Write-Step "Venv: $VenvDir"
Write-Step "Requirements: $Requirements"
Write-Step "RunBreastCancerPartition: $RunBreastCancerPartition"
Write-Step "=========================================================="

if (-not (Test-Path -Path $Requirements) -and -not $SkipInstall) {
    throw "Requirements file not found: $Requirements"
}

$Python311 = Resolve-Python311
Write-Step "Using Python launcher: $($Python311.Display)"

if ($RecreateVenv -and (Test-Path -Path $VenvDir)) {
    Write-Step "Removing existing venv: $VenvDir"
    Remove-Item -Path $VenvDir -Recurse -Force
}

$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
if (-not (Test-Path -Path $VenvPython)) {
    Write-Step "Creating venv with Python 3.11"
    $CreateVenvArgs = $Python311.Arguments + @("-m", "venv", $VenvDir)
    & $Python311.FilePath @CreateVenvArgs 2>&1 |
        Tee-Object -FilePath $LogFile -Append
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create venv: $VenvDir"
    }
} else {
    Write-Step "Venv already exists; skipping create."
}

Invoke-Python -PythonExe $VenvPython -Arguments @("--version")

if (-not $SkipInstall) {
    Invoke-Python -PythonExe $VenvPython -Arguments @("-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel")
    Invoke-Python -PythonExe $VenvPython -Arguments @("-m", "pip", "install", "-r", $Requirements)
} else {
    Write-Step "Skipping dependency install because -SkipInstall was provided."
}

Write-Step "Running EXP3 dependency preflight"
$Preflight = @"
import importlib
import sys

mods = ["yaml", "numpy", "pandas", "sklearn", "xgboost", "shap", "alibi", "joblib"]
failed = []
for mod in mods:
    try:
        importlib.import_module(mod)
    except Exception as exc:
        failed.append((mod, repr(exc)))

if failed:
    print("FAILED IMPORTS:")
    for mod, msg in failed:
        print(f"- {mod}: {msg}")
    sys.exit(1)

print("EXP3 Windows dependencies OK")
"@

$PreflightPath = Join-Path $LogDir "exp3_windows_preflight.py"
Set-Content -Path $PreflightPath -Value $Preflight -Encoding UTF8
try {
    Invoke-Python -PythonExe $VenvPython -Arguments @($PreflightPath)
} finally {
    Remove-Item -Path $PreflightPath -Force -ErrorAction SilentlyContinue
}

$ConfigCount = (Get-ChildItem "configs\experiments\exp3_cross_dataset" -Recurse -Filter "*.yaml" |
    Where-Object { $_.Name -ne "manifest.yaml" }).Count
Write-Step "EXP3 config count: $ConfigCount"
if ($ConfigCount -ne 24) {
    throw "Expected 24 EXP3 configs, found $ConfigCount."
}

Write-Step "Training Breast Cancer RF seed-42 smoke model artifact"
Invoke-Python -PythonExe $VenvPython -Arguments @(
    "scripts\train_exp3_models.py",
    "--datasets", "breast_cancer",
    "--models", "rf",
    "--seeds", "42"
)

$SmokeConfig = "configs\experiments\exp3_cross_dataset\breast_cancer\rf_shap_s42_n100.yaml"
$SmokeResult = "experiments\exp3_cross_dataset\results\breast_cancer\rf_shap\seed_42\n_100\results.json"

Write-Step "Running EXP3 smoke config: $SmokeConfig"
Invoke-Python -PythonExe $VenvPython -Arguments @("-m", "src.experiment.runner", "--config", $SmokeConfig)

if (-not (Test-Path -Path $SmokeResult)) {
    throw "Smoke run completed but results.json was not found: $SmokeResult"
}

Write-Step "Smoke gate passed: $SmokeResult"

if ($RunBreastCancerPartition) {
    Write-Step "Training all Breast Cancer EXP3 model artifacts"
    Invoke-Python -PythonExe $VenvPython -Arguments @(
        "scripts\train_exp3_models.py",
        "--datasets", "breast_cancer",
        "--models", "rf", "xgb",
        "--seeds", "42", "123", "456"
    )

    $Configs = @(
        "configs\experiments\exp3_cross_dataset\breast_cancer\rf_shap_s42_n100.yaml",
        "configs\experiments\exp3_cross_dataset\breast_cancer\rf_shap_s123_n100.yaml",
        "configs\experiments\exp3_cross_dataset\breast_cancer\rf_shap_s456_n100.yaml",
        "configs\experiments\exp3_cross_dataset\breast_cancer\xgb_shap_s42_n100.yaml",
        "configs\experiments\exp3_cross_dataset\breast_cancer\xgb_shap_s123_n100.yaml",
        "configs\experiments\exp3_cross_dataset\breast_cancer\xgb_shap_s456_n100.yaml",
        "configs\experiments\exp3_cross_dataset\breast_cancer\rf_anchors_s42_n100.yaml",
        "configs\experiments\exp3_cross_dataset\breast_cancer\rf_anchors_s123_n100.yaml",
        "configs\experiments\exp3_cross_dataset\breast_cancer\rf_anchors_s456_n100.yaml",
        "configs\experiments\exp3_cross_dataset\breast_cancer\xgb_anchors_s42_n100.yaml",
        "configs\experiments\exp3_cross_dataset\breast_cancer\xgb_anchors_s123_n100.yaml",
        "configs\experiments\exp3_cross_dataset\breast_cancer\xgb_anchors_s456_n100.yaml"
    )

    foreach ($Config in $Configs) {
        Write-Step "Running Breast Cancer partition config: $Config"
        Invoke-Python -PythonExe $VenvPython -Arguments @("-m", "src.experiment.runner", "--config", $Config)
    }

    $BreastCancerResultCount = (Get-ChildItem "experiments\exp3_cross_dataset\results\breast_cancer" -Recurse -Filter "results.json" -ErrorAction SilentlyContinue).Count
    Write-Step "Breast Cancer result count: $BreastCancerResultCount"
    if ($BreastCancerResultCount -ne 12) {
        throw "Expected 12 Breast Cancer EXP3 results, found $BreastCancerResultCount."
    }

    Write-Step "Breast Cancer partition complete."
} else {
    Write-Step "Breast Cancer partition was not launched. Rerun with -RunBreastCancerPartition after reviewing smoke output."
}

Write-Step "EXP3 Windows setup finished successfully."
