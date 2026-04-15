# 10. Parameterize max_workers for Batch Processing

Date: 2026-01-10
Status: Accepted

## Context

The batch experiment runner (`src/api/services/batch_service.py`) currently has a hardcoded worker limit of `max_workers=2`. This prevents the application from utilizing the full processing power of multi-core systems. For example, on a 16-core machine, experiments would run at only a fraction of their potential speed. This limit is also inflexible across different deployment environments (e.g., a powerful local machine vs. a resource-constrained cloud instance).

## Decision

The `max_workers` parameter for batch processing will be made configurable via an environment variable, with a sensible default.

**Rationale**:
- **Scalability**: Allows the application to scale vertically by using all available CPU cores on the host machine.
- **Flexibility**: Enables operators to tune performance based on the deployment environment. For example, the worker count can be lowered on a free-tier cloud service to avoid resource exhaustion or raised on a dedicated server to maximize throughput.
- **Sensible Default**: Defaulting to `cpu_count() - 1` is a common practice that maximizes CPU utilization while leaving one core free for the operating system and other tasks, preventing the system from becoming unresponsive.

**Implementation**:
The configuration will be managed in `config.py` using Pydantic's `Field`.

```python
# config.py
from os import cpu_count

BATCH_MAX_WORKERS: int = Field(
    default_factory=lambda: max(1, cpu_count() - 1),
    env="BATCH_MAX_WORKERS"
)
```
The batch runner will then use this configuration value instead of the hardcoded `2`.

## Consequences

### Positive
-   Batch experiment execution speed will be significantly improved on multi-core machines (potentially 4-8x faster).
-   The application is more adaptable to different hardware and deployment environments.
-   There are no breaking changes, as the functionality is backwards-compatible.

### Negative
-   If not configured carefully in a resource-constrained environment (like a container with limited CPU shares), setting `max_workers` too high could lead to performance degradation or instability due to excessive context switching or memory pressure. The sensible default mitigates this in most cases.