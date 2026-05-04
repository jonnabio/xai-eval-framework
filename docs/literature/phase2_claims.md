# Phase 2 Literature Review Claims

This file tracks the claims that Chapter 2 must support. Each claim should be
scope-calibrated and backed by verified sources in `xai_literature_matrix.md`.

## C1: XAI Evaluation Is Less Mature Than XAI Method Development

- **Statement**: The literature contains mature post-hoc explanation methods, but comparative evaluation remains fragmented across definitions, metrics, and protocols.
- **Status**: supported-draft
- **Sources**: `doshi-velez2017`, `abdulkadir2023`, `pawlicki2024`, `canha2025`
- **Chapter Use**: Historical development and critical gap synthesis.
- **Scope Boundary**: Applies to the reviewed XAI evaluation literature, not all interpretability work.

## C2: Single-Metric Evaluation Is Insufficient For XAI Method Selection

- **Statement**: No single metric captures all relevant explanation-quality dimensions; fidelity, stability, parsimony, cost, and human/semantic usefulness address different constructs.
- **Status**: supported-draft
- **Sources**: `pawlicki2024`, `abdulkadir2023`, `bhattacharya2024`, `hedstrom2023`
- **Chapter Use**: Metric taxonomy and justification for multi-metric benchmark.
- **Scope Boundary**: Supports multi-metric evaluation, not the claim that the thesis metrics exhaust all possible XAI objectives.

## C3: Method Families Differ In Evaluation Construct

- **Statement**: LIME, SHAP, Anchors, and DiCE produce different explanation objects, so they should not be interpreted as interchangeable outputs under a single metric.
- **Status**: supported-draft
- **Sources**: `ribeiro2016`, `lundberg2017`, `ribeiro2018`, `mothilal2020`
- **Chapter Use**: Method deep-dive and construct-validity argument.
- **Scope Boundary**: Applies to the four methods evaluated in this thesis.

## C4: Existing Toolkits Standardize Metrics But Do Not Fully Solve Protocol Governance

- **Statement**: Quantus and OpenXAI improve standardization and transparency, but the thesis still identifies a need for an operational protocol connecting experimental design, artifact qualification, statistical admissibility, and claim traceability.
- **Status**: hypothesis-to-support
- **Sources**: `hedstrom2023`, `agarwal2022`, `doshi-velez2017`
- **Chapter Use**: FOM-7 gap synthesis.
- **Scope Boundary**: Must be phrased as the thesis's identified contribution, not as a dismissal of existing frameworks.

## C5: Perturbation-Based Evaluation Can Create Construct-Validity Risks

- **Statement**: Metrics based on perturbing or masking features may create out-of-distribution instances or otherwise measure a proxy that diverges from explanation truth.
- **Status**: supported-draft
- **Sources**: `ref_7`, `zheng2025`
- **Chapter Use**: Fidelity/faithfulness caveats and robustness discussion.
- **Scope Boundary**: Applies to relevant perturbation-based evaluation schemes; avoid claiming all fidelity metrics are invalid.

## C6: FOM-7 Is Justified As An Operational Contribution

- **Statement**: The literature gap motivating FOM-7 is not the absence of metrics, but the absence of a thesis-scoped operational protocol that links design freeze, artifact validation, statistical inference, reproducibility profiling, and claim-level reporting.
- **Status**: thesis-claim
- **Sources**: C1-C5 plus Chapter 3 design.
- **Chapter Use**: Final synthesis of Chapter 2.
- **Scope Boundary**: FOM-7 is presented as a contribution for this benchmark setting and a reusable protocol pattern, not as a universal standard for all XAI.

## Rigor Review Checklist

- Does each claim cite sources that substantively support it?
- Is the claim too broad for the available evidence?
- Is the distinction between source claim and thesis inference explicit?
- Does the claim point toward the empirical design rather than float as background?
- Are limitations acknowledged before the chapter transitions to FOM-7?

## C7: Human-Centered Evidence Is Not Interchangeable With Functionally Grounded Metrics

- **Statement**: Human-centered XAI literature shows that explanation usefulness depends on stakeholder, task, interface, and cognitive context; therefore, functionally grounded metrics should not be presented as direct evidence of human usefulness.
- **Status**: supported-draft
- **Sources**: `miller2019`, `abdul2018`, `mohseni2021`, `langer2021`, `sokol2020`, `kaur2020`, `hase2020`, `zhang2024`
- **Chapter Use**: Conceptual distinctions and evaluation-framework sections.
- **Scope Boundary**: Supports scope calibration for the thesis; it does not require Chapter 2 to become a full HCI/user-study thesis.

## C8: Post-Hoc Explanation Methods Require Robustness And Validity Checks

- **Statement**: Post-hoc explanations can be unstable, manipulable, or misleading under some settings, so benchmark protocols should include robustness, validity, and scope checks rather than reporting explanation outputs as self-validating artifacts.
- **Status**: supported-draft
- **Sources**: `burger2023`, `slack2020`, `laugel2019`, `tomsett2020`, `nauta2023`
- **Chapter Use**: LIME/SHAP limitations, counterfactual limitations, and metric-validity discussion.
- **Scope Boundary**: Does not imply all post-hoc explanations are invalid; it supports the need for guarded evaluation.

## C9: Counterfactual Explanations Need Actionability And Feasibility Criteria

- **Statement**: Counterfactual explanations should be evaluated not only by whether they change model output, but also by feasibility, actionability, and relationship to recourse.
- **Status**: supported-draft
- **Sources**: `mothilal2020`, `karimi2022`, `poyiadzi2020`, `laugel2019`
- **Chapter Use**: DiCE and counterfactual explanation subsection.
- **Scope Boundary**: Applies primarily to counterfactual/recourse explanations, not to attribution or rule explanations.
