# EXP3 Results: Cross-Dataset Validation

## Purpose

This document defines the planned result semantics for EXP3.

It is the result-side companion to [docs/experiments/exp3_cross_dataset/README.md](../../experiments/exp3_cross_dataset/README.md).

## Current Status

Status:

- complete; both dataset partitions merged

The EXP3 model artifacts were trained, the Windows Breast Cancer partition
completed, the Linux/WSL German Credit partition completed, and both result
branches were merged into a single analysis branch.

Current raw result count:

- `24 / 24`

Merged branch:

```text
results/exp3-windows-breast-cancer
```

Merge commit:

```text
aa22d1112 Merge remote-tracking branch 'origin/results/exp3-linux-german-credit' into results/exp3-windows-breast-cancer
```

The merge procedure is documented in
[ADR 0012](../../adr/0012-exp3-partitioned-result-merge.md).

The preparation change inventory is documented in
[docs/experiments/exp3_cross_dataset/EXP3_PREPARATION_WALKTHROUGH.md](../../experiments/exp3_cross_dataset/EXP3_PREPARATION_WALKTHROUGH.md).

## Raw Artifact Root

Root:

- `experiments/exp3_cross_dataset/results/`

Layout:

```text
experiments/exp3_cross_dataset/results/<dataset>/<model>_<explainer>/seed_<seed>/n_100/
```

Per-run contents:

- `results.json`
- `metrics.csv`
- optional `instances/` checkpoint folder

## Completed Result Families

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

Completed total:

- `24` `results.json`
- `24` `metrics.csv`
- `12` Breast Cancer runs
- `12` German Credit runs

## Merged Analysis Snapshot

The merged EXP3 result set should be interpreted as a compact external
validation package, not as a replacement for the larger EXP2 benchmark.

Overall explainer means across both datasets, both models, and all seeds:

| Explainer | Accuracy | Fidelity | Faithfulness gap | Stability | Active-feature ratio | Duration (s) |
|---|---:|---:|---:|---:|---:|---:|
| `anchors` | 0.838 | 0.319 | 0.129 | 0.533 | 0.080 | 4684 |
| `shap` | 0.838 | 0.702 | 0.250 | 0.873 | 0.756 | 213 |

Interpretation:

- SHAP preserved a clear advantage on fidelity, faithfulness gap, and stability
  in the merged EXP3 unit.
- Anchors preserved the compact-explanation profile, with far fewer active
  features.
- Runtime favored SHAP overall in this EXP3 matrix because Anchors was much
  slower on both dataset partitions.
- The German Credit XGB block is a dataset/model-sensitive caveat: Anchors had
  slightly higher stability than SHAP there, even though SHAP retained higher
  fidelity.

Detailed interpretation is recorded in
[MERGED_ANALYSIS.md](./MERGED_ANALYSIS.md).

## Source-of-Truth Rules

For planned experiment design:

- [docs/experiments/exp3_cross_dataset/README.md](../../experiments/exp3_cross_dataset/README.md)

For planned execution manifest:

- [configs/experiments/exp3_cross_dataset/manifest.yaml](../../../configs/experiments/exp3_cross_dataset/manifest.yaml)

For future raw outputs:

- `experiments/exp3_cross_dataset/results/`

For derived analysis:

- `outputs/`

## Notes

EXP3 is designed to be small. It should not grow into another full EXP2-style
grid unless the thesis scope is explicitly revised.
