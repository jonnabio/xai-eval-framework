#!/usr/bin/env python3
"""Generate the didactic figures D1-D8 of the CIFIE chapter (Color + B/W versions).

Supports generating:
1. Color version (default digital edition) stored under:
   publications/book_chapters/2026_cifie_xai_fom7/figures/exported/
   publications/book_chapters/2026_cifie_xai_fom7/figures/editable/
2. Black & White version (dedicated print edition) stored under:
   publications/book_chapters/2026_cifie_xai_fom7/figures/bw/

Usage: python scripts/generate_cifie_didactic_figures.py [--only d1,d4,...] [--mode color|bw|both]
"""
from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Polygon

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "publications" / "book_chapters" / "2026_cifie_xai_fom7" / "figures"
OUT_PNG = FIG / "exported"
OUT_EDIT = FIG / "editable"
OUT_BW = FIG / "bw"

# ---------------------------------------------------------------- style tokens
INK = "#1a1a1a"      # text, outlines, arrows
DARK = "#4a4a4a"     # header bands
MID = "#8a8a8a"      # secondary marks
LIGHT = "#d6d6d6"    # fills
PALE = "#eeeeee"     # background panels
WHITE = "#ffffff"
LW = 0.8             # standard line width (pt)
TEXT_W = 14.5        # drawing width in cm (text block 14.65 cm)
FS = 7.6             # body text size (pt)
FS_HEAD = 8.2        # box header size (pt)
FS_SMALL = 6.8       # notes

for fname in ("times.ttf", "timesbd.ttf", "timesi.ttf", "timesbi.ttf"):
    path = Path("C:/Windows/Fonts") / fname
    if path.exists():
        font_manager.fontManager.addfont(str(path))
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "custom",
    "mathtext.rm": "Times New Roman",
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "text.color": INK,
    "axes.edgecolor": INK,
    "axes.linewidth": LW,
    "hatch.linewidth": 0.5,
    "hatch.color": MID,
})


def canvas(height_cm: float):
    fig = plt.figure(figsize=(TEXT_W / 2.54, height_cm / 2.54))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, TEXT_W)
    ax.set_ylim(0, height_cm)
    ax.axis("off")
    return fig, ax


def wrap(text: str, width_cm: float, size: float = FS) -> str:
    chars = max(8, int(width_cm * 28.35 / (0.47 * size)))
    return "\n".join(textwrap.fill(p, chars, break_long_words=False, break_on_hyphens=False)
                     for p in text.split("\n"))


def box(ax, x, y, w, h, *, fill=WHITE, edge=INK, lw=LW, hatch=None, radius=0.12, z=1):
    patch = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                           facecolor=fill, edgecolor=edge, linewidth=lw, hatch=hatch, zorder=z)
    ax.add_patch(patch)
    return patch


def header_box(ax, x, y, w, h, title, body=None, *, head_h=0.62, head_fill=DARK,
               body_fill=WHITE, body_size=FS, align="left", hatch=None, head_text_color=WHITE):
    """A rounded box with a colored/dark title band and wrapped body text."""
    box(ax, x, y, w, h, fill=body_fill, hatch=hatch)
    band = FancyBboxPatch((x, y + h - head_h), w, head_h,
                          boxstyle="round,pad=0,rounding_size=0.12",
                          facecolor=head_fill, edgecolor=INK, linewidth=LW, zorder=2)
    ax.add_patch(band)
    ax.add_patch(plt.Rectangle((x, y + h - head_h), w, head_h / 2, facecolor=head_fill,
                               edgecolor="none", zorder=2))
    ax.plot([x, x + w], [y + h - head_h, y + h - head_h], color=INK, lw=LW, zorder=3)
    ax.text(x + w / 2, y + h - head_h / 2, title, ha="center", va="center",
            fontsize=FS_HEAD, fontweight="bold", color=head_text_color, zorder=4)
    if body:
        tx = x + 0.2 if align == "left" else x + w / 2
        ax.text(tx, y + h - head_h - 0.18, wrap(body, w - 0.4, body_size), ha=align,
                va="top", fontsize=body_size, linespacing=1.35, zorder=4)


def arrow(ax, p0, p1, *, lw=LW, style="-|>", color=INK, rad=0.0, ls="-", z=5, ms=9):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, lw=lw,
                                 color=color, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}", zorder=z,
                                 shrinkA=0, shrinkB=0))


def note(ax, x, y, text, *, width=None, size=FS_SMALL, ha="left", style="italic", color=DARK):
    txt = wrap(text, width, size) if width else text
    ax.text(x, y, txt, ha=ha, va="top", fontsize=size, style=style, color=color,
            linespacing=1.3)


def save(fig, stem: str, is_bw: bool = False) -> None:
    if is_bw:
        OUT_BW.mkdir(parents=True, exist_ok=True)
        fig.savefig(OUT_BW / f"{stem}.png", dpi=600, facecolor=WHITE)
        fig.savefig(OUT_BW / f"{stem}.pdf", facecolor=WHITE)
        fig.savefig(OUT_BW / f"{stem}.svg", facecolor=WHITE)
        print(f"OK (BW): figures/bw/{stem}.png")
    else:
        OUT_PNG.mkdir(parents=True, exist_ok=True)
        OUT_EDIT.mkdir(parents=True, exist_ok=True)
        fig.savefig(OUT_PNG / f"{stem}.png", dpi=600, facecolor=WHITE)
        fig.savefig(OUT_EDIT / f"{stem}.pdf", facecolor=WHITE)
        fig.savefig(OUT_EDIT / f"{stem}.svg", facecolor=WHITE)
        print(f"OK (Color): figures/exported/{stem}.png")
    plt.close(fig)


