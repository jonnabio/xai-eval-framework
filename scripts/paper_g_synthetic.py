#!/usr/bin/env python3
"""Paper G: synthetic ground-truth check (plan section 2.5).

A known function is used directly as the model, so no fitted model stands between the data
and the truth. Ground truth: the exact interventional Shapley values of the predicted-class
probability, with the expectation taken over a background sample of the same distribution,
computed by enumerating all 2^8 coalitions:

    v(S) = mean_z f(x_S, z_notS),   phi_i = sum_{S not containing i} w(|S|) (v(S + i) - v(S))

Generators (8 standard normal features, independent or equicorrelated at 0.5):
- additive:     logit = beta . x
- interaction:  logit = 0.5 * beta . x + 1.5 x0 x1 - 1.5 x2 x3
with beta = (2, -1.5, 1, -0.75, 0.5, -0.25, 0, 0).
"""
from __future__ import annotations

import math
from itertools import product

import numpy as np

BETA = np.array([2.0, -1.5, 1.0, -0.75, 0.5, -0.25, 0.0, 0.0])
N_TRAIN = 2000
N_TRUTH_BACKGROUND = 500


class KnownModel:
    """A fixed function with the interface the explainers and metrics use."""

    def __init__(self, generator: str):
        if generator not in ("additive", "interaction"):
            raise KeyError(generator)
        self.generator = generator

    def logit(self, X: np.ndarray) -> np.ndarray:
        if self.generator == "additive":
            return X @ BETA
        return 0.5 * (X @ BETA) + 1.5 * X[..., 0] * X[..., 1] - 1.5 * X[..., 2] * X[..., 3]

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        p1 = 1.0 / (1.0 + np.exp(-self.logit(np.asarray(X, dtype=float))))
        return np.stack([1 - p1, p1], axis=-1)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)


def sample(n: int, d: int, rho: float, rng: np.random.Generator) -> np.ndarray:
    cov = np.full((d, d), rho) + (1 - rho) * np.eye(d)
    return rng.standard_normal((n, d)) @ np.linalg.cholesky(cov).T


def shapley_weights(d: int) -> np.ndarray:
    """w(s) = s! (d - s - 1)! / d! for coalition sizes s = 0 .. d-1."""
    return np.array([math.factorial(s) * math.factorial(d - s - 1) / math.factorial(d)
                     for s in range(d)])


def exact_shapley(value, d: int) -> np.ndarray:
    """Shapley values of a set function given as value(mask_matrix) -> v per coalition."""
    masks = np.array(list(product([0, 1], repeat=d)), dtype=bool)   # 2^d coalitions
    v = value(masks)
    index = {tuple(m): i for i, m in enumerate(masks)}
    w = shapley_weights(d)
    phi = np.zeros(d)
    for i in range(d):
        for k, m in enumerate(masks):
            if m[i]:
                continue
            with_i = m.copy()
            with_i[i] = True
            phi[i] += w[m.sum()] * (v[index[tuple(with_i)]] - v[k])
    return phi


def interventional_shapley(f, x: np.ndarray, background: np.ndarray) -> np.ndarray:
    """Exact interventional Shapley values of f at x over the background sample."""
    d = len(x)

    def value(masks):
        # (coalitions, background, d): x where the coalition holds, background elsewhere.
        z = np.where(masks[:, None, :], x[None, None, :], background[None, :, :])
        return f(z.reshape(-1, d)).reshape(len(masks), len(background)).mean(axis=1)

    return exact_shapley(value, d)


def make_condition(generator: str, rho: float, seed: int, cfg: dict) -> dict:
    """A data dict with the same keys as paper_g_lib.prepare, for the known model."""
    from paper_g_lib import baseline, pick_instances
    d = cfg["synthetic"]["n_features"]
    rng = np.random.default_rng([seed, int(rho * 100), 0 if generator == "additive" else 1])
    X_train = sample(N_TRAIN, d, rho, rng)
    X_test = sample(max(cfg["synthetic"]["n_instances"] * 2, 400), d, rho, rng)
    model = KnownModel(generator)
    groups = [np.array([j]) for j in range(d)]
    is_numeric = np.ones(d, dtype=bool)
    pred = model.predict(X_test)
    return {"X_train": X_train, "X_test": X_test, "y_train": model.predict(X_train),
            "y_test": pred, "names": [f"x{j}" for j in range(d)], "groups": groups,
            "group_names": [f"x{j}" for j in range(d)], "is_numeric": is_numeric,
            "model": model, "pred": pred, "base": baseline(X_train, groups, is_numeric),
            "instances": pick_instances(pred, cfg["synthetic"]["n_instances"], seed),
            "truth_background": sample(N_TRUTH_BACKGROUND, d, rho, rng),
            "meta": {"generator": generator, "rho": rho}}


def true_attribution(data: dict, pos: int) -> np.ndarray:
    """Exact Shapley values of the predicted-class probability at test row `pos`."""
    model, c = data["model"], int(data["pred"][pos])
    return interventional_shapley(lambda z: model.predict_proba(z)[:, c],
                                  data["X_test"][pos], data["truth_background"])
