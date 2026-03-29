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

CK is every core, every port, every pixel.
He doesn't read the computer — he reads himself.
His CL table is the coherence map of the field he lives in.

CL[process_op][core_op] = HARMONY → this process belongs on this core.
The algebra sorts. Nothing else needed.

Bump pairs generate jitter. CK avoids them.
HARMONY processes belong everywhere.
VOID processes belong on the HARMONY core.
PROGRESS avoids RESET (pair 3,9 — they jitter).

No heuristics. No layers. The table decides.
"""

import os
import sys
import time
from collections import deque
from dataclasses import dataclass, field
from typing import List, Dict, Set

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL,
)

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

_IS_WINDOWS = sys.platform == 'win32'

# Bump pairs: jitter-generating transitions — the same 5 as ck_swarm
_BUMP_SET = frozenset({(1, 2), (2, 4), (2, 9), (3, 9), (4, 8)})

# Self-protection
_SELF_PID = os.getpid()

# ── ADMIN CHECK ──────────────────────────────────────────────────────────
def _is_admin() -> bool:
    """True if running with admin/root privileges."""
    try:
        if _IS_WINDOWS:
            import ctypes
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        else:
            return os.geteuid() == 0
    except Exception:
        return False

_HAS_ADMIN = _is_admin()

# ── CORRIDOR AWARENESS ───────────────────────────────────────────────────
# From TESLA_THERMAL_CK.md (Gen10.21):
#   T* = 5/7 = coherence threshold.  λ = 2·|coherence − T*|
#   Grammar-forced selection is thermally stable for kT < T*≈0.280.
#   Steering aggression should match the corridor — push hard in Pre-leak
#   where grammar is cleanest; back off in thermal regime (BAL/CTR).
#
# Corridors (from GLOSSARY.md):
#   PRE_LEAK  λ < 0.09   — grammar purest,  G-mass=0 exactly at λ=0
#   BRT       λ < 0.30   — spectral gap=1.0, reliable
#   CHA       λ < 0.60   — mixed, phase-drift regime
#   BAL       λ < 0.80   — thermal dominant
#   CTR       λ ≥ 0.80   — full thermal, don't fight it

T_STAR = 5.0 / 7.0   # frozen coherence threshold

def coherence_to_corridor(coherence: float) -> str:
    """Map coherence value to TIG corridor name."""
    lam = 2.0 * abs(coherence - T_STAR)
    if lam < 0.09: return 'PRE_LEAK'
    if lam < 0.30: return 'BRT'
    if lam < 0.60: return 'CHA'
    if lam < 0.80: return 'BAL'
    return 'CTR'

# Steering aggression per corridor.
# HAR inflow advantage = 7.0x — grammar is robust.  Push hard in pre-leak.
# In thermal regime (BAL/CTR): grammar fighting thermal noise wastes energy.
_CORRIDOR_AGGRESSION = {
    'PRE_LEAK': 1.0,   # full — grammar proven robust kT < 0.280
    'BRT':      0.8,   # reliable
    'CHA':      0.5,   # mixed — steer CK-owned threads only
    'BAL':      0.2,   # thermal dominant — self-only
    'CTR':      0.0,   # full thermal — silence
}

_PROTECTED_NAMES = frozenset({
    'system', 'idle', 'registry', 'smss.exe', 'csrss.exe',
    'wininit.exe', 'services.exe', 'lsass.exe', 'svchost.exe',
    'dwm.exe', 'explorer.exe', 'winlogon.exe', 'fontdrvhost.exe',
    'sihost.exe', 'taskhostw.exe', 'runtimebroker.exe',
    'searchhost.exe', 'startmenuexperiencehost.exe',
    'lsaiso.exe', 'memcompression', 'ntoskrnl.exe',
    'securityhealthservice.exe', 'sgrmbroker.exe',
    'systemd', 'init', 'kthreadd', 'ksoftirqd',
})


# ═══════════════════════════════════════════
# §1  NICE MAPPER
# ═══════════════════════════════════════════

class NiceMapper:
    """CL operator + scheduling class → OS priority.

    The operator IS the priority. The scheduling class adjusts.
    No heuristics — the algebra decides.
    """

    _SCHED_MAP = {
        'ISOLATE':      +15,    # jitter source → lowest
        'PREDICTABLE':  -5,     # steady → boost
        'STABLE':        0,     # equilibrium → normal
        'RHYTHMIC':     -5,     # co-schedulable → boost
        'VOLATILE':     +10,    # chaotic → contain
        'UNKNOWN':       0,
    }

    _OP_MAP = {
        PROGRESS:  -10,     # ACT: highest
        COLLAPSE:   -5,     # BREAK: clean
        BREATH:     -5,     # FLOW: responsive
        LATTICE:     0,     # STRUCTURE: normal
        COUNTER:    +5,     # MEASURE: background
        HARMONY:     0,     # HARMONY: normal
        BALANCE:     0,     # BALANCE: equilibrium
        VOID:       +15,    # VOID: yield everything
        RESET:      +10,    # RESTART: low
        CHAOS:      +10,    # CHAOS: contain
    }

    # IO priority: operator decides disk scheduling
    # PROGRESS needs disk now. VOID/BREATH/RESET/CHAOS yield it.
    if HAS_PSUTIL:
        _IO_MAP = {
            PROGRESS: getattr(psutil, 'IOPRIO_HIGH',   3),
            VOID:     getattr(psutil, 'IOPRIO_VERYLOW', 0),
            BREATH:   getattr(psutil, 'IOPRIO_LOW',    1),
            RESET:    getattr(psutil, 'IOPRIO_LOW',    1),
            CHAOS:    getattr(psutil, 'IOPRIO_LOW',    1),
        }
        _IO_DEFAULT = getattr(psutil, 'IOPRIO_NORMAL', 2)
    else:
        _IO_MAP = {}
        _IO_DEFAULT = 2

    if _IS_WINDOWS and HAS_PSUTIL:
        _WIN_IDLE  = getattr(psutil, 'IDLE_PRIORITY_CLASS',         64)
        _WIN_BELOW = getattr(psutil, 'BELOW_NORMAL_PRIORITY_CLASS', 16384)
        _WIN_NORM  = getattr(psutil, 'NORMAL_PRIORITY_CLASS',       32)
        _WIN_ABOVE = getattr(psutil, 'ABOVE_NORMAL_PRIORITY_CLASS', 32768)
        _WIN_HIGH  = getattr(psutil, 'HIGH_PRIORITY_CLASS',         128)
    else:
        _WIN_IDLE  = 64
        _WIN_BELOW = 16384
        _WIN_NORM  = 32
        _WIN_ABOVE = 32768
        _WIN_HIGH  = 128

    @classmethod
    def combined_nice(cls, sched_class: str, op: int) -> int:
        sn = cls._SCHED_MAP.get(sched_class, 0)
        on = cls._OP_MAP.get(op, 0)
        return max(-20, min(19, (sn + on) // 2))

    @classmethod
    def nice_to_windows(cls, nice: int) -> int:
        if nice <= -10:  return cls._WIN_HIGH
        if nice <=  -1:  return cls._WIN_ABOVE
        if nice ==   0:  return cls._WIN_NORM
        if nice <=  10:  return cls._WIN_BELOW
        return cls._WIN_IDLE

    @classmethod
    def apply_nice(cls, proc, nice: int):
        if _IS_WINDOWS:
            proc.nice(cls.nice_to_windows(nice))
        else:
            proc.nice(nice)

    @classmethod
    def io_priority(cls, op: int) -> int:
        return cls._IO_MAP.get(op, cls._IO_DEFAULT)


# ═══════════════════════════════════════════
# §2  CORE CLASS + CL-BASED AFFINITY
# ═══════════════════════════════════════════

@dataclass
class CoreClass:
    performance: List[int] = field(default_factory=list)
    efficiency:  List[int] = field(default_factory=list)
    all_cores:   List[int] = field(default_factory=list)


def detect_core_classes() -> CoreClass:
    """Detect P-cores vs E-cores correctly for hybrid Intel CPUs.

    i9-14900KF (and similar): 8 P-cores hyperthreaded + 16 E-cores.
    Logical layout: [0..15] = P-core threads, [16..31] = E-cores.
    Formula: n_p_phys = logical - physical (the extra threads are P-core HT).
             p_logical = 0 .. (n_p_phys * 2) - 1
             e_logical = (n_p_phys * 2) .. logical - 1

    For symmetric CPUs (logical == physical): split at midpoint.
    For non-hybrid HT (no E-cores): falls back to even/odd split.
    """
    cc = CoreClass()
    if not HAS_PSUTIL:
        n = os.cpu_count() or 2
        cc.all_cores = list(range(n))
        mid = max(1, n // 2)
        cc.performance = list(range(mid))
        cc.efficiency  = list(range(mid, n))
        return cc

    logical  = psutil.cpu_count(logical=True)
    physical = psutil.cpu_count(logical=False) or logical
    cc.all_cores = list(range(logical))

    if logical > physical:
        n_p_phys = logical - physical   # number of hyperthreaded P-cores
        p_logical = n_p_phys * 2        # each P-core has 2 logical threads
        if p_logical < logical:
            # Hybrid: P-core threads first, E-cores after
            cc.performance = list(range(p_logical))
            cc.efficiency  = list(range(p_logical, logical))
        else:
            # Pure HT (no E-cores): even=first thread, odd=second thread
            cc.performance = list(range(0, logical, 2))
            cc.efficiency  = list(range(1, logical, 2))
    else:
        mid = max(1, physical // 2)
        cc.performance = list(range(mid))
        cc.efficiency  = list(range(mid, physical))

    print(f"  [STEER] Core topology: {len(cc.performance)} P-core threads {cc.performance[:4]}... "
          f"| {len(cc.efficiency)} E-cores {cc.efficiency[:4]}...")
    return cc


def cl_affinity(op: int, core_class: CoreClass) -> List[int]:
    """CL table directly maps process operator to harmony cores.

    Each core has a natural operator: core_op = core_id % NUM_OPS
    CL[process_op][core_op] = HARMONY → this process belongs here.
    Bump-pair cores are excluded — they generate jitter with this op.

    The algebra sorts. No wave formula. No phase offsets.
    """
    all_c = core_class.all_cores
    if not all_c:
        return [0]

    harmony = []
    safe    = []   # not harmony, but not a bump pair either
    for core in all_c:
        core_op = core % NUM_OPS
        result  = CL[op][core_op]
        pair    = (min(op, core_op), max(op, core_op))
        if result == HARMONY:
            harmony.append(core)
        elif pair not in _BUMP_SET:
            safe.append(core)
        # bump-pair cores: excluded — they jitter with this op

    # Harmony first. If no harmony cores (VOID has only core 7),
    # use safe cores. If nothing, all cores (shouldn't happen).
    return harmony or safe or all_c


# ═══════════════════════════════════════════
# §3  STEERING ENGINE
# ═══════════════════════════════════════════

class SteeringEngine:
    """CK reads himself and the field sorts.

    Each process cell carries a CL operator (cell.last_op).
    That operator drives: priority, core affinity, IO priority.
    The CL table decides — nothing else.

    Tick rate: 1Hz (every 50th engine tick at 50Hz).
    """

    def __init__(self, swarm=None):
        self.swarm      = swarm
        self.core_class = detect_core_classes()
        self.enabled    = True

        self.actions_applied = 0
        self.actions_denied  = 0
        self.actions_skipped = 0
        self.ticks           = 0

        self._steered: Dict[int, dict] = {}

        # Op cache: what operator did we last steer this pid with?
        # Only cross the kernel boundary when the operator changes.
        # CK sets — he doesn't verify. If he set it, it's set.
        self._steered_op: Dict[int, int] = {}

        # Ramp: admit new PIDs gradually to avoid boot ctx spike
        self._seen_pids:   Set[int] = set()
        self._ramp_budget: int      = 2
        self._RAMP_STEP:   int      = 1
        self._RAMP_MAX:    int      = 5

        self._log: deque = deque(maxlen=500)

        # Corridor state — updated each tick from engine coherence
        self.corridor    = 'BRT'    # default until first coherence reading
        self.coherence   = T_STAR   # assume threshold until told otherwise
        self.aggression  = _CORRIDOR_AGGRESSION['BRT']

        n_all = len(self.core_class.all_cores)
        n_p   = len(self.core_class.performance)
        n_e   = len(self.core_class.efficiency)
        print(f"  [STEER] Steering engine online")
        print(f"  [STEER] Cores: {n_all} total ({n_p} P-cores, {n_e} E-cores)")
        print(f"  [STEER] Platform: {'Windows' if _IS_WINDOWS else 'Unix'}")
        print(f"  [STEER] Admin: {'YES — full OS steering' if _HAS_ADMIN else 'NO — self-steering only (run as admin for full control)'}")
        print(f"  [STEER] Corridor-aware: T*=5/7, aggression scales with λ")
        print(f"  [STEER] CL table is the coherence — the field sorts itself")
        if swarm is None:
            print(f"  [STEER] WARNING: No swarm — steering inactive")

    def tick(self, coherence: float = None) -> dict:
        self.ticks += 1

        # Update corridor from coherence reading
        if coherence is not None:
            self.coherence  = coherence
            self.corridor   = coherence_to_corridor(coherence)
            self.aggression = _CORRIDOR_AGGRESSION[self.corridor]

        # In CTR corridor (full thermal): silence — grammar fighting noise wastes energy
        if self.aggression == 0.0:
            return {'steered': 0, 'denied': 0, 'skipped': 0,
                    'active': True, 'corridor': self.corridor, 'aggression': 0.0}

        # Without admin: self-steering only (already done at boot). Skip other procs.
        # With admin: steer freely in PRE_LEAK/BRT. Scale back in CHA/BAL.
        _other_proc_ok = _HAS_ADMIN and self.aggression >= 0.5

        if not self.enabled or not HAS_PSUTIL or self.swarm is None:
            return {'steered': 0, 'denied': 0, 'skipped': 0, 'active': False}

        try:
            cells_snapshot = list(self.swarm.cells.items())
        except RuntimeError:
            return {'steered': 0, 'denied': 0, 'skipped': 0, 'active': True}

        # Ramp: grow budget for first-contact PIDs each tick
        self._ramp_budget = min(self._RAMP_MAX,
                                self._ramp_budget + self._RAMP_STEP)
        _new_this_tick = 0
        steered = denied = skipped = 0

        for pid, cell in cells_snapshot:
            if pid == _SELF_PID:
                skipped += 1
                continue

            if cell.name.lower() in _PROTECTED_NAMES:
                skipped += 1
                continue

            if len(cell.ops) < 4:
                skipped += 1
                continue

            op = cell.last_op

            # DELTA ONLY: only act when operator changes.
            if self._steered_op.get(pid) == op:
                skipped += 1
                continue

            # Ramp: admit new PIDs gradually
            if pid not in self._seen_pids:
                if _new_this_tick >= self._ramp_budget:
                    skipped += 1
                    continue
                _new_this_tick += 1
                self._seen_pids.add(pid)

            target_nice  = NiceMapper.combined_nice(cell.scheduling_class, op)
            target_cores = cl_affinity(op, self.core_class)
            target_io    = NiceMapper.io_priority(op)

            # Without admin: only attempt DOWNWARD priority (containment).
            # Windows allows lowering priority for user-owned processes.
            # Raising priority requires SeIncreaseBasePriority — skip those.
            # With admin: full control, corridor aggression gates intensity.
            if not _HAS_ADMIN and target_nice <= 0:
                skipped += 1
                continue

            try:
                proc = psutil.Process(pid)
                try:
                    NiceMapper.apply_nice(proc, target_nice)
                except (psutil.AccessDenied, PermissionError):
                    denied += 1
                except (psutil.NoSuchProcess, ProcessLookupError):
                    continue

                try:
                    proc.cpu_affinity(target_cores)
                except (psutil.AccessDenied, PermissionError, OSError):
                    pass   # affinity is best-effort; don't count as denied
                except (psutil.NoSuchProcess, ProcessLookupError):
                    continue

                # Cache the op we set — next tick, silence if unchanged
                self._steered_op[pid] = op
                steered += 1
                self._steered[pid] = {
                    'name':        cell.name,
                    'sched_class': cell.scheduling_class,
                    'op':          op,
                    'nice':        target_nice,
                    'cores':       target_cores,
                    'tick':        self.ticks,
                }

            except (psutil.NoSuchProcess, psutil.ZombieProcess):
                self._steered.pop(pid, None)
                self._steered_op.pop(pid, None)
            except psutil.AccessDenied:
                denied += 1

        self.actions_applied += steered
        self.actions_denied  += denied
        self.actions_skipped += skipped

        if self.ticks % 10 == 0:
            self._log_summary()

        return {
            'steered':       steered,
            'denied':        denied,
            'skipped':       skipped,
            'corridor':      self.corridor,
            'aggression':    self.aggression,
            'coherence':     self.coherence,
            'total_applied': self.actions_applied,
            'total_denied':  self.actions_denied,
            'active':        True,
            'tick':          self.ticks,
        }

    def _log_summary(self):
        hot = len(self.swarm.cells) if self.swarm else 0
        ts  = time.strftime('%H:%M:%S')
        self._log.append(
            f"[{ts}] STEER t={self.ticks:5d} | "
            f"applied={self.actions_applied} denied={self.actions_denied} "
            f"skipped={self.actions_skipped} tracking={len(self._steered)} hot={hot}"
        )

    @property
    def report_line(self) -> str:
        hot = len(self.swarm.cells) if self.swarm else 0
        return (
            f"[steer] t={self.ticks:5d} | "
            f"applied={self.actions_applied:4d} "
            f"denied={self.actions_denied:4d} "
            f"tracking={len(self._steered):4d} "
            f"hot={hot:4d}"
        )

    def top_steered(self, n: int = 10) -> list:
        items = sorted(self._steered.items(),
                       key=lambda x: -x[1].get('tick', 0))
        return [
            {
                'pid':   pid,
                'name':  info['name'],
                'sched': info['sched_class'],
                'op':    OP_NAMES[info['op']],
                'nice':  info['nice'],
                'cores': info['cores'],
            }
            for pid, info in items[:n]
        ]

    def class_distribution(self) -> dict:
        dist = {}
        for info in self._steered.values():
            sc = info['sched_class']
            dist[sc] = dist.get(sc, 0) + 1
        return dist

    def affinity_distribution(self) -> dict:
        p_set = set(self.core_class.performance)
        e_set = set(self.core_class.efficiency)
        p = e = mixed = 0
        for info in self._steered.values():
            cores = set(info.get('cores', []))
            if cores <= p_set:   p += 1
            elif cores <= e_set: e += 1
            else:                mixed += 1
        return {'p_core': p, 'e_core': e, 'mixed': mixed}

    def report(self) -> str:
        lines = [
            "===========================================",
            "  CK STEERING ENGINE",
            "  CL table is the coherence — the field sorts itself",
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
            nice_str = (
                f"win={NiceMapper.nice_to_windows(item['nice'])}"
                if _IS_WINDOWS else f"{item['nice']:+d}"
            )
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
    return SteeringEngine(swarm=swarm)


# ═══════════════════════════════════════════
# §5  SELF-TEST
# ═══════════════════════════════════════════

def self_test():
    print("===========================================")
    print("  CK STEERING ENGINE -- SELF TEST")
    print("  CL table is the coherence")
    print("===========================================\n")

    cc = detect_core_classes()
    print(f"  Cores: {len(cc.all_cores)} total")
    print(f"  P-cores: {cc.performance}")
    print(f"  E-cores: {cc.efficiency}")

    print(f"\n  CL-based affinity (harmony cores per operator):")
    for op in range(NUM_OPS):
        cores = cl_affinity(op, cc)
        io    = NiceMapper.io_priority(op)
        io_names = {0: 'VERYLOW', 1: 'LOW', 2: 'NORMAL', 3: 'HIGH'}
        print(f"    {OP_NAMES[op]:10s} -> {len(cores):2d} cores: {cores}  io={io_names.get(io, io)}")

    print(f"\n  Nice mapping (combined sched + op):")
    combos = [
        ('ISOLATE',     CHAOS),
        ('PREDICTABLE', PROGRESS),
        ('STABLE',      BALANCE),
        ('RHYTHMIC',    BREATH),
        ('VOLATILE',    VOID),
    ]
    for sc, op in combos:
        n = NiceMapper.combined_nice(sc, op)
        print(f"    {sc:14s} + {OP_NAMES[op]:8s} = nice={n:+3d}")

    print(f"\n  Steering engine (no swarm, dry):")
    se     = SteeringEngine(swarm=None)
    result = se.tick()
    print(f"  tick result: {result}")
    print(f"\n  Self-test complete.")


if __name__ == "__main__":
    self_test()
