# Paper A Quality Assessment

## 1. Metadata

- **Date**: 2026-04-14 (original assessment); revised 2026-07-17; gap-closure pass 2026-07-22/24
- **Artifact**: `docs/reports/paper_a/paper_a_prototype_jmlr.tex`
- **Assessment target**: Paper A as a benchmark/methodology paper for XAI and ML evaluation
- **Status**: Submission-ready as of 2026-07-24. Score target reached (88/100); Zenodo DOI refreshed and verified; the two remaining result gaps (37 Anchors/DiCE cells, 1 SHAP overlay cell) were reviewed with the author and accepted as permanent, disclosed limitations rather than pursued further.
- **Overall score**: 88/100
- **Target score**: 85+ (reached)

## 1.1 2026-07-17 Revision Pass

This pass re-verified the April 2026 findings against the current repository
state and made editorial corrections to the manuscript. It did not attempt to
resolve the substantive evidence gaps (those still require rerunning or
importing artifacts, not text edits).

Verified unchanged since April:

- `outputs/analysis/paper_a_exp2_stats/analysis_summary.json` still reports
  299 present artifacts, 275 analyzable unique runs, 25 residual empty
  Anchors/DiCE cells, and 15/15 complete Friedman blocks; manuscript numbers
  remain synchronized to it.
- `experiments/exp2_scaled/results/svm_shap/seed_456/n_200/` still has no
  committed `results.json`; the paper still depends on the
  `outputs/batch_results.csv` recovery overlay for that cell.
- Resolved 2026-07-24: a new Zenodo version (DOI `10.5281/zenodo.21538180`,
  concept DOI `10.5281/zenodo.19297723`) archives commit `553f65d71` (the
  evidence cut in this manuscript), verified publicly resolvable via both the
  DOI redirect and the Zenodo public records API. The prior 2026-03-28
  snapshot DOI (`10.5281/zenodo.19297724`) is retained for provenance only.
- `configs/experiments/exp3_cross_dataset/` now exists with trained
  `breast_cancer`/`german_credit` model artifacts (added for the thesis, not
  Paper A), but has no benchmark run results yet, so it is not usable as an
  external-validity extension for Paper A in its current state.

Editorial corrections applied to
`docs/reports/paper_a/paper_a_prototype_jmlr.tex`:

- Standardized cohort terminology: introduced "primary benchmark (EXP2)" as
  an explicit shorthand for the primary robustness benchmark, and simplified
  "reproducibility repeatability cohort" to "reproducibility cohort"
  throughout, removing an internal naming inconsistency between the cohorts
  table and the running text.
- Clarified a methodological transparency gap: the Friedman and 45-cell
  Wilcoxon tables displayed raw p-values while the text claimed
  Holm-Bonferroni correction across the five primary metrics for each
  inferential family. Table captions and surrounding text now explicitly
  label the values as raw and report the Holm-corrected family-wise
  conclusion (all five metrics remain significant at $\alpha=0.05$ in both
  families; verified directly against
  `outputs/analysis/paper_a_exp2_stats/friedman_results.csv` and
  `wilcoxon_shap_lime_primary.csv`). Also added a one-line note that the
  identical raw p-value across four Wilcoxon metrics reflects the exact
  signed-rank floor for 45 same-direction matched pairs, not a copy-paste
  error.
- Fixed a LaTeX formatting defect: the Code and Artifact Availability
  paragraph produced a ~50pt overfull line (text extending past the page
  margin) because a git tag string and a DOI were set in non-breaking
  verbatim-style commands; wrapped the paragraph in `sloppypar` and made the
  DOI display breakable. Confirmed via rebuild that both
  `paper_a_prototype_jmlr.pdf` and `paper_a_prototype_neutral.pdf` now
  compile with no overfull boxes beyond sub-20pt cosmetic warnings typical of
  any LaTeX document.
- Rebuilt both PDFs with portable Tectonic; no undefined references or
  citations in either build.

Score impact: +1 (83 to 84) for improved statistical-reporting transparency
and terminology consistency. The score does not move further because the
April assessment's core blockers (residual empty artifacts, the uncommitted
SHAP cell, the stale DOI, and the un-bundled `outputs/` analysis tree) are
evidentiary/artifact gaps that text edits cannot close.

## 2. Objective

This note records the quality assessment of Paper A against high-standard
publication expectations for the thesis-relevant field: explainable AI (XAI),
machine learning benchmarks, statistical evaluation, and reproducible research.

