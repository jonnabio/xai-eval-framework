"""Runner for EXP4 LLM judge execution."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.evaluation.exp4_cases import load_manifest, read_cases_jsonl
from src.evaluation.exp4_prompts import prompt_version_hash, render_exp4_prompt
from src.evaluation.exp4_schema import Exp4Case, Exp4JudgeConfig, SCORE_FIELDS, exp4_output_schema, utc_now_iso
from src.experiment.config import LLMConfig
from src.llm.client import LLMClientFactory


def run_exp4_judges(
    manifest_path: Path,
    dry_run: bool = False,
    limit: Optional[int] = None,
    replicates: Optional[int] = None,
    condition: Optional[str] = None,
    judge_id: Optional[str] = None,
    force: bool = False,
) -> Dict[str, Any]:
    manifest = load_manifest(manifest_path)
    cases_path = manifest.paths.cases_dir / "exp4_cases.jsonl"
    cases = read_cases_jsonl(cases_path)
    if limit is not None:
        cases = cases[:limit]

    conditions = [condition] if condition else list(manifest.prompt_conditions)
    run_replicates = replicates or manifest.replicates
    raw_dir = manifest.paths.raw_responses_dir
    prompt_dir = manifest.paths.prompts_dir
    run_manifest_dir = manifest.paths.run_manifests_dir
    raw_dir.mkdir(parents=True, exist_ok=True)
    prompt_dir.mkdir(parents=True, exist_ok=True)
    run_manifest_dir.mkdir(parents=True, exist_ok=True)

    judges = manifest.judges if not dry_run else [_dry_run_judge()]
    if judge_id:
        judges = [judge for judge in judges if judge_key(judge) == judge_id]
        if not judges:
            raise ValueError(f"No EXP4 judge configured with judge_id={judge_id}")
    clients = {
        judge_key(judge): None if dry_run else LLMClientFactory.create(_to_llm_config(judge))
        for judge in judges
    }

    written = 0
    skipped = 0
    for case in cases:
        for judge in judges:
            key = judge_key(judge)
            for prompt_condition in conditions:
                prompt = render_exp4_prompt(case, prompt_condition, manifest.rubric_version)
                p_hash = prompt_version_hash(prompt)
                _write_prompt_once(prompt_dir, case.case_id, prompt_condition, p_hash, prompt)
                for replicate in range(1, run_replicates + 1):
                    judgment_id = build_judgment_id(case.case_id, key, prompt_condition, replicate)
                    output_path = raw_dir / key / prompt_condition / f"{judgment_id}.json"
                    if output_path.exists() and not force:
                        skipped += 1
                        continue
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    response_text = (
                        _dummy_response(case, prompt_condition, replicate)
                        if dry_run
                        else clients[key].generate(prompt)
                    )
                    envelope = _response_envelope(
                        judgment_id=judgment_id,
                        case=case,
                        judge=judge,
                        prompt_condition=prompt_condition,
                        prompt_version=p_hash,
                        rubric_version=manifest.rubric_version,
                        replicate=replicate,
                        prompt_path=str(_prompt_path(prompt_dir, case.case_id, prompt_condition, p_hash)),
                        response_text=response_text,
                        dry_run=dry_run,
                    )
                    output_path.write_text(json.dumps(envelope, indent=2, sort_keys=True), encoding="utf-8")
                    written += 1

    run_summary = {
        "timestamp_utc": utc_now_iso(),
        "manifest_path": str(manifest_path),
        "dry_run": dry_run,
        "case_count": len(cases),
        "judge_count": len(judges),
        "conditions": conditions,
        "replicates": run_replicates,
        "written_responses": written,
        "skipped_existing": skipped,
    }
    summary_path = run_manifest_dir / f"run_{utc_now_iso().replace(':', '').replace('+', 'Z')}.json"
    summary_path.write_text(json.dumps(run_summary, indent=2, sort_keys=True), encoding="utf-8")
    run_summary["run_manifest_path"] = str(summary_path)
    return run_summary


def build_judgment_id(case_id: str, judge: str, condition: str, replicate: int) -> str:
    digest = hashlib.sha1(f"{case_id}|{judge}|{condition}|{replicate}".encode("utf-8")).hexdigest()[:16]
    return f"j_{digest}"


def judge_key(judge: Exp4JudgeConfig) -> str:
    return judge.judge_id or f"{judge.provider}_{judge.model_name}".replace("/", "_").replace(":", "_")


def _to_llm_config(judge: Exp4JudgeConfig) -> LLMConfig:
    return LLMConfig(
        provider=judge.provider,
        model_name=judge.model_name,
        temperature=judge.temperature,
        max_tokens=judge.max_tokens,
    )


def _dry_run_judge() -> Exp4JudgeConfig:
    return Exp4JudgeConfig(
        judge_id="dummy_exp4",
        provider="dummy",
        model_name="exp4-dummy-judge",
        temperature=0,
        max_tokens=1200,
    )


def _dummy_response(case: Exp4Case, prompt_condition: str, replicate: int) -> str:
    base = 3
    if case.explanation_length_tokens < 35:
        concision = 5
        completeness = 3
    elif case.explanation_length_tokens > 180:
        concision = 2
        completeness = 4
    else:
        concision = 4
        completeness = 4
    if prompt_condition == "rubric_alt_sensitivity":
        base += 1
    if replicate > 1:
        base = max(1, min(5, base + ((replicate % 2) - 0)))
    scores = {
        "clarity": min(5, base + 1),
        "completeness": completeness,
        "concision": concision,
        "semantic_plausibility": base,
        "audit_usefulness": min(5, completeness + 1),
        "actionability": base,
        "overall_quality": min(5, round((base + completeness + concision) / 3)),
    }
    response = exp4_output_schema(case.case_id)
    response["scores"] = scores
    response["rationales"] = {
        field: f"Dry-run rationale for {field} based on the normalized explanation and EXP4 rubric."
        for field in SCORE_FIELDS
    }
    return json.dumps(response)


def _write_prompt_once(prompt_dir: Path, case_id: str, condition: str, prompt_hash: str, prompt: str) -> None:
    path = _prompt_path(prompt_dir, case_id, condition, prompt_hash)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(prompt, encoding="utf-8")


def _prompt_path(prompt_dir: Path, case_id: str, condition: str, prompt_hash: str) -> Path:
    return prompt_dir / condition / f"{case_id}_{prompt_hash}.txt"


def _response_envelope(
    judgment_id: str,
    case: Exp4Case,
    judge: Exp4JudgeConfig,
    prompt_condition: str,
    prompt_version: str,
    rubric_version: str,
    replicate: int,
    prompt_path: str,
    response_text: str,
    dry_run: bool,
) -> Dict[str, Any]:
    return {
        "judgment_id": judgment_id,
        "case_id": case.case_id,
        "judge_model": judge.model_name,
        "provider": judge.provider,
        "model_version": judge.model_name,
        "prompt_condition": prompt_condition,
        "prompt_version": prompt_version,
        "rubric_version": rubric_version,
        "replicate": replicate,
        "temperature": judge.temperature,
        "prompt_path": prompt_path,
        "response_text": response_text,
        "retry_count": 0,
        "dry_run": dry_run,
        "timestamp_utc": utc_now_iso(),
    }
