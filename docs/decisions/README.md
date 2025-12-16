# Architectural Decision Records (ADRs)

This log indexes all significant architectural decisions made during the development of the XAI Evaluation Framework.

| ID | Title | Status | Date | Summary |
| :--- | :--- | :--- | :--- | :--- |
| [0001](0001-record-architecture-decisions.md) | **Record Architecture Decisions** | Accepted | 2025-12-16 | Adopt ADRs to document design choices for the PhD thesis. |
| [0002](0002-use-yaml-configuration.md) | **Use YAML for Configuration** | Accepted | 2025-12-16 | Switch from JSON to YAML to support inline comments for reproducibility. |
| [0003](0003-class-based-model-wrappers.md) | **Class-Based Model Wrappers** | Accepted | 2025-12-16 | Refactor training logic into classes to manage state and lifecycle. |

## Template

When adding a new decision, copy this format:
```markdown
# NNNN. Title

**Date**: YYYY-MM-DD
**Status**: Proposed/Accepted/Deprecated

## Context
...
## Decision
...
## Consequences
...
```
