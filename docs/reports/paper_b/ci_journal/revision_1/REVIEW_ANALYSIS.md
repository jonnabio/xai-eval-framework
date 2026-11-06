# Paper B, C&I 2067810, Major Revision of 2026-11-06: analysis of every request

Source: `DECISION_LETTER.md` (verbatim). Manuscript under revision:
`../paper_b_ci.tex` (line numbers below refer to it at commit `38dd05b19`).
Plan that remediates each item: `REVISION_PLAN.md`.

Each concern is split into atomic, checkable items. Columns:

- **Verdict**: *Valid* (the reviewer is right and the paper must change), *Partly* (right in
  substance, but the manuscript already states part of it and the fix is mainly to make that
  carry weight), or *Disputed* (answered with evidence, not by changing the work).
- **Kind**: T = text only; A = re-analysis of existing artifacts; X = new experiment;
  P = editorial/process.
- **Plan**: the work package in `REVISION_PLAN.md` that closes the item.

## 1. Editor (Prof. Dr. Mehmet Tekerek)

| ID | Request | Verdict | Kind | Evidence in the repository | Plan |
|---|---|---|---|---|---|
| ED-1 | The **main benchmark** must include at least one state-of-the-art explainer (e.g., Anchors or DiCE), or justify why not | Valid | X | Anchors and DiCE were run on the same 75 Adult cells (`experiments/exp2_scaled/results/*_anchors`, `*_dice`; 57/75 and 68/75 artifact-qualified) and scored on the same five metrics. The manuscript only *cites* their omnibus result (lines 352-369) and uses Anchors in the cross-dataset table. Using those runs directly would restate the results of Paper A (C&I policy, X-1) and overlaps Paper D (X-2), so they enter through the new cohort | WP2, WP3 |
| ED-2 | Point-by-point response letter | — | P | — | WP9 |
| ED-3 | Revision deadline: "contact the editorial office before the deadline" | — | P | **30 November 2026** (author, from DergiPark) | Q-1 |

## 2. Reviewer 1

The form text refers to "the major and minor comments", but the report pasted has only the
summary and the general comment. **A separate file of detailed comments probably exists on
DergiPark** (Q-2). The items below come from the general comment and the ratings.

| ID | Request | Verdict | Kind | Assessment | Plan |
|---|---|---|---|---|---|
| R1-1 | Establish the **novelty** relative to previously published work ("Contribution: Fair") | Valid | T+X | The introduction (lines 75-86) frames the paper as *completing* the 45-cell test of [10]. That presents it as an increment on the author's own study. Same root as R2-6 | WP1, WP2, WP7 |
| R1-2 | Account for **statistical dependence among configurations** | Valid | A | The 75 cells are 5 models × 5 seeds × 3 N. Cells of a model share one trained model, and the N levels may reuse instances. The Wilcoxon test treats the 75 as independent pairs, so the p-values (2.6e-13) are too small and $d_z$ is inflated. The effective number of independent units is nearer 5 (models) or 25 (model × seed) | WP6 |
| R1-3 | Strengthen the **validity of the perturbation-based stability** evaluation | Valid | X+A | Three confounds found in the code (`src/metrics/stability.py`, `src/xai/lime_tabular.py`): (a) Gaussian noise is added to every transformed feature, one-hot columns included (off-manifold; the paper says so at lines 628-635 but does not test it); (b) the LIME explainer is seeded once, so each of the 15 calls draws a new neighbourhood, mixing explainer sampling noise with input sensitivity; (c) cosine over top-10 vectors is near zero when the top-10 *support* changes, whatever the weights | WP4 |
| R1-4 | **Fairness of the explainer configurations** | Valid | X | LIME had a 10-feature ceiling, 1,000 samples and kernel width 3.0 (below the library default $0.75\sqrt{M}\approx 7.6$). SHAP had a 50-row background and the KernelSHAP default budget. The two budgets are not matched or justified | WP2, WP5 |
| R1-5 | **Reliability of computational cost** measurements | Valid | X | Same as R2-1 | WP2 |
| R1-6 | **Generalizability of the cross-dataset findings** | Valid | X | Two datasets, two models, three seeds, and SHAP stability not measured (R2-5). Adding datasets would overlap Paper F (16 datasets, X-2) | WP3 |
| R1-7 | Strengthen the **statistical analysis and interpretation of effect sizes** | Valid | A | $d_z$ of 3.00 to 4.82 come from small within-pair variance over dependent cells; the text reads them as "very large" without a practical scale. No Hodges-Lehmann estimate, no rank-biserial, no hierarchical model, and no correction across the extended family once Anchors and DiCE enter | WP6 |
| R1-8 | Organization ("Poor") | Valid | T | Results mix new evidence with context taken from [10] (lines 352-369); the cross-dataset and probe sections read as appendices; limitations are scattered | WP7 |
| R1-9 | Literature ("Poor") | Valid | T | 38 references, **7 from 2024 or later** (`CI_SUBMISSION.md` §4.2). No recent empirical SHAP-vs-LIME or explainer-benchmark studies. The author rule (80% from 2024 or later, verified DOIs) was suspended for this edition on 2026-10-21 | WP8, D-6 |
| R1-10 | Conclusions must be fully supported by the evidence | Valid | T | Follows from R1-2, R1-3, R2-3 and R2-4: the stability and sparsity conclusions rest on the confounded measurements | WP7 |
| R1-11 | "Major and minor comments": the detailed list | — | P | Received 2026-11-06: `REVIEWER1_DETAILED_REPORT.md`; analysed in section 2b | §2b |

