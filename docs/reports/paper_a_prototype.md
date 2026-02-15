# A Framework for Rigorous Evaluation of Model-Agnostic Explainability Methods: Multi-Metric Statistical Benchmarking, Operational Protocol, and Reproducibility

**Target Venue**: Journal of Machine Learning Research (JMLR), Datasets and Benchmarks Track  
**Draft Status**: Updated from repository artifacts on February 13, 2026 (latest experiment artifacts dated February 4, 2026)

## Abstract
Evaluating explainability methods requires more than a single faithfulness proxy. We present a modular benchmarking framework centered on quantitative XAI quality metrics: fidelity, stability, sparsity, computational cost, and faithfulness gap, plus an explicit method for operating the framework end-to-end. On the UCI Adult benchmark, we use a staged protocol (EXP1 calibration/reproducibility and EXP2 comparative/robustness benchmarking); the robustness cohort currently contains 250 of 300 planned configurations (83.3% coverage). Across complete model-size blocks ($5$ models, $N \in \{50,100,200\}$), Friedman tests indicate significant method differences for fidelity ($\chi^2=42.12, p=3.78\times10^{-9}$), stability ($\chi^2=43.88, p=1.60\times10^{-9}$), sparsity ($\chi^2=35.64, p=8.92\times10^{-8}$), faithfulness gap ($\chi^2=45.00, p=9.25\times10^{-10}$), and runtime ($\chi^2=27.72, p=4.16\times10^{-6}$). SHAP leads on fidelity/stability, DiCE leads on sparsity, and LIME is generally fastest and most practical outside SVM-KernelSHAP bottlenecks. We release the framework, operation protocol, and artifacts with explicit data-quality caveats for reproducible benchmark use. LLM-based semantic scoring is deferred to a dedicated follow-up study.

## 1. Introduction
XAI evaluation remains fragmented across incompatible metrics and ad hoc setups. Most comparisons over-index on fidelity and omit stability, sparsity, and semantic interpretability. This project operationalizes a benchmark-first approach:
1. A generic trainer/explainer architecture for model-agnostic evaluation.
2. A prescriptive operation method that defines how the framework is run, audited, and reported.
3. Multi-metric quantitative scoring with explicit trade-off analysis.
4. Reproducibility and statistical rigor suitable for benchmark publication.

This revision aligns claims to the current repository state and removes unsupported statements.

## 2. Related Work and Framework Design

### 2.1 Literature-Grounded Design Rationale (Paper A Scope)
The attached literature supports five methodological requirements:
1. **Multi-metric evaluation is necessary**: taxonomic and critical reviews show that fidelity-only evaluation is incomplete and often misleading.
2. **Faithfulness is multi-faceted**: recent work on faithfulness metrics and Shapley theory shows that no single faithfulness proxy is sufficient.
3. **Computational tractability matters**: SHAP approximation complexity and sampling papers motivate explicit runtime and variance reporting.
4. **Benchmark transparency matters**: OpenXAI/Quantus-style toolkits emphasize reproducibility, standardized APIs, and clear artifact accounting.
5. **LLM-judge scores need calibration**: current evidence supports treating LLM judging as a separate, follow-up evaluation track.

### 2.2 Architecture
The framework decouples model training, explanation generation, and evaluation through a registry/factory-based design. Current benchmark coverage includes `logreg`, `rf`, `xgb`, `svm`, and `mlp` backends with `lime`, `shap`, `anchors`, and `dice` explainers.

### 2.3 Metric Suite (Primary)
The quantitative metrics implemented in current artifacts are:
- **Fidelity**: Local agreement between explainer output and model behavior.
- **Stability**: Perturbation consistency of explanations.
- **Sparsity**: Fraction/number of active explanatory features.
- **Cost**: Runtime per explained instance.
- **Faithfulness Gap**: Agreement between explanation importance and model response shifts.

