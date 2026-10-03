#!/usr/bin/env python3
"""Analyze instance-level feature agreement for Paper E."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
import platform
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kendalltau, spearmanr

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.paper_e_data_audit import _read_run, _row_invalid_reasons

DEFAULT_LIME_ROOT = PROJECT_ROOT / "outputs/analysis/paper_e/exp3_lime"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "outputs/analysis/paper_e/analysis"
BOOTSTRAP_REPS = 2000
BOOTSTRAP_SEED = 20261003
PRIMARY_PAIRS = (("shap", "lime"),)
EXP2_SECONDARY_PAIRS = (
    ("shap", "anchors"),
    ("lime", "anchors"),
    ("shap", "dice"),
    ("lime", "dice"),
    ("anchors", "dice"),
)

PRIMARY_INSTANCE_FIELDS = [
    "dataset",
    "model",
    "seed",
    "intensity",
    "instance_id",
    "true_label",
    "prediction",
    "prediction_correct",
    "top5_jaccard",
    "top10_jaccard",
    "kendall_tau_b",
    "shared_top5_nonzero",
    "sign_agreement",
    "sign_coverage",
    "shap_fidelity",
    "shap_stability",
    "lime_fidelity",
    "lime_stability",
]


def jaccard(left: Iterable[str], right: Iterable[str]) -> float | None:
    left_set = set(left)
    right_set = set(right)
    union = left_set | right_set
    if not union:
        return None
    return len(left_set & right_set) / len(union)


def _midranks_by_absolute_value(values: dict[str, float]) -> dict[str, float]:
    ordered = sorted(values.items(), key=lambda item: -abs(item[1]))
    ranks: dict[str, float] = {}
    start = 0
    while start < len(ordered):
        end = start + 1
        while (
            end < len(ordered)
            and abs(ordered[end][1]) == abs(ordered[start][1])
        ):
            end += 1
        rank = ((start + 1) + end) / 2
        for feature, _ in ordered[start:end]:
            ranks[feature] = rank
        start = end
    return ranks


def kendall_top10(left: dict[str, float], right: dict[str, float]) -> float | None:
    union = sorted(left.keys() | right.keys())
    if len(union) < 2:
        return None
    left_ranks = _midranks_by_absolute_value(left)
    right_ranks = _midranks_by_absolute_value(right)
    a = [left_ranks.get(feature, 11.0) for feature in union]
    b = [right_ranks.get(feature, 11.0) for feature in union]
    value = kendalltau(a, b, variant="b").statistic
    return float(value) if value is not None and math.isfinite(value) else None


def primary_agreement(
    shap: dict[str, float], lime: dict[str, float]
) -> dict[str, Any]:
    shap_top5 = list(shap)[:5]
    lime_top5 = list(lime)[:5]
    shap_top10 = list(shap)[:10]
    lime_top10 = list(lime)[:10]
    shared = set(shap_top5) & set(lime_top5)
    comparable = [
        feature
        for feature in shared
        if shap[feature] != 0 and lime[feature] != 0
    ]
    sign_agreement = (
        sum(
            (shap[feature] > 0) == (lime[feature] > 0)
            for feature in comparable
        )
        / len(comparable)
        if comparable
        else None
    )
    return {
        "top5_jaccard": jaccard(shap_top5, lime_top5),
        "top10_jaccard": jaccard(shap_top10, lime_top10),
        "kendall_tau_b": kendall_top10(shap, lime),
        "shared_top5_nonzero": len(comparable),
        "sign_agreement": sign_agreement,
        "sign_coverage": len(comparable) / len(shared) if shared else None,
    }


def _is_finite_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def _validate_attribution_order(run: dict[str, Any], method: str) -> None:
    if method not in {"shap", "lime"}:
        return
    invalid_ids = []
    for instance_id, row in run["_valid_rows"].items():
        values = list(row["explanation"]["raw_top"].values())
        if any(
            abs(values[index]) < abs(values[index + 1])
            for index in range(len(values) - 1)
        ):
            invalid_ids.append(instance_id)
    for instance_id in invalid_ids:
        del run["_valid_rows"][instance_id]
    run["invalid_order_ids"] = invalid_ids
    run["empty_explanation_ids"] = sorted(
        instance_id
        for instance_id, row in run["_valid_rows"].items()
        if all(value == 0 for value in row["explanation"]["raw_top"].values())
    )


def _load_run(
    path: Path,
    root: Path,
    *,
    dataset: str,
    model: str,
    seed: str,
    intensity: str,
    method: str,
    path_root: Path | None = None,
) -> dict[str, Any]:
    source_root = path_root or root
    run = _read_run(path, source_root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw_rows = payload["instance_evaluations"]
    row_exclusions = []
    id_counts: Counter[int] = Counter()
    for row in raw_rows:
        if isinstance(row, dict) and not _row_invalid_reasons(row):
            instance_id = row.get("instance_id")
            if isinstance(instance_id, int) and not isinstance(instance_id, bool):
                id_counts[instance_id] += 1
    for row_index, row in enumerate(raw_rows):
        reasons = _row_invalid_reasons(row)
        instance_id = row.get("instance_id") if isinstance(row, dict) else None
        if reasons:
            row_exclusions.append(
                {
                    "source_row_index": row_index,
                    "instance_id": instance_id,
                    "reason": "|".join(reasons),
                }
            )
        elif isinstance(instance_id, int) and id_counts[instance_id] > 1:
            row_exclusions.append(
                {
                    "source_row_index": row_index,
                    "instance_id": instance_id,
                    "reason": "duplicate_instance_id",
                }
            )
    run.update(
        {
            "dataset": dataset,
            "model": model,
            "seed": seed,
            "intensity": intensity,
            "method": method,
            "source_path": path.relative_to(source_root).as_posix(),
            "source_sha256": _sha256(path),
            "row_exclusions": row_exclusions,
        }
    )
    _validate_attribution_order(run, method)
    for instance_id in run.get("invalid_order_ids", []):
        row_exclusions.append(
            {
                "source_row_index": None,
                "instance_id": instance_id,
                "reason": "raw_top_not_sorted_by_absolute_value",
            }
        )
    for instance_id in run.get("empty_explanation_ids", []):
        row_exclusions.append(
            {
                "source_row_index": None,
                "instance_id": instance_id,
                "reason": "empty_additive_explanation",
            }
        )
    run["row_exclusions"] = row_exclusions
    return run


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_runs(root: Path, lime_root: Path) -> dict[tuple[str, ...], dict[str, Any]]:
    runs: dict[tuple[str, ...], dict[str, Any]] = {}
    exp2_root = root / "experiments/exp2_scaled/results"
    for path in sorted(exp2_root.glob("*/*/*/results.json")):
        model, method = path.parents[2].name.rsplit("_", 1)
        seed = path.parents[1].name.removeprefix("seed_")
        intensity = path.parents[0].name
        run = _load_run(
            path,
            root,
            dataset="exp2_adult",
            model=model,
            seed=seed,
            intensity=intensity,
            method=method,
        )
        runs[("exp2_adult", model, seed, intensity, method)] = run

    exp3_root = root / "experiments/exp3_cross_dataset/results"
    for path in sorted(exp3_root.glob("*/*/seed_*/n_100/results.json")):
        dataset = path.parents[3].name
        model, method = path.parents[2].name.rsplit("_", 1)
        seed = path.parents[1].name.removeprefix("seed_")
        run = _load_run(
            path,
            root,
            dataset=dataset,
            model=model,
            seed=seed,
            intensity="not_applicable",
            method=method,
        )
        runs[(dataset, model, seed, "not_applicable", method)] = run

    for key, run in list(runs.items()):
        dataset, model, seed, intensity, method = key
        if dataset == "exp2_adult":
            continue
        metadata_path = (
            root
            / "experiments/exp3_cross_dataset/models"
            / dataset
            / model
            / f"seed_{seed}/metadata.json"
        )
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        known_features = set(metadata.get("feature_names", []))
        unknown_ids = [
            instance_id
            for instance_id, row in run["_valid_rows"].items()
            if not set(row["explanation"]["raw_top"]) <= known_features
        ]
        for instance_id in unknown_ids:
            del run["_valid_rows"][instance_id]
            run["row_exclusions"].append(
                {
                    "source_row_index": None,
                    "instance_id": instance_id,
                    "reason": "unknown_feature_name",
                }
            )
        run["unknown_feature_ids"] = unknown_ids

    manifest_path = lime_root / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"EXP3 Paper E LIME manifest is missing: {manifest_path}")
    lime_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if lime_manifest.get("status") != "complete":
        raise ValueError("EXP3 Paper E LIME manifest is not complete")
    expected_lime_runs = 2 * 2 * 3
    manifest_runs = lime_manifest.get("runs", [])
    if (
        not isinstance(manifest_runs, list)
        or len(manifest_runs) != expected_lime_runs
        or any(
            not isinstance(run, dict) or run.get("status") != "complete"
            for run in manifest_runs
        )
    ):
        raise ValueError(
            f"Expected {expected_lime_runs} completed EXP3 LIME runs in the manifest"
        )
    for path in sorted(lime_root.glob("*/*/seed_*/results.json")):
        dataset = path.parents[2].name
        model = path.parents[1].name
        seed = path.parents[0].name.removeprefix("seed_")
        run = _load_run(
            path,
            root,
            dataset=dataset,
            model=model,
            seed=seed,
            intensity="not_applicable",
            method="lime",
            path_root=lime_root,
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        metadata = payload.get("experiment_metadata", {})
        source_shap = runs.get(
            (dataset, model, seed, "not_applicable", "shap")
        )
        if source_shap is None:
            raise ValueError(
                f"Missing EXP3 SHAP source run for {dataset}/{model}/seed_{seed}"
            )
        expected_ids = sorted(source_shap["_valid_rows"])
        target_ids = metadata.get("target_instance_ids")
        if (
            metadata.get("experiment") != "paper_e_exp3_lime"
            or metadata.get("status") != "complete"
            or metadata.get("dataset") != dataset
            or metadata.get("model") != model
            or str(metadata.get("seed")) != seed
            or metadata.get("target_instance_count") != len(expected_ids)
            or target_ids != expected_ids
            or sorted(run["_valid_rows"]) != expected_ids
            or metadata.get("source_run_path") != source_shap["source_path"]
        ):
            raise ValueError(
                f"EXP3 LIME IDs/provenance do not exactly match SHAP for "
                f"{dataset}/{model}/seed_{seed}"
            )
        raw_attribution_errors = []
        names = metadata.get("feature_names", [])
        for instance_id, row in run["_valid_rows"].items():
            values = row["explanation"].get("raw_attributions")
            if (
                not isinstance(values, dict)
                or list(values) != names
                or any(not _is_finite_number(value) for value in values.values())
            ):
                raw_attribution_errors.append(instance_id)
        run["invalid_full_attribution_ids"] = raw_attribution_errors
        run["row_exclusions"].extend(
            {
                "source_row_index": None,
                "instance_id": instance_id,
                "reason": "invalid_full_attribution_vector",
            }
            for instance_id in raw_attribution_errors
        )
        _validate_attribution_order(run, "lime")
        runs[(dataset, model, seed, "not_applicable", "lime")] = run

    if len([
        key for key in runs
        if key[0] != "exp2_adult" and key[-1] == "lime"
    ]) != expected_lime_runs:
        raise ValueError("EXP3 Paper E LIME results are incomplete")
    return runs


def _pair_rows(
    left: dict[str, Any] | None, right: dict[str, Any] | None
) -> tuple[list[int], list[int]]:
    if left is None or right is None:
        return [], []
    left_rows = left["_valid_rows"]
    right_rows = right["_valid_rows"]
    matched = sorted(left_rows.keys() & right_rows.keys())
    mismatches = [
        i
        for i in matched
        if (
            left_rows[i].get("true_label"),
            left_rows[i].get("prediction"),
            left_rows[i].get("prediction_correct"),
        )
        != (
            right_rows[i].get("true_label"),
            right_rows[i].get("prediction"),
            right_rows[i].get("prediction_correct"),
        )
    ]
    return matched, mismatches


def _primary_rows(
    runs: dict[tuple[str, ...], dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    diagnostics = []
    instances = []
    blocks = sorted({key[:4] for key in runs})
    for block in blocks:
        dataset, model, seed, intensity = block
        pairs = PRIMARY_PAIRS if dataset == "exp2_adult" else (("shap", "lime"),)
        for left_method, right_method in pairs:
            left = runs.get((*block, left_method))
            right = runs.get((*block, right_method))
            matched, mismatch_ids = _pair_rows(left, right)
            left_ids = set(left["_valid_rows"]) if left else set()
            right_ids = set(right["_valid_rows"]) if right else set()
            diagnostic = {
                "dataset": dataset,
                "model": model,
                "seed": seed,
                "intensity": intensity,
                "method_pair": f"{left_method}_{right_method}",
                "available": left is not None and right is not None,
                "left_valid_ids": len(left_ids),
                "right_valid_ids": len(right_ids),
                "left_source_rows": left["row_count"] if left else None,
                "right_source_rows": right["row_count"] if right else None,
                "left_valid_rows": left["valid_row_count"] if left else None,
                "right_valid_rows": right["valid_row_count"] if right else None,
                "matched_ids": len(matched),
                "left_only_ids": len(left_ids - right_ids),
                "right_only_ids": len(right_ids - left_ids),
                "same_id_sets": bool(left_ids and right_ids) and left_ids == right_ids,
                "classification_mismatches": len(mismatch_ids),
                "classification_mismatch_ids": "|".join(map(str, mismatch_ids)),
                "left_invalid_rows": left["invalid_row_count"] if left else None,
                "right_invalid_rows": right["invalid_row_count"] if right else None,
                "left_duplicate_ids": len(left["duplicate_ids"]) if left else None,
                "right_duplicate_ids": len(right["duplicate_ids"]) if right else None,
                "left_duplicate_ids_list": "|".join(
                    map(str, left["duplicate_ids"])
                ) if left else None,
                "right_duplicate_ids_list": "|".join(
                    map(str, right["duplicate_ids"])
                ) if right else None,
                "left_order_invalid": len(left.get("invalid_order_ids", [])) if left else None,
                "right_order_invalid": len(right.get("invalid_order_ids", [])) if right else None,
                "left_empty_explanations": len(left.get("empty_explanation_ids", [])) if left else None,
                "right_empty_explanations": len(right.get("empty_explanation_ids", [])) if right else None,
            }
            diagnostics.append(diagnostic)
            if left is None or right is None:
                continue
            empty_left = set(left.get("empty_explanation_ids", []))
            empty_right = set(right.get("empty_explanation_ids", []))
            for instance_id in matched:
                if instance_id in mismatch_ids:
                    continue
                if instance_id in empty_left or instance_id in empty_right:
                    continue
                left_row = left["_valid_rows"][instance_id]
                right_row = right["_valid_rows"][instance_id]
                left_map = left_row["explanation"]["raw_top"]
                right_map = right_row["explanation"]["raw_top"]
                scores = primary_agreement(left_map, right_map)
                instances.append(
                    {
                        "dataset": dataset,
                        "model": model,
                        "seed": seed,
                        "intensity": intensity,
                        "instance_id": instance_id,
                        "true_label": left_row["true_label"],
                        "prediction": left_row["prediction"],
                        "prediction_correct": left_row["prediction_correct"],
                        **scores,
                        "shap_fidelity": _quality(left_row, "fidelity"),
                        "shap_stability": _quality(left_row, "stability"),
                        "lime_fidelity": _quality(right_row, "fidelity"),
                        "lime_stability": _quality(right_row, "stability"),
                    }
                )
    return diagnostics, instances


def _quality(row: dict[str, Any], metric: str) -> float | None:
    metrics = row.get("metrics")
    value = metrics.get(metric) if isinstance(metrics, dict) else None
    return float(value) if _is_finite_number(value) else None


def _secondary_rows(
    runs: dict[tuple[str, ...], dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    diagnostics = []
    records = []
    blocks = sorted({key[:4] for key in runs if key[0] == "exp2_adult"})
    for block in blocks:
        dataset, model, seed, intensity = block
        for left_method, right_method in EXP2_SECONDARY_PAIRS:
            left = runs.get((*block, left_method))
            right = runs.get((*block, right_method))
            matched, mismatch_ids = _pair_rows(left, right)
            left_ids = set(left["_valid_rows"]) if left else set()
            right_ids = set(right["_valid_rows"]) if right else set()
            diagnostic = {
                    "dataset": dataset,
                    "model": model,
                    "seed": seed,
                    "intensity": intensity,
                    "method_pair": f"{left_method}_{right_method}",
                    "available": left is not None and right is not None,
                    "left_valid_ids": len(left_ids),
                    "right_valid_ids": len(right_ids),
                    "left_source_rows": left["row_count"] if left else None,
                    "right_source_rows": right["row_count"] if right else None,
                    "left_valid_rows": left["valid_row_count"] if left else None,
                    "right_valid_rows": right["valid_row_count"] if right else None,
                    "matched_ids": len(matched),
                    "left_only_ids": len(left_ids - right_ids),
                    "right_only_ids": len(right_ids - left_ids),
                    "same_id_sets": bool(left_ids and right_ids) and left_ids == right_ids,
                    "classification_mismatches": len(mismatch_ids),
                    "classification_mismatch_ids": "|".join(
                        map(str, mismatch_ids)
                    ),
                    "left_duplicate_ids": len(left["duplicate_ids"]) if left else None,
                    "right_duplicate_ids": len(right["duplicate_ids"]) if right else None,
                    "left_duplicate_ids_list": "|".join(
                        map(str, left["duplicate_ids"])
                    ) if left else None,
                    "right_duplicate_ids_list": "|".join(
                        map(str, right["duplicate_ids"])
                    ) if right else None,
                    "anchors_truncated_exclusions": 0,
                    "anchors_truncated_instance_ids": "",
                    "empty_set_pairs": 0,
                }
            diagnostics.append(diagnostic)
            if left is None or right is None:
                continue
            truncated_ids = []
            for instance_id in matched:
                if instance_id in mismatch_ids:
                    continue
                left_row = left["_valid_rows"][instance_id]
                right_row = right["_valid_rows"][instance_id]
                if (
                    left_row["true_label"],
                    left_row["prediction"],
                    left_row["prediction_correct"],
                ) != (
                    right_row["true_label"],
                    right_row["prediction"],
                    right_row["prediction_correct"],
                ):
                    continue
                left_values = left_row["explanation"]["raw_top"]
                right_values = right_row["explanation"]["raw_top"]
                if left_method == "anchors" and sum(
                    value == 1 for value in left_values.values()
                ) >= 10:
                    diagnostic["anchors_truncated_exclusions"] += 1
                    truncated_ids.append(instance_id)
                    continue
                if right_method == "anchors" and sum(
                    value == 1 for value in right_values.values()
                ) >= 10:
                    diagnostic["anchors_truncated_exclusions"] += 1
                    truncated_ids.append(instance_id)
                    continue
                left_set = _feature_set(left_method, left_values)
                right_set = _feature_set(right_method, right_values)
                if not left_set and not right_set:
                    diagnostic["empty_set_pairs"] += 1
                records.append(
                    {
                        "dataset": dataset,
                        "model": model,
                        "seed": seed,
                        "intensity": intensity,
                        "instance_id": instance_id,
                        "method_pair": f"{left_method}_{right_method}",
                        "left_features": len(left_set),
                        "right_features": len(right_set),
                        "jaccard": jaccard(left_set, right_set),
                        "left_empty": not left_set,
                        "right_empty": not right_set,
                    }
                )
            diagnostic["anchors_truncated_instance_ids"] = "|".join(
                map(str, sorted(set(truncated_ids)))
            )
    return diagnostics, records


def _feature_set(method: str, values: dict[str, float]) -> set[str]:
    if method == "anchors":
        return {name for name, value in values.items() if value == 1}
    if method == "dice":
        return {name for name, value in values.items() if value > 0}
    return set(list(values)[:5])


def _mean(values: Iterable[float | None]) -> float | None:
    present = [value for value in values if value is not None and math.isfinite(value)]
    return float(np.mean(present)) if present else None


def _run_summaries(
    instances: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in instances:
        groups[
            (row["dataset"], row["model"], row["seed"], row["intensity"])
        ].append(row)

    run_summaries = []
    contrasts = []
    quality = []
    quality_fields = (
        "shap_fidelity",
        "shap_stability",
        "lime_fidelity",
        "lime_stability",
    )
    for key, rows in sorted(groups.items()):
        dataset, model, seed, intensity = key
        summary = {
            "dataset": dataset,
            "model": model,
            "seed": seed,
            "intensity": intensity,
            "n_instances": len(rows),
            "n_correct": sum(bool(row["prediction_correct"]) for row in rows),
            "n_misclassified": sum(not bool(row["prediction_correct"]) for row in rows),
        }
        for metric in ("top5_jaccard", "top10_jaccard", "kendall_tau_b", "sign_agreement"):
            summary[f"{metric}_mean"] = _mean(row[metric] for row in rows)
            summary[f"{metric}_median"] = (
                float(np.median([row[metric] for row in rows if row[metric] is not None]))
                if any(row[metric] is not None for row in rows)
                else None
            )
        summary["sign_comparable_features"] = sum(
            int(row["shared_top5_nonzero"]) for row in rows
        )
        summary["sign_coverage_mean"] = _mean(row["sign_coverage"] for row in rows)
        summary["sign_defined_instances"] = sum(
            row["sign_agreement"] is not None for row in rows
        )
        run_summaries.append(summary)

        correct = [row["top5_jaccard"] for row in rows if row["prediction_correct"]]
        incorrect = [row["top5_jaccard"] for row in rows if not row["prediction_correct"]]
        enough = len(correct) >= 10 and len(incorrect) >= 10
        contrasts.append(
            {
                "dataset": dataset,
                "model": model,
                "seed": seed,
                "intensity": intensity,
                "row_type": "run",
                "n_correct": len(correct),
                "n_misclassified": len(incorrect),
                "correct_mean": _mean(correct),
                "misclassified_mean": _mean(incorrect),
                "misclassified_minus_correct": (
                    _mean(incorrect) - _mean(correct) if enough else None
                ),
                "included": enough,
            }
        )

        for quality_field in quality_fields:
            pairs = [
                (1 - row["top5_jaccard"], row[quality_field])
                for row in rows
                if row["top5_jaccard"] is not None
                and row[quality_field] is not None
            ]
            rho = None
            if len(pairs) >= 2:
                correlation = spearmanr(
                    [pair[0] for pair in pairs],
                    [pair[1] for pair in pairs],
                ).statistic
                if correlation is not None and math.isfinite(correlation):
                    rho = float(correlation)
            quality.append(
                {
                    "dataset": dataset,
                    "model": model,
                    "seed": seed,
                    "intensity": intensity,
                    "quality_metric": quality_field,
                    "n_pairs": len(pairs),
                    "spearman_rho": rho,
                }
            )

    for key in sorted({(r["dataset"], r["model"], r["seed"]) for r in run_summaries}):
        dataset, model, seed = key
        if dataset != "exp2_adult":
            continue
        seed_rows = [
            row for row in contrasts
            if row["dataset"] == dataset and row["model"] == model
            and row["seed"] == seed and row["included"]
        ]
        if seed_rows:
            contrasts.append(
                {
                    "dataset": dataset,
                    "model": model,
                    "seed": seed,
                    "intensity": "all",
                    "row_type": "seed_intensity_average",
                    "n_correct": None,
                    "n_misclassified": None,
                    "correct_mean": _mean(row["correct_mean"] for row in seed_rows),
                    "misclassified_mean": _mean(
                        row["misclassified_mean"] for row in seed_rows
                    ),
                    "misclassified_minus_correct": _mean(
                        row["misclassified_minus_correct"] for row in seed_rows
                    ),
                    "included": True,
                }
            )
    return run_summaries, contrasts, quality


def _bootstrap_interval(
    rows: list[dict[str, Any]],
    value_field: str,
    rng: np.random.Generator,
) -> tuple[float | None, float | None]:
    usable = [
        row for row in rows
        if row.get(value_field) is not None
        and math.isfinite(float(row[value_field]))
    ]
    seeds = sorted({str(row["seed"]) for row in usable})
    if len(seeds) < 2:
        return None, None
    grouped = {
        seed: [float(row[value_field]) for row in usable if str(row["seed"]) == seed]
        for seed in seeds
    }
    estimates = np.empty(BOOTSTRAP_REPS, dtype=float)
    for index in range(BOOTSTRAP_REPS):
        sampled = rng.choice(seeds, size=len(seeds), replace=True)
        values = [
            value
            for seed in sampled
            for value in grouped[str(seed)]
        ]
        estimates[index] = np.mean(values)
    low, high = np.quantile(estimates, [0.025, 0.975])
    return float(low), float(high)


def _group_summaries(
    run_summaries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    output = []
    metrics = ("top5_jaccard", "top10_jaccard", "kendall_tau_b", "sign_agreement")
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in run_summaries:
        groups[(row["dataset"], row["model"], row["intensity"])].append(row)
    for key, rows in sorted(groups.items()):
        dataset, model, intensity = key
        for metric in metrics:
            field = f"{metric}_mean"
            values = [row[field] for row in rows if row[field] is not None]
            ci_low, ci_high = _bootstrap_interval(rows, field, rng)
            output.append(
                {
                    "dataset": dataset,
                    "model": model,
                    "intensity": intensity,
                    "metric": metric,
                    "estimate_mean_of_run_means": _mean(values),
                    "estimate_median_of_run_means": (
                        float(np.median(values)) if values else None
                    ),
                    "ci95_low": ci_low,
                    "ci95_high": ci_high,
                    "n_runs": len(values),
                    "n_seeds": len({row["seed"] for row in rows if row[field] is not None}),
                    "n_instances": sum(row["n_instances"] for row in rows),
                    "sign_comparable_features": sum(
                        row["sign_comparable_features"] for row in rows
                    ),
                    "mean_sign_coverage": _mean(
                        row["sign_coverage_mean"] for row in rows
                    ),
                    "sign_defined_instances": sum(
                        row["sign_defined_instances"] for row in rows
                    ),
                }
            )

    overall_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in run_summaries:
        overall_groups[row["dataset"]].append(row)
    for dataset, rows in sorted(overall_groups.items()):
        for metric in metrics:
            field = f"{metric}_mean"
            values = [row[field] for row in rows if row[field] is not None]
            ci_low, ci_high = _bootstrap_interval(rows, field, rng)
            output.append(
                {
                    "dataset": dataset,
                    "model": "all",
                    "intensity": "all" if dataset == "exp2_adult" else "not_applicable",
                    "metric": metric,
                    "estimate_mean_of_run_means": _mean(values),
                    "estimate_median_of_run_means": (
                        float(np.median(values)) if values else None
                    ),
                    "ci95_low": ci_low,
                    "ci95_high": ci_high,
                    "n_runs": len(values),
                    "n_seeds": len({row["seed"] for row in rows if row[field] is not None}),
                    "n_instances": sum(row["n_instances"] for row in rows),
                    "sign_comparable_features": sum(
                        row["sign_comparable_features"] for row in rows
                    ),
                    "mean_sign_coverage": _mean(
                        row["sign_coverage_mean"] for row in rows
                    ),
                    "sign_defined_instances": sum(
                        row["sign_defined_instances"] for row in rows
                    ),
                }
            )
    return output


def _correctness_summaries(
    contrasts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rng = np.random.default_rng(BOOTSTRAP_SEED + 1)
    eligible = [row for row in contrasts if row["included"]]
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in eligible:
        if row["row_type"] == "run":
            groups[(row["dataset"], row["model"], row["intensity"])].append(row)
        elif row["row_type"] == "seed_intensity_average":
            groups[(row["dataset"], row["model"], row["intensity"])].append(row)
    output = []
    for key, rows in sorted(groups.items()):
        dataset, model, intensity = key
        ci_low, ci_high = _bootstrap_interval(
            rows, "misclassified_minus_correct", rng
        )
        output.append(
            {
                "dataset": dataset,
                "model": model,
                "intensity": intensity,
                "mean_misclassified_minus_correct": _mean(
                    row["misclassified_minus_correct"] for row in rows
                ),
                "median_misclassified_minus_correct": float(
                    np.median([row["misclassified_minus_correct"] for row in rows])
                ),
                "mean_correct_jaccard": _mean(row["correct_mean"] for row in rows),
                "mean_misclassified_jaccard": _mean(
                    row["misclassified_mean"] for row in rows
                ),
                "ci95_low": ci_low,
                "ci95_high": ci_high,
                "n_seed_units": len({row["seed"] for row in rows}),
                "n_positive_seed_differences": sum(
                    row["misclassified_minus_correct"] > 0 for row in rows
                ),
                "n_negative_seed_differences": sum(
                    row["misclassified_minus_correct"] < 0 for row in rows
                ),
            }
        )
    return output


def _quality_summaries(
    quality: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    seed_groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in quality:
        seed_groups[
            (
                row["dataset"],
                row["model"],
                row["seed"],
                row["quality_metric"],
            )
        ].append(row)

    seed_summaries = []
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for key, rows in seed_groups.items():
        seed_summary = {
            "dataset": key[0],
            "model": key[1],
            "seed": key[2],
            "quality_metric": key[3],
            "mean_run_spearman_rho": _mean(
                row["spearman_rho"] for row in rows
            ),
            "n_run_associations": sum(
                row["spearman_rho"] is not None for row in rows
            ),
        }
        seed_summaries.append(seed_summary)
        groups[(key[0], key[1], key[3])].append(
            {
                "seed": key[2],
                "spearman_rho": seed_summary["mean_run_spearman_rho"],
                "n_runs": seed_summary["n_run_associations"],
            }
        )
    output = []
    for key, rows in sorted(groups.items()):
        seed_values = [
            row["spearman_rho"] for row in rows
            if row["spearman_rho"] is not None
        ]
        output.append(
            {
                "dataset": key[0],
                "model": key[1],
                "quality_metric": key[2],
                "mean_seed_spearman_rho": _mean(seed_values),
                "median_seed_spearman_rho": (
                    float(np.median(seed_values)) if seed_values else None
                ),
                "n_seed_units": len(seed_values),
                "n_run_associations": sum(row["n_runs"] for row in rows),
            }
        )
    return seed_summaries, output


def _secondary_summaries(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in records:
        groups[
            (
                row["dataset"],
                row["model"],
                row["seed"],
                row["intensity"],
                row["method_pair"],
            )
        ].append(row)
    return [
        {
            "dataset": key[0],
            "model": key[1],
            "seed": key[2],
            "intensity": key[3],
            "method_pair": key[4],
            "n_matched": len(rows),
            "n_defined_jaccard": sum(row["jaccard"] is not None for row in rows),
            "mean_jaccard": _mean(row["jaccard"] for row in rows),
            "empty_left_count": sum(bool(row["left_empty"]) for row in rows),
            "empty_right_count": sum(bool(row["right_empty"]) for row in rows),
        }
        for key, rows in sorted(groups.items())
    ]


def _write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=fields,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def _plot_outputs(
    output_root: Path,
    instances: list[dict[str, Any]],
    contrasts: list[dict[str, Any]],
    quality: list[dict[str, Any]],
) -> None:
    figure_root = output_root / "figures"
    figure_root.mkdir(parents=True, exist_ok=True)

    keys = sorted({
        (row["dataset"], row["model"]) for row in instances
    })
    data = [
        [
            row["top5_jaccard"]
            for row in instances
            if (row["dataset"], row["model"]) == key
            and row["top5_jaccard"] is not None
        ]
        for key in keys
    ]
    fig, ax = plt.subplots(figsize=(max(8, len(keys) * 0.8), 5))
    if any(data):
        ax.boxplot(data, labels=[f"{d}\n{m}" for d, m in keys], showfliers=False)
        ax.set_ylabel("Instance top-5 Jaccard overlap")
        ax.set_title("SHAP–LIME top-5 feature overlap by dataset and model")
        ax.set_ylim(-0.03, 1.03)
    else:
        ax.text(0.5, 0.5, "No primary agreement observations", ha="center")
        ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(figure_root / "top5_jaccard_by_model_dataset.png", dpi=160)
    plt.close(fig)

    correct_groups = []
    correct_labels = []
    for dataset, model in keys:
        run_rows = [
            row for row in contrasts
            if row["dataset"] == dataset and row["model"] == model
            and row["row_type"] == "run"
        ]
        for field, label in (
            ("correct_mean", "Correct"),
            ("misclassified_mean", "Misclassified"),
        ):
            values = [
                row[field] for row in run_rows
                if row["included"] and row[field] is not None
            ]
            if values:
                correct_groups.append(values)
                correct_labels.append(f"{dataset}\n{model}\n{label}")
    fig, ax = plt.subplots(figsize=(max(8, len(correct_groups) * 0.8), 5))
    if correct_groups:
        ax.boxplot(correct_groups, labels=correct_labels, showfliers=True)
        ax.set_ylabel("Run mean top-5 Jaccard overlap")
        ax.set_title("SHAP–LIME agreement by prediction correctness")
        ax.set_ylim(-0.03, 1.03)
        ax.tick_params(axis="x", labelrotation=35)
    else:
        ax.text(0.5, 0.5, "No runs meet the prespecified correctness minimum", ha="center")
        ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(figure_root / "top5_jaccard_by_correctness.png", dpi=160)
    plt.close(fig)

    variables = sorted({row["quality_metric"] for row in quality})
    fig, ax = plt.subplots(figsize=(max(8, len(variables) * 1.3), 5))
    plotted = False
    for position, variable in enumerate(variables):
        values = [
            row["spearman_rho"] for row in quality
            if row["quality_metric"] == variable
            and row["spearman_rho"] is not None
        ]
        if values:
            ax.scatter([position] * len(values), values, alpha=0.65)
            plotted = True
    if plotted:
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_xticks(range(len(variables)), labels=variables, rotation=25, ha="right")
        ax.set_ylabel("Within-run Spearman rho")
        ax.set_title("Run-level association between disagreement and explainer quality")
    else:
        ax.text(0.5, 0.5, "No estimable within-run quality associations", ha="center")
        ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(figure_root / "disagreement_quality_associations.png", dpi=160)
    plt.close(fig)


def _write_report(
    output_root: Path,
    group_summary: list[dict[str, Any]],
    diagnostics: list[dict[str, Any]],
    instances: list[dict[str, Any]],
) -> None:
    overall = [
        row for row in group_summary
        if row["model"] == "all"
        and row["intensity"] in {"all", "not_applicable"}
        and row["metric"] in {"top5_jaccard", "kendall_tau_b", "sign_agreement"}
    ]
    lines = [
        "# Paper E — feature-agreement analysis",
        "",
        "This report is generated from committed EXP2/EXP3 source runs and the",
        "instance-aligned EXP3 LIME cohort. Agreement values are descriptive;",
        "no confirmatory hypothesis tests or p-values are reported.",
        "",
        "## Overall SHAP–LIME summaries",
        "",
        "| Dataset | Measure | Mean of run means | Seed-clustered 95% CI | Runs | Seeds |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in overall:
        estimate = row["estimate_mean_of_run_means"]
        estimate_text = f"{estimate:.3f}" if estimate is not None else "NA"
        interval = (
            f"[{row['ci95_low']:.3f}, {row['ci95_high']:.3f}]"
            if row["ci95_low"] is not None
            else "not estimable (<2 seeds)"
        )
        lines.append(
            f"| {row['dataset']} | {row['metric']} | "
            f"{estimate_text} | {interval} | "
            f"{row['n_runs']} | {row['n_seeds']} |"
        )
    mismatch_count = sum(row["classification_mismatches"] for row in diagnostics)
    lines.extend(
        [
            "",
            "## Cohort and QC",
            "",
            f"- Usable paired instance records: {len(instances)} (repeated across",
            "  runs, models, and EXP2 intensities; not an independent sample size).",
            f"- Pairing blocks audited: {len(diagnostics)}.",
            f"- Classification mismatches across paired IDs: {mismatch_count}.",
            f"- Seed-cluster bootstrap: {BOOTSTRAP_REPS} resamples; seed {BOOTSTRAP_SEED};",
            "  percentile intervals over run-level means.",
            "- Adult results reuse the EXP2 benchmark cohort used in Papers A and B+C.",
            "- EXP3 models were regenerated from the checked-in training recipe in an",
            "  isolated artifact directory and validated against stored configs,",
            "  training summaries, feature order, and SHAP-cohort labels/predictions.",
            "- The source model binaries are not tracked; hashes of regenerated models",
            "  and preprocessors are retained in each LIME run's metadata.",
            "- Anchors and DiCE comparisons are descriptive feature-set overlaps only.",
            "",
            "## Interpretation limits",
            "",
            "Instances recur across runs and settings; seed-clustered intervals",
            "preserve the seed as the resampling unit. EXP2 has five seeds and EXP3",
            "has three, so intervals are unstable and moderator/correctness/quality",
            "patterns remain exploratory. No universal agreement threshold is used.",
            "",
            "Machine-readable results and figure-source records are in the sibling CSV",
            "files. Figures are regenerated by `scripts/analyze_paper_e.py`.",
            "",
        ]
    )
    (output_root / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8")


def run_analysis(
    root: Path,
    output_root: Path,
    lime_root: Path,
) -> dict[str, int]:
    root = root.resolve()
    output_root = output_root.resolve()
    lime_root = lime_root.resolve()
    if output_root.exists() and any(output_root.iterdir()):
        raise FileExistsError(
            f"Paper E analysis output directory must be empty: {output_root}"
        )
    runs = _load_runs(root, lime_root)
    output_root.mkdir(parents=True, exist_ok=True)
    pairing, instances = _primary_rows(runs)
    secondary_pairing, secondary = _secondary_rows(runs)
    run_summaries, contrasts, quality = _run_summaries(instances)
    group_summaries = _group_summaries(run_summaries)
    correctness_summary = _correctness_summaries(contrasts)
    quality_by_seed, quality_summary = _quality_summaries(quality)
    secondary_summary = _secondary_summaries(secondary)

    _write_csv(output_root / "pairing_diagnostics.csv", pairing, list(pairing[0]) if pairing else [])
    _write_csv(
        output_root / "secondary_pairing_diagnostics.csv",
        secondary_pairing,
        list(secondary_pairing[0]) if secondary_pairing else [],
    )
    _write_csv(
        output_root / "instance_agreement.csv",
        instances,
        PRIMARY_INSTANCE_FIELDS,
    )
    _write_csv(
        output_root / "run_agreement_summary.csv",
        run_summaries,
        list(run_summaries[0]) if run_summaries else [],
    )
    _write_csv(
        output_root / "group_agreement_summary.csv",
        group_summaries,
        list(group_summaries[0]) if group_summaries else [],
    )
    _write_csv(
        output_root / "correctness_contrasts.csv",
        contrasts,
        list(contrasts[0]) if contrasts else [],
    )
    _write_csv(
        output_root / "correctness_group_summary.csv",
        correctness_summary,
        list(correctness_summary[0]) if correctness_summary else [],
    )
    _write_csv(
        output_root / "quality_associations.csv",
        quality,
        list(quality[0]) if quality else [],
    )
    _write_csv(
        output_root / "quality_association_by_seed.csv",
        quality_by_seed,
        list(quality_by_seed[0]) if quality_by_seed else [],
    )
    _write_csv(
        output_root / "quality_association_summary.csv",
        quality_summary,
        list(quality_summary[0]) if quality_summary else [],
    )
    _write_csv(
        output_root / "secondary_feature_set_agreement.csv",
        secondary,
        list(secondary[0]) if secondary else [],
    )
    _write_csv(
        output_root / "secondary_run_summary.csv",
        secondary_summary,
        list(secondary_summary[0]) if secondary_summary else [],
    )
    inventory_rows = [
        {
            "dataset": run["dataset"],
            "model": run["model"],
            "seed": run["seed"],
            "intensity": run["intensity"],
            "method": run["method"],
            "source_path": run["source_path"],
            "source_sha256": run["source_sha256"],
            "source_rows": run["row_count"],
            "valid_rows_before_order_qc": run["valid_row_count"],
            "unique_valid_ids_after_duplicate_qc": run["unique_valid_id_count"],
            "invalid_rows": run["invalid_row_count"],
            "invalid_reason_counts": json.dumps(
                run["invalid_reason_counts"], sort_keys=True
            ),
            "duplicate_ids": "|".join(map(str, run["duplicate_ids"])),
            "invalid_order_ids": "|".join(
                map(str, run.get("invalid_order_ids", []))
            ),
            "empty_explanation_ids": "|".join(
                map(str, run.get("empty_explanation_ids", []))
            ),
            "invalid_full_attribution_ids": "|".join(
                map(str, run.get("invalid_full_attribution_ids", []))
            ),
        }
        for run in sorted(
            runs.values(),
            key=lambda row: (
                row["dataset"],
                row["model"],
                row["seed"],
                row["intensity"],
                row["method"],
            ),
        )
    ]
    _write_csv(
        output_root / "run_inventory.csv",
        inventory_rows,
        list(inventory_rows[0]) if inventory_rows else [],
    )
    detailed_exclusions = [
        {
            "dataset": run["dataset"],
            "model": run["model"],
            "seed": run["seed"],
            "intensity": run["intensity"],
            "method": run["method"],
            "source_path": run["source_path"],
            **exclusion,
        }
        for run in runs.values()
        for exclusion in run.get("row_exclusions", [])
    ]
    _write_csv(
        output_root / "row_exclusion_diagnostics.csv",
        detailed_exclusions,
        [
            "dataset",
            "model",
            "seed",
            "intensity",
            "method",
            "source_path",
            "source_row_index",
            "instance_id",
            "reason",
        ],
    )
    _plot_outputs(output_root, instances, contrasts, quality)
    _write_report(output_root, group_summaries, pairing, instances)

    source_hashes = sorted(
        {
            run["source_path"]: run["source_sha256"]
            for run in runs.values()
        }.items()
    )
    counts = {
        "source_runs": len(runs),
        "pairing_blocks": len(pairing),
        "paired_instances": len(instances),
        "secondary_instances": len(secondary),
    }
    manifest = {
        "experiment": "paper_e_feature_agreement",
        "status": "complete",
        "analysis_script": "scripts/analyze_paper_e.py",
        "bootstrap_replicates": BOOTSTRAP_REPS,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "software_versions": {
            "python": platform.python_version(),
            "numpy": importlib.metadata.version("numpy"),
            "scipy": importlib.metadata.version("scipy"),
            "matplotlib": importlib.metadata.version("matplotlib"),
        },
        "analysis_script_sha256": _sha256(Path(__file__).resolve()),
        "counts": counts,
        "source_sha256": dict(source_hashes),
        "exclusions": {
            "invalid_or_malformed_rows": sum(
                run["invalid_row_count"] for run in runs.values()
            ),
            "duplicate_id_groups": sum(
                len(run["duplicate_ids"]) for run in runs.values()
            ),
            "attribution_order_rows": sum(
                len(run.get("invalid_order_ids", [])) for run in runs.values()
            ),
            "empty_additive_explanations": sum(
                len(run.get("empty_explanation_ids", [])) for run in runs.values()
            ),
            "invalid_full_attribution_vectors": sum(
                len(run.get("invalid_full_attribution_ids", []))
                for run in runs.values()
            ),
            "unknown_feature_name_rows": sum(
                len(run.get("unknown_feature_ids", []))
                for run in runs.values()
            ),
        },
        "outputs": sorted(
            path.relative_to(output_root).as_posix()
            for path in output_root.rglob("*")
            if path.is_file() and path.name != "manifest.json"
        ),
    }
    (output_root / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"counts": counts, "exclusions": manifest["exclusions"]}, indent=2))
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--lime-root", type=Path, default=DEFAULT_LIME_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_ROOT)
    args = parser.parse_args()
    run_analysis(args.root, args.output_dir, args.lime_root)


if __name__ == "__main__":
    main()
