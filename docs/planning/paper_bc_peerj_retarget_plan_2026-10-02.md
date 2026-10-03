# Paper B+C — Retarget to PeerJ Computer Science

**Role:** Architect (PLANNING) · **Date:** 2026-10-02 · **Lane:** `paper/bc-venue-definition`
**Trigger:** TMLR desk-rejected submission 12779 without review (email from Teng, 2026-10-02 or
earlier; no reasons given beyond "unlikely to meet one or both TMLR criteria").
**Starting point:** tag `tmlr-submission-12779` (`75b93a7f4`). The manuscript and the claims
SSOT are identical at the lane head; only `EIC_ENQUIRY_prior_publication.md` differs.

**Sources read:** PeerJ CS Instructions for Authors, Policies & Procedures, Editorial Criteria
(peerj.com/about/…; the live pages are JavaScript-only, so I read the Wayback copies from 2025),
and the Overleaf template `wlpeerj.cls` (LaTeX template for PeerJ submissions). **Re-check the
live pages before filing (task P0.3).**

---

## 1. What PeerJ CS asks for, compared with what we have

| # | PeerJ requirement | Paper B+C today (TMLR build) | Gap / action |
|---|---|---|---|
| R1 | Reviewers judge **soundness only**, not "impact, degree of advance, novelty or interest" | The paper's strength is soundness: claim registry, artifact bundle, disclosed limitations | Fits the journal. No action needed |
| R2 | **Single-blind** review: reviewers see who the authors are | Double-blind build; identity hidden behind `\ifdeanon` | Build the de-anonymised branch only. Drop the anonymity machinery from the PeerJ file |
| R3 | LaTeX: **one PDF plus all source files**, `wlpeerj.cls`, options `fleqn,10pt,lineno` (line numbers on for review) | `article` + `tmlr.sty` | New file `paper_bc_peerjcs.tex` on `wlpeerj.cls` |
| R4 | **Author Cover Page** as page 1: title; authors; affiliation (dept, institution, city, state, country); name and email of the submission admin. It must match the online form exactly | Not present | Add the page. Name: **Jonathan Herrera-Vásquez** (paper form, per the author-name rule) |
| R5 | **Abstract ≤ 500 words / 3,000 characters**; no references; **bold run-in subheadings** (`Background.` `Methods.` `Results.` `Conclusions.`) | 305 words; one unstructured paragraph; TeX source in `pub/claims.toml` | Restructure into four labelled paragraphs. **Check characters, not just words**: 305 words is probably about 2,100 characters, but it must be measured. RCA-003 guards this file |
| R6 | Standard sections: Introduction / Background → Methods → Results → Discussion → Conclusions → Acknowledgments → References. "Do not combine sections." | Taxonomy / gaps / framework / empirical / threats / future work / availability | Re-map the headings (§3). Keep the content; change only the headings and their order |
| R7 | **AI Application checklist** (applies to ML papers): 3rd-party datasets named with **DOI/URL**; preprocessing; why these techniques were chosen; **computing infrastructure (OS, hardware, software)**; metrics justified | Preprocessing, metrics and selection are covered. **No dataset DOIs/URLs and no hardware/OS/software-version paragraph** in the main text | Add a "Computing infrastructure" paragraph and dataset citations (UCI Adult, German Credit, Breast Cancer Wisconsin), all from committed artifacts |
| R8 | **AI policy:** when AI is a *component of the research*, give the tool, version and **complete prompts** in Methods. Disclose any AI use at submission. **AI-generated reference lists are prohibited.** AI used only for editing goes in the Acknowledgments | The EXP4 judges are named with exact model IDs in Supplementary S1, which also gives the system and user prompts. The original Jinja templates are lost (RCA-002, disclosed). AI-assisted drafting is not disclosed | (a) Move the judge model IDs and decoding settings into Methods, and point to S1 for the full prompts. (b) Keep the disclosure that the original templates were lost, quoting the phrase "complete prompts" so it reads as a deliberate disclosure, not an omission. (c) The author decides the wording of the AI-assistance disclosure (decision D5). (d) Record that every reference was verified against Crossref/DOI by a human |
| R9 | **No material previously published in a peer-reviewed journal.** "Unit of publication": coherent work must not be inappropriately subdivided | Paper A is published in RIMI from the same execution cohort; §Provenance states that no result is shared | Keep §Provenance. Re-run the shared-result guard (`scan_shared_literals.py --strict`, RCA-001 query). State the RIMI relationship in Notes to Staff (decision D4) |
| R10 | **Code and data: immutable archive with a DOI** holding an *exact copy* of what the study used; a GitHub link alone is not enough | Zenodo `10.5281/zenodo.21538180` = commit `553f65d71`, which **predates EXP4 cohort 2 and EXP6** | **A new Zenodo release is required** for the PeerJ version. Cite its version-specific DOI. Also attach the artifact bundle (16.2 MB as rebuilt 2026-10-02; limits are 30 MB per file and 50 MB in total) as Supplemental Data S1 |
| R11 | Figures: **separate files** named `Figure1.pdf`, …; vector PDF/EPS; **no titles or legends inside the image**; white backgrounds; colour-blind-safe; units on every axis; cite as "Fig. 1" | 3 PDF figures, embedded, plus 1 TikZ diagram | Export each figure as its own file from its committed generator (RCA-001). The TikZ figure becomes a standalone PDF with a generator. Check axis units and palette |
| R12 | Tables: editable; each table **uploaded as a separate file** (.docx preferred; .tex accepted); units in headings; fits US Letter with 2.5 cm margins | Inline `tabularx` tables | Put each table in `tables/TableN.tex`, `\input` it, and upload the same files |
| R13 | References: any **full, consistent** style (PeerJ restyles to Name–Year at production); every citation in the list and every list entry cited | 54 manual `\bibitem`s, natbib author–year | Keep them. Run the `reference-audit` skill (no orphans, no uncited entries). A `.bib` conversion is optional |
| R14 | Supplementary items named and cited as "Supplemental Article S1", "Table S1", "Data S1" | "Supplementary Table S1–S5" in a separate PDF | Rename the supplement to **Article S1** (PDF) and keep the internal Table S1–S5 labels. Fix every in-text reference |
| R15 | Declarations entered in the online form: **Funding statement**, **Competing interests**, author contributions (ICMJE), data availability | The Acknowledgments carry "no external funding / self-funded" | Move funding to the form. Remove funders from the Acknowledgments (PeerJ: "Do not acknowledge funders here") |
| R16 | US Letter, 2.5 cm margins, 12 pt Times, **left-justified** (review format) | A4/TMLR 10 pt | The class handles this. Check the review PDF |
| R17 | Title ≤ 250 characters; "avoid acronyms, abbreviations and jargon" | "…Taxonomy of XAI Evaluation Metrics and Paired Empirical Comparison of LIME versus SHAP" | Spell out XAI. LIME and SHAP are method names and stay (decision D2) |
| R18 | Fee: an APC or an Individual Lifetime Membership, paid **after acceptance**. Typeset papers over 40 pp pay a surcharge. Low-income waiver (World Bank) | Mexico is not low-income, so no waiver | The author confirms the current price, or a UNADE institutional plan (decision D3). Expected typeset length is about 25–30 pp, under the 40 pp threshold |
| R19 | Preprints (including arXiv) are allowed | Not posted | Optional (decision D6) |
| R20 | Prior reviews from another journal can be reused | There are none (desk reject) | Not applicable. Do not mention TMLR beyond what the form asks |

