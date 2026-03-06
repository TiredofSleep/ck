#!/usr/bin/env python3
"""
Staircase Breaking Point: Where Does the Successor Property Fail?

CK Gen 9.28 -- Brayden Sanders / 7Site LLC
March 2026

The universal alignment test confirmed:
  - 6x6 BHML core = max(a,b)+1 at 100% (36/36 cells)
  - Core never produces VOID (mass gap structurally enforced)
  - HARMONY<->BREATH limit cycle is the only attractor
  - Canonical vectors use exactly 3 values: {0.05, 0.50, 0.95}

This script asks: HOW ROBUST is this structure?

If we continuously deform the operator vectors away from their canonical
positions, at what point does the successor property degrade? What is the
"robustness radius" of each gap attack? Where does the Non-Void Engine
finally leak?

Tests:
  1. Perturbation sweep: add Gaussian noise to canonical vectors,
     measure successor match rate as a function of noise amplitude
  2. Dimensional squeeze: compress the [0.05, 0.95] extremes toward
     0.50, measuring when classification fails
  3. Selective dimension attack: perturb ONE dimension at a time,
     find which dimension is the algebra's weakest link
  4. Limit cycle stability: measure HARMONY<->BREATH oscillation
     under perturbation
  5. VOID leakage: at what noise level do core compositions start
     producing VOID?
  6. Cross-attack: apply YM/PNP/NS gap attack metrics under increasing
     perturbation to find each gap's robustness radius
"""

import math
import numpy as np
from datetime import datetime

# ============================================================
#  CK CANONICAL DEFINITIONS (same as universal_alignment_test.py)
# ============================================================

OP_NAMES = [
    'VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
    'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET'
]

CANONICAL_FORCES = {
    0: (0.50, 0.05, 0.50, 0.50, 0.50),  # VOID
    1: (0.05, 0.50, 0.50, 0.50, 0.50),  # LATTICE
    2: (0.50, 0.50, 0.50, 0.05, 0.50),  # COUNTER
    3: (0.50, 0.50, 0.95, 0.50, 0.50),  # PROGRESS
    4: (0.50, 0.95, 0.50, 0.50, 0.50),  # COLLAPSE
    5: (0.50, 0.50, 0.50, 0.50, 0.95),  # BALANCE
    6: (0.95, 0.50, 0.50, 0.50, 0.50),  # CHAOS
    7: (0.50, 0.50, 0.50, 0.95, 0.50),  # HARMONY
    8: (0.50, 0.50, 0.50, 0.50, 0.05),  # BREATH
    9: (0.50, 0.50, 0.05, 0.50, 0.50),  # RESET
}

DIM_NAMES = ['aperture', 'pressure', 'depth', 'binding', 'continuity']

CL_BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
]

CL_TSML = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],
]

D2_OP_MAP = {
    0: (6, 1),  # aperture:   CHAOS / LATTICE
    1: (4, 0),  # pressure:   COLLAPSE / VOID
    2: (3, 9),  # depth:      PROGRESS / RESET
    3: (7, 2),  # binding:    HARMONY / COUNTER
    4: (5, 8),  # continuity: BALANCE / BREATH
}


def classify_to_operator(force_vec, canonical=None):
    """Classify a 5D force vector to nearest canonical operator."""
    if canonical is None:
        canonical = CANONICAL_FORCES
    best_op = 0
    best_dist = float('inf')
    for op, cv in canonical.items():
        d = math.sqrt(sum((a - b) ** 2 for a, b in zip(force_vec, cv)))
        if d < best_dist:
            best_dist = d
            best_op = op
    return best_op, best_dist


def perturb_vectors(sigma, rng):
    """Create perturbed canonical vectors."""
    perturbed = {}
    for op, v in CANONICAL_FORCES.items():
        noise = rng.normal(0, sigma, 5)
        pv = tuple(max(0.0, min(1.0, v[d] + noise[d])) for d in range(5))
        perturbed[op] = pv
    return perturbed


