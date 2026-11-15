#!/usr/bin/env python3
"""Paper G: monitoring dashboard of the run (run host, read-only).

    python scripts/paper_g_dashboard.py              web page at http://127.0.0.1:8766
    python scripts/paper_g_dashboard.py --port 8800
    python scripts/paper_g_dashboard.py --text       terminal view, refreshed every 10 s
    python scripts/paper_g_dashboard.py --once       print once and exit

Read-only: it reads the work directory (shard markers, heartbeat, main and publisher logs),
raw/MANIFEST.csv, host.json, /proc and /sys, `git` on local refs and `systemctl --user show`.
It writes nothing, never calls the GitHub API, and never starts, stops or changes a run, so it
can be opened and closed at any time. Localhost only. Pattern: scripts/paper_b_dashboard.py.

It shows progress and health, never a result. Shard summaries are read through a whitelist
(the .done files also hold the model's test AUC); shard logs are never shown; the history
keeps only known operational lines of the main and publisher logs. RUN_PROTOCOL.md, section 11.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
import platform
import re
import shutil
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_g_lib as lib  # noqa: E402
import paper_g_run as run  # noqa: E402
import paper_g_status as status  # noqa: E402

PORT = 8766                       # Paper B uses 8765
RUN_BRANCH = "paper/g-runs"
SAFE_FIELDS = ("rows", "failed_rows", "seconds", "finished", "peak_rss_mib", "host", "commit",
               "error", "at")     # nothing else of a .done/.failed file is ever read out
LIVE_MIN = 2                      # heartbeat every <= 30 s; older than this is "late"
LOW_RAM_GIB = 2.0                 # the runner stops admitting jobs below 1.5 GiB
LOW_DISK_GIB = 5.0
HOT_C = 95.0                      # i5-1335U: high = crit = 100 C (sensors)
PUBLISH_STALE_MIN = 40            # the timer runs every 15 min
CACHE_S = 15

_cache: dict[str, tuple[float, object]] = {}
_cpu_prev: tuple[int, int] | None = None


def _cached(key: str, fn, ttl: float = CACHE_S):
    hit = _cache.get(key)
    if hit and time.monotonic() - hit[0] < ttl:
        return hit[1]
    val = fn()
    _cache[key] = (time.monotonic(), val)
    return val


def _cmd(*args: str) -> str | None:
    try:
        r = subprocess.run(list(args), cwd=lib.ROOT, capture_output=True, text=True, timeout=5)
        return r.stdout.strip() if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def git(*args: str) -> str | None:
    return _cached("git " + " ".join(args), lambda: _cmd("git", *args))


def systemd(unit: str) -> dict:
    """`systemctl --user show` of one unit; {} where systemd is not available."""
    def get():
        out = _cmd("systemctl", "--user", "show", unit, "-p", "ActiveState", "-p", "Result",
                   "-p", "ExecMainStatus", "-p", "LastTriggerUSec", "-p", "NextElapseUSecRealtime")
        return dict(line.split("=", 1) for line in (out or "").splitlines() if "=" in line)
    return _cached("systemd " + unit, get)


# --- small readers -----------------------------------------------------------------------

def _utc(stamp: str | None) -> datetime | None:
    if not stamp:
        return None
    try:
        t = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else t.astimezone(timezone.utc)


def _ago(t: datetime | None, now: datetime) -> str:
    if not t:
        return "never"
    d = (now - t).total_seconds()
    return f"{d:.0f} s ago" if d < 120 else f"{d / 60:.0f} min ago" if d < 7200 else f"{d / 3600:.1f} h ago"


def _dur(s: float | None) -> str:
    if s is None:
        return "—"
    return f"{s:.1f} s" if s < 120 else f"{s / 60:.1f} min" if s < 7200 else f"{s / 3600:.1f} h"


def _lines(path: Path, last: int = 400) -> list[str]:
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return [ln.rstrip("\n") for ln in fh.readlines()[-last:]]
    except OSError:
        return []


def _first_line(path: Path) -> str:
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.readline().strip()
    except OSError:
        return ""


def _safe(info: dict) -> dict:
    return {k: info[k] for k in SAFE_FIELDS if k in info}


# --- host (Linux /proc and /sys; None where not available) -----------------------------------

def _read_sys(path: str) -> str | None:
    try:
        return Path(path).read_text().strip()
    except OSError:
        return None


def cpu_percent() -> float | None:
    global _cpu_prev
    try:
        f = [int(x) for x in Path("/proc/stat").read_text().split("\n", 1)[0].split()[1:]]
    except (OSError, ValueError):
        return None
    idle, total = f[3] + (f[4] if len(f) > 4 else 0), sum(f)
    prev, _cpu_prev = _cpu_prev, (idle, total)
    if prev is None or total == prev[1]:
        return None
    return round(100 * (1 - (idle - prev[0]) / (total - prev[1])), 1)


SENSOR_GLOB = "/sys/class/thermal/thermal_zone*"


def cpu_temp_c() -> float | None:
    """Package temperature (x86_pkg_temp), else the hottest thermal zone; None if none."""
    temps = {}
    for z in sorted(Path("/").glob(SENSOR_GLOB.lstrip("/"))):
        t, v = _read_sys(f"{z}/type"), _read_sys(f"{z}/temp")
        if t and v and v.lstrip("-").isdigit():
            temps[t] = int(v) / 1000
    if not temps:
        return None
    return temps.get("x86_pkg_temp", max(temps.values()))


def throttle_count() -> int | None:
    v = _read_sys("/sys/devices/system/cpu/cpu0/thermal_throttle/package_throttle_count")
    return int(v) if v and v.isdigit() else None


def ac_power() -> bool | None:
    for p in Path("/sys/class/power_supply").glob("*"):
        if _read_sys(f"{p}/type") == "Mains":
            v = _read_sys(f"{p}/online")
            return None if v is None else v == "1"
    return None


def meminfo() -> dict:
    out = {}
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            k, v = line.split(":", 1)
            if k in ("MemTotal", "MemAvailable"):
                out[k] = int(v.split()[0]) / 1024**2
    except (OSError, ValueError):
        pass
    return out


def runner_alive(pid) -> bool:
    """The heartbeat's pid is a live paper_g_run.py process (not a reused pid)."""
    try:
        return b"paper_g_run.py" in Path(f"/proc/{int(pid)}/cmdline").read_bytes()
    except (OSError, ValueError, TypeError):
        return False


