# EXP2 Comparative Results: Adult Fixed-Grid Benchmark

## Purpose

This document explains the result artifacts for the EXP2 comparative package.

It is the result-side companion to [docs/experiments/exp2_comparative/README.md](../../experiments/exp2_comparative/README.md).

## Raw Artifact Root

Primary root:

- [experiments/exp2_comparative/results](../../../experiments/exp2_comparative/results)

Structure:

- one folder per model-explainer combination
- typical outputs include `results.json` and `metrics.csv`

Examples:

- `rf_shap`
- `rf_lime`
- `svm_anchors`
- `xgb_dice`

## Intended Role

These results provide descriptive comparative coverage across model and explainer combinations on Adult.

They should be understood as simpler and shallower than the EXP2 scaled robustness matrix.

## Source-of-Truth Rules

For raw committed comparative outputs:

- source of truth is `experiments/exp2_comparative/results/`

For derived or merged outputs:

- source of truth is `outputs/`

For interpretation:

- source of truth is `docs/reports/...`

## Relationship To EXP2 Scaled

EXP2 comparative and EXP2 scaled should not be conflated:

- `exp2_comparative` = one model-explainer grid for descriptive breadth
- `exp2_scaled` = multi-seed, multi-sample-size robustness benchmark
