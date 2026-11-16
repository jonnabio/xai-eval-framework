#!/usr/bin/env python3
"""Paper G S1: supplementary analysis (plan section 12.3.4). Descriptive; no test; no decision rule.

    python scripts/paper_g_s1_analyze.py --run --authorized "<who, date>"

Reads the frozen instance and ROAR-lite rows and the verified S1 shards; for each condition
(original, S1-B, S1-M) keeps every SHAP, occlusion and random row unchanged and replaces only LIME's
rows, then applies the frozen functions of scripts/paper_g_analyze.py and paper_g_diagnostics.py.
The original condition is recomputed as a check: it must reproduce the frozen H1/H2 outputs.
Writes outputs/analysis/paper_g/supplementary/s1/analysis/ and docs/reports/paper_g/S1_ANALYSIS_REPORT.md.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_g_analyze as an  # noqa: E402
import paper_g_diagnostics as dg  # noqa: E402
import paper_g_lib as lib  # noqa: E402

S1 = lib.OUT / "supplementary" / "s1"
OUT = S1 / "analysis"
REPORT = lib.ROOT / "docs" / "reports" / "paper_g" / "S1_ANALYSIS_REPORT.md"
FROZEN = lib.OUT / "analysis" / "confirmatory"
M6 = list(lib.INSTANCE_METRICS)
M7 = M6 + ["m7_roar"]
B2 = {"m1_deletion": "m1_deletion_b2", "m2_insertion": "m2_insertion_b2", "m3_gap": "m3_gap_b2",
      "m6_sufficiency": "m6_sufficiency_b2"}
STUDIED, ALL = ["shap", "lime", "occlusion"], ["shap", "lime", "occlusion", "random"]
CHECK_TOL = 5e-7            # frozen CSVs carry six decimals
CONDITIONS = ("original", "S1-B", "S1-M")


class S1AnalysisError(RuntimeError):
    pass


# --- loading ----------------------------------------------------------------------------------------

def load_frozen(raw: Path = lib.OUT / "raw") -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = an.read_manifest(raw)
    an.check_manifest(rows, raw)
    keep_f = an.BLOCK + ["explainer", "instance", "m4_degenerate", "f_x", *M6, *B2.values()]
    full, roar = [], []
    for r in sorted(rows, key=lambda r: r["path"]):
        st = r["path"].split("/")[0]
        if st not in ("full", "roar"):
            continue
        with gzip.open(raw / r["path"], "rt", encoding="utf-8") as fh:
            for line in fh:
                x = json.loads(line)
                (full if st == "full" else roar).append(
                    {k: x[k] for k in (keep_f if st == "full" else an.BLOCK + ["explainer", "m7_roar"])})
    return pd.DataFrame(full), pd.DataFrame(roar)


def load_s1(s1: Path = S1) -> dict:
    """The S1 shards, each verified against MANIFEST.csv; rows, M7 and block checks."""
    with open(s1 / "MANIFEST.csv", encoding="utf-8") as fh:
        man = list(csv.DictReader(fh))
    rows, m7, checks = [], [], []
    for r in man:
        data = (s1 / r["path"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != r["sha256"]:
            raise S1AnalysisError(f"hash mismatch: {r['path']}")
        res = json.loads(gzip.decompress(data))
        meta = res["meta"]
        rows += res["rows"]
        m7 += [{**x, "dataset": meta["dataset"], "model": meta["model"], "seed": meta["seed"]} for x in res["m7"]]
        checks += [{**c, "seed": meta["seed"]} for c in res["checks"]]
    return {"rows": rows, "m7": pd.DataFrame(m7), "checks": pd.DataFrame(checks), "blocks": len(man)}


# --- conditions ----------------------------------------------------------------------------------------

def condition(full: pd.DataFrame, roar: pd.DataFrame, s1: dict, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Instance and ROAR rows for one condition: LIME's rows replaced, all others as frozen."""
    if name == "original":
        return full, roar
    import paper_g_s1_lime as s1mod
    f = s1mod.substitute_lime(full[[c for c in full.columns]], s1["rows"], name)
    m = s1["m7"][s1["m7"]["representation"] == name][an.BLOCK + ["m7_roar"]]
    r = roar.merge(m.rename(columns={"m7_roar": "s1"}), on=an.BLOCK, how="left")
    is_lime = r["explainer"] == "lime"
    if r.loc[is_lime, "s1"].isna().any():
        raise S1AnalysisError(f"{name}: M7 missing for some LIME block")
    r.loc[is_lime, "m7_roar"] = r.loc[is_lime, "s1"]
    return f, r.drop(columns="s1")


