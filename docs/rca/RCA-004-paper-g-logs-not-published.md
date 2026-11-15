# RCA-004: Paper G publisher silently omits the run logs

**Status**: Closed (fix on `paper/g-metric-agreement`; the run host syncs after merge)
**Severity**: Medium (diagnostic data missing from GitHub; no observation lost or altered)
**Opened**: 2026-11-14
**Role**: Developer → Incident Responder
**Related**: [RCA-001](RCA-001-manuscript-artifact-drift.md) (the same class:
a `.gitignore` rule silently keeping required artifacts out of the
repository); `docs/reports/paper_g/RUN_PROTOCOL.md` section 5

## Symptoms

The Paper G Linux pilot completed:

- four shards, zero failed observations;
- raw shards, `raw/MANIFEST.csv` and `STATUS.md` published to `paper/g-runs`;
- issue notifications working.

But `outputs/analysis/paper_g/logs/` never reached GitHub. The publisher
copied the logs into the directory and printed `published: …` every cycle.

## Evidence

- `git check-ignore -v outputs/analysis/paper_g/logs/pilot/<shard>.log` →
  `.gitignore:54:logs/`.
- `.gitignore:77` (`*.log`, LaTeX build artifacts) matches every plain-text
  log a second time, so re-including the directory alone would still leave
  `.log` files out (git's last matching rule wins).
- `scripts/paper_g_publish.py` stages with `git add -- outputs/analysis/paper_g`.
  On a directory pathspec git skips ignored files without an error, so the
  commit held raw shards and `STATUS.md` but no logs, and `cycle` returned 0.
- `tests/analysis/test_paper_g_run.py` called no git at all: `copy_logs` was
  never exercised, and nothing checked what a publish actually commits.

## Root cause

1. **Why were no logs on GitHub?** They were never staged.
2. **Why?** `.gitignore` ignores every `logs/` directory and every `*.log`
   file, including the lane's publication directory.
3. **Why did the publisher report success?** It trusts `git add`, which skips
   ignored files under a directory pathspec without failing.
4. **Why did the tests not catch it?** The publisher's tests mocked git or ran
   no git, so no test committed into a repository with the real `.gitignore`.
5. **Why did review miss it?** RUN_PROTOCOL section 5 specifies the log copy,
   but nobody checked the destination against `.gitignore` (the RCA-001 lesson
   was applied to `outputs/*`, not to new publication paths).

**Root cause:** broad ignore rules (`logs/`, `*.log`) cover the publication
directory, and the publisher had no check that what it copied is what git
stages.

## Fixes (2026-11-14)

- **`.gitignore`:** a narrow exception, placed last so neither broad rule
  overrides it:
  `!outputs/analysis/paper_g/logs/` and `!outputs/analysis/paper_g/logs/**`.
  No other log directory is re-included.
  - `git check-ignore`: the paper_g logs, `.log.gz` included, are allowed;
    `logs/`, `experiments/exp_g/work/logs/`, other `outputs/analysis/*/logs/`
    and `docs/*.log` are still ignored.
- **`scripts/paper_g_publish.py`:**
  - `copy_logs` returns the published paths;
  - after staging, `ignored()` runs `git check-ignore` on them;
  - if any would be skipped, the cycle unstages everything, commits nothing,
    reports the event to the issue and exits 3 ("NOT published").
  - The lane guard, `STAGE_PATHS` and every metric, model and statistical
    procedure are unchanged.
- **Tests** in `tests/analysis/test_paper_g_run.py`, in an isolated temporary
  git repository with the real `.gitignore`:
  1. the pilot, shard and main logs are committed;
  2. unrelated logs stay ignored, and nothing outside
     `outputs/analysis/paper_g/` is committed;
  3. every published path belongs to the `paper-g` lane (real `lanes.toml`);
  4. with the pre-fix `.gitignore` the publisher exits 3, commits nothing and
     leaves nothing staged.
- **Negative-tested:** against the pre-fix `.gitignore`, tests 1 and 2 fail;
  with the fix all 12 tests pass.

## Effect on the pilot

None on the observations. The raw shards, the manifest and their SHA-256 are
untouched. After the run host syncs, the next publish commits the pilot logs
still present in the work directory.
