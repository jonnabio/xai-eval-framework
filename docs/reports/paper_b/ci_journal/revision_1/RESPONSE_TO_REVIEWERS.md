# Response to the editor and the reviewers

Manuscript 2067810, *When Does SHAP Outperform LIME? Model- and Configuration-Dependent Results from a Paired Tabular Benchmark*, *Computers and Informatics*. Major revision of 2026-11-06.

<!-- RESPONSE GUIDELINES (author, 2026-11-06)
1. Every item gets an answer that moves the review forward: never a question back to the
   reviewer or the editor.
2. GENERAL comments (marked "- **Type:** GENERAL" below: an assessment or a rating without a
   pointer to specific passages). Answer politely; note, without complaint, that the comment
   is general; then name AT LEAST ONE concrete place the authors identified against it, and
   state that it was revised. Pattern:
     "We thank the reviewer for this assessment. As the comment concerns the manuscript as a
      whole, we reviewed every section against it and identified the following places where
      <aspect> could be improved: (1) <section/table: what was weak>, ... We revised each of
      them: <what changed>."
   Each named place must be a real change, listed in CHANGELOG.md and in Changes / Where.
3. "Where" is the location of OUR change in the revised manuscript (section, table, figure,
   page). It is rendered as "Changes in the manuscript:", a statement, not a question.
-->
<!-- TRACKING FORMAT (read by scripts/check_revision.py; the lines marked [internal]
are removed when the letter is rendered for the journal):
  - **Status:** PENDING | REMEDIATED | EXPLAINED            [internal]
  - **Changes:** C-### ids from CHANGELOG.md                [internal]
  - **Plan:** work package of REVISION_PLAN.md              [internal]
  - **Type:** GENERAL, for an assessment without specific pointers  [internal]
  - **Response:** the answer, written for the reviewer
  - **Where:** section, table or figure of the revised manuscript
A REMEDIATED item needs Changes and Where; an EXPLAINED item needs a Response. -->

## Editor (Prof. Dr. Mehmet Tekerek)

### ED-1

> In addition, as an editorial requirement, please ensure that the main benchmark includes at least one state-of-the-art explainer comparison (e.g., Anchors or DiCE), or provide a clear justification if this is not feasible.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-008, C-012
- **Plan:** WP2, WP3
- **Response:** We thank the editor for this requirement, which strengthened the study. Both Anchors and DiCE are now part of the main benchmark, under the same paired protocol as SHAP and LIME: the same models, the same test instances, the same seeds, the same metrics and the same host. The research questions are stated as paired contrasts of SHAP against each of the other three explainers (§3.1). Anchors and DiCE produce explanations of different kinds (a rule; a counterfactual), so §3.3 explains how each is turned into a feature-attribution vector and which metrics are comparable across the four methods. The four-explainer results are in Table 2 (§4.1) and across the seven datasets in Table 4 (§4.5). [R: one sentence on the main finding for Anchors and DiCE.]
- **Where:** Section 3.3; Section 4.1, Table 2

### ED-2

> Please submit your revised manuscript and a point-by-point response letter.

- **Status:** EXPLAINED
- **Changes:** 
- **Plan:** WP9
- **Response:** This letter answers every point of the editor and both reviewers individually, quoting each comment and stating where the manuscript changed. A second copy of the manuscript with every change marked is provided.
- **Where:** 

### ED-3

> If you need additional time, please contact the editorial office before the deadline.

- **Status:** EXPLAINED
- **Changes:** 
- **Plan:** Q-1
- **Response:** The revision is submitted within the deadline of 30 November 2026.
- **Where:** 

## Reviewer 1: general assessment

### R1-1

> In particular, the authors should more clearly establish the novelty of the study relative to previously published work [...] (Contribution to the Field: Fair)

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-001, C-020
- **Plan:** WP1, WP2, WP7
- **Response:** We thank the reviewer for raising this point, which the revision takes seriously. The previous version presented the study as an extension of an earlier comparison; the revised manuscript stands on its own evidence. All results come from a new experimental cohort run for this study (§3), with four explainers instead of two, seven datasets instead of one main dataset, configuration sensitivity instead of a single setting, controls that test the validity of the stability measure, and cost measured on one host with hardware-independent counts. The contributions are restated in §1 accordingly, and §5 states in one paragraph what was known before and what this study adds. Details under R1-M1.
- **Where:** Section 1; Section 5

