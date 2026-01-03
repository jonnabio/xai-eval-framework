# Documentation Workflow Reference

This document outlines the standard workflow for documenting changes, planning tasks, and verifying results in the XAI Evaluation Framework.

## 1. Planning Phase

Before writing code, we define **what** we are doing and **why**.

### 1.1 Implementation Plan (Artifact)
- **File**: `implementation_plan.md` (Ephemeral/Agentic Artifact) or specific planning docs in `docs/planning/`.
- **Purpose**: Defines the technical approach, user reviews required (ranges, breaking changes), and verification strategy.
- **Key Sections**: Goal Description, User Review Required, Proposed Changes, Verification Plan.

### 1.2 Task Checklists
- **File**: `docs/planning/task_checklist_exp1_XX_YY.md`
- **Purpose**: Tracks high-level progress of experiments and project phases.
- **Action**: Mark tasks as `[x]` upon completion.

### 1.3 Prompt Execution Plans
- **File**: `docs/planning/prompt_execution_plan_exp1_XX_YY.md`
- **Purpose**: Defines the specific "Triggers" (User Prompts) and "Context" for the AI agent to execute tasks.
- **Action**: Update status to "Completed" when a task is done.

## 2. Decision Making

Significant architectural changes require a permanent record.

### 2.1 Architecture Decision Records (ADRs)
- **Directory**: `docs/decisions/`
- **Naming**: `XXXX-title-in-kebab-case.md` (Sequential numbering).
- **Format**:
    - **Context**: The problem and options considered.
    - **Decision**: The chosen solution.
    - **Consequences**: Pros, cons, and side effects.
- **When to write**: New frameworks, library choices, major refactors, or methodology changes (e.g., Sensitivity Analysis Framework).

## 3. Implementation & Verification

Documenting the work as it happens and proving it works.

### 3.1 Walkthroughs (Artifact)
- **File**: `walkthrough.md` (Agentic Artifact).
- **Purpose**: A narrative report of what was changed and verified during a session.
- **Content**: Summary of changes, test results, and key findings.

### 3.2 Visualization & Results
- **Directory**: `outputs/`
    - `outputs/experiments/`: Raw JSON results.
    - `outputs/paper_figures/`: Publication-ready vector figures (`.pdf`).
- **LaTeX Integration**: `outputs/paper_figures/figures_include.tex` is auto-generated to easily include new figures in the thesis.

## 4. Code Documentation Requirements

High-quality inline documentation is essential for maintainability.

### 4.1 Docstrings
- **Style**: Google Style Docstrings.
- **Where**: Every module, class, and public function.
- **Content**:
    - **Summary**: One-line description.
    - **Args**: detailed description of arguments.
    - **Returns**: description of return values.
    - **Raises**: explicit listing of exceptions.

### 4.2 Type Hinting
- **Requirement**: 100% type coverage for function signatures.
- **Tools**: Use `typing.List`, `typing.Dict`, `typing.Optional`, etc.

### 4.3 Comments
- **Inline Comments**: specific, non-obvious logic explanations.
- **TODOs**: formatting `TODO(user): description`.

## 5. Git Operations

Committing changes with traceability.

### 5.1 Commit Messages
- **Format**: Conventional Commits.
    - `feat(scope): Description` (New feature)
    - `fix(scope): Description` (Bug fix)
    - `docs(scope): Description` (Documentation)
    - `style`, `refactor`, `test`, `chore`.
- **Scope Examples**: `analysis`, `vis`, `exp1`.

### 5.2 Commit Body Guidelines
- **Body**: Detailed explanation of *what* and *why* (optional but recommended for complex changes).
- **Footer**: Reference issues or tasks (e.g., `Closes #123`).

### 5.3 Branching Strategy
- **Feature Branches**: `feat/description` or `fix/issue-id`.
- **Main**: Protected branch, PR required.

### 5.4 Push Rules
- **Pre-Push Checks**:
    - **Linting**: Ensure code adheres to style (ruff/flake8).
    - **Tests**: Run `pytest` locally to ensure no regressions.
    - **Build**: Verify project builds successfully.
- **Rules**:
    - **No Force Push**: Never force push to shared branches (`main`, `develop`).
    - **Pull Rebase**: Use `git pull --rebase` to maintain a clean history.
    - **Atomic Pushes**: Push logically grouped commits.
    - **Clean State**: Do not push temporary files or unchecked artifacts.

## 6. Thesis & Publication Flow

Specific workflow for thesis-bound content.

1.  **Run Experiment**: `python src/scripts/run_exp1_XX.py` -> JSON in `outputs/`.
2.  **Generate Figures**: `python src/scripts/generate_paper_figures.py` -> PDFs in `outputs/paper_figures/`.
3.  **Update TeX**: The script updates `figures_include.tex`.
4.  **Write Chapter**: Use insights from `walkthrough.md` and figures to write `docs/thesis_methodology_log.md` or the actual thesis document.

## Checklist for Closing a Task

1.  [ ] Code implemented and tested.
2.  [ ] ADR created (if architectural change).
3.  [ ] `task_checklist_*.md` updated.
4.  [ ] `walkthrough.md` updated with findings.
5.  [ ] Git commit with Conventional Commit message.
