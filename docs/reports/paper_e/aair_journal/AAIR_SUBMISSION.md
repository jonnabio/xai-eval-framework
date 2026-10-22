# Paper E: submission sheet for *Advances in Artificial Intelligence Research* (AAIR)

**Journal:** *Advances in Artificial Intelligence Research* (AAIR), DergiPark, ISSN 2757-7422.
Open access, CC BY-NC 4.0. Writing rules: <https://dergipark.org.tr/en/pub/aair/writing-rules>
(read 2026-10-21). Price policy: "No fee is charged from the author or institution under any
name."

**Status: READY, NOT SUBMITTED** (2026-10-21). Still to do: the three reviewer nominations,
the author's signature on the copyright form, the similarity report and the submission
itself (section 4).

Paper E was withdrawn from *Computación y Sistemas* (submission 6783), as reported by the
author on 2026-10-21; see `../README.md`. The CyS edition (`../paper_e_template.tex`,
`../paper_e.tex`, `../submission/`) is kept unchanged as the record of that submission. Plan
and decisions: `docs/planning/paper_e_aair_plan_2026-10-21.md`.

## 1. The journal's two specifications, and the one followed

The writing-rules page and the template file linked from it disagree: two columns, Cambria
9 pt and no header on the page; one column, Times New Roman 10 pt and a journal header in
the template, and in the articles the journal publishes (Vol. 5 No. 2, 2025). **The author
chose the template file (Option T, 2026-10-21)**, with every limit of the page that can
apply. The cover letter says so in one paragraph.

## 2. Requirements, checked on the built files

| Requirement | Source | This edition |
|---|---|---|
| Research article: at most 15 pages | page | 14 pages in Word (the build stops above 15) |
| At most 10 figures and tables combined | page | 6 tables + 4 figures = 10 (checked by the build) |
| At most 60 references | page | 25, each with its DOI link, except two proceedings that have no DOI (AISTATS/PMLR 108, NeurIPS 30), which give the publisher's address |
| Abstract at most 300 words; about 100-250; no uncommon abbreviations or citations | page | 249 words (the build stops above 250); no citations |
| 3-6 keywords | page | 6; "Keywords:" bold, the first capitalised, separated by semicolons, ending in a period (template) |
| Title in English and Turkish, 14 pt, centred | page | Both. The Turkish title is the author's translation; the letter says the author does not speak Turkish and asks the office to correct it |
| Author names: initials capitalised, surname in capitals; affiliation lines with e-mail | page | "Jonathan HERRERA-VÁSQUEZ"; affiliation, e-mail and ORCID (template) on one line |
| Abbreviations spelled out at first use | page | SHAP, LIME, DiCE and RQ spelled out in the Introduction; the model abbreviations at first use in Section 3.1; all listed in the Nomenclature |
| Layout: A4, single column, Times New Roman 10 pt, justified, first-line indent 0.5 cm | template | The template's section settings, styles and paragraph formats |
| Headings "1. Title", "1.1. Title", bold | template | As required |
| Equations: left-justified, number in parentheses at a right tab; cited "Eq. (1)" | template | Two equations, Word equations (OMML), each cited as Eq. (n) |
| Figures: centred, caption below, "Figure 1." bold and italic caption; colour note | template | As required, with "(Figure is in color in the on-line version of the paper)"; 600 dpi images of the figures of `../scripts/build_paper_e.py` |
| Tables: caption above, "Table 1." bold and italic caption; no borders; rules above and below | template | As required |
| References cited [1], [2], [5] and [3]-[9], numbered by first appearance | page | As required; generated from `../references.bib` |
| Reference form | template ("IEEE", with the template's examples) | Template's form: "Surname AB. “Title”, Journal 11(2) (2008) 123-131; doi: …" |
| Hyperlinks underlined, body font | page | The template's hyperlink style |
| Header and footer | template | Running head "Herrera-Vásquez / AAIR vol (20yy) p-p" and the corresponding author's e-mail filled in; the journal's volume, pages, DOI and dates left for the journal |
| Declaration of interest, Nomenclature | template | Both included |
| Ethics committee permission if required | page | Not required; Ethics Statement section in the manuscript |
| Similarity report, at most 20% | page | To run before submission (section 4) |
| Cover letter with three reviewers | page, cover-letter template | `submission/paper_e_aair_cover_letter.docx`; reviewer slots left empty for the author |
| Copyright transfer form | page | `submission/paper_e_aair_copyright_form.docx`, filled in, to sign |
| Blind review | not required | The manuscript carries the author block, as the template does |

## 3. Files

| File | Role |
|---|---|
| `paper_e_aair_template.tex` | **The source.** Edit this. Every number is a placeholder of the `paper_e` resolver |
| `paper_e_aair.tex` | Generated: the text with every number resolved; under `[coverage]` in `pub/claim_registry.toml` |
| `scripts/build_paper_e_aair_docx.py` | Builds everything below and registers the numbers (generated `paper_e_aair` block of the registry) |
| `journal_files/` | The journal's three files as downloaded on 2026-10-21 (manuscript template, cover-letter template, copyright form). Local only, not redistributed |
| `submission/paper_e_aair_manuscript.docx` | The manuscript (tracked); `.pdf` is Word's print for checking (local only) |
| `submission/paper_e_aair_cover_letter.docx` | The cover letter (tracked) |
| `submission/paper_e_aair_copyright_form.docx` | The copyright form, filled in, to sign (tracked) |

Build (Word must be installed and the three journal files present):

    .venv\Scripts\python.exe docs/reports/paper_e/aair_journal/scripts/build_paper_e_aair_docx.py

Close the .docx files in Word first. After a build, run `scripts/pubs/verify_claims.py` and
`scripts/pubs/register_paper_c.py --check` (the Paper C block must stay last in the registry).

## 4. Before submission (author)

1. Fill in the three reviewer nominations in the cover letter.
2. Sign the copyright form and the cover letter; fill in the submission date.
3. Register on DergiPark as an author and, as the template asks, as a reviewer.
4. Run the similarity report (at most 20%). The Zenodo archive of the earlier version
   (`10.5281/zenodo.23142429`) may match; the letter says so.
5. Submit at <https://dergipark.org.tr/en/pub/aair>; record the date and the submission
   number here, in `../README.md` and in `docs/context/ACTIVE_CONTEXT.md`.

## 5. Data and archive

The manuscript cites the Zenodo release 0.8.0 (`10.5281/zenodo.23142429`), the snapshot
of code and data that produced every number; the conversion changes no result, so no new
release was made (plan, section 5).