## 2b. Reviewer 1, detailed report (R1-M*n* major, R1-m*n* minor)

The detailed report refines R1-1 to R1-10. Where an item maps to one already analysed, the
earlier ID is given and only what is new is stated.

### Major comments

| ID | Request (short) | Maps to | Verdict | Kind | What is new / assessment | Plan |
|---|---|---|---|---|---|---|
| R1-M1 | Novelty against the published 45-cell comparison | R1-1, R2-6 | Valid | T(+X) | The reviewer names the 45 → 75 framing explicitly. Under D-1 (re-time only) the Adult quality numbers stay those of Paper A's cohort, so the novelty has to come from the new evidence: hierarchical inference, configuration sweep, stability controls, single-host cost with model calls, four explainers, new datasets | WP1, WP7 |
| R1-M2 | Independence of the 75 cells: shared data, models, seeds, N | R1-2 | Valid | A | Lists the four sources. Model and seed are crossed; N levels may share instances (to verify, R1-m5) | WP6 |
| R1-M3 | Robustness of significance and CIs under a hierarchical analysis | R1-2 | Valid | A | Asks for the analysis itself, not only a caveat | WP6 |
| R1-M4 | Fairness: the LIME feature budget and the different SHAP implementations (Tree vs Kernel) | R1-4, R2-4 | Valid | X+A | New: the **Tree/Kernel split** as a confound of fidelity and cost. Answer with KernelSHAP also on the tree models (a sub-grid), so implementation and model family separate | WP5 |
| R1-M5 | Sensitivity of the differences to LIME and SHAP hyperparameters | R2-2 | Valid | X | Same need as the Pareto sweep; the reviewer asks whether the *sign* of each difference survives across configurations | WP5 |
| R1-M6 | Perturbations that respect categorical constraints and dependence | R1-3 | Valid | X | As WP4.2; adds "feature dependencies": noise drawn from a conditional or a nearest-neighbour scheme, not only marginal resampling | WP4 |
| R1-M7 | LIME's low stability vs the perturbation protocol and kernel width, studied systematically | R1-3, R2-3 | Valid | X | Factorial: kernel width × perturbation scheme × σ (including σ = 0) | WP4, WP5 |
| R1-M8 | Validate latency on standardised hardware and software, with **repeated timing** | R2-1a | Valid | X | Adds repetitions explicitly (already in WP2: *r* repeats) | WP2 |
| R1-M9 | **XGBoost vs random-forest runtime reversal**: controlled experiments to tell architecture from implementation or hardware | — (new) | Valid | X | New item. Candidate mechanism: TreeExplainer cost grows with the number of leaves and depth (unpruned RF trees are far larger than depth-6 XGBoost trees), and XGBoost may take a native code path. Controlled run: RF and XGBoost at matched `n_estimators` and `max_depth` grids, cost against total leaves, both on the single host; record the SHAP code path | WP2b |
| R1-M10 | SHAP stability on the extra datasets, or restrict the claims | R2-5 | Valid | X | As WP3 | WP3 |
| R1-M11 | Kernel-width study across seeds and model families | R2-2, R2-3 | Valid | X | As WP5 (all models; the sweep needs ≥3 seeds, not 1) | WP5 |
| R1-M12 | Different numbers of valid explanations across kernel widths; use a **common set of valid instances** | — (new) | Valid | A | New: Table 6 compares 96/100 with 100/100 instances. Every sweep result is reported on the intersection of valid instances, and the share of degenerate explanations is reported as an outcome of its own | WP5 |
| R1-M13 | Masking sensitivity on more model families | — (new) | Valid | A/X | The probe used 5 RF runs. Extend to all five models. Under D-1, from stored explanations of EXP2 (re-analysis, cheap), but those are Paper A's cohort (risk X-1); or from the new LIME runs and the timing runs (preferred where available) | WP4b |
| R1-M14 | Effect sizes: computation, distributions of paired differences, robustness to dependence | R1-7 | Valid | A | Adds: plot the distribution of paired differences per endpoint and model; give $d_z$ at the model level too | WP6 |
| R1-M15 | Recommendations broader than the evidence | R1-10 | Valid | T | Restrict each recommendation to the models, datasets, configurations and host tested | WP7 |

