# Paper G — First draft (version 0.1, 2026-11-13)

> **Status of this file.** A scaffold for the author to review and rewrite. It contains no
> result: every number to come from the run is written `[R: …]`. It contains no reference:
> every citation is `[REF-n]`, described in the list at the end, to be filled only with
> sources found and checked with their DOI (reference rule: DOI URL for each, at least 80%
> from 2024 or later). The assistant writes the full text; the author decides what is in or
> out and owns the journal's AI-content limit (decision of 2026-11-13). Impersonal voice throughout.
> Target: *Informática y Sistemas*, 10 to 12 pages, APA 7.

**Title options**

1. *Do Faithfulness Metrics Agree? Metric-Dependent Rankings of Post-hoc Explanations on Tabular Data*
2. *Which Explainer Is More Faithful Depends on How Faithfulness Is Measured*
3. *Agreement Between Faithfulness Metrics for Feature-Attribution Explanations: A Paired Tabular Study*

---

## Abstract (target 150–250 words; currently ~200)

Comparisons of post-hoc explanation methods often conclude that one method is more faithful
to the model than another. Such conclusions rest on a faithfulness metric, and several metrics
exist that operationalise faithfulness differently. This study measures whether these metrics
agree. Four attribution methods (SHAP, LIME, occlusion, and a random control) were applied to
three classifiers (logistic regression, random forest, and XGBoost) trained on eight public
binary tabular datasets, with five seeds and 200 test instances per condition. Each explanation
was scored by six faithfulness metrics: deletion and insertion curves, top-k prediction gap,
faithfulness correlation, infidelity, and sufficiency. Agreement was assessed at two levels:
the order of the explainers within each dataset and model, and the scores of individual
explanations across instances. All metrics placed the random control last in [R: share] of
conditions. Among the three studied explainers, the mean rank correlation between metrics was
[R: value] (95% CI [R: interval]), against a within-metric ceiling across seeds of [R: value].
The explainer ranked first changed with the metric in [R: share] of conditions, and the order
of SHAP and LIME reversed under a change of metric in [R: share]. At the instance level, metric
pairs correlated [R: range]. [R: one-sentence conclusion following the decision rule]. Reports
of explainer faithfulness should therefore state the metric, the masking baseline, and, where
possible, results under more than one metric.

**Keywords:** explainable artificial intelligence; faithfulness; evaluation metrics; feature attribution; tabular data

---

## 1. Introduction

Post-hoc explanation methods such as SHAP and LIME are widely used to inspect the predictions
of machine-learning models on tabular data, including in credit, health and public-sector
applications [REF-1, REF-2]. Because these methods can produce different explanations for the
same prediction, their evaluation has become a research area of its own [REF-3, REF-4]. Among
the properties evaluated, *faithfulness* — the degree to which an explanation reflects the
reasoning of the model it explains — is usually treated as the most important [REF-4, REF-5].

Faithfulness cannot be observed directly. It is estimated by perturbing the input according
to the explanation and observing the response of the model. Many such estimators have been
proposed: removing features in order of importance (deletion), adding them back from a
baseline (insertion), masking the top features, correlating attributions with single-feature
removal, comparing attributions with the response to random perturbations (infidelity), and
keeping only the top features (sufficiency) [REF-6, REF-7, REF-8]. Each encodes a different
notion of what it means for an explanation to be faithful, and each depends on choices such
as the masking baseline [REF-9].

Benchmarks, however, typically report one of these metrics, or a few without examining how
they relate [REF-10, REF-11]. If the metrics disagree, the statement "method A is more faithful
than method B" is partly a statement about the metric. Recent work has raised this concern
[REF-12, REF-13], and work in image and text domains suggests that metric agreement can be low
[REF-14]. For tabular data, where most applied use of SHAP and LIME occurs, there is less
systematic evidence of how the common metrics relate across datasets and models.

Earlier studies in the same research programme found that the advantage of one explainer over
another depends on the model and configuration [REF-OWN-B], that SHAP and LIME often disagree
on which features matter for an instance [REF-OWN-E], and that explainer rankings vary across
datasets [REF-OWN-F]. *(Double-blind: cite in third person; check that no result of these
papers is restated.)* The present study asks a prior question: whether the measuring
instrument itself gives a consistent answer.

