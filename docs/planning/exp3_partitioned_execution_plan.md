# EXP3 Partitioned Execution Plan

This plan extends the primary [EXP3 execution plan](./exp3_execution_plan.md)
for a two-worker run across Windows and Linux/WSL. It is the operational source
of truth when EXP3 is executed in parallel.

## Goal

- Reduce wall-clock runtime for the 24-run EXP3 matrix.
- Keep each worker on a disjoint result partition so no two processes write the
  same `output_dir`.
- Preserve reproducibility, checkpoint resumability, and Git traceability.
- Avoid cross-platform reuse of incompatible virtual environments.

## Matrix Partition

EXP3 has 24 configurations:

- datasets: `breast_cancer`, `german_credit`
- models: `rf`, `xgb`
- explainers: `shap`, `anchors`
- seeds: `42`, `123`, `456`
- sample size: `100`

The default partition is dataset-level:

| Worker | Platform | Config subset | Run count | Result root |
|---|---|---:|---:|---|
| `exp3-windows-breast-cancer` | Windows | `configs/experiments/exp3_cross_dataset/breast_cancer/*.yaml` | 12 | `experiments/exp3_cross_dataset/results/breast_cancer/` |
| `exp3-linux-german-credit` | Linux/WSL | `configs/experiments/exp3_cross_dataset/german_credit/*.yaml` | 12 | `experiments/exp3_cross_dataset/results/german_credit/` |

This split is preferred because it avoids shared model artifact directories,
shared result directories, and simultaneous OpenML access from both workers.

## Current Readiness Checkpoint (2026-04-26)

EXP3 has passed the project-level readiness gate in the Linux/container
checkout:

- Config matrix present: `24` configs excluding `manifest.yaml`.
- Model artifacts prepared:
  - `12` model binaries: `rf.joblib` / `xgb.joblib`;
  - `12` fitted preprocessors: `preprocessor.joblib`;
  - `12` training summaries: `exp3_training_summary.json`.
- Smoke gate passed:
  `experiments/exp3_cross_dataset/results/breast_cancer/rf_shap/seed_42/n_100/results.json`.
- Completed raw results: `1 / 24`.
- German Credit data cache present:
  `data/openml/dataset_31_credit-g.arff`.
- Verification passed:
  `pytest -q tests/test_cross_dataset_loader.py`.

Readiness by worker:

| Worker | Ready to launch? | Remaining gate |
|---|---|---|
| `exp3-linux-german-credit` | Yes, from this Linux/WSL checkout | Confirm non-interactive `git push --dry-run` on the branch that will receive results. |
| `exp3-windows-breast-cancer` | Conditionally | Pull/sync these changes on Windows, use Python 3.11 `.venv-exp3`, run the Windows dependency preflight, and confirm Git push works. |

Do not use a Windows Python 3.13 environment for EXP3.

## Preconditions

### Shared

- The repository is on a branch that can receive EXP3 result commits.
- The 24 generated configs exist under
  `configs/experiments/exp3_cross_dataset/`.
- No active worker is already writing to the same partition under
  `experiments/exp3_cross_dataset/results/`.
- Git push works non-interactively on any worker that will push checkpoints.
- The first EXP3 smoke run has passed or is being executed deliberately as the
  gate before the remaining partition work.

### Windows Worker

- Use a Windows Python 3.11 virtual environment.
- Do not run the Linux shell runner from Windows unless using WSL.
- Required packages are importable from the selected Windows Python:
  `numpy`, `pandas`, `sklearn`, `xgboost`, `shap`, `yaml`, `alibi`, `joblib`.
- Avoid Python 3.13 for EXP3. `alibi` pulls compiled dependencies that can fall
  back to source builds on Python 3.13, which is fragile on Windows.

### Linux/WSL Worker

- Use a Linux/WSL virtual environment, preferably `.venv-wsl/bin/python3`.
- Do not reuse a Windows-created `.venv` from Linux/WSL.
- Required packages are importable from the selected Linux Python:
  `numpy`, `pandas`, `sklearn`, `xgboost`, `shap`, `yaml`, `alibi`, `joblib`.
- German Credit requires network access for the first OpenML ARFF download and
  then caches `data/openml/dataset_31_credit-g.arff` locally.

## Safety Rules

- Never run both workers against the full EXP3 config tree.
- Never run the same config on both workers at the same time.
- Never force retrain a model artifact while another process may use it.
- Prefer one auto-push/checkpoint process at a time per working tree.
- If both workers share the same physical checkout, disable automatic Git
  checkpointing on one side and push manually after that worker stops.
- If both workers use separate clones, push to separate result branches and
  merge after both partitions finish.

Recommended branch names:

- Windows: `results/exp3-windows-breast-cancer`
- Linux/WSL: `results/exp3-linux-german-credit`

## Phase 0 - Preflight

Current Linux/container verification already passed:

