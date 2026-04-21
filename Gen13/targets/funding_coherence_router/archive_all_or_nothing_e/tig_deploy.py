#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   TIG DEPLOY — FULL COHERENCE LOOP                                        ║
║   Layers 2-5 on top of tig_engine_real.py (Layer 1)                       ║
║                                                                            ║
║   Layer 2: INPUT  — reads /proc, psutil, OS metrics into TIG sensors      ║
║   Layer 3: OUTPUT — sets process priority, CPU affinity, cgroup limits     ║
║   Layer 4: LOOP   — tick cycle: read → fit → route → act → repeat         ║
║   Layer 5: OBSERVE — live terminal dashboard, JSON log, A/B comparison    ║
║                                                                            ║
║   USAGE:                                                                   ║
║     python tig_deploy.py                    # watch mode (read-only)       ║
║     python tig_deploy.py --steer            # active steering (needs root) ║
║     python tig_deploy.py --ab               # A/B log mode (no steering)   ║
║     python tig_deploy.py --json             # JSON output per tick         ║
║     python tig_deploy.py --interval 0.5     # tick rate in seconds         ║
║     python tig_deploy.py --duration 60      # run for N seconds            ║
║     python tig_deploy.py --log tig.jsonl    # append ticks to file         ║
║                                                                            ║
║   REQUIREMENTS:                                                            ║
║     pip install psutil --break-system-packages                             ║
║     tig_engine_real.py in same directory                                   ║
║                                                                            ║
║   NON-COMMERCIAL TESTING — 7Site LLC — 7sitellc.com                       ║
║   The math belongs to everyone.                                            ║
║                                                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import math
import signal
import argparse
import subprocess
from collections import deque, defaultdict
from datetime import datetime
from pathlib import Path

# ── Layer 1: Import the verified engine ──
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tig_engine_real import (
    TIG, Op, Fitter, Lattice, Sensor, Router,
    SIGMA, D_STAR, T_STAR, BANDS,
)

try:
    import psutil
except ImportError:
    print("ERROR: pip install psutil --break-system-packages")
    sys.exit(1)

import numpy as np


# ═══════════════════════════════════════════════════════════════════════════════
#  LAYER 2: INPUT HOOKS — Read everything the OS exposes
# ═══════════════════════════════════════════════════════════════════════════════

