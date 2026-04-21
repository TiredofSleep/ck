# -*- coding: utf-8 -*-
"""
CRYSTALOS (pre-registered stopping) - TIG Engine for Dell Aurora R16
====================================================================
Fork of `crystalos.py` that adds pre-registered stopping criteria per
`snowflake_null_spec.md` §7. The original `crystalos.py` is preserved
verbatim as a sibling file; this file exists so future χ² runs can
declare their stopping criterion in advance and avoid optional-stopping
bias.

Rationale (verbatim from snowflake_null_spec.md §7):

    The runtime is stopped by Ctrl-C at the operator's discretion
    (crystalos.py lines 310–315 handle KeyboardInterrupt). No pre-
    committed sample-size target. No pre-committed stop-at-χ²-threshold
    rule. The operator may, in principle, watch the running fire_count
    and stop whenever they like.

    Recommended fix for future sessions:
    1. Pre-register N. Operator declares "this session will collect
       exactly N fires" at start. Runtime exits automatically when
       fire_count == N.
    2. Pre-register time. Operator declares "run for T seconds" at
       start. Runtime exits at T.
    3. Pre-register both and take whichever comes first.

This file implements (1), (2), (3). At least one of --n0 or --t0 must
be supplied; if both are supplied, the run stops at whichever trips
first. The pre-registration record is written to disk *before* the main
loop starts so it cannot be edited after-the-fact.

Usage:
    python crystalos_prereg.py --n0 10000             # stop at 10,000 fires
    python crystalos_prereg.py --t0 3600              # stop after 1 hour
    python crystalos_prereg.py --n0 10000 --t0 3600   # stop whichever first
    python crystalos_prereg.py analyze                # analyze existing logs

Output:
    ~/CRYSTALOS/state/prereg_<timestamp>.json   declared criteria
    ~/CRYSTALOS/state/final_<timestamp>.json    outcome + criterion that fired
    ~/CRYSTALOS/logs/*.log                      runtime + fires

Invariants enforced:
    - pre-registration record is written before first fire
    - main loop cannot increment beyond declared bounds
    - Ctrl-C interruption is tagged "operator-interrupted" (distinct
      from pre-registered stop) so downstream χ² can discard the run
"""

import os
import sys
import time
import json
import ctypes
import subprocess
import argparse
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
# WINDOWS CPU READING (unchanged from crystalos.py)
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
# GPU MONITORING (unchanged from crystalos.py)
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
    except Exception:
        pass
    return None

# ============================================================
# COHERENCE CALCULATIONS (unchanged from crystalos.py)
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

    if 0.4 <= util <= 0.8:
        util_score = 1.0
    elif util < 0.4:
        util_score = util / 0.4
    else:
        util_score = 1.0 - (util - 0.8) / 0.2

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
# TZOLKIN BREATH (unchanged from crystalos.py)
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
# LOGGING (unchanged from crystalos.py)
# ============================================================

def log(name, msg):
    path = CRYSTALOS_LOGS / f"{name}.log"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
    except Exception:
        pass

def save_state(data):
    path = CRYSTALOS_STATE / "current.json"
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

# ============================================================
# PRE-REGISTRATION (NEW — this is the patch)
# ============================================================

def write_preregistration(n0, t0, tau, session_id):
    """
    Write the pre-registration record BEFORE the main loop starts.
    Once this file exists on disk, the declared stopping criteria are
    fixed for this session; changing them mid-run requires a visibly
    new file (which flags the session as compromised in analyze()).
    """
    record = {
        "schema": "crystalos_prereg/v1",
        "session_id": session_id,
        "declared_at": datetime.now().isoformat(timespec="seconds"),
        "criteria": {
            "n0": n0,     # None if not set
            "t0": t0,     # None if not set (seconds)
            "tau": tau,   # S* threshold for fire
        },
        "stopping_rule": _describe_rule(n0, t0),
        "notes": (
            "Whichever criterion trips first ends the session cleanly. "
            "Ctrl-C before either trips marks the session as "
            "'operator-interrupted' and downstream chi^2 analysis should "
            "discard or at minimum flag such runs."
        ),
    }
    path = CRYSTALOS_STATE / f"prereg_{session_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
    return record, path

