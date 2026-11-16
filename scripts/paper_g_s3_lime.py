#!/usr/bin/env python3
"""Paper G S3: synthetic validation of LIME output representations (plan section 12.1).

    python scripts/paper_g_s3_lime.py --run --authorized "<who, date>"

Supplementary and exploratory. Rebuilds the four synthetic conditions with the frozen
`paper_g_synthetic.make_condition`, reproduces the frozen LIME weights of every instance (gate),
computes six LIME representations (2 x 2 design: discretisation x kernel width; slopes, reference-
relative contributions, discretised weights) and compares each with the stored exact Shapley
truth. Never writes to the frozen outputs; writes outputs/analysis/paper_g/supplementary/s3/ and
docs/reports/paper_g/S3_REPORT.md. Uses paper_g_lib and paper_g_synthetic read-only.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import math
import platform
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_g_lib as lib  # noqa: E402

RAW = lib.OUT / "raw" / "synthetic"
OUT = lib.OUT / "supplementary" / "s3"
REPORT = lib.ROOT / "docs" / "reports" / "paper_g" / "S3_REPORT.md"
REPRO_TOL = 1e-8
TRUTH_TOL = 1e-6        # stored true_attr is rounded to 8 decimals
CONFIGS = {"F3": (False, 3.0), "FD": (False, None), "T3": (True, 3.0), "TD": (True, None)}
REPRESENTATIONS = {   # id: (description, config, kind)
    "S3-A": ("slopes, frozen (stored attr)", "F3", "slope"),
    "S3-A-kd": ("slopes, default kernel width", "FD", "slope"),
    "S3-B": ("contributions w*(x-mu)/s, frozen fit", "F3", "contribution"),
    "S3-B-kd": ("contributions w*(x-mu)/s, default kernel width", "FD", "contribution"),
    "S3-C": ("discretised weights, width 3.0", "T3", "discretised"),
    "S3-C-kd": ("discretised weights, default kernel width", "TD", "discretised"),
}


# --- pure functions (tested) ---------------------------------------------------------------------

def to_contribution(w: np.ndarray, x: np.ndarray, mean: np.ndarray, scale: np.ndarray) -> np.ndarray:
    """Additive decomposition of LIME's linear surrogate relative to the training mean.

    LIME fits w on z = (x - mean) / scale (lime_tabular.py: scaled_data); the surrogate's change from
    the mean point to x is sum_j w_j z_j, so the contribution of j is w_j * z_j.
    """
    return np.asarray(w, float) * (np.asarray(x, float) - np.asarray(mean, float)) / np.asarray(scale, float)


def spearman_or_nan(a: np.ndarray, b: np.ndarray) -> float:
    """Spearman correlation; NaN (undefined, counted) if either vector is constant."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if np.ptp(a) == 0 or np.ptp(b) == 0:
        return math.nan
    return float(stats.spearmanr(a, b).statistic)


def instance_seed(seed: int, pos: int) -> int:
    """The frozen per-instance seed (paper_g_lib.explain_and_score)."""
    return (seed * 100003 + int(pos)) % (2**31)


# --- LIME configurations ---------------------------------------------------------------------------

class LimeConfig:
    """LIME as in paper_g_lib.Lime, except `discretize_continuous` and `kernel_width`."""

    def __init__(self, data: dict, seed: int, cfg: dict, discretize: bool, kernel_width):
        from lime.lime_tabular import LimeTabularExplainer
        c = cfg["explainers"]["lime"]
        self.d = data["X_train"].shape[1]
        self.num_samples = c["num_samples"]
        self.model = data["model"]
        self.lime = LimeTabularExplainer(
            data["X_train"], feature_names=data["names"], class_names=["0", "1"],
            mode="classification", discretize_continuous=discretize,
            kernel_width=kernel_width, random_state=seed)

    def explain(self, x: np.ndarray, seed: int) -> np.ndarray:
        self.lime.random_state = np.random.RandomState(seed % (2**32))
        exp = self.lime.explain_instance(x, self.model.predict_proba, labels=(1,),
                                         num_features=self.d, num_samples=self.num_samples)
        w = np.zeros(self.d)
        for j, value in exp.as_map()[1]:
            w[j] = value
        return w


def stored_records(path: Path) -> dict[tuple[int, str], dict]:
    out = {}
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            out[(r["instance"], r["explainer"])] = r
    return out


