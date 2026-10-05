# Paper D — are explanations less reliable when the model is wrong?

**Working title:** *Are explanations less reliable when the model is wrong? Post-hoc
explanation quality on misclassified instances*

**Target:** *Tecnología en Marcha* (Editorial Tecnológica de Costa Rica), special issue on
Artificial Intelligence. ESCI, SciELO, DOAJ; no fees. **Deadline: 15 October 2026**, by email
to revistatm@tec.ac.cr (route confirmed by the author on 2026-10-03 from the special-issue
instructions; the journal's general instructions page names the website instead). The
instructions also ask for the author's telephone numbers, which go in the email and are not
kept in this public repository. Author target: **12 pages in Word**, including references; English.

**Status (2026-10-03): SUBMITTED.** The author sent the paper by email to
revistatm@tec.ac.cr on 2026-10-03 (blind and full Word files, three TIFF figures). The files
in `submission/` at commit `f8e88a6d7` are the ones sent; do not rebuild them unless the
journal asks for a revision. Earlier status: first render done. The analysis ran as planned (two deviations,
logged in `ANALYSIS_PLAN.md` §9). The manuscript, figures, Word file and separate TIFFs are in
`submission/`: 12 Word pages after iteration 1. Every printed number re-derives through
the claim registry. What remains before submission is in `IMPROVEMENT_ANALYSIS.md`. Paper D is
worked in the main folder, on branch `paper/d-tecnologia-en-marcha` (ADR-0021).

**History:** this folder first held a different Paper D, a case study of the claim registry.
The author dropped it on 2026-10-03 because it drifted from the XAI research line; it is
preserved at git tag `paper-d-registry-draft-2026-10-03`. The companion question "Do
explainers agree on which features matter?" is Paper E (`docs/reports/paper_e/`), to be
developed after this submission.

## Journal account request — 4 October 2026

The author confirmed sending the Spanish account-creation request to
`revistatm@tec.ac.cr`, as directed by the journal's
[registration page](https://revistas.tec.ac.cr/index.php/tec_marcha/registro).
The request supplied the author's name, UNADE affiliation, email and ORCID.
**Pending:** the journal's response and account access instructions. This request
is separate from Paper D's manuscript submission by email on 3 October 2026.

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

The first two need the packages in `requirements.txt`. On this machine, Windows
Application Control blocks SciPy's DLL inside the project `.venv`, so the analysis runs in
a separate virtual environment (Python 3.13). Measure the length in Word itself: the PDF
is only a proxy.

## Reproduce the results

This section is for a reader who wants to check the paper. It regenerates every number,
table and figure from the stored explanation runs. It does not repeat the runs.

**What is in the repository**

| Input or output | Path |
|---|---|
| UCI Adult data | `data/adult.csv` (if absent, the loader fetches it from OpenML) |
| Trained models and preprocessor | `experiments/exp1_adult/models/` |
| Explanation runs, UCI Adult (per instance) | `experiments/exp2_scaled/results/` |
| Explanation runs, German Credit | `experiments/exp3_cross_dataset/results/german_credit/` |
| Analysis results behind the paper | `outputs/analysis/paper_d/*.csv` (`metric,value` rows) |
| Pre-specified analysis plan and its deviations | `docs/reports/paper_d/ANALYSIS_PLAN.md` |

**Steps** (about 1 GB of disk; the analysis takes a few minutes on a laptop)

```bash
git clone https://github.com/jonnabio/xai-eval-framework
cd xai-eval-framework
git checkout <release tag cited in the paper>

python -m venv .venv-paper-d
.venv-paper-d/Scripts/python -m pip install -r docs/reports/paper_d/requirements.txt   # Windows
# source .venv-paper-d/bin/activate && pip install -r docs/reports/paper_d/requirements.txt   # Linux, macOS

python scripts/pubs/paper_d_analysis.py        # rewrites outputs/analysis/paper_d/
python scripts/generate_paper_d_figures.py     # rewrites docs/reports/paper_d/figures/
python scripts/pubs/render_paper_d.py          # fills the template; needs no extra package
python scripts/pubs/verify_claims.py           # every printed number matches the results
git diff --stat --ignore-cr-at-eol             # what changed against the release
```

On Windows, run `git config --global core.longpaths true` before cloning: some run paths
are longer than 260 characters and the checkout is otherwise incomplete.

**What to expect.** This was run from a clean clone on 2026-10-03 (Windows 11, Python
3.13, the versions in `requirements.txt`):

- All 13 result files have the same rows. Of 11,976 cells, 159 differ, by at most
  8 parts in 10^11 (floating-point order of operations). No printed value changes:
  `render_paper_d.py` produces the same `paper_d.tex` and `verify_claims.py` passes.
- The three figure PDFs are rewritten from the same result files, so git reports them
  as changed (the files embed their creation time).

**Limits**

- The PDF and Word files are built by `scripts/pubs/build_paper_d.py`, which also needs
  Tectonic (`tools/tectonic-portable/`, not tracked) and Quarto. Checking the results
  does not need them.
- The explanation runs were produced between January and July 2026 with the full
  environment in `requirements-frozen.txt` and the configurations under
  `configs/experiments/`. Repeating them takes days of computation and need not give
  identical values, because SHAP, XGBoost and the samplers changed between releases.
- The stored models do not reproduce every recorded prediction. The margin analysis
  (RQ4) therefore uses only the runs they reproduce at 99% or more; the paper reports
  how many.

## Release and archive

The paper cites a tagged release and its Zenodo version DOI. The procedure is the one in
`docs/reports/paper_bc/ZENODO_RELEASE.md` (Route A): bump `.zenodo.json` and
`CITATION.cff`, tag, publish a GitHub release, wait for Zenodo, then set `\paperdrelease`
and `\paperdarchive` in `paper_d_template.tex` and rebuild. The manuscript inside the
archive prints "[ZENODO VERSION DOI PENDING]"; the code and data in it are exact.

| | |
|---|---|
| Release | `paper-d-submission-2026-10-03` (commit `021d85ead`), published 2026-10-03 |
| Version | 0.5.0 |
| Version DOI (cited in the paper) | `10.5281/zenodo.23130014` |
| Concept DOI (all versions) | `10.5281/zenodo.19297723` |
| Archive | one zip, 917 MB, open access, MIT licence |

If the analysis code or its results change before acceptance, publish a new version and
update the two macros. A change to the manuscript text alone does not need one.

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
