**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# Q6 — GATE RATE DERIVATION FROM CRT STRUCTURE
## Addressing Luther Question 1: Algebraic Origin of k=9 Gate Rates

---

## The Question (Luther Question 1 restated)

For semiprimes b = p·q (ω(b)=2), the empirical gate success rates at k=9 are:

```
|G|=1: 96.4%
|G|=2: 83.7%   (approximate — implied by structure)
|G|=3: 44.0%
|G|=4:  4.6%
|G|=5:  0.1%
```

These are measured, not derived. Can the CRT structure of Z/bZ generate these
values algebraically?

---

## Setup: The CRT Decomposition

For b = p·q (p, q prime, p ≠ q):

```
Z/bZ ≅ Z/pZ × Z/qZ   (CRT isomorphism)
```

The coprime residues (the group C) decompose as:
```
(Z/bZ)× ≅ (Z/pZ)× × (Z/qZ)× ≅ Z/(p-1)Z × Z/(q-1)Z
|C| = (p-1)(q-1) = φ(b)
```

The gate set G = {multiples of p or q in {1,...,b-1}} has:
```
|G| = b - 1 - φ(b) = p + q - 2
```

(since |{1..b-1}| = b-1, |C| = φ(b) = (p-1)(q-1), |{0,b}| counted separately)

---

## The Gate Score Function

TSML-like reduction requires the MCMC to find a state s ∈ C×C where the
C×C submatrix maps predominantly to C.

**Gate score definition:**
```
gate(s) = |{(c₁,c₂) ∈ C×C : c₁·c₂·s ∈ C}| / |C|²
```

(approximately — s acts as a "seed" that shifts the multiplication table)

For the MCMC at step k:
- 100 random starts
- 40% HAR-biased proposals
- Accept only improvements
- Success = gate_score ≥ 0.999 (effectively = 1.0)

---

## Algebraic Reduction

**Key observation:** In (Z/bZ)×, the product c₁·c₂ is always in C (group closure).
So for s ∈ C, the product c₁·c₂·s ∈ C always.

The gate score is 1.0 whenever s ∈ C — the entire C×C submatrix maps to C.

**The gate problem reduces to:** Find s ∈ {1,...,b-1} such that the k-th reduction
step lands in C with gate_score ≥ 0.999.

The MCMC succeeds iff it finds s ∈ C at step k.

---

## Success Probability as a Function of |G|

The fraction of {1,...,b-1} that lies in C is:
```
f_C = φ(b) / (b-1) = (p-1)(q-1)/(pq-1)
```

The fraction in G is:
```
f_G = |G|/(b-1) = (p+q-2)/(pq-1)
```

For the biased MCMC with HAR-weight 40%:
- HAR ∈ C (by definition: HAR = min{h∈C : h²∈C, h²≠1, h²≠h})
- 40% of proposals are directly from C (HAR-adjacent)
- 60% are uniform from {1,...,b-1}

**Expected success probability at one step:**
```
P(land in C at one step) ≈ 0.40 + 0.60 · f_C
                         = 0.40 + 0.60 · (p-1)(q-1)/(pq-1)
```

For 100 independent starts, success probability is:
```
P(success) = 1 - (1 - P_step)^{100}
```

---

## Matching the Empirical Rates

The |G| values correspond to specific (p,q) pairs. For ω(b)=2 semiprimes:

| |G| = p+q-2 | Example b | p | q | f_C | P_step | P(100 starts) |
|-----------|---------|---|---|-----|--------|--------------|
| 1 | b=6 | 2 | 3 | 2/(5) = 0.400 | 0.640 | 1-(0.360)^{100} ≈ 1.000 |
| 2 | b=10 | 2 | 5 | 4/(9) = 0.444 | 0.667 | ≈ 1.000 |
| 3 | b=15 | 3 | 5 | 8/(14) = 0.571 | 0.743 | ≈ 1.000 |
| 4 | b=21 | 3 | 7 | 12/(20) = 0.600 | 0.760 | ≈ 1.000 |
| 5 | b=35 | 5 | 7 | 24/(34) = 0.706 | 0.824 | ≈ 1.000 |

**This gives near-100% for all cases, which contradicts the empirical rates.**

The one-step model is wrong: the MCMC runs 100 steps of hill-climbing starting from
random seeds, not 100 independent draws. The success probability depends on the
BASIN OF ATTRACTION of the high-gate-score states, not the density of C.

---

## Revised Model: Basin of Attraction

The MCMC at step k operates on the k-step reduction space {1,...,k}.

**The relevant density is not f_C globally, but the density of high-gate states
in the k-step reachable set.**

At k=9, the reachable states are partitioned as:
- C-reachable: states that are accessible from HAR via 9 coprime steps
- G-trapped: states that pass through a gate element before step 9

The fraction G-trapped depends on |G| and the geometry of G in {1,...,k}.

