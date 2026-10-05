#!/usr/bin/env python3
"""Render and build Paper C for Tecnologia en Marcha: paper_c.tex, PDFs, Word files, figure.

1. Render: every placeholder <<alias:key:column:format>> in paper_c_template.tex is replaced
   by a value read from a result file, and the result is written to paper_c.tex. The build
   stops on a placeholder that cannot be resolved.

       alias    file                                                     key
       sum      results/summary.csv                                      metric
       orig     outputs/analysis/exp4_llm_evaluation/icc_analysis.csv    dimension
       alpha    outputs/analysis/exp4_llm_evaluation/krippendorff_alpha.csv  dimension
       view     outputs/analysis/exp4_cohort2/cohort2_reliability_by_view.csv  dimension|view
       retest   outputs/analysis/exp4_cohort2/cohort2_test_retest.csv    condition|judge
       post     results/posthoc_scores_vs_metrics.csv                    explainer|dimension|metric
       reg      results/posthoc_rank_regression.csv                      dimension|metric

   Views and conditions: primary, stated, alt, pooled. Judges: claude, gemini, gpt.
   Formats: d integer; int integer with thousands separator; u2, u3 decimals; s2, s3
   decimals with a typeset minus sign; pct, pct1 percentage with 0 or 1 decimals; p p-value
   ("<0.001" or three decimals); rs two signed decimals plus an asterisk when the row's
   p_holm is below 0.05.

2. Build: submission/paper_c_{blind,full}.pdf (Tectonic), submission/paper_c_{blind,full}.docx
   (pandoc through Quarto, restyled to the journal's format) and submission/Figure1.tiff.

    .venv/Scripts/python.exe docs/reports/paper_c/scripts/paper_c_summary.py
    python docs/reports/paper_c/scripts/build_paper_c.py

The Word formatting functions follow scripts/pubs/build_paper_d.py (same journal).
"""
from __future__ import annotations

import csv
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
C = Path(__file__).resolve().parents[1]
OUT = C / "submission"
TECTONIC = ROOT / "tools" / "tectonic-portable" / (
    "tectonic.exe" if sys.platform == "win32" else "tectonic")
FIGURES = ["fig1"]
MAX_PDF_PAGES = 15

VIEWS = {"primary": "hidden_label_primary", "stated": "label_visible_bias_probe",
         "alt": "rubric_alt_sensitivity", "pooled": "pooled_all_conditions"}
JUDGES = {"claude": "anthropic/claude-haiku-4.5", "gemini": "google/gemini-3.8-flash",
          "gpt": "openai/gpt-5.4-mini"}
ORIG = ROOT / "outputs" / "analysis" / "exp4_llm_evaluation"
C2A = ROOT / "outputs" / "analysis" / "exp4_cohort2"
SOURCES = {
    "sum": (C / "results" / "summary.csv", ["metric"]),
    "orig": (ORIG / "icc_analysis.csv", ["dimension"]),
    "alpha": (ORIG / "krippendorff_alpha.csv", ["dimension"]),
    "view": (C2A / "cohort2_reliability_by_view.csv", ["dimension", "view"]),
    "retest": (C2A / "cohort2_test_retest.csv", ["prompt_condition", "judge_model"]),
    "post": (C / "results" / "posthoc_scores_vs_metrics.csv",
             ["explainer", "dimension", "metric"]),
    "reg": (C / "results" / "posthoc_rank_regression.csv", ["dimension", "metric"]),
}
TOKEN = re.compile(r"<<([a-z]+):([^:<>]+):([a-z_0-9]+):([a-z0-9]+)>>")

_tables: dict[str, dict[tuple[str, ...], dict[str, str]]] = {}


# --- render ------------------------------------------------------------------

def row(alias: str, key: str) -> dict[str, str]:
    if alias not in _tables:
        path, cols = SOURCES[alias]
        with path.open(encoding="utf-8") as fh:
            _tables[alias] = {tuple(r[c] for c in cols): r for r in csv.DictReader(fh)}
    parts = tuple(VIEWS.get(p, JUDGES.get(p, p)) for p in key.split("|"))
    return _tables[alias][parts]


def signed(v: float, decimals: int) -> str:
    text = f"{abs(v):.{decimals}f}"
    return f"$-${text}" if v < 0 and float(text) != 0 else text


def fmt(v: float, f: str, r: dict[str, str]) -> str:
    if f == "d":
        return str(int(round(v)))
    if f == "int":
        return f"{int(round(v)):,}"
    if f in ("u2", "u3"):
        return f"{abs(v):.{f[1]}f}"
    if f in ("s2", "s3"):
        return signed(v, int(f[1]))
    if f == "pct":
        return f"{100 * v:.0f}"
    if f == "pct1":
        return f"{100 * v:.1f}"
    if f == "p":
        return "$<$0.001" if v < 0.001 else f"{v:.3f}"
    if f == "rs":
        star = "*" if r.get("p_holm") and float(r["p_holm"]) < 0.05 else ""
        return signed(v, 2) + star
    raise KeyError(f"unknown format {f}")


