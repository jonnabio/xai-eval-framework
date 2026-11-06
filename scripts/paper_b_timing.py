"""Paper B revision 1, WP2-T: single-host re-timing of EXP2 cells.

Re-times one EXP2 cell (model, explainer, seed, N) on the recorded host
(docs/reports/paper_b/ci_journal/revision_1/env/HOST.md). It reuses the EXP2
`ExperimentRunner.setup()` and `generate_instances()` unchanged, so the data,
the model, the explainer and the instance set are those of the original run.
Only the measurement differs:

* one process, BLAS/OpenMP threads = 1, model `n_jobs` = 1, process pinned
  to one logical CPU (EXP2 also enforced single-core affinity);
* one warm-up explanation discarded (it absorbs lazy initialisation:
  Anchors' discretiser, DiCE's set-up);
* each timed explanation repeated `--repeats` times;
* per explanation: wall time (perf_counter), process CPU time
  (process_time), number of black-box model calls and rows evaluated.

Model calls are counted by wrapping `predict_proba` and `predict` on the model
classes before the explainer is built, with a re-entrancy guard so that a
`predict` implemented through `predict_proba` counts once. TreeSHAP does not
call the model (it traverses the trees), so it records zero calls.

Quality metrics are NOT recomputed here (D-1, re-time only). The run writes
one JSON file; nothing is written under the EXP2 results tree.

Usage:
    .venv/Scripts/python.exe scripts/paper_b_timing.py \
        --config configs/experiments/exp2_scaled/rf_lime_s42_n50.yaml \
        --per-stratum 5 --repeats 3 --out experiments/exp_b_rev1/pilot
"""
from __future__ import annotations

import os

for _var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
             "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_var] = "1"

import argparse  # noqa: E402
import json  # noqa: E402
import platform  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import tempfile  # noqa: E402
import threading  # noqa: E402
import time  # noqa: E402
from datetime import datetime, timezone  # noqa: E402
from importlib import metadata  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

META_COLS = ["original_index", "target", "prediction", "quadrant"]
PACKAGES = ["numpy", "pandas", "scipy", "scikit-learn", "xgboost", "shap",
            "lime", "alibi", "dice-ml"]


# --------------------------------------------------------------------------
# Model-call counter
# --------------------------------------------------------------------------
class CallCounter:
    """Counts outermost calls to predict/predict_proba and the rows they see."""

    def __init__(self) -> None:
        self.calls = 0
        self.rows = 0
        self._local = threading.local()

    def reset(self) -> None:
        self.calls = 0
        self.rows = 0

    def wrap(self, fn):
        counter = self

        def wrapped(self_model, X, *args, **kwargs):
            depth = getattr(counter._local, "depth", 0)
            if depth == 0:
                counter.calls += 1
                try:
                    counter.rows += int(np.shape(X)[0])
                except Exception:  # pragma: no cover - exotic inputs
                    counter.rows += 1
            counter._local.depth = depth + 1
            try:
                return fn(self_model, X, *args, **kwargs)
            finally:
                counter._local.depth = depth

        wrapped.__wrapped__ = fn
        wrapped.__name__ = getattr(fn, "__name__", "wrapped")
        return wrapped


def model_classes():
    """Model classes used by EXP2 (imported lazily; missing ones are skipped)."""
    out = []
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.neural_network import MLPClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.svm import SVC
    out += [RandomForestClassifier, LogisticRegression, MLPClassifier, SVC, Pipeline]
    try:
        from xgboost import XGBClassifier
        out.append(XGBClassifier)
    except ImportError:  # pragma: no cover
        pass
    return out


