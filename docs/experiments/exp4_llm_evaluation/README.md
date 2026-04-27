# EXP4: LLM-Based Semantic Evaluation

## Status

Status: planned, not executed.

EXP4 is the next experiment family after the completed EXP3 external-validation
package. It is intentionally defined as an LLM-based semantic proxy evaluation
layer, not as direct human-centered validation.

Detailed protocol:

- [DETAILED_DESIGN.md](./DETAILED_DESIGN.md)
- [RUBRIC_V1.md](./RUBRIC_V1.md)
- [SCHEMA_V1.md](./SCHEMA_V1.md)

## Purpose

EXP1, EXP2, and EXP3 establish the technical evidence stack:

- EXP1: calibration and reproducibility evidence.
- EXP2: primary confirmatory benchmark on UCI Adult Income.
- EXP3: compact external tabular validation on Breast Cancer and German Credit.

EXP4 addresses the remaining semantic-evaluation gap:

> Can LLM evaluators provide stable, rubric-based proxy judgments of explanation
> clarity, completeness, concision, plausibility, and audit usefulness, and how
> do those judgments relate to the technical metrics already measured?

## Thesis Role

EXP4 should support the thesis as a planned semantic-proxy layer that extends
the functionally grounded benchmark. It should not be used to claim validated
human interpretability unless a later human study is added.

Supported thesis language:

- "LLM-based semantic proxy evaluation"
- "rubric-based semantic assessment of explanation artifacts"
- "bridge between technical benchmark metrics and future human-centered
  validation"

Unsupported thesis language:

- "LLMs replace human evaluators"
- "EXP4 validates human interpretability"
- "LLM scores prove user trust or usefulness"

## Research Questions

RQ4.1: Can LLMs consistently score XAI explanations across semantic dimensions
such as clarity, completeness, concision, plausibility, and audit usefulness?

RQ4.2: Do LLM semantic scores align with technical metrics from EXP2/EXP3,
including fidelity, stability, sparsity, faithfulness gap, and runtime?

RQ4.3: Do explanation methods exhibit distinct semantic profiles? For example,
SHAP may be complete but verbose, LIME may be concise but unstable, Anchors may
be clear in rule form, and DiCE may be action-oriented.

RQ4.4: Are LLM judgments stable across repeated evaluations, judge models, and
prompt variants?

## Claim Scope

EXP4 can support:

- reproducible semantic-proxy scoring of selected XAI explanations;
- method-level semantic profile comparisons;
- alignment analysis between LLM rubric scores and technical metrics;
- evaluator-stability analysis across repeated LLM judgments.

EXP4 cannot support by itself:

- direct claims about human comprehension, trust, or decision usefulness;
- clinical, financial, or legal deployment claims;
- universal validity of LLM judges across all explanation formats or domains.

## Candidate Inputs

EXP4 should reuse explanation artifacts sampled from completed evidence layers
rather than launching a new predictive-model benchmark.

Input pools:

- EXP2 Adult explanations for SHAP, LIME, Anchors, and DiCE where available.
- EXP3 Breast Cancer and German Credit explanations for SHAP and Anchors.

Sampling should be stratified by:

- dataset;
- model family;
- explainer;
- prediction class;
- model confidence band;
- technical metric profile, including high/low fidelity and high/low stability.

Recommended initial sample size:

- 120 to 240 explanation cases.

## Candidate Semantic Rubric

Each LLM judge should score every case on a fixed 1-5 ordinal scale:

- clarity;
- completeness;
- concision;
- semantic plausibility;
- audit usefulness;
- actionability or decision support;
- overall explanation quality.

Each score should include a short rationale. Numeric scores and free-text
rationales must be stored separately so quantitative analysis is not dependent
on natural-language parsing after the fact.

The initial rubric is specified in [RUBRIC_V1.md](./RUBRIC_V1.md).

## Design Controls

EXP4 must control known LLM-judge risks:

- blind method labels where possible;
- randomize case order;
- normalize explanation presentation templates across methods;
- store explanation length and include it as a covariate;
- repeat each judgment at least three times;
- use at least two judge models if feasible;
- fix model version, temperature, system prompt, rubric prompt, and date;
- store raw prompts, raw responses, parsed scores, parse failures, and retry
  metadata.

## Analysis Plan

Primary analyses:

- inter-run stability of the same judge on the same case;
- inter-judge agreement across LLM models;
- method-level semantic score comparison;
- Spearman/Kendall alignment between semantic scores and technical metrics;
- bias checks for explanation length, method label visibility, and prompt
  variant.

Recommended reliability statistics:

- intraclass correlation coefficient (ICC) for repeated scores;
- Krippendorff's alpha where ordinal multi-judge agreement is needed;
- bootstrap confidence intervals for method-level semantic means.

## Artifact Contract

Planned raw artifacts should live under:

```text
experiments/exp4_llm_evaluation/
```

Planned derived outputs should live under:

```text
outputs/analysis/exp4_llm_evaluation/
```

The result semantics are documented in:

- [docs/results/exp4_llm_evaluation/README.md](../../results/exp4_llm_evaluation/README.md)

The planned case and judgment schemas are specified in
[SCHEMA_V1.md](./SCHEMA_V1.md).

## Relationship to Later Human Validation

EXP4 should be treated as an intermediate semantic-proxy layer. A later
human-centered experiment can use EXP4 to refine rubrics, prompts, and sampling,
but the human study would remain a separate validation layer.
