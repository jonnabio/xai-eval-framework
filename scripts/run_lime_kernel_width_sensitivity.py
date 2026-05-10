#!/usr/bin/env python3
"""
LIME kernel_width sensitivity probe.

Tests LIME with kernel_width in {0.25, 0.75, 3.0, 10.0} on the RF model,
seed 42, N=100 instances (50 per class).  Results are written to
outputs/analysis/lime_kernel_width_sensitivity.csv.

Reference condition: kernel_width=3.0 (project default).
Metrics mirror Appendix C of the thesis: fidelity (faithfulness_score),
stability (cosine_similarity_mean), cost (ms/instance), sparsity.
"""

from __future__ import annotations

import sys
import time
import logging
import warnings
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

from src.data_loading.adult import load_adult
from src.xai.lime_tabular import LIMETabularWrapper

# ── Constants matching the reference protocol ────────────────────────────────
MODEL_PATH      = PROJECT_ROOT / "experiments/exp1_adult/models/rf.joblib"
PREPROCESSOR    = PROJECT_ROOT / "experiments/exp1_adult/models/preprocessor.joblib"
OUTPUT_PATH     = PROJECT_ROOT / "outputs/analysis/lime_kernel_width_sensitivity.csv"
SEED            = 42
N_PER_CLASS     = 50          # 100 instances total
KERNEL_WIDTHS   = [0.25, 0.75, 3.0, 10.0]
NUM_FEATURES    = 10
NUM_SAMPLES     = 1000
T_STABILITY     = 15          # perturbation replicates
SIGMA_STABILITY = 0.1         # perturbation noise
TOP_K_FIDELITY  = 5           # top-k masking for faithfulness


def stratified_sample(X: np.ndarray, y: np.ndarray, n_per_class: int, seed: int) -> np.ndarray:
    rng = np.random.RandomState(seed)
    idx_list = []
    for cls in np.unique(y):
        pool = np.where(y == cls)[0]
        chosen = rng.choice(pool, size=min(n_per_class, len(pool)), replace=False)
        idx_list.append(chosen)
    return np.concatenate(idx_list)


def compute_fidelity(model, weights: np.ndarray, instance: np.ndarray, baseline: np.ndarray) -> float:
    """Pearson corr between |weight_i| and |pred(x) - pred(x_mask_i)| across all features."""
    p_orig = model.predict_proba(instance.reshape(1, -1))[:, 1][0]
    n_feat = len(instance)
    batch = np.tile(instance, (n_feat, 1))
    for i in range(n_feat):
        batch[i, i] = baseline[i]
    p_batch = model.predict_proba(batch)[:, 1]
    drops = np.abs(p_orig - p_batch)
    mags  = np.abs(weights)
    if np.std(drops) < 1e-9 or np.std(mags) < 1e-9:
        return 0.0
    corr, _ = pearsonr(mags, drops)
    return float(corr)


def compute_stability(lime_wrapper, model, instance: np.ndarray, T: int, sigma: float) -> float:
    """Mean pairwise cosine similarity of T perturbed explanations."""
    vecs = []
    for _ in range(T):
        noise    = np.random.normal(0, sigma, size=instance.shape)
        perturbed = instance + noise
        w = lime_wrapper.explain_instance(model, perturbed, return_full=False)
        vecs.append(w)
    vecs = np.array(vecs)           # (T, n_features)
    # Mean pairwise cosine similarity
    sim_sum = 0.0
    count   = 0
    for a in range(T):
        for b in range(a + 1, T):
            va = vecs[a].reshape(1, -1)
            vb = vecs[b].reshape(1, -1)
            n_va = np.linalg.norm(va)
            n_vb = np.linalg.norm(vb)
            if n_va < 1e-10 or n_vb < 1e-10:
                sim_sum += 0.0
            else:
                sim_sum += float(cosine_similarity(va, vb)[0, 0])
            count += 1
    return sim_sum / count if count > 0 else 0.0


def compute_sparsity(weights: np.ndarray, threshold: float = 1e-4) -> float:
    active = np.sum(np.abs(weights) > threshold)
    return float(active / len(weights))


def main():
    print("Loading data and model …")
    preprocessor = joblib.load(PREPROCESSOR)
    X_train, X_test, y_train, y_test, feature_names, _ = load_adult(
        cache_dir=str(PROJECT_ROOT / "data"),
        random_state=SEED,
        preprocessor=preprocessor,
        verbose=False,
    )
    model = joblib.load(MODEL_PATH)

    # Training data as numpy for LIME background
    X_train_np = X_train if isinstance(X_train, np.ndarray) else X_train.values
    X_test_np  = X_test  if isinstance(X_test,  np.ndarray) else X_test.values
    y_test_np  = y_test  if isinstance(y_test,  np.ndarray) else y_test.values

    baseline = X_train_np.mean(axis=0)

    # Sample 100 instances (50 per class)
    idx = stratified_sample(X_test_np, y_test_np, N_PER_CLASS, SEED)
    X_eval = X_test_np[idx]
    print(f"Evaluation set: {len(X_eval)} instances")

    records = []
    for kw in KERNEL_WIDTHS:
        print(f"\nkernel_width = {kw} …")
        wrapper = LIMETabularWrapper(
            training_data=X_train_np,
            feature_names=feature_names,
            num_features=NUM_FEATURES,
            num_samples=NUM_SAMPLES,
            kernel_width=kw,
            random_state=SEED,
        )

        fidelities, stabilities, sparsities, costs_ms = [], [], [], []
        n_valid = 0  # instances with at least one non-zero weight

        for i, inst in enumerate(X_eval):
            if i % 20 == 0:
                print(f"  instance {i}/{len(X_eval)}")

            # --- explanation + cost ---
            t0 = time.perf_counter()
            w  = wrapper.explain_instance(model, inst, return_full=False)
            cost_ms = (time.perf_counter() - t0) * 1000

            active = np.sum(np.abs(w) > 1e-4)
            if active > 0:
                n_valid += 1
                fidelities.append(compute_fidelity(model, w, inst, baseline))
                stabilities.append(compute_stability(wrapper, model, inst, T_STABILITY, SIGMA_STABILITY))
            sparsities.append(compute_sparsity(w))
            costs_ms.append(cost_ms)

        records.append({
            "kernel_width":    kw,
            "n_valid":         n_valid,
            "fidelity_mean":   round(float(np.mean(fidelities))  if fidelities  else 0.0, 3),
            "stability_mean":  round(float(np.mean(stabilities)) if stabilities else 0.0, 3),
            "sparsity_mean":   round(float(np.mean(sparsities)),  3),
            "cost_ms_mean":    round(float(np.mean(costs_ms)),    1),
        })
        print(f"  valid={n_valid}/100  fidelity={records[-1]['fidelity_mean']:.3f}  "
              f"stability={records[-1]['stability_mean']:.3f}  "
              f"cost={records[-1]['cost_ms_mean']:.0f}ms")

    df = pd.DataFrame(records)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\n=== Results ===")
    print(df.to_string(index=False))
    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    np.random.seed(SEED)
    main()