def system(full: pd.DataFrame, roar: pd.DataFrame, baseline2: bool = False) -> pd.DataFrame:
    cols = [B2.get(m, m) if baseline2 else m for m in M6]
    means = an.block_means(full, cols)
    if baseline2:
        means = means.rename(columns={v: k for k, v in B2.items()})
    return an.system_table(means, roar[an.BLOCK + ["explainer", "m7_roar"]])


def _est(ti: dict) -> dict:
    return {"mean": ti["mean"], "lo": ti["lo"], "hi": ti["hi"], "n": ti["n"]}


def h2_estimates(full: pd.DataFrame, explainers: list[str]) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    blocks = an.h2_blocks(full, explainers, M6)
    pairs = [c for c in blocks.columns if "|" in c and not c.startswith("n|")]
    ds = blocks.groupby("dataset")[["omnibus", *pairs]].mean().reset_index()
    ptab = pd.DataFrame([{"pair": p, **_est(an.t_interval(ds[p]))} for p in pairs])
    return _est(an.t_interval(ds["omnibus"])), ds, ptab


def analyse_condition(full: pd.DataFrame, roar: pd.DataFrame, spec: dict) -> dict:
    sys_t, sys_b2 = system(full, roar), system(full, roar, baseline2=True)
    res = {}
    for key, tab, expl, mets in (("h1", sys_t, STUDIED, M7), ("h1_four", sys_t, ALL, M7),
                                 ("h1_baseline2", sys_b2, STUDIED, M7),
                                 ("h1_six_metrics", sys_t, STUDIED, [m for m in M7 if m != "m4_corr"])):
        r = an.h1_analysis(tab, expl, mets, spec, test=False)
        res[key] = {"spearman": _est(r["spearman"]), "w": _est(r["w"]), "datasets": r["datasets_spearman"],
                    "datasets_w": r["datasets_w"], "undefined_pairs": int(r["blocks"]["pairs_undefined"].sum())}
    res["stability"] = an.stability_benchmark(sys_t, STUDIED, M7)
    res["positions"] = dg.r3(sys_t)
    res["random_last"] = dg.r11(sys_t)
    res["flips"] = an.winner_flips(sys_t, STUDIED, M7)
    res["shap_lime"], res["shap_lime_any"] = an.shap_lime_reversals(sys_t, M7)
    res["h2"], res["h2_datasets"], res["h2_pairs"] = h2_estimates(full, ALL)
    res["h2_three"], _, _ = h2_estimates(full, STUDIED)
    res["h2_adjusted"] = dg.r6(full)["summary"]
    res["lime_m7"] = roar[roar["explainer"] == "lime"][an.BLOCK + ["m7_roar"]].reset_index(drop=True)
    return res


def check_original(res: dict, frozen: Path = FROZEN) -> float:
    """The original condition must reproduce the frozen H1 and H2 estimates (six-decimal CSVs)."""
    h1 = pd.read_csv(frozen / "h1_summary.csv").set_index("analysis")
    om = pd.read_csv(frozen / "h2_omnibus.csv").iloc[0]
    diffs = [abs(res["h1"]["spearman"][k] - h1.loc["mean pairwise Spearman", k]) for k in ("mean", "lo", "hi")]
    diffs += [abs(res["h1"]["w"][k] - h1.loc["Kendall W", k]) for k in ("mean", "lo", "hi")]
    diffs += [abs(res["h2"][k] - om[k]) for k in ("mean", "lo", "hi")]
    return float(max(diffs))


