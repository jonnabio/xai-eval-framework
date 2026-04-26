#!/usr/bin/env python3
"""
Build an integrated EXP1/EXP2/EXP3 evidence package.

The script intentionally uses only the Python standard library so it can run in
the lightweight Windows/WSL environments used for result consolidation.
"""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path
from statistics import mean, pstdev
from typing import Dict, Iterable, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "analysis" / "integrated_evidence"

EXP1_CORE = [
    PROJECT_ROOT / "experiments" / "exp1_adult" / "results" / "rf_lime" / "results.json",
    PROJECT_ROOT / "experiments" / "exp1_adult" / "results" / "rf_shap" / "results.json",
    PROJECT_ROOT / "experiments" / "exp1_adult" / "results" / "xgb_lime" / "results.json",
    PROJECT_ROOT / "experiments" / "exp1_adult" / "results" / "xgb_shap" / "results.json",
]
EXP2_RESULTS = PROJECT_ROOT / "experiments" / "exp2_scaled" / "results"
EXP2_RECOVERY_OVERLAY = PROJECT_ROOT / "outputs" / "batch_results.csv"
EXP3_RESULTS = PROJECT_ROOT / "experiments" / "exp3_cross_dataset" / "results"

METRICS = ["fidelity", "stability", "sparsity", "faithfulness_gap", "cost", "duration_s"]
EXP2_OVERLAY_RE = re.compile(r"rec_p1_exp2_([a-z0-9]+)_([a-z]+)_s(\d+)_n(\d+)")


@dataclass
class RunRecord:
    experiment: str
    dataset: str
    model: str
    explainer: str
    seed: Optional[int]
    n: Optional[int]
    source: str
    path: str
    fidelity: Optional[float] = None
    stability: Optional[float] = None
    sparsity: Optional[float] = None
    faithfulness_gap: Optional[float] = None
    cost: Optional[float] = None
    duration_s: Optional[float] = None

    @property
    def key(self) -> tuple:
        return (self.experiment, self.dataset, self.model, self.explainer, self.seed, self.n)


def read_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_metric_name(name: str) -> str:
    mapping = {
        "efficiencyms": "cost",
        "causalalignment": "causal_alignment",
        "counterfactualsensitivity": "counterfactual_sensitivity",
    }
    lowered = name.replace("_", "").lower()
    return mapping.get(lowered, name.lower())


def metric_from_aggregates(payload: Dict[str, object]) -> Dict[str, float]:
    metrics: Dict[str, float] = {}
    aggregated = payload.get("aggregated_metrics", {})
    if not isinstance(aggregated, dict):
        return metrics

    for raw_name, raw_value in aggregated.items():
        name = normalize_metric_name(str(raw_name))
        if name not in METRICS:
            continue
        if isinstance(raw_value, dict) and "mean" in raw_value:
            metrics[name] = float(raw_value["mean"])
        elif isinstance(raw_value, (int, float)):
            metrics[name] = float(raw_value)

    return metrics


def metric_from_instances(payload: Dict[str, object]) -> Dict[str, float]:
    values: Dict[str, List[float]] = defaultdict(list)
    instances = payload.get("instance_evaluations", [])
    if not isinstance(instances, list):
        return {}

    for row in instances:
        if not isinstance(row, dict):
            continue
        row_metrics = row.get("metrics", {})
        if not isinstance(row_metrics, dict):
            continue
        for name in METRICS:
            value = row_metrics.get(name)
            if isinstance(value, (int, float)):
                values[name].append(float(value))

    return {name: mean(vals) for name, vals in values.items() if vals}


def parse_payload_metrics(payload: Dict[str, object]) -> Dict[str, Optional[float]]:
    metrics = metric_from_instances(payload)
    metrics.update(metric_from_aggregates(payload))

    meta = payload.get("experiment_metadata", {})
    if isinstance(meta, dict) and isinstance(meta.get("duration_seconds"), (int, float)):
        metrics["duration_s"] = float(meta["duration_seconds"])

    return {name: metrics.get(name) for name in METRICS}


