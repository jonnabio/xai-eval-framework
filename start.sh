#!/bin/bash

echo "=================================================="
echo "🚀 Starting XAI Evaluation Backend"
echo "=================================================="
echo "Environment: $(python --version)"
echo "Working Directory: $(pwd)"
echo "PORT: ${PORT:-10000}"
echo ""

# SKIP PIPELINE ON STARTUP
# The pipeline takes 3-5 minutes which causes Render health checks to fail
# Run manually if needed: python run_pipeline.py --mode minimal
echo "⚠️  Skipping pipeline execution on startup"
echo "   API will start immediately for health checks"
echo ""

# Run startup diagnostics
echo "Running diagnostics..."
python debug_startup.py
echo "Diagnostics complete."
echo ""

# Start FastAPI server immediately
echo "Starting FastAPI server..."
echo "=================================================="

# Use python -m to ensure correct environment
exec python -m uvicorn src.api.main:app \
    --host 0.0.0.0 \
    --port ${PORT:-10000} \
    --log-level info
