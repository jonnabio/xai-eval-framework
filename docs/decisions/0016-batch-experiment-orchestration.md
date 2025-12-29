# 16. Batch Experiment Orchestration

Date: 2025-12-28

## Status

Accepted

## Context

As the project scales to Paper B (Large Sample Comparison), we need to run 100+ experiment configurations (various datasets, models, XAI methods). Manually running `run_experiment.py` for each configuration is inefficient, error-prone, and makes reproducibility difficult. We need a way to orchestrate these experiments in batches.

Key requirements:
1.  **Efficiency**: Utilize multi-core CPUs (experiment execution is CPU-bound).
2.  **Reliability**: Handle failures gracefully (one failed experiment shouldn't stop the batch).
3.  **Reproducibility**: Ensure all experiments in a batch share the same codebase version and environmental context.
4.  **Resumability**: Skip already completed experiments if the batch is interrupted.

## Decision

We implemented a `BatchExperimentRunner` class and a corresponding CLI `run_batch_experiments.py`.

### 1. Parallelism Strategy
We utilize `concurrent.futures.ProcessPoolExecutor` for parallelism.
-   **Why**: XAI computations (SHAP/LIME) are CPU-intensive. Threading is limited by the GIL.
-   **Windows Consideration**: Windows does not support `fork()`. We use the `spawn` start method. This requires that the worker function be picklable (top-level) and guarded by `if __name__ == '__main__':`.
-   **Fallback**: A sequential mode is included for debugging.

### 2. Checkpointing
We use file-based checkpointing.
-   Before running a config, strict check for `results.json` in the target config's `output_dir`.
-   If it exists, the experiment is skipped, but its results are included in the final aggregation report.

### 3. Error Handling
-   **Strategy**: "Continue on Error".
-   Exceptions within experiments are caught and logged; the batch continues.
-   The final exit code is non-zero if *any* experiment failed.

### 4. Metadata & Provenance
A `batch_manifest.json` is generated containing:
-   Timestamp
-   Git Commit Hash
-   List of executed, skipped, and failed config IDs
-   Global execution time

## Consequences

**Positive**:
-   Significant reduction in total wall-clock time for large evaluation suites.
-   Improved reproducibility via batch manifests.
-   Easier management of long-running jobs.

**Negative**:
-   Added complexity in debugging parallel processes.
-   Memory usage spikes if `max_workers` is set too high.

## Compliance

-   Must be updated if we move to a distributed backend (e.g., Celery/Ray).
