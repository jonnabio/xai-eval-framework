
import sys
import logging
from pathlib import Path
import json

# Add src to path
sys.path.append(".")

from src.api.services.transformer import transform_experiment_to_run
from src.api.services.data_loader import discover_experiment_directories, find_result_files, load_json_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_transformation():
    print("=== Testing Experiment Transformation ===")
    
    exp_dirs = discover_experiment_directories()
    results = find_result_files(exp_dirs[0]) # We know there is only 1 root dir now
    
    success_count = 0
    fail_count = 0
    
    for file_path in results:
        try:
            data = load_json_file(file_path)
            if not data:
                print(f"Skipping empty/invalid file: {file_path}")
                continue
                
            # Simulate the loader's behavior of adding meta
            if isinstance(data, dict):
                 if "experiment_dir_name" not in data:
                        data["_meta_experiment_dir"] = exp_dirs[0].name
            
            run = transform_experiment_to_run(data)
            # print(f"Valid: {file_path.name} -> ID: {run.id}")
            success_count += 1
            
        except Exception as e:
            print(f"FAILED: {file_path} - {e}")
            fail_count += 1

    print("-" * 50)
    print(f"Total Files: {len(results)}")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")

if __name__ == "__main__":
    test_transformation()
