# Paper B revision 1: count Anchors' model calls and rows on XGBoost again (HANDOFF 2026-11-08).
#
# The counter missed XGBClassifier.predict (fixed in f64db3236), so the main timing pass recorded
# 0 calls and 0 rows for Anchors on XGBoost. This reruns only Anchors on the 25 XGBoost timing
# cells with the fixed counter, into its own folder; the main timing results are not touched.
# Only the rows and calls columns are meant to be used, not the times. Waits until the study
# chain has finished (it needs the host to itself), then runs; restartable (done cells skip).
#
#   powershell -ExecutionPolicy Bypass -File scripts\paper_b_xgb_anchors_rows.ps1
$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Py = Join-Path $Root ".venv\Scripts\python.exe"
$Out = Join-Path $Root "outputs\paper_b_rev1_xgb_anchors_rows"
$Chain = Join-Path $Root "outputs\paper_b_rev1_chain.log"
$Notes = Join-Path $Root "outputs\paper_b_rev1_monitor.log"
New-Item -ItemType Directory -Force -Path $Out | Out-Null
Remove-Item Env:PAPER_B_CONFIG -ErrorAction SilentlyContinue

function Note([string]$m) {
    $line = "{0}  {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm"), $m
    Add-Content -Path (Join-Path $Out "run.log") -Value $line -Encoding ascii
    Add-Content -Path $Notes -Value $line -Encoding ascii
}

while (-not (Select-String -Path $Chain -Pattern "chain (finished|stopped)" -Quiet)) { Start-Sleep 60 }
Note "xgb anchors rows rerun: start (25 cells, Anchors only, fixed counter)"
$cells = @()
foreach ($s in 11, 22, 33, 44, 55) { $cells += , @("adult", $s) }
foreach ($d in "breast_cancer", "german_credit", "diabetes", "spambase", "phishing", "connect4") {
    foreach ($s in 11, 22, 33) { $cells += , @($d, $s) }
}
$n = 0
foreach ($c in $cells) {
    $p = Start-Process -FilePath $Py -WorkingDirectory $Root -WindowStyle Hidden -PassThru -Wait `
        -ArgumentList "scripts\paper_b_run.py", "timing", "--dataset", $c[0], "--model", "xgb",
                      "--seed", $c[1], "--explainers", "anchors", "--root", "$Out\results",
                      "--no-require-idle" `
        -RedirectStandardOutput "$Out\$($c[0])_$($c[1]).log" -RedirectStandardError "$Out\$($c[0])_$($c[1]).err"
    $n++
    Add-Content -Path (Join-Path $Out "run.log") -Encoding ascii `
        -Value ("{0}  {1}/xgb/{2} exit {3} ({4}/25)" -f (Get-Date -Format "yyyy-MM-dd HH:mm"), $c[0], $c[1], $p.ExitCode, $n)
}
Note "xgb anchors rows rerun: finished ($n/25 cells); results in outputs/paper_b_rev1_xgb_anchors_rows/results"
