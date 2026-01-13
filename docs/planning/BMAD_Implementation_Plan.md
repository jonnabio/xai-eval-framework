# BMAD Implementation Plan: Scaling Agentic Development

**Status**: Draft
**Date**: 2026-01-12
**Target Repos**: `xai-eval-framework`, `XAI_Dashboard`

## Executive Summary
This document outlines the strategy to formally integrate the **BMAD (Breakthrough Method for Agile AI-Driven Development)** methodology into the XAI project ecosystem. The goal is to enhance the partnership between the User and the AI Agent by structuring **Context**, **Planning**, and **Roles** without stalling current critical deployment tasks.

## 1. Core Philosophy: Why BMAD?
We are adhering to the "Build More, Architect Dreams" philosophy.
- **Agentic Planning**: No code is written without a documented plan (`implementation_plan.md`).
- **Context Engineering**: We explicitly manage the context the AI consumes to ensure high-fidelity outputs.
- **Human-in-the-Loop**: The User acts as the "Controller", reviewing plans and artifacts before execution.

## 2. Immediate Integration Steps (Non-Disruptive)

### Phase A: Standardization of Workspaces (Day 0-1)
*Goal: Ensure both repositories speak the same "process language".*

1.  **Dashboard Repository (`XAI_Dashboard`)**:
    *   [ ] Create `docs/planning/` directory (Currently missing).
    *   [ ] Create `docs/bmad/` directory for methodology reference.
    *   [ ] Adopt `task_checklist.md` format for tracking frontend tasks, mirroring the backend's effective structure.

2.  **Framework Repository (`xai-eval-framework`)**:
    *   [ ] Formalize existing `task_checklist_*.md` into the standard BMAD "Task Artifact" model.
    *   [ ] Create `docs/bmad/` to house role definitions.

### Phase B: Context Engineering (The "Brain") (Day 1-2)
*Goal: Create "Shards" of context that AI Agents can ingest rapidly.*

Instead of relying on massive READMEs, we will create focused context files in `docs/context/`:
*   `docs/context/system_patterns.md`: Design patterns, preferred libraries (e.g., "Use Recharts not Chart.js").
*   `docs/context/active_state.md`: A high-level pointer to what is currently "true" in the project (linking to latest stable ADRs).
*   `docs/context/tech_stack.md`: Explicit version constraints (e.g., "Python 3.10+, Next.js 14").

**Action**: I (the Agent) will read these files at the start of complex tasks to "load" the correct context.

### Phase C: Agentic Role Definitions
*Goal: Explicitly switch "hats" during the workflow.*

We will define these roles in `docs/bmad/roles.md`:
1.  **The Architect**: Responsible for `implementation_plan.md` and `docs/architecture`. Focus: Feasibility, Design Patterns.
2.  **The Developer**: Responsible for writing code and updating `task.md`. Focus: Clean code, Tests.
3.  **The QA Engineer**: Responsible for `walkthrough.md`. Focus: Verification, Screenshots, Logs.

## 3. The New Workflow Cycle

For every feature or bugfix (e.g., "Fix Render Deployment"):

1.  **Analysis (Architect)**:
    *   Agent checks `docs/context` and `task.md`.
    *   Agent updates `task_boundary` to "PLANNING".
    *   Agent creates/updates `implementation_plan.md`.
    *   **STOP**: Request User Review/Approval.

2.  **Implementation (Developer)**:
    *   Agent writes code.
    *   Agent updates `docs/planning/task_checklist.md` as items are completed.

3.  **Verification (QA Engineer)**:
    *   Agent runs tests/deployments.
    *   Agent creates `walkthrough.md` with proof (e.g., "Curl output of health check").
    *   **STOP**: Request User Review.

## 4. Next Steps
1.  Approve this plan.
2.  Agent will create the directory scaffolds in `XAI_Dashboard`.
3.  Agent will create the initial `docs/context/system_patterns.md`.
