#!/usr/bin/env bash
set -u

# Restart managed runner when results become stale.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

RESULTS_ROOT="${RESULTS_ROOT:-$REPO_DIR/experiments/exp2_scaled/results}"
LOG_FILE="${LOG_FILE:-$REPO_DIR/logs/watchdog.log}"
SERVICE_NAME="${SERVICE_NAME:-xai-managed-runner.service}"
STALE_SECONDS="${STALE_SECONDS:-5400}"
ENABLE_WATCHDOG_EMAIL="${ENABLE_WATCHDOG_EMAIL:-0}"
ALERT_EMAIL="${ALERT_EMAIL:-}"
PYTHON_BIN="${PYTHON_BIN:-$REPO_DIR/.venv/bin/python3}"

mkdir -p "$(dirname "$LOG_FILE")"
touch "$LOG_FILE"

log() {
    printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" | tee -a "$LOG_FILE"
}

send_restart_alert() {
    if [ "$ENABLE_WATCHDOG_EMAIL" != "1" ]; then
        return 0
    fi

    if [ ! -x "$PYTHON_BIN" ] || [ ! -f "$REPO_DIR/scripts/email_report.py" ]; then
        log "[WARN] Email alert requested but notifier is unavailable."
        return 0
    fi

    local subject="[XAI Watchdog] Runner Restarted"
    local body="Watchdog restarted $SERVICE_NAME after $age_seconds seconds without result file updates.\n\nLatest file: $latest_path"
    local cmd=("$PYTHON_BIN" "$REPO_DIR/scripts/email_report.py" --subject "$subject" --message "$body")

    if [ -n "$ALERT_EMAIL" ]; then
        cmd+=(--to-email "$ALERT_EMAIL")
    fi

    if "${cmd[@]}" >> "$LOG_FILE" 2>&1; then
        log "[ALERT] Restart notification sent."
    else
        log "[WARN] Restart occurred, but email alert failed."
    fi
}

if [ ! -d "$RESULTS_ROOT" ]; then
    log "[WARN] Results root not found: $RESULTS_ROOT"
    exit 0
fi

latest_line=$(find "$RESULTS_ROOT" -type f \( -name '*.json' -o -name '*.csv' \) -printf '%T@ %p\n' 2>/dev/null | awk 'max=="" || $1>max {max=$1; line=$0} END {print line}')

if [ -z "$latest_line" ]; then
    log "[WARN] No result files found under $RESULTS_ROOT"
    exit 0
fi

latest_epoch="${latest_line%% *}"
latest_path="${latest_line#* }"
latest_epoch_int="${latest_epoch%.*}"
now_epoch=$(date +%s)
age_seconds=$((now_epoch - latest_epoch_int))

if [ "$age_seconds" -gt "$STALE_SECONDS" ]; then
    log "[STALE] No updates for ${age_seconds}s (> ${STALE_SECONDS}s). Restarting $SERVICE_NAME"
    if systemctl --user restart "$SERVICE_NAME"; then
        log "[ACTION] Restarted $SERVICE_NAME successfully."
        send_restart_alert
    else
        log "[ERROR] Failed to restart $SERVICE_NAME"
        exit 1
    fi
else
    log "[OK] Latest update ${age_seconds}s ago at $latest_path"
fi

exit 0