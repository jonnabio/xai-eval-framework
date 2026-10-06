# Paper F — External Validity of XAI Benchmark Conclusions

**Title (chosen by the author, 2026-10-05):** *How Dataset-Dependent Are Tabular Explainability Benchmarks?*  
**Status (2026-10-03):** Analytical framework initiated. Pre-analysis framework and methodological appraisal established prior to dataset commitment or experimental execution. No empirical results have been generated.  
**Status (2026-10-05):** Unchanged. Lane set up in the main folder (section 7). No venue is selected and the datasets B, C and D are not chosen. Section 4 below describes the other papers as of 2026-10-03; since then Paper B+C was split into Paper B (*CLEI Electronic Journal*) and Paper C (*Tecnología en Marcha*). The current status of every paper is in `docs/context/ACTIVE_CONTEXT.md`.  
**Status (2026-10-05, later):** Venue chosen by the author: *Journal of Computer Sciences Institute* (`VENUE_JCSI.md`; 8 pages at most). The author approved the design of `DESIGN_PROPOSAL.md`; `ANALYSIS_PLAN.md` is now version 2: **16 datasets × 4 models × 4 explainers**, 200 instances, 5 seeds, permutation tests. **Sections 2, 3 and 5 below describe version 1 (4 datasets, 48 conditions) and are superseded by the plan.** No dataset has been loaded and no code of the experiment has been run.

---

## 1. Executive Summary & Core Identity

Most XAI benchmarking studies evaluate explainers on a single tabular dataset (most commonly the UCI Adult Census Income benchmark) or report unpooled, ad-hoc evaluations across heterogeneous collections. Consequently, the XAI literature implicitly treats comparative performance—such as *"SHAP dominates in fidelity"* or *"LIME suffers from local instability"*—as general properties of the explanation algorithms rather than as dataset-conditioned phenomena.

**Paper F shifts the paradigm:**
> **The benchmark is the experimental instrument; external generalizability is the object of study.**

The central unit of interest in Paper F is **not** raw explainer performance, but the **transferability of comparative conclusions** across tabular datasets exhibiting distinct structural characteristics.

---

## 2. Research Questions

- **RQ1 (Dataset Main Effect — H1):** Does explanation quality (fidelity, stability, sparsity, faithfulness gap) and computational efficiency systematically differ across tabular datasets when controlling for explainer and model family?
- **RQ2 (Explainer × Dataset Interaction — H2 — Central Anchor):** Does the relative comparative advantage of explainers change depending on dataset structure, or does explainer ranking remain invariant across domains?
- **RQ3 (Ranking Generalizability — H3):** To what degree are intra-dataset explainer orderings ($R_{d,m}$) preserved across domain transitions, both relative to the Adult baseline and across non-baseline dataset pairs?
- **RQ4 (Quality–Cost Trade-Off Stability — H4):** Does the Pareto efficiency frontier relating explanation quality to computational cost remain stable, or do algorithmic trade-offs collapse under specific structural topologies?
- **RQ5 (Synthesis):** Across what tiers of evidence—**Absolute**, **Relative**, or **Ranking**—can XAI benchmark conclusions be legitimately generalized?

---

## 3. Factorial Experimental Architecture (48 Conditions)

The study implements a balanced $4 \times 3 \times 4$ factorial design:

```
4 Datasets × 3 Model Families × 4 Explainers = 48 Primary Conditions
```

- **4 Tabular Datasets:**
  - `Dataset A`: **UCI Adult** (Canonical baseline / reference dataset)
  - `Dataset B`: **Structural Contrast 1** (e.g., Pure continuous, dense correlation manifold)
  - `Dataset C`: **Structural Contrast 2** (e.g., High-cardinality categorical, extreme sparsity)
  - `Dataset D`: **Structural Contrast 3** (e.g., Severe class imbalance, asymmetric decision boundary)
- **3 Model Families:**
  - `Linear`: Logistic Regression / Linear Regularized Models
  - `Tree / Ensemble`: Random Forest / XGBoost / Gradient Boosted Trees
  - `Nonlinear`: Multi-Layer Perceptron (MLP) / RBF Kernel SVM
- **4 Model-Agnostic Explainers:**
  - `LIME`: Local surrogate modeling with perturbation sampling
  - `SHAP`: KernelSHAP / TreeSHAP Shapley value attribution
  - `Anchors`: High-precision IF-THEN perturbation rules
  - `DiCE`: Diverse counterfactual generation via gradient/optimization

