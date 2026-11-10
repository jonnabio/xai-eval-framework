# Active Context: XAI Evaluation Framework

> **This file holds the current state only. History is in the archive:
> [`docs/context/archive/README.md`](archive/README.md)** (index, one file per day).
> Read the archive when the task needs more than this file gives; when and how is
> rule CTX-3 of [`.ace/standards/context.md`](../../.ace/standards/context.md).
> Limit: 300 lines, checked in CI by `scripts/pubs/check_active_context.py`.

**Last updated:** 2026-11-10, by `claude-2026-11-10-paper-b-runs` (experiment laptop).

## Current objective

**Paper B, revision 1** (C&I 2067810, major revision of 2026-11-06, due
**2026-11-30**): every cohort B2 run is finished and analysed, every result is in the
manuscript and the supplement (C-040 to C-055), R1-9 is closed (C-054) and
`check_revision.py --final` passes (manuscript 15 pp, response 17 pp, supplement 52 pp). The
author decided to submit at 15 pages and let the editor decide (`LENGTH_OPTIONS_2026-11-09.md`).
What remains is the author's submission. Work folder
`docs/reports/paper_b/ci_journal/revision_1/` (start with `HANDOFF.md`). The thesis objective
below is unchanged.

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
| **B** | *When Does SHAP Outperform LIME? Model- and Configuration-Dependent Results from a Paired Tabular Benchmark* | *Computers and Informatics* (C&I, DergiPark) | **Major revision** (2067810, 2026-11-06; due 2026-11-30) | Revision complete: C-000 to C-055, all cohort B2 results in, `check_revision.py --final` passes; awaiting the author's submission (`ci_journal/revision_1/HANDOFF.md`). Runs finished 2026-11-09 on the experiment laptop (`paper/b-rev1-runs`, not merged); documents on `paper/b-ci-revision-1`. Submitted 2026-10-21 |
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
- `main` holds everything up to pull request #110 and this handoff. `paper/b-ci-revision-1` is
  level with `main` and stays open for the revision. `paper/b-rev1-runs` (raw cohort B2 rows and
  logs, 6,716 files, about 169 MB; merges cleanly) is ahead of `main` and **not merged**: the
  author decides whether it goes to `main` (see Open with the author). `thesis/rca-001-phase-2`
  is behind `main` and takes it when the thesis lane resumes. `pubs/paper-b-rev1-lane` exists on
  GitHub only (not examined).
- No lane lock is held. Nothing runs on either laptop: the experiment laptop's save loop,
  study chain and 30-minute monitor are stopped (2026-11-09 23:32); only the read-only
  dashboards may still be open there.
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

## Latest handoff - 2026-11-10, SESSION END (Paper B revision 1: cohort B2 runs finished and analysed)

Session of 2026-11-08/10, owner `claude-2026-11-10-paper-b-runs` (experiment laptop,
`D:\Github\xai-eval-framework`). Lane `paper-b`: run code on `paper/b-ci-revision-1`, results
pushed to `paper/b-rev1-runs`; this handoff on `pubs/context-2026-11-10`. The documentation
laptop worked in parallel (C-053 to C-055, PRs #106 to #110); it is not described here.

- **Completed**:
  - Cohort B2 (design hash `4ab8673a4a20`), all on the recorded host:
    main quality 575/575 jobs (52,740 valid rows; 5 Anchors-on-SVM instances timed out, disclosed
    as timeouts, not rerun: adult/svm/33 5480 and 5853, connect4/svm/22 10845, connect4/svm/33
    5786 and 674); main timing 115/115 cells.
  - Auxiliary studies through `PAPER_B_CONFIG`: `controls_nonoise` 75/75 (1 timeout, 5480),
    `controls_onehot` 75/75, `sweep` 669/669 quality + 15/15 timing, `matched` 12/12 timing;
    Anchors-on-XGBoost rows rerun 23/23 cells (not 25, as first stated). Analyses in
    `outputs/analysis/paper_b_rev1/` (main, `posthoc_<dataset>/` for the six other datasets,
    `study_*`, `xgb_anchors_rows/`), commit `1e8359d93`. Main primary effects unchanged after
    the analysis fixes.
  - Run-code fixes, each with a test (`tests/analysis/test_paper_b_rev1.py`, 54 pass):
    stale-heartbeat kill loop; admission with backfill (`plan_admissions`); RAM reserve
    6.0 -> 3.5 GB with live reload; design hash cached at launch and twin-worker guard
    (`jobs_running_elsewhere`) after a BOM in a config crashed the governor; `onehot_groups`
    verified on the data; `CallCounter` now counts `XGBClassifier.predict`
    (`_paper_b_counted`); timing runs only explainers that apply to the model
    (`explainer_applies`; 53 mislabelled tshap sweep rows dropped by `applicable_timing`, none
    deleted); analysis counts jobs in the analysed root, keeps sweep cells, has a timing-only path,
    and reports `stability_zero_vector_share`; throttling alarm uses medians.
  - Remote progress log: every runs-branch snapshot commit carries `commit_log()` (status,
    failed rows, governor events, study chain, monitor notes), read from the other laptop.
    New scripts: `scripts/paper_b_chain.ps1`, `scripts/paper_b_xgb_anchors_rows.ps1`.
- **Current State**:
  - Every run finished 2026-11-09 23:00; save loop, chain and monitor stopped; last runs-branch
    snapshot `52988d3b7`. Tree clean; `paper/b-ci-revision-1` level with `main` (#110).
  - Paper B documents: final check passes, awaiting the author's submission (see Current
    objective).
- **Next Steps**:
  1. `python scripts/pubs/check_lane.py claim --owner <session name>`; `git pull --no-rebase`.
  2. Paper B: the author submits the revision on DergiPark by 2026-11-30; record the date and
     decision in the publication table and the paper's README.
  3. Decide the fate of `paper/b-rev1-runs` (Open with the author) and act on it.
  4. No rerun is planned. If one is ever needed: `scripts\paper_b_chain.ps1 -From <study>` and
     `py scripts\paper_b_sync.py --loop` on the experiment laptop.
- **Blockers/Issues**:
  - None for the runs. Disclosed limits: the 6 Anchors timeouts above; the timing pass ran
    under the "ASUS Recommended" power plan (recorded per cell); the `cpu_ms` SHAP-LIME mixed
    model is degenerate (CPU time is descriptive only; H2 is tested in wall time, C-038).
  - Zero vectors: 5.8% (LIME) and 6.3% (full LIME) of Adult vectors are near zero (all |w| <
    1e-4); 2.7% are exactly zero. Do not quote 2.7% as the near-zero share.
  - `tests/analysis/test_stats.py` and `test_visualization.py` still fail at collection; not
    investigated.
- **Notes**:
  - Experiment laptop: use `.venv\Scripts\python.exe` (system Python lacks psutil). The
    timing gate needs other CPU <= 10%, the user idle 5 min (unless `--no-require-idle`) and AC
    power; an open dashboard tab can hold it.
  - PowerShell `Set-Content -Encoding utf8` writes a BOM that breaks `config_hash`: write
    configs with Python or `-Encoding ascii`.
  - Study configs are generated by `scripts/paper_b_studies.py`; a drift test keeps their
    `resources` table equal to the cohort's. `resources`/`sync` are outside the design hash;
    `[timing]` is inside it.
  - `gh` is not on PATH on the experiment laptop; pull requests are opened from the web.
