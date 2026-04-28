# EXP4 Results: LLM-Based Semantic Evaluation

## Purpose

This document defines the planned result semantics for EXP4.

It is the result-side companion to
[docs/experiments/exp4_llm_evaluation/README.md](../../experiments/exp4_llm_evaluation/README.md).

## Current Status

Status:

- fixed case inventory generated;
- 5-case dry run completed;
- OpenRouter one-case connectivity pilot completed;
- OpenRouter 24-case hidden-label pilot completed.

Current result notes:

- [OpenRouter pilot results](./openrouter_pilot_results.md)
- [OpenRouter label-visible bias-probe results](./openrouter_bias_probe_results.md)
- [OpenRouter 24-case complete pilot](./openrouter_24_case_pilot_complete.md)
- [Attribution versus explanation interpretation note](./attribution_vs_explanation_note.md)

## Planned Raw Artifact Root

Planned root:

```text
experiments/exp4_llm_evaluation/
```

Recommended layout:

```text
experiments/exp4_llm_evaluation/
  cases/
    exp4_cases.csv
    exp4_cases.jsonl
  prompts/
    rubric_v1.md
    system_prompt_v1.md
  raw_responses/
    <judge_model>/<prompt_version>/<case_id>/run_<replicate>.json
  parsed_scores/
    exp4_llm_scores.csv
    exp4_parse_failures.csv
```

## Planned Derived Output Root

Planned root:

```text
outputs/analysis/exp4_llm_evaluation/
```

Recommended outputs:

- case inventory and sampling report;
- score distributions by method, dataset, and judge model;
- inter-run stability tables;
- inter-judge agreement tables;
- metric-alignment analysis with EXP2/EXP3 technical metrics;
- bias diagnostics for length, method-label visibility, and prompt variant;
- thesis-ready summary fragments.

## Case-Level Contract

Each EXP4 case should have:

- stable `case_id`;
- source experiment family (`exp2_scaled` or `exp3_cross_dataset`);
- source artifact path;
- dataset;
- model family;
- explainer;
- prediction and model confidence if available;
- true label if available;
- normalized explanation text;
- structured explanation fields where available;
- linked technical metrics.

## Judgment-Level Contract

Each LLM judgment should have:

- `case_id`;
- judge model identifier;
- model provider;
- model version or dated alias;
- prompt version;
- rubric version;
- replicate index;
- temperature and decoding parameters;
- raw response path;
- parsed numeric scores;
- rationale text;
- parse status;
- timestamp.

## Planned Semantic Dimensions

The default rubric dimensions are:

- clarity;
- completeness;
- concision;
- semantic plausibility;
- audit usefulness;
- actionability or decision support;
- overall explanation quality.

Scores should use a 1-5 ordinal scale unless the experiment design ADR revises
the rubric.

## Interpretation Rules

EXP4 results should be interpreted as LLM-based semantic proxy evidence.

The central interpretation distinction is documented in
[Attribution Is Not Yet Explanation](./attribution_vs_explanation_note.md).
Many XAI artifacts are compact attribution lists. EXP4 evaluates whether those
artifacts are also usable as explanations for audit and decision review.

EXP4 may support:

- semantic profile comparisons between explanation methods;
- stability/reproducibility analysis of LLM rubric scores;
- relationship analysis between technical metrics and semantic scores.

EXP4 must not be interpreted as:

- direct human-centered validation;
- evidence of actual user trust or comprehension;
- a substitute for expert or end-user studies.

## Source-of-Truth Rules

For planned experiment design:

- [docs/experiments/exp4_llm_evaluation/README.md](../../experiments/exp4_llm_evaluation/README.md)

For planned execution:

- [docs/planning/exp4_llm_evaluation_plan.md](../../planning/exp4_llm_evaluation_plan.md)

For future raw outputs:

- `experiments/exp4_llm_evaluation/`

For future derived analysis:

- `outputs/analysis/exp4_llm_evaluation/`