def pool_memory(pid) -> dict | None:
    """Live worker processes of the runner and their resident memory (no per-shard mapping)."""
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return None
    kids = []
    for p in Path("/proc").iterdir():
        if not p.name.isdigit():
            continue
        try:
            stat = (p / "stat").read_text()
            if int(stat.rsplit(")", 1)[1].split()[1]) != pid:
                continue
            rss = next((int(ln.split()[1]) for ln in (p / "status").read_text().splitlines()
                        if ln.startswith("VmRSS:")), 0)
            kids.append(rss / 1024)
        except (OSError, ValueError, IndexError):
            continue
    return {"processes": len(kids), "rss_mib": round(sum(kids), 1),
            "largest_mib": round(max(kids), 1) if kids else None}


def host_state() -> dict:
    mem = meminfo()
    disk = shutil.disk_usage(lib.ROOT)
    return {"hostname": platform.node(), "cpu_percent": cpu_percent(), "temp_c": cpu_temp_c(),
            "throttle_count": throttle_count(), "ac_power": ac_power(),
            "ram_total_gib": mem.get("MemTotal"), "ram_available_gib": mem.get("MemAvailable"),
            "disk_free_gib": disk.free / 1024**3, "python": platform.python_version(),
            "python_prefix": sys.prefix, "head": git("rev-parse", "--short=12", "HEAD"),
            "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
            "host_json": status._read(lib.ROOT / "experiments" / "exp_g" / "host.json") or {}}


# --- runner, stages, workers ----------------------------------------------------------------

def runner_state(cfg: dict, beat: dict, stages: dict, now: datetime) -> dict:
    """idle | running | late | stalled | stopped | interrupted | completed | failed."""
    stage = beat.get("stage")
    alive = runner_alive(beat.get("pid")) if beat else False
    age = status._age_min(beat.get("heartbeat"), now) if beat.get("heartbeat") else None
    pending = bool(beat.get("running")) or bool(beat.get("todo"))
    svc = systemd(f"paper-g-run@{stage}.service") if stage else {}
    all_done = all(s["done"] == s["total"] for s in stages.values())
    if not beat:
        state = "completed" if all_done else "idle"
    elif alive:
        state = "running" if age is not None and age <= LIVE_MIN else \
            "stalled" if age is not None and age > status.STALL_MINUTES else "late"
    elif pending:
        # Stopped on purpose (systemctl stop ends with Result=success) or ended unexpectedly.
        state = "stopped" if svc.get("Result") == "success" and svc.get("ActiveState") == "inactive" \
            else "interrupted"
    elif all_done:
        state = "completed"
    elif stages.get(stage, {}).get("failed"):
        state = "failed"
    else:
        state = "idle"
    return {"state": state, "stage": stage, "alive": alive, "heartbeat_age_min": age,
            "heartbeat": beat.get("heartbeat"), "started": beat.get("started"),
            "jobs": beat.get("jobs"), "max_jobs": cfg["run"]["jobs"], "commit": beat.get("commit"),
            "pid": beat.get("pid"), "service": svc, "running": beat.get("running") or [],
            "free_memory_gib": beat.get("free_memory_gib")}


