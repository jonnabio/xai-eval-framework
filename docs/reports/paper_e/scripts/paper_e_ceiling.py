#!/usr/bin/env python3
"""Paper E post hoc: how much does each explainer agree with itself?

ANALYSIS_PLAN.md section 9, deviation of 2026-10-04 (rigor review finding F01). The
overlap between SHAP and LIME was compared with chance and with identity. Its real upper
reference is what each method reproduces of itself when it is run again on the same
instance and model with another random state. This script measures that.

For a subsample of the paired instances of each run it explains every instance twice with
LIME and twice with SHAP, using the repository wrappers and the settings of the stored
runs (LIME: 1000 samples, kernel width 3, ten features, no discretisation; SHAP: TreeSHAP
interventional on the probability scale for RF and XGB, KernelSHAP otherwise, 50
background instances). The two repetitions differ only in the random state (LIME
perturbations; SHAP background sample and KernelSHAP coalition sampling). Agreement between
the two repetitions is computed with the prespecified function
(scripts/analyze_paper_e.py::primary_agreement), and so is SHAP-LIME agreement of the
stored explanations on the same subsample.

An instance enters only if the loaded model reproduces its stored prediction.

Adult uses the model binaries in experiments/exp1_adult/models/. The EXP3 binaries are not
tracked: regenerate them first, as for the Paper E LIME cohort,
    python scripts/train_exp3_models.py --model-root <dir> --data-cache-dir data
and pass --exp3-model-root <dir>.

Writes  outputs/analysis/paper_e/posthoc/
          ceiling_instances.csv   one row per instance
          ceiling_runs.csv        run means
          ceiling_summary.csv     group estimates (mean of run means, seed-clustered interval)

    python docs/reports/paper_e/scripts/paper_e_ceiling.py --exp3-model-root <dir>
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
import time
import warnings
from collections import defaultdict
from pathlib import Path

import joblib
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_paper_e import primary_agreement  # noqa: E402
from paper_e_posthoc import ANALYSIS, BOOTSTRAP_SEED, OUT, bootstrap, run_path, write_csv  # noqa: E402
from paper_e_sign_contribution import split  # noqa: E402

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

RANDOM_STATES = (1001, 2002)   # the two repetitions
ADULT_INTENSITY = "n_100"
# Adult. The SVM is left out: KernelSHAP on it takes about two minutes per explanation, and
# its stored SHAP runs cover only 29% of the instances.
PER_RUN = {"logreg": 20, "mlp": 20, "rf": 20, "xgb": 20}
PER_RUN_EXP3 = 30
TREE = {"rf", "xgb"}
METRICS = ("top5_jaccard", "top10_jaccard", "kendall_tau_b")
PAIRS = ("lime_lime", "shap_shap", "shap_lime_stored", "lime_rerun_vs_stored", "shap_rerun_vs_stored")


def load_model(dataset: str, model: str, seed: str, exp3_root: Path | None):
    if dataset == "exp2_adult":
        path = ROOT / "experiments" / "exp1_adult" / "models" / f"{model}.joblib"
    else:
        path = exp3_root / dataset / model / f"seed_{seed}" / f"{model}.joblib"
    loaded = joblib.load(path)
    return getattr(loaded, "model", loaded)


def top10(vector: np.ndarray, names: list[str]) -> dict[str, float]:
    """Same rule as runner.py::_format_explanation: ten largest absolute values, in order."""
    pairs = sorted(((names[i], float(v)) for i, v in enumerate(vector)), key=lambda p: abs(p[1]), reverse=True)
    return dict(pairs[:10])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp3-model-root", type=Path)
    ap.add_argument("--only", nargs="*", help="restrict to dataset:model pairs, e.g. exp2_adult:svm")
    ap.add_argument("--append", action="store_true", help="keep rows already in ceiling_instances.csv")
    args = ap.parse_args()

    from src.xai.lime_tabular import LIMETabularWrapper
    from src.xai.shap_tabular import SHAPTabularWrapper

    with (ANALYSIS / "instance_agreement.csv").open(encoding="utf-8") as fh:
        instances = list(csv.DictReader(fh))
    blocks: dict[tuple, list[dict]] = defaultdict(list)
    for row in instances:
        if row["dataset"] == "exp2_adult" and row["intensity"] != ADULT_INTENSITY:
            continue
        blocks[(row["dataset"], row["model"], row["seed"], row["intensity"])].append(row)

    out_path = OUT / "ceiling_instances.csv"
    rows: list[dict] = []
    if args.append and out_path.exists():
        with out_path.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
    done = {(r["dataset"], r["model"], r["seed"]) for r in rows}

    for block in sorted(blocks):
        dataset, model, seed, intensity = block
        if args.only and f"{dataset}:{model}" not in args.only:
            continue
        if (dataset, model, seed) in done:
            continue
        if dataset != "exp2_adult" and args.exp3_model_root is None:
            continue
        if dataset == "exp2_adult" and model not in PER_RUN:
            continue
        started = time.time()
        x_train, x_test, _, names = split(dataset, seed)
        clf = load_model(dataset, model, seed, args.exp3_model_root)
        stored = {m: {str(e["instance_id"]): e for e in json.loads(
            run_path(dataset, model, seed, intensity, m).read_text(encoding="utf-8"))["instance_evaluations"]}
            for m in ("shap", "lime")}

        k = PER_RUN[model] if dataset == "exp2_adult" else PER_RUN_EXP3
        rng = np.random.default_rng([BOOTSTRAP_SEED, int(seed), sum(map(ord, dataset + model))])
        candidates = sorted(blocks[block], key=lambda r: int(r["instance_id"]))
        chosen = [candidates[i] for i in rng.permutation(len(candidates))]

        limes = [LIMETabularWrapper(training_data=x_train, feature_names=names, num_features=10, num_samples=1000,
                                    kernel_width=3.0, random_state=state) for state in RANDOM_STATES]
        shaps = [SHAPTabularWrapper(model=clf, training_data=x_train, feature_names=names,
                                    model_type="tree" if model in TREE else "kernel",
                                    n_background_samples=50, random_state=state) for state in RANDOM_STATES]
        kept = skipped = 0
        for row in chosen:
            if kept == k:
                break
            x = x_test[int(row["instance_id"])]
            if int(clf.predict(x.reshape(1, -1))[0]) != int(float(row["prediction"])):
                skipped += 1
                continue
            lime_runs = []
            for state, wrapper in zip(RANDOM_STATES, limes):
                lime_runs.append(top10(wrapper.explain_instance(clf, x, return_full=False), names))
            shap_runs = []
            for state, wrapper in zip(RANDOM_STATES, shaps):
                np.random.seed(state + int(row["instance_id"]))   # KernelSHAP samples coalitions from the global RNG
                shap_runs.append(top10(wrapper.generate_explanations(clf, x.reshape(1, -1))["feature_importance"][0], names))
            stored_shap = stored["shap"][row["instance_id"]]["explanation"]["raw_top"]
            stored_lime = stored["lime"][row["instance_id"]]["explanation"]["raw_top"]
            compared = {
                "lime_lime": primary_agreement(lime_runs[0], lime_runs[1]),
                "shap_shap": primary_agreement(shap_runs[0], shap_runs[1]),
                "shap_lime_stored": primary_agreement(stored_shap, stored_lime),
                "lime_rerun_vs_stored": primary_agreement(lime_runs[0], stored_lime),
                "shap_rerun_vs_stored": primary_agreement(shap_runs[0], stored_shap),
            }
            out = {"dataset": dataset, "model": model, "seed": seed, "intensity": intensity,
                   "instance_id": row["instance_id"], "prediction": row["prediction"]}
            for pair, values in compared.items():
                for metric in METRICS:
                    out[f"{pair}.{metric}"] = "" if values[metric] is None else values[metric]
            rows.append(out)
            kept += 1
        write_csv(out_path, rows, list(rows[0]))
        print(f"{dataset} {model} seed {seed}: {kept} instances, {skipped} skipped (prediction not reproduced), "
              f"{time.time() - started:.0f} s", flush=True)

    summarise(rows)


def summarise(rows: list[dict]) -> None:
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    by_run: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        by_run[(r["dataset"], r["model"], r["seed"])].append(r)
    run_rows = []
    for (dataset, model, seed), items in sorted(by_run.items()):
        out = {"dataset": dataset, "model": model, "seed": seed, "n_instances": len(items)}
        for pair in PAIRS:
            for metric in METRICS:
                values = [float(i[f"{pair}.{metric}"]) for i in items if i[f"{pair}.{metric}"] != ""]
                out[f"{pair}.{metric}"] = float(np.mean(values)) if values else ""
        run_rows.append(out)
    write_csv(OUT / "ceiling_runs.csv", run_rows, list(run_rows[0]))

    summary = []
    for scope in ("model", "all"):
        groups: dict[tuple, list[dict]] = defaultdict(list)
        for r in run_rows:
            groups[(r["dataset"], r["model"] if scope == "model" else "all")].append(r)
        for (dataset, model), items in sorted(groups.items()):
            for pair in PAIRS:
                for metric in METRICS:
                    seed_values: dict[str, list[float]] = defaultdict(list)
                    for r in items:
                        if r[f"{pair}.{metric}"] != "":
                            seed_values[r["seed"]].append(r[f"{pair}.{metric}"])
                    values = [v for vs in seed_values.values() for v in vs]
                    if not values:
                        continue
                    low, high = bootstrap(seed_values, rng)
                    summary.append({
                        "dataset": dataset, "model": model, "pair": pair, "metric": metric,
                        "estimate_mean_of_run_means": float(np.mean(values)),
                        "ci95_low": low, "ci95_high": high, "n_runs": len(values),
                        "n_seeds": len(seed_values), "n_instances": sum(int(r["n_instances"]) for r in items),
                    })
    write_csv(OUT / "ceiling_summary.csv", summary, list(summary[0]))
    print(f"wrote {OUT.relative_to(ROOT)}/ceiling_*.csv")


if __name__ == "__main__":
    main()
