"""Validate sample experiment data files."""
import json
from pathlib import Path
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from src.api.services.data_loader import find_result_files
from src.api.services.transformer import transform_experiment_to_run

print("=" * 70)
print("SAMPLE DATA VALIDATION")
print("=" * 70)

sample_dir = Path("experiments/sample_data")
results_dir = sample_dir / "results"

if not results_dir.exists():
    print(f"✗ Results directory not found: {results_dir}")
    exit(1)

# Find all JSON files
json_files = list(results_dir.glob("*.json"))
print(f"\nFound {len(json_files)} JSON files")

valid_count = 0
invalid_count = 0

for json_file in json_files:
    print(f"\n{'='*70}")
    print(f"Validating: {json_file.name}")
    print(f"{'='*70}")
    
    # Test 1: Valid JSON
    try:
        with open(json_file) as f:
            data = json.load(f)
        print("  ✓ Valid JSON format")
    except json.JSONDecodeError as e:
        print(f"  ✗ Invalid JSON: {e}")
        invalid_count += 1
        continue
    
    # Test 2: Required fields present
    required_fields = [
        "model_name", "model_type", "dataset", "xai_method",
        "accuracy", "timestamp", "metrics", "llm_evaluation"
    ]
    
    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        print(f"  ✗ Missing fields: {missing_fields}")
        invalid_count += 1
        continue
    else:
        print("  ✓ All required fields present")
    
    # Test 3: Transform to Run model
    try:
        # Augment with meta info expected by transformer (usually added by loader)
        data["_meta_experiment_dir"] = str(json_file.parent.parent)
        
        run = transform_experiment_to_run(data)
        print(f"  ✓ Transformation successful")
        print(f"    - Run ID: {run.id}")
        print(f"    - Model: {run.modelName}")
        print(f"    - Method: {run.method}")
        print(f"    - Accuracy: {run.accuracy:.2f}%")
        print(f"    - Explainability Score: {run.explainabilityScore:.3f}")
        valid_count += 1
    except Exception as e:
        print(f"  ✗ Transformation failed: {e}")
        invalid_count += 1
        continue

# Summary
print("\n" + "=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)
print(f"Total files: {len(json_files)}")
print(f"Valid: {valid_count}")
print(f"Invalid: {invalid_count}")

if invalid_count == 0:
    print("\n✅ All sample files are valid!")
else:
    print(f"\n⚠️  {invalid_count} file(s) failed validation")
    exit(1)