## 2. Standing constraints (unchanged)

- **RCA-001:** every number stays registered. `paper_bc_peerjcs.tex` goes into
  `pub/claim_registry.toml` (`appears_in`, `[coverage]`) **before** any prose edit, and into
  `guarded_files` in `regression-guards.yaml`. No retired value may reappear.
- **RCA-002:** EXP4 numbers come from the committed aggregate CSVs. The reconstructed sources
  stay pinned.
- **RCA-003:** abstract changes are made in `pub/claims.toml` with doubled backslashes. Re-read
  the rendered abstract in the PDF.
- **ADR-0017** (cohort-2 reporting) still applies. **ADR-0018:** nothing from this paper enters
  the CIFIE chapter.
- **Science is frozen.** No result, table value or claim changes in a retarget. Only headings,
  structure, format, declarations and new provenance (infrastructure, dataset DOIs, new Zenodo DOI).
- **Review F10 stays closed.**

## 3. Section re-map (headings only)

| PeerJ standard section | Current TMLR content moved there |
|---|---|
| Introduction | §Introduction (decision problem, contributions) |
| Background | LIME/SHAP background; benchmark-design implications |
| Survey Methodology and Taxonomy *(Methods, part 1)* | Search protocol and corpus profile; the four taxonomy views |
| Materials & Methods *(part 2)* | RQs/hypotheses; design; data and preprocessing (**+ dataset DOIs**); explainer protocol; metrics; inferential protocol; EXP4 design (**+ model IDs, prompts → S1**); **+ Computing infrastructure**; reproducibility contract |
| Results | EXP2 paired inference and probes; EXP3 replication; EXP4 reliability (both cohorts) |
| Discussion | Gaps 1–3; formalization-aware criteria and layered architecture; provenance; interpretation scope; threats to validity; future work |
| Conclusions | Current conclusion |
| Acknowledgments | Non-funding acknowledgments + AI-editing statement (D5) |
| Data and Code Availability | The current §Code and Artifact Availability (repository paths + **new Zenodo DOI**) |
| References | Unchanged |

