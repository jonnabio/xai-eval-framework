# Results Organization Proposal

This document is the proposed single entry point for understanding result artifacts in the project.

It is intentionally documentation-first. The goal is to make the current result landscape understandable before any disruptive moves or renames are attempted.

## 1. Problem Statement

Result artifacts are currently spread across several roots with different meanings:

- raw experiment outputs under `experiments/...`
- recovery outputs under `experiments/recovery/...`
- derived exports under `outputs/...`
- paper-specific figures and reporting assets under `docs/reports/...`

This is not inherently wrong, but the semantics are not obvious from the current structure alone. A new contributor, reviewer, or thesis examiner would have to infer too much context from scripts and manuscript drafts.

## 2. Current-State Audit

### 2.1 Raw Experiment Artifact Roots

Primary raw results:

- `experiments/exp1_adult/results/`
- `experiments/exp2_comparative/results/`
- `experiments/exp2_scaled/results/`

Additional result-like experiment roots:

- `experiments/exp1_adult/reproducibility/`
- `experiments/exp1_adult/llm_eval/`
- `experiments/exp1_adult/human_eval/`
- `experiments/recovery/phase1/results/`
- `experiments/sample_data/results/`

### 2.2 Derived Output Roots

Current derived outputs:

- `outputs/batch_results.csv`
- `outputs/batch_manifest.json`
- `outputs/recovery_results.csv`
- `outputs/paper_analysis/`
- `outputs/test_cf/`

### 2.3 Reporting / Narrative Roots

Interpretive and paper-facing assets:

- `docs/reports/paper_a/`
- `docs/reports/paper_b/`
- `docs/reports/paper_c/`

### 2.4 Current Semantic Ambiguity

The following distinctions are real in the repo but not clearly documented in one place:

1. committed raw result trees versus recovery overlays
2. run-level artifacts versus merged CSV overlays
3. raw run outputs versus paper-ready derived figures
4. "present in the tree" versus "qualified/analyzable"

## 3. Key Findings

### 3.1 What Is Already Good

- Raw experiment outputs are mostly kept out of `docs/`, which is correct.
- `experiments/.../results/` is a sensible home for committed per-run artifacts.
- `outputs/...` is a sensible home for merged and derived exports.
- `docs/reports/...` is a sensible home for thesis and paper interpretation.

### 3.2 What Is Still Messy

- There is no single hub that explains result semantics.
- Recovery outputs are operationally important but not visually integrated into the results story.
- `outputs/batch_results.csv` currently acts as an overlay source for EXP2 analysis, but that meaning is mostly documented in scripts and paper drafts.
- Some important distinctions, like "artifact-qualified" versus merely "present on disk", live in manuscript text instead of results documentation.

## 4. Recommended Information Architecture

The project should standardize on the following conceptual layers.

### 4.1 Layer A: Raw Committed Run Artifacts

Definition:

- one folder per committed run
- generated directly by the runner
- contains `results.json`, `metrics.csv`, and possibly `instances/`

Canonical roots:

- `experiments/exp1_adult/results/`
- `experiments/exp2_comparative/results/`
- `experiments/exp2_scaled/results/`
- ready for partitioned execution; smoke result present:
  `experiments/exp3_cross_dataset/results/`

### 4.2 Layer B: Recovery / Remediation Artifacts

Definition:

- reruns or repair-oriented outputs created to fill gaps or replace unusable cells

Canonical roots:

- `experiments/recovery/phase1/results/`
- selected CSV overlays in `outputs/`

These should not be confused with the base committed benchmark tree.

### 4.3 Layer C: Derived Analysis Outputs

Definition:

- merged tabular exports
- statistical summaries
- correlation files
- comparison CSVs
- visual analytics not yet committed as manuscript figures

Canonical root:

- `outputs/`

### 4.4 Layer D: Paper / Thesis Assets

Definition:

- manuscript-source tables
- publication figures
- claim-facing reporting assets

Canonical root:

- `docs/reports/`

## 5. Proposed Documentation Structure

To match the new `docs/experiments` hub, results should get a parallel documentation hub:

```text
docs/results/
├── README.md
├── exp1_adult/
│   └── README.md
├── exp2_comparative/
│   └── README.md
├── exp2_scaled/
│   ├── README.md
│   └── QUALIFICATION.md
└── exp3_cross_dataset/
    └── README.md
```

Each family README should answer:

- where raw artifacts live
- what counts as a valid run artifact
- whether recovery overlays exist
- where derived outputs live
- where paper-facing assets live
- what a reviewer should cite as the result source of truth

## 6. Proposed Source-of-Truth Rules

### 6.1 For Raw Run Presence

Source of truth:

- `experiments/.../results/...`

