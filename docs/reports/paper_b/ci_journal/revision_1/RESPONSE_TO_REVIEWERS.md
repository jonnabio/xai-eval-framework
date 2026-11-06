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

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP2, WP3
- **Response:** 
- **Where:** 

### ED-2

> Please submit your revised manuscript and a point-by-point response letter.

- **Status:** EXPLAINED
- **Changes:** 
- **Plan:** WP9
- **Response:** This letter answers every point of the editor and of both reviewers, one by one, and states where the manuscript changed. A copy of the revised manuscript with every change marked is provided as well.
- **Where:** 

### ED-3

> If you need additional time, please contact the editorial office before the deadline.

- **Status:** EXPLAINED
- **Changes:** 
- **Plan:** Q-1
- **Response:** The revision is submitted within the deadline (30 November 2026).
- **Where:** 

## Reviewer 1: general assessment

### R1-1

> In particular, the authors should more clearly establish the novelty of the study relative to previously published work [...] (Contribution to the Field: Fair)

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP1, WP2, WP7
- **Response:** 
- **Where:** 

### R1-2

> [...] account for potential statistical dependencies among experimental configurations [...]

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP6
- **Response:** 
- **Where:** 

### R1-3

> [...] and strengthen the validity of the perturbation-based stability evaluation.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP4
- **Response:** 
- **Where:** 

### R1-4

> Furthermore, the fairness of the explainer configurations [...] require[s] additional investigation.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP2, WP5
- **Response:** 
- **Where:** 

### R1-5

> [...] reliability of computational cost measurements [...] require[s] additional investigation.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP2
- **Response:** 
- **Where:** 

### R1-6

> [...] and generalizability of the cross-dataset findings require additional investigation.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP3
- **Response:** 
- **Where:** 

### R1-7

> The statistical analysis and interpretation of effect sizes should also be strengthened.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP6
- **Response:** 
- **Where:** 

### R1-8

> Organization of the manuscript: Poor (Poor organization of ideas and supporting points)

