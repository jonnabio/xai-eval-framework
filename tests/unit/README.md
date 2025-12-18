# Unit Tests

This directory contains pure unit tests and sanity checks for the XAI Evaluation Framework. Unlike integration tests (which live in `experiments/`), these tests verify logic, interfaces, and baseline behaviors in isolation.

## Test Modules

| Module | Purpose | EXP1 Tasks |
|--------|---------|------------|
| `test_model_sanity.py` | verifies RF/XGBoost models (Save/Load, Performance, Sanity) | EXP1-08, 09, 10, 11 |
| `../test_adult_loader.py` | (Legacy ref) verifies data loading logic | EXP1-07 |

*Note: Some legacy tests still sit in the parent `tests/` directory and will be migrated here eventually.*

## `test_model_sanity.py` Detail

This suite acts as the quality gate for any model trained in Experiment 1.

| Class | Purpose | Key Checks |
|-------|---------|------------|
| `TestModelLoading` | Persistence | Files > 1KB, load() works, restored predictions match original. |
| `TestModelPredictions` | Validity | Probabilities in [0,1], rows sum to 1, valid shapes (N,). |
| `TestModelPerformance` | Quality | Accuracy > 0.80, ROC-AUC > 0.85 (Baseline verification). |
| `TestModelReproducibility` | Determinism | Fixed seeds yield identical models; different seeds yield differences. |
| `TestBothModels` | Interface | Parametrized check that both RF/XGB expose standard API (`train`, `predict`, `save`). |

## Usage

Run all unit tests:
```bash
pytest tests/unit/ -v
```

Run only fast tests (skipping reproducibility checks):
```bash
pytest tests/unit/ -v -m "not slow"
```

Run with coverage:
```bash
pytest --cov=src.models tests/unit/
```

## Thresholds
Defined in `test_model_sanity.py` constants:
- **Accuracy**: > 0.80
- **ROC-AUC**: > 0.85
- **F1**: > 0.60

Refer to [ADR-006](../../docs/decisions/0006-model-testing-strategy.md) for rationale.
