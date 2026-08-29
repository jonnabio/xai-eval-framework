# Pre-Deposit Checklist — Thesis Director's Review

**Thesis**: "Marco para la Evaluación Multinivel de la Explicabilidad en IA" (FOM-7)
**Date**: 2026-08-29 | **Reviewer stance**: doctoral director, pre-deposit sign-off
**Frame**: monograph · RD 99/2011 + mención internacional · pre-deposit (editable) · mixed ML/methodology tribunal

This is not a copy-edit pass. It is the set of things I would refuse to sign the
*autorización de depósito* without having checked. Items are ordered by what costs most if
left unresolved, not by chapter order.

Three findings in **Gate 0** were confirmed against the sources while preparing this and are
blocking as written.

---

## Gate 0 — Blocking. Resolve before deposit.

> **Status 2026-08-29**: 0.1 and 0.2 resolved in Ch.1 (see amendment note at the end of this
> section). 0.3 remains open — it is an independent re-verification and cannot be discharged
> by the same agent that made the fixes.

- [x] **0.1 — RESOLVED 2026-08-29 (commit below). P2 is never declared. It appears for the first time alongside its own result.**
  Ch.1 §"Hipótesis o proposiciones de trabajo" declares **H1, H2, H3 and P1 only**. P2
  ("los jueces LLM alcanzan fiabilidad aceptable") is first *stated* in Ch.6
  @tbl-hipotesis — in the same cell that reports it as not confirmed. Ch.3 §sec-exp4-diseno
  forward-references it as "proposición de calibración P2 (Capítulo 6)"; `apendices.qmd:317`
  restates the outcome.
  **Why this is blocking, specifically for this thesis**: the central methodological claim is
  that FOM-7 fixes the inference plan *before* confirmatory execution (Gate 1) and that no
  claim may be made without prior gates satisfied (Gate 7). A proposition that first appears
  in the conclusions, carrying its own verdict, is the exact pattern the thesis argues
  against. A methodologist will ask whether P2 was formulated before or after seeing the ICC
  values, and the document currently cannot answer.
  **Fix**: declare P2 formally in Ch.1 next to P1, with its threshold (ICC ≥ 0.75, @koo2016)
  and its falsification condition, and state its exploratory (non-confirmatory) status there
  rather than only in Ch.3.

- [x] **0.2 — RESOLVED 2026-08-29. Objectives don't reconcile: Ch.1 declares five, Ch.6 closes six.**
  Ch.1 §"Objetivos específicos" lists 1–5. Ch.6 @tbl-objetivos closes **OE1–OE6**, where OE6
  ("Cuantificar fiabilidad de evaluadores semánticos LLM") has no antecedent in Ch.1.
  **Fix**: either add OE6 to Ch.1 (consistent with fixing 0.1, since both concern EXP4) or
  remove it from Ch.6 and fold EXP4 into OE5's taxonomy objective. The first is better —
  EXP4 is real work and deserves an objective.

- [ ] **0.3 — Confirm the extension is fully closed before deposit.**
  The rigor-review remediation (2026-08-28) closed 15 findings, but its first pass at F01
  and F15 missed seven sites, caught only on self-review. Independently re-run:
  ```
  python scripts/pubs/verify_claims.py
  cd thesis && grep -rn "estructural" *.qmd | grep -i "lime\|estabilidad"
  ```
  Expect: verifier green; the only surviving "inestabilidad estructural" at
  `capitulo-6-conclusiones.qmd:292`, where the same sentence qualifies it.

**Amendment note (0.1 / 0.2).** P2 was *not* backdated into the confirmatory set. Ch.1 now
declares it with its true provenance: formulated after the Ch.5 taxonomy identified Gap 3,
outside the plan frozen at Gate 1, exploratory and instrument-calibrating rather than
confirmatory. Presenting it as pre-specified alongside H1–H3 would have manufactured exactly
the appearance of pre-registration that Gate 7 exists to prevent; the amendment says so
explicitly in the text, which converts a structural defect into a demonstration of the
thesis's own discipline. OE6 is added on the same basis. Objective 3's grammar slip
("en el relación") fixed in passing.

---

## A. Doctoral substance — is this a *doctoral* contribution?

The tribunal's first question is not "is this correct?" but "is this a thesis?"

