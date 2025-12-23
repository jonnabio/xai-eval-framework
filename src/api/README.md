# XAI Evaluation API

This module exposes the results of XAI experiments to the `xai-benchmark` dashboard via a REST API.

## Architecture

The API follows a **Layered Architecture**:

1.  **Routes** (`routes/`): Entry points for HTTP requests. Handles query parameters and returns responses.
2.  **Services** (`services/`): Business logic.
    -   `data_loader.py`: Reads raw JSON/Parquet files from `experiments/`.
    -   `transformer.py`: Converts raw data into Pydantic models.
3.  **Data Contract** (`models/`): Shared Pydantic schemas ensuring type safety with the Frontend.
4.  **Middleware** (`middleware/`): Global concerns like Error Handling and Logging.

## Configuration

Settings are managed in `config.py` and can be overridden by environment variables or `.env`.

| Variable | Default | Description |
|---|---|---|
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `CORS_ORIGINS` | `["http://localhost:3000"]` | Allowed Dashboard URLs |

## Development

### Running the Server
```bash
python -m src.api.main
```
The API will be available at `http://localhost:8000`.
Documentation (Swagger UI) is at `http://localhost:8000/docs`.

### Testing
```bash
python -m pytest tests/test_api_*.py
```

## Implementation Status

- [x] **001-api-architecture**: Architecture Plan & Structure
- [x] **INT-05**: Data Contract (Pydantic Models)
- [ ] **INT-06**: Data Loader Service
- [ ] **INT-07**: Data Transformer
- [ ] **INT-08**: List Runs Endpoint
- [ ] **INT-09**: Run Details Endpoint
- [ ] **INT-10**: Middleware (Errors & Logging)
