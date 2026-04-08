import os
import itertools
import random

models = ["logreg", "mlp", "rf", "svm", "xgb"]
methods = ["anchors", "dice", "lime", "shap"]
seeds = [42, 123, 456, 789, 999]
mid_ns = [50, 100, 200]

base_dir = "experiments/exp2_scaled/results"
missing = []

for model in models:
    for method in methods:
        for seed in seeds:
            for n in mid_ns:
                # Construct expected path
                path = os.path.join(base_dir, f"{model}_{method}", f"seed_{seed}", f"n_{n}", "results.json")
                if not os.path.exists(path):
                    missing.append(f"{model}_{method}_s{seed}_n{n}")

random.shuffle(missing)

print(f"Total missing: {len(missing)}")
for m in missing:
    print(m)
