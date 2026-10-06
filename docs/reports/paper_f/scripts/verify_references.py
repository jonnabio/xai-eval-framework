#!/usr/bin/env python3
"""Paper F: check every reference against the record its DOI resolves to.

For each entry of references.bib that has a DOI, the record is requested from doi.org
(content negotiation, CSL JSON; it answers for Crossref and for DataCite DOIs) and the
title, the first author's family name and the year are compared with the entry. The
records are saved to reference_records.json, so that the check can be read later.

    python docs/reports/paper_f/scripts/verify_references.py            # report
    python docs/reports/paper_f/scripts/verify_references.py --mark     # also write `checked`

An entry that agrees gets the field `checked = {date}` with --mark. The year of the bib
entry may be the year of the volume or the year of first publication online; both are
accepted when the record carries them.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import unicodedata
from pathlib import Path

F = Path(__file__).resolve().parents[1]
BIB = F / "references.bib"
RECORDS = F / "reference_records.json"
ENTRY = re.compile(r"^@(\w+)\{([^,]+),(.*?)(?=^@|\Z)", re.M | re.S)


def field(body: str, name: str) -> str:
    m = re.search(rf"\b{name}\s*=\s*\{{(.*?)\}}\s*(?:,|\}}\s*$)", body, re.S)
    return m.group(1).strip() if m else ""


def plain(text: str) -> str:
    text = re.sub(r"\\[a-zA-Z]+\s*|[{}\\'\"`^~.]", "", text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def fetch(doi: str) -> dict | None:
    r = subprocess.run(["curl", "-sSL", "--retry", "3", "--max-time", "60", "-H",
                        "Accept: application/vnd.citationstyles.csl+json",
                        f"https://doi.org/{doi}"], capture_output=True)
    try:
        return json.loads(r.stdout.decode("utf-8"))
    except ValueError:
        return None


def years(rec: dict) -> set[int]:
    out = set()
    for key in ("issued", "published", "published-print", "published-online", "created"):
        parts = (rec.get(key) or {}).get("date-parts") or [[None]]
        if parts[0] and parts[0][0]:
            out.add(int(parts[0][0]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mark", action="store_true")
    args = ap.parse_args()
    bib = BIB.read_text(encoding="utf-8")
    saved = json.loads(RECORDS.read_text(encoding="utf-8")) if RECORDS.exists() else {}
    today = dt.date.today().isoformat()
    ok_keys, bad = [], 0
    for kind, key, body in ENTRY.findall(bib):
        doi = field(body, "doi")
        if not doi:
            print(f"NO DOI    {key}")
            bad += 1
            continue
        rec = saved.get(doi) or fetch(doi)
        if not rec or "title" not in rec:
            print(f"NO RECORD {key}  {doi}")
            bad += 1
            continue
        saved[doi] = rec
        title_rec = rec["title"] if isinstance(rec["title"], str) else rec["title"][0]
        a, b = plain(field(body, "title")), plain(re.sub(r"<[^>]+>", "", title_rec))
        family = plain((rec.get("author") or [{}])[0].get("family", ""))
        first = plain(field(body, "author").split(" and ")[0].split(",")[0])
        year = int(field(body, "year") or 0)
        problems = []
        if not (a == b or a in b or b in a):
            problems.append(f"title: bib '{a[:60]}' / record '{b[:60]}'")
        if family and first and family != first:
            problems.append(f"first author: bib '{first}' / record '{family}'")
        if year not in years(rec):
            problems.append(f"year: bib {year} / record {sorted(years(rec))}")
        if problems:
            bad += 1
            print(f"MISMATCH  {key}  {doi}\n          " + "\n          ".join(problems))
        else:
            ok_keys.append(key)
            print(f"ok        {key}  {year}  {doi}")
    RECORDS.write_text(json.dumps(saved, indent=1, sort_keys=True, ensure_ascii=False),
                       encoding="utf-8", newline="\n")
    if args.mark:
        for key in ok_keys:
            pat = re.compile(r"(^@\w+\{" + re.escape(key) + r",.*?)(\}\s*)(?=^@|\Z)", re.M | re.S)
            m = pat.search(bib)
            body = re.sub(r",?\s*checked\s*=\s*\{[^}]*\}", "", m.group(1)).rstrip().rstrip(",")
            bib = bib[:m.start()] + body + f",\n  checked = {{{today}}}}}\n\n" + bib[m.end():]
        BIB.write_text(bib.rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"\n{len(ok_keys)} agree with their record, {bad} do not")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
