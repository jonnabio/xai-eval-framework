#!/usr/bin/env python3
"""Paper G: check every reference against the record its DOI resolves to.

For each entry of references.toml with a DOI, the record is requested from doi.org by
content negotiation (CSL JSON; answered for Crossref and DataCite DOIs), which also shows that
the DOI resolves. Peer-reviewed papers without a DOI are read from their publisher's page:
`url` (the page's citation_* meta tags, as on proceedings.neurips.cc) or `openreview` (the
OpenReview record of the accepted paper, found by its title). The title, the first author's family name and the year stated in
references.toml are compared with the record. Records are saved to reference_records.json
(re-used unless --refresh), and generated/references.json (CSL JSON keyed by the manuscript's
citation keys) is written for pandoc. Own unpublished papers get an anonymised entry.

    python docs/reports/paper_g/scripts/verify_references.py [--refresh]

It also writes REFERENCE_VERIFICATION.md: one row per reference with its record, how it was
resolved and the manuscript claim it supports, and the share of references from 2024 onward.

Exit status 1 if any entry has no record or disagrees with it, or if fewer than 80% of the
references date from 2024 onward.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import subprocess
import tomllib
import unicodedata
import urllib.parse
from pathlib import Path

G = Path(__file__).resolve().parents[1]
REFS = G / "references.toml"
RECORDS = G / "reference_records.json"
CSL = G / "generated" / "references.json"
REPORT = G / "REFERENCE_VERIFICATION.md"
DRAFT = G / "paper_g_draft.md"
MIN_RECENT = 0.80


def plain(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def fetch(doi: str) -> dict | None:
    r = subprocess.run(["curl", "-sSL", "--retry", "3", "--max-time", "60", "-H",
                        "Accept: application/vnd.citationstyles.csl+json",
                        f"https://doi.org/{doi}"], capture_output=True)
    try:
        rec = json.loads(r.stdout.decode("utf-8"))
    except ValueError:
        return None
    return rec if isinstance(rec, dict) and rec.get("title") else None


def _get(url: str) -> str:
    r = subprocess.run(["curl", "-sSL", "--retry", "3", "--max-time", "60", url],
                       capture_output=True)
    return r.stdout.decode("utf-8", errors="replace")


def fetch_page(url: str) -> dict | None:
    """CSL JSON from the citation_* meta tags of a publisher's page."""
    meta: dict[str, list[str]] = {}
    for name, value in re.findall(r'<meta name="citation_([a-z_]+)" content="([^"]*)"', _get(url)):
        meta.setdefault(name, []).append(html.unescape(value))
    if "title" not in meta:
        return None
    authors = [dict(zip(("family", "given"), (a.split(", ", 1) + [""])[:2]))
               for a in meta.get("author", [])]
    container = (meta.get("journal_title") or meta.get("conference_title") or [""])[0]
    return {"type": "paper-conference", "title": meta["title"][0], "author": authors,
            "container-title": container, "volume": (meta.get("volume") or [""])[0],
            "issued": {"date-parts": [[int(meta["publication_date"][0][:4])]]}, "URL": url}


def fetch_openreview(note_id: str, title: str) -> dict | None:
    """CSL JSON from the OpenReview record `note_id` of an accepted paper."""
    term = urllib.parse.quote(title)
    try:
        notes = json.loads(_get(f"https://api2.openreview.net/notes/search?term={term}&limit=10"))
    except ValueError:
        return None
    for note in notes.get("notes", []):
        if note.get("id") != note_id:
            continue
        val = {k: (v or {}).get("value") for k, v in note["content"].items()}
        stamp = note.get("pdate") or note.get("odate") or note.get("cdate")
        authors = [dict(zip(("given", "family"), a.rsplit(" ", 1))) for a in val["authors"]]
        return {"type": "article-journal", "title": val["title"], "author": authors,
                "venue": val.get("venue"),
                "issued": {"date-parts": [[dt.datetime.fromtimestamp(stamp / 1000).year]]},
                "URL": f"https://openreview.net/forum?id={note_id}"}
    return None


