# ADR 002: Data Integration Strategy for Dashboard Metrics

## Status
Accepted

## Date
2025-12-30

## Context
The project consists of two main components:
1. `xai-eval-framework`: A Python backend and experiment runner.
2. `xai-benchmark`: A Next.js frontend dashboard.

The experiment runner produces results in a format optimized for research (snake_case keys, separate CSV/JSON files, disjoint LLM evaluation logs). However, the Dashboard API expects a strict schema (PascalCase keys for metrics, nested `llmEvaluation` objects) to serve the frontend.

We needed a way to bridge this gap without:
- Tightly coupling the experiment runner to the dashboard schema (which may evolve).
- Writing complex on-the-fly transformation logic in the API that degrades performance.

## Decision
We decided to implement a **Post-Processing Transformation Step** using a dedicated script (`experiments/exp1_adult/scripts/merge_dashboard_data.py`).

This script:
1. Loads the raw LLM evaluation inputs (`results_full.json`).
2. Loads the raw classical experiment results (`results.json`, `metrics.csv`).
3. Computes aggregated statistics (e.g., mean Fidelity) and formatted LLM Likert scores.
4. **Injects** these processed objects (`aggregated_metrics`, `llm_evaluation`) directly back into the `results.json` files.

The API (`data_loader.py` / `transformer.py`) then simply reads these pre-computed fields.

## Consequences

### Positive
- **Performance**: Heavy aggregation happens offline, not during API requests.
- **Decoupling**: The core experiment runner doesn't need to know about "Likert scores" or dashboard display names.
- **Simplicity**: The API transformer logic remains simple mapping code.

### Negative
- **Workflow Friction**: Users must remember to run the merge script after running new experiments, or the dashboard will show stale/incomplete data.
- **Data Duplication**: Some data is duplicated (raw vs aggregated) in the JSON files.

## Alternatives Considered
- **On-the-fly Calculation**: Calculating aggregations in `get_run()` would be too slow for large experiment sets.
- **Database**: Valid for production, but overkill for the current file-based phase.
