"""Paper F: datasets, models, explainers and measures (ANALYSIS_PLAN.md, version 2).

Everything Paper F computes goes through this module, so that the profile, the pilot and
the full run use the same code. Settings are read from docs/reports/paper_f/paper_f_config.toml.

Explanations are computed in the encoded feature space (scaled numeric columns followed by
one-hot columns), as in EXP2 and EXP3. A "feature" of a measure is an encoded column.
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import time
import tomllib
import warnings
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
os.environ.setdefault("TQDM_DISABLE", "1")

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "docs" / "reports" / "paper_f" / "paper_f_config.toml"
DATA_DIR = ROOT / "data" / "openml" / "paper_f"
OUT = ROOT / "outputs" / "analysis" / "paper_f"
OPENML = "https://www.openml.org/api/v1/json/data/{id}"
MODELS = ("logreg", "rf", "xgb", "mlp")
EXPLAINERS = ("lime", "shap", "anchors", "dice")
TARGET = "__target__"


def config() -> dict:
    with CONFIG_PATH.open("rb") as fh:
        return tomllib.load(fh)


def dataset_entry(key: str, cfg: dict | None = None) -> dict:
    for entry in (cfg or config())["dataset"]:
        if entry["key"] == key:
            return entry
    # Datasets added by the widening step of the plan are listed in candidates.csv only.
    listing = OUT / "candidates.csv"
    if listing.exists():
        rows = pd.read_csv(listing)
        hit = rows[rows["key"] == key]
        if len(hit):
            return {"key": key, "id": int(hit.iloc[0]["openml_id"])}
    raise KeyError(f"dataset {key!r} is not in {CONFIG_PATH.name} or candidates.csv")


# --- data ----------------------------------------------------------------------

def _curl(url: str, target: Path) -> None:
    # curl uses the system certificate store; Python's own store rejects some networks' chains.
    tmp = target.with_suffix(target.suffix + ".part")
    subprocess.run(["curl", "-sSL", "--fail", "--retry", "6", "--retry-all-errors",
                    "--retry-delay", "5", "--max-time", "600", "-o", str(tmp), url], check=True)
    tmp.replace(target)


def fetch(entry: dict) -> None:
    """Download the OpenML record and the data file of one dataset, unless already present."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    desc_path = DATA_DIR / f"{entry['id']}.json"
    if not desc_path.exists():
        _curl(OPENML.format(id=entry["id"]), desc_path)
    desc = json.loads(desc_path.read_text(encoding="utf-8"))["data_set_description"]
    data_path = DATA_DIR / f"{entry['id']}.parquet"
    if not data_path.exists():
        _curl(desc["parquet_url"], data_path)


def description(entry: dict) -> dict:
    path = DATA_DIR / f"{entry['id']}.json"
    return json.loads(path.read_text(encoding="utf-8"))["data_set_description"]


def _as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return [str(v) for v in value]


def load_frame(entry: dict) -> tuple[pd.DataFrame, pd.Series, dict]:
    """Raw features, binary target (1 = minority class) and the source record of a dataset."""
    desc = description(entry)
    df = pd.read_parquet(DATA_DIR / f"{entry['id']}.parquet")
    target = desc["default_target_attribute"]
    drop = [c for c in _as_list(desc.get("row_id_attribute")) + _as_list(desc.get("ignore_attribute"))
            if c in df.columns and c != target]
    df = df.drop(columns=drop)
    df = df[df[target].notna()].reset_index(drop=True)
    labels = df[target].astype(str)
    counts = labels.value_counts()
    if len(counts) != 2:
        raise ValueError(f"{entry['key']}: target has {len(counts)} classes, not 2")
    minority = sorted(counts.index, key=lambda c: (counts[c], c))[0]
    y = (labels == minority).astype(int)
    X = df.drop(columns=[target])
    meta = {"openml_id": int(desc["id"]), "name": desc["name"], "version": int(desc["version"]),
            "licence": desc.get("licence") or "", "target": target, "positive_class": minority,
            "dropped_columns": drop}
    return X, y, meta


