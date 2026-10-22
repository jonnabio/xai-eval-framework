# Active Context: XAI Evaluation Framework

> **This file holds the current state only. History is in the archive:
> [`docs/context/archive/README.md`](archive/README.md)** (index, one file per day).
> Read the archive when the task needs more than this file gives; when and how is
> rule CTX-3 of [`.ace/standards/context.md`](../../.ace/standards/context.md).
> Limit: 300 lines, checked in CI by `scripts/pubs/check_active_context.py`.

**Last updated:** 2026-10-21, by `claude-2026-10-21-session`.

## Current objective

**Close the thesis.** The tutor's note of 2026-10-12 asks for no change. On the author's
instruction of the same day, every paper is now reflected in the thesis (ADR-0023): a
new Chapter 6, `thesis/estudios-de-seguimiento.qmd`, reports the three later studies
(D, E, F) and the later controls of the inter-judge study (C); the conclusions render
as Chapter 7. No objective, hypothesis or proposition changed. Plan:
`docs/planning/thesis_followup_studies_plan_2026-10-12.md`. Record for the tutor, in
Spanish: `docs/review/tesis_cambios_para_tutor_2026-10-12.md` and `.docx`.

Since 2026-10-13 the thesis has **29 figures, 45 tables and 19 equations**, each
numbered and cited in the text (`scripts/pubs/check_equations.py`, in CI). What was
added and why: `docs/review/thesis-figure-review_2026-10-13.md`.

**Decided (2026-10-12), by the author and agreed by the tutor (reported by the author):**
a chapter of its own, no new objective, the three study names, the present length. The
record states them as agreed.

Standing task **Task 3 / RCA-001 Phase 2**:

1. Coverage sweep of the thesis: **done 2026-10-12**; every thesis source is under
   `[coverage]`. Not swept: Paper A (published; its file is not under coverage).
2. Not started: emit the registry values as LaTeX macros and Quarto inline values, and
   a CI job that builds every output and fails on undefined references and crossref
   warnings. Detail: archive `2026-09-04.md`, `2026-09-06.md`.

**Rules of the follow-up chapter** (ADR-0023):

- It prints only values registered for the papers. To print another one, add its claim
  id to `pub/thesis_followup_claims.toml` and run
  `python scripts/pubs/register_thesis_followup.py`; CI runs `--check`.
- If a paper is revised and a value changes, that check fails until the chapter prints
  the new value.
- `capitulo-6-conclusiones.qmd` keeps its file name although it renders as Chapter 7.
- New row 15 and 16 of `docs/review/top-level-statement-sweep.md` guard the status of
  the follow-up studies and the table of what they add.

## Publication status

