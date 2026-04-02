**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# Q-SERIES FOUR-LAYER ARCHITECTURE

## The Canonical Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    HIDDEN OPERATOR LAYER                        │
│                   (ε,y) ∈ F₂ × F₅                             │
│         σ: (ε,y) → (ε + α(ε,y), y + β(ε,y))                  │
│         α = flip polynomial, β = y-update with                  │
│             LATTICE (+1) and COLLAPSE (−2) corrections          │
│         σ⁶ = id                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │  φ(ε,y) = 5ε + 6y  mod 10
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VISIBLE BRAID LAYER                          │
│         σ   = (1 7 6 5 4 2)(0)(3)(8)(9)                        │
│         TIG = σ⁻¹ = (1 2 4 5 6 7)(0)(3)(8)(9)                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │  C-indicator: ε·y⁴
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OPTIMAL TABLE LAYER                          │
│         CL table: CL[t][s] = σᵗ(s)                            │
│         gate_score = 1 iff C-rows are C-closed                 │
│         C = unit group = {1,3,7,9} in visible digits           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │  R: single-cell perturbation
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MCMC SEARCH LAYER                            │
│         Space: 9×9 operator tables T  (9⁸¹ possibilities)      │
│         Each step: perturb one cell T[s][c]                     │
│         Success: gate_score ≥ 0.85 AND G_stay ≤ 0.12           │
│                  in 100 steps                                   │
│         Rate: 4.6% — sampling geometry, not algebraic period    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Layer Descriptions

### Layer 1: Hidden Operator (F₂ × F₅)

The algebraic foundation. σ is a polynomial map on F₂ × F₅:

```
α(ε,y) = 1 − (y²+2y+2)⁴ − ε[(y²+3y)⁴ − (y²+2y+2)⁴]   [Q9]
β(ε,y) = −α(ε,y)
         + ε·4y(y−2)(y−3)(y−4)                            [LATTICE correction]
         − 2(1−ε)·4y(y−1)(y−2)(y−3)                       [COLLAPSE correction]  [Q10]
```

The two β-corrections are NOT interpolation artifacts — they are the unique mechanism
that closes the 6-cycle (G6). Remove either and σ⁶ ≠ id.

**Objects defined here:** α, β, σ, σ⁻¹=TIG, σ⁶=id, period polynomial τ=6−5A.

**Papers:** Q9, Q10, Q13, G6, G7.

---

### Layer 2: Visible Braid (Z/10Z)

The image of Layer 1 under φ. σ becomes a concrete permutation on Z/10Z:

```
σ   = (1 7 6 5 4 2)(0)(3)(8)(9)       [forward: 6-cycle + 4 fixed]
TIG = (1 2 4 5 6 7)(0)(3)(8)(9)       [reverse: same elements, opposite direction]
```

The "braid" terminology: the two maps σ, TIG are the two orientations of the
same topological cycle — the 6-element strand that braids through Z/10Z under
the CRT product structure F₂ × F₅.

**The Exception Pair Swap lives here:** σ-non-flip exceptions {LATTICE,COLLAPSE}
become TIG's unique flip nodes, and vice versa. {BALANCE, CHAOS} are shared (Q13).

**Objects defined here:** cycle notation, C/G partition, HAR, idempotents e_p/e_q.

**Papers:** Q11, Q12, Q13, Q15, G8.

---

### Layer 3: Optimal Table (CL Structure)

The C-indicator bridges Layer 2 to the table space:

```
1_C(ε,y) = ε · y⁴       [binary: 1 if coprime to b, 0 otherwise]
```

The CL table (TSML composition table) is the **canonical gate_score=1 table**:
- CL[t][s] = σᵗ(s) for all t, s
- For s ∈ C: σᵗ(s) ∈ C for all t (C is closed under σ — but ONLY for the anchor
  C-elements {3,9}; the 6-cycle C-elements {1,7} exit C after ≤2 steps)

