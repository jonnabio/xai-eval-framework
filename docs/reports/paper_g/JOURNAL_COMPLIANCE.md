# Paper G — journal compliance (Informática y Sistemas)

**Date:** 2026-11-16. **Checked file:** `submission/paper_g_blind.docx`, built by
`scripts/build_paper_g.py` from `paper_g_draft.md` with the journal's article template
(`venue/template/IyS_article_template.docx`, downloaded on 2026-11-16 from the journal's
"Templates and Forms" page; SHA-256 `57f404248d35fe24…`) as the style reference, and
`submission/paper_g_blind.pdf` rendered from it by LibreOffice for the page count. Rules from
`VENUE.md` (journal site, 2026-11-13) and from the template's own guidelines.

| Requirement | Source | Status | Evidence / action |
|---|---|---|---|
| English | VENUE | Pass | Whole manuscript in English |
| 8 to 16 pages including references | VENUE | Pass | 12 pages (LibreOffice rendering of the .docx; Word may differ by a page) |
| Abstract 150 to 250 words, one paragraph | VENUE, template | Pass | 203 words, one paragraph, template style "Abstract" |
| 3 to 5 keywords, separated by semicolons | VENUE, template | Pass | 5 keywords, template style "Keywords" |
| Journal .docx template | VENUE, template | Pass (styles) / author check | Built on the template's styles, page set-up, header and footer; title, article type, abstract, keywords, headings, body, captions, source lines, tables ("Journal Table", horizontal rules only) and references use the template's styles. The author should open the file in Word once to confirm pagination and equation rendering (built and checked with LibreOffice) |
| Section order: numbered Introduction, Materials and methods, Results and discussion, Conclusions; then unnumbered Funding, Author contributions, Conflicts of interest, Data availability statement, Declaration of generative AI use, References | Template B | Pass | Related work is subsection 1.1 of the Introduction; Acknowledgments omitted for blind review |
| Headings capitalise only the first letter | Template B | Pass | |
| Figures numbered, mentioned in text, caption below, centred, ending with a period, source line | Template C | Pass | Five figures, each cited before or where it appears; "Source: Authors." under each |
| Figures as separate files, 600 dpi for charts | Template A | Pass | `submission/Figure_1.png` … `Figure_5.png` (600 dpi) and `.svg`, numbered as in the text |
| Tables numbered, title above, centred, ending with a period, horizontal lines only, source line, header row repeats | Template C | Pass | Four tables; pandoc marks header rows to repeat |
| Equations numbered on the right in parentheses, cited as "Equation (1)" | Template C | Pass | Five equations, each cited |
| APA 7 references, DOI where available, every reference cited | VENUE, template | Pass | 50 references rendered by the APA 7 CSL style (`venue/csl/apa.csl`, updated 2026-02-07); 42 with DOI, 5 peer-reviewed papers without a DOI (NeurIPS 2017 and 2019, TMLR, ICLR) given by their proceedings or OpenReview URL, 3 anonymised own manuscripts; all 50 cited (`REFERENCE_VERIFICATION.md`) |
| At least 10 references; at least 90% scientific articles | Template | Pass | 50; 46 of 50 (92%) journal articles, conference papers or chapters; 1 preprint; 3 anonymised own manuscripts |
| Project rule: at least 80% of references from 2024 onward | Project | Pass | 84% (83% excluding own manuscripts) |
| Double-blind: no names, affiliations, acknowledgements; own work in third person | VENUE, template A | Pass, with an author decision | No names in text or document properties (core.xml creator empty); own earlier manuscripts cited as anonymised entries; repository identifier withheld. **The repository holding the manuscript source is public** (see below) |
| Required declarations | VENUE, template | **Author action** | All five present; Funding, Conflicts of interest and the AI declaration carry bracketed text for the author to confirm; Author contributions withheld for review (CRediT roles at acceptance) |
| Declaration of generative AI use: tool, version, provider, purpose, sections | Template | Drafted; **author to confirm** | Names Claude (Anthropic; model identifier claude-opus-5-5), Claude Code, purposes and sections |
| At most 10% similarity, at most 30% AI-generated content (Compilatio) | VENUE | **Not verifiable here; author-owned risk** | The text was drafted by the assistant (decision of 2026-11-13: the author owns the AI-content limit). Unless the author rewrites substantial parts, the manuscript is likely to exceed the 30% AI-content limit and be returned without review |
| Response-to-reviewers form | Template | n/a | Only for revisions |

## Remaining corrections before submission (author)

1. Rewrite the text in the author's own words to the extent needed for the 30% AI-content limit; then
   rebuild (numbers are re-inserted from the result files and re-verified, so rewriting cannot
   introduce a wrong number unnoticed).
2. Confirm or replace the bracketed declarations (Funding, Conflicts of interest, AI use).
3. Decide on the public repository during review: the source `paper_g.md` and the built files are
   on the public GitHub repository under the author's account, which a reviewer could find by the
   title. Options: accept (many journals allow it; the journal's policy on preprints was not found
   on its site), or make the Paper G files private until acceptance.
4. Open `submission/paper_g_blind.docx` in Word to confirm pagination, equations and the table header
   repeat; at acceptance add the author block, CRediT roles, the Zenodo DOI and the published records
   of the earlier papers of the programme.

**JOURNAL COMPLIANCE: PASS** for the formal requirements checked here, with the author actions above
(declarations, AI-content limit, public repository) before submission.
