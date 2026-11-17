# Paper G — scientific rigor review of the manuscript

> **Revised 2026-11-16 (Task 21)** after an independent review of v0.2. Section T21 below lists
> its findings and their resolution; the original review follows, updated where it changed.

**Date:** 2026-11-16. **Reviewed:** `paper_g.md` (rendered from `paper_g_draft.md` v0.2) and the
evidence it rests on. **Severity:** Critical = must be fixed before the manuscript can be
reviewed by the author as scientifically sound; Major = must be resolved or explicitly accepted
by the author before submission; Minor = improvement. The original analysis outputs, S3, S1,
the diagnostics, the frozen code and plan sections 1 to 11 were not modified (checked against
`origin/main` before every commit).

## T21. Findings of the independent review and their resolution

| # | Severity | Finding | Resolution |
|---|---|---|---|
| T1 | Critical | Equation (1) gave M1 and M2 as arithmetic means over *d* points; the frozen `paper_g_lib._auc` / `removal_metrics` integrate by the trapezoidal rule over *G* + 1 points (step 1/*G*), with endpoints *f(x)* and *f(b)*. | Equation (1) replaced by the exact trapezoidal form with the curves, indexing and endpoints defined. Verified against the frozen functions on 40 constructed cases (`verification/verify_equations.py`); the old form differs (e.g. by 1.4 × 10⁻² in case 1). No result recomputed: the frozen values always came from the frozen code. |
| T2 | Major | Evidence classes: v0.2 placed H2's test and interval, and the decision table's raw *p*, before the run. | Table 1, Section 2.5 and Section 3.1 now separate what the plan fixed before the run (§§4, 10), what was fixed after the run but before unblinding (§11: H2 inference, stability benchmark, ties and undefined values, M4 handling, synthetic statistic, raw *p*, six-metric sensitivity, retrospective gate, omitted variance shares), the original analysis run once, and the post-unblinding supplementary experiments and diagnostics (§12). "Confirmatory" is no longer used; the H1 classification is unchanged and remains the only decision. |
| T3 | Major | Reference points: v0.2 described SHAP, occlusion and S1 as if contributions shared one reference. | Section 2.3 now gives each explainer's output and reference (SHAP: expectation over a 50-row background sample; occlusion and S1-B: the masking baseline; S1-M: LIME's training mean, off the one-hot manifold for categorical features; LIME slopes: no reference). Sections 2.4, 2.6, 3.8 and the Limitations follow it; the categorical off-manifold limitation is kept. |
| T4 | Major | Unsupported causal statements: §3.6 ("arose because both metrics scale with *f(x)*"), §3.8 ("produced agreement by construction", "generalises beyond LIME", "dominant source of variation"), the Introduction and the Conclusions ("depends on"). | Rewritten as (1) properties of the computation (the 0.5 floor; the sign with which *f(x)* enters M1, M2, M3 and M6), (2) observed associations, and (3) possible mechanisms marked as not isolated. "Dominant" removed: the S1-B random-control sensitivity changed agreement by a similar amount, and no comparison between protocol choices was tested. No new statistical comparison added. |
| T5 | Major | Equation (4) used a fixed denominator of 21; the frozen `mean_pairwise_spearman` averages over the defined pairs only. | Equation (4) now averages over the set *D*~*b*~ of defined pairs; the text gives the counts (18 undefined pairs in 3 of 160 blocks) and the dataset-level averaging. Verified on 200 constructed rank matrices with undefined pairs. Equations (2), (3) and (5), and the M4 and M7 definitions, were checked against `removal_metrics`, `infidelity_metric`, `correlation_metric`, `roar_score` and `paper_g_s1_lime.contributions`; Equation (3) now states the uncentred *R*², the empty-subset rule and the degenerate cases. |
| T6 | Minor | M4 degenerate scores were called "undefined" and "excluded". | The text states that the frozen code stores 0 and flags them, the original analysis keeps them, and an exploratory analysis leaves them out. |
| T7 | Minor | The second masking baseline was described as "a random training row". | Now: one training row drawn at random per instance, the same for every explainer. M7 described as setting the top features to the baseline and retraining, as the code does. |

## Summary

No open Critical finding (T1 resolved). The manuscript reports the original analysis exactly as frozen
(estimate, interval, permutation *p*, Holm-adjusted *p*, decision wording), separates it from the
supplementary experiments and the exploratory diagnostics (Table 1 of the manuscript; every
results subsection is labelled with its class), applies no decision rule to S1, and states the
limits of S1 (surrogate, off-manifold categorical sampling, reference mismatch with SHAP). Every
printed number is rendered from the result files and re-derived by the claim verifier. After
Task 21 the equations match the frozen code and the evidence classes match the plan's chronology.
Six Major findings remain (C1, C2, S1, S2, I1, X2); four are disclosed limitations and two are
author decisions.

## Construct validity

| # | Severity | Finding | Status |
|---|---|---|---|
| C1 | Major (disclosed) | The original H1 result measures agreement for LIME stored as slopes, which M1 to M6 read as contributions; the headline "broadly agree" therefore partly reflects a representation mismatch. | The manuscript states this where the result is reported (3.1), quantifies it (3.3 to 3.5) and frames the contribution around it (3.8). Nothing to change; the author should be aware that a reviewer may ask why the original analysis was not re-specified. Answer: re-specifying after seeing results would have been a forking path; the original is reported as frozen and S1 as specified before its run (plan 12.3, frozen at `664b71f22`). |
| C2 | Major (disclosed) | S1 on categorical features rests on a surrogate fitted to off-manifold one-hot samples; SHAP's reference (background expectation) differs from S1-B's (masking baseline). | Stated in 2.6 and the Limitations. The numeric datasets, where S1-B is exact for the surrogate, show the same direction of change (0.758 to 0.484; Section 3.4), which limits the dependence of the conclusion on the categorical approximation. |
| C3 | Minor | M4 and occlusion share their construction; occlusion is first under M4 in every block. | Reported (2.4, 3.5); the six-metric analysis is reported. |
| C4 | Minor | The synthetic check is small (eight features, two function families). | Stated in the Limitations. |

## Statistical validity

| # | Severity | Finding | Status |
|---|---|---|---|
| S1 | Major (disclosed) | Inference rests on eight datasets (*t*-intervals with 7 df); the permutation and sign-flip *p* are at their smallest attainable values, so they show direction, not strength. | The text says both *p* are the smallest attainable; the pre-run simulation of coverage is cited in 2.5. |
| S2 | Major (disclosed) | With three ranked explainers, a single consistently last explainer bounds block agreement below at 0.5, so the 0.5 decision threshold cannot separate full agreement from agreement on the last position. | Stated in 2.5 (decision rule), shown in 3.5 and in the Limitations; the classification is reported with the position distribution as the plan requires. |
| S3 | Minor | Multiplicity: Holm over H1 and H2 and over the 15 pairs is applied; S1 and the diagnostics carry no tests, so no further correction is needed. | Correct as written. |
| S4 | Minor | Some details were fixed after the run but before unblinding (H2 inference, benchmark definition, synthetic statistic, ties, M4 handling, raw *p*), and the variance decomposition was omitted. | Disclosed as a class of evidence (Table 1, Section 2.5) and in the Limitations (T2). |

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
| R1 | Minor | Every number is rendered by `scripts/build_paper_g.py` from committed result files and registered in `pub/claim_registry.toml` (all printed decimals; bare integers are covered by `register_paper_g.py --check`); the figures are drawn by `scripts/paper_g_figures.py` from the same files; build, figures and references are byte-reproducible. | Pass. |
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

**SCIENTIFIC RIGOR REVIEW: PASS** (no open Critical finding; Major findings are disclosed in the
manuscript or are author decisions).
