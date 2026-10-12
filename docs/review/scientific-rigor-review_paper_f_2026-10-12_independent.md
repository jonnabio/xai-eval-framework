# Scientific Rigor Review: Paper F (independent)

**Date**: 2026-10-12 | **Reviewer role**: Scientific Advisor | **Grade**: Major revision (text and descriptive additions only; no rerun and no change to a primary number)
**Mean score**: 3.6 | **Dimensions**: D1=3 D2=3.5 D3=3.5 D4=4.5 D5'=3.5 D6=3.5

**Independence**: written by a reviewer with no part in writing the manuscript, the plan,
the code or the earlier review. The findings and scores below were fixed before the
earlier review (`scientific-rigor-review_paper_f_2026-10-12.md`) was opened; it is
compared at the end. `RESULTS_REPORT.md` and `ACTIVE_CONTEXT.md` were not opened.

**Scope reviewed** (read whole): `docs/reports/paper_f/paper_f.tex`;
`generated/tab_datasets.tex`, `tab_primary.tex`, `tab_adult.tex`; `figures/fig1.png`;
`ANALYSIS_PLAN.md` (version 2, section 12); `paper_f_config.toml`;
`scripts/paper_f_analyze.py`, `paper_f_lib.py`, `paper_f_run.py`,
`paper_f_posthoc_family.py`; `docs/reports/paper_f/scripts/build_paper_f.py`; every file
of `outputs/analysis/paper_f/results/` including `instances.csv.gz`; `datasets.csv`,
`candidates.csv`, `power_simulation.csv`; `references.bib` (fields only).
**Prior review**: one, of the same date, by the session that wrote the text. See
"Comparison with the earlier review".
**Regression guards**: `docs/rca/regression-guards.yaml` was not read (out of the brief).
`verify_claims.py`: "OK: 1295 claims re-derived from artifacts, 1634 manuscript sites
checked, 60 retired-value guards clear, 13 cited artifacts present, 33 file(s) fully
registered, 25 file(s) clear of unpublished results".

**What was re-derived** (own script, from `instances.csv.gz` upward, not using
`paper_f_analyze.py`): failure counts and their split; the imputation and the 1,280 run
means (equal to `cells.csv` to 1e-10); the rankings (equal to `ranks.csv`); the mean
Spearman correlations by `scipy.stats.spearmanr` over the 120 pairs (0.6683, 0.8783,
0.7894, 0.8683); a bootstrap with another generator (gap 0.485 to 0.841, stability 0.792
to 0.950, sparsity 0.662 to 0.918, cost 0.818 to 0.912; the paper's limits differ by
Monte Carlo error only and no verdict changes); a permutation test (p = 1e-5 on each
measure; the largest of 100,000 permuted values was 0.35 to 0.48); agreement between
seeds (0.9475, 0.9731, 0.9950, 0.9750); the 24 Adult counts and their exact intervals;
first-place and last-place counts; rank ranges; per-classifier values; complete-case
values (0.6683, 0.8483, 0.8422, 0.8700); the post hoc values for the four kept datasets;
the variance shares.

**What could not be verified**:
- The literature. No reference was checked online; only that the 33 cited entries each
  have a DOI and a `checked` field and that 27 of 33 (82%) are from 2024 or later. Whether
  each cited paper says what the text attributes to it is unchecked.
- Anything requiring the experiment: the raw `.jsonl` rows to `instances.csv.gz` step,
  the behaviour of the launcher, the pilot, and the claim that no result was seen before
  the analysis was run. The git history is consistent with the stated order (plan
  `ea41c8a16` 17:05, pipeline `bd887cd63` 18:43 on 2026-10-05; analysis script last
  changed `e819e29b1` before the result files `b7b8d576b`).
- The power simulation (its CSV was read, not rerun), the page count and the Word file.

## One-line summary

Every number in the paper re-derives and the statistics are implemented as described,
but three of the four "generalises" verdicts rest on measures whose order is fixed in
large part by the output format and the settings of the methods, and the paper says so
only partly; the faithfulness gap, the one measure nearest to quality, is confounded with
the number of features an explanation names.

## Strengths

