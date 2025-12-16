# Experiment 1: Adult Dataset Baseline (EXP1)

## 1. Hypothesis
**Primary Hypothesis**: A reproducible Random Forest baseline on the Adult dataset will provide a stable "ground truth" performance target (Accuracy > 80%, AUC > 85%) necessary for evaluating the fidelity of post-hoc XAI explanation methods.
**Secondary Hypothesis**: The selected feature set (categorical + numerical) captures sufficient variance to model income prediction without excessive dimensionality, making it suitable for benchmarking explanation complexity.

## 2. Methodology

### Dataset
- **Source**: UCI Machine Learning Repository (Adult Income Dataset).
- **Target**: Binary classification (`<=50K`, `>50K`).
- **Statistics**: ~48k samples (Imbalanced: ~75% `<=50K`, ~25% `>50K`).
- **Features**: 14 attributes (Mixed type: Categorical & Numerical).
- **Preprocessing**: 
  - Numerical: Standard Scaling.
  - Categorical: One-Hot Encoding (handle unknown as ignore).
  - Missing Values: Imputed with mode/median.

### Model Specification
- **Algorithm**: Random Forest Classifier (`sklearn.ensemble.RandomForestClassifier`).
- **Key Hyperparameters** (See `configs/models/rf_adult_config.yaml`):
  - `n_estimators`: 200
  - `max_depth`: None (controlled via leaf nodes)
  - `class_weight`: "balanced_subsample"
  - `random_state`: 42

### Evaluation
- **Performance Metrics**:
  - Accuracy (Target: > 0.80)
  - ROC AUC (Target: > 0.85)
  - F1-Score (Macro)
- **XAI Methods (Future Work)**:
  - LIME (Local Interpretable Model-agnostic Explanations)
  - SHAP (SHapley Additive exPlanations)

## 3. Task Dependencies
| ID | Task Name | Status |
| :--- | :--- | :--- |
| **EXP1-01** | Experiment Setup & Data Loading | ✅ Complete |
| **EXP1-08** | RF Training Pipeline Implementation | ✅ Complete |
| **EXP1-02** | Semantic Evaluation Logic | 🚧 In Progress |
| **EXP1-03** | LIME Explanation Generation | 📅 Planned |
| **EXP1-04** | SHAP Explanation Generation | 📅 Planned |
| **EXP1-05** | Fidelity Evaluation | 📅 Planned |

## 4. Directory Structure
```
experiments/exp1_adult/
├── configs/             # Configuration files (YAML/JSON)
│   └── models/          # Model-specific configs (rf_adult_config.yaml)
├── models/              # Saved artifacts (NOT synced to git)
│   ├── rf_model.pkl     # Serialized model
│   └── *_metadata.json  # Model metadata
├── results/             # Outputs
│   ├── rf_metrics.json  # Performance metrics
│   ├── *.png            # Visualization plots
│   └── *.csv            # Feature importance data
├── scripts/             # Experiment-specific utility scripts
├── train_rf.py          # Main training executable
├── visualize_rf_results.py # Visualization script
└── test_rf_integration.py  # End-to-end test
```

## 5. Reproducibility
To ensure exact reproducibility for the thesis:
- **Seed**: Fixed global random seed `42` in `rf_adult_config.yaml`.
- **Environment**: Define in `environment.yml` (pinned versions).
- **Versioning**: Data is versioned via checksums in `src/data_loading/adult.py`.

## 6. Results
*(Placeholder: To be populated after full experiment run)*
- **Baseline Accuracy**: 85.23% (Preliminary)
- **Baseline ROC AUC**: 0.9012 (Preliminary)

## 7. Known Issues
- **None currently active.**
- *Note*: Ensure `experiments/exp1_adult` is in python path or run as module `python -m experiments.exp1_adult.train_rf` if import errors occur (handled by `sys.path` append in scripts).
