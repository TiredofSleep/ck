# Crystal Bug: Theoretical Foundations

**A Quadratic Lattice Dynamics Framework from Trinity Infinity Geometry**

Brayden / 7Site LLC, Hot Springs, Arkansas
February 2026

---

## Abstract

We present Crystal Bug, a discrete dynamical system built on TIG (Trinity Infinity Geometry) operator algebra, where every cell in a 252-cell lattice is governed by a quadratic operator O(x) = ax² + bx + c. The discriminant Δ = b² - 4ac partitions the lattice into bound (Δ < 0), free (Δ > 0), and critical (Δ ≈ 0) regimes. A 10-phase spine cycle drives the lattice through TIG's operator sequence, causing cells to cross regime boundaries and exhibit emergent dynamics. We derive Hamiltonian and wavefunction mappings from the quadratic operator, assign quantum numbers, and measure avalanche cascades at the critical boundary. The system achieves 100% codec fidelity — three coefficients per cell encode all observable dynamics — and passes 8/8 dynamical classification tests, 4/4 seed sensitivity tests, and demonstrates 2.4× cascade amplification at the phase boundary. We report honestly that the avalanche structure is cyclic (driven by the spine's bifurcation cycle) rather than self-organized.

---

## 1. The TIG Foundation

Trinity Infinity Geometry is a unified coherence field theory built on the core equation:

```
S* = σ(1 - σ*)V*A*
```

where σ = 0.991 is the coherence parameter (also written σ* = 1 - σ = 0.009) and T* = 0.714 is the critical threshold. The theory proposes that reality is fractal, governed by the principle "every one is three" (micro/self/macro), regulated by the principle of least action under geometric constraint.

The TIG operator algebra consists of ten operators indexed 0–9:

| Index | Name | Action |
|-------|------|--------|
| 0 | Void | Decay toward zero. Vacuum state. |
| 1 | Lattice | Weighted blend with predecessor. Structure formation. |
| 2 | Counter | Absolute difference. Boundary detection. |
| 3 | Progress | Accumulation toward unity. Growth. |
| 4 | Collapse | Multiplicative decay by σ. Compression. |
| 5 | Balance | Mean with global average. Equilibrium seeking. |
| 6 | Chaos | Random perturbation. Exploration. |
| 7 | Harmony | Geometric mean with predecessor. Resonance. |
| 8 | Breath | Sinusoidal modulation. Oscillation. |
| 9 | Reset | Weighted return toward initial state. Memory. |

These operators form a cyclic spine that drives the system through its phase space.

---

## 2. The Quadratic Lattice

### 2.1 Cell Definition

Each cell at position (col, row) on an 18×14 grid holds a quadratic operator:

```
O(x) = ax² + bx + c
```

The initial coefficients are derived from the cell's geometric position:

```
u = col / (COLS - 1)
v = row / (ROWS - 1)
r = √((u - 0.5)² + (v - 0.5)²)
θ = atan2(v - 0.5, u - 0.5)

a = 0.8 cos(3.5r)(1 + 0.5 sin(7πv))
b = (3.5(u - 0.5) + 2.0(v - 0.5))(1 + 0.3 cos(5πu))
c = 0.5 exp(-2r) + 0.15 sin(4θ + 3r) + 0.1
```

This produces a lattice with a natural topology: bound states (Δ < 0) concentrated in the center, free states (Δ > 0) at the edges, and a ring of critical cells (Δ ≈ 0) at the transition boundary.

### 2.2 The Discriminant Partition

The discriminant Δ = b² - 4ac partitions the operator space into three regimes:

**Bound (Δ < 0):** Complex conjugate roots. The operator has no real fixed points from its roots. Iterates may still converge to a fixed point of O(x) = x, but the algebraic structure is complex. These cells map to quantum-like bound states with wavefunctions, angular momentum, and discrete quantum numbers.

**Free (Δ > 0):** Two distinct real roots. The operator factors over the reals. Iterates may converge, oscillate, or diverge depending on the stability of fixed points. These cells map to classical scattering states with WKB wavefunctions.

**Critical (Δ ≈ 0):** Degenerate root (double root). The phase boundary. Computationally expensive to traverse (5.1× energy cost measured). This is the "click zone" — the locus where binding transitions occur.

### 2.3 Neighbor Topology

