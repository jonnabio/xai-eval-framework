#!/usr/bin/env python3
"""Render and build Paper F for Journal of Computer Sciences Institute.

1. Render: paper_f_template.tex -> paper_f.tex. Every placeholder <<alias:key:column:format>>
   is replaced by a value read from a result file, and the table fragments under generated/
   are written from the same files.

       alias   file                                              key
       sum     values computed here from datasets.csv, candidates.csv and
               paper_f_config.toml (the size of the design)      metric
       pow     outputs/analysis/paper_f/power_simulation.csv     <datasets>_<true correlation>
       prim    outputs/analysis/paper_f/results/primary.csv      measure
       sens    .../results/primary_complete_cases.csv            measure
       run     .../results/cells.csv, summed here                all
       fail    .../results/failures.csv, summed by method        explainer; top1..top3, top
       var     .../results/variance.csv, balanced analysis       <measure>_<method|dataset|interaction>
       chg     .../results/rank_change.csv                       <measure>_<explainer>; <measure>
       mod     .../results/per_model.csv                         <model>_<measure>
       cmp     decisions of prim against sens                    all
       adult   .../results/pairs_vs_adult.csv                    <measure>_<method>-<method>; all

   Formats: d integer; int integer with thousands separator; w, W integer as a word
   (lower case, capitalised); u2, u3 decimals; pct, pct1, pct2 percentage with no, one and
   two decimals; p p-value ("<0.001" or three decimals); outcome the sentence of OUTCOME
   for a decision of the rule (analysis plan, section 6); txt a name, as it is.

   A placeholder whose result file does not exist yet is rendered as a red "[pending]"
   mark. With --final the build stops on any pending mark.

   <<input:path:label>> becomes the table fragment or the figure at `path` (relative to
   this paper's folder) when the file exists, and a pending mark with `label` otherwise.

2. Build: submission/paper_f_{blind,full}.pdf with Tectonic. The submitted Word file is
   made in the journal's template (VENUE_JCSI.md); this PDF predicts its length.

    python docs/reports/paper_f/scripts/build_paper_f.py [--final]
"""
from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
F = Path(__file__).resolve().parents[1]
OUT = F / "submission"
GEN = F / "generated"
RES = ROOT / "outputs" / "analysis" / "paper_f"
TECTONIC = ROOT / "tools" / "tectonic-portable" / (
    "tectonic.exe" if sys.platform == "win32" else "tectonic")
MAX_PAGES = 8
HEADER = "%% GENERATED from paper_f_template.tex by scripts/build_paper_f.py. Do not edit.\n"
MAX_ABSTRACT = 800  # characters, spaces included (VENUE_JCSI.md)
ADULT_MOST = 12     # "at least 12 of the 15 other datasets", the count printed in the text
WORDS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen "
         "fourteen fifteen sixteen seventeen eighteen nineteen twenty").split()
TOKEN = re.compile(r"<<([a-z]+):([^:<>]+):([a-z_0-9]+):([a-zA-Z0-9]+)>>")
INPUT = re.compile(r"<<input:([^:<>]+):([^<>]+)>>")
STRATA = {"numeric": "numeric", "mixed": "mixed", "categorical": "categorical"}
# The sentence printed for each decision of the rule. Written on 2026-10-11, before the
# analysis was run; the keys are the strings paper_f_analyze.py writes to primary.csv.
OUTCOME = {
    "no evidence that the order is shared":
        "there is no evidence that the order of the methods is shared between datasets",
    "the order generalises":
        "the order of the methods generalises: it is shared between datasets and the "
        "interval lies above 0.5",
    "the order is shared only weakly":
        "the order of the methods is shared between datasets only weakly: the interval "
        "lies below 0.5",
    "shared, strength not determined":
        "the order of the methods is shared between datasets, with a strength that is not "
        "determined: the interval contains 0.5",
}
TERMS = {"explainer": "method", "dataset": "dataset", "explainer x dataset": "interaction"}
MODELS = {"logreg": "logistic regression", "rf": "the random forest", "xgb": "XGBoost",
          "mlp": "the multilayer perceptron"}
