import re
from datetime import datetime

try:
    with open("logs/batch_runner.log", "r") as f:
        # Use only the last N lines since the restart
        lines = f.readlines()[-3000:]
        
    running_stats = {}
    current_exp = None
    
    # regexes
    exp_re = re.compile(r"experiment: (rec_p1_exp2_svm_shap_[^\s]+)")
    proc_re = re.compile(r"Processing instance (\d+)/(\d+)")
    time_re = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")
    
    exp_times = {} 
    
    for line in lines:
        m_exp = exp_re.search(line)
        if m_exp:
            current_exp = m_exp.group(1)
            if current_exp not in exp_times:
                exp_times[current_exp] = {'total_instances': 0, 'history': []}
                
        if current_exp:
            m_proc = proc_re.search(line)
            m_time = time_re.search(line)
            if m_proc and m_time:
                inst = int(m_proc.group(1))
                tot = int(m_proc.group(2))
                t_str = m_time.group(1)
                t = datetime.strptime(t_str, "%Y-%m-%d %H:%M:%S")
                
                exp_times[current_exp]['total_instances'] = tot
                exp_times[current_exp]['history'].append((inst, t))
                
    print(f"{'Experiment':<35} | {'Progress':<10} | {'Time/Inst':<15} | {'ETA (Hours)':<15}")
    print("-" * 80)
    
    overall_remaining_seconds = 0
    active_count = 0

    for exp, data in exp_times.items():
        hist = data['history']
        if not hist:
            continue
            
        hist.sort(key=lambda x: x[1])
        
        # Filter to only keep unique instances, use the first time we see an instance
        unique_hist = {}
        for inst, t in hist:
            if inst not in unique_hist:
                 unique_hist[inst] = t
                 
        sorted_unique = sorted(list(unique_hist.items()), key=lambda x: x[0])
        
        if len(sorted_unique) < 2:
            print(f"{exp[:33]:<35} | {sorted_unique[-1][0]}/{data['total_instances']:<10} | {'Calculating...':<15} | {'Calculating...':<15}")
            continue
            
        first_inst, first_time = sorted_unique[0]
        last_inst, last_time = sorted_unique[-1]
        
        diff_inst = last_inst - first_inst
        diff_sec = (last_time - first_time).total_seconds()
        
        if diff_inst > 0 and diff_sec > 0:
            sec_per_inst = diff_sec / diff_inst
            remaining_inst = data['total_instances'] - last_inst
            eta_sec = remaining_inst * sec_per_inst
            eta_hrs = eta_sec / 3600
            eta_days = eta_hrs / 24
            
            if eta_sec > overall_remaining_seconds:
                overall_remaining_seconds = eta_sec
            active_count += 1
            
            print(f"{exp[:33]:<35} | {last_inst}/{data['total_instances']:<10} | {sec_per_inst/60:.1f} mins      | {eta_hrs:.1f} hrs ({eta_days:.1f} days)")
        else:
             print(f"{exp[:33]:<35} | {last_inst}/{data['total_instances']:<10} | {'Calculating...':<15} | {'Calculating...':<15}")
             
    print("-" * 80)
    if active_count > 0:
        print(f"Overall Max ETA for running batch: {overall_remaining_seconds / 3600 / 24:.1f} days ({overall_remaining_seconds / 3600:.1f} hours)")

except Exception as e:
    print(f"Error checking progress: {e}")
