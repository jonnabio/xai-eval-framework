# Experiments Catalog

This file is now a lightweight registry.

For experiment design, start at [README.md](./README.md).

## Families

| Family | Purpose | Design Doc | Artifact Roots |
|--------|---------|------------|----------------|
| `exp1_adult` | Baseline Adult-dataset calibration and reproducibility | [exp1_adult/README.md](./exp1_adult/README.md) | `experiments/exp1_adult/`, `outputs/` |
| `exp2_comparative` | Fixed-grid comparative benchmark on Adult | [exp2_comparative/README.md](./exp2_comparative/README.md) | `experiments/exp2_comparative/results/`, `outputs/` |
| `exp2_scaled` | Main robustness benchmark on Adult across seeds and sample sizes | [exp2_scaled/README.md](./exp2_scaled/README.md) | `experiments/exp2_scaled/results/`, `outputs/` |
| `exp3_cross_dataset` | Completed external-validation package beyond Adult on Breast Cancer and German Credit | [exp3_cross_dataset/README.md](./exp3_cross_dataset/README.md) | `configs/experiments/exp3_cross_dataset/`, `experiments/exp3_cross_dataset/models/`, `experiments/exp3_cross_dataset/results/`, `outputs/` |
| `exp4_llm_evaluation` | Planned LLM-based semantic proxy evaluation of XAI explanations | [exp4_llm_evaluation/README.md](./exp4_llm_evaluation/README.md) | `experiments/exp4_llm_evaluation/`, `outputs/analysis/exp4_llm_evaluation/` |

## Recent Change Record

EXP3 preparation is documented in:

- [EXP3 preparation walkthrough](./exp3_cross_dataset/EXP3_PREPARATION_WALKTHROUGH.md)
- [EXP3 detailed rationale](./EXP3_CROSS_DATASET_VALIDATION.md)
- [EXP3 result semantics](../results/exp3_cross_dataset/README.md)
- [EXP3 sequential execution plan](../planning/exp3_execution_plan.md)
- [EXP3 partitioned Windows + Linux/WSL execution plan](../planning/exp3_partitioned_execution_plan.md)

The current EXP3 state is `complete`: the Windows Breast Cancer partition and
Linux/WSL German Credit partition were merged into
`results/exp3-windows-breast-cancer`, yielding `24 / 24` planned run artifacts.

Cross-study integration across EXP1, EXP2, and EXP3 is documented in
[EXP1-EXP2-EXP3 Integration Pipeline](../analysis/EXP1_EXP2_EXP3_INTEGRATION_PIPELINE.md).

EXP4 planning is documented in:

- [EXP4 experiment design](./exp4_llm_evaluation/README.md)
- [EXP4 detailed protocol](./exp4_llm_evaluation/DETAILED_DESIGN.md)
- [EXP4 rubric v1](./exp4_llm_evaluation/RUBRIC_V1.md)
- [EXP4 schema v1](./exp4_llm_evaluation/SCHEMA_V1.md)
- [EXP4 result semantics](../results/exp4_llm_evaluation/README.md)
- [EXP4 execution plan](../planning/exp4_llm_evaluation_plan.md)
- [EXP4 implementation plan](../planning/exp4_implementation_plan.md)
- [ADR 0013: EXP4 as LLM-Based Semantic Proxy Evaluation](../adr/0013-exp4-llm-semantic-proxy-evaluation.md)

## Rule

If the question is "what is this experiment?", answer from `docs/experiments/...`.

If the question is "how is it executed?", answer from `configs/experiments/...` and `scripts/...`.

If the question is "what did it produce?", answer from `experiments/.../results/...` and `outputs/...`.
