# Paper D — are explanations less reliable when the model is wrong?

**Working title:** *Are explanations less reliable when the model is wrong? Post-hoc
explanation quality on misclassified instances*

**Target:** *Tecnología en Marcha* (Editorial Tecnológica de Costa Rica), special issue on
Artificial Intelligence. ESCI, SciELO, DOAJ; no fees. **Deadline: 15 October 2026**, by email
to revistatm@tec.ac.cr. Author target: **12 pages in Word**, including references; English.

**Status (2026-10-03):** analysis plan written and committed before any result was computed
(`ANALYSIS_PLAN.md`). Manuscript skeleton in place. No results yet.

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
| `ANALYSIS_PLAN.md` | Pre-specified questions, data, statistics, exclusions, overlap guard |
| `paper_d.tex` | Manuscript skeleton (journal page setup; sections to be written) |
| `ieee.csl`, `reference_default.docx` | Used by `scripts/pubs/build_paper_d.py` to make the Word file |

To be created when the analysis runs: `references.bib`, `figures/`, `submission/`,
`scripts/pubs/paper_d_analysis.py`, `scripts/generate_paper_d_figures.py` and
`outputs/analysis/paper_d/`.

## Build (once the draft exists)

```bash
python scripts/pubs/paper_d_analysis.py        # results -> outputs/analysis/paper_d/
python scripts/generate_paper_d_figures.py     # figures (.pdf, .png, .tiff)
python scripts/pubs/build_paper_d.py           # blind/full PDF and Word, figure uploads
python scripts/pubs/verify_claims.py           # every printed number re-derives
```

Measure the length in Word itself: the PDF is only a proxy.

## Plan to the deadline

| Date | Step |
|---|---|
| 3 Oct | Analysis plan and skeleton (done) |
| 4–5 Oct | Analysis script and results; register numbers |
| 6–9 Oct | Writing; references (verified, approved by the author) |
| 10 Oct | Figures; Word build; length check |
| 11 Oct | Scientific-rigor review; fixes |
| 12 Oct | Author items: ORCID, profession, Spanish read, reference approval |
| 13 Oct | Submit (two days of margin) |
