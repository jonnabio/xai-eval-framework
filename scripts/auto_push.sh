#!/bin/bash
# auto_push.sh - Periodic git sync for experiment results only.

INTERVAL="${INTERVAL:-900}"
PUSH_INTERVAL="${PUSH_INTERVAL:-10800}"
LAST_PUSH_EPOCH=0
if [ "$#" -gt 0 ]; then
    TRACKED_PATHS=("$@")
else
    TRACKED_PATHS=("experiments/exp2_scaled/results")
fi

while true; do
    echo "[$(date)] Checking for result changes to commit..."
    NOW_EPOCH=$(date +%s)
    PUSH_DUE=0
    if (( NOW_EPOCH - LAST_PUSH_EPOCH >= PUSH_INTERVAL )); then
        PUSH_DUE=1
    fi

    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    if [ -z "$CURRENT_BRANCH" ]; then
        echo "[$(date)] Error resolving current branch."
        sleep "$INTERVAL"
        continue
    fi

    git add -- "${TRACKED_PATHS[@]}"

    if [ -n "$(git status --porcelain -- "${TRACKED_PATHS[@]}")" ]; then
        if ! git commit -m "Auto-sync queue: Results checkpoint"; then
            echo "[$(date)] Commit failed; skipping fetch/push for this cycle."
            sleep "$INTERVAL"
            continue
        fi
    else
        echo "[$(date)] No result changes to commit."
    fi

    if (( PUSH_DUE == 0 )); then
        NEXT_PUSH_MINUTES=$(( (PUSH_INTERVAL - (NOW_EPOCH - LAST_PUSH_EPOCH) + 59) / 60 ))
        echo "[$(date)] Push not due yet; next push window opens in about $NEXT_PUSH_MINUTES minutes."
        echo "[$(date)] Sleeping for $INTERVAL seconds..."
        sleep "$INTERVAL"
        continue
    fi

    LAST_PUSH_EPOCH=$(date +%s)
    echo "[$(date)] Push window reached; syncing committed progress with origin."

    if ! git fetch --no-progress origin "$CURRENT_BRANCH"; then
        echo "[$(date)] Fetch failed; manual review may be required."
        sleep "$INTERVAL"
        continue
    fi

    if ! git push --no-progress origin "$CURRENT_BRANCH"; then
        echo "[$(date)] Push failed, likely due to remote divergence; changes remain local for the next sync cycle."
    else
        echo "[$(date)] Sync complete."
    fi

    echo "[$(date)] Sleeping for $INTERVAL seconds..."
    sleep "$INTERVAL"
done
