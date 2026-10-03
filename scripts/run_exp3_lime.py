#!/usr/bin/env python3
"""
EXP3 LIME cross-dataset extension.

Runs LIME on Breast Cancer and German Credit datasets under the same
protocol as the existing EXP3 SHAP/Anchors runs, enabling direct
SHAP-LIME comparison across all three datasets.

Conditions: 2 datasets × 2 models (RF, XGB) × 3 seeds = 12 experiments
N = 100 instances per experiment (50 per class).
Metrics: fidelity, stability, sparsity, cost (same as thesis Appendix C).

Results saved to: outputs/analysis/exp3_lime_results.csv
"""

from __future__ import annotations

import sys
import time
import warnings
import logging
from itertools import product
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARNING)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loading.cross_dataset import load_tabular_dataset
from src.xai.lime_tabular import LIMETabularWrapper

# ── Constants ────────────────────────────────────────────────────────────────
MODEL_ROOT  = PROJECT_ROOT / "experiments/exp3_cross_dataset/models"
OUTPUT_PATH = PROJECT_ROOT / "outputs/analysis/exp3_lime_results.csv"

DATASETS  = ["breast_cancer", "german_credit"]
MODELS    = ["rf", "xgb"]
SEEDS     = [42, 123, 456]

NUM_FEATURES  = 10
NUM_SAMPLES   = 1000
KERNEL_WIDTH  = 3.0
N_PER_CLASS   = 50      # 100 instances total
T_STABILITY   = 15
SIGMA         = 0.1
TOP_K         = 5


# ── Metric helpers ────────────────────────────────────────────────────────────

def stratified_sample(X, y, n, seed):
    rng = np.random.RandomState(seed)
    idx = []
    for cls in np.unique(y):
        pool = np.where(y == cls)[0]
        idx.append(rng.choice(pool, size=min(n, len(pool)), replace=False))
    return np.concatenate(idx)


def fidelity(model, w, inst, baseline):
    p0 = model.predict_proba(inst.reshape(1, -1))[:, 1][0]
    n = len(inst)
    batch = np.tile(inst, (n, 1))
    for i in range(n):
        batch[i, i] = baseline[i]
    drops = np.abs(p0 - model.predict_proba(batch)[:, 1])
    mags  = np.abs(w)
    if np.std(drops) < 1e-9 or np.std(mags) < 1e-9:
        return 0.0
    return float(pearsonr(mags, drops)[0])


def stability(wrapper, model, inst, T, sigma):
    vecs = []
    for _ in range(T):
        noise = np.random.normal(0, sigma, size=inst.shape)
        w = wrapper.explain_instance(model, inst + noise, return_full=False)
        vecs.append(w)
    vecs = np.array(vecs)
    sims = []
    for a in range(T):
        for b in range(a + 1, T):
            na, nb = np.linalg.norm(vecs[a]), np.linalg.norm(vecs[b])
            if na > 1e-10 and nb > 1e-10:
                sims.append(float(cosine_similarity(
                    vecs[a].reshape(1, -1), vecs[b].reshape(1, -1))[0, 0]))
            else:
                sims.append(0.0)
    return float(np.mean(sims)) if sims else 0.0


def sparsity(w, thr=1e-4):
    return float(np.sum(np.abs(w) > thr) / len(w))


# ── Main ──────────────────────────────────────────────────────────────────────

def run_one(dataset, model_name, seed):
    model_dir  = MODEL_ROOT / dataset / model_name / f"seed_{seed}"
    model_path = model_dir / f"{model_name}.joblib"
    prep_path  = model_dir / "preprocessor.joblib"

    preprocessor = joblib.load(prep_path)
    X_tr, X_te, y_tr, y_te, feature_names, _ = load_tabular_dataset(
        dataset,
        cache_dir=str(PROJECT_ROOT / "data"),
        random_state=seed,
        preprocessor=preprocessor,
    )
    model = joblib.load(model_path)

    X_tr_np = X_tr if isinstance(X_tr, np.ndarray) else X_tr.values
    X_te_np = X_te if isinstance(X_te, np.ndarray) else X_te.values
    y_te_np = y_te if isinstance(y_te, np.ndarray) else y_te.values
    baseline = X_tr_np.mean(axis=0)

    idx    = stratified_sample(X_te_np, y_te_np, N_PER_CLASS, seed)
    X_eval = X_te_np[idx]

    wrapper = LIMETabularWrapper(
        training_data=X_tr_np,
        feature_names=feature_names,
        num_features=NUM_FEATURES,
        num_samples=NUM_SAMPLES,
        kernel_width=KERNEL_WIDTH,
        random_state=seed,
    )

    fids, stabs, spars, costs = [], [], [], []
    n_valid = 0

    for inst in X_eval:
        t0 = time.perf_counter()
        w  = wrapper.explain_instance(model, inst, return_full=False)
        costs.append((time.perf_counter() - t0) * 1000)

        if np.sum(np.abs(w) > 1e-4) > 0:
            n_valid += 1
            fids.append(fidelity(model, w, inst, baseline))
            stabs.append(stability(wrapper, model, inst, T_STABILITY, SIGMA))
        spars.append(sparsity(w))

    return {
        "dataset":        dataset,
        "model":          model_name,
        "seed":           seed,
        "n_valid":        n_valid,
        "fidelity_mean":  round(float(np.mean(fids))  if fids  else 0.0, 3),
        "stability_mean": round(float(np.mean(stabs)) if stabs else 0.0, 3),
        "sparsity_mean":  round(float(np.mean(spars)), 3),
        "cost_ms_mean":   round(float(np.mean(costs)), 1),
    }


def main():
    np.random.seed(42)
    records = []
    total = len(DATASETS) * len(MODELS) * len(SEEDS)
    done  = 0

    for dataset, model_name, seed in product(DATASETS, MODELS, SEEDS):
        done += 1
        print(f"[{done}/{total}] {dataset}  {model_name}  seed={seed} ...", end=" ", flush=True)
        rec = run_one(dataset, model_name, seed)
        records.append(rec)
        print(f"fidelity={rec['fidelity_mean']:.3f}  "
              f"stability={rec['stability_mean']:.3f}  "
              f"valid={rec['n_valid']}/100")

    df = pd.DataFrame(records)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\n=== Summary by dataset+model (mean over seeds) ===")
    summary = df.groupby(["dataset", "model"])[
        ["fidelity_mean", "stability_mean", "sparsity_mean", "cost_ms_mean"]
    ].mean().round(3)
    print(summary.to_string())
    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
