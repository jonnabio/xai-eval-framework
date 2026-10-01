# Science-First Revision Plan for the CIFIE XAI Book Chapter

**Status:** Active - review remediation R0-R2 complete and Section 04 written
(2026-09-29); the TintAzul/CIFIE editorial requirements are merged into the
"Consolidated pending list" (2026-09-30), which now governs the order of work

**Created:** 2026-09-28

**Updated:** 2026-09-29 - folded in the Scientific Advisor review of
`drafts/v3_editorial_review/cifie_xai_fom7_2026-09-29_formatted.docx`;
2026-09-30 - merged the editorial compliance assessment
(`editorial/editorial_compliance_assessment_2026-09-30.md`)

**Lane:** `chapter/cifie-sync-2026-09`

**Input assessment:** `planning/general_assessment_2026-09-28.md` (with its
2026-09-29 addendum)

## Objective

Transform the current FOM-7 technical chapter into a scientifically rigorous but
readable book chapter that:

1. gives a clear general overview of XAI;
2. explains why XAI matters and what it can and cannot provide;
3. presents future-facing application areas through concrete examples;
4. organizes the field's principal research and deployment gaps;
5. retains FOM-7 and the verified benchmark as the chapter's original contribution;
6. uses APA 7 throughout; and
7. produces a Word document aligned with the thesis's professional formatting
   standards.

## Scientific principles

- Evidence precedes prose: every substantive claim receives an identified source.
- Explanation quality is purpose-, audience-, domain-, and risk-dependent.
- Plausibility, faithfulness, human usefulness, causal validity, and regulatory
  adequacy are distinct claims.
- Future-facing statements are framed as evidence-supported trajectories or research
  needs, not predictions presented as facts.
- Systematic reviews organize broad claims; primary studies support concrete
  mechanisms or examples; official standards and regulations support governance
  claims.
- Contradictory or cautionary evidence is included where relevant.
- Existing empirical numbers remain governed by RCA-001, chapter `[coverage]`, and
  ADR-0018 `[exclusivity]`.

## Non-goals

- Do not create an encyclopedic catalogue of every XAI method.
- Do not turn the chapter into a legal-compliance manual.
- Do not claim that explanations guarantee trust, fairness, causality, safety, or
  correctness.
- Do not import unpublished Paper B+C results.
- Do not edit thesis or paper artifacts from the chapter lane.
- Do not add citations merely for recency or citation volume.

## Target architecture

Keep the build's eleven-section contract, but revise the role of each section.

| Section | Proposed function | Main action on current material |
| --- | --- | --- |
| 01 | Abstract and keywords | Rewrite last, after the argument stabilizes. |
| 02 | Why XAI matters | Broaden the introduction from benchmarking motivation to the scientific and societal functions of explanation. |
| 03 | What XAI is and is not | Retain the strongest conceptual distinctions; compress repeated FOM-7 language. |
| 04 | Application horizons and concrete examples | Create the missing domain-facing section; move the detailed method catalogue to section 05. |
| 05 | Main explanation families and the evaluation problem | Compress LIME, SHAP, Anchors, and DiCE around question, output, strength, failure mode, and suitable evidence. Integrate the strongest parts of the current crisis section. |
| 06 | Gaps in XAI | Expand from metric fragmentation to technical, construct, human, causal, operational, governance, and emerging-model gaps. |
| 07 | FOM-7 as a scientific response | Preserve the seven gates, reduce repeated justification, and map each gate to one or more gaps. |
| 08 | Empirical case study | Combine the essential design and result narrative; keep protected values and tables, but present them as a demonstration of the protocol. |
| 09 | Implications for research and practice | Synthesize audience-specific lessons, domain transfer, and lifecycle governance. |
| 10 | Limitations and research agenda | Separate limitations of the Adult benchmark from the wider future XAI agenda. |
| 11 | Conclusions | Return to the broad thesis, then state the bounded contribution of FOM-7. |

### Recommended working title

**De la explicación a la evidencia: fundamentos, aplicaciones y evaluación
auditable de la inteligencia artificial explicable**

FOM-7 should remain visible in the subtitle or closing clause rather than forcing the
whole chapter to read as a protocol manual.

## Application-area design

Section 04 should use a repeated, readable structure. Each domain receives:

1. the decision or task supported by AI;
2. the stakeholder who needs an explanation;
3. one concrete example;
4. the harm caused by a misleading explanation;
5. the type of explanation or evidence that may help; and
6. the unresolved scientific gap.

Priority domains:

| Domain | Example | Scientific caution |
| --- | --- | --- |
| Health and biomedicine | A clinician examines which evidence influenced a diagnostic-risk prediction and whether the model relies on a spurious acquisition artifact. | A heatmap or feature attribution does not validate the diagnosis or establish causal relevance. |
| Finance and consequential allocation | A credit analyst and an applicant receive different explanations of a denial: one for model audit, one for contestability and possible recourse. | Correlated features, proxy variables, and infeasible counterfactuals can make an explanation misleading. |
| Cybersecurity and critical infrastructure | A security analyst uses an explanation to prioritize why an anomaly detector flagged network traffic. | Attackers may manipulate both the predictor and the explanation; timeliness and false-positive burden matter. |
| Autonomous and industrial systems | An engineer reviews why an autonomous system chose an action or why a predictive-maintenance model signaled impending failure. | A readable rationale is not a safety case; explanations must connect to validation, monitoring, and failure analysis. |
| Foundation, language, and multimodal models | A team investigates whether an LLM answer follows source evidence, a memorized pattern, or a confabulated rationale. | Fluent natural-language rationales are not necessarily faithful descriptions of internal computation. |

Education and public services can be added as a compact sixth example if it adds a
distinct stakeholder or evaluation problem rather than repeating credit allocation.

## Literature strategy

### Source hierarchy

1. **Systematic reviews and meta-surveys** for field-wide or domain-wide claims.
2. **Original peer-reviewed research** for methods, mechanisms, and empirical examples.
3. **Official standards, regulations, and institutional guidance** for governance
   requirements and terminology.
