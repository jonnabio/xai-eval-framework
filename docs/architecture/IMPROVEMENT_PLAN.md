# XAI Evaluation Framework - Architecture Analysis & Improvement Plan

**Status**: Proposed  
**Date**: 2026-01-03  
**Analysis Target**: `xai-eval-framework`, `xai-benchmark`

## Executive Summary

**Current Status**: Functional MVP with significant architectural gaps  
**Overall Assessment**: ⚠️ Needs major improvements for production readiness

This document outlines critical corrections to the system understanding, identifies high-priority security vulnerabilities, and proposes a phased roadmap for scalability and refactoring.

---

## 1. Critical Corrections to Architecture Documentation

### ❌ Python Version
- **Document Claims**: Python 3.13+
- **Actual Implementation**: Python 3.11
- **Evidence**: `environment.yml`, `render.yaml`

### ❌ Missing Components
The initial architecture document omitted 9 critical components that exist in production code:
1.  **CrossValidationRunner** (`src/experiment/cv_runner.py`) - 5-fold stratified CV
2.  **Human Evaluation System** (full API + UI for annotations)
3.  **Analysis Module** (`src/analysis/`) - Statistical analysis, confidence intervals
4.  **Scripts Module** (`src/scripts/`) - 7 utility scripts for operations
5.  **API Middleware Layer** - Exception handling, logging, error middleware
6.  **Services Layer** - Data loader, transformer, batch services
7.  **Monitoring Stack** - Sentry (error tracking) + Prometheus (metrics)
8.  **Admin/Diagnostic UI** (frontend) - Admin validation, diagnostic tools
9.  **State Management** (frontend) - Zustand for global state

### ⚠️ Incomplete API Endpoints
-   `/human-eval` - Human annotation endpoints
-   `/db` - Debug endpoints
-   `/metrics` - Prometheus metrics endpoint
-   Dual mounting strategy (root + `/api` prefix)

---

## 2. High-Priority Security Vulnerabilities

### 🔴 CRITICAL: No Authentication
**Location**: `xai-eval-framework/src/api/routes/*.py`
-   **Risk**: Unauthorized access to experiment data, ability to submit fake annotations.
-   **Recommendation**: Implement OAuth2 with JWT.

### 🔴 CRITICAL: No Rate Limiting
-   **Risk**: DoS attacks, API abuse, excessive LLM costs.
-   **Recommendation**: Implement SlowAPI middleware (`@limiter.limit("100/minute")`).

### 🟡 HIGH: File Path Traversal
**Location**: `src/api/services/data_loader.py`
-   **Current**: No path validation on `load_experiment`.
-   **Recommendation**: Sanitize and validate paths, ensure `is_relative_to(RESULTS_DIR)`.

### 🟡 HIGH: Overly Permissive CORS
**Location**: `src/api/config.py`
-   **Current**: `allow_methods: ["*"]`, `allow_headers: ["*"]`
-   **Recommendation**: Restrict to GET/POST/PUT/DELETE and Content-Type/Authorization headers.

---

## 3. Scalability Bottlenecks

### ⚠️ Backend: Memory Exhaustion
**Problem**: `load_all_experiments()` loads all data into memory.
-   **Impact**: O(n) memory growth.
-   **Recommendation**: Implement pagination + metadata index.

### ⚠️ Backend: Sequential Explanation Generation
**Problem**: SHAP/LIME explanations generated sequentially.
-   **Impact**: Single-threaded CPU usage, slow experiments.
-   **Recommendation**: Parallel batch processing with `ProcessPoolExecutor`.

### ⚠️ Frontend: Client-Side Filtering
**Problem**: Filters 600+ runs in browser on every filter change.
-   **Impact**: Laggy UX, high memory usage.
-   **Recommendation**: Server-side filtering with indexed queries (`/api/runs?model=rf&page=1`).

---

## 4. Code Quality Improvements

### 🔧 Duplicate Code: Explainer Wrappers
**Problem**: `SHAPTabularWrapper` and `LIMETabularWrapper` share 70% code.
**Recommendation**: Extract `ExplainerWrapper` abstract base class.

### 🔧 Tight Coupling: Storage Backend
**Problem**: Direct filesystem dependencies.
**Recommendation**: Implement Repository pattern (`ExperimentRepository` logic separate from `FileSystemRepository` implementation).

### 🔧 Mixed Responsibilities: ExperimentRunner
**Problem**: Monolithic class handling orchestration, computation, and I/O.
**Recommendation**: Split into `ExperimentOrchestrator`, `MetricsEngine`, and `ExperimentRepository`.

---

## 5. Missing Infrastructure Components

### 📦 Database Layer
-   **Migration**: Move from file-based JSON to PostgreSQL.
-   **Benefits**: Indexing, fast filtering, transactions.

