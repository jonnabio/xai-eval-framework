# Paper E — do explainers agree on which features matter?

**Status (2026-10-03): analysis artifacts generated.** At the author's direction, this
advances the earlier plan to wait until Paper D is submitted. The protocol, source audit,
new EXP3 LIME cohort and descriptive analysis are complete. Interpretation, literature
verification and venue selection remain author work; no confirmatory tests or p-values are
reported.

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
| EXP2, UCI Adult | SHAP, LIME, Anchors, DiCE | 299 source run files; valid instance-ID coverage varies by method and block, so each comparison uses its recorded matched intersection |
| EXP3, German Credit | SHAP, Anchors, Paper E LIME | Six new LIME runs explain the exact stored SHAP instance IDs |
| EXP3, Breast Cancer | SHAP, Anchors, Paper E LIME | Six new LIME runs explain the exact stored SHAP instance IDs |

## Generated artifacts

The new per-instance LIME cohort, run manifest, analysis tables, diagnostics and figures
are committed on `results/paper-e-agreement`:

- [`EXP3 LIME cohort`](../../../outputs/analysis/paper_e/exp3_lime/)
- [`Analysis report and artifacts`](../../../outputs/analysis/paper_e/analysis/)
- [`RESULTS.md`](../../../outputs/analysis/paper_e/analysis/RESULTS.md)

The primary SHAP-LIME analysis contains 31,411 paired instance records across 87 audited
blocks. Only matched, classification-consistent IDs are included. The machine-readable
diagnostics record 76 blocks with exact valid-ID sets, 4,936 unpaired valid method-IDs and
zero classification mismatches in primary pairs. Secondary Anchors/DiCE comparisons are
feature-set overlaps only; mismatched classifications and potentially truncated Anchor
rules are excluded and documented in the diagnostics.

The aggregate EXP3 LIME file at `outputs/analysis/exp3_lime_results.csv` remains unchanged.

**Caveat:** Anchors returns rules and DiCE returns counterfactuals, not additive
attributions. How their "top features" are defined in `raw_top` must be checked before they
are compared with SHAP and LIME. The comparison may be limited to SHAP versus LIME, plus
feature *sets* for Anchors and DiCE.

## Analysis workflow

1. `ANALYSIS_PLAN.md` was committed before computing any Paper E result.
2. The initial source audit in `DATA_AUDIT.md` was reproduced with
   `python scripts/paper_e_data_audit.py`; it is structural/identity QC, not a Paper E result.
3. The EXP3 LIME cohort is stored separately and uses the exact IDs in the existing SHAP
   runs. EXP3 model binaries are not tracked; regenerate them to an isolated artifact root:
   `python scripts/train_exp3_models.py --model-root <model-root> --data-cache-dir <cache-dir>`.
   The LIME runner validates the regenerated metadata, training metrics, feature order and
   stored target predictions before running:
   `python scripts/run_exp3_lime.py --paper-e --model-root <model-root> --data-cache-dir <cache-dir> --paper-e-output-dir <lime-output-dir>`.
4. The prespecified analyses are reproducible with
   `python scripts/analyze_paper_e.py --lime-root <lime-output-dir> --output-dir <analysis-output-dir>`
   and produced committed tables, diagnostics and figures on the results branch.
5. Remaining: verify each literature reference against its DOI with author approval, choose a
   different venue (no publication fee; English), and draft only after scientific review.
