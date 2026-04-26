# Paper C Artifact Index

## 1. Metadata

- **Date**: 2026-04-15
- **Paper**: Paper C — *From Fidelity to Semantics: A Taxonomy and Survey of Evaluation Metrics for Model-Agnostic Explainability*
- **Purpose**: Reviewer-facing path map for the sources, analysis, and reporting artifacts used by Paper C
- **Status**: Draft index; review corpus frozen 2026-04-05; 24 unique coded papers

## 2. Primary Manuscript Artifacts

| Artifact | Path | Role |
| :--- | :--- | :--- |
| JMLR manuscript source | `docs/reports/paper_c/paper_c_prototype_jmlr.tex` | Main Paper C LaTeX source, JMLR style with journal header and attribution footer. |
| JMLR rendered manuscript | `docs/reports/paper_c/paper_c_prototype_jmlr.pdf` | Compiled JMLR-branded PDF for review and journal submission. |
| Neutral manuscript source | `docs/reports/paper_c/paper_c_prototype_neutral.tex` | Internal-conference wrapper that reuses the main LaTeX source with the JMLR style package in unbranded preprint mode. |
| Neutral rendered manuscript | `docs/reports/paper_c/paper_c_prototype_neutral.pdf` | Compiled PDF for internal university presentation without visible JMLR journal branding. |
| Markdown prototype | `docs/reports/paper_c/paper_c_prototype.md` | Markdown draft used for early structure review. |
| Build/compilation instructions | `docs/reports/paper_c/paper_c_prototype_instructions.md` | Step-by-step notes on how the PDF was compiled and what packages were used. |
| Scope and validity notes | `docs/reports/paper_c/paper_c_scope_and_validity_notes.md` | Boundaries for what Paper C can and cannot claim at current corpus maturity. |
| JMLR style file | `docs/reports/paper_c/jmlr2e.sty` | Local copy of JMLR2e style package. |

## 3. Review Corpus Artifacts

| Artifact | Path | Role |
| :--- | :--- | :--- |
| Cleaned review corpus | `docs/reports/paper_c/paper_c_review_corpus.csv` | 24-paper coded corpus, frozen 2026-04-05. |
| Descriptive summary | `docs/reports/paper_c/paper_c_review_summary.md` | Auto-generated summary of corpus coding dimensions and distribution. |
| Upstream literature matrix | `docs/reports/literature_review_methodology_matrix.md` | Full thesis-level literature matrix from which Paper C corpus was derived. |

## 4. Related Analysis Artifacts

| Artifact | Path | Role |
| :--- | :--- | :--- |
| Review summary generator | `scripts/generate_paper_c_review_summary.py` | Generates `paper_c_review_summary.md` from the cleaned corpus CSV. |
| Paper metrics generator | `scripts/generate_paper_metrics.py` | Shared cross-paper metrics generator. |
| Cross-study integration driver | `scripts/integrate_experiment_evidence.py` | Generates EXP1/EXP2/EXP3 evidence handoff tables and the Paper C EXP3 integration addendum. |
| EXP3 integration addendum | `outputs/analysis/integrated_evidence/paper_c_exp3_addendum.md` | Paper C note positioning EXP3 as future semantic-evaluation material, not as completed semantic preference validation. |

## 5. Dependency and Environment Artifacts

| Artifact | Path | Role |
| :--- | :--- | :--- |
| Runtime requirements | `requirements.txt` | Active dependency declaration. |
| Frozen requirements | `requirements-frozen.txt` | Fully pinned environment snapshot. |
| Conda environment | `environment.yml` | Conda environment entry point. |

## 6. Corpus and Scope Snapshot

- **Corpus freeze date**: 2026-04-05
- **Upstream matrix rows reviewed**: 25
- **Duplicate rows removed**: 1
- **Unique coded papers**: 24
- **Cluster distribution**: 8 faithfulness/robustness, 6 modality/domain, 4 LLM-judge, 3 benchmark/toolkit, 3 taxonomy/survey
- **Evidence-source coverage**: 20 proxy, 6 benchmark, 4 LLM-judge, 4 end-user, 3 expert-human
- **Confidence mix**: 19 high, 3 medium, 2 title-level

Paper C **can** claim:
- Construct-level arguments about why XAI evaluation fragments across targets, evidence sources, and quality properties.
- Thesis-level justification for layered evaluation (technical proxy + semantic).
- Proxy-dominant measurement characterization of the current coded corpus.

Paper C **cannot yet** claim:
- Exhaustive bibliometric coverage.
- Pooled effect-size conclusions.
- Fully validated semantic evaluators vs. human judgments (pending Paper A human data collection).

## 7. Thesis Role

Paper C supplies the conceptual bridge between Paper B (quantitative benchmark layer) and Paper A (LLM-based semantic evaluation). It motivates why Paper B needs a multi-metric benchmark and why Paper A needs explicit evaluator validation.

## 8. Build Instructions

To reproduce PDFs from source:

```powershell
# JMLR branded version
.\tools\tectonic-portable\tectonic.exe .\docs\reports\paper_c\paper_c_prototype_jmlr.tex

# Neutral/unbranded version (for internal presentations)
.\tools\tectonic-portable\tectonic.exe .\docs\reports\paper_c\paper_c_prototype_neutral.tex
```
