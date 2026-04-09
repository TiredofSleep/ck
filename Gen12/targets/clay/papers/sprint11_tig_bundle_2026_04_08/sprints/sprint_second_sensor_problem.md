# SPRINT: THE SECOND SENSOR PROBLEM
## A Real Benchmark for UOP + Hybrid Design
*Benchmark: Linearized Inverted Pendulum on Cart. All matrices explicit and reproducible.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## System: Inverted Pendulum on Cart

### Why this system

The inverted pendulum on a cart (cart-pole) is the canonical 4-state benchmark in control textbooks (Ogata, Franklin, Åström). It appears in robotics, rocket guidance, and segway-type balance problems. Engineers genuinely face the question: "I can measure the pole angle. Which second sensor should I buy?"

### State-space model

**States:** x = (x₁, x₂, x₃, x₄) = (cart position, cart velocity, pole angle, pole angular velocity).

**Parameters:** Cart mass M = 1.0 kg, pole mass m = 0.1 kg, pole half-length l = 0.5 m, g = 9.81 m/s². Linearized about upright equilibrium.

**System matrix:**

A = [[0,      1,      0,      0    ],
     [0,      0,     -0.981,  0    ],
     [0,      0,      0,      1    ],
     [0,      0,     21.582,  0    ]]

Derivation:
- ẋ₁ = x₂ (position-velocity)
- ẋ₂ = −(mg/M)x₃ = −0.981·x₃ (force balance, linearized)
- ẋ₃ = x₄ (angle-angular velocity)
- ẋ₄ = g(M+m)/(Ml) · x₃ = 21.582·x₃ (torque balance, linearized)

**Eigenvalues of A:** Characteristic polynomial: λ²(λ² − 21.582) = 0? 

More carefully: det(A−λI) with the 4×4 structure. Rows 1 and 3 give λ⁴ component; cross-coupling from rows 2 and 4. Eigenvalues include λ = 0 (double, from cart position-velocity) and ±√21.582 ≈ ±4.645 (one stable, one unstable — from pole dynamics). The system is **unstable** (λ = +4.645 > 0).

**Current sensor (already installed):**

C₁ = [0, 0, 1, 0] — pole angle encoder (measures x₃ = θ).

Physical rationale: the pole angle sensor is cheapest and safest to install on the pendulum body.

---

## Observability Analysis: Current Setup

**Observability matrix** for C₁ alone (Cayley-Hamilton: need n=4 rows):

O₁ = [ C₁ ]     = [ [0, 0,  1,      0    ] ]
     [ C₁A]       [ [0, 0,  0,      1    ] ]  ← C₁A = [0,0,1,0]·A = row 3 of A
     [C₁A²]       [ [0, 0,  21.582, 0    ] ]  ← C₁A² = [0,0,0,1]·A = row 4, scaled by A₄₃
     [C₁A³]       [ [0, 0,  0,      21.582] ]

Detailed computation:
C₁ = [0,0,1,0]
C₁A = [0,0,1,0]·A: sum over rows weighted by C₁. Only row 3: [0,0,0,1].
C₁A² = [0,0,0,1]·A = row 4 of A = [0,0,21.582,0].
C₁A³ = [0,0,21.582,0]·A = 21.582·(row 3 of A) = 21.582·[0,0,0,1] = [0,0,0,21.582].

O₁ = [[0, 0,  1,      0      ],
      [0, 0,  0,      1      ],
      [0, 0,  21.582, 0      ],
      [0, 0,  0,      21.582 ]]

**Rank(O₁) = 2.** Rows 1 and 3 are proportional; rows 2 and 4 are proportional.

**Unobservable subspace:**

ker(O₁) = {x ∈ ℝ⁴ : O₁x = 0} = {x : x₃ = 0 and x₄ = 0} = span{e₁, e₂}.

**R = span{e₁, e₂} = span{(1,0,0,0), (0,1,0,0)}.**

The pole angle sensor **cannot observe cart position x₁ or cart velocity x₂.** This makes physical sense: watching the pole alone, you cannot tell if the cart is 1m left or 1m right (both give the same pole dynamics in the linearized model).

---

## Dynamics of the Unobservable Subspace

**Key computation:** How does A act on R?

A·e₁ = column 1 of A = (0,0,0,0) = 0.
A·e₂ = column 2 of A = (1,0,0,0) = e₁.

