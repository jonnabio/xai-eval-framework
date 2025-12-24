"""Quick test for API sample data."""
import requests
import sys

BASE_URL = "http://localhost:8000"

try:
    # Test 1: Count total runs
    print("1. Counting total runs...")
    response = requests.get(f"{BASE_URL}/api/runs")
    if response.status_code == 200:
        total = response.json().get("pagination", {}).get("total")
        print(f"   Total runs: {total}")
    else:
        print(f"   Failed: {response.status_code}")

    # Test 2: Filter LIME
    print("\n2. Counting LIME experiments...")
    response = requests.get(f"{BASE_URL}/api/runs?method=LIME")
    if response.status_code == 200:
        total = response.json().get("pagination", {}).get("total")
        print(f"   LIME runs: {total}")
    else:
        print(f"   Failed: {response.status_code}")

    # Test 3: Filter SHAP
    print("\n3. Counting SHAP experiments...")
    response = requests.get(f"{BASE_URL}/api/runs?method=SHAP")
    if response.status_code == 200:
        total = response.json().get("pagination", {}).get("total")
        print(f"   SHAP runs: {total}")
    else:
        print(f"   Failed: {response.status_code}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
