#!/usr/bin/env python3
"""Render and build Paper G for Informática y Sistemas.

1. Render: paper_g_draft.md (the manuscript source) -> paper_g.md. Every placeholder
   <<alias:key:column:format>> is replaced by a value read from a committed result file under
   outputs/analysis/paper_g/ (read only), and <<table:name>> by a table generated from the same
   files. Keys are the slug of the key columns' values (lower case; any run of characters other
   than letters and digits becomes "_"; several key columns joined by "__"). The aliases are
   listed in TABLES; `sum` holds the few values derived here (ranges, means, sums), each from
   the files named in its docstring.

   Formats: f1..f5 a decimal with that many places (a negative value printed with "−"); zf1..zf5 the same without the leading zero (APA p-values);
   pct0, pct1 a share printed as a percentage; d an integer; int an integer with thousands
   separator; p a p-value (f5 below 0.001, f3 otherwise).

   Labels (author rule: numbered by generated reference, in order of first appearance,
   citation or definition): a figure is defined by
   ![caption](figures/name.png){#fig:name}, a table caption by "Table: caption {#tbl:name}",
   an equation by "$$ ... $$ {#eq:name}". They are numbered in order of definition and cited
   as {{fig:name}} -> "Figure 1", {{tbl:name}} -> "Table 1", {{eq:name}} -> "Equation 1".
   Citations are pandoc's [@key], resolved from generated/references.json (APA 7).

2. Build (unless --render-only): submission/paper_g_blind.docx with pandoc, the journal's
   template as reference document (styles), APA 7 citations; submission/paper_g_blind.pdf with
   LibreOffice for the page count; submission/Figure_N.png and .svg, numbered as in the text.

    python docs/reports/paper_g/scripts/build_paper_g.py [--render-only] [--final]

With --final the build stops on any unresolved placeholder or label.
"""
from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
G = Path(__file__).resolve().parents[1]
RES = ROOT / "outputs" / "analysis" / "paper_g"
S1 = "supplementary/s1/analysis"
SOURCE = G / "paper_g_draft.md"
RENDERED = G / "paper_g.md"
SUB = G / "submission"
TEMPLATE = G / "venue" / "template" / "IyS_article_template.docx"
CSL = G / "venue" / "csl" / "apa.csl"
BIB = G / "generated" / "references.json"
MAX_PAGES, MIN_PAGES = 16, 8

M16 = ["m1_deletion", "m2_insertion", "m3_gap", "m4_corr", "m5_infidelity", "m6_sufficiency"]
NUMERIC = ["magic_telescope", "phoneme", "qsar_biodeg"]
MIXED = ["adult", "bank_marketing", "compas", "electricity", "german_credit"]
CONDITIONS = {"orig": "original", "s1b": "s1b", "s1m": "s1m"}