The study contributes:

1. A paired measurement of agreement between six faithfulness metrics on the same
   explanations, at the level of explainer rankings and at the level of individual instances.
2. A within-metric ceiling (agreement of a metric with itself across seeds) against which
   between-metric agreement is interpreted.
3. An estimate of how often the explainer judged most faithful, and the order of SHAP and LIME,
   changes with the choice of metric and of masking baseline.
4. Reporting recommendations for faithfulness claims, with code and data released.

Section 2 reviews related work. Section 3 describes the materials and methods. Section 4
reports the results, Section 5 discusses them, and Section 6 concludes.

## 2. Related work

### 2.1 Faithfulness metrics for feature attribution

*[Describe each metric family, its origin and its assumptions. Deletion and insertion
[REF-6]; masking top-k and comprehensiveness/sufficiency [REF-7]; faithfulness correlation
[REF-15]; infidelity [REF-8]; retraining-based evaluation (ROAR) [REF-16]. Keep to 1–2 sentences
each; most foundational sources are older, so this is where the 20% of pre-2024 references go.]*

### 2.2 Evaluation frameworks and benchmarks

*[Toolkits and benchmarks that bundle these metrics (e.g. libraries and benchmark suites
[REF-10, REF-11, REF-17]). Point: they report several metrics side by side but rarely analyse
agreement between them.]*

### 2.3 Disagreement in explanation evaluation

*[The disagreement problem between explainers [REF-18]; studies of metric reliability and
agreement, mostly in vision or NLP [REF-12, REF-13, REF-14]; the effect of out-of-distribution
masking and baselines [REF-9]. End with the gap: a paired, multi-dataset tabular study with a
within-metric ceiling.]*

## 3. Materials and methods

### 3.1 Design overview

The design is fully paired: the same instances are explained by every explainer, and the same
explanations are scored by every metric. The factors are 8 datasets × 3 models × 4 explainers
× 6 metrics, with 5 seeds and 200 test instances per dataset, model and seed. Figure 1 shows
the pipeline. *[Figure 1: pipeline diagram, generated by a committed script.]*

### 3.2 Datasets

Eight public binary classification datasets were taken from OpenML [REF-19], two from each of
four strata of feature composition and size (Table 1). A dataset was retained if the
cross-validated AUC of at least two of the three models lay between 0.65 and 0.98, so that
models were neither near chance nor near perfect. The list was fixed before any explanation
was computed.

*[Table 1: dataset, OpenML ID, version, rows, raw features, encoded features, share numeric,
minority-class share, CV AUC per model. Values from `outputs/analysis/paper_g/datasets.csv`.]*

### 3.3 Models

Logistic regression with L2 penalty, random forest and XGBoost [REF-20] were trained with one
configuration for all datasets, recorded before training. Numeric features were standardised,
categorical features one-hot encoded, and missing values imputed with the median or mode. Each
seed fixed a stratified 80/20 split, the model, explainer sampling and the random control.

### 3.4 Explainers

- **SHAP** [REF-21]: TreeSHAP for the tree models, KernelSHAP for logistic regression.
- **LIME** [REF-22] for tabular data, with its default kernel.
- **Occlusion:** the attribution of a feature is the drop in predicted-class probability when
  that feature alone is replaced by its baseline value.
- **Random control:** attributions drawn from a standard normal distribution with a fixed seed.

Attributions for one-hot encoded columns were summed per raw feature. All explainers
explained the predicted class.

### 3.5 Faithfulness metrics

Let *f(x)* be the predicted-class probability, *a* the attribution vector over *d* raw
features, and *b* the baseline (training mean for numeric features, mode for categorical
features). Masking a feature sets it to its baseline value.

- **M1, deletion AUC.** Features are masked one at a time in decreasing order of |*a*|; the
  area under *f* against the share of masked features. Lower is better.
- **M2, insertion AUC.** Starting from *b*, features are restored in the same order; the area
  under *f*. Higher is better.
