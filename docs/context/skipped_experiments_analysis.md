# Analysis of Skipped Experiments (Post-Batch Run)

**Date:** 2026-02-04
**Author:** Architect Agent
**Status:** Approved

## 1. Executive Summary
During the large-scale "Experiment 2" batch run, **101 configurations** were intentionally skipped to ensure the completion of the wider batch. These experiments represent critical gaps in the comparative analysis, specifically involving model-agnostic explainers (`Anchors`, `DiCE`) and non-tree-based models (`MLP`, `SVM`) using `SHAP`. This document analyzes the root causes of these failures and defines a remediation plan to be executed on a separate Linux workstation.

## 2. Methodology & Findings
The failures fall into three distinct categories:

### A. Algorithmic Instability (Target: Anchors)
*   **Affected Scope:** `Anchors` method across all models (~40 configs).
*   **Symptoms:** Infinite repetition of `IndexError: index -1 out of bounds`.
*   **Root Cause:** The `alibi` Anchors implementation (based on Multi-Armed Bandits) interacts poorly with our data preprocessing pipeline. It likely receives categorical data formatted unexpectedly (e.g., float vs. int mismatch), causing the internal candidate generation loop to fail or produce invalid indices.
*   **Severity:** **High**. Prevents any generation of Anchor-based explanations.

### B. Computational Infeasibility (Target: DiCE)
*   **Affected Scope:** `DiCE` method across all models (~40 configs).
*   **Symptoms:** Extreme execution time (>30s per instance) and log flooding with `UserWarning: X has feature names...`.
*   **Root Cause:**
    1.  **Metric Complexity:** DiCE solves an optimization problem for *each* generated counterfactual. Scaling this to 800 instances on a standard CPU is intractable.
    2.  **Integration Overhead:** The warning log flood suggests an inefficient tight loop where data is coerced repeatedly, adding significant I/O overhead.
*   **Severity:** **Medium**. Theoretically functional but practically unusable at current scale.

### C. Resource Saturation (Target: Kernel SHAP)
*   **Affected Scope:** `MLP` and `SVM` models using `SHAP` (~20 configs).
*   **Symptoms:** Process hangs (0% CPU or non-responsive) or runtimes exceeding 4 hours/experiment.
*   **Root Cause:** Unlike `TreeShap` (used for RF/XGBoost, $O(\log n)$), `MLP` and `SVM` force the use of `KernelShap`. This model-agnostic method requires exponentially many model evaluations ($2^N$ or large subsets) to approximate Shapley values. With ~100+ features (OHE), the default sampling is too aggressive for the available compute.
*   **Severity:** **Medium**. Can be resolved with approximation techniques.

---

## 3. Remediation Strategy
We will adopt a phased approach to recover these results. The priority is **Step 2 (Optimization)** to unblock the `SHAP` comparisons.

### Phase 1: SHAP Optimization (Kernel Explainer)
*   **Objective:** Recover `MLP` and `SVM` SHAP results.
*   **Technique:** **K-Means Summarization**.
*   **Implementation:**
    *   Instead of using the full training set or a large random sample as the "background dataset" for SHAP, we will use `shap.kmeans(X_train, k=10)`.
    *   This reduces the number of background comparisons per inference from $N=100+$ to $K=10$, offering a theoretical 10x speedup with minimal accumulation of error.
*   **Host:** Linux Workstation.

### Phase 2: Anchors Debugging
*   **Objective:** Fix the `IndexError` crash.
*   **Technique:** **Data Type Enforcement**.
*   **Implementation:**
    *   Create a standalone debug script to isolate `AnchorsTabularWrapper`.
    *   Explicitly enforce integer typing for categorical columns before passing to `alibi`.
    *   If that fails, loosen the `threshold` precision to prevent edge-case searches.

### Phase 3: DiCE Sampling (Lite Mode)
*   **Objective:** Obtain representative Counterfactual metrics.
*   **Technique:** **Downsampling**.
*   **Implementation:**
    *   Reduce `n` (instances to explain) from 200/50 to **20**.
    *   For research purposes, a smaller sample size is sufficient to establish the "high cost" baseline of DiCE without burning days of compute.

---

## 4. Next Steps
This context is preserved for the Linux Workstation environment. The immediate next action is to generate the **Implementation Plan** for Phase 1.
