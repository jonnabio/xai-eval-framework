#!/bin/bash

# Ensure script halts on any errors
set -e

if [ -z "$1" ]; then
  echo "Usage: ./install_cronjob.sh <your_gmail_app_password>"
  echo "You can generate an App Password at https://myaccount.google.com/apppasswords"
  exit 1
fi

APP_PASSWORD="$1"
VENV_PYTHON="/home/jonnabio/Documents/GitHub/xai-eval-framework/.venv/bin/python"
SCRIPT_PATH="/home/jonnabio/Documents/GitHub/xai-eval-framework/scripts/email_report.py"

# Write the cron syntax to a temporary file
CRON_FILE=$(mktemp)

# Export existing crontab safely (ignore error if no crontab exists)
crontab -l > "$CRON_FILE" 2>/dev/null || true

# Remove any existing instance of this specific script from the cron to avoid duplicates
sed -i '/email_report.py/d' "$CRON_FILE"

# Append the new job (Runs every 3 hours: minute 0, hour */3)
echo "0 */3 * * * export GMAIL_APP_PASSWORD='$APP_PASSWORD'; $VENV_PYTHON $SCRIPT_PATH >> /tmp/xai_cron.log 2>&1" >> "$CRON_FILE"

# Install the updated crontab
crontab "$CRON_FILE"
rm "$CRON_FILE"

echo "Success! The status report email script has been scheduled."
echo "It will run and email jonnabio@gmail.com every 3 hours."
