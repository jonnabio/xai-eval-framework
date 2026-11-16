#!/usr/bin/env python3
"""Paper G: semantic contract between explainer outputs and metric inputs (RCA-005 guard).

Every explainer declares what its attribution vector *is*; every metric declares what it *needs*.
`check` refuses an incompatible pair unless a conversion or an alternative estimand is declared
explicitly. `lime_kind_of` reads the kind from a live LIME object, so the declaration cannot drift
from the code (tests/analysis/test_paper_g_semantics.py).
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Kind(Enum):
    LOCAL_SURROGATE_COEFFICIENT = "local surrogate coefficient (slope; sign = direction of change)"
    DISCRETISED_INDICATOR_WEIGHT = "weight of the instance's bin indicator in a local surrogate"
    SIGNED_CONTRIBUTION = "signed contribution of the feature's value relative to a reference"
    UNSIGNED_IMPORTANCE = "unsigned global importance"
    RANDOM_CONTROL = "random scores (negative control)"


@dataclass(frozen=True)
class Output:
    kind: Kind
    coordinates: str          # where the values live before grouping
    reference: str | None     # what a contribution is relative to
    grouping: str             # how encoded columns become feature groups


@dataclass(frozen=True)
class Requirement:
    accepts: frozenset        # kinds the metric can consume as intended
    uses_sign: bool
    reference: str | None     # the metric's own reference (masking baseline)
    groups_by: str


@dataclass(frozen=True)
class Verdict:
    status: str               # "compatible" | "converted" | "declared alternative estimand"
    note: str


class IncompatibleSemantics(ValueError):
    """An explainer output is fed to a metric that assumes another quantity, with nothing declared."""


# --- Paper G declarations (code: scripts/paper_g_lib.py) ----------------------------------------------

EXPLAINERS = {
    "shap": Output(Kind.SIGNED_CONTRIBUTION, "encoded columns", "expected output over a background sample",
                   "sum over the group's columns"),
    "occlusion": Output(Kind.SIGNED_CONTRIBUTION, "feature groups", "metric baseline (training mean / mode)",
                        "one value per group"),
    "lime": Output(Kind.LOCAL_SURROGATE_COEFFICIENT, "encoded columns standardised by LIME's own scaler",
                   None, "sum over the group's columns"),
    "random": Output(Kind.RANDOM_CONTROL, "feature groups", None, "one value per group"),
}

_CONTRIB = frozenset({Kind.SIGNED_CONTRIBUTION, Kind.RANDOM_CONTROL})
METRICS = {
    "m1_deletion": Requirement(_CONTRIB, True, "metric baseline", "feature groups"),
    "m2_insertion": Requirement(_CONTRIB, True, "metric baseline", "feature groups"),
    "m3_gap": Requirement(_CONTRIB, True, "metric baseline", "feature groups"),
    "m4_corr": Requirement(_CONTRIB, True, "metric baseline", "feature groups"),
    "m5_infidelity": Requirement(_CONTRIB, True, "metric baseline", "feature groups"),
    "m6_sufficiency": Requirement(_CONTRIB, True, "metric baseline", "feature groups"),
    # M7 ranks by mean |a|: magnitudes only. A coefficient's magnitude is an importance only while a
    # group is a single column; a sum of one-hot slopes is not an importance.
    "m7_roar": Requirement(frozenset({Kind.SIGNED_CONTRIBUTION, Kind.UNSIGNED_IMPORTANCE, Kind.RANDOM_CONTROL,
                                      Kind.LOCAL_SURROGATE_COEFFICIENT}), False, None, "feature groups"),
}

CONVERSIONS = {
    (Kind.LOCAL_SURROGATE_COEFFICIENT, Kind.SIGNED_CONTRIBUTION):
        "c_j = w_j (x_j - mu_j) / s_j with LIME's fitted mean and scale; relative to the training mean "
        "(equal to the metric baseline for numeric features, not for categorical groups)",
}

# The frozen Paper G run fed LIME slopes to M1-M6. It is admissible only as an explicitly named
# alternative estimand ("LIME as configured"), never as the intended contribution comparison.
PAPER_G_FROZEN_DECLARATIONS = {("lime", m): "LIME as configured: slopes scored as if contributions "
                               "(ANALYSIS_PLAN.md 12; post-analysis review section 2)" for m in
                               ("m1_deletion", "m2_insertion", "m3_gap", "m4_corr", "m5_infidelity", "m6_sufficiency")}


def check(explainer: str, metric: str, *, multi_column_groups: bool, conversion: bool = False,
          declared: dict | None = None) -> Verdict:
    out, req = EXPLAINERS[explainer], METRICS[metric]
    kind, note = out.kind, ""
    if conversion:
        key = (kind, Kind.SIGNED_CONTRIBUTION)
        if key not in CONVERSIONS:
            raise IncompatibleSemantics(f"no declared conversion from {kind.name} for {explainer}")
        kind, note = Kind.SIGNED_CONTRIBUTION, CONVERSIONS[key]
    ok = kind in req.accepts
    if ok and kind is Kind.LOCAL_SURROGATE_COEFFICIENT and multi_column_groups:
        ok, note = False, "summed coefficients of a multi-column group are not an importance"
    if ok:
        return Verdict("converted" if conversion else "compatible", note)
    reason = (declared or {}).get((explainer, metric))
    if reason:
        return Verdict("declared alternative estimand", reason)
    raise IncompatibleSemantics(
        f"{explainer} outputs {kind.name} ({out.coordinates}); {metric} needs one of "
        f"{sorted(k.name for k in req.accepts)}{'; ' + note if note else ''}. Declare a conversion or an "
        "alternative estimand explicitly.")


def audit(explainers, metrics, *, multi_column_groups: bool, declared: dict | None = None) -> list[dict]:
    """Every pair, or an IncompatibleSemantics for the first undeclared incompatible one."""
    return [{"explainer": e, "metric": m,
             **check(e, m, multi_column_groups=multi_column_groups, declared=declared).__dict__}
            for e in explainers for m in metrics]


def lime_kind_of(lime_explainer) -> Kind:
    """The kind a configured `LimeTabularExplainer` returns (no discretizer: slopes)."""
    return Kind.LOCAL_SURROGATE_COEFFICIENT if lime_explainer.discretizer is None else Kind.DISCRETISED_INDICATOR_WEIGHT
