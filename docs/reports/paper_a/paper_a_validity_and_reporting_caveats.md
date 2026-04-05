# Paper A Validity and Reporting Caveats

This companion note describes the validity boundaries and technical constraints of the JMLR manuscript draft.

## 5. Validity and Reporting Caveats

### 5.1 Statistical Conclusion Validity

**Issue.** The committed `experiments/exp2_scaled/results` tree still contains 53 unavailable artifact cells from the planned 300-run grid: 27 are missing folders, 25 are present-but-empty result artifacts, and one result artifact is malformed. The current merged recovery analysis now overlays 30 SHAP reruns from `outputs/batch_results.csv`, which reduces the unresolved gap to 48 unavailable unique cells.

**Why it matters.** Missing and invalid runs reduce inferential coverage and can affect confidence in estimated method rankings and the reported quality-cost frontier if missingness is systematic.

**Mitigation already done.** The analysis uses explicit artifact qualification, excludes malformed/empty artifact-tree runs, applies block-complete filtering for omnibus tests, and uses matched-cell filtering for paired tests. In the current merged recovery snapshot, this combines 273 committed result artifacts with a 30-row SHAP recovery batch, replacing 25 existing `mlp_shap`/`svm_shap` runs and filling 5 previously unavailable cells. The resulting evidence set contains 252 analyzable unique runs out of the planned 300 (84.0% analyzable coverage).

**Residual risk / Systematic Diagnosis.** Availability loss remains systematic after the recovery overlay:

1. **Residual unavailable cells (48 cells):** After the SHAP recovery overlay, unresolved availability loss is concentrated in **Anchors (30)** and **DiCE (18)**. SHAP is fully covered in the merged snapshot through the combination of committed artifacts and the recovery batch, and LIME remains fully covered at 75/75.
2. **Residual missing result cells (23 cells):** These remaining missing cells are now confined to Anchors and DiCE families, with the heaviest model-level gaps in `logreg`, `rf`, and `mlp` configurations. This means the grid still falls short of near-complete factor coverage even after SHAP recovery.
3. **Residual empty result artifacts (25 cells):** These continue to be concentrated in **Anchors** and **DiCE**. Anchors empties remain especially pronounced in `logreg` and `mlp`, while DiCE empties remain distributed across several higher-cost model families. These should still be treated as MNAR-style operational failures rather than ignorable random omissions.

Omnibus results remain valid as the filtering protocol still admits model-size blocks with 100% explainer family coverage (15/15 blocks), but the effective merged dataset is still reduced to 252 analyzed runs. Because unresolved unavailable cells are concentrated in Anchors and DiCE, their global quality/cost summaries should be interpreted cautiously even though the SHAP availability problem has been materially reduced by the recovery batch.

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

**Residual risk.** Archival persistence for the submission snapshot is now mitigated: the materials are available in the public repository at `https://github.com/jonnabio/xai-eval-framework` and archived in Zenodo for release tag `paper-a-submission-2026-03-28` under DOI [`10.5281/zenodo.19297724`](https://doi.org/10.5281/zenodo.19297724). Remaining residual risks concern result availability gaps and external-validity limits, not archive discoverability.
