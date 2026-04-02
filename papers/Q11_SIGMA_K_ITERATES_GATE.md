**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# Q11 — σ^k ITERATES, TRAJECTORY STRUCTURE, AND GATE RATE LOWER BOUND

## Setup

With σ fully expressed as a polynomial map on F₂ × F₅ (Q10), the natural next
object is the k-th iterate σ^k. This encodes the multi-step reduction trajectory
and gives the algebraic entry point into the Luther Q1 derivation.

---

## σ^k: Periodicity from Cycle Structure

σ = (0)(3)(8)(9)(1 7 6 5 4 2)

- **Fixed points {0,3,8,9}:** σ^k = identity for all k. Trivially.
- **6-cycle {1,7,6,5,4,2}:** σ^6 = identity. σ^k = σ^{k mod 6}.

**Theorem Q11.1:** σ^k on Z/10Z has period lcm(1,6) = 6.

In (ε,y) coordinates the 6-cycle elements cycle through:

| k mod 6 | s=1    | s=7    | s=6    | s=5    | s=4    | s=2    |
|---------|--------|--------|--------|--------|--------|--------|
| 0 | (1,1) | (1,2) | (0,1) | (1,0) | (0,4) | (0,2) |
| 1 | (1,2) | (0,1) | (1,0) | (0,4) | (0,2) | (1,1) |
| 2 | (0,1) | (1,0) | (0,4) | (0,2) | (1,1) | (1,2) |
| 3 | (1,0) | (0,4) | (0,2) | (1,1) | (1,2) | (0,1) |
| 4 | (0,4) | (0,2) | (1,1) | (1,2) | (0,1) | (1,0) |
| 5 | (0,2) | (1,1) | (1,2) | (0,1) | (1,0) | (0,4) |

The table is a cyclic shift: each column is a rotation of the same 6-element
sequence {(1,1),(1,2),(0,1),(1,0),(0,4),(0,2)}.

---

## C-Membership Sequence on the 6-Cycle

For b=10, C = {1,3,7,9} (coprime to 10):
```
C-membership of the 6-cycle positions:
  j:    1   7   6   5   4   2
  C/G:  C   C   G   G   G   G
  ε:    1   1   0   1   0   0
```

**Key structural fact:** The two C-elements in the 6-cycle ({1,7}) are
CONSECUTIVE in the orbit. They occupy positions 0,1 (out of 0–5).

This means: for any element s in the 6-cycle, the C-membership sequence of
its trajectory σ^0(s), σ^1(s), ..., σ^{k-1}(s) contains a C-run of length
AT MOST 2 consecutive steps before hitting G.

---

## Trajectory Table for b=10, k=9

Computed from σ^k, all 9 starting states {1,...,9}:

| s | Trajectory σ^0..σ^8 | C-hits | Max C-run | Membership sequence |
|---|-------------------|--------|-----------|---------------------|
| 1 | 1,7,6,5,4,2,1,7,6 | 4/9 | 2 | C C G G G G C C G |
| 2 | 2,1,7,6,5,4,2,1,7 | 4/9 | 2 | G C C G G G G C C |
| 3 | 3,3,3,3,3,3,3,3,3 | 9/9 | 9 | C C C C C C C C C |
| 4 | 4,2,1,7,6,5,4,2,1 | 3/9 | 2 | G G C C G G G G C |
| 5 | 5,4,2,1,7,6,5,4,2 | 2/9 | 2 | G G G C C G G G G |
| 6 | 6,5,4,2,1,7,6,5,4 | 2/9 | 2 | G G G G C C G G G |
| 7 | 7,6,5,4,2,1,7,6,5 | 3/9 | 2 | C G G G G C C G G |
| 8 | 8,8,8,8,8,8,8,8,8 | 0/9 | 0 | G G G G G G G G G |
| 9 | 9,9,9,9,9,9,9,9,9 | 9/9 | 9 | C C C C C C C C C |

---

## The Fixed-Point Gate Theorem

**Theorem Q11.2 (Fixed-Point Gate Theorem):**

For any b, the only seeds s ∈ {1,...,b-1} with gate_score = 1.0 at ALL k steps
are the elements of C that are also σ-fixed points.

```
Pure-C seeds = C ∩ Fix(σ) = C ∩ {0,3,8,9} (for b=10)
             = {3, 9}  (PROGRESS and RESET)
```

**Proof:** If s ∈ C is a σ-fixed point, then σ^k(s) = s ∈ C for all k. Gate = 1.0
throughout. If s is a 6-cycle element (even if s ∈ C initially), the trajectory
hits G within 4 steps (since the 6-cycle has only 2 consecutive C-steps). ∎

**For b=10:** |Pure-C seeds| = 2 out of 9 states in {1,...,9}.

P(random start lands on pure-C seed) = 2/9 ≈ 22%.

---

