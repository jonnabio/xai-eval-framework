# Architecture Improvement Plan Task Checklist

This checklist tracks the implementation of the tasks outlined in the [Architecture Analysis & Improvement Plan](../../architecture/IMPROVEMENT_PLAN.md).

## Phase 1: Critical Security Fixes

- [ ] **Task 1.1: Fix SSL Verification**
  - [ ] Install `certifi` package.
  - [ ] Remove `ssl._create_unverified_https_context` global override.
  - [ ] Use `urllib` with `certifi.where()` for CA bundle path.
  - [ ] Verify adult dataset downloads work on Mac and Linux.
  - [ ] Test in Render environment.
- [ ] **Task 1.2: Secure or Remove Debug Endpoints**
  - [ ] Choose strategy (authentication, removal, or env variable).
  - [ ] Implement chosen strategy.
  - [ ] Verify endpoints are secure.
- [ ] **Task 1.3: Implement JWT Authentication**
  - [ ] Create `src/api/auth.py` and `src/api/dependencies.py`.
  - [ ] Install `python-jose[cryptography]` and `passlib[bcrypt]`.
  - [ ] Add JWT configuration to `config.py`.
  - [ ] Protect all sensitive routes.
  - [ ] Add authentication tests to `src/api/tests/test_auth.py`.
- [ ] **Task 1.4: Implement Rate Limiting**
  - [ ] Install `slowapi`.
  - [ ] Implement limiter in `src/api/main.py`.
  - [ ] Apply limits to all relevant endpoints.
  - [ ] Make rates configurable via environment variables.
  - [ ] Add rate limit tests.
- [ ] **Task 1.5: Complete Middleware Implementation**
  - [ ] Implement `RequestLoggingMiddleware` in `src/api/middleware/logging.py`.
  - [ ] Implement global error handler in `src/api/middleware/error_handler.py`.
  - [ ] Verify logging and error responses in tests.
- [ ] **Task 1.6: Input Validation Hardening**
  - [ ] Add regex validators to Pydantic models in `src/api/models/schemas.py`.
  - [ ] Add validation tests with malicious inputs.

## Phase 2: Scalability Improvements (File-Based Optimization)

- [ ] **Task 2.1: In-Memory Indexing**
  - [ ] Build `_RUN_ID_INDEX: Dict[str, Path]` on startup in `data_loader.py`.
- [ ] **Task 2.2: Caching Strategy**
  - [ ] Increase `lru_cache` maxsize to 256 in `data_loader.py`.
- [ ] **Task 2.3: Fix N+1 Query Problem**
  - [ ] Create and use `get_experiment_by_run_id` in API routes.
- [ ] **Task 2.4: Optimize Configuration**
  - [ ] Set `max_workers` dynamically based on `cpu_count()` in `config.py`.

## Phase 3: Foundational Scalability (Database Migration)

- [ ] Implement Repository Pattern (see ADR-0008).
- [ ] Define SQLAlchemy models for database schema.
- [ ] Create `DatabaseRepository` implementation.
- [ ] Implement Alembic for database migrations.
- [ ] Create a data synchronization script (`sync_db.py`).
- [ ] Update API dependencies to use `DatabaseRepository`.

## Phase 4: Code Quality Improvements

- [ ] **Task 4.1: Extract ExplainerWrapper Base Class**
  - [ ] Create `src/xai/base.py` with `ExplainerWrapper(ABC)`.
  - [ ] Refactor `SHAPTabularWrapper` and `LIMETabularWrapper` to inherit from base class.
- [ ] **Task 4.2: Unify Metric Interface**
  - [ ] Create `src/metrics/base.py` with `Metric(ABC)`.
  - [ ] Refactor all metric classes to inherit from `Metric`.
  - [ ] Fix typo: `CounterfactualSensivtyMetric` -> `CounterfactualSensitivityMetric`.
- [ ] **Task 4.3: Split ExperimentRunner Responsibilities**
  - [ ] Refactor monolithic `ExperimentRunner` into `ExperimentOrchestrator`, `MetricsEngine`, and `ExperimentRepository`.

## Phase 5: Observability & Monitoring

- [ ] **Task 5.1: Configure Existing Monitoring Stack**
  - [ ] Set Sentry environment variables in production.
  - [ ] Create Grafana dashboard for Prometheus metrics.
  - [ ] Complete `RequestLoggingMiddleware`.
- [ ] **Task 5.2: Add Custom Metrics**
  - [ ] Define custom Prometheus metrics (Counters, Histograms).
  - [ ] Instrument code to increment/observe metrics (e.g., cache hits).
- [ ] **Task 5.3: Alerting Rules**
  - [ ] Define Prometheus alerting rules for high error rates and slow response times.
- [ ] **Task 5.4: (Optional) OpenTelemetry Integration**
  - [ ] Defer until required by microservice architecture.

## Phase 6: Testing & CI/CD

- [ ] **Task 6.1: Expand Test Coverage**
  - [ ] Add tests for authentication.
  - [ ] Add tests for rate limiting.
  - [ ] Add tests for repository layer.
  - [ ] Add performance benchmark tests.
- [ ] **Task 6.2: CI/CD Pipeline (GitHub Actions)**
  - [ ] Create `.github/workflows/backend-ci.yml` for linting, testing, security scanning, and building.
  - [ ] Create `.github/workflows/frontend-ci.yml`.
- [ ] **Task 6.3: Pre-commit Hooks**
  - [ ] Create `.pre-commit-config.yaml`.
  - [ ] Instruct team on `pre-commit install`.
- [ ] **Task 6.4: Load Testing**
  - [ ] Create `locustfile.py` for load testing API endpoints.