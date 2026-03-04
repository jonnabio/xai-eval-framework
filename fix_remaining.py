import os

# Fix extract_results_metadata.py
fp = "src/scripts/extract_results_metadata.py"
with open(fp, "r") as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if "def extract_quantitative_results(results_dir):" in l:
        lines.insert(i+5, "    aggregated_data = {}\n")
        break
for i, l in enumerate(lines):
    if "def extract_cv_results(cv_dir):" in l:
        lines.insert(i+5, "    cv_data = {}\n")
        break
with open(fp, "w") as f:
    f.writelines(lines)

# Fix generate_paper_figures.py
fp = "src/scripts/generate_paper_figures.py"
with open(fp, "r") as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if "def load_cv_data():" in l:
        lines.insert(i+2, "    data = {}\n")
        break
for i, l in enumerate(lines):
    if "def prepare_radar_data(cv_data):" in l:
        lines.insert(i+2, "    radar_data = {}\n")
        break
with open(fp, "w") as f:
    f.writelines(lines)

# Fix shap_tabular.py
fp = "src/xai/shap_tabular.py"
with open(fp, "r") as f:
    content = f.read()
# We need `import logging`, `import time`, `typing`, `numpy`, `shap`, `resample`, `from .base import ExplainerWrapper` at the top
# Let's just find them and move if needed. Or we can just ignore E402 using ruff configuration, which is much safer.
# Using `# noqa: E402` or `# ruff: noqa: E402`
# A better way is to add `--ignore E402` to ruff config if possible, but let's just insert # noqa: E402.
new_lines = []
for l in content.split("\n"):
    if "import logging" in l or "import time" in l or "from typing" in l or "import numpy" in l or "import shap" in l or "from sklearn.utils" in l:
        new_lines.append(l + "  # noqa: E402")
    elif l.startswith("from .base import ExplainerWrapper"):
        new_lines.append(l + "  # noqa: E402")
    else:
        new_lines.append(l)
with open(fp, "w") as f:
    f.write("\n".join(new_lines))

# Fix models/__init__.py
fp = "src/models/__init__.py"
with open(fp, "w") as f:
    f.write('''from .base import BaseTrainer
from .factory import ModelTrainerFactory
from .sklearn_trainers import SVMTrainer, MLPTrainer, LogisticRegressionTrainer
from .rf_trainer import RandomForestTrainer
from .xgboost_trainer import XGBoostTrainer

__all__ = [
    "BaseTrainer",
    "ModelTrainerFactory",
    "SVMTrainer",
    "MLPTrainer",
    "LogisticRegressionTrainer",
    "RandomForestTrainer",
    "XGBoostTrainer"
]
''')

# Fix extract_methodology_metadata.py E722
fp = "src/scripts/extract_methodology_metadata.py"
with open(fp, "r") as f:
    content = f.read()
content = content.replace("except:", "except Exception:")
with open(fp, "w") as f:
    f.write(content)
