"""Paper B revision 1 (cohort B2): shared code of the runner, the sync and the dashboard.

Design: experiments/exp_b_rev1/cohort.toml. Plan:
docs/reports/paper_b/ci_journal/revision_1/RUNS_IMPLEMENTATION_PLAN.md.

`src/` is used, never changed: explainer wrappers (src/xai), metric classes
(src/metrics) and the stratified sampler (src/evaluation) are called with the EXP2
settings. The orchestration, the resource control and the I/O are defined here.

Heavy imports (numpy, sklearn, the explainers) are done inside functions, so the
dashboard and the sync can import this module with the standard library only.
"""
from __future__ import annotations

import contextlib
import csv
import hashlib
import json
import os
import subprocess
import sys
import time
import tomllib
from pathlib import Path
from typing import Any, Iterable, Iterator

ROOT = Path(__file__).resolve().parents[1]
COHORT_DIR = ROOT / "experiments" / "exp_b_rev1"
MAIN_CONFIG = COHORT_DIR / "cohort.toml"
# Auxiliary studies (sweep, controls, matched ensembles) run the same machinery on their own
# configuration file: PAPER_B_CONFIG=<file>. Each gets its own live folder (results, state,
# logs, stop file), so it can never mix with or disturb the main cohort.
_CFG_ENV = os.environ.get("PAPER_B_CONFIG", "").strip()
CONFIG_PATH = Path(_CFG_ENV).resolve() if _CFG_ENV else MAIN_CONFIG
VARIANT = "" if CONFIG_PATH == MAIN_CONFIG.resolve() or CONFIG_PATH == MAIN_CONFIG \
    else CONFIG_PATH.stem
MODELS_DIR = COHORT_DIR / "models"
MANIFEST = MODELS_DIR / "MANIFEST.csv"
DATA_DIR = ROOT / "data" / "paper_b_rev1"          # git-ignored (/data/*)
LIVE = ROOT / "outputs" / (f"paper_b_rev1_{VARIANT}_live" if VARIANT
                           else "paper_b_rev1_live")  # git-ignored (outputs/*)
RESULTS = LIVE / "results"                          # quality and timing rows
STATE = LIVE / "_state"                             # orchestrator, timing, sync, peaks
LOGS = LIVE / "_logs"
STOP = LIVE / "_STOP"
META_COLS = ["original_index", "target", "prediction", "quadrant"]
STRATA = ("TP", "TN", "FP", "FN")
THREAD_VARS = ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
               "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")


def single_thread_env() -> None:
    """Call before numpy is imported in a worker."""
    for var in THREAD_VARS:
        os.environ[var] = "1"


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
def config(path: Path = CONFIG_PATH) -> dict:
    with open(path, "rb") as fh:
        return tomllib.load(fh)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


OPERATIONAL_TABLES = ("resources", "sync")


def config_hash(path: Path = CONFIG_PATH) -> str:
    """SHA-256 of the experimental design: every table of the config except the
    operational ones (resource limits, sync), in canonical JSON. Changing a limit or the
    push schedule therefore does not split a cohort, and neither does git's CRLF
    conversion or a comment; any change to the design does."""
    with open(path, "rb") as fh:
        cfg = tomllib.load(fh)
    design = {k: v for k, v in cfg.items() if k not in OPERATIONAL_TABLES}
    return sha256_bytes(json.dumps(design, sort_keys=True, separators=(",", ":")).encode())


def git_commit() -> str | None:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True, timeout=10).stdout.strip() or None
    except Exception:
        return None


def seeds_for(cfg: dict, dataset: str) -> list[int]:
    role = cfg["datasets"][dataset].get("role", "cross")
    return list(cfg["seeds"]["adult" if role == "main" else "other"])


def all_quality_jobs(cfg: dict, datasets=None, models=None, explainers=None,
                     seeds=None) -> list[tuple[str, str, int, str]]:
    jobs = []
    for d in datasets or cfg["datasets"]:
        for m in models or cfg["models"]:
            for s in seeds or seeds_for(cfg, d):
                for e in explainers or cfg["explainers"]:
                    only = cfg["explainers"].get(e, {}).get("models")   # optional restriction
                    if only and m not in only:
                        continue
                    jobs.append((d, m, int(s), e))
    return jobs


def job_stem(dataset: str, model: str, seed: int, explainer: str) -> Path:
    return RESULTS / "quality" / dataset / model / f"seed_{seed}" / explainer


