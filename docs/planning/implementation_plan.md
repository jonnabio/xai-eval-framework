# Implementation Plan: CIFIE Manuscript Editing Skill

> **Status:** Completed
> **Created:** 2026-07-04
> **Author:** Scientific Editor
> **PRD Reference:** publications/book_chapters/2026_cifie_xai_fom7/

---

## Overview

Create a project-local ACE skill for editing the CIFIE/FOM-7 Spanish book chapter manuscript with guidance for academic prose, APA 7 consistency, evidence traceability, and submission readiness.

---

## Prerequisites

- [x] Requirements analyzed and understood
- [x] Existing ACE skill patterns inspected
- [x] Regression guards reviewed
- [x] Environment ready
- [x] Project-local skill location selected: `.ace/skills/cifie-manuscript-editing/`

---

## Tasks

<task id="6">
  <name>Synchronize thesis, Paper A, and Paper B+C</name>
  <objective>Create a claim-level sync matrix and align validation-boundary wording across the thesis, Paper A, and the merged Paper B+C manuscript.</objective>
  <files>
    <create>docs/reports/sync/thesis_paper_sync_matrix.md</create>
    <modify>thesis/capitulo-3-diseno-experimental.qmd</modify>
    <modify>thesis/capitulo-6-conclusiones.qmd</modify>
    <modify>docs/reports/paper_a/paper_a_prototype_jmlr.tex</modify>
    <modify>docs/reports/paper_a/paper_a_validity_and_reporting_caveats.md</modify>
    <modify>docs/reports/paper_bc/paper_bc_jmlr.tex</modify>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Verify EXP3 wording is consistent across thesis, Paper A, and Paper B+C.</test>
    <test>Verify no manuscript claims synthetic ground-truth validation, transparent-model recovery, human-centered validation, or a composite metric as completed work.</test>
    <test>Verify shared validation-boundary language remains scoped to functionally grounded comparative evidence.</test>
  </tests>
  <acceptance_criteria>
    <criterion>Each output uses the same distinction between ranking claims and broader validity claims.</criterion>
    <criterion>Paper A remains canonical for benchmark protocol and quantitative evidence; Paper B+C remains canonical for taxonomy and validity-boundary framing; the thesis synthesizes both without contradictions.</criterion>
    <criterion>The sync matrix records the source of truth and action status for major shared claims.</criterion>
  </acceptance_criteria>
  <complexity>S</complexity>
  <dependencies>None</dependencies>
</task>

<task id="1">
  <name>Create CIFIE manuscript editing skill</name>
  <objective>Add a reusable ACE skill for revising and literature-enriching the CIFIE/FOM-7 chapter while preserving workstream constraints.</objective>
  <files>
    <create>.ace/skills/cifie-manuscript-editing/SKILL.md</create>
    <create>.ace/skills/cifie-manuscript-editing/agents/openai.yaml</create>
    <modify>.aceconfig</modify>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Validate the skill folder with the skill-creator quick validator.</test>
    <test>Verify `.aceconfig` contains CIFIE manuscript editing trigger mappings.</test>
  </tests>
  <acceptance_criteria>
    <criterion>The skill can be invoked for CIFIE, book chapter, manuscript editing, and publication editing requests.</criterion>
    <criterion>The skill preserves thesis/paper read-only evidence constraints, FOM-7 terminology, APA 7 discipline, open-access literature verification, and ACTIVE_CONTEXT updates.</criterion>
  </acceptance_criteria>
  <complexity>S</complexity>
  <dependencies>None</dependencies>
</task>

