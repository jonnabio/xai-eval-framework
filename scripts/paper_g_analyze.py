#!/usr/bin/env python3
"""Paper G: the analysis of the frozen run (ANALYSIS_PLAN.md sections 4 and 11).

    python scripts/paper_g_analyze.py --validate-only
        manifest hashes and record structure of the frozen data; counts only, no statistic
    python scripts/paper_g_analyze.py --run --authorized "<who, date>"
        the single authorized analysis; refuses while experiments/exp_g/analysis.toml has an
        UNDECIDED item (plan 11.8)

Outputs: outputs/analysis/paper_g/analysis/{confirmatory,sensitivity,exploratory,synthetic,figures}
and docs/reports/paper_g/RESULTS_REPORT.md (generated, never hand-edited).

The code is split as the plan's steps are: loading, structural validation, orientation,
aggregation, ranking, agreement statistics, dataset-level inference, permutation testing,
multiplicity, sensitivity analyses, the synthetic check, and the report. Attribution vectors
(`attr`, `true_attr`) are never loaded: only metric values and `spearman_truth` are read.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import itertools
import json
import math
import sys
import tomllib
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_g_lib as lib  # noqa: E402

SPEC_PATH = lib.ROOT / "experiments" / "exp_g" / "analysis.toml"
RAW = lib.OUT / "raw"
ANALYSIS_OUT = lib.OUT / "analysis"
REPORT_PATH = lib.ROOT / "docs" / "reports" / "paper_g" / "RESULTS_REPORT.md"
STAGES = ("full", "roar", "synthetic")
BLOCK = ["dataset", "model", "seed"]
INSTANCE_FIELDS = ["stage", "dataset", "model", "seed", "explainer", "instance", "failed",
                   "pred_class", "m4_degenerate", *lib.INSTANCE_METRICS,
                   *(f"{m}_b2" for m in ("m1_deletion", "m2_insertion", "m3_gap", "m6_sufficiency"))]
ROAR_FIELDS = ["stage", "dataset", "model", "seed", "explainer", "failed", "m7_roar"]
SYNTH_EXTRA = ["spearman_truth"]
UNDECIDED = "UNDECIDED"


class ValidationError(RuntimeError):
    """The frozen data do not have the structure the analysis needs."""


# --- 1. loading ------------------------------------------------------------------------------

def load_spec(path: Path = SPEC_PATH) -> dict:
    with open(path, "rb") as fh:
        return tomllib.load(fh)


def read_manifest(raw: Path = RAW) -> list[dict]:
    with open(raw / "MANIFEST.csv", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def check_manifest(rows: list[dict], raw: Path = RAW, expected: dict[str, set[str]] | None = None) -> dict:
    """Every manifest file exists with its SHA-256; no duplicate; coverage as expected."""
    problems = []
    paths = [r["path"] for r in rows]
    if len(paths) != len(set(paths)):
        problems.append(f"duplicate manifest paths: {len(paths) - len(set(paths))}")
    for r in rows:
        p = raw / r["path"]
        if not p.exists():
            problems.append(f"missing: {r['path']}")
        elif hashlib.sha256(p.read_bytes()).hexdigest() != r["sha256"]:
            problems.append(f"hash mismatch: {r['path']}")
    if expected is not None:
        for stage, want in expected.items():
            got = {p for p in paths if p.startswith(stage + "/")}
            if got != want:
                problems.append(f"{stage}: {len(want - got)} missing, {len(got - want)} unexpected")
    if problems:
        raise ValidationError("; ".join(problems[:20]))
    return {"manifest_rows": len(rows)}


def expected_shards(cfg: dict) -> dict[str, set[str]]:
    import paper_g_run as run
    return {st: {f"{st}/{run.shard_name(sh)}.jsonl.gz" for sh in run.shards(st, cfg)}
            for st in ("pilot", *STAGES)}


def load_stage(stage: str, rows: list[dict], raw: Path = RAW) -> pd.DataFrame:
    """The records of one stage, without attribution vectors."""
    keep = {"full": INSTANCE_FIELDS, "roar": ROAR_FIELDS,
            "synthetic": INSTANCE_FIELDS + SYNTH_EXTRA}[stage]
    recs = []
    for r in sorted(rows, key=lambda r: r["path"]):
        if not r["path"].startswith(stage + "/"):
            continue
        with gzip.open(raw / r["path"], "rt", encoding="utf-8") as fh:
            for line in fh:
                x = json.loads(line)
                recs.append({k: x.get(k) for k in keep})
    return pd.DataFrame.from_records(recs, columns=keep)


# --- 2. structural validation ----------------------------------------------------------------

def validate(full: pd.DataFrame, roar: pd.DataFrame, synth: pd.DataFrame, cfg: dict,
             spec: dict) -> dict:
    """Counts, keys, alignment and directions. Raises ValidationError; returns counts only."""
    problems = []
    if set(spec["h1"]["metrics"]) != set(lib.HIGHER_IS_BETTER):
        problems.append("H1 metrics differ from the metrics with a direction")
    n_ds, n_seed = len(cfg["dataset"]), len(cfg["seeds"])
    n_exp, n_inst = len(lib.EXPLAINERS), cfg["n_instances"]
    for name, df, inst in (("full", full, n_inst), ("synthetic", synth, cfg["synthetic"]["n_instances"])):
        missing = [c for c in (INSTANCE_FIELDS if name == "full" else INSTANCE_FIELDS + SYNTH_EXTRA)
                   if c not in df.columns or df[c].isna().all()]
        if missing:
            problems.append(f"{name}: missing columns {missing}")
            continue
        if df.duplicated(BLOCK + ["explainer", "instance"]).any():
            problems.append(f"{name}: duplicate (block, explainer, instance) keys")
        if (df["failed"] != 0).any():
            problems.append(f"{name}: {int((df['failed'] != 0).sum())} failed rows")
        for key, g in df.groupby(BLOCK):
            sets = [frozenset(s) for _, s in g.groupby("explainer")["instance"]]
            if len(sets) != n_exp or len(set(sets)) != 1 or len(sets[0]) != inst:
                problems.append(f"{name} {key}: explainers do not share {inst} instances")
                break
    if len(full) != n_ds * len(lib.MODELS) * n_seed * n_exp * n_inst:
        problems.append(f"full: {len(full)} rows")
    n_syn = len(cfg["synthetic"]["generators"]) * len(cfg["synthetic"]["correlation"]) * n_seed
    if len(synth) != n_syn * n_exp * cfg["synthetic"]["n_instances"]:
        problems.append(f"synthetic: {len(synth)} rows")
    if len(roar) != n_ds * len(lib.MODELS) * n_seed * n_exp or roar.duplicated(BLOCK + ["explainer"]).any():
        problems.append(f"roar: {len(roar)} rows or duplicate keys")
    full_blocks = set(map(tuple, full[BLOCK + ["explainer"]].drop_duplicates().to_numpy()))
    roar_blocks = set(map(tuple, roar[BLOCK + ["explainer"]].to_numpy()))
    if full_blocks != roar_blocks:
        problems.append("roar blocks do not match full blocks")
    if problems:
        raise ValidationError("; ".join(problems))
    return {"full_rows": len(full), "roar_rows": len(roar), "synthetic_rows": len(synth),
            "full_blocks": full[BLOCK].drop_duplicates().shape[0],
            "m4_degenerate_rows": int(full["m4_degenerate"].astype(bool).sum())}


# --- 3. orientation ------------------------------------------------------------------------

def oriented(values: np.ndarray | pd.Series, metric: str) -> np.ndarray | pd.Series:
    """Higher is more faithful after orientation (plan section 3, 11.9). `_b2` keeps its metric's direction."""
    base = metric.removesuffix("_b2")
    return values if lib.HIGHER_IS_BETTER[base] else -values