The assessment treats Paper A as a benchmark and methodology contribution, not
as a new explainer algorithm paper. The main evaluation question is:

> Is the manuscript strong enough, as a scientific benchmark paper, for a top
> venue aligned with JMLR/TMLR/DMLR-style machine learning standards?

## 3. Assessment Setup

### 3.1 Relevant venue and policy standards

The scoring rubric was derived from the following standards and venue
expectations:

- JMLR author guidance: <https://www.jmlr.org/author-info.html>
- TMLR acceptance criteria: <https://www.jmlr.org/tmlr/acceptance-criteria.html>
- DMLR submissions guidance: <https://data.mlr.press/submissions.html>
- DMLR reviewer guidance: <https://data.mlr.press/reviewer-guidelines.html>
- Nature Machine Intelligence peer-review policy:
  <https://www.nature.com/natmachintell/editorial-policies/peer-review>
- Nature Portfolio reporting standards:
  <https://www.nature.com/natcomputsci/natcomputsci/editorial-policies/reporting-standards>
- Artificial Intelligence journal guide for authors:
  <https://www.sciencedirect.com/journal/artificial-intelligence/publish/guide-for-authors>
- ACM artifact review and badging:
  <https://www.acm.org/publications/policies/artifact-review-and-badging-current>

### 3.2 Local evidence checked

Primary local anchors:

- `docs/reports/paper_a/paper_a_prototype_jmlr.tex`
- `docs/reports/paper_a/paper_a_validity_and_reporting_caveats.md`
- `docs/reports/paper_a/paper_a_jmlr_track_positioning.md`
- `scripts/run_exp2_statistical_analysis.py`
- `configs/experiments/exp2_scaled/manifest.yaml`
- `experiments/exp2_scaled/results/`
- `outputs/batch_results.csv`
- `outputs/analysis/paper_a_exp2_stats/analysis_summary.json`

Local verification findings from this reassessment pass:

- The planned EXP2 grid in `configs/experiments/exp2_scaled/manifest.yaml`
  declares 300 runs.
- `experiments/exp2_scaled/results/` currently contains 299 tracked
  `results.json` files.
- Of those result files, 274 contain instance evaluations and 25 contain no
  instance evaluations.
- The one missing committed EXP2 result artifact is
  `experiments/exp2_scaled/results/svm_shap/seed_456/n_200/results.json`;
  `outputs/batch_results.csv` covers it through the SHAP recovery overlay.
- `python scripts/run_exp2_statistical_analysis.py` runs in the active
  environment after installing the declared `scikit-posthocs==0.11.4`
  dependency.
- `outputs/analysis/paper_a_exp2_stats/analysis_summary.json` reports 30
  overlay rows, 29 replacement rows, 275 analyzable unique runs, 15/15 complete
  Friedman blocks, 45 primary SHAP-LIME matched pairs, and 75 all-model
  SHAP-LIME matched pairs.

## 4. Scoring Results

| Criterion | Weight | Score | Rationale |
| :--- | ---: | ---: | :--- |
| Venue fit and contribution importance | 15 | 12 | Strong fit for benchmark-focused ML venues if FOM-7 is framed as a reusable benchmark operation method, not only a project-specific workflow. |
| Novelty and prior-work delta | 10 | 8 | The manuscript now includes a compact novelty-delta table against related XAI benchmark/toolkit work. The remaining risk is to avoid overclaiming algorithmic novelty. |
| Benchmark design and construct validity | 15 | 13 | The crossed design, metric orientation, leakage controls, and implementation caveats are strong. A bounded SHAP-only cross-dataset check (2026-07-24) now supports partial external-validity evidence beyond Adult, with one documented non-transfer case (German Credit/xgb Stability); the single-dataset scope for the full four-method ranking remains the main limit. |
| Statistical rigor and uncertainty | 20 | 19 | Friedman, Nemenyi, Wilcoxon, Holm correction, effect sizes, matched cells, and block aggregation are strong, and the regenerated analysis confirms 15/15 complete omnibus blocks. The 2026-07-17 pass fixed a raw-vs-Holm-corrected p-value transparency gap; the 2026-07-24 pass added Cohen's $d_z$ practical-importance reporting for the primary paired contrast. The remaining 25 empty Anchors/DiCE cells (root cause now diagnosed but not fixed) and the absence of a formal TOST equivalence procedure keep this below top-tier readiness. |
| Reproducibility and artifact quality | 20 | 18 | The model artifacts are repaired, the dependency is declared and installed in the active environment, the analysis outputs are regenerated and force-added to the repository, and the manuscript PDF has been rebuilt. The Zenodo release/DOI is refreshed and verified (2026-07-24). The 25 empty Anchors/DiCE cells and the `svm_shap_s456_n200` overlay dependency remain diagnosed but unresolved (environment/compute blockers, not neglect). |
| Claim discipline, limitations, and ethics | 10 | 9 | The caveats note is transparent and the manuscript now includes responsible-use and overgeneralization boundaries. |
| Clarity and scholarly presentation | 10 | 9 | The draft is readable, the novelty/artifact sections are stronger, the result-count narrative is synchronized to the regenerated analysis summary, and prior passes fixed an inconsistent EXP1/EXP2 cohort naming pattern and a page-margin overflow defect. |
| **Total** | **100** | **88** | **Above the 85+ target on manuscript quality and rigor. The Zenodo DOI is refreshed. Publication is still blocked on two environment-blocked result gaps (25 empty EXP2 cells, 12 EXP3 Anchors cells) that require a separate Python environment to close, and the deliberately-deferred `svm_shap_s456_n200` cell.** |

