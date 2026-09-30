# Editorial Compliance Assessment: TintAzul / CIFIE

**Date:** 2026-09-30

**Documents reviewed (this folder):** `GUÍA-PLANTILLA.docx`, `CHECKLIST DEL AUTOR.docx`,
`RÚBRICA OFICIAL DE EVALUACIÓN EDITORIAL.docx`, `GUÍA RÁPIDA DE NORMAS APA.docx`,
`DECLARACIÓN DE AUTORÍA.docx`, `LICENCIA DE PUBLICACIÓN Y CESIÓN LIMITADA DE DEREC.docx`.

**Assessed against:** chapter branch at `a1edb8bf4` (sections 01-11 as built on
2026-09-29, Word render 83 pages, about 20,900 source words).

**Verdict:** not yet compliant. The content and APA base are close; the gaps are the
template format, the front-matter data, three structural conventions, the figure
mentions, the keyword count, and four author decisions (length, AI-use declaration,
authorship, prior publication). All items are merged into the pending list of
`planning/science_first_revision_plan_2026-09-28.md` ("Consolidated pending list").

## 1. What the documents require

The six documents set requirements at four levels. None states a word limit, a font
list or margins in prose; the format is defined by the template file itself, and the
checklist requires "la plantilla oficial", "la tipografía establecida", "el
interlineado", "márgenes y estilos", "la jerarquía indicada" and "la extensión ...
[de] los lineamientos editoriales".

### 1.1 Format, read from `GUÍA-PLANTILLA.docx` (verified in the XML and a Word render)

| Element | Template value |
| --- | --- |
| Paper | A4 (21.0 x 29.7 cm) |
| Margins | top and bottom 2.54 cm; left and right 3.17 cm; header and footer 1.27 cm |
| Typeface | Cambria 12 pt for all text, headings included (applied as direct formatting; the underlying styles carry unused SimSun defaults) |
| Line spacing | 1.5 |
| Alignment | justified body text |
| Heading hierarchy | level 1 bold uppercase (RESUMEN, PALABRAS CLAVE, INTRODUCCIÓN, CONCLUSIONES, REFERENCIAS); levels 2-3 bold, sentence case; all at 12 pt |
| Header | TintAzul logo anchored top right, plus a three-line label ("Guía-Plantilla / Libro Colectivo CIFIE / TintAzul – Editorial Académica y Estratégica") |
| Page numbers | none in the template |

### 1.2 Structure and content (template, checklist III-IV, rubric II-III)

- **Portada:** chapter title (clear, specific, informative); full author name; academic
  degree; institutional affiliation; ORCID; e-mail, for each author.
- **Hoja de diseño editorial:** planning aid, "no se publicará"; includes a *Tipo de
  capítulo* choice (empirical research, literature review, academic essay, case study,
  educational innovation, systematization, other).
- **Resumen:** 150-250 words, answering: topic, importance, purpose, development,
  main contribution, conclusion; written last.
- **Palabras clave:** three to five, disciplinary terms, avoiding literal repetition of
  the title.
- **Introducción:** general context, problem or need, brief state of knowledge, gap,
  objective ("El propósito de este capítulo es..."), organization of the chapter.
- **Desarrollo:** informative subtitles (generic headings such as "Marco teórico",
  "Desarrollo" or "Resultados" are discouraged); each section answers a different
  question; each paragraph has one main idea, explanation, evidence, interpretation and
  transition; no overlong paragraphs.
- **Conclusiones:** interpretation, not summary; must answer what the chapter
  contributed, what was learned, implications, limitations and future research.
- **Referencias:** APA 7; every citation listed and every reference cited; complete
  data; DOI when available; alphabetical order.
- **Anexos:** only when indispensable.

### 1.3 Tables, figures and citations (template, APA guide, checklist VI)

- Every table and figure: numbered consecutively, clear title, source stated,
  **mentioned in the text before it appears**, relevant (no decorative figure), and not
  duplicating information already explained.
- Citations: combine narrative and parenthetical forms, paraphrase and critical
  dialogue; "y" in narrative citations and "&" inside parentheses (guide examples);
  "et al." from the first citation for three or more authors.
- Common errors to avoid: uncited references, citations without reference, wrong dates,
  inconsistent "&"/"y", incomplete DOI, broken URLs, unsorted references, missing
  italics, wrong "et al.".
