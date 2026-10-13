# Plan: reflect every paper in the thesis, and close the thesis

**Date:** 2026-10-12. **Role:** Architect (plan), then Scientific Editor (text) and
Developer (registry, checks). **Lane:** `thesis` (`thesis/rca-001-phase-2`); shared files
in separate commits. **Decision record:** ADR-0023. **Record for the tutor (Spanish):**
`docs/review/tesis_cambios_para_tutor_2026-10-12.md`.

## 1. Request

The author (2026-10-12): all the papers must be reflected in the thesis; what changes must
be documented so the details can be sent to the tutor; the three open points before
deposit must be addressed (the thesis figures changed by a chapter session, the coverage
sweep of the files not yet swept, the final pass).

The tutor's last note (2026-10-12) asks for no change. It names four strengths: the
SHAP-LIME follow-up test declared as a follow-up and not as a pre-specified test; the
threats to validity with control and residual risk; FOM-7 as an auditable instrument;
the negative result on LLM judges. The plan must not weaken any of them.

## 2. Where each paper stands in the thesis today

| Paper | Subject | In the thesis | Gap |
|---|---|---|---|
| A (published) | Four methods, five metrics, Adult | Estudio Omnibus Multimétrico, Ch. 3 and 4 | None |
| B (under review) | Paired SHAP-LIME on 75 cells | Estudio Pareado LIME–SHAP, Ch. 3 and 4; its two conditional results (latency by model family, LIME stability by dataset and kernel width) in Ch. 4, Ch. 6 and Appendix C | None found; to confirm in the final pass |
| C (submitted) | LLM judges, taxonomy | Estudio Taxonómico and Estudio de Fiabilidad Inter-juez, Ch. 3 and 5, both cohorts | The later analyses of the second cohort are missing: agreement within method, the two degraded-explanation controls, the condition without metrics |
| D (submitted) | Explanation quality on misclassified instances | Not in the thesis | Whole study |
| E (under review) | SHAP-LIME agreement on the same instance | Not in the thesis | Whole study |
| F (under review) | Do method rankings hold across 16 datasets | Not in the thesis; Ch. 3 and 6 still state the Adult-only limit | Whole study, and the limit it answers |

## 3. Design decisions

**D1. One new chapter, placed between the taxonomy and the conclusions.** Title:
"Estudios de seguimiento: alcance de validez de las conclusiones". It holds the three new
studies and the later controls of the inter-judge study, each with question, design,
result, limits. The conclusions become Chapter 7. Reason: Chapters 3 to 5 are the text
the tutor has just approved, and they report the plan frozen at FOM-7 gate 1; the new
studies came after it. A separate chapter keeps "what was planned" and "what was found
later" apart on the page, which is the distinction the tutor praised.
Alternative rejected: design in Ch. 3 and results in Ch. 4, which mixes follow-up results
into the confirmatory chapter.