# alias: (file under outputs/analysis/paper_g, key columns; [] = one row, key "all")
TABLES: dict[str, tuple[str, list[str]]] = {
    "h1": ("analysis/confirmatory/h1_summary.csv", ["analysis"]),
    "perm": ("analysis/confirmatory/h1_permutation.csv", ["analysis"]),
    "mult": ("analysis/confirmatory/multiplicity_h1_h2.csv", ["hypothesis"]),
    "h2": ("analysis/confirmatory/h2_omnibus.csv", ["analysis"]),
    "h2p": ("analysis/confirmatory/h2_pairs.csv", ["pair"]),
    "stab": ("analysis/confirmatory/stability_summary.csv", ["analysis"]),
    "stabd": ("analysis/confirmatory/stability_datasets.csv", ["dataset"]),
    "h1d": ("analysis/confirmatory/h1_datasets_spearman.csv", ["dataset"]),
    "sens": ("analysis/sensitivity/h1_sensitivity.csv", ["analysis"]),
    "h2s": ("analysis/sensitivity/h2_sensitivity.csv", ["analysis"]),
    "pm": ("analysis/sensitivity/per_model.csv", ["model"]),
    "wf": ("analysis/sensitivity/winner_flips.csv", ["pair_key"]),
    "slr": ("analysis/sensitivity/shap_lime_reversals.csv", ["pair_key"]),
    "slany": ("analysis/sensitivity/shap_lime_any_reversal.csv", []),
    "m4x": ("analysis/exploratory/h1_m4_excluded.csv", ["analysis"]),
    "syn": ("analysis/synthetic/four_by_metric.csv", ["metric"]),
    "syn3": ("analysis/synthetic/three_sensitivity_by_metric.csv", ["metric"]),
    "s3": ("supplementary/s3/s3_condition.csv", ["condition", "representation"]),
    "r3": ("exploratory_post/r3_summary.csv", ["quantity"]),
    "r6": ("exploratory_post/r6_summary.csv", ["pair"]),
    "r7g": ("exploratory_post/r7_groups.csv", ["dataset"]),
    "r7t": ("exploratory_post/r7_ties_by_model.csv", ["model"]),
    "r7d": ("exploratory_post/r7_ties_by_dataset.csv", ["dataset"]),
    "r11": ("exploratory_post/r11_summary.csv", []),
    "cmp": (f"{S1}/comparison_summary.csv", ["quantity", "condition"]),
    "cds": (f"{S1}/comparison_by_dataset.csv", ["dataset"]),
    "gate": ("diagnostics/dataset_gate.csv", ["dataset"]),
}
for _a, _d in CONDITIONS.items():
    TABLES.update({
        f"pos_{_a}": (f"{S1}/{_d}/positions_summary.csv", ["quantity"]),
        f"posm_{_a}": (f"{S1}/{_d}/positions_by_metric.csv", ["metric", "explainer"]),
        f"rl_{_a}": (f"{S1}/{_d}/random_last.csv", []),
        f"any_{_a}": (f"{S1}/{_d}/shap_lime_any.csv", []),
        f"stm_{_a}": (f"{S1}/{_d}/stability_by_metric.csv", ["metric"]),
        f"h2a_{_a}": (f"{S1}/{_d}/h2_adjusted.csv", ["pair"]),
    })

# Printed width of a figure as a share of the text width (default 100%); square or tall figures
# are narrower so the article stays within the journal's 16 pages. The submitted figure files
# (submission/Figure_n) are unaffected.
FIG_WIDTH = {"h2_matrix": "65%", "positions": "80%", "s3": "85%", "sensitivity": "90%"}

