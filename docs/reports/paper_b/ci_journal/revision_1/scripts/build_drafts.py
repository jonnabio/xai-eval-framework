#!/usr/bin/env python3
"""Paper B revision 1: render the DRAFTS awaiting the author's approval (read-only on sources).

    python docs/reports/paper_b/ci_journal/revision_1/scripts/build_drafts.py

Writes to build/drafts/:
- paper_b_ci_rev1_response_DRAFT.docx/.pdf: every reviewer comment (quoted from
  RESPONSE_TO_REVIEWERS.md) with the elaborated draft answer of PROPOSAL_2026-11-06.md Part C
  and the proposed manuscript changes (Part B) that implement it.
- paper_b_ci_rev1_proposed_changes_DRAFT.docx/.pdf: Parts A, B and D of the proposal (length
  plan, change list P-01..P-24, decisions).

Nothing in the manuscript, RESPONSE_TO_REVIEWERS.md or CHANGELOG.md is modified: these are
renders of proposals, not of approved changes.
"""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

REV = Path(__file__).resolve().parents[1]
CI = REV.parent
OUT = REV / "build" / "drafts"
PROPOSAL = REV / "PROPOSAL_2026-11-06.md"
ID_RE = r"(?:ED-\d+|R1-M\d+|R1-m\d+|R1-\d+|R2-\d+[ab]?)"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parts(text: str) -> dict[str, str]:
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^## Part ([A-D])\.", line)
        if m:
            cur = m.group(1)
            out[cur] = ""
        if cur:
            out[cur] += line + "\n"
    return out


def draft_answers(part_c: str) -> dict[str, str]:
    answers: dict[str, str] = {}
    cur = None
    for line in part_c.splitlines():
        m = re.match(rf"^\*\*({ID_RE}) \(", line)
        if m:
            cur = m.group(1)
            answers[cur] = line
            continue
        if line.startswith("### ") or line.startswith("---") or line.startswith("## "):
            cur = None
            continue
        if cur:
            answers[cur] += "\n" + line
    # Drop the bold label "**ID (topic).**" from the answer text; keep the topic.
    clean = {}
    for k, v in answers.items():
        m = re.match(r"^\*\*[^(]+\((.*?)\)\.\*\*\s*", v, flags=re.S)
        topic = re.sub(r";\s*Type GENERAL", "", m.group(1)) if m else ""
        clean[k] = (topic, v[m.end():].strip()) if m else ("", v.strip())
    return clean


def change_rows(part_b: str) -> dict[str, list[tuple[str, str, str]]]:
    by_item: dict[str, list[tuple[str, str, str]]] = {}
    for line in part_b.splitlines():
        m = re.match(r"^\| (P-\d+) \| ([^|]*) \| ([^|]*) \| ([^|]*) \|", line)
        if not m:
            continue
        pid, _kind, items, where = (g.strip() for g in m.groups())
        for it in re.findall(ID_RE, items):
            by_item.setdefault(it, []).append((pid, where, items))
    return by_item


def quotes() -> list[tuple[str, str, str]]:
    """(section heading, id, quoted comment) in the order of RESPONSE_TO_REVIEWERS.md."""
    text = (REV / "RESPONSE_TO_REVIEWERS.md").read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    out, section = [], ""
    blocks = re.split(rf"^(## .*|### {ID_RE})\s*$", text, flags=re.M)
    for i in range(1, len(blocks), 2):
        head, body = blocks[i], blocks[i + 1]
        if head.startswith("## "):
            section = head[3:].strip()
            continue
        q = "\n".join(l for l in body.splitlines() if l.startswith(">"))
        out.append((section, head[4:].strip(), q))
    return out


def widen(md: str) -> str:
    """Give each pipe-table column a width proportional to its longest cell (pandoc reads the
    relative widths from the dashes of the separator line)."""
    lines, out, i = md.splitlines(), [], 0
    while i < len(lines):
        if i + 1 < len(lines) and lines[i].startswith("|") and \
                re.match(r"^\|(\s*:?-+:?\s*\|)+\s*$", lines[i + 1]):
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            rows = [[c.strip() for c in l.strip().strip("|").split("|")]
                    for k, l in enumerate(lines[i:j]) if k != 1]
            n = len(rows[0])
            w = [max(8, len(rows[0][c]) + 3,
                     min(70, max(len(r[c]) if c < len(r) else 0 for r in rows)))
                 for c in range(n)]
            out += [lines[i], "|" + "|".join("-" * x for x in w) + "|", *lines[i + 2:j]]
            i = j
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out) + "\n"


def render(md: str, stem: str, title: str, builder) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    md = widen(md)
    src = OUT / f"_{stem}.md"
    src.write_text(md, encoding="utf-8")
    docx = OUT / f"{stem}.docx"
    r = subprocess.run(["quarto", "pandoc", str(src), "-f", "markdown", "-t", "docx", "-o",
                        str(docx)], capture_output=True, text=True)
    src.unlink(missing_ok=True)
    if r.returncode:
        sys.exit(f"pandoc failed on {stem}: {r.stderr[-800:]}")
    builder.OUT = OUT
    print(stem, builder.word_pass(docx, title, ""))
    builder.check_masked(docx)
    return docx


def main() -> int:
    builder = load(CI / "scripts" / "build_paper_b_ci_docx.py", "build_paper_b_ci_docx")
    p = parts(PROPOSAL.read_text(encoding="utf-8"))
    ans, rows = draft_answers(p["C"]), change_rows(p["B"])
    missing = []
    head = ("# Response to the editor and the reviewers — DRAFT\n\n"
            "Manuscript 2067810, *When Does SHAP Outperform LIME? Model- and "
            "Configuration-Dependent Results from a Paired Tabular Benchmark*, *Computers and "
            "Informatics*. Major revision of 2026-11-06.\n\n"
            "> **DRAFT for the author's approval — not sent.** The answers describe the "
            "*proposed* revision (PROPOSAL_2026-11-06.md); none of it is applied to the "
            "manuscript yet. Text in [R: …] is filled from the new experimental cohort (B2) "
            "when its results are in. Proposed changes P-xx are listed in the companion "
            "document *Proposed manuscript changes — DRAFT*.\n")
    md, section = [head], None
    for sec, rid, q in quotes():
        if sec != section:
            md.append(f"\n## {sec}\n")
            section = sec
        topic, text = ans.get(rid, ("", ""))
        if not text:
            missing.append(rid)
            text = "**[NO DRAFT ANSWER]**"
        md.append(f"\n### {rid}{' — ' + topic if topic else ''}\n\n{q}\n\n**Response.** {text}\n")
        if rid in rows:
            lst = "; ".join(f"{pid} ({where})" for pid, where, _ in rows[rid])
            md.append(f"\n*Proposed changes in the manuscript:* {lst}\n")
    render("".join(md), "paper_b_ci_rev1_response_DRAFT", "Response to the reviewers (draft)",
           builder)

    prop = ("# Proposed manuscript changes — DRAFT\n\n"
            "Manuscript 2067810, revision 1. **For the author's approval: nothing below is "
            "applied yet.** Kind: T = text only, can be written now; R = needs the results of "
            "cohort B2; T+R = both. Page effect: − shorter, 0 neutral, + longer.\n\n")
    body = p["A"] + "\n" + p["B"] + "\n" + p["D"]
    body = re.sub(r"^## ", "## ", body, flags=re.M)
    render(prop + body, "paper_b_ci_rev1_proposed_changes_DRAFT",
           "Proposed manuscript changes (draft)", builder)
    if missing:
        print("WARNING: items without a draft answer:", ", ".join(missing))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
