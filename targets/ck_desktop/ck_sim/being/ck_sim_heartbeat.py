"""
ck_sim_heartbeat.py -- Port of ck_heartbeat.v
==============================================
Operator: HARMONY (7) -- CL[B][D] table lookup per tick.

Software simulation of the FPGA heartbeat module:
  - CL_TSML composition table (73/100 = HARMONY)
  - 32-entry coherence window
  - 5 special-case input pairs
  - Running fuse accumulator

Every number, every threshold matches the Verilog.

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
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

# 5 special-case input pairs (from ck_brain.h line 51-53)
BUMP_PAIRS = [(1, 2), (2, 4), (2, 9), (3, 9), (4, 8)]


def compose(b: int, d: int) -> int:
    """CL[b][d] composition. One line replaces the entire Verilog case statement."""
    if 0 <= b < NUM_OPS and 0 <= d < NUM_OPS:
        return CL[b][d]
    return VOID


def is_bump(b: int, d: int) -> bool:
    """Check if (b, d) is a special-case input pair (either ordering)."""
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
        """One heartbeat tick.

        Current phase_bc enters coherence window on NEXT tick (one-tick delay).
        The coherence window records the PREVIOUS tick's
        result, not this tick's. One-tick delay between composition and window recording.

        Order:
          1. Record PREVIOUS phase_bc into coherence window
          2. Compute NEW phase_bc
          3. Bump detection
          4. Running fuse (accumulated history)
          5. Advance tick

        The current phase_bc is NEVER in the coherence window.
        It enters the window on the NEXT tick. One-tick delay.
        """
        self.phase_b = phase_b
        self.phase_d = phase_d

        # 1. Coherence window: record PREVIOUS tick's result
        # One-tick delay between composition and window recording.
        if self.tick_count > 0:
            prev_bc = self.history[(self.history_ptr - 1) % HISTORY_SIZE]
            # The previous tick's phase_bc was stored in _pending
            if hasattr(self, '_pending_bc'):
                old_val = self.history[self.history_ptr]
                if old_val == HARMONY:
                    self.harmony_count -= 1
                self.history[self.history_ptr] = self._pending_bc
                if self._pending_bc == HARMONY:
                    self.harmony_count += 1
                self.history_ptr = (self.history_ptr + 1) % HISTORY_SIZE

        # Coherence = harmony_count / window_size (always one tick behind)
        filled = min(self.tick_count, HISTORY_SIZE)
        self.coh_num = self.harmony_count
        self.coh_den = max(filled, 1)

        # 2. Compute NEW phase_bc (the present, unmeasured)
        self.phase_bc = compose(phase_b, phase_d)

        # 3. Bump detection (instantaneous, no delay)
        self.bump_detected = is_bump(phase_b, phase_d)

        # 4. Store this tick's result for NEXT tick's measurement
        self._pending_bc = self.phase_bc

        # 5. Running fuse (accumulated composition, always current)
        self.running_fuse = compose(self.running_fuse, self.phase_bc)

        # 6. Advance tick (time passes)
        self.tick_count += 1

    @property
    def coherence(self) -> float:
        """Current coherence as float."""
        if self.coh_den == 0:
            return 0.0
        return self.coh_num / self.coh_den
