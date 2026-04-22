# Always render from the thesis project directory (where `_quarto.yml` lives).
Set-Location $PSScriptRoot

# Ensure output directory exists
$outDir = Join-Path $PSScriptRoot "_output"
if (!(Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir }

Write-Host "Starting Thesis Render..." -ForegroundColor Cyan

# Defensive clean: avoids stale `.quarto` / `_freeze` artifacts and prevents Word
# locks from leaving an old DOCX in place. Also prevents confusion if the output
# filename changes (e.g., after editing `book.title`).
try {
    Get-ChildItem -Path $outDir -Filter *.docx -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction Stop
} catch {
    Write-Host "ERROR: Cannot delete existing DOCX files in $outDir. Close any open Word documents and try again." -ForegroundColor Red
    exit 1
}

if (Test-Path (Join-Path $PSScriptRoot ".quarto")) { Remove-Item -Recurse -Force (Join-Path $PSScriptRoot ".quarto") }
if (Test-Path (Join-Path $PSScriptRoot "_freeze")) { Remove-Item -Recurse -Force (Join-Path $PSScriptRoot "_freeze") }

# Render the full book using `_quarto.yml`
& "C:\Program Files\Quarto\bin\quarto.exe" clean
& "C:\Program Files\Quarto\bin\quarto.exe" render --to docx --cache-refresh

if ($LASTEXITCODE -eq 0) {
    $expectedDocx = Join-Path $outDir "JHerrera_XAI_Tesis_Doctorado.docx"
    if (Test-Path $expectedDocx) {
        Write-Host "`nSUCCESS: Thesis rendered to $expectedDocx" -ForegroundColor Green
    } else {
        $latestDocx = Get-ChildItem -Path $outDir -Filter *.docx | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($latestDocx) {
            Write-Host "`nSUCCESS: Thesis rendered to $($latestDocx.FullName)" -ForegroundColor Green
        } else {
            Write-Host "`nSUCCESS: Thesis rendered to $outDir" -ForegroundColor Green
        }
    }
    Write-Host "Remember to update the Table of Contents in Word manually." -ForegroundColor Yellow
} else {
    Write-Host "`nERROR: Render failed. Check your Quarto installation and .bib files." -ForegroundColor Red
}
