# Response to the editor and the reviewers

Manuscript 2067810, *When Does SHAP Outperform LIME? Model- and Configuration-Dependent Results from a Paired Tabular Benchmark*, *Computers and Informatics*. Major revision of 2026-11-06.

Each comment is quoted in full, followed by the answer. Where one sentence of a reviewer raises several points, the sentence is quoted in full under each of them and the point answered there is shown in bold.




## Editor (Prof. Dr. Mehmet Tekerek)

### ED-1

> In addition, as an editorial requirement, please ensure that the main benchmark includes at least one state-of-the-art explainer comparison (e.g., Anchors or DiCE), or provide a clear justification if this is not feasible.

**Response.** We thank the editor for this requirement, which strengthened the study. Both Anchors and DiCE are now part of the main benchmark, under the same paired protocol as SHAP and LIME: the same models, the same test instances, the same seeds, the same metrics and the same host. The research questions are stated as paired contrasts of SHAP against each of the other three explainers (§3.1). Anchors and DiCE produce explanations of different kinds (a rule; a counterfactual), so §3.3 explains how each is turned into a feature-attribution vector and which metrics are comparable across the four methods. The four-explainer results are in Table 2 (§4.1) and across the seven datasets in Table 4 (§4.5). SHAP's faithfulness advantage holds against Anchors and DiCE as well as LIME (fidelity higher in all 25 Adult cells against each); Anchors is not distinguishable from SHAP on stability, and DiCE ranks last on every quality endpoint (§4.1).
**Changes in the manuscript:** Section 3.3; Section 4.1, Table 2


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Reviewer 1: general assessment

### R1-1

> In particular, **the authors should more clearly establish the novelty of the study relative to previously published work**, account for potential statistical dependencies among experimental configurations, and strengthen the validity of the perturbation-based stability evaluation.
>
> 4. Contribution to the Field: Fair (Provides marginal original contributions to the literature)

**Response.** We thank the reviewer for raising this point, which the revision takes seriously. The previous version presented the study as an extension of an earlier comparison; the revised manuscript stands on its own evidence. All results come from a new experimental cohort run for this study (§3), with four explainers instead of two, seven datasets instead of one main dataset, configuration sensitivity instead of a single setting, controls that test the validity of the stability measure, and cost measured on one host with hardware-independent counts. The contributions are restated in §1 accordingly, and §5 states in one paragraph what was known before and what this study adds. Details under R1-M1.
**Changes in the manuscript:** Section 1; Section 5

### R1-2

> In particular, the authors should more clearly establish the novelty of the study relative to previously published work, **account for potential statistical dependencies among experimental configurations**, and strengthen the validity of the perturbation-based stability evaluation.

**Response.** Addressed in detail under R1-M2 and R1-M3. In brief: the design no longer nests sample sizes, the seeds no longer change the data split, and the analysis models the remaining hierarchy explicitly (mixed model, cluster bootstrap over models).
**Changes in the manuscript:** Section 3.5

### R1-3

> In particular, the authors should more clearly establish the novelty of the study relative to previously published work, account for potential statistical dependencies among experimental configurations, and **strengthen the validity of the perturbation-based stability evaluation**.

**Response.** Addressed under R1-M6 and R1-M7: a no-noise control, perturbations that respect categorical constraints, rank-based stability, and an explicit treatment of all-zero vectors (§3.4, §4.4).
**Changes in the manuscript:** Section 3.4; Section 4.4

### R1-4

> Furthermore, **the fairness of the explainer configurations**, reliability of computational cost measurements, and generalizability of the cross-dataset findings require additional investigation.

**Response.** Addressed under R1-M4 and R1-M5: LIME now uses the library's default kernel width and is evaluated with and without its feature budget. KernelSHAP is also run on the tree models to separate the implementation from the model family. A sensitivity analysis covers the main hyperparameters of both methods (§3.3, §4.3).
**Changes in the manuscript:** Section 3.3

### R1-5

> Furthermore, the fairness of the explainer configurations, **reliability of computational cost measurements**, and generalizability of the cross-dataset findings require additional investigation.

**Response.** Addressed under R1-M8: every cost measurement was repeated on one recorded host under controlled conditions, and complemented by hardware-independent counts (§3.6, §4.2).
**Changes in the manuscript:** Section 3.6; Section 4.2, Table 3

### R1-6

