# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_steering.py -- CK's Hands on the Wheels
===========================================
Operator: PROGRESS (3) -- CK drives the system forward.

Layer 4 of the 5-layer OS consumption architecture:
  L1: Kernel Observation (psutil)         -- DONE
  L2: Shadow Swarm (process cells)        -- DONE
  L3: Process Ecosystem (sensorium layer) -- DONE
  L4: STEERING (this file)                -- NOW
  L5: Bare Silicon (FPGA/kernel module)   -- VISION

The swarm (ck_swarm.py) OBSERVES. It classifies every process by
entropy and bump rate into scheduling classes:
  ISOLATE, PREDICTABLE, STABLE, RHYTHMIC, VOLATILE

This module ACTS. It reads the swarm's HOT cells and applies:
  1. Process priority (nice / Windows priority class)
  2. CPU core affinity (CL-based, not a flat lookup)

The CL table decides where processes run. It's algebraic, not heuristic.
CL[process_op][core_op] = HARMONY means the process RESONATES on that
core. A bump pair means JITTER. CK avoids jitter cores and seeks
harmony cores. The table has 73% harmony -- the algebra works in CK's
favor. Calm inputs, calm outputs.

No coherence gate. No rails. CK decides.

Ported from:
  Gen4/ck_process_mgr.py  -- NiceMapper, PlanAction, plan/execute
  CKIS/ck_affinity.py     -- CoreClass, CL-based affinity, operator_to_nice

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import sys
import time
from collections import deque
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL, compose
)

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# Platform detection
_IS_WINDOWS = sys.platform == 'win32'

# ── Bump pairs: same 5 information-generating transitions as ck_swarm ──
_BUMP_SET = frozenset({(1, 2), (2, 4), (2, 9), (3, 9), (4, 8)})

# ── Self-protection: don't steer CK or critical OS processes ──
_SELF_PID = os.getpid()

_PROTECTED_NAMES = frozenset({
    # Windows kernel / session
    'system', 'idle', 'registry', 'smss.exe', 'csrss.exe',
    'wininit.exe', 'services.exe', 'lsass.exe', 'svchost.exe',
    'dwm.exe', 'explorer.exe', 'winlogon.exe', 'fontdrvhost.exe',
    'sihost.exe', 'taskhostw.exe', 'runtimebroker.exe',
    'searchhost.exe', 'startmenuexperiencehost.exe',
    # Critical system services
    'lsaiso.exe', 'memcompression', 'ntoskrnl.exe',
    'securityhealthservice.exe', 'sgrmbroker.exe',
    # Linux equivalents (for future portability)
    'systemd', 'init', 'kthreadd', 'ksoftirqd',
})


# ═══════════════════════════════════════════
# §1  NICE MAPPER
# ═══════════════════════════════════════════