def timing_stem(dataset: str, model: str, seed: int) -> Path:
    return RESULTS / "timing" / dataset / model / f"seed_{seed}" / "timing"


# --------------------------------------------------------------------------
# Crash-safe I/O
# --------------------------------------------------------------------------
def atomic_write_text(path: Path, text: str) -> None:
    """Write a whole file so that readers see the old or the new content, never half."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
        fh.flush()
        os.fsync(fh.fileno())
    for attempt in range(20):           # Windows: a reader may hold the target briefly
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            time.sleep(0.05 * (attempt + 1))
    os.replace(tmp, path)


def atomic_write_json(path: Path, obj: Any) -> None:
    atomic_write_text(path, json.dumps(obj, indent=1, default=str))


def append_jsonl(path: Path, row: dict) -> None:
    """Append one line and force it to disk: a crash loses at most the line being written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(row, default=str, separators=(",", ":")) + "\n"
    # After a crash mid-write the file may end without a newline: start a fresh line so
    # the damaged fragment stays isolated (and is skipped by read_jsonl).
    if path.exists() and path.stat().st_size:
        with open(path, "rb") as fh:
            fh.seek(-1, os.SEEK_END)
            if fh.read(1) != b"\n":
                line = "\n" + line
    with open(path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(line)
        fh.flush()
        os.fsync(fh.fileno())


def read_jsonl(path: Path) -> Iterator[dict]:
    """Rows of a JSONL file; a truncated or damaged line (a crash mid-write) is skipped."""
    if not path.exists():
        return
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def read_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def done_keys(path: Path, key: str = "instance_id") -> set:
    return {row[key] for row in read_jsonl(path) if key in row}


# --------------------------------------------------------------------------
# Host snapshot and resource helpers (psutil; Windows-specific parts guarded)
# --------------------------------------------------------------------------
def host_snapshot() -> dict:
    import psutil
    vm = psutil.virtual_memory()
    du = psutil.disk_usage(str(ROOT))
    snap = {
        "time": time.time(),
        "cpu_percent": psutil.cpu_percent(interval=None),
        "ram_total_gb": vm.total / 2**30,
        "ram_available_gb": vm.available / 2**30,
        "disk_free_gb": du.free / 2**30,
        "logical_cpus": psutil.cpu_count(),
    }
    try:
        f = psutil.cpu_freq()
        snap["cpu_mhz"] = f.current if f else None
    except Exception:
        snap["cpu_mhz"] = None
    try:
        b = psutil.sensors_battery()
        snap["ac_power"] = None if b is None else bool(b.power_plugged)
        snap["battery_percent"] = None if b is None else b.percent
    except Exception:
        snap["ac_power"], snap["battery_percent"] = None, None
    return snap


def static_host_record() -> dict:
    import platform
    rec = {"node": platform.node(), "platform": platform.platform(),
           "processor": platform.processor(), "python": platform.python_version()}
    if sys.platform == "win32":
        with contextlib.suppress(Exception):
            rec["power_scheme"] = subprocess.run(["powercfg", "/getactivescheme"],
                                                 capture_output=True, text=True,
                                                 timeout=10).stdout.strip()
    from importlib import metadata
    rec["packages"] = {}
    for p in ("numpy", "pandas", "scipy", "scikit-learn", "xgboost", "shap", "lime",
              "alibi", "dice-ml", "psutil"):
        try:
            rec["packages"][p] = metadata.version(p)
        except metadata.PackageNotFoundError:
            rec["packages"][p] = None
    return rec


class SleepBlocker:
    """Keep Windows awake while a long run is in progress (no effect elsewhere)."""
    ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001

    def __enter__(self):
        if sys.platform == "win32":
            with contextlib.suppress(Exception):
                import ctypes
                ctypes.windll.kernel32.SetThreadExecutionState(
                    self.ES_CONTINUOUS | self.ES_SYSTEM_REQUIRED)
        return self

    def __exit__(self, *exc):
        if sys.platform == "win32":
            with contextlib.suppress(Exception):
                import ctypes
                ctypes.windll.kernel32.SetThreadExecutionState(self.ES_CONTINUOUS)
        return False


def idle_seconds() -> float | None:
    """Seconds since the last keyboard or mouse input (Windows); None if unknown."""
    if sys.platform != "win32":
        return None
    try:
        import ctypes

        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

        info = LASTINPUTINFO()
        info.cbSize = ctypes.sizeof(LASTINPUTINFO)
        if not ctypes.windll.user32.GetLastInputInfo(ctypes.byref(info)):
            return None
        return (ctypes.windll.kernel32.GetTickCount() - info.dwTime) / 1000.0
    except Exception:
        return None


def set_below_normal(proc=None) -> bool:
    try:
        import psutil
        p = proc or psutil.Process()
        if sys.platform == "win32":
            p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        else:
            p.nice(10)
        return True
    except Exception:
        return False


def pin_to_cpu(cpu: int) -> str:
    try:
        import psutil
        psutil.Process().cpu_affinity([cpu])
        return f"pinned to logical CPU {cpu}"
    except Exception as exc:
        return f"not pinned ({type(exc).__name__}: {exc})"


def process_tree_rss_gb(pid: int) -> float:
    import psutil
    try:
        p = psutil.Process(pid)
        rss = p.memory_info().rss
        for c in p.children(recursive=True):
            with contextlib.suppress(psutil.Error):
                rss += c.memory_info().rss
        return rss / 2**30
    except psutil.Error:
        return 0.0


def microbenchmark(n: int = 160, reps: int = 30) -> float:
    """A fixed single-threaded workload (ms): drift of this number means throttling."""
    import numpy as np
    rng = np.random.default_rng(0)
    a = rng.standard_normal((n, n))
    t = time.perf_counter()
    for _ in range(reps):
        a = np.tanh(a @ a.T / n)
    return (time.perf_counter() - t) * 1e3


# --------------------------------------------------------------------------
# Admission control (pure logic: unit-tested)
# --------------------------------------------------------------------------
def admission_decision(available_gb: float, expected_peak_gb: float, running: int,
                       max_workers: int, reserve_gb: float, pause_below_gb: float,
                       ac_power: bool | None, disk_free_gb: float, disk_pause_gb: float,
                       stop_requested: bool) -> tuple[bool, str]:
    if stop_requested:
        return False, "stop requested"
    if running >= max_workers:
        return False, f"{running} workers running (max {max_workers})"
    if ac_power is False:
        return False, "on battery: admission paused until AC power returns"
    if disk_free_gb < disk_pause_gb:
        return False, f"disk free {disk_free_gb:.1f} GB < {disk_pause_gb} GB"
    if available_gb < pause_below_gb:
        return False, f"RAM available {available_gb:.1f} GB < {pause_below_gb} GB"
    if available_gb - expected_peak_gb < reserve_gb:
        return False, (f"RAM available {available_gb:.1f} GB minus expected peak "
                       f"{expected_peak_gb:.1f} GB < reserve {reserve_gb} GB")
    return True, "ok"


def job_from_cmdline(cmd: list[str]) -> tuple | None:
    """(dataset, model, seed, explainer) of a `paper_b_run.py job ...` command line."""
    if not any(str(c).endswith("paper_b_run.py") for c in cmd) or "job" not in cmd:
        return None
    opt = {}
    for k in ("--dataset", "--model", "--seed", "--explainer"):
        if k in cmd and cmd.index(k) + 1 < len(cmd):
            opt[k] = cmd[cmd.index(k) + 1]
    if len(opt) != 4:
        return None
    try:
        return opt["--dataset"], opt["--model"], int(opt["--seed"]), opt["--explainer"]
    except ValueError:
        return None


def jobs_running_elsewhere(governor_pid: int) -> dict:
    """{job: pid} of quality workers alive on this machine that are not descendants of this
    governor: workers left by a governor that died keep running and writing their JSONL,
    and a second copy of the job would write the same file (2026-11-07 18:36)."""
    import psutil
    try:
        mine = {p.pid for p in psutil.Process(governor_pid).children(recursive=True)}
    except (psutil.Error, ValueError):
        mine = set()
    out = {}
    for p in psutil.process_iter(["pid", "cmdline"]):
        try:
            job = job_from_cmdline(p.info["cmdline"] or [])
        except psutil.Error:
            continue
        if job and p.info["pid"] not in mine:
            out.setdefault(job, p.info["pid"])
    return out


def reload_resources(current: dict, path: Path | None = None) -> tuple[dict, list[str]]:
    """The [resources] table read again from the config (operational, outside the design
    hash), so a limit can be tuned without restarting the run and losing the instances in
    progress. A config that does not parse keeps the current limits. Returns the limits and
    the changes as 'key: old -> new'."""
    try:
        new = dict(config(path or CONFIG_PATH)["resources"])
    except Exception:                                  # mid-edit or invalid: keep running
        return current, []
    changed = [f"{k}: {current.get(k)} -> {v}" for k, v in new.items() if current.get(k) != v]
    return new, changed


def plan_admissions(candidates, available_gb: float, running: int, max_workers: int,
                    reserve_gb: float, pause_below_gb: float, ac_power: bool | None,
                    disk_free_gb: float, disk_pause_gb: float, stop_requested: bool):
    """Which queued jobs to start now, in queue order: ([jobs], reason shown when waiting).

    `candidates` is [(job, expected_peak_gb, must_run_alone)]. A job that does not fit the
    RAM reserve is passed over, not waited for, so smaller jobs behind it still start
    (strict FIFO stalled the run at 3 of 6 workers while other programs held the memory,
    2026-11-07). A passed-over job starts alone once none of ours is running, if it leaves
    at least `pause_below_gb`; the worker cap and the kill-newest rule still guard it. Any
    other refusal (stop, worker limit, battery, disk, RAM below the pause floor) ends the
    scan. A job that must run alone starts only when nothing runs, and nothing joins it."""
    start, reason = [], "ok"
    for job, peak, alone in candidates:
        ok, why = admission_decision(available_gb, peak, running, max_workers, reserve_gb,
                                     pause_below_gb, ac_power, disk_free_gb, disk_pause_gb,
                                     stop_requested)
        ram_only = not ok and "minus expected peak" in why
        if not ok and not ram_only:
            return start, (why if not start else reason)
        if alone and running:
            reason = reason if reason != "ok" else "a job that must run alone waits for the others"
            continue
        if ram_only:
            if running == 0 and available_gb - peak >= pause_below_gb:
                start.append(job)                     # alone, nothing else of ours running
                return start, f"{why}; started alone"
            reason = reason if reason != "ok" else f"{why} (smaller jobs go first)"
            continue
        start.append(job)
        available_gb -= peak                          # account for it before the next one
        running += 1
        if alone:
            break
    return start, reason


def expected_peak_gb(peaks: dict, model: str, explainer: str, dataset: str,
                     default_gb: float) -> float:
    """95th percentile of recorded peaks for this job type, else the default.

    Peaks are keyed 'dataset|model|explainer' and also 'model|explainer'; the most
    specific key with at least 2 records is used, with a 20% margin."""
    for key in (f"{dataset}|{model}|{explainer}", f"{model}|{explainer}"):
        vals = sorted(peaks.get(key, []))
        if len(vals) >= 2:
            k = min(len(vals) - 1, int(round(0.95 * (len(vals) - 1))))
            return max(0.5, vals[k] * 1.2)
    return default_gb


def stuck_at_startup(beat_seen: bool, born: float, now: float, limit_s: float) -> bool:
    """A worker is stuck at start-up only if it has NEVER reported a heartbeat within the
    limit. A worker that reported one and then removed it is finishing, not stuck (a false
    kill at job end was seen in the pilot, 2026-11-06)."""
    return (not beat_seen) and (now - born > limit_s)


def quiet_gate(other_cpu_percent: float, idle_s: float | None, ac_power: bool | None,
               max_other_cpu: float, require_idle_s: float | None,
               quality_workers_running: int) -> tuple[bool, str]:
    if quality_workers_running:
        return False, f"{quality_workers_running} quality workers running"
    if ac_power is False:
        return False, "on battery"
    if other_cpu_percent > max_other_cpu:
        return False, f"other CPU load {other_cpu_percent:.0f}% > {max_other_cpu:.0f}%"
    if require_idle_s and idle_s is not None and idle_s < require_idle_s:
        return False, f"user active {idle_s:.0f} s ago (< {require_idle_s:.0f} s)"
    return True, "quiet"


# --------------------------------------------------------------------------
# Model-call counter
# --------------------------------------------------------------------------
class CallCounter:
    """Counts outermost calls to predict/predict_proba and the rows they receive."""

    def __init__(self) -> None:
        import threading
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
                    shape = getattr(X, "shape", None)
                    counter.rows += int(shape[0]) if shape else len(X)
                except Exception:
                    counter.rows += 1
            counter._local.depth = depth + 1
            try:
                return fn(self_model, X, *args, **kwargs)
            finally:
                counter._local.depth = depth

        wrapped.__wrapped__ = fn
        wrapped.__name__ = getattr(fn, "__name__", "wrapped")
        wrapped._paper_b_counted = True
        return wrapped


def install_counter(counter: CallCounter, classes: Iterable[type]) -> list[str]:
    """Wrap predict/predict_proba as resolved through each class's MRO (inherited plain
    functions are set on the concrete class; sklearn `available_if` descriptors are
    wrapped in their `.fn`).

    "Already counted" is our own marker, not `__wrapped__`: XGBoost decorates
    XGBClassifier.predict with functools.wraps, which sets `__wrapped__`, so the old test
    skipped it and Anchors on XGBoost (which calls predict) recorded 0 calls (2026-11-08)."""
    import inspect
    done = []
    for cls in classes:
        for name in ("predict_proba", "predict"):
            raw = next((k.__dict__[name] for k in cls.__mro__ if name in k.__dict__), None)
            if raw is None:
                continue
            if inspect.isfunction(raw):
                if not getattr(raw, "_paper_b_counted", False):
                    setattr(cls, name, counter.wrap(raw))
                    done.append(f"{cls.__name__}.{name}")
            elif inspect.isfunction(getattr(raw, "fn", None)):
                if not getattr(raw.fn, "_paper_b_counted", False):
                    raw.fn = counter.wrap(raw.fn)
                    done.append(f"{cls.__name__}.{name} (available_if)")
    return done


def model_classes() -> list[type]:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.neural_network import MLPClassifier
    from sklearn.svm import SVC
    out: list[type] = [RandomForestClassifier, LogisticRegression, MLPClassifier, SVC]
    with contextlib.suppress(ImportError):
        from xgboost import XGBClassifier
        out.append(XGBClassifier)
    return out


# --------------------------------------------------------------------------
# Datasets
# --------------------------------------------------------------------------
def _prepare_openml(name: str, spec: dict, cfg: dict) -> dict:
    import numpy as np
    from sklearn.compose import ColumnTransformer
    from sklearn.datasets import fetch_openml
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    X, y = fetch_openml(data_id=int(spec["openml_id"]), as_frame=True, return_X_y=True,
                        data_home=str(DATA_DIR / "openml_cache"), parser="auto")
    y = (y.astype(str) == str(spec["positive"])).astype(int).to_numpy()
    if y.min() == y.max():
        raise ValueError(f"{name}: positive label {spec['positive']!r} gives one class")
    cat = [c for c in X.columns if str(X[c].dtype) in ("category", "object", "bool")]
    num = [c for c in X.columns if c not in cat]
    if X[num].isna().any().any() or X[cat].isna().any().any():
        raise ValueError(f"{name}: missing values; no imputation is defined for it")
    for c in cat:
        X[c] = X[c].astype(str)
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=cfg["cohort"]["test_size"], random_state=cfg["cohort"]["split_seed"],
        stratify=y)
    pre = ColumnTransformer([
        ("num", StandardScaler(), num),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat),
    ])
    A_tr = pre.fit_transform(X_tr).astype(float)
    A_te = pre.transform(X_te).astype(float)
    names = [str(n).split("__", 1)[-1] for n in pre.get_feature_names_out()]
    return {"X_train": A_tr, "X_test": A_te, "y_train": np.asarray(y_tr),
            "y_test": np.asarray(y_te), "feature_names": names,
            "n_numeric_inputs": len(num), "n_categorical_inputs": len(cat)}


