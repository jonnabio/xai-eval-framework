#!/usr/bin/env python3
"""Paper B revision 1: post-hoc measurement controls on the stored vectors (WP4 c-e, WP4b).

    py scripts/paper_b_posthoc.py [--root RESULTS] [--out DIR] [--dataset adult]

No explainer is re-run: everything is computed from the attribution vectors that the quality
rows store (`weights`, `stability_vectors`) and from the frozen models.

- Stability on the full vectors by three measures: cosine (as the main protocol), mean
  pairwise Spearman rank correlation of |e|, and mean pairwise top-k Jaccard (k = 5); and the
  cosine with all-zero vectors excluded (WP4 c, d).
- Ceiling-free concentration (WP4, sparsity): share of sum |e| in the top 5 features, and the
  normalized entropy of |e| / sum |e| (1 = uniform, 0 = one feature).
- Masking schemes (WP4b): the prediction change when the top-5 features of each explanation
  are masked by (1) zero, (2) the training mean, (3) a value drawn from the training marginal,
  (4) the training mean of the whole group: one-hot groups and the pair education /
  education-num are masked together when any member is in the top 5.

Writes posthoc_rows.csv, posthoc_stability.csv, posthoc_masking.csv and POSTHOC.md to
outputs/analysis/paper_b_rev1/.
"""
from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_b_lib as lib  # noqa: E402

OUT = lib.ROOT / "outputs" / "analysis" / "paper_b_rev1"
K = 5
SCHEMES = ("zero", "mean", "marginal", "grouped_mean")
EXTRA_GROUPS = {"adult": [("education", "education-num")]}   # associated features


# ------------------------------------------------------------------ pure measures (tested)
def pairwise(vecs: list[np.ndarray], fn) -> float:
    vals = [fn(a, b) for a, b in itertools.combinations(vecs, 2)]
    vals = [v for v in vals if v == v]
    return float(np.mean(vals)) if vals else float("nan")


def cosine(a, b) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return 0.0 if na == 0 or nb == 0 else float(a @ b / (na * nb))


def spearman_abs(a, b) -> float:
    a, b = np.abs(a), np.abs(b)
    if np.ptp(a) == 0 or np.ptp(b) == 0:
        return float("nan")
    return float(stats.spearmanr(a, b).statistic)


def topk_jaccard(a, b, k: int = K) -> float:
    ta = set(np.argsort(-np.abs(a))[:k][np.abs(a)[np.argsort(-np.abs(a))[:k]] > 0])
    tb = set(np.argsort(-np.abs(b))[:k][np.abs(b)[np.argsort(-np.abs(b))[:k]] > 0])
    u = ta | tb
    return float(len(ta & tb) / len(u)) if u else float("nan")


def concentration(w, k: int = K) -> tuple[float, float]:
    a = np.abs(np.asarray(w, float))
    s = a.sum()
    if s == 0:
        return float("nan"), float("nan")
    top = np.sort(a)[::-1][:k].sum() / s
    p = a[a > 0] / s
    ent = float(-(p * np.log(p)).sum() / np.log(len(a))) if len(a) > 1 else 0.0
    return float(top), ent


def mask_groups(names, dataset: str, X_train) -> list[list[int]]:
    _num, groups = lib.onehot_groups(names, X_train)
    out = [list(v) for v in groups.values()]
    idx = {str(n): j for j, n in enumerate(names)}
    for grp in EXTRA_GROUPS.get(dataset, []):
        # a member is a plain column (education-num) or a one-hot group by its prefix
        # (education -> education_*)
        js = [idx[g] for g in grp if g in idx]
        for g in grp:
            js += groups.get(g, [])
        merged = set(js)
        for g in out:
            if merged & set(g):
                merged |= set(g)
        out = [g for g in out if not (set(g) & merged)] + [sorted(merged)]
    return out


def masked(x, top, scheme: str, X_train, mean, groups, rng) -> np.ndarray:
    z = np.array(x, float).copy()
    cols = set(int(j) for j in top)
    if scheme == "grouped_mean":
        for g in groups:
            if cols & set(g):
                cols |= set(g)
    cols = sorted(cols)
    if scheme == "zero":
        z[cols] = 0.0
    elif scheme in ("mean", "grouped_mean"):
        z[cols] = mean[cols]
    elif scheme == "marginal":
        z[cols] = X_train[rng.integers(0, len(X_train)), cols]
    else:
        raise ValueError(scheme)
    return z