def render() -> Path:
    template = (C / "paper_c_template.tex").read_text(encoding="utf-8")
    problems: list[str] = []

    def sub(m: re.Match) -> str:
        alias, key, col, f = m.groups()
        try:
            r = row(alias, key)
            return fmt(float(r[col]), f, r)
        except (KeyError, ValueError) as exc:
            problems.append(f"{m.group(0)}: {exc!r}")
            return m.group(0)

    out = TOKEN.sub(sub, template)
    problems += [f"unresolved: {t}" for t in re.findall(r"<<[^>]*>>", out) if t not in problems]
    if problems:
        sys.exit("render failed:\n" + "\n".join(sorted(set(problems))[:20]))
    header = "%% GENERATED from paper_c_template.tex by scripts/build_paper_c.py. Do not edit.\n"
    target = C / "paper_c.tex"
    target.write_text(header + out, encoding="utf-8", newline="\n")
    return target


# --- build -------------------------------------------------------------------

def _run(cmd: list[str], cwd: Path) -> None:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if r.returncode:
        sys.exit(f"failed: {' '.join(cmd)}\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")


def _variant(tex: str, full: bool) -> str:
    """Resolve the \\iffull ... \\else ... \\fi blocks, for pandoc (it does not evaluate them)."""
    pat = re.compile(r"^\\iffull\n(.*?)^\\else\n(.*?)^\\fi\n", re.DOTALL | re.MULTILINE)
    out, n = pat.subn(lambda m: m.group(1) if full else m.group(2), tex)
    if n != 2:
        sys.exit(f"expected 2 \\iffull blocks (author, data availability), found {n}")
    return out


def build_pdf(full: bool) -> tuple[Path, int]:
    name = "paper_c_full" if full else "paper_c_blind"
    src = C / f"{name}.tex"
    src.write_text(("\\def\\fullversion{}\n" if full else "") + "\\input{paper_c}\n",
                   encoding="utf-8")
    _run([str(TECTONIC), "-X", "compile", "--keep-logs", src.name], C)
    log = (C / f"{name}.log").read_text(encoding="utf-8", errors="ignore")
    bad = [l for l in log.splitlines() if re.search(r"undefined|Citation .* undefined", l)]
    if bad:
        sys.exit(f"{name}: unresolved references:\n" + "\n".join(bad[:10]))
    pages = int(re.search(r"Output written on .*?\((\d+) pages?", log).group(1)) \
        if "Output written" in log else -1
    pdf = OUT / f"{name}.pdf"
    shutil.move(str(C / f"{name}.pdf"), pdf)
    src.unlink()
    (C / f"{name}.log").unlink(missing_ok=True)
    return pdf, pages