def _prepare_src(name: str, spec: dict, cfg: dict) -> dict:
    import numpy as np
    if spec["loader"] == "src_adult":
        from src.data_loading.adult import load_adult
        X_tr, X_te, y_tr, y_te, names, _ = load_adult(
            cache_dir=str(ROOT / "data"), random_state=cfg["cohort"]["split_seed"],
            test_size=cfg["cohort"]["test_size"])
    else:
        from src.data_loading.cross_dataset import load_tabular_dataset
        X_tr, X_te, y_tr, y_te, names, _ = load_tabular_dataset(
            name, cache_dir=str(ROOT / "data"), random_state=cfg["cohort"]["split_seed"],
            test_size=cfg["cohort"]["test_size"])
    return {"X_train": np.asarray(X_tr, dtype=float), "X_test": np.asarray(X_te, dtype=float),
            "y_train": np.asarray(y_tr).astype(int), "y_test": np.asarray(y_te).astype(int),
            "feature_names": [str(n) for n in names]}


def prepare_dataset(name: str, cfg: dict) -> dict:
    """Prepare and cache one dataset (deterministic); return its summary."""
    import numpy as np
    spec = cfg["datasets"][name]
    data = _prepare_openml(name, spec, cfg) if spec["loader"] == "openml" else \
        _prepare_src(name, spec, cfg)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / f"{name}.npz"
    tmp = DATA_DIR / f".{name}.{os.getpid()}.npz"
    np.savez_compressed(tmp, X_train=data["X_train"], X_test=data["X_test"],
                        y_train=data["y_train"], y_test=data["y_test"],
                        feature_names=np.array(data["feature_names"]))
    os.replace(tmp, out)
    return {"dataset": name, "file": str(out.relative_to(ROOT)), "sha256": sha256_file(out),
            "n_train": int(len(data["y_train"])), "n_test": int(len(data["y_test"])),
            "n_features": int(data["X_train"].shape[1]),
            "positive_rate": float(np.mean(np.concatenate([data["y_train"], data["y_test"]])))}


