# Change ledger: Paper B, revision 1 (C&I 2067810)

Every change to the revised manuscript (`manuscript/paper_b_ci_rev1.tex`), to its abstract or
keywords, its figures, tables or data is recorded here **in the same commit that makes it**.
`scripts/check_revision.py` reads this table:

- every change names the reviewer items it answers (IDs of `REVIEW_ANALYSIS.md`), or `none`
  for a change no reviewer asked for (a correction found by the author, such as F1);
- every REMEDIATED item of `RESPONSE_TO_REVIEWERS.md` points to at least one change here.

The marked-up comparison with the submitted text, every insertion and deletion, is rebuilt
with each build: `build/paper_b_ci_rev1_changes_marked.pdf` (latexdiff against the frozen
`../paper_b_ci.tex`, whose hash is in `SUBMITTED_SNAPSHOT.sha256`).

Columns: **ID** (C-###, never reused) · **Date** · **Items** · **Where** (section, table,
figure, file) · **Change** (what and why, one sentence) · **Commit** (filled after the commit).

| ID | Date | Items | Where | Change | Commit |
|---|---|---|---|---|---|
| C-000 | 2026-11-06 | none | `manuscript/paper_b_ci_rev1.tex` | Working copy created from the submitted source (body byte-identical; provenance header added). The submitted files are frozen | — |