## 5. Analysis

Paper A has a strong scientific core. Its best features are:

- a clear multi-metric XAI benchmarking frame;
- explicit separation between calibration/reproducibility and confirmatory
  evidence cohorts;
- matched, non-parametric inference with block-level aggregation rather than
  instance-level pseudo-replication;
- transparent reporting of implementation caveats for Anchors and DiCE;
- FOM-7 as an auditable operational protocol linking execution, artifact
  qualification, statistical export, and claim-ready reporting.

The central weakness is not the idea. It is now the final submission package
boundary:

- The manuscript and caveats have been synchronized to the regenerated
  299-artifact / 275-analyzable-run merged snapshot.
- `outputs/analysis/paper_a_exp2_stats/` now exists and includes the generated
  inventory, block summaries, Friedman, Nemenyi, Wilcoxon, and uncertainty
  exports.
- The active environment now runs the deterministic analysis script after
  installing the declared `scikit-posthocs==0.11.4` dependency.
- The rendered manuscript PDF has been rebuilt from the updated LaTeX source
  with portable Tectonic 0.16.8.
- The residual evidence weakness is concentrated in 25 present-but-empty
  Anchors/DiCE artifacts, plus one committed-tree SHAP artifact still covered
  by the recovery overlay rather than by a per-run `results.json` file.
- The generated analysis outputs are under the ignored `outputs/` tree, so they
  need explicit inclusion in the next submission bundle if the project wants
  the paper package to be self-contained.

Under top-journal standards, these are material because benchmark papers are
judged as much by artifact trustworthiness and reusable evaluation governance
as by narrative results.

## 6. Anomalies and Deviations

- **Residual empty artifacts, root cause now diagnosed**: The merged snapshot
  still excludes 25 present-but-empty Anchors/DiCE result artifacts. A
  2026-07-22 live rerun of one cell (`logreg_anchors_s123_n50`) reproduced the
  exact failure: `alibi`/`dice-ml` are not importable in the project's active
  `.venv` (Python 3.13), so every per-instance explanation call raises a
  caught-but-unlogged-at-run-level `ImportError`, and the run "completes" with
  zero evaluations instead of crashing. This is a deterministic environment
  gap, not a random operational failure, and it is **not yet fixed**:
  `alibi==0.9.6` requires `numpy<2.0`, which has no Python 3.13 wheel and is
  incompatible with the `numpy==2.2.6` this environment's `scipy`/
  `scikit-learn` require. A source build of `numpy<2.0` failed on this
  machine's toolchain; forcing an unconstrained resolver install downgrades
  `alibi` to version 0.5.5 (2021-era Anchors internals) and breaks
  `protobuf`-dependent tooling elsewhere in the environment, so that path was
  rolled back rather than kept. Closing this gap requires a separate Python
  (`<3.13`, `numpy<2.0`) environment dedicated to these 25 cells.
- **Overlay dependency for one SHAP cell**: The committed result tree still
  lacks `svm_shap_s456_n200`, although the recovery overlay covers that cell
  for Paper A analysis. A resumable rerun exists (161/800 instances
  checkpointed as of 2026-04-14) but is not being pursued further: SVM kernel
  SHAP on this benchmark times out on most instances at the 300s guard limit,
  and completing the remaining ~640 instances was estimated at 2-3 additional
  days of continuous runtime, which was judged not worth pursuing versus
  disclosing the gap.
