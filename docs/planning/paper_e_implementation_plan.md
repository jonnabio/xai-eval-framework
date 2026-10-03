# Paper E — implementation plan

**Status:** In progress
**Created:** 2026-10-03
**Research plan:** `docs/reports/paper_e/ANALYSIS_PLAN.md`
**Branch:** `paper/e-feature-agreement`, based on `main`; do not merge Paper D's lane.

## Objective

Produce an auditable, instance-aligned analysis of feature agreement among
explainers, with a new EXP3 LIME cohort, without overwriting prior cohorts or
re-reporting the source papers' method-level results.

## Tasks

1. **Lock the scientific plan**
   - Keep `ANALYSIS_PLAN.md` free of results and commit it before analysis or
     running a new experiment.
   - Update README status and workflow to reflect the approved timing change.

2. **Audit existing evidence**
   - Inventory EXP2/EXP3 JSON files and report source paths, run status,
     unique-ID counts, duplicate IDs, per-method matching and `raw_top`
     validity.
   - Confirm class-1 sign semantics and the feature-set definitions for
     Anchors and DiCE from their wrappers and artifacts.
   - Stop paired analyses wherever identity or attribution semantics cannot be
     established.

3. **Create the new EXP3 LIME cohort**
   - Regenerate absent EXP3 models in an isolated artifact root using the
     checked-in trainer; verify metadata, training summaries, feature order and
     exact source-cohort labels/predictions before explanation.
   - Persist per-instance attribution maps, original instance IDs, run
     metadata, configuration and explicit failure status in a new directory.
   - Preserve `outputs/analysis/exp3_lime_results.csv` and every existing
     EXP3 run; never silently replace a cohort.
   - Add focused tests for ID matching, feature-value serialization, missing
     IDs and new-output-path isolation.

4. **Implement and run the planned analysis**
   - Add a deterministic analysis script that reads the raw run artifacts and
     the new LIME cohort, checks the plan's QC conditions, and emits
     diagnostics, analysis tables and figures.
   - Keep generated outputs in `outputs/analysis/paper_e/` on a `results/*`
     branch.
   - Report counts and exclusions; preserve empty-versus-missing semantics.
   - Use no unplanned inferential tests or post-hoc feature regrouping.

5. **Verify and hand off**
   - Unit-test metric functions on fixed fixtures, including identical,
     disjoint, tied-rank, signed, empty and missing explanations.
   - Run the analysis twice and confirm deterministic tabular outputs, apart
     from explicitly documented timestamps.
   - Verify existing cohorts are unchanged, then update `ACTIVE_CONTEXT.md`
     with the actual files, commands, results and remaining author actions.

## Branch and artifact boundaries

- Paper E-specific plans, audits and reports belong on
  `paper/e-feature-agreement`.
- `outputs/analysis/**` is results-lane material (`results/paper-e-*`) and must
  be merged through `main`, not copied from another manuscript lane.
- `scripts/pubs/**`, the claim registry, regression guards and
  `ACTIVE_CONTEXT.md` are shared-substrate files. Make any such changes as
  separate substrate commits; do not mix them with Paper E documents.
- Do not add the future manuscript to claim-registry coverage/exclusivity
  until it exists and its claims can be registered.

## Acceptance criteria

- The analysis plan is committed before new experiment output or statistics.
- EXP3 LIME explanations are paired by exact original instance IDs with the
  stored SHAP cohort; mismatches fail explicitly.
- Each reported agreement value can be regenerated from tracked inputs and a
  committed script.
- No previous output file is overwritten, and Paper A/B+C quality means are
  not presented as Paper E findings.