# ------------------------------------------------------------------------ D1
def d1_conceptos(is_bw: bool = False) -> None:
    """Transparency, interpretability and explainability: three distinct notions."""
    H = 10.7
    fig, ax = canvas(H)
    
    sys_fill = PALE if is_bw else "#eff6ff"
    sys_border = INK if is_bw else "#1d4ed8"
    
    box(ax, 4.6, 9.25, 5.3, 1.15, fill=sys_fill, edge=sys_border, lw=1.0)
    ax.text(7.25, 9.98, "Sistema de IA", ha="center", va="center", fontsize=9.2,
            fontweight="bold", color="#1e3a8a" if not is_bw else INK)
    ax.text(7.25, 9.53, "modelo, datos, proceso y contexto de uso", ha="center",
            va="center", fontsize=FS, style="italic")

    if is_bw:
        head_colors = [DARK, DARK, DARK]
        limit_fills = [PALE, PALE, PALE]
        limit_hatches = [None, None, None]
    else:
        head_colors = ["#1e40af", "#0f766e", "#6b21a8"]
        limit_fills = ["#eff6ff", "#f0fdf4", "#faf5ff"]
        limit_hatches = [None, None, None]

    cols = [
        ("Transparencia", "¿Qué elementos del sistema son visibles?",
         "Visibilidad de la estructura, los datos, los supuestos, la documentación, "
         "las versiones y las responsabilidades.",
         "Publicar documentación no demuestra que una explicación individual refleje "
         "con exactitud la salida."),
        ("Interpretabilidad", "¿Qué puede comprender una audiencia, para una tarea?",
         "Relación por la que una audiencia comprende aspectos relevantes del "
         "funcionamiento o de la salida del sistema.",
         "Un modelo sencillo para una persona experta puede ser opaco para otra "
         "audiencia."),
        ("Explicabilidad", "¿Qué procedimientos producen comprensión o razones?",
         "Procedimientos y artefactos que intentan producir esa comprensión o aportar "
         "razones examinables.",
         "Una explicación post-hoc no vuelve transparente el modelo: aproxima una "
         "parte de su comportamiento."),
    ]
    w, gap, x0, y0, h = 4.45, 0.33, 0.25, 2.05, 6.5
    for i, (name, question, definition, limit) in enumerate(cols):
        x = x0 + i * (w + gap)
        header_box(ax, x, y0, w, h, name, head_h=0.66, head_fill=head_colors[i])
        ax.text(x + w / 2, y0 + h - 0.95, wrap(question, w - 0.4, FS), ha="center",
                va="top", fontsize=FS, fontweight="bold", linespacing=1.3)
        ax.text(x + 0.22, y0 + h - 2.0, wrap(definition, w - 0.44, FS), ha="left",
                va="top", fontsize=FS, linespacing=1.38)
        # limit panel
        box(ax, x + 0.18, y0 + 0.18, w - 0.36, 2.15, fill=limit_fills[i], radius=0.08, hatch=limit_hatches[i])
        ax.text(x + 0.35, y0 + 2.12, "Lo que no garantiza", fontsize=FS_SMALL,
                fontweight="bold", va="top", color="#991b1b" if not is_bw else INK)
        ax.text(x + 0.35, y0 + 1.76, wrap(limit, w - 0.7, FS_SMALL), fontsize=FS_SMALL,
                va="top", style="italic", linespacing=1.3)
        arrow(ax, (7.25 + (i - 1) * 1.6, 9.25), (x + w / 2, y0 + h + 0.02),
              color="#1d4ed8" if not is_bw else INK)
    # common boundary
    b_fill = WHITE if is_bw else "#fffbeb"
    b_edge = INK if is_bw else "#d97706"
    box(ax, 0.25, 0.2, TEXT_W - 0.5, 1.45, fill=b_fill, edge=b_edge, hatch="////" if is_bw else None)
    box(ax, 0.55, 0.42, TEXT_W - 1.1, 1.0, fill=WHITE, lw=0)
    ax.text(TEXT_W / 2, 0.92,
            wrap("Ninguna de las tres equivale a confiabilidad: esta depende además de "
                 "validez, seguridad, robustez, privacidad, equidad y gobernanza.",
                 TEXT_W - 1.6, FS), ha="center", va="center", fontsize=FS,
            linespacing=1.35)
    save(fig, "fig_d1_conceptos_es", is_bw)


