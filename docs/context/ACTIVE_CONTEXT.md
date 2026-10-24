# Active Context: XAI Evaluation Framework

> **This file holds the current state only. History is in the archive:
> [`docs/context/archive/README.md`](archive/README.md)** (index, one file per day).
> Read the archive when the task needs more than this file gives; when and how is
> rule CTX-3 of [`.ace/standards/context.md`](../../.ace/standards/context.md).
> Limit: 300 lines, checked in CI by `scripts/pubs/check_active_context.py`.

**Last updated:** 2026-10-24, by `gemini-2026-10-24-cifie`.

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
- **CIFIE/FOM-7 chapter:** Editorial Revision 1 received 2026-10-23 (editor Dra. Irene Arostegui, 5 comments); fully attended on 2026-10-24 (commit `b40556cc2` on `main`). Built clean in color and B/W (~8,203 words, limit 9,000 words); formal response letter in md/docx/pdf (Option A, single author Jonathan Herrera-Vásquez). Ready for dispatch to the editor. Detail: `publications/book_chapters/2026_cifie_xai_fom7/drafts/v5_revision_1/`.
- Revision routes, known limits of each submitted paper and the Zenodo release route:
  the paper's README and archive `2026-10-12.md` (Paper F), `2026-10-05.md` (C),
  `2026-10-04.md` (B, E), `2026-10-03.md` (D).

## Repository state

- Main folder `xai-eval-framework`: thesis lane. Other folders: `../xai-exp4`
  (`results/exp4-cohort2`), `../xai-eval-framework-main-status` (`main`, read only).
  Lanes and the paths they own: `scripts/pubs/lanes.toml`.
- `main` holds everything up to commit `b40556cc2` (CIFIE Revision 1 attended, merged
  2026-10-24). `chapter/cifie-revision-1`, `paper/b-computers-informatics`, and
  `paper/f-external-validity` hold nothing that is not on `main`; `thesis/rca-001-phase-2`
  is behind `main` and takes `main` when the thesis lane resumes.
- The lane lock of the main folder is free.
- Nothing is running: no task, no process.
- Verifiers at the last check (2026-10-24): `verify_claims.py` 1,391 claims, 1,808
  sites, 39 files fully registered; `verify_sync.py`, `verify_exp4_reconstruction.py`,
  `scan_shared_literals.py --strict`, `check_equations.py` and `check_active_context.py`
  pass; `pytest tests/pubs` 47 passed.
- The thesis renders to Word with seven chapters and no unresolved reference
  (`thesis/render.ps1`; `thesis/_output/JHerrera_XAI_Tesis_Doctorado.docx` is tracked).

## Open with the author

0. **CIFIE/FOM-7 chapter:** Revision 1 attended; author to dispatch the package
   (`capitulo_cifie_xai_fom7_Revision_1_Atendido.docx`, `_bn.docx`,
   `RESPUESTA_A_REVISORES_REVISION_1.pdf`) to editor Dra. Irene Arostegui.
1. **Paper F:** revision for Reviewer A submitted 2026-10-19; wait for the editor.
2. Submission numbers of Papers B (C&I), C, D and E (AAIR).
3. The final text of Paper F's comments to the editor (not shown to the session).
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

## Latest handoff - 2026-10-24, SESSION END (CIFIE Book Chapter Revision 1 Attended and Merged)

Session of 2026-10-24, lane `chapter` (branch `chapter/cifie-revision-1`, owner `gemini-2026-10-24-cifie`).

