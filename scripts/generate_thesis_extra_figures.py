#!/usr/bin/env python3
"""Figures of the thesis outside the result figures of Chapter 4 and Chapter 6.

Three groups, all written to thesis/assets/figures:

1. Concept figures shared with the book chapter. They are drawn by the chapter's own
   generators (generate_cifie_didactic_figures.py, generate_cifie_equation_figures.py),
   run here with their output sent to the thesis folder only; the chapter folders belong to
   another lane and are not written.
2. Structure diagrams of the thesis: map of studies, units of analysis, the four axes of
   the taxonomy, selection guide, sequence of the evidence. They print no result; the
   counts they show (300, 275, 75, 15) are design facts stated in Chapter 3.
3. Two data figures: reliability of the LLM judges by dimension in both cohorts, and
   median cost by model family for SHAP and LIME. No value is printed as a label.

    python scripts/generate_thesis_extra_figures.py
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "thesis" / "assets" / "figures"
EXP2 = ROOT / "outputs" / "analysis" / "paper_a_exp2_stats"
COHORT1 = ROOT / "outputs" / "analysis" / "exp4_llm_evaluation" / "icc_analysis.csv"
COHORT2 = ROOT / "outputs" / "analysis" / "exp4_cohort2" / "cohort2_reliability_by_view.csv"

# Chapter figures reused in the thesis (review of 2026-10-13). d5 is left out (the thesis
# says little about audiences) and d12 too (its gate labels are not those of FOM-7 here).
SHARED = {"generate_cifie_didactic_figures": ["d1", "d2", "d3", "d4", "d6", "d7", "d8"],
          "generate_cifie_equation_figures": ["generate_d9_lime_geometria",
                                              "generate_d10_shap_coaliciones",
                                              "generate_d11_anchors_dice"]}

COLOR = {"shap": "#c0392b", "lime": "#1b6ca8", "anchors": "#2e8b57", "dice": "#6c3483"}
INK, GREY, PALE = "#1a1a1a", "#666666", "#f3f4f6"
BLUE, TEAL, AMBER, PLUM = "#1e40af", "#0f766e", "#b45309", "#6b21a8"
NOTE = dict(fontsize=7.5, color="#555555")


# --- helpers -----------------------------------------------------------------

def canvas(width: float, height: float) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text="", *, fill="white", edge=INK, size=8.0, weight="normal",
        color=INK, lw=0.9, ls="-", align="center") -> None:
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor=fill, edgecolor=edge, lw=lw, ls=ls))
    tx = x + w / 2 if align == "center" else x + 0.12
    ax.text(tx, y + h / 2, text, ha=align, va="center", fontsize=size, fontweight=weight,
            color=color, linespacing=1.25)


def arrow(ax, p0, p1, *, color=INK, lw=1.0, ls="-") -> None:
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=10, color=color,
                                 lw=lw, ls=ls, shrinkA=0, shrinkB=0))


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  {name}")


# --- 1. figures shared with the book chapter ---------------------------------

def shared_figures() -> None:
    scratch = Path(tempfile.mkdtemp(prefix="thesis_figs_"))
    for name, keys in SHARED.items():
        spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.OUT_PNG, mod.OUT_EDIT, mod.OUT_BW = OUT, scratch, scratch
        for key in keys:
            (mod.FIGURES[key] if hasattr(mod, "FIGURES") and key in mod.FIGURES
             else getattr(mod, key))(is_bw=False)
            plt.close("all")


# --- 2. structure diagrams ----------------------------------------------------

def figure_map() -> None:
    """Studies of the thesis: objective, hypothesis or proposition, chapters, status."""
    fig, ax = canvas(9.6, 6.3)
    cols = [(0.1, 1.95, "Objetivo"), (2.15, 2.95, "Estudio"),
            (5.2, 1.35, "Hipótesis o\nproposición"), (6.65, 1.1, "Capítulos")]
    status_x, status_w = 7.85, 1.65
    for x, w, title in cols + [(status_x, status_w, "Estatuto")]:
        box(ax, x, 5.62, w, 0.52, title, fill=INK, color="white", weight="bold", size=8.5)
    groups = [
        ("Plan\nconfirmativo", BLUE, [
            ("OE1 y OE4\n(transversales)", "Protocolo FOM-7 y su\nreproducibilidad", "P1", "3 y 4"),
            ("OE2", "Estudio Omnibus Multimétrico", "H1, H2", "3 y 4"),
            ("OE3", "Estudio Pareado LIME–SHAP", "H3", "3 y 4"),
            ("OE5", "Estudio Taxonómico", "—", "5")]),
        ("Exploratorio,\ndeclarado", AMBER, [
            ("OE6", "Estudio de Fiabilidad Inter-juez", "P2", "3, 5 y 6")]),
        ("Seguimiento,\nposterior al plan", TEAL, [
            ("Objetivo general\n(alcance de validez)", "Fiabilidad ante el Error", "—", "6"),
            ("", "Concordancia entre Explicadores", "—", "6"),
            ("", "Transferencia entre\nConjuntos de Datos", "—", "6")]),
    ]
    y = 5.5
    for label, colour, rows in groups:
        top = y
        for objective, study, hyp, chapters in rows:
            y -= 0.62
            for (x, w, _), text in zip(cols, (objective, study, hyp, chapters)):
                if text:
                    box(ax, x, y, w, 0.52, text, edge=colour, size=7.5,
                        weight="bold" if x == cols[1][0] else "normal")
        box(ax, status_x, y, status_w, top - 0.1 - y, label, fill=colour, edge=colour,
            color="white", weight="bold", size=8.0)
        y -= 0.14
    save(fig, "fig_mapa_tesis_es.png")


def figure_units() -> None:
    """From planned runs to the two units of inference."""
    fig, ax = canvas(9.4, 4.5)
    box(ax, 0.1, 2.75, 2.5, 1.2, "300 ejecuciones planificadas\n5 modelos × 4 métodos ×\n5 semillas × 3 tamaños",
        fill=PALE, size=7.8)
    box(ax, 3.3, 2.75, 2.5, 1.2, "275 ejecuciones analizables\ntras la auditoría de integridad\n(puerta 3)",
        fill=PALE, size=7.8)
    arrow(ax, (2.62, 3.35), (3.28, 3.35))
    box(ax, 6.55, 3.25, 2.75, 1.05,
        "15 bloques (modelo × tamaño)\nmedia de las semillas por método", edge=BLUE, size=7.8,
        weight="bold")
    box(ax, 6.55, 1.45, 2.75, 1.05,
        "75 celdas pareadas\n(modelo × semilla × tamaño)\ncon SHAP y LIME", edge=AMBER, size=7.8,
        weight="bold")
    arrow(ax, (5.82, 3.5), (6.53, 3.78), color=BLUE)
    arrow(ax, (5.82, 3.2), (6.53, 2.0), color=AMBER)
    ax.text(7.92, 3.12, "Friedman y Nemenyi (H1, H2)\nseguimiento dirigido SHAP–LIME", ha="center",
            va="top", fontsize=7.4, color=BLUE)
    ax.text(7.92, 1.32, "Wilcoxon pareado con Holm (H3)", ha="center", va="top", fontsize=7.4,
            color=AMBER)
    box(ax, 0.1, 0.35, 5.7, 1.0,
        "Dentro de cada ejecución, las instancias explicadas se resumen en una media.\n"
        "Las instancias no son unidad de inferencia:\n"
        "tratarlas como réplicas sería pseudorreplicación.",
        edge=GREY, ls="--", size=7.6, color=GREY)
    arrow(ax, (4.55, 1.37), (4.55, 2.73), color=GREY, ls="--")
    ax.text(0.1, 4.25, "Unidad de observación", fontsize=8.4, fontweight="bold")
    ax.text(6.55, 4.38, "Unidad de inferencia", fontsize=8.4, fontweight="bold")
    save(fig, "fig_unidades_analisis_es.png")


def figure_taxonomy() -> None:
    """The four axes, their categories, and the path of each benchmark metric."""
    axes_def = [
        ("Eje 1\nObjetivo de evaluación",
         ["Representatividad local", "Consistencia bajo\nperturbación", "Compacidad explicativa",
          "Relevancia causal local", "Eficiencia operativa"]),
        ("Eje 2\nFuente de evidencia",
         ["Enmascaramiento de\ncaracterísticas", "Perturbación del input",
          "Medición directa\n(conteo, tiempo)", "Comparación con\nverdad-terreno",
          "Estudio con usuario"]),
        ("Eje 3\nPropiedad de calidad",
         ["Fidelidad", "Estabilidad / robustez", "Parsimonia", "Eficiencia", "Completitud",
          "Equidad"]),
        ("Eje 4\nContexto de tarea",
         ["Auditoría y cumplimiento", "Diagnóstico y depuración", "Soporte a usuario final",
          "Inferencia en tiempo real"]),
    ]
    # Index of the category of each axis that each benchmark metric occupies
    # (Table tbl-taxonomia-benchmark of Chapter 5).
    metrics = [("Fidelidad", "#1f2937", "-", (0, 0, 0, 0)),
               ("Estabilidad", "#0f766e", "--", (1, 1, 1, 0)),
               ("Parsimonia", "#b45309", "-.", (2, 2, 2, 2)),
               ("Brecha de fidelidad", "#6b21a8", ":", (3, 0, 0, 1)),
               ("Coste", "#be123c", (0, (5, 1)), (4, 2, 3, 3))]
    fig, ax = canvas(9.6, 5.9)
    w, h, gap_x = 1.95, 0.56, 0.5
    centres: list[list[tuple[float, float]]] = []
    for i, (title, cats) in enumerate(axes_def):
        x = 0.1 + i * (w + gap_x)
        box(ax, x, 5.05, w, 0.7, title, fill=INK, color="white", weight="bold", size=8.0)
        used = {m[3][i] for m in metrics}
        col = []
        for j, cat in enumerate(cats):
            y = 4.25 - j * 0.72
            box(ax, x, y, w, h, cat, size=7.2, fill="white" if j in used else PALE,
                edge=INK if j in used else "#9ca3af", color=INK if j in used else "#6b7280",
                ls="-" if j in used else "--")
            col.append((x, y + h / 2))
        centres.append(col)
    offsets = [-0.16, -0.08, 0.0, 0.08, 0.16]
    for (name, colour, style, path), off in zip(metrics, offsets):
        for i in range(3):
            x0, y0 = centres[i][path[i]]
            x1, y1 = centres[i + 1][path[i + 1]]
            ax.plot([x0 + w, x1], [y0 + off, y1 + off], color=colour, ls=style, lw=1.6)
    ax.legend(handles=[Line2D([], [], color=c, ls=s, lw=1.8, label=n) for n, c, s, _ in metrics],
              loc="lower center", ncol=5, frameon=False, fontsize=7.8,
              bbox_to_anchor=(0.5, -0.12), title="Métricas del benchmark", title_fontsize=8)
    ax.text(0.1, 0.5, "En gris y con trazo discontinuo:\ncategorías que el benchmark no cubre.",
            **NOTE)
    save(fig, "fig_taxonomia_ejes_es.png")


def figure_guide() -> None:
    """Prescriptive criteria of the conclusions: requirement, method, condition to verify."""
    fig, ax = canvas(9.6, 5.3)
    heads = [(0.1, 3.0, "Requisito dominante"), (3.45, 1.5, "Método"),
             (5.3, 4.2, "Condición que verificar antes de usarlo")]
    for x, w, t in heads:
        box(ax, x, 4.65, w, 0.5, t, fill=INK, color="white", weight="bold", size=8.3)
    rows = [
        ("Fidelidad o consistencia\nexplicativa verificables", "shap", "SHAP",
         "Comprobar el umbral en la familia de modelo concreta;\nen modelos de árboles, la variante TreeSHAP"),
        ("Latencia crítica, sin comparar\nexplicaciones entre ejecuciones", "lime", "LIME",
         "Medir la estabilidad en el espacio de características\ny la configuración del despliegue"),
        ("Regla SI–ENTONCES exigida\npor norma o por el usuario", "anchors", "Anchors",
         "Modelo de baja complejidad; revisar cobertura\ny coste por instancia"),
        ("Acción correctiva para\ncambiar la predicción", "dice", "DiCE",
         "Factibilidad de los cambios propuestos;\ncoste elevado, sin sustituto para este objetivo"),
    ]
    for k, (need, key, label, cond) in enumerate(rows):
        y = 3.75 - k * 0.86
        box(ax, 0.1, y, 3.0, 0.7, need, size=7.6)
        box(ax, 3.45, y, 1.5, 0.7, label, fill=COLOR[key], edge=COLOR[key], color="white",
            weight="bold", size=9)
        box(ax, 5.3, y, 4.2, 0.7, cond, size=7.4, edge=COLOR[key])
        arrow(ax, (3.12, y + 0.35), (3.43, y + 0.35))
        arrow(ax, (4.97, y + 0.35), (5.28, y + 0.35), color=COLOR[key])
    box(ax, 0.1, 0.2, 9.4, 0.68,
        "En todos los casos: reportar la calidad por separado para predicciones correctas e incorrectas, "
        "indicar la repetibilidad\ndel explicador y declarar el protocolo de evaluación. "
        "Criterios válidos para las condiciones del benchmark (datos tabulares).",
        fill=PALE, edge=GREY, size=7.3, color="#374151")
    save(fig, "fig_guia_seleccion_es.png")


def figure_sequence() -> None:
    """Order of the evidence: what the frozen plan covers and what came after it."""
    fig, ax = canvas(9.6, 3.3)
    stages = [("EXP1", "calibración y\nreproducibilidad", GREY),
              ("EXP2", "benchmark primario\nH1, H2, H3, P1", BLUE),
              ("EXP3", "validación externa\nparcial", AMBER),
              ("Taxonomía", "cuatro ejes y\ntres brechas", AMBER),
              ("EXP4", "jueces LLM, dos\ncohortes (P2)", AMBER),
              ("Seguimiento", "tres estudios y\ncontroles", TEAL)]
    w, gap = 1.38, 0.2
    for i, (name, text, colour) in enumerate(stages):
        x = 0.15 + i * (w + gap)
        box(ax, x, 1.55, w, 0.42, name, fill=colour, edge=colour, color="white", weight="bold",
            size=8.2)
        box(ax, x, 0.8, w, 0.72, text, edge=colour, size=7.3)
        if i:
            arrow(ax, (x - gap + 0.02, 1.76), (x - 0.02, 1.76))
    gate_x = 0.15 + w + gap / 2
    ax.plot([gate_x, gate_x], [0.55, 2.55], color=INK, lw=1.4, ls="--")
    ax.text(gate_x, 2.62, "Puerta 1: plan\ninferencial congelado", ha="center", va="bottom",
            fontsize=7.6, fontweight="bold")
    def bracket(x0, x1, label, colour):
        ax.plot([x0, x0, x1, x1], [2.12, 2.24, 2.24, 2.12], color=colour, lw=1.3)
        ax.text((x0 + x1) / 2, 2.3, label, ha="center", va="bottom", fontsize=7.6, color=colour,
                fontweight="bold")
    step = w + gap
    bracket(0.15 + step, 0.15 + step + w, "confirmativo", BLUE)
    bracket(0.15 + 2 * step, 0.15 + 4 * step + w, "complementario y exploratorio", AMBER)
    bracket(0.15 + 5 * step, 0.15 + 5 * step + w, "posterior", TEAL)
    ax.text(0.15, 0.2, "Orden de realización, sin escala temporal. Solo EXP2 sostiene las "
            "hipótesis confirmativas;\nlo situado a su derecha se declara como posterior al plan.",
            **NOTE)
    save(fig, "fig_secuencia_evidencia_es.png")


# --- 3. data figures ----------------------------------------------------------

def figure_judges_cohorts() -> None:
    """ICC(1,1) by dimension, original cohort and replication (primary condition)."""
    names = {"completeness": "Completitud", "semantic_plausibility": "Plausibilidad semántica",
             "overall_quality": "Calidad global", "audit_usefulness": "Utilidad para auditoría",
             "concision": "Concisión", "actionability": "Accionabilidad", "clarity": "Claridad"}
    c1 = pd.read_csv(COHORT1).set_index("dimension")
    c2 = pd.read_csv(COHORT2)
    c2 = c2[c2["view"] == "hidden_label_primary"].set_index("dimension")
    order = sorted(names, key=lambda d: -c1.loc[d, "icc_2_1"])
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    for y, dim in enumerate(order):
        for table, col, colour, marker, off in ((c1, "icc_2_1", "#374151", "o", -0.16),
                                                (c2, "icc_1_1", "#0f766e", "s", 0.16)):
            r = table.loc[dim]
            ax.errorbar(r[col], y + off, xerr=[[r[col] - r["ci_lower"]], [r["ci_upper"] - r[col]]],
                        fmt=marker, color=colour, ms=6, capsize=3, lw=1.3)
    ax.axvline(0.75, color=INK, lw=1.0, ls="--")
    ax.axvspan(0.75, 1.0, color="#e5e7eb", alpha=0.6, lw=0)
    ax.text(0.875, -0.75, "fiabilidad\naceptable", ha="center", va="center", fontsize=7.4,
            color="#374151")
    ax.set_yticks(range(len(order)), [names[d] for d in order])
    ax.set_ylim(len(order) - 0.5, -1.1)
    ax.set_xlim(-0.2, 1.0)
    ax.set_xlabel("ICC(1,1) entre los tres jueces, con intervalo del 95 %")
    ax.grid(axis="x", ls=":", alpha=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(handles=[
        Line2D([], [], color="#374151", marker="o", ls="", label="Cohorte original (147 casos)"),
        Line2D([], [], color="#0f766e", marker="s", ls="",
               label="Cohorte de replicación, condición primaria (192 casos)")],
        loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=2, frameon=False, fontsize=8)
    fig.text(0.01, -0.1, "Fuente: icc_analysis.csv y cohort2_reliability_by_view.csv.", **NOTE)
    fig.tight_layout()
    save(fig, "fig_fiabilidad_jueces_es.png")


def figure_cost_by_model() -> None:
    """Median cost per explanation by model family, SHAP against LIME."""
    df = pd.read_csv(EXP2 / "paired_cells_shap_lime_all_models.csv")
    med = df.groupby("model")[["shap_cost", "lime_cost"]].median()
    order = ["logreg", "rf", "xgb", "mlp", "svm"]
    labels = ["Regresión\nlogística", "Bosque\naleatorio", "XGBoost", "MLP", "SVM"]
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    x = range(len(order))
    ax.bar([i - 0.19 for i in x], med.loc[order, "lime_cost"], width=0.38, color=COLOR["lime"],
           label="LIME")
    ax.bar([i + 0.19 for i in x], med.loc[order, "shap_cost"], width=0.38, color=COLOR["shap"],
           label="SHAP")
    ax.set_yscale("log")
    ax.set_xticks(list(x), labels)
    ax.set_ylabel("Coste mediano por instancia\n(ms, escala logarítmica)")
    ax.grid(axis="y", ls=":", alpha=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.text(0.01, -0.04, "Fuente: paired_cells_shap_lime_all_models.csv. Mediana de las 15 celdas "
             "pareadas de cada familia de modelos.", **NOTE)
    fig.tight_layout()
    save(fig, "fig_coste_por_modelo_es.png")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                         "ytick.labelsize": 8})
    print("Figuras compartidas con el capítulo de libro:")
    shared_figures()
    plt.rcdefaults()
    plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                         "ytick.labelsize": 8})
    print("Diagramas y figuras de datos:")
    for figure in (figure_map, figure_units, figure_taxonomy, figure_guide, figure_sequence,
                   figure_judges_cohorts, figure_cost_by_model):
        figure()
    print(f"en {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