4. **Critical viewpoints** for contested claims, clearly identified as viewpoints.
5. **Preprints only when necessary** for emerging topics with no adequate
   peer-reviewed source; label their status explicitly.

Vendor blogs, generic web explainers, and unsourced forecasts are excluded from the
scientific evidence base.

### Literature work packages

#### L1. Reconcile the existing evidence base

- Update `sources/evidence_map.md` and `sources/source_inventory.md` to reflect the
  completed 2026-09-27 sync.
- Mark which current references support definitions, evaluation, empirical results,
  or limitations.
- Identify claims currently supported only by the thesis or by a secondary survey.

#### L2. General XAI and importance

- Retain the strongest existing conceptual sources.
- Add authoritative sources on explanation principles and trustworthy AI.
- Build a claim matrix for debugging, monitoring, human oversight, contestability,
  audit, and governance.

#### L3. Application domains

- Select two or three high-quality sources per priority domain: normally one recent
  systematic review, one foundational or representative primary study, and one
  critical or governance source when the literature is contested.
- Prefer open-access versions when available and verify DOI, title, authors, venue,
  year, and publication status.
- Record why each source is admissible in `references/citation_audit.md`.

#### L4. Field gaps

- Extend the evidence base for human-centered evaluation, calibrated reliance,
  causal/actionable recourse, explanation attacks, distribution shift, lifecycle
  monitoring, and LLM/multimodal explainability.
- Include negative evidence: explanations can create overreliance, fail to improve
  decision performance, or remain unfaithful despite being persuasive.

#### L5. APA 7 and bibliography closure

- Add accepted records to both `references/references.bib` and
  `references/references_apa7.md`.
- Run a cited-versus-listed audit, DOI resolution check, duplicate check, and APA 7
  metadata review.
- Remove unused entries rather than carrying a general reading list into the final
  references.

## Review remediation workstream (added 2026-09-29)

A Scientific Advisor review of the 2026-09-29 formatted build (rendered through
Microsoft Word, 75 pages, all pages inspected) returned **Not ready**. The empirical
core re-derives from artifacts and the new sections 02-03 are the target register;
the blockers are reproducibility, missing promised scope, and a small number of
numeric and presentation defects. Every finding is assigned below to a remediation
unit, a production file, and the phase that closes it. Finding IDs (C, H, M, L)
follow the review.

### Correction to the 2026-09-29 checkpoint

The checkpoint under "Immediate next action" records 48 rendered pages with readable
table widths. The same file rendered by Word gives 75 pages, mid-word breaks in
Table 2 ("configuraciones / , métodos", "reproducibilida / d"), a broken code block
("Perfi / lado"), and an illegible Figure 1. The difference comes from the
renderer and from the undefined page geometry (L1). From now on, visual QA is
valid only on a Word render (see the Render gate).

### Unit order

| Unit | Scope | Findings | Why this position |
| --- | --- | --- | --- |
| R0 | Make the build reproducible | C1, H3 (generator), M10 | Uncommitted sources and scripts are the largest risk of loss; later units cannot be verified without it. |
| R1 | Correct wrong or overstated evidence | H1, H2, M1-M5 | Small, protected edits; they must not wait for the Phase 5 compression. |
| R2 | Remove the drafting voice and repository vocabulary | M9 and the meta-commentary list below | Cheapest large gain in register; it also shrinks the text before new sections are added. |
| R3 | Write the promised scope | C2 | Phases 3-4 (sections 04 and 06), already planned; the title and the section 02 roadmap promise them. |
| R4 | Reader-experience devices | Editorial assessment items | Worked examples, gate trace, decision guide; they depend on the new architecture. |
| R5 | Figures for print | H4, M8, L4, H3 (labels) | Regenerate once the Phase 5 figure selection is final. |
| R6 | APA 7 closure | M7, L3 | At Phase 8, but the listed metadata corrections can be applied at any time. |
| R7 | Word layout | M6, L1, L2, L5 | Phase 7, against a Word render. |

### Progress

| Unit | Status | Commits | Result |
| --- | --- | --- | --- |
| R0 | Done 2026-09-29 | `3e5b21a68` | Clean-checkout build of `225419856` reproduced the reviewed DOCX (document, styles, media identical); both figure generators reproduce their figures' content; dependencies declared in the build script and README; generators recorded in `figure_registry.md`; `--out` crash fixed. |
| R1 | Done 2026-09-29 | `3f8789bad` (registry), `2df96d15a` (manuscript) | H1, H2, M1-M5 corrected. New guard `A05.lime.cost.chapter` negative-tested; new claim `exp2.run.lime.model_mean.rf.cost` (436 ms). 321 claims / 496 sites / 46 retired-value guards. |
| R2 | Done 2026-09-29 | `a32c36d0e` | Drafting voice, repository vocabulary, code blocks and undefined labels removed; device kept once (section 06). Word render checked. |
| R3 (applications) | Done 2026-09-29 | `465ec28dc` (registry), `e4005b2a9` (chapter) | Section 04 written in file 04 (five domains, each with a near-term horizon, plus a synthesis); the method families moved to file 05 without benchmark numbers, followed by the evaluation problem. Eleven verified sources promoted (59 references). Cited-versus-listed check on the built DOCX clean except the two known R6 orphans. Build: about 20,900 source words, 83 pages in Word. |
| R3 (gaps) | Structure done 2026-09-30; prose with the author | see git log | Files restructured (05 method families + evaluation problem; 06 gap-section starting material; 07 FOM-7; 08 design + results). Writing brief: `planning/section06_gaps_brief_2026-09-30.md` (seven gaps with claims, evidence and boundaries, reuse map, FOM-7 scope, section 08 compression list). The author writes section 06 (E-AI-1). |
| R4-R7 | Open | | |

