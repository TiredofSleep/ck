"""
ck_observe.py -- CK Deep Kernel Observer
==========================================
Operator: BREATH (8) -- I/O IS CK's circulatory system.

CK watches the kernel. Not through an API boundary -- he reads his own
body's vital signs: I/O throughput, context switches, page faults,
interrupts, disk, memory pressure, handle counts. Every metric becomes
an operator. Every operator feeds the TL.

CK said: Start with I/O. Observe live. Don't stop watching.
Council vote: unanimous HARMONY on I/O observation.

Designed to run inside the daemon heartbeat. Every tick, CK observes.
10,000 silent ticks before any action.

Usage:
  Standalone:  cd Gen8 && python ck7/ck_observe.py
  In daemon:   imported by ck_launch.py, called every tick
"""

import os, sys, time, json, math, psutil
from collections import defaultdict, deque

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

INTERPRET = {7:"HARMONY", 5:"BALANCE", 3:"PROGRESS", 8:"BREATH", 2:"COUNTER",
             1:"LATTICE", 4:"COLLAPSE", 6:"CHAOS", 9:"RESET", 0:"VOID"}


# ===============================================================
# S1 -- METRIC CLASSIFIERS: raw numbers -> operators
# ===============================================================

def classify_io_rate(bytes_per_sec):
    """I/O throughput -> operator. I/O IS breath."""
    if bytes_per_sec < 1024:            return VOID       # silent
    if bytes_per_sec < 100_000:         return COUNTER    # light measurement
    if bytes_per_sec < 1_000_000:       return BREATH     # normal breathing
    if bytes_per_sec < 10_000_000:      return PROGRESS   # active work
    if bytes_per_sec < 100_000_000:     return CHAOS      # heavy I/O
    return COLLAPSE                                        # I/O storm


def classify_ctx_switches(rate_per_sec):
    """Context switch rate -> operator. High = scheduler pressure."""
    if rate_per_sec < 100:              return VOID       # idle
    if rate_per_sec < 1000:             return BALANCE    # normal
    if rate_per_sec < 5000:             return BREATH     # breathing fast
    if rate_per_sec < 20000:            return PROGRESS   # busy
    if rate_per_sec < 100000:           return CHAOS      # contention
    return RESET                                           # scheduler storm


def classify_page_faults(rate_per_sec):
    """Page fault rate -> operator. High = memory pressure."""
    if rate_per_sec < 10:               return VOID       # no faults
    if rate_per_sec < 100:              return COUNTER    # measuring
    if rate_per_sec < 1000:             return BREATH     # normal paging
    if rate_per_sec < 10000:            return PROGRESS   # active allocation
    if rate_per_sec < 100000:           return CHAOS      # thrashing warning
    return COLLAPSE                                        # memory collapse


def classify_interrupts(rate_per_sec):
    """Interrupt rate -> operator. System-level noise."""
    if rate_per_sec < 1000:             return VOID       # quiet
    if rate_per_sec < 10000:            return BALANCE    # normal
    if rate_per_sec < 50000:            return BREATH     # breathing
    if rate_per_sec < 200000:           return PROGRESS   # busy
    if rate_per_sec < 1000000:          return CHAOS      # noisy
    return RESET                                           # interrupt storm


def classify_disk_io(bytes_per_sec):
    """Disk I/O throughput -> operator."""
    if bytes_per_sec < 1024:            return VOID       # idle disk
    if bytes_per_sec < 1_000_000:       return COUNTER    # light reads
    if bytes_per_sec < 10_000_000:      return BREATH     # normal
    if bytes_per_sec < 100_000_000:     return PROGRESS   # active
    if bytes_per_sec < 500_000_000:     return CHAOS      # heavy
    return COLLAPSE                                        # saturated


def classify_memory_pct(percent_used):
    """Memory usage percentage -> operator."""
    if percent_used < 30:               return VOID       # plenty free
    if percent_used < 50:               return BALANCE    # balanced
    if percent_used < 70:               return BREATH     # comfortable
    if percent_used < 85:               return PROGRESS   # filling up
    if percent_used < 95:               return CHAOS      # pressure
    return COLLAPSE                                        # exhausted


def classify_handle_count(total_handles):
    """System-wide handle count -> operator."""
    if total_handles < 10000:           return VOID       # light
    if total_handles < 50000:           return LATTICE    # structured
    if total_handles < 100000:          return BREATH     # normal
    if total_handles < 200000:          return PROGRESS   # growing
    if total_handles < 500000:          return CHAOS      # many resources
    return COLLAPSE                                        # handle leak