### 2.4 Paper A Operational Outcome: Framework Operation Method (FOM-7)
Paper A contributes not only benchmark findings, but also a reusable operating method for the framework. We formalize this as **FOM-7**, a seven-stage protocol with explicit stage inputs, outputs, and quality gates:
1. Protocol specification.
2. Controlled batch execution.
3. Artifact integrity audit.
4. Metric harmonization and aggregation.
5. Statistical inference and post-hoc localization.
6. Reproducibility characterization.
7. Claim-ready reporting with caveat ledger.

The methodological contribution of Paper A is therefore dual:
- a software framework architecture;
- and an operation method that makes benchmark studies reproducible and reviewable across runs and teams.

## 3. Methodology

### 3.1 Experimental Cohorts and Scope (EXP1 vs EXP2)
We separate evidence into explicit cohorts:
- **EXP1 pilot/calibration** (`experiments/exp1_adult/results`): initial benchmark runs used to verify metric behavior and tune explainer settings.
- **EXP1 reproducibility cohort** (`experiments/exp1_adult/reproducibility`): repeated runs for variance characterization (9 seeds per core configuration).
- **EXP2 comparative cohort** (`experiments/exp2_comparative/results`): a complete $5 \times 4$ model-explainer matrix under a fixed seed.
- **EXP2 robustness cohort** (`experiments/exp2_scaled/results`): multi-seed, multi-sample-size extension for statistical inference under controlled heterogeneity.

Paper A inferential claims are driven by EXP2. EXP1 is retained for calibration and reproducibility reporting.

### 3.2 Research Questions and Hypotheses
We evaluate two research questions:
1. **RQ1**: Do explanation methods differ significantly across complementary technical metrics?
2. **RQ2**: Are metric trade-offs stable across model families and sample sizes?

We formalize RQ1 with metric-specific null hypotheses:
- $H_{0,m}$: all methods have equal median rank for metric $m$ across blocks.
- $H_{1,m}$: at least one method differs for metric $m$.

where $m \in \{$fidelity, stability, sparsity, faithfulness gap, cost$\}$.

### 3.3 Dataset, Preprocessing, and Leakage Controls
The benchmark uses the UCI Adult dataset through the project loader (`src/data_loading/adult.py`), with the following implemented protocol:
- stratified train/test split (`test_size=0.2`, `stratify=y`);
- deterministic split via configured random seed;
- numerical pipeline: `StandardScaler`;
- categorical pipeline: `OneHotEncoder(handle_unknown='ignore', sparse_output=False)`;
- preprocessor fit on training split only, then reused for test transformation.

This prevents test leakage in feature engineering and keeps feature-space alignment stable across model/explainer runs. Feature names are extracted from the fitted column transformer and propagated to explainers and downstream metrics.

### 3.4 Experimental Design and Analysis Units
#### 3.4.1 Factorial grid
- **Models**: `logreg`, `rf`, `xgb`, `svm`, `mlp`.
- **Explainers**: `lime`, `shap`, `anchors`, `dice`.
- **Sample sizes**: $N \in \{50,100,200\}$.
- **Seeds**: $\{42,123,456,789,999\}$.
- **Planned grid**: $5 \times 4 \times 5 \times 3 = 300$ runs.

#### 3.4.2 Sampling within each run
Instance selection is stratified by prediction quadrant (`TP`, `TN`, `FP`, `FN`) using the configured sampling strategy. Metric values are computed per instance and then aggregated at run level.

#### 3.4.3 Units for inference
- **Primary unit**: run-level aggregated metric (mean across evaluated instances).
- **Blocked unit for global non-parametric tests**: `(model, N)`.
- **Paired unit for SHAP-vs-LIME contrasts**: matched `(model, seed, N)` configuration.

This separation avoids pseudo-replication from instance-level values and supports valid repeated-measures comparisons.

### 3.5 Explainer and Metric Operationalization
#### 3.5.1 Explainers
The framework invokes explainers through a unified interface (`src/experiment/runner.py`, `src/experiment/metrics_engine.py`), preserving a common output contract for feature attributions. Method-specific parameters are handled by experiment configuration.

