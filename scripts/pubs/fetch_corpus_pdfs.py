#!/usr/bin/env python3
"""Retrieve open-access PDFs for the Paper B+C review corpus.

Resolution order per paper:

1. arXiv id from the manuscript bibliography, if it carries one.
2. DOI from the bibliography -> OpenAlex, which reports open-access PDF
   locations. Only `best_oa_location` / `oa_locations` are used, so a paywalled
   record simply yields nothing.
3. No identifier -> arXiv API title search, accepted only if the returned title
   matches the requested one closely.

Every download is verified before it counts: PDF magic bytes, a size floor, and
a page-one text match against the expected title. A landing page or cookie wall
saved with a .pdf extension fails verification and is deleted.

Nothing is ever substituted. If the correct paper cannot be obtained openly the
entry is recorded FAILED, because a missing row is honest and a wrong row
silently corrupts the corpus.

Usage:
    python scripts/pubs/fetch_corpus_pdfs.py [--only KEY ...] [--limit N] [--dry-run]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

import fitz  # PyMuPDF


ROOT = Path(__file__).resolve().parents[2]
BC = ROOT / "docs" / "reports" / "paper_bc"
MANIFEST = BC / "corpus_pdf_manifest.csv"
PDF_DIR = BC / "corpus_pdfs"
LEDGER = PDF_DIR / "RETRIEVAL_LOG.md"

UA = "Mozilla/5.0 (compatible; academic-corpus-retrieval/1.0)"
MIN_BYTES = 50_000
STOP = {"the", "and", "for", "with", "from", "that", "this", "are", "not", "its",
        "via", "using", "towards", "toward", "their", "how", "what", "why", "can",
        "does", "should", "␣"}


def toks(s: str) -> set[str]:
    s = re.sub(r"[^a-z0-9]+", " ", s.lower())
    return {w for w in s.split() if len(w) > 3 and w not in STOP}


def title_overlap(want: str, got: str) -> float:
    a, b = toks(want), toks(got)
    if not a:
        return 0.0
    return len(a & b) / len(a)


def curl(url: str, dest: Path | None = None, timeout: int = 45) -> bytes | None:
    cmd = ["curl", "-sSL", "--max-time", str(timeout), "-A", UA, url]
    if dest:
        cmd += ["-o", str(dest)]
    try:
        res = subprocess.run(cmd, capture_output=True, timeout=timeout + 15)
    except subprocess.TimeoutExpired:
        return None
    if res.returncode != 0:
        return None
    return res.stdout if not dest else b""


def get_json(url: str) -> dict | None:
    raw = curl(url, timeout=30)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def arxiv_id_from(link: str) -> str | None:
    m = re.search(r"arxiv\.org/abs/([0-9.]+)", link)
    if m:
        return m.group(1)
    m = re.search(r"arXiv\.(\d{4}\.\d{4,5})", link)
    if m:
        return m.group(1)
    return None


def arxiv_search(title: str) -> tuple[str, str] | None:
    q = urllib.parse.quote(f'ti:"{title}"')
    url = f"http://export.arxiv.org/api/query?search_query={q}&max_results=5"
    raw = curl(url, timeout=30)
    if not raw:
        return None
    text = raw.decode("utf-8", "ignore")
    ids = re.findall(r"<id>http://arxiv\.org/abs/([^<]+)</id>", text)
    titles = re.findall(r"<title>(.*?)</title>", text, re.S)[1:]  # first is feed title
    for aid, t in zip(ids, titles):
        t = re.sub(r"\s+", " ", t).strip()
        if title_overlap(title, t) >= 0.7:
            return aid.split("v")[0], t
    return None


def openalex_pdf(doi: str) -> str | None:
    doi = doi.replace("https://doi.org/", "").strip()
    data = get_json(f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi)}")
    if not data:
        return None
    best = data.get("best_oa_location") or {}
    if best.get("pdf_url"):
        return best["pdf_url"]
    for loc in data.get("locations") or []:
        if loc.get("is_oa") and loc.get("pdf_url"):
            return loc["pdf_url"]
    return None


def verify(path: Path, want_title: str) -> tuple[bool, str]:
    if not path.exists():
        return False, "no file written"
    size = path.stat().st_size
    if size < MIN_BYTES:
        return False, f"too small ({size} bytes) -- probably a landing page"
    with path.open("rb") as fh:
        if fh.read(5) != b"%PDF-":
            return False, "not a PDF (missing %PDF header)"
    try:
        with fitz.open(path) as doc:
            if doc.page_count == 0:
                return False, "PDF has no pages"
            text = doc.load_page(0).get_text()
    except Exception as exc:  # noqa: BLE001
        return False, f"unreadable PDF: {exc}"
    head = re.sub(r"\s+", " ", text[:3000])
    score = title_overlap(want_title, head)
    if score < 0.55:
        return False, f"page-1 text does not match title (overlap {score:.2f})"
    return True, f"verified (title overlap {score:.2f}, {size // 1024} KB)"


def resolve(row: dict) -> list[tuple[str, str]]:
    """Return every candidate (url, how) pair, best first.

    All sources are collected rather than stopping at the first that yields a
    URL: a DOI can resolve to an open-access record that is the wrong paper (as
    OpenAlex did for ali2023trustworthy) or to a landing page, and the arXiv or
    ACL copy is then the one that verifies. The caller tries each in turn and
    keeps the first that passes verification.
    """
    out: list[tuple[str, str]] = []
    link = row["link"].strip()

    aid = arxiv_id_from(link)
    if aid:
        out.append((f"https://arxiv.org/pdf/{aid}", f"arXiv {aid} (from bibliography)"))

    if link.startswith("https://doi.org/") and "arXiv" not in link:
        doi = link.replace("https://doi.org/", "")
        # ACL Anthology DOIs map directly onto a stable PDF URL.
        if doi.startswith("10.18653/v1/"):
            slug = doi.split("10.18653/v1/")[1]
            out.append((f"https://aclanthology.org/{slug}.pdf", "ACL Anthology"))
        pdf = openalex_pdf(link)
        if pdf:
            out.append((pdf, "OpenAlex open-access location (via DOI)"))

    found = arxiv_search(row["title"])
    if found:
        aid2, matched = found
        out.append((f"https://arxiv.org/pdf/{aid2}",
                    f"arXiv {aid2} (title search: {matched[:60]})"))

    # OpenAlex parses `filter=title.search:<value>` on the colon, so punctuation
    # inside the title breaks the query and it silently returns nothing. Search
    # on the leading alphanumeric words instead.
    words = re.sub(r"[^A-Za-z0-9 ]+", " ", row["title"]).split()
    q = urllib.parse.quote(" ".join(words[:10]))
    data = get_json(f"https://api.openalex.org/works?filter=title.search:{q}&per-page=3")
    # Collect across every matching record rather than stopping at the first:
    # the same paper often appears as both a publisher entry (frequently behind
    # bot protection) and an arXiv entry that actually downloads.
    for work in (data or {}).get("results", []):
        if title_overlap(row["title"], work.get("title") or "") >= 0.7:
            for loc in [work.get("best_oa_location") or {}] + (work.get("locations") or []):
                if loc.get("pdf_url"):
                    out.append((loc["pdf_url"], "OpenAlex title search"))

    seen, uniq = set(), []
    for url, how in out:
        if url not in seen:
            seen.add(url)
            uniq.append((url, how))
    return uniq


def load_ledger() -> dict:
    state: dict[str, dict] = {}
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\|\s*`?([a-z0-9_]+)`?\s*\|\s*(DONE|FAILED|PENDING)\s*\|(.*?)\|(.*?)\|", line)
            if m:
                state[m.group(1)] = {"status": m.group(2), "url": m.group(3).strip(),
                                     "note": m.group(4).strip()}
    return state


def write_ledger(rows: list[dict], state: dict) -> None:
    out = ["# Corpus PDF retrieval log", "",
           "Written by `scripts/pubs/fetch_corpus_pdfs.py`. STATUS is DONE, FAILED or PENDING.",
           "", "| citation_key | status | source_url | note |", "|---|---|---|---|"]
    for row in rows:
        k = row["citation_key"]
        st = state.get(k, {"status": "PENDING", "url": "", "note": ""})
        out.append(f"| `{k}` | {st['status']} | {st['url']} | {st['note']} |")
    done = sum(1 for s in state.values() if s["status"] == "DONE")
    failed = sum(1 for s in state.values() if s["status"] == "FAILED")
    out += ["", f"**{done} DONE · {failed} FAILED · {len(rows) - done - failed} PENDING**"]
    LEDGER.write_text("\n".join(out) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Retrieve open-access corpus PDFs.")
    ap.add_argument("--only", nargs="*", help="restrict to these citation keys")
    ap.add_argument("--limit", type=int, help="stop after N attempts")
    ap.add_argument("--dry-run", action="store_true", help="resolve URLs but do not download")
    ap.add_argument("--retry-failed", action="store_true", help="re-attempt FAILED entries")
    args = ap.parse_args(argv)

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open(encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["status"] == "missing"]
    if args.only:
        rows = [r for r in rows if r["citation_key"] in set(args.only)]

    state = load_ledger()
    attempts = 0

    for row in rows:
        key = row["citation_key"]
        prior = state.get(key, {}).get("status")
        target = PDF_DIR / f"{key}.pdf"
        if target.exists() and prior == "DONE":
            continue
        if prior == "FAILED" and not args.retry_failed:
            continue
        if args.limit and attempts >= args.limit:
            break
        attempts += 1

        candidates = resolve(row)
        if not candidates:
            state[key] = {"status": "FAILED", "url": "",
                          "note": "no open-access PDF found (arXiv + OpenAlex)"}
            print(f"FAILED  {key:<28} no open-access location")
            write_ledger(rows, state)
            time.sleep(0.4)
            continue

        if args.dry_run:
            url, how = candidates[0]
            print(f"DRY     {key:<28} {how}\n            -> {url}")
            continue

        ok = False
        for url, how in candidates:
            curl(url, dest=target)
            good, note = verify(target, row["title"])
            if good:
                state[key] = {"status": "DONE", "url": url, "note": f"{how}; {note}"}
                print(f"DONE    {key:<28} {note}")
                ok = True
                break
            target.unlink(missing_ok=True)
            last = note
        if not ok:
            state[key] = {"status": "FAILED", "url": candidates[0][0],
                          "note": f"download failed verification: {last}"}
            print(f"FAILED  {key:<28} {last}")

        write_ledger(rows, state)
        time.sleep(0.6)

    write_ledger(rows, state)
    done = sum(1 for s in state.values() if s["status"] == "DONE")
    failed = sum(1 for s in state.values() if s["status"] == "FAILED")
    print(f"\n{done} DONE, {failed} FAILED, {len(rows) - done - failed} PENDING "
          f"(of {len(rows)} tracked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
