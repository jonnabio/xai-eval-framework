# Paper F — Analysis Plan (version 2)

**Question:** Does the order of four explanation methods, found on one tabular dataset,
hold on other tabular datasets?
**Status:** Version 2, 2026-10-05, written from the author's decisions of that day
(section 12). It replaces version 1 of 2026-10-03, which is in the history of this file.
No dataset has been loaded, no model trained and no explanation computed for Paper F.
**Venue:** Journal of Computer Sciences Institute (`VENUE_JCSI.md`): 8 pages, one
hypothesis, 2 or 3 conclusions.
**Reasons for each choice:** `DESIGN_PROPOSAL.md`.

---

## 1. What the study is

Most comparisons of explanation methods use one dataset, often UCI Adult, and report that
one method is better than another. The paper tests whether such an order is a property of
the methods or of the dataset.

- The **dataset is the unit that is sampled**. The claim concerns datasets, so the number
  of datasets, not the number of instances, decides how strong the claim can be.
- The structural profile of a dataset is **descriptive only**. The study does not say which
  property of a dataset causes a change of order.

## 2. Design

**16 datasets × 4 models × 4 explainers = 256 conditions, 5 seeds, 200 instances.**

### 2.1 Datasets: sixteen, chosen by rule

Inclusion rule:
1. public, usable without registration or a restrictive licence;
2. tabular, binary target, or a binarisation that the source documents;
3. at least 1,000 rows and 5 to 100 raw features;
4. after training (section 2.5): cross-validated AUC between 0.65 and 0.98 for at least
   three of the four models. Only model results are used for this gate.

Strata: feature composition (all numeric; mixed; all or mostly categorical) by size
(under 10,000 rows; 10,000 or more). Adult is fixed in "mixed, large".

Candidate pool, in this order inside each stratum:

| Stratum | Candidates |
|---|---|
| Numeric, small | Phoneme, Spambase, QSAR biodegradation, Ozone level |
| Numeric, large | MAGIC telescope, Electricity, Default of credit card clients |
| Mixed, small | German Credit, Churn, Sick, COMPAS |
| Mixed, large | Adult, Bank Marketing, Nomao |
| Categorical, small | Chess (king-rook vs king-pawn), Mushroom |
| Categorical, large | Amazon employee access |

Procedure:
- Each candidate is checked against rules 1 to 3 from its source record, then against
  rule 4. A candidate that fails is listed with the reason and the value.
- If fewer than sixteen pass, the pool is widened with the binary tasks of the OpenML-CC18
  suite, in the order of their OpenML identifier, taking the stratum with the fewest
  datasets first, until sixteen pass or the suite is exhausted.
- If more than sixteen pass, the last candidates of the fullest strata are dropped.
- The study runs with at least twelve datasets. With fewer, it stops and the author decides.
- The final list, with source identifier, version, rows, features and the profile of
  section 2.2, is committed (`outputs/analysis/paper_f/datasets.csv`) **before any
  explanation is computed**.

Breast Cancer (569 rows) fails rule 3. It is not one of the sixteen.

### 2.2 Dataset profile (descriptive)

Rows; raw features; features after encoding; share of numeric features; median and maximum
number of categories; share of the minority class; share of missing values; mean absolute
pairwise correlation of the numeric features; cross-validated AUC of each model.

### 2.3 Models

Logistic regression (L2), random forest, XGBoost, multilayer perceptron. One configuration
per model for all datasets, written in a configuration file that is committed before
training. Preprocessing is the same for all: standard scaling of numeric features, one-hot
encoding of categorical features, median or mode imputation. Split: 80% training, 20%
test, stratified by class, by seed.

### 2.4 Explainers

LIME, SHAP (TreeSHAP for the two tree models, KernelSHAP for the other two), Anchors and
DiCE. One configuration per explainer for all datasets, taken from the EXP2 configurations
(`configs/experiments/exp2_comparative/`) and committed in the Paper F configuration file
before the run. No setting is tuned per dataset.

### 2.5 Seeds and instances

- Seeds: 42, 123, 456, 789, 101112. A seed fixes the split, the model and the explainer's
  sampling.
- Instances: 200 from the test split per dataset, model and seed, stratified by predicted
  class; all test instances if there are fewer than 200. The four explainers explain the
  same instances.
- An instance for which an explainer returns no explanation, or exceeds the time limit set
  in the configuration file, is kept and counted as a failure.

## 3. Measures

