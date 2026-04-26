# Experiment Design Hub

This directory is the single human-readable source of truth for experiment design in the project.

It separates three concerns that were previously mixed together:

- `docs/experiments`: what each experiment is, why it exists, what claims it supports
- `docs/results`: where each experiment family's results live and how result semantics are defined
- `configs/experiments`: machine-readable execution manifests and runnable YAML configs
- `experiments/.../results` and `outputs/...`: raw run artifacts and derived analysis products

## Design Rules

Every experiment family should have a design README under `docs/experiments/<experiment_family>/README.md`.

That README should define:

- purpose
- thesis or paper role
- factor matrix
- execution scope
- artifact contract
- links to implementation configs and result roots

The corresponding machine-readable manifest should live under `configs/experiments/<experiment_family>/manifest.yaml`.

## Experiment Registry

| Experiment Family | Design Doc | Machine Manifest | Status |
|-------------------|------------|------------------|--------|
| `exp1_adult` | [exp1_adult/README.md](./exp1_adult/README.md) | Mixed legacy config layout | Active / legacy |
| `exp2_comparative` | [exp2_comparative/README.md](./exp2_comparative/README.md) | [configs/experiments/exp2_comparative](../../configs/experiments/exp2_comparative) | Active |
| `exp2_scaled` | [exp2_scaled/README.md](./exp2_scaled/README.md) | [configs/experiments/exp2_scaled/manifest.yaml](../../configs/experiments/exp2_scaled/manifest.yaml) | Active |
| `exp3_cross_dataset` | [exp3_cross_dataset/README.md](./exp3_cross_dataset/README.md) | [configs/experiments/exp3_cross_dataset/manifest.yaml](../../configs/experiments/exp3_cross_dataset/manifest.yaml) | Ready for partitioned execution |

## Recent EXP3 Readiness

EXP3 is now ready for the remaining partitioned matrix. The project has:

- dataset-loader support for `breast_cancer` and `german_credit`;
- 24 generated YAML configs across two datasets, two models, two explainers, and three seeds;
- 12 trained model binaries and 12 fitted preprocessors from `scripts/train_exp3_models.py`;
- the Breast Cancer RF/SHAP seed-42 smoke result under `experiments/exp3_cross_dataset/results/`;
- runner dispatch support for the new EXP3 datasets;
- loader tests and lightweight config validation;
- a full change inventory in [exp3_cross_dataset/EXP3_PREPARATION_WALKTHROUGH.md](./exp3_cross_dataset/EXP3_PREPARATION_WALKTHROUGH.md).

The remaining 23 raw results should be produced through the partitioned
Windows + Linux/WSL runbook after each worker passes its local dependency and
Git push preflights.

EXP3 execution runbooks:

- [Sequential EXP3 execution plan](../planning/exp3_execution_plan.md)
- [Partitioned Windows + Linux/WSL EXP3 execution plan](../planning/exp3_partitioned_execution_plan.md)

## Storage Policy

Experiment design belongs here.

Result semantics are documented in:

- [docs/results/README.md](../results/README.md)

Execution artifacts belong elsewhere:

- runnable configs: `configs/experiments/...`
- raw experiment outputs: `experiments/.../results/...`
- derived analysis exports: `outputs/...`
- paper and thesis interpretation: `docs/reports/...`

## Reorganization Notes

This hub exists to correct the previous state where EXP1 and EXP2 design details were spread across:

- root README
- experiment-specific folders
- paper drafts
- config trees
- scripts

Those sources may still contain useful operational or reporting detail, but this directory should now be treated as the primary entry point for understanding experiment intent and scope.
