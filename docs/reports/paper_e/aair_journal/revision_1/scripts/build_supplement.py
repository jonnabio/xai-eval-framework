#!/usr/bin/env python3
"""Paper E, AAIR revision 1: supplementary file (reviewer 2, item 6; author decision D-2).

    .venv/Scripts/python.exe docs/reports/paper_e/aair_journal/revision_1/scripts/build_supplement.py
        [--exp3-model-root <dir>] [--no-pdf]

Every value is read from a file: model hyperparameters from the model binaries, explainer
settings from the repository configuration and wrappers (stated in SETTINGS below, each with
its source), results from outputs/analysis/paper_e/. Nothing is typed by hand.
Writes build/supplement/paper_e_aair_rev1_supplement.md, .docx and (with Word) .pdf.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import subprocess
import sys
import warnings
from pathlib import Path

REV = Path(__file__).resolve().parents[1]
AAIR = REV.parent
ROOT = Path(__file__).resolve().parents[6]
POSTHOC = ROOT / "outputs" / "analysis" / "paper_e" / "posthoc"
ANALYSIS = ROOT / "outputs" / "analysis" / "paper_e" / "analysis"
OUT = REV / "build" / "supplement"
NAME = "paper_e_aair_rev1_supplement"
ARCHIVE = "https://doi.org/10.5281/zenodo.24518192"
RELEASE = "paper-e-aair-2026-11-24-r1"

DATASET = {"exp2_adult": "Adult", "german_credit": "German Credit", "breast_cancer": "Breast Cancer"}
MODEL = {"logreg": "LR", "svm": "SVM", "mlp": "MLP", "rf": "RF", "xgb": "XGB", "all": "All"}
PARAMS = {"LogisticRegression": ["C", "penalty", "solver", "max_iter"],
          "SVC": ["C", "kernel", "gamma", "probability"],
          "MLPClassifier": ["hidden_layer_sizes", "activation", "alpha", "max_iter"],
          "RandomForestClassifier": ["n_estimators", "max_depth", "min_samples_leaf"],
          "XGBClassifier": ["n_estimators", "max_depth", "learning_rate"]}

# Explainer settings: (explainer, setting, source in the repository)
SETTINGS = [
    ("SHAP (RF, XGB)", "TreeSHAP, interventional, probability of class 1; 50 background instances "
     "from the training data", "configs/experiments/exp2_comparative/*_shap.yaml; src/xai/shap_tabular.py"),
    ("SHAP (LR, SVM, MLP)", "KernelSHAP, probability of class 1; 50 background instances",
     "configs/experiments/exp2_comparative/*_shap.yaml; src/xai/shap_tabular.py"),
    ("LIME (study)", "kernel width 3; 1000 samples; ten features; discretize_continuous = False; "
     "auto feature selection", "configs/experiments/exp2_comparative/*_lime.yaml; src/xai/lime_tabular.py"),
    ("LIME (settings analysis)", "w3_5k, w3_10k: width 3, no discretisation, 5000 / 10000 samples; "
     "wd_5k: default width 0.75*sqrt(p), no discretisation, 5000; package: default width, quartile "
     "discretisation, 5000; random states 1001 and 2002",
     "docs/reports/paper_e/scripts/paper_e_lime_settings.py"),
    ("Anchors (Adult)", "precision threshold 0.95", "configs/experiments/exp2_comparative/*_anchors.yaml; "
     "src/xai/anchors_wrapper.py"),
    ("DiCE (Adult)", "method random; one counterfactual; desired class opposite",
     "src/xai/dice_wrapper.py"),
]


def rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def f3(x: str) -> str:
    return f"{float(x):.3f}".replace("-", "−") if x not in ("", None) else "–"


def ci(r: dict, prefix: str) -> str:
    return f"{f3(r[prefix + 'estimate_mean_of_run_means'])} [{f3(r[prefix + 'ci95_low'])}, {f3(r[prefix + 'ci95_high'])}]"


def table(head: list[str], body: list[list[str]]) -> str:
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in body]
    return "\n".join(out)


def model_rows(exp3_root: Path | None) -> list[list[str]]:
    import joblib
    warnings.filterwarnings("ignore")
    out = []
    items = [("Adult", "seed-42 partition (all seeds)", ROOT / "experiments" / "exp1_adult" / "models" / f"{m}.joblib")
             for m in ("logreg", "svm", "mlp", "rf", "xgb")]
    if exp3_root:
        items += [(DATASET[d], f"seed {s}", exp3_root / d / m / f"seed_{s}" / f"{m}.joblib")
                  for d in ("german_credit", "breast_cancer") for m in ("rf", "xgb") for s in (42, 123, 456)]
    for dataset, fit, path in items:
        obj = joblib.load(path)
        obj = getattr(obj, "model", obj)
        name = type(obj).__name__
        params = obj.get_params()
        out.append([dataset, name, fit, "; ".join(f"{k} = {params.get(k)}" for k in PARAMS[name])])
    return out


def markdown(exp3_root: Path | None) -> str:
    md = ["# Supplementary material", "",
          "**Do Explainers Agree on Which Features Matter? Instance-Level Agreement between SHAP and LIME** "
          "(revision 1). Every value below is generated from the files of the archive "
          f"({ARCHIVE}, release `{RELEASE}`); the code that produces each table is named with it.", ""]

    md += ["## S1. Models", "",
           "Hyperparameters read from the model binaries used by the study"
           + ("" if exp3_root else " (Adult only; the German Credit and Breast Cancer binaries are "
              "regenerated with `scripts/train_exp3_models.py`)") + ".", "",
           table(["Dataset", "Model", "Fit", "Hyperparameters"], model_rows(exp3_root)), ""]

    md += ["## S2. Explainer configurations", "",
           table(["Explainer", "Settings", "Source"], [list(r) for r in SETTINGS]), ""]

    md += ["## S3. Agreement measures", "",
           "For one instance, $S_k$ and $L_k$ are the sets of the $k$ features with the largest absolute SHAP "
           "and LIME values. **Top-k Jaccard** $J_k = |S_k \\cap L_k| / |S_k \\cup L_k|$, $k = 5$ (primary) and "
           "$k = 10$. **Kendall's $\\tau_b$** on the union of the two top-10 lists, absent features at rank 11, "
           "ties as midranks. **Sign agreement**: share of the features of $S_5 \\cap L_5$ with both values "
           "non-zero whose signs agree; post hoc, the LIME slope $w_j$ converted into a contribution "
           "$c_j = w_j (x_j - m_j)/s_j$. **Permutation reference**: the SHAP list of an instance against the LIME "
           "list of another instance of the same run (20 draws per instance), and, in S5, of the same predicted "
           "class. **Self-agreement**: two runs of a method with different random states on the same instance. "
           "Aggregation: run means; mean of run means; 95% interval from a percentile bootstrap over seeds "
           "(2000 resamples). Code: `scripts/analyze_paper_e.py` (`primary_agreement`).", ""]

    held = [r for r in rows(POSTHOC / "rev1_heldout_summary.csv")]
    body = []
    for m in ("logreg", "svm", "mlp", "rf", "xgb", "all"):
        for subset in ("all", "heldout", "train"):
            r = next(x for x in held if x["model"] == m and x["subset"] == subset)
            body.append([MODEL[m], subset, r["n_runs"], r["n_instances"], ci(r, "top5_jaccard."),
                         ci(r, "top10_jaccard."), ci(r, "kendall_tau_b.")])
    md += ["## S4. Adult: primary measures on held-out instances (post hoc)", "",
           "Held-out: instances that are not rows of the seed-42 training partition; a run enters a cell with "
           "at least 10 instances. Code: `paper_e_revision1_analyses.py`.", "",
           table(["Model", "Subset", "Runs", "Pairs", "Top-5 Jaccard", "Top-10 Jaccard", "Kendall τb"], body), ""]

    perm = rows(POSTHOC / "rev1_same_class_permutation_summary.csv")
    body = [[DATASET[r["dataset"]], MODEL[r["model"]], f3(r["paired_top5_jaccard.estimate_mean_of_run_means"]),
             f3(r["other_any_class_top5_jaccard.estimate_mean_of_run_means"]),
             f3(r["other_same_class_top5_jaccard.estimate_mean_of_run_means"]),
             ci(r, "specific_vs_same_class.")] for r in perm]
    md += ["## S5. Permutation reference within the predicted class (post hoc)", "",
           table(["Dataset", "Model", "Paired", "Other (any class)", "Other (same class)",
                  "Instance-specific (same class)"], body), ""]

    loso = rows(POSTHOC / "rev1_leave_one_seed_out.csv")
    body = [[DATASET[r["dataset"]], MODEL[r["model"]], r["n_seeds"]]
            + [f"{f3(r[m + '.all_seeds'])} ({f3(r[m + '.loso_min'])} to {f3(r[m + '.loso_max'])})"
               for m in ("top5_jaccard", "top10_jaccard", "kendall_tau_b")] for r in loso]
    md += ["## S6. Leave one seed out (post hoc)", "",
           "All seeds, and in parentheses the smallest and largest estimate with one seed left out.", "",
           table(["Dataset", "Model", "Seeds", "Top-5 Jaccard", "Top-10 Jaccard", "Kendall τb"], body), ""]

    ls = rows(POSTHOC / "lime_settings_summary.csv")
    names = {"w3_1k": "Width 3, 1000 (study)", "w3_5k": "Width 3, 5000", "w3_10k": "Width 3, 10000",
             "wd_5k": "Default width, 5000", "package": "Package defaults"}
    body = []
    for d in ("exp2_adult", "german_credit", "breast_cancer"):
        models = sorted({r["model"] for r in ls if r["dataset"] == d} - {"all"}) + ["all"]
        for m in models:
            for s in names:
                get = {r["pair"]: r for r in ls if r["dataset"] == d and r["model"] == m and r["setting"] == s
                       and r["metric"] == "top5_jaccard"}
                body.append([DATASET[d], MODEL[m], names[s]]
                            + [f"{f3(get[p]['estimate_mean_of_run_means'])}" for p in ("self", "shap_lime", "vs_study")])
    shap_self = {(r["dataset"], r["model"]): r for r in rows(POSTHOC / "ceiling_summary.csv")
                 if r["pair"] == "shap_shap" and r["metric"] == "top5_jaccard"}
    md += ["## S7. LIME settings (post hoc)", "",
           "Top-5 Jaccard on the self-agreement subsample (760 instances). LIME self: two LIME runs with "
           "different random states; SHAP–LIME: mean of the four pairs of a SHAP and a LIME run; vs study: "
           "against the stored LIME list of the study. SHAP self-agreement for reference: "
           + "; ".join(f"{DATASET[d]} {f3(shap_self[(d, 'all')]['estimate_mean_of_run_means'])}"
                       for d in ("exp2_adult", "german_credit", "breast_cancer"))
           + ". Code: `paper_e_lime_settings.py`.", "",
           table(["Dataset", "Model", "Setting", "LIME self", "SHAP–LIME", "vs study"], body), ""]

    md += ["## S8. Reproduction", "",
           "From the repository root, with the archive of the release:", "",
           "```",
           "python docs/reports/paper_e/scripts/paper_e_revision1_analyses.py",
           "python scripts/train_exp3_models.py --model-root <dir> --data-cache-dir data",
           "python docs/reports/paper_e/scripts/paper_e_lime_settings.py --exp3-model-root <dir>",
           "python docs/reports/paper_e/aair_journal/scripts/build_paper_e_aair_docx.py",
           "python docs/reports/paper_e/aair_journal/revision_1/scripts/build_supplement.py --exp3-model-root <dir>",
           "```", ""]
    return "\n".join(md)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp3-model-root", type=Path)
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    md = OUT / f"{NAME}.md"
    md.write_text(markdown(a.exp3_model_root), encoding="utf-8")
    docx = OUT / f"{NAME}.docx"
    r = subprocess.run(["quarto", "pandoc", str(md), "-f", "markdown", "-t", "docx", "-o", str(docx)],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"pandoc failed: {r.stderr[-800:]}")
    if not a.no_pdf:
        spec = importlib.util.spec_from_file_location("aair_builder", AAIR / "scripts" / "build_paper_e_aair_docx.py")
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        builder.OUT = OUT
        pages = builder.word_pass(docx, "Supplementary material", builder.AUTHOR)
        print(f"supplement: {pages} pages")
    print(f"wrote {md.relative_to(ROOT)} and .docx")
    return 0


if __name__ == "__main__":
    sys.exit(main())
