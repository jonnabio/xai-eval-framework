# Reproducibility Guide: Experiment 1

This document details the exact environment, data, and steps required to reproduce the baseline Random Forest results for Experiment 1 (Adult Dataset) of the PhD thesis.

## 1. Environment Setup

### Software Stack
-   **OS**: Windows 10/11 or Linux (Ubuntu 22.04 recommended)
-   **Python**: 3.11 (Explicitly pinned in `environment.yml`)
-   **Package Manager**: Conda

### Key Dependencies
Exact versions as tested (see `environment.yml` for full list):
-   `scikit-learn` (latest stable)
-   `pandas`
-   `numpy`
-   `pyyaml`

## 2. Data Preparation

### Source
-   **Dataset**: UCI Adult Income Dataset
-   **Version**: OpenML ID `1590` (Version 2)
    -   *Fallback*: Direct download from UCI Archive.
-   **Total Raw Rows**: ~48,842

### Preprocessing Pipeline
Implemented in `src.data_loading.adult`, executed in this exact order:

1.  **Cleaning**:
    -   Strip whitespace from strings.
    -   Replace `?` with `NaN`.
    -   Map target (`<=50K`, `>50K`, etc.) to binary `0` / `1`.
    -   Drop rows with missing target.
    -   Remove exact duplicates.
2.  **Splitting**:
    -   Ratio: 80% Train / 20% Test
    -   Stratification: Yes (on Target)
    -   Seed: `42`
3.  **Transformation** (`ColumnTransformer`):
    -   **Numerical** (`age`, `hours-per-week`, etc.): `StandardScaler` (Zero mean, unit variance).
    -   **Categorical** (`workclass`, `education`, etc.): `OneHotEncoder` (`handle_unknown='ignore'`, `sparse=False`).

## 3. Execution Steps

Run commands from the project root.

### Step 1: Train Model
Initializes data loader (downloads if needed), processes data, and trains the Random Forest.

```bash
python experiments/exp1_adult/train_rf.py --verbose
```
-   **Expected Runtime**: < 30 seconds (first run varies by download speed).
-   **Output**: `experiments/exp1_adult/models/rf_model.pkl`

### Step 2: Verify Results
Runs integration tests to ensure model metrics meet the thesis baseline requirements.

```bash
python experiments/exp1_adult/test_rf_integration.py
```
-   **Output**: "SUCCESS: Integration Test Passed!"

## 4. Verification

To confirm successful reproduction, check the `experiments/exp1_adult/results/rf_metrics.json` file.

### Expected Metric Ranges
| Metric | Threshold | Rationale |
| :--- | :--- | :--- |
| **Accuracy** | > 0.80 | Baseline establishes simple majority class improvement (~76%). |
| **ROC AUC** | > 0.85 | Ensures robust ranking capability for the accepted random seed. |

### Artifact Validation
-   **Model Metadata**: Check `models/rf_model_metadata.json` for `n_samples` and `n_features`.
    -   *Note*: Feature count varies slightly depending on OHE of rare categories found in training split.
