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
1. **CrossValidationRunner** (`src/experiment/cv_runner.py`) - 5-fold stratified CV
2. **Human Evaluation System** (full API + UI for annotations)
3. **Analysis Module** (`src/analysis/`) - Statistical analysis, confidence intervals
4. **Scripts Module** (`src/scripts/`) - 7 utility scripts for operations
5. **API Middleware Layer** - Exception handling, logging, error middleware
6. **Services Layer** - Data loader, transformer, batch services
7. **Monitoring Stack** - Sentry (error tracking) + Prometheus (metrics)
8. **Admin/Diagnostic UI** (frontend) - Admin validation, diagnostic tools
9. **State Management** (frontend) - Zustand for global state

### ⚠️ Incomplete API Endpoints

- `/human-eval` - Human annotation endpoints
- `/db` - Debug endpoints
- `/metrics` - Prometheus metrics endpoint
- Dual mounting strategy (root + `/api` prefix)

---
## 2. High-Priority Security Vulnerabilities

### 🔴 CRITICAL: Disabled SSL Verification

**Location**: `src/data_loading/adult.py:17-25`
```python
ssl._create_default_https_context = ssl._create_unverified_https_context
```
- **Risk**: Vulnerable to MITM attacks during dataset downloads
- **Impact**: CRITICAL - Production security vulnerability
- **Recommendation**: Use `certifi` package for proper CA bundle handling

### 🔴 CRITICAL: Debug Endpoints Exposed

**Location**: `src/api/routes/debug.py`
- **Risk**: `/db/files` and `/db/loader` expose internal filesystem paths
- **Impact**: Information disclosure helps attackers map system structure
- **Recommendation**: Remove endpoints or add authentication

### 🔴 CRITICAL: No Authentication on Admin Endpoints

**Location**: `src/api/routes/human_eval.py:214, 253`
- **Risk**: Unauthorized access to experiment data, ability to submit fake annotations
- **Evidence**: `TODO: Add authentication check` comments in code
- **Recommendation**: Implement OAuth2 with JWT

### 🔴 CRITICAL: No Rate Limiting

**Location**: No rate limiting middleware found
- **Risk**: DoS attacks, API abuse, excessive LLM costs
- **Evidence**: No `slowapi` or similar in `requirements.txt`
- **Recommendation**: Implement SlowAPI middleware (`@limiter.limit("100/minute")`)

### 🟡 MEDIUM: Authentication Flag Disabled

**Location**: `src/api/config.py:80`
```python
HUMAN_EVAL_REQUIRE_AUTH: bool = False  # Set True for production
```
- **Risk**: Even with auth implemented, it's disabled by default
- **Recommendation**: Enable by default, disable only for local development

### 🟡 MEDIUM: Incomplete Middleware Implementation

**Locations**:
- `src/api/middleware/error_handler.py` - Empty (TODO comment)
- `src/api/middleware/logging.py` - Empty (TODO comment)
- **Impact**: Inconsistent error handling, no request auditing
- **Recommendation**: Complete middleware before production

### 🟢 LOW: CORS Configuration (Actually Acceptable)

**Location**: `src/api/config.py:40-54`
- **Current**: `allow_methods: ["*"]`, `allow_headers: ["*"]` BUT origins are whitelisted
- **Assessment**: Standard practice for REST APIs with known frontends
- **Status**: Acceptable as-is, document rationale in ADR

### 🟢 LOW: File Path Traversal (Theoretical Risk)

**Location**: `src/api/services/data_loader.py`
- **Current**: Only iterates within `EXPERIMENTS_DIR`, no user-supplied paths
- **Assessment**: No practical exploit path exists
- **Status**: Low priority, add validation for defense-in-depth

---
## 3. Scalability Bottlenecks

### ⚠️ Backend: N+1 Query Problem

**Location**: `src/api/routes/runs.py:199-217`
```python
async def get_run(run_id: str):
    experiments = load_all_experiments()  # ← Loads ALL to find ONE
    for exp_data in experiments:
        run = transform_experiment_to_run(exp_data)
        if run.id == run_id:
            return RunResponse(data=run, ...)
```
- **Impact**: Every single-run request loads 100+ JSON files from disk
- **Recommendation**: Create `get_experiment_by_run_id()` that loads single file

