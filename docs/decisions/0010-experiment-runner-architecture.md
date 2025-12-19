# 10. Experiment Runner Architecture

Date: 2025-12-19
Status: Accepted

## Context
We need an orchestration layer to execute end-to-end XAI evaluation experiments for the PhD thesis. The system must support:
- Configurable model selection (RF, XGBoost).
- Configurable XAI method selection (SHAP, LIME) with specific parameters.
- Reproducible execution (seeding, versioning).
- Standardized output for downstream analysis and dashboards.
- Progress tracking for long-running experiments.

## Decision

### 1. Configuration Schema
We will use **YAML** for defining experiments, validated by **Pydantic** models in Python.
- **Location**: `configs/experiments/`
- **Schema**:
    - `model`: Name, path.
    - `explainer`: Method (shap/lime), params.
    - `sampling`: Strategy (stratified), sample count.
    - `metrics`: Toggle flags (fidelity, stability, etc.) and params.

### 2. Orchestration Flow
We will implement a modular `ExperimentRunner` class in `src/experiment/runner.py`.
1.  **Setup**: Load config, load trained model, initialize explainer wrapper.
2.  **Sampling**: Generate evaluation instances using `EvaluationSampler`.
3.  **Execution Loop**:
    - For each instance:
        - Generate explanation.
        - Compute enabled metrics.
        - Record results.
4.  **Aggregation**: Compute mean/std for all metrics.
5.  **Persistence**: Save full JSON results and CSV summary.

### 3. Output Format
- **JSON** (`results.json`): Nested structure with metadata, model info, and per-instance details.
- **CSV** (`metrics.csv`): Flattened table for easy analysis (pandas/Excel).

### 4. CLI Interface
A CLI script `scripts/run_experiment.py` will serve as the entry point.
```bash
python scripts/run_experiment.py --config configs/experiments/exp1_adult_rf_shap.yaml
```

## Consequences
- **Positive**: High reproducibility, clear separation of concerns, easy to add new experiments without code changes.
- **Negative**: Slight overhead in maintaining Pydantic schemas, but worth it for validation safety.