- No wrong number was found. Abstract, text, tables and figure agree with each other and
  with the result files.
- The permutation test, the Holm correction, the bootstrap, the decision rule, the
  ranking direction of all four measures (cost included), tie handling and the failure
  imputation do what the Methods say. The rule is applied where it gives the weaker
  outcome.
- The post hoc check is labelled as such, was logged before it was run, and reports all
  four runs.
- The statement that agreement between datasets is below agreement between seeds survives
  a like-for-like check made here: with one seed at a time, agreement between datasets is
  0.62 to 0.71 (gap), 0.83 to 0.90 (stability), 0.73 to 0.79 (sparsity) and 0.87 to 0.90
  (cost), each below the between-seeds value.
- Dropping all four software-defect datasets (12 left) gives 0.64, 0.88, 0.75 and 0.86
  with lower limits 0.41, 0.78, 0.58 and 0.79 (2,000 resamples): the same four verdicts.

## Findings

### F01 [major] — D1 (Evidence relevance) / D3 (Scope calibration)

**Where**: `paper_f.tex` 346-351 ("the order of the methods generalises", three times);
410-412; Conclusion 1 (467-470): "is largely a property of the methods as configured
here: it agrees across 16 datasets on stability, sparsity and cost".
**Evidence**: on these three measures much of the order is set by the output format and
the fixed settings, before any data are seen.
- Sparsity. LIME is run with `num_features = 10`, so it uses min(10, d) features: this
  holds in 98.0% of its successful instances, and its sparsity is 1 - 10/d. KernelSHAP
  returns exactly 10.0 features in every logistic-regression and MLP cell with d > 10;
  TreeSHAP returns nearly all d (for example 72.0 and 70.0 of 72 on ozone-level-8hr). So
  "SHAP uses more features than LIME" is true by configuration whenever d > 10. The only
  two datasets where it fails are those with d <= 10: phoneme (d = 5, exact tie, both 0)
  and MagicTelescope (d = 10: 0.000 against 0.012). Anchors and DiCE name 1 to 10
  features by nature. The only pair on sparsity that the data decide is Anchors against
  DiCE, and it is the one that moves (10 of 15). Without DiCE, the agreement of the other
  three on sparsity is 0.93.
- Stability. DiCE is last on 16 of 16; see F03 for why this is close to a construction.
- Cost. LIME, SHAP and the two search methods differ by one to two orders of magnitude
  (medians 0.01 s, 0.06 s, 0.91 s and 0.42 s); the order of the first two places is the
  algorithm's price, and the remaining pair is the one that moves.
The paper discloses the KernelSHAP limit of 10 (line 451) but not that LIME's sparsity is
a constant of its setting, and nowhere says that the high agreement on these measures is
expected for that reason. A reader takes "generalises" as an empirical regularity across
datasets.
**Fix**: say in the Results or the Discussion which pairwise orders are fixed by the
format or the settings (LIME against SHAP on sparsity; the place of DiCE on stability;
LIME and SHAP against the search methods on cost) and that the data-dependent part of
each measure is the remaining pairs. Print the mean number of features used per method
(from `secondary.csv`). Reword Conclusion 1 so that it does not present a consequence of
`num_features = 10` as a finding about datasets.

### F02 [major] — D1 / D6 (Methodological rigor)

**Where**: Measures (eq. 1, lines 248-253); line 438-440: "The order on sparsity is close
to the reverse of the order on faithfulness and stability ... so a choice between the
methods remains a choice between properties, whatever the dataset"; Conclusion 3.
**Evidence**: the gap masks min(|U|, m) features, m = ceil(0.2 d), and a method that names
fewer features has fewer masked. Counted from `instances.csv.gz`: the mean number of
features masked is 8.0 for SHAP, 6.5 for LIME, 2.6 for DiCE and 2.1 for Anchors; fewer
than m are masked in 16%, 31%, 86% and 77% of their instances. Across the four methods
the order of the mean gap equals the order of the mean number of masked features
(Spearman 1.0) on 9 of the 15 datasets where it is defined and is at least 0.8 on 14
(compas 0.32). On phoneme, where every method has exactly one feature masked, LIME is
last (0.112, against 0.194, 0.150 and 0.118). The reversal between sparsity and the gap
is therefore built into the gap, and the stability measure (top five of the features
named) has a similar dependence. The paper's caveat (line 446-449, "part of their low gap
may reflect a short explanation") is in the right direction and too weak for a conclusion
that rests on it.
**Fix**: print the mean number of masked features per method beside the gap. Reword
Conclusion 3 and line 438-440: the opposition of sparsity and the gap is in part a
property of the two definitions. A gap at an equal number of masked features for the
four methods cannot be computed from the stored rows (it needs the classifiers), so it is
further work, not a quick check.

