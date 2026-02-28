import re
import glob
import yaml
from pathlib import Path
from datetime import datetime
import json

try:
    # 1. Total instances in all configs
    total_instances_overall = 0
    configs = glob.glob("configs/recovery/phase1/*.yaml")
    for cfg in configs:
        with open(cfg, 'r') as f:
            c = yaml.safe_load(f)
            # Typically samples_per_class * 4 classes (TP, TN, FP, FN)
            spc = c.get('sampling', {}).get('samples_per_class', 0)
            target_instances = spc * 4
            total_instances_overall += target_instances

    # 2. Total completed instances from finished experiments
    outputs = glob.glob("experiments/recovery/phase1/results/*/*/*/results.json")
    completed_instances_overall = 0
    for out in outputs:
        try:
            with open(out, 'r') as f:
                d = json.load(f)
                completed_instances_overall += len(d.get("instance_evaluations", []))
        except:
            pass
            
    # 3. Running instances progress
    with open("logs/batch_runner.log", "r") as f:
        # Use only the last N lines since the restart
        lines = f.readlines()[-3000:]
        
    running_stats = {}
    current_exp = None
    
    # regexes
    exp_re = re.compile(r"experiment: (rec_p1_exp2_svm_shap_[^\s]+)")
    proc_re = re.compile(r"Processing instance (\d+)/(\d+)")
    
    exp_times = {} 
    
    for line in lines:
        m_exp = exp_re.search(line)
        if m_exp:
            current_exp = m_exp.group(1)
            if current_exp not in exp_times:
                exp_times[current_exp] = {'total_instances': 0, 'history': []}
                
        if current_exp:
            m_proc = proc_re.search(line)
            if m_proc:
                inst = int(m_proc.group(1))
                tot = int(m_proc.group(2))
                exp_times[current_exp]['total_instances'] = tot
                exp_times[current_exp]['history'].append(inst)
                
    active_instances_completed = 0
    for exp, data in exp_times.items():
        hist = data['history']
        if hist:
            active_instances_completed += max(hist)

    # 4. Total overall progress
    total_current_progress = completed_instances_overall + active_instances_completed
    progress_percentage = (total_current_progress / total_instances_overall) * 100 if total_instances_overall > 0 else 0
    
    print("=" * 40)
    print("Instance-Level Progress for Phase 1")
    print("=" * 40)
    print(f"Total Target Instances:           {total_instances_overall}")
    print(f"Instances from Finished (16 exp): {completed_instances_overall}")
    print(f"Instances built by Running (6 ex):{active_instances_completed}")
    print(f"Total Inst Computations Done:     {total_current_progress} / {total_instances_overall}")
    print(f"Overall Completion Percentage:    {progress_percentage:.2f}%")
    print("=" * 40)

except Exception as e:
    print(f"Error checking progress: {e}")