# ------------------------------------------------------------------------ D2
def d2_modelos(is_bw: bool = False) -> None:
    """From interpretable-by-design models to black boxes and post-hoc explanation."""
    H = 10.6
    fig, ax = canvas(H)
    # spectrum arrow
    y_arrow = 9.95
    arrow(ax, (0.4, y_arrow), (TEXT_W - 0.3, y_arrow), lw=1.1, ms=11, color="#1e40af" if not is_bw else INK)
    ax.text(TEXT_W / 2, y_arrow + 0.22,
            "Dificultad de una audiencia para comprender el modelo directamente",
            ha="center", va="bottom", fontsize=FS, style="italic", color="#1e3a8a" if not is_bw else INK)

    if is_bw:
        stage_colors = [DARK, DARK, DARK]
        stage_fills = [WHITE, PALE, LIGHT]
        stage_hatches = [None, None, "////"]
        agn_head, spec_head = DARK, MID
        post_fill = PALE
    else:
        stage_colors = ["#065f46", "#92400e", "#9f1239"]
        stage_fills = ["#ecfdf5", "#fffbeb", "#fff1f2"]
        stage_hatches = [None, None, None]
        agn_head, spec_head = "#1e40af", "#075985"
        post_fill = "#eff6ff"

    stages = [
        ("Interpretables por diseño",
         "Reglas breves, árboles poco profundos y modelos aditivos con componentes "
         "controlados.", stage_fills[0], stage_hatches[0]),
        ("Interpretabilidad frágil",
         "Un árbol extenso o una regla con numerosas excepciones deja de ser "
         "comprensible en la práctica.", stage_fills[1], stage_hatches[1]),
        ("Cajas negras",
         "Ensambles de árboles, máquinas de vectores soporte con kernel y redes "
         "neuronales.", stage_fills[2], stage_hatches[2]),
    ]
    w, gap, y, h = 4.5, 0.25, 6.75, 2.75
    for i, (name, body, fill, hatch) in enumerate(stages):
        x = 0.25 + i * (w + gap)
        header_box(ax, x, y, w, h, name, body, head_fill=stage_colors[i], body_fill=fill, hatch=hatch)

    bx = 0.25 + 2 * (w + gap) + w / 2
    arrow(ax, (bx, y), (bx, 5.62))
    box(ax, 0.25, 4.82, TEXT_W - 0.5, 0.8, fill=post_fill, edge="#2563eb" if not is_bw else INK)
    ax.text(7.25, 5.22, "Explicación post-hoc: una aproximación sometida a prueba, "
            "no transparencia recuperada", ha="center", va="center", fontsize=FS,
            fontweight="bold", color="#1e3a8a" if not is_bw else INK)
    arrow(ax, (3.72, 4.82), (3.72, 4.07))
    arrow(ax, (10.77, 4.82), (10.77, 4.07))
    header_box(ax, 0.25, 1.0, 6.95, 3.05, "Agnóstica al modelo",
               "Consulta entradas y salidas sin acceder a parámetros internos. Portable "
               "entre familias de modelos; solo observa el comportamiento accesible "
               "mediante sus consultas.\nEjemplos: LIME, KernelSHAP, Anchors, DiCE.",
               head_fill=agn_head, body_fill="#f8fafc" if not is_bw else WHITE)
    header_box(ax, 7.3, 1.0, 6.95, 3.05, "Específica del modelo",
               "Aprovecha gradientes, activaciones o la estructura de los árboles. "
               "Puede ser más eficiente o precisa dentro de una familia, pero es menos "
               "transferible.\nEjemplo: TreeSHAP para modelos de árboles.",
               head_fill=spec_head, body_fill="#f8fafc" if not is_bw else WHITE)
    note(ax, 0.3, 0.72, "Agnosticidad y especificidad son decisiones de diseño, no "
         "calificaciones de calidad. Si un modelo interpretable ofrece un desempeño "
         "adecuado, conviene considerarlo antes que una caja negra con explicación "
         "aproximada.", width=TEXT_W - 0.6)
    save(fig, "fig_d2_modelos_es", is_bw)