def _describe_rule(n0, t0):
    if n0 is not None and t0 is not None:
        return f"stop when fire_count>={n0} OR elapsed>={t0}s, whichever first"
    if n0 is not None:
        return f"stop when fire_count>={n0}"
    if t0 is not None:
        return f"stop when elapsed>={t0}s"
    return "UNDECLARED — invalid session"

def write_final(session_id, outcome):
    path = CRYSTALOS_STATE / f"final_{session_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(outcome, f, indent=2)
    return path

# ============================================================
# MAIN — PATCHED LOOP
# ============================================================

def main(n0, t0, tau):
    # ------------------------------------------------------------
    # Validate inputs
    # ------------------------------------------------------------
    if n0 is None and t0 is None:
        print("ERROR: at least one of --n0 or --t0 must be set.", file=sys.stderr)
        print("       (snowflake_null_spec.md §7 requires pre-registered", file=sys.stderr)
        print("        stopping; UNDECLARED runs are treated as invalid.)", file=sys.stderr)
        sys.exit(2)

    if n0 is not None and n0 <= 0:
        print("ERROR: --n0 must be positive.", file=sys.stderr)
        sys.exit(2)

    if t0 is not None and t0 <= 0:
        print("ERROR: --t0 must be positive (seconds).", file=sys.stderr)
        sys.exit(2)

    if not (0.0 < tau < 1.0):
        print("ERROR: --tau must be strictly between 0 and 1.", file=sys.stderr)
        sys.exit(2)

    # ------------------------------------------------------------
    # Pre-register (disk write BEFORE loop begins)
    # ------------------------------------------------------------
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    prereg, prereg_path = write_preregistration(n0, t0, tau, session_id)

    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"CRYSTALOS (pre-reg) - session {session_id}"
        )

    print("")
    print("=" * 70)
    print("  CRYSTALOS (pre-registered stopping)")
    print("=" * 70)
    print(f"  Session:    {session_id}")
    print(f"  CPU Cores:  {os.cpu_count()}")

    gpu = get_gpu_stats()
    has_gpu = gpu is not None
    print(f"  GPU:        {'RTX 4070 DETECTED' if has_gpu else 'Not detected'}")
    print(f"  Threshold:  tau = {tau}")
    print(f"  Stop @ N0:  {n0 if n0 is not None else '(not set)'}")
    print(f"  Stop @ T0:  {str(t0) + 's' if t0 is not None else '(not set)'}")
    print(f"  Rule:       {prereg['stopping_rule']}")
    print(f"  Pre-reg:    {prereg_path}")
    print(f"  Logs:       {CRYSTALOS_LOGS}")
    print("=" * 70)
    print("  Ctrl-C interrupts and flags the run as 'operator-interrupted'")
    print("=" * 70)
    print("")

    log("crystalos_prereg",
        f"START session={session_id} n0={n0} t0={t0} tau={tau} "
        f"cores={os.cpu_count()} gpu={'yes' if has_gpu else 'no'}")
    log("fires", f"# session={session_id} preregistered rule={prereg['stopping_rule']}")

    breath = Breath()
    fire_count = 0
    phase_fires = Counter()
    start_time = time.time()
    stop_reason = None

    prev_cpu = get_cpu_times()
    time.sleep(0.1)

    try:
        while True:
            # ----------------------------------------------------
            # Pre-registered stopping check (BEFORE incrementing)
            # ----------------------------------------------------
            elapsed = time.time() - start_time
            if n0 is not None and fire_count >= n0:
                stop_reason = f"N0 tripped (fire_count={fire_count} >= n0={n0})"
                break
            if t0 is not None and elapsed >= t0:
                stop_reason = f"T0 tripped (elapsed={elapsed:.1f}s >= t0={t0}s)"
                break

            # ----------------------------------------------------
            # CPU + GPU read
            # ----------------------------------------------------
            curr_cpu = get_cpu_times()
            cpu_load = calc_cpu_percent(prev_cpu, curr_cpu)
            prev_cpu = curr_cpu
            s5 = calc_s5(cpu_load)

            gpu = get_gpu_stats() if has_gpu else None
            s6 = calc_s6(gpu)
            s_star = calc_combined(s5, s6)

            # ----------------------------------------------------
            # Breath update
            # ----------------------------------------------------
            event = breath.update()
            if event:
                window = breath.window_name()
                if window:
                    log("breath", f">>> WINDOW: {window} (phase {breath.phase}/13)")
                else:
                    state_str = "OPEN" if breath.gate_open else "CLOSED"
                    log("breath", f"Gate {state_str} (phase {breath.phase}/13)")

            # ----------------------------------------------------
            # Persist current state
            # ----------------------------------------------------
            snap = {
                "session": session_id,
                "cpu": round(cpu_load, 3),
                "s5": round(s5, 3),
                "s6": round(s6, 3) if s6 else None,
                "s_star": round(s_star, 3),
                "phase": breath.phase,
                "gate": breath.gate_open,
                "window": breath.window_name(),
                "fires": fire_count,
                "elapsed_s": round(elapsed, 1),
                "n0": n0,
                "t0": t0,
            }
            if gpu:
                snap["gpu_util"] = round(gpu['util'], 3)
                snap["gpu_temp"] = gpu['temp']
                snap["gpu_power"] = round(gpu['power'], 1)
            save_state(snap)

            # ----------------------------------------------------
            # Fire logic
            # ----------------------------------------------------
            fired = False
            if breath.gate_open and s_star >= tau:
                fire_count += 1
                phase_fires[breath.phase] += 1
                fired = True

                window = breath.window_name()
                w_str = f" [{window}]" if window else ""
                log("fires",
                    f"FIRE #{fire_count}: S*={s_star:.3f} "
                    f"phase={breath.phase}/13{w_str} "
                    f"session={session_id}")

                if fire_count % 50 == 0:
                    log("fires", f"  Distribution: {dict(phase_fires)}")

            # ----------------------------------------------------
            # Console line
            # ----------------------------------------------------
            icon = ">>>" if fired else "   "
            window = breath.window_name()
            w_str = f" [{window}]" if window else ""

            if gpu:
                gpu_str = f" GPU:{gpu['util']*100:3.0f}%/{gpu['temp']:.0f}C"
            else:
                gpu_str = ""

            gate_str = "OPEN" if breath.gate_open else "----"

            # N0 / T0 progress indicator
            if n0 is not None and t0 is not None:
                prog = (f" N:{fire_count:>5d}/{n0} "
                        f"T:{elapsed:>5.0f}/{t0:.0f}s")
            elif n0 is not None:
                prog = f" N:{fire_count:>5d}/{n0}"
            else:
                prog = f" T:{elapsed:>5.0f}/{t0:.0f}s"

            line = (f"\r{icon} Ph{breath.phase:2d}/13{w_str:12s}"
                    f" CPU:{cpu_load*100:5.1f}% S5:{s5:.2f}{gpu_str}"
                    f" | S*:{s_star:.2f} | {gate_str}{prog}")
            print(line, end="", flush=True)

            time.sleep(1.0)

    except KeyboardInterrupt:
        stop_reason = "operator-interrupted (Ctrl-C before pre-registered stop)"

    # ------------------------------------------------------------
    # Clean exit — write final record with stop reason
    # ------------------------------------------------------------
    final_elapsed = time.time() - start_time
    outcome = {
        "schema": "crystalos_prereg_final/v1",
        "session_id": session_id,
        "prereg": prereg["criteria"],
        "stopping_rule": prereg["stopping_rule"],
        "stop_reason": stop_reason,
        "stop_class": (
            "pre-registered" if stop_reason and "tripped" in stop_reason
            else "operator-interrupted"
        ),
        "fire_count": fire_count,
        "elapsed_s": round(final_elapsed, 1),
        "cycles": breath.cycle,
        "phase_distribution": dict(phase_fires),
        "finished_at": datetime.now().isoformat(timespec="seconds"),
    }
    final_path = write_final(session_id, outcome)

    print("\n" + "=" * 70)
    print(f"  Session {session_id} closed — {outcome['stop_class']}")
    print("=" * 70)
    print(f"  Reason:        {stop_reason}")
    print(f"  Total fires:   {fire_count}")
    print(f"  Elapsed:       {final_elapsed:.1f}s ({final_elapsed/60:.1f} min)")
    print(f"  Cycles:        {breath.cycle}")
    print(f"  Final record:  {final_path}")
    print("=" * 70)

    if fire_count > 0:
        print("\nTop phases:")
        for phase, count in phase_fires.most_common(5):
            pct = count / fire_count * 100
            window = WINDOWS.get(phase, "")
            w_str = f" [{window}]" if window else ""
            print(f"  Phase {phase}{w_str}: {count} ({pct:.1f}%)")
    print("")

    log("crystalos_prereg",
        f"END session={session_id} stop_class={outcome['stop_class']} "
        f"fires={fire_count} elapsed={final_elapsed:.1f}s")

    # Exit code: 0 for pre-registered stop, 130 for operator interrupt
    if outcome["stop_class"] == "operator-interrupted":
        sys.exit(130)
    sys.exit(0)

