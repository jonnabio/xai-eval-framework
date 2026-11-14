# Paper G — Run protocol (Linux run host, reporting through GitHub)

**Status:** Version 1, 2026-11-13. Author decision of the same day: the experiments run on a
separate **Linux laptop**. All logging and all information about the run reach the author and
the documentation laptop **through GitHub only**. No file is copied by hand between machines.

## 1. Roles of the machines

| Machine | Does | Never does |
|---|---|---|
| **Linux run host** | runs the pilot and the full run; commits snapshots, logs and status to `paper/g-runs` | edits documents; commits outside the lane's paths; analyses results |
| Documentation laptop (Windows, `C:\Users\jonna\Github`) | writes code, plan and paper on `paper/g-metric-agreement`; reads the run's progress from GitHub | runs experiments |
| Experiment laptop (Windows, Paper B) | nothing for Paper G | — |

## 2. Branches

- `paper/g-metric-agreement`: code, configuration, tests, documents. Merged to `main` by pull
  request when a step is complete.
- `paper/g-runs`: created from `main` once the code is merged. **Only the run host commits to
  it.** It carries only lane paths: `outputs/analysis/paper_g/**` and `experiments/exp_g/**`.
  The lane guard (`check_lane.py --staged`) runs before every automatic commit; a commit that
  fails it is not made, and the failure is reported (section 6).
- Each lane branch is merged into `main` by pull request after the run, and only then analysed
  (results are analysed once, as for Paper F).

## 3. Set-up of the run host (once)

1. Clone into a folder named `xai-eval-framework` (the lane registry checks the folder name).
2. Python **3.13**, the version of the project environment (3.13.15 on the documentation
   laptop), installed with `uv` so that it does not depend on the system Python of Ubuntu:
   `uv python install 3.13 && uv venv --python 3.13 .venv && uv pip install -r requirements-frozen.txt`.
   The pinned packages (numpy 2.2.6, scikit-learn 1.7.1, shap 0.50.0, xgboost 3.1.2) may not
   have wheels for a newer Python. Any Linux-only difference is recorded in
   `experiments/exp_g/ENVIRONMENT.md`, not patched silently.
3. GitHub access: `gh auth login` with the author's account (author, 2026-11-13). No token is
   written into any file of the repository.
4. `git config user.name` and `user.email` set to the author's commit identity.
5. Power: no sleep, no suspend on lid close, automatic updates paused for the run.
6. `python scripts/paper_g_host_check.py` writes `experiments/exp_g/host.json` (OS, kernel, CPU
   model, cores, RAM, Python version, package versions, git commit) and commits it. Every result
   row also carries the host id and the git commit it was produced with.

## 4. Running

| Command (run host) | Does |
|---|---|
| `scripts/paper_g_run.py --stage pilot` | the pilot (1 dataset, 4 models, 1 seed, 20 instances); its outputs are marked `pilot` and are not results |
| `scripts/paper_g_run.py --stage full --jobs 8` | the full run, in shards of dataset × model × seed; resumable |
| `scripts/paper_g_run.py --stage roar --jobs 8` | the ROAR-lite retrainings |
| `scripts/paper_g_run.py --stage synthetic` | the synthetic ground-truth check |

The run is started inside `tmux` (or as a `systemd --user` service), so that it survives
closing the terminal or an SSH session. A shard writes to a local, git-ignored work directory
and marks itself finished with a `.done` file. A shard that is interrupted restarts from the
beginning; finished shards are never recomputed.

## 5. What reaches GitHub, and when

A publisher (`scripts/paper_g_publish.py`) runs every **15 minutes** (systemd timer or cron)
and once at the end of each stage. Each time it:

1. copies every newly finished shard to `outputs/analysis/paper_g/raw/<stage>/<dataset>/<model>/seed_<s>.jsonl.gz`,
   unchanged, and adds it to `raw/MANIFEST.csv` (rows, failed rows, SHA-256);
2. copies each shard's log to `outputs/analysis/paper_g/logs/<stage>/…log` (plain text,
   compressed if over 1 MB);
3. rewrites **`outputs/analysis/paper_g/STATUS.md`**, the single page to read the run from:
   - stage, shards done / total, per seed and per dataset;
   - started at, last heartbeat, estimated end (from measured shard times);
   - failures: count, the shards involved, the last error line of each;
   - host id, git commit, free disk;
   - **no metric value of any explainer** (results are not looked at before the run ends);
