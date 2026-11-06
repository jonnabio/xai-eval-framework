# Implementation plan: cohort B2 runner, resource governor, sync and dashboard

**Status:** approved in substance by the author on 2026-11-06 ("OK", with these requirements:
careful resource measurement, no crash of the computer, defensive code, specific branching
with frequent commits and pushes, a plan for periods when the laptop cannot be used, and a
monitoring dashboard). Decision D-1 is changed to **a fresh cohort (B2)**, `REVISION_PLAN.md`.

## 1. What is built

| File (lane `paper-b`) | Role |
|---|---|
| `experiments/exp_b_rev1/cohort.toml` | The whole design in one file: datasets, models (explicit hyperparameters), explainers and variants, seeds, instance counts, metric settings, resource limits. Every run records its hash |
| `scripts/paper_b_lib.py` | Shared code: config, paths, atomic I/O, dataset preparation, model training and freezing, explainer factory, metrics (the `src/` classes, same settings as EXP2), host snapshot, resource helpers |
| `scripts/paper_b_run.py` | CLI: `preflight`, `prepare`, `job`, `timing`, `launch`, `launch-timing`, `pilot`, `status` |
| `scripts/paper_b_sync.py` | Copies live results into git on the runs branch (plumbing, no checkout) and pushes; one-shot or loop |
| `scripts/paper_b_dashboard.py` | Local web dashboard (`http://127.0.0.1:8765`), terminal view, and `STATUS.md` for GitHub |
| `scripts/paper_b_timing.py` | Re-timing of EXP2 cells (kept: it documents the EXP2 timing artifact, F7b) |
| `tests/analysis/test_paper_b_rev1.py` | Unit tests of the defensive parts |

`src/` is not changed: EXP2 depends on it. The runner calls its explainer wrappers, metric
classes and sampler directly.

## 2. Design rules

1. **Two passes.** The *quality pass* (fidelity, faithfulness gap, stability, sparsity) is
   host-independent and runs in parallel workers at below-normal priority. The *timing pass*
   runs alone, one process, one thread, pinned to one CPU, at normal priority, only when the
   host is quiet (§4).
2. **Timing is interleaved per cell.** A timing job takes one (dataset, model, seed) cell and
   explains each instance with every explainer in a rotating order (ABBA-like). Slow drift
   (heat, background load) then falls on all explainers alike. A fixed micro-benchmark runs
   between instances, and its time is recorded as a drift and throttling signal.
3. **Models are frozen before any run.** `prepare` trains every model from the explicit
   hyperparameters, writes it with `joblib` (compress=3), records SHA-256, size, leaves and
   depth in `experiments/exp_b_rev1/models/MANIFEST.csv`, and refuses a file over 50 MB
   (GitHub limit 100 MB). Every job checks the hash before it starts and stops on a mismatch.
   That is the regression guard for F7a.
4. **No timing through `ResourceGuard`** (F7b). Timeouts are handled by the orchestrator,
   which kills the worker process.
5. **Reproducible randomness.** Each instance seeds NumPy from (cohort seed, dataset, model,
   explainer, instance id), so a resumed job yields the same values. LIME's own
   `random_state` is the cohort seed, as in EXP2.

## 3. Defensive code

