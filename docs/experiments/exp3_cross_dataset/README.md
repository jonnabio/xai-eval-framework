# EXP3: Cross-Dataset Validation

## Purpose

EXP3 is the smallest additional package intended to improve thesis external validity beyond the Adult-only evidence stream from EXP1 and EXP2.

It is a compact cross-dataset replication layer, not a second full benchmark campaign.

## Thesis Role

EXP3 supports bounded claims about external validity:

- the framework ports beyond Adult
- selected explainer trade-offs are not purely Adult-specific
- key quantitative patterns can be rechecked on additional tabular datasets

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

1. Breast Cancer + SHAP
2. Breast Cancer + Anchors
3. German Credit + SHAP
4. German Credit + Anchors

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
