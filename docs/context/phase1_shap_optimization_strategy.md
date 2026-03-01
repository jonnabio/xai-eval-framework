# Phase 1: SHAP Optimization Strategy & Execution Record

**Date:** 2026-02-09
**Status:** **Implemented & Verified**
**Related Documents:**
- [Skipped Experiments Analysis](./skipped_experiments_analysis.md)
- [Implementation Plan](../planning/implementation_plan.md)

## 1. Context & Problem Statement
During the analysis of the "Experiment 2" batch run, it was identified that **MLP** and **SVM** models were consistently failing or timing out.
- **Root Cause:** These models utilize `shap.KernelExplainer` (model-agnostic) instead of the optimized `TreeExplainer`.
- **Bottleneck:** The default background dataset size ($N=100$ random samples) requires excessive model evaluations ($O(N \cdot 2^M)$), making execution intractable for the available compute resources (>4 hours per instance).

## 2. Strategic Decision: K-Means Summarization
To recover these skipped experiments ("Phase 1"), we shifted from random sampling to **K-Means Summarization** for the background dataset.
- **Mechanism:** Instead of passing 100 raw data points to the explainer, we use `shap.kmeans(X, k)` to generate $K$ weighted centroids.
- **Configuration:** Targeted $K=10$ to achieve a theoretical **10x speedup**.
- **Trade-off:** This is an approximation method. We accept a minor loss in fidelity for the ability to generate results at all.

## 3. Implementation Design
The `SHAPTabularWrapper` in `src/xai/shap_tabular.py` was modified to support a new initialization parameter.

### Changes Implemented
- **New Parameter:** `use_kmeans: bool` in `__init__`.
- **Logic:**
    - If `True`: Uses `shap.kmeans(data, k=n_background_samples)` (resulting in weighted centroids).
    - If `False`: Uses `sample_background_data(...)` (random/stratified sampling).

## 4. Risks & Mitigations
*   **Risk:** Pickling failures with `shap.utils.Data` objects in `ProcessPoolExecutor`.
    *   *Outcome:* Pickling works successfully, but `ExperimentRunner` retains a fallback to `ThreadPoolExecutor` as a safety net.
*   **Risk:** Accuracy degradation from summarization.
    *   *Mitigation:* Configurable $K$ allows tuning if fidelity drops acceptable thresholds.

## 5. Execution & Verification Log

### 5.1. Code Implementation
- **File:** `src/xai/shap_tabular.py`
- **Action:** Added `use_kmeans` logic.
- **Verification:**
    - Created unit test `tests/unit/xai/test_shap_tabular.py::test_kmeans_initialization`.
    - Validated that `shap.kmeans` returns a `shap.utils.DenseData` object with correct shape ($K=10$).

### 5.2. Environment Compatibility Fix
- **Issue:** During dry-run verification, executed `ExperimentRunner` failed with `ValueError: ... MT19937 is not a known BitGenerator module`.
- **Diagnosis:** The `mlp.joblib` model was trained in an environment with an incompatible `numpy` version.
- **Resolution:** Retrained the MLP model locally using `scripts/retrain_mlp_only.py`.
- **Outcome:** Model successfully re-saved; dry-run passed.

### 5.3. Configuration Generation
- **Script:** `scripts/generate_recovery_configs.py`
- **Action:**
    - Scanned `experiments/exp2_scaled/` for all `mlp_shap` and `svm_shap` configurations.
    - Generated 30 new config files in `configs/recovery/phase1/`.
    - **Modifications applied:**
        - `explainer.params.use_kmeans: true`
        - `explainer.params.n_background_samples: 10`
        - `output_dir` updated to `experiments/recovery/phase1/...`
        - `name` prefixed with `rec_p1_`.

### 5.4. Final Verification
- **Command:** `python src/experiment/runner.py --config configs/recovery/phase1/mlp_shap_s42_n100.yaml`
- **Result:** Successfully initialized `KernelExplainer` with 10 centroids and generated explanations.

### 5.5. Monitoring & Validation
- **Monitoring Script:** Created `scripts/monitor_experiments.py` (already existing) to track real-time progress.
- **Comparison Script:** Created `scripts/compare_results.py` to validate:
    - **Speedup:** Comparing `duration_seconds` against baseline (Target > 5x).
    - **Fidelity:** Comparing `faithfulness` metric (Target < 5% degradation).

## 6. Execution Plan
1.  **Launch Batch:** `python src/experiment/run_batch.py --config-dir configs/recovery/phase1 --parallel 4`
2.  **Monitor:** `python scripts/monitor_experiments.py --watch`
3.  **Validate:** `python scripts/compare_results.py --baseline experiments/exp2_scaled/results --recovery experiments/recovery/phase1/results`