### F03 [minor] — D6 / D5' (Reporting honesty)

**Where**: eq. 2 and line 257-258 ("a copy of x whose numeric features receive Gaussian
noise"); line 449-450 ("DiCE uses random search, which may account for part of its low
stability").
**Evidence**: `paper_f_lib.py` 388-393 explains each copy with a different random seed
(`seed + c + 1`). The measure therefore sums the effect of the input noise and of the
method's own sampling, and a deterministic explainer is favoured. Amazon_employee_access
has no numeric feature, so its ten copies are identical to x: there TreeSHAP scores 1.000
on both tree models, DiCE 0.05 to 0.32, Anchors 0.31 to 0.98 and LIME 0.78 to 0.90. On
that dataset the whole of DiCE's low stability is reseeding. Separately, on phoneme
(d = 5) the top five features are all the features, so LIME scores 1.000000 and SHAP
0.999980 by construction; this is one of the two datasets counted against "SHAP has ...
the highest stability on 14".
**Fix**: state in the Methods that each copy is explained with fresh random draws, that
categorical-only data receive no noise, and that with d <= 5 the measure is at its
maximum for a method that names every feature.

### F04 [minor] — D6 / D4 (Argument coherence)

**Where**: Abstract ("that of Anchors and DiCE on cost holds on 7"); line 386-388;
line 432-433; Conclusion 2 ("above all that of Anchors and DiCE").
**Evidence**: the planned statistic is the arithmetic mean of a wall time with a heavy
tail: the slowest 1% of DiCE's instances carry a median of 39% (up to 62%) of its total
time in a dataset. Anchors is cheaper than DiCE on 8 of 16 datasets with the planned
mean, on 7 with the mean of successes only, on 2 with the mean of the run medians and on
1 with the mean log time. With run medians the agreement on cost is 0.93. The headline
exception of the paper is thus a statement about the tail of DiCE's time, not about its
typical cost. The count of 7 itself is correct.
**Fix**: keep the planned result and add one sentence: the typical explanation of DiCE is
faster than that of Anchors on nearly every dataset, and the order of the means turns on
a small share of very slow DiCE searches. Label the median figures as not planned.

### F05 [minor] — D6

**Where**: line 396-403: "the method accounts for ... 6% (... cost), the dataset for ...
8%, and the interaction ... 17%".
**Evidence**: the decomposition is on raw milliseconds. For cost the largest term is the
three-way interaction (43%, `variance.csv`), which the sentence leaves out, so the three
printed shares sum to 31% with no word on the rest. On the log scale the method accounts
for 75%, the dataset for 3% and the interaction for 3% (computed here). "Method 6%" beside
an agreement of 0.87 reads as a contradiction and is an effect of the scale.
**Fix**: say that the cost shares are on the raw scale and are dominated by a few slow
conditions, or drop cost from this sentence.

### F06 [minor] — D5'

**Where**: line 459-462: "Two analyses depart from the plan, as its log records".
**Evidence**: the plan (4.2) also promises the aligned-rank analysis as a sensitivity
check ("If the two models disagree, both are reported"), the matrix of dataset pairs, the
cost and quality frontier, the secondary measures and the failure rate of every cell.
All are computed and none is reported or named as left out. The aligned-rank shares of
the interaction are 72% to 97% (`variance.csv`) against 9% to 17%: as implemented, the
alignment removes the other effects, so these are not comparable shares and the check
supports only the p value. The paper is silent on it.
**Fix**: one sentence listing the planned analyses that are in the archive and not in the
paper, and saying what the aligned-rank check does and does not confirm.

### F07 [minor] — D5'

**Where**: line 219-221: "The draws for an instance are derived from the seed and the
position of the instance, so they do not depend on the order in which the computations
run"; line 225-227: "needs more than 1,200 s".
**Evidence**: (a) true for KernelSHAP, Anchors and DiCE, false for LIME:
`LimeTabularExplainer` is built once with `random_state=seed` and keeps its own generator
(`lime_tabular.py` line 187, 511), which advances with every call; `np.random.seed` in
`evaluate` does not reach it. LIME's draws depend on the instances explained before, and
on whether the job was resumed. (b) The limit is applied by the launcher to one instance
with its ten stability copies (eleven explanations), under eight parallel jobs. All 99
failures of Anchors and 114 of the 1,326 of DiCE are time-limit failures, so they depend
on the machine and its load.
**Fix**: correct the sentence for LIME; say that the limit covers the explanation and its
ten copies and how many failures are of each kind.

### F08 [minor] — D2 (Falsifiability)

**Where**: hypothesis (line 168-169) and its null (line 277-281).
**Evidence**: the null makes the 24 orders equally likely in every dataset. Given F01,
no reader would have expected it to hold, and the largest of 100,000 permuted values
(0.35 to 0.48) is far below every observed one. The test adds little; what can fail is
the pre-registered comparison of the interval with 0.5, and that is where the one
informative outcome (the gap) arises. The hypothesis is falsifiable in form and weak in
content.
**Fix**: none to the analysis. In the Discussion, say that rejection of the null was
expected and that the evidence of the study is the size of the agreement and the
identity of the pairs that move.

### F09 [minor] — D4 / D3

**Where**: Conclusion 2: "The order of LIME and Anchors, and above all that of Anchors and
DiCE, changes between datasets".
**Evidence**: LIME against Anchors holds on 12 of 15 on two measures; LIME against SHAP
holds on 13 of 15 on three measures and LIME against DiCE on 13 on sparsity
(`pairs_vs_adult.csv`). The line between "changes" (12) and unnamed (13) is thin, and
part of the LIME against SHAP exceptions are the degenerate small-d cases of F01 and F03.
**Fix**: name the pairs by their counts, or give the threshold used.

### F10 [minor] — D3

**Where**: Possible sources of error (445-462).
**Evidence**: the plan's log (2026-10-05, "Noted for the paper") records that no
categorical-small dataset passed and only one categorical-large; 9 of the 16 are fully
numeric (Table 1). The paper names the software-defect family and not this. Also
undisclosed: DiCE treats every encoded column, one-hot columns included, as continuous
(`paper_f_lib.py` 285), so its counterfactuals can hold values no category has; and the
measures depend on the encoded d (5 to 180), while Table 1 gives raw features (5 to 72).
**Fix**: one sentence on the composition of the sixteen; one on DiCE's treatment of
one-hot columns; add the encoded number of features to Table 1 or the text.

### F11 [suggestion]

The like-for-like comparison with the seeds (one seed at a time, values under Strengths)
and the analysis without all four software-defect datasets both support the paper and
cost one sentence each, labelled as not planned. "Of 77 candidates examined": two of them
(pc1, wilt) were not put to rule 4 because the study was already complete
(`candidates.csv`).

## Dimension rationale

- **D1 = 3.** The evidence addresses "do the rankings agree", but for three measures a
  large part of the agreement is not evidence about datasets (F01), and the conclusion on
  measures rests on two definitions that are coupled (F02). Both are fixable in prose.
- **D2 = 3.5.** A rule fixed in advance with a threshold that can fail; the null it sits
  on could hardly have held (F08).
- **D3 = 3.5.** Tasks, repository and single configuration are stated; "as configured
  here" is present. F01 and F10 are what remains.
- **D4 = 4.5.** No contradiction between abstract, results, tables, figure and
  conclusions; F09 is a matter of emphasis.
- **D5' = 3.5.** Deviations, failures and the post hoc check are disclosed. F03, F06 and
  F07 are descriptions that do not match the code or the plan.
- **D6 = 3.5.** The tests, multiplicity control, unit of analysis and bootstrap are
  sound for k = 16 and correctly coded. The weakness is in the measures (F02, F03) and in
  two summaries on a heavy-tailed scale (F04, F05).

## Readiness assessment

Not ready as it stands; ready after a revision of the text. F01 and F02 change what the
conclusions may say, not a number. Everything needed for F01 to F10 is already in the
result files, except the equal-size gap of F02, which is further work. No rerun is
needed.

## Questions for the author

1. Is the paper's claim about the order "as the methods are usually configured", or about
   the methods? The answer decides how F01 is worded.
2. May two unplanned descriptive figures be printed with a label (features used and
   masked per method; the Anchors and DiCE cost order with medians)?
3. Were the cited papers read in full? This review could not check them.

## Comparison with the earlier review

- **Confirmed**: its re-derivation of the rankings and correlations; F04 (single
  configuration, DiCE random search), F05 (short explanations and the gap), F06 and F07.
  Its fixes for F01 to F07 and F09 are present in the text reviewed here; its F08
  (literature) stays open and could not be checked here either.
- **Overstated or wrong**: D2 = 5 is too high given the null (F08 here). Its F05 and F04
  are graded minor and were closed by softening a sentence; with the counts of masked
  features and of LIME's features they are the two major findings here (F02, F01). Its
  F01 was graded major and was a wording contradiction, already fixed; it would be minor
  on this scale.
- **Missed**: that sparsity is set by `num_features = 10` and the SHAP variant (F01);
  that stability reseeds every copy and is degenerate on categorical-only and d <= 5 data
  (F03); that the Anchors and DiCE exception on cost depends on the mean (F04); the scale
  of the cost variance shares (F05); the planned analyses not reported (F06); the wrong
  statement on LIME's draws and the scope of the time limit (F07); the composition of the
  sixteen and DiCE's continuous one-hot columns (F10).

## Editor's disposition (2026-10-12, not by the reviewer)

Added by the session that edits the manuscript, at the author's instruction to fix every
finding. The text above is the reviewer's and is unchanged. Figures printed for these
fixes come from `scripts/paper_f_posthoc_descriptives.py`, logged in the plan before it
was run; they equal the reviewer's counts (features masked 8.0, 6.5, 2.7 and 2.1; DiCE
faster than Anchors on 14 of 16 datasets by run medians; 99 and 114 time-limit failures).

