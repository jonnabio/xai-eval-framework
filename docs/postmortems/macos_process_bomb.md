# Postmortem: MacOS Process Bomb & System Crash
**Date:** 2026-01-25  
**Incident:** System Instability/Crash during Batch Experimentation  
**Severity:** High (System Unresponsive)

## 1. Issue Description
While running a batch of 300 XAI experiments, the user experienced multiple MacOS system crashes. The system became unresponsive due to resource exhaustion (RAM/CPU) shortly after launching the `run_batch_experiments.py` script with defaults (`--workers 4`).

## 2. Root Cause Analysis
The crash was caused by an **uncontrolled nested parallelism explosion** ("Process Bomb"), specifically triggered by the interaction between Python's `multiprocessing` behavior on MacOS and the application's concurrency logic.

### Technical Details
1.  **MacOS Spawn Method:** Python on MacOS uses `spawn` instead of `fork` (default since 3.8). Spawned child processes do not inherit the memory space or attributes (like the `daemon` flag) of the parent in the same way `fork` does.
2.  **Safety Check Failure:** The `ExperimentRunner` class included a safety check to prevent nested parallelism:
    ```python
    # src/experiment/runner.py
    if multiprocessing.current_process().daemon:
        self.max_workers = 1
    ```
    This check relied on the assumption that worker processes created by `ProcessPoolExecutor` are daemonized.
3.  **The Failure Mode:** When `batch_runner.py` launched 4 workers on MacOS using `spawn`, these workers did not consistently report as `daemon` processes during initialization.
4.  **Result:**
    -   Level 1: Hardware -> 4 Batch Workers (OK)
    -   Level 2: Each Batch Worker -> "I am not a daemon, so I'll trust `os.cpu_count()`" (default ~8-10).
    -   Level 3: Each Batch Worker spawns ~8 sub-workers for SHAP/LIME calculations.
    -   **Total Processes:** 4 * 10 = **40+ heavy Python processes** attempting to run simultaneously.
    -   **Impact:** Immediate RAM saturation and CPU thrashing, leading to kernel panic or freeze.

## 3. Resolution
We implemented a **Concurrecy Flattening** strategy to explicitly prohibit nested parallelism when running in batch mode.

### Code Fix
**File:** `src/experiment/batch_runner.py`  
**Change:** Explicitly override the `max_workers` attribute on the `ExperimentRunner` instance *before* execution within the worker process.

```python
def _run_single_experiment(config_path):
    # ...
    runner = ExperimentRunner(config)
    
    # CRITICAL FIX: Force sequential execution within the worker to prevent
    # nested parallelism explosion (Process Bomb) on MacOS/Spawn.
    runner.max_workers = 1
    
    results = runner.run()
    # ...
```

## 4. Verification
-   **Validation:** Restarted the batch process with `--workers 4`.
-   **Observation:** Monitored process count via terminal `ps aux`. Verified that exactly 4 worker processes were active and consuming resources, stable within system limits.
-   **Outcome:** Experimentation resumed successfully without further crashes.

## 5. Lessons Learned
-   **Explicit > Implicit:** Do not rely on implicit environment flags (like `daemon` status) for critical resource safety logic, especially across different OS process models (`spawn` vs `fork`).
-   **OS Differences:** Validating concurrency logic on one OS (Linux/Linux-based Docker) is insufficient for ensuring stability on MacOS due to fundamental `multiprocessing` differences.
-   **Hard Constraints:** When orchestrating nested workloads, the outer orchestrator (`BatchRunner`) must explicitly constrain the inner worker (`ExperimentRunner`).
