#!/usr/bin/env python3
"""Paper E, AAIR revision 1: final check before upload.

    .venv/Scripts/python.exe docs/reports/paper_e/aair_journal/revision_1/scripts/check_revision.py

1. Every item of REVIEW_ANALYSIS.md has an answer (**ID.**) in RESPONSE_TO_REVIEWERS.md.
2. Every C-### cited in the letter exists in CHANGELOG.md.
3. The submitted files match SUBMITTED_SNAPSHOT.sha256.
4. The built files exist, the letter has no placeholder, and the manuscript signs are text (RCA-007).
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

REV = Path(__file__).resolve().parents[1]
E = REV.parents[1]
problems = []
items = set(re.findall(r"^\| ((?:ED|R[123])-\d+) ", (REV / "REVIEW_ANALYSIS.md").read_text(encoding="utf-8"), re.M))
letter = (REV / "RESPONSE_TO_REVIEWERS.md").read_text(encoding="utf-8")
answered = set(re.findall(r"\*\*((?:ED|R[123])-\d+)\.", letter))
problems += [f"item not answered: {i}" for i in sorted(items - answered)]
changes = set(re.findall(r"^\| (C-\d{3}) ", (REV / "CHANGELOG.md").read_text(encoding="utf-8"), re.M))
problems += [f"letter cites unknown change {c}" for c in sorted(set(re.findall(r"C-\d{3}", letter)) - changes)]
for line in (REV / "SUBMITTED_SNAPSHOT.sha256").read_text(encoding="utf-8").splitlines():
    digest, rel = line.split(maxsplit=1)
    p = E / rel.lstrip("*")
    if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != digest:
        problems.append(f"submitted file changed: {rel}")
if re.search(r"_\[|pending|ZENODOPENDING", letter, re.I):
    problems.append("placeholder left in the letter")
for f in ("paper_e_aair_rev1_manuscript.docx", "paper_e_aair_rev1_manuscript.pdf",
          "paper_e_aair_rev1_changes_marked.docx", "paper_e_aair_rev1_changes_marked.pdf",
          "paper_e_aair_rev1_response.docx", "paper_e_aair_rev1_response.pdf",
          "supplement/paper_e_aair_rev1_supplement.docx", "supplement/paper_e_aair_rev1_supplement.pdf"):
    if not (REV / "build" / f).exists():
        problems.append(f"missing build output: {f}")
r = subprocess.run([sys.executable, str(REV / "scripts" / "check_signs.py")], capture_output=True, text=True)
if r.returncode:
    problems.append("sign check failed: " + (r.stderr or r.stdout)[-300:])
if problems:
    sys.exit("NOT READY:\n  " + "\n  ".join(problems))
print(f"READY: {len(items)} items answered, {len(changes)} changes logged, submitted files unchanged, "
      "outputs built, signs are text")
