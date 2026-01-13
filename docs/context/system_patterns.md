# System Patterns & Standards

**Scope**: XAI Evaluation Framework (`xai-eval-framework`)
**Status**: Active

## Architectural Patterns
1.  **Experiment Runner Pattern**:
    - Experiments are defined in `configs/experiments/`.
    - They are executed by `src/experiment/runner.py`.
    - Results are strictly saved to `outputs/experiments/`.

2.  **Data Loading**:
    - All data access must go through `src/data/loader.py`.
    - Local caching is enforced to prevent re-downloading.

3.  **Metrics Design**:
    - Metrics must implement the `BaseMetric` interface.
    - Metrics are computed *post-prediction* or *post-explanation*.

## Coding Standards
- **Configuration**: Use YAML for experiment configs. Use Pydantic for validation.
- **Type Hinting**: Required for all public methods.
- **Docstrings**: Google Style required.

## Anti-Patterns
- ❌ Hardcoding paths (use `config.py` constants).
- ❌ modifying raw data in place (always work on copies).