def load_dataset(name: str) -> dict:
    import numpy as np
    path = DATA_DIR / f"{name}.npz"
    if not path.exists():
        raise FileNotFoundError(f"{path} missing: run `paper_b_run.py prepare` first")
    z = np.load(path, allow_pickle=False)
    d = {k: z[k] for k in ("X_train", "X_test", "y_train", "y_test")}
    d["feature_names"] = [str(n) for n in z["feature_names"]]
    d["baseline"] = d["X_train"].mean(axis=0)
    return d


def training_subsample(y, cap: int, seed: int):
    """Indices of a stratified subsample of at most `cap` rows (all rows if fewer)."""
    import numpy as np
    n = len(y)
    if n <= cap:
        return np.arange(n)
    from sklearn.model_selection import train_test_split
    idx, _ = train_test_split(np.arange(n), train_size=cap, random_state=seed, stratify=y)
    return np.sort(idx)


# --------------------------------------------------------------------------
# Models: train, freeze, verify
# --------------------------------------------------------------------------
def build_model(spec: dict):
    import importlib
    mod, cls = spec["class"].rsplit(".", 1)
    params = dict(spec.get("params", {}))
    if "hidden_layer_sizes" in params:
        params["hidden_layer_sizes"] = tuple(params["hidden_layer_sizes"])
    return getattr(importlib.import_module(mod), cls)(**params)


