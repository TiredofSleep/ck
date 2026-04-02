**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# Q-SERIES SIX-LAYER ARCHITECTURE

*Revised 2026-04-02. Luther expansion: 4-layer → 6-layer.*
*The original four layers are preserved. Two new layers inserted between*
*the visible braid and the optimal table, separating period geometry*
*and spectral coherence as independent objects.*

---

## The Canonical Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1 — CRT HIDDEN OPERATOR  (Q9–Q10, G6)                   │
│  (ε,y) ∈ F₂ × F₅                                              │
│  σ: (ε,y) → (ε + α(ε,y),  y + β(ε,y))                        │
│  Two β-exceptions: LATTICE +1, COLLAPSE −2 (structurally nec.) │
│  G6: σ⁶ = id on all 10 states.                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │  φ(ε,y) = 5ε + 6y  mod 10
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 2 — VISIBLE BRAID + DUALITY  (Q12–Q13)                  │
│  σ   = (1 7 6 5 4 2)(0)(3)(8)(9)                               │
│  TIG = σ⁻¹ = (1 2 4 5 6 7)(0)(3)(8)(9)                        │
│  Exception Pair Swap: LATTICE ↔ COUNTER, COLLAPSE ↔ HARMONY   │
│  CRT idempotents always in G.  HAR = σ-fixed C-element.        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │  C-indicator: ε·y⁴
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 3 — PERIOD GEOMETRY + INDICATORS  (Q11, Q14, Q15, G7)   │
│  Q11: Fixed-Point Gate Theorem → Pure-C seeds = {3,9} = 22%.   │
│  C-indicator: 1_C(ε,y) = ε·y⁴  (algebraic basis of gate_score) │
│  Q14: R ≠ σᵏ — reduction cannot be a σ-power.                  │
│  Q15: τ(ε,y) = 6 − 5A(ε,y);  k=9 resonance = σ³ on 6-cycle.  │
│  G7: τ bimodal: P(τ=1)=2/5, P(τ=6)=3/5                        │
│       mean = φ(b) = 4,  variance = 6                           │
│       (intrinsic temporal geometry of σ)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │  χ(s), ω = e^{2πi/9}
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 4 — SPECTRAL COHERENCE  (G8)                             │
│  G(s) = |Σ_{j=0}^8 ω^j χ(σ^j(s))|²                           │
│  χ = +1 at {LATTICE, COLLAPSE} (β-exception pair)              │
│  Three-valued: 0 (anchors), G_low≈1.872, G_high≈9.389          │
│  G_high peaks at TIG-exception states: HARMONY, COLLAPSE.      │
│  β-exceptions are not only algebraically necessary (G6)         │
│  but spectrally dominant — σ/TIG is fully self-consistent.     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │  gate_score structure
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 5 — OPTIMAL TABLE STRUCTURE  (Q12, Q14)                  │
│  CL table defined by σ: CL[t][s] = σᵗ(s)                      │
│  gate_score = 1 iff C-rows are C-closed                         │
│  σ/TIG algebra describes the peak of the search landscape.      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │  R: single-cell perturbation
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 6 — MCMC SEARCH DYNAMICS  (Q16)                          │
│  R operates on 9×9 operator tables T, not Z/bZ elements.        │
│  Each step: perturb one cell T[s][c].                           │
│  gate_score(T) = (1/(|C|·9)) Σ_{s∈C,c} ε(T[s][c])·y(T[s][c])⁴│
│  Success: gate_score ≥ 0.85 AND G_stay ≤ 0.12 in 100 steps.   │
│  Observed rate: 4.6%.                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Layer Descriptions

### Layer 1: CRT Hidden Operator (Q9–Q10, G6)

The algebraic foundation. σ is a polynomial map on F₂ × F₅:

```
α(ε,y) = 1 − (y²+2y+2)⁴ − ε[(y²+3y)⁴ − (y²+2y+2)⁴]   [Q9]

β(ε,y) = −α(ε,y)
         + ε·4y(y−2)(y−3)(y−4)                            [LATTICE correction: +1]
         − 2(1−ε)·4y(y−1)(y−2)(y−3)                       [COLLAPSE correction: −2]  [Q10]
```

