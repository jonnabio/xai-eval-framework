#!/usr/bin/env python3
"""Partition thesis/references.bib into the working bibliography and a legacy file.

Context (review 2026-08-29): references.bib carried 166 entries of which only 68
were cited. The uncited remainder is not random -- it is a deep-learning /
computer-vision / NLP / RL bibliography left over from an earlier draft, plus a
block of `ref_NN` placeholder entries auto-imported from a reference manager
(@misc with only a `note` field, no author/title/year, so citeproc cannot render
them properly).

Three classes:

  LEGACY   out of scope for a thesis on XAI evaluation. Moved to
           references_legacy.bib, not deleted: the entries stay recoverable and
           out of the artifact the thesis publishes.
  PROMOTE  genuinely required citations that were sitting uncited. Rewritten as
           proper BibTeX entries and cited in the text.
  REVIEW   XAI-adjacent, defensible to cite but not required. Left in
           references.bib and reported, for the author to accept or drop. They
           are NOT auto-inserted: adding a citation to consume a bibliography
           entry is padding, not scholarship.

Duplicate keys are handled here too. goodfellow2014 and hinton2006 were each
defined twice with *different* papers, so BibTeX silently resolved each to
whichever it parsed last. Both pairs fall in LEGACY, which removes the ambiguity.

Usage:  python scripts/pubs/triage_bibliography.py [--apply]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BIB = ROOT / "thesis" / "references.bib"
LEGACY = ROOT / "thesis" / "references_legacy.bib"

# Out of scope: DL/CV/NLP/RL/GNN foundations and placeholder imports.
LEGACY_KEYS = {
    # deep learning / architectures / optimisation
    "turing1950", "lloyd1982", "rumelhart1986", "elman1990", "watkins1992",
    "williams1992", "ester1996", "hochreiter1997a", "hochreiter1997b",
    "lecun1998", "gers2000", "graves2005", "hinton2006", "mccarthy2006",
    "bengio2009", "mikolov2010", "collobertronan2011", "hinton2012",
    "bengio2013", "graves2013", "zeiler2013", "bahdanau2014", "goodfellow2014",
    "graves2014", "kingma2014", "schmidhuber2014", "simonyan2014",
    "sutskever2014", "he2015", "ioffe2015", "kalchbrenner2015", "lecun2015",
    "lipton2015", "mnih2015", "ren2015", "reynolds2015", "zheng2015",
    "schulman2017a", "schulman2017b", "haarnoja2018", "raffel2019",
    "devlin2019a", "devlin2019b", "orvieto2023",
    # graph neural networks
    "wu2020", "zhou2020", "zhou2022", "du2024", "yang2024",
    # generic AI/LLM surveys unrelated to XAI evaluation
    "chang2024", "adeyeye2024", "swamy2024",
    # metadata defect: key says Wiegreffe 2019 ("Attention is not Explanation"),
    # title says Vaswani 2017 ("Attention is all you need"). Uncited; do not
    # reuse without re-verifying which work was intended.
    "wiegreffe2019",
    # placeholder @misc imports, note-only, unrenderable
    "ref_20", "ref_25", "ref_29", "ref_30", "ref_56", "ref_57", "ref_66",
    "ref_104", "ref_109", "ref_110", "ref_111",
}

# Sitting uncited but actually required by the text. Replaced with proper
# entries; the citations are inserted in the manuscript separately.
PROMOTE = {
    "ref_65": """@book{krippendorff2018,
  author = {Krippendorff, Klaus},
  title = {Content Analysis: An Introduction to Its Methodology},
  edition = {4},
  year = {2018},
  publisher = {SAGE Publications},
  address = {Thousand Oaks, CA},
  isbn = {9781506395661},
}""",
    "ref_101": """@techreport{shapley1952,
  author = {Shapley, Lloyd S.},
  title = {A Value for N-Person Games},
  year = {1952},
  institution = {RAND Corporation},
  number = {P-295},
  address = {Santa Monica, CA},
  url = {https://www.rand.org/pubs/papers/P0295.html},
}""",
}

# XAI-adjacent, defensible but not required. Reported, never auto-cited.
REVIEW_KEYS = {
    "cohen1960": "Cohen's kappa -- classic inter-rater agreement; natural companion to the EXP4 reliability discussion",
    "friedman2001": "gradient boosting -- background for the XGBoost model family (Ch.3)",
    "friedman2008": "rule ensembles -- background for rule-based explanation (Anchors, Ch.2)",
    "goldstein2014": "ICE plots -- an XAI method absent from the Ch.2 landscape",
    "apley2020": "ALE plots -- likewise",
    "amershi2014": "interactive ML / role of humans -- human-centered evaluation (Ch.2)",
    "adhikari2022": "missing-data imputation -- relevant to Ch.3's coverage analysis",
    "ji2022": "hallucination in NLG -- relevant to the EXP4 LLM-judge discussion",
    "wang2024": "quantitative evaluation of XAI methods -- directly adjacent to the thesis topic",
    "gnnbenchmark2024": "XAI benchmarking on graphs -- adjacent benchmark, different modality",
    "gomez2023": "credit-risk discriminative power -- domain context for German Credit (EXP3)",
    "khosla2022": "adversarial robustness and explainability",
    "gafur2024": "adversarial robustness and explainability",
    "chen2024": "XAI-based adversarial examples and evaluation",
    "arrieta2019b": "second Arrieta entry; arrieta2019a is cited -- check whether these are the same work",
    "ref_14": "Barocas, Hardt & Narayanan, Fairness and ML -- supports the fairness axis of the taxonomy",
    "ref_35": "Fisher, Rudin & Dominici, model reliance -- permutation-importance foundations",
    "ref_64": "Koh et al., concept bottleneck models -- inherently-interpretable contrast",
    "boppiniti2020": "general XAI survey -- verify venue quality before citing",
    "dwivedi2022": "general XAI survey -- verify venue quality before citing",
    "saeed2023": "XAI meta-survey -- verify venue quality before citing",
    "idris2024": "XAI review -- verify venue quality before citing",
    "aluvalu2024": "XAI in health informatics -- verify venue quality before citing",
    "singh2024": "XAI for education -- verify venue quality before citing",
    "lakshmi2024": "XAI for sustainable development -- verify venue quality before citing",
    "kalasampath2025": "XAI applications review -- verify venue quality before citing",
    "mathew2025": "XAI techniques review -- verify venue quality before citing",
    "choudhari2025": "XAI review -- verify venue quality before citing",
    "mohale2025": "XAI in intrusion detection -- verify venue quality before citing",
    "reif2024": "social evaluation penalty for using AI -- marginal relevance",
}


def entries(text: str) -> list[tuple[str, str]]:
    """Split a .bib file into (key, raw_entry) pairs."""
    out = []
    for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,", text):
        start = m.start()
        depth, i = 0, text.index("{", start)
        while i < len(text):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        out.append((m.group(1), text[start : i + 1]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the files (default: report only)")
    args = ap.parse_args()

    text = BIB.read_text(encoding="utf-8", errors="ignore")
    cited: set[str] = set()
    for qmd in (ROOT / "thesis").glob("*.qmd"):
        body = re.sub(r"`[^`]*`", " ", qmd.read_text(encoding="utf-8", errors="ignore"))
        for m in re.findall(r"@([A-Za-z][A-Za-z0-9_:-]*)", body):
            cited.add(m.rstrip(".,;:)]}"))

    keep, legacy, promoted, seen = [], [], [], set()
    for key, raw in entries(text):
        if key in PROMOTE:
            promoted.append(key)
            keep.append(PROMOTE[key])
            continue
        if key in LEGACY_KEYS:
            legacy.append(raw)
            continue
        if key in seen:  # duplicate key surviving in the working file
            legacy.append(raw)
            continue
        seen.add(key)
        keep.append(raw)

    print(f"cited in text     : {len(cited & seen) + len(promoted)}")
    print(f"kept in bib       : {len(keep)}")
    print(f"moved to legacy   : {len(legacy)}")
    print(f"promoted+rewritten: {len(promoted)} -> krippendorff2018, shapley1952")
    print(f"left for review   : {len(REVIEW_KEYS & seen if isinstance(REVIEW_KEYS, set) else set(REVIEW_KEYS) & seen)}")

    if args.apply:
        BIB.write_text("\n\n".join(keep) + "\n", encoding="utf-8")
        header = (
            "% Legacy bibliography -- entries from earlier drafts, none cited by the thesis.\n"
            "% Moved out of references.bib by scripts/pubs/triage_bibliography.py (2026-08-29)\n"
            "% so the published bibliography matches the thesis's actual evidence base.\n"
            "% Not loaded by thesis/_quarto.yml. Retained for provenance.\n\n"
        )
        LEGACY.write_text(header + "\n\n".join(legacy) + "\n", encoding="utf-8")
        print(f"\nwrote {BIB.relative_to(ROOT)} and {LEGACY.relative_to(ROOT)}")
    else:
        print("\n(report only; pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