- Reference model in Spanish: book chapters as "En A. Editor (Ed.), *Título* (pp.
  xx-xx). Editorial."

### 1.4 Ethics and legal forms (declaration, licence, checklist I)

- Original and unpublished work; any prior publication, total or partial, must be
  stated explicitly and authorized.
- Not under simultaneous consideration elsewhere.
- Every listed author made a substantial intellectual contribution and approves
  submission; nobody omitted.
- AI use: either none, or **auxiliary tasks only** (grammar, style, preliminary
  organization of ideas, language correction, initial translation, other: specify),
  with commitments that all intellectual decisions, analysis, interpretation and
  conclusions are the authors', that no result or reference was generated by AI, and
  that everything was verified.
- Conflicts of interest declared.
- Licence: non-exclusive publication licence to CIFIE and TintAzul; authors keep moral
  rights and may reuse with citation; editorial (not scientific) changes allowed; ISBN
  and possible chapter DOI.
- Deliverables to sign: author checklist, authorship declaration, licence.

### 1.5 Evaluation rubric (100 points)

Pertinence and contribution 20 (contribution alone 10); scientific rigor 25
(argumentation alone 10); organization 20; writing 20; editorial aspects 15 (template
compliance 5, APA 5, overall editorial quality 5). Global coherence among title,
abstract, objective, development and conclusions is scored explicitly.

## 2. Compliance status of the current chapter

Status: **OK** compliant; **Gap** work needed; **Decision** requires the author or
the editor.

| # | Requirement | Status | Evidence in the current chapter | Action (pending-list ID) |
| --- | --- | --- | --- | --- |
| 1 | A4, margins 2.54/3.17 cm | Gap | Section properties define no page size or margins; Word renders Letter | E-FMT |
| 2 | Cambria 12 pt throughout | Gap | Theme fonts (sans serif) at 12 pt body; headings 20/16/14 pt | E-FMT |
| 3 | Headings bold 12 pt; level 1 uppercase | Gap | Pandoc heading styles, larger sizes, sentence case | E-FMT |
| 4 | 1.5 spacing, justified | OK | All 462 paragraphs at 1.5; body, captions, notes, references justified | Keep |
| 5 | Header with TintAzul logo and label | Decision | No header content | E-Q1 (ask whether authors reproduce it) |
| 6 | Portada: degree, ORCID, e-mail per author | Gap | Only name and affiliation rendered; Herrero-Uceda ORCID "pendiente"; no degrees or e-mails | E-FRONT, E-AUTH |
| 7 | Hoja de diseño: template fields, chapter type | Gap | `00_hoja_diseno_editorial.md` predates the new title and describes the old empirical-only chapter | E-FRONT; E-Q1 (is it submitted?) |
| 8 | Resumen 150-250 words answering six questions | Gap | Current abstract describes the pre-revision chapter (no applications, no gaps) | P-FINAL (rewrite last) |
| 9 | Three to five keywords, not repeating the title | Gap | Six keywords; the first ("Inteligencia artificial explicable") repeats the title | P-FINAL |
| 10 | Visible "Introducción" with the six template elements | Gap | Section 02 is titled "Por qué importa la inteligencia artificial explicable"; it has context, problem and roadmap, but no explicit "El propósito de este capítulo es..." sentence and no labelled state-of-knowledge/gap step | E-STRUCT |
| 11 | Informative development headings | OK | Sections 03-10 use descriptive titles; no generic "Resultados" | Keep |
| 12 | Conclusions answer five questions incl. limitations and future work | Gap | Section 11 states contribution and scope; limitations and agenda live only in section 10 | E-STRUCT, P-FINAL |
| 13 | Tables numbered, titled, sourced, mentioned first | OK | Tables 1-4 consecutive, APA title and *Nota.* with source, each cited before its marker | Keep |
| 14 | Tables do not duplicate text | Gap | Table 4 repeats statistics also printed in section 08 prose | P-CASE (compression) |
| 15 | Figures mentioned in text before they appear | Gap | Figure 1 is; **Figures 2-6 are never mentioned in the text** | E-FIG |
| 16 | Figures numbered, titled, sourced, not decorative | Partial | Numbered with source in caption; captions not APA-formatted; Figures 5-6 have no stated inference; Figure 1 and Figure 4 legend illegible in grayscale | E-FIG, R5 |
| 17 | Every reference cited / every citation listed | Gap | Adadi and Berrada (2018) and Belle and Papantonis (2021) uncited; no citation lacks a reference | R6 |
| 18 | Complete, correct metadata; DOI when available | Gap | Barredo Arrieta 2020, Becker and Kohavi dataset DOI, Lundberg and Lee NeurIPS, Schwalbe and Finzel 2024 (review M7) | R6 |
| 19 | Spanish reference conventions | Gap | 14 entries use English connectors ("In", "Article", "[Doctoral dissertation]", "[Data set]"); the CIFIE model uses "En" | E-APA |
| 20 | "y" narrative, "&" parenthetical | OK | No narrative "&" found; recheck at final audit | R6 |
| 21 | Alphabetical references | OK | 59 entries in order | Keep |
| 22 | Paragraph discipline, no overlong paragraphs | Gap | Many paragraphs exceed ten rendered lines in sections 05-07 | P-CASE, R4 |
| 23 | Length within the editorial guideline | Decision | No limit stated in any document; chapter about 20,900 words; working range 14,000-16,000 | E-Q1 (limit), then P-CASE |
| 24 | Original and unpublished; prior publication stated | Decision | H1-H2 statistics come from the published RIMI article (CC BY-NC-SA 4.0); cited in text, but must also be declared in the authorship form | E-PRIOR |
| 25 | No conflict with other submissions | Decision | Table 4 and section 08 state the direction of the paired SHAP-LIME contrast (H3) and the 15/15 block analysis, which belong to the Paper B+C line; an archival chapter (ISBN, possible DOI) may count as prior publication under TMLR's policy | E-PRIOR |
| 26 | Authorship and signatures | Decision | Herrero-Uceda is listed as co-author; his contribution, consent and signature are required on the declaration and licence | E-AUTH |
| 27 | AI-use declaration truthful | Decision | The form admits only auxiliary AI use and requires that analysis, interpretation and conclusions be the authors'. The commit history records AI co-authorship on the drafting of section 04 (`e4005b2a9`), the R1-R2 revisions and earlier revisions of every section from 02 to 11 since July 2026 (between one and five attributed commits per section); the latest rewrite of sections 02-03 (`7a475e7fe`) carries no attribution. `compliance/ai_use_declaration.md` states auxiliary use only | E-AI |
| 28 | Author checklist, declaration and licence signed | Gap | Forms not yet completed | E-FORMS |

