#!/usr/bin/env python3
"""Paper F: run one condition (dataset, model, seed, explainer), or launch many.

One job explains the chosen instances of one dataset, model and seed with one explainer
and appends one JSON line per instance. A job that is run again skips the instances it
already holds, so an interrupted run is resumed by running the same command.

    python scripts/paper_f_run.py job --dataset adult --model rf --seed 42 --explainer lime
    python scripts/paper_f_run.py launch --workers 10            # every job of datasets.csv
    python scripts/paper_f_run.py launch --pilot                 # plan section 7, step 4
    python scripts/paper_f_run.py status

Results: outputs/analysis/paper_f/runs/<dataset>/<model>/seed_<seed>/<explainer>.jsonl
The pilot writes to outputs/analysis/paper_f/pilot/ and is not a result.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import subprocess
import sys
import time
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_f_lib as lib  # noqa: E402


def job_path(root: Path, dataset: str, model: str, seed: int, explainer: str) -> Path:
    return root / dataset / model / f"seed_{seed}" / f"{explainer}.jsonl"


def read_done(path: Path) -> set[int]:
    done = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                done.add(int(json.loads(line)["instance"]))
            except (ValueError, KeyError):
                continue
    return done


def append(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")


def run_job(args) -> int:
    cfg = lib.config()
    root = Path(args.out)
    path = job_path(root, args.dataset, args.model, args.seed, args.explainer)
    path.parent.mkdir(parents=True, exist_ok=True)
    beat = path.with_suffix(".heartbeat")
    marker = path.with_suffix(".done")
    if marker.exists():
        return 0
    data = lib.prepare(args.dataset, args.model, args.seed, cfg)
    instances = data["instances"][:args.limit] if args.limit else data["instances"]
    done = read_done(path)
    todo = [int(i) for i in instances if int(i) not in done]
    if not todo:
        marker.write_text(str(len(instances)), encoding="utf-8")
        return 0
    explainer = lib.make_explainer(args.explainer, data["model"], data, args.seed, cfg)
    for pos in todo:
        beat.write_text(json.dumps({"instance": pos, "started": time.time()}), encoding="utf-8")
        row = {"dataset": args.dataset, "model": args.model, "seed": args.seed,
               "explainer": args.explainer, "instance": pos,
               "y": int(data["y_test"][pos]), "pred": int(data["pred"][pos])}
        row.update(lib.evaluate(explainer, data["X_test"][pos], pos, data["base"], cfg))
        append(path, row)
    beat.unlink(missing_ok=True)
    marker.write_text(str(len(instances)), encoding="utf-8")
    return 0


# --- launcher ------------------------------------------------------------------

def study_datasets() -> list[str]:
    with (lib.OUT / "datasets.csv").open(encoding="utf-8") as fh:
        return [r["key"] for r in csv.DictReader(fh)]


def expected(root: Path, cfg: dict, limit: int) -> int:
    return limit or cfg["n_instances"]


def ordered_jobs(datasets, models, seeds, explainers) -> list[tuple]:
    """Jobs (dataset, model, seed, explainer) in the order they are started: seed after
    seed, and inside a seed in a fixed shuffled order, the same for every seed.

    The shuffle mixes long and short jobs, so that the memory-heavy ones (Anchors on the
    random forest) do not all run at the same time. The seeds are kept in order so that
    each one is complete before most of the next is run; when a seed has fewer jobs left
    than there are workers, the free workers take jobs of the next seed (plan section 12,
    2026-10-07: the last job of seed 42 ran alone for ten hours).
    """
    jobs = []
    for s in seeds:
        part = [(d, m, s, e) for d in datasets for m in models for e in explainers]
        random.Random(20261005).shuffle(part)
        jobs += part
    return jobs


def requeue(queue: list[tuple], job: tuple, seeds: list[int]) -> None:
    """Put a job back behind the queued jobs of its own seed, before those of later seeds."""
    rank = seeds.index(job[2])
    pos = next((i for i, q in enumerate(queue) if seeds.index(q[2]) > rank), len(queue))
    queue.insert(pos, job)


def launch(args) -> int:
    cfg = lib.config()
    if args.pilot:
        root, datasets, seeds, limit = lib.OUT / "pilot", args.datasets or ["adult"], [42], 20
    else:
        root = Path(args.out)
        datasets, seeds, limit = args.datasets or study_datasets(), args.seeds or cfg["seeds"], args.limit
    seeds = list(dict.fromkeys(seeds))
    jobs = ordered_jobs(datasets, args.models or lib.MODELS, seeds,
                        args.explainers or lib.EXPLAINERS)
    stop = root / "_STOP"
    begun: set[int] = set()
    limit_s = cfg["run"]["time_limit_s"]
    logs = root / "_logs"
    logs.mkdir(parents=True, exist_ok=True)
    running: dict[tuple, subprocess.Popen] = {}
    born: dict[tuple, float] = {}
    retries: dict[tuple, int] = {}
    failed: list[tuple] = []
    started = time.time()

    def start(job: tuple) -> None:
        d, m, s, e = job
        cmd = [sys.executable, __file__, "job", "--dataset", d, "--model", m, "--seed", str(s),
               "--explainer", e, "--out", str(root)] + (["--limit", str(limit)] if limit else [])
        log = (logs / f"{d}_{m}_{s}_{e}.log").open("a", encoding="utf-8")
        running[job] = subprocess.Popen(cmd, stdout=log, stderr=log, cwd=lib.ROOT)
        born[job] = time.time()

    def again(job: tuple) -> None:
        """A job that stopped for a reason of the machine is run again, up to five times."""
        retries[job] = retries.get(job, 0) + 1
        if retries[job] <= 5:
            requeue(queue, job, seeds)
        else:
            failed.append(job)

    queue = list(jobs)
    while queue or running:
        while queue and len(running) < args.workers:
            # With the stop file, a seed that has not begun is not begun.
            if queue[0][2] not in begun and stop.exists():
                break
            begun.add(queue[0][2])
            start(queue.pop(0))
        if queue and not running and stop.exists():
            print(f"{time.strftime('%H:%M:%S')} stop file found; {len(queue)} jobs left "
                  f"in the queue", flush=True)
            return 0
        time.sleep(2)
        for job, proc in list(running.items()):
            path = job_path(root, *job)
            beat = path.with_suffix(".heartbeat")
            code = proc.poll()
            if code is None and limit_s:
                hb = None
                if beat.exists():
                    try:
                        hb = json.loads(beat.read_text(encoding="utf-8"))
                    except ValueError:
                        continue
                if hb and time.time() - hb["started"] > limit_s:
                    # One instance took too long: a failure of the method on that instance.
                    proc.kill()
                    proc.wait()
                    append(path, {"dataset": job[0], "model": job[1], "seed": job[2],
                                  "explainer": job[3], "instance": hb["instance"], "failed": 1,
                                  "fail_reason": f"time limit of {limit_s} s"})
                    beat.unlink(missing_ok=True)
                    del running[job]
                    queue.insert(0, job)
                elif not hb and time.time() - born[job] > limit_s:
                    # Stuck before the first instance (loading, training): the machine.
                    proc.kill()
                    proc.wait()
                    del running[job]
                    again(job)
                continue
            if code is None:
                continue
            del running[job]
            if code != 0:
                again(job)
        if int(time.time() - started) % 300 < 2:
            print(f"{time.strftime('%H:%M:%S')} running {len(running)} queued {len(queue)} "
                  f"failed {len(failed)}", flush=True)
    print(f"finished in {(time.time() - started) / 3600:.2f} h; {len(jobs) - len(failed)} of "
          f"{len(jobs)} jobs completed")
    for job in failed:
        print("FAILED", *job)
    return 1 if failed else 0


def status(args) -> int:
    root = Path(args.out)
    rows = fails = files = 0
    for path in root.glob("*/*/seed_*/*.jsonl"):
        files += 1
        for line in path.read_text(encoding="utf-8").splitlines():
            rows += 1
            fails += '"failed": 1' in line
    print(f"{files} job files, {rows} instance rows, {fails} failures under {root}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="command", required=True)
    default_out = str(lib.OUT / "runs")
    j = sub.add_parser("job")
    j.add_argument("--dataset", required=True)
    j.add_argument("--model", required=True, choices=lib.MODELS)
    j.add_argument("--seed", required=True, type=int)
    j.add_argument("--explainer", required=True, choices=lib.EXPLAINERS)
    j.add_argument("--limit", type=int, default=0)
    j.add_argument("--out", default=default_out)
    l = sub.add_parser("launch")
    l.add_argument("--workers", type=int, default=10)
    l.add_argument("--pilot", action="store_true")
    l.add_argument("--datasets", nargs="*")
    l.add_argument("--models", nargs="*")
    l.add_argument("--explainers", nargs="*")
    l.add_argument("--seeds", nargs="*", type=int)
    l.add_argument("--limit", type=int, default=0)
    l.add_argument("--out", default=default_out)
    s = sub.add_parser("status")
    s.add_argument("--out", default=default_out)
    args = ap.parse_args()
    if args.command == "job":
        # Leave without the interpreter's shutdown: after a native crash in a library its
        # threads can keep the process alive, and the launcher would wait for it.
        try:
            code = run_job(args)
        except BaseException:
            traceback.print_exc()
            code = 1
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(code)
    return {"launch": launch, "status": status}[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
