#!/usr/bin/env python3
"""Paper B revision 1 (cohort B2): the statistical analysis of the paper (WP6).

    py scripts/paper_b_analyze.py                    # results of the full run
    py scripts/paper_b_analyze.py --root PATH        # another results root (tests, pilot)
    py scripts/paper_b_analyze.py --allow-partial    # while the run is still going

Reads the quality rows (results/quality/<dataset>/<model>/seed_<s>/<explainer>.jsonl) and,
when present, the timing rows (results/timing/.../timing.jsonl). Writes to
outputs/analysis/paper_b_rev1/:

- rows.csv               one row per (dataset, model, seed, explainer, instance)
- cells.csv              cell means (dataset, model, seed, explainer)
- primary_effects.csv    Table 2: per endpoint and contrast, the mixed-model estimate with
                         95% CI, cluster-bootstrap CI over models, Holm p, d_z, HL, r_rb, sign
                         agreement over cells
- friedman.csv           Friedman test and Nemenyi critical difference on cell means
- cross_dataset.csv      Table 4: mean and SD over seeds of the model-averaged cell means
- quality_checks.csv     all-zero vectors, undefined fidelity, realized strata, seed overlap
- cost.csv               Table 3 (only when timing rows exist): median CPU ms and rows per
                         explanation; FLOPs for logistic regression and the MLP
- REPORT.md              every number above in one place, with the design hash

Design (manuscript Section 3.5): confirmatory = Adult; contrasts SHAP - X for
X in {LIME (full vector), Anchors, DiCE}; endpoints stability, fidelity, faithfulness gap and
(when timed) cost; Holm over the family; everything else exploratory, without tests.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_b_lib as lib  # noqa: E402

OUT = lib.ROOT / "outputs" / "analysis" / "paper_b_rev1"
PRIMARY = "adult"
REFERENCE = "shap"
CONTRASTS = ["lime_full", "anchors", "dice"]          # SHAP - X, confirmatory
SECONDARY = ["lime"]                                  # 10-feature variant, descriptive
FOUR = ["shap", "lime_full", "anchors", "dice"]
ENDPOINTS = ["stability", "fidelity", "faithfulness_gap"]
DESCRIPTIVE = ["sparsity"]
BOOT = 10_000
# Studentized range q_{0.05, k, inf} / sqrt(2) for the Nemenyi test (Demsar 2006, Table 5).
NEMENYI_Q05 = {2: 1.960, 3: 2.343, 4: 2.569, 5: 2.728, 6: 2.850}


# ---------------------------------------------------------------------------------------
# Statistics (pure functions; unit-tested in tests/analysis/test_paper_b_rev1.py)
# ---------------------------------------------------------------------------------------
def holm(pvals: list[float]) -> list[float]:
    """Holm-Bonferroni adjusted p-values, in the input order (NaN kept as NaN)."""
    idx = [i for i, p in enumerate(pvals) if not (p is None or math.isnan(p))]
    order = sorted(idx, key=lambda i: pvals[i])
    m, out, running = len(order), [float("nan")] * len(pvals), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvals[i]))
        out[i] = running
    return out


def hodges_lehmann(d: np.ndarray) -> float:
    """One-sample Hodges-Lehmann estimate: the median of the Walsh averages."""
    d = np.asarray(d, float)
    d = d[~np.isnan(d)]
    if d.size == 0:
        return float("nan")
    i, j = np.triu_indices(d.size)
    return float(np.median((d[i] + d[j]) / 2.0))


def rank_biserial(d: np.ndarray) -> float:
    """Matched-pairs rank-biserial correlation (Kerby 2014): (R+ - R-) / (R+ + R-), zeros
    dropped as in the Wilcoxon signed-rank test."""
    d = np.asarray(d, float)
    d = d[~np.isnan(d) & (d != 0)]
    if d.size == 0:
        return float("nan")
    r = stats.rankdata(np.abs(d))
    pos, neg = r[d > 0].sum(), r[d < 0].sum()
    return float((pos - neg) / (pos + neg))


def d_z(d: np.ndarray) -> float:
    d = np.asarray(d, float)
    d = d[~np.isnan(d)]
    if d.size < 2 or np.std(d, ddof=1) == 0:
        return float("nan")
    return float(np.mean(d) / np.std(d, ddof=1))


def nemenyi_cd(k: int, n: int, alpha: float = 0.05) -> float:
    if alpha != 0.05 or k not in NEMENYI_Q05:
        raise ValueError("Nemenyi CD tabulated for alpha = 0.05 and k = 2..6 only")
    return NEMENYI_Q05[k] * math.sqrt(k * (k + 1) / (6.0 * n))


def cluster_bootstrap_ci(df: pd.DataFrame, value: str, cluster: str, reps: int = BOOT,
                         seed: int = 20261106) -> tuple[float, float]:
    """95% percentile CI of the grand mean of `value` when whole clusters are resampled."""
    groups = [g[value].to_numpy(float) for _, g in df.groupby(cluster)]
    groups = [g[~np.isnan(g)] for g in groups]
    sums = np.array([g.sum() for g in groups])
    counts = np.array([g.size for g in groups])
    rng = np.random.default_rng(seed)
    pick = rng.integers(0, len(groups), size=(reps, len(groups)))
    means = sums[pick].sum(1) / np.maximum(counts[pick].sum(1), 1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def mixed_model(df: pd.DataFrame, value: str) -> dict:
    """value ~ 1 + (1 | model) + (1 | model:seed). Returns the intercept, its 95% CI and the
    two-sided Wald p. Falls back to a cell-mean t-test (recorded) if the fit fails."""
    import statsmodels.formula.api as smf
    d = df[["model", "seed", value]].dropna().copy()
    d["seed"] = d["seed"].astype(str)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # re_formula="1" is required: with vc_formula alone statsmodels drops the
            # random intercept of the group (here: the model).
            fit = smf.mixedlm(f"{value} ~ 1", d, groups=d["model"], re_formula="1",
                              vc_formula={"seed": "0 + C(seed)"}).fit(reml=True)
        est = float(fit.params["Intercept"])
        lo, hi = (float(x) for x in fit.conf_int().loc["Intercept"])
        p = float(fit.pvalues["Intercept"])
        if not all(map(math.isfinite, (est, lo, hi, p))):
            raise ValueError("non-finite fit")
        vc = {"var_model": float(fit.cov_re.iloc[0, 0]),
              "var_seed_in_model": float(fit.vcomp[0]) if len(fit.vcomp) else float("nan"),
              "var_residual": float(fit.scale)}
        return {"estimate": est, "ci_lo": lo, "ci_hi": hi, "p": p, "method": "mixedlm", **vc}
    except Exception as exc:                                        # noqa: BLE001
        cells = d.groupby(["model", "seed"])[value].mean().to_numpy()
        t = stats.ttest_1samp(cells, 0.0)
        ci = t.confidence_interval(0.95)
        return {"estimate": float(cells.mean()), "ci_lo": float(ci.low), "ci_hi": float(ci.high),
                "p": float(t.pvalue), "method": f"cell t-test (mixedlm failed: {exc})"[:120]}


# ---------------------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------------------
def load_quality(root: Path) -> pd.DataFrame:
    recs = []
    for f in sorted((root / "quality").glob("*/*/seed_*/*.jsonl")):
        explainer, seed = f.stem, int(f.parent.name.split("_")[1])
        model, dataset = f.parent.parent.name, f.parent.parent.parent.name
        for r in lib.read_jsonl(f):
            if r.get("failed") or "fidelity" not in r:
                continue
            recs.append({"dataset": dataset, "model": model, "seed": seed,
                         "explainer": explainer, "instance_id": int(r["instance_id"]),
                         "quadrant": r.get("quadrant"), "cohort_sha256": r.get("cohort_sha256"),
                         "fidelity": r.get("fidelity"), "faithfulness_gap": r.get("faithfulness_gap"),
                         "sparsity": r.get("sparsity"), "stability": r.get("stability"),
                         "all_zero": bool(r.get("all_zero")),
                         "stability_zero_vectors": r.get("stability_zero_vectors"),
                         "explain_wall_ms": r.get("explain_wall_ms")})
    return pd.DataFrame(recs)


def load_timing(root: Path) -> pd.DataFrame:
    recs = []
    for f in sorted((root / "timing").glob("*/*/seed_*/timing.jsonl")):
        seed = int(f.parent.name.split("_")[1])
        model, dataset = f.parent.parent.name, f.parent.parent.parent.name
        for r in lib.read_jsonl(f):
            reps = [x for x in r.get("reps", []) if not x.get("error")]
            if not reps:
                continue
            recs.append({"dataset": dataset, "model": model, "seed": seed,
                         "explainer": r["explainer"], "instance_id": int(r["instance_id"]),
                         "cpu_ms": float(np.median([x["cpu_ms"] for x in reps])),
                         "wall_ms": float(np.median([x["wall_ms"] for x in reps])),
                         "rows": float(np.median([x["rows"] for x in reps])),
                         "model_calls": float(np.median([x["model_calls"] for x in reps]))})
    return pd.DataFrame(recs)


def applicable_timing(t: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Drop timing rows of an explainer that does not apply to the model. Before b2598680b the
    sweep's timing pass ran its TreeSHAP settings on logreg and svm too, where they silently
    became KernelSHAP: 53 mislabelled rows (logreg seeds 11/22/33, svm seed 11)."""
    if t.empty:
        return t
    keep = [lib.explainer_applies(cfg, e, m) for e, m in zip(t["explainer"], t["model"])]
    return t[keep]


