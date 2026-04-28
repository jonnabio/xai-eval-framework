# EXP4 OpenRouter Full Replicated Results

## Purpose

This note documents the completed EXP4 single-judge replicated execution using
OpenRouter as the LLM access layer and `openai/gpt-4.1-2025-04-14` as the
semantic evaluator. EXP4 evaluates whether technical explanation artifacts from
EXP2 and EXP3 function as usable explanations under a structured semantic
rubric.

The evidence is interpreted as LLM-based semantic proxy evaluation. It
complements the technical metrics from EXP1, EXP2, and EXP3; it does not replace
human-subject validation.

## Execution Scope

| Item | Value |
| --- | ---: |
| Fixed EXP4 inventory cases | 192 |
| Source families | EXP2 Adult, EXP3 Breast Cancer, EXP3 German Credit |
| Prompt conditions | 3 |
| Replicates per condition | 3 |
| Real OpenRouter judgments | 1,728 |
| Parsed real OpenRouter judgments | 1,728 |
| Parse failures | 0 |
| Dry-run validation rows excluded from analysis | 15 |
| Real-judgment coverage of single-judge plan | 100.0% |

Condition coverage:

| Prompt condition | Replicate 1 | Replicate 2 | Replicate 3 |
| --- | ---: | ---: | ---: |
| Hidden-label primary | 192 | 192 | 192 |
| Label-visible bias probe | 192 | 192 | 192 |
| Alternate rubric sensitivity | 192 | 192 | 192 |

One response returned an incorrect `case_id` inside the LLM JSON body, while the
raw response envelope, judgment identifier, and prompt path all identified the
correct inventory case. The parser now treats the envelope `case_id` as
authoritative and records the returned response ID separately through
`response_case_id` and `case_id_mismatch`.

## Artifact Locations

Primary raw and derived locations:

- Inventory: `experiments/exp4_llm_evaluation/cases/exp4_cases.csv`
- JSONL inventory: `experiments/exp4_llm_evaluation/cases/exp4_cases.jsonl`
- Prompts: `experiments/exp4_llm_evaluation/prompts/`
- Raw OpenRouter responses: `experiments/exp4_llm_evaluation/raw_responses/openrouter_gpt41/`
- Run manifests: `experiments/exp4_llm_evaluation/run_manifests/`
- Parsed scores: `experiments/exp4_llm_evaluation/parsed_scores/exp4_llm_scores.csv`
- Parse failures: `experiments/exp4_llm_evaluation/parsed_scores/exp4_parse_failures.csv`
- Analysis outputs: `outputs/analysis/exp4_llm_evaluation/`

The replicated run manifests are:

- `experiments/exp4_llm_evaluation/run_manifests/run_2026-04-28T231014.938555Z0000.json`
- `experiments/exp4_llm_evaluation/run_manifests/run_2026-04-28T231053.606362Z0000.json`
- `experiments/exp4_llm_evaluation/run_manifests/run_2026-04-28T231120.258238Z0000.json`

## Primary Findings

Across the hidden-label primary condition, the LLM judge assigned the highest
mean scores to concision and semantic plausibility, with lower scores for
completeness, audit usefulness, actionability, and overall quality. This pattern
supports a central thesis claim: many XAI artifacts are compact attribution
signals, but they often lack enough context, domain interpretation, and decision
support to function as full explanations.

Mean scores by condition:

| Condition | Clarity | Completeness | Concision | Semantic plausibility | Audit usefulness | Actionability | Overall quality |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Hidden-label primary | 2.611 | 1.809 | 3.396 | 2.986 | 1.991 | 1.741 | 1.929 |
| Label-visible bias probe | 2.240 | 1.665 | 3.050 | 2.370 | 1.819 | 1.590 | 1.752 |
| Alternate rubric sensitivity | 1.599 | 1.250 | 2.167 | 1.755 | 1.392 | 1.212 | 1.382 |

SHAP received the strongest semantic scores among the evaluated explainer
families. LIME followed, while Anchors and DiCE were lower on overall quality
and actionability. This does not convert EXP4 into a human-subject study, but it
does show that the semantic proxy layer distinguishes between explanation
styles in a way that is consistent with their expected textual content.

Mean scores by explainer family:

| Explainer | Overall quality | Semantic plausibility | Completeness | Audit usefulness | Actionability |
| --- | ---: | ---: | ---: | ---: | ---: |
| SHAP | 2.374 | 3.485 | 2.111 | 2.432 | 1.934 |
| LIME | 1.778 | 2.549 | 1.684 | 1.792 | 1.691 |
| Anchors | 1.377 | 1.879 | 1.332 | 1.440 | 1.313 |
| DiCE | 1.219 | 1.549 | 1.170 | 1.243 | 1.135 |

