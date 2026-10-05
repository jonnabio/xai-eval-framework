#!/usr/bin/env python3
"""Draw the human-rated subset of EXP4 and build one rating sheet per rater.

Plan: docs/reports/paper_c/PLAN.md, section 6. Seven cases from each of the eight
dataset-by-explainer cells of the 192-case inventory, without replacement, fixed seed.
Each rater gets a self-contained HTML sheet with the cases in an order of their own.

The case record shown to a rater is read from the rendered prompt of the clean condition
(docs/reports/paper_c/clean_condition/prompts), so it is what the judges received there:
the explanation without technical metrics, outcome of the prediction or true label.

Standard library only. Reads experiments/exp4_cohort2/cases and the clean prompts, and
writes only under docs/reports/paper_c/human_subset/.

    python docs/reports/paper_c/scripts/draw_human_sample.py
"""
from __future__ import annotations

import csv
import json
import random
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CASES = ROOT / "experiments" / "exp4_cohort2" / "cases" / "exp4_cases.jsonl"
OUT = Path(__file__).resolve().parents[1] / "human_subset"
# The record of the clean condition (PLAN.md 15.3): no technical metrics, no outcome of
# the prediction and no true label. Until 2026-10-04 the sheets showed the record of the
# primary condition; no sheet had been sent when this was changed.
PROMPTS = OUT.parent / "clean_condition" / "prompts"

SAMPLE_SEED = 20261004
PER_CELL = 7
RATERS = {"A": 101, "B": 202}  # rater id -> seed of the presentation order

# Dimensions, definitions and anchors exactly as in the judge prompt
# (src/prompts/templates/exp4_semantic_eval_v1.j2), in the same order.
RUBRIC = [
    ("clarity", "Understandable organisation and wording for a non-expert reader.",
     "1 = incomprehensible; 3 = requires domain knowledge; 5 = clear to any reader."),
    ("concision", "Compact relative to useful information content; avoids unnecessary redundancy.",
     "1 = verbose or padded; 3 = adequate; 5 = maximally informative per word."),
    ("actionability", "Supports recourse, decision review, or explicit next steps for a user.",
     "1 = no actionable content; 3 = vague suggestions; 5 = specific, feasible actions."),
    ("audit_usefulness", "Supports inspection of model behaviour by an auditor or data scientist.",
     "1 = no audit value; 3 = partially informative about model logic; "
     "5 = fully supports bias/error investigation."),
    ("completeness",
     "Provides sufficient local decision information to understand the specific prediction.",
     "1 = missing key drivers; 3 = covers main drivers; 5 = full local decision context."),
    ("semantic_plausibility",
     "Coherent with the instance context and general domain knowledge.",
     "1 = implausible or contradictory; 3 = plausible; "
     "5 = highly consistent with domain expectations."),
    ("overall_quality", "Holistic semantic quality integrating all dimensions above.",
     "1 = very poor; 3 = acceptable; 5 = excellent."),
]

# Fields of the case record that carry no information for a reader (identifiers and
# file locations). They were in the judge prompt; they are left out of the sheet.
OMITTED = ("case_id", "instance_id", "source_artifact_path", "source_experiment",
           "random_seed", "sample_size", "explanation_length_tokens")


def prompt_record(case_id: str) -> dict:
    """The JSON case record inside the rendered clean-condition prompt of a case."""
    (path,) = sorted(PROMPTS.glob(f"{case_id}_*.txt"))
    text = path.read_text(encoding="utf-8")
    block = re.search(r"## Case record\s+```json\s+(\{.*?\})\s+```", text, re.S)
    return json.loads(block.group(1))


