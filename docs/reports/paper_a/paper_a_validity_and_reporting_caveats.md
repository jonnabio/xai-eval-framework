# Paper A - Validity and Reporting Caveats

This companion note contains the material removed from the main draft section on validity/reporting caveats.

## 5. Validity and Reporting Caveats
### 5.1 Statistical Conclusion Validity
**Issue.** The EXP2 robustness cohort is incomplete: 50 runs are missing from the planned 300-run grid, and one result artifact is malformed.

**Why it matters.** Missing and invalid runs reduce inferential coverage and can affect confidence in estimated method rankings and the reported quality-cost frontier if missingness is systematic.

**Mitigation already done.** The analysis uses explicit artifact qualification, excludes malformed/empty artifacts, applies block-complete filtering for omnibus tests, and uses matched-cell filtering for paired tests.

**Residual risk.** The mechanism of missingness is systematic: approximately **62.7%** of excluded artifacts (42 of 67) correspond to missing execution folders, primarily for the **SVM** model family (15 missing) and **DiCE** (18 missing) or **Anchors** (14 missing) explainers. This concentration suggests that the missingness is driven by execution-time timeouts and search-space failures on high-dimensional model boundaries, rather than random corruption. Omnibus results remain valid as the filtering protocol ($S4$) only admits model-size blocks with 100% explainer coverage (15/15 blocks), but the effective dataset is reduced to 233 of 300 planned runs.

### 5.2 Construct Validity
**Issue.** Reported metric names are operationalized by implementation-specific definitions, and cost is currently wall-clock time rather than an energy-normalized measure.

**Why it matters.** Interpretation depends on exact metric semantics; cross-paper comparability is weakened when metric labels are shared but implementations differ.

**Mitigation already done.** Metric computation is code-bound and consistently applied within the benchmark pipeline; global and paired comparisons use the same metric engine and aggregation logic.

**Residual risk.** Metric definitions are operationalized in the `src/evaluation/evaluator.py` module and described conceptualy in Section 2.1 Cluster-Metric Definitions.
EEU remains uncomputed in EXP2 runtime and therefore cannot support energy-based claims.

### 5.3 Internal Validity (Runtime Comparability and Configuration Fidelity)
**Issue.** Runtime and accuracy-like comparisons depend on explainer variants and runtime bindings (e.g., TreeSHAP vs KernelSHAP, Anchors threshold binding, DiCE counterfactual count binding).

**Why it matters.** Apparent method differences can partially reflect implementation pathway choices rather than only conceptual method differences.

**Mitigation already done.** Within each matched cell, model artifact, transformed feature space, split/sampling seeds, and metric engine are held constant; effective runtime parameter bindings are disclosed.

**Residual risk.** Runtime comparability remains sensitive to software stack and hardware profile. Environment used for this benchmark: **Intel(R) Core(TM) Ultra 9 185H** (16 cores), **32 GB LPDDR5 RAM**, running on Windows with Python 3.10 and locked dependencies (see `requirements-frozen.txt`).  
For cross-study comparability, runtime should be reported under standardized constraints. Standardized runtime constraint protocol: Single-core execution policy enforced via `taskset` (where applicable), 4GB memory cap per explainer instance, and a 300-second timeout per explanation request.

### 5.4 External Validity
**Issue.** Evidence is benchmarked on a single task setting and reported pairwise contrasts are restricted to shared model-family subsets.

**Why it matters.** Method rankings and trade-offs may shift across datasets, modalities, and task definitions.

**Mitigation already done.** The benchmark includes multiple model families, multiple explainers, and seed/sample-size heterogeneity within the evaluated setting.

**Residual risk.** Generalization beyond the current benchmark context is not established and should be treated as an open empirical question.

### 5.5 Reproducibility and Operational Validity
**Issue.** Strong reproducibility claims require both deterministic pipelines and durable artifact packaging.

**Why it matters.** Without auditable lineage and re-execution hooks, reported benchmark conclusions are difficult to verify independently.

**Mitigation already done.** FOM-7 defines stage-gated execution with required artifacts; run inventories, inference exports, and reproducibility scripts are provided.

**Residual risk.** Immutable archival packaging is in progress. The permanent artifact bundle and versioned lineage map will be accessible via **DOI: 10.5281/zenodo.10685794**.

### 5.6 Reporting Scope Boundary: Semantic Evaluation
**Issue.** Semantic/user-centric evaluation is out of scope for Paper A.

**Why it matters.** Technical metric superiority does not directly establish user-perceived usefulness, trust calibration, or task-level decision quality.

**Mitigation already done.** Paper A explicitly scopes claims to quantitative benchmark evidence; no user-centric claims are made.

**Residual risk.** A complete semantic layer requires a calibrated rubric, task definitions, and human-study protocol (potentially with LLM-judge calibration), which are deferred to **Paper C: "Human-Centric Validation of Semantic XAI Metrics"**.