METHODS = {"lime": "LIME", "shap": "SHAP", "anchors": "Anchors", "dice": "DiCE"}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def tables() -> dict[str, dict[str, dict[str, str]]]:
    out: dict[str, dict[str, dict[str, str]]] = {}
    if (RES / "datasets.csv").exists():
        with (F / "paper_f_config.toml").open("rb") as fh:
            cfg = tomllib.load(fh)
        # Size of the design as planned: every dataset has at least 1,000 rows (the rule),
        # so the 20% test split always holds the n_instances that are explained.
        d, seeds, inst = len(read(RES / "datasets.csv")), len(cfg["seeds"]), cfg["n_instances"]
        models, methods = len(cfg["models"]), len(cfg["explainers"])
        size = {
            "datasets": d, "candidates": len(read(RES / "candidates.csv")),
            "seeds": seeds, "pairs": d * (d - 1) // 2,
            "fits": d * models * seeds,                      # trained classifiers
            "runs": d * models * methods * seeds,            # one method on one classifier
            "runs_seed": d * models * methods,
            "runs_dataset": models * seeds,                  # per dataset and method
            "inst_dataset": models * seeds * inst,           # per dataset and method
            "explained": d * models * methods * seeds * inst,
            "explanations": d * models * methods * seeds * inst
            * (1 + cfg["measures"]["stability_copies"]),
        }
        out["sum"] = {k: {"value": str(v)} for k, v in size.items()}
        # The rows of Table 1, by dataset key (read by the claim registry, not by the text).
        out["data"] = {r["key"]: r for r in read(RES / "datasets.csv")}
    if (RES / "power_simulation.csv").exists():
        out["pow"] = {f"{r['k_datasets']}_{r['true_rho_bar']}": r
                      for r in read(RES / "power_simulation.csv")}
    res = RES / "results"
    if (res / "primary.csv").exists():
        out["prim"] = {r["measure"]: r for r in read(res / "primary.csv")}
    if (res / "primary_complete_cases.csv").exists():
        out["sens"] = {r["measure"]: r for r in read(res / "primary_complete_cases.csv")}
    if (res / "cells.csv").exists():
        cells = read(res / "cells.csv")
        n = sum(int(r["n"]) for r in cells)
        failed = round(sum(float(r["failure_rate"]) * int(r["n"]) for r in cells))
        out["run"] = {"all": {"seeds": str(len({r["seed"] for r in cells})),
                              "runs": str(len(cells)), "instances": str(n),
                              "failed": str(failed), "failure_rate": str(failed / n)}}
    if (res / "failures.csv").exists():
        by: dict[str, list[int]] = {}
        for r in read(res / "failures.csv"):
            t = by.setdefault(r["explainer"], [0, 0])
            t[0] += int(float(r["failures"]))
            t[1] += int(r["instances"])
        out["fail"] = {e: {"failures": str(f), "instances": str(n), "rate": str(f / n)}
                       for e, (f, n) in by.items()}
        # The three conditions with the most failures, with the names printed in the text.
        names = {r["key"]: r["name"] for r in read(RES / "datasets.csv")}
        rows = sorted(read(res / "failures.csv"), key=lambda r: -float(r["failures"]))[:3]
        total = sum(f for f, _ in by.values())
        for i, r in enumerate(rows, 1):
            out["fail"][f"top{i}"] = {
                "failures": str(int(float(r["failures"]))), "instances": r["instances"],
                "dataset": names.get(r["dataset"], r["dataset"]),
                "model": MODELS[r["model"]], "explainer": METHODS[r["explainer"]]}
        top = sum(int(float(r["failures"])) for r in rows)
        out["fail"]["top"] = {"share": str(top / total if total else 0.0)}
    if (res / "per_model.csv").exists():
        out["mod"] = {f"{r['model']}_{r['measure']}": r for r in read(res / "per_model.csv")}
    if "prim" in out and "sens" in out:
        out["cmp"] = {"all": {"changed": str(sum(
            out["prim"][m]["decision"] != out["sens"][m]["decision"] for m in out["prim"]))}}
    if (res / "variance.csv").exists():
        out["var"] = {f"{r['measure']}_{TERMS[r['term']]}": r for r in read(res / "variance.csv")
                      if r["analysis"] == "mixed model (balanced)" and r["term"] in TERMS}
    if (res / "pairs_vs_adult.csv").exists():
        pairs = read(res / "pairs_vs_adult.csv")
        out["adult"] = {f"{r['measure']}_{r['pair'].replace(' vs ', '-')}": r for r in pairs}
        same, others = [int(r["same_order"]) for r in pairs], int(pairs[0]["datasets"])
        out["adult"]["all"] = {
            "comparisons": str(len(pairs)), "others": str(others),
            "all_same": str(sum(s == others for s in same)),
            "most": str(sum(s >= ADULT_MOST for s in same)),
            "fewer": str(sum(s < ADULT_MOST for s in same))}
    if (res / "rank_change.csv").exists():
        change = read(res / "rank_change.csv")
        out["chg"] = {f"{r['measure']}_{r['explainer']}": r for r in change}
        for m in {r["measure"] for r in change}:
            part = [r for r in change if r["measure"] == m]
            out["chg"][m] = {
                "largest": str(max(float(r["largest_change"]) for r in part)),
                "first": str(sum(int(r["times_first"]) > 0 for r in part))}
    return out


