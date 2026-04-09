#!/bin/bash
# auto_push.sh - Periodic git sync for experiment results and logs only.

INTERVAL=900
TRACKED_PATHS=("experiments/exp2_scaled/results" "logs")

while true; do
    echo "[$(date)] Syncing progress with Git pool..."

    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    if [ -z "$CURRENT_BRANCH" ]; then
        echo "[$(date)] Error resolving current branch."
        sleep "$INTERVAL"
        continue
    fi

    git add -- "${TRACKED_PATHS[@]}"

    if [ -n "$(git status --porcelain -- "${TRACKED_PATHS[@]}")" ]; then
        if ! git commit -m "Auto-sync queue: Results and logs checkpoint"; then
            echo "[$(date)] Commit failed; skipping pull/push for this cycle."
            sleep "$INTERVAL"
            continue
        fi
    else
        echo "[$(date)] No result/log changes to commit."
    fi

    if ! git pull --rebase --autostash origin "$CURRENT_BRANCH"; then
        echo "[$(date)] Pull --rebase failed; manual review may be required."
        sleep "$INTERVAL"
        continue
    fi

    if ! git push origin "$CURRENT_BRANCH"; then
        echo "[$(date)] Push failed; changes remain local for the next sync cycle."
    else
        echo "[$(date)] Sync complete."
    fi

    echo "[$(date)] Sleeping for $INTERVAL seconds..."
    sleep "$INTERVAL"
done