def feature_types(X: pd.DataFrame) -> tuple[list[str], list[str]]:
    numeric = [c for c in X.columns
               if pd.api.types.is_numeric_dtype(X[c]) and not pd.api.types.is_bool_dtype(X[c])]
    return numeric, [c for c in X.columns if c not in numeric]


def split(X: pd.DataFrame, y: pd.Series, seed: int, cfg: dict) -> dict:
    """Stratified split and preprocessing fitted on the training part."""
    numeric, categorical = feature_types(X)
    X = X.copy()
    for c in categorical:
        X[c] = X[c].astype(object).where(X[c].notna(), np.nan)
        X[c] = X[c].map(lambda v: v if isinstance(v, float) and math.isnan(v) else str(v))
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=cfg["test_size"], random_state=seed, stratify=y)
    transformers = []
    if numeric:
        transformers.append(("num", Pipeline([("imputer", SimpleImputer(strategy="median")),
                                              ("scaler", StandardScaler())]), numeric))
    if categorical:
        transformers.append(("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="infrequent_if_exist", sparse_output=False,
                                     max_categories=cfg["preprocessing"]["max_categories"])),
        ]), categorical))
    pre = ColumnTransformer(transformers, verbose_feature_names_out=False)
    A_tr = np.asarray(pre.fit_transform(X_tr), dtype=float)
    A_te = np.asarray(pre.transform(X_te), dtype=float)
    names = [str(n) for n in pre.get_feature_names_out()]
    is_numeric = np.zeros(len(names), dtype=bool)
    is_numeric[:len(numeric)] = True
    return {"X_train": A_tr, "X_test": A_te, "y_train": y_tr.to_numpy(), "y_test": y_te.to_numpy(),
            "names": names, "is_numeric": is_numeric, "test_index": X_te.index.to_numpy()}


# --- models --------------------------------------------------------------------

def make_model(name: str, seed: int, cfg: dict):
    p = dict(cfg["models"][name])
    if name == "logreg":
        from sklearn.linear_model import LogisticRegression
        return LogisticRegression(random_state=seed, **p)
    if name == "rf":
        from sklearn.ensemble import RandomForestClassifier
        return RandomForestClassifier(random_state=seed, n_jobs=1, **p)
    if name == "xgb":
        from xgboost import XGBClassifier
        return XGBClassifier(random_state=seed, n_jobs=1, eval_metric="logloss", **p)
    if name == "mlp":
        from sklearn.neural_network import MLPClassifier
        p["hidden_layer_sizes"] = tuple(p["hidden_layer_sizes"])
        return MLPClassifier(random_state=seed, **p)
    raise KeyError(name)


def pick_instances(pred: np.ndarray, n: int, seed: int) -> np.ndarray:
    """Positions in the test split: n instances stratified by predicted class, or all."""
    idx = np.arange(len(pred))
    if len(idx) <= n:
        return idx
    counts = np.bincount(pred, minlength=2)
    stratify = pred if counts.min() >= 2 else None
    chosen, _ = train_test_split(idx, train_size=n, random_state=seed, stratify=stratify)
    return np.sort(chosen)


# --- explainers ----------------------------------------------------------------

class Failure(Exception):
    """The explainer returned no explanation for this instance."""


class Explainer:
    """explain(x, seed) -> (weights over the encoded features, extra values)."""

    name = ""

    def __init__(self, model, data: dict, seed: int, cfg: dict):
        self.model, self.data, self.seed = model, data, seed
        self.cfg = cfg["explainers"][self.name]
        self.d = data["X_train"].shape[1]

    def explain(self, x: np.ndarray, seed: int) -> tuple[np.ndarray, dict]:
        raise NotImplementedError


class Lime(Explainer):
    name = "lime"

    def __init__(self, model, data, seed, cfg):
        super().__init__(model, data, seed, cfg)
        from lime.lime_tabular import LimeTabularExplainer
        self.lime = LimeTabularExplainer(
            data["X_train"], feature_names=data["names"], class_names=["0", "1"],
            mode="classification", discretize_continuous=False,
            kernel_width=self.cfg["kernel_width"], random_state=seed)

    def explain(self, x, seed):
        exp = self.lime.explain_instance(x, self.model.predict_proba, labels=(1,),
                                         num_features=self.cfg["num_features"],
                                         num_samples=self.cfg["num_samples"])
        w = np.zeros(self.d)
        for j, value in exp.as_map()[1]:
            w[j] = value
        return w, {}


