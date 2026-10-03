# Paper F — Scientific Pre-Analysis Plan: External Validity of XAI Benchmark Conclusions

**Question:** *To what extent do comparative conclusions about model-agnostic explanation methods generalize across tabular datasets with different structural characteristics?*  
**Status:** Pre-Analysis Protocol locked prior to experimental execution or dataset commitment, 2026-10-03. No Paper F empirical result has been computed.  
**Scope:** 48 primary experimental conditions (4 datasets × 3 model families × 4 explainers), characterized across 5 evaluation dimensions (Fidelity, Stability, Sparsity, Faithfulness Gap, Computational Cost).

---

## 1. Research Objective & Epistemological Stance

### 1.1 Primary Research Question
*To what extent do comparative conclusions about model-agnostic explanation methods generalize across tabular datasets with different structural characteristics?*

### 1.2 The Object of Inquiry
In conventional XAI benchmarking, the dataset is treated as an interchangeable substrate and the algorithm is the primary object of evaluation. In Paper F, this relationship is inverted:
- **The benchmark is the experimental instrument.**
- **The external generalizability of benchmark conclusions is the object of inquiry.**

The unit of interest is **not** raw explainer performance on a given benchmark cell. It is the **transferability of comparative findings and rankings** across datasets exhibiting purposeful structural variation.

### 1.3 Baseline Reference
The **UCI Adult Census Income** dataset serves as the historical anchor and reference baseline ($Dataset\ A$), reflecting its ubiquitous role in Papers A, B+C, D, and the broader literature. However, the study guards against "Adult-centric parochialism" by evaluating generalizability across all dataset-pair permutations ($A \leftrightarrow B$, $A \leftrightarrow C$, $A \leftrightarrow D$, $B \leftrightarrow C$, $B \leftrightarrow D$, $C \leftrightarrow D$).

---

## 2. Factorial Experimental Design (48 Conditions)

The experiment implements a fully crossed $4 \times 3 \times 4$ factorial structure yielding 48 primary experimental conditions:

$$\text{Conditions} = 4\ \text{Datasets} \times 3\ \text{Model Families} \times 4\ \text{Explainers} = 48$$