### ⚠️ Backend: Cache Size Too Small

**Location**: `src/api/services/data_loader.py:195`
```python
@lru_cache(maxsize=32)  # ← Only 32 entries
```
- **Impact**: With 100+ experiments, cache hit rate <32%
- **Recommendation**: Increase to 256 or make configurable

### ⚠️ Backend: Memory Exhaustion

**Location**: `src/api/services/data_loader.py:91-116`
- **Problem**: `load_all_experiments()` loads all data into memory on every request
- **Impact**: O(n) memory growth, filesystem scan every time
- **Recommendation**: Implement pagination at data loading level + metadata index

### ⚠️ Backend: Hardcoded Worker Limit

**Location**: `src/api/services/batch_service.py:93`
```python
df, manifest = runner.run(parallel=True, max_workers=2)  # ← Hardcoded!
```
- **Impact**: Cannot utilize multi-core systems (16-core machine uses only 2)
- **Recommendation**: Make configurable via environment variable, default to `cpu_count() - 1`

### ⚠️ Backend: Sequential Explanation Generation

**Location**: `src/experiment/runner.py`
- **Problem**: SHAP/LIME explanations generated sequentially
- **Impact**: Single-threaded CPU usage, slow experiments
- **Recommendation**: Parallel batch processing with `ProcessPoolExecutor`

### ⚠️ Backend: Duplicate Data Transformation

**Location**: `src/api/routes/runs.py:99-150`
- **Problem**: Each experiment transformed during filtering AND during response rendering
- **Impact**: 2x CPU overhead per request
- **Recommendation**: Cache transformed results or transform once

### ⚠️ Frontend: Client-Side Filtering

**Location**: Dashboard components
- **Problem**: Filters 600+ runs in browser on every filter change
- **Impact**: Laggy UX, high memory usage
- **Recommendation**: Server-side filtering with indexed queries (`/api/runs?model=rf&page=1`)

---
## 4. Code Quality Improvements

### 🔧 Duplicate Pagination Logic

**Locations**:
- `src/api/routes/runs.py:119-134`
- `src/api/services/data_loader.py:236-246`
```python
# Identical pattern in both files
total = len(items)
start = offset
end = min(offset + limit, total)
return items[start:end], total
```
- **Recommendation**: Extract to `utils/pagination.py` as reusable utility

### 🔧 Duplicate Code: Explainer Wrappers

**Location**: `src/xai/`
- **Problem**: `SHAPTabularWrapper` and `LIMETabularWrapper` share 70% code
- **Recommendation**: Extract `ExplainerWrapper` abstract base class

### 🔧 Inconsistent Metric Interfaces

**Location**: `src/metrics/`
- **Problem**: Not all metrics inherit from `BaseMetric`, different `compute()` signatures
- **Evidence**:
  - `DomainAlignmentMetric` - standalone class
  - `CounterfactualSensivtyMetric` - standalone class (also has typo)
- **Recommendation**: Create unified `Metric(ABC)` interface

### 🔧 Tight Coupling: Storage Backend

**Location**: `src/api/services/data_loader.py`
- **Problem**: Direct filesystem dependencies throughout
- **Recommendation**: Implement Repository pattern (`ExperimentRepository` interface, `FileSystemRepository` and `DatabaseRepository` implementations)

### 🔧 Mixed Responsibilities: API Routes

**Location**: `src/api/routes/runs.py:87-150`
- **Problem**: Routes handle filtering, transformation, and pagination logic
- **Recommendation**: Move business logic to service layer

### 🔧 Mixed Responsibilities: ExperimentRunner

**Location**: `src/experiment/runner.py`
- **Problem**: Monolithic class handling orchestration, computation, and I/O
- **Recommendation**: Split into `ExperimentOrchestrator`, `MetricsEngine`, and `ExperimentRepository`

### 🔧 Incomplete TODOs in Production Code

**Locations**:
- `src/api/middleware/error_handler.py:6` - "TODO: Implement Global Exception Handler in INT-10"
- `src/api/middleware/logging.py:5` - "TODO: Implement Request Logging in INT-10"
- `src/api/routes/human_eval.py:214, 253` - "TODO: Add authentication check"
- `src/api/services/transformer.py:163` - "TODO: Real metric normalization logic needs to be robust"
- **Recommendation**: Complete or remove TODOs before production deployment

