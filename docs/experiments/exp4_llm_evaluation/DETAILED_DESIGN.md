# EXP4 Detailed Design: LLM-Based Semantic Evaluation of XAI Explanations

## 1. Scientific Positioning

EXP4 is the semantic-evaluation extension of the thesis framework. EXP1-EXP3
establish technical evidence: reproducibility, multi-metric performance,
quality-cost trade-offs, and compact external tabular validation. EXP4 tests
whether LLMs can provide a reproducible, rubric-based semantic proxy for
explanation assessment.

The experiment is not a human-subject validation study. It is a measurement
instrument study: the LLM judge is treated as a proxy evaluator whose stability,
biases, and relationship to technical metrics must be quantified.

## 2. Primary Aim

Estimate the reliability and scientific usefulness of LLM-based semantic scores
for model-agnostic XAI explanations generated in EXP2 and EXP3.

## 3. Research Questions

RQ4.1: Reliability. Are LLM rubric scores stable across repeated judgments of
the same explanation?

RQ4.2: Cross-judge agreement. Do different LLM judges assign similar semantic
profiles to the same explanations?

RQ4.3: Technical-semantic alignment. How do semantic scores relate to technical
metrics such as fidelity, stability, sparsity, faithfulness gap, and runtime?

RQ4.4: Method profiles. Do SHAP, LIME, Anchors, and DiCE exhibit distinct
semantic profiles after controlling for dataset, model, prediction confidence,
and explanation length?

RQ4.5: Bias sensitivity. Are LLM judgments affected by method-label visibility,
explanation length, prompt wording, or judge identity?

## 4. Hypotheses and Propositions

H4.1: Repeated LLM judgments show non-trivial reliability for dimension-level
semantic scoring. Operational criterion: ICC or Krippendorff's alpha is
interpreted using conventional reliability bands and reported with bootstrap
confidence intervals.

H4.2: Semantic scores are positively associated with fidelity and stability, but
not reducible to them. Operational criterion: Spearman/Kendall correlations are
reported per dimension, with multiplicity correction across dimensions.

H4.3: Explanation families have distinct semantic profiles. Expected pattern:
SHAP is advantaged on completeness and audit usefulness, Anchors is advantaged
on clarity and concision, LIME is advantaged on concision but penalized when
instability is visible in the case context, and DiCE is advantaged on
actionability when counterfactual content is present.

H4.4: Method-label visibility changes scores for at least one semantic
dimension. This is a bias-detection hypothesis, not a desired effect.

P4.1: EXP4 can operationalize a reproducible semantic-proxy layer without
collapsing it into a claim about human interpretability.

## 5. Study Design

EXP4 uses a crossed, repeated-measures evaluation design.

Evaluation unit:

```text
case_id x judge_model x prompt_condition x replicate
```

Primary condition:

- method labels hidden;
- technical metric values hidden;
- normalized explanation template;
- fixed rubric;
- structured JSON output.

Robustness conditions:

- method labels visible;
- alternative rubric wording;
- optional pairwise preference task on a subset of matched cases.

## 6. Case Sampling

### 6.1 Source Pools

EXP2 source pool:

- dataset: Adult;
- explainers: SHAP, LIME, Anchors, DiCE where qualified artifacts exist;
- models: all EXP2 model families, with RF/XGB prioritized for comparability
  with EXP3;
- metrics: fidelity, stability, sparsity, faithfulness gap, runtime.

EXP3 source pool:

- datasets: Breast Cancer, German Credit;
- explainers: SHAP, Anchors;
- models: RF, XGB;
- metrics: fidelity, stability, sparsity, faithfulness gap where available,
  runtime.

### 6.2 Stratification Variables

Sampling must preserve variation across:

- source experiment: EXP2 versus EXP3;
- dataset;
- explainer;
- model family;
- prediction class;
- prediction confidence band: low, medium, high where available;
- technical quality profile:
  - high/low fidelity;
  - high/low stability;
  - compact/verbose explanation;
  - low/high runtime where relevant.

