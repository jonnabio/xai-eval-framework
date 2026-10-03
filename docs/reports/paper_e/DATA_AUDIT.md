# Paper E — source-data audit

**Date:** 2026-10-03
**Status:** Structural and identity audit only; no Paper E agreement statistic has been
computed.
**Reproduce:** `python scripts/paper_e_data_audit.py`

The machine-readable, per-run inventory is in [`DATA_AUDIT.json`](./DATA_AUDIT.json).
The audit reads the committed run JSON directly and records row validity, duplicate IDs,
method-pair intersections and classification-label consistency.

## Findings

### EXP2 — UCI Adult

Source: `experiments/exp2_scaled/results/`.

| Explainer | Run files | Nonempty valid runs | Source rows | Error/malformed rows |
|---|---:|---:|---:|---:|
| SHAP | 74 | 74 | 29,906 | 235 |
| LIME | 75 | 75 | 34,603 | 0 |
| Anchors | 75 | 57 | 25,809 | 42 |
| DiCE | 75 | 68 | 32,489 | 1 |

There are 75 `(model, seed, intensity)` blocks. The 278 invalid rows are
error-only records with no explanation payload: 235 SHAP, 42 Anchors and 1
DiCE. One SHAP run (`svm_shap`, seed 456, `n_50`) contains two duplicated
instance IDs. All copies of a duplicated ID are excluded from paired
comparisons rather than silently choosing one.

Of the 74 blocks with nonempty SHAP and LIME runs, 64 have identical valid
instance-ID sets. The other 10 are all SVM blocks; in each, the valid SHAP
IDs are a subset of the LIME IDs. There are no disagreements in stored
class labels, predictions or correctness flags on the matched SHAP/LIME IDs.
All-four-method ID sets are identical in 36 blocks only. The analysis must
therefore use explicitly reported intersections for each comparison; the
README's broad same-instance description is not true for every stored block.

### EXP3 — German Credit and Breast Cancer

Source: `experiments/exp3_cross_dataset/results/`.

| Dataset | Source run files | Instance rows | SHAP/Anchors exact-ID blocks |
|---|---:|---:|---:|
| German Credit | 12 | 2,120 | 6/6 |
| Breast Cancer | 12 | 1,368 | 6/6 |

All 24 files have valid, nonempty, finite `raw_top` maps, unique instance IDs
and classification fields. SHAP and Anchors have exactly matching IDs in all
12 dataset/model/seed blocks, with no stored classification-label mismatches.
The existing aggregate LIME file,
`outputs/analysis/exp3_lime_results.csv`, is tracked and must not be
overwritten.

## Consequences for the new LIME cohort

The existing SHAP/Anchors configs sample up to 100 instances **per error
quadrant**. `scripts/run_exp3_lime.py` instead samples 50 instances **per
true class**. Those procedures select different instances and counts (the
stored EXP3 blocks contain 114–182 instances). A Paper E LIME run must use the
exact stored SHAP `instance_id` values, not the script's current
`stratified_sample` output. The experiment runner's `original_index` is the
row index into the seeded `X_test` array; the new run must verify source labels
and predictions for each target ID before generating explanations.

The wrapper/source code confirms the prespecified interpretation:

- SHAP serializes signed class-1 values and sorts the top ten by absolute
  magnitude.
- LIME explains class 1; its full weight vector can be serialized as signed
  contributions and ranked by absolute magnitude.
- Anchors maps active rule features to `1.0` and all other features to zero.
  `raw_top` truncates to ten entries, so rows with ten active entries may not
  contain the full rule.
- DiCE stores absolute original-to-counterfactual feature changes, not signed
  additive attributions.

These checks support the plan's primary SHAP–LIME comparison and its restricted,
descriptive feature-set comparison for Anchors/DiCE. They do not establish any
agreement result.

## Audit limits

This audit does not recompute model predictions, verify the training-data or
model hashes, calculate explanation agreement, or establish a literature-based
threshold for practically meaningful agreement. Those checks remain part of
the experiment and analysis implementation.
