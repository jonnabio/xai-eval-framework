## Model Performance Context

The Random Forest model achieved a robust test accuracy of 85.48%, providing a reliable decision boundary for evaluating interpretability. Conversely, the XGBoost model converged to a baseline accuracy of 50.0%, indicating a failure to learn meaningful patterns in this experimental configuration. Consequently, the following XAI metric evaluation primarily focuses on the Random Forest model to ensuring the validity of the explanations.

## Fidelity Analysis

Fidelity measures how accurately the surrogate explanation model resembles the black-box model's predictions. For the Random Forest model, **SHAP** demonstrated superior fidelity ($R^2 \approx 0.58$) compared to **LIME** ($R^2 \approx 0.11$). This stark contrast highlights a limitation of LIME's local linear approximation when applied to the highly non-linear, high-dimensional decision boundaries characteristic of Random Forest ensembles. SHAP's TreeExplainer, which leverages the exact tree structure, captures these non-linearities more effectively than LIME's perturbation-based sampling.

## Stability Analysis

Stability assesses the consistency of explanations for the same instance under identical conditions.

*   **SHAP (RF)** achieved exceptional stability (0.95), benefiting from the deterministic nature of the TreeExplainer algorithm.
*   **LIME (RF)** exhibited poor stability (0.09), a known consequence of its stochastic sampling process.

This result confirms that while LIME is model-agnostic, its inherent randomness (without strict seed control and high sample counts) makes it less suitable for applications requiring consistent regulatory auditing.

## Sparsity and Faithfulness Gap

LIME generated significantly sparser explanations (Sparsity $\approx$ 0.09) than SHAP (Sparsity $\approx$ 0.46), adhering to its design goal of providing interpretable, low-complexity formulas. However, this sparsity comes at the cost of the aforementioned fidelity. The Faithfulness Gap metric further corroborates the reliability of SHAP, showing a more consistent alignment with the true model behavior across valid instances.
