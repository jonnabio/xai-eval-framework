# EXP3 Preparation Walkthrough

## 1. Metadata

- **Date**: 2026-04-13
- **Experiment family**: `exp3_cross_dataset`
- **Status**: Prepared, not executed
- **Reason for deferral**: Active EXP2 worker is still running
- **Implementation commit**: `bf1096e4 feat(exp3): prepare cross-dataset validation scaffold`

## 2. Goal

Prepare EXP3 so it can begin safely after the active EXP2 worker finishes.

The preparation scope was limited to:

- dataset-loader support;
- seed-specific model artifact training entry point;
- 24-run configuration grid generation;
- documentation updates;
- lightweight validation.

No EXP3 explanation experiments were launched.

## 3. Changes Completed

### 3.1 Dataset loading

Added `src/data_loading/cross_dataset.py` with loaders for:

- `breast_cancer`, using the built-in sklearn Breast Cancer Wisconsin dataset;
- `german_credit`, using OpenML `credit-g` version 1.

The loader contract matches the existing Adult loader shape:

```text
X_train, X_test, y_train, y_test, feature_names, preprocessor
```

`src/data_loading/__init__.py` now exports the EXP3 loaders and dispatcher.

### 3.2 Runner dispatch

Updated `src/experiment/runner.py` so the experiment runner can load:

- `adult`;
- `breast_cancer`;
- `german_credit`.

For EXP3 datasets, the runner looks for seed-specific preprocessors next to
the model artifact under `experiments/exp3_cross_dataset/models/...`.

### 3.3 Config generation

Added `scripts/generate_exp3_configs.py` and generated the 24 planned EXP3
configs under:

```text
configs/experiments/exp3_cross_dataset/<dataset>/
```

The generated matrix is:

- datasets: `breast_cancer`, `german_credit`;
- models: `rf`, `xgb`;
- explainers: `shap`, `anchors`;
- seeds: `42`, `123`, `456`;
- sample size: `n=100`.

All generated configs use `max_workers: 1` to avoid local oversubscription when
EXP3 is eventually run beside other workers.

### 3.4 Model artifact preparation

Added `scripts/train_exp3_models.py`.

The script trains seed-specific model/preprocessor artifacts under:

```text
experiments/exp3_cross_dataset/models/<dataset>/<model>/seed_<seed>/
```

This script was not executed during preparation because the active EXP2 worker
was still running.

### 3.5 Documentation

Updated:

- `docs/experiments/exp3_cross_dataset/README.md`;
- `docs/results/exp3_cross_dataset/README.md`.

The docs now distinguish between EXP3 preparation and EXP3 execution, and
recommend starting with a Breast Cancer SHAP smoke test after the active EXP2
worker finishes.

## 4. File-Level Change Inventory

### 4.1 Code

| Path | Change |
|------|--------|
| `src/data_loading/cross_dataset.py` | Added EXP3 dataset loaders for `breast_cancer` and `german_credit`, plus the `load_tabular_dataset` dispatcher. |
| `src/data_loading/__init__.py` | Exported the EXP3 dataset loaders and dispatcher. |
| `src/experiment/runner.py` | Added runner support for `breast_cancer` and `german_credit`, including optional seed-specific preprocessor loading beside the model artifact. |

### 4.2 Scripts

| Path | Change |
|------|--------|
| `scripts/generate_exp3_configs.py` | Added the config generator for the fixed 24-run EXP3 grid. |
| `scripts/train_exp3_models.py` | Added the model artifact preparation entry point for seed-specific RF/XGB model and preprocessor artifacts. |

### 4.3 Configs

| Path | Change |
|------|--------|
| `configs/experiments/exp3_cross_dataset/manifest.yaml` | Updated EXP3 status from `proposed` to `prepared`, added `model_root`, and normalized artifact roots. |
| `configs/experiments/exp3_cross_dataset/breast_cancer/*.yaml` | Added 12 Breast Cancer configs across RF/XGB, SHAP/Anchors, and seeds `42`, `123`, `456`. |
| `configs/experiments/exp3_cross_dataset/german_credit/*.yaml` | Added 12 German Credit configs across RF/XGB, SHAP/Anchors, and seeds `42`, `123`, `456`. |

