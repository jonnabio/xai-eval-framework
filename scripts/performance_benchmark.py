"""Performance benchmarking for API endpoints."""

import requests
import time
import statistics
import sys

BASE_URL = "http://127.0.0.1:8000"
ITERATIONS = 10

def benchmark_endpoint(name: str, url: str):
    """Benchmark an endpoint."""
    print(f"\nBenchmarking: {name}")
    print("-" * 50)
    
    times = []
    for i in range(ITERATIONS):
        try:
            start = time.time()
            response = requests.get(url, timeout=5)
            elapsed = time.time() - start
            times.append(elapsed)
            
            if response.status_code != 200:
                print(f"  ⚠ Iteration {i+1}: Status {response.status_code}")
        except Exception as e:
            print(f"  ⚠ Iteration {i+1}: Error {e}")
    
    if times:
        avg = statistics.mean(times)
        median = statistics.median(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"  Iterations: {ITERATIONS}")
        print(f"  Average:    {avg*1000:.2f}ms")
        print(f"  Median:     {median*1000:.2f}ms")
        print(f"  Min:        {min_time*1000:.2f}ms")
        print(f"  Max:        {max_time*1000:.2f}ms")
        
        # Performance assessment
        if avg < 0.1:
            print("  Rating:     ✅ Excellent")
        elif avg < 0.5:
            print("  Rating:     ✅ Good")
        elif avg < 1.0:
            print("  Rating:     ⚠ Acceptable")
        else:
            print("  Rating:     ❌ Slow")

print("="*70)
print("API Performance Benchmark")
print("="*70)

# Check server
try:
    requests.get(f"{BASE_URL}/api/health", timeout=2)
except Exception:
    print("❌ Server not running")
    sys.exit(1)

# Benchmark endpoints
benchmark_endpoint("Health Check", f"{BASE_URL}/api/health")
benchmark_endpoint("List Runs (no filter)", f"{BASE_URL}/api/runs?limit=10")
benchmark_endpoint("List Runs (with filter)", f"{BASE_URL}/api/runs?method=LIME&limit=10")
benchmark_endpoint("Root Endpoint", f"{BASE_URL}/")

print("\n" + "="*70)
print("✅ Benchmark Complete")
print("="*70)
