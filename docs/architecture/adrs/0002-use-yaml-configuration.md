# 0002. Use YAML for Configuration

**Date**: 2025-12-16  
**Status**: Accepted

## Context
We initially used JSON for model configuration (`rf_adult_config.json`).
However, JSON does not support comments. For a research framework, documenting *why* specific hyperparameters were chosen (e.g., "n_estimators=200 for stability") directly next to the value is critical for reproducibility and peer review.

## Decision
We will use **YAML** (`.yaml`) for all configuration files.
We migrated existing JSON configs to YAML and updated the Python loaders (`_load_config`) to use `PyYAML`.

## Consequences
-   **Positive**: Config files are now self-documenting.
-   **Negative**: Introduces a dependency on `PyYAML`.
