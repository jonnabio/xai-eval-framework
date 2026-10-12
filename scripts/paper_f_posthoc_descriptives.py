#!/usr/bin/env python3
"""Paper F: descriptive figures asked for by the independent review of 2026-10-12.

    python scripts/paper_f_posthoc_descriptives.py [--results DIR]

COUNTS MADE AFTER THE RESULTS WERE SEEN (ANALYSIS_PLAN.md, section 12, 2026-10-12). They
test nothing and change no result of the planned analysis; they describe how the measures
behave, so that the paper can say what part of an order follows from the output format and
the settings of a method.

Reads results/instances.csv.gz, the per-instance rows the planned analysis wrote. Writes

    results/posthoc_descriptives.csv    metric, key, value

    features_used, <method>      mean number of features an explanation names
    features_masked, <method>    mean number of features the faithfulness gap masks:
                                 min(features named, m), m = max(1, ceil(0.2 d)), as in
                                 scripts/paper_f_lib.py (faithfulness)
        Both are means of the successful instances of each dataset and classifier, then of
        the 64 dataset-and-classifier cells, as secondary.csv is computed.
    encoded_features, min|max    smallest and largest number of encoded features d
    median_cost_faster, <method> number of datasets in which the method is the faster of
                                 Anchors and DiCE when the cost of a run is the median, not
                                 the mean, of its successful instances (mean of the runs
                                 of a dataset)
    mean_cost_faster, <method>   the same with the mean of the planned analysis (cells.csv)
    failures_time_limit, <method>   failed instances whose reason is the time limit
    failures_other, <method>        the other failed instances
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_f_lib as lib  # noqa: E402

METHODS = ["lime", "shap", "anchors", "dice"]
MASK_FRACTION = 0.2          # paper_f_config.toml, measures.mask_fraction
PAIR = ("anchors", "dice")


def encoded_features(inst: pd.DataFrame) -> pd.Series:
    """d of each dataset, from sparsity = 1 - features named / d."""
    ok = inst[(inst["failed"] == 0) & (inst["sparsity"] < 1) & (inst["n_used"] > 0)]
    d = (ok["n_used"] / (1 - ok["sparsity"])).round().astype(int)
    per = d.groupby(ok["dataset"]).agg(["min", "max"])
    if (per["min"] != per["max"]).any():
        raise ValueError("the number of encoded features is not constant inside a dataset")
    return per["max"]


def describe(inst: pd.DataFrame, cells: pd.DataFrame) -> pd.DataFrame:
    rows: list[tuple[str, str, float]] = []
    d = encoded_features(inst)
    ok = inst[inst["failed"] == 0].copy()
    m = ok["dataset"].map(d).map(lambda v: max(1, math.ceil(MASK_FRACTION * v)))
    ok["masked"] = np.minimum(ok["n_used"], m)
    cell = ok.groupby(["dataset", "model", "explainer"])[["n_used", "masked"]].mean()
    by_method = cell.groupby("explainer").mean()
    for e in METHODS:
        rows.append(("features_used", e, float(by_method.loc[e, "n_used"])))
        rows.append(("features_masked", e, float(by_method.loc[e, "masked"])))
    rows += [("encoded_features", "min", float(d.min())), ("encoded_features", "max", float(d.max()))]

    run_median = ok.groupby(["dataset", "model", "explainer", "seed"])["cost_ms"].median()
    med = run_median.groupby(["dataset", "explainer"]).mean().unstack("explainer")
    mean = cells.groupby(["dataset", "explainer"])["cost_ms"].mean().unstack("explainer")
    for label, table in (("median_cost_faster", med), ("mean_cost_faster", mean)):
        a, b = PAIR
        rows.append((label, a, float((table[a] < table[b]).sum())))
        rows.append((label, b, float((table[b] < table[a]).sum())))

    bad = inst[inst["failed"] == 1]
    limit = bad["fail_reason"].fillna("").str.startswith("time limit")
    for e in METHODS:
        mine = bad["explainer"] == e
        rows.append(("failures_time_limit", e, float((mine & limit).sum())))
        rows.append(("failures_other", e, float((mine & ~limit).sum())))
    return pd.DataFrame(rows, columns=["metric", "key", "value"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--results", default=str(lib.OUT / "results"))
    args = ap.parse_args()
    results = Path(args.results)
    out = describe(pd.read_csv(results / "instances.csv.gz"), pd.read_csv(results / "cells.csv"))
    out.to_csv(results / "posthoc_descriptives.csv", index=False)
    print(out.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
