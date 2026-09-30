#!/usr/bin/env python3
"""Generate reader-facing scientific figures specific to the CIFIE chapter.

The source statistics remain the qualified EXP2 exports. This script exists so
chapter figures can be adjusted for book-page legibility without modifying the
thesis figures or their protected numerical content.
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
STATS = ROOT / "outputs" / "analysis" / "paper_a_exp2_stats"
OUT = (
    ROOT
    / "publications"
    / "book_chapters"
    / "2026_cifie_xai_fom7"
    / "figures"
    / "exported"
)

METHOD_ORDER = ["shap", "lime", "anchors", "dice"]
METHOD_LABELS = {
    "shap": "SHAP",
    "lime": "LIME",
    "anchors": "Anchors",
    "dice": "DiCE",
}
COLORS = {
    "shap": "#1f77b4",
    "lime": "#ff7f0e",
    "anchors": "#2ca02c",
    "dice": "#d62728",
}
CD_VALUE = 1.211


def mean_ranks(metric: str) -> dict[str, float]:
    """Re-derive mean ranks from the registered 15-block EXP2 summary."""
    frame = pd.read_csv(STATS / "exp2_block_method_summary.csv")
    pivot = frame.pivot(index=["model", "n"], columns="method", values=metric)
    pivot = pivot[METHOD_ORDER].dropna()
    if len(pivot) != 15:
        raise SystemExit(f"expected 15 complete {metric} blocks, found {len(pivot)}")
    ranks = pivot.rank(axis=1, ascending=False, method="average").mean(axis=0)
    return {method: float(ranks[method]) for method in METHOD_ORDER}


def nonsignificant_pairs(metric: str) -> list[tuple[str, str]]:
    """Read Nemenyi results and retain pairs not separated at alpha=.05."""
    matrix = pd.read_csv(STATS / f"nemenyi_{metric}.csv", index_col=0)
    pairs: list[tuple[str, str]] = []
    for left, right in combinations(METHOD_ORDER, 2):
        if float(matrix.loc[left, right]) > 0.05:
            pairs.append((left, right))
    if not pairs:
        raise SystemExit(
            f"expected at least one non-significant Nemenyi pair for {metric}"
        )
    return pairs


def figure_cd_diagram() -> Path:
    """Render a legible two-panel critical-difference diagram for Word."""
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "figure.dpi": 150,
            "savefig.dpi": 300,
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5))

    for ax, metric, title in zip(
        axes,
        ["fidelity", "stability"],
        ["Fidelidad", "Estabilidad"],
    ):
        ranks = mean_ranks(metric)
        ordered = sorted(ranks, key=ranks.get)
        pairs = nonsignificant_pairs(metric)
        closest_pair = min(
            combinations(METHOD_ORDER, 2),
            key=lambda pair: abs(ranks[pair[0]] - ranks[pair[1]]),
        )
        staggered_method = max(closest_pair, key=ranks.get)

        ax.set_xlim(0.65, 4.15)
        ax.set_ylim(-0.55, 1.45)
        ax.invert_xaxis()
        ax.axhline(0.60, color="#777777", lw=0.9, ls="--")

        for method in ordered:
            rank = ranks[method]
            ax.plot(rank, 0.60, "o", color=COLORS[method], markersize=9, zorder=5)
            # The only near-collision in each panel is staggered vertically.
            label_y = 1.10 if method == staggered_method else 0.88
            ax.text(
                rank,
                label_y,
                METHOD_LABELS[method],
                ha="center",
                va="bottom",
                fontsize=9,
                color=COLORS[method],
                weight="bold",
            )
            ax.text(rank, 0.43, f"{rank:.1f}", ha="center", va="top", fontsize=8)

        cd_start = 1.0
        cd_end = cd_start + CD_VALUE
        ax.annotate(
            "",
            xy=(cd_end, 1.30),
            xytext=(cd_start, 1.30),
            arrowprops={"arrowstyle": "<->", "color": "black", "lw": 1.4},
        )
        ax.text(
            (cd_start + cd_end) / 2,
            1.35,
            f"DC = {CD_VALUE}",
            ha="center",
            va="bottom",
            fontsize=8.5,
        )

        bar_levels = [0.14 - (0.18 * index) for index in range(len(pairs))]
        for y_bar, pair in zip(bar_levels, pairs):
            pair_ranks = sorted(ranks[method] for method in pair)
            ax.plot(pair_ranks, [y_bar, y_bar], color="#333333", lw=4, solid_capstyle="round")
            for method in pair:
                rank = ranks[method]
                ax.plot(
                    [rank, rank],
                    [0.60, y_bar],
                    color=COLORS[method],
                    lw=1.1,
                    ls=":",
                    alpha=0.75,
                )

        ax.set_title(f"Diagrama DC — {title}")
        ax.set_xlabel("Rango medio (mejor → izquierda)")
        ax.set_xticks([1, 2, 3, 4])
        ax.tick_params(axis="y", left=False, labelleft=False)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.grid(axis="x", ls=":", alpha=0.35)

    fig.suptitle(
        "Diagrama de diferencia crítica (Nemenyi, k = 4, n = 15, α = .05)",
        fontsize=13,
        y=0.98,
    )
    fig.text(
        0.5,
        0.035,
        "Las barras gruesas conectan métodos que Nemenyi no separa significativamente (p > .05).",
        ha="center",
        fontsize=9,
        color="#444444",
    )
    fig.subplots_adjust(left=0.06, right=0.98, top=0.82, bottom=0.22, wspace=0.24)

    OUT.mkdir(parents=True, exist_ok=True)
    output = OUT / "fig_cd_diagram_es.png"
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)
    return output


def main() -> int:
    output = figure_cd_diagram()
    print(f"OK: {output.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
