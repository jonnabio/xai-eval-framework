#!/bin/bash
# managed_runner.sh - Automated experiment runner with resource safeguards and Git commits.

# Configurations
VENV_PYTHON=".venv/bin/python3"
CONFIG_DIR="configs/experiments/exp2_scaled"
LOG_FILE="logs/managed_runner.log"
MAX_LOAD=10.0
MIN_MEM=2000
REPO_DIR=$(pwd)

mkdir -p logs
touch "$LOG_FILE"

echo "==========================================================" | tee -a "$LOG_FILE"
echo "Starting Managed Experiment Runner at $(date)" | tee -a "$LOG_FILE"
echo "Max CPU Load: $MAX_LOAD | Min Free Mem: $MIN_MEM MB" | tee -a "$LOG_FILE"
echo "==========================================================" | tee -a "$LOG_FILE"

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
    
    wait_for_resources
    
    # Run the experiment
    # We use source .venv/bin/activate implicitly by using $VENV_PYTHON
    $VENV_PYTHON -m src.experiment.runner --config "$CONFIG_PATH" 2>&1 | tee -a "$LOG_FILE"
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo "[SUCCESS] Finished $EXP_NAME" | tee -a "$LOG_FILE"
        
        # Automatic Git Commit
        echo "[GIT] Committing results for $EXP_NAME" | tee -a "$LOG_FILE"
        git add experiments/exp2_scaled/results/
        git commit -m "Auto-commit: Results for $EXP_NAME"
        git push origin $(git rev-parse --abbrev-ref HEAD)
    else
        echo "[FAILED] Experiment $EXP_NAME failed. Check logs." | tee -a "$LOG_FILE"
    fi
    
    # Cooldown
    sleep 5
done

echo "==========================================================" | tee -a "$LOG_FILE"
echo "Managed Runner finished at $(date)" | tee -a "$LOG_FILE"
echo "==========================================================" | tee -a "$LOG_FILE"