def clean_model_name(raw_model: str, fallback: str = "unknown") -> str:
    model = (raw_model or fallback).lower()
    for prefix in ("adult_", "breast_cancer_", "german_credit_"):
        if model.startswith(prefix):
            return model[len(prefix) :]
    return model


def run_from_payload(path: Path, experiment: str, dataset: Optional[str] = None) -> RunRecord:
    payload = read_json(path)
    meta = payload.get("experiment_metadata", {})
    model_info = payload.get("model_info", {})
    if not isinstance(meta, dict):
        meta = {}
    if not isinstance(model_info, dict):
        model_info = {}

    name = str(meta.get("name", path.parent.name))
    model = clean_model_name(str(model_info.get("name", "")), fallback=path.parent.name.split("_")[0])
    explainer = str(model_info.get("explainer_method", path.parent.name.split("_")[-1])).lower()
    seed = meta.get("random_seed")

    record = RunRecord(
        experiment=experiment,
        dataset=str(dataset or meta.get("dataset", "unknown")),
        model=model,
        explainer=explainer,
        seed=int(seed) if isinstance(seed, int) else None,
        n=None,
        source="raw",
        path=str(path.relative_to(PROJECT_ROOT)),
        **parse_payload_metrics(payload),
    )

    n_match = re.search(r"_n(\d+)$", name)
    if n_match:
        record.n = int(n_match.group(1))
    return record


def load_exp1() -> List[RunRecord]:
    return [run_from_payload(path, "exp1", dataset="adult") for path in EXP1_CORE if path.exists()]


def load_exp2_raw() -> List[RunRecord]:
    rows: List[RunRecord] = []
    for path in sorted(EXP2_RESULTS.glob("*/*/n_*/results.json")):
        payload = read_json(path)
        instances = payload.get("instance_evaluations", [])
        if not isinstance(instances, list) or not instances:
            continue

        model_method = path.parts[-4]
        seed_part = path.parts[-3]
        n_part = path.parts[-2]
        if "_" not in model_method:
            continue
        model, explainer = model_method.split("_", 1)
        try:
            seed = int(seed_part.split("_", 1)[1])
            n_value = int(n_part.split("_", 1)[1])
        except (IndexError, ValueError):
            continue

        record = run_from_payload(path, "exp2", dataset="adult")
        if any(getattr(record, metric) is None for metric in ["fidelity", "stability", "sparsity", "faithfulness_gap", "cost"]):
            continue
        record.model = model
        record.explainer = explainer
        record.seed = seed
        record.n = n_value
        rows.append(record)
    return rows


def load_exp2_overlay() -> List[RunRecord]:
    if not EXP2_RECOVERY_OVERLAY.exists():
        return []

    rows: List[RunRecord] = []
    with EXP2_RECOVERY_OVERLAY.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            match = EXP2_OVERLAY_RE.fullmatch(row.get("experiment_name", ""))
            if not match:
                continue
            model, explainer, seed, n_value = match.groups()
            rows.append(
                RunRecord(
                    experiment="exp2",
                    dataset=row.get("dataset", "adult"),
                    model=model,
                    explainer=explainer,
                    seed=int(seed),
                    n=int(n_value),
                    source="recovery_overlay",
                    path=f"{EXP2_RECOVERY_OVERLAY.relative_to(PROJECT_ROOT)}::{row['experiment_name']}",
                    fidelity=float(row["fidelity_mean"]),
                    stability=float(row["stability_mean"]),
                    sparsity=float(row["sparsity_mean"]),
                    faithfulness_gap=float(row["faithfulness_gap_mean"]),
                    cost=float(row["cost_mean"]),
                    duration_s=float(row["duration"]) if row.get("duration") else None,
                )
            )
    return rows


