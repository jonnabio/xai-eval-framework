 # 0001. Record Architecture Decisions

**Date**: 2025-12-16  
**Status**: Accepted

## Context
A PhD thesis requires rigorous documentation of the "why" behind software design choices. As the framework evolves (Exp1 -> Exp2), implicit decisions can be lost, making it difficult to defend choices in the dissertation or reproduce results later.

## Decision
We will use **Architectural Decision Records (ADRs)** to immutably record significant design choices.
-   Format: Markdown files in `docs/decisions/`
-   Naming: `NNNN-title-in-kebab-case.md`
-   Structure: Title, Status, Context, Decision, Consequences.

## Consequences
-   **Positive**: Clear audit trail for the thesis methodology chapter.
-   **Negative**: Slight overhead in creating files for decisions.