# --- 4. aggregation ------------------------------------------------------------------------

def block_means(df: pd.DataFrame, columns: list[str], exclude_degenerate_m4: bool = False) -> pd.DataFrame:
    """Mean of each metric over the instances of a block and explainer (one row per explainer)."""
    d = df.copy()
    if exclude_degenerate_m4 and "m4_corr" in columns:
        d.loc[d["m4_degenerate"].astype(bool), "m4_corr"] = np.nan    # missing, never 0 (11.4)
    g = d.groupby(BLOCK + ["explainer"])[columns]
    means = g.mean()            # NaN-skipping; all-NaN gives NaN (a missing aggregate)
    return means.reset_index()


def system_table(full_means: pd.DataFrame, roar: pd.DataFrame) -> pd.DataFrame:
    """M1-M6 block means joined with the block's ROAR-lite value (M7, system level only)."""
    m7 = roar[BLOCK + ["explainer", "m7_roar"]]
    out = full_means.merge(m7, on=BLOCK + ["explainer"], how="left", validate="one_to_one")
    if out["m7_roar"].isna().any():
        raise ValidationError("M7 missing for some block")
    return out


# --- 5. ranking ----------------------------------------------------------------------------

def ranks_desc(values: np.ndarray) -> np.ndarray:
    """Average ranks, 1 = highest (most faithful after orientation). NaN in, NaN out."""
    v = np.asarray(values, dtype=float)
    if np.isnan(v).any():
        return np.full(v.shape, np.nan)
    return stats.rankdata(-v, method="average")


def rank_matrix(sys_block: pd.DataFrame, explainers: list[str], metrics: list[str]) -> np.ndarray:
    """Raters (metrics) x items (explainers) of ranks; a rater with a missing value is all-NaN."""
    b = sys_block.set_index("explainer").loc[explainers]
    return np.vstack([ranks_desc(oriented(b[m].to_numpy(dtype=float), m)) for m in metrics])


# --- 6. agreement statistics -------------------------------------------------------------------

def spearman_of_ranks(r1: np.ndarray, r2: np.ndarray) -> float:
    """Pearson correlation of two rank vectors; NaN (undefined) if either is constant or missing."""
    a, b = np.asarray(r1, float), np.asarray(r2, float)
    if np.isnan(a).any() or np.isnan(b).any():
        return math.nan
    a, b = a - a.mean(), b - b.mean()
    den = math.sqrt(float(a @ a) * float(b @ b))
    return math.nan if den < 1e-12 else float(a @ b) / den


def kendall_w(R: np.ndarray) -> float:
    """Tie-corrected Kendall's W of an m x n rank matrix (complete rows only); NaN if undefined."""
    R = np.asarray(R, float)
    R = R[~np.isnan(R).any(axis=1)]
    m, n = R.shape if R.ndim == 2 else (0, 0)
    if m < 2 or n < 2:
        return math.nan
    s = float(((R.sum(axis=0) - m * (n + 1) / 2) ** 2).sum())
    ties = 0.0
    for row in R:
        _, counts = np.unique(row, return_counts=True)
        ties += float((counts ** 3 - counts).sum())
    den = m ** 2 * (n ** 3 - n) - m * ties
    return math.nan if den <= 0 else 12 * s / den


def mean_pairwise_spearman(R: np.ndarray, pair_items: dict | None = None) -> tuple[float, int, int]:
    """Mean of the defined rater-pair Spearman correlations: (mean, defined, undefined).

    `pair_items` maps a pair (j, k) to the item columns it uses (the pairwise-available variant).
    """
    vals, undefined = [], 0
    for j, k in itertools.combinations(range(R.shape[0]), 2):
        cols = pair_items.get((j, k), slice(None)) if pair_items else slice(None)
        r = spearman_of_ranks(R[j, cols], R[k, cols])
        if math.isnan(r):
            undefined += 1
        else:
            vals.append(r)
    return (float(np.mean(vals)) if vals else math.nan), len(vals), undefined


# --- 7. dataset-level inference ---------------------------------------------------------------

