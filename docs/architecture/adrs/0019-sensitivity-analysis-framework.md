# 19. Sensitivity Analysis Framework

Date: 2026-01-02

## Status

Accepted

## Context

To ensure the reliability of XAI metrics, we need to understand their sensitivity to hyperparameter variations. Specifically:
-   **LIME**: Is the default `num_samples=5000` necessary, or can we reduce cost?
-   **SHAP**: Is the default `n_background=100` sufficient for stable estimates?

Traditional 5-Fold Cross-Validation is too computationally expensive for a broad parameter sweep (grid search). We need a more efficient but statistically valid approach to identifying "critical" parameters and "plateaus" (diminishing returns).

## Decision

We adopt a **Stratified Single-Split Sensitivity Analysis** framework:

1.  **Sampling Strategy**:
    -   Use a fixed stratified sample of **N ≈ 48** instances (12 per class quadrant).
    -   Fix random seed (`42`) across all runs to ensure paired comparisons are valid.

2.  **Metrics**:
    -   **Coefficient of Variation (CV)**: $\sigma / \mu$. Used to classify parameter sensitivity.
        -   **Robust**: CV < 0.05
        -   **Moderate**: 0.05 ≤ CV ≤ 0.10
        -   **Sensitive**: CV > 0.10
    -   **Percentage Change**: Comparison against the "Baseline" (Default config).
    -   **Plateau Detection**: Identify the parameter value where marginal improvement drops below 1%.

3.  **Hyperparameter Grids** (Log-Scale):
    -   **LIME `num_samples`**: `[500, 1000, 2000, 5000, 10000]`
    -   **SHAP `n_background`**: `[25, 50, 100, 200, 400]`

## Consequences

-   **Efficiency**: Reduces computational cost by ~80% compared to full CV, enabling broader parameter sweeps.
-   **Reproducibility**: Fixed seeds and stratified sampling ensure results are comparable.
-   **Actionable Insights**: Explicit "Robust/Sensitive" classification directly informs default parameter selection (e.g., reducing LIME samples to 1000).
-   **Limitation**: Does not measure generalization variance as robustly as CV, but sufficient for relative sensitivity comparisons.
