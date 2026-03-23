#!/bin/bash
# scripts/status.sh - Quick experiment status check for EXP2

# Configuration
CONFIG_DIR="configs/experiments/exp2_scaled"
RESULTS_ROOT="experiments/exp2_scaled/results"
PYTHON_VENV=".venv/bin/python3"

echo "=========================================================="
echo "          EXP2 GRID COMPLETION STATUS SUMMARY             "
echo "=========================================================="
echo "Current Time: $(date)"

# Count files
TOTAL=$(find "$CONFIG_DIR" -maxdepth 1 -name "*.yaml" | grep -v "manifest" | wc -l)
FINISHED=$(find "$RESULTS_ROOT" -name "results.json" | wc -l)
PENDING=$(($TOTAL - $FINISHED))

# Percentage
if [ "$TOTAL" -gt 0 ]; then
    PERCENT=$(echo "scale=2; ($FINISHED / $TOTAL) * 100" | bc)
    echo "Progress: $FINISHED / $TOTAL finished ($PERCENT%)"
else
    echo "No configs found in $CONFIG_DIR"
fi

# Instance-level checkpointing check (for the currently running work)
CURRENT_RES_DIR=$(ls -dt experiments/exp2_scaled/results/*/*/*/instances 2>/dev/null | head -n 1)
if [ -d "$CURRENT_RES_DIR" ]; then
    INST_COUNT=$(ls -1 "$CURRENT_RES_DIR" | wc -l)
    EXP_NAME=$(echo "$CURRENT_RES_DIR" | rev | cut -d'/' -f 2,3,4,5 | rev)
    echo "----------------------------------------------------------"
    echo "Current Active Progress: $EXP_NAME"
    echo "Instances Completed: $INST_COUNT / 800"
fi

echo "----------------------------------------------------------"
echo "Recently Completed:"
find "$RESULTS_ROOT" -name "results.json" -printf "%T@ %p\n" | sort -nr | head -n 5 | \
    while read -r time path; do
        echo "[$(date -d @$time '+%Y-%m-%d %H:%M:%S')] $(echo $path | rev | cut -d'/' -f 2 | rev)"
    done

echo "=========================================================="
echo "Run 'tail -f logs/managed_runner.log' for live output"
echo "=========================================================="
