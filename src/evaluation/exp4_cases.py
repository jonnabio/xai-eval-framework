"""Case extraction and sampling for EXP4."""

from __future__ import annotations

import csv
import hashlib
import json
import random
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import yaml

from src.evaluation.exp4_schema import Exp4Case, Exp4Manifest


TECHNICAL_METRIC_KEYS = [
    "fidelity",
    "stability",
    "sparsity",
    "faithfulness_gap",
    "runtime_ms",
    "cost",
]


def load_manifest(path: Path) -> Exp4Manifest:
    with path.open("r", encoding="utf-8") as handle:
        return Exp4Manifest(**yaml.safe_load(handle))


def iter_result_files(results_root: Path) -> Iterable[Path]:
    if not results_root.exists():
        return []
    return sorted(results_root.rglob("results.json"))


def load_candidate_cases(manifest: Exp4Manifest) -> List[Exp4Case]:
    cases: List[Exp4Case] = []
    for source in manifest.case_inventory.sources:
        for result_path in iter_result_files(source.results_root):
            cases.extend(_cases_from_results_file(result_path, source.name))
    return cases


def sample_cases(cases: List[Exp4Case], target_cases: int, seed: int) -> List[Exp4Case]:
    if len(cases) <= target_cases:
        return sorted(cases, key=lambda case: case.case_id)

    by_source: Dict[str, List[Exp4Case]] = defaultdict(list)
    for case in cases:
        by_source[case.source_experiment].append(case)
    if len(by_source) > 1:
        selected: List[Exp4Case] = []
        sources = sorted(by_source)
        base_quota = target_cases // len(sources)
        remainder = target_cases % len(sources)
        shortfall = 0
        for index, source in enumerate(sources):
            quota = base_quota + (1 if index < remainder else 0)
            source_cases = by_source[source]
            if len(source_cases) < quota:
                shortfall += quota - len(source_cases)
                quota = len(source_cases)
            selected.extend(_sample_cases_within_pool(source_cases, quota, seed + index))

        if shortfall:
            selected_ids = {case.case_id for case in selected}
            remaining = [case for case in cases if case.case_id not in selected_ids]
            selected.extend(_sample_cases_within_pool(remaining, shortfall, seed + len(sources)))

        return sorted(selected[:target_cases], key=lambda case: case.case_id)

    return _sample_cases_within_pool(cases, target_cases, seed)


def _sample_cases_within_pool(cases: List[Exp4Case], target_cases: int, seed: int) -> List[Exp4Case]:
    if len(cases) <= target_cases:
        return sorted(cases, key=lambda case: case.case_id)

    by_bucket: Dict[str, List[Exp4Case]] = defaultdict(list)
    medians = _metric_medians(cases)
    for case in cases:
        bucket = "|".join(
            [
                case.source_experiment,
                case.dataset,
                case.model_family,
                case.explainer,
                case.quadrant or "unknown",
                _metric_profile(case, medians),
            ]
        )
        by_bucket[bucket].append(case)

    rng = random.Random(seed)
    for bucket_cases in by_bucket.values():
        rng.shuffle(bucket_cases)

    selected: List[Exp4Case] = []
    bucket_names = sorted(by_bucket)
    while len(selected) < target_cases and bucket_names:
        next_round = []
        for bucket in bucket_names:
            if by_bucket[bucket] and len(selected) < target_cases:
                selected.append(by_bucket[bucket].pop())
            if by_bucket[bucket]:
                next_round.append(bucket)
        bucket_names = next_round

    return sorted(selected, key=lambda case: case.case_id)


