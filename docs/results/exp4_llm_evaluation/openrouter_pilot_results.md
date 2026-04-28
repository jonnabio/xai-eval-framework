# EXP4 OpenRouter Pilot Results

## Scope

This pilot evaluates the EXP4 LLM-as-evaluator pipeline using OpenRouter as the
provider and `openai/gpt-4.1-2025-04-14` as the judge model.

The pilot used the hidden-label primary prompt condition only. Ground-truth
labels were masked from the judge so the scores assess the explanation as a
semantic account of the model decision rather than as a judgment of prediction
correctness.

## Execution Summary

| Item | Value |
|---|---:|
| Fixed EXP4 inventory size | 192 cases |
| Pilot cases evaluated | 24 cases |
| Provider | OpenRouter |
| Judge model | `openai/gpt-4.1-2025-04-14` |
| Prompt condition | `hidden_label_primary` |
| Replicates | 1 |
| Raw OpenRouter responses | 24 |
| Parsed OpenRouter judgments | 24 |
| Parse failures | 0 |

The pilot confirms that OpenRouter can be used as the execution layer for EXP4:
responses were persisted, parsed under `SCHEMA_V1`, and incorporated into the
analysis pipeline without parser failures.

## Sample Composition

| Group | n | Mean Overall Quality | SD | Median |
|---|---:|---:|---:|---:|
| EXP2 scaled | 12 | 1.75 | 0.87 | 1.50 |
| EXP3 cross-dataset | 12 | 2.25 | 0.87 | 2.50 |

| Dataset | n | Mean Overall Quality | SD | Median |
|---|---:|---:|---:|---:|
| Adult | 12 | 1.75 | 0.87 | 1.50 |
| Breast Cancer | 5 | 2.40 | 0.89 | 3.00 |
| German Credit | 7 | 2.14 | 0.90 | 2.00 |

## Semantic Score Profile

| Dimension | Mean | SD | Median | Min | Max |
|---|---:|---:|---:|---:|---:|
| Clarity | 2.71 | 1.27 | 3.00 | 1 | 4 |
| Completeness | 1.92 | 0.83 | 2.00 | 1 | 3 |
| Concision | 3.50 | 1.62 | 4.00 | 1 | 5 |
| Semantic plausibility | 3.17 | 1.55 | 4.00 | 1 | 5 |
| Audit usefulness | 2.04 | 0.91 | 2.00 | 1 | 3 |
| Actionability | 1.79 | 0.72 | 2.00 | 1 | 3 |
| Overall quality | 2.00 | 0.88 | 2.00 | 1 | 3 |

The strongest dimensions were concision and semantic plausibility. This suggests
that many explanations were short and broadly coherent, but did not provide
enough context to support deeper review. Completeness, audit usefulness, and
actionability were substantially lower, indicating that explanations often
identified influential factors without supplying sufficient interpretive detail,
directionality, or recourse-oriented information.

This pattern is consistent with the distinction documented in
[Attribution Is Not Yet Explanation](./attribution_vs_explanation_note.md): many
model explanations in the pilot are technically useful attribution lists, but
they do not yet provide the contextual information a human reviewer would need
for audit or decision support.

## Explainer-Level Pilot Pattern

| Explainer | n | Mean Overall Quality | SD | Median |
|---|---:|---:|---:|---:|
| Anchors | 5 | 1.60 | 0.89 | 1.00 |
| DiCE | 6 | 1.50 | 0.84 | 1.00 |
| LIME | 2 | 2.50 | 0.71 | 2.50 |
| SHAP | 11 | 2.36 | 0.81 | 3.00 |

Within this small pilot, SHAP and LIME received higher overall semantic quality
scores than Anchors and DiCE. This should be interpreted cautiously because the
pilot is not balanced enough for confirmatory explainer comparisons. Its main
purpose is to verify real-provider execution and identify whether the scoring
profile is plausible enough to justify a larger EXP4 run.

## Model-Level Pilot Pattern

| Model Family | n | Mean Overall Quality | SD | Median |
|---|---:|---:|---:|---:|
| Logistic regression | 8 | 1.75 | 0.89 | 1.50 |
| MLP | 4 | 1.75 | 0.96 | 1.50 |
| Random forest | 3 | 1.67 | 1.15 | 1.00 |
| XGBoost | 9 | 2.44 | 0.73 | 3.00 |

The XGBoost subset received the highest average overall quality in the pilot.
This result is descriptive only and may reflect the sampled cases and explainer
mix rather than a stable model-family effect.

## Preliminary Metric Alignment

For the 24 OpenRouter pilot judgments, Spearman alignment between overall
quality and selected technical metrics was:

| Technical Metric | Spearman rho |
|---|---:|
| Fidelity | 0.60 |
| Stability | 0.28 |
| Sparsity | 0.25 |
| Faithfulness gap | 0.21 |
| Runtime proxy | -0.06 |

The strongest preliminary association was between technical fidelity and
LLM-assessed overall quality. This is consistent with the hypothesis that
technically faithful explanations tend to be judged as more semantically useful,
but the pilot size is too small for confirmatory inference.

## Interpretation for the Thesis

The OpenRouter pilot supports the feasibility of EXP4 as a semantic proxy
evaluation layer. The execution path is now validated with real provider calls:
case sampling, prompt rendering, raw response retention, schema validation, and
analysis all completed without parse failures.

Substantively, the pilot indicates that existing explanations may be concise and
locally plausible while still weak as audit artifacts. The low scores for
completeness, audit usefulness, and actionability suggest a semantic gap between
technical explanation generation and explanation usefulness for review-oriented
tasks. This strengthens the thesis argument that computational XAI metrics
should be complemented by semantic evaluation rather than interpreted as
sufficient evidence of practical explanatory quality.

These findings remain pilot evidence. They should be reported as execution and
feasibility results until the full EXP4 design is completed with the planned
case count, judge configuration, and reliability checks.
