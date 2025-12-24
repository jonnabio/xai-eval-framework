# Integration Tests

Comprehensive integration test suite for the XAI Evaluation API.

## Overview

Integration tests verify the complete API workflow end-to-end:
- Request → Data Loading → Transformation → Response
- Use real sample data (not mocks)
- Test actual system behavior

## Running Integration Tests

```bash
# Run all integration tests
python -m pytest src/api/tests/test_integration.py -v

# Run specific test class
python -m pytest src/api/tests/test_integration.py::TestFilteringIntegration -v

# Run with markers
python -m pytest -m integration -v

# Run with coverage
python -m pytest src/api/tests/test_integration.py --cov=src/api
```

## Test Coverage

### Health Checks (3 tests)
- Health endpoint accessible
- Response format validation
- Detailed health system info

### Data Loading (4 tests)
- Sample data loading
- Data structure validation
- Metrics validation
- LLM evaluation validation

### Filtering (7 tests)
- Filter by method (LIME, SHAP)
- Filter by dataset
- Filter by model type
- Filter by model name
- Multiple filters combined
- Empty results handling

### Pagination (6 tests)
- Pagination metadata presence
- Limit parameter functionality
- Offset parameter functionality
- hasNext calculation
- hasPrev calculation
- Total count consistency

### Single Run (3 tests)
- Get run by ID
- Complete data returned
- 404 for non-existent run

### Error Handling (5 tests)
- Invalid limit validation
- Negative offset validation
- Limit exceeding max
- Invalid endpoint 404
- CORS headers

### End-to-End Workflows (3 tests)
- List → Filter → Paginate
- List → Select → Detail
- Complete dashboard workflow

## Prerequisites

Integration tests require:
1. Sample data in `experiments/sample_data/results/`
2. FastAPI application properly configured
3. All services (data_loader, transformer) working

If sample data is missing, run INT-10 sample generation or:
```bash
python scripts/validate_sample_data.py
```
