# Active Context: XAI Evaluation Framework

## Session Metadata
- **Last Updated:** 2026-05-08
- **Branch:** main
- **Mode:** Repository sanitation and project context preservation

## Current Objective
Maintain a clean main branch while preserving project-relevant context for the XAI evaluation framework and thesis production work.

## Current State

### Working
- Core framework supports config-driven XAI experiments.
- FastAPI backend serves experiment runs, health checks, batch operations, and human evaluation endpoints.
- Thesis production is organized under `thesis/` with publication fragments under `pub/`.
- Experiment and recovery workflows are organized under `configs/`, `experiments/`, `scripts/`, and `src/experiment/`.

### Local Tooling
- ACE is local AI-assisted Coding Engineering tooling and is not part of the project source.
- ACE generated files should remain ignored locally via `.git/info/exclude`, not committed to the repository.

### In Progress
- Repository hygiene cleanup on `main`.
- Preserve useful project context while excluding local assistant tooling artifacts.

### Blocked
- Full `git status` can be slow or time out on the WSL `/mnt/c` worktree; prefer targeted Git checks when possible.

## Next Steps
1. Commit the project context updates.
2. Continue using narrow Git commands for status checks on this worktree.
3. Keep ACE artifacts out of project commits unless the project explicitly adopts them later.

## Active Constraints
- Do not commit secrets, generated caches, datasets, model binaries, or local assistant tooling.
- Keep experiment, thesis, API, and dashboard context project-specific.
- Preserve existing project source and generated research artifacts unless explicitly asked to remove them.