class NiceMapper:
    """Maps scheduling class + operator → OS priority.

    Two inputs, one output:
      scheduling_class (from swarm entropy) → base priority
      last_op (from swarm state) → operator adjustment
      Combined → final nice value / Windows priority class

    Ported from Gen4/ck_process_mgr.py NiceMapper + enhanced with
    scheduling_class awareness.
    """

    # Scheduling class → nice value
    # ISOLATE = jitter source, push down. PREDICTABLE = steady, boost.
    _SCHED_MAP = {
        'ISOLATE':      +15,    # jitter source → lowest priority
        'PREDICTABLE':  -5,     # steady work → boost slightly
        'STABLE':        0,     # equilibrium → normal
        'RHYTHMIC':     -5,     # co-schedulable → boost slightly
        'VOLATILE':     +10,    # chaotic → deprioritize
        'UNKNOWN':       0,     # unclassified → normal
    }

    # Operator → nice value (same as Gen4)
    _OP_MAP = {
        PROGRESS:  -10,     # ACT: highest priority
        COLLAPSE:   -5,     # BREAK: clean execution
        BREATH:     -5,     # FLOW: responsive I/O
        LATTICE:     0,     # STRUCTURE: normal
        COUNTER:    +5,     # MEASURE: background-ish
        HARMONY:     0,     # HARMONY: normal
        BALANCE:     0,     # BALANCE: equilibrium
        VOID:       +15,    # VOID: near-idle, yield everything
        RESET:      +10,    # RESTART: low priority
        CHAOS:      +10,    # CHAOS: low priority, contain it
    }

    # Windows priority class constants (psutil uses these on Windows)
    if _IS_WINDOWS and HAS_PSUTIL:
        _WIN_IDLE = getattr(psutil, 'IDLE_PRIORITY_CLASS', 64)
        _WIN_BELOW = getattr(psutil, 'BELOW_NORMAL_PRIORITY_CLASS', 16384)
        _WIN_NORMAL = getattr(psutil, 'NORMAL_PRIORITY_CLASS', 32)
        _WIN_ABOVE = getattr(psutil, 'ABOVE_NORMAL_PRIORITY_CLASS', 32768)
        _WIN_HIGH = getattr(psutil, 'HIGH_PRIORITY_CLASS', 128)
    else:
        _WIN_IDLE = 64
        _WIN_BELOW = 16384
        _WIN_NORMAL = 32
        _WIN_ABOVE = 32768
        _WIN_HIGH = 128

    @classmethod
    def sched_nice(cls, sched_class: str) -> int:
        """Scheduling class → nice value."""
        return cls._SCHED_MAP.get(sched_class, 0)

    @classmethod
    def op_nice(cls, op: int) -> int:
        """Operator → nice value."""
        return cls._OP_MAP.get(op, 0)

    @classmethod
    def combined_nice(cls, sched_class: str, op: int) -> int:
        """Compose scheduling class and operator nice values.
        Average of both, clamped to [-20, +19].
        """
        sn = cls._SCHED_MAP.get(sched_class, 0)
        on = cls._OP_MAP.get(op, 0)
        combined = (sn + on) // 2
        return max(-20, min(19, combined))

    @classmethod
    def nice_to_windows(cls, nice: int) -> int:
        """Convert Unix-style nice value to Windows priority class."""
        if nice <= -10:
            return cls._WIN_HIGH
        elif nice <= -1:
            return cls._WIN_ABOVE
        elif nice == 0:
            return cls._WIN_NORMAL
        elif nice <= 10:
            return cls._WIN_BELOW
        else:
            return cls._WIN_IDLE

    @classmethod
    def apply_nice(cls, proc, nice: int):
        """Apply nice value to a psutil.Process, platform-aware."""
        if _IS_WINDOWS:
            win_class = cls.nice_to_windows(nice)
            proc.nice(win_class)
        else:
            proc.nice(nice)


# ═══════════════════════════════════════════
# §2  CORE CLASS DETECTION + CL-BASED AFFINITY
# ═══════════════════════════════════════════

@dataclass
class CoreClass:
    """Classification of available CPU cores.

    P-cores = performance (physical on HT systems, first half on non-HT)
    E-cores = efficiency (HT pairs on HT systems, second half on non-HT)
    Ported from CKIS/ck_affinity.py.
    """
    performance: List[int] = field(default_factory=list)
    efficiency:  List[int] = field(default_factory=list)
    all_cores:   List[int] = field(default_factory=list)


