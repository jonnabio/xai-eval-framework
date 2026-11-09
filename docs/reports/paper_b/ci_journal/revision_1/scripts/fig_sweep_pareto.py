"""Paper B rev. 1, Figure 1: stability against fidelity over the configuration sweep, one panel
per model, with the Pareto front of each model.

    python fig_sweep_pareto.py <results dir with sweep_summary_long.csv> <figures dir>

Writes fig1_sweep_pareto.pdf and .png. Colours as in the paper's other figures.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

COLOR_LIME = "#0072B2"
COLOR_SHAP = "#D55E00"
MODELS = [("logreg", "Logistic regression"), ("rf", "Random forest"), ("xgb", "XGBoost"),
          ("svm", "SVM"), ("mlp", "MLP")]

res, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
s = pd.read_csv(res / "sweep_summary_long.csv")


def style(cfg):
    if cfg.startswith("lime"):
        kw = cfg.split("_")[1]
        return COLOR_LIME, {"kwdef": "o", "kw10p0": "s", "kw15p0": "^"}[kw]
    return COLOR_SHAP, ("D" if cfg.startswith("tshap") else "o")


fig, axes = plt.subplots(1, 5, figsize=(12, 2.9), sharey=True)
for ax, (m, title) in zip(axes, MODELS):
    g = s[s.model == m]
    for _, r in g.iterrows():
        c, mk = style(r.config)
        main = r.config in ("lime_kwdef_ns1000", "kshap_ns500_bg50", "tshap_bg50")
        ax.scatter(r.fidelity, r.stability, color=c, marker=mk, s=34 if main else 18,
                   facecolors=c if main else "none", linewidths=0.9, zorder=3)
    f = g.sort_values("fidelity", ascending=False)
    front, best = [], -1.0
    for _, r in f.iterrows():
        if r.stability > best:
            front.append((r.fidelity, r.stability)); best = r.stability
    xs, ys = zip(*front)
    ax.plot(xs, ys, color="#555555", linewidth=0.9, linestyle="--", zorder=2)
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("Fidelity", fontsize=8)
    ax.set_xlim(0, 1.02); ax.set_ylim(0, 1.02)
    ax.tick_params(labelsize=7)
    ax.grid(alpha=0.25, linewidth=0.5)
axes[0].set_ylabel("Stability", fontsize=8)
h = [plt.Line2D([], [], color=COLOR_LIME, marker=k, linestyle="", markerfacecolor="none", label=l)
     for k, l in (("o", "LIME, default width"), ("s", "LIME, width 10"), ("^", "LIME, width 15"))]
h += [plt.Line2D([], [], color=COLOR_SHAP, marker="o", linestyle="", markerfacecolor="none", label="KernelSHAP"),
      plt.Line2D([], [], color=COLOR_SHAP, marker="D", linestyle="", markerfacecolor="none", label="TreeSHAP"),
      plt.Line2D([], [], color="#555555", marker="o", linestyle="", label="main protocol (filled)"),
      plt.Line2D([], [], color="#555555", linestyle="--", label="Pareto front")]
fig.legend(handles=h, loc="lower center", ncol=7, fontsize=7, frameon=False, bbox_to_anchor=(0.5, -0.02))
fig.tight_layout(rect=(0, 0.08, 1, 1))
for ext in ("pdf", "png"):
    fig.savefig(out / f"fig1_sweep_pareto.{ext}", dpi=300, bbox_inches="tight")
print("ok")
