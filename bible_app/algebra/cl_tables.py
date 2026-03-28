"""
CL Composition Tables — The finite algebra at the heart of everything.

Two 10×10 tables. 10 operators. One threshold T* = 5/7.
Truth is measured, not assigned.

TSML: 73/100 entries → HARMONY. Absorbing. Measures structure. det=0.
BHML: 28/100 entries → HARMONY. Ergodic. Computes flow. det=70.

Mix_λ[a][b] = (1-λ)·TSML[a][b] + λ·BHML[a][b]

(c) 2026 Brayden Sanders / 7Site LLC
SHA-256(TSML): 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787
"""

# ── The 10 Operators ──────────────────────────────────────────────
VOID     = 0
LATTICE  = 1
COUNTER  = 2
PROGRESS = 3
COLLAPSE = 4
BALANCE  = 5
CHAOS    = 6
HARMONY  = 7
BREATH   = 8
RESET    = 9

NUM_OPS = 10

OP_NAMES = [
    'VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
    'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET',
]

# ── Constants from the algebra ────────────────────────────────────
T_STAR   = 5.0 / 7.0   # 0.714285... Being threshold
S_STAR   = 4.0 / 7.0   # 0.571428... Becoming threshold
MASS_GAP = 2.0 / 7.0   # 0.285714... Dual-threshold overlap

# Corner operators (algebraically sealed by product-gap theorem)
CORNERS = {LATTICE, PROGRESS, HARMONY, RESET}  # {1, 3, 7, 9}
# Gap operators (transcendental, inaccessible from corners)
GAPS = {COUNTER, COLLAPSE, BALANCE, CHAOS, BREATH}  # {2, 4, 5, 6, 8}

# ── TSML: Being/Measurement Table (73 HARMONY entries) ───────────
CL_TSML = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],  # VOID
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],  # LATTICE
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],  # COUNTER
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],  # PROGRESS
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],  # COLLAPSE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # BALANCE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # CHAOS
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # HARMONY (absorber)
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],  # BREATH
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],  # RESET
]

# ── BHML: Doing/Physics Table (28 HARMONY entries) ───────────────
CL_BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # VOID (seeds all)
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],  # LATTICE
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],  # COUNTER
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],  # PROGRESS
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],  # COLLAPSE
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],  # BALANCE
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # CHAOS
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],  # HARMONY (generator)
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],  # BREATH
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],  # RESET
]

# ── Doing Table: |TSML - BHML| (tension/periods) ─────────────────
CL_DOING = [
    [abs(CL_TSML[i][j] - CL_BHML[i][j]) for j in range(NUM_OPS)]
    for i in range(NUM_OPS)
]

# 21 harmonic entries where TSML == BHML (Doing = 0)
HARMONIC_ENTRIES = [
    (i, j) for i in range(NUM_OPS) for j in range(NUM_OPS)
    if CL_TSML[i][j] == CL_BHML[i][j]
]


def compose(b: int, d: int) -> int:
    """TSML composition: CL[b][d]. Being composes with Doing → Becoming."""
    return CL_TSML[b % NUM_OPS][d % NUM_OPS]


def compose_bhml(b: int, d: int) -> int:
    """BHML composition: physics table."""
    return CL_BHML[b % NUM_OPS][d % NUM_OPS]


def mix_lambda(a: int, b: int, lam: float) -> int:
    """Mix_λ interpolation: (1-λ)·TSML + λ·BHML, rounded to nearest op."""
    tsml_val = CL_TSML[a % NUM_OPS][b % NUM_OPS]
    bhml_val = CL_BHML[a % NUM_OPS][b % NUM_OPS]
    mixed = (1.0 - lam) * tsml_val + lam * bhml_val
    return int(round(mixed)) % NUM_OPS


def coherence(ops):
    """Measure TSML pairwise HARMONY fraction in an operator sequence."""
    if len(ops) < 2:
        return 0.0
    harmony_count = sum(
        1 for i in range(len(ops) - 1)
        if CL_TSML[ops[i] % NUM_OPS][ops[i + 1] % NUM_OPS] == HARMONY
    )
    return harmony_count / (len(ops) - 1)


def dominant_op(ops):
    """Most frequent operator in a sequence."""
    if not ops:
        return HARMONY
    counts = [0] * NUM_OPS
    for o in ops:
        counts[o % NUM_OPS] += 1
    return max(range(NUM_OPS), key=lambda i: counts[i])