> Furthermore, the fairness of the explainer configurations, reliability of computational cost measurements, and **generalizability of the cross-dataset findings** require additional investigation.

**Response.** Addressed under R1-M10: the cross-dataset study now covers six further datasets with all models and all four explainers, SHAP stability included. The datasets were chosen to separate dimensionality from categorical encoding (§3.2, §4.5).
**Changes in the manuscript:** Section 4.5, Table 4

### R1-7

> The statistical analysis and interpretation of effect sizes should also be strengthened.

**Response.** Addressed under R1-M3 and R1-M14.
**Changes in the manuscript:** Section 3.5; Section 4.1, Table 2

### R1-8

> 5. Organization of the manuscript: Poor

**Response.** We thank the reviewer for this assessment. As the comment concerns the manuscript as a whole, we reviewed every section against it and identified the following places where the organization could be improved: (1) Results mixed our evidence with a summary of an earlier study (former §4.1), which interrupted the line of argument; (2) the cross-dataset results, the kernel-width probe and the masking probe read as separate appendices of the main analysis; (3) limitations were spread over several sections; (4) Results had no element showing how the design fitted together. We revised each of them: the earlier-study section was removed (former Section 4.1); Results now follow one sequence, main benchmark → cost → configuration sensitivity → validity of the measurements → other datasets (§4); limitations are gathered in one subsection (§5); and a design table opens the methods (Table 1).
**Changes in the manuscript:** Section 1; former Section 4.1 (removed); Section 3.1 and Table 1 (design); Section 4 (one sequence: main benchmark, cost, configuration sensitivity, validity of the measurements, other datasets); Section 5.3 (limitations in one place)

### R1-9

> 6. Drawing and Building Upon Relevant Literature: Poor

**Response.** We thank the reviewer for this assessment. As the comment concerns the literature review as a whole, we checked it against recent work and identified the following places where it could be improved: (1) recent empirical comparisons of SHAP and LIME were missing; (2) recent benchmarks and toolkits for explanation evaluation were not discussed; (3) work on the sensitivity of LIME to its hyperparameters and on the validity of perturbation-based stability measures was not used. We revised each of them: §2 adds a paragraph on comparisons and benchmarks published from 2024 on, and positions the study against them. §1 and §2 cite the work on hyperparameter sensitivity and on the limits of perturbation-based measures that motivates the configuration sweep and the new controls, and §1 cites a recent reporting checklist for the computing environment behind the cost measurement. Older entries whose point is now made by recent work were replaced. Of the 52 references, the 26 that cite the literature are 85% from 2024 or later; the other 26 are cited for a definition (the explainers, the models and the metrics), a dataset source or a statistical method, at the place where it is used.
**Changes in the manuscript:** Section 1; Section 2

### R1-10

> I encourage the authors to address the major and minor comments comprehensively, provide additional experimental validation where necessary, and **ensure that the conclusions are fully supported by the reported evidence**.
>
> 9. Conclusion: Fair (Fair conclusion without sufficient justification from evidence presented)

**Response.** We thank the reviewer for this assessment. We re-examined each conclusion against the evidence and identified the following places where it was not sufficiently supported: (1) the stability conclusion rested on one kernel width and a perturbation scheme whose validity was not tested; (2) the sparsity conclusion was a consequence of LIME's feature budget; (3) the recommendations generalized beyond the models and datasets tested. We revised each of them: the stability conclusion now rests on the sensitivity analysis and the validity controls (§4.3–4.4); sparsity is reported descriptively (§3.1); every claim in §5 is labelled confirmatory or exploratory and bounded by what was tested (Table 5); and the conclusions (§6) restate only those results.
**Changes in the manuscript:** Section 5, Table 5; Section 6

### R1-11

> I encourage the authors to **address the major and minor comments comprehensively, provide additional experimental validation where necessary**, and ensure that the conclusions are fully supported by the reported evidence.

**Response.** Each major and minor comment of the detailed report is answered individually below.
**Changes in the manuscript:** 

## Reviewer 1: major comments

### R1-M1

> The manuscript extends a previously published SHAP–LIME comparison from 45 to 75 matched configurations. The authors should clearly establish the scientific novelty of the present work and distinguish its original contributions from previously reported findings.

