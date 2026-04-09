# Paper C Prototype Instructions

These instructions define how to create the new Paper C prototype by following the same repository layout already used for Paper A and Paper B.

Paper C in this document means the survey/taxonomy paper from the current merged PhD roadmap:

- working role: conceptual review paper that maps XAI evaluation metrics from quantitative fidelity-style metrics toward semantic evaluation;
- thesis function: framing and justification paper for Papers A and B;
- important distinction: this is **not** the same concept as the older `docs/reports/paper_c_robustness_scaling_plan.md`, which should be preserved as a separate alternate paper idea.

## 1. Mirror the Existing Paper Folder Pattern

Paper A and Paper B both use a dedicated folder under `docs/reports/` with local prototype assets. Paper C should follow the same structure:

```text
docs/reports/paper_c/
  jmlr2e.sty
  paper_c_prototype.md
  paper_c_prototype_jmlr.tex
  paper_c_jmlr_track_positioning.md        # optional companion note
  paper_c_scope_and_validity_notes.md      # optional companion note
  figures/                                 # optional, add when needed
```

Generated build artifacts should appear only after compiling:

```text
paper_c_prototype_jmlr.pdf
paper_c_prototype_jmlr.aux
paper_c_prototype_jmlr.out
paper_c_prototype_jmlr.log
paper_c_prototype_jmlr.fls
paper_c_prototype_jmlr.fdb_latexmk
```

## 2. Reuse the Same A/B Working Pattern

Use the same workflow already implied by Papers A and B:

1. Draft the narrative in `paper_c_prototype.md`.
2. Port or mirror that content into `paper_c_prototype_jmlr.tex`.
3. Keep the LaTeX file close in structure to the Markdown prototype.
4. Compile locally to produce the PDF and build artifacts in the same folder.
5. Add companion notes only if they help keep the main draft focused.

Paper A shows the pattern of using companion notes for scope/validity and venue positioning.
Paper B shows the pattern of keeping a Markdown narrative closely aligned with the JMLR `.tex` file.
Paper C should combine both strengths.

## 3. Repo Sources to Use While Drafting

Build the prototype from existing materials already in the repo instead of starting from scratch.

Primary inputs:

- `docs/reports/literature_review_methodology_matrix.md`
- `docs/reports/jmlr_format_compliance.md`
- `docs/reports/paper_a/paper_a_prototype_jmlr.tex`
- `docs/reports/paper_b/paper_b_prototype_jmlr.tex`
- `docs/reports/paper_a/paper_a_validity_and_reporting_caveats.md`
- `docs/reports/paper_a/paper_a_jmlr_track_positioning.md`
- `docs/thesis/objectives_results.md`

Secondary inputs, only where useful:

- `docs/reports/paper_c_robustness_scaling_plan.md`
- `docs/thesis/interpretation.tex`
- `docs/thesis/chapter_5_results.tex`

Interpretation rule:

- use the literature matrix as the main seed for the survey taxonomy;
- use Papers A and B mainly for structure, tone, contribution framing, and section ordering;
- do not let the older robustness/scaling Paper C note redefine this new Paper C.

## 4. Recommended Identity for Paper C

Use a title and scope that clearly differ from Papers A and B.

Recommended working title:

`From Fidelity to Semantics: A Taxonomy and Survey of Evaluation Metrics for Model-Agnostic Explainability`

Recommended paper type:

- narrative survey with explicit taxonomy;
- light systematic protocol if search/exclusion metadata is ready;
- conceptual bridge paper that motivates why semantic evaluation is needed but does not depend on finishing Paper A experiments first.

Recommended non-goals:

- do not turn this into another benchmark paper;
- do not duplicate Paper A's human-vs-LLM validation as the paper's main contribution;
- do not make this an architecture/software paper.

## 5. Create the Prototype Files in This Order

### Step 1: Create `paper_c_prototype.md`

Use it as the full prose draft and content planning document.

Minimum sections:

