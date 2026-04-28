# EXP4 OpenRouter 24-Case Pilot: Complete Three-Condition Results

## Scope

This note summarizes the completed 24-case EXP4 pilot using OpenRouter and
`openai/gpt-4.1-2025-04-14` as the LLM judge.

The pilot covers all three EXP4 prompt conditions:

1. `hidden_label_primary`;
2. `label_visible_bias_probe`;
3. `rubric_alt_sensitivity`.

Each condition was executed with one replicate for the same 24 cases.

## Execution Summary

| Item | Value |
|---|---:|
| Fixed EXP4 inventory size | 192 cases |
| Pilot cases evaluated | 24 cases |
| Conditions completed | 3 / 3 |
| Replicates per condition | 1 |
| Planned pilot judgments | 72 |
| Completed real OpenRouter judgments | 72 |
| Parse failures | 0 |
| Provider | OpenRouter |
| Judge model | `openai/gpt-4.1-2025-04-14` |

The 24-case OpenRouter pilot is complete. Raw responses were persisted, parsed
under `SCHEMA_V1`, and incorporated into the EXP4 analysis outputs.

## Condition-Level Semantic Profile

| Condition | Clarity | Completeness | Concision | Semantic Plausibility | Audit Usefulness | Actionability | Overall Quality |
|---|---:|---:|---:|---:|---:|---:|---:|
| Hidden-label primary | 2.71 | 1.92 | 3.50 | 3.17 | 2.04 | 1.79 | 2.00 |
| Label-visible bias probe | 2.54 | 1.83 | 3.46 | 2.79 | 2.04 | 1.71 | 2.00 |
| Alternate-rubric sensitivity | 1.67 | 1.25 | 2.33 | 1.88 | 1.50 | 1.17 | 1.46 |

The primary and label-visible conditions produced similar overall quality
ratings. The alternate-rubric condition produced substantially lower scores
across all dimensions, indicating prompt/rubric sensitivity in the LLM judge.

## Hidden-Label Versus Label-Visible Bias Probe

The label-visible condition did not materially change overall quality:

| Dimension | Mean Delta: Visible - Hidden | Median Delta |
|---|---:|---:|
| Clarity | -0.17 | 0.00 |
| Completeness | -0.08 | 0.00 |
| Concision | -0.04 | 0.00 |
| Semantic plausibility | -0.38 | 0.00 |
| Audit usefulness | 0.00 | 0.00 |
| Actionability | -0.08 | 0.00 |
| Overall quality | 0.00 | 0.00 |

This suggests that exposing the true label did not inflate explanation-quality
scores in the pilot. The largest mean shift was a decrease in semantic
plausibility, consistent with a slightly stricter judgment when outcome
information is visible.

## Hidden-Label Versus Alternate-Rubric Sensitivity

The alternate rubric shifted scores downward:

| Dimension | Mean Delta: Alternate - Hidden | Median Delta |
|---|---:|---:|
| Clarity | -1.04 | -1.00 |
| Completeness | -0.67 | -1.00 |
| Concision | -1.17 | -1.00 |
| Semantic plausibility | -1.29 | -1.00 |
| Audit usefulness | -0.54 | 0.00 |
| Actionability | -0.63 | -1.00 |
| Overall quality | -0.54 | 0.00 |

This is evidence of rubric sensitivity. The same explanation artifacts were
judged more harshly when the alternate prompt emphasized audit inspection and
review utility. This strengthens the methodological argument that LLM-based
semantic evaluation must report prompt and rubric versions, not only model
scores.

## Dataset Pattern

Mean overall quality by dataset:

| Condition | Adult | Breast Cancer | German Credit |
|---|---:|---:|---:|
| Hidden-label primary | 1.75 | 2.40 | 2.14 |
| Label-visible bias probe | 1.67 | 2.40 | 2.29 |
| Alternate-rubric sensitivity | 1.33 | 1.40 | 1.71 |

Breast Cancer and German Credit generally scored higher than Adult in the
primary conditions, although the sample is too small for confirmatory dataset
claims.

## Explainer Pattern

Mean overall quality by explainer:

| Condition | Anchors | DiCE | LIME | SHAP |
|---|---:|---:|---:|---:|
| Hidden-label primary | 1.60 | 1.50 | 2.50 | 2.36 |
| Label-visible bias probe | 1.60 | 1.33 | 2.00 | 2.55 |
| Alternate-rubric sensitivity | 1.20 | 1.00 | 1.00 | 1.91 |

SHAP remained the strongest explainer family in the pilot under all three
conditions. DiCE and Anchors generally scored lower as semantic artifacts,
especially under the alternate audit-oriented rubric. These are descriptive
pilot results and should not be treated as confirmatory explainer rankings.

## Thesis Interpretation

The completed 24-case pilot supports three thesis-relevant points:

1. EXP4 is operationally feasible through OpenRouter: all three prompt
   conditions completed with zero parse failures.
2. Label visibility did not materially inflate LLM explanation-quality ratings,
   suggesting limited outcome-label bias in this pilot.
3. Rubric wording materially affects scores, so LLM-based semantic evaluation
   must be treated as a controlled measurement protocol with frozen prompts,
   model identifiers, and schema validation.

Substantively, the same core result persists: many XAI outputs are concise and
plausible as attribution lists, but weak in completeness, audit usefulness, and
actionability. This reinforces the thesis claim that technical XAI metrics
should be complemented by semantic evaluation.

## Coverage

Relative to the 24-case, one-replicate OpenRouter pilot:

| Component | Completed | Planned | Coverage |
|---|---:|---:|---:|
| Hidden-label primary | 24 | 24 | 100.0% |
| Label-visible bias probe | 24 | 24 | 100.0% |
| Alternate-rubric sensitivity | 24 | 24 | 100.0% |
| Total pilot judgments | 72 | 72 | 100.0% |

Relative to the full 192-case, one-judge, three-condition, three-replicate EXP4
plan:

| Scope | Completed | Planned | Coverage |
|---|---:|---:|---:|
| Real OpenRouter judgments | 72 | 1,728 | 4.2% |
| Unique cases touched | 24 | 192 | 12.5% |

If using the larger two-judge design described in the implementation plan
(`192 cases x 2 judges x 3 conditions x 3 replicates = 3,456 judgments`), the
current 72 real OpenRouter judgments cover 2.1% of the full planned judgment
volume.