def t_interval(values, conf: float = 0.95) -> dict:
    v = np.asarray([x for x in values if not math.isnan(x)], float)
    n = len(v)
    out = {"n": n, "mean": float(v.mean()) if n else math.nan, "sd": math.nan,
           "lo": math.nan, "hi": math.nan, "df": n - 1}
    if n >= 2:
        sd = float(v.std(ddof=1))
        h = stats.t.ppf(0.5 + conf / 2, n - 1) * sd / math.sqrt(n)
        out.update(sd=sd, lo=out["mean"] - h, hi=out["mean"] + h)
    return out


def t_test_greater(values, mu0: float = 0.0) -> float:
    """One-sided one-sample t-test p for mean > mu0."""
    v = np.asarray([x for x in values if not math.isnan(x)], float)
    if len(v) < 2 or v.std(ddof=1) == 0:
        return math.nan
    return float(stats.ttest_1samp(v, mu0, alternative="greater").pvalue)


def sign_flip_p(values) -> float:
    """Exact sign-flip p (all 2^n assignments) for mean > 0; assumes symmetry about 0 under H0."""
    v = np.asarray([x for x in values if not math.isnan(x)], float)
    obs = v.mean()
    signs = np.array(list(itertools.product([1.0, -1.0], repeat=len(v))))
    return float(np.mean((signs * v).mean(axis=1) >= obs - 1e-12))


def bootstrap_ci(values, b: int, seed: int, conf: float = 0.95) -> tuple[float, float]:
    """Percentile bootstrap over datasets (sensitivity only, 11.5)."""
    v = np.asarray([x for x in values if not math.isnan(x)], float)
    rng = np.random.default_rng(seed)
    means = v[rng.integers(0, len(v), size=(b, len(v)))].mean(axis=1)
    return float(np.quantile(means, (1 - conf) / 2)), float(np.quantile(means, (1 + conf) / 2))


# --- 8. permutation testing ----------------------------------------------------------------

def _perms(n: int) -> np.ndarray:
    return np.array(list(itertools.permutations(range(n))))


def permutation_contributions(R_by_dataset: dict[str, np.ndarray]) -> tuple[list, np.ndarray]:
    """For each dataset, C[j, k, rho]: its contribution to the statistic when rater k's labels
    are permuted by rho relative to rater j's. The statistic (mean over datasets of the
    dataset mean of the block mean pairwise Spearman) is a sum of these, because undefined
    pairs stay undefined under any relabelling (a constant vector stays constant)."""
    contribs = []
    n = next(iter(R_by_dataset.values())).shape[2]
    perms = _perms(n)
    for d, R in R_by_dataset.items():            # R: blocks x raters x items
        B, m, _ = R.shape
        z = R - np.nanmean(R, axis=2, keepdims=True)
        norm = np.sqrt(np.nansum(z ** 2, axis=2))
        ok = (~np.isnan(R).any(axis=2)) & (norm > 1e-12)
        z = np.where(ok[..., None], z / np.where(norm > 1e-12, norm, 1)[..., None], 0.0)
        pairs = list(itertools.combinations(range(m), 2))
        defined = np.array([[ok[b, j] and ok[b, k] for j, k in pairs] for b in range(B)])
        n_def = defined.sum(axis=1)
        used = n_def > 0
        if not used.any():
            raise ValidationError(f"{d}: no block with a defined pair")
        w = np.where(used, 1.0 / np.maximum(n_def, 1), 0.0) / used.sum()
        C = np.zeros((m, m, len(perms)))
        for p_idx, (j, k) in enumerate(pairs):
            wb = w * defined[:, p_idx]
            for r_idx, rho in enumerate(perms):
                C[j, k, r_idx] = float((wb * (z[:, j, :] * z[:, k, rho]).sum(axis=1)).sum())
        contribs.append(C)
    return contribs, perms


def _compose_table(perms: np.ndarray) -> np.ndarray:
    """comp[a, b] = index of rho with z_j[pi_a] . z_k[pi_b] = z_j . z_k[rho]."""
    index = {tuple(p): i for i, p in enumerate(perms)}
    inv = [np.argsort(p) for p in perms]
    return np.array([[index[tuple(pb[inv[a]])] for pb in perms] for a in range(len(perms))])


def permutation_statistic(contribs: list, perms: np.ndarray, draws: np.ndarray) -> np.ndarray:
    """Statistic for each draw; draws: (n_draws, n_datasets, n_raters) permutation indices."""
    comp = _compose_table(perms)
    total = np.zeros(draws.shape[0])
    for d, C in enumerate(contribs):
        m = C.shape[0]
        for j, k in itertools.combinations(range(m), 2):
            total += C[j, k, comp[draws[:, d, j], draws[:, d, k]]]
    return total / len(contribs)


def h1_permutation_test(R_by_dataset: dict[str, np.ndarray], n_perm: int, seed: int,
                        batch: int = 20000) -> dict:
    """Dataset as the unit: one relabelling per dataset and rater, shared by its blocks (4.5)."""
    contribs, perms = permutation_contributions(R_by_dataset)
    m = contribs[0].shape[0]
    identity = np.zeros((1, len(contribs), m), dtype=int)
    obs = float(permutation_statistic(contribs, perms, identity)[0])
    rng = np.random.default_rng(seed)
    ge, done = 0, 0
    while done < n_perm:
        k = min(batch, n_perm - done)
        draws = rng.integers(0, len(perms), size=(k, len(contribs), m))
        ge += int((permutation_statistic(contribs, perms, draws) >= obs - 1e-12).sum())
        done += k
    return {"statistic": obs, "p": (1 + ge) / (1 + n_perm), "permutations": n_perm, "seed": seed}


def exact_permutation_p(R_by_dataset: dict[str, np.ndarray]) -> float:
    """Full enumeration of the relabellings (small cases; used to check the Monte Carlo test)."""
    contribs, perms = permutation_contributions(R_by_dataset)
    m, D = contribs[0].shape[0], len(contribs)
    grid = np.array(list(itertools.product(range(len(perms)), repeat=D * m))).reshape(-1, D, m)
    obs = permutation_statistic(contribs, perms, np.zeros((1, D, m), dtype=int))[0]
    return float(np.mean(permutation_statistic(contribs, perms, grid) >= obs - 1e-12))