| Paper | Venue | Status | Record |
|---|---|---|---|
| **A** | *Revista de Investigación Multidisciplinaria Iberoamericana* (RIMI) | Published | 2026; DOI [10.69850/rimi.vi3.307](https://doi.org/10.69850/rimi.vi3.307) |
| **B** | *Computers and Informatics* (C&I, DergiPark) | **Submitted 2026-10-21** | Number not recorded. Masked Word edition `docs/reports/paper_b/ci_journal/` (14 pages; intihal.net similarity 1%). Withdrawn from *CLEI Electronic Journal* (submission 1196 of 2026-10-04) by the author for its queue; withdrawal confirmed by the editor. Record: `ci_journal/CI_SUBMISSION.md`, `CLEIEJ_SUBMISSION.md` |
| **C** | *Tecnología en Marcha*, AI special issue | Submitted | 2026-10-06 (reported by the author); number not recorded. Fourth draft. Zenodo 0.12.0, [10.5281/zenodo.23165763](https://doi.org/10.5281/zenodo.23165763) |
| **D** | *Tecnología en Marcha*, AI special issue | Submitted | Through the author account, reported 2026-10-06; date and number not recorded. Zenodo 0.5.0, [10.5281/zenodo.23130014](https://doi.org/10.5281/zenodo.23130014) |
| **E** | *Computación y Sistemas* | Under review | Submitted 2026-10-04; submission 6783. Zenodo 0.8.0 |
| **F** | *Journal of Computer Sciences Institute* | **Revision submitted 2026-10-19** for Reviewer A (minor revisions required); awaiting the editor | Submitted 2026-10-12; submission 10503; 8 pages. Format corrections sent to the editor 2026-10-13. Zenodo 0.15.0, [10.5281/zenodo.23325483](https://doi.org/10.5281/zenodo.23325483). Target issue: 30 March 2027. Review and what was done: `docs/reports/paper_f/README.md`, section 9 |

- **No submitted paper is rebuilt, edited or re-analysed unless its journal asks for a
  revision.** Record every decision of a journal in this table and in the paper's README.
- The combined Paper B+C was desk-rejected by TMLR (2026-10-02) and by *Inteligencia
  Artificial* (2026-10-04), then split into B and C (ADR-0022). It is not a current
  submission.
- **CIFIE/FOM-7 chapter:** a package was sent for first editorial revision on
  2026-10-10. The chapter text is `392b2fc8c` (11 sections, 8,772 words); the package
  sent was built from an earlier text and prints numbers no registered claim backs. The
  package is to be rebuilt from `392b2fc8c` in the chapter lane (`../xai-chapter`,
  `chapter/cifie-*`). Limit 9,000 words. Detail: archive `2026-10-10.md`.
- Revision routes, known limits of each submitted paper and the Zenodo release route:
  the paper's README and archive `2026-10-12.md` (Paper F), `2026-10-05.md` (C),
  `2026-10-04.md` (B, E), `2026-10-03.md` (D).

## Repository state

- Main folder `xai-eval-framework`: thesis lane. Other folders: `../xai-exp4`
  (`results/exp4-cohort2`), `../xai-eval-framework-main-status` (`main`, read only).
  Lanes and the paths they own: `scripts/pubs/lanes.toml`.
- `main` holds everything up to pull requests #66 (registry: Paper B C&I edition) and
  #67 (Paper B C&I edition), merged 2026-10-21, and this handoff. `paper/b-computers-informatics`
  and `paper/f-external-validity` hold nothing that is not on `main`; `thesis/rca-001-phase-2`
  is behind `main` and takes `main` when the thesis lane resumes. No pull request is open.
- The lane lock of the main folder is free.
- Nothing is running: no task, no process.
- Verifiers at the last check (2026-10-21): `verify_claims.py` 1,391 claims, 1,808
  sites, 39 files fully registered; `verify_sync.py`, `verify_exp4_reconstruction.py`,
  `scan_shared_literals.py --strict`, `check_equations.py` and `check_active_context.py`
  pass; `pytest tests/pubs` 47 passed.
- The thesis renders to Word with seven chapters and no unresolved reference
  (`thesis/render.ps1`; `thesis/_output/JHerrera_XAI_Tesis_Doctorado.docx` is tracked).

## Open with the author

0. **Paper F:** revision for Reviewer A submitted 2026-10-19; wait for the editor.
1. Submission numbers of Papers B (C&I), C and D, and the date of Paper D's submission.
2. The final text of Paper F's comments to the editor (not shown to the session).
3. CIFIE: whether a corrected file goes to the editor after the package is rebuilt.
4. **The publication licence of the book chapter**: whether it allows the ten figures
   the thesis now shares with it (`fig_d1` to `fig_d4`, `fig_d6` to `fig_d11`). Not
   confirmed by the author; to check before deposit.
5. Branch protection on `main` (pull request and the checks required): agreed on
   2026-10-10, set by the author on GitHub; not confirmed as done.
6. **Before deposit:** the prior-publication policy of each journal with a paper under
   review (B at C&I, C, D, E, F), since the thesis now carries their results. Paper F's
   comments to the editor state that the thesis is not deposited.
7. The table of contents is refreshed by the author in Word after every render.

## Active constraints

The full list as it stood, with the reason for each: archive `undated-state-sections.md`
("Active Constraints"). The ones that bind current work:

- **Lanes (ADR-0013, ADR-0021).** Claim before any edit; `main` is never worked on
  directly. A commit never mixes a lane's paths with shared paths (`pub/`,
  `scripts/pubs/`, `docs/rca/`, `docs/context/`, `docs/review/`, `.zenodo.json`,
  `CITATION.cff`, `pubs-sync.yml`). Shared commits go on a `pubs/*` branch and reach
  `main` in the session they are made; lanes then take `main`. Lanes never merge into
  each other.
- **Guards.** RCA-001, RCA-002 and RCA-003 in `docs/rca/regression-guards.yaml`. Any edit
  to a numeric result: `verify_claims.py`, `verify_sync.py`,
  `verify_exp4_reconstruction.py`. Any rescoped claim in a chapter:
  `docs/review/top-level-statement-sweep.md`.
- **Coverage is a trunk event.** Adding a file to `[coverage]` turns CI red on every
  lane: triage it on a `pubs/*` branch and merge before any lane takes it.
- **Registry.** A number that needs arithmetic over registered values uses the
  `diff:<exprA>|<exprB>` resolver, not `[[unbacked]]`. `pub/claim_registry.toml` is
  CRLF: after a programmatic edit, check for `\r\r\n` and re-parse.
  `pub/fragments/` is generated: never edit or hand-merge it, run
  `scripts/pubs/generate_fragments.py`.
- **Thesis text.** Spanish prose; reports, commits and interaction in English. Study
  names are functional, never letters, and the thesis names no paper (ADR-0012); the
  anchors `#sec-estudio-a`, `#sec-estudio-b`, `#sec-exp4-fiabilidad` are frozen. The
  aggregation level is stated wherever a number could be read at more than one.
- **Thesis title, Resumen and Abstract** are authored in `pub/claims.toml`; the two
  languages mirror each other paragraph for paragraph; any figure they cite is
  registered first.
- **Thesis build.** `thesis/render.ps1`; close the Word file first. Presentation is
  applied after the render by `scripts/enforce_docx_thesis_format.py` (CRLF file) from
  `thesis/cover.txt` and the `.qmd` sources: never type section numbers into headings,
  never hand-format Dedicatoria or Agradecimientos, keep `number-sections: true`. Check
  layout claims in `word/document.xml`, not by a green render. The author refreshes
  the table of contents in Word after every render.
- **Single-author papers** are written impersonally; references carry a verified DOI
  URL and at least 80% date from 2024 or later (`.aceconfig`).
- **Permissions.** Pushing or merging `main` may be refused to the assistant: try once,
  then give the author the exact command.
- **Other reviewers (Codex) work in the same folder.** Read `git status` after a claim
  and do not touch files another session left uncommitted without the author's word.

## Latest handoff - 2026-10-21, SESSION END (Paper B withdrawn from CLEIEJ, submitted to C&I)

Session of 2026-10-21, lane `paper-b` (branch `paper/b-computers-informatics`, owner
`claude-2026-10-21-session`); shared files on `pubs/paper-b-ci-registry` and
`pubs/context-2026-10-21`.

- **Completed**:
  - Author decision: Paper B withdrawn from CLEIEJ (submission 1196, long queue); the editor
    confirmed the withdrawal. Recorded in `docs/reports/paper_b/CLEIEJ_SUBMISSION.md`; the
    CLEIEJ files are unchanged.
  - Journal rules of *Computers and Informatics* reviewed (guidelines, template, forms, price
    and ethics pages, two articles of Vol. 6 No. 1) and tabulated in
    `docs/reports/paper_b/ci_journal/CI_SUBMISSION.md`.
  - New edition `ci_journal/paper_b_ci.tex`: CLEIEJ text changed in form only (masked, Eq. (n)
    citations, competing-interests section, Vancouver references, same 38 entries and links).
  - `ci_journal/scripts/build_paper_b_ci_docx.py` writes the masked manuscript (14 pages),
    title page and cover letter into the journal's Word templates; fails on author data in the
    manuscript.
  - Registry: the edition mirrors every CLEIEJ registration (84 sites), is under `[coverage]`
    and in `scan_shared_literals.py` (PR #66). Lane work PR #67. Both merged.
  - intihal.net similarity report: 1% overall, every source under 1%.
  - Author's answers recorded: reference list kept as in CLEIEJ (author decision, not to be
    reopened for this paper); cover letter approved; optional fields and note to the editor
    advised; Paper B **submitted 2026-10-21**.
- **Current State**:
  - Paper B under submission at C&I; no number recorded. Files sent are in
    `ci_journal/submission/`. The intihal report PDF and the signed cover letter there are
    the author's, left untracked (signature; public repository).
  - Nothing running; lane lock released; no pull request open.
- **Next Steps**:
  1. `python scripts/pubs/check_lane.py claim --owner <session name>` for the task's lane;
     stop if it fails.
  2. Record the C&I submission number (and confirm the date) in `CI_SUBMISSION.md` and the
     table above.
  3. Paper F: when the JCSI editor answers, record the decision; change only what is asked.
  4. Thesis lane: take `main` into `thesis/rca-001-phase-2`; items of "Open with the author".
- **Blockers/Issues**:
  - None blocking. Pending with the author: items 1 to 7 of "Open with the author".
  - Paper B's references do not meet the 2024+ rule (7 of 38); accepted by the author for
    this paper only.
  - `tests/analysis/test_stats.py` and `test_visualization.py` fail at collection; not
    investigated.
- **Notes**:
  - C&I builds: `.venv\Scripts\python.exe docs/reports/paper_b/ci_journal/scripts/build_paper_b_ci_docx.py`
    (needs Quarto; Word for the PDFs). The journal's files are in `ci_journal/journal_files/`
    (ignored; download addresses in `CI_SUBMISSION.md`).
  - C&I's similarity report is made by the submission system (intihal.net) from the
    full-text upload of step 3; limits 20% overall, 3% per source.
  - `gh pr merge` worked for the assistant this session.
