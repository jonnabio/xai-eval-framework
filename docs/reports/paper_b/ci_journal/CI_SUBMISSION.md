# Paper B — submission sheet: *Computers and Informatics* (C&I)

**Journal:** *Computers and Informatics* (C&I), DergiPark, e-ISSN 2757-8259, DOI prefix
10.62189/ci. Open access, CC BY-NC 4.0, indexed in DOAJ and TR Dizin. Two issues a year (Vol. 6
No. 1 of 30 June 2026 has three articles). Guidelines: https://dergipark.org.tr/en/pub/ci/writing-rules.
Submit at https://dergipark.org.tr/en/journal/3364/submission/step/manuscript/new.

**Status: SUBMITTED on 2026-10-21** (author; submission number not yet recorded). Do not rebuild or edit unless the journal asks for a revision.

Prepared 2026-10-21. The author decided on 2026-10-21 to withdraw
Paper B from the *CLEI Electronic Journal* (submission 1196) because of the length of its queue,
and to submit it here. The CLEIEJ edition (`../paper_b_cleiej.tex` and its PDFs) is kept
unchanged; see `../CLEIEJ_SUBMISSION.md`.

## 1. Journal requirements, checked 2026-10-21

Sources: the "Author Guidelines", "Price Policy", "Ethical Principles and Publication Policy"
and "Aim & Scope" pages; the journal's manuscript template (journal-file 26193); two articles of
Vol. 6 No. 1 (2026), read to settle what the template leaves open.

| Requirement | Journal rule | This edition |
|---|---|---|
| Fees | "There is NO article processing or submission charge" | None |
| Review | Masked (double-blind); names, affiliations and ORCID must not appear in the manuscript | Masked; author data only on the title page. The build fails if author data reach the manuscript |
| Concurrent submission | Forbidden; the author certifies the work is not under consideration elsewhere | **The CLEIEJ withdrawal must be confirmed first** (section 4) |
| File | .doc or .docx only; no PDF manuscript | `paper_b_ci_manuscript.docx` |
| Template | The journal's Word template | Built in it: its styles, header, footer and title block |
| Language | English, one spelling throughout, CSE style, SI units, abbreviations defined at first use | American spelling, as the CLEIEJ edition |
| Length | No limit stated (published articles: 7 to 17 pages) | 14 pages in Word |
| Abstract | 150 to 200 words | 199 words, from `pub/fragments/paper_b_abstract_en.tex` |
| Keywords | 3 to 5, in alphabetical order, first letter capital | Benchmarking, Explainable artificial intelligence, Explanation evaluation, LIME, SHAP |
| Sections | Numbered "1. INTRODUCTION", subsections "1.1. Title"; Acknowledgements and References unnumbered | As required |
| Figures | Arabic numbers, caption below, "Figure 1." | As required |
| Tables | Arabic numbers, caption above, "Table 1." | As required; no vertical lines, as the template's example |
| Equations | Numbered (1) at the right; cited as Eq. (1) | Four equations, each cited as Eq. (n) |
| References | Numbered [n] in order of citation; the template's examples and published articles use Vancouver form with the DOI | 38 entries in Vancouver form, same entries and links as the CLEIEJ edition |
| Page numbers | Guidelines: "number every page"; template text: "should not use any page numbers" | The template's footer carries a page number, as in published articles; kept |
| Font | Template text says Times New Roman 11 pt; the template's styles and every published article use Segoe UI 10 pt | The template's styles (Segoe UI) |
| Title page | Separate file: name, institution, city, country, e-mail, ORCID of each author | `paper_b_ci_title_page.docx`, with the acknowledgment, data availability and competing interests |
| Cover letter | Significance, novelty, problem, fit with the journal; not the abstract | `paper_b_ci_cover_letter.docx` (draft, section 4) |
| Copyright agreement | Signed by the corresponding author, uploaded at submission | `journal_files/copyright_agreement.pdf`, to sign |
| Similarity report | intihal.net report made by the submission system from the full text of step 3; at most 20% overall and 3% from one source | 1% overall, every source under 1% (section 4) |
| Ethics | Ethics committee approval if applicable | Not applicable: public datasets, no participants |
| Competing interests | Disclosed | Unnumbered section in the manuscript and on the title page |

## 2. Files

