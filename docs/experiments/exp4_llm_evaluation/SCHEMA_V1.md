# EXP4 Schema V1

## Case Schema

Required fields for each EXP4 case:

```json
{
  "case_id": "string",
  "source_experiment": "exp2_scaled | exp3_cross_dataset",
  "source_artifact_path": "string",
  "dataset": "string",
  "model_family": "string",
  "explainer": "string",
  "instance_id": "string",
  "prediction": "string | number | null",
  "prediction_confidence": "number | null",
  "true_label": "string | number | null",
  "normalized_explanation": "string",
  "explanation_length_tokens": "integer",
  "technical_metrics": {
    "fidelity": "number | null",
    "stability": "number | null",
    "sparsity": "number | null",
    "faithfulness_gap": "number | null",
    "runtime_ms": "number | null"
  }
}
```

## LLM Output Schema

Required JSON response from the LLM judge:

```json
{
  "case_id": "string",
  "scores": {
    "clarity": 1,
    "completeness": 1,
    "concision": 1,
    "semantic_plausibility": 1,
    "audit_usefulness": 1,
    "actionability": 1,
    "overall_quality": 1
  },
  "rationales": {
    "clarity": "string",
    "completeness": "string",
    "concision": "string",
    "semantic_plausibility": "string",
    "audit_usefulness": "string",
    "actionability": "string",
    "overall_quality": "string"
  },
  "flags": {
    "insufficient_context": false,
    "format_problem": false,
    "safety_or_policy_issue": false
  }
}
```

Score values must be integers from 1 to 5.

## Parsed Judgment Table

Minimum columns:

```text
judgment_id
case_id
judge_model
provider
model_version
prompt_condition
prompt_version
rubric_version
replicate
temperature
raw_response_path
parse_status
clarity_score
completeness_score
concision_score
semantic_plausibility_score
audit_usefulness_score
actionability_score
overall_quality_score
clarity_rationale
completeness_rationale
concision_rationale
semantic_plausibility_rationale
audit_usefulness_rationale
actionability_rationale
overall_quality_rationale
timestamp_utc
```

## Failure Table

Minimum columns:

```text
judgment_id
case_id
judge_model
prompt_condition
replicate
failure_type
failure_message
raw_response_path
retry_count
timestamp_utc
```
