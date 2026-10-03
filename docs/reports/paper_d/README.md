# Paper D — are explanations less reliable when the model is wrong?

**Working title:** *Are explanations less reliable when the model is wrong? Post-hoc
explanation quality on misclassified instances*

**Target:** *Tecnología en Marcha* (Editorial Tecnológica de Costa Rica), special issue on
Artificial Intelligence. ESCI, SciELO, DOAJ; no fees. **Deadline: 15 October 2026**, by email
to revistatm@tec.ac.cr. Author target: **12 pages in Word**, including references; English.

**Status (2026-10-03): first render done.** The analysis ran as planned (two deviations,
logged in `ANALYSIS_PLAN.md` §9). The manuscript, figures, Word file and separate TIFFs are in
`submission/`: 12 Word pages after iteration 1. Every printed number re-derives through
the claim registry. What remains before submission is in `IMPROVEMENT_ANALYSIS.md`. Lane: branch
`paper-d/tecnologia-en-marcha`.

**History:** this folder first held a different Paper D, a case study of the claim registry.
The author dropped it on 2026-10-03 because it drifted from the XAI research line; it is
preserved at git tag `paper-d-registry-draft-2026-10-03`. The companion question "Do
explainers agree on which features matter?" is Paper E (`docs/reports/paper_e/`), to be
developed after this submission.

## Contribution

A re-analysis of the existing benchmark at instance level. It compares explanation quality
(fidelity, stability, faithfulness gap, sparsity) between correctly and incorrectly
classified instances for SHAP, LIME, Anchors and DiCE across five model families, with a
control for the prediction margin and an external check on German Credit. No new experiment
is run.

## Relation to Papers A and B+C

The runs are the same cohort as Paper A (published, RIMI) and Paper B+C (under review,
*Inteligencia Artificial*). Paper D reports none of their results: only within-run contrasts
between correct and misclassified instances, which neither paper computes. The provenance is
stated in the paper. This is enforced by the claim registry: `paper_d.tex` is under
`[exclusivity]` and `[coverage]` in `pub/claim_registry.toml`.

## Journal requirements (author guide, checked 2026-10-03)

| Requirement | Journal rule |
|---|---|
| Originality | Original, unpublished, not in another process at the same time |
| Structure | Title, abstract, keywords in English **and** Spanish; introduction; materials and methods; results; conclusions and/or recommendations; references; acknowledgments |
| Length | 5–15 pages, 8.5 × 11 in |
| File | Microsoft Word; one column; 1.5 line spacing; Times 12 pt |
| Authors | Full name with both surnames, profession, email, workplace, country, ORCID |
| Abstract | Spanish and English, at most 250 words each |
| Images | In the document and as separate .jpg/.tiff/.eps/.psd/.ai files; 300 ppi |
| Equations | Word equation editor or MathType |
| References | IEEE |
| Review | Double-blind |
| AI policy | No AI-plagiarised ideas or autonomously AI-written papers; assistance disclosed |

## Files

| Path | What it is |
|---|---|
| `ANALYSIS_PLAN.md` | Pre-specified questions, data, statistics, exclusions, overlap guard; §9 deviations |
| `paper_d_template.tex` | **The manuscript source.** Numbers are placeholders filled from the analysis |
| `paper_d.tex` | Generated from the template by `render_paper_d.py`. Do not edit |
| `references.bib` | IEEE references; `NEW` entries await the author's check |
| `figures/` | fig1–3 as .pdf (LaTeX), .png (Word) and .tiff (upload, 300 ppi) |
| `submission/` | `paper_d_blind.{pdf,docx}` to send; `paper_d_full.*` with author data; `Figure1-3.tiff` |
| `IMPROVEMENT_ANALYSIS.md` | Review of the first render and the plan to submission |
| `ieee.csl`, `reference_default.docx` | Used to make the Word file |

Code: `scripts/pubs/paper_d_analysis.py`, `scripts/generate_paper_d_figures.py`,
`scripts/pubs/render_paper_d.py`, `scripts/pubs/build_paper_d.py`. Results:
`outputs/analysis/paper_d/` (`superseded_rq4_all_runs.csv` is the RQ4 output before
deviation 1, kept for the record).

## Build

```bash
python scripts/pubs/paper_d_analysis.py        # results -> outputs/analysis/paper_d/
python scripts/generate_paper_d_figures.py     # figures (.pdf, .png, .tiff)
python scripts/pubs/render_paper_d.py          # template -> paper_d.tex + registry block
python scripts/pubs/build_paper_d.py           # blind/full PDF and Word, figure uploads
python scripts/pubs/verify_claims.py           # every printed number re-derives
python scripts/pubs/scan_shared_literals.py --paper-d --strict   # no Paper A/B+C number
```

The first two need SciPy, scikit-learn 1.7.1 and XGBoost. On this machine, Windows
Application Control blocks SciPy's DLL inside the project `.venv`, so the analysis ran in
a separate virtual environment (Python 3.13). Measure the length in Word itself: the PDF
is only a proxy.

## Plan to the deadline

| Date | Step |
|---|---|
| 3 Oct | Analysis plan and skeleton (done) |
| 3 Oct | Analysis, figures, first render, improvement analysis (done) |
| 4–5 Oct | Sensitivity checks S1, S5; text fixes; cut to 12 pages |
| 6–9 Oct | Writing; references (verified, approved by the author) |
| 10 Oct | Figures; Word build; length check |
| 11 Oct | Scientific-rigor review; fixes |
| 12 Oct | Author items: ORCID, profession, Spanish read, reference approval |
| 13 Oct | Submit (two days of margin) |
