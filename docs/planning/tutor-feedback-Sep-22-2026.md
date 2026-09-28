# Implementation Plan: Tutor Feedback — September 22, 2026

> **Status:** Completed and verified
> **Created:** 2026-09-27<br>
> **Completed:** 2026-09-27
> **Feedback date:** 2026-09-22<br>
> **Active lane:** `thesis/rca-001-phase-2`<br>
> **Roles:** Architect / Scientific Editor / Developer<br>
> **Related controls:** [ADR-0013](../adr/0013-publication-branching-model.md),
> [RCA-001](../rca/RCA-001-manuscript-artifact-drift.md),
> [RCA-002](../rca/RCA-002-exp4-source-recovery.md), and
> [regression guards](../rca/regression-guards.yaml)
> **Accepted decisions:** [ADR-0014](../adr/0014-exp2-block-level-targeted-contrast.md),
> [ADR-0015](../adr/0015-masking-fidelity-ood-validity-boundary.md), and
> [ADR-0016](../adr/0016-exp4-dimensional-reliability-interpretation.md)

---

## Overview

Implement the tutor's three required corrections and two recommended
improvements while preserving the thesis's inferential boundaries, claim
traceability, and publication-lane isolation. The work adds one deterministic
analysis over existing EXP2 block summaries; it does not rerun an experiment.

Two recommendations are already partially represented in the thesis:

- Chapter 6 explicitly discloses the out-of-distribution risk of independent
  mean-value masking.
- Chapter 5 already describes the relative EXP4 agreement gradient.

The implementation will propagate and sharpen those points instead of creating
parallel or contradictory explanations.

---

## Goals

- Correct the false sentence preceding the Nemenyi fidelity table.
- Resolve the SHAP–LIME/Nemenyi tension with an aggregation-aligned paired
  Wilcoxon analysis and an exact sign test over 15 blocks.
- State explicitly how seeds enter the Friedman blocks and why they are not
  independent inferential replicates.
- Make the masking/OOD threat visible at the metric-definition, validity, and
  result-interpretation sites.
- Turn the EXP4 agreement gradient into an actionable but appropriately bounded
  research conclusion.
- Register every new numerical claim before manuscript prose consumes it.

## Non-Goals

- Do not rerun EXP2, EXP4, or any LLM judge cohort.
- Do not change existing Friedman, Nemenyi, 45-cell, or 75-cell Wilcoxon values.
- Do not reinterpret the new 15-block test as having been pre-specified unless
  an earlier frozen protocol artifact proves that provenance.
- Do not edit Paper A or Paper B+C manuscript bodies.
- Do not claim that any EXP4 dimension is currently reliable enough for
  confirmatory use; all reported ICC values remain below 0.75.
- Do not use EXP6 masking sensitivity in the thesis unless it is separately
  scoped, registered, and approved.

---

## Evidence and Decisions

### D1 — Status of the proposed SHAP–LIME block contrast

The current thesis defines H1 as a global four-method hypothesis tested by
Friedman and localized with Nemenyi. It assigns the explicit SHAP–LIME Wilcoxon
analysis to the separate 75-cell paired study. Therefore, the new 15-block test
will be reported as a **review-motivated, aggregation-aligned targeted
follow-up**, not retrospectively described as pre-specified.

The global H1 decision remains based on Friedman. Nemenyi remains the
conservative simultaneous post-hoc analysis. The new paired analysis supports
the narrower SHAP–LIME statement using the same block aggregation as Friedman.

### D2 — Multiplicity family

Compute block-level SHAP–LIME Wilcoxon tests for all five declared primary
metrics and apply Holm correction across those five tests. This avoids defining
a one-test family after observing fidelity. Report fidelity in the H1 section;
retain the complete generated artifact for auditability.

The exact sign test is directional corroboration. It does not replace the
Wilcoxon decision.

### D3 — Masking/OOD response

