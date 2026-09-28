# ADR-0016: Bound the Interpretation of the EXP4 Reliability Gradient

> **Status:** Accepted<br>
> **Date:** 2026-09-27

---

## Context

EXP4 reports agreement among three LLM judges across seven semantic evaluation
dimensions. All registered ICC(1,1) values are below the thesis's 0.75
acceptability threshold, so the experiment's primary conclusion is negative:
the tested LLM-judge configuration is not reliable enough for confirmatory
assessment.

Agreement nevertheless varies by dimension. Dimensions with more directly
verifiable reference points, including semantic plausibility and completeness,
show comparatively higher agreement than dimensions that depend more strongly
on stakeholder context, presentation, or task-specific judgment. The tutor
asked the thesis to make that gradient more actionable.

The gradient can inform future rubric and calibration work, but it must not be
used to reverse the threshold decision, claim that any dimension is reliable,
or infer a causal explanation from seven observed dimension-level estimates.
EXP4 artifacts and claims are additionally protected by RCA-002.

---

## Decision

We will report EXP4 at two explicitly separated levels.

First, the confirmatory-use decision remains categorical: because every
ICC(1,1) estimate is below 0.75, no evaluated dimension supports using the
current LLM judges as a reliable substitute for human assessment in
confirmatory evaluation.

Second, the between-dimension pattern will be described as a relative,
hypothesis-generating gradient. Comparatively higher agreement on dimensions
with more verifiable semantic anchors will motivate future work on:

- decomposing broad dimensions into observable rubric criteria;
- adding anchored examples and explicit scoring rules;
- calibrating LLM judges against expert-human ratings; and
- prioritizing human review for stakeholder-dependent or task-dependent
  dimensions.

The thesis may state that the observed pattern is **consistent with** more
concrete criteria being easier to judge consistently. It may not state that
criterion type caused the agreement difference, that higher-ranked dimensions
are objectively measured, or that any current dimension has crossed the
reliability threshold.

No bounded operational use of an LLM judge will be recommended from EXP4 alone.
Such a recommendation would require a new calibration study, a declared
acceptance criterion, expert-human reference ratings, and evidence that the
intended use remains valid under the target population and task.

All statistical values and sample-size distinctions will remain sourced from
the recovered and verified EXP4 artifacts. This ADR changes interpretation and
future-work guidance, not the registered calculations.

---

## Alternatives Considered

### Report Only the Blanket Negative Result

- **Pros:** Minimizes the risk of overclaiming and is directly supported by the
  threshold decision.
- **Cons:** Discards a potentially useful design signal for improving rubrics
  and future calibration studies.
- **Why rejected:** A carefully bounded relative interpretation adds practical
  value without changing the negative reliability conclusion.

### Recommend Immediate Use for the Highest-Agreement Dimensions

- **Pros:** Produces a direct deployment recommendation.
- **Cons:** Every dimension remains below 0.75, and no expert-human calibration
  establishes fitness for a bounded operational use.
- **Why rejected:** Relative superiority is not the same as acceptable absolute
  reliability.

### Explain the Gradient as Objective Versus Aesthetic Judgment

- **Pros:** Offers a simple and memorable narrative.
- **Cons:** Overstates what the observed associations establish and can
  mischaracterize dimensions whose interpretation depends on task and
  stakeholder context rather than aesthetics.
- **Why rejected:** The evidence supports a hypothesis-generating distinction,
  not a causal taxonomy of judgment difficulty.

---

## Consequences

### Positive

- Converts the observed gradient into concrete future rubric and calibration
  priorities.
- Preserves the 0.75 boundary and the negative primary EXP4 conclusion.
- Distinguishes relative agreement from acceptable reliability.
- Prevents the thesis from implying causal explanations unsupported by EXP4.

### Negative

- The practical recommendation remains a research agenda rather than an
  immediate automation pathway.
- Repeated wording must be reviewed carefully so that summaries do not drop the
  below-threshold qualifier.

### Neutral

- Registered ICC(1,1), Krippendorff-alpha, and sample-size values do not change.
- This decision does not rerun judges or alter the recovered EXP4 source.

---

## Compliance

Every thesis site that summarizes the dimension gradient must also preserve the
statement that all ICC(1,1) values are below 0.75. Claims about the reason for
the gradient must use non-causal language such as "consistent with" and must be
identified as hypothesis-generating.

Review will run the EXP4 regression guards and claim verification required by
RCA-002. Any future claim that an LLM judge is fit for confirmatory or bounded
operational use requires a separately approved calibration design and new
registered evidence.

---

## References

- [Tutor feedback implementation plan](../planning/tutor-feedback-Sep-22-2026.md)
- [EXP4 thesis results](../../thesis/capitulo-5-taxonomia.qmd)
- [Thesis conclusions](../../thesis/capitulo-6-conclusiones.qmd)
- [RCA-002: EXP4 Source Recovery](../rca/RCA-002-exp4-source-recovery.md)
- [RCA-001: Manuscript-Artifact Drift](../rca/RCA-001-manuscript-artifact-drift.md)
- [Regression guards](../rca/regression-guards.yaml)
