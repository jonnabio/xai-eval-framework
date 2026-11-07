# Change ledger: Paper B, revision 1 (C&I 2067810)

Every change to the revised manuscript (`manuscript/paper_b_ci_rev1.tex`), to its abstract or
keywords, its figures, tables or data is recorded here **in the same commit that makes it**.
`scripts/check_revision.py` reads this table:

- every change names the reviewer items it answers (IDs of `REVIEW_ANALYSIS.md`), or `none`
  for a change no reviewer asked for (a correction found by the author, such as F1);
- every REMEDIATED item of `RESPONSE_TO_REVIEWERS.md` points to at least one change here.

The marked-up comparison with the submitted text, every insertion and deletion, is rebuilt
with each build: `build/paper_b_ci_rev1_changes_marked.pdf` (latexdiff against the frozen
`../paper_b_ci.tex`, whose hash is in `SUBMITTED_SNAPSHOT.sha256`).

Columns: **ID** (C-###, never reused) · **Date** · **Items** · **Where** (section, table,
figure, file) · **Change** (what and why, one sentence) · **Commit** (filled after the commit).

| ID | Date | Items | Where | Change | Commit |
|---|---|---|---|---|---|
| C-000 | 2026-11-06 | none | `manuscript/paper_b_ci_rev1.tex` | Working copy created from the submitted source (body byte-identical; provenance header added). The submitted files are frozen | — |
| C-001 | 2026-11-06 | R1-1, R1-M1, R2-8, R1-8 | §1 | P-01: New introduction around a practitioner's decision (which explainer, for which model, under which budget). drafted (D-D) | — |
| C-002 | 2026-11-06 | R1-9 | §2 | P-02: Condense the LIME/SHAP background. background condensed (D-D); the paragraph on recent comparisons is marked [REF] until the reference audit (WP8) supplies verified sources | — |
| C-003 | 2026-11-06 | R2-6, R1-M1, R2-7 | old §4.1 | P-03: Delete "Context: Earlier Results on This Cohort" and every pointer that sends the reader to [10] for a number (Tables 1 and 5 captions, runtime text). drafted (D-D) | — |
| C-004 | 2026-11-06 | R2-7 | §3, everywhere | P-04: Masking: remove the author names at old line 184 ("Herrera-Vásquez and Herrero-Uceda [10]") and the framing "the execution cohort released with an earlier study". drafted (D-D) | — |
| C-005 | 2026-11-06 | R1-m2, R2-4 | §3.1 | P-05: Research questions with one notation: paired difference Δ = SHAP − X for X ∈ {LIME, Anchors, DiCE}. drafted (D-D) | — |
| C-006 | 2026-11-06 | R1-m3, R1-M2 | §3.1, Table 1 | P-06: New design table: datasets, models, explainers and variants, seeds, instances per stratum, stability subset, number of paired cells, timing subset. drafted (D-D) | — |
| C-007 | 2026-11-06 | R1-m4, R1-m5, R1-M2 | §3.2 | P-07: Data and models: one fixed split per dataset (seed 42), shared by preprocessing, training and every seed. drafted (D-D) | — |
| C-008 | 2026-11-06 | ED-1, R1-4, R1-M4, R2-3, R1-m12 | §3.3 | P-08: Explainers: SHAP (TreeExplainer for tree models, KernelExplainer otherwise), LIME at the library default kernel width 0.75√M (≈ 7.79 on Adult), with and without the 10-feature budget. drafted (D-D) | — |
| C-009 | 2026-11-06 | R1-m6, R1-m7, R1-3 | §3.4 | P-09: Metric conventions stated: all-zero attribution vectors (counted and reported. drafted (D-D) | — |
| C-010 | 2026-11-06 | R2-1a, R1-5, R1-M8, R1-m14 | §3.6 | P-10: Cost measurement: one recorded host (CPU, RAM, OS, software versions). drafted (D-D) | — |
| C-011 | 2026-11-06 | R1-2, R1-M2, R1-M3, R1-7, R1-M14 | §3.5 | P-11: Statistical analysis that accounts for the hierarchy: a linear mixed model with random intercepts for model and model×seed. drafted (D-D) | — |
| C-012 | 2026-11-06 | ED-1, R1-7, R1-M14, R2-6, R1-m8 | §4.1, Table 2 | P-12: Main results for the four explainers: per-method levels and paired differences with CI, p_Holm, d_z, HL and r_rb, in one table with defined columns. structure drafted (D-D); values and result sentences marked [R], filled from cohort B2 | — |
| C-013 | 2026-11-06 | R1-m9 | old §4.3 | P-13: Delete the CV table and its "Reproducible? Yes" labels. drafted (D-D) | — |
| C-014 | 2026-11-06 | R2-1a, R2-1b, R1-5, R1-M8 | §4.2, Table 3 | P-14: Cost: median wall time and CPU time per explanation on one host, and the number of model calls and rows evaluated. structure drafted (D-D); values and result sentences marked [R], filled from cohort B2 | — |
| C-015 | 2026-11-06 | R1-M9 | §4.2 | P-15: RF vs XGBoost reversal: the controlled run (matched number of trees and depth, cost against total leaves, one host). structure drafted (D-D); values and result sentences marked [R], filled from cohort B2 | — |
| C-016 | 2026-11-06 | R2-2, R1-M5, R1-M11, R1-M12, R2-3, R1-M4 | §4.3, Fig. 1 | P-16: Configuration sensitivity: LIME kernel width × samples, KernelSHAP samples × background, KernelSHAP also on the tree models. structure drafted (D-D); values and result sentences marked [R], filled from cohort B2 | — |
| C-017 | 2026-11-06 | R1-6, R1-M10, R2-5, R1-m11, R1-m12 | §4.5, Table 4 | P-17: Cross-dataset: 7 datasets (Adult and 6 others in a 2×2 of dimension × encoding), all models, four explainers, SHAP stability included, mean ± SD over seeds. structure drafted (D-D); values and result sentences marked [R], filled from cohort B2 | — |
| C-018 | 2026-11-06 | R1-3, R1-M6, R1-M7, R1-M13, R1-m13 | §4.4 | P-18: Validity of the measurements: (a) no-noise control (explainer's own variance). structure drafted (D-D); values and result sentences marked [R], filled from cohort B2 | — |
| C-019 | 2026-11-06 | R1-M15, R1-10, R1-m15 | §5, Table 5 | P-19: One table "what holds, where, under which configuration", with each claim labelled confirmatory (main paired benchmark) or exploratory (sweep, controls, cross-dataset). structure drafted (D-D); values and result sentences marked [R], filled from cohort B2 | — |
| C-020 | 2026-11-06 | R1-1, R1-M1, R2-6 | §5 | P-20: One paragraph on the relation to earlier work, in the third person: what was known, what this study adds. structure drafted (D-D); values and result sentences marked [R], filled from cohort B2 | — |
| C-021 | 2026-11-06 | R1-10, R1-m15 | §6 | P-21: Conclusions that restate only results of Table 2 and Table 5, each traceable. structure drafted (D-D); values and result sentences marked [R], filled from cohort B2 | — |
| C-022 | 2026-11-06 | R1-m1, R1-m15 | Abstract | P-22: Rewrite: primary benchmark first, then supplementary results, each labelled. structure drafted (D-D); values and result sentences marked [R], filled from cohort B2 | — |
| C-023 | 2026-11-06 | R1-m10 | Figures | P-23: Regenerate every figure from committed scripts: labelled axes, units, scales stated, 95% CI defined in the caption, readable at print size. old figures removed (D-D); the new Figure 1 is generated from committed scripts when the results exist [R] | — |
| C-024 | 2026-11-06 | R2-7 | Build | P-24: The masking check also covers the comparison file and the Word metadata (done in the build). drafted (D-D) | — |
| C-025 | 2026-11-06 | R2-6, R1-M1 | §3.1 | D-A: one sentence discloses that an earlier analysis was replaced and why (training overlap, unrecoverable model, mixed hosts); no earlier number is used | — |
| C-026 | 2026-11-06 | none | Keywords | Keywords revised for the four-explainer scope (journal: 3 to 5) | — |
| C-027 | 2026-11-06 | R1-9 | §2, §3.2, References | WP8 (part): related-work paragraph on recent SHAP/LIME comparisons, benchmarks, Shapley estimation, LIME sampling and limits of attribution; 15 recent references and 4 dataset sources added, each verified against Crossref/DataCite/PMC (REFERENCE_AUDIT.md). The 80% rule awaits the author's choice (options A-C) | — |