def model_path(dataset: str, model: str) -> Path:
    return MODELS_DIR / dataset / f"{model}.joblib"


def model_structure(est) -> dict:
    info: dict = {}
    if hasattr(est, "estimators_") and hasattr(est.estimators_[0], "tree_"):
        info["trees"] = len(est.estimators_)
        info["leaves"] = int(sum(t.tree_.n_leaves for t in est.estimators_))
        info["max_depth_realised"] = int(max(t.tree_.max_depth for t in est.estimators_))
    if type(est).__name__ == "XGBClassifier":
        with contextlib.suppress(Exception):
            df = est.get_booster().trees_to_dataframe()
            info["trees"] = int(df["Tree"].nunique())
            info["leaves"] = int((df["Feature"] == "Leaf").sum())
    if hasattr(est, "support_vectors_"):
        info["support_vectors"] = int(est.support_vectors_.shape[0])
    return info


def read_manifest() -> dict[tuple[str, str], dict]:
    if not MANIFEST.exists():
        return {}
    with open(MANIFEST, newline="", encoding="utf-8") as fh:
        return {(r["dataset"], r["model"]): r for r in csv.DictReader(fh)}


def write_manifest(rows: dict[tuple[str, str], dict]) -> None:
    fields = ["dataset", "model", "file", "sha256", "bytes", "train_rows", "test_accuracy",
              "trained_utc", "structure", "data_sha256"]
    lines = []
    import io
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for key in sorted(rows):
        w.writerow({f: rows[key].get(f, "") for f in fields})
    lines.append(buf.getvalue())
    atomic_write_text(MANIFEST, "".join(lines))


