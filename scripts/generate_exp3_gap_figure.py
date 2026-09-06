#!/usr/bin/env python3
"""Regenerate the EXP3 cross-dataset figure as an Anchors-and-gap plot.

The figure this replaces plotted SHAP and Anchors fidelity levels side by
side. Two problems with that, both found on 2026-09-06:

1. The SHAP levels are reported in the published RIMI article, so a figure
   showing them re-reported results TMLR's editorial policy asks not to be
   reused. The table beside it was already converted to Anchors levels plus
   the SHAP-Anchors gap; the figure has to follow or the removal is cosmetic.

2. Its Breast Cancer / XGB bar was labelled 0.607 -- the April side-branch
   snapshot retired in August 2026 in favour of the canonical July value
   0.617, and registered as retired value A03.exp3.bc_xgb.april. It survived
   because scripts/pubs/verify_claims.py scans manuscript text, and a number
   baked into an embedded figure PDF is invisible to it.

No generator for the original figure was ever committed, which is why the
stale label could not be corrected by re-running anything. This script is that
generator.

    python scripts/generate_exp3_gap_figure.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "pubs"))
from claim_sources import resolve  # noqa: E402

OUT_DIR = ROOT / "docs" / "reports" / "paper_bc" / "figures"

CELLS = [
    ("breast_cancer", "rf", "BC / RF"),
    ("breast_cancer", "xgb", "BC / XGB"),
    ("german_credit", "rf", "GC / RF"),
    ("german_credit", "xgb", "GC / XGB"),
]


def main() -> None:
    labels, anchors, gaps = [], [], []
    for dataset, model, label in CELLS:
        a = resolve(f"exp3_anchors:{dataset}:{model}:fidelity")
        s = resolve(f"exp3_shap:{dataset}:{model}:fidelity")
        labels.append(label)
        anchors.append(a)
        gaps.append(s - a)
        print(f"  {label:9s} anchors={a:.3f}  gap={s - a:+.3f}")

    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "savefig.dpi": 300,
        }
    )
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    x = range(len(labels))

    # Anchors is the measured level; the gap is stacked on top of it, so the
    # bar height is the SHAP level without the SHAP level being labelled.
    ax.bar(x, anchors, width=0.55, label="Anchors fidelity", color="#4C72B0")
    ax.bar(x, gaps, width=0.55, bottom=anchors,
           label="Gap (SHAP $-$ Anchors)", color="#C7CBD1")

    for i, (a, g) in enumerate(zip(anchors, gaps)):
        ax.text(i, a / 2, f"{a:.3f}", ha="center", va="center",
                color="white", fontsize=8)
        ax.text(i, a + g / 2, f"+{g:.3f}", ha="center", va="center",
                color="#222222", fontsize=8)

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Mean fidelity (3-seed average)")
    ax.set_xlabel("Dataset / model family")
    ax.set_ylim(0, 1.0)
    ax.legend(frameon=False, ncol=2, loc="upper center",
              bbox_to_anchor=(0.5, 1.18))
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        out = OUT_DIR / f"fig_exp3_gap.{ext}"
        fig.savefig(out, bbox_inches="tight")
        print("  wrote", out.relative_to(ROOT).as_posix())
    plt.close(fig)


if __name__ == "__main__":
    main()
