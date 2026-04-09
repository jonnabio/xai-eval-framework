# Paper C Scope and Validity Notes

This note keeps repository-specific caveats for Paper C in one place so the manuscript can stay focused on the survey argument.

## Identity

Paper C in the current thesis roadmap is the survey/taxonomy paper on XAI evaluation metrics.

- It is **not** the older robustness-scaling alternate concept in `docs/reports/paper_c_robustness_scaling_plan.md`.
- Its thesis role is to connect Paper B's quantitative benchmark layer with Paper A's semantic-evaluator validation layer.

## Current Review Corpus

- Corpus freeze date: `2026-04-05`
- Upstream matrix source: `docs/reports/literature_review_methodology_matrix.md`
- Upstream rows reviewed: `25`
- Duplicate rows removed during Paper C cleaning: `1`
- Unique coded papers: `24`
- Cleaned corpus file: `docs/reports/paper_c/paper_c_review_corpus.csv`
- Generated descriptive summary: `docs/reports/paper_c/paper_c_review_summary.md`

The current coding pass is a thesis-facing, single-reviewer synthesis pass. It is traceable and structured, but it is not a full inter-rater systematic review workflow.

## Claim Discipline

Paper C can currently support:

- construct-level arguments about why XAI evaluation fragments across different targets, evidence sources, and quality properties;
- thesis-level justification for layered evaluation;
- evidence-backed reporting that proxy-heavy measurement dominates the present coded corpus.

Paper C should not currently claim:

- exhaustive coverage of all XAI evaluation literature;
- pooled effect-size conclusions across studies;
- completed validation of semantic evaluators against human judgments.

## Current Thesis Status Link

At the current repository snapshot, the broader thesis already contains:

- quantitative metric infrastructure;
- LLM-evaluation prompts and orchestration;
- stratified semantic-evaluation sampling;
- a human-annotation interface ready for collection.

What remains incomplete for the Paper A layer is the confirmatory human-validation step itself:

- human data collection is still pending;
- agreement analysis is still stubbed in thesis status notes.

That means Paper C should position semantic evaluation as necessary and promising, but still instrument-like rather than fully validated.
