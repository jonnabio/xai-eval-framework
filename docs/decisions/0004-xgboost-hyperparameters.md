# 0004. XGBoost Hyperparameters for Adult Dataset

**Date**: 2025-12-16
**Status**: Accepted

## Context
-   **Dataset**: UCI Adult (binary classification, ~48k samples).
-   **Purpose**: Baseline model for XAI evaluation (not hyperparameter optimization).
-   **Comparison**: Should be comparable to the Random Forest model (100 trees, max_depth=10).

## Decision
We will configure the XGBoost baseline with the following hyperparameters:

-   `n_estimators`: **100**
    -   *Justification*: Matches the Random Forest baseline for fair comparison of ensemble size.
-   `max_depth`: **6**
    -   *Justification*: XGBoost default. Shallower than RF (usually) because boosting reduces bias sequentially, whereas bagging (RF) reduces variance with deeper trees.
-   `learning_rate`: **0.1**
    -   *Justification*: Standard robust default for gradient boosting.
-   `objective`: `binary:logistic`
    -   *Justification*: Standard for binary classification tasks.
-   `random_state`: **42**
    -   *Justification*: Critical for reproducibility of the baseline.

## Alternatives Considered
1.  **Tuned Hyperparameters**
    -   *Status*: Rejected
    -   *Reason*: Adds a confounding variable to the XAI evaluation. We want to evaluate the *explanation method's* fidelity on a standard model, not the model's peak performance.
2.  **Linear Booster (`gblinear`)**
    -   *Status*: Rejected
    -   *Reason*: We specifically need non-linear decision boundaries to test XAI methods' ability to explain complex interactions.
3.  **Deeper Trees (e.g., 10+)**
    -   *Status*: Rejected
    -   *Reason*: High risk of overfitting on this dataset size, and makes "exact" explanation computation (like TreeSHAP) significantly slower.
