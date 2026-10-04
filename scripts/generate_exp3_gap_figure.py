#!/usr/bin/env python3
"""Regenerate the EXP3 cross-dataset figure as a gap-only plot.

2026-09-28 (review F02, author decision Q1): the figure now shows only the
paired SHAP - Anchors fidelity gap. The earlier version stacked the gap on the
Anchors level, so each bar reached the SHAP level that the published RIMI
article reports; gaps alone carry the argument without that. The Anchors
levels stay in tab:exp3_fidelity.

History of the figure before that change:

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

import argparse
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
    # Paper B (docs/reports/paper_b/figures) keeps its own copy of the figure:
    # pass --output-dir to write it there instead of the default.
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output-dir", type=Path, default=OUT_DIR)
    out_dir = parser.parse_args().output_dir.resolve()

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

    # Gap only: no bar reaches, or implies, a SHAP level.
    ax.bar(x, gaps, width=0.55, color="#4C72B0")
    for i, g in enumerate(gaps):
        ax.text(i, g + 0.012, f"+{g:.3f}", ha="center", va="bottom",
                color="#222222", fontsize=8)

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Fidelity gap, SHAP $-$ Anchors\n(3-seed average)")
    ax.set_xlabel("Dataset / model family")
    ax.set_ylim(0, 0.6)
    ax.axhline(0.0, color="#555555", linewidth=0.8)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    out_dir.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        out = out_dir / f"fig_exp3_gap.{ext}"
        fig.savefig(out, bbox_inches="tight")
        print("  wrote", out.relative_to(ROOT).as_posix())
    plt.close(fig)


if __name__ == "__main__":
    main()
