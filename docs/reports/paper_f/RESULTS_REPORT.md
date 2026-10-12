# Paper F — Results report

**Date:** 2026-10-11. **Role:** Data Scientist. **Plan:** `ANALYSIS_PLAN.md`, version 2.
**Data:** `outputs/analysis/paper_f/raw/` (commit `3d01a842a`): 1,280 jobs, 256,000 rows,
16 datasets × 4 classifiers × 4 methods × 5 seeds, 200 instances each.
**Result files:** `outputs/analysis/paper_f/results/` (commit `b7b8d576b`), written by
`scripts/paper_f_analyze.py`, run once, after the run was complete and checked.

Every number below is read from a result file, named in each section. This report
interprets them; it adds no test. Two descriptive summaries that the plan does not list
are marked "not planned".

**Scope, added 2026-10-12 after three reviews.** The paper is framed as agreement between
rankings under fixed settings and one evaluation protocol based on the features an
explanation names. It does not rank explanation quality. Sections 1 and 3 below were
written on 2026-10-11, before the reviews; read them with sections 9a to 9c.

## 1. Answer to the question

**Question:** does the order of four explanation methods, found on one tabular dataset,
hold on other tabular datasets?

**Answer: largely yes.** On the four ranked measures the order of the methods agrees
between datasets far more than chance. By the decision rule fixed before the run, the
order generalises for stability, sparsity and cost. For the faithfulness gap the order is
shared, but its strength is not determined: the interval reaches just below 0.5.

The agreement is not perfect. On every measure the datasets disagree with each other more
than two repetitions of the same dataset do, so the dataset does move the order; it moves
it in the middle and lower positions more than at the top.

## 2. Primary analysis (`primary.csv`)

Mean rank of each method over the 16 datasets (1 = best), mean rank correlation between
datasets, its 95% bootstrap interval, the Holm-corrected permutation p, and the agreement
between seeds inside a dataset.

| Measure | LIME | SHAP | Anchors | DiCE | Agreement | 95% interval | p (Holm) | Between seeds | Decision |
|---|---|---|---|---|---|---|---|---|---|
| Faithfulness gap | 2.13 | 1.19 | 3.06 | 3.63 | 0.67 | 0.49 to 0.85 | < 0.001 | 0.95 | shared, strength not determined |
| Stability | 2.06 | 1.13 | 2.81 | 4.00 | 0.88 | 0.79 to 0.95 | < 0.001 | 0.97 | the order generalises |
| Sparsity | 2.97 | 3.91 | 1.69 | 1.44 | 0.79 | 0.66 to 0.92 | < 0.001 | 0.995 | the order generalises |
| Cost | 1.06 | 1.94 | 3.50 | 3.50 | 0.87 | 0.82 to 0.91 | < 0.001 | 0.98 | the order generalises |

- The four p-values are the smallest the test can give (no permutation of 100,000
  reached the observed agreement), so the hypothesis of unrelated orders is rejected on
  each measure.
- The faithfulness gap misses "generalises" by a small margin: the lower end of its
  interval is 0.4875 against the fixed value 0.5. The rule was set before the run and is
  applied as written.
- Agreement between datasets (0.67 to 0.88) is below the agreement between seeds (0.95
  to 0.995) on every measure. The seed figure compares single-seed orders, a
  conservative reference (plan section 12, 2026-10-06), so the difference is, if
  anything, understated.

## 3. Which positions hold and which move (`ranks.csv`, `rank_change.csv`)

- **Faithfulness gap.** SHAP is first on 13 of 16 datasets and never below second. LIME
  is first on 2 (Amazon Employee, Bank Marketing) and Anchors on 1 (COMPAS). LIME and
  Anchors each go from rank 1 to rank 4 across datasets, the largest change observed.
  DiCE is third or fourth everywhere.
- **Stability.** SHAP is first on 14 datasets, LIME on 2 (JM1, Phoneme). DiCE is last on
  all 16. LIME and Anchors exchange the second and third places on 3 datasets.
- **Sparsity.** DiCE is first on 11 datasets and Anchors on 5. SHAP is last on 14
  datasets and tied last on one. The order here is nearly the reverse of the order on
  faithfulness and stability.
- **Cost.** LIME is the fastest on 15 datasets and SHAP on 1 (Phoneme); the two are
  always the first two. Anchors and DiCE are always third and fourth, and which of them
  is slower changes from dataset to dataset (8 against 8).

## 4. Adult as the reference (`pairs_vs_adult.csv`)

For each pair of methods and each measure: in how many of the 15 other datasets the pair
is in the same order as on Adult.

| Pair | Faithfulness gap | Stability | Sparsity | Cost |
|---|---|---|---|---|
| LIME–SHAP | 13 | 13 | 13 | 14 |
| LIME–Anchors | 12 | 12 | 15 | 15 |
| LIME–DiCE | 14 | 15 | 13 | 15 |
| SHAP–Anchors | 14 | 15 | 15 | 15 |
| SHAP–DiCE | 15 | 15 | 15 | 15 |
| Anchors–DiCE | 10 | 15 | 10 | 7 |

