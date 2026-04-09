#!/usr/bin/env python3
import os
import glob
import time
import yaml
import json
import psutil
import subprocess
from datetime import datetime, timedelta

# Config
PROJECT_ROOT = "/home/jonnabio/Documents/GitHub/xai-eval-framework"
LOG_FILE = os.path.join(PROJECT_ROOT, "logs/managed_runner.log")
CONFIG_DIR = os.path.join(PROJECT_ROOT, "configs/experiments/exp2_scaled")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "experiments/exp2_scaled/results")
OS_RAM_BUFFER = 2.0 # GB

def get_status():
    os.chdir(PROJECT_ROOT)
    
    # 1. System Info
    mem = psutil.virtual_memory()
    available_gb = mem.available / (1024**3)
    load = os.getloadavg()[0]
    
    # 2. Main Progress
    configs = glob.glob(os.path.join(CONFIG_DIR, "*.yaml"))
    total_configs = len(configs)
    
    results = glob.glob(os.path.join(RESULTS_DIR, "**/results.json"), recursive=True)
    finished_configs = len(results)
    
    # 3. Instance Progress
    total_target_instances = 0
    for cfg_path in configs:
        try:
            with open(cfg_path, 'r') as f:
                c = yaml.safe_load(f)
                total_target_instances += c.get('sampling', {}).get('samples_per_class', 100) * 4
        except: continue

    completed_instances = 0
    for r_path in results:
        try:
            with open(r_path, 'r') as f:
                d = json.load(f)
                completed_instances += len(d.get("instance_evaluations", []))
        except: continue
        
    # Active Progress
    active_instances = 0
    active_exps = []
    
    # Helper to map results folder name to config path
    name_to_config = {}
    for cp in configs:
        base = os.path.basename(cp).replace(".yaml", "")
        # Normalize: svmanchorss42n200
        norm = base.replace("_", "").replace("-", "")
        name_to_config[norm] = cp

    instance_dirs = glob.glob(os.path.join(RESULTS_DIR, "**/instances"), recursive=True)
    for inst_dir in sorted(instance_dirs):
        parent = os.path.dirname(inst_dir)
        if os.path.exists(os.path.join(parent, "results.json")):
            continue
        
        count = len(glob.glob(os.path.join(inst_dir, "*.json")))
        active_instances += count
        
        # Folder structure check
        rel_path = os.path.relpath(parent, RESULTS_DIR)
        parts = rel_path.split(os.sep)
        if len(parts) >= 3:
            # results/<method>/seed_<seed>/n_<n>
            method, seed, n = parts[-3], parts[-2], parts[-1]
            
            # Normalize display name
            display_name = f"{method}_{seed}_{n}"
            
            # Match to config
            # results-based norm: svmanchorsseed42n200
            res_norm = display_name.replace("_", "").replace("-", "")
            # Also try without "seed" (matching s42n200)
            res_norm_short = res_norm.replace("seed", "s").replace("n_", "n")
            
            target = 400 # fallback
            match_path = name_to_config.get(res_norm_short) or name_to_config.get(res_norm)
            
            if match_path:
                   try:
                       with open(match_path) as f:
                           c = yaml.safe_load(f)
                           # Usually samples_per_class * 4 quadrants
                           target = c.get('sampling', {}).get('samples_per_class', 100) * 4
                   except: pass
            
            active_exps.append({"name": display_name, "done": count, "total": target})

    total_done = completed_instances + active_instances
    pct = (total_done / total_target_instances * 100) if total_target_instances > 0 else 0
    
    # 4. ETA
    remaining = total_target_instances - total_done
    # Using 10s per instance as our observed rate
    eta_seconds = remaining * 10
    eta_delta = timedelta(seconds=int(eta_seconds))
    
    # Git
    try:
        last_commit = subprocess.check_output(["git", "log", "-1", "--pretty=format:%h (%cr) %s"], text=True).strip()
    except: last_commit = "Unknown"

    return {
        "mem": available_gb,
        "load": load,
        "total_configs": total_configs,
        "finished_configs": finished_configs,
        "progress_inst": f"{total_done:,} / {total_target_instances:,} ({pct:.2f}%)",
        "active": active_exps,
        "eta": str(eta_delta),
        "last_git": last_commit
    }

def draw(status):
    os.system('clear')
    print("\033[94m" + "="*70 + "\033[0m")
    print("\033[1;37mXAI EXPERIMENT DASHBOARD\033[0m".center(70))
    print("\033[94m" + "="*70 + "\033[0m")
    
    print(f" \033[1mSystem Status:\033[0m")
    print(f" RAM Available: {status['mem']:.2f} GB  |  Load (1m): {status['load']:.2f}")
    print(f" Workers Ready: 3 concurrent (RAM Limited)")
    print("-" * 70)
    
    print(f" \033[1mOverall Progress:\033[0m")
    print(f" Experiments Finished: {status['finished_configs']} / {status['total_configs']}")
    print(f" Instance Progress:     \033[1;32m{status['progress_inst']}\033[0m")
    print(f" Total ETA:             \033[1;33m~ {status['eta']} remaining\033[0m")
    print("-" * 70)
    
    print(f" \033[1mActive Experiments:\033[0m")
    if not status['active']:
        print("  - [WAIT] Waiting for scheduler...")
    else:
        for exp in status['active'][:5]: # Show top 5
            epct = (exp['done'] / exp['total'] * 100)
            bar_len = 20
            filled = int(epct / 100 * bar_len)
            bar = "█" * filled + "░" * (bar_len - filled)
            print(f"  {exp['name'][:30]:<30} [{bar}] {exp['done']}/{exp['total']} ({epct:.1f}%)")
    
    print("-" * 70)
    print(f" \033[1mLast Git Activity:\033[0m")
    print(f" {status['last_git']}")
    print("\033[94m" + "="*70 + "\033[0m")
    print(f" Update Cycle: 5s | Press Ctrl+C to exit dashboard (Runner will continue)")

if __name__ == "__main__":
    try:
        while True:
            s = get_status()
            draw(s)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\nDashboard exited. experiments are still running in the background.")
