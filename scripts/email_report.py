#!/usr/bin/env python3
import sys
import os
import smtplib
from email.message import EmailMessage
import re
import glob
import yaml
import json
import subprocess
from datetime import datetime

# Change working directory to the project root to ensure relative paths work
os.chdir('/home/jonnabio/Documents/GitHub/xai-eval-framework')

def generate_report():
    report_lines = []
    report_lines.append(f"XAI Eval Framework Status Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("="*60)
    
    # Check status
    config_dir = "configs/experiments/exp2_scaled"
    configs = glob.glob(os.path.join(config_dir, "**/*.yaml"), recursive=True)
    configs = [c for c in configs if "manifest" not in c]
    
    total_experiments = len(configs)
    finished = 0
    
    # Count finished experiments by checking for results.json in output dirs
    outputs = glob.glob("experiments/exp2_scaled/results/**/results.json", recursive=True)
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
        except (json.JSONDecodeError, IOError):
            pass
            
    # 3. Running instances progress — count instance JSON files directly from filesystem.
    # Log-parsing is unreliable for parallel workers since all workers share one log file
    # and "Processing instance" lines get attributed to the wrong experiment.
    active_instances_completed = 0
    active_count = 0
    eta_details = []

    instance_dirs = glob.glob("experiments/exp2_scaled/results/**/instances", recursive=True)
    for inst_dir in sorted(instance_dirs):
        parent = os.path.dirname(inst_dir)
        if os.path.exists(os.path.join(parent, "results.json")):
            continue  # already counted in completed_instances_overall

        count = len(glob.glob(os.path.join(inst_dir, "*.json")))
        active_instances_completed += count

        # Derive config name from path: .../results/<method>/seed_<s>/n_<n>/instances
        parts = parent.replace(os.sep, "/").split("/")
        method, seed_part, n_part = parts[-3], parts[-2], parts[-1]
        seed = seed_part.replace("seed_", "")
        n = n_part.replace("n_", "")
        exp_name = f"{method}_s{seed}_n{n}"

        total = 0
        # Config search by experiment name
        for cfg_file in configs:
            if exp_name in cfg_file:
                with open(cfg_file) as f:
                    c = yaml.safe_load(f)
                    spc = c.get("sampling", {}).get("samples_per_class", 0)
                    total = spc * 4
                break

        if total > 0:
            pct = count / total * 100
            remaining = total - count
            eta_details.append(f" - {exp_name}: {count}/{total} ({pct:.1f}% done, {remaining} remaining)")
            active_count += 1
        else:
            eta_details.append(f" - {exp_name}: {count}/? (config not found)")

    total_current_progress = completed_instances_overall + active_instances_completed
    progress_percentage = (total_current_progress / total_instances_overall) * 100 if total_instances_overall > 0 else 0
    
    
    report_lines.append("### EXP2 Scaled Batch Status")
    report_lines.append(f"Total Configs: {total_experiments}")
    report_lines.append(f"Finished: {finished} / {total_experiments}")
    report_lines.append("")
    report_lines.append("### Instance-Level Progress")
    report_lines.append(f"Total Target Instances:           {total_instances_overall}")
    report_lines.append(f"Instances from Finished ({finished} experiments): {completed_instances_overall}")
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
    # Summarize Overall ETA
    # (Based on current observed rate of ~10s per instance)
    time_per_instance = 10.0
    total_remaining = total_instances_overall - total_current_progress
    overall_eta_seconds = total_remaining * time_per_instance
    
    overall_eta_hours = overall_eta_seconds / 3600.0
    
    report_lines.append("### Current Summary Dashboard")
    report_lines.append(f"**Executing File:**      {eta_details[0].split(':')[0].strip('- ') if eta_details else 'N/A'}")
    report_lines.append(f"**Current Progress:**     {total_current_progress} / {total_instances_overall} ({progress_percentage:.2f}%)")
    report_lines.append(f"**Total Remaining:**      {total_remaining} instances")
    report_lines.append(f"**Estimated Time:**       ~{overall_eta_hours:.1f} hours left")
    report_lines.append(f"**Status:**               🚀 Running (3 workers)")
    report_lines.append("")
    
    report_lines.append("### Instance-Level Breakdown")
    report_lines.append(f"Fixed (Finished Experiments):   {completed_instances_overall}")
    report_lines.append(f"In-Flight (Pending Experiments):  {active_instances_completed}")
    report_lines.append(f"Target Total:                   {total_instances_overall}")
    report_lines.append("")
    
    report_lines.append("### Detailed Active Experiments")
    if eta_details:
        report_lines.extend(eta_details)
    else:
        report_lines.append("No active experiments found.")
        
    # Git status
    report_lines.append("")
    report_lines.append("### Recent Git Activity (Last 8 Commits)")
    try:
        git_log = subprocess.check_output(
            ["git", "log", "-n", "8", "--pretty=format:%h %ai %s"],
            text=True
        )
        report_lines.append(git_log)
        
        # Check sync status
        try:
            subprocess.run(["git", "fetch", "origin"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            local_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
            remote_hash = subprocess.check_output(["git", "rev-parse", "origin/main"], text=True).strip()
            
            if local_hash == remote_hash:
                report_lines.append("\nStatus: Synchronized with GitHub (All changes pushed)")
            else:
                unpushed_count = subprocess.check_output(["git", "rev-list", "--count", "origin/main..HEAD"], text=True).strip()
                report_lines.append(f"\nStatus: {unpushed_count} commits pending push (Pushes occur every 6h)")
        except:
            pass
            
    except Exception as e:
        report_lines.append(f"Error fetching git log: {e}")

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
    send_email("XAI Framework EXP2 Scaled - Progress Report", report_body, "jonnabio@gmail.com")
