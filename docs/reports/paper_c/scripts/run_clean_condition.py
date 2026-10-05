#!/usr/bin/env python3
"""Clean condition of the LLM-judge study: the explanation without metrics, outcome or label.

Plan: docs/reports/paper_c/PLAN.md, section 15.3. A NEW cohort (RCA-002) with its own
directory, docs/reports/paper_c/clean_condition/. It reads the 192 cases and the judge
settings of cohort 2 and writes nothing under experiments/ or outputs/.

The prompt is the primary template (src/prompts/templates/exp4_semantic_eval_v1.j2) with
one sentence changed, and the case record without three fields: technical_metrics, quadrant
and true_label. The rubric is used word for word.

    python docs/reports/paper_c/scripts/run_clean_condition.py --dry-run     # prompts only
    python docs/reports/paper_c/scripts/run_clean_condition.py --limit 2     # a trial
    python docs/reports/paper_c/scripts/run_clean_condition.py               # all 576 calls
    python docs/reports/paper_c/scripts/run_clean_condition.py --parse-only  # rebuild the CSV

A response already on disk is skipped, so an interrupted run resumes. The run needs
OPENROUTER_API_KEY (the client reads configs/secrets/api_keys.env). Use the project .venv.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation import exp4_parser as parser_mod  # noqa: E402
from src.evaluation.exp4_cases import load_manifest, read_cases_jsonl  # noqa: E402
from src.evaluation.exp4_prompts import prompt_version_hash  # noqa: E402
from src.evaluation.exp4_runner import (  # noqa: E402
    _response_envelope, _to_llm_config, build_judgment_id, judge_key)
from src.evaluation.exp4_schema import exp4_output_schema  # noqa: E402

MANIFEST = ROOT / "configs" / "experiments" / "exp4_cohort2" / "manifest.yaml"
TEMPLATE = ROOT / "src" / "prompts" / "templates" / "exp4_semantic_eval_v1.j2"
OUT = Path(__file__).resolve().parents[1] / "clean_condition"
CONDITION = "clean_no_metrics"
REMOVED = ("technical_metrics", "quadrant", "true_label")

OLD_SENTENCE = ("The case record below states the dataset, the model family, the explanation "
                "method, the model's prediction and confidence, and technical metrics computed "
                "for this explanation. The true label is withheld.")
NEW_SENTENCE = ("The case record below states the dataset, the model family, the explanation "
                "method and the model's prediction. The true label and whether the prediction "
                "was correct are not given.")


def template_text() -> str:
    """The primary template without its comment block and with the one changed sentence."""
    text = re.sub(r"\{#-.*?-#\}", "", TEMPLATE.read_text(encoding="utf-8"), flags=re.S)
    if text.count(OLD_SENTENCE) != 1:
        sys.exit("the primary template no longer contains the sentence this script replaces")
    return text.replace(OLD_SENTENCE, NEW_SENTENCE).strip()


def render(case, rubric_version: str, template: str) -> str:
    payload = case.model_dump(mode="json")
    for field in REMOVED:
        payload.pop(field)
    values = {
        "{{ rubric_version }}": rubric_version,
        "{{ case_json }}": json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False),
        "{{ output_schema_json }}": json.dumps(exp4_output_schema(case.case_id), indent=2,
                                               sort_keys=True),
    }
    prompt = template
    for token, value in values.items():
        if token not in prompt:
            sys.exit(f"the primary template has no {token}")
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
    parser_mod._write_csv(out / "clean_llm_scores.csv", rows, parser_mod._score_fieldnames())
    parser_mod._write_csv(out / "clean_parse_failures.csv", failures,
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
    cases = read_cases_jsonl(manifest.paths.cases_dir / "exp4_cases.jsonl")
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
    for n, case in enumerate(cases, 1):
        prompt = render(case, manifest.rubric_version, template)
        p_hash = prompt_version_hash(prompt)
        prompt_path = OUT / "prompts" / f"{case.case_id}_{p_hash}.txt"
        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        if not prompt_path.exists():
            prompt_path.write_text(prompt, encoding="utf-8")
        if args.dry_run:
            continue
        for judge in judges:
            key = judge_key(judge)
            judgment_id = build_judgment_id(case.case_id, key, CONDITION, 1)
            out_path = OUT / "raw_responses" / key / f"{judgment_id}.json"
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
                judgment_id=judgment_id, case=case, judge=judge, prompt_condition=CONDITION,
                prompt_version=p_hash, rubric_version=manifest.rubric_version, replicate=1,
                prompt_path=str(prompt_path.relative_to(ROOT)), response_text=text,
                dry_run=False)
            envelope["response_meta"] = getattr(clients[key], "last_response_meta", None)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(envelope, indent=2, sort_keys=True), encoding="utf-8")
            written += 1
        if n % 20 == 0:
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
