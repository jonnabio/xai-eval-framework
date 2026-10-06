#!/usr/bin/env python3
"""Paper F: analysis of the run (ANALYSIS_PLAN.md, sections 3 to 6).

    python scripts/paper_f_analyze.py [--runs DIR] [--out DIR]

Reads the per-instance rows of scripts/paper_f_run.py and writes, to
outputs/analysis/paper_f/results/:

    instances.csv.gz     one row per dataset, model, seed, explainer and instance
    cells.csv            one mean per dataset, model, explainer and seed (the level of analysis)
    failures.csv         failure rate per dataset, model and explainer
    ranks.csv            order of the four explainers per dataset and measure
    primary.csv          mean rank correlation between datasets, interval, test, ceiling, decision
    per_model.csv        the primary estimate for each model
    pairs_vs_adult.csv   share of datasets where a pair of explainers is ordered as on Adult
    rank_change.csv      largest rank change of each explainer between two datasets
    dataset_pairs.csv    rank correlation of every pair of datasets (no p-values)
    variance.csv         shares of the sum of squares, and the explainer-by-dataset test
    frontier.csv         explainers not dominated on faithfulness gap and cost, per dataset
    secondary.csv        measures that are reported and not ranked

Only permutation tests are used. Intervals are bootstrap or exact binomial.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import beta, rankdata

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_f_lib as lib  # noqa: E402

# Ranked measures and their direction (+1: higher is better).
MEASURES = {"gap": 1, "stability": 1, "sparsity": 1, "cost_ms": -1}
SECONDARY = ["faith_corr", "n_used", "anchors_precision", "anchors_coverage", "dice_valid",
             "dice_l1"]
EXPL = list(lib.EXPLAINERS)
THRESHOLD = 0.5          # plan section 6
N_BOOT, N_PERM, N_PERM_VAR = 10000, 100000, 10000
SEED = 20261005


# --- loading -------------------------------------------------------------------

def load(runs: Path) -> pd.DataFrame:
    rows = []
    for path in sorted(runs.glob("*/*/seed_*/*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    df = pd.DataFrame(rows)
    df = df.drop_duplicates(["dataset", "model", "seed", "explainer", "instance"], keep="first")
    return df.drop(columns=[c for c in ("top",) if c in df.columns])


def impute_failures(df: pd.DataFrame) -> pd.DataFrame:
    """A failed instance takes the worst value observed in its dataset and model (plan 3)."""
    df = df.copy()
    ok = df[df["failed"] == 0]
    for measure, sign in MEASURES.items():
        worst = ok.groupby(["dataset", "model"])[measure].agg("min" if sign > 0 else "max")
        fill = df.set_index(["dataset", "model"]).index.map(worst)
        df[measure] = df[measure].where(df["failed"] == 0, pd.Series(fill, index=df.index))
    return df


def cell_means(df: pd.DataFrame) -> pd.DataFrame:
    keys = ["dataset", "model", "explainer", "seed"]
    cells = df.groupby(keys)[list(MEASURES)].mean()
    cells["failure_rate"] = df.groupby(keys)["failed"].mean()
    cells["n"] = df.groupby(keys)["instance"].count()
    return cells.reset_index()


# --- ranks and agreement -------------------------------------------------------

def rank_table(cells: pd.DataFrame, measure: str, by: list[str]) -> pd.DataFrame:
    """Rank 1 = best explainer, for each group of `by` (mean of the cell means first)."""
    score = cells.groupby(by + ["explainer"])[measure].mean().unstack("explainer")[EXPL]
    score = score * MEASURES[measure]
    ranks = score.apply(lambda r: pd.Series(rankdata(-r.to_numpy()), index=EXPL), axis=1)
    return ranks


def standardise(ranks: np.ndarray) -> np.ndarray:
    """Rows to mean 0 and unit variance; a row of equal ranks becomes zeros."""
    z = ranks - ranks.mean(axis=1, keepdims=True)
    sd = z.std(axis=1, keepdims=True)
    return np.divide(z, sd, out=np.zeros_like(z), where=sd > 0)


def mean_corr(z: np.ndarray) -> float:
    """Mean Spearman correlation between all pairs of rows of standardised ranks."""
    k, n = z.shape[-2], z.shape[-1]
    total = (z.sum(axis=-2) ** 2).sum(axis=-1) - (z ** 2).sum(axis=(-2, -1))
    return total / (k * (k - 1) * n)


def bootstrap_interval(z: np.ndarray, rng) -> tuple[float, float]:
    """Percentile interval over datasets; a dataset drawn twice is not paired with itself."""
    k, n = z.shape
    corr = z @ z.T / n
    values = np.empty(N_BOOT)
    iu = np.triu_indices(k, 1)
    for b in range(N_BOOT):
        idx = rng.integers(0, k, k)
        a, c = idx[iu[0]], idx[iu[1]]
        keep = a != c
        values[b] = corr[a[keep], c[keep]].mean() if keep.any() else np.nan
    return float(np.nanquantile(values, 0.025)), float(np.nanquantile(values, 0.975))


def permutation_p(ranks: np.ndarray, rng, n_perm: int = N_PERM) -> float:
    """One-sided p of 'the orders of different datasets are unrelated'."""
    z = standardise(ranks)
    observed = mean_corr(z)
    k, n = z.shape
    count, chunk = 0, 5000
    for start in range(0, n_perm, chunk):
        size = min(chunk, n_perm - start)
        perm = rng.permuted(np.broadcast_to(z, (size, k, n)).copy(), axis=2)
        count += int((mean_corr(perm) >= observed - 1e-12).sum())
    return (1 + count) / (1 + n_perm)


def holm(p: list[float]) -> list[float]:
    order = np.argsort(p)
    out, running = [0.0] * len(p), 0.0
    for i, j in enumerate(order):
        running = max(running, (len(p) - i) * p[j])
        out[j] = min(1.0, running)
    return out


def decision(p: float, low: float, high: float) -> str:
    if p >= 0.05:
        return "no evidence that the order is shared"
    if low > THRESHOLD:
        return "the order generalises"
    if high < THRESHOLD:
        return "the order is shared only weakly"
    return "shared, strength not determined"


def ceiling(cells: pd.DataFrame, measure: str) -> float:
    """Mean rank correlation between seeds inside a dataset, averaged over datasets."""
    values = []
    for _, part in cells.groupby("dataset"):
        r = rank_table(part, measure, ["seed"]).to_numpy()
        if len(r) > 1:
            values.append(float(mean_corr(standardise(r))))
    return float(np.mean(values)) if values else float("nan")


def primary(cells: pd.DataFrame, rng) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows, all_ranks = [], []
    for measure in MEASURES:
        ranks = rank_table(cells, measure, ["dataset"])
        all_ranks.append(ranks.assign(measure=measure).reset_index())
        r = ranks.to_numpy()
        z = standardise(r)
        low, high = bootstrap_interval(z, rng)
        k = len(r)
        rho = float(mean_corr(z))
        rows.append({"measure": measure, "datasets": k, "mean_rank_corr": rho,
                     "kendall_w": ((k - 1) * rho + 1) / k, "ci_low": low, "ci_high": high,
                     "p_perm": permutation_p(r, rng), "ceiling_seeds": ceiling(cells, measure),
                     **{f"mean_rank_{e}": float(ranks[e].mean()) for e in EXPL}})
    out = pd.DataFrame(rows)
    out["p_holm"] = holm(out["p_perm"].tolist())
    out["decision"] = [decision(p, lo, hi) for p, lo, hi in
                       zip(out["p_holm"], out["ci_low"], out["ci_high"])]
    return out, pd.concat(all_ranks, ignore_index=True)


def per_model(cells: pd.DataFrame, rng) -> pd.DataFrame:
    rows = []
    for model, part in cells.groupby("model"):
        for measure in MEASURES:
            r = rank_table(part, measure, ["dataset"]).to_numpy()
            z = standardise(r)
            low, high = bootstrap_interval(z, rng)
            rows.append({"model": model, "measure": measure, "mean_rank_corr": float(mean_corr(z)),
                         "ci_low": low, "ci_high": high,
                         "p_perm": permutation_p(r, rng, 20000)})
    return pd.DataFrame(rows)


# --- secondary -----------------------------------------------------------------

def pairs_vs_adult(ranks: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for measure, part in ranks.groupby("measure"):
        part = part.set_index("dataset")
        if "adult" not in part.index:
            continue
        others = part.drop(index="adult")
        for a, b in itertools.combinations(EXPL, 2):
            ref = np.sign(part.loc["adult", a] - part.loc["adult", b])
            same = int((np.sign(others[a] - others[b]) == ref).sum()) if ref != 0 else 0
            n = len(others)
            low = beta.ppf(0.025, same, n - same + 1) if same > 0 else 0.0
            high = beta.ppf(0.975, same + 1, n - same) if same < n else 1.0
            rows.append({"measure": measure, "pair": f"{a} vs {b}",
                         "better_on_adult": a if ref < 0 else (b if ref > 0 else "tie"),
                         "same_order": same, "datasets": n, "share": same / n,
                         "ci_low": float(low), "ci_high": float(high)})
    return pd.DataFrame(rows)


def rank_change(ranks: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for measure, part in ranks.groupby("measure"):
        for e in EXPL:
            rows.append({"measure": measure, "explainer": e, "best_rank": float(part[e].min()),
                         "worst_rank": float(part[e].max()),
                         "largest_change": float(part[e].max() - part[e].min()),
                         "times_first": int((part[e] == 1).sum())})
    return pd.DataFrame(rows)


def dataset_pairs(ranks: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for measure, part in ranks.groupby("measure"):
        names = part["dataset"].tolist()
        z = standardise(part[EXPL].to_numpy())
        corr = z @ z.T / z.shape[1]
        for i, j in itertools.combinations(range(len(names)), 2):
            rows.append({"measure": measure, "dataset_a": names[i], "dataset_b": names[j],
                         "rank_corr": float(corr[i, j])})
    return pd.DataFrame(rows)


def _cube(cells: pd.DataFrame, measure: str) -> np.ndarray:
    """Values as an array [dataset, model, explainer, seed position]; needs a balanced design."""
    cells = cells.copy()
    cells["rep"] = cells.groupby(["dataset", "model", "explainer"]).cumcount()
    wide = cells.pivot_table(index=["dataset", "model"], columns=["explainer", "rep"],
                             values=measure)
    d, m = cells["dataset"].nunique(), cells["model"].nunique()
    e, s = cells["explainer"].nunique(), cells["rep"].nunique()
    arr = wide.to_numpy().reshape(d, m, e, s)
    if np.isnan(arr).any():
        raise ValueError("the design is not balanced: some cells are missing")
    return arr


def _sums_of_squares(y: np.ndarray) -> dict[str, float]:
    """Balanced decomposition over dataset (D), model (M), explainer (E); seeds are replicates."""
    g = y.mean()
    cell = y.mean(axis=3)
    D, M, E = cell.mean(axis=(1, 2)), cell.mean(axis=(0, 2)), cell.mean(axis=(0, 1))
    DM, DE, ME = cell.mean(axis=2), cell.mean(axis=1), cell.mean(axis=0)
    nd, nm, ne, ns = y.shape
    ss = {
        "dataset": nm * ne * ns * ((D - g) ** 2).sum(),
        "model": nd * ne * ns * ((M - g) ** 2).sum(),
        "explainer": nd * nm * ns * ((E - g) ** 2).sum(),
        "dataset x model": ne * ns * ((DM - D[:, None] - M[None, :] + g) ** 2).sum(),
        "explainer x dataset": nm * ns * ((DE - D[:, None] - E[None, :] + g) ** 2).sum(),
        "explainer x model": nd * ns * ((ME - M[:, None] - E[None, :] + g) ** 2).sum(),
    }
    three = (cell - DM[:, :, None] - DE[:, None, :] - ME[None, :, :]
             + D[:, None, None] + M[None, :, None] + E[None, None, :] - g)
    ss["explainer x dataset x model"] = ns * (three ** 2).sum()
    ss["residual (seeds)"] = ((y - cell[..., None]) ** 2).sum()
    return ss


def _aligned_ranks(y: np.ndarray) -> np.ndarray:
    """Aligned rank transform for the explainer-by-dataset term."""
    cell = y.mean(axis=3)
    g = y.mean()
    D, E, DE = cell.mean(axis=(1, 2)), cell.mean(axis=(0, 1)), cell.mean(axis=1)
    effect = DE - D[:, None] - E[None, :] + g
    aligned = (y - cell[..., None]) + effect[:, None, :, None]
    return rankdata(aligned).reshape(y.shape)


def _interaction_p(y: np.ndarray, rng) -> float:
    """Permutation test of explainer x dataset: explainer labels are permuted inside each
    dataset, model and seed block, after the explainer and explainer-by-model means are removed."""
    cell = y.mean(axis=3)
    ME = cell.mean(axis=0)
    resid = y - ME[None, :, :, None]
    observed = _sums_of_squares(resid)["explainer x dataset"]
    count = 0
    for _ in range(N_PERM_VAR):
        perm = rng.permuted(resid, axis=2)
        count += _sums_of_squares(perm)["explainer x dataset"] >= observed - 1e-12
    return (1 + count) / (1 + N_PERM_VAR)


def variance(cells: pd.DataFrame, rng) -> pd.DataFrame:
    rows = []
    for measure in MEASURES:
        y = _cube(cells, measure)
        for label, arr in (("mixed model (balanced)", y), ("aligned ranks", _aligned_ranks(y))):
            ss = _sums_of_squares(arr)
            total = sum(ss.values())
            p = _interaction_p(arr, rng)
            ratio = ss["explainer x dataset"] / (ss["explainer"] + ss["explainer x dataset"])
            for term, value in ss.items():
                rows.append({"measure": measure, "analysis": label, "term": term,
                             "share": value / total,
                             "p_perm": p if term == "explainer x dataset" else np.nan,
                             "interaction_over_explainer":
                                 ratio if term == "explainer x dataset" else np.nan})
    return pd.DataFrame(rows)


def frontier(cells: pd.DataFrame) -> pd.DataFrame:
    means = cells.groupby(["dataset", "explainer"])[["gap", "cost_ms"]].mean().reset_index()
    rows = []
    for dataset, part in means.groupby("dataset"):
        for _, a in part.iterrows():
            dominated = any((b["gap"] >= a["gap"]) and (b["cost_ms"] <= a["cost_ms"])
                            and ((b["gap"] > a["gap"]) or (b["cost_ms"] < a["cost_ms"]))
                            for _, b in part.iterrows())
            rows.append({"dataset": dataset, "explainer": a["explainer"], "gap": a["gap"],
                         "cost_ms": a["cost_ms"], "on_frontier": int(not dominated)})
    return pd.DataFrame(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--runs", default=str(lib.OUT / "runs"))
    ap.add_argument("--out", default=str(lib.OUT / "results"))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)

    raw = load(Path(args.runs))
    raw.to_csv(out / "instances.csv.gz", index=False)
    keys = ["dataset", "model", "explainer"]
    raw.groupby(keys)["failed"].agg(["mean", "sum", "count"]).reset_index().rename(
        columns={"mean": "failure_rate", "sum": "failures", "count": "instances"}).to_csv(
        out / "failures.csv", index=False)
    present = [c for c in SECONDARY if c in raw.columns]
    raw[raw["failed"] == 0].groupby(keys)[present].mean().reset_index().to_csv(
        out / "secondary.csv", index=False)

    cells = cell_means(impute_failures(raw))
    cells.to_csv(out / "cells.csv", index=False)
    table, ranks = primary(cells, rng)
    table.to_csv(out / "primary.csv", index=False)
    ranks.to_csv(out / "ranks.csv", index=False)
    per_model(cells, rng).to_csv(out / "per_model.csv", index=False)
    pairs_vs_adult(ranks).to_csv(out / "pairs_vs_adult.csv", index=False)
    rank_change(ranks).to_csv(out / "rank_change.csv", index=False)
    dataset_pairs(ranks).to_csv(out / "dataset_pairs.csv", index=False)
    variance(cells, rng).to_csv(out / "variance.csv", index=False)
    frontier(cells).to_csv(out / "frontier.csv", index=False)
    print(table[["measure", "datasets", "mean_rank_corr", "ci_low", "ci_high", "p_holm",
                 "ceiling_seeds", "decision"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