- **Type:** GENERAL
- **Status:** PENDING
- **Changes:** 
- **Plan:** WP7
- **Response:** We thank the reviewer for this assessment. As the comment concerns the manuscript as a whole, we reviewed every section against it and identified the following places where organization could be improved: (1) [place: what was weak]. We revised each of them: [what changed]. [DRAFT: complete with the C-### changes]
- **Where:** 

### R1-9

> Drawing and Building Upon Relevant Literature: Poor (Provides a poor summary of the major points in the relevant literature)

- **Type:** GENERAL
- **Status:** PENDING
- **Changes:** 
- **Plan:** WP8, D-6
- **Response:** We thank the reviewer for this assessment. As the comment concerns the manuscript as a whole, we reviewed every section against it and identified the following places where the use of the literature could be improved: (1) [place: what was weak]. We revised each of them: [what changed]. [DRAFT: complete with the C-### changes]
- **Where:** 

### R1-10

> [...] ensure that the conclusions are fully supported by the reported evidence. (Conclusion: Fair conclusion without sufficient justification from evidence presented)

- **Type:** GENERAL
- **Status:** PENDING
- **Changes:** 
- **Plan:** WP7
- **Response:** We thank the reviewer for this assessment. As the comment concerns the manuscript as a whole, we reviewed every section against it and identified the following places where the support of the conclusions by the evidence could be improved: (1) [place: what was weak]. We revised each of them: [what changed]. [DRAFT: complete with the C-### changes]
- **Where:** 

### R1-11

> I encourage the authors to address the major and minor comments comprehensively, provide additional experimental validation where necessary [...]

- **Status:** EXPLAINED
- **Changes:** 
- **Plan:** §2b
- **Response:** Each major and minor comment of the detailed report is answered individually below (R1-M1 to R1-M15 and R1-m1 to R1-m15).
- **Where:** 

## Reviewer 1: major comments

### R1-M1

> The manuscript extends a previously published SHAP–LIME comparison from 45 to 75 matched configurations. The authors should clearly establish the scientific novelty of the present work and distinguish its original contributions from previously reported findings.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP1, WP7
- **Response:** 
- **Where:** 

### R1-M2

> The statistical independence of the 75 matched configurations requires further justification. The authors should address potential dependencies arising from shared datasets, model configurations, random seeds, and sampling intensities and assess their implications for statistical inference.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP6
- **Response:** 
- **Where:** 

### R1-M3

> The authors should demonstrate the robustness of the reported statistical significance and confidence intervals using an analytical approach that accounts for the hierarchical structure of the experimental design.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP6
- **Response:** 
- **Where:** 

### R1-M4

> The fairness of the SHAP–LIME comparison requires further investigation. In particular, the fixed feature budget imposed on LIME and the use of different SHAP implementations may influence the reported differences in sparsity, fidelity, and computational efficiency.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP5
- **Response:** 
- **Where:** 

### R1-M5

> Additional sensitivity analyses are needed to determine whether the observed performance differences remain consistent across alternative LIME and SHAP hyperparameter configurations, rather than reflecting the particular settings selected for the benchmark.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP5
- **Response:** 
- **Where:** 

### R1-M6

> The application of Gaussian perturbations to one-hot-encoded categorical features may generate unrealistic observations. The authors should evaluate whether the reported stability results remain valid under perturbation strategies that preserve categorical constraints and relevant feature dependencies.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP4
- **Response:** 
- **Where:** 

### R1-M7

> The exceptionally low LIME stability observed on the Adult dataset may be influenced by the perturbation protocol and kernel-width configuration. The authors should investigate these effects more systematically before attributing the observed differences primarily to the explanation methods.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP4, WP5
- **Response:** 
- **Where:** 

### R1-M8

> The computational cost comparisons are potentially confounded by heterogeneous execution environments. The authors should validate the principal latency findings using standardized hardware, software configurations, and repeated timing measurements.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP2
- **Response:** 
- **Where:** 

### R1-M9

> The reported reversal in runtime performance between XGBoost and random forests represents an important finding. However, additional controlled experiments are necessary to determine whether this behavior consistently reflects model architecture rather than implementation-specific or hardware-dependent effects.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP2b
- **Response:** 
- **Where:** 

### R1-M10

> The cross-dataset analysis does not include SHAP stability measurements. The authors should extend the evaluation to both explainers on the additional datasets or explicitly restrict their generalizability claims to the outcomes directly supported by the experiments.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP3
- **Response:** 
- **Where:** 

### R1-M11

> The kernel-width sensitivity analysis is restricted to a single model and random seed. Additional experiments across multiple seeds and model families are necessary to establish the robustness of the reported stability–fidelity trade-off.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP5
- **Response:** 
- **Where:** 

### R1-M12

> The kernel-width experiments contain different numbers of valid explanations across configurations. The authors should address the potential influence of this variation on the comparative results and consider evaluating the metrics on a common set of valid instances.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP5
- **Response:** 
- **Where:** 

### R1-M13

> The masking sensitivity analysis is limited to a small subset of random-forest experiments. The authors should investigate whether the reported SHAP advantages in fidelity and faithfulness persist across alternative masking strategies and additional model families.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP4b
- **Response:** 
- **Where:** 

### R1-M14

> The reported effect sizes, particularly the exceptionally large values for fidelity and stability, require further statistical justification. The authors should clarify their computation, examine the distributions of paired differences, and assess their robustness to potential dependence among configurations.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP6
- **Response:** 
- **Where:** 

### R1-M15

> The practical recommendations regarding explainer selection appear broader than the experimental evidence supports. The authors should strengthen the empirical justification for these recommendations or explicitly restrict them to the evaluated models, datasets, configurations, and computational settings.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP7
- **Response:** 
- **Where:** 

## Reviewer 1: minor comments

### R1-m1

> The abstract should clearly distinguish findings obtained from the primary Adult benchmark from those derived from the supplementary cross-dataset and sensitivity experiments.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP7
- **Response:** 
- **Where:** 

### R1-m2

> The mathematical notation and directional hypotheses associated with RQ1–RQ4 should be presented more explicitly and consistently.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP7
- **Response:** 
- **Where:** 

### R1-m3

> The experimental design should be summarized in a dedicated table specifying model families, random seeds, sampling intensities, and the number of matched configurations.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP7
- **Response:** 
- **Where:** 

### R1-m4

> Additional details concerning model hyperparameters, preprocessing procedures, training and testing partitions, and evaluation instance selection should be provided to improve reproducibility.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP7
- **Response:** 
- **Where:** 

### R1-m5

> The procedure used to sample instances from the TP, TN, FP, and FN strata should be clarified, including whether evaluation instances overlap across configurations.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP0, WP6
- **Response:** 
- **Where:** 

### R1-m6

> The stability metric description should specify how zero-valued attribution vectors and undefined cosine similarity values were handled.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP0, WP4
- **Response:** 
- **Where:** 

### R1-m7

> The fidelity calculation should explicitly define the treatment of attribution signs, feature-removal effects, and undefined correlation coefficients.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP0, WP7
- **Response:** 
- **Where:** 

### R1-m8

> Table 1 should present the statistical estimates, confidence intervals, adjusted p-values, and effect sizes using consistent notation and clearly defined column headings.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP7
- **Response:** 
- **Where:** 

### R1-m9

> The qualitative reproducibility classifications in Table 2 should be supported by predefined criteria or replaced with appropriately qualified numerical interpretations.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP7
- **Response:** 
- **Where:** 

### R1-m10

> Figures 1 and 2 should be improved in terms of axis labeling, statistical notation, scale descriptions, and overall readability.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP7
- **Response:** 
- **Where:** 

### R1-m11

> Tables 4 and 5 should include measures of variability or uncertainty alongside the reported three-seed averages.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP3
- **Response:** 
- **Where:** 

### R1-m12

> The methodological relevance of including Anchors in the cross-dataset analysis should be clarified in relation to the manuscript's primary SHAP–LIME research questions.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP7
- **Response:** 
- **Where:** 

### R1-m13

> The grouped masking procedure should be described in greater detail, particularly regarding the identification and treatment of correlated or related features.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP4b, WP7
- **Response:** 
- **Where:** 

### R1-m14

> The reproducibility section should provide additional information about computational parallelism, execution settings, and the availability of scripts used to reproduce the statistical analyses.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP7
- **Response:** 
- **Where:** 

### R1-m15

> The discussion and conclusion should more clearly distinguish findings supported by the complete paired benchmark from exploratory observations derived from restricted experimental settings.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP7
- **Response:** 
- **Where:** 

## Reviewer 2

### R2-1a

> First, the runtime comparisons measured in milliseconds are methodologically invalid because the experiments were distributed across commodity workstations running different operating systems without recording hardware specifications, and paired cells were not executed on identical hardware hosts. To resolve this, runtime evaluations must be conducted on a single, isolated hardware environment, [...]

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP2
- **Response:** 
- **Where:** 

### R2-1b

> [...] and supplementary complexity metrics—such as theoretical time complexity, black-box model prediction calls, and FLOPs—should be reported to make the efficiency claims hardware-agnostic.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP2
- **Response:** 
- **Where:** 

### R2-2

> Second, evaluating both explainers at a single static hyperparameter configuration fails to capture the inherent trade-offs between stability, fidelity, and computational cost; therefore, the revision must include multi-objective Pareto optimal frontiers across varying sampling budgets and kernel widths.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP5
- **Response:** 
- **Where:** 

### R2-3

> Third, the claim regarding LIME's near-zero stability on the Adult dataset is confounded by an improper hyperparameter choice, as the reference kernel width of 3.0 is severely restricted for a 103-dimensional one-hot-encoded feature space, leading to an artificial collapse of local neighborhood weights.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP2 (reference width), WP4, WP5
- **Response:** 
- **Where:** 

### R2-4

> Fourth, the hypothesis test for sparsity is statistically tautological since LIME's active-feature count is constrained by a hard code-level ceiling, making it mathematically inevitable to yield sparser explanations than unconstrained SHAP.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP6 (drop H2 test), WP4 (ceiling-free sparsity)
- **Response:** 
- **Where:** 

### R2-5

> Fifth, in the cross-dataset extension, SHAP's stability was omitted without justification, leaving the multi-dataset validation incomplete and asymmetric.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP3
- **Response:** 
- **Where:** 

### R2-6

> Sixth, the manuscript heavily relies on and reuses pre-computed execution cohorts and findings from reference [10], to the extent that basic summary statistics are omitted from the tables and redirected to the previous paper; the manuscript must become entirely self-contained and independently verifiable.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP2, WP3, WP7
- **Response:** 
- **Where:** 

### R2-7

> Finally, the indirect disclosure of author identities through self-referencing requires careful scrubbing to maintain double-blind review integrity.

- **Status:** PENDING
- **Changes:** 
- **Plan:** WP7 (scrub), WP9 (metadata)
- **Response:** 
- **Where:** 

### R2-8

> Statement of the Problem or Purpose: Poor; Relevance and importance of the Topic: Fair (Marginally relevant to the mission and purpose of the journal); Contribution to the Field: Poor (Does not provide original contributions to the literature)

- **Type:** GENERAL
- **Status:** PENDING
- **Changes:** 
- **Plan:** WP1, WP7
- **Response:** We thank the reviewer for this assessment. As the comment concerns the manuscript as a whole, we reviewed every section against it and identified the following places where the statement of the problem, the relevance to the journal and the contribution could be improved: (1) [place: what was weak]. We revised each of them: [what changed]. [DRAFT: complete with the C-### changes]
- **Where:** 
