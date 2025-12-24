# XAI Evaluation API

Backend API for the XAI Evaluation Framework. Serves experiment results to the Next.js Dashboard.

## Architecture

Built with **FastAPI** for high performance and automatic documentation.

- **Stack**: Python 3.10+, FastAPI, Uvicorn, Pydantic
- **Structure**:
    - `routes/`: API endpoints
    - `models/`: Pydantic data schemas
    - `services/`: Business logic (Data Loader, Transformer)
    - `config.py`: Centralized configuration

## Running the API

### Development Mode

```bash
# Method 1: Direct Python
python -m src.api.main

# Method 2: Using uvicorn with auto-reload (Recommended for dev)
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Method 3: Using startup script
# Unix/Mac
./scripts/start_api.sh
# Windows
scripts\start_api.bat
```

### Access Points

- **API Base**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **Health Check**: http://localhost:8000/api/health

## Endpoints

### Health
- `GET /api/health` - Simple health check
- `GET /api/health/detailed` - Detailed health with system info

### Runs
- `GET /api/runs` - List all runs with filtering and pagination
- `GET /api/runs/{id}` - Get single run by ID

### Query Parameters for /api/runs

**Filters** (all optional):
- `dataset`: Filter by dataset (e.g., "AdultIncome", "CIFAR-10")
- `method`: Filter by XAI method (e.g., "LIME", "SHAP")
- `model_type`: Filter by model type (e.g., "classical", "cnn")
- `model_name`: Filter by model name (e.g., "random_forest")

**Pagination**:
- `limit`: Number of results (default: 20, max: 100)
- `offset`: Skip N results (default: 0)

### Example Requests

```bash
# Get all runs
curl http://localhost:8000/api/runs

# Filter by dataset
curl http://localhost:8000/api/runs?dataset=AdultIncome

# Filter by method
curl http://localhost:8000/api/runs?method=LIME

# Combine filters
curl "http://localhost:8000/api/runs?dataset=AdultIncome&method=LIME"

# Pagination
curl http://localhost:8000/api/runs?limit=10&offset=20

# Get specific run
curl http://localhost:8000/api/runs/{run_id}
```

### Response Format

**List Response** (`GET /api/runs`):
```json
{
  "data": [
    {
      "id": "adult_rf_lime_a3b2c1",
      "modelName": "random_forest",
      "accuracy": 85.23,
      ...
    }
  ],
  "pagination": {
    "total": 150,
    "limit": 20,
    "offset": 0,
    "returned": 20,
    "hasNext": true,
    "hasPrev": false
  },
  "metadata": {
    "version": "0.2.0",
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

**Single Run Response** (`GET /api/runs/{id}`):
```json
{
  "data": {
    "id": "adult_rf_lime_a3b2c1",
    "modelName": "random_forest",
    ...full Run object...
  },
  "metadata": {
    "version": "0.2.0",
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

## Configuration

Environment variables (optional/default):

- `API_HOST`: Server host (default: `0.0.0.0`)
- `API_PORT`: Server port (default: `8000`)
- `API_DEBUG`: Debug mode (default: `true`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

## CORS Configuration

Allowed origins (for dashboard):
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:3001`
- `http://127.0.0.1:3001`

## Implementation Status

- [x] FastAPI app & configuration
- [x] CORS Middleware
- [x] Health Check endpoints
- [x] Data Models (Pydantic)
- [x] Data Loader Service
- [x] Data Transformer Service
- [x] Runs list endpoint with filters
- [x] Runs detail endpoint
- [x] Pagination support
- [x] Integration with data loader
- [x] Integration with transformer
- [ ] Authentication (Future)
