# Paper B — submission sheet: *CLEI Electronic Journal*

**Journal:** *CLEI Electronic Journal* (CLEIej), Centro Latinoamericano de Estudios en
Informática. ISSN 0717-5000. Submit at https://www.clei.org/cleiej (register, then the
five-step submission).

**Status: SUBMITTED on 2026-10-04, submission 1196** (see "Submission record" below). Do not
rebuild the PDFs or change the manuscript unless the journal requests a revision.

Before submission: reviewed by the Scientific Editor role on 2026-10-04
(`docs/review/scientific-review_paper_b_cleiej_2026-10-04.md`), one major defect corrected;
that review was not independent of the drafting session. The author then revised the text and
confirmed the title. Decision record: ADR-0022.

## Submission record

| Item | Value |
|---|---|
| Date | 2026-10-04 |
| Journal | *CLEI Electronic Journal* |
| Submission | 1196, https://www.clei.org/cleiej/index.php/cleiej/authorDashboard/submission/1196 |
| Acknowledged by | Esteban Clua, by email from the journal system |
| File sent | `paper_b_cleiej.pdf`, 12 pages, source at commit `c72a17e88` |
| Comments for the editor | The text of section 3 |
| Decision | Pending |

## 1. Journal requirements, checked 2026-10-04

Sources: the journal's "Submissions", "About" and "Editorial Process" pages, and
`AuthorInstructions2016.pdf` from its LaTeX package.

| Requirement | Journal rule | This draft |
|---|---|---|
| Fees | "does not apply any author charges whatsoever for submitting and publishing" | None |
| Review | Single-blind, two or more external referees; the editor may reject without review | Author, repository and DOI are printed |
| Language | English | English |
| Length | **At least 12 pages**; no maximum stated | 12 pages, references included, no appendix |
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
| `paper_b_cleiej.pdf` | **The file to upload** (the journal reviews single-blind), 12 pages |
| `paper_b_cleiej_blind.tex` / `.pdf` | Double-blind build of the same source, 12 pages: no author block, no acknowledgments, repository address and DOI withheld. Not needed by this journal; kept for a venue or a reader that asks for it |
| `cleiej.cls` | Journal class, unmodified |
| `figures/` | Two figures, rebuilt by a committed script |
| `pub/claims.toml` (`[papers.paper_b]`) | Abstract and keywords; generated into `pub/fragments/` |

Build, from the repository root:
`tools/tectonic-portable/tectonic docs/reports/paper_b/paper_b_cleiej.tex`.
Then run `verify_claims.py`, `verify_sync.py`, `scan_shared_literals.py --strict` and
`verify_exp4_reconstruction.py` from `scripts/pubs/`.

## 3. Comments for the editor (text for the submission form, 2026-10-04)

> Dear Editor,
>
> I submit the manuscript "When Does SHAP Outperform LIME? Model- and Configuration-Dependent
> Results from a Paired Tabular Benchmark" for consideration as a regular article in the CLEI
> Electronic Journal. It has not been published and is not under review at another journal.
>
> The manuscript reports a paired comparison of LIME and SHAP on tabular classification
> models, over 75 matched cells of five model families. Its main results are that the latency
> ordering of the two methods depends on the model family and reverses between two tree
> ensembles, and that the near-zero stability of LIME on the Adult dataset depends on the
> kernel width and the feature space and is high on two further datasets. It closes with a
> deployment recommendation conditioned on the model architecture.
>
> Relation to earlier work. The runs analysed here were released with an earlier article by
> the author and a co-author (Revista de Investigación Multidisciplinaria Iberoamericana,
> https://doi.org/10.69850/rimi.vi3.307). That article includes a paired SHAP-LIME test on a
> 45-cell subset of three model families. The present manuscript extends that test to the
> full 75 cells, adds confidence intervals and effect sizes, and contributes the results
> listed above, which are not in the article. No numerical result of the article is restated;
> Sections 1, 4.1 and 5.1 state the relation.
>
> Two further manuscripts by the author analyse the same runs for different questions (the
> behavior of explanations on misclassified instances, and the instance-level agreement
> between the feature rankings of SHAP and LIME) and are under review at other journals.
> Neither reports a result reported here.
>
> The code, the run artifacts and earlier drafts of this work are in a public repository,
> archived at https://doi.org/10.5281/zenodo.23147228. The archived draft carries an earlier
> title of the same manuscript.
>
> Sincerely,
> Jonathan Herrera-Vásquez

Optional sentence, not included above (author decision): "An earlier and longer version,
which also contained a literature taxonomy and a study of language-model judges, was declined
by two journals without review; that material is not part of this manuscript." It is
accurate; the journal's checklist asks only about prior publication and concurrent review.

## 4. Items before submission (closed 2026-10-04)

1. Done: the author's own revision of the PDF. It removed the horizontal grid lines of
   Figure 2 and the "Provenance of the cohort" paragraph of Section 5.3 (the full PDF went
   from 13 to 12 pages). The two manuscripts under review elsewhere are now disclosed only in
   the comments for the editor.
2. Done: title confirmed by the author. The keywords were left as they are (author decision).
3. Done 2026-10-04: Zenodo version 0.9.0, `10.5281/zenodo.23147228`, from GitHub release
   `paper-b-cleiej-2026-10-04` (tag on `main` `a2ea80080`). The paper cites it. A later change
   to code or results needs a new version; a text change does not.
4. The earlier drafts are public (repository history, Zenodo). Single-blind review does not
   forbid this.

## 5. Figures

Paper B keeps its own copies in `docs/reports/paper_b/figures/`. Rebuild them with:

```bash
python scripts/generate_paper_b_figures.py --output-dir docs/reports/paper_b/figures
```

The 32-page edition and the Paper C material stay in `docs/reports/paper_bc/`; nothing of
Paper B is kept there.

## 6. Title and the double-blind build (2026-10-04)

- **Title:** "When Does SHAP Outperform LIME? Model- and Configuration-Dependent Results from a
  Paired Tabular Benchmark" (review finding F02). The earlier title was "LIME versus SHAP under
  Matched Conditions: A Paired Comparison on Tabular Models"; the Zenodo 0.9.0 archive and the
  GitHub release carry the earlier title.
- **Double-blind build:** `tectonic docs/reports/paper_b/paper_b_cleiej_blind.tex`. After every
  edit, check it with:

  ```bash
  pdftotext docs/reports/paper_b/paper_b_cleiej_blind.pdf - | grep -i -E "jonnabio|github|zenodo|UNADE|Universidad Americana|Canc.n|Jonathan|Acknowledg|by the author"
  ```

  Expected output: nothing. Reference [10] names its authors as any citation does, and the
  text refers to it in the third person.
