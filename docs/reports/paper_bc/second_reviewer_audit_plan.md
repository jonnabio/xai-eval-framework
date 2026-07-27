# Second-Reviewer Audit Plan

## Purpose

This document defines an independent human second-reviewer audit for the
Paper BC taxonomy. The audit is intended as a stress test of taxonomy
reproducibility and reviewer-response preparation, conducted by a second
human reviewer rather than the primary author.

## Scope

- Manuscript: `docs/reports/paper_bc/paper_bc_jmlr.tex`
- Review component: four-axis XAI evaluation taxonomy
- Available source basis: Paper BC bibliography and the repository literature
  matrix
- Audit size: 16 papers
- Sampling strategy: stratified subset across the thematic clusters reported
  in the manuscript
- Data collection: annotations submitted through the project's
  human-evaluation dashboard

## Stratified Sample

The audited subset covers:

- 4 faithfulness/robustness records
- 4 human-grounded records
- 3 taxonomy/survey records
- 2 benchmark/toolkit records
- 2 LLM-judge records
- 1 counterfactual/recourse record

## Coding Axes

Each record is compared on:

- inclusion decision
- evaluation target
- evidence source
- quality property
- task context

The taxonomy axes are treated as multi-label except the inclusion decision.

## Agreement Metrics

- Inclusion decision: percent agreement; Cohen's kappa only if both positive
  and negative inclusion decisions are present
- Multi-label axes: exact percent agreement and Jaccard similarity
- Overall summary: mean axis-level Jaccard and mean exact agreement

## Interpretation

The audit is deliberately conservative: semantically adjacent but
non-identical labels are counted as disagreements unless they match exactly.
This makes the stress test useful for finding ambiguous construct boundaries.

## Reporting Constraint

This audit covers a stratified subset (16/48 papers), not the full coded
corpus. It should be described in the manuscript as an independent
second-reviewer audit of that subset, not as a full-corpus inter-rater
reliability study.