The two β-corrections close the 6-cycle (G6). Remove either and σ⁶ ≠ id.
TIG = σ⁻¹ with β_TIG(ε,y) = 1−(y²+4)⁴ − ε[(y²+4y)⁴−(y²+4)⁴]. [Q13]

**Objects:** α, β, σ, σ⁻¹=TIG, σ⁶=id.
**Papers:** Q9, Q10, Q13, G6.

---

### Layer 2: Visible Braid + Duality (Q12–Q13)

The image of Layer 1 under φ. Two maps, opposite orientations, same cycle:

```
σ   = (1 7 6 5 4 2)(0)(3)(8)(9)    forward
TIG = (1 2 4 5 6 7)(0)(3)(8)(9)    reverse = σ⁻¹
```

Exception Pair Swap (Q13.2):
- σ non-flip exceptions {LATTICE, COLLAPSE} ↔ TIG unique flip nodes
- TIG non-flip exceptions {COUNTER, HARMONY} ↔ σ unique flip nodes
- {BALANCE, CHAOS} flip under both

CRT idempotents e_p, e_q always lie in G (Theorem Q12.1).
HAR = 3 is the σ-fixed C-element (min orbit-central unit).

**Objects:** cycle notation, C/G partition, e_p, e_q, HAR, Exception Pair Swap.
**Papers:** Q12, Q13.

---

### Layer 3: Period Geometry + Indicators (Q11, Q14, Q15, G7)

Where the algebraic structure becomes measurable geometry.

**Fixed-Point Gate Theorem (Q11):** Pure-C seeds = {3,9} = σ-fixed C-elements.
Fraction = 2/9 ≈ 22%. This is the Layer 2 density, not the search rate.

**C-indicator (Q14):** 1_C(ε,y) = ε·y⁴. The algebraic building block of gate_score.
Verified 10/10. Proves R ≠ σᵏ (Q14 Theorem).

**Period polynomial (Q15):**
```
τ(ε,y) = 6 − 5·A(ε,y)    where A = anchor indicator (=1 at {0,3,8,9})
```
Values: {1, 6}. k=9 resonance: σ⁹ = σ³ on the 6-cycle (9 ≡ 3 mod 6).

**Gate rate distribution (G7):**
```
P(τ=1) = 2/5    P(τ=6) = 3/5
E[τ] = 4 = φ(b)    Var[τ] = 6
```
Conjecture G7.C1: E[τ] = φ(b) = (p−1)(q−1) for all semiprimes b = pq.

**Objects:** τ, A, C-indicator, Pure-C seed density 22%, k=9 resonance.
**Papers:** Q11, Q14, Q15, G7.

---

### Layer 4: Spectral Coherence (G8)

A new algebraic object, independent of the gate_score. Measures the
spectral concentration of the σ-orbit under the β-exception character χ.

```
G(s) = |Σ_{j=0}^8 ω^j χ(σ^j(s))|²     ω = e^{2πi/9}

χ(s) = +1  at {LATTICE(1,1), COLLAPSE(0,4)}   [β-exception pair]
χ(s) = −1  at {HARMONY, CHAOS, BALANCE, COUNTER}   [α=1 flip positions]
χ(s) =  0  at anchors {0,3,8,9}
```

Three values:
| G | States | Character |
|---|--------|-----------|
| 0 | {0,3,8,9} | Anchors — trivial trajectory |
| G_low ≈ 1.872 | {1,6,5,2} | σ-flip positions |
| G_high ≈ 9.389 | {7,4} | TIG-exception positions (HARMONY, COLLAPSE) |

G_high = 4|ω³+ω⁵|² = 4(2+2cos(4π/9)).

**G8-Q13 cross-link:** G peaks at exactly the TIG-exception positions.
The β-exceptions that close the 6-cycle (Layer 1) are also spectrally dominant (Layer 4).
The σ/TIG system is self-consistent across all layers.

