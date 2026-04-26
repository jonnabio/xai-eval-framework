#!/bin/bash
# Install a Linux/WSL cron job for EXP3 email status reports every 3 hours.

set -euo pipefail

if [ "${1:-}" = "" ]; then
  echo "Usage: ./scripts/install_cronjob.sh <your_gmail_app_password> [to_email]"
  echo "You can generate an App Password at https://myaccount.google.com/apppasswords"
  exit 1
fi

APP_PASSWORD="$1"
TO_EMAIL="${2:-${XAI_REPORT_TO:-jonnabio@gmail.com}}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ -n "${VENV_PYTHON:-}" ]; then
  PYTHON_BIN="$VENV_PYTHON"
elif [ -x "$PROJECT_ROOT/.venv-wsl/bin/python3" ]; then
  PYTHON_BIN="$PROJECT_ROOT/.venv-wsl/bin/python3"
elif [ -x "$PROJECT_ROOT/.venv/bin/python" ]; then
  PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python"
else
  PYTHON_BIN="$(command -v python3)"
fi

SCRIPT_PATH="$PROJECT_ROOT/scripts/email_report.py"
LOG_PATH="$PROJECT_ROOT/logs/email_report_cron.log"

mkdir -p "$PROJECT_ROOT/logs"

CRON_FILE="$(mktemp)"
crontab -l > "$CRON_FILE" 2>/dev/null || true
sed -i '\#scripts/email_report.py#d' "$CRON_FILE"

cat >> "$CRON_FILE" <<EOF
0 */3 * * * cd "$PROJECT_ROOT" && GMAIL_APP_PASSWORD='$APP_PASSWORD' XAI_REPORT_TO='$TO_EMAIL' "$PYTHON_BIN" "$SCRIPT_PATH" --experiment "EXP3 Cross-Dataset" --config-dir configs/experiments/exp3_cross_dataset --results-dir experiments/exp3_cross_dataset/results --log-file logs/managed_runner_exp3.log >> "$LOG_PATH" 2>&1
EOF

crontab "$CRON_FILE"
rm "$CRON_FILE"

echo "Success! EXP3 status email report is scheduled every 3 hours."
echo "Recipient: $TO_EMAIL"
echo "Python: $PYTHON_BIN"
echo "Log: $LOG_PATH"