### Minor comments

| ID | Request (short) | Verdict | Kind | Assessment | Plan |
|---|---|---|---|---|---|
| R1-m1 | Abstract: separate the primary Adult findings from the supplementary ones | Valid | T | Abstract in `pub/claims.toml` (RCA-003) | WP7 |
| R1-m2 | Explicit, consistent notation for RQ1–RQ4 | Valid | T | H2 changes to descriptive (WP6); notation for paired Δ, cell, run | WP7 |
| R1-m3 | **Design table**: models, seeds, N, number of matched cells | Valid | T | New table, also covering the sweep, the controls and the datasets | WP7 |
| R1-m4 | Model hyperparameters, preprocessing, train/test split, instance selection | Valid | T | From `experiments/exp1_adult/models/metadata.json` and the configs; a table in an appendix | WP7 |
| R1-m5 | Sampling from TP/TN/FP/FN; **overlap of instances across configurations** | Valid | A+T | To verify in code (`src/experiment/runner.py`, sampling by `samples_per_class` and `sampling.random_seed`): whether N=50 is a subset of N=100/200, and whether seeds share instances. The answer feeds WP6 | WP0, WP6 |
| R1-m6 | How **zero attribution vectors and undefined cosines** are handled in stability | Valid | A+T | **Finding:** `src/metrics/stability.py` uses scikit-learn's `cosine_similarity`, which returns **0 for an all-zero vector**. A degenerate (all-zero) LIME explanation therefore counts as "dissimilar" and lowers stability, instead of being excluded or flagged. To confirm that the runner uses this class with the paper's settings ($T$=15, σ=0.1; the class defaults are 10 and 0.01), and to count how many zero vectors occur. Could be part of LIME's near-zero stability | WP0, WP4 |
| R1-m7 | Fidelity: signs, removal effects, undefined correlations | Valid | A+T | Eq. (3) uses absolute values; behaviour when the attribution or the drop vector is constant (Pearson undefined) to be read from the code and stated | WP0, WP7 |
| R1-m8 | Table 1: consistent notation and column headings | Valid | T | | WP7 |
| R1-m9 | Table 2: the "Reproducible? Yes" labels need predefined criteria | Valid | T | Replace with numbers and a stated threshold, or drop the column | WP7 |
| R1-m10 | Figures 1 and 2: axes, notation, scales, readability | Valid | T | Regenerate with `scripts/generate_paper_b_figures.py` (RCA-001: committed generator) | WP7 |
| R1-m11 | Tables 4/5: variability alongside three-seed means | Valid | A | SD or CI over seeds in the new cross-dataset table | WP3 |
| R1-m12 | Why Anchors in the cross-dataset study | Valid | T | Answered by ED-1/D-2: Anchors and DiCE are now in the main benchmark as reference explainers | WP7 |
| R1-m13 | Grouped masking: how related features were identified and treated | Valid | T | Describe the grouping rule and list the groups; from `outputs/analysis/exp6_masking_sensitivity/` and its script | WP4b, WP7 |
| R1-m14 | Reproducibility: parallelism, execution settings, analysis scripts | Valid | T | Host spec, threads, workers, scripts; availability withheld for masking but described | WP7 |
| R1-m15 | Separate confirmatory (complete paired benchmark) from exploratory findings | Valid | T | Label every result "confirmatory" or "exploratory" in Results, the discussion and the abstract | WP7 |

