# Paper A Validity and Reporting Caveats

This companion note describes the validity boundaries and technical constraints of the JMLR manuscript draft.

## 5. Validity and Reporting Caveats

### 5.1 Statistical Conclusion Validity

**Issue.** The committed `experiments/exp2_scaled/results` tree still contains 26 unavailable artifact cells from the planned 300-run grid: one missing SHAP result artifact and 25 present-but-empty result artifacts. The current merged recovery analysis overlays 30 SHAP reruns from `outputs/batch_results.csv`, which fills the missing SHAP cell for analysis and reduces the unresolved gap to 25 unavailable unique cells.

**Why it matters.** Missing and invalid runs reduce inferential coverage and can affect confidence in estimated method rankings and the reported quality-cost frontier if missingness is systematic.

**Mitigation already done.** The analysis uses explicit artifact qualification, excludes empty artifact-tree runs, applies block-complete filtering for omnibus tests, and uses matched-cell filtering for paired tests. In the current merged recovery snapshot, this combines 299 committed result artifacts with a 30-row SHAP recovery batch, replacing 29 existing `mlp_shap`/`svm_shap` runs and filling one previously unavailable SHAP cell. The resulting evidence set contains 275 analyzable unique runs out of the planned 300 (91.7% analyzable coverage).

**Residual risk / Systematic Diagnosis.** Availability loss remains systematic after the recovery overlay:

1. **Residual unavailable cells (25 cells):** After the SHAP recovery overlay, unresolved availability loss is concentrated in **Anchors (18)** and **DiCE (7)**. SHAP and LIME are fully covered in the merged snapshot through the combination of committed artifacts and the recovery batch.
2. **Residual missing result cells (0 cells after overlay):** The committed tree still lacks `experiments/exp2_scaled/results/svm_shap/seed_456/n_200/results.json`, but the recovery overlay covers that cell for the merged analysis. The corresponding `svm_shap_s456_n200` run is currently claim-tracked outside the paper evidence overlay.
3. **Residual empty result artifacts (25 cells) — root cause diagnosed 2026-07-22:** These are concentrated in **Anchors** and **DiCE**. Anchors empties are distributed across `logreg`, `mlp`, and `xgb`; DiCE empties are distributed across `logreg`, `mlp`, `svm`, and `xgb`. A live rerun of one empty cell (`logreg_anchors_s123_n50`) reproduced the exact failure: the `alibi` and `dice-ml` packages the codebase requires for these two explainers are not importable in the project's active `.venv` (Python 3.13). Each per-instance explanation call raises an `ImportError`, which the runner catches per-instance rather than per-run, so the run "completes" and writes a valid-but-empty `results.json` instead of crashing. This is a deterministic environment gap, not an MNAR-style random operational failure. It is not a quick fix: `alibi==0.9.6` (the only version with a modern Anchors API) requires `numpy<2.0`, which has no prebuilt wheel for Python 3.13 and is incompatible with the `numpy==2.2.6` this environment's `scipy`/`scikit-learn` already require; a source build of `numpy<2.0` failed on this machine's toolchain, and forcing an unconstrained resolver install downgrades `alibi` to version 0.5.5 (year-2021 Anchors internals, not recorded as the version used for the other 274 successful Anchors/DiCE runs) while breaking `protobuf`-dependent tooling elsewhere in the environment. Closing this gap requires a separate Python (`<3.13`, `numpy<2.0`) environment dedicated to these 25 cells; it was not attempted in this pass. These 25 cells remain excluded from confirmatory inference exactly as before.

Omnibus results remain valid as the filtering protocol still admits model-size blocks with 100% explainer family coverage (15/15 blocks), but the effective merged dataset is still reduced to 275 analyzed runs. Because unresolved unavailable cells are concentrated in Anchors and DiCE, their global quality/cost summaries should be interpreted cautiously even though the SHAP availability problem is covered by the recovery batch.

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

EEU remains uncomputed in the primary benchmark (EXP2) runtime and therefore cannot support energy-based claims.

### 5.3 Internal Validity (Runtime Comparability and Configuration Fidelity)

**Issue.** Runtime and accuracy-like comparisons depend on explainer variants and runtime bindings.

**Why it matters.** Apparent method differences can partially reflect implementation pathway choices rather than only conceptual method differences.

**Mitigation already done.** Within each matched cell, model artifact, transformed feature space, split/sampling seeds, and metric engine are held constant; effective runtime parameter bindings are disclosed. A standardized runtime constraint protocol (Cores=1, RAM=4GB, Timeout=300s) is configured in the experiment layer via the `ResourceGuard` utility in `src/utils/resource_control.py` to improve architectural comparability.

### 5.4 External Validity

**Issue.** Evidence is benchmarked on a single task setting and reported pairwise contrasts are restricted to shared model-family subsets.

**Why it matters.** Method rankings and trade-offs may shift across datasets, modalities, and task definitions.

**Mitigation already done.** The benchmark includes multiple model families, multiple explainers, and seed/sample-size heterogeneity within the evaluated setting. As of 2026-07-24, a bounded external-validation check (EXP3) ran SHAP in tree mode on `rf`/`xgb` across three seeds on two additional public tabular datasets, Breast Cancer Wisconsin and German Credit ($n=100$ per class each). SHAP Stability transferred well (${\geq}0.95$) for both models on Breast Cancer and for `rf` on German Credit, but dropped to 0.60 for `xgb` on German Credit — a documented exception, not a uniform confirmation. Full results are in `docs/reports/paper_a/paper_a_prototype_jmlr.tex` Section "External Validity Check: Cross-Dataset SHAP Stability" and in `experiments/exp3_cross_dataset/results/`.

**Residual risk.** This check covers only SHAP; the matching Anchors-based `exp3_cross_dataset` configs (12 of the 24 planned EXP3 cells) could not be run in this pass — same `alibi`/`numpy<2.0`/Python 3.13 environment gap as the 25 empty EXP2 cells (Section 5.1). LIME and DiCE were never in the EXP3 design. Generalization of the full four-method ranking beyond Adult Income remains an open empirical question.

### 5.5 Reproducibility and Operational Validity

**Issue.** Strong reproducibility claims require both deterministic pipelines and durable artifact packaging.

**Why it matters.** Without auditable lineage and re-execution hooks, reported benchmark conclusions are difficult to verify independently.

**Mitigation already done.** FOM-7 defines stage-gated execution with required artifacts; run inventories, inference exports, and reproducibility scripts are provided.

**Residual risk.** Archival persistence for the prior submission snapshot is mitigated: those materials are available in the public repository at `https://github.com/jonnabio/xai-eval-framework` and archived in Zenodo for release tag `paper-a-submission-2026-03-28` under DOI [`10.5281/zenodo.19297724`](https://doi.org/10.5281/zenodo.19297724). The refreshed April 2026 result cut reported in the updated draft still needs a new versioned release and DOI before submission. Remaining residual risks concern result availability gaps and external-validity limits, not archive discoverability.