| Measure | Explainers | Role |
|---|---|---|
| Faithfulness gap: change of the predicted probability when the top 20% of the features named by the explanation (at least one) are replaced by their training mean or mode | all four | ranked |
| Stability: mean Jaccard index of the five top features between the explanation of the instance and of 10 perturbed copies; numeric features perturbed by Gaussian noise of 0.05 standard deviations of the feature, categorical features unchanged | all four | ranked |
| Sparsity: share of features not used by the explanation | all four | ranked |
| Cost: wall time per explanation in milliseconds; also as a ratio to the model's prediction time | all four | ranked |
| Failure rate | all four | reported for every cell |
| Faithfulness correlation: Pearson correlation between the size of each attribution and the change of the predicted probability when that one feature is masked. This is the measure that EXP2 and EXP3 call "fidelity" (corrected 2026-10-05, section 12) | all four | reported; not ranked and not in the Holm family |
| Rule precision and coverage | Anchors | reported |
| Validity and proximity of the counterfactual | DiCE | reported |

- For the ranked measures, higher is better for faithfulness gap, stability and sparsity,
  and lower is better for cost.
- A failed instance takes the worst value observed for that measure in its dataset and
  model, so that failures cannot improve a mean. The analysis is repeated on the instances
  where all four explainers succeeded, as a sensitivity check.
- The stability and faithfulness definitions differ from those of EXP2 and EXP3. The
  changes to `src/metrics/` are shared code with tests, merged before the run.

## 4. Analysis

**Level.** One mean per dataset, model, explainer and seed: 1,280 values per measure.
Instances are never treated as independent evidence about datasets.

**Order of the explainers.** For each dataset and measure: the mean of each explainer over
models and seeds, then ranks 1 to 4.

### 4.1 Primary analysis, one per ranked measure

1. **Estimate:** the mean Spearman correlation between the explainer orders of all pairs
   of datasets, (kW − 1)/(k − 1), where W is Kendall's coefficient and k the number of
   datasets.
2. **Interval:** 95%, percentile bootstrap over datasets, 10,000 draws.
3. **Test:** permutation test of "the orders of different datasets are unrelated":
   the ranks are permuted independently inside each dataset, 100,000 permutations,
   one-sided. Holm correction over the four measures, alpha 0.05.
4. **Ceiling:** the same correlation between the orders of the five seeds inside each
   dataset, averaged over datasets. Agreement between datasets is read against it.

### 4.2 Secondary analyses

1. **Adult as reference.** For each of the six pairs of explainers and each measure: the
   share of the other datasets where the pair is in the same order as on Adult, with an
   exact binomial interval.
2. **Largest rank change** of each explainer between any two datasets.
3. **Pairs of datasets** are reported as a matrix of rank correlations, without p-values:
   with four explainers a single pair cannot reach significance.
4. **Variance shares** on the 1,280 values: explainer, dataset, model, explainer × dataset,
   explainer × model, residual.
   - Primary model: linear mixed model with dataset as a random factor (random intercept
     and random explainer effect by dataset, seed nested in dataset and model).
   - Sensitivity: aligned rank transform on the same values.
   - The explainer × dataset term is tested by permutation: explainer labels are permuted
     inside each dataset, model and seed block, 10,000 permutations.
   - If the two models disagree, both are reported and the weaker conclusion is drawn.
5. **Per model:** the primary analysis repeated for each of the four models.
6. **Cost and quality:** for each dataset, which explainers are not dominated on
   faithfulness gap and cost; descriptive.

Only permutation tests are used. Intervals are bootstrap or exact binomial.

## 5. What is not done

- No test of whether datasets differ in level: with this many values it is significant
  for any data.
- No test that treats datasets as fixed and instances as replicates.
- No claim about which dataset property causes a difference.
- No result of Papers A to E is printed. The Adult values of Paper F come from the new run.

## 6. Hypothesis and decision rule

**H:** on each ranked measure, the order of the four explainers agrees across tabular
datasets more than chance.

For each measure, with the Holm-corrected permutation p and the 95% interval of the mean
rank correlation:

| Outcome | Wording in the paper |
|---|---|
| p ≥ 0.05 | no evidence that the order is shared |
| p < 0.05 and the interval lies above 0.5 | the order generalises |
| p < 0.05 and the interval lies below 0.5 | the order is shared only weakly |
| p < 0.05 and the interval contains 0.5 | shared, strength not determined |

