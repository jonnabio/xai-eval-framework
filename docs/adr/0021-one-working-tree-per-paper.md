# ADR-0021: One Working Tree per Paper

> **Status:** Accepted<br>
> **Date:** 2026-10-03<br>
> **Amends:** [ADR-0013](0013-publication-branching-model.md) (adds lanes for Papers D, E
> and F); [ADR-0019](0019-paper-bc-venue-peerj-and-single-working-folder.md) decisions 7
> and 8 (one working folder) now apply to Paper B+C only<br>
> **Related:** [RCA-001](../rca/RCA-001-manuscript-artifact-drift.md),
> `docs/context/ACTIVE_CONTEXT.md` (handoff of 2026-10-03)

---

## Context

On 2026-10-03 three papers were in progress at once: Paper D (complete, awaiting
submission), Paper E (results, no manuscript) and Paper F (plan only). Two agent sessions
worked in the same folder and on the same branches at the same time. The result was a
Paper E branch that also carried Paper D, a merge of that branch into `main` followed by
its revert, and Paper F documents left untracked on disk. `main` had to be rebuilt.

ADR-0019 had removed the separate Paper B+C working tree because the author could not
find the paper's files in the main folder: they existed only in the other folder until
merged. Any return to separate folders has to prevent that.

## Decision

1. **Each paper in progress has its own branch and its own folder** (author decision,
   2026-10-03):

   | Paper | Folder | Branch | Paths the lane owns |
   |---|---|---|---|
   | Thesis | `xai-eval-framework` (main folder) | `thesis/rca-001-phase-2` | `thesis/**` |
   | CIFIE chapter | `../xai-chapter` | `chapter/cifie-sync-2026-09` | `publications/book_chapters/2026_cifie_xai_fom7/**` |
   | EXP4 cohort 2 | `../xai-exp4` | `results/exp4-cohort2` | `experiments/exp4_cohort2/**`, `outputs/analysis/exp4_cohort2/**` |
   | Paper D | `../xai-paper-d` | `paper-d/tecnologia-en-marcha` | `docs/reports/paper_d/**`, `outputs/analysis/paper_d/**`, the Paper D scripts |
   | Paper E | `../xai-paper-e` | `paper/e-feature-agreement` | `docs/reports/paper_e/**`, `outputs/analysis/paper_e/**`, the Paper E scripts and tests |
   | Paper F | `../xai-paper-f` | `paper/f-external-validity` | `docs/reports/paper_f/**`, `outputs/analysis/paper_f/**` |
   | Paper B+C | main folder, short-lived `paper/bc-<topic>` branch | (created when needed) | `docs/reports/paper_bc/**` |

   Paper D keeps its existing branch name, which predates this ADR.
2. **A lane edits only the paths it owns.** Everything else is shared and changes only
   through `main`: `pub/**`, `scripts/pubs/**` (except a paper's own scripts),
   `docs/rca/**`, `docs/adr/**`, `docs/context/ACTIVE_CONTEXT.md`, `src/**`, and
   experiment runners used by more than one paper (for example
   `scripts/run_exp3_lime.py`).
3. **A shared change is its own commit and reaches `main` in the session that makes
   it.** Every other lane then takes `main` (fast-forward or merge) before its next
   edit. This is ADR-0013's rule, unchanged.
4. **Finished paper work is merged into `main` in the same session, and the main folder
   is then updated from `main`.** This is what keeps every paper's files visible in the
   main folder and answers the problem recorded in ADR-0019.
5. **Lanes never merge into each other.** A paper that needs another paper's files gets
   them from `main`.
6. **One agent session per folder, and never two sessions on one branch.** Sessions in
   different folders may run at the same time. `main` is not checked out in any folder
   for work.
7. **`ACTIVE_CONTEXT.md` is edited once per session, at the end**, after taking `main`,
   in a commit that contains nothing else. It is the file most likely to conflict.
8. **A paper's working tree is removed when the paper is published** or abandoned, after
   its branch is merged into `main`.

## Consequences

- Two papers can be edited, built and verified at the same time without one checkout
  seeing the other's half-finished files.
- A new working tree lacks the files git ignores. Seed it from the main folder:
  `cp -rn .ace/. <folder>/.ace/` and, for LaTeX builds, `tools/tectonic-portable/`. The
  Python environment is the main folder's `.venv`, called by path.
- Disk use grows by one checkout per paper.
- The rule in decision 4 depends on discipline. A check that a lane's commit touches
  only its own paths is not built yet; plan task 8
  (`scripts/pubs/check_substrate_current.py`) is the place for it.
- Paper B+C stays in the main folder under ADR-0019 until the author asks for a
  separate folder for it.