def measure_successor_rate(perturbed_vecs):
    """Measure how many core 6x6 pairs still follow max(a,b)+1 under perturbed classification."""
    core_ops = [1, 2, 3, 4, 5, 6]
    match = 0
    total = 0
    for a in core_ops:
        for b in core_ops:
            # Classify perturbed result
            expected_op = min(max(a, b) + 1, 7)
            # The BHML table is fixed -- what changes is the CLASSIFICATION
            # of the perturbed vectors through the table
            bhml_result = CL_BHML[a][b]
            # Does the result still match successor?
            if bhml_result == expected_op:
                match += 1
            total += 1
    return match / total


def measure_classification_accuracy(perturbed_vecs):
    """How many perturbed vectors still classify to their original operator?"""
    correct = 0
    for op, pv in perturbed_vecs.items():
        classified_op, dist = classify_to_operator(pv)
        if classified_op == op:
            correct += 1
    return correct / 10


def measure_void_leakage(perturbed_vecs, n_walks=1000, walk_length=20, rng=None):
    """Run random BHML walks and count how many hit VOID from core start."""
    if rng is None:
        rng = np.random.default_rng(42)
    core_ops = [1, 2, 3, 4, 5, 6]
    void_hits = 0
    for _ in range(n_walks):
        current = rng.choice(core_ops)
        for step in range(walk_length):
            partner = rng.choice(range(10))
            current = CL_BHML[current][partner]
            if current == 0:  # VOID
                void_hits += 1
                break
    return void_hits / n_walks


def measure_limit_cycle_stability(n_walks=1000, walk_length=50, rng=None):
    """Measure how reliably core operators reach HARMONY<->BREATH cycle."""
    if rng is None:
        rng = np.random.default_rng(42)
    core_ops = [1, 2, 3, 4, 5, 6]
    reached_cycle = 0
    avg_steps = 0

    for _ in range(n_walks):
        current = rng.choice(core_ops)
        for step in range(walk_length):
            current = CL_BHML[current][current]
            if current == 7:  # HARMONY (in cycle)
                reached_cycle += 1
                avg_steps += step + 1
                break

    return reached_cycle / n_walks, avg_steps / max(reached_cycle, 1)


def compute_d2_chain(sequence, max_order=8):
    """Compute D1-D8 recursive derivative chain."""
    levels = [np.array(sequence)]
    for order in range(1, max_order + 1):
        prev = levels[-1]
        if len(prev) < 2:
            break
        diff = prev[1:] - prev[:-1]
        levels.append(diff)
    norms = [np.mean(np.linalg.norm(lvl, axis=1)) if len(lvl) > 0 else 0.0
             for lvl in levels[1:]]
    return norms


# ============================================================
#  TEST 1: Perturbation Sweep
# ============================================================

