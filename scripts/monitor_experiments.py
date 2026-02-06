#!/usr/bin/env python3
"""
Real-time Monitor for XAI Experiments.
Usage: python scripts/monitor_experiments.py [config_dir]
"""
import sys
import time
import os
import glob
import logging
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import curses
import collections

# Ensure src is in path
sys.path.append(str(Path(__file__).parent.parent))

# Try imports
try:
    from src.experiment.config import load_config as _load_config
except ImportError as e:
    # If running from scripts/, parent might not be in path correctly if not set
    sys.path.append(os.getcwd())
    try:
        from src.experiment.config import load_config as _load_config
    except ImportError:
        # Fallback for when src is not Python package or path issue
        # Just manually load yaml if needed, but let's try to be robust
        print(f"Error importing src.experiment.config: {e}")
        # Try to modify path to include the root of the repo explicitly
        repo_root = str(Path(__file__).resolve().parent.parent)
        sys.path.append(repo_root)
        try:
             from src.experiment.config import load_config as _load_config
        except ImportError:
             print(f"Critical Error: Could not import src.experiment.config even after adding {repo_root} to path.")
             sys.exit(1)

def load_config_safe(path):
    try:
        return _load_config(path)
    except Exception as e:
        return None

def get_experiment_status(config_dir="configs/experiments"):
    """
    Scans configs and determines status based on output files.
    """
    # Recursive search for configs
    configs = glob.glob(os.path.join(config_dir, "**/*.yaml"), recursive=True)
    
    stats = {
        "total": 0,
        "finished": 0,
        "in_progress": [],
        "pending": 0,
        "failed": 0,
        "skipped": 0,
        "batch_start_time": None
    }
    
    results = []
    start_times = []

    for cfg_path in configs:
        if "manifest" in cfg_path:
            continue
            
        stats["total"] += 1
        cfg = load_config_safe(Path(cfg_path))
        
        if not cfg:
            stats["skipped"] += 1
            continue
            
        out_dir = cfg.output_dir
        res_file = out_dir / "results.json"
        
        entry = {
            "name": cfg.name,
            "status": "pending",
            "duration": None,
            "start_time": None,
            "config_path": cfg_path
        }

        if res_file.exists():
            entry["status"] = "finished"
            stats["finished"] += 1
            entry["completed_at"] = datetime.fromtimestamp(res_file.stat().st_mtime)
            # Try to find start time
            try:
                # Use directory creation time as a proxy for start time
                st = datetime.fromtimestamp(out_dir.stat().st_ctime)
                entry["start_time"] = st
                start_times.append(st)
                entry["duration"] = entry["completed_at"] - st
            except:
                pass
        elif out_dir.exists():
            # Directory exists but no result -> In Progress (or crashed)
            entry["status"] = "running"
            try:
                entry["start_time"] = datetime.fromtimestamp(out_dir.stat().st_ctime)
                start_times.append(entry["start_time"])
                entry["duration"] = datetime.now() - entry["start_time"]
            except:
                 entry["start_time"] = datetime.now()
            stats["in_progress"].append(entry)
        else:
            stats["pending"] += 1
            
        results.append(entry)
        
    if start_times:
        stats["batch_start_time"] = min(start_times)
        
    return stats, results

def tail_log(filename, n=10):
    """Return last n lines of a file."""
    if not os.path.exists(filename):
        return [f"Log file not found: {filename}"]
    
    try:
        # Simple tail implementation
        with open(filename, 'r') as f:
            # Read all lines is inefficient for huge files but safe for now
            # For 25MB file it's okay, but maybe seek to end?
            f.seek(0, 2)
            fsize = f.tell()
            f.seek(max(fsize - 10000, 0), 0) # Read last 10KB
            lines = f.readlines()
            return lines[-n:]
    except Exception as e:
        return [f"Error reading log: {e}"]

def safe_addstr(win, y, x, string, attr=0):
    """Safely add string to window, ignoring errors if out of bounds."""
    try:
        max_y, max_x = win.getmaxyx()
        if y >= max_y or x >= max_x:
            return
        
        # Truncate if needed
        available_len = max_x - x - 1
        if len(string) > available_len:
            string = string[:available_len]
            
        win.addstr(y, x, string, attr)
    except curses.error:
        pass

