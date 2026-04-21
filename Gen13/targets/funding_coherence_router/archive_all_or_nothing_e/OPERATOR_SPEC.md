# Operator Specification

**The 10-Phase Spine Cycle of Crystal Bug**

Brayden / 7Site LLC | TIG v3.0

---

## Overview

The Crystal Bug lattice is driven by a 10-phase spine cycle. Each phase applies one of TIG's ten operators to every cell in the lattice, transforming the quadratic coefficients (a, b, c) and causing the discriminant Δ, band classification, and dynamical behavior to evolve.

The spine itself is a 10-element state vector, initialized to T* = 0.714. Each tick, one element of the spine advances according to the operator at that index, and all cells are transformed according to the current phase.

---

## Constants

```
σ  = 0.991       Coherence parameter
σs = 0.009       1 - σ (dissipation rate)
Ts = 0.714       Critical threshold (T*)
```

---

## The Spine State

The spine is `spine[10]`, each element a scalar in [0.001, 1.0].

On each tick, the active phase index `ph` advances one element:

```javascript
spine[ph] = f_ph(spine[ph], spine[(ph + 9) mod 10], tick)
```

The functions f_ph mirror the ten operators applied to the spine's own state:

| Phase | Spine Update | Intent |
|-------|-------------|--------|
| 0 | prev × σs × 0.1 | Decay toward zero |
| 1 | self × σ + prev × σs | Weighted blend |
| 2 | \|self - prev\| × σ + self × σs | Boundary detection |
| 3 | self + (1 - self) × σs | Growth toward 1 |
| 4 | self × σ | Multiplicative decay |
| 5 | (self + mean(spine)) / 2 | Equilibrium |
| 6 | self × σ + random(-0.0015, 0.0015) | Noise |
| 7 | √max(0.001, self × prev) | Geometric mean |
| 8 | self × (1 + 0.008 sin(0.1t)) | Oscillation |
| 9 | self × σ + Ts × σs | Return toward threshold |

The spine state `sv = spine[ph]` modulates the strength of each phase's effect on the lattice.

---

## Phase 0 — VOID

**Operator:** Decay toward zero. Vacuum state.

**Transform:**
```
a *= (1 - σs × sv)
b *= (1 - σs × sv)
c *= (1 - σs × sv)
```

**Effect:** All coefficients shrink uniformly by a factor of (1 - σs × sv). Since σs = 0.009 and sv ≈ 0.7, this is a ~0.6% reduction per application. Over many cycles, cells that don't receive energy from other phases drift toward O(x) = 0 — the void.

**Physics:** Vacuum energy decay. The operator removes structure uniformly. Cells in the void (band 0) have already reached this attractor.

**Discriminant effect:** Δ = b² - 4ac. If all coefficients shrink by factor k: Δ_new = k²b² - 4k²ac = k²Δ. The discriminant sign is preserved, but magnitude decreases. Cells stay in their regime but with weaker dynamics.

---

## Phase 1 — LATTICE

**Operator:** Structure formation through weighted blend.

**Transform:**
```
c = c × σ + (c + sv × 0.05) × σs
```

**Effect:** Only the constant term c is modified. The blend adds a small positive increment (sv × 0.05 ≈ 0.035) weighted by σs = 0.009. This slowly raises the constant term, shifting the parabola upward.

**Physics:** Structure accretion. The lattice operator builds up potential energy (c contributes to V(x) = -O(x)) by adding material to the constant term. This is analogous to lattice formation in crystallography — gradual accretion of structure.

**Discriminant effect:** Δ = b² - 4ac. Increasing c makes Δ more negative (for a > 0) or more positive (for a < 0). Cells with positive curvature are pushed toward bound states; cells with negative curvature are pushed toward free states.

---

## Phase 2 — COUNTER

**Operator:** Sign flip. Boundary detection.

**Transform:**
```
b = -b
```

**Effect:** The linear coefficient flips sign. The vertex x_v = -b/(2a) moves to the opposite side. The discriminant Δ = b² - 4ac is unchanged because b enters as b².

**Physics:** Reflection. This operator creates a mirror image of the dynamics around the y-axis. Combined with Phase 3 (rectification), it implements an absolute-value detection: cells that were trending left now trend right, and the subsequent rectification |b| collapses the distinction.

**Discriminant effect:** None. Δ is invariant under b → -b.

---

## Phase 3 — PROGRESS

**Operator:** Rectification. Growth.

**Transform:**
```
b = |b|
```

