::: {custom-style="Title"}
Do Faithfulness Metrics Agree? Metric-Dependent Rankings of Post-hoc Explanations on Tabular Data
:::

::: {custom-style="Article Type"}
Manuscript type: Research article
:::

::: {custom-style="Abstract Title"}
Abstract
:::

::: {custom-style="Abstract"}
Claims that one post-hoc explanation method is more faithful than another rest on a faithfulness
metric, and the available metrics operationalise faithfulness differently. This study measured
whether seven common metrics agree, using a paired design: SHAP, LIME, occlusion and a random
control explained four classifiers on eight public tabular datasets (five seeds, 200 instances
per condition), and every explanation was scored by every metric. In the pre-specified analysis,
the metrics broadly agreed on the order of the explainers (mean pairwise Spearman correlation
0.723, 95% CI [0.645,
0.802]) but agreed weakly on individual explanations
(0.154). A post-analysis review found that LIME had been stored as
local slopes rather than contributions, so contribution-based metrics placed it last almost
uniformly. A synthetic validation against exact Shapley values and a supplementary re-analysis
with LIME's surrogate contributions showed that this representation inflated system-level
agreement: with contributions, agreement fell to
0.529
([0.389,
0.669]), and to
0.309 under a second masking baseline, while
instance-level agreement was unchanged. Faithfulness-metric agreement therefore depends on the
level of evaluation, on the semantics of the attributions compared, and on the evaluation
protocol. Comparisons of explainers should declare what their attributions represent, report
more than one metric and masking baseline, and include a random control.
:::

::: {custom-style="Keywords"}
**Keywords:** explainable artificial intelligence; faithfulness metrics; feature attribution; evaluation; tabular data
:::

# 1. Introduction

Post-hoc explanation methods such as SHAP and LIME are widely used to inspect the predictions of
machine-learning models trained on tabular data, including in finance, health and public
administration [@salih2024; @obrienquinn2024; @qureshi2026]. Because different methods can give
different explanations for the same prediction [@krishna2024], their evaluation has become a
research area of its own, and the field still lacks agreed definitions and criteria [@weber2024].
Among the properties evaluated, *faithfulness*, the degree to which an explanation reflects the
reasoning of the model it explains, is usually treated as central [@lyu2024].

Faithfulness cannot be observed directly. It is estimated by perturbing the input according to
the explanation and observing the model's response: removing features in order of importance
(deletion) or restoring them from a baseline (insertion) [@samek2017], masking the most important
features or keeping only them (comprehensiveness and sufficiency) [@deyoung2020], correlating
attributions with the effect of removing single features [@bhatt2020], comparing attributions
with the response to random perturbations (infidelity) [@yeh2019], or retraining the model without
the top features [@hooker2019]. Each estimator encodes a different notion of faithfulness and
depends on choices such as the masking baseline, which can push inputs out of the data
distribution [@zheng2025; @simic2025].

If these metrics disagree, the statement "method A is more faithful than method B" is partly a
statement about the metric. Studies of the metrics themselves have found that fidelity metrics
lack verification and can give different verdicts on the same explanation
[@mironicolau2025], that perturbation-curve scores depend on the model [@edin2025], and that
rankings of attribution methods change with the evaluation setting [@duan2024]. Most of this
evidence comes from images and text; for tabular data, where much applied use of SHAP and LIME
occurs, the evaluation of explanations is less studied [@velmurugan2025].

Earlier studies of the same research programme found that the advantage of one explainer over
another depends on the model and its configuration [@ownB], that SHAP and LIME often disagree on
which features matter for an instance [@ownE], and that explainer rankings vary across datasets
[@ownF]. The present study asks a prior question: whether the measuring instrument itself gives a
consistent answer. It contributes a paired, multi-dataset measurement of agreement between seven
faithfulness metrics, at the level of explainer rankings and of individual explanations, with a
within-metric stability benchmark and a synthetic check against exact attributions. In the course
of the study, a construct mismatch was found in one explainer's output; supplementary experiments
specified after that finding show how much the observed agreement depended on it. The main
finding is that faithfulness-metric agreement depends on the level at which it is evaluated, on
the semantics of the attributions being compared, and on the evaluation protocol.

## 1.1. Related work