#### 3.5.2 Quantitative metrics
Metrics are computed by `MetricsEngine` and stored per instance:

1. **Cost** (`src/metrics/cost.py`):
- wall-clock time via `perf_counter`;
- tracked as `time_ms`.

2. **Sparsity** (`src/metrics/sparsity.py`):
- active feature ratio using threshold $\tau = 10^{-4}$;
- reported as `nonzero_percentage`.

3. **Fidelity / Faithfulness** (`src/metrics/faithfulness.py`):
- per-feature perturbation and top-$k$ masking formulation;
- with prediction function $f(\cdot)$, input $x$, attribution vector $w$, and baseline $\tilde{x}$:
  - top-$k$ gap:
  $$\Delta_k = | f(x) - f(x_{\text{mask-top-}k}) |$$
  - attribution-drop correlation:
  $$\rho = \text{corr}(|w_i|,\ |f(x)-f(x_{-i})|)$$
- current pipeline maps `fidelity := faithfulness_score := rho`;
- `faithfulness_gap := \Delta_k` is reported separately.

4. **Stability** (`src/metrics/stability.py`):
- generate $T$ perturbed inputs $x^{(t)} = x + \epsilon^{(t)}$, with $\epsilon^{(t)} \sim \mathcal{N}(0,\sigma^2)$;
- recompute explanations and evaluate pairwise cosine similarity:
  $$S = \frac{2}{T(T-1)} \sum_{a<b} \cos(e^{(a)}, e^{(b)})$$
- defaults are configurable (`stability_perturbations`, `stability_noise_level`).

#### 3.5.3 Semantic metrics (deferred)
LLM-based semantic scoring exists as an experimental module in the repository but is not part of the primary inferential claims for Paper A. It is treated as future work pending dedicated calibration against human annotations and stronger external-validity controls.

### 3.6 Artifact Integrity and Coverage Protocol
To prevent optimistic bias from silent failures, we explicitly audit:
- completed configurations,
- missing configurations,
- malformed artifacts,
- coverage imbalance by method-model pair.

Current inventory in this repository state:
- `experiments/exp1_adult/results`: 29 files (4 core runs, 24 LIME tuning runs, 1 diagnostic run).
- `experiments/exp1_adult/reproducibility`: 36 core repeated runs (+1 test artifact excluded from analysis).
- `experiments/exp2_comparative/results`: 20 files (complete $5 \times 4$ matrix).
- `experiments/exp2_scaled/results`: 250 files for a planned 300-run robustness grid.
- malformed JSON identified at `experiments/exp2_scaled/results/svm_shap/seed_999/n_200/results.json`.

All global-method comparisons in this manuscript are computed on complete `(model, N)` blocks within the EXP2 robustness cohort; focused pairwise analyses are computed on explicitly matched subsets.

### 3.7 Statistical Analysis Pipeline
#### 3.7.1 Global method comparison
For each metric, we run Friedman tests over blocked comparisons (`model x N`) with methods as treatments.

#### 3.7.2 Post-hoc localization
When Friedman is significant, we run Nemenyi pairwise post-hoc tests to control family-wise error and localize which method pairs differ.

#### 3.7.3 Focused pairwise SHAP-vs-LIME test
For matched configurations (`model`, `seed`, `N`), we run Wilcoxon signed-rank tests on:
- fidelity,
- stability,
- sparsity,
- faithfulness gap,
- cost.

#### 3.7.4 Uncertainty reporting
Where available in project outputs, we report:
- mean and standard deviation,
- coefficient of variation (CV),
- confidence intervals from both $t$-distribution and bootstrap procedures (`src/analysis/confidence.py`).

### 3.8 Reproducibility Protocol
Reproducibility is handled at three levels:
1. **Configuration determinism**: fixed seeds and declared experiment configs.
2. **Artifact determinism**: structured outputs (`results.json`, CSV summaries, analysis JSON).
3. **Variance characterization**: repeated-run CV reporting (`reproducibility_report.csv`).