# ------------------------------------------------------------------------ D3
def d3_local_global(is_bw: bool = False) -> None:
    """Local explanation around one instance versus a global summary of many."""
    H = 9.4
    fig = plt.figure(figsize=(TEXT_W / 2.54, H / 2.54))
    rng = np.random.default_rng(7)
    
    # --- panel A: local
    axa = fig.add_axes([0.075, 0.37, 0.40, 0.54])
    xs = rng.uniform(-3, 3, 150)
    ys = rng.uniform(-3, 3, 150)
    boundary = lambda x: 0.35 * x ** 2 - 1.2
    above = ys > boundary(xs)
    
    class_a_color = "#0d9488" if not is_bw else MID
    class_b_color = "#e11d48" if not is_bw else DARK
    approx_color = "#2563eb" if not is_bw else INK
    star_color = "#d97706" if not is_bw else INK
    
    axa.scatter(xs[above], ys[above], s=10, marker="o", facecolor=class_a_color if not is_bw else WHITE,
                edgecolor=class_a_color if not is_bw else MID, linewidth=0.6, zorder=2)
    axa.scatter(xs[~above], ys[~above], s=12, marker="^", color=class_b_color if not is_bw else DARK,
                linewidth=0, zorder=2)
    gx = np.linspace(-3, 3, 200)
    axa.plot(gx, boundary(gx), color=INK, lw=1.0, ls="--", zorder=3)
    px, py = 1.4, boundary(1.4) + 0.12
    slope = 0.7 * px
    lx = np.linspace(px - 1.1, px + 1.1, 20)
    axa.add_patch(Circle((px, py), 1.05, fill=False, ls=":", lw=0.9, edgecolor=INK, zorder=3))
    axa.plot(lx, py + slope * (lx - px), color=approx_color, lw=1.8, zorder=4)
    axa.scatter([px], [py], s=80, marker="*", color=star_color, zorder=5)
    axa.set_xlim(-3, 3); axa.set_ylim(-3, 3)
    axa.set_xticks([]); axa.set_yticks([])
    axa.set_xlabel("Característica 1", fontsize=FS); axa.set_ylabel("Característica 2", fontsize=FS)
    for s in axa.spines.values():
        s.set_linewidth(LW)
    from matplotlib.lines import Line2D
    handles = [
        Line2D([], [], marker="*", color=star_color, ls="none", markersize=8, label="Instancia explicada"),
        Line2D([], [], color=approx_color, lw=1.8, label="Aproximación local"),
        Line2D([], [], color=INK, lw=0.9, ls=":", label="Vecindario local"),
        Line2D([], [], color=INK, lw=1.0, ls="--", label="Frontera del modelo"),
        Line2D([], [], marker="o", markerfacecolor=class_a_color if not is_bw else WHITE,
               markeredgecolor=class_a_color if not is_bw else MID, ls="none",
               markersize=4, label="Clase A"),
        Line2D([], [], marker="^", color=class_b_color if not is_bw else DARK, ls="none",
               markersize=4, label="Clase B"),
    ]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.055, 0.25), ncol=2,
               frameon=False, fontsize=FS_SMALL, handlelength=2.0, columnspacing=1.2,
               handletextpad=0.5, borderaxespad=0)
    fig.text(0.075, 0.955, "A. Alcance local", fontsize=FS_HEAD, fontweight="bold")
    fig.text(0.075, 0.1, wrap("Describe el comportamiento del modelo alrededor de una "
             "instancia: útil para una decisión concreta, un error o un caso límite.",
             6.0, FS_SMALL), fontsize=FS_SMALL, style="italic", va="top", color=DARK)

    # --- panel B: global
    axb = fig.add_axes([0.63, 0.37, 0.34, 0.54])
    feats = ["Característica 1", "Característica 2", "Característica 3",
             "Característica 4", "Característica 5"]
    means = np.array([0.62, 0.45, 0.33, 0.21, 0.12])
    spreads = np.array([0.28, 0.1, 0.24, 0.05, 0.16])
    ypos = np.arange(len(feats))[::-1]
    
    if not is_bw:
        bar_colors = ["#2563eb", "#0d9488", "#059669", "#d97706", "#e11d48"]
    else:
        bar_colors = [LIGHT] * len(feats)
        
    axb.barh(ypos, means, height=0.55, color=bar_colors, edgecolor=INK, linewidth=LW, zorder=2)
    for yv, m, s in zip(ypos, means, spreads):
        pts = np.clip(rng.normal(m, s, 22), 0.0, 1.05)
        axb.scatter(pts, yv + rng.uniform(-0.18, 0.18, pts.size), s=5, color=INK,
                    linewidth=0, zorder=3)
    axb.set_yticks(ypos); axb.set_yticklabels(feats, fontsize=FS_SMALL)
    axb.set_xticks([]); axb.set_xlim(0, 1.1)
    axb.set_xlabel("Importancia (barra: promedio; puntos: casos)", fontsize=FS_SMALL)
    for side in ("top", "right"):
        axb.spines[side].set_visible(False)
    for s in axb.spines.values():
        s.set_linewidth(LW)
    axb.tick_params(length=0)
    fig.text(0.63, 0.955, "B. Alcance global", fontsize=FS_HEAD, fontweight="bold")
    fig.text(0.63, 0.23, wrap("Resume patrones en una población. Agregar explicaciones "
             "locales puede ocultar la heterogeneidad entre casos.", 5.0, FS_SMALL),
             fontsize=FS_SMALL, style="italic", va="top", color=DARK)
    fig.text(0.97, 0.03, "Ilustración esquemática con datos simulados.",
             fontsize=6.2, ha="right", style="italic", color=MID)
    save(fig, "fig_d3_local_global_es", is_bw)