So: **A maps e₂ → e₁ → 0.** The subspace R = span{e₁,e₂} is A-invariant: A(R) ⊆ R.

**Consequence for multi-step observability:** For any v ∈ R = αe₁ + βe₂:
- Cᵢ·v = αCᵢ₁ + βCᵢ₂ (step 0)
- Cᵢ·Av = Cᵢ·(βe₁) = βCᵢ₁ (step 1)
- Cᵢ·A²v = 0 (step ≥ 2, since A²e₂ = A·e₁ = 0)

**Theorem (proved):** Sensor Cᵢ resolves both directions of R iff Cᵢ₁ ≠ 0.

**Proof:** Given Cᵢ₁ ≠ 0: from step 1 measurement βCᵢ₁ → recover β. From step 0: αCᵢ₁ + βCᵢ₂ → recover α. Both recovered. If Cᵢ₁ = 0: step 0 gives βCᵢ₂ (only β if Cᵢ₂ ≠ 0), step 1 gives 0, α permanently hidden. □

**Corollary:** The UOP score for sensor Cᵢ relative to {C₁} is:
- score = **2** if Cᵢ₁ ≠ 0 (full resolution — achieves observability)
- score = **1** if Cᵢ₁ = 0, Cᵢ₂ ≠ 0 (partial — resolves ẋ direction only)
- score = **0** if Cᵢ₁ = 0, Cᵢ₂ = 0 (structural zero — cannot resolve R at all)

---

## Candidate Sensors

Seven candidates representing physically meaningful sensor choices:

| ID | Cᵢ | Physical interpretation | Noise σᵢ | Cᵢ₁ | Cᵢ₂ | UOP score |
|---|---|---|---|---|---|---|
| f₂ | [1, 0, 0, 0] | Cart position encoder | 1.00 | 1 | 0 | **2** |
| f₃ | [0, 1, 0, 0] | Cart velocity (tachometer) | 2.00 | 0 | 1 | 1 |
| f₄ | [0, 0, 0, 1] | Pole rate gyro | **0.10** | 0 | 0 | **0** |
| f₅ | [0, 0, 2, 0] | High-precision angle encoder | **0.05** | 0 | 0 | **0** |
| f₆ | [1, 0, 1, 0] | Cart encoder + angle (combo) | 1.00 | 1 | 0 | **2** |
| f₇ | [0, 0, 1, 1] | Angle + rate gyro (combo) | 0.50 | 0 | 0 | **0** |
| f₈ | [0, 1, 0, 1] | Velocity + rate gyro | 1.00 | 0 | 1 | 1 |

**σ notes:** Rate gyros (MEMS) are extremely precise — σ₄ = 0.1 rad/s is achievable. High-precision optical angle encoders (f₅) achieve σ₅ = 0.05 rad easily. Cart encoders (f₂) are standard but subject to friction noise — σ₂ = 1.0 m is conservative. Tachometers are notoriously noisy — σ₃ = 2.0 m/s.

---

## UOP Score Computation (explicit)

**ker(O₁) = R = span{e₁, e₂}.** Reduced problem: which sensor Cᵢ has ker(O(C₁,Cᵢ)) ∩ R = {0}?

**f₂ = [1,0,0,0]:** C₂₁ = 1. Theorem: score = **2**. Full observability.
Verify: O({C₁,C₂}) includes C₂ = [1,0,0,0] and C₂A = [0,1,0,0]. Together with O₁: rank([O₁; C₂; C₂A]) = rank of matrix with rows spanning all 4 directions. = **4**. Fully observable. ✓

**f₃ = [0,1,0,0]:** C₃₁ = 0, C₃₂ = 1. score = **1** (resolves e₂ direction).
ker(O({C₁,C₃})) ∩ R: C₃·e₁ = 0, C₃·e₂ = 1. So e₂ resolved. Remaining: e₁ hidden (step 1: C₃·Ae₁ = C₃·0 = 0; no further help). ker = span{e₁}. dim = 1. score = 2−1 = 1. ✓

**f₄ = [0,0,0,1]:** C₄₁ = 0, C₄₂ = 0. score = **0**.
Prove: For all v ∈ R = αe₁ + βe₂: C₄·v = 0 (since C₄₁=C₄₂=0). C₄·Av = C₄·βe₁ = 0. C₄·A²v = 0. All steps zero. ker(O({C₁,C₄})) ⊇ R. Score = 0. ✓