def run_block(generator: str, rho: float, seed: int, cfg: dict, stored: dict) -> tuple[list, list, dict]:
    """One condition x seed: reproduction rows, instance rows, reference check."""
    import paper_g_synthetic as syn  # noqa: F401  (also used for the truth check)
    data = syn.make_condition(generator, rho, seed, cfg)
    frozen = lib.make_explainer("lime", data["model"], data, seed, cfg)          # frozen F3 object
    variants = {k: LimeConfig(data, seed, cfg, *v) for k, v in CONFIGS.items() if k != "F3"}
    mu, scale = frozen.lime.scaler.mean_, frozen.lime.scaler.scale_
    cond = f"{generator}_rho{int(rho * 100):02d}"
    repro, rows = [], []
    truth_check = math.nan
    for k, pos in enumerate(data["instances"]):
        pos = int(pos)
        rec = stored[(pos, "lime")]
        x, c = data["X_test"][pos], int(data["pred"][pos])
        s = instance_seed(seed, pos)
        w_f3 = lib.orient(lib.group_attr(frozen.explain(x, s), data["groups"]), c)
        stored_attr = np.array(rec["attr"], float)
        err = float(np.max(np.abs(np.round(w_f3, 8) - stored_attr)))
        repro.append({"condition": cond, "seed": seed, "instance": pos, "max_abs_diff": err,
                      "reproduced": int(err <= REPRO_TOL), "pred_stored": rec["pred_class"], "pred_rebuilt": c})
        w = {k: lib.orient(v.explain(x, s), c) for k, v in variants.items()}
        vec = {"S3-A": stored_attr,
               "S3-A-kd": w["FD"],
               "S3-B": to_contribution(stored_attr, x, mu, scale),
               "S3-B-kd": to_contribution(w["FD"], x, variants["FD"].lime.scaler.mean_,
                                          variants["FD"].lime.scaler.scale_),
               "S3-C": w["T3"], "S3-C-kd": w["TD"]}
        truth = np.array(rec["true_attr"], float)
        if k == 0:   # independent check of the rebuilt condition against the stored truth
            truth_check = float(np.max(np.abs(syn.true_attribution(data, pos) - truth)))
        for rid, v in vec.items():
            rows.append({"condition": cond, "seed": seed, "instance": pos, "pred_class": c,
                         "representation": rid, "config": REPRESENTATIONS[rid][1],
                         "kind": REPRESENTATIONS[rid][2], "spearman_truth": spearman_or_nan(v, truth)})
    ref = {"condition": cond, "seed": seed,
           "max_abs_lime_mean_minus_truth_background_mean": float(np.max(np.abs(mu - data["truth_background"].mean(axis=0)))),
           "max_abs_lime_mean_minus_metric_baseline": float(np.max(np.abs(mu - data["base"]))),
           "lime_scale_min": float(scale.min()), "lime_scale_max": float(scale.max()),
           "truth_recomputed_first_instance_max_abs_diff": truth_check}
    return repro, rows, ref


# --- summaries and outputs ------------------------------------------------------------------------

def summarise(rows: list[dict]) -> tuple[list, list, list]:
    by_cs: dict = {}
    for r in rows:
        by_cs.setdefault((r["condition"], r["seed"], r["representation"]), []).append(r["spearman_truth"])
    cs = []
    for (cond, seed, rid), v in sorted(by_cs.items()):
        ok = [x for x in v if not math.isnan(x)]
        cs.append({"condition": cond, "seed": seed, "representation": rid, "instances": len(v),
                   "undefined": len(v) - len(ok), "mean_spearman_truth": float(np.mean(ok)) if ok else math.nan})
    by_c: dict = {}
    for r in cs:
        by_c.setdefault((r["condition"], r["representation"]), []).append(r["mean_spearman_truth"])
    cond = [{"condition": c, "representation": rid, "seeds": len(v), "mean_over_seeds": float(np.mean(v)),
             "min_seed": float(np.min(v)), "max_seed": float(np.max(v))} for (c, rid), v in sorted(by_c.items())]
    by_k: dict = {}
    for r in rows:
        by_k.setdefault((r["condition"], r["representation"], r["pred_class"]), []).append(r["spearman_truth"])
    cls = [{"condition": c, "representation": rid, "pred_class": k, "instances": len(v),
            "mean_spearman_truth": float(np.nanmean(v)) if not all(math.isnan(x) for x in v) else math.nan}
           for (c, rid, k), v in sorted(by_k.items())]
    return cs, cond, cls


def write_csv(path: Path, rows: list[dict], gz: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if gz:   # fixed header time, so identical content gives identical bytes
        raw = open(path, "wb")   # no file name or time in the gzip header
        fh = io.TextIOWrapper(gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0),
                              encoding="utf-8", newline="")
    else:
        fh = open(path, "w", encoding="utf-8", newline="")
    with fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.8f}" if isinstance(v, float) else v) for k, v in r.items()})
    if gz:
        raw.close()