### 🔧 Typo in Class Name

**Location**: `src/metrics/sensitivity.py:12`
```python
class CounterfactualSensivtyMetric:  # ← Missing 'i' in Sensitivity
```
- **Recommendation**: Rename to `CounterfactualSensitivityMetric`

---
## 5. Missing Infrastructure Components

### 📦 Database Layer

- **Current**: File-based JSON storage only
- **Limitation**: No indexing, O(n) queries, no transactions
- **Migration Path**: Move to PostgreSQL with hybrid approach
- **Benefits**: Indexing, fast filtering, transactions, concurrent writes

### 🔐 Authentication System

- **Current**: No authentication implemented
- **Required**: FastAPI with JWT for admin endpoints
- **Implementation**: OAuth2 password bearer with role-based access control

### 📊 Observability Enhancement

- **Current**: Sentry and Prometheus available but need configuration
- **Status**: Infrastructure exists, needs environment setup and monitoring dashboards
- **Optional Addition**: OpenTelemetry for unified traces, metrics, and logs

### 🔄 CI/CD Pipeline

- **Current**: Manual deployment via git push
- **Needed**: GitHub Actions for automated testing, linting, security scanning
- **Benefits**: Catch bugs before production, enforce code quality standards

---
## 6. Implementation Roadmap

### Phase 1: Critical Security Fixes

**Priority**: Must complete before production use

#### Task 1.1: Fix SSL Verification

- **Location**: `src/data_loading/adult.py:17-25`
- **Action**:
  - Install `certifi` package
  - Remove `ssl._create_unverified_https_context` global override
  - Use `urllib` with `certifi.where()` for CA bundle path
- **Testing**: Verify adult dataset downloads work on Mac and Linux
- **Verification**: Test in Render environment

#### Task 1.2: Secure or Remove Debug Endpoints

- **Location**: `src/api/routes/debug.py`
- **Options**:
  a. Add authentication requirement (preferred)
  b. Remove endpoints entirely (simplest)
  c. Disable via environment variable in production
- **Action**: Choose option based on operational needs
- **Testing**: Verify endpoints return 401 when unauthenticated (if kept)

#### Task 1.3: Implement JWT Authentication

- **Files to Create**:
  - `src/api/auth.py` - Token generation and verification
  - `src/api/dependencies.py` - `get_current_user`, `get_admin_user` dependencies
- **Dependencies**: Install `python-jose[cryptography]` and `passlib[bcrypt]`
- **Configuration**: Add to `config.py`:
```python
JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
JWT_ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS: int = 24
```
- **Protected Routes**:
  - `GET /human-eval/admin/stats` - Admin only
  - `GET /human-eval/admin/annotations` - Admin only
  - `GET /db/*` - Admin only (if keeping debug endpoints)
- **Testing**: Add authentication tests to `src/api/tests/test_auth.py`

#### Task 1.4: Implement Rate Limiting

- **Dependencies**: Install `slowapi`
- **Implementation**:
```python
# src/api/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```
- **Apply Limits**:
  - `/runs` - `@limiter.limit("100/minute")`
  - `/runs/{id}/details` - `@limiter.limit("50/minute")`
  - `/human-eval/*` - `@limiter.limit("20/minute")`
  - POST endpoints - `@limiter.limit("10/minute")`
- **Configuration**: Make rates configurable via environment variables
- **Testing**: Use pytest with rate limit mocking

#### Task 1.5: Complete Middleware Implementation

- **File**: `src/api/middleware/logging.py`
```python
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] {request.method} {request.url}")
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"[{request_id}] Status: {response.status_code} Duration: {duration:.3f}s")
    return response
```
- **File**: `src/api/middleware/error_handler.py`
  - Implement consistent error response format
  - Add request ID to error responses
  - Log errors with full context (but sanitize sensitive data)
- **Testing**: Verify logging in tests, check error response format

#### Task 1.6: Input Validation Hardening

- **Action**: Add regex validators to Pydantic models
```python
run_id: str = Field(..., pattern=r'^[a-zA-Z0-9_-]+$')
dataset: str = Field(..., pattern=r'^[a-zA-Z0-9_]+$')
```
- **Location**: `src/api/models/schemas.py`
- **Testing**: Add validation tests with malicious inputs

