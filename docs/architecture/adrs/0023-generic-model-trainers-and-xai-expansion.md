# ADR 0023: Generic Model Trainers and XAI Breadth Expansion

**Date**: 2026-01-13
**Status**: Proposed

## Context
The current framework (`src/models/tabular_models.py`) is heavily coupled to Random Forest (`AdultRandomForestTrainer`). To fulfill the thesis objective of a "comparative evaluation framework," we need to support a diverse set of models (SVM, MLP, Logistic Regression) and explanation methods (Anchors, DiCE).
Adding these into the existing structure would lead to code duplication and lack of polymorphism, making the experiment runner brittle.

## Decision
We will refactor the model training and XAI layers to use a **Factory Pattern** and **Abstract Base Classes**.

### 1. Model Architecture
- **Refactor**: Split `tabular_models.py` into `src/models/trainers.py`.
- **Base Class**: Create `BaseTrainer(ABC)` that defines the contract:
    - `train(...)`
    - `predict(...)`
    - `save(...)`
    - `evaluate(...)`
- **Implementations**:
    - `RandomForestTrainer` (migrated)
    - `XGBoostTrainer`
    - `SVMTrainer` (New: `sklearn.svm.SVC` with `probability=True`)
    - `MLPTrainer` (New: `sklearn.neural_network.MLPClassifier`)
    - `LogisticRegressionTrainer` (New: `sklearn.linear_model.LogisticRegression`)
- **Factory**: `ModelTrainerFactory.get_trainer(config)` to instantiate the correct class based on config string.

### 2. XAI Architecture
- **Dependency Expansion**: Add `alibi` and `dice-ml` to `environment.yml`.
- **Wrappers**:
    - `AnchorsTabularWrapper` (New): Adapts `alibi` to our `ExplainerWrapper` interface.
    - `DiCETabularWrapper` (Update): Refactor to inherit from `ExplainerWrapper` and genericize input handling.

### 3. Experiment Configuration
- Experiment configs will use a `model_type` field (e.g., "svm", "mlp") that the `BatchExperimentRunner` uses to request a trainer from the factory.

## Consequences
### Positive
- **Extensibility**: Adding a 6th model (e.g., LightGBM) becomes trivial (add class + register in factory).
- **Polymorphism**: `ExperimentRunner` code becomes cleaner, not needing `if model == 'rf': ...`.
- **Breadth**: Enable the 24-experiment matrix required for the thesis results.

### Negative
- **Environment Size**: `tensorflow` (dependency of DiCE/Alibi) is large (~500MB+), slowing down CI/CD and deployment.
- **Complexity**: Introduction of `Abstract Base Classes` requires stricter typing and interface compliance.

## Mitigation
- We will try to use the `sklearn` backend for DiCE where possible to avoid heavy TensorFlow usage at runtime, though installation is still required.
- We will deprecate `train_random_forest_adult` but keep it as a wrapper calling `RandomForestTrainer` temporarily to avoid breaking legacy scripts.
