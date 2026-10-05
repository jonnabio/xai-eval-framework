#!/usr/bin/env python3
"""Positive control of the LLM-judge study: explanations made worse in a known way.

Plan: docs/reports/paper_c/PLAN.md, section 18.3. A NEW cohort (RCA-002) with its own
directory, docs/reports/paper_c/positive_control/. It reads the cases and the judge settings
of cohort 2 and writes nothing under experiments/ or outputs/.

Cases: the SHAP and LIME cases with a non-zero printed weight (79). Each is shown in three
versions of its explanation text, in the prompt of the clean condition word for word:

    original    the stored text
    truncated   the three items with the largest absolute weight, the rest removed
    shuffled    the same names and weights, the names reassigned by a permutation that
                leaves no name in its place; the weights keep their order

    python docs/reports/paper_c/scripts/run_positive_control.py --dry-run     # prompts only
    python docs/reports/paper_c/scripts/run_positive_control.py --limit 2     # a trial
    python docs/reports/paper_c/scripts/run_positive_control.py               # all 711 calls
    python docs/reports/paper_c/scripts/run_positive_control.py --parse-only  # rebuild the CSV

A response already on disk is skipped, so an interrupted run resumes. The run needs
OPENROUTER_API_KEY (the client reads configs/secrets/api_keys.env). Use the project .venv.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
for p in (str(ROOT), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

from src.evaluation import exp4_parser as parser_mod  # noqa: E402
from src.evaluation.exp4_cases import _count_tokens, load_manifest, read_cases_jsonl  # noqa: E402
from src.evaluation.exp4_prompts import prompt_version_hash  # noqa: E402
from src.evaluation.exp4_runner import (  # noqa: E402
    _response_envelope, _to_llm_config, build_judgment_id, judge_key)
from src.evaluation.exp4_schema import exp4_output_schema  # noqa: E402
from paper_c_reliability import all_weights_zero  # noqa: E402
from run_clean_condition import MANIFEST, REMOVED, template_text  # noqa: E402

OUT = HERE.parent / "positive_control"
VERSIONS = ("original", "truncated", "shuffled")
EXPLAINERS = ("shap", "lime")
KEPT_ITEMS = 3
SEED = 20261005


def split(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Header and (name, weight as printed) items of a rendered explanation."""
    header, body = text.split(": ", 1)
    items = [tuple(part.rsplit(": ", 1)) for part in body.split("; ")]
    if f"{header}: " + "; ".join(f"{n}: {w}" for n, w in items) != text:
        sys.exit(f"cannot split and rebuild the explanation text: {text[:80]}")
    return header, items


def join(header: str, items: list[tuple[str, str]]) -> str:
    return f"{header}: " + "; ".join(f"{n}: {w}" for n, w in items)


def version_text(text: str, version: str, index: int) -> str:
    header, items = split(text)
    if version == "original":
        return text
    if version == "truncated":
        keep = sorted(range(len(items)), key=lambda i: -abs(float(items[i][1])))[:KEPT_ITEMS]
        return join(header, [items[i] for i in sorted(keep)])
    rng = random.Random(SEED + index)
    order = list(range(len(items)))
    while any(i == j for i, j in enumerate(order)):
        rng.shuffle(order)
    return join(header, [(items[j][0], items[i][1]) for i, j in enumerate(order)])


def render(case, text: str, rubric_version: str, template: str) -> str:
    payload = case.model_dump(mode="json")
    for field in REMOVED:
        payload.pop(field)
    payload["normalized_explanation"] = text
    payload["explanation_length_tokens"] = _count_tokens(text)
    values = {
        "{{ rubric_version }}": rubric_version,
        "{{ case_json }}": json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False),
        "{{ output_schema_json }}": json.dumps(exp4_output_schema(case.case_id), indent=2,
                                               sort_keys=True),
    }
    prompt = template
    for token, value in values.items():
        prompt = prompt.replace(token, value)
    if "{{" in prompt or "{%" in prompt:
        sys.exit("unrendered template syntax left in the prompt")
    return prompt


