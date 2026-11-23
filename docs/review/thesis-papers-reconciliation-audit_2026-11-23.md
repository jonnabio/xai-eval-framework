# Thesis reconciliation audit: Papers A–F against the thesis

**Date:** 2026-11-23. **Role:** Scientific Advisor (audit), Scientific Editor (dispositions).
**Session:** `claude-2026-11-23-reconcile` (substrate) and `claude-2026-11-23-thesis` (thesis lane).
**Scope:** Papers A–F against Chapters 1–7, Appendices A–G, `pub/claim_registry.toml` and the
79 claims mirrored by `pub/thesis_followup_claims.toml`. Paper G is outside the thesis (author).
**Fixed by ADR-0023:** no confirmatory statistic of Chapters 3–5 (χ²_F 42.12 and 40.68, Nemenyi
CD 1.211, 75-cell Wilcoxon d_z 4.820 / 3.002, the P1 CVs, the P2 ICCs) and no objective,
hypothesis or proposition (OE1–OE6, H1–H3, P1–P2) is changed by this audit.

## 1. Baseline (on `main`, `f37549772`, before any thesis edit)

| Check | Result |
|---|---|
| `verify_claims.py` | OK: 2,083 claims, 2,500 sites, 66 retired-value guards, 41 files fully registered |
| `verify_sync.py` | OK |
| `verify_exp4_reconstruction.py` | OK: 18 pinned EXP4 sources |
| `register_thesis_followup.py --check` | OK: 79 claims mirrored |
| `check_equations.py` | OK: 19 equations, 29 figures, 45 tables, each numbered and cited |
| `scan_shared_literals.py --strict` | 0 unexplained, 99 known coincidences |

Registry: 308 claims carry a thesis site. Of these, 12 are shared with a Paper A file,
18 with a Paper B file, 58 with the former combined B+C manuscript (`paper_bc`), 17 with a
Paper C file; the 79 of the follow-up block are mirrored from Papers C (6), D (23), E (14)
and F (36).

## 2. Reconciliation matrix

| Paper | Venue and status | Where in the thesis | Registry | Status |
|---|---|---|---|---|
| **A** | RIMI, published (10.69850/rimi.vi3.307) | Ch. 3 (design, FOM-7); Ch. 4 `sec-estudio-a` (Friedman, Nemenyi); Ch. 7; App. A–E | 12 claims shared with the Paper A file; `scan_shared_literals.py --strict` clean | Reconciled for the printed values. EXP2 provenance findings: §3.1 |
| **B** | C&I 2067810, revision 1 submitted 2026-11-12 | Ch. 3; Ch. 4 `sec-estudio-b` (75-cell Wilcoxon, H3); Ch. 7 `sec-limitaciones`, `sec-fronteras`; App. C (LIME sensitivity) | 18 + 58 (`paper_bc`) shared | Reconciled to the submitted original. Revision 1 (cohort B2) held in Paper B: §3.2 |
| **C** | *Tecnología en Marcha*, submitted 2026-10-06 | Ch. 3 `sec-exp4-diseno`; Ch. 5 `sec-exp4-fiabilidad` (both cohorts); Ch. 6 `sec-seg-jueces` (later controls); App. F, G | 17 shared; 6 mirrored | Reconciled |
| **D** | *Tecnología en Marcha*, submitted 2026-10-03 | Ch. 6 `sec-seg-error`; Ch. 7 `sec-concl-seguimiento`; App. G | 23 mirrored | Reconciled. The held-out check (70,788 instances in training) and the external German Credit contrast that does not reproduce the SHAP deficit are both stated |
| **E** | AAIR, submitted 2026-10-22 | Ch. 6 `sec-seg-concordancia`; Ch. 7; App. G | 14 mirrored | Reconciled. The slope-to-contribution conversion before sign agreement (Ch. 6, the paragraph on signs) is consistent with RCA-005 |
| **F** | JCSI 10503, final version submitted 2026-10-25 | Ch. 6 `sec-seg-transferencia`; Ch. 7; App. G | 36 mirrored | Reconciled for values. Reviewer A additions brought in qualitatively: §3.3 |

