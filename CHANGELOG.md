# Changelog

All notable changes to this project will be documented in this file.

## [Experiment 1 - In Progress]

### 2025-12-26 - EXP1-26 & EXP1-27 (Metrics & Experiments)
- **Implemented**: `FaithfulnessMetric` in `src/metrics/faithfulness.py` using prediction gap and correlation (masking-based).
- **Updated**: `ExperimentRunner` to use `FaithfulnessMetric` instead of R²-based Fidelity.
- **Added**: Unit tests for Faithfulness metric.
- **Executed**: Missing experimental combinations:
    - **RF + LIME**: Success.
    - **XGB + SHAP**: Partially completed (Blocked by `base_score` serialization bug in `xgboost`/`shap`).
- **Refined**: Documentation compliance check.
- **Added**: `docs/decisions/0013-faithfulness-metric.md` (ADR).

### 2025-12-27 - EXP1-28 & EXP1-29 (Advanced Metrics)
- **Implemented**: `DomainAlignmentMetric` for validating explanations against labor economics priors.
    - Added `ADR-0014` documenting the "Ground Truth" feature sets (Tier 1/Tier 2).
- **Implemented**: `CounterfactualSensitivityMetric` using `dice-ml`.
    - Created `DiCETabularWrapper` for counterfactual generation.
    - Added `ADR-0015` documenting the sensitivity logic.
- **Updated**: `ExperimentRunner` to integrate new metrics with configuration toggles.
- **Verified**: Unit tests and integration tests for new metrics.

### 2025-12-27 - EXP1-30 (Batch Experiment Runner)
- **Implemented**: `BatchExperimentRunner` class in `src/experiment/batch_runner.py` with:
    - Parallel execution using `ProcessPoolExecutor` (spawn context).
    - Checkpointing to skip completed experiments.
    - Result aggregation and manifest generation.
- **Added**: CLI script `scripts/run_batch_experiments.py` for orchestration.
- **Added**: `ADR-0016` documenting batch execution architecture.
- **Added**: `tests/experiment/test_batch_runner.py` with full coverage.
- **Dependencies**: Added `gitpython` for provenance tracking.

### 2025-12-27 - Bug Fixes
- **Fixed**: XGBoost + SHAP compatibility issue (`ValueError: [5E-1]`).
    - Updated `SHAPTabularWrapper` to catch `TreeExplainer` parsing errors.
    - Implemented automatic fallback to `KernelExplainer` for newer XGBoost models.

### 2025-12-16 - EXP1-08 Complete
- **Added**: `AdultRandomForestTrainer` class in `src/models/tabular_models.py` for robust model lifecycle management.
- **Added**: Comprehensive documentation suite (`docs/config_schema.md`, `docs/decisions/`, repository READMEs).
- **Implemented**: End-to-end Random Forest training pipeline (`experiments/exp1_adult/train_rf.py`).
- **Implemented**: Integration tests (`experiments/exp1_adult/test_rf_integration.py`) and unit tests (`tests/test_rf_training.py`).
- **Changed**: Migrated model configuration from JSON to YAML (`rf_adult_config.yaml`) to support inline comments.
- **Changed**: Refactored `train_random_forest_adult` to use the new class-based approach while maintaining backward compatibility.

## [Unreleased]
### Added
- REST API with FastAPI (INT-01 to INT-18)
- Experiment execution endpoint
- Results retrieval endpoints
- Comprehensive error handling and logging
- Docker support for deployment
- Production configuration management

See PR #[NUMBER] for complete details.

### Added (EXP1-49 - Render Deployment)
- **Deployment Strategy**: Migrated from Railway to Render.com (Free Tier) (ADR-0020).
- **Configuration**:
    - Infrastructure-as-Code via `render.yaml`.
    - Production readiness in `config.py` (Sentry, Prometheus, Dynamic CORS).
    - Health check endpoint `/health`.
- **Observability**: Integrated `sentry-sdk` and `prometheus-fastapi-instrumentator`.
- **Verification**: Added `tests/integration/test_render_deployment.py`.

### Added (EXP1-47 - Dashboard Frontend)
- **Enhanced Metrics Dashboard**: Visualizing aggregated metrics (Fidelity, Stability) with confidence intervals.
- **Radar Comparison**: Interactive Recharts-based radar chart for multi-model comparison.
- **Instance Viewer**: Paginated table (`LLMInstanceViewer`) with detailed explanations modal.
- **Frontend Architecture**:
    - New API Client (`src/lib/api-client.ts`).
    - React Query Hooks (`useExperimentData.ts`) for caching and pagination.
    - Page Integration at `/experiments/[id]`.