# ------------------------------------------------------------------------ D4
def d4_objetos(is_bw: bool = False) -> None:
    """One illustrative case explained through four explanatory objects."""
    H = 13.2
    fig, ax = canvas(H)
    
    card_fill = PALE if is_bw else "#eff6ff"
    card_edge = INK if is_bw else "#1d4ed8"
    box(ax, 0.25, 11.0, TEXT_W - 0.5, 1.95, fill=card_fill, edge=card_edge)
    ax.text(7.25, 12.62, "Caso ilustrativo", ha="center", va="center",
            fontsize=9, fontweight="bold", color="#1e3a8a" if not is_bw else INK)
    ax.text(7.25, 12.12, "Solicitante: 38 años · estudios universitarios · "
            "ocupación técnica · 35 horas semanales", ha="center", va="center", fontsize=FS)
    ax.text(7.25, 11.5, "Predicción del modelo: ingreso anual ≤ 50.000 USD",
            ha="center", va="center", fontsize=FS, fontweight="bold")
    w, h = 6.95, 4.75
    pos = [(0.25, 5.85), (7.3, 5.85), (0.25, 0.75), (7.3, 0.75)]
    titles = ["Atribución (LIME, SHAP)", "Regla (Anchors)", "Contrafactual (DiCE)",
              "Ejemplos (casos similares)"]
    questions = ["¿Cuánto contribuye cada característica a esta predicción?",
                 "¿Bajo qué condiciones se mantiene la predicción?",
                 "¿Qué cambio alteraría el resultado?",
                 "¿A qué casos conocidos se parece?"]
    
    head_colors = [DARK, DARK, DARK, DARK] if is_bw else ["#1e40af", "#065f46", "#9a3412", "#6b21a8"]
    
    for (x, y), t, q, hc in zip(pos, titles, questions, head_colors):
        header_box(ax, x, y, w, h, t, head_h=0.62, head_fill=hc)
        ax.text(x + w / 2, y + h - 0.85, q, ha="center", va="top", fontsize=FS,
                style="italic")
    # A: attribution bars
    x, y = pos[0]
    feats = [("horas semanales", -0.8), ("ocupación", -0.5), ("estudios", 0.55),
             ("edad", 0.25)]
    cx = x + 4.6
    ax.plot([cx, cx], [y + 0.55, y + 3.45], color=INK, lw=LW)
    for i, (f, v) in enumerate(feats):
        yy = y + 3.05 - i * 0.72
        bar_fill = (DARK if v < 0 else WHITE) if is_bw else ("#dc2626" if v < 0 else "#059669")
        bar_hatch = (None if v < 0 else "////") if is_bw else None
        ax.add_patch(plt.Rectangle((cx, yy - 0.2), v * 2.0, 0.4,
                                   facecolor=bar_fill,
                                   edgecolor=INK, lw=LW, hatch=bar_hatch))
        ax.text(x + 0.25, yy, f, va="center", fontsize=FS)
    ax.text(cx - 1.2, y + 0.3, "hacia ≤ 50.000", ha="center", fontsize=FS_SMALL, style="italic")
    ax.text(cx + 1.2, y + 0.3, "hacia > 50.000", ha="center", fontsize=FS_SMALL, style="italic")
    # B: rule
    x, y = pos[1]
    rule_fill = PALE if is_bw else "#ecfdf5"
    box(ax, x + 0.35, y + 1.45, w - 0.7, 1.95, fill=rule_fill, radius=0.08, edge="#059669" if not is_bw else INK)
    ax.text(x + 0.6, y + 3.05, "SI   horas semanales ≤ 40", fontsize=FS + 0.4, va="top",
            fontweight="bold")
    ax.text(x + 0.6, y + 2.55, "Y    ocupación = técnica", fontsize=FS + 0.4, va="top",
            fontweight="bold")
    ax.text(x + 0.6, y + 2.05, "ENTONCES   ingreso ≤ 50.000 USD", fontsize=FS + 0.4,
            va="top", fontweight="bold", color="#065f46" if not is_bw else INK)
    note(ax, x + 0.35, y + 1.2, "La precisión y la cobertura de la regla deben "
         "informarse juntas: una regla muy estrecha puede ser precisa y aplicarse a muy "
         "pocos casos.", width=w - 0.7)
    # C: counterfactual
    x, y = pos[2]
    rows = [("", "Caso", "Alternativa"), ("horas semanales", "35", "45"),
            ("ocupación", "técnica", "gestión"),
            ("predicción", "≤ 50.000", "> 50.000")]
    for i, (a, b, c) in enumerate(rows):
        yy = y + 3.2 - i * 0.55
        bold = "bold" if i in (0, 3) else "normal"
        ax.text(x + 0.35, yy, a, fontsize=FS, va="center", fontweight=bold)
        ax.text(x + 3.35, yy, b, fontsize=FS, va="center", ha="center", fontweight=bold)
        ax.text(x + 5.6, yy, c, fontsize=FS, va="center", ha="center", fontweight=bold, color="#c2410c" if (not is_bw and i==3) else INK)
        if i in (1, 2, 3):
            arrow(ax, (x + 4.0, yy), (x + 4.85, yy), ms=6, lw=0.6, color="#ea580c" if not is_bw else INK)
    ax.plot([x + 0.3, x + w - 0.3], [y + 2.95, y + 2.95], color=INK, lw=0.5)
    note(ax, x + 0.35, y + 1.05, "Válido para el modelo no significa factible, "
         "accionable ni justo para la persona.", width=w - 0.7)
    # D: examples
    x, y = pos[3]
    ex = [("Caso A", "similar; ≤ 50.000"), ("Caso B", "similar; ≤ 50.000"),
          ("Caso C", "difiere en ocupación; > 50.000")]
    for i, (a, b) in enumerate(ex):
        yy = y + 2.95 - i * 0.62
        ex_fill = (WHITE if i < 2 else LIGHT) if is_bw else (WHITE if i < 2 else "#f3e8ff")
        box(ax, x + 0.35, yy - 0.24, w - 0.7, 0.48, fill=ex_fill,
            radius=0.06)
        ax.text(x + 0.55, yy, a, fontsize=FS, va="center", fontweight="bold")
        ax.text(x + 1.6, yy, b, fontsize=FS, va="center")
    note(ax, x + 0.35, y + 0.95, "Un ejemplo similar puede ser comprensible sin "
         "representar el mecanismo del predictor.", width=w - 0.7)
    ax.text(TEXT_W - 0.25, 0.2, "Caso, valores y explicaciones ilustrativos; no son "
            "resultados del estudio.", ha="right", fontsize=6.2, style="italic", color=MID)
    save(fig, "fig_d4_objetos_explicativos_es", is_bw)


