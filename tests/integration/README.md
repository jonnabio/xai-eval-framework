# Integration Tests

This directory contains end-to-end integration tests for the XAI Framework. Unlike unit tests, these verify that multiple components (Data Loading -> Training -> Persistence) work correctly together.

## Test Suite: `test_training_runner.py`

Verifies the Master Training Runner (`experiments/exp1_adult/run_train_models.py`).

| Test Function | Components Tested | Purpose |
|---------------|-------------------|---------|
| `test_full_training_pipeline` | Config, Data, RF, XGB, IO | Verifies the happy path of the entire training vertical. |
| `test_dry_run_mode` | Config, Data | Ensures configuration validation without expensive training. |
| `test_single_model_training` | CLI Filtering | Verifies that we can train subsets of models. |
| `test_invalid_config_handling`| Error Handling | Ensures robust failure on bad configs. |

## Running Tests

Run all integration tests:
```bash
pytest tests/integration/ -v
```

Run only the training runner tests:
```bash
pytest tests/integration/test_training_runner.py -v
```

## Caveats
- These tests require the **Adult Dataset** to be present (or downloadable) in the cache directory.
- `test_full_training_pipeline` trains actual models (albeit small ones), so it may take a few seconds.