We explicitly separate:
- measured evidence in committed artifacts,
- from planned but not yet completed extensions (e.g., semantic human-calibrated evaluation).

### 3.9 Validity Threats and Mitigations
1. **Incomplete factorial coverage**: mitigated by block-complete analysis and explicit inventory reporting.
2. **Runtime heterogeneity across explainers**: mitigated by treating cost as first-class metric, not a footnote.
3. **Metric-definition ambiguity**: mitigated by code-level operational definitions tied to implementation files.

### 3.10 Framework Operation Method (FOM-7): Executable Protocol
To make the operation method concrete, we define each stage with required artifacts and a pass/fail gate.

| Stage | Objective | Required Artifacts | Gate (must pass before next stage) |
| :--- | :--- | :--- | :--- |
| S1: Protocol specification | Freeze study design before execution | Config files under `configs/experiments/`, explicit model/explainer/seed/sample grid | Planned run count and factors are fully enumerated |
| S2: Controlled execution | Produce run artifacts under fixed configs | Per-run `results.json`, logs, `outputs/batch_manifest.json` | Each planned config has terminal status (`success`, `failed`, or `skipped`) |
| S3: Integrity audit | Detect silent data-quality failures | Missing-run report (`scripts/check_missing_results.py`), JSON parse audit | Missing and malformed artifacts are explicitly listed |
| S4: Harmonization and aggregation | Convert heterogeneous results into analysis-ready tables | Aggregated CSV/JSON summaries (e.g., `outputs/batch_results.csv`) | All retained runs contain required primary metrics |
| S5: Statistical inference | Quantify significance and pairwise differences | Friedman, Nemenyi, and Wilcoxon outputs with metric-level p-values | Inferential outputs are complete for all primary metrics |
| S6: Reproducibility characterization | Quantify variance under repeated runs | `experiments/exp1_adult/reproducibility/reproducibility_report.csv` | CV and dispersion are reported for each core metric |
| S7: Claim-ready reporting | Bind manuscript claims to verifiable artifacts | Manuscript tables/figures + caveat list + artifact inventory | Every quantitative claim is traceable to a versioned artifact |

Reference command sequence used by this repository implementation:
1. `python3 scripts/run_batch_experiments.py --config-dir configs/experiments/exp2_scaled --output outputs/batch_results.csv --parallel`
2. `python3 scripts/check_missing_results.py`
3. `python3 scripts/quick_summary.py`
4. `python3 scripts/full_summary.py`
5. `python3 scripts/run_reproducibility_study.py --config-dir configs/experiments --pattern "exp1_adult_*.yaml" --output-dir experiments/exp1_adult/reproducibility`

These commands are implementation-specific realizations of FOM-7. The method itself is platform-agnostic: any implementation is acceptable if it satisfies the same stage artifacts and quality gates.

## 4. Results

### 4.1 Global Trade-offs (EXP2 robustness: 15 complete model-size blocks)

| Method | Fidelity | Stability | Sparsity | Faithfulness Gap | Time (ms) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| SHAP | 0.8176 | 0.7377 | 0.2264 | 0.4474 | 685220.23 |
| LIME | 0.5602 | 0.0144 | 0.0846 | 0.3342 | 3660.68 |
| Anchors | 0.3853 | 0.0006 | 0.0928 | 0.2382 | 25326.92 |
| DiCE | 0.1716 | 0.3602 | 0.0164 | 0.0988 | 16306.50 |

Key interpretation:
- SHAP dominates fidelity and stability but has extreme runtime variance (notably SVM).
- LIME offers strong practical speed with moderate fidelity.
- DiCE is sparsest, but fidelity is lowest.
- Anchors under current settings show near-zero stability and high runtime.

### 4.2 Statistical Significance (Friedman across methods)

