#!/usr/bin/env python3
"""Paper F: download the candidate datasets, profile them and apply the inclusion rule.

Plan sections 2.1 and 2.2. No explanation is computed here.

    python scripts/paper_f_datasets.py            # download, profile, gate, select

Outputs (outputs/analysis/paper_f/):
    candidates.csv   every candidate with its profile, each rule and the reason it failed
    datasets.csv     the datasets of the study, in the order of the plan
"""
from __future__ import annotations

import csv
import json
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_f_lib as lib  # noqa: E402

PUBLIC = {"public", "cc0", "cc by", "cc-by", "cc by 4.0", "publicly available", "public domain"}


def profile(X: pd.DataFrame, y: pd.Series) -> dict:
    numeric, categorical = lib.feature_types(X)
    levels = [X[c].nunique(dropna=True) for c in categorical]
    corr = float("nan")
    if len(numeric) > 1:
        c = X[numeric].astype(float).corr().abs().to_numpy()
        corr = float(np.nanmean(c[np.triu_indices_from(c, k=1)]))
    return {
        "rows": len(X), "features": X.shape[1], "numeric": len(numeric),
        "categorical": len(categorical),
        "share_numeric": round(len(numeric) / X.shape[1], 3),
        "categories_median": float(np.median(levels)) if levels else 0.0,
        "categories_max": int(max(levels)) if levels else 0,
        "minority_share": round(float(y.mean()), 4),
        "missing_share": round(float(X.isna().to_numpy().mean()), 4),
        "mean_abs_corr": round(corr, 3),
    }


def composition(p: dict) -> str:
    if p["categorical"] == 0:
        return "numeric"
    if p["share_numeric"] < 0.2:
        return "categorical"
    return "mixed"


def cv_auc(X: pd.DataFrame, y: pd.Series, model: str, cfg: dict) -> float:
    """Cross-validated AUC of one model on the training part of the gate seed."""
    rule = cfg["rule"]
    data = lib.split(X, y, rule["gate_seed"], cfg)
    A, t = data["X_train"], data["y_train"]
    scores = []
    folds = StratifiedKFold(rule["cv_folds"], shuffle=True, random_state=rule["gate_seed"])
    for tr, va in folds.split(A, t):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            m = lib.make_model(model, rule["gate_seed"], cfg).fit(A[tr], t[tr])
        scores.append(roc_auc_score(t[va], m.predict_proba(A[va])[:, 1]))
    return float(np.mean(scores))


def assess(entry: dict, cfg: dict, gate: bool = True) -> dict:
    """Rules 1 to 3 from the source record and the data; rule 4 (AUC gate) when `gate`."""
    rule = cfg["rule"]
    row = {"key": entry["key"], "openml_id": entry["id"],
           "source": entry.get("source", "pool"), "stratum_plan": entry.get("stratum", "")}
    try:
        lib.fetch(entry)
    except Exception as exc:
        # A download that fails is not a rule that fails: stop, so that it is run again.
        raise SystemExit(f"{entry['key']}: download failed ({exc}); run the script again")
    try:
        X, y, meta = lib.load_frame(entry)
    except ValueError as exc:
        row.update(passes=0, reason=f"rule 2: {exc}"[:160])
        return row
    p = profile(X, y)
    size = "large" if p["rows"] >= rule["size_cut"] else "small"
    row.update(name=meta["name"], version=meta["version"], licence=meta["licence"],
               target=meta["target"], positive_class=meta["positive_class"], **p,
               stratum=f"{composition(p)}-{size}")
    reasons = []
    if meta["licence"].strip().lower() not in PUBLIC:
        reasons.append(f"rule 1: licence {meta['licence']!r}")
    if p["rows"] < rule["min_rows"]:
        reasons.append(f"rule 3: {p['rows']} rows")
    if not rule["min_features"] <= p["features"] <= rule["max_features"]:
        reasons.append(f"rule 3: {p['features']} features")
    row.update(passes=int(not reasons), reason="; ".join(reasons))
    return apply_gate(row, entry, cfg) if gate and not reasons else row


def apply_gate(row: dict, entry: dict, cfg: dict) -> dict:
    """Rule 4: cross-validated AUC inside the range for enough models."""
    rule = cfg["rule"]
    X, y, _ = lib.load_frame(entry)
    aucs = Parallel(n_jobs=4)(delayed(cv_auc)(X, y, m, cfg) for m in lib.MODELS)
    inside = 0
    for m, a in zip(lib.MODELS, aucs):
        row[f"auc_{m}"] = round(a, 4)
        inside += rule["auc_low"] <= a <= rule["auc_high"]
    row["models_in_range"] = inside
    if inside < rule["min_models_in_range"]:
        row.update(passes=0, reason=f"rule 4: {inside} of 4 models with AUC in "
                                    f"[{rule['auc_low']}, {rule['auc_high']}]")
    return row


def cc18_entries(known: set[int]) -> list[dict]:
    """The datasets of the OpenML-CC18 suite (study 99) not already in the pool, by identifier."""
    path = lib.DATA_DIR / "study_99.json"
    if not path.exists():
        lib._curl("https://www.openml.org/api/v1/json/study/99", path)
    ids = sorted(int(i) for i in json.loads(path.read_text(encoding="utf-8"))
                 ["study"]["data"]["data_id"])
    return [{"key": f"cc18_{i}", "id": i, "source": "OpenML-CC18"} for i in ids if i not in known]