## 3. Decisions and questions

### 3.1 Questions for the editor (E-Q1)

1. Maximum and minimum length, in words or pages, and whether references count.
2. Whether authors should submit on the template file itself, including the header
   logo and label, or whether the header is added by the publisher.
3. Whether the *Hoja de diseño editorial* is submitted with the chapter.
4. Figure requirements for print: colour or grayscale, minimum resolution, file format.
5. Submission format (Word only, or Word plus PDF) and deadline.
6. Whether a chapter drawing on results already published elsewhere (with citation) is
   acceptable, and what authorization is expected.

### 3.2 Author decisions

- **E-AI:** decide how AI use will be declared so that the form can be signed truthfully:
  either declare it under "otra (especificar)" with an accurate description of drafting
  assistance and author verification, or rewrite the AI-drafted passages so that only
  auxiliary use remains. The declaration's commitment that analysis, interpretation and
  conclusions are the authors' must hold as signed.
- **E-AUTH:** confirm Dr. Herrero-Uceda's contribution and consent, obtain his ORCID,
  degree and e-mail, and his signature on the declaration and licence; or remove him
  from the byline.
- **E-PRIOR:** (a) declare the RIMI prior publication of the H1-H2 results in the
  authorship form; (b) decide whether the chapter keeps the direction of H3 and the
  15/15 block analysis while Paper B+C is under TMLR review, or reports only published
  and thesis-level statements that do not anticipate Paper B+C; if kept, align the
  timing with the TMLR editors.
- **E-TYPE:** choose the *Tipo de capítulo*; the current chapter is a scientific
  synthesis with a methodological proposal and a bounded empirical case ("Otro" with a
  one-line description, or "Investigación empírica").

## 4. What already complies

1.5 line spacing, justified body, informative development headings, four APA-style
tables with sources, DOI coverage, alphabetical references, consistent "&"/"y",
no uncited-citation gaps, traceable numbers (RCA-001 registry), no decorative
tables, and an explicit scope statement for the empirical case. The rubric's weighted
criteria (contribution, argumentation, coherence) are addressed by the
science-first plan already in progress.
