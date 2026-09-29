# Science-First Revision Plan for the CIFIE XAI Book Chapter

**Status:** Active - Phase 1 complete; Phase 2 architecture gate complete

**Created:** 2026-09-28

**Lane:** `chapter/cifie-sync-2026-09`

**Input assessment:** `planning/general_assessment_2026-09-28.md`

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

**Exit criterion:** the Word document is visually coherent with the thesis and has no
layout defect hidden by a successful build exit code.

### Phase 8: Scientific and submission verification

- Run `verify_claims.py`, `verify_sync.py`, and
  `verify_exp4_reconstruction.py` after protected edits.
- Run the chapter build and inspect the generated Word document.
- Perform a full Scientific Advisor rigor review.
- Perform a final reference audit.
- Confirm the chapter contains no protected Paper B+C result.

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

### Readability gate

- Each section has one clear argumentative function.
- Repeated definitions and conclusions are consolidated.
- Technical terms are defined before use.
- Examples follow a consistent decision-stakeholder-risk-evidence pattern.
- Tables synthesize repeated comparisons instead of duplicating prose.

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

## Immediate next action

Phase 0 and Phase 1 are complete. The source inventory and evidence map are reconciled,
and seventeen sources are staged without creating uncited bibliography entries. The
targeted primary pass closed or narrowed the operational claims in cybersecurity,
autonomous systems, distribution shift, and LLM faithfulness. The production outline,
editorial design sheet, scope statement, and migration map now implement the approved
science-first architecture while preserving the eleven-file build contract.

The next section-level unit is the evidence-backed rewrite of sections 02 and 03,
including transfer of only the sources actually cited into the production APA 7
bibliographies. Section 04 follows as the new application section. A release Word
render is intentionally deferred until that first integrated prose unit is complete;
before then, the new title and architecture would be paired with the legacy body and
would not constitute a coherent review artifact.

### Checkpoint verification

- `verify_claims.py`: 257 claims re-derived, 429 manuscript sites checked, all
  exclusivity guards clear.
- `verify_sync.py`: paper and thesis fragments remain synchronized.
- `verify_exp4_reconstruction.py`: all 18 available source hashes match the protected
  reconstruction record.
- Top-level scope sweep: title, central thesis, objectives, outline, and README retain
  the same bounded claim; no explanation is equated with trust, correctness, causal
  validity, safety, or universal method superiority.
