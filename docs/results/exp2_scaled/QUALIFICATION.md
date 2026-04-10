# EXP2 Scaled Artifact Qualification

## Purpose

This note documents how to interpret EXP2 scaled results when raw run folders, recovery artifacts, and analysis overlays do not all describe the same cohort.

It exists so the qualification rules are not only embedded in scripts and paper drafts.

## Result Layers

EXP2 scaled has multiple result layers:

1. Base committed result tree
2. Recovery rerun artifacts
3. Batch CSV overlay
4. Qualified analysis cohort
5. Paper/thesis reporting summaries

## 1. Base Committed Result Tree

Root:

- [experiments/exp2_scaled/results](../../../experiments/exp2_scaled/results)

This is the main raw artifact tree.

Expected run-level path:

```text
experiments/exp2_scaled/results/<model>_<explainer>/seed_<seed>/n_<sample_size>/
```

Expected run-level files:

- `results.json`
- `metrics.csv`

Optional checkpoint folder:

- `instances/`

## 2. Recovery Rerun Artifacts

Root:

- [experiments/recovery/phase1/results](../../../experiments/recovery/phase1/results)

These are remediation outputs and should not be silently treated as part of the base committed tree.

## 3. Batch CSV Overlay

Known overlay source:

- [outputs/batch_results.csv](../../../outputs/batch_results.csv)

Known use:

- loaded by [scripts/run_exp2_statistical_analysis.py](../../../scripts/run_exp2_statistical_analysis.py)
- used to overlay selected recovery rows onto the committed EXP2 run-level metrics

Important consequence:

- a cell can be analyzable through the overlay even if the committed raw tree has a missing, empty, or superseded artifact

## 4. Qualified Analysis Cohort

The qualified cohort is not simply "all folders under `experiments/exp2_scaled/results`."

Qualification should consider:

- whether `results.json` exists
- whether `results.json` is non-empty and parseable
- whether metrics required by the analysis are present
- whether a recovery overlay supersedes a base-tree cell
- whether the analysis requires complete blocks or matched pairs

The current qualification implementation should be read from:

- [scripts/run_exp2_statistical_analysis.py](../../../scripts/run_exp2_statistical_analysis.py)

## 5. Reporting Cohort

Paper and thesis claims should cite the qualified analysis cohort rather than raw folder counts alone.

Relevant reporting roots:

- [docs/reports/paper_a](../../../docs/reports/paper_a)
- [docs/reports/paper_b](../../../docs/reports/paper_b)

## Practical Rule

Use this rule when reading EXP2 scaled results:

- raw artifact presence: inspect `experiments/exp2_scaled/results/`
- recovery provenance: inspect `experiments/recovery/phase1/results/` and `outputs/batch_results.csv`
- analyzable counts and inferential cohorts: inspect `scripts/run_exp2_statistical_analysis.py` outputs and reporting docs
- paper-ready interpretation: inspect `docs/reports/...`

## Recommendation

Before final thesis submission, generate a frozen EXP2 qualification snapshot that records:

- planned cells
- base committed artifacts
- empty artifacts
- malformed artifacts
- overlay replacements
- final analyzable unique runs
- block-complete cohorts
- matched-pair cohorts

That snapshot should become the auditable source for all final EXP2 coverage claims.