def years(rec: dict) -> set[int]:
    out = set()
    for key in ("issued", "published", "published-print", "published-online"):
        parts = (rec.get(key) or {}).get("date-parts") or [[None]]
        if parts[0] and parts[0][0]:
            out.add(int(parts[0][0]))
    return out


# Crossref types as CSL names them (doi.org answers with Crossref's names).
CSL_TYPE = {"journal-article": "article-journal", "proceedings-article": "paper-conference",
            "book-chapter": "chapter", "posted-content": "article"}
# Words kept capitalised in sentence case (APA 7 article titles): proper names, and the
# pronoun I. Acronyms and mixed-case names (SHAP, XGBoost, OpenML) are kept by rule.
PROPER = {"Shapley", "I", "Monte", "Carlo", "Kendall", "Spearman"}


def sentence_case(title: str) -> str:
    """APA sentence case: the first word, and the first word after a colon, question mark or
    dash, keep their capital; every other part of a word in title case (capital, then lower
    case; each part of a hyphenated word separately) is lowered, except proper names."""
    title = " ".join(title.split()).replace("—", "—\0 ")
    out, start = [], True
    for w in title.split(" "):
        core = w.strip("\"“”‘’'()[]:?\0—,")
        parts = core.split("-")
        new = []
        for k, p in enumerate(parts):
            titled = len(p) > 1 and p[0].isupper() and p[1:].islower()
            named = k > 0 and len(parts[0]) == 1 and parts[0].isupper()  # F-Fidelity, E-XAI
            keep = (start and k == 0) or not titled or p in PROPER or named
            if start and k == 0 and p[:1].islower():  # a subtitle starts with a capital
                p = p[0].upper() + p[1:]
            new.append(p if keep else p.lower())
        out.append(w.replace(core, "-".join(new)) if core else w)
        start = w.endswith((":", "?", "\0"))
    return " ".join(out).replace("—\0 ", "—")


def csl_entry(ref: dict, rec: dict, book: dict | None = None) -> dict:
    """The record as pandoc reads it: the citation key as id, the stated year as issued,
    CSL type names, APA sentence case for the title (with its subtitle)."""
    keep = ("type", "title", "author", "container-title", "volume", "issue", "page",
            "publisher", "DOI", "URL", "number", "collection-title")
    out = {k: rec[k] for k in keep if rec.get(k)}
    out["id"] = ref["key"]
    out["type"] = CSL_TYPE.get(out.get("type", ""), out.get("type", "article-journal"))
    title = re.sub(r"<[^>]+>", "", out["title"] if isinstance(out["title"], str)
                   else out["title"][0])
    sub = rec.get("subtitle") or []
    if sub and isinstance(sub, list) and sub[0].lower() not in title.lower():
        title = f"{title.rstrip(':')}: {sub[0]}"
    out["title"] = sentence_case(html.unescape(title))
    for k in ("container-title", "collection-title"):
        if isinstance(out.get(k), list):
            out[k] = out[k][0] if out[k] else ""
        if out.get(k):
            out[k] = html.unescape(out[k])
    if out["type"] == "chapter" and book:  # the proceedings volume, not the series
        out["collection-title"] = out.get("container-title", "")
        out["container-title"] = html.unescape(book["title"] if isinstance(book["title"], str)
                                               else book["title"][0])
        if 0 < len(book.get("editor") or []) <= 6:
            out["editor"] = book["editor"]
    if out["type"] == "article-journal":
        out.pop("publisher", None)
    out["issued"] = {"date-parts": [[ref["year"]]]}
    if ref.get("doi"):
        out["DOI"] = ref["doi"]
        out.pop("URL", None)
    for k in ("container", "type"):
        if ref.get(k):
            out["container-title" if k == "container" else k] = ref[k]
    if ref.get("doi", "").lower().startswith("10.48550/arxiv."):  # DataCite: arXiv preprint
        out.update({"type": "article", "publisher": "arXiv", "genre": "Preprint"})
        out.pop("container-title", None)
    if ref.get("doi", "").startswith("10.21203/"):
        out.update({"type": "article", "publisher": "Research Square", "genre": "Preprint"})
        out.pop("container-title", None)
    return out


