# Mathematical & Methodological Architecture of the PhD Dissertation: Rigorous Multi-Metric Benchmarking of Model-Agnostic Explainable AI
*Advanced PhD Level (Researchers, Doctoral Committee, & Peer Reviewers)*

---

## 1. Formal Problem Formulation & Theoretical Foundations

Let $f: \mathcal{X} \to \mathcal{Y}$ represent an opaque, non-linear black-box predictor trained over an input feature space $\mathcal{X} \subseteq \mathbb{R}^d$ to map to a target space $\mathcal{Y}$. In local post-hoc Explainable AI (XAI), given a target instance $\mathbf{x} \in \mathcal{X}$, the goal is to construct an interpretable model $g \in \mathcal{G}$ operating over a simplified binary input vector $\mathbf{x}' \in \{0, 1\}^M$ that locally approximates the decision boundary of $f$ around $\mathbf{x}$.

### 1.1 Mathematical Formulation of Post-Hoc Explainer Paradigms

#### A. Local Interpretable Model-agnostic Explanations (LIME)
LIME formulates local explanation as an additive feature attribution optimization problem:
$$\arg\min_{g \in \mathcal{G}} \mathcal{L}(f, g, \pi_{\mathbf{x}}) + \Omega(g)$$
where $\mathcal{L}$ measures the local unfaithfulness of $g$ in approximating $f$ over a perturbed sample space $\mathcal{Z}$, weighted by an exponential proximity kernel:
$$\pi_{\mathbf{x}}(\mathbf{z}) = \exp\left( -\frac{D(\mathbf{x}, \mathbf{z})^2}{\sigma^2} \right)$$
and $\Omega(g)$ penalizes model complexity (e.g., constraining the $L_0$ norm $\|g\|_0 \le K$).

#### B. Shapley Additive exPlanations (SHAP & KernelSHAP)
SHAP calculates the unique additive feature attribution vector $\boldsymbol{\phi} = (\phi_1, \dots, \phi_M) \in \mathbb{R}^M$ satisfying four fundamental game-theoretic axioms: **Efficiency** ($\sum \phi_i = f(\mathbf{x}) - \mathbb{E}[f(\mathbf{x})]$), **Symmetry**, **Dummy/Nullity**, and **Additivity**.

The classical Shapley value for feature $i$ given characteristic function $v(S) = \mathbb{E}_{\mathbf{z} \sim \mathcal{D}}[f(\mathbf{z}) \mid \mathbf{z}_S = \mathbf{x}_S]$ is defined by:
$$\phi_i(v) = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(|N|-|S|-1)!}{|N|!} \Big[ v(S \cup \{i\}) - v(S) \Big]$$

KernelSHAP estimates $\boldsymbol{\phi}$ by solving a weighted linear regression over simplified coalition vectors $\mathbf{z}' \in \{0,1\}^M$ with Shapley kernel weights:
$$\pi_{\mathbf{x}}(\mathbf{z}') = \frac{M - 1}{\binom{M}{|\mathbf{z}'|} |\mathbf{z}'| (M - |\mathbf{z}'|)}$$

#### C. Anchors (High-Precision Rule Explanations)
An Anchor is a rule predicate $A \subseteq \text{predicates}$ such that $A(\mathbf{x}) = 1$, maximizing coverage $\text{cov}(A) = \mathbb{P}_{\mathbf{z} \sim \mathcal{D}}[A(\mathbf{z}) = 1]$ subject to a high-precision probabilistic constraint:
$$\mathbb{P}_{\mathbf{z} \sim \mathcal{D}(\cdot \mid A(\mathbf{z})=1)} \Big[ f(\mathbf{z}) = f(\mathbf{x}) \Big] \ge \tau \quad \text{with confidence } 1 - \delta$$
where $\tau \in (0, 1]$ (typically $\tau = 0.95$).

#### D. Diverse Counterfactual Explanations (DiCE)
DiCE generates a set of $K$ diverse counterfactual instances $\mathbf{C} = \{\mathbf{c}_1, \dots, \mathbf{c}_K\}$ solving the multi-objective loss:
$$\arg\min_{\mathbf{c}_1, \dots, \mathbf{c}_K} \frac{1}{K}\sum_{k=1}^K \text{loss}(f(\mathbf{c}_k), y^*) + \frac{\alpha}{K}\sum_{k=1}^K \text{dist}(\mathbf{x}, \mathbf{c}_k) - \beta \cdot \text{DPP\_diversity}(\mathbf{c}_1, \dots, \mathbf{c}_K)$$
where $y^* \neq f(\mathbf{x})$ is the desired counterfactual target class, $\text{dist}(\cdot, \cdot)$ is a normalized distance metric, and $\text{DPP\_diversity}$ maximizes the determinant of the diversity kernel matrix using a Determinantal Point Process.

---

## 2. The FOM-7 Operational Protocol: 7-Gate Governance Architecture

