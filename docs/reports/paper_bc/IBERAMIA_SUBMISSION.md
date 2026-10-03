# Paper B+C — submission sheet: *Inteligencia Artificial* (IBERAMIA)

**Journal:** *Inteligencia Artificial*, Revista Iberoamericana de Inteligencia Artificial
(IBERAMIA). ISSN 1137-3601 (print), 1988-3064 (online). Indexed in Scopus, ESCI (Clarivate),
DOAJ and Compendex. Submit at https://journal.iberamia.org (register, then "Submissions").

**Status (2026-10-02):** manuscript ready for submission. Not yet submitted.

**Venue history:** TMLR desk-rejected the paper (`TMLR_REJECTION_RECORD.md`). A PeerJ Computer
Science edition was prepared and then dropped before filing: PeerJ charges a publication fee
after acceptance (about US$2,155, or a US$755 membership) and the author cannot pay fees
(ADR-0020). *Inteligencia Artificial* charges nothing.

---

## 1. Journal requirements, checked 2026-10-02

Source: https://journal.iberamia.org/index.php/intartif/about/submissions, the journal's LaTeX
template (`iberamia_LaTex.zip`) and its formatting-guidelines PDF.

| Requirement | Journal rule | This submission |
|---|---|---|
| **Length** | **No page limit for research articles.** Only thesis summaries are limited (2–4 pp) | 32 pp A4, including Appendix A. **No restriction applies.** |
| File | One PDF, **maximum 4 MB** | `paper_bc_iberamia.pdf`, 0.36 MB |
| Fees | "No fees for publication nor editing tasks" | None |
| Template | LaTeX recommended: `iberamia.sty`, A4, 10 pt, two-sided | `iberamia.sty` unmodified; `logo.png` from the template |
| Review | Double-blind: no names, affiliations, funding acknowledgments, or web pointers that identify the authors; self-citations in the third person | Author block replaced by "Authors omitted for double-blind review"; GitHub URL and Zenodo DOI hidden (`\camerareadyfalse`); identity scan clean (§5) |
| Language | English preferred | English |
| Abstract | English abstract **and Spanish "Resumen"** (mandatory per the template) | Both, from `pub/claims.toml` |
| Keywords | English list; Spanish optional | Both |
| Headings | Up to three levels | Section, subsection, subsubsection; run-in paragraph labels only below that |
| Figures/tables | Centred, numbered, captioned, referenced in the text | Unchanged from the verified edition |
| References | Clear and complete, DOIs when available; template uses numbered citations | Numbered (`natbib`, `numbers`); entries keep their DOIs |
| Supplementary files | Not provided for (single PDF upload) | Supplementary Tables S1–S6 are **Appendix A** of the PDF |
| Originality | Not published or under review elsewhere; arXiv preprints allowed | Not under review anywhere. The RIMI paper shares no result (§6) |
| Licence | CC BY-NC; copyright transferred to IBERAMIA | Note for the author: different from PeerJ's CC BY |
| Comments for the Editor | Up to five suggested reviewers with name, email and justification | Draft in §4 |
| Review time | About 6–8 weeks; at most one resubmission | – |

## 2. Files

| File | Role |
|---|---|
| `paper_bc_iberamia.tex` | Manuscript source (review build by default) |
| `paper_bc_iberamia_appendix.tex` | Appendix A, `\input` after the references: Tables S1–S6 |
| `paper_bc_iberamia.pdf` | **The file to upload** |
| `iberamia.sty`, `logo.png` | Journal template files, unmodified |
| `pub/claims.toml` → `pub/fragments/paper_bc_{abstract_en,resumen_es,keywords_en,palabras_clave_es}.tex` | Abstract, Resumen and keywords (generated) |

Build: see `BUILD.md`.

## 3. Submission form (metadata)

- **Title:** From Fidelity to Semantics: A Taxonomy of Explainable AI Evaluation Metrics and a
  Paired Empirical Comparison of LIME and SHAP
- **Author (form only; not in the PDF):** Jonathan Herrera-Vásquez, Department of Computer
  Science, Universidad Americana de Europa (UNADE), Cancún, Quintana Roo, Mexico;
  jonnabio@gmail.com.
- **Abstract:** paste `pub/fragments/paper_bc_abstract_en.tex` as plain text (drop the `%` line;
  `$d_z{=}3.00$` → d_z = 3.00; `\texttt{TreeExplainer}` → TreeExplainer; `vs.\ ` → vs.).
