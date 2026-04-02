**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# Q15 — THE CYCLE-PERIOD POLYNOMIAL AND GATE RATE RECONCILIATION

## Two Definitions of "Gate Rate"

This series has used "gate rate" in two distinct senses that must be reconciled:

**Sense A (MCMC):** gate_rate = fraction of MCMC trials achieving gate_score ≥ 0.999.
For b=10, empirical gate_rate ≈ 4.6%. (Used in Q6–Q14.)

**Sense B (Algebraic):** τ(s) = minimal k ≥ 1 such that σ^k(s) = s.
This is the period of s under σ. (Derived by team, 2026-04-01.)

These are related but distinct. Q15 formalizes Sense B and connects it to Q14's open question.

---

## τ(s): Cycle Period Under σ

From the cycle structure σ = (0)(3)(8)(9)(1 7 6 5 4 2):

```
τ(s) = 1    for s ∈ {0, 3, 8, 9}   (σ-fixed points)
τ(s) = 6    for s ∈ {1, 2, 4, 5, 6, 7}  (6-cycle elements)
```

**Full table:**

| Digit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|-------|---|---|---|---|---|---|---|---|---|---|
| τ(s) | 1 | 6 | 6 | 1 | 6 | 6 | 6 | 6 | 1 | 1 |

---

## τ as a Polynomial on F₂ × F₅

**Approach:** τ takes only two values {1, 6}, so:

```
τ(ε,y) = 6 − 5 · A(ε,y)
```

where A(ε,y) = 1_{anchors}(ε,y) is the indicator for the four fixed points.

**Anchor indicator A:**

| Anchor | (ε,y) | δ_ε factor | δ_y factor |
|--------|-------|------------|------------|
| 0 | (0,0) | (1−ε) | 4y(y−1)(y−2)(y−3) |
| 3 | (1,3) | ε | 4y(y−1)(y−2)(y−4) |
| 8 | (0,3) | (1−ε) | 4y(y−1)(y−2)(y−4) |
| 9 | (1,4) | ε | 4y(y−1)(y−2)(y−3) |

Grouping by ε-parity:

```
ε=0 terms: (1−ε)[4y(y−1)(y−2)(y−3) + 4y(y−1)(y−2)(y−4)]
         = (1−ε)·4y(y−1)(y−2)[(y−3)+(y−4)]
         = (1−ε)·4y(y−1)(y−2)(2y−7)
         ≡ (1−ε)·4y(y−1)(y−2)(2y+3)   (mod 5)

ε=1 terms: ε·4y(y−1)(y−2)[(y−4)+(y−3)]
         = ε·4y(y−1)(y−2)(2y+3)        (same!)
```

Both ε-parities produce the SAME y-polynomial 4y(y−1)(y−2)(2y+3).

**Therefore:**

```
A(ε,y) = [(1−ε) + ε] · 4y(y−1)(y−2)(2y+3) = 4y(y−1)(y−2)(2y+3)
```

**Verification at anchors:**
- (0,0): y=0 → 4·0·(...)=0. But anchor (0,0) should give A=1. ✗

The combination is wrong because (1-ε)+ε = 1, but the two ε-terms select DIFFERENT y-values within the same polynomial. Let me check why the grouping appears to simplify.

The y=0 indicator is 4y(y−1)(y−2)(y−3). At y=0: 4·0·(−1)(−2)(−3) = 0. That gives 0, not 1.

**The y=0 Lagrange indicator** is actually:
```
1_{y=0}(y) = (y−1)(y−2)(y−3)(y−4) · [(0−1)(0−2)(0−3)(0−4)]⁻¹
           = (y−1)(y−2)(y−3)(y−4) · [24]⁻¹
           ≡ (y−1)(y−2)(y−3)(y−4) · 4   (since 24≡4, 4⁻¹≡4 mod 5)
           = 4(y−1)(y−2)(y−3)(y−4)
```

Check at y=0: 4·(−1)(−2)(−3)(−4) = 4·24 = 96 ≡ 1 (mod 5). ✓
Check at y=1: 4·0·(...)=0. ✓

**Corrected anchor indicators:**