# --- 9. multiplicity -------------------------------------------------------------------------

def holm(pvals: list[float]) -> list[float]:
    """Holm step-down adjusted p-values (monotone, capped at 1); NaN stays NaN."""
    idx = [i for i, p in enumerate(pvals) if not math.isnan(p)]
    order = sorted(idx, key=lambda i: pvals[i])
    adj, running = [math.nan] * len(pvals), 0.0
    for rank, i in enumerate(order):
        running = max(running, (len(order) - rank) * pvals[i])
        adj[i] = min(1.0, running)
    return adj


# --- H1 --------------------------------------------------------------------------------------

def h1_blocks(sys_tab: pd.DataFrame, explainers: list[str], metrics: list[str],
              pair_items: dict | None = None) -> tuple[pd.DataFrame, dict[str, np.ndarray]]:
    rows, by_ds = [], {}
    for key, g in sys_tab.groupby(BLOCK):
        R = rank_matrix(g, explainers, metrics)
        mps, n_def, n_undef = mean_pairwise_spearman(R, pair_items)
        rows.append({**dict(zip(BLOCK, key)), "kendall_w": math.nan if pair_items else kendall_w(R),
                     "mean_pairwise_spearman": mps, "pairs_defined": n_def, "pairs_undefined": n_undef,
                     "raters_missing": int(np.isnan(R).any(axis=1).sum())})
        by_ds.setdefault(key[0], []).append(R)
    return pd.DataFrame(rows), {d: np.stack(v) for d, v in sorted(by_ds.items())}


def dataset_means(blocks: pd.DataFrame, column: str) -> pd.DataFrame:
    g = blocks.groupby("dataset")[column]
    return pd.DataFrame({"mean": g.mean(), "blocks_defined": g.count(), "blocks": g.size()}).reset_index()


def h1_analysis(sys_tab: pd.DataFrame, explainers: list[str], metrics: list[str], spec: dict,
                test: bool = True, pair_items: dict | None = None) -> dict:
    blocks, R_by = h1_blocks(sys_tab, explainers, metrics, pair_items)
    ds_s = dataset_means(blocks, "mean_pairwise_spearman")
    ds_w = dataset_means(blocks, "kendall_w")
    out = {"blocks": blocks, "datasets_spearman": ds_s, "datasets_w": ds_w,
           "spearman": t_interval(ds_s["mean"]), "w": t_interval(ds_w["mean"])}
    if test and not pair_items:
        out["permutation"] = h1_permutation_test(R_by, spec["h1"]["permutations"], spec["h1"]["permutation_seed"])
    return out


def decision(p: float, lo: float, hi: float, alpha: float, threshold: float) -> str:
    """The frozen decision table of section 4.4."""
    if math.isnan(p) or p >= alpha:
        return "no evidence that the metrics share an order"
    if lo > threshold:
        return "the metrics broadly agree"
    if hi < threshold:
        return "the metrics agree only weakly"
    return "agreement present, strength not determined"


def stability_benchmark(sys_tab: pd.DataFrame, explainers: list[str], metrics: list[str]) -> dict:
    """Within-metric stability across seeds (11.3): 10 seed pairs per dataset x model x metric."""
    rows = []
    for (d, mdl), g in sys_tab.groupby(["dataset", "model"]):
        for m in metrics:
            ranks = {s: ranks_desc(oriented(gs.set_index("explainer").loc[explainers, m].to_numpy(float), m))
                     for s, gs in g.groupby("seed")}
            vals = [spearman_of_ranks(ranks[a], ranks[b]) for a, b in itertools.combinations(sorted(ranks), 2)]
            ok = [v for v in vals if not math.isnan(v)]
            rows.append({"dataset": d, "model": mdl, "metric": m, "seed_pairs": len(vals),
                         "undefined": len(vals) - len(ok), "mean": float(np.mean(ok)) if ok else math.nan})
    cell = pd.DataFrame(rows)
    by_metric = cell.groupby(["dataset", "metric"])["mean"].mean().reset_index()
    by_ds = by_metric.groupby("dataset")["mean"].mean().reset_index()
    return {"cells": cell, "dataset_metric": by_metric, "datasets": by_ds, "summary": t_interval(by_ds["mean"])}


# --- H2 --------------------------------------------------------------------------------------

def h2_blocks(full: pd.DataFrame, explainers: list[str], metrics: list[str],
              exclude_degenerate_m4: bool = False) -> pd.DataFrame:
    """15 pairwise Spearman correlations across the instances of each block (oriented metrics)."""
    rows = []
    pairs = list(itertools.combinations(metrics, 2))
    for key, g in full[full["explainer"].isin(explainers)].groupby(BLOCK + ["explainer"]):
        g = g.sort_values("instance")
        degen = g["m4_degenerate"].astype(bool).to_numpy()
        row = dict(zip(BLOCK + ["explainer"], key))
        for a, b in pairs:
            keep = ~degen if exclude_degenerate_m4 and "m4_corr" in (a, b) else np.ones(len(g), bool)
            x = oriented(g[a].to_numpy(float), a)[keep]
            y = oriented(g[b].to_numpy(float), b)[keep]
            row[f"{a}|{b}"] = spearman_of_ranks(stats.rankdata(x), stats.rankdata(y)) if len(x) > 2 else math.nan
            row[f"n|{a}|{b}"] = int(keep.sum())
        rows.append(row)
    out = pd.DataFrame(rows)
    out["omnibus"] = out[[f"{a}|{b}" for a, b in pairs]].mean(axis=1, skipna=True)
    return out


