# Paper B+C pre-submission review plan (TMLR)

**Date:** 2026-09-28
**Role:** Architect (plan); Scientific Advisor carries out Phases 1-3, Scientific Editor Phase 4
**Lane:** `paper/bc-venue-definition` (worktree `../xai-paper-bc`), base `835bde4e0`
**Scope:** `docs/reports/paper_bc/paper_bc_tmlr.tex` (2,036 lines, 26 pp) and
`paper_bc_tmlr_supplementary.tex` (413 lines, 5 pp)

## Why a new review

The last rigor review (`docs/reports/paper_bc/scientific-rigor-review_paper_bc_jmlr_2026-07-28.md`)
read the JMLR version. None of the following changes have been reviewed since:

- the move to TMLR, including the TMLR style file, anonymity and the Broader Impact Statement;
- the removal of every result shared with the published RIMI paper (Paper A);
- the corpus rebuilt at 44 papers, with the new Corpus provenance paragraph;
- the ICC relabelled ICC(1,1), plus the Table S3 and S6 corrections (RCA-002);
- the EXP4 replication cohort and the corrected sample of 192 cases (ADR-0017);
- the restated EXP3 sentence in the abstract.

No reference audit of this paper is on record. `paper_bc_tmlr.tex` is also outside
`[coverage]`, so nothing checks that each number it prints is registered.

## Constraints

- Guarded files: RCA-001 (main text, registry), RCA-002 (main text, supplementary,
  EXP4 CSVs), RCA-003 (`pub/claims.toml`, abstract fragment). Phases 1-3 edit none of them.
- Register first, edit second (RCA-001, invariant 1). A claim that is rescoped
  triggers `docs/review/top-level-statement-sweep.md`.
- No result may be shared with Paper A (RCA-001, prior-publication invariant).
- The committed EXP4 cohort stays primary. Cohort 2 is reported as a replication and
  never replaces it (ADR-0017). Every summary must say the primary ICC is below 0.75
  in both cohorts (ADR-0016 as amended).
- Commit and push each report as soon as it is written.

## Phase 1 - Scientific rigor review (`scientific-rigor-review`)

1. Record the `verify_claims.py` summary line as the baseline.
2. Read the whole main text and supplementary: the built PDF for the rendered text,
   and the source for the labels.
3. Mark each of the 2026-07-28 findings F01-F04 as confirmed fixed, carried forward
   or reopened.
4. Map every top-level claim to its evidence: the title, abstract, contributions list
   and conclusion each map to body sections and artifacts.
5. Re-derive each number the argument depends on, stating its aggregation level. Check
   the EXP2 statistics, the EXP3 fidelity ordering and LIME moderation, the EXP4 ICC and
   Krippendorff's alpha for both cohorts, and the corpus distribution.
6. Score D1-D6, and add a TMLR section that judges the paper against the venue's two
   acceptance criteria: the claims are supported by evidence, and the work is of
   interest to some part of the TMLR audience.
7. Check figures separately. A number baked into a PDF figure is invisible to the
   verifier, so each figure with data labels needs a committed generator.

**Output:** `docs/review/scientific-rigor-review_paper_bc_tmlr_2026-09-28.md`, with
severity-ranked findings (major / minor / suggestion).

## Phase 2 - Reference audit (`reference-audit`)

Check for duplicate keys and entries, entries that are cited but missing, entries that
are present but never cited, and wrong metadata (DOI, venue, year, arXiv version when a
published version exists). Check that the RIMI self-citation is phrased in the third
person for the anonymous build.

**Output:** `docs/review/reference-audit_paper_bc_tmlr_2026-09-28.md`

## Phase 3 - Coverage report (read-only)

Run `verify_claims.py --coverage-report` for `paper_bc_tmlr.tex` and the
supplementary. Sort each numeric literal into one of four classes: registered, retired,
structural, or unregistered (each unregistered one becomes a finding). Do **not** add
the files to `[coverage]` yet: that turns CI red on every lane until the list is cleared.

**Output:** a section of the Phase 1 report, or
`docs/review/coverage-triage_paper_bc_tmlr_2026-09-28.md` if it runs long.

## Decision point - author

Present the findings and agree which ones to fix, defer or accept. Any fix that changes
a claim's scope, a number or a result shared with the thesis goes through the sync
matrix (`docs/reports/sync/thesis_paper_sync_matrix.md`).

## Phase 4 - Remediation (Scientific Editor, separate session)

1. Register new or changed numbers in `pub/claim_registry.toml`, then edit the prose.
2. Make one atomic commit per finding or cluster of related findings.
3. Add both `.tex` files to `[coverage]` once the triage list is cleared.
4. Run the top-level statement sweep if any claim was rescoped.

## Phase 5 - Submission gate (QA)

Run the whole "After any revision" checklist in
`docs/reports/paper_bc/OPENREVIEW_SUBMISSION.md`:

1. Rebuild both PDFs with 0 undefined references.
2. Read page 1 of the built PDF.
3. Run all three verifiers.
4. Scan the PDFs and the bundle for author identity.
5. Run the shared-result query against Paper A.
6. Rebuild the bundle.
7. Regenerate the sheet's abstract.

Then report the result to the author in writing.

## Author items outstanding (not blocked by this plan, but they block filing)

- Sign-off that the detailed revision is finished.
- Verification of the 28 reconstructed rows of the review corpus (Next Steps 0a).
- Confirmation that the paper is under review at no other venue.
- After filing: email the editor note to tmlr-editors@jmlr.org (not as a forum comment).

## Estimate

| Phase | Effort |
| ----- | ------ |
| Phase 1 | ~3-4 h |
| Phase 2 | ~1 h |
| Phase 3 | ~1 h |
| Phase 4 | depends on the findings |
| Phase 5 | ~1 h |
