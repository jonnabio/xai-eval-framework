# 16. Batch Experiment Orchestration

Date: 2025-12-27

## Status

Proposed

## Context

As the project scales to Paper B (Large Sample Comparison), we need to run 100+ experiment configurations (various datasets, models, XAI methods). Manually running `run_experiment.py` for each configuration is inefficient, error-prone, and makes reproducibility difficult. We need a way to orchestrate these experiments in batches.

Key requirements:
1.  **Efficiency**: Utilize multi-core CPUs (experiment execution is CPU-bound).
2.  **Reliability**: Handle failures gracefully (one failed experiment shouldn't stop the batch).
3.  **Reproducibility**: Ensure all experiments in a batch share the same codebase version and environmental context.
4.  **Resumability**: Skip already completed experiments if the batch is interrupted.

## Decision

We will implement a `BatchExperimentRunner` class and a corresponding CLI `run_batch_experiments.py`.

### 1. Parallelism Strategy
We will use `concurrent.futures.ProcessPoolExecutor` for parallelism.
-   **Why**: XAI computations (SHAP/LIME) are CPU-intensive. Threading is limited by the GIL.
-   **Windows Consideration**: Windows does not support `fork()`. We must use the `spawn` start method. This requires that the worker function be picklable (top-level function) and that we guard the entry point with `if __name__ == '__main__':`.
-   **Fallback**: We will include a sequential mode for debugging and environments where multiprocessing fails.

### 2. Checkpointing
We will use file-based checkpointing.
-   Before running a config, strict check for `results.json` in the target config's `output_dir`.
-   If it exists, the experiment is skipped, but its results are loaded and included in the final aggregation report.

### 3. Error Handling
-   **Strategy**: "Continue on Error".
-   Exceptions within an individual experiment will be caught, logged to a separate `batch_failures.log`, and the batch will continue.
-   The final exit code of the CLI will be non-zero if *any* experiment failed, alerting the user to inspect the logs.

### 4. Metadata & Provenance
A `batch_manifest.json` will be generated at the end of the run containing:
-   Timestamp
-   Git Commit Hash
-   List of executed config IDs
-   List of skipped config IDs
-   List of failed config IDs
-   Global execution time

## Consequences

**Positive**:
-   Significant reduction in total wall-clock time for large evaluation suites.
-   Improved reproducibility via batch manifests.
-   Easier management of long-running jobs (set and forget).

**Negative**:
-   Added complexity in debugging parallel processes (logs can be interleaved, though we will configure logging to mitigate this).
-   Memory usage spikes if `max_workers` is set too high for memory-intensive datasets. User must tune `--workers`.

## Compliance

-   Must be updated if we move to a distributed backend (e.g., Celery/Ray) in the future, though `ProcessPoolExecutor` abstraction makes this transition easier.
