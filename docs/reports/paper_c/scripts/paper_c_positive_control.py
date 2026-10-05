#!/usr/bin/env python3
"""Analysis of the positive control (PLAN.md, section 18.3), fixed before the run.

Reads positive_control/parsed_scores/positive_control_llm_scores.csv and the scores of the
clean condition, and writes under docs/reports/paper_c/results/:

    positive_control.csv       version, judge (or "mean"), dimension -> mean paired difference
                               (version minus original), bootstrap interval, share of cases
                               scored lower, and the ICC(1,1) among the judges of the difference
    positive_control_icc.csv   set, scope, dimension -> ICC(1,1) among the judges; set is
                               "original" or "original+<version>"
    positive_control_summary.csv  metric,value (single values used in the text)

    .venv/Scripts/python.exe docs/reports/paper_c/scripts/paper_c_positive_control.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from paper_c_reliability import DIMS, coefficients

ROOT = Path(__file__).resolve().parents[4]
C = Path(__file__).resolve().parents[1]
OUT = C / "results"
SCORES = C / "positive_control" / "parsed_scores" / "positive_control_llm_scores.csv"
CLEAN = C / "clean_condition" / "parsed_scores" / "clean_llm_scores.csv"
CHANGED = ("truncated", "shuffled")
EXPECTED = {"truncated": "completeness", "shuffled": "semantic_plausibility"}
SCOPES = {"shap_lime_nonzero": ["shap", "lime"], "shap": ["shap"], "lime_nonzero": ["lime"]}
BOOTSTRAP_RESAMPLES = 4000
BOOTSTRAP_SEED = 20261005


def wide(frame: pd.DataFrame, dim: str) -> pd.DataFrame:
    """Cases by judges for one version; complete cases."""
    return frame.pivot_table(index="case_id", columns="judge_model", values=f"{dim}_score",
                             aggfunc="mean").dropna()


def interval(diff: np.ndarray, rng: np.random.Generator) -> tuple[float, float]:
    draws = rng.integers(0, len(diff), (BOOTSTRAP_RESAMPLES, len(diff)))
    lower, upper = np.percentile(diff[draws].mean(1), [2.5, 97.5])
    return float(lower), float(upper)


def main() -> None:
    cases = pd.DataFrame([json.loads(line) for line in (
        ROOT / "experiments" / "exp4_cohort2" / "cases" / "exp4_cases.jsonl").open(encoding="utf-8")])
    scores = pd.read_csv(SCORES).merge(cases[["case_id", "explainer"]], on="case_id")
    scores["version"] = scores["prompt_condition"].str.replace("control_", "", regex=False)
    by_version = {v: part for v, part in scores.groupby("version")}
    original = by_version["original"]
    rng = np.random.default_rng(BOOTSTRAP_SEED)

    shifts, iccs, summary = [], [], {}
    summary["calls.parsed"] = len(scores)
    summary["cases"] = scores["case_id"].nunique()

    for version in CHANGED:
        for dim in DIMS:
            a, b = wide(original, dim), wide(by_version[version], dim)
            ids = a.index.intersection(b.index)
            diff = b.loc[ids] - a.loc[ids]
            columns = {**{j: diff[j].to_numpy(float) for j in diff.columns},
                       "mean": diff.mean(1).to_numpy(float)}
            agreement = coefficients(diff.to_numpy(float))
            for judge, d in columns.items():
                lower, upper = interval(d, rng)
                shifts.append({"version": version, "judge_model": judge, "dimension": dim,
                               "n_cases": len(d), "mean_shift": d.mean(), "ci_lower": lower,
                               "ci_upper": upper, "share_lower": (d < 0).mean(),
                               "share_higher": (d > 0).mean(),
                               "icc_of_shift": agreement["icc_1_1"]})
        row = next(r for r in shifts if r["version"] == version and r["judge_model"] == "mean"
                   and r["dimension"] == EXPECTED[version])
        summary[f"{version}.passed"] = float(row["ci_upper"] < 0)

    for scope, explainers in SCOPES.items():
        base = original[original["explainer"].isin(explainers)]
        for dim in DIMS:
            iccs.append({"set": "original", "scope": scope, "dimension": dim,
                         **coefficients(wide(base, dim).to_numpy(float))})
            for version in CHANGED:
                part = by_version[version]
                part = part[part["explainer"].isin(explainers)]
                both = np.vstack([wide(base, dim).to_numpy(float), wide(part, dim).to_numpy(float)])
                iccs.append({"set": f"original+{version}", "scope": scope, "dimension": dim,
                             **coefficients(both)})

    # The original version against the clean condition: the same prompt on another day.
    clean = pd.read_csv(CLEAN)
    pair = original.merge(clean, on=["case_id", "judge_model"], suffixes=("_control", "_clean"))
    same = pd.DataFrame({d: pair[f"{d}_score_control"] == pair[f"{d}_score_clean"] for d in DIMS})
    for judge, part in same.groupby(pair["judge_model"]):
        summary[f"retest.{judge}.same_min"] = part.mean().min()
        summary[f"retest.{judge}.same_max"] = part.mean().max()
    summary["retest.same_all"] = same.to_numpy().mean()
    summary["dates.first"] = float(scores["timestamp_utc"].min()[:10].replace("-", ""))
    summary["dates.last"] = float(scores["timestamp_utc"].max()[:10].replace("-", ""))

    fmt = dict(index=False, float_format="%.6f", lineterminator="\n")
    pd.DataFrame(shifts).to_csv(OUT / "positive_control.csv", **fmt)
    pd.DataFrame(iccs).to_csv(OUT / "positive_control_icc.csv", **fmt)
    with (OUT / "positive_control_summary.csv").open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("metric,value\n")
        for key, value in summary.items():
            fh.write(f"{key},{float(value):.6f}\n")
    print(f"OK: positive control, {len(scores)} parsed responses, {summary['cases']} cases")


if __name__ == "__main__":
    main()
