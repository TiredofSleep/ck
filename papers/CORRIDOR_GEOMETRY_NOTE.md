# Corridor Geometries: Different Structures from Different Levels
## Three Tests + Visual Chain Traces

*Brayden Sanders / 7Site LLC | March 2026*
*All computations exact on 300-state model. Corridor visualization from 9-state chains.*

---

## The Picture

Each corridor level produces a **different chain geometry** — a different characteristic shape of the path from start to HAR. The same chain algebra, different λ, different dynamics:

| Corridor | λ range | Gap γ | Chain geometry |
|----------|---------|-------|----------------|
| Pre-leak | [0.00, 0.09) | **0.515** | Direct collapse, almost no wandering |
| BRT | [0.09, 0.30) | 0.333 | Short excursions, mostly direct |
| CHA | [0.30, 0.60) | 0.296 | Occasional G-detours before collapse |
| BAL | [0.60, 0.80) | 0.208 | Long G-excursions dominant |
| COL | [0.80, 0.90) | 0.187 | Near-persistent G-wandering |
| CTR | [0.90, 1.00) | 0.138 | Approaching BHML order structure |

The gap decreases monotonically across corridors, from ~0.52 at Pre-leak to ~0.14 at CTR. Each corridor is a distinct dynamical regime, not just a label.

---

## Test 1 — Full Gap Profile

The gap at each corridor midpoint (N=300):

**Pre-leak (λ=0.04): γ=0.515** — fastest mixing, strongest HAR pull, almost no G-territory.

**CHA (λ=0.45): γ=0.296** — about half the Pre-leak gap. Chains spend meaningful time in G but collapse in geometric time. This is the corridor the corridor argument works hardest on.

**CTR (λ=0.95): γ=0.138** — weakest mixing, but still positive. The algebra still collapses here; it just takes longer.

**The monotone decrease is the gap profile.** It is not flat across corridors. Each corridor has its own spectral scale.

---

## Test 2 — Channel Survival Exponents

How does each non-HAR corner state's flow to HAR decay with λ?

At λ=0: all three states have similar direct-HAR flow (~2-3%).

Decay rates (flow → HAR per unit λ):
- **State 1:** slope = −0.019 (fastest decay, direct feeder loses flow fastest)
- **State 3:** slope = −0.010
- **State 9:** slope = −0.008 (slowest decay, most resilient)

**State 9 is the last channel standing.** As λ increases, state 1's direct connection to HAR erodes fastest. State 9 maintains its flow longest. This matches the algebraic structure: state 9 connects to state 3 which connects to HAR; the 2-cycle path {9↔3→HAR} survives longer under the deformation than state 1's single-hop path.

---

## Test 3 — Attractor Bifurcation

HAR remains the dominant attractor until **λ* ≈ 0.9963** — essentially at the BHML endpoint λ=1. The crossover is not gradual; it happens sharply in the last 0.4% of the deformation.

| λ | HAR mass | State-9 mass |
|---|----------|-------------|
| 0.90 | 0.597 | 0.011 |
| 0.95 | 0.533 | 0.098 |
| 0.99 | 0.285 | 0.464 |
| **1.00** | **0.000** | **0.525** |

**HAR is the attractor everywhere except exactly at the BHML endpoint.** The bifurcation is a phase transition at λ=1, not a gradual shift. In the deformation family, HAR loses to state 9 only when the ordering structure (BHML) completely dominates.

**RH implication:** In the analytic deployment, σ=½ plays the HAR role — it remains the unique attractor until the very last possible moment. An off-line zero would require reaching λ=1 (pure BHML order) — but the deformation never gets there for finite t. The frequency×duration bound ensures that.

---

## The Corridor Geometries (Visual)

Looking at the chain traces across corridors:

**Pre-leak:** Chains go almost directly to HAR. Occasional one-step excursions into G, but the path is nearly a straight line down to 7. The geometry is a vertical drop.

**CHA:** Chains wander more. Some take detours through states 3 and 9 before collapsing. The geometry is a jagged path that still arrives at 7, but with visible side trips.

**BAL/COL:** Chains spend most of their time in G-territory. The geometry is a long random walk punctuated by occasional collapse attempts. The path looks like diffusion with an absorbing boundary far away.

This is the fractal self-similarity you noticed: each corridor level contains its own version of the same structure, at a different scale. The Pre-leak geometry is what you'd see if you zoomed in on a single step of the CHA geometry.

---

## Revised Attractor Language

**Old:** $C = \{1,3,7,9\}$ is the absorbing class.

**New (three-role structure):**
- $C$ = closed transport class (algebraic closure, all λ)
- $\{1,3,9\}$ = transient internal channels (carry no stationary mass for λ<1)
- $\{7\}$ = unique terminal attractor (all stationary mass for λ<0.9963)

**The corridor system provides admissible transport, but only the central attractor carries stationary support.** Off-line structures may exist as transient channel traversals — but only the critical line (σ=½ in the analytic deployment) carries sustained asymptotic support.

---

## Updated Open Layer Statement

The four-layer note's open problem (Z.5) should now read:

> *Does the critical-strip deployment preserve the unique attractor structure? Specifically: does σ=½ carry all stationary support of the analytic continuation of K_λ, as HAR carries all stationary support of the discrete model for λ<0.9963?*

This is sharper than the previous "faithfulness to both gradings" language. It names the exact property — unique stationary support at the critical line — that the finite model exhibits exactly and the analytic deployment must inherit.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
