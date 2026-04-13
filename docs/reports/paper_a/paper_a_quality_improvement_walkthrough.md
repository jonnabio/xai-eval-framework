# Paper A Quality Improvement Walkthrough

## 1. Metadata

- **Date**: 2026-04-13
- **Scope**: Paper A quality-score improvement pass
- **Status**: Completed for safe non-result-tree edits
- **Commit intent**: Stage for next push cycle

## 2. Goal

Improve Paper A's high-standard assessment score while an EXP2 worker is still
running, without reading or rewriting the live experiment result snapshot as a
final analysis source.

The selected safe work items were:

- novelty delta;
- responsible-use section;
- artifact index;
- dependency declaration for the Paper A statistical analysis script.

## 3. Changes Completed

### 3.1 Manuscript updates

Updated `docs/reports/paper_a/paper_a_prototype_jmlr.tex` with:

- a novelty-delta table comparing Paper A against OpenXAI, Quantus, and BEExAI;
- a responsible-use and benchmark-boundaries subsection;
- a reference to the new Paper A artifact index.

These edits strengthen venue fit, novelty framing, claim discipline, and
reviewer traceability without changing the reported result snapshot.

### 3.2 Companion positioning note

Updated `docs/reports/paper_a/paper_a_jmlr_track_positioning.md` with:

- a filled novelty-delta section;
- the recommended benchmark-governance contribution wording;
- a link to the new artifact index.

This closes the prior novelty-delta placeholder in the JMLR-track companion note.

### 3.3 Artifact index

Added `docs/reports/paper_a/paper_a_artifact_index.md`.

The index maps the reviewer-facing artifact stack:

- manuscript and companion notes;
- experiment design and execution artifacts;
- result and recovery artifacts;
- analysis and figure scripts;
- dependency/environment files;
- public repository and Zenodo archive;
- final snapshot synchronization rule.

The synchronization rule states that manuscript evidence-accounting numbers
should be updated from `outputs/analysis/paper_a_exp2_stats/analysis_summary.json`
after the active worker finishes and the statistical analysis is regenerated.

### 3.4 Quality assessment note

Updated `docs/reports/paper_a/paper_a_quality_assessment.md` with an interim
improvement-pass record listing the completed actions and the deferred
post-worker actions.

### 3.5 Dependency declaration

Updated `requirements.txt` with:

- `scipy`;
- `scikit-posthocs==0.11.4`.

This makes the Paper A analysis dependency visible in the active dependency
path, not only in `requirements-frozen.txt`.

## 4. Verification

Completed checks:

- reviewed diffs for the modified paper and dependency files;
- searched for remaining placeholder markers in the edited Paper A files;
- verified edited files are ASCII-only;
- confirmed `rf_anchors_s42_n100` was still running and avoided analysis
  regeneration while the result snapshot is live;
- confirmed the staged work does not require touching `experiments/`.

Not run:

- LaTeX rebuild of `paper_a_prototype_jmlr.pdf`;
- `scripts/run_exp2_statistical_analysis.py`;
- regeneration of `outputs/analysis/paper_a_exp2_stats/`.

These are intentionally deferred until the active EXP2 worker finishes.

## 5. Next Steps

After the active `rf_anchors_s42_n100` worker finishes:

1. install/update dependencies in the intended analysis environment;
2. run `python scripts/run_exp2_statistical_analysis.py`;
3. update Paper A and the caveats note from
   `outputs/analysis/paper_a_exp2_stats/analysis_summary.json`;
4. rebuild the manuscript PDF;
5. commit the regenerated analysis outputs and synchronized manuscript counts.
