# EXP3: Cross-Dataset Validation

## Purpose

EXP3 is the smallest additional package intended to improve thesis external validity beyond the Adult-only evidence stream from EXP1 and EXP2.

It is a compact cross-dataset replication layer, not a second full benchmark campaign.

## Thesis Role

EXP3 supports bounded claims about external validity:

- the framework ports beyond Adult
- selected explainer trade-offs are not purely Adult-specific
- key quantitative patterns can be rechecked on additional tabular datasets

## Preparation Status

Status:

- design manifest exists;
- dataset-loader support is prepared for `breast_cancer` and `german_credit`;
- config generation is handled by `scripts/generate_exp3_configs.py`;
- model artifact preparation is handled by `scripts/train_exp3_models.py`;
- preparation walkthrough and file-level change inventory are documented in
  [EXP3_PREPARATION_WALKTHROUGH.md](./EXP3_PREPARATION_WALKTHROUGH.md);
- full execution should wait until the active EXP2 worker has finished.

EXP3 compute should start with a single Breast Cancer SHAP smoke run before any
Anchors jobs are launched.

## Planned Matrix

Declared in [configs/experiments/exp3_cross_dataset/manifest.yaml](../../../configs/experiments/exp3_cross_dataset/manifest.yaml):

- datasets: `breast_cancer`, `german_credit`
- models: `rf`, `xgb`
- explainers: `shap`, `anchors`
- seeds: `42`, `123`, `456`
- sample size: `100`

Planned total:

- `24` configurations

## Execution Priority

## Python Environment (WSL/Linux)

EXP3 is designed to run under WSL/Linux as well as native Linux.

- Do **not** reuse a Python venv created on Windows from WSL.
- Use a WSL venv (recommended: `.venv-wsl`) and point runners with `VENV_PYTHON`.
- EXP3 includes Anchors configs, which require `alibi` to be installed.

Quick setup:

```bash
bash scripts/setup_venv_wsl.sh
```

Reference: `docs/guides/WSL_PYTHON_ENV.md`.

Recommended order:

1. Generate EXP3 configs with `python scripts/generate_exp3_configs.py`.
2. Train Breast Cancer model artifacts with:
   `python scripts/train_exp3_models.py --datasets breast_cancer --models rf xgb --seeds 42 123 456`.
3. Run one smoke-test configuration:
   `python -m src.experiment.runner --config configs/experiments/exp3_cross_dataset/breast_cancer/rf_shap_s42_n100.yaml`.
4. Complete Breast Cancer + SHAP.
5. Complete Breast Cancer + Anchors.
6. Train and execute German Credit + SHAP.
7. Complete German Credit + Anchors.

Within each block:

- `rf` before `xgb`
- seeds `42`, `123`, `456`

## Resumability and Git Checkpointing

- **Training resumability:** `scripts/train_exp3_models.py` skips existing artifacts unless `--force` is passed.
- **Run resumability:** the runner checkpoints each evaluated instance under `.../instances/<id>.json`; re-running the same config resumes from checkpoints until `results.json` is written.
- **Batch resumability:** `scripts/managed_runner_exp3.sh` skips configs that already have `results.json`.
- **Frequent commits/pushes:** `scripts/managed_runner_exp3.sh` starts `scripts/auto_push.sh` in the background to commit/push checkpoints while a config is still running; configure cadence with `INTERVAL` and `PUSH_INTERVAL`. A shared Git lock (`.git/xai_git_sync.lock`) prevents index races.

Full runbook: `docs/planning/exp3_execution_plan.md`.

## Artifact Contract

Design:

- this document
- [EXP3 preparation walkthrough](./EXP3_PREPARATION_WALKTHROUGH.md)

Results guide:

- [docs/results/exp3_cross_dataset/README.md](../../results/exp3_cross_dataset/README.md)

Execution/config:

- [configs/experiments/exp3_cross_dataset](../../../configs/experiments/exp3_cross_dataset)
- `scripts/generate_exp3_configs.py`
- `scripts/train_exp3_models.py`

Code support:

- `src/data_loading/cross_dataset.py`
- `src/experiment/runner.py`

Raw outputs:

- `experiments/exp3_cross_dataset/results/`

Derived outputs:

- `outputs/`

Interpretation:

- future thesis and paper reporting under `docs/reports/...`

## Detailed Design

For the fuller rationale, success criteria, and run list, see the legacy detailed note:

- [EXP3_CROSS_DATASET_VALIDATION.md](../EXP3_CROSS_DATASET_VALIDATION.md)
