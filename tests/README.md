# Testing Strategy

This document outlines the testing philosophy and standards for the XAI Inspection Framework. As a Ph.D. research project, maintaining reproducibility and correctness is critical.

## 1. Testing Philosophy
We adhere to a "Pyramid of Testing" approach tailored for ML research:
1.  **Unit Tests (Base)**: Strict validation of individual functions (data loading, metric calculations). Fast and frequent.
2.  **Integration Tests (Middle)**: Verifying complete pipelines (e.g., Train -> Save -> Load -> Predict).
3.  **Scientific Validation (Top)**: Asserting that model performance meets baseline expectations (e.g., Accuracy > 80%).

**Why?**
-   **Reproducibility**: Ensures random seeds and configurations usually produce deterministic results.
-   **Refactoring Safety**: Allows us to optimize internal logic without breaking the experimental results.

## 2. Test Organization

### Directory Layout
Tests mirror the source directory structure where possible.

```
xai-eval-framework/
├── tests/                       # Global Unit Tests
│   ├── test_adult_loader.py     # Tests src/data_loading/adult.py
│   └── test_rf_training.py      # Tests src/models/tabular_models.py
├── experiments/
│   └── exp1_adult/
│       └── test_rf_integration.py # Experiment-specific Integration Tests
└── src/                         # Source Code
```

### Mapping
-   `src.data_loading.adult` -> `tests.test_adult_loader`
-   `src.models.tabular_models` -> `tests.test_rf_training`

## 3. Running Tests

We use `pytest` as the test runner.

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test File
```bash
python -m pytest tests/test_rf_training.py
```

### Run Integration Tests
Integration tests often live outside the main test suite to avoid slowing down CI.
```bash
python experiments/exp1_adult/test_rf_integration.py
```

### With Coverage
To check line coverage:
```bash
pip install pytest-cov
pytest --cov=src tests/
```

## 4. Test Categories

| Category | Location | Purpose | Frequency |
| :--- | :--- | :--- | :--- |
| **Unit** | `tests/` | Verify single functions/classes. Mock external dependencies if needed. | On every commit. |
| **Integration** | `experiments/` | Verify end-to-end workflows (I/O, Model Persistence). | Before pushing. |
| **Data Validation** | `src/data_loading` | Runtime checks ensuring data schema/ranges are valid. | Runtime (implicit). |

## 5. Coverage Goals

| Module | Goal | Rationale |
| :--- | :--- | :--- |
| **Data Loaders** | 90%+ | Critical path. Bad data invalidates all downstream results. |
| **Metrics** | 90%+ | Metric logic must be strictly correct to trust evaluations. |
| **Models** | 70%+ | Focus on checking the *wrapper* logic, not testing scikit-learn itself. |
| **Scripts** | 50% | Scripts change often; test via integration tests instead. |

## 6. Continuous Integration
*(Placeholder for Future CI Implementation)*
-   Tests are currently local-only.
-   Future: GitHub Actions to run `pytest` on PRs to `main`.

## 7. Adding New Tests

1.  **Naming**: Files must start with `test_`. Functions must start with `test_`.
2.  **Docstrings**: Use the standard template (Context, Test Cases, Expected Behavior).
3.  **Fixtures**: Use `pytest.fixture` for setup/teardown (especially temp directories).
4.  **Markers**: Use `@pytest.mark.slow` for training tests > 2s.

### Example Template
```python
def test_new_feature(test_config):
    """
    Test that [functionality] works correctly.

    Context:
        [Why this matters]

    Test Cases:
        1. [Scenario 1]

    Expected Behavior:
        [What should happen]
    """
    # Setup
    ...
    # Act
    ...
    # Assert
    assert result == expected
```
