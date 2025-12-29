# Experiment module

This module handles the orchestration of XAI evaluation experiments.

## Architecture

The system follows a configuration-driven architecture defined in [ADR-010](../../docs/decisions/0010-experiment-runner-architecture.md).

### Components

1.  **Configuration (`config.py`)**: Pydantic models defining the experiment schema.
2.  **Runner (`runner.py`)**: Core class `ExperimentRunner` that orchestrates:
    - Data loading
    - Model loading
    - Explainer initialization
    - Sampling of evaluation instances
    - Execution of explanation + metrics
    - Result aggregation and saving

### Usage

Config objects are typically loaded from YAML files via `config.load_config(path)`.

```python
from src.experiment.config import load_config
from src.experiment.runner import ExperimentRunner

# Load config
config = load_config("configs/experiments/my_experiment.yaml")

# Run
runner = ExperimentRunner(config)
results = runner.run()
```

## Configuration Schema

### Batch Execution (`batch_runner.py`)
Orchestrator for executing multiple experiments in parallel.
- **Features**: Parallel execution (ProcessPoolExecutor), Checkpointing (skips existing results), Result Aggregation.
- **Class**: `BatchExperimentRunner`.
- **Usage**:
    ```python
    from src.experiment.batch_runner import BatchExperimentRunner
    runner = BatchExperimentRunner(config_paths)
    df, manifest = runner.run(parallel=True)
    ```

See `src/experiment/config.py` for the full schema. Key sections:
- `model`: Path to saved joblib model.
- `explainer`: 'shap' or 'lime' with parameters.
- `sampling`: Evaluation instance selection strategy.
- `metrics`: Toggles for fidelity, stability, sparsity, cost.
