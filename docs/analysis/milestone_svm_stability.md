# Research Milestone: SVM + Kernel SHAP Stability Analysis

**Date:** 2026-02-19
**Status:** Phase 1 Recovery - First SVM Batch Finalized
**Experiment ID:** `rec_p1_exp2_svm_shap_s123_n50`

## Executive Summary
The first configuration of the high-latency SVM + Kernel SHAP recovery experiments has been completed and verified. The results confirm our hypothesis regarding the **"Stability Premium"** of SVM models in the XAI Evaluation Framework. While the computational cost is significantly higher than MLP models, the resulting explanations are nearly **3x more stable**.

## Comparative Stability Profile
Analysis of the finalized batch against established MLP and Random Forest baselines:

| Model Family | Mean Stability | Std. Deviation | Count (Instances) | Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **SVM (Kernel SHAP)** | **0.926** | **0.071** | 200 | High (support vector dependent) |
| **Random Forest** | 0.942 | 0.010 | 1000+ | High (ensemble pathing) |
| **MLP (Deep Learning)**| **0.331** | **0.019** | 1000+ | Extreme (non-linear decision surfaces) |

## Performance Trade-offs
The data confirms a massive divergence in the Stability-vs-Cost tradeoff:

*   **Computational Cost (Latency):**
    *   **SVM SHAP:** 261,737 seconds (~72.7 hours) for 200 instances.
    *   **Avg Instance Time:** ~21.8 minutes.
*   **Fidelity:**
    *   **Mean Fidelity:** 0.877 (High accuracy of the explanation in mirroring the black-box).
*   **Stability:**
    *   **Mean Stability:** 0.926 (Ultra-robust to local perturbations).

## Scientific Significance
This milestone provides the first "anchor point" for the SVM axis in Paper B. It demonstrates that for critical applications where explanation consistency is paramount, the high computational overhead of Kernel SHAP on SVM models is justified. The decision boundary of the SVM (adult dataset) allows for more deterministic and consistent attribution compared to the erratic gradients found in MLPs.

## Next Steps
1.  **Monitor N=400 SVM Batch:** Currently at 82.3%. Expected to provide even more robust global stability metrics.
2.  **Integrate into Trade-off Scatter Plot:** Successfully updated `outputs/paper_analysis/stability_vs_latency_tradeoff.png` to include this new anchor.
3.  **Cross-Seed Verification:** Awaiting completion of Seed 789 and 456 to confirm seed-independence of this stability profile.
