#!/usr/bin/env python3
"""
Generate focused Paper B figures from paired SHAP-vs-LIME analysis artifacts.

Outputs (default):
  docs/reports/paper_b/figures/fig_b1_quality_endpoints.pdf
  docs/reports/paper_b/figures/fig_b1_quality_endpoints.png
  docs/reports/paper_b/figures/fig_b2_runtime_heterogeneity.pdf
  docs/reports/paper_b/figures/fig_b2_runtime_heterogeneity.png
"""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ANALYSIS_DIR = PROJECT_ROOT / "outputs" / "analysis" / "paper_a_exp2_stats"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "docs" / "reports" / "paper_b" / "figures"

COLOR_LIME = "#0072B2"
COLOR_SHAP = "#D55E00"


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "legend.fontsize": 9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "figure.dpi": 300,
            "savefig.dpi": 300,
        }
    )


def generate_quality_figure(wilcoxon_csv: Path, output_dir: Path) -> None:
    df = pd.read_csv(wilcoxon_csv)
    metric_order = ["stability", "fidelity", "faithfulness_gap", "sparsity"]
    labels = ["Stability", "Fidelity", "Faithfulness Gap", "Active Ratio (Sparsity)"]

    subset = df.set_index("metric").loc[metric_order].reset_index()
    n_pairs = int(subset["n_pairs"].iloc[0])
    lime_vals = subset["lime_mean"].values
    shap_vals = subset["shap_mean"].values

    x = np.arange(len(labels))
    width = 0.36

    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    ax.bar(x - width / 2, lime_vals, width, label="LIME", color=COLOR_LIME)
    ax.bar(x + width / 2, shap_vals, width, label="SHAP", color=COLOR_SHAP)

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Mean value across matched cells")
    ax.set_title(f"Primary Quality Endpoints (n={n_pairs} matched SHAP-LIME cells)")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(loc="upper right")

    # Note on sparsity direction to prevent misread.
    ax.text(
        0.01,
        -0.28,
        "Note: lower Active Ratio indicates sparser explanations.",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8,
    )

    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(output_dir / f"fig_b1_quality_endpoints.{ext}", bbox_inches="tight")
    plt.close(fig)


def generate_runtime_figure(paired_csv: Path, output_dir: Path) -> None:
    df = pd.read_csv(paired_csv)

    long_cost = pd.DataFrame(
        {
            "method": ["LIME"] * len(df) + ["SHAP"] * len(df),
            "cost_ms": list(df["lime_cost"].values) + list(df["shap_cost"].values),
        }
    )

    model_order = ["logreg", "rf", "xgb", "mlp", "svm"]
    med = (
        df.groupby("model")[["lime_cost", "shap_cost"]]
        .median()
        .reindex(model_order)
        .reset_index()
    )

    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.9))

    # Panel A: overall runtime distribution
    positions = [0, 1]
    lime = long_cost[long_cost["method"] == "LIME"]["cost_ms"].values
    shap = long_cost[long_cost["method"] == "SHAP"]["cost_ms"].values
    box = axes[0].boxplot(
        [lime, shap],
        positions=positions,
        widths=0.55,
        patch_artist=True,
        showfliers=False,
    )
    box["boxes"][0].set(facecolor=COLOR_LIME, alpha=0.8)
    box["boxes"][1].set(facecolor=COLOR_SHAP, alpha=0.8)
    for whisker in box["whiskers"]:
        whisker.set(color="#555555", linewidth=1.0)
    for cap in box["caps"]:
        cap.set(color="#555555", linewidth=1.0)
    for median in box["medians"]:
        median.set(color="black", linewidth=1.2)

    axes[0].set_xticks(positions)
    axes[0].set_xticklabels(["LIME", "SHAP"])
    axes[0].set_yscale("log")
    axes[0].set_ylabel("Cost per explanation (ms, log scale)")
    axes[0].set_title("Overall Runtime Distribution")
    axes[0].grid(axis="y", alpha=0.25, which="both")

    # Panel B: model-level medians
    x = np.arange(len(med))
    width = 0.37
    axes[1].bar(x - width / 2, med["lime_cost"], width, label="LIME", color=COLOR_LIME)
    axes[1].bar(x + width / 2, med["shap_cost"], width, label="SHAP", color=COLOR_SHAP)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(med["model"].str.upper())
    axes[1].set_yscale("log")
    axes[1].set_ylabel("Median cost (ms, log scale)")
    axes[1].set_title("Runtime Heterogeneity by Model")
    axes[1].grid(axis="y", alpha=0.25, which="both")
    axes[1].legend(loc="upper left")

    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(output_dir / f"fig_b2_runtime_heterogeneity.{ext}", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--analysis-dir",
        type=Path,
        default=DEFAULT_ANALYSIS_DIR,
        help="Directory containing paired SHAP-LIME analysis exports.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where figures are written.",
    )
    args = parser.parse_args()

    setup_style()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    wilcoxon_csv = args.analysis_dir / "wilcoxon_shap_lime_all_models.csv"
    paired_csv = args.analysis_dir / "paired_cells_shap_lime_all_models.csv"

    generate_quality_figure(wilcoxon_csv, args.output_dir)
    generate_runtime_figure(paired_csv, args.output_dir)

    print(f"Wrote figures to: {args.output_dir}")


if __name__ == "__main__":
    main()
