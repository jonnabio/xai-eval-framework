#!/usr/bin/env python3
"""Paper G: run one stage of the experiment in resumable shards.

    python scripts/paper_g_run.py --stage pilot [--jobs N]
    python scripts/paper_g_run.py --stage full  [--jobs N]
    python scripts/paper_g_run.py --stage roar  [--jobs N]      (needs the full stage)
    python scripts/paper_g_run.py --stage synthetic [--jobs N]
    python scripts/paper_g_run.py --stage full --list           (print shards and their state)

A shard is one dataset x model x seed (synthetic: generator x correlation x seed). It writes
<work>/<stage>/<shard>.jsonl.gz and then <shard>.done (a JSON summary). A finished shard is
never recomputed; an unfinished one restarts from the beginning; a shard that raised writes
<shard>.failed with the error and is tried again on the next start. Each shard logs to
<work>/logs/<stage>/<shard>.log. The main process writes <work>/heartbeat.json every 30 s.

Nothing is aggregated here and no metric value is printed: results are analysed once, after
the run (plan, section 4). Run protocol: docs/reports/paper_g/RUN_PROTOCOL.md.
"""
from __future__ import annotations

import os
import sys

# One thread per job, set before numpy is imported (RUN_PROTOCOL.md, section 9).
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import gzip  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import platform  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import traceback  # noqa: E402
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait  # noqa: E402
from datetime import datetime, timezone  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_g_lib as lib  # noqa: E402

PILOT_DATASET = "adult"      # the largest mixed dataset: the slowest case for timing
PILOT_INSTANCES = 20
STAGES = ("pilot", "full", "roar", "synthetic")


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short=12", "HEAD"], cwd=lib.ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def host_id() -> str:
    return platform.node() or "unknown"


def work_dir(cfg: dict) -> Path:
    return lib.ROOT / cfg["run"]["work_dir"]


# --- shards --------------------------------------------------------------------------

def shards(stage: str, cfg: dict) -> list[dict]:
    if stage == "pilot":
        return [{"stage": stage, "dataset": PILOT_DATASET, "model": m, "seed": cfg["seeds"][0]}
                for m in lib.MODELS]
    if stage in ("full", "roar"):
        return [{"stage": stage, "dataset": d["key"], "model": m, "seed": s}
                for s in cfg["seeds"] for d in cfg["dataset"] for m in lib.MODELS]
    if stage == "synthetic":
        return [{"stage": stage, "dataset": f"{g}_rho{int(r * 100):02d}", "generator": g,
                 "rho": r, "model": "known", "seed": s}
                for s in cfg["seeds"] for g in cfg["synthetic"]["generators"]
                for r in cfg["synthetic"]["correlation"]]
    raise KeyError(stage)


def shard_name(sh: dict) -> str:
    return f"{sh['dataset']}/{sh['model']}/seed_{sh['seed']}"


def shard_path(sh: dict, cfg: dict, suffix: str) -> Path:
    return work_dir(cfg) / sh["stage"] / f"{shard_name(sh)}{suffix}"


def state(sh: dict, cfg: dict) -> str:
    if shard_path(sh, cfg, ".done").exists():
        return "done"
    if shard_path(sh, cfg, ".failed").exists():
        return "failed"
    return "todo"


# --- one shard ---------------------------------------------------------------------------

def _logger(sh: dict, cfg: dict) -> logging.Logger:
    path = work_dir(cfg) / "logs" / sh["stage"] / f"{shard_name(sh)}.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    log = logging.getLogger(f"paper_g.{sh['stage']}.{shard_name(sh)}")
    log.handlers.clear()
    h = logging.FileHandler(path, encoding="utf-8")
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    log.addHandler(h)
    log.setLevel(logging.INFO)
    log.propagate = False
    return log


def _stamp(sh: dict, commit: str) -> dict:
    return {"stage": sh["stage"], "dataset": sh["dataset"], "model": sh["model"],
            "seed": sh["seed"], "host": host_id(), "commit": commit}


