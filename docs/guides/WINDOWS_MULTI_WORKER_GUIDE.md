# Windows Multi-Worker Guide

## Purpose

This document is the source of truth for running an additional **Windows worker machine** for the `xai-eval-framework` experiment queue.

Use this guide when:
- adding a second Windows workstation
- rebuilding a broken Windows worker
- instructing another Windows machine through an LLM prompt

## Scripts Used

The Windows worker flow is implemented in:
- `scripts/managed_runner.ps1`
- `scripts/auto_push.ps1`
- `scripts/status_dashboard.ps1`

## Preconditions

Before launching a second Windows worker, make sure the machine has:

1. Git access with push permission to the repository.
2. Python/Conda environment installed and working.
3. Required dependencies installed from `requirements.txt`.
4. Valid model artifacts in `experiments/exp1_adult/models/`.
5. Enough free RAM for long-running XAI jobs.

## Setup

From the repository root:

```powershell
git fetch origin
git switch main
git pull --rebase origin main
pip install -r requirements.txt
```

## Validate Model Artifacts

The worker depends on healthy model binaries. At minimum, verify the models load locally:

```powershell
@'
import joblib
paths = [
    r"experiments/exp1_adult/models/rf.joblib",
    r"experiments/exp1_adult/models/xgb.joblib",
    r"experiments/exp1_adult/models/svm.joblib",
    r"experiments/exp1_adult/models/mlp.joblib",
    r"experiments/exp1_adult/models/logreg.joblib",
]
for p in paths:
    obj = joblib.load(p)
    print("OK", p, type(obj))
'@ | python -
```

If any of these fail, do not launch the worker until the models are restored or retrained.

## Launch Worker

Start the Windows worker in the background:

```powershell
Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File .\scripts\managed_runner.ps1"
```

This starts:
- the managed experiment runner
- the periodic result-sync daemon

## Monitor Worker

### 1. Dashboard

Use the Windows terminal dashboard:

```powershell
.\scripts\status_dashboard.ps1
```

The dashboard shows:
- overall progress
- active experiment result directories
- latest write age
- recent completed runs
- live worker PID and config path

### 2. Raw Runner Log

```powershell
Get-Content -Path "logs\managed_runner.log" -Wait
```

### 3. Raw Sync Log

```powershell
Get-Content -Path "logs\auto_push.log" -Wait
```

## Reliable Live Progress

The most reliable signal is **instance file growth** inside the active result directory, not just console output.

Example:

```powershell
Get-ChildItem .\experiments\exp2_scaled\results\rf_dice\seed_456\n_50\instances -Filter *.json | Measure-Object
```

The runner also logs progress snapshots based on instance-file growth.

## Important Operational Notes

1. Auto-commit is implemented on Windows.
   - `managed_runner.ps1` attempts a per-experiment results commit.
   - `auto_push.ps1` creates periodic local checkpoint commits.

2. Auto-push may still fail if the local branch is behind `origin/main`.
   - This does not mean the experiment stopped.
   - It means results were committed locally but not pushed yet.

3. Long-running experiments can stay quiet for a while.
   - Check the dashboard’s `Current Results` and `Live Worker` sections.
   - Check the latest write time in the active `instances/` folder.

## If the Worker Stops

Check for live processes:

```powershell
Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -like '*managed_runner.ps1*' -or
    $_.CommandLine -like '*auto_push.ps1*' -or
    $_.CommandLine -like '*src.experiment.runner*'
} | Select-Object ProcessId, ParentProcessId, Name, CommandLine
```

If the worker is stale, restart it:

```powershell
Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File .\scripts\managed_runner.ps1"
```

## Suggested LLM Prompt For Another Windows Machine

Use this exact instruction:

```text
You are operating a Windows worker for the repository xai-eval-framework.
Follow the document docs/guides/WINDOWS_MULTI_WORKER_GUIDE.md exactly.
Work only from the repository root.
Before launching the worker, verify the model binaries load successfully.
Then start scripts/managed_runner.ps1 in the background and monitor it with scripts/status_dashboard.ps1.
If Git push fails due to remote divergence, do not stop the worker; report that results are committing locally but not pushing.
```

## Document To Reference

If you need one document to point another machine or LLM at, use:

- `docs/guides/WINDOWS_MULTI_WORKER_GUIDE.md`