**f₅ = [0,0,2,0]:** C₅ = 2·C₁. Identical null space. ker(O({C₁,C₅})) = ker(O₁). score = **0**. ✓

**f₆ = [1,0,1,0]:** C₆₁ = 1. score = **2**. Full observability (same argument as f₂, C₆₁=1).

**f₇ = [0,0,1,1]:** C₇₁ = 0, C₇₂ = 0. score = **0**. Same proof as f₄ restricted to components 1,2.

**f₈ = [0,1,0,1]:** C₈₁ = 0, C₈₂ = 1. score = **1** (same as f₃).

---

## Classical Criteria: Fisher Information

**Setup.** We compute the Fisher information contribution from sensor Cᵢ to estimating the initial state x₀ from a single measurement y = Cᵢx(t) + εᵢ at time t with noise variance σᵢ².

For initial state estimation: y = Cᵢ·e^{At}·x₀ + ε. Sensitivity: Φᵢ(t) = Cᵢ·e^{At} ∈ ℝ^{1×4}.

**FIM contribution from sensor i at time t:** Jᵢ(t) = (1/σᵢ²)·Φᵢ(t)ᵀ·Φᵢ(t).

**Instantaneous FIM (t=0):** Jᵢ(0) = (1/σᵢ²)·CᵢᵀCᵢ. This is the dominant classical term for short observation windows and captures the sensor's geometric information contribution at the start.

**Trace of Jᵢ(0):** tr(Jᵢ(0)) = (1/σᵢ²)·‖Cᵢ‖².

| Sensor | ‖Cᵢ‖² | σᵢ | tr(Jᵢ(0)) | Classical rank |
|---|---|---|---|---|
| f₂ = [1,0,0,0] | 1 | 1.00 | **1.0** | 5th |
| f₃ = [0,1,0,0] | 1 | 2.00 | 0.25 | 6th |
| **f₄ = [0,0,0,1]** | **1** | **0.10** | **100.0** | **1st** |
| **f₅ = [0,0,2,0]** | **4** | **0.05** | **1600.0** | **1st (by far)** |
| f₆ = [1,0,1,0] | 2 | 1.00 | 2.0 | 4th |
| f₇ = [0,0,1,1] | 2 | 0.50 | 8.0 | 3rd |
| f₈ = [0,1,0,1] | 2 | 1.00 | 2.0 | 4th |

**Classical ranking (by trace):** f₅ >> f₄ >> f₇ >> f₆=f₈ >> f₂ >> f₃.

**The divergence:** f₅ and f₄ rank 1st and 2nd classically. Both have UOP score = **0**.

---

## The Divergence — Exact Statement

**Proposition (proved):** Sensors f₄ and f₅ have UOP score = 0 and tr(J(0)) >> tr(J(0)) for f₂ and f₃.

- f₅ = [0,0,2,0] with σ₅ = 0.05: tr(J₅) = 1600. After adding f₅: the system is still unobservable. The cart cannot be located.
- f₄ = [0,0,0,1] with σ₄ = 0.10: tr(J₄) = 100. After adding f₄: the system is still unobservable. Same problem.
- f₂ = [1,0,0,0] with σ₂ = 1.00: tr(J₂) = 1.0. After adding f₂: fully observable. Cart can be located.

**Why a classical engineer might buy f₄ or f₅:**
A rate gyro (f₄) is a standard component (cheap, well-understood, σ=0.1 is typical MEMS spec). An engineer applying standard A-optimal sensor selection would choose f₄ — it contributes 100× more to the FIM trace than the cart encoder. The FIM trace argument says: "adding the rate gyro massively reduces estimation error."

**Why that decision is structurally wrong:**
The FIM trace increase from f₄ lands entirely in the e₄ (θ̇) direction. But e₃ (θ) and e₄ (θ̇) are already observable from C₁ (pole angle sensor). The additional precision in θ̇ is real — but it is precision on a quantity already identifiable. The cart position and velocity (e₁ and e₂) remain in the null space: zero FIM contribution from f₄, zero from f₅.

After adding f₄ to {C₁}: A-optimal criterion improves (θ̇ now estimated with 100× better precision), but the system has the same unobservable subspace R = span{e₁,e₂}. Cart position variance = ∞. No state estimator (Kalman filter or otherwise) can locate the cart.