def load_exp2() -> List[RunRecord]:
    raw = load_exp2_raw()
    overlay = load_exp2_overlay()
    by_key = {row.key: row for row in raw}
    for row in overlay:
        by_key[row.key] = row
    return sorted(by_key.values(), key=lambda r: (r.model, r.explainer, r.seed or -1, r.n or -1))


def load_exp3() -> List[RunRecord]:
    rows: List[RunRecord] = []
    for path in sorted(EXP3_RESULTS.glob("*/*/*/n_*/results.json")):
        dataset = path.parts[-5]
        model_method = path.parts[-4]
        seed_part = path.parts[-3]
        n_part = path.parts[-2]
        if "_" not in model_method:
            continue
        model, explainer = model_method.split("_", 1)
        record = run_from_payload(path, "exp3", dataset=dataset)
        record.model = model
        record.explainer = explainer
        record.seed = int(seed_part.split("_", 1)[1])
        record.n = int(n_part.split("_", 1)[1])
        rows.append(record)
    return rows


def mean_or_none(values: Iterable[Optional[float]]) -> Optional[float]:
    clean = [v for v in values if v is not None]
    return mean(clean) if clean else None


def std_or_none(values: Iterable[Optional[float]]) -> Optional[float]:
    clean = [v for v in values if v is not None]
    return pstdev(clean) if len(clean) > 1 else 0.0 if clean else None


def format_float(value: Optional[float], digits: int = 3) -> str:
    if value is None:
        return "NA"
    return f"{value:.{digits}f}"


def build_summary(rows: List[RunRecord], group_cols: List[str]) -> List[Dict[str, object]]:
    grouped: Dict[tuple, List[RunRecord]] = defaultdict(list)
    for row in rows:
        grouped[tuple(getattr(row, col) for col in group_cols)].append(row)

    summaries: List[Dict[str, object]] = []
    for key, group in sorted(grouped.items()):
        summary = {col: val for col, val in zip(group_cols, key)}
        summary["runs"] = len(group)
        for metric in METRICS:
            summary[f"{metric}_mean"] = mean_or_none(getattr(row, metric) for row in group)
            summary[f"{metric}_std"] = std_or_none(getattr(row, metric) for row in group)
        summaries.append(summary)
    return summaries


