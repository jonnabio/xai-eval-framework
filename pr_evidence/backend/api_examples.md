# API Request Examples

## 1. Run Experiment
```bash
curl -X POST "http://localhost:8000/api/runs" \
  -H "Content-Type: application/json" \
  -d '{
    "dataset": "AdultIncome",
    "model_type": "random_forest",
    "method": "LIME",
    "params": {"sample_size": 100}
  }'
```

Response:
```json
{
  "id": "adult_rf_lime_1703498200",
  "status": "completed",
  "dataset": "AdultIncome",
  "modelName": "random_forest",
  "metrics": {
    "Fidelity": 0.85,
    "Stability": 0.92,
    "Sparsity": 0.75,
    ...
  }
}
```

## 2. Get Experiment List
```bash
curl "http://localhost:8000/api/runs?limit=5"
```

Response:
```json
{
  "data": [
    {
      "id": "adult_rf_lime_1",
      "modelName": "random_forest",
      ...
    }
  ],
  "pagination": {
    "total": 1,
    "limit": 5,
    "offset": 0
  }
}
```
