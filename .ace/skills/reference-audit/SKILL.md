---
name: reference-audit
description: Audit a manuscript's bibliography - duplicate entries, orphaned (cited but undefined) and unused (defined but uncited) references, APA 7 consistency, and re-verification of metadata against scholarly databases via the paper-lookup skill. Produces docs/review/reference-audit_*.md. Report-only unless explicitly told to edit.
metadata:
  project: xai-eval-framework
  role: Scientific Advisor
  rebuilt: 2026-09-27 (original was local-only and lost; see docs/context/ACTIVE_CONTEXT.md)
---

# Skill: Reference Audit

> Make every citation resolvable, every reference used, every entry unique
> and correctly described.

Triggers (`.aceconfig`): references, bibliography, duplicate citations,
citation dedup, reference audit.

## Scope by document

| Document | Citations | Bibliography |
|---|---|---|
| Thesis | `@key` in `thesis/*.qmd` | `thesis/references.bib` |
| Paper B+C | `\citep`/`\citet` in `docs/reports/paper_bc/*.tex` | embedded `thebibliography` |
| Paper A | `\cite*` in `docs/reports/paper_a/*.tex` | its `.bib` / embedded list |
| CIFIE chapter | APA 7 author-date in `publications/book_chapters/2026_cifie_xai_fom7/` | `references/` |

## Checks

1. **Orphans:** cited keys with no bibliography entry (these render as `??` or
   bare keys; also confirm against the rendered DOCX/PDF, not only the source).
2. **Unused entries:** bibliography entries never cited.
3. **Duplicates:** the same work under two keys: same DOI, same title after
   case/punctuation normalisation, or same authors + year + near-identical title.
   Also near-duplicate keys (`koo2016` vs `koo2016guideline`) across documents.
4. **APA 7 consistency (thesis, CIFIE):** author list form, year, title case,
   journal italics, volume(issue), pages, DOI as https://doi.org/..., "et al."
   usage for 3+ authors in text.
5. **Metadata re-verification:** for each entry with a DOI, and a sample of
   those without, look the work up with the `paper-lookup` skill
   (`.ace/packs/scientific/paper-lookup/SKILL.md`; Crossref/OpenAlex first).
   Flag mismatched year, title, venue, author order, or a DOI that resolves to
   a different work. Flag preprints cited where a published version exists.
6. **Citation-claim fit (sample):** for the citations carrying the main
   argumentative load, check that the cited work says what the sentence says.

## Report

Write `docs/review/reference-audit_<document>_<YYYY-MM-DD>.md` with a summary
table (counts per check), then one row per issue: key, location(s), problem,
evidence (lookup result), proposed fix.

## Rules

- Report-only by default. Do not edit `.bib` files, embedded bibliographies or
  manuscripts unless the author explicitly asks for the fixes.
- When fixes are requested: change citation keys consistently across every
  file that uses them, re-render, and re-run the orphan check on the rendered
  output.
- Never invent metadata; an entry that cannot be verified is reported as
  unverified, not corrected by guess.