### 🔐 Authentication System
-   **Implementation**: FastAPI with JWT.

### 📊 Enhanced Observability
-   **Recommendation**: OpenTelemetry for unified traces, metrics, and logs.

### 🔄 CI/CD Pipeline
-   **Recommendation**: GitHub Actions for Backend/Frontend testing, linting, security scanning, and auto-deployment.

---

## 6. Implementation Roadmap

### Phase 1: Security & Stability (Weeks 1-2)
**Priority**: Critical security vulnerabilities
-   **Authentication (JWT)**:
    -   Install `python-jose[cryptography]` and `passlib`.
    -   Create `src/api/auth.py` for token generation and verification.
    -   Add `get_current_user` dependency to sensitive routes (`/human-eval`, `/admin`).
-   **Rate Limiting**:
    -   Install `slowapi`.
    -   Initialize limiter in `main.py` using `get_remote_address`.
    -   Apply `@limiter.limit("5/minute")` to computationally expensive endpoints like `/runs`.
-   **Path Traversal & CORS**:
    -   Update `data_loader.py` to use `pathlib.Path.resolve()` and check `path.is_relative_to(SAFE_ROOT)`.
    -   Restrict CORS origins to the specific Frontend URL (from env var) in production.
-   **Input Validation**:
    -   Enforce strict Pydantic v2 usage.
    -   Add regex validators for all ID string fields to prevent injection.

### Phase 2: Scalability (Weeks 3-4)
**Priority**: Performance & Workflow Preservation
-   **Migrate to PostgreSQL with Hybrid Sync**:
    -   *Schema Design*: Create tables `experiments` (metadata), `runs` (metrics), and `explanations` (JSONB).
    -   *Sync Script (`sync_db.py`)*:
        1.  Scan `experiments/` directory recursively.
        2.  Compute checksum of each `results.json`.
        3.  Upsert record in DB only if checksum changed (Idempotent Sync).
        4.  Run this script automatically in `startup_event`.
-   **Server-Side Filtering**:
    -   Update `/api/runs` to accept query params: `?model=rf&metric_accuracy_gt=0.8&page=1`.
    -   Rewrite `src/api/services/runs.py` to build SQL queries using `SQLAlchemy` or `SQLModel`.
-   **Parallel Processing**:
    -   Replace sequential loops in `BatchExperimentRunner` with `concurrent.futures.ProcessPoolExecutor`.
-   **Caching**:
    -   Use `functools.lru_cache` for configuration loading.
    -   (Optional) simple Redis cache for expensive aggregation queries.

### Phase 3: Code Quality (Weeks 5-6)
**Priority**: Maintainability
-   **Refactoring Wrappers**:
    -   Create `src/xai/base.py` defining `ExplainerWrapper(ABC)` with abstract method `explain(instance) -> Explanation`.
    -   Subclass `SHAPWrapper` and `LIMEWrapper` enforcing this interface.
-   **Repository Pattern**:
    -   Define `ExperimentRepository` interface (Protocol).
    -   Implement `FileSystemRepository` (current logic) and `SqlRepository` (new DB logic).
    -   Inject repository dependency into API routes to decouple storage details.

### Phase 4: Observability (Week 7)
**Priority**: Monitoring
-   **OpenTelemetry**:
    -   Install `opentelemetry-distro` and `opentelemetry-exporter-otlp`.
    -   Auto-instrument FastAPI and SQLAlchemy.
    -   Configure exporter to send traces to a collector (e.g., Jaeger or Honeycomb).

### Phase 5: Testing & CI/CD (Week 8)
**Priority**: Automation
-   **CI Pipeline (`.github/workflows/ci.yml`)**:
    -   Job 1: Linting (`ruff`, `mypy`).
    -   Job 2: Backend Tests (`pytest --cov`).
    -   Job 3: Frontend Tests (`vitest`).
-   **Load Testing**:
    -   Create `locustfile.py` to simulate 50 concurrent users fetching experiment results.
    -   Verify API latency remains < 200ms under load.

---

## 7. Architectural Decision Records (ADRs)

### ADR-001: Hybrid Database Strategy
**Decision**: Adopt PostgreSQL for query capabilities while retaining JSON files for deployment.
**Rationale**: 
-   **Scalability**: SQL enables `O(1)` lookups and efficient filtering for the dashboard.
-   **Workflow Preservation**: Retaining file-based deployment ensures the existing CI/CD and "Offline Pipeline" remain valid. The DB is a read-only cache of the file system state.

### ADR-002: Adopt OpenTelemetry
**Decision**: Standardize observability using OpenTelemetry.
**Rationale**: Provides unified tracing, metrics, and logs across services.

---

## 8. Conclusion
The current architecture serves as a solid MVP for research but requires specific interventions to be production-ready. The roadmap prioritizes security first, followed by scalability and maintainability.
