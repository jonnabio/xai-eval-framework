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
We intentionally organize evidence into staged cohorts to separate *development*, *verification*, and *confirmatory inference*. This prevents circular analysis (tuning and claiming on the same evidence) and makes claim provenance auditable.

| Cohort | Objective | Design characteristics | Role in Paper A |
| :--- | :--- | :--- | :--- |
| **EXP1 pilot/calibration** (`experiments/exp1_adult/results`) | Debug and calibrate the evaluation stack before large-scale inference | Small core run set plus targeted tuning artifacts | Used for implementation sanity, metric behavior checks, and explainer parameter calibration; **not used as primary inferential evidence** |
| **EXP1 reproducibility** (`experiments/exp1_adult/reproducibility`) | Quantify run-to-run variance under repeated seeds | 9 repeated runs per core configuration | Used to report coefficient of variation (CV) and reproducibility stability profiles |
| **EXP2 comparative** (`experiments/exp2_comparative/results`) | Establish full method/model coverage under controlled budget | Complete $5 \times 4$ model-explainer matrix at fixed seed | Used as balanced breadth check and baseline comparative layer |
| **EXP2 robustness** (`experiments/exp2_scaled/results`) | Support cross-method inference under controlled heterogeneity | Multi-seed ($5$) and multi-sample-size ($N \in \{50,100,200\}$) design | **Primary inferential cohort** for Friedman/Nemenyi/Wilcoxon analyses |

Methodological rationale for EXP1/EXP2 separation:
1. **Tuning-evaluation separation**: EXP1 absorbs calibration work so EXP2 can function as confirmatory evidence.
2. **Validity layering**: EXP1 addresses implementation validity and reproducibility; EXP2 addresses comparative and inferential validity.
3. **Failure transparency**: explicit cohort boundaries make missing/invalid artifacts visible instead of silently mixed into pooled summaries.
4. **Claim discipline**: claims are scoped to cohorts that are actually fit-for-purpose (e.g., significance claims from EXP2 robustness only).

Operationally, this mirrors the train/dev/test principle in predictive modeling, but adapted for XAI evaluation systems: **EXP1 = development and reliability qualification**, **EXP2 = comparative and inferential qualification**.

Accordingly, Paper A inferential claims are driven by EXP2 (especially block-complete analyses in `exp2_scaled`), while EXP1 is used for calibration and reproducibility characterization.

### 3.2 Research Questions and Hypotheses
This section defines the inferential target of the study and makes explicit what is treated as confirmatory versus robustness-oriented evidence.

Let:
- $\mathcal{K}$ be the set of explanation methods;
- $\mathcal{B}$ be the set of evaluation blocks, where each block is a `(model, N)` context;
- $y_{k,b,m}$ be the run-level aggregated score for method $k$, block $b$, and metric $m$.

We study the metric set
$m \in \{$fidelity, stability, sparsity, faithfulness gap, cost$\}$.
These metrics intentionally span distinct constructs (faithfulness, consistency, cognitive compactness, and computational burden), so no single metric is interpreted as sufficient for global method superiority.

We evaluate two research questions:
1. **RQ1 (Method separation)**: Do explanation methods differ significantly on each technical metric when compared over repeated evaluation blocks?
2. **RQ2 (Trade-off stability)**: Are method trade-offs stable across context modifiers (model family and sample size), or do they shift materially by context?

For **RQ1**, the confirmatory metric-wise hypotheses are:
- $H_{0,m}^{(1)}$: all methods have equal median rank for metric $m$ across blocks.
- $H_{1,m}^{(1)}$: at least one method differs in median rank for metric $m$.

Interpretation of RQ1:
- rejection of $H_{0,m}^{(1)}$ implies the benchmark can discriminate methods on metric $m$;
- non-rejection implies that observed differences are not strong enough, given current variance and coverage, to support method-level separation for $m$.

For **RQ2**, we formalize stability as *context-invariance of relative method behavior*, using two complementary hypotheses:
- $H_{0,m}^{(2a)}$: the relative ordering of methods for metric $m$ is stable across blocks (no systematic context-driven rank shifts).
- $H_{1,m}^{(2a)}$: method ordering for metric $m$ changes across blocks (context-dependent rank shifts exist).
- $H_{0,m}^{(2b)}$: pairwise method differences on metric $m$ do not vary systematically with model family or sample size.
- $H_{1,m}^{(2b)}$: pairwise method differences on metric $m$ vary systematically with model family and/or sample size.

Interpretation of RQ2:
- this is not a question of whether trade-offs exist (they generally do), but whether they are **stable enough to support portable guidance**;
- practical instability is flagged by context-dependent rank reversals and/or large shifts in pairwise effect magnitude across block strata.

Methodological scoping:
- RQ1 is the primary confirmatory layer for statistical discrimination.
- RQ2 is the robustness layer linking statistical outcomes to external validity and deployment relevance.

### 3.3 Dataset, Preprocessing, and Leakage Controls
The benchmark uses the Adult Income dataset (UCI Census Income) through a dedicated data pipeline (`src/data_loading/adult.py`) with explicit provenance, cleaning, and transformation controls.

#### 3.3.1 Data provenance and schema control
The loader implements a source hierarchy and cache validation protocol:
1. primary source: OpenML Adult v2 (`data_id=1590`);
2. fallback source: direct UCI files (`adult.data`, `adult.test`);
3. cache integrity: checksum-validated parquet cache with metadata (`shape`, `columns`, `source`, `download_date`, package versions).

Schema is fixed to 15 columns:
- **Target**: `income`;
- **Numeric predictors** (6): `age`, `fnlwgt`, `education-num`, `capital-gain`, `capital-loss`, `hours-per-week`;
- **Categorical predictors** (8): `workclass`, `education`, `marital-status`, `occupation`, `relationship`, `race`, `sex`, `native-country`.

The cleaning stage performs:
- whitespace normalization for string fields;
- normalization of missing markers (`?`) to `NaN`;
- target canonicalization and binary encoding (`<=50K`/`<=50K.` -> `0`, `>50K`/`>50K.` -> `1`);
- duplicate-row removal;
- numeric type coercion for all six continuous/count features.

In the current artifact state, the cleaned dataset contains 48,790 rows (after duplicate/invalid-target filtering).

#### 3.3.2 Split protocol and deterministic execution
Data are split with a stratified holdout protocol:
- `train_test_split(test_size=0.2, stratify=y, random_state=seed)`.

This guarantees:
- class-prior preservation between train/test;
- exact split reproducibility for a given seed;
- controlled seed variation across robustness cohorts without changing the split algorithm itself.

For the default seed configuration, this corresponds to 39,032 training rows and 9,758 test rows, with nearly identical class prevalence across splits.

#### 3.3.3 Preprocessing design and feature-space construction
Preprocessing is implemented as a `ColumnTransformer` with two branches:
1. numeric branch: `StandardScaler` applied to the six numeric features;
2. categorical branch: `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` applied to the eight categorical features.

Important implementation details:
- one-hot encoding is learned on the training partition only;
- unseen test categories are ignored (no transformation failure);
- categorical missing values are represented as explicit categories by the encoder (rather than row deletion);
- output is dense to simplify downstream model/explainer interoperability.

With the current training vocabulary, the categorical branch yields 102 encoded columns; combined with six scaled numeric columns, the processed design matrix has 108 features.

#### 3.3.4 Leakage controls and cross-stage alignment
Leakage prevention is enforced at multiple levels:
1. the preprocessor is fitted on training data only and then frozen for test transformation;
2. feature names are extracted from the fitted transformer and propagated to explainers/metrics to avoid attribution-index drift;
3. when available, `ExperimentRunner` loads the persisted training preprocessor artifact (`preprocessor.pkl` / `preprocessor.joblib`) from the model directory and reuses it for experiment execution.

The third control is critical: it ensures that explanation generation and metric evaluation operate in exactly the same transformed feature space used by the trained black-box model.

#### 3.3.5 Construct caveats relevant to Adult
Adult is appropriate for tabular XAI benchmarking but carries known socio-demographic imbalance and proxy-feature concerns (e.g., `sex`, `race`, `native-country`). Therefore, this section establishes preprocessing and leakage rigor, but does not claim that preprocessing removes fairness-related construct risks; those remain part of validity considerations.

### 3.4 Experimental Design and Analysis Units
#### 3.4.1 Design type and inferential target
The EXP2 comparative study is structured as a crossed, repeated-seed factorial design with:
- model family $g \in \mathcal{G}=\{$`logreg`, `rf`, `xgb`, `svm`, `mlp`$\}$;
- explainer $k \in \mathcal{K}=\{$`lime`, `shap`, `anchors`, `dice`$\}$;
- seed $s \in \mathcal{S}=\{42,123,456,789,999\}$;
- sampling intensity $n \in \mathcal{N}=\{50,100,200\}$.

Each executed configuration defines one run-level observation for each metric $m$:
$y_{g,k,s,n,m}$.