Adopt the tutor's explicit-disclosure option. The implemented training-mean
replacement is deterministic and common across methods, but it does not preserve
the joint feature distribution and therefore does not eliminate OOD bias.

### D4 — EXP4 interpretation boundary

Treat the higher agreement for completeness and semantic plausibility as a
relative, hypothesis-generating gradient. It motivates future bounded use for
verifiable properties after human calibration; it does not establish current
confirmatory validity for any dimension.

---

## Expected Statistical Result

The following values were independently derived from the committed
`exp2_block_method_summary.csv` and are regression targets for the new script:

| Quantity | Expected value |
|:--|--:|
| Blocks | 15 |
| Positive SHAP–LIME fidelity differences | 15 |
| Negative differences / ties | 0 / 0 |
| Wilcoxon statistic | 0 |
| Wilcoxon raw two-sided p-value | `6.103515625e-05` |
| Wilcoxon Holm p-value, five-metric family | `3.0517578125e-04` |
| Exact two-sided sign-test p-value | `6.103515625e-05` |
| Mean fidelity difference | approximately `+0.2479` |

These values must be regenerated in the project-pinned environment before they
are registered or inserted into the thesis.

---

## Branch and Commit Strategy

| Sequence | Lane | Purpose | Merge target |
|:--:|:--|:--|:--|
| 1 | `results/exp2-block-shap-lime` | Analysis script, tests, and new exports | `main` only |
| 2 | `pubs/tutor-feedback-claims` | Claim resolvers and registry entries | `main` |
| 3 | `thesis/rca-001-phase-2` | Thesis prose and bibliography | Remains branch-private |
| 4 | `pubs/tutor-feedback-context` | Sync record and active-context handoff, if needed | `main` |

No commit may mix shared substrate files with manuscript-body files. After each
trunk merge, merge `main` into the thesis lane; never merge publication lanes
into each other.

---

## Implementation Tasks

### TF-01 — Preflight and environment

**Objective:** establish a current, reproducible starting point.

**Actions:**

1. Confirm the thesis lane is clean and level with its remote.
2. Reread `docs/context/ACTIVE_CONTEXT.md` and the current regression guards.
3. Use a Python 3.11 environment compatible with the pinned scientific stack.
4. Run the existing verifiers before any edit and save their outputs.
5. Record hashes of existing `outputs/analysis/paper_a_exp2_stats/` files so the
   new analysis cannot silently rewrite prior evidence.

**Exit criteria:** clean baseline, compatible environment, and all applicable
pre-change checks recorded.

### TF-02 — Generate block-level paired evidence

**Create:**

- `scripts/run_exp2_block_paired_analysis.py`
- `tests/test_exp2_block_paired_analysis.py`
- `outputs/analysis/paper_a_exp2_stats/paired_blocks_shap_lime.csv`
- `outputs/analysis/paper_a_exp2_stats/wilcoxon_shap_lime_blocks.csv`
- `outputs/analysis/paper_a_exp2_stats/sign_test_shap_lime_blocks.csv`

**Requirements:**

1. Read the committed `exp2_block_method_summary.csv`.
2. Require exactly 15 unique `(model, n)` blocks and one SHAP/LIME value per
   block and metric.
3. Export the paired block values and differences.
4. Run two-sided Wilcoxon signed-rank tests over the five primary metrics.
5. Apply Holm correction across the five Wilcoxon tests.
6. Compute exact two-sided sign tests and positive/negative/tie counts.
7. Sort output deterministically and use repository-relative provenance paths.
8. Fail on missing blocks, duplicate blocks, missing values, or method mismatch.

**Tests:**

- The fidelity row matches every value in the Expected Statistical Result table.
- Seed-level rows cannot be mistaken for independent blocks.
- Repeated execution produces byte-identical new outputs.
- All pre-existing EXP2 analysis artifacts remain byte-identical.

### TF-03 — Register new numerical claims

