# Active Context: XAI Evaluation Framework

> **This file holds the current state only. History is in the archive:
> [`docs/context/archive/README.md`](archive/README.md)** (index, one file per day).
> Read the archive when the task needs more than this file gives; when and how is
> rule CTX-3 of [`.ace/standards/context.md`](../../.ace/standards/context.md).
> Limit: 300 lines, checked in CI by `scripts/pubs/check_active_context.py`.

**Last updated:** 2026-10-12, by session `claude-2026-10-12-thesis-review`.

## Current objective

**Close the thesis.** The tutor's note of 2026-10-12 asks for no change. On the author's
instruction of the same day, every paper is now reflected in the thesis (ADR-0023): a
new Chapter 6, `thesis/estudios-de-seguimiento.qmd`, reports the three later studies
(D, E, F) and the later controls of the inter-judge study (C); the conclusions render
as Chapter 7. No objective, hypothesis or proposition changed. Plan:
`docs/planning/thesis_followup_studies_plan_2026-10-12.md`. Record for the tutor, in
Spanish: `docs/review/tesis_cambios_para_tutor_2026-10-12.md` and `.docx`.

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
| **B** | *CLEI Electronic Journal* | Under review | Submitted 2026-10-04; submission 1196; 12 pages |
| **C** | *Tecnología en Marcha*, AI special issue | Submitted | 2026-10-06 (reported by the author); number not recorded. Fourth draft. Zenodo 0.12.0, [10.5281/zenodo.23165763](https://doi.org/10.5281/zenodo.23165763) |
| **D** | *Tecnología en Marcha*, AI special issue | Submitted | Through the author account, reported 2026-10-06; date and number not recorded. Zenodo 0.5.0, [10.5281/zenodo.23130014](https://doi.org/10.5281/zenodo.23130014) |
| **E** | *Computación y Sistemas* | Under review | Submitted 2026-10-04; submission 6783. Zenodo 0.8.0 |
| **F** | *Journal of Computer Sciences Institute* | Under review | Submitted 2026-10-12; submission 10503; 8 pages. Zenodo 0.15.0, [10.5281/zenodo.23325483](https://doi.org/10.5281/zenodo.23325483). Target issue: 30 March 2027 |

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
- `main` at `1062a1dd9` (pull request #57, the follow-up chapter), merged by the author
  on 2026-10-12. The thesis branch is level with it, plus the record of the tutor's
  agreement in a further pull request.
- Nothing is running: no task, no process.
- Verifiers at the last check (2026-10-12): `verify_claims.py` 1,387 claims, 1,728
  sites, 38 files fully registered; `verify_sync.py`, `verify_exp4_reconstruction.py`,
  `register_thesis_followup.py --check`, `register_paper_c.py --check` and
  `register_paper_f.py --check` pass.
- The thesis renders to Word with seven chapters and no unresolved reference
  (`thesis/render.ps1`; `thesis/_output/JHerrera_XAI_Tesis_Doctorado.docx` is tracked).

## Open with the author

1. Submission numbers of Papers C and D, and the date of Paper D's submission.
2. The final text of Paper F's comments to the editor (not shown to the session).
3. CIFIE: whether a corrected file goes to the editor after the package is rebuilt.
4. Thesis figures: **closed 2026-10-12.** Commit `ba418a927` had replaced three Chapter 4
   figures with the black-and-white print versions of the book chapter; the colour
   files are restored and the generator no longer writes the B/W pass to the thesis.
5. Branch protection on `main` (pull request and the checks required): agreed on
   2026-10-10, set by the author on GitHub; not confirmed as done.
6. **Before deposit:** the prior-publication policy of each journal with a paper under
   review (B, C, D, E, F), since the thesis now carries their results. Paper F's
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

## Latest handoff - 2026-10-13 (thesis figures and tables: 29 figures, all cited)

- **Completed** (lane `thesis`, owner `claude-2026-10-12-thesis-review`):
  - Pull requests #57 and #58 merged by the author on 2026-10-12. Detail: archive
    `2026-10-12.md`.
  - **Chapter 6:** five Spanish figures from the result files of each study
    (`scripts/generate_thesis_followup_figures.py`), plus the sequence of the evidence.
  - **Chapter 4:** stability against cost as median and interquartile range; cost by
    model family; every figure cited.
  - **Chapters 1, 2, 3, 5 and 7**, which had no figure: map of the thesis; eight concept
    figures and two FOM-7 figures shared with the book chapter (`d1`, `d2`, `d3`, `d4`,
    `d6`, `d7`, `d8`, `d9`, `d10`, `d11`; not `d5`, not `d12`); units of analysis;
    taxonomy axes; judge reliability in both cohorts; selection guide. Generator:
    `scripts/generate_thesis_extra_figures.py`. The arrow chain that was Equation 3.9
    is replaced by the FOM-7 figure, so the thesis has 19 equations.
  - **Tables:** the 18 never cited now are; one table of Chapter 2 gained its caption and
    number (`tbl-metodos-constructos`).
  - **Check:** `scripts/pubs/check_equations.py` enforces number and citation for
    equations, figures and tables (19, 29 and 45). Rule in
    `.ace/standards/documentation.md` ("Manuscripts: Figures and Tables") and `.aceconfig`.
  - **English figures kept** for presentations (author's decision), now produced from
    the Spanish generator by `scripts/generate_thesis_supplementary_figures_en.py`.
  - Record for the tutor updated; review and what was done:
    `docs/review/thesis-figure-review_2026-10-13.md`. Thesis rendered: 29 figures, no
    unresolved reference.
- **Rules for thesis figures:**
  - Method colours: SHAP `#c0392b`, LIME `#1b6ca8`, Anchors `#2e8b57`, DiCE `#6c3483`.
  - A figure prints nothing its generator does not compute from a result file; a
    schematic says that it is one.
  - `generate_spanish_thesis_figures.py` and the two `generate_cifie_*_figures.py` also
    write the book-chapter folders (chapter lane): from the thesis lane run them with
    those outputs redirected, as `generate_thesis_extra_figures.py` does.
- **Changed in a shared script, to know in the chapter lane:**
  `generate_cifie_equation_figures.py` no longer prints 97.4% and 22.5% in `d11` (values
  without a source); the chapter's committed images are older than the scripts and
  change at its next rebuild.
- **Open with the author:**
  1. The publication licence of the book chapter, for the ten shared figures, before
     deposit.
  2. Read the new figures and their captions; the Spanish text is the assistant's.
- **Next steps**: merge the pull request; then the items that stand from before (send
  the record and the thesis to the tutor, table of contents in Word, journals'
  prior-publication policies).
- **Blockers**: none.