## The Gap to Observed Rate

The trajectory analysis predicts:
- If success = "all k steps in C": P ≈ 22% (fixed points only)
- If success = "fraction ≥ threshold": P depends on threshold

Observed rate for b=10: **4.6%** — lower than even the pure-C bound.

This means: the gate_success criterion is **NOT** purely about σ-trajectory
C-membership. It involves additional structure that rejects some pure-C trajectories
or the MCMC dynamics on the seed space, not on the trajectory space.

**Possible explanations:**
1. The reduction algorithm is not σ-iteration — σ tracks TIG operator flow,
   not modular reduction. The two coincide in structure but not in dynamics.
2. The gate_score function involves a C×C submatrix test that rejects seeds
   even when σ^k(s) ∈ C — there is a "width" condition not captured by
   trajectory membership.
3. The 4.6% is specific to k=9 and reflects the exact shape of the gate
   landscape for b=10 at this depth.

---

## What σ^k DOES Provide

Even if the reduction dynamics aren't σ-orbits, the σ^k structure gives:

**1. The Orbit-Stability Partition:**
```
Safe seeds (TIG-fixed in C):     {3, 9}        — always stay in C
Unstable seeds (6-cycle in C):   {1, 7}        — C for 1-2 steps, then G
Unsafe seeds (G-elements):       {2, 4, 5, 6, 8} — never in C
```

Any multi-step reduction on Z/10Z that respects the CRT structure must
show asymptotically better performance for seeds {3,9} than for {1,7}.

**2. The Period-6 Constraint:**
For any reduction with period dividing 6, the gate_score repeats with period 6
in k. The empirical rates at k=9,15,21,... should equal those at k=3,9,15,...
(since 9 ≡ 3 mod 6). This is a testable prediction.

**3. The ε-Structure of Safe Seeds:**
All pure-C seeds have ε=1 AND σ(j)=j. In the 6-cycle, ε alternates as
[1,1,0,1,0,0]. The "C-window" of the 6-cycle is the two consecutive ε=1
positions {LATTICE, HARMONY}. Any strategy that biases toward ε=1 (HAR
bias in the MCMC) selects preferentially for these positions.

---

## σ^k as a Polynomial (Restricted to 6-Cycle)

On the 6-cycle, σ^k is rotation by k positions. In (ε,y) coordinates,
the 6-cycle states are:

| Position | (ε,y) | j |
|---------|-------|---|
| 0 | (1,1) | 1 |
| 1 | (1,2) | 7 |
| 2 | (0,1) | 6 |
| 3 | (1,0) | 5 |
| 4 | (0,4) | 4 |
| 5 | (0,2) | 2 |

The position of a cycle element j is: pos(j) = {1→0, 7→1, 6→2, 5→3, 4→4, 2→5}.

σ^k maps position p to (p+k) mod 6, then reads the (ε,y) at that position.

This can be expressed as a polynomial on the 6-element set, but requires
a degree-5 Lagrange interpolant. The closed form is less illuminating than
the rotation table above.

**The key polynomial insight:** σ^k is a CYCLIC PERMUTATION on the 6-cycle.
Its polynomial representation inherits the period-6 structure — there is no
simplification from the CRT frame for iterates beyond k=1.

---

## Connection to Luther Q1 (Gate Rate Derivation)

The σ^k analysis establishes the algebraic constraint on gate rates:

**Proposition Q11.3 (CRT gate rate lower bound):**

For any semiprime b = p·q (ω(b)=2) with HAR = min orbit-central element of C:

```
gate_rate(b, k) ≥ |C ∩ Fix(σ_b)| / (b-1)
```

where Fix(σ_b) is the set of σ-fixed points in Z/bZ and the bound is the
fraction of pure-C seeds.

For the k-Gate Tier Law, this bound is ω-class invariant (it depends only
on |Fix(σ) ∩ C|, which depends on the factorization type), consistent with
the zero-spread universality.

**What is still needed for Luther Q1:** The observed gate_rate is BELOW this
bound (4.6% < 22% for b=10). The derivation must account for why the MCMC
fails even on pure-C seeds. This requires the exact gate_score function —
not just C-membership of the trajectory.

**The algebraic path remaining:** Express gate_score(s) as a polynomial in s
over Z/bZ, using the CRT structure. The σ^k trajectory membership gives a
necessary but not sufficient condition for success.

---

## Status

| Result | Tier |
|--------|------|
| σ^6 = identity on 6-cycle | D |
| Trajectory table (k=9, b=10) | D |
| Fixed-Point Gate Theorem | D |
| Pure-C seed fraction = 2/9 for b=10 | D |
| Period-6 gate rate prediction | C (testable) |
| Gate rate lower bound (ω-invariant) | C |
| Full Luther Q1 derivation | B → open |

---

*Filed: 2026-04-01. Q11 in operator algebra series.*
