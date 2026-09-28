# ADR-0018: The CIFIE Chapter Excludes Results of the Unpublished Paper B+C

> **Status:** Accepted<br>
> **Date:** 2026-09-27<br>
> **Related:** [ADR-0013](0013-publication-branching-model.md) (the `chapter/cifie-*`
> lane), [RCA-001](../rca/RCA-001-manuscript-artifact-drift.md),
> `docs/review/cifie-chapter-sync_2026-09-27.md`

---

## Context

The CIFIE collective book chapter is an archival publication derived from the
thesis. Paper B+C is under preparation for TMLR, which does not accept results
already published elsewhere. That rule is why Paper B+C was scrubbed of every
result shared with the published RIMI paper (Paper A). The chapter printed
Paper B+C's central results: the 75-cell paired SHAP–LIME effect sizes and
mean differences, LIME's stability CV and Anchors' coverage percentage.
Nothing detected the overlap, because the chapter was outside the claim
registry.

## Decision

1. **The chapter prints no result of Paper B+C while Paper B+C is
   unpublished** (author decision 2026-09-27). Where the chapter needs those
   results, it states their direction in prose and cites the thesis.
2. **Results already published in RIMI may appear.** They are cited to RIMI
   (Herrera-Vásquez & Herrero-Uceda, 2026). CIFIE and RIMI are connected, so no
   further disclosure note is needed.
3. **Thesis-only results may appear.** This includes the thesis's
   review-motivated 15-block SHAP–LIME follow-up, reported by counts and
   $p_{\mathrm{Holm}}$ only. Its mean difference equals the 75-cell mean
   difference, which is a Paper B+C result.
4. **The rule is enforced, not remembered.** `[exclusivity]` in
   `pub/claim_registry.toml` lists the chapter's sections and Table 4;
   `verify_claims.py` fails on any value there that is registered for Paper B+C
   and not for Paper A. It matches by value at the printed precision. Paper B+C
   sites must therefore be registered for every result the paper prints.
5. **The chapter is under `[coverage]`.** Every result-shaped number in it is
   registered with a chapter site and a pinned count.

## Consequences

- The chapter can be submitted to CIFIE at any time without creating a
  prior-publication problem for Paper B+C.
- When Paper B+C is published, the rule can be relaxed: add Paper B+C to
  `allow_if_also`, or remove the `[exclusivity]` entry, and cite the paper.
- The chapter's empirical section is less quantitative on the SHAP–LIME
  contrast; the thesis carries the detail.
- Any future chapter number that coincides in value with a Paper B+C result
  fails CI, even if it means something else. It then needs an
  `[[exclusivity_exception]]` with a reason.