---

## The Hybrid Protocol Applied

**Step 1 — UOP pre-screening:**

Compute score for each candidate:
- f₄: score = 0 → **ELIMINATED.** (Angular velocity direction already observable from C₁.)
- f₅: score = 0 → **ELIMINATED.** (Proportional to existing sensor.)
- f₇: score = 0 → **ELIMINATED.** (Both components blind to R.)

Survivors: {f₂, f₃, f₆, f₈}.

Protocol message: "f₄, f₅, f₇ are structurally redundant. Adding them will not reduce the unobservable subspace regardless of noise level or observation duration."

**Step 2 — Classical ranking of survivors:**

| Survivor | UOP score | tr(J(0)) | Rank among survivors |
|---|---|---|---|
| f₂ = [1,0,0,0] | 2 | 1.0 | 3rd |
| f₃ = [0,1,0,0] | 1 | 0.25 | 4th |
| f₆ = [1,0,1,0] | 2 | 2.0 | **1st** |
| f₈ = [0,1,0,1] | 1 | 2.0 | 2nd |

Among survivors, classical criterion selects f₆.

**Step 3 — Select: f₆ = [1, 0, 1, 0] (cart position + angle combined sensor).**

After adding f₆: rank(O({C₁,C₆})) = 4. System fully observable. ✓

---

## Full Decision Table

| Sensor | Physical type | σ | UOP score | tr(J₀) | Classical rank | Hybrid rank | Observability after? |
|---|---|---|---|---|---|---|---|
| **f₅** = [0,0,2,0] | High-gain angle | 0.05 | **0** | **1600** | **1st** | ELIMINATED | ✗ No |
| **f₄** = [0,0,0,1] | Rate gyro | 0.10 | **0** | **100** | **2nd** | ELIMINATED | ✗ No |
| f₇ = [0,0,1,1] | Angle+rate gyro | 0.50 | **0** | 8 | 3rd | ELIMINATED | ✗ No |
| f₆ = [1,0,1,0] | Position+angle | 1.00 | 2 | 2 | 4th | **1st** | ✓ Yes |
| f₈ = [0,1,0,1] | Velocity+gyro | 1.00 | 1 | 2 | 5th | 2nd | Partial |
| f₂ = [1,0,0,0] | Cart encoder | 1.00 | 2 | 1 | 6th | 3rd | ✓ Yes |
| f₃ = [0,1,0,0] | Tachometer | 2.00 | 1 | 0.25 | 7th | 4th | Partial |

**The classical method picks f₅ (high-gain angle sensor). The system remains unobservable. The engineer spends the budget and still cannot locate the cart.**

**The hybrid method picks f₆ (cart position + angle combo). The system becomes fully observable.**

---

## Geometric Interpretation: What Each Sensor Sees

The 4-dimensional state space splits:
- Observable subspace (from C₁): span{e₃, e₄} — pole angle and angular velocity.
- Unobservable subspace R: span{e₁, e₂} — cart position and velocity.

```
STATE SPACE PICTURE

  e₂ (cart velocity)
  ↑
  |    R = DARK (unobservable from C₁)
  |    ┌─────────────────┐
  |    │ f₄, f₅, f₇     │
  |    │ live entirely   │   e₃,e₄ plane (OBSERVABLE)
  |    │ in this region  │   → C₁ covers this
  |    └─────────────────┘
  └──────────────────────────────→ e₁ (cart position)
  
  f₂, f₆: cross the boundary ✓ (see into R)
  f₃, f₈: partially cross boundary (see e₂ but not e₁)
  f₄, f₅, f₇: stay entirely in the observable region ✗
```

f₅ = [0,0,2,0] sees 2×θ — inside the already-lit subspace. Very bright, very precise, completely useless for the dark region.

f₄ = [0,0,0,1] sees θ̇ — also inside the lit subspace. Excellent noise, zero contribution to R.

f₂ = [1,0,0,0] crosses into R (sees x₁). Lower precision but illuminates the dark region.

---

## Why the Classical Criterion Fails Here

**The failure mode has a name:** *precision amplification on already-resolved directions.*

The FIM trace criterion rewards sensors for making existing estimates more precise. A high-precision pole angle sensor makes θ measurement much better. But in a partially observable system, the already-observable directions are already identifiable in principle — infinite refinement of them does not reduce the unobservable directions.