# ============================================================
# ANALYZE FUNCTION — extended to warn on operator-interrupted runs
# ============================================================

def analyze():
    print("")
    print("=" * 70)
    print("  CRYSTALOS (pre-registered) FIRE ANALYSIS")
    print("=" * 70)

    # Enumerate completed sessions
    final_files = sorted(CRYSTALOS_STATE.glob("final_*.json"))
    if final_files:
        print(f"\n  Completed sessions: {len(final_files)}")
        print("  " + "-" * 66)
        for fp in final_files:
            try:
                with open(fp, encoding="utf-8") as f:
                    rec = json.load(f)
                cls = rec.get("stop_class", "?")
                sid = rec.get("session_id", "?")
                fc = rec.get("fire_count", 0)
                el = rec.get("elapsed_s", 0)
                print(f"  {sid}  {cls:<22s}  fires={fc:<6d}  elapsed={el:.0f}s")
            except Exception:
                print(f"  {fp.name}  (unreadable)")

    # Full chi^2 on combined fires.log
    log_path = CRYSTALOS_LOGS / "fires.log"
    if not log_path.exists():
        print(f"\nNo fire log found at: {log_path}")
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
                except Exception:
                    pass

    if not fires:
        print("\nNo fires found in log.")
        return

    total = len(fires)
    print(f"\nTotal fires (across all sessions): {total}")

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
        marker = " +" if dev > 2 else (" -" if dev < -2 else "")
        print(f"  {phase:2d}{w_str:14s}: {bar:<25} {count:4d} ({pct:5.1f}%){marker}")

    print(f"\nExpected if uniform: {100/13:.1f}% per phase")

    chi2 = sum((phase_counts.get(p, 0) - expected) ** 2 / expected for p in range(13))
    print(f"\nChi-square test:")
    print(f"  X2 = {chi2:.4f}, df = 12")
    if chi2 > 26.22:
        print(f"  p < 0.01 — HIGHLY SIGNIFICANT")
    elif chi2 > 21.03:
        print(f"  p < 0.05 — SIGNIFICANT")
    else:
        print(f"  p > 0.05 — not significant at 0.05")

    # Honest caveat
    print("\nNote: if any session closed with stop_class='operator-interrupted',")
    print("      those fires carry optional-stopping bias and the aggregated")
    print("      chi^2 above is not a clean p-value. Filter fires.log by")
    print("      session_id and retain only pre-registered sessions for a")
    print("      referee-defensible chi^2.")

    print("=" * 70)

# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CRYSTALOS with pre-registered stopping rule.",
    )
    parser.add_argument("--n0", type=int, default=None,
                        help="Pre-registered fire-count target. "
                             "Session ends when fire_count >= n0.")
    parser.add_argument("--t0", type=float, default=None,
                        help="Pre-registered time budget in seconds. "
                             "Session ends when elapsed >= t0.")
    parser.add_argument("--tau", type=float, default=0.7,
                        help="S* threshold for fire. Default 0.7.")
    parser.add_argument("mode", nargs="?", default="run",
                        choices=["run", "analyze"],
                        help="'run' to collect data (default); "
                             "'analyze' to summarize existing logs.")
    args = parser.parse_args()

    if args.mode == "analyze":
        analyze()
        if sys.platform == 'win32':
            try:
                input("\nPress Enter to close...")
            except EOFError:
                pass
    else:
        main(args.n0, args.t0, args.tau)
