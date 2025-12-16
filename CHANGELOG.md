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