- **M3, top-k prediction gap.** *f(x) − f(x′)*, where *x′* masks the top 20% of features (at
  least one). Higher is better.
- **M4, faithfulness correlation.** Pearson correlation between *a_i* and the drop in *f* when
  feature *i* alone is masked. Higher is better.
- **M5, infidelity** [REF-8]. The expected squared difference between *Iᵀa* and
  *f(x) − f(x − I)* for Gaussian perturbations *I*. Lower is better.
- **M6, sufficiency.** *f(x) − f(x″)*, where *x″* keeps only the top 20% of features and
  masks the rest. Lower is better.

*[Equations (1)–(6), numbered and cited in the text by generated reference (author rule).]*

Metrics were oriented so that a higher score always means more faithful before ranking. As a
sensitivity check, M1, M2, M3 and M6 were recomputed with a second baseline: a random training
row instead of the mean.

M4 and occlusion are built on the same single-feature masking, so M4 is expected to favour
occlusion. Results are therefore also reported without that combination.

### 3.6 Agreement analysis

**System level (H1).** In each dataset × model × seed block, the explainers were ranked under
each metric by their mean score over the 200 instances. With metrics as raters and explainers
as items, agreement was measured by Kendall's *W* and by the mean pairwise Spearman correlation
between metrics, *(mW − 1)/(m − 1)* [REF-23]. The 95% interval was obtained by percentile
bootstrap over datasets (10,000 draws). The null hypothesis that metrics rank the explainers
independently was tested by permuting ranks within each metric and block (100,000
permutations, one-sided). The primary estimate uses the three studied explainers; the random
control is reported separately as a check.

**Ceiling.** The agreement of each metric with itself across the five seeds, averaged over
datasets and models, bounds what agreement between metrics can reach given sampling noise.

**Instance level (H2).** For each dataset, model, explainer and seed, the Spearman correlation
across the 200 instances was computed for every pair of metrics, and summarised by its mean over
datasets with a bootstrap interval over datasets.

**Secondary measures.** The share of blocks in which the top-ranked explainer changes between
two metrics; the share in which the order of SHAP and LIME reverses; variance shares of the
ranks attributable to metric, dataset, model and their interactions (linear mixed model with
dataset as a random factor; aligned rank transform as a sensitivity analysis [REF-24]).

**Decision rule.** Fixed before the run (Table 2). Holm correction was applied over H1 and H2.

*[Table 2: decision rule for H1, as in ANALYSIS_PLAN.md section 4.4.]*

### 3.7 Reproducibility

Code, configuration and per-instance scores are released under an open licence [Zenodo DOI,
anonymised for review]. Runs were made on a single laptop CPU [R: hardware, total time].

## 4. Results

### 4.1 Models and sanity check

*[Model AUCs per dataset (summary; full values in Table 1). Share of conditions in which every
metric placed the random control last: [R]. Any metric that failed this check is named here.]*

### 4.2 System-level agreement (H1)

*[Mean pairwise Spearman between metrics: [R] (95% CI [R]); permutation p = [R]. Within-metric
ceiling: [R]. Decision-rule wording: [R]. Figure 2: heat map of the 6 × 6 between-metric rank
correlation, studied explainers only. Figure 3: per-dataset agreement against the ceiling.]*

### 4.3 How often the conclusion changes

*[Winner flips between metric pairs (Table 3). SHAP–LIME order reversal: [R] of blocks. Which
metric pairs disagree most.]*

### 4.4 Instance-level agreement (H2)

*[Figure 4: matrix of mean instance-level Spearman correlations between metrics, with intervals.
Which metrics cluster together (e.g. deletion-type against correlation-type).]*

### 4.5 Sources of disagreement

*[Variance shares; per-model results; effect of the second baseline; with and without the
occlusion–M4 combination.]*

## 5. Discussion

*[To be written after the results. Planned points, to be kept or dropped depending on the
outcome:]*

- **What the agreement level means for published comparisons.** If agreement is weak, a single
  metric supports only a claim about that metric.
- **Families of metrics.** Whether removal-based metrics (M1, M3, M6) agree with each other more
  than with correlation-based ones (M4, M5), which would indicate that they measure different
  constructs rather than noisy versions of one.
