# Paper B, C&I 2067810: Reviewer 1, detailed report (verbatim)

The file attached by Reviewer 1 on DergiPark, pasted by the author on 2026-11-06. Item IDs used
in `REVIEW_ANALYSIS.md`: major comment *n* = **R1-M*n***, minor comment *n* = **R1-m*n***.

---

Reviewer Report

Manuscript Title: When Does SHAP Outperform LIME? Model- and Configuration-Dependent Results from a Paired Tabular Benchmark

Recommendation: Major Revision

## Major Comments

Comment 1: The manuscript extends a previously published SHAP–LIME comparison from 45 to 75 matched configurations. The authors should clearly establish the scientific novelty of the present work and distinguish its original contributions from previously reported findings.

Comment 2: The statistical independence of the 75 matched configurations requires further justification. The authors should address potential dependencies arising from shared datasets, model configurations, random seeds, and sampling intensities and assess their implications for statistical inference.

Comment 3: The authors should demonstrate the robustness of the reported statistical significance and confidence intervals using an analytical approach that accounts for the hierarchical structure of the experimental design.

Comment 4: The fairness of the SHAP–LIME comparison requires further investigation. In particular, the fixed feature budget imposed on LIME and the use of different SHAP implementations may influence the reported differences in sparsity, fidelity, and computational efficiency.

Comment 5: Additional sensitivity analyses are needed to determine whether the observed performance differences remain consistent across alternative LIME and SHAP hyperparameter configurations, rather than reflecting the particular settings selected for the benchmark.

Comment 6: The application of Gaussian perturbations to one-hot-encoded categorical features may generate unrealistic observations. The authors should evaluate whether the reported stability results remain valid under perturbation strategies that preserve categorical constraints and relevant feature dependencies.

Comment 7: The exceptionally low LIME stability observed on the Adult dataset may be influenced by the perturbation protocol and kernel-width configuration. The authors should investigate these effects more systematically before attributing the observed differences primarily to the explanation methods.

Comment 8: The computational cost comparisons are potentially confounded by heterogeneous execution environments. The authors should validate the principal latency findings using standardized hardware, software configurations, and repeated timing measurements.

Comment 9: The reported reversal in runtime performance between XGBoost and random forests represents an important finding. However, additional controlled experiments are necessary to determine whether this behavior consistently reflects model architecture rather than implementation-specific or hardware-dependent effects.

Comment 10: The cross-dataset analysis does not include SHAP stability measurements. The authors should extend the evaluation to both explainers on the additional datasets or explicitly restrict their generalizability claims to the outcomes directly supported by the experiments.

Comment 11: The kernel-width sensitivity analysis is restricted to a single model and random seed. Additional experiments across multiple seeds and model families are necessary to establish the robustness of the reported stability–fidelity trade-off.

Comment 12: The kernel-width experiments contain different numbers of valid explanations across configurations. The authors should address the potential influence of this variation on the comparative results and consider evaluating the metrics on a common set of valid instances.

Comment 13: The masking sensitivity analysis is limited to a small subset of random-forest experiments. The authors should investigate whether the reported SHAP advantages in fidelity and faithfulness persist across alternative masking strategies and additional model families.

Comment 14: The reported effect sizes, particularly the exceptionally large values for fidelity and stability, require further statistical justification. The authors should clarify their computation, examine the distributions of paired differences, and assess their robustness to potential dependence among configurations.

Comment 15: The practical recommendations regarding explainer selection appear broader than the experimental evidence supports. The authors should strengthen the empirical justification for these recommendations or explicitly restrict them to the evaluated models, datasets, configurations, and computational settings.

## Minor Comments

Comment 1: The abstract should clearly distinguish findings obtained from the primary Adult benchmark from those derived from the supplementary cross-dataset and sensitivity experiments.

Comment 2: The mathematical notation and directional hypotheses associated with RQ1–RQ4 should be presented more explicitly and consistently.

Comment 3: The experimental design should be summarized in a dedicated table specifying model families, random seeds, sampling intensities, and the number of matched configurations.

Comment 4: Additional details concerning model hyperparameters, preprocessing procedures, training and testing partitions, and evaluation instance selection should be provided to improve reproducibility.

Comment 5: The procedure used to sample instances from the TP, TN, FP, and FN strata should be clarified, including whether evaluation instances overlap across configurations.

Comment 6: The stability metric description should specify how zero-valued attribution vectors and undefined cosine similarity values were handled.

Comment 7: The fidelity calculation should explicitly define the treatment of attribution signs, feature-removal effects, and undefined correlation coefficients.

Comment 8: Table 1 should present the statistical estimates, confidence intervals, adjusted p-values, and effect sizes using consistent notation and clearly defined column headings.

Comment 9: The qualitative reproducibility classifications in Table 2 should be supported by predefined criteria or replaced with appropriately qualified numerical interpretations.

Comment 10: Figures 1 and 2 should be improved in terms of axis labeling, statistical notation, scale descriptions, and overall readability.

Comment 11: Tables 4 and 5 should include measures of variability or uncertainty alongside the reported three-seed averages.

Comment 12: The methodological relevance of including Anchors in the cross-dataset analysis should be clarified in relation to the manuscript's primary SHAP–LIME research questions.

Comment 13: The grouped masking procedure should be described in greater detail, particularly regarding the identification and treatment of correlated or related features.

Comment 14: The reproducibility section should provide additional information about computational parallelism, execution settings, and the availability of scripts used to reproduce the statistical analyses.

Comment 15: The discussion and conclusion should more clearly distinguish findings supported by the complete paired benchmark from exploratory observations derived from restricted experimental settings.

## Overall Recommendation

Major Revision

The manuscript addresses a relevant research problem and presents potentially valuable findings concerning the model- and configuration-dependent behavior of SHAP and LIME. However, substantial methodological clarification, additional experimental validation, and stronger statistical justification are required before the conclusions can be considered sufficiently robust for publication.