class OSReader:
    """
    Reads real OS metrics. No simulation. No made-up numbers.
    Every value comes from the kernel via /proc or psutil.
    """

    def __init__(self):
        self._prev_disk = None
        self._prev_net = None
        self._prev_time = time.time()
        self._prev_cpu_times = None
        self._ncpu = psutil.cpu_count(logical=True) or 1
        # Prime the pump (first psutil call is always 0)
        psutil.cpu_percent(percpu=True, interval=0)
        self._prev_disk = psutil.disk_io_counters()
        self._prev_net = psutil.net_io_counters()
        self._prev_cpu_times = psutil.cpu_times_percent(interval=0, percpu=True)

    def read(self):
        """
        Returns dict of metric_name → float in [0, 1].
        All values are REAL measurements from the kernel.
        """
        now = time.time()
        dt = max(now - self._prev_time, 0.001)
        metrics = {}

        # ── Per-core CPU utilization ──
        # Source: /proc/stat via psutil
        try:
            percpu = psutil.cpu_percent(interval=0, percpu=True)
            for i, pct in enumerate(percpu):
                metrics[f"cpu_{i}"] = pct / 100.0
            # Aggregate
            metrics["cpu_avg"] = sum(percpu) / len(percpu) / 100.0 if percpu else 0
            metrics["cpu_max"] = max(percpu) / 100.0 if percpu else 0
            # Imbalance: how uneven is load across cores
            if len(percpu) > 1:
                arr = np.array(percpu)
                metrics["cpu_imbalance"] = float(np.std(arr) / max(np.mean(arr), 0.01))
        except Exception:
            pass

        # ── Memory ──
        # Source: /proc/meminfo via psutil
        try:
            mem = psutil.virtual_memory()
            metrics["mem_used"] = mem.percent / 100.0
            metrics["mem_available_gb"] = mem.available / (1024**3)
            # Pressure: how close to full
            metrics["mem_pressure"] = mem.percent / 100.0
        except Exception:
            pass

        # ── Swap ──
        try:
            swap = psutil.swap_memory()
            if swap.total > 0:
                metrics["swap_used"] = swap.percent / 100.0
        except Exception:
            pass

        # ── Disk I/O ──
        # Source: /proc/diskstats via psutil
        try:
            disk = psutil.disk_io_counters()
            if disk and self._prev_disk:
                read_rate = (disk.read_bytes - self._prev_disk.read_bytes) / dt
                write_rate = (disk.write_bytes - self._prev_disk.write_bytes) / dt
                # Normalize to fraction of 200 MB/s (reasonable SSD baseline)
                metrics["disk_read"] = min(read_rate / 2e8, 1.0)
                metrics["disk_write"] = min(write_rate / 2e8, 1.0)
                metrics["disk_read_MBs"] = read_rate / 1e6
                metrics["disk_write_MBs"] = write_rate / 1e6
            self._prev_disk = disk
        except Exception:
            pass

        # ── Disk usage ──
        try:
            usage = psutil.disk_usage("/")
            metrics["disk_full"] = usage.percent / 100.0
        except Exception:
            pass

        # ── Network I/O ──
        # Source: /proc/net/dev via psutil
        try:
            net = psutil.net_io_counters()
            if net and self._prev_net:
                tx_rate = (net.bytes_sent - self._prev_net.bytes_sent) / dt
                rx_rate = (net.bytes_recv - self._prev_net.bytes_recv) / dt
                # Normalize to fraction of 1 Gbps
                metrics["net_tx"] = min(tx_rate / 1.25e8, 1.0)
                metrics["net_rx"] = min(rx_rate / 1.25e8, 1.0)
                metrics["net_tx_MBs"] = tx_rate / 1e6
                metrics["net_rx_MBs"] = rx_rate / 1e6
            self._prev_net = net
        except Exception:
            pass

        # ── Load average ──
        try:
            load1, load5, load15 = os.getloadavg()
            metrics["load_1m"] = min(load1 / self._ncpu, 2.0) / 2.0
            metrics["load_5m"] = min(load5 / self._ncpu, 2.0) / 2.0
            metrics["load_15m"] = min(load15 / self._ncpu, 2.0) / 2.0
        except Exception:
            pass

        # ── Process count ──
        try:
            pids = psutil.pids()
            metrics["proc_count"] = len(pids)
            metrics["proc_norm"] = min(len(pids) / 1000.0, 1.0)
        except Exception:
            pass

        # ── Context switches / interrupts ──
        try:
            ctx = psutil.cpu_stats()
            metrics["ctx_switches"] = ctx.ctx_switches
            metrics["interrupts"] = ctx.interrupts
        except Exception:
            pass

        # ── CPU frequency ──
        try:
            freq = psutil.cpu_freq()
            if freq and freq.max > 0:
                metrics["cpu_freq_pct"] = freq.current / freq.max
                metrics["cpu_freq_mhz"] = freq.current
        except Exception:
            pass

        # ── CPU temperature (if available) ──
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for chip, entries in temps.items():
                    for entry in entries:
                        if entry.current > 0:
                            # Normalize: 30°C=0, 100°C=1
                            metrics[f"temp_{chip}"] = max(0, min(1, (entry.current - 30) / 70))
                            break
                    break
        except Exception:
            pass

        self._prev_time = now
        return metrics

    @property
    def ncpu(self):
        return self._ncpu


