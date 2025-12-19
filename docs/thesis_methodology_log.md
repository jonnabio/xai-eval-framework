# Thesis Methodology Log

This document tracks the evolution of the experimental methodology for the PhD thesis, recording key decisions, implementations, and validations.

## Experiment 1: Adult Dataset (Tabular Binary Classification)

**Objective**: Evaluation of XAI methods (SHAP, LIME) on a standard tabular dataset to establish a baseline for the evaluation framework.

### 1. Data Pipeline
- **Dataset**: UCI Adult Income dataset.
- **Preprocessing**: 
    - Imputation: Mode/Median.
    - Encoding: One-Hot for categorical, StandardScaler for numerical.
    - Split: 80/20 train/test.
- **Validation**: Strict schema checks and determinism (fixed seeds).

### 2. Models
- **Algorithms**: Random Forest (RF) and XGBoost.
- **Configuration**: Standardized hyperparameters (e.g., n_estimators=100) via YAML configs.
- **Performance**: Validated baseline accuracy (>80%) and ROC-AUC (>0.85).

### 3. XAI Generation
- **Methods**:
    - **SHAP**: `TreeExplainer` for efficiency and path-dependent feature perturbation.
    - **LIME**: `LimeTabularExplainer` with discretized continuous features.
- **Wrapper Abstraction**: Unifying interface returning normalized feature importance weights and textual top-k features.

### 4. Evaluation Framework
- **Sampling Strategy**: Stratified sampling by error quadrant (TP, TN, FP, FN) to capture diverse model behaviors.
- **Metrics**:
    - **Fidelity**: R2 score of the linear explanation against the model prediction locally.
    - **Stability**: Cosine similarity of explanations under Gaussian noise perturbation (std=0.1).
    - **Sparsity**: Percentage of zero-weighted features (Gini/Entropy alternatives considered but simple sparsity chosen for MVP).
    - **Cost**: Computational time per explanation.

### 5. LLM Evaluation
- **Hypothesis**: LLMs can serve as proxy evaluators for "human-centered" metrics like Intuitiveness and Clarity.
- **Setup**:
    - **Prompting**: Jinja2 templated prompts providing context, true label, prediction, and top-k features.
    - **Scoring**: 1-5 Likert scale for Intuitiveness and Clarity.
    - **Models**: OpenAI GPT-4 and Google Gemini Pro as evaluators.
- **Infrastructure**: Robust client wrappers with error handling and cost tracking.

### 6. Orchestration
- **Reproducibility**: `ExperimentRunner` class manages the full lifecycle (setup -> sample -> generate -> measure -> save).
- **Configuration**: Pydantic-validated YAML configs ensure strict adherence to experimental parameters.
