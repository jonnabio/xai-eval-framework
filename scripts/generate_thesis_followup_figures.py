#!/usr/bin/env python3
"""Spanish figures of the follow-up chapter of the thesis (ADR-0023).

Each figure is drawn from the result files of its study, the same files the corresponding
paper is built from, so a figure cannot disagree with the registered values of the chapter.
No number is printed as a label: the values are in the tables of the chapter, which the
claim check covers. Colours of the methods as in the other thesis figures and in the papers.

    python scripts/generate_thesis_followup_figures.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "thesis" / "assets" / "figures"
ERROR = ROOT / "outputs" / "analysis" / "paper_d"
CONCORDANCE = ROOT / "outputs" / "analysis" / "paper_e" / "posthoc"
TRANSFER = ROOT / "outputs" / "analysis" / "paper_f" / "results"
JUDGES = ROOT / "docs" / "reports" / "paper_c" / "results"

METHODS = ["shap", "lime", "anchors", "dice"]
LABEL = {"shap": "SHAP", "lime": "LIME", "anchors": "Anchors", "dice": "DiCE"}
COLOR = {"shap": "#c0392b", "lime": "#1b6ca8", "anchors": "#2e8b57", "dice": "#6c3483"}
MARKER = {"shap": "s", "lime": "o", "anchors": "^", "dice": "D"}
NOTE = dict(fontsize=7.5, color="#555555")


def setup() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9, "legend.fontsize": 8,
        "xtick.labelsize": 8, "ytick.labelsize": 8, "savefig.dpi": 220,
        "axes.spines.top": False, "axes.spines.right": False,
    })


def key_table(path: Path) -> dict[str, float]:
    """A two-column result file (metric, value) as a dictionary."""
    t = pd.read_csv(path)
    return dict(zip(t["metric"], t["value"]))


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)
    print(f"  {name}")


def figure_error() -> None:
    """Mean per-run difference, misclassified minus correct, with its 95% interval."""
    t = key_table(ERROR / "rq1.csv")
    metrics = [("fidelity", "Δ fidelidad"), ("stability", "Δ estabilidad"),
               ("faithfulness_gap", "Δ brecha de fidelidad")]
    fig, axes = plt.subplots(1, 3, figsize=(9.2, 2.9), sharey=True)
    for ax, (metric, title) in zip(axes, metrics):
        for y, m in enumerate(METHODS):
            mean, lo, hi = (t[f"{m}.{metric}.{k}"] for k in ("mean", "ci_lo", "ci_hi"))
            significant = t[f"{m}.{metric}.p_holm"] < 0.05
            ax.errorbar(mean, y, xerr=[[mean - lo], [hi - mean]], fmt=MARKER[m], color=COLOR[m],
                        mfc=COLOR[m] if significant else "white", ms=7, capsize=3, lw=1.3)
        ax.axvline(0, color="#555555", lw=0.9, ls="--")
        ax.set_xlabel(title)
        ax.grid(axis="x", ls=":", alpha=0.5)
        ax.set_yticks(range(len(METHODS)), [LABEL[m] for m in METHODS])
    axes[0].invert_yaxis()
    fig.text(0.01, -0.06, "Fuente: rq1.csv del estudio. Media por ejecución de la "
             "diferencia (mal clasificadas menos bien clasificadas) e intervalo del 95 %. Marcador "
             "relleno: significativa tras la corrección de Holm. Valores negativos: menor calidad "
             "en los errores.", wrap=True, **NOTE)
    fig.tight_layout()
    save(fig, "fig_seg_error_es.png")


def figure_margin() -> None:
    """Mean stability by prediction margin, correct against misclassified instances."""
    t = key_table(ERROR / "fig_margin.csv")
    centres = np.linspace(0.025, 0.475, 10)
    fig, axes = plt.subplots(1, 4, figsize=(9.2, 2.7))
    for ax, m in zip(axes, METHODS):
        for group, style in (("cor", dict(marker="o", ls="-", mfc=COLOR[m])),
                             ("mis", dict(marker="s", ls="--", mfc="white"))):
            ys = [t.get(f"{m}.stability.{group}.b{b}", np.nan) for b in range(10)]
            ax.plot(centres, ys, color=COLOR[m], ms=4, lw=1.2, **style)
        ax.set_title(LABEL[m], color=COLOR[m], fontweight="bold")
        ax.set_xlabel(r"Margen $|\hat{p} - 0.5|$")
        ax.grid(ls=":", alpha=0.5)
    axes[0].set_ylabel("Estabilidad media")
    handles = [Line2D([], [], color="#333333", marker="o", ls="-", label="Bien clasificadas"),
               Line2D([], [], color="#333333", marker="s", ls="--", mfc="white",
                      label="Mal clasificadas")]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False,
               bbox_to_anchor=(0.5, -0.07))
    fig.text(0.01, -0.15, "Fuente: fig_margin.csv del estudio. Intervalos de margen "
             "de anchura 0.05 con al menos 30 instancias (UCI Adult).", **NOTE)
    fig.tight_layout()
    save(fig, "fig_seg_margen_es.png")


def figure_concordance() -> None:
    """Top-5 overlap of SHAP and LIME: same instance against different instances."""
    t = pd.read_csv(CONCORDANCE / "review2_permutation_summary.csv")
    t = t[t["model"] != "all"]
    datasets = [("exp2_adult", "Adult"), ("german_credit", "German Credit"),
                ("breast_cancer", "Breast Cancer")]
    models = {"logreg": "Regresión logística", "svm": "SVM", "mlp": "MLP",
              "rf": "Bosque aleatorio", "xgb": "XGBoost"}
    rows, labels, breaks = [], [], []
    for key, name in datasets:
        part = t[t["dataset"] == key].set_index("model")
        for model in [m for m in models if m in part.index]:
            rows.append(part.loc[model])
            labels.append(f"{name} · {models[model]}")
        breaks.append(len(rows))
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    for y, r in enumerate(rows):
        same = r["paired_top5_jaccard.estimate_mean_of_run_means"]
        lo, hi = r["paired_top5_jaccard.ci95_low"], r["paired_top5_jaccard.ci95_high"]
        other = r["other_instance_top5_jaccard.estimate_mean_of_run_means"]
        ax.plot([other, same], [y, y], color="#bbbbbb", lw=2.2, zorder=1)
        ax.errorbar(same, y, xerr=[[same - lo], [hi - same]], fmt="o", color="#222222", ms=6,
                    capsize=3, lw=1.2, zorder=3)
        ax.plot(other, y, "o", mfc="white", mec="#222222", ms=6, zorder=3)
    for b in breaks[:-1]:
        ax.axhline(b - 0.5, color="#cccccc", lw=0.8)
    ax.set_yticks(range(len(rows)), labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel(r"Solapamiento de las cinco características principales ($J_5$)")
    ax.grid(axis="x", ls=":", alpha=0.5)
    handles = [Line2D([], [], color="#222222", marker="o", ls="", label="Misma instancia (SHAP y LIME)"),
               Line2D([], [], color="#222222", marker="o", mfc="white", ls="",
                      label="Instancias distintas de la misma ejecución"),
               Line2D([], [], color="#bbbbbb", lw=2.2, label="Parte propia de la instancia")]
    ax.legend(handles=handles, loc="upper center", ncol=3, frameon=False,
              bbox_to_anchor=(0.5, -0.16))
    fig.text(0.01, -0.12, "Fuente: review2_permutation_summary.csv del estudio. "
             "Media de las medias por ejecución; la barra de error describe la dispersión entre semillas.",
             **NOTE)
    fig.tight_layout()
    save(fig, "fig_seg_concordancia_es.png")


def figure_transfer() -> None:
    """Rank of each method on each of the datasets, by measure."""
    ranks = pd.read_csv(TRANSFER / "ranks.csv")
    names = sorted(ranks["dataset"].unique(), key=lambda d: (d != "adult", d))
    measures = [("gap", "Brecha de fidelidad"), ("stability", "Estabilidad"),
                ("sparsity", "Parsimonia"), ("cost_ms", "Coste")]
    style = {"lime": "-", "shap": "--", "anchors": "-.", "dice": ":"}
    fig, axes = plt.subplots(4, 1, figsize=(8.6, 7.4), sharex=True)
    for ax, (key, title) in zip(axes, measures):
        part = ranks[ranks["measure"] == key].set_index("dataset").loc[names]
        for m in ["lime", "shap", "anchors", "dice"]:
            ax.plot(range(len(names)), part[m], marker=MARKER[m], ls=style[m], color=COLOR[m],
                    ms=5, lw=1.2, label=LABEL[m])
        ax.set_ylim(4.4, 0.6)
        ax.set_yticks([1, 2, 3, 4])
        ax.set_ylabel("Rango")
        ax.set_title(title, loc="left")
    axes[-1].set_xticks(range(len(names)), [n.replace("_", " ") for n in names], rotation=45,
                        ha="right")
    axes[0].legend(loc="lower right", ncol=4, frameon=False, bbox_to_anchor=(1.0, 1.02))
    fig.text(0.01, -0.02, "Fuente: ranks.csv del estudio. Rango de cada método "
             "en cada conjunto de datos (1 = mejor); Adult, a la izquierda, es la referencia.", **NOTE)
    fig.tight_layout()
    save(fig, "fig_seg_transferencia_es.png")


def figure_judges() -> None:
    """ICC(1,1) of two dimensions for the stored texts and with each degraded version added."""
    t = pd.read_csv(JUDGES / "positive_control_icc.csv")
    t = t[t["scope"] == "shap_lime_nonzero"].set_index(["dimension", "set"])
    dimensions = [("completeness", "Completitud"), ("semantic_plausibility", "Plausibilidad semántica")]
    sets = [("original", "Textos almacenados", "#555555"),
            ("original+truncated", "Con los textos truncados", "#1b6ca8"),
            ("original+shuffled", "Con los pesos reasignados", "#c0392b")]
    fig, ax = plt.subplots(figsize=(6.6, 2.9))
    for i, (dim, _) in enumerate(dimensions):
        for j, (key, _, colour) in enumerate(sets):
            r = t.loc[(dim, key)]
            y = i + (j - 1) * 0.22
            ax.errorbar(r["icc_1_1"], y, xerr=[[r["icc_1_1"] - r["ci_lower"]],
                                              [r["ci_upper"] - r["icc_1_1"]]],
                        fmt="o", color=colour, ms=6, capsize=3, lw=1.3)
    ax.axvline(0.75, color="#333333", lw=1.0, ls="--")
    ax.text(0.755, -0.52, "umbral de fiabilidad aceptable", fontsize=7.5, color="#333333", va="top")
    ax.set_yticks(range(len(dimensions)), [d for _, d in dimensions])
    ax.set_ylim(len(dimensions) - 0.45, -0.6)
    ax.set_xlim(-0.05, 1.0)
    ax.set_xlabel("ICC(1,1) entre los tres jueces, con intervalo del 95 %")
    ax.grid(axis="x", ls=":", alpha=0.5)
    ax.legend(handles=[Line2D([], [], color=c, marker="o", ls="", label=lab) for _, lab, c in sets],
              loc="lower right", frameon=True)
    fig.text(0.01, -0.05, "Fuente: positive_control_icc.csv del estudio. Casos de SHAP "
             "y LIME con algún peso no nulo.", **NOTE)
    fig.tight_layout()
    save(fig, "fig_seg_jueces_es.png")


def main() -> None:
    setup()
    print("Figuras del capítulo de estudios de seguimiento:")
    figure_error()
    figure_margin()
    figure_concordance()
    figure_transfer()
    figure_judges()
    print(f"en {OUT}")


if __name__ == "__main__":
    main()
