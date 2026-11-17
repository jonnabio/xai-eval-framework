# Paper G — journal compliance (Informática y Sistemas)

**Date:** 2026-11-16 (revised in Task 21). **Checked file:** `submission/paper_g_blind.docx`, built
by `scripts/build_paper_g.py` from `paper_g_draft.md` on the journal's article template
(`venue/template/IyS_article_template.docx`, from the journal's "Templates and Forms" page,
SHA-256 `57f404248d35fe24…`), and `submission/paper_g_blind.pdf` rendered from it by LibreOffice
for the page count. Rules from `VENUE.md`, the template's guidelines, and the journal's submission
page (Submission Preparation Checklist and Author Guidelines, read 2026-11-16).

## A. Checks done by the build (automatable)

| Requirement | Status | Evidence |
|---|---|---|
| English; official template | Pass | Template styles, page set-up, header and footer; title, article type, abstract, keywords, headings, captions, source lines, tables, references in the template's styles. Built and checked with LibreOffice; to be opened once in Word (part B) |
| 8 to 16 pages including references | Pass | 13 pages (LibreOffice) |
| Abstract 150 to 250 words, one paragraph; 3 to 5 keywords | Pass | 220 words; 5 keywords |
| Numbered sections in the template's order; declarations unnumbered in the template's order | Pass | 1 Introduction (1.1 Related work), 2 Materials and methods, 3 Results and discussion, 4 Conclusions; Funding, Author contributions, Conflicts of interest, Data availability statement, Declaration of generative AI use; references |
| Figures: numbered, cited, caption below, source line; separate files, 300 dpi or vector | Pass | 5 figures; `submission/Figure_N.png` (600 dpi) and `.svg`, named by their number |
| Tables: numbered, cited, title above, horizontal rules only, source line, repeated header | Pass | 4 tables, "Journal Table" style |
| Equations: numbered on the right, cited as "Equation (N)" | Pass | 5 equations, each cited; each checked against the frozen code (`verification/verify_equations_output.txt`, 480 checks, 0 disagreements) |
| APA 7, DOI where available, every reference cited | Pass with exceptions | 50 references, all cited; 42 with DOI; exceptions in `REFERENCE_VERIFICATION.md` (5 peer-reviewed without DOI, 1 preprint, 3 anonymised own manuscripts, 1 article assigned to an issue dated 2027) |
| At least 90% scientific articles (template) | Pass | 46 of 50 (92%) |
| Project rule: at least 80% from 2024 onward | Pass | 84% (83% without own manuscripts) |
| No identifying information in the file | Pass | No names, affiliations, emails or acknowledgements in the text; document properties carry no author; own work cited as anonymised entries; repository identifier withheld |
| Every number traceable to the result files | Pass | Claim registry, `register_paper_g.py --check`, `verify_claims.py` |

## B. Submission components (author only; not automatable)

| Component | Journal requirement | Status |
|---|---|---|
| Anonymised manuscript (.docx) | Upload in OJS | Built (`submission/paper_g_blind.docx`); author to open in Word once and upload |
| Figures as separate files | Upload, named Figure_N | Built (`submission/Figure_1` … `Figure_5`) |
| Submission checklist | Accepted online in OJS; no file to upload | Author: all items in `AUTHOR_REVIEW_CHECKLIST.md`, section 4 |
| Publication agreement | No separate signed agreement: the copyright notice (CC BY-NC-ND 4.0) and the authors' declarations (originality, approval, licence) are accepted in the OJS form | Author |
| Author metadata and ORCID; Supporting Agencies field; keywords one by one; language | OJS form | Author |
| Required declarations in the manuscript | Funding, Author contributions, Conflicts of interest, Data availability, Declaration of generative AI use, completed even when "none" | **Pending:** Funding, Conflicts of interest and the AI statement carry bracketed text only the author can complete; Author contributions withheld for review |
| AI-content (30%) and similarity (10%) limits, Compilatio | Over either limit, returned without review | **Author-owned risk:** the text is assistant-drafted; see `AUTHOR_REVIEW_CHECKLIST.md`, section 2 |
| Ethics approval | Only if human participants or personal data | Public de-identified benchmark data, no participants; author to confirm no approval is required |
| Supplementary material | Optional at submission; any requested by the editor | None prepared; code and results are in the repository (identity-revealing; see part C) |
| Response-to-reviewers form | Only for revisions | n/a |

## C. Double-blind risk (unresolved)

- The manuscript source (`docs/reports/paper_g/paper_g_draft.md`, since 2026-11-13), the rendered
  manuscript, the built .docx and the analysis plan are in the **public** GitHub repository
  `jonnabio/xai-eval-framework`; its commit history carries the author's full name and email.
  A reviewer who searches the title or distinctive phrases can find the author.
- Deleting or moving the files would not remove them from the public history, forks, clones or
  caches. Changing the repository's visibility or rewriting its history needs the author's
  authorisation and was not done.
- The journal's pages do not state a preprint or public-repository policy.
- **Options for the author:** (1) disclose to the editor at submission that a working version is in
  a public repository and ask whether that is acceptable; (2) make the repository private during
  review (this does not reach existing copies); (3) accept the risk. The choice is the author's.

**JOURNAL COMPLIANCE:** the automatable checks pass (part A); the submission components of part B
and the double-blind decision of part C are author actions.
