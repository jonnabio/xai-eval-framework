# 0024: Recursive Experiment Loading

## Status
Accepted

## Context
The initial data loading strategy for the XAI Dashboard assumed a flat structure where all experiment results were located in `experiments/<experiment_name>/results/*.json`. 

However, the reproducibility studies (EXP1-29) introduced a deep directory structure:
`experiments/exp1_adult/reproducibility/exp1_adult_xgb_lime/seed_<SEED>/results.json`

The original `data_loader.py` failed to discover these nested files, resulting in only ~20 experiments loading in the dashboard (from `exp2_comparative`) instead of the expected 600+.

## Decision
We have updated the `src.api.services.data_loader` module to implement **recursive discovery** of result files.

### Key Changes
1.  **Discovery Scope**: The `discover_experiment_directories` function now considers the root `experiments` folder as the search base.
2.  **Recursive Search**: The `find_result_files` function now uses `rglob("results.json")` (and `rglob("*_metrics.json")`) to find files at any depth within the experiment structure.
3.  **Git Configuration**: Updated `.gitignore` to explicitly un-ignore (whitelist) these deep result paths to ensure they are tracked in version control and deployed to Render.

## Consequences
### Positive
- **Complete Visibility**: All valid `results.json` files, regardless of nesting depth (e.g., tuning runs, seeded reproducibility runs), are now loaded.
- **Robustness**: The loader is less brittle to directory structure changes.

### Negative
- **Performance**: Recursive searching over a very large filesystem could be slower, though insignificant for <1000 files.
- **Repo Size**: Committing hundreds of JSON result files increases the git repository size.

## Compliance
- This change requires all experiment results to be named `results.json` (or `*_metrics.json` for legacy support).
- Development environments must ensure these files are not ignored by `git` if they are intended for production (see `docs/ops/sync_experiments_guide.md`).
