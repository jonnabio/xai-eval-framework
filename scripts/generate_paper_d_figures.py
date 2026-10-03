#!/usr/bin/env python3
"""Generate the figures of Paper D (claim-registry case study).

Each figure is written three ways, because the journal wants images both
inside the Word document and as separate files in an allowed format:
    figures/<name>.pdf    vector, used by the LaTeX build
    figures/<name>.png    300 ppi, embedded in the .docx
    figures/<name>.tiff   300 ppi, the separate upload (.tiff is an allowed format)

Inputs are the committed snapshots in outputs/analysis/paper_d/, written by
scripts/pubs/paper_d_metrics.py, so the figures re-derive like the text.

    python scripts/generate_paper_d_figures.py
"""
from __future__ import annotations

import csv
import subprocess
import sys
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "outputs" / "analysis" / "paper_d"
FIG = ROOT / "docs" / "reports" / "paper_d" / "figures"
TECTONIC = ROOT / "tools" / "tectonic-portable" / ("tectonic.exe" if sys.platform == "win32" else "tectonic")
DPI = 300


def _style() -> None:
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "savefig.dpi": DPI,
    })


def _raster(pdf: Path) -> None:
    """PDF -> PNG and TIFF at 300 ppi with poppler's pdftoppm."""
    stem = pdf.with_suffix("")
    for fmt in ("png", "tiff"):
        extra = ["-tiffcompression", "lzw"] if fmt == "tiff" else []
        subprocess.run(["pdftoppm", f"-{fmt}", *extra, "-r", str(DPI), "-singlefile", str(pdf),
                        str(stem)], check=True)
        if fmt == "tiff":
            tif = stem.with_suffix(".tif")
            if tif.exists():
                tif.replace(stem.with_suffix(".tiff"))


def fig1_architecture() -> None:
    src = FIG / "fig1_architecture.tex"
    subprocess.run([str(TECTONIC), "-X", "compile", src.name], cwd=FIG, check=True,
                   capture_output=True)
    _raster(FIG / "fig1_architecture.pdf")


def fig2_registry_growth() -> None:
    rows = list(csv.DictReader((DATA / "registry_growth.csv").open(encoding="utf-8")))
    # Several commits can land on one day; plot the last state of each day.
    by_day: dict[str, dict] = {}
    for r in rows:
        by_day[r["date"]] = r
    days = [date.fromisoformat(d) for d in by_day]
    claims = [int(r["claims"]) for r in by_day.values()]
    sites = [int(r["sites"]) for r in by_day.values()]

    fig, ax = plt.subplots(figsize=(6.3, 2.9))
    ax.step(days, sites, where="post", color="#4d4d4d", lw=1.6, label="Manuscript sites checked")
    ax.step(days, claims, where="post", color="#1f77b4", lw=1.6, label="Registered claims")
    ax.set_ylabel("Count")
    ax.set_xlabel("Date (2026)")
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.set_ylim(0, None)
    ax.grid(axis="y", alpha=0.3)
    ax.legend(frameon=False, loc="upper left")
    fig.autofmt_xdate(rotation=0, ha="center")
    fig.tight_layout()
    out = FIG / "fig2_registry_growth.pdf"
    fig.savefig(out)
    plt.close(fig)
    _raster(out)


CLASS_LABELS = {
    "value_artifact_mismatch": "Value differs from artifact",
    "cross_document_inconsistency": "Cross-document inconsistency",
    "label_or_aggregation": "Wrong label or aggregation",
    "unbacked_value": "Value without an artifact",
    "provenance": "Artifact provenance",
    "prior_publication_overlap": "Prior-publication overlap",
    "render_defect": "Rendering defect",
    "claim_scope": "Claim scope",
    "coherence": "Internal coherence",
    "methodology": "Methodology",
    "reporting": "Reporting",
}


def fig3_incident_classes() -> None:
    rows = [r for r in csv.DictReader((DATA / "incident_catalogue.csv").open(encoding="utf-8"))
            if not r["dup_of"] and r["defect_class"] not in ("not_a_defect", "process_gap")]
    order = list(CLASS_LABELS)
    counts = {c: {"yes": 0, "partial": 0, "no": 0} for c in order}
    for r in rows:
        counts[r["defect_class"]][r["caught_now"]] += 1
    order = sorted(order, key=lambda c: (-counts[c]["yes"] - counts[c]["partial"],
                                         -sum(counts[c].values())))
    y = list(range(len(order)))[::-1]
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    left = [0] * len(order)
    for key, colour, label in (("yes", "#1f77b4", "Caught by the checks"),
                               ("partial", "#9ecae1", "Partly caught"),
                               ("no", "#d9d9d9", "Not caught")):
        vals = [counts[c][key] for c in order]
        ax.barh(y, vals, left=left, color=colour, edgecolor="white", label=label)
        left = [a + b for a, b in zip(left, vals)]
    ax.set_yticks(y)
    ax.set_yticklabels([CLASS_LABELS[c] for c in order])
    ax.set_xlabel("Defects found by audits and reviews")
    ax.xaxis.get_major_locator().set_params(integer=True)
    ax.legend(frameon=False, loc="lower right")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    out = FIG / "fig3_incident_classes.pdf"
    fig.savefig(out)
    plt.close(fig)
    _raster(out)


def main() -> int:
    FIG.mkdir(parents=True, exist_ok=True)
    _style()
    fig1_architecture()
    fig2_registry_growth()
    fig3_incident_classes()
    for p in sorted(FIG.glob("fig*.*")):
        if p.suffix in (".pdf", ".png", ".tiff"):
            print(f"  {p.relative_to(ROOT)}  {p.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