def draw_dashboard(stdscr, config_dir, log_file):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1000) # Refresh every 1s

    # Colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE) # Header

    last_refresh = 0
    stats = None
    details = None
    log_lines = []
    
    while True:
        max_y, max_x = stdscr.getmaxyx()
        
        # Calculate split size
        dashboard_height = int(max_y * 0.7)
        log_height = max_y - dashboard_height
        
        if dashboard_height < 5 or log_height < 3:
             # Screen too small
             try:
                 stdscr.erase()
                 stdscr.addstr(0,0, "Screen too small")
                 stdscr.refresh()
             except: pass
             time.sleep(0.5)
             continue

        # Windows
        try:
            # Recreate windows to handle resize
            dash_win = stdscr.subwin(dashboard_height, max_x, 0, 0)
            log_win = stdscr.subwin(log_height, max_x, dashboard_height, 0)
        except:
            # If screen too small
            continue
            
        dash_win.erase()
        log_win.erase()
        
        # --- DATA UPDATE (throttled) ---
        now = time.time()
        if now - last_refresh > 2 or stats is None: # Refresh stats every 2s
            try:
                stats, details = get_experiment_status(config_dir)
                last_refresh = now
            except Exception as e:
                safe_addstr(dash_win, 2, 0, f"Error loading stats: {e}", curses.color_pair(3))
        
        # Always update log
        log_lines = tail_log(log_file, n=log_height-2)

        # --- DASHBOARD RENDER ---
        # Header
        header = f" XAI Experiment Monitor | {datetime.now().strftime('%H:%M:%S')} "
        safe_addstr(dash_win, 0, 0, header, curses.color_pair(5) | curses.A_BOLD)
        dash_win.chgat(0, 0, -1, curses.color_pair(5))
        
        if stats:
            # Summary
            row = 2
            safe_addstr(dash_win, row, 1, f"Total: {stats['total']}")
            safe_addstr(dash_win, row, 15, f"Finished: {stats['finished']}", curses.color_pair(1))
            safe_addstr(dash_win, row, 30, f"Running: {len(stats['in_progress'])}", curses.color_pair(2))
            safe_addstr(dash_win, row, 45, f"Pending: {stats['pending']}", curses.color_pair(4))
            
            # ETA
            eta_str = "Calculating..."
            if stats['batch_start_time'] and stats['finished'] > 0:
                elapsed = (datetime.now() - stats['batch_start_time']).total_seconds()
                rate = stats['finished'] / elapsed 
                if rate > 0:
                    remaining = stats['total'] - stats['finished']
                    eta_seconds = remaining / rate
                    finish_time = datetime.now() + timedelta(seconds=int(eta_seconds))
                    eta_str = f"{timedelta(seconds=int(eta_seconds))} (End: {finish_time.strftime('%H:%M')})"
            
            
            safe_addstr(dash_win, row, 60, f"ETA: {eta_str}", curses.A_BOLD)

            # System Utils
            try:
                import psutil
                cpu = psutil.cpu_percent(interval=None) # Start async measurement if possible, or non-blocking
                mem = psutil.virtual_memory().percent
                safe_addstr(dash_win, row, 90, f"CPU: {cpu}% | RAM: {mem}%", curses.color_pair(4))
            except ImportError:
                 safe_addstr(dash_win, row, 90, "Run pip install psutil", curses.color_pair(3))
            
            # Progress Bar
            row += 2
            pct = stats['finished'] / stats['total'] if stats['total'] > 0 else 0
            pct_str = f" {pct*100:.1f}%"
            # Reserve space for brackets [] and the percentage string and some margin (start + end brackets = 2)
            reserved = 2 + len(pct_str)
            bar_len = max(max_x - 4 - reserved, 10)
            
            filled = int(bar_len * pct)
            # Ensure filled doesn't exceed bar_len due to float rounding issues
            filled = min(filled, bar_len)
            
            bar = "[" + "=" * filled + " " * (bar_len - filled) + "]" + pct_str
            safe_addstr(dash_win, row, 1, bar, curses.color_pair(4))
            
            # Active Experiments
            row += 2
            safe_addstr(dash_win, row, 1, "Active Experiments:", curses.A_UNDERLINE)
            row += 1
            
            header_str = "{:<40} {:<10} {:<15}".format("Experiment", "Start", "Duration")
            safe_addstr(dash_win, row, 1, header_str, curses.A_BOLD)
            row += 1
            
            running = sorted(stats["in_progress"], key=lambda x: x["duration"] if x["duration"] else timedelta(0), reverse=True)
            for exp in running:
                if row >= dashboard_height - 1: break
                
                name = exp['name']
                if len(name) > 38: name = name[:35] + "..."
                start = exp['start_time'].strftime("%H:%M:%S") if isinstance(exp['start_time'], datetime) else "?"
                dur = str(exp['duration']).split('.')[0]
                
                line = "{:<40} {:<10} {:<15}".format(name, start, dur)
                safe_addstr(dash_win, row, 1, line, curses.color_pair(2))
                row += 1

        # --- LOG RENDER ---
        # Separator
        log_win.hline(0, 0, curses.ACS_HLINE, max_x)
        safe_addstr(log_win, 0, 2, f" Log Tail: {log_file} ", curses.A_REVERSE)
        
        l_row = 1
        for line in log_lines:
            if l_row >= log_height - 1: break
            clean_line = line.strip()
            # if len(clean_line) > max_x - 2: clean_line = clean_line[:max_x-5] + "..."
            safe_addstr(log_win, l_row, 1, clean_line)
            l_row += 1

        dash_win.refresh()
        log_win.refresh()
        
        # Auto-refresh log often, dashboard less often logic handled data-side.
        # But we need to handle input
        c = stdscr.getch()
        if c == ord('q'):
            break

def main():
    parser = argparse.ArgumentParser(description="Monitor XAI Experiments")
    parser.add_argument("--config_dir", default="configs/experiments", help="Directory containing experiment configs")
    
    # improved default log search
    default_log = "logs/recovery_runner.log"
    possible_logs = [
        "logs/recovery_runner.log",
        "final_log.txt", 
        "logs/final_log.txt"
    ]
    for p in possible_logs:
        if os.path.exists(p):
            default_log = p
            break
            
    parser.add_argument("--log_file", default=default_log, help="Log file to tail")
    args = parser.parse_args()

    if not os.path.exists(args.config_dir):
        # Only warn, don't exit, might be just monitoring logs
        pass
    
    try:
        curses.wrapper(draw_dashboard, args.config_dir, args.log_file)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Fatal Error: {e}")

if __name__ == "__main__":
    main()