def fmt(v: float, f: str) -> str:
    if f == "d":
        return str(int(round(v)))
    if f == "int":
        return f"{int(round(v)):,}"
    if f in ("w", "W"):
        word = WORDS[int(round(v))]
        return word.capitalize() if f == "W" else word
    if f in ("u2", "u3"):
        return f"{v:.{f[1]}f}".replace("-", "$-$")
    if f == "pct":
        return f"{100 * v:.0f}"
    if f in ("pct1", "pct2"):
        return f"{100 * v:.{f[3]}f}"
    if f == "p":
        return "$<$0.001" if v < 0.001 else f"{v:.3f}"
    raise KeyError(f"unknown format {f}")


def escape(text: str) -> str:
    return text.replace("_", r"\_").replace("&", r"\&").replace("%", r"\%")


def dataset_table() -> str:
    if not (RES / "datasets.csv").exists():
        return "\\pending{Table 1: the datasets of the study}\n"
    lines = [r"\begin{table*}[t]", r"\centering",
             r"\caption{Datasets of the study. Features are counted before encoding.}",
             r"\label{tab:datasets}", r"\small",
             r"\begin{tabular}{llrrrrl}", r"\toprule",
             r"Dataset & OpenML id & Rows & Features & Numeric (\%) & Minority class (\%) "
             r"& Stratum \\", r"\midrule"]
    for r in read(RES / "datasets.csv"):
        kind, size = r["stratum"].split("-")
        lines.append(" & ".join([
            escape(r["name"]), r["openml_id"], f"{int(r['rows']):,}", r["features"],
            f"{100 * float(r['share_numeric']):.0f}", f"{100 * float(r['minority_share']):.1f}",
            f"{STRATA[kind]}, {'under' if size == 'small' else 'from'} 10,000 rows"]) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    return "\n".join(lines)


def render_text() -> str:
    """The template with every placeholder filled; nothing is written."""
    template = (F / "paper_f_template.tex").read_text(encoding="utf-8")
    data = tables()
    problems: list[str] = []

    def sub(m: re.Match) -> str:
        alias, key, col, f = m.groups()
        if alias not in data:
            return f"\\pending{{{alias}:{escape(key)}}}"
        try:
            if f == "outcome":
                return OUTCOME[data[alias][key][col]]
            if f == "txt":
                return escape(data[alias][key][col])
            return fmt(float(data[alias][key][col]), f)
        except (KeyError, ValueError) as exc:
            problems.append(f"{m.group(0)}: {exc!r}")
            return m.group(0)

    def place(m: re.Match) -> str:
        path, label = m.groups()
        if not (F / path).exists():
            # A table that does not exist yet still takes its number and its label, so
            # that the draft builds before the results exist.
            stem = Path(path).stem
            anchor = (f"\\refstepcounter{{table}}\\label{{tab:{stem[4:]}}}"
                      if stem.startswith("tab_") else "")
            return f"\\pending{{{label}}}{anchor}"
        if path.endswith(".tex"):
            return f"\\input{{{path[:-4]}}}"
        return f"\\includegraphics[width=\\textwidth]{{{path}}}"

    out = TOKEN.sub(sub, INPUT.sub(place, template))
    problems += [f"unresolved: {t}" for t in re.findall(r"<<[^>]*>>", out)]
    if problems:
        sys.exit("render failed:\n" + "\n".join(sorted(set(problems))[:20]))
    return out


def render(final: bool) -> tuple[Path, int]:
    out = render_text()
    GEN.mkdir(exist_ok=True)
    (GEN / "tab_datasets.tex").write_text(dataset_table(), encoding="utf-8", newline="\n")
    body = out.split("\\begin{document}", 1)[1]
    pending = len(re.findall(r"\\pending\{", body)) \
        + len(re.findall(r"\\pending\{", dataset_table())) \
        + body.count("\\paperfarchive") * (0 if "zenodo.org" in out or "doi.org/10.5281" in out else 1)
    if final and pending:
        sys.exit(f"--final: {pending} pending marks remain")
    target = F / "paper_f.tex"
    target.write_text(HEADER + out, encoding="utf-8", newline="\n")
    return target, pending


def abstract_length(tex: str) -> int:
    """Characters of the abstract as printed, spaces included."""
    text = tex.split("\\textbf{Abstract}\\par", 1)[1].split("\\medskip", 1)[0]
    text = text.replace("\\smallskip", "").replace("\\%", "%").replace("~", " ")
    text = re.sub(r"\$<\$", "<", text).replace("$", "")
    return len(" ".join(text.split()))


def reference_report(tex: str) -> tuple[str, bool]:
    """The author's rule for references (README, section 7, rule 7), on the cited entries.

    An entry counts as verified when it has a field `checked = {date}`, written by the
    person or session that compared it with the record its DOI resolves to.
    """
    bib = (F / "references.bib").read_text(encoding="utf-8")
    entries = {m.group(1): m.group(2) for m in
               re.finditer(r"^@\w+\{([^,]+),(.*?)(?=^@|\Z)", bib, flags=re.M | re.S)}
    cited: list[str] = []
    for group in re.findall(r"\\cite\{([^}]*)\}", tex):
        cited += [k.strip() for k in group.split(",") if k.strip() not in cited]
    no_doi = [k for k in cited if not re.search(r"\bdoi\s*=", entries.get(k, ""))]
    unchecked = [k for k in cited if not re.search(r"\bchecked\s*=", entries.get(k, ""))]
    years = {k: int(m.group(1)) for k in cited
             if (m := re.search(r"\byear\s*=\s*\{?(\d{4})", entries.get(k, "")))}
    recent = sum(y >= 2024 for y in years.values())
    share = recent / len(cited) if cited else 0.0
    ok = not no_doi and not unchecked and share >= 0.8
    text = (f"refs  {len(cited)} cited; {recent} from 2024 or later ({100 * share:.0f}%, "
            f"rule: 80%); {len(no_doi)} without DOI; {len(unchecked)} not marked as checked")
    return text, ok


def build_pdf(full: bool) -> tuple[Path, int]:
    name = "paper_f_full" if full else "paper_f_blind"
    src = F / f"{name}.tex"
    src.write_text(("\\def\\fullversion{}\n" if full else "") + "\\input{paper_f}\n",
                   encoding="utf-8")
    r = subprocess.run([str(TECTONIC), "-X", "compile", "--keep-logs", src.name], cwd=F,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        sys.exit(f"tectonic failed for {name}:\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")
    log = (F / f"{name}.log").read_text(encoding="utf-8", errors="ignore")
    bad = [l for l in log.splitlines() if re.search(r"Citation .* undefined|Reference .* undefined", l)]
    if bad:
        sys.exit(f"{name}: unresolved references:\n" + "\n".join(bad[:10]))
    m = re.search(r"Output written on .*?\((\d+) pages?", log)
    pages = int(m.group(1)) if m else -1
    pdf = OUT / f"{name}.pdf"
    shutil.move(str(F / f"{name}.pdf"), pdf)
    for ext in (".tex", ".log", ".aux", ".bbl", ".blg", ".out"):
        (F / f"{name}{ext}").unlink(missing_ok=True)
    return pdf, pages


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--final", action="store_true", help="fail if any pending mark remains")
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    tex, pending = render(args.final)
    print("tex ", tex.relative_to(ROOT), f"({pending} pending marks)")
    abstract = abstract_length(tex.read_text(encoding="utf-8"))
    print(f"abstract  {abstract} characters (limit {MAX_ABSTRACT})")
    if args.final and abstract > MAX_ABSTRACT:
        sys.exit("--final: the abstract is over the journal's limit")
    report, refs_ok = reference_report(tex.read_text(encoding="utf-8"))
    print(report)
    if args.final and not refs_ok:
        sys.exit("--final: the reference rule is not met")
    for full in (False, True):
        pdf, pages = build_pdf(full)
        print("pdf ", pdf.relative_to(ROOT), f"({pages} pages)")
        if pages > MAX_PAGES:
            print(f"WARNING: {pages} pages; the journal's limit is {MAX_PAGES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
