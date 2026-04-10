# EXP1: Adult Baseline

## Purpose

EXP1 establishes the baseline experimental environment on the Adult Income dataset.

It serves as the calibration layer for:

- dataset preprocessing
- model training artifacts
- core XAI pipeline validation
- early metric sanity checks
- reproducibility packaging

## Scope

Dataset:

- `adult`

Primary role:

- baseline and calibration

Secondary role:

- provides frozen model artifacts later reused by EXP2

## Main Components

Located under [experiments/exp1_adult](../../../experiments/exp1_adult):

- trained models
- baseline experiment scripts
- local reports
- reproducibility materials
- early observations and evaluation summaries

## Design Summary

EXP1 is intentionally narrower than EXP2.

Its design goal is not full-factor breadth. It is to prove the pipeline works end-to-end on a single canonical tabular task and to produce trusted model artifacts for later benchmarking.

Historically, EXP1 includes:

- Random Forest and XGBoost baseline work
- SHAP and LIME baseline comparisons
- reproducibility and methodology support materials

## Source-of-Truth Links

- experiment assets: [experiments/exp1_adult](../../../experiments/exp1_adult)
- local experiment readme: [experiments/exp1_adult/README.md](../../../experiments/exp1_adult/README.md)
- observations: [experiments/exp1_adult/EXPERIMENT_OBSERVATIONS.md](../../../experiments/exp1_adult/EXPERIMENT_OBSERVATIONS.md)
- evaluation report: [experiments/exp1_adult/EVALUATION_REPORT.md](../../../experiments/exp1_adult/EVALUATION_REPORT.md)
- results guide: [docs/results/exp1_adult/README.md](../../results/exp1_adult/README.md)

## Artifact Contract

Design:

- this document

Execution/config:

- legacy root configs such as [exp1_adult_rf_shap.yaml](../../../configs/experiments/exp1_adult_rf_shap.yaml)

Raw outputs:

- `experiments/exp1_adult/results/`

Derived outputs:

- `outputs/`

Interpretation:

- `docs/reports/...`

## Known Limitation

EXP1 documentation remains partly legacy and asset-centric. This README exists to anchor EXP1 in the new `docs/experiments` structure without rewriting all historical materials.
