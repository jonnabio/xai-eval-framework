# 12. Thesis Study Nomenclature (Named Studies, No Paper Cross-References)

Date: 2026-08-29
Status: Accepted

## Context

The thesis referred to its constituent studies by bare letters — *Estudio A*,
*Estudio B*, *Estudio C* — and, in two places, by the publication artifact they
feed (*Paper A*, *Paper B*). Three defects followed from this.

**1. Forward references without an antecedent.** The letters first appear on
p. 14, in specific objective OE5 (`thesis/capitulo-1-marco-teorico.qmd`), but
they are only defined in Chapter 3. A reader — or an examiner reading the
objectives in isolation, which is exactly how objectives get read — meets
"marco conceptual integrador para los Estudios A y B" with no way to know what
A and B are. The same holds for the abstract-adjacent chapter roadmap in
`introduccion.qmd`.

**2. Three competing naming systems for the same objects.** The same study was
addressed by letter (Estudio A), by publication artifact (Paper A), and by
experimental phase (EXP1/EXP2), with all three colliding in the opening
sentence of Chapter 3. The mapping between the three was never stated in the
thesis.

**3. The letter scheme no longer closed.** A fourth study exists — the LLM
inter-judge reliability study behind OE6, carried in
`capitulo-5-taxonomia.qmd` §`sec-exp4-fiabilidad` — and it never received a
letter, because it was formulated after the taxonomy was built. It was simply
called "Estudio de fiabilidad de evaluadores semánticos", inconsistently with
its three lettered siblings.

A separate constraint applies to the thesis specifically: **a doctoral thesis
is a self-contained document**. Naming Paper A and Paper B inside it makes the
thesis depend on artifacts that are not part of the deposit, are not in its
bibliography, and — in the case of the merged Paper B+C — no longer exist under
the name the thesis used.

## Decision

**Replace the letter scheme with functional names, applied uniformly across the
thesis, and remove every reference from the thesis to the derived papers.**

### Canonical study names

| Name | Question it answers | Objective | Chapters |
|:---|:---|:---:|:---:|
| **Estudio Omnibus Multimétrico** | Do SHAP, LIME, Anchors and DiCE differ across the five quality metrics over the full factorial design? | OE2 | 3, 4 |
| **Estudio Pareado LIME–SHAP** | How does the quality-cost relationship between LIME and SHAP behave over matched model/seed/sample-size cells? | OE3 | 3, 4 |
| **Estudio Taxonómico** | What conceptual structure organizes the XAI evaluation metric space, and what construct gaps does it reveal? | OE5 | 5 |
| **Estudio de Fiabilidad Inter-juez** | Do LLM-based semantic evaluators reach the inter-judge convergence needed to support confirmatory claims? | OE6 | 3, 5 |

Objectives OE1 (FOM-7 formalization) and OE4 (reproducibility profile) are
**transversal to the two empirical studies** and are deliberately not assigned
to a single one.

### Rules

1. **Full name on first mention** in a chapter or section; lowercase short
   forms (*el estudio omnibus*, *el estudio pareado*, *el estudio taxonómico*)
   thereafter and inside table cells where the full name would overflow.
2. **Section anchors are frozen.** `#sec-estudio-a`, `#sec-estudio-b` and
   `#sec-exp4-fiabilidad` keep their identifiers even though their headings
   were renamed. Anchors are cross-reference infrastructure, not prose; churning
   them breaks `@sec-` references across chapters and the appendices for no
   reader-visible gain.
3. **The thesis names no paper.** Neither "Paper A" nor "Paper B" nor
   "Paper B+C" appears in thesis prose. The thesis stands alone.
4. **The nomenclature table (`{#tbl-estudios}`) in Chapter 1 is the single
   definition site**, placed between the specific objectives and the
   hypotheses — that is, before the first use of any study name in an argument.
5. **Where the contrast is empirical-vs-conceptual rather than the identity of
   a particular study**, prefer "los dos estudios empíricos" over repeating both
   full names. Applied in Chapter 5, where the point is the
   functionally-grounded evidence boundary, not which study produced it.

### Explicitly out of scope

Filesystem paths containing `paper_a` — `outputs/analysis/paper_a_exp2_stats/`,
cited in `apendices.qmd`, `capitulo-3` and `capitulo-4` — are **not** renamed.
They are artifact locations under the RCA-001 invariant *"every artifact path a
manuscript cites exists in the working tree"*, and they are consumed by Paper A
and Paper B+C as well. Renaming the directory is an artifact-migration task
(directory, generating scripts, `pub/claim_registry.toml` resolvers), not a
prose edit, and is not undertaken here.