### 6.2 For Recovery Overlays

Source of truth:

- the recovery result tree plus any explicitly documented overlay CSVs

Example:

- `experiments/recovery/phase1/results/`
- `outputs/batch_results.csv`

### 6.3 For Analyzable / Qualified Cohorts

Source of truth:

- analysis scripts and their documented qualification rules

This should be summarized in `docs/results/...`, not only in manuscript text.

### 6.4 For Paper Figures / Tables

Source of truth:

- `docs/reports/...`

## 7. Proposed Minimal-Change Implementation

This is the recommended first pass because it improves clarity without breaking paths.

### 7.1 Keep Existing Artifact Roots

Do not move:

- `experiments/.../results/...`
- `experiments/recovery/...`
- `outputs/...`
- `docs/reports/...`

### 7.2 Add Results Documentation Only

Add:

- `docs/results/README.md`
- per-family result guides

### 7.3 Add Cross-Links

Link:

- experiment design docs to result docs
- result docs to raw artifact roots
- result docs to analysis outputs
- result docs to reporting roots

## 8. Proposed Full-Cleanup Option

This is a later, riskier option and should only happen after the docs-first layer is stable.

Potential later moves:

- normalize special-case outputs into clearer `outputs/analysis/...` subfolders
- standardize recovery overlays under an explicit `outputs/recovery/` root
- reduce ad hoc result-like folders that do not clearly belong to raw artifacts

This should not happen while active runners or scripts still assume the current paths.

## 9. Path-by-Path Mapping Proposal

| Current Path | Proposed Role | Recommendation |
|-------------|---------------|----------------|
| `experiments/exp1_adult/results/` | raw committed artifacts | keep |
| `experiments/exp1_adult/reproducibility/` | reproducibility result family | keep, document |
| `experiments/exp1_adult/llm_eval/` | evaluation artifact family | keep, document |
| `experiments/exp1_adult/human_eval/` | evaluation artifact family | keep, document |
| `experiments/exp2_comparative/results/` | raw committed artifacts | keep |
| `experiments/exp2_scaled/results/` | raw committed artifacts | keep |
| `experiments/recovery/phase1/results/` | recovery artifacts | keep, document as non-base layer |
| `outputs/batch_results.csv` | recovery overlay / derived export | keep, document explicitly |
| `outputs/recovery_results.csv` | recovery summary export | keep, document |
| `outputs/paper_analysis/` | derived analysis | keep |
| `docs/reports/paper_a/` | paper-facing interpretation and assets | keep |
| `docs/reports/paper_b/` | paper-facing interpretation and assets | keep |
| `docs/reports/paper_c/` | paper-facing interpretation and assets | keep |

## 10. Family Guides

Start here for family-specific result semantics:

- [EXP1 Adult Results](./exp1_adult/README.md)
- [EXP2 Comparative Results](./exp2_comparative/README.md)
- [EXP2 Scaled Results](./exp2_scaled/README.md)
- [EXP2 Scaled Artifact Qualification](./exp2_scaled/QUALIFICATION.md)
- [EXP3 Cross-Dataset Results](./exp3_cross_dataset/README.md)
- [EXP1-EXP2-EXP3 Integration Pipeline](../analysis/EXP1_EXP2_EXP3_INTEGRATION_PIPELINE.md)

EXP3 now has a completed raw result cohort (`24 / 24` planned runs). The
integrated evidence package generated from EXP1, EXP2, and EXP3 lives under:

- `outputs/analysis/integrated_evidence/`

## 11. Migration Sequence

Recommended order:

1. Create `docs/results/README.md`
2. Add per-family result READMEs
3. Cross-link from `docs/experiments/...`
4. Document EXP2 overlay and qualification logic clearly
5. Generate integrated evidence for thesis/paper handoff with
   `python3 scripts/integrate_experiment_evidence.py`
6. Only after that, consider any filesystem cleanup

## 12. Risks

### 12.1 Operational Risk

Many scripts assume current paths, especially for:

- EXP2 result scanning
- recovery overlay loading
- managed runner syncing
- status dashboards

### 12.2 Reporting Risk

Paper drafts already reference:

- `experiments/exp2_scaled/results/`
- `outputs/batch_results.csv`
- `docs/reports/paper_a/`

Moving these paths now would create unnecessary churn.

### 12.3 Recommendation

Do not move result directories yet.

First make them understandable through a documentation layer. Then revisit whether any physical reorganization is still necessary.

## 13. Recommended Next Step

Continue the minimal-change version:

- keep current storage
- use `docs/results` as the single human-readable hub for result semantics
- use `outputs/analysis/integrated_evidence/` as the generated handoff layer for
  thesis and paper integration
