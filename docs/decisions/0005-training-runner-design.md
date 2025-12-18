# 5. Training Runner Design

Date: 2025-12-16
Status: Accepted

## Context
Experiment 1 (Adult Dataset MVP) requires training two baseline models: Random Forest and XGBoost.
Currently, these are handled by separate scripts (`train_rf.py`, `train_xgb.py`) or ad-hoc separate execution.
To ensure robustness, reproducibility, and ease of use, we need a unified orchestration layer that guarantees:
- Identical data splits for both models.
- Consistent configuration usage.
- Standardized logging and metric artifacts.
- A single entry point for reproducing the "Model Training" vertical of the experiment.

## Decision
We will implement a unified **Training Runner** script (`experiments/exp1_adult/run_train_models.py`) governed by a dedicated **Configuration File** (`experiments/exp1_adult/config/training_config.yaml`).

### 1. Architecture
- **Single Orchestrator**: One script to rule them all. It allows training "all" or specific subsets of models via CLI flags.
- **Decoupled Config**: Hyperparameters and paths are moved to YAML, keeping code clean and allowing experiment variations without code changes.

### 2. Configuration Strategy
- **YAML as Source of Truth**: All default values (paths, params) live in `training_config.yaml`.
- **CLI Overrides**: `argparse` handles runtime flags like `--dry-run`, `--verbose`, or selecting specific models (`--models rf`).

### 3. Output Structure
- `models/`: Serialized model artifacts (`.pkl`).
- `results/`: Metric logs (CSV and Parquet).
- `logs/`: Application execution logs (`.log`).

### 4. Logging & Monitoring
- **Dual Logging**: 
    - Console (INFO): Concise progress bars and summary tables.
    - File (DEBUG): Detailed trace for debugging and audit.
- **Metrics Persistence**: 
    - CSV for human readability / quick checks.
    - Parquet for efficient programmatic loading in downstream tasks.

### 5. Reproducibility
- The script controls the `random_state`. 
- It loads data **once** and passes the same training/test sets to all trainers, eliminating split variance.
- Config versioning is tracked in the output metadata.

## Consequences
### Positive
- **Consistency**: Guaranteed same data for RF and XGBoost.
- **Convenience**: "One click" reproduction of the training phase.
- **Extensibility**: Easy to add a third model (e.g., SVM) by adding a config section and a few lines of code.

### Negative
- **Complexity**: The runner script is more complex than standalone "Hello World" training scripts.
- **Dependency**: Requires `training_config.yaml` to exist and be valid.