Because seed coverage is partially unbalanced in the realized artifact set, confirmatory inference is built on block-level summaries. For block $b=(g,n)$:
$$
\bar{y}_{k,b,m}=\frac{1}{|S_{k,b}|}\sum_{s \in S_{k,b}} y_{g,k,s,n,m},
$$
where $S_{k,b}\subseteq\mathcal{S}$ is the set of analyzable seeds for method $k$ in block $b$. This construction ensures that each block contributes one value per method, preventing methods with more successful seed executions from being over-weighted in omnibus tests.

#### 3.4.2 Planned matrix versus realized execution
The planned robustness matrix contains:
$$
|\mathcal{G}|\times|\mathcal{K}|\times|\mathcal{S}|\times|\mathcal{N}|=5\times4\times5\times3=300
$$
run configurations (`configs/experiments/exp2_scaled/manifest.yaml`).

In the current repository snapshot:
- 250 result files are present under `experiments/exp2_scaled/results`;
- 233 are analyzable (non-empty `instance_evaluations`);
- 16 are structurally empty;
- 1 file is malformed JSON.

For global method comparisons, we retain only model-size blocks with at least one analyzable run for each of the four methods. This yields 15/15 complete blocks (`5` models x `3` sample sizes), preserving full model-size coverage at the block level despite missing seed-level replications.

Within those complete blocks, per-method seed availability is heterogeneous:
- SHAP: 2-5 seeds per block (mean $\approx 4.33$),
- LIME: 5 seeds per block (mean $=5.00$),
- Anchors: 1-5 seeds per block (mean $\approx 2.87$),
- DiCE: 2-5 seeds per block (mean $\approx 3.33$).

No imputation is applied for missing runs; all inference is conditional on observed analyzable artifacts.

#### 3.4.3 Within-run sampling protocol and realized exposure
Each run uses stratified error-quadrant sampling (`src/evaluation/sampler.py`):
- `TP` (true positive),
- `TN` (true negative),
- `FP` (false positive),
- `FN` (false negative).

The configuration parameter `samples_per_class = N` is interpreted as **target samples per quadrant**, so the nominal run size is $4N$ instances.

Realized run size can be lower when:
1. a quadrant has fewer than $N$ available test instances for a given model/seed; or
2. some sampled instances fail during explainer execution and are dropped at evaluation time.

Empirically (EXP2 analyzable runs), realized run sizes range from 27 to 800 instances (median 400). Across all retained instance evaluations (103,577 total), quadrant proportions remain close to balanced:
- TP: 26,523 (25.6%),
- TN: 26,050 (25.2%),
- FP: 25,200 (24.3%),
- FN: 25,804 (24.9%).

This near-balance is important because it limits confounding of metric summaries by error-type composition.

#### 3.4.4 Analysis units and anti-pseudoreplication strategy
The design distinguishes four analytical levels:
1. **Instance level**: raw metric outputs for each explained case.
2. **Run level**: per-configuration aggregation of instance metrics ($y_{g,k,s,n,m}$).
3. **Block level**: per-method averages within `(model, N)` blocks ($\bar{y}_{k,b,m}$), used for omnibus non-parametric comparisons.
4. **Matched-pair level**: explicit SHAP-LIME pairs on shared `(model, seed, N)` cells.

Global Friedman/Nemenyi analyses are performed on a $15 \times 4$ block-method matrix (15 model-size blocks, 4 methods), which avoids pseudo-replication from instance-level observations and avoids double-counting seed replicates as independent blocks.

For focused SHAP-vs-LIME contrasts, matched analyzable cells are:
- 65 pairs when all five models are allowed;
- 45 pairs for the restricted `logreg`/`rf`/`xgb` subset used in the primary paired analysis.

#### 3.4.5 Retention and exclusion rules
To make the inferential dataset reproducible and auditable, runs are handled under fixed inclusion logic:
1. parseable JSON artifact required (malformed files excluded);
2. non-empty per-instance evaluations required for run-level analysis;
3. no synthetic completion of missing runs or seeds;
4. omnibus method tests restricted to block-complete contexts;
5. paired tests restricted to explicitly matched SHAP-LIME configurations.

These rules separate **experimental design intent** (300-run full factorial) from **inferential design realization** (artifact-qualified subsets), which is critical for defensible claims under incomplete execution.

### 3.5 Experimental Design Protocol (Replication Specification)
This section provides the executable design specification used for Paper A and is intended to be sufficient for independent replication without implementation guesswork.

#### 3.5.1 Purpose and hypotheses linkage
Section 3.5 operationalizes the confirmatory and robustness questions defined in Section 3.2:
1. **RQ1** (method separation): test whether explainer methods differ on each primary quantitative metric.
2. **RQ2** (trade-off stability): test whether method trade-offs are stable across model family and sampling intensity.

Accordingly, the protocol is built to isolate method effects while controlling data representation, sampling logic, and metric computation paths. Reliability and faithfulness are treated as system properties of the full `(model, explainer, data, metric)` pipeline rather than of explainers in isolation.

#### 3.5.2 Experimental factors and conditions
Independent variables are defined in the EXP2 configuration artifacts (`configs/experiments/exp2_comparative`, `configs/experiments/exp2_scaled`, `configs/experiments/exp2_scaled/manifest.yaml`):

1. **Dataset** (fixed): Adult Income (`dataset: adult`).
2. **Model family**: `logreg`, `rf`, `xgb`, `svm`, `mlp`.
3. **Explainer method**: `lime`, `shap`, `anchors`, `dice`.
4. **Seed**: $\{42,123,456,789,999\}$ (EXP2 robustness).
5. **Sampling intensity**: `samples_per_class = N`, with $N \in \{50,100,200\}$ (EXP2 robustness); `N=10` (EXP2 comparative).
6. **Perturbation regime for stability**: Gaussian input noise with `stability_perturbations=15` (EXP2 robustness) and `stability_noise_level=0.1` (default from `src/experiment/config.py`, because not overridden in EXP2 YAML).
7. **Method-specific secondary flag**: `counterfactual=true` when explainer is `dice`; otherwise `false`.

Planned EXP2 robustness design size is $5\times4\times5\times3=300$ configurations (see Table X: Design Matrix).

**Ablation status (explicit scope boundary)**:
1. Paper A is a comparative benchmark, not a component-ablation study.
2. No component-removal or hyperparameter-factor ablation enters any confirmatory table or hypothesis test.
3. EXP1 tuning artifacts are treated as calibration records only and are excluded from inferential analysis sets.
4. Ablation-based causal attribution of performance differences is reserved for a separate extension study (Paper B).

#### 3.5.3 Controls and baselines
Within each matched cell `(model, seed, N)`, fairness controls are:
1. same black-box model artifact path (`experiments/exp1_adult/models/*.joblib`);
2. same transformed feature space via reused preprocessor artifact (`preprocessor.pkl`/`preprocessor.joblib`);
3. same split/sampling seeds for data partition and TP/TN/FP/FN sampling;
4. same sampled evaluation protocol and metric engine (`src/experiment/metrics_engine.py`);
5. same primary metric set and aggregation logic.

Comparator set in Paper A is `lime`, `shap`, `anchors`, `dice` (no method is treated as “oracle”). Practical baselines are therefore cross-method.

Controls currently **not included**:
- random-attribution sanity baseline;
- model-parameter randomization sanity check;
- label-randomization sanity check.

Because these sanity controls are absent, Paper A claims are restricted to **relative method performance under trained-model conditions**. The manuscript does not claim explanation validity under label/model randomization perturbations.

#### 3.5.4 Data protocol
Data provenance, preprocessing, and leakage controls are defined in Section 3.3 and implemented in `src/data_loading/adult.py`.

Replicable protocol:
1. Clean Adult dataset (whitespace normalization, `?` to `NaN`, canonical binary target mapping, duplicate removal).
2. Stratified split: `train_test_split(test_size=0.2, stratify=y, random_state=seed)`.
3. Fit preprocessor on training split only (if no persisted preprocessor supplied).
4. Transform train/test with the same fitted transformer.
5. Extract transformed feature names and propagate to explainers/metrics.
6. Build evaluation subset via TP/TN/FP/FN stratified sampling (`src/evaluation/sampler.py`) with target size $N$ per quadrant.

For seed `42`, the split is:
- train: 39,032 rows (`y=0`: 29,687; `y=1`: 9,345);
- test: 9,758 rows (`y=0`: 7,422; `y=1`: 2,336).

Nominal per-run sample size is $4N$; realized size may be lower when some quadrants have fewer than $N$ available instances.

#### 3.5.5 Model training protocol
Paper A EXP2 runs load **frozen pre-trained models** from EXP1 artifacts; models are not retrained inside EXP2.

Model objective (all families): binary classification of income class (`<=50K` vs `>50K`).

