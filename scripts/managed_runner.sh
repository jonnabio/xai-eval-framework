#!/bin/bash
# managed_runner.sh - Automated experiment runner with resource safeguards and Git commits.

# Configurations
VENV_PYTHON=".venv/bin/python3"
CONFIG_DIR="configs/experiments/exp2_scaled"
LOG_FILE="logs/managed_runner.log"
RESULTS_PATH="experiments/exp2_scaled/results"
CLAIM_ROOT="experiments/exp2_scaled/worker_claims"
LOCK_FILE="${LOCK_FILE:-.git/xai_git_sync.lock}"
LOCK_WAIT_SECONDS="${LOCK_WAIT_SECONDS:-300}"
MAX_LOAD=10.0
MIN_MEM="${MIN_MEM:-4200}"
REPO_DIR=$(pwd)
CURRENT_GIT_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
if [ -n "${XAI_WORKER_ID:-}" ]; then
    WORKER_ID="$XAI_WORKER_ID"
elif [[ "$CURRENT_GIT_BRANCH" == results/* ]]; then
    WORKER_ID="${CURRENT_GIT_BRANCH#results/}"
else
    WORKER_ID="$(hostname | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9._-]/-/g; s/^-*//; s/-*$//')"
fi
RESULTS_BRANCH="${XAI_RESULTS_BRANCH:-${CURRENT_GIT_BRANCH:-results/$WORKER_ID}}"

mkdir -p logs
touch "$LOG_FILE"

LOCK_FD=0
if command -v flock >/dev/null 2>&1; then
    # shellcheck disable=SC2094
    exec {LOCK_FD}>"$LOCK_FILE"
fi

echo "==========================================================" | tee -a "$LOG_FILE"
echo "Starting Managed Experiment Runner at $(date)" | tee -a "$LOG_FILE"
echo "Max CPU Load: $MAX_LOAD | Min Free Mem: $MIN_MEM MB" | tee -a "$LOG_FILE"
echo "==========================================================" | tee -a "$LOG_FILE"

# Start background sync daemon
bash scripts/auto_push.sh >> logs/auto_push.log 2>&1 &
SYNC_PID=$!
echo "Started background Git sync daemon (PID: $SYNC_PID)" | tee -a "$LOG_FILE"

# Function to check resources
wait_for_resources() {
    while true; do
        # Check Memory
        FREE_MEM=$(free -m | awk '/^Mem:/{print $7}')
        
        # Check CPU Load (1-minute average)
        LOAD_1MIN=$(uptime | awk -F'load average:' '{ print $2 }' | awk -F',' '{ print $1 }' | xargs)
        
        LOAD_INT=$(echo "$LOAD_1MIN > $MAX_LOAD" | bc -l)
        MEM_INT=$(echo "$FREE_MEM < $MIN_MEM" | bc -l)

        if [ "$LOAD_INT" -eq 1 ]; then
            echo "[WAIT] High CPU Load ($LOAD_1MIN). Sleeping 30s..." | tee -a "$LOG_FILE"
            sleep 30
        elif [ "$MEM_INT" -eq 1 ]; then
            echo "[WAIT] Low Free Memory ($FREE_MEM MB). Sleeping 30s..." | tee -a "$LOG_FILE"
            sleep 30
        else
            break
        fi
    done
}

claim_experiment() {
    local exp_name="$1"
    local config_path="$2"
    local output_dir="$3"
    local results_file="$output_dir/results.json"
    local claim_path="$CLAIM_ROOT/$exp_name.json"

    if ! git fetch --no-progress origin main >> "$LOG_FILE" 2>&1; then
        echo "[CLAIM] Could not fetch origin/main before claiming $exp_name. Will retry later." | tee -a "$LOG_FILE"
        return 2
    fi

    local base_commit
    base_commit=$(git rev-parse origin/main 2>>"$LOG_FILE") || return 2

    if git cat-file -e "$base_commit:$results_file" 2>/dev/null; then
        echo "[CLAIM] $exp_name already has results.json on origin/main. Skipping." | tee -a "$LOG_FILE"
        return 1
    fi

    if git cat-file -e "$base_commit:$claim_path" 2>/dev/null; then
        local claim_worker
        claim_worker=$(git show "$base_commit:$claim_path" 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin).get("worker_id",""))' 2>/dev/null || true)
        if [ "$claim_worker" = "$WORKER_ID" ]; then
            echo "[CLAIM] Reusing existing claim for $exp_name owned by this worker." | tee -a "$LOG_FILE"
            return 0
        fi
        echo "[CLAIM] $exp_name is already claimed by worker ${claim_worker:-unknown}; skipping." | tee -a "$LOG_FILE"
        return 1
    fi

    local tmp_index tmp_claim tmp_msg blob tree claim_commit
    tmp_index=$(mktemp)
    tmp_claim=$(mktemp)
    tmp_msg=$(mktemp)
    python3 - "$exp_name" "$WORKER_ID" "$RESULTS_BRANCH" "$config_path" "$output_dir" "$base_commit" > "$tmp_claim" <<'PY'
import json
import socket
import sys
from datetime import datetime, timezone

exp_name, worker_id, branch, config_path, output_dir, base_commit = sys.argv[1:]
print(json.dumps({
    "experiment_name": exp_name,
    "worker_id": worker_id,
    "host": socket.gethostname(),
    "results_branch": branch,
    "config_path": config_path.replace("\\", "/"),
    "output_dir": output_dir.replace("\\", "/"),
    "claimed_at": datetime.now(timezone.utc).isoformat(),
    "base_main_commit": base_commit,
    "claim_version": 1,
}, indent=2))
PY

    blob=$(git hash-object -w "$tmp_claim") || {
        rm -f "$tmp_index" "$tmp_claim" "$tmp_msg"
        return 2
    }
    GIT_INDEX_FILE="$tmp_index" git read-tree "$base_commit" || {
        rm -f "$tmp_index" "$tmp_claim" "$tmp_msg"
        return 2
    }
    GIT_INDEX_FILE="$tmp_index" git update-index --add --cacheinfo "100644,$blob,$claim_path" || {
        rm -f "$tmp_index" "$tmp_claim" "$tmp_msg"
        return 2
    }
    tree=$(GIT_INDEX_FILE="$tmp_index" git write-tree) || {
        rm -f "$tmp_index" "$tmp_claim" "$tmp_msg"
        return 2
    }
    {
        printf 'Claim experiment %s for %s\n\n' "$exp_name" "$WORKER_ID"
        printf 'Reserve %s before running so other workstations skip it.\n' "$exp_name"
    } > "$tmp_msg"
    claim_commit=$(GIT_AUTHOR_NAME='jonna' GIT_AUTHOR_EMAIL='jonna@users.noreply.github.com' GIT_COMMITTER_NAME='jonna' GIT_COMMITTER_EMAIL='jonna@users.noreply.github.com' git commit-tree "$tree" -p "$base_commit" -F "$tmp_msg") || {
        rm -f "$tmp_index" "$tmp_claim" "$tmp_msg"
        return 2
    }
    rm -f "$tmp_index" "$tmp_claim" "$tmp_msg"

    if git push --no-progress origin "$claim_commit:refs/heads/main" >> "$LOG_FILE" 2>&1; then
        echo "[CLAIM] Claimed $exp_name on main with commit $claim_commit." | tee -a "$LOG_FILE"
        git fetch --no-progress origin main >> "$LOG_FILE" 2>&1 || true
        return 0
    fi

    echo "[CLAIM] Claim push for $exp_name was rejected, likely because another worker updated main. Skipping this pass." | tee -a "$LOG_FILE"
    git fetch --no-progress origin main >> "$LOG_FILE" 2>&1 || true
    return 2
}

# Get list of missing experiments
MISSING_LIST=$($VENV_PYTHON scripts/check_missing_results.py | tail -n +2)


for EXP_NAME in $MISSING_LIST; do
    CONFIG_PATH="$CONFIG_DIR/$EXP_NAME.yaml"
    
    if [ ! -f "$CONFIG_PATH" ]; then
        echo "[ERROR] Config not found: $CONFIG_PATH" | tee -a "$LOG_FILE"
        continue
    fi

    echo "----------------------------------------------------------" | tee -a "$LOG_FILE"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] Starting experiment: $EXP_NAME" | tee -a "$LOG_FILE"

    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    if [ -z "$CURRENT_BRANCH" ]; then
        echo "[ERROR] Failed to resolve current branch. Skipping $EXP_NAME." | tee -a "$LOG_FILE"
        continue
    fi

    echo "[GIT] Fetching latest queue state for $RESULTS_PATH..." | tee -a "$LOG_FILE"
    if git fetch --no-progress origin "$CURRENT_BRANCH" >> "$LOG_FILE" 2>&1; then
        if ! git diff --quiet HEAD "origin/$CURRENT_BRANCH" -- "$RESULTS_PATH"; then
            if git restore --source "origin/$CURRENT_BRANCH" --staged --worktree -- "$RESULTS_PATH" >> "$LOG_FILE" 2>&1; then
                echo "[GIT] Updated local result queue from origin/$CURRENT_BRANCH." | tee -a "$LOG_FILE"
            else
                echo "[WARN] Failed to refresh $RESULTS_PATH from origin/$CURRENT_BRANCH." | tee -a "$LOG_FILE"
            fi
        else
            echo "[GIT] Local result queue already matches origin/$CURRENT_BRANCH." | tee -a "$LOG_FILE"
        fi
    else
        echo "[WARN] Fetch failed; continuing with local queue state." | tee -a "$LOG_FILE"
    fi

    OUTPUT_DIR=$(awk -F: '/^[[:space:]]*output_dir[[:space:]]*:/ {gsub(/^[ \t'\''"]+|[ \t'\''"]+$/, "", $2); print $2; exit}' "$CONFIG_PATH")
    if [ -n "$OUTPUT_DIR" ] && [ -f "$OUTPUT_DIR/results.json" ]; then
        echo "[SKIP] $EXP_NAME already exists locally after queue refresh." | tee -a "$LOG_FILE"
        continue
    fi

    claim_experiment "$EXP_NAME" "$CONFIG_PATH" "$OUTPUT_DIR"
    CLAIM_STATUS=$?
    if [ "$CLAIM_STATUS" -ne 0 ]; then
        echo "[SKIP] $EXP_NAME was not claimed by this worker. Selecting another experiment." | tee -a "$LOG_FILE"
        sleep 5
        continue
    fi
    
    wait_for_resources
    
    # Run the experiment
    # We use source .venv/bin/activate implicitly by using $VENV_PYTHON
    $VENV_PYTHON -m src.experiment.runner --config "$CONFIG_PATH" 2>&1 | tee -a "$LOG_FILE"
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo "[SUCCESS] Finished $EXP_NAME" | tee -a "$LOG_FILE"
        
        # Automatic Git Commit
        echo "[GIT] Committing results for $EXP_NAME" | tee -a "$LOG_FILE"
        if [ "$LOCK_FD" -ne 0 ]; then
            if ! flock -w "$LOCK_WAIT_SECONDS" "$LOCK_FD"; then
                echo "[WARN] Could not acquire git lock; skipping commit/push for $EXP_NAME." | tee -a "$LOG_FILE"
                sleep 5
                continue
            fi
        fi
        git add -- "$RESULTS_PATH"
        if [ -n "$(git status --porcelain -- "$RESULTS_PATH")" ]; then
            if git commit -m "Auto-commit: Results for $EXP_NAME"; then
                if ! git push origin "HEAD:$CURRENT_BRANCH"; then
                    echo "[WARN] Push failed for $EXP_NAME; results remain committed locally." | tee -a "$LOG_FILE"
                fi
            else
                echo "[WARN] Commit failed for $EXP_NAME." | tee -a "$LOG_FILE"
            fi
        else
            echo "[GIT] No new result changes detected for $EXP_NAME." | tee -a "$LOG_FILE"
        fi
        if [ "$LOCK_FD" -ne 0 ]; then flock -u "$LOCK_FD" || true; fi
    else
        echo "[FAILED] Experiment $EXP_NAME failed. Check logs." | tee -a "$LOG_FILE"
    fi
    
    # Cooldown
    sleep 5
done

echo "==========================================================" | tee -a "$LOG_FILE"
echo "Managed Runner finished at $(date)" | tee -a "$LOG_FILE"
echo "==========================================================" | tee -a "$LOG_FILE"

# Cleanup sync process
if [ -n "$SYNC_PID" ]; then
    kill $SYNC_PID
    echo "Stopped background Git sync daemon."
fi