def write_report(path: Path, cond: list, cls: list, refs: list, repro: list, prov: dict) -> None:
    L = ["# Paper G — S3 report: LIME representations against the synthetic truth", "",
         "Generated by `scripts/paper_g_s3_lime.py`; do not edit. Supplementary and exploratory "
         "(plan section 12.1); descriptive only; no representation is selected.", "",
         f"- code commit: {prov['code_commit']}; authorized: {prov['authorized']}",
         f"- reproduction gate: {prov['reproduced']} of {prov['reproduction_rows']} instances reproduce the "
         f"stored LIME weights within {REPRO_TOL} (max difference {prov['max_reproduction_diff']:.2e})",
         f"- truth check: the stored exact Shapley values of the first instance of every block are "
         f"recomputed by the frozen code; max difference {prov['truth_check_max_abs_diff']:.2e}",
         f"- instance rows: {prov['instance_rows']}; undefined correlations: {prov['undefined']}", "",
         "**Table S3-1. Mean Spearman correlation with the exact Shapley truth, per condition "
         "(mean over the 5 seeds of the per-seed means over 200 instances; range over seeds).**", "",
         "| condition | " + " | ".join(REPRESENTATIONS) + " |", "|---|" + "---|" * len(REPRESENTATIONS)]
    for c in sorted({r["condition"] for r in cond}):
        cells = []
        for rid in REPRESENTATIONS:
            r = next(x for x in cond if x["condition"] == c and x["representation"] == rid)
            cells.append(f"{r['mean_over_seeds']:.3f} [{r['min_seed']:.3f}, {r['max_seed']:.3f}]")
        L.append(f"| {c} | " + " | ".join(cells) + " |")
    L += ["", "Representations: " + "; ".join(f"**{k}** {v[0]}" for k, v in REPRESENTATIONS.items()) + ".", "",
          "**Table S3-2. By predicted class (mean over instances).**", "",
          "| condition | representation | class 0 | class 1 |", "|---|---|---|---|"]
    for c in sorted({r["condition"] for r in cls}):
        for rid in REPRESENTATIONS:
            v = {r["pred_class"]: r["mean_spearman_truth"] for r in cls if r["condition"] == c and r["representation"] == rid}
            L.append(f"| {c} | {rid} | {v.get(0, math.nan):.3f} | {v.get(1, math.nan):.3f} |")
    L += ["", "**Table S3-3. References (max over features; per condition x seed).**", "",
          "| condition | seed | LIME mean − truth background mean | LIME mean − metric baseline |", "|---|---|---|---|"]
    for r in refs:
        L.append(f"| {r['condition']} | {r['seed']} | {r['max_abs_lime_mean_minus_truth_background_mean']:.4f} | "
                 f"{r['max_abs_lime_mean_minus_metric_baseline']:.2e} |")
    L += ["", "Per condition x seed values: `supplementary/s3/s3_condition_seed.csv`; instance values: "
          "`s3_instances.csv.gz`.", ""]
    path.write_text("\n".join(L), encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--authorized", default="")
    a = ap.parse_args(argv)
    if not a.run or not a.authorized.strip():
        print("refused: S3 runs only with --run and an --authorized statement (plan 12.1)", file=sys.stderr)
        return 2
    import paper_g_run as run
    cfg = lib.config()
    repro, rows, refs = [], [], []
    for sh in run.shards("synthetic", cfg):
        stored = stored_records(RAW / f"{run.shard_name(sh)}.jsonl.gz")
        r1, r2, ref = run_block(sh["generator"], sh["rho"], sh["seed"], cfg, stored)
        bad = [r for r in r1 if not r["reproduced"] or r["pred_stored"] != r["pred_rebuilt"]]
        if not ref["truth_recomputed_first_instance_max_abs_diff"] <= TRUTH_TOL:
            bad.append({"truth": ref["truth_recomputed_first_instance_max_abs_diff"]})
        print(f"{run.shard_name(sh)}: reproduced {len(r1) - len(bad)}/{len(r1)}", flush=True)
        repro += r1
        if bad:
            write_csv(OUT / "s3_reproduction.csv", repro)
            print(f"STOP: reproduction gate failed in {run.shard_name(sh)} (plan 12.1)", file=sys.stderr)
            return 3
        rows += r2
        refs.append(ref)
    cs, cond, cls = summarise(rows)
    write_csv(OUT / "s3_reproduction.csv", repro)
    write_csv(OUT / "s3_instances.csv.gz", rows, gz=True)
    write_csv(OUT / "s3_condition_seed.csv", cs)
    write_csv(OUT / "s3_condition.csv", cond)
    write_csv(OUT / "s3_by_class.csv", cls)
    write_csv(OUT / "s3_reference.csv", refs)
    import lime
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=lib.ROOT, capture_output=True, text=True).stdout.strip()
    prov = {"authorized": a.authorized, "code_commit": commit, "python": platform.python_version(),
            "numpy": np.__version__, "lime": getattr(lime, "__version__", "0.2.0.1"),
            "reproduction_rows": len(repro), "reproduced": sum(r["reproduced"] for r in repro),
            "truth_check_max_abs_diff": max(r["truth_recomputed_first_instance_max_abs_diff"] for r in refs),
            "max_reproduction_diff": max(r["max_abs_diff"] for r in repro),
            "instance_rows": len(rows), "undefined": sum(math.isnan(r["spearman_truth"]) for r in rows),
            "files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob("s3_*"))}}
    (OUT / "s3_provenance.json").write_text(json.dumps(prov, indent=1), encoding="utf-8")
    write_report(REPORT, cond, cls, refs, repro, prov)
    print(json.dumps({k: v for k, v in prov.items() if k != "files"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
