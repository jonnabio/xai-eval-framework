#!/usr/bin/env python3
"""Paper G: data, models, explainers and the seven faithfulness metrics.

Plan: docs/reports/paper_g/ANALYSIS_PLAN.md (version 2). Configuration:
experiments/exp_g/config.toml.

Data loading, the split and the model settings follow Paper F (scripts/paper_f_lib.py); they
are copied, not imported, so that this lane does not depend on another lane's files. No Paper F
result is read.

Conventions
-----------
- A *group* is one raw feature: one numeric column, or all one-hot columns of a categorical
  feature. Attributions are summed per group; masking a group sets all its columns to the
  baseline. Every metric works on groups.
- Attributions are *oriented* toward the predicted class c: explainers explain the
  probability of class 1, and for c = 0 the sign is flipped (p0 = 1 - p1 in a binary model).
  f(x) below is the probability of c.
- The baseline is the training mean of a numeric column and the one-hot vector of the
  training mode of a categorical feature.
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

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "experiments" / "exp_g" / "config.toml"
DATA_DIR = ROOT / "data" / "openml" / "paper_g"
OUT = ROOT / "outputs" / "analysis" / "paper_g"
OPENML = "https://www.openml.org/api/v1/json/data/{id}"
MODELS = ("logreg", "rf", "xgb", "mlp")
EXPLAINERS = ("shap", "lime", "occlusion", "random")
INSTANCE_METRICS = ("m1_deletion", "m2_insertion", "m3_gap", "m4_corr", "m5_infidelity",
                    "m6_sufficiency")
HIGHER_IS_BETTER = {"m1_deletion": False, "m2_insertion": True, "m3_gap": True,
                    "m4_corr": True, "m5_infidelity": False, "m6_sufficiency": False,
                    "m7_roar": True}
SEP = "\x1f"  # separates feature and category in one-hot column names


def config(path: Path = CONFIG_PATH) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def dataset_entry(key: str, cfg: dict) -> dict:
    for entry in cfg["dataset"]:
        if entry["key"] == key:
            return entry
    raise KeyError(f"dataset {key!r} is not in {CONFIG_PATH.name}")


# --- data (as Paper F) -----------------------------------------------------------

def _curl(url: str, target: Path) -> None:
    tmp = target.with_suffix(target.suffix + ".part")
    subprocess.run(["curl", "-sSL", "--fail", "--retry", "6", "--retry-all-errors",
                    "--retry-delay", "5", "--max-time", "600", "-o", str(tmp), url], check=True)
    tmp.replace(target)


def fetch(entry: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    desc_path = DATA_DIR / f"{entry['id']}.json"
    if not desc_path.exists():
        _curl(OPENML.format(id=entry["id"]), desc_path)
    desc = json.loads(desc_path.read_text(encoding="utf-8"))["data_set_description"]
    data_path = DATA_DIR / f"{entry['id']}.parquet"
    if not data_path.exists():
        _curl(desc["parquet_url"], data_path)


def description(entry: dict) -> dict:
    return json.loads((DATA_DIR / f"{entry['id']}.json").read_text(encoding="utf-8"))[
        "data_set_description"]


def _as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return [str(v) for v in value]


def load_frame(entry: dict) -> tuple[pd.DataFrame, pd.Series, dict]:
    """Raw features, binary target (1 = minority class) and the source record."""
    fetch(entry)
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
    meta = {"openml_id": int(desc["id"]), "name": desc["name"], "version": int(desc["version"]),
            "target": target, "positive_class": minority, "dropped_columns": drop}
    return df.drop(columns=[target]), y, meta


def feature_types(X: pd.DataFrame) -> tuple[list[str], list[str]]:
    numeric = [c for c in X.columns
               if pd.api.types.is_numeric_dtype(X[c]) and not pd.api.types.is_bool_dtype(X[c])]
    return numeric, [c for c in X.columns if c not in numeric]


def _combiner(feature, category):
    return f"{feature}{SEP}{category}"


def split(X: pd.DataFrame, y: pd.Series, seed: int, cfg: dict) -> dict:
    """Stratified split, preprocessing fitted on the training part, and feature groups."""
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
                                     max_categories=cfg["preprocessing"]["max_categories"],
                                     feature_name_combiner=_combiner)),
        ]), categorical))
    pre = ColumnTransformer(transformers, verbose_feature_names_out=False)
    A_tr = np.asarray(pre.fit_transform(X_tr), dtype=float)
    A_te = np.asarray(pre.transform(X_te), dtype=float)
    names = [str(n) for n in pre.get_feature_names_out()]
    groups, group_names, is_numeric = make_groups(names, numeric)
    return {"X_train": A_tr, "X_test": A_te, "y_train": y_tr.to_numpy(), "y_test": y_te.to_numpy(),
            "names": names, "groups": groups, "group_names": group_names,
            "is_numeric": is_numeric, "test_index": X_te.index.to_numpy()}


def make_groups(names: list[str], numeric: list[str]):
    """Column indices of each raw feature, in the order of first appearance."""
    order: list[str] = []
    cols: dict[str, list[int]] = {}
    for j, n in enumerate(names):
        g = n if n in numeric else n.split(SEP, 1)[0]
        if g not in cols:
            order.append(g)
            cols[g] = []
        cols[g].append(j)
    is_numeric = np.array([n in numeric for n in names])
    return [np.array(cols[g]) for g in order], order, is_numeric


def baseline(X_train: np.ndarray, groups: list[np.ndarray], is_numeric: np.ndarray) -> np.ndarray:
    """Training mean of numeric columns; one-hot of the training mode of each categorical group."""
    base = X_train.mean(axis=0)
    for g in groups:
        if not is_numeric[g[0]]:
            base[g] = 0.0
            base[g[int(np.argmax(X_train[:, g].sum(axis=0)))]] = 1.0
    return base


# --- models (as Paper F) ---------------------------------------------------------

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


def fit(model, X, y):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return model.fit(X, y)


def pick_instances(pred: np.ndarray, n: int, seed: int) -> np.ndarray:
    idx = np.arange(len(pred))
    if len(idx) <= n:
        return idx
    counts = np.bincount(pred, minlength=2)
    stratify = pred if counts.min() >= 2 else None
    chosen, _ = train_test_split(idx, train_size=n, random_state=seed, stratify=stratify)
    return np.sort(chosen)


# --- explainers --------------------------------------------------------------------
# explain(x, seed) returns attributions over encoded columns, for the probability of class 1.

class Explainer:
    name = ""

    def __init__(self, model, data: dict, seed: int, cfg: dict):
        self.model, self.data, self.seed = model, data, seed
        self.cfg = cfg["explainers"][self.name]
        self.d = data["X_train"].shape[1]

    def explain(self, x: np.ndarray, seed: int) -> np.ndarray:
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
        self.lime.random_state = np.random.RandomState(seed % (2**32))
        exp = self.lime.explain_instance(x, self.model.predict_proba, labels=(1,),
                                         num_features=self.d,
                                         num_samples=self.cfg["num_samples"])
        w = np.zeros(self.d)
        for j, value in exp.as_map()[1]:
            w[j] = value
        return w


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
        np.random.seed(seed % (2**32))
        if self.kind == "tree":
            values = self.shap.shap_values(x.reshape(1, -1), check_additivity=False)
        else:
            values = self.shap.shap_values(x.reshape(1, -1), silent=True,
                                           l1_reg=self.cfg.get("l1_reg", "auto"))
        if isinstance(values, list):
            values = values[1] if len(values) > 1 else values[0]
        values = np.asarray(values, dtype=float)
        if values.ndim == 3:
            values = values[:, :, 1] if values.shape[2] > 1 else values[:, :, 0]
        return values.reshape(-1)


class Occlusion(Explainer):
    """Attribution of a group = p1(x) - p1(x with that group set to the baseline)."""

    name = "occlusion"

    def explain(self, x, seed):
        groups, base = self.data["groups"], self.data["base"]
        batch = np.tile(x, (len(groups) + 1, 1))
        for i, g in enumerate(groups):
            batch[i + 1, g] = base[g]
        p = self.model.predict_proba(batch)[:, 1]
        w = np.zeros(self.d)
        for i, g in enumerate(groups):
            w[g[0]] = p[0] - p[i + 1]       # one value per group, on its first column
        return w


class RandomControl(Explainer):
    """Negative control: N(0, 1) score per group, seeded per instance."""

    name = "random"

    def explain(self, x, seed):
        rng = np.random.default_rng(seed)
        w = np.zeros(self.d)
        for g in self.data["groups"]:
            w[g[0]] = rng.standard_normal()
        return w


EXPLAINER_CLASSES = {c.name: c for c in (Shap, Lime, Occlusion, RandomControl)}


def make_explainer(name: str, model, data: dict, seed: int, cfg: dict) -> Explainer:
    return EXPLAINER_CLASSES[name](model, data, seed, cfg)


# --- metrics ---------------------------------------------------------------------

def group_attr(w: np.ndarray, groups: list[np.ndarray]) -> np.ndarray:
    return np.array([w[g].sum() for g in groups])


def orient(a: np.ndarray, pred_class: int) -> np.ndarray:
    return a if pred_class == 1 else -a


def order_of(a: np.ndarray) -> np.ndarray:
    """Groups by attribution toward the predicted class, largest first; ties by index."""
    return np.lexsort((np.arange(len(a)), -a))


def n_top(n_groups: int, fraction: float) -> int:
    return max(1, math.ceil(fraction * n_groups))


def _masked(x: np.ndarray, base: np.ndarray, groups, which) -> np.ndarray:
    z = x.copy()
    for i in which:
        z[groups[i]] = base[groups[i]]
    return z


def _auc(p: np.ndarray) -> float:
    """Area under a curve sampled at 0, 1/G, ..., 1."""
    return float(np.trapezoid(p, dx=1.0 / (len(p) - 1)))


def removal_metrics(a: np.ndarray, x: np.ndarray, prob, base: np.ndarray, groups,
                    fraction: float) -> dict:
    """M1, M2, M3 and M6 for oriented group attributions `a`. prob(batch) -> f of each row."""
    G = len(groups)
    order = order_of(a)
    k = n_top(G, fraction)
    rows = [x]
    for t in range(1, G + 1):                         # deletion: mask the first t
        rows.append(_masked(x, base, groups, order[:t]))
    for t in range(G + 1):                            # insertion: restore the first t
        rows.append(_masked(x, base, groups, order[t:]))
    rows.append(_masked(x, base, groups, order[k:]))  # sufficiency: keep the top k only
    p = prob(np.vstack(rows))
    deletion = p[: G + 1]
    insertion = p[G + 1: 2 * G + 2]
    return {"m1_deletion": _auc(deletion), "m2_insertion": _auc(insertion),
            "m3_gap": float(p[0] - deletion[k]), "m6_sufficiency": float(p[0] - p[-1])}


def correlation_metric(a, x, prob, base, groups) -> tuple[float, bool]:
    """M4: Pearson correlation of a with the drop of f when each group alone is masked."""
    rows = [x] + [_masked(x, base, groups, [i]) for i in range(len(groups))]
    p = prob(np.vstack(rows))
    drops = p[0] - p[1:]
    if drops.std() < 1e-12 or a.std() < 1e-12:
        return 0.0, True
    return float(np.corrcoef(a, drops)[0, 1]), False


def infidelity_metric(a, x, prob, base, groups, draws: int, keep_prob: float,
                      rng: np.random.Generator) -> float:
    """M5: 1 - R^2 of f(x) - f(x masked on S) on sum_{i in S} a_i, no intercept, over draws of S."""
    G = len(groups)
    masks = rng.random((draws, G)) < keep_prob
    masks[masks.sum(axis=1) == 0, rng.integers(0, G)] = True
    rows = [x] + [_masked(x, base, groups, np.flatnonzero(m)) for m in masks]
    p = prob(np.vstack(rows))
    dy = p[0] - p[1:]
    s = masks.astype(float) @ a
    ss = float(dy @ dy)
    if ss < 1e-18:
        return 0.0
    if float(s @ s) < 1e-18:
        return 1.0
    beta = float(s @ dy) / float(s @ s)
    return float(((dy - beta * s) ** 2).sum() / ss)


def class_prob(model, pred_class: int):
    def prob(batch):
        return model.predict_proba(batch)[:, pred_class]
    return prob


def instance_metrics(a: np.ndarray, x: np.ndarray, model, pred_class: int, base: np.ndarray,
                     base2: np.ndarray, groups, cfg: dict, rng: np.random.Generator) -> dict:
    m = cfg["metrics"]
    prob = class_prob(model, pred_class)
    out = removal_metrics(a, x, prob, base, groups, m["mask_fraction"])
    out["m4_corr"], out["m4_degenerate"] = correlation_metric(a, x, prob, base, groups)
    out["m5_infidelity"] = infidelity_metric(a, x, prob, base, groups, m["infidelity_draws"],
                                             m["infidelity_keep_prob"], rng)
    second = removal_metrics(a, x, prob, base2, groups, m["mask_fraction"])
    out.update({f"{k}_b2": v for k, v in second.items()})
    out["f_x"] = float(prob(x.reshape(1, -1))[0])
    return out


def roar_score(global_rank: np.ndarray, data: dict, model_name: str, seed: int, cfg: dict,
               auc_full: float) -> dict:
    """M7: mean drop of test AUC after retraining without the top share of groups."""
    groups, base = data["groups"], data["base"]
    G = len(groups)
    drops = {}
    for level in cfg["metrics"]["roar_levels"]:
        k = n_top(G, level)
        cols = np.concatenate([groups[i] for i in global_rank[:k]])
        Xtr, Xte = data["X_train"].copy(), data["X_test"].copy()
        Xtr[:, cols] = base[cols]
        Xte[:, cols] = base[cols]
        model = fit(make_model(model_name, seed, cfg), Xtr, data["y_train"])
        auc = roc_auc_score(data["y_test"], model.predict_proba(Xte)[:, 1])
        drops[f"roar_drop_{level}"] = float(auc_full - auc)
    drops["m7_roar"] = float(np.mean(list(drops.values())))
    return drops


# --- one condition ------------------------------------------------------------------

def prepare(key: str, model_name: str, seed: int, cfg: dict) -> dict:
    X, y, meta = load_frame(dataset_entry(key, cfg))
    data = split(X, y, seed, cfg)
    model = fit(make_model(model_name, seed, cfg), data["X_train"], data["y_train"])
    pred = model.predict(data["X_test"]).astype(int)
    data.update(model=model, pred=pred, meta=meta,
                base=baseline(data["X_train"], data["groups"], data["is_numeric"]),
                instances=pick_instances(pred, cfg["n_instances"], seed),
                auc=float(roc_auc_score(data["y_test"], model.predict_proba(data["X_test"])[:, 1])))
    return data


def explain_and_score(data: dict, explainer_names, seed: int, cfg: dict, n_instances=None):
    """Yield one row per instance and explainer. An explainer error is a failed row."""
    model = data["model"]
    explainers = {n: make_explainer(n, model, data, seed, cfg) for n in explainer_names}
    instances = data["instances"] if n_instances is None else data["instances"][:n_instances]
    for pos in instances:
        x = data["X_test"][pos]
        c = int(data["pred"][pos])
        inst_seed = (seed * 100003 + int(pos)) % (2**31)
        rng_b2 = np.random.default_rng([seed, int(pos), 2])
        base2 = data["X_train"][rng_b2.integers(0, len(data["X_train"]))]
        for name, ex in explainers.items():
            row = {"instance": int(pos), "explainer": name, "pred_class": c, "failed": 0,
                   "fail_reason": ""}
            t0 = time.perf_counter()
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    w = ex.explain(x, inst_seed)
                row["explain_s"] = time.perf_counter() - t0
                a = orient(group_attr(w, data["groups"]), c)
                rng = np.random.default_rng([seed, int(pos), 5])   # same subsets for every explainer
                row.update(instance_metrics(a, x, model, c, data["base"], base2, data["groups"],
                                            cfg, rng))
                row["attr"] = [round(float(v), 8) for v in a]
            except (MemoryError, OSError):
                raise
            except Exception as exc:  # the explainer, not the machine
                row.update(failed=1, fail_reason=f"{type(exc).__name__}: {exc}"[:200])
            row["total_s"] = time.perf_counter() - t0
            yield row


def set_threads(n: int) -> None:
    for var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        os.environ[var] = str(n)
