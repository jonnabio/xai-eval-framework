# Experiment 1: Adult Dataset MVP

This experiment establishes the baseline for the XAI Evaluation Framework using the UCI Adult (Census Income) dataset.

## Components
1.  **Dataset**: UCI Adult (Classification: `<=50K` vs `>50K`).
2.  **Models**: 
    - Random Forest (Bagging baseline).
    - XGBoost (Boosting baseline).
3.  **Metrics**: Accuracy, ROC-AUC, F1-Score (Weighted).

## 🚀 Quick Start: Training Models

We provide a **Master Training Runner** to train all models with consistent data splits.

### 1. Default Run (Train Everything)
Trains both Random Forest and XGBoost using default hyperparameters.
```bash
python experiments/exp1_adult/run_train_models.py
```
*Outputs artifacts to `models/` and results to `results/`.*

### 2. Custom Run
Train only XGBoost with verbose logging:
```bash
python experiments/exp1_adult/run_train_models.py --models xgboost --verbose
```

Simulate a run (validate config/data) without training:
```bash
python experiments/exp1_adult/run_train_models.py --dry-run
```

Use a specific configuration file:
```bash
python experiments/exp1_adult/run_train_models.py --config my_custom_config.yaml
```

## Directory Structure
```
experiments/exp1_adult/
├── config/
│   └── training_config.yaml   # Source of truth for hyperparameters
├── models/                    # Saved model artifacts (.pkl)
├── results/                   # Metric logs (.csv, .parquet)
├── logs/                      # Execution logs
├── run_train_models.py        # Orchestration script
└── train_*.py                 # (Legacy) individual scripts
```

## Configuration
Hyperparameters are properly managed in `config/training_config.yaml`. 
Refer to [ADR-005](../../docs/decisions/0005-training-runner-design.md) for design decisions.

## Model Validation

After training models, you should run the sanity check suite to ensure they are valid for XAI evaluation:

### Quick Validation
```bash
# Checks baseline performance and interfaces (fast)
pytest tests/unit/test_model_sanity.py -v -m "not slow"
```

### Full Validation
```bash
# Checks deep reproducibility (re-trains models multiple times)
pytest tests/unit/test_model_sanity.py -v
```

### Validation Criteria
| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| **Accuracy** | > 0.80 | Beats majority class baseline (~0.76). |
| **ROC-AUC** | > 0.85 | Ensure strong class separation. |
| **F1 Score** | > 0.60 | Balance recall/precision on imbalanced data. |

If validation fails, check [ADR-006](../../docs/decisions/0006-model-testing-strategy.md) for debugging tips.