**Response.** We agree that the previous version relied too much on the earlier study. The revision answers this in three ways. First, every result now comes from a new cohort designed and run for this study, on one host, with four explainers and seven datasets; no number is taken from the earlier work, which was replaced because an audit found training-test overlap, an unrecoverable model and timings from mixed hosts (§3.1). Second, the analysis asks a different question: not whether SHAP is better on average, but when the ordering of the methods depends on the model, the configuration and the measurement protocol. That calls for configuration sensitivity (§4.3) and validity controls (§4.4) that the earlier study did not have. Third, cost is reported in hardware-independent terms (model calls, complexity) next to time on one host. §1 states these contributions; §5 positions them against earlier work. The new finding is that SHAP's advantage lies in faithfulness, not in stability: on Adult its stability advantage over LIME is not significant, and on all six further datasets LIME with the full vector is the more stable explainer while SHAP keeps the highest fidelity (§4.1, §4.5).
**Changes in the manuscript:** Section 1; former Section 4.1; Section 5; Section 3.1

### R1-M2

> The statistical independence of the 75 matched configurations requires further justification. The authors should address potential dependencies arising from shared datasets, model configurations, random seeds, and sampling intensities and assess their implications for statistical inference.

**Response.** We thank the reviewer for this important comment. On re-examining the design we found the dependencies the reviewer points to. The three sampling intensities were nested (the smaller samples were subsets of the larger), and all cells of a model family shared one trained model. The revised design removes the nesting: there is one sample size, and seeds vary only the instance draw and the explainers' randomness, over one fixed split (§3.1–3.2, Table 1). The remaining dependency, cells sharing a model, is modelled explicitly (R1-M3). The number of independent units at each level is stated in Table 1.
**Changes in the manuscript:** Section 3.1, Table 1; Section 3.2; Section 3.5

### R1-M3

> The authors should demonstrate the robustness of the reported statistical significance and confidence intervals using an analytical approach that accounts for the hierarchical structure of the experimental design.

**Response.** As suggested, the inference now accounts for the structure of the design. For each endpoint and contrast we fit a linear mixed model with random intercepts for model and for seed within model. A cluster bootstrap over models gives confidence intervals, and the number of models in which each difference has the same sign is reported. The exact sign test at the model level is also given; with five models it cannot go below p = 0.0625, and the text says so. The cell-level Wilcoxon test is kept as a description (§3.5, Table 2). The hierarchical analysis makes two conclusions more cautious. A cell-level Wilcoxon test, as in the earlier version, would declare SHAP more stable than LIME and its faithfulness gap larger than that of Anchors (p < 0.001 for both); the mixed model, which accounts for the variation between models, does not (Holm-adjusted p = 0.25 for both). The cluster bootstrap agrees with the mixed model except for the faithfulness gap against Anchors, where its interval excludes zero. Every other conclusion is the same under all three analyses, and the model-level signs agree in direction for all nine quality contrasts (five of five models for seven, four of five for stability against LIME and Anchors).
**Changes in the manuscript:** Section 3.5

### R1-M4

> The fairness of the SHAP–LIME comparison requires further investigation. In particular, the fixed feature budget imposed on LIME and the use of different SHAP implementations may influence the reported differences in sparsity, fidelity, and computational efficiency.

**Response.** We agree that both choices could shape the differences. (1) LIME is now run both with its 10-feature budget and without it (all features). The comparison of sparsity, fidelity and cost is reported for both (§3.3, Table 2). (2) To separate the SHAP implementation from the model family, KernelSHAP is also run on the two tree models, next to TreeSHAP (§4.3). Without the budget, LIME's vector covers every feature and its fidelity and stability change as reported in Table 2. KernelSHAP on the tree ensembles is within 0.02 of TreeSHAP on fidelity and stability, so the quality differences between model families do not come from the TreeSHAP implementation (§4.3). In cost, however, the implementation matters: KernelSHAP on the tree ensembles takes 7 (random forest) and 73 (XGBoost) times TreeSHAP's time (§4.3).
**Changes in the manuscript:** Section 3.3; Section 4.3, Fig. 1

### R1-M5

> Additional sensitivity analyses are needed to determine whether the observed performance differences remain consistent across alternative LIME and SHAP hyperparameter configurations, rather than reflecting the particular settings selected for the benchmark.

