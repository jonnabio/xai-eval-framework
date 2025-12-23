# XAI Evaluation Framework - Pre-Integration Status

- **Date**: 2025-12-22
- **Version**: v0.1.0 (Pre-Integration)
- **Branch**: feature/api-integration (based on main)

## 1. Current State
### What Currently Works
- **Experiment Execution**: complete pipeline for Adult dataset (loading, training, XAI generation).
- **Models**: Random Forest (`n_estimators=100`) and XGBoost.
- **XAI Methods**: LIME (Tabular) and SHAP (Tree/Kernel).
- **Metrics**: Fidelity (R2), Stability, Sparsity, Cost.
- **Testing**: 
    - Total tests: 64
    - Passed: 64 (100%)
    - Coverage: Key modules (models, explainers, metrics) covered. 
    - See: `tests/`
- **Data Pipeline**:
    - Format: JSON + Parquet/CSV
    - Location: `experiments/exp1_adult/results/`
    - Artifacts: Trained models (`.pkl`, `.json`), Metric logs (`metrics.json`), Dataframes (`parquet`).

### Repository Structure
```text
xai-eval-framework/
├── experiments/
│   └── exp1_adult/
│       ├── configs/     # YAML configurations
│       ├── results/     # JSON/CSV outputs (metrics, feature importance)
│       └── scripts/     # Visualization & fix scripts
├── src/
│   ├── data_loading/    # Adult dataset loader
│   ├── models/          # SKLearn/XGB wrappers
│   ├── explainers/      # LIME/SHAP wrappers
│   └── evaluation/      # Metric implementations
├── tests/               # Pytest suite
└── docs/                # Architecture records
```

### Dependencies
Defined in `environment.yml`:
- Core: python=3.11, numpy, pandas, scikit-learn, xgboost
- XAI: shap, lime
- Dev: pytest, black, ruff
- **New for Integ**: fastapi, uvicorn, pydantic (added in Phase 0)

### Known Issues
- `visualize_rf_results.py` requires `seaborn` (added to env).
- Large result files (SHAP values) are not fully committed to git (intentional).

## 2. What Will Change (Integration)
### Additions
- **API Module**: `src/api/` containing FastAPI routes and services.
- **Endpoints**:
    - `GET /api/health` (Alive check)
    - `GET /api/runs` (List experiments)
    - `GET /api/runs/{id}` (Run details)
- **Tests**: `tests/test_api_*.py` for API validation.

### No Changes To
- Existing experiment logic (`train_rf.py`, `run_train_models.py`).
- Data storage format (API reads *from* existing JSONs).
- Metric calculation logic.

### Compatibility
- The API is an **opt-in layer**. Running experiments via CLI remains unchanged.
- No breaking changes to the core library.

## 3. Rollback Plan
If integration fails or introduces regressions:
1.  **Delete API**: Remove `src/api/` directory.
2.  **Revert Env**: Remove `fastapi`, `uvicorn`, `pydantic` from `environment.yml`.
3.  **Git Revert**: Revert to commit [HEAD_HASH_BEFORE_MERGE].
4.  **Verify**: Run `pytest` to ensure 64/64 tests pass.

## 4. Test Baseline
- **Baseline File**: `docs/integration/pre-integration-tests.txt`
- **Result**: 25 passed, 0 failed.
- **Git Status**: `docs/integration/pre-integration-status.txt`

## 5. Git Snapshot
- **Current Branch**: `feature/api-integration`
- **Clean Directory**: Yes (after this documentation commit).
- **Uncommitted Changes**: None expected.