The value 0.5 is fixed here. By simulation (`scripts/paper_f_power_simulation.py`), with
sixteen datasets the test detects a true correlation of 0.5 almost always and of 0.2 in
77% of studies, and the estimate of a true 0.5 falls between 0.27 and 0.72.

## 7. Order of work

1. Shared code, on a `pubs/*` branch: a loader for the datasets; the stability and
   faithfulness changes with tests.
2. Lane: configuration file; `scripts/paper_f_*` for the profile, training, the run in
   resumable shards, and the analysis; tests.
3. Dataset profile and model training; the AUC gate; `datasets.csv` committed.
4. **Pilot:** one dataset, four models, four explainers, one seed, 20 instances, to measure
   time and find failures. Its outputs are deleted and are not results.
5. The full run. Estimate: 585 processor hours, about three days on the author's laptop
   with twelve processes (`DESIGN_PROPOSAL.md`, section 6).
6. Analysis scripts are committed before the full run ends and are run once on the
   complete data.
7. Zenodo version, manuscript in the journal template, claim registry.

## 8. Reproducibility

- Every table and figure has a generator in `scripts/paper_f_*` that reads
  `outputs/analysis/paper_f/`.
- A Paper F run is its own cohort; it overwrites nothing of EXP2, EXP3 or EXP4 (RCA-002).
- Package versions and the machine are recorded with the run.

## 9. Open points

1. Where the run is made: the author's laptop is assumed.
2. ~~The time limit per explanation is set after the pilot.~~ Set: 1,200 seconds
   (section 12).
3. Whether the journal wants an anonymous file (`VENUE_JCSI.md`, section 1).

## 10. Deviations

Any departure from this plan is recorded in section 12 with its date and reason before the
manuscript is written, and named in the paper if it touches a reported result.

## 11. Sections of version 1 that no longer apply

Four datasets and three model families; 100 instances per quadrant; fidelity as a measure
for the four explainers; the thresholds 0.50 and 0.80 on W; significance of tau for single
pairs of datasets; the test of the dataset main effect; the three-tier synthesis.

## 12. Amendments and deviation log

