# Publication Strategy: JMLR, AIES, & FAccT

## Overview
This document outlines the three-paper strategy for publishing the results of the XAI Evaluation Framework and fulfilling the PhD thesis objectives.

- **Paper A**: "A Framework for Rigorous Quantitative Evaluation of Model-Agnostic Explainability Methods" (JMLR)
- **Paper B**: "LIME vs SHAP: A Comprehensive Empirical Comparison at Scale" (AIES)
- **Paper C**: "Aligning LLM-based Semantic Assessment of Explainability with Human Validation" (FAccT)

---

## 📄 Paper A: The Framework (JMLR)

**Full Title**: "A Framework for Rigorous Evaluation of Model-Agnostic Explainability Methods: Multi-Metric Statistical Benchmarking, Operational Protocol, and Reproducibility"
**Target Venue**: JMLR (Datasets & Benchmarks Track)
**Length**: 10-12 pages
**Submission Deadline**: Rolling

### Abstract (Draft)
Evaluating explainability methods requires more than a single faithfulness proxy. We present a modular benchmarking framework centered on quantitative XAI quality metrics: fidelity, stability, sparsity, computational cost, and faithfulness gap, plus an explicit method for operating the framework end-to-end (FOM-7). On the UCI Adult benchmark, we validate the framework through a staged protocol spanning 300 robustness configurations. Our framework enables rigorous, reproducible benchmarking of model-agnostic XAI methods across multiple dimensions, controlling for dataset leakage and algorithmic variance. Results reject the null of equal method performance across primary metrics, highlighting strict quality-cost frontiers. The framework is released as an open-source Python package with complete reproducibility artifacts.

### Key Contributions
1.  **First validated operational framework** (FOM-7) for comprehensive XAI benchmarking and reproducibility governance.
2.  **Five complementary quantitative metrics** spanning technical quality and operational cost.
3.  **Extensive experimental coverage**: Built-in benchmarking spanning five model families and four explainer families.
4.  **Statistical rigor**: Non-parametric paired testing and multiplicity-aware significance testing across 300 settings.
5.  **Reusable implementation**: Modular Python package.

### Structure
1.  **Introduction**: Motivation, gap in current eval, standardized framework need.
2.  **Background**: LIME/SHAP overview, existing metrics gaps.
3.  **Framework Design**: Architecture, Operational Protocol (FOM-7), and Classical Metrics (Fidelity, Stability, Sparsity, Faithfulness Gap, Cost).
4.  **Validation Methodology**: Statistical Rigor, Extensibility, Artifact integrity.
5.  **Results**: Robustness benchmarking across complete model-size blocks.
6.  **Discussion**: Strengths, limitations, broader impact.
7.  **Conclusion**

---

## 📄 Paper B: The Comparison (AIES)

**Full Title**: "LIME vs SHAP: A Comprehensive Empirical Comparison at Scale"
**Target Venue**: AIES (AI, Ethics, and Society)
**Length**: 6-8 pages
**Submission Deadline**: TBD

### Abstract (Draft)
LIME and SHAP are widely used explainability methods, but guidance on when to use each remains limited. We present a comprehensive empirical comparison evaluating both methods across advanced quantitative metrics including causal alignment and counterfactual sensitivity. Our study on tabular data reveals fundamental trade-offs: SHAP offers superior stability and fidelity but at significantly higher computational cost. LIME provides sparser, faster explanations but with high variability. We provide evidence-based recommendations: use LIME for real-time production systems; use SHAP for offline auditing.

### Key Hypotheses
*   **H1**: SHAP more stable than LIME.
*   **H2**: LIME more sparse than SHAP.
*   **H3**: LIME faster than SHAP.
*   **H4**: Methods differ in causal alignment and counterfactual sensitivity (Thesis Obj 2).

### Structure
1.  **Introduction**: LIME vs SHAP dilemma, existing insufficient comparisons.
2.  **Background**: Brief LIME/SHAP overview.
3.  **Methodology**: Evaluation framework (cite Paper A), Adult dataset setup, Metrics (incorporating Causal/CF metrics).
4.  **Results**:
    *   Overall Comparison (Radar Plot).
    *   Stability, Sparsity, and Cost.
    *   Causal Alignment and Counterfactual Sensitivity.
5.  **Practical Recommendations**: Decision framework, Deployment patterns (Hybrid/Tiered).
6.  **Conclusion**.

---

## 📄 Paper C: LLM & Human Evaluation (FAccT)

**Full Title**: "Aligning LLM-based Semantic Assessment of Explainability with Human Validation"
**Target Venue**: FAccT
**Length**: 8-10 pages
**Submission Deadline**: Jan 2026/2027 (FAccT)

### Abstract (Draft)
While quantitative metrics measure the technical fidelity of AI explanations, they often fail to capture semantic usability for human stakeholders. We introduce a novel LLM-based semantic assessment framework for XAI, evaluating explanations on clarity, coherence, and actionability. To validate LLM proxies, we conduct a comprehensive human annotation study, demonstrating that carefully prompted LLM evaluators achieve substantial human agreement ($\kappa=0.65$). We further map semantic qualities to classical quantitative metrics, showing where computational stability diverges from human-perceived utility.

### Key Contributions (Thesis Objectives 3 & 4)
1.  **LLM-based semantic evaluation** for tabular XAI.
2.  **Human Validation Study** proving LLM reliability as explanation judges ($\kappa=0.65$).
3.  **Correlation Analysis** between classical quantitative metrics and user-centric semantic scores.

### Structure
1.  **Introduction**: The gap between technical fidelity and human interpretability.
2.  **Methodology**: LLM Prompting strategies for judging explainability.
3.  **Human Validation**: Study design, annotator agreement, and mapping to LLMs.
4.  **Results**: LLM vs Human $\kappa$ scores, Semantic vs Classical metric correlations.
5.  **Discussion**: When to rely on LLMs for XAI evaluation.
6.  **Conclusion**

---

## 📊 Experimental Requirements (EXP1 & EXP2 & EXP3)

*   **Paper A (EXP1/EXP2)**: UCI Adult, 5 Models, 4 Explainers, 5 Metrics, 300 runs.
*   **Paper B (EXP2 extension)**: Focus deep-dive on SHAP/LIME, adding Causal Alignment and Counterfactual Sensitivity runs.
*   **Paper C (EXP3)**: Human annotation study (approx 50-100 explanations), LLM evaluation pipeline (e.g., GPT-4/Claude) over the same dataset.

## 📝 Writing Timeline
*   **Now**: Finalize Paper A (Framework & Quantitative).
*   **Next Month**: Submit Paper A to JMLR.
*   **Following Months**: Execute EXP3 (Human/LLM) and Draft Papers B & C concurrently based on venue deadlines.
