# Paper E: conversion plan for *Advances in Artificial Intelligence Research* (AAIR)

Status: **approved by the author on 2026-10-21, Option T** (section 2). Lane `paper-e`,
branch `paper/e-aair`.

## 0. Why

The author withdrew Paper E from *Computación y Sistemas* (CyS; submission 6783, sent
2026-10-04). The editor said peer review would not start for over a year, and the PhD
timeline can't wait that long. The editor confirmed the withdrawal. New venue: AAIR
(DergiPark, ISSN 2757-7422, open access CC BY-NC 4.0, no fee: "No fee is charged from
the author or institution under any name"). Guidelines:
<https://dergipark.org.tr/en/pub/aair/writing-rules>, read 2026-10-21. The author
requires them to be followed to the letter.

## 1. Author decisions (2026-10-21)

1. **References:** the 80%-from-2024 rule is waived for this paper; it applies to future
   papers. The 25 verified references stay; each keeps its DOI URL.
2. **Reviewers:** the three nominations are added later. The cover letter keeps the slots
   empty until then.
3. **Turkish title:** a careful translation goes in. The letter to the editor states
   that the author does not speak Turkish and asks the editorial office to correct the
   title if needed.
4. **Withdrawal confirmation:** not stored in the repository.
5. **Zenodo:** see section 5.

## 2. Conflict to settle first: the guide text and the template file disagree

The writing-rules page gives one specification. The template file it links
(`journal_files/manuscript_template.docx`, journal-file 18038) and the latest published
article (Vol. 5 No. 2, Dec 2025, pp. 42-55, read 2026-10-21) follow a different one.

| Item | Writing-rules page | Template file | Published article (2025) |
|---|---|---|---|
| Columns | two columns of 85 mm, 10 mm gap | "A single-column format is used for the body" (the table also lists 8.5 cm columns) | single column |
| Font | Cambria 9 pt; headings Cambria 11/9 pt | Times New Roman 10 pt | Times New Roman 10 pt |
| Margins | 30/25/15/15 mm | 2.5 cm all sides | as in the template |
| Title | English **and Turkish**, 14 pt | English, 14 pt | English only |
| Headers, footers, page numbers | "should not be used" | journal header, "Surname et al. / AAIR" running header, "Page n" footer, corresponding-author footnote | present |
| Length | at most 15 pages | "should not exceed 8-10 pages" | 14 pages |
| Abstract | at most 300 words; template section says about 100-250 words, italic 8 pt | about 200 words, 10 pt, indented 0.5 cm | single block |
| Equations | 1x2 borderless table (90/10), Word equation editor | right tab, "do not use … tables"; cited as "Eq. (1)" | n/a |
| Authors | initials-capital names, affiliation lines with e-mails | names with ORCID on the affiliation line | ORCID icons, full surnames in capitals |
| References | example list in the Pamukkale (PAJES) style | "IEEE Citation and Reference Style", examples with doi | numbered |
| Extra sections | Acknowledgment, Appendix | Declaration of interest, Acknowledgements, Nomenclature | Declaration present |

The page text appears to be generic text taken from another DergiPark journal. Its
"Section 5" reference examples are in the PAJES style. The journal publishes in the
template's format. "To the letter" can't satisfy both, so the author picks one:

- **Option T (recommended): the template file plus the page's numeric limits.** Layout,
  fonts, header and footer, equations, ORCID and IEEE references as in the template, as
  the journal publishes. From the page: 15 pages at most, abstract within 100-250 words
  (meets both texts), 3-6 keywords, 10 figures and tables at most, 60 references at
  most, numbered [n] citations in separate brackets, captions (figures below, tables
  above), centred figures, wide floats at the top or bottom, underlined hyperlinks in
  the body font, abbreviations spelled out at first use, **title in English and
  Turkish**, all equations numbered. The cover letter states the choice in one
  sentence.
- **Option P: the page text exactly** (two columns, Cambria 9 pt, 30/25/15/15 mm, no
  header or footer, equation tables, PAJES references), built in the template file's
  styles changed to match. This follows the written rule, but the result won't look
  like what the journal publishes.

The 8-10 pages in the template: the page's 15-page rule for research articles is the
binding limit under either option. The current text is 15 pages in the CyS layout, so
the Word build will be measured, and the plan shortens nothing unless it goes over 15.

## 3. Requirements this edition meets (either option)

| Rule | CyS edition | AAIR edition |
|---|---|---|
| Research article, at most 15 pages | 15 (CyS) | Measured after the build; 15 or fewer |
| At most 10 figures and tables combined | 4 + 6 = 10 | 10, none added |
| At most 60 references | 25 | 25, DOI URL on each (exception granted, section 1) |
| Abstract at most 300 words; about 100-250; no uncommon abbreviations or citations | about 300 | Cut to 250 or fewer; check for abbreviations and citations |
| 3-6 keywords | as in CyS | 3-6 |
| Title in English and Turkish | English | Both; note in the letter (section 1) |
| Citations [1],[2],[5] and [3]-[9], numbered by first appearance | BibTeX numeric | Generated from `references.bib` in that form |
| Every equation numbered; Word equation editor, including symbols in the text | 2 numbered | Native Word equations (OMML) in the chosen layout, numbered and cited by generated numbers |
| Figure captions below, table captions above, figures centred, wide floats at the top or bottom | LaTeX | As required; figures re-exported from the committed generators, no data changes |
| Original or modified figures from other sources cited | none taken | None |
| Hyperlinks underlined, body font | n/a | As required |
| Copyright transfer form, signed | n/a | `journal_files/copyright_form.docx`, filled in for the author to sign |
| Cover letter (template `cover_letter_template.docx`), three reviewers, who not to use | n/a | Built from the template; reviewer slots left empty (section 1); plus originality, the CyS withdrawal, the Zenodo preprint and the Turkish-title note |
| Printing permissions | n/a | None needed: every figure is original |
| Similarity report, at most 20%, uploaded | n/a | Run before submission; the Zenodo 0.8.0 preprint may match, so it's disclosed in the cover letter |
| Ethics committee permission if required | n/a | Not required: public data, no participants; one sentence in the manuscript |
| Register as a reviewer (template, section 3.3) | n/a | Author, on the DergiPark account |

Notes on the cover-letter template: it declares that "the contents of this manuscript
have not been submitted … elsewhere". That is true only because the CyS submission was
withdrawn, so the letter states the withdrawal in plain words. The template's "last 12
months in the Communications" line is copied from another journal. It's kept as written,
since it is true: there is no earlier AAIR submission.

## 4. Folder and evidence (CyS edition untouched)

- New folder `docs/reports/paper_e/aair_journal/`, mirroring `paper_b/ci_journal/`:
  - `AAIR_SUBMISSION.md`: requirements table and submission record;
  - `paper_e_aair.tex`: the text of this edition, changed only in form, read by the
    builder;
  - `scripts/build_paper_e_aair_docx.py`;
  - `journal_files/`: the three files as downloaded on 2026-10-21, kept local and not redistributed (as for Paper B);
  - `submission/`: manuscript .docx and .pdf, cover letter, copyright form.
- **Not modified:** `paper_e_template.tex`, `paper_e.tex`, `tables/`, `figures/`,
  `submission/paper_e_blind.pdf`, `submission/paper_e_full.pdf`, `cys.*`, `template/`.
  The top-level `README.md` gets a status line and a "Withdrawn from CyS" record (date
  as reported, no confirmation file) pointing to the new folder.
- Numbers: the builder takes every value from the generated `paper_e.tex` and tables,
  never typed, and `verify_claims.py` covers the new text. No analysis is re-run.
- Masking: the guidelines don't ask for a blind manuscript, and the template puts
  names and ORCID in the manuscript. The AAIR edition carries the author block, so no
  separate title page is made.

## 5. Zenodo advice: is citing 0.8.0 healthy?

Checked 2026-10-21: `10.5281/zenodo.23142429` resolves; the record is version 0.8.0,
published 2026-10-04, under the concept DOI `10.5281/zenodo.19297723`.

**Yes, keep citing 0.8.0.** It's the snapshot of the code and data that produced every
number in Paper E, and the conversion changes no result. A version DOI is the right
citation for reproducibility. A new release would only add a snapshot whose code is
identical for Paper E, and it would make two Zenodo records carry the paper. Optional:
also mention the concept DOI in the data-availability sentence, so readers can find the
latest version. Revisit only if the AAIR review asks for a new analysis.

## 6. Steps, commits and pull requests

1. Lane commit: this plan, the README status (withdrawn from CyS), the three journal
   files. PR 1 to `main`.
2. Shared commit on `pubs/paper-e-aair-registry`: register the new document in
   `pub/claim_registry.toml` and `[coverage]`; record the venue change in
   `docs/context/ACTIVE_CONTEXT.md`. Its own PR, merged in this session.
3. Lane commits: `paper_e_aair.tex` (impersonal voice; abstract at 250 words or fewer;
   English and Turkish titles; ethics sentence; declaration of interest; the reference
   form), then the builder.
4. Build the manuscript and a PDF check copy. Checks:
   - every row of section 3, in `word/document.xml` and not by eye;
   - page count, float count, abstract word count;
   - `verify_claims.py`, `verify_sync.py`, `verify_exp4_reconstruction.py`,
     `check_equations.py`.
5. Cover letter and copyright form, then PR 2 to `main`.
6. The author adds the three reviewers, signs, runs the similarity report and submits.
   The record goes into `AAIR_SUBMISSION.md`, the README and ACTIVE_CONTEXT.

## 7. Question for the author

Section 2: **Option T** (template file plus the page's limits, recommended) or **Option
P** (page text exactly)?
