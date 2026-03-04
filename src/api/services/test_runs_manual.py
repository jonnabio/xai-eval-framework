"""Manual test of runs endpoints with real data."""
import requests

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("MANUAL RUNS ENDPOINTS TEST")
print("=" * 70)

# Test 1: List all runs
print("\n1. Testing GET /api/runs (all runs)...")
try:
    response = requests.get(f"{BASE_URL}/api/runs")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Total runs: {data['pagination']['total']}")
        print(f"   ✓ Returned: {data['pagination']['returned']}")
        
        if data['data']:
            print(f"   ✓ First run ID: {data['data'][0]['id']}")
            first_run_id = data['data'][0]['id']
        else:
            first_run_id = None
    else:
        print(f"   ✗ Failed: {response.text}")
        first_run_id = None
except Exception as e:
    print(f"   ✗ Connection failed: {e}")
    first_run_id = None

# Test 2: Filter by dataset
print("\n2. Testing filters (dataset=AdultIncome)...")
try:
    response = requests.get(f"{BASE_URL}/api/runs?dataset=AdultIncome")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Filtered results: {len(data['data'])}")
except Exception as e:
    print(f"   ✗ Connection failed: {e}")


# Test 3: Pagination
print("\n3. Testing pagination (limit=5)...")
try:
    response = requests.get(f"{BASE_URL}/api/runs?limit=5")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Returned: {data['pagination']['returned']}")
        print(f"   ✓ Has next: {data['pagination']['hasNext']}")
except Exception as e:
    print(f"   ✗ Connection failed: {e}")

# Test 4: Get single run
if first_run_id:
    print(f"\n4. Testing GET /api/runs/{first_run_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/runs/{first_run_id}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Run ID: {data['data']['id']}")
            print(f"   ✓ Model: {data['data']['modelName']}")
            print(f"   ✓ Method: {data['data']['method']}")
            print(f"   ✓ Accuracy: {data['data']['accuracy']:.2f}%")
    except Exception as e:
        print(f"   ✗ Connection failed: {e}")

# Test 5: Get non-existent run
print("\n5. Testing 404 (non-existent run)...")
try:
    response = requests.get(f"{BASE_URL}/api/runs/nonexistent_xyz")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 404:
        print("   ✓ Correctly returns 404")
except Exception as e:
    print(f"   ✗ Connection failed: {e}")

print("\n" + "=" * 70)
print("✅ MANUAL TEST COMPLETE")
print("=" * 70)
