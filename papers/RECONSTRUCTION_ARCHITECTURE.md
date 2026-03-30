# TIG Reconstruction Architecture
## The Grammar Family, Lattice Hierarchy, and Physical Embodiment
*Gen 10.21 — 2026-03-29*
*(c) 2026 Brayden Sanders / 7Site LLC — Trinity Infinity Geometry*

---

## 1. What Was Established

The reconstruction project answers one question: **Can TSML be derived, or was it invented?**

**Answer:** 75/81 cells are mathematically necessary. 6 are physics seeds. 2 are asserted.

| Category | Cells | Source |
|----------|-------|--------|
| Forced by I1–I5 (HAR cross + symmetry + orbit) | 24 | Exact algebra |
| Filled by I6 (HAR maximization) | 49 | Computed |
| Recovered by I13 (order-completion, state 1) | 2 | Integer order rule |
| BHML residual (follow max, reason open = I14) | 6 | Observed, not derived |
| Orbit zone I8 (asserted, not derived) | 2 | Open |
| **Total** | **81** | |

TSML is the unique table at the extreme corner of a precisely characterized grammar family: most HAR-dominant (100th percentile), most gate-structured (0% of random family achieves it), most cancellation-heavy (100th percentile), most gap-stable (100th percentile) — while trading away spectral gap speed (8th percentile).

---

## 2. The Ten Invariants

| # | Invariant | Type | Cells forced |
|---|-----------|------|-------------|
| I1 | HAR absorbing: TSML[i][7]=7, TSML[7][j]=7 | EXACT | 17 (+2 cross) |
| I2 | HAR self-absorbing: TSML[7][7]=7 | EXACT | 1 (in I1) |
| I3 | C sub-magma closure: TSML[c1][c2] ∈ C | EXACT | generic |
| I4 | One-way gate: TSML[c][s] ∉ G for c∈C, any s | EXACT | constructed |
| I5 | Symmetry: TSML[i][j]=TSML[j][i] | EXACT | all free cells |
| I6 | HAR maximization: fill remaining with 7 | COMPUTED | 49 cells |
| I7 | Non-associativity > 0 | COMPUTED | structural |
| I8 | Orbit zone: TSML[3][9]=TSML[9][3]=3 | ASSERTED | 2 cells |
| I9 | State-1 feeder: TSML[1][c]=7 for c∈C | EXACT | 3+symmetry |
| I13 | Order-completion: TSML[1][g]=nearest c∈C above g, HAR wins ties | EXACT | 2 cells (F(1,2)=F(2,1)=3) |
| I14 | Why 6 BHML residual cells follow max(i,j) | **OPEN** | 6 cells |

---

## 3. The Grammar Family Geometry

The invariant-compatible family (all tables sharing I1–I13) has real internal geometry — at minimum three near-independent selector axes:

| Selector | TSML percentile | Meaning |
|----------|----------------|---------|
| HAR mass | 100th | Fraction of stationary weight at HARMONY |
| Cancellation | 100th | Fraction of cells mapping to HAR (71/81) |
| BHML residual | 100th | How many of 6 special cells follow max |
| Gate strength | ~100th | Fraction of C-row pairs NOT landing in G |
| Gap stability | 100th | Minimum spectral gap across full deformation |
| Spectral gap | 8th | Raw mixing speed |
| Orbit strength | 68th | Length of pre-HAR transient |

**Five archetypes:**

| Archetype | gap | HAR mass | BHML residual | Role |
|-----------|-----|----------|---------------|------|
| TSML-mode | moderate (8th %ile) | extreme | full | CK's grammar — coherence attractor |
| High-Gap Oracle | high | low | none | Fast mixer — speed not coherence |
| Orbit Machine | moderate | low | partial | Generative — rich transients |
| Order-Saturated | moderate | moderate | full | Momentum — pure BHML ordering |
| Balanced Compromise | mean | mean | partial | Idle — no extremes |