def stage_table(cfg: dict, beat: dict) -> tuple[dict, dict]:
    state = status.collect(cfg)
    stages, cells = {}, {}
    for stage, rows in state.items():
        n = {k: sum(r["state"] == k for r in rows) for k in ("done", "failed", "todo")}
        secs = [r["info"].get("seconds") for r in rows if r["state"] == "done" and r["info"].get("seconds")]
        peaks = [r["info"].get("peak_rss_mib") for r in rows if r["info"].get("peak_rss_mib")]
        fins = [_utc(r["info"].get("finished")) for r in rows if r["state"] == "done"]
        starts = [f.timestamp() - (r["info"].get("seconds") or 0)
                  for f, r in zip(fins, [r for r in rows if r["state"] == "done"]) if f]
        active = beat.get("stage") == stage and (bool(beat.get("running")) or bool(beat.get("todo")))
        label = ("completed" if n["done"] == len(rows) else
                 "running" if active else
                 "not started" if n["done"] + n["failed"] == 0 else
                 "finished with failures" if n["failed"] and not n["todo"] else "partial")
        jobs = beat.get("jobs") or cfg["run"]["jobs"]
        stages[stage] = {
            "total": len(rows), "done": n["done"], "failed": n["failed"], "todo": n["todo"],
            "label": label, "median_s": statistics.median(secs) if secs else None,
            "peak_rss_mib": max(peaks) if peaks else None,
            "first_start": datetime.fromtimestamp(min(starts), timezone.utc).isoformat(timespec="seconds")
            if starts else None,
            "last_finish": max(fins).isoformat(timespec="seconds") if any(fins) else None,
            "eta_h": status.eta_hours(rows, jobs) if secs else None,
            "shards": [{"shard": r["shard"], "state": r["state"], **_safe(r["info"])} for r in rows
                       if r["state"] != "todo"]}
        table: dict[str, dict] = {}
        for r in rows:
            c = table.setdefault(f"{r['dataset']}|{r['model']}", {
                "dataset": r["dataset"], "model": r["model"], "seeds": set(), "done_seeds": set(),
                "shards": 0, "done": 0, "failed": 0, "secs": []})
            c["seeds"].add(r["seed"])
            c["shards"] += 1
            if r["state"] == "done":
                c["done"] += 1
                c["done_seeds"].add(r["seed"])
                if r["info"].get("seconds"):
                    c["secs"].append(r["info"]["seconds"])
            c["failed"] += r["state"] == "failed"
        cells[stage] = []
        for c in table.values():
            left = c["shards"] - c["done"]
            avg = sum(c["secs"]) / len(c["secs"]) if c["secs"] else None
            cells[stage].append({
                "dataset": c["dataset"], "model": c["model"], "done_seeds": len(c["done_seeds"]),
                "seeds": len(c["seeds"]), "done": c["done"], "shards": c["shards"],
                "failed": c["failed"], "avg_s": avg,
                # Serial compute still owed by this cell (median of its own shards x shards left).
                "left_s": statistics.median(c["secs"]) * left if c["secs"] and left else (0.0 if not left else None)})
    return stages, cells


def workers(cfg: dict, rs: dict, now: datetime) -> list[dict]:
    out = []
    for name in rs["running"]:
        parts = name.split("/")
        seed = parts[2].removeprefix("seed_") if len(parts) == 3 else None
        first = _first_line(run.work_dir(cfg) / "logs" / (rs["stage"] or "") / f"{name}.log")
        m = re.match(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d),\d+ INFO start ", first)
        started = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S").astimezone(timezone.utc) if m else None
        out.append({"shard": name, "dataset": parts[0], "model": parts[1] if len(parts) > 1 else None,
                    "seed": seed, "elapsed_s": (now - started).total_seconds() if started else None})
    return out


# --- publishing ---------------------------------------------------------------------------

PUB_RE = re.compile(r"^(\S+) (published|NOT published)(.*)$")


def publishing(cfg: dict, stages: dict, now: datetime) -> dict:
    log = _lines(run.work_dir(cfg) / "logs" / "publish.log")
    last_ok = last_bad = None
    for line in log:
        m = PUB_RE.match(line)
        if m and m.group(2) == "published":
            last_ok = (m.group(1), line)
        elif (m and m.group(2) == "NOT published") or line.startswith("refused"):
            last_bad = (m.group(1) if m else None, line)
    last_line = next((ln for ln in reversed(log) if PUB_RE.match(ln) or ln.startswith("refused")), None)
    events = status._read(run.work_dir(cfg) / "events.json") or {}
    remote = git("log", "-1", "--format=%h %cI %s", f"refs/remotes/origin/{RUN_BRANCH}")
    r_sha, r_time, r_subj = (remote.split(" ", 2) + [None, None, None])[:3] if remote else (None, None, None)
    ahead = git("rev-list", "--count", f"refs/remotes/origin/{RUN_BRANCH}..HEAD")
    manifest = set()
    try:
        with open(lib.OUT / "raw" / "MANIFEST.csv", encoding="utf-8") as fh:
            manifest = {r["path"] for r in csv.DictReader(fh)}
    except (OSError, KeyError):
        pass
    done = {f"{st}/{s['shard']}.jsonl.gz" for st, v in stages.items() for s in v["shards"]
            if s["state"] == "done"}
    tracked = set((git("ls-files", "outputs/analysis/paper_g/logs") or "").splitlines())
    no_log = sorted(p for p in manifest
                    if f"outputs/analysis/paper_g/logs/{p.removesuffix('.jsonl.gz')}.log" not in tracked
                    and f"outputs/analysis/paper_g/logs/{p.removesuffix('.jsonl.gz')}.log.gz" not in tracked)
    return {"timer": systemd("paper-g-publish.timer"), "service": systemd("paper-g-publish.service"),
            "last_ok": _utc(last_ok[0]).isoformat(timespec="seconds") if last_ok and _utc(last_ok[0]) else None,
            "last_ok_line": last_ok[1] if last_ok else None,
            "last_line": last_line, "last_bad": last_bad[1] if last_bad else None,
            "last_line_bad": bool(last_line and (last_line.startswith("refused") or " NOT published" in last_line)),
            "push_failing_since": events.get("push_failing_since"),
            "remote_sha": r_sha, "remote_time": r_time, "remote_subject": r_subj,
            "unpushed_commits": int(ahead) if ahead and ahead.isdigit() else None,
            "awaiting_copy": len(done - manifest), "manifest_shards": len(manifest),
            "published_without_log": no_log}


# --- history (whitelisted operational lines only) --------------------------------------------

