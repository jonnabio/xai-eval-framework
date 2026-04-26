#!/usr/bin/env bash
# Launch the EXP3 Linux/WSL console dashboard with sensible defaults.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

PYTHON_BIN="${PYTHON_BIN:-}"
INTERVAL="${INTERVAL:-5}"
CONFIG_DIR="${CONFIG_DIR:-configs/experiments/exp3_cross_dataset}"
RESULTS_DIR="${RESULTS_DIR:-experiments/exp3_cross_dataset/results}"
LOG_FILE="${LOG_FILE:-logs/exp3_linux_german_credit.log}"

if [[ -z "$PYTHON_BIN" ]]; then
  if [[ -x ".venv-wsl/bin/python3" ]]; then
    PYTHON_BIN=".venv-wsl/bin/python3"
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
  else
    echo "[ERROR] Could not find a Python interpreter." >&2
    echo "        Recommended: bash scripts/setup_venv_wsl.sh" >&2
    exit 1
  fi
fi

mkdir -p logs

echo "=========================================================="
echo "EXP3 Linux Console Dashboard"
echo "Project root: $PROJECT_ROOT"
echo "Python: $PYTHON_BIN"
echo "Config dir: $CONFIG_DIR"
echo "Results dir: $RESULTS_DIR"
echo "Log file: $LOG_FILE"
echo "Refresh interval: ${INTERVAL}s"
echo "=========================================================="

exec "$PYTHON_BIN" scripts/status_dashboard.py \
  --interval "$INTERVAL" \
  --config-dir "$CONFIG_DIR" \
  --results-dir "$RESULTS_DIR" \
  --log-file "$LOG_FILE" \
  "$@"