---

## 4. Distinctiveness Across the Publication Suite

Paper F occupies a dedicated, unconfounded niche within the overarching research framework:

| Manuscript | Core Focus | Primary Comparison | Dataset Scope | Key Dependent Variable |
|---|---|---|---|---|
| **Paper A / RIMI** | Benchmark architecture prototype | Explainer quality baseline | UCI Adult | Fidelity, Stability, Cost |
| **Paper B+C / IBERAMIA** | Multilevel evaluation framework & taxonomy | Evaluator alignment & validation | Adult (EXP1–4) + EXP3 replication | Metrics + Human/LLM agreement |
| **Paper D / Tec. en Marcha** | Misclassification impact | Correct vs. Incorrect instances | Adult (+ German Credit check) | Quality deficit ($\Delta$ Stability) |
| **Paper E** | Feature attribution consensus | Explainer vs. Explainer (disagreement) | Adult + German Credit + BC | Top-$k$ Jaccard, Rank concordance |
| **Paper F (This Study)** | **External validity & generalizability** | **Comparative conclusions across datasets** | **Adult + 3 Structural Contrasts** | **Rank Concordance, Interaction ($\mathrm{Expl} \times \mathrm{Data}$)** |

---

## 5. End-to-End Analytical Pipeline

```
1. Dataset Structural Characterization (10 standardized dimensions)
                           ↓
2. Baseline Predictive Modeling (12 baselines: 4 datasets × 3 models)
                           ↓
3. 48-Condition XAI Benchmark Execution (Fidelity, Stability, Sparsity, Faithfulness, Cost)
                           ↓
4. Descriptive Metric Profiles & Uncertainty Quantification
                           ↓
5. Within-Dataset Independent Benchmarks (Conclusions A, B, C, D)
                           ↓
6. Cross-Dataset Main Effects Analysis (H1: Y ~ Dataset + Explainer + Model)
                           ↓
7. Explainer × Dataset Interaction Analysis (H2: Explainer × Dataset)
                           ↓
8. Ranking Generalizability Analysis (H3: Kendall's W, Tau, Spearman's Rho across all pairs)
                           ↓
9. Quality–Cost Frontier Stability Analysis (H4: Pareto Dominance Shifts)
                           ↓
10. Three-Tier External Validity Synthesis (Absolute vs. Relative vs. Ranking Generalizability)
```

---

## 6. Directory Map & Associated Artifacts

- [`README.md`](README.md) — This charter document.
- [`ANALYSIS_PLAN.md`](ANALYSIS_PLAN.md) — Pre-analysis protocol locking hypotheses, metric formalizations, statistical procedures, and acceptance criteria.
- [`paper_f_config.toml`](paper_f_config.toml) — Every setting of the experiment: seeds, the inclusion rule, the models, the explainers, the measures, the candidate pool.
- [`paper_f_template.tex`](paper_f_template.tex) — Source of the manuscript. `paper_f.tex` and `generated/` are written from it by [`scripts/build_paper_f.py`](scripts/build_paper_f.py), which also builds `submission/paper_f_{blind,full}.pdf` (local). A result that does not exist yet is a red "[pending]" mark; `--final` refuses to build while one remains.
- [`references.bib`](references.bib) — Entries checked for Papers C, D and E, and two new ones marked for the author's check.
- [`VENUE_JCSI.md`](VENUE_JCSI.md) — The journal's rules, a study of its times from received to published (data and scripts in `venue/`), and how the paper is shaped for it.
- [`DESIGN_PROPOSAL.md`](DESIGN_PROPOSAL.md) — Approved by the author on 2026-10-05 and written into the plan. Scientific Advisor's proposal of 2026-10-05 (number and choice of datasets, metrics, analysis, cost of the run). A proposal: it does not change the plan until the author approves it.
- [`METHODOLOGICAL_ANALYSIS.md`](METHODOLOGICAL_ANALYSIS.md) — Rigorous scientific appraisal of research challenges, algorithmic sensitivities, dataset selection archetypes, and threats to validity.

---

## 6a. Commands (added 2026-10-05)

Run from the repository root with the project environment (`.venv\Scripts\python.exe`).
The environment needs `anchor-exp==0.0.2.0` and `dice-ml==0.12` besides the project's
packages.

