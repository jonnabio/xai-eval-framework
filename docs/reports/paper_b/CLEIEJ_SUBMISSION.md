# Paper B — submission sheet: *CLEI Electronic Journal*

**Journal:** *CLEI Electronic Journal* (CLEIej), Centro Latinoamericano de Estudios en
Informática. ISSN 0717-5000. Submit at https://www.clei.org/cleiej (register, then the
five-step submission).

**Status (2026-10-04):** first draft built, 13 pages. Reviewed by the Scientific Editor role the same day
(`docs/review/scientific-review_paper_b_cleiej_2026-10-04.md`); one major defect corrected.
That review was not independent of the drafting session. The author has not yet read the
corrected text. Decision record: ADR-0022.

## 1. Journal requirements, checked 2026-10-04

Sources: the journal's "Submissions", "About" and "Editorial Process" pages, and
`AuthorInstructions2016.pdf` from its LaTeX package.

| Requirement | Journal rule | This draft |
|---|---|---|
| Fees | "does not apply any author charges whatsoever for submitting and publishing" | None |
| Review | Single-blind, two or more external referees; the editor may reject without review | Author, repository and DOI are printed |
| Language | English | English |
| Length | **At least 12 pages**; no maximum stated | 13 pages, references included, no appendix |
| Page | A4, 10 pt, single column, page numbers, no other header or footer | `cleiej.cls`, unmodified |
| Abstract | **At most 200 words**, on the first page with the keywords | 199 words, from `pub/claims.toml` |
| Keywords | Short list; should fall within the journal's topics | Five |
| Sections | Numbered; abstract, acknowledgments and references unnumbered | As required |
| Tables | Caption before the table, no vertical lines, no period at the end of a caption | As required |
| Figures | Caption after the figure, each referred to in the text | As required |
| References | IEEE style, numbered in order of citation, DOIs included | 38 entries, in citation order, each cited |
| File | PDF only | `paper_b_cleiej.pdf` |
| Originality | Not published and not under review elsewhere, or explained to the editor | See section 3 |
| Licence | CC-BY; authors keep copyright | – |
| On acceptance | ASCII text of title, authors, institutions, abstract and keywords | – |

Published examples (Vol. 29 No. 4, 2026) run from 14 to 31 pages.

## 2. Files

| File | Role |
|---|---|
| `paper_b_cleiej.tex` | Manuscript source |
| `paper_b_cleiej.pdf` | The file to upload |
| `cleiej.cls` | Journal class, unmodified |
| `figures/` | Three figures, each rebuilt by a committed script |
| `pub/claims.toml` (`[papers.paper_b]`) | Abstract and keywords; generated into `pub/fragments/` |

Build, from the repository root:
`tools/tectonic-portable/tectonic docs/reports/paper_b/paper_b_cleiej.tex`.
Then run `verify_claims.py`, `verify_sync.py`, `scan_shared_literals.py --strict` and
`verify_exp4_reconstruction.py` from `scripts/pubs/`.

## 3. Comments for the editor (draft)

> This manuscript reports a paired comparison of LIME and SHAP on tabular models. Its runs
> were released with an earlier article by the author (Revista de Investigación
> Multidisciplinaria Iberoamericana, https://doi.org/10.69850/rimi.vi3.307). That article
> includes a paired SHAP-LIME test on a 45-cell subset of three model families. The present
> manuscript extends it to the full 75 cells of five model families, adds confidence intervals
> and effect sizes, and contributes the results that are not in the article: the dependence of
> the latency ordering on the model family, the dependence of LIME's stability on the kernel
> width and the dataset, and the cross-dataset extension. No numerical result of the article
> is restated; Sections 1, 4.1 and 5.3 state the relation. Two further manuscripts by the
> author, on other questions and with no shared result, are under review at other journals.
> Earlier drafts of this work are available in the public repository and its archive. An
> earlier and longer version, which also contained a literature taxonomy and a study of
> language-model judges, was declined by two journals without review; that material is not
> part of this manuscript.

**[AUTHOR]** Decide whether the last sentence is sent. It is accurate; the journal's checklist
asks only about prior publication and concurrent review.

## 4. Open before submission

1. A review by someone who did not write the draft. The Scientific Editor review of
   2026-10-04 (`docs/review/scientific-review_paper_b_cleiej_2026-10-04.md`) was done by the
   drafting session.
2. Author's read of the PDF.
3. Done 2026-10-04: Zenodo version 0.9.0, `10.5281/zenodo.23147228`, from GitHub release
   `paper-b-cleiej-2026-10-04` (tag on `main` `a2ea80080`). The paper cites it. A later change
   to code or results needs a new version; a text change does not.
4. The earlier drafts are public (repository history, Zenodo). Single-blind review does not
   forbid this.

## 5. Figures

Paper B keeps its own copies in `docs/reports/paper_b/figures/`. Rebuild them with:

```bash
python scripts/generate_paper_b_figures.py --output-dir docs/reports/paper_b/figures
python scripts/generate_exp3_gap_figure.py --output-dir docs/reports/paper_b/figures
```

The 32-page edition and the Paper C material stay in `docs/reports/paper_bc/`; nothing of
Paper B is kept there.