- **Keywords:** explainable AI; evaluation metrics; taxonomy; LIME; SHAP.
- **Language:** English.

## 4. Comments for the Editor (draft)

The journal asks for up to five potential reviewers with full name, email and a scientific
justification. These candidates are authors of work the paper builds on. **[AUTHOR]** Check each
for conflicts of interest (no co-authorship or shared institution), and add their current
institutional email from their institution's page. Do not use an email copied from a paper
without checking it.

1. **Anna Hedström** — first author of Quantus, the XAI evaluation toolkit the taxonomy positions
   against (proxy and benchmark metric families).
2. **Christin Seifert** — senior author of Nauta et al. (2023), the systematic review of
   quantitative XAI evaluation that the gap analysis builds on.
3. **Stefan Haufe** — first author of "Explainable AI needs formalization" (2026), the basis of
   the formalization-aware evaluation criteria.
4. **Kary Främling** — co-author of Canha et al. (2025), a functionally grounded benchmark
   framework for XAI methods; author of contextual-importance explanations.
5. **Francisco Herrera** (Universidad de Granada) — co-author of the trustworthy- and
   responsible-AI surveys cited in the paper; an Ibero-American XAI researcher. (No relation to
   the submitting author; the surname is a coincidence.)

Suggested opening for the comment box:

> This manuscript proposes a four-axis taxonomy of XAI evaluation metrics, grounded in a
> 44-paper structured scoping corpus, and a paired empirical comparison of LIME and SHAP. The
> empirical cohort was released with an earlier article (Revista de Investigación
> Multidisciplinaria Iberoamericana, https://doi.org/10.69850/rimi.vi3.307); this manuscript
> reports no result of that article, and the overlap is stated in the section "Provenance of
> the Empirical Cohort". Suggested reviewers: [the list above, with emails].

The RIMI sentence names the earlier article but not, in itself, the submitting author, and it
goes only to the editor. It is the same disclosure made to TMLR and planned for PeerJ.

## 5. Anonymity check (review PDF, 2026-10-02)

`pdftotext paper_bc_iberamia.pdf` searched for the author's name, email, institution, city,
GitHub account and Zenodo. The only match is reference [24], Herrera-Vásquez and
Herrero-Uceda (2026). That is a third-person citation of published work, which the journal
allows, and the text treats it as anyone else's paper. Re-run this check after every edit:

```bash
pdftotext docs/reports/paper_bc/paper_bc_iberamia.pdf - | grep -i -E "jonnabio|github\.com/jonnabio|zenodo|UNADE|Universidad Americana|Canc.n|Jonathan"
```

Expected output: nothing.

## 6. Paper A (RIMI) overlap

Unchanged by the refactor: `scan_shared_literals.py --strict` reports 0 unexplained matches (55
known coincidences); `verify_claims.py` passes with the IBERAMIA files and the Spanish
abstract under `[coverage]`. §"Provenance of the Empirical Cohort" states that the per-method
mean levels, the four-method omnibus and the cross-dataset SHAP levels are cited to RIMI and
not restated.

## 7. AI-use disclosure

The journal has no AI policy. The Acknowledgments keep the disclosure written for PeerJ: the
author designed and directed the research, and AI tools assisted with language editing,
programming support and number checking. It identifies no one, so it stays in the review
build. **Reference list:** the author confirmed on 2026-10-02 that no reference was first
suggested by AI.

## 8. Code and data

- Review build: the paper says the code and data are in a public repository with a versioned DOI
  archive, both withheld for double-blind review.
- Camera-ready build (`\camerareadytrue`): GitHub URL plus Zenodo
  `10.5281/zenodo.23111684` (version 0.4.0). If the code or data change before acceptance,
  publish a new Zenodo version (`ZENODO_RELEASE.md`) and update `\zenodoversiondoi`.

## 9. After acceptance (camera-ready)

1. Set `\camerareadytrue`: this restores the author block, the repository URL and the DOI.
2. Fill in `\thispaperdoi`, `year`, `volume`, `issue` and `page` with the journal's values.
3. Add funding acknowledgments if any (none at present).
4. Rebuild, re-run the four verifiers, and send the PDF.

## 10. Optional: arXiv preprint (approved by the author, D6)

Allowed by the journal. Build the camera-ready variant (`\camerareadytrue`) for arXiv, category
cs.LG with cross-list cs.AI. Posting it publicly makes the double-blind review weaker: reviewers
could find it. Posting after acceptance avoids that.
