#!/usr/bin/env python3
"""Summary values and the figure for Paper C, from committed files only.

Writes docs/reports/paper_c/results/summary.csv (columns metric,value) and
docs/reports/paper_c/figures/fig1.{pdf,png,tiff}. Nothing here is a new analysis: every
value is a count, a share or an extreme of a table that already exists.

    .venv/Scripts/python.exe docs/reports/paper_c/scripts/paper_c_summary.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
C = Path(__file__).resolve().parents[1]
ORIG = ROOT / "outputs" / "analysis" / "exp4_llm_evaluation"
C2A = ROOT / "outputs" / "analysis" / "exp4_cohort2"
C2 = ROOT / "experiments" / "exp4_cohort2"
PRIMARY = "hidden_label_primary"

DIMENSIONS = ["completeness", "semantic_plausibility", "overall_quality", "audit_usefulness",
              "concision", "clarity", "actionability"]
LABELS = {"completeness": "Completeness", "semantic_plausibility": "Semantic plausibility",
          "overall_quality": "Overall quality", "audit_usefulness": "Audit usefulness",
          "concision": "Concision", "clarity": "Clarity", "actionability": "Actionability"}


def summary() -> dict[str, float]:
    out: dict[str, float] = {}
    cases = [json.loads(line) for line in
             (C2 / "cases" / "exp4_cases.jsonl").open(encoding="utf-8")]
    out["cases"] = len(cases)
    for field in ("dataset", "explainer", "source_experiment", "quadrant"):
        for key, n in pd.Series([c[field] for c in cases]).value_counts().items():
            out[f"cases.{field}.{key}"] = n
    out["cases.model_families"] = len({c["model_family"] for c in cases})

    cov = pd.read_csv(C2A / "cohort2_coverage.csv")
    out["calls"] = cov["responses"].sum()
    out["parsed"] = cov["parsed"].sum()
    out["failed"] = cov["failed"].sum()

    scores = pd.read_csv(C2 / "parsed_scores" / "exp4_llm_scores.csv")
    primary = scores[scores["prompt_condition"] == PRIMARY]
    out["primary.actionability_share_1"] = (primary["actionability_score"] == 1).mean()
    by_judge = primary.groupby("judge_model")
    clarity_sd = by_judge["clarity_score"].std()
    clarity_mean = by_judge["clarity_score"].mean()
    low = clarity_sd.idxmin()
    out["primary.clarity_sd_min"] = clarity_sd[low]
    out["primary.clarity_offset_min_sd_judge"] = clarity_mean.drop(low).mean() - clarity_mean[low]

    for name, key in (("cohort2_label_bias", "label"), ("cohort2_rubric_sensitivity", "rubric")):
        shift = pd.read_csv(C2A / f"{name}.csv")["mean_shift"]
        out[f"{key}.shift_maxabs"] = shift.abs().max()
        out[f"{key}.shift_medianabs"] = shift.abs().median()

    retest = pd.read_csv(C2A / "cohort2_test_retest.csv")
    cols = [c for c in retest.columns if c.endswith("_score")]
    for judge, part in retest[retest["prompt_condition"] == PRIMARY].groupby("judge_model"):
        short = judge.split("/")[1].split("-")[0]
        out[f"retest.{short}.min"] = part[cols].min(axis=1).iloc[0]
        out[f"retest.{short}.max"] = part[cols].max(axis=1).iloc[0]

    views = pd.read_csv(C2A / "cohort2_reliability_by_view.csv")
    prim = views[views["view"] == PRIMARY]
    out["primary.icc_max"] = prim["icc_1_1"].max()
    out["primary.n_ci_upper_above_075"] = (prim["ci_upper"] > 0.75).sum()
    for view, part in views.groupby("view"):
        out[f"n_above_075.{view}"] = (part["icc_1_1"] > 0.75).sum()
    orig = pd.read_csv(ORIG / "icc_analysis.csv")
    out["orig.icc_max"] = orig["icc_2_1"].max()
    out["orig.ci_upper_max"] = orig["ci_upper"].max()
    out["orig.icc_n"] = orig["n_cases"].iloc[0]

    corpus = pd.read_csv(C / "paper_c_review_corpus.csv")
    out["corpus.size"] = len(corpus)
    for key, n in corpus["primary_cluster"].value_counts().items():
        out[f"corpus.cluster.{key}"] = n
    audit = pd.read_csv(C / "corpus_audit" / "second_reviewer_audit_results.csv")
    out["audit.records"] = len(audit)
    out["audit.adjudication_required"] = (audit["adjudication_required"] == "yes").sum()
    for axis in ("evaluation_target", "evidence_source", "quality_property", "task_context"):
        out[f"audit.exact.{axis}"] = (audit[f"{axis}_jaccard"] == 1).mean()

    out["human.sample"] = len(pd.read_csv(C / "human_subset" / "sample_cases.csv"))
    return out


def figure() -> None:
    orig = pd.read_csv(ORIG / "icc_analysis.csv").set_index("dimension")
    views = pd.read_csv(C2A / "cohort2_reliability_by_view.csv")
    new = views[views["view"] == PRIMARY].set_index("dimension")
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    for offset, frame, col, marker, colour, label in (
            (0.16, orig, "icc_2_1", "o", "#1f4e79", "First panel (147 complete cases)"),
            (-0.16, new, "icc_1_1", "s", "#c0504d", "Second panel (192 cases)")):
        ys = [len(DIMENSIONS) - 1 - i + offset for i in range(len(DIMENSIONS))]
        x = frame.loc[DIMENSIONS, col]
        err = [x - frame.loc[DIMENSIONS, "ci_lower"], frame.loc[DIMENSIONS, "ci_upper"] - x]
        ax.errorbar(x, ys, xerr=err, fmt=marker, color=colour, capsize=3, markersize=5,
                    linewidth=1.2, label=label)
    ax.axvline(0.75, color="black", linestyle="--", linewidth=1)
    ax.axvline(0, color="grey", linewidth=0.6)
    ax.set_yticks(range(len(DIMENSIONS)))
    ax.set_yticklabels([LABELS[d] for d in reversed(DIMENSIONS)])
    ax.set_xlabel("ICC(1,1) with 95% confidence interval")
    ax.set_xlim(-0.3, 1.0)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=8,
              frameon=False)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    out = C / "figures"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "fig1.pdf")
    fig.savefig(out / "fig1.png", dpi=300)
    fig.savefig(out / "fig1.tiff", dpi=300, pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)


def main() -> None:
    values = summary()
    path = C / "results" / "summary.csv"
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("metric,value\n")
        for key, value in values.items():
            fh.write(f"{key},{float(value):.6f}\n")
    figure()
    print(f"OK: {len(values)} summary values; figure in {C / 'figures'}")


if __name__ == "__main__":
    main()
