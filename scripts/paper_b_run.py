#!/usr/bin/env python3
"""Paper B revision 1 (cohort B2): prepare, run and resume the experiments.

    python scripts/paper_b_run.py preflight            checks before anything heavy
    python scripts/paper_b_run.py prepare              datasets + models, frozen by hash
    python scripts/paper_b_run.py pilot                every dataset x model x explainer, 4 instances
    python scripts/paper_b_run.py launch               the quality pass (parallel, governed)
    python scripts/paper_b_run.py launch-timing        the timing pass (alone, quiet host only)
    python scripts/paper_b_run.py status               counts of done / failed jobs
    python scripts/paper_b_run.py job ...              one quality job (used by launch)
    python scripts/paper_b_run.py timing ...           one timing cell (used by launch-timing)

Every command can be stopped (Ctrl+C, or create outputs/paper_b_rev1_live/_STOP) and run
again: finished instances are never recomputed. Design: experiments/exp_b_rev1/cohort.toml;
plan: docs/reports/paper_b/ci_journal/revision_1/RUNS_IMPLEMENTATION_PLAN.md.
"""
from __future__ import annotations

import os
import sys

# Workers must be single-threaded before numpy is imported anywhere.
if len(sys.argv) > 1 and sys.argv[1] in ("job", "timing"):
    for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
               "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        os.environ[_v] = "1"

import argparse  # noqa: E402
import json  # noqa: E402
import random  # noqa: E402
import signal  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import traceback  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import paper_b_lib as lib  # noqa: E402

EXIT_FATAL = 2      # do not retry (model hash mismatch, bad arguments)


def log(msg: str) -> None:
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}", flush=True)


def root_of(args) -> Path:
    return Path(args.root) if getattr(args, "root", None) else lib.RESULTS


