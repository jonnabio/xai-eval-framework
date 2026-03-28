# Paper A Validity and Reporting Caveats

This companion note describes the validity boundaries and technical constraints of the JMLR manuscript draft.

## 5. Validity and Reporting Caveats

### 5.1 Statistical Conclusion Validity

**Issue.** The EXP2 robustness cohort contains 17 excluded artifacts from the planned 300-run grid: 16 are effectively "empty" (missing results) and one result artifact is malformed.

**Why it matters.** Missing and invalid runs reduce inferential coverage and can affect confidence in estimated method rankings and the reported quality-cost frontier if missingness is systematic.

**Mitigation already done.** The analysis uses explicit artifact qualification, excludes malformed/empty artifacts, applies block-complete filtering for omnibus tests, and uses matched-cell filtering for paired tests. A "recovery" phase successfully restored 13 previously missing Anchors and SHAP artifacts, bringing the analyzable dataset to 283 of 300 planned runs (94.3%).

**Residual risk / Systematic Diagnosis.** The mechanism of missingness is indeed systematic and follows two primary failure modes:

1. **Search-Space/Runtime Timeouts (16 artifacts):** Primarily affecting the **DiCE** explainer across MLP, RF, SVM, and XGB model families. DiCE (Diverse Counterfactual Explanations) solves a multi-objective optimization problem to find counterfactuals. Under the standardized 300s timeout constraint, these runs consistently failed to converge or find valid counterfactuals within the high-dimensional Adult dataset features. These are technically MNAR (Missing Not At Random) as they occur specifically in high-complexity configurations.
2. **Serialization Corruption (1 artifact):** Specifically `svm_shap_s999_n200`. This artifact is malformed due to an invalid control character (illegal byte sequence) in the JSON stream, likely caused by a race condition or an unhandled exception during the `json.dump` process onto the network-mapped drive.

Omnibus results remain valid as the filtering protocol only admits model-size blocks with 100% explainer coverage (15/15 blocks), but the effective dataset is reduced to the analyzed 283 runs. The concentration of failures in DiCE implies that DiCE's average cost and quality metrics are likely optimistic (underestimating cost for failed cases), which is explicitly noted in the final trade-off discussion.

### 5.2 Construct Validity

**Issue.** Reported metric names are operationalized by implementation-specific definitions.

**Why it matters.** Interpretation depends on exact metric semantics; cross-paper comparability is weakened when metric labels are shared but implementations differ.

**Mitigation already done.** Metric computation is code-bound and consistently applied within the benchmark pipeline; global and paired comparisons use the same metric engine and aggregation logic.

**Residual risk.** Metric definitions are operationalized in the `src/metrics/` directory. For reviewer traceability, the following anchors define the formal relationship between reported metrics and implementation classes:

| Metric Name | Implementation Anchor (`src/metrics/`) | Primary Class / Method |
| :--- | :--- | :--- |
| **Fidelity** | `fidelity.py` | `FidelityMetric` |
| **Stability** | `stability.py` | `StabilityMetric` |
| **Sparsity** | `sparsity.py` | `SparsityMetric` |
| **Faithfulness Gap** | `faithfulness.py` | `FaithfulnessMetric` (`faithfulness_gap`) |
| **Cost (ms)** | `cost.py` | `CostMetric` |

EEU remains uncomputed in EXP2 runtime and therefore cannot support energy-based claims.

### 5.3 Internal Validity (Runtime Comparability and Configuration Fidelity)

**Issue.** Runtime and accuracy-like comparisons depend on explainer variants and runtime bindings.

**Why it matters.** Apparent method differences can partially reflect implementation pathway choices rather than only conceptual method differences.

**Mitigation already done.** Within each matched cell, model artifact, transformed feature space, split/sampling seeds, and metric engine are held constant; effective runtime parameter bindings are disclosed. A standardized runtime constraint protocol (Cores=1, RAM=4GB, Timeout=300s) is enforced via the `ResourceGuard` utility in `src/utils/resource_control.py` to ensure architectural comparability.

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