### R1-2

> [...] account for potential statistical dependencies among experimental configurations [...]

- **Status:** REMEDIATED
- **Changes:** C-011
- **Plan:** WP6
- **Response:** Addressed in detail under R1-M2 and R1-M3. In brief: the design no longer nests sample sizes, the seeds no longer change the data split, and the analysis models the remaining hierarchy explicitly (mixed model, cluster bootstrap over models).
- **Where:** Section 3.5

### R1-3

> [...] and strengthen the validity of the perturbation-based stability evaluation.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-009, C-018
- **Plan:** WP4
- **Response:** Addressed under R1-M6 and R1-M7: a no-noise control, perturbations that respect categorical constraints, rank-based stability, and an explicit treatment of all-zero vectors (§3.4, §4.4).
- **Where:** Section 3.4; Section 4.4

### R1-4

> Furthermore, the fairness of the explainer configurations [...] require[s] additional investigation.

- **Status:** REMEDIATED
- **Changes:** C-008
- **Plan:** WP2, WP5
- **Response:** Addressed under R1-M4 and R1-M5: LIME now uses the library's default kernel width and is evaluated with and without its feature budget. KernelSHAP is also run on the tree models to separate the implementation from the model family. A sensitivity analysis covers the main hyperparameters of both methods (§3.3, §4.3).
- **Where:** Section 3.3

### R1-5

> [...] reliability of computational cost measurements [...] require[s] additional investigation.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-010, C-014
- **Plan:** WP2
- **Response:** Addressed under R1-M8: every cost measurement was repeated on one recorded host under controlled conditions, and complemented by hardware-independent counts (§3.6, §4.2).
- **Where:** Section 3.6; Section 4.2, Table 3

### R1-6

> [...] and generalizability of the cross-dataset findings require additional investigation.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-017
- **Plan:** WP3
- **Response:** Addressed under R1-M10: the cross-dataset study now covers six further datasets with all models and all four explainers, SHAP stability included. The datasets were chosen to separate dimensionality from categorical encoding (§3.2, §4.5).
- **Where:** Section 4.5, Table 4

### R1-7

> The statistical analysis and interpretation of effect sizes should also be strengthened.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-011, C-012
- **Plan:** WP6
- **Response:** Addressed under R1-M3 and R1-M14.
- **Where:** Section 3.5; Section 4.1, Table 2

### R1-8

> Organization of the manuscript: Poor (Poor organization of ideas and supporting points)

- **Type:** GENERAL
- **Status:** REMEDIATED
- **Changes:** C-001, C-003, C-006, C-012, C-016, C-018
- **Plan:** WP7
- **Response:** We thank the reviewer for this assessment. As the comment concerns the manuscript as a whole, we reviewed every section against it and identified the following places where the organization could be improved: (1) Results mixed our evidence with a summary of an earlier study (former §4.1), which interrupted the line of argument; (2) the cross-dataset results, the kernel-width probe and the masking probe read as separate appendices of the main analysis; (3) limitations were spread over several sections; (4) Results had no element showing how the design fitted together. We revised each of them: the earlier-study section was removed (former Section 4.1); Results now follow one sequence, main benchmark → cost → configuration sensitivity → validity of the measurements → other datasets (§4); limitations are gathered in one subsection (§5); and a design table opens the methods (Table 1).
- **Where:** Section 1; former Section 4.1 (removed); Section 3.1 and Table 1 (design); Section 4 (one sequence: main benchmark, cost, configuration sensitivity, validity of the measurements, other datasets); Section 5.3 (limitations in one place)

### R1-9

> Drawing and Building Upon Relevant Literature: Poor (Provides a poor summary of the major points in the relevant literature)