To eliminate experimental drift, un-reproducible seed variation, and reporting bias in XAI evaluation, this dissertation introduces the **FOM-7 Protocol** (*Framework for Operational Metrics in 7 Gates*).

```
[ Gate 1: Freezing ] ──> Pre-registered design & hypothesis matrix (300 cells)
         │
         ▼
[ Gate 2: Execution ] ──> Deterministic execution under manifest isolation
         │
         ▼
[ Gate 3: Audit ]     ──> Artifact integrity check (|E*| = 275 qualified cells)
         │
         ▼
[ Gate 4: Harmonize ] ──> Block-level aggregation over K=15 (model x sample-size) blocks
         │
         ▼
[ Gate 5: Export ]    ──> Non-parametric inferential testing (Friedman + Nemenyi + Holm)
         │
         ▼
[ Gate 6: Profile ]   ──> Variance decomposition (CV = sigma/mu) separating seeds from methods
         │
         ▼
[ Gate 7: Report ]    ──> Provenance-backed claim registry (pub/claim_registry.toml)
```

### 2.1 Formal Specification of the 7 Gates

1. **Gate 1 (Freezing):** Pre-registration of experimental space $\mathcal{E} = \mathcal{M} \times \mathcal{X}_{exp} \times \mathcal{S} \times \mathcal{N}$, where $|\mathcal{M}|=5$ model families ($\text{LogReg}, \text{RF}, \text{XGB}, \text{SVM}, \text{MLP}$), $|\mathcal{X}_{exp}|=4$ explainers ($\text{LIME}, \text{SHAP}, \text{Anchors}, \text{DiCE}$), $|\mathcal{S}|=5$ random seeds, and $|\mathcal{N}|=3$ sample sizes ($N \in \{100, 500, 1000\}$), producing 300 planned experimental cells.
2. **Gate 2 (Execution):** Containerized execution via deterministic manifest files.
3. **Gate 3 (Audit):** Rigorous filtering of cell artifacts:
   $$\mathcal{E}^* = \{ e \in \mathcal{E} \mid \text{status}(e) \in \{\text{ok\_instance}, \text{ok\_aggregated}\} \}$$
   In our benchmark, $|\mathcal{E}^*| = 275$ qualified cells ($91.67\%$ yield); non-qualifying cells (primarily constraint timeouts in DiCE/Anchors) are formally audited and logged rather than imputed.
4. **Gate 4 (Harmonization):** Block-level metric aggregation across $K=15$ model-size blocks ($\text{block}_{m, n} = \text{model}_m \times \text{size}_n$).
5. **Gate 5 (Exportation):** Inferential statistical evaluation using non-parametric Friedman tests:
   $$Q = \frac{12 K}{k(k+1)} \left[ \sum_{j=1}^k \bar{R}_j^2 - \frac{k(k+1)^2}{4} \right] \sim \chi^2_{k-1}$$
   Followed by post-hoc Nemenyi tests with Critical Distance ($CD$):
   $$CD = q_{\alpha, k} \sqrt{\frac{k(k+1)}{6K}}$$
   with Holm-Bonferroni step-down multiplicity correction.
6. **Gate 6 (Profiling):** Variance decomposition isolating seed-induced stochasticity ($\sigma^2_{\text{seed}}$) from true explainer main effects ($\sigma^2_{\text{method}}$) via the Coefficient of Variation ($CV = \frac{\sigma}{\mu}$).
7. **Gate 7 (Reporting):** Automated verification mapping published numbers back to raw execution artifacts via `pub/claim_registry.toml`.

---

## 3. The PhD Publication Matrix: Scientific Arc & Contributions

```
                          ┌─────────────────────────────────────────┐
                          │   PhD Thesis: Rigorous XAI Evaluation   │
                          └────────────────────┬────────────────────┘
                                               │
         ┌─────────────────────────────────────┼─────────────────────────────────────┐
         │                                     │                                     │
         ▼                                     ▼                                     ▼
[ Theoretical & Methodological ]      [ Empirical Benchmark ]               [ Governance & Human ]
  ├── Paper A (RIMI 2026): FOM-7        ├── Paper B (CLEIej): LIME vs SHAP    ├── Paper E (CyS): Pareto Frontier
  └── Paper C (Tec. Marcha): Scaling    └── Paper D (Tec. Marcha): Adult      └── Paper F (JCSI): Human/LLM Judge
```

---

### Paper A: Theoretical & Methodological Framework (FOM-7 Protocol)
* **Venue & Status:** Published in *Revista de Investigación Multidisciplinaria Iberoamericana (RIMI)* (2026, DOI: `10.69850/rimi.vi3.307`).
* **Core Contribution:** Establishes the formal mathematical foundation of multi-metric evaluation ($\text{Fidelity}, \text{Stability}, \text{Sparsity}, \text{Cost}, \text{Faithfulness Gap}$) and specifies the 7-gate FOM-7 protocol.
* **Key Finding:** Proves that single-metric evaluations (e.g., fidelity alone) create false rankings because methods optimize different objective trade-offs.

