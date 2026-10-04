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

An instance enters only if the loaded model reproduces its stored prediction; the number of
candidates skipped for this reason is written per run.

Additions of the second review (ANALYSIS_PLAN.md section 9, second entry of 2026-10-04):
  - the top-10 lists of every repetition are saved, so that every measure below can be
    recomputed without running an explainer;
  - SHAP-LIME agreement between the new runs (mean of the four pairs of one SHAP and one
    LIME repetition), which puts self-agreement and agreement between the methods on the
    same runs and the same model binary;
  - LIME with the default kernel width of the package (0.75 * sqrt(number of features)),
    twice, all other settings unchanged;
  - a permutation reference: each pair is also computed between an instance and every other
    instance of the same run (pair name with the suffix _other).

Adult uses the model binaries in experiments/exp1_adult/models/. The EXP3 binaries are not
tracked: regenerate them first, as for the Paper E LIME cohort,
    python scripts/train_exp3_models.py --model-root <dir> --data-cache-dir data
and pass --exp3-model-root <dir>.

Writes  outputs/analysis/paper_e/posthoc/
          ceiling_lists.json      the top-10 lists of every repetition, per instance
          ceiling_skipped.csv     candidates skipped per run (stored prediction not reproduced)
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
# name: the lists compared; several pairs of lists are averaged
PAIRS = {
    "lime_lime": [("lime_a", "lime_b")],
    "shap_shap": [("shap_a", "shap_b")],
    "shap_lime_stored": [("stored_shap", "stored_lime")],
    "lime_rerun_vs_stored": [("lime_a", "stored_lime")],
    "shap_rerun_vs_stored": [("shap_a", "stored_shap")],
    "shap_lime_rerun": [(a, b) for a in ("shap_a", "shap_b") for b in ("lime_a", "lime_b")],
    "limed_limed": [("limed_a", "limed_b")],
    "shap_limed_rerun": [(a, b) for a in ("shap_a", "shap_b") for b in ("limed_a", "limed_b")],
    "lime_limed": [(a, b) for a in ("lime_a", "lime_b") for b in ("limed_a", "limed_b")],
}
# pairs that also get the permutation reference (an instance against another of its run)
PERMUTED = ("lime_lime", "shap_shap", "shap_lime_stored", "shap_lime_rerun", "limed_limed", "shap_limed_rerun")


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
    ap.add_argument("--append", action="store_true", help="keep the instances already in ceiling_lists.json")
    ap.add_argument("--summarise-only", action="store_true", help="recompute the CSV files from ceiling_lists.json")
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

    lists_path, skipped_path = OUT / "ceiling_lists.json", OUT / "ceiling_skipped.csv"
    entries: list[dict] = []
    skipped_rows: list[dict] = []
    if (args.append or args.summarise_only) and lists_path.exists():
        entries = json.loads(lists_path.read_text(encoding="utf-8"))
        with skipped_path.open(encoding="utf-8") as fh:
            skipped_rows = list(csv.DictReader(fh))
    if args.summarise_only:
        summarise(entries)
        return
    done = {(r["dataset"], r["model"], r["seed"]) for r in entries}

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
        # LIME with the default kernel width of the package (kernel_width=None)
        limes_default = [LIMETabularWrapper(training_data=x_train, feature_names=names, num_features=10,
                                            num_samples=1000, kernel_width=None, random_state=state)
                         for state in RANDOM_STATES]
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
            default_runs = [top10(wrapper.explain_instance(clf, x, return_full=False), names)
                            for wrapper in limes_default]
            entries.append({
                "dataset": dataset, "model": model, "seed": seed, "intensity": intensity,
                "instance_id": row["instance_id"], "prediction": row["prediction"],
                "lime_a": lime_runs[0], "lime_b": lime_runs[1], "shap_a": shap_runs[0], "shap_b": shap_runs[1],
                "limed_a": default_runs[0], "limed_b": default_runs[1],
                "stored_shap": stored["shap"][row["instance_id"]]["explanation"]["raw_top"],
                "stored_lime": stored["lime"][row["instance_id"]]["explanation"]["raw_top"],
            })
            kept += 1
        skipped_rows.append({"dataset": dataset, "model": model, "seed": seed, "kept": kept, "skipped": skipped})
        lists_path.write_text(json.dumps(entries, indent=0), encoding="utf-8", newline="\n")
        write_csv(skipped_path, skipped_rows, list(skipped_rows[0]))
        print(f"{dataset} {model} seed {seed}: {kept} instances, {skipped} skipped (prediction not reproduced), "
              f"{time.time() - started:.0f} s", flush=True)

    summarise(entries)


def compare(first: dict, second: dict, pair: str) -> dict[str, float | str]:
    """Measures of a pair between the lists of two entries (the same entry for a paired value)."""
    values: dict[str, list[float]] = {metric: [] for metric in METRICS}
    for left, right in PAIRS[pair]:
        result = primary_agreement(first[left], second[right])
        for metric in METRICS:
            if result[metric] is not None:
                values[metric].append(result[metric])
    return {metric: float(np.mean(v)) if v else "" for metric, v in values.items()}


def summarise(entries: list[dict]) -> None:
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    rows = []
    for e in entries:
        out = {k: e[k] for k in ("dataset", "model", "seed", "intensity", "instance_id", "prediction")}
        for pair in PAIRS:
            for metric, value in compare(e, e, pair).items():
                out[f"{pair}.{metric}"] = value
        rows.append(out)
    write_csv(OUT / "ceiling_instances.csv", rows, list(rows[0]))

    by_run: dict[tuple, list[int]] = defaultdict(list)
    for k, e in enumerate(entries):
        by_run[(e["dataset"], e["model"], e["seed"])].append(k)
    names = list(PAIRS) + [f"{pair}_other" for pair in PERMUTED]
    run_rows = []
    for (dataset, model, seed), index in sorted(by_run.items()):
        out = {"dataset": dataset, "model": model, "seed": seed, "n_instances": len(index)}
        for pair in PAIRS:
            for metric in METRICS:
                values = [float(rows[k][f"{pair}.{metric}"]) for k in index if rows[k][f"{pair}.{metric}"] != ""]
                out[f"{pair}.{metric}"] = float(np.mean(values)) if values else ""
        # permutation reference: an instance against every other instance of the run
        for pair in PERMUTED:
            other: dict[str, list[float]] = {metric: [] for metric in METRICS}
            for i in index:
                for j in index:
                    if i != j:
                        for metric, value in compare(entries[i], entries[j], pair).items():
                            if value != "":
                                other[metric].append(value)
            for metric in METRICS:
                out[f"{pair}_other.{metric}"] = float(np.mean(other[metric])) if other[metric] else ""
        run_rows.append(out)
    write_csv(OUT / "ceiling_runs.csv", run_rows, list(run_rows[0]))

    summary = []
    for scope in ("model", "all"):
        groups: dict[tuple, list[dict]] = defaultdict(list)
        for r in run_rows:
            groups[(r["dataset"], r["model"] if scope == "model" else "all")].append(r)
        for (dataset, model), items in sorted(groups.items()):
            for pair in names:
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