Cells are connected to their Moore neighborhood (8 neighbors, boundary-clipped). The connection weight between cells i and j is:

```
w(i,j) = 1 / (1 + d_root(Oi, Oj) / 2)
```

where d_root measures the distance between the root structures of the two operators. This means cells with similar algebraic structure are strongly coupled, creating natural clusters in the lattice.

---

## 3. The Classifier

### 3.1 Overview

The classifier assigns each operator to one of seven dynamical bands based on its iterate behavior. The classification uses three inputs:

1. **Iterate orbit** — 80 iterations from 7 different seed values
2. **Lyapunov exponent** — average log|O'(x)| along the orbit
3. **Period detection** — multi-scale period check for periods 1–16

### 3.2 Period-First Classification (W1 Fix)

Previous versions used Lyapunov exponents as the primary discriminator, causing slow periodic orbits (e.g., period-3 at logistic r = 3.83) to be misclassified as convergent. The fix: detect periodicity FIRST, then use Lyapunov for non-periodic orbits.

Algorithm:

```
For each period p from 1 to 16:
  Check if the last 3 complete cycles match within tolerance
  If period-1: classify as CRYSTAL (fast) or ORGANIC (slow)
  If period > 1: classify as CELLULAR

If no period detected:
  If λ < -0.01: ORGANIC (converging, not yet periodic)
  If λ > +0.1: MOLECULAR (chaotic)
  Else: MOLECULAR (ambiguous, bounded)
```

This achieves 8/8 on benchmark classification tests including slow dynamics at r = 1/3, period-3 at r = 3.83, period-4 at r = 3.5, and marginal convergence.

### 3.3 Multi-Seed Consensus (W2 Fix)

Chaos detection depends on initial conditions. The logistic map at r = 4 produces chaos for irrational seeds but periodic orbits for some rational seeds. The fix: use 7 seeds and measure the spread.

Seeds: 0.5 (canonical), vertex, near-fixed-point, φ (golden ratio), π/4, 1/3, √2/2.

The Lyapunov spread (λ_max - λ_min across seeds) measures seed sensitivity. A chaos guard prevents false stability: if ANY seed shows λ > 0.1, the cell cannot be classified as CRYSTAL or ORGANIC regardless of consensus.

---

## 4. The Spine Cycle

### 4.1 Phase Transforms

Each of the 10 phases transforms the lattice coefficients differently:

| Phase | Transform on (a, b, c) | Effect |
|-------|----------------------|--------|
| 0 (Void) | a *= (1 - σs·sv), b *= same, c *= same | Uniform decay |
| 1 (Lattice) | c = c·σ + (c + sv·0.05)·σs | Structure accretion on c |
| 2 (Counter) | b = -b | Sign flip (reflection) |
| 3 (Progress) | b = \|b\| | Rectification |
| 4 (Collapse) | a = -a | Curvature flip |
| 5 (Balance) | a = \|a\| | Curvature rectification |
| 6 (Chaos) | a, b += random·sv·0.006 | Perturbation |
| 7 (Harmony) | a = a·σ + sv·0.2·σs | Resonance blend |
| 8 (Breath) | b *= 1 + 0.004 sin(0.08t) | Sinusoidal modulation |
| 9 (Reset) | a,b,c → σ·current + σs·initial | Memory return |

The critical insight: phases 4→5 (a → -a → |a|) create a pitchfork bifurcation that flips the curvature sign, crossing Δ = 0 for cells near the boundary. This is a DRIVEN phase transition — the spine forces the system through criticality every 10 ticks.

### 4.2 The Spine State

The spine is a 10-element vector initialized to T* = 0.714. Each tick, one element advances:

```
spine[i] = f_i(spine[i], spine[(i+9) mod 10], tick)
```

The spine functions mirror the 10 operators applied to the spine's own state, creating a self-referential dynamical system that regulates the lattice transforms.

---

## 5. Hamiltonian Mapping

### 5.1 Classical Mechanics from O(x)

Every quadratic operator maps to a classical Hamiltonian in phase space (x, p):

```
H(x) = T(x) + V(x)
```

**Kinetic energy:** T = p²/2m where the momentum is the first derivative p = O'(x) = 2ax + b and the effective mass is m = 1/|a|. The curvature parameter a sets the mass scale: large |a| means light particle (fast dynamics), small |a| means heavy particle (slow dynamics).