Mechanical evidence for "reconciled": every mirrored value passes `register_thesis_followup.py
--check` (same resolver and printed literal as the paper claim) and every shared value passes
`verify_claims.py`. Paper revisions after 2026-10-12 were checked by reading each paper's
record (`docs/reports/paper_*/README.md`): only B (revision 1) and F (Reviewer A) changed text
after the follow-up chapter was written.

## 3. Findings after 2026-10-12 and their disposition

### 3.1 EXP2 cohort, WP0 findings F1–F9 (`docs/reports/paper_b/ci_journal/revision_1/WP0_FINDINGS.md`)

These come from Paper B's revision and bear on Paper A, the thesis and Papers D and E, which
share the EXP2 cohort.

| Finding | Fact | Thesis today | Disposition |
|---|---|---|---|
| **F1** | The fitted `ColumnTransformer` outputs **108** columns; the thesis says **103** (seven occurrences on six lines: App. C; Ch. 7 `sec-limitaciones` twice, `sec-fronteras`, `sec-exp3-nota`, `sec-futuro`, `sec-sintesis`) | 103, as a bare integer outside the coverage scan | **Held at 103** (author decision R1, 2026-11-23) so that no text approved by the tutor changes. Recorded here: 108 is the encoded width actually produced by the frozen preprocessor; 103 is the figure carried since the original drafting. No registered value depends on it. To correct before deposit if the author chooses (§4, item 1) |
| F2 | Stability noise is added to every transformed feature, one-hot columns included; LIME draws a new neighbourhood on every call | Ch. 3 defines the metric; the mechanism was not stated | Qualitative sentence added to Ch. 7 `sec-limitaciones` (decision R3, thesis edit E2) |
| F3 | Fidelity uses absolute values; a constant vector scores 0 | Ch. 3 defines the metric | No change |
| F4 | N levels nested; seeds nearly disjoint; SHAP and LIME see identical instances in a cell | Ch. 4 pairs by cell | No change: the thesis's 75-cell analysis is the planned one; the hierarchical reading is Paper B revision 1's |
| **F7a** | The RF model of the January–February SHAP/LIME runs was never committed and cannot be rebuilt (F7e) | Not stated | **Open** (§4, item 2) |
| **F7b** | `ResourceGuard` adds a ~1 s floor to timed explanations after 2026-03-23; 25 of 31 later runs affected (one SHAP/LIME run, `mlp_shap` seed 42, N=200) | Ch. 3 names `ResourceGuard` but not the floor | **Open** (§4, item 2) |
| **F7c** | In 10 of 15 SVM cells SHAP explained a subset of LIME's instances | Stated only for the agreement study (Ch. 6 `sec-seg-concordancia`, Límites) | **Open** for Ch. 4 (§4, item 2) |
| **F8** | Models were trained on the seed-42 split; for seeds ≠ 42 the instances are drawn from a split of which ~80% is training data (60 of 75 cells) | Stated and checked for the misclassification study (Ch. 6 `sec-seg-error`: 70,788 instances in training; the stability deficit holds on the held-out ones). Ch. 3 gives the split with `random_state = s` and does not say the models were fitted once on s = 42 | **Partly addressed.** Open for Ch. 3–4 (§4, item 2) |
| F9 | DiCE ran with `total_CFs = 1`; Anchors `threshold = 0.95` hard-coded | Already disclosed: Ch. 3 (DiCE and Anchors configuration), App. C configuration table. No "five counterfactuals" anywhere in the thesis or `pub/claims.toml` | Closed |

WP0 F7–F8 state that they need an RCA ("RCA-004"). That number was later used for the
Paper G publisher (`docs/rca/RCA-004-paper-g-logs-not-published.md`); **no RCA exists for the
EXP2 provenance incident.** Recorded as open (§4, item 2).

### 3.2 Paper B revision 1 (cohort B2)

Cohort B2's numbers stay in Paper B (`docs/reports/paper_b/ci_journal/revision_1/`) while C&I
reviews it double-blind: RCA-001 invariant 11 (no result re-reported across a published and a
submitted manuscript) and the open prior-publication question (ACTIVE_CONTEXT, item 6). The
thesis receives only the mechanism, without a number (decision R3, thesis edit E2): in Ch. 7
`sec-limitaciones`, *Alcance de la inestabilidad de LIME*, Gaussian noise applied to one-hot
binary columns produces points off the data manifold, and that combines with LIME's own
sampling variance, whose size the self-agreement result of Ch. 6 `sec-seg-concordancia`
shows. No registered value, objective or hypothesis changes.

