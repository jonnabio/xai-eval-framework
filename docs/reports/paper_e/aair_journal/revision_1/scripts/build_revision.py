#!/usr/bin/env python3
"""Paper E, AAIR revision 1: changes-marked manuscript and response letter (.docx and .pdf).

    .venv/Scripts/python.exe docs/reports/paper_e/aair_journal/revision_1/scripts/build_revision.py

Needs Word (COM). Steps:
  1. The submitted frozen files are checked against SUBMITTED_SNAPSHOT.sha256.
  2. Baseline: the SUBMITTED source rebuilt with today's pipeline (signs as text, RCA-007),
     in _work/, without touching the registry. Its text must equal the submitted .docx, the
     signs aside (the submitted file holds them as equations): only real edits are marked.
  3. The revised manuscript is built (build_paper_e_aair_docx.py, edition rev1).
  4. Word compares baseline and revision: build/paper_e_aair_rev1_changes_marked.docx/.pdf.
  5. RESPONSE_TO_REVIEWERS.md becomes build/paper_e_aair_rev1_response.docx/.pdf: the
     internal status line and the change ids (C-###) are removed; each reviewer starts on
     a new page.
"""
from __future__ import annotations

import hashlib
import importlib.util
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REV = Path(__file__).resolve().parents[1]
AAIR = REV.parent
E = AAIR.parent
ROOT = Path(__file__).resolve().parents[6]
BUILD = REV / "build"
WORK = REV / "_work"
NAME = "paper_e_aair_rev1"
SUBMITTED_DOCX = AAIR / "submission" / "paper_e_aair_manuscript.docx"

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
  $c = $w.CompareDocuments($o, $r, 2, 1, $true, $true, $true, $true, $true, $true, $true, $true, $true, $true, "Author", $true)
  $c.SaveAs2($out, 12)
  $c.ActiveWindow.View.RevisionsFilter.Markup = 2
  $c.ActiveWindow.View.ShowRevisionsAndComments = $true
  $c.ExportAsFixedFormat($pdf, 17, $false, 0, 0, 1, 1, 7, $true, $true, 0, $true, $true, $false)
  "revisions=" + $c.Revisions.Count
} finally {
  foreach ($d in @($c, $r, $o)) { if ($d) { try { $d.Close(0) } catch {} } }
  $w.Quit()
}
"""
PAGE_BREAK = '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```'


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_snapshot() -> None:
    bad = []
    for line in (REV / "SUBMITTED_SNAPSHOT.sha256").read_text(encoding="utf-8").splitlines():
        digest, rel = line.split(maxsplit=1)
        path = E / rel.lstrip("*")
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            bad.append(rel)
    if bad:
        sys.exit(f"refusing to build: submitted files changed: {bad}")


def paragraphs(docx: Path) -> list[str]:
    """Text of each paragraph, equation text included; a sign is U+2212 in either form."""
    xml = zipfile.ZipFile(docx).read("word/document.xml").decode("utf-8")
    out = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S):
        t = "".join(re.findall(r"<(?:w|m):t(?: [^>]*)?>([^<]*)</(?:w|m):t>", p))
        t = re.sub(r"(?<![A-Za-z])-(?=\d)", "−", t)
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            out.append(t)
    return out


def baseline(builder) -> Path:
    """The submitted source through today's pipeline; registry untouched."""
    work = WORK / "baseline"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    builder.SOURCE = AAIR / "paper_e_aair_template.tex"
    builder.RENDERED = work / "paper_e_aair_submitted.tex"
    builder.OUT = work
    builder.NAME = "paper_e_aair_submitted"
    tex, numbers = builder.render()
    out, _ = builder.build_manuscript(tex)
    builder.verify_numbers(out, tex, numbers)
    builder.word_pass(out, builder.RUNNING_HEAD, builder.AUTHOR)
    a, b = paragraphs(out), paragraphs(SUBMITTED_DOCX)
    if a != b:
        import difflib
        diff = [l for l in difflib.unified_diff(b, a, lineterm="", n=0) if l[:1] in "+-"][2:6]
        sys.exit(f"the rebuilt baseline differs from the submitted .docx: {diff}")
    print("baseline: submitted source rebuilt; text identical to the submitted .docx (signs aside)")
    return out


def compare(original: Path, revised: Path, out: Path) -> None:
    script = WORK / "_compare.ps1"
    script.write_text(COMPARE_PS1, encoding="utf-8")
    for p in (out, out.with_suffix(".pdf")):
        p.unlink(missing_ok=True)
    r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script),
                        str(original), str(revised), str(out), str(out.with_suffix(".pdf"))],
                       capture_output=True, text=True)
    if r.returncode or not out.exists():
        sys.exit(f"Word comparison failed:\n{r.stdout[-1200:]}\n{r.stderr[-1200:]}")
    m = re.search(r"revisions=(\d+)", r.stdout)
    print(f"changes marked: {m.group(1) if m else '?'} Word revisions")


def justify(docx: Path) -> None:
    """Justify the body text of the letter (author request, 2026-11-25): the paragraph
    styles pandoc writes for prose and quotes are set to justified (python-docx keeps the
    schema order of w:pPr, which Word requires)."""
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    doc = Document(str(docx))
    for name in ("Normal", "Body Text", "First Paragraph", "Block Text", "Compact"):
        try:
            doc.styles[name].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        except KeyError:
            pass
    doc.save(str(docx))


def letter_markdown() -> str:
    text = (REV / "RESPONSE_TO_REVIEWERS.md").read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = text[text.index("Dear "):]                                  # internal header dropped
    text = re.sub(r"(?m)^---\s*$", "", text)
    text = re.sub(r"\s*\((?:C-\d{3}(?:,\s*)?)+\)", "", text)            # internal change ids
    keep = []
    for line in text.splitlines():
        if line.startswith("## Reviewer"):
            keep += ["", PAGE_BREAK, ""]
        keep.append(line)
    out = "\n".join(keep).strip()
    if re.search(r"_\[|C-\d{3}|pending", out):
        sys.exit("the response letter still holds an open placeholder or an internal id")
    return out.lstrip("-\n ")


def main() -> int:
    check_snapshot()
    BUILD.mkdir(exist_ok=True)
    WORK.mkdir(exist_ok=True)
    builder = load(AAIR / "scripts" / "build_paper_e_aair_docx.py", "aair_builder")
    try:
        base = baseline(builder)
        builder = load(AAIR / "scripts" / "build_paper_e_aair_docx.py", "aair_builder_rev1")
        sys.argv = [sys.argv[0]]
        if builder.main():
            sys.exit("revised manuscript build failed")
        revised = BUILD / f"{NAME}_manuscript.docx"
        marked = BUILD / f"{NAME}_changes_marked.docx"
        compare(base, revised, marked)
        letter_md = WORK / "response.md"
        letter_md.write_text(letter_markdown(), encoding="utf-8")
        letter = BUILD / f"{NAME}_response.docx"
        r = subprocess.run(["quarto", "pandoc", str(letter_md), "-f", "markdown", "-t", "docx", "-o", str(letter)],
                           capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"pandoc failed on the response letter: {r.stderr[-800:]}")
        justify(letter)
        builder.OUT = WORK
        pages = builder.word_pass(letter, "Response to the editor and reviewers", builder.AUTHOR)
        print(f"response letter: {pages} pages")
    finally:
        shutil.rmtree(WORK, ignore_errors=True)
    check_snapshot()
    for f in sorted(BUILD.iterdir()):
        print(f"  {f.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
