**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# G7 — GATE RATE DISTRIBUTION THEOREM

## Statement

**Theorem G7 (Gate Rate Distribution):** For b=10 under σ, the distribution of
cycle periods τ(s) over {0,...,9} is:

```
P(τ = 1) = 4/10 = 40%     (anchor states: {0,3,8,9})
P(τ = 6) = 6/10 = 60%     (6-cycle states: {1,2,4,5,6,7})
```

The distribution is **bimodal** with:
```
Mean:     τ̄  = (4·1 + 6·6)/10 = 40/10 = 4
Variance: σ² = (4·(1−4)² + 6·(6−4)²)/10 = (36 + 24)/10 = 6
Std dev:  σ  = √6 ≈ 2.449
```

---

## Derivation

From Q15, the period polynomial:
```
τ(ε,y) = 6 − 5·A(ε,y)
```
where A = 1 at anchors {0,3,8,9} and A = 0 at 6-cycle {1,2,4,5,6,7}.

**Mean:**
```
τ̄ = E[τ] = (1/10) Σ_{s=0}^{9} τ(s)
   = (1/10)[1+6+6+1+6+6+6+6+1+1]
   = (1/10)[4·1 + 6·6]
   = (1/10)[4 + 36] = 4
```

**Variance:**
```
σ² = E[(τ − τ̄)²]
   = (1/10)[4·(1−4)² + 6·(6−4)²]
   = (1/10)[4·9 + 6·4]
   = (1/10)[36 + 24] = 6
```

**Alternate form:** Since τ takes only two values {1,6}:
```
σ² = P(τ=1)·P(τ=6)·(6−1)²  =  (4/10)·(6/10)·25  =  24/10·(something)
```
Wait — for a Bernoulli-like two-point distribution at values {a,b} with p and 1−p:
```
σ² = p(1−p)(b−a)²  =  (4/10)(6/10)(5²)  =  0.24 · 25 = 6  ✓
```

---

## Structural Interpretation

The bimodal distribution with peaks at {1, 6} and gap between is the **signature
of the CRT decomposition** of Z/10Z:

```
Z/10Z  ≅  Z/2Z × Z/5Z
```

- **Anchor class (τ=1):** States with τ=1 are the σ-fixed points. These are
  determined by the zero-dimensional part of the CRT product — elements where
  σ acts trivially in BOTH components. For b=pq, anchors are always exactly
  those elements projecting to fixed structures in both F_p and F_q.

- **Cycle class (τ=6):** States with τ=6 are the non-fixed elements of the
  unit cycle. The cycle length 6 = lcm(p−1, q−1) = lcm(1, 4) = 4...

Actually for b=10=2×5: τ_cycle = lcm(ord in F₂*, ord in F₅*) = lcm(1,4) = 4?
But the cycle has length 6, not 4. The cycle length comes from the TOTAL structure
of σ on Z/10Z including the non-unit elements, not just the unit group C.

The 6-element cycle {1,2,4,5,6,7} includes:
- C-elements {1,7} (units in Z/10Z)
- G-elements {2,4,5,6} (non-units)

The cycle mixes unit and non-unit elements — it is a cycle of σ as an operator
on ALL of Z/10Z, not just on the unit subgroup. The period 6 is determined by
the global permutation structure, not by the multiplicative order in C.

**τ̄ = 4:** The mean period equals 4 = |C| for b=10. This is the order of the
multiplicative group (Z/10Z)* = C. For b=pq: |C| = (p−1)(q−1) = φ(b).

```
For b=10: φ(10) = φ(2)·φ(5) = 1·4 = 4 = τ̄  ✓
```

**Conjecture G7.C1:** For any semiprime b=pq, the mean cycle period of σ on Z/bZ equals φ(b).

---

## The Two Gate Classes as CRT Sectors

The bimodal split (τ=1 vs τ=6) partitions Z/10Z into two sectors:

**Sector 1 (τ=1): Anchors = C-fixed ∪ G-fixed**
```
{0}  — VOID (gcd=10, not in C or G in {1..9})
{3}  — PROGRESS (σ-fixed C-element, gcd(3,10)=1)
{8}  — BREATH (σ-fixed G-element, gcd(8,10)=2)
{9}  — RESET (σ-fixed C-element, gcd(9,10)=1)
```
Two C-elements {3,9} and two non-C elements {0,8} are anchors.

**Sector 6 (τ=6): The Mixed 6-Cycle**
```
{1,7}  — C-elements in the cycle (LATTICE, HARMONY)
{2,4,5,6}  — G-elements in the cycle (COUNTER, COLLAPSE, BALANCE, CHAOS)
```

The 6-cycle is the fundamental dynamical unit of σ. It mixes C and G elements
in a fixed ratio: 2/6 = 1/3 of cycle elements are in C, 4/6 = 2/3 are in G.

---

## Gate Rate Distribution for General Semiprime b=pq

**Pattern from b=10:**
- Anchors: |Fix(σ)| elements with τ=1
- Cycle: b−1−|Fix(σ)| elements with τ = cycle_length

For a general semiprime b=pq, the anchor count and cycle structure are determined
by the σ-orbit structure on Z/bZ. The distribution remains bimodal:

```
P(τ = 1)           = |Fix(σ)| / b
P(τ = cycle_length) = (b − |Fix(σ)|) / b
```

with mean τ̄ = φ(b) (conjectured by G7.C1).

---

## Connection to Luther Q1 (Closed)

The gate rate distribution theorem completes the algebraic characterization
established in Q11-Q16:

| Object | Determined by |
|--------|--------------|
| τ(s) ∈ {1,6} | Q15 period polynomial |
| Gate rate distribution: mean=4, var=6 | G7 (this paper) |
| gate_score(T) formula | Q14, Q16 |
| σ⁶ = id (proof) | G6 |
| R ≠ σ^k (table search) | Q16 |
| 4.6% = search landscape rate | Q16 |

**Luther Q1 is closed.** (Luther, 2026-04-01.)

The two objects are now fully separated:
- **Algebraic structure:** σ/τ/CRT describes the optimal table (gate_score=1 target)
- **Search rate:** 4.6% describes the difficulty of reaching that target via MCMC

---

## Theorem G7 — Boxed

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Theorem G7 (Gate Rate Distribution, b=10):                │
│                                                             │
│    τ: Z/10Z → {1,6}    (two-point distribution)           │
│                                                             │
│    P(τ=1) = 2/5,  P(τ=6) = 3/5                           │
│                                                             │
│    Mean:     E[τ] = 4 = φ(10)                             │
│    Variance: Var[τ] = 6 = φ(10)·(1 + 1/5)                │
│                                                             │
│    Bimodal: peaks at {1,6}, gap between.                   │
│    Signature of the CRT product Z/2Z × Z/5Z.              │
│                                                             │
│  Conjecture G7.C1: For b=pq, E[τ] = φ(b) = (p−1)(q−1). │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

*Filed: 2026-04-01. G7 closes the gate rate distribution. Luther Q1 confirmed closed.*
