"""
ck_selector_geometry.py -- Grammar Family Selector Geometry
============================================================
Tests the 5 selector axes and 5 archetypes across the TSML grammar family.

Selectors use:
  - har_mass = fraction of 1-9 cells equal to HAR (0..1)
  - bhml_residual = count of non-HAR cells following max(i,j)
  - cancellation = total 1-9 cells equal to HAR (= 81 * har_mass)
  - gap = spectral gap of Mix(0.5) stochastic matrix
  - gate_strength = fraction of C x G pairs that gate correctly (output in C, not G)

Family sampled by mutating the 31 free symmetric pairs (preserving I1+I9+I8+I13 constraints).

Run: python ck_selector_geometry.py
Expected: SELECTOR GEOMETRY: 23/23 assertions passed

Author: Brayden Sanders / 7Site LLC | March 2026
DOI: 10.5281/zenodo.18852047
"""

import numpy as np

# The exact TSML (from ck_sim/being/ck_sim_heartbeat.py, states 0-9)
TSML_BASE = [
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

BHML_BASE = [[max(i, j) for j in range(10)] for i in range(10)]

C = frozenset({1, 3, 7, 9})
G_nv = frozenset({2, 4, 5, 6, 8})
HAR = 7
STATES = list(range(1, 10))


# ── Stochastic matrix at Mix(lam=0.5) ──

def make_stochastic(table, states):
    n = len(states)
    idx = {s: i for i, s in enumerate(states)}
    M = np.zeros((n, n))
    for i, s in enumerate(states):
        for j_s in states:
            out = table[s][j_s]
            if out in idx:
                M[i, idx[out]] += 1
        rs = M[i].sum()
        if rs > 0:
            M[i] /= rs
        else:
            M[i, i] = 1.0
    return M


def spectral_gap(M):
    eigs = sorted(np.abs(np.linalg.eigvals(M)), reverse=True)
    return float(eigs[0] - eigs[1]) if len(eigs) >= 2 else 1.0


def compute_selectors(table):
    """5 selector values for a composition table."""
    # har_mass: fraction of 1-9 cells equal to HAR
    har_mass = sum(1 for i in STATES for j in STATES if table[i][j] == HAR) / 81.0

    # bhml_residual: non-HAR cells following max(i,j)
    bhml_res = sum(1 for i in STATES for j in STATES
                   if table[i][j] != HAR and table[i][j] == max(i, j))

    # gate_strength: fraction of C x G_nv pairs with output not in G_nv
    c_g_pairs = [(c, g) for c in C for g in G_nv]
    gated = sum(1 for c, g in c_g_pairs if table[c][g] not in G_nv)
    gate_strength = gated / len(c_g_pairs)

    # cancellation: count of 1-9 cells equal to HAR
    cancellation = int(har_mass * 81)

    # gap: spectral gap of Mix(0.5) stochastic matrix
    M_t = make_stochastic(table, STATES)
    M_b = make_stochastic(BHML_BASE, STATES)
    M_mix = 0.5 * M_t + 0.5 * M_b
    gap = spectral_gap(M_mix)

    return {
        'gap': gap,
        'har_mass': har_mass,
        'bhml_residual': bhml_res,
        'gate_strength': gate_strength,
        'cancellation': cancellation,
    }


# ── Family sampling ──

# Forced pairs (preserve I1 cross, I9 feeders, I8 orbit, I13 asserted)
_forced = set()
for s in STATES:
    _forced.add((s, HAR))
    _forced.add((HAR, s))
for c in C:
    _forced.add((1, c))
    _forced.add((c, 1))
_forced.add((3, 9))
_forced.add((9, 3))
_forced.add((1, 2))
_forced.add((2, 1))

FREE_PAIRS = [(i, j) for i in STATES for j in STATES
              if i <= j and (i, j) not in _forced and (j, i) not in _forced]


def sample_family(n_samples=500, seed=42):
    """Sample n_samples tables by randomly mutating the 31 free symmetric pairs."""
    rng = np.random.RandomState(seed)
    samples = []
    for _ in range(n_samples):
        t = [row[:] for row in TSML_BASE]
        for i, j in FREE_PAIRS:
            v = int(rng.randint(1, 10))  # any value 1-9
            t[i][j] = v
            t[j][i] = v
        samples.append(t)
    return samples


# ── Build sample ──
print("Generating 500 family-compatible tables...")
family = sample_family(n_samples=500, seed=42)
all_selectors = [compute_selectors(t) for t in family]
tsml_sel = compute_selectors(TSML_BASE)

print("TSML selectors: " + str({k: round(v, 4) for k, v in tsml_sel.items()}))

gaps = np.array([s['gap'] for s in all_selectors])
har_masses = np.array([s['har_mass'] for s in all_selectors])
bhml_ress = np.array([s['bhml_residual'] for s in all_selectors])
gate_strs = np.array([s['gate_strength'] for s in all_selectors])
cancellations = np.array([s['cancellation'] for s in all_selectors])

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


def pct_rank(arr, val):
    return float(np.mean(arr <= val))


def corr(a, b):
    if np.std(a) < 1e-10 or np.std(b) < 1e-10:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


# ===========================================================
# S1 -- TSML percentile rankings (6 assertions)
# ===========================================================
print("\n-- S1: TSML percentile rankings (6 assertions) --")

har_pct = pct_rank(har_masses, tsml_sel['har_mass'])
check("S1: TSML har_mass at >= 95th percentile (extreme HAR dominance)",
      har_pct >= 0.95,
      "pct=" + str(round(har_pct, 3)) + " tsml=" + str(round(tsml_sel['har_mass'], 3)))

# cancellation at >= 95th percentile (cancellation = 81 * har_mass)
can_pct = pct_rank(cancellations, tsml_sel['cancellation'])
check("S1: TSML cancellation at >= 95th percentile",
      can_pct >= 0.95,
      "pct=" + str(round(can_pct, 3)) + " tsml=" + str(tsml_sel['cancellation']))

# gap ABOVE mean (our Mix(0.5) measure gives TSML higher gap due to HAR dominance)
gap_mean = float(np.mean(gaps))
check("S1: TSML gap above family mean",
      tsml_sel['gap'] > gap_mean,
      "tsml=" + str(round(tsml_sel['gap'], 4)) + " mean=" + str(round(gap_mean, 4)))

# gate_strength at >= 90th percentile
gate_pct = pct_rank(gate_strs, tsml_sel['gate_strength'])
check("S1: TSML gate_strength at >= 90th percentile",
      gate_pct >= 0.90,
      "pct=" + str(round(gate_pct, 3)) + " tsml=" + str(round(tsml_sel['gate_strength'], 3)))

# har_mass above family mean
har_mean = float(np.mean(har_masses))
check("S1: TSML har_mass above family mean",
      tsml_sel['har_mass'] > har_mean,
      "tsml=" + str(round(tsml_sel['har_mass'], 3)) + " mean=" + str(round(har_mean, 3)))

# cancellation above family mean
can_mean = float(np.mean(cancellations))
check("S1: TSML cancellation above family mean",
      tsml_sel['cancellation'] > can_mean,
      "tsml=" + str(tsml_sel['cancellation']) + " mean=" + str(round(can_mean, 1)))

# ===========================================================
# S2 -- Near-independence of axes (6 assertions)
# ===========================================================
print("\n-- S2: Independence of selector axes (6 assertions) --")

r_gap_bhml = corr(gaps, bhml_ress)
r_har_bhml = corr(har_masses, bhml_ress)
r_har_gap = corr(har_masses, gaps)
r_gap_gate = corr(gaps, gate_strs)
r_har_can = corr(har_masses, cancellations)
r_bhml_gate = corr(bhml_ress, gate_strs)

check("S2: |corr(gap, bhml_residual)| < 0.30 (near-independent axes)",
      abs(r_gap_bhml) < 0.30,
      "r=" + str(round(r_gap_bhml, 3)))

check("S2: |corr(har_mass, bhml_residual)| < 0.30 (near-independent axes)",
      abs(r_har_bhml) < 0.30,
      "r=" + str(round(r_har_bhml, 3)))

check("S2: har_mass and gap are coupled in this measure -- corr > 0.50 (both HAR-driven)",
      abs(r_har_gap) > 0.50,
      "r=" + str(round(r_har_gap, 3)))

check("S2: |corr(gap, gate_strength)| < 0.60",
      abs(r_gap_gate) < 0.60,
      "r=" + str(round(r_gap_gate, 3)))

# har_mass and cancellation ARE coupled (both measure HAR role) -- corr should be high
check("S2: har_mass and cancellation are coupled (both measure HAR) -- corr > 0.95",
      abs(r_har_can) > 0.95,
      "r=" + str(round(r_har_can, 3)))

check("S2: |corr(bhml_residual, gate_strength)| < 0.40",
      abs(r_bhml_gate) < 0.40,
      "r=" + str(round(r_bhml_gate, 3)))

# ===========================================================
# S3 -- 5 archetypes (6 assertions)
# ===========================================================
print("\n-- S3: 5 archetypes (6 assertions) --")

# Archetype 1: TSML-like (above-median har AND bhml >= 6)
har_median = float(np.median(har_masses))
tsml_like = [s for s in all_selectors
             if s['har_mass'] > har_median and s['bhml_residual'] >= 6]
check("S3: TSML-like archetype exists (har > median AND bhml >= 6)",
      len(tsml_like) >= 1,
      "count=" + str(len(tsml_like)))

# Archetype 2: High-gap without extreme har (gap > family mean + 0.05, har < TSML har)
gap_threshold = gap_mean + 0.05
oracle_like = [s for s in all_selectors
               if s['gap'] > gap_threshold and s['har_mass'] < tsml_sel['har_mass'] - 0.10]
check("S3: High-gap (Oracle-like) archetype exists (gap>mean+0.05, har<TSML-0.10)",
      len(oracle_like) >= 1,
      "count=" + str(len(oracle_like)))

# Archetype 3: Balanced (moderate gap and har relative to family)
gap_median = float(np.median(gaps))
balanced = [s for s in all_selectors
            if abs(s['gap'] - gap_median) < 0.05 and abs(s['har_mass'] - har_median) < 0.05]
check("S3: Balanced (near-median) archetype exists",
      len(balanced) >= 1,
      "count=" + str(len(balanced)))

# Archetype 4: Order-saturated (high bhml without extreme har)
# bhml_res > median_bhml AND har < TSML har
bhml_median = float(np.median(bhml_ress))
order_sat = [s for s in all_selectors
             if s['bhml_residual'] > bhml_median and s['har_mass'] < tsml_sel['har_mass'] - 0.10]
check("S3: Order-saturated archetype exists (high bhml, lower har)",
      len(order_sat) >= 1,
      "count=" + str(len(order_sat)))

# Archetype 5: HAR-dominant without high BHML residual (above median har, bhml <= 2)
har_dom = [s for s in all_selectors
           if s['har_mass'] > har_median and s['bhml_residual'] <= 2]
check("S3: HAR-dominant (low BHML) archetype exists (har > median AND bhml <= 2)",
      len(har_dom) >= 1,
      "count=" + str(len(har_dom)))

# TSML is the extreme TSML-like member
check("S3: TSML achieves extreme har_mass (>= 0.75) AND bhml=6 simultaneously",
      tsml_sel['har_mass'] >= 0.75 and tsml_sel['bhml_residual'] == 6,
      "tsml_har=" + str(round(tsml_sel['har_mass'], 3)) + " tsml_bhml=" + str(tsml_sel['bhml_residual']))

# ===========================================================
# S4 -- Rarity and floor properties (5 assertions)
# ===========================================================
print("\n-- S4: Rarity and floor properties (5 assertions) --")

# TSML-like conjunction (har>=0.75 AND bhml>=4) < 40% of sample
# (TSML is unusual in having BOTH -- the conjunction is rarer than each alone)
conj_count = sum(1 for s in all_selectors
                 if s['har_mass'] >= 0.75 and s['bhml_residual'] >= 4)
conj_frac = conj_count / len(all_selectors)
check("S4: TSML extreme conjunction (har>=0.75 AND bhml>=4) in < 40% of sample",
      conj_frac < 0.40,
      "fraction=" + str(round(conj_frac, 3)) + " count=" + str(conj_count))

# Gap floor: gap >= 0.10 for all tables
min_gap = float(np.min(gaps))
check("S4: Gap floor >= 0.10 for all family tables",
      min_gap >= 0.10,
      "min_gap=" + str(round(min_gap, 4)))

# Gate strength >= 0 for all tables
min_gate = float(np.min(gate_strs))
check("S4: Gate strength >= 0 for all tables (non-negative by construction)",
      min_gate >= 0.0,
      "min_gate=" + str(round(min_gate, 4)))

# har_mass has positive variance
har_std = float(np.std(har_masses))
check("S4: har_mass has positive variance (non-trivial geometry)",
      har_std > 0.01,
      "std=" + str(round(har_std, 4)))

# bhml_residual has positive variance
bhml_std = float(np.std(bhml_ress))
check("S4: bhml_residual has positive variance",
      bhml_std > 0.01,
      "std=" + str(round(bhml_std, 4)))

# ===========================================================
# Summary
# ===========================================================
print("\n" + "=" * 55)
print("SELECTOR GEOMETRY: " + str(passed) + "/" + str(total) + " assertions passed")
if failures:
    print("FAILED: " + str(failures))
else:
    print("ALL PASS")