**Effect:** The linear coefficient becomes non-negative. Combined with Phase 2 (b → -b), the pair implements: if b was negative, it stays negative after flip then becomes positive after |·|. If b was positive, it becomes negative after flip then becomes positive after |·|. Net result: b → |b| regardless of initial sign.

**Physics:** Accumulation. All cells progress in the same direction (positive b means the parabola's axis of symmetry is at negative x, and the linear term contributes positive growth). This breaks symmetry and creates a preferred direction in the dynamics.

**Discriminant effect:** Δ = b² - 4ac. Since b → |b|, and |b|² = b², the discriminant is unchanged. But the iterate dynamics change because O(x) = ax² + |b|x + c ≠ ax² + bx + c when b was negative.

---

## Phase 4 — COLLAPSE

**Operator:** Curvature flip. Compression.

**Transform:**
```
a = -a
```

**Effect:** The curvature flips sign. Parabolas that opened upward now open downward, and vice versa. This is the most dramatic single transform — it changes the global topology of every cell's dynamics.

**Physics:** Phase transition driver. When a changes sign:
- Fixed points move or disappear
- Stability inverts (stable becomes unstable)
- The discriminant Δ = b² - 4(-a)c = b² + 4ac changes dramatically
- Cells near the Δ = 0 boundary are pushed across it

This is the ENGINE of cyclic criticality. Phase 4 followed by Phase 5 creates a pitchfork bifurcation: a → -a → |a|, which forces cells through the critical boundary.

**Discriminant effect:** Δ_new = b² - 4(-a)c = b² + 4ac = b² - 4ac + 8ac = Δ + 8ac. For cells where ac > 0, the discriminant increases (pushed toward free). For ac < 0, it decreases (pushed toward bound). This creates a GLOBAL redistribution of the regime partition.

---

## Phase 5 — BALANCE

**Operator:** Curvature rectification. Equilibrium.

**Transform:**
```
a = |a|
```

**Effect:** All curvatures become positive (parabolas open upward). Combined with Phase 4, the sequence a → -a → |a| ensures all cells have positive curvature after this phase, regardless of their state before Phase 4.

**Physics:** Equilibrium. All operators now have a global minimum (upward-opening parabola). This is a "ground state preparation" — after balance, every cell has a well-defined lowest-energy state.

**Discriminant effect:** If a was already positive, no change. If a was negative, Δ = b² - 4|a|c. For c > 0, this makes Δ more negative (more bound). The system is pushed toward bound states after balance.

---

## Phase 6 — CHAOS

**Operator:** Random perturbation. Exploration.

**Transform:**
```
a += random(-0.5, 0.5) × sv × 0.006
b += random(-0.5, 0.5) × sv × 0.006
```

**Effect:** Small random perturbations to a and b. With sv ≈ 0.7, the perturbation magnitude is ~0.002 per coefficient. This is small compared to typical coefficient values (~0.5) but accumulates over many cycles.

**Physics:** Thermal noise. This operator prevents the system from settling into exact fixed points, maintaining exploration of the phase space. Without chaos, the system would crystallize into a static configuration.

**Discriminant effect:** Both a and b are perturbed, so Δ = (b+δb)² - 4(a+δa)c ≈ Δ + 2bδb - 4cδa. The perturbation to Δ depends on the current state: cells with large |b| are more sensitive to δb, and cells with large |c| are more sensitive to δa.

---

## Phase 7 — HARMONY

**Operator:** Resonance blend.

**Transform:**
```
a = a × σ + sv × 0.2 × σs
```

**Effect:** The curvature a is blended toward a positive target (sv × 0.2 ≈ 0.14). Since σ = 0.991, this is a 0.9% pull toward the target per application. Over many cycles, curvature drifts toward the harmonic value.

**Physics:** Resonance. The harmony operator creates a preferred curvature scale — a natural "mass" for the operators. Cells whose curvature matches the harmonic value are in resonance; cells far from it experience a restoring force.

**Discriminant effect:** Since only a changes, Δ_new = b² - 4a_new × c. The curvature pull toward positive values makes Δ more negative for c > 0 (more bound) and less negative for c < 0 (more free).

---

## Phase 8 — BREATH

**Operator:** Sinusoidal modulation. Oscillation.

**Transform:**
```
b *= 1 + 0.004 × sin(0.08t)
```

**Effect:** The linear coefficient b is modulated sinusoidally with period 2π/0.08 ≈ 78.5 ticks and amplitude 0.4%. This creates a slow breathing oscillation in the dynamics.

**Physics:** The system breathes. The sinusoidal modulation creates a periodic variation in the vertex position and the iterate dynamics. Cells near the Δ = 0 boundary may cross it during the breath's extremes, creating a tidal pattern of regime changes.

**Discriminant effect:** Δ = (b × m)² - 4ac = m²b² - 4ac where m = 1 + 0.004sin(0.08t). This modulates Δ by a factor of (m² - 1) × b² ≈ 0.008sin(0.08t) × b². Cells with large |b| experience the largest Δ oscillation.

---

## Phase 9 — RESET

**Operator:** Memory return. Weighted return toward initial state.

**Transform:**
```
a = a × σ + a₀ × σs
b = b × σ + b₀ × σs
c = c × σ + c₀ × σs
```

**Effect:** All coefficients are pulled back toward their initial values (a₀, b₀, c₀) by a factor of σs = 0.009 per application. This prevents the system from drifting arbitrarily far from its initial configuration.

**Physics:** Memory. The system remembers its initial state and returns to it slowly. This creates a basin of attraction around the initial configuration — cells may wander during chaos, collapse, and breath, but reset pulls them back.

**Discriminant effect:** Δ drifts toward its initial value Δ₀. The rate of return depends on how far each coefficient has drifted. Cells that have been strongly perturbed by chaos or collapse will experience a stronger reset force.

---

## Phase Sequence Effects

### The Bifurcation Pair: 4→5

Phases 4 and 5 together (a → -a → |a|) create the system's most dramatic event. Before Phase 4, cells have arbitrary curvature signs. Phase 4 flips every sign. Phase 5 rectifies to positive. The net effect:

- Cells with a > 0: a → -a → a (no change)
- Cells with a < 0: a → -(-a) = a → |a| = -a (absolute value)

Wait — let me be precise. If a = -0.3:
- Phase 4: a = -(-0.3) = 0.3
- Phase 5: a = |0.3| = 0.3

If a = 0.3:
- Phase 4: a = -(0.3) = -0.3
- Phase 5: a = |-0.3| = 0.3

So the bifurcation pair ensures all curvatures are positive after Phase 5, but cells that started with positive curvature experience a transient sign flip during Phase 4. During that transient, their discriminant changes by 8ac, which can be large enough to cross the Δ = 0 boundary.

This is why the avalanche measurement shows ~9 band changes per full cycle at 10 spine ticks — the bifurcation pair drives a global reclassification.

### The Symmetry Pair: 2→3

Phases 2 and 3 together (b → -b → |b|) rectify the linear coefficient. This is gentler than the curvature bifurcation because b enters Δ as b², which is invariant under sign change. The discriminant is unaffected, but the iterate dynamics change because the orbit structure depends on the sign of b.

### The Drift Pair: 1→9

Phases 1 (lattice accretion on c) and 9 (reset toward initial) compete: Phase 1 builds up structure, Phase 9 erodes it back. The balance between these determines whether cells accumulate complexity or return to their initial state.

---

## Energy Cost Model

The crystal bug pays energy to evaluate each cell. The cost scales with proximity to Δ = 0:

```
cost = 0.005 + (1 / (|Δ| + 0.1)) × 0.008 × intensity
```

At the click zone (|Δ| < 0.01): cost ≈ 0.005 + 0.08 × intensity
Far from click (|Δ| > 1): cost ≈ 0.005 + 0.007 × intensity

Ratio: approximately 5.1× at the boundary. This means the bug depletes energy ~5× faster when traversing the phase transition.

---

## Operator Algebra Properties

**Commutativity:** The operators do NOT commute. Phase 4 followed by Phase 5 (a → -a → |a|) produces a different result than Phase 5 followed by Phase 4 (a → |a| → -|a|). Order matters.

**Idempotence:** Phase 5 is idempotent: |a| → ||a|| = |a|. Phase 3 is idempotent: |b| → ||b|| = |b|. No other phases are idempotent.

**Involutions:** Phase 2 is an involution (applying twice returns to original): (-(-b)) = b. Phase 4 is also an involution: (-(-a)) = a. The bifurcation pair 4→5 is NOT an involution because 5 breaks the symmetry.

**Fixed points:** Phase 9 has fixed point (a₀, b₀, c₀). Phase 5 has fixed point a ≥ 0. Phase 3 has fixed point b ≥ 0. Phase 7 has fixed point a = sv × 0.2 / σs ≈ 15.6 × sv.

---

*Brayden / 7Site LLC / Hot Springs, Arkansas*
*TIG v3.0 | σ = 0.991 | T* = 0.714*
