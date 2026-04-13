# Paper A Artifact Index

## 1. Metadata

- **Date**: 2026-04-13
- **Paper**: Paper A, JMLR-style benchmark manuscript
- **Purpose**: Reviewer-facing path map for the code, data, analysis, and reporting artifacts used by Paper A
- **Status**: Draft index; regenerate analysis counts after the active EXP2 worker finishes

## 2. Primary Manuscript Artifacts

| Artifact | Path | Role |
| :--- | :--- | :--- |
| JMLR manuscript source | `docs/reports/paper_a/paper_a_prototype_jmlr.tex` | Main Paper A LaTeX source. |
| Rendered manuscript | `docs/reports/paper_a/paper_a_prototype_jmlr.pdf` | Compiled PDF used for review. |
| Validity caveats | `docs/reports/paper_a/paper_a_validity_and_reporting_caveats.md` | Boundaries for statistical, construct, internal, external, and reproducibility validity. |
| JMLR-track positioning | `docs/reports/paper_a/paper_a_jmlr_track_positioning.md` | Companion note for benchmark-track contribution framing. |
| Quality assessment | `docs/reports/paper_a/paper_a_quality_assessment.md` | Internal scorecard and 85+ improvement plan. |

## 3. Experiment Design and Execution Artifacts

| Artifact | Path | Role |
| :--- | :--- | :--- |
| EXP2 manifest | `configs/experiments/exp2_scaled/manifest.yaml` | Declares the planned 300-run robustness grid. |
| EXP2 configuration files | `configs/experiments/exp2_scaled/*.yaml` | Per-cell model, explainer, seed, sample-size, metric, and output settings. |
| Experiment runner | `src/experiment/runner.py` | Executes individual configured benchmark runs. |
| Batch runner | `src/experiment/batch_runner.py` | Supports multi-run experiment orchestration. |
| Resource guard | `src/utils/resource_control.py` | Runtime constraint helper used for comparable execution conditions. |

## 4. Result and Recovery Artifacts

| Artifact | Path | Role |
| :--- | :--- | :--- |
| EXP2 result tree | `experiments/exp2_scaled/results/` | Per-run outputs and instance-level artifacts for the main robustness benchmark. |
| SHAP recovery batch | `outputs/batch_results.csv` | Recovery overlay source for MLP/SVM SHAP rows used by the merged Paper A snapshot. |
| Paper-level comparison export | `outputs/paper_analysis/paper_comparison.csv` | Existing paper-facing comparison table. |
| Complete comparison export | `outputs/paper_analysis/complete_comparison.csv` | Broader comparison export used for exploratory/reporting context. |

## 5. Analysis and Figure Artifacts

| Artifact | Path | Role |
| :--- | :--- | :--- |
| Statistical analysis driver | `scripts/run_exp2_statistical_analysis.py` | Deterministically generates Paper A inferential tables from qualified EXP2 inputs. |
| Expected analysis output directory | `outputs/analysis/paper_a_exp2_stats/` | Target directory for run inventory, run-level metrics, block summaries, Friedman tests, Nemenyi tables, Wilcoxon tests, uncertainty tables, paired-cell exports, and `analysis_summary.json`. |
| Figure generation driver | `scripts/generate_paper_a_figures.py` | Generates Paper A figures from qualified analysis outputs. |

## 6. Dependency and Environment Artifacts

| Artifact | Path | Role |
| :--- | :--- | :--- |
| Runtime requirements | `requirements.txt` | Active dependency declaration for project workflows. |
| Frozen requirements | `requirements-frozen.txt` | Fully pinned environment snapshot; currently includes `scikit-posthocs==0.11.4`. |
| Conda environment | `environment.yml` | Conda environment entry point, including pip installation from `requirements-frozen.txt`. |

## 7. Submission Snapshot and Archive

| Artifact | Location | Role |
| :--- | :--- | :--- |
| Public repository | `https://github.com/jonnabio/xai-eval-framework` | Public code and artifact repository. |
| Zenodo archive | `https://doi.org/10.5281/zenodo.19297724` | Version-specific archive for release tag `paper-a-submission-2026-03-28`. |

## 8. Snapshot Synchronization Rule

For manuscript submission, all numerical evidence-accounting statements should
come from `outputs/analysis/paper_a_exp2_stats/analysis_summary.json`.

The following manuscript quantities must be checked against that generated
summary after the active EXP2 worker has finished:

- present result artifacts;
- empty or malformed artifacts;
- recovery overlay rows;
- overlay replacements;
- analyzable unique runs;
- unresolved cells;
- complete `(model, sample-size)` blocks;
- SHAP-LIME matched-cell counts.

This prevents manuscript drift between live experiment outputs, recovery CSVs,
and the final benchmark snapshot.