**D2. No new objective and no new hypothesis.** The three studies are attached to the
closing clause of the general objective ("delimitando explícitamente el alcance de
validez de la evidencia obtenida"), each on one axis: the correctness of the prediction
(D), the choice of explainer for one instance (E), the dataset (F). H1 to H3, P1 and P2
are untouched. Reason: an objective is stated beforehand; adding OE7 to OE9 now would be
the fault the thesis itself names for OE6. Alternative for the author and the tutor: one
exploratory objective OE7, worded like OE6. It is not applied.

**D3. Status stated once and repeated where a result is used.** The studies are later
than the confirmatory plan. Each has its own analysis plan committed before its results
were computed; the analyses added after seeing results are marked post hoc, as in the
papers. None changes the outcome of H1 to H3, P1 or P2.

**D4. Functional names (ADR-0012), no paper named.**

| Name | Question | Source study |
|---|---|---|
| Estudio de Fiabilidad ante el Error | Are explanations less reliable when the model is wrong? | D |
| Estudio de Concordancia entre Explicadores | How far do SHAP and LIME agree on the same instance? | E |
| Estudio de Transferencia entre Conjuntos de Datos | Does the order of the methods hold on other datasets? | F |

**D5. File names are not renumbered.** The new file is
`thesis/estudios-de-seguimiento.qmd`; `capitulo-6-conclusiones.qmd` keeps its name
although it renders as Chapter 7. Chapter numbers are generated; the file name is
infrastructure named in 53 registry sites, the guards and the chapter lane. Same reasoning
as the frozen anchors of ADR-0012.

**D6. Every number comes from the registry.** The new chapter prints only values already
registered for the papers. Their registry blocks are generated and cannot carry a thesis
site, so a new generated block `thesis_followup` mirrors the chosen claims (same
resolver, same value) with the thesis as site: `scripts/pubs/register_thesis_followup.py`,
list in `pub/thesis_followup_claims.toml`, `--check` in CI. The new file goes under
`[coverage]`.

**D7. Scope of Paper F's result is kept as the paper states it:** agreement of rankings
under fixed settings and one evaluation protocol, not a ranking of explanation quality.

## 4. Changes by file

| File | Change | Size |
|---|---|---|
| `thesis/estudios-de-seguimiento.qmd` | New chapter (D1) | about 3,000 words, 4 tables |
| `thesis/_quarto.yml` | Chapter added before the conclusions | 1 line |
| `thesis/introduccion.qmd` | Seven chapters; one sentence on the follow-up studies | 1 paragraph |
| `thesis/capitulo-1-marco-teorico.qmd` | `tbl-estudios`: three rows and a status column; "cuatro estudios" wording; chapter numbers | table and 2 sentences |
| `thesis/capitulo-3-diseno-experimental.qmd` | Validity table: external-validity row points to the new chapter; one paragraph in §Estudios complementarios; chapter numbers | 3 short edits |
| `thesis/capitulo-5-taxonomia.qmd` | One sentence pointing to the later controls; chapter number | 2 sentences |
| `thesis/capitulo-6-conclusiones.qmd` | New subsection on what the follow-up studies add; limitation "Universo experimental acotado", generalisation table, future line 4 and final synthesis updated | about 500 words |
| `thesis/apendices.qmd` | Appendix G: artifacts, scripts and archives of the follow-up studies | 1 table |
| `pub/claims.toml` | Resumen and Abstract: one mirrored sentence, no new number | 2 sentences |
| `pub/claim_registry.toml`, `scripts/pubs/`, CI | D6 | generated |
| `thesis/assets/figures/` (3 files) | Point 2 below | restore |

Not changed: objectives, hypotheses, propositions, the FOM-7 protocol, every result table
of Chapters 4 and 5, the prescriptive criteria.

## 5. The three open points

**Point 2, thesis figures.** Finding: commit `ba418a927` (a chapter session, 2026-10-05)
replaced `fig_cobertura_exp2_es.png`, `fig_correlacion_metricas_es.png` and
`fig_estabilidad_coste_es.png` with the black-and-white print versions made for the book
chapter (byte-identical to the chapter's `figures/bw/` files). The data are the same. In
the grey correlation matrix the label −0.62 is white on light grey and cannot be read.
Action: restore the three colour files from `ba418a927~1`; make
`scripts/generate_spanish_thesis_figures.py` write the thesis folder in colour only.

**Point 3, coverage sweep.** Put under `[coverage]`, one at a time, `apendices.qmd`,
`capitulo-1`, `capitulo-2`, `introduccion.qmd` and the new chapter; triage each with
`verify_claims.py --coverage-report`; register, declare structural, or mark `[[unbacked]]`
with a reason. Any defect found is reported in the tutor record.

**Point 4, final pass.** Top-level statement sweep, rows 1 to 14, with the log updated;
ADR-0012 greps; full render with `thesis/render.ps1`; reading `word/document.xml` for
unresolved references; the table of contents is refreshed by the author in Word.

## 6. Order of work and checks

1. Plan, ADR-0023 (shared commit).
2. Point 2 (thesis commit; generator in a shared commit).
3. New chapter and the edits of section 4 (thesis commits).
4. Registry block, coverage of the new file, Resumen and Abstract, fragments (shared
   commits). `verify_claims.py`, `verify_sync.py`, `verify_exp4_reconstruction.py` green.
5. Point 3, file by file.
6. Point 4.
7. Tutor record finished with what was done; `ACTIVE_CONTEXT.md` and its archive updated;
   pull request to `main`.

## 7. Risks

| Risk | Handling |
|---|---|
| A journal treats results in a deposited thesis as prior publication | The thesis is not deposited. Before deposit the author checks the policy of each journal with a paper under review (B, C, D, E, F). Paper F's comments to the editor state that the thesis is not deposited. |
| The new chapter reopens the tutor's review | The record for the tutor lists every change and states what is untouched. |
| A paper is revised after review and its numbers change | The thesis block is generated from the paper claims: `--check` fails until the thesis text is brought level. |
| The new chapter overstates a follow-up result | D3 and D7; each section carries the limits its paper states. |
| Chapter renumbering leaves a wrong literal chapter number | Every literal "Capítulo N" was listed (2026-10-12) and is checked again in point 4. |