### 6.3 Sample Size

Recommended PhD-level initial design:

- 192 cases total.

Suggested allocation:

| Source | Cases | Rationale |
|---|---:|---|
| EXP2 Adult | 144 | Primary source with all four explainer families. |
| EXP3 Breast Cancer | 24 | External tabular validation domain. |
| EXP3 German Credit | 24 | External tabular validation domain. |

EXP2 allocation target:

```text
4 explainers x 3 model groups x 3 technical-profile strata x 4 cases = 144
```

EXP3 allocation target:

```text
2 datasets x 2 explainers x 2 models x 3 seeds x 2 selected cases = 48
```

If 192 cases is operationally too expensive, a defensible pilot design is 96
cases with the same stratification but half the per-cell case count.

## 7. Judge Models

Use at least two judge models. A stronger design uses three:

- one frontier closed model;
- one cost-efficient closed model;
- one open or locally reproducible model if available.

Each judge must be recorded with:

- provider;
- model identifier;
- dated version or API alias;
- temperature;
- maximum output tokens;
- system prompt hash;
- rubric prompt hash.

Recommended default decoding:

- temperature: 0 or nearest deterministic setting;
- top_p: 1 unless provider requires otherwise;
- JSON or structured output mode where available.

## 8. Rubric Dimensions

Use a 1-5 ordinal scale with anchors:

- 1: very poor;
- 2: weak;
- 3: adequate;
- 4: strong;
- 5: excellent.

Required dimensions:

1. clarity;
2. completeness;
3. concision;
4. semantic plausibility;
5. audit usefulness;
6. actionability or decision support;
7. overall explanation quality.

Dimension definitions and score anchors are specified in
[RUBRIC_V1.md](./RUBRIC_V1.md).

## 9. Prompt Conditions

Primary direct-assessment prompt:

- method label hidden;
- one case per prompt;
- fixed output schema;
- rubric dimensions scored independently;
- concise rationale required for each dimension.

Bias probe 1: method-label visibility.

- Same cases as primary condition.
- Explanation method label is shown.
- Compare score shifts against hidden-label condition.

Bias probe 2: prompt wording sensitivity.

- Same rubric constructs, alternative wording.
- Compare rank and score stability.

Optional pairwise condition:

- matched explanations for the same instance/model when available;
- randomized A/B ordering;
- judge selects preferred explanation per rubric dimension;
- used to reduce calibration dependence of numeric scores.

## 10. Data Architecture

Raw case inventory:

```text
experiments/exp4_llm_evaluation/cases/exp4_cases.csv
experiments/exp4_llm_evaluation/cases/exp4_cases.jsonl
```

Prompt and rubric artifacts:

```text
experiments/exp4_llm_evaluation/prompts/system_prompt_v1.md
experiments/exp4_llm_evaluation/prompts/rubric_prompt_v1.md
experiments/exp4_llm_evaluation/prompts/rubric_prompt_v1_alt.md
```

Raw responses:

```text
experiments/exp4_llm_evaluation/raw_responses/
  <judge_model>/<prompt_condition>/<case_id>/replicate_<r>.json
```

Parsed scores:

```text
experiments/exp4_llm_evaluation/parsed_scores/exp4_llm_scores.csv
experiments/exp4_llm_evaluation/parsed_scores/exp4_parse_failures.csv
```

Derived analysis:

```text
outputs/analysis/exp4_llm_evaluation/
```

## 11. Required Schemas

Minimum case fields:

- case_id;
- source_experiment;
- source_artifact_path;
- dataset;
- model_family;
- explainer;
- instance_id;
- prediction;
- prediction_confidence;
- true_label;
- normalized_explanation;
- explanation_length_tokens;
- technical_fidelity;
- technical_stability;
- technical_sparsity;
- technical_faithfulness_gap;
- technical_runtime_ms.

Minimum judgment fields:

