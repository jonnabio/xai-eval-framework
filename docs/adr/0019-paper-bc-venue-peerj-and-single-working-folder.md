# ADR-0019: Paper B+C Moves to PeerJ Computer Science; Paper Work Returns to the Main Folder

> **Status:** Accepted<br>
> **Date:** 2026-10-02<br>
> **Amends:** [ADR-0013](0013-publication-branching-model.md) (the paper lane's
> separate working tree)<br>
> **Related:** [ADR-0017](0017-exp4-cohort2-replication-reporting.md),
> [ADR-0018](0018-cifie-chapter-excludes-unpublished-results.md),
> [RCA-001](../rca/RCA-001-manuscript-artifact-drift.md),
> `docs/reports/paper_bc/TMLR_REJECTION_RECORD.md`,
> `docs/planning/paper_bc_peerj_retarget_plan_2026-10-02.md`

---

## Context

Paper B+C was filed with TMLR on 2026-09-30 as submission 12779 and rejected
without review. The notice gave two reasons only: the submission was "unlikely
to meet one or both" of TMLR's criteria, and reviewer capacity was short. It
named no defect in the manuscript.

Two things followed.

1. **A venue had to be chosen.** The author wanted a credible journal where
   acceptance depends on soundness, not on perceived interest.
2. **The paper's files were hard to find.** ADR-0013 gave the paper lane its
   own working tree, `../xai-paper-bc`. The author works in
   `xai-eval-framework` and found the PeerJ files missing there, because they
   existed only in the other folder until merged.

## Decision

1. **Paper B+C targets PeerJ Computer Science**, as a Research Article
   (author decision, 2026-10-02). PeerJ reviews for soundness and explicitly
   not for novelty or impact.
2. **TMLR is deprecated as a venue and its artifacts are removed from the
   tree.** The filed version stays at tag `tmlr-submission-12779`. The
   rejection is recorded in `docs/reports/paper_bc/TMLR_REJECTION_RECORD.md`.
3. **There is one Paper B+C edition.** `paper_bc_peerjcs.tex` and
   `paper_bc_peerjcs_supplemental_S1.tex` replace the TMLR files at every
   wiring point: `pub/claims.toml` (`[papers.paper_bc]`), the claim registry,
   `[coverage]`, the regression guards, `verify_sync.py`,
   `scan_shared_literals.py`, the artifact bundle and the Makefile.
4. **The science is unchanged by the move.** Results, tables and figures were
   carried over verbatim. Text was added only where PeerJ requires it, and
   none of it carries a result: a structured abstract, a computing
   infrastructure paragraph, dataset DOIs, the EXP4 judge model identifiers in
   Methods, and an AI-use disclosure.
5. **Review is single-blind.** The anonymity switch (`\ifdeanon`) is gone and
   there is no anonymous build.
6. **AI use is disclosed as assistance under the author's direction.** The
   author guides the work and makes the planning, design and interpretation
   decisions. The disclosure lists every kind of assistance visible in the
   public repository history (language editing, programming support, checking
   numbers against artifacts), so that it cannot be read as an understatement.
7. **The separate paper working tree is retired.** `../xai-paper-bc` is
   removed, and the branches `paper/bc-venue-definition` and
   `paper/bc-peerj-cs` are deleted after merging into `main`. Paper B+C
   material lives in `docs/reports/paper_bc/` of the main folder.
8. **Paper edits still go through a branch and `main`.** A change to the paper
   is made on a short-lived `paper/bc-<topic>` branch in the main folder,
   verified, merged to `main`, and merged from `main` into the thesis lane in
   the same session. ADR-0013's other rules stand: lanes never merge into each
   other, the registry is edited on the branch that edits the manuscript, and
   the four verifiers pass before every merge.

## Consequences

**Positive**
- One folder holds all Paper B+C material, and nothing TMLR-specific remains
  to be mistaken for the current version.
- The claim registry keeps the counts of the filed version (321 claims, 485
  sites), which is the evidence that no number changed in the port.

**Negative**
- Switching to a `paper/bc-*` branch in the main folder changes the checked-out
  thesis files. ADR-0013 introduced the second working tree to avoid exactly
  this, because the thesis DOCX is often open in Word. Close Word before
  switching branches, or the switch fails on the file lock.
- PeerJ charges a fee after acceptance. The author has not decided how to
  pay; filing waits on that decision.

**Unchanged**
- ADR-0018 still holds: the CIFIE chapter prints no Paper B+C result while the
  paper is unpublished. PeerJ, like TMLR, does not accept material already
  published in a peer-reviewed journal.
- The `chapter/cifie-*` and `results/*` working trees are not affected.

## Disclosed while porting

Hardware was never recorded for any experiment run, and the host is recorded
only for runs launched through the work queue. The paper now says so, and
states the consequence: wall-clock cost includes between-host variance, and the
two members of a paired cell may have run on different hosts. The quality
endpoints do not depend on the host. Future experiments should record the host,
processor and memory in each run's metadata.

## Verification

`verify_claims.py`, `verify_sync.py`, `verify_exp4_reconstruction.py` and
`scan_shared_literals.py --strict` pass on `main` and on the thesis lane. Both
PDFs build in the main folder with no undefined reference.