Moving gaps and framework into Discussion is the one structural judgment call. They are
synthesis, not Results. Alternative: keep them as a "Taxonomy and Gap Analysis" Results
subsection. The Architect recommends Discussion.

## 4. Tasks

**Phase 0 — Lane and inputs (no manuscript edits)**
- P0.1 Record the desk reject: `OPENREVIEW_SUBMISSION.md` (status), `ACTIVE_CONTEXT.md`,
  memory. Paper lane **unfrozen** for the retarget.
- P0.2 Cut `paper/bc-peerj-cs` from `tmlr-submission-12779`. The TMLR files stay intact as the
  record of what was filed.
- P0.3 The author downloads the Overleaf template zip (Overleaf → Download source) into
  `docs/reports/paper_bc/peerj/`. Commit `wlpeerj.cls` unmodified. Re-check the live
  instructions pages.
- P0.4 ADR-0019: "Paper B+C venue change TMLR → PeerJ CS" (single-blind; identity machinery
  retired in the new build; what TMLR-specific checks no longer apply).

**Phase 1 — Registry first**
- P1.1 Register `paper_bc_peerjcs.tex` (+ `tables/*.tex`) in `appears_in` / `[coverage]`.
  Add it to the RCA-001/RCA-002 `guarded_files`. Verifiers must be green on an unchanged copy
  before any edit.
- P1.2 Register any new number that the infrastructure paragraph introduces (versions, core
  counts, RAM), sourced from committed run metadata, not from memory.

**Phase 2 — Port (mechanical)**
- P2.1 New `paper_bc_peerjcs.tex` on `wlpeerj.cls` (`fleqn,10pt,lineno`) with the Author
  Cover Page, the de-anonymised branch only, and no `\ifdeanon`.
- P2.2 Re-map the headings per §3. Extract the tables to `tables/TableN.tex`.
- P2.3 Supplement → `paper_bc_peerjcs_supplemental_article_S1.tex` ("Article S1"). Update the
  in-text references.
- P2.4 Makefile targets and `scripts/pubs/build_artifact_bundle.py` / `verify_sync.py` support
  for the new file names (RCA-003 guarded: the missing-input refusal stays).