- **Type:** GENERAL
- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-002
- **Plan:** WP8, D-6
- **Response:** We thank the reviewer for this assessment. As the comment concerns the literature review as a whole, we checked it against recent work and identified the following places where it could be improved: (1) recent empirical comparisons of SHAP and LIME were missing; (2) recent benchmarks and toolkits for explanation evaluation were not discussed; (3) work on the sensitivity of LIME to its hyperparameters and on the validity of perturbation-based stability measures was not used. We revised each of them: §2 adds a paragraph on comparisons and benchmarks published from 2024 on, and positions the study against them. §3.3–3.4 cite the work on hyperparameter sensitivity and perturbation validity that motivates the new controls. [R: number of references, share from 2024 on.]
- **Where:** Section 2

### R1-10

> [...] ensure that the conclusions are fully supported by the reported evidence. (Conclusion: Fair conclusion without sufficient justification from evidence presented)

- **Type:** GENERAL
- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-019, C-021
- **Plan:** WP7
- **Response:** We thank the reviewer for this assessment. We re-examined each conclusion against the evidence and identified the following places where it was not sufficiently supported: (1) the stability conclusion rested on one kernel width and a perturbation scheme whose validity was not tested; (2) the sparsity conclusion was a consequence of LIME's feature budget; (3) the recommendations generalized beyond the models and datasets tested. We revised each of them: the stability conclusion now rests on the sensitivity analysis and the validity controls (§4.3–4.4); sparsity is reported descriptively (§3.1); every claim in §5 is labelled confirmatory or exploratory and bounded by what was tested (Table 5); and the conclusions (§6) restate only those results.
- **Where:** Section 5, Table 5; Section 6

### R1-11

> I encourage the authors to address the major and minor comments comprehensively, provide additional experimental validation where necessary [...]

- **Status:** EXPLAINED
- **Changes:** 
- **Plan:** §2b
- **Response:** Each major and minor comment of the detailed report is answered individually below.
- **Where:** 

## Reviewer 1: major comments

### R1-M1

> The manuscript extends a previously published SHAP–LIME comparison from 45 to 75 matched configurations. The authors should clearly establish the scientific novelty of the present work and distinguish its original contributions from previously reported findings.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-001, C-003, C-020, C-025
- **Plan:** WP1, WP7
- **Response:** We agree that the previous version relied too much on the earlier study. The revision answers this in three ways. First, every result now comes from a new cohort designed and run for this study, on one host, with four explainers and seven datasets; no number is taken from the earlier work. Second, the analysis asks a different question: not whether SHAP is better on average, but when the ordering of the methods depends on the model, the configuration and the measurement protocol. That calls for configuration sensitivity (§4.3) and validity controls (§4.4) that the earlier study did not have. Third, cost is reported in hardware-independent terms (model calls, complexity) next to time on one host. §1 states these contributions; §5 positions them against earlier work. [R: one sentence on the finding that is new.]
- **Where:** Section 1; former Section 4.1; Section 5; Section 3.1

### R1-M2

> The statistical independence of the 75 matched configurations requires further justification. The authors should address potential dependencies arising from shared datasets, model configurations, random seeds, and sampling intensities and assess their implications for statistical inference.

- **Status:** REMEDIATED
- **Changes:** C-006, C-007, C-011
- **Plan:** WP6
- **Response:** We thank the reviewer for this important comment. On re-examining the design we found the dependencies the reviewer points to. The three sampling intensities were nested (the smaller samples were subsets of the larger), and all cells of a model family shared one trained model. The revised design removes the nesting: there is one sample size, and seeds vary only the instance draw and the explainers' randomness, over one fixed split (§3.1–3.2, Table 1). The remaining dependency, cells sharing a model, is modelled explicitly (R1-M3). The number of independent units at each level is stated in Table 1.
- **Where:** Section 3.1, Table 1; Section 3.2; Section 3.5

### R1-M3

