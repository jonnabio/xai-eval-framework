#!/usr/bin/env python3
"""Paper G S1: supplementary LIME contributions (plan section 12.3).

    python scripts/paper_g_s1_lime.py --pilot --authorized "<who, date>"
    python scripts/paper_g_s1_lime.py --full --authorized "<who, date>" [--jobs 6]

Supplementary and exploratory. For each block it rebuilds the frozen model and LIME exactly
(reconstruction gate, 12.3.2), converts LIME's encoded-column coefficients into contributions to its
fitted linear surrogate relative to a reference (S1-B: the metrics' masking baseline; S1-M: LIME's
training mean), groups and orients them as the frozen run did, and recomputes M1-M7 with the frozen
metric code. Uses paper_g_lib read-only; never writes to the frozen outputs. The full run is
block-parallel, resumable and atomic (one shard per dataset x model x seed under supplementary/s1/).
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")          # one scientific thread per worker (as the frozen runner)

import argparse  # noqa: E402
import csv  # noqa: E402
import gzip  # noqa: E402
import hashlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import platform  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait  # noqa: E402
from datetime import datetime, timezone  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_g_lib as lib  # noqa: E402
import paper_g_semantics as sem  # noqa: E402

RAW = lib.OUT / "raw" / "full"
PILOT_OUT = lib.OUT / "supplementary" / "s1_pilot"
PILOT_REPORT = lib.ROOT / "docs" / "reports" / "paper_g" / "S1_PILOT_REPORT.md"
PILOT_DATASETS = ("phoneme", "german_credit")      # 12.3.6, chosen by rule
PILOT_SEED = 42
PILOT_INSTANCES = 20
FULL_OUT = lib.OUT / "supplementary" / "s1"
FULL_INSTANCES = 200
AUDIT_N = 5                     # per block: inputs kept so the conversion can be re-done independently
MIN_FREE_GIB = 1.5              # the frozen runner's admission threshold
TOL_FX, TOL_ATTR, TOL_METRIC, TOL_REF = 1e-12, 1e-8, 1e-9, 1e-12
REPRESENTATIONS = {"S1-B": "lime_s1_baseline", "S1-M": "lime_s1_mean"}
SIGNED = ("m1_deletion", "m2_insertion", "m3_gap", "m4_corr", "m5_infidelity", "m6_sufficiency")
B2 = ("m1_deletion_b2", "m2_insertion_b2", "m3_gap_b2", "m6_sufficiency_b2")


class GateFailure(RuntimeError):
    """A reconstruction or acceptance check of 12.3.2 / 12.3.6 failed."""


# --- conversion (pure, tested) ---------------------------------------------------------------------

def contributions(w: np.ndarray, x: np.ndarray, reference: np.ndarray, scale: np.ndarray) -> np.ndarray:
    """c_j = w_j (x_j - r_j) / s_j: the additive decomposition of LIME's linear surrogate from r to x."""
    w, x, r, s = (np.asarray(v, float) for v in (w, x, reference, scale))
    if not (w.shape == x.shape == r.shape == s.shape):
        raise ValueError("w, x, reference and scale must have the same encoded-column shape")
    if not np.all(np.isfinite(s)) or np.any(s <= 0):
        raise ValueError("LIME scales must be finite and positive")
    return w * (x - r) / s


def s1_vectors(w: np.ndarray, x: np.ndarray, pred_class: int, data: dict, scaler) -> dict[str, np.ndarray]:
    """S1-B and S1-M group vectors, oriented to the predicted class as the frozen run orients."""
    out = {}
    for rid, ref in (("S1-B", data["base"]), ("S1-M", scaler.mean_)):
        out[rid] = lib.orient(lib.group_attr(contributions(w, x, ref, scaler.scale_), data["groups"]), pred_class)
    return out


def has_categorical_groups(data: dict) -> bool:
    return any(not data["is_numeric"][g[0]] for g in data["groups"])


def contract_check(data: dict) -> list[dict]:
    """RCA-005: every S1 representation x metric pair must be admitted (S1-M on mixed data as declared)."""
    multi = any(len(g) > 1 for g in data["groups"])
    rows = []
    for rid, name in REPRESENTATIONS.items():
        for m in (*SIGNED, "m7_roar"):
            v = sem.check(name, m, multi_column_groups=multi, declared=sem.S1_DECLARATIONS)
            rows.append({"representation": rid, "metric": m, "status": v.status, "note": v.note})
    return rows


