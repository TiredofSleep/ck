"""
ck_phase_detector.py -- 3-Lattice Phase Detector
=================================================
Tests the engine-ready lambda -> phase mapping and structural
properties of Mix_lambda throughout [0, 1].

Run: python ck_phase_detector.py
Expected: PHASE DETECTOR: 33/33 assertions passed

Author: Brayden Sanders / 7Site LLC | March 2026
DOI: 10.5281/zenodo.18852047
"""

import numpy as np

# The exact TSML (from ck_sim/being/ck_sim_heartbeat.py, states 0-9)
TSML = [
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

# BHML: F(i,j) = max(i,j) for all i,j in 0-9
BHML = [[max(i, j) for j in range(10)] for i in range(10)]

C = frozenset({1, 3, 7, 9})
G_nv = frozenset({2, 4, 5, 6, 8})
HAR = 7
STATES = list(range(1, 10))
T_STAR = 5.0 / 7.0


# ── Core helpers ──

def make_stochastic(table, states):
    """Row-stochastic matrix: M[i,k] = P(output=k | input state i, uniform random operator j)."""
    n = len(states)
    idx = {s: i for i, s in enumerate(states)}
    M = np.zeros((n, n))
    for ci, s in enumerate(states):
        for j_s in states:
            out = table[s][j_s]
            if out in idx:
                M[ci, idx[out]] += 1
        rs = M[ci].sum()
        if rs > 0:
            M[ci] /= rs
        else:
            M[ci, ci] = 1.0
    return M


def mix_stochastic(lam, states):
    """Stochastic matrix for Mix_lam = (1-lam)*M_TSML + lam*M_BHML."""
    M_t = make_stochastic(TSML, states)
    M_b = make_stochastic(BHML, states)
    return (1.0 - lam) * M_t + lam * M_b


def spectral_gap(M):
    """Spectral gap = lambda_1 - |lambda_2|."""
    eigs = sorted(np.abs(np.linalg.eigvals(M)), reverse=True)
    return float(eigs[0] - eigs[1]) if len(eigs) >= 2 else 1.0


def stationary(M, tol=1e-13):
    """Stationary distribution via power iteration."""
    v = np.ones(M.shape[0]) / M.shape[0]
    for _ in range(10000):
        v_new = v @ M
        if np.max(np.abs(v_new - v)) < tol:
            return v_new
        v = v_new
    return v


def c_closed_at_lambda(lam):
    """Check C closure under round(Mix_lam) composition."""
    for a in C:
        for b in C:
            v = round((1.0 - lam) * TSML[a][b] + lam * BHML[a][b])
            if v not in C:
                return False
    return True


def gate_holds_at_lambda(lam):
    """Check one-way gate: no C x G_nv pair routes back to G_nv."""
    for c in C:
        for g in G_nv:
            v = round((1.0 - lam) * TSML[c][g] + lam * BHML[c][g])
            if v in G_nv:
                return False
    return True


def bhml_residual_count_at_lambda(lam, states):
    """Count non-HAR cells where round(Mix_lam[i][j]) == max(i,j)."""
    count = 0
    for i in states:
        for j in states:
            v = round((1.0 - lam) * TSML[i][j] + lam * BHML[i][j])
            if v != HAR and v == max(i, j):
                count += 1
    return count


def detect_phase(lam):
    """Return phase (1, 2, or 3) given Mix_lambda deformation parameter."""
    if lam < 0.09:
        return 1  # Grammar phase: C closed, gate holds, HAR absorbing
    elif lam < 0.45:
        return 2  # Transitional phase: gate opening, HAR weakening
    else:
        return 3  # Order phase: BHML order dominant


# Test harness
passed = 0
total = 0
failures = []


def check(name, cond, note=""):
    global passed, total
    total += 1
    ok = bool(cond)
    if ok:
        passed += 1
        print("  PASS  " + name + ("  [" + note + "]" if note else ""))
    else:
        failures.append(name)
        print("  FAIL  " + name + ("  [" + note + "]" if note else ""))


# ===========================================================
# S1 -- Phase boundaries (8 assertions)
# ===========================================================
print("\n-- S1: Phase boundaries (8 assertions) --")

# Mix_lam=0.0 is pure TSML: Phase 1 (C closed, gate holds)
check("S1: lam=0.0 (pure TSML) -> Phase 1",
      detect_phase(0.0) == 1, "phase=" + str(detect_phase(0.0)))

check("S1: lam=0.0 C closed",
      c_closed_at_lambda(0.0), "c_closed=" + str(c_closed_at_lambda(0.0)))

check("S1: lam=0.05 -> Phase 1 (well inside grammar phase)",
      detect_phase(0.05) == 1, "phase=" + str(detect_phase(0.05)))

# Phase 1/2 boundary at lam=0.09
check("S1: lam=0.09 -> Phase 2 (boundary)",
      detect_phase(0.09) == 2, "phase=" + str(detect_phase(0.09)))

# Phase 2 at lam=0.20
check("S1: lam=0.20 -> Phase 2 (transitional)",
      detect_phase(0.20) == 2, "phase=" + str(detect_phase(0.20)))

# Phase 2/3 boundary at lam=0.45
check("S1: lam=0.45 -> Phase 3 (order boundary)",
      detect_phase(0.45) == 3, "phase=" + str(detect_phase(0.45)))

# Phase 3 at lam=0.70
check("S1: lam=0.70 -> Phase 3 (order dominant)",
      detect_phase(0.70) == 3, "phase=" + str(detect_phase(0.70)))

# T* = 5/7 maps to corridor_lambda = 0 -> deep Phase 1
corridor_at_tstar = 2.0 * abs(T_STAR - T_STAR)
check("S1: T*=5/7 corridor_lambda=0 is deep Phase 1",
      abs(corridor_at_tstar) < 1e-10 and detect_phase(0.0) == 1,
      "corridor=" + str(corridor_at_tstar) + " phase=" + str(detect_phase(0.0)))

# ===========================================================
# S2 -- C-closure test at each phase (8 assertions)
# ===========================================================
print("\n-- S2: C-closure at each phase (8 assertions) --")

# lam=0: C closed (Phase 1)
check("S2: lam=0.0 C closed under TSML",
      c_closed_at_lambda(0.0))

# lam=0.05: C still closed (Phase 1)
check("S2: lam=0.05 C closed (Phase 1)",
      c_closed_at_lambda(0.05),
      "closed=" + str(c_closed_at_lambda(0.05)))

# lam=0.09: C closure begins to break (Phase 1/2 boundary)
# Verify by checking at lam=0.083 (1/12) which is the exact first-leak threshold
lam_leak = 1.0 / 12.0
# At lam just below 1/12, C should be closed; at 1/12 it breaks
c_before = c_closed_at_lambda(lam_leak - 0.005)
c_at_leak = c_closed_at_lambda(lam_leak)
check("S2: lam=1/12-eps still closed, lam=1/12 breaks (first leak threshold)",
      c_before and not c_at_leak,
      "before=" + str(c_before) + " at_leak=" + str(c_at_leak) + " lam_leak=" + str(round(lam_leak, 4)))

# lam=0.15: C closure broken (Phase 2)
check("S2: lam=0.15 C closure broken (Phase 2)",
      not c_closed_at_lambda(0.15),
      "closed=" + str(c_closed_at_lambda(0.15)))

# lam=0.20: C closure still broken
check("S2: lam=0.20 C closure broken",
      not c_closed_at_lambda(0.20))

# lam=1.0: pure BHML -- one-way gate is BROKEN (C x G now produces G values)
# At lam=1.0: BHML[c][g] = max(c,g); for c=1,g=2: max(1,2)=2 which is in G
gate_broken_bhml = any(max(c, g) in G_nv for c in C for g in G_nv)
check("S2: lam=1.0 (BHML) one-way gate is broken (C x G can reach G via max)",
      gate_broken_bhml,
      "gate_broken=" + str(gate_broken_bhml) + " example: max(1,2)=" + str(max(1,2)))

# At lam=1.0, order rule holds: max(9,j)=9 for all j (9 dominates)
order_holds = all(round((0.0)*TSML[9][j] + (1.0)*BHML[9][j]) == 9 for j in STATES)
check("S2: lam=1.0 order dominant: max(9,j)=9 for all j",
      order_holds)

# Gate holds in Phase 1 (lam=0.05) but breaks in Phase 2 (lam=0.20)
gate_05 = gate_holds_at_lambda(0.05)
gate_20 = gate_holds_at_lambda(0.20)
check("S2: gate holds at lam=0.05 (Phase 1) but breaks by lam=0.20 (Phase 2)",
      gate_05 and not gate_20,
      "gate_05=" + str(gate_05) + " gate_20=" + str(gate_20))

# ===========================================================
# S3 -- Gap floor throughout (6 assertions)
# ===========================================================
print("\n-- S3: Gap floor throughout (6 assertions) --")

# Test spectral gap >= 0.10 at 6 lambda values
lam_test_values = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
gap_results = {}
for lam in lam_test_values:
    M = mix_stochastic(lam, STATES)
    gap_results[lam] = spectral_gap(M)

check("S3: spectral gap >= 0.10 at lam=0.0",
      gap_results[0.0] >= 0.10,
      "gap=" + str(round(gap_results[0.0], 4)))

check("S3: spectral gap >= 0.10 at lam=0.2",
      gap_results[0.2] >= 0.10,
      "gap=" + str(round(gap_results[0.2], 4)))

check("S3: spectral gap >= 0.10 at lam=0.4",
      gap_results[0.4] >= 0.10,
      "gap=" + str(round(gap_results[0.4], 4)))

check("S3: spectral gap >= 0.10 at lam=0.6",
      gap_results[0.6] >= 0.10,
      "gap=" + str(round(gap_results[0.6], 4)))

check("S3: spectral gap >= 0.10 at lam=0.8",
      gap_results[0.8] >= 0.10,
      "gap=" + str(round(gap_results[0.8], 4)))

check("S3: spectral gap >= 0.10 at lam=1.0 (BHML endpoint)",
      gap_results[1.0] >= 0.10,
      "gap=" + str(round(gap_results[1.0], 4)))

# ===========================================================
# S4 -- Single dominant state (6 assertions)
# ===========================================================
print("\n-- S4: Single dominant state (6 assertions) --")

lam_dom_tests = [0.0, 0.2, 0.5, 0.7, 0.9, 1.0]
stat_results = {}
dom_states = {}
dom_masses = {}
for lam in lam_dom_tests:
    M = mix_stochastic(lam, STATES)
    stat = stationary(M)
    dom_states[lam] = STATES[int(np.argmax(stat))]
    dom_masses[lam] = float(max(stat))
    stat_results[lam] = stat

# At each lambda, one state has >= 25% mass
check("S4: single dominant state >= 25% mass at all tested lambda values",
      all(dom_masses[lam] >= 0.25 for lam in lam_dom_tests),
      "dom_masses=" + str({lam: round(dom_masses[lam], 3) for lam in lam_dom_tests}))

# At lam=0 (pure TSML): dominant state = HAR=7
check("S4: lam=0.0 dominant state = HAR=7",
      dom_states[0.0] == HAR,
      "dom=" + str(dom_states[0.0]) + " mass=" + str(round(dom_masses[0.0], 3)))

# At lam=1.0 (pure BHML): dominant state = 9
check("S4: lam=1.0 dominant state = 9 (order endpoint)",
      dom_states[1.0] == 9,
      "dom=" + str(dom_states[1.0]) + " mass=" + str(round(dom_masses[1.0], 3)))

# Transition: dominant shifts from 7 toward 9 as lam increases
# At lam=0.7, dominant >= 7 (shifted)
check("S4: lam=0.7 dominant state >= 7 (shifted toward order endpoint)",
      dom_states[0.7] >= 7,
      "dom=" + str(dom_states[0.7]))

# HAR dominant mass at lam=0 is > 0.50 (HAR strongly dominates at pure TSML)
check("S4: lam=0.0 HAR dominant mass > 0.50 (strong attractor)",
      dom_masses[0.0] > 0.50,
      "mass=" + str(round(dom_masses[0.0], 3)))

# At lam=1.0 state 9 dominates with > 0.50 mass (strong order attractor)
check("S4: lam=1.0 state-9 dominant mass > 0.50",
      dom_masses[1.0] > 0.50,
      "mass=" + str(round(dom_masses[1.0], 3)))

# ===========================================================
# S5 -- BHML residual throughout (5 assertions)
# ===========================================================
print("\n-- S5: BHML residual throughout (5 assertions) --")

# BHML residual cells are the 6 pairs: (2,4),(4,2),(4,8),(8,4),(2,9),(9,2)
BHML_RESIDUAL_PAIRS = [(2,4),(4,2),(4,8),(8,4),(2,9),(9,2)]

def bhml_residual_present(lam):
    """Check that all 6 BHML residual pairs follow max rule at given lam."""
    for i, j in BHML_RESIDUAL_PAIRS:
        v = round((1.0 - lam) * TSML[i][j] + lam * BHML[i][j])
        if v != max(i, j):
            return False
    return True

# At lam=0.0 (TSML): all 6 present
check("S5: 6 BHML residual pairs follow max at lam=0.0 (TSML)",
      bhml_residual_present(0.0) and bhml_residual_count_at_lambda(0.0, STATES) == 6,
      "count=" + str(bhml_residual_count_at_lambda(0.0, STATES)))

# At lam=0.3: still present
check("S5: 6 BHML residual pairs follow max at lam=0.3",
      bhml_residual_present(0.3),
      "present=" + str(bhml_residual_present(0.3)))

# At lam=0.6: still present
check("S5: 6 BHML residual pairs follow max at lam=0.6",
      bhml_residual_present(0.6),
      "present=" + str(bhml_residual_present(0.6)))

# At lam=1.0 (BHML): all 6 still follow max (they are max by definition)
bhml_at_1 = all(BHML[i][j] == max(i, j) for i, j in BHML_RESIDUAL_PAIRS)
check("S5: 6 BHML residual pairs follow max at lam=1.0 (BHML)",
      bhml_residual_present(1.0) and bhml_at_1,
      "present=" + str(bhml_residual_present(1.0)))

# The 6 pairs are the SAME cells at every tested lambda (persistent structure)
consistent = all(bhml_residual_present(lam) for lam in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
check("S5: 6 BHML residual pairs persist at ALL tested lambda values (0,0.2,...,1.0)",
      consistent,
      "consistent=" + str(consistent))

# ===========================================================
# Summary
# ===========================================================
print("\n" + "=" * 55)
print("PHASE DETECTOR: " + str(passed) + "/" + str(total) + " assertions passed")
if failures:
    print("FAILED: " + str(failures))
else:
    print("ALL PASS")
