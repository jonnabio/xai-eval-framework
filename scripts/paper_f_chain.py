#!/usr/bin/env python3
"""Paper F: run the five parts (one per seed) one after another, without supervision.

    python scripts/paper_f_chain.py            # supervise until every seed is complete
    python scripts/paper_f_chain.py --ensure   # start the supervisor only if none is running
    python scripts/paper_f_chain.py --status   # one line per seed
    python scripts/paper_f_chain.py --tick     # one step, then exit (the scheduled task)

Since 2026-10-06 the run is driven by --tick from a Windows scheduled task every 10
minutes: a long-lived supervisor was found stopped in the morning without a trace, twice.
A tick keeps no process alive: if no launcher is running, it starts the launcher of the
first seed that is not complete. The count of launches per seed is kept in
runs/_chain_state.json.

For each seed, in the order of the configuration file:
  - if the seed is complete (one `.done` marker per condition), go to the next;
  - otherwise make sure exactly one launcher works on it (an already running launcher is
    adopted, never doubled) and wait for it to end;
  - a launcher that ends before the seed is complete is started again, up to MAX_RELAUNCH
    times; after that the seed is logged as incomplete and the chain goes on. Nothing is
    lost: the launcher is resumable and can be run again later.

It computes nothing itself and reads no result: it counts marker files and starts
`paper_f_run.py launch --seeds <seed>`. While it runs it asks Windows not to go to sleep
for being idle. To pause after the current part, create the file
outputs/analysis/paper_f/runs/_STOP ; delete it and run --ensure to go on.

Log: outputs/analysis/paper_f/runs/_chain.log
"""
from __future__ import annotations

import argparse
import ctypes
import datetime as dt
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_f_lib as lib  # noqa: E402

RUNS = lib.OUT / "runs"
LOG = RUNS / "_chain.log"
PID = RUNS / "_chain.pid"
STOP = RUNS / "_STOP"
WORKERS = 8
MAX_RELAUNCH = 6
POLL_S = 60
PYTHON = lib.ROOT / ".venv" / "Scripts" / "python.exe"


def log(text: str) -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    line = f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} {text}"
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line, flush=True)


def processes() -> list[tuple[int, str]]:
    """(pid, command line) of every python process, read through PowerShell."""
    cmd = ("Get-CimInstance Win32_Process -Filter \"name like 'python%'\" | "
           "ForEach-Object { \"$($_.ProcessId)`t$($_.CommandLine)\" }")
    out = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True,
                         text=True, encoding="utf-8", errors="replace").stdout
    rows = []
    for line in out.splitlines():
        pid, _, command = line.partition("\t")
        if pid.strip().isdigit():
            rows.append((int(pid), command))
    return rows


def launchers() -> list[tuple[int, str]]:
    return [(p, c) for p, c in processes() if "paper_f_run.py" in c and " launch" in c]


def supervisors() -> list[int]:
    # The environment's python.exe starts the real interpreter as a child with the same
    # command line, so this process and its parent are one supervisor.
    mine = {os.getpid(), os.getppid()}
    return [p for p, c in processes()
            if "paper_f_chain.py" in c and "--ensure" not in c and "--status" not in c
            and "--tick" not in c
            and p not in mine]


def conditions(cfg: dict) -> int:
    with (lib.OUT / "datasets.csv").open(encoding="utf-8") as fh:
        datasets = sum(1 for _ in fh) - 1
    return datasets * len(lib.MODELS) * len(lib.EXPLAINERS)


def done(seed: int) -> int:
    return sum(1 for _ in RUNS.glob(f"*/*/seed_{seed}/*.done"))


def keep_awake(on: bool) -> None:
    """Ask Windows not to sleep for being idle while this process lives."""
    if sys.platform != "win32":
        return
    ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | (ES_SYSTEM_REQUIRED if on else 0))


def start_launcher(seed: int) -> None:
    out = (RUNS / f"_launcher_seed{seed}.log").open("a", encoding="utf-8")
    err = (RUNS / f"_launcher_seed{seed}.err.log").open("a", encoding="utf-8")
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
    subprocess.Popen([str(PYTHON), "scripts/paper_f_run.py", "launch", "--workers", str(WORKERS),
                      "--seeds", str(seed)], cwd=lib.ROOT, stdout=out, stderr=err,
                     stdin=subprocess.DEVNULL, creationflags=flags)


