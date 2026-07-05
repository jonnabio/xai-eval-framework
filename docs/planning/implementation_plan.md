# Implementation Plan: Manuscript Editing Skill Rename

> **Status:** Completed
> **Created:** 2026-07-04
> **Author:** Scientific Editor
> **PRD Reference:** .ace/skills/manuscript-editing/SKILL.md

---

## Overview

Rename the project-local `cifie-manuscript-editing` skill to the reusable `manuscript-editing` skill while preserving CIFIE/FOM-7 behavior as a project profile.

---

## Prerequisites

- [x] Requirements analyzed and understood
- [x] Existing skill and `.aceconfig` trigger paths inspected
- [x] Regression guards reviewed
- [x] Environment ready
- [x] Rename scope identified

---

## Tasks

<task id="1">
  <name>Rename manuscript editing skill</name>
  <objective>Generalize the CIFIE-specific skill into a reusable manuscript editing skill with a CIFIE/FOM-7 project profile.</objective>
  <files>
    <modify>.ace/skills/manuscript-editing/SKILL.md</modify>
    <modify>.ace/skills/manuscript-editing/agents/openai.yaml</modify>
    <modify>.aceconfig</modify>
    <modify>docs/context/ACTIVE_CONTEXT.md</modify>
  </files>
  <tests>
    <test>Validate `.ace/skills/manuscript-editing` with the skill-creator quick validator.</test>
    <test>Verify old `cifie-manuscript-editing` references are removed from `.ace` and `.aceconfig`.</test>
  </tests>
  <acceptance_criteria>
    <criterion>The skill name and folder are `manuscript-editing`.</criterion>
    <criterion>The CIFIE/FOM-7 constraints remain available as a project profile.</criterion>
    <criterion>ACE triggers point to `.ace/skills/manuscript-editing/SKILL.md`.</criterion>
  </acceptance_criteria>
  <complexity>S</complexity>
  <dependencies>None</dependencies>
</task>

---

## Verification Plan

After all tasks complete:

- [x] Skill validation passes
- [x] `.aceconfig` trigger mappings updated
- [x] Documentation updated
- [x] ACTIVE_CONTEXT.md updated
- [x] Acceptance criteria verified

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| Generic skill loses CIFIE-specific safeguards | M | H | Preserve CIFIE/FOM-7 behavior as an explicit project profile |
| Old skill path remains in triggers | L | M | Verify references after rename |

---

## Open Items

- [ ] Decide later whether `.ace/` and `.aceconfig` should remain local-only or become project-tracked artifacts.

---

## Approval

| Role | Name | Date | Status |
| ---- | ---- | ---- | ------ |
| Scientific Editor | Codex | 2026-07-04 | Completed |

---

_Implementation Plan - ACE-Framework v2.3_