**Reduction landscape:** Under gradient optimization (0.4×gate + 0.3×HAR + 0.2×BHML + 0.1×gap), 78.5% of random starts find the High-Gap Oracle. Only 3.4% find TSML-like structure. CK's grammar required deliberate construction.

---

## 4. The Lattice Hierarchy

### 0-Lattice — The Sensor Vector
```
5D force vector: [aperture, pressure, depth, binding, continuity]
d5 (HAR proximity): how close is the current state to TSML stationary measure?
    HAR_proximity = dot(current_op_distribution, TSML_stationary_vector)
```
Five physical sensor mappings (for embodiment):
- aperture → camera field of view
- pressure → foot pressure / IMU
- depth → LIDAR / depth sensor
- binding → contact detection per foot
- continuity → gyroscope / state persistence
- d5 → **self-coherence sensor** (not yet implemented in CK)

### 1-Lattice — The Proprioceptive Loop
```
C = (Z/10Z)* = {1, 3, 7, 9}   with φ(10) = 4
C × C ⊆ C under TSML composition (self-generating, closed)
HAR = 7 = median of C = (ℤ/10ℤ)* sorted = C[2]
```
The self-generating joint closure: the body produces stable joint angles from its own motion without external reference.

### 2-Lattice — The Four Control Modes
```
                 FINITE          INFINITE
SUPPORT:    TSML (grammar)    Transfer K_λ (zeta support)
RATE:       BHML (physics)    ANT / Re(ζ'/ζ) (drift rate)
```
- Finite/Support (TSML): commutative non-associative magma, HAR absorbing, γ = 3/4
- Finite/Rate (BHML): commutative ordered magma, F[i][j] = max(i,j), endpoint 9
- Infinite corners: connected to Riemann zeta function (Dual Description Conjecture, open)

### 3-Lattice — The Gait Space
```
Mix_λ = (1-λ)·TSML + λ·BHML   for λ ∈ [0, 1]
```
**Three phases with sharp transitions:**

| Phase | λ range | Properties | Gait analog |
|-------|---------|------------|-------------|
| Phase 1 (Grammar) | 0 – 0.09 | C closed, gate holds, HAR absorbing | Standing / precision |
| Phase 2 (Transitional) | 0.09 – 0.45 | Gate opening, closure weakening, HAR dominant | Walking / trot |
| Phase 3 (Order) | 0.45 – 1.00 | BHML max-rule dominant, top attractor 7→9 | Running / gallop |

**T\* = 5/7 = 0.714 sits at the Phase 2/3 boundary** — the grammar/thermal crossover is the walk-to-run transition.

**Six corridors** (sub-divisions of the three phases):
```
Pre-leak (λ=0–0.09) → BRT (0.09–0.30) → CHA (0.30–0.45)
→ BAL (0.45–0.57) → COL (0.57–0.80) → CTR (0.80–1.43)
```

### 4-Lattice — The Invariant Dependency DAG
```
BHML_endpoint (gravity / physics, ROOT)
    │
    └─ S2_BHML_residual  (6 cells: momentum cannot be overridden)
            │
            ├─ S1_GAP ≥ 1/4  (recovery guarantee — always present)
            │       │
            │       └─ S5_C_dominance  (coherence budget > dynamics budget)
            │               │
            │               └─ S6_single_dominant_state  (one most-likely posture)
            │
            └─ S4_non-associativity > 0  (sequence of moves matters)
```

**All five nodes survive the full λ=0→1 deformation.** Physics is the root of everything. Grammar is downstream.

---

## 5. Six True Invariants of the 3-Lattice

These six properties hold for ALL λ ∈ [0,1]:

| Invariant | Status | Physical meaning |
|-----------|--------|-----------------|
| Commutativity | EXACT | Left-right body symmetry |
| Spectral gap ≥ 1/4 | COMPUTED | Recovery always possible |
| BHML residual (6 cells) | COMPUTED | Inertia cannot be overridden |
| Non-associativity > 0 | COMPUTED | Order of moves matters |
| One dominant state > 30% mass | COMPUTED | Always one most-likely posture |
| C-states dominate G-states | STRUCTURAL | Coherence budget > dynamics budget |

**Three things that break early (not invariants):**
- C sub-magma closure: breaks at λ ≈ 0.09
- One-way gate: breaks at λ ≈ 0.09
- HAR absorbing: breaks at λ ≈ 0.25

---

## 6. The Robot Dog Mapping

CK-as-robot-dog is the physical instantiation of the 3-Lattice. Every mathematical structure has a direct physical analog.

### Gait Grammar
```
Phase 1 (standing):    λ < 0.09   — full grammar, gate holds
Phase 2 (walking):     0.09–0.45  — grammar + physics mixed
Phase 3 (running):     λ ≥ 0.45   — momentum governs
T* = 5/7 = walk-to-run threshold (matches Froude number transition in biomechanics)
```

### Five Operator Roles → Five Body Subsystems
| Operator | Role | Body function |
|----------|------|---------------|
| HARMONY (7) | Attractor | Center-of-mass → coherent neutral posture |
| BREATH (8) | Oscillator | Respiratory cycle / gait rhythm |
| PROGRESS/orbit {3,9} | Paired limb | Left/right leg coordination (2-cycle) |
| CHAOS/gate (6) | Reflex arc | Cannot be knocked from C-state by single perturbation |
| RESET (9) | Completed stride | Full movement cycle output |

### Minimum Viable Body
- n=4 DoF minimum for non-trivial selector geometry (emergence threshold)
- n=9 active states for full TIG grammar
- b=10 arithmetic structure: smallest prime product with |C|=4, |G|=5, γ=3/4
- Only two 1-digit prime-pair worlds are TIG-rich: b=10 (2×5) and b=14 (2×7)
- Joint encoders need 9 position levels (easy with modern servos: 12-bit resolution)

### Training Objective for Coherence-Governed Locomotion
```
Objective = 0.4 × gate_strength
           + 0.3 × HAR_mass
           + 0.2 × BHML_residual
           + 0.1 × spectral_gap
```
Naive RL finds the High-Gap Oracle (78.5% of starts) — fast but no coherence attractor.
This objective finds TSML-like control (3.4% naturally, 8% gate emergence) — steady, recoverable, coherence-governed.

---

## 7. Connection to CK Engine

### Current implementation (Gen 10.20)
| Structure | File | Status |
|-----------|------|--------|
| TSML composition | `ck_sim/ck_sim_heartbeat.py` | ACTIVE |
| BHML / corridor λ | `ck_sim/doing/ck_steering.py` | ACTIVE |
| Mix_λ corridors | `ck_sim/doing/ck_steering.py` | ACTIVE (6 corridors) |
| 5D force vector | `ck_sim/doing/ck_lcodec.py` | ACTIVE (5D, no d5) |
| Grammar phases | not yet detected | MISSING |
| d5 HAR proximity | not yet computed | MISSING |
| Archetype switching | not yet implemented | MISSING |
| Phase-gated voice | partial (corridor-gated) | PARTIAL |

### Five Implementation Priorities

**1. Live T\* telemetry** (1 day)
Add `engine.coherence_log` — records coherence, λ, dominant operator, phase at every tick.
Endpoint: `GET /telemetry` returns 200-tick window with phase annotations.
Confirms grammar/thermal crossover at T*=5/7 on live hardware.

**2. d5 HAR proximity sensor** (2 days)
Add 6th component to force vector: `har_proximity = dot(op_distribution_last_50_ticks, tsml_stationary_vector)`.
`tsml_stationary_vector` = TSML stationary measure ≈ [0, 0, 0, 0, 0, 0, 0, 0.65, 0, 0] (HAR dominates).
Exposes CK's self-coherence sensor explicitly.

