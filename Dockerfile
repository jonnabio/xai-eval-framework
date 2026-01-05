# Dockerfile for XAI Evaluation Framework Reproduction
FROM python:3.11-slim

WORKDIR /workspace

# Install system dependencies
# git: for potential pip git installs
# wget: for data download if needed
# gcc/g++: for building python extensions (shap, xgboost)
RUN apt-get update && apt-get install -y \
    git \
    wget \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage caching
COPY requirements-frozen.txt .
RUN pip install --no-cache-dir -r requirements-frozen.txt

# Copy the rest of the application
COPY . .

# Ensure scripts are executable
RUN chmod +x experiments/exp1_adult/reproducibility_package/run_full_pipeline.sh

# Default command: Run the minimal reproduction pipeline
CMD exec python -m uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-10000} --log-level info