class Shap(Explainer):
    name = "shap"

    def __init__(self, model, data, seed, cfg):
        super().__init__(model, data, seed, cfg)
        import shap
        rng = np.random.default_rng(seed)
        n = min(self.cfg["n_background"], len(data["X_train"]))
        background = data["X_train"][rng.choice(len(data["X_train"]), n, replace=False)]
        self.kind = "kernel"
        if type(model).__name__ in ("RandomForestClassifier", "XGBClassifier"):
            self.kind = "tree"
            self.shap = shap.TreeExplainer(model, data=background,
                                           feature_perturbation="interventional",
                                           model_output="probability")
        else:
            self.shap = shap.KernelExplainer(model.predict_proba, background)

    def explain(self, x, seed):
        if self.kind == "tree":
            values = self.shap.shap_values(x.reshape(1, -1), check_additivity=False)
        else:
            values = self.shap.shap_values(x.reshape(1, -1), silent=True)
        if isinstance(values, list):
            values = values[1] if len(values) > 1 else values[0]
        values = np.asarray(values, dtype=float)
        if values.ndim == 3:
            values = values[:, :, 1] if values.shape[2] > 1 else values[:, :, 0]
        return values.reshape(-1), {"shap_kind": self.kind}


class Anchors(Explainer):
    """The reference implementation of Anchors (package anchor-exp)."""

    name = "anchors"

    def __init__(self, model, data, seed, cfg):
        super().__init__(model, data, seed, cfg)
        from anchor import anchor_tabular
        categorical = {int(j): ["0", "1"] for j in np.flatnonzero(~data["is_numeric"])}
        np.random.seed(seed)
        self.anchor = anchor_tabular.AnchorTabularExplainer(
            ["0", "1"], data["names"], data["X_train"], categorical_names=categorical)

    def explain(self, x, seed):
        exp = self.anchor.explain_instance(x, self.model.predict, threshold=self.cfg["threshold"])
        w = np.zeros(self.d)
        w[[int(j) for j in exp.features()]] = 1.0
        return w, {"anchors_precision": float(exp.precision()),
                   "anchors_coverage": float(exp.coverage())}


class Dice(Explainer):
    name = "dice"

    def __init__(self, model, data, seed, cfg):
        super().__init__(model, data, seed, cfg)
        import dice_ml
        frame = pd.DataFrame(data["X_train"], columns=data["names"])
        frame[TARGET] = data["y_train"]
        d = dice_ml.Data(dataframe=frame, continuous_features=list(data["names"]),
                         outcome_name=TARGET)
        m = dice_ml.Model(model=model, backend="sklearn", model_type="classifier")
        self.dice = dice_ml.Dice(d, m, method=self.cfg["method"])

    def explain(self, x, seed):
        query = pd.DataFrame(x.reshape(1, -1), columns=self.data["names"])
        try:
            result = self.dice.generate_counterfactuals(
                query, total_CFs=self.cfg["total_cfs"], desired_class="opposite",
                random_seed=seed, verbose=False)
            cfs = result.cf_examples_list[0].final_cfs_df
        except Exception as exc:  # DiCE raises when it finds no counterfactual
            raise Failure(f"dice: {type(exc).__name__}") from exc
        if cfs is None or len(cfs) == 0:
            raise Failure("dice: no counterfactual")
        cf = cfs[self.data["names"]].iloc[0].to_numpy(dtype=float)
        w = np.abs(cf - x)
        w[w < 1e-6] = 0.0
        valid = int(self.model.predict(cf.reshape(1, -1))[0] != self.model.predict(x.reshape(1, -1))[0])
        return w, {"dice_valid": valid, "dice_l1": float(w.sum())}


EXPLAINER_CLASSES = {c.name: c for c in (Lime, Shap, Anchors, Dice)}


def make_explainer(name: str, model, data: dict, seed: int, cfg: dict) -> Explainer:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return EXPLAINER_CLASSES[name](model, data, seed, cfg)


# --- measures ------------------------------------------------------------------

