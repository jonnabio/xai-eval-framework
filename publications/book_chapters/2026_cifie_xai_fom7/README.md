# CIFIE XAI FOM-7 Book Chapter

This folder contains the planning, source materials, manuscript drafts, figures, tables, references, compliance artifacts, and final submission package for the CIFIE collective book chapter derived from the doctoral research project on model-agnostic evaluation frameworks for Explainable AI.

## Scope

- Chapter language: Spanish.
- Writing style: highly scientific, readable, and primarily impersonal.
- Technical level: high, with concepts introduced before formal detail.
- Central argument: explanations become defensible evidence only when purpose,
  audience, construct, evaluation, traceability, and inferential scope are aligned.
- Central contribution: FOM-7 as a reproducible protocol for multi-metric benchmarking of post-hoc, model-agnostic explanation methods.
- Methods discussed: LIME, SHAP, Anchors, and DiCE.
- Application areas: health, finance, cybersecurity, autonomous systems, and
  foundation or language models.
- Empirical results: synchronized from the dissertation and the registered evidence
  substrate; unpublished Paper B+C results are excluded.
- Relationship to thesis: derived from and connected to the doctoral dissertation, but managed as an independent publication artifact.
- Reference style: APA 7.
- Final format: Word, aligned with compatible thesis presentation standards.

## Build

From the repository root, on a committed state of `chapter/cifie-sync-2026-09`:

1. Figures (only after a data or figure change):
   `python scripts/generate_cifie_chapter_figures.py` (Figure 2) and
   `python scripts/generate_spanish_thesis_figures.py` (the other five, copied
   from `thesis/assets/figures/`). Both need `matplotlib` and `pandas`.
2. Word document: `python scripts/build_cifie_chapter.py [--out PATH]`. Needs
   pandoc (bundled with Quarto), `python-docx` and `Pillow`.
3. Inspect the result on a Microsoft Word render, not only by exit code.

Verified 2026-09-29: a build from a clean checkout of `225419856` reproduced the
committed `drafts/v3_editorial_review/cifie_xai_fom7_2026-09-29_formatted.docx`
(same document, styles and media; only the creation timestamp and an empty header
differ), and both figure generators reproduced the figures' content.

## Authors

- Jonathan Herrera-Vásquez, Universidad Americana de Europa, ORCID: 0000-0002-7149-6635.
- Miguel Herrero-Uceda, Universidad Americana de Europa.

## Structure

- `manuscript/`: chapter outline, editorial design sheet, section files, and assembled manuscript.
- `editorial/`: publisher requirements, template notes, and editorial correspondence.
- `sources/`: source materials derived from the dissertation, symposium presentation, and related paper material.
- `figures/`: editable and exported figure assets, tracked through the figure registry.
- `tables/`: working tables for methods, metrics, FOM-7 gates, and result summaries.
- `references/`: BibTeX entries, APA 7 reference tracking, and citation audit.
- `compliance/`: author checklist, AI-use declaration, rubric self-assessment, and submission packet notes.
- `drafts/`: versioned working drafts from planning through submission.
- `final/submission_package/`: final files prepared for editorial submission.