def write_case_inventory(
    cases: List[Exp4Case],
    all_candidates: List[Exp4Case],
    output_dir: Path,
    target_cases: int,
    seed: int,
) -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = output_dir / "exp4_cases.jsonl"
    csv_path = output_dir / "exp4_cases.csv"
    report_path = output_dir / "exp4_sampling_report.json"

    with jsonl_path.open("w", encoding="utf-8") as handle:
        for case in cases:
            handle.write(json.dumps(case.model_dump(mode="json"), ensure_ascii=False) + "\n")

    rows = [case.model_dump(mode="json") for case in cases]
    fieldnames = [
        "case_id",
        "source_experiment",
        "source_artifact_path",
        "dataset",
        "model_family",
        "explainer",
        "instance_id",
        "prediction",
        "prediction_confidence",
        "true_label",
        "normalized_explanation",
        "explanation_length_tokens",
        "quadrant",
        "random_seed",
        "sample_size",
        "technical_metrics",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row["technical_metrics"] = json.dumps(row["technical_metrics"], sort_keys=True)
            writer.writerow({key: row.get(key) for key in fieldnames})

    report = {
        "target_cases": target_cases,
        "selected_cases": len(cases),
        "candidate_cases": len(all_candidates),
        "random_seed": seed,
        "jsonl_path": str(jsonl_path),
        "csv_path": str(csv_path),
        "by_source": _count_by(cases, "source_experiment"),
        "by_dataset": _count_by(cases, "dataset"),
        "by_explainer": _count_by(cases, "explainer"),
        "shortfall": max(target_cases - len(cases), 0),
    }
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def read_cases_jsonl(path: Path) -> List[Exp4Case]:
    cases = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                cases.append(Exp4Case(**json.loads(line)))
    return cases


def build_case_inventory(manifest_path: Path, target_cases: Optional[int] = None, seed: Optional[int] = None) -> Dict[str, Any]:
    manifest = load_manifest(manifest_path)
    target = target_cases or manifest.case_inventory.target_cases
    random_seed = seed if seed is not None else manifest.case_inventory.random_seed
    candidates = load_candidate_cases(manifest)
    selected = sample_cases(candidates, target, random_seed)
    return write_case_inventory(selected, candidates, manifest.paths.cases_dir, target, random_seed)


def _cases_from_results_file(result_path: Path, source_experiment: str) -> List[Exp4Case]:
    try:
        payload = json.loads(result_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    evaluations = payload.get("instance_evaluations") or []
    if not isinstance(evaluations, list):
        return []

    metadata = payload.get("experiment_metadata") or {}
    model_info = payload.get("model_info") or {}
    dataset = str(metadata.get("dataset") or _infer_dataset(result_path))
    model_family = _normalize_model_family(model_info.get("name") or result_path)
    explainer = str(model_info.get("explainer_method") or _infer_explainer(result_path)).lower()
    random_seed = _safe_int(metadata.get("random_seed") or _path_value(result_path, r"seed_(\d+)"))
    sample_size = _safe_int(_path_value(result_path, r"n_(\d+)"))

    cases: List[Exp4Case] = []
    for evaluation in evaluations:
        if not isinstance(evaluation, dict):
            continue
        explanation = _normalize_explanation(evaluation.get("explanation"), explainer)
        if not explanation:
            continue
        metrics = _normalize_metrics(evaluation.get("metrics") or {})
        instance_id = str(evaluation.get("instance_id", "unknown"))
        case_id = _stable_case_id(
            source_experiment,
            dataset,
            model_family,
            explainer,
            str(random_seed),
            str(sample_size),
            instance_id,
            str(result_path),
        )
        try:
            cases.append(
                Exp4Case(
                    case_id=case_id,
                    source_experiment=source_experiment,
                    source_artifact_path=str(result_path),
                    dataset=dataset,
                    model_family=model_family,
                    explainer=explainer,
                    instance_id=instance_id,
                    prediction=evaluation.get("prediction"),
                    prediction_confidence=_safe_float(evaluation.get("prediction_confidence")),
                    true_label=evaluation.get("true_label"),
                    normalized_explanation=explanation,
                    explanation_length_tokens=_count_tokens(explanation),
                    technical_metrics=metrics,
                    quadrant=evaluation.get("quadrant"),
                    random_seed=random_seed,
                    sample_size=sample_size,
                )
            )
        except ValueError:
            continue
    return cases


def _normalize_explanation(explanation: Any, explainer: str) -> str:
    if explanation is None:
        return ""
    if isinstance(explanation, str):
        return explanation.strip()
    if not isinstance(explanation, dict):
        return str(explanation).strip()

    top_features = explanation.get("top_features") or explanation.get("raw_top")
    if isinstance(top_features, list) and top_features:
        parts = []
        for item in top_features[:10]:
            if isinstance(item, dict):
                feature = item.get("feature") or item.get("name") or item.get("column") or "feature"
                value = item.get("value", item.get("importance", item.get("weight", item.get("effect"))))
                sign = item.get("direction") or item.get("sign")
                if value is None:
                    parts.append(f"{feature}")
                elif sign:
                    parts.append(f"{feature}: {value} ({sign})")
                else:
                    parts.append(f"{feature}: {value}")
            elif isinstance(item, (list, tuple)) and len(item) >= 2:
                parts.append(f"{item[0]}: {item[1]}")
            else:
                parts.append(str(item))
        return f"{explainer.upper()} top local factors: " + "; ".join(parts)

    for key in ("rule", "anchor", "counterfactual", "text", "summary"):
        value = explanation.get(key)
        if value:
            return f"{explainer.upper()} explanation: {value}"

    compact = json.dumps(explanation, sort_keys=True, default=str)
    return f"{explainer.upper()} explanation details: {compact[:1200]}"


def _normalize_metrics(metrics: Dict[str, Any]) -> Dict[str, Optional[float]]:
    normalized = {}
    for key in TECHNICAL_METRIC_KEYS:
        normalized[key] = _safe_float(metrics.get(key))
    if normalized.get("runtime_ms") is None and normalized.get("cost") is not None:
        normalized["runtime_ms"] = normalized["cost"]
    return normalized


def _stable_case_id(*parts: str) -> str:
    digest = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"exp4_{digest}"


def _count_tokens(text: str) -> int:
    return max(1, len(re.findall(r"\w+|[^\w\s]", text)))


def _safe_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _safe_int(value: Any) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _infer_dataset(path: Path) -> str:
    parts = [part.lower() for part in path.parts]
    for dataset in ("adult", "breast_cancer", "german_credit"):
        if dataset in parts or dataset.replace("_", "-") in parts:
            return dataset
    return "unknown"


def _infer_explainer(path: Path) -> str:
    text = str(path).lower()
    for explainer in ("anchors", "shap", "lime", "dice"):
        if explainer in text:
            return explainer
    return "unknown"


def _normalize_model_family(value: Any) -> str:
    text = str(value).lower()
    for model in ("logreg", "xgb", "svm", "mlp", "rf"):
        if re.search(rf"(^|[_/\-]){model}($|[_/\-])", text):
            return model
    return Path(text).stem or "unknown"


def _path_value(path: Path, pattern: str) -> Optional[str]:
    match = re.search(pattern, str(path))
    return match.group(1) if match else None


def _metric_medians(cases: List[Exp4Case]) -> Dict[str, float]:
    medians = {}
    for key in ("fidelity", "stability"):
        values = sorted(v for case in cases if (v := case.technical_metrics.get(key)) is not None)
        if values:
            medians[key] = values[len(values) // 2]
    return medians


def _metric_profile(case: Exp4Case, medians: Dict[str, float]) -> str:
    labels = []
    for key in ("fidelity", "stability"):
        value = case.technical_metrics.get(key)
        median = medians.get(key)
        if value is None or median is None:
            labels.append(f"{key}_unknown")
        elif value >= median:
            labels.append(f"{key}_high")
        else:
            labels.append(f"{key}_low")
    return "|".join(labels)


def _count_by(cases: List[Exp4Case], field: str) -> Dict[str, int]:
    counts: Dict[str, int] = defaultdict(int)
    for case in cases:
        counts[str(getattr(case, field))] += 1
    return dict(sorted(counts.items()))
