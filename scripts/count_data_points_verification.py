
import json
import os
from pathlib import Path

def count_data_points():
    experiments_dir = Path("experiments")
    total_points = 0
    file_count = 0
    
    print(f"{'File':<60} | {'Points':<10}")
    print("-" * 75)
    
    for results_file in experiments_dir.glob("**/results.json"):
        try:
            with open(results_file, 'r') as f:
                data = json.load(f)
                
            points = 0
            if isinstance(data, dict):
                if "instance_evaluations" in data and isinstance(data["instance_evaluations"], list):
                    points = len(data["instance_evaluations"])
                # Handle potential other formats if necessary, but instance_evaluations is the standard
            
            if points > 0:
                print(f"{str(results_file):<60} | {points:<10}")
                total_points += points
                file_count += 1
                
        except Exception as e:
            print(f"Error reading {results_file}: {e}")

    print("-" * 75)
    print(f"Total Files with Data: {file_count}")
    print(f"Total Data Points: {total_points}")

if __name__ == "__main__":
    count_data_points()
