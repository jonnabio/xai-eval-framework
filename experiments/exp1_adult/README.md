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