# --- frozen pipeline pieces -------------------------------------------------------------------------

def instance_seed(seed: int, pos: int) -> int:
    return (seed * 100003 + int(pos)) % (2**31)


def frozen_metrics(a: np.ndarray, pos: int, x: np.ndarray, c: int, data: dict, seed: int, cfg: dict) -> dict:
    """M1-M6 (+ _b2, m4_degenerate, f_x) exactly as lib.explain_and_score computes them."""
    rng_b2 = np.random.default_rng([seed, int(pos), 2])
    base2 = data["X_train"][rng_b2.integers(0, len(data["X_train"]))]
    rng = np.random.default_rng([seed, int(pos), 5])
    return lib.instance_metrics(a, x, data["model"], c, data["base"], base2, data["groups"], cfg, rng)


def stored_rows(dataset: str, model: str, seed: int, raw: Path = RAW) -> dict[int, dict]:
    path = raw / dataset / model / f"seed_{seed}.jsonl.gz"
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return {r["instance"]: r for r in map(json.loads, fh) if r["explainer"] == "lime"}


def run_block(dataset: str, model: str, seed: int, cfg: dict, n: int, stored: dict,
              data: dict | None = None, audit_n: int = 0) -> dict:
    """Reconstruction gate, conversion and metric recomputation for one block (first n instances)."""
    data = data or lib.prepare(dataset, model, seed, cfg)
    lime = lib.make_explainer("lime", data["model"], data, seed, cfg)
    scaler = lime.lime.scaler
    num = data["is_numeric"]
    ref_gap = float(np.max(np.abs(data["base"][num] - scaler.mean_[num]))) if num.any() else 0.0
    if ref_gap > TOL_REF:
        raise GateFailure(f"{dataset}/{model}: numeric baseline differs from LIME mean by {ref_gap:.2e}")
    contract = contract_check(data)
    instances = [int(p) for p in data["instances"][:n]]
    if any(p not in stored for p in instances):
        raise GateFailure(f"{dataset}/{model}: reconstructed instance ids not in the stored rows")
    recon, rows, vecs, audit = [], [], {rid: [] for rid in REPRESENTATIONS}, []
    for k_inst, pos in enumerate(instances):
        rec, x, c = stored[pos], data["X_test"][pos], int(data["pred"][pos])
        s = instance_seed(seed, pos)
        w = lime.explain(x, s)
        w2 = lime.explain(x, s)
        a_frozen = lib.orient(lib.group_attr(w, data["groups"]), c)     # what the run scored (unrounded)
        grouped = np.round(a_frozen, 8)
        attr = np.array(rec["attr"], float)
        frozen = frozen_metrics(a_frozen, pos, x, c, data, seed, cfg)
        fx = float(frozen["f_x"])
        metric_gap = max(abs(float(frozen[k]) - float(rec[k])) for k in (*SIGNED, *B2))
        r = {"dataset": dataset, "model": model, "seed": seed, "instance": pos,
             "pred_match": int(c == rec["pred_class"]), "fx_diff": abs(fx - float(rec["f_x"])),
             "attr_max_diff": float(np.max(np.abs(grouped - attr))), "deterministic": int(np.array_equal(w, w2)),
             "metric_max_diff": metric_gap}
        r["passed"] = int(r["pred_match"] and r["fx_diff"] <= TOL_FX and r["attr_max_diff"] <= TOL_ATTR
                          and r["deterministic"] and r["metric_max_diff"] <= TOL_METRIC)
        recon.append(r)
        if not r["passed"]:
            raise GateFailure(f"{dataset}/{model}/seed_{seed} instance {pos}: reconstruction gate failed: {r}")
        if k_inst < audit_n:
            audit.append({"instance": pos, "pred_class": c, "w": [repr(float(v)) for v in w],
                          "x": [repr(float(v)) for v in x]})
        for rid, a in s1_vectors(w, x, c, data, scaler).items():
            vecs[rid].append(a)
            met = frozen_metrics(a, pos, x, c, data, seed, cfg)
            rows.append({"dataset": dataset, "model": model, "seed": seed, "instance": pos, "pred_class": c,
                         "representation": rid, **{k: float(met[k]) for k in (*SIGNED, *B2, "f_x")},
                         "m4_degenerate": int(bool(met["m4_degenerate"])), "failed": 0,
                         "group_vector": json.dumps([round(float(v), 10) for v in a])})
    checks = mode_zero_checks(data, instances, vecs)
    m7 = []
    for rid, vs in vecs.items():
        rank = lib.order_of(np.abs(np.array(vs)).mean(axis=0))
        m7.append({"dataset": dataset, "model": model, "seed": seed, "representation": rid,
                   "instances": len(vs), **lib.roar_score(rank, data, model, seed, cfg, data["auc"]),
                   "global_rank": json.dumps([int(i) for i in rank])})
    out = {"reconstruction": recon, "rows": rows, "m7": m7, "contract": contract,
           "checks": [{"dataset": dataset, "model": model, "numeric_baseline_minus_lime_mean": ref_gap,
                       "categorical_groups": int(has_categorical_groups(data)), **checks}]}
    if audit_n:
        out["audit"] = {"instances": audit, "lime_mean": [repr(float(v)) for v in scaler.mean_],
                        "lime_scale": [repr(float(v)) for v in scaler.scale_],
                        "baseline": [repr(float(v)) for v in data["base"]],
                        "groups": [[int(j) for j in g] for g in data["groups"]],
                        "is_numeric": [bool(v) for v in data["is_numeric"]]}
    return out


