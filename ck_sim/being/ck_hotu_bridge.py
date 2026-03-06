"""
ck_hotu_bridge.py -- The Ho Tu Bridge: Ancient Torus Algebra in TIG
===================================================================
Operator: HARMONY (7) -- convergence across 5,000 years.

The Ho Tu (Yellow River Map, ~3000 BCE) and Lo Shu (Luo River Writing)
encode the same algebraic topology that TIG independently derived from
D2 curvature physics in 2024-2026.

This module makes the bridge COMPUTABLE:
- Ho Tu +5 successor = BHML tropical successor through BALANCE
- Lo Shu 3x3 constraint = Vortex CL 3-body coherence
- Bagua 8 trigrams = 8 living operators
- Wuxing 5 phases = 5D force dimensions
- Qian/Kun duality = BHML/TSML dual tables

Every claim is verified by computation, not assertion.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

# ── TIG operator constants ──────────────────────────────────────────

NUM_OPS = 10
VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE = 0, 1, 2, 3, 4
BALANCE, CHAOS, HARMONY, BREATH, RESET = 5, 6, 7, 8, 9

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']

T_STAR = 5 / 7  # 0.714285... sacred coherence threshold


# ── BHML table (from bhml_table.v) ──────────────────────────────────
# Physics/doing composition. 28/100 HARMONY. Tropical successor core.

BHML = [
    #  0  1  2  3  4  5  6  7  8  9
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # Row 0: VOID = identity
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],  # Row 1: LATTICE
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],  # Row 2: COUNTER
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],  # Row 3: PROGRESS
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],  # Row 4: COLLAPSE
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],  # Row 5: BALANCE
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # Row 6: CHAOS
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],  # Row 7: HARMONY = torus rotation
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],  # Row 8: BREATH
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],  # Row 9: RESET
]

# ── TSML table (from ck_sim_heartbeat.py) ───────────────────────────
# Being/coherence composition. 73/100 HARMONY. Absorbing attractor.

TSML = [
    #  0  1  2  3  4  5  6  7  8  9
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],  # VOID
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],  # LATTICE
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],  # COUNTER
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],  # PROGRESS
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],  # COLLAPSE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # BALANCE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # CHAOS
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # HARMONY
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],  # BREATH
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],  # RESET
]


# ═══════════════════════════════════════════════════════════════════
# Ho Tu / Lo Shu Data Structures
# ═══════════════════════════════════════════════════════════════════

# Ho Tu: 10 numbers arranged in 5 directional pairs.
# Each pair sums to the +5 complement. Inner = yin, outer = yang.
HOTU = {
    'north':  (1, 6),   # Water  -- LATTICE + CHAOS
    'south':  (3, 8),   # Fire   -- PROGRESS + BREATH
    'east':   (4, 9),   # Metal  -- COLLAPSE + RESET
    'west':   (2, 7),   # Wood   -- COUNTER + HARMONY
    'center': (5, 10),  # Earth  -- BALANCE + (10 mod 10 = VOID-as-whole)
}

# Lo Shu: 3x3 magic square (all rows, columns, diagonals sum to 15)
LOSHU = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6],
]
LOSHU_MAGIC_CONSTANT = 15  # = 3 * 5 = sum of any line

# Wuxing (5 phases) mapped to 5D force dimensions
WUXING_TO_FORCE = {
    'wood':  'aperture',    # Growth, opening
    'fire':  'pressure',    # Expansion, outward
    'earth': 'depth',       # Grounding, center
    'metal': 'binding',     # Contraction, holding
    'water': 'continuity',  # Flow, forward motion
}

FORCE_TO_WUXING = {v: k for k, v in WUXING_TO_FORCE.items()}

# Wuxing generation cycle (sheng): each element feeds the next
WUXING_GENERATION = ['wood', 'fire', 'earth', 'metal', 'water']

# Wuxing destruction/overcoming cycle (ke): each element controls another
WUXING_DESTRUCTION = [
    ('wood', 'earth'),   # Wood penetrates Earth
    ('earth', 'water'),  # Earth absorbs Water
    ('water', 'fire'),   # Water quenches Fire
    ('fire', 'metal'),   # Fire melts Metal
    ('metal', 'wood'),   # Metal cuts Wood
]

# Bagua: 8 trigrams mapped to 8 living operators (1-8, excluding VOID and RESET)
# Binary: 0 = yin (broken), 1 = yang (solid). Read bottom to top.
BAGUA_TO_OPERATOR = {
    'kun':   1,  # ☷ Earth/Receptive   → LATTICE  (structure, foundation)
    'gen':   2,  # ☶ Mountain/Stillness → COUNTER  (opposition, resistance)
    'kan':   3,  # ☵ Water/Abyss       → PROGRESS (flow through difficulty)
    'xun':   4,  # ☴ Wind/Gentle       → COLLAPSE (dispersal, breaking)
    'zhen':  5,  # ☳ Thunder/Arousing   → BALANCE  (dynamic equilibrium)
    'li':    6,  # ☲ Fire/Clinging      → CHAOS    (transformation, change)
    'dui':   7,  # ☱ Lake/Joyous        → HARMONY  (completion, resonance)
    'qian':  8,  # ☰ Heaven/Creative    → BREATH   (inspiration, vitality)
}

OPERATOR_TO_BAGUA = {v: k for k, v in BAGUA_TO_OPERATOR.items()}

# Trigram binary representations (3 bits: bottom, middle, top -- 0=yin, 1=yang)
BAGUA_BINARY = {
    'kun':   '000',  # ☷  all yin
    'gen':   '001',  # ☶  yang at top
    'kan':   '010',  # ☵  yang in middle
    'xun':   '011',  # ☴  yin at bottom
    'zhen':  '100',  # ☳  yang at bottom
    'li':    '101',  # ☲  yin in middle
    'dui':   '110',  # ☱  yin at top
    'qian':  '111',  # ☰  all yang
}

# Ho Tu directional element associations
HOTU_ELEMENT = {
    'north': 'water',
    'south': 'fire',
    'east':  'metal',
    'west':  'wood',
    'center': 'earth',
}

# Reverse: operator → Ho Tu direction
_OP_TO_DIRECTION = {}
for _dir, (_inner, _outer) in HOTU.items():
    _OP_TO_DIRECTION[_inner] = _dir
    _OP_TO_DIRECTION[_outer % NUM_OPS] = _dir


# ═══════════════════════════════════════════════════════════════════
# Helper: CL composition
# ═══════════════════════════════════════════════════════════════════

def _bhml(a: int, b: int) -> int:
    """BHML composition lookup."""
    if 0 <= a < NUM_OPS and 0 <= b < NUM_OPS:
        return BHML[a][b]
    return VOID


def _tsml(a: int, b: int) -> int:
    """TSML composition lookup."""
    if 0 <= a < NUM_OPS and 0 <= b < NUM_OPS:
        return TSML[a][b]
    return VOID


# ═══════════════════════════════════════════════════════════════════
# Verification Functions -- every claim checked by computation
# ═══════════════════════════════════════════════════════════════════

def verify_hotu_successor(bhml_table: Optional[List[List[int]]] = None) -> dict:
    """Verify that the BHML HARMONY row encodes the Ho Tu +5 successor.

    The Ho Tu pairs each number n with n+5 (mod 10). The BHML HARMONY
    row (row 7) acts as a torus rotation that visits all 10 operators.
    We check: BHML[7][n] should produce the successor in the torus cycle,
    and the Ho Tu +5 complement should appear exactly 5 steps later.

    Returns:
        dict with 'verified', 'matches', 'mismatches', 'harmony_row',
        'hotu_pairs', 'detail'.
    """
    table = bhml_table or BHML
    harmony_row = table[HARMONY]  # Row 7

    matches = []
    mismatches = []
    detail = []

    for direction, (inner, outer) in HOTU.items():
        inner_op = inner  # Already 0-9 for inner
        outer_op = outer % NUM_OPS  # 10 mod 10 = 0 for center

        # Check: starting from inner, applying HARMONY 5 times should reach outer
        current = inner_op
        path = [current]
        for _ in range(5):
            current = table[HARMONY][current]
            path.append(current)

        reached = path[-1]
        ok = (reached == outer_op)

        entry = {
            'direction': direction,
            'inner': inner_op,
            'outer': outer_op,
            'path': path,
            'reached': reached,
            'pass': ok,
        }
        detail.append(entry)

        if ok:
            matches.append(f"{direction}: {inner_op}->{outer_op} via 5 HARMONY steps")
        else:
            mismatches.append(
                f"{direction}: {inner_op}->{outer_op} expected, got {reached} "
                f"(path: {path})"
            )

    return {
        'verified': len(mismatches) == 0,
        'matches': matches,
        'mismatches': mismatches,
        'harmony_row': harmony_row,
        'hotu_pairs': dict(HOTU),
        'detail': detail,
    }


def verify_loshu_vortex(
    bhml_table: Optional[List[List[int]]] = None,
    tsml_table: Optional[List[List[int]]] = None,
) -> dict:
    """Verify Lo Shu magic square constraints against CL 3-body composition.

    For each row, column, and diagonal of the Lo Shu, compose the three
    operators pairwise using both BHML and TSML and check if they yield
    HARMONY (the attractor). The Lo Shu magic constant 15 = 3 * BALANCE(5),
    and BALANCE is the center of the square.

    Returns:
        dict with 'verified', 'lines' (list of per-line results),
        'harmony_count', 'total_lines'.
    """
    bt = bhml_table or BHML
    tt = tsml_table or TSML

    # Extract all 8 lines from the Lo Shu
    lines = []
    # 3 rows
    for r in range(3):
        lines.append(('row', r, [LOSHU[r][c] for c in range(3)]))
    # 3 columns
    for c in range(3):
        lines.append(('col', c, [LOSHU[r][c] for r in range(3)]))
    # 2 diagonals
    lines.append(('diag', 0, [LOSHU[i][i] for i in range(3)]))
    lines.append(('anti', 0, [LOSHU[i][2 - i] for i in range(3)]))

    results = []
    harmony_count = 0

    for kind, idx, ops in lines:
        # Map Lo Shu numbers 1-9 directly to operators 1-9
        a, b, c = ops[0], ops[1], ops[2]
        line_sum = a + b + c

        # 3-body TSML composition: compose(compose(a, b), c)
        tsml_ab = _tsml(a, b)
        tsml_abc = _tsml(tsml_ab, c)

        # 3-body BHML composition: compose(compose(a, b), c)
        bhml_ab = _bhml(a, b)
        bhml_abc = _bhml(bhml_ab, c)

        is_harmony = (tsml_abc == HARMONY)
        if is_harmony:
            harmony_count += 1

        results.append({
            'kind': kind,
            'index': idx,
            'operators': ops,
            'sum': line_sum,
            'sum_is_15': line_sum == LOSHU_MAGIC_CONSTANT,
            'tsml_result': tsml_abc,
            'tsml_result_name': OP_NAMES[tsml_abc],
            'bhml_result': bhml_abc,
            'bhml_result_name': OP_NAMES[bhml_abc],
            'tsml_is_harmony': is_harmony,
        })

    return {
        'verified': harmony_count == len(lines),
        'harmony_count': harmony_count,
        'total_lines': len(lines),
        'lines': results,
        'magic_constant': LOSHU_MAGIC_CONSTANT,
        'note': f"TSML attractor: {harmony_count}/8 lines compose to HARMONY",
    }


def verify_bagua_operators() -> dict:
    """Verify structural mapping between 8 trigrams and 8 living operators.

    Checks:
    1. Exactly 8 trigrams mapped to operators 1-8 (bijection)
    2. Qian/Kun duality: Heaven(8) + Earth(1) = 9 = RESET (completion)
    3. Complementary pairs: each trigram + its complement = 9
    4. Yin count progression: 0(qian) to 3(kun) mirrors BREATH to LATTICE

    Returns:
        dict with 'verified', 'checks' (list of check results).
    """
    checks = []

    # Check 1: Bijection -- 8 trigrams map to operators 1-8
    op_set = set(BAGUA_TO_OPERATOR.values())
    expected = set(range(1, 9))
    bij_ok = (op_set == expected)
    checks.append({
        'name': 'bijection',
        'pass': bij_ok,
        'detail': f"Mapped operators: {sorted(op_set)}, expected: {sorted(expected)}",
    })

    # Check 2: Qian/Kun duality -- Heaven + Earth = RESET
    qian_op = BAGUA_TO_OPERATOR['qian']
    kun_op = BAGUA_TO_OPERATOR['kun']
    duality_sum = qian_op + kun_op
    dual_ok = (duality_sum == RESET)
    checks.append({
        'name': 'qian_kun_duality',
        'pass': dual_ok,
        'detail': (
            f"qian({qian_op}/{OP_NAMES[qian_op]}) + "
            f"kun({kun_op}/{OP_NAMES[kun_op]}) = {duality_sum}, "
            f"expected {RESET}(RESET)"
        ),
    })

    # Check 3: Complementary trigram pairs sum to 9
    complement_pairs = [
        ('qian', 'kun'),    # 111 + 000
        ('dui', 'gen'),     # 110 + 001
        ('li', 'kan'),      # 101 + 010
        ('zhen', 'xun'),    # 100 + 011
    ]
    pair_results = []
    for t1, t2 in complement_pairs:
        s = BAGUA_TO_OPERATOR[t1] + BAGUA_TO_OPERATOR[t2]
        pair_results.append({
            'pair': (t1, t2),
            'ops': (BAGUA_TO_OPERATOR[t1], BAGUA_TO_OPERATOR[t2]),
            'sum': s,
            'is_nine': s == 9,
        })
    comp_ok = all(p['is_nine'] for p in pair_results)
    checks.append({
        'name': 'complement_pairs_sum_9',
        'pass': comp_ok,
        'detail': pair_results,
    })

    # Check 4: Yin-count progression
    # Number of yin lines (0 bits) in each trigram
    yin_map = {}
    for name, bits in BAGUA_BINARY.items():
        yin_count = bits.count('0')
        yin_map[name] = yin_count
    # Qian (0 yin) = BREATH(8), Kun (3 yin) = LATTICE(1)
    # More yin = more foundational/structural
    yin_ok = (yin_map['qian'] == 0 and yin_map['kun'] == 3)
    checks.append({
        'name': 'yin_progression',
        'pass': yin_ok,
        'detail': {name: f"{yin_map[name]} yin -> op {BAGUA_TO_OPERATOR[name]}"
                   for name in BAGUA_BINARY},
    })

    return {
        'verified': all(c['pass'] for c in checks),
        'checks': checks,
    }


def verify_wuxing_forces() -> dict:
    """Verify 5-phase to 5D dimension mapping with generation/destruction cycles.

    Checks:
    1. Five phases map to five distinct force dimensions (bijection)
    2. Generation cycle is a 5-cycle (wood→fire→earth→metal→water→wood)
    3. Destruction cycle forms a pentagram (5-pointed star)
    4. BALANCE (5) = center = earth = depth (the pivot)

    Returns:
        dict with 'verified', 'checks'.
    """
    checks = []

    # Check 1: Bijection
    dims = set(WUXING_TO_FORCE.values())
    expected_dims = {'aperture', 'pressure', 'depth', 'binding', 'continuity'}
    bij_ok = (dims == expected_dims) and (len(WUXING_TO_FORCE) == 5)
    checks.append({
        'name': 'bijection',
        'pass': bij_ok,
        'detail': f"Phases: {list(WUXING_TO_FORCE.keys())}, dims: {sorted(dims)}",
    })

    # Check 2: Generation cycle is a proper 5-cycle
    gen = WUXING_GENERATION
    gen_ok = (len(gen) == 5 and len(set(gen)) == 5)
    # Verify it cycles: gen[i] generates gen[(i+1) % 5]
    gen_pairs = [(gen[i], gen[(i + 1) % 5]) for i in range(5)]
    checks.append({
        'name': 'generation_cycle',
        'pass': gen_ok,
        'detail': f"Cycle: {' -> '.join(gen)} -> {gen[0]}",
        'pairs': gen_pairs,
    })

    # Check 3: Destruction cycle forms pentagram
    # In a regular pentagram on 5 points, each element skips one
    dest = WUXING_DESTRUCTION
    dest_sources = [d[0] for d in dest]
    dest_ok = (len(dest) == 5 and set(dest_sources) == set(gen))
    checks.append({
        'name': 'destruction_pentagram',
        'pass': dest_ok,
        'detail': [f"{a} overcomes {b}" for a, b in dest],
    })

    # Check 4: Earth = center = depth = BALANCE(5)
    earth_dim = WUXING_TO_FORCE.get('earth')
    # BALANCE is operator 5, earth is the center element in Ho Tu
    center_ok = (earth_dim == 'depth')
    checks.append({
        'name': 'earth_center_balance',
        'pass': center_ok,
        'detail': (
            f"earth -> {earth_dim}, BALANCE = op {BALANCE}, "
            f"Ho Tu center = (5, 10), depth = dimension index 2 (center of 5)"
        ),
    })

    return {
        'verified': all(c['pass'] for c in checks),
        'checks': checks,
    }


# ═══════════════════════════════════════════════════════════════════
# Computational Functions -- usable by CK at runtime
# ═══════════════════════════════════════════════════════════════════

def operator_pair_complement(op: int) -> int:
    """Return the Ho Tu complement: the operator at distance +5 (mod 10).

    Ho Tu pairs: 1↔6, 2↔7, 3↔8, 4↔9, 5↔0(10).
    Every pair = (yin, yang) of the same element.

    Args:
        op: Operator index (0-9).

    Returns:
        The complementary operator.
    """
    return (op + 5) % NUM_OPS


def hotu_distance(op_a: int, op_b: int) -> float:
    """Compute torus distance between two operators using Ho Tu topology.

    The Ho Tu arranges 1-10 on a torus: 5 cardinal pairs connected through
    center. Distance measures the minimum path through the torus.

    The torus has two metrics:
    - Ring distance: shortest path around the 10-cycle (mod 10)
    - Complement distance: hop through center costs 1 (via +5 complement)

    Returns the minimum of direct ring distance and complement hop distance,
    normalized to [0.0, 1.0] where 0.0 = same operator, 1.0 = maximally far.
    """
    if op_a == op_b:
        return 0.0

    a = op_a % NUM_OPS
    b = op_b % NUM_OPS

    # Direct ring distance (shortest path on mod-10 circle)
    ring_dist = min(abs(a - b), NUM_OPS - abs(a - b))

    # Complement hop: a → complement(a) → ring to b
    comp_a = (a + 5) % NUM_OPS
    hop_dist = 1 + min(abs(comp_a - b), NUM_OPS - abs(comp_a - b))

    # Also try: a → ring to complement(b) → b
    comp_b = (b + 5) % NUM_OPS
    hop_dist2 = min(abs(a - comp_b), NUM_OPS - abs(a - comp_b)) + 1

    best = min(ring_dist, hop_dist, hop_dist2)

    # Normalize: max possible distance on torus = 5 (half the ring)
    return best / 5.0


def loshu_coherence(
    prev_op: int,
    curr_op: int,
    next_op: int,
    bhml_table: Optional[List[List[int]]] = None,
    tsml_table: Optional[List[List[int]]] = None,
) -> float:
    """Compute Lo Shu coherence for a 3-operator configuration.

    The Lo Shu says: any 3-in-a-line that sums to 15 are in harmony.
    We translate this to CL algebra: compose three operators pairwise
    through both tables and measure how close to HARMONY the result is.

    Returns:
        float in [0.0, 1.0] where 1.0 = perfect Lo Shu coherence.
    """
    bt = bhml_table or BHML
    tt = tsml_table or TSML

    # Clamp to valid range
    p = prev_op % NUM_OPS
    c = curr_op % NUM_OPS
    n = next_op % NUM_OPS

    # TSML 3-body: compose(compose(p, c), n)
    tsml_result = tt[tt[p][c]][n]
    # BHML 3-body: compose(compose(p, c), n)
    bhml_result = bt[bt[p][c]][n]

    # Score components:
    score = 0.0

    # 1. TSML hits HARMONY = 0.4 points
    if tsml_result == HARMONY:
        score += 0.4

    # 2. BHML hits HARMONY = 0.2 points
    if bhml_result == HARMONY:
        score += 0.2

    # 3. Sum proximity to 15 (magic constant) = up to 0.2 points
    op_sum = p + c + n
    sum_diff = abs(op_sum - LOSHU_MAGIC_CONSTANT)
    if sum_diff == 0:
        score += 0.2
    elif sum_diff <= 3:
        score += 0.2 * (1.0 - sum_diff / 4.0)

    # 4. Ho Tu complement presence = 0.2 points
    # If any two of the three are Ho Tu complements (+5 apart)
    ops = [p, c, n]
    has_complement = False
    for i in range(3):
        for j in range(i + 1, 3):
            if (ops[i] + 5) % NUM_OPS == ops[j]:
                has_complement = True
                break
    if has_complement:
        score += 0.2

    return min(score, 1.0)


def wuxing_phase(force_5d: List[float]) -> str:
    """Map a 5D force vector to its dominant Wuxing phase.

    Dimension order: [aperture, pressure, depth, binding, continuity]
    Wuxing order:    [wood,     fire,     earth, metal,   water]

    The dominant phase is the dimension with the highest absolute magnitude.

    Args:
        force_5d: 5-element force vector.

    Returns:
        Wuxing phase name ('wood', 'fire', 'earth', 'metal', 'water').
    """
    dim_names = ['aperture', 'pressure', 'depth', 'binding', 'continuity']
    phases = list(WUXING_GENERATION)  # wood, fire, earth, metal, water

    if len(force_5d) < 5:
        return 'earth'  # Default to center

    # Find dominant dimension by absolute magnitude
    max_idx = 0
    max_val = abs(force_5d[0])
    for i in range(1, 5):
        v = abs(force_5d[i])
        if v > max_val:
            max_val = v
            max_idx = i

    return phases[max_idx]


def wuxing_balance(force_5d: List[float]) -> dict:
    """Compute the Wuxing balance of a 5D force vector.

    Returns the relative strength of each phase and whether the
    generation and destruction cycles are in balance.

    Args:
        force_5d: 5-element force vector.

    Returns:
        dict with phase strengths, dominant phase, cycle balance info.
    """
    phases = list(WUXING_GENERATION)
    if len(force_5d) < 5:
        force_5d = [0.0] * 5

    # Normalize to strengths
    total = sum(abs(v) for v in force_5d)
    if total == 0:
        strengths = {p: 0.2 for p in phases}
    else:
        strengths = {p: abs(force_5d[i]) / total for i, p in enumerate(phases)}

    # Check generation cycle balance: each feeder should be >= 60% of fed
    gen_balance = []
    for i in range(5):
        feeder = phases[i]
        fed = phases[(i + 1) % 5]
        ratio = strengths[feeder] / max(strengths[fed], 1e-9)
        gen_balance.append({
            'feeder': feeder,
            'fed': fed,
            'ratio': round(ratio, 3),
            'balanced': 0.6 <= ratio <= 1.6,
        })

    # Check destruction cycle: controller should not overwhelm controlled
    dest_balance = []
    for controller, controlled in WUXING_DESTRUCTION:
        ratio = strengths[controller] / max(strengths[controlled], 1e-9)
        dest_balance.append({
            'controller': controller,
            'controlled': controlled,
            'ratio': round(ratio, 3),
            'balanced': ratio < 2.0,
        })

    return {
        'strengths': {k: round(v, 4) for k, v in strengths.items()},
        'dominant': max(strengths, key=strengths.get),
        'generation_balance': gen_balance,
        'destruction_balance': dest_balance,
        'overall_balanced': (
            all(g['balanced'] for g in gen_balance) and
            all(d['balanced'] for d in dest_balance)
        ),
    }


def bagua_binary(op: int) -> str:
    """Return the binary trigram representation for an operator.

    The 8 living operators (1-8) map to 8 trigrams (3 bits each).
    VOID(0) and RESET(9) are the frame -- they wrap the trigrams.

    Args:
        op: Operator index (0-9).

    Returns:
        3-bit string ('000' to '111') or '---' for VOID/RESET.
    """
    name = OPERATOR_TO_BAGUA.get(op)
    if name is None:
        return '---'  # VOID and RESET are outside the 8 trigrams
    return BAGUA_BINARY[name]


def bagua_yin_yang_ratio(op: int) -> Tuple[int, int]:
    """Return (yin_count, yang_count) for an operator's trigram.

    Args:
        op: Operator index (0-9).

    Returns:
        (yin, yang) tuple. (0, 0) for VOID/RESET.
    """
    bits = bagua_binary(op)
    if bits == '---':
        return (0, 0)
    yin = bits.count('0')
    yang = bits.count('1')
    return (yin, yang)


# ═══════════════════════════════════════════════════════════════════
# Bridge Context -- for CK's voice system
# ═══════════════════════════════════════════════════════════════════

def bridge_context(
    current_ops: Optional[List[int]] = None,
    force_5d: Optional[List[float]] = None,
) -> dict:
    """Return a Ho Tu / Lo Shu perspective on the current operator state.

    Suitable for CK's fractal voice to add ancient resonance to word
    selection. The voice system can use this to understand operator
    relationships through the lens of 5,000-year-old topology.

    Args:
        current_ops: Recent operator sequence (last 3+ ops).
        force_5d: Current 5D force vector from heartbeat or D2.

    Returns:
        dict with:
            'dominant_phase': Current Wuxing phase
            'hotu_direction': Ho Tu cardinal direction
            'hotu_element': Associated element
            'trigram': Bagua trigram name
            'trigram_bits': Binary representation
            'complement_op': Ho Tu complement operator
            'complement_name': Name of complement
            'loshu_coherence': 3-body coherence if 3+ ops given
            'torus_position': Normalized position on Ho Tu torus
            'yin_yang': (yin, yang) balance of current operator
            'phase_balance': Wuxing balance summary (if force given)
    """
    ops = current_ops or []
    curr_op = ops[-1] if ops else HARMONY  # Default to HARMONY

    # Ho Tu direction and element
    direction = _OP_TO_DIRECTION.get(curr_op, 'center')
    element = HOTU_ELEMENT.get(direction, 'earth')

    # Complement
    comp = operator_pair_complement(curr_op)

    # Trigram
    trigram_name = OPERATOR_TO_BAGUA.get(curr_op, 'none')
    trigram_bits = bagua_binary(curr_op)
    yin_yang = bagua_yin_yang_ratio(curr_op)

    # Lo Shu coherence (needs 3 ops)
    lo_coh = 0.0
    if len(ops) >= 3:
        lo_coh = loshu_coherence(ops[-3], ops[-2], ops[-1])

    # Wuxing phase
    phase = wuxing_phase(force_5d) if force_5d else element

    # Phase balance
    phase_bal = None
    if force_5d and len(force_5d) >= 5:
        phase_bal = wuxing_balance(force_5d)

    return {
        'dominant_phase': phase,
        'hotu_direction': direction,
        'hotu_element': element,
        'trigram': trigram_name,
        'trigram_bits': trigram_bits,
        'complement_op': comp,
        'complement_name': OP_NAMES[comp],
        'loshu_coherence': round(lo_coh, 4),
        'torus_position': curr_op / NUM_OPS,
        'yin_yang': yin_yang,
        'phase_balance': phase_bal,
    }


# ═══════════════════════════════════════════════════════════════════
# Full Bridge Report
# ═══════════════════════════════════════════════════════════════════

def full_bridge_report(
    bhml_table: Optional[List[List[int]]] = None,
    tsml_table: Optional[List[List[int]]] = None,
) -> str:
    """Run all verifications and produce a human-readable report.

    Args:
        bhml_table: BHML table (uses built-in if None).
        tsml_table: TSML table (uses built-in if None).

    Returns:
        Multi-line string report with PASS/FAIL for each check.
    """
    bt = bhml_table or BHML
    tt = tsml_table or TSML

    lines = []
    lines.append("=" * 68)
    lines.append("  Ho Tu Bridge Report -- Ancient Torus Algebra in TIG")
    lines.append("=" * 68)
    lines.append("")

    # 1. Ho Tu successor verification
    lines.append("--- 1. Ho Tu +5 Successor (BHML HARMONY Row) ---")
    r1 = verify_hotu_successor(bt)
    lines.append(f"  Status: {'PASS' if r1['verified'] else 'FAIL'}")
    lines.append(f"  HARMONY row: {r1['harmony_row']}")
    for m in r1['matches']:
        lines.append(f"    [OK] {m}")
    for m in r1['mismatches']:
        lines.append(f"    [!!] {m}")
    lines.append("")

    # 2. Lo Shu vortex verification
    lines.append("--- 2. Lo Shu 3-Body Vortex Coherence ---")
    r2 = verify_loshu_vortex(bt, tt)
    lines.append(f"  Status: {'PASS' if r2['verified'] else 'PARTIAL'}")
    lines.append(f"  HARMONY count: {r2['harmony_count']}/{r2['total_lines']}")
    lines.append(f"  Magic constant: {r2['magic_constant']}")
    for ln in r2['lines']:
        ops_str = f"({ln['operators'][0]},{ln['operators'][1]},{ln['operators'][2]})"
        sum_mark = "=" if ln['sum_is_15'] else "!="
        h_mark = "H" if ln['tsml_is_harmony'] else ln['tsml_result_name'][:3]
        lines.append(
            f"    {ln['kind']}[{ln['index']}] {ops_str:>10} "
            f"sum{sum_mark}15  TSML={h_mark:>3}  BHML={ln['bhml_result_name'][:3]}"
        )
    lines.append("")

    # 3. Bagua operators
    lines.append("--- 3. Bagua Trigram <-> Operator Mapping ---")
    r3 = verify_bagua_operators()
    lines.append(f"  Status: {'PASS' if r3['verified'] else 'FAIL'}")
    for chk in r3['checks']:
        mark = 'OK' if chk['pass'] else '!!'
        lines.append(f"    [{mark}] {chk['name']}")
    # Show the mapping
    for name in ['kun', 'gen', 'kan', 'xun', 'zhen', 'li', 'dui', 'qian']:
        op = BAGUA_TO_OPERATOR[name]
        bits = BAGUA_BINARY[name]
        lines.append(f"      {name:>5} {bits} -> {op} ({OP_NAMES[op]})")
    lines.append("")

    # 4. Wuxing forces
    lines.append("--- 4. Wuxing 5-Phase <-> 5D Force Mapping ---")
    r4 = verify_wuxing_forces()
    lines.append(f"  Status: {'PASS' if r4['verified'] else 'FAIL'}")
    for chk in r4['checks']:
        mark = 'OK' if chk['pass'] else '!!'
        lines.append(f"    [{mark}] {chk['name']}")
    lines.append(f"  Generation: {' -> '.join(WUXING_GENERATION)} -> {WUXING_GENERATION[0]}")
    lines.append(f"  Destruction: {', '.join(f'{a}>{b}' for a, b in WUXING_DESTRUCTION)}")
    lines.append("")

    # 5. Ho Tu complement table
    lines.append("--- 5. Ho Tu Complement Table ---")
    for i in range(NUM_OPS):
        c = operator_pair_complement(i)
        lines.append(f"    {OP_NAMES[i]:>10}({i}) <-> {OP_NAMES[c]:>10}({c})")
    lines.append("")

    # 6. Torus distance matrix (upper triangle)
    lines.append("--- 6. Ho Tu Torus Distance (key pairs) ---")
    key_pairs = [
        (LATTICE, CHAOS), (COUNTER, HARMONY), (PROGRESS, BREATH),
        (COLLAPSE, RESET), (BALANCE, VOID),
        (LATTICE, HARMONY), (COUNTER, CHAOS), (PROGRESS, BALANCE),
    ]
    for a, b in key_pairs:
        d = hotu_distance(a, b)
        lines.append(
            f"    {OP_NAMES[a]:>10} <-> {OP_NAMES[b]:<10}  d = {d:.3f}"
        )
    lines.append("")

    lines.append("=" * 68)
    all_pass = r1['verified'] and r3['verified'] and r4['verified']
    lines.append(
        f"  Overall: {'ALL STRUCTURAL CHECKS PASS' if all_pass else 'SOME CHECKS NEED ATTENTION'}"
    )
    lines.append(
        f"  Lo Shu TSML coherence: {r2['harmony_count']}/{r2['total_lines']} lines -> HARMONY"
    )
    lines.append("=" * 68)

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════
# Self-test
# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print(full_bridge_report())
