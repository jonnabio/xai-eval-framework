#!/usr/bin/env python3
"""Paper B revision 1: the supplementary file for the reviewers (decision D-B).

    python docs/reports/paper_b/ci_journal/revision_1/scripts/build_supplement.py

A document independent of the paper that lets a reviewer confirm the results: the full
design, the hyperparameters, the data and model fingerprints, the environment, every
per-dataset and per-model result and how to regenerate each table. Everything is read from
the committed sources (cohort.toml, models/MANIFEST.csv, the prepared data, env/HOST.md);
sections S7-S13 come from the analysis of cohort B2 (supplement_results.py); studies not yet run
are marked [R].
Masked: no repository address, no author data (checked).

Writes build/supplement/paper_b_ci_rev1_supplement.docx and .pdf (Word needed for the PDF).
"""
from __future__ import annotations

import csv
import importlib.util
import subprocess
import sys
from pathlib import Path

REV = Path(__file__).resolve().parents[1]
CI = REV.parent
ROOT = REV.parents[4]
OUT = REV / "build" / "supplement"
sys.path.insert(0, str(ROOT / "scripts"))
import paper_b_lib as lib  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
import supplement_results as sr  # noqa: E402

NAMES = {"adult": "Adult", "breast_cancer": "Breast Cancer", "german_credit": "German Credit",
         "diabetes": "Diabetes", "spambase": "Spambase", "phishing": "Phishing",
         "connect4": "Connect-4"}
MODELS = {"logreg": "Logistic regression", "rf": "Random forest", "xgb": "XGBoost",
          "svm": "SVM (RBF)", "mlp": "MLP"}


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fmt(v) -> str:
    if isinstance(v, dict):
        return ", ".join(f"{k}={fmt(x)}" for k, x in v.items())
    if isinstance(v, list):
        return "(" + ", ".join(map(str, v)) + ")"
    return str(v)


