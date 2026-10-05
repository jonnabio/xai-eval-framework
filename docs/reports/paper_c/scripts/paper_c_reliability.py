#!/usr/bin/env python3
"""Reliability analyses added after the rigor review (PLAN.md, sections 15.2 and 15.3).

All are post hoc and were fixed in the plan before this script was run. It reads the parsed
scores of cohort 2 and, when present, of the clean condition, and writes only under
docs/reports/paper_c/results/:

    reliability_long.csv       condition, scope, dimension -> coefficients and agreement
    variance_between.csv       dimension -> share of case-level variance between explainers
    first_panel_interval.csv   dimension -> F-based interval of the first panel's ICC
    judge_behaviour.csv        judge, condition -> share of responses naming a metric
    clean_shift.csv            judge, dimension -> mean paired difference, clean - primary
    clean_fidelity.csv         explainer -> Spearman of overall quality with fidelity
    review_summary.csv         metric,value (single values used in the text)

Conditions: primary3 (primary, three replicates averaged per judge), primary1 (primary,
replicate 1), clean (one call). Scopes: all, shap_lime, and each explainer.

    .venv/Scripts/python.exe docs/reports/paper_c/scripts/paper_c_reliability.py
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[4]
C = Path(__file__).resolve().parents[1]
C2 = ROOT / "experiments" / "exp4_cohort2"
ORIG = ROOT / "outputs" / "analysis" / "exp4_llm_evaluation"
OUT = C / "results"
CLEAN = C / "clean_condition" / "parsed_scores" / "clean_llm_scores.csv"

DIMS = ["completeness", "semantic_plausibility", "overall_quality", "audit_usefulness",
        "concision", "clarity", "actionability"]
METRIC_WORDS = r"fidelity|stability|sparsity|faithfulness"
SCOPES = {"all": None, "shap_lime": ["shap", "lime"], "shap": ["shap"], "lime": ["lime"],
          "anchors": ["anchors"], "dice": ["dice"]}


def matrix(scores: pd.DataFrame, dim: str) -> np.ndarray:
    """Cases by judges, the mean of whatever replicates the frame holds; complete cases."""
    return scores.pivot_table(index="case_id", columns="judge_model", values=f"{dim}_score",
                              aggfunc="mean").dropna().to_numpy(float)


def f_interval(icc: float, n: int, k: int) -> tuple[float, float]:
    """Exact 95% interval of ICC(1,1) from the F distribution (Shrout and Fleiss)."""
    f0 = (1 + (k - 1) * icc) / (1 - icc)
    fl = f0 / stats.f.ppf(0.975, n - 1, n * (k - 1))
    fu = f0 * stats.f.ppf(0.975, n * (k - 1), n - 1)
    return (fl - 1) / (fl + k - 1), (fu - 1) / (fu + k - 1)


def coefficients(x: np.ndarray) -> dict[str, float]:
    n, k = x.shape
    grand = x.mean()
    msr = k * ((x.mean(1) - grand) ** 2).sum() / (n - 1)
    msc = n * ((x.mean(0) - grand) ** 2).sum() / (k - 1)
    msw = ((x - x.mean(1, keepdims=True)) ** 2).sum() / (n * (k - 1))
    mse = ((x - x.mean(1, keepdims=True) - x.mean(0, keepdims=True) + grand) ** 2).sum() \
        / ((n - 1) * (k - 1))
    out = {"n_cases": n, "icc_1_1": np.nan, "ci_lower": np.nan, "ci_upper": np.nan,
           "icc_1_k": np.nan, "icc_2_1": np.nan, "icc_3_1": np.nan}
    if msr + (k - 1) * msw > 0:
        icc = (msr - msw) / (msr + (k - 1) * msw)
        out["icc_1_1"] = icc
        if icc < 1:
            out["ci_lower"], out["ci_upper"] = f_interval(icc, n, k)
    if msr > 0:
        out["icc_1_k"] = (msr - msw) / msr
    if msr + (k - 1) * mse > 0:
        out["icc_2_1"] = (msr - mse) / (msr + (k - 1) * mse + k * (msc - mse) / n)
        out["icc_3_1"] = (msr - mse) / (msr + (k - 1) * mse)
    return out


def raw_agreement(x: np.ndarray) -> dict[str, float]:
    pairs = list(combinations(range(x.shape[1]), 2))
    return {"pair_exact": float(np.mean([(x[:, a] == x[:, b]).mean() for a, b in pairs])),
            "pair_within_1": float(np.mean([(np.abs(x[:, a] - x[:, b]) <= 1).mean()
                                            for a, b in pairs]))}


def reliability(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for condition, frame in frames.items():
        for scope, explainers in SCOPES.items():
            part = frame if explainers is None else frame[frame["explainer"].isin(explainers)]
            for dim in DIMS:
                x = matrix(part, dim)
                row = {"condition": condition, "scope": scope, "dimension": dim,
                       **coefficients(x)}
                # Raw agreement is defined on single integer scores only.
                row.update(raw_agreement(x) if condition != "primary3"
                           else {"pair_exact": np.nan, "pair_within_1": np.nan})
                rows.append(row)
    return pd.DataFrame(rows)


def variance_between(primary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for dim in DIMS:
        means = primary.groupby(["case_id", "explainer"])[f"{dim}_score"].mean().reset_index()
        total = means[f"{dim}_score"].var(ddof=0)
        within = means.groupby("explainer")[f"{dim}_score"].transform(lambda v: v - v.mean())
        rows.append({"dimension": dim, "between_explainer_share": 1 - (within ** 2).mean() / total})
    return pd.DataFrame(rows)


def names_metric(frame: pd.DataFrame) -> pd.Series:
    cols = [c for c in frame.columns if c.endswith("_rationale")]
    text = frame[cols].fillna("").agg(" ".join, axis=1).str.lower()
    return text.str.contains(METRIC_WORDS, regex=True)


def holm(pvals: list[float]) -> list[float]:
    order = np.argsort(pvals)
    out, running = [np.nan] * len(pvals), 0.0
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, (len(pvals) - rank) * pvals[idx]))
        out[idx] = running
    return out


def main() -> None:
    OUT.mkdir(exist_ok=True)
    cases = pd.DataFrame([json.loads(line) for line in
                          (C2 / "cases" / "exp4_cases.jsonl").open(encoding="utf-8")])
    info = cases[["case_id", "explainer", "dataset", "quadrant"]].copy()
    info["fidelity"] = [m["fidelity"] for m in cases["technical_metrics"]]

    scores = pd.read_csv(C2 / "parsed_scores" / "exp4_llm_scores.csv")
    primary = scores[scores["prompt_condition"] == "hidden_label_primary"].merge(info, on="case_id")
    frames = {"primary3": primary, "primary1": primary[primary["replicate"] == 1]}
    has_clean = CLEAN.exists()
    if has_clean:
        frames["clean"] = pd.read_csv(CLEAN).merge(info, on="case_id")

    long = reliability(frames)
    long.to_csv(OUT / "reliability_long.csv", index=False, float_format="%.6f", lineterminator="\n")
    between = variance_between(primary)
    between.to_csv(OUT / "variance_between.csv", index=False, float_format="%.6f",
                   lineterminator="\n")

    orig = pd.read_csv(ORIG / "icc_analysis.csv")
    first = pd.DataFrame([{"dimension": r.dimension, "icc_1_1": r.icc_2_1,
                           **dict(zip(("ci_lower", "ci_upper"),
                                      f_interval(r.icc_2_1, int(r.n_cases), int(r.n_judges))))}
                          for r in orig.itertuples()])
    first.to_csv(OUT / "first_panel_interval.csv", index=False, float_format="%.6f",
                 lineterminator="\n")

    behaviour = []
    for condition, frame in frames.items():
        if condition == "primary3":
            continue
        share = names_metric(frame).groupby(frame["judge_model"]).mean()
        behaviour += [{"judge_model": j, "condition": condition, "names_metric_share": v}
                      for j, v in share.items()]
    pd.DataFrame(behaviour).to_csv(OUT / "judge_behaviour.csv", index=False,
                                   float_format="%.6f", lineterminator="\n")

    summary: dict[str, float] = {}
    means = primary.groupby(["case_id", "quadrant"])["overall_quality_score"].mean().reset_index()
    right = means[means["quadrant"].isin(["TP", "TN"])]["overall_quality_score"]
    wrong = means[means["quadrant"].isin(["FP", "FN"])]["overall_quality_score"]
    summary["label.mean_correct"] = right.mean()
    summary["label.mean_wrong"] = wrong.mean()
    summary["label.mwu_p"] = stats.mannwhitneyu(right, wrong).pvalue
    one = primary[primary["replicate"] == 1]["overall_quality_score"]
    summary["overall.modal_share"] = one.value_counts(normalize=True).max()
    summary["overall.modal_score"] = one.value_counts().idxmax()
    summary["cases.shap_lime"] = int(info["explainer"].isin(["shap", "lime"]).sum())
    summary["cases.anchors_dice"] = int(info["explainer"].isin(["anchors", "dice"]).sum())
    prim = long[(long["condition"] == "primary3") & (long["scope"] == "all")]
    summary["primary3.n_icc1k_above_075"] = int((prim["icc_1_k"] >= 0.75).sum())
    summary["primary3.n_ci_upper_above_075"] = int((prim["ci_upper"] > 0.75).sum())
    summary["first.ci_upper_max"] = first["ci_upper"].max()
    summary["between.max"] = between["between_explainer_share"].max()
    shap = long[(long["condition"] == "primary3") & (long["scope"] == "shap")]
    summary["shap.icc_max"] = shap["icc_1_1"].max()
    summary["anchors_dice.icc_max"] = long[(long["condition"] == "primary3")
                                           & long["scope"].isin(["anchors", "dice"])]["icc_1_1"].max()
    coverage = pd.read_csv(ROOT / "outputs" / "analysis" / "exp4_cohort2" / "cohort2_coverage.csv")
    clean_calls = len(list((C / "clean_condition" / "raw_responses").rglob("*.json")))
    summary["calls.total"] = coverage["responses"].sum() + clean_calls
    summary["calls.parsed"] = coverage["parsed"].sum() + (len(frames["clean"]) if has_clean else 0)
    summary["calls.clean"] = clean_calls
    summary["clean.available"] = float(has_clean)

    if has_clean:
        clean = frames["clean"]
        summary["clean.parsed"] = len(clean)
        summary["clean.cases_complete"] = len(matrix(clean, "overall_quality"))
        base = frames["primary1"]
        cols = [f"{d}_score" for d in DIMS]
        pair = clean.merge(base, on=["case_id", "judge_model"], suffixes=("_clean", "_primary"))
        shift = []
        for judge, part in pair.groupby("judge_model"):
            for dim, col in zip(DIMS, cols):
                diff = part[f"{col}_clean"] - part[f"{col}_primary"]
                shift.append({"judge_model": judge, "dimension": dim, "n_pairs": len(diff),
                              "mean_shift": diff.mean(), "share_changed": (diff != 0).mean()})
        shift = pd.DataFrame(shift)
        shift.to_csv(OUT / "clean_shift.csv", index=False, float_format="%.6f",
                     lineterminator="\n")
        summary["clean.shift_maxabs"] = shift["mean_shift"].abs().max()
        summary["clean.shift_overall_mean"] = \
            shift[shift["dimension"] == "overall_quality"]["mean_shift"].mean()

        rows = []
        for condition in ("primary1", "clean"):
            frame = frames[condition]
            case_mean = frame.groupby(["case_id", "explainer", "fidelity"])[
                "overall_quality_score"].mean().reset_index()
            block = []
            for explainer, part in sorted(case_mean.groupby("explainer")):
                rho, p = stats.spearmanr(part["fidelity"], part["overall_quality_score"])
                block.append({"condition": condition, "explainer": explainer,
                              "n_cases": len(part), "spearman_rho": rho, "p_value": p})
            for row, adj in zip(block, holm([b["p_value"] for b in block])):
                row["p_holm"] = adj
            rows += block
        pd.DataFrame(rows).to_csv(OUT / "clean_fidelity.csv", index=False, float_format="%.6f",
                                  lineterminator="\n")

    with (OUT / "review_summary.csv").open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("metric,value\n")
        for key, value in summary.items():
            fh.write(f"{key},{float(value):.6f}\n")
    print(f"OK: reliability tables in {OUT} (clean condition: {'yes' if has_clean else 'no'})")


if __name__ == "__main__":
    main()
