#!/usr/bin/env python3
"""Paper B revision 1: budget of the full B2 runs, estimated from the pilot.

    python scripts/paper_b_pilot_budget.py            table + totals (Markdown)
    python scripts/paper_b_pilot_budget.py --csv out.csv

Per pilot job (one seed, 1 instance per stratum = 4 instances, stability on each) the
rows give t_e, the median time of one explanation (`explain_wall_ms`), and the `.done`
marker gives the job's elapsed time E. With T stability perturbations,
E ~ 4 (t_e + f) + 4 T t_e, so the per-instance overhead f (fidelity, set-up share) is
f = max(0, (E - 4 (T + 1) t_e) / 4). A full job explains n instances and runs
stability on k of them: n (t_e + f) + k T t_e. Seeds multiply it.

The wall time of the quality pass is the sum over jobs divided by the number of
workers (an optimistic bound: the longest single job can dominate; it is listed).
The timing pass is sequential: cells x explainers x instances x (repeats + warm-up)
x t_e. Pilot explanations ran on a loaded host (parallel workers), so these estimates
are conservative for the timing pass.

It prints times and memory only; no metric value is read.
"""
from __future__ import annotations

import argparse
import csv
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_b_lib as lib  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--csv")
    a = ap.parse_args(argv)
    cfg = lib.config()
    T = cfg["metrics"]["stability_T"]
    n_full = 4 * cfg["sampling"]["per_stratum"]
    k_full = 4 * cfg["sampling"]["stability_per_stratum"]
    workers = cfg["resources"]["max_workers"]
    tc = cfg["timing"]
    n_time = 4 * tc["per_stratum"]
    peaks = lib.read_json(lib.STATE / "peaks.json", {}) or {}
    root = lib.LIVE / "pilot" / "quality"
    rows_out, missing, failed_jobs = [], [], []
    per_cell_te: dict[tuple, dict] = {}
    for d in cfg["datasets"]:
        seeds = lib.seeds_for(cfg, d)
        for m in cfg["models"]:
            for e in cfg["explainers"]:
                stem = root / d / m / f"seed_{seeds[0]}" / e
                done = lib.read_json(stem.with_suffix(".done"))
                rows = list(lib.read_jsonl(stem.with_suffix(".jsonl")))
                if not done:
                    missing.append(f"{d}/{m}/{e}")
                    continue
                ok = [r for r in rows if not r.get("failed")]
                if not ok:
                    failed_jobs.append(f"{d}/{m}/{e}")
                    continue
                te = statistics.median(r["explain_wall_ms"] for r in ok) / 1e3
                n_rows = len(rows)
                f = max(0.0, (done["elapsed_s"] - n_rows * (T + 1) * te) / max(1, n_rows))
                full = n_full * (te + f) + k_full * T * te
                per_cell_te.setdefault((d, m), {})[e] = te
                pk = peaks.get(f"{d}|{m}|{e}", [done.get("peak_rss_gb", 0)])
                rows_out.append({"dataset": d, "model": m, "explainer": e,
                                 "t_explain_s": te, "overhead_s": f,
                                 "pilot_failed_rows": sum(1 for r in rows if r.get("failed")),
                                 "full_job_h": full / 3600, "seeds": len(seeds),
                                 "all_seeds_h": full * len(seeds) / 3600,
                                 "peak_gb": max(pk)})
    total_h = sum(r["all_seeds_h"] for r in rows_out)
    longest = max(rows_out, key=lambda r: r["full_job_h"], default=None)
    timing_h = 0.0
    for (d, m), te in per_cell_te.items():
        timing_h += len(lib.seeds_for(cfg, d)) * n_time * sum(te.values()) * tc["repeats"] / 3600
        timing_h += len(lib.seeds_for(cfg, d)) * sum(te.values()) * tc["warmup_per_explainer"] / 3600
    rows_out.sort(key=lambda r: -r["all_seeds_h"])
    print("| dataset | model | explainer | t/explanation (s) | full job (h) | x seeds (h) | peak (GB) | pilot failed rows |")
    print("|---|---|---|---:|---:|---:|---:|---:|")
    for r in rows_out[:25]:
        print(f"| {r['dataset']} | {r['model']} | {r['explainer']} | {r['t_explain_s']:.3f} | "
              f"{r['full_job_h']:.2f} | {r['all_seeds_h']:.2f} | {r['peak_gb']:.2f} | {r['pilot_failed_rows']} |")
    print(f"\n(top 25 of {len(rows_out)} job types by total hours)\n")
    print(f"Quality pass: {total_h:.1f} CPU-hours; on {workers} workers about "
          f"{total_h / workers:.1f} h of wall time (lower bound).")
    if longest:
        print(f"Longest single job: {longest['dataset']}/{longest['model']}/{longest['explainer']}"
              f" {longest['full_job_h']:.1f} h.")
    print(f"Timing pass (sequential, quiet host): about {timing_h:.1f} h plus gate waits.")
    if missing:
        print(f"\nNot finished in the pilot ({len(missing)}): {', '.join(missing[:12])}"
              f"{' ...' if len(missing) > 12 else ''}")
    if failed_jobs:
        print(f"Every instance failed ({len(failed_jobs)}): {', '.join(failed_jobs)}")
    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows_out[0]) if rows_out else ["dataset"])
            w.writeheader()
            w.writerows(rows_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
