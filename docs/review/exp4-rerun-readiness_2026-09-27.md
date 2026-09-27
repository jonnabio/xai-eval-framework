# EXP4 Judge Re-run — Readiness Findings, 2026-09-27

**Decision (author, 2026-09-27):** re-run the three EXP4 LLM judges so that raw
judge data exists. This is a **new cohort**, not a reproduction (RCA-002): the
original raw responses and templates are gone. Its outputs go to their own
directory and never overwrite the committed aggregates in
`outputs/analysis/exp4_llm_evaluation/` (RCA-002 guard).

## 1. The exact 192 original cases are recoverable

`judge_disagreement.csv` (blob `1fc48ed5b`) lists the 192 case IDs of the
original cohort. A case ID is

```
"exp4_" + sha1("|".join([source_experiment, dataset, model_family, explainer,
                         str(random_seed), str(sample_size), instance_id,
                         str(result_path)]))[:16]
```

(`src/evaluation/exp4_cases.py::_stable_case_id`). Recomputing it for every
instance in the tracked `results.json` files under `experiments/exp2_scaled/`
and `experiments/exp3_cross_dataset/` (126,015 candidates) matches **192/192**
when `result_path` is rendered as a **Windows-style path relative to the repo
root** (e.g. `experiments\exp2_scaled\...\results.json`). Posix-relative,
absolute and `./`-prefixed renderings match 0/192. The original run was
therefore executed on Windows from the repository root.

Consequence: the explanation text, technical metrics, prediction, confidence
and true label of every original case can be rebuilt from committed data, so
the re-run can score the identical inputs. Select them **by ID**:
`sample_cases(pool, 192, seed=42)` over today's tracked results reproduces only
121/192, so the candidate pool at the original run differed from today's.

Composition of the 192 recovered cases:

| Field | Counts |
|---|---|
| source | exp2_scaled 96, exp3_cross_dataset 96 |
| dataset | adult 96, german_credit 53, breast_cancer 43 |
| explainer | anchors 76, shap 52, dice 32, lime 32 |
| model family | xgb 56, logreg 52, mlp 44, rf 40 |
| quadrant | TP 52, FN 47, TN 47, FP 46 |

All 192 carry a true label; mean explanation length 81.1 tokens.

## 2. New finding: the manuscripts misdescribe the EXP4 sample (OPEN)

Paper B+C (§EXP4, "three LLM judges independently scored n=147 paired ...")
and Supplementary Table S1 ("n = 147 paired SHAP/LIME explanation outputs";
system instruction naming the UCI Adult Income dataset only) describe the
sample as paired SHAP/LIME explanations on Adult. The recovered cases are half
Adult and half Breast Cancer / German Credit, and span four explainers with
Anchors the largest group. No reported statistic changes, but the description
of what was measured does, as may the S1 system instruction if the judges
were in fact told every case was Adult. Needs an author decision and a sweep of
Paper B+C, the supplementary and thesis Ch.3/Ch.5 before submission. Not fixed
here: the paper is under author revision.

## 3. What the re-run needs

| Item | State |
|---|---|
| Case inputs | Recoverable exactly (section 1). |
| Code | Reconstructed runner, parser, schema, analysis: pinned (`exp4_source_pins.json`). Providers supported: `openai`, `gemini`, `openrouter`, `dummy`. |
| Templates | Lost. Must be rebuilt: wording from Table S1, interface from `render_exp4_prompt` (`case_json`, `output_schema_json`, `rubric_version`, `prompt_condition`; `true_label` blanked for `hidden_label_primary`). S1 is a paraphrase, not a transcription, so the rebuilt templates are a new instrument version and must be committed this time. |
| Conditions | `hidden_label_primary` (primary ICC), `label_visible_bias_probe`, `rubric_alt_sensitivity`; manifest default 3 replicates. |
| Judges | Original: `gpt-4o-mini` (OpenAI), `claude-3-haiku-20240307` (Anthropic; the code has no Anthropic provider, so presumably via OpenRouter), `gemini-1.5-flash` (Google); temperature 0.0, `max_tokens` 512 per S1 (schema default 1200). Availability of each to be checked with a key. |
| API keys | None set on this laptop. |
| Scale | 192 cases x 3 judges x 3 replicates = 1,728 calls for the primary condition; 5,184 with all three conditions. |
| Retention | Raw responses, parsed scores, prompts, rendered-prompt hashes and run manifests all committed, under a new cohort directory. |
