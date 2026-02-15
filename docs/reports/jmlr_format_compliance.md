# JMLR Format and Submission Compliance Notes

This note captures publication-format requirements relevant to the current prototype for Journal of Machine Learning Research (JMLR), with emphasis on Datasets and Benchmarks positioning.

## 1. Official Sources Consulted
- JMLR author information page: https://jmlr.org/author-info.html
- JMLR style/template package page: https://jmlr.org/format/
- JMLR style package repository: https://github.com/JMLR/jmlr-style-file
- JMLR call for benchmark papers: https://jmlr.org/call-for-papers/benchmark.html

## 2. Core Formatting Requirements
1. Use the official JMLR LaTeX style/package (`jmlr` / `jmlr2e` ecosystem from the official repository).
2. Prepare manuscript in the JMLR publication style (single-column final presentation).
3. Use the sample template as baseline for front matter and bibliography setup.
4. Keep all figures/tables publication-ready and reproducible from scripts.

## 3. Datasets and Benchmarks Track Positioning
The benchmark call emphasizes:
1. scientific rigor in evaluation design,
2. practical reproducibility,
3. public usability of artifacts (data/code/model outputs),
4. and clear benchmark scope/limitations.

For this project, that translates to:
- explicit experiment inventory reporting,
- transparent handling of missing/corrupt runs,
- complete statistical protocol disclosure,
- and clear distinction between validated claims and pending validation.

## 4. Practical Checklist for This Manuscript
- [ ] Move the prototype from Markdown to the official JMLR LaTeX template.
- [ ] Add a formal Related Work section with BibTeX citations.
- [ ] Add a complete Experimental Protocol section with block design and tests.
- [ ] Add artifact-coverage table (`planned`, `completed`, `missing`, `invalid`).
- [ ] Add a reproducibility statement (seeds, environment, scripts, outputs).
- [ ] Add ethical/limitations section for LLM-as-a-judge use.
- [ ] Add code/data availability and license statement.

## 5. Current Gap Assessment
- Strengths:
  - multi-metric evaluation with non-parametric statistical testing;
  - explicit reproducibility metrics;
  - semantic-evaluation module with dimension-level outputs.
- Gaps to close before submission:
  - finalize missing/corrupt run recovery or explicitly freeze benchmark scope;
  - complete human-calibration evidence for LLM-judge claims;
  - migrate to official JMLR LaTeX submission format.
