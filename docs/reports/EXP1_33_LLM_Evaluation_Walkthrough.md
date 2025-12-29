# Walkthrough - EXP1-33 Run LLM Evaluation

I have implemented and executed the pipeline for evaluating explanation quality using LLMs (OpenRouter/GPT-4o).

## Changes
1.  **Prompt Engineering**: Created `src/prompts/templates/explanation_eval.j2` for standardized evaluation (Coherence, Faithfulness, Usefulness).
2.  **Infrastructure**:
    -   Integrated `OpenRouterClient` in `src/llm/client.py` for cost-effective execution.
    -   Implemented `LLMEvaluator` in `src/evaluation/evaluator.py`.
3.  **Execution Script**: Created `scripts/run_llm_evaluation.py` to stratify samples (Model x Explainer x Quadrant) and run the batch.

## Execution Results

### Validation Phase
-   **Mode**: Validation (1 sample per stratum, 16 total)
-   **Provider**: Dummy (Dry run)
-   **Status**: ✅ Passed

### Full Evaluation Phase
-   **Mode**: Full (5 samples per stratum, 80 total)
-   **Provider**: OpenRouter (`openai/gpt-4o`)
-   **Status**: ✅ Completed
-   **Output**: `experiments/exp1_adult/llm_eval/results_full.json`
-   **Time**: ~6 minutes

### Output Snippet
```json
{
  "instance_id": 6961,
  "quadrant": "TP",
  "eval_scores": {
    "coherence": 3,
    "faithfulness": 2,
    "usefulness": 2,
    "reasoning": "The explanation highlights 'capital-gain' as a significant positive contributor... however, the inclusion of multiple 'native-country' features... reduces coherence..."
  }
}
```

## Observations
-   The evaluation pipeline successfully generated detailed reasoning and scores for all 80 instances.
-   **Note**: Some explanations seemingly lacked prediction probability metadata (passed as 0.0), which confused the LLM in some cases. This can be refined in future data generation steps (EXP1-27 refinement).
