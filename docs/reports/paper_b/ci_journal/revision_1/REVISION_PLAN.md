# Paper B, C&I 2067810, Major Revision: remediation plan

**Status:** PROPOSED 2026-11-06. To be approved by the author; no manuscript or experiment work
starts before that. Lane `paper-b`, branch `paper/b-ci-revision-1`.
Inputs: `DECISION_LETTER.md`, `REVIEW_ANALYSIS.md` (item IDs used below).

## 1. Strategy in one paragraph

Four of the gravest items have one root: the paper re-analyses the cohort of the author's
published Paper A [10]. Those items are R2-6 (reuse and self-containment), R1-1 and R2-8
(novelty), R2-1 (mixed-host timing) and ED-1 (Anchors/DiCE only cited). C&I treats reuse of
one's own published work, **even with citation**, as self-plagiarism (X-1), so no amount of
rewording fixes it. The plan therefore runs a **new, self-contained cohort, B2, on one recorded
host**, with four explainers. It uses a corrected and justified LIME reference, instrumented
cost (wall time, CPU time, model calls) and the stability controls the reviewers ask for. Paper
A is cited for the metric definitions only. The new cohort also carries the configuration sweep
(Pareto fronts) and the symmetric cross-dataset extension. The paper keeps its question ("when
does SHAP outperform LIME?"). Anchors and DiCE enter as reference explainers in the main
benchmark.

## 2. Decisions for the author (needed before WP2)

| ID | Decision | Options | Recommendation |
|---|---|---|---|
| D-1 | Cohort | (a) **new single-host cohort B2** (new instance-sampling seeds; the trained models are reused); (b) keep the EXP2 cohort and re-time only | **(a)**. (b) leaves R2-6, R1-1 and X-1 open and cannot add Anchors/DiCE (X-2) |
| D-2 | Explainers added to the main benchmark (ED-1) | Anchors + DiCE; Anchors only | **Both**. Anchors is a local rule explainer, DiCE a counterfactual one; the metrics apply to both through their feature-importance export (as in EXP2). The text states that DiCE's attribution is derived, so its fidelity is not like-for-like |
| D-3 | LIME reference kernel width (R2-3) | library default $0.75\sqrt{M}$ (≈7.6–7.8); keep 3.0 | **Library default as the reference.** 3.0 stays as one point of the sweep, which is where the configuration-dependence finding now lives |
| D-4 | Cross-dataset scope (R1-6, R2-5) | the two EXP3 datasets (Breast Cancer, German Credit) with all five models, four explainers and full endpoints; or add datasets | **Two datasets, made symmetric and complete.** More datasets would overlap Paper F (X-2); the limit is stated, with Paper F's question left to future work, not cited for numbers |
| D-5 | "FLOPs" (R2-1b) | model calls + CPU time + theoretical complexity, FLOPs for logreg/MLP only; or FLOPs for every model | **First option**, with a stated reason: FLOPs are not defined for tree traversal or the RBF-SVM kernel in a comparable way. Model calls are the hardware-agnostic unit for a black-box explainer |
| D-6 | References (R1-9) | apply the author rule (DOI on every entry, ≥80% from 2024 or later); or targeted update only | **Apply the rule.** The suspension of 2026-10-21 was for that edition, and a reviewer graded the literature "Poor". Classics stay where a definition is cited (LIME, SHAP, Wilcoxon, Holm…) |
| D-7 | Compute host | this laptop (AMD Ryzen 5 4600H, 6 cores, 31.4 GB, Windows 11); or one cloud VM of a fixed type | **Laptop**, if the pilot (WP2.1) fits the deadline; otherwise one fixed cloud VM. Either way the spec is recorded and every cell runs there |

## 3. Work packages

### WP0. Setup (no results)

1. Python 3.11 venv from `requirements-frozen.txt` (`.venv` is absent on this machine; only
   Python 3.13 is installed). Record `pip freeze` and the host spec (CPU, cores, RAM, OS, power
   plan) into the cohort manifest.
2. Settle X-4: load `experiments/exp1_adult/models/preprocessor.joblib` and report the number
   of transformed features (103 or 108).
3. Q-1, Q-2 answered by the author.

### WP1. Problem statement and contributions (R1-1, R2-8)

Rewrite the introduction around a practitioner's decision: which explainer, for which model,
under which latency and stability budget. State three contributions that need no reference to
[10]:

1. a self-contained four-explainer benchmark on one host, with hardware-agnostic cost;
2. configuration-aware results (Pareto fronts) instead of one fixed setting;
3. conditional findings that tell a practitioner when SHAP or LIME is preferable.

[10] is cited once, in Methods, for the metric definitions. No "earlier study on this cohort".

### WP2. New main cohort B2 (ED-1, R1-4, R1-5, R2-1, R2-3, R2-6)

- **Design:** 5 models (logreg, rf, xgb, svm, mlp; the existing trained models) × 4 explainers
  (SHAP, LIME, Anchors, DiCE) × 5 **new** seeds × confusion-matrix-stratified instances. The
  instance count per cell is fixed after the pilot (target ≥100 per cell; stability on a fixed
  sub-sample if KernelSHAP-SVM does not fit).
- **Two passes, separated:**
  - *Quality pass:* fidelity, faithfulness gap, stability, sparsity. Host-independent, so it may
    use parallel workers on the host.
  - *Timing pass:* a fixed instance sub-sample per cell; **one process, one thread**
    (`OMP/MKL/OPENBLAS_NUM_THREADS=1`), warm-up excluded, idle machine, mains power, fixed power
    plan, repeated *r* times. Every member of a pair runs on the same host in the same session.
- **Cost instruments:** wall time, process CPU time, **number of black-box model calls**
  (counting wrapper around `predict_proba`) and rows evaluated, per explanation.
- **Configurations, stated and justified:** LIME at the library-default kernel width
  (D-3), `num_samples` 1,000 (5,000 in the sweep), `num_features` = M for the main measurement
  (no ceiling; see WP4). SHAP: TreeExplainer (tree models) and KernelExplainer with an explicit
  `nsamples`; background of 50 rows (varied in WP5). Anchors and DiCE: the EXP2 settings, with
  their run-completeness reported (EXP2 had 57/75 and 68/75; failures are reported, not
  imputed).
- **WP2.1 pilot first** (one seed, 20 instances, every model × explainer). It measures the time
  per explanation on this host and fixes N and the stability sub-sample to fit the deadline.
  The budget table goes into this plan before the full run starts.
- Output: a new directory `experiments/exp_b2_single_host/` (cohort manifest, configs,
  `results.json` per run, host spec). It never overwrites EXP2 (RCA-002 cohort rule applied by
  analogy).

### WP3. Symmetric cross-dataset extension (R1-6, R2-5)

Same protocol as WP2 on Breast Cancer and German Credit: every model, four explainers, **SHAP
stability included**, same host. The two datasets need logreg, SVM and MLP models trained with
the EXP3 split and seeds, alongside the existing RF and XGBoost. Table 4/5 of the current paper
are replaced by one table of all endpoints × explainer × dataset × model, with paired
differences.

### WP4. Validity of the stability and sparsity measurements (R1-3, R2-3, R2-4)

On the B2 cohort (a sub-grid where the cost is high):

1. **Explainer-only variance control:** σ = 0, the same instance explained *T* times. This
   separates LIME's own sampling noise from sensitivity to the input.
2. **On-manifold perturbation:** Gaussian noise on the numeric features only; categorical
   features resampled with a small probability from the training marginals, so one-hot rows
   stay valid. Reported next to the original σ = 0.1 all-features scheme.
3. **Support-robust stability:** cosine on full attribution vectors (no top-10 truncation),
   plus Spearman rank correlation and top-k Jaccard.
4. **Ceiling-free sparsity:** LIME with `num_features = M`, and concentration measures that
   need no ceiling (share of |attribution| in the top-k, normalized entropy). They are computed
   for every explainer. H2 is reported as **descriptive** (see WP6).

### WP5. Configuration sweep and Pareto fronts (R2-2, R1-4, R2-3)

- LIME: `kernel_width` ∈ {0.75, 1.5, 3, 5, default, 10, 15} × `num_samples` ∈ {250, 500, 1000,
  2000, 5000}.
- KernelSHAP: `nsamples` ∈ {100, 250, 500, 1000, auto} × background ∈ {10, 25, 50, 100}.
  TreeSHAP: background ∈ {10, 25, 50, 100} (it is exact, so no sampling budget).
- All five models, one seed, a fixed instance set, on the WP2 host; cost measured as in WP2.
- Output: non-dominated (Pareto) sets over (stability ↑, fidelity ↑, cost ↓) per model, with a
  figure per model. The text reports whether one explainer's front dominates the other's, and
  where the fronts cross. That replaces Table 6 and answers R2-3 on all models, not one.

### WP6. Statistics (R1-2, R1-7, R2-4)

- **Dependence:** report three levels together:
  - the 125-cell (or available) paired Wilcoxon, now labelled descriptive at the cell level;
  - a **linear mixed model** Δ ~ 1 + (1 | model) + (1 | model:seed) for each endpoint;
  - a **cluster bootstrap** over models, with the model-level sign count (5 units: the exact
    two-sided sign test cannot go below p = 0.0625, and the text says so).
- **Effect sizes:** keep $d_z$, explained as within-pair standardisation that grows when
  pairs are similar. Add the Hodges–Lehmann median difference with CI, the matched-pairs
  rank-biserial correlation, and the difference on the metric's own scale with a stated
  practical threshold.
- **Multiplicity:** Holm over the final family: endpoints × explainer contrasts, SHAP vs each
  of LIME, Anchors and DiCE. Four-explainer omnibus: Friedman with model as block and complete
  cases, plus Nemenyi or Holm post-hoc.
- **H2 (sparsity):** removed as a hypothesis test; reported descriptively, with the ceiling-free
  measures of WP4.
- Implemented as a committed analysis script with tests under the lane, writing
  `outputs/analysis/paper_b_rev1/`. That path is shared; it is added to `lanes.toml` for
  `paper-b` through a `pubs/*` commit first, as Paper D/E/F did.

### WP7. Manuscript rewrite (R1-8, R1-10, R2-6, R2-7, R2-8)

Proposed structure:
1. Introduction (WP1)
2. Related work, updated (WP8)
3. Methods: cohort B2, host and instruments, explainers and configurations with
   justification, metrics, validity controls, statistics
4. Results: main four-explainer benchmark; cost (wall, CPU, model calls, complexity table);
   configuration sweep and Pareto fronts; stability validity; cross-dataset
5. Discussion: conditional recommendation (updated tier table), threats to validity in one
   place
6. Conclusions: every sentence traceable to a result table

- **Self-contained:** every table carries the per-method levels it compares; no caption or
  sentence sends the reader to [10] for a number.
- **Blinding scrub:** no author names in the text (current line 184); [10] cited in the third
  person as any other work, and only for definitions; no "released with an earlier study";
  repository paths kept generic until acceptance.
- Masking-scheme probe (current §4.7): re-run on B2 or dropped. It is a reuse of EXP2 artifacts
  otherwise (X-1).
- Title kept; abstract and keywords rewritten in `pub/claims.toml` (RCA-003: doubled
  backslashes) and regenerated with `generate_fragments.py`.

### WP8. Literature (R1-9)

Reference audit (`.ace/skills/reference-audit/SKILL.md`) and enrichment: 2024–2026 empirical
comparisons of SHAP and LIME, explainer benchmarks (e.g., OpenXAI successors, XAI-Bench-type
suites), explainer hyperparameter sensitivity, stability metrics and on-manifold perturbation,
and hardware-aware cost reporting. Each entry has a verified DOI; the 2024+ share follows D-6.
Paper E and F results are not cited for numbers (X-2).

### WP9. Response letter and submission package (ED-2, R2-7)

- `RESPONSE_TO_REVIEWERS.md` → `.docx`, table form: each item ID, the reviewer's text, the
  response, and where the manuscript changed (section and page of the revised file).
- Revised manuscript with changes highlighted (a second copy), since C&I states no format.
- Builder: extend the masking check to self-citation phrasing and Word core properties
  (author, last modified by, company).
- New intihal.net similarity check expected at upload (≤20% overall, ≤3% per source). The new
  text against Paper A is checked first with the local similarity check, if available.
- Record the decision and the dates in `CI_SUBMISSION.md`, `docs/context/ACTIVE_CONTEXT.md`
  (publication table, via a `pubs/*` commit) and the archive.

## 4. Sequence and dependencies

```
WP0 ──> D-1..D-7 approved ──> WP2.1 pilot ──> budget fixed ──┬─> WP2 quality pass ─┐
                                                              ├─> WP2 timing pass ──┤
                                                              ├─> WP3 ─────────────┤
                                                              └─> WP4, WP5 ────────┴─> WP6 ─> WP7 ─> WP9
WP1, WP8 (text) run in parallel with the experiments ────────────────────────────────────┘
```

Compute runs in the background; the text packages proceed meanwhile. The run time is estimated
from the pilot, not now: KernelSHAP on the SVM was the tail of EXP2 (p95 ≈ 67 s per explanation,
and stability multiplies the explanations by 16).

## 5. Verification gates (every WP that prints a number)

1. `verify_claims.py`, `verify_sync.py`, `verify_exp4_reconstruction.py`,
   `scan_shared_literals.py --strict`, `check_equations.py`: pass.
2. Every new value registered; no value from Papers A, D, E, F or the CIFIE chapter in the
   manuscript (exclusivity, X-2).
3. Every figure has a committed generator (RCA-001).
4. B2 artifacts tracked by git and verified from a clean worktree.
5. Response letter: every item ID of `REVIEW_ANALYSIS.md` answered, each answer pointing to a
   real place in the revised file.
6. Builder masking check passes; Word metadata clean.

## 6. Risks

| Risk | Mitigation |
|---|---|
| Compute does not fit the deadline (KernelSHAP-SVM) | Pilot first; timing on a sub-sample; stability sub-sample; explicit `nsamples`; ask the editor for an extension early (the letter invites it) |
| Anchors/DiCE failures leave holes in the paired grid | Report completeness; pairwise-complete tests; a failure is a result, not imputed |
| Results change direction (e.g., LIME stability at the default width) | Report as found; the title is a question and survives either answer |
| Similarity with Paper A > 3% | New text; definitions paraphrased and cited; local check before upload |
| Thesis follow-up chapter prints old Paper B values | Thesis lane updates after acceptance (X-5); recorded in ACTIVE_CONTEXT |
