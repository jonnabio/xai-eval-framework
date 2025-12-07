# Branching Strategy & Workflow

## Project Context
- **Thesis**: "Arquitectura Agnóstica para la Interpretabilidad de Modelos de Inteligencia Artificial de Caja Negra"
- **Goal**: Develop a Model-Agnostic XAI Evaluation Framework.
- **Scope**: Multiple experiments starting with tabular data (Adult dataset MVP) and extending to image, text, and time series.

## Branch Roles

### `main`
- **Status**: Stable, runnable, production-ready.
- **Usage**: Backs thesis results and paper figures.
- **Rule**: Direct commits are discouraged; always merge via Pull Requests (PRs), even when working solo.

### `dev/exp1-adult-mvp`
- **Status**: Working branch for Experiment 1 (Tabular/Adult MVP).
- **Focus**: Dataset loader, model training, XAI wrappers, metrics implementation, and initial LLM evaluation.

### Future Branches (Naming Pattern)
- `dev/exp2-*`: Image experiments.
- `dev/exp3-*`: Text experiments.
- `dev/exp4-*`: Time series experiments.

## Workflow

1. **Start from `main`**:
   Always ensure you are starting from the latest stable version.
   ```bash
   git checkout main
   git pull
   git checkout -b dev/exp1-adult-mvp
   ```

2. **Develop**:
   Commit frequently on your feature/experiment branch.

3. **Pull Request**:
   When the experiment slice is stable (e.g., pipeline runs end-to-end), open a PR into `main`.

4. **Review**:
   (Self-review is acceptable). Ensure:
   - Tests pass.
   - README/Docs are updated.
   - Figures/Metrics generated match thesis claims.

5. **Merge**:
   Merge the PR and delete the dev branch if it is no longer needed.

## Commit Message Style
Use clear, descriptive, conventional commit messages:

- `feat: add Adult data loader`
- `feat: add RF/XGBoost models for Exp1`
- `feat: add LIME/SHAP wrappers`
- `chore: update environment.yml`
- `docs: update Exp1 methodology notes`

## Tagging (Milestones)
Create lightweight tags for major experimental milestones to preserve exact states used for the thesis:
- `v0.1-exp1-adult-mvp`
- `v0.2-exp1-full-benchmark`
