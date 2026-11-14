# Prompt: set up the Linux run host for Paper G

Paste the text below into an AI assistant that helps you on the Linux laptop: Claude Code
running on that laptop (it can run the commands itself) or a chat assistant (it guides you
step by step). Source of truth: `RUN_PROTOCOL.md` in this folder.

---

You are helping me set up a Linux laptop as the **run host** for a research experiment
("Paper G"). The machine only runs the experiment; it never edits code or documents. Work step
by step: run or give one step at a time, check its output, and stop and tell me if anything
fails or differs from what is expected below. Do not improvise fixes that change the
repository's code, configuration or package versions. If something cannot be done as written,
stop and explain what happened.

## The machine

- Ubuntu 26.04 LTS; Intel Core i5-1335U (10 cores, 12 threads, 15 W laptop CPU); 14 GiB RAM.
- GitHub: I log in with my own account through `gh`.

## Goal

1. Clone `https://github.com/jonnabio/xai-eval-framework` into `~/xai-eval-framework` (the
   folder name must be exactly `xai-eval-framework`) and work on branch `paper/g-runs` only.
2. Python **3.13** (not the system Python) installed with `uv`, packages exactly as pinned in
   `requirements-frozen.txt`.
3. The host check and the tests pass.
4. Two systemd **user** services installed: a publisher timer (every 15 min, pushes progress
   to GitHub) and the run service.
5. The **pilot** stage started. Not the full run: the full run starts only after the pilot has
   been reviewed.

## Steps

### 1. Power and updates (the run must not be interrupted)
- Settings → Power: never suspend automatically, on battery or plugged in.
- Lid close must not suspend: in `/etc/systemd/logind.conf` set `HandleLidSwitch=ignore`,
  `HandleLidSwitchExternalPower=ignore`, `HandleLidSwitchDocked=ignore`, then
  `sudo systemctl restart systemd-logind` (warn me first: this may end the graphical session).
- Pause automatic updates for the run: `sudo systemctl stop unattended-upgrades` and
  `sudo systemctl disable unattended-upgrades` (I re-enable it after the run).
- Check free disk: `df -h ~` (at least 5 GB wanted).

### 2. Tools
```sh
sudo apt update
sudo apt install -y git curl tmux gh lm-sensors
curl -LsSf https://astral.sh/uv/install.sh | sh
exec $SHELL -l        # so that uv is on PATH
uv --version
gh auth login         # GitHub.com, HTTPS, log in with a browser; my account
gh auth setup-git
git config --global user.name  "<my name as on GitHub>"
git config --global user.email "<my GitHub email>"
```
Ask me for the name and email; do not guess them.

### 3. Repository and environment
```sh
git clone https://github.com/jonnabio/xai-eval-framework.git ~/xai-eval-framework
cd ~/xai-eval-framework
git switch paper/g-runs
git log --oneline -1
uv python install 3.13
uv venv --python 3.13 .venv
uv pip install -r requirements-frozen.txt
```
If a package fails to install (some pins may be Windows-specific), stop and show me the error.
Do not change versions. If a Windows-only package is the only failure, tell me which; it may be
skipped and recorded in `experiments/exp_g/ENVIRONMENT.md`.

### 4. Checks
```sh
.venv/bin/python scripts/paper_g_host_check.py
.venv/bin/python -m pytest tests/analysis/test_paper_g_metrics.py tests/analysis/test_paper_g_run.py -q
.venv/bin/python scripts/pubs/check_lane.py status
```
Expected: the host check ends **without** "HOST CHECK FAILED" (Python 3.13.x, no
`pin_mismatches`); **23 passed**; lane status shows branch `paper/g-runs` and lane `paper-g`.
Show me the output of each.

### 5. Services
```sh
mkdir -p ~/.config/systemd/user
cp experiments/exp_g/systemd/* ~/.config/systemd/user/
systemctl --user daemon-reload
loginctl enable-linger "$USER"
.venv/bin/python scripts/pubs/check_lane.py claim --owner paper-g-run-host   # lane lock, needed by the publisher
systemctl --user enable --now paper-g-publish.timer
systemctl --user list-timers | grep paper-g
```
Then one publishing cycle by hand, to prove that GitHub access works:
```sh
.venv/bin/python scripts/paper_g_publish.py
git log --oneline -1
gh issue list --search '"Paper G run" in:title'
```
Expected: a commit `data(paper-g): … snapshot …` pushed to `paper/g-runs` (it carries
`host.json` and `STATUS.md`). If the publisher prints "refused", check the branch.

### 6. Start the pilot
```sh
systemctl --user start paper-g-run@pilot
systemctl --user status paper-g-run@pilot
tail -f experiments/exp_g/work/logs/pilot_main.log      # Ctrl+C to stop watching; the run continues
```
The pilot is 4 shards (Adult, 4 models, 1 seed, 20 instances). It should finish in minutes.
When it ends, run the publisher once more (`.venv/bin/python scripts/paper_g_publish.py`) and
tell me it is done. **Do not start the full run.** I will review the pilot first.

## Rules
- Never commit or push anything by hand. Only `paper_g_publish.py` commits, and only on
  `paper/g-runs`.
- Never edit files in the repository. To get new code: stop the run, `git pull` on
  `paper/g-runs` (I will say when), restart.
- Never print or store my GitHub token anywhere.
- Useful commands later: `.venv/bin/python scripts/paper_g_run.py --stage full --list`
  (state of each shard), `systemctl --user status paper-g-run@<stage>`,
  `journalctl --user -u paper-g-run@<stage>`, `sensors` (CPU temperature).
