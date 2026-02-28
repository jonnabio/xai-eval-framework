import sys
import os
from pathlib import Path
import json

# Add current directory to path so we can import from src if needed
sys.path.append(os.getcwd())

# Add scripts to path to import monitor_experiments
sys.path.append(os.path.join(os.getcwd(), 'scripts'))

try:
    from monitor_experiments import get_experiment_status
    
    # Run status check
    config_dir = "configs/recovery/phase1"
    print(f"Checking status for config dir: {config_dir}")
    stats, results = get_experiment_status(config_dir)
    
    print(f"Total Experiments: {stats['total']}")
    print(f"Finished: {stats['finished']}")
    print(f"Pending: {stats['pending']}")
    print(f"Running: {len(stats['in_progress'])}")
    print(f"Skipped: {stats['skipped']}")
    
    if stats['in_progress']:
        print(f"\nCurrently Running: {len(stats['in_progress'])} (Details hidden for brevity)")
        for exp in stats['in_progress']:
            print(f"- {exp['name']} (Started: {exp['start_time']}, Duration: {exp['duration'].total_seconds() // 60:.0f} mins)")
            
except Exception as e:
    print(f"Error checking status: {e}")
    # Fallback: manual glob if import fails
    import glob
    print("Attempting manual count...")
    configs = glob.glob(os.path.join("configs/experiments/exp2_scaled", "**/*.yaml"), recursive=True)
    total = len(configs)
    print(f"Total config files found: {total}")