---
## Phase 2: Scalability Improvements (File-Based Optimization)

**Goal**: Solve performance bottlenecks (N+1 queries, linear scans) using efficient in-memory indexing and caching, avoiding the complexity of a database.

**Rationale**: Current scale (<1000 experiments) does not justify a database. In-memory indexing provides O(1) performance with zero operational cost.

### Proposed Changes

#### Task 2.1: In-Memory Indexing
- **Component**: `src/api/services/data_loader.py`
- **Action**: Build `_RUN_ID_INDEX: Dict[str, Path]` on startup.
- **Benefit**: Replaces O(n) filesystem scan with O(1) dict lookup.

#### Task 2.2: Caching Strategy
- **Component**: `src/api/services/data_loader.py`
- **Action**: Increase `@lru_cache(maxsize=32)` to `maxsize=256`.
- **Benefit**: Caches ~2.5MB of data, covering active working set.

#### Task 2.3: Fix N+1 Query Problem
- **Component**: `src/api/routes/runs.py`
- **Action**: Use `get_experiment_by_run_id` (cached/indexed) instead of `load_all_experiments()`.
- **Benefit**: Reduces latency from ~500ms to <50ms.

#### Task 2.4: Optimize Configuration
- **Component**: `src/api/config.py`
- **Action**: Set `max_workers` dynamically based on `cpu_count()`.

### Verification Plan
- **Benchmark**: Measure response time of `/runs/{id}` before and after.
- **Memory**: Ensure index doesn't consume excessive RAM (expected <1MB).
- **Correctness**: Verify all experiments are discoverable.

#### Task 4.1: Extract ExplainerWrapper Base Class

**File**: `src/xai/base.py`
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List
import numpy as np

class ExplainerWrapper(ABC):
    """Abstract base class for XAI explainers"""

    def __init__(self, model: Any, **kwargs):
        self.model = model
        self.config = kwargs

    @abstractmethod
    def explain(self, instance: np.ndarray, **kwargs) -> Dict[str, Any]:
        """
        Generate explanation for a single instance.
        
        Returns:
            Dict with 'feature_importance' (weights dict) and method-specific data
        """
        pass

    @abstractmethod
    def explain_batch(self, instances: np.ndarray, **kwargs) -> List[Dict[str, Any]]:
        """Generate explanations for batch of instances"""
        pass

    def get_feature_names(self) -> List[str]:
        """Get feature names if available"""
        return getattr(self, 'feature_names', [])

    def preprocess_instance(self, instance: np.ndarray) -> np.ndarray:
        """Common preprocessing logic"""
        if len(instance.shape) == 1:
            return instance.reshape(1, -1)
        return instance

    def format_explanation(self, weights: Dict[str, float], top_k: int = 10) -> Dict:
        """Common formatting logic for explanations"""
        sorted_features = sorted(weights.items(), key=lambda x: abs(x[1]), reverse=True)
        return {
            "top_features": [
                f"{feat}: {weight:.4f}"
                for feat, weight in sorted_features[:top_k]
            ],
            "raw_weights": dict(sorted_features[:top_k])
        }
```

**Update**: `src/xai/shap_tabular.py`
```python
from src.xai.base import ExplainerWrapper
import shap

class SHAPTabularWrapper(ExplainerWrapper):
    """SHAP explainer for tabular models"""

    def __init__(self, model: Any, training_data: np.ndarray, feature_names: List[str], **kwargs):
        super().__init__(model, **kwargs)
        self.feature_names = feature_names
        self.explainer = shap.TreeExplainer(model)
        self.training_data = training_data

    def explain(self, instance: np.ndarray, **kwargs) -> Dict[str, Any]:
        instance = self.preprocess_instance(instance)
        shap_values = self.explainer.shap_values(instance)

        # Extract SHAP values (handle multi-class output)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]  # Positive class

        weights = dict(zip(self.feature_names, shap_values[0]))

        return {
            "feature_importance": weights,
            "explanation": self.format_explanation(weights),
            "method": "shap",
            "base_value": self.explainer.expected_value
        }

    def explain_batch(self, instances: np.ndarray, **kwargs) -> List[Dict[str, Any]]:
        return [self.explain(inst) for inst in instances]
