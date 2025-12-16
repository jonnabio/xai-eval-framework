# Configuration Schema Documentation
**Reference Config**: `experiments/exp1_adult/configs/models/rf_adult_config.yaml`

This document outlines the configuration schema for Experiment 1 (Adult Dataset + Random Forest). The configuration is divided into four main sections: `model`, `training`, `output`, and `validation`.

---

## 1. Model Configuration (`model`)
Defines the architecture and hyperparameters of the Random Forest classifier.

| Parameter | Type | Default | Description & Impact |
| :--- | :--- | :--- | :--- |
| `type` | String | `"RandomForest"` | Identifier for the model architecture factory. Used to select the correct model class. |
| `params.n_estimators` | Integer | `200` | **Description**: Number of trees in the forest.<br>**Valid Range**: 100-1000<br>**Impact**: Higher values increase stability and performance but linearly increase training time. 200 is a robust baseline. |
| `params.max_depth` | Integer/Null| `null` | **Description**: Maximum depth of each tree.<br>**Valid Range**: 10-100 or `null`<br>**Impact**: Controls model complexity. `null` allows trees to grow fully (potential overfitting), usually controlled by `min_samples_leaf` instead. |
| `params.min_samples_split`| Integer | `2` | **Description**: Minimum samples required to split an internal node.<br>**Valid Range**: 2-10<br>**Impact**: Higher values act as regularization, preventing the model from learning specific noise patterns. |
| `params.min_samples_leaf` | Integer | `1` | **Description**: Minimum samples required at a leaf node.<br>**Valid Range**: 1-20<br>**Impact**: Smoothes the decision boundary. Increasing to 5-10 significantly reduces overfitting on noisy data. |
| `params.max_features` | String/Int | `"sqrt"` | **Description**: Number of features to consider for best split.<br>**Impact**: `"sqrt"` is the standard heuristic for classification problems. |
| `params.bootstrap` | Boolean | `true` | **Description**: Whether to use bootstrap samples for building trees.<br>**Impact**: Must be `true` for standard Random Forest behavior (bagging). |
| `params.n_jobs` | Integer | `-1` | **Description**: Number of parallel jobs.<br>**Impact**: `-1` uses all available cores. Affects **wall-clock time** only, not model result. |
| `params.random_state` | Integer | `42` | **Description**: Seed for random number generator.<br>**Impact**: **Critical for reproducibility**. Ensures the same trees are built every time. |
| `params.class_weight` | String | `"balanced_subsample"`| **Description**: Weighting strategy for classes.<br>**Impact**: addressing the 1:3 imbalance in Adult dataset without manual resampling. |
| `params.verbose` | Integer | `0` | **Description**: Sklearn verbosity level. |

---

## 2. Training Configuration (`training`)
Controls the data split and training process execution.

| Parameter | Type | Default | Description & Impact |
| :--- | :--- | :--- | :--- |
| `test_size` | Float | `0.2` | **Description**: Proportion of data reserved for testing.<br>**Valid Range**: 0.1-0.3<br>**Impact**: 0.2 (20%) provides ~9000 test samples for Adult, which is statistically significant for evaluation. |
| `random_state` | Integer | `42` | **Description**: Seed for the train/test split.<br>**Impact**: **Critical**. Ensures the model is trained and tested on the exact same data subsets across runs. |

---

## 3. Output Configuration (`output`)
Specifies where artifacts are stored.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `model_dir` | Path String | `"experiments/exp1_adult/models"` | Directory for saving serialized `.pkl` models. |
| `results_dir` | Path String | `"experiments/exp1_adult/results"` | Directory for saving CSVs (feature importance) and JSONs (metrics). |
| `model_filename` | String | `"rf_model.pkl"` | Filename for the trained model artifact. |
| `metrics_filename` | String | `"rf_metrics.json"` | Filename for the detailed performance metrics. |

---

## 4. Validation Configuration (`validation`)
Defines success criteria for the experiment pipeline.

| Parameter | Type | Default | Description & Impact |
| :--- | :--- | :--- | :--- |
| `min_accuracy` | Float | `0.80` | **Description**: Minimum acceptable Accuracy.<br>**Context**: Baseline for Adult is ~85%. < 80% indicates a failure. |
| `min_roc_auc` | Float | `0.85` | **Description**: Minimum acceptable ROC AUC.<br>**Context**: A robust Random Forest should achieve ~0.90 AUC. |

---

## Usage Scenarios

### Scenario A: Fast Debugging
Use this for integration tests or quick syntax checks.
```yaml
model:
  params:
    n_estimators: 10  # Reduced from 200
    n_jobs: 1         # Serial execution for easier debugging
```

### Scenario B: High Performance (Production)
Use this when training the final baseline for the thesis.
```yaml
model:
  params:
    n_estimators: 500       # Increased stability
    min_samples_leaf: 5     # Better generalization
    class_weight: "balanced" # Standard balanced instead of subsample for speed if needed
```
