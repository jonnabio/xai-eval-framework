#!/usr/bin/env python3
"""Paper G: is the precision of the agreement estimate (H1) useful with eight datasets?

No data are read. Design of the plan (version 2): in each block (dataset x model x seed)
three studied explainers are ranked by each of seven metrics. Agreement between metrics in a
block is the mean pairwise Spearman correlation rho_bar = (m W - 1) / (m - 1), m = 7. The
estimate is the mean of rho_bar over all blocks; its 95% interval is a percentile bootstrap
over datasets (plan section 4.1).

Latent-score model, for dataset d, block b, metric g, explainer j:

    score = s * mu[j] + sqrt(h) * U[d, g, j] + sqrt(1 - h) * E[d, b, g, j]

mu = (-1, 0, 1). U is disagreement between metrics that persists within a dataset (it makes
blocks of a dataset correlated, which is why datasets, not blocks, are resampled); E is
block-level noise. h is the dataset share of the noise. The signal s is set so that the
population rho_bar takes a target value.

For each number of datasets k and each target, the script reports the mean estimate, the
mean bootstrap interval and its width, the coverage of the true value, and the power of a
block-level permutation test (null simulated with independent rankings in every block). It
also reports a t-interval and one-sided t-test on the k dataset means, which treat the
dataset as the unit. Finding of the first run (2026-11-13): the block-level test is
anti-conservative when blocks of a dataset are correlated, and the percentile bootstrap
undercovers with few datasets; see the plan, section 4.1.

Output: outputs/analysis/paper_g/power_simulation.csv
Run:    python scripts/paper_g_power_simulation.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from scipy import stats

N_METRICS = 7
N_EXPLAINERS = 3
BLOCKS_PER_DATASET = 20          # 4 models x 5 seeds
K_VALUES = (6, 8, 10, 12, 16)
TARGET_RHO = (0.0, 0.2, 0.5, 0.8)
H_SHARES = (0.2, 0.5, 0.8)
MU = np.array([-1.0, 0.0, 1.0])
N_SIM = 1000
N_BOOT = 1000
SEED = 20261113
OUT = Path(__file__).resolve().parents[1] / "outputs" / "analysis" / "paper_g" / "power_simulation.csv"


def ranks(scores: np.ndarray) -> np.ndarray:
    return scores.argsort(axis=-1).argsort(axis=-1) + 1.0


def rho_bar_blocks(scores: np.ndarray) -> np.ndarray:
    """Mean pairwise Spearman between metrics, per block. scores: (..., m, n)."""
    r = ranks(scores)
    m, n = r.shape[-2], r.shape[-1]
    col = r.sum(axis=-2)
    s = ((col - m * (n + 1) / 2) ** 2).sum(axis=-1)
    w = 12 * s / (m**2 * (n**3 - n))
    return (m * w - 1) / (m - 1)


def draw(rng, n_sim, k, s, h):
    shape_u = (n_sim, k, 1, N_METRICS, N_EXPLAINERS)
    shape_e = (n_sim, k, BLOCKS_PER_DATASET, N_METRICS, N_EXPLAINERS)
    u = rng.standard_normal(shape_u)
    e = rng.standard_normal(shape_e)
    scores = s * MU + np.sqrt(h) * u + np.sqrt(1 - h) * e
    return rho_bar_blocks(scores)          # (n_sim, k, blocks)


def signal_for(rng, target, h):
    if target == 0:
        return 0.0
    lo, hi = 0.0, 6.0
    for _ in range(25):
        mid = (lo + hi) / 2
        got = draw(rng, 1, 400, mid, h).mean()
        lo, hi = (mid, hi) if got < target else (lo, mid)
    return (lo + hi) / 2


def main() -> None:
    rng = np.random.default_rng(SEED)
    rows = []
    for h in H_SHARES:
        signals = {t: signal_for(rng, t, h) for t in TARGET_RHO}
        for k in K_VALUES:
            # Null of the permutation test: rankings independent in every block.
            null_est = np.concatenate(
                [draw(rng, 2000, k, 0.0, 0.5).mean(axis=(1, 2)) for _ in range(10)]
            )
            crit = float(np.quantile(null_est, 0.95))
            for target, s in signals.items():
                per_ds = draw(rng, N_SIM, k, s, h).mean(axis=2)       # (n_sim, k)
                est = per_ds.mean(axis=1)
                idx = rng.integers(0, k, size=(N_SIM, N_BOOT, k))
                boot = np.take_along_axis(per_ds[:, None, :].repeat(N_BOOT, 1), idx, axis=2).mean(axis=2)
                lo = np.quantile(boot, 0.025, axis=1)
                hi = np.quantile(boot, 0.975, axis=1)
                sd = per_ds.std(axis=1, ddof=1)
                tq = stats.t.ppf(0.975, k - 1)
                tlo, thi = est - tq * sd / np.sqrt(k), est + tq * sd / np.sqrt(k)
                tstat = est / (sd / np.sqrt(k))
                t_reject = tstat > stats.t.ppf(0.95, k - 1)
                rows.append({
                    "dataset_share_h": h,
                    "k_datasets": k,
                    "true_rho_bar": target,
                    "signal": round(s, 4),
                    "mean_estimate": round(float(est.mean()), 3),
                    "mean_ci_low": round(float(lo.mean()), 3),
                    "mean_ci_high": round(float(hi.mean()), 3),
                    "mean_ci_width": round(float((hi - lo).mean()), 3),
                    "coverage": round(float(((lo <= target) & (target <= hi)).mean()), 3),
                    "power_perm_test": round(float((est > crit).mean()), 3),
                    "ci_above_0_5": round(float((lo > 0.5).mean()), 3),
                    "ci_below_0_5": round(float((hi < 0.5).mean()), 3),
                    "t_ci_width": round(float((thi - tlo).mean()), 3),
                    "t_coverage": round(float(((tlo <= target) & (target <= thi)).mean()), 3),
                    "t_test_reject": round(float(t_reject.mean()), 3),
                    "t_ci_above_0_5": round(float((tlo > 0.5).mean()), 3),
                })
                print(",".join(str(v) for v in rows[-1].values()), flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)


if __name__ == "__main__":
    main()
