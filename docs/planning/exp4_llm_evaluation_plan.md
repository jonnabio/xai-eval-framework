# EXP4 LLM Evaluation Plan

## Status

Status: draft plan, not executed.

This plan operationalizes EXP4 as an LLM-based semantic proxy evaluation layer
for selected explanation artifacts from EXP2 and EXP3.

The full scientific protocol is defined in
[docs/experiments/exp4_llm_evaluation/DETAILED_DESIGN.md](../experiments/exp4_llm_evaluation/DETAILED_DESIGN.md).

The code implementation plan is defined in
[docs/planning/exp4_implementation_plan.md](./exp4_implementation_plan.md).

## Objective

Design a reproducible LLM-evaluation workflow that scores XAI explanations on
semantic dimensions not captured directly by technical metrics.

The goal is to evaluate LLMs as rubric-based proxy judges, not to validate human
interpretability directly.

## Inputs

Candidate source experiments:

- EXP2 Adult benchmark:
  - SHAP;
  - LIME;
  - Anchors;
  - DiCE where valid artifacts exist.
- EXP3 cross-dataset validation:
  - SHAP;
  - Anchors;
  - Breast Cancer;
  - German Credit.

Each sampled case should link back to source metrics so EXP4 can analyze
alignment between semantic scores and technical evidence.

## Sampling Plan

Recommended initial design:

| Factor | Values |
|---|---|
| Source | EXP2, EXP3 |
| Dataset | Adult, Breast Cancer, German Credit |
| Explainer | SHAP, LIME, Anchors, DiCE where available |
| Model | Prefer RF/XGB for cross-study comparability; sample other EXP2 models if needed |
| Prediction class | Stratified by class |
| Confidence | Low, medium, high where prediction probability is available |
| Technical profile | High/low fidelity and high/low stability |

Recommended starting size:

- 120 to 240 cases.

## Evaluation Units

One evaluation unit is:

```text
case x judge_model x prompt_version x replicate
```

Recommended minimum:

- 2 judge models;
- 1 primary rubric prompt;
- 1 robustness prompt variant;
- 3 repeated judgments per case.

## Prompting Contract

Prompts should include:

- task role: evaluator of XAI explanations;
- dataset/domain context;
- model prediction and confidence where available;
- normalized explanation;
- rubric definitions;
- required JSON output schema;
- instruction not to infer protected attributes or unstated facts;
- instruction to score only the explanation presented.

Prompts should avoid:

- exposing method labels when testing unbiased semantic quality;
- revealing technical metric values before the LLM judgment;
- asking the LLM to decide whether a model is legally or clinically valid.

## Rubric

Default score scale:

- 1 = very poor;
- 2 = weak;
- 3 = adequate;
- 4 = strong;
- 5 = excellent.

Default dimensions:

- clarity;
- completeness;
- concision;
- semantic plausibility;
- audit usefulness;
- actionability or decision support;
- overall explanation quality.

Every score must include a concise rationale.

Use [RUBRIC_V1.md](../experiments/exp4_llm_evaluation/RUBRIC_V1.md) unless a
new rubric version is accepted before execution.

## Bias Controls

EXP4 should include the following controls:

- blind method names in the primary condition;
- randomized case order;
- explanation presentation templates normalized across methods;
- explanation length recorded as a covariate;
- repeated judgments for stability;
- model-version and prompt-version pinning;
- parse-failure and retry logging.

Optional robustness checks:

- label-visible condition to estimate method-label bias;
- reversed order for paired comparisons;
- alternative rubric wording to estimate prompt sensitivity.

## Analysis

Primary outputs:

- score summaries by method, dataset, model, and judge;
- inter-run reliability for repeated LLM judgments;
- inter-judge agreement across LLMs;
- correlation of semantic scores with technical metrics;
- method-level semantic profile comparison;
- bias diagnostics for explanation length and prompt variant.

Recommended tests:

- Spearman or Kendall correlation for score/metric alignment;
- Krippendorff's alpha or ICC for reliability;
- bootstrap confidence intervals for method-level means;
- nonparametric method comparisons where score distributions are ordinal.

## Acceptance Criteria

EXP4 is ready to execute when:

- case sampler is implemented and produces stable case IDs;
- rubric prompt and JSON schema are frozen;
- [SCHEMA_V1.md](../experiments/exp4_llm_evaluation/SCHEMA_V1.md) has been
  implemented by the parser;
- at least one parser validation test passes on mock LLM responses;
- raw-response and parsed-score directories are created;
- a dry run produces valid scores for at least 5 cases;
- the thesis claim boundary is documented.

## Claim Boundary

Accepted wording:

> EXP4 evaluates LLM-based semantic scoring as a reproducible proxy layer for
> explanation assessment.

Rejected wording:

> EXP4 validates human interpretability.

Human-centered validation remains a later, separate evidence layer.
