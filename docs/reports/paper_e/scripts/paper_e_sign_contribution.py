#!/usr/bin/env python3
"""Paper E post hoc test: sign agreement after LIME slopes are turned into contributions.

ANALYSIS_PLAN.md section 9, deviation of 2026-10-04. The prespecified sign agreement
compares the sign of a SHAP value (a contribution relative to the expected output) with the
sign of a LIME coefficient. LIME was run with discretize_continuous=False, so that
coefficient is the slope w_j of the local linear model on LIME's standardised scale
z_j = (x_j - m_j) / s_j, where m and s are the mean and the standard deviation of the
training data given to LIME. The contribution of feature j to the local model's output,
relative to the training mean, is w_j * z_j, and its sign is sign(w_j) * sign(x_j - m_j).

If the two methods disagree about the direction of effects, sign agreement stays low after
this conversion. If the low prespecified value only reflects the two quantities, it rises
and no longer depends on the predicted class.

The instance values are not stored in the runs. They are reloaded with the loaders the
runs used, and the alignment is checked before anything is computed:
  - the stored true label of every paired instance equals y_test[instance_id];
  - for the two EXP3 datasets, the SHA-256 of the reloaded train and test arrays equals the
    hash recorded in the Paper E LIME run.
A block that fails a check is excluded and reported.

Reads   outputs/analysis/paper_e/analysis/instance_agreement.csv, the SHAP and LIME runs,
        data/ (Adult, German Credit), experiments/exp1_adult/models/preprocessor.joblib
Writes  outputs/analysis/paper_e/posthoc/
          sign_contribution_runs.csv      per run and predicted class
          sign_contribution_summary.csv   group estimates, seed-clustered 95% intervals
          sign_contribution_checks.csv    alignment checks per block

    python docs/reports/paper_e/scripts/paper_e_sign_contribution.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import logging
import sys
import warnings
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paper_e_posthoc import ANALYSIS, BOOTSTRAP_SEED, OUT, bootstrap, run_path, write_csv  # noqa: E402

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)


def sha256_array(values: np.ndarray) -> str:
    """Same hash as scripts/run_exp3_lime.py::_sha256_array."""
    return hashlib.sha256(np.ascontiguousarray(values).view(np.uint8)).hexdigest()


_splits: dict[tuple[str, str], tuple] = {}


def split(dataset: str, seed: str):
    """(X_train, X_test, y_test, feature_names) as the runs loaded them."""
    key = (dataset, seed)
    if key not in _splits:
        if dataset == "exp2_adult":
            import joblib
            from src.data_loading.adult import load_adult
            pre = joblib.load(ROOT / "experiments" / "exp1_adult" / "models" / "preprocessor.joblib")
            x_tr, x_te, _, y_te, names, _ = load_adult(
                cache_dir=str(ROOT / "data"), random_state=int(seed), preprocessor=pre, verbose=False)
        else:
            from src.data_loading.cross_dataset import load_tabular_dataset
            x_tr, x_te, _, y_te, names, _ = load_tabular_dataset(
                dataset, cache_dir=str(ROOT / "data"), random_state=int(seed))
        _splits[key] = (np.asarray(x_tr, dtype=float), np.asarray(x_te, dtype=float),
                        np.asarray(y_te), list(names))
    return _splits[key]


def main() -> None:
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    with (ANALYSIS / "instance_agreement.csv").open(encoding="utf-8") as fh:
        instances = list(csv.DictReader(fh))
    blocks: dict[tuple, dict[str, dict]] = defaultdict(dict)
    for row in instances:
        blocks[(row["dataset"], row["model"], row["seed"], row["intensity"])][row["instance_id"]] = row

    checks, run_rows = [], []
    for block in sorted(blocks):
        dataset, model, seed, intensity = block
        x_train, x_test, y_test, names = split(dataset, seed)
        column = {name: k for k, name in enumerate(names)}
        mean = x_train.mean(axis=0)
        runs = {m: json.loads(run_path(dataset, model, seed, intensity, m).read_text(encoding="utf-8"))
                for m in ("shap", "lime")}
        by_id = {m: {str(e["instance_id"]): e for e in runs[m]["instance_evaluations"]} for m in runs}

        paired = blocks[block]
        label_ok = sum(int(y_test[int(i)]) == int(float(r["true_label"])) for i, r in paired.items())
        check = {"dataset": dataset, "model": model, "seed": seed, "intensity": intensity,
                 "paired_instances": len(paired), "labels_matching": label_ok,
                 "train_hash_matches": "", "test_hash_matches": ""}
        if dataset != "exp2_adult":
            meta = runs["lime"]["experiment_metadata"]
            check["train_hash_matches"] = sha256_array(x_train) == meta["train_features_sha256"]
            check["test_hash_matches"] = sha256_array(x_test) == meta["test_features_sha256"]
        aligned = label_ok == len(paired) and check["train_hash_matches"] in ("", True) \
            and check["test_hash_matches"] in ("", True)
        check["included"] = aligned
        checks.append(check)
        if not aligned:
            continue

        per_class: dict[str, dict[str, list]] = defaultdict(lambda: {"slope": [], "contribution": [], "at_mean": 0})
        for instance_id, row in paired.items():
            shap = by_id["shap"][instance_id]["explanation"]["raw_top"]
            lime = by_id["lime"][instance_id]["explanation"]["raw_top"]
            shared = [f for f in list(shap)[:5] if f in list(lime)[:5] and shap[f] != 0 and lime[f] != 0]
            x = x_test[int(instance_id)]
            slope_same, contribution_same, usable = 0, 0, 0
            for feature in shared:
                deviation = x[column[feature]] - mean[column[feature]]
                if deviation == 0:
                    per_class[row["prediction"]]["at_mean"] += 1
                    continue
                usable += 1
                slope_same += (shap[feature] > 0) == (lime[feature] > 0)
                contribution_same += (shap[feature] > 0) == (lime[feature] * deviation > 0)
            if usable:
                per_class[row["prediction"]]["slope"].append(slope_same / usable)
                per_class[row["prediction"]]["contribution"].append(contribution_same / usable)
        for predicted_class in ("0", "1", "all"):
            if predicted_class == "all":
                slope = [v for c in per_class.values() for v in c["slope"]]
                contribution = [v for c in per_class.values() for v in c["contribution"]]
                at_mean = sum(c["at_mean"] for c in per_class.values())
            elif predicted_class in per_class:
                slope, contribution = per_class[predicted_class]["slope"], per_class[predicted_class]["contribution"]
                at_mean = per_class[predicted_class]["at_mean"]
            else:
                continue
            if slope:
                run_rows.append({
                    "dataset": dataset, "model": model, "seed": seed, "intensity": intensity,
                    "predicted_class": predicted_class, "n_instances": len(slope),
                    "sign_agreement_slope_mean": float(np.mean(slope)),
                    "sign_agreement_contribution_mean": float(np.mean(contribution)),
                    "features_at_training_mean": at_mean,
                })
    write_csv(OUT / "sign_contribution_checks.csv", checks, list(checks[0]))
    write_csv(OUT / "sign_contribution_runs.csv", run_rows, list(run_rows[0]))

    summary = []
    for scope in ("model", "all"):
        groups: dict[tuple, list[dict]] = defaultdict(list)
        for r in run_rows:
            groups[(r["dataset"], r["model"] if scope == "model" else "all", r["predicted_class"])].append(r)
        for (dataset, model, predicted_class), rows in sorted(groups.items()):
            out = {"dataset": dataset, "model": model, "predicted_class": predicted_class}
            for quantity in ("slope", "contribution"):
                seed_values: dict[str, list[float]] = defaultdict(list)
                for r in rows:
                    seed_values[r["seed"]].append(r[f"sign_agreement_{quantity}_mean"])
                low, high = bootstrap(seed_values, rng)
                out[f"{quantity}_estimate_mean_of_run_means"] = float(
                    np.mean([r[f"sign_agreement_{quantity}_mean"] for r in rows]))
                out[f"{quantity}_ci95_low"], out[f"{quantity}_ci95_high"] = low, high
            out["n_runs"] = len(rows)
            out["n_seeds"] = len({r["seed"] for r in rows})
            out["n_instances"] = sum(r["n_instances"] for r in rows)
            summary.append(out)
    write_csv(OUT / "sign_contribution_summary.csv", summary, list(summary[0]))
    excluded = [c for c in checks if not c["included"]]
    print(f"blocks: {len(checks)}, excluded by an alignment check: {len(excluded)}")
    for c in excluded:
        print("  excluded:", c)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
