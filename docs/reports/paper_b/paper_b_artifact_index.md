# Paper B Artifact Index

## 1. Metadata

- **Date**: 2026-04-15
- **Paper**: Paper B — *LIME vs SHAP: A Paired Empirical Comparison*
- **Purpose**: Reviewer-facing path map for the code, data, analysis, and reporting artifacts used by Paper B
- **Status**: Draft index; based on EXP2-scaled robustness cohort (299/300 committed results; `svm_shap_s456_n200` still in-flight on `jon_asus`)

## 2. Primary Manuscript Artifacts

| Artifact | Path | Role |
| :--- | :--- | :--- |
| JMLR manuscript source | `docs/reports/paper_b/paper_b_prototype_jmlr.tex` | Main Paper B LaTeX source, JMLR style with journal header and attribution footer. |
| JMLR rendered manuscript | `docs/reports/paper_b/paper_b_prototype_jmlr.pdf` | Compiled JMLR-branded PDF for review and journal submission. |
| Neutral manuscript source | `docs/reports/paper_b/paper_b_prototype_neutral.tex` | Internal-conference wrapper that reuses the main LaTeX source with the JMLR style package in unbranded preprint mode. |
| Neutral rendered manuscript | `docs/reports/paper_b/paper_b_prototype_neutral.pdf` | Compiled PDF for internal university presentation without visible JMLR journal branding. |
| Markdown mirror | `docs/reports/paper_b/paper_b_prototype_jmlr.md` | Markdown version of manuscript content for quick reference and diffing. |
| JMLR style file | `docs/reports/paper_b/jmlr2e.sty` | Local copy of JMLR2e style package. |

## 3. Experiment Design and Execution Artifacts

| Artifact | Path | Role |
| :--- | :--- | :--- |
| EXP2 manifest | `configs/experiments/exp2_scaled/manifest.yaml` | Declares the planned 300-run robustness grid. |
| EXP2 LIME/SHAP configs | `configs/experiments/exp2_scaled/[logreg|rf|xgb|svm|mlp]_[lime|shap]_s*_n*.yaml` | Per-cell configurations for the 150 LIME/SHAP runs. |
| Experiment runner | `src/experiment/runner.py` | Executes individual configured benchmark runs. |
| Batch runner | `src/experiment/batch_runner.py` | Supports multi-run experiment orchestration. |
| Resource guard | `src/utils/resource_control.py` | Runtime constraint helper for comparable execution conditions. |

## 4. Result Artifacts

| Artifact | Path | Role |
| :--- | :--- | :--- |
| EXP2 result tree | `experiments/exp2_scaled/results/` | Per-run outputs and instance-level artifacts for the robustness benchmark. |
| LIME result subdirs | `experiments/exp2_scaled/results/*/lime/` | Per-model LIME metric outputs. |
| SHAP result subdirs | `experiments/exp2_scaled/results/*/shap/` | Per-model SHAP metric outputs. |
| Recovery overlay | `outputs/batch_results.csv` | Recovery overlay source for MLP/SVM SHAP rows. |

## 5. Analysis and Figure Artifacts

| Artifact | Path | Role |
| :--- | :--- | :--- |
| Figure generation driver | `scripts/generate_paper_b_figures.py` | Generates Paper B-specific figures from EXP2 analysis outputs. |
| Paper metrics generator | `scripts/generate_paper_metrics.py` | Generates per-paper statistical summary metrics. |
| Statistical analysis driver | `scripts/run_exp2_statistical_analysis.py` | Deterministically generates inferential tables from qualified EXP2 inputs. |
| Analysis output directory | `outputs/analysis/paper_a_exp2_stats/` | Shared EXP2 analysis outputs (run inventory, run-level metrics, Wilcoxon tests, paired-cell exports etc.). |
| Cross-study integration driver | `scripts/integrate_experiment_evidence.py` | Generates EXP1/EXP2/EXP3 evidence handoff tables and the Paper B EXP3 integration addendum. |
| EXP3 integration addendum | `outputs/analysis/integrated_evidence/paper_b_exp3_addendum.md` | Paper B context note for using EXP3 as supporting evidence rather than a replacement for the SHAP-LIME paired test. |

## 6. Dependency and Environment Artifacts

| Artifact | Path | Role |
| :--- | :--- | :--- |
| Runtime requirements | `requirements.txt` | Active dependency declaration. |
| Frozen requirements | `requirements-frozen.txt` | Fully pinned environment snapshot. |
| Conda environment | `environment.yml` | Conda environment entry point. |

## 7. Key Claims and Evidence Snapshot

- **Analysis cohort**: 75 matched SHAP-LIME cells on identical (model, seed, N) coordinates.
- **SHAP dominance**: Stability, fidelity, faithfulness gap — all statistically significant with Holm correction.
- **LIME advantage**: Sparser explanations; lower runtime (median 65.7 ms vs 684.1 ms for SHAP; means 3,660.7 ms vs 11,708.3 ms due to kernel-SHAP heavy tails).
- **Inference units**: Paired Wilcoxon tests, paired effect sizes ($d_z$), Holm correction.
- **Models**: logreg, rf, xgb, svm, mlp; seeds 42/123/456/789/999; N ∈ {50, 100, 200}.

## 8. Build Instructions

To reproduce PDFs from source:

```powershell
# JMLR branded version
.\tools\tectonic-portable\tectonic.exe .\docs\reports\paper_b\paper_b_prototype_jmlr.tex

# Neutral/unbranded version (for internal presentations)
.\tools\tectonic-portable\tectonic.exe .\docs\reports\paper_b\paper_b_prototype_neutral.tex
```