## Alternatives Considered

### Alternative 1: Keep the letters, gloss them once
Add a definition of A/B/C at first use and leave all 36 sites untouched.
- **Pros:** Near-zero diff; preserves continuity with the published papers,
  which use the letter scheme.
- **Cons:** The name still carries no meaning when it appears in a table cell,
  a figure caption, or a sentence quoted out of context — which is how an
  examiner encounters it. Does not solve the unlettered fourth study.
- **Why rejected:** It treats the symptom (missing antecedent) and not the
  cause (the label is arbitrary).

### Alternative 2: Name + letter on every mention
"el Estudio Omnibus Multimétrico (Estudio A)".
- **Pros:** Backward-compatible with the papers and with prior thesis drafts.
- **Cons:** Doubles the length of every mention across 36 sites; the
  parenthetical letter is dead weight after the glossary.
- **Why rejected:** Offered to the author and declined in favour of the clean
  rename. The correspondence is preserved once, in a note under
  `{#tbl-estudios}`.

### Alternative 3: Name the studies after their experimental phases (EXP1–EXP4)
- **Pros:** One naming system instead of two; already used for artifact paths.
- **Cons:** Phases and studies are not in bijection — the Estudio Omnibus
  Multimétrico and the Estudio Pareado LIME–SHAP both draw on EXP2, and the
  Estudio Taxonómico has no phase at all. The phase names also describe *when
  data was produced*, not *what question is asked*.
- **Why rejected:** Would force a false one-to-one mapping and erase the
  inferential-scope distinction that separates the two empirical studies.

## Consequences

### Positive
- Every study name is self-explanatory at first contact; OE5 no longer depends
  on Chapter 3 to be intelligible.
- The fourth study is named on the same footing as the other three, closing the
  gap the letter scheme could not express.
- The thesis is self-contained: no dangling reference to a paper that is not in
  its bibliography, and no exposure to the Paper B / Paper B+C merge.
- One definition site (`{#tbl-estudios}`) also documents the objective-to-study
  and study-to-chapter traceability that was previously implicit.

### Negative
- Nomenclature now diverges between the thesis and the papers, which retain the
  letter scheme. The correspondence is documented in this ADR and in the note
  under `{#tbl-estudios}` but is not enforced by any script.
- Names are longer than letters; a few table cells use the lowercase short form
  instead, so a reader sees two surface forms of the same name.
- Prior review reports (`docs/review/scientific-rigor-review_thesis_2026-08-11.md`)
  reference the old letters. These are dated records of past state and are
  deliberately **not** rewritten.

### Neutral
- The rename touched no numeric value, table datum or citation. Line counts in
  the diff are inflated by paragraph re-wrapping to the file's ~78-column prose
  width.

## Compliance

- `scripts/pubs/verify_claims.py` and `scripts/pubs/verify_sync.py` must stay
  green across the change; both were re-run after the edit (142 claims
  re-derived, 225 manuscript sites checked, 26 retired-value guards clear;
  fragments wiring intact). Neither script checks nomenclature — they establish
  that the rename was semantically inert with respect to RCA-001.
- Regression check for future edits, from the repository root:

  ```
  grep -rn "Estudios\? [ABC]\b" thesis/*.qmd     # expect only the tbl-estudios note
  grep -rn "Paper A\|Paper B\|Paper C" thesis/*.qmd   # expect no matches
  ```

- Any new study introduced in the thesis must be added as a row to
  `{#tbl-estudios}` with its question, objective and chapters, and must be
  named functionally rather than by letter.

## References

- `thesis/capitulo-1-marco-teorico.qmd` — OE5 wording and the
  `{#tbl-estudios}` nomenclature table (definition site)
- `thesis/capitulo-3-diseno-experimental.qmd`,
  `thesis/capitulo-4-resultados.qmd`, `thesis/capitulo-5-taxonomia.qmd`,
  `thesis/introduccion.qmd` — migrated call sites
- `docs/rca/regression-guards.yaml` — RCA-001, artifact-path invariant that
  keeps `outputs/analysis/paper_a_exp2_stats/` out of scope
- `docs/adr/0011-publication-sync-pipeline.md` — the SSOT/fragment pipeline
  that keeps thesis and paper abstracts aligned; it is unaffected because it
  synchronizes abstracts and keywords, not study labels
- `docs/reports/sync/thesis_paper_sync_matrix.md` — thesis/paper claim mapping,
  which remains the place where the Paper A / Paper B+C correspondence lives
