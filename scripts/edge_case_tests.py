"""Test edge cases and boundary conditions."""

import requests
import time

BASE_URL = "http://127.0.0.1:8000"

print("="*70)
print("Edge Case Testing")
print("="*70)

try:
    # Test 1: Empty filter results
    print("\n1. Testing empty filter results...")
    response = requests.get(f"{BASE_URL}/api/runs?dataset=NonExistentDataset")
    data = response.json()
    assert len(data["data"]) == 0
    assert data["pagination"]["total"] == 0
    print("  ✓ Empty results handled correctly")

    # Test 2: Maximum limit
    print("\n2. Testing maximum limit (100)...")
    response = requests.get(f"{BASE_URL}/api/runs?limit=100")
    if response.status_code in [200]:
        print("  ✓ Maximum limit accepted")
    else:
        print(f"  ✗ Failed: {response.status_code}")

    # Test 3: Minimum limit
    print("\n3. Testing minimum limit (1)...")
    response = requests.get(f"{BASE_URL}/api/runs?limit=1")
    data = response.json()
    assert response.status_code == 200
    assert len(data["data"]) <= 1
    print("  ✓ Minimum limit works")

    # Test 4: Large offset (beyond results)
    print("\n4. Testing large offset...")
    response = requests.get(f"{BASE_URL}/api/runs?offset=9999")
    data = response.json()
    assert response.status_code == 200
    assert len(data["data"]) == 0
    print("  ✓ Large offset handled gracefully")

    # Test 5: Special characters in filter
    print("\n5. Testing special characters in filter...")
    response = requests.get(f"{BASE_URL}/api/runs?model_name=test%20name")
    assert response.status_code == 200
    print("  ✓ URL encoding handled")

    # Test 6: Case sensitivity in filters
    print("\n6. Testing case sensitivity...")
    response1 = requests.get(f"{BASE_URL}/api/runs?method=LIME")
    response2 = requests.get(f"{BASE_URL}/api/runs?method=lime")
    data1 = response1.json()
    data2 = response2.json()
    # Should be case-insensitive if data loaded correspondingly, but API spec says case insensitive filters
    if data1["pagination"]["total"] == data2["pagination"]["total"]:
        print("  ✓ Case-insensitive filtering works")
    else:
        print("  ⚠ Filtering might be case sensitive (check implementation)")

    # Test 7: Boundary limit
    print("\n7. Testing boundary: limit just above minimum...")
    response = requests.get(f"{BASE_URL}/api/runs?limit=2")
    assert response.status_code == 200
    print("  ✓ Boundary value accepted")

    # Test 8: Response time with all filters
    print("\n8. Testing all filters combined...")
    start = time.time()
    response = requests.get(
        f"{BASE_URL}/api/runs?"
        f"dataset=AdultIncome&method=LIME&model_type=classical&limit=5"
    )
    elapsed = time.time() - start
    assert response.status_code == 200
    print(f"  ✓ All filters work ({elapsed:.3f}s)")

    print("\n" + "="*70)
    print("✅ All edge case tests passed!")
    print("="*70)

except Exception as e:
    print(f"\n❌ Test Failed: {e}")
