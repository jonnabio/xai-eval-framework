
import subprocess

def check_git_tracking():
    print("Checking git tracking for experiments/exp1_adult/results...")
    try:
        # List all files in the directory that are tracked by git
        result = subprocess.run(
            ["git", "ls-files", "experiments/exp1_adult/results"],
            capture_output=True,
            text=True
        )
        files = result.stdout.splitlines()
        print(f"Tracked files count: {len(files)}")
        # print first 10
        for f in files[:10]:
            print(f"  - {f}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_git_tracking()
