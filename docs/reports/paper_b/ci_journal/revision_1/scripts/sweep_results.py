"""Paper B rev. 1: configuration sweep (quality). Usage: sweep_results.py <sweep results/quality> <out dir>.

LIME kernel widths 0.75 to 5 are reported as degenerate and left out of the comparisons; every
other comparison is on the instances valid under every remaining configuration of the model.
"""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
rows = []
for f in ROOT.rglob("*.jsonl"):
    model, seed, cfg = f.parts[-3], int(f.parts[-2].split("_")[1]), f.stem
    for l in f.read_text().splitlines():
        d = json.loads(l)
        rows.append(dict(model=model, seed=seed, config=cfg, instance_id=d["instance_id"],
                         stability=d.get("stability"), fidelity=d.get("fidelity"),
                         gap=d.get("faithfulness_gap"), wall=d.get("explain_wall_ms"),
                         degenerate=bool(d.get("all_zero")), zero_vectors=d.get("stability_zero_vectors") or 0))
r = pd.DataFrame(rows)
r["family"] = r.config.str.split("_").str[0]
print("rows", len(r), "configs", r.config.nunique())

# degenerate share per config (pooled over models)
deg = r.groupby(["family", "config"]).agg(all_zero=("degenerate", "mean"), zero_vectors_of_15=("zero_vectors", "mean"))
deg.round(3).to_csv(OUT / "sweep_degenerate.csv")
print("== degenerate share, top 12\n", deg.head(12).round(3).to_string())
print("by kernel width (LIME):", r[r.family == "lime"].assign(kw=lambda d: d.config.str.split("_").str[1])
      .groupby("kw").degenerate.mean().round(3).to_dict())

# common valid instances per model x seed: valid (non-degenerate, all metrics present) under every config
r = r[~r.config.str.contains(r"lime_kw(?:0p75|1p5|3p0|5p0)_")].copy()   # degenerate widths, reported above
r["valid"] = ~r.config.isna() & r[["stability", "fidelity", "gap"]].notna().all(axis=1)
ncfg = r.groupby("model").config.nunique()
ok = r[r.valid].groupby(["model", "seed", "instance_id"]).config.nunique().reset_index()
ok = ok[ok.config == ok.model.map(ncfg)][["model", "seed", "instance_id"]]
c = r.merge(ok, on=["model", "seed", "instance_id"])
print("common valid instances per model:", ok.groupby("model").size().to_dict(), "of 12")
r = r[~r.degenerate]

summ = c.groupby(["model", "config"])[["stability", "fidelity", "gap", "wall"]].mean()
summ.round(4).to_csv(OUT / "sweep_summary.csv")

# sign of SHAP - LIME over the grid: every (SHAP config, LIME config) pair, per model, cell means
res = []
for m, g in summ.groupby(level="model"):
    g = g.droplevel("model")
    sh = g[~g.index.str.startswith("lime")]; li = g[g.index.str.startswith("lime")]
    for ep in ("stability", "fidelity", "gap"):
        d = sh[ep].values[:, None] - li[ep].values[None, :]
        res.append(dict(model=m, endpoint=ep, pairs=d.size, shap_ahead=int((d > 0).sum()),
                        share=(d > 0).mean(), shap_min=sh[ep].min(), shap_max=sh[ep].max(),
                        lime_min=li[ep].min(), lime_max=li[ep].max(),
                        lime_best=li[ep].idxmax(), shap_worst=sh[ep].idxmin()))
sg = pd.DataFrame(res)
sg.round(3).to_csv(OUT / "sweep_signs.csv", index=False)
print("== SHAP ahead of LIME over all config pairs\n", sg.round(3).to_string())

# LIME by kernel width and samples (pooled over models): stability, fidelity
li = c[c.family == "lime"].copy()
li["kw"] = li.config.str.split("_").str[1]; li["ns"] = li.config.str.split("_").str[2]
for ep in ("stability", "fidelity"):
    print(f"== LIME {ep} by kernel width x samples\n",
          li.pivot_table(index="kw", columns="ns", values=ep, aggfunc="mean").round(3).to_string())
# KernelSHAP: default (auto) vs 500, budgets, background
ks = c[c.family == "kshap"]
print("== KernelSHAP by config, per model\n",
      ks.pivot_table(index="config", columns="model", values=["stability", "fidelity"], aggfunc="mean").round(3).to_string())
ts = c[c.family == "tshap"]
print("== TreeSHAP by background\n",
      ts.pivot_table(index="config", columns="model", values=["stability", "fidelity"], aggfunc="mean").round(3).to_string())

# Pareto fronts on (stability, fidelity), maximise both, per model
fr = []
for m, g in summ.groupby(level="model"):
    g = g.droplevel("model")
    for cfg, row in g.iterrows():
        dom = ((g.stability >= row.stability) & (g.fidelity >= row.fidelity) &
               ((g.stability > row.stability) | (g.fidelity > row.fidelity))).any()
        if not dom:
            fr.append(dict(model=m, config=cfg, stability=row.stability, fidelity=row.fidelity))
fr = pd.DataFrame(fr)
fr.round(3).to_csv(OUT / "sweep_pareto.csv", index=False)
print("== Pareto front (stability, fidelity)\n", fr.round(3).to_string())
summ.reset_index().to_csv(OUT / "sweep_summary_long.csv", index=False)