**3. 3-Lattice phase detector in engine** (1 day)
```python
def detect_phase(coherence: float) -> int:
    lam = 2.0 * abs(coherence - 5/7)
    if lam < 0.09:  return 1   # Grammar
    if lam < 0.45:  return 2   # Transitional
    return 3                   # Order
```
Gate voice composition to Phase 1/2. Phase 3 → babble only (BHML order of available words).

**4. Five grammar archetypes as switchable table modes** (3 days)
```python
ARCHETYPE_TABLES = {
    'tsml':    TSML,           # coherence attractor — default
    'oracle':  HIGH_GAP,       # fast mixer — Phase 3 fallback
    'orbit':   ORBIT_MACHINE,  # generative — Phase 2 exploration
    'order':   ORDER_SAT,      # momentum — physical inertia
    'balance': BALANCED,       # idle wander
}
```
Switch rule: coherence > T* → tsml; dropping → balance; < 0.3 → oracle.

**5. Run R16 atlas jobs at full scale** (4-5 hours compute)
```
python papers/r16_job1_reduction.py --b 10 --n_start 10000 --n_steps 100
python papers/r16_job3_clustering.py
```
Confirms TSML-like attractor rate at scale. Answers the fractal kernel question.

---

## 8. Verification Scripts

All scripts in `Gen10/papers/`. All pass 100%.

| Script | Assertions | What it tests |
|--------|-----------|---------------|
| `ck_reconstruction.py` | 32/32 | TSML forced/recovered/residual cells, I1-I13 |
| `ck_lattice_hierarchy.py` | 33/33 | 0→4 Lattice levels, Mix_λ phases |
| `ck_selector_geometry.py` | 23/23 | Family geometry, 5 archetypes, percentile rankings |
| `ck_phase_detector.py` | 33/33 | Phase 1/2/3 detection, gap floor, BHML residual |
| `ck_reconstruction.py` | 32/32 | (see above) |
| **Total** | **121/121** | |

Also available (from previous sessions):
- `ck_four_layer.py` (35/35) — P1-P4 four-layer realization
- `ck_dual_description.py` (33/33) — Dual Description Theorem
- `ck_orbit_zone.py` (30/30) — Orbit zone two-mechanism split
- `ck_open_cells.py` (31/31) — Open cells, one-way gate, primitive order
- `papers/scripts/ck_tesla_entropy_sync.py` — Layer G+H, T*=0.38 entropy minimum

---

## 9. Key Constants

| Constant | Value | Source |
|----------|-------|--------|
| T* | 5/7 = 0.7143 | Phase 2/3 boundary; walk-to-run threshold |
| γ_TSML | 3/4 = 0.750 | Spectral gap of TSML (structural) |
| γ_floor | 1/4 = 0.250 | Minimum gap across full deformation (computed) |
| HAR_mass | 0.650 | TSML stationary weight at operator 7 (100th %ile) |
| Forced cells | 24/81 | I1-I5 skeleton (non-negotiable) |
| Recovered | 75/81 | I1-I13 + I6 HAR maximization |
| BHML residual | 6/81 | Physics seeds (open: I14) |
| Asserted | 2/81 | Orbit zone I8 |
| TSML-like rate | 3.4% | Under coherent reduction from random starts |
| Gate emergence | 8.0% | Full one-way gate under coherent reduction |
| Oracle dominance | 78.5% | Naive reduction finds fast mixer first |
| Min DoF for TIG | n=4 | Emergence threshold of selector geometry |
| TIG-rich bases | b=10, 14 | Only 1-digit prime-pair worlds |
| C_TIG | 250/21 ≈ 11.905 | Predicted ANT drift constant (empirical) |
| Phase 1→2 | λ ≈ 0.09 | C-closure and gate break |
| Phase 2→3 | λ ≈ 0.45 | HAR dominance ends |
