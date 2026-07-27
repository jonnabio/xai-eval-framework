# Simulated Second-Reviewer Audit Summary

## Status

This is an LLM-assisted simulated audit for internal revision planning. It is
not an independent human second-reviewer audit.

## Sample

- Records audited: 16
- Sampling frame: Paper BC bibliography plus repository literature matrix
- Sampling approach: stratified across manuscript clusters
- Clusters represented:
  - faithfulness/robustness: 4
  - human-grounded: 4
  - taxonomy/survey: 3
  - benchmark/toolkit: 2
  - LLM-judge: 2
  - counterfactual/recourse: 1

## Agreement Results

| Audit item | Exact agreement | Mean Jaccard | Interpretation |
| --- | ---: | ---: | --- |
| Inclusion decision | 100.0% | n/a | All simulated records were retained as includable. Cohen's kappa is not estimable because the sample contains included records only. |
| Evaluation target | 62.5% | 0.802 | Generally stable, but conceptual papers blur target boundaries. |
| Evidence source | 56.2% | 0.771 | Moderate ambiguity around taxonomy, human, end-user, and normative evidence labels. |
| Quality property | 25.0% | 0.657 | Weakest axis; adjacent labels such as stability/robustness, usefulness/plausibility, and sensitivity/stability require clearer codebook rules. |
| Task context | 81.2% | 0.906 | Strongest axis; disagreements mostly involve broad versus specific context labels. |

Overall mean axis-level Jaccard: 0.784.

Records requiring adjudication: 12/16.

## Main Codebook Issues Found

1. Sensitivity, robustness, and stability need explicit nesting rules.
2. Human-grounded evidence should distinguish end-user task evidence,
   expert-human review, and conceptual human-centered taxonomy claims.
3. Quality-property labels need a controlled vocabulary so broad labels such
   as usefulness, plausibility, interpretability, and semantic alignment do not
   drift across papers.
4. Normative/legal reasoning in counterfactual papers should be coded either
   as an evidence-source subtype or as task context, but not inconsistently as
   both.
5. Conceptual taxonomy papers need a rule for whether they target the
   taxonomy itself, the explainer method, model behavior, or all three.

## Recommended Manuscript Use

Use this simulation to justify codebook refinement and claim-discipline
changes. Do not use it to claim validated inter-rater reliability unless a
human second reviewer independently repeats the audit.
