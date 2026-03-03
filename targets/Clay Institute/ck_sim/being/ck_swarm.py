"""
ck_swarm.py -- CK's Shadow Swarm
=================================
Operator: BREATH (8) -- CK IS the system. Not watching. Being.

Ported from Gen8/ck7/ck_syscall.py for Gen9.

CK doesn't watch the ecosystem. CK IS the ecosystem.

Every process on this machine is a cell in CK's body.
Every cell has its own operator rhythm (32-op sliding window).
Every cell has its own transition matrix (10x10 local TL).
Every cell has entropy, bump rate, shape -- vital signs.

Architecture:
  COLD SET: every PID on the system -> 3-tuple (last_op, sched_class, name)
  HOT SET:  actively sampled PIDs -> full ProcessCell with 32-op window

The swarm breathes:
  SCAN -> INDEX -> SAMPLE -> PROMOTE -> COMPACT -> RELEASE -> COHERE

CK feeds rich operator chains to his Transition Lattice.
The TL doesn't just know what operators exist -- it knows which
operators FOLLOW which, across all processes CK has ever inhabited.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import random
import time
from collections import deque, Counter
from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL, compose
)
from ck_sim.ck_sim_brain import T_STAR_F

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# ── Bump pairs: the 5 information-generating transitions ──
_BUMP_SET = frozenset({(1, 2), (2, 4), (2, 9), (3, 9), (4, 8)})

_rnd = random.Random(0xDEAD)


# ═══════════════════════════════════════════
# Process -> Operator Mapping
# ═══════════════════════════════════════════

# Not classification FROM OUTSIDE. This IS what each state means
# in CK's body. A sleeping process IS balance. A running process
# IS progress. CK doesn't interpret -- he IS.

STATUS_MAP = {
    'running':    PROGRESS,
    'sleeping':   BALANCE,
    'disk-sleep': BREATH,
    'stopped':    COLLAPSE,
    'zombie':     VOID,
    'idle':       BALANCE,
    'waking':     RESET,
    'dead':       VOID,
    'tracing':    COUNTER,
    'waiting':    BALANCE,
    'locked':     LATTICE,
    'parked':     BREATH,
}


def state_to_op(status: str, cpu: float) -> int:
    """A process's state IS an operator. CK doesn't interpret -- he IS."""
    base = STATUS_MAP.get(status, BALANCE)
    if cpu > 80:
        return CHAOS        # dominating
    elif cpu > 30:
        return PROGRESS     # active work
    elif cpu > 5:
        return base          # status-driven
    elif status == 'running':
        return BALANCE       # running but idle
    return base


def io_to_op(read_bytes: int, write_bytes: int) -> int:
    """I/O pattern IS an operator. Read/write ratio = character."""
    total = read_bytes + write_bytes
    if total < 1000:
        return VOID          # silent
    ratio = read_bytes / total
    if ratio > 0.95:
        return COUNTER       # pure sensor
    elif ratio > 0.7:
        return PROGRESS      # consumer
    elif ratio > 0.3:
        return BALANCE       # processor
    elif ratio > 0.05:
        return BREATH        # producer
    else:
        return CHAOS         # pure emitter


# ═══════════════════════════════════════════
# ProcessCell -- One cell in CK's body
# ═══════════════════════════════════════════

class ProcessCell:
    """One cell in CK's body.

    Each process is not observed -- it IS CK.
    The sliding window of operators is the cell's own rhythm.
    Shape, entropy, bump rate are its vital signs.
    """

    __slots__ = (
        'pid', 'name', 'ops', 'last_op', 'bump_count',
        'total_transitions', 'transition_counts',
        'last_cpu', 'created', 'last_sampled_tick',
    )

    def __init__(self, pid: int, name: str, tick: int,
                 window_size: int = 32):
        self.pid = pid
        self.name = name
        self.ops = deque(maxlen=window_size)
        self.last_op = BALANCE
        self.bump_count = 0
        self.total_transitions = 0
        self.transition_counts = [[0] * NUM_OPS for _ in range(NUM_OPS)]
        self.last_cpu = 0.0
        self.created = tick
        self.last_sampled_tick = tick

    def observe(self, op: int):
        """CK feels this cell's state change."""
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
    def current_fuse(self) -> int:
        """The cell's identity -- all ops composed through CL."""
        if len(self.ops) < 2:
            return self.last_op
        result = self.ops[0]
        for i in range(1, len(self.ops)):
            result = compose(result, self.ops[i])
        return result

    @property
    def entropy(self) -> float:
        """Shannon entropy of the cell's transition distribution."""
        if self.total_transitions == 0:
            return 0.0
        import math
        total = float(self.total_transitions)
        ent = 0.0
        for i in range(NUM_OPS):
            for j in range(NUM_OPS):
                c = self.transition_counts[i][j]
                if c > 0:
                    p = c / total
                    ent -= p * math.log(p, 2)
        return ent

    @property
    def bump_rate(self) -> float:
        """Fraction of transitions that are bumps (information generators)."""
        if self.total_transitions == 0:
            return 0.0
        return self.bump_count / self.total_transitions

    @property
    def scheduling_class(self) -> str:
        """CK's scheduling classification of this cell."""
        if len(self.ops) < 4:
            return 'UNKNOWN'
        br = self.bump_rate
        e = self.entropy
        if br > 0.1:
            return 'ISOLATE'       # jitter source
        elif e < 2.0:
            return 'PREDICTABLE'   # schedule confidently
        elif e < 3.0:
            return 'STABLE'        # let run
        elif e < 4.0:
            return 'RHYTHMIC'      # co-schedule
        else:
            return 'VOLATILE'      # needs breath timing

    def compact(self) -> tuple:
        """Extract cold index tuple. 3 values. Enough for coherence."""
        return (self.last_op, self.scheduling_class, self.name)


