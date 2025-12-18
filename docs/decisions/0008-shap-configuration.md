# 8. SHAP Configuration for Experiment 1

Date: 2025-12-18
Status: Accepted

## Context
We are evaluating XAI methods on the UCI Adult dataset using Random Forest and XGBoost models. To ensure fair benchmarking of fidelity and stability metrics, we must standardize the configuration of SHAP (Shapley Additive exPlanations), particularly `TreeExplainer`, which is the preferred method for tree-based models.

## Decision
We will use the following configuration for the `SHAPTabularWrapper`:

### 1. Explainer Selection
*   **Primary**: `shap.TreeExplainer`
    *   **Usage**: Applied to Random Forest and XGBoost models.
    *   **Rationale**: Provides exact Shapley values (feature consistency) and is significantly faster than model-agnostic methods.
*   **Fallback**: `shap.KernelExplainer`
    *   **Usage**: If a model is not supported by TreeExplainer (e.g., generic sklearn pipeline without tree attributes).
    *   **Rationale**: Model-agnostic approximation based on LIME principles but with Shapley theoretical guarantees.

### 2. Background Data Strategy
*   **Method**: Random Stratified Sampling.
*   **Size**: `100` samples.
*   **Rationale**: 
    *   SHAP uses background data to estimate the expected value $E[f(x)]$.
    *   Passing the entire training set (32k+ rows) to `KernelExplainer` is computationally infeasible. `TreeExplainer` handles it better but still benefits from a representative background for the `expected_value` calculation, or it uses the node information directly (interventional feature perturbation).
    *   We standardize on passing a background summary (100 samples) to ensure consistent `expected_value` calculation across explainer types.

### 3. Output Configuration
*   **Target Class**: Positive Class (`1`, e.g., ">50K").
*   **Format**: Dense numpy array `(n_samples, n_features)`.
*   **Values**: Marginal contributions (feature importance) that sum to $f(x) - E[f(x)]$.

### 4. Reproducibility
*   **Random State**: `42`.
*   Used for sampling the background dataset from the training data.

## Consequences
*   **Accuracy**: `TreeExplainer` gives us exact values, avoiding the sampling variance inherent in LIME or KernelSHAP (when using sufficient samples).
*   **Performance**: Fast generation allows for larger scale evaluation of stability properly.
*   **Memory**: Storing the background sample (100 rows) is negligible.

## References
*   Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. NeurIPS.
*   SHAP Documentation: https://shap.readthedocs.io/