**Response.** A sensitivity analysis now covers LIME's kernel width and number of samples and KernelSHAP's number of samples and background size, on all models, three seeds, and a common set of valid instances. For each pair of methods, the text states whether the sign of the difference holds over the whole grid, and where it changes (§4.3, Fig. 1). On Adult, kernel widths of 0.75 to 5 give degenerate explanations (all-zero explanations or all-zero perturbed vectors) and are reported as such. On the remaining configurations, SHAP's fidelity exceeds LIME's in every pair of configurations on all five models. The stability ordering changes with LIME's configuration: LIME's stability rises from 0.34 (default width, 250 samples) to 0.98 (width 15, 5,000 samples), and at the upper end LIME is more stable than every SHAP configuration on every model except the random forest (§4.3, Fig. 1).
**Changes in the manuscript:** Section 4.3, Fig. 1

### R1-M6

> The application of Gaussian perturbations to one-hot-encoded categorical features may generate unrealistic observations. The authors should evaluate whether the reported stability results remain valid under perturbation strategies that preserve categorical constraints and relevant feature dependencies.

**Response.** We agree that Gaussian noise on one-hot columns creates observations that cannot occur. The stability analysis now compares the original scheme with one that preserves the constraints. Noise is added to numeric features only, and each categorical feature is resampled with a small probability from its training distribution, so every perturbed observation is a valid row (§3.4, §4.4). With valid perturbations, LIME with the full vector is more stable than SHAP on all five models and in all 15 model-seed cells, whereas under the original Gaussian noise SHAP was ahead. The stability ordering of SHAP and LIME on Adult therefore depends on whether the perturbed rows can occur, and the text now says so (§4.4, §5, Conclusions, Abstract). SHAP stays more stable than Anchors and DiCE under both schemes.
**Changes in the manuscript:** Section 4.4

### R1-M7

> The exceptionally low LIME stability observed on the Adult dataset may be influenced by the perturbation protocol and kernel-width configuration. The authors should investigate these effects more systematically before attributing the observed differences primarily to the explanation methods.

**Response.** We investigated both factors systematically and found a third. The analysis now varies the kernel width (R1-M5) and the perturbation scheme (R1-M6), and adds a control without input noise. That control measures how much of LIME's instability comes from its own random sampling rather than from the input change. On examining the code we also found that an all-zero explanation entered the cosine similarity as 0. It is now counted, and stability is reported with and without such vectors (§3.4, §4.4). Without input noise, LIME's repeated explanations are almost identical (stability 0.98 to 0.99 with ten features): its own sampling accounts for 8% of its instability under the original protocol (22% with all features), so most of it is its response to the perturbation, and in particular to perturbations that create impossible one-hot rows (R1-M6). Excluding all-zero vectors raises LIME's stability by 0.01 to 0.08 and changes no ordering (§4.1, §4.4). The kernel width and the number of samples explain most of the rest: at the default width and 1,000 samples LIME's stability is 0.53 on the sweep instances, at a width of 15 it is 0.90, and with 5,000 samples as well 0.98 (§4.3).
**Changes in the manuscript:** Section 4.4

### R1-M8

> The computational cost comparisons are potentially confounded by heterogeneous execution environments. The authors should validate the principal latency findings using standardized hardware, software configurations, and repeated timing measurements.

**Response.** Every cost measurement was repeated on a single recorded host. The host's processor, memory, operating system and software versions are reported. Each explanation was timed in one process, single-threaded and pinned to one core, after a warm-up, three times. The explainers alternated per instance, so slow drift affected all of them equally. Timing paused whenever other activity on the host exceeded a threshold. The cost comparison is tested in wall-clock time, which on one pinned core of a quiet host measures the explainer's work at sub-millisecond resolution; CPU time, which Windows advances only in 15.6 ms steps, is reported alongside (§3.6). The paired cells of the earlier version ran on different hosts; that problem no longer arises. On this host, KernelSHAP takes 3 to 25 times LIME's wall time, TreeSHAP less than LIME on XGBoost and about as much on the random forest (on the six further datasets, less or more depending on the dataset), and SHAP less than Anchors in every cell; the difference from LIME is not significant after Holm correction (§4.2, Tables 2 and 3).
**Changes in the manuscript:** Section 3.6; Section 4.2, Table 3

### R1-M9

> The reported reversal in runtime performance between XGBoost and random forests represents an important finding. However, additional controlled experiments are necessary to determine whether this behavior consistently reflects model architecture rather than implementation-specific or hardware-dependent effects.

