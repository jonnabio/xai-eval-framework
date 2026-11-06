#!/usr/bin/env python3
"""Paper B revision 1 (cohort B2): monitoring dashboard.

    python scripts/paper_b_dashboard.py              web page at http://127.0.0.1:8765
    python scripts/paper_b_dashboard.py --port 8800
    python scripts/paper_b_dashboard.py --text       terminal view, refreshed every 10 s
    python scripts/paper_b_dashboard.py --once       print once and exit
    python scripts/paper_b_dashboard.py --status-md  write outputs/paper_b_rev1_live/STATUS.md

Read-only: it reads the files under outputs/paper_b_rev1_live/ and the process list, and
never starts, stops or changes anything, so it is safe to open and close at any time.
Localhost only. The sync pushes STATUS.md with every snapshot, so the same summary can be
read on GitHub (branch paper/b-rev1-runs) from a phone.

It shows progress and health, never a result: no metric value is displayed (the results
are analysed once the cohort is complete).
"""
from __future__ import annotations

import argparse
import html
import json
import os
import sys
import time
import tomllib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_b_lib as lib  # noqa: E402  (standard library at import time)

_line_cache: dict[Path, tuple[float, int, int, int, float | None]] = {}


def _count(path: Path) -> tuple[int, int, float | None]:
    """(rows, failed rows, time of the last row) of a JSONL file, cached by mtime and size."""
    try:
        st = path.stat()
    except OSError:
        return 0, 0, None
    hit = _line_cache.get(path)
    if hit and hit[0] == st.st_mtime and hit[1] == st.st_size:
        return hit[2], hit[3], hit[4]
    rows = failed = 0
    last_t = None
    for r in lib.read_jsonl(path):
        rows += 1
        failed += int(r.get("failed", 0) or 0)
        last_t = r.get("time", last_t)
    _line_cache[path] = (st.st_mtime, st.st_size, rows, failed, last_t)
    return rows, failed, last_t


def _alive(pid) -> bool:
    if not pid:
        return False
    try:
        import psutil
        return psutil.pid_exists(int(pid))
    except Exception:
        return True


def gather() -> dict:
    with open(lib.CONFIG_PATH, "rb") as fh:
        cfg = tomllib.load(fh)
    per = cfg["sampling"]["per_stratum"] * 4
    out: dict = {"now": time.time(), "passes": {}}
    for name, root, jobs, rows_per in (
        ("pilot", lib.LIVE / "pilot",
         [(d, m, lib.seeds_for(cfg, d)[0], e) for d in cfg["datasets"] for m in cfg["models"]
          for e in cfg["explainers"]], 4),
        ("quality", lib.RESULTS, lib.all_quality_jobs(cfg), per),
    ):
        table: dict[str, dict] = {}
        tot = {"jobs": len(jobs), "done": 0, "rows": 0, "failed": 0, "expected_rows": 0,
               "recent": 0}
        for d, m, s, e in jobs:
            stem = root / "quality" / d / m / f"seed_{s}" / e
            rows, failed, last_t = _count(stem.with_suffix(".jsonl"))
            done = stem.with_suffix(".done").exists()
            t = table.setdefault(f"{d}|{e}", {"dataset": d, "explainer": e, "jobs": 0,
                                               "done": 0, "rows": 0, "failed": 0})
            t["jobs"] += 1
            t["done"] += done
            t["rows"] += rows
            t["failed"] += failed
            tot["done"] += done
            tot["rows"] += rows
            tot["failed"] += failed
            tot["expected_rows"] += rows_per
            if last_t and out["now"] - last_t < 3600:
                tot["recent"] += 1
        out["passes"][name] = {"total": tot, "table": sorted(table.values(),
                                                               key=lambda r: (r["dataset"], r["explainer"]))}
    # Timing pass: cells.
    cells = [(d, m, s) for d in cfg["datasets"] for m in cfg["models"] for s in lib.seeds_for(cfg, d)]
    tdone = sum((lib.RESULTS / "timing" / d / m / f"seed_{s}" / "timing").with_suffix(".done").exists()
                for d, m, s in cells)
    out["timing"] = {"cells": len(cells), "done": tdone,
                     "state": lib.read_json(lib.STATE / "timing.json", {}),
                     "gate": lib.read_json(lib.STATE / "timing_gate.json", {})}
    orch = lib.read_json(lib.STATE / "orchestrator.json", {}) or {}
    orch["alive"] = _alive(orch.get("pid")) and out["now"] - orch.get("updated", 0) < 60
    out["orchestrator"] = orch
    out["sync"] = lib.read_json(lib.STATE / "sync.json", {}) or {}
    out["preflight"] = lib.read_json(lib.STATE / "preflight.json", {}) or {}
    bench = list(lib.read_jsonl(lib.STATE / "bench.jsonl"))
    # Compare like with like: the first and last benchmark taken with the same number
    # of workers running (parallel load slows it without any heat).
    same = [b for b in bench if bench and b.get("workers") == bench[-1].get("workers")]
    out["bench"] = {"first": same[0]["bench_ms"] if same else None,
                    "last": same[-1]["bench_ms"] if same else None, "n": len(same),
                    "workers": bench[-1].get("workers") if bench else None}
    out["warnings"] = warnings(out)
    return out