def _rows_full(sh, cfg, log, n_instances=None):
    data = lib.prepare(sh["dataset"], sh["model"], sh["seed"], cfg)
    log.info("prepared: %d train, %d test, %d columns, %d groups, test AUC %.4f",
             len(data["X_train"]), len(data["X_test"]), data["X_train"].shape[1],
             len(data["groups"]), data["auc"])
    info = {"auc": data["auc"], "n_groups": len(data["groups"]),
            "n_columns": int(data["X_train"].shape[1]), "meta": data["meta"]}
    return lib.explain_and_score(data, lib.EXPLAINERS, sh["seed"], cfg, n_instances), info


def _rows_roar(sh, cfg, log):
    src = shard_path({**sh, "stage": "full"}, cfg, ".jsonl.gz")
    if not shard_path({**sh, "stage": "full"}, cfg, ".done").exists():
        raise RuntimeError(f"full shard not finished: {src}")
    attrs: dict[str, list] = {}
    with gzip.open(src, "rt", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if r.get("failed") == 0 and "attr" in r:
                attrs.setdefault(r["explainer"], []).append(r["attr"])
    data = lib.prepare(sh["dataset"], sh["model"], sh["seed"], cfg)
    log.info("roar: full-model test AUC %.4f", data["auc"])

    def gen():
        for name in lib.EXPLAINERS:
            if name not in attrs:
                yield {"explainer": name, "failed": 1, "fail_reason": "no attributions"}
                continue
            imp = np.abs(np.array(attrs[name])).mean(axis=0)
            rank = lib.order_of(imp)
            t0 = time.perf_counter()
            row = {"explainer": name, "failed": 0, "fail_reason": "",
                   "global_rank": [int(i) for i in rank], "auc_full": data["auc"]}
            row.update(lib.roar_score(rank, data, sh["model"], sh["seed"], cfg, data["auc"]))
            row["total_s"] = time.perf_counter() - t0
            log.info("roar %s done in %.1f s", name, row["total_s"])
            yield row
    return gen(), {"auc": data["auc"], "n_groups": len(data["groups"])}


def _rows_synthetic(sh, cfg, log):
    import paper_g_synthetic as syn
    from scipy.stats import spearmanr
    data = syn.make_condition(sh["generator"], sh["rho"], sh["seed"], cfg)

    def gen():
        truth = {}
        for row in lib.explain_and_score(data, lib.EXPLAINERS, sh["seed"], cfg):
            pos = row["instance"]
            if pos not in truth:
                truth[pos] = syn.true_attribution(data, pos)
            row["true_attr"] = [round(float(v), 8) for v in truth[pos]]
            if row["failed"] == 0:
                rho_t = spearmanr(row["attr"], truth[pos]).statistic
                row["spearman_truth"] = None if np.isnan(rho_t) else float(rho_t)
            yield row
    return gen(), {"generator": sh["generator"], "rho": sh["rho"]}


def run_shard(sh: dict, cfg: dict, commit: str) -> dict:
    """Compute one shard. Returns its summary; raises only for machine errors."""
    log = _logger(sh, cfg)
    out = shard_path(sh, cfg, ".jsonl.gz")
    out.parent.mkdir(parents=True, exist_ok=True)
    shard_path(sh, cfg, ".failed").unlink(missing_ok=True)
    tmp = out.with_name(out.name + ".part")
    started = time.perf_counter()
    log.info("start %s %s on %s, commit %s", sh["stage"], shard_name(sh), host_id(), commit)
    try:
        if sh["stage"] == "pilot":
            rows, info = _rows_full(sh, cfg, log, PILOT_INSTANCES)
        elif sh["stage"] == "full":
            rows, info = _rows_full(sh, cfg, log)
        elif sh["stage"] == "roar":
            rows, info = _rows_roar(sh, cfg, log)
        else:
            rows, info = _rows_synthetic(sh, cfg, log)
        n = failed = 0
        stamp = _stamp(sh, commit)
        with gzip.open(tmp, "wt", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps({**stamp, **row}) + "\n")
                n += 1
                failed += int(row.get("failed", 0))
                if failed and row.get("failed"):
                    log.warning("failed row: %s %s: %s", row.get("explainer"),
                                row.get("instance"), row.get("fail_reason"))
                if n % 100 == 0:
                    log.info("%d rows", n)
        tmp.replace(out)
        summary = {**_stamp(sh, commit), **info, "rows": n, "failed_rows": failed,
                   "seconds": round(time.perf_counter() - started, 1), "finished": now(),
                   "peak_rss_mib": _peak_rss_mib()}
        shard_path(sh, cfg, ".done").write_text(json.dumps(summary, indent=1), encoding="utf-8")
        log.info("done: %d rows, %d failed, %.1f s", n, failed, summary["seconds"])
        return summary
    except Exception as exc:
        tb = traceback.format_exc()
        log.error("shard failed: %s\n%s", exc, tb)
        shard_path(sh, cfg, ".failed").write_text(json.dumps(
            {**_stamp(sh, commit), "error": f"{type(exc).__name__}: {exc}"[:500],
             "at": now()}, indent=1), encoding="utf-8")
        tmp.unlink(missing_ok=True)
        return {"failed": True, "shard": shard_name(sh), "error": str(exc)[:500]}


def _peak_rss_mib() -> float | None:
    try:
        import resource
        return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1)  # Linux: KiB
    except Exception:
        return None


