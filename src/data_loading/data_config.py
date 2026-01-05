from pathlib import Path

import os
# Directory structure
# Use env var or default to /workspace/data if it exists (for container), else local ./data
default_data_dir = "/workspace/data" if Path("/workspace").exists() else "./data"
DATA_ROOT = Path(os.environ.get("DATA_DIR", default_data_dir))
RAW_DATA_DIR = DATA_ROOT / "raw"

# Adult dataset configuration
ADULT_CONFIG = {
    "cache_dir": RAW_DATA_DIR / "adult",
    "expected_rows": 48842,  # approximate total
    "min_rows": 30000,  # minimum valid
    "expected_cols": 15,
    "column_names": [
        'age', 'workclass', 'fnlwgt', 'education', 'education-num',
        'marital-status', 'occupation', 'relationship', 'race', 'sex',
        'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'
    ],
    "sources": {
        "primary": {"method": "openml", "id": "adult", "version": 2},
        "uci_data": "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
        "uci_test": "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test",
    }
}
