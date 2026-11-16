#!/usr/bin/env python3
"""Independent verification of the S1 run and analysis (Task 19, section 7). Read-only.

Imports no Paper G module: its own loaders, pandas and scipy. Checks coverage, hashes, the
reconstruction record, instance alignment, unchanged frozen rows, the conversion (re-done from the
stored audit inputs), M7 alignment, and recomputes the H1-form, W, sensitivity, H2-form and
rank-position summaries for the three conditions, comparing them with the generated outputs.
Exit 0 only if every check passes.
"""
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

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "outputs/analysis/paper_g"
S1 = OUT / "supplementary/s1"
AN = S1 / "analysis"
LOWER = {"m1_deletion", "m5_infidelity", "m6_sufficiency"}
M6 = ["m1_deletion", "m2_insertion", "m3_gap", "m4_corr", "m5_infidelity", "m6_sufficiency"]
M7 = M6 + ["m7_roar"]
B2 = {"m1_deletion": "m1_deletion_b2", "m2_insertion": "m2_insertion_b2", "m3_gap": "m3_gap_b2",
      "m6_sufficiency": "m6_sufficiency_b2"}
STUDIED, ALL = ["shap", "lime", "occlusion"], ["shap", "lime", "occlusion", "random"]
KEY = ["dataset", "model", "seed"]
TOL = 5e-6            # generated CSVs carry six decimals
fails = []


def check(name, ok, detail=""):
    print(f"{'OK  ' if ok else 'FAIL'} {name}{': ' + detail if detail else ''}")
    if not ok:
        fails.append(name)


def orient(v, m):
    return -v if m.removesuffix("_b2") in LOWER else v