- Of the 24 comparisons, 12 hold on all 15 other datasets and 21 hold on at least 12.
- The three weak ones are all Anchors against DiCE: 7 of 15 on cost (exact 95% interval
  0.21 to 0.73, no better than a coin), 10 of 15 on the faithfulness gap and on sparsity
  (0.38 to 0.88).
- With 15 datasets, even "15 of 15" has an interval of 0.78 to 1.00.

## 5. By classifier (`per_model.csv`)

The agreement is present for each of the four classifiers taken alone (p at the minimum
of the 20,000 permutations in all 16 cases; these are not Holm-corrected).

| Classifier | Faithfulness gap | Stability | Sparsity | Cost |
|---|---|---|---|---|
| Logistic regression | 0.73 | 0.80 | 0.87 | 0.85 |
| Random forest | 0.71 | 0.80 | 0.71 | 0.79 |
| XGBoost | 0.64 | 0.82 | 0.78 | 0.89 |
| MLP | 0.64 | 0.82 | 0.88 | 0.91 |

Three intervals contain 0.5: the faithfulness gap for XGBoost (0.46 to 0.83) and the MLP
(0.44 to 0.84), and sparsity for the random forest (0.49 to 0.91).

## 6. Variance shares (`variance.csv`)

Balanced decomposition of the sum of squares of the 1,280 run means (a deviation from the
mixed model named in the plan, recorded in plan section 12 on 2026-10-11).

| Measure | Method | Dataset | Method × dataset | Method × dataset as a share of (method + method × dataset) |
|---|---|---|---|---|
| Faithfulness gap | 19% | 40% | 9% | 0.34 |
| Stability | 65% | 14% | 9% | 0.12 |
| Sparsity | 43% | 25% | 10% | 0.19 |
| Cost | 6% | 8% | 17% | 0.74 |

- The method-by-dataset term is significant by permutation on every measure (p = 0.0001,
  the minimum of 10,000 permutations), in both the plain and the aligned-rank analysis.
  The dataset does change how the methods compare; section 2 shows that the change is
  mostly not large enough to reorder them.
- For the faithfulness gap the dataset alone explains more variance (40%) than the
  method (19%): how large a gap is depends first on the dataset.
- **Cost needs care.** In milliseconds, the method explains 6% and the three-way term
  43%, because a few conditions are extremely slow (DiCE on the random forest for Ozone,
  Amazon Employee and QSAR). The order by cost is nevertheless the most regular of the
  four. Variance shares of raw times and agreement of orders answer different questions.
- **The shares of the aligned-rank analysis are not comparable with the plain ones.**
  The alignment removes the other effects by construction, so the method-by-dataset term
  takes 72% to 97% there. Only its p-value should be used; it agrees with the plain
  analysis, so the rule "if the two disagree, the weaker conclusion" does not apply.

## 7. Failures and the sensitivity check (`failures.csv`, `primary_complete_cases.csv`)

- 1,425 of 256,000 rows failed (0.56%): 1,326 DiCE, 99 Anchors, none for LIME or SHAP.
- Three conditions hold 1,279 of them: DiCE on the random forest for Amazon Employee
  (77% of its instances), DiCE on XGBoost for Ozone (41%), DiCE on the random forest for
  QSAR biodegradation (10%).
- A failed instance takes the worst value seen in its dataset and classifier. Repeating
  the primary analysis on the instances that all four methods explained gives the same
  four decisions: faithfulness gap 0.67 (0.48 to 0.85), stability 0.85 (0.75 to 0.94),
  sparsity 0.84 (0.72 to 0.95), cost 0.87 (0.82 to 0.92). The results do not depend on
  how failures are scored.

## 8. Cost against faithfulness (`frontier.csv`)

A method is on the frontier of a dataset if no other method is both at least as
faithful and at least as fast. LIME is on it for 15 datasets, SHAP for 14, Anchors for 1
(COMPAS) and DiCE for none. Median cost of the run means (not planned, descriptive, from
`cells.csv`): LIME 7 ms, SHAP 60 ms, DiCE 1,231 ms, Anchors 1,478 ms.

## 9. Limits of these results

1. **Sixteen datasets, not sixteen independent ones.** JM1, KC1, PC3 and PC4 are
   software-defect datasets of one family. Not planned, descriptive, from
   `dataset_pairs.csv`: on the faithfulness gap the six pairs inside that family agree at
   0.90 on average and the other 114 pairs at 0.66. The family raises the faithfulness
   figure somewhat; the other three measures differ little (0.87 to 0.90 against 0.79 to
   0.88).
2. **Four methods give coarse orders.** A rank correlation between two datasets can only
   take a few values; 7 of the 120 pairs of datasets have zero or negative correlation on
   the faithfulness gap, 2 on sparsity, none on stability or cost.
3. **SHAP is two algorithms.** TreeSHAP gives a weight to every feature, KernelSHAP with
   its defaults at most ten (plan section 12). The sparsity and stability of SHAP depend
   on the classifier family; the last place of SHAP on sparsity is partly this.