Loaded model families and persisted hyperparameters (from model artifacts/configs):
1. `logreg`: `solver=lbfgs`, `max_iter=1000`, `random_state=42`.
2. `rf`: `n_estimators=50`, `max_depth=15`, `min_samples_leaf=1`, `class_weight=balanced_subsample`, `random_state=42`.
3. `xgb`: `n_estimators=100`, `max_depth=6`, `learning_rate=0.1`, `objective=binary:logistic`, `eval_metric=logloss`, `random_state=42`.
4. `svm`: `kernel=rbf`, `C=1.0`, `gamma=scale`, `probability=true`, `random_state=42`.
5. `mlp`: `hidden_layer_sizes=[100]`, `activation=relu`, `solver=adam`, `max_iter=500`, `random_state=42`.

Early stopping:
- supported by `XGBoostTrainer` only when validation data are explicitly passed;
- not active in the saved EXP2 model artifacts (no validation set passed in the model-generation scripts used for persisted artifacts).

Calibration:
- no explicit probability calibration stage (`Platt`, `isotonic`, or post-hoc calibration wrapper) is applied.

Calibration interpretation policy:
1. all methods are evaluated on the same fixed uncalibrated model outputs within each matched cell;
2. inferential claims are comparative (method ordering/trade-offs), not claims about calibrated probability quality;
3. no calibration-dependent claim is made in Paper A.

Randomness handling:
- training-time model randomness is fixed at seed `42` in saved model artifacts;
- EXP2 seed variation changes split/sampling and explainer stochasticity, but does not retrain models.

#### 3.5.6 Explanation generation protocol
All explainers are called through `ExplainerWrapper.explain_instance` (single-instance interface) and timed per call.

Common input representation:
1. dense transformed feature vector (108-dimensional in current Adult vocabulary);
2. model prediction interface requiring `predict_proba` for probability-based methods/metrics.

Method-specific protocol:
1. **SHAP** (`src/xai/shap_tabular.py`)
- `explainer_type=tree` for `rf/xgb`; `kernel` for `svm/mlp/logreg` (from EXP2 configs);
- background sample size `n_background_samples=50`;
- tree mode uses `feature_perturbation="interventional"` and `model_output="probability"`;
- class-1 attribution is retained for binary tasks;
- if TreeExplainer fails for model-serialization reasons, fallback is KernelExplainer.

2. **LIME** (`src/xai/lime_tabular.py`)
- `num_samples=1000` and `num_features=10` via config schema/EXP2 configs;
- `kernel_width=3.0` in EXP2 configs;
- `discretize_continuous=False` (wrapper default);
- class-1 local explanation map is converted to dense feature vector.

3. **Anchors** (`src/xai/anchors_wrapper.py`)
- fit `AnchorTabular` on transformed training data;
- per-instance rule extraction at precision threshold `0.95`;
- anchor membership converted to binary feature-importance vector.

4. **DiCE** (`src/xai/dice_wrapper.py`)
- DiCE backend `method="random"` (wrapper default);
- counterfactual target class `desired_class="opposite"`;
- feature-importance proxy is absolute difference between original instance and generated counterfactual.

Implementation caveats requiring explicit disclosure:
1. `anchors` threshold is hardcoded at `0.95` inside wrapper call and currently not read from YAML parameter.
2. `dice` YAML parameter `num_counterfactuals` is not propagated; implementation currently uses `total_CFs=1`.

Parameter-binding policy used for all reported runs:
1. SHAP: `explainer_type` and `n_background_samples` are read from YAML and applied.
2. LIME: `kernel_width` from `explainer.params` is applied; `num_samples` and `num_features` are bound via schema fields (`explainer.num_samples`, `explainer.num_features`) with defaults `1000/10`; duplicate entries under `params` are dropped in runner preprocessing.
3. Anchors: YAML `threshold` is currently not consumed by runtime; effective threshold is fixed at `0.95`.
4. DiCE: YAML `num_counterfactuals` is currently not consumed by runtime; effective setting is `total_CFs=1` with backend `method="random"`.

These bindings define the effective treatment settings and therefore the exact conditions under which EXP2 claims are valid.

Runtime constraints:
- per-instance cost is measured with `perf_counter` around explanation generation;
- no explicit per-run timeout or memory cap is encoded in experiment YAML;
- batch execution uses process-level parallelism (`scripts/run_batch_experiments.py`) and forces one evaluation worker per experiment process to avoid nested process explosion (`src/experiment/batch_runner.py`).

Runtime budget profile over analyzable EXP2 runs (`outputs/analysis/paper_a_exp2_stats/exp2_run_level_metrics.csv`):

| Method | Runs | Mean Cost (ms) | Median (ms) | P95 (ms) | Max (ms) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| SHAP | 65 | 503870.23 | 1098.11 | 1603727.03 | 9393990.21 |
| LIME | 75 | 3660.68 | 65.73 | 13192.05 | 85825.65 |
| Anchors | 43 | 28762.43 | 34063.36 | 64568.75 | 67997.67 |
| DiCE | 50 | 15337.17 | 9759.79 | 34172.81 | 37164.19 |

#### 3.5.7 Evaluation metrics and measurement procedure
Metrics are computed per instance in `MetricsEngine`, then aggregated.

Primary metrics used for confirmatory claims:
1. **Cost** (`cost`): wall-clock explanation time in milliseconds.
2. **Sparsity** (`sparsity`): proportion of active features, threshold $\tau=10^{-4}$.
3. **Fidelity proxy** (`fidelity`): operationalized as faithfulness correlation score.
4. **Faithfulness gap** (`faithfulness_gap`): absolute prediction change after masking top-$k$ features ($k=5$).
5. **Stability** (`stability`): mean pairwise cosine similarity under Gaussian perturbations.

Faithfulness computation (`src/metrics/faithfulness.py`), with model score function $f$, instance $x$, baseline $\tilde{x}$, and attribution weights $w$:
$$
\Delta_k = \left| f(x)-f(x_{\text{mask-top-}k}) \right|,
\qquad
\rho = \mathrm{corr}\left(|w_i|,\left|f(x)-f(x_{-i})\right|\right).
$$
Pipeline mapping is:
- `fidelity := rho`;
- `faithfulness_gap := \Delta_k`.

Stability computation (`src/metrics/stability.py`):
$$
x^{(t)} = x + \epsilon^{(t)}, \ \epsilon^{(t)} \sim \mathcal{N}(0,\sigma^2),
\qquad
S=\frac{2}{T(T-1)}\sum_{a<b}\cos\left(e^{(a)},e^{(b)}\right),
$$
with $T=\texttt{stability\_perturbations}$ and $\sigma=\texttt{stability\_noise\_level}$.

Secondary metric track:
- `cf_sensitivity` (counterfactual sensitivity recall-style metric) is computed when `counterfactual=true` and DiCE counterfactuals are available;
- domain-alignment metric is implemented but disabled in EXP2 configs (`domain=false`).

Aggregation levels:
1. instance-level metric vectors;
2. run-level aggregates (`mean`, `std`, `min`, `max`, `count`) in `results.json`;
3. block-level method summaries over `(model, N)` for omnibus tests.

**Cost/EEU note**: EEU is specified in design artifacts (`experiments/exp1_adult/configs/metrics/exp1_metrics_config.yaml`) but is not computed in EXP2 runtime because memory/model-call instrumentation is not emitted in run artifacts. Therefore:
1. confirmatory cost inference uses wall-clock milliseconds only;
2. EEU is excluded from hypothesis tests, tables, and figures in Paper A.

#### 3.5.8 Statistical analysis plan
Confirmatory inference uses the retained inferential dataset defined by artifact qualification rules (Section 3.4.5, Section 3.6).

Planned and realized run structure:
1. planned EXP2 robustness grid: 300 runs;
2. present artifacts: 250;
3. analyzable runs: 233;
4. global omnibus analysis set: 15 complete `(model, N)` blocks.

Hypothesis tests:
1. **Global multi-method test (RQ1)**: Friedman test per metric across methods with blocks `(model, N)`.
2. **Post-hoc localization**: Nemenyi pairwise comparisons when Friedman rejects the null.
3. **Focused paired comparison**: Wilcoxon signed-rank test for SHAP vs LIME on matched `(model, seed, N)` cells.

Multiple-comparison control:
- Nemenyi procedure controls family-wise error for all method pairs under Friedman framework.

Uncertainty reporting:
- mean, standard deviation, and coefficient of variation (CV);
- confidence intervals via both $t$-distribution and bootstrap (`src/analysis/confidence.py`) where generated.

Effect sizes:
- Friedman-level effect size is reported as Kendall’s $W$ in the EXP2 inference export;
- paired SHAP-LIME effect size is reported as Cohen’s $d_z$ in the EXP2 Wilcoxon exports.

#### 3.5.9 Robustness and sensitivity analyses
Robustness is assessed along three implemented axes:
1. **Seed heterogeneity**: five seeds in EXP2 robustness.
2. **Sample-size heterogeneity**: $N \in \{50,100,200\}$ per error quadrant.
3. **Perturbation robustness**: Gaussian-noise stability metric (`T=15`, $\sigma=0.1$ by default).

