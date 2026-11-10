"""Paper B revision 1: sections S7-S13 of the supplementary file, from the analysis output.

Called by build_supplement.py. Reads the files that `scripts/paper_b_analyze.py` writes
(results/: primary_effects.csv, cells.csv, cost.csv, quality_checks.csv, status.json). When the
per-instance rows (rows.csv, about 10 MB, not committed) are given, it first derives the small
files the supplement needs (instances.csv, overlap.csv, paired_differences.csv,
zero_vector_exclusion.csv and fig_s1_paired_differences.png) and writes them to results/, so
that later builds work without the rows.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

NAMES = {"adult": "Adult", "breast_cancer": "Breast Cancer", "german_credit": "German Credit",
         "diabetes": "Diabetes", "spambase": "Spambase", "phishing": "Phishing",
         "connect4": "Connect-4"}
MODELS = {"logreg": "Logistic regression", "rf": "Random forest", "xgb": "XGBoost",
          "svm": "SVM (RBF)", "mlp": "MLP"}
EXPL = {"shap": "SHAP", "lime": "LIME (10)", "lime_full": "LIME (full)", "anchors": "Anchors",
        "dice": "DiCE"}
ENDP = {"stability": "Stability", "fidelity": "Fidelity", "faithfulness_gap": "Faithfulness gap",
        "sparsity": "Sparsity", "wall_ms": "Wall time (ms)", "cpu_ms": "CPU time (ms)",
        "rows": "Rows evaluated"}
CONTRASTS = ["lime_full", "anchors", "dice"]
ENDPOINTS = ["stability", "fidelity", "faithfulness_gap"]
DORDER = list(NAMES)
MORDER = list(MODELS)
EORDER = list(EXPL)


def f(v, d=2) -> str:
    try:
        v = float(v)
    except (TypeError, ValueError):
        return "—"
    if v != v:
        return "—"
    if abs(v) >= 1000:
        return f"{v:,.0f}"
    return f"{v:.{d}f}".replace("-", "−")


def p(v) -> str:
    v = float(v)
    return "<0.001" if v < 0.001 else f"{v:.3f}"


# ---------------------------------------------------------------------------------------
# Derived files (need the per-instance rows)
# ---------------------------------------------------------------------------------------
def timing_cells(timing_root: Path, out: Path) -> None:
    """Finished timing cells per dataset and model (timing/<d>/<m>/seed_<s>/timing.done)."""
    import pandas as pd
    recs = [{"dataset": f.parents[2].name, "model": f.parents[1].name,
             "seed": int(f.parent.name.split("_")[1])}
            for f in sorted(Path(timing_root).glob("timing/*/*/seed_*/timing.done"))]
    pd.DataFrame(recs, columns=["dataset", "model", "seed"]).to_csv(out / "timing_cells.csv",
                                                                     index=False)


def derive(rows: Path, out: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd
    q = pd.read_csv(rows)
    key = ["dataset", "model", "seed", "instance_id"]

    inst = (q[q.explainer == "shap"].groupby(["dataset", "model", "seed", "quadrant"])
            .instance_id.nunique().unstack(fill_value=0).reset_index())
    stab = (q[(q.explainer == "shap") & q.stability.notna()]
            .groupby(["dataset", "model", "seed"]).instance_id.nunique().rename("stability_n"))
    inst = inst.merge(stab.reset_index(), on=["dataset", "model", "seed"], how="left")
    inst.to_csv(out / "instances.csv", index=False)

    ov = []
    for (d, m), g in q[q.explainer == "shap"].groupby(["dataset", "model"]):
        sets = {s: set(x.instance_id) for s, x in g.groupby("seed")}
        js = [len(sets[a] & sets[b]) / len(sets[a] | sets[b])
              for a, b in itertools.combinations(sorted(sets), 2)]
        ov.append({"dataset": d, "model": m, "pairs": len(js), "jaccard_mean": sum(js) / len(js),
                   "jaccard_max": max(js)})
    pd.DataFrame(ov).to_csv(out / "overlap.csv", index=False)

    qa = q[q.dataset == "adult"]
    recs, fig_data = [], {}
    for ep, x in itertools.product(ENDPOINTS, CONTRASTS):
        a = qa[qa.explainer == "shap"][key + [ep]].rename(columns={ep: "a"})
        b = qa[qa.explainer == x][key + [ep]].rename(columns={ep: "b"})
        mm = a.merge(b, on=key).dropna(subset=["a", "b"])
        mm["delta"] = mm.a - mm.b
        fig_data[(ep, x)] = mm
        for mod, g in itertools.chain([("all", mm)], mm.groupby("model")):
            dq = g.delta.quantile([0, .1, .25, .5, .75, .9, 1]).to_list()
            recs.append({"endpoint": ep, "contrast": x, "model": mod, "n": len(g),
                         "mean": g.delta.mean(), "share_positive": (g.delta > 0).mean(),
                         **dict(zip(["min", "p10", "q25", "median", "q75", "p90", "max"], dq))})
    pd.DataFrame(recs).to_csv(out / "paired_differences.csv", index=False)

    fig, axes = plt.subplots(3, 3, figsize=(10, 8.5), sharey="row")
    for i, ep in enumerate(ENDPOINTS):
        for j, x in enumerate(CONTRASTS):
            ax = axes[i, j]
            mm = fig_data[(ep, x)]
            data = [mm[mm.model == m].delta.to_numpy() for m in MORDER]
            ax.boxplot(data, widths=0.6, showfliers=True, flierprops={"markersize": 2,
                       "alpha": 0.4}, medianprops={"color": "#1f77b4"})
            ax.axhline(0, color="0.4", lw=0.8, ls="--")
            ax.set_xticks(range(1, 6), ["LR", "RF", "XGB", "SVM", "MLP"], fontsize=8)
            if i == 0:
                ax.set_title(f"SHAP − {EXPL[x]}", fontsize=10)
            if j == 0:
                ax.set_ylabel(ENDP[ep], fontsize=9)
            ax.tick_params(axis="y", labelsize=8)
    fig.tight_layout()
    fig.savefig(out / "fig_s1_paired_differences.png", dpi=200)
    plt.close(fig)

    # Exclusion of instances with an all-zero LIME vector (sensitivity check of §4.1).
    import importlib.util
    import sys
    root = Path(__file__).resolve().parents[6]
    sys.path.insert(0, str(root / "scripts"))
    spec = importlib.util.spec_from_file_location("pba", root / "scripts" / "paper_b_analyze.py")
    pba = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pba)
    ex = []
    for x in ("lime_full", "lime"):
        bad = q[(q.explainer == x) & ((q.stability_zero_vectors.fillna(0) > 0) |
                                      (q.all_zero.fillna(0) > 0))]
        badk = set(map(tuple, bad[key].values))
        keep = ~pd.Series(list(map(tuple, qa[key].values)), index=qa.index).isin(badk)
        for ep in ENDPOINTS:
            for label, src in (("all", qa), ("excluded", qa[keep])):
                mm = pba.paired(src, ep, x)
                r = pba.mixed_model(mm, "delta")
                ex.append({"contrast": x, "endpoint": ep, "set": label, "n": len(mm),
                           "estimate": r["estimate"], "ci_lo": r["ci_lo"], "ci_hi": r["ci_hi"],
                           "p": r["p"]})
    pd.DataFrame(ex).to_csv(out / "zero_vector_exclusion.csv", index=False)


# ---------------------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------------------
def pending(what: str) -> list[str]:
    return ["", f"*[R] {what} Written from the result rows when that study is complete.*", ""]


def sections(res: Path, cfg: dict, n_features: dict) -> list[str]:
    import pandas as pd
    st = json.loads((res / "status.json").read_text(encoding="utf-8"))
    prim = pd.read_csv(res / "primary_effects.csv")
    cells = pd.read_csv(res / "cells.csv")
    cost = pd.read_csv(res / "cost.csv")
    qc = pd.read_csv(res / "quality_checks.csv")
    inst = pd.read_csv(res / "instances.csv")
    ov = pd.read_csv(res / "overlap.csv")
    pdiff = pd.read_csv(res / "paired_differences.csv")
    zx = pd.read_csv(res / "zero_vector_exclusion.csv")
    order = lambda df, cols: df.assign(**{f"_{c}": df[c].map({k: i for i, k in enumerate(o)})
                                          for c, o in cols}).sort_values([f"_{c}" for c, _ in cols])

    md = []
    # S7 ---------------------------------------------------------------------------------
    md += ["## S7. Realized instances", "",
           f"Quality pass: {st['jobs_finished']} of {st['jobs_total']} jobs, "
           f"{st['rows']:,} instance rows. Instances per stratum of the test split, for each "
           "dataset, model and seed (a stratum with fewer than 25 instances is taken whole), and "
           "the instances with stability computed:", "",
           "| Dataset | Model | Seed | TP | TN | FP | FN | Stability |",
           "|---|---|---:|---:|---:|---:|---:|---:|"]
    for r in order(inst, [("dataset", DORDER), ("model", MORDER)]).itertuples():
        md.append(f"| {NAMES[r.dataset]} | {MODELS[r.model]} | {r.seed} | {r.TP} | {r.TN} | "
                  f"{r.FP} | {r.FN} | {int(r.stability_n)} |")
    md += ["", "Overlap of the instance sets between seeds (Jaccard index over all pairs of seeds "
           "of the same dataset and model):", "",
           "| Dataset | Model | Mean | Maximum |", "|---|---|---:|---:|"]
    for r in order(ov, [("dataset", DORDER), ("model", MORDER)]).itertuples():
        md.append(f"| {NAMES[r.dataset]} | {MODELS[r.model]} | {f(r.jaccard_mean)} | "
                  f"{f(r.jaccard_max)} |")
    pooled = (ov.jaccard_mean * ov.pairs).sum() / ov.pairs.sum()
    md += ["", f"Over all {int(ov.pairs.sum())} pairs of seeds: mean {f(pooled)}, maximum "
           f"{f(ov.jaccard_max.max())} (the values of §3.2 of the paper).", ""]
    md += ["", "Degenerate explanations per dataset and explainer: share of all-zero attribution "
           "vectors, share of instances with undefined fidelity, and share of all-zero vectors "
           "among the 15 perturbed explanations of each stability instance:", "",
           "| Dataset | Explainer | Rows | All-zero | Fidelity undefined | Zero among perturbed |",
           "|---|---|---:|---:|---:|---:|"]
    for r in order(qc, [("dataset", DORDER), ("explainer", EORDER)]).itertuples():
        md.append(f"| {NAMES[r.dataset]} | {EXPL[r.explainer]} | {r.rows:,} | "
                  f"{100 * r.all_zero_share:.1f}% | {100 * r.fidelity_exact_zero_share:.1f}% | "
                  f"{100 * r.stability_zero_vector_share:.1f}% |")
    md.append("")

    # S8 ---------------------------------------------------------------------------------
    md += ["## S8. Primary benchmark (Adult): per model and seed", "",
           "Mean of each endpoint per cell (model, seed) and explainer. LIME (10) uses the "
           "10-feature budget, LIME (full) the full vector; the confirmatory contrasts use LIME "
           "(full).", "",
           "| Model | Seed | Explainer | Stability | Fidelity | Faithfulness gap | Sparsity |",
           "|---|---:|---|---:|---:|---:|---:|"]
    ca = order(cells[cells.dataset == "adult"], [("model", MORDER), ("explainer", EORDER)])
    for r in ca.sort_values(["_model", "seed", "_explainer"]).itertuples():
        md.append(f"| {MODELS[r.model]} | {r.seed} | {EXPL[r.explainer]} | {f(r.stability)} | "
                  f"{f(r.fidelity)} | {f(r.faithfulness_gap)} | {f(r.sparsity)} |")
    md += ["", "Paired effects SHAP − X on Adult, every endpoint and contrast (confirmatory rows "
           "marked C; Holm correction over the 12 confirmatory tests). Mixed model with random "
           "intercepts for model and for seed within model; variance components of the model "
           "(between models, seeds within models, residual); cluster bootstrap over models; "
           "number of the 25 cells with a positive difference.", "",
           "| Endpoint | X | | Estimate [95% CI] | p | p Holm | Bootstrap 95% CI | "
           "Var. model | Var. seed | Var. residual | Cells > 0 |",
           "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in prim.itertuples():
        d = 0 if r.endpoint in ("wall_ms", "cpu_ms", "rows") else 3
        md.append(f"| {ENDP[r.endpoint]} | {EXPL[r.contrast.split('-', 1)[1]]} | "
                  f"{'C' if r.confirmatory else ''} | {f(r.estimate, d)} [{f(r.ci_lo, d)}, "
                  f"{f(r.ci_hi, d)}] | {p(r.p)} | {p(r.p_holm) if r.confirmatory else '—'} | "
                  f"[{f(r.boot_lo, d)}, {f(r.boot_hi, d)}] | {f(r.var_model, 4)} | "
                  f"{f(r.var_seed_in_model, 4)} | {f(r.var_residual, 4)} | "
                  f"{r.cells_positive} |")
    md += ["", "Distribution of the instance-level paired differences SHAP − X (quantiles over "
           "all Adult instances, and per model):", "",
           "| Endpoint | X | Model | n | Mean | Share > 0 | Min | P10 | Q1 | Median | Q3 | P90 | Max |",
           "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    mo = {**{"all": -1}, **{m: i for i, m in enumerate(MORDER)}}
    pdiff = pdiff.assign(_m=pdiff.model.map(mo))
    for r in pdiff.itertuples():
        md.append(f"| {ENDP[r.endpoint]} | {EXPL[r.contrast]} | "
                  f"{'All' if r.model == 'all' else MODELS[r.model]} | {r.n:,} | {f(r.mean)} | "
                  f"{100 * r.share_positive:.0f}% | {f(r.min)} | {f(r.p10)} | {f(r.q25)} | "
                  f"{f(r.median)} | {f(r.q75)} | {f(r.p90)} | {f(r.max)} |")
    md += ["", "![Figure S1. Instance-level paired differences SHAP − X on Adult, by model "
           "(LR logistic regression, RF random forest, XGB XGBoost, SVM, MLP). Dashed line: no "
           "difference.](fig_s1_paired_differences.png){width=100%}", ""]

    # S9 ---------------------------------------------------------------------------------
    t = cfg["timing"]
    seeds = {d: (5 if d == "adult" else 3) for d in NAMES}
    full = t["per_stratum"] * 4
    md += ["## S9. Cost", "",
           f"Timing pass: {t['per_stratum']} instances per stratum ({full} per cell), "
           f"{t['repeats']} repetitions (median used), {t['warmup_per_explainer']} warm-up "
           "explanation per explainer, explainers interleaved per instance, one process and one "
           "thread pinned to logical CPU 2, measurements paused while any other process used "
           "more than 10% of a core. Wall time from the high-resolution performance counter; "
           "CPU time from the process clock (15.6 ms steps on Windows). FLOPs per explanation "
           "for logistic regression (2p + 2 per row) and the MLP (one hidden layer of 100 "
           "units), with p the number of encoded features.", ""]
    tc = pd.read_csv(res / "timing_cells.csv")
    done = tc.groupby(["dataset", "model"]).seed.nunique().to_dict()
    total = sum(5 * seeds[d] for d in NAMES)
    if len(tc) < total:
        todo = [NAMES[d] for d in DORDER
                if any(done.get((d, m), 0) < seeds[d] for m in MORDER)]
        md += [f"*Timing pass at this build: {len(tc)} of {total} cells finished. Not complete: "
               f"{', '.join(todo)}. Rows marked * rest on fewer seeds than planned; rows of "
               "models not started are absent.*", ""]
    md += ["| Dataset | Model | Explainer | n | Wall (ms) | CPU (ms) | Rows | Model calls | MFLOPs |",
           "|---|---|---|---:|---:|---:|---:|---:|---:|"]
    for r in order(cost, [("dataset", DORDER), ("model", MORDER), ("explainer", EORDER)]).itertuples():
        star = "*" if done.get((r.dataset, r.model), 0) < seeds[r.dataset] else ""
        fl = f(r.flops_per_explanation / 1e6) if r.flops_per_explanation == r.flops_per_explanation else "—"
        rows_ = "not counted" if (r.model == "xgb" and r.explainer == "anchors") else f"{r.rows_median:,.0f}"
        calls = "not counted" if (r.model == "xgb" and r.explainer == "anchors") else f"{r.calls_median:,.0f}"
        md.append(f"| {NAMES[r.dataset]} | {MODELS[r.model]} | {EXPL[r.explainer]} | "
                  f"{r.n}{star} | {f(r.wall_ms_median, 1)} | {f(r.cpu_ms_median, 1)} | {rows_} | "
                  f"{calls} | {fl} |")
    md += ["", "Anchors calls XGBoost through a prediction method the counter did not wrap, so its "
           "rows and calls on XGBoost were not counted; its time is measured as for every other "
           "explainer.", ""]
    mt = pd.read_csv(res / "studies_timing" / "matched_timing.csv")
    MM = {"rf": "Random forest, depth 15", "rf_d6": "Random forest, depth 6",
          "xgb": "XGBoost, depth 6", "xgb_d15": "XGBoost, depth 15"}
    md += ["Matched tree ensembles (Adult, 100 trees each, three seeds, 20 instances per cell, "
           "same timing protocol): each ensemble at its own depth and at the other's. Median wall "
           "time per explanation:", "",
           "| Model | TreeSHAP (ms) | LIME, full (ms) | TreeSHAP / LIME |", "|---|---:|---:|---:|"]
    for m in ("rf", "rf_d6", "xgb_d15", "xgb"):
        a = mt[(mt.model == m) & (mt.config == "shap")].wall_ms.iloc[0]
        l = mt[(mt.model == m) & (mt.config == "lime_full")].wall_ms.iloc[0]
        md.append(f"| {MM[m]} | {f(a, 1)} | {f(l, 1)} | {f(a / l)} |")
    md.append("")

    # S10 --------------------------------------------------------------------------------
    md += ["## S10. Configuration sweep", "",
           "Adult, five models, three seeds, one instance per stratum (12 per model), stability on "
           "each. LIME with the full vector. Degenerate explanations per configuration (pooled "
           "over models): share of all-zero explanations and mean number of all-zero vectors among "
           "the 15 perturbed explanations:", "",
           "| Configuration | All-zero | Zero among 15 perturbed |", "|---|---:|---:|"]
    dg = pd.read_csv(res / "sweep" / "sweep_degenerate.csv")
    for r in dg.itertuples():
        md.append(f"| `{r.config}` | {100 * r.all_zero:.0f}% | {f(r.zero_vectors_of_15, 1)} |")
    sq = pd.read_csv(res / "sweep" / "sweep_summary_long.csv")
    stt = pd.read_csv(res / "studies_timing" / "sweep_timing.csv")
    sq = sq.drop(columns=["wall"], errors="ignore").merge(stt[["model", "config", "wall_ms"]],
                                                         on=["model", "config"], how="left")
    pf = pd.read_csv(res / "sweep" / "sweep_pareto.csv")
    front = set(zip(pf.model, pf.config))
    md += ["", "Mean stability, fidelity and faithfulness gap on the 12 instances valid under every "
           "remaining configuration (LIME widths 0.75 to 5 left out), median wall time per "
           "explanation from the sweep's timing pass (same protocol as S9), and membership of the "
           "stability-fidelity Pareto front (P):", "",
           "| Model | Configuration | Stability | Fidelity | Faithfulness gap | Wall (ms) | Front |",
           "|---|---|---:|---:|---:|---:|---|"]
    for r in order(sq, [("model", MORDER)]).sort_values(["_model", "config"]).itertuples():
        md.append(f"| {MODELS[r.model]} | `{r.config}` | {f(r.stability)} | {f(r.fidelity)} | "
                  f"{f(r.gap)} | {f(r.wall_ms, 1)} | {'P' if (r.model, r.config) in front else ''} |")
    md += ["", "Configuration names: `lime_kw<width>_ns<samples>` (`kwdef` = 0.75 times the square "
           "root of the number of features), `kshap_ns<coalitions>_bg<background rows>` (`nsauto` "
           "= the library default, 2M + 2048), `tshap_bg<background rows>`. Wall time of every "
           "configuration, the degenerate LIME widths included, is in "
           "`results/studies_timing/sweep_timing.csv`.", ""]

    # S11 --------------------------------------------------------------------------------
    md += ["## S11. Measurement controls", "",
           "Exclusion of instances with an all-zero LIME vector (any of the explanation and its "
           "15 perturbed copies), Adult, mixed-model estimate of SHAP − X:", "",
           "| X | Endpoint | Instances | n | Estimate [95% CI] | p |",
           "|---|---|---|---:|---:|---:|"]
    for r in zx.itertuples():
        md.append(f"| {EXPL[r.contrast]} | {ENDP[r.endpoint]} | "
                  f"{'all' if r.set == 'all' else 'without all-zero'} | {r.n:,} | "
                  f"{f(r.estimate, 3)} [{f(r.ci_lo, 3)}, {f(r.ci_hi, 3)}] | {p(r.p)} |")
    cs = pd.read_csv(res / "controls" / "controls_stability.csv")
    md += ["", "Stability under the main protocol (Gaussian noise, sigma 0.1), without noise, and "
           "with noise that keeps one-hot features valid (a category resampled with probability "
           "0.1), on the same Adult instances (three seeds, 12 stability instances per cell):", "",
           "| Model | Explainer | Main | No noise | Valid one-hot |", "|---|---|---:|---:|---:|"]
    for r in order(cs, [("model", MORDER), ("explainer", EORDER)]).itertuples():
        md.append(f"| {MODELS[r.model]} | {EXPL[r.explainer]} | {f(r.main)} | "
                  f"{f(r.controls_nonoise)} | {f(r.controls_onehot)} |")
    ps = pd.read_csv(res / "controls" / "posthoc_stability.csv")
    md += ["", "Stability of the main runs on Adult by measure: cosine (as in the paper), cosine "
           "without all-zero vectors, mean pairwise Spearman correlation of absolute "
           "attributions, and mean top-5 Jaccard overlap:", "",
           "| Model | Explainer | Cosine | Cosine, no zero vectors | Spearman | Top-5 Jaccard |",
           "|---|---|---:|---:|---:|---:|"]
    for r in order(ps, [("model", MORDER), ("explainer", EORDER)]).itertuples():
        md.append(f"| {MODELS[r.model]} | {EXPL[r.explainer]} | {f(r.stab_cosine)} | "
                  f"{f(r.stab_cosine_nonzero)} | {f(r.stab_spearman)} | {f(r.stab_top5_jaccard)} |")
    mg = pd.read_csv(res / "controls" / "posthoc_masking_gaps.csv")
    md += ["", "Faithfulness gap SHAP − X on Adult under four masking schemes of the top-5 "
           "features (zero, training mean, draw from the training marginal, group mean with "
           "one-hot groups and education / education-num masked together): mean of cell means, "
           "and cells with SHAP ahead:", "",
           "| Model | X | Zero | Mean | Marginal | Grouped |", "|---|---|---:|---:|---:|---:|"]
    mg["x"] = mg.contrast.str.split("-", n=1).str[1]
    for (m, x), g in order(mg, [("model", MORDER)]).groupby(["_model", "x"], sort=True):
        g = g.set_index("scheme")
        cell = lambda k: f"{f(g.loc[k, 'gap_mean'], 3)} ({g.loc[k, 'cells_shap_ahead']}/{g.loc[k, 'cells']})"
        md.append(f"| {MODELS[g.model.iloc[0]]} | {EXPL[x]} | {cell('zero')} | {cell('mean')} | "
                  f"{cell('marginal')} | {cell('grouped_mean')} |")
    md.append("")

    # S12 --------------------------------------------------------------------------------
    md += ["## S12. Further datasets: per model", "",
           "Mean (SD) over the three seeds, per dataset, model and explainer. Table 4 of the "
           "paper averages these over the five models.", "",
           "| Dataset | Model | Explainer | Stability | Fidelity | Faithfulness gap | Sparsity |",
           "|---|---|---|---:|---:|---:|---:|"]
    co = cells[cells.dataset != "adult"]
    g = co.groupby(["dataset", "model", "explainer"])[["stability", "fidelity", "faithfulness_gap",
                                                       "sparsity"]].agg(["mean", "std"])
    g.columns = [f"{a}_{b}" for a, b in g.columns]
    g = order(g.reset_index(), [("dataset", DORDER), ("model", MORDER), ("explainer", EORDER)])
    for r in g.itertuples():
        md.append(f"| {NAMES[r.dataset]} | {MODELS[r.model]} | {EXPL[r.explainer]} | " +
                  " | ".join(f"{f(getattr(r, e + '_mean'))} ({f(getattr(r, e + '_std'))})"
                             for e in ("stability", "fidelity", "faithfulness_gap", "sparsity")) + " |")
    md.append("")

    # S13 --------------------------------------------------------------------------------
    md += ["## S13. How to regenerate every table", "",
           "1. Install the frozen environment; prepare the datasets and check the model hashes "
           "of S6 (`paper_b_run.py prepare`, then `paper_b_run.py preflight`). The prepared data "
           "reproduce the data hashes of S6 exactly.",
           "2. Quality pass: `paper_b_run.py launch` (resumable; one row per instance).",
           "3. Cost pass: `paper_b_run.py launch-timing` on an idle host.",
           "4. Analysis: `paper_b_analyze.py --root <results> --out <analysis>` writes every "
           "value of Tables 2–4 of the paper and of S7–S12 (primary_effects.csv, cells.csv, "
           "cost.csv, quality_checks.csv, cross_dataset.csv, friedman.csv).",
           "5. This file: `build_supplement.py --analysis <analysis>` derives the instance "
           "counts, overlaps, distributions, Figure S1 and the exclusion check from the "
           "per-instance rows.", ""]
    return md
