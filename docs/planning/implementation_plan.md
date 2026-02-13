# Implementation Plan - Phase 1: SHAP Optimization (Kernel Explainer)

**Status:** Draft
**Role:** Architect
**Date:** 2026-02-04
**Context:** [Skipped Experiments Analysis](../context/skipped_experiments_analysis.md)

## 1. Executive Summary
This plan addresses the critical performance bottleneck observed in "Phase 1" of the recovery strategy. The `KernelExplainer` used for model-agnostic SHAP explanations (SVM, MLP) is computationally infeasible with the current background dataset size (100 random samples). We will implement **K-Means Summarization** to reduce the background dataset to $K=10$ weighted centroids, theoretically providing a 10x speedup while maintaining approximation accuracy.

## 2. Architecture & Design

### 2.1. Component: `SHAPTabularWrapper`
**File:** `src/xai/shap_tabular.py`

**Current Behavior:**
- `__init__` calls `sample_background_data` to select `n_background_samples` random instances.
- `KernelExplainer` computes Shapley values by integrating over these samples ($O(M \times N_{bg})$ evaluations per instance).

**Proposed Change:**
- Introduce a new initialization parameter: `use_kmeans: bool = False`.
- If `use_kmeans` is `True`:
    - Bypass `sample_background_data`.
    - Use `shap.kmeans(training_data, k=n_background_samples)` to generate weighted centroids.
    - Pass these centroids to `shap.KernelExplainer`.
- **Constraint:** Ensure `n_background_samples` acts as $K$ (number of centroids) when this mode is active.

### 2.2. Configuration Schema
**File:** `src/experiment/config.py` (Implicit) / YAML Configs

**Change:**
- The existing `explainer.params` dictionary in the YAML config will support the new `use_kmeans` key.
- No schema validation changes are anticipated as `params` is a flexible dictionary.

## 3. Implementation Steps

### Step 1: Modify `SHAPTabularWrapper`
- **Location**: `src/xai/shap_tabular.py`
- **Action**: Update `__init__` logic.
- **Detail**:
  ```python
  if kwargs.get('use_kmeans', False):
      # ... logic to use shap.kmeans ...
      self.background_data = shap.kmeans(training_data, self.n_background_samples)
  else:
      # ... existing sampling ...
  ```

### Step 2: Unit Testing
- **Location**: `tests/unit/xai/test_shap_tabular.py`
- **Action**: Add test case `test_shap_kmeans_initialization`.
- **Verification**:
    1. Initialize wrapper with `use_kmeans=True`.
    2. Check that `self.explainer.data` is of type `shap.utils.DenseData` or contains centroids.
    3. Run a dummy explanation to ensure no runtime errors.

### Step 3: Integration Verification (Smoke Test)
- **Location**: Local Execution
- **Action**: Create a temporary config `configs/smoke_test_shap_kmeans.yaml` targeting a small subset (10 instances) with `model: svm` or `mlp`.
- **Criteria**: Execution time per instance < 2 seconds (vs >30s baseline).

## 4. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Pickling Failure** | Medium | Low | `shap.kmeans` returns a custom object. If `ProcessPoolExecutor` fails to pickle it, the runner automatically falls back to `ThreadPoolExecutor`. We will verify this in the smoke test. |
| **Accuracy Loss** | Low | Medium | K-Means is a standard approximation. If results are wildly different, we can increase $K$ to 20 or 50. |
| **Dependency Version** | Low | Low | `shap` library versions can vary. We assume the installed version supports `kmeans` (standard feature). |

## 5. Definition of Done
1. `SHAPTabularWrapper` supports `use_kmeans`.
2. Unit tests pass.
3. Smoke test confirms speedup on local machine.
4. Recovery configs for MLP/SVM are generated/updated.
