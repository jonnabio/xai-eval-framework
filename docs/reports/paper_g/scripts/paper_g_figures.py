#!/usr/bin/env python3
"""Paper G: the manuscript's figures, drawn from the committed result files only.

Reads outputs/analysis/paper_g/ (original analysis, S1, S3 and exploratory diagnostics; read
only) and writes docs/reports/paper_g/figures/<name>.png (600 dpi, as the journal asks for
charts) and <name>.svg. No value is computed here beyond selecting and arranging the stored
summaries; the numbers the text prints are rendered by build_paper_g.py from the same files.

    ~/xai-eval-framework/.venv/bin/python docs/reports/paper_g/scripts/paper_g_figures.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
RES = ROOT / "outputs" / "analysis" / "paper_g"
S1 = RES / "supplementary" / "s1" / "analysis"
OUT = Path(__file__).resolve().parents[1] / "figures"

METRICS = ["m1_deletion", "m2_insertion", "m3_gap", "m4_corr", "m5_infidelity",
           "m6_sufficiency", "m7_roar"]
LABEL = {"m1_deletion": "M1", "m2_insertion": "M2", "m3_gap": "M3", "m4_corr": "M4",
         "m5_infidelity": "M5", "m6_sufficiency": "M6", "m7_roar": "M7"}
DATASETS = ["magic_telescope", "phoneme", "qsar_biodeg",   # numeric
            "adult", "bank_marketing", "compas", "electricity", "german_credit"]  # mixed
# Okabe-Ito palette (colour-blind safe).
C = {"original": "#0072B2", "S1-B": "#D55E00", "S1-M": "#009E73", "grey": "#999999",
     "r1": "#009E73", "r2": "#56B4E9", "r3": "#E69F00", "tied": "#BBBBBB"}

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 8.5,
                     "axes.labelsize": 8, "legend.fontsize": 7, "xtick.labelsize": 7,
                     "ytick.labelsize": 7, "axes.spines.top": False,
                     "axes.spines.right": False, "svg.hashsalt": "paper_g",
                     "svg.fonttype": "none"})


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.png", dpi=600, bbox_inches="tight",
                metadata={"Software": None})
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)
    print(f"wrote figures/{name}.png and .svg")


def fig_agreement_datasets() -> None:
    """System-level (H1-form) agreement per dataset: original, S1-B and S1-M."""
    df = pd.read_csv(S1 / "comparison_by_dataset.csv").set_index("dataset").loc[DATASETS]
    stab = pd.read_csv(RES / "analysis" / "confirmatory" / "stability_datasets.csv"
                       ).set_index("dataset").loc[DATASETS, "mean"]
    fig, ax = plt.subplots(figsize=(6.5, 2.8))
    x = np.arange(len(DATASETS))
    ax.bar(x, stab.values, width=0.75, color="#EEEEEE", edgecolor="none",
           label="Within-metric stability (original)")
    for k, (cond, dx, marker) in enumerate([("original", -0.18, "o"), ("S1-B", 0.0, "s"),
                                            ("S1-M", 0.18, "^")]):
        ax.scatter(x + dx, df[cond], color=C[cond], marker=marker, s=22, zorder=3,
                   label={"original": "Original (LIME slopes)",
                          "S1-B": "S1-B (LIME contributions, baseline reference)",
                          "S1-M": "S1-M (LIME contributions, mean reference)"}[cond])
    for i in x:
        ax.plot([i - 0.18, i], [df["original"].iloc[i], df["S1-B"].iloc[i]],
                color=C["grey"], lw=0.6, zorder=2)
    ax.axhline(0.5, color="black", lw=0.6, ls="--")
    ax.axvline(2.5, color=C["grey"], lw=0.6, ls=":")
    ax.text(1.0, 1.04, "numeric", ha="center", fontsize=7, color="#555555")
    ax.text(5.0, 1.04, "mixed", ha="center", fontsize=7, color="#555555")
    ax.set_xticks(x, [d.replace("_", " ") for d in DATASETS], rotation=25, ha="right")
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Mean pairwise Spearman\nbetween metrics")
    ax.legend(loc="lower left", ncol=2, frameon=False, bbox_to_anchor=(0, -0.42))
    save(fig, "fig_agreement_datasets")


def fig_positions() -> None:
    """Rank of each studied explainer under each metric, original and S1-B (160 blocks)."""
    sources = {"Original (LIME slopes)": RES / "exploratory_post" / "r3_positions_by_metric.csv",
               "S1-B (LIME contributions)": S1 / "s1b" / "positions_by_metric.csv"}
    fig, axes = plt.subplots(2, 3, figsize=(6.5, 3.8), sharex=True, sharey=True,
                             gridspec_kw={"wspace": 0.12, "hspace": 0.25})
    for row, (title, path) in enumerate(sources.items()):
        df = pd.read_csv(path)
        for col, expl in enumerate(["shap", "lime", "occlusion"]):
            ax = axes[row, col]
            sub = df[df.explainer == expl].set_index("metric").loc[METRICS]
            left = np.zeros(len(METRICS))
            for part, lab in [("r1", "first"), ("r2", "second"), ("r3", "last"),
                              ("tied", "tied")]:
                ax.barh(range(len(METRICS)), sub[part], left=left, color=C[part],
                        height=0.75, label=lab)
                left += sub[part].to_numpy()
            ax.set_yticks(range(len(METRICS)), [LABEL[m] for m in METRICS])
            ax.set_xlim(0, 160)
            ax.invert_yaxis()
            if row == 0:
                ax.set_title({"shap": "SHAP", "lime": "LIME", "occlusion": "Occlusion"}[expl])
            if col == 0:
                ax.set_ylabel(title, fontsize=7.5)
            if row == 1:
                ax.set_xlabel("Blocks (of 160)")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=4, frameon=False, loc="upper center",
               bbox_to_anchor=(0.5, 1.0))
    fig.subplots_adjust(top=0.86)
    save(fig, "fig_positions")


def fig_h2_matrix() -> None:
    """Instance-level agreement between M1-M6: unadjusted (lower) and adjusted (upper)."""
    raw = pd.read_csv(RES / "analysis" / "confirmatory" / "h2_matrix.csv").set_index("metric")
    adj = pd.read_csv(RES / "exploratory_post" / "r6_summary.csv").set_index("pair")
    m = METRICS[:6]
    grid = np.full((6, 6), np.nan)
    for i in range(6):
        for j in range(6):
            if i > j:
                grid[i, j] = raw.loc[m[i], m[j]]
            elif i < j:
                grid[i, j] = adj.loc[f"{m[i]}|{m[j]}", "adjusted_mean"]
    fig, ax = plt.subplots(figsize=(3.6, 3.2))
    im = ax.imshow(grid, cmap="RdBu_r", vmin=-0.8, vmax=0.8)
    for i in range(6):
        for j in range(6):
            if i != j:
                v = grid[i, j]
                ax.text(j, i, f"{v:.2f}".replace("-", "−"), ha="center", va="center",
                        fontsize=6.5, color="white" if abs(v) > 0.5 else "black")
    ax.set_xticks(range(6), [LABEL[k] for k in m])
    ax.set_yticks(range(6), [LABEL[k] for k in m])
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel("Upper triangle: adjusted for $f(x)$ (exploratory)", fontsize=7)
    ax.set_ylabel("Lower triangle: unadjusted (H2)", fontsize=7)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Mean Spearman over instances")
    save(fig, "fig_h2_matrix")


def fig_sensitivity() -> None:
    """System-level agreement under the specified sensitivity analyses, three LIME representations."""
    df = pd.read_csv(S1 / "comparison_summary.csv")
    rows = [("H1 mean pairwise Spearman (3 explainers, 7 metrics)", "Primary specification"),
            ("H1 second baseline (Spearman)", "Second masking baseline"),
            ("H1 six metrics, no M4 (Spearman)", "Six metrics (M4 removed)"),
            ("H1 four explainers (Spearman)", "With random control"),
            ("within-metric stability benchmark", "Within-metric stability")]
    fig, ax = plt.subplots(figsize=(6.5, 2.6))
    for r, (q, label) in enumerate(rows):
        for k, (cond, dy, marker) in enumerate([("original", -0.22, "o"), ("S1-B", 0.0, "s"),
                                                ("S1-M", 0.22, "^")]):
            v = df[(df.quantity == q) & (df.condition == cond)].iloc[0]
            ax.errorbar(v["mean"], r + dy, xerr=[[v["mean"] - v["lo"]], [v["hi"] - v["mean"]]],
                        fmt=marker, color=C[cond], ms=4, lw=1, capsize=2,
                        label={"original": "Original (LIME slopes)", "S1-B": "S1-B",
                               "S1-M": "S1-M"}[cond] if r == 0 else None)
    ax.axvline(0.5, color="black", lw=0.6, ls="--")
    ax.set_yticks(range(len(rows)), [lab for _, lab in rows])
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel("Mean over eight datasets with 95% t-interval")
    ax.legend(frameon=False, loc="upper center", ncol=3, bbox_to_anchor=(0.5, -0.22))
    save(fig, "fig_sensitivity")


def fig_s3() -> None:
    """S3: agreement of LIME representations with exact Shapley values (synthetic)."""
    df = pd.read_csv(RES / "supplementary" / "s3" / "s3_condition.csv")
    conds = ["additive_rho00", "additive_rho50", "interaction_rho00", "interaction_rho50"]
    names = {"additive_rho00": "Additive,\nindependent", "additive_rho50": "Additive,\ncorrelated",
             "interaction_rho00": "Interaction,\nindependent",
             "interaction_rho50": "Interaction,\ncorrelated"}
    reps = [("S3-A", "Slopes (as stored)", C["original"]),
            ("S3-B", "Contributions $w_j(x_j-\\mu_j)/s_j$", C["S1-M"]),
            ("S3-C", "Discretised LIME", C["r3"])]
    fig, ax = plt.subplots(figsize=(6.5, 2.6))
    x = np.arange(len(conds))
    for k, (rep, label, color) in enumerate(reps):
        sub = df[df.representation == rep].set_index("condition").loc[conds]
        kd = df[df.representation == rep + "-kd"].set_index("condition").loc[conds]
        pos = x + (k - 1) * 0.26
        ax.bar(pos, sub["mean_over_seeds"], width=0.24, color=color, label=label + " (width 3.0)")
        ax.errorbar(pos, sub["mean_over_seeds"],
                    yerr=[sub["mean_over_seeds"] - sub["min_seed"],
                          sub["max_seed"] - sub["mean_over_seeds"]],
                    fmt="none", color="black", lw=0.6, capsize=1.5)
        ax.scatter(pos, kd["mean_over_seeds"], marker="D", s=10, facecolor="white",
                   edgecolor="black", lw=0.6, zorder=3,
                   label="Package default width" if k == 0 else None)
    ax.axhline(0, color="black", lw=0.5)
    ax.set_xticks(x, [names[c] for c in conds])
    ax.set_ylim(-0.1, 1.05)
    ax.set_ylabel("Mean Spearman with\nexact Shapley values")
    ax.legend(frameon=False, loc="upper center", ncol=2, fontsize=6.5,
              bbox_to_anchor=(0.5, -0.28))
    save(fig, "fig_s3")


def main() -> None:
    fig_agreement_datasets()
    fig_positions()
    fig_h2_matrix()
    fig_sensitivity()
    fig_s3()


if __name__ == "__main__":
    main()
