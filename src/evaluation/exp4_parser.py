"""Parser and CSV export for EXP4 raw LLM responses."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from pydantic import ValidationError

from src.evaluation.exp4_cases import load_manifest
from src.evaluation.exp4_schema import Exp4Judgment, SCORE_FIELDS


def strip_json_fences(text: str) -> str:
    cleaned = text.strip()
    match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", cleaned, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else cleaned


def parse_judgment_text(text: str) -> Exp4Judgment:
    payload = json.loads(strip_json_fences(text))
    return Exp4Judgment(**payload)


def iter_raw_response_files(raw_dir: Path) -> Iterable[Path]:
    if not raw_dir.exists():
        return []
    return sorted(raw_dir.rglob("*.json"))


def parse_raw_response_file(path: Path) -> Tuple[Dict[str, Any], Exp4Judgment | None, str | None]:
    envelope = json.loads(path.read_text(encoding="utf-8"))
    response_text = envelope.get("response_text", "")
    try:
        return envelope, parse_judgment_text(response_text), None
    except (json.JSONDecodeError, ValidationError, TypeError, ValueError) as exc:
        return envelope, None, f"{type(exc).__name__}: {exc}"


def parse_manifest_responses(manifest_path: Path) -> Dict[str, Any]:
    manifest = load_manifest(manifest_path)
    output_dir = manifest.paths.parsed_scores_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    rows: List[Dict[str, Any]] = []
    failures: List[Dict[str, Any]] = []
    raw_files = list(iter_raw_response_files(manifest.paths.raw_responses_dir))
    for raw_path in raw_files:
        envelope, judgment, error = parse_raw_response_file(raw_path)
        if judgment is None:
            failures.append(_failure_row(envelope, raw_path, error or "unknown parse failure"))
        else:
            rows.append(_score_row(envelope, judgment, raw_path))

    scores_path = output_dir / "exp4_llm_scores.csv"
    failures_path = output_dir / "exp4_parse_failures.csv"
    summary_path = output_dir / "exp4_parse_summary.json"

    _write_csv(scores_path, rows, _score_fieldnames())
    _write_csv(failures_path, failures, _failure_fieldnames())
    summary = {
        "raw_response_count": len(raw_files),
        "parsed_count": len(rows),
        "failure_count": len(failures),
        "scores_path": str(scores_path),
        "failures_path": str(failures_path),
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def _score_row(envelope: Dict[str, Any], judgment: Exp4Judgment, raw_path: Path) -> Dict[str, Any]:
    row = {
        "judgment_id": envelope.get("judgment_id"),
        "case_id": judgment.case_id,
        "judge_model": envelope.get("judge_model"),
        "provider": envelope.get("provider"),
        "model_version": envelope.get("model_version") or envelope.get("judge_model"),
        "prompt_condition": envelope.get("prompt_condition"),
        "prompt_version": envelope.get("prompt_version"),
        "rubric_version": envelope.get("rubric_version"),
        "replicate": envelope.get("replicate"),
        "temperature": envelope.get("temperature"),
        "raw_response_path": str(raw_path),
        "parse_status": "parsed",
        "timestamp_utc": envelope.get("timestamp_utc"),
        "insufficient_context": judgment.flags.insufficient_context,
        "format_problem": judgment.flags.format_problem,
        "safety_or_policy_issue": judgment.flags.safety_or_policy_issue,
    }
    scores = judgment.scores.model_dump()
    rationales = judgment.rationales.model_dump()
    for field in SCORE_FIELDS:
        row[f"{field}_score"] = scores[field]
        row[f"{field}_rationale"] = rationales[field]
    return row


def _failure_row(envelope: Dict[str, Any], raw_path: Path, error: str) -> Dict[str, Any]:
    return {
        "judgment_id": envelope.get("judgment_id"),
        "case_id": envelope.get("case_id"),
        "judge_model": envelope.get("judge_model"),
        "prompt_condition": envelope.get("prompt_condition"),
        "replicate": envelope.get("replicate"),
        "failure_type": error.split(":", 1)[0],
        "failure_message": error,
        "raw_response_path": str(raw_path),
        "retry_count": envelope.get("retry_count", 0),
        "timestamp_utc": envelope.get("timestamp_utc"),
    }


def _write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def _score_fieldnames() -> List[str]:
    fields = [
        "judgment_id",
        "case_id",
        "judge_model",
        "provider",
        "model_version",
        "prompt_condition",
        "prompt_version",
        "rubric_version",
        "replicate",
        "temperature",
        "raw_response_path",
        "parse_status",
    ]
    fields.extend(f"{field}_score" for field in SCORE_FIELDS)
    fields.extend(f"{field}_rationale" for field in SCORE_FIELDS)
    fields.extend(["insufficient_context", "format_problem", "safety_or_policy_issue", "timestamp_utc"])
    return fields


def _failure_fieldnames() -> List[str]:
    return [
        "judgment_id",
        "case_id",
        "judge_model",
        "prompt_condition",
        "replicate",
        "failure_type",
        "failure_message",
        "raw_response_path",
        "retry_count",
        "timestamp_utc",
    ]