_TABLES: dict | None = None


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def rows(rel: str) -> list[dict]:
    with open(RES / rel, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _num(v: str):
    try:
        return float(v)
    except (TypeError, ValueError):
        return v


def _derived(t: dict) -> dict:
    """Values derived here from the loaded tables (no other input).

    flips/revs   ranges (min, max) of winner flips and strict SHAP-LIME reversals over the
                 15 pairs of M1-M6 (`m16`) and the 6 pairs with M7 (`m7`); original from
                 sensitivity/, S1 from supplementary/s1/analysis/<condition>/
    type         mean H1-form agreement over the numeric and the mixed datasets
                 (comparison_by_dataset.csv)
    s1diff       largest |S1-B - S1-M| over the summary quantities (comparison_summary.csv)
    m4deg        undefined faithfulness-correlation scores, summed over models
    gate         lowest and highest cross-validated AUC over datasets and models
    lastm16      blocks (of 160) with LIME ranked last under each of M1-M4 and M6
    undef        undefined metric-pair correlations in the original H1 blocks and the blocks
                 with any (analysis/confirmatory/h1_blocks.csv)
    synref       synthetic reference orders (condition x seed) with LIME third or fourth of
                 four (analysis/synthetic/four_reference.csv)
    """
    out: dict[str, dict] = {}
    for a, d in CONDITIONS.items():
        for kind, fname, col in (("flips", "winner_flips.csv", "flip_share"),
                                 ("revs", "shap_lime_reversals.csv", "reversal_share")):
            if a == "orig":
                rel = "analysis/sensitivity/" + ("winner_flips.csv" if kind == "flips"
                                                 else "shap_lime_reversals.csv")
            else:
                rel = f"{S1}/{d}/{fname}"
            vals = {r["pair_key"]: float(r[col]) for r in rows(rel)}
            m16 = [v for k, v in vals.items() if "m7" not in k]
            m7 = [v for k, v in vals.items() if "m7" in k]
            out[f"{kind}_{a}_m16"] = {"min": min(m16), "max": max(m16)}
            out[f"{kind}_{a}_m7"] = {"min": min(m7), "max": max(m7)}
    cds = {r["dataset"]: r for r in rows(f"{S1}/comparison_by_dataset.csv")}
    for name, group in (("numeric", NUMERIC), ("mixed", MIXED)):
        out[f"type_{name}"] = {c: sum(float(cds[d][c]) for d in group) / len(group)
                               for c in ("original", "S1-B", "S1-M")}
    summ = rows(f"{S1}/comparison_summary.csv")
    by = {}
    for r in summ:
        by.setdefault(r["quantity"], {})[r["condition"]] = float(r["mean"])
    out["s1diff"] = {"max": max(abs(v["S1-B"] - v["S1-M"]) for v in by.values())}
    deg = rows("analysis/exploratory/m4_degenerate_by_model.csv")
    out["m4deg"] = {"degenerate": sum(int(r["degenerate"]) for r in deg),
                    "rows": sum(int(r["rows"]) for r in deg)}
    aucs = [float(r[f"cv_auc_{m}"]) for r in rows("diagnostics/dataset_gate.csv")
            for m in ("logreg", "rf", "xgb", "mlp")]
    out["gate"] = {"min": min(aucs), "max": max(aucs)}
    pos = {(r["metric"], r["explainer"]): r for r in rows(
        "exploratory_post/r3_positions_by_metric.csv")}
    out["lastm16"] = {m: float(pos[(m, "lime")]["r3"]) for m in M16}
    hb = rows("analysis/confirmatory/h1_blocks.csv")
    out["undef"] = {"pairs": sum(int(r["pairs_undefined"]) for r in hb),
                    "blocks": sum(int(r["pairs_undefined"]) > 0 for r in hb)}
    ref = rows("analysis/synthetic/four_reference.csv")
    out["synref"] = {"lime_low": sum(float(r["rank_lime"]) >= 3 for r in ref), "n": len(ref)}
    return {"sum": {k: v for k, v in out.items()}}


def tables() -> dict:
    """{alias: {key: {column: value}}} for every placeholder of the manuscript."""
    global _TABLES
    if _TABLES is None:
        t: dict[str, dict] = {}
        for alias, (rel, keys) in TABLES.items():
            t[alias] = {}
            for r in rows(rel):
                key = "__".join(slug(r[k]) for k in keys) if keys else "all"
                t[alias][key] = {c: _num(v) for c, v in r.items()}
        t.update(_derived(t))
        _TABLES = t
    return _TABLES


def _half_up(v: float, places: int) -> str:
    """Rounded half up from the value's shortest decimal form: 102/160 = 63.75 prints 63.8,
    which binary rounding of 0.6375 * 100 would print as 63.7."""
    d = Decimal(repr(round(v, 12))).quantize(Decimal(1).scaleb(-places), ROUND_HALF_UP)
    return f"{d:.{places}f}"


def fmt(v, f: str) -> str:
    if f == "d":
        return f"{int(round(v))}"
    if f == "int":
        return f"{int(round(v)):,}"
    if f in ("pct0", "pct1"):
        return _half_up(100 * v, int(f[3]))
    if f == "p":
        f = "f5" if v < 0.001 else "f3"
    if re.fullmatch(r"zf[1-5]", f):                    # APA 7 p-value: no leading zero
        return fmt(v, f[1:]).replace("0.", ".", 1)
    if re.fullmatch(r"f[0-5]", f):
        s = _half_up(v, int(f[1]))
        return s.replace("-", "−") if s.strip("-0.") else s.lstrip("-")
    raise KeyError(f"unknown format {f}")


# The template's source line under every figure and table ("Source: Authors, or the reference").
SOURCE_LINE = '::: {custom-style="Source"}\nSource: Authors.\n:::'

PLACEHOLDER = re.compile(r"<<([a-z0-9_]+):([^:<>]+):([^:<>]+):([a-z0-9]+)>>")


def value(alias: str, key: str, column: str) -> float:
    return float(tables()[alias][key][column])


def gen_tables() -> dict[str, str]:
    """Markdown tables generated from the result files, written with placeholders so that
    each printed value has a source (rendered and registered like the text's)."""
    t = tables()
    ds = ["phoneme", "qsar_biodeg", "magic_telescope", "electricity", "german_credit", "adult",
          "bank_marketing", "compas"]
    cfg = (ROOT / "experiments" / "exp_g" / "config.toml").read_text(encoding="utf-8")
    ids = dict(re.findall(r'key = "([a-z_]+)"\nid = (\d+)', cfg))
    strata = dict(re.findall(r'key = "([a-z_]+)"\nid = \d+\nstratum = "([a-z-]+)"', cfg))
    lines = ["| Dataset | OpenML ID | Stratum | Features | LR | RF | XGB | MLP |",
             "|------------------|------:|------------------|----:|------:|------:|------:|------:|"]
    for d in ds:
        lines.append(f"| {d.replace('_', ' ')} | {ids[d]} | {strata[d]} | <<r7g:{d}:G:d>> | "
                     + " | ".join(f"<<gate:{d}:cv_auc_{m}:f3>>"
                                  for m in ("logreg", "rf", "xgb", "mlp")) + " |")
    datasets = "\n".join(lines)

    def ci(q: str, c: str) -> str:
        k = f"{slug(q)}__{slug(c)}"
        if k not in t["cmp"]:
            raise KeyError(f"cmp {k}")
        return f"<<cmp:{k}:mean:f3>> [<<cmp:{k}:lo:f3>>, <<cmp:{k}:hi:f3>>]"
    quantities = [
        ("H1-form agreement, mean pairwise Spearman^O^",
         "H1 mean pairwise Spearman (3 explainers, 7 metrics)"),
        ("Kendall's *W*^O^", "H1 Kendall W"),
        ("Second masking baseline^S^", "H1 second baseline (Spearman)"),
        ("Six metrics (M4 removed)^S^", "H1 six metrics, no M4 (Spearman)"),
        ("With the random control (four explainers)^S^", "H1 four explainers (Spearman)"),
        ("Within-metric stability benchmark^O^", "within-metric stability benchmark"),
        ("H2-form instance-level agreement^O^", "H2 omnibus (4 explainers)"),
        ("H2-form, adjusted for *f(x)*^C^", "H2 omnibus adjusted for f_x (exploratory)"),
    ]
    lines = ["| Quantity | Original (LIME slopes) | S1-B | S1-M |",
             "|--------------------------------|------------------|------------------|------------------|"]
    for label, q in quantities:
        lines.append(f"| {label} | " + " | ".join(ci(q, c) for c in ("original", "S1-B", "S1-M"))
                     + " |")
    q1 = slug("blocks with one explainer at the same untied extreme rank under all 7 metrics")
    q2 = slug("... of which lime last")
    rows_ = [
        ("Blocks with one explainer at the same extreme rank under all seven metrics^C^",
         lambda a: f"<<pos_{a}:{q1}:value:d>>"),
        ("... LIME untied last under all seven metrics^C^", lambda a: f"<<pos_{a}:{q2}:value:d>>"),
        ("Random control untied last under all seven metrics^C^",
         lambda a: f"<<rl_{a}:all:untied_last_all7:d>>"),
        ("Blocks with any strict SHAP–LIME reversal^S^", lambda a: f"<<any_{a}:all:"
                                                             "blocks_with_any_strict_reversal:d>>"),
        ("Winner flips, pairs of M1–M6 (%)^S^",
         lambda a: f"<<sum:flips_{a}_m16:min:pct1>>–<<sum:flips_{a}_m16:max:pct1>>"),
        ("Winner flips, pairs with M7 (%)^S^",
         lambda a: f"<<sum:flips_{a}_m7:min:pct1>>–<<sum:flips_{a}_m7:max:pct1>>"),
    ]
    for label, cell in rows_:
        lines.append(f"| {label} | " + " | ".join(cell(a) for a in CONDITIONS) + " |")
    evidence = "\n".join(lines)

    decision = "\n".join([
        "| Outcome of the permutation test and the 95% interval | Wording |",
        "|------------------------------------|------------------------------------|",
        "| *p* ≥ .05 | no evidence that the metrics share an order |",
        "| *p* < .05, interval above 0.5 | the metrics broadly agree |",
        "| *p* < .05, interval below 0.5 | the metrics agree only weakly |",
        "| *p* < .05, interval contains 0.5 | agreement present, strength not determined |"])
    return {"datasets": datasets, "evidence": evidence, "decision": decision}


def expanded_source() -> str:
    """The manuscript source with the generated tables inserted, placeholders unresolved."""
    text = strip_front(SOURCE.read_text(encoding="utf-8"))
    gen = gen_tables()
    return re.sub(r"<<table:([a-z]+)>>", lambda m: gen[m.group(1)], text)


def placeholders() -> list[tuple[str, str, str, str]]:
    """Every (alias, key, column, format) printed in the manuscript, tables included."""
    return PLACEHOLDER.findall(expanded_source())


def render(text: str, final: bool = False) -> tuple[str, list[str]]:
    problems: list[str] = []
    t = tables()

    def sub(m: re.Match) -> str:
        alias, key, column, f = m.groups()
        try:
            return fmt(float(t[alias][key][column]), f)
        except (KeyError, ValueError, TypeError) as exc:
            problems.append(f"placeholder {m.group(0)}: {exc!r}")
            return f"[UNRESOLVED {m.group(0)[2:-2]}]"
    gen = gen_tables()
    text = re.sub(r"<<table:([a-z]+)>>", lambda m: gen[m.group(1)], text)
    text = PLACEHOLDER.sub(sub, text)

    numbers: dict[str, dict[str, int]] = {"fig": {}, "tbl": {}, "eq": {}}
    defined = set(re.findall(r"\{#((?:fig|tbl|eq):[a-z0-9_]+)\}", text))
    # Numbered in order of first appearance, citation or definition (journal rule).
    for kind, name in re.findall(r"\{\{?#?(fig|tbl|eq):([a-z0-9_]+)\}\}?", text):
        if f"{kind}:{name}" in defined:
            numbers[kind].setdefault(name, len(numbers[kind]) + 1)

    def fig(m: re.Match) -> str:
        n = numbers["fig"][m.group(3)]
        return (f"![**Figure {n}.** {m.group(1)}]({m.group(2)})"
                f"{{width={FIG_WIDTH.get(m.group(3), '100%')}}}\n\n" + SOURCE_LINE)
    text = re.sub(r"!\[(.*?)\]\((.*?)\)\{#fig:([a-z0-9_]+)\}", fig, text, flags=re.S)
    text = re.sub(r"^Table: (.*?) \{#tbl:([a-z0-9_]+)\}$",
                  lambda m: f"Table: **Table {numbers['tbl'][m.group(2)]}.** {m.group(1)}",
                  text, flags=re.M)
    text = re.sub(r"\$\$(.*?)\$\$ \{#eq:([a-z0-9_]+)\}",
                  lambda m: f"$${m.group(1).strip()} \\qquad ({numbers['eq'][m.group(2)]})$$",
                  text, flags=re.S)
    word = {"fig": "Figure", "tbl": "Table", "eq": "Equation"}
    form = {"fig": "{w} {n}", "tbl": "{w} {n}", "eq": "{w} ({n})"}  # template: "Equation (1)"

    def ref(m: re.Match) -> str:
        kind, name = m.groups()
        if name not in numbers[kind]:
            problems.append(f"undefined label {kind}:{name}")
            return f"[UNDEFINED {kind}:{name}]"
        return form[kind].format(w=word[kind], n=numbers[kind][name])
    text = re.sub(r"\{\{(fig|tbl|eq):([a-z0-9_]+)\}\}", ref, text)
    if final and problems:
        raise SystemExit("\n".join(problems))
    return text, problems


def figures_in_order(text: str) -> list[str]:
    return re.findall(r"!\[\*\*Figure \d+\.\*\* .*?\]\((figures/[a-z0-9_]+)\.png\)", text, re.S)


# Evidence class of each section of the manuscript (analysis plan sections 4, 11 and 12).
SECTION_CLASS = {
    "Abstract": "original analysis, supplementary (summary)", "1": "context", "2": "methods",
    "3.1": "A original analysis (H1 decision pre-specified; H2 inference fixed before unblinding)",
    "3.2": "A sensitivity (pre-specified; six-metric fixed before unblinding)", "3.3": "B supplementary (S3)",
    "3.4": "B supplementary (S1-B primary, S1-M sensitivity)", "3.5": "C exploratory (R3)",
    "3.6": "C exploratory (R6)", "3.7": "C exploratory (R7, R11)",
    "3.8": "interpretation of A to C", "4": "conclusion"}


def evidence_map() -> str:
    """EVIDENCE_MAP.md: for each section, its evidence class and the files its values come from."""
    sections: dict[str, dict] = {}
    current = "Abstract"
    for line in expanded_source().splitlines():
        m = re.match(r"^#{1,2} (\d+(?:\.\d+)?)\.? (.*)", line)
        if m:
            current = m.group(1)
            sections.setdefault(current, {"title": m.group(2), "values": 0, "files": set()})
            continue
        sections.setdefault(current, {"title": "Abstract", "values": 0, "files": set()})
        for alias, *_ in PLACEHOLDER.findall(line):
            sections[current]["values"] += 1
            if alias == "sum":
                sections[current]["files"].add("(derived in build_paper_g.py: see _derived)")
            else:
                sections[current]["files"].add(TABLES[alias][0])
    out = ["# Paper G — evidence map", "",
           "Generated by `scripts/build_paper_g.py --evidence-map`; do not edit. For each section",
           "of the manuscript: its evidence class (A original analysis, as specified before the run",
           "or fixed after it before unblinding; B supplementary experiments specified after the",
           "review of the results; C exploratory diagnostics), the number of values it prints, and the result files under",
           "`outputs/analysis/paper_g/` they are read from. Every value is registered in",
           "`pub/claim_registry.toml` (block `paper_g`) and re-derived by",
           "`scripts/pubs/verify_claims.py`; bare integers are covered by",
           "`scripts/pubs/register_paper_g.py --check`, which requires `paper_g.md` to equal the",
           "rendering of the source from the result files.", "",
           "| Section | Title | Class | Values | Source files |", "|---|---|---|---|---|"]
    for sec, d in sections.items():
        cls = SECTION_CLASS.get(sec, SECTION_CLASS.get(sec.split(".")[0], ""))
        files = "<br>".join(f"`{f}`" for f in sorted(d["files"])) or "—"
        out.append(f"| {sec} | {d['title']} | {cls} | {d['values']} | {files} |")
    return "\n".join(out) + "\n"


def build(text: str) -> None:
    SUB.mkdir(exist_ok=True)
    body = G / "generated" / "paper_g_for_docx.md"
    # The manuscript's front matter (status note) is not part of the submitted file.
    body.write_text(equations_for_word(text), encoding="utf-8", newline="\n")
    docx = SUB / "paper_g_blind.docx"
    cmd = ["pandoc", str(body), "-o", str(docx), "--citeproc", "--csl", str(CSL),
           "--bibliography", str(BIB), "--resource-path", str(G), "-M",
           "reference-section-title=Bibliographic references", "-M", "link-citations=false",
           "--columns=40"]  # every pipe table wider than 40: relative column widths
    if TEMPLATE.exists():
        cmd += ["--reference-doc", str(TEMPLATE)]
    subprocess.run(cmd, check=True, cwd=G)
    if TEMPLATE.exists():
        fix_docx(docx)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(SUB),
                    str(docx)], check=True, capture_output=True)
    pdf = SUB / "paper_g_blind.pdf"
    pages = len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))
    for n, stem in enumerate(figures_in_order(text), 1):
        for ext in ("png", "svg"):
            shutil.copyfile(G / f"{stem}.{ext}", SUB / f"Figure_{n}.{ext}")
    print(f"built {docx.relative_to(ROOT)} and {pdf.name}: {pages} pages "
          f"(journal: {MIN_PAGES} to {MAX_PAGES})")


