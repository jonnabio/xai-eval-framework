#!/usr/bin/env python3
"""English versions of four Chapter 4 figures, for presentations.

  fig_cd_diagram_en.png, fig_boxplots_metrics_en.png,
  fig_paired_differences_en.png, fig_radar_methods_en.png

Until 2026-10-13 this was a separate copy of the Spanish generator, with its own typed
ranks and groups, and it had drifted from it. It now runs the Spanish generator
(generate_thesis_supplementary_figures.py) and translates the text of each figure before
saving, so both languages show the same data, the same colours and the same layout.

The thesis does not use these files.

    python scripts/generate_thesis_supplementary_figures_en.py
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.text import Text

HERE = Path(__file__).resolve().parent
FILES = {"fig_cd_diagram_es.png": "fig_cd_diagram_en.png",
         "fig_boxplots_metricas_es.png": "fig_boxplots_metrics_en.png",
         "fig_diferencias_pareadas_es.png": "fig_paired_differences_en.png",
         "fig_radar_metodos_es.png": "fig_radar_methods_en.png"}

# Applied in this order: whole phrases first, single words last.
TRANSLATION = [
    ("Diagrama de diferencia crítica", "Critical difference diagram"),
    ("Las barras horizontales gruesas conectan métodos no significativamente distintos "
     "(diferencia de rangos < DC).",
     "Thick horizontal bars join methods that are not significantly different "
     "(rank difference < CD)."),
    ("Rango medio (mejor → izquierda)", "Mean rank (better → left)"),
    ("Diagrama DC —", "CD diagram —"),
    ("DC =", "CD ="),
    ("Distribución de métricas por método (n=15 bloques por método)",
     "Distribution of metrics by method (n=15 blocks per method)"),
    ("Cada punto representa un bloque (modelo, tamaño de muestra).",
     "Each point is one block (model, sample size)."),
    ("por método — distribución de bloques", "by method — distribution over blocks"),
    ("media por bloque (g, n)", "mean per block (g, n)"),
    ("Diferencias pareadas SHAP − LIME por celda (n=75 celdas (modelo, semilla, n))",
     "Paired differences SHAP − LIME per cell (n=75 cells (model, seed, n))"),
    ("Rojo = SHAP superior; azul = LIME superior.", "Red = SHAP higher; blue = LIME higher."),
    ("Diferencias pareadas —", "Paired differences —"),
    ("Celda pareada (ordenada por diferencia decreciente)",
     "Paired cell (sorted by decreasing difference)"),
    ("positivas", "positive"), ("negativas", "negative"), ("Media =", "Mean ="),
    ("Perfil multidimensional por método", "Multidimensional profile by method"),
    ("(normalizado [0,1]; radio mayor = mejor)", "(normalised [0,1]; larger radius = better)"),
    ("Parsimonia y eficiencia están invertidas (mayor radio = mejor).",
     "Sparsity and efficiency are inverted (larger radius = better)."),
    ("Brecha\nfidelidad", "Faithfulness\ngap"),
    ("Eficiencia\n(coste inv.)", "Efficiency\n(inverse cost)"),
    ("Fuente:", "Source:"),
    ("Fidelidad", "Fidelity"), ("Estabilidad", "Stability"), ("Parsimonia", "Sparsity"),
]


def translate(text: str) -> str:
    for spanish, english in TRANSLATION:
        text = text.replace(spanish, english)
    return text


def main() -> None:
    spec = importlib.util.spec_from_file_location(
        "thesis_figures_es", HERE / "generate_thesis_supplementary_figures.py")
    es = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(es)

    def save_english(fig: plt.Figure, filename: str) -> None:
        for item in fig.findobj(Text):
            item.set_text(translate(item.get_text()))
        for ax in fig.axes:
            # The axis names of the radar are tick labels, which matplotlib writes again
            # from the axis at draw time.
            if ax.name == "polar":
                ax.set_xticklabels([translate(t.get_text()) for t in ax.get_xticklabels()])
        fig.tight_layout()
        fig.savefig(es.OUT / FILES[filename], bbox_inches="tight")
        plt.close(fig)
        print(f"  Saved: {FILES[filename]}")

    es.save = save_english
    es.setup()
    print("Generating the English figures from the Spanish generator...")
    es.figure_cd_diagram()
    es.figure_boxplots()
    es.figure_paired_differences()
    es.figure_radar()


if __name__ == "__main__":
    main()
