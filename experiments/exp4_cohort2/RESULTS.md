# EXP4 Cohort 2: Results (2026-09-27, final)

**Status: complete.** All 5,184 judge calls have been made: 192 cases x 3
judges x 3 conditions x 3 replicates. Cost: US$20.24.

The run stopped once when credit ran out and resumed after a top-up without
repeating any call. Eleven calls that failed on the provider side
(`finish_reason=error`, empty or cut-off output) were retried. The failed
attempts are kept in `failed_attempts/`, and every retry succeeded.

Everything below comes from `outputs/analysis/exp4_cohort2/`, produced by
`scripts/exp4_cohort2_compare.py`. The ICC is ICC(1,1) (see RCA-002),
computed with the same code as the original cohort.

## Coverage

| Judge | hidden_label | label_visible | rubric_alt | Parse failures (judge format) | Parsed after trailing-comma repair |
|---|---|---|---|---|---|
| gpt-5.4-mini | 576/576 | 576/576 | 576/576 | 3 (label_visible; reply omitted `scores`) | 7 |
| claude-haiku-4.5 | 576/576 | 576/576 | 576/576 | 0 | 0 |
| gemini-3.8-flash | 576/576 | 576/576 | 576/576 | 1 (rubric_alt; `scores` mis-structured) | 39 |

5,180 of 5,184 responses parse. The four failures are judge behaviour and are
not retried. In every condition, all 192 cases have scores from all three
judges.

## Reliability against the original cohort

ICC(1,1) and Krippendorff's alpha, n=192 cases for every cohort 2 view.

| Dimension | Original ICC (n=147) | hidden_label (95% CI) | label_visible | rubric_alt (95% CI) | Pooled | Original α | α, hidden_label |
|---|---|---|---|---|---|---|---|
| clarity | 0.321 | -0.019 (-0.16 to 0.12) | 0.026 | -0.249 (-0.38 to -0.11) | -0.090 | 0.278 | -0.019 |
| completeness | 0.585 | 0.731 (0.66 to 0.79) | 0.744 | **0.753** (0.69 to 0.81) | **0.839** | 0.566 | 0.730 |
| concision | 0.453 | 0.373 (0.24 to 0.49) | 0.360 | 0.650 (0.56 to 0.73) | 0.524 | 0.409 | 0.372 |
| semantic_plausibility | 0.601 | 0.604 (0.51 to 0.69) | 0.594 | 0.566 (0.46 to 0.66) | 0.664 | 0.573 | 0.604 |
| audit_usefulness | 0.376 | 0.699 (0.62 to 0.77) | 0.730 | 0.668 (0.58 to 0.74) | **0.820** | 0.340 | 0.699 |
| actionability | 0.400 | -0.025 (-0.16 to 0.12) | -0.074 | 0.056 (-0.09 to 0.20) | 0.039 | 0.362 | -0.025 |
| overall_quality | 0.431 | 0.660 (0.57 to 0.73) | 0.624 | 0.614 (0.52 to 0.70) | 0.706 | 0.394 | 0.659 |

"Pooled" is what the pipeline computes by default: each case x judge score is
averaged over every condition and replicate before the ICC is taken.

### Findings

1. **Under the definition in Table S1 (hidden_label only), no dimension reaches
   0.75.** The headline survives, but it is weaker than published:
   completeness (upper CI 0.79) and audit usefulness (0.77) have intervals
   that cross 0.75. The published claim that even the upper bound stays below
   0.75 does not hold for this panel.
2. **The threshold is crossed in two other views.** Completeness reaches 0.753
   under the alternative rubric. Under the pipeline's default pooling,
   completeness (0.84) and audit usefulness (0.82) exceed 0.75, because
   averaging nine responses per case and judge suppresses response noise and
   inflates the ICC. So "no dimension reaches 0.75" depends on the condition
   and on a pooling choice the manuscripts do not state. It matters to know
   which one the original cohort used (OPEN; see
   `docs/review/exp4-rerun-readiness_2026-09-27.md`).
3. **The ranking of dimensions is not stable across judge panels.** Clarity
   and actionability fall to about 0. Actionability is a floor effect (86% of
   primary scores are 1). On clarity, Gemini barely varies (SD 0.38) and
   scores about 0.6 below the other judges, and ICC(1,1) counts that offset
   as error. Completeness, audit usefulness and overall quality rise
   substantially. Semantic plausibility is the most stable (0.601 original,
   0.604 cohort 2).
4. **Showing the true label barely moves the scores.** The mean shift for
   label_visible minus hidden_label is at most 0.14 points (Claude, audit
   usefulness) and mostly under 0.05, and reliability is almost unchanged.
5. **Rubric wording matters more than the label.** Against label_visible, the
   alternative rubric shifts Claude down by up to 0.50 points (concision) and
   Gemini's actionability up by 0.28. Reliability moves in both directions:
   concision rises (0.36 to 0.65), while clarity (0.03 to -0.25), overall
   quality and semantic plausibility fall. Agreement is a property of judges
   and rubric wording together, not of the construct alone.
6. **Test-retest (overall_quality, same score in all 3 replicates, by
   condition):** Claude 0.96-0.98, Gemini 0.82-0.88, GPT 0.59-0.68. The judges
   differ markedly in how deterministic they are at temperature 0.

## Not changed

The original cohort's aggregates in `outputs/analysis/exp4_llm_evaluation/`
are untouched, and every published EXP4 number still traces to them. What
cohort 2 changes in the manuscripts is an author decision; nothing has been
edited.