def warnings(s: dict) -> list[str]:
    w = []
    o = s["orchestrator"]
    if o and not o.get("alive") and o.get("queue"):
        w.append("The orchestrator is not running but jobs remain queued: run `launch` again "
                 "(it resumes).")
    host = o.get("host") or {}
    if host.get("ac_power") is False:
        w.append("ON BATTERY: admission is paused. Connect the charger.")
    if host.get("ram_available_gb") is not None and host["ram_available_gb"] < 4:
        w.append(f"Low RAM: {host['ram_available_gb']:.1f} GB available.")
    if host.get("disk_free_gb") is not None and host["disk_free_gb"] < 10:
        w.append(f"Low disk: {host['disk_free_gb']:.1f} GB free.")
    b = s["bench"]
    if b["first"] and b["last"] and b["last"] > 1.15 * b["first"]:
        w.append(f"Throttling suspected: the micro-benchmark is {b['last'] / b['first']:.2f}x "
                 "its first value (heat or power plan).")
    sy = s["sync"]
    lp = sy.get("last_push_time")
    if (o.get("alive") or s["timing"]["state"].get("pid")) and (not lp or s["now"] - lp > 1800):
        w.append("No push to GitHub for over 30 minutes: is `paper_b_sync.py --loop` running?")
    if sy.get("last_error"):
        w.append(f"Last sync error: {sy['last_error'][:200]}")
    for p in ("pilot", "quality"):
        t = s["passes"][p]["total"]
        if t["rows"] and t["failed"] / t["rows"] > 0.05:
            w.append(f"{p}: {t['failed']} of {t['rows']} instance rows failed (> 5%).")
    if s["orchestrator"].get("failed"):
        w.append(f"{len(s['orchestrator']['failed'])} jobs failed for good: see the failures list.")
    return w


def _ago(t) -> str:
    if not t:
        return "never"
    d = time.time() - t
    return f"{d:.0f} s ago" if d < 120 else f"{d / 60:.0f} min ago" if d < 7200 else f"{d / 3600:.1f} h ago"