**Faithfulness metrics and their reliability.** Perturbation-based metrics were introduced for
images [@samek2017] and text [@deyoung2020] and later formalised for general feature attributions
[@yeh2019; @bhatt2020; @hooker2019]. Their reliability has been questioned on several grounds:
removal creates out-of-distribution inputs [@zheng2025; @nieradzik2024], the perturbation method
changes validation outcomes [@simic2025], model calibration affects perturbation-based results
[@decker2025], and scores are not comparable across models without normalisation [@edin2025].
Meta-evaluations construct explanations of known faithfulness to test the metrics
[@zaman2025; @mariotti2024], and benchmarks of evaluation measures in vision report incoherent or
manipulable results [@vandersmissen2024; @chowdhury2024; @fresz2024; @klotz2025]. Subjective,
objective and mathematical evaluation measures need not align either [@kares2027].

**Evaluation frameworks.** Systematic evaluations of methods and metrics show that design choices
such as the model and data type change which method is preferred, and recommend several metrics
[@klein2024; @bommer2024]. Applied tabular evaluations bundle several metrics, for example in
intrusion detection or health [@arreche2024; @qureshi2026], but rarely analyse how the metrics
relate. A recent tabular and image study reports that local explanation rankings depend on the
classifier, the masking operator and the computational budget [@ababneh2026].

**Disagreement.** The disagreement problem concerns explainers that disagree with each other
[@krishna2024; @mitrut2024; @parashar2026; @aggul2026]. Disagreement among the *criteria* of
faithfulness has recently been analysed conceptually, as choices left open by a general
requirement [@shanklin2026]. Impossibility results show that no attribution method can be
reliable for all end tasks on rich model classes [@bilodeau2024], and evaluation without ground
truth has its own limits [@rawal2025; @rahnama2024]. The present study is the empirical
counterpart for tabular data: a paired measurement of how far common metrics agree, with a
benchmark for their own stability and with the role of attribution semantics made explicit.

# 2. Materials and methods

## 2.1. Design and evidence classes

The design is fully paired: the same instances are explained by every explainer, and the same
explanations are scored by every metric. The factors are 8 datasets × 4 models × 4 explainers ×
7 metrics, with 5 seeds and 200 test instances per dataset, model and seed; a *block* is one
dataset, model and seed (160 blocks). The analysis plan, including hypotheses, statistics and the
decision rule, was fixed before the run. Because the study changed after a review of its first
results, the evidence is reported in five classes (Table 1); results of
different classes are never pooled, and only the first carries a decision.

| Class | Content | Specified |
|---|---|---|
| Confirmatory | H1 and H2, their intervals, tests, Holm correction and decision rule | Before the run |
| Pre-specified sensitivity | Second masking baseline, six metrics, four explainers, per model, winner flips, synthetic check | Before the run |
| Post-run specification | H2 test and interval, stability benchmark, synthetic statistic, ties, M4-undefined exclusion | After the run, before results were examined |
| Supplementary experiments | S3 (synthetic LIME representations) and S1 (LIME as contributions; S1-B primary, S1-M sensitivity) | After the review of the results |
| Exploratory diagnostics | Explainer positions, *f(x)*-adjusted H2, M7 removal sets and ties, random control last | After the review of the results |

Table: **Table 1.** Classes of evidence and when each was specified.

::: {custom-style="Source"}
Source: Authors.
:::

## 2.2. Datasets and models

Eight public binary classification datasets were taken from OpenML [@bischl2025], two from each of
four strata of feature composition and size (Table 2). The list was fixed before any
explanation was computed. The eligibility rule required a five-fold cross-validated AUC between
0.65 and 0.98 for at least two of the four models. The check was specified before the run but
executed after it, as a retrospective diagnostic; no dataset was to be removed whatever its
outcome. All eight datasets passed with all four models (AUC from 0.667 to
0.966).

Table: **Table 2.** Datasets, number of raw features and five-fold cross-validated AUC per model (LR logistic regression, RF random forest, XGB XGBoost, MLP multilayer perceptron).

