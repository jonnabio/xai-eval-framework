# Paper B, C&I submission 2067810: decision of 2026-11-06 (verbatim)

Received by the author and pasted into the session of 2026-11-06. Kept verbatim as the source
of every item in `REVIEW_ANALYSIS.md`. Rating scales are as given by the journal form.

---

Dear Jonathan Herrera,

Decision: Major Revision

Decision Date: November 6, 2026

Editor Comment: Thank you for submitting your manuscript "When Does SHAP Outperform LIME? Model- and Configuration-Dependent Results from a Paired Tabular Benchmark" (ID: 2067810) to Computers and Informatics. The manuscript has been evaluated by two reviewers. Based on their reports and our editorial assessment, we invite you to submit a major revision.

This decision does not guarantee eventual acceptance. The revised manuscript will be re-evaluated, and acceptance will depend on whether the concerns are adequately addressed.

Please address all points raised in the reviewer reports appended below. In addition, as an editorial requirement, please ensure that the main benchmark includes at least one state-of-the-art explainer comparison (e.g., Anchors or DiCE), or provide a clear justification if this is not feasible.

Please submit your revised manuscript and a point-by-point response letter. If you need additional time, please contact the editorial office before the deadline.

We appreciate your interest in Computers and Informatics and look forward to receiving your revised submission.

Sincerely,

Prof. Dr. Mehmet Tekerek
Editor in Chief
Computers and Informatics

## Reviewer-1

1. Short Summary of the Manuscript:
-The manuscript presents a comparative evaluation of SHAP and LIME using a paired experimental benchmark comprising 75 matched configurations across five machine learning model families on the UCI Adult dataset. The study examines explanation stability, sparsity, fidelity, faithfulness gap, and computational cost through paired statistical analyses, including Holm-adjusted significance testing and effect-size estimation. Additional experiments involving the Breast Cancer Wisconsin and German Credit datasets investigate the sensitivity of selected findings to dataset characteristics, while supplementary analyses examine LIME kernel-width settings and feature-masking strategies. The results indicate that SHAP generally achieves higher stability and fidelity under the reference benchmark configuration, whereas LIME provides sparser explanations and lower computational costs in most evaluated settings. However, runtime performance varies considerably across model architectures, and LIME stability appears sensitive to experimental configuration and feature representation. The study provides potentially useful insights into explainer selection, although methodological limitations concerning statistical dependence, perturbation validity, computational environments, and cross-dataset generalizability require further consideration.

2. Statement of the Problem or Purpose: Good
3. Relevance and importance of the Topic: Excellent
4. Contribution to the Field: Fair (Provides marginal original contributions to the literature)
5. Organization of the manuscript: Poor
6. Drawing and Building Upon Relevant Literature: Poor
7. Methodology: Poor
8. Discussion: Fair
9. Conclusion: Fair (Fair conclusion without sufficient justification from evidence presented)

Comments and Suggestions for Author: The manuscript addresses a relevant research problem in explainable artificial intelligence and presents potentially valuable findings regarding the model and configuration dependent performance of SHAP and LIME. The paired experimental design and multi-metric evaluation are noteworthy strengths. However, several substantial issues must be addressed before the manuscript can be considered for publication. In particular, the authors should more clearly establish the novelty of the study relative to previously published work, account for potential statistical dependencies among experimental configurations, and strengthen the validity of the perturbation-based stability evaluation. Furthermore, the fairness of the explainer configurations, reliability of computational cost measurements, and generalizability of the cross-dataset findings require additional investigation. The statistical analysis and interpretation of effect sizes should also be strengthened. I encourage the authors to address the major and minor comments comprehensively, provide additional experimental validation where necessary, and ensure that the conclusions are fully supported by the reported evidence.

Recommendation: Major Revision

## Reviewer-2

1. Short Summary of the Manuscript:
-This manuscript presents a controlled, paired empirical comparison of two widely used post-hoc explainability methods, SHAP and LIME, across five model families (logistic regression, random forest, XGBoost, SVM, and MLP) and 75 matched experimental cells on the UCI Adult dataset. The authors evaluate five primary endpoints—stability, fidelity, faithfulness gap, sparsity, and computational cost—using Holm-corrected paired Wilcoxon signed-rank tests and standardized effect sizes (d z). While the aggregate results confirm that SHAP outperforms LIME in stability and fidelity whereas LIME produces sparser explanations, the study highlights that runtime ordering is strictly model-dependent, with SHAP's TreeExplainer running faster than LIME on XGBoost but slower on random forests. Furthermore, through cross-dataset extensions (Breast Cancer and German Credit) and a sensitivity probe, the paper demonstrates that LIME's near-zero stability on the Adult dataset is not an intrinsic flaw of the algorithm, but rather a condition-dependent outcome modulated by the high-dimensional one-hot-encoded feature space and the chosen kernel width.

2. Statement of the Problem or Purpose: Poor
3. Relevance and importance of the Topic: Fair (Marginally relevant to the mission and purpose of the journal)
4. Contribution to the Field: Poor (Does not provide original contributions to the literature)
5. Organization of the manuscript: Fair
6. Drawing and Building Upon Relevant Literature: Good
7. Methodology: Fair
8. Discussion: Fair
9. Conclusion: Fair (Fair conclusion without sufficient justification from evidence presented)

Comments and Suggestions for Author: Dear Author, Your manuscript has been evaluated by the editorial board and peer reviewers, and it has been determined that it requires a Major Revision before further consideration can be given. While the comparative evaluation of SHAP and LIME across multiple model families addresses a highly relevant topic in explainable artificial intelligence (XAI), the current version of the manuscript exhibits several critical methodological flaws, experimental limitations, and presentation issues that must be thoroughly addressed. First, the runtime comparisons measured in milliseconds are methodologically invalid because the experiments were distributed across commodity workstations running different operating systems without recording hardware specifications, and paired cells were not executed on identical hardware hosts. To resolve this, runtime evaluations must be conducted on a single, isolated hardware environment, and supplementary complexity metrics—such as theoretical time complexity, black-box model prediction calls, and FLOPs—should be reported to make the efficiency claims hardware-agnostic. Second, evaluating both explainers at a single static hyperparameter configuration fails to capture the inherent trade-offs between stability, fidelity, and computational cost; therefore, the revision must include multi-objective Pareto optimal frontiers across varying sampling budgets and kernel widths. Third, the claim regarding LIME's near-zero stability on the Adult dataset is confounded by an improper hyperparameter choice, as the reference kernel width of 3.0 is severely restricted for a 103-dimensional one-hot-encoded feature space, leading to an artificial collapse of local neighborhood weights. Fourth, the hypothesis test for sparsity is statistically tautological since LIME's active-feature count is constrained by a hard code-level ceiling, making it mathematically inevitable to yield sparser explanations than unconstrained SHAP. Fifth, in the cross-dataset extension, SHAP's stability was omitted without justification, leaving the multi-dataset validation incomplete and asymmetric. Sixth, the manuscript heavily relies on and reuses pre-computed execution cohorts and findings from reference [10], to the extent that basic summary statistics are omitted from the tables and redirected to the previous paper; the manuscript must become entirely self-contained and independently verifiable. Finally, the indirect disclosure of author identities through self-referencing requires careful scrubbing to maintain double-blind review integrity. You are invited to submit a revised manuscript accompanied by a detailed point-by-point response letter addressing all the concerns raised above.

Recommendation: Major Revision
