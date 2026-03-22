import os
import itertools

models = ["rf", "xgb", "svm", "mlp", "logreg"]
explainers = ["shap", "lime", "anchors", "dice"]
seeds = ["42", "123", "456", "789", "999"]
sample_sizes = ["50", "100", "200"]

base_dir = r"c:\Users\jonna\OneDrive\Documentos\Code__Projects_Local\xai-eval-framework\experiments\exp2_scaled\results"

missing = []

for mod, exp, s, n in itertools.product(models, explainers, seeds, sample_sizes):
    folder_name = f"{mod}_{exp}"
    seed_folder = f"seed_{s}"
    n_folder = f"n_{n}"
    
    expected_path = os.path.join(base_dir, folder_name, seed_folder, n_folder, "results.json")
    if not os.path.exists(expected_path):
        missing.append((mod, exp, s, n))

print(f"Total missing: {len(missing)}")
for m in missing[:10]:
    print(m)
if len(missing) > 10:
    print("...")
