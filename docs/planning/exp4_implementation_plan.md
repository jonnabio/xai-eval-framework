# EXP4 Implementation Plan

## Status

Status: first implementation pass complete; OpenRouter full single-judge
replicated execution complete.

Implemented components:

- manifest at `configs/experiments/exp4_llm_evaluation/manifest.yaml`;
- case extraction and stratified sampling in `src/evaluation/exp4_cases.py`;
- schema validation in `src/evaluation/exp4_schema.py`;
- prompt templates and renderer in `src/evaluation/exp4_prompts.py`;
- dry-run and provider-backed judgment runner in `src/evaluation/exp4_runner.py`;
- strict response parser in `src/evaluation/exp4_parser.py`;
- analysis exports in `src/evaluation/exp4_analysis.py`;
- command-line entry points under `scripts/exp4_*.py`;
- focused tests under `tests/exp4/`.

Verified with Windows `.venv-exp3`:

```bash
./.venv-exp3/Scripts/python.exe -m pytest tests/exp4
```

Result: 10 tests passed.

This document translates the EXP4 scientific protocol into concrete code work.
It should be read with:

- [EXP4 detailed design](../experiments/exp4_llm_evaluation/DETAILED_DESIGN.md)
- [EXP4 rubric v1](../experiments/exp4_llm_evaluation/RUBRIC_V1.md)
- [EXP4 schema v1](../experiments/exp4_llm_evaluation/SCHEMA_V1.md)
- [EXP4 execution plan](./exp4_llm_evaluation_plan.md)
- [ADR 0013](../adr/0013-exp4-llm-semantic-proxy-evaluation.md)

## Implementation Goal

Implement a reproducible EXP4 pipeline that:

1. samples explanation cases from EXP2 and EXP3;
2. renders frozen LLM-evaluation prompts;
3. executes LLM judges with raw-response persistence;
4. parses and validates structured scores;
5. analyzes reliability, agreement, semantic profiles, metric alignment, and
   bias diagnostics;
6. exports thesis-ready evidence without violating the proxy-evaluation claim
   boundary.

## Existing Code to Reuse

The repository already has useful LLM and prompt infrastructure:

- `src/llm/client.py`
  - Reuse `LLMClientFactory`, `OpenAIClient`, `GeminiClient`, `OpenRouterClient`,
    and `DummyClient`.
- `src/prompts/engine.py`
  - Reuse prompt-template loading and rendering.
- `src/prompts/templates/`
  - Add EXP4-specific templates here.
- `scripts/run_llm_eval.py`
  - Treat as legacy EXP1-era implementation. Do not extend it directly for
    EXP4 because it lacks EXP4 schemas, raw-response layout, reliability
    replicates, prompt conditions, and bias controls.
- `scripts/analyze_human_llm_agreement.py`
  - Reuse statistical ideas only. EXP4 needs a separate LLM-only reliability
    and semantic-profile analysis script.

## New Code Modules

### 1. EXP4 case models and schema validation

New file:

```text
src/evaluation/exp4_schema.py
```

Responsibilities:

- define `Exp4Case`;
- define `Exp4Scores`;
- define `Exp4Rationales`;
- define `Exp4Flags`;
- define `Exp4Judgment`;
- validate score range `1..5`;
- validate required rationales;
- provide JSON/CSV serialization helpers.

Implementation notes:

- Prefer Pydantic if already available in the environment.
- If avoiding a dependency edge, use dataclasses plus explicit validators.
- Keep schema names aligned with
  `docs/experiments/exp4_llm_evaluation/SCHEMA_V1.md`.

Tests:

```text
tests/exp4/test_exp4_schema.py
```

### 2. Case extraction and normalization

New file:

```text
src/evaluation/exp4_cases.py
```

Responsibilities:

- scan EXP2 and EXP3 result roots;
- load `results.json` and `metrics.csv` where available;
- qualify candidate cases;
- normalize explanation text across SHAP, LIME, Anchors, and DiCE;
- compute `explanation_length_tokens`;
- attach technical metrics;
- generate stable `case_id` values;
- implement stratified sampling.

Key design point:

EXP4 should not ask the LLM to parse raw explainer internals. It should receive
a normalized explanation string plus minimal context.

Expected source roots:

```text
experiments/exp2_scaled/results/
experiments/exp3_cross_dataset/results/
outputs/batch_results.csv
```

New script:

```text
scripts/exp4_build_cases.py
```

Outputs:

```text
experiments/exp4_llm_evaluation/cases/exp4_cases.csv
experiments/exp4_llm_evaluation/cases/exp4_cases.jsonl
experiments/exp4_llm_evaluation/cases/exp4_sampling_report.json
```

Tests:

```text
tests/exp4/test_exp4_cases.py
```

### 3. Prompt templates and prompt renderer

New templates:

```text
src/prompts/templates/exp4_semantic_eval_v1.j2
src/prompts/templates/exp4_semantic_eval_v1_label_visible.j2
src/prompts/templates/exp4_semantic_eval_v1_alt.j2
```

New file:

```text
src/evaluation/exp4_prompts.py
```

