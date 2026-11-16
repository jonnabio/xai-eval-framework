#!/usr/bin/env python3
"""Paper G exploratory diagnostics R3, R6, R7, R11 on the frozen data (plan section 12.2).

    python scripts/paper_g_diagnostics.py --run --authorized "<who, date>"

Exploratory. Reuses the frozen conventions of scripts/paper_g_analyze.py (orientation, average
ranks, block means, M7 at system level) read-only; never writes to the confirmatory outputs.
Writes outputs/analysis/paper_g/exploratory_post/ and docs/reports/paper_g/DIAGNOSTICS_REPORT.md.
"""
from __future__ import annotations

import argparse
import gzip
import itertools
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_g_analyze as an  # noqa: E402
import paper_g_lib as lib  # noqa: E402

OUT = lib.OUT / "exploratory_post"
REPORT = lib.ROOT / "docs" / "reports" / "paper_g" / "DIAGNOSTICS_REPORT.md"
FROZEN = lib.OUT / "analysis" / "confirmatory"
M6 = list(lib.INSTANCE_METRICS)
M7 = M6 + ["m7_roar"]
STUDIED = ["shap", "lime", "occlusion"]
ALL = STUDIED + ["random"]
H2_TOL = 5e-7


# --- loading (fields beyond the frozen analysis loader: f_x and global_rank) -----------------------

def load(raw: Path = lib.OUT / "raw") -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = an.read_manifest(raw)
    an.check_manifest(rows, raw)
    full, roar = [], []
    for r in sorted(rows, key=lambda r: r["path"]):
        stage = r["path"].split("/")[0]
        if stage not in ("full", "roar"):
            continue
        with gzip.open(raw / r["path"], "rt", encoding="utf-8") as fh:
            for line in fh:
                x = json.loads(line)
                if stage == "full":
                    full.append({k: x[k] for k in an.BLOCK + ["explainer", "instance", "m4_degenerate", "f_x", *M6]})
                else:
                    roar.append({k: x[k] for k in an.BLOCK + ["explainer", "m7_roar", "global_rank"]})
    return pd.DataFrame(full), pd.DataFrame(roar)


# --- R3: explainer rank positions --------------------------------------------------------------------

def r3(sys_tab: pd.DataFrame) -> dict:
    pos_rows, block_rows, so_rows = [], [], []
    for key, g in sys_tab.groupby(an.BLOCK):
        R = an.rank_matrix(g, STUDIED, M7)                       # 7 x 3, average ranks, 1 = best
        b = g.set_index("explainer")
        for j, m in enumerate(M7):
            for i, e in enumerate(STUDIED):
                tied = int((R[j] == R[j, i]).sum() > 1)
                pos_rows.append({"dataset": key[0], "metric": m, "explainer": e, "tied": tied,
                                 "rank": None if tied else int(R[j, i])})
        extreme = [(e, p) for i, e in enumerate(STUDIED) for p in (1, 3)
                   if all(R[j, i] == p and (R[j] == p).sum() == 1 for j in range(len(M7)))]
        signs = [float(np.sign(an.oriented(b.loc["shap", m], m) - an.oriented(b.loc["occlusion", m], m))) for m in M7]
        pairs = list(itertools.combinations(range(len(M7)), 2))
        agree = sum(1 for a, c in pairs if signs[a] != 0 and signs[a] == signs[c])
        block_rows.append({**dict(zip(an.BLOCK, key)),
                           "extreme_explainer": extreme[0][0] if extreme else "",
                           "extreme_position": extreme[0][1] if extreme else "",
                           "consistently_last": next((e for e, p in extreme if p == 3), "")})
        so_rows.append({**dict(zip(an.BLOCK, key)), "pair_agreement_share": agree / len(pairs),
                        "all_seven_same_order": int(len(set(signs)) == 1 and signs[0] != 0),
                        "ties": int(sum(s == 0 for s in signs))})
    pos = pd.DataFrame(pos_rows)
    counts = (pos.assign(r1=pos["rank"].eq(1), r2=pos["rank"].eq(2), r3=pos["rank"].eq(3))
              .groupby(["dataset", "metric", "explainer"])[["r1", "r2", "r3", "tied"]].sum().reset_index())
    blocks = pd.DataFrame(block_rows)
    so = pd.DataFrame(so_rows)
    n = len(blocks)
    summary = pd.DataFrame([
        {"quantity": "blocks", "value": n},
        {"quantity": "blocks with one explainer at the same untied extreme rank under all 7 metrics",
         "value": int((blocks["extreme_explainer"] != "").sum())},
        *[{"quantity": f"... of which {e} last", "value": int((blocks["consistently_last"] == e).sum())} for e in STUDIED],
        *[{"quantity": f"... of which {e} first", "value": int(((blocks["extreme_explainer"] == e)
                                                                 & (blocks["extreme_position"] == 1)).sum())} for e in STUDIED],
        {"quantity": "SHAP vs occlusion: mean share of the 21 metric pairs with the same order", "value": so["pair_agreement_share"].mean()},
        {"quantity": "SHAP vs occlusion: blocks with the same order under all 7 metrics", "value": int(so["all_seven_same_order"].sum())},
    ])
    by_metric = counts.groupby(["metric", "explainer"])[["r1", "r2", "r3", "tied"]].sum().reset_index()
    return {"positions": counts, "positions_by_metric": by_metric, "blocks": blocks,
            "shap_occlusion": so, "shap_occlusion_datasets": so.groupby("dataset")[["pair_agreement_share", "all_seven_same_order"]].mean().reset_index(),
            "summary": summary}