def h2_analysis(full: pd.DataFrame, explainers: list[str], metrics: list[str], spec: dict,
                exclude_degenerate_m4: bool = False) -> dict:
    blocks = h2_blocks(full, explainers, metrics, exclude_degenerate_m4)
    pairs = [f"{a}|{b}" for a, b in itertools.combinations(metrics, 2)]
    ds = blocks.groupby("dataset")[["omnibus", *pairs]].mean().reset_index()
    b, seed = spec["h2"]["bootstrap"], spec["h2"]["bootstrap_seed"]
    omni = {**t_interval(ds["omnibus"]), "p_t": t_test_greater(ds["omnibus"]),
            "p_sign_flip": sign_flip_p(ds["omnibus"]),
            "boot_lo": bootstrap_ci(ds["omnibus"], b, seed)[0], "boot_hi": bootstrap_ci(ds["omnibus"], b, seed)[1]}
    prow = []
    for p in pairs:
        ti = t_interval(ds[p])
        lo, hi = bootstrap_ci(ds[p], b, seed)
        prow.append({"pair": p, **ti, "p_t": t_test_greater(ds[p]), "boot_lo": lo, "boot_hi": hi,
                     "undefined_blocks": int(blocks[p].isna().sum())})
    ptab = pd.DataFrame(prow)
    ptab["p_holm15"] = holm(ptab["p_t"].tolist())
    return {"blocks": blocks, "datasets": ds, "omnibus": omni, "pairs": ptab}


def matrix_from_pairs(ptab: pd.DataFrame, metrics: list[str]) -> pd.DataFrame:
    M = pd.DataFrame(np.eye(len(metrics)), index=metrics, columns=metrics)
    for _, r in ptab.iterrows():
        a, b = r["pair"].split("|")
        M.loc[a, b] = M.loc[b, a] = r["mean"]
    return M


# --- 10. secondary and sensitivity analyses -----------------------------------------------------

def winner_flips(sys_tab: pd.DataFrame, explainers: list[str], metrics: list[str]) -> pd.DataFrame:
    rows = []
    blocks = list(sys_tab.groupby(BLOCK))
    for a, b in itertools.combinations(metrics, 2):
        flip = tie = 0
        for _, g in blocks:
            R = rank_matrix(g, explainers, [a, b])
            tops = []
            for r in R:
                best = np.flatnonzero(r == np.nanmin(r))
                tops.append(None if len(best) != 1 else int(best[0]))
            if None in tops:
                tie += 1
            elif tops[0] != tops[1]:
                flip += 1
        rows.append({"metric_a": a, "metric_b": b, "blocks": len(blocks), "flips": flip, "ties": tie,
                     "flip_share": flip / len(blocks), "tie_share": tie / len(blocks)})
    return pd.DataFrame(rows)


def shap_lime_reversals(sys_tab: pd.DataFrame, metrics: list[str]) -> tuple[pd.DataFrame, dict]:
    signs = {}
    for key, g in sys_tab.groupby(BLOCK):
        b = g.set_index("explainer")
        signs[key] = {m: float(np.sign(oriented(b.loc["shap", m], m) - oriented(b.loc["lime", m], m)))
                      for m in metrics}
    rows, any_rev = [], 0
    for key, s in signs.items():
        vals = [v for v in s.values() if v != 0]
        any_rev += int(1.0 in vals and -1.0 in vals)
    n = len(signs)
    for a, b in itertools.combinations(metrics, 2):
        strict = sum(1 for s in signs.values() if s[a] * s[b] == -1)
        ties = sum(1 for s in signs.values() if s[a] == 0 or s[b] == 0)
        rows.append({"metric_a": a, "metric_b": b, "blocks": n, "strict_reversals": strict,
                     "tie_involved": ties, "reversal_share": strict / n, "tie_share": ties / n})
    return pd.DataFrame(rows), {"blocks": n, "blocks_with_any_strict_reversal": any_rev,
                                "share": any_rev / n}


def degenerate_counts(full: pd.DataFrame) -> dict[str, pd.DataFrame]:
    f = full.assign(deg=full["m4_degenerate"].astype(bool))
    return {k: f.groupby(k)["deg"].agg(degenerate="sum", rows="size").reset_index()
            for k in ("dataset", "model", "explainer")}


def circularity_pair_items(metrics: list[str], explainers: list[str]) -> dict:
    """Pairwise-available variant (11.8, O2): pairs with M4 use the items other than Occlusion."""
    j4, keep = metrics.index("m4_corr"), [i for i, e in enumerate(explainers) if e != "occlusion"]
    return {tuple(sorted((j4, k))): keep for k in range(len(metrics)) if k != j4}


# --- 11. synthetic ground-truth check ----------------------------------------------------------

def synthetic_agreement(synth: pd.DataFrame, explainers: list[str], metrics: list[str]) -> dict:
    """11.6: per condition x seed, Spearman of each metric's explainer order with the reference."""
    rows, refs = [], []
    s = synth[synth["explainer"].isin(explainers)]
    for (cond, seed), g in s.groupby(["dataset", "seed"]):
        means = g.groupby("explainer")[["spearman_truth", *metrics]].mean().loc[explainers]
        ref = ranks_desc(means["spearman_truth"].to_numpy(float))
        refs.append({"condition": cond, "seed": seed,
                     **{f"rank_{e}": r for e, r in zip(explainers, ref)}})
        for m in metrics:
            r = ranks_desc(oriented(means[m].to_numpy(float), m))
            rows.append({"condition": cond, "seed": seed, "metric": m,
                         "spearman_with_reference": spearman_of_ranks(r, ref)})
    blocks = pd.DataFrame(rows)
    by_metric = blocks.groupby("metric")["spearman_with_reference"].agg(
        mean="mean", defined="count", blocks="size").reset_index()
    by_cond = blocks.groupby(["condition", "metric"])["spearman_with_reference"].mean().reset_index()
    return {"blocks": blocks, "reference": pd.DataFrame(refs), "by_metric": by_metric, "by_condition": by_cond}


# --- 12. outputs and report -----------------------------------------------------------------------