Additional implemented sensitivity view:
- reproducibility CV study in EXP1 repeated-seed cohort (`experiments/exp1_adult/reproducibility/reproducibility_report.csv`).

Not included in current Paper A core protocol:
- adversarial perturbation attacks;
- causal-intervention benchmarks beyond proxy counterfactual sensitivity.

Adversarial scope boundary:
- no adversarial stress campaign is part of Paper A; robustness claims are limited to seed, sample-size, and Gaussian-noise perturbation dimensions.

Quantitative robustness interpretation rule used in reporting:
1. directional consistency: sign of SHAP-LIME median difference must match between the 45-cell primary set and 65-cell all-model sensitivity set;
2. inferential consistency: Holm-adjusted significance decision must not change between these two matched-set analyses.

If either condition fails for a metric, that metric is reported as sensitivity-unstable rather than robust.

#### 3.5.10 Reproducibility package and rerun instructions
Reproducibility artifacts currently available in repository:
1. source code (`src/`, `scripts/`);
2. experiment configs (`configs/experiments/`);
3. model and preprocessor artifacts (`experiments/exp1_adult/models/`);
4. per-run outputs (`experiments/exp2_scaled/results/**/results.json`, `metrics.csv`);
5. batch manifest and aggregate exports (`outputs/batch_manifest.json`, `outputs/batch_results.csv`);
6. figure-generation script and outputs (`scripts/generate_paper_a_figures.py`, `outputs/paper_a_figures/`).

Execution-environment assumptions:
- Python environment defined by `requirements.txt` / `requirements-frozen.txt`;
- package/runtime versions partially captured in saved model metadata and explicit analysis outputs;
- reference host used for current manuscript regeneration: Apple M3 Pro, macOS 26.3 (arm64), 11 logical CPUs, 18 GB RAM, Python 3.13.2;
- lockfile anchor: `sha256(requirements-frozen.txt)=b52d5a1f2e2edd5ada372ca66d18ef1447712fdd2c21f004d7e1f46a5ef9c6dc`.

Minimal rerun sequence:
1. install dependencies from `requirements-frozen.txt` (or controlled equivalent);
2. verify/create model + preprocessor artifacts in `experiments/exp1_adult/models/`;
3. run EXP2 robustness batch:
   `python3 scripts/run_batch_experiments.py --config-dir configs/experiments/exp2_scaled --output outputs/batch_results.csv --parallel`;
4. audit coverage:
   `python3 scripts/check_missing_results.py`;
5. generate summaries/figures:
   `python3 scripts/quick_summary.py`, `python3 scripts/full_summary.py`, `python3 scripts/generate_paper_a_figures.py`;
6. compile manuscript outputs.

Archival status:
- immutable DOI has not yet been minted in this repository state;
- provenance anchor currently used for this draft: `outputs/batch_manifest.json` (`git_hash=9fc70eb1e218a11f2fdd4bdb3aab3ea10a799a6f`) plus deterministic analysis exports under `outputs/analysis/paper_a_exp2_stats/`.

### 3.6 Statistical Analysis Pipeline (Replication-Grade Specification)
This section defines the executable protocol that produces all inferential artifacts for Paper A from repository-tracked inputs. It is written as a direct replication contract for independent teams (see Table X and Appendix X).

#### 3.6.1 Experimental factors and conditions
Independent variables are instantiated from `configs/experiments/exp2_comparative/`, `configs/experiments/exp2_scaled/`, and `configs/experiments/exp2_scaled/manifest.yaml`:
1. **Dataset** (fixed): `adult` (UCI Adult Income; tabular binary classification).
2. **Model family**: `logreg`, `rf`, `xgb`, `svm`, `mlp`.
3. **Explainer method**: `shap`, `lime`, `anchors`, `dice`.
4. **Random seed** (robustness cohort): $\{42,123,456,789,999\}$.
5. **Sampling intensity**: `samples_per_class=N`, $N\in\{50,100,200\}$ for EXP2 robustness; `N=10` for EXP2 comparative.
6. **Stability perturbation regime**: `stability_perturbations=15` and default `stability_noise_level=0.1`.
7. **Counterfactual metric activation**: `counterfactual=true` only for DiCE runs; `false` otherwise.

Planned EXP2 robustness grid size is $5\times4\times5\times3=300$ configurations. Paper A includes no component-removal ablation as a confirmatory factor; claims are strictly comparative across the defined method-family grid.

#### 3.6.2 Controls and baselines
For every matched `(model, seed, N)` cell, the following are held constant:
1. model artifact path (`experiments/exp1_adult/models/*.joblib`);
2. transformed feature space and preprocessor artifact reuse;
3. split and sampling random-state values;
4. evaluation sampler and metric engine implementation;
5. metric set and aggregation logic.

Baselines are cross-method (`shap`, `lime`, `anchors`, `dice`) under shared conditions; no method is treated as an oracle. Sanity-control baselines (random attribution, model randomization, label randomization) are not part of Paper A runs, so claims are bounded to trained-model comparative performance.

#### 3.6.3 Data protocol
Data handling is implemented in `src/data_loading/adult.py` and `src/evaluation/sampler.py`:
1. clean Adult records (whitespace normalization, missing-value canonicalization, duplicate removal, binary target normalization);
2. split with `train_test_split(test_size=0.2, stratify=y, random_state=seed)`;
3. fit preprocessor on train only (`StandardScaler` for numeric, `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` for categorical);
4. transform train/test with the same fitted transformer;
5. propagate transformed feature names to explainers and metric engine;
6. sample TP/TN/FP/FN strata with target size `N` per stratum.

For seed `42`, split sizes are train `39,032` (`y=0`: `29,687`, `y=1`: `9,345`) and test `9,758` (`y=0`: `7,422`, `y=1`: `2,336`). Nominal run size is `4N`; realized run size can be lower if a stratum is capacity-limited.

#### 3.6.4 Model training protocol
EXP2 does not retrain models; it evaluates frozen EXP1 models:
1. `logreg`: `solver=lbfgs`, `max_iter=1000`, `random_state=42`.
2. `rf`: `n_estimators=50`, `max_depth=15`, `min_samples_leaf=1`, `class_weight=balanced_subsample`, `random_state=42`.
3. `xgb`: `n_estimators=100`, `max_depth=6`, `learning_rate=0.1`, `objective=binary:logistic`, `eval_metric=logloss`, `random_state=42`.
4. `svm`: `kernel=rbf`, `C=1.0`, `gamma=scale`, `probability=true`, `random_state=42`.
5. `mlp`: `hidden_layer_sizes=[100]`, `activation=relu`, `solver=adam`, `max_iter=500`, `random_state=42`.

Early stopping is implemented only for XGBoost when validation data are explicitly provided; it is not active in the persisted EXP2 artifacts. No probability calibration wrapper (Platt/isotonic) is applied. EXP2 seed variation therefore affects split/sampling/explainer randomness, not model retraining randomness.

#### 3.6.5 Explanation generation protocol
Per-instance explanations are generated through `ExplainerWrapper.explain_instance` on a dense transformed vector (108 features in current Adult vocabulary), with per-call wall-clock timing.

Method-specific execution:
1. **SHAP** (`src/xai/shap_tabular.py`): `tree` mode for `rf/xgb`, `kernel` for `logreg/svm/mlp`; `n_background_samples=50`; class-1 attribution retained.
2. **LIME** (`src/xai/lime_tabular.py`): `num_samples=1000`, `num_features=10`, `kernel_width=3.0`, `discretize_continuous=False`; class-1 local map converted to dense vector.
3. **Anchors** (`src/xai/anchors_wrapper.py`): `AnchorTabular` fit on transformed train matrix; runtime precision threshold fixed at `0.95`.
4. **DiCE** (`src/xai/dice_wrapper.py`): backend `method="random"`, `desired_class="opposite"`, importance proxy from absolute original-counterfactual feature delta.

Parameter binding caveats that define effective treatment settings:
1. SHAP YAML parameters are consumed as configured.
2. LIME `kernel_width` is consumed from params; `num_samples`/`num_features` are bound via schema fields.
3. Anchors YAML `threshold` is not consumed; effective runtime threshold is fixed at `0.95`.
4. DiCE YAML `num_counterfactuals` is not consumed; runtime uses `total_CFs=1`.

Execution constraints: no explicit timeout/memory cap in EXP2 YAML; batch orchestration forces one evaluation worker per experiment process to prevent nested process amplification.

#### 3.6.6 Evaluation metrics and measurement procedure
Metrics are computed per instance in `src/experiment/metrics_engine.py`, then aggregated.

Primary confirmatory metrics:
1. `cost`: explanation time (ms).
2. `sparsity`: active-feature ratio with threshold $\tau=10^{-4}$.
3. `fidelity`: mapped to faithfulness correlation score $\rho$.
4. `faithfulness_gap`: top-$k$ masking prediction shift $\Delta_k$ with $k=5$.
5. `stability`: mean pairwise cosine similarity under Gaussian perturbations.

