#!/usr/bin/env python3
"""Audit source-run identity and explanation schemas for Paper E."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

EXP2_METHODS = ("shap", "lime", "anchors", "dice")
EXP3_METHODS = ("shap", "anchors")
EXP3_DATASETS = ("german_credit", "breast_cancer")
MODELS = ("rf", "xgb")
SEEDS = (42, 123, 456)
METHOD_PAIRS = (
    ("shap", "lime"),
    ("shap", "anchors"),
    ("shap", "dice"),
    ("lime", "anchors"),
    ("lime", "dice"),
    ("anchors", "dice"),
)


def _row_invalid_reasons(row: Any) -> list[str]:
    if not isinstance(row, dict):
        return ["not_an_object"]

    reasons = []
    if not isinstance(row.get("instance_id"), int):
        reasons.append("missing_or_invalid_instance_id")
    if "error" in row and "explanation" not in row:
        reasons.append("source_error")

    explanation = row.get("explanation")
    raw_top = explanation.get("raw_top") if isinstance(explanation, dict) else None
    if not isinstance(raw_top, dict) or not raw_top:
        reasons.append("missing_or_empty_raw_top")
    elif any(
        not isinstance(name, str)
        or not name
        or isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        for name, value in raw_top.items()
    ):
        reasons.append("invalid_raw_top")

    if "true_label" not in row or "prediction" not in row:
        reasons.append("missing_classification_labels")
    elif row.get("prediction_correct") != (
        row["true_label"] == row["prediction"]
    ):
        reasons.append("inconsistent_prediction_correct")
    return reasons


def _read_run(path: Path, root: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read result file {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"Result file must contain a JSON object: {path}")
    rows = payload.get("instance_evaluations")
    if not isinstance(rows, list):
        raise ValueError(f"Missing instance_evaluations list in {path}")

    valid_rows: dict[int, dict[str, Any]] = {}
    id_counts: Counter[int] = Counter()
    invalid_reasons: Counter[str] = Counter()
    valid_row_count = 0
    for row in rows:
        reasons = _row_invalid_reasons(row)
        if reasons:
            invalid_reasons.update(reasons)
            continue
        valid_row_count += 1
        instance_id = row["instance_id"]
        id_counts[instance_id] += 1
        valid_rows[instance_id] = row

    duplicate_ids = sorted(
        instance_id for instance_id, count in id_counts.items() if count > 1
    )
    for instance_id in duplicate_ids:
        del valid_rows[instance_id]

    return {
        "path": path.relative_to(root).as_posix(),
        "row_count": len(rows),
        "valid_row_count": valid_row_count,
        "invalid_row_count": len(rows) - valid_row_count,
        "invalid_reason_counts": dict(sorted(invalid_reasons.items())),
        "duplicate_ids": duplicate_ids,
        "duplicate_record_count": sum(id_counts[i] for i in duplicate_ids),
        "unique_valid_id_count": len(valid_rows),
        "_valid_rows": valid_rows,
    }


def _pair_audit(
    left: dict[str, Any] | None, right: dict[str, Any] | None
) -> dict[str, Any]:
    if left is None or right is None:
        return {
            "available": False,
            "matched_ids": 0,
            "same_id_sets": False,
            "classification_mismatches": None,
        }
    left_rows = left["_valid_rows"]
    right_rows = right["_valid_rows"]
    matched_ids = sorted(left_rows.keys() & right_rows.keys())
    mismatches = sum(
        (
            left_rows[instance_id]["true_label"],
            left_rows[instance_id]["prediction"],
            left_rows[instance_id]["prediction_correct"],
        )
        != (
            right_rows[instance_id]["true_label"],
            right_rows[instance_id]["prediction"],
            right_rows[instance_id]["prediction_correct"],
        )
        for instance_id in matched_ids
    )
    return {
        "available": True,
        "left_valid_ids": len(left_rows),
        "right_valid_ids": len(right_rows),
        "matched_ids": len(matched_ids),
        "same_id_sets": bool(left_rows and right_rows)
        and left_rows.keys() == right_rows.keys(),
        "classification_mismatches": mismatches,
    }


def _public_run(run: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in run.items() if not key.startswith("_")}


def audit_sources(root: Path) -> dict[str, Any]:
    root = root.resolve()
    exp2_root = root / "experiments" / "exp2_scaled" / "results"
    exp2_runs: dict[tuple[str, str, str], dict[str, Any]] = {}
    for path in sorted(exp2_root.glob("*/*/*/results.json")):
        model, method = path.parents[2].name.rsplit("_", 1)
        key = (model, path.parents[1].name, path.parents[0].name)
        run = _read_run(path, root)
        run.update({"model": model, "method": method})
        exp2_runs.setdefault(key, {})[method] = run

    method_counts: dict[str, dict[str, int]] = {}
    for method in EXP2_METHODS:
        entries = [
            runs[method]
            for runs in exp2_runs.values()
            if method in runs
        ]
        method_counts[method] = {
            "files": len(entries),
            "nonempty_valid_runs": sum(
                run["unique_valid_id_count"] > 0 for run in entries
            ),
            "source_rows": sum(run["row_count"] for run in entries),
            "valid_rows": sum(run["valid_row_count"] for run in entries),
            "invalid_rows": sum(run["invalid_row_count"] for run in entries),
            "duplicate_ids": sum(len(run["duplicate_ids"]) for run in entries),
        }

    pairwise_counts = {
        f"{left}_{right}": {
            "available_blocks": 0,
            "same_id_blocks": 0,
            "mismatched_id_blocks": 0,
            "matched_ids_total": 0,
            "classification_mismatches": 0,
        }
        for left, right in METHOD_PAIRS
    }
    exp2_blocks = []
    all_four_exact_id_blocks = 0
    for (model, seed, intensity), methods in sorted(exp2_runs.items()):
        pair_audits = {}
        for left, right in METHOD_PAIRS:
            result = _pair_audit(methods.get(left), methods.get(right))
            pair_audits[f"{left}_{right}"] = result
            if result["available"]:
                counts = pairwise_counts[f"{left}_{right}"]
                counts["available_blocks"] += 1
                counts["matched_ids_total"] += result["matched_ids"]
                counts["classification_mismatches"] += (
                    result["classification_mismatches"] or 0
                )
                if result["same_id_sets"]:
                    counts["same_id_blocks"] += 1
                else:
                    counts["mismatched_id_blocks"] += 1
        if all(
            method in methods and methods[method]["unique_valid_id_count"] > 0
            for method in EXP2_METHODS
        ):
            ids = [
                frozenset(methods[method]["_valid_rows"])
                for method in EXP2_METHODS
            ]
            all_four_exact_id_blocks += len(set(ids)) == 1
        exp2_blocks.append(
            {
                "model": model,
                "seed": seed,
                "intensity": intensity,
                "methods": {
                    method: _public_run(run)
                    for method, run in sorted(methods.items())
                },
                "pairwise": pair_audits,
            }
        )

    exp3_runs = []
    exp3_counts = {
        "files": 0,
        "expected_files": (
            len(EXP3_DATASETS) * len(MODELS) * len(SEEDS) * len(EXP3_METHODS)
        ),
        "source_rows": 0,
        "invalid_rows": 0,
        "duplicate_ids": 0,
        "exact_shap_anchor_blocks": 0,
        "classification_mismatches": 0,
    }
    for dataset in EXP3_DATASETS:
        for model in MODELS:
            for seed in SEEDS:
                methods: dict[str, dict[str, Any]] = {}
                for method in EXP3_METHODS:
                    path = (
                        root
                        / "experiments"
                        / "exp3_cross_dataset"
                        / "results"
                        / dataset
                        / f"{model}_{method}"
                        / f"seed_{seed}"
                        / "n_100"
                        / "results.json"
                    )
                    if path.exists():
                        run = _read_run(path, root)
                        run.update({"model": model, "method": method})
                        methods[method] = run
                pair = _pair_audit(methods.get("shap"), methods.get("anchors"))
                for run in methods.values():
                    exp3_counts["files"] += 1
                    exp3_counts["source_rows"] += run["row_count"]
                    exp3_counts["invalid_rows"] += run["invalid_row_count"]
                    exp3_counts["duplicate_ids"] += len(run["duplicate_ids"])
                if pair["available"] and pair["same_id_sets"]:
                    exp3_counts["exact_shap_anchor_blocks"] += 1
                exp3_counts["classification_mismatches"] += (
                    pair["classification_mismatches"] or 0
                )
                exp3_runs.append(
                    {
                        "dataset": dataset,
                        "model": model,
                        "seed": seed,
                        "methods": {
                            method: _public_run(run)
                            for method, run in sorted(methods.items())
                        },
                        "shap_anchors": pair,
                    }
                )

    legacy_lime = root / "outputs" / "analysis" / "exp3_lime_results.csv"
    return {
        "exp2": {
            "source": "experiments/exp2_scaled/results/",
            "run_blocks": len(exp2_runs),
            "method_counts": method_counts,
            "pairwise_counts": pairwise_counts,
            "all_four_exact_id_blocks": all_four_exact_id_blocks,
            "blocks": exp2_blocks,
        },
        "exp3": {
            "source": "experiments/exp3_cross_dataset/results/",
            "counts": exp3_counts,
            "missing_files": exp3_counts["expected_files"] - exp3_counts["files"],
            "legacy_lime_aggregate_exists": legacy_lime.is_file(),
            "legacy_lime_aggregate_path": legacy_lime.relative_to(root).as_posix(),
            "runs": exp3_runs,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/reports/paper_e/DATA_AUDIT.json"),
    )
    args = parser.parse_args()

    root = args.root.resolve()
    audit = audit_sources(root)
    output = args.output if args.output.is_absolute() else root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(audit, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(f"Saved source audit: {output}")
    print(
        "EXP2: "
        f"{audit['exp2']['run_blocks']} blocks, "
        f"{sum(x['invalid_rows'] for x in audit['exp2']['method_counts'].values())} invalid rows, "
        f"{audit['exp2']['pairwise_counts']['shap_lime']['same_id_blocks']} exact "
        "SHAP/LIME ID blocks"
    )
    print(
        "EXP3: "
        f"{audit['exp3']['counts']['files']} files, "
        f"{audit['exp3']['counts']['exact_shap_anchor_blocks']} exact "
        "SHAP/Anchors ID blocks"
    )


if __name__ == "__main__":
    main()