def record_check(entry: dict, cfg: dict) -> dict | None:
    """Rules 2 and 3 from the OpenML record alone, so that unsuitable data are not downloaded."""
    rule = cfg["rule"]
    path = lib.DATA_DIR / f"{entry['id']}.qualities.json"
    if not path.exists():
        lib._curl(f"https://www.openml.org/api/v1/json/data/qualities/{entry['id']}", path)
    q = {i["name"]: i.get("value") for i in
         json.loads(path.read_text(encoding="utf-8"))["data_qualities"]["quality"]}
    classes, rows_, feats = (int(float(q[k])) for k in
                             ("NumberOfClasses", "NumberOfInstances", "NumberOfFeatures"))
    reasons = []
    if classes != 2:
        reasons.append(f"rule 2: {classes} classes")
    if rows_ < rule["min_rows"]:
        reasons.append(f"rule 3: {rows_} rows")
    if not rule["min_features"] <= feats - 1 <= rule["max_features"]:
        reasons.append(f"rule 3: {feats - 1} features")
    if not reasons:
        return None
    return {"key": entry["key"], "openml_id": entry["id"], "source": entry["source"],
            "rows": rows_, "features": feats - 1, "passes": 0,
            "reason": "; ".join(reasons) + " (OpenML record)"}


def widen(rows: list[dict], cfg: dict) -> None:
    """Plan 2.1: add CC18 datasets, fewest-filled stratum first, lowest identifier first."""
    target = cfg["target_datasets"]
    extra = []
    for entry in cc18_entries({int(r["openml_id"]) for r in rows}):
        early = record_check(entry, cfg)
        row = early or assess(entry, cfg, gate=False)
        if "name" in row:
            row["key"] = re.sub(r"[^a-z0-9]+", "_", row["name"].lower()).strip("_")
        rows.append(row)
        extra.append((entry, row))
        print(f"cc18 {entry['id']:6d} {row.get('name', ''):28s} "
              f"{row.get('stratum', ''):18s} {row['reason']}", flush=True)
    strata = sorted({r["stratum"] for r in rows if r.get("stratum")})
    waiting = [(e, r) for e, r in extra if r["passes"]]
    for _, r in waiting:
        r.update(passes=0, reason="not needed: the study was complete before its turn")
    while sum(r["passes"] for r in rows) < target and waiting:
        filled = {s: sum(r["passes"] for r in rows if r.get("stratum") == s) for s in strata}
        open_strata = {r["stratum"] for _, r in waiting}
        stratum = min(open_strata, key=lambda s: (filled[s], s))
        entry, row = next((e, r) for e, r in waiting if r["stratum"] == stratum)
        waiting.remove((entry, row))
        row.update(passes=1, reason="")
        apply_gate(row, entry, cfg)
        print(f"gate {row['key']:28s} {'PASS' if row['passes'] else 'FAIL'}  "
              + "  ".join(f"{m}={row.get('auc_' + m, '')}" for m in lib.MODELS), flush=True)


def select(rows: list[dict], target: int) -> list[dict]:
    """Passing candidates in plan order; if too many, drop the last of the fullest strata."""
    chosen = [r for r in rows if r["passes"]]
    while len(chosen) > target:
        sizes: dict[str, int] = {}
        for r in chosen:
            sizes[r["stratum"]] = sizes.get(r["stratum"], 0) + 1
        fullest = max(sizes, key=lambda s: (sizes[s], s))
        last = [r for r in chosen if r["stratum"] == fullest and r["key"] != "adult"][-1]
        last["reason"] = f"passes, dropped: stratum {fullest} is the fullest"
        last["passes"] = 0
        chosen.remove(last)
    return chosen


def write(path: Path, rows: list[dict]) -> None:
    fields: list[str] = []
    for r in rows:
        fields += [k for k in r if k not in fields]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    cfg = lib.config()
    rows = []
    for entry in cfg["dataset"]:
        row = assess(entry, cfg)
        rows.append(row)
        print(f"{row['key']:18s} {'PASS' if row['passes'] else 'FAIL'}  "
              f"{row.get('rows', '')} x {row.get('features', '')}  {row.get('stratum', '')}  "
              + "  ".join(f"{m}={row.get('auc_' + m, '')}" for m in lib.MODELS)
              + f"  {row['reason']}", flush=True)
    if sum(r["passes"] for r in rows) < cfg["target_datasets"]:
        print("\nfewer than the target pass: widening with the OpenML-CC18 suite", flush=True)
        widen(rows, cfg)
    chosen = select(rows, cfg["target_datasets"])
    write(lib.OUT / "candidates.csv", rows)
    write(lib.OUT / "datasets.csv", chosen)
    print(f"\n{len(chosen)} datasets selected of {len(rows)} candidates "
          f"(target {cfg['target_datasets']}, floor {cfg['min_datasets']})")
    return 0 if len(chosen) >= cfg["min_datasets"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