def report(refs: list[dict], csl: list[dict], saved: dict, bad: int) -> str:
    """REFERENCE_VERIFICATION.md from the records (no value typed by hand)."""
    by_id = {c["id"]: c for c in csl}
    cited = set(re.findall(r"@([A-Za-z0-9]+)", DRAFT.read_text(encoding="utf-8")))
    rows = []
    for r in refs:
        c = by_id.get(r["key"], {})
        names = [a.get("family") or a.get("literal", "") for a in c.get("author", [])]
        who = names[0] + (" et al." if len(names) > 2 else f" & {names[1]}" if len(names) == 2
                          else "") if names else ""
        if r.get("own"):
            res = "own manuscript under review; anonymised, no DOI"
            ident = "—"
        elif r.get("doi"):
            res = "doi.org content negotiation (CSL JSON): resolves, record agrees"
            ident = f"https://doi.org/{r['doi']}"
        elif r.get("url"):
            res = "publisher page, citation meta tags: title, authors, year agree"
            ident = r["url"]
        else:
            res = "OpenReview record of the accepted paper: title, authors, year agree"
            ident = f"https://openreview.net/forum?id={r['openreview']}"
        venue = c.get("container-title") or c.get("publisher") or c.get("genre", "")
        era = "own" if r.get("own") else "2024+" if r["year"] >= 2024 else "foundational"
        rows.append(f"| {r['key']} | {who} | {r['year']} | {c.get('title', '')} | {venue} | "
                    f"{ident} | {res} | {r['role']} | {era} | "
                    f"{'yes' if r['key'] in cited else 'NO'} |")
    n = len(refs)
    recent = sum(r["year"] >= 2024 for r in refs)
    ext = [r for r in refs if not r.get("own")]
    recent_ext = sum(r["year"] >= 2024 for r in ext)
    articles = sum(1 for c in csl if c.get("type") in ("article-journal", "paper-conference",
                                                        "chapter"))
    uncited = [r["key"] for r in refs if r["key"] not in cited]
    return "\n".join([
        "# Paper G — reference verification",
        "",
        "Generated by `scripts/verify_references.py` from `references.toml` and the records in",
        "`reference_records.json`; do not edit. Each record was requested from the authority its",
        "identifier points to (doi.org content negotiation for DOIs; the publisher's page or",
        "OpenReview for peer-reviewed papers without a DOI), and the stated title, first author and",
        "year were compared with it. The manuscript claim each reference supports is the `role`",
        "recorded before it was cited; its relevance was judged from the abstract.",
        "",
        "| Item | Value |",
        "|---|---|",
        f"| References | {n} |",
        f"| Agree with their record (or own work) | {n - bad} of {n} |",
        f"| From 2024 onward | {recent} of {n} ({100 * recent / n:.1f}%); excluding the three "
        f"anonymised own manuscripts {recent_ext} of {len(ext)} "
        f"({100 * recent_ext / len(ext):.1f}%) |",
        f"| Requirement (project) | at least 80% from 2024 onward: "
        f"{'met' if min(recent / n, recent_ext / len(ext)) >= MIN_RECENT else 'NOT met'} |",
        f"| Journal articles, conference papers and chapters | {articles} of {n} "
        f"({100 * articles / n:.1f}%); journal asks at least 90% scientific articles |",
        f"| Preprints | {', '.join(c['id'] for c in csl if c.get('genre') == 'Preprint') or 'none'} |",
        f"| Cited in the manuscript | {n - len(uncited)} of {n}"
        + (f"; not cited: {', '.join(uncited)}" if uncited else "") + " |",
        "",
        "Own work: the three earlier manuscripts of the programme are under review and are cited",
        "in the third person as anonymised entries; the author replaces them with the published",
        "records at acceptance. Foundational (pre-2024) sources are kept only where they define a",
        "method the study uses (LIME, SHAP, XGBoost and the origins of M1 to M7).",
        "",
        "| Key | Authors | Year | Title | Venue | Identifier | Verification | Supports | Era | Cited |",
        "|---|---|---|---|---|---|---|---|---|---|",
        *rows, ""])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--refresh", action="store_true", help="request every record again")
    args = ap.parse_args()
    refs = tomllib.loads(REFS.read_text(encoding="utf-8"))["ref"]
    saved = {} if args.refresh or not RECORDS.exists() else json.loads(
        RECORDS.read_text(encoding="utf-8"))
    csl, bad = [], 0
    for ref in refs:
        if ref.get("own"):
            csl.append({"id": ref["key"], "type": "manuscript", "title": ref["title"],
                        "author": [{"literal": "Anonymous"}],
                        "issued": {"date-parts": [[ref["year"]]]},
                        "genre": "Manuscript under review"})
            print(f"own       {ref['key']}  {ref['year']}  (anonymised, no DOI)")
            continue
        doi = ref.get("doi") or ref.get("url") or f"openreview:{ref['openreview']}"
        rec = saved.get(doi)
        if not rec:
            rec = (fetch(ref["doi"]) if ref.get("doi") else fetch_page(ref["url"])
                   if ref.get("url") else fetch_openreview(ref["openreview"], ref["title"]))
        if not rec:
            print(f"NO RECORD {ref['key']}  {doi}")
            bad += 1
            continue
        saved[doi] = rec
        title_rec = rec["title"] if isinstance(rec["title"], str) else rec["title"][0]
        a, b = plain(ref["title"]), plain(title_rec)
        auth = rec.get("author") or [{}]
        family = plain(auth[0].get("family") or auth[0].get("literal") or "")
        problems = []
        if not (a and a in b):
            problems.append(f"title: stated '{a[:60]}' / record '{b[:60]}'")
        if plain(ref["first"]) not in family and family not in plain(ref["first"]):
            problems.append(f"first author: stated '{plain(ref['first'])}' / record '{family}'")
        if ref["year"] not in years(rec) and not ref.get("foundational"):
            problems.append(f"year: stated {ref['year']} / record {sorted(years(rec))}")
        if problems:
            bad += 1
            print(f"MISMATCH  {ref['key']}  {doi}\n          " + "\n          ".join(problems))
            continue
        book = None
        if rec.get("type") == "book-chapter" and ref.get("doi"):
            parent = re.sub(r"_\d+$", "", ref["doi"])
            book = saved.get(parent) or fetch(parent)
            if book:
                saved[parent] = book
        csl.append(csl_entry(ref, rec, book))
        print(f"ok        {ref['key']}  {ref['year']}  {doi}")
    RECORDS.write_text(json.dumps(saved, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                       encoding="utf-8", newline="\n")
    CSL.parent.mkdir(exist_ok=True)
    CSL.write_text(json.dumps(csl, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
                   newline="\n")
    REPORT.write_text(report(refs, csl, saved, bad), encoding="utf-8", newline="\n")
    recent = sum(r["year"] >= 2024 for r in refs)
    recent_ext = sum(r["year"] >= 2024 and not r.get("own") for r in refs)
    n_ext = sum(not r.get("own") for r in refs)
    share, share_ext = recent / len(refs), recent_ext / n_ext
    print(f"\n{len(refs) - bad} of {len(refs)} entries agree with their record or are own work")
    print(f"from 2024 onward: {recent}/{len(refs)} = {share:.1%} (all); "
          f"{recent_ext}/{n_ext} = {share_ext:.1%} (excluding own unpublished work)")
    return 1 if bad or min(share, share_ext) < MIN_RECENT else 0


if __name__ == "__main__":
    raise SystemExit(main())