### Added (EXP1-47 - Dashboard Frontend)
- **Enhanced Metrics Dashboard**: Visualizing aggregated metrics (Fidelity, Stability) with confidence intervals.
- **Radar Comparison**: Interactive Recharts-based radar chart for multi-model comparison.
- **Instance Viewer**: Paginated table (`LLMInstanceViewer`) with detailed explanations modal.
- **Frontend Architecture**:
    - New API Client (`src/lib/api-client.ts`).
    - React Query Hooks (`useExperimentData.ts`) for caching and pagination.
    - Page Integration at `/experiments/[id]`.

### Added (EXP1-46 - Dashboard Integration)
- **Detailed Results Endpoint**: `GET /runs/{run_id}/details` for full experiment data.
- **Instance Pagination**: `GET /runs/{run_id}/instances` for granular explanation data.
- **Service Layer**: Updated `data_loader.py` with caching and `transformer.py` with detailed Pydantic models.
- **Testing**: Added `tests/api/test_detailed_routes.py` covering new endpoints.

### Added (EXP1-14)
- **Evaluation Framework**
    - `src/evaluation/sampler.py`: Stratified sampling (TP/TN/FP/FN).
    - `src/metrics/`: Full metrics suite (Fidelity, Stability, Sparsity, Cost).
- **EXP1-20**: Implemented robust experiment orchestration system.
    - Added `ExperimentRunner` with Pydantic configuration.
    - Added CLI script `scripts/run_experiment.py`.
    - Added YAML configs for RF+SHAP and XGB+LIME.
    - Documented architecture in ADR-010.
    - `scripts/generate_eval_instances.py`: Dataset generation.
    - `ADR-009`: Evaluation Strategy.
    - Comprehensive Unit and Integration Tests.
- **EXP1-21**: Implemented Jinja2 prompt template system.
    - Created `src/prompts/` module.
    - Implemented `PromptEngine` for safe template rendering.
    - Added `eval_instruction.j2` base template for LLM evaluation.

### Added (EXP1-13)
- **SHAP Tabular Wrapper** (`src/xai/shap_tabular.py`)
  - `SHAPTabularWrapper` class prioritizing `TreeExplainer`
  - Utility functions: `sample_background_data`, `validate_shap_additivity`
  - Standardized dense output format consistent with LIME
  - Comprehensive unit tests covering initialization, additivity, and consistency
- **Documentation**
  - `docs/decisions/0008-shap-configuration.md`: ADR for SHAP usage
  - `src/xai/README.md`: Updated with SHAP details
  - `experiments/exp1_adult/examples/example_shap_usage.py`: Usage example

### Added (EXP1-12)
- **LIME Tabular Wrapper** (`src/xai/lime_tabular.py`)
  - `LIMETabularWrapper` class with standardized explanation interface
  - `generate_explanations()` method for batch explanation generation
  - `explain_instance()` method for single instance explanations
  - `generate_lime_explanations()` convenience function
  - Comprehensive docstrings following Google style guide
  - Type hints for all public methods
  - Configuration tracking via `get_config()` method
  - Timing metadata for performance analysis

- **Documentation**
  - `docs/decisions/0007-lime-configuration.md`: ADR for LIME configuration.
  - `src/xai/README.md`: Documentation for XAI module.
  - `experiments/exp1_adult/examples/example_lime_usage.py`: Usage example script.

### Added
- **EXP1-11: Model Testing & Sanity Checks**
    - Created `tests/unit/test_model_sanity.py`: Comprehensive test suite for trained models.
    - Implemented `ADR-006` defining the model testing strategy.
    - Added tests for:
        - **Integrity**: Save/load round-trip validation.
        - **Sanity**: Prediction shapes `(N,)` and probability ranges `[0,1]`.
        - **Performance**: Baseline checks (Accuracy > 0.80, ROC-AUC > 0.85).
        - **Reproducibility**: Deterministic behavior with fixed seeds.
    - Introduced `TestBothModels` parametrized tests for interface compliance.

### Added
- **EXP1-10: Master Training Runner**
    - Created `experiments/exp1_adult/run_train_models.py` orchestration script.
    - Implemented `training_config.yaml` for centralized hyperparameter management.
    - Added CLI support for filtering models (`--models rf,xgboost`) and dry-runs.
    - Implemented dual-format metric persistence (CSV + Parquet).
- **ADR-005**: Training Runner Design.
- **Integration Tests**: Added `tests/integration/test_training_runner.py` covering the full pipeline.

### Changed
- `xgboost_trainer.py`: Refined `load` method to better handle path objects.

### Added
- XGBoostTrainer class in src/models/xgboost_trainer.py
- Training script: experiments/exp1_adult/train_xgb.py
- Config: experiments/exp1_adult/configs/xgb_config.yaml
- Tests: tests/test_xgb_training.py, test_xgb_integration.py
- ADR-004: XGBoost hyperparameter decisions
- Updated src/models/README.md

### Notes
- XGBoost configured to match RF (100 trees) for fair comparison
- Early stopping enabled with validation data