class ModelHashMismatch(RuntimeError):
    pass


def load_model_checked(dataset: str, model: str):
    """Load a frozen model and verify its SHA-256 against the manifest (F7a guard)."""
    import joblib
    row = read_manifest().get((dataset, model))
    if row is None:
        raise ModelHashMismatch(f"{dataset}/{model} not in {MANIFEST}: run prepare")
    path = ROOT / row["file"]
    actual = sha256_file(path)
    if actual != row["sha256"]:
        raise ModelHashMismatch(f"{path}: sha256 {actual[:12]} != manifest {row['sha256'][:12]}")
    return joblib.load(path), row["sha256"]


# --------------------------------------------------------------------------
# Explainers (src wrappers, EXP2 settings unless the cohort says otherwise)
# --------------------------------------------------------------------------
def build_explainer(variant: str, cfg: dict, model_name: str, model, data: dict, seed: int):
    import math
    import pandas as pd
    spec = cfg["explainers"][variant]
    X_tr, names = data["X_train"], data["feature_names"]
    m = X_tr.shape[1]
    method = spec["method"]
    if method == "shap":
        from src.xai.shap_tabular import SHAPTabularWrapper
        # TreeSHAP for tree ensembles unless the variant forces KernelSHAP (WP5: separates the
        # method from the TreeSHAP implementation). Matched-size ensembles of WP2b ("rf_*",
        # "xgb_*") are tree models too.
        tree = (model_name in ("rf", "xgb") or model_name.startswith(("rf_", "xgb_"))) \
            and spec.get("algorithm", "auto") != "kernel"
        kwargs = {}
        if not tree:
            ns = spec.get("kernel_nsamples_by_model", {}).get(model_name,
                                                               spec.get("kernel_nsamples", "auto"))
            if ns != "auto":
                kwargs["nsamples"] = int(ns)
        exp = SHAPTabularWrapper(model=model, training_data=X_tr, feature_names=names,
                                 model_type="tree" if tree else "kernel",
                                 n_background_samples=int(spec["n_background_samples"]),
                                 **kwargs)
        info = {"shap_algorithm": "TreeExplainer" if tree else "KernelExplainer", **kwargs}
    elif method == "lime":
        from src.xai.lime_tabular import LIMETabularWrapper
        kw = spec.get("kernel_width", "default")
        kernel_width = None if kw == "default" else float(kw)
        nf = m if spec.get("num_features") == "all" else int(spec["num_features"])
        exp = LIMETabularWrapper(training_data=X_tr, feature_names=names,
                                 class_names=["0", "1"], num_features=nf,
                                 num_samples=int(spec["num_samples"]), random_state=seed,
                                 kernel_width=kernel_width)
        info = {"kernel_width_effective": 0.75 * math.sqrt(m) if kernel_width is None
                else kernel_width, "num_features": nf}
    elif method == "anchors":
        from src.xai.anchors_wrapper import AnchorsTabularWrapper
        exp = AnchorsTabularWrapper(training_data=X_tr, feature_names=names,
                                    threshold=float(spec["threshold"]))
        info = {"threshold": spec["threshold"]}
    elif method == "dice":
        from src.xai.dice_wrapper import DiCETabularWrapper
        df = pd.DataFrame(X_tr, columns=names)
        df["target"] = data["y_train"]
        exp = DiCETabularWrapper(model=model, training_data=df, feature_names=names,
                                 target_column="target", categorical_features=[],
                                 num_counterfactuals=int(spec["num_counterfactuals"]))
        info = {"num_counterfactuals": spec["num_counterfactuals"]}
    else:
        raise ValueError(f"unknown explainer method {method!r}")
    return exp, info


