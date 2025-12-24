"""
Comprehensive manual API testing script.

Tests all endpoints with various scenarios and edge cases.
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any
import time

BASE_URL = "http://127.0.0.1:8000"

class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

class TestResult:
    """Track test results."""
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.errors = []
    
    def record_pass(self, test_name: str):
        self.total += 1
        self.passed += 1
        print(f"{Colors.GREEN}✓{Colors.RESET} {test_name}")
    
    def record_fail(self, test_name: str, error: str):
        self.total += 1
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"{Colors.RED}✗{Colors.RESET} {test_name}: {error}")
    
    def record_warning(self, test_name: str, warning: str):
        self.warnings += 1
        print(f"{Colors.YELLOW}⚠{Colors.RESET} {test_name}: {warning}")
    
    def print_summary(self):
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"Total tests: {self.total}")
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {self.failed}{Colors.RESET}")
        print(f"{Colors.YELLOW}Warnings: {self.warnings}{Colors.RESET}")
        
        if self.errors:
            print("\nFailed Tests:")
            for test_name, error in self.errors:
                print(f"  - {test_name}: {error}")
        
        print("="*70)
        
        if self.failed > 0:
            sys.exit(1)

results = TestResult()

def test_section(title: str):
    """Print section header."""
    print(f"\n{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BLUE}{title}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*70}{Colors.RESET}")

def test_health_endpoints():
    """Test health check endpoints."""
    test_section("1. Health Check Endpoints")
    
    # Test 1.1: Basic health check
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                results.record_pass("Health check returns healthy status")
            else:
                results.record_fail("Health check", f"Status not healthy: {data.get('status')}")
        else:
            results.record_fail("Health check", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Health check", str(e))
    
    # Test 1.2: Detailed health check
    try:
        response = requests.get(f"{BASE_URL}/api/health/detailed", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "system" in data:
                results.record_pass("Detailed health includes system info")
            else:
                results.record_fail("Detailed health", "Missing system info")
        else:
            results.record_fail("Detailed health", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Detailed health", str(e))

def test_root_endpoint():
    """Test root endpoint."""
    test_section("2. Root Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            required_fields = ["name", "version", "status", "endpoints"]
            missing = [f for f in required_fields if f not in data]
            if not missing:
                results.record_pass("Root endpoint returns complete info")
            else:
                results.record_fail("Root endpoint", f"Missing fields: {missing}")
        else:
            results.record_fail("Root endpoint", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Root endpoint", str(e))

def test_documentation_endpoints():
    """Test API documentation endpoints."""
    test_section("3. Documentation Endpoints")
    
    # Test 3.1: Swagger UI
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            results.record_pass("Swagger UI accessible")
        else:
            results.record_fail("Swagger UI", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Swagger UI", str(e))
    
    # Test 3.2: ReDoc
    try:
        response = requests.get(f"{BASE_URL}/redoc", timeout=5)
        if response.status_code == 200:
            results.record_pass("ReDoc accessible")
        else:
            results.record_fail("ReDoc", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("ReDoc", str(e))
    
    # Test 3.3: OpenAPI JSON
    try:
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "openapi" in data and "info" in data:
                results.record_pass("OpenAPI schema valid")
            else:
                results.record_fail("OpenAPI schema", "Invalid structure")
        else:
            results.record_fail("OpenAPI schema", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("OpenAPI schema", str(e))

def test_list_runs_endpoint():
    """Test /api/runs endpoint."""
    test_section("4. List Runs Endpoint")
    
    # Test 4.1: Basic list
    try:
        response = requests.get(f"{BASE_URL}/api/runs", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and "pagination" in data:
                results.record_pass("List runs returns valid structure")
                
                # Store count for later tests
                total_runs = data["pagination"]["total"]
                print(f"  Total runs available: {total_runs}")
            else:
                results.record_fail("List runs", "Invalid response structure")
        else:
            results.record_fail("List runs", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("List runs", str(e))
    
    # Test 4.2: Pagination - limit
    try:
        response = requests.get(f"{BASE_URL}/api/runs?limit=2", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if len(data["data"]) <= 2:
                results.record_pass("Pagination limit works correctly")
            else:
                results.record_fail("Pagination limit", f"Returned {len(data['data'])} items")
        else:
            results.record_fail("Pagination limit", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Pagination limit", str(e))
    
    # Test 4.3: Pagination - offset
    try:
        response1 = requests.get(f"{BASE_URL}/api/runs?limit=1&offset=0", timeout=10)
        response2 = requests.get(f"{BASE_URL}/api/runs?limit=1&offset=1", timeout=10)
        
        if response1.status_code == 200 and response2.status_code == 200:
            data1 = response1.json()
            data2 = response2.json()
            
            if len(data1["data"]) > 0 and len(data2["data"]) > 0:
                if data1["data"][0]["id"] != data2["data"][0]["id"]:
                    results.record_pass("Pagination offset works correctly")
                else:
                    results.record_fail("Pagination offset", "Same run returned")
            else:
                results.record_warning("Pagination offset", "Not enough data to test")
        else:
            results.record_fail("Pagination offset", "Request failed")
    except Exception as e:
        results.record_fail("Pagination offset", str(e))

def test_filtering():
    """Test filtering functionality."""
    test_section("5. Filtering")
    
    # Test 5.1: Filter by method=LIME
    try:
        response = requests.get(f"{BASE_URL}/api/runs?method=LIME", timeout=10)
        if response.status_code == 200:
            data = response.json()
            all_lime = all(run["method"] == "LIME" for run in data["data"])
            if all_lime:
                results.record_pass("Filter by method=LIME works")
            else:
                results.record_fail("Filter by method", "Non-LIME runs returned")
        else:
            results.record_fail("Filter by method", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Filter by method", str(e))
    
    # Test 5.2: Filter by method=SHAP
    try:
        response = requests.get(f"{BASE_URL}/api/runs?method=SHAP", timeout=10)
        if response.status_code == 200:
            data = response.json()
            all_shap = all(run["method"] == "SHAP" for run in data["data"])
            if all_shap:
                results.record_pass("Filter by method=SHAP works")
            else:
                results.record_fail("Filter by method SHAP", "Non-SHAP runs returned")
        else:
            results.record_fail("Filter by method SHAP", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Filter by method SHAP", str(e))
    
    # Test 5.3: Filter by dataset
    try:
        response = requests.get(f"{BASE_URL}/api/runs?dataset=AdultIncome", timeout=10)
        if response.status_code == 200:
            data = response.json()
            all_adult = all(run["dataset"] == "AdultIncome" for run in data["data"])
            if all_adult:
                results.record_pass("Filter by dataset works")
            else:
                results.record_fail("Filter by dataset", "Wrong dataset returned")
        else:
            results.record_fail("Filter by dataset", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Filter by dataset", str(e))
    
    # Test 5.4: Multiple filters
    try:
        response = requests.get(
            f"{BASE_URL}/api/runs?dataset=AdultIncome&method=LIME",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            all_match = all(
                run["dataset"] == "AdultIncome" and run["method"] == "LIME"
                for run in data["data"]
            )
            if all_match:
                results.record_pass("Multiple filters work correctly")
            else:
                results.record_fail("Multiple filters", "Filter not applied correctly")
        else:
            results.record_fail("Multiple filters", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Multiple filters", str(e))

def test_single_run_endpoint():
    """Test /api/runs/{id} endpoint."""
    test_section("6. Single Run Endpoint")
    
    # Get a valid run ID first
    try:
        list_response = requests.get(f"{BASE_URL}/api/runs?limit=1", timeout=10)
        if list_response.status_code != 200:
            results.record_fail("Get run ID", "Could not fetch run list")
            return
        
        list_data = list_response.json()
        if len(list_data["data"]) == 0:
            results.record_warning("Single run test", "No runs available")
            return
        
        run_id = list_data["data"][0]["id"]
        
        # Test 6.1: Get valid run
        response = requests.get(f"{BASE_URL}/api/runs/{run_id}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data["data"]["id"] == run_id:
                results.record_pass("Get single run by ID works")
            else:
                results.record_fail("Get single run", "Wrong run returned")
        else:
            results.record_fail("Get single run", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Get single run", str(e))
    
    # Test 6.2: Get non-existent run (404)
    try:
        response = requests.get(
            f"{BASE_URL}/api/runs/nonexistent_id_xyz_123",
            timeout=10
        )
        if response.status_code == 404:
            results.record_pass("Non-existent run returns 404")
        else:
            results.record_fail("Non-existent run", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Non-existent run", str(e))

def test_error_handling():
    """Test error handling."""
    test_section("7. Error Handling")
    
    # Test 7.1: Invalid limit (too low)
    try:
        response = requests.get(f"{BASE_URL}/api/runs?limit=0", timeout=10)
        if response.status_code == 400: # Custom handler uses 400
            results.record_pass("Invalid limit (0) returns 400")
        else:
            # Also accept 422 if standard handler catches it first
            if response.status_code == 422:
                 results.record_pass("Invalid limit (0) returns 422")
            else:
                 results.record_fail("Invalid limit low", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Invalid limit low", str(e))
    
    # Test 7.2: Invalid limit (too high)
    try:
        response = requests.get(f"{BASE_URL}/api/runs?limit=1000", timeout=10)
        if response.status_code == 400: # Custom handler uses 400
            results.record_pass("Invalid limit (1000) returns 400")
        else:
            if response.status_code == 422:
                 results.record_pass("Invalid limit (1000) returns 422")
            else:
                 results.record_fail("Invalid limit high", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Invalid limit high", str(e))
    
    # Test 7.3: Negative offset
    try:
        response = requests.get(f"{BASE_URL}/api/runs?offset=-1", timeout=10)
        if response.status_code == 400: # Custom handler uses 400
            results.record_pass("Negative offset returns 400")
        else:
            if response.status_code == 422:
                 results.record_pass("Negative offset returns 422")
            else:
                 results.record_fail("Negative offset", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Negative offset", str(e))
    
    # Test 7.4: Non-existent endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/nonexistent", timeout=10)
        if response.status_code == 404:
            results.record_pass("Non-existent endpoint returns 404")
        else:
            results.record_fail("Non-existent endpoint", f"Status code: {response.status_code}")
    except Exception as e:
        results.record_fail("Non-existent endpoint", str(e))

def test_cors():
    """Test CORS headers."""
    test_section("8. CORS Headers")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/health",
            headers={"Origin": "http://localhost:3000"},
            timeout=5
        )
        
        if "access-control-allow-origin" in response.headers:
            origin = response.headers["access-control-allow-origin"]
            if origin == "http://localhost:3000":
                results.record_pass("CORS headers present and correct")
            else:
                results.record_warning("CORS headers", f"Origin: {origin}")
        else:
            results.record_fail("CORS headers", "Headers not present")
    except Exception as e:
        results.record_fail("CORS headers", str(e))

def test_performance():
    """Test response times."""
    test_section("9. Performance")
    
    # Test 9.1: Health check speed
    try:
        start = time.time()
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            if elapsed < 0.5:
                results.record_pass(f"Health check fast ({elapsed:.3f}s)")
            elif elapsed < 1.0:
                results.record_warning("Health check", f"Slow: {elapsed:.3f}s")
            else:
                results.record_fail("Health check speed", f"Too slow: {elapsed:.3f}s")
    except Exception as e:
        results.record_fail("Health check speed", str(e))
    
    # Test 9.2: List runs speed
    try:
        start = time.time()
        response = requests.get(f"{BASE_URL}/api/runs?limit=10", timeout=10)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            if elapsed < 2.0:
                results.record_pass(f"List runs fast ({elapsed:.3f}s)")
            elif elapsed < 5.0:
                results.record_warning("List runs", f"Slow: {elapsed:.3f}s")
            else:
                results.record_fail("List runs speed", f"Too slow: {elapsed:.3f}s")
    except Exception as e:
        results.record_fail("List runs speed", str(e))

def main():
    """Run all tests."""
    print(f"{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BLUE}XAI Evaluation API - Manual E2E Tests{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"Base URL: {BASE_URL}")
    print(f"Started: {datetime.now().isoformat()}")
    
    # Check if server is running
    try:
        # Retry logic for server startup
        connected = False
        for i in range(5):
            try:
                response = requests.get(f"{BASE_URL}/api/health", timeout=2)
                connected = True
                break
            except Exception:
                time.sleep(1)
        
        if connected:
            print(f"{Colors.GREEN}✓ Server is running{Colors.RESET}")
        else:
             raise Exception("Server unavailable")
    except Exception:
        print(f"{Colors.RED}✗ Server is not running at {BASE_URL}{Colors.RESET}")
        print("Please start the server with: python -m src.api.main")
        sys.exit(1)
    
    # Run all test sections
    test_health_endpoints()
    test_root_endpoint()
    test_documentation_endpoints()
    test_list_runs_endpoint()
    test_filtering()
    test_single_run_endpoint()
    test_error_handling()
    test_cors()
    test_performance()
    
    # Print summary
    results.print_summary()

if __name__ == "__main__":
    main()
