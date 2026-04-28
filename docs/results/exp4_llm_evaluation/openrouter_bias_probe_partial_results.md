# EXP4 OpenRouter Label-Visible Bias Probe: Partial Results

## Scope

This note documents the partial label-visible bias-probe run for EXP4 using
OpenRouter and `openai/gpt-4.1-2025-04-14`.

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
| Label-visible judgments completed | 12 |
| Label-visible target for 24-case pilot | 24 |
| Label-visible completion within pilot | 50.0% |
| Provider | OpenRouter |
| Judge model | `openai/gpt-4.1-2025-04-14` |
| Replicates | 1 |
| Parse failures | 0 |

The run stopped because the OpenRouter account reached a credit limit. The
available account credit was insufficient for additional GPT-4.1 requests, even
after reducing the output token cap. A cheaper OpenRouter GPT-4.1 Mini judge was
also attempted, but the account then reported insufficient credits.

## Label-Visible Semantic Profile

For the 12 completed label-visible judgments:

| Dimension | Mean | Median |
|---|---:|---:|
| Clarity | 2.67 | 3.00 |
| Completeness | 1.92 | 2.00 |
| Concision | 3.75 | 4.00 |
| Semantic plausibility | 2.92 | 3.00 |
| Audit usefulness | 2.17 | 2.00 |
| Actionability | 1.75 | 2.00 |
| Overall quality | 2.08 | 2.00 |

The same qualitative pattern observed in the hidden-label pilot remains:
explanations are more highly rated for concision than for completeness, audit
usefulness, or actionability.

## Paired Hidden-Label Versus Label-Visible Comparison

The 12 completed label-visible judgments can be paired with their corresponding
hidden-label judgments for the same case, judge, and replicate.

| Dimension | Mean Delta: Visible - Hidden | Median Delta |
|---|---:|---:|
| Clarity | -0.08 | 0.00 |
| Completeness | -0.08 | 0.00 |
| Concision | 0.17 | 0.00 |
| Semantic plausibility | -0.42 | -0.50 |
| Audit usefulness | 0.00 | 0.00 |
| Actionability | -0.08 | 0.00 |
| Overall quality | -0.08 | 0.00 |

At this partial sample size, seeing the true label did not materially change
overall explanation-quality scores. The largest observed shift was a modest
decrease in semantic plausibility. This may indicate that when the true label is
visible, the judge becomes slightly more sensitive to whether the explanation
appears consistent with the outcome.

## Interpretation

This is partial bias-probe evidence, not a completed condition. It supports two
preliminary conclusions:

1. The EXP4 label-visible prompt works technically: raw responses are persisted
   and parsed with zero schema failures.
2. In the 12 paired cases available so far, label visibility did not cause a
   large overall-score shift.

The condition should be completed after OpenRouter credits are replenished. The
next target is to finish the remaining 12 label-visible judgments for the
24-case pilot, then run the alternate-rubric sensitivity condition.

## Coverage

Relative to the 24-case, one-replicate OpenRouter pilot:

| Component | Completed | Planned | Coverage |
|---|---:|---:|---:|
| Hidden-label primary | 24 | 24 | 100.0% |
| Label-visible bias probe | 12 | 24 | 50.0% |
| Alternate-rubric sensitivity | 0 | 24 | 0.0% |
| Total pilot judgments | 36 | 72 | 50.0% |

Relative to the full 192-case, one-judge, three-condition, three-replicate EXP4
plan:

| Scope | Completed | Planned | Coverage |
|---|---:|---:|---:|
| Real OpenRouter judgments | 36 | 1,728 | 2.1% |
| Unique cases touched | 24 | 192 | 12.5% |

If using the larger two-judge design described in the implementation plan
(`192 cases x 2 judges x 3 conditions x 3 replicates = 3,456 judgments`), the
current 36 real OpenRouter judgments cover 1.0% of the full planned judgment
volume.