```text
pytest -q tests/test_cross_dataset_loader.py
3 passed
```

Each physical worker still needs its own environment and Git checks because the
Windows and Linux partitions use separate Python environments.

Recommended Windows automation:

```powershell
.\scripts\setup_exp3_windows.ps1
```

This creates `.venv-exp3`, installs dependencies, runs the Windows dependency
preflight, trains the Breast Cancer RF seed-42 model artifact, runs the RF/SHAP
seed-42 smoke config, and verifies the smoke `results.json`.

Run the dependency check on each platform.

Windows PowerShell:

```powershell
py -3.11 --version

@"
import importlib
for mod in ["yaml", "numpy", "pandas", "sklearn", "xgboost", "shap", "alibi", "joblib"]:
    importlib.import_module(mod)
print("EXP3 Windows dependencies OK")
"@ | .\.venv-exp3\Scripts\python.exe -
```

Linux/WSL:

```bash
.venv-wsl/bin/python3 - <<'PY'
import importlib
for mod in ["yaml", "numpy", "pandas", "sklearn", "xgboost", "shap", "alibi", "joblib"]:
    importlib.import_module(mod)
print("EXP3 Linux dependencies OK")
PY
```

Validate config count:

Windows PowerShell:

```powershell
(Get-ChildItem configs\experiments\exp3_cross_dataset -Recurse -Filter *.yaml |
  Where-Object { $_.Name -ne "manifest.yaml" }).Count
```

Linux/WSL:

```bash
find configs/experiments/exp3_cross_dataset -name "*.yaml" ! -name manifest.yaml | wc -l
```

Expected value: `24`.

Confirm model artifacts:

Windows PowerShell:

```powershell
(Get-ChildItem experiments\exp3_cross_dataset\models -Recurse -Include rf.joblib,xgb.joblib).Count
(Get-ChildItem experiments\exp3_cross_dataset\models -Recurse -Filter preprocessor.joblib).Count
```

Linux/WSL:

```bash
find experiments/exp3_cross_dataset/models \( -name rf.joblib -o -name xgb.joblib \) | wc -l
find experiments/exp3_cross_dataset/models -name preprocessor.joblib | wc -l
```

Expected values: `12` and `12`.

## Phase 1 - Windows Smoke Run

Start with the smallest Breast Cancer RF/SHAP path. This is the gate before
parallel execution.

As of 2026-04-26, this gate has passed in the Linux/container checkout. On
Windows, re-running the smoke through `scripts/setup_exp3_windows.ps1` is still
acceptable and resumable; if the synced `results.json` already exists, the
partition runner should skip that completed config.

Windows PowerShell:

```powershell
.\.venv-exp3\Scripts\python.exe scripts\train_exp3_models.py --datasets breast_cancer --models rf --seeds 42
.\.venv-exp3\Scripts\python.exe -m src.experiment.runner --config configs\experiments\exp3_cross_dataset\breast_cancer\rf_shap_s42_n100.yaml
```

Success condition:

```text
experiments/exp3_cross_dataset/results/breast_cancer/rf_shap/seed_42/n_100/results.json
```

If the smoke run fails, stop and fix the failure before launching either
partition.

## Phase 2 - Prepare Model Artifacts

Train only the artifacts needed by each worker.

Windows PowerShell:

```powershell
.\.venv-exp3\Scripts\python.exe scripts\train_exp3_models.py --datasets breast_cancer --models rf xgb --seeds 42 123 456
```

Linux/WSL:

```bash
.venv-wsl/bin/python3 scripts/train_exp3_models.py --datasets german_credit --models rf xgb --seeds 42 123 456
```

Training is idempotent. Existing `(model.joblib, preprocessor.joblib)` pairs are
skipped unless `--force` is passed.

As of 2026-04-26, all 12 model/preprocessor pairs have been prepared in this
checkout. Re-running the training commands on each worker is safe and should
skip existing artifacts unless the worker checkout lacks them.

## Phase 3 - Execute Partitions

The current EXP3 managed runner scans every config under `CONFIG_DIR`. To keep
workers partitioned, either run targeted loops or create temporary subset
directories. Targeted loops are preferred because they do not require generated
files.

### Windows Partition

After the smoke gate passes, the Windows Breast Cancer partition can be launched
with:

```powershell
.\scripts\setup_exp3_windows.ps1 -SkipInstall -RunBreastCancerPartition
```

Run Breast Cancer configs in the documented priority order: SHAP first, then
Anchors; within each block, `rf` before `xgb`; seeds `42`, `123`, `456`.

Windows PowerShell:

```powershell
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
  .\.venv-exp3\Scripts\python.exe -m src.experiment.runner --config $Config
  if ($LASTEXITCODE -ne 0) {
    throw "EXP3 Windows partition failed at $Config"
  }
}
```

### Linux/WSL Partition

