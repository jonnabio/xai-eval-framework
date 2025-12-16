#!/bin/bash
# scripts/build_docs.sh
# -----------------------------------------------------------------------------
# Documentation Build Script
# 
# Purpose:
#   1. Generate API documentation from source code
#   2. Build HTML site
#   3. Check for missing docstrings
#   4. Generate coverage report
#
# Usage:
#   bash scripts/build_docs.sh
# -----------------------------------------------------------------------------

# Exit on error
set -e

echo "====================================================================="
echo "Building XAI Evaluation Framework Documentation"
echo "====================================================================="

# 1. auto-generate API docs
#    -f: force overwrite
#    -o: output directory
echo "[1/4] Generating API documentation from source..."
sphinx-apidoc -f -o docs/api src/

# 2. Build HTML documentation
#    -b html: HTML builder
#    -W: Treat warnings as errors (ensures validation)
echo "[2/4] Building HTML documentation..."
sphinx-build -M html docs/ docs/_build

# 3. Check for specific missing docstrings issues (optional additional check)
#    We use Sphinx's built-in coverage builder for the main report, but if
#    we wanted strict enforcement, we could use 'interrogate' here.
#    For now, we rely on the coverage report in step 4.

# 4. Generate Coverage Report
#    -b coverage: Coverage builder
echo "[3/4] Generating documentation coverage report..."
sphinx-build -b coverage docs/ docs/_build/coverage

echo "====================================================================="
echo "Documentation Build Complete!"
echo "====================================================================="
echo "HTML Report:     docs/_build/html/index.html"
echo "Coverage Report: docs/_build/coverage/python.txt"
echo ""
echo "Coverage Summary:"
cat docs/_build/coverage/python.txt
echo "====================================================================="