def complete_cells(q: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Keep only cells (dataset, model, seed) whose every applicable explainer job is finished
    (an explainer restricted to other models, e.g. the sweep's TreeSHAP settings on SVM, is not
    expected; requiring it dropped every logreg/svm/mlp cell of the sweep, 2026-11-09)."""
    done = set()
    for d, m, s in q[["dataset", "model", "seed"]].drop_duplicates().itertuples(index=False):
        stem = lib.RESULTS / "quality" / d / m / f"seed_{s}"
        need = [e for e in cfg["explainers"] if lib.explainer_applies(cfg, e, m)]
        if all((stem / f"{e}.done").exists() for e in need):
            done.add((d, m, s))
    key = list(zip(q["dataset"], q["model"], q["seed"]))
    return q[[k in done for k in key]]


# ---------------------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------------------
def paired(q: pd.DataFrame, endpoint: str, x: str) -> pd.DataFrame:
    """Instance-level SHAP - X differences for one endpoint (same instances by design)."""
    keys = ["dataset", "model", "seed", "instance_id"]
    a = q[q.explainer == REFERENCE][keys + [endpoint]].rename(columns={endpoint: "a"})
    b = q[q.explainer == x][keys + [endpoint]].rename(columns={endpoint: "b"})
    m = a.merge(b, on=keys).dropna(subset=["a", "b"])
    m["delta"] = m["a"] - m["b"]
    return m


def primary_effects(q: pd.DataFrame, t: pd.DataFrame) -> pd.DataFrame:
    qa = q[q.dataset == PRIMARY]
    rows = []
    endpoints = [(e, qa) for e in ENDPOINTS + DESCRIPTIVE]
    if not t.empty:
        # Cost is tested in wall time (author, 2026-11-07): Windows advances process CPU time in
        # 15.6 ms steps, too coarse for explainers that take a few ms. CPU time stays descriptive.
        endpoints += [("wall_ms", t[t.dataset == PRIMARY]), ("cpu_ms", t[t.dataset == PRIMARY]),
                      ("rows", t[t.dataset == PRIMARY])]
    for (ep, src), x in itertools.product(endpoints, CONTRASTS + SECONDARY):
        m = paired(src, ep, x)
        if m.empty:
            continue
        cells = m.groupby(["model", "seed"]).agg(a=("a", "mean"), b=("b", "mean"),
                                                 delta=("delta", "mean"))
        mm = mixed_model(m, "delta")
        lo_b, hi_b = cluster_bootstrap_ci(m, "delta", "model")
        confirm = x in CONTRASTS and ep not in DESCRIPTIVE and ep not in ("rows", "cpu_ms")
        rows.append({"endpoint": ep, "contrast": f"shap-{x}", "confirmatory": confirm,
                     "n_instances": len(m), "n_cells": len(cells),
                     "mean_shap": cells["a"].mean(), "mean_x": cells["b"].mean(),
                     **{k: mm[k] for k in ("estimate", "ci_lo", "ci_hi", "p", "method")},
                     "var_model": mm.get("var_model"), "var_seed_in_model": mm.get("var_seed_in_model"),
                     "var_residual": mm.get("var_residual"),
                     "boot_lo": lo_b, "boot_hi": hi_b,
                     "d_z": d_z(cells["delta"].to_numpy()),
                     "hl": hodges_lehmann(cells["delta"].to_numpy()),
                     "r_rb": rank_biserial(cells["delta"].to_numpy()),
                     "cells_positive": int((cells["delta"] > 0).sum())})
    df = pd.DataFrame(rows)
    if not df.empty:
        conf = df["confirmatory"].to_numpy()
        df["p_holm"] = float("nan")
        df.loc[conf, "p_holm"] = holm(df.loc[conf, "p"].tolist())
    return df


def friedman(q: pd.DataFrame) -> pd.DataFrame:
    qa = q[q.dataset == PRIMARY]
    rows = []
    for ep in ENDPOINTS:
        c = qa[qa.explainer.isin(FOUR)].groupby(["model", "seed", "explainer"])[ep].mean().unstack()
        c = c.dropna()
        if len(c) < 2 or c.shape[1] < len(FOUR):
            continue
        st = stats.friedmanchisquare(*[c[e] for e in FOUR])
        ranks = c[FOUR].rank(axis=1, ascending=False).mean()
        rows.append({"endpoint": ep, "n_cells": len(c), "chi2": st.statistic, "p": st.pvalue,
                     "cd_nemenyi": nemenyi_cd(len(FOUR), len(c)),
                     **{f"rank_{e}": ranks[e] for e in FOUR}})
    return pd.DataFrame(rows)


def cross_dataset(q: pd.DataFrame) -> pd.DataFrame:
    c = q.groupby(["dataset", "model", "seed", "explainer"])[ENDPOINTS + DESCRIPTIVE].mean()
    per_seed = c.groupby(["dataset", "seed", "explainer"]).mean()          # average over models
    agg = per_seed.groupby(["dataset", "explainer"]).agg(["mean", "std"])
    agg.columns = [f"{a}_{b}" for a, b in agg.columns]
    return agg.reset_index()


def quality_checks(q: pd.DataFrame) -> pd.DataFrame:
    g = q.groupby(["dataset", "explainer"])
    out = pd.DataFrame({
        "rows": g.size(),
        "all_zero_share": g["all_zero"].mean(),
        "fidelity_exact_zero_share": g["fidelity"].apply(lambda s: float((s == 0).mean())),
        "stability_rows": g["stability"].apply(lambda s: int(s.notna().sum())),
        # A count per stability instance, out of stability_T perturbed explanations (15):
        # 0.88 means about one in 17 vectors, not 88%. The share says it directly.
        "stability_zero_vectors_mean": g["stability_zero_vectors"].mean(),
        "stability_zero_vector_share": g["stability_zero_vectors"].mean()
        / lib.config()["metrics"]["stability_T"],
    }).reset_index()
    ov = []
    for (d, m), sub in q[q.explainer == REFERENCE].groupby(["dataset", "model"]):
        sets = {s: set(x["instance_id"]) for s, x in sub.groupby("seed")}
        for s1, s2 in itertools.combinations(sorted(sets), 2):
            u = sets[s1] | sets[s2]
            ov.append(len(sets[s1] & sets[s2]) / len(u) if u else float("nan"))
    out.attrs["seed_overlap_jaccard_mean"] = float(np.nanmean(ov)) if ov else float("nan")
    out.attrs["seed_overlap_jaccard_max"] = float(np.nanmax(ov)) if ov else float("nan")
    return out


def flops_per_row(model: str, n_features: int) -> float | None:
    """Multiply-adds x 2 for one forward pass (probability output)."""
    if model == "logreg":
        return 2.0 * n_features + 2
    if model == "mlp":
        h = 100
        return 2.0 * (n_features * h + h * 1) + 4 * h         # dense layers + ReLU/bias
    return None


def cost_table(t: pd.DataFrame) -> pd.DataFrame:
    if t.empty:
        return t
    c = t.groupby(["dataset", "model", "explainer"]).agg(
        cpu_ms_median=("cpu_ms", "median"), wall_ms_median=("wall_ms", "median"),
        rows_median=("rows", "median"), calls_median=("model_calls", "median"),
        n=("cpu_ms", "size")).reset_index()
    nfeat = {d: lib.load_dataset(d)["X_train"].shape[1] for d in c["dataset"].unique()}
    c["flops_per_explanation"] = [
        (flops_per_row(m, nfeat[d]) or float("nan")) * r
        for d, m, r in zip(c["dataset"], c["model"], c["rows_median"])]
    return c


def report(out: Path, hashes: list[str], q: pd.DataFrame, prim: pd.DataFrame,
           fr: pd.DataFrame, cross: pd.DataFrame, qc: pd.DataFrame, cost: pd.DataFrame,
           partial: bool) -> None:
    def cell(v) -> str:
        if isinstance(v, (float, np.floating)):
            return "" if math.isnan(v) else f"{v:.4g}"
        return str(v)

    def tab(df: pd.DataFrame, cols: list[str] | None = None) -> str:
        if df.empty:
            return "_(no data yet)_\n"
        d = df[cols] if cols else df
        head = "| " + " | ".join(map(str, d.columns)) + " |"
        sep = "|" + "---|" * len(d.columns)
        body = ["| " + " | ".join(cell(v) for v in r) + " |" for r in d.itertuples(index=False)]
        return "\n".join([head, sep, *body]) + "\n"
    lines = ["# Paper B revision 1: analysis report (cohort B2)", "",
             f"- Design hash: `{', '.join(hashes)}`",
             f"- Rows: {len(q):,}; cells: {q[['dataset', 'model', 'seed']].drop_duplicates().shape[0]}",
             f"- {'PARTIAL: the run is not finished; numbers will change' if partial else 'Complete cells only'}",
             f"- Seed overlap of instances (Jaccard, same dataset and model): mean "
             f"{qc.attrs.get('seed_overlap_jaccard_mean', float('nan')):.3f}, max "
             f"{qc.attrs.get('seed_overlap_jaccard_max', float('nan')):.3f}", "",
             "## Table 2: primary effects (Adult)", "",
             tab(prim, ["endpoint", "contrast", "confirmatory", "n_cells", "mean_shap", "mean_x",
                        "estimate", "ci_lo", "ci_hi", "boot_lo", "boot_hi", "p_holm", "d_z", "hl",
                        "r_rb", "cells_positive", "method"]) if not prim.empty else tab(prim),
             "## Friedman / Nemenyi (Adult, cell means; rank 1 = highest)", "", tab(fr),
             "## Table 4: other datasets (mean and SD over seeds of model-averaged means)", "",
             tab(cross), "## Quality checks", "", tab(qc),
             "## Table 3: cost", "", tab(cost)]
    (out / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def count_finished(root: Path) -> int:
    """Finished quality jobs under a results root: one .done marker per job."""
    return len(list(Path(root).glob("quality/*/*/seed_*/*.done")))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=lib.RESULTS)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--allow-partial", action="store_true",
                    help="analyse finished cells while the run is going (marked PARTIAL)")
    ap.add_argument("--include-incomplete", action="store_true",
                    help="preview only: also use cells whose explainers are not all finished")
    a = ap.parse_args(argv)
    if a.include_incomplete:
        a.allow_partial = True
    cfg = lib.config()
    q = load_quality(a.root)
    if q.empty:
        # Timing-only studies (matched; the Anchors-on-XGBoost rows rerun): the cost table only.
        t = applicable_timing(load_timing(a.root), cfg)
        if t.empty:
            print("no quality rows and no timing rows")
            return 1
        a.out.mkdir(parents=True, exist_ok=True)
        t.to_csv(a.out / "timing_rows.csv", index=False)
        cost = cost_table(t)
        cost.to_csv(a.out / "cost.csv", index=False)
        (a.out / "REPORT.md").write_text(
            f"# Timing-only analysis\n\n- Root: `{a.root}`\n- Timing rows: {len(t):,}; cells: "
            f"{t[['dataset', 'model', 'seed']].drop_duplicates().shape[0]}\n- Per-row value: median "
            f"over repeats; cost.csv: median over instances per dataset, model and explainer\n",
            encoding="utf-8")
        print(f"timing-only analysis written to {a.out} ({len(t):,} timing rows)")
        return 0
    hashes = sorted(q["cohort_sha256"].dropna().unique())
    if len(hashes) != 1:
        print(f"refusing: rows of {len(hashes)} different designs: {hashes}")
        return 1
    if a.root == lib.RESULTS and not a.include_incomplete:
        q = complete_cells(q, cfg)
    t = applicable_timing(load_timing(a.root), cfg)
    a.out.mkdir(parents=True, exist_ok=True)
    q.to_csv(a.out / "rows.csv", index=False)
    q.groupby(["dataset", "model", "seed", "explainer"])[ENDPOINTS + DESCRIPTIVE].mean() \
        .reset_index().to_csv(a.out / "cells.csv", index=False)
    prim = primary_effects(q, t)
    fr = friedman(q)
    cross = cross_dataset(q[q.dataset != PRIMARY])
    qc = quality_checks(q)
    cost = cost_table(t)
    for name, df in (("primary_effects", prim), ("friedman", fr), ("cross_dataset", cross),
                     ("quality_checks", qc), ("cost", cost)):
        df.to_csv(a.out / f"{name}.csv", index=False)
    total = len(lib.all_quality_jobs(cfg, None, None, None, None))
    # Counted in the results being analysed (--root), as the orchestrator counts them: on the
    # documentation laptop lib.RESULTS is an empty live folder, and the 18:21 preview of a
    # synced snapshot reported 0 of 575 (2026-11-07).
    finished = count_finished(a.root)
    partial = finished < total
    if partial and not a.allow_partial and a.root == lib.RESULTS:
        print(f"run not finished ({finished}/{total} jobs): use --allow-partial for a preview")
        return 1
    report(a.out, hashes, q, prim, fr, cross, qc, cost, partial)
    json.dump({"rows": len(q), "jobs_finished": finished, "jobs_total": total,
               "partial": partial, "design": hashes[0]},
              open(a.out / "status.json", "w"), indent=1)
    print(f"analysis written to {a.out} ({len(q):,} rows; {'PARTIAL' if partial else 'complete'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
