# EXP4 Rubric V1

## Scoring Scale

Use a 1-5 ordinal score for each dimension:

- 1: very poor;
- 2: weak;
- 3: adequate;
- 4: strong;
- 5: excellent.

The evaluator must score only the explanation shown in the case. It must not
infer hidden facts, assume clinical or financial correctness, or use method
reputation as evidence.

## Dimensions

### Clarity

Does the explanation communicate its main point in a way that a technically
informed reader can understand?

- 1: confusing or unintelligible;
- 3: understandable with effort;
- 5: immediately clear and well organized.

### Completeness

Does the explanation provide enough information to understand the model
decision at the local instance level?

- 1: omits essential information;
- 3: covers the main decision factors but leaves gaps;
- 5: covers the relevant decision factors without major omissions.

### Concision

Is the explanation compact relative to the amount of useful information it
provides?

- 1: excessively verbose or cluttered;
- 3: acceptable but could be tighter;
- 5: concise without losing necessary information.

### Semantic Plausibility

Does the explanation make domain sense given the provided case context?

- 1: implausible or contradictory;
- 3: broadly plausible with uncertainty;
- 5: strongly plausible and coherent with the provided context.

### Audit Usefulness

Would the explanation help an auditor inspect why the model made this decision?

- 1: not useful for audit;
- 3: somewhat useful but incomplete;
- 5: highly useful for audit or model-behavior inspection.

### Actionability or Decision Support

Does the explanation support a meaningful next step, intervention, or decision
review?

- 1: no actionable or decision-support value;
- 3: limited or indirect decision-support value;
- 5: clear support for review, recourse, or decision-making.

### Overall Explanation Quality

Considering all dimensions, how good is the explanation as a semantic account
of the model decision?

- 1: very poor;
- 3: adequate;
- 5: excellent.

## Required Rationale

For each dimension, provide one concise rationale sentence. The rationale should
refer to observable properties of the explanation, not to assumptions about the
explainer family.
