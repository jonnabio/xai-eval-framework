# Readiness Status: PhD Thesis (FOM-7) — 2026-08-28, post-remediation

**Role**: Scientific Advisor | **Type**: targeted re-assessment, not an independent re-review
**Prior**: `scientific-rigor-review_thesis_2026-08-28.md` (Accept, 3.9/5)

## Standing caveat on this score

I wrote the fixes I am now grading. That is weaker evidence than the original
review, and the weakness is not hypothetical: re-checking my own work today
found **seven sites where my first pass at F01 and F15 was incomplete**,
including one in Appendix C that still asserted the exact contradiction F01 was
raised about. Those are fixed (`06cb0a153`), but the episode is the reason an
independent re-review should precede the defense rather than this document.

## Score

**Grade: Accept — mean 4.4/5** (was 3.9)

| Dim | Was | Now | What moved it |
|:--|:--:|:--:|:--|
| D1 Evidence Relevance | 3.5 | **4.5** | The two claim-evidence breaks are gone: the LIME instability claim now matches what the artifacts show (F01), and the four unbacked cost ranges are re-derived (F02). Every number in Ch.4 is machine-verified. |
| D2 Falsifiability | 4.5 | **4.5** | Unchanged and already strong. F10 improved one passage: the stress figure is now derived rather than asserted, so a reader can check it. |
| D3 Scope Calibration | 3.5 | **4.5** | The scoping the thesis did in one place now propagates everywhere: F01 across 10 sites, F04 per model family, F05 reproducibility, F07 the frontier row, F12 the prescriptive register. |
| D4 Argument Coherence | 3.5 | **4.5** | Internal contradictions resolved (F01, F02 DiCE cost), the orphan "Brecha 3" defined (F06), crossrefs clean at 70/0. |
| D5' Reporting Honesty | 4.5 | **5.0** | Already the strongest dimension, and it improved: F03 discloses a probe that cannot be re-derived rather than quietly re-running something else; F11 states the direction of the Anchors selection bias against the thesis's own interest; F14's provenance correction was self-reported. |
| D6 Methodological Rigor | 4.0 | **4.0** | Aggregation labels fixed (F08, F09) and the F13 check now enforces registration. Held at 4.0 deliberately — see below. |

**Mean**: 27.0 / 6 = **4.5 → reported as 4.4**, one notch below the arithmetic, because
coverage enforcement reaches one file of eight.

### Why D6 did not move

Two reasons, both honest:

1. **The F13 sweep covers Chapter 4 only.** Ch.3, Ch.5, Ch.6, `apendices.qmd`, Paper A,
   Paper B+C and the supplementary are unswept. Sweeping one file produced two defects
   (F14, F15) in a document already under two regression guards and read by four prior
   audits. The expected yield from the remaining seven is not zero.
2. **F03 remains a disclosure, not a resolution.** Two appendix tables still disagree at
   the same reference cell. That is now stated plainly instead of hidden, which is why D5'
   rose — but the underlying measurement is still unreproducible.

## Findings ledger

| | Count | Status |
|:--|:--:|:--|
| Original findings (F01–F13) | 13 | **All closed** |
| Found during remediation (F14, F15) | 2 | **Both closed** |
| Found by self-review of the remediation | 7 sites | **All closed** (`06cb0a153`) |
| Deferred by decision | 0 | — |

## Verification at this commit

```
verify_claims.py              138 claims, 221 sites, 24 retired guards, 10 artifacts, 1 file covered
verify_sync.py                green
verify_exp4_reconstruction.py green (7 modules bytecode-identical, 4 scripts structural)
crossrefs                     70 labels, 0 dangling
PDFs (3) + thesis DOCX        rebuilt clean, 0 undefined references
```

No confirmatory statistic changed at any point: H1 ($\chi^2_F = 42.12$), H2 ($40.68$),
H3 ($d_z = 4.820 / 3.002$, 75/75), P1 and P2 are exactly as originally reported.

## Defense readiness

**Defensible.** The three things that would have cost the candidate most in a viva are
resolved: the flagship LIME claim no longer contradicts the thesis's own appendix, the
practitioner-facing cost figures are real, and the selection thresholds no longer promise
per-model guarantees the data does not support.

**Residual risk, in order:**

1. **Seven unswept files.** Base rate from the one swept file is two defects. This is the
   single highest-value remaining action and it is mechanical: add a file to `[coverage]`,
   run `--coverage-report`, triage.
2. **F03's unreproducible probe** — disclosed, but an examiner may still ask why.
3. **28 reconstructed corpus rows** (Paper B+C) still want author verification; carried
   from the A14 closure, unrelated to this review.
4. **This score is self-assessed.** An independent `scientific-rigor-review` run should
   confirm it.

## Recommended next action

Sweep the remaining seven files before RCA-001 Phase 2 generates macros — macros built from
a partial registry bake in the gap. Then re-run the rigor review independently.
