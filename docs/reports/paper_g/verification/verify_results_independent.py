#!/usr/bin/env python3
"""Independent re-computation of the Paper G results (Task 15, step 6). Read-only.

Does not import scripts/paper_g_analyze.py. Reads the raw shards with its own loader and
recomputes the main quantities with scipy / statsmodels routines, then compares them with the
generated outputs in outputs/analysis/paper_g/analysis/. Prints one line per check.
"""
import gzip
import itertools
import json
import math
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[4]
RAW, OUT = ROOT / "outputs/analysis/paper_g/raw", ROOT / "outputs/analysis/paper_g/analysis"
LOWER = {"m1_deletion", "m5_infidelity", "m6_sufficiency"}             # plan section 3
M6 = ["m1_deletion", "m2_insertion", "m3_gap", "m4_corr", "m5_infidelity", "m6_sufficiency"]
M7 = M6 + ["m7_roar"]
STUDIED, ALL = ["shap", "lime", "occlusion"], ["shap", "lime", "occlusion", "random"]
fails = []

def check(name, ours, theirs, tol=1e-6):
    ok = (math.isnan(ours) and math.isnan(theirs)) or abs(ours - theirs) <= tol
    print(f"{'OK  ' if ok else 'FAIL'} {name}: independent {ours:.6f} generated {theirs:.6f}")
    if not ok: fails.append(name)

def load(stage, cols):
    recs = []
    for p in sorted((RAW / stage).rglob("*.jsonl.gz")):
        for line in gzip.open(p, "rt"):
            x = json.loads(line)
            recs.append({c: x[c] for c in cols})
    return pd.DataFrame(recs)

key = ["dataset", "model", "seed"]
full = load("full", key + ["explainer", "instance", "m4_degenerate"] + M6)
roar = load("roar", key + ["explainer", "m7_roar"])
syn = load("synthetic", key + ["explainer", "instance", "spearman_truth"] + M6)
def orient(df, m):
    return -df[m] if m in LOWER else df[m]

means = full.groupby(key + ["explainer"])[M6].mean().reset_index().merge(roar, on=key + ["explainer"])
def spear(a, b):
    if np.ptp(a) == 0 or np.ptp(b) == 0: return math.nan
    return stats.spearmanr(a, b).statistic

def h1(explainers, metrics, table=means):
    rows = []
    for k, g in table.groupby(key):
        g = g.set_index("explainer").loc[explainers]
        vals = {m: orient(g, m).to_numpy() for m in metrics}
        sp = [spear(vals[a], vals[b]) for a, b in itertools.combinations(metrics, 2)]
        R = np.vstack([stats.rankdata(-vals[m]) for m in metrics])
        chi2 = stats.friedmanchisquare(*R.T).statistic if R.shape[1] > 2 else math.nan
        rows.append({"dataset": k[0], "sp": np.nanmean(sp), "w": chi2 / (len(metrics) * (len(explainers) - 1)),
                     "undef": int(np.isnan(sp).sum())})
    return pd.DataFrame(rows)

def tint(v):
    v = np.asarray(v)
    lo, hi = stats.t.interval(0.95, len(v) - 1, loc=v.mean(), scale=stats.sem(v))
    return v.mean(), lo, hi

b = h1(STUDIED, M7)
ds = b.groupby("dataset")[["sp", "w"]].mean()
print(f"H1 blocks {len(b)}, per dataset {sorted(b.groupby('dataset').size().unique())}, undefined pairs {b['undef'].sum()}")
gen_ds = pd.read_csv(OUT / "confirmatory/h1_datasets_spearman.csv").set_index("dataset")["mean"]
check("H1 max |dataset mean Spearman diff|", float((ds["sp"] - gen_ds).abs().max()), 0.0)
s = pd.read_csv(OUT / "confirmatory/h1_summary.csv").set_index("analysis")
for lab, col in (("mean pairwise Spearman", "sp"), ("Kendall W", "w")):
    m, lo, hi = tint(ds[col])
    for nm, ours in (("mean", m), ("lo", lo), ("hi", hi)):
        check(f"H1 {lab} {nm}", ours, s.loc[lab, nm])
for lab, ex, mets in (("H1 four explainers", ALL, M7), ("H1 circularity: M4 removed for all explainers (six metrics)", STUDIED, [m for m in M7 if m != "m4_corr"])):
    m, lo, hi = tint(h1(ex, mets).groupby("dataset")["sp"].mean())
    sens = pd.read_csv(OUT / "sensitivity/h1_sensitivity.csv").set_index("analysis")
    check(f"{lab} mean", m, sens.loc[lab, "spearman_mean"])
    check(f"{lab} lo", lo, sens.loc[lab, "spearman_lo"])

# Brute-force permutation check (independent relabelling, fewer draws): is the generated p plausible?
rng = np.random.default_rng(1)
obs = ds["sp"].mean()
ge = 0
B = 2000
blocks = {d: [(g.set_index("explainer").loc[STUDIED]) for _, g in gd.groupby(["model", "seed"])] for d, gd in means.groupby("dataset")}
for _ in range(B):
    tot = []
    for d, bl in blocks.items():
        perm = {m: rng.permutation(3) for m in M7}
        vals = [np.nanmean([spear(orient(g, a).to_numpy()[perm[a]], orient(g, c).to_numpy()[perm[c]])
                            for a, c in itertools.combinations(M7, 2)]) for g in bl]
        tot.append(np.mean(vals))
    ge += np.mean(tot) >= obs - 1e-12