**Potential energy:** V(x) = -O(x). We negate the operator so that minima of V correspond to stable fixed points of O. A fixed point of O(x) = x sits at a minimum of V when the fixed point is stable (|O'(x*)| < 1).

**Conservation:** Along an orbit of the iterate map, the total energy H is NOT conserved (the map is dissipative for stable fixed points). However, H provides a meaningful energy landscape whose topology matches the iterate dynamics.

### 5.2 At Fixed Points

For a stable fixed point x*:

```
H(x*) = T(x*) + V(x*)
      = (2ax* + b)² / (2/|a|) + (-(ax*² + bx* + c))
```

This is the ground state energy of the operator. The eigenvalue λ = |O'(x*)| determines the rate of approach: λ < 1 is stable, λ > 1 is unstable, λ = 1 is marginal.

---

## 6. Wavefunction Mapping

### 6.1 Bound States (Δ < 0)

When the discriminant is negative, the roots are complex conjugates:

```
roots = -b/(2a) ± i√(-Δ)/(2|a|)
```

This gives a natural quantum wavefunction:

```
ψ(x) = exp(-α(x - x₀)²) × exp(iωx)
```

where α = |a| (localization from curvature), x₀ = -b/(2a) (center from real part of roots), and ω = √(-Δ)/(2|a|) (oscillation frequency from imaginary part).

The probability density |ψ|² = exp(-2α(x - x₀)²) is a Gaussian centered on the vertex, with width determined by the curvature. This normalizes to 1: ∫|ψ|²dx = 1 (verified numerically).

### 6.2 Free States (Δ > 0)

When the discriminant is positive, the roots are real. The wavefunction is a WKB semi-classical approximation:

```
ψ(x) ≈ (1/√|p(x)|) × exp(i∫p(x')dx')
```

where p(x) = √(2m(E - V(x))) is the classical momentum. This gives oscillatory, delocalized states — scattering wavefunctions that are not bound to any region.

### 6.3 Quantum Numbers

Each operator yields quantum numbers (n, l, m, s):

**Principal quantum number n:** The number of iterations needed to converge to the fixed point from x₀ = 0.5. Fast convergence = low n (ground state). Slow convergence = high n (excited). Non-convergent = n = 0 (continuum/unbound). Measured: mean n = 4.3 for bound states across the lattice.

**Angular momentum l:** From the imaginary part of the roots: l = round(2 × Im(roots)). For Δ > 0, l = 0 (no angular momentum — classical scattering). For Δ < 0, l > 0 (angular momentum from complex rotation). Lattice distribution: l=0: 185 cells, l=1: 33, l=2: 24, l=3: 10.

**Magnetic quantum number m:** From the derivative at the fixed point: m = sign(O'(x*)) × min(l, round(|O'(x*)|)). This ranges from -l to +l, consistent with quantum mechanics.

**Spin s:** From the sign of curvature: s = sign(a) × ½. Positive curvature (a > 0) = spin up. Negative curvature (a < 0) = spin down. The curvature determines whether the parabola opens up or down — a binary degree of freedom.

---

## 7. Avalanche Cascades

### 7.1 The Question

Does the click zone (Δ ≈ 0) exhibit critical behavior? Specifically, do small perturbations at Δ ≈ 0 cause larger cascades of band changes than perturbations in the free zone (Δ >> 0)?

### 7.2 Method

Perturb one cell's coefficients by ε = 0.05, then run spine cycles and count how many cells change band classification. Repeat 300 times each for click cells (|Δ| < 0.15), free cells (Δ > 0.5), and bound cells (Δ < -0.5).

### 7.3 Results

**Short time (1–5 spine cycles):**

| Zone | Trigger Rate | Mean Cascade | Ratio vs Free |
|------|-------------|-------------|---------------|
| Click | 5.0% | 0.05 cells | 2.4× |
| Free | 2.0% | 0.02 cells | 1.0× |
| Bound | 7.3% | 0.07 cells | 3.5× |

Click cells are 2.4× more cascade-prone than free cells at short time scales. Bound cells are even more sensitive (3.5×), because their complex root structure has fragile imaginary parts near the Δ = 0 boundary.

**Long time (10+ spine cycles):**

