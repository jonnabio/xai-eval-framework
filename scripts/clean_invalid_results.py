import shutil
from pathlib import Path

def clean_invalid():
    results_dir = Path("experiments/exp2_comparative/results")
    if not results_dir.exists():
        return

    print(f"Scanning {results_dir} for invalid results...")
    
    count = 0
    for exp_folder in results_dir.iterdir():
        if not exp_folder.is_dir():
            continue
            
        metrics_csv = exp_folder / "metrics.csv"
        results_json = exp_folder / "results.json"
        
        # Criteria for invalid:
        # 1. metrics.csv missing
        # 2. metrics.csv empty (size < 10 bytes)
        # 3. metrics.csv exists but results.json missing (less likely to cause skip, but bad)
        
        is_invalid = False
        reason = ""
        
        if not metrics_csv.exists():
            is_invalid = True
            reason = "Missing metrics.csv"
        elif metrics_csv.stat().st_size < 10:
            is_invalid = True
            reason = "Empty metrics.csv"
            
        if is_invalid:
            print(f"Removing {exp_folder.name}: {reason}")
            # Remove the whole folder to force re-run
            shutil.rmtree(exp_folder)
            count += 1
            
    print(f"\nRemoved {count} invalid experiment result folders.")

if __name__ == "__main__":
    clean_invalid()
