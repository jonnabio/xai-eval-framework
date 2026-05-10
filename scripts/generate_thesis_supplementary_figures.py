#!/usr/bin/env python
"""Generate supplementary PNG figures for the thesis Chapter 4.

Produces four figures not included in generate_spanish_thesis_figures.py:
  1. fig_cd_diagram_es.png       — Critical difference diagram (Nemenyi)
  2. fig_boxplots_metricas_es.png — Boxplots by method for fidelity and stability
  3. fig_diferencias_pareadas_es.png — Paired differences SHAP-LIME (75 cells)
  4. fig_radar_metodos_es.png    — Method profile radar chart (5 metrics)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
STATS = ROOT / "outputs" / "analysis" / "paper_a_exp2_stats"
OUT = ROOT / "thesis" / "assets" / "figures"

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
METRIC_LABELS_ES = {
    "fidelity": "Fidelidad",
    "stability": "Estabilidad",
    "sparsity": "Parsimonia",
    "faithfulness_gap": "Brecha de\nfidelidad",
    "cost": "Coste",
}


def setup() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "legend.fontsize": 9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "figure.dpi": 140,
            "savefig.dpi": 220,
        }
    )


def save(fig: plt.Figure, filename: str) -> None:
    fig.tight_layout()
    fig.savefig(OUT / filename, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {filename}")


# ---------------------------------------------------------------------------
# Figure 1: Critical difference diagram
# ---------------------------------------------------------------------------
FRIEDMAN_RANKS = {
    "fidelity": {"shap": 1.0, "lime": 2.0, "anchors": 3.2, "dice": 3.8},
    "stability": {"shap": 1.0, "dice": 2.0, "lime": 3.4, "anchors": 3.6},
}
# Groups where |Ri - Rj| < CD=1.211 (not significantly different)
CD_GROUPS = {
    "fidelity": [
        ["shap", "lime"],        # |1.0-2.0|=1.0 < 1.211
        ["anchors", "dice"],     # |3.2-3.8|=0.6 < 1.211
    ],
    "stability": [
        ["shap", "dice"],        # |1.0-2.0|=1.0 < 1.211
        ["lime", "anchors"],     # |3.4-3.6|=0.2 < 1.211
    ],
}
CD_VALUE = 1.211


def figure_cd_diagram() -> None:
    metrics = ["fidelity", "stability"]
    metric_titles = {"fidelity": "Fidelidad", "stability": "Estabilidad"}

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.2))

    for ax, metric in zip(axes, metrics):
        ranks = FRIEDMAN_RANKS[metric]
        groups = CD_GROUPS[metric]

        # Sort methods by rank for left-to-right display
        sorted_methods = sorted(ranks.keys(), key=lambda m: ranks[m])

        # Horizontal axis = rank value (1 to 4)
        ax.set_xlim(0.5, 4.5)
        ax.set_ylim(-0.8, 1.4)
        ax.invert_xaxis()  # Convention: best rank on left

        # Draw CD bar at top
        cd_start = 1.0
        cd_end = 1.0 + CD_VALUE
        ax.annotate(
            "",
            xy=(cd_end, 1.2),
            xytext=(cd_start, 1.2),
            arrowprops=dict(arrowstyle="<->", color="black", lw=1.5),
        )
        ax.text(
            (cd_start + cd_end) / 2,
            1.32,
            f"DC = {CD_VALUE}",
            ha="center",
            va="bottom",
            fontsize=8.5,
            color="black",
        )

        # Draw method ticks and labels
        y_method = 0.85
        for method in sorted_methods:
            r = ranks[method]
            color = COLORS[method]
            ax.plot(r, y_method, "o", color=color, markersize=9, zorder=5)
            ax.text(
                r,
                y_method + 0.22,
                METHOD_LABELS[method],
                ha="center",
                va="bottom",
                fontsize=9,
                color=color,
                weight="bold",
            )
            ax.text(
                r,
                y_method - 0.22,
                f"{r:.1f}",
                ha="center",
                va="top",
                fontsize=8,
                color="#444444",
            )

        # Draw vertical axis line
        ax.axhline(y=y_method, xmin=0.05, xmax=0.95, color="#888888", lw=0.8, ls="--")

        # Draw non-significant groups (horizontal thick bars)
        bar_y_positions = [-0.15, -0.45]
        for idx, group in enumerate(groups):
            group_ranks = sorted([ranks[m] for m in group])
            y_bar = bar_y_positions[idx % len(bar_y_positions)]
            ax.plot(
                group_ranks,
                [y_bar, y_bar],
                color="#333333",
                lw=3.5,
                solid_capstyle="round",
            )
            # Vertical connectors
            for m in group:
                r = ranks[m]
                ax.plot(
                    [r, r],
                    [y_method, y_bar],
                    color=COLORS[m],
                    lw=1.2,
                    ls=":",
                    alpha=0.7,
                )

        ax.set_xlabel("Rango medio (mejor → izquierda)", fontsize=9)
        ax.set_title(f"Diagrama DC — {metric_titles[metric]}", fontsize=11)
        ax.set_xticks([1, 2, 3, 4])
        ax.tick_params(axis="y", left=False, labelleft=False)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.grid(axis="x", ls=":", alpha=0.4)

        # Note on non-significant groups
        ax.text(
            0.02,
            -0.16,
            "Las barras horizontales gruesas conectan métodos no significativamente distintos (p > 0.05).",
            transform=ax.transAxes,
            fontsize=7.5,
            color="#555555",
            va="top",
        )

    fig.suptitle(
        "Diagrama de diferencia crítica (Nemenyi, k=4, n=15, α=0.05)",
        fontsize=12,
        y=1.02,
    )
    save(fig, "fig_cd_diagram_es.png")


# ---------------------------------------------------------------------------
# Figure 2: Boxplots by method for fidelity and stability
# ---------------------------------------------------------------------------

def figure_boxplots() -> None:
    df = pd.read_csv(STATS / "exp2_block_method_summary.csv")

    metrics_to_plot = ["fidelity", "stability"]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))

    for ax, metric in zip(axes, metrics_to_plot):
        data_by_method = [
            df.loc[df["method"] == m, metric].dropna().values
            for m in METHOD_ORDER
        ]
        colors_list = [COLORS[m] for m in METHOD_ORDER]
        labels = [METHOD_LABELS[m] for m in METHOD_ORDER]

        bp = ax.boxplot(
            data_by_method,
            tick_labels=labels,
            patch_artist=True,
            medianprops=dict(color="black", lw=2),
            whiskerprops=dict(lw=1.2),
            capprops=dict(lw=1.2),
            flierprops=dict(marker="o", markersize=4, alpha=0.5),
            widths=0.55,
        )
        for patch, color in zip(bp["boxes"], colors_list):
            patch.set_facecolor(color)
            patch.set_alpha(0.75)
        for flier, color in zip(bp["fliers"], colors_list):
            flier.set(markerfacecolor=color, markeredgecolor=color)

        # Overlay individual points (jitter)
        rng = np.random.default_rng(42)
        for i, (data, color) in enumerate(zip(data_by_method, colors_list), start=1):
            jitter = rng.uniform(-0.12, 0.12, size=len(data))
            ax.plot(
                i + jitter,
                data,
                "o",
                color=color,
                markersize=3.5,
                alpha=0.45,
                zorder=3,
            )

        label_es = {"fidelity": "Fidelidad", "stability": "Estabilidad"}[metric]
        ax.set_ylabel(f"{label_es} media por bloque (g, n)")
        ax.set_title(f"{label_es} por método — distribución de bloques")
        ax.grid(axis="y", ls=":", alpha=0.45)
        ax.spines[["top", "right"]].set_visible(False)

        # Annotate median values
        for i, (data, m) in enumerate(zip(data_by_method, METHOD_ORDER), start=1):
            med = np.median(data)
            ax.text(
                i,
                med + 0.005,
                f"{med:.3f}",
                ha="center",
                va="bottom",
                fontsize=7.5,
                color="#222222",
            )

    fig.suptitle(
        "Distribución de métricas por método (n=15 bloques por método)",
        fontsize=12,
        y=1.02,
    )
    axes[0].text(
        0.0,
        -0.15,
        "Fuente: exp2_block_method_summary.csv. Cada punto representa un bloque (modelo, tamaño de muestra).",
        transform=axes[0].transAxes,
        fontsize=7.5,
        color="#555555",
    )
    save(fig, "fig_boxplots_metricas_es.png")


# ---------------------------------------------------------------------------
# Figure 3: Paired differences SHAP-LIME
# ---------------------------------------------------------------------------

def figure_paired_differences() -> None:
    df = pd.read_csv(STATS / "paired_cells_shap_lime_all_models.csv")

    metrics = ["fidelity", "stability"]
    metric_labels_es = {"fidelity": "Fidelidad", "stability": "Estabilidad"}

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    for ax, metric in zip(axes, metrics):
        diffs = df[f"diff_{metric}"].sort_values(ascending=False).values
        n = len(diffs)
        x = np.arange(1, n + 1)
        positive = diffs >= 0
        negative = ~positive

        ax.bar(x[positive], diffs[positive], color="#1f77b4", alpha=0.80, width=1.0, label="SHAP > LIME")
        ax.bar(x[negative], diffs[negative], color="#d62728", alpha=0.80, width=1.0, label="LIME > SHAP")
        ax.axhline(0, color="black", lw=0.8)

        mean_diff = np.mean(diffs)
        ax.axhline(mean_diff, color="#333333", lw=1.4, ls="--", label=f"Media = {mean_diff:.3f}")

        n_pos = positive.sum()
        n_neg = negative.sum()
        label_es = metric_labels_es[metric]
        ax.set_title(
            f"Diferencias pareadas — {label_es}\n({n_pos}/{n} positivas, {n_neg}/{n} negativas)",
            fontsize=11,
        )
        ax.set_xlabel("Celda pareada (ordenada por diferencia decreciente)")
        ax.set_ylabel(f"$d_i$ = SHAP$-$LIME ({label_es})")
        ax.legend(fontsize=8, loc="upper right")
        ax.grid(axis="y", ls=":", alpha=0.4)
        ax.spines[["top", "right"]].set_visible(False)

    fig.suptitle(
        "Diferencias pareadas SHAP − LIME por celda (n=75 celdas (modelo, semilla, n))",
        fontsize=12,
        y=1.02,
    )
    axes[0].text(
        0.0,
        -0.16,
        "Fuente: paired_cells_shap_lime_all_models.csv. Azul = SHAP superior; rojo = LIME superior.",
        transform=axes[0].transAxes,
        fontsize=7.5,
        color="#555555",
    )
    save(fig, "fig_diferencias_pareadas_es.png")


# ---------------------------------------------------------------------------
# Figure 4: Method radar chart (5 metrics, normalized)
# ---------------------------------------------------------------------------

def figure_radar() -> None:
    df = pd.read_csv(STATS / "exp2_block_method_summary.csv")
    summary = (
        df.groupby("method")[["fidelity", "stability", "sparsity", "faithfulness_gap", "cost"]]
        .mean()
        .reindex(METHOD_ORDER)
    )

    # Normalize to [0, 1]; for cost and sparsity: lower is "better" so invert
    # Cost: invert so high radar = efficient
    # Sparsity: keep as-is (lower = more parsimonious, but parsimonia axis = "compacidad")
    # For radar: all axes point "outward = better"
    raw = summary.copy()
    normalized = pd.DataFrame(index=raw.index)

    # fidelity: higher is better → normalize 0–1
    normalized["Fidelidad"] = (raw["fidelity"] - raw["fidelity"].min()) / (raw["fidelity"].max() - raw["fidelity"].min())
    # stability: higher is better
    normalized["Estabilidad"] = (raw["stability"] - raw["stability"].min()) / (raw["stability"].max() - raw["stability"].min())
    # sparsity: lower is more parsimonious — invert so "outward = more parsimonious"
    s_inv = 1.0 - (raw["sparsity"] - raw["sparsity"].min()) / (raw["sparsity"].max() - raw["sparsity"].min())
    normalized["Parsimonia"] = s_inv
    # faithfulness_gap: higher is better
    normalized["Brecha\nfidelidad"] = (raw["faithfulness_gap"] - raw["faithfulness_gap"].min()) / (raw["faithfulness_gap"].max() - raw["faithfulness_gap"].min())
    # cost: lower is better → invert
    c_inv = 1.0 - (raw["cost"] - raw["cost"].min()) / (raw["cost"].max() - raw["cost"].min())
    normalized["Eficiencia\n(coste inv.)"] = c_inv

    labels = list(normalized.columns)
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # close the polygon

    fig, ax = plt.subplots(figsize=(7, 6), subplot_kw=dict(polar=True))

    for method in METHOD_ORDER:
        values = normalized.loc[method].tolist()
        values += values[:1]
        ax.plot(angles, values, "o-", lw=2.0, color=COLORS[method],
                label=METHOD_LABELS[method], markersize=5)
        ax.fill(angles, values, alpha=0.12, color=COLORS[method])

    # Gridlines and labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_yticks([0.25, 0.50, 0.75, 1.0])
    ax.set_yticklabels(["0.25", "0.50", "0.75", "1.00"], fontsize=7, color="#666666")
    ax.set_ylim(0, 1.05)
    ax.set_title(
        "Perfil multidimensional por método\n(normalizado [0,1]; radio mayor = mejor)",
        fontsize=12,
        pad=18,
    )
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15), fontsize=9)
    ax.grid(color="#cccccc", linestyle=":", linewidth=0.8)

    ax.text(
        0.5,
        -0.09,
        "Fuente: exp2_block_method_summary.csv. Parsimonia y eficiencia están invertidas (mayor radio = mejor).",
        transform=ax.transAxes,
        ha="center",
        fontsize=7.5,
        color="#555555",
    )
    save(fig, "fig_radar_metodos_es.png")


def main() -> None:
    setup()
    print("Generating supplementary thesis figures...")
    figure_cd_diagram()
    figure_boxplots()
    figure_paired_differences()
    figure_radar()
    print(f"\nAll figures saved to: {OUT}")


if __name__ == "__main__":
    main()
