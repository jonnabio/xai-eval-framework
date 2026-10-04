# ADR-0021: One Working Tree per Paper

> **Status:** Accepted<br>
> **Date:** 2026-10-03 (amended the same day: Paper D moved to the main folder)<br>
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
   | Thesis | main folder (`xai-eval-framework`) | `thesis/rca-001-phase-2` | `thesis/**` |
   | CIFIE chapter | `../xai-chapter` | `chapter/cifie-sync-2026-09` | `publications/book_chapters/2026_cifie_xai_fom7/**` |
   | EXP4 cohort 2 | `../xai-exp4` | `results/exp4-cohort2` | `experiments/exp4_cohort2/**`, `outputs/analysis/exp4_cohort2/**` |
   | Paper E | main folder | `paper/e-feature-agreement` | `docs/reports/paper_e/**`, `outputs/analysis/paper_e/**`, the Paper E scripts and tests |
   | Paper F | `../xai-paper-f` | `paper/f-external-validity` | `docs/reports/paper_f/**`, `outputs/analysis/paper_f/**` |
   | Paper B+C | main folder | short-lived `paper/bc-<topic>` (created when needed) | `docs/reports/paper_bc/**` |
   | Paper D | main folder | `paper/d-tecnologia-en-marcha` | `docs/reports/paper_d/**`, `outputs/analysis/paper_d/**`, the Paper D scripts |

   **Amendment, 2026-10-03 (author decision):** Paper D is worked in the main folder,
   at `docs/reports/paper_d/`, like Paper B+C. Its separate folder `../xai-paper-d` was
   removed after a file comparison showed the main folder held the same files, and its
   branch `paper-d/tecnologia-en-marcha` is replaced by `paper/d-tecnologia-en-marcha`.
   The main folder therefore hosts three lanes (thesis, Paper B+C, Paper D) and has one
   of them checked out at a time: switch branch only with a clean tree, and return the
   folder to `thesis/rca-001-phase-2` when the paper session ends.

   **Amendment, 2026-10-03 (author decision): Paper E is worked in the main folder,**
   at `docs/reports/paper_e/`, on branch `paper/e-feature-agreement`. A session had
   followed the registry and written the Paper E manuscript in `../xai-paper-e`, where
   the author could not see it; the files were moved to the main folder the same
   session and `scripts/pubs/lanes.toml` now names the main folder for the lane. The
   folder `../xai-paper-e` holds nothing and is to be removed by the author
   (`git worktree remove ../xai-paper-e`). **Rule: a paper the author asks to work on
   is worked in the main folder, under `docs/reports/paper_<x>/`, unless the author
   names another folder in that session.** If the registry says otherwise, change the
   registry first; do not work in the other folder.
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
9. **Decisions 2, 3 and 6 are enforced by `scripts/pubs/check_lane.py`** (added
   2026-10-03). The lanes, folders and owned paths are in `scripts/pubs/lanes.toml`,
   which is the binding copy of the table above.
   - A session starts with `python scripts/pubs/check_lane.py claim --owner <name>` and
     ends with `release`. The claim fails when the branch is not a lane, when the lane
     is checked out in the wrong folder, when the lane has not taken `main`, or when
     another session holds the folder's lock. A lock expires 12 hours after its last
     commit.
   - The pre-commit hook (`.githooks/pre-commit`, enabled with
     `git config core.hooksPath .githooks`) refuses a commit that has no live lock,
     touches another lane's paths, or mixes lane paths with shared paths.
   - CI (`pubs-sync.yml`, job `lanes`) refuses a commit reaching `main` that changes the
     paths of two lanes or mixes lane paths with shared ones.

## Consequences

- Two papers can be edited, built and verified at the same time without one checkout
  seeing the other's half-finished files.
- A new working tree lacks the files git ignores. Seed it from the main folder:
  `cp -rn .ace/. <folder>/.ace/` and, for LaTeX builds, `tools/tectonic-portable/`. The
  Python environment is the main folder's `.venv`, called by path.
- Disk use grows by one checkout per paper.
- Decision 4 (merge finished paper work into `main` the same session) still depends on
  discipline; nothing checks it.
- The session lock is taken by the session itself. A session that skips `claim` is
  stopped at its first commit only when the folder has no live lock; it is not stopped
  from editing files. Git itself refuses to check out one branch in two folders.
- The hook is local and can be bypassed with `--no-verify`, which agents must not use.
  The CI job is the copy that cannot be bypassed, and it sees only what reaches `main`.
- Paper B+C and Paper D stay in the main folder until the author asks for a separate
  folder for either. Thesis work and those two papers cannot be edited at the same
  time, because they share one checkout.