4. **The faithfulness gap favours methods that name many features** only up to the cap of
   20% of the features; DiCE and Anchors name about three features on average
   (`secondary.csv`), SHAP about 21 and LIME about 10. A low gap for DiCE and Anchors is
   in part a short explanation, not only a wrong one.
5. **Cost is wall time on one laptop** with eight jobs at once, and fewer at the end of
   seed 42.
6. **The value 0.5 is a convention** fixed in the plan. The faithfulness-gap decision
   turns on 0.4875 against 0.5.
7. **Scope.** Binary tabular tasks, one configuration per method, no tuning per dataset,
   the measures as defined in the plan. No property of a dataset is claimed as a cause.
8. **DiCE failures** are recorded as `UserConfigValidationException`; that this means "no
   counterfactual found" is a reading, not checked in the library code.

## 9a. Check made after the results: the software-defect family counted once

Added 2026-10-12 (posthoc_defect_family.csv; plan section 12; rigor review F07). The
primary analysis repeated on 13 datasets, the twelve others and one of JM1, KC1, PC3 and
PC4, once for each of the four. Not part of the planned analysis.

| Measure | Planned (16 datasets) | Family counted once: range of the four runs | Lowest interval end | Decision |
|---|---|---|---|---|
| Faithfulness gap | 0.67 | 0.64 to 0.67 | 0.42 | unchanged in all four |
| Stability | 0.88 | 0.85 to 0.88 | 0.75 | unchanged in all four |
| Sparsity | 0.79 | 0.76 to 0.77 | 0.61 | unchanged in all four |
| Cost | 0.87 | 0.86 to 0.87 | 0.80 | unchanged in all four |

The family raised the faithfulness and sparsity figures by about 0.03 at most; no
decision of the rule depends on it. Limit 1 of section 9 is answered by this check.

## 9b. Counts made after the results: how the measures behave

Added 2026-10-12 (`posthoc_descriptives.csv`; plan section 12; independent review F01, F02,
F04, F07). Descriptive; no test.

| Method | Features named (mean) | Features the gap masks (mean) | Time-limit failures | Other failures |
|---|---|---|---|---|
| LIME | 9.5 | 6.5 | 0 | 0 |
| SHAP | 21.3 | 8.0 | 0 | 0 |
| Anchors | 3.0 | 2.1 | 99 | 0 |
| DiCE | 3.0 | 2.7 | 114 | 1,212 |

- The encoded datasets have 5 to 180 features.
- With the median of a run in place of its mean, DiCE is faster than Anchors on 14 of the
  16 datasets; with the planned mean, on 8. The planned order of the two turns on a small
  share of very slow DiCE searches.
- What this changes in the reading: on sparsity, stability and cost much of the order
  follows from the output format, the algorithm and the settings (LIME set to 10
  features, kernel SHAP at most 10, tree SHAP every feature; DiCE's random search; the
  price of the two search methods), and the faithfulness gap grows with the number of
  features named. Sections 1 and 3 of this report were written before these counts and
  should be read with them.

## 9c. Counts and audit made after the results: the protocol

Added 2026-10-12 (`posthoc_protocol.csv`, `audit_resume.csv`; plan section 12; Codex
review F07, F08, F10, F11). Descriptive; no test.

- Anchors rules that name more features than the gap masks: 18% of the explained
  instances; more than five: 10%. There the features used are chosen by column index.
- DiCE faster than Anchors, of 16 datasets: 8 with the planned mean (failures take the
  worst value), 9 with the mean of successful instances, 14 with their median.
- Median difference between Anchors and DiCE over the datasets: 0.05 in the faithfulness
  gap and 0.05 in sparsity, against a median range of the four methods of 0.13 and 0.54.
  LIME and Anchors: 0.06 in the gap, 0.14 in stability (range 0.60). LIME and SHAP: 0.02
  in the gap.
- Median cost ratio: 1.9 between Anchors and DiCE, 7.2 between LIME and SHAP, 246 between
  the slowest and the fastest method.
- Restarts: by the file times of the run's working directory, no LIME or SHAP job was
  stopped and started again (the time on disk of each exceeds the time of its rows by
  0.4 s at most); 15 Anchors and 7 DiCE jobs were, which changes nothing for them since
  their draws depend on the seed and the instance only. This audit is a dated record: it
  cannot be repeated from the archive.

## 10. Reported, not ranked (`secondary.csv`)

Means over the 64 dataset-and-classifier cells, successful instances only. Faithfulness
correlation: SHAP 0.70, LIME 0.49, Anchors 0.28, DiCE 0.17, the same order as the
faithfulness gap. DiCE validity: 0.96.

## 11. For the manuscript

Tables 2 and 3 and Figure 1 are generated (`generated/tab_primary.tex`,
`generated/tab_adult.tex`, `figures/fig1.pdf`). The draft builds at 7 pages of 8 with 7
pending marks: the two result sentences of the abstract, the reading of Table 3, the
Discussion, the sources of error, the conclusions, and the Zenodo DOI. These are the
Scientific Editor's; sections 1, 3, 6 and 9 above are the material for them.
