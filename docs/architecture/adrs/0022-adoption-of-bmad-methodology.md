# 22. Adoption of BMAD Methodology

Date: 2026-01-12

## Status

Accepted

## Context

As the complexity of the XAI Evaluation Framework and Dashboard grows, maintaining context and ensuring consistent execution by AI agents has become challenging. We rely heavily on AI assistance for development, but "context drift" and lack of standardized task execution have occasionally slowed progress. We need a structured way to interact with AI agents that mimics a high-performance engineering team.

## Decision

We will adopt the **BMAD (Breakthrough Method for Agile AI-Driven Development)** methodology across all active workspaces.

Key components of this adoption include:

1.  **Agentic Roles**: Explicitly defining personas for the AI to adopt:
    - **Architect**: For planning and design (`PLANNING` mode).
    - **Developer**: For implementation (`EXECUTION` mode).
    - **QA Engineer**: For verification (`VERIFICATION` mode).

2.  **Context Engineering ("Sharding")**:
    - Replacing monolithic context dumps with small, pointed Markdown files in `docs/context/`.
    - Files: `tech_stack.md`, `system_patterns.md`, `active_state.md`.

3.  **Structured Artifacts**:
    - **Implementation Plan**: Required before any code changes.
    - **Walkthrough**: Required after checking in code.
    - **Task Checklist**: Living document tracking granular progress.

## Consequences

### Positive
- **Consistency**: AI agents will produce code that aligns better with existing patterns due to explicitly loaded `system_patterns.md`.
- **Traceability**: Every task will have a clear lineage from Plan -> Code -> Walkthrough.
- **Scalability**: New workspaces can be "bootstrapped" quickly by copying the `docs/bmad` structure.

### Negative
- **Overhead**: Requires maintaining the `docs/context` files. If they go stale, the Agent leads itself astray.
- **Verbosity**: Small tasks might feel "heavy" if forced through the full workflow. *Mitigation*: We will use a lightweight version for minor fixes (skip formal plan, just use task boundary).

## Compliance
All new feature requests must start with the Agent "reading the context" and producing an `implementation_plan.md`.
