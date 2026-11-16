#!/usr/bin/env python3
"""Paper G: the dataset eligibility gate, run retrospectively as a diagnostic (plan 11.1).

    python scripts/paper_g_dataset_gate.py      writes outputs/analysis/paper_g/diagnostics/dataset_gate.csv

The plan (section 2.1) asked for this gate before any explanation was computed; it was not run
then. It is run now with the procedure of the Paper F gate (scripts/paper_f_datasets.py, cv_auc)
and the values of config.toml [rule]. It computes model AUCs only and reads no run output.
Whatever it finds, all eight datasets stay in the study (Decision A); a failing dataset is
recorded and reported, never removed or replaced here.
"""
from __future__ import annotations

import csv
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from joblib import Parallel, delayed
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_g_lib as lib  # noqa: E402

OUT = lib.OUT / "diagnostics" / "dataset_gate.csv"


def cv_auc(key: str, model: str, cfg: dict) -> float:
    """Mean 5-fold AUC of one model on the training part of the gate seed (Paper F procedure)."""
    rule = cfg["rule"]
    X, y, _ = lib.load_frame(lib.dataset_entry(key, cfg))
    data = lib.split(X, y, rule["gate_seed"], cfg)
    A, t = data["X_train"], data["y_train"]
    folds = StratifiedKFold(rule["cv_folds"], shuffle=True, random_state=rule["gate_seed"])
    scores = []
    for tr, va in folds.split(A, t):
        m = lib.fit(lib.make_model(model, rule["gate_seed"], cfg), A[tr], t[tr])
        scores.append(roc_auc_score(t[va], m.predict_proba(A[va])[:, 1]))
    return float(np.mean(scores))


def in_range(auc: float, rule: dict) -> bool:
    return rule["auc_low"] <= auc <= rule["auc_high"]


def gate_row(key: str, aucs: dict[str, float], rule: dict) -> dict:
    inside = sum(in_range(a, rule) for a in aucs.values())
    passes = inside >= rule["min_models_in_range"]
    return {"dataset": key, **{f"cv_auc_{m}": round(a, 4) for m, a in aucs.items()},
            "models_in_range": inside, "models": len(aucs),
            "passes": int(passes), "retained": 1,
            "note": "" if passes else (f"deviation: {inside} of {len(aucs)} models in "
                                       f"[{rule['auc_low']}, {rule['auc_high']}]; retained (Decision A)")}


def main() -> int:
    cfg = lib.config()
    rule = cfg["rule"]
    keys = [d["key"] for d in cfg["dataset"]]
    for k in keys:
        lib.fetch(lib.dataset_entry(k, cfg))
    jobs = [(k, m) for k in keys for m in lib.MODELS]
    aucs = Parallel(n_jobs=4)(delayed(cv_auc)(k, m, cfg) for k, m in jobs)
    by = {k: {} for k in keys}
    for (k, m), a in zip(jobs, aucs):
        by[k][m] = a
    commit = subprocess.run(["git", "rev-parse", "--short=12", "HEAD"], cwd=lib.ROOT,
                            capture_output=True, text=True).stdout.strip()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows = [{**gate_row(k, by[k], rule), "gate": "retrospective diagnostic (plan 11.1)",
             "procedure": f"Paper F cv_auc; split seed {rule['gate_seed']}; StratifiedKFold("
                          f"{rule['cv_folds']}, shuffle, {rule['gate_seed']}); mean fold AUC; inclusive",
             "commit": commit, "run_at": stamp} for k in keys]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"{r['dataset']:16} {'PASS' if r['passes'] else 'FAIL'}  in range {r['models_in_range']}/4  "
              + "  ".join(f"{m}={r['cv_auc_' + m]}" for m in lib.MODELS))
    print(f"{sum(r['passes'] for r in rows)} of {len(rows)} pass; all {len(rows)} retained -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
