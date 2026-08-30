# Scientific Rigor Review: PhD Thesis — "Marco para la Evaluación Multinivel de la Explicabilidad en IA" (FOM-7)

**Date**: 2026-08-11 | **Reviewer role**: Scientific Advisor | **Grade**: Accept
**Mean score**: 4.3 | **Dimensions**: D1=4.5 D2=4.5 D3=4.0 D4=4.0 D5'=5.0 D6=4.0

**Scope reviewed**: `thesis/index.qmd`, `introduccion.qmd`, `capitulo-1-marco-teorico.qmd`,
`capitulo-2-fundamentos.qmd`, `capitulo-3-diseno-experimental.qmd`,
`capitulo-4-resultados.qmd`, `capitulo-5-taxonomia.qmd`, `capitulo-6-conclusiones.qmd`,
`apendices.qmd` — full text, read in sequence.

## One-line summary

A methodologically mature, unusually self-critical doctoral thesis with formally
pre-specified hypotheses, complete claim-to-artifact traceability, and honest reporting of a
negative result (P2); its main weaknesses are internal — a numeric contradiction between
Chapter 4's primary results and Chapter 5's restatement of them, and a "future work" item in
Chapter 6 that describes work the same chapter reports as already completed a few paragraphs
earlier.

## Strengths

- **Pre-registered-style inferential discipline**: formal $H_0$/$H_1$ pairs for H1–H3, a
  falsifiable reproducibility proposition (P1) and a falsifiable calibration proposition
  (P2), a statistical plan fixed before results (Ch.3) that is followed exactly in Ch.4, and
  explicit multiplicity control (Holm–Bonferroni within three named inferential families).
- **Exemplary reporting honesty (D5')**: P2 (LLM-judge inter-rater reliability) is reported as
  **not confirmed** with ICC(2,1) values as low as 0.321 (Ch.5, Ch.6) rather than being
  omitted or softened; LIME's near-zero stability is described as "structural," not glossed
  over; the Ch.6 limitations section discloses that LIME's parsimony is a configuration
  artifact (`num_features=10` ceiling) and that feature-masking fidelity may be confounded by
  correlated features (`education`/`education-num`, $r=1.0$).
- **Full claim traceability**: Table `@tbl-claim-traceability` (Ch.4) and Table
  `@tbl-appendix-stat-outputs` (Appendix D) link every confirmatory claim to a specific CSV
  artifact and generating script — this is the FOM-7 "gate 7" requirement applied to the
  thesis's own prose, and it is genuinely auditable.
- **Missing-data impact is quantified, not asserted**: Ch.3's coverage-impact analysis
  computes the variance inflation factor ($\sqrt{5/2.3}\approx1.47$) from Anchors' reduced
  replicate count and shows the Friedman statistic would remain significant even under a
  conservative 50% power-loss assumption.
- **Scope discipline**: the "Fronteras de generalización" table (Ch.6) is a rare and valuable
  feature — it states explicitly, per major claim, what is supported, what is not, and what
  evidence would be needed to extend it. Very few doctoral theses do this as systematically.
- **Genuine (if partial) external validation**: EXP3 replicates the SHAP > Anchors fidelity
  ordering on two additional datasets (12/12 paired comparisons) and reports, honestly, that
  the SHAP–LIME effect size *attenuates* outside Adult Income rather than claiming full
  replication.

## Findings

### F01 [major] — D1 (Evidence Relevance) / D6 (Methodological Rigor)

- **Location**: `capitulo-5-taxonomia.qmd` (opening paragraphs) vs. `capitulo-4-resultados.qmd`
  (§ Estudio A, § Perfil multidimensional por método).
- **Evidence**: Ch.5: *"un evaluador que conozca solo los rangos de fidelidad (SHAP: 0.810,
  LIME: 0.560, **Anchors: 0.514, DiCE: 0.412**)"* and *"La parsimonia media de DiCE (**0.085**
  características activas) y su fidelidad baja (**0.412**)"*. Ch.4: *"Anchors = 0.389 ±
  0.100, DiCE = 0.170 ± 0.103"*, *"DiCE ocupa el último lugar en fidelidad (**0.172**)"*, and
  *"La parsimonia [de DiCE] es la más baja de todos los métodos (**0.017**)"*; separately,
  Ch.4 attributes 0.085 to Anchors/LIME, not DiCE (*"La parsimonia de Anchors es comparable a
  la de LIME (0.085)"*).
- **Observation**: Chapter 5 restates the benchmark's headline fidelity numbers for Anchors
  and DiCE with values that do not match Chapter 4's own reported means (Anchors 0.514 vs.
  0.386–0.389; DiCE 0.412 vs. 0.170–0.172), and additionally assigns DiCE a parsimony value
  (0.085) that Chapter 4 assigns to Anchors/LIME, while Chapter 4 gives DiCE's actual parsimony
  as 0.017 — a value five times smaller.
