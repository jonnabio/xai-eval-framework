#!/usr/bin/env python3
"""Paper F: progress dashboard of the run, for the Command Prompt.

    python scripts\\paper_f_monitor.py              refresh every 10 seconds, Ctrl+C to leave
    python scripts\\paper_f_monitor.py --every 5    another interval, in seconds
    python scripts\\paper_f_monitor.py --once       print once and exit

Standard library only; any Python 3.11+ runs it, the project environment is not needed.
It only reads: files of outputs/analysis/paper_f/runs/ and the list of processes. It never
starts, stops or changes anything, so it is safe to open and close at any time.

It shows progress, speed and failures. It shows no measure of any explanation method: the
results are analysed once, when the run is complete (analysis plan, section 7).

Time left is estimated from the work that remains, not from the count of conditions: the
seconds of every row (`total_s`) are read only to add them up per job. A condition that is
not finished is given the time the same condition took in another seed; when there is none,
the mean of its dataset and method, then of its method. The seeds run in order, and the
workers that a seed no longer needs take jobs of the next seed, so the end of a seed is
the time its work and the work of the seeds before it need together; the end of the last
seed is the end of the run.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import re
import subprocess
import sys
import time
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "analysis" / "paper_f"
RUNS = OUT / "runs"
CONFIG = ROOT / "docs" / "reports" / "paper_f" / "paper_f_config.toml"
EXPLAINERS = ("lime", "shap", "anchors", "dice")
MODELS = ("logreg", "rf", "xgb", "mlp")
RATE_WINDOW_H = 3.0
WORKERS = 8                 # jobs at once, as in paper_f_chain.py; read from the launcher when it runs
MIN_ROWS = 10               # rows a job needs before its own pace is used to estimate it

BOLD, DIM, GREEN, YELLOW, RED, CYAN, RESET = (
    "\x1b[1m", "\x1b[2m", "\x1b[32m", "\x1b[33m", "\x1b[31m", "\x1b[36m", "\x1b[0m")


def colour(text: str, code: str, on: bool) -> str:
    return f"{code}{text}{RESET}" if on else text


def bar(done: float, total: float, width: int = 30) -> str:
    filled = int(round(width * done / total)) if total else 0
    return "[" + "#" * filled + "." * (width - filled) + "]"


def duration(seconds: float) -> str:
    if seconds < 0 or seconds != seconds:
        return "-"
    h, m = divmod(int(seconds) // 60, 60)
    return f"{h // 24}d {h % 24:02d}h" if h >= 48 else f"{h}h {m:02d}m"


def count_lines(path: Path) -> tuple[int, int, float]:
    """Rows, failed rows and seconds of work of a job file, without parsing the values."""
    rows = failed = 0
    secs = 0.0
    key = b'"total_s": '
    try:
        with path.open("rb") as fh:
            for line in fh:
                if line.strip():
                    rows += 1
                    failed += b'"failed": 1' in line
                    i = line.rfind(key)
                    if i >= 0:
                        try:
                            x = float(line[i + len(key):].split(b",")[0].split(b"}")[0])
                        except ValueError:
                            continue
                        if x == x:
                            secs += x
    except OSError:
        pass
    return rows, failed, secs


def fail_reasons(path: Path) -> list[str]:
    reasons = []
    try:
        with path.open("rb") as fh:
            for line in fh:
                if b'"failed": 1' in line:
                    text = line.decode("utf-8", "replace")
                    key = '"fail_reason": "'
                    i = text.find(key)
                    reason = text[i + len(key):].split('"')[0] if i >= 0 else "?"
                    reasons.append("time limit" if "time limit" in reason
                                   else "no counterfactual" if "dice" in reason.lower()
                                   else reason[:40])
    except OSError:
        pass
    return reasons


def launchers_alive() -> tuple[int | None, int]:
    """Number of launcher processes (two per launcher; None when it cannot be read) and
    the number of jobs the launcher runs at once."""
    cmd = ("Get-CimInstance Win32_Process -Filter \"name like 'python%'\" | "
           "Where-Object { $_.CommandLine -match 'paper_f_run.py launch' } | "
           "ForEach-Object { $_.CommandLine }")
    try:
        out = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True,
                             text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None, WORKERS
    if out.returncode != 0:
        return None, WORKERS
    found = [line for line in out.stdout.splitlines() if "paper_f_run.py" in line]
    workers = WORKERS
    for line in found:
        m = re.search(r"--workers\s+(\d+)", line)
        if m and int(m.group(1)) > 0:
            workers = int(m.group(1))
    return len(found), workers


def time_left(snap: dict, workers: int) -> dict | None:
    """Per seed: (hours of work left, seconds from now until its end). None while no job
    is far enough to estimate from."""
    n_inst, jobs = snap["n_inst"], snap["jobs"]
    pools: dict[tuple, list[float]] = {}
    own = {}
    for (seed, d, m, e), (rows, secs, done) in jobs.items():
        if not rows or not (done or rows >= MIN_ROWS):
            continue
        full = secs if done else secs / rows * n_inst
        own[(seed, d, m, e)] = full
        for key in ((d, m, e), (d, e), (e,), ()):
            pools.setdefault(key, []).append(full)
    if not pools:
        return None
    mean = {k: sum(v) / len(v) for k, v in pools.items()}
    out = {}
    before = 0.0                 # work of the seeds before this one, which is done first
    for seed in snap["seeds"]:
        work = longest = 0.0
        for d in snap["datasets"]:
            for m in MODELS:
                for e in EXPLAINERS:
                    rows, _, done = jobs.get((seed, d, m, e), (0, 0.0, False))
                    if done:
                        continue
                    full = own.get((seed, d, m, e))
                    if full is None:
                        full = next(mean[k] for k in ((d, m, e), (d, e), (e,), ()) if k in mean)
                    left = full * max(0.0, 1 - rows / n_inst)
                    work += left
                    longest = max(longest, left)
        # A seed cannot end before its longest job, however many jobs run at once.
        before += work
        out[seed] = (work / 3600, max(before / workers, longest))
    return out


def memory_free_gb() -> float | None:
    if sys.platform != "win32":
        return None
    import ctypes

    class Status(ctypes.Structure):
        _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong)] + [
            (n, ctypes.c_ulonglong) for n in ("total", "avail", "tp", "ap", "tv", "av", "ax")]
    s = Status()
    s.length = ctypes.sizeof(Status)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(s))
    return s.avail / 2**30


def snapshot(cache: dict) -> dict:
    with CONFIG.open("rb") as fh:
        cfg = tomllib.load(fh)
    with (OUT / "datasets.csv").open(encoding="utf-8") as fh:
        datasets = [r["key"] for r in csv.DictReader(fh)]
    per_seed = len(datasets) * len(MODELS) * len(EXPLAINERS)
    n_inst = cfg["n_instances"]
    now = time.time()
    seeds = {s: {"done": 0, "rows": 0, "failed": 0, "recent": 0, "by_expl": dict.fromkeys(EXPLAINERS, 0),
                 "by_data": dict.fromkeys(datasets, 0)} for s in cfg["seeds"]}
    active, reasons, jobs = [], {}, {}
    for path in RUNS.glob("*/*/seed_*/*.jsonl"):
        dataset, model, seed_dir = path.relative_to(RUNS).parts[:3]
        seed = int(seed_dir.removeprefix("seed_"))
        if seed not in seeds:
            continue
        marker = path.with_suffix(".done")
        stat = path.stat()
        key = (str(path), stat.st_size)
        if key not in cache:                      # count a file again only when it grew
            cache[key] = (count_lines(path), fail_reasons(path))
        (rows, failed, secs), why = cache[key]
        jobs[(seed, dataset, model, path.stem)] = (rows, secs, marker.exists())
        s = seeds[seed]
        s["rows"] += rows
        s["failed"] += failed
        for r in why:
            reasons[(path.stem, r)] = reasons.get((path.stem, r), 0) + 1
        if marker.exists():
            s["done"] += 1
            s["by_expl"][path.stem] += 1
            if dataset in s["by_data"]:
                s["by_data"][dataset] += 1
            if now - marker.stat().st_mtime < RATE_WINDOW_H * 3600:
                s["recent"] += 1
        elif path.with_suffix(".heartbeat").exists() or now - stat.st_mtime < 1800:
            beat = path.with_suffix(".heartbeat")
            started = None
            if beat.exists():
                try:
                    started = beat.stat().st_mtime
                except OSError:
                    pass
            active.append({"name": f"{dataset} / {model} / {path.stem}", "seed": seed,
                           "rows": rows, "last": now - stat.st_mtime,
                           "on_instance": now - started if started else None})
    return {"cfg": cfg, "datasets": datasets, "per_seed": per_seed, "n_inst": n_inst,
            "seeds": seeds, "active": sorted(active, key=lambda a: a["name"]),
            "reasons": reasons, "jobs": jobs, "now": now}


def render(snap: dict, alive: int | None, workers: int, use_colour: bool) -> str:
    c = lambda t, code: colour(t, code, use_colour)  # noqa: E731
    seeds, per_seed, n_inst = snap["seeds"], snap["per_seed"], snap["n_inst"]
    limit = snap["cfg"]["run"]["time_limit_s"]
    lines = [c("PAPER F  -  How Dataset-Dependent Are Tabular Explainability Benchmarks?", BOLD),
             f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}   16 datasets x 4 models x 4 methods "
             f"= {per_seed} conditions per seed, {n_inst} instances each", ""]

    current = next((s for s in seeds if seeds[s]["done"] < per_seed), None)
    total_done = sum(v["done"] for v in seeds.values())
    total_rows = sum(v["rows"] for v in seeds.values())
    total_failed = sum(v["failed"] for v in seeds.values())
    recent = sum(v["recent"] for v in seeds.values())
    rate = recent / RATE_WINDOW_H                     # conditions per hour, last hours

    left = time_left(snap, workers)
    ends, at = {}, dt.datetime.now()
    if left is not None:
        for s in seeds:
            if seeds[s]["done"] < per_seed:
                # A seed does not end before the seed in front of it.
                at = max(at, dt.datetime.now() + dt.timedelta(seconds=left[s][1]))
                ends[s] = at

    lines.append(c("SEEDS", BOLD) + c("   conditions done, methods done of "
                                      f"{per_seed // len(EXPLAINERS)} each, estimated end", DIM))
    at_work = {a["seed"] for a in snap["active"]}
    for s, v in seeds.items():
        pct = 100 * v["done"] / per_seed
        state = (c("complete", GREEN) if v["done"] >= per_seed
                 else c("running ", CYAN) if s in at_work
                 else c("waiting ", DIM))
        end = f"  ends {ends[s]:%a %d %b %H:%M}" if s in ends else ""
        methods = " ".join(f"{e[0].upper()}{v['by_expl'][e]:>2}" for e in EXPLAINERS)
        lines.append(f"  seed {s:>6}  {bar(v['done'], per_seed, 20)} {v['done']:>3}/{per_seed} "
                     f"{pct:5.1f}%  {methods}  {state}{end}")
    all_total = per_seed * len(seeds)
    lines.append(f"  {'all':>11}  {bar(total_done, all_total, 20)} {total_done:>4}/{all_total} "
                 f"{100 * total_done / all_total:5.1f}%  rows {total_rows:,}")
    lines.append(c("  " + ", ".join(f"{e[0].upper()} = {e}" for e in EXPLAINERS), DIM))
    lines.append("")

    lines.append(c("TIME LEFT", BOLD)
                 + c(f"   (from the work that remains, {workers} jobs at once)", DIM))
    if current is None:
        lines.append(c("  every seed is complete", GREEN))
    elif left is None:
        lines.append("  no job is far enough to estimate from yet; wait for the first ones")
    else:
        now = dt.datetime.now()
        work_all = sum(left[s][0] for s in ends)
        last = list(ends)[-1]
        lines.append(f"  seed {current}: {duration((ends[current] - now).total_seconds())} left, "
                     f"about {ends[current]:%a %d %b %H:%M}   "
                     f"({left[current][0]:,.0f} job-hours of work)")
        three = [s for s in list(seeds)[:3] if s in ends]
        if three and len(seeds) > 3:
            lines.append(f"  three seeds (fallback): {duration((ends[three[-1]] - now).total_seconds())} "
                         f"left, about {ends[three[-1]]:%a %d %b %H:%M}")
        lines.append(c(f"  ALL {len(seeds)} SEEDS: {duration((ends[last] - now).total_seconds())} left, "
                       f"about {ends[last]:%a %d %b %H:%M}", BOLD)
                     + f"   ({work_all:,.0f} job-hours of work)")
        if rate > 0:
            by_count = now + dt.timedelta(seconds=(all_total - total_done) / rate * 3600)
            lines.append(c(f"  by the count of the last {RATE_WINDOW_H:.0f} hours "
                           f"({rate:.1f} conditions an hour): about {by_count:%a %d %b %H:%M}", DIM))
        lines.append(c("  It assumes the run is never stopped and the pace of the jobs stays as "
                       "measured.", DIM))
    lines.append("")

    if current is not None:
        v = seeds[current]
        each = per_seed // len(EXPLAINERS)
        lines.append(c(f"SEED {current} BY METHOD", BOLD))
        lines.append("  " + "   ".join(f"{e} {v['by_expl'][e]:>2}/{each}" for e in EXPLAINERS))
        lines.append(c(f"SEED {current} BY DATASET", BOLD) + c("   (16 conditions each)", DIM))
        items = [f"{d[:15]:<15} {n:>2}" for d, n in v["by_data"].items()]
        for i in range(0, len(items), 4):
            lines.append("  " + "   ".join(items[i:i + 4]))
        lines.append("")

    lines.append(c(f"JOBS AT WORK ({len(snap['active'])})", BOLD)
                 + c("   rows done of 200, time since the last row", DIM))
    for a in snap["active"]:
        wait = a["on_instance"] if a["on_instance"] is not None else a["last"]
        flag = ""
        if a["on_instance"] is None and a["last"] > 300:
            flag = c("  not started again yet", DIM)
        elif wait > 0.75 * limit:
            flag = c("  near the time limit", YELLOW)
        lines.append(f"  {a['name']:<38} seed {a['seed']:<6} {bar(a['rows'], n_inst, 12)} "
                     f"{a['rows']:>3}  {int(a['last'] // 60):>3} min{flag}")
    if not snap["active"]:
        lines.append(c("  none", YELLOW))
    lines.append("")

    share = 100 * total_failed / total_rows if total_rows else 0
    lines.append(c("FAILED INSTANCES", BOLD) + f"   {total_failed} of {total_rows:,} rows ({share:.2f}%)")
    for (expl, why), n in sorted(snap["reasons"].items(), key=lambda kv: -kv[1])[:6]:
        lines.append(f"  {n:>4}  {expl:<8} {why}")
    lines.append("")

    lines.append(c("HEALTH", BOLD))
    if alive is None:
        launcher = c("could not be read", YELLOW)
    elif alive == 0:
        launcher = (c("none running", RED) + " (the scheduled task starts one within 10 minutes)"
                    if current is not None else c("none needed", GREEN))
    elif alive <= 2:
        launcher = c("running", GREEN)
    else:
        launcher = c(f"{alive // 2} launchers at once: there must be only one", RED)
    lines.append(f"  launcher: {launcher}")
    mem = memory_free_gb()
    if mem is not None:
        lines.append("  free memory: " + c(f"{mem:.1f} GB", RED if mem < 1 else YELLOW if mem < 2 else GREEN))
    if (RUNS / "_STOP").exists():
        lines.append(c("  STOP file present: no new seed will be started", YELLOW))
    chain = RUNS / "_chain.log"
    if chain.exists():
        last = chain.read_text(encoding="utf-8", errors="replace").strip().splitlines()[-1:]
        lines.append(c("  last chain event: " + (last[0] if last else "-"), DIM))
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--every", type=float, default=10.0, help="seconds between refreshes")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--no-colour", action="store_true")
    args = ap.parse_args()
    if not RUNS.exists():
        print(f"no run directory at {RUNS}")
        return 1
    use_colour = not args.no_colour and sys.stdout.isatty()
    if use_colour:
        os.system("")                              # turns on ANSI codes in the Windows console
    cache: dict = {}
    alive, workers, alive_at = None, WORKERS, 0.0
    try:
        while True:
            if time.time() - alive_at > 30:        # the process list is slow to read
                (alive, workers), alive_at = launchers_alive(), time.time()
            text = render(snapshot(cache), alive, workers, use_colour)
            if args.once:
                print(text)
                return 0
            sys.stdout.write("\x1b[2J\x1b[H" if use_colour else "\n" * 2)
            sys.stdout.write(text + "\n\n" + colour(
                f"refresh every {args.every:g} s   Ctrl+C to leave (the run is not touched)",
                DIM, use_colour) + "\n")
            sys.stdout.flush()
            time.sleep(args.every)
    except KeyboardInterrupt:
        print("\nmonitor closed; the run continues")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
