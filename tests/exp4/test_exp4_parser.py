import json

from src.evaluation.exp4_parser import parse_judgment_text, strip_json_fences


VALID_RESPONSE = {
    "case_id": "case-1",
    "scores": {
        "clarity": 4,
        "completeness": 4,
        "concision": 4,
        "semantic_plausibility": 4,
        "audit_usefulness": 4,
        "actionability": 3,
        "overall_quality": 4,
    },
    "rationales": {
        "clarity": "Clear.",
        "completeness": "Complete enough.",
        "concision": "Concise.",
        "semantic_plausibility": "Plausible.",
        "audit_usefulness": "Useful.",
        "actionability": "Some review value.",
        "overall_quality": "Strong.",
    },
    "flags": {
        "insufficient_context": False,
        "format_problem": False,
        "safety_or_policy_issue": False,
    },
}


def test_strip_json_fences():
    text = "```json\n{\"case_id\": \"case-1\"}\n```"
    assert strip_json_fences(text) == '{"case_id": "case-1"}'


def test_parse_judgment_text():
    judgment = parse_judgment_text(json.dumps(VALID_RESPONSE))
    assert judgment.case_id == "case-1"
    assert judgment.scores.overall_quality == 4
