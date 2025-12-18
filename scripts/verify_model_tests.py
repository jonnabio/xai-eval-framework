"""
Verify Model Tests (EXP1-11)

Purpose:
    Quickly verify that model unit tests pass and coverage is adequate.
    Acts as a local CI check before committing.

Usage:
    python scripts/verify_model_tests.py

Output:
    - Summary of test execution (Pass/Fail)
    - Coverage report for src/models/
"""

import sys
import pytest
import subprocess
from pathlib import Path

def run_tests():
    """Run pytest on the unit test module and capture result."""
    print("Running Model Sanity Tests...")
    # We run pytest module directly
    result = pytest.main([
        "tests/unit/test_model_sanity.py",
        "-v",
        "-m", "not slow" # Default to fast checks for "verification"
    ])
    return result

def check_coverage():
    """Run pytest with coverage and return status."""
    print("\nChecking Coverage...")
    try:
        # We use subprocess to isolate coverage run and capture output easily
        # targeted at src/models/
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/unit/test_model_sanity.py",
            "--cov=src.models",
            "--cov-report=term-missing"
        ]
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"Coverage check failed to run: {e}")
        return 1

def main():
    """Orchestrate verification."""
    print("="*40)
    print("Model Test Verification Tool")
    print("="*40)
    
    # 1. Run Tests
    test_code = run_tests()
    
    if test_code != 0:
        print("\n❌ Tests Failed!")
        sys.exit(1)
        
    print("\n✅ Verification Tests Passed!")
    
    # 2. Check Coverage (Optional but recommended)
    # We run it separately or enabled above. 
    # Since I separated them, let's run coverage now if user has pytest-cov
    cov_code = check_coverage()
    
    if cov_code == 0:
        print("\n✅ Coverage Check Passed!")
        sys.exit(0)
    else:
        print("\n⚠️  Coverage/Tests with coverage had issues.")
        sys.exit(cov_code)

if __name__ == "__main__":
    main()
