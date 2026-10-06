#!/usr/bin/env python3
"""Render and build Paper F for Journal of Computer Sciences Institute.

1. Render: paper_f_template.tex -> paper_f.tex. Every placeholder <<alias:key:column:format>>
   is replaced by a value read from a result file, and the table fragments under generated/
   are written from the same files.

       alias   file                                              key
       sum     values computed here from datasets.csv and candidates.csv   metric
       prim    outputs/analysis/paper_f/results/primary.csv      measure

   Formats: d integer; int integer with thousands separator; w, W integer as a word
   (lower case, capitalised); u2, u3 decimals; pct percentage without decimals;
   p p-value ("<0.001" or three decimals).

   A placeholder whose result file does not exist yet is rendered as a red "[pending]"
   mark. With --final the build stops on any pending mark.

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
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
F = Path(__file__).resolve().parents[1]
OUT = F / "submission"
GEN = F / "generated"
RES = ROOT / "outputs" / "analysis" / "paper_f"
TECTONIC = ROOT / "tools" / "tectonic-portable" / (
    "tectonic.exe" if sys.platform == "win32" else "tectonic")
MAX_PAGES = 8
WORDS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen "
         "fourteen fifteen sixteen seventeen eighteen nineteen twenty").split()
TOKEN = re.compile(r"<<([a-z]+):([^:<>]+):([a-z_0-9]+):([a-zA-Z0-9]+)>>")
STRATA = {"numeric": "numeric", "mixed": "mixed", "categorical": "categorical"}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def tables() -> dict[str, dict[str, dict[str, str]]]:
    out: dict[str, dict[str, dict[str, str]]] = {}
    if (RES / "datasets.csv").exists():
        out["sum"] = {
            "datasets": {"value": str(len(read(RES / "datasets.csv")))},
            "candidates": {"value": str(len(read(RES / "candidates.csv")))},
        }
    if (RES / "results" / "primary.csv").exists():
        out["prim"] = {r["measure"]: r for r in read(RES / "results" / "primary.csv")}
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


def render(final: bool) -> tuple[Path, int]:
    template = (F / "paper_f_template.tex").read_text(encoding="utf-8")
    data = tables()
    problems: list[str] = []

    def sub(m: re.Match) -> str:
        alias, key, col, f = m.groups()
        if alias not in data:
            return f"\\pending{{{alias}:{key}}}"
        try:
            return fmt(float(data[alias][key][col]), f)
        except (KeyError, ValueError) as exc:
            problems.append(f"{m.group(0)}: {exc!r}")
            return m.group(0)

    out = TOKEN.sub(sub, template)
    problems += [f"unresolved: {t}" for t in re.findall(r"<<[^>]*>>", out)]
    if problems:
        sys.exit("render failed:\n" + "\n".join(sorted(set(problems))[:20]))
    GEN.mkdir(exist_ok=True)
    (GEN / "tab_datasets.tex").write_text(dataset_table(), encoding="utf-8", newline="\n")
    body = out.split("\\begin{document}", 1)[1]
    pending = len(re.findall(r"\\pending\{", body)) \
        + len(re.findall(r"\\pending\{", dataset_table())) \
        + body.count("\\paperfarchive") * (0 if "zenodo.org" in out or "doi.org/10.5281" in out else 1)
    if final and pending:
        sys.exit(f"--final: {pending} pending marks remain")
    header = "%% GENERATED from paper_f_template.tex by scripts/build_paper_f.py. Do not edit.\n"
    target = F / "paper_f.tex"
    target.write_text(header + out, encoding="utf-8", newline="\n")
    return target, pending


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
