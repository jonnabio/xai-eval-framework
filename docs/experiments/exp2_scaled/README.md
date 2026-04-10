# EXP2 Scaled: Adult Robustness Benchmark

## Purpose

EXP2 scaled is the primary Adult-dataset robustness benchmark.

This is the main multi-factor experiment family used to study explainer behavior across:

- model family
- explainer method
- random seed
- per-quadrant sampling intensity

## Thesis Role

EXP2 scaled is the project's main inferential benchmark layer on Adult.

It supports:

- robustness comparisons
- multi-seed analysis
- sample-size sensitivity
- method ranking under a fixed benchmark environment

## Factor Matrix

Declared in [configs/experiments/exp2_scaled/manifest.yaml](../../../configs/experiments/exp2_scaled/manifest.yaml):

- models: `rf`, `xgb`, `svm`, `mlp`, `logreg`
- explainers: `shap`, `lime`, `anchors`, `dice`
- seeds: `42`, `123`, `456`, `789`, `999`
- sample sizes: `50`, `100`, `200`

Planned total:

- `300` configurations

## Operational Notes

This family is computationally expensive because:

- many cells use expensive explainers such as Anchors and DiCE
- stability is enabled
- each configuration evaluates multiple sampled instances per quadrant
- the benchmark is repeated across multiple seeds and sample sizes

## Artifact Contract

Design:

- this document

Results guide:

- [docs/results/exp2_scaled/README.md](../../results/exp2_scaled/README.md)

Execution/config:

- [configs/experiments/exp2_scaled](../../../configs/experiments/exp2_scaled)

Raw outputs:

- [experiments/exp2_scaled/results](../../../experiments/exp2_scaled/results)

Derived outputs:

- `outputs/`
- statistical exports from analysis scripts

Interpretation:

- [docs/reports/paper_a](../../../docs/reports/paper_a)
- [docs/reports/paper_b](../../../docs/reports/paper_b)

## Source-of-Truth Boundary

This document defines what EXP2 scaled is.

The paper drafts may discuss findings and caveats, but they should not be treated as the primary design source of truth for the experiment family.
