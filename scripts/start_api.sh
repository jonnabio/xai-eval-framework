#!/bin/bash

echo "================================================"
echo "Starting XAI Evaluation API"
echo "================================================"

cd "$(dirname "$0")/.."

# Activate conda environment and run
# Assumes conda is in path or initialized
# If not, you might need: source ~/anaconda3/etc/profile.d/conda.sh

echo "Starting API server..."
python -m src.api.main
