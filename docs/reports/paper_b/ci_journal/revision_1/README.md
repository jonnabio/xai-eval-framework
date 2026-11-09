# Paper B, revision 1 (Computers and Informatics, submission 2067810)

Major revision requested 2026-11-06, due 2026-11-30. Everything about the revision lives in
this folder. The submitted edition (`../paper_b_ci.tex`, `../submission/`) is **frozen**:
its hashes are in `SUBMITTED_SNAPSHOT.sha256`, and every build and check refuses to run if one
of them changed.

## Map

| Path | What |
|---|---|
| `DECISION_LETTER.md`, `REVIEWER1_DETAILED_REPORT.md` | The decision and the reports, verbatim |
| `REVIEW_ANALYSIS.md` | The 53 items (editor 3, reviewer 1: 41, reviewer 2: 9), each with verdict and work package; ED-2 and ED-3 need no answer (author, 2026-11-07), so the letter answers 51 |
| `REVISION_PLAN.md` | Decisions D-1 to D-7, work packages, schedule |
| `WP0_FINDINGS.md`, `provenance/` | Facts from the code and the EXP2 audit (F1–F9; incident F7, F8) |
| `RUNS_IMPLEMENTATION_PLAN.md`, `RUNBOOK.md`, `env/` | Cohort B2: how it runs, how to operate it, the host |
| `manuscript/paper_b_ci_rev1.tex`, `abstract_rev1.tex`, `keywords_rev1.tex` | **The revised manuscript** (working copy), its abstract and keywords |
| `CHANGELOG.md` | **Every change**, numbered C-###, with the items it answers, recorded in the commit that makes it |
| `RESPONSE_TO_REVIEWERS.md` | **The answer to every item**: REMEDIATED (with its changes and location) or EXPLAINED |
| `PROPOSAL_2026-11-06.md` | The approved proposal (D-E); Part E maps each P-change to its C-change and records later corrections |
| `REFERENCE_AUDIT.md` | Every reference verified (DOI, metadata); the 80% rule, option A |
| `CONSISTENCY_2026-11-07.md` | Manuscript, ledger, response and proposal checked against each other; every open item and what it waits for |
| `HANDOFF.md` | Messages between the documentation laptop and the experiment laptop |
| `results/` | The analysis of cohort B2 behind the values printed (`results/README.md`: source snapshot, scope) |
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
| `supplement/paper_b_ci_rev1_supplement.docx` / `.pdf` / `.md` | The supplementary file for the reviewers (D-B), independent of the paper: design, data, models, fingerprints, environment; result sections [R] until the analysis fills them. Rendered by `scripts/build_supplement.py` |
| `drafts/paper_b_ci_rev1_response_DRAFT.docx` / `.pdf` | **Historical** (the proposal of 2026-11-06, approved; superseded by the letter and the ledger): every comment with its elaborated draft answer (PROPOSAL Part C) and the P-changes that implement it. Rendered by `scripts/build_drafts.py` |
| `drafts/paper_b_ci_rev1_proposed_changes_DRAFT.docx` / `.pdf` | **Historical**, as above: length plan, changes P-01..P-24, decisions D-A..D-E (PROPOSAL Parts A, B, D) |

The comparison baseline is the submitted source rebuilt with the same pipeline; the build
verifies that its text equals the submitted `.docx` before comparing, so only real edits are
marked (the submitted `.docx` carries invisible zero-width spaces from its own Word pass).

## Commands (from the repository root)

```bash
.venv/Scripts/python.exe docs/reports/paper_b/ci_journal/revision_1/scripts/check_revision.py
.venv/Scripts/python.exe docs/reports/paper_b/ci_journal/revision_1/scripts/build_revision.py   # needs Word
.venv/Scripts/python.exe docs/reports/paper_b/ci_journal/revision_1/scripts/check_revision.py --final   # before upload
```

## Supplementary file (D-B)

`build/supplement/paper_b_ci_rev1_supplement.docx` and `.pdf`, built by
`scripts/build_supplement.py` (S1–S6 from the design and the frozen models; S7–S13 from
`results/`, by `scripts/supplement_results.py`). Needs the prepared datasets
(`paper_b_run.py prepare`) and the analysis packages. After a new analysis:

```bash
python scripts/paper_b_analyze.py --root <runs>/results --out <analysis>
python docs/reports/paper_b/ci_journal/revision_1/scripts/build_supplement.py     --analysis docs/reports/paper_b/ci_journal/revision_1/results     --rows <analysis>/rows.csv --timing-root <runs>/results
```

(copy the analysis CSVs into `results/` first; `rows.csv` is not committed).

## Mandatory before submission

1. **Length review (author, 2026-11-08).** The manuscript is 13 pages after C-042 and
   14 after C-048 (validity controls). The author decides on the length once every result is in;
   do not trim before then, and do not submit before this review is done.
2. Every [R] marker filled; `check_revision.py --final` passes.
3. Abstract within 150-200 words after the last fill.

## Rule for every edit

1. Edit `manuscript/paper_b_ci_rev1.tex` (or the revision's abstract fragment).
2. Add a row to `CHANGELOG.md` (next C-### ID, the items, where, what).
3. Update the items' entries in `RESPONSE_TO_REVIEWERS.md` (status, change IDs, response, where).
4. Run `check_revision.py`, then `build_revision.py`; commit everything together, then push.

Journal templates (`../journal_files/`, git-ignored) are re-downloaded from the URLs in
`../CI_SUBMISSION.md` §2 when missing.