<task id="2">
  <name>Open-access literature enrichment pass</name>
  <objective>Strengthen the CIFIE/FOM-7 manuscript with verified open-access XAI evaluation sources found through Semantic Scholar and cross-checked through Crossref/OpenAlex/Unpaywall.</objective>
  <files>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/manuscript/*.md</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/references/references.bib</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/references/references_apa7.md</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/references/citation_audit.md</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/sources/evidence_map.md</modify>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Verify accepted sources were searched in Semantic Scholar and cross-checked through Crossref/OpenAlex or Unpaywall/OA metadata.</test>
    <test>Verify added manuscript citations have matching bibliography and APA working-list entries.</test>
    <test>Verify edited manuscript sections contain no leftover Pandoc citation keys.</test>
  </tests>
  <acceptance_criteria>
    <criterion>Only verified sources are added as confirmed citations.</criterion>
    <criterion>Accepted and rejected sources are documented in the citation audit.</criterion>
    <criterion>FOM-7 terminology and thesis/paper read-only constraints are preserved.</criterion>
  </acceptance_criteria>
  <complexity>M</complexity>
  <dependencies>Task 1</dependencies>
</task>

<task id="3">
  <name>Revise limitations and future work section</name>
  <objective>Improve `10_limitaciones_trabajo_futuro.md` for academic Spanish prose, stronger in-text citation support, and clearer FOM-7 alignment.</objective>
  <files>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/manuscript/10_limitaciones_trabajo_futuro.md</modify>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Verify the revised section contains no Pandoc citation keys.</test>
    <test>Verify in-text citations correspond to entries in `references/references.bib`.</test>
    <test>Verify thesis and paper artifacts remain read-only.</test>
  </tests>
  <acceptance_criteria>
    <criterion>Section 10 reads as publication-ready Spanish academic prose.</criterion>
    <criterion>Limitations and future work are framed through FOM-7 evidence boundaries, not generic caveats.</criterion>
    <criterion>Claims about metrics, human validation, method sensitivity, and generalization are citation-supported.</criterion>
  </acceptance_criteria>
  <complexity>M</complexity>
  <dependencies>Task 2</dependencies>
</task>

<task id="4">
  <name>Revise introduction section</name>
  <objective>Improve `02_introduccion.md` for academic Spanish prose, stronger in-text citation support, and clearer FOM-7 alignment.</objective>
  <files>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/manuscript/02_introduccion.md</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/sources/evidence_map.md</modify>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Verify the revised section contains no Pandoc citation keys.</test>
    <test>Verify in-text citations correspond to entries in `references/references.bib`.</test>
    <test>Verify thesis and paper artifacts remain read-only.</test>
  </tests>
  <acceptance_criteria>
    <criterion>Section 02 reads as publication-ready Spanish academic prose.</criterion>
    <criterion>The introduction frames FOM-7 as a response to an evidentiary gap in XAI evaluation.</criterion>
    <criterion>Claims about opacity, post-hoc methods, metric fragmentation, benchmarks, and contribution are citation-supported.</criterion>
  </acceptance_criteria>
  <complexity>M</complexity>
  <dependencies>Task 3</dependencies>
</task>

<task id="5">
  <name>Revise technical XAI foundations section</name>
  <objective>Strengthen `03_fundamentos_xai.md` through an iterative literature-enrichment loop, sharpening conceptual distinctions and FOM-7 alignment while preserving APA 7 citation discipline.</objective>
  <files>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/manuscript/02_introduccion.md</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/manuscript/03_fundamentos_xai.md</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/references/references.bib</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/references/references_apa7.md</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/references/citation_audit.md</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/sources/evidence_map.md</modify>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Query Semantic Scholar first and cross-check accepted sources through OpenAlex or Crossref metadata.</test>
    <test>Prefer open-access sources verified through OpenAlex, arXiv, publisher, repository, or comparable OA links.</test>
    <test>Verify section 03 contains no Pandoc citation keys and every in-text citation has a matching reference entry.</test>
  </tests>
  <acceptance_criteria>
    <criterion>Section 03 distinguishes interpretability, explainability, transparency, local/global scope, plausibility, fidelity, stability, robustness, and metric proxies.</criterion>
    <criterion>Section 03 explicitly frames FOM-7 as a protocol for admissible, traceable evidence rather than universal method ranking.</criterion>
    <criterion>Accepted and rejected literature sources are documented with identifiers and verification status.</criterion>
  </acceptance_criteria>
  <complexity>M</complexity>
  <dependencies>Task 4</dependencies>
</task>

---

## Verification Plan

After all tasks complete:

- [x] Skill validation passes
- [x] `.aceconfig` trigger mappings added
- [x] Open-access literature enrichment workflow added
- [x] Open-access literature enrichment pass completed
- [x] Section 10 revision completed
- [x] Section 02 revision completed
- [x] Documentation updated
- [x] ACTIVE_CONTEXT.md updated
- [x] Acceptance criteria verified

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| Skill trigger is too broad and activates on unrelated book chapters | M | L | Keep the skill body scoped to CIFIE/FOM-7 and project paths |
| Manuscript edits introduce unsupported claims | M | H | Require evidence-map and citation-audit checks for claim-sensitive edits |

---

## Open Items

- [ ] Final CIFIE template and word limit remain pending outside this skill task.

---

## Approval

| Role | Name | Date | Status |
| ---- | ---- | ---- | ------ |
| Scientific Editor | Codex | 2026-07-04 | Completed |

---

_Implementation Plan - ACE-Framework v2.3_
