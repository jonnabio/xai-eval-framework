# Database Migration Plan (Phase 2) - REVISED

## 1. Executive Summary
**Status**: APPROVED pending implementation
**Deployment Model**: Research-Only (Option A)
- Experiments are run offline/locally.
- Results are committed to Git as JSON files.
- Render serves data by syncing committed files to the database.
- **Database Provider**: External PostgreSQL (e.g., Neon, Supabase) via `DATABASE_URL`.
- **Sync Strategy**: Background thread on startup.

## 2. Architecture: Hybrid Approach

### 2.1 Principles
- **Source of Truth**: The Git repository (Project Filesystem).
- **Query Engine**: PostgreSQL (Metadata & Instance Index).
- **Data Flow**:
  1. Experiment results committed to `experiments/` dir.
  2. Deployment triggers.
  3. API starts -> Background Thread detects new files -> Syncs to DB.
  4. API queries DB for filtering/pagination.
  5. API reads JSON from disk for full heavy payloads (if needed).

### 2.2 Technology Stack
- **Database**: PostgreSQL 15+ (External/Neon)
- **ORM**: SQLAlchemy 2.0 (Async) + Alembic
- **Driver**: `asyncpg`

## 3. Schema Design

### 3.1 Tables

#### 3.1.1 `experiments`
Stores experiment metadata for fast filtering and file tracking.

```sql
CREATE TABLE experiments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id VARCHAR(100) UNIQUE NOT NULL,

    -- Metadata
    model_name VARCHAR(100) NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    dataset VARCHAR(50) NOT NULL,
    xai_method VARCHAR(50) NOT NULL,

    -- Storage
    file_path VARCHAR(512) NOT NULL, -- Relative path in Repo
    file_checksum VARCHAR(64) NOT NULL, -- MD5 for idempotent sync

    -- Metrics
    metrics JSONB, -- Flexible storage {accuracy: 0.95, ...}
    instance_count INT,

    -- Timestamps
    experiment_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Status
    status VARCHAR(20) DEFAULT 'completed'
);

-- Indexes for performance
CREATE INDEX idx_exp_dataset ON experiments(dataset);
CREATE INDEX idx_exp_method ON experiments(xai_method);
CREATE INDEX idx_exp_model ON experiments(model_name);
CREATE INDEX idx_exp_timestamp ON experiments(experiment_timestamp DESC);
CREATE INDEX idx_exp_metrics ON experiments USING GIN(metrics);
```

#### 3.1.2 `instance_evaluations`
Stores instance-level data to enable pagination without loading massive JSON files.

```sql
CREATE TABLE instance_evaluations (
    id SERIAL PRIMARY KEY,
    experiment_id UUID REFERENCES experiments(id) ON DELETE CASCADE,
    instance_id INT NOT NULL,
    quadrant VARCHAR(2) NOT NULL, -- TP, FP, TN, FN

    -- Predictions
    true_label INT,
    prediction INT,
    prediction_correct BOOLEAN,

    -- Data
    metrics JSONB, -- Instance-level metrics
    -- explanation JSONB, -- OMITTED: Store in file to save DB space, or add if critical for search

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_instances_experiment ON instance_evaluations(experiment_id);
CREATE INDEX idx_instances_quadrant ON instance_evaluations(quadrant);
```

#### 3.1.3 `users` (For later Phase)
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);
```

## 4. Implementation Steps

### Task 2.1: Database Provisioning
1. **Action**: User provisions Postgres (Neon/Render).
2. **Config**: Set `DATABASE_URL` in `.env` and Render Dashboard.

### Task 2.2: Setup & Configuration
1. **Dependencies**: `sqlalchemy[asyncio]`, `asyncpg`, `alembic`, `psycopg2-binary`.
2. **Module**: `src/api/database.py` with `AsyncSession`.
3. **Models**: `src/api/models/orm.py`.

### Task 2.3: Migrations
1. `alembic init -t async migrations`.
2. Configure `alembic.ini` to use `os.getenv("DATABASE_URL")`.
3. Generate/Apply initial schema.

### Task 2.4: Sync Logic (Robust & Idempotent)
**Script**: `scripts/sync_db.py` (callable from module).

**Logic**:
1. Iterate `EXPERIMENTS_DIR`.
2. For each JSON:
   - Compute MD5.
   - Query DB for `run_id`.
   - **IF** exists AND checksum matches: SKIP.
   - **IF** exists AND checksum differs: UPDATE (Update metadata, Delete+Reinsert Instances).
   - **IF** new: INSERT (Experiment + Instances).
3. **Transaction**: Use minimal transactions (per experiment) to avoid locking.

### Task 2.5: Integration (Startup Background Sync)
**File**: `src/api/main.py`

```python
@app.on_event("startup")
async def startup_event():
    if settings.USE_DATABASE:
        import threading
        from scripts.sync_db import sync_all
        # Run in background to pass health checks immediately
        t = threading.Thread(target=sync_all, daemon=True)
        t.start()
```

### Task 2.6: Repository Pattern (Gradual Migration)
1. Interface: `ExperimentRepository`.
2. Implement: `DatabaseRepository` (SQL) & `FileSystemRepository` (Legacy).
3. Switch:
```python
def get_repository():
    return DatabaseRepository() if settings.USE_DATABASE else FileSystemRepository()
```

## 5. Verification Plan
1. **Local Test**: Run Postgres in Docker/Local, run sync, verify tables populated.
2. **Idempotency**: Run sync twice, ensure 2nd run is instantaneous/no-op.
3. **Deployment**:
   - Push to Render.
   - Verify logs: "Background sync started".
   - Verify logs after ~2 min: "Sync complete".
   - Verify API `/runs` returns data.