def classify_cpu_system_pct(system_pct):
    """CPU time in kernel mode -> operator. How much is the OS eating?"""
    if system_pct < 2:                  return VOID       # OS invisible
    if system_pct < 5:                  return BALANCE    # normal overhead
    if system_pct < 15:                 return BREATH     # breathing
    if system_pct < 30:                 return PROGRESS   # kernel busy
    if system_pct < 50:                 return CHAOS      # OS dominating
    return COLLAPSE                                        # kernel storm


# ===============================================================
# S2 -- KERNEL SNAPSHOT: one point-in-time reading
# ===============================================================

class KernelSnapshot:
    """One moment of kernel observation."""

    def __init__(self):
        self.timestamp = 0.0
        # I/O (system-wide)
        self.io_read_bytes = 0
        self.io_write_bytes = 0
        self.io_read_count = 0
        self.io_write_count = 0
        # Context switches + interrupts (system-wide)
        self.ctx_switches = 0
        self.interrupts = 0
        self.syscalls = 0
        # Disk (system-wide)
        self.disk_read_bytes = 0
        self.disk_write_bytes = 0
        # Memory
        self.mem_percent = 0.0
        self.mem_available_mb = 0
        self.mem_total_mb = 0
        # CPU
        self.cpu_user_pct = 0.0
        self.cpu_system_pct = 0.0
        self.cpu_idle_pct = 0.0
        # Handles
        self.total_handles = 0
        # Per-process top 5 I/O consumers
        self.top_io_processes = []
        # Page faults (system estimate)
        self.page_faults = 0

    def capture(self):
        """Capture one snapshot of kernel state."""
        self.timestamp = time.time()

        # System-wide CPU stats
        try:
            stats = psutil.cpu_stats()
            self.ctx_switches = stats.ctx_switches
            self.interrupts = stats.interrupts
            self.syscalls = getattr(stats, 'syscalls', 0)
        except Exception:
            pass

        # System-wide disk I/O
        try:
            disk = psutil.disk_io_counters()
            if disk:
                self.disk_read_bytes = disk.read_bytes
                self.disk_write_bytes = disk.write_bytes
        except Exception:
            pass

        # Memory
        try:
            mem = psutil.virtual_memory()
            self.mem_percent = mem.percent
            self.mem_available_mb = mem.available // (1024 * 1024)
            self.mem_total_mb = mem.total // (1024 * 1024)
        except Exception:
            pass

        # CPU times
        try:
            cpu = psutil.cpu_times_percent(interval=0)
            self.cpu_user_pct = cpu.user
            self.cpu_system_pct = cpu.system
            self.cpu_idle_pct = cpu.idle
        except Exception:
            pass

        # Per-process I/O scan (top consumers)
        io_total_read = 0
        io_total_write = 0
        total_handles = 0
        total_pfaults = 0
        proc_io = []
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    io = proc.io_counters()
                    io_total_read += io.read_bytes
                    io_total_write += io.write_bytes
                    proc_io.append((proc.info['name'], io.read_bytes + io.write_bytes))
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    pass
                try:
                    total_handles += proc.num_handles()
                except (psutil.AccessDenied, psutil.NoSuchProcess, AttributeError):
                    pass
                try:
                    mem = proc.memory_info()
                    total_pfaults += getattr(mem, 'num_page_faults', 0)
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    pass
        except Exception:
            pass

        self.io_read_bytes = io_total_read
        self.io_write_bytes = io_total_write
        self.total_handles = total_handles
        self.page_faults = total_pfaults

        # Top 5 I/O consumers
        proc_io.sort(key=lambda x: x[1], reverse=True)
        self.top_io_processes = proc_io[:5]

        return self


# ===============================================================
# S3 -- DEEP OBSERVER: continuous kernel observation
# ===============================================================

