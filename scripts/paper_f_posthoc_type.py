#!/usr/bin/env python3
"""Paper F: the order of the methods by the type of features of a dataset.

    python scripts/paper_f_posthoc_type.py [--results DIR]

A COMPARISON MADE AFTER THE RESULTS WERE SEEN, asked for by Reviewer A of JCSI (2026-10-19;
ANALYSIS_PLAN.md, section 12). It tests nothing and changes no result of the planned
analysis; it describes where the comparisons that vary between datasets fall.

The type is the stratum of the plan, computed from the data (datasets.csv): numeric (no
categorical feature), mixed, categorical (one dataset, too few to compare). The size is the
second half of the stratum (under 10,000 rows or from 10,000).

Reads results/ranks.csv (rank 1 = best, the per-dataset ranks of the planned analysis) and
datasets.csv. Writes

    results/posthoc_type.csv    metric, key, value

    datasets, <type>                       number of datasets of the type
    shap_first_gap, <type>                 datasets where SHAP has rank 1 on the gap
    lime_above_anchors_stability, <type>   datasets where LIME is ranked above Anchors
    anchors_above_dice_sparsity, <type>    datasets where Anchors is ranked above DiCE
    modal_order_sparsity, <type>           datasets that share the most frequent order
    within, <type>_<measure>               mean Spearman correlation inside the type
    between_types, <measure>               mean Spearman correlation of a numeric and a
                                           mixed dataset
    within_size, <size>_<measure>          the same inside each size
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_f_analyze as an  # noqa: E402
import paper_f_lib as lib  # noqa: E402

TYPES = ("numeric", "mixed", "categorical")
SIZES = ("small", "large")
MEASURES = ("gap", "stability", "sparsity", "cost_ms")


def between(a: np.ndarray, b: np.ndarray) -> float:
    """Mean Spearman correlation over every pair of one row of `a` and one of `b`."""
    za, zb = an.standardise(a), an.standardise(b)
    return float((za @ zb.T).mean() / a.shape[1])


def describe(ranks: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
    kind = data.set_index("key")["stratum"].str.split("-").str[0]
    size = data.set_index("key")["stratum"].str.split("-").str[1]
    ranks = ranks.assign(type=ranks["dataset"].map(kind), size=ranks["dataset"].map(size))
    if ranks["type"].isna().any():
        raise ValueError("a dataset of ranks.csv has no stratum in datasets.csv")
    rows: list[tuple[str, str, float]] = []
    by = {m: ranks[ranks["measure"] == m] for m in MEASURES}
    for t in TYPES:
        g = {m: by[m][by[m]["type"] == t] for m in MEASURES}
        rows.append(("datasets", t, float(len(g["gap"]))))
        rows.append(("shap_first_gap", t, float((g["gap"]["shap"] == 1).sum())))
        s = g["stability"]
        rows.append(("lime_above_anchors_stability", t, float((s["lime"] < s["anchors"]).sum())))
        s = g["sparsity"]
        rows.append(("anchors_above_dice_sparsity", t, float((s["anchors"] < s["dice"]).sum())))
        order = s[an.EXPL].astype(str).agg("-".join, axis=1)
        rows.append(("modal_order_sparsity", t, float(order.value_counts().max())))
        if len(g["gap"]) > 1:
            for m in MEASURES:
                rows.append(("within", f"{t}_{m}",
                             float(an.mean_corr(an.standardise(g[m][an.EXPL].to_numpy())))))
    for m in MEASURES:
        num = by[m][by[m]["type"] == "numeric"][an.EXPL].to_numpy()
        mix = by[m][by[m]["type"] == "mixed"][an.EXPL].to_numpy()
        rows.append(("between_types", m, between(num, mix)))
        for z in SIZES:
            part = by[m][by[m]["size"] == z][an.EXPL].to_numpy()
            rows.append(("within_size", f"{z}_{m}", float(an.mean_corr(an.standardise(part)))))
    return pd.DataFrame(rows, columns=["metric", "key", "value"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--results", default=str(lib.OUT / "results"))
    args = ap.parse_args()
    results = Path(args.results)
    out = describe(pd.read_csv(results / "ranks.csv"), pd.read_csv(results.parent / "datasets.csv"))
    out.to_csv(results / "posthoc_type.csv", index=False)
    print(out.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
