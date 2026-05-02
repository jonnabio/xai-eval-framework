# Always render from the thesis project directory (where `_quarto.yml` lives).
Set-Location $PSScriptRoot

if (!$env:ComSpec) { $env:ComSpec = Join-Path $env:WINDIR "System32\cmd.exe" }
if (!$env:PATHEXT) { $env:PATHEXT = ".COM;.EXE;.BAT;.CMD" }
if ($env:PATH -notlike "*$($env:WINDIR)\System32*") {
    $env:PATH = "$($env:WINDIR)\System32;$env:PATH"
}

# Ensure output directory exists
$outDir = Join-Path $PSScriptRoot "_output"
if (!(Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir }

Write-Host "Starting Thesis Render..." -ForegroundColor Cyan

$repoRoot = Split-Path $PSScriptRoot -Parent
$formatScript = Join-Path $repoRoot "scripts\enforce_docx_thesis_format.py"

function Set-DocxBodyStyleFallback {
    param(
        [Parameter(Mandatory = $true)][string]$DocxPath,
        [switch]$Check
    )

    Add-Type -AssemblyName System.IO.Compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem

    $bodyStyleIds = @(
        "Normal",
        "Default",
        "Textoindependiente",
        "BodyText",
        "Prrafodelista",
        "ListParagraph",
        "Bibliography",
        "FirstParagraph",
        "Compact",
        "BlockText"
    )

    $zip = [System.IO.Compression.ZipFile]::Open($DocxPath, [System.IO.Compression.ZipArchiveMode]::Update)
    try {
        $entry = $zip.GetEntry("word/styles.xml")
        if (!$entry) {
            throw "word/styles.xml not found in $DocxPath"
        }

        $reader = New-Object System.IO.StreamReader($entry.Open())
        try {
            [xml]$stylesXml = $reader.ReadToEnd()
        } finally {
            $reader.Close()
        }

        $ns = New-Object System.Xml.XmlNamespaceManager($stylesXml.NameTable)
        $ns.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")
        $wNs = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        $changed = $false

        foreach ($styleId in $bodyStyleIds) {
            $style = $stylesXml.SelectSingleNode("//w:style[@w:type='paragraph' and @w:styleId='$styleId']", $ns)
            if (!$style) { continue }

            $pPr = $style.SelectSingleNode("w:pPr", $ns)
            if (!$pPr) {
                $pPr = $stylesXml.CreateElement("w", "pPr", $wNs)
                [void]$style.AppendChild($pPr)
                $changed = $true
            }

            $jc = $pPr.SelectSingleNode("w:jc", $ns)
            if (!$jc) {
                $jc = $stylesXml.CreateElement("w", "jc", $wNs)
                [void]$pPr.AppendChild($jc)
                $changed = $true
            }
            if ($jc.GetAttribute("val", $wNs) -ne "both") {
                $jc.SetAttribute("val", $wNs, "both")
                $changed = $true
            }

            $spacing = $pPr.SelectSingleNode("w:spacing", $ns)
            if (!$spacing) {
                $spacing = $stylesXml.CreateElement("w", "spacing", $wNs)
                [void]$pPr.AppendChild($spacing)
                $changed = $true
            }
            if ($spacing.GetAttribute("line", $wNs) -ne "480") {
                $spacing.SetAttribute("line", $wNs, "480")
                $changed = $true
            }
            if ($spacing.GetAttribute("lineRule", $wNs) -ne "auto") {
                $spacing.SetAttribute("lineRule", $wNs, "auto")
                $changed = $true
            }
        }

        if ($Check) {
            foreach ($styleId in $bodyStyleIds) {
                $style = $stylesXml.SelectSingleNode("//w:style[@w:type='paragraph' and @w:styleId='$styleId']", $ns)
                if (!$style) { continue }
                $jc = $style.SelectSingleNode("w:pPr/w:jc", $ns)
                $spacing = $style.SelectSingleNode("w:pPr/w:spacing", $ns)
                if (!$jc -or $jc.GetAttribute("val", $wNs) -ne "both") {
                    throw "Style $styleId in $DocxPath is not justified."
                }
                if (!$spacing -or $spacing.GetAttribute("line", $wNs) -ne "480" -or $spacing.GetAttribute("lineRule", $wNs) -ne "auto") {
                    throw "Style $styleId in $DocxPath is not double-spaced."
                }
            }
        }

        if ($changed) {
            $entry.Delete()
            $newEntry = $zip.CreateEntry("word/styles.xml")
            $writer = New-Object System.IO.StreamWriter($newEntry.Open(), [System.Text.UTF8Encoding]::new($false))
            try {
                $stylesXml.Save($writer)
            } finally {
                $writer.Close()
            }
        }
        Write-Host "Formatted $DocxPath with PowerShell DOCX style fallback."
    } finally {
        if ($zip) { $zip.Dispose() }
    }
}

function Invoke-DocxFormatEnforcer {
    param(
        [Parameter(Mandatory = $true)][string]$DocxPath,
        [switch]$Check
    )

    if (!(Test-Path $formatScript)) {
        Write-Host "ERROR: Missing DOCX formatting script at $formatScript" -ForegroundColor Red
        exit 1
    }
    if (!(Test-Path $DocxPath)) {
        Write-Host "ERROR: Missing DOCX file at $DocxPath" -ForegroundColor Red
        exit 1
    }

    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        if ($Check) {
            & $python.Source $formatScript $DocxPath --check
        } else {
            & $python.Source $formatScript $DocxPath
        }
    } else {
        $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
        if ($pyLauncher) {
            if ($Check) {
                & $pyLauncher.Source -3 $formatScript $DocxPath --check
            } else {
                & $pyLauncher.Source -3 $formatScript $DocxPath
            }
        } else {
            Set-DocxBodyStyleFallback $DocxPath -Check:$Check
            return
        }
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Thesis DOCX formatting enforcement failed." -ForegroundColor Red
        exit 1
    }
}

