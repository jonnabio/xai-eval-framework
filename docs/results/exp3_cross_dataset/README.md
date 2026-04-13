# EXP3 Results: Cross-Dataset Validation

## Purpose

This document defines the planned result semantics for EXP3.

It is the result-side companion to [docs/experiments/exp3_cross_dataset/README.md](../../experiments/exp3_cross_dataset/README.md).

## Current Status

Status:

- prepared / not yet executed

No EXP3 raw result tree is expected to be complete until the EXP3 model
artifacts are trained and at least one smoke-test run has passed. The current
preparation stage provides dataset-loader support, config generation, and a
model-training entry point, but execution is deferred while EXP2 is active.

## Planned Raw Artifact Root

Planned root:

- `experiments/exp3_cross_dataset/results/`

Planned layout:

```text
experiments/exp3_cross_dataset/results/<dataset>/<model>_<explainer>/seed_<seed>/n_100/
```

Expected per-run contents:

- `results.json`
- `metrics.csv`
- optional `instances/` checkpoint folder

## Planned Result Families

Datasets:

- `breast_cancer`
- `german_credit`

Models:

- `rf`
- `xgb`

Explainers:

- `shap`
- `anchors`

Seeds:

- `42`
- `123`
- `456`

Sample size:

- `n_100`

Planned total:

- `24` run folders

## Source-of-Truth Rules

For planned experiment design:

- [docs/experiments/exp3_cross_dataset/README.md](../../experiments/exp3_cross_dataset/README.md)

For planned execution manifest:

- [configs/experiments/exp3_cross_dataset/manifest.yaml](../../../configs/experiments/exp3_cross_dataset/manifest.yaml)

For future raw outputs:

- `experiments/exp3_cross_dataset/results/`

For future derived analysis:

- `outputs/`

## Notes

EXP3 is designed to be small. It should not grow into another full EXP2-style grid unless the thesis scope is explicitly revised.