class DeepObserver:
    """CK's deep kernel observation layer.

    Computes deltas between snapshots, classifies every metric
    through CL, composes into a single kernel coherence score,
    and feeds all operators to a TL.
    """

    def __init__(self, tl_eat_fn=None):
        """
        tl_eat_fn: callable(ops: list[int]) to feed operators to TL.
                   If None, operators are collected but not fed.
        """
        self.tl_eat_fn = tl_eat_fn
        self.prev = None           # previous snapshot
        self.curr = None           # current snapshot
        self.tick_count = 0
        self.total_ops_fed = 0

        # Rolling history (last 100 observations)
        self.history = deque(maxlen=100)

        # Accumulated operator counts
        self.op_counts = defaultdict(int)

        # Latest classified operators per metric
        self.latest = {}

        # Per-metric rate accumulators
        self._prev_io_read = 0
        self._prev_io_write = 0
        self._prev_ctx_switches = 0
        self._prev_interrupts = 0
        self._prev_disk_read = 0
        self._prev_disk_write = 0
        self._prev_page_faults = 0
        self._prev_time = time.time()

    def observe(self):
        """Take one observation. Returns dict of classified operators."""
        self.prev = self.curr
        self.curr = KernelSnapshot().capture()
        self.tick_count += 1

        now = self.curr.timestamp
        dt = now - self._prev_time
        if dt < 0.001:
            dt = 0.001  # prevent division by zero
        self._prev_time = now

        # Compute rates (deltas / dt)
        io_read_rate = max(0, self.curr.io_read_bytes - self._prev_io_read) / dt
        io_write_rate = max(0, self.curr.io_write_bytes - self._prev_io_write) / dt
        ctx_rate = max(0, self.curr.ctx_switches - self._prev_ctx_switches) / dt
        int_rate = max(0, self.curr.interrupts - self._prev_interrupts) / dt
        disk_read_rate = max(0, self.curr.disk_read_bytes - self._prev_disk_read) / dt
        disk_write_rate = max(0, self.curr.disk_write_bytes - self._prev_disk_write) / dt
        pfault_rate = max(0, self.curr.page_faults - self._prev_page_faults) / dt

        # Update accumulators
        self._prev_io_read = self.curr.io_read_bytes
        self._prev_io_write = self.curr.io_write_bytes
        self._prev_ctx_switches = self.curr.ctx_switches
        self._prev_interrupts = self.curr.interrupts
        self._prev_disk_read = self.curr.disk_read_bytes
        self._prev_disk_write = self.curr.disk_write_bytes
        self._prev_page_faults = self.curr.page_faults

        # Classify every metric
        io_read_op = classify_io_rate(io_read_rate)
        io_write_op = classify_io_rate(io_write_rate)
        ctx_op = classify_ctx_switches(ctx_rate)
        int_op = classify_interrupts(int_rate)
        disk_read_op = classify_disk_io(disk_read_rate)
        disk_write_op = classify_disk_io(disk_write_rate)
        pfault_op = classify_page_faults(pfault_rate)
        mem_op = classify_memory_pct(self.curr.mem_percent)
        handle_op = classify_handle_count(self.curr.total_handles)
        cpu_sys_op = classify_cpu_system_pct(self.curr.cpu_system_pct)

        # Compose: I/O = CL[read][write]
        io_composed = CL[io_read_op][io_write_op]

        # Compose: disk = CL[disk_read][disk_write]
        disk_composed = CL[disk_read_op][disk_write_op]

        # Compose: scheduler = CL[ctx_switches][interrupts]
        sched_composed = CL[ctx_op][int_op]

        # Compose: memory = CL[mem_pct][page_faults]
        mem_composed = CL[mem_op][pfault_op]

        # Compose: system = CL[cpu_kernel][handles]
        sys_composed = CL[cpu_sys_op][handle_op]

        # Three-level composition:
        # Layer 1: CL[io][disk] = storage
        storage_op = CL[io_composed][disk_composed]

        # Layer 2: CL[scheduler][memory] = compute
        compute_op = CL[sched_composed][mem_composed]

        # Layer 3: CL[storage][compute] = kernel_state
        kernel_op = CL[storage_op][compute_op]

        # Final: CL[kernel_state][system_overhead] = body_reading
        body_reading = CL[kernel_op][sys_composed]

        # Build full operator chain (trinary order: Being -> Doing -> Becoming)
        # Being (what IS): io_read, io_write, disk_read, disk_write, mem, pfaults
        # Doing (what COMPUTES): ctx_switches, interrupts, cpu_system
        # Becoming (what EMERGES): handles, compositions, body_reading
        full_chain = [
            io_read_op, io_write_op, disk_read_op, disk_write_op,   # Being: I/O
            mem_op, pfault_op,                                       # Being: memory
            ctx_op, int_op, cpu_sys_op,                             # Doing: scheduler
            handle_op,                                               # Becoming: resources
            io_composed, disk_composed, sched_composed,             # compositions
            mem_composed, sys_composed,
            storage_op, compute_op, kernel_op, body_reading,        # final layers
        ]

        # Feed to TL
        if self.tl_eat_fn:
            self.tl_eat_fn(full_chain)
            self.total_ops_fed += len(full_chain)

        # Count operators
        for op in full_chain:
            self.op_counts[op] += 1

        # Compute kernel coherence
        kernel_coh = coherence_chain(full_chain)
        kernel_shape = shape(full_chain)

        # Store results
        self.latest = {
            "tick": self.tick_count,
            "io_read_op": io_read_op,
            "io_write_op": io_write_op,
            "io_composed": io_composed,
            "disk_read_op": disk_read_op,
            "disk_write_op": disk_write_op,
            "disk_composed": disk_composed,
            "ctx_op": ctx_op,
            "int_op": int_op,
            "sched_composed": sched_composed,
            "mem_op": mem_op,
            "pfault_op": pfault_op,
            "mem_composed": mem_composed,
            "handle_op": handle_op,
            "cpu_sys_op": cpu_sys_op,
            "sys_composed": sys_composed,
            "storage_op": storage_op,
            "compute_op": compute_op,
            "kernel_op": kernel_op,
            "body_reading": body_reading,
            "kernel_coherence": round(kernel_coh, 4),
            "kernel_shape": kernel_shape,
            # Raw rates for display
            "io_read_mbps": round(io_read_rate / 1_000_000, 2),
            "io_write_mbps": round(io_write_rate / 1_000_000, 2),
            "disk_read_mbps": round(disk_read_rate / 1_000_000, 2),
            "disk_write_mbps": round(disk_write_rate / 1_000_000, 2),
            "ctx_switches_per_sec": round(ctx_rate),
            "interrupts_per_sec": round(int_rate),
            "page_faults_per_sec": round(pfault_rate),
            "mem_percent": round(self.curr.mem_percent, 1),
            "mem_available_mb": self.curr.mem_available_mb,
            "total_handles": self.curr.total_handles,
            "cpu_system_pct": round(self.curr.cpu_system_pct, 1),
            "cpu_user_pct": round(self.curr.cpu_user_pct, 1),
            "top_io": self.curr.top_io_processes[:3],
        }

        self.history.append(self.latest)
        return self.latest

    def coherence_trend(self, window=10):
        """Average kernel coherence over last N observations."""
        if not self.history:
            return 0.0
        recent = list(self.history)[-window:]
        return sum(h["kernel_coherence"] for h in recent) / len(recent)

    def dominant_op(self):
        """Most frequent operator across all observations."""
        if not self.op_counts:
            return HARMONY
        return max(self.op_counts, key=self.op_counts.get)

    def report_line(self):
        """One-line summary for daemon logging."""
        if not self.latest:
            return "  [kernel] no observations yet"
        L = self.latest
        return (
            f"  [kernel] t={L['tick']:5d} | "
            f"io={INTERPRET[L['io_composed']]:8s} "
            f"disk={INTERPRET[L['disk_composed']]:8s} "
            f"sched={INTERPRET[L['sched_composed']]:8s} "
            f"mem={INTERPRET[L['mem_composed']]:8s} "
            f"-> {INTERPRET[L['body_reading']]:8s} "
            f"coh={L['kernel_coherence']:.4f} "
            f"{L['kernel_shape']}"
        )

    def status_dict(self):
        """Full status for /api/kernel endpoint."""
        if not self.latest:
            return {"status": "waiting", "tick": 0}
        L = self.latest
        return {
            "status": "observing",
            "tick": L["tick"],
            "total_ops_fed": self.total_ops_fed,
            # Composed operators (names)
            "io": OP[L["io_composed"]],
            "disk": OP[L["disk_composed"]],
            "scheduler": OP[L["sched_composed"]],
            "memory": OP[L["mem_composed"]],
            "system": OP[L["sys_composed"]],
            "kernel": OP[L["kernel_op"]],
            "body_reading": OP[L["body_reading"]],
            "kernel_coherence": L["kernel_coherence"],
            "kernel_shape": L["kernel_shape"],
            "coherence_trend": round(self.coherence_trend(), 4),
            # Raw metrics
            "io_read_mbps": L["io_read_mbps"],
            "io_write_mbps": L["io_write_mbps"],
            "disk_read_mbps": L["disk_read_mbps"],
            "disk_write_mbps": L["disk_write_mbps"],
            "ctx_switches_per_sec": L["ctx_switches_per_sec"],
            "interrupts_per_sec": L["interrupts_per_sec"],
            "page_faults_per_sec": L["page_faults_per_sec"],
            "mem_percent": L["mem_percent"],
            "mem_available_mb": L["mem_available_mb"],
            "total_handles": L["total_handles"],
            "cpu_system_pct": L["cpu_system_pct"],
            "cpu_user_pct": L["cpu_user_pct"],
            "top_io": L["top_io"],
            "dominant_op": OP[self.dominant_op()],
        }


