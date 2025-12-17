# Models Module (`src.models`)

This module contains the model training and management logic for the XAI Evaluation Framework. It currently supports tabular data experiments (Experiment 1: Adult Dataset).

## Available Trainers

| Trainer Class | Source File | Experiment | Description |
| :--- | :--- | :--- | :--- |
| `AdultRandomForestTrainer` | `tabular_models.py` | EXP1-08 | Baseline Bagging model (Interpretable baseline). |
| `XGBoostTrainer` | `xgboost_trainer.py` | EXP1-09 | Baseline Boosting model (High-performance non-linear baseline). |

## Common Interface Pattern

All trainers follow a consistent object-oriented interface to ensure interchangeable usage in experiments:

- **`__init__(config: dict)`**: Initialize with hyperparameters.
- **`train(X_train, y_train, X_val, y_val)`**: Fit model (supports early stopping).
- **`evaluate(X_test, y_test)`**: Return dict of metrics (Accuracy, F1, ROC-AUC, etc.).
- **`save(path: Path)`**: Persist model and metadata to disk.
- **`load(path: Path)`**: Class method to restore a trained instance.
- **`predict(X)` / `predict_proba(X)`**: Inference methods.
- **`get_feature_importance()`**: Return standardized feature importance DataFrame.

## Usage Examples

### Random Forest
```python
from src.models.tabular_models import AdultRandomForestTrainer
from src.data_loading.adult import load_adult

X_train, X_test, y_train, y_test = load_adult()

trainer = AdultRandomForestTrainer({'n_estimators': 100})
trainer.train(X_train, y_train)
metrics = trainer.evaluate(X_test, y_test)
trainer.save("models/rf")
```

### XGBoost
```python
from src.models.xgboost_trainer import XGBoostTrainer

# Supports validation data for early stopping
trainer = XGBoostTrainer({'learning_rate': 0.1})
trainer.train(X_train, y_train, X_val=X_test, y_val=y_test)
trainer.save("models/xgb")
```

## Configuration

Models are configured via dictionaries or YAML files found in `experiments/exp1_adult/configs/`.

| Key | Description |
| :--- | :--- |
| `n_estimators` | Number of trees (default: 100). |
| `max_depth` | Tree depth (RF default: None, XGB default: 6). |
| `random_state` | Seed for reproducibility (fixed to 42). |
| `n_jobs` | Parallelization (-1 uses all cores). |

Ref: `docs/config_schema.md` (planned) and ADRs in `docs/decisions/`.

## Output Artifacts

Calling `save()` creates a directory containing:
1.  **Model Binary**: `*_model.pkl` (Joblib serialised).
2.  **Metadata**: `*_model_metadata.json` (Config, timestamp, versions).
3.  **Metrics**: `*_metrics.json` (Test set performance).
4.  **Feature Importance**: `*_feature_importance.csv` (Ranked features).

## Integration (Adding New Trainers)

To add a new model (e.g., SVM, Neural Net):
1.  Create a new module in `src/models/`.
2.  Implement a class with the **Common Interface Pattern** methods above.
3.  Use `joblib` for persistence.
4.  Ensure `get_feature_importance` returns a consistent DataFrame format (`feature`, `importance`, `rank`).
5.  Add unit tests in `tests/`.
