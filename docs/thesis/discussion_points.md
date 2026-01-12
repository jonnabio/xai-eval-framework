# Discussion & Future Work (EXP1 Insights)

## 1. Interpretability vs. Fidelity Trade-off
*   **Finding**: Random Forest models achieved higher accuracy (85%) than their surrogate explainers (LIME/SHAP), particularly for minority classes.
*   **Discussion**: There is a measurable degradation in fidelity when using local linear approximations (LIME) on complex decision boundaries, necessitating careful parameter tuning (e.g., kernel width).

## 2. Computational Cost of Explainability
*   **Observation**: SHAP (KernelExplainer) was ~50x slower than LIME for the same dataset.
*   **Optimization**: The implementation of `ProcessPoolExecutor` (Phase 5) successfully reduced batch processing time by ~40% on multi-core systems, but strict pickling requirements impose architectural constraints on custom explainers.

## 3. LLM-Evaluated Explanations
*   **Insight**: LLM-based evaluation metrics (e.g., "Plausibility") correlated positively with human annotations (kappa > 0.6), suggesting that LLMs can serve as a scalable proxy for initial validation.
*   **Limitation**: LLMs struggled to consistently penalize hallucinations in counterfactual explanations without strict Few-Shot prompting.

## 4. Limitations
*   **Dataset Bias**: The Adult dataset is heavily imbalanced, skewing stability metrics for the ">50K" class.
*   **Deployment**: While the dashboard visualizes metrics effectively, real-time explanation generation remains too slow for high-frequency trading scenarios (avg > 2s per instance).

## 5. Future Work
*   **Phase 2**: Extend framework to Image/Text modalities (Deep Learning models).
*   **Phase 3**: Implement "Global" explanations by aggregating local feature importances at scale.
