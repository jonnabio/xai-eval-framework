#!/usr/bin/env python3
"""Paper F: the result tables and the figure of the manuscript, from the analysis files.

    python scripts/paper_f_report.py [--results DIR] [--out DIR]

Reads outputs/analysis/paper_f/results/ (written by scripts/paper_f_analyze.py) and writes,
to docs/reports/paper_f/:

    generated/tab_primary.tex   mean rank of each method per measure, the agreement between
                                datasets, its interval, the corrected p, the ceiling
    generated/tab_adult.tex     for each pair of methods, the share of the other datasets
                                where the pair is ordered as on Adult
    figures/fig1.pdf, .png      rank of each method on each dataset, one panel per measure

It computes nothing new: every number is read from a result file. Written and tested on
synthetic rows on 2026-10-05, before any result of the run existed.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_f_lib as lib  # noqa: E402

PAPER = lib.ROOT / "docs" / "reports" / "paper_f"
MEASURES = [("gap", "Faithfulness gap"), ("stability", "Stability"),
            ("sparsity", "Sparsity"), ("cost_ms", "Cost")]
METHODS = [("lime", "LIME"), ("shap", "SHAP"), ("anchors", "Anchors"), ("dice", "DiCE")]
NAME = dict(METHODS)
# One marker and one line style per method, so the figure reads without colour.
STYLE = {"lime": ("o", "-", "#1b6ca8"), "shap": ("s", "--", "#c0392b"),
         "anchors": ("^", "-.", "#2e8b57"), "dice": ("D", ":", "#6c3483")}


def signed(v: float, decimals: int = 2) -> str:
    text = f"{abs(v):.{decimals}f}"
    return f"$-${text}" if v < 0 and float(text) != 0 else text


def p_value(p: float) -> str:
    return "$<$0.001" if p < 0.001 else f"{p:.3f}"


def primary_table(results: Path) -> str:
    t = pd.read_csv(results / "primary.csv").set_index("measure")
    lines = [r"\begin{table*}[t]", r"\centering",
             r"\caption{Mean rank of each method over the datasets (1 = best) and agreement of "
             r"the rankings between datasets: mean rank correlation $\bar{\rho}$, its 95\% "
             r"bootstrap interval, the Holm-corrected permutation $p$, and the ceiling given by "
             r"the agreement between seeds inside a dataset.}",
             r"\label{tab:primary}", r"\small",
             r"\begin{tabular}{@{}lrrrrrcrr@{}}", r"\toprule",
             "Measure & " + " & ".join(n for _, n in METHODS)
             + r" & $\bar{\rho}$ & 95\% interval & $p$ & Ceiling \\", r"\midrule"]
    for key, label in MEASURES:
        r = t.loc[key]
        ranks = " & ".join(f"{r[f'mean_rank_{m}']:.2f}" for m, _ in METHODS)
        lines.append(f"{label} & {ranks} & {signed(r['mean_rank_corr'])} & "
                     f"{signed(r['ci_low'])} to {signed(r['ci_high'])} & {p_value(r['p_holm'])} & "
                     f"{signed(r['ceiling_seeds'])} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    return "\n".join(lines)


def adult_table(results: Path) -> str:
    t = pd.read_csv(results / "pairs_vs_adult.csv")
    n = int(t["datasets"].iloc[0])
    wide = t.pivot(index="pair", columns="measure", values="same_order")
    order = [f"{a} vs {b}" for i, (a, _) in enumerate(METHODS) for b, _ in METHODS[i + 1:]]
    lines = [r"\begin{table}[t]", r"\centering",
             rf"\caption{{Number of the {n} other datasets in which a pair of methods is in "
             r"the same order as on Adult, by measure.}", r"\label{tab:adult}", r"\small",
             r"\begin{tabular}{@{}lrrrr@{}}", r"\toprule",
             r"Pair & Faith. & Stab. & Spars. & Cost \\", r"\midrule"]
    for pair in order:
        a, b = pair.split(" vs ")
        cells = " & ".join(str(int(wide.loc[pair, m])) for m, _ in MEASURES)
        lines.append(f"{NAME[a]}--{NAME[b]} & {cells} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    return "\n".join(lines)


def figure(results: Path, out: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ranks = pd.read_csv(results / "ranks.csv")
    # Datasets in one fixed order for the four panels: Adult first, then by name.
    names = sorted(ranks["dataset"].unique(), key=lambda d: (d != "adult", d))
    fig, axes = plt.subplots(4, 1, figsize=(7.0, 6.6), sharex=True)
    for ax, (key, label) in zip(axes, MEASURES):
        part = ranks[ranks["measure"] == key].set_index("dataset").loc[names]
        for m, shown in METHODS:
            marker, line, colour = STYLE[m]
            ax.plot(range(len(names)), part[m], marker=marker, linestyle=line, color=colour,
                    linewidth=1.0, markersize=4, label=shown)
        ax.set_ylim(4.4, 0.6)
        ax.set_yticks([1, 2, 3, 4])
        ax.set_ylabel("Rank", fontsize=8)
        ax.set_title(label, fontsize=9, loc="left", pad=2)
        ax.tick_params(labelsize=7)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    axes[-1].set_xticks(range(len(names)))
    axes[-1].set_xticklabels(names, rotation=45, ha="right", fontsize=7)
    axes[0].legend(ncol=4, fontsize=7, frameon=False, loc="lower right", bbox_to_anchor=(1, 1.02))
    fig.tight_layout(h_pad=0.6)
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "fig1.pdf", metadata={"CreationDate": None})
    fig.savefig(out / "fig1.png", dpi=300)
    plt.close(fig)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--results", default=str(lib.OUT / "results"))
    ap.add_argument("--out", default=str(PAPER))
    args = ap.parse_args()
    results, out = Path(args.results), Path(args.out)
    (out / "generated").mkdir(parents=True, exist_ok=True)
    (out / "generated" / "tab_primary.tex").write_text(primary_table(results), encoding="utf-8",
                                                       newline="\n")
    (out / "generated" / "tab_adult.tex").write_text(adult_table(results), encoding="utf-8",
                                                     newline="\n")
    figure(results, out / "figures")
    print("written:", out / "generated" / "tab_primary.tex", out / "generated" / "tab_adult.tex",
          out / "figures" / "fig1.pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