> The authors should demonstrate the robustness of the reported statistical significance and confidence intervals using an analytical approach that accounts for the hierarchical structure of the experimental design.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-011
- **Plan:** WP6
- **Response:** As suggested, the inference now accounts for the structure of the design. For each endpoint and contrast we fit a linear mixed model with random intercepts for model and for seed within model. A cluster bootstrap over models gives confidence intervals, and the number of models in which each difference has the same sign is reported. The exact sign test at the model level is also given; with five models it cannot go below p = 0.0625, and the text says so. The cell-level Wilcoxon test is kept as a description (§3.5, Table 2). [R: whether conclusions change under the hierarchical analysis.]
- **Where:** Section 3.5

### R1-M4

> The fairness of the SHAP–LIME comparison requires further investigation. In particular, the fixed feature budget imposed on LIME and the use of different SHAP implementations may influence the reported differences in sparsity, fidelity, and computational efficiency.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-008, C-016
- **Plan:** WP5
- **Response:** We agree that both choices could shape the differences. (1) LIME is now run both with its 10-feature budget and without it (all features). The comparison of sparsity, fidelity and cost is reported for both (§3.3, Table 2). (2) To separate the SHAP implementation from the model family, KernelSHAP is also run on the two tree models, next to TreeSHAP (§4.3). [R: what changes with each.]
- **Where:** Section 3.3; Section 4.3, Fig. 1

### R1-M5

> Additional sensitivity analyses are needed to determine whether the observed performance differences remain consistent across alternative LIME and SHAP hyperparameter configurations, rather than reflecting the particular settings selected for the benchmark.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-016
- **Plan:** WP5
- **Response:** A sensitivity analysis now covers LIME's kernel width and number of samples and KernelSHAP's number of samples and background size, on all models, three seeds, and a common set of valid instances. For each pair of methods, the text states whether the sign of the difference holds over the whole grid, and where it changes (§4.3, Fig. 1). [R]
- **Where:** Section 4.3, Fig. 1

### R1-M6

> The application of Gaussian perturbations to one-hot-encoded categorical features may generate unrealistic observations. The authors should evaluate whether the reported stability results remain valid under perturbation strategies that preserve categorical constraints and relevant feature dependencies.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-018
- **Plan:** WP4
- **Response:** We agree that Gaussian noise on one-hot columns creates observations that cannot occur. The stability analysis now compares the original scheme with one that preserves the constraints. Noise is added to numeric features only, and each categorical feature is resampled with a small probability from its training distribution, so every perturbed observation is a valid row (§3.4, §4.4). [R]
- **Where:** Section 4.4

### R1-M7

> The exceptionally low LIME stability observed on the Adult dataset may be influenced by the perturbation protocol and kernel-width configuration. The authors should investigate these effects more systematically before attributing the observed differences primarily to the explanation methods.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-018
- **Plan:** WP4, WP5
- **Response:** We investigated both factors systematically and found a third. The analysis now varies the kernel width (R1-M5) and the perturbation scheme (R1-M6), and adds a control without input noise. That control measures how much of LIME's instability comes from its own random sampling rather than from the input change. On examining the code we also found that an all-zero explanation entered the cosine similarity as 0. It is now counted, and stability is reported with and without such vectors (§3.4, §4.4). [R: which factor explains how much.]
- **Where:** Section 4.4

### R1-M8

> The computational cost comparisons are potentially confounded by heterogeneous execution environments. The authors should validate the principal latency findings using standardized hardware, software configurations, and repeated timing measurements.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-010, C-014
- **Plan:** WP2
- **Response:** Every cost measurement was repeated on a single recorded host. The host's processor, memory, operating system and software versions are reported. Each explanation was timed in one process, single-threaded and pinned to one core, after a warm-up, three times. The explainers alternated per instance, so slow drift affected all of them equally. Timing paused whenever other activity on the host exceeded a threshold (§3.6). The paired cells of the earlier version ran on different hosts; that problem no longer arises.
- **Where:** Section 3.6; Section 4.2, Table 3

### R1-M9

> The reported reversal in runtime performance between XGBoost and random forests represents an important finding. However, additional controlled experiments are necessary to determine whether this behavior consistently reflects model architecture rather than implementation-specific or hardware-dependent effects.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-015
- **Plan:** WP2b
- **Response:** We agree this needed a controlled test. Random forests and gradient-boosted trees were trained on the same data at matched numbers of trees and depths. The cost of TreeSHAP and of LIME was measured on one host against the total number of leaves (§4.2). [R: whether the reversal follows tree size, i.e. architecture, or persists at matched size, i.e. implementation.]
- **Where:** Section 4.2