# --- R6: H2 adjusted for prediction level ----------------------------------------------------------

def residual_rank(y_rank: np.ndarray, f_rank: np.ndarray) -> np.ndarray:
    X = np.column_stack([np.ones_like(f_rank), f_rank])
    coef, *_ = np.linalg.lstsq(X, y_rank, rcond=None)
    return y_rank - X @ coef


def partial_spearman(a: np.ndarray, b: np.ndarray, f: np.ndarray) -> float:
    """Pearson correlation of rank residuals after OLS on rank(f) (with intercept); NaN if undefined."""
    ra, rb, rf = stats.rankdata(a), stats.rankdata(b), stats.rankdata(f)
    ea, eb = residual_rank(ra, rf), residual_rank(rb, rf)
    if np.std(ea) < 1e-12 or np.std(eb) < 1e-12:
        return math.nan
    return float(np.corrcoef(ea, eb)[0, 1])


def r6(full: pd.DataFrame) -> dict:
    pairs = list(itertools.combinations(M6, 2))
    rows = []
    for key, g in full.groupby(an.BLOCK + ["explainer"]):
        g = g.sort_values("instance")
        f = g["f_x"].to_numpy(float)
        row = dict(zip(an.BLOCK + ["explainer"], key))
        for a, b in pairs:
            x, y = an.oriented(g[a].to_numpy(float), a), an.oriented(g[b].to_numpy(float), b)
            row[f"raw|{a}|{b}"] = an.spearman_of_ranks(stats.rankdata(x), stats.rankdata(y))
            row[f"adj|{a}|{b}"] = partial_spearman(x, y, f)
        rows.append(row)
    blocks = pd.DataFrame(rows)
    for kind in ("raw", "adj"):
        blocks[f"{kind}|omnibus"] = blocks[[f"{kind}|{a}|{b}" for a, b in pairs]].mean(axis=1, skipna=True)
    cols = [c for c in blocks.columns if "|" in c]
    ds = blocks.groupby("dataset")[cols].mean().reset_index()
    summ = []
    for name in ["omnibus"] + [f"{a}|{b}" for a, b in pairs]:
        r, j = an.t_interval(ds[f"raw|{name}"]), an.t_interval(ds[f"adj|{name}"])
        summ.append({"pair": name, "unadjusted_mean": r["mean"], "unadjusted_lo": r["lo"], "unadjusted_hi": r["hi"],
                     "adjusted_mean": j["mean"], "adjusted_lo": j["lo"], "adjusted_hi": j["hi"],
                     "adjusted_undefined_blocks": int(blocks[f"adj|{name}"].isna().sum()) if name != "omnibus" else 0})
    return {"blocks": blocks, "datasets": ds, "summary": pd.DataFrame(summ)}


