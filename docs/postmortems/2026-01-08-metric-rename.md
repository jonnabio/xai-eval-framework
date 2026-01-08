# Postmortem: Metric Rename Outage (2026-01-08)

## Incident Summary
- **Date**: 2026-01-08 / 2026-01-07 (Local)
- **Impact**: Render deployment failed to start (CrashLoopBackOff).
- **Duration**: ~20 minutes.
- **Root Cause**: `ImportError` due to renaming `CounterfactualSensivtyMetric` to `CounterfactualSensitivityMetric` without updating a compiled dependency in `runner.py`.

## Root Cause Analysis
### What Happened?
1.  **Task 3.2**: Refactored `src/metrics` and renamed `CounterfactualSensivtyMetric` (typo fix).
2.  **Verification**: Verified `src/metrics` logic and checked `src/api` for direct imports of `src/metrics` (Found none).
3.  **Deployment**: Committed and pushed.
4.  **Failure**: `src/api/main.py` -> `batch.py` -> `batch_service.py` -> `batch_runner.py` -> `runner.py`.
    - `runner.py` imported the OLD class name from `src.metrics`.
    - Since `runner.py` is transitively imported by the API (even if not used at runtime startup immediately, Python imports top-level modules), the `ImportError` crashed the app on startup.

### Why was it missed?
-   **Dependency Checking Failure**: The check `grep "from src.metrics" src/api` only found *direct* imports. It did not trace the full dependency tree.
-   **Assumption of Isolation**: Assumed `src/experiment` was completely decoupled from `src/api` except for data loading. However, the `BatchJobManager` (for async experiments) links the two.

## Corrective Actions (Taken)
1.  **Fix**: Updated `src/experiment/runner.py` to use `CounterfactualSensitivityMetric`.
2.  **Monitoring**: Added `prometheus-fastapi-instrumentator` (Task 3.3 work) which was bundled with the fix.
3.  **Verification**: Verified `runner.py` import logic via `grep` and verified dependency availability.

## Prevention & Lessons Learned
1.  **Transitive Dependency Scanning**: Future safety checks must trace imports or run `mypy`/`pylint` on the entire codebase, not just specific directories.
2.  **Startup Verification**: We should run a local `python -c "from src.api.main import app"` check before pushing critical refactors, specifically to catch top-level import errors.
3.  **Search Broadly**: When renaming a symbol, use IDE-wide symbol search or `grep -r "OldName" .` across the *entire* src directory, not just the module being refactored.