Faithfulness implementation (`src/metrics/faithfulness.py`):
$$
\Delta_k=\left|f(x)-f(x_{\text{mask-top-}k})\right|,\qquad
\rho=\mathrm{corr}\left(|w_i|,\left|f(x)-f(x_{-i})\right|\right).
$$
Pipeline mapping is `fidelity := rho` and `faithfulness_gap := Δ_k`.

Stability implementation (`src/metrics/stability.py`):
$$
x^{(t)}=x+\epsilon^{(t)},\ \epsilon^{(t)}\sim\mathcal{N}(0,\sigma^2),\qquad
S=\frac{2}{T(T-1)}\sum_{a<b}\cos\left(e^{(a)},e^{(b)}\right),
$$
with `T=stability_perturbations` and `σ=stability_noise_level`.

Secondary metrics:
1. `cf_sensitivity` is computed only when `counterfactual=true` and DiCE CF artifacts are available.
2. Domain alignment is implemented but disabled in EXP2 (`domain=false`).

Aggregation hierarchy:
1. instance-level values;
2. run-level summaries in each `results.json` (`mean`, `std`, `min`, `max`, `count`);
3. block-level summaries over `(model, N)` for global inference.

EEU status: EEU design exists in `experiments/exp1_adult/configs/metrics/exp1_metrics_config.yaml`, but EXP2 runtime does not emit memory/model-call telemetry required for EEU computation. Confirmatory cost inference therefore uses milliseconds only. `[TO FILL: implement EEU instrumentation (memory + model_calls) or keep EEU formally out of Paper A claims]`

#### 3.6.7 Statistical analysis plan
Analysis units and eligibility are deterministic and artifact-gated:
1. planned runs: `300`;
2. present `results.json`: `250`;
3. analyzable runs: `233`;
4. excluded artifacts: `16` empty, `1` malformed JSON.

Global inference is restricted to complete `(model, N)` blocks; this yields `15` blocks for four-way method comparison. Pairwise SHAP-LIME sets are:
1. primary: `45` matched cells (`logreg/rf/xgb`);
2. sensitivity: `65` matched cells (all model families).

Hypothesis testing stack (`scripts/run_exp2_statistical_analysis.py`):
1. Friedman omnibus test per metric over methods on complete blocks;
2. Nemenyi post-hoc localization for method pairs per metric;
3. two-sided Wilcoxon signed-rank for SHAP vs LIME on matched cells.

Multiplicity control:
1. within-metric pairwise control via Nemenyi;
2. across-metric Holm-Bonferroni over the five primary metrics for each inferential family (Friedman, Wilcoxon-45, Wilcoxon-65).

Uncertainty and effect-size reporting:
1. `mean`, `std`, `CV`;
2. confidence intervals from `src/analysis/confidence.py` (`t` and BCa bootstrap, 10,000 resamples, seed `42`);
3. Kendall’s $W$ (Friedman), Cohen’s $d_z$ and median paired difference (Wilcoxon).

All generated inferential artifacts are exported to `outputs/analysis/paper_a_exp2_stats/` (see Appendix X for file map).

#### 3.6.8 Robustness and sensitivity analyses
Implemented robustness axes:
1. seed heterogeneity (5 seeds);
2. sample-size heterogeneity (`N=50/100/200`);
3. perturbation robustness through Gaussian-noise stability metric.

Sensitivity controls:
1. replicate SHAP-LIME inference on both 45-cell and 65-cell matched sets;
2. enforce block-complete filtering for global tests;
3. exclude malformed/empty artifacts without synthetic reconstruction.

Deviation interpretation rule:
1. robust directional claim requires identical SHAP-LIME median-difference sign across 45-cell and 65-cell analyses;
2. robust inferential claim requires no Holm-adjusted significance flip across these analyses.

Adversarial stress testing is not part of Paper A. `[TO FILL: adversarial stress protocol with pre-registered deviation thresholds for extension experiments]`

#### 3.6.9 Reproducibility package
Release package for Paper A contains:
1. code (`src/`, `scripts/`);
2. experiment YAMLs (`configs/experiments/`);
3. frozen model/preprocessor artifacts (`experiments/exp1_adult/models/`);
4. run artifacts (`experiments/exp2_scaled/results/**/results.json`, `metrics.csv`);
5. aggregate outputs (`outputs/batch_manifest.json`, `outputs/batch_results.csv`);
6. inferential outputs (`outputs/analysis/paper_a_exp2_stats/`);
7. figure scripts and figure files (`scripts/generate_paper_a_figures.py`, `outputs/paper_a_figures/`).

Reference environment/provenance anchors:
1. host used for manuscript regeneration: Apple M3 Pro, macOS 26.3 (arm64), 11 logical CPUs, 18 GB RAM, Python 3.13.2;
2. dependency lock hash: `sha256(requirements-frozen.txt)=b52d5a1f2e2edd5ada372ca66d18ef1447712fdd2c21f004d7e1f46a5ef9c6dc`;
3. batch provenance hash: `outputs/batch_manifest.json` with `git_hash=9fc70eb1e218a11f2fdd4bdb3aab3ea10a799a6f`.

Minimal rerun sequence:
1. `python3 scripts/run_batch_experiments.py --config-dir configs/experiments/exp2_scaled --output outputs/batch_results.csv --parallel`
2. `python3 scripts/check_missing_results.py`
3. `python3 scripts/quick_summary.py`
4. `python3 scripts/full_summary.py`
5. `python3 scripts/generate_paper_a_figures.py`
6. `python3 scripts/run_exp2_statistical_analysis.py`

Archival status: `[TO FILL: immutable DOI bundle for camera-ready reproducibility package]`.

### 3.7 Inferential Implementation Details
This section specifies the inferential workflow applied to EXP2 and the supporting reproducibility cohort. It is designed to be executable from repository artifacts without undocumented analytical choices.

#### 3.7.1 Inferential objective and RQ linkage
The statistical pipeline operationalizes Section 3.2 as follows:
1. **RQ1 (method separation)**: test whether explainer methods differ on each primary metric.
2. **RQ2 (trade-off stability)**: test whether observed method differences remain consistent across model families and sampling intensities.

All tests are metric-specific and are performed on pre-defined analysis units (Section 3.4), not on pooled instance rows, to avoid pseudo-replication.

#### 3.7.2 Analysis populations and eligibility sets
Statistical inputs are drawn from artifact-qualified EXP2 outputs:
1. planned robustness grid: 300 configurations;
2. present artifacts: 250 `results.json` files;
3. analyzable artifacts: 233 (non-empty `instance_evaluations`);
4. malformed artifacts: 1; structurally empty artifacts: 16.

Eligibility follows Section 3.4.5:
1. JSON must parse;
2. run must contain analyzable instance-level metrics;
3. no imputation for missing runs;
4. global multi-method tests restricted to complete `(model, N)` blocks.

Resulting inferential sets:
1. **Global omnibus set**: 15 complete `(model, N)` blocks x 4 methods.
2. **Primary paired SHAP-LIME set**: 45 matched cells on `logreg/rf/xgb`.
3. **Sensitivity paired SHAP-LIME set**: 65 matched cells on all 5 model families.
4. **Reproducibility cohort**: EXP1 repeated-run set (`9` seeds per core configuration).

#### 3.7.3 Estimands, aggregation, and metric directionality
For metric $m$, run-level estimand is $y_{g,k,s,n,m}$ (Section 3.4). Global method inference uses block-level summaries:
$$
\bar{y}_{k,b,m}=\frac{1}{|S_{k,b}|}\sum_{s\in S_{k,b}}y_{g,k,s,n,m}, \quad b=(g,n).
$$

Primary inferential metrics are:
1. fidelity,
2. stability,
3. sparsity,
4. faithfulness gap,
5. cost.

Directionality is fixed before analysis:
1. higher is better: fidelity, stability, faithfulness gap;
2. lower is better: sparsity, cost.

Directionality is used for interpretive ranking and visualization normalization (e.g., method radar; see Figure X), while non-parametric significance tests operate on observed metric values per design block.

#### 3.7.4 Global omnibus test (Friedman)
For each metric $m$:
1. build a block-by-method matrix with rows = complete `(model, N)` blocks and columns = methods;
2. apply Friedman’s test with methods as repeated treatments and blocks as matched contexts;
3. evaluate against $\alpha=0.05$ (see Table X).

Rationale for Friedman:
1. repeated-measures design across common blocks;
2. no Gaussian assumption required;
3. robust under heterogeneous metric scales.

#### 3.7.5 Post-hoc localization (Nemenyi)
When Friedman rejects $H_{0,m}^{(1)}$:
1. run Nemenyi pairwise post-hoc comparisons over the same block-structured matrix;
2. report pairwise adjusted p-values for all method pairs within metric $m$;
3. declare significance at $\alpha=0.05$ (see Appendix X).

