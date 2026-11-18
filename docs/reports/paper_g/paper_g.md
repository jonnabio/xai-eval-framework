::: {custom-style="Title"}
Do faithfulness metrics agree? Metric-dependent rankings of post-hoc explanations on tabular data
:::

::: {custom-style="Article Type"}
Manuscript type: Research article
:::

::: {custom-style="Abstract Title"}
Abstract
:::

::: {custom-style="Abstract"}
Claims that one post-hoc explanation method is more faithful than another rest on a faithfulness
metric, and the available metrics operationalise faithfulness differently. This study asked
whether seven common metrics agree, and tested two hypotheses fixed before the run: that the
metrics rank explainers in the same order (H1) and that they correlate positively across
individual explanations (H2). SHAP, LIME, occlusion and a random control explained four
classifiers on eight public tabular datasets (five seeds, 200 instances per condition), and every
explanation was scored by every metric. Both hypotheses were supported: the metrics broadly agreed
on the order of the explainers (mean pairwise Spearman correlation
0.723, 95% CI [0.645,
0.802]) but only weakly on individual explanations
(0.154). In the configuration used, LIME's
output was a local slope, not the contribution that the metrics assume, and contribution-based
metrics ranked it last in every block. In supplementary analyses specified after this finding and
carrying no test decision, the slopes were unrelated to exact Shapley values
in synthetic data while LIME's surrogate contributions tracked them, and with LIME represented as
contributions on the real data, system-level agreement was
0.529
([0.389,
0.669]), and
0.309 under a second masking baseline, while
instance-level agreement was unchanged. The metrics therefore agreed on rankings only under the
original setup, and weakly on individual explanations. Comparisons of explainers should declare what their attributions represent, report more than one
metric and masking baseline, and include a random control.
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
[@ownF]. The present study asks a prior question, about the measuring instrument itself: **do
common faithfulness metrics agree on which explanations are more faithful?** Agreement is examined
at two levels, each with a hypothesis fixed before the experiment:

- **H1 (system level):** within each dataset, model and seed, the metrics rank the explainers in
  the same order more often than chance would produce. The null hypothesis is that the metrics
  rank the explainers independently.
- **H2 (instance level):** across the individual explanations of one explainer, pairs of metrics
  are positively correlated. The null hypothesis is that the mean correlation is not positive.

The study contributes a paired, multi-dataset test of both hypotheses for seven faithfulness
metrics on tabular data, with a within-metric stability benchmark and a synthetic check against
exact attributions. During the study, one explainer's output was found not to be of the kind the
metrics assume; supplementary experiments specified after that finding show how the answer
changes when the mismatch is removed.

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
relate. Benchmark frameworks also bundle faithfulness metrics for tabular explainers
[@agarwal2022], but report them side by side rather than measuring how far they agree. A recent
tabular and image study reports that local explanation rankings depend on the
classifier, the masking operator and the computational budget [@ababneh2026].

**Disagreement.** The disagreement problem concerns explainers that disagree with each other
[@krishna2024; @mitrut2024; @parashar2026; @aggul2026]. Disagreement among the *criteria* of
faithfulness has recently been analysed conceptually, as choices left open by a general
requirement [@shanklin2026]. Impossibility results show that no attribution method can be
reliable for all end tasks on rich model classes [@bilodeau2024], and evaluation without ground
truth has its own limits [@rawal2025; @rahnama2024]. The present study is the empirical
counterpart for tabular data: a paired measurement of how far common metrics agree, with a
benchmark for their own stability and with the role of attribution semantics made explicit.
Table 1 sets it against the closest studies.

Table: **Table 1.** Closest studies and how the present study differs.

| Study | What it examines | Difference in the present study |
|----------------|------------------------------------|------------------------------------|
| @duan2024 | Consistency of attribution-evaluation results across evaluation settings, on images | Tabular data; paired agreement between seven metrics at ranking and instance level |
| @edin2025 | Perturbation-curve scores that are not comparable across models, and their normalisation | Agreement between metric families, not the scale of one metric |
| @mironicolau2025 | Fidelity metrics that lack verification and can disagree on the same explanation | Multi-dataset measurement with a within-metric stability benchmark and the dataset as the unit of inference |
| @ababneh2026 | Dependence of explainer rankings on classifier, masking operator and budget | Agreement among metrics on the same explanations, with the attribution semantics made explicit |
| @shanklin2026 | Conceptual account of why faithfulness criteria disagree | Empirical counterpart with a random control and a synthetic ground-truth check |