def draw() -> list[dict]:
    cells: dict[tuple[str, str], list[dict]] = defaultdict(list)
    with CASES.open(encoding="utf-8") as fh:
        for line in fh:
            case = json.loads(line)
            cells[(case["dataset"], case["explainer"])].append(case)
    rng = random.Random(SAMPLE_SEED)
    chosen = []
    for key in sorted(cells):
        pool = sorted(cells[key], key=lambda c: c["case_id"])
        chosen += rng.sample(pool, PER_CELL)
    return chosen


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Explanation rating sheet - rater __RATER__</title>
<style>
body{font-family:Arial,Helvetica,sans-serif;max-width:860px;margin:0 auto;padding:16px;
line-height:1.45;color:#1a1a1a;background:#fff}
h1{font-size:1.3rem} h2{font-size:1.05rem;margin:0 0 8px}
.bar{position:sticky;top:0;background:#fff;border-bottom:1px solid #999;padding:8px 0;
display:flex;gap:12px;align-items:center;flex-wrap:wrap}
button{font-size:1rem;padding:6px 14px;cursor:pointer}
.case{border:1px solid #999;border-radius:6px;padding:14px;margin:18px 0}
.case.done{border-color:#2a7a2a}
table{border-collapse:collapse;margin:6px 0} td,th{border:1px solid #bbb;padding:3px 8px;
text-align:left;font-size:.92rem}
.expl{background:#f2f2f2;padding:8px;border-radius:4px;font-family:Consolas,monospace;
font-size:.9rem;overflow-wrap:anywhere}
.dim{margin:10px 0;padding-top:8px;border-top:1px dashed #bbb}
.dim b{display:block} .anch{font-size:.85rem;color:#444}
label.s{margin-right:14px;white-space:nowrap}
textarea{width:100%;box-sizing:border-box}
details{margin:8px 0}
</style></head><body>
<h1>Explanation rating sheet &mdash; rater __RATER__</h1>
<details open><summary><b>Instructions</b></summary>
<p>You will rate __N__ explanations. Each one was produced by an explanation method for one
prediction of a binary classifier on tabular data. Rate the <b>explanation</b>, not the
model's prediction.</p>
<p>For each case give an integer from 1 (very poor) to 5 (excellent) on each of the seven
dimensions. Use the definition and the anchors shown under each dimension. Work alone and do
not discuss the cases with the other rater. A comment is optional.</p>
<p>Your answers are saved in this browser as you go. When all cases are complete, press
<b>Export ratings</b> and send the downloaded file to the author.</p>
</details>
<div class="bar"><span id="progress"></span>
<button id="export">Export ratings</button><span id="msg"></span></div>
<div id="cases"></div>
<script>
const RATER = "__RATER__";
const RUBRIC = __RUBRIC__;
const CASES = __CASES__;
const KEY = "paper_c_ratings_" + RATER;
let state = {};
try { state = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { state = {}; }
function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }
function esc(s) { return String(s).replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c])); }
function complete(id) { const r = state[id] || {}; return RUBRIC.every(d => r[d[0]]); }
function progress() {
  const done = CASES.filter(c => complete(c.case_id)).length;
  document.getElementById("progress").textContent = done + " of " + CASES.length + " cases complete";
  CASES.forEach((c, i) => document.getElementById("case" + i).classList.toggle("done", complete(c.case_id)));
}
const root = document.getElementById("cases");
CASES.forEach((c, i) => {
  const rec = c.record, div = document.createElement("div");
  div.className = "case"; div.id = "case" + i;
  let h = "<h2>Case " + (i + 1) + " of " + CASES.length + "</h2><table>";
  for (const k of Object.keys(rec)) {
    if (k === "normalized_explanation" || k === "technical_metrics") continue;
    h += "<tr><th>" + esc(k) + "</th><td>" + esc(rec[k] === null ? "not given" : rec[k]) + "</td></tr>";
  }
  h += "</table><p><b>Explanation</b></p><div class='expl'>" + esc(rec.normalized_explanation) + "</div>";
  if (rec.technical_metrics) {
    h += "<p><b>Technical metrics of this explanation</b></p><table>";
    for (const k of Object.keys(rec.technical_metrics))
      h += "<tr><th>" + esc(k) + "</th><td>" + esc(Number(rec.technical_metrics[k]).toFixed(4)) + "</td></tr>";
    h += "</table>";
  }
  RUBRIC.forEach(d => {
    h += "<div class='dim'><b>" + esc(d[0]) + "</b>" + esc(d[1]) + "<div class='anch'>" + esc(d[2]) + "</div>";
    for (let s = 1; s <= 5; s++)
      h += "<label class='s'><input type='radio' name='" + i + "_" + d[0] + "' value='" + s + "'> " + s + "</label>";
    h += "</div>";
  });
  h += "<div class='dim'><label>Comment (optional)<br><textarea rows='2' id='c" + i + "'></textarea></label></div>";
  div.innerHTML = h; root.appendChild(div);
  const r = state[c.case_id] || {};
  RUBRIC.forEach(d => {
    div.querySelectorAll("input[name='" + i + "_" + d[0] + "']").forEach(inp => {
      if (String(r[d[0]]) === inp.value) inp.checked = true;
      inp.addEventListener("change", () => {
        state[c.case_id] = state[c.case_id] || {};
        state[c.case_id][d[0]] = Number(inp.value); save(); progress();
      });
    });
  });
  const ta = document.getElementById("c" + i); ta.value = r.comment || "";
  ta.addEventListener("input", () => {
    state[c.case_id] = state[c.case_id] || {}; state[c.case_id].comment = ta.value; save();
  });
});
progress();
document.getElementById("export").addEventListener("click", () => {
  const missing = CASES.filter(c => !complete(c.case_id)).length;
  const msg = document.getElementById("msg");
  if (missing && !confirm(missing + " case(s) are incomplete. Export anyway?")) return;
  const out = { rater: RATER, exported_at: new Date().toISOString(),
    ratings: CASES.map((c, i) => Object.assign({ case_id: c.case_id, position: i + 1 }, state[c.case_id] || {})) };
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([JSON.stringify(out, null, 2)], { type: "application/json" }));
  a.download = "ratings_rater_" + RATER + ".json";
  document.body.appendChild(a); a.click(); a.remove();
  msg.textContent = "File ratings_rater_" + RATER + ".json downloaded.";
});
</script></body></html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    chosen = draw()
    with (OUT / "sample_cases.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["case_id", "dataset", "explainer", "model_family", "quadrant"])
        for c in chosen:
            w.writerow([c["case_id"], c["dataset"], c["explainer"], c["model_family"],
                        c["quadrant"]])
    for rater, seed in RATERS.items():
        order = list(chosen)
        random.Random(seed).shuffle(order)
        cases = []
        for c in order:
            record = prompt_record(c["case_id"])
            shown = {k: v for k, v in record.items() if k not in OMITTED}
            cases.append({"case_id": c["case_id"], "record": shown})
        page = (PAGE.replace("__RATER__", rater)
                .replace("__N__", str(len(cases)))
                .replace("__RUBRIC__", json.dumps(RUBRIC))
                .replace("__CASES__", json.dumps(cases).replace("</", "<\\/")))
        (OUT / f"rating_sheet_rater_{rater}.html").write_text(page, encoding="utf-8",
                                                              newline="\n")
    print(f"OK: {len(chosen)} cases; sheets for raters {', '.join(RATERS)} in {OUT}")


if __name__ == "__main__":
    main()
