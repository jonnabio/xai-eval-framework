@echo off
echo ========================================================================
echo XAI Evaluation API - Complete Test Suite
echo ========================================================================

echo.
echo 1. Running Unit Tests
echo ------------------------------------------------------------------------
python -m pytest src/api/tests/ -v -m "not integration" --tb=short
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo 2. Running Integration Tests
echo ------------------------------------------------------------------------
python -m pytest src/api/tests/test_integration.py -v -m integration --tb=short
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo 3. Running All Tests with Coverage
echo ------------------------------------------------------------------------
python -m pytest src/api/tests/ --cov=src/api --cov-report=term-missing --cov-report=html
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo 4. Test Summary
echo ------------------------------------------------------------------------
python -m pytest src/api/tests/ --tb=no -q

echo.
echo ========================================================================
echo ✅ All Tests Passed!
echo ========================================================================
echo.
echo Coverage report generated: htmlcov/index.html
echo.
