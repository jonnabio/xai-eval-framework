# Active Context: XAI Evaluation Framework

> **This file holds the current state only. History is in the archive:
> [`docs/context/archive/README.md`](archive/README.md)** (index, one file per day).
> Read the archive when the task needs more than this file gives; when and how is
> rule CTX-3 of [`.ace/standards/context.md`](../../.ace/standards/context.md).
> Limit: 300 lines, checked in CI by `scripts/pubs/check_active_context.py`.

**Last updated:** 2026-11-25, by `claude-2026-11-24-paper-e`: session end, Paper E AAIR revision 1 submitted.

## Current objective

**Paper E, AAIR revision 1: SUBMITTED 2026-11-25** (major revision of 2026-11-24, editor Remzi
Gürfidan). Wait for the decision; do not rebuild unless the journal asks. Record:
`docs/reports/paper_e/aair_journal/revision_1/`.

**Paper G** (*Do faithfulness metrics agree?*, lane `paper-g`, *Informática y Sistemas*):
**SUBMITTED 2026-11-17**, submission 8895 (acknowledged the same day). Pre-submission review,
reviewer fixes, declarations and template compliance: PRs #143 and #144. Wait for the decision;
do not rebuild unless the journal asks for a revision.

**Paper B, revision 1** (C&I 2067810): **SUBMITTED 2026-11-12** after the editor reopened the
step left empty on 2026-11-10. Wait for the decision. The thesis objective below is unchanged.

**Close the thesis.** The tutor's note of 2026-10-12 asks for no change. On the author's
instruction of the same day, every paper is now reflected in the thesis (ADR-0023): a
new Chapter 6, `thesis/estudios-de-seguimiento.qmd`, reports the three later studies
(D, E, F) and the later controls of the inter-judge study (C); the conclusions render
as Chapter 7. No objective, hypothesis or proposition changed. Plan:
`docs/planning/thesis_followup_studies_plan_2026-10-12.md`. Record for the tutor, in
Spanish: `docs/review/tesis_cambios_para_tutor_2026-10-12.md` and `.docx`.

