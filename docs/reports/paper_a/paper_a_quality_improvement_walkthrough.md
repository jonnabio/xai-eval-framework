# Paper A Quality Improvement Walkthrough

## 1. Metadata

- **Date**: 2026-04-14
- **Scope**: Paper A quality-score improvement pass
- **Status**: Manuscript and assessment synchronized to regenerated EXP2 analysis
- **Commit intent**: Stage for next push cycle

## 2. Goal

Improve Paper A's high-standard assessment score while preserving the
handoff/claim protocol and using the regenerated EXP2 analysis as the single
source for result-count updates.

The selected first-pass safe work items were:

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
- after experiment consolidation, installed the declared
  `scikit-posthocs==0.11.4` dependency in the active environment;
- ran `python scripts/run_exp2_statistical_analysis.py`;
- verified `outputs/analysis/paper_a_exp2_stats/analysis_summary.json` reports
  299 committed artifacts, 275 analyzable unique runs, 30 overlay rows, 29
  replacement rows, 15/15 complete Friedman blocks, 45 primary SHAP-LIME
  matched pairs, and 75 all-model SHAP-LIME matched pairs;
- synchronized `paper_a_prototype_jmlr.tex`, `paper_a_prototype.md`,
  `paper_a_validity_and_reporting_caveats.md`, and
  `paper_a_quality_assessment.md` to the regenerated snapshot.
- rebuilt `paper_a_prototype_jmlr.pdf` with portable Tectonic 0.16.8 after
  confirming `latexmk` and `pdflatex` were unavailable on this workstation.

Not run:

- archival release/DOI refresh for the April 2026 result cut.

## 5. Next Steps

Before the next submission/release cut:

1. explicitly bundle or force-add `outputs/analysis/paper_a_exp2_stats/`,
   because `outputs/` is ignored by default;
2. resolve or document the claimed `svm_shap_s456_n200` per-run artifact so the
   committed tree no longer relies only on the overlay for that SHAP cell;
3. diagnose the 25 empty Anchors/DiCE artifacts and decide whether targeted
   reruns are worth the compute cost;
4. refresh the April 2026 release/DOI after the paper source, PDF, and analysis
   outputs are synchronized.
