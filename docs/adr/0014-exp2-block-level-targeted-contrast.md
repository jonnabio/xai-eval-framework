# ADR-0014: Add an Aggregation-Aligned EXP2 Targeted Contrast

> **Status:** Accepted<br>
> **Date:** 2026-09-27

---

## Context

EXP2 uses two different inferential units for different questions. The global
Friedman test and its Nemenyi localization use 15 `(model, n)` blocks after
averaging qualified seeds within each method. The existing H3 Wilcoxon analysis
uses 75 matched `(model, seed, n)` SHAP-LIME cells.

The fidelity Nemenyi result does not localize the global effect to SHAP versus
LIME: their mean-rank difference is 1.000, below the critical difference of
1.211. The tutor requested a paired test that directly evaluates SHAP versus
LIME at the same aggregation level as the omnibus analysis. Calling the
existing 75-cell H3 test an answer to that request would mix inferential units.
Calling a newly added test pre-specified would also misstate its provenance.

The new analysis must preserve the registered Friedman, Nemenyi, and 75-cell
results, comply with the registry-first claim workflow, and avoid treating five
seeds as independent Friedman blocks.

---

## Decision

We will add a deterministic, two-sided paired Wilcoxon signed-rank contrast
between SHAP and LIME over the 15 existing `(model, n)` blocks.

The implementation will:

1. derive paired SHAP and LIME values from the committed EXP2 block summary;
2. test all five declared primary metrics rather than selecting fidelity alone;
3. apply Holm correction across those five Wilcoxon tests;
4. report an exact two-sided sign test for the fidelity direction as a
   distribution-light corroborating result; and
5. export the paired blocks, Wilcoxon results, and sign-test results as separate
   machine-readable artifacts.

The manuscript will label this analysis a **review-motivated,
aggregation-aligned targeted follow-up**. It will not describe it as
pre-specified unless an earlier frozen protocol artifact establishes that
provenance.

The inferential hierarchy remains unchanged:

- Friedman is the primary global test for H1 and H2.
- Nemenyi remains the all-pairs post-hoc localization after Friedman.
- The new 15-block contrast addresses the focused SHAP-LIME question at the
  omnibus aggregation level.
- The existing 75-cell SHAP-LIME analysis remains the H3 paired analysis and is
  not relabelled as a 15-block result.

Seeds are repeated runs used to estimate each method's value within a
`(model, n)` block; they are averaged within the block and are not counted as
75 independent blocks in Friedman, Nemenyi, or the new contrast.

Per [ADR-0013](0013-publication-branching-model.md), analysis code and generated
outputs will be committed through the results lane, shared claim plumbing
through the publication substrate lane, and thesis prose through the thesis
lane. Numeric prose may consume the results only after claim registration and
verification.

---

## Alternatives Considered

### Keep Nemenyi as the Only 15-Block Pairwise Evidence

- **Pros:** No new analysis or multiplicity family.
- **Cons:** Leaves the requested focused SHAP-LIME question unresolved and can
  invite a false reading of the non-significant Nemenyi localization.
- **Why rejected:** The focused paired contrast answers a different, narrower
  question while retaining Nemenyi as the all-pairs procedure.

### Use the Existing 75-Cell H3 Wilcoxon Result

- **Pros:** Reuses a registered result with greater nominal sample size.
- **Cons:** Does not match the 15-block aggregation used by Friedman and
  Nemenyi; it would obscure the role of seeds.
- **Why rejected:** The tutor's concern is specifically the apparent tension at
  the omnibus block level. The 75-cell result remains useful corroboration, but
  it is not a substitute.

### Test Fidelity Alone Without Multiplicity Correction

- **Pros:** Minimizes the number of tests and directly follows the wording of
  the feedback.
- **Cons:** Selects one outcome after inspecting the results and creates an
  inconsistent inferential family.
- **Why rejected:** Running the same declared contrast across all five primary
  metrics and applying Holm correction is more transparent and reproducible.

### Describe the New Contrast as Pre-Specified

- **Pros:** Would present a simpler confirmatory narrative.
- **Cons:** No frozen pre-analysis artifact currently establishes that status.
- **Why rejected:** Provenance is part of the result. Retrospective relabelling
  would overstate the evidential design.

---

## Consequences

### Positive

- Resolves the Nemenyi/SHAP-LIME interpretive tension without changing existing
  tests.
- Uses the same block construction as the global EXP2 analysis.
- Makes seed aggregation and multiplicity handling explicit.
- Produces reviewable artifacts that can be claim-registered before prose is
  edited.

### Negative

- Adds a new inferential family and three generated artifacts to maintain.
- The result is a review-motivated follow-up and must be presented with that
  limitation.
- Fifteen blocks constrain power and the precision of effect estimates.

### Neutral

- Existing Friedman, Nemenyi, 45-cell, and 75-cell outputs remain authoritative
  for their original questions.
- This decision adds analysis over committed summaries; it does not authorize
  an EXP2 rerun.

---

## Compliance

Compliance will be verified by tests that assert exactly 15 unique matched
`(model, n)` blocks, one SHAP and one LIME value per block, the declared
two-sided alternatives, and Holm adjustment over exactly five metrics. The
analysis must reproduce from committed inputs in the pinned Python 3.11
environment and must not embed workstation-specific paths.

Before manuscript edits, every reported number must be registered in
`pub/claim_registry.toml`, resolved by `scripts/pubs/claim_sources.py`, and pass
the repository claim and regression checks. Review must confirm that prose
distinguishes Nemenyi, the 15-block follow-up, and the 75-cell H3 analysis.

---

## References

- [Tutor feedback implementation plan](../planning/tutor-feedback-Sep-22-2026.md)
- [Experimental design](../../thesis/capitulo-3-diseno-experimental.qmd)
- [EXP2 results](../../thesis/capitulo-4-resultados.qmd)
- [Committed EXP2 block summary](../../outputs/analysis/paper_a_exp2_stats/exp2_block_method_summary.csv)
- [ADR-0013: Publication Branching Model](0013-publication-branching-model.md)
- [RCA-001: Manuscript-Artifact Drift](../rca/RCA-001-manuscript-artifact-drift.md)
- [Regression guards](../rca/regression-guards.yaml)
