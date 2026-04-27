"""Prompt rendering for EXP4 LLM evaluation."""

from __future__ import annotations

import hashlib
import json
from typing import Dict

from src.evaluation.exp4_schema import Exp4Case, exp4_output_schema
from src.prompts.engine import PromptEngine


TEMPLATE_BY_CONDITION: Dict[str, str] = {
    "hidden_label_primary": "exp4_semantic_eval_v1.j2",
    "label_visible_bias_probe": "exp4_semantic_eval_v1_label_visible.j2",
    "rubric_alt_sensitivity": "exp4_semantic_eval_v1_alt.j2",
}


def render_exp4_prompt(
    case: Exp4Case,
    prompt_condition: str,
    rubric_version: str = "RUBRIC_V1",
    engine: PromptEngine | None = None,
) -> str:
    if prompt_condition not in TEMPLATE_BY_CONDITION:
        raise ValueError(f"Unknown EXP4 prompt condition: {prompt_condition}")
    prompt_engine = engine or PromptEngine()
    case_payload = case.model_dump(mode="json")
    if prompt_condition == "hidden_label_primary":
        case_payload["true_label"] = None
    prompt = prompt_engine.render(
        TEMPLATE_BY_CONDITION[prompt_condition],
        rubric_version=rubric_version,
        prompt_condition=prompt_condition,
        case_json=json.dumps(case_payload, indent=2, sort_keys=True, ensure_ascii=False),
        output_schema_json=json.dumps(exp4_output_schema(case.case_id), indent=2, sort_keys=True),
    )
    return prompt.strip()


def prompt_version_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
