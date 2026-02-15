# Literature Review Matrix for Methodology Design

This matrix consolidates the attached paper set and maps each paper to concrete design decisions for the JMLR prototype.

## Summary
- Total papers reviewed: 25
- Primary clusters: metric taxonomies, faithfulness/attribution theory, benchmarking toolkits, modality-specific XAI benchmarks, and LLM-as-a-judge reliability.
- Main methodological implication: keep multi-metric evaluation, report uncertainty and coverage, and treat LLM judges as calibrated proxies rather than direct substitutes for users.

## Paper-by-Paper Mapping

| Paper | Primary focus | Methodology implication for this project | Confidence |
| :--- | :--- | :--- | :--- |
| `14708_XAI_Evaluation_Metrics__Taxonomies__Concepts_and_Applications__INES_2023_-7.pdf` | XAI metric taxonomy and PRISMA-style review | Keep explicit metric taxonomy and justify why each metric is needed | High |
| `A Survey on LLM-as-a-Judge.pdf` | LLM-judge design patterns, failure modes, and evaluation pipeline | Add judge calibration, bias checks, and meta-evaluation protocol | Medium |
| `Attribution-based Explanations that Provide Recourse.pdf` | Tension between robustness and recourse sensitivity | Report trade-offs instead of claiming universal dominance of one explainer | High |
| `Automating expert-level medical reasoning evaluation of large language models.pdf` | Domain-expert evaluation automation with LLMs | Use domain-aware rubrics and avoid generic one-score semantic evaluation | Title-level |
| `B-XAIC Dataset Benchmarking Explainable AI for Graph Neural Networks Using Chemical Data.pdf` | Ground-truth rationales and benchmark realism for GNN XAI | Emphasize benchmark realism and rationale-linked datasets in future expansions | High |
| `Consensus on Feature Attributions in the Rashomon Set.pdf` | Attribution consensus under model multiplicity | Add model uncertainty framing and consensus reporting where possible | High |
| `Discovering Salient Neurons in deep NLP models.pdf` | Neuron-level interpretability and localization | Keep scope clear: feature attributions differ from representation-level interpretability | High |
| `Evaluating explainability for graph neural networks.pdf` | Evaluation framework for GNN explainers | Include modality-specific caveat: metrics may not transfer unchanged to graphs | Title-level |
| `Evaluating the necessity of the multiple metrics for assessing explainable AI A critical examination.pdf` | Necessity and redundancy of multiple metrics | Retain multi-metric suite and test complementarity statistically | High |
| `Evaluating the necessity of the multiple metrics for assessing explainable AIAcritical examination.pdf` | Duplicate of previous paper | De-duplicate references and avoid double counting evidence | High |
| `Evaluation of Neural Network Explanations and Beyond.pdf` | Systematic evaluation of explanation methods | Include standardized metric implementations and transparent reporting | High |
| `Explaining Deep Models in PaddlePaddle.pdf` | Practical XAI toolkit integration | Preserve modular API design for explainers/metrics | High |
| `F-FIDELITY A ROBUST FRAMEWORK FOR FAITHFULNESS EVALUATION OF EXPLAINABLE AI.pdf` | Faithfulness robustness and perturbation-aware evaluation | Add robustness-aware faithfulness interpretation and sensitivity checks | Medium |
| `Globally-Consistent Rule-Based Summary-Explanations for Machine Learning Models.pdf` | Globally consistent local rule summaries | Distinguish local explanation quality from global consistency requirements | High |
| `NeurIPS-2023-judging-llm-as-a-judge-with-mt-bench-and-chatbot-arena-Paper-Datasets_and_Benchmarks.pdf` | LLM-as-judge validation against human preference | Keep LLM judge as proxy, include known judge biases and control strategy | High |
| `On the Complexity of SHAP-Score-Based Explanations.pdf` | Computational complexity of SHAP-score explanations | Report computational cost as first-class metric and discuss tractability | High |
| `On the Faithfulness of Vision Transformer Explanations.pdf` | Faithfulness metric limitations and alternatives | Avoid single-faithfulness-metric claims; report multiple faithfulness indicators | High |
| `OpenXAI- Towards a Transparent Evaluation of Post hoc Model Explanations.pdf` | Reproducible benchmarking framework with broad metric coverage | Keep transparent artifact structure and explicit benchmark inventory | High |
| `Quantus- An Explainable AI Toolkit for Responsible Evaluation of Neural Network Explanations and Beyond.pdf` | Open toolkit for explanation evaluation | Align metric definitions and reproducibility behavior with established toolkit practice | High |
| `Sampling Permutations for Shapley Value Estimation.pdf` | Better approximation schemes for Shapley estimation | Attribute runtime/variance differences partly to estimator choice, not only explainer family | High |
| `The Faithful Shapley Interaction Index.pdf` | Interaction-level Shapley faithfulness axioms | Clarify whether feature interaction effects are modeled or omitted in baseline pipeline | High |
| `User Perceptions vs. Proxy LLM Judges.pdf` | Gap between proxy LLM judges and user perceptions | Add explicit external-validity caveat for LLM semantic scores | High |
| `Using Prototypical Few-Shot Architecture for Explainable AI.pdf` | Intrinsic explainability via prototypical/few-shot structures | Separate intrinsic and post-hoc explainability claims in framing | Medium |
| `Using Shapley Values and Variational Autoencoders to Explain Predictive Models with Dependent Mixed Features.pdf` | Shapley under dependent mixed features | State dependence assumptions and note limits of independent-feature approximations | High |
| `XAI Beyond Classification.pdf` | Explainability in unsupervised/clustering settings | Add scope boundary: current benchmark is classification-focused; extension path needed | High |

## Design Principles Adopted
1. Multi-metric reporting is mandatory; single-score ranking is not sufficient.
2. Faithfulness should be treated as a family of tests, not one number.
3. Runtime and numerical stability are part of explanation quality.
4. Coverage accounting (missing/corrupt runs) is part of scientific reporting.
5. LLM judges require calibration and human-grounded validation before strong claims.
