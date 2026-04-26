# Integrated Evidence Snapshot: EXP1 + EXP2 + EXP3

Date: 2026-04-26
Status: Generated analysis handoff

## Scope

This package integrates the three empirical layers used by the thesis and paper
track:

- EXP1: Adult calibration and reproducibility baseline.
- EXP2: Adult robustness benchmark and primary inferential cohort.
- EXP3: two-domain external tabular validation on Breast Cancer and German
  Credit.

## Completeness

```text
EXP1 core runs: 4 / 4
EXP2 analyzable runs after recovery overlay: 275 / 300 planned
EXP2 recovery overlay rows: 30
EXP3 completed runs: 24 / 24
```

## Method-Level Snapshot

| Experiment | Explainer | Runs | Fidelity | Stability | Active-feature ratio | Cost (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| EXP1 | shap | 2 | 0.463 | 0.699 | 0.343 | 0.1 |
| EXP1 | lime | 2 | 0.308 | 0.104 | 0.093 | 31.0 |
| EXP2 | shap | 75 | 0.808 | 0.732 | 0.226 | 11034.7 |
| EXP2 | lime | 75 | 0.560 | 0.014 | 0.085 | 226.5 |
| EXP2 | anchors | 57 | 0.388 | 0.052 | 0.084 | 38094.2 |
| EXP2 | dice | 68 | 0.172 | 0.366 | 0.017 | 2056.3 |
| EXP3 | shap | 12 | 0.702 | 0.873 | 0.756 | 1003.1 |
| EXP3 | anchors | 12 | 0.319 | 0.533 | 0.080 | 2744.4 |

## EXP3 Dataset Snapshot

| Dataset | Explainer | Runs | Fidelity | Stability | Active-feature ratio | Duration (s) |
| --- | --- | --- | --- | --- | --- | --- |
| breast_cancer | anchors | 6 | 0.236 | 0.392 | 0.069 | 4635.8 |
| breast_cancer | shap | 6 | 0.693 | 0.953 | 0.656 | 231.9 |
| german_credit | anchors | 6 | 0.401 | 0.675 | 0.091 | 4733.1 |
| german_credit | shap | 6 | 0.712 | 0.793 | 0.857 | 193.8 |

## Integrated Interpretation

- EXP1 remains the calibration layer: it establishes Adult baseline behavior for
  RF/XGB with LIME and SHAP before the robustness campaign.
- EXP2 remains the primary inferential layer: it provides the large factorial
  Adult benchmark, recovery-overlay qualification, non-parametric tests, and the
  strongest evidence for method ranking.
- EXP3 is the external-validity layer: it should be used to qualify, not replace,
  the EXP2 claim. The thesis-level wording should be "Adult-centered benchmark
  with two-domain external tabular validation."
- In the integrated evidence package, SHAP retains the technical-quality profile
  established in EXP2. The EXP2 SHAP-LIME mean fidelity gap is
  0.248, and the EXP3 SHAP-Anchors mean fidelity gap is
  0.384.
- The runtime story must remain bounded. EXP2 supports LIME as the low-latency
  attribution method, while EXP3 shows that Anchors can be slower than SHAP in
  the completed cross-dataset matrix.

## Use Rules

- Use EXP2 for confirmatory statistical claims.
- Use EXP3 for portability and external-validity language.
- Use EXP1 for calibration, reproducibility, and historical continuity.
- Do not pool EXP3 with EXP2 for a single omnibus hypothesis test unless a new
  preregistered cross-study statistical design is added.