::: {custom-style="Source"}
Source: Authors.
:::

# 2. Materials and methods

## 2.1. Design and evidence classes

The design is fully paired: the same instances are explained by every explainer, and the same
explanations are scored by every metric. The factors are 8 datasets × 4 models × 4 explainers ×
7 metrics, with 5 seeds and 200 test instances per dataset, model and seed; a *block* is one
dataset, model and seed (160 blocks). The research question, the hypotheses, the metrics, the H1 statistic,
interval, permutation test and decision rule, and the planned secondary and sensitivity analyses
were fixed in the analysis plan before the run. Other operational details were fixed after the
run had finished but before any metric value, attribution or agreement statistic was examined;
the analysis was then run once, and its outputs were frozen. A review of those outputs led to two
supplementary experiments and four exploratory diagnostics. The evidence is therefore reported in
five classes (Table 2); results of different classes are never pooled. H1 and H2
are tested only in the original analysis, and only H1 has a rule, fixed before the run, that
classifies the strength of agreement.

| Class | Content | When specified |
|---|---|---|
| Pre-specified | Hypotheses H1 and H2; metrics and their directions; H1 statistic, dataset-level *t*-interval, dataset-unit permutation test and decision rule; Holm correction over H1 and H2; the H2 estimate; winner flips, SHAP–LIME order, second masking baseline, random control, per-model summaries; synthetic-check design | Before the run |
| Pre-unblinding clarifications | Seven metrics and the three studied explainers as the primary H1 population; ties and undefined correlations; degenerate M4 values kept as stored; the within-metric stability benchmark; H2 orientation, *t*-interval, one-sided *t*-test, sign-flip test and Holm over its 15 pairs; the synthetic statistic; raw permutation *p* for the decision table; the six-metric sensitivity; the M4-exclusion sensitivity; the retrospective dataset check; omission of the variance shares | After the run, before any result was examined |
| Original analysis | The two classes above, run once on the frozen data; outputs frozen | After the pre-unblinding clarifications |
| Supplementary experiments | S3 (synthetic LIME representations) and S1 (LIME as surrogate contributions; S1-B primary, S1-M sensitivity) | After the original results were reviewed |
| Exploratory diagnostics | Explainer positions; *f(x)*-adjusted instance-level correlations; M7 removal sets and ties; random control last | After the original results were reviewed |

Table: **Table 2.** Classes of evidence and when each was specified.

::: {custom-style="Source"}
Source: Authors.
:::

## 2.2. Datasets and models

Eight public binary classification datasets were taken from OpenML [@bischl2025], two from each of
four strata of feature composition and size (Table 3). The list was fixed before any
explanation was computed. The eligibility rule required a five-fold cross-validated AUC between
0.65 and 0.98 for at least two of the four models. The check was specified before the run but
executed after it, as a retrospective diagnostic; no dataset was to be removed whatever its
outcome. All eight datasets passed with all four models (AUC from 0.667 to
0.966).

Table: **Table 3.** Datasets, number of raw features and five-fold cross-validated AUC per model (LR logistic regression, RF random forest, XGB XGBoost, MLP multilayer perceptron).

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
random control. All datasets are public, de-identified benchmark tables; the study involved no
human participants.

## 2.3. Explainers and their reference points

The explainers differ in what their output represents and, for those that output contributions,
in the reference point the contribution is measured from.

- **SHAP** [@lundberg2017; @li2024]: interventional TreeSHAP on the predicted probability for the
  tree models and KernelSHAP (no feature selection) for logistic regression and the multilayer
  perceptron, both with a background sample of 50 training rows. The output is an additive
  contribution relative to the model's expected output over that background sample.
- **Occlusion:** the change in predicted-class probability when one feature alone is set to the
  metrics' masking baseline *b* (Section 2.4); a contribution relative to *b* for that feature
  only, without interactions.