**Response.** We agree this needed a controlled test, and §4.2 now poses the reversal the reviewer identified as the question the controlled run answers. Random forests and gradient-boosted trees were trained on the same data at matched numbers of trees and depths. The cost of TreeSHAP and of LIME was measured on one host with each ensemble at its own depth and at the other's (§4.2; supplementary file, S9). The reversal follows tree size more than the implementation: lowering the random forest from depth 15 to 6 cuts TreeSHAP's time from 21.7 to 3.2 ms, and raising XGBoost from depth 6 to 15 raises it from 1.4 to 7.4 ms, against 12.5 to 21.6 ms for LIME. At matched depth XGBoost remains 2.3 to 2.9 times cheaper, a smaller effect of the implementation. The total number of leaves, which the plan named, was not recorded; depth is the controlled variable.
**Changes in the manuscript:** Section 4.2

### R1-M10

> The cross-dataset analysis does not include SHAP stability measurements. The authors should extend the evaluation to both explainers on the additional datasets or explicitly restrict their generalizability claims to the outcomes directly supported by the experiments.

**Response.** SHAP stability is now measured on every dataset, with all models and all four explainers, so the cross-dataset comparison is symmetric (§4.5, Table 4).
**Changes in the manuscript:** Section 4.5, Table 4

### R1-M11

> The kernel-width sensitivity analysis is restricted to a single model and random seed. Additional experiments across multiple seeds and model families are necessary to establish the robustness of the reported stability–fidelity trade-off.

**Response.** The kernel-width analysis now covers all five models and three seeds (§4.3).
**Changes in the manuscript:** Section 4.3, Fig. 1

### R1-M12

> The kernel-width experiments contain different numbers of valid explanations across configurations. The authors should address the potential influence of this variation on the comparative results and consider evaluating the metrics on a common set of valid instances.

**Response.** We thank the reviewer for spotting this. Every configuration is now compared on the common set of instances for which all configurations gave a valid explanation. The share of degenerate explanations of each configuration is reported as an outcome in its own right (§4.3).
**Changes in the manuscript:** Section 3.4; Section 4.3, Fig. 1

### R1-M13

> The masking sensitivity analysis is limited to a small subset of random-forest experiments. The authors should investigate whether the reported SHAP advantages in fidelity and faithfulness persist across alternative masking strategies and additional model families.

**Response.** The four masking schemes are now applied to all models and datasets of the main benchmark, not only to random forests (§4.4). Under all four schemes, SHAP's faithfulness gap exceeds that of every other explainer on every Adult model, except against LIME on XGBoost, where the difference is close to zero. On the six further datasets SHAP is ahead in 460 of 480 combinations of model, explainer and scheme; most exceptions are Anchors on Connect-4, which is ahead of SHAP on three of five models under every scheme, as under the main protocol (§4.4).
**Changes in the manuscript:** Section 4.4

### R1-M14

> The reported effect sizes, particularly the exceptionally large values for fidelity and stability, require further statistical justification. The authors should clarify their computation, examine the distributions of paired differences, and assess their robustness to potential dependence among configurations.

**Response.** We agree that the very large d_z values needed explanation. §3.5 now defines d_z (mean paired difference over the standard deviation of the differences) and explains why it grows when paired differences vary little, as here. Robust effect sizes are reported next to it: the Hodges–Lehmann difference and the matched rank-biserial correlation. Effect sizes are also given at the model level, which is robust to the dependence between cells. The supplement shows the distribution of the paired differences per endpoint and model, as quantiles and as Figure S1, with the variance components of each mixed model (§4.1; Supplement S8).
**Changes in the manuscript:** Section 3.5; Section 4.1, Table 2

### R1-M15

> The practical recommendations regarding explainer selection appear broader than the experimental evidence supports. The authors should strengthen the empirical justification for these recommendations or explicitly restrict them to the evaluated models, datasets, configurations, and computational settings.

**Response.** The recommendations are now restricted to the models, datasets, configurations and host tested. §5 opens with a table that states, for each claim, the evidence, the condition and whether it is confirmatory or exploratory (Table 5).
**Changes in the manuscript:** Section 5, Table 5

## Reviewer 1: minor comments

### R1-m1

> The abstract should clearly distinguish findings obtained from the primary Adult benchmark from those derived from the supplementary cross-dataset and sensitivity experiments.

