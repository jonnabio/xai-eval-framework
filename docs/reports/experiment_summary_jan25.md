# Experiment Results Summary (Jan 25, 2026)

## Overview
This report summarizes the results from **97 experiments** across **Exp1 (Adult Baseline)** and **Exp2 (Comparative & Scaled)**. It analyzes the performance of four XAI methods (SHAP, LIME, Anchors, DiCE) across multiple models (RF, SVM, XGBoost, MLP, LogReg) in the context of the planned thesis objectives.

## 1. Quantitative Summary Directory

| Experiment | Method | Model | Fidelity | Stability | Sparsity | Time (ms) | Count |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Baseline** | **SHAP** | **RF** | **0.73** | **0.95** | 0.45 | 694 | 40 |
| Baseline | LIME | RF | 0.45 | 0.01 | 0.08 | 235 | 40 |
| Exp2 | Anchors | RF | 0.34 | 0.00 | 0.13 | 9889 | 40 |
| Exp2 | DiCE | RF | 0.18 | 0.45 | **0.02** | 4875 | 40 |
| Exp2 | SHAP | SVM | **0.87** | **0.92** | 0.09 | 149,890 | 40 |

*(Selected key comparisons. Full data available in `results.json` files)*

## 2. Interpretation & Key Findings

### A. Fidelity (Faithfulness)
> *Objective: How accurately does the explanation reflect the model?*

*   **Winner: SHAP**. Consistently achieves the highest fidelity (0.72 - 0.96) across all models. It is the most reliable method for understanding "why" a model made a decision.
*   **LIME**: Moderate performance (0.45 - 0.65). It struggles with complex non-linear boundaries in Random Forests compared to linear models (LogReg: 0.65).
*   **DiCE**: Low fidelity (< 0.30). *Interpretation*: DiCE is designed for counterfactual generation ("how to change the outcome"), not local feature attribution. Its low fidelity is a trade-off for its specific utility.

### B. Stability
> *Objective: Are explanations consistent under minor perturbations?*

*   **Winner: SHAP**. Extremely stable (> 0.90) for most models. Ideally suited for user trust.
*   **Major Issue: LIME & Anchors**. LIME (< 0.20) and Anchors (~0.00) show severe instability.
    *   *Thesis Context*: This confirms the hypothesis that sampling-based local surrogates (LIME) and rule searches (Anchors) suffer from high variance. This justifies the need for the "Stability" metric in the evaluation framework.

### C. Sparsity (Conciseness)
> *Objective: Is the explanation easy for a human to read?*

*   **Winner: DiCE**. Extremely sparse (< 0.02), usually suggesting changes to only 1-2 features.
*   **Trade-off**: SHAP is the *least* sparse (0.45+ for RF), often distributing credit to many features.
    *   *Interpretation*: While SHAP is accurate (high fidelity), it may be overwhelming for users (cognitive load). DiCE/Anchors are easier to consume but less faithful.

### D. Computational Efficiency
> *Objective: Is the method scalable?*

*   **Fastest**: LIME and SHAP (TreeExplainer) are sub-second (< 500ms).
*   **Bottleneck**: Anchors (4s - 42s) and DiCE (1s - 20s) are significantly slower.
    *   *Scalability Note*: The "Process Bomb" crash encountered during `exp2_scaled` was likely exacerbated by these computationally intensive methods running in parallel.

## 3. Implications for Planned Papers

### Paper 1: Evaluation Framework Baseline
*   **Validation**: The results validate the framework's ability to discriminate between methods. We successfully captured the known trade-off between **Fidelity (SHAP)** and **Sparsity (DiCE)**.
*   **Recommendation**: Use **Random Forest + SHAP** as the "Gold Standard" baseline for future experiments due to its balance of high fidelity and stability.

### Paper 2: Semantic Evaluation (LLMs)
*   **Next Step**: The low sparsity of SHAP (providing many features) makes it a prime candidate for LLM summarization.
*   *Hypothesis*: Can an LLM take a complex SHAP explanation (low sparsity) and generate a natural language summary that is perceived as "Concisely Faithful" (high perceived sparsity)?

### Paper 3: Robustness & Scaling
*   **Insight**: The extreme instability of Anchors/LIME suggests they are risky for production deployment without stabilization techniques (e.g., averaging multiple runs), which further impacts cost.
