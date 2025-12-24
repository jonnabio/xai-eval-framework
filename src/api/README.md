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

### Testing Endpoints

```bash
# Health check
curl http://localhost:8000/api/health

# Detailed health
curl http://localhost:8000/api/health/detailed

# API info
curl http://localhost:8000/
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
- [ ] Experiment Runs Endpoints (`/api/runs`)
- [ ] Authentication (Future)