- **Submission-bundle drift risk**: resolved 2026-07-22 —
  `outputs/analysis/paper_a_exp2_stats/` is now force-added to the repository
  (`.gitignore` alone cannot re-include files under an already-ignored parent
  directory such as `outputs/`, so `git add -f` was required, matching how
  `outputs/batch_results.csv` was evidently added previously).
- **TeX toolchain reproducibility risk**: The PDF was rebuilt with portable
  Tectonic because `latexmk`/`pdflatex` are not installed on this workstation;
  the release workflow should record the exact compiler path or use a standard
  TeX environment.
- **External validity limit**: partially addressed 2026-07-22/23 — the 12
  SHAP-only `exp3_cross_dataset` configs (rf/xgb x breast_cancer/german_credit
  x 3 seeds) were run and are reported as a bounded external-validation check
  (see Section 7.4). The 12 Anchors-based `exp3` configs remain blocked by the
  same `alibi`/`numpy` environment gap described above.
- **Archive versioning gap**: resolved 2026-07-24 — a new Zenodo version (DOI
  `10.5281/zenodo.21538180`) archives commit `553f65d71`, the evidence cut
  reported in this manuscript, verified publicly resolvable. The prior March
  snapshot DOI (`10.5281/zenodo.19297724`) is retained for provenance only.

## 7. Conclusion and Next Steps

### 7.1 Verdict

Paper A currently scores **88/100** under a high-standard benchmark-paper
rubric after the April 2026 result synchronization, the 2026-07-17 editorial
revision pass, and the 2026-07-22/24 gap-closure pass (including the
2026-07-24 Zenodo DOI refresh). **As of 2026-07-24, Paper A is considered
submission-ready.** The two remaining result gaps — the 25 empty EXP2
Anchors/DiCE cells plus the 12 EXP3 Anchors cells (diagnosed:
`alibi`/`numpy<2.0` incompatible with this Python 3.13 environment), and the
`svm_shap_s456_n200` overlay dependency (an estimated 2-3 days of further
compute for one cell) — were explicitly reviewed with the author and a
decision was made **not to pursue further compute or environment migration**.
Both are disclosed transparently in the manuscript's own limitations
sections (Section~\ref{sec:results}, "Limitation" bullets) and in this
assessment, and neither affects the paper's reported statistical
conclusions (the Friedman tests already run on 15/15 complete blocks; the
SHAP-LIME paired contrast already has its full 45/75 matched cells). This is
now the final position for this evidence cut, not a pending action item.

The paper reached **85+** without changing its core research idea. Should a
reviewer or venue explicitly require full-grid completeness, the
`<3.13`/`numpy<2.0` environment work described above remains the path to close
the Anchors/DiCE gaps; it is not planned unless that feedback occurs.

### 7.2 Priority plan to reach 85+ (historical; target reached — see 7.1)

1. **Submission-bundle synchronization**
   - Keep the rebuilt `docs/reports/paper_a/paper_a_prototype_jmlr.pdf`
     synchronized with the updated LaTeX source.
   - Explicitly bundle or force-add `outputs/analysis/paper_a_exp2_stats/`,
     because the `outputs/` tree is ignored by default.
   - Treat `analysis_summary.json` as the single source for manuscript counts:
     present artifacts, analyzable runs, overlay rows, replacements, empty runs,
     missing cells, complete blocks, and matched pairs.

2. **Residual artifact repair**
   - Finish or import `svm_shap_s456_n200` into the committed per-run result
     tree so the paper no longer depends on a recovery overlay for that SHAP
     cell.
   - Diagnose the 25 empty Anchors/DiCE artifacts by method, model, seed, and
     sample size; rerun only cells where the claim protocol indicates the work
     is safe and non-duplicative.

3. **External validity upgrade**
   - Add a minimal second tabular dataset via `exp3_cross_dataset`, or clearly
     reposition the paper as a single-dataset proof-of-protocol with replication
     as the next study.
   - If time allows, add one cross-dataset stability check for SHAP vs LIME and
     report it as external-validation evidence, not as a full second benchmark.

4. **Statistical polish**
   - Add equivalence or practical-importance thresholds for key metrics.
   - Report uncertainty tables from the regenerated analysis output.
   - Keep the block-level inference discipline and avoid any instance-level
     significance claims.

### 7.3 Expected score after completion

If the remaining bundle portion of item 1 is completed, the score should rise
to roughly **84-85** because the current analysis would become reviewable as a
coherent artifact package.

