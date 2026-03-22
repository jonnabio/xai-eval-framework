#!/bin/bash
set -e

# Activate the virtual environment
source .venv/bin/activate

LOG_FILE="logs/exp2_completion_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

echo "Starting EXP2 grid completion..." | tee -a "$LOG_FILE"
echo "Log file: $LOG_FILE"

# Memory threshold in MB (Wait if free memory drops below 2000 MB)
MEM_THRESHOLD=2000

wait_for_memory() {
    while true; do
        # Get available memory in MB
        AVAIL_MEM=$(free -m | awk '/^Mem:/{print $7}')
        if [ "$AVAIL_MEM" -lt "$MEM_THRESHOLD" ]; then
            echo "[WARNING] High memory usage detected ($AVAIL_MEM MB available). Script will SLEEP for 60 seconds to allow the system to recover..." | tee -a "$LOG_FILE"
            sleep 60
        else
            break
        fi
    done
}

run_safe() {
    CMD="$@"
    echo "------------------------------------------------------" | tee -a "$LOG_FILE"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] Starting: $CMD" | tee -a "$LOG_FILE"
    wait_for_memory
    
    # Run the command and append both stdout and stderr to the log file
    eval "$CMD" 2>&1 | tee -a "$LOG_FILE"
    
    # Slight sleep between runs to let kernel free up caches
    sleep 5
}

echo "=================== RESTORING ARTIFACTS ===================" | tee -a "$LOG_FILE"
ROOT="experiments/exp2_scaled/results"
REC="experiments/recovery/phase1/results"
REC_P1="experiments/exp_recov_p1"

# SVM SHAP Recovery
mkdir -p "$ROOT/svm_shap/seed_123/n_50" && cp -n "$REC/svm_shap/seed_123/n_50/results.json" "$ROOT/svm_shap/seed_123/n_50/" || true
mkdir -p "$ROOT/svm_shap/seed_123/n_100" && cp -n "$REC/svm_shap/seed_123/n_100/results.json" "$ROOT/svm_shap/seed_123/n_100/" || true
mkdir -p "$ROOT/svm_shap/seed_123/n_200" && cp -n "$REC/svm_shap/seed_123/n_200/results.json" "$ROOT/svm_shap/seed_123/n_200/" || true
mkdir -p "$ROOT/svm_shap/seed_42/n_50" && cp -n "$REC/svm_shap/seed_42/n_50/results.json" "$ROOT/svm_shap/seed_42/n_50/" || true
mkdir -p "$ROOT/svm_shap/seed_42/n_100" && cp -n "$REC/svm_shap/seed_42/n_100/results.json" "$ROOT/svm_shap/seed_42/n_100/" || true

# MLP SHAP Recovery
mkdir -p "$ROOT/mlp_shap/seed_42/n_50" && cp -n "$REC_P1/mlp_shap/seed_42/n_50/results.json" "$ROOT/mlp_shap/seed_42/n_50/" || true
mkdir -p "$ROOT/mlp_shap/seed_42/n_100" && cp -n "$REC_P1/mlp_shap/seed_42/n_100/results.json" "$ROOT/mlp_shap/seed_42/n_100/" || true
mkdir -p "$ROOT/mlp_shap/seed_456/n_100" && cp -n "$REC_P1/mlp_shap/seed_456/n_100/results.json" "$ROOT/mlp_shap/seed_456/n_100/" || true
mkdir -p "$ROOT/mlp_shap/seed_456/n_200" && cp -n "$REC_P1/mlp_shap/seed_456/n_200/results.json" "$ROOT/mlp_shap/seed_456/n_200/" || true
mkdir -p "$ROOT/mlp_shap/seed_789/n_100" && cp -n "$REC_P1/mlp_shap/seed_789/n_100/results.json" "$ROOT/mlp_shap/seed_789/n_100/" || true
mkdir -p "$ROOT/mlp_shap/seed_999/n_50" && cp -n "$REC_P1/mlp_shap/seed_999/n_50/results.json" "$ROOT/mlp_shap/seed_999/n_50/" || true
echo "Artifacts restored!" | tee -a "$LOG_FILE"

echo "=================== EXECUTING SVM GAPS ===================" | tee -a "$LOG_FILE"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/svm_anchors_s123_n200.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/svm_anchors_s456_n200.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/svm_anchors_s789_n200.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/svm_anchors_s999_n200.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/svm_dice_s42_n50.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/svm_dice_s42_n100.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/svm_dice_s456_n50.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/svm_dice_s456_n100.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/svm_dice_s789_n50.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/svm_dice_s789_n100.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/svm_dice_s999_n50.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/svm_dice_s999_n100.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/svm_dice_s999_n200.yaml"

echo "=================== EXECUTING RF GAPS ===================" | tee -a "$LOG_FILE"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/rf_anchors_s42_n100.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/rf_anchors_s789_n50.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/rf_anchors_s789_n200.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/rf_anchors_s999_n200.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/rf_dice_s123_n200.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/rf_dice_s456_n50.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/rf_dice_s456_n100.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/rf_dice_s789_n50.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/rf_dice_s789_n200.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/rf_dice_s999_n200.yaml"

echo "=================== EXECUTING XGB GAPS ===================" | tee -a "$LOG_FILE"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/xgb_anchors_s123_n50.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/xgb_anchors_s123_n100.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/xgb_anchors_s456_n200.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/xgb_anchors_s999_n50.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/xgb_anchors_s999_n100.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/xgb_dice_s42_n100.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/xgb_dice_s456_n50.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/xgb_dice_s789_n50.yaml"

echo "=================== EXECUTING MLP GAPS ===================" | tee -a "$LOG_FILE"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/mlp_anchors_s42_n50.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/mlp_anchors_s42_n100.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/mlp_anchors_s456_n50.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/mlp_anchors_s456_n100.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/mlp_anchors_s789_n50.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/mlp_anchors_s789_n200.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/mlp_dice_s42_n50.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/mlp_dice_s42_n100.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/mlp_dice_s123_n100.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/mlp_dice_s789_n100.yaml"

echo "=================== EXECUTING LOGREG GAPS ===================" | tee -a "$LOG_FILE"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/logreg_dice_s789_n100.yaml"
run_safe "python -m src.experiment.runner --config configs/experiments/exp2_scaled/logreg_dice_s999_n100.yaml"

echo "=================== FINAL AGGREGATION ===================" | tee -a "$LOG_FILE"
run_safe "python scripts/generate_paper_a_figures.py"

echo "ALL EXP2 EXPERIMENTS COMPLETED!" | tee -a "$LOG_FILE"
