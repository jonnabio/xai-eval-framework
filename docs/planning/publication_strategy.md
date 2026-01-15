# Publication Strategy: JMLR & FAccT

## Overview
This document outlines the two-paper strategy for publishing the results of the XAI Evaluation Framework (EXP1).

- **Paper A**: "A Framework for Rigorous Evaluation of Model-Agnostic Explainability Methods" (JMLR)
- **Paper B**: "LIME vs SHAP: A Comprehensive Empirical Comparison Using LLM-based Semantic Evaluation" (FAccT)

---

## 📄 Paper A: The Framework (JMLR)

**Full Title**: "A Framework for Rigorous Evaluation of Model-Agnostic Explainability Methods: Combining Classical Metrics with LLM-based Semantic Assessment"
**Target Venue**: JMLR (Datasets & Benchmarks Track)
**Length**: 10-12 pages
**Submission Deadline**: Rolling

### Abstract (Draft)
Evaluating explainability methods remains a critical challenge in AI. Existing approaches rely on limited metrics that fail to capture semantic quality. We present [Framework Name], a comprehensive evaluation framework combining classical metrics (fidelity, stability, sparsity, computational cost) with novel advanced metrics (causal alignment, counterfactual sensitivity) and LLM-based semantic assessment. Our framework enables rigorous, reproducible benchmarking of model-agnostic XAI methods across multiple dimensions. We validate the framework through a case study comparing LIME and SHAP on tabular data, demonstrating: (1) LLM evaluators achieve substantial human agreement ($\kappa=0.65$), (2) six metrics capture distinct aspects of explanation quality, (3) reproducibility across runs (CV<0.1). The framework is released as an open-source Python package with complete reproducibility artifacts.

### Key Contributions
1.  **First validated framework** for comprehensive XAI evaluation combining automated and semantic assessment methods.
2.  **Six complementary metrics** spanning technical and semantic quality.
3.  **LLM-based semantic evaluation** validated with human reliability ($\kappa=0.65$).
4.  **Statistical rigor**: Reproducibility protocol and significance testing.
5.  **Reusable implementation**: Modular Python package.

### Structure
1.  **Introduction**: Motivation, gap in current eval, standardized framework need.
2.  **Background**: LIME/SHAP overview, existing metrics gaps, LLMs as evaluators.
3.  **Framework Design**: Architecture, Classical Metrics (Fidelity, Stability, Sparsity, Cost), Advanced Metrics (Causal, CF Sensitivity), LLM-based Semantic Eval.
4.  **Validation Methodology**: Human Agreement Study, Statistical Rigor, Extensibility.
5.  **Case Study**: Tabular Data Evaluation (Adult dataset, RF/XGBoost, LIME/SHAP).
6.  **Discussion**: Strengths, limitations, broader impact.
7.  **Conclusion**

---

## 📄 Paper B: The Comparison (FAccT)

**Full Title**: "LIME vs SHAP: A Comprehensive Empirical Comparison Using LLM-based Semantic Evaluation"
**Target Venue**: FAccT (or AIES)
**Length**: 6-8 pages
**Submission Deadline**: Jan 2025 (FAccT)

### Abstract (Draft)
LIME and SHAP are widely used explainability methods, but guidance on when to use each remains limited. We present the first comprehensive empirical comparison evaluating both methods across six complementary metrics. Our study on tabular data reveals fundamental trade-offs: SHAP offers superior stability (0.95 vs 0.24, $p<0.001$) and fidelity but at 20x` higher computational cost. LIME provides sparser, faster explanations but with high variability. We provide evidence-based recommendations: use LIME for real-time production systems; use SHAP for offline auditing.

### Key Hypotheses
*   **H1**: SHAP more stable than LIME.
*   **H2**: LIME more sparse than SHAP.
*   **H3**: LIME faster than SHAP.
*   **H4**: Methods differ in causal alignment.

### Structure
1.  **Introduction**: LIME vs SHAP dilemma, existing insufficient comparisons.
2.  **Background**: Brief LIME/SHAP overview.
3.  **Methodology**: Evaluation framework (cite Paper A), Adult dataset setup, Metrics.
4.  **Results**:
    *   Overall Comparison (Radar Plot).
    *   Stability: SHAP dominates (0.95 vs 0.24).
    *   Sparsity: LIME more interpretable (1-2 feats vs 5-7).
    *   Cost: LIME 20x faster (0.08s vs 1.9s).
    *   Causal Alignment: SHAP slightly better.
    *   LLM Semantic Eval: Aligns with classical metrics but adds nuance.
5.  **Practical Recommendations**: Decision framework, Deployment patterns (Hybrid/Tiered).
6.  **Limitations & Future Work**.
7.  **Related Work**.
8.  **Conclusion**.

---

## 📊 Experimental Requirements (EXP1)
Based on the paper outlines, EXP1 must provide:

*   **Dataset**: UCI Adult (Stratified sample: 200 instances).
*   **Models**: Random Forest, XGBoost (Accuracy > 0.80).
*   **XAI Methods**:
    *   **LIME**: 5000 samples, 10 features, Euclidean kernel.
    *   **SHAP**: TreeExplainer, 100 background samples.
*   **Metrics (All 6 implemented)**:
    *   Fidelity, Stability, Sparsity, Cost.
    *   Causal Alignment (Ground truth defined).
    *   Counterfactual Sensitivity.
    *   LLM Evaluation (validated).
*   **Validation**: 10 independent runs, 5-fold CV.

## 📝 Writing Timeline
*   **Now - Week 6**: Write Paper A (Framework).
*   **Week 7**: Submit Paper A to JMLR.
*   **Week 8 - 12**: Write Paper B (Comparison).
*   **Week 12**: Submit Paper B to FAccT.

## 🔄 Coordination
*   **Paper A** focuses on the *tool* and *methodology*.
*   **Paper B** focuses on the *empirical findings* and *practical advice*.
*   Submit A first so B can cite usage of the framework.