| Step | Command | Output |
|---|---|---|
| Datasets and inclusion rule | `python scripts/paper_f_datasets.py` | `outputs/analysis/paper_f/candidates.csv`, `datasets.csv` |
| Pilot | `python scripts/paper_f_run.py launch --pilot` | `outputs/analysis/paper_f/pilot/` (local, not a result) |
| Full run, resumable | `python scripts/paper_f_run.py launch --workers 10` | `outputs/analysis/paper_f/runs/` (local until the run ends) |
| All parts, unattended | Windows task `PaperF-chain-ensure` runs `python scripts/paper_f_chain.py --tick` every 10 minutes | starts the launcher of the first incomplete seed when none is running; log in `runs/_chain.log`; pause with the file `runs/_STOP` |
| Parts done | `python scripts/paper_f_chain.py --status` | conditions done per seed |
| Progress | `python scripts/paper_f_run.py status` | counts of job files, rows and failures |
| Analysis | `python scripts/paper_f_analyze.py` | `outputs/analysis/paper_f/results/` |
| Result tables and figure | `python scripts/paper_f_report.py` | `generated/tab_primary.tex`, `generated/tab_adult.tex`, `figures/fig1.pdf` (after the analysis) |
| Manuscript | `python docs/reports/paper_f/scripts/build_paper_f.py` | `paper_f.tex`, `submission/*.pdf` |
| Tests | `python -m pytest tests/analysis/test_paper_f_lib.py tests/analysis/test_paper_f_analyze.py` | |

The run can be stopped at any time; the same launch command continues it. Downloaded data
are in `data/openml/paper_f/` (git-ignored).

## 7. Lane and Working Rules (added 2026-10-05)

Paper F is lane `paper-f` of `scripts/pubs/lanes.toml` (ADR-0021, amendment of 2026-10-05).

| Item | Value |
|---|---|
| Folder | the main folder, `xai-eval-framework` (there is no `../xai-paper-f`) |
| Branch | `paper/f-external-validity` (any `paper/f-*`) |
| Session start | `python scripts/pubs/check_lane.py claim --owner <session name>`; stop if it fails |
| Session end | `python scripts/pubs/check_lane.py release --owner <same name>` |

**Paths the lane owns** (everything else is shared and reaches `main` in its own commit, by pull request):

| Path | Use |
|---|---|
| `docs/reports/paper_f/**` | plan, manuscript source, figures, result tables, build scripts; `submission/` is git-ignored |
| `outputs/analysis/paper_f/**` | analysis artifacts written by the Paper F scripts |
| `scripts/paper_f_*` | generators and analysis scripts (analysis plan, section 11.3) |
| `tests/analysis/test_paper_f_*` | their tests |
| `docs/planning/paper_f_*` | planning notes |

**Rules that apply before any result exists:**

1. **Plan first.** The datasets B, C and D, and every choice the plan leaves open, are fixed in
   `ANALYSIS_PLAN.md` (section 12, dated) and committed before the code that depends on them runs.
2. **New runs are new cohorts** (RCA-002). Paper F runs write to `outputs/analysis/paper_f/` or
   to their own experiment directory. They never overwrite the stored EXP2, EXP3 or EXP4 results.
3. **No result of another paper is printed.** Paper A is published; Papers B, C, D and E are
   submitted or ready. A number that one of them reports cannot be reported again here
   (RCA-001). The Adult baseline of Paper F is either a new run or a cited result.
4. **Shared code goes through `main`.** A change to `src/**`, to a runner another paper uses
   (for example `scripts/run_exp3_lime.py`) or to `src/data_loading/cross_dataset.py` is a
   shared commit on a `pubs/*` branch, not a lane commit.
5. **Numbers come from files.** When a manuscript exists, its numbers are filled from result
   files by a build script and registered in `pub/claim_registry.toml` (`[coverage]`,
   `[exclusivity]`, a `paper_f` resolver) before submission, as for Papers C, D and E.
6. **Every figure has a committed generator.**
7. **References (author rule, 2026-10-05, essential).** Every reference carries its DOI
   URL. Every reference is verified against the source: the DOI resolves and the authors,
   title, venue, year and pages are those of the record. At least 80% of the references
   date from 2024 or later. `build_paper_f.py --final` must not pass while any of the
   three fails. State on 2026-10-05: the draft cites 22 works, 3 of them from 2024 or
   later, and several entries have no DOI, so the reference list has to be rebuilt.