# --- outputs ---------------------------------------------------------------------------------------------

def _csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, float_format="%.6f", lineterminator="\n")


def comparison(results: dict) -> pd.DataFrame:
    rows = []
    for label, key, sub in (("H1 mean pairwise Spearman (3 explainers, 7 metrics)", "h1", "spearman"),
                            ("H1 Kendall W", "h1", "w"),
                            ("H1 four explainers (Spearman)", "h1_four", "spearman"),
                            ("H1 second baseline (Spearman)", "h1_baseline2", "spearman"),
                            ("H1 six metrics, no M4 (Spearman)", "h1_six_metrics", "spearman"),
                            ("H2 omnibus (4 explainers)", "h2", None), ("H2 omnibus (3 studied)", "h2_three", None)):
        for c, r in results.items():
            v = r[key][sub] if sub else r[key]
            rows.append({"quantity": label, "condition": c, **v})
    for c, r in results.items():
        s = r["stability"]["summary"]
        rows.append({"quantity": "within-metric stability benchmark", "condition": c, **_est(s)})
        adj = r["h2_adjusted"].set_index("pair").loc["omnibus"]
        rows.append({"quantity": "H2 omnibus adjusted for f_x (exploratory)", "condition": c,
                     "mean": adj["adjusted_mean"], "lo": adj["adjusted_lo"], "hi": adj["adjusted_hi"], "n": 8})
    return pd.DataFrame(rows)


def dataset_table(results: dict, checks: pd.DataFrame) -> pd.DataFrame:
    kind = checks.groupby("dataset")["categorical_groups"].max().map({0: "numeric", 1: "mixed"})
    rows = []
    for c, r in results.items():
        for _, x in r["h1"]["datasets"].iterrows():
            rows.append({"dataset": x["dataset"], "type": kind.get(x["dataset"], "?"), "condition": c,
                         "h1_spearman": x["mean"]})
    t = pd.DataFrame(rows).pivot_table(index=["dataset", "type"], columns="condition", values="h1_spearman").reset_index()
    return t[["dataset", "type", *CONDITIONS]]


def write_all(results: dict, s1: dict, out: Path, report: Path, header: dict) -> pd.DataFrame:
    comp = comparison(results)
    _csv(comp, out / "comparison_summary.csv")
    ds = dataset_table(results, s1["checks"])
    _csv(ds, out / "comparison_by_dataset.csv")
    for c, r in results.items():
        tag = c.replace("-", "").lower()
        _csv(r["h1"]["datasets"], out / tag / "h1_datasets.csv")
        _csv(r["positions"]["summary"], out / tag / "positions_summary.csv")
        _csv(r["positions"]["positions_by_metric"], out / tag / "positions_by_metric.csv")
        _csv(r["positions"]["shap_occlusion_datasets"], out / tag / "shap_occlusion_by_dataset.csv")
        _csv(r["random_last"]["summary"], out / tag / "random_last.csv")
        _csv(r["flips"], out / tag / "winner_flips.csv")
        _csv(r["shap_lime"], out / tag / "shap_lime_reversals.csv")
        _csv(pd.DataFrame([r["shap_lime_any"]]), out / tag / "shap_lime_any.csv")
        _csv(r["h2_pairs"], out / tag / "h2_pairs.csv")
        _csv(r["h2_adjusted"], out / tag / "h2_adjusted.csv")
        _csv(r["stability"]["dataset_metric"].groupby("metric")["mean"].mean().reset_index(), out / tag / "stability_by_metric.csv")
        _csv(r["lime_m7"], out / tag / "lime_m7.csv")
    m = results["original"]["lime_m7"].merge(results["S1-B"]["lime_m7"], on=an.BLOCK, suffixes=("_original", "_s1b")) \
        .merge(results["S1-M"]["lime_m7"].rename(columns={"m7_roar": "m7_roar_s1m"}), on=an.BLOCK)
    _csv(m, out / "lime_m7_by_block.csv")
    write_report(results, comp, ds, report, header)
    return comp