**Modify:**

- `scripts/pubs/claim_sources.py`
- `pub/claim_registry.toml`

**Actions:**

1. Add resolvers for the new paired-block and sign-test exports.
2. Register block count, sign counts, Wilcoxon statistic, raw and Holm p-values,
   sign-test p-value, and mean fidelity difference.
3. List every manuscript site that prints each value.
4. Add the new result exports as cited artifacts if the manuscript names them.
5. Negative-test the registry by changing one manuscript value and confirming
   that `verify_claims.py` fails at the altered site.

**Exit criteria:** registry checks pass and no new number relies on
`[[unbacked]]`.

### TF-04 — Correct and extend the statistical narrative

**Modify:**

- `thesis/capitulo-3-diseno-experimental.qmd`
- `thesis/capitulo-4-resultados.qmd`
- `thesis/capitulo-6-conclusiones.qmd`

**Chapter 3 changes:**

- Define the Friedman block score as the mean across qualified seeds:
  `mean(g,k,n,m) = sum_s(y[g,k,s,n,m]) / r[g,k,n]`.
- State that seeds are averaged within `(g, n)` and are not treated as 75
  independent Friedman blocks.
- State that SHAP and LIME contribute five seeds per block; Anchors and DiCE use
  the qualified seeds documented in the coverage section.
- Add the targeted 15-block Wilcoxon/sign-test procedure, its five-metric Holm
  family, and its review-motivated status.

**Chapter 4 changes:**

- Replace the false sentence claiming every Nemenyi pair exceeds the critical
  difference with the exact three significant pair identities.
- Preserve the Nemenyi table and its SHAP–LIME non-significant result.
- Add the 15-block Wilcoxon and sign-test results after the Nemenyi discussion.
- Explain why the tests answer different questions and use different power.
- Keep the 15-block analysis distinct from the existing 75-cell H3 analysis.
- Update the H1 results overview and claim-traceability row.

**Chapter 6 changes:**

- Update the H1 synthesis row with the global Friedman result and the targeted
  block-level evidence.
- Do not alter the formal H1 definition in Chapter 1.

### TF-05 — Close the masking/OOD validity loop

**Modify:**

- `thesis/capitulo-1-marco-teorico.qmd`
- `thesis/capitulo-3-diseno-experimental.qmd`
- `thesis/capitulo-4-resultados.qmd`
- `thesis/capitulo-6-conclusiones.qmd`
- `thesis/references.bib`

**Actions:**

1. At the fidelity definition, state that each feature is replaced independently
   by its training-set mean in transformed feature space.
2. Add the OOD mechanism and residual differential-bias risk to the Chapter 3
   validity-threat table or its explanatory text.
3. Replace Chapter 4's generic alternative-operationalization caveat with an
   explicit OOD masking limitation and a cross-reference to Chapter 6.
4. Preserve Chapter 6's existing detailed disclosure; remove duplication rather
   than repeat its full numeric example elsewhere.
5. Add and verify the Hooker/ROAR and Rong references using the existing
   publication bibliography as provenance, then run the reference audit.

**Exit criteria:** the thesis no longer criticizes perturbation-based fidelity
without explicitly delimiting its own masking metric.

### TF-06 — Strengthen the EXP4 agreement-gradient conclusion

**Modify:**

- `thesis/capitulo-5-taxonomia.qmd`
- `thesis/capitulo-6-conclusiones.qmd`

**Actions:**

1. Preserve the registered ICC and Krippendorff-alpha values.
2. State that agreement increases relatively for dimensions with more
   verifiable referents and falls for stakeholder-/context-dependent dimensions.
3. Convert that gradient into a future design recommendation: prioritize
   explicit correctness criteria and stakeholder information.
4. State explicitly that the relative gradient does not authorize current
   confirmatory LLM-as-a-judge use because no dimension reaches 0.75.
