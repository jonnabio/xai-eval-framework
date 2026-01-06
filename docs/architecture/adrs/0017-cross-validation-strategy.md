# 0017. Cross-Validation Strategy

**Date**: 2026-01-02
**Status**: Accepted

## Context
Experiment 1 (EXP1) initially relied on a single 80/20 train/test split. While sufficient for initial prototyping, single-split evaluations are prone to high variance and may not accurately reflect the generalizability of XAI metrics (Stability, Fidelity, etc.). To draw robust conclusions for the thesis, we need a validation strategy that utilizes the available data more effectively and quantifies performance variability.

## Decision
We will implement **5-Fold Stratified Cross-Validation** for all subsequent experiments in EXP1.
-   **Strata**: Target variable (income class) to ensure balanced class distribution in every fold.
-   **K=5**: Chosen as a balance between computational cost (training/explaining 5 times) and statistical reliability.
-   **Architecture**: A new `CrossValidationRunner` orchestrates the process, injecting fold-specific data into the existing `ExperimentRunner`.
-   **Aggregation**: Metrics will be aggregated across folds (mean, std) to produce the final experiment result.

## Consequences
-   **Positive**: Reduced selection bias from random splitting; provides variance estimates for all metrics; aligns with standard ML evaluation practices.
-   **Negative**: Increases computational time by approximately 5x.
-   **Neutral**: Requires refactoring `ExperimentRunner` to accept pre-split data inputs.
