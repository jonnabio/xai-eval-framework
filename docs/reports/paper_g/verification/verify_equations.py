#!/usr/bin/env python3
"""Paper G: check the manuscript's numbered equations against the frozen implementation.

Each equation of paper_g_draft.md is coded here independently, in the closed form the manuscript
prints, and compared with the frozen function it describes on constructed examples (random
logistic models, grouped one-hot style features, ties, constant attributions, undefined rank
correlations). No result file is read and no scientific result is recomputed.

    ~/xai-eval-framework/.venv/bin/python docs/reports/paper_g/verification/verify_equations.py

Writes verify_equations_output.txt next to this script; exit status 1 on any disagreement.
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import paper_g_analyze as an  # noqa: E402
import paper_g_lib as lib  # noqa: E402
import paper_g_s1_lime as s1  # noqa: E402

TOL = 1e-12
lines: list[str] = []
failures = 0


def check(name: str, got: float, want: float, tol: float = TOL) -> None:
    global failures
    ok = (math.isnan(got) and math.isnan(want)) or abs(got - want) <= tol
    failures += not ok
    lines.append(f"{'ok  ' if ok else 'FAIL'} {name}: frozen {got!r} manuscript {want!r}")


def example(rng: np.random.Generator, n_groups: int):
    """A logistic model on grouped columns: some groups one column, some three (one-hot-like)."""
    sizes = rng.choice([1, 1, 3], size=n_groups)
    groups, start = [], 0
    for s in sizes:
        groups.append(np.arange(start, start + s))
        start += s
    d = start
    w, c = rng.normal(size=d), rng.normal()
    x, b = rng.normal(size=d), rng.normal(size=d)
    pred_class = int(rng.random() < 0.5)

    def prob(batch):
        p1 = 1 / (1 + np.exp(-(np.atleast_2d(batch) @ w + c)))
        return p1 if pred_class == 1 else 1 - p1
    return groups, x, b, prob


def masked(x, b, groups, which):
    z = x.copy()
    for i in which:
        z[groups[i]] = b[groups[i]]
    return z


def manuscript_m1_m2(a, x, b, groups, f):
    """Equation (1): trapezoidal areas over the G + 1 points t = 0, ..., G, step 1/G."""
    G = len(groups)
    pi = np.lexsort((np.arange(G), -a))                      # decreasing a, ties by index
    p = [f(masked(x, b, groups, pi[:t]))[0] for t in range(G + 1)]   # p_0 = f(x), p_G = f(b)
    q = [f(masked(x, b, groups, pi[t:]))[0] for t in range(G + 1)]   # q_0 = f(b), q_G = f(x)
    m1 = (0.5 * (p[0] + p[G]) + sum(p[1:G])) / G
    m2 = (0.5 * (q[0] + q[G]) + sum(q[1:G])) / G
    return m1, m2, pi


def manuscript_m3_m6(a, x, b, groups, f, pi):
    """Equation (2): T = the top k = max(1, ceil(0.2 G)) features by a."""
    G = len(groups)
    k = max(1, math.ceil(0.2 * G))
    T, rest = pi[:k], pi[k:]
    fx = f(x)[0]
    return fx - f(masked(x, b, groups, T))[0], fx - f(masked(x, b, groups, rest))[0]


def manuscript_m4(a, x, b, groups, f):
    """Pearson correlation of a_i with Delta_i = f(x) - f(x_{i<-b}); 0 (flagged) if constant."""
    fx = f(x)[0]
    delta = np.array([fx - f(masked(x, b, groups, [i]))[0] for i in range(len(groups))])
    if delta.std() < 1e-12 or a.std() < 1e-12:
        return 0.0
    return float(np.corrcoef(a, delta)[0, 1])


def manuscript_m5(a, x, b, groups, f, masks):
    """Equation (3): 1 - R^2_0 of the no-intercept fit of Delta_r on s_r over the R subsets."""
    fx = f(x)[0]
    dy = np.array([fx - f(masked(x, b, groups, np.flatnonzero(m)))[0] for m in masks])
    s = np.array([a[m].sum() for m in masks])
    if dy @ dy < 1e-18:
        return 0.0
    if s @ s < 1e-18:
        return 1.0
    beta = (s @ dy) / (s @ s)
    return float(((dy - beta * s) ** 2).sum() / (dy @ dy))


def manuscript_agreement(R):
    """Equation (4): mean of rho_s over the defined pairs D_b (both rank vectors non-constant)."""
    vals = []
    for j, k in itertools.combinations(range(R.shape[0]), 2):
        u, v = R[j] - R[j].mean(), R[k] - R[k].mean()
        if u @ u < 1e-12 or v @ v < 1e-12:
            continue                                         # undefined: not in D_b
        vals.append((u @ v) / math.sqrt((u @ u) * (v @ v)))
    return float(np.mean(vals)) if vals else math.nan, len(vals)


def main() -> int:
    rng = np.random.default_rng(20261116)
    for case in range(40):
        G = int(rng.integers(2, 12))
        groups, x, b, f = example(rng, G)
        a = rng.normal(size=G)
        if case % 5 == 0:
            a[: G // 2] = a[0]                              # ties in the attribution
        if case % 13 == 0:
            a[:] = 0.7                                      # constant attribution
        frozen = lib.removal_metrics(a, x, f, b, groups, 0.2)
        m1, m2, pi = manuscript_m1_m2(a, x, b, groups, f)
        m3, m6 = manuscript_m3_m6(a, x, b, groups, f, pi)
        check(f"case {case} G={G} M1 (Eq. 1)", frozen["m1_deletion"], m1)
        check(f"case {case} G={G} M2 (Eq. 1)", frozen["m2_insertion"], m2)
        check(f"case {case} G={G} M3 (Eq. 2)", frozen["m3_gap"], m3)
        check(f"case {case} G={G} M6 (Eq. 2)", frozen["m6_sufficiency"], m6)
        check(f"case {case} G={G} M4", lib.correlation_metric(a, x, f, b, groups)[0],
              manuscript_m4(a, x, b, groups, f))
        draws_rng = np.random.default_rng(case)
        frozen_m5 = lib.infidelity_metric(a, x, f, b, groups, 100, 0.5, draws_rng)
        replay = np.random.default_rng(case)                # the same subsets the frozen code drew
        masks = replay.random((100, G)) < 0.5
        masks[masks.sum(axis=1) == 0, replay.integers(0, G)] = True
        check(f"case {case} G={G} M5 (Eq. 3)", frozen_m5, manuscript_m5(a, x, b, groups, f, masks))
        # The arithmetic sum over d points printed in v0.2 differs from the frozen area:
        if case == 1:
            old = sum(f(masked(x, b, groups, pi[:t]))[0] for t in range(1, G + 1)) / G
            lines.append(f"info v0.2 Eq. 1 (sum over t=1..d) for case 1: {old!r} vs frozen "
                         f"{frozen['m1_deletion']!r} (difference {old - frozen['m1_deletion']:+.3e})")

    # Equation (4) against the frozen agreement statistic, with undefined pairs.
    for case in range(200):
        R = np.vstack([an.ranks_desc(v) for v in rng.integers(0, 3, size=(7, 3)).astype(float)])
        got, n_def, n_undef = an.mean_pairwise_spearman(R)
        want, n_want = manuscript_agreement(R)
        check(f"agreement case {case} (|D_b| = {n_want})", got, want)
        if n_def != n_want or n_def + n_undef != 21:
            check(f"agreement case {case} defined-pair count", float(n_def), float(n_want))

    # Equation (5): S1 contribution of a raw feature, against the frozen S1 code.
    for case in range(20):
        d = int(rng.integers(2, 9))
        w, x, r, s = rng.normal(size=d), rng.normal(size=d), rng.normal(size=d), rng.uniform(0.1, 2, d)
        groups = [np.arange(0, 1), np.arange(1, d)]
        got = lib.group_attr(s1.contributions(w, x, r, s), groups)
        want = np.array([sum(w[k] * (x[k] - r[k]) / s[k] for k in g) for g in groups])
        for j in range(2):
            check(f"S1 case {case} group {j} (Eq. 5)", float(got[j]), float(want[j]))

    lines.append(f"\n{sum(1 for ln in lines if ln.startswith(('ok', 'FAIL')))} checks, "
                 f"{failures} disagreement(s)")
    out = Path(__file__).with_name("verify_equations_output.txt")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(lines[-1].strip())
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