**For small k (k=9), G elements are relatively dense in {1,...,9}:**

| b | G ∩ {1,...,9} | density | Trap probability |
|---|--------------|---------|-----------------|
| b=6, G={3,4} | {3,4,6,8,9} overlap varies | low for k=9 |
| b=10, G={2,4,5,6,8} | {2,4,5,6,8} | 5/9 = 0.556 | high |
| b=35, G={5,7,10,14,...} | {5,7} | 2/9 = 0.222 | moderate |

**Key structural insight:** The gate rate at k=9 is determined by how many elements
of G lie in {1,...,9}. If G ∩ {1,...,9} is large, the MCMC is likely to hit a gate
element before reaching a high-score state.

The empirical rates:
```
|G|=1 → 96.4%: G has 1 element in {1..k}, rarely encountered
|G|=3 → 44.0%: G has ~3 elements in {1..k}, frequent obstruction
|G|=4 →  4.6%: G has ~4 elements, very frequent obstruction
|G|=5 →  0.1%: G nearly fills {1..k}, almost always trapped
```

---

## The CRT Derivation Path (C-tier conjecture)

**Claim Q6 (C-tier):** The gate rate at step k for semiprime b=p·q with gate set
G = {multiples of p or q in {1,...,b-1}} is approximately:

```
rate(b, k) ≈ P(MCMC avoids G ∩ {1,...,k} for k steps)
           ≈ (1 - |G ∩ {1,...,k}| / k)^{αk}
```

for some constant α determined by the HAR-bias (α ≈ 0.6 for 40% HAR weight).

The key quantity is |G ∩ {1,...,k}|, which equals:

```
|G ∩ {1,...,k}| = ⌊k/p⌋ + ⌊k/q⌋ - ⌊k/b⌋
```

(inclusion-exclusion: multiples of p, plus multiples of q, minus multiples of pq=b)

At k=9, for b=p·q with p < q:
```
|G ∩ {1,...,9}| = ⌊9/p⌋ + ⌊9/q⌋ - ⌊9/b⌋
```

For b=35 (p=5,q=7): ⌊9/5⌋+⌊9/7⌋-⌊9/35⌋ = 1+1-0 = 2
For b=21 (p=3,q=7): ⌊9/3⌋+⌊9/7⌋-⌊9/21⌋ = 3+1-0 = 4
For b=15 (p=3,q=5): ⌊9/3⌋+⌊9/5⌋-⌊9/15⌋ = 3+1-0 = 4
For b=10 (p=2,q=5): ⌊9/2⌋+⌊9/5⌋-⌊9/10⌋ = 4+1-0 = 5

**Checking against |G| ordering:**

| b | |G|=p+q-2 | |G∩{1..9}| (inclusion-excl) |
|---|---------|--------------------------|
| 10 | 5 | 5 |
| 21 | 8 | 4 |
| 15 | 6 | 4 |
| 35 | 10 | 2 |

**|G| and |G∩{1..9}| are not proportional.** The global gate count |G| is not
the right predictor — the local count |G∩{1..k}| is.

But empirically, |G| (not |G∩{1..9}|) predicts the rate. This suggests the MCMC
rate depends on something that correlates with |G| but is not simply |G∩{1..9}|.

---

## Current Status and What Luther's Derivation Would Need

The algebraic path is not closed. The CRT decomposition gives:

1. The exact value of |G ∩ {1,...,k}| via inclusion-exclusion (D-tier, trivial)
2. The density f_C = φ(b)/(b-1) (D-tier, trivial)
3. The gate set structure as two arithmetic progressions (D-tier)

What is NOT derived:
- The MCMC hill-climbing dynamics on this structure
- Why |G| (global) correlates better than |G∩{1..9}| (local)
- The exact constants in the escape probability formula

**For Luther Question 1 to be answered:** The derivation must go through the
MCMC transition matrix on the k-step state space, whose spectral gap determines
the mixing rate and success probability. This matrix has entries determined by
the CRT structure but is not yet computed.

**Proposed path:** Build the 9×9 MCMC transition matrix for the first semiprime
at each |G| class, compute the probability of reaching a C-state in ≤100 steps.
Compare across b values with same |G|. If the probability is |G|-class invariant,
confirm the zero-spread universality. If the matrix entries have a CRT pattern,
the algebraic derivation is within reach.

---

## Status Table

| Claim | Tier |
|-------|------|
| |G∩{1..k}| formula (inclusion-exclusion) | D |
| f_C = φ(b)/(b-1) | D |
| Gate rate is NOT f_C alone | D (empirical contradiction) |
| Gate rate correlates with |G| (not |G∩{1..k}|) | D (empirical) |
| MCMC transition matrix structure from CRT | C (not yet computed) |
| Algebraic derivation of exact rates | B-conjecture (Luther Q1 target) |

---

*Filed: 2026-04-01. Sprint: operator algebra series, Q6 addressing Luther Question 1.*