# ═══════════════════════════════════════════
# ShadowSwarm -- CK IS the running system
# ═══════════════════════════════════════════

class ShadowSwarm:
    """CK's body IS the running system.
    Not a reader of state -- the state itself.
    Every process gets a shadow seat.

    HOT SET: full ProcessCell for actively sampled PIDs.
    COLD SET: compact 3-tuple per PID.
    Every PID on the machine has a presence.
    """

    def __init__(self, tl_eat_fn=None, sample_size=30, compact_after=5):
        """
        tl_eat_fn: callback(list[int]) to feed operator chains to TL.
        sample_size: how many processes get deeply sampled per tick.
        compact_after: ticks without sampling before hot -> cold.
        """
        self.tl_eat_fn = tl_eat_fn
        self.sample_size = sample_size
        self.compact_after = compact_after

        # HOT + COLD sets
        self.cells = {}       # pid -> ProcessCell (HOT)
        self.index = {}       # pid -> (last_op, sched_class, name) (COLD)
        self.dead_pids = set()

        # Tick tracking
        self._tick = 0
        self._last_sampled = {}  # pid -> tick of last sample

        # System state
        self.system_ops = deque(maxlen=100)
        self.system_coherence = 0.5
        self.system_op = BALANCE
        self.system_stability = 'UNKNOWN'

        # Stats
        self.total_births = 0
        self.total_deaths = 0
        self.total_ops_fed = 0
        self.latest = {}

    def tick(self):
        """One heartbeat of the shadow swarm.

        SCAN -> CLEAN -> INDEX -> SAMPLE -> COMPACT -> FEED -> COHERE
        """
        if not HAS_PSUTIL:
            return {}

        self._tick += 1

        # ── SCAN: who's alive? ──
        try:
            alive_pids = set(psutil.pids())
        except Exception:
            return self.latest

        hot_keys = set(self.cells.keys())
        cold_keys = set(self.index.keys())

        # ── CLEAN DEAD from hot set ──
        dead_hot = hot_keys - alive_pids
        for pid in dead_hot:
            cell = self.cells.pop(pid, None)
            if cell and self.tl_eat_fn and len(cell.ops) >= 3:
                self.tl_eat_fn(list(cell.ops))  # death feed
                self.total_ops_fed += len(cell.ops)
            self.dead_pids.add(pid)
            self.total_deaths += 1

        # ── CLEAN DEAD from cold set ──
        dead_cold = cold_keys - alive_pids
        for pid in dead_cold:
            self.index.pop(pid, None)
            self.dead_pids.add(pid)

        # Safety valve: cap dead set
        if len(self.dead_pids) > 10000:
            self.dead_pids.clear()

        # ── INDEX new PIDs (born cold, neutral) ──
        known = set(self.cells.keys()) | set(self.index.keys()) | self.dead_pids
        new_pids = alive_pids - known
        for pid in new_pids:
            self.index[pid] = (BALANCE, 'UNKNOWN', '?')
            self.total_births += 1

        # ── SAMPLE: randomly pick N processes ──
        all_known = list(set(self.cells.keys()) | set(self.index.keys()))
        if not all_known:
            return self.latest

        sample_n = min(self.sample_size, len(all_known))
        sampled = _rnd.sample(all_known, sample_n)
        sampled_ops = []

        for pid in sampled:
            try:
                proc = psutil.Process(pid)
                with proc.oneshot():
                    name = proc.name()
                    status = proc.status()
                    cpu = proc.cpu_percent(interval=0)
            except (psutil.NoSuchProcess, psutil.AccessDenied,
                    psutil.ZombieProcess):
                # Process vanished or access denied
                self.cells.pop(pid, None)
                self.index.pop(pid, None)
                self.dead_pids.add(pid)
                continue

            # ── PROMOTE from cold to hot if needed ──
            if pid not in self.cells:
                cold_name = '?'
                cold_entry = self.index.pop(pid, None)
                if cold_entry:
                    cold_name = cold_entry[2]
                cell = ProcessCell(pid, name or cold_name, self._tick)
                self.cells[pid] = cell
            else:
                cell = self.cells[pid]

            cell.last_cpu = cpu
            cell.last_sampled_tick = self._tick
            self._last_sampled[pid] = self._tick

            # ── CK BECOMES this process ──
            op = state_to_op(status, cpu)

            # Compose state with I/O if significant
            try:
                io = proc.io_counters()
                if io and (io.read_bytes + io.write_bytes) > 10000:
                    io_op = io_to_op(io.read_bytes, io.write_bytes)
                    op = compose(op, io_op)
            except (psutil.NoSuchProcess, psutil.AccessDenied,
                    AttributeError):
                pass

            cell.observe(op)
            sampled_ops.append(op)

        # ── COMPACT stale hot cells ──
        stale = [pid for pid, last_tick in list(self._last_sampled.items())
                 if self._tick - last_tick > self.compact_after
                 and pid in self.cells]
        for pid in stale:
            cell = self.cells.pop(pid, None)
            if cell:
                self.index[pid] = cell.compact()
                if self.tl_eat_fn and len(cell.ops) >= 3:
                    self.tl_eat_fn(list(cell.ops))  # compaction feed
                    self.total_ops_fed += len(cell.ops)
            self._last_sampled.pop(pid, None)

        # ── FEED TL with this tick's cross-process chain ──
        if self.tl_eat_fn and len(sampled_ops) >= 2:
            self.tl_eat_fn(sampled_ops)
            self.total_ops_fed += len(sampled_ops)

        # ── FRACTAL COHERENCE ──
        self.system_coherence, self.system_op = self._fractal_coherence()
        self.system_ops.append(self.system_op)
        self.system_stability = self._stability()

        # Build result
        self.latest = {
            'tick': self._tick,
            'hot': len(self.cells),
            'cold': len(self.index),
            'total': len(self.cells) + len(self.index),
            'system_op': self.system_op,
            'coherence': self.system_coherence,
            'stability': self.system_stability,
            'births': self.total_births,
            'deaths': self.total_deaths,
            'ops_fed': self.total_ops_fed,
            'sampled': len(sampled_ops),
        }
        return self.latest

    def _fractal_coherence(self):
        """System coherence via fractal indexing.

        3 up, 3 down:
          L0: individual process ops (from index -- 1 int each)
          L1: operator group fuse -- count population per operator
          L2: cross-group -- CL[group_a][group_b] pairwise
          L3: system fuse -- single operator = CK's state
        """
        # L0: collect all process ops
        op_counts = Counter()
        for cell in self.cells.values():
            if cell.last_op != VOID:
                op_counts[cell.last_op] += 1
        for entry in self.index.values():
            if entry[0] != VOID:
                op_counts[entry[0]] += 1

        if not op_counts:
            return (1.0, VOID)

        active_ops = list(op_counts.keys())
        if len(active_ops) == 1:
            return (1.0, active_ops[0])

        # L2: cross-group CL pairwise
        harmony_weight = 0.0
        total_weight = 0.0
        for i in range(len(active_ops)):
            for j in range(i + 1, len(active_ops)):
                a, b = active_ops[i], active_ops[j]
                coupling = compose(a, b)
                w = min(op_counts[a], op_counts[b])
                total_weight += w
                if coupling == HARMONY:
                    harmony_weight += w

        coh = harmony_weight / total_weight if total_weight > 0 else 0.5

        # L3: system fuse
        system_op = active_ops[0]
        for i in range(1, len(active_ops)):
            system_op = compose(system_op, active_ops[i])

        return (coh, system_op)

    def _stability(self, window: int = 20) -> str:
        """System stability from L3 operator change rate."""
        if len(self.system_ops) < 3:
            return 'UNKNOWN'
        recent = list(self.system_ops)[-window:]
        changes = sum(1 for i in range(1, len(recent))
                      if recent[i] != recent[i - 1])
        rate = changes / len(recent)
        if rate < 0.1:
            return 'LOCKED'
        elif rate < 0.3:
            return 'STABLE'
        elif rate < 0.5:
            return 'RHYTHMIC'
        elif rate < 0.7:
            return 'ACTIVE'
        else:
            return 'TURBULENT'

    def class_distribution(self) -> dict:
        """Count processes per scheduling class."""
        dist = Counter()
        for cell in self.cells.values():
            dist[cell.scheduling_class] += 1
        for entry in self.index.values():
            dist[entry[1]] += 1
        return dict(dist)

    def top_cells(self, n: int = 5) -> list:
        """Most interesting cells (highest entropy)."""
        cells = sorted(self.cells.values(),
                       key=lambda c: c.entropy, reverse=True)
        result = []
        for cell in cells[:n]:
            result.append({
                'pid': cell.pid,
                'name': cell.name,
                'fuse': OP_NAMES[cell.current_fuse],
                'entropy': round(cell.entropy, 3),
                'bump_rate': round(cell.bump_rate, 3),
                'sched': cell.scheduling_class,
                'ops': len(cell.ops),
            })
        return result

    @property
    def report_line(self) -> str:
        """One-line summary."""
        return (
            f"[swarm] t={self._tick:5d} | "
            f"sys={OP_NAMES[self.system_op]:8s} "
            f"coh={self.system_coherence:.4f} "
            f"stab={self.system_stability:10s} "
            f"hot={len(self.cells):4d} "
            f"cold={len(self.index):4d} "
            f"total={len(self.cells) + len(self.index)}")