---

### Paper B: Scaled Empirical Comparison — LIME vs SHAP
* **Venue & Status:** Submitted to *CLEI Electronic Journal (CLEIej)* (2026-10-04, Subm. #1196).
* **Core Hypotheses Tested:**
  * $H_1$: $\text{Stability}(\text{SHAP}) > \text{Stability}(\text{LIME})$ ($p < 0.001$, confirmed).
  * $H_2$: $\text{Sparsity}(\text{LIME}) < \text{Sparsity}(\text{SHAP})$ (confirmed).
  * $H_3$: $\text{Cost}(\text{LIME}) \ll \text{Cost}(\text{SHAP})$ ($p < 0.001$, confirmed).
* **Key Finding:** Proves that KernelSHAP's Shapley kernel optimization guarantees numerical stability under input perturbation, whereas LIME's monte-carlo perturbation sampling introduces significant seed variance ($\sigma^2_{\text{seed}}$), leading to instability across runs.

---

### Paper C: Scalability, Sample Size Dynamics, & Robustness
* **Venue & Status:** Ready to submit to *Tecnología en Marcha* (AI Special Issue, Zenodo v0.12.0 DOI: `10.5281/zenodo.23165763`).
* **Core Contribution:** Analyzes the functional scaling behavior of explainers as background sample size $N$ increases from 100 to 1,000 instances.
* **Key Finding:** Demonstrates that KernelSHAP's computational complexity scales as $\mathcal{O}(N \cdot M \cdot 2^M)$ without background sub-sampling, creating a steep execution cost barrier, whereas tree-specific algorithms (TreeSHAP) exploit structural paths to reduce complexity to $\mathcal{O}(N \cdot L \cdot D^2)$.

---

### Paper D: Empirical Validation on Tabular Benchmarks (UCI Adult)
* **Venue & Status:** Ready to submit to *Tecnología en Marcha* (AI Special Issue).
* **Core Contribution:** First comprehensive multi-model, multi-explainer benchmark execution over the *UCI Adult Income* tabular dataset across 300 experimental cells.
* **Key Finding:** Provides empirical mean ranks across 15 complete model blocks:
  * **Fidelity:** SHAP ($\bar{R}=0.8081$) significantly outperforms LIME ($\bar{R}=0.5602$, $p < 0.05$).
  * **Structural vs Attributional Methods:** Anchors and DiCE cannot be evaluated on linear feature attribution scales; they require rule-coverage and counterfactual distance metrics respectively.

---

### Paper E: Pareto Optimization Frontiers & XAI Governance
* **Venue & Status:** Submitted to *Computación y Sistemas (CIC-IPN)* (2026-10-04, Subm. #6783).
* **Core Contribution:** Formulates XAI selection as a Multi-Objective Optimization Problem (MOOP):
  $$\max_{g \in \mathcal{G}} \Big( \text{Fidelity}(g), \text{Stability}(g), -\text{Cost}(g), -\text{Sparsity}(g) \Big)$$
* **Key Finding:** Identifies the non-dominated Pareto frontier:
  * **Healthcare / High-Stakes Audit:** SHAP dominates (maximal stability and fidelity).
  * **Low-Latency Production API:** LIME / TreeSHAP dominate (minimal cost, low sparsity).
  * Provides a formal governance decision framework for deploying XAI in regulated industries.

---

### Paper F: Human & LLM-as-a-Judge Semantic Alignment
* **Venue & Status:** Early development (*Journal of Computer Sciences Institute*).
* **Core Contribution:** Investigates the semantic alignment between quantitative mathematical metrics ($\text{Fidelity}, \text{Stability}$) and human/LLM cognitive evaluations.
* **Key Finding:** Formulates a pre-analysis plan testing whether high-fidelity mathematical attribution vectors correspond to superior human task performance and LLM explanation preference.

---

## 4. Synthesis & Doctoral Defense Narrative

This dissertation unifies these six papers into a cohesive defense thesis:

$$\text{Opaque Model } f(\mathbf{x}) \xrightarrow[\text{Gate 1--3}]{\text{FOM-7 Protocol}} \text{Audited Explanations } g(\mathbf{x}) \xrightarrow[\text{Gate 4--6}]{\text{Pareto Evaluation}} \text{Defensible XAI Governance}$$

1. **The Core Gap:** The unvalidated proliferation of post-hoc explainers created a crisis of evaluation in XAI.
2. **The Methodological Solution (Paper A):** The 7-gate FOM-7 protocol provides mathematical rigor, statistical multiplicity control, and artifact auditability.
3. **Empirical Benchmarking (Papers B, C, D):** Extensive empirical evidence on 300 cells establishes exact performance trade-offs between LIME, SHAP, Anchors, and DiCE across 5 model families.
4. **Decision Governance & Human Alignment (Papers E, F):** Pareto frontier analysis and semantic alignment bridge the gap between mathematical evaluation and real-world deployment.
