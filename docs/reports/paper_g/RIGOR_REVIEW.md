# Paper G — scientific rigor review of the manuscript

**Date:** 2026-11-16. **Reviewed:** `paper_g.md` (rendered from `paper_g_draft.md` v0.2) and the
evidence it rests on. **Severity:** Critical = must be fixed before the manuscript can be
reviewed by the author as scientifically sound; Major = must be resolved or explicitly accepted
by the author before submission; Minor = improvement. The original confirmatory outputs, S3, S1,
the diagnostics, the frozen code and plan sections 1 to 11 were not modified (checked against
`origin/main` before every commit).

## Summary

No Critical finding. The manuscript reports the confirmatory analysis exactly as frozen
(estimate, interval, permutation *p*, Holm-adjusted *p*, decision wording), separates it from the
supplementary experiments and the exploratory diagnostics (Table 1 of the manuscript; every
results subsection is labelled with its class), applies no decision rule to S1, and states the
limits of S1 (surrogate, off-manifold categorical sampling, reference mismatch with SHAP). Every
printed number is rendered from the result files and re-derived by the claim verifier. Six Major
findings remain; four concern disclosure or author decisions rather than defects.

## Construct validity

| # | Severity | Finding | Status |
|---|---|---|---|
| C1 | Major (disclosed) | The confirmatory result measures agreement for LIME stored as slopes, which M1 to M6 read as contributions; the headline "broadly agree" therefore partly reflects a representation mismatch. | The manuscript states this where the result is reported (3.1), quantifies it (3.3 to 3.5) and frames the contribution around it (3.8). Nothing to change; the author should be aware that a reviewer may ask why the confirmatory analysis was not re-specified. Answer: re-specifying after seeing results would have been a forking path; the original is reported as frozen and S1 as specified before its run (plan 12.3, frozen at `664b71f22`). |
| C2 | Major (disclosed) | S1 on categorical features rests on a surrogate fitted to off-manifold one-hot samples; SHAP's reference (background expectation) differs from S1-B's (masking baseline). | Stated in 2.6 and the Limitations. The numeric datasets, where S1-B is exact for the surrogate, show the same direction of change (0.758 to 0.484; Section 3.4), which limits the dependence of the conclusion on the categorical approximation. |
| C3 | Minor | M4 and occlusion share their construction; occlusion is first under M4 in every block. | Reported (2.4, 3.5); the six-metric analysis is reported. |
| C4 | Minor | The synthetic check is small (eight features, two function families). | Stated in the Limitations. |

## Statistical validity

| # | Severity | Finding | Status |
|---|---|---|---|
| S1 | Major (disclosed) | Inference rests on eight datasets (*t*-intervals with 7 df); the permutation and sign-flip *p* are at their smallest attainable values, so they show direction, not strength. | The text says both *p* are the smallest attainable; the pre-run simulation of coverage is cited in 2.5. |
| S2 | Major (disclosed) | With three ranked explainers, a single consistently last explainer bounds block agreement below at 0.5, so the 0.5 decision threshold cannot separate full agreement from agreement on the last position. | Stated in 2.5 (decision rule), shown in 3.5 and in the Limitations; the classification is reported with the position distribution as the plan requires. |
| S3 | Minor | Multiplicity: Holm over H1 and H2 and over the 15 pairs is applied; S1 and the diagnostics carry no tests, so no further correction is needed. | Correct as written. |
| S4 | Minor | Some details were fixed after the run (H2 test and interval, benchmark definition, synthetic statistic, ties, M4 exclusion), and the variance decomposition was omitted. | Disclosed as a class of evidence (Table 1) and in the Limitations. |

## Internal validity

| # | Severity | Finding | Status |
|---|---|---|---|
| I1 | Major (disclosed) | The supplementary experiments and diagnostics were specified after the first results were reviewed (garden of forking paths). | Mitigations stated: specifications frozen before execution, S1-B primary and S1-M sensitivity named in advance, no tests, original outputs untouched; the two S1 variants differ by at most 0.024. |
| I2 | Minor | The pairing (same instances, explanations and seeds for every explainer and metric) removes instance and model variation from the comparisons. | Described in 2.1. |

## External validity

| # | Severity | Finding | Status |
|---|---|---|---|
| E1 | Minor | Binary tabular classification only; four model families; one configuration per explainer and model; LIME's fitting choices not varied (S2 not run). | Limitations; future work in the Conclusions. |

## Reproducibility

| # | Severity | Finding | Status |
|---|---|---|---|
| R1 | Minor | Every number is rendered by `scripts/build_paper_g.py` from committed result files and registered in `pub/claim_registry.toml` (185 claims; bare integers are covered by `register_paper_g.py --check`); the figures are drawn by `scripts/paper_g_figures.py` from the same files; build, figures and references are byte-reproducible. | Pass. |
| R2 | Minor | The archive DOI of the Paper G code and results is not yet created (Data availability withholds it for review). | Author: create the Zenodo version at acceptance. |

## Novelty

| # | Severity | Finding | Status |
|---|---|---|---|
| N1 | Minor | Closest recent work: Shanklin et al. (2026) analyse disagreement among faithfulness criteria conceptually (no tabular measurement); Ababneh & Aljarrah (2026) report that tabular explanation rankings depend on classifier, masking operator and budget (one tabular dataset, two models); Miró-Nicolau et al. (2025), Duan et al. (2024) and Edin et al. (2025) question metric reliability in other settings. Paper G's paired eight-dataset measurement, the within-metric stability benchmark, and the demonstration that attribution semantics can produce apparent agreement are not covered by them. | All cited and positioned in 1.1 and 3.8. |
| N2 | Minor | Relation to the programme's earlier papers: Paper B (configuration dependence), Paper E (SHAP–LIME instance-level disagreement; it documented LIME's slope output) and Paper F (dataset dependence of rankings). Paper G restates no result of them (qualitative statements only; the claim verifier's exclusivity check is clear), and asks a different question (agreement of the measuring instruments). | Cited in the third person as anonymised manuscripts. |

## Ethics and reporting

| # | Severity | Finding | Status |
|---|---|---|---|
| X1 | Minor | Public benchmark datasets only, including COMPAS and Adult, which carry known fairness concerns; they are used as evaluation benchmarks, with no claim about individuals and no human participants. | No ethics approval required; no change. |
| X2 | Major (author) | The text was drafted by the assistant; the journal returns manuscripts with more than 30% AI-generated content (Compilatio). The AI-use declaration is drafted honestly. | Author decision (2026-11-13: the author owns this limit). See `JOURNAL_COMPLIANCE.md`. |

**SCIENTIFIC RIGOR REVIEW: PASS** (no Critical finding; Major findings are disclosed in the
manuscript or are author decisions).