def _csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, float_format="%.6f", lineterminator="\n")


def _summary_frame(d: dict, label: str) -> pd.DataFrame:
    return pd.DataFrame([{"analysis": label, **d}])


def check_spec_decided(spec: dict) -> list[str]:
    open_items = [k for k in ("h1_decision_p", "circularity_variant") if spec["h1"].get(k) == UNDECIDED]
    if spec["h1"].get("h1_decision_p") not in (UNDECIDED, "raw", "holm"):
        open_items.append("h1_decision_p must be raw or holm")
    if spec["h1"].get("circularity_variant") not in (UNDECIDED, "drop_m4_rater", "pairwise_available"):
        open_items.append("circularity_variant must be drop_m4_rater or pairwise_available")
    return open_items


def run_analysis(full: pd.DataFrame, roar: pd.DataFrame, synth: pd.DataFrame, spec: dict,
                 out: Path, report: Path, header: dict) -> dict:
    """Every analysis of the plan and section 11; writes CSVs, figures and the report."""
    h1s = spec["h1"]
    studied, allx = h1s["studied"], [*h1s["studied"], h1s["control"]]
    m7, m6 = h1s["metrics"], spec["h2"]["metrics"]
    sys_tab = system_table(block_means(full, list(lib.INSTANCE_METRICS)), roar)
    res: dict = {"header": header}

    # Confirmatory: H1 (studied, 7 raters) and H2 (4 explainers, 6 metrics).
    h1 = h1_analysis(sys_tab, studied, m7, spec)
    h2 = h2_analysis(full, spec["h2"]["explainers"], m6, spec)
    raw_p = [h1["permutation"]["p"], h2["omnibus"]["p_t"]]
    adj = holm(raw_p)
    mult = pd.DataFrame([{"hypothesis": "H1", "test": "dataset-level permutation", "p_raw": raw_p[0], "p_holm": adj[0]},
                         {"hypothesis": "H2", "test": "one-sided t on dataset means", "p_raw": raw_p[1], "p_holm": adj[1]}])
    p_for_table = raw_p[0] if h1s["h1_decision_p"] == "raw" else adj[0]
    dec = decision(p_for_table, h1["spearman"]["lo"], h1["spearman"]["hi"], h1s["alpha"], h1s["threshold"])
    stab = stability_benchmark(sys_tab, studied, m7)
    c = out / "confirmatory"
    _csv(h1["blocks"], c / "h1_blocks.csv")
    _csv(h1["datasets_spearman"], c / "h1_datasets_spearman.csv")
    _csv(h1["datasets_w"], c / "h1_datasets_kendall_w.csv")
    _csv(pd.concat([_summary_frame(h1["spearman"], "mean pairwise Spearman"),
                    _summary_frame(h1["w"], "Kendall W")]), c / "h1_summary.csv")
    _csv(_summary_frame(h1["permutation"], "H1 permutation"), c / "h1_permutation.csv")
    _csv(stab["cells"], c / "stability_cells.csv")
    _csv(stab["dataset_metric"], c / "stability_dataset_metric.csv")
    _csv(stab["datasets"], c / "stability_datasets.csv")
    _csv(_summary_frame(stab["summary"], "within-metric stability"), c / "stability_summary.csv")
    _csv(h2["blocks"], c / "h2_blocks.csv")
    _csv(h2["datasets"], c / "h2_datasets.csv")
    _csv(_summary_frame(h2["omnibus"], "H2 omnibus"), c / "h2_omnibus.csv")
    _csv(h2["pairs"], c / "h2_pairs.csv")
    _csv(matrix_from_pairs(h2["pairs"], m6).reset_index(names="metric"), c / "h2_matrix.csv")
    _csv(mult, c / "multiplicity_h1_h2.csv")
    _csv(pd.DataFrame([{"h1_decision_p": h1s["h1_decision_p"], "p_used": p_for_table,
                        "interval_lo": h1["spearman"]["lo"], "interval_hi": h1["spearman"]["hi"],
                        "threshold": h1s["threshold"], "decision": dec}]), c / "h1_decision.csv")

    # Planned sensitivity and secondary analyses.
    s = out / "sensitivity"
    h1_4 = h1_analysis(sys_tab, allx, m7, spec)
    sys_b2 = system_table(block_means(full, [spec["baseline2"]["substitute"].get(m, m) for m in lib.INSTANCE_METRICS]
                                      ).rename(columns={v: k for k, v in spec["baseline2"]["substitute"].items()}), roar)
    h1_b2 = h1_analysis(sys_b2, studied, m7, spec)
    var = h1s["circularity_variant"]
    if var == "drop_m4_rater":
        h1_circ = h1_analysis(sys_tab, studied, [m for m in m7 if m != "m4_corr"], spec)
    else:
        h1_circ = h1_analysis(sys_tab, studied, m7, spec, test=False,
                              pair_items=circularity_pair_items(m7, studied))
    h2_3 = h2_analysis(full, studied, m6, spec)
    sens = []
    for label, r in (("H1 four explainers", h1_4), ("H1 second baseline", h1_b2), (f"H1 circularity ({var})", h1_circ)):
        sens.append({"analysis": label, **{f"spearman_{k}": v for k, v in r["spearman"].items()},
                     **{f"w_{k}": v for k, v in r["w"].items()}, "p_permutation": r.get("permutation", {}).get("p", math.nan)})
        _csv(r["datasets_spearman"], s / f"{label.lower().replace(' ', '_').replace('(', '').replace(')', '')}_datasets.csv")
    _csv(pd.DataFrame(sens), s / "h1_sensitivity.csv")
    _csv(pd.concat([_summary_frame({k: v for k, v in h2_3["omnibus"].items()}, "H2 three studied explainers"),
                    _summary_frame({"mean": h2["omnibus"]["mean"], "lo": h2["omnibus"]["boot_lo"],
                                    "hi": h2["omnibus"]["boot_hi"]}, "H2 bootstrap interval")]), s / "h2_sensitivity.csv")
    _csv(h2_3["pairs"], s / "h2_pairs_three_explainers.csv")
    wf = winner_flips(sys_tab, studied, m7)
    sl, sl_any = shap_lime_reversals(sys_tab, m7)
    _csv(wf, s / "winner_flips.csv")
    _csv(sl, s / "shap_lime_reversals.csv")
    _csv(pd.DataFrame([sl_any]), s / "shap_lime_any_reversal.csv")
    per_model = []
    for mdl in lib.MODELS:
        a = h1_analysis(sys_tab[sys_tab["model"] == mdl], studied, m7, spec, test=False)
        b = h2_blocks(full[full["model"] == mdl], spec["h2"]["explainers"], m6).groupby("dataset")["omnibus"].mean()
        per_model.append({"model": mdl, **{f"h1_{k}": v for k, v in a["spearman"].items()},
                          **{f"h2_{k}": v for k, v in t_interval(b).items()}})
    _csv(pd.DataFrame(per_model), s / "per_model.csv")

    # Exploratory: degenerate M4 excluded (11.4).
    e = out / "exploratory"
    for k, df in degenerate_counts(full).items():
        _csv(df, e / f"m4_degenerate_by_{k}.csv")
    sys_x = system_table(block_means(full, list(lib.INSTANCE_METRICS), exclude_degenerate_m4=True), roar)
    h1_x = h1_analysis(sys_x, studied, m7, spec)
    h2_x = h2_analysis(full, spec["h2"]["explainers"], m6, spec, exclude_degenerate_m4=True)
    _csv(h1_x["blocks"], e / "h1_m4_excluded_blocks.csv")
    _csv(_summary_frame({**h1_x["spearman"], "p_permutation": h1_x["permutation"]["p"]}, "H1 M4 degenerate excluded"),
         e / "h1_m4_excluded.csv")
    _csv(h2_x["pairs"], e / "h2_m4_excluded_pairs.csv")
    _csv(h2_x["blocks"][[c_ for c_ in h2_x["blocks"].columns if c_.startswith("n|")] + BLOCK + ["explainer"]],
         e / "h2_m4_excluded_counts.csv")

    # Synthetic ground-truth check (11.6).
    y = out / "synthetic"
    syn4 = synthetic_agreement(synth, allx, m6)
    syn3 = synthetic_agreement(synth, studied, m6)
    for name, r in (("four", syn4), ("three_sensitivity", syn3)):
        for k in ("blocks", "reference", "by_metric", "by_condition"):
            _csv(r[k], y / f"{name}_{k}.csv")

    res.update(h1=h1, h2=h2, mult=mult, decision=dec, p_for_table=p_for_table, stability=stab,
               h1_4=h1_4, h1_b2=h1_b2, h1_circ=h1_circ, h2_3=h2_3, flips=wf, shap_lime=sl, sl_any=sl_any,
               per_model=pd.DataFrame(per_model), h1_x=h1_x, h2_x=h2_x, syn4=syn4, syn3=syn3, spec=spec)
    write_figures(res, out / "figures")
    write_report(res, report)
    return res


