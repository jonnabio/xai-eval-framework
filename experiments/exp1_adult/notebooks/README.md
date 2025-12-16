# Experiment 1 Analysis Notebooks

This directory contains Jupyter notebooks for interactive analysis, visualization, and validation of the Random Forest baseline on the Adult dataset.

## Notebook Index

| Notebook | Status | Purpose | Inputs | Outputs | Related Task |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **[`01_eda_adult.ipynb`](01_eda_adult.ipynb)** | ✅ Complete | Exploratory Data Analysis (EDA). Analyzes class imbalance, feature distributions, and correlations. | `src.data_loading.adult.load_adult` | Class imbalance plots, Correlation matrix | **EXP1-01** |
| **[`02_sanity_checks.ipynb`](02_sanity_checks.ipynb)** | 🚧 Planned | Validation of model behavior. Checks prediction distributions and basic logic tests (e.g., monotonicity). | `models/rf_model.pkl`, Test Set | Distribution plots, Failure cases | **EXP1-08** |

## Usage
Ensure you are using the project's conda environment (`xai_eval`) to run these notebooks.

```bash
conda activate xai_eval
jupyter notebook
```

The notebooks are configured to automatically append the project root to `sys.path` to allow importing from `src`.
