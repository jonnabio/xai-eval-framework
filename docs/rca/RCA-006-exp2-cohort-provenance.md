# RCA-006: EXP2 cohort provenance gaps (split seed coupling, unrecorded RF artifact, ResourceGuard timing floor, and partial SVM SHAP cells)

**Status**: Closed 2026-11-24. Disclosed in every live manuscript that uses the cohort; replacement
cohort B2 in Paper B; guard below.
**Severity**: High (internal validity of the EXP2 cohort behind Paper A, Paper B's original
submission, Papers D and E and the thesis; no stored result altered)
**Opened**: 2026-11-06 (found during Paper B revision 1, WP0); RCA written 2026-11-24
**Role**: Incident Responder
**Related**: `docs/reports/paper_b/ci_journal/revision_1/WP0_FINDINGS.md` (F1, F7a–F7e, F8, F9;
evidence in `provenance/`); `docs/review/thesis-papers-reconciliation-audit_2026-11-23.md`;
RCA-001 (numbers drifting from their source). WP0 named this incident "RCA-004"; that number went to
the Paper G publisher (RCA-004), so it is filed as RCA-006.

## Symptoms

Found while building the timing sub-sample of Paper B revision 1 (WP2-T, 2026-11-06): regenerating
each EXP2 cell's instance set with today's code and models did not reproduce the stored sets for
the random forest, and timings on one host were far below the EXP2 medians.

## Evidence (WP0)

- **F1.** `experiments/exp1_adult/models/preprocessor.joblib` outputs **108** columns
  (`get_feature_names_out()`; 6 numeric and 8 categorical inputs). The thesis and Paper B said 103.
- **F7a / F7e.** The random forest of the January–February runs (all 15 SHAP and 15 LIME RF runs and
  the early Anchors/DiCE RF runs) was never committed. The committed `rf.joblib` (the only version git
  ever held) shares a median 7.5% of their instances; retraining with the repository defaults does not
  reproduce them either. 9 April Anchors/DiCE RF runs used the committed model, so RF Anchors/DiCE
  mix two forests. SHAP and LIME saw identical instances in every RF cell, hence one model.
- **F7b.** `ResourceGuard.run_guarded` (added 2026-03-23, `8dbe946f0`) sleeps 1 s per memory check and
  `join()`s inside the timed window: 25 of the 31 later runs have a minimum cost ≥ 990 ms (one
  SHAP/LIME run materially affected, `mlp_shap` seed 42, N=200).
- **F7c.** In 10 of the 15 SVM cells SHAP explained 27–199 instances, a subset of LIME's 200–800, so
  the cell means compare different instance sets.
- **F8.** `load_adult(random_state=self.config.random_seed)` re-splits with each run's seed, while the
  models were fitted once on the seed-42 split: for seeds ≠ 42 about 80% of the "test" rows are
  seed-42 training rows (60 of 75 cells).
- **F9.** `src/xai/dice_wrapper.py` calls `generate_counterfactuals(..., total_CFs=1)` whatever the
  config says (5); `src/xai/anchors_wrapper.py` hard-codes `threshold=0.95`.

## Root cause

1. **Why did seeds ≠ 42 evaluate training points?** The run seed was passed to
   `load_adult(random_state=...)`, so one seed controlled both the data split and the replicate
   (instance draw, explainer randomness), while the models stayed fitted on one split.
2. **Why could an RF be used that no one can recover?** Model artifacts were not hash-pinned and
   checked against a committed manifest before workers started; `rf.joblib` was a pointer whose
   target lived on a worker.
3. **Why does cost carry a 1 s floor?** `ResourceGuard` wrapped the timed call and waited for its
   polling thread's `join()` inside the timed window; no test compared guarded and direct timings.
4. **Why did prose disagree with the code?** Wrapper parameters (`total_CFs`, `threshold`) were
   hard-coded instead of read from the experiment YAML, and the encoded width was typed in prose
   instead of read from `preprocessor.joblib`.
5. **Why did no check catch any of it?** Provenance was asserted, not re-derived: nothing regenerated
   instance sets from stored models, and `verify_claims.py` deliberately ignores bare integers such
   as 103.

**Root cause:** the EXP2 runner did not separate the data split from the replicate, did not bind a
run to a verified model artifact, and timed through infrastructure code; the manuscripts described
the intended configuration rather than one read from the artifacts.

## Corrective actions

- **Paper A** (published, RIMI): the archival record is immutable; this RCA and the thesis are the
  record of its limits.
- **Paper B revision 1** (C&I 2067810): EXP2 replaced by cohort B2 (`experiments/exp_b_rev1/`,
  `scripts/paper_b_run.py`): one split per dataset (`split_seed = 42` in `cohort.toml`) shared by
  preprocessing, training and every seed; frozen models with SHA-256 in `models/MANIFEST.csv`, each
  record carrying the cohort and model hashes; timing by `time.perf_counter()` around the explain
  call, without `ResourceGuard`.
- **Paper D**: held-out sensitivity analysis excluding the 70,788 in-training instances; the stability
  deficit on misclassified instances holds (thesis Ch. 6 `sec-seg-error`).
- **Paper E**: pairs on the intersection of matched instance ids and discloses the incomplete SVM SHAP
  runs (thesis Ch. 6 `sec-seg-concordancia`).
- **Papers F and G**: own runners (`scripts/paper_f_lib.py`, `scripts/paper_g_lib.py`) re-fit the
  model on each replicate's own split and draw instances from its test part, so split and model never
  diverge; Paper G's publisher records a SHA-256 per published file.
- **Thesis** (PR #149, `bbb084506`; PR #150, `73d44f7c1`): 103 → 108 encoded dimensions (seven
  occurrences) and "ocho variables categóricas"; F8 in Ch. 3 `sec-muestreo`, F7c in Ch. 3
  `sec-cobertura`, F7a and F7b in Ch. 3 `sec-trazabilidad`, both in `tbl-validity-threats`; F9 was
  already stated in Ch. 3 and Appendix C.
- **Not done**: `src/experiment/runner.py`, `src/xai/dice_wrapper.py`, `src/xai/anchors_wrapper.py` and
  `ResourceGuard` are unchanged, so the EXP2 code still reproduces what the cohort did. A new
  experiment does not reuse that runner without fixing them first (guard below).

## Tests

No new automated test: the EXP2 code is frozen as a record. The checks are the guard's invariants
and the existing manuscript checks (`verify_claims.py`, `check_equations.py`), plus the B2 runner's
manifest check.

## Standard update

A new experiment fits each model on a split that does not depend on the replicate seed, or re-fits it
on that seed's split; binds every run to a hashed model artifact; times the explainer call directly;
reads every explainer parameter it reports from the configuration; and a manuscript states encoded
dimensions from the fitted preprocessor.
