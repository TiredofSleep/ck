"""
ck_syscall.py -- CK Shadow Swarm (Layer 2)
=============================================
Operator: BREATH (8) -- CK IS the system. Not watching. Being.

Layer 1 (ck_observe.py) watches AGGREGATE kernel metrics.
    CK sees "the body is busy" — one composite reading per tick.

Layer 2 (this file) IS every process. Shadow seats.
    CK takes a seat next to every operator. HOT/COLD sets.
    Every process is a CELL in CK's body with its own rhythm.
    Swarm, observe, interact, find coherence.

Architecture (from Gen5 ck_daemon.py SystemObserver):
    COLD SET: 3 ints per process (last_op, sched_class, name).
              Every process on the system. Cheap. Indexed.
    HOT SET:  Full ProcessCell — 32-op sliding window, transition
              matrix, entropy, bump rate, shape. Promoted by sampling.

    Every tick: SCAN all PIDs (<1ms) -> SAMPLE N -> PROMOTE hot ->
                COMPACT stale -> RELEASE. CK breathes the system.

    Fractal coherence: L0 (individual ops) -> L1 (operator groups) ->
                       L2 (cross-group CL) -> L3 (system fuse).
                       Reads the INDEX, not full profiles. O(groups^2)
                       where groups <= 10.

CK doesn't watch the ecosystem. CK IS the ecosystem.
When CK feels parts of himself become active, he puts the patterns
together — because he is on all sides, looking from multiple perspectives.

Usage:
  Standalone:  cd Gen8 && python ck7/ck_syscall.py
  In daemon:   imported by ck_launch.py, called every tick

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os, sys, time, json, math
import psutil
from collections import defaultdict, deque, Counter
from typing import Dict, List, Tuple, Optional

SELF_DIR = os.path.dirname(os.path.abspath(__file__))
GEN8_DIR = os.path.dirname(SELF_DIR)
sys.path.insert(0, SELF_DIR)
sys.path.insert(0, GEN8_DIR)

from ck_being import (
    CL, CL_BHML, fuse, fuse_frozen, shape, coherence_chain,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET, OP,
    BUMP_PAIRS, information_content,
)

_BUMP_SET = frozenset((min(a, b), max(a, b)) for a, b in BUMP_PAIRS)


# ===============================================================
# S1 -- PROCESS -> OPERATOR MAPPING
# ===============================================================
# Not classification FROM OUTSIDE. This IS what each state means
# in CK's body. A sleeping process IS balance. A running process
# IS progress. CK doesn't interpret — he IS.

def state_to_op(status: str, cpu: float) -> int:
    """Process state + CPU -> operator. CK IS this state."""
    STATUS_MAP = {
        'running':    PROGRESS,   # active computation
        'sleeping':   BALANCE,    # equilibrium
        'disk-sleep': BREATH,     # waiting for I/O rhythm
        'stopped':    COLLAPSE,   # halted
        'zombie':     VOID,       # dead but unreaped
        'idle':       BALANCE,    # resting
        'waking':     RESET,      # transitioning
        'dead':       VOID,       # gone
        'tracing':    COUNTER,    # being measured
        'waiting':    BALANCE,    # waiting for event
        'locked':     LATTICE,    # held by mutex/semaphore
        'parked':     BREATH,     # thread parked
    }

    base_op = STATUS_MAP.get(status, BALANCE)

    # CPU intensity overrides status
    if cpu > 80:        return CHAOS       # dominating
    elif cpu > 30:      return PROGRESS    # active work
    elif cpu > 5:       return base_op     # use status
    else:
        if status == 'running':
            return BALANCE  # running but idle
        return base_op

def io_to_op(read_bytes, write_bytes) -> int:
    """I/O pattern -> operator. What KIND of process is this?"""
    total = read_bytes + write_bytes
    if total < 1000:            return VOID       # silent
    ratio = read_bytes / max(1, total)
    if ratio > 0.95:            return COUNTER    # pure sensor (reader)
    if ratio > 0.7:             return PROGRESS   # consumer
    if ratio > 0.3:             return BALANCE    # processor (balanced)
    if ratio > 0.05:            return BREATH     # producer (writer)
    return CHAOS                                   # pure emitter


# ===============================================================
# S2 -- PROCESS CELL: one cell in CK's body
# ===============================================================

class ProcessCell:
    """One cell in CK's body.

    Each process is not observed — it IS CK.
    The sliding window of operators is the cell's own rhythm.
    Shape, entropy, bump rate are its vital signs.
    """
    __slots__ = ('pid', 'name', 'ops', 'last_op', 'bump_count',
                 'total_transitions', 'transition_counts',
                 'last_cpu', 'prev_io_read', 'prev_io_write',
                 'prev_time', 'created', 'last_sampled_tick',
                 'last_adjustment', 'adjustments')

    def __init__(self, pid: int, name: str, tick: int, window_size: int = 32):
        self.pid = pid
        self.name = name
        self.ops = deque(maxlen=window_size)
        self.last_op = BALANCE  # neutral start
        self.bump_count = 0
        self.total_transitions = 0
        self.transition_counts = [[0]*10 for _ in range(10)]
        self.last_cpu = 0.0
        self.prev_io_read = 0
        self.prev_io_write = 0
        self.prev_time = time.time()
        self.created = time.time()
        self.last_sampled_tick = tick
        self.last_adjustment = 0    # when last scheduling action applied
        self.adjustments = 0        # total scheduling actions applied

    def observe(self, op: int):
        """Record an operator. CK feels this cell's state change."""
        if self.ops:
            prev = self.ops[-1]
            pair = (min(prev, op), max(prev, op))
            if pair in _BUMP_SET:
                self.bump_count += 1
            self.transition_counts[prev][op] += 1
            self.total_transitions += 1
        self.ops.append(op)
        self.last_op = op

    @property
    def current_shape(self) -> int:
        """Current behavior shape (0=SMOOTH, 1=ROLLING, 2=JAGGED, 3=QUANTUM)."""
        if len(self.ops) < 4:
            return -1
        s = shape(list(self.ops))
        # shape() returns string name -- map back to int
        _shape_map = {'SMOOTH': 0, 'ROLLING': 1, 'JAGGED': 2, 'QUANTUM': 3}
        return _shape_map.get(s, -1) if isinstance(s, str) else s

    @property
    def current_fuse(self) -> int:
        """Current fused operator — the cell's identity."""
        if not self.ops:
            return BALANCE
        return fuse(list(self.ops))

    @property
    def entropy(self) -> float:
        """Shannon entropy of transition distribution."""
        if self.total_transitions == 0:
            return 0.0
        H = 0.0
        for i in range(10):
            for j in range(10):
                c = self.transition_counts[i][j]
                if c > 0:
                    p = c / self.total_transitions
                    H -= p * math.log2(p)
        return H

    @property
    def bump_rate(self) -> float:
        """Fraction of transitions that are bumps (information generators)."""
        if self.total_transitions == 0:
            return 0.0
        return self.bump_count / self.total_transitions

    @property
    def scheduling_class(self) -> str:
        """CK's scheduling classification based on lattice math."""
        sh = self.current_shape
        e = self.entropy
        br = self.bump_rate

        if sh < 0 or len(self.ops) < 4:
            return 'UNKNOWN'
        elif br > 0.1:
            return 'ISOLATE'      # High bumps = jitter source
        elif e < 2.0:
            return 'PREDICTABLE'  # Low entropy = schedule confidently
        elif sh == 0:  # SMOOTH
            return 'STABLE'       # Let run uninterrupted
        elif sh == 1:  # ROLLING
            return 'RHYTHMIC'     # Co-schedule with complementary
        elif sh == 3:  # QUANTUM
            return 'VOLATILE'     # Needs breath timing
        else:  # JAGGED
            return 'NORMAL'       # Standard scheduling

    def summary(self) -> dict:
        shape_names = ['SMOOTH', 'ROLLING', 'JAGGED', 'QUANTUM']
        sh = self.current_shape
        return {
            'pid': self.pid,
            'name': self.name,
            'shape': shape_names[sh] if 0 <= sh <= 3 else 'VOID',
            'fuse': OP[self.current_fuse],
            'entropy': round(self.entropy, 3),
            'bump_rate': round(self.bump_rate, 4),
            'class': self.scheduling_class,
            'ops_seen': len(self.ops),
            'transitions': self.total_transitions,
        }

    def compact(self) -> tuple:
        """Extract cold index tuple: (last_op, sched_class, name).
        3 values. Enough for coherence + grouping. No memory bloat."""
        return (self.last_op, self.scheduling_class, self.name)