This controls family-wise error for pairwise method comparisons **within** each metric.  
Across-metric multiplicity is controlled using Holm-Bonferroni adjustment over the five primary metrics, applied separately to:
1. the Friedman family (five omnibus p-values),
2. the 45-pair Wilcoxon family,
3. the 65-pair Wilcoxon family.

#### 3.7.6 Focused paired SHAP-vs-LIME analysis (Wilcoxon)
To isolate the main attribution-method contrast under strict matching:
1. construct paired observations on identical `(model, seed, N)` cells;
2. run two-sided Wilcoxon signed-rank tests for each primary metric;
3. report paired method means (and/or medians) plus p-values.

Primary paired analysis uses the 45-cell `logreg/rf/xgb` subset; all-model 65-cell analysis is used as sensitivity support.

#### 3.7.7 Uncertainty quantification and interval estimation
For each reported metric summary, we provide:
1. mean and standard deviation;
2. coefficient of variation (CV);
3. confidence intervals where available.

CI procedures are implemented in `src/analysis/confidence.py`:
1. $t$-distribution CI for the mean (`compute_t_ci`);
2. bootstrap CI (`compute_bootstrap_ci`) with BCa method, `n_resamples=10000`, `random_seed=42`, percentile fallback on failure.

#### 3.7.8 Effect sizes and practical significance
Effect-size reporting is produced alongside p-values:
1. **Friedman layer**: Kendall’s $W$ is reported for each metric ($W=\chi^2/[B\,(K-1)]$, with $B$ blocks and $K$ methods).
2. **Paired Wilcoxon layer**: Cohen’s $d_z$ is reported on paired SHAP-LIME differences.
3. **Location effect support**: paired median differences are reported per metric.

These values are exported by the EXP2 statistical driver for direct manuscript/appendix ingestion.

#### 3.7.9 Sensitivity, missingness handling, and deviation controls
Sensitivity safeguards in the statistical layer:
1. re-run key paired contrast on both restricted (45) and all-model (65) matched sets;
2. restrict global multi-method inference to block-complete contexts only;
3. exclude malformed/empty artifacts rather than partially reconstructing runs.

Deviation-control status:
1. dispersion is reported via std/CV/CI;
2. no threshold-based practical-equivalence rule is enforced in the current protocol; robustness claims are therefore based on direction consistency, effect size magnitude, and uncertainty intervals rather than binary pass/fail cutoffs.

#### 3.7.10 Reproducible execution of the analysis stack
The analysis workflow is reproducible from committed scripts and outputs:
1. generate/refresh run artifacts via batch execution;
2. audit missing and malformed artifacts (`scripts/check_missing_results.py`);
3. aggregate and summarize (`scripts/quick_summary.py`, `scripts/full_summary.py`);
4. regenerate manuscript figures (`scripts/generate_paper_a_figures.py`);
5. execute deterministic EXP2 inference export:
   `python3 scripts/run_exp2_statistical_analysis.py`.

The EXP2 driver writes all inferential artifacts (Friedman, Nemenyi, Wilcoxon, multiplicity-adjusted p-values, effect sizes, matched-cell inventories) to:
`outputs/analysis/paper_a_exp2_stats/`.

### 3.8 Reproducibility Protocol
#### 3.8.1 Scope and methodological role
This section specifies the reproducibility contract for the methodological pipeline defined in Sections 3.6 and 3.7. Its role is to guarantee that reported answers to RQ1/RQ2 can be regenerated from versioned inputs without undocumented analyst choices (see Table X).

#### 3.8.2 Definitions, notation, and assumptions
We define a run key as:
$$
r=(g,k,s,n),
$$
where $g$ is model family, $k$ is explainer, $s$ is random seed, and $n$ is per-quadrant sampling intensity.

For reproducibility, we use four state objects:
1. **Configuration state** $\mathcal{C}$: YAML specifications, seed grid, metric switches, and command-line invocation.
2. **Artifact state** $\mathcal{A}$: per-run outputs (`results.json`, `metrics.csv`) and aggregate exports.
3. **Inference state** $\mathcal{I}$: statistical tables and summaries under `outputs/analysis/paper_a_exp2_stats/`.
4. **Variance state** $\mathcal{V}$: repeated-run dispersion outputs (`reproducibility_report.csv`).

Assumptions:
1. model artifacts in `experiments/exp1_adult/models/` are frozen during EXP2;
2. configuration files under `configs/experiments/` are immutable during one execution pass;
3. reported claims are computed only from artifact-qualified runs.

#### 3.8.3 Reproducibility procedure (executable)
1. Freeze protocol inputs:
   - config directories (`configs/experiments/exp2_scaled`, `configs/experiments/exp2_comparative`);
   - dependency anchor `sha256(requirements-frozen.txt)=b52d5a1f2e2edd5ada372ca66d18ef1447712fdd2c21f004d7e1f46a5ef9c6dc`;
   - provenance anchor `outputs/batch_manifest.json` (`git_hash=9fc70eb1e218a11f2fdd4bdb3aab3ea10a799a6f`).
2. Execute batch generation of EXP2 artifacts:
   - `python3 scripts/run_batch_experiments.py --config-dir configs/experiments/exp2_scaled --output outputs/batch_results.csv --parallel`
3. Audit artifact integrity:
   - `python3 scripts/check_missing_results.py`
   - classify runs as `ok_instance`, `empty`, or `json_error` through the statistical inventory.
4. Regenerate deterministic inference exports:
   - `python3 scripts/run_exp2_statistical_analysis.py`
   - verify population counts in `analysis_summary.json` (planned `300`, present `250`, analyzable `233`, complete blocks `15`, paired sets `45/65`).
5. Regenerate descriptive summaries/figures:
   - `python3 scripts/quick_summary.py`
   - `python3 scripts/full_summary.py`
   - `python3 scripts/generate_paper_a_figures.py`
6. Regenerate repeated-run variance characterization:
   - `python3 scripts/run_reproducibility_study.py --config-dir configs/experiments --pattern "exp1_adult_*.yaml" --output-dir experiments/exp1_adult/reproducibility`

#### 3.8.4 Quality checks and acceptance criteria
A reproduction attempt is considered methodologically valid only if all conditions below hold:
1. **Config determinism**: execution uses the declared seed grid and model/explainer matrix from EXP2 manifests.
2. **Artifact integrity**: malformed and empty artifacts are explicitly enumerated; no implicit imputation is applied.
3. **Inferential eligibility**: omnibus tests are computed only on complete `(model, N)` blocks.
4. **Claim traceability**: each quantitative claim in Section 4 maps to a versioned file in `outputs/analysis/paper_a_exp2_stats/` or figure source under `outputs/paper_a_figures/`.
5. **Variance reporting**: reproducibility dispersion (CV/CI) is present for repeated-run cohorts.

#### 3.8.5 Environment and compute disclosure
Reference host used for manuscript regeneration:
1. Apple M3 Pro, macOS 26.3 (arm64);
2. 11 logical CPUs, 18 GB RAM;
3. Python 3.13.2.

This host profile is reported as provenance metadata, not as a required execution platform. Hardware-normalized runtime scaling is not currently modeled. `[TO FILL: provide multi-hardware runtime normalization protocol if cross-machine runtime claims are elevated]`

### 3.9 Validity Threats and Mitigations
#### 3.9.1 Scope and role
This section formalizes validity threats for the methodological core and specifies mitigations, diagnostics, and residual risk boundaries for interpretation of Section 4 results.

#### 3.9.2 Internal validity
1. **Threat**: incomplete EXP2 execution coverage (planned `300`, present `250`, analyzable `233`), with one malformed file and empty artifacts.
2. **Mitigation**:
   - explicit missingness/parse auditing;
   - block-complete filtering for omnibus inference;
   - matched-cell filtering for paired inference.
3. **Residual risk**: missingness may be non-random across method-model cells; effect estimates can be coverage-sensitive.

#### 3.9.3 Construct validity
1. **Threat**: metric naming may be conflated with alternative definitions in literature.
2. **Mitigation**:
   - code-bound operational definitions (`src/metrics/faithfulness.py`, `src/metrics/stability.py`, `src/metrics/sparsity.py`);
   - explicit mapping `fidelity := faithfulness correlation`, `faithfulness_gap := top-k masking shift`.
3. **Residual risk**:
   - EEU is specified in design artifacts but not computed in EXP2 runtime;
   - cost claims are therefore wall-clock specific and not energy-normalized.

#### 3.9.4 Statistical conclusion validity
1. **Threat**: inflated error rates under multiple tests and pseudo-replication from instance-level pooling.
2. **Mitigation**:
   - run/block-level inference units;
   - Friedman omnibus + Nemenyi localization;
   - Wilcoxon for matched SHAP-LIME contrasts;
   - Holm-Bonferroni across primary metrics per inferential family.
3. **Residual risk**: practical equivalence thresholds are not pre-registered; significance is complemented by effect sizes and interval dispersion.