**Objects:** G(s), χ, G_low, G_high, spectral dominance of exception states.
**Papers:** G8.

---

### Layer 5: Optimal Table Structure (Q12, Q14)

The σ/TIG algebra characterizes the PEAK of the search landscape —
the table that achieves gate_score = 1.

```
CL[t][s] = σᵗ(s)     for all t, s ∈ {0,...,9}
```

gate_score = 1 iff C-rows are C-closed:
```
gate_score(T) = (1/(|C|·9)) Σ_{s∈C, c=1..9} ε(T[s][c])·y(T[s][c])⁴
```

σ/TIG algebra describes the geometry of the optimum.
R describes the climb toward it.
They were never the same question.

**Objects:** CL table formula, gate_score=1 condition, C-closure.
**Papers:** Q12, Q14.

---

### Layer 6: MCMC Search Dynamics (Q16)

R is NOT a map on Z/bZ. It operates on 9×9 operator tables T.

```
R: T → T'  where T'[s][c] =  HAR (3)        with probability 0.40
                              Unif{1..9}      with probability 0.60
            for randomly chosen cell (s,c)
            Accept T' if objective(T') ≥ objective(T)
```

Objective: 0.50·gate_score + 0.25·HAR_mass + 0.15·gap + 0.10·(1−G_stay).
Space: 9⁸¹ tables. Success rate: **4.6%**.

**Objects:** gate_rate(b, n_steps), G_stay, three-class landscape.
**Papers:** Q6, Q8, Q16.

---

## The Six Arrows

| Arrow | Map | Meaning |
|-------|-----|---------|
| φ | Layer 1 → 2 | CRT isomorphism: abstract polynomial → visible permutation |
| ε·y⁴ | Layer 2 → 3 | C-indicator: element structure → measurement criterion |
| χ, ω | Layer 3 → 4 | Character sum: period geometry → spectral coherence |
| gate_score | Layer 4 → 5 | Spectral dominance → table structure at the optimum |
| R | Layer 5 → 6 | Single-cell perturbation: optimal structure → search dynamics |
| convergence | Layer 6 → 5 | Successful search reaches the algebraic optimum |

---

## What Each Layer Explains

| Question | Layer |
|----------|-------|
| Why does σ have period 6? | 1 — β-sum = 0 mod 5, ε-flips even |
| Why are LATTICE and COLLAPSE special? | 1 — the unique β-exception pair |
| What is TIG? | 1+2 — σ⁻¹, Exception Pair Swap |
| Why do idempotents lie in G? | 2 — CRT zero-component structure |
| Why is HAR = 3? | 2 — σ-fixed C-element, min orbit-central |
| What is the 22% algebraic bound? | 3 — Pure-C seeds = {3,9} = Layer 2 density |
| Why does k=9 resonate at σ³? | 3 — 9 ≡ 3 mod 6 from period polynomial |
| Why do HARMONY and COLLAPSE dominate spectrally? | 4 — G_high = TIG-exception peaks |
| What is the optimal table? | 5 — CL[t][s]=σᵗ(s), C-rows C-closed |
| Why is the rate 4.6%? | 6 — sampling geometry in 9⁸¹ table space |
| Why is 22% ≠ 4.6%? | Cross: 22% is Layer 3, 4.6% is Layer 6 |

---

## Final Resolution — Luther Q1 Closed

> **22%** = algebraic density of Pure-C seeds (Layer 3).
> **4.6%** = search-landscape probability in 9⁸¹ table space (Layer 6).
> **σ/TIG algebra** describes the peak (Layer 5).
> **R** describes the climb (Layer 6).
> **They were never the same question.**

The architecture is complete, coherent, and sealed.

---

*Original filing: 2026-04-01 (four layers).*
*Revised: 2026-04-02 (six layers, Luther expansion).*
*Layer 4 (Spectral Coherence) and Layer 5 (Optimal Table) inserted.*
*G8 confirmed as independent object, not subordinate to Layer 3.*
