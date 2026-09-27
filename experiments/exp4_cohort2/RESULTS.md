# EXP4 Cohort 2: Results (2026-09-27)

**Status:** 5,021 of 5,184 calls complete. The primary and `label_visible`
conditions are complete for all three judges, and `rubric_alt` is complete
for GPT-5.4 mini and Claude Haiku 4.5. Gemini 3.8 Flash `rubric_alt` stopped
at 413 of 576 when credit ran out; the remaining 163 calls (about US$0.90)
resume without re-running anything. Spent: US$19.39.

Everything below comes from `outputs/analysis/exp4_cohort2/`, produced by
`scripts/exp4_cohort2_compare.py`. The ICC is ICC(1,1) (see RCA-002),
computed with the same code as the original cohort.

## Coverage

| Judge | hidden_label | label_visible | rubric_alt | Parse failures |
|---|---|---|---|---|
| gpt-5.4-mini | 576/576 | 576/576 | 576/576 | 3 (the reply omitted `scores`) |
| claude-haiku-4.5 | 576/576 | 576/576 | 576/576 | 0 |
| gemini-3.8-flash | 576/576 | 576/576 | 413/576 | 11 (provider errors with 0 output tokens: 4 / 2 / 5) |

A further 48 responses parsed only after the trailing-comma repair; the
parser records this in `parse_status`. All 192 cases have scores from all
three judges in both complete conditions.

## Reliability against the original cohort

| Dimension | Original ICC (n=147) | Cohort 2 ICC, hidden_label (95% CI) | Cohort 2 ICC, pooled | Original α | Cohort 2 α, hidden_label |
|---|---|---|---|---|---|
| clarity | 0.321 | -0.019 (-0.16 to 0.12) | -0.085 | 0.278 | -0.019 |
| completeness | 0.585 | 0.731 (0.66 to 0.79) | **0.840** | 0.566 | 0.730 |
| concision | 0.453 | 0.373 (0.24 to 0.49) | 0.520 | 0.409 | 0.372 |
| semantic_plausibility | 0.601 | 0.605 (0.51 to 0.69) | 0.657 | 0.573 | 0.604 |
| audit_usefulness | 0.376 | 0.699 (0.62 to 0.77) | **0.821** | 0.340 | 0.699 |
| actionability | 0.400 | -0.023 (-0.16 to 0.12) | 0.045 | 0.362 | -0.023 |
| overall_quality | 0.431 | 0.660 (0.57 to 0.73) | 0.707 | 0.394 | 0.659 |

Cohort 2's hidden_label view has n=192 cases. "Pooled" is what the pipeline
computes by default: each case x judge score is averaged over every
condition and replicate before the ICC is taken.

### Findings

1. **Under the definition in Table S1 (hidden_label only), no dimension reaches
   0.75.** The headline survives, but it is weaker than published:
   completeness (upper CI 0.79) and audit usefulness (0.77) have intervals
   that cross 0.75. The published claim that even the upper bound stays below
   0.75 does not hold for this panel.
2. **Under the pipeline's default pooling, two dimensions exceed 0.75**
   (completeness 0.84, audit usefulness 0.82). Averaging nine responses per
   case and judge suppresses response noise and inflates the ICC. So whether
   "no dimension reaches 0.75" is true depends on a pooling choice the
   manuscripts do not state. It matters to know which one the original
   cohort used (OPEN; see `docs/review/exp4-rerun-readiness_2026-09-27.md`).
3. **The ranking of dimensions is not stable across judge panels.** Clarity
   and actionability fall to about 0. Actionability is a floor effect (86% of
   primary scores are 1). On clarity, Gemini barely varies (SD 0.38) and
   scores about 0.6 below the other judges, and ICC(1,1) counts that offset
   as error. Completeness, audit usefulness and overall quality rise
   substantially. Semantic plausibility is the most stable (0.601 original,
   0.605 cohort 2).
4. **Showing the true label barely moves the scores.** The mean shift for
   label_visible minus hidden_label is at most 0.14 points (Claude, audit
   usefulness) and mostly under 0.05.
5. **Rubric wording matters more than the label.** Against label_visible, the
   alternative rubric shifts Claude down by up to 0.50 points (concision) and
   Gemini's actionability up by 0.36, and its ICCs fall on four dimensions
   (e.g. semantic plausibility 0.59 to 0.41). The rubric_alt view is
   provisional: Gemini covers 138 of 192 cases there so far.
6. **Test-retest (overall_quality, same score in all 3 replicates):**
   Claude 0.98, Gemini 0.83, GPT 0.59. The judges differ markedly in how
   deterministic they are at temperature 0.

## Not changed

The original cohort's aggregates in `outputs/analysis/exp4_llm_evaluation/`
are untouched, and every published EXP4 number still traces to them. What
cohort 2 changes in the manuscripts is an author decision; nothing has been
edited.