p_gen = pd.read_csv(OUT / "confirmatory/h1_permutation.csv")["p"].iloc[0]
print(f"{'OK  ' if ge == 0 and p_gen <= 1 / 1001 else 'NOTE'} H1 brute-force permutation: {ge} of {B} relabelled statistics >= observed; generated p {p_gen:.6g}")

# Stability benchmark
rows = []
for (d, mo), g in means.groupby(["dataset", "model"]):
    for m in M7:
        r = {s_: stats.rankdata(-orient(gs.set_index("explainer").loc[STUDIED], m).to_numpy()) for s_, gs in g.groupby("seed")}
        rows.append({"dataset": d, "metric": m, "v": np.nanmean([spear(r[a], r[c]) for a, c in itertools.combinations(sorted(r), 2)])})
st = pd.DataFrame(rows).groupby(["dataset", "metric"])["v"].mean().groupby("dataset").mean()
m, lo, hi = tint(st)
ss = pd.read_csv(OUT / "confirmatory/stability_summary.csv").iloc[0]
check("stability mean", m, ss["mean"])
check("stability lo", lo, ss["lo"])
check("stability hi", hi, ss["hi"])

# H2
rows = []
for k, g in full.groupby(key + ["explainer"]):
    o = pd.DataFrame({m: orient(g, m) for m in M6})
    rho = o.corr(method="spearman")
    pairs = {f"{a}|{c}": rho.loc[a, c] for a, c in itertools.combinations(M6, 2)}
    rows.append({"dataset": k[0], **pairs, "omni": np.nanmean(list(pairs.values()))})
h2 = pd.DataFrame(rows)
h2d = h2.groupby("dataset").mean(numeric_only=True)
print(f"H2 blocks {len(h2)}, per dataset {sorted(h2.groupby('dataset').size().unique())}")
om = pd.read_csv(OUT / "confirmatory/h2_omnibus.csv").iloc[0]
m, lo, hi = tint(h2d["omni"])
check("H2 omnibus mean", m, om["mean"])
check("H2 omnibus lo", lo, om["lo"])
check("H2 omnibus hi", hi, om["hi"])
check("H2 one-sided t p", stats.ttest_1samp(h2d["omni"], 0, alternative="greater").pvalue, om["p_t"])
signs = np.array(list(itertools.product([1, -1], repeat=8)))
check("H2 sign-flip p", float(np.mean((signs * h2d["omni"].to_numpy()).mean(1) >= h2d["omni"].mean() - 1e-12)), om["p_sign_flip"])
pt = pd.read_csv(OUT / "confirmatory/h2_pairs.csv").set_index("pair")
ps = [stats.ttest_1samp(h2d[p], 0, alternative="greater").pvalue for p in pt.index]
check("H2 max |pair mean diff|", float(max(abs(h2d[p].mean() - pt.loc[p, "mean"]) for p in pt.index)), 0.0)
check("H2 max |Holm-15 diff| (statsmodels)", float(np.max(np.abs(multipletests(ps, method="holm")[1] - pt["p_holm15"].to_numpy()))), 0.0)
mult = pd.read_csv(OUT / "confirmatory/multiplicity_h1_h2.csv")
check("Holm H1/H2 (statsmodels) max diff", float(np.max(np.abs(multipletests(mult["p_raw"], method="holm")[1] - mult["p_holm"]))), 0.0)

# Synthetic
rows = []
for (c, s_), g in syn.groupby(["dataset", "seed"]):
    mm = g.groupby("explainer")[["spearman_truth"] + M6].mean().loc[ALL]
    ref = stats.rankdata(-mm["spearman_truth"].to_numpy())
    for m in M6:
        rows.append({"metric": m, "v": spear(stats.rankdata(-orient(mm, m).to_numpy()), ref)})
sy = pd.DataFrame(rows).groupby("metric")["v"].mean()
gs = pd.read_csv(OUT / "synthetic/four_by_metric.csv").set_index("metric")["mean"]
check("synthetic max |per-metric diff|", float((sy - gs).abs().max()), 0.0)

# Degenerate M4: confirm the exploratory equality is real, not a copied output
mx = full.copy()
mx.loc[mx["m4_degenerate"], "m4_corr"] = np.nan
mx = mx.groupby(key + ["explainer"])[M6].mean().reset_index().merge(roar, on=key + ["explainer"])
dx = h1(STUDIED, M7, mx).groupby("dataset")["sp"].mean()
print(f"M4 exclusion: blocks whose H1 statistic changed {int((h1(STUDIED, M7, mx)['sp'] - b['sp']).abs().gt(1e-12).sum())}; "
      f"max dataset-mean change {float((dx - ds['sp']).abs().max()):.2e}")
print(f"\n{len(fails)} failed check(s): {fails}")
sys.exit(1 if fails else 0)
