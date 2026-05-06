#!/usr/bin/env python
"""Generate Spanish PNG figures for the thesis Chapter 4."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
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
METRIC_LABELS = {
    "fidelity": "Fidelidad",
    "stability": "Estabilidad",
    "sparsity": "Parsimonia",
    "faithfulness_gap": "Brecha de fidelidad",
    "cost": "Coste",
}


def setup() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
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


def figure_stability_cost() -> None:
    df = pd.read_csv(STATS / "exp2_block_method_summary.csv")
    grouped = (
        df.groupby("method")[["stability", "cost", "fidelity"]]
        .agg(["mean", "std"])
        .reindex(METHOD_ORDER)
    )

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    for method in METHOD_ORDER:
        x = grouped.loc[method, ("cost", "mean")]
        y = grouped.loc[method, ("stability", "mean")]
        xerr = grouped.loc[method, ("cost", "std")]
        yerr = grouped.loc[method, ("stability", "std")]
        size = 110 + 240 * grouped.loc[method, ("fidelity", "mean")]
        ax.errorbar(
            x,
            y,
            xerr=xerr,
            yerr=yerr,
            fmt="o",
            markersize=np.sqrt(size),
            color=COLORS[method],
            ecolor=COLORS[method],
            elinewidth=1.0,
            capsize=3,
            alpha=0.9,
            label=METHOD_LABELS[method],
        )
        ax.annotate(
            METHOD_LABELS[method],
            (x, y),
            xytext=(6, 4),
            textcoords="offset points",
            weight="bold",
        )

    ax.set_xscale("log")
    ax.set_xlabel("Coste computacional medio por instancia (ms, escala log)")
    ax.set_ylabel("Estabilidad media")
    ax.set_title("Relación entre estabilidad y coste por método")
    ax.grid(True, which="both", linestyle=":", linewidth=0.7, alpha=0.55)
    ax.legend(title="Método", loc="upper right")
    ax.text(
        0.01,
        -0.22,
        "Fuente: exp2_block_method_summary.csv. Barras = desviación estándar entre bloques.",
        transform=ax.transAxes,
        fontsize=8,
        color="#555555",
    )
    save(fig, "fig_estabilidad_coste_es.png")


def figure_metric_correlation() -> None:
    df = pd.read_csv(STATS / "exp2_run_level_metrics.csv")
    metrics = ["fidelity", "stability", "sparsity", "faithfulness_gap", "cost"]
    corr = df[metrics].corr(method="spearman")
    labels = [METRIC_LABELS[m] for m in metrics]

    fig, ax = plt.subplots(figsize=(6.2, 5.4))
    im = ax.imshow(corr.values, vmin=-1, vmax=1, cmap="RdBu_r")
    ax.set_xticks(range(len(labels)), labels=labels, rotation=35, ha="right")
    ax.set_yticks(range(len(labels)), labels=labels)
    ax.set_title("Correlación entre métricas del banco de pruebas")

    for i in range(len(labels)):
        for j in range(len(labels)):
            value = corr.values[i, j]
            color = "white" if abs(value) > 0.55 else "black"
            ax.text(j, i, f"{value:.2f}", ha="center", va="center", color=color)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Correlación de Spearman")
    ax.text(
        0.0,
        -0.25,
        "Fuente: exp2_run_level_metrics.csv. La matriz muestra asociaciones empíricas, no causalidad.",
        transform=ax.transAxes,
        fontsize=8,
        color="#555555",
    )
    save(fig, "fig_correlacion_metricas_es.png")


def figure_coverage() -> None:
    inv = pd.read_csv(STATS / "exp2_run_inventory.csv")
    inv["analizable"] = inv["status"].isin(["ok_instance", "ok_aggregated"])
    pivot = (
        inv.pivot_table(
            index="model",
            columns="method",
            values="analizable",
            aggfunc="sum",
            fill_value=0,
        )
        .reindex(index=["logreg", "rf", "xgb", "svm", "mlp"], columns=METHOD_ORDER)
        .astype(int)
    )
    ratio = pivot / 15.0

    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    im = ax.imshow(ratio.values, vmin=0, vmax=1, cmap="YlGnBu")
    ax.set_xticks(range(len(METHOD_ORDER)), [METHOD_LABELS[m] for m in METHOD_ORDER])
    ax.set_yticks(range(len(pivot.index)), [m.upper() if m != "logreg" else "LOGREG" for m in pivot.index])
    ax.set_xlabel("Método explicador")
    ax.set_ylabel("Modelo predictivo")
    ax.set_title("Cobertura analítica EXP2 por modelo y método")

    for i in range(ratio.shape[0]):
        for j in range(ratio.shape[1]):
            val = pivot.values[i, j]
            ax.text(j, i, f"{val}/15", ha="center", va="center", color="black", weight="bold")

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Proporción analizable")
    ax.text(
        0.0,
        -0.18,
        "Fuente: exp2_run_inventory.csv. Una celda analizable supera la auditoría de integridad FOM-7.",
        transform=ax.transAxes,
        fontsize=8,
        color="#555555",
    )
    save(fig, "fig_cobertura_exp2_es.png")


def main() -> None:
    setup()
    figure_stability_cost()
    figure_metric_correlation()
    figure_coverage()
    print(f"Figuras generadas en {OUT}")


if __name__ == "__main__":
    main()