#### 3.9.5 External validity
1. **Threat**: evidence is from one dataset family (tabular Adult) and one benchmark task.
2. **Mitigation**:
   - model diversity (`logreg/rf/xgb/svm/mlp`);
   - explainer diversity (`shap/lime/anchors/dice`);
   - heterogeneity across seeds and sample sizes.
3. **Residual risk**: transfer to text/vision/time-series domains is not established in Paper A.

#### 3.9.6 Implementation validity
1. **Threat**: config-runtime parameter divergence (Anchors threshold, DiCE CF count).
2. **Mitigation**: explicit disclosure of effective runtime settings in Section 3.6.5 and interpretation limits on those settings.
3. **Residual risk**: parameter harmonization is pending and may alter absolute performance levels. `[TO FILL: camera-ready harmonization diff report between YAML-exposed and runtime-bound parameters]`

#### 3.9.7 Diagnostic policy
Before any inferential reporting:
1. run inventory diagnostics must be regenerated;
2. malformed and empty artifacts must be listed in the manuscript;
3. robustness statements must pass directional/significance consistency checks between 45-cell and 65-cell SHAP-LIME analyses.

### 3.10 Framework Operation Method (FOM-7): Executable Protocol
#### 3.10.1 Scope and formal definition
FOM-7 is the operational methodology contribution of Paper A. It transforms a benchmark specification into auditable, claim-ready evidence with stage-gated progression.

We define:
$$
\mathcal{M}_{\text{FOM7}} = \{(S_i, A_i, G_i)\}_{i=1}^{7},
$$
where $S_i$ is stage $i$, $A_i$ are required artifacts for stage $i$, and $G_i$ is the gate condition to enter $S_{i+1}$.

Progression rule:
$$
S_i \rightarrow S_{i+1}\ \text{iff}\ G_i=\text{pass}.
$$

#### 3.10.2 Stage protocol, controls, and gate logic

| Stage | Objective | Required Artifacts | Gate (must pass before next stage) |
| :--- | :--- | :--- | :--- |
| S1: Protocol specification | Freeze study design before execution | Config files under `configs/experiments/`, explicit model/explainer/seed/sample grid | Planned run count and factors are fully enumerated |
| S2: Controlled execution | Produce run artifacts under fixed configs | Per-run `results.json`, logs, `outputs/batch_manifest.json` | Each planned config has terminal status (`success`, `failed`, or `skipped`) |
| S3: Integrity audit | Detect silent data-quality failures | Missing-run report (`scripts/check_missing_results.py`), JSON parse audit | Missing and malformed artifacts are explicitly listed |
| S4: Harmonization and aggregation | Convert heterogeneous results into analysis-ready tables | Aggregated CSV/JSON summaries (e.g., `outputs/batch_results.csv`) | All retained runs contain required primary metrics |
| S5: Statistical inference | Quantify significance and pairwise differences | Friedman, Nemenyi, and Wilcoxon outputs with metric-level p-values | Inferential outputs are complete for all primary metrics |
| S6: Reproducibility characterization | Quantify variance under repeated runs | `experiments/exp1_adult/reproducibility/reproducibility_report.csv` | CV and dispersion are reported for each core metric |
| S7: Claim-ready reporting | Bind manuscript claims to verifiable artifacts | Manuscript tables/figures + caveat list + artifact inventory | Every quantitative claim is traceable to a versioned artifact |

Comparability controls embedded in FOM-7:
1. shared transformed feature space across methods;
2. shared split/sampling seeds within matched cells;
3. shared metric engine and aggregation stack;
4. explicit exclusion rather than reconstruction of malformed/empty runs.

#### 3.10.3 Reference implementation procedure
Reference command sequence used by this repository implementation:
1. `python3 scripts/run_batch_experiments.py --config-dir configs/experiments/exp2_scaled --output outputs/batch_results.csv --parallel`
2. `python3 scripts/check_missing_results.py`
3. `python3 scripts/quick_summary.py`
4. `python3 scripts/full_summary.py`
5. `python3 scripts/run_reproducibility_study.py --config-dir configs/experiments --pattern "exp1_adult_*.yaml" --output-dir experiments/exp1_adult/reproducibility`
6. `python3 scripts/run_exp2_statistical_analysis.py`

#### 3.10.4 Failure handling and reporting policy
If any gate fails:
1. downstream inferential steps are not claim-eligible;
2. failure status and missing artifacts are reported explicitly;
3. manuscript claims must be downgraded to descriptive-only status for affected comparisons.

These commands are implementation-specific realizations of FOM-7. The method remains platform-agnostic if equivalent stage artifacts and gate checks are satisfied (see Figure X and Table X).

## 4. Results

### 4.1 Overview of evaluation setup (minimum necessary context)
Section 4 reports two evidence streams: EXP2 robustness (global and paired method comparisons) and EXP1 reproducibility (variance profiling across repeated runs). Compared explainers are SHAP, LIME, Anchors, and DiCE. Reported metrics are Fidelity, Stability, Sparsity, Faithfulness Gap, and Cost (ms). [TO FILL: metric definitions or explicit cross-reference to Section 3.6.6]. In this section, “15 complete model-size blocks” denotes the block-level EXP2 units used for global multi-method inference, and “45 matched configs” denotes the SHAP-LIME subset with shared `(model, seed, N)` cells on `logreg/rf/xgb`.

### 4.2 Global trade-offs across methods (quality vs cost)
Table 4.1 reports method means over the EXP2 complete-block set.

Table 4.1. Global method means (EXP2 robustness: 15 complete model-size blocks)

| Method | Fidelity | Stability | Sparsity | Faithfulness Gap | Time (ms) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| SHAP | 0.8176 | 0.7377 | 0.2264 | 0.4474 | 685220.23 |
| LIME | 0.5602 | 0.0144 | 0.0846 | 0.3342 | 3660.68 |
| Anchors | 0.3853 | 0.0006 | 0.0928 | 0.2382 | 25326.92 |
| DiCE | 0.1716 | 0.3602 | 0.0164 | 0.0988 | 16306.50 |

SHAP has the highest Fidelity (`0.8176`), highest Stability (`0.7377`), and highest Faithfulness Gap (`0.4474`) among the four methods. DiCE has the lowest Sparsity value (`0.0164`), while LIME has the lowest Cost (`3660.68` ms). Anchors shows very low Stability (`0.0006`) with Cost (`25326.92` ms) above LIME and DiCE.

The quality-cost frontier is therefore explicit in the reported means: SHAP occupies the strongest quality region on Fidelity/Stability/Faithfulness Gap but at the highest runtime (`685220.23` ms), whereas LIME occupies the lowest-cost region with reduced quality on Fidelity and Stability. DiCE improves conciseness (Sparsity) relative to SHAP/LIME/Anchors but with lower Fidelity and Faithfulness Gap.

### 4.3 Global statistical evidence across methods
Table 4.2 reports Friedman omnibus tests over methods for each primary metric.

Table 4.2. Friedman tests across methods

| Metric | Statistic | p-value | Significant |
| :--- | ---: | ---: | :--- |
| Fidelity | 42.12 | 3.78e-09 | Yes |
| Stability | 43.88 | 1.60e-09 | Yes |
| Sparsity | 35.64 | 8.92e-08 | Yes |
| Faithfulness Gap | 45.00 | 9.25e-10 | Yes |
| Cost | 27.72 | 4.16e-06 | Yes |

For every metric, the Friedman test rejects the null of equal performance across methods. This establishes that method-level differences are statistically detectable at the global level. It does not, by itself, determine which specific method pairs differ or the direction of those differences.

[TO FILL: post-hoc method and correction].

### 4.4 Targeted pairwise comparison (SHAP vs LIME on shared families)
Table 4.3 reports SHAP-LIME paired inference on the shared `logreg/rf/xgb` subset.

Table 4.3. Paired SHAP vs LIME (45 matched configs on `logreg/rf/xgb`)

| Metric | SHAP Mean | LIME Mean | Wilcoxon p-value |
| :--- | ---: | ---: | ---: |
| Fidelity | 0.8112 | 0.5556 | 5.68e-14 |
| Stability | 0.8013 | 0.0154 | 5.68e-14 |
| Sparsity | 0.3156 | 0.0845 | 5.68e-14 |
| Faithfulness Gap | 0.3924 | 0.3408 | 5.68e-14 |
| Cost (ms) | 1258.72 | 210.45 | 2.29e-06 |

Within this matched set, SHAP is higher on Fidelity, Stability, and Faithfulness Gap, whereas LIME has lower Cost and lower Sparsity value. Statistically, all listed Wilcoxon p-values indicate a non-zero paired difference. Practically, the SHAP quality gains on the reported quality metrics are accompanied by a runtime penalty relative to LIME in the same matched cells.

This pairwise result is constrained to shared `logreg/rf/xgb` configurations and cannot be generalized to methods not in the pair (Anchors/DiCE) or to model families outside the matched set.

