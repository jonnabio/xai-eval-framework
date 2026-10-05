#!/usr/bin/env python3
"""Post hoc analysis for Paper C: judge scores against the technical metrics.

Fixed in docs/reports/paper_c/PLAN.md, section 7, before it was run. The judges were shown
the metrics in the prompt (PLAN.md, section 14.2), so the result is "how closely the scores
follow the metrics shown", nothing more.

Data: cohort 2, condition hidden_label_primary, mean of the three judges and the three
replicates per case. Reads experiments/exp4_cohort2/ and writes only under
docs/reports/paper_c/results/.

    .venv/Scripts/python.exe docs/reports/paper_c/scripts/paper_c_posthoc.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[4]
C2 = ROOT / "experiments" / "exp4_cohort2"
OUT = Path(__file__).resolve().parents[1] / "results"

CONDITION = "hidden_label_primary"
DIMENSIONS = ["overall_quality", "clarity", "completeness", "concision",
              "semantic_plausibility", "audit_usefulness", "actionability"]
PRIMARY = "overall_quality"
METRICS = ["fidelity", "stability", "sparsity", "faithfulness_gap", "cost"]
MIN_CASES = 20      # a cell with fewer cases is reported without a test
N_BOOT = 5000
SEED = 20261004


def load() -> pd.DataFrame:
    """One row per case: strata, technical metrics and mean judge score per dimension."""
    cases = [json.loads(line) for line in
             (C2 / "cases" / "exp4_cases.jsonl").open(encoding="utf-8")]
    frame = pd.DataFrame([
        {"case_id": c["case_id"], "dataset": c["dataset"], "explainer": c["explainer"],
         **{m: c["technical_metrics"][m] for m in METRICS}}
        for c in cases
    ])
    scores = pd.read_csv(C2 / "parsed_scores" / "exp4_llm_scores.csv")
    scores = scores[scores["prompt_condition"] == CONDITION]
    means = scores.groupby("case_id")[[f"{d}_score" for d in DIMENSIONS]].mean()
    means.columns = DIMENSIONS
    return frame.merge(means, left_on="case_id", right_index=True, validate="one_to_one")


def spearman_ci(x: np.ndarray, y: np.ndarray, rng: np.random.Generator):
    """Spearman correlation, its p-value and a percentile bootstrap interval over cases."""
    if len(np.unique(x)) < 2 or len(np.unique(y)) < 2:
        return np.nan, np.nan, np.nan, np.nan
    rho, p = stats.spearmanr(x, y)
    boots = []
    n = len(x)
    for _ in range(N_BOOT):
        idx = rng.integers(0, n, n)
        if len(np.unique(x[idx])) > 1 and len(np.unique(y[idx])) > 1:
            boots.append(stats.spearmanr(x[idx], y[idx])[0])
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return rho, p, lo, hi


def holm(pvals: pd.Series) -> pd.Series:
    """Holm-adjusted p-values; missing values stay missing and are not counted."""
    out = pd.Series(np.nan, index=pvals.index)
    valid = pvals.dropna().sort_values()
    m, running = len(valid), 0.0
    for rank, (idx, p) in enumerate(valid.items()):
        running = max(running, min(1.0, (m - rank) * p))
        out[idx] = running
    return out


def within_explainer(data: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    rows = []
    for explainer, part in sorted(data.groupby("explainer")):
        for dim in DIMENSIONS:
            for metric in METRICS:
                x, y = part[metric].to_numpy(float), part[dim].to_numpy(float)
                tested = len(part) >= MIN_CASES
                rho, p, lo, hi = spearman_ci(x, y, rng) if tested else (np.nan,) * 4
                rows.append({"explainer": explainer, "dimension": dim, "metric": metric,
                             "n_cases": len(part), "spearman_rho": rho, "ci_lower": lo,
                             "ci_upper": hi, "p_value": p})
    out = pd.DataFrame(rows)
    # Holm over the 20 tests of the primary outcome (5 metrics in each of 4 explainers).
    # The other dimensions are descriptive and carry no adjusted p-value.
    out["p_holm"] = np.nan
    primary = out["dimension"] == PRIMARY
    out.loc[primary, "p_holm"] = holm(out.loc[primary, "p_value"])
    return out


def rank_regression(data: pd.DataFrame) -> pd.DataFrame:
    """Rank of the score on rank of the metric, with explainer and dataset as strata."""
    rows = []
    strata = pd.get_dummies(data[["explainer", "dataset"]], drop_first=True).to_numpy(float)
    for dim in DIMENSIONS:
        for metric in METRICS:
            y = stats.rankdata(data[dim])
            x = stats.rankdata(data[metric])
            design = np.column_stack([np.ones(len(data)), x, strata])
            beta, *_ = np.linalg.lstsq(design, y, rcond=None)
            resid = y - design @ beta
            dof = len(y) - np.linalg.matrix_rank(design)
            cov = (resid @ resid / dof) * np.linalg.pinv(design.T @ design)
            se = float(np.sqrt(cov[1, 1]))
            t = beta[1] / se
            rows.append({"dimension": dim, "metric": metric, "n_cases": len(data),
                         "rank_slope": beta[1], "std_error": se, "t": t,
                         "p_value": 2 * stats.t.sf(abs(t), dof)})
    out = pd.DataFrame(rows)
    out["p_holm"] = np.nan
    primary = out["dimension"] == PRIMARY
    out.loc[primary, "p_holm"] = holm(out.loc[primary, "p_value"])
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data = load()
    assert len(data) == 192 and not data[DIMENSIONS + METRICS].isna().any().any()
    within_explainer(data).to_csv(OUT / "posthoc_scores_vs_metrics.csv", index=False,
                                  float_format="%.6f", lineterminator="\n")
    rank_regression(data).to_csv(OUT / "posthoc_rank_regression.csv", index=False,
                                 float_format="%.6f", lineterminator="\n")
    print(f"OK: {len(data)} cases; results in {OUT}")


if __name__ == "__main__":
    main()