- **Reasoning**: This is exactly the failure mode the thesis's own "puerta 7" (claim
  traceability) is designed to prevent: a downstream chapter restating primary results from
  memory rather than from the qualified artifact. It does not undermine the confirmed
  hypotheses (H1–H3 rest on Ch.4/Appendix D's numbers, which are internally consistent and
  match the CSV-traced tables), but it is a factual inconsistency inside a document whose
  central methodological claim is end-to-end numeric traceability — an external examiner
  checking Ch.5 against Ch.4 will find the discrepancy immediately.
- **Suggestion**: Correct Ch.5's illustrative numbers to match Ch.4/Appendix D
  (Anchors fidelity ≈0.386–0.389, DiCE fidelity ≈0.170–0.172, DiCE parsimony ≈0.017), or, if
  Ch.5's figures come from a different aggregation (e.g., a different block subset), state that
  explicitly and cite the source artifact. The qualitative argument in Ch.5 (no method
  dominates on all axes) survives unchanged with the corrected numbers.

### F02 [major] — D4 (Argument Coherence) / D5' (Reporting Honesty)

- **Location**: `capitulo-6-conclusiones.qmd`, §"Líneas de investigación futura" item 4, vs.
  the immediately preceding §"Nota sobre la validación externa parcial: EXP3"
  (`sec-exp3-nota`) in the same chapter.
- **Evidence**: `sec-exp3-nota` states: *"Adicionalmente, se completó una extensión de EXP3
  que incluye LIME en los mismos dos datasets... El resultado más notable concierne a la
  estabilidad: LIME obtiene similitud coseno media de 0.922–0.927 en Breast Cancer y
  0.748–0.854 en German Credit..."* (i.e., LIME + stability cross-dataset work is reported as
  **done**). Item 4 of "Líneas de investigación futura," a few paragraphs later, states:
  *"EXP3 replicó el ordenamiento de fidelidad SHAP-Anchors... pero excluyó a LIME y las
  métricas de estabilidad. La extensión prioritaria es, por tanto, incorporar LIME y la
  métrica de similitud coseno al protocolo cross-dataset..."* (i.e., frames this as **not yet
  done**, top-priority future work).
- **Observation**: The two passages directly contradict each other on whether LIME +
  stability were incorporated into the cross-dataset protocol. It reads as though the "future
  work" section was drafted before the EXP3 extension was completed and not updated
  afterward.
- **Reasoning**: This is a coherence break in the thesis's own closing chapter, and it
  actually *understates* completed work — a more serious error for a thesis defense than an
  overstatement would be, since a committee member who reads `sec-exp3-nota` closely will
  reasonably ask why item 4 doesn't acknowledge it. The residual real gap (per
  `sec-exp3-nota` itself) is narrower than item 4 claims: SHAP's stability was *not*
  instrumented on Breast Cancer/German Credit, so the full paired SHAP–LIME $d_z$ comparison
  is still unverified cross-dataset — but LIME-side stability is already measured.
- **Suggestion**: Rewrite item 4 to reflect the actual remaining gap: *"EXP3 already measured
  LIME fidelity and stability on two additional datasets (§sec-exp3-nota); the residual gap is
  instrumenting SHAP's stability on those same datasets to compute the full paired SHAP–LIME
  effect size outside Adult Income."*

### F03 [minor] — D6 (Methodological Rigor) / D4 (Argument Coherence)

- **Location**: `capitulo-4-resultados.qmd`, § Perfil multidimensional por método → SHAP,
  vs. § Estudio B → Diferencias en métricas de calidad (same chapter).
- **Evidence**: SHAP profile paragraph: *"La parsimonia más alta de todos los métodos (0.234
  frente a 0.085 de LIME) refleja que SHAP puede distribuir importancias entre un mayor número
  de características..."*. Estudio B paragraph, same chapter: *"En parsimonia (ratio activo),
  SHAP es consistentemente más denso que LIME... **por lo que LIME es el método más
  parsimonioso en este benchmark**."*
- **Observation**: The parsimony metric is explicitly defined in Ch.3 as "proportion of active
  features," direction $\downarrow$ ("un valor bajo indica mayor concisión"). A higher value
  (SHAP, 0.234) is therefore *less* parsimonious by the metric's own stated direction, which
  the Estudio B paragraph correctly reflects ("LIME es el método más parsimonioso"). The SHAP
  profile paragraph calls the same 0.234 value "la parsimonia más alta," using "parsimonia" as
  if higher were better — the opposite of the metric's defined direction.
- **Reasoning**: Likely a wording slip ("highest value of the parsimony metric" intended,
  "highest parsimony" written), but it directly contradicts a correct statement six pages
  later in the same chapter, and a reader skimming only the SHAP profile section would come
  away with the metric direction backwards.
- **Suggestion**: Reword to "SHAP exhibits the highest active-feature ratio (0.234 vs. 0.085
  for LIME), i.e., it is the least parsimonious method by this metric — reflecting that it
  distributes importance across more features when the model requires it," removing the
  "mayor/más alta parsimonia" phrasing for the less-parsimonious method.

### F04 [suggestion] — D6 (Methodological Rigor)

- **Location**: `capitulo-3-diseno-experimental.qmd`, § Evaluación cuantitativa del impacto
  estadístico.
- **Evidence**: *"Incluso asumiendo una reducción del poder del 50%... el estadístico de Coste
  sería $\chi^2 \approx 15.2$ ($p \approx 0.0016$)"*.
