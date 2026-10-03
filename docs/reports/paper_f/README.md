# Paper F — External Validity of XAI Benchmark Conclusions

**Working Title:** *To What Extent Do Comparative Conclusions About Model-Agnostic Explanation Methods Generalize Across Tabular Datasets?*  
**Status (2026-10-03):** Analytical framework initiated. Pre-analysis framework and methodological appraisal established prior to dataset commitment or experimental execution. No empirical results have been generated.

---

## 1. Executive Summary & Core Identity

Most XAI benchmarking studies evaluate explainers on a single tabular dataset (most commonly the UCI Adult Census Income benchmark) or report unpooled, ad-hoc evaluations across heterogeneous collections. Consequently, the XAI literature implicitly treats comparative performance—such as *"SHAP dominates in fidelity"* or *"LIME suffers from local instability"*—as general properties of the explanation algorithms rather than as dataset-conditioned phenomena.

**Paper F shifts the paradigm:**
> **The benchmark is the experimental instrument; external generalizability is the object of study.**

The central unit of interest in Paper F is **not** raw explainer performance, but the **transferability of comparative conclusions** across tabular datasets exhibiting distinct structural characteristics.

---

## 2. Research Questions

- **RQ1 (Dataset Main Effect — H1):** Does explanation quality (fidelity, stability, sparsity, faithfulness gap) and computational efficiency systematically differ across tabular datasets when controlling for explainer and model family?
- **RQ2 (Explainer × Dataset Interaction — H2 — Central Anchor):** Does the relative comparative advantage of explainers change depending on dataset structure, or does explainer ranking remain invariant across domains?
- **RQ3 (Ranking Generalizability — H3):** To what degree are intra-dataset explainer orderings ($R_{d,m}$) preserved across domain transitions, both relative to the Adult baseline and across non-baseline dataset pairs?
- **RQ4 (Quality–Cost Trade-Off Stability — H4):** Does the Pareto efficiency frontier relating explanation quality to computational cost remain stable, or do algorithmic trade-offs collapse under specific structural topologies?
- **RQ5 (Synthesis):** Across what tiers of evidence—**Absolute**, **Relative**, or **Ranking**—can XAI benchmark conclusions be legitimately generalized?

---

## 3. Factorial Experimental Architecture (48 Conditions)

The study implements a balanced $4 \times 3 \times 4$ factorial design:

```
4 Datasets × 3 Model Families × 4 Explainers = 48 Primary Conditions
```

- **4 Tabular Datasets:**
  - `Dataset A`: **UCI Adult** (Canonical baseline / reference dataset)
  - `Dataset B`: **Structural Contrast 1** (e.g., Pure continuous, dense correlation manifold)
  - `Dataset C`: **Structural Contrast 2** (e.g., High-cardinality categorical, extreme sparsity)
  - `Dataset D`: **Structural Contrast 3** (e.g., Severe class imbalance, asymmetric decision boundary)
- **3 Model Families:**
  - `Linear`: Logistic Regression / Linear Regularized Models
  - `Tree / Ensemble`: Random Forest / XGBoost / Gradient Boosted Trees
  - `Nonlinear`: Multi-Layer Perceptron (MLP) / RBF Kernel SVM
- **4 Model-Agnostic Explainers:**
  - `LIME`: Local surrogate modeling with perturbation sampling
  - `SHAP`: KernelSHAP / TreeSHAP Shapley value attribution
  - `Anchors`: High-precision IF-THEN perturbation rules
  - `DiCE`: Diverse counterfactual generation via gradient/optimization

---

## 4. Distinctiveness Across the Publication Suite

Paper F occupies a dedicated, unconfounded niche within the overarching research framework:

| Manuscript | Core Focus | Primary Comparison | Dataset Scope | Key Dependent Variable |
|---|---|---|---|---|
| **Paper A / RIMI** | Benchmark architecture prototype | Explainer quality baseline | UCI Adult | Fidelity, Stability, Cost |
| **Paper B+C / IBERAMIA** | Multilevel evaluation framework & taxonomy | Evaluator alignment & validation | Adult (EXP1–4) + EXP3 replication | Metrics + Human/LLM agreement |
| **Paper D / Tec. en Marcha** | Misclassification impact | Correct vs. Incorrect instances | Adult (+ German Credit check) | Quality deficit ($\Delta$ Stability) |
| **Paper E** | Feature attribution consensus | Explainer vs. Explainer (disagreement) | Adult + German Credit + BC | Top-$k$ Jaccard, Rank concordance |
| **Paper F (This Study)** | **External validity & generalizability** | **Comparative conclusions across datasets** | **Adult + 3 Structural Contrasts** | **Rank Concordance, Interaction ($\mathrm{Expl} \times \mathrm{Data}$)** |

---

## 5. End-to-End Analytical Pipeline

```
1. Dataset Structural Characterization (10 standardized dimensions)
                           ↓
2. Baseline Predictive Modeling (12 baselines: 4 datasets × 3 models)
                           ↓
3. 48-Condition XAI Benchmark Execution (Fidelity, Stability, Sparsity, Faithfulness, Cost)
                           ↓
4. Descriptive Metric Profiles & Uncertainty Quantification
                           ↓
5. Within-Dataset Independent Benchmarks (Conclusions A, B, C, D)
                           ↓
6. Cross-Dataset Main Effects Analysis (H1: Y ~ Dataset + Explainer + Model)
                           ↓
7. Explainer × Dataset Interaction Analysis (H2: Explainer × Dataset)
                           ↓
8. Ranking Generalizability Analysis (H3: Kendall's W, Tau, Spearman's Rho across all pairs)
                           ↓
9. Quality–Cost Frontier Stability Analysis (H4: Pareto Dominance Shifts)
                           ↓
10. Three-Tier External Validity Synthesis (Absolute vs. Relative vs. Ranking Generalizability)
```

---

## 6. Directory Map & Associated Artifacts

- [`README.md`](file:///c:/Users/jonna/Github/xai-eval-framework/docs/reports/paper_f/README.md) — This charter document.
- [`ANALYSIS_PLAN.md`](file:///c:/Users/jonna/Github/xai-eval-framework/docs/reports/paper_f/ANALYSIS_PLAN.md) — Pre-analysis protocol locking hypotheses, metric formalizations, statistical procedures, and acceptance criteria.
- [`METHODOLOGICAL_ANALYSIS.md`](file:///c:/Users/jonna/Github/xai-eval-framework/docs/reports/paper_f/METHODOLOGICAL_ANALYSIS.md) — Rigorous scientific appraisal of research challenges, algorithmic sensitivities, dataset selection archetypes, and threats to validity.