- [ ] **A.1 — Can you state the contribution in two sentences without using "framework"?**
  Rehearse aloud. If the answer leans on FOM-7 being *organised*, that is engineering. The
  doctoral claim must be epistemic: FOM-7 makes a class of unsupportable claim impossible to
  state.
- [ ] **A.2 — Is the taxonomy (Ch.5) defensible as a *third* contribution?**
  Ch.5 honestly self-classifies as "operacionalización doctoral integradora... no una
  taxonomía completamente nueva en sentido fuerte". This honesty is right, and it is also
  the weakest flank. **Anticipate**: "you have a protocol and a benchmark; the taxonomy is a
  literature organisation exercise." The defensible answer is the task-context axis plus the
  admissible-inference-scope column, and that Ch.5's Gaps 1–3 are *generative* — Gap 3
  produced EXP4. Make sure you can trace that line without notes.
- [ ] **A.3 — Does the thesis argue why one dataset is sufficient for a doctorate?**
  The confirmatory core (H1–H3) rests entirely on UCI Adult Income. EXP3 gives partial
  cross-dataset validation for fidelity only, on two datasets, two models, no SVM/MLP,
  without SHAP stability. This is the single largest external-validity exposure.
  **Anticipate**: "your headline effect sizes are one-dataset findings." The answer must be
  the pre-declared scope plus the Fronteras table, not a claim of generality.
- [ ] **A.4 — Is the negative result (P2) framed as a contribution rather than a failure?**
  It should be: it is a falsifiable proposition, tested and rejected, with the ICC(1,1)
  relabelling erring conservative. Ensure Ch.6 presents it that way and that OE6 (per 0.2)
  makes it a planned objective rather than a leftover.
- [ ] **A.5 — Word count against programme norms.** The body is ~35,700 words
  (Ch.2 9,865 · Ch.4 6,078 · Ch.3 5,115 · Ch.6 4,839 · Ch.5 3,680 · appendices 3,021 ·
  Ch.1 2,124). Ch.1 at 2,124 words is thin for a chapter that must carry problem,
  justification, objectives and hypotheses — and it is the chapter Gate 0.1/0.2 requires you
  to extend anyway. Verify the total against your programme's expectations.

## B. Statistical defensibility — for the methodologists

- [ ] **B.1 — Unit of inference.** Confirm you can defend the block $(g,n)$ as the Friedman
  unit and the cell $(g,s,n)$ as the Wilcoxon unit, and explain *why* instance-level would
  be pseudoreplication. Ch.3 states this; be able to argue it.
- [ ] **B.2 — Multiplicity.** Three Holm families, no correction *between* families. Be
  ready to justify why that is not a fishing expedition — the answer is that the families
  answer different questions on different units, and it is stated in @tbl-stat-plan before
  results.
- [ ] **B.3 — Nemenyi's conservatism.** Ch.4 reports SHAP–LIME as *not* separable under
  Nemenyi (1.000 < CD 1.211), then separates them decisively in the paired test
  ($d_z = 4.82$). Rehearse this: it is a legitimate design choice (omnibus then targeted
  paired contrast), but stated carelessly it sounds like shopping for a significant test.
- [ ] **B.4 — MNAR missingness in Anchors.** Now disclosed with direction (optimistic bias)
  and bounded via τ=0.90. Verify the paragraph in Ch.3 survives contact with a statistician:
  18/75 missing, non-random, concentrated in high-uncertainty strata.
- [ ] **B.5 — Effect size interpretation.** $d_z = 4.82$ is extraordinarily large. Be ready
  to explain *why* it is plausible rather than a measurement artifact: paired design, same
  frozen models, same instances, 75/75 directional consistency. A large $d_z$ with no
  exceptions usually means the two methods measure something structurally different — which
  is in fact the thesis's own argument.
- [ ] **B.6 — The masking/OOD confound.** Ch.6 admits it "no puede descartarse" that part of
  the SHAP–LIME fidelity gap reflects differential sensitivity to OOD masking rather than
  attribution quality. This is honest and it is a live attack. Decide now whether you defend
  it as a bounded caveat or pre-empt it in the presentation.
- [ ] **B.7 — P1's two CV figures.** Ch.4 now reports both the RF/$N$=100 subgroup (<3%) and
  the pooled figures (SHAP 11.4%, LIME 12.0%). Confirm you can explain why they differ by
  4× without it sounding like the favourable number was chosen first.

## C. Algorithmic defensibility — for the ML members