| Risk | Defence |
|---|---|
| Out of memory (freezes Windows) | Admission control: a worker starts only if the available RAM minus the expected peak of that job stays above a reserve (default 6 GB of 31.4). The expected peak is learned from earlier jobs of the same model × explainer (95th percentile of recorded peaks; conservative default 3 GB). Each worker is sampled every 2 s. Over its cap (default 8 GB) it is killed and its job retried alone. Under 3 GB available, admission pauses; under 1.5 GB, the newest worker is killed and requeued |
| CPU saturation, unusable laptop | Workers = min(config, logical CPUs − 2), default 4 of 12 threads. BELOW_NORMAL priority. BLAS/OpenMP threads = 1 per worker |
| Thermal throttling | CPU frequency and a fixed micro-benchmark recorded every few minutes. The dashboard warns when the benchmark slows by more than 15% from its first value |
| A hung explanation (Anchors, KernelSHAP-SVM) | Per-instance heartbeat file. Past the time limit the worker is killed, the instance is recorded as failed with the reason, and the job resumes after it (the Paper F pattern) |
| A crash, reboot or power cut | Results are appended one JSON line per instance, flushed and `fsync`ed. A job skips instances it already holds, so the same command resumes. A `.done` marker is written atomically (temporary file plus `os.replace`) |
| Sleep or hibernation mid-run | The orchestrator calls `SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` while it runs and restores it at exit |
| Running on battery | Preflight refuses to start without AC power; the orchestrator pauses admission if power is lost and resumes when it returns |
| Disk full | Preflight needs ≥ 10 GB free; the orchestrator pauses under 5 GB |
| Interrupt or closed console | Ctrl+C or the stop file `outputs/paper_b_rev1_live/_STOP`: no new job starts and running jobs finish their instance. A second Ctrl+C kills the workers; resume is always safe |
| Model or code changed mid-cohort | Every row carries the cohort config hash, the model SHA-256 and the git commit. The analysis refuses mixed hashes within a cohort |
| Lost data | `paper_b_sync.py --loop` commits the live results to `paper/b-rev1-runs` and pushes every 15 minutes (§5) |
| Timing contaminated by user activity | Quiet-host gate (§4) |

## 4. Quiet-host gate (timing pass only)

Before each timed instance, timing proceeds only if:
(a) no quality workers are running (the timing launcher refuses to start otherwise);
(b) system CPU use by other processes is under 10% over 2 s;
(c) optionally (`--require-idle`, on by default), no keyboard or mouse input for 5 minutes
    (Windows `GetLastInputInfo`);
(d) AC power.

Otherwise it waits, polls every 30 s, and records the wait. Touching the laptop pauses the
timing and never spoils it.

## 5. Branching and pushes

| Branch | Content | Who writes | Pushed |
|---|---|---|---|
| `main` | Released state | Pull requests only, merged by the author (the assistant's merges into `main` are blocked by the permission classifier) | — |
| `paper/b-ci-revision-1` | Code, configs, frozen models, docs, manuscript | Ordinary commits, by explicit path | After every commit |
| `paper/b-rev1-runs` | Results only: `experiments/exp_b_rev1/results/**`, `STATUS.md` | `paper_b_sync.py`, by git plumbing (temporary index, `commit-tree`, `update-ref`); the working branch is never switched | Every 15 min while running; never forced |
| `rca/004-exp2-provenance` | RCA-004 (shared files) | Ordinary commits | After every commit; pull request to `main` |

The runs branch is merged into the revision branch at each milestone (pilot, quality pass,
timing pass). Both are `paper/b-*` branches of the same lane, so the merge stays inside the
lane. The revision branch reaches `main` through a pull request at the end, or earlier if the
author wants a checkpoint.

## 6. Dashboard

`python scripts/paper_b_dashboard.py` serves `http://127.0.0.1:8765` (localhost only,
read-only, auto-refresh every 10 s) and writes `outputs/paper_b_rev1_live/STATUS.md`, which
the sync pushes, so progress can be read on GitHub from a phone. It shows:

- progress per pass, dataset, model and explainer, and the estimated time left;
- each worker: job, current instance, elapsed time, RSS, CPU;
- the host: CPU %, RAM, disk, AC or battery, CPU frequency, drift of the micro-benchmark;
- failures with their reasons; timing-gate waits;
- the last push to GitHub (commit and age), with a warning when older than 30 minutes.

It reads files and the process list only; opening or closing it never affects the run.

## 7. Tests

- the call counter (outermost calls only, inherited methods, `available_if` descriptors);
- append, fsync, resume and the atomic `.done` marker;
- admission control on simulated memory figures;
- the quiet-gate logic on simulated readings;
- the model hash check (mismatch stops the job);
- the sync on a temporary git repository: commit by plumbing, no change to HEAD or index,
  push refused without force;
- instance selection: per-stratum counts, determinism.

## 8. Order of work

1. This plan, the runbook and the code with tests; commit and push.
2. `preflight`, then `prepare`: data, model training and freezing; commit and push the
   models and manifest.
3. `pilot`: every dataset × model × explainer on 4 instances, quality and timing. It gives
   the time and peak memory per explanation and the budget table, by 2026-11-10.
4. Full quality pass, then the timing pass at night (§4); sync throughout.