Open from R0: the empty-header non-determinism in `format_academic_text` is
deferred to E-FMT. (Closed 2026-09-30: `main` fast-forwarded to `a1edb8bf4` and
pushed at the author's instruction; chapter work is not merged into the thesis lane.)

### Narrative arc adopted by the author (2026-09-30)

The author asked for a slower progression that does not reach FOM-7 or technical
detail too early: the need for explanation; the concept isolated from neighbouring
concepts (interpretability, transparency, model types), taught with diagrams; why it
matters, with practical fields; the evaluation crisis as the final framing of the
problem; the solution (FOM-7 and the science behind it); then application,
implications, limitations and conclusions. This supersedes the section order of the
scaffold. The existing text was moved accordingly (mechanical move, no new prose):

| File | Section | Content and origin |
| --- | --- | --- |
| 02 | Introducción | need for explanation; objective and roadmap (from former 02) |
| 03 | Qué es y qué no es la XAI | unchanged |
| 04 | Por qué importa la XAI | lifecycle functions, audiences, trust, governance (from former 02), then the application domains (former 04) |
| 05 | La crisis de evaluación en XAI | crisis and gap material (from former 05 and 06); the author's gap taxonomy goes here (brief) |
| 06 | Protocolo FOM-7 | former 07 |
| 07 | Métodos evaluados y diseño del benchmark | LIME, SHAP, Anchors, DiCE (former 05) and the benchmark design (former 08) |
| 08 | Aplicación empírica | the results (former 08) |
| 09-11 | Implicaciones, limitaciones, conclusiones | unchanged |

Tables renumbered to the new order (1 FOM-7 gates, 2 methods, 3 metrics, 4 results);
figure order unchanged. The build's table widths follow the new order.

**Author follow-ups created by the new arc (N-ARC):**

1. Section 02 is now short (about 520 words): expand it into the template's
   introduction (context, problem, brief state of knowledge, gap, "El propósito de este
   capítulo es...", organization) without introducing FOM-7 in technical terms.
2. Update the three roadmap passages to the new order: section 02 "Objetivo, tesis y
   recorrido", the closing paragraph of section 03, and the closing transition of
   section 04 ("Lo que los ámbitos tienen en común").
3. Section 03, "Niveles de evaluación y alcance de FOM-7": its FOM-7 paragraph introduces
   the protocol early; consider moving it to section 06 and keeping only the evaluation
   levels in section 03.
4. Practical fields: the author named the legal field; the current domains are health,
   finance, cybersecurity, autonomous systems and foundation models. A justice or public
   administration domain needs sources (literature pass L3).
5. Didactic figures (proposal, for the author's approval; they add figures before the
   empirical ones, so the empirical figures would be renumbered):
   - D1 concept map: explainability, interpretability, transparency (section 03);
   - D2 model spectrum: interpretable by design, black box with post-hoc explanation;
     model-agnostic versus model-specific (section 03);
   - D3 local versus global scope (section 03);
   - D4 one case, four explanatory objects: attribution, rule, counterfactual, example
     (section 03; links to the R4 worked example);
   - D5 who needs which explanation along the lifecycle (section 04);
   - D6 evaluation levels: application-, human- and functionally grounded (section 03 or
     05);
   - D7 the evidence chain artifact, construct, metric, test, result, claim (section 05);
   - D8 FOM-7 gate flow with one traced claim (section 06; R4.2).
6. Section 07 (4,589 words) is now the largest: the P-CASE compression applies mainly
   here (the design duplications listed in the section 06 brief, now in section 07).
7. The Resumen is rewritten last, following the slow arc.

### Consolidated pending list (2026-09-30)

This list merges the open review units (R3 gaps, R4-R7), the next steps agreed on
2026-09-29, and the TintAzul/CIFIE editorial requirements. It supersedes the unit order
above for everything still open. IDs starting with E come from
`editorial/editorial_compliance_assessment_2026-09-30.md`, where each is tied to the
editorial document that requires it.

**Author decisions recorded 2026-09-30**

| ID | Decision | Consequences (new tasks) |
| --- | --- | --- |
| E-AI | Use the official form's auxiliary-use option (grammar, style, organization of ideas) and sign that analysis, interpretation and conclusions are the author's. | **E-AI-1:** from 2026-09-30, AI support on the chapter is limited to auxiliary tasks: organizing ideas, outlines and evidence maps, source verification, grammar and style editing of author text, registry and build work, formatting, reference checks. New scientific prose is written by the author. **E-AI-2:** before signing, the author reviews and rewrites in his own words the passages drafted with AI assistance (commit history: every section 02-11, including section 04 of 2026-09-29), so the signed declaration describes the text as submitted. |
| E-PRIOR | No items from Paper B+C in the chapter. Ideas and discussion without direct citation are acceptable. The RIMI prior publication of H1-H2 is declared on the form. | **E-PRIOR-1** (see list below): remove the paired SHAP-LIME contrast and everything derived from it; keep the conceptual quality-cost discussion without Paper B+C results or citation. |
| E-AUTH | Dr. Herrero-Uceda declined authorship; he is removed from the byline. The chapter has a single author. Citations of the RIMI article keep him as co-author of that article. | **E-AUTH-1:** remove him from `00_hoja_diseno_editorial.md`, the chapter README and the build byline; single-author declaration and licence; no conflict of interest arising from authorship. |
| E-Q1 (length) | **Answered 2026-10-01:** "9000 palabras, Times New Roman, interlineado 1,5." Body at 20,350 words must fall to about 8,800; see `planning/length_plan_9000_2026-10-01.md` (budget per section, decision per subsection). Open: whether the 9,000 include references (E-Q1b). Times New Roman replaces the template's Cambria in the build and in the didactic figures. | **E-SIZE:** after every big edit, report the chapter size (routine below). |

**E-PRIOR-1: Paper B+C material to remove** (located 2026-09-30; **done 2026-09-30**, together with E-AUTH-1; Wilcoxon (1945) and Lakens (2013) left the bibliography once uncited; 57 references):

- `tables/table_results_summary.md`: the H3 row, the exploratory 15/15 row, and the
  note's references to them.
- `08_aplicacion_empirica_perfiles_fom7.md`: in "SHAP y LIME: frontera calidad-coste",
  the paired-contrast sentences and the 15/15 analysis ($p_{\mathrm{Holm}} = 3.05
  \times 10^{-4}$); in "Reproducibilidad", the LIME cross-dataset stability sentence
  (EXP3 LIME extension).
- `07_diseno_empirico.md`: the paired-cell unit paragraph (75 coincident cells) and
  the SHAP-LIME Wilcoxon paragraph of the inferential plan.
- `11_conclusiones.md`: the sentence on the paired SHAP-LIME contrast.
- `06_protocolo_fom7.md`: the "(H1 a H3 en la Tabla 4)" pointer becomes "(H1 y H2)".
- Registry: drop the chapter sites of the 15/15 exploratory claim (`3.05`) and add the
  removed statements to the review of `[exclusivity]`, which checks numbers only; the
  prose check is manual (grep for "pareado", "H3", "15 de 15", "menos dimensiones").
- Kept: the gate descriptions that name Wilcoxon as a generic paired test (section 06,
  Table 2), and the qualitative SHAP-LIME quality-cost discussion based on the
  published block-level results (RIMI) and on the chapter's own section 08 profiles.

**E-SIZE: size routine after every big edit**

After every structural unit, section rewrite or bulk edit, the report to the author
includes: body words (sections 01-11 plus tables, excluding the design sheet, source
notes and references), words per changed section, Word page count of the built DOCX,
and the change against the previous report. Baseline (2026-09-30, `06267988c`):

| Measure | Value |
| --- | --- |
| Sections 01-11 | 19,874 words |
| Tables 1-4 | 1,029 words |
| Body (sections + tables) | 20,903 words |
| Reference list (59 entries) | 2,205 words |
| Word render | 83 pages |
| Largest sections | 05 (4,430), 06 (2,400), 07 (2,253), 04 (2,094), 08 (1,995) |

Size log (append one row per big edit):

| Date | Unit | Body words | Change | Word pages | Sections changed |
| --- | --- | ---: | ---: | ---: | --- |
| 2026-09-30 | Baseline (`06267988c`) | 20,903 | | 83 | |
| 2026-09-30 | E-PRIOR-1 + E-AUTH-1 | 20,434 | -469 | 81 | 06 (+2), 07 (-166), 08 (-172), 11 (-22), Table 4 (-111) |
| 2026-09-30 | P-CASE structure (files 05-08) | 20,424 | -10 | 82 | 05 3,296; 06 1,136 (starting material); 07 2,399 (FOM-7); 08 3,901 (design + results) |
| 2026-09-30 | E-APA / R6 (references only) | 20,424 | 0 | 82 | in-text citation edits in 02, 03, 08; reference list 55 entries |
| 2026-09-30 | E-FMT template format (build only) | 20,424 | 0 | 78 | A4, Cambria 12 pt; page count falls with the wider A4 text block |
| 2026-09-30 | N-ARC narrative move | 20,350 | -74 | 77 | 02 520; 04 3,223; 05 1,848; 06 2,399; 07 4,589; 08 1,820 (obsolete transition paragraph of former 05 removed) |

**Track A: decisions and questions (start now, in parallel with drafting)**

| ID | Item | Owner | Blocks |
| --- | --- | --- | --- |
| E-Q1 | **Open (length unanswered 2026-09-30; monitored through E-SIZE).** Ask the editor: length limit; whether to submit on the template file with its header logo and label; whether the *Hoja de diseño* is submitted; figure requirements for print; submission format and deadline; acceptability and authorization of results already published elsewhere | Author | P-CASE target length, E-FMT header, E-FRONT, R5 |
| E-AI | **Decided 2026-09-30:** auxiliary-use declaration; see E-AI-1 and E-AI-2 | Author | E-FORMS; possibly author rewriting of drafted passages |
| E-AUTH | **Decided 2026-09-30:** Dr. Herrero-Uceda removed (declined authorship); single author; see E-AUTH-1 | Author | E-FRONT, E-FORMS |
| E-PRIOR | **Decided 2026-09-30:** declare RIMI prior publication; remove all Paper B+C material; see E-PRIOR-1 | Author | E-FORMS; Table 4 and section 08 wording |
| E-TYPE | Choose the *Tipo de capítulo* for the design sheet | Author | E-FRONT |

**Track B: content, in this order**

| Order | ID | Item | Depends on |
| --- | --- | --- | --- |
| 1 | A-04 | Author review of section 04 (in progress 2026-09-30) | none |
| 2 | P-CASE | Section 06 field-gap taxonomy; FOM-7 to file 07; design merged into file 08 with the results; compression of sections 05-08 toward the length limit, including removing statistics duplicated between Table 4 and section 08 prose and splitting overlong paragraphs | A-04; E-Q1 for the target length |
| 3 | E-STRUCT | Template structure: section 02 titled "Introducción" with the six template elements, including an explicit "El propósito de este capítulo es..." sentence and a labelled state-of-knowledge and gap step; conclusions that answer contribution, learning, implications, limitations and future research | P-CASE |
| 4 | R4 | Reader devices, scaled to the length limit: four-method worked example, gate-trace figure, decision guide | P-CASE, E-Q1 |
| 5 | E-FIG + R5 | Mention every figure in the text before it appears (Figures 2-6 currently are not); state each figure's inference; keep only non-decorative figures; APA captions; grayscale-legible regeneration; valid error bars | P-CASE, E-Q1 figure rules |
| 6 | E-APA + R6 **(done 2026-09-30; Zheng et al. 2025 not externally verifiable, unchanged)** | Metadata corrections (Barredo Arrieta 2020, Becker and Kohavi dataset DOI, Lundberg and Lee NeurIPS, Schwalbe and Finzel 2024); remove or cite Adadi and Belle; Spanish reference conventions ("En", "Artículo", "Tesis doctoral", "[Conjunto de datos]") in the 14 affected entries; recheck "y"/"&" | none (can run any time) |
| 7 | P-FINAL | Resumen rewritten last (150-250 words, answering the template's six questions); three to five keywords that do not repeat the title; conclusions finalized; top-level statement sweep | all content units |
| 8 | E-FRONT | Portada with title, full names, academic degree, affiliation, ORCID and e-mail for each author; design sheet updated to the template fields | E-AUTH, E-TYPE, E-Q1 |

**Track C: format and submission**

| Order | ID | Item | Depends on |
| --- | --- | --- | --- |
| 9 | E-FMT (replaces R7 format targets) **(done 2026-09-30 except the header, which awaits E-Q1)** | Build on the template's format: A4; margins 2.54 cm top and bottom, 3.17 cm left and right; Cambria 12 pt throughout; headings bold at 12 pt, level 1 in uppercase; 1.5 spacing; justified text; header per the editor's answer. Keep from R7: Table 2 widths, keep-with-next for table titles and notes, left-aligned code and table cells, deterministic header parts. Page numbers are optional (the template has none) | E-Q1 |
| 10 | E-FORMS | Complete the author checklist, authorship declaration (with E-AI, E-AUTH, E-PRIOR outcomes) and licence; author signatures | Track A |
| 11 | FINAL-QA | Full Scientific Advisor rigor review, reference audit, rubric self-score, Word render of every page, clean-checkout rebuild; assemble `final/submission_package/` | all |

The earlier "Next steps" list of 2026-09-29 maps as follows: author reading of
section 04 is A-04; section 06 is P-CASE; reader devices are R4; figures, APA and Word
layout are E-FIG/R5, E-APA/R6 and E-FMT; the Resumen, conclusions and final review are
P-FINAL and FINAL-QA.

### R0. Reproducibility (Critical, C1)

1. Commit on `chapter/cifie-sync-2026-09`, in separate commits by kind (ADR-0013):
   the revised sections 02, 03, 07 and 08; `references.bib` and
   `references_apa7.md`; `fig_cd_diagram_es.png` and `figure_registry.md`; the
   evidence map, source inventory, citation audit and candidate literature;
   `scripts/build_cifie_chapter.py`; and `scripts/generate_cifie_chapter_figures.py`
   (currently untracked).
2. Declare the build dependencies (`python-docx`, `Pillow`, `matplotlib`, `pandas`,
   and Quarto's pandoc) in the build script docstring and in the chapter README.
3. Make the figure generator the only producer of `figures/exported/*_es.png` used
   by the chapter, and record the generator in `figure_registry.md` for each figure.
   This closes the RCA-001 invariant that a figure with data labels needs a
   committed generator.
4. Rebuild from a clean checkout of the lane and compare paragraph count, headings,
   tables, media hashes and page count with the reviewed build. Record the result.
5. Do not keep chapter commits on `thesis/*`. The five chapter commits currently on
   `thesis/rca-001-phase-2` (`664496a25`..`835bde4e0`) are also on the chapter lane;
   the thesis lane should stop carrying chapter work (ADR-0013).
6. Ensure `scripts/pubs/scan_shared_literals.py` reaches every lane that builds the
   chapter; it is absent from `thesis/rca-001-phase-2`.
7. Treat reviewed builds as outputs: keep the formatted DOCX out of version control
   or commit it only together with the commit hash it was built from.

### R1. Evidence corrections (High and Medium)

| ID | Location | Correction | Verification |
| --- | --- | --- | --- |
| H1 | `04_metodos_lime_shap_anchors_dice.md`, LIME paragraph ("coste medio de 226 ms") | Remove the retired value. In the new architecture this sentence moves to section 08 anyway; cite the registered per-model LIME costs. | Widen the `A05.lime.cost` retired guard to text `226 ms` and add the chapter files; negative-test that `226 ms` fails `verify_claims.py`. |
| H2 | `08_aplicacion_empirica_perfiles_fom7.md`, "Reproducibilidad como hallazgo"; `tables/table_results_summary.md`, P1 row | Replace "configuraciones replicadas de EXP1" with the EXP2 RF/N=100 subset over five seeds; add the pooled fidelity CVs (11.4% SHAP, 12.0% LIME) against the 15% criterion. Keep section 07's EXP1 CV < 9% statement, which is correct for EXP1. | Add the chapter sites to `exp2.pooled_cv.shap.fidelity` and `exp2.pooled_cv.lime.fidelity` (currently thesis sites only). |
| M1 | Table 4, H3 row; section 08 SHAP-LIME paragraph; section 11 | Label thesis-only results as unpublished and not yet peer reviewed at first use, e.g. "según resultados de la tesis doctoral, aún no publicados". Replace "sitúa el origen de la inestabilidad en el espacio codificado" with "es compatible con una interacción entre el ancho de kernel y la dimensionalidad del espacio codificado, que la tesis deja abierta". | Top-level statement sweep of 01 and 11. |
| M2 | Section 01 Resumen; section 08 "Síntesis"; section 09 | Qualify "LIME conserva ventajas de coste y parsimonia" as a comparison with SHAP, with the stated exceptions: DiCE is the most parsimonious (0.017), TreeSHAP on XGBoost (21 ms) is cheaper than LIME on XGBoost (122 ms), and LIME on SVM costs 17,620 ms. Report the LIME RF cost or explain its omission; the registered run-level LIME mean (`exp2.run.lime.cost.mean`, 3,661 ms) can state the overall level. | All values already registered except the LIME RF run mean, which needs a new `exp2.run.lime.model_mean.rf.cost` claim. Do not use `exp2.paired.cost.median.lime.rf`: paired-contrast values belong to Paper B+C and fail `[exclusivity]`. |
| M3 | Section 08 design (first use of SHAP) | Disclose that "SHAP" pools TreeExplainer (rf, xgb; model-specific) and KernelExplainer (other models), so method and explainer variant are confounded for SHAP. Adjust any wording that calls every evaluated method model-agnostic. | Prose only. |
| M4 | Section 08, coverage and global evidence | State that Anchors missingness (7/15 on logreg and on MLP) is not random, that block means for Anchors rest on fewer seeds, and the bias bound the thesis reports (tau = 0.90 probe) or a pointer to it. | Any number used must be registered or cited as unbacked. |
| M5 | Section 08 SHAP-LIME paragraph; Table 4 follow-up row | Replace "motivado por la revisión" with an explicit label: exploratory, post hoc, not part of the frozen protocol, reported for direction only. | Prose only. |

### R2. Reader-facing register (Medium, M9)

Remove sentences addressed to the author or describing the book format. Current
instances in the reviewed build:

- `04`: "El capítulo debe cuidar especialmente el lenguaje al interpretar DiCE".
- `05`: the subsection "Implicación para el capítulo" ("El capítulo debe presentar...").
- `06`: "Dentro de este capítulo, FOM-7 debe presentarse como protocolo...".
- `08`: "En un artículo empírico, esta sección podría presentarse..." and
  "La implicación para un capítulo de libro es conceptual".
- `09`: "la pregunta editorialmente más valiosa para un capítulo de libro".

Also:

- Keep the device "no se dice X, sino Y" at most once (it appears in 04, 06 and 09).
- Remove repository paths and code identifiers from prose (`manifest.yaml`,
  `results.json`, `outputs/batch_results.csv`, `logreg_anchors`, `mlp_shap`/
  `svm_shap`, `logreg`, `rf`...), replacing them with plain-language names. Code
  identifiers may appear only in a technical box or the reproducibility note.
- Define or remove thesis labels (P1, H1-H3) before first use; in the chapter they
  appear in section 06 before Table 4 defines them.
- Remove duplicated arguments between old section 05 and new 02-03 ("el nombre del
  método deja de ser una unidad experimental suficiente" and "dos excesos
  simétricos" each occur twice).

### R3. Promised scope (Critical, C2)

Closed by Phases 3 and 4 (sections 04 and 06) as already planned. Additional
requirements from the review:

- The roadmap in section 02 ("examina después áreas de aplicación... organiza las
  brechas...") and the section 03 closing paragraph must match the final headings
  exactly. Re-check both after sections 04 and 06 exist.
- The user requirement "expected future uses of XAI" must be answered at field level
  in section 04 (horizons per domain) and section 10 Part B, not only as future work
  for the benchmark.
- Rewrite the Resumen so that it mentions applications and gaps, which the title now
  promises.

### R4. Reader-experience devices

1. **Worked example across methods (section 05):** one Adult instance explained by
   LIME, SHAP, Anchors and DiCE side by side (weights, attribution, rule,
   counterfactual). Generate it from the committed models and a committed script
   with a fixed seed, or label it explicitly as illustrative. Any printed value is a
   result-shaped literal and must be registered or declared illustrative before
   coverage runs.
2. **One claim traced through the seven gates (section 07):** follow "SHAP supera a
   LIME en fidelidad" from cell artifacts to Table 4, one sentence per gate, as a
   figure that replaces the ASCII flow block.
3. **Plain-language consequence after each key result (section 08):** e.g. a block
   stability near 0.014 means that two explanations of nearly the same case share
   almost no feature ranking.
4. **Decision guide (section 09):** a table from question type to relevant evidence,
   explanation family, and what the benchmark can and cannot say.
5. **Technical boxes (sections 07-08):** statistical plan, gate artifacts, and the
   SHAP-variant detail move to boxes so the main text carries the argument.
6. **One running applicant:** introduced in section 02 or 04 (credit decision),
   explained in section 05, and revisited in section 08.

### R5. Figures for print (High, H4; Medium, M8)

- Design every chapter figure for grayscale in the generator; stop greyscaling colour
  images inside the build (`monochrome_embedded_images`), except as a safety check.
- Figure 1: text colour chosen by cell luminance (white on dark cells).
- Figure 4: distinct marker shapes and line styles, no colour-only legend; replace
  symmetric SD bars on the log axis with interquartile or min-max bars, or plot on a
  linear axis.
- Figure 3: label the printed values as medians or remove them; register any value
  that stays.
- Remove titles and CSV filenames from inside the images; APA figure number, title
  and note belong to the caption.
- Apply the Phase 5 figure selection first (coverage, one global comparison, one
  multi-metric profile) so that only retained figures are regenerated.

### R6. APA 7 corrections (Medium, M7; Low, L3)

Verified against Crossref or DataCite on 2026-09-29 unless marked otherwise:

- Arrieta et al. (2019) -> Barredo Arrieta, A., et al. (2020), *Information Fusion*,
  58, 82-115 (in-text: Barredo Arrieta et al., 2020).
- Kohavi & Becker (1996) -> Becker, B., & Kohavi, R. (1996). *Adult* [Data set]. UCI
  Machine Learning Repository. https://doi.org/10.24432/C5XW20 (in-text: Becker &
  Kohavi, 1996).
- Schwalbe & Finzel (2023) -> (2024), vol. 38, no. 5, pp. 3043-3101 (issue year).
- Lundberg & Lee (2017): cite *Advances in Neural Information Processing Systems 30*
  (NeurIPS 2017), not arXiv; author "Lee, S.-I." (confirm pages against the
  proceedings; not Crossref-indexed).
- Mothilal et al. (2020): fix the rendered "Transparency\*" (Markdown asterisk in
  "FAT\*").
- Remove or cite Adadi & Berrada (2018) and Belle & Papantonis (2021): both are
  listed and uncited in the reviewed build.
- Figure captions to APA: bold number and italic title above the figure, *Nota.*
  below; not "Fuente:" inside an italic caption below the image.
- Low: en dashes in page ranges; article numbers (Belle 688969, Marcinkevičs e1493,
  Canha); Ribeiro et al. (2016) pages 1135-1144 with "In"; Agarwal et al. (2022)
  volume and pages; Zheng et al. (2025) ICLR/OpenReview record instead of the project
  page; Wachter et al. as *Harvard Journal of Law & Technology*, 31(2).

### R7. Word layout (Medium, M6; Low, L1, L2, L5)

Superseded in part on 2026-09-30 by E-FMT: the page geometry, typeface and heading
format now follow the TintAzul/CIFIE template (A4, Cambria 12 pt), and page numbers
are optional. The table, code-block and header-part items below remain.

- ~~Set page size and margins explicitly~~ A4 with the template margins (E-FMT).
- ~~Add decimal page numbers in the footer~~ optional; the template has none.
- Table 2: widen "Propósito" (currently 2.35 cm) at the expense of "Artefacto de
  salida"; no column may break a word.
- Code blocks: left-aligned, never justified; replace the FOM-7 flow block with the
  R4 figure.
- Keep-with-next on table number and title, and on the header row, so no table title
  is stranded (Table 3 on p. 45); keep table notes with the last row (Table 2 note
  split across pp. 32-33).
- Tables stay left-aligned inside cells (deliberate exception to the justified
  standard, recorded here); references stay justified unless the author accepts
  left alignment to avoid the wide gaps around DOIs.
- Stop python-docx from creating empty header/footer parts, or fill them with the
  page number; refresh `docProps/app.xml`.

### Tracking-document reconciliation (M10)

- `sources/evidence_map.md`: update statuses marked "Pendiente de verificar" and
  remove the retracted phrase "inestabilidad estructural".
- `references/citation_audit.md`: drop `altukhi2025`; add the sources promoted on
  2026-09-28.
- `manuscript/chapter_outline.md` on other lanes still states 7,000-8,500 words;
  the recorded decision is no word limit with a 14,000-16,000 working range.

## Execution phases

### Phase 0: Baseline and protection checks

- Run the three project verifiers before any manuscript edit.
- Record the current build, word count, headings, citations, tables, and figures.
- Confirm the chapter branch remains current with the trunk-owned claim substrate.
- Freeze the accepted chapter requirements in the planning record.

**Exit criterion:** clean baseline and no substrate drift.

### Phase 1: Claim-evidence architecture

- Complete literature work packages L1-L4.
- Create a section-level matrix linking every planned major claim to evidence.
- Decide which examples are illustrative and which report empirical findings.
- Propose bibliography additions before drafting prose.

**Exit criterion:** no planned major section lacks an evidence base.

### Phase 2: Structural rewrite

- Revise `manuscript/chapter_outline.md` and the editorial design sheet.
- Reassign current material to the target architecture.
- Remove duplicated exposition before adding new prose.
- Preserve table markers and protected result sites during moves.

**Exit criterion:** the assembled outline tells the broad XAI-to-FOM-7 story without
depending on the empirical results to explain why XAI matters.

### Phase 3: General overview and applications

- Rewrite sections 02 and 03.
- Create the future-facing application section with bounded examples.
- Introduce a compact stakeholder-purpose matrix if it improves comprehension.
- Use citations at the point of each scientific claim; avoid citation dumping at the
  end of long paragraphs.

**Exit criterion:** a non-specialist technical reader can explain what XAI is, why it
matters, who explanations are for, and why one explanation cannot serve every need.

### Phase 4: Gaps and FOM-7 bridge

- Rebuild the crisis section as the seven-part gap taxonomy.
- Map FOM-7 gates to the gaps they address and explicitly identify gaps FOM-7 does
  not solve, especially human usefulness, causal validity, and deployment impact.
- Keep the distinction between functional, human-grounded, and
  application-grounded evaluation visible.

**Exit criterion:** FOM-7 appears as a justified response with explicit boundaries,
not as a universal XAI framework.

### Phase 5: Empirical case compression

- Combine the design and findings into a focused case study.
- Retain protected statistics only where they demonstrate a methodological lesson.
- Prefer synthesis over repeated method profiles.
- Keep aggregation level, source, and scope explicit for every number.

**Exit criterion:** the case study demonstrates the argument without dominating it.

### Phase 6: Discussion, limitations, and conclusion

- Separate practical implications from speculative future work.
- Turn the gap taxonomy into a prioritized research agenda.
- Rewrite the conclusion around the broad scientific thesis and then state the
  bounded FOM-7 contribution.
- Rewrite the abstract last.

**Exit criterion:** every conclusion is proportionate to the evidence and the chapter
answers all author requirements directly.

### Phase 7: Word rendering aligned with the thesis

- Extend the chapter build with a chapter-specific DOCX formatting stage.
- Reuse compatible thesis standards without importing thesis-only front matter:
  justified body text, 1.5 line spacing, consistent heading styles, decimal page
  numbers, centered captions and figures, readable APA tables, and hanging-reference
  indents.
- Decide whether to use the thesis reference DOCX directly or a chapter-specific
  derivative after visual comparison.
- Render and inspect every page, including table breaks, figure sizing, captions,
  headings, references, and widow/orphan behavior.

- Apply R7 (page geometry, page numbers, Table 2 widths, keep-with-next, code-block
  alignment) and R5 (figures regenerated for grayscale).
- Render through Microsoft Word (for example, export to PDF via Word automation on a
  scratch copy); a LibreOffice or python-docx inspection is not sufficient.

**Exit criterion:** the Word document is visually coherent with the thesis and has no
layout defect hidden by a successful build exit code, on a Word render.

### Phase 8: Scientific and submission verification

- Run `verify_claims.py`, `verify_sync.py`, and
  `verify_exp4_reconstruction.py` after protected edits.
- Run the chapter build and inspect the generated Word document.
- Perform a full Scientific Advisor rigor review.
- Perform a final reference audit.
- Confirm the chapter contains no protected Paper B+C result.
- Rebuild from a clean checkout of the lane and confirm the output matches the
  reviewed build (R0).
- Re-check every open finding of the 2026-09-29 review by ID and record its outcome.

**Exit criterion:** verifiers green, scientific-review findings resolved or explicitly
accepted, APA 7 audit clean, and final Word output visually approved.

## Proposed quality gates

### Content gate

- The chapter defines XAI, interpretability, transparency, and post-hoc explanation.
- It explains at least four distinct reasons XAI matters.
- It includes at least five evidence-grounded application examples.
- It presents a structured field-gap taxonomy.
- It retains FOM-7 and the empirical case without claiming universal validity.

### Evidence gate

- Every major factual claim has a traceable source.
- Broad claims rely primarily on systematic reviews or authoritative frameworks.
- Concrete examples rely on domain or primary evidence.
- Counterevidence is represented where the literature is contested.
- No future claim is presented as an established outcome.
- Results available only in the unpublished thesis are labelled as such at first use
  and never carry a confirmatory decision without their statistics.
- Post hoc or exploratory analyses are labelled as such where they are reported.
- Every number states its aggregation level and cohort (EXP1 vs EXP2 subset vs
  EXP2 pooled).
- Causal language ("origen", "causa", "explica por qué") is used only where the
  design supports it.

### Readability gate

- Each section has one clear argumentative function.
- Repeated definitions and conclusions are consolidated.
- Technical terms are defined before use.
- Examples follow a consistent decision-stakeholder-risk-evidence pattern.
- Tables synthesize repeated comparisons instead of duplicating prose.
- No sentence addresses the author or describes the book format ("el capítulo
  debe...", "para un capítulo de libro...").
- No repository path, file name or code identifier appears in prose, captions or
  figure images outside a technical box.
- Thesis labels (P1, H1-H3, EXP1, EXP2) are defined before first use or replaced.
- Each key result is followed by its practical meaning for a reader.
- The roadmap in section 02 matches the final headings.

### Figure gate

- Every figure is legible in grayscale print without relying on colour.
- Every data label in a figure is registered or removed, and every figure has a
  committed generator.
- Error bars are valid on the plotted scale and their statistic is stated.
- Figure number, title and note follow APA 7 and are not duplicated inside the image.

### Reproducibility gate

- The final DOCX builds from a clean checkout of the chapter lane with declared
  dependencies and no step outside committed scripts.
- The build commit hash is recorded with the reviewed file.

### Render gate

- Visual QA is performed on a Microsoft Word render of every page.
- Page size, margins and page numbers are explicit in the document.
- No table or code block breaks a word; no table title or note is separated from its
  table.

### Publication gate

- APA 7 in-text and reference formatting is consistent.
- No cited source is missing and no uncited reference remains.
- All DOI and stable URLs resolve at final audit.
- The Word render meets the agreed thesis-like formatting standard.

### Regression gate

- Chapter `[coverage]` passes.
- Chapter `[exclusivity]` passes.
- Any numeric change is registered before prose is finalized.
- Shared substrate and chapter-body changes remain in separate commits.

## Risks and controls

| Risk | Impact | Control |
| --- | --- | --- |
| Broadening creates a generic XAI survey | High | Keep the evidence-audit thesis and FOM-7 as the organizing contribution. |
| Applications become promotional | High | Pair every benefit example with a failure mode and evidentiary limit. |
| Too many citations reduce readability | Medium | Use claim-centered source selection and synthesis tables. |
| New literature introduces unsupported novelty claims | High | Verify metadata and use wording such as “this chapter proposes” only after a scoped novelty check. |
| Empirical compression loses protected context | High | Preserve registered values, aggregation labels, and claim counts; run verifiers after moves. |
| Word formatting diverges from the thesis | Medium | Reuse tested formatting rules and perform page-by-page visual QA. |
| Source inventory remains inconsistent | Medium | Reconcile planning artifacts before the new literature pass. |
| Uncommitted revision work is lost or diverges between worktrees | High | R0 first; commit per section unit; build only from committed state. |
| A retired value survives because a guard matches too narrowly | High | Guards match the bare value plus unit and list chapter files; negative-test each widened guard. |
| Renderer differences hide layout defects | Medium | Render gate: Word render only, explicit page geometry. |
| Worked example introduces unregistered numbers | Medium | Generate from committed models and script, register or label as illustrative before coverage runs. |
| Unpublished thesis results read as validated evidence | Medium | Label at first use; keep statistics in the thesis citation, not decisions without data. |

## Immediate next action

The evidence-backed rewrite of sections 02 and 03 is complete. The integrated unit now
defines XAI and its boundaries, explains why explanation is purpose-, audience-, and
risk-dependent, distinguishes trust from trustworthiness, and connects explanation to
the AI lifecycle. Six sources used in the prose were promoted into both production
bibliographies, and the candidate literature, evidence map, source inventory, and
citation audit were reconciled. The reader-facing Word build has also been regenerated
and visually inspected across all 48 pages; table widths, figure captions, bibliography
formatting, and the critical-difference diagram are readable and free of internal paths.

**Revised order after the 2026-09-29 review:** R0 (commit and reproducible build),
then R1 (evidence corrections H1, H2, M1-M5) and R2 (drafting voice and repository
vocabulary). Only then does Section 04 start. R3-R7 follow the phases as mapped in
"Review remediation workstream".

The next section-level unit after R0-R2 is Section 04, **Application horizons and
concrete examples**. It will use the repeated decision-stakeholder-risk-evidence-gap structure
for health and biomedicine, finance and consequential allocation, cybersecurity and
critical infrastructure, autonomous and industrial systems, and foundation/language/
multimodal models. Sources will be promoted into the APA 7 bibliography only when they
are cited in production prose, and each claimed benefit will be paired with its
scientific limitation or failure mode.

### Checkpoint verification

- `verify_claims.py`: 320 claims re-derived, 491 manuscript sites checked, 35
  retired-value guards clear, 13 cited artifacts present, 21 files fully registered,
  and 15 files clear of unpublished results.
- `verify_sync.py`: paper and thesis fragments remain synchronized.
- `verify_exp4_reconstruction.py`: all 18 available source hashes match the protected
  reconstruction record.
- `scan_shared_literals.py --strict`: 0 unexplained matches and 53 known
  coincidences.
- Production bibliography: 48 BibTeX records and 48 APA 7 entries.
- Word QA: 11 sections, 4 tables, approximately 18,548 words, and 48 rendered pages.
- Top-level scope sweep: title, central thesis, objectives, outline, and README retain
  the same bounded claim; no explanation is equated with trust, correctness, causal
  validity, safety, or universal method superiority.