### 4.4 Documentation

| Path | Change |
|------|--------|
| `docs/experiments/exp3_cross_dataset/README.md` | Documented preparation status, execution priority, and the first smoke-test sequence. |
| `docs/results/exp3_cross_dataset/README.md` | Documented result-side status and deferred execution semantics. |
| `docs/experiments/exp3_cross_dataset/EXP3_PREPARATION_WALKTHROUGH.md` | Added the session-level walkthrough, validation record, and change inventory. |

### 4.5 Tests

| Path | Change |
|------|--------|
| `tests/test_cross_dataset_loader.py` | Added loader smoke tests for Breast Cancer and dispatcher validation. |

## 5. Verification

Commands run:

```powershell
python scripts\generate_exp3_configs.py
python -m pytest tests\test_cross_dataset_loader.py
python -c "from pathlib import Path; from src.experiment.config import load_config; paths=sorted(Path('configs/experiments/exp3_cross_dataset').glob('*/*.yaml')); [load_config(p) for p in paths]; print(f'validated {len(paths)} EXP3 configs')"
python -c "from src.data_loading.cross_dataset import load_breast_cancer; X_train,X_test,y_train,y_test,features,_=load_breast_cancer(verbose=False); print(X_train.shape, X_test.shape, len(features), y_train.mean().round(4), y_test.mean().round(4))"
```

Observed results:

- `tests/test_cross_dataset_loader.py`: 3 passed;
- EXP3 config schema validation: 24 configs validated;
- Breast Cancer loader smoke check:
  `(455, 30) (114, 30) 30 0.6264 0.6316`.

## 6. Deferred Execution

Do not run the full EXP3 grid until the active EXP2 worker finishes.

Recommended first execution sequence:

1. Train Breast Cancer RF model for seed 42:
   `python scripts/train_exp3_models.py --datasets breast_cancer --models rf --seeds 42`.
2. Run the first SHAP smoke test:
   `python -m src.experiment.runner --config configs/experiments/exp3_cross_dataset/breast_cancer/rf_shap_s42_n100.yaml`.
3. If successful, train the remaining Breast Cancer RF/XGB artifacts.
4. Run Breast Cancer SHAP configs before starting Anchors.
5. Defer German Credit until Breast Cancer is verified.

## 7. Readiness Checkpoint: 2026-04-26

EXP3 moved from scaffold-ready to execution-ready for the remaining partitioned
matrix.

Commands completed:

```bash
python scripts/train_exp3_models.py --datasets breast_cancer --models rf --seeds 42
python -m src.experiment.runner --config configs/experiments/exp3_cross_dataset/breast_cancer/rf_shap_s42_n100.yaml
python scripts/train_exp3_models.py --datasets breast_cancer german_credit --models rf xgb --seeds 42 123 456
pytest -q tests/test_cross_dataset_loader.py
```

Observed results:

- Breast Cancer RF/SHAP seed-42 smoke run completed and wrote:
  `experiments/exp3_cross_dataset/results/breast_cancer/rf_shap/seed_42/n_100/results.json`.
- EXP3 model artifacts prepared:
  - `12` model binaries: `rf.joblib` / `xgb.joblib`;
  - `12` fitted preprocessors: `preprocessor.joblib`;
  - `12` training summaries: `exp3_training_summary.json`.
- Current raw EXP3 results: `1 / 24`.
- Loader tests: `3 passed`.
- German Credit loader smoke: `(800, 61)` train and `(200, 61)` test.
- German Credit cache:
  `data/openml/dataset_31_credit-g.arff`.

Implementation note:

- sklearn's OpenML metadata API path failed in this environment with HTTP 301
  redirect loops.
- `src/data_loading/cross_dataset.py` now loads OpenML German Credit dataset id
  `31` through the canonical direct ARFF download and local cache.

Execution handoff:

- Linux/WSL German Credit partition is ready after `git push --dry-run` passes.
- Windows Breast Cancer partition is ready after pulling/syncing these changes,
  using Python 3.11 `.venv-exp3`, passing the Windows dependency preflight, and
  confirming Git push works.
- Continue to use the partitioned runbook:
  `docs/planning/exp3_partitioned_execution_plan.md`.