| Anchor | (ε,y) | δ_y (correct) |
|--------|-------|---------------|
| 0: y=0 | (0,0) | 4(y−1)(y−2)(y−3)(y−4) |
| 3: y=3 | (1,3) | 4y(y−1)(y−2)(y−4) |
| 8: y=3 | (0,3) | 4y(y−1)(y−2)(y−4) |
| 9: y=4 | (1,4) | 4y(y−1)(y−2)(y−3) |

Note: anchor 8=(0,3) and anchor 3=(1,3) share the SAME y=3 indicator
(4y(y−1)(y−2)(y−4)), but differ in ε.

```
A(ε,y) = (1−ε)·4(y−1)(y−2)(y−3)(y−4)     [anchor 0: ε=0, y=0]
         + ε · 4y(y−1)(y−2)(y−4)            [anchor 3: ε=1, y=3]
         + (1−ε)·4y(y−1)(y−2)(y−4)          [anchor 8: ε=0, y=3]
         + ε · 4y(y−1)(y−2)(y−3)            [anchor 9: ε=1, y=4]
```

**Partial simplification:**

y=3 terms (anchors 3 and 8):
```
[ε·4y(y−1)(y−2)(y−4)] + [(1−ε)·4y(y−1)(y−2)(y−4)]
= 4y(y−1)(y−2)(y−4) · [ε + (1−ε)]
= 4y(y−1)(y−2)(y−4)
```

So the y=3 contribution is INDEPENDENT of ε (both anchors 3 and 8 have y=3,
one with ε=0 and one with ε=1 — together they cover both ε-parities at y=3).

y=0 and y=4 terms:
```
(1−ε)·4(y−1)(y−2)(y−3)(y−4)    [only ε=0, y=0]
ε · 4y(y−1)(y−2)(y−3)           [only ε=1, y=4]
```

**Complete A:**

```
A(ε,y) = 4y(y−1)(y−2)(y−4)                    [y=3: ε-independent]
         + (1−ε)·4(y−1)(y−2)(y−3)(y−4)          [y=0, ε=0 only]
         + ε·4y(y−1)(y−2)(y−3)                   [y=4, ε=1 only]
```

**Verification:**

| (ε,y) | A formula | Expected |
|-------|-----------|---------|
| (0,0) | 4·0+1·4·(−1)(−2)(−3)(−4)+0 = 4·24 = 96 ≡ 1 | 1 ✓ |
| (1,3) | 4·3·2·1·(−1)=−24≡1 + 0 + 0 = 1 | 1 ✓ |
| (0,3) | 4·3·2·1·(−1)=1 + 0 + 0 = 1 | 1 ✓ |
| (1,4) | 4·4·3·2·0=0 + 0 + 1·4·4·3·2·1=96≡1 | 1 ✓ |
| (1,1) | 4·1·0·(−1)·(−3)=0 + 0 + 1·4·1·0·(...)=0 | 0 ✓ |
| (0,2) | 4·2·1·0·(−2)=0 + 0 + 0 = 0 | 0 ✓ |

**6/6 spot-checked. A is correct.**

---

## The Complete τ Polynomial