| Dataset | OpenML ID | Stratum | Features | LR | RF | XGB | MLP |
|------------------|------:|------------------|----:|------:|------:|------:|------:|
| phoneme | 1489 | numeric-small | 5 | 0.819 | 0.962 | 0.939 | 0.928 |
| qsar biodeg | 1494 | numeric-small | 41 | 0.927 | 0.919 | 0.924 | 0.925 |
| magic telescope | 1120 | numeric-large | 10 | 0.837 | 0.933 | 0.926 | 0.929 |
| electricity | 151 | numeric-large | 8 | 0.827 | 0.966 | 0.922 | 0.901 |
| german credit | 31 | mixed | 20 | 0.771 | 0.781 | 0.792 | 0.750 |
| adult | 1590 | mixed | 14 | 0.905 | 0.901 | 0.924 | 0.883 |
| bank marketing | 1461 | mixed-categorical | 16 | 0.907 | 0.927 | 0.931 | 0.895 |
| compas | 42192 | mixed-categorical | 13 | 0.734 | 0.667 | 0.733 | 0.731 |

::: {custom-style="Source"}
Source: Authors.
:::

Logistic regression with L2 penalty, random forest, XGBoost [@chen2016] and a multilayer
perceptron were trained with one configuration for all datasets, recorded before training.
Numeric features were standardised, categorical features one-hot encoded and missing values
imputed. Each seed fixed a stratified 80/20 split, the model, the explainers' sampling and the
random control.

## 2.3. Explainers and attribution semantics

- **SHAP** [@lundberg2017; @li2024]: TreeSHAP for the tree models and KernelSHAP for logistic
  regression and the multilayer perceptron; an additive contribution relative to a background
  expectation.
- **LIME** [@ribeiro2016] for tabular data (package 0.2.0.1) with continuous features not discretised (*discretize_continuous* false),
  kernel width 3.0 (the package default is 0.75·√*p*), 1,000 samples drawn around the training
  mean, and all features. In this configuration LIME returns the coefficients of a locally
  weighted linear surrogate fitted on standardised features: a slope per training standard
  deviation, whose sign is the direction of change and not whether the feature's current value
  raises the prediction. It is not a per-feature contribution. One-hot columns are sampled as
  continuous values [@ademi2025; @knab2025].
- **Occlusion:** the drop in predicted-class probability when one feature is set to its baseline.
- **Random control:** attributions drawn from a standard normal distribution with a fixed seed.

Attributions of one-hot columns were summed per raw feature, and every explainer explained the
predicted class. The LIME output representation was decided in the original configuration and is
reported as run; it is examined by the supplementary experiments (Section 2.6).

## 2.4. Faithfulness metrics

Let *f(x)* be the predicted-class probability, *a* the attribution vector over *d* raw features,
*b* the masking baseline (training mean for numeric features, mode for categorical ones), and
*x*~*S*←*b*~ the instance with the features in *S* set to *b*. Let *π* order the features by
decreasing attribution toward the predicted class (ties by index) and *T* be the top
⌈0.2*d*⌉ features. Deletion (M1) and insertion (M2), in Equation (1), are the areas under the probability
curve as features are masked from *x*, or restored from *b*, in the order *π*:

$$M_1 = \frac{1}{d}\sum_{k=1}^{d} f\big(x_{\pi_{1..k}\leftarrow b}\big), \qquad M_2 = \frac{1}{d}\sum_{k=1}^{d} f\big(b_{\pi_{1..k}\leftarrow x}\big) \qquad (1)$$

The top-*k* prediction gap (M3) and sufficiency (M6) mask the top features or all others
(Equation (2)):

$$M_3 = f(x) - f\big(x_{T\leftarrow b}\big), \qquad M_6 = f(x) - f\big(x_{\bar{T}\leftarrow b}\big) \qquad (2)$$

Faithfulness correlation (M4) [@bhatt2020] is the Pearson correlation between *a*~*i*~ and the
single-feature effect *Δ*~*i*~ = *f(x)* − *f(x*~{*i*}←*b*~*)*. Infidelity (M5) [@yeh2019] is used in
a scale-free form (Equation (3)): over 100 random subsets *S*~*r*~ (each feature masked with probability 0.5),

$$M_5 = 1 - R^2\Big(f(x) - f\big(x_{S_r\leftarrow b}\big) \sim \textstyle\sum_{i\in S_r} a_i\Big) \qquad (3)$$

