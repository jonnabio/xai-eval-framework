# EXP2 Comparative: Adult Fixed-Grid Benchmark

## Purpose

EXP2 comparative is the broad but fixed-grid Adult benchmark used for descriptive comparison across model and explainer combinations.

It is the smaller, simpler EXP2 package relative to `exp2_scaled`.

## Scope

Dataset:

- `adult`

Primary role:

- descriptive comparative context across model and explainer families

## Factor Matrix

Defined by configs under [configs/experiments/exp2_comparative](../../../configs/experiments/exp2_comparative):

- models: `logreg`, `mlp`, `rf`, `svm`, `xgb`
- explainers: `shap`, `lime`, `anchors`, `dice`
- one config per model-explainer pair

This package is intentionally smaller than `exp2_scaled` because it does not expand into the full multi-seed, multi-sample-size grid.

## Artifact Contract

Design:

- this document

Results guide:

- [docs/results/exp2_comparative/README.md](../../results/exp2_comparative/README.md)

Execution/config:

- [configs/experiments/exp2_comparative](../../../configs/experiments/exp2_comparative)

Raw outputs:

- [experiments/exp2_comparative/results](../../../experiments/exp2_comparative/results)

Derived outputs:

- `outputs/`

Interpretation:

- `docs/reports/paper_a/`
- `docs/reports/paper_b/`

## Relationship To Other Packages

- EXP1 provides the baseline and training foundation.
- EXP2 comparative provides broad descriptive coverage on Adult.
- EXP2 scaled provides the main robustness and inferential benchmark on Adult.
