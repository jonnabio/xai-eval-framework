# EXP3 Execution Plan (Cross-Dataset Validation)

This plan is the **operational runbook** for EXP3: prerequisites, training,
resumability, and how we checkpoint results into Git so they reliably make it to
the thesis + papers via the publication sync pipeline.

## Goal

- Execute the 24-run EXP3 matrix on `breast_cancer` + `german_credit`.
- Preserve resumability at three layers: **training**, **per-config runner**, and
  **grid orchestration**.
- Ensure that partial progress is captured via **frequent commits + pushes**.

## Preconditions (must be true before starting)

### Python environment

- Use a **WSL/Linux** Python environment (do not reuse a Windows-built `.venv`).
- Install deps from `requirements.txt` (at minimum: `numpy`, `pandas`,
  `scikit-learn`, `xgboost`, `shap`, `pyyaml`, `alibi`).

Recommended setup:

```bash
bash scripts/setup_venv_wsl.sh
```

Reference: `docs/guides/WSL_PYTHON_ENV.md`.

### Git push is working (non-interactive)

Before launching EXP3, confirm this succeeds:

```bash
git push --dry-run
```

If it fails under WSL, configure Windows Git Credential Manager:

```bash
git config --global credential.helper /mnt/c/PROGRA~1/Git/mingw64/bin/git-credential-manager.exe
git push --dry-run
```

### OpenML access (German Credit only)

German Credit uses OpenML (`credit-g`). The first run requires internet access
and caches under `data/openml/`.

## Step 1 — Train EXP3 model artifacts (idempotent)

Training generates:

```text
experiments/exp3_cross_dataset/models/<dataset>/<model>/seed_<seed>/
```

Run:

```bash
.venv-wsl/bin/python3 scripts/train_exp3_models.py
```

Resume behavior:

- `scripts/train_exp3_models.py` skips existing `(model.joblib, preprocessor.joblib)` unless `--force` is passed.

## Step 2 — Smoke test (fast failure signal)

Run one Breast Cancer SHAP config first:

```bash
.venv-wsl/bin/python3 -m src.experiment.runner --config configs/experiments/exp3_cross_dataset/breast_cancer/rf_shap_s42_n100.yaml
```

## Step 3 — Run the full grid (resumable)

Run the managed runner (recommended):

```bash
VENV_PYTHON=.venv-wsl/bin/python3 bash scripts/managed_runner_exp3.sh
```

Grid resumability:

- `scripts/managed_runner_exp3.sh` skips configs whose `output_dir/results.json` already exists.

Per-config resumability (critical):

- The runner checkpoints each instance under `.../instances/<id>.json` and reloads them on restart.
- Re-running the same config resumes until `results.json` is written.

Implementation reference:

- `src/experiment/runner.py:389` (checkpoint load)

## Step 4 — Frequent commits and pushes (checkpointing)

Why:

- EXP3 runs can take hours; we commit partial `instances/*.json` checkpoints so an interruption does not lose work.

Mechanism:

- `scripts/managed_runner_exp3.sh` starts `scripts/auto_push.sh` in the background to commit checkpoints and push periodically.
- A shared lock file (`.git/xai_git_sync.lock`) prevents Git index races between the background daemon and the runner commit/push.

Tune cadence:

```bash
INTERVAL=900 PUSH_INTERVAL=3600 VENV_PYTHON=.venv-wsl/bin/python3 bash scripts/managed_runner_exp3.sh
```

## Step 5 — Propagate results into papers + thesis

After EXP3 produces stable `results.json` files:

1. Update any new claims/figures/tables in `pub/claims.toml` (SSOT).
2. Regenerate fragments + verify wiring:

```bash
bash scripts/pubs/build_all.sh
```

This ensures Paper A/B/C and the thesis ingest the same source-of-truth fragments
before rendering.

## Verification checklist

- [ ] `scripts/train_exp3_models.py` completed for both datasets.
- [ ] Smoke test `breast_cancer/rf_shap_s42_n100` produces `results.json`.
- [ ] `experiments/exp3_cross_dataset/results/**/results.json` exists for all 24 runs (or an explicitly recorded partial subset).
- [ ] GitHub has recent pushes containing `instances/*.json` checkpoints and final `results.json`.
- [ ] `scripts/pubs/build_all.sh` passes `scripts/pubs/verify_sync.py`.
