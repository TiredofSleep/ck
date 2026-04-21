# -*- coding: utf-8 -*-
"""
CRYSTALOS - TIG Engine for Dell Aurora R16
==========================================
24-Core CPU + RTX 4070 GPU Coherence Monitor

Just run: python crystalos.py
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

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ============================================================
# PATHS
# ============================================================

CRYSTALOS_HOME = Path.home() / "CRYSTALOS"
CRYSTALOS_LOGS = CRYSTALOS_HOME / "logs"
CRYSTALOS_STATE = CRYSTALOS_HOME / "state"

CRYSTALOS_HOME.mkdir(exist_ok=True)
CRYSTALOS_LOGS.mkdir(exist_ok=True)
CRYSTALOS_STATE.mkdir(exist_ok=True)

# ============================================================
# WINDOWS CPU READING
# ============================================================

class FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", ctypes.c_uint32),
                ("dwHighDateTime", ctypes.c_uint32)]

def get_cpu_times():
    idle = FILETIME()
    kernel = FILETIME()
    user = FILETIME()
    success = ctypes.windll.kernel32.GetSystemTimes(
        ctypes.byref(idle),
        ctypes.byref(kernel),
        ctypes.byref(user)
    )
    if success:
        return idle, kernel, user
    return None, None, None

def filetime_to_int(ft):
    return (ft.dwHighDateTime << 32) | ft.dwLowDateTime

def calc_cpu_percent(prev, curr):
    if not prev or not curr or not prev[0] or not curr[0]:
        return 0.5
    
    idle_diff = filetime_to_int(curr[0]) - filetime_to_int(prev[0])
    kernel_diff = filetime_to_int(curr[1]) - filetime_to_int(prev[1])
    user_diff = filetime_to_int(curr[2]) - filetime_to_int(prev[2])
    
    total = kernel_diff + user_diff
    if total == 0:
        return 0.5
    
    cpu = 1.0 - (idle_diff / total)
    return max(0.0, min(1.0, cpu))

# ============================================================
# GPU MONITORING (NVIDIA)
# ============================================================

def get_gpu_stats():
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=utilization.gpu,temperature.gpu,power.draw',
             '--format=csv,noheader,nounits'],
            capture_output=True, text=True, timeout=5,
            startupinfo=startupinfo
        )
        
        if result.returncode == 0:
            parts = result.stdout.strip().split(',')
            if len(parts) >= 3:
                return {
                    'util': float(parts[0].strip()) / 100.0,
                    'temp': float(parts[1].strip()),
                    'power': float(parts[2].strip())
                }
    except:
        pass
    return None

# ============================================================
# COHERENCE CALCULATIONS
# ============================================================

def calc_s5(cpu_load):
    """CPU coherence - best at 50% load"""
    return 1.0 - abs(cpu_load - 0.5) * 2

def calc_s6(gpu):
    """GPU coherence - optimal 40-80% util, cool temps"""
    if not gpu:
        return None
    
    util = gpu['util']
    temp = gpu['temp']
    
    # Utilization score
    if 0.4 <= util <= 0.8:
        util_score = 1.0
    elif util < 0.4:
        util_score = util / 0.4
    else:
        util_score = 1.0 - (util - 0.8) / 0.2
    
    # Temperature score
    if temp < 70:
        temp_score = 1.0
    elif temp < 85:
        temp_score = 1.0 - (temp - 70) / 15
    else:
        temp_score = 0.2
    
    return max(0.0, min(1.0, util_score * 0.6 + temp_score * 0.4))

def calc_combined(s5, s6):
    """Combined S* - weight GPU more for gaming rig"""
    if s6 is not None:
        return s5 * 0.4 + s6 * 0.6
    return s5

# ============================================================
# TZOLKIN BREATH
# ============================================================

WINDOWS = {0: "RESET", 5: "REDOX_DEEP", 7: "HARMONY", 12: "HARVEST"}

class Breath:
    def __init__(self):
        self.phase = 0
        self.cycle = 0
        self.gate_open = True
        self.last_change = time.time()
        self.open_time = 4.0
        self.close_time = 4.0
    
    def update(self):
        now = time.time()
        elapsed = now - self.last_change
        event = None
        
        if self.gate_open and elapsed >= self.open_time:
            self.gate_open = False
            self.last_change = now
            event = "CLOSE"
        elif not self.gate_open and elapsed >= self.close_time:
            self.gate_open = True
            self.phase = (self.phase + 1) % 13
            if self.phase == 0:
                self.cycle += 1
            self.last_change = now
            event = "OPEN"
        
        return event
    
    def window_name(self):
        return WINDOWS.get(self.phase, "")

# ============================================================
# LOGGING
# ============================================================

def log(name, msg):
    path = CRYSTALOS_LOGS / f"{name}.log"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
    except:
        pass

def save_state(data):
    path = CRYSTALOS_STATE / "current.json"
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass

# ============================================================
# MAIN
# ============================================================

def main():
    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW("CRYSTALOS - Dell Aurora R16")
    
    print("")
    print("=" * 64)
    print("  CRYSTALOS - TIG Engine for Dell Aurora R16")
    print("=" * 64)
    print(f"  CPU Cores: {os.cpu_count()}")
    
    gpu = get_gpu_stats()
    has_gpu = gpu is not None
    print(f"  GPU: {'RTX 4070 DETECTED' if has_gpu else 'Not detected'}")
    print(f"  Threshold: 0.7")
    print(f"  Logs: {CRYSTALOS_LOGS}")
    print("=" * 64)
    print("  Press Ctrl+C to stop")
    print("=" * 64)
    print("")
    
    log("crystalos", f"CRYSTALOS started - {os.cpu_count()} cores, GPU={'yes' if has_gpu else 'no'}")
    
    breath = Breath()
    fire_count = 0
    phase_fires = Counter()
    tau = 0.7
    
    prev_cpu = get_cpu_times()
    time.sleep(0.1)
    
    try:
        while True:
            # CPU
            curr_cpu = get_cpu_times()
            cpu_load = calc_cpu_percent(prev_cpu, curr_cpu)
            prev_cpu = curr_cpu
            s5 = calc_s5(cpu_load)
            
            # GPU
            gpu = get_gpu_stats() if has_gpu else None
            s6 = calc_s6(gpu)
            
            # Combined
            s_star = calc_combined(s5, s6)
            
            # Breath
            event = breath.update()
            if event:
                window = breath.window_name()
                if window:
                    log("breath", f">>> WINDOW: {window} (phase {breath.phase}/13)")
                else:
                    state = "OPEN" if breath.gate_open else "CLOSED"
                    log("breath", f"Gate {state} (phase {breath.phase}/13)")
            
            # Save state
            state = {
                "cpu": round(cpu_load, 3),
                "s5": round(s5, 3),
                "s6": round(s6, 3) if s6 else None,
                "s_star": round(s_star, 3),
                "phase": breath.phase,
                "gate": breath.gate_open,
                "window": breath.window_name(),
                "fires": fire_count
            }
            if gpu:
                state["gpu_util"] = round(gpu['util'], 3)
                state["gpu_temp"] = gpu['temp']
                state["gpu_power"] = round(gpu['power'], 1)
            save_state(state)
            
            # Fire logic
            fired = False
            if breath.gate_open and s_star >= tau:
                fire_count += 1
                phase_fires[breath.phase] += 1
                fired = True
                
                window = breath.window_name()
                w_str = f" [{window}]" if window else ""
                log("fires", f"FIRE #{fire_count}: S*={s_star:.3f} phase={breath.phase}/13{w_str}")
                
                if fire_count % 50 == 0:
                    log("fires", f"  Distribution: {dict(phase_fires)}")
            
            # Console output
            icon = ">>>" if fired else "   "
            window = breath.window_name()
            w_str = f" [{window}]" if window else ""
            
            if gpu:
                gpu_str = f" GPU:{gpu['util']*100:3.0f}%/{gpu['temp']:.0f}C"
            else:
                gpu_str = ""
            
            gate_str = "OPEN" if breath.gate_open else "----"
            
            line = f"\r{icon} Phase {breath.phase:2d}/13{w_str:12s} | CPU:{cpu_load*100:5.1f}% S5:{s5:.2f}{gpu_str} | S*:{s_star:.2f} | {gate_str} | Fires:{fire_count:4d}"
            print(line, end="", flush=True)
            
            time.sleep(1.0)
            
    except KeyboardInterrupt:
        print("\n\nStopping CRYSTALOS...")
        log("crystalos", f"Stopped. Total fires: {fire_count}")
        
        # Final stats
        print("\n" + "=" * 64)
        print("FINAL STATS")
        print("=" * 64)
        print(f"Total fires: {fire_count}")
        print(f"Cycles completed: {breath.cycle}")
        print(f"Phase distribution: {dict(phase_fires)}")
        
        if fire_count > 0:
            print("\nTop phases:")
            for phase, count in phase_fires.most_common(5):
                pct = count / fire_count * 100
                window = WINDOWS.get(phase, "")
                w_str = f" [{window}]" if window else ""
                print(f"  Phase {phase}{w_str}: {count} ({pct:.1f}%)")
        
        print("=" * 64)

# ============================================================
# ANALYZE FUNCTION
# ============================================================

def analyze():
    print("")
    print("=" * 64)
    print("  CRYSTALOS FIRE ANALYSIS")
    print("=" * 64)
    
    log_path = CRYSTALOS_LOGS / "fires.log"
    if not log_path.exists():
        print(f"\nNo fire log found at: {log_path}")
        print("Run CRYSTALOS first to generate data.")
        return
    
    fires = []
    with open(log_path, encoding="utf-8") as f:
        for line in f:
            if "FIRE #" in line:
                try:
                    parts = line.split("FIRE #")[1]
                    num = int(parts.split(":")[0])
                    s_star = float(parts.split("S*=")[1].split()[0])
                    phase = int(parts.split("phase=")[1].split("/")[0])
                    fires.append({"num": num, "s": s_star, "phase": phase})
                except:
                    pass
    
    if not fires:
        print("\nNo fires found in log.")
        return
    
    total = len(fires)
    print(f"\nTotal fires: {total}")
    
    phase_counts = Counter(f['phase'] for f in fires)
    expected = total / 13
    
    print("\nPhase Distribution:")
    print("-" * 50)
    
    for phase in range(13):
        count = phase_counts.get(phase, 0)
        pct = count / total * 100 if total > 0 else 0
        exp_pct = 100 / 13
        dev = pct - exp_pct
        
        bar = "#" * int(pct / 2)
        window = WINDOWS.get(phase, "")
        w_str = f" [{window}]" if window else ""
        
        if dev > 2:
            marker = " +"
        elif dev < -2:
            marker = " -"
        else:
            marker = ""
        
        print(f"  {phase:2d}{w_str:14s}: {bar:<25} {count:4d} ({pct:5.1f}%){marker}")
    
    print(f"\nExpected if uniform: 7.7% per phase")
    
    # Chi-square
    chi2 = sum((phase_counts.get(p, 0) - expected) ** 2 / expected for p in range(13))
    
    print(f"\nChi-square test:")
    print(f"  X2 = {chi2:.2f}, df = 12")
    if chi2 > 26.22:
        print(f"  p < 0.01 - HIGHLY SIGNIFICANT")
    elif chi2 > 21.03:
        print(f"  p < 0.05 - SIGNIFICANT")
    else:
        print(f"  p > 0.05 - Not significant")
    
    # HARMONY
    h_count = phase_counts.get(7, 0)
    h_pct = h_count / total * 100 if total > 0 else 0
    print(f"\nHARMONY (phase 7): {h_count} fires ({h_pct:.1f}%)")
    
    # 24-core analysis
    print("\n24-Core Geometry:")
    pairs = [("2x12", [2, 12]), ("4x6", [4, 6]), ("3x8", [3, 8])]
    for name, phases in pairs:
        combined = sum(phase_counts.get(p, 0) for p in phases)
        pct = combined / total * 100 if total > 0 else 0
        print(f"  {name} (phases {phases[0]},{phases[1]}): {pct:.1f}%")
    
    print("=" * 64)

# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "analyze":
        analyze()
        input("\nPress Enter to close...")
    else:
        main()