## 3. Reviewer 2

| ID | Request | Verdict | Kind | Assessment | Plan |
|---|---|---|---|---|---|
| R2-1a | Runtime is invalid: mixed hosts and OSes, no hardware record, pairs not on one host. **Re-run timing on a single, isolated hardware environment** | Valid | X | The manuscript admits it (lines 334-339, 780-788). Host data survive for only a few runs (`experiments/exp2_scaled/worker_manifests/`: JON_ASUS, JONAASUSROG), so the existing timings cannot be repaired | WP2 |
| R2-1b | Report **hardware-agnostic complexity**: theoretical time complexity, **black-box model calls**, **FLOPs** | Valid (FLOPs: Partly) | X+T | Model-call counts can be instrumented exactly (LIME: `num_samples` per explanation; KernelSHAP: nsamples × background rows; TreeSHAP: none, it traverses the trees). FLOPs are only defined analytically for logreg and the MLP. For trees and the RBF-SVM the honest hardware-agnostic unit is model calls plus CPU time (D-5) | WP2 |
| R2-2 | Single static configuration: give **multi-objective Pareto frontiers** (stability, fidelity, cost) **across sampling budgets and kernel widths** | Valid | X | Only a 4-point kernel-width probe exists, on one model and one seed (Table 6, lines 594-636) | WP5 |
| R2-3 | LIME's near-zero stability is **confounded by kernel width 3.0**, too narrow for 103 one-hot dimensions | Valid | X | Supported by our own probe: width 10 gives stability 0.664 (Table 6). Width 3.0 is below the library default (7.6). The paper already calls the result configuration-dependent, but it still reports 3.0 as the reference and builds RQ1 on it | WP2 (reference width), WP4, WP5 |
| R2-4 | The **sparsity test is tautological**: LIME is capped at 10 features | Valid | A+X | The manuscript concedes it (lines 307-312) yet keeps H2 as a hypothesis test with Holm-adjusted p and $d_z$ (Table 1). It has to go as an inferential claim. **Side finding:** LIME's maximum active ratio in the artifacts is 0.0926 = 10/108, not 10/103 (X-4) | WP6 (drop H2 test), WP4 (ceiling-free sparsity) |
| R2-5 | Cross-dataset: **SHAP stability omitted**; validation incomplete and asymmetric | Valid | X | Lines 587-589 admit it. EXP3 models exist (`experiments/exp3_cross_dataset/models/`). Paper F's SHAP stability on those datasets cannot be used (X-2) | WP3 |
| R2-6 | **Reuse of cohorts and findings from [10]**; summary statistics redirected to [10]. The paper must be **self-contained and independently verifiable** | Valid | X+T | Lines 75-86, 183-194, 352-369, the Table 1 and 5 captions and line 467 all send the reader to [10]. C&I policy: "Reusing the author's own previously published work, **with or without citation**, is considered self-plagiarism." Restating [10]'s levels is not allowed. The only clean fix is a **new cohort** whose levels the paper reports itself | WP2, WP3, WP7 |
| R2-7 | **Blinding**: indirect disclosure of identity through self-referencing | Valid | T | Line 184 names the authors of [10] ("Herrera-Vásquez and Herrero-Uceda~[10]"), and the whole framing says "an earlier study … released with" this cohort, which identifies the author. Word file metadata to check too | WP7 (scrub), WP9 (metadata) |
| R2-8 | Problem statement "Poor"; relevance "Marginal"; contribution "Poor" | Valid | T | The introduction opens on method popularity, not on a practitioner's decision problem, and the contributions are stated relative to [10] | WP1, WP7 |