def validate_r6_against_frozen(summary: pd.DataFrame, frozen: Path = FROZEN) -> float:
    """Max |unadjusted - frozen H2| over the omnibus and the 15 pairs (frozen CSV: six decimals)."""
    om = pd.read_csv(frozen / "h2_omnibus.csv").iloc[0]
    pairs = pd.read_csv(frozen / "h2_pairs.csv").set_index("pair")
    s = summary.set_index("pair")
    diffs = [abs(s.loc["omnibus", "unadjusted_mean"] - om["mean"]), abs(s.loc["omnibus", "unadjusted_lo"] - om["lo"])]
    diffs += [abs(s.loc[p, "unadjusted_mean"] - pairs.loc[p, "mean"]) for p in pairs.index]
    return float(max(diffs))


# --- R7: M7 structure ---------------------------------------------------------------------------------

def r7(roar: pd.DataFrame, levels: list[float]) -> dict:
    sizes = roar.assign(G=roar["global_rank"].map(len)).groupby("dataset")["G"].agg(["min", "max"])
    if (sizes["min"] != sizes["max"]).any():
        raise an.ValidationError("a dataset has global rankings of different lengths")
    grp = pd.DataFrame([{"dataset": d, "G": int(G), **{f"k_{lv}": lib.n_top(int(G), lv) for lv in levels}}
                        for d, G in sizes["min"].items()])
    rows, ties = [], []
    for key, g in roar[roar["explainer"].isin(STUDIED)].groupby(an.BLOCK):
        b = g.set_index("explainer")
        G = len(b.loc["shap", "global_rank"])
        for lv in levels:
            k = lib.n_top(G, lv)
            sets = [frozenset(b.loc[e, "global_rank"][:k]) for e in STUDIED]
            same = sum(1 for a, c in itertools.combinations(sets, 2) if a == c)
            rows.append({**dict(zip(an.BLOCK, key)), "level": lv, "k": k, "identical_pairs": same,
                         "all_three_identical": int(len(set(sets)) == 1)})
        m7 = b.loc[STUDIED, "m7_roar"].to_numpy(float)
        ties.append({**dict(zip(an.BLOCK, key)),
                     "any_equal_pair": int(any(m7[i] == m7[j] for i, j in itertools.combinations(range(3), 2))),
                     "top_tied": int((m7 == m7.max()).sum() > 1)})
    rs, tie = pd.DataFrame(rows), pd.DataFrame(ties)
    by_ds = (rs.assign(any_identical=rs["identical_pairs"].gt(0)).groupby(["dataset", "level"])
             [["any_identical", "all_three_identical"]].mean().reset_index())
    return {"groups": grp, "removal_sets": rs, "removal_by_dataset": by_ds, "ties": tie,
            "ties_by_dataset": tie.groupby("dataset")[["any_equal_pair", "top_tied"]].mean().reset_index(),
            "ties_by_model": tie.groupby("model")[["any_equal_pair", "top_tied"]].mean().reset_index()}


# --- R11: random control last --------------------------------------------------------------------------

def r11(sys_tab: pd.DataFrame) -> dict:
    rows = []
    for key, g in sys_tab.groupby(an.BLOCK):
        R = an.rank_matrix(g, ALL, M7)                            # 7 x 4
        i = ALL.index("random")
        untied = [bool(R[j, i] == 4 and (R[j] == 4).sum() == 1) for j in range(len(M7))]
        last_or_tied = [bool(R[j, i] == R[j].max()) for j in range(len(M7))]
        rows.append({**dict(zip(an.BLOCK, key)), **{f"untied_last|{m}": int(u) for m, u in zip(M7, untied)},
                     "untied_last_all7": int(all(untied)), "last_or_tied_all7": int(all(last_or_tied))})
    b = pd.DataFrame(rows)
    per_metric = pd.DataFrame([{"metric": m, "share_untied_last": b[f"untied_last|{m}"].mean()} for m in M7])
    summary = pd.DataFrame([{"denominator_blocks": len(b), "untied_last_all7": int(b["untied_last_all7"].sum()),
                             "share_untied_last_all7": b["untied_last_all7"].mean(),
                             "last_or_tied_all7": int(b["last_or_tied_all7"].sum()),
                             "share_last_or_tied_all7": b["last_or_tied_all7"].mean()}])
    return {"blocks": b, "per_metric": per_metric, "summary": summary}


# --- outputs ----------------------------------------------------------------------------------------