def top_set(w: np.ndarray, k: int, tol: float) -> frozenset[int]:
    """The k features with the largest absolute attribution, among those used."""
    used = np.flatnonzero(np.abs(w) > tol)
    order = sorted(used, key=lambda j: (-abs(w[j]), j))
    return frozenset(int(j) for j in order[:k])


def jaccard(a: frozenset, b: frozenset) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def baseline(data: dict) -> np.ndarray:
    """Masking values: training mean of numeric columns, training mode of one-hot columns."""
    mean = data["X_train"].mean(axis=0)
    return np.where(data["is_numeric"], mean, np.round(mean))


def faithfulness(w: np.ndarray, x: np.ndarray, model, base: np.ndarray, cfg: dict) -> dict:
    """Gap: probability change when the top features are masked. Corr: the EXP2 'fidelity'."""
    m = cfg["measures"]
    d = len(x)
    k = max(1, math.ceil(m["mask_fraction"] * d))
    top = sorted(top_set(w, k, m["zero_tolerance"]))
    batch = np.tile(x, (d + 2, 1))
    batch[1, top] = base[top]
    rows = np.arange(d)
    batch[rows + 2, rows] = base
    p = model.predict_proba(batch)[:, 1]
    drops, size = np.abs(p[0] - p[2:]), np.abs(w)
    corr = 0.0
    if drops.std() > 1e-9 and size.std() > 1e-9:
        corr = float(np.corrcoef(size, drops)[0, 1])
    return {"gap": float(abs(p[0] - p[1])), "faith_corr": corr, "p1": float(p[0])}


def evaluate(explainer: Explainer, x: np.ndarray, instance: int, base: np.ndarray,
             cfg: dict) -> dict:
    """All measures of one explainer on one instance. Never raises for an explainer failure."""
    m = cfg["measures"]
    seed = explainer.seed * 100003 + int(instance)
    out: dict = {"failed": 0, "fail_reason": ""}
    started = time.perf_counter()
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            np.random.seed(seed % (2**32))
            t0 = time.perf_counter()
            w, extra = explainer.explain(x, seed % (2**31))
            out["cost_ms"] = 1000 * (time.perf_counter() - t0)
    except (MemoryError, OSError):
        raise  # the machine, not the method: the job stops and the launcher runs it again
    except Exception as exc:
        out.update(failed=1, fail_reason=f"{type(exc).__name__}: {exc}"[:200],
                   total_s=time.perf_counter() - started)
        return out
    tol = m["zero_tolerance"]
    used = int((np.abs(w) > tol).sum())
    out.update(extra, n_used=used, sparsity=1 - used / len(w))
    out.update(faithfulness(w, x, explainer.model, base, cfg))
    top = top_set(w, m["top_k"], tol)
    out["top"] = sorted(top)
    # The perturbed copies depend on the instance only, so the four explainers see the same ones.
    rng = np.random.default_rng([20261005, int(instance)])
    numeric = explainer.data["is_numeric"]
    scores, failed_copies = [], 0
    for c in range(m["stability_copies"]):
        xp = x.copy()
        xp[numeric] += rng.normal(0, m["stability_noise_sd"], int(numeric.sum()))
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                np.random.seed((seed + c + 1) % (2**32))
                wp, _ = explainer.explain(xp, (seed + c + 1) % (2**31))
            scores.append(jaccard(top, top_set(wp, m["top_k"], tol)))
        except (MemoryError, OSError):
            raise
        except Exception:
            failed_copies += 1
            scores.append(0.0)
    out.update(stability=float(np.mean(scores)), stab_failed_copies=failed_copies,
               total_s=time.perf_counter() - started)
    return out


# --- one condition -------------------------------------------------------------

def prepare(key: str, model_name: str, seed: int, cfg: dict) -> dict:
    """Data, fitted model and chosen instances of one dataset, model and seed."""
    X, y, _ = load_frame(dataset_entry(key, cfg))
    data = split(X, y, seed, cfg)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = make_model(model_name, seed, cfg).fit(data["X_train"], data["y_train"])
    pred = model.predict(data["X_test"]).astype(int)
    data.update(model=model, pred=pred, base=baseline(data),
                instances=pick_instances(pred, cfg["n_instances"], seed))
    return data
