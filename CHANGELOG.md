# Changelog

All notable changes to this project will be documented in this file.

## [Experiment 1 - In Progress]

### 2025-12-16 - EXP1-08 Complete
- **Added**: `AdultRandomForestTrainer` class in `src/models/tabular_models.py` for robust model lifecycle management.
- **Added**: Comprehensive documentation suite (`docs/config_schema.md`, `docs/decisions/`, repository READMEs).
- **Implemented**: End-to-end Random Forest training pipeline (`experiments/exp1_adult/train_rf.py`).
- **Implemented**: Integration tests (`experiments/exp1_adult/test_rf_integration.py`) and unit tests (`tests/test_rf_training.py`).
- **Changed**: Migrated model configuration from JSON to YAML (`rf_adult_config.yaml`) to support inline comments.
- **Changed**: Refactored `train_random_forest_adult` to use the new class-based approach while maintaining backward compatibility.

## [Unreleased]

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