### R1-M10

> The cross-dataset analysis does not include SHAP stability measurements. The authors should extend the evaluation to both explainers on the additional datasets or explicitly restrict their generalizability claims to the outcomes directly supported by the experiments.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-017
- **Plan:** WP3
- **Response:** SHAP stability is now measured on every dataset, with all models and all four explainers, so the cross-dataset comparison is symmetric (§4.5, Table 4).
- **Where:** Section 4.5, Table 4

### R1-M11

> The kernel-width sensitivity analysis is restricted to a single model and random seed. Additional experiments across multiple seeds and model families are necessary to establish the robustness of the reported stability–fidelity trade-off.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-016
- **Plan:** WP5
- **Response:** The kernel-width analysis now covers all five models and three seeds (§4.3).
- **Where:** Section 4.3, Fig. 1

### R1-M12

> The kernel-width experiments contain different numbers of valid explanations across configurations. The authors should address the potential influence of this variation on the comparative results and consider evaluating the metrics on a common set of valid instances.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-016
- **Plan:** WP5
- **Response:** We thank the reviewer for spotting this. Every configuration is now compared on the common set of instances for which all configurations gave a valid explanation. The share of degenerate explanations of each configuration is reported as an outcome in its own right (§4.3).
- **Where:** Section 4.3, Fig. 1

### R1-M13

> The masking sensitivity analysis is limited to a small subset of random-forest experiments. The authors should investigate whether the reported SHAP advantages in fidelity and faithfulness persist across alternative masking strategies and additional model families.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-018
- **Plan:** WP4b
- **Response:** The four masking schemes are now applied to all models and datasets of the main benchmark, not only to random forests (§4.4). [R]
- **Where:** Section 4.4

### R1-M14

> The reported effect sizes, particularly the exceptionally large values for fidelity and stability, require further statistical justification. The authors should clarify their computation, examine the distributions of paired differences, and assess their robustness to potential dependence among configurations.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-011, C-012
- **Plan:** WP6
- **Response:** We agree that the very large d_z values needed explanation. §3.5 now defines d_z (mean paired difference over the standard deviation of the differences) and explains why it grows when paired differences vary little, as here. Robust effect sizes are reported next to it: the Hodges–Lehmann difference and the matched rank-biserial correlation. Effect sizes are also given at the model level, which is robust to the dependence between cells. The supplement shows the distribution of the paired differences per endpoint and model (§4.1). [R]
- **Where:** Section 3.5; Section 4.1, Table 2

### R1-M15

> The practical recommendations regarding explainer selection appear broader than the experimental evidence supports. The authors should strengthen the empirical justification for these recommendations or explicitly restrict them to the evaluated models, datasets, configurations, and computational settings.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-019
- **Plan:** WP7
- **Response:** The recommendations are now restricted to the models, datasets, configurations and host tested. §5 opens with a table that states, for each claim, the evidence, the condition and whether it is confirmatory or exploratory (Table 5).
- **Where:** Section 5, Table 5

## Reviewer 1: minor comments

### R1-m1

> The abstract should clearly distinguish findings obtained from the primary Adult benchmark from those derived from the supplementary cross-dataset and sensitivity experiments.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-022
- **Plan:** WP7
- **Response:** The abstract now reports the primary benchmark first and then, marked as supplementary, the configuration, validity and cross-dataset results.
- **Where:** Abstract

### R1-m2

> The mathematical notation and directional hypotheses associated with RQ1–RQ4 should be presented more explicitly and consistently.

- **Status:** REMEDIATED
- **Changes:** C-005
- **Plan:** WP7
- **Response:** The research questions now share one notation: the paired difference Δ = SHAP − X for each explainer X and endpoint. The direction of each hypothesis is stated explicitly. Sparsity is a descriptive question (R2-4) (§3.1).
- **Where:** Section 3.1