**Analogy to the sprint-series language:** f₅ is a refinement move (same observable subspace, higher precision). f₂ is an orthogonal jump (new unobservable direction accessed). The classical criterion rewards refinement moves when they are cheap and precise. UOP insists on orthogonal jumps first.

**This is not pathological — it is systematic:** Any time:
1. The current sensor family has non-trivial unobservable subspace, AND
2. One candidate sensor has lower noise but lives in the already-observable region,

the classical FIM trace (or D-optimality) will prefer the redundant precise sensor. The better the noise characteristics of the redundant sensor, the worse the failure.

---

## Theorem (Second Sensor Problem — proved)

**Theorem (proved):** For any partially observable linear system (A, C₁) with unobservable subspace R ≠ {0}: there exist candidate sensors with arbitrarily high Fisher information trace contribution and UOP score = 0. Specifically: any sensor C₂ = α·C₁·e^{At₀} for any t₀, α has score = 0 and tr(FIM contribution) → ∞ as σ₂ → 0.

**Proof.** C₂ = α·C₁·e^{At₀} means the sensor measures the same functional of the state as C₁ measured at a different time — same information content. ker(O({C₁,C₂})) = ker(O({C₁})) (the second row is linearly dependent in the observability matrix). Score = 0. tr(J₂) = (α²/σ₂²)·‖C₁·e^{At₀}‖² → ∞ as σ₂ → 0. □

**Corollary:** The classical FIM trace is not a safe proxy for observability improvement. UOP score = 0 is a necessary pre-screening condition for any sensor worth buying.

---

## Appendix: Michaelis-Menten Second Experiment

The same pattern holds for the biology domain. After one low-substrate experiment (S₀=0.1):

Current ambiguity: R = same-ratio pairs {(V,K),(V',K') : V/K = V'/K'} — 12 unresolved pairs on 5×5 grid.

**Classical FIM:** Low-substrate experiment with σ=0.01 has FIM trace gain ≈ 1000 (very precise ratio measurement). High-substrate experiment (S₀=100) with σ=1.0 has FIM trace gain ≈ 1 (modest Vmax measurement).

**UOP scores:** Second low-substrate (any S₀ in linear regime): score = 0. High-substrate: score = 12 (= |R|, perfect complement).

**Decision:** Classical picks low-substrate repeat (σ → 0 wins). Hybrid eliminates all low-substrate repeats (score = 0 for all), selects high-substrate as unique structural survivor.

**Physical consequence:** A biologist running only low-substrate assays, no matter how precisely, cannot separately determine Vmax and Km. They learn the ratio with extreme precision. A single high-substrate experiment — even with poorer precision — gives Vmax, and the ratio from the prior experiment then gives Km. The hybrid protocol delivers this prescription mechanically.

---

## Summary

**Benchmark system:** Inverted pendulum on cart — 4 states, standard matrices, reproducible.

**Current sensor:** Pole angle encoder C₁ = [0,0,1,0]. Unobservable: cart position + velocity.

**Classical top pick:** f₅ = high-gain angle sensor (tr = 1600). UOP score = 0. System remains unobservable after installation.

**Hybrid protocol pick:** f₆ = cart position + angle combo (tr = 2). UOP score = 2. System fully observable.

**Theorem (proved):** Score-0 sensors have arbitrarily high FIM contributions as noise → 0. UOP pre-screening eliminates them. Hybrid protocol selects the minimum-score-positive sensor that maximizes classical criteria among survivors.

**Strongest honest claim:**
> The second sensor problem has a wrong answer that classical criteria will reliably produce whenever a precise but redundant sensor is available. In the inverted pendulum, a MEMS rate gyro (σ=0.1) beats a cart encoder (σ=1.0) by 100:1 on Fisher trace — yet the gyro contributes zero to observability and the encoder completes it. UOP pre-screening catches this divergence structurally, before any noise calculation is performed.

**Strongest honest boundary:**
> The inverted pendulum example uses a 4-state linear system where observability is binary (observable or not) and the unobservable subspace can be computed exactly. For nonlinear systems, high-dimensional systems, and systems with partial observability (some but not all state directions unobservable), the UOP score computation requires linearization or sampling, and the score is approximate. The hybrid protocol remains valid; the score thresholding (eliminate score < τ) needs tuning for the approximate case.