def spear(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if np.ptp(a) == 0 or np.ptp(b) == 0:
        return math.nan
    return float(stats.spearmanr(a, b).statistic)


def tint(v):
    v = np.asarray([x for x in v if not math.isnan(x)], float)
    lo, hi = stats.t.interval(0.95, len(v) - 1, loc=v.mean(), scale=stats.sem(v))
    return v.mean(), lo, hi


def self_test():
    """Constructed reference cases for the statistics used below."""
    R = np.array([[1, 2, 3], [1, 3, 2], [2, 1, 3], [1, 2, 3]], float)
    chi2 = stats.friedmanchisquare(*R.T).statistic
    m, n = R.shape
    S = ((R.sum(0) - m * (n + 1) / 2) ** 2).sum()
    check("self-test: Kendall W via Friedman equals the closed form", abs(chi2 / (m * (n - 1)) - 12 * S / (m**2 * (n**3 - n))) < 1e-12)
    check("self-test: Spearman of reversed ranks is -1", abs(spear([1, 2, 3], [3, 2, 1]) + 1) < 1e-12)
    check("self-test: constant vector gives undefined", math.isnan(spear([1, 1, 1], [1, 2, 3])))


def load_raw():
    with open(OUT / "raw/MANIFEST.csv", encoding="utf-8") as fh:
        man = list(csv.DictReader(fh))
    bad = [r["path"] for r in man if hashlib.sha256((OUT / "raw" / r["path"]).read_bytes()).hexdigest() != r["sha256"]]
    check("frozen raw shards unchanged (SHA-256 vs MANIFEST)", not bad, f"{len(man)} files")
    full, roar = [], []
    for r in man:
        st = r["path"].split("/")[0]
        if st not in ("full", "roar"):
            continue
        for line in gzip.open(OUT / "raw" / r["path"], "rt"):
            x = json.loads(line)
            if st == "full":
                full.append({k: x[k] for k in KEY + ["explainer", "instance", "f_x", *M6, *B2.values()]})
            else:
                roar.append({k: x[k] for k in KEY + ["explainer", "m7_roar"]})
    return pd.DataFrame(full), pd.DataFrame(roar)


def load_s1(full):
    with open(S1 / "MANIFEST.csv", encoding="utf-8") as fh:
        man = list(csv.DictReader(fh))
    cfg = tomllib.loads((ROOT / "experiments/exp_g/config.toml").read_text())
    models = sorted(full["model"].unique())
    expected = {(d["key"], m, s) for d in cfg["dataset"] for m in models for s in cfg["seeds"]}
    shards, rows, m7, recon = {}, [], [], []
    for r in man:
        data = (S1 / r["path"]).read_bytes()
        done = json.loads((S1 / r["path"].replace(".json.gz", ".done.json")).read_text())
        ok = hashlib.sha256(data).hexdigest() == r["sha256"] == done["sha256"]
        if not ok:
            check(f"S1 shard hash {r['path']}", False)
        res = json.loads(gzip.decompress(data))
        k = (res["meta"]["dataset"], res["meta"]["model"], res["meta"]["seed"])
        shards[k] = res
        rows += res["rows"]
        recon += res["reconstruction"]
        m7 += [{**x, "dataset": k[0], "model": k[1], "seed": k[2]} for x in res["m7"]]
    check("S1 coverage: 160 blocks = 8 datasets x 4 models x 5 seeds", set(shards) == expected and len(man) == 160,
          f"{len(shards)} blocks")
    check("S1 shard hashes (bytes = MANIFEST = .done)", len([f for f in fails if f.startswith("S1 shard hash")]) == 0)
    rc = pd.DataFrame(recon)
    check("reconstruction: 32,000 instances, every check passed", len(rc) == 32000 and rc["passed"].all())
    check("reconstruction tolerances", rc["fx_diff"].max() <= 1e-12 and rc["attr_max_diff"].max() <= 1e-8
          and rc["metric_max_diff"].max() <= 1e-9 and rc["deterministic"].all() and rc["pred_match"].all(),
          f"max f_x {rc['fx_diff'].max():.1e}, attr {rc['attr_max_diff'].max():.1e}, metric {rc['metric_max_diff'].max():.1e}")
    return shards, pd.DataFrame(rows), pd.DataFrame(m7)


def check_alignment(full, rows):
    lime = full[full["explainer"] == "lime"][KEY + ["instance", "f_x"]]
    for rep in ("S1-B", "S1-M"):
        r = rows[rows["representation"] == rep][KEY + ["instance", "f_x"]]
        m = lime.merge(r, on=KEY + ["instance"], how="outer", suffixes=("", "_s1"), indicator=True)
        check(f"{rep}: instances identical to the frozen LIME rows", (m["_merge"] == "both").all() and len(m) == 32000)
        check(f"{rep}: f_x identical to the frozen LIME rows", float((m["f_x"] - m["f_x_s1"]).abs().max()) <= 1e-12)


def check_conversion(shards, rows):
    worst, n = 0.0, 0
    idx = rows.set_index(KEY + ["instance", "representation"])["group_vector"]
    for k, res in shards.items():
        a = res["audit"]
        mu, s, b = (np.array([float(v) for v in a[f]]) for f in ("lime_mean", "lime_scale", "baseline"))
        groups = a["groups"]
        cols = sorted(j for g in groups for j in g)
        if cols != list(range(len(mu))):
            check(f"groups partition the encoded columns {k}", False)
        for inst in a["instances"]:
            w, x = np.array([float(v) for v in inst["w"]]), np.array([float(v) for v in inst["x"]])
            sign = 1.0 if inst["pred_class"] == 1 else -1.0
            for rep, ref in (("S1-B", b), ("S1-M", mu)):
                c = w * (x - ref) / s
                g = sign * np.array([c[gg].sum() for gg in groups])
                stored = np.array(json.loads(idx[(*k, inst["instance"], rep)]))
                worst = max(worst, float(np.max(np.abs(g - stored))))
                n += 1
            num = np.array(a["is_numeric"])
            worst_ref = float(np.max(np.abs(b[num] - mu[num]))) if num.any() else 0.0
            if worst_ref > 1e-12:
                check(f"numeric baseline = LIME mean {k}", False)
    check("conversion re-done from audit inputs (w, x, mu, s, b, groups) equals stored group vectors",
          worst <= 1e-9, f"{n} vectors, max diff {worst:.1e}")


def check_m7(rows, m7):
    worst = 0
    for (d, mo, s, rep), g in rows.groupby(KEY + ["representation"]):
        V = np.array([json.loads(v) for v in g.sort_values("instance")["group_vector"]])
        imp = np.abs(V).mean(axis=0)
        order = sorted(range(len(imp)), key=lambda i: (-imp[i], i))
        stored = json.loads(m7[(m7["dataset"] == d) & (m7["model"] == mo) & (m7["seed"] == s)
                               & (m7["representation"] == rep)]["global_rank"].iloc[0])
        worst += int(order != stored)
    check("M7 global rankings = order of mean |group contribution| (ties by index)", worst == 0, f"{worst} mismatches")
    by = pd.read_csv(AN / "lime_m7_by_block.csv")
    for rep, col in (("S1-B", "m7_roar_s1b"), ("S1-M", "m7_roar_s1m")):
        mm = by.merge(m7[m7["representation"] == rep][KEY + ["m7_roar"]], on=KEY)
        check(f"M7 by block aligned for {rep}", len(mm) == 160 and float((mm[col] - mm["m7_roar"]).abs().max()) <= 1e-6)


def substitute(full, roar, rows, m7, rep):
    if rep == "original":
        return full, roar
    s = rows[rows["representation"] == rep].set_index(KEY + ["instance"])
    f = full.copy()
    lime = f["explainer"] == "lime"
    keyed = f.loc[lime].set_index(KEY + ["instance"]).index
    for c in (*M6, *B2.values()):
        f.loc[lime, c] = s.loc[keyed, c].to_numpy()
    r = roar.copy()
    mm = m7[m7["representation"] == rep].set_index(KEY)["m7_roar"]
    rl = r["explainer"] == "lime"
    r.loc[rl, "m7_roar"] = mm.loc[r.loc[rl].set_index(KEY).index].to_numpy()
    return f, r


def h1_family(full, roar, explainers, metrics, baseline2=False):
    cols = {m: (B2.get(m, m) if baseline2 else m) for m in M6}
    means = full.groupby(KEY + ["explainer"])[[cols[m] for m in M6]].mean().rename(columns={v: k for k, v in cols.items()})
    sysd = means.reset_index().merge(roar, on=KEY + ["explainer"])
    sp_ds, w_ds = {}, {}
    pos = {}
    for k, g in sysd.groupby(KEY):
        g = g.set_index("explainer").loc[explainers]
        R = np.vstack([stats.rankdata(-orient(g[m].to_numpy(float), m)) for m in metrics])
        sp = [spear(R[i], R[j]) for i, j in itertools.combinations(range(len(metrics)), 2)]
        ok = [v for v in sp if not math.isnan(v)]
        sp_ds.setdefault(k[0], []).append(np.mean(ok) if ok else math.nan)
        chi2 = stats.friedmanchisquare(*R.T).statistic          # tie-corrected; W = chi2 / (m (n - 1))
        w_ds.setdefault(k[0], []).append(chi2 / (R.shape[0] * (R.shape[1] - 1)))
        for i, m in enumerate(metrics):
            for e_i, e in enumerate(explainers):
                tied = (R[i] == R[i, e_i]).sum() > 1
                key = (m, e)
                pos.setdefault(key, {"r1": 0, "r2": 0, "r3": 0, "tied": 0})
                pos[key]["tied" if tied else f"r{int(R[i, e_i])}"] = pos[key].get("tied" if tied else f"r{int(R[i, e_i])}", 0) + 1
    sp = tint([np.nanmean(v) for v in sp_ds.values()])
    w = tint([np.nanmean(v) for v in w_ds.values()])
    return sp, w, pos


def h2(full, explainers):
    ds = {}
    for k, g in full[full["explainer"].isin(explainers)].groupby(KEY + ["explainer"]):
        g = g.sort_values("instance")
        vals = [spear(orient(g[a].to_numpy(float), a), orient(g[b].to_numpy(float), b)) for a, b in itertools.combinations(M6, 2)]
        ds.setdefault(k[0], []).append(np.nanmean(vals))
    return tint([np.mean(v) for v in ds.values()])


def check_summaries(full, roar, rows, m7):
    comp = pd.read_csv(AN / "comparison_summary.csv")
    get = lambda q, c: comp[(comp["quantity"] == q) & (comp["condition"] == c)].iloc[0]  # noqa: E731
    for cond in ("original", "S1-B", "S1-M"):
        f, r = substitute(full, roar, rows, m7, cond)
        sp, w, pos = h1_family(f, r, STUDIED, M7)
        for q, v in (("H1 mean pairwise Spearman (3 explainers, 7 metrics)", sp), ("H1 Kendall W", w)):
            g = get(q, cond)
            check(f"{cond}: {q}", max(abs(v[0] - g["mean"]), abs(v[1] - g["lo"]), abs(v[2] - g["hi"])) <= TOL,
                  f"{v[0]:.4f} [{v[1]:.4f}, {v[2]:.4f}]")
        for q, args in (("H1 four explainers (Spearman)", (ALL, M7, False)),
                        ("H1 second baseline (Spearman)", (STUDIED, M7, True)),
                        ("H1 six metrics, no M4 (Spearman)", (STUDIED, [m for m in M7 if m != "m4_corr"], False))):
            v = h1_family(f, r, *args[:2], baseline2=args[2])[0]
            g = get(q, cond)
            check(f"{cond}: {q}", max(abs(v[0] - g["mean"]), abs(v[1] - g["lo"]), abs(v[2] - g["hi"])) <= TOL, f"{v[0]:.4f}")
        v = h2(f, ALL)
        g = get("H2 omnibus (4 explainers)", cond)
        check(f"{cond}: H2 omnibus", max(abs(v[0] - g["mean"]), abs(v[1] - g["lo"]), abs(v[2] - g["hi"])) <= TOL, f"{v[0]:.4f}")
        pb = pd.read_csv(AN / cond.replace("-", "").lower() / "positions_by_metric.csv").set_index(["metric", "explainer"])
        bad = sum(int(pb.loc[k, c]) != pos[k].get(c, 0) for k in pos for c in ("r1", "r2", "r3", "tied"))
        check(f"{cond}: explainer rank positions", bad == 0, f"{bad} mismatched cells")


def main():
    self_test()
    full, roar = load_raw()
    shards, rows, m7 = load_s1(full)
    check_alignment(full, rows)
    check_conversion(shards, rows)
    check_m7(rows, m7)
    check_summaries(full, roar, rows, m7)
    print(f"\n{len(fails)} failed check(s): {fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
