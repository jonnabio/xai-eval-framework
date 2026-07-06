#!/usr/bin/env python3
"""
EXP6 masking-sensitivity analysis for Paper BC.

This script reuses stored EXP2 top-feature explanations and recomputes
prediction-drop metrics under multiple masking schemes. It is intentionally
scoped as a top-feature sensitivity check because EXP2 persisted the top-10
attribution values, not full attribution vectors.

Outputs:
    outputs/analysis/exp6_masking_sensitivity/exp6_instance_level.csv
    outputs/analysis/exp6_masking_sensitivity/exp6_run_level.csv
    outputs/analysis/exp6_masking_sensitivity/exp6_paired_shap_lime.csv
    outputs/analysis/exp6_masking_sensitivity/exp6_summary.json
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import joblib
import numpy as np
import pandas as pd
from scipy import stats

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sklearn.model_selection import train_test_split

from src.data_loading.adult import CATEGORICAL_FEATURES, NUMERIC_FEATURES, TARGET_COLUMN


EXP2_RESULTS_DIR = PROJECT_ROOT / "experiments" / "exp2_scaled" / "results"
MODEL_DIR = PROJECT_ROOT / "experiments" / "exp1_adult" / "models"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "analysis" / "exp6_masking_sensitivity"
ADULT_CSV = PROJECT_ROOT / "data" / "adult.csv"

# Targeted probe on RF, where OOD masking can materially affect tree branch
# traversal and where prediction is fast enough for an interactive remediation.
MODELS = ["rf"]
METHODS = ["shap", "lime"]
SEEDS = [42, 123, 456, 789, 999]
# Keep EXP6 intentionally lightweight: one matched size across all model/seed
# cells. This is a masking-sensitivity probe, not a replacement for EXP2.
N_VALUES = [50]
TOP_K = 5
MARGINAL_DRAWS = 3
MAX_INSTANCES_PER_RUN = 40


@dataclass(frozen=True)
class RunKey:
    model: str
    method: str
    seed: int
    n: int


def load_adult_fast(preprocessor: object, random_state: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[str]]:
    """
    Fast local Adult loader for EXP6.

    The standard loader performs cache validation and fallback download checks.
    EXP6 only needs the already cached local CSV plus the fitted preprocessor
    used by the committed models.
    """
    df = pd.read_csv(ADULT_CSV)
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
    df = df.replace(["?", " ?"], np.nan)
    if not np.issubdtype(df[TARGET_COLUMN].dtype, np.number):
        df[TARGET_COLUMN] = df[TARGET_COLUMN].map(
            {"<=50K": 0, "<=50K.": 0, ">50K": 1, ">50K.": 1}
        )
    df = df.dropna(subset=[TARGET_COLUMN]).drop_duplicates()
    df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(int)
    for col in NUMERIC_FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )
    X_train_processed = preprocessor.transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    feature_names = list(NUMERIC_FEATURES)
    ohe = preprocessor.named_transformers_["cat"].named_steps["onehot"]
    feature_names.extend(ohe.get_feature_names_out(CATEGORICAL_FEATURES).tolist())
    return (
        np.asarray(X_train_processed, dtype=float),
        np.asarray(X_test_processed, dtype=float),
        np.asarray(y_train, dtype=int),
        np.asarray(y_test, dtype=int),
        feature_names,
    )


def predict_score(model: object, X: np.ndarray) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)
        if getattr(proba, "ndim", 1) > 1 and proba.shape[1] > 1:
            return np.asarray(proba[:, 1], dtype=float)
        return np.asarray(proba, dtype=float).reshape(-1)
    return np.asarray(model.predict(X), dtype=float).reshape(-1)


def load_models() -> Dict[str, object]:
    models: Dict[str, object] = {}
    for model_name in MODELS:
        path = MODEL_DIR / f"{model_name}.joblib"
        print(f"Loading model {model_name} from {path}", flush=True)
        models[model_name] = joblib.load(path)
    return models


def feature_groups(feature_names: Sequence[str]) -> List[List[int]]:
    """
    Dependency-aware groups in the processed Adult feature space.

    These groups are intentionally conservative and target the correlations
    described in the manuscript: education/education-num, marital status,
    relationship, sex, occupation, and workclass.
    """
    groups_by_prefix = [
        ["education-num", "education_"],
        ["marital-status_", "relationship_", "sex_"],
        ["occupation_", "workclass_"],
    ]
    groups: List[List[int]] = []
    for prefixes in groups_by_prefix:
        idxs = [
            i
            for i, name in enumerate(feature_names)
            if any(name == prefix or name.startswith(prefix) for prefix in prefixes)
        ]
        if idxs:
            groups.append(sorted(set(idxs)))
    return groups


def expand_group(indices: Iterable[int], groups: Sequence[Sequence[int]]) -> List[int]:
    selected = set(indices)
    changed = True
    while changed:
        changed = False
        for group in groups:
            group_set = set(group)
            if selected & group_set and not group_set <= selected:
                selected |= group_set
                changed = True
    return sorted(selected)


def parse_top_features(raw_top: Dict[str, float], feature_index: Dict[str, int]) -> List[Tuple[int, float]]:
    parsed: List[Tuple[int, float]] = []
    for name, value in raw_top.items():
        idx = feature_index.get(name)
        if idx is None:
            continue
        parsed.append((idx, float(value)))
    parsed.sort(key=lambda item: abs(item[1]), reverse=True)
    return parsed


def masked_prediction_drop(
    model: object,
    instance: np.ndarray,
    indices: Sequence[int],
    scheme: str,
    train_mean: np.ndarray,
    X_train: np.ndarray,
    rng: np.random.Generator,
) -> float:
    if not indices:
        return 0.0

    p_orig = float(predict_score(model, instance.reshape(1, -1))[0])
    indices = list(indices)

    if scheme == "zero":
        masked = instance.copy()
        masked[indices] = 0.0
        return abs(p_orig - float(predict_score(model, masked.reshape(1, -1))[0]))

    if scheme == "mean":
        masked = instance.copy()
        masked[indices] = train_mean[indices]
        return abs(p_orig - float(predict_score(model, masked.reshape(1, -1))[0]))

    if scheme == "marginal":
        row_ids = rng.integers(0, X_train.shape[0], size=MARGINAL_DRAWS)
        masked_batch = np.tile(instance, (MARGINAL_DRAWS, 1))
        masked_batch[:, indices] = X_train[row_ids][:, indices]
        p_masked = predict_score(model, masked_batch)
        return float(np.mean(np.abs(p_orig - p_masked)))

    raise ValueError(f"Unknown masking scheme: {scheme}")


def compute_instance_metrics(
    model: object,
    instance: np.ndarray,
    top_features: Sequence[Tuple[int, float]],
    scheme: str,
    train_mean: np.ndarray,
    X_train: np.ndarray,
    groups: Sequence[Sequence[int]],
    rng: np.random.Generator,
) -> Dict[str, float]:
    p_orig = float(predict_score(model, instance.reshape(1, -1))[0])

    def drop_for(indices: Sequence[int], base_scheme: str) -> float:
        if not indices:
            return 0.0
        indices = list(indices)
        if base_scheme == "zero":
            masked = instance.copy()
            masked[indices] = 0.0
            return abs(p_orig - float(predict_score(model, masked.reshape(1, -1))[0]))
        if base_scheme == "mean":
            masked = instance.copy()
            masked[indices] = train_mean[indices]
            return abs(p_orig - float(predict_score(model, masked.reshape(1, -1))[0]))
        if base_scheme == "marginal":
            row_ids = rng.integers(0, X_train.shape[0], size=MARGINAL_DRAWS)
            masked_batch = np.tile(instance, (MARGINAL_DRAWS, 1))
            masked_batch[:, indices] = X_train[row_ids][:, indices]
            p_masked = predict_score(model, masked_batch)
            return float(np.mean(np.abs(p_orig - p_masked)))
        raise ValueError(f"Unknown masking scheme: {base_scheme}")

    top_indices = [idx for idx, _ in top_features[:TOP_K]]
    if scheme == "grouped_mean":
        top_indices_for_gap = expand_group(top_indices, groups)
        single_feature_sets = [expand_group([idx], groups) for idx, _ in top_features]
        base_scheme = "mean"
    else:
        top_indices_for_gap = top_indices
        single_feature_sets = [[idx] for idx, _ in top_features]
        base_scheme = scheme

    topk_gap = drop_for(top_indices_for_gap, base_scheme)

    drops: List[float] = []
    magnitudes: List[float] = []
    for feature_set, (_, weight) in zip(single_feature_sets, top_features):
        drops.append(drop_for(feature_set, base_scheme))
        magnitudes.append(abs(weight))

    if len(drops) < 2 or np.std(drops) < 1e-12 or np.std(magnitudes) < 1e-12:
        corr = 0.0
    else:
        corr = float(stats.pearsonr(magnitudes, drops).statistic)
        if not np.isfinite(corr):
            corr = 0.0

    return {
        "topk_gap": float(topk_gap),
        "top_feature_corr": corr,
        "n_features_masked_topk": float(len(top_indices_for_gap)),
    }


def result_paths() -> Iterable[Tuple[RunKey, Path]]:
    for model in MODELS:
        for method in METHODS:
            for seed in SEEDS:
                for n_value in N_VALUES:
                    path = (
                        EXP2_RESULTS_DIR
                        / f"{model}_{method}"
                        / f"seed_{seed}"
                        / f"n_{n_value}"
                        / "results.json"
                    )
                    if path.exists():
                        yield RunKey(model, method, seed, n_value), path


def holm_adjust(p_values: Sequence[float]) -> List[float]:
    p = np.asarray(p_values, dtype=float)
    order = np.argsort(p)
    adjusted = np.empty_like(p)
    running = 0.0
    m = len(p)
    for rank, idx in enumerate(order):
        candidate = (m - rank) * p[idx]
        running = max(running, candidate)
        adjusted[idx] = min(1.0, running)
    return adjusted.tolist()


def paired_summary(run_df: pd.DataFrame) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    for scheme in ["zero", "mean", "marginal", "grouped_mean"]:
        for metric in ["topk_gap", "top_feature_corr"]:
            pivot = run_df[run_df["masking_scheme"] == scheme].pivot_table(
                index=["model", "seed", "n"], columns="method", values=metric
            )
            pivot = pivot.dropna(subset=["shap", "lime"])
            if pivot.empty:
                continue
            diff = pivot["shap"] - pivot["lime"]
            try:
                stat = stats.wilcoxon(pivot["shap"], pivot["lime"], zero_method="wilcox")
                p_value = float(stat.pvalue)
            except ValueError:
                p_value = 1.0
            dz = float(diff.mean() / diff.std(ddof=1)) if len(diff) > 1 and diff.std(ddof=1) > 0 else 0.0
            rows.append(
                {
                    "masking_scheme": scheme,
                    "metric": metric,
                    "n_pairs": int(len(diff)),
                    "lime_mean": float(pivot["lime"].mean()),
                    "shap_mean": float(pivot["shap"].mean()),
                    "mean_delta_shap_minus_lime": float(diff.mean()),
                    "median_delta_shap_minus_lime": float(diff.median()),
                    "positive_pairs": int((diff > 0).sum()),
                    "wilcoxon_p": p_value,
                    "dz": dz,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["holm_p"] = holm_adjust(out["wilcoxon_p"].tolist())
    return out


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    preprocessor = joblib.load(MODEL_DIR / "preprocessor.joblib")
    models = load_models()

    dataset_cache: Dict[int, Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[str]]] = {}
    instance_rows: List[Dict[str, object]] = []
    schemes = ["zero", "mean", "marginal", "grouped_mean"]

    for key, path in result_paths():
        print(f"Processing {key.model}/{key.method}/seed={key.seed}/n={key.n}", flush=True)
        if key.seed not in dataset_cache:
            print(f"  Loading Adult split for seed {key.seed}", flush=True)
            X_train, X_test, y_train, y_test, feature_names = load_adult_fast(
                preprocessor=preprocessor,
                random_state=key.seed,
            )
            dataset_cache[key.seed] = (X_train, X_test, y_train, y_test, feature_names)
            print(f"  Loaded split: train={X_train.shape}, test={X_test.shape}", flush=True)

        X_train, X_test, y_train, y_test, feature_names = dataset_cache[key.seed]
        train_mean = np.mean(X_train, axis=0)
        groups = feature_groups(feature_names)
        feature_index = {name: idx for idx, name in enumerate(feature_names)}
        model = models[key.model]

        payload = json.loads(path.read_text())
        n_before = len(instance_rows)
        eval_rows = payload.get("instance_evaluations", [])[:MAX_INSTANCES_PER_RUN]
        print(f"  Evaluating {len(eval_rows)} stored instances", flush=True)
        for row_idx, row in enumerate(eval_rows, start=1):
            if row_idx % 10 == 0:
                print(f"    instance {row_idx}/{len(eval_rows)}", flush=True)
            if "error" in row:
                continue
            instance_id = int(row["instance_id"])
            raw_top = row.get("explanation", {}).get("raw_top", {})
            top_features = parse_top_features(raw_top, feature_index)
            if not top_features:
                continue
            instance = np.asarray(X_test[instance_id], dtype=float)
            for scheme in schemes:
                rng = np.random.default_rng(key.seed + instance_id + len(scheme))
                metrics = compute_instance_metrics(
                    model,
                    instance,
                    top_features,
                    scheme,
                    train_mean,
                    X_train,
                    groups,
                    rng,
                )
                instance_rows.append(
                    {
                        "model": key.model,
                        "method": key.method,
                        "seed": key.seed,
                        "n": key.n,
                        "instance_id": instance_id,
                        "masking_scheme": scheme,
                        **metrics,
                    }
                )
        print(f"  Wrote {len(instance_rows) - n_before} scheme-instance rows", flush=True)

    instance_df = pd.DataFrame(instance_rows)
    instance_df.to_csv(OUTPUT_DIR / "exp6_instance_level.csv", index=False)

    run_df = (
        instance_df.groupby(["model", "method", "seed", "n", "masking_scheme"], as_index=False)
        .agg(
            topk_gap=("topk_gap", "mean"),
            top_feature_corr=("top_feature_corr", "mean"),
            n_features_masked_topk=("n_features_masked_topk", "mean"),
            n_instances=("instance_id", "count"),
        )
    )
    run_df.to_csv(OUTPUT_DIR / "exp6_run_level.csv", index=False)

    paired_df = paired_summary(run_df)
    paired_df.to_csv(OUTPUT_DIR / "exp6_paired_shap_lime.csv", index=False)

    summary = {
        "analysis": "EXP6 top-feature masking sensitivity",
        "source_results": str(EXP2_RESULTS_DIR.relative_to(PROJECT_ROOT)),
        "probe_scope": "n=50 matched EXP2 Adult RF runs across five seeds",
        "instance_rows": int(len(instance_df)),
        "run_rows": int(len(run_df)),
        "paired_rows": int(len(paired_df)),
        "masking_schemes": schemes,
        "top_k": TOP_K,
        "marginal_draws": MARGINAL_DRAWS,
        "max_instances_per_run": MAX_INSTANCES_PER_RUN,
        "feature_groups": [
            [feature_names[i] for i in group]
            for group in feature_groups(dataset_cache[SEEDS[0]][4])
        ],
        "paired_summary": paired_df.to_dict(orient="records"),
        "interpretation": (
            "This is a top-feature sensitivity analysis based on stored EXP2 "
            "top-10 explanations. It tests masking-protocol sensitivity of "
            "prediction-drop metrics but does not replace full-vector fidelity."
        ),
    }
    (OUTPUT_DIR / "exp6_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
