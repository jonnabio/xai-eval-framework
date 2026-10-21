# Paper B — submission sheet: *Computers and Informatics* (C&I)

**Journal:** *Computers and Informatics* (C&I), DergiPark, e-ISSN 2757-8259, DOI prefix
10.62189/ci. Open access, CC BY-NC 4.0, indexed in DOAJ and TR Dizin. Two issues a year (Vol. 6
No. 1 of 30 June 2026 has three articles). Guidelines: https://dergipark.org.tr/en/pub/ci/writing-rules.
Submit at https://dergipark.org.tr/en/journal/3364/submission/step/manuscript/new.

**Status (2026-10-21): prepared, NOT submitted.** The author decided on 2026-10-21 to withdraw
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
| Similarity report | Full-text PDF, quotes included, bibliography excluded, no match excluded; at most 20% overall and 3% from one source | **Not made**: needs iThenticate or Turnitin access (section 4); form `journal_files/similarity_report_form.pdf` |
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

## 4. Before submission (open)

1. **Withdrawal from CLEIEJ.** The journal forbids concurrent submission, and the cover letter
   states that the earlier submission was withdrawn. Ask CLEIEJ to withdraw submission 1196 and
   wait for the confirmation; record it in `../CLEIEJ_SUBMISSION.md`.
2. **Reference rule (essential, author rule of 2026-10-05).** For a manuscript not yet submitted,
   every reference carries its DOI URL and is verified, and at least 80% date from 2024 or later.
   This edition, like the CLEIEJ one, has **7 of 38 (18%)** from 2024 or later, and 5 entries
   without any link (Lundberg 2017, Hooker 2019, Adebayo 2018, Kohavi 1996, Holm 1979). Meeting
   the rule means replacing or adding about 30 references, each verified against its source, and
   rewriting the sentences that cite them. Author decision needed.
3. **Similarity report.** The text of the CLEIEJ edition is public (GitHub repository, Zenodo
   0.9.0 `10.5281/zenodo.23147228`), and Sections 2 and 3 share wording with the RIMI article.
   A report run against the web may match the author's own archive above the 3% single-source
   limit. The cover letter discloses the archive; the editors decide after reading the report.
4. **Cover letter:** review the text, set the date. It says "an earlier version was submitted to
   another journal and has been withdrawn" (true only after item 1).
5. Sign the copyright agreement.
6. The running head on the title page ("SHAP versus LIME on a paired tabular benchmark") is a
   proposal.

## Submission record

| Item | Value |
|---|---|
| Date | — |
| Submission | — |
| Files sent | — |
| Decision | — |
