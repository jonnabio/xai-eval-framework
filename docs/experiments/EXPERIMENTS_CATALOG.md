# Experiments Catalog

This file is now a lightweight registry.

For experiment design, start at [README.md](./README.md).

## Families

| Family | Purpose | Design Doc | Artifact Roots |
|--------|---------|------------|----------------|
| `exp1_adult` | Baseline Adult-dataset calibration and reproducibility | [exp1_adult/README.md](./exp1_adult/README.md) | `experiments/exp1_adult/`, `outputs/` |
| `exp2_comparative` | Fixed-grid comparative benchmark on Adult | [exp2_comparative/README.md](./exp2_comparative/README.md) | `experiments/exp2_comparative/results/`, `outputs/` |
| `exp2_scaled` | Main robustness benchmark on Adult across seeds and sample sizes | [exp2_scaled/README.md](./exp2_scaled/README.md) | `experiments/exp2_scaled/results/`, `outputs/` |
| `exp3_cross_dataset` | Prepared external-validation package beyond Adult; execution deferred until EXP2 finishes | [exp3_cross_dataset/README.md](./exp3_cross_dataset/README.md) | `configs/experiments/exp3_cross_dataset/`, `experiments/exp3_cross_dataset/models/`, `experiments/exp3_cross_dataset/results/`, `outputs/` |

## Recent Change Record

EXP3 preparation is documented in:

- [EXP3 preparation walkthrough](./exp3_cross_dataset/EXP3_PREPARATION_WALKTHROUGH.md)
- [EXP3 detailed rationale](./EXP3_CROSS_DATASET_VALIDATION.md)
- [EXP3 result semantics](../results/exp3_cross_dataset/README.md)

The current EXP3 state is `prepared / not yet executed`: configs, loaders,
runner support, model-prep scripts, and validation tests exist; raw EXP3
result artifacts are intentionally absent until the active EXP2 worker
finishes and the first Breast Cancer SHAP smoke test is run.

## Rule

If the question is "what is this experiment?", answer from `docs/experiments/...`.

If the question is "how is it executed?", answer from `configs/experiments/...` and `scripts/...`.

If the question is "what did it produce?", answer from `experiments/.../results/...` and `outputs/...`.
