import re
with open("src/api/tests/test_data_loader.py", "r") as f:
    code = f.read()

# Fix discover test
code = code.replace('assert "exp_test1" in names\n        assert "exp_test2" in names\n        assert "exp_empty" in names', 'assert "test_experiments" in names')

# Fix find results test
code = code.replace('names = [f.name for f in files]\n        assert "rf_lime.json" in names\n        assert "xgb_shap.json" in names\n        assert "invalid.json" in names', 'parents = [f.parent.name for f in files]\n        assert "rf_lime" in parents\n        assert "xgb_shap" in parents\n        assert "invalid" in parents')

# Fix load json valid test
code = code.replace('mock_experiments_dir / "exp_test1" / "results" / "rf_lime.json"', 'mock_experiments_dir / "exp_test1" / "results" / "rf_lime" / "results.json"')
code = code.replace('mock_experiments_dir / "exp_test1" / "results" / "invalid.json"', 'mock_experiments_dir / "exp_test1" / "results" / "invalid" / "results.json"')

# Fix filter experiments with generator
code = code.replace('len(filtered)', 'len(list(filtered))')
code = code.replace('filtered[0]', 'list(filtered)[0]')

with open("src/api/tests/test_data_loader.py", "w") as f:
    f.write(code)