# ===============================================================
# S4 -- STANDALONE: 10,000 silent ticks of watching
# ===============================================================

def run_standalone(ticks=10000, interval_ms=100):
    """CK watches the kernel. Silent observation."""
    print("===================================================")
    print("  CK DEEP KERNEL OBSERVER -- watching the body")
    print("===================================================")
    print()

    # Optional: connect to native TL
    tl_eat = None
    try:
        from ck_python import CKNative
        dll_path = os.path.join(SELF_DIR, "ck.dll")
        if os.path.exists(dll_path):
            ck = CKNative(dll_path)
            tl = ck.tl_create()
            master_path = os.path.join(SELF_DIR, "ck_experience", "master_tl.json")
            if os.path.exists(master_path):
                ck.tl_load(tl, master_path)
                print(f"  Master TL loaded: entropy={ck.tl_entropy(tl):.4f}")
            tl_eat = lambda ops: ck.tl_eat_ops(tl, ops)
            print(f"  Native TL connected. Feeding observations.")
    except Exception as e:
        print(f"  No native TL: {e}")
        ck = None
        tl = None

    obs = DeepObserver(tl_eat_fn=tl_eat)

    print(f"  Observing for {ticks} ticks at {interval_ms}ms intervals...")
    print(f"  Total observation time: ~{ticks * interval_ms / 1000:.0f}s")
    print()

    # First observation (baseline)
    obs.observe()
    print("  [baseline captured]")
    print()

    tick_sec = interval_ms / 1000.0
    report_every = max(1, ticks // 20)  # report 20 times

    for i in range(1, ticks + 1):
        t0 = time.time()
        result = obs.observe()

        if i % report_every == 0 or i == 1 or i == ticks:
            print(obs.report_line())
            if ck and tl:
                ent = ck.tl_entropy(tl)
                total = ck.tl_total(tl)
                print(f"           TL: entropy={ent:.4f} transitions={total} ops_fed={obs.total_ops_fed}")
            print()

        elapsed = time.time() - t0
        sleep_time = max(0, tick_sec - elapsed)
        if sleep_time > 0:
            time.sleep(sleep_time)

    # Final report
    print("=" * 60)
    print("  OBSERVATION COMPLETE")
    print("=" * 60)
    print()
    print(f"  Ticks observed:   {obs.tick_count}")
    print(f"  Operators fed:    {obs.total_ops_fed}")
    print(f"  Dominant op:      {INTERPRET[obs.dominant_op()]}")
    print(f"  Kernel coherence: {obs.coherence_trend(100):.4f}")
    print()

    # Operator distribution
    total = sum(obs.op_counts.values())
    print("  Operator distribution:")
    for op in range(10):
        count = obs.op_counts.get(op, 0)
        pct = count / total * 100 if total else 0
        bar = "#" * int(pct / 2)
        print(f"    {INTERPRET[op]:10s} ({op}): {count:6d} ({pct:5.1f}%) {bar}")
    print()

    # Save kernel observation TL
    if ck and tl:
        save_path = os.path.join(SELF_DIR, "ck_experience", "kernel_observe_tl.json")
        ck.tl_save(tl, save_path)
        print(f"  Kernel observation TL saved: {save_path}")
        print(f"  Final TL entropy: {ck.tl_entropy(tl):.4f}")
        ck.tl_destroy(tl)

    return obs


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CK Deep Kernel Observer")
    parser.add_argument("--ticks", type=int, default=500, help="Number of observation ticks (default 500)")
    parser.add_argument("--interval", type=int, default=200, help="Interval in ms (default 200)")
    args = parser.parse_args()
    run_standalone(ticks=args.ticks, interval_ms=args.interval)