4. runs the lane guard on the staged files, commits as
   `data(paper-g): <stage> snapshot <date time> (<done>/<total>)`, and pushes.
   If the push fails (network), it retries at the next cycle; nothing is lost.

## 6. Notifications

One GitHub issue, **"Paper G run"**, is opened when the run host is set up. The publisher adds a
comment (via `gh`) only on events, not on every cycle:

- stage started; seed finished; stage finished;
- any shard failed (with the log path and the last error line);
- no heartbeat change for 60 minutes while a stage is running (stalled);
- push failing for more than 2 hours.

The author is notified by GitHub's normal notification. The documentation laptop reads the
same issue and `STATUS.md` with `git fetch` or `gh issue view`.

## 7. Rules

- The run host never commits a document, the plan, code or anything outside the two lane
  output paths. Code changes go through `paper/g-metric-agreement` → `main` → `git merge main`
  on `paper/g-runs` (with the run stopped), and the snapshot records the new commit.
- A result row carries: stage, dataset, model, explainer, seed, instance id, metric values,
  time, host id, git commit. Nothing is aggregated on the run host.
- Secrets: none in the repository. The OpenML cache and the work directory are git-ignored.
- Size: per-instance rows are gzip-compressed JSON lines; expected total under 200 MB (to be
  checked on the pilot). If larger, the author decides where the raw rows go (as with Paper B).

## 8. Code to write (step 3 of the plan)

`scripts/paper_g_host_check.py`, `scripts/paper_g_run.py`, `scripts/paper_g_publish.py`,
`scripts/paper_g_status.py` (builds `STATUS.md`; also usable on the documentation laptop), the
systemd unit and timer files under `experiments/exp_g/systemd/`, and tests in
`tests/analysis/test_paper_g_*.py` (resume, manifest, status page, guard refusal).

## 9. The run host (author, 2026-11-13)

| Item | Value |
|---|---|
| OS | Ubuntu 26.04 LTS |
| CPU | 13th Gen Intel Core i5-1335U: 10 cores (2 performance, 8 efficiency), 12 threads, 15 W class |
| RAM | 14 GiB total, about 9 GiB available |
| GitHub | `gh` logged in with the author's account |
| Free disk | to record in `host.json` (at least 5 GB wanted) |

Consequences:

- **Jobs: 6 by default**, not 8. A 15 W laptop CPU slows down when hot, and its two performance
  cores are shared. The pilot measures 4, 6 and 8 jobs and the fastest stable setting is used.
- **Memory:** each job is limited to one thread per library (`OMP_NUM_THREADS=1` and the same for
  MKL/OpenBLAS), so that six jobs use six threads and stay under about 6 GiB. The pilot records
  peak memory per job; the runner stops starting new jobs below 1.5 GiB of free memory.
- **Heat:** the laptop stands on a hard surface with its vents clear; `host.json` and the status page
  record CPU temperature where the sensors allow it.
- The machine-time estimate (about 1 to 2 days) was made for the Ryzen of Paper F; it is replaced by
  the pilot's measured figure.

## 10. Commands on the run host, in order

```sh
# once
sudo apt install -y git curl tmux gh
curl -LsSf https://astral.sh/uv/install.sh | sh
gh auth login                               # the author's account
git clone https://github.com/jonnabio/xai-eval-framework.git ~/xai-eval-framework
cd ~/xai-eval-framework
git switch paper/g-runs                      # created from main once the code is merged
uv python install 3.13
uv venv --python 3.13 .venv
uv pip install -r requirements-frozen.txt
.venv/bin/python scripts/paper_g_host_check.py   # must end without "HOST CHECK FAILED"
.venv/bin/python -m pytest tests/analysis/test_paper_g_metrics.py tests/analysis/test_paper_g_run.py -q
mkdir -p ~/.config/systemd/user && cp experiments/exp_g/systemd/* ~/.config/systemd/user/
systemctl --user daemon-reload
loginctl enable-linger "$USER"               # services keep running after logout
systemctl --user enable --now paper-g-publish.timer

# stages, one after the other
systemctl --user start paper-g-run@pilot
systemctl --user start paper-g-run@full      # after the pilot is reviewed
systemctl --user start paper-g-run@roar      # after full
systemctl --user start paper-g-run@synthetic

# watching
systemctl --user status paper-g-run@full
tail -f experiments/exp_g/work/logs/full_main.log
.venv/bin/python scripts/paper_g_run.py --stage full --list
```