5. Add stratified human calibration by dimension to the Chapter 6 future-work
   paragraph.

**Guard:** Chapter 5 is protected by both RCA-001 and RCA-002. Run both guard
test sets after this edit.

### TF-07 — Cross-document and top-level consistency

**Actions:**

1. Run [the top-level statement sweep](../review/top-level-statement-sweep.md)
   for H1, the Resumen, Abstract, and Chapter 6.
2. Confirm that Paper A and Paper B+C remain factually compatible without body
   edits.
3. Update `docs/reports/sync/thesis_paper_sync_matrix.md` only if the new
   thesis-only block analysis requires an explicit boundary entry.
4. Confirm the thesis uses the functional study names fixed by ADR-0012.
5. Confirm no literal chapter or section numbers were introduced.

---

## Verification Plan

### Automated checks

Run from the repository root in the compatible environment:

```powershell
python scripts/run_exp2_block_paired_analysis.py
python -m pytest tests/test_exp2_block_paired_analysis.py
python scripts/pubs/verify_claims.py
python scripts/pubs/verify_claims.py --coverage-report
python scripts/pubs/verify_sync.py
python scripts/pubs/verify_exp4_reconstruction.py
```

Also verify:

- No retired value reappears.
- No new unresolved cross-reference or citation is present.
- Only the three planned result exports differ under the EXP2 analysis output
  directory.
- New citations are used, unique, and present in `thesis/references.bib`.

### Render and visual checks

1. Close the thesis DOCX in Word.
2. Run `thesis/render.ps1`.
3. Inspect the render log for unresolved citations and cross-references.
4. Inspect `word/document.xml` for heading numbering, table borders, caption
   properties, and unresolved reference text.
5. Open the DOCX in Word, refresh the table of contents, save, and recheck the
   affected pages visually.

---

## Risks and Mitigations

| Risk | Mitigation |
|:--|:--|
| Retrospective analysis described as pre-specified | Label it review-motivated unless a frozen artifact proves otherwise |
| Seed pseudoreplication | Export exactly 15 block pairs and test the block keys |
| Multiplicity chosen after seeing fidelity | Compute and Holm-correct the full five-metric block family |
| Existing EXP2 artifacts rewritten with laptop-specific paths | Use a focused new script and assert old artifact hashes are unchanged |
| OOD risk minimized by deterministic mean masking | Disclose that determinism does not preserve the joint distribution |
| EXP4 gradient overclaimed | Preserve the below-0.75 boundary at every recommendation site |
| Green render hides layout defects | Inspect DOCX XML and the Word-rendered pages |

---

## Success Criteria

- [x] The sentence before the Nemenyi table agrees with all six table rows.
- [x] The new analysis deterministically reproduces the expected 15-block
      fidelity result and five-test Holm correction.
- [x] Seeds are explicitly averaged within blocks and never counted as 75
      independent Friedman units.
- [x] Nemenyi, the new 15-block contrast, and the existing 75-cell H3 analysis
      are clearly distinguished.
- [x] Every new numeric value is artifact-backed and registered before use.
- [x] The masking/OOD limitation appears at the methods and interpretation
      boundaries, with the detailed Chapter 6 disclosure retained.
- [x] The EXP4 gradient yields a bounded research recommendation without
      implying current confirmatory reliability.
- [x] All RCA-001 and RCA-002 checks pass.
- [x] The top-level statement sweep reports no contradiction.
- [x] The final DOCX has no unresolved references and passes XML and visual QA.
- [x] No Paper A or Paper B+C manuscript body was changed.

---

## Completion Record

Implementation completed on 2026-09-27. Verification passed for the deterministic
15-block analysis and tests, claim re-derivation and coverage, publication sync,
EXP4 source pins, source formatting, DOCX archive integrity, unresolved-reference
scans, and a rendered 172-page visual review. The thesis DOCX was regenerated and
contains the implemented tutor-feedback changes.
