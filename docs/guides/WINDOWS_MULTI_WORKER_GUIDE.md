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

Set a stable worker identity once per workstation. Use a different value on
each physical machine:

```powershell
[Environment]::SetEnvironmentVariable("XAI_WORKER_ID", "workstation-a", "User")
$env:XAI_WORKER_ID = "workstation-a"
```

The worker writes and pushes to:

```text
results/<XAI_WORKER_ID>
```

For example, `workstation-a` pushes to `results/workstation-a`. This keeps
live checkpoint commits from colliding with the other workstations.

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

At startup, `managed_runner.ps1` switches the repository from `main` to the
worker result branch (`results/<worker_id>`). The sync daemon commits every
15 minutes and pushes that worker branch every 6 hours. It does **not** rebase
while experiments are running.

## Global Experiment Claims

Before a workstation starts an experiment, it now reserves that experiment on
`main` by creating:

```text
experiments/exp2_scaled/worker_claims/<experiment_name>.json
```

The claim is pushed to GitHub immediately. If another workstation already
claimed the experiment, the runner skips it and chooses another one. This is
the duplication guard: worker result branches store outputs, while `main`
stores the shared claim queue and consolidated completed results.

Do not edit or delete claim files while workers are running unless you are
manually recovering a dead worker. A claim without a final `results.json` means
that a workstation owns or previously owned that experiment.

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

## Consolidate All Worker Branches

Use `main` as the consolidated source of truth. Individual workstations can
show different percentages because each one is checked out on its own worker
branch and may not have every other workstation's latest pushed checkpoints.

Run the collector from one machine only:

```powershell
cd C:\Users\jonna\Github\xai-eval-framework
.\scripts\collect_worker_results.ps1 -Push
```

The collector automatically merges all remote branches matching:

```text
origin/results/*
```

If a workstation used a non-standard branch name, pass it explicitly:

```powershell
.\scripts\collect_worker_results.ps1 -ExtraBranches origin/linux_dell -Push
```

The collector does not switch the active checkout or rebase worker branches.
It fetches GitHub, creates merge commits from Git objects, pushes `main`, and
uses `logs\git_mutex` so it does not collide with local auto-push operations.
After it finishes, read the global completion percentage from `main`.

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

Each worker also writes manifest files under:

```text
experiments/exp2_scaled/worker_manifests/<worker_id>/
```

The most useful file is:

```text
experiments/exp2_scaled/worker_manifests/<worker_id>/current.json
```

It records the active experiment, status, result branch, output directory,
instance count, target count, latest checkpoint time, and whether
`results.json` exists.

## Important Operational Notes

1. Auto-commit is implemented on Windows worker branches.
   - `managed_runner.ps1` attempts a per-experiment results commit.
   - `auto_push.ps1` creates periodic local checkpoint commits.

2. Auto-push targets `results/<worker_id>`, not `main`.
   - This avoids rebase conflicts on `main` during active experiments.
   - Final aggregation into `main` should be done by a separate collector step.

3. Work assignment claims target `main`.
   - Claims are tiny JSON files under `worker_claims/`.
   - They are pushed before the expensive experiment starts.
   - If the claim push is rejected, the worker fetches again and picks another experiment.

4. Auto-push may still fail if the worker branch was changed elsewhere.
   - This does not mean the experiment stopped.
   - It means results were committed locally but not pushed yet.
   - Do not rebase during an active experiment; inspect and reconcile later.

5. Long-running experiments can stay quiet for a while.
   - Check the dashboard’s `Current Results` and `Live Worker` sections.
   - Check the latest write time in the active `instances/` folder.
   - Check the worker manifest `current.json`.

6. Do not run two workstations with the same `XAI_WORKER_ID`.
   - If two machines share the same worker branch, push conflicts can return.

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

## Updating Existing Workers Safely

Use this sequence on every workstation before adopting this branch-based
workflow. It preserves any local result files before pulling script updates:

```powershell
cd C:\Users\jonna\Github\xai-eval-framework

# 1. Stop local worker processes only.
Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -like '*managed_runner.ps1*' -or
    $_.CommandLine -like '*auto_push.ps1*' -or
    $_.CommandLine -like '*src.experiment.runner*'
} | ForEach-Object {
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}

# 2. Back up local uncommitted result files outside Git history.
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backup = "outputs\git_safety_backups\$stamp-before-worker-branch-update"
New-Item -ItemType Directory -Path $backup -Force | Out-Null
git status --porcelain -- experiments/exp2_scaled/results | Out-File "$backup\git-status-results.txt"
Compress-Archive -Path "experiments\exp2_scaled\results" -DestinationPath "$backup\results.zip" -Force

# 3. Commit local result changes to a safety branch if any exist.
$safetyBranch = "safety/$env:COMPUTERNAME-$stamp-before-worker-branch-update"
git switch -c $safetyBranch
git add -- experiments/exp2_scaled/results experiments/exp2_scaled/worker_manifests
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -m "Safety checkpoint before worker branch update"
    git push -u origin HEAD
}

# 4. Pull the updated workflow from main.
git fetch origin
git switch main
git pull --ff-only origin main

# 5. Set a unique worker id for this machine, then launch.
[Environment]::SetEnvironmentVariable("XAI_WORKER_ID", "workstation-a", "User")
$env:XAI_WORKER_ID = "workstation-a"
Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File .\scripts\managed_runner.ps1"
```

Change `workstation-a` to a unique value on each machine, such as
`workstation-b` and `workstation-c`.

## Suggested LLM Prompt For Another Windows Machine

Use this exact instruction:

```text
You are operating a Windows worker for the repository xai-eval-framework.
Follow the document docs/guides/WINDOWS_MULTI_WORKER_GUIDE.md exactly.
Work only from the repository root.
Before launching the worker, verify the model binaries load successfully.
Then start scripts/managed_runner.ps1 in the background and monitor it with scripts/status_dashboard.ps1.
If Git push fails due to remote divergence, do not stop the worker; report that results are committing locally but not pushing.
Use a unique XAI_WORKER_ID on this machine so it pushes to its own results/<worker_id> branch.
```

## Document To Reference

If you need one document to point another machine or LLM at, use:

- `docs/guides/WINDOWS_MULTI_WORKER_GUIDE.md`