By dataset, German Credit received the highest mean semantic scores, followed
by Breast Cancer and Adult. This suggests that EXP4 is sensitive not only to
the explainer method, but also to the explanation surface produced in each
dataset and model context.

| Dataset | Overall quality | Semantic plausibility | Concision |
| --- | ---: | ---: | ---: |
| German Credit | 1.960 | 2.807 | 3.329 |
| Breast Cancer | 1.680 | 2.351 | 2.780 |
| Adult | 1.541 | 2.138 | 2.659 |

## Replicate Stability

The three-replicate design indicates moderate stability. The dimensions closest
to audit decision support were the most stable: actionability, completeness,
audit usefulness, and overall quality had zero replicate range for roughly
70-76% of case-condition groups. Concision and semantic plausibility varied
more, which is expected because they depend more on how the judge interprets
the density and domain meaning of a compact attribution list.

Mean replicate variability:

| Dimension | Mean replicate std. | Mean replicate range | Zero-range groups |
| --- | ---: | ---: | ---: |
| Clarity | 0.280 | 0.608 | 53.5% |
| Completeness | 0.141 | 0.300 | 70.7% |
| Concision | 0.392 | 0.852 | 49.8% |
| Semantic plausibility | 0.288 | 0.625 | 51.9% |
| Audit usefulness | 0.152 | 0.325 | 70.3% |
| Actionability | 0.116 | 0.247 | 75.7% |
| Overall quality | 0.153 | 0.328 | 69.8% |

## Label-Visibility Bias Probe

Revealing the true label did not inflate semantic scores. In fact, the
label-visible condition reduced mean scores across all dimensions, with the
largest decrease in semantic plausibility. This suggests that, for this judge
and prompt version, outcome visibility made the evaluator more critical rather
than more generous.

| Dimension | Mean visible-minus-hidden delta | Median delta | Paired judgments |
| --- | ---: | ---: | ---: |
| Clarity | -0.372 | 0.0 | 576 |
| Completeness | -0.144 | 0.0 | 576 |
| Concision | -0.345 | 0.0 | 576 |
| Semantic plausibility | -0.616 | -1.0 | 576 |
| Audit usefulness | -0.172 | 0.0 | 576 |
| Actionability | -0.151 | 0.0 | 576 |
| Overall quality | -0.177 | 0.0 | 576 |

## Metric Alignment

The semantic scores show positive, moderate association with sparsity and
fidelity, weaker positive association with stability and faithfulness gap, and
weak negative association with runtime and cost. For overall quality, Spearman
correlations were:

| Technical metric | Spearman correlation | N |
| --- | ---: | ---: |
| Sparsity | 0.460 | 1,728 |
| Fidelity | 0.364 | 1,728 |
| Stability | 0.253 | 1,728 |
| Faithfulness gap | 0.135 | 1,728 |
| Runtime | -0.119 | 1,728 |
| Cost | -0.119 | 1,728 |

This supports the framework premise that technical metrics and semantic
evaluation are related but not interchangeable. Compact, faithful explanations
tend to be evaluated more favorably, but technical quality alone does not
guarantee completeness, audit usefulness, or actionability.

## Thesis Interpretation

EXP4 adds a semantic evaluation layer to the thesis. EXP1 establishes
calibration and reproducibility, EXP2 provides the main Adult benchmark,
EXP3 tests external tabular portability, and EXP4 evaluates whether the
resulting explanation artifacts are semantically useful under a structured
LLM-judge rubric.

The full replicated EXP4 result strengthens the thesis argument that
explainability assessment must be multi-level. A technically strong attribution
can still be semantically incomplete. Conversely, a semantically clear
explanation should still be checked against fidelity, stability, sparsity,
runtime, and cost. EXP4 therefore functions as a bridge between technical XAI
metrics and the human-facing interpretation goals of explainable AI.

## Limitations

- The completed run uses one real LLM judge model. Inter-judge agreement with a
  second independent model remains future work.
- EXP4 is a semantic proxy evaluation, not a direct user study.
- The findings are conditioned on OpenRouter delivery of
  `openai/gpt-4.1-2025-04-14`, the EXP4 prompt templates, and rubric version 1.
- Raw LLM rationales should be treated as audit evidence for the scoring
  process, not as authoritative clinical, financial, or human-subject judgment.