# Styles pandoc uses that the journal template does not define, defined on the template's own
# styles; pandoc's "Table" is replaced by the template's "Journal Table" (horizontal rules only,
# as the journal asks).
EXTRA_STYLES = (
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Compact"><w:name w:val="Compact"/>'
    '<w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="20" w:after="20"/>'
    '</w:pPr><w:rPr><w:sz w:val="16"/><w:szCs w:val="16"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="FirstParagraph">'
    '<w:name w:val="First Paragraph"/><w:basedOn w:val="Textoindependiente"/><w:next '
    'w:val="Textoindependiente"/><w:qFormat/></w:style>'
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="CaptionedFigure">'
    '<w:name w:val="Captioned Figure"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/>'
    '<w:spacing w:before="120" w:after="0" w:line="240" w:lineRule="auto"/>'
    '<w:jc w:val="center"/></w:pPr></w:style>'
    # Text width 17.59 cm = 9972 twips: centre tab at the middle, right tab at the margin.
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Equation">'
    '<w:name w:val="Equation"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr>'
    '<w:keepLines/><w:tabs><w:tab w:val="center" w:pos="4986"/><w:tab w:val="right" '
    'w:pos="9972"/></w:tabs><w:spacing w:before="120" w:after="120"/><w:ind w:left="0" '
    'w:firstLine="0"/><w:jc w:val="left"/></w:pPr></w:style>')