- **The baseline as a hidden factor.** How much of the disagreement the masking baseline
  explains, and the out-of-distribution problem of masking [REF-9].
- **Recommendations for reporting:** state the metric and baseline; report at least two metrics
  from different families; include a random control; report a within-metric ceiling.
- **Relation to earlier work** of the programme [REF-OWN-E, REF-OWN-F]: explainers disagree
  with each other, rankings vary across datasets, and — this study — the instrument that ranks
  them is not neutral either. *(No values from those papers.)*

### 5.1 Limitations

- Eight datasets, all binary and tabular; three model families, no neural networks.
- Four explainers, which makes rank orders coarse; the instance-level analysis compensates in part.
- No ground truth of faithfulness: the study measures agreement, not correctness.
- One configuration per explainer and per model; one masking fraction (20%) for M3 and M6.
- Retraining-based evaluation (ROAR) [is / is not] included [R: per pilot].

## 6. Conclusions

*[Two or three conclusions, each tied to H1, H2 or the winner-flip analysis, using the wording
of the decision rule. No new claims.]*

---

## Declarations (required by the journal)

**Funding.** [Author to state.]
**Author contributions.** [Single author: conceptualisation, methodology, software, analysis,
writing.]
**Conflicts of interest.** None declared. [Author to confirm.]
**Data availability.** Code, configuration and per-instance results: [Zenodo DOI, after review].
Datasets: OpenML, identifiers in Table 1.
**Declaration of generative AI use.** [Author to state precisely, e.g.: an AI assistant was used
to draft a structural scaffold of the manuscript, to write and test analysis code under the
author's direction, and to check references; the author rewrote the text, verified all results
and references, and takes full responsibility for the content.]

---

## References to find and verify (placeholders)

Each must be found, read, and recorded with its DOI URL in `reference_records.json`. At least
80% of the final list must date from 2024 or later. Do not fill from memory.

| ID | What it must support | Era to look for |
|---|---|---|
| REF-1 | Applied use of SHAP/LIME on tabular data in high-stakes domains | 2024+ |
| REF-2 | Survey of XAI for tabular data | 2024+ |
| REF-3 | Survey of XAI evaluation | 2024+ |
| REF-4 | Faithfulness as a central evaluation property; definition | 2024+ |
| REF-5 | Faithfulness/fidelity terminology review | 2024+ |
| REF-6 | Origin of deletion/insertion curves | foundational (pre-2024 allowed) |
| REF-7 | Origin of comprehensiveness/sufficiency | foundational |
| REF-8 | Origin of infidelity | foundational |
| REF-9 | Masking baselines / out-of-distribution effect on perturbation metrics | 2024+ |
| REF-10 | XAI benchmark toolkit reporting several faithfulness metrics | 2024+ |
| REF-11 | Tabular XAI benchmark | 2024+ |
| REF-12 | Concern that faithfulness metrics are unreliable or inconsistent | 2024+ |
| REF-13 | Study of agreement or reliability of evaluation metrics | 2024+ |
| REF-14 | Metric disagreement in vision or NLP | 2024+ |
| REF-15 | Origin of faithfulness correlation | foundational |
| REF-16 | Origin of ROAR | foundational |
| REF-17 | Another benchmark/library (e.g. recent evaluation suite) | 2024+ |
| REF-18 | The disagreement problem between explainers | 2024+ preferred |
| REF-19 | OpenML | 2024+ version if one exists |
| REF-20 | XGBoost | foundational |
| REF-21 | SHAP | foundational |
| REF-22 | LIME | foundational |
| REF-23 | Kendall's W / rank agreement methodology | 2024+ applied source preferred |
| REF-24 | Aligned rank transform | foundational |
| REF-OWN-B, -E, -F | Earlier papers of the programme (B at C&I under review; E at AAIR under review; F at JCSI accepted) | cite only as permitted; check status at submission |

Foundational sources number about 9 of about 25–30, so at least 20 recent sources are needed to
stay above 80%. Extra recent sources (2024–2026) should be found for sections 2.2 and 2.3.