```

**Update**: `src/xai/lime_tabular.py` similarly

**Benefits**:
- Eliminate 70% code duplication
- Easier to add new explainers (just implement `explain()` method)
- Consistent interface for all explainers

#### Task 4.2: Unify Metric Interface

**Update**: `src/metrics/base.py`
```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class Metric(ABC):
    """Unified base class for all XAI metrics"""

    def __init__(self, **config):
        self.config = config
        self.name = self.__class__.__name__.replace("Metric", "").lower()

    @abstractmethod
    def compute(self, explanation: Dict, **kwargs) -> float:
        """
        Compute metric value.
        
        Args:
            explanation: Dict with 'feature_importance' (weights)
            **kwargs: Metric-specific parameters
            
        Returns:
            Metric value (normalized 0-1 if possible)
        """
        pass

    def validate_inputs(self, explanation: Dict, **kwargs):
        """Common validation logic"""
        if "feature_importance" not in explanation:
            raise ValueError(f"{self.name} requires 'feature_importance' in explanation")
```

**Update All Metrics**: Inherit from `Metric` and implement `compute(explanation, **kwargs)`

**Fix Typo**: Rename `CounterfactualSensivtyMetric` → `CounterfactualSensitivityMetric`

#### Task 4.3: Split ExperimentRunner Responsibilities

**Current Problem**: ExperimentRunner is a monolithic class (300+ lines) handling:
1. Experiment orchestration
2. Explainer initialization
3. Metric computation
4. Result serialization
5. File I/O

**Refactored Structure**:

```python
# src/experiment/orchestrator.py
class ExperimentOrchestrator:
    """High-level experiment workflow coordination"""

    def __init__(self, config: ExperimentConfig, repository: ExperimentRepository):
        self.config = config
        self.repository = repository
        self.metrics_engine = MetricsEngine(config.metrics)

    def run(self) -> ExperimentResult:
        # Load data
        data = self.load_dataset()

        # Train or load model
        model = self.get_model()

        # Initialize explainer
        explainer = self.create_explainer(model, data)

        # Sample instances
        instances = self.sample_instances(data)

        # Generate explanations and compute metrics
        evaluations = self.metrics_engine.evaluate_instances(
            explainer, instances, model, data
        )

        # Build result
        result = ExperimentResult(
            metadata=self.build_metadata(),
            instance_evaluations=evaluations
        )

        # Save
        self.repository.save(result)
        return result

# src/experiment/metrics_engine.py
class MetricsEngine:
    """Handles all metric computation"""

    def __init__(self, metrics_config: MetricsConfig):
        self.metrics = self.initialize_metrics(metrics_config)

    def evaluate_instances(self, explainer, instances, model, data) -> List[InstanceEvaluation]:
        results = []
        for instance in instances:
            explanation = explainer.explain(instance)
            scores = self.compute_all_metrics(explanation, instance, model, data)
            results.append(InstanceEvaluation(..., metrics=scores))
        return results

    def compute_all_metrics(self, explanation, instance, model, data) -> Dict[str, float]:
        scores = {}
        for metric in self.metrics:
            scores[metric.name] = metric.compute(explanation, instance=instance, model=model, data=data)
        return scores

# src/experiment/repository.py (if not using API repository)
class ExperimentRepository:
    """Handles experiment result persistence"""

    def save(self, result: ExperimentResult):
        # Save to JSON or database
        pass

    def load(self, experiment_id: str) -> ExperimentResult:
        pass
```

**Benefits**:
- Single Responsibility Principle
- Easier testing (mock each component)
- More flexible (swap implementations)

---
### Phase 5: Observability & Monitoring

**Priority**: Production operational excellence

#### Task 5.1: Configure Existing Monitoring Stack

**Sentry Configuration**:
```bash
# Already implemented, just needs environment setup
# In Render dashboard, add:
SENTRY_DSN=https://xxx@sentry.io/xxx
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1
```

**Prometheus Configuration**:
- Already exposes `/metrics` endpoint
- Create Grafana dashboard for API metrics:
  - Request rate by endpoint
  - Response time percentiles (p50, p95, p99)
  - Error rate
  - Cache hit rate

**Request Logging** (complete the TODO):
```python
# src/api/middleware/logging.py
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        logger.info(
            f"[{request_id}] Started {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host
            }
        )

        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        logger.info(
            f"[{request_id}] Completed {response.status_code} in {duration:.3f}s",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "duration_ms": duration * 1000
            }
        )

        response.headers["X-Request-ID"] = request_id
        return response
