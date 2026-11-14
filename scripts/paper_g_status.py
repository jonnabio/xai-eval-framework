#!/usr/bin/env python3
"""Paper G: build the status page of the run (STATUS.md) from the work directory.

    python scripts/paper_g_status.py            print the page
    python scripts/paper_g_status.py --write    write outputs/analysis/paper_g/STATUS.md

It reads only shard markers (.done, .failed), the heartbeat and the host record. It shows
progress, timing, failures and the machine; it never shows a metric value (plan, section 4:
results are analysed once, after the run).
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_g_lib as lib  # noqa: E402
import paper_g_run as run  # noqa: E402

STALL_MINUTES = 60


def _read(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _age_min(stamp: str | None, now: datetime) -> float | None:
    if not stamp:
        return None
    t = datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return (now - t).total_seconds() / 60


def collect(cfg: dict) -> dict:
    """Machine-readable state of every stage, used by the page and by the publisher."""
    out = {}
    for stage in run.STAGES:
        shards = run.shards(stage, cfg)
        rows = []
        for sh in shards:
            st = run.state(sh, cfg)
            info = _read(run.shard_path(sh, cfg, ".done" if st == "done" else ".failed")) \
                if st != "todo" else None
            rows.append({"shard": run.shard_name(sh), "seed": sh["seed"],
                         "dataset": sh["dataset"], "model": sh["model"], "state": st,
                         "info": info or {}})
        out[stage] = rows
    return out


def eta_hours(rows: list[dict], jobs: int) -> float | None:
    secs = [r["info"].get("seconds") for r in rows if r["state"] == "done" and r["info"].get("seconds")]
    left = sum(r["state"] != "done" for r in rows)
    if not secs or not left:
        return None if left else 0.0
    return statistics.median(secs) * left / max(jobs, 1) / 3600


def build(cfg: dict, now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    work = run.work_dir(cfg)
    beat = _read(work / "heartbeat.json") or {}
    host = _read(lib.ROOT / "experiments" / "exp_g" / "host.json") or {}
    state = collect(cfg)
    age = _age_min(beat.get("heartbeat"), now)
    active = beat.get("stage")
    running = bool(beat.get("running")) or bool(beat.get("todo"))
    stalled = running and age is not None and age > STALL_MINUTES
    L = ["# Paper G — run status", "",
         f"Generated {now.strftime('%Y-%m-%d %H:%M UTC')} by `scripts/paper_g_status.py`. "
         "Progress only: no metric value is shown before the run ends.", ""]
    flag = "**STALLED**" if stalled else ("running" if running else "idle")
    L += ["| Item | Value |", "|---|---|",
          f"| State | {flag} |",
          f"| Active stage | {active or '—'} |",
          f"| Last heartbeat | {beat.get('heartbeat', '—')}"
          + (f" ({age:.0f} min ago)" if age is not None else "") + " |",
          f"| Jobs | {beat.get('jobs', '—')} |",
          f"| Running shards | {', '.join(beat.get('running') or []) or '—'} |",
          f"| Free memory | {beat.get('free_memory_gib') and round(beat['free_memory_gib'], 1)} GiB |",
          f"| Host | {beat.get('host') or host.get('hostname', '—')} "
          f"({host.get('cpu', '?')}, {host.get('ram_gib', '?')} GiB RAM) |",
          f"| Commit of the run | {beat.get('commit', '—')} |",
          f"| Free disk | {host.get('free_disk_gib', '—')} GiB at set-up |", ""]
    L += ["## Stages", "", "| Stage | Done | Failed | To do | Total | Estimated time left |",
          "|---|---|---|---|---|---|"]
    for stage, rows in state.items():
        n = {s: sum(r["state"] == s for r in rows) for s in ("done", "failed", "todo")}
        eta = eta_hours(rows, beat.get("jobs") or cfg["run"]["jobs"])
        L.append(f"| {stage} | {n['done']} | {n['failed']} | {n['todo']} | {len(rows)} | "
                 + ("—" if eta is None else f"{eta:.1f} h") + " |")
    for stage, rows in state.items():
        if not any(r["state"] != "todo" for r in rows) or stage == "pilot":
            continue
        seeds = sorted({r["seed"] for r in rows})
        L += ["", f"### {stage}: shards done per seed", "",
              "| Seed | Done | Failed | Total |", "|---|---|---|---|"]
        for s in seeds:
            rs = [r for r in rows if r["seed"] == s]
            L.append(f"| {s} | {sum(r['state'] == 'done' for r in rs)} | "
                     f"{sum(r['state'] == 'failed' for r in rs)} | {len(rs)} |")
    fails = [(st, r) for st, rows in state.items() for r in rows if r["state"] == "failed"]
    L += ["", "## Failures", ""]
    if not fails:
        L.append("None.")
    else:
        L += ["| Stage | Shard | Error | Log |", "|---|---|---|---|"]
        for st, r in fails:
            err = (r["info"].get("error") or "").replace("|", "/").replace("\n", " ")
            L.append(f"| {st} | {r['shard']} | {err[:160]} | `logs/{st}/{r['shard']}.log` |")
    rowfail = [(st, r) for st, rows in state.items() for r in rows
               if r["state"] == "done" and r["info"].get("failed_rows")]
    if rowfail:
        L += ["", "Shards with failed explanation rows (kept and counted, plan section 2):", ""]
        for st, r in rowfail:
            L.append(f"- {st} {r['shard']}: {r['info']['failed_rows']} of {r['info']['rows']} rows")
    pilot = [r for r in state["pilot"] if r["state"] == "done"]
    if pilot:
        L += ["", "## Pilot timing and memory", "", "| Shard | Seconds | Peak memory (MiB) |",
              "|---|---|---|"]
        for r in pilot:
            L.append(f"| {r['shard']} | {r['info'].get('seconds')} | {r['info'].get('peak_rss_mib')} |")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args(argv)
    page = build(lib.config())
    if args.write:
        lib.OUT.mkdir(parents=True, exist_ok=True)
        (lib.OUT / "STATUS.md").write_text(page, encoding="utf-8")
    else:
        print(page)
    return 0


if __name__ == "__main__":
    sys.exit(main())