def parse() -> dict:
    rows, failures = [], []
    for raw_path in parser_mod.iter_raw_response_files(OUT / "raw_responses"):
        envelope, judgment, error = parser_mod.parse_raw_response_file(raw_path)
        rel = raw_path.relative_to(ROOT)
        if judgment is None:
            failures.append(parser_mod._failure_row(envelope, rel, error or "unknown"))
        else:
            rows.append(parser_mod._score_row(envelope, judgment, rel))
    out = OUT / "parsed_scores"
    out.mkdir(parents=True, exist_ok=True)
    parser_mod._write_csv(out / "positive_control_llm_scores.csv", rows,
                          parser_mod._score_fieldnames())
    parser_mod._write_csv(out / "positive_control_parse_failures.csv", failures,
                          parser_mod._failure_fieldnames())
    return {"parsed": len(rows), "failed": len(failures)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="write the prompts, call no judge")
    ap.add_argument("--limit", type=int, default=None, help="first N cases only")
    ap.add_argument("--parse-only", action="store_true")
    ap.add_argument("--judge", default=None, help="one judge_id of the manifest")
    ap.add_argument("--shard", default=None, metavar="I/N",
                    help="cases I, I+N, I+2N, ... (0-based); run several in parallel, then "
                         "--parse-only")
    args = ap.parse_args()

    if args.parse_only:
        print(parse())
        return 0

    manifest = load_manifest(MANIFEST)
    cases = [(i, c) for i, c in enumerate(read_cases_jsonl(manifest.paths.cases_dir / "exp4_cases.jsonl"))
             if c.explainer in EXPLAINERS and not all_weights_zero(c.normalized_explanation)]
    if args.limit:
        cases = cases[:args.limit]
    if args.shard:
        index, count = (int(v) for v in args.shard.split("/"))
        cases = cases[index::count]
    judges = [j for j in manifest.judges if args.judge in (None, judge_key(j))]
    if not judges:
        sys.exit(f"no judge '{args.judge}' in {MANIFEST}")
    template = template_text()

    clients = {}
    if not args.dry_run:
        from src.llm.client import LLMClientFactory
        clients = {judge_key(j): LLMClientFactory.create(_to_llm_config(j)) for j in judges}

    written = skipped = errors = 0
    for n, (index, case) in enumerate(cases, 1):
        for version in VERSIONS:
            condition = f"control_{version}"
            prompt = render(case, version_text(case.normalized_explanation, version, index),
                            manifest.rubric_version, template)
            p_hash = prompt_version_hash(prompt)
            prompt_path = OUT / "prompts" / condition / f"{case.case_id}_{p_hash}.txt"
            prompt_path.parent.mkdir(parents=True, exist_ok=True)
            if not prompt_path.exists():
                prompt_path.write_text(prompt, encoding="utf-8")
            if args.dry_run:
                continue
            for judge in judges:
                key = judge_key(judge)
                judgment_id = build_judgment_id(case.case_id, key, condition, 1)
                out_path = OUT / "raw_responses" / key / condition / f"{judgment_id}.json"
                if out_path.exists():
                    skipped += 1
                    continue
                try:
                    text = clients[key].generate(prompt)
                except Exception as exc:  # the next run fills the gap
                    errors += 1
                    print(f"ERROR {case.case_id} {key}: {type(exc).__name__}: {exc}", flush=True)
                    continue
                envelope = _response_envelope(
                    judgment_id=judgment_id, case=case, judge=judge, prompt_condition=condition,
                    prompt_version=p_hash, rubric_version=manifest.rubric_version, replicate=1,
                    prompt_path=str(prompt_path.relative_to(ROOT)), response_text=text,
                    dry_run=False)
                envelope["response_meta"] = getattr(clients[key], "last_response_meta", None)
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(json.dumps(envelope, indent=2, sort_keys=True),
                                    encoding="utf-8")
                written += 1
        if n % 10 == 0:
            print(f"{n}/{len(cases)} cases; written {written}, skipped {skipped}, "
                  f"errors {errors}", flush=True)

    print(f"prompts for {len(cases)} cases in {OUT / 'prompts'}")
    if not args.dry_run:
        print(f"written {written}, skipped {skipped}, errors {errors}")
        if not args.shard and not args.judge:
            print(parse())
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
