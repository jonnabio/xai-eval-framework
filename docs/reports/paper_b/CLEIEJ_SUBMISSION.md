# Paper B — submission sheet: *CLEI Electronic Journal*

**Journal:** *CLEI Electronic Journal* (CLEIej), Centro Latinoamericano de Estudios en
Informática. ISSN 0717-5000. Submit at https://www.clei.org/cleiej (register, then the
five-step submission).

**Status (2026-10-04):** first draft built, 13 pages. **Not ready to submit**: it has not had
the independent review that the plan requires
(`docs/planning/paper_b_13pp_reduction_plan_2026-10-04.md`, step 7), and the author has not
read it. Decision record: ADR-0022.

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
| Abstract | **At most 200 words**, on the first page with the keywords | 191 words, from `pub/claims.toml` |
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
> were released with an earlier article (Revista de Investigación Multidisciplinaria
> Iberoamericana, https://doi.org/10.69850/rimi.vi3.307); the manuscript reports no result of
> that article and says so in Section 5.3. Two further manuscripts by the author, on other
> questions and with no shared result, are under review at other journals. An earlier and
> longer version of this work, which also contained a literature taxonomy and a study of
> language-model judges, was declined by two journals without review; that material is not
> part of this manuscript.

**[AUTHOR]** Decide whether the last sentence is sent. It is accurate; the journal's checklist
asks only about prior publication and concurrent review.

## 4. Open before submission

1. Independent review of the draft (focus, novelty against Papers A, D and E, claim support).
2. Author's read of the PDF.
3. A new Zenodo version: the DOI printed now (`10.5281/zenodo.23111684`, version 0.4.0) is the
   archive of the 32-page edition. Update `\zenodoversiondoi` after the release.
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
