#!/bin/bash
# managed_runner_exp3.sh - Resumable EXP3 runner with periodic git checkpointing.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

CONFIG_DIR="${CONFIG_DIR:-configs/experiments/exp3_cross_dataset}"
RESULTS_PATH="${RESULTS_PATH:-experiments/exp3_cross_dataset/results}"
LOG_FILE="${LOG_FILE:-logs/managed_runner_exp3.log}"

PUSH_REMOTE="${PUSH_REMOTE:-origin}"
PUSH_BRANCH="${PUSH_BRANCH:-$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)}"

# Override with VENV_PYTHON if you use a dedicated environment (recommended on Windows/WSL).
if [ -n "${VENV_PYTHON:-}" ]; then
  PYTHON="$VENV_PYTHON"
elif [ -x ".venv/bin/python3" ]; then
  PYTHON=".venv/bin/python3"
elif [ -x ".venv-wsl/bin/python3" ]; then
  PYTHON=".venv-wsl/bin/python3"
else
  PYTHON="python3"
fi

mkdir -p logs
touch "$LOG_FILE"

echo "==========================================================" | tee -a "$LOG_FILE"
echo "EXP3 Managed Runner starting at $(date)" | tee -a "$LOG_FILE"
echo "Python: $PYTHON" | tee -a "$LOG_FILE"
echo "Config dir: $CONFIG_DIR" | tee -a "$LOG_FILE"
echo "Results path: $RESULTS_PATH" | tee -a "$LOG_FILE"
echo "Push target: $PUSH_REMOTE $PUSH_BRANCH" | tee -a "$LOG_FILE"
echo "==========================================================" | tee -a "$LOG_FILE"

# Background checkpoint daemon (commits often; pushes periodically).
# Configure cadence via env vars:
#   INTERVAL=900 PUSH_INTERVAL=3600 bash scripts/auto_push.sh <paths...>
bash scripts/auto_push.sh "$RESULTS_PATH" >> logs/auto_push_exp3.log 2>&1 &
SYNC_PID=$!

cleanup() {
  if [ -n "${SYNC_PID:-}" ]; then
    kill "$SYNC_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT INT TERM

if [ ! -d "$CONFIG_DIR" ]; then
  echo "[ERROR] Missing EXP3 config directory: $CONFIG_DIR" | tee -a "$LOG_FILE"
  exit 1
fi

mapfile -t CONFIGS < <(find "$CONFIG_DIR" -type f -name "*.yaml" ! -name "manifest.yaml" | sort)
if [ "${#CONFIGS[@]}" -eq 0 ]; then
  echo "[ERROR] No EXP3 configs found under $CONFIG_DIR" | tee -a "$LOG_FILE"
  exit 1
fi

read_config_fields() {
  local config_path="$1"
  "$PYTHON" - "$config_path" <<'PY'
import sys
import yaml

path = sys.argv[1]
with open(path, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

name = str(cfg.get("name", ""))
output_dir = str(cfg.get("output_dir", ""))
model_path = str((cfg.get("model") or {}).get("path", ""))
print(name)
print(output_dir)
print(model_path)
PY
}

for CONFIG_PATH in "${CONFIGS[@]}"; do
  mapfile -t FIELDS < <(read_config_fields "$CONFIG_PATH")
  EXP_NAME="${FIELDS[0]:-}"
  OUTPUT_DIR="${FIELDS[1]:-}"
  MODEL_PATH="${FIELDS[2]:-}"

  if [ -z "$EXP_NAME" ] || [ -z "$OUTPUT_DIR" ] || [ -z "$MODEL_PATH" ]; then
    echo "[ERROR] Failed to parse required fields from $CONFIG_PATH" | tee -a "$LOG_FILE"
    continue
  fi

  if [ ! -f "$MODEL_PATH" ]; then
    echo "[ERROR] Missing EXP3 model artifact for $EXP_NAME: $MODEL_PATH" | tee -a "$LOG_FILE"
    echo "        Run: $PYTHON scripts/train_exp3_models.py" | tee -a "$LOG_FILE"
    exit 2
  fi

  if [ -f "$OUTPUT_DIR/results.json" ]; then
    echo "[SKIP] $EXP_NAME already has $OUTPUT_DIR/results.json" | tee -a "$LOG_FILE"
    continue
  fi

  echo "----------------------------------------------------------" | tee -a "$LOG_FILE"
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] Running EXP3: $EXP_NAME" | tee -a "$LOG_FILE"
  echo "Config: $CONFIG_PATH" | tee -a "$LOG_FILE"

  set +e
  $PYTHON -m src.experiment.runner --config "$CONFIG_PATH" 2>&1 | tee -a "$LOG_FILE"
  RUN_STATUS=${PIPESTATUS[0]}
  set -e

  if [ "$RUN_STATUS" -ne 0 ]; then
    echo "[FAILED] $EXP_NAME (exit $RUN_STATUS). Resume by re-running the same config." | tee -a "$LOG_FILE"
    sleep 5
    continue
  fi

  echo "[SUCCESS] Finished $EXP_NAME" | tee -a "$LOG_FILE"

  git add -- "$RESULTS_PATH"
  if git diff --cached --quiet -- "$RESULTS_PATH"; then
    echo "[GIT] No EXP3 result changes to commit for $EXP_NAME." | tee -a "$LOG_FILE"
    continue
  fi

  if git commit -m "EXP3: results for $EXP_NAME" >> "$LOG_FILE" 2>&1; then
    if ! git push --no-progress "$PUSH_REMOTE" "HEAD:$PUSH_BRANCH" >> "$LOG_FILE" 2>&1; then
      echo "[WARN] Push failed; EXP3 results remain committed locally." | tee -a "$LOG_FILE"
    fi
  else
    echo "[WARN] Commit failed for $EXP_NAME (results still staged)." | tee -a "$LOG_FILE"
  fi

  sleep 5
done

echo "==========================================================" | tee -a "$LOG_FILE"
echo "EXP3 Managed Runner finished at $(date)" | tee -a "$LOG_FILE"
echo "==========================================================" | tee -a "$LOG_FILE"
