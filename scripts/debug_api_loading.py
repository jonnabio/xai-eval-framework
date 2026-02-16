import sys
from pathlib import Path
project_root = Path("/home/jonnabio/Documents/GitHub/xai-eval-framework")
sys.path.insert(0, str(project_root))

from src.api.services.data_loader import find_result_files, load_json_file, get_experiments_dir

def debug_loading():
    base_dir = get_experiments_dir()
    all_files = find_result_files(base_dir)
    print(f"Total files on disk: {len(all_files)}")
    
    found_count = 0
    corrupt_files = []
    missing_data_files = []
    
    for f in all_files:
        data = load_json_file(f)
        if data is None:
            corrupt_files.append(str(f))
            continue
            
        if not isinstance(data, dict):
            missing_data_files.append(str(f))
            continue
            
        found_count += 1
        
    print(f"Successfully loaded: {found_count}")
    print(f"Corrupt (JSON Error): {len(corrupt_files)}")
    for cf in corrupt_files:
        print(f"  - {cf}")
    print(f"Invalid format: {len(missing_data_files)}")

if __name__ == "__main__":
    debug_loading()