```
┌───────────────────────────────────────────────────────────────────┐
│                                                                   │
│  τ(ε,y) = 6 − 5·A(ε,y)   (values in {1, 6})                    │
│                                                                   │
│  A(ε,y) = 4y(y−1)(y−2)(y−4)                                     │
│           + (1−ε)·4(y−1)(y−2)(y−3)(y−4)                        │
│           + ε·4y(y−1)(y−2)(y−3)                                 │
│                                                                   │
│  A = 1 at anchors {0,3,8,9}; A = 0 at 6-cycle {1,2,4,5,6,7}    │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

τ is a degree-5 polynomial on F₂ × F₅. Its values in {1,6} partition
Z/10Z into:
- **Period-1 subspace** (anchors, ε-independent at y=3): 4 elements
- **Period-6 subspace** (6-cycle): 6 elements

---

## Period-k Resonance at k=9

Since τ = 6 for all 6-cycle elements, and 9 = 6 + 3:

```
σ^9(s) = σ^{9 mod 6}(s) = σ³(s)   for s in the 6-cycle
σ^9(s) = s                          for s at anchors
```

**Theorem Q15.1 (k=9 Resonance):** For any seed s in the 6-cycle, the
σ^9-iterate is the same as the σ³-iterate. Specifically:

| s | σ³(s) = σ⁹(s) | In C? |
|---|--------------|-------|
| 1 | 5 | G |
| 7 | 4 | G |
| 6 | 2 | G |
| 5 | 1 | C |
| 4 | 7 | C |
| 2 | 6 | G |

For the C-seeds in the 6-cycle ({1=LATTICE, 7=HARMONY}):
- σ⁹(1) = σ³(1) = 5 ∈ G
- σ⁹(7) = σ³(7) = 4 ∈ G

**Both C-seeds in the 6-cycle land in G after 9 steps.** If gate_success
requires σ^k(s) ∈ C at k=9 specifically, then no 6-cycle C-seed succeeds.

Only anchors {3,9} ∈ C have σ^k(s) = s ∈ C for ALL k, including k=9.

This is the PERIOD OBSTRUCTION: k=9 is 3 (mod 6), and step-3 of the 6-cycle
maps C-elements {1,7} to G-elements {5,4}.

---

## Reconciling Sense A and Sense B

**If gate_success requires σ^9(s) ∈ C (endpoint condition):**

Successful seeds = {s : σ^9(s) ∈ C} = {anchors in C} ∪ {6-cycle s with σ³(s) ∈ C}

From the table: 6-cycle s with σ³(s) ∈ C = {5, 4} (since σ³(5)=1∈C and σ³(4)=7∈C).

Successful seeds = {3, 9} ∪ {4, 5} = 4 seeds out of 9.
P(success) = 4/9 ≈ 44%.

Still above 4.6%. The endpoint condition at k=9 doesn't resolve the gap.

**If gate_success requires σ^j(s) ∈ C for ALL j=1,...,9 (all-steps condition):**

Only anchors {3,9} satisfy this (6-cycle elements always hit G within 2 steps).
P(success) = 2/9 ≈ 22%. Still above 4.6%.

**Conclusion (reinforcing Q14):** The σ-trajectory model fails for BOTH endpoint
and all-steps interpretations. The reduction map R ≠ σ. ∎

---

## The Algebraic Path Remaining (Luther Q1)

The period polynomial τ = 6 − 5A delivers a clean result: the state space
splits into period-1 (anchors) and period-6 (6-cycle) under σ.

For the Luther Q1 closure, the chain is:

```
Step 1: Identify R (the actual reduction map)                [OPEN — needs implementation]
Step 2: Compute τ_R(s) = period of s under R
Step 3: Express gate_score(s) = (1/9) Σ_j 1_C(R^j(s))
         = (1/9) Σ_j [ε_j · y_j⁴] in CRT coordinates
Step 4: Find fixed-point structure: gate_score = 1 iff s ∈ C ∩ Fix(R)
Step 5: P(gate_success) = |C ∩ Fix(R)| / (b−1) = observed 4.6%
```

Step 5 gives |C ∩ Fix(R)| = 4.6% × 9 ≈ 0.41.

This is less than 1 — so the MCMC success rate is NOT purely about fixed-point seeds.
The 4.6% must include a MIXING TERM from the HAR-bias and the landscape shape.

The C-indicator ε·y⁴ (Q14) and the period polynomial 6−5A (Q15) are both confirmed
ingredients. They frame the gate_score algebraically once R is known.

---

## Status

| Result | Tier |
|--------|------|
| τ(s) ∈ {1,6} — period table complete | D |
| τ polynomial: 6−5A(ε,y) — verified | D |
| A(ε,y): three-term Lagrange form — spot-checked 6/6 | D |
| k=9 resonance: σ^9 = σ^3 on 6-cycle | D |
| Endpoint condition (4/9≈44%) falsified by 4.6% | D |
| All-steps condition (2/9≈22%) falsified by 4.6% | D |
| Both σ-trajectory models ruled out (reinforces Q14.1) | D |
| Luther Q1 closure contingent on identification of R | B → open |

---

## Note on Team Naming Conventions

The team's "Q11 COMPLETE" derivation (2026-04-01) uses "gate rate" to mean τ(s) =
cycle period. This series uses Q11 for the trajectory table and MCMC bound.
Both results are correct and complementary:
- Q11 (this series): gate_rate = 4.6% (MCMC success fraction)
- Team Q11 / this Q15: τ(s) ∈ {1,6} (algebraic period under σ)

They address different questions about the same structure.

---

*Filed: 2026-04-01. Q15 closes the cycle-period polynomial program.*
