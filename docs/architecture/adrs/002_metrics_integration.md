# ADR-002: Service-Layer Integration for Advanced Metrics

## Status
Accepted

## Context
Experiment 1 (EXP1) produces rich, hierarchical data including:
- Classical metrics (Fidelity, Stability, Sparsity)
- Advanced metrics (Faithfulness, Counterfactual Sensitivity)
- LLM Evaluations (Likert scores, justifications)
- Instance-level evaluations (metrics + explanation details)

The current dashboard backend serves `Run` objects (aggregated summaries). The frontend requires detailed instance-level data for visualization. We need a robust, scalable pattern to serve this data from the Railway environment (filesystem storage) while maintaining performance.

## Decisions

### 1. Storage & Mapping Strategy
**Decision**: **Filesystem with Runtime Scanning and Caching**.
**Rationale**:
- **Source of Truth**: The `experiments/exp1_adult/results/*.json` files are the authoritative record.
- **Mapping**: `run_id` is a hash of metadata (dataset, model, timestamp). Since we cannot decode path from hash, we must scan available results to find the matching ID.
- **Performance**: N < 100 experiments makes scanning trivial (< 50ms). We will add `functools.lru_cache` to the lookup function to optimize repeated access.

### 2. Schema Architecture
**Decision**: **Extend `src/api/models/schemas.py`**.
- We will NOT create a parallel `metrics.py`.
- **New Models**:
    - `aggregations.MetricStatistics`: {mean, std, min, max, median}
    - `instances.InstanceEvaluation`: {instance_id, metrics, explanation, quadrant}
    - `results.ExperimentResult`: Superset containing metadata, model info, aggregated metrics array, and instance list.
- **Backward Compatibility**: `ExperimentResult` will include a `to_legacy_run()` helper (or similar) if needed, but primarily it serves new endpoints.

### 3. API Endpoint Design
**Decision**: **Segmented Endpoints on `/runs` Resource**.
- `GET /runs/{run_id}`: Keeps returning the legacy `Run` summary (fast, lightweight).
- `GET /runs/{run_id}/details`: Returns `ExperimentResultResponse` (full detailed object, excluding instances list to save bandwidth).
- `GET /runs/{run_id}/instances`: Returns `InstancesResponse` (paginated list of `InstanceEvaluation`).

### 4. Configuration & Caching
**Decision**: **Config-Driven Limits**.
- `RESULTS_CACHE_TTL_SECONDS`: 300 (5 mins).
- `RESULTS_DEFAULT_PAGE_SIZE`: 50.
- `RESULTS_MAX_INSTANCES_PER_REQUEST`: 100.

## Consequences
- **Positive**:
    - Clean separation of summary vs. detail views.
    - Type-safe contract for frontend via Pydantic.
    - Performance protected via paging and caching.
- **Negative**:
    - Scanning introduces O(N) lookup, but cached.
    - Duplication of data structures between `ExperimentRunner` output schema and API schema (maintenance overhead).