where the fit has no intercept; subset masking replaces Gaussian noise, which is undefined for
categorical features. M7, ROAR-lite [@hooker2019], ranks features by the mean |*a*| over an
explainer's instances, retrains the model without the top 10, 20, 30 and 50% of features and
scores the mean drop in test AUC; it has one value per block and explainer. Lower is better for
M1, M5 and M6, and higher for M2, M3, M4 and M7; all metrics were oriented so that higher means
more faithful before ranking. M1 to M6 treat attributions as signed contributions relative to the
masking baseline, which holds for SHAP and occlusion but not for LIME as configured; M7 uses only
magnitudes. M4 and occlusion share their construction (single-feature masking), so M4 is expected
to favour occlusion.

## 2.5. Agreement analysis

**System level (H1).** In each block, the three studied explainers (SHAP, LIME, occlusion) were
ranked under each metric: by their mean score over the 200 instances for M1 to M6 and by the
block's value for M7, with average ranks for ties. Agreement was the mean pairwise Spearman
correlation over the 21 metric pairs (Equation (4)),

$$\bar\rho = \frac{1}{21}\sum_{m<m'} \rho_s\big(r_m, r_{m'}\big) \qquad (4)$$

where *r*~*m*~ is the explainers' rank vector under metric *m*, together with Kendall's *W* with tie
correction; an undefined correlation (all explainers tied) was left out and counted. Because the
20 blocks of a dataset are not independent, the dataset was the unit of inference: estimates were
averaged within each dataset, and the 95% interval is a *t*-interval over the eight dataset means.
The null hypothesis that the metrics rank the explainers independently was tested by a
permutation test that applied one permutation of the explainer labels per dataset and metric to
all blocks of that dataset (one-sided). A simulation run before the experiment showed that
permuting within blocks inflates false positives when blocks are correlated, and that a
percentile bootstrap over eight datasets undercovers.

**Within-metric stability benchmark.** For each dataset, model and metric, the order of the
studied explainers in each seed was compared with every other seed (ten seed pairs, Spearman).
Seeds change the split, the model and the explainers' sampling, so the benchmark is a reference
level for between-metric agreement, not an upper bound.

**Instance level (H2).** For each block and explainer (all four), the Spearman correlation across
the 200 instances was computed for each of the 15 pairs of M1 to M6, averaged within the block and
then within the dataset; the interval is the *t*-interval over the eight dataset values, with a
one-sided *t*-test of a positive mean and an exact sign-flip test as a supplement. The 15 pairs
were tested with Holm correction.

**Decision rule.** The classification of Table 3, fixed before the run, uses the raw
permutation *p* of H1 and its interval; Holm correction over H1 and H2 is reported beside it. With
three ranked explainers, if one explainer holds the same first or last rank under every metric in
a block, each pairwise correlation is 0.5 or 1, so the block's agreement cannot fall below 0.5;
the classification is therefore read with the distribution of explainer positions.

Table: **Table 3.** Decision rule for H1, fixed before the run.

| Outcome of the permutation test and the 95% interval | Wording |
|------------------------------------|------------------------------------|
| *p* ≥ .05 | no evidence that the metrics share an order |
| *p* < .05, interval above 0.5 | the metrics broadly agree |
| *p* < .05, interval below 0.5 | the metrics agree only weakly |
| *p* < .05, interval contains 0.5 | agreement present, strength not determined |

::: {custom-style="Source"}
Source: Authors.
:::

**Secondary and sensitivity analyses (pre-specified).** The share of blocks in which the
top-ranked explainer changes between two metrics (winner flips; ties at the top counted
separately); strict SHAP–LIME order reversals; the analysis with the random control as a fourth
explainer; M1, M2, M3 and M6 recomputed with a second baseline (a random training row); the
analysis without M4 (six metrics); and per-model summaries. A planned variance decomposition was
omitted because its specification was incomplete, a deviation from the plan. Details fixed after
the run but before results were examined (Table 1) include an analysis
excluding the 147 of 128,000 instance-level M4 scores that
were undefined.

**Synthetic check.** Four synthetic conditions used known functions directly as the model: an
additive logistic function and one with two pairwise interactions, each with eight standard normal
features, independent or correlated (pairwise correlation 0.5). Exact interventional Shapley
values of the predicted-class probability served as true attributions [@rahnama2024;
@islam2025]. For each condition and seed, the explainers were ordered by their mean Spearman
correlation with the truth (the reference order), and each of M1 to M6 was scored by the Spearman
correlation between its order of the explainers and the reference order.

## 2.6. Supplementary experiments and exploratory diagnostics

