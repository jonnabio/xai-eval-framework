# BibTeX Repair Log

This log tracks citation problems found while preparing the Phase 2 literature
review expansion.

## Current Audit

- Audit date: 2026-05-03
- Thesis files checked: `thesis/*.qmd`
- Used citation keys: 47
- Bibliography keys in `thesis/references.bib`: 134

## Missing Keys

These keys are cited in thesis `.qmd` files but are not currently defined in
`thesis/references.bib`:

| Missing Key | Current Use | Recommended Action |
|---|---|---|
| `brown2023` | User expectations / XAI practicality claims | Replaced with verified sources: `hoffman2023`, `pawlicki2024`, and `burger2023` depending on claim context |
| `demsar2006` | Friedman/Nemenyi statistical methodology | Added verified BibTeX |
| `friedman1937` | Friedman test | Added verified BibTeX |
| `kohavi1996` | UCI Adult Income dataset | Added verified BibTeX |
| `lakens2013` | Effect size interpretation | Added verified BibTeX |
| `linardatos2021` | Interpretability/explainability distinction | Replaced with existing verified key `linardatos2020` |
| `nemenyi1963` | Nemenyi post-hoc test | Added verified BibTeX |
| `wilcoxon1945` | Wilcoxon signed-rank test | Added verified BibTeX |

## Repair Status

- `brown2023`: removed from thesis citations; no verified Brown-authored 2023
  source matching the cited claims was identified during Sprint 1.
- `linardatos2021`: removed from thesis citations and normalized to
  `linardatos2020`, which is already present in `references.bib`.
- Statistical and dataset keys were added to `thesis/references.bib`.
- `burger2023` and `hoffman2023` were added as verified replacement sources.

## Follow-up Issues Found

The missing-key defect is resolved, but a duplicate-key scan found two
pre-existing duplicate BibTeX keys:

| Duplicate Key | Count | Action |
|---|---:|---|
| `goodfellow2014` | 2 | Inspect duplicate entries and merge or rename |
| `hinton2006` | 2 | Inspect duplicate entries and merge or rename |

These duplicates were not introduced by Sprint 1, but should be cleaned before
the next full thesis render.

## Key Normalization Notes

- Prefer ASCII citation keys where possible.
- Existing key `marcinkevičs2023` contains a non-ASCII character. It is currently
  both cited and present, but it is a render-risk candidate if tooling behaves
  inconsistently. Consider renaming to `marcinkevics2023` in both `.qmd` and
  `references.bib`.
- Avoid anonymous keys like `ref_7` for sources that become central to the
  thesis argument. Replace with author-year keys after verification.

## Repair Workflow

1. Verify the source through `paper-lookup`, Crossref, OpenAlex, Semantic Scholar,
   arXiv, publisher pages, or official dataset pages.
2. Fetch or construct BibTeX only from verified metadata.
3. Add the BibTeX entry to `thesis/references.bib`.
4. Run the citation audit again.
5. Render the thesis after Quarto is available.

## Acceptance Criteria

- No cited key is missing from `thesis/references.bib`.
- No high-value source uses a vague `ref_*` key.
- All central method/framework citations include DOI, arXiv ID, proceedings URL,
  or stable publisher/project URL where available.
- Citation keys are stable, ASCII, and descriptive.
