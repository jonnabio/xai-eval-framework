#!/usr/bin/env python3
"""Simple resource monitor script.
Prints current CPU and RAM usage percentages.
Usage: python scripts/resource_monitor.py
"""
import sys
import os

# Ensure psutil is available
try:
    import psutil
except ImportError:
    sys.stderr.write("psutil is required. Install via 'pip install psutil'\n")
    sys.exit(1)

def main():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    print(f"CPU: {cpu}% | RAM: {mem}%")

if __name__ == "__main__":
    main()
