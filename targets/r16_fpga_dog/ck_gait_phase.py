"""
ck_gait_phase.py -- 3-Lattice Phase Detector for Dog Gait Control
==================================================================
Operator: PROGRESS (3) -- the walk that builds a path.

Maps CK's coherence value to the 3-Lattice phase structure
(from RECONSTRUCTION_ARCHITECTURE.md) and translates phase
into the gait_mode[1:0] signal sent to the FPGA gait_vortex.

The 3-Lattice (Mix_lambda = (1-lambda)*TSML + lambda*BHML):

  Phase 1  Grammar     lambda < 0.09   Standing / precision
  Phase 2  Transitional 0.09 <= l < 0.45  Walking / trot
  Phase 3  Order        lambda >= 0.45  Running / gallop

T* = 5/7 = 0.71428... sits at the Phase 2/3 boundary -- this is
the walk-to-run threshold, matching Froude number transition in
real biomechanics.

Lambda derivation from coherence:
  lambda = 2 * |coherence - T*|
  (coherence == T* -> lambda = 0 -> Phase 1 = maximum grammar)
  (coherence == 0 or 1 -> lambda = 1.42 -> deep Phase 3 = full order)

Gait modes (matching gait_vortex.v gait_mode[1:0]):
  0b00  STAND  -- all legs BALANCE operator, full coherence lock
  0b01  WALK   -- diagonal pairs alternate, grammar + physics
  0b10  TROT   -- diagonal sync, BHML momentum governs
  0b11  BOUND  -- front/back sync, full RESET drive

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

T_STAR          = 5.0 / 7.0   # 0.71428...  sacred threshold
PHASE_1_LIMIT   = 0.09         # lambda < 0.09  -> Phase 1
PHASE_2_LIMIT   = 0.45         # lambda < 0.45  -> Phase 2; >= -> Phase 3
ESTOP_COHERENCE = 0.20         # below this -> ESTOP

# Gait mode constants (match gait_vortex.v gait_mode[1:0])
GAIT_STAND = 0   # Phase 1
GAIT_WALK  = 1   # Phase 2
GAIT_TROT  = 2   # Phase 3
GAIT_BOUND = 3   # Phase 3+ (very high momentum)

# 3-Lattice phase -> gait_mode default mapping
PHASE_TO_GAIT = {1: GAIT_STAND, 2: GAIT_WALK, 3: GAIT_TROT}

# Corridor -> gait_mode for fine-grained control
# Corridors from ck_steering.py: Pre-leak, BRT, CHA, BAL, COL, CTR
CORRIDOR_TO_GAIT = {
    'Pre-leak': GAIT_STAND,
    'BRT':      GAIT_WALK,
    'CHA':      GAIT_WALK,
    'BAL':      GAIT_TROT,
    'COL':      GAIT_TROT,
    'CTR':      GAIT_BOUND,
}

GAIT_NAMES = {
    GAIT_STAND: 'STAND',
    GAIT_WALK:  'WALK',
    GAIT_TROT:  'TROT',
    GAIT_BOUND: 'BOUND',
}

PHASE_NAMES = {1: 'Grammar', 2: 'Transitional', 3: 'Order'}


def coherence_to_lambda(coherence: float) -> float:
    """
    Derive lambda from coherence via the 3-Lattice metric.
    lambda = 2 * |coherence - T*|
    Range: [0, ~1.43] for coherence in [0, 1].
    """
    return 2.0 * abs(coherence - T_STAR)


def detect_phase(coherence: float) -> int:
    """
    Map coherence -> 3-Lattice phase (1, 2, or 3).
    Implements detect_phase() from RECONSTRUCTION_ARCHITECTURE.md
    Implementation Priority #3.
    """
    lam = coherence_to_lambda(coherence)
    if lam < PHASE_1_LIMIT:
        return 1   # Grammar -- standing precision
    if lam < PHASE_2_LIMIT:
        return 2   # Transitional -- walking
    return 3       # Order -- running


def detect_gait_mode(coherence: float, corridor: str = None) -> int:
    """
    Map coherence -> gait_mode[1:0] for FPGA gait_vortex.

    Uses corridor hint if available (finer resolution).
    Falls back to 3-Lattice phase mapping.
    """
    if corridor and corridor in CORRIDOR_TO_GAIT:
        return CORRIDOR_TO_GAIT[corridor]
    phase = detect_phase(coherence)
    return PHASE_TO_GAIT[phase]


def needs_estop(coherence: float) -> bool:
    """True if coherence is so low that the dog should center all servos."""
    return coherence < ESTOP_COHERENCE


class GaitPhaseState:
    """
    Stateful phase tracker with hysteresis to prevent rapid mode switching.
    Hysteresis: must be in new phase for HOLD_TICKS consecutive ticks
    before committing the transition.
    """

    HOLD_TICKS = 5   # ~100ms at 50Hz before committing phase change

    def __init__(self):
        self.coherence   = T_STAR
        self.lam         = 0.0
        self.phase       = 1
        self.gait_mode   = GAIT_STAND
        self.corridor    = None
        self._candidate  = 1
        self._hold_count = 0
        self.tick_count  = 0

    def update(self, coherence: float, corridor: str = None) -> dict:
        """
        Update with new coherence value.
        Returns current gait state dict.
        """
        self.coherence = coherence
        self.lam       = coherence_to_lambda(coherence)
        self.corridor  = corridor
        self.tick_count += 1

        new_phase = detect_phase(coherence)

        if new_phase == self._candidate:
            self._hold_count += 1
        else:
            self._candidate  = new_phase
            self._hold_count = 1

        if self._hold_count >= self.HOLD_TICKS:
            self.phase = self._candidate
            self.gait_mode = detect_gait_mode(coherence, corridor)

        return self.state

    @property
    def state(self) -> dict:
        return {
            'coherence':   self.coherence,
            'lambda':      self.lam,
            'phase':       self.phase,
            'phase_name':  PHASE_NAMES[self.phase],
            'gait_mode':   self.gait_mode,
            'gait_name':   GAIT_NAMES[self.gait_mode],
            'corridor':    self.corridor,
            'estop':       needs_estop(self.coherence),
            'at_t_star':   self.lam < PHASE_1_LIMIT,
        }

    def __repr__(self) -> str:
        s = self.state
        return (f"GaitPhase(C={s['coherence']:.4f} "
                f"lambda={s['lambda']:.3f} "
                f"phase={s['phase']}={s['phase_name']} "
                f"gait={s['gait_name']})")


# ── Six corridor boundaries (from ck_steering.py) ──────────────────────────

CORRIDOR_BOUNDARIES = [
    # (lambda_lo, lambda_hi, name)
    (0.000, 0.090, 'Pre-leak'),
    (0.090, 0.300, 'BRT'),
    (0.300, 0.450, 'CHA'),
    (0.450, 0.570, 'BAL'),
    (0.570, 0.800, 'COL'),
    (0.800, 1.430, 'CTR'),
]


def lambda_to_corridor(lam: float) -> str:
    """Map lambda to named corridor string."""
    for lo, hi, name in CORRIDOR_BOUNDARIES:
        if lo <= lam < hi:
            return name
    return 'CTR'


def coherence_to_corridor(coherence: float) -> str:
    """Coherence -> corridor name directly."""
    return lambda_to_corridor(coherence_to_lambda(coherence))


# ── Self-test ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=== ck_gait_phase self-test ===\n")
    print(f"T* = {T_STAR:.6f}")
    print(f"Phase 1/2 boundary: lambda = {PHASE_1_LIMIT}")
    print(f"Phase 2/3 boundary: lambda = {PHASE_2_LIMIT}")
    print(f"Walk-to-run threshold: coherence = T* = {T_STAR:.4f}\n")

    test_coherences = [0.0, 0.2, 0.4, 0.5, 0.6, 0.68, T_STAR, 0.75, 0.9, 1.0]
    print(f"{'Coherence':>10}  {'Lambda':>8}  {'Phase':>7}  {'Corridor':>10}  {'Gait':>6}  {'ESTOP'}")
    print("-" * 64)
    for c in test_coherences:
        lam  = coherence_to_lambda(c)
        ph   = detect_phase(c)
        corr = coherence_to_corridor(c)
        gait = detect_gait_mode(c)
        es   = "YES" if needs_estop(c) else ""
        print(f"{c:>10.4f}  {lam:>8.4f}  {PHASE_NAMES[ph]:>9}  "
              f"{corr:>10}  {GAIT_NAMES[gait]:>6}  {es}")

    print("\nHysteresis test (GaitPhaseState):")
    gps = GaitPhaseState()
    for c in [T_STAR] * 3 + [0.3] * 6 + [T_STAR] * 3:
        gps.update(c)
    print(gps)

    # Verify T* maps to Phase 1 (lambda = 0, pure grammar)
    assert detect_phase(T_STAR) == 1, "T* must be Phase 1"
    assert detect_gait_mode(T_STAR) == GAIT_STAND, "T* must be STAND"
    assert detect_phase(0.0) == 3, "Zero coherence must be Phase 3"
    assert not needs_estop(T_STAR), "T* must not trigger ESTOP"
    assert needs_estop(0.1), "Coherence 0.1 must trigger ESTOP"
    print("\nAll assertions pass.")