def _worker(sh, cfg, commit):
    return run_shard(sh, cfg, commit)


# --- main loop -------------------------------------------------------------------------------

def free_memory_gib() -> float | None:
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemAvailable:"):
                return int(line.split()[1]) / 1024**2
    except OSError:
        return None
    return None


def write_heartbeat(cfg, stage, jobs, todo, running, done, failed, started):
    path = work_dir(cfg) / "heartbeat.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "stage": stage, "jobs": jobs, "host": host_id(), "commit": git_commit(),
        "started": started, "heartbeat": now(), "todo": todo, "running": running,
        "done": done, "failed": failed, "free_memory_gib": free_memory_gib(),
        "pid": os.getpid()}, indent=1), encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--stage", choices=STAGES, required=True)
    ap.add_argument("--jobs", type=int)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args(argv)
    cfg = lib.config()
    jobs = args.jobs or cfg["run"]["jobs"]
    all_shards = shards(args.stage, cfg)
    if args.list:
        for sh in all_shards:
            print(f"{state(sh, cfg):7s} {shard_name(sh)}")
        return 0
    if args.stage in ("pilot", "full", "roar"):
        for d in {sh["dataset"] for sh in all_shards}:
            lib.fetch(lib.dataset_entry(d, cfg))    # download once, before the workers start
    pending = [sh for sh in all_shards if state(sh, cfg) != "done"]
    commit, started = git_commit(), now()
    min_free = cfg["run"]["min_free_memory_gib"]
    print(f"{args.stage}: {len(all_shards) - len(pending)} of {len(all_shards)} shards done; "
          f"{len(pending)} to run with {jobs} jobs (commit {commit})", flush=True)
    done = len(all_shards) - len(pending)
    failed = 0
    running = {}
    last_beat = 0.0
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        while pending or running:
            free = free_memory_gib()
            while pending and len(running) < jobs and (free is None or free >= min_free or not running):
                sh = pending.pop(0)
                running[pool.submit(_worker, sh, cfg, commit)] = sh
            finished, _ = wait(list(running), timeout=30, return_when=FIRST_COMPLETED)
            for fut in finished:
                sh = running.pop(fut)
                result = fut.result()
                if result.get("failed"):
                    failed += 1
                    print(f"{now()} FAILED {shard_name(sh)}: {result['error']}", flush=True)
                else:
                    done += 1
                    print(f"{now()} done {shard_name(sh)} ({done}/{len(all_shards)}, "
                          f"{result['seconds']} s)", flush=True)
            if time.time() - last_beat >= 30 or finished:
                write_heartbeat(cfg, args.stage, jobs, len(pending),
                                [shard_name(s) for s in running.values()], done, failed, started)
                last_beat = time.time()
    write_heartbeat(cfg, args.stage, jobs, 0, [], done, failed, started)
    print(f"{args.stage}: finished; {done} done, {failed} failed", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