**Response.** The abstract now reports the primary benchmark first and then, marked as exploratory, the configuration, validity and cross-dataset results.
**Changes in the manuscript:** Abstract

### R1-m2

> The mathematical notation and directional hypotheses associated with RQ1–RQ4 should be presented more explicitly and consistently.

**Response.** The research questions now share one notation: the paired difference Δ = SHAP − X for each explainer X and endpoint. The direction of each hypothesis is stated explicitly. Sparsity is a descriptive question (R2-4) (§3.1).
**Changes in the manuscript:** Section 3.1

### R1-m3

> The experimental design should be summarized in a dedicated table specifying model families, random seeds, sampling intensities, and the number of matched configurations.

**Response.** Added: Table 1 lists datasets, models, explainers and variants, seeds, instances per stratum, the stability subset and the number of paired cells.
**Changes in the manuscript:** Section 3.1, Table 1

### R1-m4

> Additional details concerning model hyperparameters, preprocessing procedures, training and testing partitions, and evaluation instance selection should be provided to improve reproducibility.

**Response.** §3.2 states the split (80/20, stratified, fixed), the preprocessing (one-hot encoding and standardization, fitted on the training split) and the selection of instances. The supplement lists every model's hyperparameters.
**Changes in the manuscript:** Section 3.2

### R1-m5

> The procedure used to sample instances from the TP, TN, FP, and FN strata should be clarified, including whether evaluation instances overlap across configurations.

**Response.** §3.2 now describes the sampling. Instances are drawn per confusion-matrix stratum from the test split only, with a fixed number per stratum, and every explainer explains the same instances. When a stratum has fewer instances, all are taken, and realized counts are reported. Draws for different seeds are independent. All seeds sample from the same fixed test split, so where a stratum is small they can share instances (in the smallest strata, all of them); this overlap is measured and reported.
**Changes in the manuscript:** Section 3.2

### R1-m6

> The stability metric description should specify how zero-valued attribution vectors and undefined cosine similarity values were handled.

**Response.** §3.4 states the convention. An all-zero attribution vector gives a cosine of 0 in the original definition. Such vectors are now counted, and stability is reported with and without them.
**Changes in the manuscript:** Section 3.4

### R1-m7

> The fidelity calculation should explicitly define the treatment of attribution signs, feature-removal effects, and undefined correlation coefficients.

**Response.** §3.4 now states that fidelity correlates absolute attributions with absolute prediction changes, so signs are not used. Each feature is removed by replacing it with its training mean. When either vector is constant, the correlation is undefined: it is set to 0, and such cases are counted and reported.
**Changes in the manuscript:** Section 3.4

### R1-m8

> Table 1 should present the statistical estimates, confidence intervals, adjusted p-values, and effect sizes using consistent notation and clearly defined column headings.

**Response.** The main results table now uses one notation, with each column defined in the caption: estimate, 95% CI, Holm-adjusted p, d_z, Hodges–Lehmann difference, rank-biserial r.
**Changes in the manuscript:** Section 4.1, Table 2

### R1-m9

> The qualitative reproducibility classifications in Table 2 should be supported by predefined criteria or replaced with appropriately qualified numerical interpretations.

**Response.** The table and its labels were removed. Variability across seeds is now reported as a variance component of the mixed model, with no qualitative label.
**Changes in the manuscript:** former Section 4.3

### R1-m10

> Figures 1 and 2 should be improved in terms of axis labeling, statistical notation, scale descriptions, and overall readability.

**Response.** Every figure was regenerated, with labelled axes and units, the scale stated, intervals defined in the caption, and a size readable in print.
**Changes in the manuscript:** Figures

### R1-m11

> Tables 4 and 5 should include measures of variability or uncertainty alongside the reported three-seed averages.

**Response.** The cross-dataset table reports the mean over seeds, and its caption states the largest standard deviation over seeds (below 0.04 in every cell); the standard deviation of every cell, per model, is in the supplementary file (S12).
**Changes in the manuscript:** Section 4.5, Table 4

### R1-m12

> The methodological relevance of including Anchors in the cross-dataset analysis should be clarified in relation to the manuscript's primary SHAP–LIME research questions.

