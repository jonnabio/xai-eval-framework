# Experiment 1 Spec: Adult MVP v1

## 1. Dataset
- **Name**: UCI Adult Income dataset.
- **Target**: `income` > 50K (binary classification).
- **Preprocessing**:
  - **Encoding**: One-Hot Encoding (OHE) for categorical variables.
  - **Scaling**: Standard scaling for numerical features (if required by specific models).
  - **Split**: Train/Validation/Test split (e.g., 70/15/15 or 80/20).
  - **Seeds**: Fixed random seeds for reproducibility.

## 2. Models (MVP)
- **Random Forest** (Main): `scikit-learn` implementation.
- **XGBoost** (Optional): `xgboost` implementation (Gradient Boosting).

## 3. XAI Methods (MVP)
- **LIME**: `lime.lime_tabular.LimeTabularExplainer` (tabular data).
- **SHAP**:
  - `shap.TreeExplainer` (optimized for tree-based models).
  - `shap.KernelExplainer` (model-agnostic fallback if needed).
- **Global Baseline**: Permutation Feature Importance.

## 4. Metrics
- **Fidelity**: $R^2$ or MSE between the surrogate model (explanation) and the true model prediction on the local neighborhood.
- **Stability**: Cosine similarity or Kendall’s $\tau$ between explanations generated under small perturbations of the input.
- **Sparsity**: Percentage of non-zero feature importances or Top-K feature coverage.
- **Cost / EEUs (Explanation Energy Units)**:
  - Execution time.
  - Basic memory usage.
  - Custom "Explanation Energy Units" definition for this MVP.

## 5. Sample Sizes & Seeds
- **Instances to Explain**: ~200 test instances.
- **Random Seeds**: Specific seeds for train/test splitting and sampling to ensure consistent results.

## 6. Outputs
- **Tables**: Aggregated metrics per (Model, XAI Method).
- **Files**:
  - `metrics_exp1_adult_v1.parquet`: Detailed metrics storage.
  - `explanations_exp1_adult_v1.jsonl`: Serialized explanations.
- **LLM Evaluation**: Initial batch of 50 LIME + 50 SHAP explanations for semantic evaluation.