## 4. Cross-cutting constraints found during the analysis

| ID | Constraint | Consequence |
|---|---|---|
| X-1 | **C&I self-plagiarism policy** (Ethical Principles page, read 2026-11-06): reuse of the author's published work "with or without citation" is self-plagiarism; manuscripts with significant similarity are rejected; at most 3% similarity to one source | Paper A's (RIMI) values cannot be restated. The present design, built on Paper A's cohort, is the core weakness. Supports D-1 |
| X-2 | **Registry exclusivity** (`pub/claim_registry.toml`, `[exclusivity]`): results in Papers D, E, F and the CIFIE chapter are forbidden in `docs/reports/paper_b/` unless also in Paper A. Paper D carries 74 Anchors/DiCE claims on the same EXP2 cohort; Paper F carries cross-dataset SHAP/LIME/Anchors/DiCE results | The EXP2 Anchors/DiCE runs and Paper F's numbers cannot be used. A new cohort produces new values; `verify_claims.py` will enforce the boundary |
| X-3 | RCA-001: every printed number is registered; figures need committed generators | Every new value is registered through a `pubs/*` commit (shared path), never typed |
| X-4 | **Sparsity denominator**: artifacts give a LIME maximum active ratio of 10/108; the text says 103 transformed features (lines 233, 620) | Establish the true dimension from `experiments/exp1_adult/models/preprocessor.joblib` before rewriting. If 108 is right, it is a correction to state in the response letter |
| X-5 | ADR-0023: the thesis follow-up chapter prints Paper B values; if they change, `register_thesis_followup.py --check` fails | Thesis lane follow-up after acceptance, not during the revision (lanes never merge into each other) |
| X-6 | Reference rule (`.aceconfig`: DOI URL on every entry; 80% from 2024 or later) | D-6 |
| X-7 | Masked review: author data must stay on the title page only; the C&I builder already fails if they reach the manuscript | Extend the builder's check to self-citation phrasing and Word metadata (WP9) |

## 5. Questions for the author

- **Q-1.** Revision deadline: **answered 2026-11-06: 30 November 2026** (24 days).
- **Q-2.** Reviewer 1's detailed file: **answered 2026-11-06**, saved as
  `REVIEWER1_DETAILED_REPORT.md`, analysed in §2b (30 items).
- **Q-3.** Cloud provider: the author answered "OpenRouter" (2026-11-06). **Open:** OpenRouter
  is a routing service for LLM APIs; it rents no virtual machines, so it cannot host the runs.
  Re-asked; **answered 2026-11-06: this laptop** is the single recorded host (D-7).

## 6. Item count

Editor 3; Reviewer 1 general 11 + detailed 30 (15 major, 15 minor); Reviewer 2 9 (R2-1a and R2-1b
are separate). **53 items** (corrected 2026-11-06 from 52),
answered one by one in the response letter (WP9). Every detailed item maps to a work package;
three are new beyond the first analysis: R1-M9 (runtime reversal), R1-M12 (common valid
instances), R1-M13 (masking across models).