HISTORY_RES = (
    (re.compile(r"^(\w+): (\d+) of (\d+) shards done; (\d+) to run with (\d+) jobs \(commit (\w+)\)$"),
     lambda m: (None, m.group(1), f"stage {m.group(1)} started: {m.group(4)} to run, {m.group(5)} jobs, "
                                  f"commit {m.group(6)}")),
    (re.compile(r"^(\S+Z) done (\S+) \((\d+)/(\d+), ([\d.]+) s\)$"),
     lambda m: (m.group(1), None, f"shard done {m.group(2)} ({m.group(3)}/{m.group(4)}, {m.group(5)} s)")),
    (re.compile(r"^(\S+Z) FAILED (\S+):"), lambda m: (m.group(1), None, f"shard FAILED {m.group(2)}")),
    (re.compile(r"^(\w+): finished; (\d+) done, (\d+) failed$"),
     lambda m: (None, m.group(1), f"stage {m.group(1)} finished: {m.group(2)} done, {m.group(3)} failed")),
)


def history(cfg: dict, limit: int = 40) -> list[dict]:
    out = []
    logs = run.work_dir(cfg) / "logs"
    for stage in run.STAGES:
        for line in _lines(logs / f"{stage}_main.log"):
            for rx, fn in HISTORY_RES:
                m = rx.match(line)
                if m:
                    t, _st, text = fn(m)
                    out.append({"time": t, "source": f"{stage} runner", "event": text,
                                "bad": "FAILED" in text or (" 0 failed" not in text and "finished" in text)})
                    break
    prev = None
    for line in _lines(logs / "publish.log"):
        m = PUB_RE.match(line)
        if m:
            ok = m.group(2) == "published"
            new = re.search(r"(\d+) new shard", line)
            if ok and new and new.group(1) == "0" and prev == "ok":
                continue            # quiet cycles are not events
            prev = "ok" if ok else "bad"
            out.append({"time": m.group(1), "source": "publisher",
                        "event": ("publisher succeeded" if ok else "publisher refused") + m.group(3)[:120],
                        "bad": not ok})
        elif line.startswith("refused"):
            prev = "bad"
            out.append({"time": None, "source": "publisher", "event": line[:160], "bad": True})
    return out[-limit:]


# --- state and warnings -------------------------------------------------------------------

