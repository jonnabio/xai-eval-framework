# Paper F — Venue: Journal of Computer Sciences Institute (JCSI)

**Venue chosen by the author on 2026-10-05.**
Journal of Computer Sciences Institute (J. Comput. Sci. Inst.), Lublin University of
Technology, Poland. ISSN 2544-0764 (online). Site: <https://ph.pollub.pl/index.php/jcsi>.
Rules read on 2026-10-05 from the journal's pages *Submissions*, *About the Journal*,
*Ethical principles* and from its 2025 paper template. Read them again before submitting.

---

## 1. Rules of the journal

| Item | Rule |
|---|---|
| Language | English only (from 2026) |
| Length | **Not shorter than 4 and not longer than 8 pages**, in the journal template |
| Template | The 2025 template, DOCX. A4, two columns of 8 cm with 1 cm between, margins 2.5 cm top and bottom and 2 cm left and right, Times New Roman 10 pt, single spacing, justified, hyphenation on. Only the styles of the template. |
| Files to send | The source as `surname_of_corresponding_author.docx` and a matching PDF, through the journal site |
| Title block | Title; authors with ORCID if available; affiliation; corresponding author's email |
| Abstract | **At most 800 characters, spaces included** |
| Keywords | 3 to 6, separated by semicolons |
| Section 1 | Introduction (may have 2 or 3 subsections): literature review, purpose of the research, research areas **and the hypothesis** |
| Section 2 | Materials and methods: the object of the research, the method, the research carried out, the scenarios |
| Section 3 | Selected results: tables, graphs, the most important results |
| Section 4 | Discussion and conclusions: the results discussed **against the hypotheses of the Introduction**, comments, possible sources of error, the new and most important results, **2 or 3 original conclusions**, directions for further research |
| Acknowledgements | Optional, at the end, before the references |
| Figures | Centred in the column, caption below; a figure may span the page. Good quality, embedded. Each needs an alternative description (the submission page asks for the journal's rules on alternative descriptions to be followed) |
| Tables | Numbered, title above, the Table style; font at most 2 pt smaller than the text; a table may span the page |
| Formulae | Numbered at the right margin; variables in italics, vectors bold, constants upright |
| References | Numbered in square brackets in order of first citation. Format of the template, for example: `A. Sutton, L. Tompson, Title, Computers & Security 148 (2025) 104110, https://doi.org/...`. DOI links active. A web page: short description, address, date of access in brackets |
| Originality | Not published elsewhere and not under consideration by another journal |
| Conflict of interest | The authors certify there is none; any possible conflict is reported to the editors |
| Generative AI | Not an author. **Any use in the research or in the writing is disclosed in the manuscript** (Methods, Acknowledgements or a dedicated declaration) **and in the submission system, with the name of the tool** and the reason for using it |
| Citations | No excessive self-citation |
| Plagiarism check | Crossref Similarity Check (iThenticate) on every manuscript |
| Fees | None for submission or publication |
| Licence | CC BY 4.0; the author keeps the copyright |
| Review | The journal states double-blind peer review. The template carries the authors' names. **Open point:** whether the uploaded file must be anonymous; to be checked in the submission system or asked of the editors |
| Stated times | Initial assessment 1 to 2 weeks; review 1 to 4 weeks; publication 4 months |
| Issues | Four a year: 30 March, 30 June, 30 September, 30 December |

**What these rules mean for Paper F:**

1. **Eight pages** in two columns hold about 4,500 to 5,000 words with figures and tables.
   The sixteen-dataset study must be reported with one result table, one or two figures
   and the rest in an archive (Zenodo) that the paper cites.
2. The **abstract is about 120 words** (800 characters).
3. The paper states **one hypothesis in the Introduction** and returns to it in the last
   section with **two or three conclusions**.
4. **Self-citation:** Papers A to E are by the same author. Cite only those that are
   needed (the published Paper A for the framework), not all.
5. **Prior work in a public repository:** the plan, the code and later the results are
   public on GitHub and Zenodo. Say so in the comments to the editor.
6. **AI declaration:** required. The author writes it, as for Papers C and D.
7. The file name is the author's surname as the journal site accepts it.

---

## 2. Study of the journal: time from received to published

**What was done.** The 84 articles of the five latest issues (volumes 36 to 40, September
2025 to September 2026) were downloaded from the journal site and their first page was
read for the dates "Received" and "Accepted". The publication date is the date of the
issue. Data: `venue/jcsi_timing_vol36_40.csv`; scripts: `venue/jcsi_fetch.py`,
`venue/jcsi_analyze.py`. The counts of figures, tables and references come from pattern
matching on the extracted text and are approximate.

**Times (days), 84 articles:**

| Interval | Shortest | First quartile | Median | Third quartile | Longest |
|---|---|---|---|---|---|
| Received to accepted | 13 | 37 | 54.5 | 75 | 187 |
| Accepted to published | 44 | 79 | 107.5 | 138 | 239 |
| Received to published | 73 | 134 | 182.5 | 195 | 332 |

**Finding 1: the date of submission decides most of the time to publication.** Two thirds
of the total is the wait between acceptance and the next issue. The articles with the
shortest total time were received 10 to 14 weeks before an issue date and accepted in
about three to six weeks. In each issue, the last article accepted was accepted 44 to
101 days before the issue date; the last received, 73 to 176 days before.

**Finding 2: authors from outside the publishing university wait longer for acceptance.**
72 of the 84 articles are from Lublin University of Technology. For them the median from
received to accepted is 50.5 days; for the 12 others it is 68 days. For the six external
articles of 2026 it was 44 to 112 days.

**Finding 3: what the fastest third of the articles looks like** (28 articles, 73 to 144
days from received to published) against the slowest third (190 to 332 days):

| Feature | Fastest third | Slowest third |
|---|---|---|
| Pages, median | 7 | 7 |
| References, median | 9.5 | 7.5 |
| Figures, median | 6 | 9 |
| Tables, median | 4 | 3 |
| States a hypothesis | 21 of 28 | 14 of 28 |
| Title names a comparison | 18 of 28 | 10 of 28 |
| Reports a statistical test | 9 of 28 | 5 of 28 |
| From Lublin University of Technology | 26 of 28 | 21 of 28 |

These are associations in 84 articles, not causes. The differences in style are small
next to findings 1 and 2. They are still the profile the journal accepts quickly, and
they agree with the journal's own instructions.

**Closest published articles** (to read before writing):
- "Comparative analysis of interpretable artificial intelligence methods" (vol. 38, 2026,
  pp. 51-58): Grad-CAM, SHAP and LIME; 8 pages.
- "Comparison of classical machine learning methods in the task of obesity level
  classification" (vol. 40, 2026, pp. 304-312): states a research hypothesis, uses
  Wilcoxon and McNemar tests with Holm correction, SHAP and LIME; accepted in 54 days.
- "Comparative analysis of machine learning classifiers" (vol. 38, 2026, pp. 59-65):
  accepted in 19 days.

---

## 3. How Paper F is shaped for this journal

| Aspect | Decision for the manuscript |
|---|---|
| Title | Chosen by the author on 2026-10-05: *How Dataset-Dependent Are Tabular Explainability Benchmarks?* It does not name a comparison, as the faster articles of the journal more often do; the author preferred a short research question, and that association was weak. |
| Length | 7 to 8 pages in the template; measured in Word |
| Hypothesis | One, stated at the end of the Introduction (analysis plan, section 6) |
| Structure | The four sections of the journal, with these names |
| Tables and figures | About 4 tables and 3 to 5 figures at most; tables carry the numbers, figures show the ranking across datasets. Each figure has a committed generator and an alternative description |
| Statistics | Permutation tests and intervals, stated in one short paragraph of the methods |
| Conclusions | Three, numbered, each answering the hypothesis |
| References | 15 to 20, in the template's format, with DOI links; at most one or two of the author's own |
| Sources of error | A named paragraph in the last section, as the journal asks |
| AI declaration | A dedicated paragraph before the references; the author's text |
| Data and code | One sentence with the Zenodo DOI |

**Timing.** Today is 2026-10-05. The issue of 30 December 2026 is very likely closed: in
the three September and December issues studied, no article was received later than 98
days before the issue date, which for this issue was 23 September. Realistic targets:

| Issue | To have a good chance, be received by | Note |
|---|---|---|
| 30 March 2027 | end of November 2026 | external articles of 2026 took 44 to 112 days to acceptance; the last acceptances for a March issue were in mid December |
| 30 June 2027 | end of February 2027 | comfortable |

The run of the experiment takes about three days of computing after the code is ready, so
the March 2027 issue is reachable if the manuscript is sent in November.
