#!/usr/bin/env python3
"""Paper D analysis: is explanation quality lower on misclassified instances?

Implements docs/reports/paper_d/ANALYSIS_PLAN.md (committed before this script ran).
Every table is written to outputs/analysis/paper_d/ as `metric,value` rows, the format
the registry's `paper_d:<table>:<metric>` resolver reads (scripts/pubs/claim_sources.py).

Tables
  data     inventory, exclusions, instance counts                        (plan s3, s6)
  rq1      per-run delta = mean(misclassified) - mean(correct), Wilcoxon + Holm  (s5)
  rq1r     robustness: delta averaged over n within (model, seed)          (s5)
  rq2      delta by model family + Kruskal-Wallis, Holm                     (s5)
  rq3      delta FP - FN per run, Wilcoxon + Holm                           (s5)
  rq4      run fixed-effects regression with and without the margin         (s5)
  rq4q     contrast within margin quintiles                                 (s5)
  ext      German Credit (EXP3), descriptive                                (s5)
  fig_*    binned data for scripts/generate_paper_d_figures.py

Run: python scripts/pubs/paper_d_analysis.py   (needs scipy, scikit-learn, xgboost)
"""
from __future__ import annotations

import csv
import json
import sys
import warnings
from collections import defaultdict
from pathlib import Path

import joblib
import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "outputs" / "analysis" / "paper_d"
EXP2 = ROOT / "experiments" / "exp2_scaled" / "results"
EXP3 = ROOT / "experiments" / "exp3_cross_dataset" / "results" / "german_credit"
MODELS = ROOT / "experiments" / "exp1_adult" / "models"

FAMILIES = ["logreg", "rf", "xgb", "svm", "mlp"]
METHODS = ["shap", "lime", "anchors", "dice"]
PRIMARY = ["fidelity", "stability", "faithfulness_gap"]
SECONDARY = ["sparsity"]
DESCRIPTIVE = ["cost"]
MIN_GROUP = 10          # plan s6: runs with < 10 per group are excluded
ALPHA = 0.05
D_MIN, DELTA_MIN = 0.5, 0.05   # plan s5: practical relevance


def holm(pvals: list[float]) -> list[float]:
    m = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, (m - rank) * pvals[idx])
        adj[idx] = min(1.0, running)
    return list(adj)


def load_runs(root: Path, dataset: str) -> list[dict]:
    runs = []
    for f in sorted(root.glob("*_*/seed_*/n_*/results.json")):
        cell = f.parts[-4]
        model, method = cell.split("_", 1)
        seed = int(f.parts[-3].split("_")[1])
        n = int(f.parts[-2].split("_")[1])
        d = json.loads(f.read_text(encoding="utf-8"))
        runs.append({"dataset": dataset, "model": model, "method": method, "seed": seed,
                     "n": n, "instances": d.get("instance_evaluations") or []})
    return runs


def run_delta(inst: list[dict], metric: str, a: set[str], b: set[str]):
    xa = [i["metrics"].get(metric) for i in inst if i.get("quadrant") in a]
    xb = [i["metrics"].get(metric) for i in inst if i.get("quadrant") in b]
    xa = [v for v in xa if v is not None and np.isfinite(v)]
    xb = [v for v in xb if v is not None and np.isfinite(v)]
    if len(xa) < MIN_GROUP or len(xb) < MIN_GROUP:
        return None
    return float(np.mean(xa) - np.mean(xb))


ERR, COR = {"FP", "FN"}, {"TP", "TN"}


def summarize(deltas: np.ndarray) -> dict:
    n = len(deltas)
    mean = float(np.mean(deltas))
    sd = float(np.std(deltas, ddof=1)) if n > 1 else float("nan")
    half = stats.t.ppf(0.975, n - 1) * sd / np.sqrt(n) if n > 1 else float("nan")
    nonzero = deltas[deltas != 0]
    p = float(stats.wilcoxon(deltas).pvalue) if len(nonzero) > 0 else 1.0
    return {"n": n, "median": float(np.median(deltas)), "mean": mean,
            "ci_lo": mean - half, "ci_hi": mean + half,
            "dz": mean / sd if sd > 0 else float("nan"), "p": p,
            "pos": int((deltas > 0).sum()), "neg": int((deltas < 0).sum())}


