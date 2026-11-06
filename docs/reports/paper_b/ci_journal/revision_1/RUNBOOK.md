# Runbook: running cohort B2 on this laptop

For the author. Commands are run from `D:\Github\xai-eval-framework` in a Command Prompt or
PowerShell, with the project environment: `.venv\Scripts\python.exe` (written `py` below).
Design: `experiments/exp_b_rev1/cohort.toml`. How it works: `RUNS_IMPLEMENTATION_PLAN.md`.

## 1. Before the first run (once)

1. **Power and sleep** (Settings → System → Power, or `powercfg`):
   - on AC: *Sleep = Never*, *Turn off screen = 10 min* (the screen may go off; the
     computer must not sleep). The runner also blocks sleep while it runs.
   - *When I close the lid* (Control Panel → Power Options) **on AC: Do nothing**, if the
     lid will be closed during runs.
2. **Windows Update:** Settings → Windows Update → *Pause updates for 2 weeks* (until
   2026-11-20 or later). A forced restart would stop the run. The run resumes, but hours
   can be lost.
3. **Cooling:** keep the vents free; a hard surface or a cooling pad. Heat slows the CPU,
   which matters for the timing pass. The dashboard warns when the micro-benchmark drifts.
4. **Charger connected.** The runner refuses to start on battery and pauses on battery.
5. Keep **at least 20 GB free** on D:.

## 2. Starting

Open three windows:

| Window | Command | Role |
|---|---|---|
| 1 | `py scripts\paper_b_run.py preflight` then `py scripts\paper_b_run.py launch` | The quality pass |
| 2 | `py scripts\paper_b_sync.py --loop` (already running in the background since 2026-11-06; see §9) | Every 15 min: saves the results to `paper/b-rev1-runs` and pushes the commits of `paper/b-ci-revision-1` |
| 3 | `py scripts\paper_b_dashboard.py` | Open http://127.0.0.1:8765 in a browser |

Order of the passes: `prepare` (once) → `pilot` → `pilot-timing` → `launch` → `launch-timing`.

## 3. Stopping and resuming

- **Stop cleanly:** Ctrl+C once in window 1. Each worker finishes its current instance, then
  stops. Or create the file `outputs\paper_b_rev1_live\_STOP` from anywhere.
- **Stop now:** Ctrl+C twice. The instance being computed is lost and recomputed later; nothing
  else is.
- **Resume:** delete `outputs\paper_b_rev1_live\_STOP` if it exists, and run the same
  command again. Finished instances are never recomputed. This also holds after a crash, a
  power cut or a restart.
- Keep window 2 (sync) running. On closing, it makes one last save.

## 4. Using the laptop while it runs

| Pass | Can I use the laptop? | What happens |
|---|---|---|
| `prepare` (training) | Light use only (browser, documents) | Uses several cores for some minutes per model |
| Quality pass (`pilot`, `launch`) | **Yes, light use.** Avoid heavy work (video calls, compiling, games) | Workers run at *below-normal* priority on at most 4 of the 12 threads, so the machine stays responsive. Heavy use only slows the run; it never changes a result (quality does not depend on speed) |
| Timing pass (`pilot-timing`, `launch-timing`) | **No.** Leave it alone, ideally overnight | The *quiet-host gate* pauses timing whenever you touch the keyboard or mouse (and for 5 minutes after), or when another program uses more than 10% CPU. Touching the laptop never spoils a measurement, but the pass waits |

## 5. If the laptop cannot be used during the experiments

The simplest plan keeps the two passes apart:

1. **Days: quality pass**, with you using the laptop lightly (§4). If you need the laptop
   for heavy work, stop the run cleanly (§3) and resume afterwards. Only time is lost.
2. **Nights: timing pass.** Start `launch-timing` when you finish for the day and leave the
   laptop on, plugged in, lid open (or *Do nothing* on lid close). It needs the laptop to
   itself. In the morning, Ctrl+C once.
3. **If you need the laptop all day for other work over several days**, the quality pass can
   run on another computer of yours (quality does not depend on the machine). Only the
   timing pass must stay on this laptop. Ask before doing it: the models, data and code
   must be copied exactly, and the manifest hashes check that.
4. **A cloud machine** can also take the quality pass if needed; the timing pass stays here
   (D-7).

Estimated durations come from the pilot (by 2026-11-10) and will be written here.

## 6. Watching from elsewhere

`paper_b_sync.py` pushes `STATUS.md` with every save. Open the repository on GitHub, branch
**`paper/b-rev1-runs`**, file `experiments/exp_b_rev1/results/STATUS.md`. It shows progress,
failures and the last save time, and it works from a phone. It is never more than 15 minutes
old while the sync runs.

## 7. What the warnings mean

| Dashboard warning | Do |
|---|---|
| Orchestrator not running, jobs queued | Run `launch` again (it resumes) |
| On battery | Connect the charger; the run continues by itself |
| Low RAM | Nothing; admission pauses by itself. If it persists, close other programs |
| Throttling suspected | Check ventilation; for the timing pass, wait until the laptop cools |
| No push for 30 minutes | Check window 2; run `py scripts\paper_b_sync.py` once by hand |
| Push refused (remote moved) | Do not force. Tell the assistant: someone pushed to the runs branch |
| Jobs failed for good | Note them; the assistant decides (retry, or report as a failure of the method) |

## 8. Branches (nothing here touches `main`)

| Branch | Content |
|---|---|
| `paper/b-ci-revision-1` | Code, configuration, frozen models, documents, manuscript |
| `paper/b-rev1-runs` | Results only, saved automatically every 15 minutes |
| `main` | Reached only through pull requests that the author merges |

## 9. The background save loop

Since 2026-11-06 the save loop runs as a hidden background process, started with:

```powershell
Start-Process -WindowStyle Hidden -FilePath .venv\Scripts\python.exe `
  -ArgumentList "scripts\paper_b_sync.py","--loop" `
  -RedirectStandardOutput outputs\paper_b_rev1_live\_logs\sync.log `
  -RedirectStandardError outputs\paper_b_rev1_live\_logs\sync.err.log
```

Every 15 minutes it (1) copies the live results to `paper/b-rev1-runs` and pushes it, and
(2) pushes any new commits of `paper/b-ci-revision-1`. Pushes are never forced; only
committed work travels. The dashboard shows the last push.

- **Is it running?** The dashboard's "GitHub sync" tile, or `outputs\paper_b_rev1_live\_state\sync.json`
  (`loop_heartbeat` is refreshed every minute).
- **Stop it:** create the empty file `outputs\paper_b_rev1_live\_STOP_SYNC`. Within a minute it
  makes one last save and exits.
- **After a restart of Windows** it is not running: start it again with the command above.