def mode_zero_checks(data: dict, instances: list[int], vecs: dict) -> dict:
    """Every categorical group whose instance value is the mode has S1-B contribution exactly 0."""
    at_mode = nonzero = 0
    for k, pos in enumerate(instances):
        x = data["X_test"][pos]
        for gi, g in enumerate(data["groups"]):
            if not data["is_numeric"][g[0]] and np.array_equal(x[g], data["base"][g]):
                at_mode += 1
                nonzero += int(vecs["S1-B"][k][gi] != 0.0)
    return {"categorical_values_at_mode": at_mode, "s1b_nonzero_at_mode": nonzero}


# --- system level (full run, later): LIME's rows replaced, all other rows frozen ------------------

def substitute_lime(full: pd.DataFrame, s1_rows: list[dict], representation: str) -> pd.DataFrame:
    """The frozen instance rows with LIME's metric values replaced by one S1 representation (12.3.4)."""
    s1 = pd.DataFrame([r for r in s1_rows if r["representation"] == representation])
    key = ["dataset", "model", "seed", "instance"]
    cols = [c for c in (*SIGNED, *B2, "m4_degenerate") if c in full.columns]
    lime = full[full["explainer"] == "lime"].drop(columns=cols).merge(s1[key + cols], on=key, how="left",
                                                                         validate="one_to_one")
    if lime[cols].isna().any().any():
        raise GateFailure("S1 rows do not cover every frozen LIME row")
    lime["m4_degenerate"] = lime["m4_degenerate"].astype(bool)
    out = pd.concat([full[full["explainer"] != "lime"], lime[full.columns]], ignore_index=True)
    return out.sort_values(["dataset", "model", "seed", "explainer", "instance"]).reset_index(drop=True)


# --- outputs -------------------------------------------------------------------------------------------

def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (repr(v) if isinstance(v, float) else v) for k, v in r.items()})