def _csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, float_format="%.6f", lineterminator="\n")


def run_all(full: pd.DataFrame, roar: pd.DataFrame, out: Path, report: Path, header: dict,
            levels: list[float], frozen: Path | None = FROZEN) -> dict:
    sys_tab = an.system_table(an.block_means(full, M6), roar[an.BLOCK + ["explainer", "m7_roar"]])
    res = {"r3": r3(sys_tab), "r6": r6(full), "r7": r7(roar, levels), "r11": r11(sys_tab)}
    res["r6_validation"] = validate_r6_against_frozen(res["r6"]["summary"], frozen) if frozen else math.nan
    for name, parts in res.items():
        if isinstance(parts, dict):
            for k, df in parts.items():
                _csv(df, out / f"{name}_{k}.csv")
    write_report(res, report, header)
    return res


def _md(df: pd.DataFrame) -> str:
    out = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(f"{v:.3f}" if isinstance(v, float) else str(v) for v in r) + " |")
    return "\n".join(out)


def write_report(res: dict, path: Path, header: dict) -> None:
    r3_, r6_, r7_, r11_ = res["r3"], res["r6"], res["r7"], res["r11"]
    L = ["# Paper G — Exploratory diagnostics R3, R6, R7, R11", "",
         "Generated by `scripts/paper_g_diagnostics.py`; do not edit. **Exploratory** (plan section 12.2), "
         "computed after the confirmatory results were seen; no original table is changed.", ""]
    L += [f"- {k}: {v}" for k, v in header.items()]
    L += ["", "## R3. Explainer rank positions (three studied explainers, seven metrics)", "",
          "**Table D1. Block-level structure (160 blocks).**", "", _md(r3_["summary"]), "",
          "**Table D2. Untied rank counts and ties per metric and explainer (over 8 datasets × 20 blocks).**", "",
          _md(r3_["positions_by_metric"]), "",
          "**Table D3. SHAP versus occlusion without LIME, per dataset (descriptive; the 0.5 rule is not applied).**", "",
          _md(r3_["shap_occlusion_datasets"]), "",
          "## R6. H2 adjusted for the predicted-class probability (rank-based partial correlation)", "",
          f"Validation: the unadjusted values equal the frozen H2 outputs to {res['r6_validation']:.1e} "
          f"(tolerance {H2_TOL}).", "",
          "**Table D4. Dataset-level means and 95% t-intervals, unadjusted and adjusted.**", "",
          _md(r6_["summary"]), "",
          "## R7. M7 structure", "", "**Table D5. Feature groups and removal-set sizes per dataset.**", "",
          _md(r7_["groups"]), "",
          "**Table D6. Share of blocks with identical removal sets among the studied explainers, per dataset and level.**", "",
          _md(r7_["removal_by_dataset"]), "",
          "**Table D7. M7 ties among the studied explainers, by dataset and by model.**", "",
          _md(r7_["ties_by_dataset"]), "", _md(r7_["ties_by_model"]), "",
          "Identical removal sets give identical retraining inputs at that level; whether retraining "
          "variance explains the rest of M7's instability is not tested here.", "",
          "## R11. Random control ranked last", "",
          "Ranks among the four explainers (average ranks). Denominator: 160 blocks.", "",
          _md(r11_["summary"]), "", _md(r11_["per_metric"]), ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L), encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--authorized", default="")
    a = ap.parse_args(argv)
    if not a.run or not a.authorized.strip():
        print("refused: the diagnostics run only with --run and an --authorized statement (plan 12.2)", file=sys.stderr)
        return 2
    full, roar = load()
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=lib.ROOT, capture_output=True, text=True).stdout.strip()
    res = run_all(full, roar, OUT, REPORT, {"authorized": a.authorized, "code commit": commit,
                                             "data": "outputs/analysis/paper_g/raw (frozen 04c6dfd84)"},
                  lib.config()["metrics"]["roar_levels"])
    if not res["r6_validation"] <= H2_TOL:
        print(f"STOP: R6 unadjusted path differs from the frozen H2 by {res['r6_validation']:.2e}", file=sys.stderr)
        return 3
    print(f"diagnostics written to {OUT} and {REPORT}; R6 validation {res['r6_validation']:.1e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