- [ ] **C.1 — Is comparing Anchors and DiCE on attribution metrics fair?**
  The thesis says no, repeatedly and correctly (Ch.2's asymmetry matrix, Ch.4's profiles,
  Contexts C/D). **Anticipate the sharper form**: "then why report a single ranking at all?"
  Have the answer ready — the ranking is per-metric and scope-bound, never aggregate.
- [ ] **C.2 — Configuration caveats that a specialist will spot.**
  Appendix C records that Anchors' YAML `threshold` is not consumed at runtime (τ fixed at
  0.95) and DiCE runs with `total_CFs = 1` effective. A specialist may read these as bugs
  that condition the results. Decide whether these are presented as *documented
  implementation constraints* or as defects — currently they read as caveats in a table and
  are not revisited where those methods are ranked.
- [ ] **C.3 — LIME's parsimony is a configuration ceiling** (`num_features = 10`), disclosed
  in Ch.6. Verify it is also flagged wherever parsimony is compared, not only in limitations.
- [ ] **C.4 — TreeSHAP vs KernelSHAP is a confound inside "SHAP".** SHAP is exact on rf/xgb
  and approximate on logreg/svm/mlp. That single label spans two algorithms with different
  cost profiles (21 ms vs 54,231 ms) and different stability (xgb 0.575 vs rf 0.949).
  **Anticipate**: "your SHAP results average two different estimators." Ch.4 discusses it
  per model; make sure the framing is deliberate rather than incidental.
- [ ] **C.5 — Are the four methods still state of the art in 2026?**
  Newest cited work is 2025 (7 entries); nothing from 2026. For a 2026 defense, be ready for
  "why not attention-based or concept-based explainers, or newer counterfactual methods?"
  The scope answer (model-agnostic post-hoc on tabular data) is legitimate — but it should
  be *stated as a scope decision* in Ch.1, not merely implied.

## D. Evidence chain — FOM-7 held to its own standard

The thesis proposes a protocol for claim traceability. The tribunal is entitled to apply it
to the thesis itself.

- [ ] **D.1 — Every number in the document traces to an artifact.** Currently enforced for
  Ch.4 only (`verify_claims.py`, 138 claims / 221 sites). Ch.3, Ch.5, Ch.6 and the appendices
  are not yet swept. Sweeping the one covered file found two defects. **Before deposit**, run
  `--coverage-report` on the remaining files.
- [ ] **D.2 — Gate 7 applied to Gate 7.** Verify @tbl-claim-traceability rows name the
  artifact each number actually comes from. One row was wrong until 2026-08-28 (the P1 row
  cited the EXP1 reproducibility report; the values come from the EXP2 run-level table).
  Re-check the remaining four rows by hand.
- [ ] **D.3 — Reproducibility claim is literally true.** Zenodo `10.5281/zenodo.21538180`,
  commit `553f65d71`. Confirm a clean checkout of that commit reproduces Ch.4's tables via
  `scripts/run_exp2_statistical_analysis.py`. The thesis claims this; someone may try it.
- [ ] **D.4 — Disclosed irreproducibles are complete.** Currently: the Table S5 `num_samples`
  probe (disclosed), the EXP4 raw judge responses (lost), three EXP4 Jinja templates (never
  committed). Confirm nothing else is in this category and that each is disclosed *in the
  thesis*, not only in the RCA documents.
- [ ] **D.5 — EXP4's provenance.** The EXP4 sources were reconstructed from `__pycache__`
  bytecode (RCA-002). Appendix F discloses this. Decide whether the defense should volunteer
  it — I would: it demonstrates the audit discipline the thesis advocates, and it is
  discoverable in the public repository.

## E. Formal compliance — RD 99/2011 + mención internacional

- [ ] **E.1 — Mención internacional, all four conditions.** (i) ≥3 months' stay at a foreign
  institution, documented; (ii) part of the thesis written **and presented** in a non-official
  language — currently only `thesis_abstract_en.qmd` exists in English, which is very likely
  insufficient; (iii) two favourable reports from foreign doctors; (iv) a foreign-institution
  member on the tribunal.
  **Action**: confirm with your programme what "part of the thesis" requires — an abstract
  alone is usually not accepted. Extending Ch.6's synthesis or a full chapter is the common
  remedy, and Paper A/B+C already exist in English as a source.