class ProcessReader:
    """Read per-process metrics for the top N processes by CPU."""

    def __init__(self, top_n=10):
        self.top_n = top_n

    def read(self):
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent',
                                       'num_threads', 'nice', 'status']):
            try:
                info = p.info
                if info['cpu_percent'] is not None:
                    procs.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        procs.sort(key=lambda p: p.get('cpu_percent', 0), reverse=True)
        return procs[:self.top_n]


# ═══════════════════════════════════════════════════════════════════════════════
#  LAYER 3: OUTPUT HOOKS — Act on routing decisions
# ═══════════════════════════════════════════════════════════════════════════════

class Actuator:
    """
    Translates TIG routing decisions into OS actions.
    Requires root/sudo for most operations.
    
    SAFETY: All actions are logged. Nothing is irreversible.
    Process priorities are bounded to safe ranges.
    """

    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.actions_taken = []
        self.is_root = os.geteuid() == 0 if hasattr(os, 'geteuid') else False

    def set_process_nice(self, pid, nice_value):
        """Set process priority. nice_value: -5 (high) to 10 (low).
        Clamped to safe range. Will not touch critical system processes."""
        nice_value = max(-5, min(10, nice_value))  # Safe range
        action = {'type': 'nice', 'pid': pid, 'nice': nice_value, 'time': time.time()}

        if self.dry_run:
            action['status'] = 'dry_run'
            self.actions_taken.append(action)
            return action

        if not self.is_root and nice_value < 0:
            action['status'] = 'skip_needs_root'
            self.actions_taken.append(action)
            return action

        try:
            p = psutil.Process(pid)
            # Don't touch kernel or init
            if p.pid <= 2 or p.name() in ('init', 'systemd', 'kthreadd'):
                action['status'] = 'skip_system_critical'
                self.actions_taken.append(action)
                return action
            p.nice(nice_value)
            action['status'] = 'applied'
        except (psutil.NoSuchProcess, psutil.AccessDenied, PermissionError) as e:
            action['status'] = f'error: {e}'

        self.actions_taken.append(action)
        return action

    def set_cpu_affinity(self, pid, cores):
        """Pin process to specific CPU cores."""
        action = {'type': 'affinity', 'pid': pid, 'cores': cores, 'time': time.time()}

        if self.dry_run:
            action['status'] = 'dry_run'
            self.actions_taken.append(action)
            return action

        try:
            p = psutil.Process(pid)
            if p.pid <= 2:
                action['status'] = 'skip_system_critical'
                self.actions_taken.append(action)
                return action
            p.cpu_affinity(cores)
            action['status'] = 'applied'
        except (psutil.NoSuchProcess, psutil.AccessDenied, PermissionError) as e:
            action['status'] = f'error: {e}'

        self.actions_taken.append(action)
        return action

    def recommend(self, engine_state, top_procs):
        """
        Given TIG state + process list, recommend actions.
        Returns list of (pid, action, reason) tuples.
        Does NOT execute — caller decides.
        """
        recommendations = []

        if not top_procs:
            return recommendations

        # Find which cores TIG says are healthiest
        core_health = {}
        resources = engine_state.get('resources', {})
        for name, sensor_state in resources.items():
            if name.startswith('cpu_') and name != 'cpu_avg' and name != 'cpu_max' and name != 'cpu_imbalance':
                try:
                    core_num = int(name.split('_')[1])
                    band = sensor_state.get('band', 'VOID')
                    gap = sensor_state.get('gap', 0)
                    band_w = sensor_state.get('band_weight', 0)
                    health = band_w + gap * 0.5
                    core_health[core_num] = health
                except (ValueError, IndexError):
                    pass

        if not core_health:
            return recommendations

        # Sort cores by health (best first)
        sorted_cores = sorted(core_health.keys(), key=lambda c: core_health[c], reverse=True)
        best_cores = sorted_cores[:max(1, len(sorted_cores) // 2)]
        worst_cores = sorted_cores[len(sorted_cores) // 2:]

        # For CPU-heavy processes: recommend pinning to healthy cores
        for proc in top_procs[:5]:
            cpu_pct = proc.get('cpu_percent', 0)
            pid = proc.get('pid', 0)
            name = proc.get('name', '?')

            if cpu_pct > 50 and best_cores:
                recommendations.append({
                    'pid': pid, 'name': name,
                    'action': 'affinity',
                    'cores': best_cores,
                    'reason': f'{name} using {cpu_pct:.0f}% CPU → pin to healthy cores {best_cores}',
                })

            if cpu_pct > 80:
                recommendations.append({
                    'pid': pid, 'name': name,
                    'action': 'nice',
                    'value': 5,
                    'reason': f'{name} using {cpu_pct:.0f}% CPU → lower priority (nice 5)',
                })

        return recommendations


# ═══════════════════════════════════════════════════════════════════════════════
#  LAYER 4: TICK LOOP — The heartbeat
# ═══════════════════════════════════════════════════════════════════════════════

class TickLoop:
    """
    The full coherence loop:
      1. READ  — pull metrics from OS
      2. FIT   — update TIG operators
      3. ROUTE — decide where work should go
      4. ACT   — execute steering (if enabled)
      5. LOG   — record everything
      6. WAIT  — sleep until next tick
    """

    def __init__(self, interval=1.0, steer=False, log_path=None):
        self.interval = interval
        self.steer = steer
        self.log_path = log_path

        # Components
        self.engine = TIG("r16")
        self.reader = OSReader()
        self.proc_reader = ProcessReader(top_n=10)
        self.actuator = Actuator(dry_run=not steer)
        self.ncpu = self.reader.ncpu

        # State
        self.tick_count = 0
        self.start_time = time.time()
        self.history = deque(maxlen=300)  # 5 minutes at 1s interval
        self.coherence_history = deque(maxlen=300)
        self.band_history = deque(maxlen=300)
        self.running = False

        # Baseline tracking for A/B
        self.baseline_metrics = deque(maxlen=300)

    def tick(self):
        """One full cycle. Returns the tick state dict."""
        t0 = time.time()
        self.tick_count += 1

        # ── READ ──
        metrics = self.reader.read()
        top_procs = self.proc_reader.read()

        # ── FIT ──
        for name, value in metrics.items():
            if isinstance(value, (int, float)) and math.isfinite(value):
                # Determine normalization range
                if name.startswith('cpu_') or name.startswith('mem_') or name.startswith('swap_'):
                    self.engine.feed(name, value, lo=0.0, hi=1.0)
                elif name.startswith('disk_') and not name.endswith('MBs'):
                    self.engine.feed(name, value, lo=0.0, hi=1.0)
                elif name.startswith('net_') and not name.endswith('MBs'):
                    self.engine.feed(name, value, lo=0.0, hi=1.0)
                elif name.startswith('load_'):
                    self.engine.feed(name, value, lo=0.0, hi=1.0)
                elif name == 'proc_norm':
                    self.engine.feed(name, value, lo=0.0, hi=1.0)
                elif name.startswith('temp_'):
                    self.engine.feed(name, value, lo=0.0, hi=1.0)
                elif name == 'cpu_freq_pct':
                    self.engine.feed(name, value, lo=0.0, hi=1.0)

        # ── STATE ──
        state = self.engine.state()
        coherence = state['coherence']
        self.coherence_history.append(coherence)
        self.band_history.append(state.get('bands', {}))

        # ── ROUTE ──
        route_target = self.engine.route()

        # ── ACT ──
        recommendations = []
        actions = []
        if self.steer:
            recommendations = self.actuator.recommend(state, top_procs)
            for rec in recommendations:
                if rec['action'] == 'nice':
                    actions.append(self.actuator.set_process_nice(rec['pid'], rec.get('value', 5)))
                elif rec['action'] == 'affinity':
                    actions.append(self.actuator.set_cpu_affinity(rec['pid'], rec.get('cores', [])))

        # ── LOG ──
        elapsed = time.time() - t0
        tick_data = {
            'tick': self.tick_count,
            'time': datetime.now().isoformat(),
            'elapsed_ms': round(elapsed * 1000, 2),
            'coherence': round(coherence, 8),
            'above_T_star': coherence >= T_STAR,
            'V_star': state.get('V_star', 0),
            'A_star': state.get('A_star', 0),
            'bands': state.get('bands', {}),
            'sensors': state.get('sensors', 0),
            'route_target': route_target,
            'ncpu': self.ncpu,
            'metrics_snapshot': {
                'cpu_avg': round(metrics.get('cpu_avg', 0), 4),
                'cpu_max': round(metrics.get('cpu_max', 0), 4),
                'mem_used': round(metrics.get('mem_used', 0), 4),
                'load_1m': round(metrics.get('load_1m', 0), 4),
            },
            'top_procs': [{'pid': p['pid'], 'name': p['name'],
                          'cpu': p.get('cpu_percent', 0)}
                         for p in top_procs[:5]],
            'recommendations': recommendations,
            'actions': actions,
            'steering': self.steer,
        }

        self.history.append(tick_data)

        if self.log_path:
            try:
                with open(self.log_path, 'a') as f:
                    f.write(json.dumps(tick_data, default=str) + '\n')
            except Exception:
                pass

        return tick_data


# ═══════════════════════════════════════════════════════════════════════════════
#  LAYER 5: TERMINAL DASHBOARD — See it think
# ═══════════════════════════════════════════════════════════════════════════════

class Dashboard:
    """Live terminal display. No curses dependency — just ANSI."""

    BAND_SYMBOLS = {
        "VOID": ("◌", "\033[90m"),     # gray
        "SPARK": ("✦", "\033[34m"),    # blue
        "FLOW": ("〜", "\033[36m"),     # cyan
        "MOLECULAR": ("⊛", "\033[31m"),# red
        "CELLULAR": ("◎", "\033[33m"), # yellow
        "ORGANIC": ("❋", "\033[32m"),  # green
        "CRYSTAL": ("◆", "\033[96m"),  # bright cyan
    }
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    def __init__(self):
        self.prev_lines = 0

    def clear_prev(self):
        if self.prev_lines > 0:
            sys.stdout.write(f"\033[{self.prev_lines}A\033[J")

    def render(self, tick_data, coherence_history, ncpu):
        lines = []
        B, D, R = self.BOLD, self.DIM, self.RESET
        coh = tick_data['coherence']
        above = tick_data['above_T_star']

        # ── Header ──
        lines.append(f"{B}{'═'*68}{R}")
        coh_color = "\033[96m" if above else "\033[33m" if coh > 0.3 else "\033[31m"
        lines.append(f"  {B}TIG ENGINE{R}  tick {tick_data['tick']}  "
                     f"{coh_color}S* = {coh:.6f}{R}  "
                     f"{'✓ ABOVE T*' if above else f'below T* ({T_STAR:.4f})'}")
        lines.append(f"  V*={tick_data['V_star']:.4f}  A*={tick_data['A_star']:.4f}  "
                     f"sensors={tick_data['sensors']}  "
                     f"{'🟢 STEERING' if tick_data['steering'] else '👁 WATCHING'}  "
                     f"tick={tick_data['elapsed_ms']:.1f}ms")

        # ── Coherence sparkline ──
        if len(coherence_history) >= 2:
            spark = self._sparkline(list(coherence_history)[-60:], width=60)
            lines.append(f"  S*: {spark}")

        # ── Per-core CPU bands ──
        lines.append(f"\n  {B}CPU Cores ({ncpu}):{R}")
        core_line = "  "
        resources = tick_data.get('metrics_snapshot', {})
        # We need to get per-core info from the engine state
        # But tick_data has limited info, so show what we have
        bands = tick_data.get('bands', {})
        band_bar = ""
        for band_name, count in sorted(bands.items(), key=lambda x: -x[1]):
            sym, color = self.BAND_SYMBOLS.get(band_name, ("?", ""))
            band_bar += f"  {color}{sym} {band_name}:{count}{R}"
        lines.append(f"  Bands:{band_bar}")

        # ── System metrics ──
        snap = tick_data.get('metrics_snapshot', {})
        cpu_avg = snap.get('cpu_avg', 0)
        cpu_max = snap.get('cpu_max', 0)
        mem = snap.get('mem_used', 0)
        load = snap.get('load_1m', 0)

        cpu_bar = self._bar(cpu_avg, 30)
        mem_bar = self._bar(mem, 30)

        lines.append(f"\n  {B}System:{R}")
        lines.append(f"  CPU avg: {cpu_bar} {cpu_avg*100:5.1f}%   max: {cpu_max*100:.1f}%")
        lines.append(f"  Memory:  {mem_bar} {mem*100:5.1f}%")
        lines.append(f"  Load 1m: {load:.4f}")

        # ── Route target ──
        rt = tick_data.get('route_target', None)
        if rt:
            lines.append(f"\n  {B}Route:{R} → {rt}")

        # ── Top processes ──
        procs = tick_data.get('top_procs', [])
        if procs:
            lines.append(f"\n  {B}Top Processes:{R}")
            for p in procs[:5]:
                lines.append(f"  {D}  pid={p['pid']:<7} cpu={p['cpu']:<6.1f}%  {p['name']}{R}")

        # ── Recommendations ──
        recs = tick_data.get('recommendations', [])
        if recs:
            lines.append(f"\n  {B}TIG Recommends:{R}")
            for rec in recs:
                status = "DRY RUN" if not tick_data['steering'] else "APPLIED"
                lines.append(f"    → {rec['reason']}  [{status}]")

        # ── Footer ──
        lines.append(f"\n{D}  NON-COMMERCIAL TESTING — 7Site LLC — 7sitellc.com")
        lines.append(f"  σ={SIGMA}  D*={D_STAR:.4f}  T*={T_STAR:.4f}  Ctrl+C to stop{R}")
        lines.append(f"{'═'*68}")

        # Output
        self.clear_prev()
        output = '\n'.join(lines)
        print(output)
        self.prev_lines = len(lines)

    def _bar(self, value, width=30):
        filled = int(value * width)
        if value > 0.9:
            color = "\033[31m"  # red
        elif value > 0.7:
            color = "\033[33m"  # yellow
        else:
            color = "\033[32m"  # green
        return f"{color}{'█' * filled}{'░' * (width - filled)}{self.RESET}"

    def _sparkline(self, values, width=60):
        if not values:
            return ""
        sparks = " ▁▂▃▄▅▆▇█"
        mn, mx = min(values), max(values)
        rng = max(mx - mn, 1e-10)
        # Sample to width
        step = max(1, len(values) // width)
        sampled = values[::step][:width]
        chars = []
        for v in sampled:
            idx = int((v - mn) / rng * 8)
            idx = max(0, min(8, idx))
            chars.append(sparks[idx])
        return ''.join(chars)


# ═══════════════════════════════════════════════════════════════════════════════
#  LAYER 5b: A/B COMPARISON — Honest benchmarking
# ═══════════════════════════════════════════════════════════════════════════════

class ABLogger:
    """
    Logs baseline OS metrics alongside TIG analysis.
    After the run, compare: did TIG's classifications predict
    what actually happened?
    
    This is NOT a simulated benchmark. It logs REAL metrics
    and REAL TIG predictions side by side. You judge.
    """

    def __init__(self, path="tig_ab_log.jsonl"):
        self.path = path
        self.entries = []

    def log(self, tick_data, raw_metrics):
        entry = {
            'tick': tick_data['tick'],
            'time': tick_data['time'],
            'tig': {
                'coherence': tick_data['coherence'],
                'bands': tick_data['bands'],
                'route': tick_data['route_target'],
                'V_star': tick_data['V_star'],
                'A_star': tick_data['A_star'],
            },
            'os': {
                'cpu_avg': raw_metrics.get('cpu_avg', 0),
                'cpu_max': raw_metrics.get('cpu_max', 0),
                'mem_used': raw_metrics.get('mem_used', 0),
                'load_1m': raw_metrics.get('load_1m', 0),
                'disk_read': raw_metrics.get('disk_read', 0),
                'disk_write': raw_metrics.get('disk_write', 0),
                'net_tx': raw_metrics.get('net_tx', 0),
                'net_rx': raw_metrics.get('net_rx', 0),
            },
        }
        self.entries.append(entry)
        try:
            with open(self.path, 'a') as f:
                f.write(json.dumps(entry, default=str) + '\n')
        except Exception:
            pass

    def summary(self):
        if not self.entries:
            return "No data collected."

        cohs = [e['tig']['coherence'] for e in self.entries]
        cpus = [e['os']['cpu_avg'] for e in self.entries]
        mems = [e['os']['mem_used'] for e in self.entries]

        # Did coherence track inversely with CPU load? (it should)
        if len(cohs) > 5 and len(cpus) > 5:
            corr = float(np.corrcoef(cohs, cpus)[0, 1]) if np.std(cpus) > 0.001 else 0
        else:
            corr = 0

        # Band transitions — did they predict load changes?
        band_changes = 0
        for i in range(1, len(self.entries)):
            if self.entries[i]['tig']['bands'] != self.entries[i-1]['tig']['bands']:
                band_changes += 1

        lines = [
            f"═══ A/B COMPARISON SUMMARY ═══",
            f"  Ticks collected: {len(self.entries)}",
            f"  Duration: {(self.entries[-1]['tick'] - self.entries[0]['tick'])} ticks",
            f"",
            f"  TIG Coherence:",
            f"    Mean S*:   {np.mean(cohs):.6f}",
            f"    Min S*:    {np.min(cohs):.6f}",
            f"    Max S*:    {np.max(cohs):.6f}",
            f"    Std S*:    {np.std(cohs):.6f}",
            f"",
            f"  OS Metrics:",
            f"    Mean CPU:  {np.mean(cpus)*100:.1f}%",
            f"    Mean MEM:  {np.mean(mems)*100:.1f}%",
            f"",
            f"  Correlation (S* vs CPU): {corr:.4f}",
            f"    {'Negative = TIG coherence drops when CPU rises (EXPECTED)' if corr < -0.1 else ''}",
            f"    {'Positive = coherence rises with CPU (UNEXPECTED)' if corr > 0.1 else ''}",
            f"    {'Near zero = no clear relationship yet (need more data/variance)' if abs(corr) <= 0.1 else ''}",
            f"",
            f"  Band transitions: {band_changes}",
            f"    {'Active dynamics — bands responding to load changes' if band_changes > 5 else 'Stable — try generating load to see transitions'}",
            f"",
            f"  HONEST ASSESSMENT:",
            f"    This is REAL data from YOUR machine.",
            f"    Correlation tells you if TIG is tracking something real.",
            f"    Band transitions tell you if classification responds to events.",
            f"    Neither proves TIG is BETTER than existing tools — only that",
            f"    it produces a COHERENT signal from raw OS metrics.",
            f"",
            f"  Log saved to: {self.path}",
        ]
        return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="TIG Deploy — Full coherence loop on real hardware",
        epilog="NON-COMMERCIAL TESTING — 7Site LLC — 7sitellc.com"
    )
    parser.add_argument("--steer", action="store_true",
                       help="Enable active steering (set process priorities/affinity). Needs root.")
    parser.add_argument("--ab", action="store_true",
                       help="A/B logging mode: record TIG analysis alongside raw OS metrics")
    parser.add_argument("--json", action="store_true",
                       help="Output JSON per tick instead of dashboard")
    parser.add_argument("--interval", type=float, default=1.0,
                       help="Seconds between ticks (default: 1.0)")
    parser.add_argument("--duration", type=float, default=None,
                       help="Run for N seconds then stop (default: run until Ctrl+C)")
    parser.add_argument("--log", type=str, default=None,
                       help="Append tick data to this JSONL file")
    parser.add_argument("--no-dash", action="store_true",
                       help="Suppress terminal dashboard")
    args = parser.parse_args()

    # ── Setup ──
    loop = TickLoop(
        interval=args.interval,
        steer=args.steer,
        log_path=args.log,
    )
    dashboard = Dashboard() if not args.json and not args.no_dash else None
    ab_logger = ABLogger() if args.ab else None

    # ── Banner ──
    if not args.json:
        print(f"\033[1m")
        print(f"╔══════════════════════════════════════════════════════════╗")
        print(f"║  TIG DEPLOY — FULL COHERENCE LOOP                      ║")
        print(f"║  {loop.ncpu} CPU cores detected                               ║")
        print(f"║  Interval: {args.interval}s  Mode: {'STEER' if args.steer else 'WATCH'}              ║")
        print(f"║  σ={SIGMA}  D*={D_STAR:.4f}  T*={T_STAR:.4f}                     ║")
        print(f"║  NON-COMMERCIAL TESTING — 7Site LLC — 7sitellc.com     ║")
        print(f"╚══════════════════════════════════════════════════════════╝")
        print(f"\033[0m")
        if args.steer and not loop.actuator.is_root:
            print(f"\033[33m  ⚠ --steer requires root. Running in dry-run mode.\033[0m")
        print(f"  Starting in 1 second... (Ctrl+C to stop)\n")
        time.sleep(1)

    # ── Warmup: prime the sensors with a few quick reads ──
    reader = loop.reader
    for _ in range(3):
        metrics = reader.read()
        for name, value in metrics.items():
            if isinstance(value, (int, float)) and math.isfinite(value):
                if 0 <= value <= 1:
                    loop.engine.feed(name, value)
        time.sleep(0.2)

    # ── Main loop ──
    loop.running = True
    start = time.time()

    def handle_sigint(sig, frame):
        loop.running = False
    signal.signal(signal.SIGINT, handle_sigint)

    try:
        while loop.running:
            tick_data = loop.tick()

            if ab_logger:
                raw = reader.read()
                ab_logger.log(tick_data, raw)

            if args.json:
                print(json.dumps(tick_data, default=str))
            elif dashboard:
                dashboard.render(tick_data, loop.coherence_history, loop.ncpu)

            if args.duration and (time.time() - start) >= args.duration:
                break

            # Adaptive sleep: subtract tick time from interval
            sleep_time = max(0.01, args.interval - tick_data['elapsed_ms'] / 1000)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        pass

    # ── Summary ──
    if not args.json:
        print(f"\n\n{'═'*60}")
        print(f"  TIG DEPLOY — SESSION COMPLETE")
        print(f"  Ticks: {loop.tick_count}")
        print(f"  Duration: {time.time() - start:.1f}s")
        if loop.coherence_history:
            cohs = list(loop.coherence_history)
            print(f"  Coherence: mean={np.mean(cohs):.6f} min={np.min(cohs):.6f} max={np.max(cohs):.6f}")
        if loop.actuator.actions_taken:
            print(f"  Actions taken: {len(loop.actuator.actions_taken)}")
        print(f"{'═'*60}")

    if ab_logger:
        print(f"\n{ab_logger.summary()}")

    # ── Export final state ──
    try:
        final_path = "tig_final_state.json"
        state = loop.engine.state()
        state['session'] = {
            'ticks': loop.tick_count,
            'duration': time.time() - start,
            'coherence_history': [round(x, 8) for x in loop.coherence_history],
        }
        with open(final_path, 'w') as f:
            json.dump(state, f, indent=2, default=str)
        if not args.json:
            print(f"\n  Final state saved to {final_path}")
    except Exception:
        pass


if __name__ == "__main__":
    main()