- judgment_id;
- case_id;
- judge_model;
- prompt_condition;
- prompt_version;
- rubric_version;
- replicate;
- raw_response_path;
- parse_status;
- clarity_score;
- completeness_score;
- concision_score;
- semantic_plausibility_score;
- audit_usefulness_score;
- actionability_score;
- overall_quality_score;
- dimension_rationales;
- timestamp_utc.

The JSON output contract is specified in [SCHEMA_V1.md](./SCHEMA_V1.md).

## 12. Statistical Analysis

### 12.1 Reliability

- Intraclass correlation coefficient for repeated direct scores.
- Krippendorff's alpha for ordinal multi-judge agreement.
- Bootstrap confidence intervals for reliability estimates.

### 12.2 Method-Level Semantic Profiles

- Dimension-level score summaries by explainer.
- Ordinal mixed-effects models where feasible.
- Nonparametric fallback: Friedman or Kruskal-Wallis-style comparisons with
  stratified bootstrap and Holm correction.

Recommended model structure:

```text
semantic_score ~ explainer + dataset + model_family + confidence_band
               + explanation_length_tokens + (1 | case_id) + (1 | judge_model)
```

### 12.3 Technical-Semantic Alignment

- Spearman and Kendall correlations between semantic dimensions and technical
  metrics.
- Partial correlation or mixed-model adjustment for dataset/model/explainer
  where feasible.
- Explicit analysis of metric disagreement cases, such as high fidelity but low
  clarity.

### 12.4 Bias Diagnostics

- Score shift from hidden-label to label-visible condition.
- Score sensitivity to prompt wording.
- Association between explanation length and semantic scores.
- Judge-model fixed effects.

### 12.5 Multiplicity

Apply Holm-Bonferroni or false-discovery-rate control within predeclared
families:

- reliability tests;
- method comparisons;
- metric-alignment correlations;
- bias probes.

## 13. Quality Gates

Gate 1: Case inventory freeze.

- `exp4_cases.csv` and `exp4_cases.jsonl` are generated.
- Case IDs are stable.
- Sampling report is stored.

Gate 2: Prompt and rubric freeze.

- Rubric and prompt files are versioned.
- JSON schema is versioned.
- Dry-run examples parse successfully.

Gate 3: Execution audit.

- Every planned judgment has one raw response or a logged failure.
- Retry policy is documented.
- Provider/model metadata are complete.

Gate 4: Parse audit.

- Parsed score table reconciles with raw responses.
- Parse failures are counted and inspected.
- No untracked manual score edits.

Gate 5: Reliability export.

- Inter-run and inter-judge reliability tables are generated.
- Low-reliability dimensions are flagged before interpretation.

Gate 6: Bias and alignment export.

- Bias diagnostics and metric-alignment tables are generated.
- Findings are bounded by reliability results.

Gate 7: Thesis handoff.

- Thesis-ready summary uses proxy-evaluation language.
- No human-validation claims are introduced.

## 14. Threats to Validity

Construct validity:

- LLM rubric scores may not measure human understanding.
- Semantic plausibility may reflect the LLM's priors rather than domain truth.

Internal validity:

- Prompt wording, method-label visibility, and explanation length may affect
  scores.
- Provider-side model updates may change judgments.

External validity:

- Results apply to the sampled tabular explanations and selected judge models.
- They do not generalize automatically to image, text, or time-series XAI.

Statistical conclusion validity:

- Ordinal scores should not be overinterpreted as interval measurements.
- Multiple semantic dimensions require multiplicity control.

Reproducibility:

- Raw prompts, raw responses, model identifiers, and parser versions must be
  retained.

## 15. Decision Boundary

EXP4 is successful if it produces:

- a stable case inventory;
- valid raw and parsed LLM judgments;
- reliability estimates;
- semantic profiles by explainer;
- alignment analysis against technical metrics;
- explicit bias diagnostics;
- thesis-ready language that preserves the proxy-evaluation boundary.

EXP4 is not successful if it only produces aggregate LLM scores without raw
responses, rubric traceability, reliability analysis, or bias checks.
