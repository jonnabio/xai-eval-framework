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

## Artifact Contract

Design:

- this document

Results guide:

- [docs/results/exp3_cross_dataset/README.md](../../results/exp3_cross_dataset/README.md)

Execution/config:

- [configs/experiments/exp3_cross_dataset](../../../configs/experiments/exp3_cross_dataset)

Raw outputs:

- `experiments/exp3_cross_dataset/results/`

Derived outputs:

- `outputs/`

Interpretation:

- future thesis and paper reporting under `docs/reports/...`

## Detailed Design

For the fuller rationale, success criteria, and run list, see the legacy detailed note:

- [EXP3_CROSS_DATASET_VALIDATION.md](../EXP3_CROSS_DATASET_VALIDATION.md)
