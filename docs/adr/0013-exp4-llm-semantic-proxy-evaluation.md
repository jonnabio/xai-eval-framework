# 13. EXP4 as LLM-Based Semantic Proxy Evaluation

Date: 2026-04-27
Status: Proposed

## Context

EXP1, EXP2, and EXP3 now provide a coherent technical evidence stack:

- EXP1 supports calibration and reproducibility.
- EXP2 supports the primary confirmatory benchmark on UCI Adult Income.
- EXP3 supports compact external tabular validation on Breast Cancer and German
  Credit.

The remaining thesis-level evidence gap is semantic and user-facing. The
existing benchmark is functionally grounded: it measures fidelity, stability,
sparsity, faithfulness gap, and runtime, but it does not directly measure
clarity, comprehensibility, audit usefulness, or semantic plausibility.

A full human-centered study would provide the strongest validation, but it is a
larger undertaking and requires recruitment, protocol review, annotation
management, and agreement analysis. The project therefore needs an intermediate
experiment that can extend the thesis framework toward semantic evaluation while
preserving reproducibility and bounded claims.

## Decision

Define EXP4 as an LLM-based semantic proxy evaluation experiment.

EXP4 will use LLMs as rubric-based judges over selected explanation artifacts
from EXP2 and EXP3. It will score explanation cases on semantic dimensions such
as clarity, completeness, concision, semantic plausibility, audit usefulness,
actionability, and overall explanation quality.

EXP4 will explicitly not claim direct human validation.

## Consequences

### Positive

- Adds a missing semantic evaluation layer to the thesis architecture.
- Reuses completed EXP2/EXP3 artifacts instead of launching a new predictive
  benchmark.
- Creates a reproducible prompt/rubric/score artifact trail.
- Enables alignment analysis between technical metrics and semantic proxy
  scores.
- Prepares the ground for later human-centered validation by refining cases,
  rubrics, and expected disagreement modes.

### Negative

- LLM judgments may contain position bias, verbosity bias, method-label bias, or
  prompt sensitivity.
- LLM scores cannot be interpreted as human trust, comprehension, or real-world
  usefulness.
- Model versions and provider behavior may change over time, so raw prompts,
  raw responses, and dated model identifiers must be retained.
- The thesis must maintain a strict distinction between proxy semantic evidence
  and human-centered evidence.

## Required Controls

EXP4 must include:

- frozen prompt and rubric versions;
- raw prompt and raw response persistence;
- parsed score persistence with parse-failure logs;
- repeated judgments for reliability analysis;
- method-label blinding where possible;
- explanation-length tracking;
- at least one robustness condition for prompt or judge sensitivity.

## Follow-Up

- Implement the EXP4 case sampler.
- Freeze the rubric and JSON output schema.
- Run a small dry run before full execution.
- Document result semantics under
  `docs/results/exp4_llm_evaluation/README.md`.
- Keep human-centered validation as a separate future experiment unless the
  thesis scope is explicitly revised.
