# 0018. Statistical Validation Methodology

**Date**: 2026-01-02
**Status**: Accepted

## Context
Comparing XAI methods (e.g., LIME vs. SHAP) requires rigorous statistical testing to support claims of superiority. Evaluating on simple mean scores is insufficient for a thesis. We need a standardized statistical framework to determine if observed differences in metrics (Fidelity, Stability, Sparsity) are significant. Furthermore, with only $N=5$ observations from cross-validation, standard bootstrap methods may be unreliable.

## Decision
We adopt a two-tiered statistical validation approach:

1.  **Hypothesis Testing**:
    -   **Global Test**: **Friedman Test** to detect if any significant differences exist among multiple methods (RF+LIME, RF+SHAP, etc.).
    -   **Post-Hoc**: **Nemenyi Test** for pairwise comparisons, which controls the Family-Wise Error Rate (FWER).
    -   **Effect Size**: **Cohen's $d_z$** (paired) to quantify the magnitude of differences.

2.  **Confidence Intervals**:
    -   **Primary**: **t-Distribution CIs** ($\alpha=0.05$). Chosen because the sample size ($N=5$ folds) is small, and parametric methods offer exact coverage if fold means are normally distributed.
    -   **Secondary**: **Bootstrap BCa**. Included as a sensitivity check but with explicit warnings for $N<20$.

## Consequences
-   **Positive**: Provides strong statistical evidence for thesis claims; Nemenyi/Friedman are standard in ML comparisons (Demšar, 2006); t-CIs are robust for small samples.
-   **Negative**: Limits the "fine-grained" analysis that might be possible with instance-level large-N bootstrapping, but ensures correctness.
-   **Risks**: Assumption of normality for t-Intervals (checked via simulation).