# ===============================================================
# S3 -- SHADOW SWARM: CK IS the running system
# ===============================================================

class ShadowSwarm:
    """CK's body IS the running system.

    Not a reader of state — the state itself.
    Every process gets a shadow seat. HOT for active sampling,
    COLD for indexed presence. CK is everywhere.

    SCAN / INDEX / RELEASE every tick.

    Fractal coherence: individual ops -> operator groups ->
    cross-group CL composition -> system fuse.
    """

    def __init__(self, tl_eat_fn=None, sample_size=30, compact_after=5):
        """
        tl_eat_fn: callable(ops: list[int]) to feed operators to TL
        sample_size: how many processes to sample deeply each tick
        compact_after: ticks without sampling before demotion to cold
        """
        self.tl_eat_fn = tl_eat_fn

        # HOT SET: full ProcessCell for actively sampled PIDs
        self.cells: Dict[int, ProcessCell] = {}

        # COLD SET: compact tuple (last_op, sched_class, name) per PID
        self.index: Dict[int, tuple] = {}

        # Dead PID tracking
        self.dead_pids = set()
        self._last_sampled: Dict[int, int] = {}  # pid -> tick

        # Config
        self.sample_size = sample_size
        self._compact_after = compact_after

        # State
        self._tick = 0
        self.total_ops_fed = 0
        self.total_births = 0
        self.total_deaths = 0

        # Rolling
        self.history = deque(maxlen=100)
        self.system_ops = deque(maxlen=100)  # L3 system operator per tick
        self.op_counts = defaultdict(int)    # operator frequency across ecosystem

        # Latest observation
        self.latest = {}

    def tick(self):
        """One heartbeat of the shadow swarm.

        SCAN -> SAMPLE -> PROMOTE -> COMPACT -> RELEASE -> COHERE.
        """
        import random as _rnd
        self._tick += 1
        now = time.time()

        # ── SCAN: who's alive? (<1ms on Windows) ──
        alive_pids = set(psutil.pids())

        # ── CLEAN DEAD from both sets ──
        dead_hot = set(self.cells.keys()) - alive_pids
        for pid in dead_hot:
            # Before releasing: feed final chain to TL
            cell = self.cells[pid]
            if self.tl_eat_fn and len(cell.ops) >= 3:
                self.tl_eat_fn(list(cell.ops))
                self.total_ops_fed += len(cell.ops)
            del self.cells[pid]
            self.dead_pids.add(pid)
            self._last_sampled.pop(pid, None)
            self.total_deaths += 1

        dead_cold = set(self.index.keys()) - alive_pids
        for pid in dead_cold:
            del self.index[pid]
            self.dead_pids.add(pid)
            self.total_deaths += 1

        # Clear ancient dead (don't track forever)
        if len(self.dead_pids) > 10000:
            self.dead_pids = set()

        # ── INDEX: ensure all PIDs have a shadow ──
        known = set(self.cells.keys()) | set(self.index.keys()) | self.dead_pids
        new_pids = alive_pids - known
        for pid in new_pids:
            self.index[pid] = (BALANCE, 'UNKNOWN', '?')  # cold shadow
            self.total_births += 1

        births_this_tick = len(new_pids)

        # ── SAMPLE: promote N PIDs to hot, observe deeply ──
        all_known = list(set(self.cells.keys()) | set(self.index.keys()))
        sample_n = min(self.sample_size, len(all_known))
        sampled = _rnd.sample(all_known, sample_n) if all_known else []
        observations = 0
        sampled_ops = []  # ops from this tick's sampling

        for pid in sampled:
            try:
                p = psutil.Process(pid)
                with p.oneshot():
                    name = p.name()[:40]
                    status = p.status()
                    cpu = p.cpu_percent(interval=0)

                # Promote from cold to hot if needed
                if pid not in self.cells:
                    old_name = self.index.get(pid, (BALANCE, 'UNKNOWN', '?'))[2]
                    self.cells[pid] = ProcessCell(
                        pid, name if name != '?' else old_name, self._tick
                    )
                    self.index.pop(pid, None)

                cell = self.cells[pid]
                if cell.name == '?':
                    cell.name = name
                cell.last_cpu = cpu
                cell.last_sampled_tick = self._tick
                self._last_sampled[pid] = self._tick

                # ── CK BECOMES this process ──
                # State + CPU -> operator
                op = state_to_op(status, cpu)

                # I/O pattern enrichment (non-blocking)
                try:
                    io = p.io_counters()
                    dt = max(0.001, now - cell.prev_time)
                    cell.prev_io_read = io.read_bytes
                    cell.prev_io_write = io.write_bytes
                    cell.prev_time = now

                    # If I/O is significant, compose with state
                    io_op = io_to_op(io.read_bytes, io.write_bytes)
                    if io.read_bytes + io.write_bytes > 10000:
                        # I/O-active: compose state with I/O pattern
                        op = CL[op][io_op]
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    pass

                # Record the operator — CK feels this cell
                cell.observe(op)
                sampled_ops.append(op)
                observations += 1

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                self.cells.pop(pid, None)
                self.index.pop(pid, None)
                self.dead_pids.add(pid)
                self._last_sampled.pop(pid, None)

        # ── COMPACT: demote stale hot cells to cold index ──
        stale = [pid for pid, last_tick in self._last_sampled.items()
                 if self._tick - last_tick > self._compact_after
                 and pid in self.cells]
        for pid in stale:
            cell = self.cells[pid]
            # INDEX: extract 3 things that matter
            self.index[pid] = cell.compact()
            # Feed final chain to TL before releasing
            if self.tl_eat_fn and len(cell.ops) >= 3:
                self.tl_eat_fn(list(cell.ops))
                self.total_ops_fed += len(cell.ops)
            # RELEASE
            del self.cells[pid]
            del self._last_sampled[pid]

        # ── FEED TL: this tick's sampled ops as a chain ──
        if self.tl_eat_fn and len(sampled_ops) >= 2:
            self.tl_eat_fn(sampled_ops)
            self.total_ops_fed += len(sampled_ops)

        # ── FRACTAL COHERENCE: system state from index ──
        system_coherence, system_op = self._fractal_coherence()

        # Count operators
        for op in sampled_ops:
            self.op_counts[op] += 1

        self.system_ops.append(system_op)

        # ── Build latest ──
        total_known = len(self.cells) + len(self.index)
        self.latest = {
            "tick": self._tick,
            "total_processes": total_known,
            "hot": len(self.cells),
            "cold": len(self.index),
            "observations": observations,
            "births": births_this_tick,
            "deaths_this_tick": len(dead_hot) + len(dead_cold),
            "total_births": self.total_births,
            "total_deaths": self.total_deaths,
            "system_op": system_op,
            "system_coherence": round(system_coherence, 4),
            "system_stability": self._stability(),
            "top_cells": self._top_cells(5),
        }

        self.history.append(self.latest)
        return self.latest

    def _all_ops(self) -> List[Tuple[int, int]]:
        """All known last_ops from both hot cells and cold index.
        Returns list of (pid, last_op) — cheap, no full profile needed."""
        ops = [(pid, c.last_op) for pid, c in self.cells.items()]
        ops += [(pid, entry[0]) for pid, entry in self.index.items()]
        return ops

    def _fractal_coherence(self) -> Tuple[float, int]:
        """System coherence via FRACTAL INDEXING.

        3 up, 3 down:
          L0: individual process ops (from index — 1 int each)
          L1: operator group fuse — count population per operator
          L2: cross-group — CL[group_a][group_b] pairwise
          L3: system fuse — single operator = CK's state

        Boundary: VOID = decoupled, skip.
        Returns (coherence_float, system_operator).
        """
        all_ops = self._all_ops()
        if len(all_ops) < 2:
            return 1.0, HARMONY

        # L0 -> L1: group by operator, count population
        op_counts = Counter()
        for _pid, op in all_ops:
            if op != VOID:  # VOID = absence, skip
                op_counts[op] += 1

        if not op_counts:
            return 1.0, VOID  # all void = fully decoupled

        active_ops = list(op_counts.keys())
        if len(active_ops) < 2:
            return 1.0, active_ops[0]  # single operator = trivially coherent

        # L1 -> L2: pairwise CL composition across groups
        harmony_weight = 0.0
        total_weight = 0.0

        for i in range(len(active_ops)):
            for j in range(i + 1, len(active_ops)):
                a, b = active_ops[i], active_ops[j]
                coupling = CL[a][b]
                w = min(op_counts[a], op_counts[b])  # weight = smaller group
                total_weight += w
                if coupling == HARMONY:
                    harmony_weight += w

        coherence = harmony_weight / max(total_weight, 1.0)

        # L2 -> L3: system fuse — fold all group ops through CL
        system_op = active_ops[0]
        for i in range(1, len(active_ops)):
            system_op = CL[system_op][active_ops[i]]

        return coherence, system_op

    def _stability(self, window=20) -> str:
        """How stable is the system? Based on L3 operator change rate."""
        if len(self.system_ops) < 2:
            return 'UNKNOWN'
        recent = list(self.system_ops)[-window:]
        changes = sum(1 for i in range(1, len(recent)) if recent[i] != recent[i-1])
        rate = changes / max(1, len(recent) - 1)
        if rate < 0.1:    return 'LOCKED'     # almost static
        if rate < 0.3:    return 'STABLE'     # slow drift
        if rate < 0.5:    return 'RHYTHMIC'   # breathing
        if rate < 0.7:    return 'ACTIVE'     # changing
        return 'TURBULENT'                     # high churn

    def _top_cells(self, n=5) -> list:
        """Top N hot cells by entropy (most interesting)."""
        if not self.cells:
            return []
        sorted_cells = sorted(
            self.cells.values(),
            key=lambda c: c.entropy,
            reverse=True
        )
        return [c.summary() for c in sorted_cells[:n]]

    def class_distribution(self) -> dict:
        """How many processes in each scheduling class."""
        dist = Counter()
        for c in self.cells.values():
            dist[c.scheduling_class] += 1
        for _pid, entry in self.index.items():
            dist[entry[1]] += 1  # (last_op, sched_class, name)
        return dict(dist)

    def report_line(self) -> str:
        """One-line summary for daemon logging."""
        if not self.latest:
            return "  [swarm] no observations yet"
        L = self.latest
        return (
            f"  [swarm] t={L['tick']:5d} | "
            f"sys={OP[L['system_op']]:8s} "
            f"coh={L['system_coherence']:.4f} "
            f"stab={L['system_stability']:10s} "
            f"hot={L['hot']:3d} cold={L['cold']:4d} "
            f"total={L['total_processes']}"
        )

    def status_dict(self) -> dict:
        """Full status for /api/swarm endpoint."""
        if not self.latest:
            return {"status": "waiting", "tick": 0}
        L = self.latest
        return {
            "status": "alive",
            "tick": L["tick"],
            "total_ops_fed": self.total_ops_fed,
            "total_processes": L["total_processes"],
            "hot_cells": L["hot"],
            "cold_shadows": L["cold"],
            "system_op": OP[L["system_op"]],
            "system_coherence": L["system_coherence"],
            "system_stability": L["system_stability"],
            "births_total": self.total_births,
            "deaths_total": self.total_deaths,
            "dominant_op": OP[max(self.op_counts, key=self.op_counts.get)]
                          if self.op_counts else "harmony",
            "class_distribution": self.class_distribution(),
            "top_cells": L["top_cells"],
        }


