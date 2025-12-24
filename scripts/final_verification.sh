#!/bin/bash

echo "========================================================================"
echo "Final Verification Checklist"
echo "========================================================================"

FAILED=0

check() {
    if eval "$2"; then
        echo "✅ $1"
    else
        echo "❌ $1"
        FAILED=$((FAILED + 1))
    fi
}

# 1. Check automated tests
echo -e "\n1. Automated Tests"
# Using dry-run/quiet mode just to check they run, assuming full run passed earlier
check "Unit tests pass" "pytest src/api/tests/ -m 'not integration' -q --tb=no"
check "Integration tests pass" "pytest src/api/tests/test_integration.py -q --tb=no"

# 2. Check server starts
echo -e "\n2. Server Startup"
# Simple import check
timeout 5 python -c "from src.api.main import app; print('OK')" > /dev/null 2>&1
check "Server imports successfully" "[ $? -eq 0 ]"

# 3. Check sample data
echo -e "\n3. Sample Data"
check "Sample data directory exists" "[ -d experiments/sample_data/results ]"
check "Sample JSON files exist" "[ $(ls experiments/sample_data/results/*.json 2>/dev/null | wc -l) -gt 0 ]"

# 4. Check documentation
echo -e "\n4. Documentation"
check "API README exists" "[ -f src/api/README.md ]"
check "Testing docs exist" "[ -f docs/testing/INTEGRATION_TESTS.md ]"
check "ADR exists" "[ -f docs/adr/001-api-architecture.md ]"

# 5. Check code quality
echo -e "\n5. Code Quality"
check "No syntax errors in routes" "python -m py_compile src/api/routes/*.py"
check "No syntax errors in services" "python -m py_compile src/api/services/*.py"

echo -e "\n========================================================================"
if [ $FAILED -eq 0 ]; then
    echo "✅ All verification checks passed!"
    echo "========================================================================"
    exit 0
else
    echo "❌ $FAILED verification check(s) failed"
    echo "========================================================================"
    exit 1
fi