def _md(df: pd.DataFrame, nd: int = 3) -> str:
    out = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(f"{v:.{nd}f}" if isinstance(v, float) else str(v) for v in r) + " |")
    return "\n".join(out)


def write_report(results: dict, comp: pd.DataFrame, ds: pd.DataFrame, path: Path, header: dict) -> None:
    L = ["# Paper G — S1 supplementary analysis", "",
         "Generated by `scripts/paper_g_s1_analyze.py`; do not edit. **Supplementary and exploratory** "
         "(plan 12.3.4): estimates and 95% t-intervals over the eight datasets; no test, no decision rule, no "
         "preferred representation. The original condition is recomputed from the frozen rows as a check.", ""]
    L += [f"- {k}: {v}" for k, v in header.items()]
    wide = comp.pivot_table(index="quantity", columns="condition", values="mean", sort=False)[list(CONDITIONS)].reset_index()
    L += ["", "**Table S1-1. Original versus S1-B (primary supplementary) versus S1-M (sensitivity): means.**", "",
          _md(wide), "", "**Table S1-2. The same with 95% intervals.**", "",
          _md(comp[["quantity", "condition", "mean", "lo", "hi"]]), "",
          "**Table S1-3. H1 mean pairwise Spearman per dataset.**", "", _md(ds), ""]
    for c in CONDITIONS:
        r = results[c]
        L += [f"## {c}", "", "Explainer positions (three studied explainers, seven metrics):", "",
              _md(r["positions"]["summary"]), "", "Untied ranks per metric:", "",
              _md(r["positions"]["positions_by_metric"]), "",
              f"SHAP–LIME: blocks with at least one strict reversal {r['shap_lime_any']['blocks_with_any_strict_reversal']} "
              f"of {r['shap_lime_any']['blocks']}.", "", _md(r["shap_lime"][["metric_a", "metric_b", "reversal_share", "tie_share"]]), "",
              "Winner flips:", "", _md(r["flips"][["metric_a", "metric_b", "flip_share", "tie_share"]]), "",
              "Random control last under all seven metrics:", "", _md(r["random_last"]["summary"]), "",
              "Within-metric stability by metric:", "",
              _md(r["stability"]["dataset_metric"].groupby("metric")["mean"].mean().reset_index()), "",
              "H2 pairs (4 explainers):", "", _md(r["h2_pairs"]), ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L), encoding="utf-8")


def run(authorized: str) -> int:
    spec = an.load_spec()
    full, roar = load_frozen()
    s1 = load_s1()
    if s1["blocks"] != 160 or len(s1["rows"]) != 160 * 200 * 2:
        raise S1AnalysisError(f"S1 coverage: {s1['blocks']} blocks, {len(s1['rows'])} rows")
    results = {c: analyse_condition(*condition(full, roar, s1, c), spec) for c in CONDITIONS}
    gap = check_original(results["original"])
    if gap > CHECK_TOL:
        raise S1AnalysisError(f"original condition differs from the frozen outputs by {gap:.2e}")
    import subprocess
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=lib.ROOT, capture_output=True, text=True).stdout.strip()
    write_all(results, s1, OUT, REPORT, {"authorized": authorized, "code commit": commit,
                                          "original-condition check (max |recomputed − frozen|)": f"{gap:.1e}",
                                          "S1 blocks": s1["blocks"], "S1 instance rows": len(s1["rows"])})
    print(f"S1 analysis written to {OUT} and {REPORT}; original check {gap:.1e}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--authorized", default="")
    a = ap.parse_args(argv)
    if not a.run or not a.authorized.strip():
        print("refused: the S1 analysis runs only with --run and an --authorized statement", file=sys.stderr)
        return 2
    try:
        return run(a.authorized)
    except (S1AnalysisError, an.ValidationError) as exc:
        print(f"STOP: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