- **LIME** [@ribeiro2016] for tabular data (package 0.2.0.1) with continuous features not
  discretised (*discretize_continuous* false), kernel width 3.0 (the package default is
  0.75·√*p*), 1,000 samples drawn around the training mean, and all features. In this
  configuration LIME returns the coefficients of a locally weighted linear surrogate fitted on
  standardised features: a slope per training standard deviation, whose sign is the direction of
  change and not whether the feature's current value raises the prediction. It has no reference
  point and is not a per-feature contribution. One-hot columns are sampled as continuous values,
  so the surrogate is fitted partly on points off the one-hot manifold [@ademi2025; @knab2025].
- **Random control:** attributions drawn from a standard normal distribution with a fixed seed.

Attributions of one-hot columns were summed per raw feature, and every attribution was oriented
to the predicted class. The LIME output representation was decided in the original configuration
and is reported as run; it is examined by the supplementary experiments (Section 2.6).

## 2.4. Faithfulness metrics

Let *f(x)* be the predicted-class probability, *a* the oriented attribution vector over the *G*
raw features, *b* the masking baseline (training mean for numeric features, the one-hot of the
training mode for categorical ones), and *x*~*S*←*b*~ the instance with the features in *S* set to
*b* (all columns of a one-hot feature together). Let *π* order the features by decreasing *a*
(ties by index) and *T* = {*π*~1~, …, *π*~*k*~} be the top *k* = max(1, ⌈0.2*G*⌉) features.
Deletion (M1) and insertion (M2) are the trapezoidal areas over *G* + 1 equally spaced points
(step 1/*G*) of the curves *p*~*t*~ = *f*(*x*~{*π*1..*πt*}←*b*~), which masks the first *t* features,
and *q*~*t*~ = *f*(*x*~{*πt+1..πG*}←*b*~), which restores the first *t* features to a fully masked
instance, for *t* = 0, …, *G* (Equation (1)). The endpoints are *p*~0~ = *q*~*G*~ = *f(x)* and
*p*~*G*~ = *q*~0~ = *f(b)*:

$$M_1 = \frac{1}{G}\Big[\frac{p_0 + p_G}{2} + \sum_{t=1}^{G-1} p_t\Big], \qquad M_2 = \frac{1}{G}\Big[\frac{q_0 + q_G}{2} + \sum_{t=1}^{G-1} q_t\Big] \qquad (1)$$

The top-*k* prediction gap (M3) masks the top features and sufficiency (M6) masks all others
(Equation (2)):

$$M_3 = f(x) - f\big(x_{T\leftarrow b}\big), \qquad M_6 = f(x) - f\big(x_{\bar{T}\leftarrow b}\big) \qquad (2)$$

Faithfulness correlation (M4) [@bhatt2020] is the Pearson correlation between *a*~*i*~ and the
single-feature effect *Δ*~*i*~ = *f(x)* − *f*(*x*~{*i*}←*b*~); when *a* or *Δ* is constant the
correlation is undefined, and the frozen code stores 0 and flags the score
(147 of 128,000 scores). Infidelity (M5) [@yeh2019] is used
in a scale-free form (Equation (3)): over *R* = 100 random subsets *S*~*r*~ (each feature masked
independently with probability 0.5; a subset that masks nothing is given one randomly chosen
feature; the subsets are shared by all explainers of an instance), with
*Δ*~*r*~ = *f(x)* − *f*(*x*~*Sr*←*b*~) and *s*~*r*~ = Σ~*i*∈*Sr*~ *a*~*i*~,

$$M_5 = \frac{\sum_{r=1}^{R}\big(\Delta_r - \hat\beta s_r\big)^2}{\sum_{r=1}^{R}\Delta_r^2}, \qquad \hat\beta = \frac{\sum_{r} s_r\Delta_r}{\sum_{r} s_r^2} \qquad (3)$$

that is, one minus the uncentred *R*² of the least-squares fit of *Δ* on *s* without intercept
(*M*~5~ = 0 if all *Δ*~*r*~ are 0 and 1 if all *s*~*r*~ are 0); subset masking replaces Gaussian
noise, which is undefined for categorical features. M7, ROAR-lite [@hooker2019], ranks features by
the mean |*a*| over an explainer's 200 instances; for each share ℓ ∈ {10%, 20%, 30%, 50%} the top
max(1, ⌈ℓ*G*⌉) features are set to *b* in the training and test data, the model is retrained, and
M7 is the mean over ℓ of the drop in test AUC; it has one value per block and explainer. Lower is
better for M1, M5 and M6, and higher for M2, M3, M4 and M7; all metrics were oriented so that
higher means more faithful before ranking. M1 to M6 read attributions as signed contributions
relative to *b*: occlusion's output is of that kind, SHAP's is a contribution relative to a
different reference (the background expectation), and LIME's slopes are not contributions; M7
uses only magnitudes. M4 and occlusion share their construction (single-feature masking), so M4
is expected to favour occlusion. The second masking baseline replaces *b* by one training row
drawn at random for each instance (the same row for every explainer).

## 2.5. Agreement analysis

**System level (H1).** In each block *u*, the three studied explainers (SHAP, LIME, occlusion)
were ranked under each metric: by their mean score over the 200 instances for M1 to M6 and by
the block's value for M7, with average ranks for ties. The block's agreement is the mean Spearman
correlation over the set *D*~*u*~ of metric pairs whose correlation is defined
(Equation (4)):

$$\bar\rho_u = \frac{1}{|D_u|}\sum_{(m,m')\in D_u} \rho_s\big(r_m, r_{m'}\big) \qquad (4)$$

where *r*~*m*~ is the explainers' rank vector under metric *m* and *ρ*~*s*~ the Spearman
correlation, computed as the Pearson correlation of the two rank vectors. A pair is undefined when
either rank vector is constant (all explainers tied); it is left out, never set to 0. Without
ties |*D*~*u*~| = 21; in the original analysis
18 pairs were undefined, in 3 of the 160 blocks. Kendall's
*W* with tie correction is reported beside it. Because the 20 blocks of a dataset are not
independent, the dataset was the unit of inference: the block values were averaged within each
dataset, and the estimate is the mean of the eight dataset means with a 95% *t*-interval. The null
hypothesis that the metrics rank the explainers independently was tested by a permutation test
that applied one permutation of the explainer labels per dataset and metric to all blocks of that
dataset (100,000 permutations, one-sided). A simulation run before the experiment showed that
permuting within blocks inflates false positives when blocks are correlated, and that a percentile
bootstrap over eight datasets undercovers.

**Within-metric stability benchmark (pre-unblinding).** For each dataset, model and metric, the
order of the studied explainers in each seed was compared with every other seed (ten seed pairs,
Spearman; undefined pairs left out), and the values were averaged over models and metrics within
each dataset. Seeds change the split, the model and the explainers' sampling, so the benchmark is
a reference level for between-metric agreement, not an upper bound.

**Instance level (H2).** The plan fixed the hypothesis (pairs of metrics correlate
positively across instances) and the estimate: for each block and explainer (all four), the
Spearman correlation across the 200 instances for each of the 15 pairs of M1 to M6, with metrics
oriented, averaged within the block and then within the dataset. Its inference was fixed after
the run and before unblinding: the *t*-interval over the eight dataset values, a one-sided
*t*-test of a positive mean (the test entering the Holm correction with H1), an exact sign-flip
test as a supplement, and Holm correction over the 15 pair tests.

**Decision rule.** The classification of Table 4 was fixed before the run; that it uses
the raw permutation *p* of H1, with the Holm-adjusted *p* over H1 and H2 reported beside it, was
fixed before unblinding. With three ranked explainers, if one explainer holds the same first or
last rank under every metric in a block, each pairwise correlation is 0.5 or 1, so the block's
agreement cannot fall below 0.5; the classification is therefore read with the distribution of
explainer positions.

Table: **Table 4.** Decision rule for H1, fixed before the run.

| Outcome of the permutation test and the 95% interval | Wording |
|------------------------------------|------------------------------------|
| *p* ≥ .05 | no evidence that the metrics share an order |
| *p* < .05, interval above 0.5 | the metrics broadly agree |
| *p* < .05, interval below 0.5 | the metrics agree only weakly |
| *p* < .05, interval contains 0.5 | agreement present, strength not determined |

::: {custom-style="Source"}
Source: Authors.
:::

**Secondary and sensitivity analyses.** Pre-specified: the share of blocks in which the
top-ranked explainer changes between two metrics (winner flips; ties at the top counted
separately); strict SHAP–LIME order reversals; the analysis with the random control as a fourth
explainer; M1, M2, M3 and M6 recomputed with the second baseline; and per-model summaries. Fixed
before unblinding: the analysis without M4 (six metrics), and an exploratory analysis that leaves
out the flagged M4 scores, which the primary analysis keeps as stored. A planned variance
decomposition was omitted because its specification was incomplete, a deviation from the plan.

**Synthetic check.** Four synthetic conditions used known functions directly as the model: an
additive logistic function and one with two pairwise interactions, each with eight standard normal
features, independent or correlated (pairwise correlation 0.5). Exact interventional Shapley
values of the predicted-class probability, with the expectation over 500 background rows of the
same distribution, served as true attributions [@rahnama2024; @islam2025]. For each condition and
seed, the explainers were ordered by their mean Spearman correlation with the truth (the reference
order), and each of M1 to M6 was scored by the Spearman correlation between its order of the
explainers and the reference order (statistic fixed before unblinding).

## 2.6. Supplementary experiments and exploratory diagnostics

A review of the original outputs found the LIME representation issue of Section 2.3 (the same
behaviour had been documented in an earlier study of the programme [@ownE]). The following
analyses were specified after that review, with their outputs written separately from the
original results, which were not modified; they carry no test decision.

**S3, synthetic validation of LIME representations.** In the synthetic conditions (numeric
features only), three representations of LIME were compared with the exact Shapley values
(instance-level Spearman correlation): the stored slopes; the contributions of LIME's fitted
surrogate relative to its training mean, *w*~*j*~(*x*~*j*~ − *μ*~*j*~)/*s*~*j*~; and LIME with
quartile discretisation; each at kernel width 3.0 and at the package default.

**S1, LIME as surrogate contributions on the real data.** LIME was re-explained with the frozen
configuration on the same instances, and its fitted surrogate was represented as the contribution
of each raw feature relative to a reference *r* (Equation (5)), oriented to the predicted
class:

$$c_j(r) = \sum_{k \in G_j} w_k\,\frac{x_k - r_k}{s_k} \qquad (5)$$

where *G*~*j*~ is the set of encoded columns of feature *j*, *w*~*k*~ the surrogate's coefficient on
standardised column *k*, and *s*~*k*~ the scale LIME fitted to that column. The two variants differ
only in *r*. In S1-B, the primary variant, *r* is the metrics' masking baseline *b*, so S1-B
contributions are relative to the same point as occlusion and the metrics (but not as SHAP); a
categorical feature at its training mode contributes 0. In S1-M, the sensitivity variant, *r* is
LIME's training mean *μ*, whose categorical coordinates are the dummy shares, a point off the
one-hot manifold. For numeric features *b* = *μ*, so the variants coincide. Both are contributions
of the surrogate, not of the model; for categorical features the surrogate was fitted to
off-manifold one-hot samples. Every instance was reconstructed and checked against the stored run
before use, and the metrics were recomputed on the S1 attributions; the analyses of Section 2.5
were then repeated with the S1 LIME rows substituted for the original ones and every other row
unchanged.

**Exploratory diagnostics.** The frequency with which each explainer holds each rank under each
metric (positions); the instance-level correlations adjusted for the predicted-class probability
by a rank-based partial correlation, because M1, M2, M3 and M6 contain *f(x)* by construction
(Equation (1), Equation (2)); the size of M7's removal sets and the frequency of identical sets
and tied scores; and the share of blocks in which every metric places the random control last.

## 2.7. Reproducibility

Code, configuration, per-instance scores and every analysis output are released under an open
licence (archive identifier withheld for double-blind review). All numbers in this article are
rendered by a script from the committed result files and re-derived by an automated check. The
remaining parameters, the seeds and the software versions are listed in Appendix A. The runs used one laptop (Intel Core i5-1335U CPU, Linux) with a
fixed software environment.

# 3. Results and discussion

## 3.1. Broad agreement under the original attribution representations (original analysis)

At system level, the mean pairwise Spearman correlation between metrics was
0.723 (95% CI [0.645,
0.802]) and Kendall's *W* 0.762
([0.701, 0.824]). The permutation test gave
*p* = .00001 (the smallest value attainable with
100,000 permutations), and *p* = .00002 after
Holm correction over H1 and H2. With the interval above 0.5, the frozen decision rule classifies
the result as "the metrics broadly agree", both before and after correction. **H1 is supported:**
the null hypothesis of independent rankings is rejected, and the agreement is broad. The within-metric
stability benchmark was 0.873
([0.826, 0.920]), so the
between-metric estimate was lower than the within-metric benchmark (no test compares them). Agreement was
lowest for random forests (0.637) and highest for logistic regression
(0.798). Leaving out the flagged M4 scores (exploratory) gave the same estimate
(0.723).

At instance level, agreement was weak: the mean correlation between metric pairs across instances
was 0.154 ([0.099, 0.209];
one-sided *t*-test *p* = .00016, sign-flip *p* = .0039, the smallest attainable with eight
datasets).
**H2 is supported, with a small effect:** the null hypothesis is rejected (inference fixed before
unblinding, Section 2.5), but the mean correlation is small, and the pairs differed in sign:
deletion and insertion correlated negatively (−0.351), as did
infidelity and sufficiency (−0.181), whereas deletion and
the top-*k* gap correlated most strongly (0.507; Figure 1).

These results are reported exactly as the frozen analysis produced them. They describe agreement among the metrics for the explainer outputs
*as stored*; as Section 2.3 explains, LIME's stored output was a
slope, while M1 to M6 read attributions as contributions. Sections 3.3 and 3.4 show what this
means for the result.

![**Figure 1.** Mean instance-level Spearman correlation between metric pairs over eight datasets (original representation): unadjusted (lower triangle, H2) and adjusted for the predicted-class probability (upper triangle, exploratory).](figures/fig_h2_matrix.png){width=65%}

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
(Figure 2). In these synthetic conditions, then, the same fitted surrogate tracked the true
attributions when read as a contribution and did not when read as slopes.

![**Figure 2.** Agreement of LIME representations with exact Shapley values in the synthetic conditions (mean over five seeds; bars at kernel width 3.0 with the range over seeds, diamonds at the package default width).](figures/fig_s3.png){width=85%}

::: {custom-style="Source"}
Source: Authors.
:::

## 3.4. Agreement with LIME represented as contributions (S1, supplementary)

With S1-B, system-level agreement fell from 0.723
to 0.529
([0.389,
0.669]), an interval that contains
0.5, and Kendall's *W* from 0.762 to
0.588 (Table 5). Agreement fell in seven of the eight
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
most 0.024 in any summary quantity, so the choice between the two references
did not change these descriptions. The within-metric stability benchmark also fell with S1-B,
from 0.873 to
0.797: rankings with LIME represented as
contributions were less stable across seeds, which may account for part of the fall in
between-metric agreement. The fall in between-metric agreement was more than twice as large,
however, which is consistent with metrics ordering the same explainers differently and not only
with noisier rankings. No decision rule is applied to S1; the H1 classification of
Section 3.1 stands for the representation it was made on.

Table: **Table 5.** System-level and instance-level agreement under the three LIME representations (mean over eight datasets with 95% *t*-interval; counts of the 160 blocks). Original column: ^O^ original analysis, ^S^ pre-specified sensitivity analysis, ^C^ exploratory; the S1 columns are supplementary.

| Quantity | Original (LIME slopes) | S1-B | S1-M |
|--------------------------------|------------------|------------------|------------------|
| H1-form agreement, mean pairwise Spearman^O^ | 0.723 [0.645, 0.802] | 0.529 [0.389, 0.669] | 0.540 [0.389, 0.692] |
| Kendall's *W*^O^ | 0.762 [0.701, 0.824] | 0.588 [0.473, 0.703] | 0.598 [0.471, 0.725] |
| Second masking baseline^S^ | 0.616 [0.546, 0.687] | 0.309 [0.219, 0.398] | 0.285 [0.212, 0.359] |
| Six metrics (M4 removed)^S^ | 0.690 [0.602, 0.777] | 0.483 [0.336, 0.629] | 0.489 [0.329, 0.649] |
| With the random control (four explainers)^S^ | 0.753 [0.700, 0.806] | 0.757 [0.689, 0.824] | 0.762 [0.689, 0.835] |
| Within-metric stability benchmark^O^ | 0.873 [0.826, 0.920] | 0.797 [0.727, 0.867] | 0.798 [0.724, 0.873] |
| H2-form instance-level agreement^O^ | 0.154 [0.099, 0.209] | 0.147 [0.095, 0.199] | 0.154 [0.097, 0.212] |
| H2-form, adjusted for *f(x)*^C^ | 0.233 [0.155, 0.312] | 0.225 [0.143, 0.306] | 0.235 [0.147, 0.323] |
| Blocks with one explainer at the same extreme rank under all seven metrics^C^ | 96 | 44 | 43 |
| ... LIME untied last under all seven metrics^C^ | 87 | 25 | 27 |
| Random control untied last under all seven metrics^C^ | 15 | 126 | 128 |
| Blocks with any strict SHAP–LIME reversal^S^ | 46 | 96 | 92 |
| Winner flips, pairs of M1–M6 (%)^S^ | 6.9–31.3 | 7.5–40.6 | 7.5–39.4 |
| Winner flips, pairs with M7 (%)^S^ | 49.4–63.8 | 49.4–62.5 | 46.3–59.4 |

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
(Figure 5). In each of those blocks every pairwise correlation is 0.5 or 1 by
construction (Section 2.5), so their contribution to the original estimate reflects agreement on
the last position at least. With S1-B, LIME was last
under all seven metrics in 25 blocks, and was last under M1
in 100 blocks; the order of the three explainers then varied
between metrics, and strict SHAP–LIME reversals between two of M1 to M6 occurred in
7.5% to 33.8% of blocks (original
0.0% to 1.9%); in pairs with M7, which uses only
magnitudes, they occurred in 26.9% to 28.8% of blocks originally and
30.0% to 37.5% with S1-B. Occlusion was ranked first
by M4 in all 160 blocks under both representations, as the
shared construction of M4 and occlusion predicts.

![**Figure 5.** Rank of each studied explainer under each metric over the 160 blocks, with LIME as stored (slopes, top) and as contributions relative to the masking baseline (S1-B, bottom).](figures/fig_positions.png){width=80%}

::: {custom-style="Source"}
Source: Authors.
:::

## 3.6. Instance-level agreement adjusted for the prediction (exploratory)

Adjusting the instance-level correlations for the predicted-class probability raised their mean
from 0.154 to 0.233
([0.155, 0.312]). The negative correlation
between deletion and insertion largely disappeared (0.094),
and insertion and sufficiency became strongly related (0.712;
Figure 1). By construction (Equation (1), Equation (2)), after orientation *f(x)* enters
M2 and M3 with a positive coefficient and M1 and M6 with a negative one; the pairs whose
correlation rose after adjustment include those with opposite coefficients. This is consistent
with a shared dependence on *f(x)* acting on these pairs, but the adjustment is a partial
correlation on the observed data and does not isolate that mechanism. Even adjusted, instance-level agreement remained far below system-level
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

The results bear on three conditions of faithfulness-metric agreement. Each statement below is
marked as a property of the computation, an observed association, or a possible mechanism that
the study did not isolate.

**Level of evaluation.** *Observed:* system-level agreement was
0.723 in the original analysis and
0.529 with S1-B, whereas the
mean instance-level correlation was 0.154 originally and
0.147 with S1-B, and some metric pairs correlated
negatively. *Property of the computation:* after orientation *f(x)* enters M2 and M3 with a positive
coefficient and M1 and M6 with a negative one, so their instance-level correlations depend
partly on how *f(x)* varies across instances; *observed:* adjusting for *f(x)* raised the mean to
0.233, still well below the system-level values. Agreement on how explainers rank on average therefore
did not carry over to agreement on individual explanations, the use made of explanations in
practice [@rawal2025; @bilodeau2024].

**Attribution semantics.** *Observed:* the original "broad agreement" was obtained with an
explainer whose output was a slope, scored by metrics that read contributions, and that
explainer was ranked last by each of M1, M2, M3, M4 and M6 in every block. *Property of the
computation:* in any block where one explainer is last under every metric, each pairwise
correlation is 0.5 or 1. *Observed:* with LIME represented as contributions of the same fitted
surrogate, LIME was no longer last in most blocks and agreement was
0.529, with an interval
containing 0.5; the within-metric stability benchmark also fell, but by less than half as much
(Section 3.4), so lower stability alone does not explain the change. *Possible mechanism, not isolated:* reading slopes as contributions lowered
LIME's scores under the contribution-based metrics, which is consistent with S3, where the slopes
were unrelated to exact Shapley values while the contributions tracked them; on the real data S1
changes the representation only, but no ground truth exists there. The study shows one case; it
does not establish how often representation mismatches arise for other explainers. It
complements the conceptual account of why faithfulness criteria disagree [@shanklin2026], and it
suggests that the reference point of each attribution deserves explicit reporting, since SHAP,
occlusion, S1-B and S1-M measure contributions from different points [@li2024; @sokol2025;
@knab2025].

**Evaluation protocol.** *Observed:* with S1-B, agreement was
0.309 under the second masking baseline, against
0.529 under the primary one,
consistent with reports that perturbation choices change validation outcomes [@simic2025;
@zheng2025; @ababneh2026]; the study did not compare the size of this change with that of other
protocol choices by a test. The retraining metric had the lowest within-metric stability and
tied often on datasets with few features; metric pairs flipped the winner in up to
40.6% of blocks even among M1 to M6 with S1-B; and M4 ranked first the
explainer that shares its construction. *Property of the computation:* with three explainers, one
consistently last explainer is enough to satisfy a 0.5 threshold, so aggregate agreement
statistics need the explainers' positions beside them [@duan2024; @edin2025].

**Recommendations.** Comparisons of explainers on tabular data should (1) declare what each
explainer's output represents and its reference point, and check it against what each metric
assumes; (2) report at least two metrics from different families and at least two masking
baselines; (3) include a random control and report how often it ranks last; (4) report a
within-metric stability benchmark and the explainers' rank positions next to any aggregate
agreement statistic; and (5) separate claims about rankings from claims about individual
explanations.

# 4. Conclusions

The study asked whether common faithfulness metrics agree on which explanations are more
faithful. For the eight datasets, four models and three explainers studied, the answer has two
parts. On the ranking of explainers, the metrics agreed broadly (H1 supported); on individual
explanations, they agreed only weakly (H2 supported, with a small effect). The ranking agreement
was not robust, however. It was obtained with an explainer whose output did not match what the
metrics assume. With LIME represented as surrogate contributions, in a supplementary analysis
that carries no test decision, agreement was moderate, its interval contained 0.5, and it fell
further under a second masking baseline, while instance-level agreement stayed weak. Whether the
metrics agree therefore depends on the level of evaluation, on what the attributions represent and
on the evaluation protocol, and a claim that one explainer is more faithful than another should
state all three. The study does not show whether the metrics agree for other explainers, tasks or
data types. Future work should extend the comparison to explainers with declared reference
semantics, to more masking schemes and to regression and multiclass tasks.

# Funding

This research received no external funding.

# Author contributions

Withheld for double-blind review; stated in CRediT terms at acceptance.

# Conflicts of interest

The author declares no conflicts of interest.

# Data availability statement

The datasets are public on OpenML (identifiers in Table 3). Code, configuration,
per-instance scores and all analysis outputs are openly available in an archived repository whose
persistent identifier is withheld for double-blind review and will be added at acceptance.

# Declaration of generative AI use

The author used the AI tool Claude (Anthropic), under the author's direction, to help write the
analysis code, edit the English text and format the references. The research question, the plan,
the design and the interpretation are the author's. The author reviewed all content and takes
full responsibility for it.

# Appendix A. Model parameters and software

Table 6 lists the settings not given in Section 2, the seeds and the software versions.

Table: **Table 6.** Parameters, seeds and software of the run (frozen configuration and run host record).

| Component | Setting |
|------------------|----------------------------------------------------------------|
| Seeds | 42, 123, 456, 789, 101112 |
| Preprocessing | Numeric features standardised; categorical features one-hot encoded, at most 20 levels (rarer levels grouped); missing values imputed |
| Logistic regression | L2 penalty, *C* = 1.0, at most 1,000 iterations |
| Random forest | 100 trees, other settings at the package defaults |
| XGBoost | 100 trees, maximum depth 4, learning rate 0.1 |
| Multilayer perceptron | One hidden layer of 100 units, at most 500 iterations |
| Software | Python 3.13.12; numpy 2.2.6, pandas 2.3.3, scipy 1.16.3, scikit-learn 1.7.1, xgboost 3.1.2, shap 0.50.0, lime 0.2.0.1 |

::: {custom-style="Source"}
Source: Authors.
:::