def write_figures(res: dict, fig_dir: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"svg.hashsalt": "paper-g", "svg.fonttype": "none", "font.size": 9})
    fig_dir.mkdir(parents=True, exist_ok=True)
    meta = {"Date": None, "Creator": "scripts/paper_g_analyze.py"}

    ds = res["h1"]["datasets_spearman"]
    st = res["stability"]["datasets"].set_index("dataset")["mean"]
    fig, ax = plt.subplots(figsize=(6, 3.2))
    x = np.arange(len(ds))
    ax.bar(x - 0.2, ds["mean"], 0.4, label="between metrics (H1)")
    ax.bar(x + 0.2, st.loc[ds["dataset"]].to_numpy(), 0.4, label="within-metric stability")
    ax.axhline(res["spec"]["h1"]["threshold"], color="k", lw=0.8, ls="--")
    ax.set_xticks(x, ds["dataset"], rotation=30, ha="right")
    ax.set_ylabel("mean pairwise Spearman")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(fig_dir / "fig_g1_h1_datasets.svg", metadata=meta)
    plt.close(fig)

    M = matrix_from_pairs(res["h2"]["pairs"], res["spec"]["h2"]["metrics"])
    fig, ax = plt.subplots(figsize=(4.2, 3.6))
    im = ax.imshow(M.to_numpy(), vmin=-1, vmax=1, cmap="RdBu_r")
    labels = [m.split("_")[0].upper() for m in M.index]
    ax.set_xticks(range(len(labels)), labels)
    ax.set_yticks(range(len(labels)), labels)
    fig.colorbar(im, ax=ax, label="mean Spearman (dataset level)")
    fig.tight_layout()
    fig.savefig(fig_dir / "fig_g2_h2_matrix.svg", metadata=meta)
    plt.close(fig)

    bm = res["syn4"]["by_metric"]
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar([m.split("_")[0].upper() for m in bm["metric"]], bm["mean"])
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("Spearman with reference order")
    fig.tight_layout()
    fig.savefig(fig_dir / "fig_g3_synthetic.svg", metadata=meta)
    plt.close(fig)


def _f(x, nd: int = 3) -> str:
    return "—" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{nd}f}"


def _md(df: pd.DataFrame, nd: int = 3) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(_f(v, nd) if isinstance(v, float) else str(v) for v in r) + " |")
    return "\n".join(lines)