def render_text(s: dict) -> str:
    o = s["orchestrator"]
    host = o.get("host") or {}
    L = [f"Paper B rev. 1, cohort B2 - {time.strftime('%Y-%m-%d %H:%M:%S')}"]
    for w in s["warnings"]:
        L.append(f"  !! {w}")
    L.append(f"Orchestrator: {'RUNNING' if o.get('alive') else 'not running'}"
             f" (mode {o.get('mode', '-')}, workers {len(o.get('workers', []))}/{o.get('max_workers', '-')},"
             f" queue {o.get('queue', '-')}, admission: {o.get('admission', '-')})")
    if host:
        L.append(f"Host: CPU {host.get('cpu_percent', 0):.0f}%  RAM free {host.get('ram_available_gb', 0):.1f}"
                 f"/{host.get('ram_total_gb', 0):.1f} GB  disk free {host.get('disk_free_gb', 0):.0f} GB  "
                 f"{'AC' if host.get('ac_power') else 'BATTERY' if host.get('ac_power') is False else '?'}"
                 f"  {host.get('cpu_mhz') or '?'} MHz")
    for p in ("pilot", "quality"):
        t = s["passes"][p]["total"]
        L.append(f"{p:8}: jobs {t['done']}/{t['jobs']}  rows {t['rows']}/{t['expected_rows']}"
                 f"  failed rows {t['failed']}")
    tm = s["timing"]
    gate = tm["gate"] or {}
    L.append(f"timing  : cells {tm['done']}/{tm['cells']}"
             + (f"  gate: {'WAITING — ' + gate.get('reason', '') if gate.get('waiting') else 'running'}"
                if gate else ""))
    for w in o.get("workers", []):
        el = time.time() - (w.get("instance_started") or w["born"])
        L.append(f"  pid {w['pid']:>6} {'/'.join(map(str, w['job'])):40} inst {w.get('instance')}"
                 f" {el:6.0f} s  RSS {w.get('rss_gb') or 0:.2f} GB (peak {w['peak_gb']:.2f})")
    sy = s["sync"]
    L.append(f"Sync: last push {_ago(sy.get('last_push_time'))}"
             f" ({(sy.get('last_pushed') or '')[:10]}), last commit {_ago(sy.get('last_commit_time'))}")
    return "\n".join(L)