- **Completed**:
  - Editorial Revision 1 of CIFIE/FOM-7 book chapter (`publications/book_chapters/2026_cifie_xai_fom7/drafts/v5_revision_1/capitulo_cifie_xai_fom7_Revision_1.docx`) from editor Dra. Irene Arostegui (Colección CIFIE / Editorial Tintazul) systematically reviewed and all 5 comments fully addressed:
    - **C44**: Mapped FOM-7 7-gate lifecycle to empirical metrics in Table 1 across operational, statistical, and agreement tiers (`06_protocolo_fom7.md`, `07_diseno_empirico.md`, `table_metrics.md`).
    - **C50**: Qualified absolute reproducibility claims with 4-layer control framework (seeds, environment, pinned deps, deterministic SHAP/LIME sampling) (`07_diseno_empirico.md`).
    - **C54**: Demarcated provenance of RIMI 2026 / PhD thesis empirical baseline vs original chapter contributions (`02_introduccion.md`, `table_results_summary.md`).
    - **C69**: Calibrated epistemic modesty; purged "certificar/certificación", reframing FOM-7 as technical acceptance criteria under Level 3 functional evaluation (`11_conclusiones.md`).
    - **C71**: Restructured Section 10 into explicit limitations axes followed by mirrored future agenda (`10_limitaciones_trabajo_futuro.md`).
  - Incorporated author's edit in Section 10 heading (*«Alcance y limitaciones del estudio»*).
  - Recompiled both digital color and monochrome print Word manuscripts via `pandoc`:
    - `capitulo_cifie_xai_fom7_Revision_1_Atendido.docx` (8,203 words).
    - `capitulo_cifie_xai_fom7_Revision_1_Atendido_bn.docx` (8,203 words).
  - Drafted formal response letter to the editor (`RESPUESTA_A_REVISORES_REVISION_1.md`) using Option A clean academic header, single-author first-person impersonal tone (Jonathan Herrera-Vásquez), and detailed comment-by-comment remediation tables.
  - Built professional Word and PDF editions of the response letter via `build_letter.py` (python-docx + Word COM) with left-aligned headers and blockquotes avoiding unjustified whitespace stretching:
    - `RESPUESTA_A_REVISORES_REVISION_1.docx`
    - `RESPUESTA_A_REVISORES_REVISION_1.pdf`
  - Verified numerical integrity (`verify_claims.py`: 1,391 claims, 1,808 sites; `verify_sync.py`: clean).
  - Merged work from `chapter/cifie-revision-1` into `main` (commit `b40556cc2`) and pushed to `origin`.
- **Current State**:
  - `main` branch updated to commit `b40556cc2` containing all CIFIE Revision 1 remediations, recompiled manuscripts, and response letters.
  - All chapter artifacts in `publications/book_chapters/2026_cifie_xai_fom7/drafts/v5_revision_1/` are complete, formatted, and ready for delivery to Dra. Irene Arostegui.
  - Working tree clean of lane changes; lane lock released.
- **Next Steps**:
  1. Author sends submission package (`capitulo_cifie_xai_fom7_Revision_1_Atendido.docx`, `_bn.docx`, `RESPUESTA_A_REVISORES_REVISION_1.pdf`) to Dra. Irene Arostegui.
  2. Record submission numbers for Papers B (C&I), C, D, and E (AAIR) when assigned.
  3. Paper F: await JCSI editorial decision on Reviewer A revision.
  4. Thesis lane: rebase/merge `main` into `thesis/rca-001-phase-2` and address open author items.
- **Blockers/Issues**:
  - None blocking. Keep Word closed when recompiling docx manuscripts or building response letter to avoid Windows file lock errors (`EACCES`/`permission denied`).
- **Notes**:
  - Recompile command for CIFIE chapter:
    `pandoc --citeproc --bibliography=publications/book_chapters/2026_cifie_xai_fom7/drafts/v4_final_submission/capitulo_cifie.bib --csl=publications/book_chapters/2026_cifie_xai_fom7/drafts/v4_final_submission/apa.csl --reference-doc=publications/book_chapters/2026_cifie_xai_fom7/drafts/v4_final_submission/custom_template.docx ...`
  - Response letter builder script: `python C:/Users/jonna/.gemini/antigravity-ide/brain/e09777f1-a95d-432c-ab9c-9538b759a455/scratch/build_letter.py` (converts markdown to docx with custom styling and exports PDF via Word COM).
