# ADR-0015: Define the OOD Validity Boundary of Masking Fidelity

> **Status:** Accepted<br>
> **Date:** 2026-09-27

---

## Context

The thesis operationalizes fidelity by replacing selected features with their
training-set means and measuring the model-output change. This creates a common
perturbation scheme across explainers, but independent feature replacement can
break dependencies among tabular features and produce samples outside the data
distribution.

The thesis already identifies out-of-distribution perturbations as a general
threat and discloses the specific mean-masking limitation in Chapter 6. The
tutor requested that the apparent tension be closed explicitly: the work
criticizes unrealistic perturbations in XAI evaluation while using a masking
metric that is itself exposed to that problem.

A dependency-aware masking experiment or remove-and-retrain study would require
new experimental design, execution, and registration. No such rerun is part of
the approved tutor-feedback scope.

---

## Decision

We will use an explicit validity-boundary disclosure for the existing masking
fidelity metric.

The thesis will state that:

- fidelity replaces selected features independently with their training means;
- this operation does not preserve the joint feature distribution and can
  generate implausible or out-of-distribution observations;
- applying the same masking rule to every explainer improves procedural
  comparability but does not eliminate construct-validity bias;
- the reported fidelity values therefore measure behavior under this specific
  perturbation operator, not explanation truth in an unrestricted sense; and
- claims based on fidelity are bounded to that operationalization and should be
  tested with distribution-aware or retraining-based alternatives in future
  work.

The disclosure will appear where readers need it: at the metric definition in
the methods, in the results interpretation, and in the threats/limitations
discussion. The wording may be concise at repeated sites, but it must point to
one consistent validity boundary.

This decision does not authorize importing EXP6 sensitivity results into the
thesis, rerunning EXP2, or claiming that tabular data or mean replacement solves
the OOD problem. A dependency-aware sensitivity study remains separately
scoped work requiring its own protocol and registered claims.

---

## Alternatives Considered

### Claim That Mean Masking Mitigates OOD Bias

- **Pros:** Preserves a stronger interpretation of the current fidelity values.
- **Cons:** Mean values can still be implausible jointly, especially for
  correlated, constrained, categorical, or one-hot-encoded features.
- **Why rejected:** A shared deterministic baseline improves comparability, not
  distributional validity.

### Add a Dependency-Aware or Remove-and-Retrain Experiment Now

- **Pros:** Could quantify sensitivity to the perturbation mechanism and
  strengthen construct validity.
- **Cons:** Expands the experimental scope, requires protocol choices and new
  computation, and cannot be treated as a documentation-only correction.
- **Why rejected:** It is valuable follow-up work but is outside the approved
  implementation plan.

### Keep the Disclosure Only in Chapter 6

- **Pros:** Avoids repetition in methods and results.
- **Cons:** Readers may encounter and interpret the metric before seeing its
  principal validity limitation.
- **Why rejected:** The limitation is material to the metric definition and to
  the strength of the associated claims.

---

## Consequences

### Positive

- Aligns the thesis's methodological critique with its own measurement design.
- Prevents the fidelity metric from being interpreted as an unqualified ground
  truth measure.
- Preserves the comparability and reproducibility benefits of the existing
  experiment without concealing its validity boundary.

### Negative

- Fidelity conclusions must use narrower language throughout the thesis.
- The disclosure does not estimate the magnitude or direction of the possible
  OOD bias.
- Stronger distribution-aware evidence remains future work.

### Neutral

- No existing numerical result or artifact changes.
- The current masking procedure remains the operational definition for EXP2.

---

## Compliance

Review will verify that the methods, results, and limitations sections use the
same description of independent training-mean replacement and do not claim
that it preserves the data distribution. Conclusions and tables that compare
methods on fidelity must remain explicitly scoped to this operationalization.

Any future dependency-aware or retraining-based sensitivity result must enter
through the registry-first workflow and receive separate scope approval before
it is used to strengthen the thesis claims.

---

## References

- [Tutor feedback implementation plan](../planning/tutor-feedback-Sep-22-2026.md)
- [Experimental design](../../thesis/capitulo-3-diseno-experimental.qmd)
- [EXP2 results](../../thesis/capitulo-4-resultados.qmd)
- [Conclusions and validity boundaries](../../thesis/capitulo-6-conclusiones.qmd)
- [Thesis bibliography](../../thesis/references.bib)
- [Phase 2 evidence claims](../literature/phase2_claims.md)
- [RCA-001: Manuscript-Artifact Drift](../rca/RCA-001-manuscript-artifact-drift.md)
