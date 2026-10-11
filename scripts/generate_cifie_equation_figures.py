#!/usr/bin/env python3
"""Generate didactic figures illustrating the mathematical equations of the CIFIE chapter.

Produces both:
1. Color version (default digital edition) stored under:
   publications/book_chapters/2026_cifie_xai_fom7/figures/exported/
   publications/book_chapters/2026_cifie_xai_fom7/figures/editable/
2. Black & White version (dedicated print edition) stored under:
   publications/book_chapters/2026_cifie_xai_fom7/figures/bw/

Figures generated:
- fig_d9_lime_geometria_es: Local tangent hyperplane, exponential kernel pi_x(z) and OOD risk.
- fig_d10_shap_coaliciones_es: Combinatorial coalition lattice, KernelSHAP U-curve, and additive waterfall.
- fig_d11_anchors_dice_es: Anchors PAC bounding box vs. DiCE multi-objective force balance & DPP diversity.
- fig_d12_fom7_metrologia_es: FOM-7 Gate 2 Lipschitz/Cosine stability ball vs. Gate 6 rank disagreement.

Usage: python scripts/generate_cifie_equation_figures.py [--mode color|bw|both]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Prevent loading incompatible user-site numpy packages on Windows
sys.path = [p for p in sys.path if "AppData" not in p or "Python" not in p]

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Rectangle, Ellipse
from matplotlib.lines import Line2D

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
    p = Path("C:/Windows/Fonts") / fname
    if p.exists():
        font_manager.fontManager.addfont(str(p))

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


# ==============================================================================
# FIGURE D9: LIME GEOMETRY & OOD PERTURBATIONS
# ==============================================================================
def generate_d9_lime_geometria(is_bw: bool = False) -> None:
    """Panel A: Local exponential kernel pi_x(z) and tangent surrogate g.
    Panel B: Independent feature perturbation throwing synthetic instances OOD.
    """
    H = 8.4
    fig = plt.figure(figsize=(TEXT_W / 2.54, H / 2.54))

    # Palette
    c_blue = "#1e40af" if not is_bw else INK
    c_teal = "#0f766e" if not is_bw else DARK
    c_rose = "#be123c" if not is_bw else DARK
    bg_box = "#f8fafc" if not is_bw else WHITE
    ood_color = "#dc2626" if not is_bw else INK

    # Panel A: Local tangent plane and exponential proximity kernel
    axa = fig.add_axes([0.085, 0.22, 0.40, 0.68])
    axa.set_title("A. Foco gaussiano $\\pi_x(z)$ y sustituto lineal $g(z)$", fontsize=FS_HEAD, fontweight="bold", pad=7)

    # Complex non-linear decision boundary
    x_grid = np.linspace(-3, 3, 200)
    y_boundary = 0.3 * np.sin(1.8 * x_grid) + 0.15 * x_grid**2 - 0.4
    axa.plot(x_grid, y_boundary, color=INK, lw=1.2, ls="--", label="Frontera de $f(x)$", zorder=3)

    # Query instance x
    qx, qy = 0.5, 0.3 * np.sin(1.8 * 0.5) + 0.15 * 0.5**2 - 0.05

    # Radial kernel contour levels
    radii = [0.4, 0.8, 1.3, 1.8]
    alphas = [0.25, 0.16, 0.09, 0.04] if not is_bw else [0.2, 0.12, 0.07, 0.03]
    k_fill = "#3b82f6" if not is_bw else LIGHT
    for r, a in zip(radii, alphas):
        circle = Circle((qx, qy), r, facecolor=k_fill, edgecolor=MID, alpha=a, lw=0.5, ls=":", zorder=1)
        axa.add_patch(circle)

    # Tangent linear surrogate g(z)
    slope = 0.3 * 1.8 * np.cos(1.8 * 0.5) + 0.3 * 0.5
    tx = np.linspace(qx - 1.4, qx + 1.4, 30)
    ty = qy + slope * (tx - qx)
    axa.plot(tx, ty, color=c_blue, lw=1.8, label="Sustituto $g(z)$", zorder=4)

    # Synthetic perturbations z with size and opacity scaled by pi_x(z)
    rng = np.random.default_rng(42)
    pz_x = rng.normal(qx, 0.75, 45)
    pz_y = rng.normal(qy, 0.75, 45)
    dists = np.sqrt((pz_x - qx)**2 + (pz_y - qy)**2)
    weights = np.exp(-(dists**2) / (0.9**2))

    # Scatter points colored by class above/below f(x)
    f_val = 0.3 * np.sin(1.8 * pz_x) + 0.15 * pz_x**2 - 0.4
    class_1 = pz_y > f_val
    for px, py, w, c1 in zip(pz_x, pz_y, weights, class_1):
        color = (c_teal if c1 else c_rose) if not is_bw else (DARK if c1 else LIGHT)
        size = 10 + 40 * w
        alpha = 0.3 + 0.7 * w
        marker = "o" if c1 else "^"
        axa.scatter(px, py, s=size, facecolor=color, edgecolor=INK, linewidth=0.4, alpha=alpha, zorder=2, marker=marker)

    # Highlight point x
    axa.scatter([qx], [qy], s=110, marker="*", facecolor="#fbbf24" if not is_bw else WHITE,
                edgecolor=INK, linewidth=1.2, zorder=6, label="Instancia evaluada $x$")

    axa.set_xlim(-2.2, 2.5)
    axa.set_ylim(-1.6, 2.2)
    axa.set_xlabel("Característica 1 ($z_1$)", fontsize=FS)
    axa.set_ylabel("Característica 2 ($z_2$)", fontsize=FS)
    axa.tick_params(labelsize=FS_SMALL)

    # Annotations
    axa.text(qx + 0.15, qy + 0.55, "$\\pi_x(z) \\approx 1.0$", fontsize=FS_SMALL, fontweight="bold", color=c_blue)
    axa.text(qx + 1.25, qy + 1.3, "$\\pi_x(z) \\to 0$", fontsize=FS_SMALL, style="italic", color=MID)

    # Panel B: Out-of-Distribution (OOD) perturbation phenomenon
    axb = fig.add_axes([0.565, 0.22, 0.40, 0.68])
    axb.set_title("B. Riesgo de perturbación fuera de distribución (OOD)", fontsize=FS_HEAD, fontweight="bold", pad=7)

    # Realistic correlated distribution (Age vs Education)
    mean = [35, 12]
    cov = [[60, 18], [18, 8]]
    data = rng.multivariate_normal(mean, cov, 180)
    axb.scatter(data[:, 0], data[:, 1], s=12, facecolor=MID, alpha=0.35, edgecolor="none", zorder=1, label="Distribución empírica")

    # In-distribution ellipse
    ell = Ellipse((35, 12), width=28, height=7.5, angle=22, facecolor="none", edgecolor=c_teal, lw=1.2, ls="--", zorder=2)
    axb.add_patch(ell)

    # Point x
    px0, py0 = 22, 9
    axb.scatter([px0], [py0], s=110, marker="*", facecolor="#fbbf24" if not is_bw else WHITE,
                edgecolor=INK, linewidth=1.2, zorder=5)

    # Independent perturbations (Cartesian box sampling)
    ood_pts = np.array([
        [18, 17],
        [19, 16],
        [20, 18],
        [50, 4]
    ])
    axb.scatter(ood_pts[:, 0], ood_pts[:, 1], s=45, marker="X", facecolor=ood_color,
                edgecolor=INK, linewidth=0.8, zorder=6, label="Muestra sintética OOD")

    in_pts = np.array([
        [23, 9.5],
        [21, 8.8],
        [24, 10.2]
    ])
    axb.scatter(in_pts[:, 0], in_pts[:, 1], s=25, marker="o", facecolor=c_teal if not is_bw else DARK,
                edgecolor=INK, linewidth=0.5, zorder=4)

    # Callout box for OOD
    axb.annotate("Violación lógica de correlación\n(`Edad=18`, `Años_Estudio=17`)",
                 xy=(18, 17), xytext=(24, 18.5),
                 arrowprops=dict(arrowstyle="->", color=ood_color, lw=0.9),
                 fontsize=FS_SMALL, color=ood_color, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.2", facecolor=bg_box, edgecolor=ood_color, lw=0.6))

    axb.set_xlim(12, 58)
    axb.set_ylim(2, 21)
    axb.set_xlabel("Edad (años)", fontsize=FS)
    axb.set_ylabel("Años de estudio completados", fontsize=FS)
    axb.tick_params(labelsize=FS_SMALL)

    # Custom legends at bottom
    leg_a = [
        Line2D([], [], color=INK, lw=1.2, ls="--", label="Frontera de $f(x)$"),
        Line2D([], [], color=c_blue, lw=1.8, label="Sustituto $g(z)$"),
        Line2D([], [], marker="*", color="#fbbf24" if not is_bw else INK, ls="none", markersize=9, label="Instancia $x$"),
        Line2D([], [], marker="X", color=ood_color, ls="none", markersize=7, label="Perturbación OOD")
    ]
    fig.legend(handles=leg_a, loc="lower center", bbox_to_anchor=(0.5, 0.02), ncol=4,
               frameon=False, fontsize=FS_SMALL, handletextpad=0.3, columnspacing=1.2)

    save(fig, "fig_d9_lime_geometria_es", is_bw)


# ==============================================================================
# FIGURE D10: SHAPLEY COALITION LATTICE & KERNELSHAP U-CURVE
# ==============================================================================
def generate_d10_shap_coaliciones(is_bw: bool = False) -> None:
    """Panel A: 3-feature Boolean coalition lattice & permutation paths.
    Panel B: KernelSHAP U-shaped combinatorial weight curve pi(z').
    Panel C: Shapley Additive Waterfall chart showing efficiency.
    """
    H = 8.6
    fig = plt.figure(figsize=(TEXT_W / 2.54, H / 2.54))

    c_blue = "#1e40af" if not is_bw else INK
    c_teal = "#0f766e" if not is_bw else DARK
    c_rose = "#be123c" if not is_bw else DARK

    # --- Panel A: 3-Feature Coalition Lattice
    axa = fig.add_axes([0.02, 0.16, 0.29, 0.74])
    axa.set_title("A. Retículo de coaliciones ($2^{|F|}$)", fontsize=FS_HEAD, fontweight="bold", pad=7)
    axa.axis("off")

    nodes = {
        "empty": (0.5, 0.08, "$\\emptyset$"),
        "x1": (0.16, 0.38, "$\\{x_1\\}$"),
        "x2": (0.50, 0.38, "$\\{x_2\\}$"),
        "x3": (0.84, 0.38, "$\\{x_3\\}$"),
        "x12": (0.16, 0.68, "$\\{x_1, x_2\\}$"),
        "x13": (0.50, 0.68, "$\\{x_1, x_3\\}$"),
        "x23": (0.84, 0.68, "$\\{x_2, x_3\\}$"),
        "all": (0.5, 0.94, "$\\{x_1, x_2, x_3\\}$"),
    }

    edges = [
        ("empty", "x1"), ("empty", "x2"), ("empty", "x3"),
        ("x1", "x12"), ("x1", "x13"),
        ("x2", "x12"), ("x2", "x23"),
        ("x3", "x13"), ("x3", "x23"),
        ("x12", "all"), ("x13", "all"), ("x23", "all")
    ]

    for u, v in edges:
        x0, y0, _ = nodes[u]
        x1, y1, _ = nodes[v]
        axa.plot([x0, x1], [y0, y1], color=LIGHT if not is_bw else MID, lw=0.9, zorder=1)

    path = [("empty", "x2"), ("x2", "x12"), ("x12", "all")]
    for u, v in path:
        x0, y0, _ = nodes[u]
        x1, y1, _ = nodes[v]
        axa.plot([x0, x1], [y0, y1], color=c_blue, lw=1.6, ls="-", zorder=2)

    for k, (nx, ny, lbl) in nodes.items():
        box_w, box_h = 0.22, 0.10
        fill = "#eff6ff" if not is_bw else WHITE
        edge = c_blue if (k in ["x2", "x12"]) else INK
        patch = FancyBboxPatch((nx - box_w/2, ny - box_h/2), box_w, box_h,
                               boxstyle="round,pad=0.02,rounding_size=0.03",
                               facecolor=fill, edgecolor=edge, lw=1.0, zorder=3)
        axa.add_patch(patch)
        axa.text(nx, ny, lbl, ha="center", va="center", fontsize=FS_SMALL, zorder=4, fontweight="bold")

    axa.text(0.5, 0.0, "Permutación marginal de $x_1$",
             ha="center", va="top", fontsize=6.2, style="italic", color=c_blue)

    # --- Panel B: KernelSHAP U-shaped Weight Curve
    axb = fig.add_axes([0.41, 0.22, 0.25, 0.68])
    axb.set_title("B. Núcleo $\\pi(z')$ en U", fontsize=FS_HEAD, fontweight="bold", pad=7)

    M = 10
    z_sizes = np.arange(1, M)
    from math import comb
    weights = [(M - 1) / (comb(M, z) * z * (M - z)) for z in z_sizes]

    if not is_bw:
        bar_c = [c_rose if (z in [1, M-1]) else c_teal for z in z_sizes]
    else:
        bar_c = [DARK if (z in [1, M-1]) else LIGHT for z in z_sizes]

    axb.plot(z_sizes, weights, color=INK, lw=1.0, ls="--", zorder=3)
    axb.scatter(z_sizes, weights, s=36, color=bar_c, edgecolor=INK, zorder=4)

    axb.set_xlabel("Tamaño de coalición $|z'|$", fontsize=FS)
    axb.set_ylabel("Ponderación $\\pi(z')$", fontsize=FS)
    axb.set_xticks(z_sizes)
    axb.set_ylim(-0.005, 0.115)
    axb.tick_params(labelsize=FS_SMALL)
    for s in ("top", "right"):
        axb.spines[s].set_visible(False)

    axb.text(1.3, 0.085, "Aislamiento\nsingular", fontsize=5.8, ha="left", color=c_rose if not is_bw else INK, fontweight="bold")
    axb.text(8.7, 0.085, "Efecto\ntotal", fontsize=5.8, ha="right", color=c_rose if not is_bw else INK, fontweight="bold")
    axb.text(5, 0.02, "Ponderación mínima\nen coaliciones intermedias", fontsize=5.8, ha="center", style="italic", color=MID)

    # --- Panel C: Additive Waterfall (Efficiency Axiom)
    axc = fig.add_axes([0.74, 0.22, 0.23, 0.68])
    axc.set_title("C. Cascada aditiva", fontsize=FS_HEAD, fontweight="bold", pad=7)

    steps = ["Base $\\mathbb{E}[f]$", "Puntaje", "Ingresos", "Deuda", "Salida $f$"]
    vals = [0.50, 0.22, 0.18, -0.05, 0.85]
    cumulative = [0.0, 0.50, 0.72, 0.90, 0.0]

    y_pos = np.arange(len(steps))[::-1]
    axc.barh(y_pos[0], vals[0], left=0.0, height=0.55, color=MID if is_bw else "#94a3b8", edgecolor=INK, lw=0.7)
    axc.barh(y_pos[1], vals[1], left=cumulative[1], height=0.55, color=DARK if is_bw else c_teal, edgecolor=INK, lw=0.7)
    axc.barh(y_pos[2], vals[2], left=cumulative[2], height=0.55, color=DARK if is_bw else c_teal, edgecolor=INK, lw=0.7)
    axc.barh(y_pos[3], abs(vals[3]), left=cumulative[3] + vals[3], height=0.55, color=LIGHT if is_bw else c_rose, edgecolor=INK, lw=0.7)
    axc.barh(y_pos[4], vals[4], left=0.0, height=0.55, color=DARK if is_bw else c_blue, edgecolor=INK, lw=1.1)

    axc.set_yticks(y_pos)
    axc.set_yticklabels(steps, fontsize=FS_SMALL)
    axc.set_xlim(0, 1.0)
    axc.set_xlabel("Probabilidad", fontsize=FS)
    axc.tick_params(labelsize=FS_SMALL)
    for s in ("top", "right"):
        axc.spines[s].set_visible(False)

    axc.text(0.5, 4.4, "$\\sum \\phi_i = f(x) - \\mathbb{E}[f]$", ha="center", fontsize=6.4,
             fontweight="bold", color=c_blue)

    save(fig, "fig_d10_shap_coaliciones_es", is_bw)


# ==============================================================================
# FIGURE D11: ANCHORS INVARIANCE BOX & DICE FORCE BALANCE
# ==============================================================================
def generate_d11_anchors_dice(is_bw: bool = False) -> None:
    """Panel A: Anchors axis-aligned bounding box and PAC certainty region.
    Panel B: DiCE multi-objective physics (boundary crossing, proximity, DPP repulsion).
    """
    H = 8.4
    fig = plt.figure(figsize=(TEXT_W / 2.54, H / 2.54))

    c_blue = "#1e40af" if not is_bw else INK
    c_teal = "#0f766e" if not is_bw else DARK
    c_amber = "#b45309" if not is_bw else MID
    c_rose = "#be123c" if not is_bw else DARK

    # Panel A: Anchors Invariance Hyper-Rectangle
    axa = fig.add_axes([0.085, 0.22, 0.40, 0.68])
    axa.set_title("A. Anchors: Hiper-rectángulo de invarianza PAC", fontsize=FS_HEAD, fontweight="bold", pad=7)

    rng = np.random.default_rng(101)
    ages = rng.uniform(18, 65, 120)
    hours = rng.uniform(20, 60, 120)

    in_box = (ages > 35) & (hours <= 40)
    pred_1 = in_box.copy()
    noise_idx = rng.choice(np.where(in_box)[0], size=1)
    pred_1[noise_idx] = False
    pred_1[~in_box] = (ages[~in_box] > 50) | (hours[~in_box] > 48)

    c1_color = c_teal if not is_bw else DARK
    c0_color = c_rose if not is_bw else LIGHT
    axa.scatter(ages[~in_box & pred_1], hours[~in_box & pred_1], s=14, marker="o", facecolor=c1_color, alpha=0.35, edgecolor="none")
    axa.scatter(ages[~in_box & ~pred_1], hours[~in_box & ~pred_1], s=14, marker="^", facecolor=c0_color, alpha=0.35, edgecolor="none")

    # Anchor Box
    rect = Rectangle((35, 20), 30, 20, facecolor="#ecfdf5" if not is_bw else LIGHT,
                     edgecolor=c_teal if not is_bw else INK, lw=1.6, ls="-", alpha=0.5 if not is_bw else 0.3, zorder=2)
    axa.add_patch(rect)

    axa.scatter(ages[in_box & pred_1], hours[in_box & pred_1], s=26, marker="o", facecolor=c1_color, edgecolor=INK, lw=0.6, zorder=3)
    axa.scatter(ages[in_box & ~pred_1], hours[in_box & ~pred_1], s=26, marker="^", facecolor=c0_color, edgecolor=INK, lw=0.6, zorder=3)

    qx, qy = 45, 32
    axa.scatter([qx], [qy], s=110, marker="*", facecolor="#fbbf24" if not is_bw else WHITE, edgecolor=INK, lw=1.2, zorder=5)

    axa.set_xlim(16, 67)
    axa.set_ylim(18, 63)
    axa.set_xlabel("Edad (años)", fontsize=FS)
    axa.set_ylabel("Horas trabajadas por semana", fontsize=FS)
    axa.tick_params(labelsize=FS_SMALL)

    # Box title banner
    axa.text(50, 42.5, r"Regla $A$: $(\text{Edad} > 35 \ \text{y}\ \text{Horas} \leq 40)$", fontsize=6.4,
             fontweight="bold", color=c_teal if not is_bw else INK, ha="center",
             bbox=dict(boxstyle="round,pad=0.2", facecolor=WHITE, edgecolor=c_teal if not is_bw else INK, lw=0.7))

    axa.text(50, 22.5, "Precisión $\\text{prec}(A) = 97.4\\%$\nCobertura $\\text{cov}(A) = 22.5\\%$",
             fontsize=6.0, ha="center", style="italic", color=DARK,
             bbox=dict(boxstyle="round,pad=0.2", facecolor=WHITE, edgecolor="none", alpha=0.85))

    # Panel B: DiCE Multi-Objective Force Physics
    axb = fig.add_axes([0.565, 0.22, 0.40, 0.68])
    axb.set_title("B. DiCE: Balance de fuerzas y diversidad DPP", fontsize=FS_HEAD, fontweight="bold", pad=7)

    axb.axvline(0.0, color=INK, lw=1.4, ls="--", zorder=2)
    axb.text(-0.06, 1.85, "Frontera de decisión\n($y^*=1$)", ha="right", va="top", fontsize=FS_SMALL, color=DARK, fontweight="bold")

    x0, y0 = -1.1, 0.0
    axb.scatter([x0], [y0], s=120, marker="*", facecolor="#fbbf24" if not is_bw else WHITE, edgecolor=INK, lw=1.2, zorder=5)
    axb.text(x0, y0 - 0.28, "Instancia $x$\n(Denegado)", ha="center", va="top", fontsize=FS_SMALL, fontweight="bold")

    cf_pts = [
        (0.5, 1.1, "$c_1$ (Ingresos)"),
        (0.4, -0.9, "$c_2$ (Deuda)"),
        (0.9, 0.1, "$c_3$ (Mixto)")
    ]

    for cx, cy, lbl in cf_pts:
        axb.scatter([cx], [cy], s=60, marker="D", facecolor=c_blue if not is_bw else DARK, edgecolor=INK, lw=0.8, zorder=5)
        axb.text(cx + 0.12, cy, lbl, va="center", fontsize=6.2, fontweight="bold", color=c_blue if not is_bw else INK)

        dx, dy = x0 - cx, y0 - cy
        norm = np.sqrt(dx**2 + dy**2)
        axb.annotate("", xy=(cx + 0.38 * dx / norm, cy + 0.38 * dy / norm), xytext=(cx, cy),
                     arrowprops=dict(arrowstyle="->", color=c_amber if not is_bw else MID, lw=1.2))

        axb.annotate("", xy=(cx + 0.30, cy), xytext=(cx, cy),
                     arrowprops=dict(arrowstyle="->", color=c_teal if not is_bw else DARK, lw=1.2))

    axb.annotate("", xy=(0.45, 0.35), xytext=(0.45, 0.8),
                 arrowprops=dict(arrowstyle="<->", color=c_rose if not is_bw else INK, lw=1.1, ls=":"))
    axb.text(0.52, 0.60, "Repulsión DPP\n$\\det(\\mathbf{K})$", fontsize=5.8, color=c_rose if not is_bw else INK, style="italic")

    axb.plot([-1.8, 1.8], [-1.5, -1.5], color=c_rose if not is_bw else INK, lw=1.6, ls="-")
    axb.text(0.0, -1.72, "Barrera de inmutabilidad (variables congeladas)", ha="center", fontsize=5.8, color=c_rose if not is_bw else INK, fontweight="bold")

    axb.set_xlim(-1.7, 1.7)
    axb.set_ylim(-1.9, 1.9)
    axb.set_xticks([])
    axb.set_yticks([])
    axb.set_xlabel("Espacio de optimización de variables", fontsize=FS)
    for s in axb.spines.values():
        s.set_linewidth(LW)

    leg = [
        Line2D([], [], marker="*", color="#fbbf24" if not is_bw else INK, ls="none", markersize=9, label="Instancia $x$"),
        Line2D([], [], marker="D", color=c_blue if not is_bw else DARK, ls="none", markersize=6, label="Contrafactual $c_i$"),
        Line2D([], [], color=c_amber if not is_bw else MID, lw=1.2, label="Proximidad ($\\lambda_1$)"),
        Line2D([], [], color=c_rose if not is_bw else INK, lw=1.1, ls=":", label="Diversidad DPP ($\\det\\mathbf{K}$)")
    ]
    fig.legend(handles=leg, loc="lower center", bbox_to_anchor=(0.5, 0.02), ncol=4,
               frameon=False, fontsize=FS_SMALL, handletextpad=0.3, columnspacing=1.2)

    save(fig, "fig_d11_anchors_dice_es", is_bw)


# ==============================================================================
# FIGURE D12: FOM-7 GEOMETRIC METRICS (STABILITY & CONSISTENCY)
# ==============================================================================
def generate_d12_fom7_metrologia(is_bw: bool = False) -> None:
    """Panel A: Gate 2 Lipschitz sphere vs. operational cosine angular shift.
    Panel B: Gate 6 Cross-explainer Spearman rank crossing (disagreement paradox).
    """
    H = 8.4
    fig = plt.figure(figsize=(TEXT_W / 2.54, H / 2.54))

    c_blue = "#1e40af" if not is_bw else INK
    c_teal = "#0f766e" if not is_bw else DARK
    c_amber = "#b45309" if not is_bw else MID
    c_rose = "#be123c" if not is_bw else DARK

    # --- Panel A: Lipschitz Sphere & Cosine Stability
    axa = fig.add_axes([0.04, 0.18, 0.42, 0.72])
    axa.set_title("A. Estabilidad G2: Bola de perturbación $\\epsilon$", fontsize=FS_HEAD, fontweight="bold", pad=7)

    circ = Circle((0, 0), 1.0, facecolor="#f8fafc" if not is_bw else WHITE, edgecolor=INK, lw=1.2, ls="--", zorder=1)
    axa.add_patch(circ)
    axa.scatter([0], [0], s=80, marker="o", facecolor=INK, zorder=5)
    axa.text(0, -0.16, "$x$", ha="center", fontsize=FS_HEAD, fontweight="bold")

    axa.annotate("", xy=(0.8, 0.8), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", color=INK, lw=2.0))
    axa.text(0.85, 0.85, "$E(x)$", fontsize=FS_HEAD, fontweight="bold")

    theta_stable = np.radians([42, 47, 44])
    for th in theta_stable:
        vx, vy = 0.75 * np.cos(th), 0.75 * np.sin(th)
        axa.annotate("", xy=(vx, vy), xytext=(0, 0),
                     arrowprops=dict(arrowstyle="->", color=c_teal if not is_bw else DARK, lw=1.2, ls="-"))

    theta_unstable = np.radians([115, -20, 160])
    for th in theta_unstable:
        vx, vy = 0.70 * np.cos(th), 0.70 * np.sin(th)
        axa.annotate("", xy=(vx, vy), xytext=(0, 0),
                     arrowprops=dict(arrowstyle="->", color=c_rose if not is_bw else MID, lw=1.1, ls=":"))

    axa.set_xlim(-1.4, 1.4)
    axa.set_ylim(-1.4, 1.4)
    axa.set_xticks([])
    axa.set_yticks([])
    axa.axis("off")

    axa.text(0.45, 0.12, "KernelSHAP\n$\\cos \\theta \\geq 0.95$\n(Robusto)", fontsize=6.0, color=c_teal if not is_bw else DARK, fontweight="bold")
    axa.text(-1.25, 0.55, "LIME estocástico\n$\\cos \\theta < 0.75$\n(Volátil)", fontsize=6.0, color=c_rose if not is_bw else INK, fontweight="bold")
    axa.text(0, -1.22, "Radio de ruido $\\Vert x - x' \\Vert_2 \\leq \\epsilon$", ha="center", fontsize=6.2, style="italic", color=MID)

    # --- Panel B: Gate 6 Cross-Explainer Rank Disagreement (Bumps Chart)
    axb = fig.add_axes([0.53, 0.22, 0.44, 0.68])
    axb.set_title("B. Consistencia G6: Cruce de rangos inter-método", fontsize=FS_HEAD, fontweight="bold", pad=7)

    features = ["Edad", "Educación", "Horas", "Ganancia_Cap", "Estado_Civil"]
    rank_lime = [1, 2, 3, 4, 5]
    rank_shap = [4, 1, 5, 2, 3]

    colors_feat = [c_blue, c_teal, c_amber, c_rose, "#7c3aed"] if not is_bw else [INK, DARK, MID, DARK, INK]
    styles_feat = ["-", "-", "--", "-.", ":"]

    for r_l, r_s, col, ls, feat in zip(rank_lime, rank_shap, colors_feat, styles_feat, features):
        axb.plot([0, 1], [r_l, r_s], color=col, lw=1.6, ls=ls, marker="o", markersize=6, zorder=3)
        axb.text(-0.06, r_l, f"{feat} (#{r_l})", ha="right", va="center", fontsize=6.4)
        axb.text(1.06, r_s, f"{feat} (#{r_s})", ha="left", va="center", fontsize=6.4)

    axb.set_xlim(-0.65, 1.65)
    axb.set_ylim(6.3, 0.3)
    axb.set_xticks([0, 1])
    axb.set_xticklabels(["LIME ($E_1$)", "SHAP ($E_2$)"], fontsize=FS, fontweight="bold")
    axb.set_yticks([])
    for s in axb.spines.values():
        s.set_visible(False)

    axb.text(0.5, 5.85, "Divergencia de Spearman: $d_i = \\text{rango}(E_1)_i - \\text{rango}(E_2)_i$\n$\\text{Consistencia} = +0.10$ (desacuerdo crítico)",
             ha="center", fontsize=5.8, style="italic", color=c_rose if not is_bw else INK,
             bbox=dict(boxstyle="round,pad=0.2", facecolor="#fff1f2" if not is_bw else WHITE, edgecolor=c_rose if not is_bw else INK, lw=0.6))

    save(fig, "fig_d12_fom7_metrologia_es", is_bw)


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--mode", choices=["color", "bw", "both"], default="both")
    args = parser.parse_args()

    modes = [False] if args.mode == "color" else ([True] if args.mode == "bw" else [False, True])

    for is_bw in modes:
        generate_d9_lime_geometria(is_bw=is_bw)
        generate_d10_shap_coaliciones(is_bw=is_bw)
        generate_d11_anchors_dice(is_bw=is_bw)
        generate_d12_fom7_metrologia(is_bw=is_bw)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
