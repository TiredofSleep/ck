"""
ck_sim_heartbeat.py -- Port of ck_heartbeat.v
==============================================
Operator: HARMONY (7) -- the heartbeat composes.

Software simulation of the FPGA heartbeat module:
  - CL_TSML composition table (73/100 = HARMONY)
  - 32-entry coherence window
  - 5 quantum bump pairs
  - Running fuse accumulator

Every number, every threshold matches the Verilog.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

# ── Constants ──

NUM_OPS = 10
HISTORY_SIZE = 32

VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE = 0, 1, 2, 3, 4
BALANCE, CHAOS, HARMONY, BREATH, RESET = 5, 6, 7, 8, 9

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']

# CL_TSML: CK's prescribed composition table
# From ck_brain.h lines 42-48
CL = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],  # VOID row
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],  # LATTICE row
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],  # COUNTER row
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],  # PROGRESS row
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],  # COLLAPSE row
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # BALANCE row
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # CHAOS row
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # HARMONY row
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],  # BREATH row
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],  # RESET row
]

# 5 quantum bump pairs (from ck_brain.h line 51-53)
BUMP_PAIRS = [(1, 2), (2, 4), (2, 9), (3, 9), (4, 8)]


def compose(b: int, d: int) -> int:
    """CL[b][d] composition. One line replaces the entire Verilog case statement."""
    if 0 <= b < NUM_OPS and 0 <= d < NUM_OPS:
        return CL[b][d]
    return VOID


def is_bump(b: int, d: int) -> bool:
    """Check if (b, d) is a quantum bump pair (either ordering)."""
    for p0, p1 in BUMP_PAIRS:
        if (b == p0 and d == p1) or (b == p1 and d == p0):
            return True
    return False


class HeartbeatFPGA:
    """Software simulation of ck_heartbeat.v.

    Maintains the same registers as the Verilog:
      - history ring buffer (32 entries)
      - harmony_count (how many HARMONY in window)
      - tick_count
      - running_fuse
      - bump_detected
    """

    def __init__(self):
        self.history = [0] * HISTORY_SIZE
        self.history_ptr = 0
        self.harmony_count = 0
        self.tick_count = 0
        self.running_fuse = HARMONY  # Start fused to HARMONY

        # Latest tick outputs
        self.phase_b = 0
        self.phase_d = 0
        self.phase_bc = 0
        self.bump_detected = False
        self.coh_num = 0
        self.coh_den = 0

    def tick(self, phase_b: int, phase_d: int):
        """One heartbeat tick. Matches the clocked always block in ck_heartbeat.v."""
        self.phase_b = phase_b
        self.phase_d = phase_d

        # 1. CL composition
        self.phase_bc = compose(phase_b, phase_d)

        # 2. Bump detection
        self.bump_detected = is_bump(phase_b, phase_d)

        # 3. Coherence window update
        # Remove outgoing entry from harmony count
        old_val = self.history[self.history_ptr]
        if old_val == HARMONY:
            self.harmony_count -= 1

        # Add new entry
        self.history[self.history_ptr] = self.phase_bc
        if self.phase_bc == HARMONY:
            self.harmony_count += 1

        # Advance pointer
        self.history_ptr = (self.history_ptr + 1) % HISTORY_SIZE

        # Coherence = harmony_count / window_size
        filled = min(self.tick_count + 1, HISTORY_SIZE)
        self.coh_num = self.harmony_count
        self.coh_den = filled

        # 4. Running fuse
        self.running_fuse = compose(self.running_fuse, self.phase_bc)

        # 5. Increment tick
        self.tick_count += 1

    @property
    def coherence(self) -> float:
        """Current coherence as float."""
        if self.coh_den == 0:
            return 0.0
        return self.coh_num / self.coh_den