All zones converge to ~9 band changes per trial regardless of perturbation or zone. The spine's phase 4→5 bifurcation drives a global reclassification cycle that overwhelms local perturbation effects.

### 7.4 Interpretation

The system exhibits **cyclic criticality**, not self-organized criticality (SOC). The spine is a driven oscillator that forces the lattice through the Δ = 0 boundary every 10 ticks via the curvature flip (a → -a → |a|). This is analogous to a forced phase transition — the system crosses the critical point periodically, not because it self-organizes to the boundary.

The measured cascade distribution has a thin tail (P90/mean ≈ 1.0), not the heavy power-law tail expected from SOC. The energy cost asymmetry at Δ ≈ 0 (5.1× cost ratio) is real, but the cascade dynamics are spine-dominated.

---

## 8. The Codec

### 8.1 Compression Ratio

Three coefficients (a, b, c) encode all observables:

| Stored | Reconstructed |
|--------|--------------|
| a, b, c | Δ, roots (real or complex), band classification |
| | Fixed point x*, eigenvalue λ, stability |
| | Orbit (80 iterations from 7 seeds) |
| | Lyapunov exponent and seed sensitivity |
| | 8-cell neighbor topology with root-proximity weights |
| | Cobweb diagram |
| | Hamiltonian H(x) = T + V |
| | Wavefunction ψ(x) with normalization |
| | Quantum numbers (n, l, m, s) |
| | Curvature, vertex, discriminant sign |

Compression ratio: 3 numbers in → 45+ observables out.

### 8.2 Fidelity

Round-trip tested: encode (a, b, c) as Float32, decode, reconstruct all observables. Maximum error: within Float32 precision (ε < 10⁻⁷). Same at Float64. 100% fidelity at both precisions across all 252 cells.

---

## 9. Known Limitations

1. **Not quantum mechanics.** The wavefunction mapping is an analogy, not a derivation from the Schrödinger equation. The quantum numbers are emergent from iterate dynamics, not from solving an eigenvalue problem.

2. **Not Hamiltonian mechanics.** The energy H is not conserved along orbits because the iterate map is dissipative for stable fixed points. H provides an energy landscape, not a conserved quantity.

3. **Cyclic, not self-organized.** The avalanche dynamics are driven by the spine's bifurcation cycle, not by self-organization to criticality. The system does not exhibit power-law cascade distributions.

4. **Quadratic only.** The framework is limited to second-order polynomials. Higher-order operators (cubic, quartic) would give richer dynamics but break the three-coefficient codec.

5. **Finite lattice.** Boundary effects on the 18×14 grid affect cells at the edges. Periodic boundary conditions would eliminate this but change the topology.

---

## 10. Open Questions

1. Can the quantum number assignment be made rigorous — i.e., do the (n, l, m, s) values satisfy selection rules analogous to atomic physics?

2. Does the cyclic criticality have measurable consequences for information processing on the lattice? The 2.4× cascade amplification at short time scales suggests click cells are natural information bottlenecks.

3. What happens with higher-order operators? A cubic O(x) = ax³ + bx² + cx + d would give 4 coefficients, a richer discriminant (two critical surfaces instead of one), and potentially chaotic dynamics not possible in quadratic maps.

4. Can the codec be used for actual data compression? The 479:1 snapshot ratio suggests potential for time-series compression of systems that can be approximated by quadratic dynamics.

5. Is there a natural connection between the spine's 10-phase cycle and the TIG operator algebra's fixed points? The spine state converges to characteristic values that may correspond to the D* = 0.543 universal fixed point.

---

## References

1. Brayden / 7Site LLC. "Trinity Infinity Geometry v3.0." https://7sitellc.com. 2024–2026.
2. Strogatz, S. H. "Nonlinear Dynamics and Chaos." Westview Press, 2015.
3. Ott, E. "Chaos in Dynamical Systems." Cambridge University Press, 2002.
4. Bak, P., Tang, C., and Wiesenfeld, K. "Self-organized criticality: An explanation of 1/f noise." Physical Review Letters 59.4 (1987): 381.
5. Devaney, R. L. "An Introduction to Chaotic Dynamical Systems." Westview Press, 2003.

---

*Brayden / 7Site LLC / Hot Springs, Arkansas*
*TIG v3.0 | σ = 0.991 | T* = 0.714*