def gather(now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    cfg = lib.config()
    beat = status._read(run.work_dir(cfg) / "heartbeat.json") or {}
    if not isinstance(beat, dict):
        beat = {}
    stages, cells = stage_table(cfg, beat)
    rs = runner_state(cfg, beat, stages, now)
    total = sum(s["total"] for s in stages.values())
    done = sum(s["done"] for s in stages.values())
    starts = [s["first_start"] for s in stages.values() if s["first_start"]]
    finishes = [s["last_finish"] for s in stages.values() if s["last_finish"]]
    first = _utc(min(starts)) if starts else None
    # Time spent running: up to now while a runner is alive, else up to the last finished shard.
    end = now if rs["alive"] or not finishes else _utc(max(finishes))
    remaining = [s for s in stages.values() if s["todo"] or s["failed"]]
    s = {"now": now.isoformat(timespec="seconds"), "runner": rs, "stages": stages, "cells": cells,
         "overall": {"done": done, "total": total,
                     "failed": sum(st["failed"] for st in stages.values()),
                     "running": len(rs["running"]),
                     "pending": total - done - sum(st["failed"] for st in stages.values()),
                     "first_start": first.isoformat(timespec="seconds") if first else None,
                     "elapsed_s": (end - first).total_seconds() if first and end else None,
                     # Only when every unfinished stage has its own timing evidence.
                     "eta_h": sum(st["eta_h"] for st in remaining)
                     if remaining and all(st["eta_h"] is not None for st in remaining) else
                     (0.0 if not remaining else None)},
         "workers": workers(cfg, rs, now),
         "pool": pool_memory(rs["pid"]) if rs["alive"] else None,
         "host": host_state(), "publishing": publishing(cfg, stages, now),
         "history": history(cfg)}
    s["missing_work_logs"] = [f"{st}/{sh['shard']}" for st, v in stages.items() for sh in v["shards"]
                              if not (run.work_dir(cfg) / "logs" / st / f"{sh['shard']}.log").exists()]
    s["warnings"] = warnings(s, now)
    return s


def warnings(s: dict, now: datetime) -> list[str]:
    w = []
    rs, h, p = s["runner"], s["host"], s["publishing"]
    if rs["state"] == "stalled":
        w.append(f"STALLED: the runner is alive but its heartbeat is {rs['heartbeat_age_min']:.0f} min old.")
    elif rs["state"] == "late":
        w.append(f"Heartbeat late: {rs['heartbeat_age_min']:.0f} min old (written every 30 s).")
    if rs["state"] == "interrupted":
        svc = rs["service"]
        w.append(f"Runner gone with shards still queued (stage {rs['stage']}): unexpected termination"
                 + (f" (service result {svc.get('Result')}, status {svc.get('ExecMainStatus')})" if svc else "")
                 + ". Restart the stage; finished shards are kept.")
    nf = s["overall"]["failed"]
    if nf:
        w.append(f"{nf} failed shard(s): see the failures list and the issue.")
    rows_failed = sum(sh.get("failed_rows") or 0 for st in s["stages"].values() for sh in st["shards"])
    if rows_failed:
        w.append(f"{rows_failed} failed explanation row(s) inside finished shards (kept and counted).")
    if h["ram_available_gib"] is not None and h["ram_available_gib"] < LOW_RAM_GIB:
        w.append(f"Low memory: {h['ram_available_gib']:.1f} GiB available (runner pauses admission below 1.5).")
    if h["disk_free_gib"] < LOW_DISK_GIB:
        w.append(f"Low disk: {h['disk_free_gib']:.1f} GiB free.")
    if h["temp_c"] is not None and h["temp_c"] >= HOT_C:
        w.append(f"CPU package at {h['temp_c']:.0f} °C (limit 100 °C): check the vents.")
    if h["ac_power"] is False:
        w.append("ON BATTERY: connect the charger.")
    if p["push_failing_since"]:
        w.append(f"Push to GitHub failing since {p['push_failing_since']}.")
    if p["last_line_bad"]:
        w.append(f"Last publisher cycle did not publish: {p['last_line'][:160]}")
    timer = p["timer"].get("ActiveState")
    if timer and timer != "active":
        w.append(f"Publisher timer is {timer}" + (" while a stage runs." if rs["alive"] else "."))
    last_ok = _utc(p["last_ok"])
    if timer == "active" and last_ok and (now - last_ok).total_seconds() > PUBLISH_STALE_MIN * 60:
        w.append(f"No successful publish for {_ago(last_ok, now)} (timer every 15 min).")
    if p["unpushed_commits"]:
        w.append(f"{p['unpushed_commits']} local commit(s) not on origin/{RUN_BRANCH} yet "
                 "(a local commit is not a push).")
    if p["published_without_log"]:
        w.append(f"{len(p['published_without_log'])} published shard(s) have no log in git "
                 f"(RCA-004), e.g. {p['published_without_log'][0]}.")
    if s["missing_work_logs"]:
        w.append(f"{len(s['missing_work_logs'])} finished shard(s) have no log in the work directory.")
    if h["branch"] and h["branch"] != RUN_BRANCH:
        w.append(f"This folder is on {h['branch']}, not {RUN_BRANCH}.")
    if not h["python"].startswith("3.13"):
        w.append(f"Python {h['python']}: the run uses 3.13 (.venv).")
    return w


def heartbeat() -> dict:
    """Cheap liveness for the heartbeat bar: no scan of shard markers."""
    cfg = lib.config()
    beat = status._read(run.work_dir(cfg) / "heartbeat.json") or {}
    now = datetime.now(timezone.utc)
    pub = [ln for ln in _lines(run.work_dir(cfg) / "logs" / "publish.log", 5) if PUB_RE.match(ln)]
    last = PUB_RE.match(pub[-1]) if pub else None
    return {"now": now.timestamp(),
            "runner": {"t": (_utc(beat.get("heartbeat")) or now).timestamp() if beat else None,
                       "alive": runner_alive(beat.get("pid")) if beat else False,
                       "label": f"{beat.get('stage', '')} · {len(beat.get('running') or [])} running · "
                                f"{beat.get('todo', '-')} queued" if beat else ""},
            "publisher": {"t": _utc(last.group(1)).timestamp() if last and _utc(last.group(1)) else None,
                          "ok": bool(last and last.group(2) == "published"),
                          "timer": systemd("paper-g-publish.timer").get("ActiveState", "")}}


# --- rendering ----------------------------------------------------------------------------

def _gib(x) -> str:
    return "not available" if x is None else f"{x:.1f} GiB"


def _hours(x) -> str:
    return "—" if x is None else f"{x:.1f} h"


def render_text(s: dict) -> str:
    rs, h, p, o = s["runner"], s["host"], s["publishing"], s["overall"]
    L = [f"Paper G run monitor - {s['now']} (read-only; no metric values)"]
    L += [f"  !! {w}" for w in s["warnings"]]
    L.append(f"Runner: {rs['state'].upper()}  stage {rs['stage'] or '-'}  heartbeat "
             f"{rs['heartbeat'] or 'never'}  workers {len(rs['running'])} running / {rs['jobs'] or '-'} "
             f"jobs (configured {rs['max_jobs']})")
    L.append(f"Overall: {o['done']}/{o['total']} shards, {o['failed']} failed, {o['pending']} pending; "
             f"elapsed {_dur(o['elapsed_s'])}; time left "
             + ("not estimable yet" if o["eta_h"] is None else f"{o['eta_h']:.1f} h"))
    for name, st in s["stages"].items():
        L.append(f"  {name:9} {st['done']:>3}/{st['total']:<3} failed {st['failed']:<3} {st['label']:22}"
                 f" median {_dur(st['median_s'])}  peak {st['peak_rss_mib'] or '-'} MiB")
    for wk in s["workers"]:
        L.append(f"  worker {wk['shard']:32} {_dur(wk['elapsed_s'])}")
    if s["pool"]:
        L.append(f"  worker processes: {s['pool']['processes']}, resident {s['pool']['rss_mib']:.0f} MiB")
    temp = "not available" if h["temp_c"] is None else f"{h['temp_c']:.0f} °C"
    power = {True: "AC", False: "BATTERY", None: "not available"}[h["ac_power"]]
    L.append(f"Host: {h['hostname']}  CPU {h['cpu_percent'] if h['cpu_percent'] is not None else '-'}%  "
             f"{temp}  RAM free {_gib(h['ram_available_gib'])}  disk free {_gib(h['disk_free_gib'])}  {power}")
    L.append(f"Code: {h['branch']} @ {h['head']}  run commit {rs['commit'] or '-'}  Python {h['python']}")
    L.append(f"GitHub: timer {p['timer'].get('ActiveState', 'not available')}  last publish "
             f"{p['last_ok'] or 'never'}  origin {p['remote_sha'] or '-'} ({p['remote_time'] or '-'})  "
             f"unpushed {p['unpushed_commits'] if p['unpushed_commits'] is not None else '-'}  "
             f"awaiting copy {p['awaiting_copy']}")
    return "\n".join(L)


def render_html(s: dict) -> str:
    e = html.escape
    rs, h, p, o = s["runner"], s["host"], s["publishing"], s["overall"]
    tone = {"running": "ok", "completed": "ok", "idle": "idle", "stopped": "idle", "late": "warn",
            "stalled": "bad", "interrupted": "bad", "failed": "bad"}[rs["state"]]

    def bar(done, total, failed=0):
        pd = 0 if not total else 100 * done / total
        pf = 0 if not total else 100 * failed / total
        return (f'<div class="bar"><span style="width:{pd:.2f}%"></span>'
                f'<span class="f" style="width:{pf:.2f}%"></span></div>')

    stage_rows = "".join(
        f"<tr><td><b>{e(n)}</b></td><td>{bar(st['done'], st['total'], st['failed'])}</td>"
        f"<td>{st['done']}/{st['total']}</td><td class='{'bad' if st['failed'] else ''}'>{st['failed']}</td>"
        f"<td>{st['todo']}</td><td>{e(st['label'])}</td><td>{_dur(st['median_s'])}</td>"
        f"<td>{st['peak_rss_mib'] or '—'}</td><td>{_hours(st['eta_h'])}</td></tr>"
        for n, st in s["stages"].items())
    cell_html = ""
    for n, rows in s["cells"].items():
        st = s["stages"][n]
        if st["label"] == "not started":
            continue
        body = "".join(
            f"<tr><td>{e(c['dataset'])}</td><td>{e(c['model'])}</td><td>{c['done_seeds']}/{c['seeds']}</td>"
            f"<td>{c['done']}/{c['shards']}</td><td class='{'bad' if c['failed'] else ''}'>{c['failed']}</td>"
            f"<td>{_dur(c['avg_s'])}</td><td>{_dur(c['left_s'])}</td></tr>" for c in rows)
        cell_html += (f"<h3>{e(n)}</h3><div class='scroll'><table><tr><th>dataset</th><th>model</th>"
                      f"<th>seeds done</th><th>shards done</th><th>failed</th><th>mean shard time</th>"
                      f"<th>compute left (serial)</th></tr>{body}</table></div>")
    shard_rows = "".join(
        f"<tr><td>{e(n)}</td><td>{e(sh['shard'])}</td><td class='{'bad' if sh['state'] == 'failed' else ''}'>"
        f"{e(sh['state'])}</td><td>{sh.get('rows', '—')}</td><td>{sh.get('failed_rows', '—')}</td>"
        f"<td>{_dur(sh.get('seconds'))}</td><td>{sh.get('peak_rss_mib') or '—'}</td>"
        f"<td>{e(str(sh.get('finished') or sh.get('at') or '—'))}</td><td>{e(str(sh.get('commit', '—')))}</td>"
        f"<td>{e(str(sh.get('error', ''))[:160])}</td></tr>"
        for n, st in s["stages"].items() for sh in st["shards"][-60:])
    work = "".join(f"<tr><td>{e(w['shard'])}</td><td>{e(w['dataset'])}</td><td>{e(str(w['model']))}</td>"
                   f"<td>{e(str(w['seed']))}</td><td>{_dur(w['elapsed_s'])}</td></tr>"
                   for w in s["workers"]) or "<tr><td colspan=5>none running</td></tr>"
    pool = s["pool"]
    hist = "".join(f"<tr class='{'bad' if ev['bad'] else ''}'><td>{e(ev['time'] or '—')}</td>"
                   f"<td>{e(ev['source'])}</td><td>{e(ev['event'])}</td></tr>"
                   for ev in reversed(s["history"])) or "<tr><td colspan=3>nothing recorded</td></tr>"
    warn = "".join(f"<li>{e(w)}</li>" for w in s["warnings"])
    temp = "not available" if h["temp_c"] is None else f"{h['temp_c']:.0f} °C"
    power = {True: "AC", False: "battery", None: "not available"}[h["ac_power"]]
    hj = h["host_json"]
    eta = "not estimable yet" if o["eta_h"] is None else f"{o['eta_h']:.1f} h"
    timer = p["timer"]
    act = s["stages"].get(rs["stage"])
    active_n = f"{act['done']}/{act['total']}" if act else "—"
    active_label = f"{rs['stage']}: {act['label']}" if act else "no stage started"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Paper G run monitor</title><style>
:root{{--bg:#fbfbf9;--fg:#1d1d1b;--mut:#6b6b66;--line:#e3e2dc;--acc:#2f6f5e;--bad:#b3261e;--warn:#fff4d6;--amber:#d9a21b}}
@media (prefers-color-scheme:dark){{:root{{--bg:#161615;--fg:#ecebe6;--mut:#a3a29c;--line:#34332f;--acc:#6fbfa6;--bad:#ff8a80;--warn:#3a3218}}}}
body{{background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,sans-serif;margin:0 auto;padding:16px;max-width:1150px}}
h1{{font-size:18px;margin:0 0 4px}} h2{{font-size:15px;margin:24px 0 6px}} h3{{font-size:13px;margin:12px 0 4px}}
small,.mut{{color:var(--mut)}} .tag{{font-size:11px;color:var(--mut);font-weight:400;margin-left:6px}}
table{{border-collapse:collapse;width:100%}} td,th{{border-bottom:1px solid var(--line);padding:4px 6px;text-align:left;vertical-align:top}}
.bar{{display:flex;background:var(--line);height:9px;border-radius:4px;overflow:hidden;min-width:90px}}
.bar span{{display:block;height:100%;background:var(--acc)}} .bar span.f{{background:var(--bad)}}
.kpi{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin-top:12px}}
.kpi div{{border:1px solid var(--line);border-radius:8px;padding:8px}} .kpi b{{display:block;font-size:20px}}
.warn{{background:var(--warn);border-radius:8px;padding:6px 10px 6px 26px}} .bad{{color:var(--bad);font-weight:600}}
.st-ok{{color:var(--acc)}} .st-warn{{color:var(--amber)}} .st-bad{{color:var(--bad)}} .st-idle{{color:var(--mut)}}
.scroll{{overflow-x:auto}}
.hb{{display:flex;flex-wrap:wrap;gap:14px;align-items:center;border:1px solid var(--line);border-radius:8px;padding:8px 10px;margin:10px 0;position:sticky;top:0;background:var(--bg);z-index:2}}
.hb span.item{{display:flex;align-items:center;gap:6px;white-space:nowrap}}
.dot{{width:11px;height:11px;border-radius:50%;background:var(--mut);display:inline-block}}
.dot.ok{{background:#2e9e6a;animation:pulse 1.2s ease-in-out infinite}} .dot.slow{{background:var(--amber)}} .dot.dead{{background:var(--bad)}} .dot.idle{{background:var(--mut)}}
@keyframes pulse{{0%{{box-shadow:0 0 0 0 rgba(46,158,106,.6)}}70%{{box-shadow:0 0 0 7px rgba(46,158,106,0)}}100%{{box-shadow:0 0 0 0 rgba(46,158,106,0)}}}}
@media (prefers-reduced-motion:reduce){{.dot.ok{{animation:none}}}}
</style></head><body>
<h1>Paper G — run monitor</h1>
<div class="mut">{e(s['now'])} UTC · heartbeat every 2 s · full refresh every 30 s · read-only · progress and health only, no metric values</div>
<div class="hb" aria-live="polite">
<span class="item"><span class="dot" id="d-run"></span><b>Runner</b> <span id="t-run">…</span></span>
<span class="item"><span class="dot" id="d-pub"></span><b>Publisher</b> <span id="t-pub">…</span></span>
<span class="item"><span class="dot" id="d-page"></span><b>This page</b> <span id="t-page">…</span></span>
</div>
{f'<h2>Warnings</h2><ul class="warn">{warn}</ul>' if warn else '<p class="st-ok">No warnings.</p>'}
<h2>1. Overview <span class="tag">now</span></h2>
<div class="kpi">
<div>Runner<b class="st-{tone}">{e(rs['state'])}</b><small>stage {e(str(rs['stage'] or '—'))} · heartbeat {e(_ago(_utc(rs['heartbeat']), _utc(s['now'])))}</small></div>
<div>Active stage<b>{active_n}</b><small>{e(active_label)}</small></div>
<div>All four stages<b>{o['done']}/{o['total']}</b><small>{o['running']} running · {o['pending']} pending · {o['failed']} failed{' · experiment complete' if o['done'] == o['total'] else ''}</small></div>
<div>Time<b>{_dur(o['elapsed_s'])}</b><small>since first shard {e(o['first_start'] or '—')} · left: {e(eta)}</small></div>
</div>
<p class="mut">Stage start (this runner): {e(str(rs['started'] or '—'))} · run commit {e(str(rs['commit'] or '—'))}. Time left counts only stages with their own finished shards; the pilot (20 instances) does not predict the full run.</p>
<h2>2. Progress by stage</h2><div class="scroll"><table>
<tr><th>stage</th><th>progress</th><th>done</th><th>failed</th><th>pending</th><th>state</th><th>median shard</th><th>peak MiB</th><th>time left</th></tr>{stage_rows}</table></div>
<h2>3. Progress by dataset and model</h2>{cell_html or '<p class="mut">No stage started.</p>'}
<h2>4. Active workers <span class="tag">now</span></h2>
<p class="mut">{len(rs['running'])} shard(s) running · jobs of this runner {rs['jobs'] or '—'} · configured {rs['max_jobs']} ·
worker processes {pool['processes'] if pool else 'not available'} · resident memory {f"{pool['rss_mib']:.0f} MiB (largest {pool['largest_mib']} MiB)" if pool and pool['processes'] else 'not available'} · memory per shard: not available (the pool does not map processes to shards)</p>
<div class="scroll"><table><tr><th>shard</th><th>dataset</th><th>model</th><th>seed</th><th>running for</th></tr>{work}</table></div>
<h2>5. Host <span class="tag">now</span></h2>
<div class="kpi">
<div>CPU<b>{'—' if h['cpu_percent'] is None else f"{h['cpu_percent']:.0f}%"}</b><small>temperature {e(temp)} · kernel throttle events {h['throttle_count'] if h['throttle_count'] is not None else 'not available'}</small></div>
<div>Memory<b>{_gib(h['ram_available_gib'])}</b><small>available of {_gib(h['ram_total_gib'])}</small></div>
<div>Disk<b>{_gib(h['disk_free_gib'])}</b><small>free · power {e(power)}</small></div>
<div>Host<b>{e(h['hostname'])}</b><small>{e(str(hj.get('cpu', '')))} · Python {e(h['python'])} ({e(h['python_prefix'])}) · {e(str(h['branch']))} @ {e(str(h['head']))}</small></div>
</div>
<h2>6. GitHub publishing</h2><table>
<tr><td>Timer</td><td>{e(timer.get('ActiveState', 'not available'))} · next {e(timer.get('NextElapseUSecRealtime') or '—')}</td></tr>
<tr><td>Last successful cycle</td><td>{e(p['last_ok'] or 'never')} ({e(_ago(_utc(p['last_ok']), _utc(s['now'])))})</td></tr>
<tr><td>Last cycle</td><td class="{'bad' if p['last_line_bad'] else ''}">{e(p['last_line'] or '—')}</td></tr>
<tr><td>On GitHub (origin/{RUN_BRANCH})</td><td>{e(p['remote_sha'] or '—')} · {e(p['remote_time'] or '—')} ({e(_ago(_utc(p['remote_time']), _utc(s['now'])))}) · {e(p['remote_subject'] or '')}</td></tr>
<tr><td>Local commits not pushed</td><td>{p['unpushed_commits'] if p['unpushed_commits'] is not None else 'not available'} <small>(as of the last fetch or push)</small></td></tr>
<tr><td>Finished shards awaiting copy</td><td>{p['awaiting_copy']} · {p['manifest_shards']} in MANIFEST.csv</td></tr>
<tr><td>Push failing since</td><td>{e(p['push_failing_since'] or '—')}</td></tr>
</table>
<p class="mut">Remote progress: <code>outputs/analysis/paper_g/STATUS.md</code> on {RUN_BRANCH} and issue #118.</p>
<h2>7. Shards finished or failed <span class="tag">history</span></h2>
<div class="scroll"><table><tr><th>stage</th><th>shard</th><th>state</th><th>rows</th><th>failed rows</th><th>time</th><th>peak MiB</th><th>finished</th><th>commit</th><th>error</th></tr>{shard_rows or '<tr><td colspan=10>none</td></tr>'}</table></div>
<h2>8. Execution history <span class="tag">history</span></h2>
<div class="scroll"><table><tr><th>time (UTC)</th><th>source</th><th>event</th></tr>{hist}</table></div>
<script>
let hb = null, fetchedAt = 0, fails = 0;
function fmt(a) {{ return a < 120 ? a.toFixed(0) + ' s ago' : a < 7200 ? (a / 60).toFixed(0) + ' min ago' : (a / 3600).toFixed(1) + ' h ago'; }}
function set(k, cls, txt) {{ document.getElementById('d-' + k).className = 'dot ' + cls; document.getElementById('t-' + k).textContent = txt; }}
function render() {{
  if (hb) {{
    const now = Date.now() / 1000, r = hb.runner, p = hb.publisher;
    if (!r.t) set('run', 'idle', 'no run yet');
    else {{ const a = now - r.t; set('run', r.alive ? (a < 120 ? 'ok' : a < 3600 ? 'slow' : 'dead') : 'idle',
            fmt(a) + (r.label ? ' · ' + r.label : '') + (r.alive ? '' : ' · runner not running')); }}
    if (!p.t) set('pub', 'idle', 'no cycle yet · timer ' + (p.timer || '?'));
    else {{ const a = now - p.t; set('pub', !p.ok ? 'dead' : a < 1200 ? 'ok' : a < 2400 ? 'slow' : 'dead',
            fmt(a) + (p.ok ? '' : ' · last cycle refused') + ' · timer ' + (p.timer || '?')); }}
  }}
  const pa = (Date.now() - fetchedAt) / 1000;
  set('page', fails ? 'dead' : pa < 6 ? 'ok' : 'slow', fails ? 'dashboard server not answering' : 'updated ' + pa.toFixed(0) + ' s ago');
}}
async function poll() {{
  try {{ const r = await fetch('/api/heartbeat', {{cache: 'no-store'}}); hb = await r.json(); fetchedAt = Date.now(); fails = 0; }}
  catch (err) {{ fails += 1; }}
  render();
}}
poll(); setInterval(poll, 2000); setInterval(render, 1000);
setTimeout(() => location.reload(), 30000);
</script>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.startswith("/api/heartbeat"):
                body, ctype = json.dumps(heartbeat()).encode(), "application/json"
            elif self.path.startswith("/api/state"):
                body, ctype = json.dumps(gather(), default=str).encode(), "application/json"
            elif self.path in ("/", "/index.html"):
                body, ctype = render_html(gather()).encode(), "text/html; charset=utf-8"
            else:
                body, ctype = b"not found", "text/plain"
                self.send_response(404)
                self._send(body, ctype)
                return
            self.send_response(200)
        except Exception as exc:          # show the problem instead of failing silently
            body, ctype = f"dashboard error: {type(exc).__name__}: {exc}".encode(), "text/plain"
            self.send_response(500)
        self._send(body, ctype)

    def _send(self, body: bytes, ctype: str):
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_a):
        pass


def serve(port: int = PORT) -> ThreadingHTTPServer:
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, default=PORT)
    ap.add_argument("--text", action="store_true")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--every", type=float, default=10)
    a = ap.parse_args(argv)
    if a.once:
        cpu_percent()
        time.sleep(0.2)               # a short first sample for the CPU figure
        print(render_text(gather()))
        return 0
    if a.text:
        try:
            while True:
                print("\033[2J\033[H" + render_text(gather()), flush=True)
                time.sleep(a.every)
        except KeyboardInterrupt:
            return 0
    srv = serve(a.port)
    print(f"dashboard at http://127.0.0.1:{a.port}  (Ctrl+C to close; the run is not affected)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
