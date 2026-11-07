
param([string]$orig, [string]$rev, [string]$out, [string]$pdf)
$ErrorActionPreference = "Stop"
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
$o = $null; $r = $null; $c = $null
try {
  $o = $w.Documents.Open($orig, $false, $true)
  $r = $w.Documents.Open($rev, $false, $true)
  # Destination new document (2), word-level granularity (1); author kept neutral (masked).
  $c = $w.CompareDocuments($o, $r, 2, 1, $true, $true, $true, $true, $true, $true, $true, $true, $true, $true, "Author", $true)
  $c.SaveAs2($out, 12)
  $c.ActiveWindow.View.RevisionsFilter.Markup = 2
  $c.ActiveWindow.View.ShowRevisionsAndComments = $true
  # PDF with the markup (Item 7 = document with markup).
  $c.ExportAsFixedFormat($pdf, 17, $false, 0, 0, 1, 1, 7, $true, $true, 0, $true, $true, $false)
  "revisions=" + $c.Revisions.Count
} finally {
  # Always release the files, even after an error (a hidden Word would keep them locked).
  foreach ($d in @($c, $r, $o)) { if ($d) { try { $d.Close(0) } catch {} } }
  $w.Quit()
}