def install_counter(counter: CallCounter, classes) -> list[str]:
    """Wrap predict/predict_proba as resolved through each class's MRO.

    Plain functions (possibly inherited, e.g. RandomForestClassifier.predict_proba
    from ForestClassifier) are wrapped and set on the concrete class. sklearn's
    `available_if` descriptors (SVC.predict_proba, Pipeline.*) carry the function
    in `.fn`, which is wrapped in place. Returns what was wrapped, for the record.
    """
    import inspect

    done = []
    for cls in classes:
        for name in ("predict_proba", "predict"):
            raw = None
            for klass in cls.__mro__:
                if name in klass.__dict__:
                    raw = klass.__dict__[name]
                    break
            if raw is None:
                continue
            if inspect.isfunction(raw):
                if getattr(raw, "__wrapped__", None) is None:
                    setattr(cls, name, counter.wrap(raw))
                    done.append(f"{cls.__name__}.{name}")
            elif inspect.isfunction(getattr(raw, "fn", None)):
                if getattr(raw.fn, "__wrapped__", None) is None:
                    raw.fn = counter.wrap(raw.fn)
                    done.append(f"{cls.__name__}.{name} (available_if)")
    return done


# --------------------------------------------------------------------------
# Host and environment record
# --------------------------------------------------------------------------
def host_record() -> dict:
    rec = {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python": platform.python_version(),
        "logical_cpus": os.cpu_count(),
        "thread_env": {v: os.environ.get(v) for v in
                       ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                        "NUMEXPR_NUM_THREADS")},
        "packages": {},
    }
    for p in PACKAGES:
        try:
            rec["packages"][p] = metadata.version(p)
        except metadata.PackageNotFoundError:
            rec["packages"][p] = None
    if sys.platform == "win32":
        try:
            out = subprocess.run(["powercfg", "/getactivescheme"], capture_output=True,
                                 text=True, timeout=10).stdout.strip()
            rec["power_scheme"] = out
        except Exception:  # pragma: no cover
            rec["power_scheme"] = None
    try:
        rec["git_commit"] = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                                           capture_output=True, text=True,
                                           timeout=10).stdout.strip()
    except Exception:  # pragma: no cover
        rec["git_commit"] = None
    return rec


def pin_to_one_cpu(cpu: int) -> str:
    try:
        import psutil
        psutil.Process().cpu_affinity([cpu])
        return f"pinned to logical CPU {cpu}"
    except Exception as exc:  # pragma: no cover - platform dependent
        return f"not pinned ({exc})"


def single_thread_model(model) -> list[str]:
    """Force single-threaded prediction where the model exposes a knob."""
    changed = []
    for est in getattr(model, "steps", [(None, model)]):
        est = est[1]
        for attr in ("n_jobs", "nthread"):
            if hasattr(est, attr):
                try:
                    est.set_params(**{attr: 1})
                except Exception:
                    setattr(est, attr, 1)
                changed.append(f"{type(est).__name__}.{attr}=1")
    return changed


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def select_instances(instances, per_stratum: int):
    """First `per_stratum` instances of each quadrant, in sampler order."""
    picked = []
    for q in ("TP", "TN", "FP", "FN"):
        sub = instances[instances["quadrant"] == q]
        picked.append(sub.head(per_stratum))
    import pandas as pd
    return pd.concat(picked)


