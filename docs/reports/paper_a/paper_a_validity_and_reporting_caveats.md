# Paper A Validity and Reporting Caveats

This companion note describes the validity boundaries and technical constraints of the JMLR manuscript draft.

## 5. Validity and Reporting Caveats

### 5.1 Statistical Conclusion Validity

**Issue.** The current live EXP2 robustness cohort contains 52 unavailable cells from the planned 300-run grid: 26 are missing folders, 25 are present-but-empty result artifacts, and one result artifact is malformed.

**Why it matters.** Missing and invalid runs reduce inferential coverage and can affect confidence in estimated method rankings and the reported quality-cost frontier if missingness is systematic.

**Mitigation already done.** The analysis uses explicit artifact qualification, excludes malformed/empty artifacts, applies block-complete filtering for omnibus tests, and uses matched-cell filtering for paired tests. In the current live repo snapshot, this yields 274 present result artifacts and 248 analyzable runs out of the planned 300 (82.7% analyzable coverage).

**Residual risk / Systematic Diagnosis.** Availability loss is systematic and now spans both missing cells and invalid present artifacts:

1. **Missing result cells (26 cells):** These are concentrated in **Anchors (11)**, **DiCE (11)**, and **SHAP (4)**, with the heaviest model-level gaps in MLP, RF, and SVM configurations. This means the live grid no longer supports claims of near-complete factor coverage.
2. **Empty result artifacts (25 cells):** These are concentrated in **Anchors (18)** and **DiCE (7)**. Anchors empties are especially pronounced in `logreg` and `mlp`, while DiCE empties remain distributed across several higher-cost model families. These should be treated as MNAR-style operational failures rather than ignorable random omissions.
3. **Serialization corruption (1 artifact):** Specifically `svm_shap_s999_n200`. This artifact remains malformed due to an invalid control character in the JSON stream.

Omnibus results remain valid as the filtering protocol still admits model-size blocks with 100% explainer family coverage (15/15 blocks), but the effective dataset is reduced to 248 analyzed runs. Because unavailable cells are concentrated in Anchors and DiCE, their global quality/cost summaries should be interpreted cautiously; LIME is the only method with full 75/75 availability in the current live snapshot.

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

**Mitigation already done.** Within each matched cell, model artifact, transformed feature space, split/sampling seeds, and metric engine are held constant; effective runtime parameter bindings are disclosed. A standardized runtime constraint protocol (Cores=1, RAM=4GB, Timeout=300s) is configured in the experiment layer via the `ResourceGuard` utility in `src/utils/resource_control.py` to improve architectural comparability.

### 5.4 External Validity

**Issue.** Evidence is benchmarked on a single task setting and reported pairwise contrasts are restricted to shared model-family subsets.

**Why it matters.** Method rankings and trade-offs may shift across datasets, modalities, and task definitions.

**Mitigation already done.** The benchmark includes multiple model families, multiple explainers, and seed/sample-size heterogeneity within the evaluated setting.

**Residual risk.** Generalization beyond the current benchmark context is not established and should be treated as an open empirical question.

### 5.5 Reproducibility and Operational Validity

**Issue.** Strong reproducibility claims require both deterministic pipelines and durable artifact packaging.

**Why it matters.** Without auditable lineage and re-execution hooks, reported benchmark conclusions are difficult to verify independently.

**Mitigation already done.** FOM-7 defines stage-gated execution with required artifacts; run inventories, inference exports, and reproducibility scripts are provided.

**Residual risk.** Current reproducibility materials are available in the public repository at `https://github.com/jonnabio/xai-eval-framework` for the submission snapshot being archived as release tag `paper-a-submission-2026-03-28`. Long-term archival persistence remains a residual risk until Zenodo completes deposition and assigns the version-specific DOI for this tagged snapshot.
