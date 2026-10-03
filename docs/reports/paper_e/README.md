# Paper E — do explainers agree on which features matter?

**Status (2026-10-03): analysis initiated at the author's direction.** This advances the
earlier plan to wait until Paper D is submitted. Paper E has an analysis plan, but it must be
committed before any Paper E statistic is calculated or the new EXP3 LIME cohort is run.
Nothing in this folder is a result.

## The question

When several post-hoc explainers explain the **same prediction**, do they point to the same
features, in the same order and with the same direction of effect? The literature calls this
the "disagreement problem". Practitioners often treat SHAP, LIME and other methods as
interchangeable, but if they disagree on the top features, the choice of explainer changes
the explanation a user sees.

## Sub-questions (formalized in `ANALYSIS_PLAN.md` before results are computed)

1. How much do the explainers agree on the top-k features for the same instance?
   Measures: top-k overlap, rank correlation, and sign agreement.
2. Does agreement depend on the model family, the dataset, or the sampling intensity?
3. Is agreement lower on misclassified instances? This links to Paper D's result; cite it,
   do not repeat it.
4. Does agreement predict explanation quality? For example, are instances where explainers
   disagree also those with low fidelity or stability?

## Why it can be a separate paper (and how to keep it separate)

- **Different question.** Paper D compares quality between correct and incorrect
  predictions. Paper E compares explainers with one another.
- **New data, not only re-analysis.** It must include something that exists nowhere else:
  - EXP2 (Adult): all four methods explained the **same instances**, and each run stores the
    top-10 attributions (`instance_evaluations[].explanation.raw_top`).
  - EXP3 (German Credit, Breast Cancer): SHAP and Anchors have per-instance attributions.
    **LIME stored only averages** (`outputs/analysis/exp3_lime_results.csv`), so a new LIME
    run with per-instance attributions is needed: `scripts/run_exp3_lime.py`, extended to save
    `raw_top`. That run is a new experiment, and it is what makes Paper E broader than a slice
    of the existing cohort.
- **Different venue and time.** Submit after Paper D, to a different journal.
- **Disclosed provenance.** State, as Papers B+C and D do, that the EXP2/EXP3 runs are the
  benchmark cohort of Papers A and B+C, and report none of their results.
- **Enforced.** When the manuscript exists, add it to `[coverage]` and `[exclusivity]` in
  `pub/claim_registry.toml`.

## Data available now (checked 2026-10-03)

| Source | Explainers with per-instance attributions | Notes |
|---|---|---|
| EXP2, UCI Adult | SHAP, LIME, Anchors, DiCE | 299 runs; same instances across methods within a (model, seed, n); top-10 features and weights per explanation |
| EXP3, German Credit | SHAP, Anchors | 12 runs; LIME to be re-run with attributions saved |
| EXP3, Breast Cancer | SHAP, Anchors | 12 runs; LIME to be re-run with attributions saved |

**Caveat:** Anchors returns rules and DiCE returns counterfactuals, not additive
attributions. How their "top features" are defined in `raw_top` must be checked before they
are compared with SHAP and LIME. The comparison may be limited to SHAP versus LIME, plus
feature *sets* for Anchors and DiCE.

## Analysis workflow

1. Commit `ANALYSIS_PLAN.md` before computing any Paper E result.
2. Review the initial source audit in `DATA_AUDIT.md` and reproduce it with
   `python scripts/paper_e_data_audit.py`; it is structural/identity QC, not a Paper E result.
3. Extend `scripts/run_exp3_lime.py` to save per-instance attributions for the exact IDs in the
   existing EXP3 SHAP runs. This is a new cohort, kept in its own output directory.
4. Run the prespecified analyses and retain reproducible tables, diagnostics and figure sources.
5. Literature check: verify each reference against its DOI; the author approves each.
6. Choose a different venue (no publication fee; English), then draft only after the analysis
   artifacts pass verification.
