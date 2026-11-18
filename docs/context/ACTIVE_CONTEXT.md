# Active Context: XAI Evaluation Framework

> **This file holds the current state only. History is in the archive:
> [`docs/context/archive/README.md`](archive/README.md)** (index, one file per day).
> Read the archive when the task needs more than this file gives; when and how is
> rule CTX-3 of [`.ace/standards/context.md`](../../.ace/standards/context.md).
> Limit: 300 lines, checked in CI by `scripts/pubs/check_active_context.py`.

**Last updated:** 2026-11-17, by `claude-2026-11-17` (Windows documentation laptop): Paper G submitted.

## Current objective

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
| **E** | *Do Explainers Agree on Which Features Matter? Instance-Level Agreement between SHAP and LIME* | *Advances in Artificial Intelligence Research* (AAIR, DergiPark) | **Submitted 2026-10-22** | Number not recorded. Word edition `docs/reports/paper_e/aair_journal/` (14 pages; intihal.net similarity 1%). Withdrawn from *Computación y Sistemas* (submission 6783 of 2026-10-04) by the author for its queue; withdrawal confirmed by the editor. Record: `aair_journal/AAIR_SUBMISSION.md`. Zenodo 0.8.0, [10.5281/zenodo.23142429](https://doi.org/10.5281/zenodo.23142429) |
| **G** | *Do faithfulness metrics agree? Metric-dependent rankings of post-hoc explanations on tabular data* | *Informática y Sistemas* (UTM) | **Submitted 2026-11-17** (submission 8895; acknowledged the same day) | `docs/reports/paper_g/` (README, `review/BULLETPROOF_REVIEW_2026-11-17.md`); submitted files `submission/paper_g_blind.docx` (16 pp) and `Figure_1..5.png`, from PR #144 (`db0be47da`). Run: PR #123; analysis: #126-#140 |
| **F** | *How Dataset-Dependent Are Tabular Explainability Benchmarks?* | *Journal of Computer Sciences Institute* | **Accepted by the reviewer; final version submitted 2026-10-25** (editor's request of the same day); awaiting publication | Submitted 2026-10-12; submission 10503; 8 pages. Format corrections sent to the editor 2026-10-13. Zenodo 0.15.0, [10.5281/zenodo.23325483](https://doi.org/10.5281/zenodo.23325483). Target issue: 30 March 2027. Final files: `herrera-vasquez-final.pdf` (no. 47982) and `.docx` (no. 47981), in `submission/final_2026-10-25/`. Review and what was done: `docs/reports/paper_f/README.md`, sections 9 and 10 |

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
- `main` holds everything up to pull request #114 and this handoff. `paper/b-ci-revision-1` is
  level with `main`; kept until the editor confirms receipt, then deleted. `paper/b-rev1-runs` (raw cohort B2 rows and
  logs, 6,716 files, about 169 MB; merges cleanly) is ahead of `main` and **not merged**: the
  author decides whether it goes to `main` (see Open with the author). `thesis/rca-001-phase-2`
  is behind `main` and takes it when the thesis lane resumes. `pubs/paper-b-rev1-lane` exists on
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
- **Permissions.** Pushing or merging `main` may be refused to the assistant: try once; if refused, leave it to the author.

## Latest handoff - 2026-11-16, SESSION END (Paper G: manuscript merged; handoff to the Windows laptop)

Session owner `paper-g-task21` (Linux run host, documentation clone
`~/Documents/GitHub/xai-eval-framework`); Tasks 20 and 21 and this consolidation. Lane `paper-g`
(lock released); this handoff on `pubs/context-2026-11-16-paper-g-handoff`.

- **Project state:** Paper G experimental phase COMPLETE; original analysis COMPLETE AND VERIFIED;
  S3 COMPLETE; S1 COMPLETE AND VERIFIED; exploratory diagnostics COMPLETE; manuscript preparation
  ACTIVE; submission NOT AUTHORIZED.
- **Revisions:** PR #139 merge `aa5524d70` (manuscript, figures, references, build scripts,
  reports); PR #140 merge `b34f61227` (resolver `paper_g`, `scripts/pubs/register_paper_g.py`,
  185 claims, coverage and exclusivity guards, CI step). Manuscript source: last change
  `58d6b9b68` (`docs/reports/paper_g/paper_g_draft.md`). Claim registry: `b34f61227`. `main`
  after this handoff is its merge commit, which descends from `b34f61227`.
- **Integrity (checked at `b34f61227`):** no change since `bb6ea3c7c` to
  `outputs/analysis/paper_g/` (1,294 files; raw and S1 manifests identical), frozen code,
  `experiments/exp_g/`, `RESULTS_REPORT.md`, `ANALYSIS_PLAN.md`; original analysis identical to
  `3b0063f41`; `paper_g_analyze.py --validate-only` passes; `verify_claims` 2,083 claims, 2,500
  sites; `register_paper_g.py --check` OK; 134 Paper G tests pass; equations of the manuscript
  match the frozen functions (`docs/reports/paper_g/verification/verify_equations.py`, 480 checks).
- **Manuscript artifacts** (`docs/reports/paper_g/`): `paper_g_draft.md` (source; numbers are
  placeholders), `paper_g.md` (rendered), `submission/paper_g_blind.docx` and `.pdf` (13 pages,
  journal template), `submission/Figure_1..5`, `EVIDENCE_MAP.md`, `RIGOR_REVIEW.md`,
  `JOURNAL_COMPLIANCE.md`, `SUBMISSION_READINESS.md`, `REFERENCE_VERIFICATION.md`,
  `AUTHOR_REVIEW_CHECKLIST.md`. Rebuild after any edit of the source:
  `python docs/reports/paper_g/scripts/build_paper_g.py --evidence-map`, then
  `python scripts/pubs/register_paper_g.py` and `python scripts/pubs/verify_claims.py` (the
  .docx build needs pandoc and LibreOffice; on Windows, open the .docx in Word instead).
- **Remaining author actions** (never completed by the assistant):
  1. Substantive review of the manuscript; the journal's AI-content limit (30%, Compilatio).
  2. Funding declaration (and the OJS Supporting Agencies field).
  3. Conflicts-of-interest declaration.
  4. Generative-AI-use declaration: extent of own review; any other assistant used (ChatGPT was
     set up as advisor, `CHATGPT_ADVISOR_PROMPT.md`).
  5. Double-blind risk: the manuscript and its history are public on GitHub under the author's
     name since 2026-11-13; decide (tell the editor, make private, or accept). Not changed.
  6. Word check of pagination, equations and repeated table headers.
  7. Submission components in OJS (anonymised .docx, figure files, checklist and copyright
     notice accepted online, author metadata and ORCID; no separate signed agreement).
- **Next task (Windows documentation laptop):** Task 21 — final manuscript review, author
  corrections and submission readiness. No experiment is to be restarted.
- **Windows sync:** in `C:\Users\jonna\Github\xai-eval-framework`: `git status` (preserve any
  local changes first: commit them on a branch or `git stash push -u`), then `git fetch origin`,
  `git switch main`, `git pull --ff-only origin main`, `git status`, `git log -1 --oneline`;
  check `git merge-base --is-ancestor b34f61227 HEAD` returns 0.
- **Notes:** `pub/fragments/build_meta.env` changes when `generate_fragments.py` runs on another
  machine (path and time); do not commit that change. Merged branches `paper/g-manuscript-completion`
  and `pubs/paper-g-claims` are kept on GitHub (not deleted).
