---
name: scientific-rigor-review
description: Epistemic rigor review of an idea, hypothesis, manuscript or thesis chapter in plain prose. Adapts the ai-research pack's ARA rigor-reviewer (six dimensions) to manuscripts that are not ARA directories. Produces a severity-ranked report in docs/review/scientific-rigor-review_*.md. Read-only on the manuscript.
metadata:
  project: xai-eval-framework
  role: Scientific Advisor
  rebuilt: 2026-09-27 (original was local-only and lost; see docs/context/ACTIVE_CONTEXT.md)
---

# Skill: Scientific Rigor Review

> Review whether a manuscript's claims are supported by its evidence, scoped
> correctly, falsifiable, coherent, honestly reported and methodologically
> sound. Report only: never edit the manuscript under review.

Triggers (`.aceconfig`): idea review, hypothesis review, peer review, science
correctness, methodology review, scientific rigor.

Upstream basis: `.ace/packs/ai-research/rigor-reviewer/SKILL.md` (ARA Seal
Level 2). That skill reads structured ARA files; this one reads prose.

---

## Before reading

1. Read `docs/context/ACTIVE_CONTEXT.md` and `docs/rca/regression-guards.yaml`.
   Note which files under review are guarded (RCA-001, RCA-002, RCA-003) and
   read the named RCAs.
2. Find the previous review of the same document in `docs/review/`. Every
   prior finding is either **confirmed fixed**, **carried forward** (renumbered,
   marked "carried from <date> Fnn") or **reopened**.
3. Run `python scripts/pubs/verify_claims.py` and record its summary line.
   A number the verifier cannot see (in a figure, in prose without a
   registered value) is in scope for this review.

## Six dimensions (score 1-5, halves allowed)

| Dim | Name | Question |
|---|---|---|
| D1 | Evidence relevance | Does the cited evidence substantively address what each claim asserts, of the right type (causal vs associative, confirmatory vs exploratory)? |
| D2 | Falsifiability | Is each hypothesis stated so that an independent researcher could say what result would refute it? |
| D3 | Scope calibration | Do claims stay inside the population, datasets, models and conditions actually tested? Watch universal framings ("estructuralmente", "always", "across") built on one benchmark. |
| D4 | Argument coherence | Do chapters agree with each other and with the Resumen/Abstract? Same quantity, same value, same aggregation level everywhere. |
| D5' | Reporting honesty | Are negative results, deviations, missing data, reconstructions and retrospective analyses disclosed where the claim is made? |
| D6 | Methodological rigor | Are tests, multiplicity control, units of analysis (blocks vs runs vs seeds), reliability models and effect sizes appropriate and correctly described? |

Anchors per dimension: 5 = no material issue; 4 = minor issues only; 3 = at
least one major issue that is fixable in prose; 2 = several major issues or
one that changes a conclusion; 1 = the dimension fails.

## Procedure

1. Read the whole scope, not excerpts. Record the file list in the report.
2. For every numeric claim that carries an argument, re-derive it from the
   artifact (`outputs/analysis/...`, `experiments/...`) or confirm it is
   registered in `pub/claim_registry.toml`. State the aggregation level.
3. Build a claim map: each top-level statement (objectives, hypotheses,
   Resumen/Abstract; see `docs/review/top-level-statement-sweep.md`) -> the
   body sections and artifacts that support it.
4. Look for contradictions between the document's own results before looking
   outward. The most damaging findings are internal.
5. Grade each finding: **major** (changes or undermines a conclusion),
   **minor** (misstatement that does not change a conclusion), **suggestion**.
6. For each finding give: location (file:line), quoted text, the evidence that
   contradicts or fails to support it, the dimension(s), and a concrete fix.
   Do not apply the fix.

## Report

Write `docs/review/scientific-rigor-review_<document>_<YYYY-MM-DD>.md`:

```markdown
# Scientific Rigor Review: <document>

**Date**: YYYY-MM-DD | **Reviewer role**: Scientific Advisor | **Grade**: Accept / Minor revision / Major revision / Reject
**Mean score**: x.x | **Dimensions**: D1=_ D2=_ D3=_ D4=_ D5'=_ D6=_

**Scope reviewed**: ...
**Prior review**: ... (fixed / carried / reopened)
**Regression guards**: ... ; verify_claims summary line.

## One-line summary
## Strengths
## Findings
### F01 [major] — D1 (Evidence Relevance) / ...
## Dimension rationale
## Readiness assessment
## Questions for the author
```

## Rules

- Read-only: no edit to any manuscript, fragment or registry during a review.
- Never assert a number you did not re-derive or find registered.
- A finding about a guarded file names the guard and its invariant.
- Spanish manuscript prose is quoted in Spanish; the report is in English.