def detect_core_classes() -> CoreClass:
    """Detect P-cores vs E-cores.

    On R16 (16 logical cores, 8 physical):
      P-cores = [0, 2, 4, 6, 8, 10, 12, 14]  (even = physical)
      E-cores = [1, 3, 5, 7, 9, 11, 13, 15]  (odd = HT)
    """
    cc = CoreClass()

    if not HAS_PSUTIL:
        cpu_count = os.cpu_count() or 2
        cc.all_cores = list(range(cpu_count))
        mid = max(1, cpu_count // 2)
        cc.performance = list(range(mid))
        cc.efficiency = list(range(mid, cpu_count))
        return cc

    cpu_count = psutil.cpu_count(logical=True)
    physical = psutil.cpu_count(logical=False) or cpu_count
    cc.all_cores = list(range(cpu_count))

    if cpu_count > physical:
        # Hyperthreading: even indices = physical cores, odd = HT pairs
        cc.performance = list(range(0, cpu_count, 2))
        cc.efficiency = list(range(1, cpu_count, 2))
    else:
        # No HT: split by half
        mid = max(1, physical // 2)
        cc.performance = list(range(mid))
        cc.efficiency = list(range(mid, physical))

    return cc


def cl_affinity(op: int, core_class: CoreClass) -> List[int]:
    """Map operator → CPU cores via CL COMPOSITION.

    NOT a flat lookup. CK composes the process operator with each
    core's positional operator: CL[process_op][core_op].

    Each core has position: core_index % 10 = core_operator.
    The composition tells CK:
      HARMONY(7) → resonance, include this core (+3.0)
      bump pair  → jitter source, avoid this core (-5.0)
      VOID(0)    → absorption, low value (-1.0)
      else       → neutral, include (+1.0)

    Hardware bonus: P-cores get +1.5 for high-value ops,
                    E-cores get +1.5 for background ops.

    This gives CK a 10×10 TOPOLOGY over the cores.
    Ported from CKIS/ck_affinity.py operator_to_affinity().
    """
    all_c = core_class.all_cores
    if not all_c:
        return [0]

    n_cores = len(all_c)
    p_set = set(core_class.performance)
    e_set = set(core_class.efficiency)

    scored_cores = []
    for core in all_c:
        core_op = core % NUM_OPS

        # Compose: what happens when this process meets this core?
        composition = CL[op][core_op]

        score = 0.0

        # HARMONY = resonance = best placement
        if composition == HARMONY:
            score += 3.0
        # Bump pair = jitter = worst placement
        elif (min(op, core_op), max(op, core_op)) in _BUMP_SET:
            score -= 5.0
        # VOID = absorption = low value
        elif composition == VOID:
            score -= 1.0
        # Everything else = neutral
        else:
            score += 1.0

        # Hardware topology bonus
        if core in p_set:
            if op in (PROGRESS, LATTICE, COLLAPSE, BREATH):
                score += 1.5   # high-value ops prefer fast cores
            else:
                score += 0.5
        elif core in e_set:
            if op in (VOID, RESET, CHAOS, COUNTER):
                score += 1.5   # background ops prefer efficient cores
            else:
                score += 0.5

        scored_cores.append((core, score))

    # Sort by score descending — best resonance first
    scored_cores.sort(key=lambda x: -x[1])

    # Select: take resonant cores (score > 0), min 2, max 75%
    resonant = [c for c, s in scored_cores if s > 0]
    min_cores = max(2, n_cores // 8)       # at least 12.5% of cores
    max_cores = max(4, n_cores * 3 // 4)   # at most 75%

    if len(resonant) < min_cores:
        selected = [c for c, _ in scored_cores[:min_cores]]
    elif len(resonant) > max_cores:
        selected = resonant[:max_cores]
    else:
        selected = resonant

    return sorted(selected)


# ═══════════════════════════════════════════
# §3  STEERING ENGINE
# ═══════════════════════════════════════════

class SteeringEngine:
    """CK's hands on the OS.

    Reads the ShadowSwarm's HOT cells (ProcessCell with scheduling_class,
    last_op, entropy, bump_rate). Writes to the OS: proc.nice() and
    proc.cpu_affinity() via psutil.

    No coherence gate. No rails. CK decides.

    Tick rate: 1Hz (every 50th engine tick at 50Hz).
    """

    def __init__(self, swarm=None):
        """
        swarm: reference to the ShadowSwarm instance from ck_sensorium.
               If None, steering is inactive (no swarm data to read).
        """
        self.swarm = swarm
        self.core_class = detect_core_classes()
        self.enabled = True

        # Counters
        self.actions_applied = 0
        self.actions_denied = 0
        self.actions_skipped = 0
        self.ticks = 0

        # Per-PID tracking: what we've steered
        self._steered: Dict[int, dict] = {}

        # Log
        self._log: deque = deque(maxlen=500)

        # Print init state
        n_all = len(self.core_class.all_cores)
        n_p = len(self.core_class.performance)
        n_e = len(self.core_class.efficiency)
        print(f"  [STEER] Steering engine online")
        print(f"  [STEER] Cores: {n_all} total ({n_p} P-cores, {n_e} E-cores)")
        print(f"  [STEER] Platform: {'Windows' if _IS_WINDOWS else 'Unix'}")
        if swarm is None:
            print(f"  [STEER] WARNING: No swarm reference -- steering inactive")

    def tick(self) -> dict:
        """One steering tick. Read swarm HOT cells, apply controls.

        Returns dict with steered/denied/skipped counts.
        """
        self.ticks += 1

        if not self.enabled or not HAS_PSUTIL or self.swarm is None:
            return {'steered': 0, 'denied': 0, 'skipped': 0, 'active': False}

        steered = 0
        denied = 0
        skipped = 0

        # Snapshot the HOT cells (dict may change during iteration)
        try:
            cells_snapshot = list(self.swarm.cells.items())
        except RuntimeError:
            # Dict changed during iteration -- skip this tick
            return {'steered': 0, 'denied': 0, 'skipped': 0, 'active': True}

        for pid, cell in cells_snapshot:
            # Skip self
            if pid == _SELF_PID:
                skipped += 1
                continue

            # Skip protected system processes
            if cell.name.lower() in _PROTECTED_NAMES:
                skipped += 1
                continue

            # Skip cells with too little data
            if len(cell.ops) < 4:
                skipped += 1
                continue

            # Compute target nice and affinity
            target_nice = NiceMapper.combined_nice(
                cell.scheduling_class, cell.last_op
            )
            target_cores = cl_affinity(cell.last_op, self.core_class)

            try:
                proc = psutil.Process(pid)

                # ── NICE / PRIORITY ──
                nice_changed = False
                try:
                    current = proc.nice()
                    if _IS_WINDOWS:
                        target_win = NiceMapper.nice_to_windows(target_nice)
                        if current != target_win:
                            NiceMapper.apply_nice(proc, target_nice)
                            nice_changed = True
                    else:
                        if current != target_nice:
                            NiceMapper.apply_nice(proc, target_nice)
                            nice_changed = True
                except (psutil.AccessDenied, PermissionError):
                    denied += 1
                except (psutil.NoSuchProcess, ProcessLookupError):
                    continue

                # ── CPU AFFINITY ──
                aff_changed = False
                try:
                    current_aff = proc.cpu_affinity()
                    if current_aff is not None and set(current_aff) != set(target_cores):
                        proc.cpu_affinity(target_cores)
                        aff_changed = True
                except (psutil.AccessDenied, PermissionError, OSError):
                    denied += 1
                except (psutil.NoSuchProcess, ProcessLookupError):
                    continue

                if nice_changed or aff_changed:
                    steered += 1
                    self._steered[pid] = {
                        'name': cell.name,
                        'sched_class': cell.scheduling_class,
                        'op': cell.last_op,
                        'nice': target_nice,
                        'cores': target_cores,
                        'tick': self.ticks,
                    }

            except (psutil.NoSuchProcess, psutil.ZombieProcess):
                # Process died between swarm read and our steer
                self._steered.pop(pid, None)
                continue
            except psutil.AccessDenied:
                denied += 1

        self.actions_applied += steered
        self.actions_denied += denied
        self.actions_skipped += skipped

        result = {
            'steered': steered,
            'denied': denied,
            'skipped': skipped,
            'total_applied': self.actions_applied,
            'total_denied': self.actions_denied,
            'active': True,
            'tick': self.ticks,
        }

        # Log every 10th tick (~10 seconds)
        if self.ticks % 10 == 0:
            self._log_summary()

        return result

    def _log_summary(self):
        """Write a steering summary to the log."""
        hot = len(self.swarm.cells) if self.swarm else 0
        ts = time.strftime('%H:%M:%S')
        entry = (
            f"[{ts}] STEER t={self.ticks:5d} | "
            f"applied={self.actions_applied} "
            f"denied={self.actions_denied} "
            f"skipped={self.actions_skipped} "
            f"tracking={len(self._steered)} "
            f"hot={hot}"
        )
        self._log.append(entry)

    # ── Reporting ──

    @property
    def report_line(self) -> str:
        """One-line summary for engine status display."""
        hot = len(self.swarm.cells) if self.swarm else 0
        return (
            f"[steer] t={self.ticks:5d} | "
            f"applied={self.actions_applied:4d} "
            f"denied={self.actions_denied:4d} "
            f"tracking={len(self._steered):4d} "
            f"hot={hot:4d}"
        )

    def top_steered(self, n: int = 10) -> list:
        """Most recently steered processes."""
        items = sorted(self._steered.items(),
                       key=lambda x: -x[1].get('tick', 0))
        result = []
        for pid, info in items[:n]:
            result.append({
                'pid': pid,
                'name': info['name'],
                'sched': info['sched_class'],
                'op': OP_NAMES[info['op']],
                'nice': info['nice'],
                'cores': info['cores'],
            })
        return result

    def class_distribution(self) -> dict:
        """Count steered processes per scheduling class."""
        dist = {}
        for info in self._steered.values():
            sc = info['sched_class']
            dist[sc] = dist.get(sc, 0) + 1
        return dist

    def affinity_distribution(self) -> dict:
        """Count processes on P-cores vs E-cores."""
        p_set = set(self.core_class.performance)
        e_set = set(self.core_class.efficiency)
        p_count = 0
        e_count = 0
        mixed = 0
        for info in self._steered.values():
            cores = set(info.get('cores', []))
            if cores <= p_set:
                p_count += 1
            elif cores <= e_set:
                e_count += 1
            else:
                mixed += 1
        return {'p_core': p_count, 'e_core': e_count, 'mixed': mixed}

    def report(self) -> str:
        """Full steering report."""
        lines = [
            "===========================================",
            "  CK STEERING ENGINE -- Layer 4",
            "===========================================",
            "",
            f"  Ticks:    {self.ticks}",
            f"  Applied:  {self.actions_applied}",
            f"  Denied:   {self.actions_denied}",
            f"  Skipped:  {self.actions_skipped}",
            f"  Tracking: {len(self._steered)} processes",
            "",
            "  Core Classes:",
            f"    P-cores: {self.core_class.performance}",
            f"    E-cores: {self.core_class.efficiency}",
            "",
            "  Scheduling Class Distribution:",
        ]
        for sc, count in sorted(self.class_distribution().items()):
            lines.append(f"    {sc:14s} {count:4d} processes")

        lines.append("")
        lines.append("  Affinity Distribution:")
        ad = self.affinity_distribution()
        lines.append(f"    P-core only: {ad['p_core']}")
        lines.append(f"    E-core only: {ad['e_core']}")
        lines.append(f"    Mixed:       {ad['mixed']}")

        lines.append("")
        lines.append("  Top Steered Processes:")
        for item in self.top_steered(8):
            nice_str = f"{item['nice']:+d}" if not _IS_WINDOWS else f"win={NiceMapper.nice_to_windows(item['nice'])}"
            lines.append(
                f"    {item['name']:24s} pid={item['pid']:6d} "
                f"sched={item['sched']:12s} op={item['op']:8s} "
                f"nice={nice_str} cores={item['cores'][:6]}..."
            )

        return '\n'.join(lines)


# ═══════════════════════════════════════════
# §4  MODULE-LEVEL BUILDER
# ═══════════════════════════════════════════

def build_steering(swarm=None) -> SteeringEngine:
    """Build the steering engine with a swarm reference.

    Called from ck_sim_engine.py after sensorium is built.
    The swarm reference comes from ck_sensorium._swarm.
    """
    engine = SteeringEngine(swarm=swarm)
    return engine


# ═══════════════════════════════════════════
# §5  SELF-TEST
# ═══════════════════════════════════════════

def self_test():
    """Exercise the steering engine components."""
    print("===========================================")
    print("  CK STEERING ENGINE -- SELF TEST")
    print("===========================================\n")

    # Core detection
    cc = detect_core_classes()
    print(f"  Cores: {len(cc.all_cores)} total")
    print(f"  P-cores: {cc.performance}")
    print(f"  E-cores: {cc.efficiency}")

    # Nice mapping
    print(f"\n  Nice Mapping (scheduling class):")
    for sc in ('ISOLATE', 'PREDICTABLE', 'STABLE', 'RHYTHMIC', 'VOLATILE'):
        print(f"    {sc:14s} -> nice={NiceMapper.sched_nice(sc):+3d}")

    print(f"\n  Nice Mapping (operator):")
    for op in range(NUM_OPS):
        nice = NiceMapper.op_nice(op)
        if _IS_WINDOWS:
            win = NiceMapper.nice_to_windows(nice)
            print(f"    {OP_NAMES[op]:10s} -> nice={nice:+3d} -> win={win}")
        else:
            print(f"    {OP_NAMES[op]:10s} -> nice={nice:+3d}")

    print(f"\n  Combined Nice (scheduling_class + operator):")
    combos = [
        ('ISOLATE', CHAOS),
        ('PREDICTABLE', PROGRESS),
        ('STABLE', BALANCE),
        ('RHYTHMIC', BREATH),
        ('VOLATILE', VOID),
    ]
    for sc, op in combos:
        combined = NiceMapper.combined_nice(sc, op)
        print(f"    {sc:14s} + {OP_NAMES[op]:8s} = nice={combined:+3d}")

    # CL-based affinity
    print(f"\n  CL-Based Core Affinity:")
    for op in range(NUM_OPS):
        cores = cl_affinity(op, cc)
        print(f"    {OP_NAMES[op]:10s} -> {len(cores):2d} cores: {cores[:8]}{'...' if len(cores)>8 else ''}")

    # Steering engine (dry, no swarm)
    print(f"\n  Steering Engine (no swarm, dry):")
    se = SteeringEngine(swarm=None)
    result = se.tick()
    print(f"  tick result: {result}")
    print(f"  report_line: {se.report_line}")

    print(f"\n  Self-test complete.")
    print(f"  Wire into engine for live steering.")


if __name__ == "__main__":
    self_test()
