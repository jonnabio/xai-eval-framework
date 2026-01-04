#!/bin/bash
set -e  # Exit on any error

echo "=================================================="
echo "🚀 Starting XAI Evaluation Backend"
echo "=================================================="
echo "Environment: $(python --version)"
echo "Working Directory: $(pwd)"
echo "PORT: ${PORT:-10000}"
echo ""

# Step 1: Run pipeline once on startup
echo "Step 1: Running XAI evaluation pipeline (minimal mode)..."
python run_pipeline.py --mode minimal || {
    echo "⚠️  Pipeline failed but continuing to start API server..."
}

echo ""
echo "✅ Pipeline complete!"
echo ""

# Step 2: Start FastAPI server and keep it running
echo "Step 2: Starting FastAPI server..."
echo "=================================================="

# Use PORT from environment (Render sets this), default to 10000
exec uvicorn src.api.main:app \
    --host 0.0.0.0 \
    --port ${PORT:-10000} \
    --log-level info
