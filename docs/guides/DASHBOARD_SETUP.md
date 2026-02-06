# Dashboard Setup & Integration Guide

## Overview
This document provides a comprehensive guide to setting up, running, and troubleshooting the `xai-benchmark` dashboard and its backend `xai-eval-framework`.

## Architecture
- **Frontend**: `xai-benchmark` (Next.js) - Visualizes results.
- **Backend**: `xai-eval-framework` (FastAPI) - Runs experiments and serves data.
- **Comms**: REST API via `NEXT_PUBLIC_API_URL`.

## Prerequisites
- **Node.js**: v18+ (for dashboard)
- **Python**: 3.10+ (for API)
- **Libs**: `pip install -r requirements.txt` (Must include `alibi` and `dice-ml` for all experiments)

## Setup Instructions

### 1. Backend Setup (`xai-eval-framework`)
1.  **Install Dependencies**:
    ```bash
    cd xai-eval-framework
    pip install -r requirements.txt
    pip install alibi dice-ml  # Critical for Anchors/DiCE
    ```
2.  **Start API Server**:
    ```bash
    # Starts server on http://localhost:8000
    .venv/bin/python -m uvicorn src.api.main:app --port 8000 --host 0.0.0.0
    ```
3.  **Run Experiments** (Optional if results exist):
    ```bash
    # To run missing/skipped experiments
    python scripts/run_recovery.py --config-dir configs/experiments/exp2_scaled --workers 1
    ```

### 2. Frontend Setup (`xai-benchmark`)
1.  **Install Dependencies**:
    ```bash
    cd xai-benchmark
    npm install
    ```
2.  **Configure Environment**:
    Create `.env.local` in `xai-benchmark/`:
    ```env
    NEXT_PUBLIC_API_URL=http://localhost:8000/api
    ```
3.  **Start Dashboard**:
    ```bash
    npm run dev
    ```
    Access at `http://localhost:3000`.

## Troubleshooting

### Feature Mismatch Error
*Error*: `ValueError: X has 107 features, but MLPClassifier is expecting 108 features`.
*Cause*: Mismatch between training-time preprocessor and test-time data loading.
*Fix*: Ensure `runner.py` loads the saved `preprocessor.joblib` from the model directory (`experiments/exp1_adult/models/`) instead of creating a new one.

### Missing Dependencies
*Error*: `ModuleNotFoundError: No module named 'alibi'` (or `dice_ml`).
*Fix*: Run `pip install alibi dice-ml`. These are heavy dependencies often excluded from minimal installs but required for full benchmarks.

## Data Flow
1.  Experiments run -> Results save to `experiments/.../results.json`
2.  API (`src/api`) reads JSONs -> Serves via `/api/runs`
3.  Frontend fetches `/api/runs` -> Displays charts.
