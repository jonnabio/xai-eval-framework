# Top-level statement sweep

**Status:** Living checklist. Not a dated report — update it in place.
**Last swept:** 2026-09-02
**Owner role:** Scientific Editor

---

## Why this exists

`scripts/pubs/verify_claims.py` guarantees that a *number* in a manuscript still
matches its artifact. It cannot see a **prose commitment** — an objective, a
hypothesis, a scope qualifier, an abstract sentence — because those carry no
registered value.

Three defects of exactly that shape reached late-stage review, each from the same
cause: a claim was corrected in a chapter body and the top-level framing was never
revisited.

| Found | Defect | Lag |
|---|---|---|
| 2026-09-02 | The Resumen and Abstract asserted LIME instability as `estructuralmente inestables` — the universal framing Ch.6 had explicitly retracted on 2026-08-28 | 5 weeks |
| 2026-09-02 | The objetivo general said `validar`, while Ch.6 concedes *"Ausencia de evaluación human-centered"* | since drafting |
| 2026-08-29 | OE5 promised only an integrative role, leaving OE6 without a legitimate antecedent | since OE6 was formulated |

Two of the three sat in the passages an examiner reads first. The cost of the sweep
is minutes; the cost of missing it is a viva question you cannot answer.

---

## When to run it

Run the whole sweep when **any** of these happens:

- a claim is rescoped, qualified or retracted anywhere in the body
- a value is added to `[[retired]]` in `pub/claim_registry.toml`
- an objective, hypothesis or proposition is added, dropped or reworded
- a rigor review closes a finding that changed what the thesis asserts
- before deposit

For a single localised edit, sweep only the rows whose **Invalidated by** column
names the section you touched.

---

## The map

Each row: a statement that is read as a promise, and the sections whose correction
would falsify it.

| # | Statement | Lives in | Invalidated by a change in |
|---|---|---|---|
| 1 | **Objetivo general** | `capitulo-1` §Objetivo general | Ch.6 `sec-contribuciones`, `sec-limitaciones`, the validity ladder |
| 2 | **OE1** — FOM-7 protocol | `capitulo-1` §Objetivos específicos | Ch.3 §Protocolo FOM-7; Ch.6 contribución metodológica |
| 3 | **OE2** — omnibus multimétrico | ” | Ch.4 Friedman/Nemenyi results |
| 4 | **OE3** — paired LIME–SHAP | ” | Ch.4 Wilcoxon paired analysis |
| 5 | **OE4** — reproducibility profile | ” | Ch.4 CV/dispersion; Ch.6 P1 row |
| 6 | **OE5** — taxonomy + construct gaps | ” | Ch.5 `sec-taxonomia-*`, `sec-taxonomia-brechas` |
| 7 | **OE6** — inter-judge reliability | ” | Ch.3 `sec-exp4-diseno`; Ch.5 `sec-exp4-fiabilidad` |
| 8 | **H1, H2** — global differences | `capitulo-1` §Hipótesis | Ch.4 Friedman |
| 9 | **H3** — quality–cost SHAP vs LIME | ” | Ch.4 Wilcoxon paired |
| 10 | **P1** — protocol reproducibility | ” | Ch.4 CV; Ch.6 P1 row |
| 11 | **P2** — semantic-judge reliability | ” | Ch.5 `sec-exp4-fiabilidad` |
| 12 | **Resumen** | `pub/claims.toml` → `pub/fragments/thesis_resumen_es.qmd` | **any** of the above |
| 13 | **Abstract** | `pub/claims.toml` → `pub/fragments/thesis_abstract_en.qmd` | **any** of the above; must mirror row 12 |
| 14 | **`tbl-estudios`** — study nomenclature | `capitulo-1` | ADR-0012; any new or renamed study |

Rows 12 and 13 are the highest-risk: they restate every other row, are read first,
and are the furthest from the evidence.

---

## Checks that can be run

These catch the mechanical half. The judgement half is reading rows 1–14 against
the sections named beside them.

```bash
# Retired wording must not reappear anywhere, abstracts included
python scripts/pubs/verify_claims.py

# ES/EN abstracts must stay wired to the fragments
python scripts/pubs/verify_sync.py

# Abstracts must not drift from the SSOT: regenerate and expect no diff
python scripts/pubs/generate_fragments.py && git diff --exit-code pub/fragments/

# Scope words worth eyeballing after any rescoping
grep -rn "estructural\|universal\|siempre\|garantiza\|valida" thesis/*.qmd pub/claims.toml
```

**A number in an abstract must be registered first.** Reaching for an unregistered
figure turns a prose edit into a resolver-writing exercise. As of 2026-09-02 the
Resumen and Abstract cite only registered values (`d_z` 4.82 / 3.00, 15 blocks,
ICC(1,1) 0.321–0.601), each listed as a site on its claim.

---

## Sweep log

| Date | Trigger | Rows checked | Outcome |
|---|---|---|---|
| 2026-09-02 | Rigor review of the Resumen, then of the objetivo general | 1–14 | Rows 12/13 rewritten (4 major + 3 minor findings); row 1 revised for scope, coverage and an undefined term. Rows 2–11, 14 consistent. |
