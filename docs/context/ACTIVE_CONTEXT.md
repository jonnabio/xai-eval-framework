# Active Context: XAI Evaluation Framework

## Session Metadata
- **Last Updated:** 2026-06-20
- **Branch:** publication/cifie-xai-fom7-book-chapter
- **Mode:** Publication workstream scaffolding

## Current Objective
Create and maintain a separate CIFIE collective book chapter workstream derived from the doctoral XAI research while preserving existing thesis and paper artifacts.

## Current State

### Working
- Core framework supports config-driven XAI experiments.
- FastAPI backend serves experiment runs, health checks, batch operations, and human evaluation endpoints.
- Thesis production is organized under `thesis/` with publication fragments under `pub/`.
- Experiment and recovery workflows are organized under `configs/`, `experiments/`, `scripts/`, and `src/experiment/`.
- CIFIE book chapter scaffolding is organized under `publications/book_chapters/2026_cifie_xai_fom7/` as an independent publication artifact.

### Local Tooling
- ACE is local AI-assisted Coding Engineering tooling and is not part of the project source.
- ACE generated files should remain ignored locally via `.git/info/exclude`, not committed to the repository.

### In Progress
- CIFIE Spanish technical book chapter workstream setup for FOM-7/XAI evaluation.
- Source inventory and evidence mapping for section-by-section chapter drafting.
- Extraction pass 1 completed for initial references, citation audit, and metrics table.
- Extraction pass 2 completed for empirical result summary and figure registry.
- Extraction pass 3 completed for FOM-7 protocol details and gate reconciliation.
- Controlled drafting pass 1 completed for XAI foundations and methods sections.
- Preserve useful project context while excluding local assistant tooling artifacts.

### Blocked
- Full `git status` can be slow or time out on the WSL `/mnt/c` worktree; prefer targeted Git checks when possible.

## Next Steps
1. Use `publications/book_chapters/2026_cifie_xai_fom7/sources/evidence_map.md` to extract verified material section by section.
2. Complete APA 7 reference formatting, DOI/URL validation, and citation insertion planning.
3. Decide which registered thesis figures should be copied/exported into the chapter package.
4. Continue section-level drafting with `05_crisis_evaluacion_xai.md` and refine links to `06_protocolo_fom7.md`.
5. Continue using narrow Git commands for status checks on this worktree.
6. Keep ACE artifacts out of project commits unless the project explicitly adopts them later.

## Active Constraints
- Do not commit secrets, generated caches, datasets, model binaries, or local assistant tooling.
- Keep experiment, thesis, API, and dashboard context project-specific.
- Preserve existing project source and generated research artifacts unless explicitly asked to remove them.
- Do not overwrite existing thesis or paper artifacts while developing the CIFIE book chapter.
- Manage the CIFIE chapter as a distinct publication output under `publications/book_chapters/2026_cifie_xai_fom7/`.
