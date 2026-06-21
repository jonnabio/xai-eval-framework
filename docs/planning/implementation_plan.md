# Implementation Plan: CIFIE XAI FOM-7 Book Chapter Workstream

> **Status:** Completed
> **Created:** 2026-06-20
> **Author:** Architect
> **PRD Reference:** publications/book_chapters/chapter_instructions.md

---

## Overview

Create a separate publication workstream for the CIFIE collective book chapter derived from the doctoral research on model-agnostic XAI evaluation. The workstream will live under `publications/book_chapters/2026_cifie_xai_fom7/` and must not overwrite thesis or paper artifacts.

---

## Prerequisites

- [x] Requirements analyzed and understood
- [x] Existing publication structure inspected
- [x] Regression guards reviewed
- [x] Branch created: `publication/cifie-xai-fom7-book-chapter`
- [x] Stakeholder confirmed normalization of Spanish UTF-8 accents

---

## Tasks

<task id="1">
  <name>Create publication directory structure</name>
  <objective>Establish the independent CIFIE book chapter workstream under publications/book_chapters/2026_cifie_xai_fom7/.</objective>
  <files>
    <create>publications/book_chapters/2026_cifie_xai_fom7/**</create>
    <modify>None outside the new workstream</modify>
  </files>
  <tests>
    <test>Verify the requested directories exist.</test>
  </tests>
  <acceptance_criteria>
    <criterion>No thesis or paper artifacts are overwritten.</criterion>
    <criterion>Requested directory tree exists.</criterion>
  </acceptance_criteria>
  <complexity>S</complexity>
  <dependencies>None</dependencies>
</task>

<task id="2">
  <name>Create manuscript, table, figure, reference, and compliance placeholders</name>
  <objective>Create the requested publication files with normalized Spanish text where content was specified.</objective>
  <files>
    <create>README.md, manuscript/*.md, tables/*.md, references/*.md, references/*.bib, compliance/*.md, figures/figure_registry.md</create>
    <modify>None outside the new workstream</modify>
  </files>
  <tests>
    <test>Verify requested files exist.</test>
    <test>Inspect key files for normalized Spanish accents.</test>
  </tests>
  <acceptance_criteria>
    <criterion>Content-bearing files match the instruction intent.</criterion>
    <criterion>Requested empty manuscript section files remain empty.</criterion>
  </acceptance_criteria>
  <complexity>M</complexity>
  <dependencies>Task 1</dependencies>
</task>

<task id="3">
  <name>Update active context</name>
  <objective>Record the new publication workstream and current branch in ACTIVE_CONTEXT.md.</objective>
  <files>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Verify active context reflects the new workstream without removing existing context.</test>
  </tests>
  <acceptance_criteria>
    <criterion>ACTIVE_CONTEXT.md documents the CIFIE workstream and constraint against overwriting thesis/paper artifacts.</criterion>
  </acceptance_criteria>
  <complexity>S</complexity>
  <dependencies>Tasks 1 and 2</dependencies>
</task>

---

## Verification Plan

After all tasks complete:

- [x] Requested directories exist
- [x] Requested files exist
- [x] Specified Spanish content uses normalized UTF-8 accents
- [x] Placeholder manuscript section files requested as empty are empty
- [x] No existing thesis or paper artifacts modified by this task
- [x] ACTIVE_CONTEXT.md updated

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| Encoding artifacts from the source instruction could enter Spanish publication files | M | M | Normalize Spanish accents manually in created content |
| Existing thesis or paper files could be accidentally touched | L | H | Scope writes to the new publication folder plus ACE planning/context files only |
| The WSL view of `chapter_instructions.md` differs from Windows | M | L | Use the PowerShell-read instruction content as authoritative |

---

## Open Items

- [ ] Editorial template and final CIFIE formatting requirements remain pending.
- [ ] Miguel Herrero-Uceda ORCID remains pending / unavailable.

---

## Follow-up Task: Source Inventory and Evidence Map

> **Status:** Completed
> **Started:** 2026-06-20
> **Role:** Architect

<task id="4">
  <name>Create source inventory and evidence map</name>
  <objective>Prepare section-level planning artifacts that map the CIFIE chapter to thesis, paper, figure, table, reference, and experiment sources without modifying the original artifacts.</objective>
  <files>
    <create>publications/book_chapters/2026_cifie_xai_fom7/sources/source_inventory.md</create>
    <create>publications/book_chapters/2026_cifie_xai_fom7/sources/evidence_map.md</create>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Verify source-planning files exist under the new workstream.</test>
    <test>Verify no thesis or paper source artifacts were edited.</test>
  </tests>
  <acceptance_criteria>
    <criterion>The chapter has a clear section-by-section extraction plan.</criterion>
    <criterion>Empirical claims are mapped to source artifacts requiring verification.</criterion>
    <criterion>Original thesis and paper artifacts remain read-only during this task.</criterion>
  </acceptance_criteria>
  <complexity>M</complexity>
  <dependencies>Scaffold commit bb726805a</dependencies>
</task>

### Verification

- [x] Source inventory exists under the CIFIE workstream.
- [x] Evidence map exists under the CIFIE workstream.
- [x] Original thesis and paper artifacts were used read-only for planning.
- [x] ACTIVE_CONTEXT.md updated with the source-mapping checkpoint.

---

## Follow-up Task: Extraction Pass 1

> **Status:** Completed
> **Started:** 2026-06-20
> **Role:** Developer

<task id="5">
  <name>Populate initial references, citation audit, and metrics table</name>
  <objective>Extract verified bibliography entries and metric definitions from thesis sources before drafting chapter prose.</objective>
  <files>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/references/references.bib</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/references/citation_audit.md</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/tables/table_metrics.md</modify>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Verify BibTeX keys were copied from `thesis/references.bib`.</test>
    <test>Verify `table_metrics.md` reflects thesis metric definitions and source files.</test>
    <test>Verify citation audit distinguishes copied entries from APA/DOI validation still pending.</test>
  </tests>
  <acceptance_criteria>
    <criterion>Initial core references exist in the chapter bibliography.</criterion>
    <criterion>Metrics table is populated before prose drafting.</criterion>
    <criterion>No original thesis, paper, or experiment artifacts were edited.</criterion>
  </acceptance_criteria>
  <complexity>M</complexity>
  <dependencies>Source map commit 6fc27c503</dependencies>
</task>

### Verification

- [x] Core method and evaluation references copied from thesis bibliography.
- [x] Citation audit records pending citation insertion, DOI checks, URL checks, and table source dependencies.
- [x] Metrics table populated from thesis metric definitions.
- [x] Original thesis and paper artifacts were used read-only for extraction.

---

## Follow-up Task: Extraction Pass 2

> **Status:** Completed
> **Started:** 2026-06-20
> **Role:** Developer

<task id="6">
  <name>Populate result summary and figure registry</name>
  <objective>Extract result claims, statistical summaries, method profiles, traceability notes, and candidate figures from `thesis/capitulo-4-resultados.qmd` before drafting prose.</objective>
  <files>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/tables/table_results_summary.md</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/figures/figure_registry.md</modify>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Verify result summaries are traceable to `thesis/capitulo-4-resultados.qmd`.</test>
    <test>Verify figure registry points to existing thesis figure assets.</test>
    <test>Verify no original thesis, paper, or figure assets were edited.</test>
  </tests>
  <acceptance_criteria>
    <criterion>Result summary table is populated before prose drafting.</criterion>
    <criterion>Figure registry identifies candidate figures, source files, and chapter destinations.</criterion>
    <criterion>Original thesis artifacts remain read-only.</criterion>
  </acceptance_criteria>
  <complexity>M</complexity>
  <dependencies>Extraction pass 1 commit 8e51eb1fd</dependencies>
</task>

### Verification

- [x] Coverage, hypothesis decisions, SHAP-LIME paired results, method profiles, and claim traceability extracted.
- [x] Seven candidate Spanish thesis figures registered.
- [x] Figure files were not copied or modified during this pass.
- [x] Original thesis and paper artifacts were used read-only for extraction.

---

## Follow-up Task: Extraction Pass 3

> **Status:** Completed
> **Started:** 2026-06-20
> **Role:** Developer

<task id="7">
  <name>Extract FOM-7 protocol details</name>
  <objective>Populate the FOM-7 manuscript section and reconcile the FOM-7 gates table against thesis protocol details before drafting broader prose.</objective>
  <files>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/manuscript/06_protocolo_fom7.md</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/tables/table_fom7_gates.md</modify>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Verify the seven gates match `thesis/capitulo-3-diseno-experimental.qmd`.</test>
    <test>Verify the manuscript section preserves FOM-7 scope, admissibility rule, and limits.</test>
    <test>Verify no original thesis, paper, or experiment artifacts were edited.</test>
  </tests>
  <acceptance_criteria>
    <criterion>FOM-7 protocol section is populated from verified thesis sources.</criterion>
    <criterion>FOM-7 gates table includes purpose, input, output, controlled failure, and evidence.</criterion>
    <criterion>Original thesis artifacts remain read-only.</criterion>
  </acceptance_criteria>
  <complexity>M</complexity>
  <dependencies>Extraction pass 2 commit b91a27f94</dependencies>
</task>

### Verification

- [x] Seven FOM-7 gates extracted and reconciled against the thesis protocol table.
- [x] Sequential admissibility rule included.
- [x] Limits of FOM-7 included to prevent overclaiming.
- [x] Original thesis and paper artifacts were used read-only for extraction.

---

## Follow-up Task: Controlled Drafting Pass 1

> **Status:** Completed
> **Started:** 2026-06-20
> **Role:** Developer

<task id="8">
  <name>Draft XAI foundations and method sections</name>
  <objective>Populate the first two technical manuscript sections from extracted thesis sources and verified chapter references.</objective>
  <files>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/manuscript/03_fundamentos_xai.md</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/manuscript/04_metodos_lime_shap_anchors_dice.md</modify>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Verify both manuscript files are populated.</test>
    <test>Verify citations used are present in chapter `references/references.bib`.</test>
    <test>Verify no original thesis or paper artifacts were edited.</test>
  </tests>
  <acceptance_criteria>
    <criterion>Sections are drafted in Spanish academic style.</criterion>
    <criterion>Drafting remains scoped to foundations and method descriptions.</criterion>
    <criterion>No empirical claims exceed the extracted evidence tables.</criterion>
  </acceptance_criteria>
  <complexity>M</complexity>
  <dependencies>Extraction pass 3 commit 998c91d53</dependencies>
</task>

### Verification

- [x] XAI foundations section drafted.
- [x] LIME, SHAP, Anchors, and DiCE method section drafted.
- [x] Citations limited to entries already present in the chapter bibliography.
- [x] Original thesis and paper artifacts were used read-only for drafting.

---

## Follow-up Task: Controlled Drafting Pass 2

> **Status:** Completed
> **Started:** 2026-06-20
> **Role:** Developer

<task id="9">
  <name>Draft XAI evaluation crisis and bridge to FOM-7</name>
  <objective>Populate the crisis section and lightly revise the FOM-7 protocol section so the argument flows from evaluation fragmentation to protocol governance.</objective>
  <files>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/manuscript/05_crisis_evaluacion_xai.md</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/manuscript/06_protocolo_fom7.md</modify>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Verify crisis-section citations exist in chapter `references/references.bib`.</test>
    <test>Verify the FOM-7 section retains its extracted gate details.</test>
    <test>Verify no original thesis or paper artifacts were edited.</test>
  </tests>
  <acceptance_criteria>
    <criterion>Crisis section explains fragmentation, metric insufficiency, construct gaps, reproducibility, and toolkit-governance limits.</criterion>
    <criterion>FOM-7 section includes a clear transition from crisis diagnosis to protocol solution.</criterion>
    <criterion>Drafting remains scoped to the CIFIE workstream.</criterion>
  </acceptance_criteria>
  <complexity>M</complexity>
  <dependencies>Controlled drafting pass 1 commit b6b5b3c99</dependencies>
</task>

### Verification

- [x] Crisis section drafted.
- [x] FOM-7 opening lightly revised to bridge from crisis diagnosis.
- [x] Citations limited to entries already present in the chapter bibliography.
- [x] Original thesis and paper artifacts were used read-only for drafting.

---

## Follow-up Task: Controlled Drafting Pass 3

> **Status:** Completed
> **Started:** 2026-06-20
> **Role:** Developer

<task id="10">
  <name>Draft empirical design and results sections</name>
  <objective>Populate `07_diseno_empirico.md` and `08_resultados.md` using extracted metrics, FOM-7 gates, and result summaries as evidence controls.</objective>
  <files>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/manuscript/07_diseno_empirico.md</modify>
    <modify>publications/book_chapters/2026_cifie_xai_fom7/manuscript/08_resultados.md</modify>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Verify both manuscript files are populated.</test>
    <test>Verify empirical figures and statistics are traceable to extracted tables.</test>
    <test>Verify no original thesis or paper artifacts were edited.</test>
  </tests>
  <acceptance_criteria>
    <criterion>Design section describes dataset, models, factors, metrics, FOM-7 controls, and inferential plan.</criterion>
    <criterion>Results section reports coverage, hypothesis decisions, method profiles, reproducibility, and quality-cost interpretation.</criterion>
    <criterion>Claims remain within the scope documented in extracted evidence tables.</criterion>
  </acceptance_criteria>
  <complexity>M</complexity>
  <dependencies>Controlled drafting pass 2 commit 1186af587</dependencies>
</task>

### Verification

- [x] Empirical design section drafted.
- [x] Results section drafted.
- [x] Statistics and method profiles use `table_results_summary.md`, `table_metrics.md`, and `table_fom7_gates.md` as controls.
- [x] Original thesis and paper artifacts were used read-only for drafting.

---

## Approval

| Role | Name | Date | Status |
| ---- | ---- | ---- | ------ |
| Architect | Codex | 2026-06-20 | Completed |
| Stakeholder | Jonathan Herrera-Vásquez | 2026-06-20 | Approved for scaffolding |

---

_Implementation Plan - ACE-Framework v2.3_
