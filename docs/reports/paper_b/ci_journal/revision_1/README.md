# Paper B, revision 1 (Computers and Informatics, submission 2067810)

Major revision requested 2026-11-06, due 2026-11-30. Everything about the revision lives in
this folder. The submitted edition (`../paper_b_ci.tex`, `../submission/`) is **frozen**:
its hashes are in `SUBMITTED_SNAPSHOT.sha256`, and every build and check refuses to run if one
of them changed.

## Map

| Path | What |
|---|---|
| `DECISION_LETTER.md`, `REVIEWER1_DETAILED_REPORT.md` | The decision and the reports, verbatim |
| `REVIEW_ANALYSIS.md` | The 53 items (editor 3, reviewer 1: 41, reviewer 2: 9), each with verdict and work package |
| `REVISION_PLAN.md` | Decisions D-1 to D-7, work packages, schedule |
| `WP0_FINDINGS.md`, `provenance/` | Facts from the code and the EXP2 audit (F1–F9; incident F7, F8) |
| `RUNS_IMPLEMENTATION_PLAN.md`, `RUNBOOK.md`, `env/` | Cohort B2: how it runs, how to operate it, the host |
| `manuscript/paper_b_ci_rev1.tex` | **The revised manuscript** (working copy; the only file edited) |
| `CHANGELOG.md` | **Every change**, numbered C-###, with the items it answers, recorded in the commit that makes it |
| `RESPONSE_TO_REVIEWERS.md` | **The answer to every item**: REMEDIATED (with its changes and location) or EXPLAINED |
| `scripts/check_revision.py` | Checks frozen files, completeness of the answers, ledger consistency (`--final` before submission) |
| `scripts/build_revision.py` | Renders everything into `build/` |
| `build/` | **The new PDFs**, apart from the submitted ones |

## Build outputs (`build/`)

| File | What |
|---|---|
| `paper_b_ci_rev1_manuscript.docx` / `.pdf` | The revised manuscript in the journal's Word template, masked: the file to upload |
| `paper_b_ci_rev1_changes_marked.docx` / `.pdf` | Every insertion and deletion against the submitted manuscript (Word's comparison; tracked changes by "Author", masked) |
| `paper_b_ci_rev1_response.docx` / `.pdf` | The response letter (internal tracking lines removed) |
| `paper_b_ci_rev1_preview.pdf` | LaTeX rendering of the revised source |
| `BUILD_MANIFEST.md` | Date, commit, hashes, pages, tracking status of the last build |

The comparison baseline is the submitted source rebuilt with the same pipeline; the build
verifies that its text equals the submitted `.docx` before comparing, so only real edits are
marked (the submitted `.docx` carries invisible zero-width spaces from its own Word pass).

## Commands (from the repository root)

```bash
.venv/Scripts/python.exe docs/reports/paper_b/ci_journal/revision_1/scripts/check_revision.py
.venv/Scripts/python.exe docs/reports/paper_b/ci_journal/revision_1/scripts/build_revision.py   # needs Word
.venv/Scripts/python.exe docs/reports/paper_b/ci_journal/revision_1/scripts/check_revision.py --final   # before upload
```

## Rule for every edit

1. Edit `manuscript/paper_b_ci_rev1.tex` (or the revision's abstract fragment).
2. Add a row to `CHANGELOG.md` (next C-### ID, the items, where, what).
3. Update the items' entries in `RESPONSE_TO_REVIEWERS.md` (status, change IDs, response, where).
4. Run `check_revision.py`, then `build_revision.py`; commit everything together, then push.

Journal templates (`../journal_files/`, git-ignored) are re-downloaded from the URLs in
`../CI_SUBMISSION.md` §2 when missing.