### R1-m3

> The experimental design should be summarized in a dedicated table specifying model families, random seeds, sampling intensities, and the number of matched configurations.

- **Status:** REMEDIATED
- **Changes:** C-006
- **Plan:** WP7
- **Response:** Added: Table 1 lists datasets, models, explainers and variants, seeds, instances per stratum, the stability subset and the number of paired cells.
- **Where:** Section 3.1, Table 1

### R1-m4

> Additional details concerning model hyperparameters, preprocessing procedures, training and testing partitions, and evaluation instance selection should be provided to improve reproducibility.

- **Status:** REMEDIATED
- **Changes:** C-007
- **Plan:** WP7
- **Response:** §3.2 states the split (80/20, stratified, fixed), the preprocessing (one-hot encoding and standardization, fitted on the training split) and the selection of instances. The supplement lists every model's hyperparameters.
- **Where:** Section 3.2

### R1-m5

> The procedure used to sample instances from the TP, TN, FP, and FN strata should be clarified, including whether evaluation instances overlap across configurations.

- **Status:** REMEDIATED
- **Changes:** C-007
- **Plan:** WP0, WP6
- **Response:** §3.2 now describes the sampling. Instances are drawn per confusion-matrix stratum from the test split only, with a fixed number per stratum, and every explainer explains the same instances. When a stratum has fewer instances, all are taken, and realized counts are reported. Draws for different seeds are independent. All seeds sample from the same fixed test split, so where a stratum is small they can share instances (in the smallest strata, all of them); this overlap is measured and reported.
- **Where:** Section 3.2

### R1-m6

> The stability metric description should specify how zero-valued attribution vectors and undefined cosine similarity values were handled.

- **Status:** REMEDIATED
- **Changes:** C-009
- **Plan:** WP0, WP4
- **Response:** §3.4 states the convention. An all-zero attribution vector gives a cosine of 0 in the original definition. Such vectors are now counted, and stability is reported with and without them.
- **Where:** Section 3.4

### R1-m7

> The fidelity calculation should explicitly define the treatment of attribution signs, feature-removal effects, and undefined correlation coefficients.

- **Status:** REMEDIATED
- **Changes:** C-009
- **Plan:** WP0, WP7
- **Response:** §3.4 now states that fidelity correlates absolute attributions with absolute prediction changes, so signs are not used. Each feature is removed by replacing it with its training mean. When either vector is constant, the correlation is undefined: it is set to 0, and such cases are counted and reported.
- **Where:** Section 3.4

### R1-m8

> Table 1 should present the statistical estimates, confidence intervals, adjusted p-values, and effect sizes using consistent notation and clearly defined column headings.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-012
- **Plan:** WP7
- **Response:** The main results table now uses one notation, with each column defined in the caption: estimate, 95% CI, Holm-adjusted p, d_z, Hodges–Lehmann difference, rank-biserial r.
- **Where:** Section 4.1, Table 2

### R1-m9

> The qualitative reproducibility classifications in Table 2 should be supported by predefined criteria or replaced with appropriately qualified numerical interpretations.

- **Status:** REMEDIATED
- **Changes:** C-013
- **Plan:** WP7
- **Response:** The table and its labels were removed. Variability across seeds is now reported as a variance component of the mixed model, with no qualitative label.
- **Where:** former Section 4.3

### R1-m10

> Figures 1 and 2 should be improved in terms of axis labeling, statistical notation, scale descriptions, and overall readability.

- **Status:** PENDING (old figures removed; the new figure is generated from the results of cohort B2)
- **Changes:** C-023
- **Plan:** WP7
- **Response:** Every figure was regenerated, with labelled axes and units, the scale stated, intervals defined in the caption, and a size readable in print.
- **Where:** Figures

### R1-m11

> Tables 4 and 5 should include measures of variability or uncertainty alongside the reported three-seed averages.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-017
- **Plan:** WP3
- **Response:** The cross-dataset table now reports mean ± standard deviation over seeds.
- **Where:** Section 4.5, Table 4

### R1-m12