1. Title
2. Abstract
3. Keywords
4. Introduction
5. Background and Definitions
6. Review Method or Literature Selection Protocol
7. Taxonomy of XAI Evaluation Metrics
8. Comparative Synthesis and Open Gaps
9. Implications for the Thesis Framework
10. Limitations
11. Conclusion
12. References placeholder or citation key list

### Step 2: Create `paper_c_prototype_jmlr.tex`

Base the front matter on the same pattern used by:

- `docs/reports/paper_a/paper_a_prototype_jmlr.tex`
- `docs/reports/paper_b/paper_b_prototype_jmlr.tex`

Use the same package family unless a clear Paper C need appears:

- `jmlr2e`
- `amsmath`
- `microtype`
- `booktabs`
- `tabularx`
- `array`
- `enumitem`
- `lastpage`

Suggested front-matter placeholders:

- paper id: `PAPER-C-0001`
- short heading: short survey title
- submitted month/year: current drafting month

### Step 3: Add companion notes only if needed

Optional files:

- `paper_c_jmlr_track_positioning.md`
- `paper_c_scope_and_validity_notes.md`

Use these only to keep the main manuscript from getting overloaded with venue-specific or caveat-heavy text.

## 6. Section-by-Section Layout for the Prototype

This section is the main instruction set for content development.

### Abstract

Follow the A/B style:

- start with the field-level problem;
- state the gap in current XAI evaluation;
- say what the paper contributes;
- end with the practical value for benchmarking and semantic evaluation.

The abstract should answer:

- why current XAI evaluation is fragmented;
- what taxonomy or synthesis the paper provides;
- how this positions semantic evaluation;
- why this matters for the broader thesis program.

### Introduction

Mirror the rhetorical pattern of Papers A and B:

1. state the practical problem;
2. describe the literature gap;
3. position this paper relative to the larger research program;
4. close with contributions and scope.

Recommended introduction blocks:

- fragmentation of XAI evaluation terminology and metrics;
- mismatch between proxy metrics and explanation usefulness;
- lack of unified placement for semantic evaluation;
- need for a taxonomy that connects fidelity, stability, sparsity, plausibility, human judgment, and LLM-based judging.

End the introduction with:

- a bullet or enumerated contribution list;
- a scope paragraph stating that the paper focuses on model-agnostic post-hoc explainability evaluation.

### Background and Definitions

Use this section to stabilize terminology before the taxonomy:

- intrinsic vs post-hoc explainability;
- local vs global explanations;
- model-specific vs model-agnostic methods;
- explanation quality vs system quality vs user-perceived quality;
- semantic evaluation vs faithfulness proxies.

Keep this section compact. It should support the taxonomy, not become a separate survey inside the survey.

### Review Method / Literature Selection Protocol

Paper C should be more explicit about source selection than Papers A and B because it is a survey paper.

Minimum prototype content:

- the review objective;
- source pools already used in the thesis;
- inclusion logic;
- exclusion logic;
- how papers were coded into the taxonomy.

If a full PRISMA-style search is not yet frozen, the prototype may use a lighter "structured narrative review" framing, but it must still describe:

- what was searched;
- what counted as relevant;
- how thematic clusters were formed.

The existing `docs/reports/literature_review_methodology_matrix.md` should be the starting coding table.

### Taxonomy of XAI Evaluation Metrics

This should be the core section of Paper C.

Organize the taxonomy across a few consistent axes instead of one long list.

Recommended axes:

1. **Evaluation target**
   - explanation artifact
   - explainer method
   - model behavior
   - user/task outcome

2. **Evidence source**
   - perturbation/proxy metrics
   - synthetic ground truth or benchmarks
   - human experts
   - end users
   - LLM judges

3. **Quality property**
   - fidelity
   - stability/robustness
   - sparsity/parsimony
   - plausibility
   - counterfactual quality / recourse
   - semantic alignment / causal alignment

4. **Task/modality context**
   - tabular
   - image
   - text
   - time series
   - graph or other specialized domains

Recommended core table:

- one synthesis table that maps metric families to definitions, assumptions, strengths, weaknesses, and failure modes.

Recommended core figure:

- one conceptual diagram that places proxy metrics, human judgment, and semantic evaluation on the same continuum.

### Comparative Synthesis and Open Gaps

This section should move beyond taxonomy and produce the paper's argument.

Recommended subsections:

- where current metrics overlap or partially duplicate one another;
- where current metrics fail to capture explanation meaning;
- when proxy metrics are sufficient;
- when human or semantic evaluation becomes necessary;
- why LLM-based semantic evaluation is promising but risky.

This is where Paper C should naturally motivate Paper A without becoming Paper A.

### Implications for the Thesis Framework

Add one dedicated section that connects the survey back to the dissertation.

Recommended outputs:

- justify the metric stack used in Paper B;
- justify the need for semantic evaluator validation in Paper A;
- propose a minimal evaluation stack for the framework;
- identify which evaluation layers are confirmatory versus exploratory.

This section is important because it turns the survey into a thesis-integrated paper rather than a disconnected literature summary.

### Limitations

Paper C should explicitly state:

- survey scope boundaries;
- database and paper-set limitations;
- possible bias toward model-agnostic post-hoc XAI;
- limited direct user-study evidence in parts of the literature;
- unresolved external validity of LLM judges.

### Conclusion

Follow the A/B style:

- restate the paper's organizing contribution;
- summarize the main conceptual gap;
- end with how the taxonomy informs future empirical work.

## 7. Layout and Tone Rules Borrowed from Papers A and B

Paper C should preserve the same manuscript style cues already present in A/B:

- concise, high-density abstract;
- strong problem-setting subsection near the start;
- explicit "related work and novelty delta" logic, even in a survey;
- enumerated contributions;
- clear scope boundaries;
- tables used for synthesis, not decoration;
- claim language that stays proportional to available evidence.

Avoid:

- overly generic survey prose;
- turning the taxonomy into a glossary only;
- promising full systematic-review completeness if the search protocol is not yet frozen;
- repeating Paper A or B results in detail.

## 8. Minimal JMLR Prototype Metadata

For consistency with the existing paper prototypes, start from a header like this:

```tex
\documentclass[twoside,11pt]{article}

\usepackage{jmlr2e}
\usepackage{amsmath}
\usepackage{microtype}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{enumitem}
\usepackage{lastpage}

\jmlrheading{0}{2026}{1-\pageref{LastPage}}{Submitted 4/2026}{Preprint}{PAPER-C-0001}{Jonathan Herrera-Vasquez}
\ShortHeadings{From Fidelity to Semantics}{Herrera-Vasquez}
\firstpageno{1}
```

This does not lock the final venue. It only keeps the prototype format consistent with Papers A and B.

## 9. Suggested Definition of Done for the Prototype

Consider the prototype complete when all of the following are true:

- `docs/reports/paper_c/` exists and matches the A/B folder pattern;
- `paper_c_prototype.md` contains a complete narrative draft;
- `paper_c_prototype_jmlr.tex` contains a working JMLR-formatted manuscript draft;
- the manuscript includes at least one taxonomy table;
- the manuscript includes one section explicitly connecting the survey to Papers A and B;
- the PDF compiles locally;
- the older `paper_c_robustness_scaling_plan.md` remains untouched as a different paper concept.

## 10. Build Command

From the repo root:

```bash
cd docs/reports/paper_c
latexmk -pdf paper_c_prototype_jmlr.tex
```

If `latexmk` is unavailable, fall back to:

```bash
cd docs/reports/paper_c
pdflatex paper_c_prototype_jmlr.tex
pdflatex paper_c_prototype_jmlr.tex
```

## 11. Recommended Next Action

After creating the two prototype files, fill these in first:

1. title, abstract, and introduction;
2. taxonomy table;
3. thesis-implications section;
4. review-method section;
5. conclusion and limitations.

That ordering matches the current repo practice: get the argument and structure stable first, then deepen the literature coverage and figure polish.