def emit(table: str, rows: dict[str, float]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{table}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["metric", "value"])
        for k, v in rows.items():
            w.writerow([k, repr(float(v))])


def test_family(cells: dict, tests: list[tuple[str, str]], prefix: dict, out: dict):
    """Wilcoxon per (method, metric) on the deltas in `cells`, Holm over the family."""
    res = {}
    for method, metric in tests:
        d = np.array(cells.get((method, metric), []))
        if len(d) >= 2:
            res[(method, metric)] = summarize(d)
    keys = list(res)
    for k, adj in zip(keys, holm([res[k]["p"] for k in keys])):
        res[k]["p_holm"] = adj
    for (method, metric), r in res.items():
        for field, v in r.items():
            out[f"{method}.{metric}.{field}"] = v
        out[f"{method}.{metric}.relevant"] = float(
            r["p_holm"] < ALPHA and abs(r["dz"]) >= D_MIN and abs(r["median"]) >= DELTA_MIN)
    return res


def margins_for(runs: list[dict]) -> dict[tuple, dict[int, float]]:
    """Recompute p-hat for every (model, seed, instance) from the stored models (RQ4)."""
    from src.data_loading.adult import load_adult
    prep = joblib.load(MODELS / "preprocessor.joblib")
    need: dict[int, dict[str, set[int]]] = defaultdict(lambda: defaultdict(set))
    for r in runs:
        for i in r["instances"]:
            need[r["seed"]][r["model"]].add(int(i["instance_id"]))
    models = {m: joblib.load(MODELS / f"{m}.joblib") for m in FAMILIES}
    out: dict[tuple, dict[int, float]] = {}
    check = {"agree": 0, "total": 0, "label_ok": 0}
    for seed, by_model in need.items():
        _, X_test, _, y_test, _, _ = load_adult(cache_dir=str(ROOT / "data"), random_state=seed,
                                                preprocessor=prep, verbose=False)
        y_test = np.asarray(y_test)
        for model, ids in by_model.items():
            ids_arr = np.array(sorted(ids))
            proba = models[model].predict_proba(X_test[ids_arr])[:, 1]
            out[(model, seed)] = dict(zip(ids_arr.tolist(), proba.tolist()))
            out[(model, seed, "pred")] = dict(zip(ids_arr.tolist(),
                                                  models[model].predict(X_test[ids_arr]).tolist()))
            out[(model, seed, "y")] = dict(zip(ids_arr.tolist(), y_test[ids_arr].tolist()))
    return out


def cluster_ols(y, X, groups):
    """OLS on within-run demeaned data; cluster-robust (by run) covariance, CR1."""
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    meat = np.zeros((X.shape[1], X.shape[1]))
    uniq = np.unique(groups)
    for g in uniq:
        sel = groups == g
        s = X[sel].T @ u[sel]
        meat += np.outer(s, s)
    G, N, K = len(uniq), len(y), X.shape[1]
    V = XtX_inv @ meat @ XtX_inv * (G / (G - 1)) * ((N - 1) / (N - K - G))
    se = np.sqrt(np.diag(V))
    t = stats.t.ppf(0.975, G - 1)
    return beta, se, beta - t * se, beta + t * se


def demean(v, groups):
    out = v.astype(float).copy()
    for g in np.unique(groups):
        sel = groups == g
        out[sel] -= out[sel].mean()
    return out


