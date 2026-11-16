#!/usr/bin/env python3
"""Paper G quality review: what LIME returns under Paper G's configuration (constructed toy only).

A model whose class-1 probability is linear in the features, p(x) = 0.5 + 0.04 * beta.(x - mu),
has exact contributions relative to the training mean c_j = 0.04 * beta_j * (x_j - mu_j)
(interventional Shapley values with the mean as the single reference). LIME is configured as in
scripts/paper_g_lib.py::Lime (discretize_continuous=False, kernel_width=3.0, num_samples=1000,
labels=(1,), all features). No Paper G data, generator or model is used.
"""
import numpy as np
from lime.lime_tabular import LimeTabularExplainer
from scipy import stats

rng = np.random.default_rng(0)
d = 8
beta = np.array([2.0, -1.5, 1.0, -0.5, 0.25, 0.0, 1.2, -0.8])
sd = np.array([1.0, 2.0, 0.5, 1.0, 3.0, 1.0, 1.0, 0.5])         # unequal feature scales
X = rng.normal(0, 1, (2000, d)) * sd
mu = X.mean(axis=0)


def proba(Z):
    p1 = np.clip(0.5 + 0.04 * (Z - mu) @ beta, 0.0, 1.0)
    return np.column_stack([1 - p1, p1])


def lime_weights(x, seed, **kw):
    ex = LimeTabularExplainer(X, mode="classification", class_names=["0", "1"], random_state=seed, **kw)
    exp = ex.explain_instance(x, proba, labels=(1,), num_features=d, num_samples=1000)
    w = np.zeros(d)
    for j, v in exp.as_map()[1]:
        w[j] = v
    return w, ex


rows = []
for i in range(6):
    x = X[100 + i]
    w, ex = lime_weights(x, i, discretize_continuous=False, kernel_width=3.0)
    z = (x - ex.scaler.mean_) / ex.scaler.scale_                 # LIME's standardised coordinates
    c_true = 0.04 * beta * (x - mu)
    slope_per_sd = 0.04 * beta * ex.scaler.scale_                # d p / d z_j
    rows.append((stats.spearmanr(w, slope_per_sd).statistic, stats.spearmanr(w, c_true).statistic,
                 stats.spearmanr(w * z, c_true).statistic, float(np.max(np.abs(w - slope_per_sd)))))
    if i == 0:
        print("instance 0: LIME weight   :", np.round(w, 4))
        print("            0.04*beta*sd  :", np.round(slope_per_sd, 4), " (slope per training s.d.)")
        print("            true contrib  :", np.round(c_true, 4))
        print("            LIME w * z    :", np.round(w * z, 4))
print("\nper instance: rho(w, slope)  rho(w, contribution)  rho(w*z, contribution)  max|w - slope|")
for r in rows:
    print(f"              {r[0]:6.3f}        {r[1]:6.3f}                {r[2]:6.3f}                {r[3]:.4f}")
x = X[100]
w_def, _ = lime_weights(x, 0, discretize_continuous=False)                 # default kernel width
w_disc, _ = lime_weights(x, 0)                                             # package default: discretised
print(f"\nkernel width default (0.75*sqrt(d) = {0.75*np.sqrt(d):.2f}) vs 3.0: rho of weights {stats.spearmanr(w_def, rows and lime_weights(x, 0, discretize_continuous=False, kernel_width=3.0)[0]).statistic:.3f}")
print(f"discretize_continuous=True (package default): rho(w, contribution) = {stats.spearmanr(w_disc, 0.04*beta*(x-mu)).statistic:.3f}")