TAB = "`<w:r><w:tab/></w:r>`{=openxml}"


def equations_for_word(text: str) -> str:
    """Template: an equation is centred, its number in parentheses at the right margin, and it is
    separated from the text by a blank line. Each numbered display equation becomes an
    "Equation" paragraph (centre and right tab stops, see EXTRA_STYLES): tab, formula, tab, (n)."""
    return re.sub(r"\$\$(.+?) \\qquad \((\d+)\)\$\$",
                  lambda m: (f'::: {{custom-style="Equation"}}\n{TAB}$\\displaystyle '
                             f'{m.group(1).strip()}${TAB}({m.group(2)})\n:::'),
                  text, flags=re.S)


def fix_docx(path: Path) -> None:
    """Make pandoc's output use the journal template's styles (see EXTRA_STYLES)."""
    import zipfile
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        files = {i.filename: z.read(i.filename) for i in infos}
    styles = files["word/styles.xml"].decode("utf-8")
    if 'w:styleId="Compact"' not in styles:
        styles = styles.replace("</w:styles>", EXTRA_STYLES + "</w:styles>")
    files["word/styles.xml"] = styles.encode("utf-8")
    files["word/document.xml"] = files["word/document.xml"].replace(
        b'<w:tblStyle w:val="Table" />', b'<w:tblStyle w:val="JournalTable" />')
    tmp = path.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for i in infos:
            z.writestr(i, files[i.filename])
    tmp.replace(path)


def strip_front(text: str) -> str:
    """Drop the source's status block (everything before the title block)."""
    i = text.find("\n::: {custom-style=\"Title\"}")
    return text[i + 1:] if i >= 0 else text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--render-only", action="store_true")
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--evidence-map", action="store_true", help="also write EVIDENCE_MAP.md")
    args = ap.parse_args()
    if args.evidence_map:
        (G / "EVIDENCE_MAP.md").write_text(evidence_map(), encoding="utf-8", newline="\n")
    text, problems = render(strip_front(SOURCE.read_text(encoding="utf-8")), args.final)
    RENDERED.write_text(text, encoding="utf-8", newline="\n")
    print(f"rendered {RENDERED.relative_to(ROOT)}; {len(problems)} problem(s)")
    for p in problems:
        print("  " + p)
    if not args.render_only:
        build(text)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