def main() -> int:
    import argparse
    import numpy as np
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--analysis", default=str(REV / "results"),
                    help="output folder of scripts/paper_b_analyze.py (default: results/)")
    ap.add_argument("--rows", help="rows.csv of that analysis: derive the per-instance tables "
                    "and Figure S1 into --analysis first")
    ap.add_argument("--timing-root", help="results folder of the runs (with timing/): count the "
                    "finished timing cells into --analysis first")
    ap.add_argument("--no-word", action="store_true", help="do not open Word for the PDF")
    args = ap.parse_args()
    cfg = lib.config()
    manifest = list(csv.DictReader(open(lib.MANIFEST, encoding="utf-8")))
    md = ["# Supplementary material",
          "",
          "*When Does SHAP Outperform LIME? Model- and Configuration-Dependent Results from a "
          "Paired Tabular Benchmark.* Manuscript 2067810, *Computers and Informatics*, "
          "revision 1.",
          "",
          "This file is independent of the paper: it states the whole design and every result "
          "at the level of dataset, model and seed, so that each number in the paper can be "
          "checked. Repository and archive addresses are withheld for masked review.",
          "",
          f"Design fingerprint (SHA-256 of the design configuration): `{lib.config_hash()}`. "
          "Every result row carries it; the analysis refuses rows of another design.",
          ""]

    # S1 design
    c = cfg["cohort"]
    md += ["## S1. Design", "",
           "| Item | Setting |", "|---|---|",
           f"| Split | one stratified split per dataset, test share {c['test_size']}, seed "
           f"{c['split_seed']}; shared by preprocessing, training and every seed |",
           f"| Training cap | {c['max_train_rows']:,} rows (stratified subsample of the training split) |",
           f"| Seeds | Adult: {fmt(cfg['seeds']['adult'])}; other datasets: {fmt(cfg['seeds']['other'])} |",
           f"| Instances | up to {cfg['sampling']['per_stratum']} per stratum (TP, TN, FP, FN) of "
           "the test split; smaller strata taken whole |",
           f"| Stability subset | first {cfg['sampling']['stability_per_stratum']} instances per stratum |",
           f"| Stability | T = {cfg['metrics']['stability_T']} perturbed copies, Gaussian noise "
           f"sigma = {cfg['metrics']['stability_sigma']} on the encoded features |",
           f"| Faithfulness gap | top k = {cfg['metrics']['fidelity_top_k']} features masked together |",
           f"| Sparsity threshold | {cfg['metrics']['sparsity_threshold']} |",
           f"| Timing subset | {cfg['timing']['per_stratum']} instances per stratum, "
           f"{cfg['timing']['repeats']} repetitions, {cfg['timing']['warmup_per_explainer']} "
           "warm-up per explainer, one process, one thread, pinned to one core |",
           ""]

    # S2 datasets
    md += ["## S2. Datasets", "",
           "| Dataset | Source | Train rows | Test rows | Encoded features | Positive share | Role |",
           "|---|---|---:|---:|---:|---:|---|"]
    for name, spec in cfg["datasets"].items():
        d = np.load(lib.DATA_DIR / f"{name}.npz", allow_pickle=True)
        y = np.concatenate([d["y_train"], d["y_test"]])
        src = (f"OpenML {spec['openml_id']}" if spec["loader"] == "openml" else "UCI")
        role = "primary" if spec.get("role") == "main" else spec.get("cell", "further")
        md.append(f"| {NAMES.get(name, name)} | {src} | {d['X_train'].shape[0]:,} | "
                  f"{d['X_test'].shape[0]:,} | {d['X_train'].shape[1]} | {y.mean():.3f} | {role} |")
    md += ["", "Train rows are those available before the training cap. Connect-4: a win is "
           "the positive class; loss and draw are the negative class.", ""]

    # S3 models
    md += ["## S3. Models", "", "| Model | Class | Hyperparameters |", "|---|---|---|"]
    for m, spec in cfg["models"].items():
        md.append(f"| {MODELS.get(m, m)} | `{spec['class']}` | {fmt(spec['params'])} |")
    md += ["", "Test accuracy of the frozen models:", "",
           "| Dataset | " + " | ".join(MODELS[m] for m in cfg["models"]) + " |",
           "|---|" + "---:|" * len(cfg["models"])]
    acc = {(r["dataset"], r["model"]): r["test_accuracy"] for r in manifest}
    for name in cfg["datasets"]:
        md.append(f"| {NAMES.get(name, name)} | " +
                  " | ".join(acc.get((name, m), "—") for m in cfg["models"]) + " |")
    md.append("")

    # S4 explainers
    md += ["## S4. Explainers", "", "| Variant | Settings |", "|---|---|"]
    for e, spec in cfg["explainers"].items():
        s = {k: v for k, v in spec.items() if k not in ("kernel_nsamples_by_model",)}
        md.append(f"| {e} | {fmt(s)} |")
    md += ["", "SHAP uses TreeSHAP for the random forest and XGBoost and KernelSHAP otherwise. "
           "LIME's default kernel width is 0.75 times the square root of the number of encoded "
           "features. Anchors: the attribution vector marks the anchor's features with 1. "
           "DiCE: the attribution of a feature is the absolute change in the counterfactual.", ""]

    # S5 environment
    md += ["## S5. Computing environment", "",
           "One laptop for every run: AMD Ryzen 5 4600H (6 cores, 12 threads, 3.0 GHz base), "
           "31.4 GB RAM, Windows 11 Home 10.0.26300, on mains power. CPython 3.11.11; "
           "scikit-learn 1.7.1, XGBoost 3.1.2, SHAP 0.50.0, LIME 0.2.0.1, NumPy 2.2.6, pandas "
           "2.3.3, SciPy 1.16.3, alibi 0.9.6, dice-ml 0.12. The full frozen environment is "
           "part of the artifacts.", ""]

    # S6 fingerprints
    md += ["## S6. Model and data fingerprints", "",
           "Each run checks the model file against these hashes before it starts.", "",
           "| Dataset | Model | Model SHA-256 (first 16) | Data SHA-256 (first 16) |",
           "|---|---|---|---|"]
    for r in manifest:
        md.append(f"| {NAMES.get(r['dataset'], r['dataset'])} | {MODELS.get(r['model'], r['model'])} "
                  f"| `{r['sha256'][:16]}` | `{r['data_sha256'][:16]}` |")
    md.append("")

    # S7-S13 results, from the analysis of cohort B2 (supplement_results.py)
    res = Path(args.analysis)
    if args.rows:
        sr.derive(Path(args.rows), res)
    if args.timing_root:
        sr.timing_cells(Path(args.timing_root), res)
    md += sr.sections(res, cfg, {})

    OUT.mkdir(parents=True, exist_ok=True)
    src = OUT / "_supplement.md"
    widen = load(REV / "scripts" / "build_drafts.py", "build_drafts").widen
    src.write_text(widen("\n".join(md)), encoding="utf-8")
    docx = OUT / "paper_b_ci_rev1_supplement.docx"
    r = subprocess.run(["quarto", "pandoc", str(src), "-f", "markdown", "-t", "docx",
                        f"--resource-path={res}", "-o", str(docx)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"pandoc failed: {r.stderr[-800:]}")
    (OUT / "paper_b_ci_rev1_supplement.md").write_text("\n".join(md), encoding="utf-8")
    src.unlink(missing_ok=True)
    builder = load(CI / "scripts" / "build_paper_b_ci_docx.py", "build_paper_b_ci_docx")
    builder.OUT = OUT
    if not args.no_word:
        print("supplement:", builder.word_pass(docx, "Supplementary material", ""))
    builder.check_masked(docx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