function Invoke-Quarto {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)

    $quarto = "C:\Progra~1\Quarto\bin\quarto.exe"
    $systemPath = "$($env:WINDIR)\System32;$($env:WINDIR);$($env:WINDIR)\System32\Wbem"
    $commandLine = "set `"PATH=$systemPath;$env:PATH`" && set `"PATHEXT=$env:PATHEXT`" && $quarto " + ($Arguments -join " ")
    $startInfo = [System.Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = $env:ComSpec
    $startInfo.Arguments = "/c $commandLine"
    $startInfo.WorkingDirectory = $PSScriptRoot
    $startInfo.UseShellExecute = $false
    $startInfo.Environment["Path"] = "$systemPath;$env:PATH"
    $startInfo.Environment["PATH"] = "$systemPath;$env:PATH"
    $startInfo.Environment["PATHEXT"] = $env:PATHEXT
    [void]$startInfo.Environment.Remove("ELECTRON_RUN_AS_NODE")
    $process = [System.Diagnostics.Process]::Start($startInfo)
    $process.WaitForExit()
    if ($process.ExitCode -ne 0) {
        return $false
    }
    return $true
}

# Keep the Word reference template itself compliant before Quarto reads it.
$referenceDoc = Join-Path $PSScriptRoot "assets\Plantilla_Tesis_Doctorado.docx"
Invoke-DocxFormatEnforcer $referenceDoc

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
$renderSucceeded = Invoke-Quarto @("render", "--to", "docx", "--cache-refresh")

if ($renderSucceeded) {
    $expectedDocx = Join-Path $outDir "JHerrera_XAI_Tesis_Doctorado.docx"
    if (Test-Path $expectedDocx) {
        Invoke-DocxFormatEnforcer $expectedDocx -Check
        Write-Host "`nSUCCESS: Thesis rendered to $expectedDocx" -ForegroundColor Green
    } else {
        $latestDocx = Get-ChildItem -Path $outDir -Filter *.docx | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($latestDocx) {
            Invoke-DocxFormatEnforcer $latestDocx.FullName -Check
            Write-Host "`nSUCCESS: Thesis rendered to $($latestDocx.FullName)" -ForegroundColor Green
        } else {
            Write-Host "`nSUCCESS: Thesis rendered to $outDir" -ForegroundColor Green
        }
    }
    Write-Host "Remember to update the Table of Contents in Word manually." -ForegroundColor Yellow
} else {
    Write-Host "`nERROR: Render failed. Check your Quarto installation and .bib files." -ForegroundColor Red
}
