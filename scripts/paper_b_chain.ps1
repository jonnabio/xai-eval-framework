# Paper B revision 1: run the auxiliary studies one after another, unattended (RUNBOOK §10).
#
#   powershell -ExecutionPolicy Bypass -File scripts\paper_b_chain.ps1
#   powershell -ExecutionPolicy Bypass -File scripts\paper_b_chain.ps1 -From sweep
#
# Each step sets PAPER_B_CONFIG to the study's config, starts a save loop for that study
# (results under experiments/exp_b_rev1/studies_results/<study>/ on paper/b-rev1-runs), runs
# the step to completion, then stops the save loop with its _STOP_SYNC file (one last
# snapshot). A step that is already complete returns at once (the runner resumes), so the
# chain can be restarted at any point. Progress: outputs\paper_b_rev1_chain.log.
param([string]$From = "controls_nonoise")

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Py = Join-Path $Root ".venv\Scripts\python.exe"
$Log = Join-Path $Root "outputs\paper_b_rev1_chain.log"

$Steps = @(
    @{ Study = "controls_nonoise"; Mode = "launch" },
    @{ Study = "controls_onehot";  Mode = "launch" },
    @{ Study = "sweep";            Mode = "launch" },
    @{ Study = "sweep";            Mode = "launch-timing" },
    @{ Study = "matched";          Mode = "launch-timing" }
)

function Write-Log([string]$msg) {
    $line = "{0}  {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $msg
    Add-Content -Path $Log -Value $line -Encoding ascii
}

$started = $false
foreach ($s in $Steps) {
    if (-not $started -and $s.Study -ne $From) { continue }
    $started = $true
    $env:PAPER_B_CONFIG = "experiments\exp_b_rev1\studies\$($s.Study).toml"
    $live = Join-Path $Root "outputs\paper_b_rev1_$($s.Study)_live"
    New-Item -ItemType Directory -Force -Path $live | Out-Null
    Remove-Item (Join-Path $live "_STOP_SYNC") -ErrorAction SilentlyContinue
    $sync = Start-Process -FilePath $Py -ArgumentList "scripts\paper_b_sync.py", "--loop" `
        -WorkingDirectory $Root -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput (Join-Path $live "sync_loop.out") `
        -RedirectStandardError (Join-Path $live "sync_loop.err")
    Write-Log "start $($s.Study) $($s.Mode) (save loop pid $($sync.Id))"
    $p = Start-Process -FilePath $Py -ArgumentList "scripts\paper_b_run.py", $s.Mode `
        -WorkingDirectory $Root -WindowStyle Hidden -PassThru -Wait
    Write-Log "end   $($s.Study) $($s.Mode) (exit $($p.ExitCode))"
    New-Item -ItemType File -Force -Path (Join-Path $live "_STOP_SYNC") | Out-Null
    $sync.WaitForExit(300000) | Out-Null       # one last snapshot, then the loop leaves
    if ($p.ExitCode -ne 0) {
        Write-Log "chain stopped: $($s.Study) $($s.Mode) exited $($p.ExitCode)"
        exit $p.ExitCode
    }
}
Remove-Item Env:PAPER_B_CONFIG -ErrorAction SilentlyContinue
Write-Log "chain finished"