> The methodological relevance of including Anchors in the cross-dataset analysis should be clarified in relation to the manuscript's primary SHAP–LIME research questions.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-008, C-017
- **Plan:** WP7
- **Response:** Anchors, and DiCE too, are now part of the main benchmark at the editor's request (ED-1). §3.3 states their role: reference explainers of other kinds (a rule, a counterfactual), against which the SHAP–LIME differences can be read.
- **Where:** Section 3.3; Section 4.5, Table 4

### R1-m13

> The grouped masking procedure should be described in greater detail, particularly regarding the identification and treatment of correlated or related features.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-018
- **Plan:** WP4b, WP7
- **Response:** §4.4 now describes how related features were identified (the one-hot columns of one categorical variable, and pairs that encode the same information, such as education and education-num [R: rule to be read from the masking script and stated exactly]) and how a group is masked (all its columns replaced together).
- **Where:** Section 4.4

### R1-m14

> The reproducibility section should provide additional information about computational parallelism, execution settings, and the availability of scripts used to reproduce the statistical analyses.

- **Status:** REMEDIATED
- **Changes:** C-010
- **Plan:** WP7
- **Response:** §3.6 states that the quality measurements ran in parallel worker processes, which does not affect them, and that every timing ran alone under the conditions of R1-M8. The analysis scripts and every result file are in the public repository and archive, whose addresses are withheld during review.
- **Where:** Section 3.6

### R1-m15

> The discussion and conclusion should more clearly distinguish findings supported by the complete paired benchmark from exploratory observations derived from restricted experimental settings.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-019, C-021, C-022
- **Plan:** WP7
- **Response:** Each result is labelled confirmatory (the main paired benchmark) or exploratory (sensitivity, validity controls, other datasets) in §4, in Table 5 and in the conclusions.
- **Where:** Section 5, Table 5; Section 6; Abstract

## Reviewer 2

### R2-1a

> First, the runtime comparisons measured in milliseconds are methodologically invalid because the experiments were distributed across commodity workstations running different operating systems without recording hardware specifications, and paired cells were not executed on identical hardware hosts. To resolve this, runtime evaluations must be conducted on a single, isolated hardware environment, [...]

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-010, C-014
- **Plan:** WP2
- **Response:** We agree with the reviewer, and the earlier timings have been replaced. All cost measurements of the revision come from one recorded host, under the controlled protocol described under R1-M8 (§3.6). Every paired comparison ran on that host in the same session.
- **Where:** Section 3.6; Section 4.2, Table 3

### R2-1b

> [...] and supplementary complexity metrics—such as theoretical time complexity, black-box model prediction calls, and FLOPs—should be reported to make the efficiency claims hardware-agnostic.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-014
- **Plan:** WP2
- **Response:** Next to time, the revision reports for each explanation the number of calls to the model and the number of rows the model evaluated. These counts do not depend on the hardware. Table 3 adds the theoretical complexity of each explainer. FLOPs are reported for logistic regression and the MLP, where they are well defined per prediction. For tree ensembles and the RBF-SVM a per-prediction FLOP count is not comparable across model types, so model calls and rows evaluated are the hardware-independent measure there (§4.2).
- **Where:** Section 4.2, Table 3

### R2-2