def wait_no_launcher() -> None:
    while launchers():
        time.sleep(POLL_S)


def supervise() -> int:
    if supervisors():
        print("a supervisor is already running")
        return 0
    cfg = lib.config()
    total = conditions(cfg)
    PID.write_text(str(os.getpid()), encoding="ascii")
    keep_awake(True)
    log(f"chain started (pid {os.getpid()}); seeds {cfg['seeds']}; {total} conditions per seed")
    try:
        for seed in cfg["seeds"]:
            relaunches = 0
            while done(seed) < total:
                active = launchers()
                if active:
                    # A launcher is at work (on this seed or left from another): wait for it.
                    time.sleep(POLL_S)
                    continue
                if STOP.exists():
                    log(f"stop file found; chain paused before seed {seed} "
                        f"({done(seed)} of {total} done)")
                    return 0
                if relaunches >= MAX_RELAUNCH:
                    log(f"seed {seed} INCOMPLETE after {relaunches} launches: "
                        f"{done(seed)} of {total} done; going on to the next seed")
                    break
                relaunches += 1
                log(f"seed {seed}: {done(seed)} of {total} done; starting launcher "
                    f"(launch {relaunches})")
                start_launcher(seed)
                time.sleep(30)
            else:
                wait_no_launcher()
                log(f"seed {seed} complete: {done(seed)} of {total} conditions")
        log("chain finished: every seed was handled. The analysis is NOT run by the chain.")
    finally:
        keep_awake(False)
        PID.unlink(missing_ok=True)
    return 0


def ensure() -> int:
    if supervisors():
        return 0
    cfg = lib.config()
    total = conditions(cfg)
    if STOP.exists() or all(done(s) >= total for s in cfg["seeds"]):
        return 0
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
    out = (RUNS / "_chain.out.log").open("a", encoding="utf-8")
    subprocess.Popen([str(PYTHON), "scripts/paper_f_chain.py"], cwd=lib.ROOT, stdout=out,
                     stderr=out, stdin=subprocess.DEVNULL, creationflags=flags)
    log("supervisor started by --ensure")
    return 0


def tick() -> int:
    """One step: if nothing is running, start the launcher of the first incomplete seed."""
    import json
    if STOP.exists() or launchers() or supervisors():
        return 0
    cfg = lib.config()
    total = conditions(cfg)
    state_path = RUNS / "_chain_state.json"
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    for seed in cfg["seeds"]:
        n = done(seed)
        if n >= total:
            if not state.get(f"complete_{seed}"):
                state[f"complete_{seed}"] = True
                log(f"seed {seed} complete: {n} of {total} conditions")
            continue
        launches = state.get(str(seed), 0)
        if launches >= MAX_RELAUNCH:
            if not state.get(f"gave_up_{seed}"):
                state[f"gave_up_{seed}"] = True
                log(f"seed {seed} INCOMPLETE after {launches} launches: {n} of {total} done; "
                    "going on to the next seed")
            continue
        state[str(seed)] = launches + 1
        state_path.write_text(json.dumps(state, indent=1), encoding="utf-8")
        log(f"tick: seed {seed}: {n} of {total} done; starting launcher (launch {launches + 1})")
        start_launcher(seed)
        return 0
    state_path.write_text(json.dumps(state, indent=1), encoding="utf-8")
    return 0


def status() -> int:
    cfg = lib.config()
    total = conditions(cfg)
    for seed in cfg["seeds"]:
        print(f"seed {seed:>6}: {done(seed):3d} of {total} conditions done")
    print("supervisor:", "running" if supervisors() else "not running",
          "| launchers:", len(launchers()), "| stop file:", "yes" if STOP.exists() else "no")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ensure", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--tick", action="store_true")
    args = ap.parse_args()
    if args.status:
        return status()
    if args.tick:
        return tick()
    if args.ensure:
        return ensure()
    return supervise()


if __name__ == "__main__":
    raise SystemExit(main())
