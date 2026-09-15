# RCA-003: TOML escapes silently corrupt LaTeX in the claims SSOT

**Status**: Closed
**Severity**: Medium (reader-visible defect on page 1 of a submission-ready PDF)
**Opened**: 2026-09-14
**Role**: Scientific Editor → Incident Responder
**Related**: [RCA-001](RCA-001-manuscript-artifact-drift.md) (the fragment
pipeline this defect travels through); commit `3d6ba90ba` (the first instance)

## Symptoms

Pre-submission check of Paper B+C for TMLR, 2026-09-14. The abstract on page 1
of `paper_bc_tmlr.pdf` read:

> for tree-based models, SHAP's extttTreeExplainer reverses this ordering

The intended text was `SHAP's \texttt{TreeExplainer}`. The PDF committed on
2026-09-06 as "submittable" carried the defect; the readiness checklist, the
anonymity pass and all three verifiers were green.

## Evidence

- `pub/claims.toml:69` held `\texttt` with a single backslash inside a `"""`
  basic string. TOML reads `\t` as a TAB, so the generated
  `pub/fragments/paper_bc_abstract_en.tex` contained `<TAB>exttt{...}`, which
  LaTeX typesets as the letters "exttt".
- Present since `95b9fb53c` (2026-08-24), when the abstract moved into the SSOT.
- **This is the second instance.** `3d6ba90ba` (2026-09-05) fixed `vs.\` at a
  line end, which TOML read as a line continuation and which ate the space
  ("vs.694.6 ms"). That fix doubled the one backslash it concerned; the
  `\texttt` one line below was not examined.
- A scan of every `"""` string in `claims.toml` found no other odd-length
  backslash run: all 15 other LaTeX macros in the file are correctly doubled.
  A scan of every fragment found no other control character.

## Root cause

1. **Why did the PDF print "exttt"?** The fragment held a TAB instead of `\t`.
2. **Why?** `claims.toml` stores LaTeX in TOML basic strings, where a backslash
   is an escape character.
3. **Why was it not caught?** Nothing checks the fragment text itself.
   `verify_sync.py` checks only that fragments exist and are wired in;
   `verify_claims.py` checks numbers, and this sentence carries none.
4. **Why did the first instance not prevent the second?** It was fixed as a
   point defect rather than as a class: one backslash was doubled, and no check
   was added for the others.
5. **Why did review miss it?** Every check before submission read the source or
   the verifier output, not the rendered abstract.

**Root cause:** an encoding hazard in the SSOT format (LaTeX inside TOML basic
strings) with no mechanical check, and a first occurrence fixed at the instance
level instead of the class level.

## Fixes (2026-09-14)

- `pub/claims.toml`: `\texttt` → `\\texttt`. Fragment updated to match; only
  that line changed.
- `scripts/pubs/verify_sync.py` gained two checks, run in CI by
  `pubs-sync.yml`:
  1. every backslash run inside a `"""` string in `claims.toml` has even length;
  2. no generated fragment contains a control character.
- **Negative-tested.** Against the pre-fix `claims.toml` and fragment,
  `verify_sync.py` exits 1 naming `claims.toml:69` and the TAB at
  `paper_bc_abstract_en.tex:20`; with the source fixed but the fragment stale,
  it still exits 1 on the fragment; after the fix it exits 0.
- `paper_bc_tmlr.pdf` rebuilt on the paper lane and the abstract re-read in the
  PDF text.

Found in the same pass and fixed alongside, a separate defect: the artifact
bundle did not include `paper_bc_tmlr_supplementary.pdf`. OpenReview accepts
one supplementary file, so reviewers would never have seen Tables S1-S6.
`build_artifact_bundle.py` now copies it in as `supplementary_tables.pdf`, and
refuses to write a bundle when any listed input is missing (it previously
printed the omission and zipped anyway).

## Lessons

- **A defect that recurs is a class.** Fix the class, with a check, on the
  second occurrence at the latest.
- **Read the rendered output of any prose that travels through a generator.**
  Source and verifier output were both clean while the PDF was wrong; the same
  lesson as the thesis notes' "a green render proves nothing about layout".