> Second, evaluating both explainers at a single static hyperparameter configuration fails to capture the inherent trade-offs between stability, fidelity, and computational cost; therefore, the revision must include multi-objective Pareto optimal frontiers across varying sampling budgets and kernel widths.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-016
- **Plan:** WP5
- **Response:** As requested, the revision evaluates both explainers over a grid of sampling budgets and kernel widths (LIME), and sampling budgets and background sizes (KernelSHAP). For each model it reports the Pareto-optimal configurations for stability, fidelity and cost (§4.3, Fig. 1). [R: whether one method's front dominates.]
- **Where:** Section 4.3, Fig. 1

### R2-3

> Third, the claim regarding LIME's near-zero stability on the Adult dataset is confounded by an improper hyperparameter choice, as the reference kernel width of 3.0 is severely restricted for a 103-dimensional one-hot-encoded feature space, leading to an artificial collapse of local neighborhood weights.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-008, C-016
- **Plan:** WP2 (reference width), WP4, WP5
- **Response:** We agree. The reference LIME configuration is now the library's default kernel width, 0.75√M. We also correct a figure the reviewer quotes: the Adult feature space has 108 transformed features, not 103 as the earlier text stated, so the default width is about 7.79. The value 3.0 remains one point of the sensitivity analysis, where its effect is shown (§4.3). [R: stability at the default width.]
- **Where:** Section 3.3; Section 4.3, Fig. 1

### R2-4

> Fourth, the hypothesis test for sparsity is statistically tautological since LIME's active-feature count is constrained by a hard code-level ceiling, making it mathematically inevitable to yield sparser explanations than unconstrained SHAP.

- **Status:** REMEDIATED
- **Changes:** C-005
- **Plan:** WP6 (drop H2 test), WP4 (ceiling-free sparsity)
- **Response:** We agree. With a 10-feature budget, LIME's sparsity follows from its configuration, and testing it as a hypothesis was not meaningful. The revision removes the sparsity hypothesis test (§3.1). Sparsity is reported descriptively and for LIME without the budget, together with measures that do not depend on a ceiling: the share of attribution mass in the top-k features and the normalized entropy (§4.1).
- **Where:** Section 3.1

### R2-5

> Fifth, in the cross-dataset extension, SHAP's stability was omitted without justification, leaving the multi-dataset validation incomplete and asymmetric.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-017
- **Plan:** WP3
- **Response:** Corrected: SHAP stability is now measured on every dataset (R1-M10).
- **Where:** Section 4.5, Table 4

### R2-6

> Sixth, the manuscript heavily relies on and reuses pre-computed execution cohorts and findings from reference [10], to the extent that basic summary statistics are omitted from the tables and redirected to the previous paper; the manuscript must become entirely self-contained and independently verifiable.

- **Status:** PENDING (text drafted; waits for the results of cohort B2)
- **Changes:** C-003, C-012, C-020, C-025
- **Plan:** WP2, WP3, WP7
- **Response:** We agree, and the revision is self-contained. All results come from a new cohort run for this study. Every table reports the per-method levels it compares, and no number is taken from or referred to [10], which is now cited only for the definitions of the metrics (§3.4). [Decision D-A: whether to add one sentence on why the earlier cohort was replaced.]
- **Where:** former Section 4.1; Section 4.1, Table 2; Section 5; Section 3.1

### R2-7

> Finally, the indirect disclosure of author identities through self-referencing requires careful scrubbing to maintain double-blind review integrity.

- **Status:** REMEDIATED
- **Changes:** C-003, C-004, C-024
- **Plan:** WP7 (scrub), WP9 (metadata)
- **Response:** We thank the reviewer. The author names in the text and the framing that tied this study to the earlier one were removed. The earlier study is cited in the third person, like any other source, and only for definitions. The file properties were cleared of personal data.
- **Where:** former Section 4.1; Section 3, everywhere; Build

### R2-8

> Statement of the Problem or Purpose: Poor; Relevance and importance of the Topic: Fair (Marginally relevant to the mission and purpose of the journal); Contribution to the Field: Poor (Does not provide original contributions to the literature)

- **Type:** GENERAL
- **Status:** REMEDIATED
- **Changes:** C-001, C-002
- **Plan:** WP1, WP7
- **Response:** We thank the reviewer for this assessment. As it concerns the framing of the manuscript as a whole, we re-examined the introduction and identified the following places where it could be improved: (1) the introduction opened on the popularity of the methods instead of the decision a practitioner has to make; (2) the gap was stated relative to an earlier study instead of the literature; (3) the relevance to computing practice (cost, deployment) was implicit. We revised each of them: §1 now opens with the decision problem (which explainer, for which model, under which latency and stability budget). It states the gap against recent comparisons (§2), and it presents three contributions, including cost in hardware-independent terms, a computing concern central to the journal. The new evidence behind the contributions is summarized under R1-M1.
- **Where:** Section 1 (decision problem, gap, three contributions); Section 2
