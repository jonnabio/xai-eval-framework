# Paper D — claim-registry case study

**Working title:** *Verifiable result traceability in AI research: a claim registry that links
published numbers to their artifacts* (Spanish title in the manuscript).

**Target:** *Tecnología en Marcha* (Editorial Tecnológica de Costa Rica), special issue on
Artificial Intelligence. ESCI, SciELO, DOAJ; diamond open access, no fees.
**Deadline: 15 October 2026**, by email to revistatm@tec.ac.cr (special-issue call); the issue
is published in February 2027. **Status (2026-10-03):** first complete draft; not submitted.

## Why this paper is separate from Papers A and B+C

Paper D reports the *method* the project used to keep its manuscripts correct (the claim
registry and its checks) and a case study of the defects it found. It prints no scientific
result of Paper A (published, RIMI) or Paper B+C (under review at *Inteligencia
Artificial*). This is enforced: `paper_d.tex` is in the registry's `[exclusivity]` list, so the
build fails if a Paper B+C result appears in it, and in `[coverage]`.

## Journal requirements (author guide, checked 2026-10-03)

Source: "Instrucciones para publicar"
(https://revistas.tec.ac.cr/index.php/tec_marcha/libraryFiles/downloadPublic/6) and the
submission page.

| Requirement | Journal rule | Paper D |
|---|---|---|
| Originality | Original, unpublished, not in another process at the same time | Yes; no overlap with A or B+C (exclusivity check) |
| Structure | Title, abstract, keywords (English and Spanish); introduction; materials and methods; results; conclusions and/or recommendations; references; acknowledgments | Yes, plus a Discussion section and a Data availability statement |
| Length | 5–15 pages, 8.5 × 11 in | **12 pages in Word**, including references (author target) |
| File | Microsoft Word, one column, 1.5 line spacing, Times 12 pt | `submission/paper_d_blind.docx` (Times New Roman 12 pt, 1.5, letter, 2.5 cm margins) |
| Titles | Simple, clear, short; Spanish and English | Both |
| Authors | Full name with both surnames, profession, email, workplace (institution, department), country, **ORCID** | In `paper_d_full.docx`; **ORCID is a placeholder: [AUTHOR]** |
| Abstract | Spanish and English, at most 250 words | English 214, Spanish 238 words (measured in the Word file) |
| Keywords | Spanish and English | Both |
| Images | Inside the document **and** as separate files; .jpg, .tiff, .eps, .psd or .ai; 300 ppi if raster | `submission/Figure1-3.tiff`, 300 ppi |
| Equations | Microsoft Office equation editor or MathType | Native Word equations (pandoc writes Office Math) |
| Units | SI where relevant | n/a |
| References | IEEE, at the end | IEEE (`IEEEtran` in LaTeX; `ieee.csl` in Word) |
| Review | Double-blind, two external reviewers | `paper_d_blind.docx` omits identity; the full file goes to the editor |
| Language | Spanish mainly; English accepted | English (author decision) |
| AI policy | Prohibits AI-plagiarised ideas or autonomously AI-written papers | Ideas and direction are the author's; AI assistance disclosed in the Acknowledgments |

## Files

| Path | What it is |
|---|---|
| `paper_d.tex` | The manuscript source (LaTeX, set to the journal's page) |
| `references.bib` | References; DOI entries fetched from doi.org and verified against Crossref |
| `ieee.csl`, `reference_default.docx` | IEEE citation style and pandoc's base Word template, used to build the .docx |
| `figures/` | `fig1_architecture.tex` (TikZ) and the generated figures as .pdf, .png and .tiff |
| `submission/` | Generated: `paper_d_blind.{docx,pdf}`, `paper_d_full.{docx,pdf}`, `Figure1-3.tiff` |
| `outputs/analysis/paper_d/` | The case-study data: registry snapshot and growth, incident catalogue and summary, CI export and summary |

## Build

```bash
python scripts/pubs/paper_d_metrics.py          # case-study data (pinned commit 124a7db4c)
python scripts/generate_paper_d_figures.py      # Figures 1-3 (.pdf, .png, .tiff)
python scripts/pubs/build_paper_d.py            # PDFs, Word files, figure uploads
python scripts/pubs/verify_claims.py            # every number in paper_d.tex re-derives
```

`build_paper_d.py` fails on any undefined reference or citation. The Word length is
measured with Word itself: open `submission/paper_d_blind.docx` and check the page count.
On 2026-10-03 it was 12 pages (blind and full).

## Every number is registered

Paper D's numbers come from `outputs/analysis/paper_d/` through the `paper_d:` resolver in
`scripts/pubs/claim_sources.py`, and each one is a claim in `pub/claim_registry.toml` (ids
`paper_d.*`). The registry figures describe the registry as it stood at commit `124a7db4c`,
read from git, so they do not change as the registry grows.

## Open items before submission

1. **[AUTHOR] ORCID**: replace `[ORCID]` in `paper_d.tex` (full version only).
2. **[AUTHOR] Profession** line: "Computer scientist" is a placeholder; confirm.
3. **[AUTHOR] References**: the AI assistant proposed them. All 19 were verified against
   their DOI records or the publisher page, but the author must read and approve each one. The
   Acknowledgments say so.
4. **[AUTHOR] Incident catalogue**: the coding (`incident_catalogue.csv`) was a first pass
   by the AI assistant from the review records; the author must check every row, especially
   the `caught_now` column, before submission.
5. **[AUTHOR] Spanish title and Resumen**: native read.
6. Scientific-rigor review of the draft (Scientific Advisor), then fixes.
7. Submission email: blind .docx, full .docx (title page data for the editor),
   Figure1-3.tiff, and a short cover note naming the special issue.
