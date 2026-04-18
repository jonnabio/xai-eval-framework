# Branching Strategy & Workflow

## Project Context
- **Thesis**: "Arquitectura Agnóstica para la Interpretabilidad de Modelos de Inteligencia Artificial de Caja Negra"
- **Goal**: Develop a Model-Agnostic XAI Evaluation Framework.
- **Scope**: Multi-machine distributed experiments (Exp1 Adult MVP completed; Exp2 comparative/scaled in progress).

## Branch Roles

### `main`
- **Status**: Stable, production-ready, source of truth for thesis results.
- **Usage**: Backs thesis results and paper figures.
- **Rule**: All changes merged here via PR or explicit merge commit. Do not push directly during active experiments.

### `results/<worker-id>` (e.g. `results/jon_asus`, `results/linux_dell`)
- **Purpose**: Auto-sync checkpoints from distributed worker machines.
- **Lifecycle**: Created per worker run; merged into `main` when results are verified; deleted after merge.
- **Current state**:
  - `results/jon_asus` — merged into `main` (same commit as HEAD).
  - `results/linux_dell` — active Linux worker branch (last commit: `eea42d43`).

### `linux_dell`
- **Purpose**: Claim/metadata branch for the Linux Dell worker.
- **Current state**: Active, tracking worker state (`eea42d43`).

### Future Dev Branches (Naming Pattern)
- `dev/exp2-*`: Comparative/scaled experiments.
- `dev/exp3-*`: Text experiments.
- `dev/exp4-*`: Time series experiments.

## Workflow

### Feature / Experiment Development
1. **Start from `main`**:
   ```bash
   git checkout main
   git pull
   git checkout -b dev/<scope>
   ```
2. Commit frequently on the feature/experiment branch.
3. Open a PR into `main` when the slice is stable (pipeline runs end-to-end).
4. Self-review: ensure tests pass, docs/README updated, figures match thesis claims.
5. Merge and delete the dev branch.

### Distributed Worker Results
1. Each worker auto-pushes to its `results/<worker-id>` branch.
2. When a worker run finishes, verify results, then merge into `main`:
   ```bash
   git checkout main
   git merge results/<worker-id> --no-ff -m "merge(results/<worker-id>): <description>"
   ```
3. Delete the remote worker branch after merge if no longer needed:
   ```bash
   git push origin --delete results/<worker-id>
   ```

## Commit Message Style
Use clear, descriptive, conventional commit messages:

- `feat: add Adult data loader`
- `feat: add RF/XGBoost models for Exp1`
- `feat: add LIME/SHAP wrappers`
- `chore: update environment.yml`
- `chore(worker): update <worker-id> manifest state`
- `docs: update Exp1 methodology notes`
- `merge(results/<worker-id>): integrate worker results`

## Tagging (Milestones)
Create lightweight tags for major experimental milestones to preserve exact states used for the thesis:
- `v0.1-exp1-adult-mvp`
- `v0.2-exp1-full-benchmark`
- `v0.3-exp2-comparative` _(planned)_
