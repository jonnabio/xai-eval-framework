import sys
from pathlib import Path
project_root = Path("/home/jonnabio/Documents/GitHub/xai-eval-framework")
sys.path.insert(0, str(project_root))

from src.api.services.data_loader import find_result_files, load_json_file, get_experiments_dir

def debug_data_points():
    base_dir = get_experiments_dir()
    all_files = find_result_files(base_dir)
    
    total_points = 0
    exp_count = 0
    
    recovery_points = 0
    recovery_count = 0
    
    for f in all_files:
        data = load_json_file(f)
        if data and isinstance(data, dict):
            pts = len(data.get("instance_evaluations", []))
            total_points += pts
            exp_count += 1
            
            if "recovery" in str(f):
                recovery_points += pts
                recovery_count += 1
                
    print(f"Total Healthy Experiments: {exp_count}")
    print(f"Total Data Points: {total_points}")
    print(f"Recovery Experiments: {recovery_count}")
    print(f"Recovery Data Points: {recovery_points}")
    print(f"Legacy (Non-Recovery) Data Points: {total_points - recovery_points}")

if __name__ == "__main__":
    debug_data_points()
