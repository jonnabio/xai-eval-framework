#!/usr/bin/env python3
"""Paper E post hoc analyses added in response to the rigor review of 2026-10-04.

ANALYSIS_PLAN.md section 9, deviation of 2026-10-04 (review findings F02, F03, F06, F07,
F09, F10). All are re-cuts of the stored explanations; no explainer is run.

  1. majority_sign      F02  Baseline for the converted sign agreement: replace the sign of
                             every LIME slope by the majority sign of that feature's slope
                             in the same run, convert to a contribution, compare with SHAP.
                             It uses no instance-level information from LIME.
  2. shared_features    F10  Mean number of shared non-zero top-5 features (the denominator
                             of sign agreement).
  3. rerank             F07  Top-5 overlap and Kendall tau-b after LIME's ten stored features
                             are re-ranked by the absolute contribution |w_j (x_j - m_j)/s_j|.
  4. shared_tau         F06  Kendall tau-b on the features present in both top-10 lists only
                             (no rank 11 for absent features).
  5. heldout            F03  Adult: share of paired instances that are rows of the model's
                             training data (seed-42 partition), and the correct-versus-
                             misclassified contrast on held-out rows only.
  6. coverage           F09  Paired instances as a share of the valid LIME instances, by model.

Aggregation is the plan's section 5: run means, mean of run means, seed-clustered percentile
bootstrap (2000 resamples, seed 20261003).

Writes outputs/analysis/paper_e/posthoc/review_*.csv

    python docs/reports/paper_e/scripts/paper_e_review_analyses.py
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import kendalltau

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_paper_e import primary_agreement  # noqa: E402
from paper_e_posthoc import ANALYSIS, BOOTSTRAP_SEED, OUT, bootstrap, run_path, write_csv  # noqa: E402
from paper_e_sign_contribution import split  # noqa: E402

MIN_GROUP = 10   # plan section 6: minimum matched instances per correctness group


def summarise(run_rows: list[dict], value_fields: list[str], keys: tuple[str, ...], rng) -> list[dict]:
    """Mean of run means and seed-clustered interval, per dataset/model and per dataset."""
    out = []
    for scope in ("model", "all"):
        groups: dict[tuple, list[dict]] = defaultdict(list)
        for r in run_rows:
            groups[(r["dataset"], r["model"] if scope == "model" else "all") + tuple(r[k] for k in keys)].append(r)
        for group, rows in sorted(groups.items()):
            row = {"dataset": group[0], "model": group[1], **dict(zip(keys, group[2:]))}
            for field in value_fields:
                seed_values: dict[str, list[float]] = defaultdict(list)
                for r in rows:
                    if r[field] != "":
                        seed_values[r["seed"]].append(float(r[field]))
                values = [v for vs in seed_values.values() for v in vs]
                low, high = bootstrap(seed_values, rng)
                row[f"{field}.estimate_mean_of_run_means"] = float(np.mean(values)) if values else ""
                row[f"{field}.ci95_low"], row[f"{field}.ci95_high"] = low, high
            row["n_runs"] = len(rows)
            row["n_seeds"] = len({r["seed"] for r in rows})
            out.append(row)
    return out


def mean(values: list[float]) -> float | str:
    return float(np.mean(values)) if values else ""


def main() -> None:
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    with (ANALYSIS / "instance_agreement.csv").open(encoding="utf-8") as fh:
        instances = list(csv.DictReader(fh))
    blocks: dict[tuple, dict[str, dict]] = defaultdict(dict)
    for row in instances:
        blocks[(row["dataset"], row["model"], row["seed"], row["intensity"])][row["instance_id"]] = row

    # rows of the Adult seed-42 training partition, to recognise training instances
    adult_train_rows = {r.tobytes() for r in np.ascontiguousarray(split("exp2_adult", "42")[0])}

    sign_runs, rank_runs, heldout_runs, membership_runs = [], [], [], []
    for block in sorted(blocks):
        dataset, model, seed, intensity = block
        x_train, x_test, _, names = split(dataset, seed)
        column = {name: k for k, name in enumerate(names)}
        mean_train = x_train.mean(axis=0)
        scale = x_train.std(axis=0)
        scale[scale == 0] = 1.0
        stored = {m: {str(e["instance_id"]): e for e in json.loads(
            run_path(dataset, model, seed, intensity, m).read_text(encoding="utf-8"))["instance_evaluations"]}
            for m in ("shap", "lime")}
        paired = blocks[block]

        # majority sign of each feature's LIME slope in this run
        signs: dict[str, int] = defaultdict(int)
        for instance_id in paired:
            for feature, value in stored["lime"][instance_id]["explanation"]["raw_top"].items():
                if value:
                    signs[feature] += 1 if value > 0 else -1

        converted, majority, shared_counts = [], [], []
        rerank_j5, rerank_tau, shared_tau = [], [], []
        groups = {True: {"train": [], "heldout": []}, False: {"train": [], "heldout": []}}
        for instance_id, row in paired.items():
            shap = stored["shap"][instance_id]["explanation"]["raw_top"]
            lime = stored["lime"][instance_id]["explanation"]["raw_top"]
            x = x_test[int(instance_id)]
            z = {f: (x[column[f]] - mean_train[column[f]]) / scale[column[f]] for f in lime}

            shared = [f for f in list(shap)[:5] if f in list(lime)[:5] and shap[f] != 0 and lime[f] != 0]
            shared_counts.append(len(shared))
            usable = [f for f in shared if z[f] != 0 and signs[f] != 0]
            if usable:
                converted.append(np.mean([(shap[f] > 0) == (lime[f] * z[f] > 0) for f in usable]))
                majority.append(np.mean([(shap[f] > 0) == (signs[f] * z[f] > 0) for f in usable]))

            # LIME's ten stored features re-ranked by absolute contribution
            contribution = dict(sorted(((f, lime[f] * z[f]) for f in lime), key=lambda p: abs(p[1]), reverse=True))
            again = primary_agreement(shap, contribution)
            rerank_j5.append(again["top5_jaccard"])
            if again["kendall_tau_b"] is not None:
                rerank_tau.append(again["kendall_tau_b"])

            # Kendall tau-b on the features present in both top-10 lists
            both = [f for f in shap if f in lime]
            if len(both) >= 2:
                tau = kendalltau([abs(shap[f]) for f in both], [abs(lime[f]) for f in both], variant="b").statistic
                if tau is not None and np.isfinite(tau):
                    shared_tau.append(float(tau))

            if dataset == "exp2_adult":
                where = "train" if np.ascontiguousarray(x).tobytes() in adult_train_rows else "heldout"
                groups[row["prediction_correct"] == "True"][where].append(float(row["top5_jaccard"]))

        base = {"dataset": dataset, "model": model, "seed": seed, "intensity": intensity}
        sign_runs.append({**base, "n_instances": len(converted),
                          "converted_sign_agreement": mean(converted),
                          "majority_sign_agreement": mean(majority),
                          "shared_nonzero_top5": mean(shared_counts)})
        rank_runs.append({**base, "n_instances": len(rerank_j5),
                          "reranked_top5_jaccard": mean(rerank_j5), "reranked_kendall_tau_b": mean(rerank_tau),
                          "shared_only_kendall_tau_b": mean(shared_tau), "n_shared_tau": len(shared_tau)})
        if dataset == "exp2_adult":
            n_train = len(groups[True]["train"]) + len(groups[False]["train"])
            n_all = n_train + len(groups[True]["heldout"]) + len(groups[False]["heldout"])
            correct_all = len(groups[True]["train"]) + len(groups[True]["heldout"])
            wrong_all = len(groups[False]["train"]) + len(groups[False]["heldout"])
            membership_runs.append({
                **base, "n_instances": n_all, "share_training_rows": n_train / n_all,
                "share_training_rows_correct": len(groups[True]["train"]) / correct_all if correct_all else "",
                "share_training_rows_misclassified": len(groups[False]["train"]) / wrong_all if wrong_all else ""})
            ok, wrong = groups[True]["heldout"], groups[False]["heldout"]
            included = len(ok) >= MIN_GROUP and len(wrong) >= MIN_GROUP
            heldout_runs.append({**base, "n_correct_heldout": len(ok), "n_misclassified_heldout": len(wrong),
                                 "included": included,
                                 "correct_mean": mean(ok), "misclassified_mean": mean(wrong),
                                 "misclassified_minus_correct": (np.mean(wrong) - np.mean(ok)) if included else ""})

    write_csv(OUT / "review_sign_baseline_runs.csv", sign_runs, list(sign_runs[0]))
    sign_summary = summarise(
        sign_runs, ["converted_sign_agreement", "majority_sign_agreement", "shared_nonzero_top5"], (), rng)
    write_csv(OUT / "review_sign_baseline_summary.csv", sign_summary, list(sign_summary[0]))
    write_csv(OUT / "review_rank_sensitivity_runs.csv", rank_runs, list(rank_runs[0]))
    rank_summary = summarise(
        rank_runs, ["reranked_top5_jaccard", "reranked_kendall_tau_b", "shared_only_kendall_tau_b"], (), rng)
    write_csv(OUT / "review_rank_sensitivity_summary.csv", rank_summary, list(rank_summary[0]))

    # training membership: by seed group (42 versus the other four) and model
    write_csv(OUT / "review_training_membership_runs.csv", membership_runs, list(membership_runs[0]))
    membership = []
    for label, keep in (("seed_42", lambda s: s == "42"), ("other_seeds", lambda s: s != "42")):
        for model in sorted({r["model"] for r in membership_runs}) + ["all"]:
            rows = [r for r in membership_runs if keep(r["seed"]) and model in (r["model"], "all")]
            membership.append({
                "seeds": label, "model": model, "n_runs": len(rows),
                "share_training_rows": mean([r["share_training_rows"] for r in rows]),
                "share_training_rows_correct": mean([r["share_training_rows_correct"] for r in rows
                                                     if r["share_training_rows_correct"] != ""]),
                "share_training_rows_misclassified": mean([r["share_training_rows_misclassified"] for r in rows
                                                           if r["share_training_rows_misclassified"] != ""])})
    write_csv(OUT / "review_training_membership_summary.csv", membership, list(membership[0]))

    # held-out correctness contrast: average over intensities per (model, seed), then by model
    write_csv(OUT / "review_heldout_contrast_runs.csv", heldout_runs, list(heldout_runs[0]))
    per_seed: dict[tuple, list[float]] = defaultdict(list)
    for r in heldout_runs:
        if r["included"]:
            per_seed[(r["model"], r["seed"])].append(float(r["misclassified_minus_correct"]))
    heldout = []
    for model in sorted({m for m, _ in per_seed}):
        seed_values = {s: [float(np.mean(v))] for (m, s), v in per_seed.items() if m == model}
        values = [v[0] for v in seed_values.values()]
        low, high = bootstrap(seed_values, rng)
        heldout.append({"dataset": "exp2_adult", "model": model,
                        "mean_misclassified_minus_correct": float(np.mean(values)),
                        "ci95_low": low, "ci95_high": high,
                        "min_seed_difference": min(values), "max_seed_difference": max(values),
                        "n_seed_units": len(values),
                        "n_negative_seed_differences": sum(v < 0 for v in values),
                        "n_positive_seed_differences": sum(v > 0 for v in values),
                        "n_runs_included": sum(1 for r in heldout_runs if r["model"] == model and r["included"]),
                        "n_runs": sum(1 for r in heldout_runs if r["model"] == model)})
    write_csv(OUT / "review_heldout_contrast_summary.csv", heldout, list(heldout[0]))

    # coverage: paired instances as a share of valid LIME instances
    with (ANALYSIS / "pairing_diagnostics.csv").open(encoding="utf-8") as fh:
        pairing = list(csv.DictReader(fh))
    coverage = []
    for dataset in sorted({r["dataset"] for r in pairing}):
        for model in sorted({r["model"] for r in pairing if r["dataset"] == dataset}):
            rows = [r for r in pairing if r["dataset"] == dataset and r["model"] == model]
            paired_n = sum(int(float(r["matched_ids"] or 0)) for r in rows)
            lime_n = sum(int(float(r["right_valid_ids"] or 0)) for r in rows)
            shap_errors = sum(int(float(r["left_invalid_rows"] or 0)) for r in rows)
            coverage.append({"dataset": dataset, "model": model, "paired": paired_n, "lime_valid": lime_n,
                             "share_paired_percent": 100.0 * paired_n / lime_n, "shap_error_rows": shap_errors})
    write_csv(OUT / "review_coverage.csv", coverage, list(coverage[0]))
    print(f"wrote {OUT.relative_to(ROOT)}/review_*.csv")


if __name__ == "__main__":
    main()
