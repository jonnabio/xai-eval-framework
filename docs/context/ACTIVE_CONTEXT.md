# Active Context: XAI Evaluation Framework

> **This file holds the current state only. History is in the archive:
> [`docs/context/archive/README.md`](archive/README.md)** (index, one file per day).
> Read the archive when the task needs more than this file gives; when and how is
> rule CTX-3 of [`.ace/standards/context.md`](../../.ace/standards/context.md).
> Limit: 300 lines, checked in CI by `scripts/pubs/check_active_context.py`.

**Last updated:** 2026-10-22, by `claude-2026-10-21-paper-e`.

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

| Paper | Title | Venue | Status | Record |
|---|---|---|---|---|
| **A** | *A framework for rigorous evaluation of model-agnostic explainability methods: multi-metric statistical benchmarking, operational protocol, and reproducibility* | *Revista de Investigación Multidisciplinaria Iberoamericana* (RIMI) | Published | 2026; DOI [10.69850/rimi.vi3.307](https://doi.org/10.69850/rimi.vi3.307) |
| **B** | *When Does SHAP Outperform LIME? Model- and Configuration-Dependent Results from a Paired Tabular Benchmark* | *Computers and Informatics* (C&I, DergiPark) | **Submitted 2026-10-21** | Number not recorded. Masked Word edition `docs/reports/paper_b/ci_journal/` (14 pages; intihal.net similarity 1%). Withdrawn from *CLEI Electronic Journal* (submission 1196 of 2026-10-04) by the author for its queue; withdrawal confirmed by the editor. Record: `ci_journal/CI_SUBMISSION.md`, `CLEIEJ_SUBMISSION.md` |
| **C** | *Do LLM Judges Agree on the Quality of Explanations? A Two-Panel Reliability Study* | *Tecnología en Marcha*, AI special issue | Submitted | 2026-10-06 (reported by the author); number not recorded. Fourth draft. Zenodo 0.12.0, [10.5281/zenodo.23165763](https://doi.org/10.5281/zenodo.23165763) |
| **D** | *Are explanations less reliable when the model is wrong? Post-hoc explanation quality on misclassified instances* | *Tecnología en Marcha*, AI special issue | **Submitted 2026-10-03** | Through the author account (date given by the author on 2026-10-22); number not recorded. Zenodo 0.5.0, [10.5281/zenodo.23130014](https://doi.org/10.5281/zenodo.23130014) |
| **E** | *Do Explainers Agree on Which Features Matter? Instance-Level Agreement between SHAP and LIME* | *Advances in Artificial Intelligence Research* (AAIR, DergiPark) | **Submitted 2026-10-22** | Number not recorded. Word edition `docs/reports/paper_e/aair_journal/` (14 pages; intihal.net similarity 1%). Withdrawn from *Computación y Sistemas* (submission 6783 of 2026-10-04) by the author for its queue; withdrawal confirmed by the editor. Record: `aair_journal/AAIR_SUBMISSION.md`. Zenodo 0.8.0, [10.5281/zenodo.23142429](https://doi.org/10.5281/zenodo.23142429) |
| **F** | *How Dataset-Dependent Are Tabular Explainability Benchmarks?* | *Journal of Computer Sciences Institute* | **Revision submitted 2026-10-19** for Reviewer A (minor revisions required); awaiting the editor | Submitted 2026-10-12; submission 10503; 8 pages. Format corrections sent to the editor 2026-10-13. Zenodo 0.15.0, [10.5281/zenodo.23325483](https://doi.org/10.5281/zenodo.23325483). Target issue: 30 March 2027. Review and what was done: `docs/reports/paper_f/README.md`, section 9 |

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
- `main` holds everything up to pull requests #69 (Paper E AAIR edition, lane) and #70
  (its registry and this handoff), merged 2026-10-22 in that order.
  `paper/b-computers-informatics` and `paper/f-external-validity` hold nothing that is not
  on `main`; `thesis/rca-001-phase-2` is behind `main` and takes `main` when the thesis
  lane resumes.
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
0. **Paper E (AAIR):** submitted 2026-10-22; record the submission number. Merge #69,
   then #70.
1. Submission numbers of Papers B (C&I), C, D and E (AAIR).
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

## Latest handoff - 2026-10-22, SESSION END (Paper E withdrawn from CyS; submitted to AAIR)

Session of 2026-10-21/22, lane `paper-e` (branch `paper/e-aair`, owners
`claude-2026-10-21-paper-e` and `claude-2026-10-22-paper-e`); shared files on
`pubs/paper-e-aair-registry`.

- **Completed**:
  - Paper E withdrawn from *Computación y Sistemas* (submission 6783; review would not start
    for over a year; editor confirmed). Recorded in `docs/reports/paper_e/README.md`; the
    CyS edition is unchanged and kept as evidence.
  - AAIR (*Advances in Artificial Intelligence Research*, DergiPark, no fee) chosen by the
    author. Guidelines analysed; plan approved: `docs/planning/paper_e_aair_plan_2026-10-21.md`.
    The writing-rules page and the template file disagree; the author chose the template
    (Option T) with the page's limits.
  - Author decisions for Paper E: 2024+ reference rule waived (future papers keep it);
    Turkish title by translation, the author does not speak Turkish; Zenodo 0.8.0 kept
    (citation sound, no new release); no blind version (the journal asks for none).
  - AAIR edition in `docs/reports/paper_e/aair_journal/`: source `paper_e_aair_template.tex`,
    builder `scripts/build_paper_e_aair_docx.py`, manuscript .docx (14 pages, 10 floats,
    25 references, abstract 249 words), cover letter, copyright form; record
    `AAIR_SUBMISSION.md`.
  - Registry: generated `paper_e_aair` block (507 claims); `paper_e_aair.tex` under
    `[coverage]` and `[exclusivity]`. All verifiers, registration checks and `tests/pubs`
    (47) passed on a clean tree.
  - Similarity report (intihal.net) read: 1%, nine unrelated sources each under 1%.
  - Form texts drafted: ethical statement, supporting institution, thanks, note to editor.
  - **Paper E submitted to AAIR on 2026-10-22** (author); cover letter as sent committed.
  - Paper D submission date confirmed by the author: 2026-10-03.
  - Publication table now carries each paper's title.
- **Current State**:
  - Papers B, C, D, E submitted; F revision submitted; A published. No submission numbers
    for B (C&I), C, D, E (AAIR).
  - PRs #69 (lane) and #70 (registry, context) merged at session end, #69 first (if a merge
    was refused, the commands are in Next Steps).
  - Nothing running; lane lock released.
- **Next Steps**:
  1. `python scripts/pubs/check_lane.py claim --owner <session name>`; stop if it fails.
  2. If #69 or #70 is still open: `gh pr merge 69 --squash`, then `gh pr merge 70 --merge`.
  3. Record submission numbers (B, C, D, E) when the author gives them.
  4. Paper F: record the JCSI editor's decision when it arrives.
  5. Thesis lane: take `main` into `thesis/rca-001-phase-2`; items of "Open with the author".
- **Blockers/Issues**:
  - Uncommitted moves of Paper B's CLEIEJ files into `docs/reports/paper_b/CLEIEJ_DEPRECATED/`
    are in the main folder (another session or the author); left untouched. Until they are
    committed with the registry paths updated, `verify_claims.py` fails in that folder
    (83 "file not found" for `paper_b_cleiej.tex`). Needs the author's decision.
  - The AAIR cover letter as sent omits the CyS withdrawal paragraph; the withdrawal is
    disclosed only if the author kept it in the note to the editor.
  - `tests/analysis/test_stats.py` and `test_visualization.py` fail at collection; not
    investigated.
- **Notes**:
  - AAIR build: `.venv\Scripts\python.exe docs/reports/paper_e/aair_journal/scripts/build_paper_e_aair_docx.py`
    (Quarto and Word; journal files in `aair_journal/journal_files/`, ignored). Close the
    .docx files in Word first. Then `register_paper_c.py --check`: the Paper C block must
    stay last in the registry, so the AAIR block sits after the CyS Paper E block.
  - Word waits on a dialog when it updates the copyright form's web-linked logo field; the
    builder does not update fields there.
  - Signed forms and similarity reports stay untracked (public repository).
  - `check_lane.py --staged` needs a claim even for commits of shared files.
