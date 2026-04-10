# EXP2 Scaled Results: Adult Robustness Benchmark

## Purpose

This document explains the result semantics for the main EXP2 scaled benchmark.

It is the result-side companion to [docs/experiments/exp2_scaled/README.md](../../experiments/exp2_scaled/README.md).

## Result Layers

### 1. Base Committed Run Artifacts

Primary root:

- [experiments/exp2_scaled/results](../../../experiments/exp2_scaled/results)

This is the base committed run tree for the benchmark.

Typical layout:

```text
experiments/exp2_scaled/results/<model>_<explainer>/seed_<seed>/n_<sample_size>/
```

Typical per-run contents:

- `results.json`
- `metrics.csv`
- optional `instances/` checkpoint folder

### 2. Recovery Artifacts

Primary recovery root:

- [experiments/recovery/phase1/results](../../../experiments/recovery/phase1/results)

Purpose:

- rerun or recovery outputs for selected missing or weak cells, especially SHAP-related recovery slices

These are not the same thing as the base committed benchmark tree.

### 3. Recovery Overlay Export

Overlay source currently used in analysis:

- [outputs/batch_results.csv](../../../outputs/batch_results.csv)

Observed role in the current codebase:

- this CSV is used as a recovery overlay in the EXP2 statistical analysis workflow
- it can replace or fill selected SHAP cells relative to the committed `exp2_scaled/results` tree

This means "present on disk in the committed tree" and "included in the analyzable merged snapshot" are not identical concepts.

### 4. Derived Analysis Outputs

Current output roots include:

- [outputs/paper_analysis](../../../outputs/paper_analysis)
- [outputs/recovery_results.csv](../../../outputs/recovery_results.csv)

Purpose:

- merged exports
- comparison views
- non-manuscript visual summaries

### 5. Paper / Thesis Assets

Interpretive and reporting assets live under:

- [docs/reports/paper_a](../../../docs/reports/paper_a)
- [docs/reports/paper_b](../../../docs/reports/paper_b)

These should be treated as reporting layers, not as the raw result source of truth.

## Source-of-Truth Rules

For raw committed EXP2 scaled outputs:

- source of truth is `experiments/exp2_scaled/results/`

For recovery reruns:

- source of truth is `experiments/recovery/phase1/results/`

For merged recovery overlays used in analysis:

- source of truth is the documented analysis pipeline, currently including `outputs/batch_results.csv`

For paper claims:

- source of truth is the qualified analysis outputs and manuscript reporting under `docs/reports/...`

## Important Distinction

EXP2 scaled has at least four different meanings of "results":

1. raw committed run folders
2. recovery rerun folders
3. merged analyzable overlays
4. paper-facing qualified summaries

This document exists so those meanings do not have to be reconstructed from scripts and paper drafts alone.

## Qualification Rules

For the detailed distinction between raw artifacts, recovery overlays, and analyzable cohorts, see:

- [QUALIFICATION.md](./QUALIFICATION.md)