# ------------------------------------------------------------------ driver
def run(root: Path, out: Path, dataset: str) -> int:
    recs, mrecs = [], []
    data = lib.load_dataset(dataset)
    Xtr, Xte = data["X_train"], data["X_test"]
    mean = Xtr.mean(axis=0)
    groups = mask_groups(data["feature_names"], dataset, Xtr)
    for mdir in sorted((root / "quality" / dataset).glob("*")):
        model_name = mdir.name
        model, _ = lib.load_model_checked(dataset, model_name)
        for f in sorted(mdir.glob("seed_*/*.jsonl")):
            seed, expl = int(f.parent.name.split("_")[1]), f.stem
            rng = np.random.default_rng(lib.instance_seed(seed, dataset, model_name, expl, "mask"))
            batch, meta = [], []
            for r in lib.read_jsonl(f):
                if r.get("failed") or "weights" not in r:
                    continue
                w = np.asarray(r["weights"], float)
                top_share, ent = concentration(w)
                rec = {"dataset": dataset, "model": model_name, "seed": seed, "explainer": expl,
                       "instance_id": int(r["instance_id"]), "top5_share": top_share,
                       "entropy_norm": ent}
                sv = r.get("stability_vectors")
                if sv:
                    vecs = [np.asarray(v, float) for v in sv]
                    nz = [v for v in vecs if np.any(np.abs(v) >= 1e-4)]
                    rec.update({"stab_cosine": pairwise(vecs, cosine),
                                "stab_cosine_nonzero": pairwise(nz, cosine) if len(nz) > 1 else float("nan"),
                                "stab_spearman": pairwise(vecs, spearman_abs),
                                "stab_top5_jaccard": pairwise(vecs, topk_jaccard),
                                "zero_vectors": len(vecs) - len(nz),
                                "stab_stored": r.get("stability")})
                recs.append(rec)
                if np.all(np.abs(w) < 1e-4):
                    continue
                x = Xte[int(r["instance_id"])]
                if "prediction" in r and int(model.predict(x.reshape(1, -1))[0]) != int(r["prediction"]):
                    raise RuntimeError(f"{f}: instance {r['instance_id']} does not index the "
                                       "test split as stored (prediction differs)")
                top = np.argsort(-np.abs(w))[:K]
                for sc in SCHEMES:
                    batch.append(masked(x, top, sc, Xtr, mean, groups, rng))
                    meta.append((rec, sc))
                batch.append(x)
                meta.append((rec, "original"))
            if not batch:
                continue
            p = model.predict_proba(np.vstack(batch))[:, 1]
            orig = {}
            for (rec, sc), pv in zip(meta, p):
                if sc == "original":
                    orig[rec["instance_id"]] = pv
            for (rec, sc), pv in zip(meta, p):
                if sc != "original":
                    mrecs.append({k: rec[k] for k in ("dataset", "model", "seed", "explainer",
                                                      "instance_id")} |
                                 {"scheme": sc, "drop": abs(orig[rec["instance_id"]] - pv)})
    rows, mk = pd.DataFrame(recs), pd.DataFrame(mrecs)
    if rows.empty:
        print("no rows")
        return 1
    out.mkdir(parents=True, exist_ok=True)
    rows.to_csv(out / "posthoc_rows.csv", index=False)
    mk.to_csv(out / "posthoc_masking.csv", index=False)
    stab_cols = [c for c in ("stab_cosine", "stab_cosine_nonzero", "stab_spearman",
                             "stab_top5_jaccard", "zero_vectors", "top5_share", "entropy_norm")
                 if c in rows]
    st = rows.groupby(["model", "explainer"])[stab_cols].mean().reset_index()
    st.to_csv(out / "posthoc_stability.csv", index=False)
    # SHAP - X top-5 drop gap per scheme and model (cell means, then mean over cells)
    lines = ["# Post-hoc measurement controls (cohort B2)", "", f"Dataset: {dataset}; rows: "
             f"{len(rows):,}; masking rows: {len(mk):,}", "",
             "## Stability by measure and concentration (means over instances)", "",
             st.to_csv(index=False, float_format="%.4g"), "",
             "## Top-5 masking: SHAP minus X, mean of cell means, and cells with SHAP ahead", ""]
    if not mk.empty:
        cm = mk.groupby(["model", "seed", "explainer", "scheme"])["drop"].mean().unstack("explainer")
        res = []
        for x in [c for c in cm.columns if c != "shap"]:
            if "shap" not in cm:
                break
            d = (cm["shap"] - cm[x]).dropna().reset_index(name="gap")
            for (m, sc), g in d.groupby(["model", "scheme"]):
                res.append({"model": m, "contrast": f"shap-{x}", "scheme": sc,
                            "gap_mean": g["gap"].mean(), "cells": len(g),
                            "cells_shap_ahead": int((g["gap"] > 0).sum())})
        rs = pd.DataFrame(res)
        rs.to_csv(out / "posthoc_masking_gaps.csv", index=False)
        lines.append(rs.to_csv(index=False, float_format="%.4g") if not rs.empty else "_(none)_")
    (out / "POSTHOC.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"post-hoc written to {out} ({len(rows):,} rows)")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=lib.RESULTS)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--dataset", default="adult")
    a = ap.parse_args(argv)
    return run(a.root, a.out, a.dataset)


if __name__ == "__main__":
    raise SystemExit(main())