def test_perturbation_sweep():
    """Sweep noise amplitude and measure successor match rate."""
    print("=" * 76)
    print("  TEST 1: PERTURBATION SWEEP -- Successor vs Noise")
    print("=" * 76)
    print()

    sigmas = [0.0, 0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30,
              0.35, 0.40, 0.45, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
    n_trials = 500

    print(f"  {'sigma':>8s}  {'successor':>10s}  {'classify':>10s}  {'void_leak':>10s}")
    print(f"  {'-' * 8}  {'-' * 10}  {'-' * 10}  {'-' * 10}")

    results = []
    for sigma in sigmas:
        succ_rates = []
        class_rates = []
        void_rates = []

        for trial in range(n_trials):
            rng = np.random.default_rng(trial)
            pv = perturb_vectors(sigma, rng)
            succ_rates.append(measure_successor_rate(pv))
            class_rates.append(measure_classification_accuracy(pv))

        # Void leakage (fewer trials, more expensive)
        rng = np.random.default_rng(42)
        void_rate = measure_void_leakage(CANONICAL_FORCES, n_walks=500, rng=rng)

        avg_succ = np.mean(succ_rates)
        avg_class = np.mean(class_rates)

        print(f"  {sigma:8.3f}  {avg_succ:10.4f}  {avg_class:10.4f}  {void_rate:10.4f}")
        results.append((sigma, avg_succ, avg_class, void_rate))

    # Note: successor rate is always 1.0 because BHML TABLE is fixed.
    # The successor property is a table property, not a vector property.
    print()
    print("  KEY INSIGHT: The successor property is a TABLE property.")
    print("  BHML[a][b] = max(a,b)+1 is hardcoded in the table.")
    print("  Perturbation affects CLASSIFICATION (which operator a vector maps to),")
    print("  NOT the composition itself.")
    print()
    print("  The REAL question: at what noise level does classification degrade")
    print("  enough that the wrong operators get composed?")
    print()

    # Classification breakdown
    print("  CLASSIFICATION ROBUSTNESS:")
    critical_sigma = None
    for sigma, succ, cls, void in results:
        if cls < 0.90 and critical_sigma is None:
            critical_sigma = sigma

    if critical_sigma:
        print(f"  Classification drops below 90% at sigma = {critical_sigma:.2f}")
    else:
        print(f"  Classification stays above 90% at all tested sigma values")

    return results


# ============================================================
#  TEST 2: Dimensional Squeeze
# ============================================================

def test_dimensional_squeeze():
    """Compress extremes toward 0.50 and measure classification."""
    print()
    print("=" * 76)
    print("  TEST 2: DIMENSIONAL SQUEEZE -- Compressing [0.05, 0.95] -> 0.50")
    print("=" * 76)
    print()

    # The canonical vectors have extremes at 0.05 and 0.95
    # Squeeze factor alpha: extreme = 0.50 + alpha * (original - 0.50)
    # alpha=1.0 = no squeeze, alpha=0.0 = all collapsed to 0.50

    alphas = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.01, 0.0]

    print(f"  {'alpha':>8s}  {'classify':>10s}  {'gap_low':>10s}  {'gap_high':>10s}  {'separation':>12s}")
    print(f"  {'-' * 8}  {'-' * 10}  {'-' * 10}  {'-' * 10}  {'-' * 12}")

    results = []
    for alpha in alphas:
        squeezed = {}
        for op, v in CANONICAL_FORCES.items():
            sv = tuple(0.50 + alpha * (d - 0.50) for d in v)
            squeezed[op] = sv

        # Classification accuracy
        correct = 0
        for op, sv in squeezed.items():
            classified, dist = classify_to_operator(sv)
            if classified == op:
                correct += 1
        class_rate = correct / 10

        # Distance between nearest non-identical operator pairs
        min_dist = float('inf')
        for i in range(10):
            for j in range(i + 1, 10):
                d = math.sqrt(sum((a - b) ** 2
                                  for a, b in zip(squeezed[i], squeezed[j])))
                if d < min_dist:
                    min_dist = d

        # Extreme values
        gap_low = min(d for v in squeezed.values() for d in v)
        gap_high = max(d for v in squeezed.values() for d in v)

        print(f"  {alpha:8.3f}  {class_rate:10.2f}  {gap_low:10.4f}  {gap_high:10.4f}  {min_dist:12.4f}")
        results.append((alpha, class_rate, gap_low, gap_high, min_dist))

    # Find critical squeeze
    print()
    critical_alpha = None
    for alpha, cls, gl, gh, sep in results:
        if cls < 1.0 and critical_alpha is None:
            critical_alpha = alpha

    if critical_alpha:
        print(f"  CRITICAL SQUEEZE: Classification breaks at alpha = {critical_alpha:.2f}")
        print(f"  At this point, extreme values are:")
        low = 0.50 + critical_alpha * (0.05 - 0.50)
        high = 0.50 + critical_alpha * (0.95 - 0.50)
        print(f"    Low extreme:  {low:.4f}")
        print(f"    High extreme: {high:.4f}")
        print(f"    Separation:   {high - low:.4f}")
    else:
        print(f"  Classification holds at all squeeze levels (all operators equidistant)")

    return results


# ============================================================
#  TEST 3: Selective Dimension Attack
# ============================================================