def instance_seed(seed: int, *parts: Any) -> int:
    """Deterministic 32-bit seed from the cohort seed and the instance coordinates."""
    h = hashlib.sha256(("|".join([str(seed), *map(str, parts)])).encode()).digest()
    return int.from_bytes(h[:4], "little")


def select_instances(model, data: dict, seed: int, per_stratum: int):
    """Stratified TP/TN/FP/FN sample of the fixed test split (src sampler)."""
    import pandas as pd
    from src.evaluation.sampler import EvaluationSampler
    X_te = pd.DataFrame(data["X_test"], columns=data["feature_names"])
    sampler = EvaluationSampler(model=model, X_test=X_te, y_test=pd.Series(data["y_test"]),
                                random_state=seed)
    inst = sampler.sample_stratified_by_error(n_per_group=per_stratum)
    return inst


def first_per_stratum(instances, k: int) -> set[int]:
    keep = set()
    for q in STRATA:
        sub = instances[instances["quadrant"] == q]
        keep.update(int(i) for i in sub["original_index"].head(k))
    return keep


def onehot_groups(feature_names, X_train) -> tuple[list[int], dict[str, list[int]]]:
    """Numeric column indices and one-hot groups {feature: [indices]}.

    The encoders name a one-hot column `<feature>_<category>`, but feature names and
    categories may themselves contain underscores (Phishing `having_IP_Address_1`, German
    Credit `checking_status_<0`) and numeric names may share a prefix (Spambase
    `word_freq_*`), so the name alone cannot tell. A prefix p (cut at an underscore) is a
    one-hot group when the columns named `p_*` are two or more, take only the values 0 and 1
    in the training data, and every training row has exactly one 1 among them. Prefixes are
    tried longest first and a column joins one group only, so nested feature names (`a` and
    `a_b`) separate. Standardized numeric columns never qualify.
    """
    import numpy as np
    names = [str(n) for n in feature_names]
    X = np.asarray(X_train, dtype=float)
    if X.ndim != 2 or X.shape[1] != len(names):
        raise ValueError(f"X_train has {X.shape[-1]} columns for {len(names)} names")
    binary = np.all((X == 0) | (X == 1), axis=0)
    prefixes = {n[:i] for j, n in enumerate(names) if binary[j]
                for i, ch in enumerate(n) if ch == "_" and i > 0}
    groups: dict[str, list[int]] = {}
    in_group: set[int] = set()
    for p in sorted(prefixes, key=lambda s: (-len(s), s)):          # longest first
        idx = [j for j, n in enumerate(names) if n.startswith(p + "_") and j not in in_group]
        if len(idx) >= 2 and binary[idx].all() and np.all(X[:, idx].sum(axis=1) == 1):
            groups[p] = idx
            in_group.update(idx)
    groups = dict(sorted(groups.items(), key=lambda kv: kv[1][0]))  # in column order
    numeric = [j for j in range(len(names)) if j not in in_group]
    return numeric, groups


