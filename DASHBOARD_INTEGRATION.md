# Dashboard Integration Guide

## Overview

This guide explains how to integrate this XAI evaluation framework with the XAI Benchmark Dashboard (`xai-benchmark` project).

## Architecture

The integration follows a client-server architecture:

```
xai-eval-framework (Python Backend)  ←→  xai-benchmark (Next.js Dashboard)
         ↓                                         ↑
    REST API (FastAPI)              HTTP/JSON API calls
         ↓                                         ↑
    Experiment Results  ────────────────→  Interactive Visualizations
```

## Quick Start

### 1. Set up the Python API

```bash
# Install additional dependencies
conda install -c conda-forge fastapi uvicorn pydantic

# Create API structure
mkdir -p api/routes api/services
```

### 2. Run the API server

```bash
# From xai-eval-framework directory
python -m api.main
```

API will be available at `http://localhost:8000`

### 3. Configure the Dashboard

```bash
# In xai-benchmark directory
# Create .env.local with:
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 4. Start the Dashboard

```bash
cd ../xai-benchmark
npm run dev
```

Dashboard will be at `http://localhost:3000`

## Data Contract

The dashboard expects data in this format:

```json
{
  "id": "abc123",
  "modelName": "random_forest",
  "modelType": "classical",
  "dataset": "AdultIncome", 
  "method": "LIME",
  "accuracy": 85.23,
  "explainabilityScore": 0.87,
  "processingTime": 125.5,
  "status": "completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "metrics": {
    "Fidelity": 0.92,
    "Stability": 0.88,
    "Sparsity": 0.75,
    "CausalAlignment": 0.85,
    "CounterfactualSensitivity": 0.78,
    "EfficiencyMS": 125.5
  },
  "llmEval": {
    "Likert": {
      "clarity": 4,
      "usefulness": 4,
      "completeness": 3,
      "trustworthiness": 4,
      "overall": 4
    },
    "Justification": "The explanation provides clear feature importance..."
  }
}
```

## Implementation Files Needed

### 1. API Models (`api/models.py`)

```python
"""Pydantic models matching the dashboard TypeScript types."""
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class ModelType(str, Enum):
    CLASSICAL = "classical"


class Dataset(str, Enum):
    ADULT_INCOME = "AdultIncome"


class XaiMethod(str, Enum):
    LIME = "LIME"
    SHAP = "SHAP"


class MetricSet(BaseModel):
    Fidelity: float = Field(..., ge=0, le=1)
    Stability: float = Field(..., ge=0, le=1)
    Sparsity: float = Field(..., ge=0, le=1)
    CausalAlignment: float = Field(..., ge=0, le=1)
    CounterfactualSensitivity: float = Field(..., ge=0, le=1)
    EfficiencyMS: float = Field(..., ge=0)


class Run(BaseModel):
    id: str
    modelName: str
    modelType: ModelType
    dataset: Dataset
    method: XaiMethod
    accuracy: float
    explainabilityScore: float
    processingTime: float
    status: str
    timestamp: datetime
    metrics: MetricSet
    # ... other fields
```

### 2. Main API App (`api/main.py`)

```python
"""FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="XAI Evaluation API")

# Enable CORS for dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes
from .routes import health, runs
app.include_router(health.router, prefix="/api")
app.include_router(runs.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
```

### 3. Routes (`api/routes/runs.py`)

```python
"""Endpoints for experiment runs."""
from fastapi import APIRouter
from ..services.data_loader import load_runs_from_experiments

router = APIRouter()

@router.get("/runs")
async def get_runs():
    """Get all experiment runs."""
    runs = load_runs_from_experiments()
    return {"data": runs}

@router.get("/runs/{run_id}")
async def get_run(run_id: str):
    """Get specific run by ID."""
    runs = load_runs_from_experiments()
    run = next((r for r in runs if r.id == run_id), None)
    if not run:
        raise HTTPException(status_code=404)
    return {"data": run}
```

### 4. Data Loader (`api/services/data_loader.py`)

```python
"""Load experiment results from filesystem."""
import json
from pathlib import Path
from typing import List
from ..models import Run
from .transformer import transform_experiment_to_run

def load_runs_from_experiments() -> List[Run]:
    """Load all runs from experiment results."""
    runs = []
    experiments_dir = Path(__file__).parent.parent.parent / "experiments"
    
    for exp_dir in experiments_dir.iterdir():
        results_dir = exp_dir / "results"
        if not results_dir.exists():
            continue
            
        for metrics_file in results_dir.glob("*_metrics.json"):
            with open(metrics_file) as f:
                data = json.load(f)
            
            run = transform_experiment_to_run(exp_dir.name, data, metrics_file)
            runs.append(run)
    
    return runs
```

### 5. Transformer (`api/services/transformer.py`)

```python
"""Transform experiment results to API format."""
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from ..models import Run, ModelType, Dataset, XaiMethod, MetricSet, LlmEval, LikertScores

def transform_experiment_to_run(exp_name: str, data: Dict[str, Any], file: Path) -> Run:
    """Transform experiment data to Run object."""
    return Run(
        id=f"{exp_name}_{data.get('model_name')}_{data.get('method')}",
        modelName=data.get("model_name", "unknown"),
        modelType=ModelType.CLASSICAL,
        dataset=Dataset.ADULT_INCOME,
        method=XaiMethod.LIME,
        accuracy=data.get("accuracy", 0) * 100,
        explainabilityScore=calculate_score(data.get("metrics", {})),
        processingTime=data.get("metrics", {}).get("processing_time_ms", 0),
        status="completed",
        timestamp=datetime.fromtimestamp(file.stat().st_mtime),
        metrics=MetricSet(
            Fidelity=data.get("metrics", {}).get("fidelity", 0),
            Stability=data.get("metrics", {}).get("stability", 0),
            Sparsity=data.get("metrics", {}).get("sparsity", 0),
            CausalAlignment=data.get("metrics", {}).get("causal_alignment", 0),
            CounterfactualSensitivity=data.get("metrics", {}).get("counterfactual", 0),
            EfficiencyMS=data.get("metrics", {}).get("processing_time_ms", 0),
        ),
        llmEval=LlmEval(
            Likert=LikertScores(clarity=3, usefulness=3, completeness=3, 
                               trustworthiness=3, overall=3),
            Justification="Pending LLM evaluation"
        ),
    )

def calculate_score(metrics: Dict) -> float:
    """Calculate overall explainability score."""
    weights = {"fidelity": 0.3, "stability": 0.25, "sparsity": 0.15, 
               "causal_alignment": 0.2, "counterfactual": 0.1}
    return sum(metrics.get(k, 0) * v for k, v in weights.items())
```

## Testing

### Test API Directly

```bash
# Health check
curl http://localhost:8000/api/health

# Get all runs
curl http://localhost:8000/api/runs

# Get specific run
curl http://localhost:8000/api/runs/exp1_adult_rf_lime
```

### Test Full Integration

1. Start API: `python -m api.main`
2. Start dashboard: `cd ../xai-benchmark && npm run dev`
3. Open `http://localhost:3000`
4. Verify data appears in visualizations

## Next Steps

1. Add database support for scalability
2. Implement authentication
3. Add real-time WebSocket updates for running experiments
4. Deploy both services to production

## References

- FastAPI docs: https://fastapi.tiangolo.com/
- Dashboard types: `xai-benchmark/src/lib/types.ts`
- API adapter: `xai-benchmark/src/lib/apiAdapter.ts`
