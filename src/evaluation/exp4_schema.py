"""Schemas for EXP4 LLM-as-evaluator judgments."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


SCORE_FIELDS = [
    "clarity",
    "completeness",
    "concision",
    "semantic_plausibility",
    "audit_usefulness",
    "actionability",
    "overall_quality",
]

PROMPT_CONDITIONS = {
    "hidden_label_primary",
    "label_visible_bias_probe",
    "rubric_alt_sensitivity",
}


class Exp4Case(BaseModel):
    case_id: str
    source_experiment: Literal["exp2_scaled", "exp3_cross_dataset"]
    source_artifact_path: str
    dataset: str
    model_family: str
    explainer: str
    instance_id: str
    prediction: Any = None
    prediction_confidence: Optional[float] = None
    true_label: Any = None
    normalized_explanation: str
    explanation_length_tokens: int = Field(..., ge=1)
    technical_metrics: Dict[str, Optional[float]] = Field(default_factory=dict)
    quadrant: Optional[str] = None
    random_seed: Optional[int] = None
    sample_size: Optional[int] = None

    @field_validator("normalized_explanation")
    @classmethod
    def explanation_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("normalized_explanation must not be empty")
        return value.strip()


class Exp4Scores(BaseModel):
    clarity: int = Field(..., ge=1, le=5)
    completeness: int = Field(..., ge=1, le=5)
    concision: int = Field(..., ge=1, le=5)
    semantic_plausibility: int = Field(..., ge=1, le=5)
    audit_usefulness: int = Field(..., ge=1, le=5)
    actionability: int = Field(..., ge=1, le=5)
    overall_quality: int = Field(..., ge=1, le=5)


class Exp4Rationales(BaseModel):
    clarity: str
    completeness: str
    concision: str
    semantic_plausibility: str
    audit_usefulness: str
    actionability: str
    overall_quality: str

    @field_validator(*SCORE_FIELDS)
    @classmethod
    def rationale_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("rationales must be non-empty strings")
        return value.strip()


class Exp4Flags(BaseModel):
    insufficient_context: bool = False
    format_problem: bool = False
    safety_or_policy_issue: bool = False


class Exp4Judgment(BaseModel):
    case_id: str
    scores: Exp4Scores
    rationales: Exp4Rationales
    flags: Exp4Flags = Field(default_factory=Exp4Flags)


class Exp4JudgeConfig(BaseModel):
    judge_id: Optional[str] = None
    provider: Literal["openai", "gemini", "dummy", "openrouter"]
    model_name: str
    temperature: float = Field(0.0, ge=0.0, le=2.0)
    max_tokens: int = Field(1200, ge=1)


class Exp4ManifestPaths(BaseModel):
    cases_dir: Path = Path("experiments/exp4_llm_evaluation/cases")
    prompts_dir: Path = Path("experiments/exp4_llm_evaluation/prompts")
    raw_responses_dir: Path = Path("experiments/exp4_llm_evaluation/raw_responses")
    parsed_scores_dir: Path = Path("experiments/exp4_llm_evaluation/parsed_scores")
    run_manifests_dir: Path = Path("experiments/exp4_llm_evaluation/run_manifests")
    analysis_dir: Path = Path("outputs/analysis/exp4_llm_evaluation")
    log_file: Path = Path("logs/exp4_llm_evaluation.log")


class Exp4CaseSource(BaseModel):
    name: Literal["exp2_scaled", "exp3_cross_dataset"]
    results_root: Path


class Exp4CaseInventory(BaseModel):
    target_cases: int = Field(192, ge=1)
    random_seed: int = 42
    sources: List[Exp4CaseSource]


class Exp4Manifest(BaseModel):
    experiment_family: Literal["exp4_llm_evaluation"]
    status: str = "implementation_ready"
    schema_version: str = "SCHEMA_V1"
    rubric_version: str = "RUBRIC_V1"
    case_inventory: Exp4CaseInventory
    judges: List[Exp4JudgeConfig]
    prompt_conditions: List[str]
    replicates: int = Field(3, ge=1)
    paths: Exp4ManifestPaths = Field(default_factory=Exp4ManifestPaths)

    @field_validator("prompt_conditions")
    @classmethod
    def known_prompt_conditions(cls, value: List[str]) -> List[str]:
        unknown = sorted(set(value) - PROMPT_CONDITIONS)
        if unknown:
            raise ValueError(f"unknown prompt conditions: {unknown}")
        return value


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def exp4_output_schema(case_id: str = "<case_id>") -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "scores": {field: 1 for field in SCORE_FIELDS},
        "rationales": {field: "string" for field in SCORE_FIELDS},
        "flags": {
            "insufficient_context": False,
            "format_problem": False,
            "safety_or_policy_issue": False,
        },
    }
