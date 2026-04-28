# EXP4 OpenRouter Label-Visible Bias Probe Results

## Scope

This note documents the completed 24-case label-visible bias-probe pilot for
EXP4 using OpenRouter and `openai/gpt-4.1-2025-04-14`.

The purpose of this condition is to test whether LLM explanation-quality scores
change when the judge sees the true label. The hidden-label condition asks the
judge to evaluate the explanation without knowing the ground truth. The
label-visible condition exposes the true label and checks whether this changes
the semantic evaluation.

## Execution Status

| Item | Value |
|---|---:|
| Fixed EXP4 inventory size | 192 cases |
| Hidden-label pilot judgments | 24 |
| Label-visible judgments completed | 24 |
| Label-visible target for 24-case pilot | 24 |
| Label-visible completion within pilot | 100.0% |
| Provider | OpenRouter |
| Judge model | `openai/gpt-4.1-2025-04-14` |
| Replicates | 1 |
| Parse failures | 0 |

The run initially stopped because an API key associated with a different
OpenRouter account had insufficient credits. After replacing the key with the
credited OpenRouter account key, the condition resumed successfully. The runner
skipped the 12 already-completed responses and wrote the remaining 12 responses.

## Label-Visible Semantic Profile

For the 24 completed label-visible judgments:

| Dimension | Mean | Median |
|---|---:|---:|
| Clarity | 2.54 | 3.00 |
| Completeness | 1.83 | 2.00 |
| Concision | 3.46 | 4.00 |
| Semantic plausibility | 2.79 | 3.00 |
| Audit usefulness | 2.04 | 2.00 |
| Actionability | 1.71 | 2.00 |
| Overall quality | 2.00 | 2.00 |

The same qualitative pattern observed in the hidden-label pilot remains:
explanations are more highly rated for concision than for completeness, audit
usefulness, or actionability.

## Paired Hidden-Label Versus Label-Visible Comparison

The 24 completed label-visible judgments can be paired with their corresponding
hidden-label judgments for the same case, judge, and replicate.

| Dimension | Mean Delta: Visible - Hidden | Median Delta |
|---|---:|---:|
| Clarity | -0.17 | 0.00 |
| Completeness | -0.08 | 0.00 |
| Concision | -0.04 | 0.00 |
| Semantic plausibility | -0.38 | 0.00 |
| Audit usefulness | 0.00 | 0.00 |
| Actionability | -0.08 | 0.00 |
| Overall quality | 0.00 | 0.00 |

At the 24-case pilot size, seeing the true label did not materially change
overall explanation-quality scores. Median deltas were zero across all
dimensions. The largest mean shift was a modest decrease in semantic
plausibility. This may indicate that when the true label is visible, the judge
becomes slightly more sensitive to whether the explanation appears consistent
with the outcome.

## Interpretation

This completed 24-case bias-probe condition supports three pilot conclusions:

1. The EXP4 label-visible prompt works technically: raw responses are persisted
   and parsed with zero schema failures.
2. In the 24 paired cases, label visibility did not cause a large overall-score
   shift.
3. The semantic pattern remains consistent with the hidden-label pilot:
   explanations are relatively concise but weak in completeness, audit
   usefulness, and actionability.

The next target is the alternate-rubric sensitivity condition for the same
24-case pilot.

## Coverage

Relative to the 24-case, one-replicate OpenRouter pilot:

| Component | Completed | Planned | Coverage |
|---|---:|---:|---:|
| Hidden-label primary | 24 | 24 | 100.0% |
| Label-visible bias probe | 24 | 24 | 100.0% |
| Alternate-rubric sensitivity | 0 | 24 | 0.0% |
| Total pilot judgments | 48 | 72 | 66.7% |

Relative to the full 192-case, one-judge, three-condition, three-replicate EXP4
plan:

| Scope | Completed | Planned | Coverage |
|---|---:|---:|---:|
| Real OpenRouter judgments | 48 | 1,728 | 2.8% |
| Unique cases touched | 24 | 192 | 12.5% |

If using the larger two-judge design described in the implementation plan
(`192 cases x 2 judges x 3 conditions x 3 replicates = 3,456 judgments`), the
current 48 real OpenRouter judgments cover 1.4% of the full planned judgment
volume.