### 4.5 Reproducibility and variance profile
EXP1 repeated-run evidence indicates low dispersion for quality-oriented metrics and higher dispersion for runtime. The quality metrics remain relatively stable across repeated seeds, while computational cost varies more substantially for SHAP variants.

Decision-relevant variability findings:
- Metric stability (quality): Fidelity CV `<= 0.0634`, Stability CV `<= 0.0826`, Sparsity CV `<= 0.0441`, Faithfulness Gap CV `<= 0.0358`.
- Runtime instability (cost): Cost CV reaches `0.225` for SHAP variants.
- Interpretation boundary: quality rankings are more repeatable than runtime behavior under the reported repeated-run protocol.

### 4.6 Synthesis and implications for practice
- When the decision objective is maximum Fidelity/Stability/Faithfulness Gap and runtime budget is permissive, SHAP is the supported choice in this benchmark.
- When compute or latency is constrained, LIME is the supported low-cost option, with lower reported Fidelity and Stability than SHAP.
- When explanation conciseness (Sparsity) is prioritized, DiCE provides the lowest reported Sparsity value, with lower reported Fidelity and Faithfulness Gap.
- Methods are not statistically interchangeable on the primary metrics: omnibus Friedman tests reject the null of equal method performance for all five metrics.
- SHAP-vs-LIME trade-off is robust on the shared matched set: higher quality metrics for SHAP are paired with higher runtime cost.

Interpretation limits:
- [TO FILL: parameterization details / failure analysis for Anchors stability near zero].
- [TO FILL: external validation on additional datasets/tasks before generalizing these method rankings].

## 5. Validity and Reporting Caveats
### 5.1 Statistical Conclusion Validity
**Issue.** The EXP2 robustness cohort is incomplete: 50 runs are missing from the planned 300-run grid, and one result artifact is malformed.

**Why it matters.** Missing and invalid runs reduce inferential coverage and can affect confidence in estimated method rankings and the reported quality-cost frontier if missingness is systematic.

**Mitigation already done.** The analysis uses explicit artifact qualification, excludes malformed/empty artifacts, applies block-complete filtering for omnibus tests, and uses matched-cell filtering for paired tests.

**Residual risk.** The mechanism of missingness is not yet characterized as random vs systematic. `[TO FILL: missingness diagnosis by method/model/seed/sample-size cell and impact analysis]`

### 5.2 Construct Validity
**Issue.** Reported metric names are operationalized by implementation-specific definitions, and cost is currently wall-clock time rather than an energy-normalized measure.

**Why it matters.** Interpretation depends on exact metric semantics; cross-paper comparability is weakened when metric labels are shared but implementations differ.

**Mitigation already done.** Metric computation is code-bound and consistently applied within the benchmark pipeline; global and paired comparisons use the same metric engine and aggregation logic.

**Residual risk.** Some metric definitions still need explicit manuscript anchoring for reviewer-level traceability. `[TO FILL: metric definitions location/cross-reference]`  
EEU remains uncomputed in EXP2 runtime and therefore cannot support energy-based claims.

### 5.3 Internal Validity (Runtime Comparability and Configuration Fidelity)
**Issue.** Runtime and accuracy-like comparisons depend on explainer variants and runtime bindings (e.g., TreeSHAP vs KernelSHAP, Anchors threshold binding, DiCE counterfactual count binding).

**Why it matters.** Apparent method differences can partially reflect implementation pathway choices rather than only conceptual method differences.

**Mitigation already done.** Within each matched cell, model artifact, transformed feature space, split/sampling seeds, and metric engine are held constant; effective runtime parameter bindings are disclosed.

**Residual risk.** Runtime comparability remains sensitive to software stack and hardware profile. `[TO FILL: environment spec for publication artifact, including CPU policy and dependency lock granularity]`  
For cross-study comparability, runtime should be reported under standardized constraints. `[TO FILL: standardized runtime constraint protocol (cores, memory cap, timeout policy)]`

### 5.4 External Validity
**Issue.** Evidence is benchmarked on a single task setting and reported pairwise contrasts are restricted to shared model-family subsets.

**Why it matters.** Method rankings and trade-offs may shift across datasets, modalities, and task definitions.

**Mitigation already done.** The benchmark includes multiple model families, multiple explainers, and seed/sample-size heterogeneity within the evaluated setting.

**Residual risk.** Generalization beyond the current benchmark context is not established and should be treated as an open empirical question.

### 5.5 Reproducibility and Operational Validity
**Issue.** Strong reproducibility claims require both deterministic pipelines and durable artifact packaging.

**Why it matters.** Without auditable lineage and re-execution hooks, reported benchmark conclusions are difficult to verify independently.

**Mitigation already done.** FOM-7 defines stage-gated execution with required artifacts; run inventories, inference exports, and reproducibility scripts are provided.

**Residual risk.** Immutable archival packaging is not finalized. `[TO FILL: DOI-backed artifact bundle with versioned lineage map]`

### 5.6 Reporting Scope Boundary: Semantic Evaluation
**Issue.** Semantic/user-centric evaluation is out of scope for Paper A.

**Why it matters.** Technical metric superiority does not directly establish user-perceived usefulness, trust calibration, or task-level decision quality.

**Mitigation already done.** Paper A explicitly scopes claims to quantitative benchmark evidence; no user-centric claims are made.

**Residual risk.** A complete semantic layer requires a calibrated rubric, task definitions, and human-study protocol (potentially with LLM-judge calibration), which are deferred. `[TO FILL: future study design pointer for semantic evaluation integration]`

## 6. JMLR-Track Positioning
This work is positioned for the **Datasets and Benchmarks** track.

- **Claim:** The submission provides a reusable XAI benchmark artifact stack.  
  **Evidence/artifact:** code (`src/`, `scripts/`), experiment configs (`configs/experiments/`), run artifacts (`experiments/exp2_scaled/results/**/results.json`), summary exports, and inferential outputs (`outputs/analysis/paper_a_exp2_stats/`).  
  **Why it matters to the track:** benchmark-track contributions require reusable resources, not only narrative findings.

- **Claim:** The benchmark is auditable with explicit failure accounting.  
  **Evidence/artifact:** coverage/missingness diagnostics, malformed-artifact reporting, and stage-gated FOM-7 execution with artifact gates.  
  **Why it matters to the track:** transparent handling of incomplete runs improves trustworthiness of benchmark evidence.

- **Claim:** The evaluation protocol supports multi-objective comparison rather than single-metric ranking.  
  **Evidence/artifact:** joint reporting of Fidelity, Stability, Sparsity, Faithfulness Gap, and Cost with omnibus and paired non-parametric tests.  
  **Why it matters to the track:** benchmark utility increases when trade-offs are measurable across quality, robustness, and compute axes.

- **Claim:** The framework is designed for extension and repeat execution.  
  **Evidence/artifact:** config-driven experiment matrix, deterministic analysis driver, reproducibility scripts, and FOM-7 operational protocol.  
  **Why it matters to the track:** reusable benchmark infrastructure supports follow-on comparisons and ablations by other groups.

- **Claim:** The methodological novelty is the combination of benchmark evidence with auditable execution governance (FOM-7).  
  **Evidence/artifact:** explicit stage/gate model linking protocol specification, integrity audit, inference export, and claim-ready reporting.  
  **Why it matters to the track:** this contributes a replicable benchmark operation model, not only method-level score tables.  
  `[TO FILL: comparison citations to existing XAI benchmark/toolkit papers and novelty delta statement]`

Artifact packaging expected for submission:
- released code/configs/analysis outputs and failure reports are present;
- logs and lineage graph should be explicitly indexed in submission metadata. `[TO FILL: artifact index with paths for logs/lineage graph]`

## 7. Conclusion
The reported results indicate a multi-objective frontier rather than a single best method: SHAP is strongest on the reported quality-oriented metrics, LIME is strongest on runtime efficiency, and DiCE is strongest on the reported sparsity criterion. Global non-parametric tests reject the null of equal performance across methods on all primary metrics, while the SHAP-LIME paired subset confirms a quality-cost trade-off on shared model families.

Methodologically, Paper A contributes FOM-7 as an auditable operation protocol for benchmark studies: protocol freezing, controlled execution, integrity auditing, harmonized inference, reproducibility profiling, and claim-traceable reporting. This contribution is operational rather than algorithmic; it specifies how benchmark evidence is generated and qualified under incomplete execution.

- **Takeaway:** Method selection should be objective-driven (quality, sparsity, or runtime), not based on a single aggregate score.
- **Takeaway:** Statistical evidence supports method differentiation at the omnibus level; pairwise direction should be interpreted within matched design constraints.
- **Limitation:** Incomplete EXP2 coverage (missing and malformed artifacts) qualifies confidence in frontier stability across the full planned grid.
- **Next steps:** complete missingness diagnostics and publish archival artifact bundle with explicit lineage. `[TO FILL: missingness diagnosis + DOI package plan]`
- **Next steps:** integrate deferred semantic evaluation with calibrated rubric and task-grounded human-study protocol. `[TO FILL: future semantic study protocol]`

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
