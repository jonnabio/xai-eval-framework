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

## Latest handoff - 2026-10-12 (every paper reflected in the thesis; open points closed)

- **Completed** (lane `thesis`, owner `claude-2026-10-12-thesis-review`):
  - Context file split and its standard (pull request #56, merged by the author).
  - Plan and ADR-0023. New Chapter 6 with the three follow-up studies and the later
    inter-judge controls; pointers and renumbering in the other chapters; Appendix G;
    one mirrored sentence in the Resumen and Abstract.
  - `scripts/pubs/register_thesis_followup.py`: 79 paper claims mirrored for the
    chapter; CI step added.
  - Two scope statements added to Chapters 3 and 5 from the later review of the judge
    prompts: the primary condition of cohort 2 did not hide the label effectively, and
    Anchors and DiCE were scored in a rendering that is not their own.
  - The three points open before deposit: figures restored; coverage sweep finished
    (ten literals in the appendices, a typed table number fixed, a probe without
    artifact now disclosed); final pass done (statement sweep rows 1 to 16, ADR-0012
    greps, full render read from `word/document.xml`).
  - Record for the tutor written, with a Word copy.
  - **Equations (author rule, 2026-10-12):** the 20 displayed equations of the thesis
    (17 in Chapter 3, 3 in Chapter 4) are labelled and each is cited in the text;
    numbers are generated. Rule in `.ace/standards/documentation.md` ("Manuscripts:
    Equations") and `.aceconfig`; `scripts/pubs/check_equations.py` runs in CI. It
    applies to every manuscript from now on; a submitted paper takes it at its next
    revision. The tracked Word file of the thesis was rebuilt later the same day with
    the numbers and the reviewed figures.
  - **Figure review (2026-10-12).** The seven thesis figures (all in Chapter 4) were
    regenerated from the current data; values unchanged. Four figure-versus-text defects
    fixed: the CD diagram and its caption left out the LIME-Anchors group in fidelity
    (ranks and groups are now computed in
    `scripts/generate_thesis_supplementary_figures.py`, no longer typed); the radar
    caption gave LIME the lead in parsimony (it is DiCE); the boxplot caption called
    the LIME stability mean a median; the coverage figure counted the inventory (274)
    and not the analysed runs (275). Method colours now follow the submitted papers
    (SHAP red, LIME blue, Anchors green, DiCE purple; palette of Paper F). **Paper
    figures were not touched** (papers are submitted): Paper B's two figures were read
    against the thesis and agree in values; C, D and F were read; E's are PDF only and
    were not opened. Not done: the unused English figures in `thesis/assets/figures`
    keep the old palette; the book-chapter figures take the new palette at their next
    rebuild (same generator); Chapter 6 has no figure.
- **Current state**: merged to `main` (pull request #57). The tutor agreed to the four
  design decisions; the record for the tutor states them as agreed.
- **Next steps**:
  1. Author: read Chapter 6 and the record; send the record and the rendered thesis to
     the tutor; refresh the table of contents in Word.
  2. Before deposit: the journals' prior-publication policies (point 6 above).
  3. Task 3 step 2 (macros and the CI build), if the author wants it before deposit.
- **Blockers**: none.