def write_report(path: Path, res: dict, prov: dict) -> None:
    rec, rows, m7 = res["reconstruction"], res["rows"], res["m7"]
    L = ["# Paper G — S1 pilot report", "",
         "Generated by `scripts/paper_g_s1_lime.py --pilot`; do not edit. Supplementary and exploratory "
         "(plan section 12.3.6). **Implementation and construct validation only: no agreement statistic "
         "is computed and none may be read from these rows.**", "",
         f"- code commit: {prov['code_commit']}; authorized: {prov['authorized']}",
         f"- scope: {', '.join(PILOT_DATASETS)}; models {', '.join(lib.MODELS)}; seed {PILOT_SEED}; "
         f"first {PILOT_INSTANCES} frozen instances",
         f"- wall time {prov['seconds']:.0f} s", "",
         "**Table P1. Reconstruction gate (12.3.2).**", "",
         "| check | value | tolerance |", "|---|---|---|",
         f"| instances passing every check | {sum(r['passed'] for r in rec)} of {len(rec)} | all |",
         f"| predicted class equal | {sum(r['pred_match'] for r in rec)} of {len(rec)} | all |",
         f"| max \\|f_x − stored\\| | {max(r['fx_diff'] for r in rec):.2e} | {TOL_FX} |",
         f"| max \\|regrouped LIME − stored attr\\| | {max(r['attr_max_diff'] for r in rec):.2e} | {TOL_ATTR} |",
         f"| repeated explanation identical | {sum(r['deterministic'] for r in rec)} of {len(rec)} | all |",
         f"| max \\|M1–M6, _b2 recomputed on the reconstructed unrounded vector − stored\\| | {max(r['metric_max_diff'] for r in rec):.2e} | {TOL_METRIC} |",
         "", "**Table P2. Construct checks per block.**", "",
         "| dataset | model | categorical groups | max \\|numeric baseline − LIME mean\\| | categorical values at the mode | S1-B non-zero at the mode |",
         "|---|---|---|---|---|---|"]
    for c in res["checks"]:
        L.append(f"| {c['dataset']} | {c['model']} | {c['categorical_groups']} | {c['numeric_baseline_minus_lime_mean']:.1e} | "
                 f"{c['categorical_values_at_mode']} | {c['s1b_nonzero_at_mode']} |")
    statuses = {}
    for r in res["contract"]:
        statuses[(r["representation"], r["status"])] = statuses.get((r["representation"], r["status"]), 0) + 1
    L += ["", "**Table P3. Semantic contract (RCA-005) for every representation × metric × block.**", "",
          "| representation | status | pairs |", "|---|---|---|"]
    L += [f"| {k[0]} | {k[1]} | {v} |" for k, v in sorted(statuses.items())]
    L += ["", "**Table P4. Completeness.**", "", "| item | value | expected |", "|---|---|---|",
          f"| instance rows | {len(rows)} | 320 |",
          f"| failed rows | {sum(r['failed'] for r in rows)} | 0 |",
          f"| m4_degenerate rows (recorded, allowed) | {sum(r['m4_degenerate'] for r in rows)} | — |",
          f"| non-finite metric values | {prov['nonfinite']} | 0 |",
          f"| M7 rows | {len(m7)} | 16 |", "",
          f"Acceptance (12.3.6): **{'PASS' if prov['accepted'] else 'FAIL'}**.", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L), encoding="utf-8")