| Metric | Statistic | p-value | Significant |
| :--- | ---: | ---: | :--- |
| Fidelity | 42.12 | 3.78e-09 | Yes |
| Stability | 43.88 | 1.60e-09 | Yes |
| Sparsity | 35.64 | 8.92e-08 | Yes |
| Faithfulness Gap | 45.00 | 9.25e-10 | Yes |
| Cost | 27.72 | 4.16e-06 | Yes |

All primary metrics reject equal-performance null hypotheses.

### 4.3 Focused SHAP vs LIME Comparison (paired, 45 matched configs on `logreg/rf/xgb`)

| Metric | SHAP Mean | LIME Mean | Wilcoxon p-value |
| :--- | ---: | ---: | ---: |
| Fidelity | 0.8112 | 0.5556 | 5.68e-14 |
| Stability | 0.8013 | 0.0154 | 5.68e-14 |
| Sparsity | 0.3156 | 0.0845 | 5.68e-14 |
| Faithfulness Gap | 0.3924 | 0.3408 | 5.68e-14 |
| Cost (ms) | 1258.72 | 210.45 | 2.29e-06 |

Interpretation:
- SHAP outperforms LIME on fidelity/stability/faithfulness gap.
- LIME remains significantly cheaper computationally on these shared model families.

### 4.4 Reproducibility Snapshot (EXP1 repeated runs; `reproducibility_report.csv`)
- Fidelity CV <= 0.0634 across all four reported baselines.
- Stability CV <= 0.0826 across all four reported baselines.
- Sparsity CV <= 0.0441 and faithfulness-gap CV <= 0.0358.
- Cost CV reaches 0.225 for SHAP variants, indicating runtime instability relative to quality metrics.

## 5. Validity and Reporting Caveats
1. The EXP2 robustness cohort is incomplete (50 missing runs) with one malformed result file; conclusions should be presented with this coverage qualifier.
2. Runtime comparisons are sensitive to explainer implementation (e.g., TreeSHAP vs KernelSHAP) and hardware.
3. Semantic evaluation is intentionally out of scope for Paper A and reserved for a separate calibrated study.

## 6. JMLR-Track Positioning
This work fits the Datasets and Benchmarks track if positioned as:
1. A reproducible XAI benchmark framework with explicit artifact lineage and failure accounting.
2. A multi-metric evaluation protocol with robust non-parametric testing.
3. A reusable operation method (FOM-7) that standardizes how benchmark studies are executed and audited.
4. A clearly scoped quantitative benchmark with deferred semantic-evaluation extension.

## 7. Conclusion
The current evidence supports a clear multi-objective trade-off frontier: SHAP leads fidelity/stability, LIME leads practical runtime, and DiCE leads sparsity. Beyond these empirical findings, Paper A contributes a concrete operation method (FOM-7) for running, auditing, and reporting XAI benchmark studies. The framework already discriminates methods with high statistical confidence, and Paper A should focus on this quantitative benchmark core plus its operational protocol contribution.

## 8. Methodology-Driving References (from attached set)
- `14708_XAI_Evaluation_Metrics__Taxonomies__Concepts_and_Applications__INES_2023_-7.pdf`
- `Evaluating the necessity of the multiple metrics for assessing explainable AI A critical examination.pdf`
- `Evaluation of Neural Network Explanations and Beyond.pdf`
- `Quantus- An Explainable AI Toolkit for Responsible Evaluation of Neural Network Explanations and Beyond.pdf`
- `OpenXAI- Towards a Transparent Evaluation of Post hoc Model Explanations.pdf`
- `Attribution-based Explanations that Provide Recourse.pdf`
- `Consensus on Feature Attributions in the Rashomon Set.pdf`
- `On the Complexity of SHAP-Score-Based Explanations.pdf`
- `Sampling Permutations for Shapley Value Estimation.pdf`
- `The Faithful Shapley Interaction Index.pdf`
- `On the Faithfulness of Vision Transformer Explanations.pdf`
