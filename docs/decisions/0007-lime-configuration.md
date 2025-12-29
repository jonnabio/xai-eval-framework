# 7. LIME Configuration for Experiment 1

Date: 2025-12-18
Status: Accepted

## Context
We are evaluating XAI methods on the UCI Adult dataset using Random Forest and XGBoost models (trained in EXP1-08/09). We need to standardize LIME hyperparameters to ensure fair and reproducible comparisons for the benchmarking of stability and fidelity metrics. The LIME library version >0.2.0.1 is used.

## Decision
We will use the following LIME configuration for the `LimeTabularExplainer`:

*   **num_features**: `10`
    *   Top features to include in the generic explanation output. Matches common XAI usage patterns.
*   **num_samples**: `5000`
    *   Number of perturbed samples used to train the local surrogate linear model. Tuned in EXP1-31 to maximize stability (Stability: 0.99).
*   **kernel_width**: `None`
    *   We let LIME auto-calculate this (defaults to `sqrt(num_features) * 0.75`). Tuned in EXP1-31, finding that fixed widths (0.25-2.0) yielded poor fidelity (<0.3) for this dataset, while auto-width achieved R2 > 0.6.
*   **feature_selection**: `"auto"`
    *   [NEW] Explicitly enabled. Tuned in EXP1-31, showing slightly better Fidelity and Stability than "none".
*   **discretize_continuous**: `False`
    *   We choose NOT to discretize. The Adult dataset has continuous features like `age`, `capital-gain`. Discretization introduces binning artifacts that can obscure the true decision boundary of the complex model (RF/XGB). We prefer the local linear approximation on the continuous values.
*   **mode**: `"classification"`
    *   Explicitly set for binary target.
*   **random_state**: `42`
    *   Fixed seed for reproducibility of perturbations.

## Consequences
*   **Performance**: Generating explanations with 5000 perturbations takes approximately 3-5 seconds per instance on standard CPU. This is acceptable for our evaluation scale (<1000 test instances).
*   **Precision**: By disabling discretization, we get more precise coefficients but potentially less human-readable "rules" (e.g., "Age * 0.05" vs "Age > 50"). Since our primary goal is algorithmic evaluation (fidelity/stability), precision is preferred.
*   **Storage**: We will standardize outputs to dense arrays, ensuring consistent shapes regardless of how many features LIME selects locally.

## References
*   Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier.
*   LIME Documentation: https://lime-ml.readthedocs.io/
