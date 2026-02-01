# PhD Thesis Project: Objectives and Results

## Overview
The primary goal of this thesis project is to develop and validate a comprehensive **Evaluation Framework for Explainable AI (XAI)**. The framework integrates classical quantitative metrics, novel causal-based metrics, and Large Language Model (LLM) based semantic evaluations to provide a holistic assessment of explanation quality.

The current phase (Experiment 1) focuses on a tabular binary classification task using the **Adult Income Dataset** to establish a rigorous baseline.

---

## 1. Methodology & Experimental Foundation
### Objectives
-   **Baseline Establishment**: Set up a reproducible evaluation pipeline on a standard tabular dataset (UCI Adult).
-   **Model Implementation**: Train and validate "black-box" models (Random Forest, XGBoost) with standardized metrics.
-   **XAI Generation**: Integrate standard post-hoc explanation methods (SHAP, LIME).
-   **Orchestration**: Develop a `BatchExperimentRunner` for robust, parallelized execution of experiments across diverse configurations.

### Results Obtained
-   **Pipeline**: Fully operational data pipeline with strict schema checks, imputation, and one-hot/standard scaling.
-   **Models**: 
    -   Random Forest and XGBoost models trained.
    -   Performance validated (>80% Accuracy, >0.85 ROC-AUC).
-   **XAI Integration**:
    -   **SHAP**: Implemented using `TreeExplainer`; path-dependent feature perturbation.
    -   **LIME**: Implemented using `LimeTabularExplainer`; continuous features preserved without discretization.
-   **Orchestration**: `BatchExperimentRunner` implemented with checkpointing, auto-discovery of configs, and result aggregation.

---

## 2. Quantitative Evaluation Metrics
### Objectives
 Implement a multi-faceted suite of metrics to evaluate explanations:
-   **Fidelity (Faithfulness)**: Measure how accurately the explanation reflects the model's decision process.
-   **Stability**: Assess explanation consistency under input perturbations.
-   **Sparsity**: Evaluate the conciseness of explanations.
-   **Causal Alignment**: Measure alignment with domain-specific causal knowledge.
-   **Counterfactual Sensitivity**: Quantify explanation changes under minimal prediction-flipping perturbations.

### Results Obtained
-   **Fidelity**: Implemented "Faithfulness" metric based on feature masking (replacing initial R² approach).
-   **Stability**: Implemented cosine similarity under Gaussian noise perturbation.
-   **Sparsity**: Implemented percentage of zero-weighted features.
-   **Causal Alignment**: Implemented `DomainAlignmentMetric` calculating Precision/Recall@K against defined ground-truth causal features.
-   **Counterfactual Sensitivity**: Implemented using `DiCE` to generate counterfactuals and measure explanation shifts.

---

## 3. LLM-Based Semantic Evaluation
### Objectives
-   **Semantic Proxy**: Leverage LLMs as proxy evaluators for "human-centered" metrics (Intuitiveness, Clarity) that are hard to quantify mathematically.
-   **Orchestration**: Build a robust engine to handle LLM API calls with cost tracking and rate limiting.
-   **Prompt Engineering**: Design and validate Jinja2-templated prompts for consistent evaluation.

### Results Obtained
-   **Infrastructure**: `LLMClientFactory` built supporting OpenAI (GPT-4) and Google (Gemini Pro).
-   **Templates**: 5 prompt templates designed and refined (Fidelity, Stability, Sparsity, Causal, CF).
-   **Evaluation**: 
    -   Stratified sampling strategy implemented.
    -   Batch evaluation executed on 80 stratified samples.
-   **Analysis**: Correlation analysis performed between LLM scores and classical metrics (Radar plots, heatmaps generated).

---

## 4. Human Validation
### Objectives
-   **Ground Truth**: Collect human annotations to validate the correlation/reliability of LLM-based metrics.
-   **Interface**: Develop a user-friendly interface for annotators to review explanations and provide ratings.

### Results Obtained
-   **Sampling**: 20 stratified instances selected for human review.
-   **System**: Human validation interface integrated into the dashboard (Backend + Frontend).
-   **Status**: Ready for data collection. Analysis scripts for Cohen's Kappa score are stubbed.

---

## 5. Statistical Validation & Reproducibility
### Objectives
-   **Scientific Rigor**: Assess the statistical significance of results.
-   **Reproducibility**: Verify results are robust to random seed variations.
-   **Generalization**: Use Cross-Validation to ensure stability across data splits.

### Results Obtained
-   **Reproducibility**: Multi-run study completed (4 combinations × 10 seeds). Coefficient of Variation (CV) computed.
-   **Cross-Validation**: 5-fold Stratified Cross-Validation framework implemented and executed.
-   **Significance**: 
    -   Hypothesis tests (Friedman, Wilcoxon) implemented.
    -   Bonferroni correction applied.
    -   Effect sizes (Cohen's d) computed.
-   **Confidence Intervals**: Implemented t-distribution and Bootstrap CIs for error bars.
-   **Sensitivity Analysis**: Hyperparameter sensitivity analysis completed for LIME/SHAP parameters.

---

## 6. Software Artifacts & Deployment
### Objectives
-   **Interactive Dashboard**: Create a web-based dashboard to visualize all experimental results, compare models/methods, and inspect individual instances.
-   **Production Deployment**: Deploy the full stack (Backend + Frontend) to a public cloud for accessibility.
-   **Documentation**: Produce publication-quality artifacts and reproducible code packages.

### Results Obtained
-   **Dashboard**:
    -   **Backend**: FastAPI extended to serve `AdvancedMetrics` and `LLMEvaluationScore`.
    -   **Frontend**: Next.js app updated with `EnhancedMetricsDashboard`, `RadarComparison`, and `LLMInstanceViewer`.
    -   **Testing**: End-to-End Playwright tests covering visual components and data flow.
-   **Deployment**:
    -   **Backend**: Successfully deployed to **Render** (Production environment configured with Sentry/Prometheus).
    -   **Frontend**: Deployment to **Vercel** is the next pending milestone (Phase F).
-   **Visualization**: Publication-quality vector figures generated (Heatmaps, Radar charts, Boxplots).