def render_html(s: dict) -> str:
    o = s["orchestrator"]
    host = o.get("host") or {}
    e = html.escape

    def bar(done, total):
        pct = 0 if not total else 100 * done / total
        return (f'<div class="bar"><span style="width:{pct:.1f}%"></span></div>'
                f'<small>{done} / {total} ({pct:.0f}%)</small>')

    rows = []
    for p in ("pilot", "quality"):
        for r in s["passes"][p]["table"]:
            rows.append(f"<tr><td>{p}</td><td>{e(r['dataset'])}</td><td>{e(r['explainer'])}</td>"
                        f"<td>{bar(r['done'], r['jobs'])}</td><td>{r['rows']}</td>"
                        f"<td class='{'bad' if r['failed'] else ''}'>{r['failed']}</td></tr>")
    workers = "".join(
        f"<tr><td>{w['pid']}</td><td>{e('/'.join(map(str, w['job'])))}</td><td>{w.get('instance')}</td>"
        f"<td>{time.time() - (w.get('instance_started') or w['born']):.0f} s</td>"
        f"<td>{(w.get('rss_gb') or 0):.2f} GB</td><td>{w['peak_gb']:.2f} GB</td></tr>"
        for w in o.get("workers", [])) or "<tr><td colspan=6>none</td></tr>"
    fails = "".join(f"<li>{e(k)}: {e(v)}</li>" for k, v in (o.get("failed") or {}).items()) or "<li>none</li>"
    warn = "".join(f"<li>{e(w)}</li>" for w in s["warnings"])
    tm, sy = s["timing"], s["sync"]
    gate = tm["gate"] or {}
    q, pl = s["passes"]["quality"]["total"], s["passes"]["pilot"]["total"]
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="10"><title>B2 run monitor</title><style>
:root{{--bg:#fbfbf9;--fg:#1d1d1b;--mut:#6b6b66;--line:#e3e2dc;--acc:#2f6f5e;--bad:#b3261e;--warn:#fff4d6}}
@media (prefers-color-scheme:dark){{:root{{--bg:#161615;--fg:#ecebe6;--mut:#a3a29c;--line:#34332f;--acc:#6fbfa6;--bad:#ff8a80;--warn:#3a3218}}}}
body{{background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,sans-serif;margin:0;padding:16px;max-width:1100px}}
h1{{font-size:18px;margin:0 0 4px}} h2{{font-size:15px;margin:22px 0 6px}} small,.mut{{color:var(--mut)}}
table{{border-collapse:collapse;width:100%}} td,th{{border-bottom:1px solid var(--line);padding:4px 6px;text-align:left;vertical-align:top}}
.bar{{background:var(--line);height:8px;border-radius:4px;overflow:hidden;min-width:80px}} .bar span{{display:block;height:100%;background:var(--acc)}}
.kpi{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px}}
.kpi div{{border:1px solid var(--line);border-radius:8px;padding:8px}} .kpi b{{display:block;font-size:20px}}
.warn{{background:var(--warn);border-radius:8px;padding:6px 10px}} .bad{{color:var(--bad);font-weight:600}}
.scroll{{overflow-x:auto}}</style></head><body>
<h1>Paper B revision 1 — cohort B2</h1><div class="mut">{time.strftime('%Y-%m-%d %H:%M:%S')} · refreshes every 10 s · read-only</div>
{f'<h2>Warnings</h2><ul class="warn">{warn}</ul>' if warn else ''}
<div class="kpi" style="margin-top:12px">
<div>Orchestrator<b>{'running' if o.get('alive') else 'stopped'}</b><small>{e(str(o.get('mode', '-')))} · {len(o.get('workers', []))}/{o.get('max_workers', '-')} workers · queue {o.get('queue', '-')}</small></div>
<div>Pilot<b>{pl['done']}/{pl['jobs']}</b><small>jobs · {pl['failed']} failed rows</small></div>
<div>Quality pass<b>{q['done']}/{q['jobs']}</b><small>jobs · {q['rows']}/{q['expected_rows']} rows · {q['failed']} failed</small></div>
<div>Timing pass<b>{tm['done']}/{tm['cells']}</b><small>cells · {'gate waiting: ' + e(gate.get('reason', '')) if gate.get('waiting') else 'gate open' if gate else 'not started'}</small></div>
<div>Host<b>{host.get('cpu_percent', 0):.0f}% CPU</b><small>RAM free {host.get('ram_available_gb', 0):.1f} GB · disk {host.get('disk_free_gb', 0):.0f} GB · {'AC' if host.get('ac_power') else 'battery' if host.get('ac_power') is False else '?'} · {host.get('cpu_mhz') or '?'} MHz</small></div>
<div>GitHub sync<b>{_ago(sy.get('last_push_time'))}</b><small>{e((sy.get('last_pushed') or '')[:10])} · branch {e(lib.config()['sync']['branch'])}</small></div>
</div>
<p class="mut">Admission: {e(str(o.get('admission', '-')))} · micro-benchmark first/last: {s['bench']['first'] or '-'} / {s['bench']['last'] or '-'} ms</p>
<h2>Workers</h2><div class="scroll"><table><tr><th>pid</th><th>job</th><th>instance</th><th>on it</th><th>RSS</th><th>peak</th></tr>{workers}</table></div>
<h2>Progress by dataset and explainer</h2><div class="scroll"><table><tr><th>pass</th><th>dataset</th><th>explainer</th><th>jobs</th><th>rows</th><th>failed</th></tr>{''.join(rows)}</table></div>
<h2>Jobs failed for good</h2><ul>{fails}</ul>
</body></html>"""


def write_status_md() -> None:
    s = gather()
    md = ["# Cohort B2 run status", "", f"Generated {time.strftime('%Y-%m-%d %H:%M:%S %Z')} by "
          "`scripts/paper_b_dashboard.py` (no metric values are shown).", "", "```",
          render_text(s), "```", ""]
    lib.atomic_write_text(lib.LIVE / "STATUS.md", "\n".join(md))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            s = gather()
            if self.path.startswith("/api/state"):
                body, ctype = json.dumps(s, default=str).encode(), "application/json"
            else:
                body, ctype = render_html(s).encode(), "text/html; charset=utf-8"
            self.send_response(200)
        except Exception as exc:          # show the problem instead of failing silently
            body, ctype = f"dashboard error: {exc}".encode(), "text/plain"
            self.send_response(500)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_a):
        pass


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--text", action="store_true")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--status-md", action="store_true")
    ap.add_argument("--every", type=float, default=10)
    a = ap.parse_args(argv)
    if a.status_md:
        write_status_md()
        return 0
    if a.once:
        print(render_text(gather()))
        return 0
    if a.text:
        try:
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print(render_text(gather()))
                time.sleep(a.every)
        except KeyboardInterrupt:
            return 0
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    print(f"dashboard at http://127.0.0.1:{a.port}  (Ctrl+C to close; the run is not affected)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
