#!/usr/bin/env python3
"""Paper B revision 1: render the revised manuscript, the changes-marked comparison and the
response letter into revision_1/build/, apart from the submitted files.

    .venv/Scripts/python.exe docs/reports/paper_b/ci_journal/revision_1/scripts/build_revision.py
    ... build_revision.py --no-word        LaTeX outputs only (no Word needed)

Outputs (revision_1/build/):
  paper_b_ci_rev1_manuscript.docx / .pdf   the revised manuscript in the journal's Word
                                           template, masked (the file to upload)
  paper_b_ci_rev1_preview.pdf              LaTeX rendering of the revised source
  paper_b_ci_rev1_changes_marked.docx/.pdf every insertion and deletion against the submitted
                                           manuscript (Word's document comparison of the frozen
                                           ../submission/paper_b_ci_manuscript.docx with the revised
                                           .docx; tracked changes, author "Author", masked)
  paper_b_ci_rev1_response.docx / .pdf     the response letter (internal tracking lines removed)
  BUILD_MANIFEST.md                        date, commit, hashes, pages, check results

It refuses to build if a submitted file changed (SUBMITTED_SNAPSHOT.sha256). It never writes
into ../submission/. LaTeX is compiled from ci_journal/, where the relative paths of both
sources resolve.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

REV = Path(__file__).resolve().parents[1]
CI = REV.parent
ROOT = CI.parents[3]
BUILD = REV / "build"
WORK = BUILD / "_latex"
SUBMITTED = CI / "paper_b_ci.tex"
REVISED = REV / "manuscript" / "paper_b_ci_rev1.tex"
NAME = "paper_b_ci_rev1"
# Page budget of the manuscript in the journal's Word template. The journal sets no length
# limit (writing rules, last updated 2025-02-22); its published articles run 7 to 17 pages.
PAGE_BUDGET = 12                     # author decision D-C, 2026-11-06: aim 12 pages
SUBMITTED_DOCX = CI / "submission" / "paper_b_ci_manuscript.docx"   # frozen; text-check only
# Kept in the lane's own folder (pub/ is a shared path).
REV_ABSTRACT = REV / "manuscript" / "abstract_rev1.tex"
REV_KEYWORDS = REV / "manuscript" / "keywords_rev1.tex"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def pdflatex(tex: Path, jobname: str) -> Path:
    WORK.mkdir(parents=True, exist_ok=True)
    for _ in range(2):                                  # references and labels
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                            f"-output-directory={WORK}", f"-jobname={jobname}", str(tex)],
                           cwd=CI, capture_output=True, text=True, errors="replace")
        if r.returncode:
            tail = "\n".join(r.stdout.splitlines()[-25:])
            sys.exit(f"pdflatex failed on {tex.name}:\n{tail}")
    log = (WORK / f"{jobname}.log").read_text(encoding="utf-8", errors="replace")
    undefined = re.findall(r"(?:Reference|Citation) `([^']+)' .*undefined", log)
    if undefined:
        print(f"WARNING {jobname}: undefined references {sorted(set(undefined))}")
    return WORK / f"{jobname}.pdf"


def pdf_pages(pdf: Path) -> int:
    data = pdf.read_bytes()
    return len(re.findall(rb"/Type\s*/Page[^s]", data))


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


COMPARE_PS1 = r"""
param([string]$orig, [string]$rev, [string]$out, [string]$pdf)
$ErrorActionPreference = "Stop"
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
$o = $null; $r = $null; $c = $null
try {
  $o = $w.Documents.Open($orig, $false, $true)
  $r = $w.Documents.Open($rev, $false, $true)
  # Destination new document (2), word-level granularity (1); author kept neutral (masked).
  $c = $w.CompareDocuments($o, $r, 2, 1, $true, $true, $true, $true, $true, $true, $true, $true, $true, $true, "Author", $true)
  $c.SaveAs2($out, 12)
  $c.ActiveWindow.View.RevisionsFilter.Markup = 2
  $c.ActiveWindow.View.ShowRevisionsAndComments = $true
  # PDF with the markup (Item 7 = document with markup).
  $c.ExportAsFixedFormat($pdf, 17, $false, 0, 0, 1, 1, 7, $true, $true, 0, $true, $true, $false)
  "revisions=" + $c.Revisions.Count
} finally {
  # Always release the files, even after an error (a hidden Word would keep them locked).
  foreach ($d in @($c, $r, $o)) { if ($d) { try { $d.Close(0) } catch {} } }
  $w.Quit()
}
"""


def word_compare(original: Path, revised: Path, out: Path) -> Path:
    """Tracked-changes comparison by Word (CompareDocuments); also exports a PDF."""
    script = WORK / "_compare.ps1"
    script.write_text(COMPARE_PS1, encoding="utf-8")
    for p in (out, out.with_suffix(".pdf")):
        p.unlink(missing_ok=True)
    r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                        str(script), str(original), str(revised), str(out),
                        str(out.with_suffix(".pdf"))], capture_output=True, text=True)
    if r.returncode or not out.exists():
        sys.exit(f"Word comparison failed:\n{r.stdout[-1200:]}\n{r.stderr[-1200:]}")
    m = re.search(r"revisions=(\d+)", r.stdout)
    print(f"changes marked: {m.group(1) if m else '?'} Word revisions")
    return out


def docx_paragraphs(docx: Path) -> list[str]:
    import zipfile
    xml = zipfile.ZipFile(docx).read("word/document.xml").decode("utf-8")
    out = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S):
        t = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)).replace("​", "")
        t = re.sub(r"\s+", " ", re.sub(r"^[•\-\d]+\.?\s*", "", t)).strip()
        if t:
            out.append(t)
    return out


def text_differences(a: Path, b: Path) -> list[str]:
    import difflib
    return [l for l in difflib.unified_diff(docx_paragraphs(b), docx_paragraphs(a), lineterm="", n=0)
            if l[:1] in "+-" and not l.startswith(("+++", "---"))]


def scrub_core(docx: Path, builder) -> None:
    """Reset the document properties Word fills with the Windows user (masked review)."""
    import zipfile
    tmp = docx.with_suffix(".tmp")
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in zin.namelist():
            data = zin.read(n)
            if n == "docProps/core.xml":
                data = builder.core_properties(data.decode("utf-8"), "Revised manuscript, "
                                               "changes marked", "").encode("utf-8")
            zout.writestr(n, data)
    tmp.replace(docx)


def count_revisions(docx: Path) -> str:
    import zipfile
    xml = zipfile.ZipFile(docx).read("word/document.xml").decode("utf-8", "ignore")
    return f"{xml.count('<w:ins ')} insertions, {xml.count('<w:del ')} deletions (Word revisions)"


PAGE_BREAK = '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```'


def response_markdown() -> str:
    """The letter as sent: internal tracking lines and HTML comments removed."""
    text = (REV / "RESPONSE_TO_REVIEWERS.md").read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    keep = []
    for line in text.splitlines():
        if re.match(r"^- \*\*(Status|Changes|Plan|Type):\*\*", line):
            continue
        if line in ("## Reviewer 1: general assessment", "## Reviewer 2"):
            keep += ["", PAGE_BREAK, ""]  # each party starts on a new page
        keep.append(line.replace("- **Response:**", "**Response.**")
                    .replace("- **Where:**", "**Changes in the manuscript:**"))
    return "\n".join(keep)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-word", action="store_true", help="skip the Word outputs")
    a = ap.parse_args(argv)
    check = load(REV / "scripts" / "check_revision.py", "check_revision")
    snap = check.check_snapshot()
    if snap:
        sys.exit("refusing to build: " + "; ".join(snap))
    BUILD.mkdir(exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    report = [f"# Build of revision 1 — {time.strftime('%Y-%m-%d %H:%M:%S')}", ""]
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                            text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", str(REV), str(CI / "scripts")],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
    report += [f"- Commit: `{commit}`{' (with uncommitted changes in the revision folder)' if dirty else ''}",
               f"- Revised source: `{REVISED.relative_to(ROOT).as_posix()}` (sha256 {sha(REVISED)[:16]})",
               ""]
    outputs: list[Path] = []

    # 1. LaTeX preview of the revised source.
    prev = pdflatex(REVISED, f"{NAME}_preview")
    shutil.copyfile(prev, BUILD / f"{NAME}_preview.pdf")
    outputs.append(BUILD / f"{NAME}_preview.pdf")

    # 3. The journal-format manuscript (Word template) and 4. the response letter.
    builder = load(CI / "scripts" / "build_paper_b_ci_docx.py", "build_paper_b_ci_docx")
    baseline = None
    if not a.no_word:
        # Baseline for the comparison: the SUBMITTED source rebuilt with today's pipeline, so
        # that only real edits are marked (the submitted .docx carries zero-width spaces and
        # formatting marks of its own Word pass). Its text must equal the submitted .docx.
        bdir = WORK / "baseline"
        bdir.mkdir(parents=True, exist_ok=True)
        rc = builder.main(["--source", str(SUBMITTED), "--out", str(bdir), "--name",
                           "paper_b_ci_submitted", "--manuscript-only",
                           "--abstract", str(ROOT / "pub/fragments/paper_b_abstract_en.tex"),
                           "--keywords", str(ROOT / "pub/fragments/paper_b_keywords_en.tex")])
        if rc:
            sys.exit("baseline rebuild failed")
        baseline = bdir / "paper_b_ci_submitted_manuscript.docx"
        diff = text_differences(baseline, SUBMITTED_DOCX)
        if diff:
            sys.exit(f"the rebuilt baseline differs from the submitted .docx in {len(diff)} "
                     f"paragraphs, e.g. {diff[0][:200]!r}: comparison refused")
        report.append("- Comparison baseline: the submitted source rebuilt today; its text is "
                      "identical to `../submission/paper_b_ci_manuscript.docx` (checked, "
                      "zero-width spaces ignored)")
    args = ["--source", str(REVISED), "--out", str(BUILD), "--name", NAME, "--manuscript-only"]
    if REV_ABSTRACT.exists():
        args += ["--abstract", str(REV_ABSTRACT)]
    if REV_KEYWORDS.exists():
        args += ["--keywords", str(REV_KEYWORDS)]
    if a.no_word:
        args.append("--no-pdf")
    rc = builder.main(args)
    if rc:
        sys.exit(f"Word build failed ({rc})")
    outputs.append(BUILD / f"{NAME}_manuscript.docx")
    if not a.no_word:
        outputs.append(BUILD / f"{NAME}_manuscript.pdf")
        marked = word_compare(baseline, BUILD / f"{NAME}_manuscript.docx",
                              BUILD / f"{NAME}_changes_marked.docx")
        scrub_core(marked, builder)
        builder.check_masked(marked)
        outputs += [marked, marked.with_suffix(".pdf")]
        report.append(f"- Changes marked against the submitted manuscript: {count_revisions(marked)}")
    letter_md = WORK / "response.md"
    letter_md.write_text(response_markdown(), encoding="utf-8")
    letter = BUILD / f"{NAME}_response.docx"
    r = subprocess.run(["quarto", "pandoc", str(letter_md), "-f", "markdown", "-t", "docx",
                        "-o", str(letter)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"pandoc failed on the response letter: {r.stderr[-800:]}")
    outputs.append(letter)
    if not a.no_word:
        print("response letter:", builder.word_pass(letter, "Response to the reviewers", ""))
        outputs.append(letter.with_suffix(".pdf"))
    builder.check_masked(BUILD / f"{NAME}_manuscript.docx")

    if not a.no_word:
        pages = pdf_pages(BUILD / f"{NAME}_manuscript.pdf")
        flag = "within" if pages <= PAGE_BUDGET else "OVER"
        report.append(f"- Length: {pages} pages in the journal template; budget {PAGE_BUDGET} "
                      f"({flag})")
        if pages > PAGE_BUDGET:
            print(f"WARNING: the manuscript has {pages} pages, over the budget of {PAGE_BUDGET}")

    # 5. Tracking status and manifest.
    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        check_rc = check.main([])
    report += ["", "## Tracking", "", "```", buf.getvalue().strip(), "```", "",
               "## Files", "", "| File | Pages | SHA-256 |", "|---|---:|---|"]
    for p in outputs:
        pages = pdf_pages(p) if p.suffix == ".pdf" else ""
        report.append(f"| `{p.name}` | {pages} | `{sha(p)[:16]}` |")
    report += ["", "The submitted files (`../submission/`, `../paper_b_ci.tex`) were checked "
               "against `SUBMITTED_SNAPSHOT.sha256` before the build and are unchanged."]
    (BUILD / "BUILD_MANIFEST.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    return check_rc


if __name__ == "__main__":
    raise SystemExit(main())
