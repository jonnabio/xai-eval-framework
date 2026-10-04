#!/usr/bin/env python3
"""Paper E post hoc diagnostics (ANALYSIS_PLAN.md section 9, deviation of 2026-10-03).

These analyses were added AFTER the prespecified results were inspected. They do not
replace any prespecified estimate; they explain one of them (sign agreement).

Reads   outputs/analysis/paper_e/analysis/instance_agreement.csv  (prespecified output)
        the SHAP and LIME run files behind it
Writes  outputs/analysis/paper_e/posthoc/
          sign_by_predicted_class_runs.csv     run-level mean sign agreement per predicted class
          sign_by_predicted_class_summary.csv  group estimates, seed-clustered 95% intervals
          sign_constancy_runs.csv              per run and method: how constant a feature's sign is
          sign_constancy_summary.csv           group means of the above
          chance_overlap.csv                   expected top-k Jaccard of two random k-subsets
          manifest.json

Standard library and NumPy only.

    python docs/reports/paper_e/scripts/paper_e_posthoc.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
ANALYSIS = ROOT / "outputs" / "analysis" / "paper_e" / "analysis"
LIME_EXP3 = ROOT / "outputs" / "analysis" / "paper_e" / "exp3_lime"
OUT = ROOT / "outputs" / "analysis" / "paper_e" / "posthoc"

BOOTSTRAP_REPS = 2000
BOOTSTRAP_SEED = 20261003  # same as the prespecified analysis
MIN_FEATURE_INSTANCES = 10  # a feature enters the constancy measure with at least this many nonzero values in a run

# Encoded feature counts. Adult: the LIME runs return 10 of p features and record
# sparsity 10/p = 0.0926, so p = 108. EXP3: length of `feature_names` in the run metadata.
N_FEATURES = {"exp2_adult": 108, "german_credit": 61, "breast_cancer": 30}


def run_path(dataset: str, model: str, seed: str, intensity: str, method: str) -> Path:
    if dataset == "exp2_adult":
        return (ROOT / "experiments" / "exp2_scaled" / "results" / f"{model}_{method}"
                / f"seed_{seed}" / intensity / "results.json")
    if method == "lime":
        return LIME_EXP3 / dataset / model / f"seed_{seed}" / "results.json"
    return (ROOT / "experiments" / "exp3_cross_dataset" / "results" / dataset
            / f"{model}_{method}" / f"seed_{seed}" / "n_100" / "results.json")


def bootstrap(seed_values: dict[str, list[float]], rng: np.random.Generator):
    """Seed-clustered percentile interval over run-level means (plan section 5)."""
    seeds = sorted(seed_values)
    if len(seeds) < 2:
        return None, None
    est = np.empty(BOOTSTRAP_REPS)
    for i in range(BOOTSTRAP_REPS):
        sampled = rng.choice(seeds, size=len(seeds), replace=True)
        est[i] = np.mean([v for s in sampled for v in seed_values[str(s)]])
    low, high = np.quantile(est, [0.025, 0.975])
    return float(low), float(high)


def expected_random_jaccard(p: int, k: int) -> float:
    """Expected Jaccard of two independent uniform random k-subsets of p features."""
    total = math.comb(p, k)
    return sum(
        math.comb(k, i) * math.comb(p - k, k - i) / total * (i / (2 * k - i))
        for i in range(0, k + 1)
        if p - k >= k - i
    )


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    source = ANALYSIS / "instance_agreement.csv"
    with source.open(encoding="utf-8") as fh:
        instances = list(csv.DictReader(fh))

    # --- 1. sign agreement by predicted class ---------------------------------
    by_run: dict[tuple, list[float]] = defaultdict(list)
    paired_ids: dict[tuple, set[str]] = defaultdict(set)
    for row in instances:
        block = (row["dataset"], row["model"], row["seed"], row["intensity"])
        paired_ids[block].add(row["instance_id"])
        if row["sign_agreement"] != "":
            by_run[block + (row["prediction"],)].append(float(row["sign_agreement"]))
    run_rows = [
        {"dataset": d, "model": m, "seed": s, "intensity": i, "predicted_class": c,
         "n_instances": len(v), "sign_agreement_mean": float(np.mean(v))}
        for (d, m, s, i, c), v in sorted(by_run.items())
    ]
    write_csv(OUT / "sign_by_predicted_class_runs.csv", run_rows, list(run_rows[0]))

    summary = []
    for scope in ("model", "all"):
        groups: dict[tuple, list[dict]] = defaultdict(list)
        for r in run_rows:
            groups[(r["dataset"], r["model"] if scope == "model" else "all",
                    r["predicted_class"])].append(r)
        for (d, m, c), rows in sorted(groups.items()):
            seed_values: dict[str, list[float]] = defaultdict(list)
            for r in rows:
                seed_values[r["seed"]].append(r["sign_agreement_mean"])
            low, high = bootstrap(seed_values, rng)
            summary.append({
                "dataset": d, "model": m, "predicted_class": c,
                "estimate_mean_of_run_means": float(np.mean([r["sign_agreement_mean"] for r in rows])),
                "ci95_low": low, "ci95_high": high,
                "n_runs": len(rows), "n_seeds": len(seed_values),
                "n_instances": sum(r["n_instances"] for r in rows),
            })
    write_csv(OUT / "sign_by_predicted_class_summary.csv", summary, list(summary[0]))

    # --- 2. sign constancy: is a feature's sign the same for every instance? --
    # For each run and method, and each feature with a nonzero top-10 value in at least
    # MIN_FEATURE_INSTANCES paired instances: the share of those instances carrying the
    # feature's majority sign. 0.5 = the sign follows the instance; 1.0 = it never changes.
    constancy_rows = []
    hashes = {}
    for block in sorted(paired_ids):
        d, m, s, i = block
        for method in ("shap", "lime"):
            path = run_path(d, m, s, i, method)
            hashes[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
            run = json.loads(path.read_text(encoding="utf-8"))
            signs: dict[str, list[int]] = defaultdict(list)
            for ev in run["instance_evaluations"]:
                if str(ev.get("instance_id")) not in paired_ids[block]:
                    continue
                top = (ev.get("explanation") or {}).get("raw_top") or {}
                for feature, value in top.items():
                    if value:
                        signs[feature].append(1 if value > 0 else -1)
            shares, weights = [], []
            for values in signs.values():
                if len(values) >= MIN_FEATURE_INSTANCES:
                    positive = sum(v > 0 for v in values)
                    shares.append(max(positive, len(values) - positive) / len(values))
                    weights.append(len(values))
            constancy_rows.append({
                "dataset": d, "model": m, "seed": s, "intensity": i, "method": method,
                "n_features": len(shares),
                "majority_sign_share_mean": float(np.mean(shares)) if shares else "",
                "majority_sign_share_weighted": float(np.average(shares, weights=weights)) if shares else "",
            })
    write_csv(OUT / "sign_constancy_runs.csv", constancy_rows, list(constancy_rows[0]))

    constancy_summary = []
    for scope in ("model", "all"):
        groups = defaultdict(list)
        for r in constancy_rows:
            if r["majority_sign_share_weighted"] != "":
                groups[(r["dataset"], r["model"] if scope == "model" else "all", r["method"])].append(r)
        for (d, m, method), rows in sorted(groups.items()):
            seed_values = defaultdict(list)
            for r in rows:
                seed_values[r["seed"]].append(r["majority_sign_share_weighted"])
            low, high = bootstrap(seed_values, rng)
            constancy_summary.append({
                "dataset": d, "model": m, "method": method,
                "estimate_mean_of_run_means": float(np.mean([r["majority_sign_share_weighted"] for r in rows])),
                "ci95_low": low, "ci95_high": high,
                "n_runs": len(rows), "n_seeds": len(seed_values),
            })
    write_csv(OUT / "sign_constancy_summary.csv", constancy_summary, list(constancy_summary[0]))

    # --- 3. chance reference for the overlap measures --------------------------
    chance = [
        {"dataset": d, "n_features": p,
         "expected_top5_jaccard": expected_random_jaccard(p, 5),
         "expected_top10_jaccard": expected_random_jaccard(p, 10)}
        for d, p in N_FEATURES.items()
    ]
    write_csv(OUT / "chance_overlap.csv", chance, list(chance[0]))

    # --- 4. group summary of the prespecified secondary feature-set overlaps ----
    # Not a new measure: the plan's section 5 aggregation (mean of run means, seed-clustered
    # interval) applied to secondary_run_summary.csv, which the analysis script left per run.
    with (ANALYSIS / "secondary_run_summary.csv").open(encoding="utf-8") as fh:
        secondary_runs = [r for r in csv.DictReader(fh) if r["mean_jaccard"] != ""]
    secondary = []
    for scope in ("model", "all"):
        groups = defaultdict(list)
        for r in secondary_runs:
            groups[(r["method_pair"], r["model"] if scope == "model" else "all")].append(r)
        for (pair, m), rows in sorted(groups.items()):
            seed_values = defaultdict(list)
            for r in rows:
                seed_values[r["seed"]].append(float(r["mean_jaccard"]))
            low, high = bootstrap(seed_values, rng)
            secondary.append({
                "method_pair": pair, "model": m,
                "estimate_mean_of_run_means": float(np.mean([float(r["mean_jaccard"]) for r in rows])),
                "ci95_low": low, "ci95_high": high,
                "n_runs": len(rows), "n_seeds": len(seed_values),
                "n_instances": sum(int(r["n_defined_jaccard"]) for r in rows),
            })
    write_csv(OUT / "secondary_group_summary.csv", secondary, list(secondary[0]))

    # --- 5. Adult agreement pooled over intensity (per model) and over model (per intensity)
    # The analysis script reports Adult per (model, intensity) and overall. These two
    # margins use the same aggregation on run_agreement_summary.csv.
    with (ANALYSIS / "run_agreement_summary.csv").open(encoding="utf-8") as fh:
        adult_runs = [r for r in csv.DictReader(fh) if r["dataset"] == "exp2_adult"]
    margins = []
    for label, key in (("model", lambda r: (r["model"], "all")),
                       ("intensity", lambda r: ("all", r["intensity"]))):
        groups = defaultdict(list)
        for r in adult_runs:
            groups[key(r)].append(r)
        for (m, i), rows in sorted(groups.items()):
            for metric in ("top5_jaccard", "top10_jaccard", "kendall_tau_b", "sign_agreement"):
                seed_values = defaultdict(list)
                for r in rows:
                    if r[f"{metric}_mean"] != "":
                        seed_values[r["seed"]].append(float(r[f"{metric}_mean"]))
                values = [v for vs in seed_values.values() for v in vs]
                low, high = bootstrap(seed_values, rng)
                margins.append({
                    "dataset": "exp2_adult", "model": m, "intensity": i, "margin": label,
                    "metric": metric, "estimate_mean_of_run_means": float(np.mean(values)),
                    "ci95_low": low, "ci95_high": high, "n_runs": len(values),
                    "n_seeds": len(seed_values),
                    "n_instances": sum(int(r["n_instances"]) for r in rows),
                })
    write_csv(OUT / "adult_margin_summary.csv", margins, list(margins[0]))

    (OUT / "manifest.json").write_text(json.dumps({
        "experiment": "paper_e_posthoc",
        "status": "post hoc; see ANALYSIS_PLAN.md section 9 (2026-10-03)",
        "script": "docs/reports/paper_e/scripts/paper_e_posthoc.py",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_sha256": {"outputs/analysis/paper_e/analysis/instance_agreement.csv":
                         hashlib.sha256(source.read_bytes()).hexdigest(), **hashes},
        "bootstrap_replicates": BOOTSTRAP_REPS, "bootstrap_seed": BOOTSTRAP_SEED,
        "min_feature_instances": MIN_FEATURE_INSTANCES, "n_features": N_FEATURES,
        "numpy": np.__version__,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
