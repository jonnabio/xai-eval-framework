# ADR-0017: Report EXP4 Cohort 2 as a Replication with a Second Judge Panel

> **Status:** Accepted<br>
> **Date:** 2026-09-27<br>
> **Amends:** [ADR-0016](0016-exp4-dimensional-reliability-interpretation.md) (compliance wording)<br>
> **Related:** [RCA-002](../rca/RCA-002-exp4-source-recovery.md),
> `experiments/exp4_cohort2/RESULTS.md`,
> `docs/review/exp4-rerun-readiness_2026-09-27.md`

---

## Context

The raw responses and prompt templates of the original EXP4 cohort are lost
(RCA-002); its committed aggregates remain the source of every published EXP4
number. At the author's request, the study was re-run on 2026-09-27
(cohort 2). The inputs were the **same 192 cases**, recovered by ID from the
committed case list. The judges were a new panel (`openai/gpt-5.4-mini`,
`anthropic/claude-haiku-4.5`, `google/gemini-3.8-flash`), because the original
models are no longer all available. The templates were rebuilt from
Supplementary Table S1. The run covered all three prompt conditions with three
replicates each, and it is complete: 5,180 of 5,184 responses parse.

Four facts constrain how the result can be reported:

1. **The negative result replicates under the primary definition.** In the
   `hidden_label_primary` condition, no dimension reaches ICC(1,1) 0.75
   (maximum 0.731, completeness).
2. **The margin does not replicate.** The upper 95% bounds for completeness
   (0.791) and audit usefulness (0.765) exceed 0.75. The original cohort's
   largest upper bound was 0.695.
3. **The threshold is crossed in secondary views.** Under the alternative
   rubric, completeness reaches 0.753. Under the pipeline's default pooling,
   which averages each case x judge over every condition and replicate,
   completeness (0.839) and audit usefulness (0.820) exceed 0.75. Averaging
   nine responses suppresses response noise and inflates the ICC.
4. **The ADR-0016 gradient replicates only in part.** Completeness and semantic
   plausibility stay among the higher-agreement dimensions and clarity stays
   the lowest, but audit usefulness, which ADR-0016 groups with the
   stakeholder-dependent low-agreement dimensions, becomes one of the
   highest-agreement dimensions (0.699). Actionability falls to about zero
   through a floor effect: almost every score is 1.

Recovering the cases also showed that the manuscripts misdescribe the sample.
The sample is 192 single explanations: 96 from EXP2 on Adult and 96 from EXP3
on German Credit and Breast Cancer, across four model families and four
explainers. It is not "147 paired SHAP/LIME outputs"; 147 is the original
cohort's complete-case subset for the ICC.

---

## Decision

1. **Framing.** Cohort 2 is reported as a **replication with a second judge
   panel on the same cases**, not as a reproduction and not as a replacement.
   The original cohort's values stay as the primary published table. Cohort 2
   is reported beside them.
2. **Primary definition.** The ICC(1,1) of the `hidden_label_primary`
   condition is the primary reliability estimate, as Supplementary Table S1
   states. The pooled estimate and the per-condition estimates are reported as
   sensitivity analyses, with the pooling stated.
3. **The confirmatory-use decision is unchanged.** No dimension supports
   confirmatory LLM-judge use: the primary estimate is below 0.75 in both
   cohorts, and crossing the threshold in secondary views depends on rubric
   wording and aggregation. The disagreement across panels is itself evidence
   against confirmatory use.
4. **The gradient is reported as partially replicated.** The ADR-0016
   interpretation, that higher agreement is consistent with verifiable
   referents, holds for completeness, semantic plausibility and clarity, and
   is not supported for audit usefulness in cohort 2. It remains
   hypothesis-generating. No causal account is offered for the change in audit
   usefulness.
5. **Sample description.** Every site that describes the EXP4 sample states
   the 192 single-explanation cases and their composition, and presents 147 as
   the original cohort's complete-case subset.
6. **Traceability.** Every cohort 2 number printed in a manuscript is
   registered in `pub/claim_registry.toml` against
   `outputs/analysis/exp4_cohort2/`, through the `exp4c2` and
   `exp4c2_shift_maxabs` resolvers.

## Amendment to ADR-0016

ADR-0016's compliance rule, "every thesis site that summarizes the dimension
gradient must also preserve the statement that all ICC(1,1) values are below
0.75", is replaced by:

> Every site that summarizes the dimension gradient must preserve the
> statement that **the primary-condition ICC(1,1) is below 0.75 on every
> dimension in both cohorts**. A site that reports a secondary view above
> 0.75 must name the view (alternative rubric or pooled over conditions) in
> the same sentence.

The rest of ADR-0016 stands: two levels of reporting, non-causal "consistent
with" language, and no bounded operational use recommended from EXP4 alone.

---

## Alternatives Considered

### Replace the Original Cohort with Cohort 2

- **Pros:** Cohort 2 has raw data, complete cases (n=192) and current judges.
- **Cons:** Different judges, rebuilt templates; it would silently change every
  published EXP4 number.
- **Why rejected:** The original values are what was measured and published;
  the new cohort adds evidence, it does not overwrite it.

### Report Only the Pooled View

- **Pros:** It is what the analysis code computes by default.
- **Cons:** It averages away response noise and crosses 0.75 on two dimensions,
  reversing the conclusion by an aggregation choice the manuscripts never
  stated.
- **Why rejected:** Supplementary Table S1 defines the primary estimate on
  `hidden_label`; the pooled view is reported as sensitivity.

### Omit Cohort 2 from the Manuscripts

- **Pros:** No manuscript change.
- **Cons:** Leaves a known non-robust margin claim and a wrong sample
  description in place.
- **Why rejected:** The replication materially qualifies published claims.

---

## Consequences

### Positive

- The negative EXP4 result now rests on two judge panels.
- Panel dependence and rubric sensitivity become reportable findings.
- The sample description is corrected everywhere.

### Negative

- The original "largest upper bound 0.695" margin argument must be qualified.
- More numbers to register and keep in sync across three documents.

### Neutral

- Original EXP4 aggregates, registry values and RCA-002 guards are unchanged.