| File | Role |
|---|---|
| `paper_b_ci.tex` | Text of this edition: a copy of `../paper_b_cleiej.tex` changed only in form (masked review, Eq. (n) citations, competing-interests section, Vancouver references). Not compiled; read by the builder |
| `scripts/build_paper_b_ci_docx.py` | Writes the three Word files into the journal's templates and prints PDFs with Word |
| `submission/paper_b_ci_manuscript.docx` | **The manuscript to upload** (masked) |
| `submission/paper_b_ci_title_page.docx` | **Title page to upload** |
| `submission/paper_b_ci_cover_letter.docx` | **Cover letter to upload**, after the author's review |
| `submission/*.pdf` | Word prints of the three files, to check the layout; not for upload |
| `journal_files/` | The journal's template and forms, downloaded 2026-10-21 (not committed; `.gitignore`) |

Figures are those of the CLEIEJ edition (`../figures/`, PNG copies; generator
`scripts/generate_paper_b_figures.py`).

Build, from the repository root (needs Quarto and, for the PDFs, Word):

```bash
.venv/Scripts/python.exe docs/reports/paper_b/ci_journal/scripts/build_paper_b_ci_docx.py
```

Then `verify_claims.py`, `verify_sync.py`, `scan_shared_literals.py --strict` and
`verify_exp4_reconstruction.py` from `scripts/pubs/`. The edition is under `[coverage]` in
`pub/claim_registry.toml` and every literal it prints is registered (added 2026-10-21).

The journal's files are re-downloaded from:
manuscript template https://dergipark.org.tr/en/download/journal-file/26193, title page 17769,
copyright agreement 17770, similarity report form 17771, cover letter 17772 (same address).

## 3. What changed from the CLEIEJ edition

- Masked review: no author block, no acknowledgment, the repository and Zenodo addresses withheld
  in the data-availability section (they are on the title page).
- Each displayed equation is cited in the text as Eq. (n) (author rule of 2026-10-12).
- A "Competing Interests" section (as in the journal's published articles).
- References in Vancouver form; same 38 entries, same DOIs and links (checked by script).
- No result, sentence of analysis or claim changed.

## 4. Before submission

1. Done 2026-10-21: CLEIEJ withdrawal of submission 1196 confirmed by the editor (reported by
   the author).
2. Reference rule: author decision of 2026-10-21, the reference list stays as in the CLEIEJ
   edition for this paper (7 of 38 from 2024 or later; 5 entries without a link). Not to be
   reopened for this edition.
3. Done 2026-10-21: **similarity report** by intihal.net, made by the submission system from the
   masked manuscript (report shared by the author, "Intihal Proje Detaylari.pdf"). Settings:
   minimum match of 9 words, citations and bibliography excluded. Document: 14 pages, 5,937
   words, 35,625 characters. **Similarity index 1%** (limit 20%); eight primary sources, each
   **under 1%** (limit 3%), none of them related to this work: breast-cancer image segmentation
   (A. Tekerek), personality prediction in social media (Elsevier), fraud detection in review
   platforms (ITU), Russian loanwords (dissertation), multivariate group differences (Bayesian),
   one source without a title, hip abductor activity (Wiley), energy efficiency and mortgage
   default (Springer). No match with the author's archive or the RIMI article is listed. Within
   the journal's limits; no revision needed.
4. Done 2026-10-21: cover letter approved by the author. Set the date on the day of submission.
5. Sign the copyright agreement.
6. The running head on the title page ("SHAP versus LIME on a paired tabular benchmark") is a
   proposal.

The masked copy is the manuscript itself (`submission/paper_b_ci_manuscript.docx`); the journal
reviews masked, so there is no separate unmasked manuscript. Upload: manuscript, title page,
cover letter, signed copyright agreement; the similarity report is made by the system.

## Submission record

| Item | Value |
|---|---|
| Date | 2026-10-21 (author, in session; to be confirmed) |
| Submission | Number not recorded |
| Files sent | `submission/paper_b_ci_manuscript.docx` (masked, full text for intihal.net), `paper_b_ci_title_page.docx`, `paper_b_ci_cover_letter.docx`, signed copyright agreement |
| Similarity | intihal.net 1%, every source under 1% (section 4) |
| Optional fields | Ethical statement: public anonymised datasets, no participants, no approval required; original and not under consideration elsewhere. Supporting institution: none, no external funding. Thanks: left empty (advised, to keep the review masked: the person thanked co-authored reference [10]); the acknowledgment is on the title page |
| Note to the editor | CLEIEJ 1196 withdrawn and confirmed; relation to the RIMI article (ref. [10]); other manuscripts on the same runs report none of these results; public archive on the title page; similarity 1% |
| Decision | Pending |
