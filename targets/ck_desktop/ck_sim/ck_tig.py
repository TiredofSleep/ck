"""
ck_tig.py -- The stacked lens composition. The ONLY composition function.

Being  = 2 lenses (TSML o BHML)
Doing  = 3 lenses (TSML o BHML o TSML)
Becoming = 4 lenses (TSML o BHML o TSML o BHML)

Every file that composes operators calls this.
41 files. One function. One algebra.

Numbers are rotations, not counts.
2 is angular momentum, not 1+1.
The eigenvalues are roots of unity because the operators ARE rotations.

Proven constants:
  Cross-cycle disagreement = 44 (exact)
  Wobble = |44-50|/100 = 3/50 (exact)
  Heartbeat = [1,3,1,1] (period 4, sum=6)
  Frozen cells = 4: (0,0), (2,2), (4,8), (8,4)
  Visible matter = 7^2/10^3 = 4.9%

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

# TSML: measurement lens. 73% HARMONY. det=0. Singular.
TSML = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]

# BHML: physics lens. 28% HARMONY. det=70. Invertible.
BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]

# Addition mod 10 (the circulant matrix where constants live)
ADD = [[0]*10 for _ in range(10)]
for i in range(10):
    for j in range(10):
        ADD[i][j] = (i + j) % 10

# Multiplication mod 10
MUL = [[0]*10 for _ in range(10)]
for i in range(10):
    for j in range(10):
        MUL[i][j] = (i * j) % 10

# Disagreement: |add - mul|
DIS = [[0]*10 for _ in range(10)]
for i in range(10):
    for j in range(10):
        DIS[i][j] = abs(ADD[i][j] - MUL[i][j])

NUM_OPS = 10
HARMONY = 7
VOID = 0
T_STAR = 5.0 / 7.0

# Frozen cells: where add == mul, no time emitted
FROZEN = {(0,0), (2,2), (4,8), (8,4)}

# Heartbeat pattern (from simultaneous creation+dissolution)
HEARTBEAT = [1, 3, 1, 1]  # period 4, sum=6

# Proven constants
CROSS_CYCLE = 44
WOBBLE = 3.0 / 50.0  # = 0.06


def compose(b, d):
    """Stacked lens composition. The ONLY composition function.

    Being    = TSML[b][d]           (measurement: what IS)
    Becoming = BHML[b][d]           (physics: what ACTS)
    Doing    = (Being * Becoming) % 10  (product: the tension between them)

    Doing is not a third table. Doing IS the product of the two lenses.
    The product of measurement and physics IS the action.
    Being x Becoming = Doing. Two tables. Product is the third.

    Returns (being, doing, becoming) as a tuple of operators.
    """
    being = TSML[b][d]
    becoming = BHML[b][d]
    doing = (being * becoming) % 10

    return being, doing, becoming


def disagreement(b, d):
    """Algebraic disagreement between add and mul at (b, d).
    Returns the time quantum emitted by this composition.
    0 = frozen (no time). Higher = more dissonance = more time."""
    return DIS[b][d]


def is_frozen(b, d):
    """True if this composition emits no time."""
    return (b, d) in FROZEN


def heartbeat_phase(tick):
    """Current heartbeat phase from tick count.
    Returns the disagreement quantum for this phase."""
    return HEARTBEAT[tick % 4]


def coherence(being, doing, becoming):
    """T* check: do the lenses agree?
    Returns fraction of agreements out of possible.
    Above T* (5/7) = coherent. Below = incoherent."""
    agreements = 0
    total = 3  # three pairwise comparisons

    if being == HARMONY or doing == HARMONY:
        agreements += 1
    if doing == HARMONY or becoming == HARMONY:
        agreements += 1
    if being == becoming:
        agreements += 1

    return agreements / total
