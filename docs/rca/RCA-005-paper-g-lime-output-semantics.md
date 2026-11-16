# RCA-005: Paper G scored LIME slopes as if they were contributions

**Status**: Corrective action in place (guard merged, PR #131); supplementary validation S3 under plan section 12
**Severity**: High (construct validity of every LIME-involving Paper G result; no data lost or altered)
**Opened**: 2026-11-16
**Role**: Scientific Advisor → Incident Responder
**Related**: `docs/reports/paper_g/PAPER_G_POST_ANALYSIS_QUALITY_REVIEW.md` (section 2);
`docs/reports/paper_e/ANALYSIS_PLAN.md` (entries of 2026-10-03/04); RCA-001 (numbers drifting from
their source: the same class of "assumption never checked against the artifact").

## Symptoms

- In the Paper G synthetic check, LIME's agreement with the exact Shapley values was 0.00–0.02 in
  every condition, equal to the random control, while SHAP and occlusion reached 0.68–0.97.
- LIME's agreement had opposite signs by predicted class (−0.111 for class 0, +0.128 for class 1).
- Found after the single authorized analysis (PR #129), by the post-analysis review (PR #130).

## Evidence

- `scripts/paper_g_lib.py`, class `Lime`: `LimeTabularExplainer(..., discretize_continuous=False,
  kernel_width=3.0)`, hard-coded, copied from `scripts/paper_f_lib.py:212`; not in
  `experiments/exp_g/config.toml`, not in the plan, and described in the draft as "default kernel".
- LIME 0.2.0.1 source: without a discretizer, samples are drawn around the training mean, the
  surrogate is a weighted ridge regression on `z = (x − m)/s`, and `as_map()` returns its
  coefficients: slopes per training standard deviation.
- Metrics M1–M6 (`removal_metrics`, `correlation_metric`, `infidelity_metric`) use the vector as
  signed contributions relative to the masking baseline; the synthetic truth is a contribution.
- Constructed demonstration (`docs/reports/paper_g/review/lime_semantics_demo.py`): LIME weights equal
  the slope per s.d. to 7e-4 and do not change with the instance; ρ(weight, contribution) ranges from
  −0.50 to +0.29; ρ(weight · z, contribution) = 1.000.
- Paper E had established and confirmed the same semantics on 2026-10-04 (sign agreement 0.945–0.990
  after conversion).

## Root cause

1. **Why were slopes scored as contributions?** Paper G's metrics were defined on signed
   contributions (plan section 10, 2026-11-14), and the explainer code was reused unchanged.
2. **Why was the reuse not checked?** No explainer declared what its output *is*; the plan's metric
   definitions assumed a contribution for every explainer without saying so.
3. **Why did Paper E's finding not reach Paper G?** It lived in Paper E's plan and README as a post-hoc
   note; no framework-level record (standard, guard or shared documentation) carried it forward.
4. **Why did tests not catch it?** The Paper G tests checked each metric on contribution-like inputs and
   each explainer in isolation; no test checked an explainer's output type against a metric's input
   type.
5. **Why did review not catch it?** The pre-run review and the power simulation examined the analysis,
   not the semantics of the inputs; the LIME settings were not in the configuration file reviewers read.

**Root cause:** explainer output semantics were implicit, so nothing could compare them with the
metrics' input assumptions, and a known incompatibility documented in one paper had no mechanism to
reach the next.

## Comparable assumptions elsewhere

- `src/xai/lime_tabular.py` also defaults to `discretize_continuous=False`. The framework metric
  `src/metrics/faithfulness.py` uses magnitudes (`np.abs(weights)`, `|drops|`), which is closer to
  treating slopes as unsigned importances; it is not changed here (shared path, other papers'
  frozen results) and is listed as a review trigger.
- Papers A–F: Paper E documented and handled the issue; Paper F used LIME rankings across datasets.
  A retrospective check of Paper F is outside this RCA and is left to the author.

## Corrective actions

- **Immediate:** the post-analysis review classified every LIME-involving Paper G result; the manuscript
  withdraws or qualifies the affected claims; the original outputs stay unchanged.
- **Permanent:** `scripts/paper_g_semantics.py` (PR #131), a machine-checked contract:
  - each explainer declares its output kind (local surrogate coefficient, discretised indicator
    weight, signed contribution, unsigned importance, random control), coordinates, reference and
    grouping; each metric declares the kinds it accepts;
  - `check()` refuses an incompatible pair unless a conversion or an alternative estimand is declared;
  - `lime_kind_of()` reads the kind from the live LIME object, so the declaration fails its test as
    soon as the code changes;
  - the frozen Paper G run passes only with its explicit "LIME as configured" declaration.
- **Supplementary:** S3 (plan 12.1) tests whether a contribution-valued LIME representation recovers the
  synthetic truth.

## Tests

`tests/analysis/test_paper_g_semantics.py` (12 tests): compatible pairs pass; LIME slopes into each of
M1–M6 are refused; LIME into M7 is refused for multi-column groups; declared conversions and estimands
are explicit and pair-specific; the frozen run fails without its declarations; the LIME declaration is
bound to the live configuration.

## Standard update

A new analysis plan states, for every explainer, what its attribution vector is (kind, coordinates,
reference) and, for every metric, what it requires; the contract module and its test are the
machine-checked form of that statement.
