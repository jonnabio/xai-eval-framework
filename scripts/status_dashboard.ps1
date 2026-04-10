# Launch the cross-platform terminal dashboard on Windows.

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$BootstrapPaths = @(
    "C:\ProgramData\anaconda3",
    "C:\ProgramData\anaconda3\Scripts"
)
foreach ($BootstrapPath in $BootstrapPaths) {
    if ((Test-Path -Path $BootstrapPath) -and -not (($env:Path -split ';') -contains $BootstrapPath)) {
        $env:Path = "$BootstrapPath;$env:Path"
    }
}

$PythonExe = if (Test-Path "C:\ProgramData\anaconda3\python.exe") {
    "C:\ProgramData\anaconda3\python.exe"
} else {
    (Get-Command python -ErrorAction Stop).Source
}

& $PythonExe .\scripts\status_dashboard.py