def write_csv(path: Path, rows: List[Dict[str, object]], fieldnames: List[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: List[List[str]], headers: List[str]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    out.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(out)


def find_summary(summary_rows: List[Dict[str, object]], **match: object) -> Optional[Dict[str, object]]:
    for row in summary_rows:
        if all(row.get(k) == v for k, v in match.items()):
            return row
    return None


def build_publication_trace() -> List[Dict[str, str]]:
    return [
        {
            "surface": "thesis",
            "chapter_or_section": "Capitulo 4 resultados; external validity discussion",
            "primary_inputs": "EXP2 statistical cohort plus EXP3 merged validation",
            "generated_artifact": "thesis_fragment_es.qmd",
            "claim_boundary": "Adult-centered benchmark with two-domain external tabular validation",
        },
        {
            "surface": "paper_a",
            "chapter_or_section": "framework and benchmark validity",
            "primary_inputs": "EXP1 calibration, EXP2 qualified analysis, EXP3 portability check",
            "generated_artifact": "paper_a_exp3_addendum.md",
            "claim_boundary": "framework portability, not universal cross-domain dominance",
        },
        {
            "surface": "paper_b",
            "chapter_or_section": "quality-cost frontier",
            "primary_inputs": "EXP2 SHAP-LIME paired evidence plus EXP3 SHAP-Anchors contrast",
            "generated_artifact": "paper_b_exp3_addendum.md",
            "claim_boundary": "SHAP technical-quality result generalizes to EXP3, but runtime trade-offs are method/dataset dependent",
        },
        {
            "surface": "paper_c",
            "chapter_or_section": "metric taxonomy and semantic-evaluation agenda",
            "primary_inputs": "EXP1/EXP2 proxy metrics and EXP3 cross-domain artifacts",
            "generated_artifact": "paper_c_exp3_addendum.md",
            "claim_boundary": "metric-layer complementarity, not validated human semantic preference",
        },
    ]


def build_markdown_outputs(
    snapshot: Dict[str, object],
    method_summary: List[Dict[str, object]],
    exp_dataset_summary: List[Dict[str, object]],
) -> Dict[str, str]:
    exp2_shap = find_summary(method_summary, experiment="exp2", explainer="shap")
    exp2_lime = find_summary(method_summary, experiment="exp2", explainer="lime")
    exp2_anchors = find_summary(method_summary, experiment="exp2", explainer="anchors")
    exp2_dice = find_summary(method_summary, experiment="exp2", explainer="dice")
    exp3_shap = find_summary(method_summary, experiment="exp3", explainer="shap")
    exp3_anchors = find_summary(method_summary, experiment="exp3", explainer="anchors")

    table_rows = []
    for exp_name in ["exp1", "exp2", "exp3"]:
        for explainer in ["shap", "lime", "anchors", "dice"]:
            row = find_summary(method_summary, experiment=exp_name, explainer=explainer)
            if not row:
                continue
            table_rows.append(
                [
                    exp_name.upper(),
                    explainer,
                    str(row["runs"]),
                    format_float(row.get("fidelity_mean")),
                    format_float(row.get("stability_mean")),
                    format_float(row.get("sparsity_mean")),
                    format_float(row.get("cost_mean"), 1),
                ]
            )

    dataset_rows = []
    for row in exp_dataset_summary:
        if row["experiment"] != "exp3":
            continue
        dataset_rows.append(
            [
                str(row["dataset"]),
                str(row["explainer"]),
                str(row["runs"]),
                format_float(row.get("fidelity_mean")),
                format_float(row.get("stability_mean")),
                format_float(row.get("sparsity_mean")),
                format_float(row.get("duration_s_mean"), 1),
            ]
        )

    exp2_fid_gap = (
        (exp2_shap or {}).get("fidelity_mean", 0.0) - (exp2_lime or {}).get("fidelity_mean", 0.0)
        if exp2_shap and exp2_lime
        else None
    )
    exp3_fid_gap = (
        (exp3_shap or {}).get("fidelity_mean", 0.0) - (exp3_anchors or {}).get("fidelity_mean", 0.0)
        if exp3_shap and exp3_anchors
        else None
    )

    integration_summary = f"""# Integrated Evidence Snapshot: EXP1 + EXP2 + EXP3

Date: {date.today().isoformat()}
Status: Generated analysis handoff

## Scope

This package integrates the three empirical layers used by the thesis and paper
track:

- EXP1: Adult calibration and reproducibility baseline.
- EXP2: Adult robustness benchmark and primary inferential cohort.
- EXP3: two-domain external tabular validation on Breast Cancer and German
  Credit.

## Completeness

```text
EXP1 core runs: {snapshot['counts']['exp1_core_runs']} / 4
EXP2 analyzable runs after recovery overlay: {snapshot['counts']['exp2_analyzable_runs']} / 300 planned
EXP2 recovery overlay rows: {snapshot['counts']['exp2_overlay_rows']}
EXP3 completed runs: {snapshot['counts']['exp3_runs']} / 24
```

## Method-Level Snapshot

{markdown_table(table_rows, ["Experiment", "Explainer", "Runs", "Fidelity", "Stability", "Active-feature ratio", "Cost (ms)"])}

## EXP3 Dataset Snapshot

{markdown_table(dataset_rows, ["Dataset", "Explainer", "Runs", "Fidelity", "Stability", "Active-feature ratio", "Duration (s)"])}

## Integrated Interpretation

- EXP1 remains the calibration layer: it establishes Adult baseline behavior for
  RF/XGB with LIME and SHAP before the robustness campaign.
- EXP2 remains the primary inferential layer: it provides the large factorial
  Adult benchmark, recovery-overlay qualification, non-parametric tests, and the
  strongest evidence for method ranking.
- EXP3 is the external-validity layer: it should be used to qualify, not replace,
  the EXP2 claim. The thesis-level wording should be "Adult-centered benchmark
  with two-domain external tabular validation."
- In the integrated evidence package, SHAP retains the technical-quality profile
  established in EXP2. The EXP2 SHAP-LIME mean fidelity gap is
  {format_float(exp2_fid_gap)}, and the EXP3 SHAP-Anchors mean fidelity gap is
  {format_float(exp3_fid_gap)}.
- The runtime story must remain bounded. EXP2 supports LIME as the low-latency
  attribution method, while EXP3 shows that Anchors can be slower than SHAP in
  the completed cross-dataset matrix.

## Use Rules

- Use EXP2 for confirmatory statistical claims.
- Use EXP3 for portability and external-validity language.
- Use EXP1 for calibration, reproducibility, and historical continuity.
- Do not pool EXP3 with EXP2 for a single omnibus hypothesis test unless a new
  preregistered cross-study statistical design is added.
"""

    thesis_fragment = f"""<!-- Generated by scripts/integrate_experiment_evidence.py -->

### Integracion EXP1-EXP2-EXP3

La evidencia empirica queda organizada en tres capas complementarias. EXP1
funciona como calibracion sobre Adult; EXP2 constituye el benchmark confirmativo
principal sobre Adult; y EXP3 opera como validacion externa compacta sobre dos
dominios tabulares adicionales. En conjunto, la formulacion mas precisa para la
tesis es: **benchmark centrado en Adult con validacion tabular externa en dos
dominios**.

EXP2 conserva el peso inferencial principal: {snapshot['counts']['exp2_analyzable_runs']}
ejecuciones analizables despues de aplicar la superposicion de recuperacion
documentada. EXP3 anade {snapshot['counts']['exp3_runs']} ejecuciones completas,
distribuidas entre Breast Cancer y German Credit, y permite comprobar si los
patrones tecnicos principales se mantienen fuera de Adult.

La sintesis integrada muestra continuidad en la ventaja tecnica de SHAP en
fidelidad y estabilidad, pero tambien obliga a matizar el argumento de coste:
LIME sigue siendo el comparador de baja latencia en EXP2, mientras que en EXP3
Anchors resulta computacionalmente mas costoso que SHAP en promedio. Por ello,
la conclusion no debe formularse como una jerarquia universal de metodos, sino
como una frontera de seleccion dependiente del objetivo: fidelidad/estabilidad,
parsimonia, forma explicativa y restricciones de tiempo.
"""

    paper_a = f"""# Paper A EXP3 Integration Addendum

EXP3 strengthens Paper A as a framework manuscript. The result should be framed
as a portability check: the same runner, artifact contract, and metric bundle
were applied beyond Adult to Breast Cancer and German Credit. The added claim is
not that the benchmark is universal; it is that the framework can accumulate
cross-dataset tabular evidence without changing the evidence protocol.

Recommended sentence:

> Beyond the Adult-centered robustness benchmark, a compact 24-run validation on
> Breast Cancer and German Credit reproduced the central technical pattern:
> SHAP retained higher fidelity/stability than Anchors, while Anchors retained a
> compact rule-style profile.
"""

    paper_b = f"""# Paper B EXP3 Integration Addendum

Paper B remains a SHAP-LIME paired comparison based on EXP2. EXP3 should be used
as supporting context rather than as a new primary test because EXP3 compares
SHAP with Anchors, not LIME.

The useful contribution is interpretive: SHAP's high technical-quality profile
persists when contrasted against a rule-style method on additional tabular
datasets. However, EXP3 also shows that runtime trade-offs are not universal:
Anchors was slower than SHAP in the merged EXP3 package.
"""

    paper_c = """# Paper C EXP3 Integration Addendum

EXP3 supports Paper C's argument that XAI evaluation must remain layered.
Technical proxy metrics, explanation form, and semantic plausibility are not the
same construct. The merged EXP3 artifacts provide paired dense-attribution
outputs and compact rule-style outputs on identical model/dataset cells, making
them suitable candidates for later semantic or LLM-judge comparison.

Recommended use: cite EXP3 as a source of cross-domain artifacts for future
semantic evaluation, not as evidence that semantic preference has already been
validated.
"""

    return {
        "integration_summary.md": integration_summary,
        "thesis_fragment_es.qmd": thesis_fragment,
        "paper_a_exp3_addendum.md": paper_a,
        "paper_b_exp3_addendum.md": paper_b,
        "paper_c_exp3_addendum.md": paper_c,
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    exp1 = load_exp1()
    exp2_raw = load_exp2_raw()
    exp2_overlay = load_exp2_overlay()
    exp2 = load_exp2()
    exp3 = load_exp3()
    rows = exp1 + exp2 + exp3

    method_summary = build_summary(rows, ["experiment", "explainer"])
    exp_dataset_summary = build_summary(rows, ["experiment", "dataset", "explainer"])
    model_method_summary = build_summary(rows, ["experiment", "dataset", "model", "explainer"])

    snapshot = {
        "generated_on": date.today().isoformat(),
        "source_roots": {
            "exp1_core": [str(path.relative_to(PROJECT_ROOT)) for path in EXP1_CORE],
            "exp2_scaled": str(EXP2_RESULTS.relative_to(PROJECT_ROOT)),
            "exp2_recovery_overlay": str(EXP2_RECOVERY_OVERLAY.relative_to(PROJECT_ROOT)),
            "exp3_cross_dataset": str(EXP3_RESULTS.relative_to(PROJECT_ROOT)),
        },
        "counts": {
            "exp1_core_runs": len(exp1),
            "exp2_present_result_files": len(list(EXP2_RESULTS.glob("*/*/n_*/results.json"))),
            "exp2_qualified_raw_runs": len(exp2_raw),
            "exp2_overlay_rows": len(exp2_overlay),
            "exp2_analyzable_runs": len(exp2),
            "exp3_runs": len(exp3),
            "integrated_run_rows": len(rows),
        },
        "method_summary": method_summary,
        "publication_traceability": build_publication_trace(),
    }

    run_rows = [asdict(row) for row in rows]
    run_fields = list(run_rows[0].keys()) if run_rows else []
    summary_fields = ["experiment", "explainer", "runs"] + [
        f"{metric}_{suffix}" for metric in METRICS for suffix in ("mean", "std")
    ]
    dataset_fields = ["experiment", "dataset", "explainer", "runs"] + [
        f"{metric}_{suffix}" for metric in METRICS for suffix in ("mean", "std")
    ]
    model_fields = ["experiment", "dataset", "model", "explainer", "runs"] + [
        f"{metric}_{suffix}" for metric in METRICS for suffix in ("mean", "std")
    ]

    write_csv(OUTPUT_DIR / "run_level_metrics.csv", run_rows, run_fields)
    write_csv(OUTPUT_DIR / "method_summary.csv", method_summary, summary_fields)
    write_csv(OUTPUT_DIR / "dataset_method_summary.csv", exp_dataset_summary, dataset_fields)
    write_csv(OUTPUT_DIR / "model_method_summary.csv", model_method_summary, model_fields)
    write_csv(
        OUTPUT_DIR / "publication_traceability.csv",
        snapshot["publication_traceability"],
        ["surface", "chapter_or_section", "primary_inputs", "generated_artifact", "claim_boundary"],
    )
    (OUTPUT_DIR / "evidence_snapshot.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")

    for filename, content in build_markdown_outputs(snapshot, method_summary, exp_dataset_summary).items():
        (OUTPUT_DIR / filename).write_text(content, encoding="utf-8")

    print(f"Integrated evidence written to {OUTPUT_DIR}")
    print(json.dumps(snapshot["counts"], indent=2))


if __name__ == "__main__":
    main()