```
                           4 TABULAR DATASETS
         ┌───────────────────┬───────────────────┬───────────────────┬───────────────────┐
         │ Adult (Reference) │ Dataset B         │ Dataset C         │ Dataset D         │
         │ Mixed / Baseline  │ Contrast 1        │ Contrast 2        │ Contrast 3        │
         └─────────┬─────────┴─────────┬─────────┴─────────┬─────────┴─────────┬─────────┘
                   │                   │                   │                   │
                   ▼                   ▼                   ▼                   ▼
    ┌────────────────────────────────────────────────────────────────────────────────────────┐
    │                                   3 MODEL FAMILIES                                     │
    │        1. Linear (LogReg)   │   2. Tree Ensemble (RF/XGB)   │   3. Nonlinear (MLP)     │
    └───────────────────────────────────────────┬────────────────────────────────────────────┘
                                                │
                                                ▼
    ┌────────────────────────────────────────────────────────────────────────────────────────┐
    │                                 4 AGNOSTIC EXPLAINERS                                  │
    │       1. LIME (Surrogate)   │   2. SHAP (Shapley)   │   3. Anchors   │   4. DiCE       │
    └────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Model Families
1. **Linear:** Logistic Regression with $L_2$ regularization (interpretable, convex baseline with linear decision boundaries).
2. **Tree / Ensemble:** Random Forest / XGBoost (non-linear, axis-aligned partitioning with non-smooth boundaries).
3. **Nonlinear Continuous:** Multi-Layer Perceptron (MLP) with ReLU activations (smooth, highly non-linear decision manifolds).

### 2.2 Agnostic Explainers
1. **LIME:** Local sparse linear surrogate computed over isotropic Gaussian/tabular perturbations.
2. **SHAP:** Marginal/KernelSHAP and TreeSHAP (where family permits) computing additive Shapley attributions.
3. **Anchors:** Bottom-up beam search identifying high-precision IF-THEN perturbation-invariant rules.
4. **DiCE:** Gradient- and optimization-based diverse counterfactual search under feasibility constraints.

### 2.3 Repetition and Sampling Protocols
- **Instances per condition:** Fixed evaluation sample $n_{\text{eval}} = 100$ per quadrant / class-balanced partition, matching EXP2/EXP3 standards.
- **Seeds:** 5 fixed random seeds ($s \in \{42, 123, 456, 789, 101112\}$) controlling data splitting, model training, and explainer stochasticity.
- **Instance alignment:** For a given dataset, model, and seed, all four explainers explain the exact identical set of test instances.

---

## 3. Dataset Characterization Protocol

Prior to training classifiers or generating explanations, each candidate dataset must be profiled across a standardized 10-dimensional structural matrix.

### 3.1 Structural Characterization Dimensions
| Dimension | Metric / Operationalization | Formal Symbol | Purpose |
|---|---|---|---|
| **1. Sample Size** | Total available observations | $n$ | Determines statistical power & manifold density |
| **2. Raw Dimensionality** | Unprocessed feature count | $d_{\text{raw}}$ | Base problem complexity |
| **3. Effective Dimensionality** | Dimensions post one-hot & scaling | $d_{\text{eff}}$ | True dimensionality exposed to explainers |
| **4. Feature Composition** | Ratio of continuous to categorical | $\rho_{\text{type}} = d_{\text{cont}} / d_{\text{raw}}$ | Explores perturbation validity differences |
| **5. Categorical Cardinality** | Median & maximum category levels | $\kappa_{\text{med}}, \kappa_{\text{max}}$ | Measures one-hot sparsity expansion |
| **6. Class Balance** | Minority class proportion | $\pi_{\text{min}} = \min(P(y=0), P(y=1))$ | Quantifies decision-boundary asymmetry |
| **7. Missingness** | Overall % missing & mechanism (MCAR/MAR) | $\%_{\text{miss}}$ | Identifies imputation artifact risks |
| **8. Distributional Skewness** | Mardia's multivariate skewness / kurtosis | $\gamma_{1,d}, \gamma_{2,d}$ | Quantifies non-normality & outlier presence |
| **9. Feature Dependence** | Mean pairwise correlation & variance inflation | $\bar{r}, \overline{\text{VIF}}$ | Quantifies multicollinearity (critical for SHAP/LIME) |
| **10. Predictive Difficulty** | 5-fold CV AUC-ROC of baseline models | $\text{AUC}_{\text{CV}}$ | Establishes model learnability & margin sharpness |

### 3.2 Methodological Invariant: Strictly Descriptive Framing
> [!IMPORTANT]
> The structural characterization protocol is **strictly descriptive**. Causal claims attributing explainer behavior to specific structural dimensions (e.g., *"LIME failed because correlation was high"*) are prohibited in the confirmatory analysis because four datasets cannot support causal inference across ten collinear structural dimensions. Structural profiles serve solely to demonstrate purposeful contrast and frame external validity boundaries.

---

## 4. Baseline Predictive Analysis

Before computing explanations, the validity of the predictive models must be empirically established across all 12 dataset-model combinations ($4\ \text{Datasets} \times 3\ \text{Model Families}$).

### 4.1 Required Predictive Metrics
For each of the 12 combinations, report:
1. **Discrimination:** Stratified 5-fold cross-validated **ROC-AUC** and **Balanced Accuracy**.
2. **Precision–Recall Balance:** Macro-averaged **$F_1$-score**.
3. **Probability Calibration:** **Brier Score** and expected calibration error (ECE).

### 4.2 Quality Gating Criterion
- Any model exhibiting chance-level discrimination ($\text{AUC} \le 0.55$) fails the validity gate. An explainer cannot be evaluated on a decision surface that reflects pure label noise. If a model fails to converge or train satisfactorily on a given dataset, hyperparameter grids must be systematically adjusted under a logged deviation.

---

## 5. Explanation-Quality & Efficiency Metrics

For each of the 48 conditions, five standardized metrics from the repository's core framework are collected:

### 5.1 Metric Formulations
1. **Fidelity ($\mathcal{F}_{\text{fid}}$):** Accuracy or $R^2$ of the explainer's local proxy model within the local perturbation neighborhood $\mathcal{N}(x)$ relative to the black-box prediction:
   $$\mathcal{F}_{\text{fid}} = \frac{1}{|\mathcal{N}(x)|} \sum_{z \in \mathcal{N}(x)} \mathbb{I}[f(z) = g_x(z)]$$
2. **Stability ($\mathcal{S}_{\text{stab}}$):** Lipschitz-like consistency under infinitesimal feature perturbation $\epsilon$:
   $$\mathcal{S}_{\text{stab}} = 1 - \frac{\|e(x) - e(x + \epsilon)\|_2}{\|\epsilon\|_2}$$
   (operationalized via cosine similarity or rank correlation between original and perturbed explanations).
3. **Sparsity / Parsimony ($\mathcal{P}_{\text{spar}}$):** Proportion of features receiving zero or negligible attribution (or inverse length of Anchors rules / DiCE feature changes):
   $$\mathcal{P}_{\text{spar}} = \frac{1}{d} \sum_{j=1}^d \mathbb{I}[|e_j(x)| < \tau]$$
4. **Faithfulness Gap ($\mathcal{G}_{\text{faith}}$):** The monotonicity of model prediction attenuation upon systematically masking the top-$k$ most important features:
   $$\mathcal{G}_{\text{faith}} = |f(x) - f(x_{\setminus \text{top-}k})|$$
5. **Computational Cost ($\mathcal{C}_{\text{cost}}$):** Mean wall-clock execution time (in milliseconds) required to generate a single instance explanation:
   $$\mathcal{C}_{\text{cost}} = \frac{1}{N} \sum_{i=1}^N t_{\text{elapsed}}(x_i)$$

### 5.2 Descriptive Representation
Raw metric outcomes are expressed as:
$$M_{d,m,e} = f(\text{Dataset}_d, \text{Model}_m, \text{Explainer}_e)$$
All reporting must present **central tendency** (mean, median), **dispersion** (IQR, standard deviation), and **uncertainty** (95% bootstrap confidence intervals derived from 2,000 cluster-resamples on seed). Point estimates alone are strictly disallowed.

---

## 6. Within-Dataset Analysis Protocol

The analysis first treats each dataset as an autonomous benchmark study:

```
Dataset A (Adult)     ──>  Benchmark Report A: Explainer comparisons & conclusions
Dataset B (Contrast 1)──>  Benchmark Report B: Explainer comparisons & conclusions
Dataset C (Contrast 2)──>  Benchmark Report C: Explainer comparisons & conclusions
Dataset D (Contrast 3)──>  Benchmark Report D: Explainer comparisons & conclusions
```

### 6.1 Intra-Dataset Comparative Inquiries
Within each dataset $d \in \{A, B, C, D\}$ independently:
1. Which explainer achieves the highest fidelity, stability, sparsity, and faithfulness?
2. Are explainer differences statistically significant within dataset $d$ (non-parametric Friedman tests with post-hoc Holm-adjusted Wilcoxon signed-rank tests)?
3. What is the qualitative benchmark conclusion (e.g., *"SHAP is strictly superior in fidelity on Dataset B, but DiCE exhibits lowest stability"* )?

This creates four distinct, self-contained empirical pictures against which transferability is evaluated.

---

## 7. Cross-Dataset Statistical Inferential Strategy (H1 & H2)

### 7.1 Formal Hypotheses
- **H1 (Dataset Main Effect):** Explanation quality metrics systematically differ across datasets after controlling for explainer and model family:
  $$H_{1,0}: \beta_{\text{Dataset}} = 0 \quad \text{vs.} \quad H_{1,1}: \beta_{\text{Dataset}} \neq 0$$
- **H2 (Explainer × Dataset Interaction — Central Hypothesis):** The relative performance differences among explainers are moderated by the dataset:
  $$H_{2,0}: \gamma_{\text{Explainer} \times \text{Dataset}} = 0 \quad \text{vs.} \quad H_{2,1}: \gamma_{\text{Explainer} \times \text{Dataset}} \neq 0$$

### 7.2 Model Specification
To accommodate the repeated-measures structure (instances nested within models and seeds, evaluated across multiple explainers), we specify a **Linear Mixed-Effects Model (LMM)** or **Aligned Rank Transform (ART-ANOVA)** for non-normal metric distributions:

$$Y_{ijk} = \mu + \alpha_i (\text{Dataset}) + \beta_j (\text{Explainer}) + \gamma_k (\text{Model}) + (\alpha\beta)_{ij} (\text{Dataset} \times \text{Explainer}) + (\beta\gamma)_{jk} + u_{\text{seed}} + \epsilon_{ijk}$$

Where:
- $\alpha_i$ represents the fixed effect of the $i$-th dataset ($i \in \{1..4\}$).
- $\beta_j$ represents the fixed effect of the $j$-th explainer ($j \in \{1..4\}$).
- $\gamma_k$ controls for classifier family ($k \in \{1..3\}$).
- $(\alpha\beta)_{ij}$ is the critical interaction term testing **H2**.
- $u_{\text{seed}}$ is the random intercept accounting for seed-level variance.

### 7.3 Effect Size Reporting
Alongside $F$-tests and $p$-values:
- Report **partial $\eta^2$** ($\eta_p^2$) and Cohen's $f^2$ for main effects and interactions.
- If $(\alpha\beta)_{ij}$ is statistically significant ($p < 0.01$) and exhibits a non-trivial effect size ($\eta_p^2 \ge 0.06$), **H2 is confirmed**, demonstrating that comparative benchmark claims do not exhibit domain invariance.

---

## 8. Ranking Generalizability Protocol (H3)

### 8.1 Explainer Rank Vector Formulation
For each metric $m$ and dataset $d$, construct the 4-element explainer rank vector:
$$R_{d,m} = \big(r_{\text{LIME}}, r_{\text{SHAP}}, r_{\text{Anchors}}, r_{\text{DiCE}}\big) \in \{1, 2, 3, 4\}^4$$
where rank 1 represents the optimal performer on metric $m$.

### 8.2 Rank Agreement Statistics
1. **Pairwise Rank Concordance:** For each metric $m$, compute Kendall's $\tau_b$ and Spearman's $\rho$ across all 6 dataset pairs:
   $$\tau(R_{d_1, m}, R_{d_2, m}) \quad \forall (d_1, d_2) \in \{(A,B), (A,C), (A,D), (B,C), (B,D), (C,D)\}$$
2. **Global Concordance:** Compute **Kendall's Coefficient of Concordance ($W$)** across all 4 datasets simultaneously:
   $$W_m = \frac{12 \sum_{j=1}^4 \big(\bar{R}_{j,m} - \frac{k(n+1)}{2}\big)^2}{k^2(n^3 - n)}$$
   where $k=4$ datasets and $n=4$ explainers.

### 8.3 Rank Invariance Thresholds
- $W \ge 0.80$: Strong rank generalizability (explainer hierarchy is robust across domains).
- $0.50 \le W < 0.80$: Moderate generalizability (hierarchy fluctuates in intermediate ranks).
- $W < 0.50$: Rank breakdown (explainer hierarchy is highly domain-dependent; benchmark rankings do not generalize).

---

## 9. Quality–Cost Generalizability Protocol (H4)

### 9.1 Efficiency Frontier Formalization
For each dataset $d$, construct the two-dimensional bi-objective space:
$$\mathcal{P}_d = \big\{ (\mathcal{F}_{\text{fid}}(e), \mathcal{C}_{\text{cost}}(e)) \mid e \in \{\text{LIME}, \text{SHAP}, \text{Anchors}, \text{DiCE}\} \big\}$$

### 9.2 Pareto Dominance Criteria
An explainer $e_1$ Pareto-dominates $e_2$ ($e_1 \succ e_2$) if:
$$\mathcal{F}_{\text{fid}}(e_1) \ge \mathcal{F}_{\text{fid}}(e_2) \quad \text{and} \quad \mathcal{C}_{\text{cost}}(e_1) \le \mathcal{C}_{\text{cost}}(e_2)$$
with at least one strict inequality.

### 9.3 Frontier Shift Analysis
- Identify the **non-dominated Pareto set** $\Omega_d \subseteq \{\text{LIME}, \text{SHAP}, \text{Anchors}, \text{DiCE}\}$ for each dataset.
- Test whether membership in $\Omega_d$ remains invariant:
  $$\Omega_A \stackrel{?}{=} \Omega_B \stackrel{?}{=} \Omega_C \stackrel{?}{=} \Omega_D$$
- Quantify **relative cost inflation**: Does an explainer's relative cost inflate disproportionately when moving from low $d_{\text{eff}}$ to high $d_{\text{eff}}$ datasets, dropping it from the frontier?

---

## 10. Three-Tier Generalizability Synthesis Framework

All empirical findings are synthesized into three distinct tiers of external validity:

```
                       THREE-TIER SYNTHESIS HIERARCHY
  ┌────────────────────────────────────────────────────────────────────────┐
  │ Tier 1: Absolute Generalizability                                     │
  │ Do raw metric values remain comparable across datasets?               │
  │ Criteria: Ratio of variance across datasets vs. within datasets       │
  ├────────────────────────────────────────────────────────────────────────┤
  │ Tier 2: Relative Generalizability                                     │
  │ Are relative advantage margins (Cohen's d) between explainers stable? │
  │ Criteria: Explainer × Dataset interaction magnitude (eta_p^2)         │
  ├────────────────────────────────────────────────────────────────────────┤
  │ Tier 3: Ranking Generalizability                                      │
  │ Is the ordinal sequence (best to worst) of explainers preserved?       │
  │ Criteria: Kendall's W >= 0.80 and pairwise tau_b significance         │
  └────────────────────────────────────────────────────────────────────────┘
```

| Generalizability Tier | Target Question | Operational Test | Plausible Outcome |
|---|---|---|---|
| **Tier 1: Absolute** | Do raw scores transfer? | Equivalence testing / ANOVA $R^2$ of Dataset | **Rejected:** Metric baselines scale with dimensionality & noise. |
| **Tier 2: Relative** | Do effect sizes transfer? | $\text{Explainer} \times \text{Dataset}$ interaction ($\eta_p^2$) | **Conditioned:** Moderate interactions expected for sparse vs. dense data. |
| **Tier 3: Ranking** | Does explainer hierarchy transfer? | Kendall's $W$ and pairwise $\tau_b$ | **Core Test:** Reveals whether practitioners can trust general recommendations. |

---

## 11. Reproducibility, Seed Controls, and Pre-Registration Invariants

1. **Pre-Analysis Locking:** This document is committed to version control **before** candidate datasets B, C, and D are finalized and before any Paper F code is executed.
2. **Deterministic Seed Tracking:** All splits, model initializations, and explainer sampling routines use five locked PRNG seeds ($42, 123, 456, 789, 101112$).
3. **Traceability:** Every reported table and figure will have a dedicated generator script in `scripts/` mapping directly to artifacts in `outputs/analysis/paper_f/`.
4. **Deviation Log:** Any departure from this pre-analysis plan must be recorded with a dated rationale in Section 13 prior to manuscript finalization.

---

## 12. Pre-Analysis Plan Amendments & Deviation Log
*(Reserved for post-registration refinements prior to data collection)*

| Date | Section | Nature of Amendment | Justification / Authority |
|---|---|---|---|
| 2026-10-03 | All | Plan created and locked | Initial study framework established |