# ------------------------------------------------------------------------ D5
def d5_ciclo_audiencias(is_bw: bool = False) -> None:
    """Explanation functions along the lifecycle, and what each audience needs."""
    H = 10.3
    fig, ax = canvas(H)
    
    head_colors = [DARK, DARK, DARK, DARK] if is_bw else ["#1e40af", "#075985", "#065f46", "#6b21a8"]
    
    stages = [
        ("Diseño", "Descubrir dependencias espurias, variables proxy o fugas de "
         "información.", "Localizar qué características influyen"),
        ("Validación", "Probar casos límite y comparar si distintos modelos se apoyan "
         "en patrones semejantes.", "Comprobar que la señal se conserva ante "
         "perturbaciones"),
        ("Operación", "Monitorear cambios, analizar incidentes y señalar salidas que "
         "requieren revisión.", "Comunicar incertidumbre, límites y condiciones de uso"),
        ("Tras la decisión", "Documentar, auditar y permitir impugnar el "
         "resultado.", "Trazar datos, versión del modelo, explicador y conclusión"),
    ]
    ax.text(0.25, H - 0.25, "A. Funciones de la explicación a lo largo del ciclo de vida",
            fontsize=FS_HEAD, fontweight="bold", va="top")
    w, gap, y, h = 3.28, 0.29, 4.35, 5.0
    for i, (name, func, evid) in enumerate(stages):
        x = 0.25 + i * (w + gap)
        header_box(ax, x, y, w, h, name, head_h=0.62, head_fill=head_colors[i])
        ax.text(x + 0.18, y + h - 0.85, wrap(func, w - 0.36, FS), fontsize=FS, va="top",
                linespacing=1.35)
        ev_fill = PALE if is_bw else ["#eff6ff", "#f0f9ff", "#ecfdf5", "#faf5ff"][i]
        box(ax, x + 0.15, y + 0.15, w - 0.3, 1.85, fill=ev_fill, radius=0.07)
        ax.text(x + 0.3, y + 1.82, "Evidencia necesaria", fontsize=FS_SMALL,
                fontweight="bold", va="top")
        ax.text(x + 0.3, y + 1.45, wrap(evid, w - 0.6, FS_SMALL), fontsize=FS_SMALL,
                va="top", style="italic", linespacing=1.3)
        if i < 3:
            arrow(ax, (x + w + 0.03, y + h / 2), (x + w + gap - 0.03, y + h / 2), ms=8, color=INK)
    ax.text(0.25, 3.98, "B. Audiencias y lo que necesitan de una explicación",
            fontsize=FS_HEAD, fontweight="bold", va="top")
    auds = [("Desarrollo", "reproducir y corregir el comportamiento"),
            ("Validación", "pruebas independientes y criterios de aceptación"),
            ("Profesional del dominio", "pertinencia, límites y margen para apartarse"),
            ("Dirección", "exposición al riesgo y controles"),
            ("Autoridad supervisora", "documentación verificable"),
            ("Persona afectada", "comunicación comprensible y vías reales de revisión")]
    cw, ch = 4.55, 1.5
    aud_fills = [WHITE] * 6 if is_bw else ["#eff6ff", "#f0f9ff", "#ecfdf5", "#fffbeb", "#fef2f2", "#faf5ff"]
    aud_fills[5] = LIGHT if is_bw else "#fef2f2"
    for i, (who, need) in enumerate(auds):
        cx = 0.25 + (i % 3) * (cw + 0.22)
        cy = 1.9 - (i // 3) * (ch + 0.18)
        box(ax, cx, cy, cw, ch, fill=aud_fills[i], radius=0.08)
        ax.text(cx + 0.2, cy + ch - 0.22, who, fontsize=FS, fontweight="bold", va="top")
        ax.text(cx + 0.2, cy + ch - 0.66, wrap(need, cw - 0.4, FS), fontsize=FS, va="top",
                linespacing=1.3)
    save(fig, "fig_d5_ciclo_audiencias_es", is_bw)


# ------------------------------------------------------------------------ D6
def d6_niveles(is_bw: bool = False) -> None:
    """Three levels of evaluation and where FOM-7 sits."""
    H = 8.6
    fig, ax = canvas(H)
    
    if is_bw:
        tiers = [
            ("Centrada en la aplicación", "Personas expertas en tareas reales.",
             "¿Mejora la explicación el desempeño en el contexto de uso?", WHITE, None, DARK),
            ("Centrada en humanos", "Personas en tareas simplificadas.",
             "¿Comprenden, anticipan o corrigen mejor las personas?", WHITE, None, DARK),
            ("Funcionalmente fundamentada", "Proxies computacionales, sin participantes.",
             "¿Qué propiedades medibles tiene el artefacto explicativo?", LIGHT, "////", DARK),
        ]
    else:
        tiers = [
            ("Centrada en la aplicación", "Personas expertas en tareas reales.",
             "¿Mejora la explicación el desempeño en el contexto de uso?", "#eff6ff", None, "#1e40af"),
            ("Centrada en humanos", "Personas en tareas simplificadas.",
             "¿Comprenden, anticipan o corrigen mejor las personas?", "#f0f9ff", None, "#0369a1"),
            ("Funcionalmente fundamentada", "Proxies computacionales, sin participantes.",
             "¿Qué propiedades medibles tiene el artefacto explicativo?", "#ecfdf5", None, "#047857"),
        ]

    x0, w = 2.2, 9.1
    for i, (name, who, q, fill, hatch, head_col) in enumerate(tiers):
        y = 6.0 - i * 2.55
        indent = (2 - i) * 0.55
        box(ax, x0 + indent, y, w - 2 * indent, 2.15, fill=fill, hatch=hatch,
            lw=1.4 if i == 2 else LW, edge=head_col if not is_bw else INK)
        box(ax, x0 + indent + 0.3, y + 0.25, w - 2 * indent - 0.6, 1.65, fill=WHITE,
            lw=0, radius=0.06)
        ax.text(x0 + w / 2, y + 1.65, name, ha="center", va="center", fontsize=FS_HEAD,
                fontweight="bold", color=head_col if not is_bw else INK)
        ax.text(x0 + w / 2, y + 1.12, who, ha="center", va="center", fontsize=FS)
        ax.text(x0 + w / 2, y + 0.58, q, ha="center", va="center", fontsize=FS,
                style="italic")
    # side arrows
    arrow(ax, (1.1, 1.0), (1.1, 8.1), lw=1.0)
    ax.text(0.75, 4.55, "más realismo y más coste", rotation=90, ha="center",
            va="center", fontsize=FS, style="italic")
    arrow(ax, (13.35, 8.1), (13.35, 1.0), lw=1.0)
    ax.text(13.7, 4.55, "más control, escala y reproducibilidad", rotation=90,
            ha="center", va="center", fontsize=FS, style="italic")
    # FOM-7 tag
    tag_fill = DARK if is_bw else "#047857"
    box(ax, 9.2, 0.15, 4.05, 0.62, fill=tag_fill)
    ax.text(11.22, 0.46, "Nivel de FOM-7 y del caso", ha="center", va="center",
            fontsize=FS, color=WHITE, fontweight="bold")
    arrow(ax, (9.2, 0.46), (8.75, 0.95), ms=7)
    note(ax, 2.3, 0.72, "Ningún nivel domina en todos los casos: cada uno responde "
         "preguntas distintas.", width=7.0)
    save(fig, "fig_d6_niveles_evaluacion_es", is_bw)


# ------------------------------------------------------------------------ D7
def d7_cadena(is_bw: bool = False) -> None:
    """The evidence chain from explanatory artifact to published claim."""
    H = 6.4
    fig, ax = canvas(H)
    
    link_heads = [INK] * 6 if is_bw else ["#1e40af", "#1d4ed8", "#0d9488", "#059669", "#d97706", "#7c3aed"]
    fail_bg = PALE if is_bw else "#fff1f2"
    
    links = [
        ("Artefacto", "salida del explicador", "salidas vacías, malformadas o no comparables"),
        ("Constructo", "propiedad que se quiere medir", "la métrica no mide lo que nombra"),
        ("Métrica", "operacionalización", "definiciones y parámetros que varían entre estudios"),
        ("Prueba", "inferencia estadística", "prueba incompatible con el diseño; pseudorreplicación"),
        ("Resultado", "valor observado", "variación de semilla confundida con un efecto"),
        ("Afirmación", "conclusión publicada", "alcance mayor que la evidencia"),
    ]
    n = len(links)
    w, gap = 2.14, 0.28
    x0 = (TEXT_W - (n * w + (n - 1) * gap)) / 2
    y, h = 4.3, 1.75
    for i, (name, what, fail) in enumerate(links):
        x = x0 + i * (w + gap)
        header_box(ax, x, y, w, h, name, head_h=0.58,
                   head_fill=link_heads[i])
        ax.text(x + w / 2, y + 0.6, wrap(what, w - 0.25, FS_SMALL), ha="center",
                va="center", fontsize=FS_SMALL, linespacing=1.25)
        if i < n - 1:
            arrow(ax, (x + w + 0.02, y + h / 2), (x + w + gap - 0.02, y + h / 2), ms=8)
        # failure
        ax.plot([x + w / 2, x + w / 2], [y, y - 0.45], color=MID, lw=0.7, ls=":")
        box(ax, x, 1.55, w, 2.25, fill=fail_bg, radius=0.07, edge="#be123c" if not is_bw else INK)
        ax.text(x + w / 2, 3.55, "Fallo típico", ha="center", va="top",
                fontsize=FS_SMALL, fontweight="bold", color="#9f1239" if not is_bw else INK)
        ax.text(x + w / 2, 3.15, wrap(fail, w - 0.25, FS_SMALL), ha="center", va="top",
                fontsize=FS_SMALL, style="italic", linespacing=1.28)
    note(ax, TEXT_W / 2, 1.2, "La crisis de evaluación aparece cuando se rompe algún "
         "eslabón: la cifra existe, pero la afirmación ya no está respaldada. FOM-7 "
         "controla cada eslabón antes de admitir una conclusión.", width=TEXT_W - 1.5,
         ha="center")
    save(fig, "fig_d7_cadena_evidencia_es", is_bw)


# ------------------------------------------------------------------------ D8
def d8_fom7_traza(is_bw: bool = False) -> None:
    """FOM-7's seven gates with one published claim traced through them."""
    gates = [
        ("1", "Congelación", "Diseño y plan inferencial congelados",
         "Diseño de 5 modelos, 4 métodos, 5 semillas y 3 tamaños de muestra fijado antes de ejecutar."),
        ("2", "Ejecución", "Resultados crudos por celda",
         "Las 300 celdas planificadas se ejecutan desde manifiestos con semillas fijas."),
        ("3", "Auditoría", "Inventario de celdas analizables",
         "Quedan 275 celdas calificadas; las faltantes se registran, no se reconstruyen."),
        ("4", "Armonización", "Métricas por ejecución y por bloque",
         "La fidelidad se agrega en 15 bloques de modelo por tamaño de muestra."),
        ("5", "Exportación", "Tablas inferenciales deterministas",
         "Prueba de Friedman sobre los 15 bloques, con ajuste de Holm."),
        ("6", "Perfilado", "Variación entre semillas (CV)",
         "Se separa la variación de semilla del efecto del método."),
        ("7", "Reporte", "Afirmación trazable y delimitada",
         "«Los métodos difieren en fidelidad», con prueba, fuente y alcance: Adult, "
         "datos tabulares, métricas declaradas."),
    ]
    
    gate_colors = [DARK] * 7 if is_bw else ["#1e40af", "#1d4ed8", "#0d9488", "#059669", "#d97706", "#e11d48", "#7c3aed"]
    gate_colors[6] = INK if is_bw else "#7c3aed"
    
    row_h, gap = 1.3, 0.22
    H = 1.3 + len(gates) * (row_h + gap) + 0.9
    fig, ax = canvas(H)
    top = H - 0.35
    cols = [(0.25, 3.6, "Puerta"), (4.15, 3.95, "Artefacto de salida"),
            (8.4, 5.85, "Traza de una afirmación publicada")]
    for x, w, t in cols:
        ax.text(x + 0.05, top, t, fontsize=FS_HEAD, fontweight="bold", va="top")
    ax.plot([0.25, TEXT_W - 0.25], [top - 0.5, top - 0.5], color=INK, lw=LW)
    for i, (num, name, art, trace) in enumerate(gates):
        y = top - 0.8 - (i + 1) * (row_h + gap) + gap
        box(ax, 0.25, y, 3.6, row_h, fill=gate_colors[i])
        ax.add_patch(Circle((0.85, y + row_h / 2), 0.36, facecolor=WHITE, edgecolor=WHITE,
                            zorder=3))
        ax.text(0.85, y + row_h / 2, num, ha="center", va="center", fontsize=9,
                fontweight="bold", zorder=4, color=gate_colors[i])
        ax.text(1.45, y + row_h / 2, name, va="center", fontsize=FS_HEAD, color=WHITE,
                fontweight="bold", zorder=4)
        box(ax, 4.15, y, 3.95, row_h, fill=PALE if is_bw else "#f8fafc")
        ax.text(4.35, y + row_h / 2, wrap(art, 3.6, FS), va="center", fontsize=FS,
                linespacing=1.3)
        box(ax, 8.4, y, 5.85, row_h, fill=WHITE if is_bw else ("#faf5ff" if i==6 else WHITE), lw=1.6 if i == 6 else LW, edge="#7c3aed" if (not is_bw and i==6) else INK)
        ax.text(8.6, y + row_h / 2, wrap(trace, 5.45, FS), va="center", fontsize=FS,
                linespacing=1.3)
        arrow(ax, (3.87, y + row_h / 2), (4.13, y + row_h / 2), ms=6, lw=0.7)
        arrow(ax, (8.12, y + row_h / 2), (8.38, y + row_h / 2), ms=6, lw=0.7)
        if i < len(gates) - 1:
            arrow(ax, (0.85, y), (0.85, y - gap + 0.01), ms=6, lw=0.8)
    note(ax, 0.25, 0.72, "Las puertas son secuenciales: si una falla, los resultados "
         "afectados se tratan como evidencia descriptiva y no sostienen afirmaciones "
         "inferenciales.", width=TEXT_W - 0.5)
    save(fig, "fig_d8_fom7_traza_es", is_bw)


FIGURES = {"d1": d1_conceptos, "d2": d2_modelos, "d3": d3_local_global,
           "d4": d4_objetos, "d5": d5_ciclo_audiencias, "d6": d6_niveles,
           "d7": d7_cadena, "d8": d8_fom7_traza}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", default=",".join(FIGURES))
    parser.add_argument("--mode", choices=["color", "bw", "both"], default="both")
    args = parser.parse_args()
    
    keys = [k.strip() for k in args.only.split(",")]
    modes = [False] if args.mode == "color" else ([True] if args.mode == "bw" else [False, True])
    
    for is_bw in modes:
        for key in keys:
            FIGURES[key](is_bw=is_bw)
            
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
