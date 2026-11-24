# RCA-006: Paper E (AAIR) minus signs written as Word equations, invisible to some readers

**Status:** Resolved (fix and guard on `paper/e-aair-revision-1`)
**Severity:** High (a reviewer read wrong signs in three tables of a submitted manuscript)
**Date:** 2026-11-24
**Found by:** AAIR reviewer 2, decision of 2026-11-24 (item R2-1 of
`docs/reports/paper_e/aair_journal/revision_1/REVIEW_ANALYSIS.md`)

## Issue Summary

Reviewer 2 reported that Tables 1, 4 and 5 of the submitted Paper E show positive differences
and interval bounds where the means imply negative ones (e.g., Table 4, MLP: 0.364 and 0.305,
difference shown as 0.059, interval [0.069, 0.049]). The analysis and the LaTeX tables were
correct (−0.059 [−0.069, −0.049]); the signs were lost on the way to the reader.

## Timeline

| When | What |
|---|---|
| 2026-10-22 | Paper E submitted to AAIR from `build_paper_e_aair_docx.py` output |
| 2026-11-24 | Decision: reviewer 2 reports the sign inconsistency |
| 2026-11-24 | Cause found, fixed, check added (this RCA) |

## Symptoms

- In the submitted `.docx`, each of the 58 minus signs is a one-character OMML equation
  (`<m:oMath>…<m:t>-</m:t>…</m:oMath>`) followed by the number in an ordinary run.
- Word and LibreOffice draw them (Word's PDF has 58 U+2212). A reader or converter that skips
  equations (plain-text extraction, some web previews and conversions) shows the number
  without its sign. The first check of this session read only `w:t` and also saw no signs.

## Root Cause Analysis

### The 5 Whys

1. Why did the reviewer see no signs? Their copy did not render the equation objects.
2. Why were signs equation objects? The LaTeX source writes them `$-$` (the table generator
   of `build_paper_e.py`), and pandoc turns any `$…$` into OMML.
3. Why was that not noticed? The build checked pages, floats, abstract and references, and the
   PDF was printed by Word, which draws the equations; no check read the Word text.
4. Why no text check? Numbers were verified in the LaTeX (`verify_claims.py`), assumed to be
   carried to Word unchanged.
5. Why the assumption? The conversion LaTeX → Word was treated as layout only, not as a
   step that can change content.

### Root Cause Statement

The Word build carried numeric signs as math objects instead of text, and nothing verified the
numbers of the Word file, only those of the LaTeX source.

### Contributing Factors

- `$-$` is the right LaTeX for a minus in text mode, so the source looked correct.
- Visual review was done on the Word-printed PDF, the one rendering that hides the problem.

## Resolution

### Immediate Fix

`plain_signs()` in `docs/reports/paper_e/aair_journal/scripts/build_paper_e_aair_docx.py`:
`$-$` becomes U+2212 and bare `$n$` becomes `n` before pandoc, so every sign is ordinary text.

### Permanent Fix

`verify_numbers()` runs on every build and fails it if (a) any Word equation contains only a
sign or digits, (b) any generated table row is not found, cell by cell, in the plain text of
the Word table, or (c) the count of negative numbers differs between source and Word text.
Tested both ways: the submitted `.docx` fails (58 sign equations); the revision build passes
(56 table rows, every sign). The submitted edition can no longer be rebuilt by the script
(`--edition submitted` is refused).

## Regression Prevention

### Tests Added

- `verify_numbers()` inside the build (no build completes without it).
- `docs/reports/paper_e/aair_journal/revision_1/scripts/check_signs.py`: the same check on the
  built file, runnable on its own.

### Standards Updated

None; the rule is in the guard below. Other Word builders converting LaTeX through pandoc
(Paper B C&I, Paper G) should be checked against the same invariant: review trigger.

### Regression Guard

`docs/rca/regression-guards.yaml`, id RCA-006.

## Verification

- `build_paper_e_aair_docx.py` (rev1): "number check: 56 table rows and every sign match".
- Plain-text read of the revision Table 4: `Adult | MLP | 0.364 | 0.305 | −0.059 | [−0.069, −0.049] | 5/5`.
- Revision PDF: 58 U+2212, as in the source.

## Lessons Learned

- A format conversion is a content step: verify numbers on the file that is sent.
- Check with the weakest reader (plain text), not with the program that wrote the file.

### Action items

- Check Papers B and G Word builds for `$-$` or numbers inside OMML (follow-up, outside this lane).

## References

- `docs/reports/paper_e/aair_journal/revision_1/DECISION_LETTER.md` (reviewer 2, item 1)
- RCA-001 (numbers drift from artifacts): this is its Word-side counterpart
