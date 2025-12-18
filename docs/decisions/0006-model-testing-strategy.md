# 6. Model Testing Strategy

Date: 2025-12-17
Status: Accepted

## Context
Experiment 1 involves training Random Forest and XGBoost models on the Adult dataset. These models serve as the foundation for the subsequent XAI evaluation (LIME, SHAP).
Currently, we have integration tests (`test_training_runner.py`) that verify the *process* of training, but we lack rigorous "sanity checks" for the *artifacts* themselves.
XAI methods can be computationally expensive and sensitive to model behavior. If a model is degenerate (e.g., predicting all zeros, or outputting invalid probabilities), debugging the XAI method becomes impossible.
We need a strategy to ensure models are valid, performant, and reproducible before they enter the evaluation pipeline.

## Decision
We will implement a dedicated **Model Sanity Test Suite** (`tests/unit/test_model_sanity.py`) that acts as a quality gate for trained model artifacts.

### 1. Scope of Tests
The suite will cover:
- **Integrity**: Verify models can be saved and loaded (pickled) without state loss.
- **Sanity**: Verify predictions have correct shapes `(N,)` and probabilities are valid `[0, 1]`.
- **Performance**: Verify models exceed minimal baselines to be useful for XAI:
    - **Accuracy**: > 0.80 (Adult baseline is ~0.76).
    - **ROC-AUC**: > 0.85 (Strong separation).
- **Reproducibility**: Verify that fixing `random_state` yields deterministic predictions and feature importances.

### 2. Test Isolation Strategy
To ensure speed and independence:
- **Module-Scoped Fixtures**: Training happens *once* per test module using a small but representative subset of data.
- **Temporary Directories**: All save/load tests use `tmp_path` to avoid cluttering the workspace.
- **Fixed Seeds**: All tests use `random_state=42`.

## Consequences
### Positive
- **Confidence**: We can trust the models used for LIME/SHAP are correct.
- **Debugging**: Failures in XAI pipelines can be ruled out as "bad models" quickly.
- **Documentation**: acts as executable documentation of what a "valid" model looks like.

### Negative
- **Maintenance**: Thresholds (0.80/0.85) may need adjustment if data preprocessing changes significantly.
- **Runtime**: Reproducibility tests requiring fresh training are slower; they will be marked with `@pytest.mark.slow`.