| Date | Section | Change | Reason and authority |
|---|---|---|---|
| 2026-10-03 | All | Version 1 created | Initial framework |
| 2026-10-05 | 11.3, 11.4 of version 1 | Generator scripts are named `scripts/paper_f_*`; the deviation log is this section | Lane setup (ADR-0021, amendment of 2026-10-05) |
| 2026-10-05 | 2.1 | Sixteen datasets, chosen by rule; floor of twelve | Author decision. Four datasets cannot support the claim (`DESIGN_PROPOSAL.md`, section 2) |
| 2026-10-05 | 2.3 | Four models: logistic regression, random forest, XGBoost, MLP | Author decision |
| 2026-10-05 | 2.5 | 200 instances by predicted class; no balance by quadrant | Author decision |
| 2026-10-05 | 3 | Four measures rank the four explainers; fidelity for LIME and SHAP only; new stability and faithfulness definitions | Author accepted the advisor's answer that one fidelity measure for the four is not valid. The author did not comment on the two new definitions; they are the advisor's proposal and are open to the author's change until the code is merged |
| 2026-10-05 | 4 | Permutation tests only; pairs of datasets without p-values; mixed model primary, aligned rank transform as sensitivity | Author decision |
| 2026-10-05 | 6 | One hypothesis and a decision rule with the value 0.5 | Advisor's proposal, required by the venue's structure; open to the author's change until the run starts |
| 2026-10-05 | 5, 7 | The Adult baseline is a new run; 16 datasets and 4 models are run | Author decision |
| 2026-10-05 | Venue | Journal of Computer Sciences Institute | Author decision |
| 2026-10-05 | 3, 6 | The two new measure definitions and the decision rule are confirmed | Author decision ("proceed as proposed", "OK") |
| 2026-10-05 | 3 | **Correction of an error of the advisor.** The row "Fidelity: R² of the local linear model" is replaced. The R² class exists in `src/metrics/fidelity.py`, but EXP2 and EXP3 never used it: what they report as fidelity is the faithfulness correlation computed in `src/metrics/faithfulness.py`. That measure is defined for any attribution vector, so the statement of `DESIGN_PROPOSAL.md` (section 4) that the framework's fidelity is not defined for Anchors and DiCE was wrong. The four ranked measures do not change. The faithfulness correlation is reported for the four explainers as a secondary measure, outside the ranking and the Holm family | Found while reading the code, before any Paper F explanation was computed |
| 2026-10-05 | 7 (step 1) | The loader and the measures are in the lane (`scripts/paper_f_lib.py`, tests in `tests/analysis/test_paper_f_*`), not in `src/` | No code of another paper changes; Paper F is self-contained in its archive |
| 2026-10-05 | 2.4 | Anchors is computed with the reference implementation of its authors (package `anchor-exp` 0.0.2.0), not with `alibi` as in EXP2. DiCE is `dice-ml` 0.12. | `alibi` cannot be installed on the Python 3.13 of this machine (it needs NumPy below 2). Threshold 0.95 as planned; one-hot columns are declared categorical, numeric columns are cut at quartiles (the package default) |
| 2026-10-05 | 2.3 | Categories beyond the 20 most frequent of a feature are grouped into one level before one-hot encoding. The positive class is the minority class. A dataset's stratum is computed from the data: numeric if it has no categorical feature, categorical if under 20% of its features are numeric, mixed otherwise | Needed to make the plan executable; fixed in `paper_f_config.toml` before any model was trained |
| 2026-10-05 | 3 | Details fixed in code before the pilot: the faithfulness gap masks at most ⌈0.2·d⌉ of the features an explanation names (d encoded features); the stability copies of an instance are the same for the four explainers; a copy whose explanation fails counts as Jaccard 0; DiCE attributions below 10⁻⁶ are zero | Needed to make the plan executable |
| 2026-10-05 | 2.1 | **Result of the rule.** 12 of the 17 pool candidates pass. Fail: Spambase, Sick, Chess and Mushroom (AUC above 0.98 for two or more models), Nomao (118 features). Widening with OpenML-CC18 in the order of the plan added JM1, PC4, PC3 and KC1; PhishingWebsites (AUC too high) and numerai28.6 (AUC near 0.5) failed. Sixteen datasets: `outputs/analysis/paper_f/datasets.csv`; every candidate and reason: `candidates.csv` | Rule applied as written. **Noted for the paper:** JM1, PC4, PC3 and KC1 are software-defect datasets of one family, so the sixteen are less independent than the count suggests; no categorical-small dataset passed and only one categorical-large |
| 2026-10-05 | 7 (step 4) | **Pilot, after `datasets.csv` was committed (`bd887cd63`).** (a) Adult, four models, four explainers, seed 42, 20 instances: 16 jobs, 320 rows, no failure, longest instance 270 s (Anchors on the random forest). (b) Added to the plan's pilot: two instances of every dataset, model and explainer with seed 42, to find programming and machine errors before a run of several days: 256 jobs, 512 rows. Two instances failed for a reason of the method (DiCE found no counterfactual: Ozone level, XGBoost). Two problems were of the machine: with 14 jobs at once one Anchors call ran out of memory, and one job stayed alive after a crash inside XGBoost. The pilot outputs were deleted | Plan section 7. Part (b) is an addition, made because a failure found only during the full run would cost days |
| 2026-10-05 | 3, 7 | Changes after the pilot, none of them to a measure, a dataset or a setting of a model or explainer: an out-of-memory or operating-system error stops the job, which is run again, and is not recorded as a failure of the method; a job with no progress for the time limit is stopped and run again; the jobs run in a fixed shuffled order with 10 at a time. Time limit for one instance and explainer: 1,200 s (`paper_f_config.toml`) | Machine problems must not be counted as failures of an explanation method |
| 2026-10-05 | 4 | **Disclosure.** To test `paper_f_analyze.py`, it was run once on the 512 pilot rows and its summary table was seen. Those values come from two instances per condition and one seed; they are not results, are not reported, and no setting was changed after seeing them | Honest record of what was seen before the run |
| 2026-10-05 | 2.4 | Noted for the paper: KernelSHAP with its default settings returns at most 10 non-zero attributions, TreeSHAP returns one for every feature. Both are "SHAP with one configuration"; the sparsity and stability of SHAP therefore depend on the model family | Observed in the pilot; a property of the library defaults, left as planned |
| 2026-10-05 | 7 (step 5) | Cost estimate from the pilot: 800 to 1,060 processor hours, about three to four and a half days with 10 jobs at once on the author's laptop (the earlier estimate from EXP2 run times was 585) | Pilot timings on this machine |
| 2026-10-05 | 2.1 | Before `datasets.csv` was committed, the runner was tried on 3 instances of German Credit with two models (8 short jobs) to find programming errors. The outputs were written to a temporary folder outside the repository and are not used | Disclosure; the plan says the list is committed before any explanation is computed |