def write_report(res: dict, path: Path) -> None:
    """RESULTS_REPORT.md: numbered tables and figures, confirmatory first, generated only."""
    h1, h2, sp = res["h1"], res["h2"], res["spec"]
    L = ["# Paper G — Results report", "",
         "Generated by `scripts/paper_g_analyze.py`; do not edit by hand. Plan: "
         "`ANALYSIS_PLAN.md` sections 4 and 11.", ""]
    L += [f"- {k}: {v}" for k, v in res["header"].items()]
    L += ["", "## 1. Confirmatory analyses", "",
          "**Table R1. H1: agreement between seven metrics on the order of the three studied explainers "
          "(dataset level, n = 8).**", "",
          _md(pd.DataFrame([{"measure": "mean pairwise Spearman", **{k: h1["spearman"][k] for k in ("mean", "lo", "hi", "n")}},
                            {"measure": "Kendall W", **{k: h1["w"][k] for k in ("mean", "lo", "hi", "n")}}])), "",
          f"Permutation test (dataset unit, {sp['h1']['permutations']:,} permutations, seed {sp['h1']['permutation_seed']}): "
          f"p = {_f(h1['permutation']['p'], 5)}.", "",
          "**Table R2. Holm correction over H1 and H2.**", "", _md(res["mult"], 5), "",
          f"Decision table (section 4.4) applied with the {sp['h1']['h1_decision_p']} p "
          f"({_f(res['p_for_table'], 5)}) and the t-interval: **{res['decision']}**.", "",
          "**Table R3. Within-metric stability benchmark (section 11.3), dataset level.**", "",
          _md(pd.DataFrame([{k: res["stability"]["summary"][k] for k in ("mean", "lo", "hi", "n")}])), "",
          "**Table R4. H2: instance-level agreement, omnibus (four explainers, dataset level).**", "",
          _md(pd.DataFrame([{k: h2["omnibus"][k] for k in ("mean", "lo", "hi", "n", "p_t", "p_sign_flip")}]), 5), "",
          "**Table R5. H2: the 15 metric pairs (dataset level; Holm over the 15).**", "",
          _md(h2["pairs"][["pair", "mean", "lo", "hi", "p_t", "p_holm15", "undefined_blocks"]], 4), "",
          "Figure R1: `analysis/figures/fig_g1_h1_datasets.svg`. Figure R2: `analysis/figures/fig_g2_h2_matrix.svg`.", "",
          "## 2. Sensitivity and secondary analyses (planned)", "",
          "**Table R6. H1 and H2 sensitivity.**", "", _md(_sens_table(res)), "",
          "**Table R7. Winner flips between metrics (studied explainers).**", "",
          _md(res["flips"][["metric_a", "metric_b", "flip_share", "tie_share"]]), "",
          "**Table R8. SHAP–LIME order reversals between metrics.**", "",
          _md(res["shap_lime"][["metric_a", "metric_b", "reversal_share", "tie_share"]]), "",
          f"Blocks with at least one strict SHAP–LIME reversal: {res['sl_any']['blocks_with_any_strict_reversal']} "
          f"of {res['sl_any']['blocks']}.", "",
          "**Table R9. Per model (descriptive).**", "",
          _md(res["per_model"][["model", "h1_mean", "h1_lo", "h1_hi", "h2_mean", "h2_lo", "h2_hi"]]), "",
          "## 3. Exploratory analyses (rule set after the run)", "",
          "**Table R10. Degenerate M4 rows excluded (section 11.4).**", "",
          _md(pd.DataFrame([{"analysis": "H1", **{k: res["h1_x"]["spearman"][k] for k in ("mean", "lo", "hi")}},
                            {"analysis": "H2 omnibus", **{k: res["h2_x"]["omnibus"][k] for k in ("mean", "lo", "hi")}}])), "",
          "## 4. Synthetic ground-truth check (descriptive, section 11.6)", "",
          "**Table R11. Agreement of each metric's explainer order with the reference order "
          "(four explainers; 20 condition × seed blocks).**", "", _md(res["syn4"]["by_metric"]), "",
          "Figure R3: `analysis/figures/fig_g3_synthetic.svg`.", "",
          "## 5. Not computed", "",
          "- Variance shares and the aligned rank transform (section 11.7): stopped pending a specification.", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L), encoding="utf-8")


def _sens_table(res: dict) -> pd.DataFrame:
    rows = []
    for label, r in (("four explainers", res["h1_4"]), ("second baseline", res["h1_b2"]),
                     (f"circularity ({res['spec']['h1']['circularity_variant']})", res["h1_circ"])):
        rows.append({"analysis": label, "mean": r["spearman"]["mean"], "lo": r["spearman"]["lo"],
                     "hi": r["spearman"]["hi"], "p_permutation": r.get("permutation", {}).get("p", math.nan)})
    rows.append({"analysis": "H2 three studied explainers", "mean": res["h2_3"]["omnibus"]["mean"],
                 "lo": res["h2_3"]["omnibus"]["lo"], "hi": res["h2_3"]["omnibus"]["hi"], "p_permutation": math.nan})
    return pd.DataFrame(rows)


# --- command line -----------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--validate-only", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--authorized", default="")
    a = ap.parse_args(argv)
    spec, cfg = load_spec(), lib.config()
    if a.run:
        open_items = check_spec_decided(spec)
        if open_items or not a.authorized.strip():
            print("refused: the real-data analysis needs the author's authorization (--authorized) and "
                  f"a decided specification; open: {open_items or 'none'}", file=sys.stderr)
            return 2
    elif not a.validate_only:
        ap.error("give --validate-only or --run")
    rows = read_manifest()
    counts = check_manifest(rows, expected=expected_shards(cfg))
    full, roar, synth = (load_stage(st, rows) for st in STAGES)
    counts.update(validate(full, roar, synth, cfg, spec))
    print(json.dumps(counts, indent=1))
    if a.validate_only:
        return 0
    import subprocess
    commit = subprocess.run(["git", "rev-parse", "--short=12", "HEAD"], cwd=lib.ROOT,
                            capture_output=True, text=True).stdout.strip()
    header = {"authorized": a.authorized, "code commit": commit, "data": "outputs/analysis/paper_g/raw (frozen 04c6dfd84)",
              **{f"validation {k}": v for k, v in counts.items()}}
    run_analysis(full, roar, synth, spec, ANALYSIS_OUT, REPORT_PATH, header)
    print(f"analysis written to {ANALYSIS_OUT} and {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
