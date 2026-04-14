# EXP3: Cross-Dataset Generalization Validation

This detailed note has been superseded as the primary entry point by:

- [exp3_cross_dataset/README.md](./exp3_cross_dataset/README.md)

Use the new README as the source of truth for experiment identity and package boundaries.

The content below is preserved as extended design rationale.

> Status: Prepared, not executed
>
> Thesis role: Smallest additional package to strengthen external validity beyond the Adult-only benchmark in EXP1/EXP2.

## 0. Implementation Update

As of 2026-04-13, EXP3 has moved from proposal to preparation.

Implemented preparation artifacts:

- dataset loaders for `breast_cancer` and `german_credit` in `src/data_loading/cross_dataset.py`;
- runner dispatch support for EXP3 datasets in `src/experiment/runner.py`;
- 24 generated configs under `configs/experiments/exp3_cross_dataset/`;
- config generation script at `scripts/generate_exp3_configs.py`;
- seed-specific model artifact preparation script at `scripts/train_exp3_models.py`;
- loader validation tests at `tests/test_cross_dataset_loader.py`;
- result-side semantics in `docs/results/exp3_cross_dataset/README.md`;
- session walkthrough and file-level inventory in
  [exp3_cross_dataset/EXP3_PREPARATION_WALKTHROUGH.md](./exp3_cross_dataset/EXP3_PREPARATION_WALKTHROUGH.md).

Deferred artifacts:

- trained EXP3 model binaries and preprocessors under `experiments/exp3_cross_dataset/models/`;
- raw EXP3 execution results under `experiments/exp3_cross_dataset/results/`;
- derived EXP3 analysis exports under `outputs/`.

Reason for deferral:

- the active EXP2 worker is still running, so EXP3 execution should begin only
  with the first Breast Cancer RF SHAP smoke test after EXP2 finishes.

## 1. Purpose

EXP3 is a deliberately small validation package designed to answer the most likely PhD-thesis external-validity objection:

> Are the benchmark conclusions specific to the Adult Income dataset, or do the main patterns persist on additional tabular domains?

EXP3 is not intended to duplicate the full EXP2 grid. Its function is to provide a compact, auditable, cross-dataset replication layer that complements:

- `EXP1`: baseline calibration and reproducibility on Adult
- `EXP2`: broad comparative and robustness benchmarking on Adult
- `EXP3`: external validation on additional tabular datasets

## 2. Claim Scope

EXP3 supports the following bounded claims:

- The framework is portable to multiple tabular datasets beyond Adult.
- The comparative behavior of selected explainers is not purely Adult-specific.
- The main trade-offs among fidelity, stability, sparsity, and runtime remain interpretable across domains.

EXP3 does not support:

- universal cross-domain claims across all tabular settings
- modality transfer claims outside tabular classification
- a replacement of EXP2 as the thesis' primary inferential cohort

## 3. Minimal Design Decision

### 3.1 Dataset Selection

Primary EXP3 datasets:

1. `breast_cancer`
2. `german_credit`

Rationale:

- `breast_cancer` is small, well-behaved, and computationally inexpensive. It provides a low-friction second domain with a very different feature profile from Adult.
- `german_credit` preserves a socioeconomic/risk-style classification setting without being a duplicate of Adult.
- Together they improve external validity while keeping implementation and runtime bounded.

Fallback if `german_credit` becomes operationally costly:

- replace `german_credit` with `bank_marketing`, but only if its preprocessing path is easier to operationalize in the existing framework

### 3.2 Model Selection

Included models:

1. `rf`
2. `xgb`

Rationale:

- They are already strong tabular baselines in the project.
- They reduce implementation variance compared with adding SVM/MLP in the cross-dataset stage.
- They support both tree-native and model-agnostic explanation comparisons cleanly.

### 3.3 Explainer Selection

Included explainers:

1. `shap`
2. `anchors`

Rationale:

- `shap` is a mainstream attribution baseline and performed strongly in EXP2.
- `anchors` offers a qualitatively different, rule-based explanation family and improves the methodological breadth of the validation package.
- Excluding `lime` and `dice` keeps EXP3 small while preserving heterogeneity of explanation style.

### 3.4 Seed and Sample Design

Included seeds:

- `42`
- `123`
- `456`

Per-quadrant sampling:

- `n = 100`

Resulting instance volume:

- `4 quadrants x 100 = 400 instances per experiment`

This keeps EXP3 large enough to be credible while avoiding the runtime inflation of the full EXP2 `n in {50,100,200}` sweep.

## 4. Planned Matrix

### 4.1 Experimental Factors

| Factor | Values |
|--------|--------|
| Datasets | `breast_cancer`, `german_credit` |
| Models | `rf`, `xgb` |
| Explainers | `shap`, `anchors` |
| Seeds | `42`, `123`, `456` |
| Sample size | `n=100` |

### 4.2 Total Planned Runs

`2 datasets x 2 models x 2 explainers x 3 seeds x 1 sample size = 24 runs`