### 3.3 Paper F, Reviewer A (2026-10-19; final version 2026-10-25)

Reviewer A asked (1) why the top five features define stability and (2) for conclusions by
type of dataset. Paper F answered with a sentence after its stability equation and a post hoc
comparison of nine numeric and six mixed datasets (`docs/reports/paper_f/README.md` §9;
`scripts/paper_f_posthoc_type.py`). Thesis edit E1 (decision R2) brings both into
`sec-seg-transferencia` in words, with no new literal:

- the size five was fixed in the plan as the encoded width of the smallest dataset, so it is
  defined on every dataset, and lies between the few features named by Anchors' rules and
  DiCE's counterfactuals and LIME's feature cap;
- a comparison marked *post hoc*: separating numeric from mixed datasets does not change the
  order of the methods; it moves which pairwise comparisons vary.

The agreement values of that comparison (0.65 to 0.87 in the paper) are not printed; printing
them would require registering them first (`pub/thesis_followup_claims.toml`).

### 3.4 Bibliography (decision P3)

`thesis/references.bib` carried the same INES 2023 paper twice: `abdulkadir2023` (with DOI
10.1109/INES59282.2023.10297629) and `kadir2023` (`@misc`, no DOI), the latter cited once in
Ch. 2. Ch. 7 wrote the author as "Abdulkadir et al." twice. Thesis edit E3: the Ch. 2 citation
points to `abdulkadir2023`, the duplicate entry is deleted, and Ch. 7 reads "Abdul Kadir et
al.".

### 3.5 Other observations

- **Adult's categorical count.** Ch. 3 (Adult description) gives 6 numeric and 8 categorical
  variables, which matches the frozen preprocessor (WP0 F1). Ch. 7 `sec-exp3-nota` says the
  103-dimension space comes from "codificación one-hot de 13 variables categóricas". The two
  disagree; Ch. 3 is right. Not in the approved edits: §4, item 3.
- **Gate 0.3 grep** (`director-predeposit-checklist_2026-08-29.md`): the qualified sentence
  survives at `capitulo-6-conclusiones.qmd:338` (it was line 292 when the gate was written).
  A second hit, line 42 (P1 row of `tbl-hipotesis`: "incoherencia estructural, no ruido del
  protocolo"), describes the source of the CV, not a universal property of LIME; left to the
  author's reading.

## 4. Open with the author

1. **103 vs 108** (F1): keep 103, or correct it in the thesis before deposit (seven
   occurrences, no registered value; the tutor record would note it).
2. **EXP2 provenance** (F7a, F7b, F7c, F8 for Ch. 3–4): whether the thesis discloses them
   as limits of the confirmatory cohort, and an RCA for the incident (none exists; RCA-004
   is the Paper G publisher). This touches text the tutor approved; not done here.
3. **"13 variables categóricas"** in Ch. 7 `sec-exp3-nota`: correct to 8 (Ch. 3).
4. Prior-publication policy of each journal with a paper under review, before deposit
   (unchanged; ACTIVE_CONTEXT item 6).

## 5. Thesis edits made under this audit (lane `thesis`, `thesis/rca-001-phase-2`)

| Id | File | Change | New literal |
|---|---|---|---|
| E1 | `estudios-de-seguimiento.qmd` `sec-seg-transferencia` | Why five features define stability; post hoc numeric vs mixed note | none |
| E2 | `capitulo-6-conclusiones.qmd` `sec-limitaciones` | One-hot perturbation and sampling variance in the scope of LIME's instability; "Abdul Kadir et al." twice | none |
| E3 | `capitulo-2-fundamentos.qmd`, `references.bib` | `kadir2023` → `abdulkadir2023`; duplicate entry removed | none |

Verification after the edits is recorded in the thesis pull request and in
`docs/context/ACTIVE_CONTEXT.md` (handoff of 2026-11-23).
