# 9. Evaluation Framework Strategy

Date: 2025-12-18
Status: Accepted

## Context
To rigorously pinpoint the strengths and weaknesses of XAI methods (LIME, SHAP) on our tabular dataset (Adult), we need a standardized evaluation framework. This requires two components:
1.  **Data**: A representative subset of instances to explain. Generating explanations for the full test set (thousands of samples) is computationally prohibitive for methods like LIME and KernelSHAP, especially when calculating stability (which requires repeated runs).
2.  **Metrics**: Clear, mathematical definitions of quality attributes (Fidelity, Stability, Sparsity, Cost).

## Decision

### 1. Sampling Strategy
We will create a standard **Evaluation Dataset** (`eval_instances.csv`) derived from the test set of our best-performing model (XGBoost).
*   **Method**: Stratified Sampling by Error Quadrant.
*   **Strata**:
    *   **True Positives (TP)**: Correctly predicted positive class.
    *   **True Negatives (TN)**: Correctly predicted negative class.
    *   **False Positives (FP)**: Incorrectly predicted as positive (Type I error).
    *   **False Negatives (FN)**: Incorrectly predicted as negative (Type II error).
*   **Size**: 50 instances per quadrant (Total ~200 instances). If a quadrant has fewer than 50, we include all of them.
*   **Rationale**: Evaluating only on correct predictions ignores how XAI helps debug errors. Evaluating only on random samples might miss rare error cases (like FP/FN in imbalanced datasets).

### 2. Metrics Architecture
We will implement a `src/metrics/` module with a consistent `BaseMetric` interface.

#### A. Fidelity (Faithfulness)
*   **Definition**: How well the explanation model (linear proxy) mimics the black-box model locally.
*   **Calculation**:
    1.  Generate $N=5000$ perturbed samples around the instance $x$ (weighted by kernel).
    2.  Get black-box predictions $f(z)$ and explanation predictions $g(z)$.
    3.  Compute $R^2$ score (Coefficient of Determination) or MAE.
*   **Target**: $R^2 > 0.9$ is considered high fidelity.

#### B. Stability (Robustness)
*   **Definition**: How much the explanation changes when the input/sampling is slightly perturbed.
*   **Calculation**:
    1.  Generate explanation $E_1$ for $x$.
    2.  Repeat generation $k=10$ times (standard LIME/SHAP with different seeds or slight input noise).
    3.  Compute average pairwise **Cosine Similarity** between feature importance vectors.
*   **Target**: Cosine Similarity > 0.9.

#### C. Sparsity (Complexity)
*   **Definition**: The conciseness of the explanation.
*   **Calculation**:
    1.  **Non-zero %**: Proportion of features with $|weight| > \epsilon$.
    2.  **Effective Complexity**: Number of top features needed to account for 90% of total absolute importance.

#### D. Cost (Efficiency)
*   **Definition**: Computational burden.
*   **Calculation**:
    1.  **Wall-clock time** (ms) per instance.
    2.  (Optional) Estimated Energy Usage proxy based on FLOPs/Time.

## Consequences
*   **Standardization**: All future experiments (e.g., adding a new explainer) will use the exact same `eval_instances.csv` and metric implementations, ensuring 100% comparability.
*   **Compute Load**: Stability metrics require re-running explanations multiple times, multiplying compute cost. The sampling strategy (limiting to ~200 instances) keeps this feasible.
*   **Bias**: The evaluation set is biased towards "hard" cases (errors make up ~50% of the set vs <20% in real distribution). This is intentional for XAI debugging utility.

## References
*   *Evaluation of LIME and SHAP* (standard literature approach for stratified sampling).
*   *Quantifying the Stability of Interpretable Explanations* (Alvarez-Melis et al.).
