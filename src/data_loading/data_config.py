from pathlib import Path

# Directory structure
DATA_ROOT = Path("./data")
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