def pilot(authorized: str, out: Path = PILOT_OUT, report: Path = PILOT_REPORT) -> int:
    cfg = lib.config()
    t0 = time.perf_counter()
    res = {"reconstruction": [], "rows": [], "m7": [], "contract": [], "checks": []}
    try:
        for d in PILOT_DATASETS:
            for m in lib.MODELS:
                b = run_block(d, m, PILOT_SEED, cfg, PILOT_INSTANCES, stored_rows(d, m, PILOT_SEED))
                for k in res:
                    res[k] += b[k]
                print(f"{d}/{m}/seed_{PILOT_SEED}: gate passed for {len(b['reconstruction'])} instances", flush=True)
    except (GateFailure, sem.IncompatibleSemantics) as exc:
        for k, v in res.items():
            if v:
                write_csv(out / f"s1_pilot_{k}.csv", v)
        print(f"STOP: {exc}", file=sys.stderr)
        return 3
    nonfinite = sum(1 for r in res["rows"] for k in (*SIGNED, *B2) if not math.isfinite(r[k]))
    accepted = (len(res["rows"]) == 320 and len(res["m7"]) == 16 and nonfinite == 0
                and all(r["passed"] for r in res["reconstruction"])
                and all(c["s1b_nonzero_at_mode"] == 0 for c in res["checks"]))
    for k, v in res.items():
        write_csv(out / f"s1_pilot_{k}.csv", v)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=lib.ROOT, capture_output=True, text=True).stdout.strip()
    prov = {"authorized": authorized, "code_commit": commit, "python": platform.python_version(),
            "numpy": np.__version__, "seconds": time.perf_counter() - t0, "nonfinite": nonfinite,
            "accepted": accepted, "files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                            for p in sorted(out.glob("s1_pilot_*.csv"))}}
    (out / "s1_pilot_provenance.json").write_text(json.dumps(prov, indent=1), encoding="utf-8")
    write_report(report, res, prov)
    print(json.dumps({k: v for k, v in prov.items() if k != "files"}, indent=1))
    return 0 if accepted else 4


# --- full run: block-parallel, resumable, atomic (plan 12.3; Task 19) ---------------------------------

def det_gzip_json(obj) -> bytes:
    """Deterministic gzip of canonical JSON (sorted keys; no time or name in the header)."""
    raw = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
        gz.write(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    return raw.getvalue()


def block_paths(out: Path, dataset: str, model: str, seed: int) -> dict[str, Path]:
    stem = out / "shards" / dataset / model / f"seed_{seed}"
    return {"shard": stem.with_suffix(".json.gz"), "done": stem.with_suffix(".done.json"),
            "failed": stem.with_suffix(".failed.json"), "log": out / "block_logs" / dataset / model / f"seed_{seed}.txt"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def block_state(out: Path, dataset: str, model: str, seed: int) -> str:
    """'done' (shard verified by its recorded hash), 'todo'; a mismatch is an error, never overwritten."""
    p = block_paths(out, dataset, model, seed)
    if not p["done"].exists():
        return "todo"
    rec = json.loads(p["done"].read_text(encoding="utf-8"))
    if not p["shard"].exists() or sha256(p["shard"]) != rec["sha256"]:
        raise GateFailure(f"{dataset}/{model}/seed_{seed}: published shard does not match its .done hash")
    return "done"


def _peak_rss_mib() -> float:
    import resource
    return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1)


def compute_block(dataset: str, model: str, seed: int, out: str, n: int = FULL_INSTANCES,
                  commit: str = "") -> dict:
    """One block in a worker: gate, conversion, metrics, M7; atomic publication; never raises."""
    out = Path(out)
    paths = block_paths(out, dataset, model, seed)
    for k in ("shard", "log"):
        paths[k].parent.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    log = [f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} start {dataset}/{model}/seed_{seed} "
           f"on {platform.node()} commit {commit}"]
    try:
        cfg = lib.config()
        res = run_block(dataset, model, seed, cfg, n, stored_rows(dataset, model, seed), audit_n=AUDIT_N)
        nonfinite = sum(1 for r in res["rows"] for k in (*SIGNED, *B2) if not math.isfinite(r[k]))
        nonfinite += sum(1 for r in res["m7"] if not math.isfinite(r["m7_roar"]))
        if len(res["rows"]) != 2 * n or len(res["m7"]) != 2 or nonfinite:
            raise GateFailure(f"incomplete or non-finite block: rows {len(res['rows'])}, m7 {len(res['m7'])}, "
                              f"non-finite {nonfinite}")
        if res["checks"][0]["s1b_nonzero_at_mode"]:
            raise GateFailure("S1-B non-zero at a categorical mode")
        res["meta"] = {"dataset": dataset, "model": model, "seed": seed, "instances": n, "host": platform.node(),
                       "commit": commit, "python": platform.python_version(), "numpy": np.__version__}
        data = det_gzip_json(res)
        tmp = paths["shard"].with_name(paths["shard"].name + ".part")
        tmp.write_bytes(data)
        os.replace(tmp, paths["shard"])                                    # atomic publication
        done = {"dataset": dataset, "model": model, "seed": seed, "sha256": hashlib.sha256(data).hexdigest(),
                "rows": len(res["rows"]), "m7_rows": len(res["m7"]), "reconstruction_rows": len(res["reconstruction"]),
                "seconds": round(time.perf_counter() - t0, 1), "peak_rss_mib": _peak_rss_mib(),
                "finished": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "host": platform.node(),
                "commit": commit}
        rec = res["reconstruction"]
        log.append(f"gate passed {sum(r['passed'] for r in rec)}/{len(rec)}; max fx {max(r['fx_diff'] for r in rec):.1e}; "
                   f"max attr {max(r['attr_max_diff'] for r in rec):.1e}; max metric {max(r['metric_max_diff'] for r in rec):.1e}")
        log.append(f"done in {done['seconds']} s, peak {done['peak_rss_mib']} MiB, sha256 {done['sha256']}")
        paths["log"].write_text("\n".join(log) + "\n", encoding="utf-8")
        tmpd = paths["done"].with_name(paths["done"].name + ".part")
        tmpd.write_text(json.dumps(done, indent=1, sort_keys=True), encoding="utf-8")
        os.replace(tmpd, paths["done"])
        paths["failed"].unlink(missing_ok=True)
        return {"status": "done", **done}
    except Exception as exc:                                   # recorded, reported, never silently skipped
        err = f"{type(exc).__name__}: {exc}"[:2000]
        log.append(f"FAILED: {err}")
        paths["log"].write_text("\n".join(log) + "\n", encoding="utf-8")
        paths["failed"].write_text(json.dumps({"dataset": dataset, "model": model, "seed": seed, "error": err,
                                               "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
                                              indent=1), encoding="utf-8")
        return {"status": "failed", "dataset": dataset, "model": model, "seed": seed, "error": err}


def free_memory_gib() -> float | None:
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemAvailable:"):
                return int(line.split()[1]) / 1024**2
    except OSError:
        return None
    return None


def package_temp_c() -> float | None:
    for z in Path("/sys/class/thermal").glob("thermal_zone*"):
        try:
            if (z / "type").read_text().strip() == "x86_pkg_temp":
                return int((z / "temp").read_text()) / 1000
        except (OSError, ValueError):
            continue
    return None


def full_blocks(cfg: dict) -> list[tuple[str, str, int]]:
    return [(d["key"], m, s) for s in cfg["seeds"] for d in cfg["dataset"] for m in lib.MODELS]


def run_full(authorized: str, out: Path = FULL_OUT, jobs: int = 6, blocks=None, block_fn=compute_block,
             n: int = FULL_INSTANCES, min_free: float = MIN_FREE_GIB) -> int:
    """All blocks with at most `jobs` workers; stops admitting on the first failure; resumable."""
    cfg = lib.config()
    blocks = list(blocks if blocks is not None else full_blocks(cfg))
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=lib.ROOT, capture_output=True, text=True).stdout.strip()
    out.mkdir(parents=True, exist_ok=True)
    main_log = out / "run_log.txt"

    def note(msg: str) -> None:
        line = f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} {msg}"
        with open(main_log, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        print(line, flush=True)

    pending = [b for b in blocks if block_state(out, *b) == "todo"]
    note(f"start: {len(blocks) - len(pending)} of {len(blocks)} blocks done; {len(pending)} to run with {jobs} jobs; "
         f"commit {commit}; authorized {authorized!r}")
    failed, running = [], {}
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        while (pending and not failed) or running:
            free = free_memory_gib()
            while pending and not failed and len(running) < jobs and (free is None or free >= min_free or not running):
                b = pending.pop(0)
                running[pool.submit(block_fn, *b, str(out), n, commit)] = b
            finished, _ = wait(list(running), timeout=30, return_when=FIRST_COMPLETED)
            for fut in finished:
                b = running.pop(fut)
                r = fut.result()
                ndone = sum(block_state(out, *x) == "done" for x in blocks)
                if r["status"] == "done":
                    note(f"done {'/'.join(map(str, b))} ({ndone}/{len(blocks)}, {r['seconds']} s, "
                         f"{r['peak_rss_mib']} MiB; free {free_memory_gib() or 0:.1f} GiB; cpu {package_temp_c()} C)")
                else:
                    failed.append(r)
                    note(f"FAILED {'/'.join(map(str, b))}: {r['error'][:300]}")
            (out / "heartbeat.json").write_text(json.dumps({"at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                                          "running": ["/".join(map(str, x)) for x in running.values()],
                                                          "pending": len(pending), "failed": len(failed)}), encoding="utf-8")
    if failed:
        note(f"STOP: {len(failed)} block(s) failed; no manifest written")
        return 3
    rows = []
    for b in sorted(blocks):
        p = block_paths(out, *b)
        d = json.loads(p["done"].read_text(encoding="utf-8"))
        rows.append({"path": str(p["shard"].relative_to(out)), "sha256": d["sha256"], "rows": d["rows"],
                     "m7_rows": d["m7_rows"], "seconds": d["seconds"], "peak_rss_mib": d["peak_rss_mib"],
                     "host": d["host"], "commit": d["commit"]})
    write_csv(out / "MANIFEST.csv", rows)
    note(f"finished: {len(rows)} blocks; manifest written")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--authorized", default="")
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args(argv)
    if a.full:
        if not a.authorized.strip():
            print("refused: the full S1 run needs an --authorized statement (plan 12.3; Task 19)", file=sys.stderr)
            return 2
        return run_full(a.authorized, jobs=max(1, min(a.jobs, 6)))
    if not a.pilot or not a.authorized.strip():
        print("refused: the S1 pilot runs only with --pilot and an --authorized statement (plan 12.3.6)", file=sys.stderr)
        return 2
    return pilot(a.authorized)


if __name__ == "__main__":
    sys.exit(main())