- [ ] **E.2 — Indicios de calidad.** Paper A carries a JMLR *preprint* header
  ("Submitted 2/2026"); Papers B/C target AIES/FAccT. Confirm what your programme requires
  as quality indicators for a monograph, and whether preprints count. If accepted
  publications are required, this is a timeline item, not a document item.
- [ ] **E.3 — Deposit mechanics.** Anti-plagiarism report; public exhibition period;
  tribunal composition and eligibility; `Plantilla_Tesis_Doctorado.docx` conformity —
  note `render.ps1` warns the Word table of contents must be regenerated manually.
- [ ] **E.4 — Authorship and co-authors.** Paper A lists Herrera-Vasquez and Herrero-Uceda.
  For a monograph reusing that material, confirm no co-author authorisation is needed, or
  obtain it.
- [ ] **E.5 — Data protection / ethics.** UCI Adult contains `race` and `sex` attributes and
  the thesis discusses fairness as a taxonomy axis. Confirm whether your programme requires
  an ethics statement for work on a dataset with protected attributes, even public ones.

## F. Document quality

- [ ] **F.1 — Bibliography hygiene.** `references.bib` has **166 entries; only 68 are cited**
  in the thesis. ~98 orphans will not appear in the rendered output but will be visible to
  anyone opening the source repository the thesis publicly cites. Run the project's
  `reference-audit` skill before deposit.
- [ ] **F.2 — Cross-references.** 70 labels, 0 dangling as of 2026-08-29. Re-verify after any
  Gate 0 edits, and re-render — A13 was a dangling reference found only by rebuilding.
- [ ] **F.3 — Figures.** Seven figures in Ch.4, all Spanish-labelled. Confirm each is
  referenced in text, legible in the DOCX at print size, and that the radar chart
  (@fig-radar-metodos) is not read as an aggregate score — it normalises axes and could be
  misread as exactly the composite index the thesis argues against.
- [ ] **F.4 — Terminological consistency.** Spanish/English mixing is heavy
  ("functionally-grounded", "faithfulness gap", "recourse"). Decide a policy and apply it —
  a tribunal member may object to untranslated anglicisms in a Spanish thesis.
- [ ] **F.5 — Table 3.1 numbering.** Ch.3 references "la Tabla 3.1" in prose while the rest
  of the document uses Quarto cross-references. Make it consistent.

## G. Defense rehearsal — the five hardest questions

Prepare a two-minute answer to each. These are the ones I would ask.

- [ ] **G.1** "Your strongest claim is that LIME is unstable, but your own appendix shows
  stability of 0.664 at `kernel_width=10`, and EXP3 shows 0.75–0.93 on other datasets. What
  exactly is the finding?"
- [ ] **G.2** "You compare four methods, but Anchors produces rules and DiCE produces
  counterfactuals. Isn't the fidelity ranking a category error?"
- [ ] **G.3** "One dataset. Why is that a doctorate rather than a case study?"
- [ ] **G.4** "FOM-7 is seven reasonable steps. Which one is novel, and what published study
  would it have prevented?" — *the hardest question in the set; A.1 is the preparation.*
- [ ] **G.5** "P2 failed. Does that invalidate the taxonomy's Gap 3, or confirm it?"
  (It confirms it — but say so crisply, and make sure Gate 0.1 has made P2 a declared
  proposition so the answer isn't undermined by its own provenance.)

## H. Deposit go/no-go

| Gate | Condition | Status |
|:--|:--|:--|
| Scientific | Gate 0.1–0.3 resolved | ☐ |
| Scientific | D.1 coverage sweep run on all chapters | ☐ |
| Scientific | A.3 external-validity framing rehearsed | ☐ |
| Formal | E.1 mención internacional, all four conditions evidenced | ☐ |
| Formal | E.2 indicios de calidad confirmed with programme | ☐ |
| Formal | E.3 deposit mechanics complete | ☐ |
| Editorial | F.1 bibliography audited | ☐ |
| Editorial | F.2 rebuild clean after final edits | ☐ |
| Defense | G.1–G.5 rehearsed | ☐ |

**My assessment as director**: the scientific core is sound and the evidence discipline is
unusually strong — stronger than most theses I would sign. Gate 0.1 and 0.2 are structural
rather than substantive, but they sit in the argumentative spine of a thesis whose whole
claim is pre-specification, so they must be fixed before deposit rather than explained at
the defense. E.1 is the item most likely to delay you, and it is administrative, not
scientific — start it now.