**Phase 3 — Content required by PeerJ (author approves each)**
- P3.1 Structured abstract in `pub/claims.toml` (new key `paper_bc_abstract_peerj_en`; the
  TMLR key stays). ≤ 3,000 characters, measured on the rendered text.
- P3.2 Computing-infrastructure paragraph and dataset DOIs/URLs.
- P3.3 EXP4: judge IDs and decoding settings into Methods; prompt pointer to Article S1.
- P3.4 Title (D2), Acknowledgments with the funding statement removed, AI-assistance statement
  (D5).
- P3.5 New Zenodo release from the retarget commit. Put the DOI in Data Availability and in
  `CITATION.cff`/README if those carry it.

**Phase 4 — Figures and tables**
- P4.1 Re-run the figure generators, export `Figure1.pdf`…`FigureN.pdf` without in-image
  titles, and check axis units and a colour-blind-safe palette. Turn the TikZ framework figure
  into a standalone PDF with a committed source.
- P4.2 Per-table upload files. Units in parentheses in the headings.

**Phase 5 — Submission gate (PeerJ edition of the "After any revision" checklist)**
- `verify_claims.py`, `verify_sync.py`, `verify_exp4_reconstruction.py`,
  `scan_shared_literals.py --strict` all green, run **from a clean worktree**.
- `reference-audit`: 0 orphans, 0 uncited, DOIs resolve.
- Read the review PDF: line numbers, US Letter, cover page first, abstract headings bold,
  figure/table order matches first citation, "Fig. N" citation style.
- Upload set: review PDF + `.tex` + `.bib`/`bbl` + `wlpeerj.cls` + Figure files + Table
  files + Article S1 PDF + Data S1 (bundle zip). Each under 30 MB, total under 50 MB.
- The online form matches the cover page exactly. Funding, competing interests ("none"),
  AI-use disclosure, data-availability DOI.
- Notes to Staff: the RIMI relationship (D4).
- Phase 5 report to the author. **The author files; Claude does not.**

**Phase 6 — After filing:** tag `peerjcs-submission-<id>`; update context and memory.

## 5. Decisions for the author

| ID | Decision | Recommendation |
|---|---|---|
| D1 | Article type: Research Article or AI Application | **Research Article.** It fits taxonomy + experiment + reliability study. Meet the AI Application checklist anyway (R7) |
| D2 | Title | "From Fidelity to Semantics: A Taxonomy of Explainable AI Evaluation Metrics and a Paired Empirical Comparison of LIME and SHAP" |
| D3 | APC vs Lifetime Membership; any UNADE plan | Check the price page and UNADE before Phase 2. Payment happens only after acceptance |
| D4 | How to declare the Paper A (RIMI) relationship | Keep §Provenance as written. Add one sentence in Notes to Staff with the RIMI DOI and the statement that no result is shared |
| D5 | AI-assistance disclosure wording (drafting/editing/code support) | Disclose in the submission form and the Acknowledgments. State that every reference was verified by the author against DOI records. Omitting it is a "serious breach" under PeerJ policy |
| D6 | Post an arXiv preprint at submission | Optional. Allowed by PeerJ. It adds a public timestamp |
| D7 | Section 3 placement of gaps/framework | Discussion |

## 6. Risks

- **Prompt-completeness under the AI policy (highest).** The original-cohort Jinja templates
  are lost. Mitigation: S1 gives the transcribed system and user prompts in full, cohort 2 has
  its exact prompts and raw responses archived, and the loss is disclosed. An editor could
  still ask. The disclosure must be explicit, not buried.
- **Unit-of-publication objection** (Paper A and B+C from one cohort). Mitigation: §Provenance
  and the shared-literal scan.
- **AI-generated-reference prohibition.** Mitigation: the reference audit with DOI resolution
  and the author's attestation.
- **The Zenodo DOI is stale** (R10). This blocks submission until P3.5 is done.

Estimated effort: Phases 0–2 about 4 h; Phase 3 about 3 h plus author review; Phase 4 about
2 h; Phase 5 about 2 h.
