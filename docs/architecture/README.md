# XAI Evaluation Framework Architecture

## Overview
The XAI Evaluation Framework is designed to evaluate explainable AI methods on tabular data models. It consists of a FastAPI backend and a Next.js frontend.

## Documentation Structure
The detailed architecture documentation has been consolidated into the `docs/architecture/` directory.

-   **Start Here**: [Architecture Improvement Plan](architecture/IMPROVEMENT_PLAN.md) - Outlines the current state, security gaps, and improvement roadmap.
-   **Decision Records**: [ADRs](architecture/adrs/) - Historical architectural decisions.

## Key Components
1.  **Backend (`src/api`)**: FastAPI application handling experiment orchestration, data loading, and metric calculation.
2.  **Frontend**: Next.js dashboard for visualizing results.
3.  **Experiment Runner**: Core logic for executing XAI methods (SHAP, LIME) and computing evaluation metrics.

*See `docs/architecture/` for more detailed diagrams and component breakdowns.*