**Response.** We thank the reviewer. Anchors, and DiCE too, are now part of the main benchmark at the editor's request (ED-1), on every dataset. §3.3 now states their role: the research questions remain about SHAP and LIME, and Anchors (a rule) and DiCE (a counterfactual) are reference explainers of other kinds, which show whether a SHAP–LIME difference is specific to the pair or shared by explainers in general.
**Changes in the manuscript:** Section 3.3; Section 4.5, Table 4

### R1-m13

> The grouped masking procedure should be described in greater detail, particularly regarding the identification and treatment of correlated or related features.

**Response.** §4.4 now describes how related features were identified and how a group is masked. A group is (1) all one-hot columns of one categorical input variable, and (2) on Adult, the categorical education and its numeric code education-num, merged into one group because they encode the same information. When any feature of a group is among the top-k features, the whole group is replaced by its training means.


**Changes in the manuscript:** Section 4.4

### R1-m14

> The reproducibility section should provide additional information about computational parallelism, execution settings, and the availability of scripts used to reproduce the statistical analyses.

**Response.** §3.6 states that the quality measurements ran in parallel worker processes, which does not affect them, and that every timing ran alone under the conditions of R1-M8. The analysis scripts and every result file are in the public repository and archive, whose addresses are withheld during review.
**Changes in the manuscript:** Section 3.6

### R1-m15

> The discussion and conclusion should more clearly distinguish findings supported by the complete paired benchmark from exploratory observations derived from restricted experimental settings.

**Response.** Each result is labelled confirmatory (the main paired benchmark) or exploratory (sensitivity, validity controls, other datasets) in §4, in Table 5 and in the conclusions.
**Changes in the manuscript:** Section 5, Table 5; Section 6; Abstract


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Reviewer 2

### R2-1a

> First, the runtime comparisons measured in milliseconds are methodologically invalid because the experiments were distributed across commodity workstations running different operating systems without recording hardware specifications, and paired cells were not executed on identical hardware hosts. **To resolve this, runtime evaluations must be conducted on a single, isolated hardware environment**, and supplementary complexity metrics—such as theoretical time complexity, black-box model prediction calls, and FLOPs—should be reported to make the efficiency claims hardware-agnostic.

**Response.** We agree with the reviewer, and the earlier timings have been replaced. All cost measurements of the revision come from one recorded host, under the controlled protocol described under R1-M8 (§3.6). Every paired comparison ran on that host in the same session.
**Changes in the manuscript:** Section 1; Section 3.6; Section 4.2, Table 3

### R2-1b

> First, the runtime comparisons measured in milliseconds are methodologically invalid because the experiments were distributed across commodity workstations running different operating systems without recording hardware specifications, and paired cells were not executed on identical hardware hosts. To resolve this, runtime evaluations must be conducted on a single, isolated hardware environment, and **supplementary complexity metrics—such as theoretical time complexity, black-box model prediction calls, and FLOPs—should be reported to make the efficiency claims hardware-agnostic**.

**Response.** Next to time, the revision reports for each explanation the number of calls to the model and the number of rows the model evaluated. These counts do not depend on the hardware. Table 3 adds the theoretical complexity of each explainer. FLOPs are reported for logistic regression and the MLP, where they are well defined per prediction. For tree ensembles and the RBF-SVM a per-prediction FLOP count is not comparable across model types, so model calls and rows evaluated are the hardware-independent measure there (§4.2). On Adult, a KernelSHAP explanation evaluates 25,001 rows against 1,000 for LIME, which is 5.5 against 0.22 MFLOPs for logistic regression and 555 against 22 for the MLP.
**Changes in the manuscript:** Section 4.2, Table 3

### R2-2

> Second, evaluating both explainers at a single static hyperparameter configuration fails to capture the inherent trade-offs between stability, fidelity, and computational cost; therefore, the revision must include multi-objective Pareto optimal frontiers across varying sampling budgets and kernel widths.

**Response.** As requested, the revision evaluates both explainers over a grid of sampling budgets and kernel widths (LIME), and sampling budgets and background sizes (KernelSHAP). For each model it reports the Pareto-optimal configurations for stability and fidelity (§4.3, Fig. 1), and the cost of every configuration on the same host (§4.3; supplementary file, S10). On the random forest, TreeSHAP dominates every LIME configuration. On the other four models neither method dominates: the front joins SHAP at the fidelity end with LIME at a wide kernel width at the stability end (Fig. 1).
**Changes in the manuscript:** Section 4.3, Fig. 1