Run German Credit configs in the same priority order.

This partition is ready to launch from this Linux/WSL checkout after confirming
the target branch can be pushed:

```bash
git push --dry-run
```

Linux/WSL:

```bash
set -euo pipefail

configs=(
  configs/experiments/exp3_cross_dataset/german_credit/rf_shap_s42_n100.yaml
  configs/experiments/exp3_cross_dataset/german_credit/rf_shap_s123_n100.yaml
  configs/experiments/exp3_cross_dataset/german_credit/rf_shap_s456_n100.yaml
  configs/experiments/exp3_cross_dataset/german_credit/xgb_shap_s42_n100.yaml
  configs/experiments/exp3_cross_dataset/german_credit/xgb_shap_s123_n100.yaml
  configs/experiments/exp3_cross_dataset/german_credit/xgb_shap_s456_n100.yaml
  configs/experiments/exp3_cross_dataset/german_credit/rf_anchors_s42_n100.yaml
  configs/experiments/exp3_cross_dataset/german_credit/rf_anchors_s123_n100.yaml
  configs/experiments/exp3_cross_dataset/german_credit/rf_anchors_s456_n100.yaml
  configs/experiments/exp3_cross_dataset/german_credit/xgb_anchors_s42_n100.yaml
  configs/experiments/exp3_cross_dataset/german_credit/xgb_anchors_s123_n100.yaml
  configs/experiments/exp3_cross_dataset/german_credit/xgb_anchors_s456_n100.yaml
)

for config in "${configs[@]}"; do
  .venv-wsl/bin/python3 -m src.experiment.runner --config "$config"
done
```

## Phase 4 - Checkpointing and Git

For a shared working tree, use manual commits after each partition block to
avoid Git index races:

```bash
git add experiments/exp3_cross_dataset/results/breast_cancer
git commit -m "EXP3: breast cancer partition results"
git push
```

```bash
git add experiments/exp3_cross_dataset/results/german_credit
git commit -m "EXP3: german credit partition results"
git push
```

For separate clones, each worker may push to its own result branch. After both
partitions finish, merge the result branches into the main EXP3 branch.

## Phase 4.5 - Email Reports

EXP3 email reports are generated by `scripts/email_report.py`. The script is
cross-platform, defaults to EXP3, and summarizes local results plus pushed
`origin/main` and `origin/results/*` worker branches.

Manual test without sending email:

Linux/WSL:

```bash
python scripts/email_report.py --print-only --no-fetch
```

Windows PowerShell:

```powershell
.\.venv-exp3\Scripts\python.exe .\scripts\email_report.py --print-only --no-fetch
```

Install the Linux/WSL cron job, every 3 hours:

```bash
bash scripts/install_cronjob.sh "<gmail-app-password>" "jonnabio@gmail.com"
```

Install the Windows scheduled task, every 3 hours:

```powershell
.\scripts\install_email_report_task.ps1 -GmailAppPassword "<gmail-app-password>" -ToEmail "jonnabio@gmail.com"
```

If `GMAIL_APP_PASSWORD` is missing or SMTP fails, the report is written to the
platform temp directory as `latest_xai_report.txt` instead of being lost.

## Phase 5 - Verification

Count completed EXP3 result files:

```bash
find experiments/exp3_cross_dataset/results -name results.json | wc -l
```

Expected final value: `24`.

Check each partition:

```bash
find experiments/exp3_cross_dataset/results/breast_cancer -name results.json | wc -l
find experiments/exp3_cross_dataset/results/german_credit -name results.json | wc -l
```

Expected values: `12` and `12`.

Run the project result validation scripts that apply to EXP3 after all raw
results exist. Then propagate stable result claims through the publication
pipeline:

```bash
bash scripts/pubs/build_all.sh
```

## Recovery

- If a config is interrupted, re-run the same config on the same worker. The
  runner resumes from `instances/*.json` checkpoints until `results.json` is
  written.
- If a worker accidentally starts the wrong dataset, stop it before it writes
  additional checkpoints. Keep completed `results.json` only if the config was
  uniquely assigned and reproducible.
- If both workers wrote the same `output_dir`, preserve both copies outside the
  result tree, compare them manually, and keep one canonical output.
- If Git push fails, keep running the partition only if local disk is stable;
  commit and push once credentials or branch divergence are fixed.

## Completion Criteria

- [ ] Windows dependency preflight passed.
- [x] Linux/WSL dependency preflight passed.
- [x] Breast Cancer RF/SHAP seed `42` smoke run produced `results.json`.
- [ ] Breast Cancer partition produced 12 `results.json` files.
- [ ] German Credit partition produced 12 `results.json` files.
- [ ] EXP3 total is 24 `results.json` files.
- [ ] EXP3 result commits are pushed or explicitly recorded as local-only.
- [ ] Publication sync passes after EXP3 claims are updated.
