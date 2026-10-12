#!/usr/bin/env python3
"""Paper F: counts and an audit asked for by the Codex review of 2026-10-12.

    python scripts/paper_f_posthoc_protocol.py [--results DIR] [--runs DIR]

MADE AFTER THE RESULTS WERE SEEN (ANALYSIS_PLAN.md, section 12, 2026-10-12). Nothing here is
a test and no result of the planned analysis changes.

1. Counts, from results/instances.csv.gz and results/cells.csv, written to
   results/posthoc_protocol.csv (metric, key, value):

    anchors_over_budget, mask|top5   share of the successful Anchors instances whose rule
        names more features than the faithfulness gap masks (m) or than the stability
        measure compares (5). All features of a rule have weight 1, so in these instances
        the features used are chosen by column index (paper_f_lib.top_set).
    mean_success_cost_faster, anchors|dice   number of datasets in which the method is the
        faster of the two when the cost of a run is the mean of its SUCCESSFUL instances.
        With posthoc_descriptives.csv this separates the two things that differ between
        the planned mean (failures take the worst value) and the run median of successes.
    absdiff_median, <measure>_<a>-<b>   median over the datasets of the absolute difference
        between the dataset means of two methods (cells.csv, the planned values)
    range_median, <measure>         median over the datasets of the difference between the
        largest and the smallest of the four dataset means
    cost_ratio_median, <a>-<b>|range   median over the datasets of the larger of two
        dataset mean costs divided by the smaller; "range" is slowest over fastest of four

2. Audit of resumed jobs, from the working directory of the run (runs/, local, not in the
   archive), written to results/audit_resume.csv when that directory exists. A job that was
   stopped and started again builds its explanation method anew; for LIME, whose random
   generator advances with every explanation, the instances explained after the restart
   then get other draws than an uninterrupted job would give. For each job file: the time
   from its creation to its last write, the sum of the times of its rows, and their
   difference. A job is flagged when the difference is more than SLACK_S seconds and more
   than half of the summed time. The file times are those of the author's disk: the audit
   cannot be repeated from the archive, and its result is a dated record.
"""
from __future__ import annotations

import argparse
import itertools
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_f_lib as lib  # noqa: E402
from paper_f_posthoc_descriptives import MASK_FRACTION, encoded_features  # noqa: E402

METHODS = ["lime", "shap", "anchors", "dice"]
TOP_K = 5                    # paper_f_config.toml, measures.top_k
SLACK_S = 300.0              # set-up of a job (data, classifier, explainer) and disk delays
PAIRS = {"gap": [("anchors", "dice"), ("lime", "anchors"), ("lime", "shap")],
         "stability": [("lime", "anchors")],
         "sparsity": [("anchors", "dice")]}


def counts(inst: pd.DataFrame, cells: pd.DataFrame) -> pd.DataFrame:
    rows: list[tuple[str, str, float]] = []
    d = encoded_features(inst)
    ok = inst[inst["failed"] == 0]
    anchors = ok[ok["explainer"] == "anchors"]
    m = anchors["dataset"].map(d).map(lambda v: max(1, math.ceil(MASK_FRACTION * v)))
    rows.append(("anchors_over_budget", "mask", float((anchors["n_used"] > m).mean())))
    rows.append(("anchors_over_budget", "top5", float((anchors["n_used"] > TOP_K).mean())))

    run_mean = ok.groupby(["dataset", "model", "explainer", "seed"])["cost_ms"].mean()
    success = run_mean.groupby(["dataset", "explainer"]).mean().unstack("explainer")
    rows.append(("mean_success_cost_faster", "anchors",
                 float((success["anchors"] < success["dice"]).sum())))
    rows.append(("mean_success_cost_faster", "dice",
                 float((success["dice"] < success["anchors"]).sum())))

    for measure in ("gap", "stability", "sparsity"):
        table = cells.groupby(["dataset", "explainer"])[measure].mean().unstack("explainer")[METHODS]
        rows.append(("range_median", measure,
                     float((table.max(axis=1) - table.min(axis=1)).median())))
        for a, b in PAIRS[measure]:
            rows.append(("absdiff_median", f"{measure}_{a}-{b}",
                         float((table[a] - table[b]).abs().median())))
    cost = cells.groupby(["dataset", "explainer"])["cost_ms"].mean().unstack("explainer")[METHODS]
    for a, b in (("anchors", "dice"), ("lime", "shap")):
        pair = cost[[a, b]]
        rows.append(("cost_ratio_median", f"{a}-{b}",
                     float((pair.max(axis=1) / pair.min(axis=1)).median())))
    rows.append(("cost_ratio_median", "range", float((cost.max(axis=1) / cost.min(axis=1)).median())))
    return pd.DataFrame(rows, columns=["metric", "key", "value"])


def audit(runs: Path, inst: pd.DataFrame) -> pd.DataFrame:
    """One row per job file: time on disk against the time of its rows."""
    work = inst.groupby(["dataset", "model", "seed", "explainer"])["total_s"].sum()
    rows = []
    for path in sorted(runs.glob("*/*/seed_*/*.jsonl")):
        dataset, model, seed = path.relative_to(runs).parts[:3]
        key = (dataset, model, int(seed.removeprefix("seed_")), path.stem)
        stat = path.stat()
        span = stat.st_mtime - getattr(stat, "st_birthtime", stat.st_ctime)   # creation time
        rows.append({"dataset": key[0], "model": key[1], "seed": key[2], "explainer": key[3],
                     "span_s": span, "rows_s": float(work.get(key, np.nan))})
    out = pd.DataFrame(rows)
    out["excess_s"] = out["span_s"] - out["rows_s"]
    out["flagged"] = ((out["excess_s"] > SLACK_S)
                      & (out["excess_s"] > 0.5 * out["rows_s"])).astype(int)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--results", default=str(lib.OUT / "results"))
    ap.add_argument("--runs", default=str(lib.OUT / "runs"))
    args = ap.parse_args()
    results, runs = Path(args.results), Path(args.runs)
    inst = pd.read_csv(results / "instances.csv.gz", low_memory=False)
    out = counts(inst, pd.read_csv(results / "cells.csv"))
    if runs.exists():
        table = audit(runs, inst)
        table.to_csv(results / "audit_resume.csv", index=False)
        flagged = table.groupby("explainer")["flagged"].agg(["sum", "count"])
        for e in METHODS:
            out.loc[len(out)] = ("jobs_flagged_resumed", e, float(flagged.loc[e, "sum"]))
            out.loc[len(out)] = ("jobs_audited", e, float(flagged.loc[e, "count"]))
        print(table[table["flagged"] == 1].sort_values("excess_s", ascending=False)
              .head(30).to_string(index=False))
    else:
        print(f"{runs} not found: the audit of resumed jobs is skipped")
    out.to_csv(results / "posthoc_protocol.csv", index=False)
    print(out.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
