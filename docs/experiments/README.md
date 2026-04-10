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
| `exp2_comparative` | [exp2_comparative/README.md](./exp2_comparative/README.md) | [configs/experiments/exp2_comparative](../../../configs/experiments/exp2_comparative) | Active |
| `exp2_scaled` | [exp2_scaled/README.md](./exp2_scaled/README.md) | [configs/experiments/exp2_scaled/manifest.yaml](../../../configs/experiments/exp2_scaled/manifest.yaml) | Active |
| `exp3_cross_dataset` | [exp3_cross_dataset/README.md](./exp3_cross_dataset/README.md) | [configs/experiments/exp3_cross_dataset/manifest.yaml](../../../configs/experiments/exp3_cross_dataset/manifest.yaml) | Proposed |

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