### R2-3

> Third, the claim regarding LIME's near-zero stability on the Adult dataset is confounded by an improper hyperparameter choice, as the reference kernel width of 3.0 is severely restricted for a 103-dimensional one-hot-encoded feature space, leading to an artificial collapse of local neighborhood weights.

**Response.** We agree. The reference LIME configuration is now the library's default kernel width, 0.75√M. We also correct a figure the reviewer quotes: the Adult feature space has 108 transformed features, not 103 as the earlier text stated, so the default width is about 7.79. The value 3.0 remains one point of the sensitivity analysis, where its effect is shown (§4.3): at a width of 3.0, every perturbed explanation on Adult is all-zero, which confirms the collapse the reviewer describes, and widths of 0.75 to 5 are reported as degenerate. Widths of 10 and 15 are valid and raise LIME's stability up to 0.98 (§4.3, Fig. 1). At the default width, LIME's stability on Adult is 0.56 with the full vector and 0.33 with the 10-feature budget, against 0.74 for SHAP; the difference between SHAP and LIME with the full vector is not significant (§4.1).
**Changes in the manuscript:** Section 3.3; Section 4.3, Fig. 1

### R2-4

> Fourth, the hypothesis test for sparsity is statistically tautological since LIME's active-feature count is constrained by a hard code-level ceiling, making it mathematically inevitable to yield sparser explanations than unconstrained SHAP.

**Response.** We agree. With a 10-feature budget, LIME's sparsity follows from its configuration, and testing it as a hypothesis was not meaningful. The revision removes the sparsity hypothesis test (§3.1). Sparsity is reported descriptively and for LIME without the budget, together with measures that do not depend on a ceiling: the share of attribution mass in the top-k features and the normalized entropy (§4.1).
**Changes in the manuscript:** Section 3.1

### R2-5

> Fifth, in the cross-dataset extension, SHAP's stability was omitted without justification, leaving the multi-dataset validation incomplete and asymmetric.

**Response.** Corrected: SHAP stability is now measured on every dataset (R1-M10).
**Changes in the manuscript:** Section 4.5, Table 4

### R2-6

> Sixth, the manuscript heavily relies on and reuses pre-computed execution cohorts and findings from reference [10], to the extent that basic summary statistics are omitted from the tables and redirected to the previous paper; the manuscript must become entirely self-contained and independently verifiable.

**Response.** We agree, and the revision is self-contained. All results come from a new cohort run for this study. Every table reports the per-method levels it compares, and no number is taken from or referred to [10], which is now cited only for the definitions of the metrics (§3.4). An earlier analysis of the SHAP–LIME question was replaced in full: an audit found that in most of its cells the evaluation instances overlapped the training partition, that one model could not be recovered and that its timings mixed hosts. §3.1 states this in one sentence, and no number from that analysis is used.
**Changes in the manuscript:** former Section 4.1; Section 4.1, Table 2; Section 5; Section 3.1

### R2-7

> Finally, the indirect disclosure of author identities through self-referencing requires careful scrubbing to maintain double-blind review integrity.

**Response.** We thank the reviewer. The author names in the text and the framing that tied this study to the earlier one were removed. The earlier study is cited in the third person, like any other source, and only for definitions. The file properties were cleared of personal data.
**Changes in the manuscript:** former Section 4.1; Section 3, everywhere; Build

### R2-8

> Statement of the Problem or Purpose: Poor; Relevance and importance of the Topic: Fair (Marginally relevant to the mission and purpose of the journal); Contribution to the Field: Poor (Does not provide original contributions to the literature)

**Response.** We thank the reviewer for this assessment. As it concerns the framing of the manuscript as a whole, we re-examined the introduction and identified the following places where it could be improved: (1) the introduction opened on the popularity of the methods instead of the decision a practitioner has to make; (2) the gap was stated relative to an earlier study instead of the literature; (3) the relevance to computing practice (cost, deployment) was implicit. We revised each of them: §1 now opens with the decision problem (which explainer, for which model, under which latency and stability budget). It states the gap against recent comparisons (§2), and it presents three contributions, including cost in hardware-independent terms, a computing concern central to the journal. The new evidence behind the contributions is summarized under R1-M1.
**Changes in the manuscript:** Section 1 (decision problem, gap, three contributions); Section 2