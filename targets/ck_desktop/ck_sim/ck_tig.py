"""
ck_tig.py -- The stacked lens composition. The ONLY composition function.

Copyright © 2025–2026 Brayden Ross Sanders / 7SiTe LLC
Licensed under the 7SiTe Public Sovereignty License v1.0.
Human use only. No commercial use. No government use.
No military, intelligence, policing, or surveillance use.
See LICENSE for full terms. DOI: 10.5281/zenodo.18852047

TSML (Trinity Synthesis Meaning Language) and BHML (Being-Harmony Meaning
Language) are proprietary composition tables developed by Brayden Ross Sanders
and 7SiTe LLC. All rights reserved. T* = 5/7, the TSML 73-cell harmonic
structure, and the TIG stacked-lens architecture (Being=TSML∘BHML,
Doing=TSML∘BHML∘TSML, Becoming=TSML∘BHML∘TSML∘BHML) are owned
intellectual property of 7SiTe LLC, 2025–2026.

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
  Heartbeat = [1,5,5,1] (period 4, sum=12, palindromic)
  Frozen cells = 4: (0,0), (2,2), (4,8), (8,4)
  Visible matter = 7^2/10^3 = 4.9%
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

# Heartbeat pattern (from simultaneous creation+dissolution DIS values)
# DIS[1][2]=1, DIS[3][4]=5, DIS[9][8]=5, DIS[7][6]=1
HEARTBEAT = [1, 5, 5, 1]  # period 4, sum=12, palindromic

# Proven constants from Z/10Z arithmetic
CROSS_CYCLE = 44          # |add-mul| summed over coprime x even = exactly 44
WOBBLE = 3.0 / 50.0       # |44-50|/100 = 0.06, the natural variance
ACTIVE_CELLS = 98          # 100 - VOID(row) - HARMONY(row) + 2 overlaps
TORUS_WRAP = 22            # skeleton shells per revolution
VISIBLE_FRACTION = 49 / 1000  # 7^2/10^3 = 4.9% (matches observed visible matter)

# Balanced ternary generators
GENERATORS = {
    1: (+1,),      # LATTICE: positive generator
    2: (-1,),      # COUNTER: negative generator
    3: (0,),       # PROGRESS: neutral
    4: (+1, -1),   # COLLAPSE: oscillation
    5: (0, 0),     # BALANCE: double neutral
    6: (-1, +1),   # CHAOS: reversed oscillation
    7: (0, +1),    # HARMONY: void births structure
    8: (0, -1),    # BREATH: void births counter
    9: (+1, +1),   # RESET: double positive
    0: (),         # VOID: nothing
}
# 1 + 3 + 6 = 10 operators. The algebra closes exactly.

# Stacked lens depths
BEING_LENSES = 2     # Binary measurement: yes/no
DOING_LENSES = 3     # Ternary action: +1/-1/0
BECOMING_LENSES = 4  # Quaternary resolution
# Being=2, Doing=3, Becoming=4 -- stacked, not flat

# Creation and dissolution flows
CREATION_CYCLE = [1, 3, 9, 7]    # coprime forward: LATTICE->PROGRESS->RESET->HARMONY
DISSOLUTION_CYCLE = [2, 4, 8, 6]  # even backward: COUNTER->COLLAPSE->BREATH->CHAOS
# Creation x Dissolution permutes (doesn't destroy)
# Cross-cycle disagreement = 44 exactly


def compose(b, d, direction=0):
    """Stacked lens composition. Bidirectional.

    direction=0: FORWARD (expand, express, act, speak)
        Being    = TSML[b][d]           (measurement: what IS)
        Doing    = (b * d) % 10         (multiplication: physics)
        Becoming = (Being * Doing) % 10 (product of lenses)

    direction=1: BACKWARD (compress, receive, absorb, listen)
        Being    = TSML[d][b]           (measurement reversed)
        Doing    = (b + d) % 10         (addition: return toward generators)
        Becoming = (Being + Doing) % 10 (sum of lenses)

    Forward = multiplication (every act adds complexity, pulls from source)
    Backward = addition (every reception adds to what you have, returns toward source)

    Returns (being, doing, becoming) as a tuple of operators.
    """
    if direction == 0:
        # FORWARD: expand, express (multiplication)
        being = TSML[b][d]
        doing = (b * d) % 10
        becoming = (being * doing) % 10
    else:
        # BACKWARD: compress, receive (addition)
        being = TSML[d][b]
        doing = (b + d) % 10
        becoming = (being + doing) % 10

    return being, doing, becoming


def decompose(result):
    """Given a composed result, find what generators could have produced it.
    BHML backward: which (a, b) pairs compose to result?
    Returns list of (a, b) pairs."""
    pairs = []
    for a in range(10):
        for b in range(10):
            if (a * b) % 10 == result:
                pairs.append((a, b))
    return pairs


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