def run(args) -> Path:
    counter = CallCounter()
    wrapped = install_counter(counter, model_classes())

    from src.experiment.config import load_config
    from src.experiment.runner import ExperimentRunner

    cfg = load_config(Path(args.config))
    scratch = Path(tempfile.mkdtemp(prefix="paper_b_timing_"))
    cfg.output_dir = scratch  # never write into the EXP2 results tree
    if args.kernel_width is not None:
        if cfg.explainer.method != "lime":
            raise SystemExit("--kernel-width applies to LIME configs only")
        cfg.explainer.params = dict(cfg.explainer.params or {})
        if args.kernel_width == "default":
            cfg.explainer.params.pop("kernel_width", None)
            cfg.explainer.params["kernel_width"] = None
        else:
            cfg.explainer.params["kernel_width"] = float(args.kernel_width)

    pin = pin_to_one_cpu(args.cpu)
    t_setup = time.perf_counter()
    runner = ExperimentRunner(cfg)
    runner.setup()
    setup_s = time.perf_counter() - t_setup
    knobs = single_thread_model(runner.model)

    instances = runner.generate_instances()
    chosen = select_instances(instances, args.per_stratum)
    explainer = runner.explainer
    model = runner.model

    records = []
    rows = list(chosen.iterrows())
    # Warm-up on the first instance: absorbs lazy initialisation.
    if rows:
        x0 = rows[0][1].drop(labels=META_COLS).values.astype(float)
        counter.reset()
        w0 = time.perf_counter()
        explainer.explain_instance(model, x0, return_full=True)
        warmup = {"wall_ms": (time.perf_counter() - w0) * 1e3,
                  "model_calls": counter.calls, "rows": counter.rows}
    else:
        warmup = None

    for _, row in rows:
        x = row.drop(labels=META_COLS).values.astype(float)
        reps = []
        for _rep in range(args.repeats):
            counter.reset()
            c0, w0 = time.process_time(), time.perf_counter()
            err = None
            try:
                explainer.explain_instance(model, x, return_full=True)
            except Exception as exc:  # recorded, not hidden
                err = f"{type(exc).__name__}: {exc}"
            reps.append({
                "wall_ms": (time.perf_counter() - w0) * 1e3,
                "cpu_ms": (time.process_time() - c0) * 1e3,
                "model_calls": counter.calls,
                "rows": counter.rows,
                "error": err,
            })
        records.append({
            "instance_id": int(row["original_index"]),
            "quadrant": row["quadrant"],
            "repeats": reps,
        })

    def med(key):
        vals = [r[key] for rec in records for r in rec["repeats"] if r["error"] is None]
        return float(np.median(vals)) if vals else None

    def total(key):
        return float(sum(r[key] for rec in records for r in rec["repeats"]
                         if r["error"] is None))

    n_ok = sum(r["error"] is None for rec in records for r in rec["repeats"])

    explainer_cfg = explainer.get_config() if hasattr(explainer, "get_config") else {}
    result = {
        "schema": "paper_b_rev1_timing/1",
        "cell": {
            "config": str(Path(args.config).as_posix()),
            "name": cfg.name,
            "model": cfg.model.type if hasattr(cfg.model, "type") else None,
            "explainer": cfg.explainer.method,
            "seed": cfg.random_seed,
            "samples_per_class": cfg.sampling.samples_per_class,
            "kernel_width_override": args.kernel_width,
        },
        "protocol": {
            "per_stratum": args.per_stratum,
            "repeats": args.repeats,
            "warmup_explanations": 1,
            "affinity": pin,
            "model_single_thread": knobs,
            "timer_wall": "time.perf_counter",
            "timer_cpu": "time.process_time",
            "timer_cpu_resolution_s": time.get_clock_info("process_time").resolution,
            "counted_methods": wrapped,
            "note": ("CPU time per explanation is quantised by the OS clock "
                     "(15.625 ms on Windows); use the cell totals for CPU time."),
        },
        "host": host_record(),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "setup_seconds": setup_s,
        "explainer_config": {k: (v if isinstance(v, (int, float, str, bool, type(None)))
                                 else str(v)) for k, v in explainer_cfg.items()},
        "warmup": warmup,
        "summary": {
            "instances": len(records),
            "median_wall_ms": med("wall_ms"),
            "median_cpu_ms": med("cpu_ms"),
            "median_model_calls": med("model_calls"),
            "median_rows": med("rows"),
            "timed_explanations": n_ok,
            "total_wall_ms": total("wall_ms"),
            "total_cpu_ms": total("cpu_ms"),
            "mean_cpu_ms_from_total": (total("cpu_ms") / n_ok) if n_ok else None,
            "errors": sum(r["error"] is not None for rec in records for r in rec["repeats"]),
        },
        "instances": records,
    }
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = "" if args.kernel_width is None else f"_kw{args.kernel_width}"
    out = out_dir / f"{cfg.name}{suffix}.json"
    out.write_text(json.dumps(result, indent=1), encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--config", required=True, help="EXP2 cell config (YAML)")
    ap.add_argument("--per-stratum", type=int, default=5,
                    help="instances timed per TP/TN/FP/FN stratum")
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--cpu", type=int, default=2, help="logical CPU to pin to")
    ap.add_argument("--kernel-width", default=None,
                    help="LIME only: a number, or 'default' for 0.75*sqrt(M)")
    ap.add_argument("--out", required=True, help="output directory")
    args = ap.parse_args(argv)
    out = run(args)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
