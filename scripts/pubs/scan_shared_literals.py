#!/usr/bin/env python3
"""Find Paper B+C numbers that Paper A already prints, without the registry.

verify_claims.py enforces RCA-001's prior-publication invariant through the
registry: a claim registered for both a published manuscript and a submission
is a conflict. That only works if every site is registered. On 2026-09-28 the
SHAP and LIME mean costs were found printed in both papers while the registry
listed only the Paper B+C site, so the check could not see them (review F02).

This scan does not use the registry. It reads every decimal literal in the
Paper B+C main text, supplementary and abstract fragment, and reports each one
that equals a Paper A literal at the Paper B+C literal's printed precision
(Paper B+C "11,708.3" matches Paper A "11708.26"). Low-precision numbers match
by coincidence, so each match must be triaged. A match that is known not to be
a shared result is listed in KNOWN_COINCIDENCES with its reason; anything else
is reported as unexplained.

    python scripts/pubs/scan_shared_literals.py            # report, exit 0
    python scripts/pubs/scan_shared_literals.py --strict   # exit 1 on unexplained

The submission gate runs it with --strict; CI runs the report.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_claims import _scannable  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PAPER_A = ROOT / "docs" / "reports" / "paper_a" / "paper_a_prototype_jmlr.tex"
PAPER_BC = [
    ROOT / "pub" / "fragments" / "paper_bc_abstract_en.tex",
    ROOT / "pub" / "fragments" / "paper_bc_resumen_es.tex",
    ROOT / "docs" / "reports" / "paper_bc" / "paper_bc_iberamia.tex",
    ROOT / "docs" / "reports" / "paper_bc" / "paper_bc_iberamia_appendix.tex",
]

DECIMAL = re.compile(r"(?<![\w.])\d[\d,]*\.\d+")

# Paper B+C literal -> why its match in Paper A is not a shared result.
# Triaged 2026-09-28 against the contexts in both papers.
KNOWN_COINCIDENCES = {
    "00.3": "TikZ coordinate (0,0.3) in the continuum figure",
    "0.015": "seed SD of LIME stability, RF/N=100 (review F08); Paper A 0.0154 is a LIME stability mean in its primary-subset table",
    "0.9": "stratum-median CV of SHAP fidelity (%); Paper A's 0.90-0.95 values are unrelated",
    "1.4": "stratum-median CV of SHAP stability (%); Paper A 1.39 is unrelated",
    "2.3": "stratum-median CV of LIME fidelity (%); Paper A 2.29 is a p-value mantissa",
    "0.05": "significance level alpha",
    "0.01": "LIME stability range bound (tab:exp3_lime caption); Paper A 0.0144 is its block mean, not printed here",
    "0.02": "same caption range bound; Paper A 0.0154 is an unrelated cell",
    "0.014": "Table S5 reference-row stability; matches Paper A's block-level LIME stability only by rounding (see supp.s5 unbacked entries)",
    "0.1": "Gaussian perturbation scale sigma, a protocol setting",
    "0.15": "Table S3 display threshold",
    "0.23": "EXP3 German Credit RF SHAP-LIME gap; Paper A 0.2264 is SHAP sparsity",
    "0.236": "lower CI bound of the paired fidelity difference; Paper A 0.2361 is Anchors faithfulness gap",
    "0.24": "EXP3 German Credit XGB SHAP-LIME gap; Paper A 0.2361 is Anchors faithfulness gap",
    "0.278": "original-cohort Krippendorff alpha for clarity; Paper A 0.2778 is an EXP3 SHAP sparsity cell",
    "0.35": "prose bound over registered alpha values",
    "0.5": "generic constant",
    "0.601": "original-cohort ICC for semantic plausibility; Paper A 0.6014 is an EXP3 SHAP stability cell",
    "0.7": "reproducibility CV (0.7%), RF/N=100 stratum; Paper A 0.7137 is unrelated",
    "0.8": "reproducibility CV (0.8%), RF/N=100 stratum; Paper A 0.8081 is SHAP fidelity",
    "0.95": "Anchors precision threshold tau, a protocol setting",
    "0.98": "figure width (\\linewidth)",
    "1.0": "definitional association (V = 1.0)",
    "3.0": "LIME kernel width, a protocol setting",
    "3.8": "judge model version (Gemini 3.8 Flash)",
    "5.4": "judge model version (GPT-5.4 mini)",
    "100.0": "percentage (100.0% inclusion agreement)",
    "1702.08608": "arXiv identifier",
    "2505.22252": "arXiv identifier",
}


def _decimals(literal: str) -> int:
    return len(literal.split(".", 1)[1])


def _literals(path: Path) -> list[tuple[int, str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    text = text.split("\\begin{thebibliography}")[0]
    out = []
    for lineno, line in enumerate(_scannable(text).splitlines(), 1):
        out += [(lineno, m.group(0).replace(",", "")) for m in DECIMAL.finditer(line)]
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 if any match is not in KNOWN_COINCIDENCES")
    args = parser.parse_args(argv)

    a_values = sorted({lit for _, lit in _literals(PAPER_A)})
    unexplained, explained = [], 0
    for path in PAPER_BC:
        rel = path.relative_to(ROOT).as_posix()
        for lineno, lit in _literals(path):
            places = _decimals(lit)
            hits = [a for a in a_values
                    if _decimals(a) >= places and abs(round(float(a), places) - float(lit)) < 1e-9]
            if not hits or float(lit) == 0.0:
                continue
            if lit in KNOWN_COINCIDENCES:
                explained += 1
                continue
            unexplained.append(f"{rel}:{lineno} prints {lit!r}; Paper A prints {', '.join(hits)}")

    for line in unexplained:
        print("[shared-literal]", line)
    print(f"shared-literal scan: {len(unexplained)} unexplained match(es), "
          f"{explained} known coincidence(s)")
    return 1 if (args.strict and unexplained) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
