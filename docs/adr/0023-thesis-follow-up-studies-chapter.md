# 23. The Thesis Reports the Later Studies in a Follow-up Chapter

Date: 2026-10-12
Status: Accepted. The author confirmed the four points on 2026-10-12: a chapter of its
own, no new objective, the three study names, and the length of the chapter. The tutor
agreed to them (reported by the author, 2026-10-12).

## Context

Three studies were completed after the thesis text was last edited (2026-09-27): explanation
quality on misclassified instances, agreement between SHAP and LIME on the same instance,
and agreement of method rankings across 16 datasets. The inter-judge study also gained
later controls on its second cohort. The author requires every paper of the project to be
reflected in the thesis. The tutor has approved the current text and singled out, as its
main strength, that it separates what was planned from what was found later.

## Decision

1. **A new chapter**, `thesis/estudios-de-seguimiento.qmd`, between the taxonomy chapter
   and the conclusions, reports the three studies and the later controls. The conclusions
   render as Chapter 7.
2. **No objective, hypothesis or proposition is added or reworded.** The studies are tied
   to the closing clause of the general objective (delimiting the scope of validity) and
   are declared as later than the plan frozen at FOM-7 gate 1. Each had its own analysis
   plan committed before its results; analyses added afterwards are marked post hoc.
3. **Names** (extends the table of ADR-0012): Estudio de Fiabilidad ante el Error,
   Estudio de Concordancia entre Explicadores, Estudio de Transferencia entre Conjuntos
   de Datos. The thesis still names no paper.
4. **File names are not renumbered.** `capitulo-6-conclusiones.qmd` keeps its name.
5. **Numbers are mirrored from the paper claims by a generator**, not typed:
   `scripts/pubs/register_thesis_followup.py` writes the block `thesis_followup` of
   `pub/claim_registry.toml` from the ids listed in `pub/thesis_followup_claims.toml`,
   copying resolver, value and tolerance, and CI runs its `--check`.

## Consequences

- RCA-001 says a quantity in more than one manuscript is registered once. The paper
  blocks are generated and are rewritten by their builds, so they cannot list a thesis
  site. A mirrored claim is the same resolver and the same value under a second id, kept
  equal by the generator; the invariant holds in substance, not in letter.
- If a paper is revised and a value changes, the check fails until the thesis prints the
  new value.
- The file name of the conclusions no longer matches its chapter number.
- Before deposit, the author checks the prior-publication policy of each journal that has
  a paper of the project under review.

## Alternatives rejected

- **Design in Chapter 3, results in Chapter 4.** Mixes later results into the
  confirmatory chapters.
- **New specific objectives OE7 to OE9.** An objective stated after its result.
- **Hand-written thesis claims.** Nothing would tie them to the paper values.
- **Editing the generated paper blocks.** The paper builds overwrite them and their CI
  checks fail.
