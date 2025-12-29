# 13. Adoption of Faithfulness Metric (Prediction Gap) over R² Fidelity

Date: 2025-12-26

## Status

Accepted

## Context

In the initial design of Experiment 1, "Fidelity" was defined as the R² score of a surrogate model (GLM) trained on neighborhood data generated around an instance. This approach mimics the internal logic of LIME but has significant limitations:

1.  **Incompatibility with SHAP**: SHAP values are not derived from a local linear regression in the same direct way LIME is (especially TreeSHAP), making R² an inconsistent metric for comparison.
2.  **Implementation Complexity**: Correctly generating the specific local neighborhood used by different explainers to calculate an accurate R² is difficult and error-prone without deep integration into the library internals.
3.  **Literature Alignment**: Recent XAI benchmarks favor "Faithfulness" or "Infidelity" metrics based on feature masking (perturbation) rather than goodness-of-fit (R²). Ideally, if critical features (identified by the explanation) are removed, the model's prediction should change significantly.

## Decision

We have decided to replace the R²-based `FidelityMetric` with a masking-based `FaithfulnessMetric` for all experiments.

### New Metric Definition

The `FaithfulnessMetric` calculates two key scores:

1.  **Faithfulness Gap (Prediction Gap)**:
    - **Logic**: Identify the top-$k$ most important features from the explanation. Mask these features (replace with baseline/mean). Measure the absolute change in the model's prediction probability.
    - **Formula**: $|\text{Prediction}_{\text{original}} - \text{Prediction}_{\text{masked}}|$
    - **Interpretation**: Higher is better (indicates the explanation correctly identified improved features).

2.  **Faithfulness Correlation**:
    - **Logic**: For each feature in the instance, mask it individually and record the drop in prediction probability. Calculate the Pearson correlation between the explanation's feature importance weights and these prediction drops.
    - **Interpretation**: High positive correlation indicates that features assigned higher importance by the explainer are indeed more influential on the model's output.

## Consequences

### Positive
- **Method Agnostic**: Works fairly for both LIME and SHAP without relying on their internal optimization objectives.
- **Robustness**: Relies on direct model inference rather than surrogate fitting, reducing implementation errors.
- **Interpretability**: "Prediction drop" is a more intuitive measure of feature importance than an abstract R² score.

### Negative
- **Computational Cost**: Requires $N$ additional model inferences per instance (where $N$ is the number of features for correlation, or 2 for gap), whereas R² might be computed from existing explainer internals (if exposed).
- **Baseline Dependency**: The choice of masking value (zeros, mean, marginals) affects the score. we use the dataset mean (zero-imputation for standardized data) as the baseline.

## Implementation Details

- **Class**: `src.metrics.faithfulness.FaithfulnessMetric`
- **Output**: Returns `faithfulness_gap` (primary for now called 'fidelity' for compat) and `faithfulness_corr`.
- **Integration**: `ExperimentRunner` computes the global baseline (mean of X_train) during setup and passes it to the metric.

## References
- Sensitivity Analysis of (and Practitioners' Guide to) Interpretability Methods (Fel et al., 2021)
- Quantifying the interpretability of deep neural networks (Alvarez-Melis & Jaakkola, 2018)
