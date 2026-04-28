# EXP4 Interpretation Note: Attribution Is Not Yet Explanation

## Purpose

This note records the interpretation issue raised during EXP4 review: many XAI
artifacts evaluated in EXP4 are closer to raw attribution lists than to
human-usable explanations.

The distinction matters because EXP4 does not ask whether an attribution vector
exists. It asks whether the resulting artifact is understandable, complete,
auditable, and actionable as an explanation.

## Concrete Example

An EXP4-normalized SHAP artifact can look like this:

```text
Explanation:
SHAP top local factors:
worst concave points: 0.42;
mean concavity: 0.31;
worst perimeter: 0.28;
worst radius: 0.21
```

This artifact gives a ranked list of influential features and numeric
contributions. It is useful as a compact technical signal, but it is not yet a
complete human explanation.

## What A Human Reviewer Can See

A human reviewer can infer that:

- the explanation is a local feature-importance list;
- the model relied on tumor geometry features;
- the listed features probably contributed to the prediction;
- the artifact is concise.

However, the reviewer cannot reliably infer:

- what the numbers mean on their scale;
- whether positive values push toward malignant, benign, high income, low
  income, approval, denial, or another class;
- what the actual feature values were for the instance;
- whether the feature values are unusually high or low;
- how the listed factors relate to domain knowledge;
- what an auditor should inspect next;
- what an affected person could change or review.

Therefore, the artifact is better described as an attribution output than as a
fully contextualized explanation.

## How The LLM Evaluator Handles This

The EXP4 LLM judge reads the artifact under a fixed rubric. It does not inspect
the underlying model internals and it does not decide whether the model
prediction is correct. It scores the artifact as an explanation.

For this type of SHAP list, the expected scoring pattern is:

| Dimension | Expected Pattern | Reason |
|---|---:|---|
| Clarity | Low to moderate | The list is readable, but the values are not explained |
| Completeness | Low | Feature values, direction, baseline, and context are missing |
| Concision | High | The artifact is short and compact |
| Semantic plausibility | Moderate to high | The breast-cancer features are domain-relevant |
| Audit usefulness | Low to moderate | It identifies factors, but does not support deep inspection |
| Actionability | Low | It provides no next step, recourse, or review guidance |
| Overall quality | Low to moderate | It is useful as attribution, weak as explanation |

This is the pattern observed in the OpenRouter pilot: concision and semantic
plausibility were higher than completeness, audit usefulness, and actionability.

## Stronger Explanation Form

A more human-usable explanation would preserve the attribution information but
add interpretation:

```text
The model predicted malignant primarily because the tumor has high values for
worst concave points, mean concavity, worst perimeter, and worst radius. These
features describe irregularity and size of the tumor boundary, which are
clinically associated with malignancy. The positive SHAP values indicate that
these features increased the model's malignant prediction for this instance.
```

This stronger form explains:

- the predicted class;
- the direction of contribution;
- the domain meaning of the features;
- why those features matter;
- how the raw attribution should be interpreted.

## Thesis Relevance

EXP4 operationalizes the gap between:

```text
feature attribution
```

and:

```text
usable explanation
```

Earlier experiments can show that a method has fidelity, stability, sparsity, or
faithfulness properties. EXP4 asks whether the output is also semantically
adequate for review. The pilot evidence suggests that many technical XAI outputs
are concise and plausible but incomplete as audit artifacts.

The thesis claim should therefore be framed as follows:

> Technical attribution quality is necessary but not sufficient for practical
> explainability. A multi-level evaluation framework must also assess semantic
> completeness, audit usefulness, and actionability.

This interpretation should guide future EXP4 reporting and any thesis language
that discusses LLM-based semantic evaluation.
