# Experiment 1: Adult Dataset MVP

This experiment establishes the baseline for the XAI Evaluation Framework using the UCI Adult (Census Income) dataset.

## Components
1.  **Dataset**: UCI Adult (Classification: `<=50K` vs `>50K`).
2.  **Models**: 
    - Random Forest (Bagging baseline).
    - XGBoost (Boosting baseline).
3.  **Metrics**: Accuracy, ROC-AUC, F1-Score (Weighted).

## 🚀 Quick Start: Training Models

We provide a **Master Training Runner** to train models and a **Batch Experiment Runner** for parallel evaluation.

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
│   └── training_config.yaml   # Source of truth for training hyperparameters
├── models/                    # Saved model artifacts (.pkl, .joblib)
├── results/                   # Metric logs (.csv, .parquet, .json)
├── logs/                      # Execution logs
├── run_train_models.py        # Model training orchestration script
└── train_*.py                 # (Legacy) individual scripts
```

## 🚀 Usage Guide

### 1. Training Models
Train Random Forest and XGBoost base models:
```bash
python experiments/exp1_adult/run_train_models.py
```
This requires `config/training_config.yaml`.

### 2. Running XAI Experiments
Run a full evaluation pipeline (data load -> generate explanations -> compute metrics):
```bash
# Example: Random Forest + SHAP
python scripts/run_experiment.py --config configs/experiments/exp1_adult_rf_shap.yaml

# Example: XGBoost + LIME
python scripts/run_experiment.py --config configs/experiments/exp1_adult_xgb_lime.yaml
```
Output: `results.json` and `metrics.csv` in the specified output directory.

### 3. Running LLM Evaluation
Evaluate the quality of generated explanations using GPT-4 or Gemini:
```bash
python scripts/run_llm_eval.py \
    --input_dir experiments/exp1_adult/results/rf_shap \
    --provider openai \
    --model gpt-4
```
Output: `llm_eval.json` in the input directory.

### 4. Running Batch Verification (Parallel)
Run the full XAI evaluation suite across all models and explainers in parallel:
```bash
python scripts/run_batch_experiments.py --config-dir configs/experiments --output outputs/final_results.csv --parallel
```
This enables large-scale metric collection (Fidelity, Stability, Domain Alignment).
**See Full Report**: [EVALUATION_REPORT.md](EVALUATION_REPORT.md)

## XAI Explanation Generation

### LIME Explanations

Generate LIME explanations for trained models:

```bash
# Example: Generate explanations for test instances
python examples/example_lime_usage.py
```

**What LIME Does:**
- Trains local linear models on perturbed samples
- Identifies which features most influence individual predictions
- Provides both positive (increases prediction) and negative (decreases prediction) importance values

**Configuration:**
- **num_features**: 10 (top features to include in explanation)
- **num_samples**: 5000 (perturbed samples for local model)
- **kernel_width**: Auto-calculated (controls locality)
- **random_state**: 42 (reproducibility)

See `docs/decisions/0007-lime-configuration.md` for configuration rationale.

**Output Format:**
```python
explanations = {
    'feature_importance': np.ndarray,  # (n_instances, 108) - all features
    'top_features': np.ndarray,        # (n_instances, 10) - top feature indices
    'metadata': {
        'total_time_seconds': 15.3,
        'avg_time_per_instance': 3.06,
        'num_features_requested': 10,
        'num_samples': 5000,
        ...
    }
}
```

## Configuration

### Environment Variables
To use LLM evaluation features, set the following environment variables (e.g., in a `.env` file):

```bash
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
```

### Dataset
The Adult dataset will be automatically downloaded and cached in `data/`.
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

### SHAP Explanations

Generate SHAP values using `TreeExplainer` (exact for trees) or `KernelExplainer`:

```bash
# Example: Generate SHAP explanations
python examples/example_shap_usage.py
```

**Configuration:**
- **model_type**: "tree" (default) or "kernel".
- **n_background_samples**: 100 (summary size).
- **random_state**: 42.

See `docs/decisions/0008-shap-configuration.md`.

**Output Format:**
Same as LIME (`feature_importance` dense array, `top_features`, `metadata`).

## Evaluation Framework

We use a standardized framework to evaluate XAI equality:

1.  **Instances**: 200 stratified samples (TP, TN, FP, FN) generated via `scripts/generate_eval_instances.py`.
2.  **Metrics**:
    - **Fidelity**: $R^2$ of explanation vs black-box.
    - **Stability**: Cosine similarity under perturbation.
    - **Sparsity**: \% Non-zero features.
    - **Cost**: Computation time.

See `docs/decisions/0009-evaluation-strategy.md` for details.

## Contributing
