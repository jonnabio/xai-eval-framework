#!/usr/bin/env python3
"""Paper B revision 1: check that every reviewer item is answered and every change tracked.

    python docs/reports/paper_b/ci_journal/revision_1/scripts/check_revision.py
    python docs/reports/paper_b/ci_journal/revision_1/scripts/check_revision.py --final

Checks:
1. The submitted files are unchanged (SUBMITTED_SNAPSHOT.sha256).
2. Every item ID of REVIEW_ANALYSIS.md has an entry in RESPONSE_TO_REVIEWERS.md, and no entry
   answers an unknown ID.
3. Each entry has a valid status. REMEDIATED needs Changes (existing C-ids) and Where;
   EXPLAINED needs a Response; a REMEDIATED item also needs a Response.
4. Each change of CHANGELOG.md has a unique ID and names existing items (or `none`).
5. A GENERAL item (an assessment without pointers) must be REMEDIATED: its answer names at
   least one concrete place that was revised (author rule, 2026-11-06).
6. --final: no item PENDING, no [DRAFT] placeholder, and every change except C-000 is cited by some answer or
   marked `none`.

Exit code 0 when everything holds (PENDING items are reported, and fail only with --final).
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

REV = Path(__file__).resolve().parents[1]
CI = REV.parent
ID_RE = r"(?:ED-\d+|R1-M\d+|R1-m\d+|R1-\d+|R2-\d+[ab]?)"
STATUSES = {"PENDING", "REMEDIATED", "EXPLAINED"}


def analysis_ids(text: str) -> list[str]:
    out = []
    for i in re.findall(rf"^\| ({ID_RE}) \|", text, flags=re.M):
        if i not in out:
            out.append(i)
    return out


def parse_response(text: str) -> dict[str, dict]:
    entries = {}
    blocks = re.split(rf"^### ({ID_RE})\s*$", text, flags=re.M)
    for i in range(1, len(blocks), 2):
        rid, body = blocks[i], blocks[i + 1]
        fields = {}
        for key in ("Type", "Status", "Changes", "Plan", "Response", "Where"):
            m = re.search(rf"^- \*\*{key}:\*\*[ \t]*(.*?)(?=^- \*\*|\Z|^### |^## )", body,
                          flags=re.M | re.S)
            fields[key.lower()] = (m.group(1).strip() if m else "")
        if rid in entries:
            fields["duplicate"] = True
        entries[rid] = fields
    return entries


def parse_changelog(text: str) -> dict[str, dict]:
    rows = {}
    for line in text.splitlines():
        m = re.match(r"^\| (C-\d{3}) \|", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            rows[m.group(1)] = {"bad": f"{len(cells)} columns"}
            continue
        cid, date, items, where, change, commit = cells[:6]
        rows.setdefault(cid, {"dup": 0})
        rows[cid].update({"date": date, "items": items, "where": where, "change": change,
                          "commit": commit})
        rows[cid]["dup"] = rows[cid].get("dup", 0) + 1
    return rows


def check_snapshot() -> list[str]:
    problems = []
    for line in (REV / "SUBMITTED_SNAPSHOT.sha256").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, name = line.split(maxsplit=1)
        path = (CI / name.strip().lstrip("*")).resolve()
        if not path.exists():
            problems.append(f"submitted file missing: {name}")
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != digest and \
                hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest() != digest and \
                hashlib.sha256(data.replace(b"\n", b"\r\n")).hexdigest() != digest:
            problems.append(f"submitted file CHANGED: {name}")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--final", action="store_true", help="no PENDING item allowed")
    a = ap.parse_args(argv)
    errors: list[str] = check_snapshot()
    ids = analysis_ids((REV / "REVIEW_ANALYSIS.md").read_text(encoding="utf-8"))
    resp = parse_response((REV / "RESPONSE_TO_REVIEWERS.md").read_text(encoding="utf-8"))
    log = parse_changelog((REV / "CHANGELOG.md").read_text(encoding="utf-8"))

    for cid, row in log.items():
        if "bad" in row:
            errors.append(f"{cid}: malformed row ({row['bad']})")
            continue
        if row["dup"] > 1:
            errors.append(f"{cid}: ID used {row['dup']} times")
        if row["items"].lower() != "none":
            for it in re.split(r"[,\s]+", row["items"]):
                if it and it not in ids:
                    errors.append(f"{cid}: unknown item {it!r}")
        if not row["change"]:
            errors.append(f"{cid}: no description")

    missing = [i for i in ids if i not in resp]
    extra = [i for i in resp if i not in ids]
    errors += [f"item {i} has no answer in RESPONSE_TO_REVIEWERS.md" for i in missing]
    errors += [f"answer to unknown item {i}" for i in extra]
    counts = {s: 0 for s in STATUSES}
    cited: set[str] = set()
    for rid, f in resp.items():
        if f.get("duplicate"):
            errors.append(f"{rid}: answered twice")
        st = f["status"].split()[0] if f["status"] else ""
        if st not in STATUSES:
            errors.append(f"{rid}: status {f['status']!r} is not one of {sorted(STATUSES)}")
            continue
        counts[st] += 1
        changes = re.findall(r"C-\d{3}", f["changes"])
        cited.update(changes)
        for c in changes:
            if c not in log:
                errors.append(f"{rid}: cites {c}, which is not in CHANGELOG.md")
        if st == "REMEDIATED":
            if not changes:
                errors.append(f"{rid}: REMEDIATED without any change ID")
            if not f["where"]:
                errors.append(f"{rid}: REMEDIATED without a location (Where)")
            if not f["response"]:
                errors.append(f"{rid}: REMEDIATED without a response text")
        if st == "EXPLAINED" and not f["response"]:
            errors.append(f"{rid}: EXPLAINED without a response text")
        if f.get("type", "").startswith("GENERAL") and st == "EXPLAINED":
            errors.append(f"{rid}: a GENERAL comment must name at least one place that was "
                          "revised (REMEDIATED with a change), not only an explanation")
        if a.final and "[DRAFT" in f["response"]:
            errors.append(f"{rid}: response still contains a [DRAFT] placeholder")
    pending = [r for r, f in resp.items() if f["status"].startswith("PENDING")]
    if a.final:
        errors += [f"{r}: still PENDING" for r in pending]
        for cid, row in log.items():
            if cid != "C-000" and "bad" not in row and row["items"].lower() != "none" \
                    and cid not in cited:
                errors.append(f"{cid}: names items but no answer cites it")

    print(f"items {len(ids)}: {counts['REMEDIATED']} remediated, {counts['EXPLAINED']} explained, "
          f"{counts['PENDING']} pending; changes recorded: {len(log)}; "
          f"submitted files: {'unchanged' if not any('submitted' in e for e in errors) else 'PROBLEM'}")
    for e in errors:
        print(f"ERROR: {e}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