### 4.3 Per-Run Metric Bundle

Enabled metrics:

- `fidelity`
- `stability`
- `sparsity`
- `cost`

Disabled in the minimal package:

- `domain`
- `counterfactual`

Rationale:

- This preserves direct comparability with the core quantitative layer from EXP2.
- It avoids the runtime and implementation overhead of DiCE-driven counterfactual metrics during the cross-dataset validation stage.

## 5. Proposed Naming Convention

EXP3 configs should follow:

```text
exp3_<dataset>_<model>_<explainer>_s<seed>_n100
```

Examples:

- `exp3_breast_cancer_rf_shap_s42_n100`
- `exp3_breast_cancer_xgb_anchors_s123_n100`
- `exp3_german_credit_rf_shap_s456_n100`

Config path convention:

```text
configs/experiments/exp3_cross_dataset/<dataset>/<model>_<explainer>_s<seed>_n100.yaml
```

Output path convention:

```text
experiments/exp3_cross_dataset/results/<dataset>/<model>_<explainer>/seed_<seed>/n_100/
```

## 6. Planned Execution Order

To maximize early completions and reduce thesis risk, the recommended execution order is:

1. `breast_cancer + rf + shap`
2. `breast_cancer + xgb + shap`
3. `breast_cancer + rf + anchors`
4. `breast_cancer + xgb + anchors`
5. `german_credit + rf + shap`
6. `german_credit + xgb + shap`
7. `german_credit + rf + anchors`
8. `german_credit + xgb + anchors`

Within each block:

- run seeds in order `42`, `123`, `456`

Rationale:

- SHAP jobs usually complete faster than Anchors.
- Breast Cancer should be cheaper than German Credit.
- This ordering creates analyzable partial evidence early, even before the full EXP3 grid finishes.

## 7. Minimal Deliverables Required

To make EXP3 thesis-defensible, the project should produce:

1. dataset loaders for `breast_cancer` and `german_credit`
2. frozen trained model artifacts for `rf` and `xgb` on both datasets
3. 24 YAML experiment configs
4. completed `results.json` and `metrics.csv` outputs for qualified runs
5. one compact analysis export comparing EXP2 Adult patterns with EXP3 patterns

## 8. Recommended Analysis Questions

The final EXP3 analysis should answer:

1. Does SHAP still dominate fidelity/stability on additional datasets?
2. Does Anchors remain materially slower than SHAP outside Adult?
3. Are model-level rankings broadly preserved across datasets?
4. Which conclusions appear dataset-stable versus dataset-sensitive?

These questions are sufficient to defend an external-validation chapter without requiring a second full benchmark campaign.

## 9. Success Criteria

EXP3 should be considered successful if:

1. Both additional datasets are fully operational in the framework.
2. At least 80% of the 24 planned runs complete with valid artifacts.
3. The analysis can report at least one dataset-stable comparative pattern and at least one dataset-sensitive pattern.
4. Thesis language can move from "Adult-only benchmark" to "Adult-centered benchmark with external tabular validation."

## 10. Risk Controls

Primary risks:

- dataset-loader implementation overhead
- preprocessing mismatch across datasets
- Anchors runtime inflation
- incomplete artifact coverage near thesis deadlines

Mitigations:

- keep the matrix fixed at 24 runs
- keep only `rf` and `xgb`
- keep only `shap` and `anchors`
- keep only `n=100`
- run SHAP blocks first to secure early results

## 11. Planned Run List

### 11.1 Breast Cancer

| Dataset | Model | Explainer | Seeds | Sample size | Planned runs |
|---------|-------|-----------|-------|-------------|--------------|
| `breast_cancer` | `rf` | `shap` | `42,123,456` | `n=100` | 3 |
| `breast_cancer` | `rf` | `anchors` | `42,123,456` | `n=100` | 3 |
| `breast_cancer` | `xgb` | `shap` | `42,123,456` | `n=100` | 3 |
| `breast_cancer` | `xgb` | `anchors` | `42,123,456` | `n=100` | 3 |

### 11.2 German Credit

| Dataset | Model | Explainer | Seeds | Sample size | Planned runs |
|---------|-------|-----------|-------|-------------|--------------|
| `german_credit` | `rf` | `shap` | `42,123,456` | `n=100` | 3 |
| `german_credit` | `rf` | `anchors` | `42,123,456` | `n=100` | 3 |
| `german_credit` | `xgb` | `shap` | `42,123,456` | `n=100` | 3 |
| `german_credit` | `xgb` | `anchors` | `42,123,456` | `n=100` | 3 |

## 12. Thesis Positioning

Recommended thesis wording:

> EXP3 serves as a cross-dataset external validation layer. Whereas EXP2 provides the primary, high-depth comparative benchmark on Adult, EXP3 tests whether the principal quantitative trade-offs observed in EXP2 remain visible on additional tabular classification datasets under a constrained but reproducible evaluation matrix.

This keeps the thesis honest, methodologically strong, and realistically scoped.
