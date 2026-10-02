#!/usr/bin/env python3
"""
Generate the Paper B+C figures from paired SHAP-vs-LIME analysis artifacts.

Outputs (default), the files paper_bc_peerjcs.tex includes:
  docs/reports/paper_bc/figures/fig_b1_quality_endpoints.pdf
  docs/reports/paper_bc/figures/fig_b1_quality_endpoints.png
  docs/reports/paper_bc/figures/fig_b2_runtime_heterogeneity.pdf
  docs/reports/paper_bc/figures/fig_b2_runtime_heterogeneity.png

Figure 1 plots the mean paired difference (SHAP - LIME) with its 95% t
interval, the quantities of tab:paired_main. It used to plot the two methods'
mean levels side by side, which are results of the published RIMI article
(Paper A) and may not be re-reported in Paper B+C (review F02,
2026-09-28).
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
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "docs" / "reports" / "paper_bc" / "figures"

# Two-sided 95% Student-t quantile at df = 74 (75 matched cells); the same
# constant as scripts/pubs/claim_sources.py, which registers these intervals.
T975_DF74 = 1.9925435

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


def generate_quality_figure(paired_csv: Path, output_dir: Path) -> None:
    df = pd.read_csv(paired_csv)
    metric_order = ["stability", "fidelity", "faithfulness_gap", "sparsity"]
    labels = ["Stability", "Fidelity", "Faithfulness gap", "Active ratio\n(sparsity)"]

    n_pairs = len(df)
    if n_pairs != 75:
        raise SystemExit(f"expected 75 matched cells, found {n_pairs}")
    means, halves = [], []
    for metric in metric_order:
        diff = df[f"diff_{metric}"].to_numpy(dtype=float)
        means.append(diff.mean())
        halves.append(T975_DF74 * diff.std(ddof=1) / np.sqrt(n_pairs))

    y = np.arange(len(labels))[::-1]
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    ax.errorbar(means, y, xerr=halves, fmt="o", color=COLOR_SHAP,
                ecolor="#333333", elinewidth=1.2, capsize=4, markersize=6)
    ax.axvline(0.0, color="#555555", linewidth=0.9, linestyle="--")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Mean paired difference, SHAP $-$ LIME (95% CI)")
    # No in-image title: PeerJ puts titles in the caption only (n is stated there).
    ax.grid(axis="x", alpha=0.25)
    ax.set_xlim(-0.05, max(m + h for m, h in zip(means, halves)) + 0.05)

    # Sparsity is an active-feature ratio: a positive difference means SHAP
    # is denser, i.e. LIME is sparser. Say so on the figure.
    ax.text(0.99, 0.02, "Positive active-ratio difference: LIME is sparser.",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8)

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
    # Panel letter instead of a title (PeerJ: no titles in images).
    axes[0].set_title("A", loc="left", fontweight="bold")
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
    axes[1].set_title("B", loc="left", fontweight="bold")
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

    paired_csv = args.analysis_dir / "paired_cells_shap_lime_all_models.csv"

    generate_quality_figure(paired_csv, args.output_dir)
    generate_runtime_figure(paired_csv, args.output_dir)

    print(f"Wrote figures to: {args.output_dir}")


if __name__ == "__main__":
    main()
