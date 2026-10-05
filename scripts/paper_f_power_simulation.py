#!/usr/bin/env python3
"""Paper F: how many datasets does the ranking analysis need?

No data are read. For n = 4 explainers ranked in each of k datasets, the script
simulates Kendall's W and the mean pairwise Spearman correlation between
datasets, rho_bar = (k W - 1) / (k - 1), under a latent-score model:

    score[d, j] = s * mu[j] + e[d, j],   e ~ N(0, 1),   mu = (-1.5, -0.5, 0.5, 1.5)

The signal s is set so that the population rho_bar takes a target value. For
each k the script reports the critical W at alpha = 0.05 under random rankings,
the power to reject random rankings, and the central 95% range of the estimate.

Output: outputs/analysis/paper_f/power_simulation.csv
Run:    python scripts/paper_f_power_simulation.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

N_EXPLAINERS = 4
K_VALUES = (4, 6, 8, 10, 12, 16, 20)
TARGET_RHO = (0.0, 0.2, 0.5, 0.8)
MU = np.array([-1.5, -0.5, 0.5, 1.5])
N_SIM = 20000
SEED = 20261005
OUT = Path(__file__).resolve().parents[1] / "outputs" / "analysis" / "paper_f" / "power_simulation.csv"


def ranks(scores: np.ndarray) -> np.ndarray:
    """Ranks 1..n along the last axis (continuous scores, so no ties)."""
    return scores.argsort(axis=-1).argsort(axis=-1) + 1.0


def kendall_w(r: np.ndarray) -> np.ndarray:
    """Kendall's W for arrays of shape (..., k, n)."""
    k, n = r.shape[-2], r.shape[-1]
    col = r.sum(axis=-2)
    s = ((col - k * (n + 1) / 2) ** 2).sum(axis=-1)
    return 12 * s / (k**2 * (n**3 - n))


def rho_bar(w: np.ndarray, k: int) -> np.ndarray:
    return (k * w - 1) / (k - 1)


def simulate(rng: np.random.Generator, k: int, s: float, n_sim: int = N_SIM) -> np.ndarray:
    scores = s * MU + rng.standard_normal((n_sim, k, N_EXPLAINERS))
    return kendall_w(ranks(scores))


def signal_for(rng: np.random.Generator, target: float) -> float:
    """Signal s whose population rho_bar equals `target` (bisection, k = 200)."""
    if target == 0:
        return 0.0
    lo, hi = 0.0, 5.0
    for _ in range(30):
        mid = (lo + hi) / 2
        got = rho_bar(simulate(rng, 200, mid, 400), 200).mean()
        lo, hi = (mid, hi) if got < target else (lo, mid)
    return (lo + hi) / 2


def main() -> None:
    rng = np.random.default_rng(SEED)
    signals = {t: signal_for(rng, t) for t in TARGET_RHO}
    rows = []
    for k in K_VALUES:
        null_w = simulate(rng, k, 0.0, 200000)
        crit = float(np.quantile(null_w, 0.95))
        for target, s in signals.items():
            w = simulate(rng, k, s)
            rb = rho_bar(w, k)
            lo, hi = np.quantile(rb, [0.025, 0.975])
            rows.append({
                "k_datasets": k,
                "true_rho_bar": target,
                "critical_w_alpha05": round(crit, 3),
                "power": round(float((w > crit).mean()), 3),
                "mean_w": round(float(w.mean()), 3),
                "mean_rho_bar_hat": round(float(rb.mean()), 3),
                "rho_bar_hat_p2_5": round(float(lo), 3),
                "rho_bar_hat_p97_5": round(float(hi), 3),
                "range_width": round(float(hi - lo), 3),
            })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    for r in rows:
        print(",".join(str(v) for v in r.values()))


if __name__ == "__main__":
    main()
