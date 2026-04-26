# EXP1-EXP2-EXP3 Integration Pipeline

Date: 2026-04-26
Status: Active pipeline

## Purpose

This pipeline prepares the project to analyze EXP3 together with EXP1 and EXP2
without collapsing their different evidentiary roles.

The integration rule is:

- EXP1 is the calibration and reproducibility layer.
- EXP2 is the primary confirmatory benchmark layer.
- EXP3 is the external tabular validation layer.

EXP3 should qualify and strengthen the thesis claim, not replace the EXP2
statistical cohort.

## Roles Applied

Per `docs/bmad/roles.md`, this pipeline combines:

- Data Scientist: qualify analyzable runs, preserve statistical boundaries, and
  distinguish raw files from admissible evidence.
- Scientific Editor: convert metric summaries into thesis and paper narrative
  fragments with bounded claims.

## Script

Run:

```bash
python3 scripts/integrate_experiment_evidence.py
```

The script uses only the Python standard library. This is deliberate so it can
run in WSL, Linux, or the Windows EXP3 handoff environment without requiring the
full scientific stack.

## Inputs

| Evidence layer | Input | Role |
|---|---|---|
| EXP1 | `experiments/exp1_adult/results/{rf,xgb}_{lime,shap}/results.json` | Adult calibration baseline |
| EXP2 | `experiments/exp2_scaled/results/` | Primary Adult robustness benchmark |
| EXP2 recovery | `outputs/batch_results.csv` | Recovery overlay for selected SHAP cells |
| EXP3 | `experiments/exp3_cross_dataset/results/` | Breast Cancer + German Credit validation |

## Qualification Rules

For EXP2, the pipeline follows the same distinction used in the thesis results
chapter:

- a present `results.json` file is not automatically analyzable;
- empty or metricless EXP2 artifacts are excluded from the raw qualified layer;
- recovery overlay rows from `outputs/batch_results.csv` replace or fill matching
  EXP2 SHAP cells;
- the merged EXP2 analyzable cohort is reported separately from raw file count.

For EXP3, the completed 24-run matrix is included as a validation package. EXP3
is not pooled into the EXP2 Friedman or SHAP-LIME confirmatory tests.

## Outputs

Generated root:

```text
outputs/analysis/integrated_evidence/
```

Generated artifacts:

| Artifact | Role |
|---|---|
| `evidence_snapshot.json` | Machine-readable counts, source roots, method summaries, and publication traceability |
| `run_level_metrics.csv` | Normalized EXP1/EXP2/EXP3 run-level metric table |
| `method_summary.csv` | Method-level means by experiment |
| `dataset_method_summary.csv` | Dataset/method means for cross-dataset interpretation |
| `model_method_summary.csv` | Model/dataset/method means for caveat discovery |
| `publication_traceability.csv` | Mapping from evidence layer to thesis and Paper A/B/C use |
| `integration_summary.md` | Human-readable scientific analysis handoff |
| `thesis_fragment_es.qmd` | Spanish thesis-ready integration fragment |
| `paper_a_exp3_addendum.md` | Paper A integration note |
| `paper_b_exp3_addendum.md` | Paper B integration note |
| `paper_c_exp3_addendum.md` | Paper C integration note |

## Current Snapshot

As generated on 2026-04-26:

```text
EXP1 core runs: 4 / 4
EXP2 present result files: 299 / 300
EXP2 qualified raw runs before overlay: 274
EXP2 recovery overlay rows: 30
EXP2 analyzable runs after overlay: 275 / 300
EXP3 completed runs: 24 / 24
Integrated run rows: 303
```

## Thesis Integration

Use `outputs/analysis/integrated_evidence/thesis_fragment_es.qmd` as the first
draft for the Chapter 4 integrated discussion.

Recommended thesis wording:

> benchmark centrado en Adult con validacion tabular externa en dos dominios

The thesis should continue to locate confirmatory statistics in EXP2 and use
EXP3 for external-validity language.

## Paper Integration

Paper A:

- Use EXP3 to strengthen framework portability and artifact-contract claims.
- Do not use EXP3 as a new omnibus benchmark.

Paper B:

- Keep the primary claim as SHAP-LIME paired evidence from EXP2.
- Use EXP3 as supporting context showing that SHAP's technical-quality profile
  persists against Anchors in additional tabular domains.

Paper C:

- Use EXP3 to motivate layered evaluation and future semantic/LLM-judge studies.
- Do not claim semantic preference validation from EXP3 alone.

## Guardrails

- Do not merge EXP2 and EXP3 into one hypothesis test unless a new statistical
  design is explicitly documented.
- Do not describe EXP3 as universal cross-domain evidence.
- Keep "raw file count", "qualified run", and "publication claim" separate.
