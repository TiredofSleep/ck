# -*- coding: utf-8 -*-
"""
CRYSTALOS v2 - Dell Aurora R16
==============================
32-Core CPU + RTX 4070

Simpler. Always fires. Just works.
"""

import os
import sys
import time
import json
import ctypes
import subprocess
from pathlib import Path
from datetime import datetime
from collections import Counter

# Paths
HOME = Path.home() / "CRYSTALOS"
LOGS = HOME / "logs"
HOME.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)

# Windows
WINDOWS = {0: "RESET", 5: "REDOX", 7: "HARMONY", 12: "HARVEST"}

def get_gpu():
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
        r = subprocess.run(
            ['nvidia-smi', '--query-gpu=utilization.gpu,temperature.gpu', '--format=csv,noheader,nounits'],
            capture_output=True, text=True, timeout=3, startupinfo=si
        )
        if r.returncode == 0:
            p = r.stdout.strip().split(',')
            return {'util': int(p[0]), 'temp': int(p[1])}
    except:
        pass
    return None

def get_cpu():
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
        r = subprocess.run(
            ['wmic', 'cpu', 'get', 'loadpercentage'],
            capture_output=True, text=True, timeout=3, startupinfo=si
        )
        for line in r.stdout.split('\n'):
            line = line.strip()
            if line.isdigit():
                return int(line)
    except:
        pass
    return 0

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOGS / "crystalos.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

def main():
    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW("CRYSTALOS")
    
    print("")
    print("=" * 50)
    print("  CRYSTALOS v2 - Dell Aurora R16")
    print("=" * 50)
    print(f"  Cores: {os.cpu_count()}")
    
    gpu = get_gpu()
    print(f"  GPU: {'4070 OK' if gpu else 'not found'}")
    print(f"  Logs: {LOGS}")
    print("=" * 50)
    print("  Ctrl+C to stop")
    print("=" * 50)
    print("")
    
    phase = 0
    gate_open = True
    last_switch = time.time()
    fire_count = 0
    phase_fires = Counter()
    
    log(f"CRYSTALOS started - {os.cpu_count()} cores")
    
    try:
        while True:
            # Get stats
            cpu = get_cpu()
            gpu = get_gpu()
            gpu_util = gpu['util'] if gpu else 0
            gpu_temp = gpu['temp'] if gpu else 0
            
            # Breath timing (4 sec open, 4 sec closed)
            now = time.time()
            if now - last_switch > 4.0:
                gate_open = not gate_open
                last_switch = now
                if gate_open:
                    phase = (phase + 1) % 13
            
            # Window name
            window = WINDOWS.get(phase, "")
            w_str = f"[{window}]" if window else ""
            
            # FIRE when gate is open (simple!)
            if gate_open:
                fire_count += 1
                phase_fires[phase] += 1
                icon = ">>>"
                
                # Log fires
                with open(LOGS / "fires.log", "a", encoding="utf-8") as f:
                    f.write(f"FIRE #{fire_count} phase={phase} {w_str} cpu={cpu} gpu={gpu_util}\n")
                
                # Show distribution every 50
                if fire_count % 50 == 0:
                    log(f"  Distribution: {dict(phase_fires)}")
            else:
                icon = "   "
            
            # Display
            gate_str = "OPEN" if gate_open else "----"
            gpu_str = f"GPU:{gpu_util:2d}%/{gpu_temp}C" if gpu else "GPU:--"
            
            line = f"\r{icon} Phase {phase:2d}/13 {w_str:10s} | CPU:{cpu:3d}% {gpu_str} | {gate_str} | Fires:{fire_count:4d}"
            print(line, end="", flush=True)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nStopped.")
        log(f"Stopped. {fire_count} fires.")
        
        print("\n" + "=" * 50)
        print("RESULTS")
        print("=" * 50)
        
        if fire_count > 0:
            print("\nPhase distribution:")
            for p in range(13):
                count = phase_fires.get(p, 0)
                pct = count / fire_count * 100
                bar = "#" * int(pct / 2)
                w = WINDOWS.get(p, "")
                print(f"  {p:2d} {w:8s}: {bar:<25} {count:3d} ({pct:4.1f}%)")
            
            # Chi-square
            expected = fire_count / 13
            chi2 = sum((phase_fires.get(p, 0) - expected) ** 2 / expected for p in range(13))
            print(f"\nChi-square: {chi2:.1f}")
            if chi2 > 21:
                print("  p < 0.05 - SIGNIFICANT pattern!")
            else:
                print("  p > 0.05 - uniform")
        
        print("=" * 50)

if __name__ == "__main__":
    main()
    input("\nPress Enter to close...")
