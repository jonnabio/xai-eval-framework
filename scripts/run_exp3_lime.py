#!/usr/bin/env python3
"""
EXP3 LIME cross-dataset extension.

Runs LIME on Breast Cancer and German Credit datasets under the same
protocol as the existing EXP3 SHAP/Anchors runs, enabling direct
SHAP-LIME comparison across all three datasets.

Conditions: 2 datasets × 2 models (RF, XGB) × 3 seeds = 12 experiments
N = 100 instances per experiment (50 per class).
Metrics: fidelity, stability, sparsity, cost (same as thesis Appendix C).

Results saved to: outputs/analysis/exp3_lime_results.csv
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import shutil
import sys
import tempfile
import time
import warnings
import logging
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARNING)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loading.cross_dataset import load_tabular_dataset
from src.xai.lime_tabular import LIMETabularWrapper

# ── Constants ────────────────────────────────────────────────────────────────
MODEL_ROOT  = PROJECT_ROOT / "experiments/exp3_cross_dataset/models"
SOURCE_MODEL_ROOT = MODEL_ROOT
OUTPUT_PATH = PROJECT_ROOT / "outputs/analysis/exp3_lime_results.csv"
PAPER_E_OUTPUT_ROOT = (
    PROJECT_ROOT / "outputs/analysis/paper_e/exp3_lime"
)

DATASETS  = ["breast_cancer", "german_credit"]
MODELS    = ["rf", "xgb"]
SEEDS     = [42, 123, 456]

NUM_FEATURES  = 10
NUM_SAMPLES   = 1000
KERNEL_WIDTH  = 3.0
N_PER_CLASS   = 50      # 100 instances total
T_STABILITY   = 15
SIGMA         = 0.1
TOP_K         = 5


# ── Metric helpers ────────────────────────────────────────────────────────────

def stratified_sample(X, y, n, seed):
    rng = np.random.RandomState(seed)
    idx = []
    for cls in np.unique(y):
        pool = np.where(y == cls)[0]
        idx.append(rng.choice(pool, size=min(n, len(pool)), replace=False))
    return np.concatenate(idx)


def fidelity(model, w, inst, baseline):
    p0 = model.predict_proba(inst.reshape(1, -1))[:, 1][0]
    n = len(inst)
    batch = np.tile(inst, (n, 1))
    for i in range(n):
        batch[i, i] = baseline[i]
    drops = np.abs(p0 - model.predict_proba(batch)[:, 1])
    mags  = np.abs(w)
    if np.std(drops) < 1e-9 or np.std(mags) < 1e-9:
        return 0.0
    return float(pearsonr(mags, drops)[0])


def stability(wrapper, model, inst, T, sigma, rng=None):
    vecs = []
    noise_rng = rng if rng is not None else np.random
    for _ in range(T):
        noise = noise_rng.normal(0, sigma, size=inst.shape)
        w = wrapper.explain_instance(model, inst + noise, return_full=False)
        vecs.append(w)
    vecs = np.array(vecs)
    sims = []
    for a in range(T):
        for b in range(a + 1, T):
            na, nb = np.linalg.norm(vecs[a]), np.linalg.norm(vecs[b])
            if na > 1e-10 and nb > 1e-10:
                sims.append(float(cosine_similarity(
                    vecs[a].reshape(1, -1), vecs[b].reshape(1, -1))[0, 0]))
            else:
                sims.append(0.0)
    return float(np.mean(sims)) if sims else 0.0


def sparsity(w, thr=1e-4):
    return float(np.sum(np.abs(w) > thr) / len(w))


# ── Main ──────────────────────────────────────────────────────────────────────

def run_one(dataset, model_name, seed):
    model_dir  = MODEL_ROOT / dataset / model_name / f"seed_{seed}"
    model_path = model_dir / f"{model_name}.joblib"
    prep_path  = model_dir / "preprocessor.joblib"

    preprocessor = joblib.load(prep_path)
    X_tr, X_te, y_tr, y_te, feature_names, _ = load_tabular_dataset(
        dataset,
        cache_dir=str(PROJECT_ROOT / "data"),
        random_state=seed,
        preprocessor=preprocessor,
    )
    model = joblib.load(model_path)

    X_tr_np = X_tr if isinstance(X_tr, np.ndarray) else X_tr.values
    X_te_np = X_te if isinstance(X_te, np.ndarray) else X_te.values
    y_te_np = y_te if isinstance(y_te, np.ndarray) else y_te.values
    baseline = X_tr_np.mean(axis=0)

    idx    = stratified_sample(X_te_np, y_te_np, N_PER_CLASS, seed)
    X_eval = X_te_np[idx]

    wrapper = LIMETabularWrapper(
        training_data=X_tr_np,
        feature_names=feature_names,
        num_features=NUM_FEATURES,
        num_samples=NUM_SAMPLES,
        kernel_width=KERNEL_WIDTH,
        random_state=seed,
    )

    fids, stabs, spars, costs = [], [], [], []
    n_valid = 0

    for inst in X_eval:
        t0 = time.perf_counter()
        w  = wrapper.explain_instance(model, inst, return_full=False)
        costs.append((time.perf_counter() - t0) * 1000)

        if np.sum(np.abs(w) > 1e-4) > 0:
            n_valid += 1
            fids.append(fidelity(model, w, inst, baseline))
            stabs.append(stability(wrapper, model, inst, T_STABILITY, SIGMA))
        spars.append(sparsity(w))

    return {
        "dataset":        dataset,
        "model":          model_name,
        "seed":           seed,
        "n_valid":        n_valid,
        "fidelity_mean":  round(float(np.mean(fids))  if fids  else 0.0, 3),
        "stability_mean": round(float(np.mean(stabs)) if stabs else 0.0, 3),
        "sparsity_mean":  round(float(np.mean(spars)), 3),
        "cost_ms_mean":   round(float(np.mean(costs)), 1),
    }


def main_legacy():
    np.random.seed(42)
    records = []
    total = len(DATASETS) * len(MODELS) * len(SEEDS)
    done  = 0

    for dataset, model_name, seed in product(DATASETS, MODELS, SEEDS):
        done += 1
        print(f"[{done}/{total}] {dataset}  {model_name}  seed={seed} ...", end=" ", flush=True)
        rec = run_one(dataset, model_name, seed)
        records.append(rec)
        print(f"fidelity={rec['fidelity_mean']:.3f}  "
              f"stability={rec['stability_mean']:.3f}  "
              f"valid={rec['n_valid']}/100")

    df = pd.DataFrame(records)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\n=== Summary by dataset+model (mean over seeds) ===")
    summary = df.groupby(["dataset", "model"])[
        ["fidelity_mean", "stability_mean", "sparsity_mean", "cost_ms_mean"]
    ].mean().round(3)
    print(summary.to_string())
    print(f"\nSaved to: {OUTPUT_PATH}")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha256_array(values: np.ndarray) -> str:
    contiguous = np.ascontiguousarray(values)
    return hashlib.sha256(contiguous.view(np.uint8)).hexdigest()


def target_instance_ids(source_rows: list[dict[str, Any]], test_size: int) -> list[int]:
    ids = []
    for row in source_rows:
        instance_id = row.get("instance_id")
        if isinstance(instance_id, bool) or not isinstance(instance_id, int):
            raise ValueError("Every source explanation must have an integer instance_id")
        if instance_id < 0 or instance_id >= test_size:
            raise ValueError(
                f"Source instance_id {instance_id} is outside X_test range [0, {test_size})"
            )
        ids.append(instance_id)
    if len(ids) != len(set(ids)):
        raise ValueError("Source SHAP explanations contain duplicate instance IDs")
    return sorted(ids)


def validate_source_predictions(
    source_rows: list[dict[str, Any]],
    y_test: np.ndarray,
    predictions: np.ndarray,
) -> None:
    rows_by_id = {row["instance_id"]: row for row in source_rows}
    ids = target_instance_ids(source_rows, len(y_test))
    for instance_id in ids:
        row = rows_by_id[instance_id]
        label = int(y_test[instance_id])
        prediction = int(predictions[instance_id])
        if label != row.get("true_label"):
            raise ValueError(
                f"True-label mismatch for source instance {instance_id}: "
                f"stored={row.get('true_label')} current={label}"
            )
        if prediction != row.get("prediction"):
            raise ValueError(
                f"Prediction mismatch for source instance {instance_id}: "
                f"stored={row.get('prediction')} current={prediction}"
            )
        if bool(label == prediction) != row.get("prediction_correct"):
            raise ValueError(
                f"Correctness mismatch for source instance {instance_id}"
            )


def validate_training_reproduction(
    actual_summary: dict[str, Any],
    source_summary: dict[str, Any],
) -> None:
    for key in ("dataset", "model", "seed", "n_train", "n_test", "n_features"):
        if actual_summary.get(key) != source_summary.get(key):
            raise ValueError(
                f"Reproduced training summary mismatch for {key}: "
                f"stored={source_summary.get(key)!r} "
                f"reproduced={actual_summary.get(key)!r}"
            )

    actual_metrics = actual_summary.get("metrics")
    source_metrics = source_summary.get("metrics")
    if not isinstance(actual_metrics, dict) or not isinstance(source_metrics, dict):
        raise ValueError("Training summaries must contain metric objects")
    if actual_metrics.keys() != source_metrics.keys():
        raise ValueError("Reproduced training summary metric names differ")

    for metric, expected in source_metrics.items():
        observed = actual_metrics[metric]
        if isinstance(expected, list):
            if observed != expected:
                raise ValueError(
                    f"Reproduced training metric mismatch for {metric}"
                )
        elif (
            isinstance(expected, (int, float))
            and isinstance(observed, (int, float))
        ):
            if not np.isclose(observed, expected, rtol=0, atol=1e-12):
                raise ValueError(
                    f"Reproduced training metric mismatch for {metric}: "
                    f"stored={expected!r} reproduced={observed!r}"
                )
        elif observed != expected:
            raise ValueError(
                f"Reproduced training metric mismatch for {metric}"
            )


def serialize_attributions(
    weights: list[float] | np.ndarray,
    feature_names: list[str],
    top_k: int = NUM_FEATURES,
) -> dict[str, Any]:
    values = np.asarray(weights, dtype=float)
    if values.ndim != 1 or len(values) != len(feature_names):
        raise ValueError("Attribution vector length must match feature_names")
    if not np.isfinite(values).all():
        raise ValueError("Attribution vector contains non-finite values")

    ranked = sorted(
        zip(feature_names, values.tolist()),
        key=lambda item: -abs(item[1]),
    )
    return {
        "raw_top": {name: value for name, value in ranked[:top_k]},
        "raw_attributions": {
            name: float(value) for name, value in zip(feature_names, values)
        },
    }


def run_one_paper_e(
    dataset: str,
    model_name: str,
    seed: int,
    output_root: Path,
    model_root: Path = MODEL_ROOT,
    cache_dir: Path = PROJECT_ROOT / "data",
) -> dict[str, Any]:
    model_dir = model_root / dataset / model_name / f"seed_{seed}"
    model_path = model_dir / f"{model_name}.joblib"
    prep_path = model_dir / "preprocessor.joblib"
    source_path = (
        PROJECT_ROOT
        / "experiments/exp3_cross_dataset/results"
        / dataset
        / f"{model_name}_shap"
        / f"seed_{seed}"
        / "n_100/results.json"
    )
    source_model_dir = (
        SOURCE_MODEL_ROOT / dataset / model_name / f"seed_{seed}"
    )
    output_path = (
        output_root / dataset / model_name / f"seed_{seed}" / "results.json"
    )
    if output_path.exists():
        raise FileExistsError(
            f"Paper E LIME output already exists; refusing to overwrite: {output_path}"
        )
    if not source_path.is_file():
        raise FileNotFoundError(f"Stored SHAP source run is missing: {source_path}")

    source_payload = json.loads(source_path.read_text(encoding="utf-8"))
    source_rows = source_payload.get("instance_evaluations")
    if not isinstance(source_rows, list) or not source_rows:
        raise ValueError(f"Stored SHAP run has no instance rows: {source_path}")

    metadata_path = source_model_dir / "metadata.json"
    reproduced_metadata_path = model_dir / "metadata.json"
    source_summary_path = source_model_dir / "exp3_training_summary.json"
    reproduced_summary_path = model_dir / "exp3_training_summary.json"
    for required_path in (
        metadata_path,
        reproduced_metadata_path,
        source_summary_path,
        reproduced_summary_path,
    ):
        if not required_path.is_file():
            raise FileNotFoundError(
                f"Required EXP3 model provenance file is missing: {required_path}"
            )
    expected_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    reproduced_metadata = json.loads(
        reproduced_metadata_path.read_text(encoding="utf-8")
    )
    for key in ("model_class", "config", "feature_names"):
        if reproduced_metadata.get(key) != expected_metadata.get(key):
            raise ValueError(
                f"Reproduced model metadata mismatch for {key}: "
                f"{dataset}/{model_name}/seed_{seed}"
            )
    source_summary = json.loads(source_summary_path.read_text(encoding="utf-8"))
    reproduced_summary = json.loads(
        reproduced_summary_path.read_text(encoding="utf-8")
    )
    validate_training_reproduction(reproduced_summary, source_summary)

    preprocessor = joblib.load(prep_path)
    X_tr, X_te, y_tr, y_te, feature_names, _ = load_tabular_dataset(
        dataset,
        cache_dir=str(cache_dir),
        random_state=seed,
        preprocessor=preprocessor,
    )
    if feature_names != expected_metadata.get("feature_names"):
        raise ValueError(
            f"Reproduced feature order differs from stored EXP3 metadata: "
            f"{dataset}/{model_name}/seed_{seed}"
        )
    X_tr_np = np.asarray(X_tr, dtype=float)
    X_te_np = np.asarray(X_te, dtype=float)
    y_tr_np = np.asarray(y_tr)
    y_te_np = np.asarray(y_te)
    model = joblib.load(model_path)
    predictions = np.asarray(model.predict(X_te_np))
    validate_source_predictions(source_rows, y_te_np, predictions)
    ids = target_instance_ids(source_rows, len(X_te_np))

    wrapper = LIMETabularWrapper(
        training_data=X_tr_np,
        feature_names=feature_names,
        num_features=NUM_FEATURES,
        num_samples=NUM_SAMPLES,
        kernel_width=KERNEL_WIDTH,
        random_state=seed,
    )
    rng = np.random.default_rng(seed)
    baseline = X_tr_np.mean(axis=0)
    rows_by_id = {row["instance_id"]: row for row in source_rows}
    instance_records = []
    for position, instance_id in enumerate(ids, start=1):
        instance = X_te_np[instance_id]
        started = time.perf_counter()
        weights, _ = wrapper.explain_instance(model, instance, return_full=True)
        cost_ms = (time.perf_counter() - started) * 1000
        serialized = serialize_attributions(weights, feature_names)
        has_attribution = bool(np.any(np.abs(weights) > 1e-4))
        if has_attribution:
            fidelity_value = fidelity(model, weights, instance, baseline)
            stability_value = stability(
                wrapper, model, instance, T_STABILITY, SIGMA, rng=rng
            )
        else:
            fidelity_value = None
            stability_value = None

        source = rows_by_id[instance_id]
        instance_records.append(
            {
                "instance_id": instance_id,
                "true_label": int(y_te_np[instance_id]),
                "prediction": int(predictions[instance_id]),
                "prediction_correct": bool(
                    y_te_np[instance_id] == predictions[instance_id]
                ),
                "quadrant": source.get("quadrant"),
                "explanation_valid": has_attribution,
                "metrics": {
                    "fidelity": fidelity_value,
                    "stability": stability_value,
                    "sparsity": sparsity(weights),
                    "cost_ms": cost_ms,
                },
                "explanation": serialized,
            }
        )
        if position % 25 == 0 or position == len(ids):
            print(
                f"    {dataset}/{model_name}/seed_{seed}: "
                f"{position}/{len(ids)} instances"
            )

    cached_dataset_path = (
        cache_dir / "openml/dataset_31_credit-g.arff"
        if dataset == "german_credit"
        else None
    )
    if cached_dataset_path is not None and not cached_dataset_path.is_file():
        raise FileNotFoundError(
            f"German Credit dataset cache is missing after loading: "
            f"{cached_dataset_path}"
        )

    output = {
        "experiment_metadata": {
            "experiment": "paper_e_exp3_lime",
            "status": "complete",
            "dataset": dataset,
            "model": model_name,
            "seed": seed,
            "source_method": "shap",
            "source_run_path": source_path.relative_to(PROJECT_ROOT).as_posix(),
            "target_instance_count": len(ids),
            "target_instance_ids": ids,
            "lime": {
                "num_features": NUM_FEATURES,
                "num_samples": NUM_SAMPLES,
                "kernel_width": KERNEL_WIDTH,
                "stability_perturbations": T_STABILITY,
                "stability_sigma": SIGMA,
                "random_state": seed,
            },
            "model_sha256": _sha256(model_path),
            "preprocessor_sha256": _sha256(prep_path),
            "training_model_class": expected_metadata.get("model_class"),
            "training_script_sha256": _sha256(
                PROJECT_ROOT / "scripts/train_exp3_models.py"
            ),
            "lime_script_sha256": _sha256(Path(__file__).resolve()),
            "data_loader_sha256": _sha256(
                PROJECT_ROOT / "src/data_loading/cross_dataset.py"
            ),
            "source_training_summary_path": (
                source_summary_path.relative_to(PROJECT_ROOT).as_posix()
            ),
            "source_training_summary_sha256": _sha256(source_summary_path),
            "training_config": expected_metadata.get("config"),
            "dataset_source": (
                "sklearn.datasets.load_breast_cancer"
                if dataset == "breast_cancer"
                else "https://www.openml.org/data/download/31/dataset_31_credit-g.arff"
            ),
            "dataset_cache_sha256": (
                _sha256(cached_dataset_path)
                if cached_dataset_path is not None
                else None
            ),
            "train_features_sha256": _sha256_array(X_tr_np),
            "train_labels_sha256": _sha256_array(y_tr_np),
            "test_features_sha256": _sha256_array(X_te_np),
            "test_labels_sha256": _sha256_array(y_te_np),
            "feature_names": list(feature_names),
            "python": platform.python_version(),
            "numpy": importlib.metadata.version("numpy"),
            "pandas": importlib.metadata.version("pandas"),
            "scipy": importlib.metadata.version("scipy"),
            "joblib": importlib.metadata.version("joblib"),
            "scikit_learn": importlib.metadata.version("scikit-learn"),
            "lime_version": importlib.metadata.version("lime"),
            "xgboost": importlib.metadata.version("xgboost"),
            "created_utc": datetime.now(timezone.utc).isoformat(),
        },
        "instance_evaluations": instance_records,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(".tmp")
    temporary_path.write_text(
        json.dumps(output, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(output_path)
    return {
        "dataset": dataset,
        "model": model_name,
        "seed": seed,
        "status": "complete",
        "instance_count": len(ids),
        "valid_explanations": sum(
            row["explanation_valid"] for row in instance_records
        ),
        "output_path": output_path.relative_to(output_root).as_posix(),
    }


def run_paper_e(
    output_root: Path,
    model_root: Path = MODEL_ROOT,
    cache_dir: Path = PROJECT_ROOT / "data",
) -> None:
    output_root = output_root.resolve()
    if output_root.exists():
        raise FileExistsError(
            f"Paper E output directory already exists; refusing to overwrite: {output_root}"
        )
    output_root.parent.mkdir(parents=True, exist_ok=True)
    staging_root = Path(
        tempfile.mkdtemp(
            prefix=f".{output_root.name}.",
            dir=output_root.parent,
        )
    )
    try:
        run_records = []
        for dataset, model_name, seed in product(DATASETS, MODELS, SEEDS):
            print(f"[Paper E] {dataset} {model_name} seed={seed}")
            run_records.append(
                run_one_paper_e(
                    dataset,
                    model_name,
                    seed,
                    staging_root,
                    model_root=model_root,
                    cache_dir=cache_dir,
                )
            )

        manifest = {
            "experiment": "paper_e_exp3_lime",
            "status": "complete",
            "source": "stored EXP3 SHAP instance IDs",
            "runs": run_records,
        }
        (staging_root / "manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        staging_root.replace(output_root)
        print(
            f"Completed {len(run_records)} instance-aligned LIME runs. "
            f"Manifest: {output_root / 'manifest.json'}"
        )
    finally:
        if staging_root.exists():
            shutil.rmtree(staging_root)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--paper-e",
        action="store_true",
        help="Run a new, instance-aligned Paper E cohort without replacing legacy output.",
    )
    parser.add_argument(
        "--paper-e-output-dir",
        type=Path,
        default=PAPER_E_OUTPUT_ROOT,
        help="Empty directory for the new Paper E cohort.",
    )
    parser.add_argument(
        "--model-root",
        type=Path,
        default=MODEL_ROOT,
        help="Directory containing the EXP3 model and preprocessor artifacts.",
    )
    parser.add_argument(
        "--data-cache-dir",
        type=Path,
        default=PROJECT_ROOT / "data",
        help="Directory used for local dataset caches.",
    )
    args = parser.parse_args()
    if args.paper_e:
        run_paper_e(
            args.paper_e_output_dir,
            model_root=args.model_root,
            cache_dir=args.data_cache_dir,
        )
    else:
        main_legacy()


if __name__ == "__main__":
    main()
