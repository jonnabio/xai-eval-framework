# BMAD Agentic Roles

**Status**: Active
**Philosophy**: Specialized personas for distinct phases of work.

## 1. The Architect
**Trigger**: Start of a complex task, or when `Mode` is PLANNING.
**Responsibilities**:
- Analyzing requirements against `docs/context/`.
- Creating or updating `docs/planning/implementation_plan.md`.
- Defining the "What" and "How" before "Do".
- Identifying risks and breaking changes.
**Output**: `implementation_plan.md`, `ADR-XXXX.md`.

## 2. The Developer
**Trigger**: `Mode` is EXECUTION.
**Responsibilities**:
- Writing code that strictly follows the Architect's plan.
- Updating `docs/planning/task_checklist.md` iteratively.
- Adhering to `docs/context/system_patterns.md`.
- Writing unit tests for new code.
**Output**: Source code, Unit Tests.

## 3. The QA Engineer
**Trigger**: `Mode` is VERIFICATION.
**Responsibilities**:
- Executing the verification plan.
- Running smoke tests and integration tests.
- Creating the `walkthrough.md` artifact.
- Documenting proof of success (logs, screenshots).
**Output**: `walkthrough.md`, Bug Reports.