A post-analysis review found the LIME representation issue of Section 2.3 (the same behaviour had
been documented in an earlier study of the programme [@ownE]). The following analyses were
specified after that review, with their outputs written separately from the original results,
which were not modified; they carry no test decision.

**S3, synthetic validation of LIME representations.** In the synthetic conditions, three
representations of LIME were compared with the exact Shapley values (instance-level Spearman
correlation): the stored slopes; the contributions of LIME's fitted surrogate relative to its
training mean, *w*~*j*~(*x*~*j*~ − *μ*~*j*~)/*s*~*j*~; and LIME with quartile discretisation; each at
kernel width 3.0 and at the package default.

**S1, LIME as surrogate contributions on the real data.** LIME was re-explained with the frozen
configuration on the same instances, and its fitted surrogate was represented as the contribution
of each raw feature relative to a reference *r* (Equation (5)):

$$c_j(r) = \sum_{k \in G_j} w_k\,\frac{x_k - r_k}{s_k} \qquad (5)$$

where *G*~*j*~ is the set of encoded columns of feature *j*, *w*~*k*~ the surrogate's coefficient on
standardised column *k* and *s*~*k*~ its scale. In S1-B, the primary variant, *r* is the metrics'
masking baseline; in S1-M, the sensitivity variant, *r* is LIME's training mean. The two coincide
for numeric features. Every instance was reconstructed and checked against the stored run before
use, and the metrics were recomputed on the S1 attributions; the analyses of Section 2.5 were then
repeated with the S1 LIME rows substituted for the original ones and every other row unchanged.
For categorical features, S1 rests on a surrogate fitted to off-manifold one-hot samples.

**Exploratory diagnostics.** The frequency with which each explainer holds each rank under each
metric (positions); the H2 correlations adjusted for the predicted-class probability by a
rank-based partial correlation, since several metrics scale with *f(x)*; the size of M7's removal
sets and the frequency of identical sets and tied scores; and the share of blocks in which every
metric places the random control last.

## 2.7. Reproducibility

Code, configuration, per-instance scores and every analysis output are released under an open
licence (archive identifier withheld for double-blind review). All numbers in this article are
rendered by a script from the committed result files and re-derived by an automated check. The
runs used one laptop (Intel Core i5-1335U CPU) with a fixed software environment.

# 3. Results and discussion

## 3.1. Broad agreement under the original attribution representations (confirmatory)

At system level, the mean pairwise Spearman correlation between metrics was
0.723 (95% CI [0.645,
0.802]) and Kendall's *W* 0.762
([0.701, 0.824]). The permutation test gave
*p* = 0.00001 (the smallest value attainable with
100,000 permutations), and *p* = 0.00002 after
Holm correction over H1 and H2. With the interval above 0.5, the frozen decision rule classifies
the result as "the metrics broadly agree", both before and after correction. The within-metric
stability benchmark was 0.873
([0.826, 0.920]), so the
metrics agreed with each other less than each agreed with itself across seeds. Agreement was
lowest for random forests (0.637) and highest for logistic regression
(0.798). Excluding the undefined M4 scores left the estimate unchanged
(0.723).

At instance level, agreement was weak: the mean correlation between metric pairs across instances
was 0.154 ([0.099, 0.209];
one-sided *t*-test *p* = 0.00016, sign-flip *p* = 0.0039, the smallest attainable with eight
datasets).
H2 is supported as a positive mean, but its size is small, and the pairs differed in sign:
deletion and insertion correlated negatively (−0.351), as did
infidelity and sufficiency (−0.181), whereas deletion and
the top-*k* gap correlated most strongly (0.507; Figure 1).

These confirmatory results are reported exactly as specified. They describe agreement among the
metrics for the explainer outputs *as stored*; as Section 2.3 explains, LIME's stored output was a
slope, while M1 to M6 read attributions as contributions. Sections 3.3 and 3.4 show what this
means for the result.

![**Figure 1.** Mean instance-level Spearman correlation between metric pairs over eight datasets (original representation): unadjusted (lower triangle, H2) and adjusted for the predicted-class probability (upper triangle, exploratory).](figures/fig_h2_matrix.png){width=100%}

::: {custom-style="Source"}
Source: Authors.
:::

## 3.2. Pre-specified sensitivity analyses

The second masking baseline lowered system-level agreement to
0.616 ([0.546,
0.687]); removing M4 gave
0.690, and adding the
random control as a fourth explainer 0.753. The explainer
ranked first changed between two of M1 to M6 in 6.9% to
31.3% of blocks, and between M7 and another metric in
49.4% to 63.8%. In the synthetic check, the
metrics' order of the four explainers agreed with the reference order with a mean Spearman
correlation from 0.76 (M5) to 0.92 (M1); the
reference order itself placed LIME third or fourth of four in all 20
conditions and seeds, which, given its slope output, reflects the representation rather than the
method (Section 3.3).

## 3.3. LIME's output representation against exact attributions (S3, supplementary)

In the synthetic conditions, the stored slopes were unrelated to the exact Shapley values (mean
Spearman 0.02 with independent and
0.02 with correlated additive features), whereas the surrogate
contributions of the same fitted LIME model agreed closely in the additive conditions
(0.96 with independent and
0.96 with correlated features) and moderately with interactions
(0.64 to
0.71). Discretised LIME lay between them
(0.58 to
0.89), and the kernel width changed little
(Figure 2). The construct mismatch is therefore one of representation, not of LIME's fit: the
same surrogate, read as a contribution, tracks the true attributions.

![**Figure 2.** Agreement of LIME representations with exact Shapley values in the synthetic conditions (mean over five seeds; bars at kernel width 3.0 with the range over seeds, diamonds at the package default width).](figures/fig_s3.png){width=100%}

::: {custom-style="Source"}
Source: Authors.
:::

## 3.4. Agreement with LIME represented as contributions (S1, supplementary)

With S1-B, system-level agreement fell from 0.723
to 0.529
([0.389,
0.669]), an interval that contains
0.5, and Kendall's *W* from 0.762 to
0.588 (Table 4). Agreement fell in seven of the eight
datasets, most for compas (0.639 to 0.271) and qsar biodeg
(0.676 to 0.336), and rose for electricity
(0.578 to 0.759; Figure 3). The
mean over the numeric datasets fell from 0.758 to
0.484, and over the mixed ones from 0.703 to
0.557. Under the second masking baseline, S1-B agreement was
0.309, against
0.616 originally (Figure 4).
Instance-level agreement was unchanged (0.147), and so
was its pattern: deletion and insertion still correlated negatively
(−0.407). The two S1 variants differed by at
most 0.024 in any summary quantity, so the choice of reference does not change
these conclusions. No decision rule is applied to S1; the confirmatory classification of
Section 3.1 stands for the representation it was made on.

Table: **Table 4.** System-level and instance-level agreement under the three LIME representations (mean over eight datasets with 95% *t*-interval; counts of the 160 blocks). Class A is confirmatory; other rows are pre-specified sensitivity analyses, supplementary (S1) or exploratory (C).

| Quantity | Original (LIME slopes) | S1-B | S1-M |
|--------------------------------|------------------|------------------|------------------|
| H1-form agreement, mean pairwise Spearman (A for original) | 0.723 [0.645, 0.802] | 0.529 [0.389, 0.669] | 0.540 [0.389, 0.692] |
| Kendall's *W* | 0.762 [0.701, 0.824] | 0.588 [0.473, 0.703] | 0.598 [0.471, 0.725] |
| Second masking baseline | 0.616 [0.546, 0.687] | 0.309 [0.219, 0.398] | 0.285 [0.212, 0.359] |
| Six metrics (M4 removed) | 0.690 [0.602, 0.777] | 0.483 [0.336, 0.629] | 0.489 [0.329, 0.649] |
| With the random control (four explainers) | 0.753 [0.700, 0.806] | 0.757 [0.689, 0.824] | 0.762 [0.689, 0.835] |
| Within-metric stability benchmark | 0.873 [0.826, 0.920] | 0.797 [0.727, 0.867] | 0.798 [0.724, 0.873] |
| H2-form instance-level agreement (A for original) | 0.154 [0.099, 0.209] | 0.147 [0.095, 0.199] | 0.154 [0.097, 0.212] |
| H2-form, adjusted for *f(x)* (C) | 0.233 [0.155, 0.312] | 0.225 [0.143, 0.306] | 0.235 [0.147, 0.323] |
| Blocks with one explainer at the same extreme rank under all seven metrics (C) | 96 | 44 | 43 |
| ... LIME untied last under all seven metrics (C) | 87 | 25 | 27 |
| Random control untied last under all seven metrics (C) | 15 | 126 | 128 |
| Blocks with any strict SHAP–LIME reversal | 46 | 96 | 92 |
| Winner flips, pairs of M1–M6 (%) | 6.9–31.3 | 7.5–40.6 | 7.5–39.4 |
| Winner flips, pairs with M7 (%) | 49.4–63.8 | 49.4–62.5 | 46.3–59.4 |

::: {custom-style="Source"}
Source: Authors.
:::

![**Figure 3.** System-level agreement between metrics per dataset under the original LIME slopes and the two S1 contribution representations; grey bars show the within-metric stability benchmark and the dashed line the decision threshold of 0.5.](figures/fig_agreement_datasets.png){width=100%}

::: {custom-style="Source"}
Source: Authors.
:::

![**Figure 4.** System-level agreement under the specified sensitivity analyses for the three LIME representations (mean over eight datasets with 95% *t*-interval).](figures/fig_sensitivity.png){width=100%}

::: {custom-style="Source"}
Source: Authors.
:::

## 3.5. Explainer positions (exploratory)

Under the original representation, LIME was ranked last by each of M1, M2, M3, M4 and M6 in all
160 blocks (and by M5 in 157), and was the untied
last explainer under all seven metrics in 87 blocks
(Figure 5). In such blocks the system-level correlation cannot fall below 0.5, so much
of the original agreement was agreement on which explainer was last. With S1-B, LIME was last
under all seven metrics in 25 blocks, and was last under M1
in 100 blocks; the order of the three explainers then varied
between metrics, and strict SHAP–LIME reversals between two of M1 to M6 occurred in
7.5% to 33.8% of blocks (original
0.0% to 1.9%); in pairs with M7, which uses only
magnitudes, they occurred in 26.9% to 28.8% of blocks originally and
30.0% to 37.5% with S1-B. Occlusion was ranked first
by M4 in all 160 blocks under both representations, as the
shared construction of M4 and occlusion predicts.

![**Figure 5.** Rank of each studied explainer under each metric over the 160 blocks, with LIME as stored (slopes, top) and as contributions relative to the masking baseline (S1-B, bottom).](figures/fig_positions.png){width=100%}

::: {custom-style="Source"}
Source: Authors.
:::

## 3.6. Instance-level agreement adjusted for the prediction (exploratory)

Adjusting the instance-level correlations for the predicted-class probability raised their mean
from 0.154 to 0.233
([0.155, 0.312]). The negative correlation
between deletion and insertion largely disappeared (0.094),
which indicates that it arose because both metrics scale with *f(x)* in opposite directions;
insertion and sufficiency became strongly related (0.712;
Figure 1). Even adjusted, instance-level agreement remained far below system-level
agreement, under every representation (0.225
with S1-B).


## 3.7. Retraining metric and random control (exploratory)

M7 was the least stable metric: its agreement with itself across seeds was
0.384 under the original representation and 0.394
with S1-B, and winner flips involving M7 occurred in 49.4% to
62.5% of blocks with S1-B. Its removal sets are small when there are few
features (phoneme has 5 raw features, so the first removal level removes
1), different explainers then often remove the same set, and their scores
tie; ties between explainers were most frequent for logistic regression
(40% of its blocks). The random control was the untied last
explainer under all seven metrics in 15 of 160 blocks under the
original representation and in 126 with S1-B; only with
comparable LIME attributions did it behave as a negative control should.

## 3.8. Discussion

The results support three conclusions about faithfulness-metric agreement.

**It depends on the level of evaluation.** Metrics that agree on the order of explainers can
disagree on which individual explanations are faithful: system-level agreement was
0.723 (original) or
0.529 (S1-B), whereas
instance-level agreement was 0.154 under every representation, and some metric
pairs correlated negatively. Part of the instance-level disagreement is a shared dependence on the
predicted probability rather than on the explanation. A metric that is adequate to rank
explainers on average is therefore not thereby adequate to validate a single explanation, which is
the use made of explanations in practice [@rawal2025; @bilodeau2024].

**It depends on attribution semantics.** The confirmatory "broad agreement" was obtained with an
explainer whose output was a slope scored by metrics that read contributions. Every
contribution-based metric placed that explainer last, which produced agreement by construction of
the comparison rather than by consensus on faithfulness. Represented as contributions of the same
fitted surrogate, LIME competed with SHAP and occlusion, and agreement became moderate and
uncertain. The finding generalises beyond LIME: an evaluation compares attributions only if they
answer the same question, relative to the same reference [@li2024; @sokol2025; @knab2025]. It
complements the conceptual account of why faithfulness criteria disagree [@shanklin2026] with an
empirical case in which the disagreement was hidden by a representation mismatch.

**It depends on the evaluation protocol.** Once LIME was comparable, the masking baseline became
the dominant source of variation (S1-B 0.529
against 0.309 under the second baseline), in line with
evidence that perturbation choices drive validation outcomes [@simic2025; @zheng2025;
@ababneh2026]. The retraining metric was unstable and tie-prone, metric pairs flipped the winner
in up to 40.6% of blocks even among M1 to M6 with S1-B, and M4 favoured
the explainer that shares its construction. With three explainers, a single consistently last
explainer is enough to satisfy a 0.5 threshold, so aggregate agreement statistics must be read
with the explainers' positions [@duan2024; @edin2025].

**Recommendations.** Comparisons of explainers on tabular data should (1) declare what each
explainer's output represents and its reference point, and check it against what each metric
assumes; (2) report at least two metrics from different families and at least two masking
baselines; (3) include a random control and report how often it ranks last; (4) report a
within-metric stability benchmark and the explainers' rank positions next to any aggregate
agreement statistic; and (5) separate claims about rankings from claims about individual
explanations.

**Limitations.** The study has eight binary tabular datasets and four model families, and three
studied explainers make rank statistics coarse. LIME was run in one configuration whose output is a
slope; S1 addresses its representation but not its fitting choices (kernel, sampling around the
training mean), which also affect its stability [@tzionis2026], and for categorical features S1 rests on a surrogate fitted to off-manifold samples
[@ademi2025]. SHAP's reference (a background expectation) differs from the masking baseline used by
S1-B and the metrics. The supplementary experiments and diagnostics were specified after the
first results had been reviewed; they are reported as such and carry no decision, and S1 was not
tested against the original analysis. Several analysis details were fixed after the run, the
dataset check was run retrospectively, and the planned variance decomposition was omitted. The
decision threshold of 0.5 cannot separate agreement on every position from agreement on the last
position. Ground truth exists only in a small synthetic setting; on real data the study measures
agreement, not correctness. The metrics share masking machinery, M4 shares its construction with
occlusion, M3 and M6 use one masking fraction, M5 is a Monte Carlo estimate, and M7 uses four
removal levels with one retraining each. Instance-level correlations depend on the predicted
probability, and the adjusted correlations are exploratory.

# 4. Conclusions

Faithfulness metrics agreed broadly on the order of explainers in the pre-specified analysis, and
weakly on individual explanations. The broad system-level agreement depended on an explainer
whose output did not match what the metrics assume; with comparable attributions, agreement was
moderate, uncertain and strongly dependent on the masking baseline, while instance-level agreement
stayed weak. Whether faithfulness metrics agree is therefore not a property of the metrics alone
but of the level of evaluation, the semantics of the attributions and the evaluation protocol.
Claims that one explainer is more faithful than another should state all three. Future work should
extend the comparison to explainers with declared reference semantics, to more masking schemes and
to regression and multiclass tasks.

# Funding

[Author to state the funding, or: "This research received no external funding."]

# Author contributions

[Withheld for double-blind review. At acceptance, in CRediT terms, for example: Conceptualization,
Methodology, Software, Formal analysis, Investigation, Data curation, Visualization, Writing –
original draft, Writing – review & editing.]

# Conflicts of interest

[Author to confirm: "The author declares no conflicts of interest."]

# Data availability statement

The datasets are public on OpenML (identifiers in Table 2). Code, configuration,
per-instance scores and all analysis outputs are openly available in an archived repository whose
persistent identifier is withheld for double-blind review and will be added at acceptance.

# Declaration of generative AI use

During the preparation of this work, the author used Claude (Anthropic; model identifier claude-opus-5-5), through the Claude
Code tool, to write and test the experiment, analysis and figure code, to draft the text of all
sections from the author's analysis plan and results, and to search for and check references
against their bibliographic records. All numbers are rendered by script from the result files. The
author reviewed and edited the content and takes full responsibility for it. [Author to confirm
the wording and the sections concerned.]
