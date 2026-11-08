# Active Context: XAI Evaluation Framework

> **This file holds the current state only. History is in the archive:
> [`docs/context/archive/README.md`](archive/README.md)** (index, one file per day).
> Read the archive when the task needs more than this file gives; when and how is
> rule CTX-3 of [`.ace/standards/context.md`](../../.ace/standards/context.md).
> Limit: 300 lines, checked in CI by `scripts/pubs/check_active_context.py`.

**Last updated:** 2026-11-07, by `claude-2026-11-07-paper-b-docs`.

## Current objective

**Paper B, revision 1** (C&I 2067810, major revision of 2026-11-06, due
**2026-11-30**; extension decision by 10 November, the author's): the text is done; the
results of cohort B2 are the only input pending. Work folder
`docs/reports/paper_b/ci_journal/revision_1/` (start with `HANDOFF.md`,
`CONSISTENCY_2026-11-07.md`). The thesis objective below is unchanged.

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
| **B** | *When Does SHAP Outperform LIME? Model- and Configuration-Dependent Results from a Paired Tabular Benchmark* | *Computers and Informatics* (C&I, DergiPark) | **Major revision** (2067810, 2026-11-06; due 2026-11-30) | Revision text done and consistent (C-000 – C-037, `ci_journal/revision_1/CONSISTENCY_2026-11-07.md`); only the cohort B2 results are pending (`revision_1/HANDOFF.md`). Runs on the experiment laptop (`paper/b-rev1-runs`), documents on `paper/b-ci-revision-1`. Submitted 2026-10-21 |
| **C** | *Do LLM Judges Agree on the Quality of Explanations? A Two-Panel Reliability Study* | *Tecnología en Marcha*, AI special issue | Submitted | 2026-10-06 (reported by the author); number not recorded. Fourth draft. Zenodo 0.12.0, [10.5281/zenodo.23165763](https://doi.org/10.5281/zenodo.23165763) |
| **D** | *Are explanations less reliable when the model is wrong? Post-hoc explanation quality on misclassified instances* | *Tecnología en Marcha*, AI special issue | **Submitted 2026-10-03** | Through the author account (date given by the author on 2026-10-22); number not recorded. Zenodo 0.5.0, [10.5281/zenodo.23130014](https://doi.org/10.5281/zenodo.23130014) |
| **E** | *Do Explainers Agree on Which Features Matter? Instance-Level Agreement between SHAP and LIME* | *Advances in Artificial Intelligence Research* (AAIR, DergiPark) | **Submitted 2026-10-22** | Number not recorded. Word edition `docs/reports/paper_e/aair_journal/` (14 pages; intihal.net similarity 1%). Withdrawn from *Computación y Sistemas* (submission 6783 of 2026-10-04) by the author for its queue; withdrawal confirmed by the editor. Record: `aair_journal/AAIR_SUBMISSION.md`. Zenodo 0.8.0, [10.5281/zenodo.23142429](https://doi.org/10.5281/zenodo.23142429) |
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

- Two laptops (author, 2026-11-06). **This one** (`C:\Users\jonna\Github`) edits documents
  on `paper/b-ci-revision-1`; **the experiment laptop** (`D:\Github\xai-eval-framework`, Ryzen 5
  4600H, the one recorded host) runs cohort B2 and pushes only `paper/b-rev1-runs`.
- `main` holds everything up to pull request #80 and this handoff. `paper/b-ci-revision-1` is
  level with `main` and stays open for the revision. `paper/b-rev1-runs` (snapshots of the
  running cohort, not merged) is ahead of `main`; merge it once the results are final.
  `thesis/rca-001-phase-2` is behind `main` and takes it when the thesis lane resumes.
  `pubs/paper-b-rev1-lane` exists on GitHub only (not examined this session).
- Lane lock of the main folder released at session end. Nothing runs on this laptop; the
  cohort B2 quality pass runs on the experiment laptop (6 workers, sync loop every 15 min).
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

## Latest handoff - 2026-11-07, SESSION END (Paper B revision 1: text complete, awaiting cohort B2 results)

Session of 2026-11-06/07, owner `claude-2026-11-07-paper-b-docs` (documentation laptop).
Lane `paper-b` (`paper/b-ci-revision-1`); shared files on `pubs/context-2026-11-07`. Pull
requests #79 and #80 merged, and the one carrying this handoff.

- **Completed**:
  - MiKTeX installed (user install); `build_revision.py` runs on this laptop.
  - References, option A (C-028): 53 references, literature 23 of 27 from 2024 on (85%).
    Introduction cites verified sources for each claim (C-031); REFORMS added, DOI checked and
    full text read, cited for item 2c only (C-032).
  - Methods aligned with the code (C-029); role of Anchors and DiCE stated (C-030).
  - Introduction: two gaps (control, configuration) mapped to the three contributions (C-033).
  - Table 5: row "usefulness for people" removed (C-034). Conclusions open with the answer to
    the title question, slots [R] (C-035). Abstract and §1: only model calls are
    host-independent, not CPU time (C-032, C-036). RF–XGBoost reversal posed as the tested
    question, credited to the reviewer in the letter (C-037).
  - Quality results filled (C-040, PR after #85): Tables 2 (no p_Holm yet) and 4, §4.1, §4.5,
    §6, abstract; analysis in `revision_1/results/`. Manuscript now 12 of 12 pages in Word.
  - Cost (H2) tested in wall-clock time, not CPU time: Windows CPU time moves in 15.6 ms
    steps, seen in the first timing cells (author's decision, C-038; analysis script updated;
    the running timing pass is unaffected). PR #84.
  - Response letter: ED-2 and ED-3 removed (no answer, author); every comment quoted in full;
    the editor, Reviewer 1 and Reviewer 2 each start on a new page.
  - Consistency pass: manuscript, ledger, response and proposal agree
    (`CONSISTENCY_2026-11-07.md`; proposal Part E). Handoff note to the experiment laptop
    (`revision_1/HANDOFF.md`).
  - Partial analysis of the 18:21 snapshot (scratchpad, pinned packages, not committed):
    on Adult SHAP leads on fidelity against all three (p_Holm < 1e-4) and on the faithfulness
    gap against LIME and DiCE; stability against LIME not significant; on the six other
    datasets full LIME is more stable than SHAP. Cost: no data yet.
- **Update 2026-11-08 (documentation laptop, PRs #91, #92)**:
  - Cost results filled from the 25 Adult timing cells (C-042): Table 2 cost rows and p_Holm
    (family of 12), Table 3, §4.2, Table 5 cost row, §6, abstract. H2 not supported: KernelSHAP
    3-25x LIME's wall time (19.5 s on SVM) but p_Holm 0.11; SHAP faster than Anchors in all
    cells; TreeSHAP ~LIME on RF, 1/9 of LIME on XGBoost. `revision_1/results/` regenerated
    (snapshot 992d20038, with cost.csv).
  - `check_revision.py`: 51 items, 28 closed (27 remediated, 1 explained), 23 pending; 44
    changes (C-000 – C-043; C-043, PR #94: §4.1 zero-vector exclusion, Table 5 rows, §5/§5.1
    partial, R1-M3). Manuscript 13 pages (references spill).
  - **Mandatory before submission: the author's length review**, once every result is in; do
    not trim before then (author, 2026-11-08; listed in `revision_1/README.md`).
  - Asked the experiment laptop (HANDOFF.md): Anchors on XGBoost records 0 model calls
    (`XGBClassifier.predict` not counted).
  - Timing pass: 33 of 115 cells at 07:14 on 2026-11-08 (Adult done), 0 errors.
- **Current State**:
  - Manuscript 12 pages (budget 12), letter 15 pages; `check_revision.py`: 51 items, 19
    closed (18 remediated, 1 explained), 32 pending; 42 changes (C-000 – C-041).
  - Cohort B2: quality pass complete (575/575). Timing pass: 6 of 115 cells at 22:24 (Adult
    logreg 7-8 min, RF 10 min per cell; benchmark 16 ms, 0 errors). Estimate about 37 h in
    total (SVM cells about 1.6 h each), so it ends around 9 November, morning. Then the sweep, validity controls, grouped masking and the matched RF–XGBoost run not started.
  - Tree clean; all branches pushed; lock released.
- **Next Steps**:
  1. `python scripts/pubs/check_lane.py claim --owner <session name>` on
     `paper/b-ci-revision-1`; `git pull --no-rebase`.
  2. Read `revision_1/HANDOFF.md`; check whether the experiment laptop answered it.
  3. When results arrive on `paper/b-rev1-runs`: run `scripts/paper_b_analyze.py` on them,
     fill every [R] marker (Tables 2–5, §4, §5, §6, abstract, response), regenerate
     `CONSISTENCY_*.md`, then `check_revision.py --final` and `build_revision.py`.
  4. The supplement (D-B), last, as the author asked.
- **Blockers/Issues**:
  - Cohort B2 results (33 of the 34 open items). R1-9 waits for the author's reading of the
    15 recent abstracts (`REFERENCE_AUDIT.md`).
  - Closed by the experiment laptop (2fd1cb7f9, after the session's last merge): the Adult
    LIME zero-vector figure (0.88, 0.95) is a count out of 15 perturbed explanations, i.e.
    5.8% and 6.3% of vectors (the commit message's 2.7%/3.0% was wrong); the 0-of-575 job count was read from the wrong folder. Merge
    `paper/b-ci-revision-1` into `main` (it carries that fix) when resuming if not merged.
  - Decision with the author: extension request by 10 November. The timing pass runs under
    the "ASUS Recommended" power plan (recorded per cell; disclose, do not restart).
  - `tests/analysis/test_stats.py` and `test_visualization.py` fail at collection; not
    investigated.
- **Notes**:
  - Builds on this laptop: prepend `%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64` to PATH in
    Git Bash; `.venv\Scripts\python.exe docs/reports/paper_b/ci_journal/revision_1/scripts/build_revision.py`.
  - The build's citation check does not read `\cite[...]{...}`: name a locator in the prose.
  - The analysis needs statsmodels and the pinned pandas/SciPy (`revision_1/env/
    requirements-rev1-frozen.txt`); the project `.venv` has neither: use a throwaway venv.
  - Internal notes in `RESPONSE_TO_REVIEWERS.md` must be HTML comments; every change gets a
    C-row in `CHANGELOG.md` in the same commit and its C-id under each item it answers.
  - After `main` is merged into the lane, pull with `--no-rebase`: a rebase drops the merge
    commit and the lane guard refuses commits until `main` is merged again.
