# Ensure output directory exists
$outDir = "d:\Github\xai-eval-framework\thesis\_output"
if (!(Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir }

Write-Host "Starting Thesis Render..." -ForegroundColor Cyan

# Rendering the thesis to Word using Quarto
quarto render index.qmd --to docx

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nSUCCESS: Thesis rendered to $outDir/index.docx" -ForegroundColor Green
    Write-Host "Remember to update the Table of Contents in Word manually." -ForegroundColor Yellow
} else {
    Write-Host "`nERROR: Render failed. Check your Quarto installation and .bib files." -ForegroundColor Red
}
