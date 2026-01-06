# 14. Adoption of Domain Alignment Metric

Date: 2025-12-27

## Status

Accepted

## Context

To validate Explainable AI (XAI) methods, we need to assess whether the explanations align with established domain knowledge. For the Adult Income dataset, there is a rich body of Labor Economics literature that identifies theoretical drivers of income.

We initially considered a "Causal Alignment" metric but realized that without a validated causal graph or interventional data, measuring "causality" is strictly impossible and academically risky for the thesis. We need a metric that quantifies alignment with domain priors without making indefensible causal claims.

## Decision

We will implement a **Domain Alignment Metric** that measures the overlap between XAI feature attribution and a tiered set of "Ground Truth" features derived from labor economics theory.

### Ground Truth Feature Set

We define two tiers of features:

**Tier 1 (Core Drivers)**:
- `age`: Experience accumulation.
- `education-num` (or `education`): Human capital.
- `hours-per-week`: Labor supply.
- `occupation`: Skill level/job type.
- `workclass`: Employment sector.

**Tier 2 (Secondary/Demographic Factors)**:
- `marital-status`: Household economics.
- `capital-gain`, `capital-loss`: Wealth accumulation.
- `sex`, `race`: Labor market structural factors.

### Metric Definition

The metric calculates:
1.  **Domain Precision@K**: The fraction of the Top-K explained features that appear in either Tier 1 or Tier 2 lists.
    - $P@K = \frac{|\text{TopK} \cap (\text{Tier1} \cup \text{Tier2})|}{K}$
2.  **Core Recall@K**: The fraction of Tier 1 features found in the Top-K.
    - $R@K = \frac{|\text{TopK} \cap \text{Tier1}|}{|\text{Tier1}|}$

## Consequences

### Positive
- **Academic Rigor**: Avoids false causal claims while leveraging domain knowledge.
- **Interpretability**: Provides a clear score (0-1) for how "sensible" an explanation is to a domain expert.
- **Flexibility**: The "Ground Truth" list can be configured per dataset in the future.

### Negative
- **Dataset Specific**: Heavily relies on the specific definition of "Ground Truth" for the Adult dataset. Requires re-configuration for any new dataset.
- **Subjectivity**: The selection of "Core" vs "Secondary" features is based on literature but involves some subjective judgment.

## Implementation
- **Class**: `src.metrics.domain.DomainAlignmentMetric`
- **Config**: Toggles via `metrics.domain: true`.
