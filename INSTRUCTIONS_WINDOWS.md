# Instructions for Windows Node

We have just re-architected the `xai-eval-framework` to act as a **Decentralized Peer-to-Peer Compute Cluster** over Git. This will allow the Linux and Windows workstations to crunch through the experiment queue collaboratively, drastically reducing evaluation time without overlapping runs.

## Important Structural Changes

- **Randomized Target Fetching:** `src/experiment/runner.py` now naturally shuffles the target rows when evaluating a set of instances. Even if both machines launch the same configuration script simultaneously, they will process instances from random trajectories.
- **Aggressive Checkpointing:** `scripts/auto_push.sh` is now a 15-minute background polling daemon that explicitly pushes internal JSON instances to the master Git pool. It automatically rebases remote changes.
- **Daemon Hookup:** `scripts/managed_runner.sh` now daemonizes the auto-push service on launch and safely cleans it up when the script finishes.

## How to Initialize Evaluation

Please copy and paste these exact steps into your LLM terminal on the Windows machine. Ensure your Git push credentials/tokens are properly initialized, as the system relies heavily on pushing `instances/` dynamically.

```bash
# 1. Stash any parallel collisions or stray checkpoints
git stash

# 2. Pull the structural upgrades from the master pool
git pull --rebase origin main

# 3. Double-check your requirements
pip install -r requirements.txt

# 4. Background execution (This will invoke both the worker and the syncer)
nohup bash scripts/managed_runner.sh > logs/nohup_runner.log 2>&1 &

echo "Runner launched! You can monitor progress with: tail -f logs/managed_runner.log"
```

Once executed on both sides, the machines will automatically avoid repeating each other's evaluated models and safely sync their checkpoints without needing a centralized database layer.
