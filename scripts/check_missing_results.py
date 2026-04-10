import json
import os
from pathlib import Path

models = ["logreg", "mlp", "rf", "svm", "xgb"]
methods = ["anchors", "dice", "lime", "shap"]
seeds = [42, 123, 456, 789, 999]
mid_ns = [50, 100, 200]

base_dir = Path("experiments/exp2_scaled/results")
comparative_dir = Path("experiments/exp2_comparative/results")

# Conservative runtime fallbacks, in seconds, based on local docs.
default_method_cost = {
    "shap": 60.0,
    "lime": 300.0,
    "dice": 9000.0,
    "anchors": 10800.0,
}


def load_runtime_estimates() -> dict[tuple[str, str], float]:
    estimates: dict[tuple[str, str], float] = {}

    for results_json in comparative_dir.glob("*_*/results.json"):
        try:
            payload = json.loads(results_json.read_text(encoding="utf-8"))
            stem = results_json.parent.name
            model, method = stem.split("_", 1)
            duration = float(payload["experiment_metadata"]["duration_seconds"])
            estimates[(model, method)] = duration
        except Exception:
            continue

    return estimates


runtime_estimates = load_runtime_estimates()
missing: list[tuple[float, str]] = []

for model in models:
    for method in methods:
        for seed in seeds:
            for n in mid_ns:
                path = base_dir / f"{model}_{method}" / f"seed_{seed}" / f"n_{n}" / "results.json"
                if path.exists():
                    continue

                base_runtime = runtime_estimates.get((model, method), default_method_cost[method])
                estimated_runtime = base_runtime * (n / 100.0)
                exp_name = f"{model}_{method}_s{seed}_n{n}"
                missing.append((estimated_runtime, exp_name))

missing.sort(key=lambda item: (item[0], item[1]))

print(f"Total missing: {len(missing)}")
for _, exp_name in missing:
    print(exp_name)
