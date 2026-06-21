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

## Approval

| Role | Name | Date | Status |
| ---- | ---- | ---- | ------ |
| Architect | Codex | 2026-06-20 | Completed |
| Stakeholder | Jonathan Herrera-Vásquez | 2026-06-20 | Approved for scaffolding |

---

_Implementation Plan - ACE-Framework v2.3_