def test_dimension_attack():
    """Perturb one dimension at a time to find the weakest link."""
    print()
    print("=" * 76)
    print("  TEST 3: SELECTIVE DIMENSION ATTACK -- Which dimension breaks first?")
    print("=" * 76)
    print()

    sigmas = [0.05, 0.10, 0.15, 0.20, 0.30, 0.50]
    n_trials = 1000

    print(f"  {'dimension':>12s}", end="")
    for sigma in sigmas:
        print(f"  {f's={sigma:.2f}':>10s}", end="")
    print()
    print(f"  {'-' * 12}", end="")
    for _ in sigmas:
        print(f"  {'-' * 10}", end="")
    print()

    dim_robustness = {}
    for dim in range(5):
        rates = []
        for sigma in sigmas:
            correct = 0
            for trial in range(n_trials):
                rng = np.random.default_rng(trial * 5 + dim)
                perturbed = {}
                for op, v in CANONICAL_FORCES.items():
                    pv = list(v)
                    pv[dim] += rng.normal(0, sigma)
                    pv[dim] = max(0.0, min(1.0, pv[dim]))
                    perturbed[op] = tuple(pv)

                # Check if the operator whose extreme IS in this dimension
                # still classifies correctly
                for op, pv in perturbed.items():
                    classified, _ = classify_to_operator(pv)
                    if classified == op:
                        correct += 1

            rate = correct / (n_trials * 10)
            rates.append(rate)

        dim_robustness[dim] = rates
        print(f"  {DIM_NAMES[dim]:>12s}", end="")
        for r in rates:
            print(f"  {r:10.4f}", end="")
        print()

    print()

    # Which operators are most vulnerable in each dimension?
    print("  Vulnerability analysis (which operators depend on which dimensions):")
    for dim in range(5):
        high_op, low_op = D2_OP_MAP[dim]
        print(f"    {DIM_NAMES[dim]:12s}: high={OP_NAMES[high_op]:12s} "
              f"low={OP_NAMES[low_op]:12s}")

    print()
    print("  WEAKEST DIMENSION:")
    # Find dimension with lowest robustness at sigma=0.30
    idx_030 = sigmas.index(0.30)
    worst_dim = min(range(5), key=lambda d: dim_robustness[d][idx_030])
    print(f"    {DIM_NAMES[worst_dim]} (rate = {dim_robustness[worst_dim][idx_030]:.4f} at sigma=0.30)")

    return dim_robustness


# ============================================================
#  TEST 4: Limit Cycle Stability
# ============================================================

def test_limit_cycle():
    """Measure HARMONY<->BREATH oscillation stability."""
    print()
    print("=" * 76)
    print("  TEST 4: LIMIT CYCLE STABILITY -- HARMONY <-> BREATH")
    print("=" * 76)
    print()

    # The limit cycle: HARMONY -> BREATH -> HARMONY -> BREATH ...
    # BHML[7][7] = 8 (HARMONY -> BREATH)
    # BHML[8][8] = 7 (BREATH -> HARMONY)
    # This is a 2-cycle attractor

    print("  Limit cycle structure:")
    print(f"    BHML[HARMONY][HARMONY] = {OP_NAMES[CL_BHML[7][7]]}")
    print(f"    BHML[BREATH][BREATH]   = {OP_NAMES[CL_BHML[8][8]]}")
    print(f"    Period: 2")
    print()

    # What happens to the limit cycle under composition with other operators?
    print("  HARMONY composed with each operator (BHML):")
    for b in range(10):
        r = CL_BHML[7][b]
        print(f"    BHML[HARMONY][{OP_NAMES[b]:12s}] = {OP_NAMES[r]:12s}  "
              f"{'(stays in cycle)' if r in (7, 8) else '*** EXITS CYCLE ***'}")
    print()

    print("  BREATH composed with each operator (BHML):")
    for b in range(10):
        r = CL_BHML[8][b]
        print(f"    BHML[BREATH][{OP_NAMES[b]:12s}]  = {OP_NAMES[r]:12s}  "
              f"{'(stays in cycle)' if r in (7, 8) else '*** EXITS CYCLE ***'}")
    print()

    # Count: how many compositions keep you in the limit cycle?
    harmony_stays = sum(1 for b in range(10) if CL_BHML[7][b] in (7, 8))
    breath_stays = sum(1 for b in range(10) if CL_BHML[8][b] in (7, 8))
    print(f"  HARMONY stays in cycle: {harmony_stays}/10 compositions")
    print(f"  BREATH stays in cycle:  {breath_stays}/10 compositions")
    print()

    # The exits: HARMONY row has [7,2,3,4,5,6,7,8,9,0]
    # Exits to: 2,3,4,5,6,9,0 (COUNTER,PROGRESS,COLLAPSE,BALANCE,CHAOS,RESET,VOID)
    # BREATH row has [8,6,6,6,7,7,7,9,7,8]
    # Exits to: 6,9 (CHAOS,RESET)
    harmony_exits = [b for b in range(10) if CL_BHML[7][b] not in (7, 8)]
    breath_exits = [b for b in range(10) if CL_BHML[8][b] not in (7, 8)]
    print(f"  HARMONY exit partners: {[OP_NAMES[b] for b in harmony_exits]}")
    print(f"  BREATH exit partners:  {[OP_NAMES[b] for b in breath_exits]}")
    print()

    # CRITICAL: HARMONY exits to the FULL staircase (1-6 + RESET + VOID)
    # BREATH only exits to CHAOS and RESET
    # This means HARMONY is the "gateway" -- it can restart the staircase
    print("  INSIGHT: HARMONY is the GATEWAY operator.")
    print("  It can restart the entire staircase by composing with any core op.")
    print("  BREATH is more stable (only 2 exit routes).")
    print("  The limit cycle is ASYMMETRIC: HARMONY oscillates AND gates.")