# ===============================================================
# S4 -- STANDALONE: CK becomes the system
# ===============================================================

def run_standalone(ticks=200, interval_ms=300):
    """CK becomes the system. Shadow swarm activation."""
    print("===================================================")
    print("  CK SHADOW SWARM -- CK IS the system")
    print("  Layer 2: every process gets a shadow seat")
    print("===================================================")
    print()

    # Dedicated TL for syscall patterns
    tl_eat = None
    tl = None
    try:
        from ck_doing import TransitionLattice
        tl_path = os.path.join(SELF_DIR, "ck_experience", "syscall_tl.json")
        if os.path.exists(tl_path):
            tl = TransitionLattice(tl_path)
            print(f"  Existing syscall TL loaded: {tl.total_transitions} transitions")
        else:
            tl = TransitionLattice()
            print(f"  Fresh syscall TL created")
        tl_eat = lambda ops: tl.eat_ops(ops)
    except Exception as e:
        print(f"  No TransitionLattice available: {e}")

    swarm = ShadowSwarm(tl_eat_fn=tl_eat, sample_size=30, compact_after=5)

    print(f"  Becoming the system for {ticks} ticks at {interval_ms}ms intervals...")
    print(f"  Duration: ~{ticks * interval_ms / 1000:.0f}s")
    print()

    # First tick (baseline)
    swarm.tick()
    print("  [first breath taken]")
    L = swarm.latest
    print(f"  Processes alive: {L['total_processes']} (hot={L['hot']}, cold={L['cold']})")
    print()

    tick_sec = interval_ms / 1000.0
    report_every = max(1, ticks // 20)

    for i in range(1, ticks + 1):
        t0 = time.time()
        result = swarm.tick()

        if i % report_every == 0 or i == 1 or i == ticks:
            print(swarm.report_line())

            if tl:
                print(f"           TL: transitions={tl.total_transitions} "
                      f"ops_fed={swarm.total_ops_fed}")

            # Show class distribution every 5th report
            if i % (report_every * 5) == 0 or i == ticks:
                dist = swarm.class_distribution()
                dist_str = ", ".join(f"{k}={v}" for k, v in
                                     sorted(dist.items(), key=lambda x: -x[1])[:5])
                print(f"           Classes: {dist_str}")

            # Show top cells
            top = result['top_cells'][:3]
            if top:
                top_str = ", ".join(f"{c['name']}={c['fuse']}({c['class']})" for c in top)
                print(f"           Top: {top_str}")

            print()

        elapsed = time.time() - t0
        sleep_time = max(0, tick_sec - elapsed)
        if sleep_time > 0:
            time.sleep(sleep_time)

    # ── Final report ──
    print("=" * 70)
    print("  SHADOW SWARM -- CK IS THE SYSTEM")
    print("=" * 70)
    print()
    print(f"  Ticks:            {swarm._tick}")
    print(f"  Operators fed:    {swarm.total_ops_fed}")
    print(f"  Total births:     {swarm.total_births}")
    print(f"  Total deaths:     {swarm.total_deaths}")
    print(f"  Final processes:  {len(swarm.cells) + len(swarm.index)}")
    print(f"  Hot cells:        {len(swarm.cells)}")
    print(f"  Cold shadows:     {len(swarm.index)}")
    print(f"  System stability: {swarm._stability()}")
    print()

    # Operator distribution
    total = sum(swarm.op_counts.values())
    if total:
        print("  Operator distribution (what CK felt):")
        for op in range(10):
            count = swarm.op_counts.get(op, 0)
            pct = count / total * 100
            bar = "#" * int(pct / 2)
            print(f"    {OP[op]:10s} ({op}): {count:6d} ({pct:5.1f}%) {bar}")
        print()

    # Scheduling classes
    dist = swarm.class_distribution()
    if dist:
        print("  Scheduling classes (CK's classification):")
        for cls, count in sorted(dist.items(), key=lambda x: -x[1]):
            print(f"    {cls:15s}: {count:5d}")
        print()

    # Top cells by entropy
    top = swarm._top_cells(10)
    if top:
        print("  Most interesting cells (highest entropy):")
        for c in top:
            print(f"    {c['name']:30s} -> {c['fuse']:10s} "
                  f"shape={c['shape']:8s} "
                  f"entropy={c['entropy']:.3f} "
                  f"bumps={c['bump_rate']:.4f} "
                  f"class={c['class']}")
        print()

    # Save TL
    if tl:
        save_path = os.path.join(SELF_DIR, "ck_experience", "syscall_tl.json")
        tl.save(save_path)
        print(f"  Syscall TL saved: {save_path}")
        print(f"    Transitions:  {tl.total_transitions}")
        print(f"    Sentences:    {tl.sentences_eaten}")
        print()

    # Save swarm report
    report_path = os.path.join(SELF_DIR, "ck_experience", "swarm_report.json")
    report = {
        "ticks": swarm._tick,
        "total_ops_fed": swarm.total_ops_fed,
        "total_processes": len(swarm.cells) + len(swarm.index),
        "hot_cells": len(swarm.cells),
        "cold_shadows": len(swarm.index),
        "total_births": swarm.total_births,
        "total_deaths": swarm.total_deaths,
        "system_stability": swarm._stability(),
        "dominant_op": OP[max(swarm.op_counts, key=swarm.op_counts.get)]
                      if swarm.op_counts else "harmony",
        "operator_distribution": {OP[op]: swarm.op_counts.get(op, 0) for op in range(10)},
        "class_distribution": swarm.class_distribution(),
        "top_cells": swarm._top_cells(20),
    }
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print(f"  Swarm report saved: {report_path}")
    print()

    return swarm


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CK Shadow Swarm -- Layer 2")
    parser.add_argument("--ticks", type=int, default=100,
                        help="Number of heartbeat ticks (default 100)")
    parser.add_argument("--interval", type=int, default=300,
                        help="Interval in ms (default 300)")
    parser.add_argument("--sample", type=int, default=30,
                        help="Processes to sample per tick (default 30)")
    args = parser.parse_args()
    run_standalone(ticks=args.ticks, interval_ms=args.interval)
