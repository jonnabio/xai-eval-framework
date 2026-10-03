#!/usr/bin/env python3
"""Paper D figures, from outputs/analysis/paper_d/ (scripts/pubs/paper_d_analysis.py).

Writes docs/reports/paper_d/figures/fig{1,2,3}.{pdf,png,tiff}. Tecnologia en Marcha asks for
images at 300 ppi, also uploaded as separate .tiff/.jpg files; captions live in the
manuscript, so no figure carries an in-image title.
"""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "outputs" / "analysis" / "paper_d"
OUT = ROOT / "docs" / "reports" / "paper_d" / "figures"
METHODS = ["shap", "lime", "anchors", "dice"]
LABEL = {"shap": "SHAP", "lime": "LIME", "anchors": "Anchors", "dice": "DiCE"}
METRICS = ["fidelity", "stability", "faithfulness_gap"]
MLABEL = {"fidelity": "Fidelity", "stability": "Stability", "faithfulness_gap": "Faithfulness gap"}
FAMILIES = ["logreg", "rf", "xgb", "svm", "mlp"]
FLABEL = {"logreg": "LR", "rf": "RF", "xgb": "XGB", "svm": "SVM", "mlp": "MLP"}

plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
                     "font.size": 9, "axes.linewidth": 0.6})


def table(name: str) -> dict[str, float]:
    with open(SRC / f"{name}.csv", encoding="utf-8") as fh:
        return {r["metric"]: float(r["value"]) for r in csv.DictReader(fh)}


def save(fig, stem: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.tiff", dpi=300, bbox_inches="tight",
                pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)


def fig1() -> None:
    """RQ1: mean per-run delta (misclassified - correct) with 95% CI."""
    t = table("rq1")
    fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.2), sharey=True)
    y = np.arange(len(METHODS))[::-1]
    for ax, k in zip(axes, METRICS):
        for yi, m in zip(y, METHODS):
            mean, lo, hi = t[f"{m}.{k}.mean"], t[f"{m}.{k}.ci_lo"], t[f"{m}.{k}.ci_hi"]
            sig = t[f"{m}.{k}.p_holm"] < 0.05
            ax.errorbar(mean, yi, xerr=[[mean - lo], [hi - mean]], fmt="o",
                        color="black" if sig else "0.6", mfc="black" if sig else "white",
                        ms=4, capsize=2, lw=0.9)
        ax.axvline(0, color="0.4", lw=0.6, ls="--")
        ax.set_xlabel(f"Δ {MLABEL[k].lower()}")
        ax.grid(axis="x", color="0.9", lw=0.5)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels([LABEL[m] for m in METHODS])
    fig.tight_layout()
    save(fig, "fig1")


def fig2() -> None:
    """RQ2: median per-run delta by model family."""
    t = table("rq2")
    fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.3), sharey=True)
    for ax, k in zip(axes, METRICS):
        grid = np.full((len(METHODS), len(FAMILIES)), np.nan)
        for i, m in enumerate(METHODS):
            for j, f in enumerate(FAMILIES):
                grid[i, j] = t.get(f"{m}.{k}.{f}.median", np.nan)
        lim = np.nanmax(np.abs(grid))
        ax.imshow(grid, cmap="RdBu", vmin=-lim, vmax=lim, aspect="auto")
        for i in range(len(METHODS)):
            for j in range(len(FAMILIES)):
                v = grid[i, j]
                if np.isfinite(v):
                    ax.text(j, i, f"{v:+.2f}", ha="center", va="center", fontsize=7,
                            color="white" if abs(v) > 0.6 * lim else "black")
        ax.set_xticks(range(len(FAMILIES)))
        ax.set_xticklabels([FLABEL[f] for f in FAMILIES])
        ax.set_xlabel(MLABEL[k])
    axes[0].set_yticks(range(len(METHODS)))
    axes[0].set_yticklabels([LABEL[m] for m in METHODS])
    fig.tight_layout()
    save(fig, "fig2")


def fig3() -> None:
    """RQ4: mean stability by prediction margin, correct vs misclassified."""
    t = table("fig_margin")
    centres = np.linspace(0.025, 0.475, 10)
    fig, axes = plt.subplots(1, 4, figsize=(6.5, 2.1))
    for ax, m in zip(axes, METHODS):
        for lab, style in (("cor", dict(color="black", marker="o")),
                           ("mis", dict(color="0.55", marker="s", ls="--"))):
            ys = [t.get(f"{m}.stability.{lab}.b{b}", np.nan) for b in range(10)]
            ax.plot(centres, ys, ms=3, lw=0.9, mfc="white", **style,
                    label="Correct" if lab == "cor" else "Misclassified")
        ax.set_xlabel("Margin |p̂ − 0.5|")
        ax.text(0.03, 0.95, LABEL[m], transform=ax.transAxes, va="top", fontweight="bold")
        ax.grid(color="0.9", lw=0.5)
    axes[0].set_ylabel("Mean stability")
    axes[0].legend(frameon=False, fontsize=7, loc="lower right")
    fig.tight_layout()
    save(fig, "fig3")


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    print(f"wrote {OUT}")