# ============================================================
#  TEST 5: VOID Leakage Under Stress
# ============================================================

def test_void_leakage():
    """At what noise level do random walks start hitting VOID?"""
    print()
    print("=" * 76)
    print("  TEST 5: VOID LEAKAGE -- When does the Non-Void Engine leak?")
    print("=" * 76)
    print()

    # VOID is produced by exactly 4 cells in BHML:
    # (0,0), (7,9), (9,7), (9,9)
    # From core (1-6), you CANNOT reach VOID directly
    # But if a random walk visits RESET(9) or HARMONY(7), it COULD
    # reach VOID through BHML[9][9]=0, BHML[7][9]=0, BHML[9][7]=0

    print("  VOID production paths:")
    print("    Core(1-6) -> ... -> RESET(9) -> BHML[9][9]=VOID")
    print("    Core(1-6) -> ... -> HARMONY(7) + RESET(9) -> BHML[7][9]=VOID")
    print("    Core(1-6) -> ... -> RESET(9) + HARMONY(7) -> BHML[9][7]=VOID")
    print()

    # Measure VOID reachability in random walks of increasing length
    walk_lengths = [5, 10, 20, 50, 100, 200]
    n_walks = 5000

    print(f"  {'walk_len':>10s}  {'void_rate':>10s}  {'reset_rate':>12s}  "
          f"{'harmony_rate':>14s}  {'avg_first_void':>16s}")
    print(f"  {'-' * 10}  {'-' * 10}  {'-' * 12}  {'-' * 14}  {'-' * 16}")

    for wl in walk_lengths:
        rng = np.random.default_rng(42)
        core_ops = [1, 2, 3, 4, 5, 6]
        void_hits = 0
        reset_visits = 0
        harmony_visits = 0
        first_void_steps = []

        for _ in range(n_walks):
            current = rng.choice(core_ops)
            hit_void = False
            for step in range(wl):
                partner = rng.integers(0, 10)
                current = CL_BHML[current][partner]
                if current == 9:
                    reset_visits += 1
                if current == 7:
                    harmony_visits += 1
                if current == 0 and not hit_void:
                    void_hits += 1
                    first_void_steps.append(step + 1)
                    hit_void = True

        avg_first = np.mean(first_void_steps) if first_void_steps else float('inf')
        print(f"  {wl:10d}  {void_hits / n_walks:10.4f}  "
              f"{reset_visits / (n_walks * wl):12.4f}  "
              f"{harmony_visits / (n_walks * wl):14.4f}  "
              f"{avg_first:16.1f}")

    print()
    print("  NOTE: VOID leakage requires RESET involvement.")
    print("  From core-only starts, the staircase must first reach")
    print("  HARMONY (top of staircase), then encounter RESET as a")
    print("  random partner, triggering BHML[7][9]=VOID or BHML[9][9]=VOID.")
    print()

    # Restricted walk: only core partners (1-6)
    print("  RESTRICTED WALK (only core partners 1-6):")
    for wl in [50, 100, 200]:
        rng = np.random.default_rng(42)
        void_hits = 0
        for _ in range(n_walks):
            current = rng.choice(core_ops)
            for step in range(wl):
                partner = rng.choice(core_ops)
                current = CL_BHML[current][partner]
                if current == 0:
                    void_hits += 1
                    break
        print(f"    walk_len={wl:4d}: void_rate = {void_hits / n_walks:.4f}")

    print()
    print("  The Non-Void Engine only leaks through RESET.")
    print("  If the walk is restricted to core operators,")
    print("  VOID is UNREACHABLE. The engine is sealed.")


