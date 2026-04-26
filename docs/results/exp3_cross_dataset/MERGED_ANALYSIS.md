# EXP3 Merged Analysis: Cross-Dataset Validation

Date: 2026-04-26
Status: Complete raw analysis snapshot

## Scope

This document summarizes the merged EXP3 result set after combining:

- Windows Breast Cancer partition
- Linux/WSL German Credit partition

The merged artifact branch is:

```text
results/exp3-windows-breast-cancer
```

The merged commit is:

```text
aa22d1112
```

EXP3 is a compact external-validation package. It tests whether selected
patterns from the Adult-centered EXP1/EXP2 evidence stream remain interpretable
on two additional tabular classification domains.

## Completeness

The merged result tree contains the complete planned EXP3 matrix:

```text
results.json: 24 / 24
metrics.csv: 24 / 24
breast_cancer runs: 12 / 12
german_credit runs: 12 / 12
```

Completed factors:

| Factor | Values |
|---|---|
| Datasets | `breast_cancer`, `german_credit` |
| Models | `rf`, `xgb` |
| Explainers | `shap`, `anchors` |
| Seeds | `42`, `123`, `456` |
| Sample size | `n_100` |

## Dataset-Level Results

Mean metrics by dataset, model, and explainer:

| Dataset | Model | Explainer | Accuracy | Fidelity | Faithfulness gap | Stability | Active-feature ratio | Duration (s) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `breast_cancer` | `rf` | `anchors` | 0.962 | 0.265 | 0.101 | 0.304 | 0.069 | 6711 |
| `breast_cancer` | `rf` | `shap` | 0.962 | 0.779 | 0.278 | 0.953 | 0.979 | 125 |
| `breast_cancer` | `xgb` | `anchors` | 0.956 | 0.208 | 0.091 | 0.480 | 0.069 | 2561 |
| `breast_cancer` | `xgb` | `shap` | 0.956 | 0.607 | 0.349 | 0.953 | 0.333 | 338 |
| `german_credit` | `rf` | `anchors` | 0.719 | 0.351 | 0.109 | 0.672 | 0.115 | 7707 |
| `german_credit` | `rf` | `shap` | 0.719 | 0.714 | 0.149 | 0.985 | 0.908 | 204 |
| `german_credit` | `xgb` | `anchors` | 0.713 | 0.451 | 0.216 | 0.677 | 0.068 | 1760 |
| `german_credit` | `xgb` | `shap` | 0.713 | 0.711 | 0.223 | 0.601 | 0.805 | 183 |

Note on `sparsity`: the stored metric is `nonzero_percentage`, so lower values
mean a more compact explanation. This document uses "active-feature ratio" to
avoid ambiguity.

## Overall Explainer Results

Across both datasets, both models, and all seeds:

| Explainer | Accuracy | Fidelity | Faithfulness gap | Stability | Active-feature ratio | Duration (s) |
|---|---:|---:|---:|---:|---:|---:|
| `anchors` | 0.838 | 0.319 | 0.129 | 0.533 | 0.080 | 4684 |
| `shap` | 0.838 | 0.702 | 0.250 | 0.873 | 0.756 | 213 |

## Paired Interpretation

Within matched dataset/model/seed cells, SHAP minus Anchors averaged:

| Metric | Mean paired difference |
|---|---:|
| Accuracy | 0.000 |
| Duration (s) | -4472 |
| Cost (ms) | -1741 |
| Active-feature ratio | +0.676 |
| Fidelity | +0.384 |
| Faithfulness gap | +0.120 |
| Stability | +0.340 |

Interpretation:

- Accuracy differences are zero because paired explainers evaluate the same
  model predictions.
- SHAP is higher on fidelity, faithfulness gap, and stability.
- Anchors is far more compact, with a much lower active-feature ratio.
- In this EXP3 matrix, SHAP is also faster on average.

## Main Findings

1. **SHAP generalizes as the stronger technical explainer.** Across the merged
   EXP3 package, SHAP has higher fidelity, higher faithfulness gap, and higher
   stability than Anchors.

2. **Anchors remains the compact explanation family.** Anchors consistently uses
   far fewer active features, preserving its rule-like explanatory profile.

3. **Runtime is not a simple SHAP penalty.** In this cross-dataset package,
   Anchors was slower overall. This matters for thesis language because it
   prevents overgeneralizing the common claim that SHAP is always the expensive
   option.

4. **German Credit XGB is the important caveat.** In the German Credit XGB block,
   Anchors slightly exceeded SHAP on stability. SHAP still had higher fidelity,
   but this block provides the dataset/model-sensitive finding required for a
   balanced external-validation narrative.

## Paper and Thesis Impact

### Paper A

EXP3 strengthens the framework paper by showing that the pipeline is not limited
to Adult Income. The correct claim is that the framework supports reproducible
multi-dataset tabular benchmarking, with the primary inferential evidence still
coming from EXP2.

### Paper B

Although Paper B focuses on LIME and SHAP, EXP3 supports the broader
quality-cost frontier argument. SHAP remains strong on technical quality metrics,
while compact rule-style explanations can trade off fidelity and runtime.

### Paper C

EXP3 supplies paired explanation artifacts suitable for semantic evaluation.
Dense SHAP explanations and compact Anchors rules can be compared on identical
instances to test whether human or LLM judges prefer compactness over technical
faithfulness.

### Thesis

EXP3 allows thesis wording to move from "Adult-only benchmark" to
"Adult-centered benchmark with two-domain external tabular validation." The
bounded claim is:

> In two additional tabular domains, SHAP preserved its technical-quality
> advantage over Anchors on fidelity-oriented metrics, while Anchors preserved a
> compact rule-style profile. The German Credit XGB block shows that some
> stability behavior remains dataset/model-sensitive.

## Limitations

- EXP3 is intentionally small and should not be interpreted as a universal
  cross-domain benchmark.
- The result set compares only `shap` and `anchors`; it does not re-run the full
  EXP2 explainer family.
- Stability and fidelity are implementation-specific to the framework's metric
  definitions and should be cited with the metric implementation paths.
- The merged branch is artifact-heavy because it preserves per-instance
  checkpoint JSON files.
