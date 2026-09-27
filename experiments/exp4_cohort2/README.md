# EXP4 cohort 2 (2026-09)

A re-run of the EXP4 three-judge reliability study, decided by the author on
2026-09-27 because the original raw judge responses were lost (RCA-002). It is
a **new cohort, not a reproduction**, and it never writes over the original
cohort's aggregates in `outputs/analysis/exp4_llm_evaluation/`.

| | Original cohort | Cohort 2 |
|---|---|---|
| Cases | 192, sampled | the **same 192**, recovered by ID (`cases/`) |
| Judges | gpt-4o-mini, claude-3-haiku-20240307, gemini-1.5-flash | openai/gpt-5.4-mini, anthropic/claude-haiku-4.5, google/gemini-3.8-flash (via OpenRouter) |
| Prompts | templates lost | rebuilt from Supplementary Table S1 (`src/prompts/templates/exp4_semantic_eval_v1*.j2`); the rubric_alt wording is new |
| Raw data | lost | committed here |

Configuration: `configs/experiments/exp4_cohort2/manifest.yaml`.

## Layout

- `cases/` -- the 192-case inventory, rebuilt by
  `scripts/exp4_recover_case_inventory.py`
- `prompts/` -- every rendered prompt, named `<case_id>_<prompt hash>.txt`
- `raw_responses/<judge>/<condition>/` -- one JSON envelope per call, with the
  response text and `response_meta` (served model, finish reason, token usage)
- `parsed_scores/` -- validated scores
- `run_manifests/` -- one summary per run invocation
- analysis: `outputs/analysis/exp4_cohort2/`

## Run

```
python scripts/exp4_recover_case_inventory.py --output-dir experiments/exp4_cohort2/cases
python scripts/exp4_run_llm_judges.py --manifest configs/experiments/exp4_cohort2/manifest.yaml
python scripts/exp4_parse_llm_responses.py --manifest configs/experiments/exp4_cohort2/manifest.yaml
python scripts/exp4_analyze_llm_scores.py --manifest configs/experiments/exp4_cohort2/manifest.yaml
```

The judge run needs `OPENROUTER_API_KEY`. It skips responses already on disk,
so an interrupted run resumes. The analysis CLI ends with a `KeyError` after
writing all outputs, a known defect preserved in the reconstruction (RCA-002).

## Reading the results

`_icc_per_dimension` and `_krippendorff_per_dimension` average each
case x judge over **every** condition and replicate present, so the pipeline's
ICC pools all three prompt conditions. Report two views: pooled (what the code
computes) and `hidden_label_primary` only (what Supplementary Table S1 says the
primary ICC is). Only `hidden_label_primary` withholds the true label; the
clean rubric-sensitivity contrast is `rubric_alt_sensitivity` against
`label_visible_bias_probe`.