def reference_docx() -> Path:
    """Pandoc's default reference.docx restyled to the journal's format."""
    ref = OUT / "_reference.docx"
    with zipfile.ZipFile(C / "reference_default.docx") as zin, \
            zipfile.ZipFile(ref, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                x = data.decode("utf-8")
                for attr in ("ascii", "hAnsi", "eastAsia", "cs"):
                    x = re.sub(rf'w:{attr}="[^"]*"', f'w:{attr}="Times New Roman"', x)
                x = re.sub(r'w:(asciiTheme|hAnsiTheme|eastAsiaTheme|cstheme)="[^"]*"\s*', "", x)
                x = re.sub(r'<w:sz w:val="\d+"\s*/>', '<w:sz w:val="24"/>', x)
                x = re.sub(r'<w:szCs w:val="\d+"\s*/>', '<w:szCs w:val="24"/>', x)
                x = re.sub(r'<w:spacing ([^/]*?)w:line="\d+"', r'<w:spacing \1w:line="360"', x)
                data = x.encode("utf-8")
            zout.writestr(item, data)
    return ref


TIMES = ('<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
         'w:eastAsia="Times New Roman" w:cs="Times New Roman"/>')
# US Letter (12240 x 15840 twips), 2.5 cm margins (1418 twips).
SECT = ('<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1418" w:right="1418" '
        'w:bottom="1418" w:left="1418" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>')
SMALL = '<w:sz w:val="20"/><w:szCs w:val="20"/>'


def _small_table(tbl: str) -> str:
    """10 pt, single-spaced table cells (element order follows the OOXML schema)."""
    def rpr(m: re.Match) -> str:
        body = m.group(1)
        if "<w:sz " in body:
            return m.group(0)
        if "<w:vertAlign" in body:
            body = body.replace("<w:vertAlign", SMALL + "<w:vertAlign", 1)
        else:
            body += SMALL
        return f"<w:rPr>{body}</w:rPr>"
    tbl = re.sub(r"<w:rPr>([\s\S]*?)</w:rPr>", rpr, tbl)
    tbl = re.sub(r"<w:r>(?!<w:rPr>)", f"<w:r><w:rPr>{SMALL}</w:rPr>", tbl)
    return re.sub(r'(<w:pStyle w:val="Compact"\s*/>)',
                  r'\1<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>', tbl)


def _rewrite(docx: Path, edit) -> None:
    tmp = docx.with_suffix(".tmp")
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename in ("word/styles.xml", "word/document.xml"):
                data = edit(item.filename, data.decode("utf-8")).encode("utf-8")
            zout.writestr(item, data)
    tmp.replace(docx)


def enforce_format(docx: Path) -> None:
    """Times New Roman 12 pt, 1.5 line spacing, letter paper, 2.5 cm margins; tables 10 pt."""
    def edit(name: str, x: str) -> str:
        if name == "word/styles.xml":
            x = re.sub(r"<w:rFonts\b[^>]*/>", TIMES, x)
            x = re.sub(r'<w:sz w:val="\d+"\s*/>', '<w:sz w:val="24"/>', x)
            x = re.sub(r'<w:szCs w:val="\d+"\s*/>', '<w:szCs w:val="24"/>', x)
            x = re.sub(r"<w:spacing\b([^>]*?)\s*/>",
                       lambda m: "<w:spacing"
                       + re.sub(r'\s*w:(line|lineRule)="[^"]*"', "", m.group(1))
                       + ' w:line="360" w:lineRule="auto"/>', x)
            x = re.sub(r"(<w:pPrDefault>\s*<w:pPr>)(?![\s\S]{0,80}w:line=)",
                       r'\1<w:spacing w:line="360" w:lineRule="auto"/>', x)
            x = re.sub(r'(<w:style [^>]*w:styleId="(?:BodyText|FirstParagraph|Compact)"[\s\S]*?)'
                       r'<w:spacing\b[^>]*/>',
                       r'\1<w:spacing w:before="0" w:after="100" w:line="360" w:lineRule="auto"/>',
                       x)
            x = re.sub(r'(<w:style [^>]*w:styleId="Compact"[\s\S]*?)<w:spacing\b[^>]*/>',
                       r'\1<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>', x)
            x = re.sub(r'(<w:pPrDefault>\s*<w:pPr>\s*)<w:spacing\b[^>]*/>',
                       r'\1<w:spacing w:before="0" w:after="100" w:line="360" w:lineRule="auto"/>',
                       x)
        else:
            x = re.sub(r"<w:tbl>[\s\S]*?</w:tbl>", lambda m: _small_table(m.group(0)), x)
            x = re.sub(r"<w:sectPr\b[\s\S]*?</w:sectPr>", "", x)
            x = x.replace("</w:body>", SECT + "</w:body>")
        return x
    _rewrite(docx, edit)


AI_HEADING = "Declaration on the Use of Artificial Intelligence (AI)"


def _declaration_after_references(docx: Path) -> None:
    """Pandoc puts the reference list last; the journal puts the AI declaration after it."""
    def edit(name: str, x: str) -> str:
        if name != "word/document.xml":
            return x
        paras = list(re.finditer(r"<w:p\b[\s\S]*?</w:p>", x))
        text = [re.sub(r"<[^>]+>", "", m.group(0)) for m in paras]
        start = next(i for i, t in enumerate(text) if t.strip() == AI_HEADING)
        end = next(i for i, t in enumerate(text) if i > start and t.strip() == "References")
        block = x[paras[start].start():paras[end].start()]
        x = x[:paras[start].start()] + x[paras[end].start():]
        cut = x.rfind("<w:sectPr")
        cut = cut if cut != -1 and cut > x.rfind("</w:p>") else x.rfind("</w:body>")
        return x[:cut] + block + x[cut:]
    _rewrite(docx, edit)


def build_docx(full: bool, ref: Path) -> Path:
    name = "paper_c_full" if full else "paper_c_blind"
    tmp = C / f"_{name}_pandoc.tex"
    tmp.write_text(_variant((C / "paper_c.tex").read_text(encoding="utf-8"), full),
                   encoding="utf-8")
    out = OUT / f"{name}.docx"
    _run(["quarto", "pandoc", tmp.name, "-o", str(out), "--citeproc",
          "--bibliography", "references.bib", "--csl", "ieee.csl",
          f"--reference-doc={ref}", "--default-image-extension=png",
          "--resource-path=.", "-f", "latex", "-t", "docx",
          "-M", "reference-section-title=References"], C)
    tmp.unlink()
    _declaration_after_references(out)
    enforce_format(out)
    return out


def main() -> int:
    OUT.mkdir(exist_ok=True)
    print("tex ", render().relative_to(ROOT))
    for full in (False, True):
        pdf, pages = build_pdf(full)
        print("pdf ", pdf.relative_to(ROOT), f"({pages} pages)")
        if pages > MAX_PDF_PAGES:
            print(f"WARNING: {pages} pages, the journal's limit is {MAX_PDF_PAGES}; "
                  "measure the Word file before cutting")
    ref = reference_docx()
    for full in (False, True):
        print("docx", build_docx(full, ref).relative_to(ROOT))
    ref.unlink()
    for i, fig in enumerate(FIGURES, 1):
        shutil.copyfile(C / "figures" / f"{fig}.tiff", OUT / f"Figure{i}.tiff")
        print("fig ", (OUT / f"Figure{i}.tiff").relative_to(ROOT))
    for pattern in ("paper_c_*.aux", "paper_c_*.blg", "paper_c_*.bbl"):
        for p in C.glob(pattern):
            p.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
