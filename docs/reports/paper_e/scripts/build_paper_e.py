#!/usr/bin/env python3
"""Build Paper E: figures, tables, paper_e.tex and the two PDFs.

No number in the manuscript is typed by hand. Each <<kind|...>> placeholder in
paper_e_template.tex and each table cell is read from the CSV files under
outputs/analysis/paper_e/ (analysis/ = prespecified, posthoc/ = post hoc).

    python docs/reports/paper_e/scripts/paper_e_posthoc.py     # once, if posthoc/ is missing
    python docs/reports/paper_e/scripts/build_paper_e.py        # figures + tables + tex + PDFs
    python docs/reports/paper_e/scripts/build_paper_e.py --no-pdf

Outputs, all under docs/reports/paper_e/:
    figures/fig*.pdf  tables/*.tex  paper_e.tex
    submission/paper_e_blind.pdf   (for review: no author identity)
    submission/paper_e_full.pdf
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
D = ROOT / "docs" / "reports" / "paper_e"
A = ROOT / "outputs" / "analysis" / "paper_e" / "analysis"
P = ROOT / "outputs" / "analysis" / "paper_e" / "posthoc"
EXE = "tectonic.exe" if sys.platform == "win32" else "tectonic"
TECTONIC_CANDIDATES = [
    ROOT / "tools" / "tectonic-portable" / EXE,
    ROOT.parent / "xai-eval-framework" / "tools" / "tectonic-portable" / EXE,
]

DATASETS = [("exp2_adult", "Adult"), ("german_credit", "German Credit"), ("breast_cancer", "Breast Cancer")]
MODEL_LABEL = {"logreg": "LR", "svm": "SVM", "mlp": "MLP", "rf": "RF", "xgb": "XGB", "all": "All"}
ADULT_MODELS = ["logreg", "svm", "mlp", "rf", "xgb"]
EXP3_MODELS = ["rf", "xgb"]
GROUPS = ([("exp2_adult", m) for m in ADULT_MODELS]
          + [("german_credit", m) for m in EXP3_MODELS]
          + [("breast_cancer", m) for m in EXP3_MODELS])
QUALITY = [("shap_fidelity", "SHAP fidelity"), ("shap_stability", "SHAP stability"),
           ("lime_fidelity", "LIME fidelity"), ("lime_stability", "LIME stability")]
PAIRS = [("shap_anchors", "SHAP vs. Anchors"), ("lime_anchors", "LIME vs. Anchors"),
         ("shap_dice", "SHAP vs. DiCE"), ("lime_dice", "LIME vs. DiCE"),
         ("anchors_dice", "Anchors vs. DiCE")]


class Data:
    def __init__(self) -> None:
        self.group = pd.read_csv(A / "group_agreement_summary.csv")
        self.runs = pd.read_csv(A / "run_agreement_summary.csv")
        self.corr = pd.read_csv(A / "correctness_group_summary.csv")
        self.contrasts = pd.read_csv(A / "correctness_contrasts.csv")
        self.qual = pd.read_csv(A / "quality_association_summary.csv")
        self.qual_seed = pd.read_csv(A / "quality_association_by_seed.csv")
        self.pairing = pd.read_csv(A / "pairing_diagnostics.csv")
        self.inventory = pd.read_csv(A / "run_inventory.csv")
        self.margin = pd.read_csv(P / "adult_margin_summary.csv")
        self.sign = pd.read_csv(P / "sign_by_predicted_class_summary.csv")
        self.sign_runs = pd.read_csv(P / "sign_by_predicted_class_runs.csv")
        self.const = pd.read_csv(P / "sign_constancy_summary.csv")
        self.sec = pd.read_csv(P / "secondary_group_summary.csv")
        self.chance = pd.read_csv(P / "chance_overlap.csv")

    @staticmethod
    def _one(frame: pd.DataFrame, what: str) -> pd.Series:
        if len(frame) != 1:
            raise SystemExit(f"lookup {what} matched {len(frame)} rows, expected 1")
        return frame.iloc[0]

    def agree(self, dataset: str, model: str, metric: str) -> pd.Series:
        """Agreement for a dataset/model, pooled over Adult intensities."""
        if dataset == "exp2_adult" and model != "all":
            g = self.margin
            return self._one(g[(g.model == model) & (g.intensity == "all") & (g.metric == metric)],
                             f"margin {model} {metric}")
        g = self.group
        return self._one(g[(g.dataset == dataset) & (g.model == model) & (g.metric == metric)],
                         f"group {dataset} {model} {metric}")

    def intensity(self, intensity: str, metric: str) -> pd.Series:
        g = self.margin
        return self._one(g[(g.model == "all") & (g.intensity == intensity) & (g.metric == metric)],
                         f"intensity {intensity} {metric}")

    def scalar(self, name: str) -> int:
        pr = self.pairing
        if name == "paired":
            return int(pr.matched_ids.sum())
        if name == "blocks":
            return len(pr)
        if name == "exact_blocks":
            return int(pr.same_id_sets.astype(str).str.lower().eq("true").sum())
        if name == "unpaired":
            return int(pr.left_only_ids.sum() + pr.right_only_ids.sum())
        if name == "mismatches":
            return int(pr.classification_mismatches.sum())
        if name == "invalid_rows":
            return int(self.inventory.invalid_rows.sum())
        if name == "source_runs":
            return len(self.inventory)
        if name == "primary_runs":
            return len(self.runs)
        if name in ("tau_undefined", "sign_undefined"):
            inst = pd.read_csv(A / "instance_agreement.csv",
                               usecols=["kendall_tau_b", "sign_agreement"])
            column = "kendall_tau_b" if name == "tau_undefined" else "sign_agreement"
            return int(inst[column].isna().sum())
        if name.startswith("inst_"):
            return int(self.runs[self.runs.dataset == name[5:]].n_instances.sum())
        if name.startswith("runs_"):
            return int((self.runs.dataset == name[5:]).sum())
        if name.startswith("corr_runs_"):
            c = self.contrasts
            return int(((c.dataset == name[10:]) & (c.row_type == "run") & c.included).sum())
        raise SystemExit(f"unknown scalar {name}")


def f3(x: float) -> str:
    return f"{x:.3f}".replace("-", "$-$")


def f2(x: float) -> str:
    return f"{x:.2f}".replace("-", "$-$")


def ci(row: pd.Series) -> str:
    return f"[{f3(row.ci95_low)}, {f3(row.ci95_high)}]"


def integer(x: int) -> str:
    return f"{x:,}".replace(",", "{,}")


def resolve(data: Data, spec: str) -> str:
    kind, *a = spec.split("|")
    field = {"est": "estimate_mean_of_run_means", "lo": "ci95_low", "hi": "ci95_high"}
    if kind == "n":
        return integer(data.scalar(a[0]))
    if kind == "agree":      # dataset|model|metric|field
        return f3(data.agree(a[0], a[1], a[2])[field[a[3]]])
    if kind == "int":        # intensity|metric|field
        return f3(data.intensity(a[0], a[1])[field[a[2]]])
    if kind == "sign":       # dataset|model|class|field
        s = data.sign
        return f3(Data._one(s[(s.dataset == a[0]) & (s.model == a[1]) & (s.predicted_class == int(a[2]))],
                            spec)[field[a[3]]])
    if kind == "const":      # dataset|model|method|field
        s = data.const
        return f3(Data._one(s[(s.dataset == a[0]) & (s.model == a[1]) & (s.method == a[2])], spec)[field[a[3]]])
    if kind == "corr":       # dataset|model|column
        c = data.corr
        inten = "all" if a[0] == "exp2_adult" else "not_applicable"
        row = Data._one(c[(c.dataset == a[0]) & (c.model == a[1]) & (c.intensity == inten)], spec)
        return f3(row[{"diff": "mean_misclassified_minus_correct", "lo": "ci95_low", "hi": "ci95_high",
                       "correct": "mean_correct_jaccard", "mis": "mean_misclassified_jaccard"}[a[2]]])
    if kind == "corrmax":    # largest absolute model-level difference (intensity-pooled)
        c = data.corr
        return f3(c[c.intensity.isin(["all", "not_applicable"])].mean_misclassified_minus_correct.abs().max())
    if kind == "qual":       # dataset|model|metric
        q = data.qual
        return f2(Data._one(q[(q.dataset == a[0]) & (q.model == a[1]) & (q.quality_metric == a[2])],
                            spec).mean_seed_spearman_rho)
    if kind == "qrange":     # dataset|metric|min or max   (over model families)
        q = data.qual
        values = q[(q.dataset == a[0]) & (q.quality_metric == a[1])].mean_seed_spearman_rho
        return f2(values.min() if a[2] == "min" else values.max())
    if kind == "sec":        # pair|model|field
        s = data.sec
        return f3(Data._one(s[(s.method_pair == a[0]) & (s.model == a[1])], spec)[field[a[2]]])
    if kind == "chance":     # dataset|5 or 10
        c = data.chance
        return f3(Data._one(c[c.dataset == a[0]], spec)[f"expected_top{a[1]}_jaccard"])
    raise SystemExit(f"unknown placeholder <<{spec}>>")


# --- tables -------------------------------------------------------------------

def table_agreement(data: Data) -> str:
    lines = []
    for dataset, label in DATASETS:
        models = (ADULT_MODELS if dataset == "exp2_adult" else EXP3_MODELS) + ["all"]
        for k, model in enumerate(models):
            cells = []
            for metric in ("top5_jaccard", "top10_jaccard", "kendall_tau_b"):
                row = data.agree(dataset, model, metric)
                cells.append(f"{f3(row.estimate_mean_of_run_means)} {ci(row)}")
            n = data.agree(dataset, model, "top5_jaccard")
            name = label if k == 0 else ""
            lines.append(f"{name} & {MODEL_LABEL[model]} & {int(n.n_runs)} & {integer(int(n.n_instances))} & "
                         + " & ".join(cells) + r" \\")
        lines.append(r"\hline")
    return "\n".join(lines) + "\n"


def table_sign(data: Data) -> str:
    lines = []
    for dataset, label in DATASETS:
        models = (ADULT_MODELS if dataset == "exp2_adult" else EXP3_MODELS) + ["all"]
        for k, model in enumerate(models):
            overall = data.agree(dataset, model, "sign_agreement").estimate_mean_of_run_means
            s, c = data.sign, data.const
            by_class = [Data._one(s[(s.dataset == dataset) & (s.model == model) & (s.predicted_class == cls)],
                                  "sign").estimate_mean_of_run_means for cls in (0, 1)]
            const = [Data._one(c[(c.dataset == dataset) & (c.model == model) & (c.method == meth)],
                               "const").estimate_mean_of_run_means for meth in ("shap", "lime")]
            name = label if k == 0 else ""
            lines.append(f"{name} & {MODEL_LABEL[model]} & {f3(overall)} & {f3(by_class[0])} & {f3(by_class[1])} & "
                         f"{f3(const[0])} & {f3(const[1])}" + r" \\")
        lines.append(r"\hline")
    return "\n".join(lines) + "\n"


def table_correctness(data: Data) -> str:
    lines = []
    c = data.corr
    for dataset, model in GROUPS:
        if dataset == "breast_cancer":
            continue
        inten = "all" if dataset == "exp2_adult" else "not_applicable"
        row = Data._one(c[(c.dataset == dataset) & (c.model == model) & (c.intensity == inten)], "corr")
        name = "Adult" if dataset == "exp2_adult" else "GC"
        lines.append(f"{name} & {MODEL_LABEL[model]} & {f3(row.mean_correct_jaccard)} & "
                     f"{f3(row.mean_misclassified_jaccard)} & {f3(row.mean_misclassified_minus_correct)} & "
                     f"{ci(row)} & {int(row.n_negative_seed_differences)}/{int(row.n_seed_units)}" + r" \\")
    lines.append(r"\hline")  # the rule is in the generated file: \hline after \input fails
    return "\n".join(lines) + "\n"


def table_quality(data: Data) -> str:
    lines = []
    q = data.qual
    for dataset, label in DATASETS:
        models = ADULT_MODELS if dataset == "exp2_adult" else EXP3_MODELS
        for k, model in enumerate(models):
            cells = [f2(Data._one(q[(q.dataset == dataset) & (q.model == model) & (q.quality_metric == metric)],
                                  "qual").mean_seed_spearman_rho) for metric, _ in QUALITY]
            lines.append(f"{label if k == 0 else ''} & {MODEL_LABEL[model]} & " + " & ".join(cells) + r" \\")
        lines.append(r"\hline")
    return "\n".join(lines) + "\n"


def table_secondary(data: Data) -> str:
    lines = []
    s = data.sec
    for pair, label in PAIRS:
        row = Data._one(s[(s.method_pair == pair) & (s.model == "all")], "sec")
        lines.append(f"{label} & {int(row.n_runs)} & {integer(int(row.n_instances))} & "
                     f"{f3(row.estimate_mean_of_run_means)} & {ci(row)}" + r" \\")
    lines.append(r"\hline")
    return "\n".join(lines) + "\n"


# --- figures ------------------------------------------------------------------

BLUE, ORANGE, GREY = "#1f5fa8", "#d1711f", "#555555"


def style() -> None:
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 8, "axes.labelsize": 8, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
        "legend.fontsize": 7.5, "axes.spines.top": False, "axes.spines.right": False,
        "axes.linewidth": 0.6, "pdf.fonttype": 42, "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
    })


def group_axis(ax, positions: list[float], short: bool = False) -> None:
    ax.set_xticks(positions, [MODEL_LABEL[m] for _, m in GROUPS])
    bounds = {"exp2_adult": (0, 4), "german_credit": (5, 6), "breast_cancer": (7, 8)}
    for dataset, label in DATASETS:
        lo, hi = bounds[dataset]
        if short:
            label = {"German Credit": "German Cr.", "Breast Cancer": "Breast Ca."}.get(label, label)
        ax.text((positions[lo] + positions[hi]) / 2, -0.19, label, transform=ax.get_xaxis_transform(),
                ha="center", va="top", fontsize=8)
    for edge in (4, 6):
        ax.axvline((positions[edge] + positions[edge + 1]) / 2, color="#bbbbbb", linewidth=0.5)


def positions() -> list[float]:
    return [0, 1, 2, 3, 4, 5.4, 6.4, 7.8, 8.8]


def fig_overlap(data: Data) -> None:
    pos = positions()
    fig, ax = plt.subplots(figsize=(6.9, 2.5))
    for x, (dataset, model) in zip(pos, GROUPS):
        runs = data.runs[(data.runs.dataset == dataset) & (data.runs.model == model)].top5_jaccard_mean
        jitter = [x + 0.26 * ((i % 7) / 6 - 0.5) for i in range(len(runs))]
        ax.scatter(jitter, runs, s=7, color=BLUE, alpha=0.35, linewidths=0, zorder=2)
        row = data.agree(dataset, model, "top5_jaccard")
        est = row.estimate_mean_of_run_means
        ax.errorbar(x, est, yerr=[[est - row.ci95_low], [row.ci95_high - est]], fmt="D", color="black",
                    markersize=3.5, capsize=2.5, linewidth=0.9, zorder=3)
        chance = float(data.chance[data.chance.dataset == dataset].expected_top5_jaccard.iloc[0])
        ax.hlines(chance, x - 0.42, x + 0.42, color=ORANGE, linewidth=1.0, linestyles="dashed", zorder=1)
    ax.scatter([], [], s=9, color=BLUE, alpha=0.5, label="Run mean")
    ax.errorbar([], [], yerr=[], fmt="D", color="black", markersize=3.5, label="Mean of run means, 95% interval")
    ax.plot([], [], color=ORANGE, linestyle="dashed", linewidth=1.0, label="Expected overlap of two random top-5 sets")
    ax.set_ylim(0, 1)
    ax.set_ylabel("SHAP\u2013LIME top-5 Jaccard overlap")
    group_axis(ax, pos)
    ax.legend(frameon=False, loc="upper left", ncol=1)
    fig.savefig(D / "figures" / "fig1_top5_overlap.pdf")
    plt.close(fig)


def fig_sign(data: Data) -> None:
    pos = positions()
    fig, ax = plt.subplots(figsize=(6.9, 2.5))
    s = data.sign
    for cls, colour, shift, marker in ((0, BLUE, -0.16, "o"), (1, ORANGE, 0.16, "s")):
        for x, (dataset, model) in zip(pos, GROUPS):
            row = Data._one(s[(s.dataset == dataset) & (s.model == model) & (s.predicted_class == cls)], "sign")
            est = row.estimate_mean_of_run_means
            ax.errorbar(x + shift, est, yerr=[[est - row.ci95_low], [row.ci95_high - est]], fmt=marker,
                        color=colour, markersize=4, capsize=2.5, linewidth=0.9,
                        label=f"Predicted class {cls}" if x == 0 else None)
    for x, (dataset, model) in zip(pos, GROUPS):
        overall = data.agree(dataset, model, "sign_agreement").estimate_mean_of_run_means
        ax.hlines(overall, x - 0.4, x + 0.4, color="black", linewidth=1.0,
                  label="All instances (prespecified estimate)" if x == 0 else None)
    ax.axhline(0.5, color="#999999", linewidth=0.5, linestyle="dotted")
    ax.set_ylim(-0.03, 1.03)
    ax.set_ylabel("Sign agreement on shared\ntop-5 features")
    group_axis(ax, pos)
    ax.legend(frameon=False, loc="lower left", ncol=3, bbox_to_anchor=(0.0, 1.0))
    fig.savefig(D / "figures" / "fig2_sign_by_class.pdf")
    plt.close(fig)


def fig_correctness(data: Data) -> None:
    groups = [g for g in GROUPS if g[0] != "breast_cancer"]
    fig, ax = plt.subplots(figsize=(3.35, 2.6))
    c, cc = data.corr, data.contrasts
    for y, (dataset, model) in enumerate(groups):
        if dataset == "exp2_adult":
            seeds = cc[(cc.dataset == dataset) & (cc.model == model) & (cc.row_type == "seed_intensity_average")]
            row = Data._one(c[(c.dataset == dataset) & (c.model == model) & (c.intensity == "all")], "corr")
        else:
            seeds = cc[(cc.dataset == dataset) & (cc.model == model) & (cc.row_type == "run") & cc.included]
            row = Data._one(c[(c.dataset == dataset) & (c.model == model)], "corr")
        ax.scatter(seeds.misclassified_minus_correct, [y + 0.18] * len(seeds), s=9, color=BLUE, alpha=0.5,
                   linewidths=0)
        est = row.mean_misclassified_minus_correct
        ax.errorbar(est, y - 0.08, xerr=[[est - row.ci95_low], [row.ci95_high - est]], fmt="D", color="black",
                    markersize=3.5, capsize=2.5, linewidth=0.9)
    ax.axvline(0, color="#999999", linewidth=0.6)
    ax.set_yticks(range(len(groups)),
                  [f"{dict(DATASETS)[d]}, {MODEL_LABEL[m]}" for d, m in groups])
    ax.invert_yaxis()
    ax.set_xlabel("Top-5 Jaccard: misclassified minus correct")
    fig.savefig(D / "figures" / "fig3_correctness.pdf")
    plt.close(fig)


def fig_quality(data: Data) -> None:
    pos = positions()
    fig, axes = plt.subplots(2, 2, figsize=(6.9, 3.9), sharex=True, sharey=True)
    q, qs = data.qual, data.qual_seed
    for ax, (metric, label) in zip(axes.ravel(), QUALITY):
        for x, (dataset, model) in zip(pos, GROUPS):
            seeds = qs[(qs.dataset == dataset) & (qs.model == model) & (qs.quality_metric == metric)]
            ax.scatter([x] * len(seeds), seeds.mean_run_spearman_rho, s=9, color=BLUE, alpha=0.45, linewidths=0)
            mean = Data._one(q[(q.dataset == dataset) & (q.model == model) & (q.quality_metric == metric)],
                             "qual").mean_seed_spearman_rho
            ax.hlines(mean, x - 0.3, x + 0.3, color="black", linewidth=1.1)
        ax.axhline(0, color="#999999", linewidth=0.6)
        ax.set_title(label, fontsize=8, loc="left")
        ax.set_ylim(-0.75, 0.45)
        for edge in (4, 6):
            ax.axvline((pos[edge] + pos[edge + 1]) / 2, color="#bbbbbb", linewidth=0.5)
    for ax in axes[1]:
        group_axis(ax, pos, short=True)
    for ax in axes[:, 0]:
        ax.set_ylabel("Spearman $\\rho$ with\ndisagreement")
    fig.subplots_adjust(hspace=0.22, wspace=0.06)
    fig.savefig(D / "figures" / "fig4_quality.pdf")
    plt.close(fig)


# --- render and compile -------------------------------------------------------

def render(data: Data) -> None:
    tables = {"agreement": table_agreement, "sign": table_sign, "correctness": table_correctness,
              "quality": table_quality, "secondary": table_secondary}
    (D / "tables").mkdir(exist_ok=True)
    for name, fn in tables.items():
        (D / "tables" / f"{name}.tex").write_bytes(
            ("% GENERATED by scripts/build_paper_e.py -- do not edit\n" + fn(data)).encode("utf-8"))
    template = (D / "paper_e_template.tex").read_text(encoding="utf-8")
    count = 0

    def sub(match: re.Match) -> str:
        nonlocal count
        count += 1
        return resolve(data, match.group(1))

    body = re.sub(r"<<([^<>]+)>>", sub, template)
    header = ("%% GENERATED from paper_e_template.tex by docs/reports/paper_e/scripts/build_paper_e.py.\n"
              "%% Do not edit: change the template and rebuild.\n")
    (D / "paper_e.tex").write_bytes((header + body).encode("utf-8"))
    print(f"rendered paper_e.tex ({count} values) and {len(tables)} tables")


def compile_pdf() -> None:
    tectonic = next((p for p in TECTONIC_CANDIDATES if p.exists()), None) or shutil.which("tectonic")
    if not tectonic:
        raise SystemExit("tectonic not found; see README.md, 'Build'")
    out = D / "submission"
    out.mkdir(exist_ok=True)
    for name, prefix in (("paper_e_blind", ""), ("paper_e_full", "\\def\\fullversion{}")):
        wrapper = D / f"{name}.tex"
        wrapper.write_text(prefix + "\\input{paper_e.tex}\n", encoding="utf-8")
        try:
            run = subprocess.run([str(tectonic), "--keep-logs", "--outdir", str(out), wrapper.name],
                                 cwd=D, capture_output=True, text=True, encoding="utf-8", errors="replace")
        finally:
            wrapper.unlink()
        problems = [line for line in (run.stdout + run.stderr).splitlines()
                    if re.search(r"undefined|Overfull \\hbox \((?:[2-9]\d|\d{3,})|^error|Citation", line)]
        for line in problems:
            print(f"  {name}: {line.strip()}")
        if run.returncode:
            print(run.stderr[-3000:])
            raise SystemExit(f"tectonic failed for {name}")
        for junk in out.glob(f"{name}.*"):
            if junk.suffix != ".pdf":
                junk.unlink()
        print(f"built submission/{name}.pdf")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-pdf", action="store_true")
    args = ap.parse_args()
    data = Data()
    style()
    (D / "figures").mkdir(exist_ok=True)
    for fn in (fig_overlap, fig_sign, fig_correctness, fig_quality):
        fn(data)
    print("wrote 4 figures")
    render(data)
    if not args.no_pdf:
        compile_pdf()


if __name__ == "__main__":
    main()