```

**Add to main.py**:
```python
app.add_middleware(RequestLoggingMiddleware)
```

#### Task 5.2: Add Custom Metrics

**File**: `src/api/middleware/metrics.py`
```python
from prometheus_client import Counter, Histogram

# Define custom metrics
api_requests_total = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

api_request_duration_seconds = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)

cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_name']
)

experiments_loaded_total = Counter(
    'experiments_loaded_total',
    'Total experiments loaded from filesystem'
)
```

**Instrument code**:
```python
# In data_loader.py
@lru_cache(maxsize=256)
def get_experiment_result(run_id: str):
    cache_hits_total.labels(cache_name='experiment_result').inc()
    # ... existing code
```

#### Task 5.3: Alerting Rules

**Prometheus Alerts (if using Prometheus + Alertmanager)**:
```yaml
# alerts.yml
groups:
  - name: xai_api_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(api_requests_total{status=~"5.."}[5m]) > 0.05
        for: 2m
        annotations:
          summary: "High error rate on API"
          description: "{{ $value }}% of requests are failing"

      - alert: SlowResponseTime
        expr: histogram_quantile(0.95, rate(api_request_duration_seconds_bucket[5m])) > 1.0
        for: 5m
        annotations:
          summary: "API response time degraded"
          description: "P95 latency is {{ $value }}s"
```

#### Task 5.4: (Optional) OpenTelemetry Integration

Only add if you need distributed tracing:
```bash
# requirements.txt
opentelemetry-distro
opentelemetry-exporter-otlp
opentelemetry-instrumentation-fastapi
opentelemetry-instrumentation-sqlalchemy
```

```python
# src/api/telemetry.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

def setup_telemetry(app, db_engine):
    provider = TracerProvider()
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.OTLP_ENDPOINT))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app)
    SQLAlchemyInstrumentor().instrument(engine=db_engine)
```

```python
# In main.py
if settings.ENABLE_TELEMETRY:
    setup_telemetry(app, engine)
```

**Note**: Current Sentry + Prometheus stack is sufficient for most use cases. Only add OpenTelemetry if you have microservices or complex distributed systems.

---
### Phase 6: Testing & CI/CD

**Priority**: Automation and quality assurance

#### Task 6.1: Expand Test Coverage

**Current Coverage**: Good foundation exists in `src/api/tests/`

**Add**:
1. **Authentication Tests** (`test_auth.py`):
```python
def test_protected_endpoint_requires_auth():
    response = client.get("/human-eval/admin/stats")
    assert response.status_code == 401