- **Observation**: The transformation from "50% power reduction" to a specific resulting
  $\chi^2$ value is asserted rather than derived (no formula or reference for how a power-loss
  percentage maps onto a noncentrality/statistic reduction is given).
- **Reasoning**: The surrounding safety-margin argument (290% margin over the critical value)
  is solid and doesn't need this extra sensitivity claim to be convincing; as written, the
  specific number is unfalsifiable by the reader without seeing the underlying calculation.
- **Suggestion**: Either show the transformation (e.g., halving the noncentrality parameter
  and recomputing the tail probability under the noncentral $\chi^2$) or drop the specific
  $\chi^2\approx15.2$ figure and keep the (already sufficient) 290%-margin argument alone.

### F05 [suggestion] — D6 (Methodological Rigor)

- **Location**: `capitulo-3-diseno-experimental.qmd` § Cobertura de artefactos; corroborated by
  `capitulo-4-resultados.qmd` § Anchors profile ("Anchors tiene una cobertura de solo 56
  celdas calificadas... refleja que en los estratos de mayor incertidumbre el algoritmo de
  búsqueda de reglas no converge").
- **Observation** (absence, no quote to cite): Anchors' 24% missingness is explicitly caused
  by non-convergence to a rule meeting the precision threshold — i.e., missingness is
  outcome-dependent (MNAR), concentrated in exactly the instances/blocks where Anchors would
  likely have scored worst had it converged. The thesis's missing-data analysis (Ch.3)
  quantifies the *variance* impact of reduced replicate counts but does not discuss the
  *selection-bias* direction: dropping non-convergent (presumably harder) cases could bias
  Anchors' reported fidelity/stability means upward relative to its true performance across
  all attempted instances.
- **Reasoning**: This doesn't threaten H1/H2 (Anchors already ranks near the bottom even
  under this potential upward bias, and Friedman's rank-based procedure is noted as robust to
  within-block variance inflation), but it is a relevant caveat for the prescriptive
  recommendation "Anchors debe usarse con cautela" (Ch.6) — the caution should arguably be
  stronger, not weaker, once this selection effect is acknowledged.
- **Suggestion**: Add one sentence to the Ch.3 coverage-impact discussion (or Ch.6
  limitations) naming this as a directional caveat: non-convergence exclusion is not
  missing-at-random and likely biases Anchors' reported quality metrics optimistically rather
  than pessimistically.

### F06 [suggestion] — D3 (Scope Calibration)

- **Location**: `capitulo-6-conclusiones.qmd`, § Contribución aplicada: criterios
  prescriptivos de selección de métodos XAI.
- **Evidence**: *"Los resultados del benchmark son suficientemente consistentes para formular
  criterios de selección **prescriptivos** en lugar de simples 'recomendaciones
  contextuales'"*; *"**SHAP debe seleccionarse**..."*; *"**LIME puede seleccionarse**
  exclusivamente cuando..."*.
- **Observation**: Chapter 2 explicitly commits the thesis to conditional language ("FOM-7
  no debe usar la palabra 'mejor' sin calificador... debe hablar de mejor fidelidad local,
  mayor estabilidad bajo una perturbación definida..."). Each Ch.6 recommendation is in fact
  conditioned by context (bullet-listed), but framing them collectively as "prescriptivos"
  and using bare imperative mood ("debe seleccionarse") is a stronger register than the
  epistemic discipline the thesis sets for itself elsewhere, and sits in tension with the
  same chapter's own "Fronteras de generalización" table, which restricts these same claims to
  "Condiciones del benchmark descritas" and explicitly excludes "preferencias de usuarios
  finales" and "dominios regulados."
- **Reasoning**: Not a factual error — every recommendation is scoped by an explicit context
  clause — but the rhetorical framing ("prescriptivos," imperative mood) is more likely to be
  quoted out of context (e.g., "thesis says SHAP must be selected") than the more careful
  language used in Ch.2–Ch.4.
- **Suggestion**: Either keep "prescriptivos" but open the subsection with one sentence
  reiterating that each criterion is conditional on the benchmark's dataset/model scope (cross
  -referencing the Fronteras table), or soften to "orientative" / "empirically grounded"
  criteria rather than "prescriptive."

## Questions for the author

- For F01: can Ch.5's Anchors=0.514/DiCE=0.412 figures be traced to any artifact (e.g., an
  earlier EXP2 run, a different block subset), or are they a transcription slip from a draft
  stage? This determines whether the fix is a one-line correction or requires re-checking
  whether other narrative passages in Ch.5/Ch.6 also carry stale numbers.
- For F02: is the SHAP-stability instrumentation on Breast Cancer/German Credit planned before
  the defense, or is it explicitly deferred? If deferred, item 4's wording should say so
  precisely rather than imply the whole LIME+stability extension is still pending.
- For F05: does the Anchors implementation log *how many* candidate instances were attempted
  before declaring non-convergence per cell? If so, a short appendix note on the
  attempted-vs-converged ratio would let a reader gauge the size of the potential selection
  bias directly rather than relying on the qualitative caveat alone.
