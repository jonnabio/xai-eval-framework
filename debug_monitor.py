
import sys
import os
from pathlib import Path
import glob
from datetime import datetime

# Add root to path
sys.path.append(os.getcwd())

try:
    from src.experiment.config import load_config
except ImportError:
    # Try adding parent
    sys.path.append(str(Path(os.getcwd()).parent))
    from src.experiment.config import load_config

def check_status(config_dir="configs/experiments"):
    print(f"Scanning {config_dir}...")
    configs = glob.glob(os.path.join(config_dir, "**/*.yaml"), recursive=True)
    print(f"Found {len(configs)} config files.")
    
    stats = {"total": 0, "finished": 0, "running": 0, "pending": 0, "skipped": 0}
    
    for cfg_path in configs:
        if "manifest" in cfg_path:
            continue
            
        print(f"Checking {cfg_path}...", end="")
        try:
            cfg = load_config(Path(cfg_path))
        except Exception as e:
            print(f" FAILED to load: {e}")
            stats["skipped"] += 1
            continue
            
        out_dir = cfg.output_dir
        res_file = out_dir / "results.json"
        
        if res_file.exists():
            print(" FINISHED")
            stats["finished"] += 1
        elif out_dir.exists():
            print(" RUNNING")
            stats["running"] += 1
        else:
            print(f" PENDING (Expected: {out_dir})")
            stats["pending"] += 1
            
        stats["total"] += 1
        
    print("\nSummary:")
    print(stats)

if __name__ == "__main__":
    check_status()
