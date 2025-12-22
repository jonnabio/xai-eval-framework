# Experiment Report: Adult Dataset Baseline (EXP1)

## 1. Metadata
- **Date**: 2025-12-20
- **Experiment ID**: EXP1-Adult
- **Status**: Success

## 2. Hypothesis & Objective
- **Objective**: Establish baseline performance and XAI metric benchmarks for Random Forest and XGBoost using SHAP and LIME.
- **Hypothesis**: SHAP will demonstrate higher stability due to its exact game-theoretic properties, while LIME will be computationally cheaper and sparser.

## 3. Experimental Setup
- **Dataset**: UCI Adult Income (Binary Classification).
- **Models**: 
  - Random Forest (`n_estimators=100`)
  - XGBoost (Default parameters)
- **XAI Methods**: 
  - `TreeSHAP` (Interventional background)
  - `LIME` (Tabular, Discretized)
- **Metrics**: Fidelity (R2), Stability (Lipschitz/Noise), Sparsity (Zero-weights), Cost (Time).

## 4. Results

| Method | Stability | Sparsity (Zero-Ratio) | Cost (Time/Expl) | Fidelity (R2) |
| :--- | :--- | :--- | :--- | :--- |
| **RF + SHAP** | **0.95 ± 0.06** | 0.50 ± 0.03 | High (~1.9s) | -7.93 |
| **XGB + LIME** | 0.24 ± 0.14 | **0.09 ± 0.00** | **Low (~0.08s)** | -12.12 |

## 5. Analysis
- **Stability Dominance**: SHAP is significantly more stable (0.95) than LIME (0.24). LIME's reliance on random sampling in the local neighborhood leads to high variance in explanations for the same instance.
- **Sparsity Trade-off**: LIME produces much sparser explanations (only using ~9% of features), making it potentially more readable for end-users compared to SHAP, which distributes credit across ~50% of features.
- **Metric Validity**: The negative Fidelity (R2) scores for both methods suggest that the linear approximation metric is ill-suited for the complex, non-linear decision boundaries of these models on this dataset. A "Faithfulness" metric based on feature masking may be a better alternative.

## 6. Anomalies & Deviations
- **RF Model Persistence**: The `run_train_models.py` script initially failed to save the Random Forest model due to a configuration structure mismatch in `AdultRandomForestTrainer`. This was resolved by patching the runner and enforcing a manual save in `scripts/fix_rf_model.py`.
- **SHAP Configuration**: The `feature_perturbation` parameter is not supported by the `SHAPTabularWrapper` (which infers it from the explainer type), causing a crash. This parameter was removed from the experiment config.

## 7. Conclusion & Next Steps
- **Conclusion**: SHAP is the preferred method for robust, consistent explanations, while LIME is viable only when extreme sparsity or low latency is required. The Fidelity metric definition needs refinement.
- **Next Steps**: 
    1. Proceed to LLM-based evaluation (Experiment 2).
    2. Refine the Fidelity metric implementation.