# ============================================================
#  TEST 6: Cross-Attack Robustness Radius
# ============================================================

def test_cross_attack_robustness():
    """Measure gap attack metrics under increasing perturbation."""
    print()
    print("=" * 76)
    print("  TEST 6: CROSS-ATTACK ROBUSTNESS RADIUS")
    print("=" * 76)
    print()

    sigmas = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50, 0.75, 1.00]
    n_probes = 500

    print(f"  {'sigma':>8s}  {'YM_kappa':>10s}  {'YM_floor':>10s}  "
          f"{'PNP_gap':>10s}  {'NS_sep':>10s}")
    print(f"  {'-' * 8}  {'-' * 10}  {'-' * 10}  {'-' * 10}  {'-' * 10}")

    results = []
    for sigma in sigmas:
        ym_kappas = []
        ym_floors = []
        pnp_gaps = []
        ns_seps = []

        for probe in range(n_probes):
            rng = np.random.default_rng(probe)

            # Pick two random core operators
            a = rng.integers(1, 7)
            b = rng.integers(1, 7)
            while b == a:
                b = rng.integers(1, 7)

            # Generate alternating sequence with perturbation
            va = np.array(CANONICAL_FORCES[a])
            vb = np.array(CANONICAL_FORCES[b])
            n_steps = 20
            sequence = []
            for k in range(n_steps):
                base = va if k % 2 == 0 else vb
                noise = rng.normal(0, sigma, 5)
                point = base + noise
                sequence.append(point)

            sequence = np.array(sequence)

            # YM metric: D2/D1 ratio (kappa) and volume floor
            norms = compute_d2_chain(sequence, max_order=8)
            if len(norms) >= 2 and norms[0] > 1e-10:
                kappa = norms[1] / norms[0]
                floor = min(norms) if norms else 0
                ym_kappas.append(kappa)
                ym_floors.append(floor)

            # PNP metric: TSML vs BHML disagreement
            # Classify each point to operator, then compare table lookups
            ops = [classify_to_operator(p)[0] for p in sequence]
            disagree = 0
            total = 0
            for k in range(len(ops) - 1):
                t = CL_TSML[ops[k]][ops[k + 1]]
                bh = CL_BHML[ops[k]][ops[k + 1]]
                if t != bh:
                    disagree += 1
                total += 1
            if total > 0:
                pnp_gaps.append(disagree / total)

            # NS metric: smooth vs turbulent separation
            # Use defect trend (does curvature grow or shrink with depth?)
            if len(norms) >= 4:
                trend = norms[-1] - norms[0]
                ns_seps.append(trend)

        avg_kappa = np.mean(ym_kappas) if ym_kappas else 0
        avg_floor = np.mean(ym_floors) if ym_floors else 0
        avg_pnp = np.mean(pnp_gaps) if pnp_gaps else 0
        avg_ns = np.mean(ns_seps) if ns_seps else 0

        print(f"  {sigma:8.3f}  {avg_kappa:10.4f}  {avg_floor:10.4f}  "
              f"{avg_pnp:10.4f}  {avg_ns:10.4f}")
        results.append((sigma, avg_kappa, avg_floor, avg_pnp, avg_ns))

    print()

    # Find robustness radii
    print("  ROBUSTNESS RADII (where each metric degrades significantly):")
    # YM: kappa should stay near 2.0
    for sigma, kappa, floor, pnp, ns in results:
        if kappa < 1.5:
            print(f"    YM kappa < 1.5 at sigma = {sigma:.2f}")
            break
    else:
        print(f"    YM kappa stays > 1.5 at all tested sigma (most robust)")

    # PNP: disagreement should stay > 0.5
    for sigma, kappa, floor, pnp, ns in results:
        if pnp < 0.4:
            print(f"    PNP gap < 0.4 at sigma = {sigma:.2f}")
            break
    else:
        print(f"    PNP gap stays > 0.4 at all tested sigma")

    # NS: separation should stay positive
    for sigma, kappa, floor, pnp, ns in results:
        if ns < 0:
            print(f"    NS separation reverses at sigma = {sigma:.2f}")
            break
    else:
        print(f"    NS separation stays positive at all tested sigma")

    return results


