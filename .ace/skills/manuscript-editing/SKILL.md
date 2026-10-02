---
name: manuscript-editing
description: Revise academic manuscripts (Spanish and English) for the XAI evaluation publications - the CIFIE/FOM-7 book chapter, the thesis and the papers. Covers academic prose revision, APA 7 consistency, evidence traceability to artifacts and the claim registry, open-access literature enrichment, preservation of FOM-7 terminology, and submission-readiness checks.
metadata:
  project: xai-eval-framework
  role: Scientific Editor
  rebuilt: 2026-09-27 (original was local-only and lost; see docs/context/ACTIVE_CONTEXT.md)
---

# Skill: Manuscript Editing

> Improve the manuscript without changing what the evidence supports.

Triggers (`.aceconfig`): cifie, book chapter, manuscript editing, publication
editing, academic manuscript, citation editing, literature enrichment.

## Documents and conventions

| Document | Location | Language / style |
|---|---|---|
| CIFIE/FOM-7 book chapter | `publications/book_chapters/2026_cifie_xai_fom7/` | Spanish, APA 7 |
| Thesis | `thesis/*.qmd` (Quarto -> DOCX via `thesis/render.ps1`) | Spanish prose; English interaction and commits |
| Paper B+C (Inteligencia Artificial, IBERAMIA) | `docs/reports/paper_bc/` | English with a Spanish Resumen, `iberamia.sty`, double-blind, numbered citations |
| Paper A | `docs/reports/paper_a/` | English |

Branching follows ADR-0013: manuscript bodies are branch-private; `pub/`,
`scripts/pubs/`, `docs/rca/` are shared substrate and never share a commit
with a manuscript body.

## Non-negotiables

1. **Numbers.** Every result-shaped number must be registered in
   `pub/claim_registry.toml` before it reaches prose (RCA-001). After any
   numeric edit run `python scripts/pubs/verify_claims.py`; a value that also
   appears elsewhere needs a pinned `count`.
2. **Abstracts.** The thesis Resumen/Abstract and paper abstracts are authored
   in `pub/claims.toml`, mirrored ES/EN, and regenerated with
   `scripts/pubs/generate_fragments.py`. Never hand-edit `pub/fragments/`.
   LaTeX macros inside TOML strings use doubled backslashes (RCA-003).
3. **Top-level statements.** Rescoping or retracting a claim triggers
   `docs/review/top-level-statement-sweep.md`.
4. **Terminology.** Preserve FOM-7 terms and the functional study names fixed
   by ADR-0012 (Estudio Omnibus Multimétrico, Estudio Pareado LIME–SHAP,
   Estudio Taxonómico, Estudio de Fiabilidad Inter-juez); never letters.
   Chapter/section numbers are generated, never typed.
5. **Scope.** Keep validity boundaries: results hold for the benchmark and
   conditions tested; exploratory results (P2/EXP4, EXP3) stay exploratory.
   Name the aggregation level (block vs run, mean vs median) wherever a number
   could be read at more than one level.
6. **Evidence first.** Prose may be tightened; claims may not be strengthened
   beyond their artifact. A persuasive sentence is not evidence.

## Procedure

1. Read the section in full and its guards in `docs/rca/regression-guards.yaml`.
2. Revise for clarity, precision and academic register; in Spanish, prefer
   precise nominal style without calques; keep terms consistent with the
   thesis glossary and prior chapters.
3. APA 7: author-date in-text citations, reference list consistency (use the
   `reference-audit` skill for a full pass).
4. Literature enrichment: add open-access, verifiable sources only, looked up
   with `.ace/packs/scientific/paper-lookup/SKILL.md`; add each to the
   bibliography and confirm it resolves in the rendered output.
5. Render (thesis: `thesis/render.ps1`; papers: Tectonic per `BUILD.md`) and
   read the changed pages in the rendered output, not only the source.
6. Submission readiness (papers): run the "After any revision" checklist in
   `docs/reports/paper_bc/IBERAMIA_SUBMISSION.md` and report the result.

## Output

The edited manuscript on its lane, verifiers green, and a short change note in
the commit message that says what changed and why, and which numbers (if any)
were registered.
