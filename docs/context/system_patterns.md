# System Patterns & Standards

**Scope**: XAI Evaluation Framework (`xai-eval-framework`)
**Status**: Active

## Architectural Patterns

1. **Config-driven experiment runner**
   - Experiments are defined in `configs/experiments/`.
   - Execution is orchestrated through `src/experiment/runner.py` and batch helpers in `src/experiment/`.
   - Results and manifests should be written to configured output locations, not hardcoded paths.

2. **Standardized XAI wrapper interface**
   - XAI methods live under `src/xai/`.
   - Wrappers expose consistent explanation outputs such as `feature_importance`, `top_features`, and `metadata`.
   - Method-specific behavior should stay inside wrappers, leaving metrics and runners method-agnostic.

3. **Metric interface separation**
   - Metrics live under `src/metrics/`.
   - Metrics should operate on model predictions, explanations, or derived artifacts without owning experiment orchestration.
   - New metrics should follow the existing base/interface patterns.

4. **FastAPI service boundary**
   - API routes live under `src/api/routes/`.
   - Business logic and data loading belong in `src/api/services/`.
   - Pydantic schemas live under `src/api/models/`.
   - API handlers should stay thin and delegate transformation/loading work.

5. **Thesis and publication production**
   - Thesis source lives under `thesis/`.
   - Publication fragments and generated sync artifacts live under `pub/`.
   - Scripts under `scripts/pubs/` manage publication synchronization.

## Coding Standards

- Use YAML configuration for experiment definitions.
- Use Pydantic for validated configuration and API schemas where already established.
- Add type hints for public Python functions.
- Prefer `pathlib` for filesystem paths.
- Keep data loaders, model trainers, explainers, metrics, and API services separated by responsibility.
- Avoid broad refactors when making targeted fixes.

## Repository Hygiene

- ACE is local AI-assisted Coding Engineering tooling and should not be committed as project source.
- Local ACE files are ignored through `.git/info/exclude`.
- Generated caches, large outputs, local datasets, virtual environments, and model binaries should stay out of commits unless explicitly whitelisted.

## Anti-Patterns

- Hardcoding paths instead of using config or established constants.
- Modifying raw data in place.
- Mixing API route logic with data loading or result transformation internals.
- Committing local assistant tooling, generated caches, or environment-specific files.
- Replacing project-specific context with generic framework templates.