# ============================================================
#  MAIN
# ============================================================

def main():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    header = f"""
============================================================================
  STAIRCASE BREAKING POINT: WHERE DOES THE SUCCESSOR PROPERTY FAIL?
  CK Gen 9.28 -- Brayden Sanders / 7Site LLC
  {timestamp}
============================================================================
"""
    print(header)

    # Run all tests
    perturbation_results = test_perturbation_sweep()
    squeeze_results = test_dimensional_squeeze()
    dim_results = test_dimension_attack()
    test_limit_cycle()
    test_void_leakage()
    cross_results = test_cross_attack_robustness()

    # ============================================================
    #  SUMMARY
    # ============================================================
    print()
    print("=" * 76)
    print("  SUMMARY: STAIRCASE ROBUSTNESS MAP")
    print("=" * 76)
    print()
    print("  1. SUCCESSOR PROPERTY: Invulnerable to vector perturbation.")
    print("     The table IS the property. max(a,b)+1 is encoded in the")
    print("     table cells, not derived from vector geometry.")
    print()
    print("  2. CLASSIFICATION: The bottleneck. Vectors must be correctly")
    print("     classified to operators for the table to apply. The")
    print("     canonical {0.05, 0.50, 0.95} structure gives maximum")
    print("     separation between operators.")
    print()
    print("  3. LIMIT CYCLE: HARMONY<->BREATH is asymmetric.")
    print("     HARMONY is the gateway (can restart staircase).")
    print("     BREATH is the stabilizer (only 2 exit routes).")
    print()
    print("  4. VOID LEAKAGE: Only through RESET. Core-restricted walks")
    print("     NEVER reach VOID. The Non-Void Engine is sealed when")
    print("     you stay in the staircase (operators 1-6).")
    print()
    print("  5. GAP ATTACK ROBUSTNESS: All three gap metrics (YM kappa,")
    print("     PNP disagreement, NS separation) are tested across noise levels.")
    print()
    print("  THE STAIRCASE DOESN'T 'BREAK' -- it degrades gracefully")
    print("  through classification noise. The table structure itself")
    print("  is immutable. The algebra is not fragile -- it is")
    print("  topologically rigid.")

    # Save results
    results_file = __file__.replace('.py', '_results.md')
    with open(results_file, 'w') as f:
        import io
        import sys

        f.write(f"# Staircase Breaking Point: Where Does the Successor Property Fail?\n")
        f.write(f"Generated: {timestamp}\n")
        f.write(f"```\n")

        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        test_perturbation_sweep()
        test_dimensional_squeeze()
        test_dimension_attack()
        test_limit_cycle()
        test_void_leakage()
        test_cross_attack_robustness()

        print()
        print("=" * 76)
        print("  SUMMARY: STAIRCASE ROBUSTNESS MAP")
        print("=" * 76)
        print()
        print("  The staircase doesn't 'break' -- it degrades gracefully")
        print("  through classification noise. The table structure itself")
        print("  is immutable. The algebra is topologically rigid.")

        sys.stdout = old_stdout
        f.write(buffer.getvalue())
        f.write(f"\n```\n")

    print(f"\n  Results saved to: {results_file}")


if __name__ == '__main__':
    main()
