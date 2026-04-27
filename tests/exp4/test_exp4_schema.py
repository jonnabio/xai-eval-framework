import pytest
from pydantic import ValidationError

from src.evaluation.exp4_schema import Exp4Case, Exp4Judgment


def test_exp4_judgment_accepts_valid_schema():
    judgment = Exp4Judgment(
        case_id="case-1",
        scores={
            "clarity": 4,
            "completeness": 3,
            "concision": 5,
            "semantic_plausibility": 4,
            "audit_usefulness": 4,
            "actionability": 3,
            "overall_quality": 4,
        },
        rationales={
            "clarity": "Clear structure.",
            "completeness": "Main factors are present.",
            "concision": "Compact.",
            "semantic_plausibility": "Coherent with the provided context.",
            "audit_usefulness": "Useful for inspection.",
            "actionability": "Supports review.",
            "overall_quality": "Good overall.",
        },
        flags={},
    )

    assert judgment.scores.clarity == 4
    assert judgment.flags.insufficient_context is False


def test_exp4_judgment_rejects_out_of_range_score():
    with pytest.raises(ValidationError):
        Exp4Judgment(
            case_id="case-1",
            scores={
                "clarity": 6,
                "completeness": 3,
                "concision": 5,
                "semantic_plausibility": 4,
                "audit_usefulness": 4,
                "actionability": 3,
                "overall_quality": 4,
            },
            rationales={field: "ok" for field in [
                "clarity",
                "completeness",
                "concision",
                "semantic_plausibility",
                "audit_usefulness",
                "actionability",
                "overall_quality",
            ]},
            flags={},
        )


def test_exp4_case_requires_non_empty_explanation():
    with pytest.raises(ValidationError):
        Exp4Case(
            case_id="case-1",
            source_experiment="exp2_scaled",
            source_artifact_path="results.json",
            dataset="adult",
            model_family="rf",
            explainer="shap",
            instance_id="1",
            normalized_explanation=" ",
            explanation_length_tokens=1,
        )
