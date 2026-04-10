# EXP1 Results: Adult Baseline

## Purpose

This document explains where EXP1 result artifacts live and how to interpret their roles.

It is the result-side companion to [docs/experiments/exp1_adult/README.md](../../experiments/exp1_adult/README.md).

## Result Families

### 1. Core Raw Run Artifacts

Primary root:

- [experiments/exp1_adult/results](../../../experiments/exp1_adult/results)

Typical contents:

- per-experiment `results.json`
- per-experiment `metrics.csv`
- method/model-specific subfolders such as `rf_shap`, `xgb_lime`, and tuning outputs

### 2. Reproducibility Artifacts

Root:

- [experiments/exp1_adult/reproducibility](../../../experiments/exp1_adult/reproducibility)

Purpose:

- multi-seed validation runs used to evaluate variance and reproducibility behavior

### 3. Human / LLM Evaluation Artifacts

Roots:

- [experiments/exp1_adult/human_eval](../../../experiments/exp1_adult/human_eval)
- [experiments/exp1_adult/llm_eval](../../../experiments/exp1_adult/llm_eval)

Purpose:

- semantic evaluation artifacts that are adjacent to EXP1 but conceptually distinct from the core quantitative result tree

### 4. Reproducibility Package Assets

Root:

- [experiments/exp1_adult/reproducibility_package](../../../experiments/exp1_adult/reproducibility_package)

Purpose:

- archival and packaging support for reproducibility distribution

## Source-of-Truth Rules

For raw EXP1 run outputs:

- source of truth is `experiments/exp1_adult/results/`

For reproducibility runs:

- source of truth is `experiments/exp1_adult/reproducibility/`

For interpretation:

- supporting narratives live in:
  - [experiments/exp1_adult/EVALUATION_REPORT.md](../../../experiments/exp1_adult/EVALUATION_REPORT.md)
  - [experiments/exp1_adult/EXPERIMENT_OBSERVATIONS.md](../../../experiments/exp1_adult/EXPERIMENT_OBSERVATIONS.md)
  - `docs/reports/...`

## Notes

EXP1 remains partly legacy in structure. The intent of this document is not to rewrite the historical layout, but to make it understandable from one place.
