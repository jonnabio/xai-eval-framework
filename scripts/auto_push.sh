#!/bin/bash
# auto_push.sh - Periodic git sync for experiments

INTERVAL=900 # 15 minutes (so they constantly share internal checkpoints)

while true; do
    echo "[$(date)] Syncing progress with Git pool..."
    
    # Rebase any remote queue updates
    git pull --rebase origin $(git rev-parse --abbrev-ref HEAD)
    
    # Add checkpoints and logs so far
    git add experiments/ configs/ logs/
    git commit -m "Auto-sync queue: Checkpoints and progress"
    
    # Push back to pool
    git push origin $(git rev-parse --abbrev-ref HEAD)
    
    echo "[$(date)] Sync complete. Sleeping for $INTERVAL seconds..."
    sleep $INTERVAL
done
