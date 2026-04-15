# 7. Optimized File-Based Architecture

Date: 2026-01-10
Status: Accepted

## Context

The initial plan for scaling the application proposed a full database migration to handle a growing number of experiment results. However, an analysis of the current scale (<1000 experiments) shows that the entire dataset can easily fit into memory. A database adds significant operational complexity, including addon costs (e.g., on Render), schema migrations, and data synchronization logic. The current implementation suffers from O(n) performance for single-run lookups, as it scans all files to find one.

## Decision

We will retain the file-based architecture but optimize it with in-memory indexing and enhanced caching. This approach balances performance and simplicity.

**Rationale**:
- **Performance**: An in-memory dictionary lookup is O(1), which is faster than a database network round-trip for this scale.
- **Simplicity**: This avoids introducing external dependencies like PostgreSQL, database connectors, and migration tools (e.g., Alembic). The codebase remains simple and purely Python-based.
- **Cost**: This solution has zero additional infrastructure cost on hosting platforms like Render.
- **Maintenance**: It is easier to maintain a file-based system, which can be version-controlled directly with Git.

**Implementation**:
1.  **In-Memory Indexing**: On application startup, a dictionary `_RUN_ID_INDEX: Dict[str, Path]` will be built, mapping each unique `run_id` to its corresponding JSON file path. This replaces the O(n) filesystem scan with an O(1) lookup.
2.  **Enhanced Caching**: The `lru_cache` size for data loading functions will be increased from 32 to 256 to better cover the active working set of experiments.

## Consequences

### Positive
-   The `GET /api/runs/{run_id}` endpoint performance will improve dramatically (from ~500ms to <50ms).
-   The system avoids the operational overhead and cost of a database.
-   The architecture remains simple and easy for new developers to understand.

### Negative
-   Application startup time will increase slightly to build the initial index (a one-time cost).
-   All filtering logic remains in Python. This is performant for the current scale (<10,000 items) but may become a bottleneck at a much larger scale.
-   This solution is not suitable for environments with very high concurrency or where multiple writer processes need to be coordinated.

### Alternatives Considered
1.  **Full Database Migration**: Rejected as over-engineering for the current project scale.
2.  **Retain Current State**: Rejected due to unacceptable O(n) performance for single-item lookups.