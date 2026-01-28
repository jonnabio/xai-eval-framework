#!/usr/bin/env python3
"""
Real-time Monitor for XAI Experiments.
Usage: python scripts/monitor_experiments.py
"""
import sys
import time
import os
import glob
import logging
from pathlib import Path
from datetime import datetime, timedelta
import curses

# Ensure src is in path
sys.path.append(str(Path(__file__).parent.parent))

from src.experiment.config import load_config as _load_config # Rename to avoid conflict if needed, but it's fine

def load_config_safe(path):
    try:
        return _load_config(path)
    except Exception as e:
        return None

def get_experiment_status(config_dir="configs/experiments/exp2_scaled"):
    """
    Scans all configs and determines status based on output files.
    """
    configs = glob.glob(os.path.join(config_dir, "*.yaml"))
    
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
            "start_time": None
        }

        if res_file.exists():
            entry["status"] = "finished"
            stats["finished"] += 1
            entry["completed_at"] = datetime.fromtimestamp(res_file.stat().st_mtime)
            # Infer start time from dir creation for batch metrics
            try:
                st = datetime.fromtimestamp(out_dir.stat().st_birthtime if hasattr(os.stat_result, 'st_birthtime') else out_dir.stat().st_ctime)
                start_times.append(st)
            except:
                pass
        elif out_dir.exists():
            # Directory exists but no result -> In Progress (or crashed)
            entry["status"] = "running"
            entry["start_time"] = datetime.fromtimestamp(out_dir.stat().st_birthtime if hasattr(os.stat_result, 'st_birthtime') else out_dir.stat().st_ctime)
            start_times.append(entry["start_time"])
            entry["duration"] = datetime.now() - entry["start_time"]
            stats["in_progress"].append(entry)
        else:
            stats["pending"] += 1
            
        results.append(entry)
        
    if start_times:
        stats["batch_start_time"] = min(start_times)
        
    return stats, results

def draw_dashboard(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(5000) # Refresh every 5s

    # Colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)

    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        # Header
        if max_y > 0:
            header = f"XAI Experiment Monitor - {datetime.now().strftime('%H:%M:%S')}"
            stdscr.addstr(0, 0, header[:max_x-1], curses.A_BOLD)
        
        # Load Stats
        try:
            stats, details = get_experiment_status()
        except Exception as e:
            if max_y > 2:
                msg = f"Error loading stats: {e}"
                stdscr.addstr(2, 0, msg[:max_x-1], curses.color_pair(3))
            stdscr.refresh()
            time.sleep(5)
            continue
            
        # Summary
        row = 2
        if row < max_y: stdscr.addstr(row, 0, f"Total Experiments: {stats['total']}")
        if row+1 < max_y: stdscr.addstr(row+1, 0, f"Finished: {stats['finished']}", curses.color_pair(1))
        if row+2 < max_y: stdscr.addstr(row+2, 0, f"Running:  {len(stats['in_progress'])}", curses.color_pair(2))
        if row+3 < max_y: stdscr.addstr(row+3, 0, f"Pending:  {stats['pending']}", curses.color_pair(4))
        
        # ETA Calculation
        eta_str = "Calculating..."
        if stats['batch_start_time'] and stats['finished'] > 0:
            elapsed = (datetime.now() - stats['batch_start_time']).total_seconds()
            rate = stats['finished'] / elapsed # experiments per second
            if rate > 0:
                remaining = stats['total'] - stats['finished']
                eta_seconds = remaining / rate
                eta = timedelta(seconds=int(eta_seconds))
                finish_time = datetime.now() + eta
                eta_str = f"{eta} (approx {finish_time.strftime('%H:%M')})"
        
        if row+4 < max_y: stdscr.addstr(row+4, 0, f"ETA:      {eta_str}", curses.A_BOLD)

        # System Utils
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory().percent
            if row+5 < max_y:
                stdscr.addstr(row+5, 0, f"CPU: {cpu}% | RAM: {mem}%", curses.color_pair(4))
            row_offset = 6
        except ImportError:
            row_offset = 5

        # Progress Bar
        pct = 0
        if stats['total'] > 0:
            pct = stats['finished'] / stats['total']
        
        if row+5+row_offset < max_y:
            bar_len = min(50, max_x - 20)
            if bar_len > 0:
                filled = int(bar_len * pct)
                bar = "[" + "=" * filled + " " * (bar_len - filled) + f"] {pct*100:.1f}%"
                stdscr.addstr(row+row_offset, 0, bar, curses.A_BOLD)

        # Active Experiments Table
        row += (row_offset + 2)
        if row < max_y: stdscr.addstr(row, 0, "Active Experiments:", curses.A_UNDERLINE)
        row += 1
        if row < max_y: 
            header_str = "{:<40} {:<10} {:<15}".format("Experiment", "Start Time", "Duration")
            stdscr.addstr(row, 0, header_str[:max_x-1])
        row += 1
        
        # Sort running by duration desc
        running = sorted(stats["in_progress"], key=lambda x: x["duration"], reverse=True)
        
        for exp in running[:20]: # Show max 20
            if row >= max_y - 4: break # Leave room for footer
            
            name = exp['name']
            if len(name) > 38: name = name[:35] + "..."
            start = exp['start_time'].strftime("%H:%M:%S")
            dur = str(exp['duration']).split('.')[0] # Remove micros
            
            line = "{:<40} {:<10} {:<15}".format(name, start, dur)
            stdscr.addstr(row, 0, line[:max_x-1], curses.color_pair(2))
            row += 1
            
        # Recent Finished
        row += 2
        if row < max_y: stdscr.addstr(row, 0, "Recently Finished:", curses.A_UNDERLINE)
        row += 1
        
        finished_list = sorted([x for x in details if x['status'] == 'finished'], 
                               key=lambda x: x.get('completed_at', datetime.min), reverse=True)
        
        for exp in finished_list[:5]:
            if row >= max_y: break
            name = exp['name']
            completed = exp.get('completed_at').strftime("%H:%M:%S")
            line = f"{name[:50]} ({completed})"
            stdscr.addstr(row, 0, line[:max_x-1], curses.color_pair(1))
            row += 1
            
        stdscr.refresh()
        
        # Input check to exit
        c = stdscr.getch()
        if c == ord('q'):
            break

if __name__ == "__main__":
    try:
        curses.wrapper(draw_dashboard)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
