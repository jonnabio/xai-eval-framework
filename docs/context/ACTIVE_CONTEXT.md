# Active Context: XAI Evaluation Framework

> **This file holds the current state only. History is in the archive:
> [`docs/context/archive/README.md`](archive/README.md)** (index, one file per day).
> Read the archive when the task needs more than this file gives; when and how is
> rule CTX-3 of [`.ace/standards/context.md`](../../.ace/standards/context.md).
> Limit: 300 lines, checked in CI by `scripts/pubs/check_active_context.py`.

**Last updated:** 2026-10-12, by session `claude-2026-10-12-thesis-review`.

## Current objective

**Thesis review** (author, 2026-10-12). With every paper published or under review, the
open work of the project is the thesis. The folder is on the thesis lane
(`thesis/rca-001-phase-2`). The scope and form of the review are not yet set by the
author.

Standing thesis task, not finished: **Task 3 / RCA-001 Phase 2**, make each published
number exist in one place.

1. Coverage sweep, one file at a time. Enforced under `[coverage]` in
   `pub/claim_registry.toml`: chapters 3, 4, 5 and 6. Remaining: `apendices.qmd`, then
   `capitulo-1`, `capitulo-2`, `introduccion` and Paper A. Workflow: add the file on a
   `pubs/*` branch, triage with `verify_claims.py --coverage-report`, register or
   declare structural.
2. Then emit the registry values as LaTeX macros and Quarto inline values, and add a CI
   job that builds every output and fails on undefined references and crossref warnings.

Detail: archive `2026-09-04.md`, `2026-09-06.md` and `undated-state-sections.md`.

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
- `main` at `799720f70` (pull request #55) before this session's change; the thesis
  branch was fast-forwarded to it and pushed on 2026-10-12.
- Nothing is running: no task, no process.
- Verifiers at the last check (2026-10-12): `verify_claims.py` 1,308 claims, 33 files.

## Open with the author

1. Submission numbers of Papers C and D, and the date of Paper D's submission.
2. The final text of Paper F's comments to the editor (not shown to the session).
3. CIFIE: whether a corrected file goes to the editor after the package is rebuilt.
4. Thesis figures: commit `ba418a927` (a chapter session) rewrote three figures under
   `thesis/assets/figures/` and made `scripts/generate_spanish_thesis_figures.py` write
   to both the thesis and the chapter. Whether those figures are the wanted ones is not
   decided; the generator is to be separated on a `pubs/*` branch.
5. Branch protection on `main` (pull request and the checks required): agreed on
   2026-10-10, set by the author on GitHub; not confirmed as done.

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

## Latest handoff - 2026-10-12 (thesis review mode; context file split)

- **Completed**:
  - Folder moved from the Paper F lane to the thesis lane. The stale lock of
    `claude-2026-10-12-session-start` was released on the author's word.
  - **This file was split.** Its 76 sections (5,284 lines, 375 KB) were moved verbatim
    to `docs/context/archive/`, one file per day plus `undated-state-sections.md`, with
    an index. This file was rewritten as state only. New standard
    `.ace/standards/context.md` (loaded at every session start), a core rule in
    `.aceconfig`, and `scripts/pubs/check_active_context.py` in CI.
- **Current state**: branch `pubs/active-context-archive` holds the change; it reaches
  `main` by pull request, then the thesis lane takes `main`.
- **Next steps**:
  1. Merge the pull request; `git switch thesis/rca-001-phase-2`; `git merge main`;
     claim the lane.
  2. Begin the thesis review as the author directs. Review is the Scientific Advisor
     role: read-only on the manuscript, findings to `docs/review/`.
- **Blockers**: none.
