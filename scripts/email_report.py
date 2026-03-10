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
            
    # 3. Running instances progress — count instance JSON files directly from filesystem.
    # Log-parsing is unreliable for parallel workers since all workers share one log file
    # and "Processing instance" lines get attributed to the wrong experiment.
    active_instances_completed = 0
    overall_remaining_seconds = 0
    active_count = 0
    eta_details = []

    instance_dirs = glob.glob("experiments/recovery/phase1/results/*/*/*/instances")
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
        exp_name = f"rec_p1_exp2_{method}_s{seed}_n{n}"

        total = 0
        cfg_path = f"configs/recovery/phase1/{method}_s{seed}_n{n}.yaml"
        if os.path.exists(cfg_path):
            with open(cfg_path) as f:
                c = yaml.safe_load(f)
                spc = c.get("sampling", {}).get("samples_per_class", 0)
                total = spc * 4

        if total > 0:
            pct = count / total * 100
            remaining = total - count
            eta_details.append(f" - {exp_name}: {count}/{total} ({pct:.1f}% done, {remaining} remaining)")
            active_count += 1
        else:
            eta_details.append(f" - {exp_name}: {count}/? (config not found)")

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
    total_remaining = total_instances_overall - total_current_progress
    if active_count > 0:
        report_lines.append(f"**Remaining instances across all active runs:** {total_remaining}")
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