class ValidStabilityMetric:
    """Stability with perturbations that keep the encoded instance valid (WP4, control b):
    Gaussian noise (sigma) on the numeric columns only; each one-hot group is resampled from
    the training marginals with probability `p_resample`, else kept. Same output and the same
    cosine computation as src.metrics.stability.StabilityMetric; uses np.random (seeded by the
    caller per instance, as the main protocol)."""

    def __init__(self, n_iterations: int, perturbation_std: float, X_train, feature_names,
                 p_resample: float = 0.1):
        import numpy as np
        self.n_iterations, self.sigma, self.p = n_iterations, perturbation_std, p_resample
        self.numeric, self.groups = onehot_groups(feature_names, X_train)
        self.marginals = {}
        for g, idx in self.groups.items():
            counts = (np.asarray(X_train)[:, idx] > 0.5).sum(0).astype(float)
            self.marginals[g] = counts / counts.sum() if counts.sum() else \
                np.full(len(idx), 1.0 / len(idx))

    def perturb(self, x):
        import numpy as np
        z = np.array(x, dtype=float).copy()
        z[self.numeric] += np.random.normal(0, self.sigma, size=len(self.numeric))
        for g, idx in self.groups.items():
            if np.random.random_sample() < self.p:
                k = np.random.choice(len(idx), p=self.marginals[g])
                z[idx] = 0.0
                z[idx[k]] = 1.0
        return z

    def compute(self, _w, model=None, data=None, explainer_func=None) -> dict:
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity
        x = np.array(data, dtype=float)
        x = x[0] if x.ndim > 1 else x
        vecs = []
        for _ in range(self.n_iterations):
            v = explainer_func(model, self.perturb(x).reshape(1, -1))["feature_importance"]
            v = np.asarray(v, dtype=float)
            vecs.append(v[0] if v.ndim > 1 else v)
        sims = cosine_similarity(np.array(vecs))[np.triu_indices(self.n_iterations, k=1)]
        return {"cosine_similarity_mean": float(np.mean(sims)),
                "cosine_similarity_std": float(np.std(sims)), "n_iterations": self.n_iterations}


def round_vec(v, digits: int) -> list[float]:
    import numpy as np
    return [float(x) for x in np.round(np.asarray(v, dtype=float), digits)]
