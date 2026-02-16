#!/usr/bin/env python3
"""
Generate publication figures for Paper A from repository artifacts.

Outputs:
    outputs/paper_a_figures/figures/*.pdf
    outputs/paper_a_figures/figure_summary.json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import FancyBboxPatch


PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXP2_RESULTS_DIR = PROJECT_ROOT / "experiments" / "exp2_scaled" / "results"
EXP1_REPRO_CSV = (
    PROJECT_ROOT / "experiments" / "exp1_adult" / "reproducibility" / "reproducibility_report.csv"
)
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "paper_a_figures"
FIGURES_DIR = OUTPUT_DIR / "figures"

METRICS = ["fidelity", "stability", "sparsity", "faithfulness_gap", "cost"]
METHOD_ORDER = ["shap", "lime", "anchors", "dice"]
MODEL_ORDER = ["logreg", "rf", "xgb", "svm", "mlp"]
SEED_ORDER = [42, 123, 456, 789, 999]
N_ORDER = [50, 100, 200]
EXPECTED_RUNS_PER_MODEL_METHOD = len(SEED_ORDER) * len(N_ORDER)

METHOD_COLORS = {
    "shap": "#D55E00",
    "lime": "#0072B2",
    "anchors": "#009E73",
    "dice": "#CC79A7",
}


def setup_style() -> None:
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "pdf.fonttype": 42,
            "savefig.dpi": 300,
        }
    )


def parse_results_file(path: Path) -> Tuple[Dict[str, float], str]:
    try:
        payload = json.loads(path.read_text())
    except Exception:
        return {}, "json_error"

    instance_rows = payload.get("instance_evaluations", [])
    if not instance_rows:
        # Fallback: use aggregated metrics when available
        agg = payload.get("aggregated_metrics", {}) or {}
        mapped: Dict[str, float] = {}
        key_map = {
            "fidelity": "fidelity",
            "stability": "stability",
            "sparsity": "sparsity",
            "faithfulness_gap": "faithfulness_gap",
            "cost": "cost",
            "efficiencyms": "cost",
        }
        for k, v in agg.items():
            out_key = key_map.get(str(k).strip().lower())
            if out_key is None:
                continue
            if isinstance(v, dict) and "mean" in v:
                mapped[out_key] = float(v["mean"])
            elif isinstance(v, (int, float)):
                mapped[out_key] = float(v)
        if mapped:
            return mapped, "ok_aggregated"
        return {}, "empty"

    metric_values: Dict[str, List[float]] = {m: [] for m in METRICS}
    for row in instance_rows:
        metrics = row.get("metrics", {})
        for metric in METRICS:
            value = metrics.get(metric)
            if value is not None:
                metric_values[metric].append(value)

    means: Dict[str, float] = {}
    for metric, values in metric_values.items():
        if values:
            means[metric] = float(np.mean(values))

    # Use wall-clock duration normalized by evaluated instances for cost,
    # matching the aggregate definition used in manuscript tables.
    duration = payload.get("experiment_metadata", {}).get("duration_seconds")
    if duration is not None and len(instance_rows) > 0:
        means["cost"] = float(duration) * 1000.0 / len(instance_rows)

    return means, "ok_instance"


def load_exp2_scaled_runs() -> Tuple[pd.DataFrame, pd.DataFrame]:
    records: List[Dict[str, object]] = []
    file_records: List[Dict[str, object]] = []

    for path in EXP2_RESULTS_DIR.glob("*/*/n_*/results.json"):
        model, method = path.parts[-4].split("_", 1)
        seed = int(path.parts[-3].split("_")[1])
        n_value = int(path.parts[-2].split("_")[1])

        metric_means, status = parse_results_file(path)
        file_records.append(
            {
                "model": model,
                "method": method,
                "seed": seed,
                "n": n_value,
                "path": str(path),
                "status": status,
            }
        )
        if status not in {"ok_instance", "ok_aggregated"}:
            continue

        record = {
            "model": model,
            "method": method,
            "seed": seed,
            "n": n_value,
            "path": str(path),
        }
        record.update(metric_means)
        records.append(record)

    return pd.DataFrame(records), pd.DataFrame(file_records)


def compute_complete_blocks(df: pd.DataFrame) -> List[Tuple[str, int]]:
    blocks: List[Tuple[str, int]] = []
    for (model, n_value), block_df in df.groupby(["model", "n"]):
        methods_in_block = set(block_df["method"].unique())
        if not set(METHOD_ORDER).issubset(methods_in_block):
            continue
        ok = True
        for method in METHOD_ORDER:
            method_df = block_df[block_df["method"] == method]
            if any(method_df[m].dropna().empty for m in METRICS):
                ok = False
                break
        if ok:
            blocks.append((model, int(n_value)))
    return sorted(blocks, key=lambda x: (MODEL_ORDER.index(x[0]), x[1]))


def method_block_summary(df: pd.DataFrame, complete_blocks: List[Tuple[str, int]]) -> pd.DataFrame:
    rows = []
    for model, n_value in complete_blocks:
        block = df[(df["model"] == model) & (df["n"] == n_value)]
        for method in METHOD_ORDER:
            method_df = block[block["method"] == method]
            row = {"model": model, "n": n_value, "method": method}
            for metric in METRICS:
                row[metric] = float(method_df[metric].mean())
            rows.append(row)
    return pd.DataFrame(rows)


def minmax_score(values: pd.Series, higher_is_better: bool) -> pd.Series:
    min_v, max_v = float(values.min()), float(values.max())
    if np.isclose(min_v, max_v):
        return pd.Series(np.ones(len(values)), index=values.index)
    if higher_is_better:
        return (values - min_v) / (max_v - min_v)
    return (max_v - values) / (max_v - min_v)


def plot_fom7_flow(save_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.axis("off")

    boxes = [
        (0.02, 0.62, "S1\nProtocol"),
        (0.26, 0.62, "S2\nExecute"),
        (0.50, 0.62, "S3\nIntegrity"),
        (0.74, 0.62, "S4\nAggregate"),
        (0.14, 0.16, "S5\nInfer"),
        (0.42, 0.16, "S6\nReproduce"),
        (0.70, 0.16, "S7\nReport"),
    ]

    for x, y, label in boxes:
        patch = FancyBboxPatch(
            (x, y),
            0.20,
            0.22,
            boxstyle="round,pad=0.02,rounding_size=0.02",
            linewidth=1.0,
            edgecolor="#333333",
            facecolor="#F4F6F8",
        )
        ax.add_patch(patch)
        ax.text(x + 0.10, y + 0.11, label, ha="center", va="center", fontsize=8)

    arrows = [
        ((0.22, 0.73), (0.26, 0.73)),
        ((0.46, 0.73), (0.50, 0.73)),
        ((0.70, 0.73), (0.74, 0.73)),
        ((0.84, 0.62), (0.80, 0.30)),
        ((0.34, 0.27), (0.42, 0.27)),
        ((0.62, 0.27), (0.70, 0.27)),
    ]
    for start, end in arrows:
        ax.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops={"arrowstyle": "->", "lw": 1.2, "color": "#4A4A4A"},
        )

    ax.text(
        0.02,
        0.02,
        "Gates: each stage must produce auditable artifacts before progression.",
        fontsize=8,
        color="#4A4A4A",
    )

    fig.tight_layout()
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_coverage_heatmap(file_df: pd.DataFrame, save_path: Path) -> pd.DataFrame:
    coverage = pd.DataFrame(
        0,
        index=MODEL_ORDER,
        columns=METHOD_ORDER,
        dtype=int,
    )

    for (model, method), group in file_df.groupby(["model", "method"]):
        coverage.loc[model, method] = len(group)

    invalid_counts = pd.DataFrame(
        0,
        index=MODEL_ORDER,
        columns=METHOD_ORDER,
        dtype=int,
    )
    bad_df = file_df[~file_df["status"].isin(["ok_instance", "ok_aggregated"])]
    for (model, method), group in bad_df.groupby(["model", "method"]):
        invalid_counts.loc[model, method] = len(group)

    ratio = coverage / EXPECTED_RUNS_PER_MODEL_METHOD
    annotation = coverage.astype(str) + "/15"
    for model in MODEL_ORDER:
        for method in METHOD_ORDER:
            bad = invalid_counts.loc[model, method]
            if bad > 0:
                annotation.loc[model, method] += f"\ninvalid:{bad}"

    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    sns.heatmap(
        ratio,
        cmap="YlGnBu",
        vmin=0.0,
        vmax=1.0,
        annot=annotation.values,
        fmt="",
        cbar_kws={"label": "Completion ratio"},
        linewidths=0.5,
        linecolor="white",
        ax=ax,
    )
    ax.set_xlabel("Explainer")
    ax.set_ylabel("Model")
    ax.set_title("EXP2 Robustness Coverage by Model and Explainer")
    fig.tight_layout()
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)

    return coverage


def plot_method_radar(summary_df: pd.DataFrame, save_path: Path) -> pd.DataFrame:
    method_means = (
        summary_df.groupby("method")[METRICS]
        .mean()
        .reindex(METHOD_ORDER)
    )

    score_df = pd.DataFrame(index=method_means.index)
    score_df["Fidelity"] = minmax_score(method_means["fidelity"], higher_is_better=True)
    score_df["Stability"] = minmax_score(method_means["stability"], higher_is_better=True)
    score_df["Sparsity (low is better)"] = minmax_score(
        method_means["sparsity"], higher_is_better=False
    )
    score_df["Faithfulness Gap"] = minmax_score(
        method_means["faithfulness_gap"], higher_is_better=True
    )
    score_df["Efficiency (low cost)"] = minmax_score(
        method_means["cost"], higher_is_better=False
    )

    labels = list(score_df.columns)
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5.0, 4.8), subplot_kw={"projection": "polar"})
    for method in METHOD_ORDER:
        values = score_df.loc[method].tolist()
        values += values[:1]
        ax.plot(angles, values, label=method.upper(), color=METHOD_COLORS[method], linewidth=1.6)
        ax.fill(angles, values, color=METHOD_COLORS[method], alpha=0.10)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"])
    ax.set_title("Normalized Method Profile Across Core Metrics")
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.05))
    fig.tight_layout()
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)

    return method_means


def plot_fidelity_cost_tradeoff(summary_df: pd.DataFrame, save_path: Path) -> None:
    method_stats = (
        summary_df.groupby("method")[["fidelity", "cost"]]
        .agg(["mean", "std"])
        .reindex(METHOD_ORDER)
    )

    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    for method in METHOD_ORDER:
        mean_fid = method_stats.loc[method, ("fidelity", "mean")]
        std_fid = method_stats.loc[method, ("fidelity", "std")]
        mean_cost = method_stats.loc[method, ("cost", "mean")]
        std_cost = method_stats.loc[method, ("cost", "std")]

        ax.errorbar(
            mean_cost,
            mean_fid,
            xerr=std_cost,
            yerr=std_fid,
            fmt="o",
            color=METHOD_COLORS[method],
            ecolor=METHOD_COLORS[method],
            elinewidth=1.0,
            capsize=3,
            markersize=6,
            label=method.upper(),
        )
        ax.annotate(method.upper(), (mean_cost, mean_fid), xytext=(4, 3), textcoords="offset points")

    ax.set_xscale("log")
    ax.set_xlabel("Cost per Instance (ms, log scale)")
    ax.set_ylabel("Fidelity")
    ax.set_title("Fidelity vs Computational Cost (Method Means Across Blocks)")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_reproducibility_heatmap(save_path: Path) -> pd.DataFrame:
    repro_df = pd.read_csv(EXP1_REPRO_CSV)
    cols = [
        "fidelity_cv",
        "stability_cv",
        "sparsity_cv",
        "faithfulness_gap_cv",
        "cost_cv",
    ]
    display = repro_df[["experiment"] + cols].copy()
    display["experiment"] = (
        display["experiment"]
        .str.replace("exp1_adult_", "", regex=False)
        .str.replace("_", "+", regex=False)
        .str.upper()
    )
    display = display.set_index("experiment")
    display.columns = ["Fidelity", "Stability", "Sparsity", "Faithfulness Gap", "Cost"]

    fig, ax = plt.subplots(figsize=(6.2, 2.4))
    sns.heatmap(
        display,
        annot=True,
        fmt=".3f",
        cmap="YlOrRd",
        cbar_kws={"label": "Coefficient of Variation"},
        linewidths=0.4,
        linecolor="white",
        ax=ax,
    )
    ax.set_title("EXP1 Reproducibility (CV Across 9 Runs)")
    ax.set_xlabel("Metric")
    ax.set_ylabel("Configuration")
    fig.tight_layout()
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)

    return display


def main() -> None:
    setup_style()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    exp2_df, file_df = load_exp2_scaled_runs()
    complete_blocks = compute_complete_blocks(exp2_df)
    summary_df = method_block_summary(exp2_df, complete_blocks)

    # Figure A1: FOM7 flow
    plot_fom7_flow(FIGURES_DIR / "fig_a1_fom7_flow.pdf")

    # Figure A2: coverage
    coverage = plot_coverage_heatmap(file_df, FIGURES_DIR / "fig_a2_coverage_heatmap.pdf")

    # Figure A3: normalized radar profile
    method_means = plot_method_radar(summary_df, FIGURES_DIR / "fig_a3_method_radar.pdf")

    # Figure A4: fidelity-cost trade-off
    plot_fidelity_cost_tradeoff(summary_df, FIGURES_DIR / "fig_a4_fidelity_cost_tradeoff.pdf")

    # Figure A5: reproducibility CV heatmap
    repro_display = plot_reproducibility_heatmap(FIGURES_DIR / "fig_a5_reproducibility_cv.pdf")

    malformed_count = int((file_df["status"] == "json_error").sum())
    empty_count = int((file_df["status"] == "empty").sum())
    aggregated_count = int((file_df["status"] == "ok_aggregated").sum())

    summary = {
        "exp2_present_files": int(len(file_df)),
        "exp2_analyzable_runs": int(len(exp2_df)),
        "exp2_malformed_runs": malformed_count,
        "exp2_empty_runs": empty_count,
        "exp2_aggregated_only_runs": aggregated_count,
        "complete_blocks": [list(b) for b in complete_blocks],
        "coverage_expected_per_model_method": EXPECTED_RUNS_PER_MODEL_METHOD,
        "coverage_counts": coverage.to_dict(),
        "method_means_over_complete_blocks": method_means.to_dict(),
        "reproducibility_cv_table": repro_display.to_dict(),
        "figures_dir": str(FIGURES_DIR),
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "figure_summary.json").write_text(json.dumps(summary, indent=2))

    print(f"Generated figures in: {FIGURES_DIR}")
    print(f"Summary written to: {OUTPUT_DIR / 'figure_summary.json'}")


if __name__ == "__main__":
    main()
