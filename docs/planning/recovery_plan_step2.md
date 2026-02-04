# Implementation Plan: Optimization of Kernel SHAP

**Goal:** Resume and complete the skipped `MLP` and `SVM` SHAP experiments by optimizing the explainer initialization.

## 1. Context
Previous attempts to run `SHAP` on `MLP` and `SVM` models resulted in hangs due to the computational cost of `KernelShap`. The default behavior (using large background samples) causes combinatorial explosions in model evaluations.

## 2. Proposed Changes

### A. Modify `src/experiment/runner.py`
We need to change how the `SHAPTabularWrapper` is initialized for non-tree models.

**Current Logic:**
```python
# Generic initialization often uses raw X_train or large random samples
self.explainer = SHAPTabularWrapper(...)
```

**New Logic:**
*   Detect if the method is `kernel` (implied for SVM/MLP).
*   Apply **K-Means Summarization** to the background data.

```python
import shap

# ... inside setup() ...
if model_type == "kernel":
    # Summarize background data to 10 representative centroids
    # This speeds up KernelShap by ~10x-20x
    background_data = shap.kmeans(self.dataset['X_train'], 10)
else:
    background_data = self.dataset['X_train']
```

### B. Create "Recovery" Configs
We do not want to re-run the *entire* batch. We will create a dedicated manifest for just the skipped items.

1.  **Identify Targets:**
    *   `experiments/exp2_scaled/mlp_shap_*.yaml`
    *   `experiments/exp2_scaled/svm_shap_*.yaml`

2.  **Scripting:**
    *   Create `scripts/generate_recovery_manifest.py`.
    *   This script will scan the `configs/` directory and generate a `batch_recovery.yaml` or a list of files that match the skipped criteria.

## 3. Verification Plan (Linux Workstation)

1.  **Pull Latest Code:** Ensure `skipped_experiments_analysis.md` is present.
2.  **Apply Optimization:** Edit `src/experiment/runner.py`.
3.  **Run Benchmark:**
    *   Select **one** skipped config (e.g., `mlp_shap_s42_n50`).
    *   Run it interactively: `python scripts/run_batch_experiments.py --config-dir ... --pattern mlp_shap_s42_n50.yaml`.
    *   **Success Metric:** Experiment completes in <10 minutes (vs. >3 hours).
4.  **Execute Phase 1 Batch:** Run all skipped MLP/SVM experiments.

## 4. Artifacts
*   `docs/context/skipped_experiments_analysis.md` (Context)
*   `src/experiment/runner.py` (Code Change)
*   `scripts/run_batch_recovery.sh` (Execution Script - to be created)