**Reconciliation with Papers A–F, 2026-11-23/24** (PRs #148, #149, #150; RCA-006). Audit and its
dispositions: `docs/review/thesis-papers-reconciliation-audit_2026-11-23.md` (closed). In the
thesis: Paper F's Reviewer A additions in Ch. 6 `sec-seg-transferencia` (in words, the numeric vs
mixed check marked *post hoc*); the mechanism of LIME's instability in Ch. 7 `sec-limitaciones`
(no Paper B revision-1 number); Adult's encoded width 108 (was 103) and "ocho variables
categóricas" (was 13); the EXP2 provenance limits (WP0 F7a–c, F8) disclosed in Ch. 3
(`sec-muestreo`, `sec-cobertura`, `sec-trazabilidad`, `tbl-validity-threats`). No confirmatory
statistic, objective or hypothesis changed. Earlier, PR #141 (2026-11-16, tutor's note) corrected
the DOI of Abdul Kadir et al. (2023) to 10.1109/INES59282.2023.10297629; the duplicate
`kadir2023` entry is now removed.

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
| **B** | *When Does SHAP Outperform LIME? Model- and Configuration-Dependent Results from a Paired Tabular Benchmark* | *Computers and Informatics* (C&I, DergiPark) | **Revision 1 submitted 2026-11-12** (2067810; major revision of 2026-11-06) | Revision C-000 – C-056, final check passes; 15 pp, supplement 52 pp; files from `ci_journal/revision_1/build/`. Record: `revision_1/README.md`, "Submission". Submitted 2026-10-21 |
| **C** | *Do LLM Judges Agree on the Quality of Explanations? A Two-Panel Reliability Study* | *Tecnología en Marcha*, AI special issue | Submitted | 2026-10-06 (reported by the author); number not recorded. Fourth draft. Zenodo 0.12.0, [10.5281/zenodo.23165763](https://doi.org/10.5281/zenodo.23165763) |
| **D** | *Are explanations less reliable when the model is wrong? Post-hoc explanation quality on misclassified instances* | *Tecnología en Marcha*, AI special issue | **Submitted 2026-10-03** | Through the author account (date given by the author on 2026-10-22); number not recorded. Zenodo 0.5.0, [10.5281/zenodo.23130014](https://doi.org/10.5281/zenodo.23130014) |
| **E** | *Do Explainers Agree on Which Features Matter? Instance-Level Agreement between SHAP and LIME* | *Advances in Artificial Intelligence Research* (AAIR, DergiPark) | **Revision 1 submitted 2026-11-25** (major revision of 2026-11-24; R1 minor, R2 and R3 major) | Revision: 21 items, `aair_journal/revision_1/` (manuscript 14 pp, changes marked, response 12 pp, supplement 9 pp); Zenodo 0.16.0, [10.5281/zenodo.24518192](https://doi.org/10.5281/zenodo.24518192). First submitted 2026-10-22; number not recorded. Word edition `docs/reports/paper_e/aair_journal/` (14 pages; intihal.net similarity 1%). Withdrawn from *Computación y Sistemas* (submission 6783 of 2026-10-04) by the author for its queue; withdrawal confirmed by the editor. Record: `aair_journal/AAIR_SUBMISSION.md`. Zenodo 0.8.0, [10.5281/zenodo.23142429](https://doi.org/10.5281/zenodo.23142429) |
| **F** | *How Dataset-Dependent Are Tabular Explainability Benchmarks?* | *Journal of Computer Sciences Institute* | **Accepted by the reviewer; final version submitted 2026-10-25** (editor's request of the same day); to be published in Vol. 41 (2026) | Submitted 2026-10-12; submission 10503; 8 pages. Format corrections sent to the editor 2026-10-13. Zenodo 0.15.0, [10.5281/zenodo.23325483](https://doi.org/10.5281/zenodo.23325483). To be published in Vol. 41 (2026) (author, 2026-11-25). Final files: `herrera-vasquez-final.pdf` (no. 47982) and `.docx` (no. 47981), in `submission/final_2026-10-25/`. Review and what was done: `docs/reports/paper_f/README.md`, sections 9 and 10 |
| **G** | *Do faithfulness metrics agree? Metric-dependent rankings of post-hoc explanations on tabular data* | *Informática y Sistemas* (UTM) | **Submitted 2026-11-17** (submission 8895; acknowledged the same day) | `docs/reports/paper_g/` (README, `review/BULLETPROOF_REVIEW_2026-11-17.md`); submitted files `submission/paper_g_blind.docx` (16 pp) and `Figure_1..5.png`, from PR #144 (`db0be47da`). Run: PR #123; analysis: #126-#140 |

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

- Three machines. **Documentation laptop** (Windows, `C:\Users\jonna\Github`) edits documents;
  **experiment laptop** (Windows, `D:\Github\xai-eval-framework`, Ryzen 5 4600H) is Paper B's
  recorded host; **Linux run host** (`jonnabio-Latitude-5450`, Ubuntu 26.04.1, i5-1335U, 14 GiB)
  is Paper G's only recorded host. On it, `~/xai-eval-framework` is the run clone (branch
  `paper/g-runs`, lock `paper-g-run-host`, never edited by hand) and
  `~/Documents/GitHub/xai-eval-framework` is a documentation clone.
- **Paper G branches:** `paper/g-runs` frozen at `04c6dfd84` (merged, PR #123; publisher timer stopped); `paper/g-manuscript-completion` and `pubs/paper-g-claims` merged (#139, #140); no Paper G work is unmerged.
- `main` holds everything up to pull request #150 and this handoff. `paper/b-ci-revision-1` is
  level with `main`; kept until the editor confirms receipt, then deleted. `paper/b-rev1-runs` (raw cohort B2 rows and
  logs, 6,716 files, about 169 MB; merges cleanly) is ahead of `main` and **not merged**: the
  author decides whether it goes to `main` (see Open with the author). `thesis/rca-001-phase-2`
  was level with `main` after PR #150 and takes `main` when the thesis lane resumes. `pubs/paper-b-rev1-lane` exists on
  GitHub only (not examined).
- Locks: `paper-g-run-host` in the run clone only (goes stale 12 h after the last publish, by
  design). Nothing runs on any machine; the run host keeps the read-only dashboard
  (`paper-g-dashboard` user unit, http://127.0.0.1:8766) until the author closes it.
- Lanes and the paths they own: `scripts/pubs/lanes.toml`.
- The thesis renders to Word with seven chapters and no unresolved reference
  (`thesis/render.ps1`; `thesis/_output/JHerrera_XAI_Tesis_Doctorado.docx` is tracked).

## Open with the author

0. **CIFIE/FOM-7 chapter:** Revision 1 attended; author to dispatch the package
   (`capitulo_cifie_xai_fom7_Revision_1_Atendido.docx`, `_bn.docx`,
   `RESPUESTA_A_REVISORES_REVISION_1.pdf`) to editor Dra. Irene Arostegui.
1. **Paper F:** final version submitted 2026-10-25; wait for the journal (proofs or
   publication, target issue 30 March 2027).
2. Submission numbers of Papers C, D and E (AAIR). Paper B (C&I) is 2067810.
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
8. **Paper B runs branch:** whether `paper/b-rev1-runs` (169 MB of raw rows) is merged into
   `main`, kept as a branch, or deposited elsewhere (e.g. Zenodo). The analyses it feeds are
   already on `main` (`outputs/analysis/paper_b_rev1/`, `revision_1/results/`).
9. **Paper G:** the author actions of the latest handoff (review, declarations, AI-content
   limit, double-blind risk of the public repository, Word check, OJS submission components);
   `docs/reports/paper_g/AUTHOR_REVIEW_CHECKLIST.md`. Submission is the author's.
10. **Linux run host:** automatic updates were paused for the run (`unattended-upgrades`,
    `apt-daily*.timer` disabled 2026-11-14). No further Paper G run is planned (experimental
    phase complete), so they can be re-enabled (author, sudo):
    `sudo systemctl enable --now unattended-upgrades apt-daily-upgrade.timer apt-daily.timer`.
11. **Tutor record for the 2026-11-23/24 edits:** Ch. 3, which the tutor approved, now carries
    the EXP2 provenance disclosures (E5) and Ch. 7 the width 108 (E4); the tutor record
    (`docs/review/tesis_cambios_para_tutor_2026-10-12.md`) does not list them yet. Also flagged:
    the Resumen and Abstract call the benchmarking conditions "reproducibles"; F7a qualifies that
    for the random-forest cells (sweep log 2026-11-24). No rewording made.

## Active constraints

The full list as it stood, with the reason for each: archive `undated-state-sections.md`
("Active Constraints"). The ones that bind current work:

- **Lanes (ADR-0013, ADR-0021).** Claim before any edit; `main` is never worked on
  directly. A commit never mixes a lane's paths with shared paths (`pub/`,
  `scripts/pubs/`, `docs/rca/`, `docs/context/`, `docs/review/`, `.zenodo.json`,
  `CITATION.cff`, `pubs-sync.yml`). Shared commits go on a `pubs/*` branch and reach
  `main` in the session they are made; lanes then take `main`. Lanes never merge into
  each other.
- **Guards.** RCA-001 to RCA-006 in `docs/rca/regression-guards.yaml`; RCA-006 (EXP2 cohort
  provenance) guards Ch. 3, Ch. 7, the appendices and `WP0_FINDINGS.md`: the EXP2 runner is not
  reused for a new cohort, the width stays 108, the Ch. 3 disclosures stay. Any edit
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
- **Permissions.** Pushing or merging `main` may be refused to the assistant: try once; if refused, leave it to the author.

## Latest handoff - 2026-11-25, SESSION END (Paper E AAIR revision 1 submitted)

Session `claude-2026-11-24-paper-e` (documentation laptop). Lane `paper-e`; lock released at
the end of this handoff. Previous handoff: archive `2026-11-24.md`.

- **Completed:**
  - AAIR decision (major revision, 2026-11-24) analysed: 21 items (`REVIEW_ANALYSIS.md`), plan
    WP0–WP7 and decisions D-1..D-5 agreed (`REVISION_PLAN.md`), changes C-000..C-010.
  - RCA-007: pandoc wrote each LaTeX minus as a one-character Word equation; signs are now text
    and `build_paper_e_aair_docx.py` checks every table row and negative number (`--edition rev1`
    default; the submitted edition is refused).
  - New post hoc analyses: Adult held-out, same-class permutation, leave-one-seed-out
    (`paper_e_revision1_analyses.py`), LIME settings (`paper_e_lime_settings.py`); ANALYSIS_PLAN
    deviations of 2026-11-24 recorded.
  - Manuscript, changes-marked file (Word compare), response letter (each item: heading, verbatim
    comment, "Response."; overview items list the changes; justified), supplement (S1–S8).
  - Zenodo 0.16.0 (`10.5281/zenodo.24518192`, release `paper-e-aair-2026-11-24-r1`).
  - PRs #152–#158 merged. **Revision uploaded by the author 2026-11-25.**
  - Publication table: E revised; F "to be published in Vol. 41 (2026)" (author, 2026-11-25).
- **Current State:** `check_revision.py` READY (21 items). Papers B, C, D, E, F (in press), G
  wait for the journals. Thesis state as in archive `2026-11-24.md`.
- **Next Steps:**
  1. Sync: `git fetch origin`, `git switch main`, `git pull --ff-only`; `check_lane.py claim`.
  2. Act only on a journal's decision; record it in the table above and the paper's README.
  3. Thesis items still open from 2026-11-24: refresh the table of contents in Word; E4/E5 in the
     tutor record; prior-publication policy of each journal before deposit.
- **Blockers/Issues:** none. Untracked and left alone: `docs/reports/paper_a/paper_a_rimi.pdf`,
  `docs/reports/paper_g/venue/template/ISRTIC_Plantilla_Articulo-EN.docx` (author's files).
- **Notes:** Paper E revision build: `.venv/Scripts/python.exe
  docs/reports/paper_e/aair_journal/revision_1/scripts/build_revision.py` then
  `check_revision.py`; it also rebuilds the manuscript and changes-marked files (restore them
  with `git checkout` if only the letter changed). German Credit and Breast Cancer analyses need
  the EXP3 binaries (`scripts/train_exp3_models.py --model-root <dir>`). The lane guard refuses
  branch names outside `scripts/pubs/lanes.toml` (use `paper/e-*` for Paper E).
