# Phase 2 Findings

This file is the evolving synthesis layer for the Chapter 2 literature review.
It should contain conclusions drawn from the literature matrix, not raw paper
summaries.

## Current Baseline

- `thesis/03-capitulo-2-fundamentos.qmd` currently has 8,413 words after the
  polish pass tightened Spanish orthography, added targeted citation anchors,
  and preserved the final Phase 2 metric taxonomy, FOM-7 synthesis, and
  method-vs-evaluation-construct matrix.
- Target length is 8,000-12,000 words.
- The current chapter already introduces XAI, black-box models, basic
  interpretability/explainability distinctions, and evaluation criteria.
- The chapter now meets the 8,000-12,000 word target. The polish pass also made
  Chapter 3 explicitly reuse the FOM-7 constructs introduced here: fidelity,
  stability, robustness, complexity, cost, artifact qualification, statistical
  admissibility, and claim traceability.

## Initial Synthesis

### Finding F1: The Review Needs To Move From Definitions To Argument

The current chapter defines important terms, but it does not yet build a full
doctoral argument. The expanded chapter should show that XAI method development
has produced mature explanation families while evaluation practice remains
fragmented across incompatible constructs, metrics, and evidence sources.

### Finding F2: FOM-7 Should Be Positioned As Protocol Governance

The likely contribution gap is not "there are no XAI metrics" and not "there are
no XAI toolkits." Quantus and OpenXAI already address parts of the tooling and
benchmarking problem. The sharper thesis claim is that FOM-7 connects:

- experimental design freeze,
- artifact qualification,
- harmonized metric tables,
- statistical admissibility,
- reproducibility profiling,
- claim traceability.

This gives FOM-7 a defensible role as protocol governance rather than another
metric library.

### Finding F3: The Four Methods Must Be Treated As Different Explanation Objects

LIME, SHAP, Anchors, and DiCE should not be presented as interchangeable ways to
produce the same kind of explanation. They correspond to different explanation
families:

- LIME: local surrogate approximation,
- SHAP: additive attribution grounded in Shapley values,
- Anchors: high-precision rule explanations with coverage constraints,
- DiCE: counterfactual alternatives intended for actionability.

This distinction is essential for interpreting why some metrics favor some
methods and why fidelity-style metrics are not equally natural for all methods.

### Finding F4: Conceptual Distinctions Need To Protect Against Overclaiming

The expanded review should explicitly separate:

- interpretability and explainability,
- transparency and explanation,
- fidelity and faithfulness,
- plausibility and correctness,
- robustness and stability,
- user usefulness and explanation truth.

These distinctions will help the thesis avoid treating proxy metrics as direct
evidence of semantic truth or human utility.

## Next Synthesis Tasks

1. Verify the foundational sources listed in `xai_literature_matrix.md`.
2. Add 2022-2026 sources for human-centered XAI evaluation and metric taxonomy.
3. Convert each search cluster into one provisional Chapter 2 subsection.
4. Apply a rigor-review pass to every claim before moving text into the thesis.
