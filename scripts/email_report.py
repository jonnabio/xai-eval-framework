#!/usr/bin/env python3
import sys
import os
import smtplib
from email.message import EmailMessage
import re
import glob
import yaml
import json
from datetime import datetime

# Change working directory to the project root to ensure relative paths work
os.chdir('/home/jonnabio/Documents/GitHub/xai-eval-framework')

def generate_report():
    report_lines = []
    report_lines.append(f"XAI Eval Framework Status Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("="*60)
    
    # Check status
    config_dir = "configs/recovery/phase1"
    configs = glob.glob(os.path.join(config_dir, "*.yaml"))
    
    total_experiments = len(configs)
    finished = 0
    in_progress = 0
    
    for cfg in configs:
        name = os.path.basename(cfg).replace(".yaml", "")
        # Find if it has results
        # A bit hacky but fast:
        res = glob.glob("experiments/recovery/phase1/results/*/*/*/*/results.json")
        # Let's count properly
        pass
        
    outputs = glob.glob("experiments/recovery/phase1/results/*/*/*/results.json")
    finished = len(outputs)
    
    # 1. Total instances in all configs
    total_instances_overall = 0
    for cfg in configs:
        with open(cfg, 'r') as f:
            c = yaml.safe_load(f)
            spc = c.get('sampling', {}).get('samples_per_class', 0)
            target_instances = spc * 4
            total_instances_overall += target_instances

    # 2. Total completed instances from finished experiments
    completed_instances_overall = 0
    for out in outputs:
        try:
            with open(out, 'r') as f:
                d = json.load(f)
                completed_instances_overall += len(d.get("instance_evaluations", []))
        except:
            pass
            
    # 3. Running instances progress
    lines = []
    if os.path.exists("logs/batch_runner.log"):
        with open("logs/batch_runner.log", "r") as f:
            lines = f.readlines()[-3000:]
            
    running_stats = {}
    current_exp = None
    
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
                
    active_instances_completed = 0
    overall_remaining_seconds = 0
    active_count = 0
    
    eta_details = []
    
    for exp, data in exp_times.items():
        hist = data['history']
        if not hist:
            continue
            
        hist.sort(key=lambda x: x[1])
        unique_hist = {}
        for inst, t in hist:
            if inst not in unique_hist:
                 unique_hist[inst] = t
                 
        sorted_unique = sorted(list(unique_hist.items()), key=lambda x: x[0])
        
        last_inst = sorted_unique[-1][0]
        active_instances_completed += last_inst
        
        if len(sorted_unique) >= 2:
            first_inst, first_time = sorted_unique[0]
            _, last_time = sorted_unique[-1]
            diff_inst = last_inst - first_inst
            diff_sec = (last_time - first_time).total_seconds()
            
            if diff_inst > 0 and diff_sec > 0:
                sec_per_inst = diff_sec / diff_inst
                remaining_inst = data['total_instances'] - last_inst
                eta_sec = remaining_inst * sec_per_inst
                
                if eta_sec > overall_remaining_seconds:
                    overall_remaining_seconds = eta_sec
                active_count += 1
                
                eta_hrs = eta_sec / 3600
                eta_details.append(f" - {exp}: {last_inst}/{data['total_instances']} (ETA: {eta_hrs:.1f} hrs)")
            else:
                eta_details.append(f" - {exp}: {last_inst}/{data['total_instances']} (ETA: Calculating...)")
        else:
            eta_details.append(f" - {exp}: {last_inst}/{data['total_instances']} (ETA: Calculating...)")

    total_current_progress = completed_instances_overall + active_instances_completed
    progress_percentage = (total_current_progress / total_instances_overall) * 100 if total_instances_overall > 0 else 0
    
    
    report_lines.append("### Phase 1 Recovery Batch Status")
    report_lines.append(f"Total Configs: {total_experiments}")
    report_lines.append(f"Finished: {finished} / {total_experiments}")
    report_lines.append("")
    report_lines.append("### Instance-Level Progress")
    report_lines.append(f"Total Target Instances:           {total_instances_overall}")
    report_lines.append(f"Instances from Finished (16 exp): {completed_instances_overall}")
    report_lines.append(f"Instances built by Running:       {active_instances_completed}")
    report_lines.append(f"Total Inst Computations Done:     {total_current_progress} / {total_instances_overall}")
    report_lines.append(f"Overall Completion Percentage:    {progress_percentage:.2f}%")
    report_lines.append("")
    report_lines.append("### Active Experiments Progress & ETAs")
    if eta_details:
        report_lines.extend(eta_details)
    else:
        report_lines.append("No active experiments found in recent logs.")
        
    report_lines.append("")
    if active_count > 0:
        report_lines.append(f"**Overall Max ETA for running batch:** {overall_remaining_seconds / 3600 / 24:.1f} days ({overall_remaining_seconds / 3600:.1f} hours)")
    else:
        report_lines.append("**Overall Max ETA:** N/A")

    return "\n".join(report_lines)

def send_email(subject, body, to_email):
    # Retrieve credentials from environment variables manually set by the user
    gmail_user = os.environ.get("GMAIL_USER", "jonnabio@gmail.com")
    gmail_password = os.environ.get("GMAIL_APP_PASSWORD")

    from email.utils import make_msgid, formatdate
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = f"{subject} [{datetime.now().strftime('%H:%M:%S')}]"
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = make_msgid()

    if not gmail_password:
        print("WARNING: GMAIL_APP_PASSWORD environment variable not set.")
        print("Saving report locally to /tmp/latest_xai_report.txt instead of emailing.")
        with open("/tmp/latest_xai_report.txt", "w") as f:
            f.write(f"To: {to_email}\nSubject: {subject}\n\n{body}")
        return

    try:
        # Connect to Gmail's SMTP server securely
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()
        print(f"Successfully sent automated email report to {to_email} via Gmail SMTP.")
    except Exception as e:
        print(f"Failed to send email. Ensure your App Password is correct. Error: {e}")
        with open("/tmp/latest_xai_report.txt", "w") as f:
            f.write(f"To: {to_email}\nSubject: {subject}\n\n{body}")

if __name__ == "__main__":
    report_body = generate_report()
    send_email("XAI Framework Phase 1 Recovery - Progress Report", report_body, "jonnabio@gmail.com")
