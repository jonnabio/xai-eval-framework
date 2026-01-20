
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.append(".")

from src.api.services.data_loader import load_all_experiments, discover_experiment_directories, find_result_files

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_loading():
    print("=== Debugging Data Loader ===")
    
    # 1. Discover Directories
    exp_dirs = discover_experiment_directories()
    print(f"Discovered {len(exp_dirs)} experiment directories:")
    for d in exp_dirs:
        print(f"  - {d}")

    # 2. Find Files
    total_files = 0
    for d in exp_dirs:
        files = find_result_files(d)
        print(f"Directory {d.name}: Found {len(files)} result files")
        total_files += len(files)
        for f in files:
            print(f"    - {f.relative_to(d)}")

    print(f"Total files found: {total_files}")
    
    # 3. Load Experiments
    print("\nAttempting to load experiments...")
    experiments = load_all_experiments()
    print(f"Successfully loaded {len(experiments)} experiments")
    
    # 4. Breakdown by directory
    counts = {}
    for exp in experiments:
        meta = exp.get("_meta_experiment_dir") or "unknown"
        # If not set in loader (depends on implementation version), try to infer
        if not meta and "experiment_metadata" in exp:
             # Just strictly use what load_all_experiments does
             pass
        # Wait, the current implementation adds _meta_experiment_dir if missing
        
        counts[meta] = counts.get(meta, 0) + 1
        
    print("\nLoaded Count by Directory:")
    for k, v in counts.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    debug_loading()