| Finding | Action in `paper_f_template.tex` |
|---|---|
| F01 | Fixed. Abstract, a new paragraph of the Discussion and Conclusion 1 say that much of the agreement on sparsity, stability and cost follows from the output format, the algorithm and the settings, and name the orders the data decide. The mean number of features each method names is printed. Answer taken to question 1: the claim is about the methods as configured |
| F02 | Fixed in the text. The mean number of masked features is printed beside the features named; the Discussion and Conclusion 3 say the opposition of sparsity and the gap is partly built into the definitions; the gap at an equal number of masked features is named as further work. It is not computed |
| F03 | Fixed. The Measures say that each copy is explained with new draws, that data without numeric features receive no noise, and what happens with five features or fewer |
| F04 | Fixed. The planned mean stays the reported result; the Results add the count with run medians, labelled as made after the results, and the Discussion says the order on cost turns on the slow searches of DiCE |
| F05 | Fixed. The Results say the cost shares are of raw times and print the three-way term |
| F06 | Fixed. The last section lists the planned analyses that are in the archive and not in the paper, and what the aligned-rank check confirms |
| F07 | Fixed. The sentence on the draws excepts LIME; the time limit is said to cover an explanation and its ten copies; the time-limit failures are counted by method |
| F08 | Fixed in the Discussion: rejection of the null was to be expected; the evidence is the size of the agreement and the pairs that change |
| F09 | Fixed. Conclusion 2 names only the order of Anchors and DiCE, the pair whose three comparisons hold on fewer than 12 of 15 datasets |
| F10 | Fixed. The sources of error give the composition of the sixteen and DiCE's treatment of one-hot columns; the Methods give the range of encoded features |
| F11 | "Candidates examined" is now "candidates listed". The two further unplanned checks are not added |
| Question 3 | Open: the cited papers have not been read in full |
