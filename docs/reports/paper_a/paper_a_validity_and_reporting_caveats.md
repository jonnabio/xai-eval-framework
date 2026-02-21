# Paper A - Validity and Reporting Caveats

This companion note contains the material removed from the main draft section on validity/reporting caveats.

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