# ==========================================================================
# preflight
# ==========================================================================
def cmd_preflight(args) -> int:
    import psutil
    cfg = lib.config()
    res = cfg["resources"]
    problems, notes = [], []
    snap = lib.host_snapshot()
    if sys.version_info[:2] != (3, 11):
        problems.append(f"Python {sys.version.split()[0]}: the pinned environment is 3.11 (.venv)")
    pins = {"numpy": "2.2.6", "scikit-learn": "1.7.1", "xgboost": "3.1.2", "shap": "0.50.0",
            "lime": "0.2.0.1", "pandas": "2.3.3", "scipy": "1.16.3"}
    pk = lib.static_host_record()["packages"]
    for p, v in pins.items():
        if pk.get(p) != v:
            problems.append(f"{p} {pk.get(p)} != pinned {v}")
    for p in ("alibi", "dice-ml", "psutil"):
        if not pk.get(p):
            problems.append(f"{p} not installed")
    if snap["ac_power"] is False:
        problems.append("on battery: connect the charger")
    if snap["disk_free_gb"] < res["disk_min_gb"]:
        problems.append(f"disk free {snap['disk_free_gb']:.1f} GB < {res['disk_min_gb']} GB")
    if snap["ram_available_gb"] < res["ram_reserve_gb"] + res["default_peak_gb"]:
        problems.append(f"RAM available {snap['ram_available_gb']:.1f} GB is too low to start "
                        f"(needs {res['ram_reserve_gb'] + res['default_peak_gb']:.0f} GB): close "
                        "a browser or other large programs (RUNBOOK.md, section 4)")
    notes.append(f"logical CPUs {snap['logical_cpus']}; workers will be "
                 f"{min(res['max_workers'], max(1, (snap['logical_cpus'] or 2) - 2))}")
    r = subprocess.run(["git", "ls-remote", "--heads", cfg["sync"]["remote"]], cwd=lib.ROOT,
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        problems.append("git remote not reachable: pushes would fail")
    if sys.platform == "win32":
        r = subprocess.run(["powercfg", "/query", "SCHEME_CURRENT", "SUB_SLEEP", "STANDBYIDLE"],
                           capture_output=True, text=True, timeout=20)
        ac = [l for l in r.stdout.splitlines() if "Current AC Power Setting Index" in l]
        if ac and int(ac[0].split(":")[-1].strip(), 16) != 0:
            notes.append("Windows sleeps on AC after "
                         f"{int(ac[0].split(':')[-1].strip(), 16) // 60} min idle: the runner "
                         "blocks sleep while it runs, but setting 'Never' on AC is safer "
                         "(RUNBOOK.md)")
    others = running_runner_pids()
    if others:
        problems.append(f"another paper_b_run.py is running: pids {others}")
    if not lib.MANIFEST.exists():
        notes.append("models not frozen yet: run `prepare`")
    for n in notes:
        log(f"note: {n}")
    for p in problems:
        log(f"PROBLEM: {p}")
    log("preflight " + ("FAILED" if problems else "passed"))
    lib.atomic_write_json(lib.STATE / "preflight.json",
                          {"time": time.time(), "problems": problems, "notes": notes,
                           "snapshot": snap})
    return 1 if problems else 0


# ==========================================================================
# prepare: datasets and frozen models
# ==========================================================================
def cmd_prepare(args) -> int:
    import joblib
    import numpy as np
    cfg = lib.config()
    max_mb = cfg["sync"]["max_file_mb"]
    datasets = args.datasets or list(cfg["datasets"])
    models = args.models or list(cfg["models"])
    manifest = lib.read_manifest()
    for d in datasets:
        cached = lib.DATA_DIR / f"{d}.npz"
        if getattr(args, "keep_data", False) and cached.exists():
            log(f"dataset {d}: kept as prepared (--keep-data)")
            dd = lib.load_dataset(d)
            summary = {"sha256": lib.sha256_file(cached), "n_train": len(dd["y_train"]),
                       "n_test": len(dd["y_test"]), "n_features": dd["X_train"].shape[1],
                       "positive_rate": float(np.mean(np.concatenate([dd["y_train"],
                                                                      dd["y_test"]])))}
        else:
            log(f"dataset {d}: preparing")
            summary = lib.prepare_dataset(d, cfg)
        log(f"dataset {d}: {summary['n_train']} train / {summary['n_test']} test rows, "
            f"{summary['n_features']} features, positive rate {summary['positive_rate']:.3f}")
        data = lib.load_dataset(d)
        idx = lib.training_subsample(data["y_train"], cfg["cohort"]["max_train_rows"],
                                     cfg["cohort"]["split_seed"])
        for m in models:
            path = lib.model_path(d, m)
            if (d, m) in manifest and path.exists() and not args.force:
                log(f"  {d}/{m}: frozen already ({manifest[(d, m)]['sha256'][:12]}), kept")
                continue
            est = lib.build_model(cfg["models"][m])
            t = time.time()
            est.fit(data["X_train"][idx], data["y_train"][idx])
            acc = float(np.mean(est.predict(data["X_test"]) == data["y_test"]))
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
            joblib.dump(est, tmp, compress=3)
            size = tmp.stat().st_size
            if size > max_mb * 2**20:
                tmp.unlink()
                log(f"  {d}/{m}: REFUSED, {size / 2**20:.1f} MB > {max_mb} MB limit")
                return 1
            os.replace(tmp, path)
            manifest[(d, m)] = {
                "dataset": d, "model": m, "file": path.relative_to(lib.ROOT).as_posix(),
                "sha256": lib.sha256_file(path), "bytes": size, "train_rows": len(idx),
                "test_accuracy": f"{acc:.4f}",
                "trained_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "structure": json.dumps(lib.model_structure(est)),
                "data_sha256": summary["sha256"]}
            lib.write_manifest(manifest)
            log(f"  {d}/{m}: trained in {time.time() - t:.0f} s on {len(idx)} rows, "
                f"test accuracy {acc:.4f}, {size / 2**20:.1f} MB")
    log(f"manifest: {lib.MANIFEST.relative_to(lib.ROOT)}")
    return 0


# ==========================================================================
# job: one quality job (dataset, model, seed, explainer variant)
# ==========================================================================
def cmd_job(args) -> int:
    import numpy as np
    import psutil
    from src.metrics import FaithfulnessMetric, SparsityMetric, StabilityMetric

    cfg = lib.config()
    if cfg["resources"].get("below_normal_priority", True):
        lib.set_below_normal()
    d, m, s, e = args.dataset, args.model, int(args.seed), args.explainer
    stem = root_of(args) / "quality" / d / m / f"seed_{s}" / e
    out, beat = stem.with_suffix(".jsonl"), stem.with_suffix(".heartbeat")
    done, meta_path = stem.with_suffix(".done"), stem.with_suffix(".meta.json")
    if done.exists():
        return 0
    try:
        model, msha = lib.load_model_checked(d, m)
    except lib.ModelHashMismatch as exc:
        log(f"FATAL {exc}")
        return EXIT_FATAL
    data = lib.load_dataset(d)
    per = args.per_stratum or cfg["sampling"]["per_stratum"]
    k_stab = args.stability_per_stratum if args.stability_per_stratum is not None \
        else cfg["sampling"]["stability_per_stratum"]
    inst = lib.select_instances(model, data, s, per)
    stab_ids = lib.first_per_stratum(inst, k_stab)
    explainer, info = lib.build_explainer(e, cfg, m, model, data, s)
    mc = cfg["metrics"]
    chash = lib.config_hash()
    if not meta_path.exists():
        counts = inst["quadrant"].value_counts().to_dict()
        lib.atomic_write_json(meta_path, {
            "job": [d, m, s, e], "cohort_sha256": chash, "model_sha256": msha,
            "git_commit": lib.git_commit(), "explainer": info, "host": lib.static_host_record(),
            "per_stratum": per, "stability_per_stratum": k_stab,
            "realised_strata": {q: int(counts.get(q, 0)) for q in lib.STRATA},
            "instance_ids": [int(i) for i in inst["original_index"]],
            "stability_ids": sorted(stab_ids), "started_utc": time.time()})
    have = lib.done_keys(out)
    proc = psutil.Process()
    peak = proc.memory_info().rss
    n_ok = n_fail = 0
    t_job = time.time()
    store, digits = mc.get("store_vectors", True), mc.get("vector_digits", 6)
    # WP4 controls: the same instance selection as the main cohort, but only its stability
    # subset is computed (optional; the main configuration does not set it).
    only_stab = bool(cfg["sampling"].get("stability_only", False))
    for _, row in inst.iterrows():
        iid = int(row["original_index"])
        if iid in have or (only_stab and iid not in stab_ids):
            continue
        if lib.STOP.exists() and not args.ignore_stop:
            log("stop file: leaving after the last finished instance")
            break
        lib.atomic_write_json(beat, {"instance": iid, "started": time.time(), "pid": os.getpid(),
                                     "job": [d, m, s, e]})
        np.random.seed(lib.instance_seed(s, d, m, e, iid))
        x = row.drop(labels=lib.META_COLS).values.astype(float)
        rec = {"instance_id": iid, "quadrant": row["quadrant"], "target": int(row["target"]),
               "prediction": int(row["prediction"]), "cohort_sha256": chash,
               "model_sha256": msha, "time": time.time()}
        try:
            t0 = time.perf_counter()
            w, _meta = explainer.explain_instance(model, x, return_full=True)
            rec["explain_wall_ms"] = (time.perf_counter() - t0) * 1e3
            w = np.asarray(w, dtype=float)
            rec["sparsity"] = float(SparsityMetric(threshold=mc["sparsity_threshold"])
                                    .compute(w)["nonzero_percentage"])
            fm = FaithfulnessMetric(top_k=mc["fidelity_top_k"])
            fm.baseline_values = data["baseline"]
            fres = fm.compute(w, model=model, data=x)
            rec["fidelity"] = float(fres["faithfulness_score"])
            rec["faithfulness_gap"] = float(fres["faithfulness_gap"])
            rec["all_zero"] = bool(np.all(np.abs(w) < mc["sparsity_threshold"]))
            if store:
                rec["weights"] = lib.round_vec(w, digits)
            if iid in stab_ids:
                vecs = []

                def efunc(mod, dd, _vecs=vecs):
                    v = np.asarray(explainer.explain_instance(mod, dd[0], return_full=False),
                                   dtype=float)
                    _vecs.append(v)
                    return {"feature_importance": v}

                noise = mc.get("stability_noise", "gaussian_all")
                if noise == "gaussian_all":                       # the main protocol
                    sm = StabilityMetric(n_iterations=mc["stability_T"],
                                         perturbation_std=mc["stability_sigma"])
                elif noise == "onehot_valid":                     # WP4 control (b)
                    sm = lib.ValidStabilityMetric(
                        mc["stability_T"], mc["stability_sigma"], data["X_train"],
                        data["feature_names"], mc.get("onehot_resample_p", 0.1))
                else:
                    raise ValueError(f"unknown stability_noise {noise!r}")
                sres = sm.compute(None, model=model, data=x, explainer_func=efunc)
                rec["stability"] = float(sres["cosine_similarity_mean"])
                rec["stability_zero_vectors"] = int(sum(
                    np.all(np.abs(v) < mc["sparsity_threshold"]) for v in vecs))
                if store:
                    rec["stability_vectors"] = [lib.round_vec(v, digits) for v in vecs]
            n_ok += 1
        except Exception as exc:
            rec.update({"failed": 1, "fail_reason": f"{type(exc).__name__}: {exc}"[:500],
                        "traceback": traceback.format_exc(limit=4)[-2000:]})
            n_fail += 1
        lib.append_jsonl(out, rec)
        peak = max(peak, proc.memory_info().rss)
    beat.unlink(missing_ok=True)
    if lib.STOP.exists() and not args.ignore_stop:
        return 0
    wanted = {int(i) for i in stab_ids} if only_stab else {int(i) for i in inst["original_index"]}
    remaining = wanted - lib.done_keys(out)
    if remaining:
        log(f"{len(remaining)} instances still missing; not marking done")
        return 1
    rows = list(lib.read_jsonl(out))
    lib.atomic_write_json(done, {"rows": len(rows), "failed": sum(r.get("failed", 0) for r in rows),
                                 "peak_rss_gb": peak / 2**30, "elapsed_s": time.time() - t_job,
                                 "finished": time.time()})
    return 0


# ==========================================================================
# timing: one cell, every explainer interleaved, alone on a quiet host
# ==========================================================================
def cmd_timing(args) -> int:
    import numpy as np
    import psutil

    cfg = lib.config()
    tc = cfg["timing"]
    d, m, s = args.dataset, args.model, int(args.seed)
    stem = root_of(args) / "timing" / d / m / f"seed_{s}" / "timing"
    out, beat = stem.with_suffix(".jsonl"), stem.with_suffix(".heartbeat")
    done, meta_path = stem.with_suffix(".done"), stem.with_suffix(".meta.json")
    if done.exists():
        return 0
    pin = lib.pin_to_cpu(int(tc["cpu"]))
    counter = lib.CallCounter()
    counted = lib.install_counter(counter, lib.model_classes())   # before any explainer
    try:
        model, msha = lib.load_model_checked(d, m)
    except lib.ModelHashMismatch as exc:
        log(f"FATAL {exc}")
        return EXIT_FATAL
    for est in [model]:
        for attr in ("n_jobs", "nthread"):
            if attr in getattr(est, "get_params", lambda: {})():
                est.set_params(**{attr: 1})
    data = lib.load_dataset(d)
    per = args.per_stratum or cfg["sampling"]["per_stratum"]
    inst = lib.select_instances(model, data, s, per)
    timed_ids = lib.first_per_stratum(inst, args.timing_per_stratum or tc["per_stratum"])
    inst = inst[inst["original_index"].astype(int).isin(timed_ids)]
    variants = args.explainers or list(cfg["explainers"])
    explainers, infos = {}, {}
    for e in variants:
        explainers[e], infos[e] = lib.build_explainer(e, cfg, m, model, data, s)
    if not meta_path.exists():
        lib.atomic_write_json(meta_path, {
            "cell": [d, m, s], "explainers": variants, "cohort_sha256": lib.config_hash(),
            "model_sha256": msha, "git_commit": lib.git_commit(), "affinity": pin,
            "counted_methods": counted, "explainer_info": infos, "host": lib.static_host_record(),
            "timer_cpu_resolution_s": time.get_clock_info("process_time").resolution,
            "instance_ids": sorted(timed_ids), "repeats": tc["repeats"],
            "started_utc": time.time()})
    have = {(r["instance_id"], r["explainer"]) for r in lib.read_jsonl(out)}
    rows = list(inst.iterrows())
    x0 = rows[0][1].drop(labels=lib.META_COLS).values.astype(float) if rows else None
    for e in variants:                       # warm-up: lazy set-up of Anchors, DiCE, ...
        for _ in range(int(tc["warmup_per_explainer"])):
            if x0 is not None:
                try:
                    explainers[e].explain_instance(model, x0, return_full=True)
                except Exception:
                    pass
    psutil.cpu_percent(interval=None)
    for i, (_, row) in enumerate(rows):
        iid = int(row["original_index"])
        x = row.drop(labels=lib.META_COLS).values.astype(float)
        order = variants[i % len(variants):] + variants[:i % len(variants)]
        if i % 2:
            order = order[::-1]                       # ABBA-like rotation
        bench = lib.microbenchmark() if i % int(tc["benchmark_every_instances"]) == 0 else None
        for pos, e in enumerate(order):
            if (iid, e) in have:
                continue
            waited = 0.0
            while True:                               # quiet-host gate
                if lib.STOP.exists() and not args.ignore_stop:
                    log("stop file: timing left after the last finished explanation")
                    beat.unlink(missing_ok=True)
                    return 0
                other = psutil.cpu_percent(interval=2.0)
                snap = lib.host_snapshot()
                ok, why = lib.quiet_gate(
                    other, lib.idle_seconds(), snap["ac_power"], tc["max_other_cpu_percent"],
                    60 * tc["require_idle_minutes"] if args.require_idle else None,
                    quality_workers_running=count_quality_workers())
                if ok:
                    break
                lib.atomic_write_json(lib.STATE / "timing_gate.json",
                                      {"time": time.time(), "waiting": True, "reason": why,
                                       "cell": [d, m, s], "instance": iid, "explainer": e})
                time.sleep(float(tc["gate_poll_s"]))
                waited += float(tc["gate_poll_s"]) + 2.0
            lib.atomic_write_json(beat, {"instance": iid, "explainer": e, "started": time.time(),
                                         "pid": os.getpid()})
            reps = []
            for _r in range(int(tc["repeats"])):
                counter.reset()
                c0, w0 = time.process_time(), time.perf_counter()
                err = None
                try:
                    explainers[e].explain_instance(model, x, return_full=True)
                except Exception as exc:
                    err = f"{type(exc).__name__}: {exc}"[:300]
                reps.append({"wall_ms": (time.perf_counter() - w0) * 1e3,
                             "cpu_ms": (time.process_time() - c0) * 1e3,
                             "model_calls": counter.calls, "rows": counter.rows, "error": err})
            snap = lib.host_snapshot()
            lib.append_jsonl(out, {"instance_id": iid, "quadrant": row["quadrant"],
                                   "explainer": e, "order_pos": pos, "order": order,
                                   "reps": reps, "bench_ms": bench, "cpu_mhz": snap["cpu_mhz"],
                                   "gate_wait_s": waited, "time": time.time()})
            lib.atomic_write_json(lib.STATE / "timing_gate.json",
                                  {"time": time.time(), "waiting": False, "cell": [d, m, s],
                                   "instance": iid, "explainer": e})
    beat.unlink(missing_ok=True)
    got = {(r["instance_id"], r["explainer"]) for r in lib.read_jsonl(out)}
    need = {(int(i), e) for i in timed_ids for e in variants}
    if need - got:
        return 1
    lib.atomic_write_json(done, {"rows": len(got), "finished": time.time()})
    return 0


def _runner_procs(subcommands: tuple[str, ...] | None = None) -> list[int]:
    """PIDs of Python processes executing this script (optionally with one of the given
    subcommands), excluding this process and its ancestors (shells, the venv launcher)."""
    import psutil
    me = psutil.Process()
    skip = {me.pid} | {p.pid for p in me.parents()}
    pids = []
    for p in psutil.process_iter(["pid", "name", "cmdline"]):
        cl = p.info.get("cmdline") or []
        if p.info["pid"] in skip or not cl or "python" not in (p.info.get("name") or "").lower():
            continue
        idx = next((i for i, c in enumerate(cl) if c.endswith("paper_b_run.py")), None)
        if idx is None:
            continue
        sub = cl[idx + 1] if idx + 1 < len(cl) else ""
        if subcommands is None or sub in subcommands:
            pids.append(p.info["pid"])
    return pids


def running_runner_pids() -> list[int]:
    return _runner_procs()


def count_quality_workers() -> int:
    """Quality workers running; a venv launcher and its interpreter count once."""
    import psutil
    pids = set(_runner_procs(("job",)))
    roots = {p for p in pids
             if not any(a.pid in pids for a in psutil.Process(p).parents())} if pids else set()
    return len(roots)


# ==========================================================================
# launch: the governed quality pass
# ==========================================================================
class Governor:
    """Starts quality jobs as subprocesses within the memory, CPU, disk and power limits,
    kills hung or oversized workers, retries, and writes its state for the dashboard."""

    def __init__(self, args, jobs: list[tuple], root: Path, extra: list[str]):
        import psutil
        self.psutil = psutil
        self.args, self.root, self.extra = args, root, extra
        self.cfg = lib.config()
        self.res = self.cfg["resources"]
        cpus = psutil.cpu_count() or 2
        self.max_workers = max(1, min(args.workers or self.res["max_workers"], cpus - 2))
        self.queue = list(jobs)
        self.running: dict[tuple, dict] = {}
        self.retries: dict[tuple, int] = {}
        self.alone: set[tuple] = set()
        self.failed: dict[tuple, str] = {}
        self.finished = 0
        self.peaks = lib.read_json(lib.STATE / "peaks.json", {}) or {}
        self.reason = ""
        self.stopping = False
        self.started = time.time()
        self.last_bench = 0.0
        lib.LOGS.mkdir(parents=True, exist_ok=True)

    # -- helpers ---------------------------------------------------------
    def stem(self, job):
        d, m, s, e = job
        return self.root / "quality" / d / m / f"seed_{s}" / e

    def start(self, job):
        d, m, s, e = job
        cmd = [sys.executable, str(Path(__file__).resolve()), "job", "--dataset", d,
               "--model", m, "--seed", str(s), "--explainer", e, "--root", str(self.root),
               *self.extra]
        # A heartbeat left by a killed worker would make the new one look over its time limit
        # before it writes its own (it was killed again at once, in a loop: 2026-11-07).
        self.stem(job).with_suffix(".heartbeat").unlink(missing_ok=True)
        logf = open(lib.LOGS / f"{d}_{m}_{s}_{e}.log", "a", encoding="utf-8")
        flags = subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
        proc = subprocess.Popen(cmd, stdout=logf, stderr=subprocess.STDOUT, cwd=lib.ROOT,
                                creationflags=flags)
        self.running[job] = {"proc": proc, "log": logf, "born": time.time(), "peak_gb": 0.0}
        log(f"start {d}/{m}/seed {s}/{e} (pid {proc.pid})")

    def kill(self, job, why: str):
        w = self.running.get(job)
        if not w:
            return
        try:
            parent = self.psutil.Process(w["proc"].pid)
            for c in parent.children(recursive=True):
                c.kill()
            parent.kill()
        except self.psutil.Error:
            pass
        try:
            w["proc"].wait(timeout=30)
        except subprocess.TimeoutExpired:
            pass
        w["log"].close()
        del self.running[job]
        log(f"killed {'/'.join(map(str, job))}: {why}")

    def retry(self, job, why: str, alone: bool = False):
        self.retries[job] = self.retries.get(job, 0) + 1
        if alone:
            self.alone.add(job)
        if self.retries[job] > self.res["max_retries"]:
            self.failed[job] = why
            log(f"FAILED {'/'.join(map(str, job))} after {self.retries[job] - 1} retries: {why}")
        else:
            self.queue.insert(0, job)

    def record_peak(self, job, gb: float):
        d, m, _s, e = job
        for key in (f"{d}|{m}|{e}", f"{m}|{e}"):
            self.peaks.setdefault(key, []).append(round(gb, 3))
            self.peaks[key] = self.peaks[key][-50:]
        lib.atomic_write_json(lib.STATE / "peaks.json", self.peaks)

    # -- one supervision step ----------------------------------------------
    def step(self):
        snap = lib.host_snapshot()
        now = time.time()
        # Measure workers; enforce the per-worker cap.
        for job, w in list(self.running.items()):
            gb = lib.process_tree_rss_gb(w["proc"].pid)
            w["rss_gb"] = gb
            w["peak_gb"] = max(w["peak_gb"], gb)
            if gb > self.res["worker_cap_gb"]:
                self.kill(job, f"RSS {gb:.1f} GB > cap {self.res['worker_cap_gb']} GB")
                self.append_failed_instance(job, f"memory cap {self.res['worker_cap_gb']} GB")
                self.retry(job, "memory cap", alone=True)
        # System memory pressure: kill the newest worker.
        if snap["ram_available_gb"] < self.res["kill_newest_below_gb"] and self.running:
            newest = max(self.running, key=lambda j: self.running[j]["born"])
            self.kill(newest, f"system RAM available {snap['ram_available_gb']:.1f} GB")
            self.retry(newest, "system memory pressure", alone=True)
        # Heartbeats: per-instance time limit and stuck start-up.
        for job, w in list(self.running.items()):
            beat = lib.read_json(self.stem(job).with_suffix(".heartbeat"))
            if beat and beat.get("started", 0) < w["born"] - 1:
                beat = None                   # written by an earlier, killed worker
            if beat:
                w["beat_seen"] = True
            w["instance"] = beat.get("instance") if beat else None
            w["instance_started"] = beat.get("started") if beat else None
            if w["proc"].poll() is not None or self.stem(job).with_suffix(".done").exists():
                continue                      # finishing or finished: never killed here
            if beat and now - beat["started"] > self.res["instance_time_limit_s"]:
                self.kill(job, f"instance {beat['instance']} over "
                               f"{self.res['instance_time_limit_s']} s")
                lib.append_jsonl(self.stem(job).with_suffix(".jsonl"), {
                    "instance_id": beat["instance"], "failed": 1,
                    "fail_reason": f"time limit of {self.res['instance_time_limit_s']} s"})
                self.queue.insert(0, job)        # resumes after the failed instance
            elif lib.stuck_at_startup(w.get("beat_seen", False), w["born"], now,
                                      self.res["job_start_limit_s"]):
                self.kill(job, f"no first instance after {self.res['job_start_limit_s']} s")
                self.retry(job, "stuck at start-up")
        # Finished processes.
        for job, w in list(self.running.items()):
            code = w["proc"].poll()
            if code is None:
                continue
            w["log"].close()
            del self.running[job]
            if code == 0 and self.stem(job).with_suffix(".done").exists():
                self.finished += 1
                self.record_peak(job, w["peak_gb"])
                log(f"done {'/'.join(map(str, job))} (peak {w['peak_gb']:.2f} GB)")
            elif code == 0:
                pass                              # stopped by the stop file: resumable
            elif code == EXIT_FATAL:
                self.failed[job] = "fatal (see log)"
                log(f"FATAL {'/'.join(map(str, job))}: see its log")
            else:
                self.retry(job, f"exit code {code}")
        # Admission.
        stop = self.stopping or lib.STOP.exists()
        self.queue = [j for j in self.queue if not self.stem(j).with_suffix(".done").exists()]
        cands = [(j, lib.expected_peak_gb(self.peaks, j[1], j[3], j[0],
                                          self.res["default_peak_gb"]), j in self.alone)
                 for j in self.queue if j not in self.running]
        to_start, self.reason = lib.plan_admissions(
            cands, snap["ram_available_gb"], len(self.running), self.max_workers,
            self.res["ram_reserve_gb"], self.res["pause_admission_below_gb"],
            snap["ac_power"], snap["disk_free_gb"], self.res["disk_pause_gb"], stop)
        peaks = {j: p for j, p, _a in cands}
        for job in to_start:
            self.queue.remove(job)
            self.start(job)
            snap["ram_available_gb"] -= peaks[job]
        if now - self.last_bench > 600:
            self.last_bench = now
            lib.append_jsonl(lib.STATE / "bench.jsonl", {"time": now, "bench_ms": lib.microbenchmark(),
                                                          "cpu_mhz": snap["cpu_mhz"],
                                                          "workers": len(self.running)})
        self.write_state(snap)

    def append_failed_instance(self, job, why):
        beat = lib.read_json(self.stem(job).with_suffix(".heartbeat"))
        w = self.running.get(job)
        if beat and (not w or beat.get("started", 0) >= w["born"] - 1):
            lib.append_jsonl(self.stem(job).with_suffix(".jsonl"),
                             {"instance_id": beat["instance"], "failed": 1, "fail_reason": why})

    def write_state(self, snap):
        lib.atomic_write_json(lib.STATE / "orchestrator.json", {
            "pid": os.getpid(), "mode": self.args.mode, "root": str(self.root),
            "started": self.started, "updated": time.time(), "max_workers": self.max_workers,
            "cohort_sha256": lib.config_hash(), "stopping": self.stopping or lib.STOP.exists(),
            "queue": len(self.queue), "finished_this_run": self.finished,
            "failed": {"/".join(map(str, k)): v for k, v in self.failed.items()},
            "admission": self.reason, "host": snap,
            "workers": [{"job": list(j), "pid": w["proc"].pid, "born": w["born"],
                         "rss_gb": w.get("rss_gb"), "peak_gb": w["peak_gb"],
                         "instance": w.get("instance"),
                         "instance_started": w.get("instance_started")}
                        for j, w in self.running.items()]})

    def run(self) -> int:
        def on_sigint(_sig, _frm):
            if not self.stopping:
                self.stopping = True
                # Workers run in their own process group (they do not see Ctrl+C); the
                # stop file tells each of them to leave after its current instance.
                lib.atomic_write_text(lib.STOP, f"stop requested by Ctrl+C at {time.ctime()}\n")
                log("Ctrl+C: no new job starts; running jobs leave after their current "
                    f"instance. Ctrl+C again kills them. Delete {lib.STOP} to run again.")
            else:
                for job in list(self.running):
                    self.kill(job, "second Ctrl+C")
                raise SystemExit(130)
        signal.signal(signal.SIGINT, on_sigint)
        log(f"{len(self.queue)} jobs queued; up to {self.max_workers} workers")
        with lib.SleepBlocker():
            while self.queue or self.running:
                self.step()
                if (self.stopping or lib.STOP.exists()) and not self.running:
                    break
                time.sleep(2)
        self.write_state(lib.host_snapshot())
        log(f"left: {len(self.queue)} queued, {len(self.failed)} failed, "
            f"{self.finished} finished this run")
        return 1 if self.failed else 0


def ordered(jobs: list[tuple]) -> list[tuple]:
    """Seeds in order; within a seed, a fixed shuffle mixes heavy and light jobs."""
    out = []
    for seed in sorted({j[2] for j in jobs}):
        block = [j for j in jobs if j[2] == seed]
        random.Random(seed).shuffle(block)
        out += block
    return out


def cmd_launch(args, pilot: bool = False) -> int:
    cfg = lib.config()
    if pilot:
        root = lib.LIVE / "pilot"
        jobs = [(d, m, lib.seeds_for(cfg, d)[0], e) for d in (args.datasets or cfg["datasets"])
                for m in (args.models or cfg["models"])
                for e in (args.explainers or cfg["explainers"])]
        extra = ["--per-stratum", "1", "--stability-per-stratum", "1"]
        args.mode = "pilot"
    else:
        root = lib.RESULTS
        jobs = lib.all_quality_jobs(cfg, args.datasets, args.models, args.explainers, args.seeds)
        extra = []
        args.mode = "quality"
    jobs = [j for j in ordered(jobs)
            if not (root / "quality" / j[0] / j[1] / f"seed_{j[2]}" / j[3]).with_suffix(".done").exists()]
    if not lib.MANIFEST.exists():
        log("models are not frozen: run `prepare` first")
        return 1
    if lib.STOP.exists():
        log(f"stop file present ({lib.STOP}); delete it to start")
        return 1
    return Governor(args, jobs, root, extra).run()


def cmd_launch_timing(args, pilot: bool = False) -> int:
    cfg = lib.config()
    if count_quality_workers():
        log("quality workers are running: the timing pass needs the host to itself")
        return 1
    root = lib.LIVE / "pilot" if pilot else lib.RESULTS
    cells = [(d, m, s) for d in (args.datasets or cfg["datasets"])
             for m in (args.models or cfg["models"])
             for s in ([lib.seeds_for(cfg, d)[0]] if pilot else (args.seeds or lib.seeds_for(cfg, d)))]
    extra = (["--per-stratum", "1", "--timing-per-stratum", "1"] if pilot else [])
    if not args.require_idle:
        extra.append("--no-require-idle")
    res = cfg["resources"]
    with lib.SleepBlocker():
        for d, m, s in cells:
            if (root / "timing" / d / m / f"seed_{s}" / "timing").with_suffix(".done").exists():
                continue
            if lib.STOP.exists():
                log("stop file: timing pass left")
                return 0
            for attempt in range(res["max_retries"] + 1):
                cmd = [sys.executable, str(Path(__file__).resolve()), "timing", "--dataset", d,
                       "--model", m, "--seed", str(s), "--root", str(root), *extra]
                log(f"timing {d}/{m}/seed {s} (attempt {attempt + 1})")
                lib.atomic_write_json(lib.STATE / "timing.json", {
                    "pid": os.getpid(), "updated": time.time(), "cell": [d, m, s],
                    "pilot": pilot, "attempt": attempt + 1})
                with open(lib.LOGS / f"timing_{d}_{m}_{s}.log", "a", encoding="utf-8") as logf:
                    code = subprocess.call(cmd, stdout=logf, stderr=subprocess.STDOUT, cwd=lib.ROOT)
                if code in (0, EXIT_FATAL):
                    break
    lib.atomic_write_json(lib.STATE / "timing.json", {"pid": None, "updated": time.time(),
                                                      "finished": True})
    return 0


# ==========================================================================
# status
# ==========================================================================
def cmd_status(args) -> int:
    cfg = lib.config()
    root = lib.LIVE / "pilot" if args.pilot else lib.RESULTS
    jobs = lib.all_quality_jobs(cfg) if not args.pilot else \
        [(d, m, lib.seeds_for(cfg, d)[0], e) for d in cfg["datasets"] for m in cfg["models"]
         for e in cfg["explainers"]]
    n_done = n_rows = n_fail = 0
    for d, m, s, e in jobs:
        stem = root / "quality" / d / m / f"seed_{s}" / e
        n_done += stem.with_suffix(".done").exists()
        for r in lib.read_jsonl(stem.with_suffix(".jsonl")):
            n_rows += 1
            n_fail += r.get("failed", 0)
    print(f"{'pilot' if args.pilot else 'quality'}: {n_done}/{len(jobs)} jobs done, "
          f"{n_rows} instance rows, {n_fail} failed")
    return 0


# ==========================================================================
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("preflight")
    p = sub.add_parser("prepare")
    p.add_argument("--datasets", nargs="*")
    p.add_argument("--models", nargs="*")
    p.add_argument("--force", action="store_true", help="retrain frozen models (never mid-cohort)")
    p.add_argument("--keep-data", action="store_true",
                   help="use the prepared dataset files as they are (safe while a run reads them)")
    for name in ("job", "timing"):
        p = sub.add_parser(name)
        p.add_argument("--dataset", required=True)
        p.add_argument("--model", required=True)
        p.add_argument("--seed", required=True, type=int)
        if name == "job":
            p.add_argument("--explainer", required=True)
            p.add_argument("--stability-per-stratum", type=int)
        else:
            p.add_argument("--explainers", nargs="*")
            p.add_argument("--timing-per-stratum", type=int)
            p.add_argument("--no-require-idle", dest="require_idle", action="store_false")
        p.add_argument("--per-stratum", type=int)
        p.add_argument("--root")
        p.add_argument("--ignore-stop", action="store_true")
    for name in ("launch", "pilot", "launch-timing", "pilot-timing"):
        p = sub.add_parser(name)
        p.add_argument("--datasets", nargs="*")
        p.add_argument("--models", nargs="*")
        p.add_argument("--explainers", nargs="*")
        p.add_argument("--seeds", nargs="*", type=int)
        p.add_argument("--workers", type=int)
        p.add_argument("--no-require-idle", dest="require_idle", action="store_false")
    p = sub.add_parser("status")
    p.add_argument("--pilot", action="store_true")
    args = ap.parse_args(argv)
    lib.STATE.mkdir(parents=True, exist_ok=True)
    return {
        "preflight": cmd_preflight, "prepare": cmd_prepare, "job": cmd_job,
        "timing": cmd_timing, "status": cmd_status,
        "launch": lambda a: cmd_launch(a), "pilot": lambda a: cmd_launch(a, pilot=True),
        "launch-timing": lambda a: cmd_launch_timing(a),
        "pilot-timing": lambda a: cmd_launch_timing(a, pilot=True),
    }[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