def main() -> None:
    warnings.filterwarnings("ignore")
    runs = load_runs(EXP2, "adult")
    data: dict[str, float] = {"runs_total": len(runs)}
    n_inst = sum(len(r["instances"]) for r in runs)
    data["instances_total"] = n_inst
    for m in METHODS:
        mr = [r for r in runs if r["method"] == m]
        data[f"{m}.runs_present"] = len(mr)
        data[f"{m}.runs_nonempty"] = sum(1 for r in mr if r["instances"])
        data[f"{m}.unlabelled"] = sum(1 for r in mr for i in r["instances"] if i.get("quadrant") not in ERR | COR)
        data[f"{m}.correct"] = sum(1 for r in mr for i in r["instances"] if i.get("quadrant") in COR)
        data[f"{m}.misclassified"] = sum(1 for r in mr for i in r["instances"] if i.get("quadrant") in ERR)
    data["unlabelled_total"] = sum(data[f"{m}.unlabelled"] for m in METHODS)
    data["analysed_total"] = n_inst - data["unlabelled_total"]

    # ---- RQ1 / RQ3 per-run deltas ---------------------------------------------------
    cells = defaultdict(list)           # (method, metric) -> [delta]
    cells_fpfn = defaultdict(list)
    per_run = []                        # for RQ1 robustness and RQ2
    for r in runs:
        for metric in PRIMARY + SECONDARY + DESCRIPTIVE:
            d = run_delta(r["instances"], metric, ERR, COR)
            if d is not None:
                cells[(r["method"], metric)].append(d)
                per_run.append((r["method"], metric, r["model"], r["seed"], r["n"], d))
            e = run_delta(r["instances"], metric, {"FP"}, {"FN"})
            if e is not None and metric in PRIMARY:
                cells_fpfn[(r["method"], metric)].append(e)
    for m in METHODS:
        data[f"{m}.runs_analysed"] = len(cells[(m, "fidelity")])
    data["runs_analysed"] = sum(data[f"{m}.runs_analysed"] for m in METHODS)

    rq1: dict[str, float] = {}
    res1 = test_family(cells, [(m, k) for m in METHODS for k in PRIMARY], {}, rq1)
    test_family(cells, [(m, k) for m in METHODS for k in SECONDARY], {}, rq1)
    for m in METHODS:   # cost: descriptive (median delta, and relative to correct)
        d = np.array(cells.get((m, "cost"), []))
        if len(d):
            rq1[f"{m}.cost.median"] = float(np.median(d))
            rq1[f"{m}.cost.pos"] = int((d > 0).sum())
            rq1[f"{m}.cost.n"] = len(d)
    rq1["n_primary_tests"] = len(res1)
    rq1["n_significant"] = sum(1 for r in res1.values() if r["p_holm"] < ALPHA)
    rq1["n_relevant"] = sum(1 for (m, k) in res1 if rq1[f"{m}.{k}.relevant"] == 1.0)
    emit("rq1", rq1)

    # robustness: average over n within (model, seed)
    agg = defaultdict(list)
    for method, metric, model, seed, n, d in per_run:
        agg[(method, metric, model, seed)].append(d)
    cells_r = defaultdict(list)
    for (method, metric, model, seed), ds in agg.items():
        cells_r[(method, metric)].append(float(np.mean(ds)))
    rq1r: dict[str, float] = {}
    resr = test_family(cells_r, [(m, k) for m in METHODS for k in PRIMARY], {}, rq1r)
    agree = 0
    for key in res1:
        a, b = res1[key], resr.get(key)
        if b is None:
            continue
        same_dir = np.sign(a["median"]) == np.sign(b["median"])
        same_sig = (a["p_holm"] < ALPHA) == (b["p_holm"] < ALPHA)
        firm = same_dir and same_sig
        rq1r[f"{key[0]}.{key[1]}.firm"] = float(firm)
        agree += firm
    rq1r["n_agree"] = agree
    emit("rq1r", rq1r)

    # ---- RQ2: by family ---------------------------------------------------------------
    rq2: dict[str, float] = {}
    kw = {}
    for m in METHODS:
        for k in PRIMARY:
            groups = []
            for fam in FAMILIES:
                ds = [d for (mm, kk, mo, s, n, d) in per_run if mm == m and kk == k and mo == fam]
                if ds:
                    rq2[f"{m}.{k}.{fam}.median"] = float(np.median(ds))
                    rq2[f"{m}.{k}.{fam}.min"] = float(np.min(ds))
                    rq2[f"{m}.{k}.{fam}.max"] = float(np.max(ds))
                    rq2[f"{m}.{k}.{fam}.n"] = len(ds)
                    groups.append(ds)
            if len(groups) >= 2:
                h = stats.kruskal(*groups)
                kw[(m, k)] = (float(h.statistic), float(h.pvalue), len(groups))
    keys = list(kw)
    for key, adj in zip(keys, holm([kw[k][1] for k in keys])):
        m, k = key
        rq2[f"{m}.{k}.kw_H"], rq2[f"{m}.{k}.kw_p"], rq2[f"{m}.{k}.kw_groups"] = kw[key]
        rq2[f"{m}.{k}.kw_p_holm"] = adj
    rq2["n_kw_tests"] = len(kw)
    rq2["n_kw_significant"] = sum(1 for m, k in kw if rq2[f"{m}.{k}.kw_p_holm"] < ALPHA)
    emit("rq2", rq2)

    # ---- RQ3 ------------------------------------------------------------------------
    rq3: dict[str, float] = {}
    res3 = test_family(cells_fpfn, [(m, k) for m in METHODS for k in PRIMARY], {}, rq3)
    rq3["n_tests"] = len(res3)
    rq3["n_significant"] = sum(1 for r in res3.values() if r["p_holm"] < ALPHA)
    emit("rq3", rq3)

    # ---- RQ4: margin control ----------------------------------------------------------
    marg = margins_for(runs)
    rq4: dict[str, float] = {}
    rq4q: dict[str, float] = {}
    figm: dict[str, float] = {}
    # Deviation 1 (ANALYSIS_PLAN s9): a run enters RQ4 only if the stored model reproduces
    # its recorded predictions (>= 99%). The Jan-Feb random-forest runs were made with a
    # model that is no longer in the repository, so their margin cannot be recomputed.
    agree_pred = total = 0
    reproducible = set()
    for gi, r in enumerate(runs):
        ok = n_r = 0
        for i in r["instances"]:
            if i.get("quadrant") not in ERR | COR:
                continue
            n_r += 1
            ok += int(marg[(r["model"], r["seed"], "pred")][int(i["instance_id"])] == i["prediction"])
        total += n_r
        agree_pred += ok
        if n_r and ok / n_r >= 0.99:
            reproducible.add(gi)
    rq4["prediction_reproduced"] = agree_pred
    rq4["prediction_total"] = total
    rq4["runs_nonempty"] = sum(1 for r in runs if r["instances"])
    rq4["runs_reproducible"] = len(reproducible)
    for fam in FAMILIES:
        rq4[f"{fam}.runs_reproducible"] = sum(1 for gi in reproducible if runs[gi]["model"] == fam)
        rq4[f"{fam}.runs_nonempty"] = sum(1 for r in runs if r["model"] == fam and r["instances"])
    # SVC: Platt-scaled proba and predict() can disagree; count it (disclosed in the paper).
    for fam in FAMILIES:
        dis = tot = 0
        for gi, r in enumerate(runs):
            if r["model"] != fam or gi not in reproducible:
                continue
            for i in r["instances"]:
                if i.get("quadrant") not in ERR | COR:
                    continue
                p = marg[(fam, r["seed"])][int(i["instance_id"])]
                tot += 1
                dis += int((p >= 0.5) != bool(i["prediction"]))
        rq4[f"{fam}.proba_pred_disagree"] = dis
        rq4[f"{fam}.proba_total"] = tot
    edges_by_method = {}
    for m in METHODS:
        for k in PRIMARY:
            ys, mis, mg, grp = [], [], [], []
            for gi, r in enumerate(runs):
                if r["method"] != m or gi not in reproducible:
                    continue
                for i in r["instances"]:
                    q = i.get("quadrant")
                    v = i["metrics"].get(k)
                    if q not in ERR | COR or v is None or not np.isfinite(v):
                        continue
                    p = marg[(r["model"], r["seed"])][int(i["instance_id"])]
                    ys.append(v); mis.append(float(q in ERR)); mg.append(abs(p - 0.5)); grp.append(gi)
            if not ys:
                continue
            ys, mis, mg, grp = map(np.asarray, (ys, mis, mg, grp))
            yd, md, gd = demean(ys, grp), demean(mis, grp), demean(mg, grp)
            b0, s0, lo0, hi0 = cluster_ols(yd, md[:, None], grp)
            b1, s1, lo1, hi1 = cluster_ols(yd, np.column_stack([md, gd]), grp)
            pre = f"{m}.{k}"
            rq4[f"{pre}.b_raw"], rq4[f"{pre}.lo_raw"], rq4[f"{pre}.hi_raw"] = b0[0], lo0[0], hi0[0]
            rq4[f"{pre}.b_adj"], rq4[f"{pre}.lo_adj"], rq4[f"{pre}.hi_adj"] = b1[0], lo1[0], hi1[0]
            rq4[f"{pre}.b_margin"], rq4[f"{pre}.lo_margin"], rq4[f"{pre}.hi_margin"] = b1[1], lo1[1], hi1[1]
            rq4[f"{pre}.n_inst"], rq4[f"{pre}.n_runs"] = len(ys), len(np.unique(grp))
            shrink = 1 - b1[0] / b0[0] if b0[0] != 0 else float("nan")
            rq4[f"{pre}.shrink"] = shrink
            rq4[f"{pre}.explained"] = float(shrink > 0.5 and lo1[0] <= 0 <= hi1[0])
            # margin quintiles (method-wide edges), contrast within quintile
            if m not in edges_by_method:
                edges_by_method[m] = np.quantile(mg, [0.2, 0.4, 0.6, 0.8])
            qi = np.digitize(mg, edges_by_method[m])
            for q in range(5):
                sel = qi == q
                e_, c_ = ys[sel & (mis == 1)], ys[sel & (mis == 0)]
                rq4q[f"{pre}.q{q+1}.n_mis"], rq4q[f"{pre}.q{q+1}.n_cor"] = len(e_), len(c_)
                if len(e_) and len(c_):
                    rq4q[f"{pre}.q{q+1}.diff"] = float(e_.mean() - c_.mean())
            # binned means for the margin figure
            bins = np.linspace(0, 0.5, 11)
            bi = np.clip(np.digitize(mg, bins) - 1, 0, 9)
            for b in range(10):
                for lab, flag in (("cor", 0), ("mis", 1)):
                    sel = (bi == b) & (mis == flag)
                    if sel.sum() >= 30:
                        figm[f"{pre}.{lab}.b{b}"] = float(ys[sel].mean())
            for lab, flag in (("cor", 0), ("mis", 1)):
                rq4[f"{pre}.margin_median_{lab}"] = float(np.median(mg[mis == flag]))
    rq4["n_explained"] = sum(1 for kk, v in rq4.items() if kk.endswith(".explained") and v == 1.0)
    emit("rq4", rq4)
    emit("rq4q", rq4q)
    emit("fig_margin", figm)

    # ---- External check: German Credit -----------------------------------------------
    ext: dict[str, float] = {}
    gruns = load_runs(EXP3, "german_credit")
    ext["runs_total"] = len(gruns)
    for m in ("shap", "anchors"):
        for k in PRIMARY:
            ds = [run_delta(r["instances"], k, ERR, COR) for r in gruns if r["method"] == m]
            ds = np.array([d for d in ds if d is not None])
            if len(ds):
                ext[f"{m}.{k}.n"] = len(ds)
                ext[f"{m}.{k}.median"] = float(np.median(ds))
                ext[f"{m}.{k}.min"] = float(ds.min())
                ext[f"{m}.{k}.max"] = float(ds.max())
                ext[f"{m}.{k}.pos"] = int((ds > 0).sum())
                ext[f"{m}.{k}.neg"] = int((ds < 0).sum())
                # same sign as the Adult median?
                a = rq1.get(f"{m}.{k}.median")
                if a is not None:
                    ext[f"{m}.{k}.same_sign_as_adult"] = int((np.sign(ds) == np.sign(a)).sum())
    emit("ext", ext)
    emit("data", data)

    # long CSV of per-run deltas for figures
    with open(OUT / "fig_deltas.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["method", "metric", "model", "seed", "n", "delta"])
        w.writerows(per_run)
    print(f"wrote {OUT}")
    for m in METHODS:
        for k in PRIMARY + SECONDARY:
            if f"{m}.{k}.median" in rq1:
                print(f"{m:8s} {k:17s} n={rq1[f'{m}.{k}.n']:.0f} med={rq1[f'{m}.{k}.median']:+.4f} "
                      f"dz={rq1[f'{m}.{k}.dz']:+.2f} pH={rq1[f'{m}.{k}.p_holm']:.2g} "
                      f"rel={rq1[f'{m}.{k}.relevant']:.0f}")


if __name__ == "__main__":
    main()