Responsibilities:

- build prompt contexts from `Exp4Case`;
- enforce hidden-label vs label-visible conditions;
- embed rubric definitions;
- embed required JSON schema;
- hash prompt versions for audit metadata;
- optionally write rendered prompts for dry-run review.

Prompt conditions:

- `hidden_label_primary`;
- `label_visible_bias_probe`;
- `rubric_alt_sensitivity`.

Tests:

```text
tests/exp4/test_exp4_prompts.py
```

### 4. LLM judgment runner

New file:

```text
src/evaluation/exp4_runner.py
```

Responsibilities:

- load case inventory;
- create judge clients through `LLMClientFactory`;
- execute `case x judge x condition x replicate`;
- persist every raw response before parsing;
- record provider/model metadata;
- support resume behavior by skipping existing raw response files unless
  `--force` is passed;
- support `--dry-run` through `DummyClient`;
- write run manifest and progress logs.

New script:

```text
scripts/exp4_run_llm_judges.py
```

Outputs:

```text
experiments/exp4_llm_evaluation/raw_responses/
experiments/exp4_llm_evaluation/run_manifests/
logs/exp4_llm_evaluation.log
```

Tests:

```text
tests/exp4/test_exp4_runner.py
```

### 5. Parser and validation export

New file:

```text
src/evaluation/exp4_parser.py
```

Responsibilities:

- parse raw LLM JSON;
- strip Markdown code fences if present;
- validate `SCHEMA_V1`;
- write parsed score rows;
- write parse failures;
- preserve raw-response paths in all rows;
- never silently coerce invalid scores.

New script:

```text
scripts/exp4_parse_llm_responses.py
```

Outputs:

```text
experiments/exp4_llm_evaluation/parsed_scores/exp4_llm_scores.csv
experiments/exp4_llm_evaluation/parsed_scores/exp4_parse_failures.csv
experiments/exp4_llm_evaluation/parsed_scores/exp4_parse_summary.json
```

Tests:

```text
tests/exp4/test_exp4_parser.py
```

### 6. EXP4 analysis pipeline

New file:

```text
src/evaluation/exp4_analysis.py
```

Responsibilities:

- compute score summaries by method, dataset, model, judge, and condition;
- compute repeated-judgment reliability;
- compute inter-judge agreement;
- correlate semantic scores with technical metrics;
- run hidden-label vs label-visible bias diagnostics;
- test explanation-length sensitivity;
- export thesis-ready tables and narrative fragments.

New script:

```text
scripts/exp4_analyze_llm_scores.py
```

Outputs:

```text
outputs/analysis/exp4_llm_evaluation/score_summary.csv
outputs/analysis/exp4_llm_evaluation/reliability.csv
outputs/analysis/exp4_llm_evaluation/interjudge_agreement.csv
outputs/analysis/exp4_llm_evaluation/metric_alignment.csv
outputs/analysis/exp4_llm_evaluation/bias_diagnostics.csv
outputs/analysis/exp4_llm_evaluation/exp4_analysis_summary.md
outputs/analysis/exp4_llm_evaluation/thesis_fragment_es.qmd
```

Tests:

```text
tests/exp4/test_exp4_analysis.py
```

## Configuration

New directory:

```text
configs/experiments/exp4_llm_evaluation/
```

New manifest:

```text
configs/experiments/exp4_llm_evaluation/manifest.yaml
```

Manifest fields:

```yaml
experiment_family: exp4_llm_evaluation
status: planned
case_inventory:
  target_cases: 192
  random_seed: 42
  sources:
    - exp2_scaled
    - exp3_cross_dataset
judges:
  - provider: openai
    model_name: TBD
    temperature: 0
    max_tokens: 1200
  - provider: openrouter
    model_name: TBD
    temperature: 0
    max_tokens: 1200
prompt_conditions:
  - hidden_label_primary
  - label_visible_bias_probe
  - rubric_alt_sensitivity
replicates: 3
paths:
  cases_dir: experiments/exp4_llm_evaluation/cases
  raw_responses_dir: experiments/exp4_llm_evaluation/raw_responses
  parsed_scores_dir: experiments/exp4_llm_evaluation/parsed_scores
  analysis_dir: outputs/analysis/exp4_llm_evaluation
```

Keep model names as `TBD` until the execution environment and budget are fixed.

## Directory Contract

Create these directories during implementation:

```text
experiments/exp4_llm_evaluation/
  cases/
  prompts/
  raw_responses/
  parsed_scores/
  run_manifests/

outputs/analysis/exp4_llm_evaluation/
logs/
```

Do not commit large raw-response batches until the execution branch and storage
policy are explicitly confirmed.

## Execution Flow

### Step 0. Preflight

Commands:

```bash
python -m pytest tests/unit/llm/test_client.py tests/unit/prompts/test_engine.py
```

Check:

- Python environment can import project modules.
- LLM provider keys are available only for real execution.
- Dry-run mode works without external API keys.

### Step 1. Build case inventory

Command:

```bash
python scripts/exp4_build_cases.py \
  --manifest configs/experiments/exp4_llm_evaluation/manifest.yaml \
  --target-cases 192 \
  --seed 42
```

Expected outputs:

- `exp4_cases.csv`;
- `exp4_cases.jsonl`;
- `exp4_sampling_report.json`.

Gate:

- case count equals target or documented shortfall;
- no empty normalized explanations;
- stable `case_id` values.

### Step 2. Render prompt dry run

Command:

```bash
python scripts/exp4_run_llm_judges.py \
  --manifest configs/experiments/exp4_llm_evaluation/manifest.yaml \
  --dry-run \
  --limit 5 \
  --replicates 1
```

Expected outputs:

- raw dummy responses for 5 cases;
- run manifest;
- no parser failures after Step 3.

### Step 3. Parse dry-run responses

Command:

```bash
python scripts/exp4_parse_llm_responses.py \
  --manifest configs/experiments/exp4_llm_evaluation/manifest.yaml
```

Gate:

- `exp4_parse_failures.csv` exists and is empty or contains only documented
  intentional malformed fixtures.

### Step 4. Pilot real execution

Command:

```bash
python scripts/exp4_run_llm_judges.py \
  --manifest configs/experiments/exp4_llm_evaluation/manifest.yaml \
  --limit 24 \
  --replicates 1 \
  --condition hidden_label_primary
```

Gate:

- all raw responses are persisted;
- parse success rate is at least 95%;
- cost and latency are acceptable;
- prompt output quality is inspected manually for 5-10 cases.

### Step 5. Full execution

Command:

```bash
python scripts/exp4_run_llm_judges.py \
  --manifest configs/experiments/exp4_llm_evaluation/manifest.yaml \
  --replicates 3
```

Recommended execution policy:

- run one prompt condition at a time;
- commit only manifests and parser summaries first;
- decide separately whether raw LLM responses should be committed or archived.

### Step 6. Parse full execution

Command:

```bash
python scripts/exp4_parse_llm_responses.py \
  --manifest configs/experiments/exp4_llm_evaluation/manifest.yaml
```

Gate:

- parsed score count matches expected judgments minus documented failures;
- invalid score values are zero;
- failures are inspected and classified.

### Step 7. Analyze

Command:

```bash
python scripts/exp4_analyze_llm_scores.py \
  --manifest configs/experiments/exp4_llm_evaluation/manifest.yaml
```

Gate:

- reliability tables generated;
- inter-judge agreement tables generated;
- metric-alignment tables generated;
- bias diagnostics generated;
- summary markdown generated.

## Test Plan

Minimum tests before real execution:

```bash
python -m pytest \
  tests/exp4/test_exp4_schema.py \
  tests/exp4/test_exp4_cases.py \
  tests/exp4/test_exp4_prompts.py \
  tests/exp4/test_exp4_parser.py \
  tests/exp4/test_exp4_runner.py
```

Minimum tests before thesis integration:

```bash
python -m pytest tests/exp4
python scripts/exp4_analyze_llm_scores.py --manifest configs/experiments/exp4_llm_evaluation/manifest.yaml
```

## Implementation Order

1. Add manifest and static prompt templates. Completed.
2. Implement schemas and validators. Completed.
3. Implement case extraction for a small EXP2/EXP3 subset. Completed.
4. Implement case sampler and stable IDs. Completed.
5. Implement prompt renderer and dry-run fixture output. Completed.
6. Implement LLM runner with dry-run behavior. Completed.
7. Implement parser. Completed.
8. Implement analysis pipeline. Completed.
9. Run 5-case dry run. Pending execution gate.
10. Run 24-case pilot. Complete.
11. Freeze prompt/rubric/schema versions. Complete for OpenRouter GPT-4.1
    single-judge execution.
12. Run full execution. Complete for 192 cases, three prompt conditions, and
    three replicates.

## Engineering Risks

### Result schema heterogeneity

EXP2 and EXP3 result files may store explanations differently across methods.
Mitigation: centralize normalization in `src/evaluation/exp4_cases.py` and
record `normalization_status` in the case inventory.

### LLM output drift

LLMs may return malformed or schema-adjacent JSON.
Mitigation: structured-output mode where available, strict parser, raw-response
persistence, and parse-failure table.

### Cost overrun

Full EXP4 can multiply quickly:

```text
192 cases x 2 judges x 3 conditions x 3 replicates = 3456 judgments
```

Mitigation: dry run, 24-case pilot, and budget review before full run.

### Claim inflation

Semantic proxy scores may be misread as human validation.
Mitigation: all generated summaries must include the proxy-evaluation boundary.

### Large artifacts

Raw responses may become too large for routine commits.
Mitigation: decide before full execution whether raw responses are committed,
archived externally, or summarized in Git with a manifest.

## Done Definition

Implementation is complete when:

- all EXP4 scripts exist;
- all EXP4 tests pass;
- dry run produces valid parsed rows;
- pilot run succeeds with acceptable parse success;
- analysis script generates all planned outputs;
- docs are updated with actual command outputs and artifact counts;
- thesis handoff fragment is generated but does not claim human validation.