If items 1 and 2 are completed, the score should plausibly reach **85-87**.

If items 1, 2, and either the minimal `exp3_cross_dataset` replication or a
well-bounded external-validity rewrite are completed, the score should plausibly
reach **87-89**.

If all four items are completed and the regenerated artifact package runs from
a clean environment, the paper becomes a credible benchmark-track submission
candidate rather than an internal thesis draft.

### 7.4 Improvement Passes

Completed on 2026-04-13 while the EXP2 worker was still active:

- added a novelty-delta table to `paper_a_prototype_jmlr.tex`;
- filled the novelty-delta placeholder in `paper_a_jmlr_track_positioning.md`;
- added a responsible-use and benchmark-boundaries subsection to the manuscript;
- created `paper_a_artifact_index.md` as a reviewer-facing artifact map;
- added `scipy` and `scikit-posthocs==0.11.4` to `requirements.txt` so the
  Paper A statistical analysis dependency is declared in the active dependency
  path, not only in `requirements-frozen.txt`.

Completed on 2026-04-14 after result synchronization:

- repaired the Adult model artifacts needed by the reproducibility stack;
- installed the declared `scikit-posthocs==0.11.4` dependency in the active
  analysis environment;
- regenerated `outputs/analysis/paper_a_exp2_stats/`;
- synchronized `paper_a_prototype_jmlr.tex`,
  `paper_a_prototype.md`, and `paper_a_validity_and_reporting_caveats.md` to
  the 299-artifact / 275-analyzable-run / 25-residual-gap snapshot;
- rebuilt `paper_a_prototype_jmlr.pdf` with portable Tectonic 0.16.8 after
  confirming `latexmk` and `pdflatex` were unavailable locally;
- updated the working score from 72/100 to 83/100.

Completed on 2026-07-22/24 (gap-closure pass):

- force-added `outputs/analysis/paper_a_exp2_stats/` to the repository
  (`git add -f`, since `.gitignore` negation cannot re-include files under an
  already-ignored parent directory such as `outputs/`);
- diagnosed the root cause of the 25 empty Anchors/DiCE artifacts via a live
  rerun: `alibi`/`dice-ml` are not importable in the active Python 3.13
  `.venv`; confirmed `alibi==0.9.6` requires `numpy<2.0`, which has no
  Python 3.13 wheel and is incompatible with this environment's
  `numpy==2.2.6`; attempted and rolled back an unconstrained install that
  would have downgraded `alibi` to 0.5.5 and broken `protobuf`-dependent
  tooling; left the 25 cells and the 12 EXP3 Anchors configs unresolved
  pending a dedicated Python `<3.13`/`numpy<2.0` environment;
- ran the 12 SHAP-only `exp3_cross_dataset` configs (breast_cancer/
  german_credit x rf/xgb x 3 seeds) and added a new manuscript subsection,
  "External Validity Check: Cross-Dataset SHAP Stability", reporting the
  results as a bounded, single-explainer check;
- added Cohen's $d_z$ practical-importance reporting to the primary
  SHAP-LIME paired comparison table, grounded in Cohen (1988) small/medium/
  large conventions;
- fixed an EXP1/EXP2 cohort-naming inconsistency and a page-margin overflow
  defect (carried over from the 2026-07-17 pass's verification);
- committed the Paper A gap-closure work (commit `553f65d71`);
- refreshed the Zenodo release: published version DOI `10.5281/zenodo.21538180`
  (concept DOI `10.5281/zenodo.19297723`) archiving commit `553f65d71`,
  verified publicly resolvable via the DOI redirect and the Zenodo public
  records API; updated the manuscript's Code and Artifact Availability
  section and acknowledgments accordingly;
- updated the working score from 84/100 to 88/100.

Completed on 2026-07-24 (final decision on remaining gaps):

- reviewed the 25 empty EXP2 Anchors/DiCE cells, the 12 EXP3 Anchors cells,
  and the `svm_shap_s456_n200` overlay dependency with the author; decided
  not to pursue the required Python `<3.13`/`numpy<2.0` environment migration
  or the further ~2-3 days of SHAP compute, and to accept all three as
  permanent, disclosed limitations of this evidence cut instead;
- updated the manuscript's "Limitation" and "Next steps" bullets in
  Section~\ref{sec:conclusion} to reflect this as a final position rather
  than pending work; rebuilt both PDFs.

Nothing further is required before submission unless review feedback asks
for full-grid completeness.
