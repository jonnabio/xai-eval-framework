# 1. API Architecture

Date: 2025-12-22
Status: Accepted

## Context
The goal is to integrate the `xai-eval-framework` (Backend) with `xai-benchmark` (Frontend Dashboard). Currently, the backend runs ML experiments and saves results as JSON files, but has no mechanism to expose this data to the dashboard. We need a REST API that:
1.  Serves experiment runs and metrics.
2.  Is simple to develop and maintain (solo developer, PhD thesis constraint).
3.  Provides type safety to match the TypeScript frontend.
4.  Scales reasonably for research data (thousands of runs, not millions).

## Decision
We will build the API using **FastAPI** with a **Layered Architecture**.

### Technology Choice: FastAPI
-   **Why**: Modern Python framework, native Pydantic integration (perfect for our Data Contract), automatic OpenAPI/Swagger documentation (crucial for thesis), async support.
-   **Alternatives Considered**:
    -   *Flask*: Mature but requires manual validation and doc generation.
    -   *Django REST Framework*: Too heavy; optimized for DB-backed apps (we use files).

### Architecture Pattern: Layered Strategy
We will separate concerns into three distinct layers:
1.  **Routes Layer** (`src/api/routes/`): Handles HTTP requests, query parameters, and responses. Thin translation layer.
2.  **Service Layer** (`src/api/services/`): Business logic. Validates data, calls data loaders, transforms data into Pydantic models.
3.  **Data Access Layer** (`src/api/services/data_loader.py`): Interacts with the filesystem (JSON/Parquet files).

### Directory Structure
```text
src/api/
├── config.py           # Configuration (Paths, CORS, Version)
├── main.py             # App entry point, Middleware
├── middleware/         # Error handling, Logging
├── models/             # Pydantic Schemas (Shared Contract)
├── routes/             # Endpoints (Runs, Health)
└── services/           # Data Loading & Transformation Logic
```

## Consequences
### Positive
-   **Type Safety**: Pydantic guarantees API outputs match Frontend interfaces.
-   **Documentation**: Auto-generated Swagger UI helps verify endpoints instantly.
-   **Maintainability**: Clear separation of concerns makes it easy to add new metrics or models.

### Negative
-   **No Database**: We are sticking to file-based storage for now (simplifies deployment but limits complex filtering efficiency).
-   **CORS**: Need to manage cross-origin requests carefully during development.