def test_valid_token_grants_access():
    token = create_access_token({"sub": "admin", "role": "admin"})
    response = client.get(
        "/human-eval/admin/stats",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```
2. **Rate Limiting Tests** (`test_rate_limiting.py`):
```python
def test_rate_limit_enforced():
    # Make 101 requests (limit is 100/minute)
    for i in range(101):
        response = client.get("/runs")
        if i < 100:
            assert response.status_code == 200
        else:
            assert response.status_code == 429  # Too Many Requests
```
3. **Repository Tests** (`test_repositories.py`):
```python
def test_database_repository_filtering():
    repo = DatabaseRepository(session)
    runs, total = repo.list_experiments({"dataset": "adult"}, 0, 10)
    assert all(r.dataset == "adult" for r in runs)
```
4. **Performance Benchmarks** (`test_benchmarks.py`):
```python
import pytest

@pytest.mark.benchmark
def test_list_experiments_performance(benchmark):
    result = benchmark(lambda: client.get("/runs?limit=20"))
    assert result.status_code == 200
    # Ensure response time < 200ms
```

#### Task 6.2: CI/CD Pipeline (GitHub Actions)

**File**: `.github/workflows/backend-ci.yml`
```yaml
name: Backend CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install ruff mypy
          pip install -r requirements.txt

      - name: Lint with ruff
        run: ruff check src/

      - name: Type check with mypy
        run: mypy src/ --ignore-missing-imports

  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: xai_eval_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-benchmark

      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/xai_eval_test
        run: |
          pytest src/api/tests/ \
            --cov=src/api \
            --cov-report=xml \
            --cov-report=term-missing \
            --benchmark-skip

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install bandit
        run: pip install bandit[toml]

      - name: Security scan with bandit
        run: bandit -r src/ -ll -f json -o bandit-report.json

      - name: Upload security report
        uses: actions/upload-artifact@v3
        with:
          name: bandit-report
          path: bandit-report.json

  build:
    runs-on: ubuntu-latest
    needs: [lint, test, security]
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t xai-eval-framework .

      - name: Test Docker image
        run: |
          docker run -d -p 10000:10000 --name test-container xai-eval-framework
          sleep 10
          curl -f http://localhost:10000/health || exit 1
          docker stop test-container
```

**File**: `.github/workflows/frontend-ci.yml`
```yaml
name: Frontend CI

on:
  push:
    branches: [main, develop]
    paths:
      - 'frontend/**'
  pull_request:
    branches: [main]
    paths:
      - 'frontend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./frontend

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Run tests
        run: npm run test

      - name: Build
        run: npm run build
```

#### Task 6.3: Pre-commit Hooks

**File**: `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=1000']

  - repo: https://github.com/python-poetry/poetry
    rev: 1.7.0
    hooks:
      - id: poetry-check
```

**Setup**:
```bash
pip install pre-commit
pre-commit install
```

#### Task 6.4: Load Testing

**File**: `tests/load/locustfile.py`
```python
from locust import HttpUser, task, between

class XAIAPIUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def list_runs(self):
        self.client.get("/api/runs?limit=20")

    @task(2)
    def get_run_details(self):
        # Assume we have a known run_id
        self.client.get("/api/runs/some-run-id")

    @task(1)
    def get_instances(self):
        self.client.get("/api/runs/some-run-id/instances?limit=50")

    def on_start(self):
        # Called once per user on startup
        pass
```

**Run load test**:
```bash
locust -f tests/load/locustfile.py --host=https://xai-eval-framework.onrender.com
# Open browser to http://localhost:8089
# Configure: 50 users, spawn rate 10/s
# Verify API latency stays < 200ms under load
```

---
## 7. Architectural Decision Records (ADRs)

### ADR-001: Optimized File-Based Architecture
 
 **Decision**: Retain file-based architecture but optimize with in-memory indexing and caching.
 
 **Context**:
 - Original plan proposed database migration for scalability.
 - Analysis showed current scale (<1000 experiments) fits easily in memory.
 - Database adds significant operational complexity (Render Addon costs, migrations, sync logic).
 
 **Rationale**:
 - **Performance**: In-memory dict lookup is O(1), faster than database network round-trip.
 - **Simplicity**: No external dependencies (`postgres`), no `alembic`, no `sync_db`.
 - **Cost**: Zero additional cost on Render.
 - **Maintenance**: Codebase remains simple and purely Python-based.
 
 **Consequences**:
 - Must implement `_RUN_ID_INDEX` in `data_loader.py`.
 - Application startup time increases slightly (scanning files once).
 - Filtering happens in Python (fast enough for <10k items).
 
 **Alternatives Considered**:
 1. **Database Migration**: Rejected as over-engineering for current scale.
 2. **Current State**: Rejected due to O(n) scan performance issues.
 3. **Chosen: Optimized File-Based**: Best balance of performance and simplicity.

---
### ADR-002: Adopt OpenTelemetry (Optional)

**Decision**: Use existing Sentry + Prometheus stack; add OpenTelemetry only if needed.

**Context**:
- Sentry already implemented for error tracking
- Prometheus already implemented for metrics
- OpenTelemetry provides unified observability

**Rationale**:
- Current stack covers 90% of monitoring needs
- OpenTelemetry adds complexity without clear benefit at current scale
- Can add later if system grows to microservices
- Focus effort on completing middleware and monitoring dashboards

**Consequences**:
- Stick with proven tools (Sentry, Prometheus)
- Add structured logging with correlation IDs
- Build Grafana dashboards for existing metrics
- Defer OpenTelemetry to future phase

---
### ADR-003: Repository Pattern for Data Access

**Decision**: Implement Repository pattern with `ExperimentRepository` interface.

**Context**:
- Data access logic spread across routes and services
- Tight coupling to filesystem makes testing difficult
- Database migration requires rewriting data access

**Rationale**:
- **Abstraction**: Decouple business logic from storage implementation
- **Testability**: Easy to mock repositories in tests
- **Flexibility**: Swap between filesystem and database implementations
- **Migration Path**: Can run both implementations in parallel during transition

**Implementation**:
```python
class ExperimentRepository(ABC):
    @abstractmethod
    def list_experiments(filters, offset, limit) -> (List[Run], int)
    
    @abstractmethod
    def get_experiment_by_run_id(run_id) -> Optional[ExperimentResult]

class DatabaseRepository(ExperimentRepository):
    # Fast SQL queries

class FileSystemRepository(ExperimentRepository):
    # Current filesystem logic
```

**Consequences**:
- All routes depend on `ExperimentRepository` interface
- Can switch implementations via dependency injection
- Easier testing with mock repositories
- Clear separation of concerns

---
### ADR-004: JWT Authentication for Admin Endpoints

**Decision**: Use JWT tokens with role-based access control for admin endpoints.

**Context**:
- Admin endpoints currently unprotected (human eval stats, annotations export)
- Need authentication without external dependency
- Must work with stateless API (no sessions)

**Rationale**:
- **JWT**: Industry standard, stateless, works with FastAPI
- **RBAC**: Simple role field in token (admin, annotator, viewer)
- **FastAPI Integration**: Built-in OAuth2 password bearer support
- **No Database**: Token validation doesn't require DB lookup

**Implementation**:
```python
# Generate token
token = create_access_token({"sub": username, "role": "admin"})

# Protect endpoint
@router.get("/admin/stats")
async def get_stats(current_user: User = Depends(get_admin_user)):
    # Only admin role can access
```

**Consequences**:
- Tokens expire after 24 hours
- Need `JWT_SECRET_KEY` environment variable
- Can add more granular permissions later
- All sensitive endpoints require authentication

---
### ADR-005: Parameterize max_workers for Batch Processing

**Decision**: Make batch processing worker count configurable, default to `cpu_count() - 1`.

**Context**:
- Currently hardcoded to `max_workers=2`
- Cannot utilize multi-core systems effectively
- Different environments have different CPU counts

**Rationale**:
- **Scalability**: Use all available CPU cores
- **Flexibility**: Override via environment variable for constrained environments
- **Sensible Default**: `cpu_count() - 1` leaves one core for system tasks

**Configuration**:
```python
# config.py
BATCH_MAX_WORKERS: int = Field(
    default_factory=lambda: max(1, cpu_count() - 1),
    env="BATCH_MAX_WORKERS"
)
```

**Consequences**:
- Batch experiments run 4-8x faster on typical machines
- Can limit workers on Render free tier (set `BATCH_MAX_WORKERS=2`)
- No breaking changes (backwards compatible)

---
## 8. Conclusion

The current architecture serves as a solid MVP for research but requires specific interventions to be production-ready. The roadmap prioritizes security first (critical fixes that must be done before production use), followed by performance quick wins (high impact, low effort), then scalability foundation (database migration), and finally code quality improvements.

**Implementation Priority**

**Must Do Before Production**:
- Phase 1: Security fixes (SSL, authentication, rate limiting, debug endpoints)

**High Impact Quick Wins**:
- Phase 2 Tasks 2.1-2.4: Cache size, N+1 fix, max_workers, pagination utility

**Foundation for Scale**:
- Phase 3: Database migration with hybrid approach

**Long-term Maintenance**:
- Phase 4: Code quality refactoring
- Phase 5: Complete observability stack
- Phase 6: CI/CD automation

**Success Metrics**

**Security**:
- ✅ All admin endpoints require authentication
- ✅ No critical security vulnerabilities in bandit scan
- ✅ Rate limiting prevents DoS attacks

**Performance**:
- ✅ Single run lookup < 50ms (from 500ms+)
- ✅ List 100 runs < 200ms
- ✅ Batch experiments use all CPU cores

**Quality**:
- ✅ Test coverage > 80%
- ✅ CI/CD pipeline catches bugs before merge
- ✅ No TODO comments in production code

**Operations**:
- ✅ Error rate < 0.1%
- ✅ P95 latency < 500ms
- ✅ Alerts configured for anomalies