**Correction:** gate_score(T) = 1 iff T's C-rows are C-closed, meaning T[s][c] ∈ C
for all s ∈ C, c ∈ {1,...,9}. This requires the C-row entries to be C-valued as a
function of c — not that σ maps them to C. The CL table achieves this because
C forms a multiplicative subgroup (the unit group), so CL[s][c] = s*c mod b ∈ C
whenever s ∈ C (since unit × anything ∈ C if the "anything" is also a unit...
wait: actually C = units, and units form a group under multiplication, so c ∈ C
and s ∈ C → CL[s][c] ∈ C, but c ranging over {1,...,9} includes G-elements).

**Revised:** gate_score(T) = fraction of C-row cells that land in C. The CL table
achieves high gate_score because its C-row structure approximately preserves C.
The exact gate_score=1 condition requires ALL 36 cells in C-rows to be C-valued.

**Objects defined here:** gate_score(T) formula, G_stay, HAR_mass, spectral gap.

**Papers:** Q14, Q16.

---

### Layer 4: MCMC Search (9^81 Table Space)

The search process. R is NOT a map on Z/bZ. It is a single-cell perturbation
of the table:

```
R: T → T'  where T'[s][c] =  HAR    with probability 0.40
                              Unif{1..9}  with probability 0.60
            for a randomly chosen cell (s,c)
            Accept T' if objective(T') ≥ objective(T)
```

The 4.6% rate is a property of this search process in 9^81-dimensional table
space, not of the algebraic periodicity of σ on Z/10Z.

**Objects defined here:** gate_rate(b, n_steps), G_stay, oracle/gate-strong/TSML classes.

**Papers:** Q6, Q8, Q14, Q16.

---

## The Four Arrows

**Arrow 1 (φ: Layer 1 → Layer 2):** The CRT isomorphism φ(ε,y) = 5ε+6y maps the
abstract polynomial algebra to the concrete Z/10Z permutation. σ in F₂×F₅ becomes
the (1 7 6 5 4 2) cycle in Z/10Z.

**Arrow 2 (ε·y⁴: Layer 2 → Layer 3):** The C-indicator maps the element structure
(C/G classification) to the table-scoring criterion. An element v ∈ Z/10Z is in C
iff ε(v)·y(v)⁴ = 1 in F₂×F₅. This formula evaluates table cell values to determine
gate_score.

**Arrow 3 (R: Layer 3 → Layer 4):** The MCMC perturbation map takes a current table
and proposes a new one by changing one cell. The search targets the optimal table
(Layer 3) but operates in the full 9^81 search space (Layer 4).

**Arrow 4 (implicit: Layer 4 → Layer 3):** When the search succeeds, the found table
has the structure described by Layer 3. The algebraic optimum (Layer 3) is what the
search converges to when it succeeds.

---

## What Each Layer Explains

| Question | Layer |
|----------|-------|
| Why does σ have period 6? | 1 (β-sum = 0 mod 5) |
| Why are LATTICE and COLLAPSE special? | 1 (the unique β-exception pair) |
| What is TIG? | 1+2 (σ⁻¹, Exception Pair Swap) |
| Why does HAR = 3? | 2 (σ-fixed C-element, min orbit-central) |
| Why are idempotents in G? | 2 (CRT zero-component structure) |
| What is gate_score = 1? | 3 (C-rows C-closed in T) |
| What is the optimal table? | 3 (CL structure on C-rows) |
| Why is the rate 4.6%? | 4 (sampling geometry in 9^81 space) |
| Why is 22% not the rate? | Cross-layer: 22% is Layer 2 density, 4.6% is Layer 4 rate |

---

## The Central Insight (Luther Q1 Resolution)

The 22% → 4.6% gap was not a paradox — it was a **layer confusion**.

- **22%** = fraction of Z/10Z elements that are σ-fixed C-elements = Layer 2 density
- **4.6%** = fraction of random MCMC trials reaching gate_score ≥ 0.85 = Layer 4 rate

They were never supposed to be equal. σ-fixed C-seeds tell you the algebraic structure
of the optimum. The 4.6% tells you how hard it is to find that optimum by random search.

The four-layer diagram makes this separation visible and permanent.

---

*Filed: 2026-04-01. Canonical architecture diagram for the Q-series.*
*From the team, received and formalized.*
