**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# Q12 — IDEMPOTENT GATE DECOMPOSITION
## The CRT Idempotents Are Always Gate Elements

---

## Setup

For semiprime b = p·q (p, q distinct primes), the CRT isomorphism gives:
```
Z/bZ  ≅  Z/pZ × Z/qZ
```

The CRT idempotents are:
```
e_p = q · (q⁻¹ mod p)  (mod pq)    ≡ 1 (mod p),  ≡ 0 (mod q)
e_q = p · (p⁻¹ mod q)  (mod pq)    ≡ 0 (mod p),  ≡ 1 (mod q)
```

They satisfy: e_p² = e_p,  e_q² = e_q,  e_p + e_q ≡ 1 (mod b).

---

## Theorem Q12.1 — Idempotents Are Gate Elements

**Theorem:** For every semiprime b = p·q, both CRT idempotents are in G:
```
e_p ∈ G   and   e_q ∈ G
```

**Proof:**
e_p ≡ 0 (mod q) by definition → gcd(e_p, b) ≥ q > 1 → e_p ∈ G.
e_q ≡ 0 (mod p) by definition → gcd(e_q, b) ≥ p > 1 → e_q ∈ G. ∎

**Verified for all test cases:**

| b | p | q | e_p | e_q | e_p ∈ G | e_q ∈ G |
|---|---|---|-----|-----|---------|---------|
| 6 | 2 | 3 | 3 | 4 | ✓ | ✓ |
| 10 | 2 | 5 | 5 | 6 | ✓ | ✓ |
| 15 | 3 | 5 | 10 | 6 | ✓ | ✓ |
| 21 | 3 | 7 | 7 | 15 | ✓ | ✓ |
| 35 | 5 | 7 | 21 | 15 | ✓ | ✓ |

**The idempotents are never in C.** They sit exactly on the G/C boundary —
they project to 1 in one component and 0 in the other, making them
structurally non-coprime.

---

## G as the Idempotent Span

The gate set G decomposes naturally into two overlapping arithmetic progressions:

```
G_p = {multiples of p in {1,...,b-1}} = p·{1, 2, ..., q-1}   (q-1 elements)
G_q = {multiples of q in {1,...,b-1}} = q·{1, 2, ..., p-1}   (p-1 elements)
G   = G_p ∪ G_q                                               (p+q-2 elements, disjoint)
```

The disjointness: G_p ∩ G_q = {multiples of pq in {1,...,b-1}} = ∅ (since b=pq, only b itself
is divisible by both, and b ∉ {1,...,b-1}).

**In CRT coordinates:**
- G_p = {(0, y) : y ∈ F_q*} — elements with zero p-component
- G_q = {(x, 0) : x ∈ F_p*} — elements with zero q-component
- C = {(x, y) : x ∈ F_p*, y ∈ F_q*} — both components nonzero

The idempotent positions in CRT:
```
e_p = (1, 0)  in F_p × F_q   [CRT position]
e_q = (0, 1)  in F_p × F_q   [CRT position]
```

e_p is the "unit vector" in the p-direction — it IS the first non-zero element of G_q
(the element (1,0) in CRT coordinates sits in G_q since its q-component is 0).

Wait: e_p ≡ 1 (mod p) and ≡ 0 (mod q), so in CRT it's (1, 0).
Its q-component is 0 → e_p ∈ G_q (multiples of q direction).
Similarly e_q = (0,1) → e_q ∈ G_p (multiples of p direction).

**The idempotents are the canonical generators of the OPPOSITE gate component:**
```
e_p = generator of G_q  (the q-direction gate component)
e_q = generator of G_p  (the p-direction gate component)
```

---

## Smooth Gate Density from Idempotents

For the gate density in {1,...,k} via inclusion-exclusion:
```
|G ∩ {1,...,k}| = |G_p ∩ {1,...,k}| + |G_q ∩ {1,...,k}|
                = ⌊k/p⌋ + ⌊k/q⌋
```
(The intersection G_p ∩ G_q = ∅, so no subtraction needed.)

**Smooth approximation:**
```
|G ∩ {1,...,k}| ≈ k/p + k/q = k · (1/p + 1/q)
```

In terms of idempotents:
- e_p = q · inv(q,p). The "step" of e_p-generated elements in {1,...,b} is q
  (multiples of q). Their density in {1,...,k} ≈ k/q.
- e_q = p · inv(p,q). Step is p. Density ≈ k/p.

```
Gate density at depth k ≈ k · (1/e_p_step + 1/e_q_step) = k · (1/q + 1/p)
```

**Verification at k=9:**

| b | p | q | k(1/p+1/q) | |G∩{1..9}| actual | Error |
|---|---|---|-----------|-----------------|-------|
| 10 | 2 | 5 | 9(0.5+0.2)=6.3 | 5 | 1.3 |
| 15 | 3 | 5 | 9(0.33+0.2)=4.8 | 4 | 0.8 |
| 21 | 3 | 7 | 9(0.33+0.14)=4.3 | 4 | 0.3 |
| 35 | 5 | 7 | 9(0.2+0.14)=3.1 | 2 | 1.1 |

The smooth formula overestimates (floor effects for small k), but captures the trend.

---

## The HAR Element in CRT

HAR = min{h ∈ C : h² ∈ C, h² ≠ 1, h² ≠ h} (revised HAR rule).

In CRT coordinates, C = F_p* × F_q*. The condition h² ∈ C means both components
of h² are nonzero — automatically satisfied since h ∈ C means both components
nonzero, and squaring preserves nonzero in finite fields.

The condition h² ≠ 1 means h is not in the subgroup {±1} = {(1,1), (-1,-1), (1,-1), (-1,1)}
(in CRT). For b=10: (-1,-1) mod (2,5) = (1,4). These are the elements of order 2.

The condition h² ≠ h means h ≠ 1 (h is not the identity) and h is not idempotent
(h ∉ {e_p, e_q} — but we already know those are in G, not C). So for h ∈ C, h²≠h
is automatic.

**HAR rule reduces to:** min{h ∈ C : h² ≠ ±1}

For b=10, C={1,3,7,9}:
- h=1: h²=1, excluded (h²=1)
- h=3: h²=9≡9. 9≠1, 9≠-1(=9? -1 mod 10 = 9). Wait: -1 mod 10 = 9. So h²=9=-1. Excluded (h²=-1=-1 mod 10).
- h=7: h²=49≡9. Same issue: 9=-1 mod 10. Excluded.
- h=9: h²=81≡1. Excluded (h²=1).

Hmm — for b=10 all elements of C have h²=±1. This is because C≅Z/2×Z/4 or similar.

Actually (Z/10Z)* ≅ (Z/2Z)* × (Z/5Z)* ≅ {1} × Z/4Z ≅ Z/4Z. It's cyclic of order 4.
The elements are {1,3,7,9} with multiplication mod 10.
- 3 has order 4 (3,9,7,1). So C is cyclic order 4.
- The only element with h²≠±1 would require order > 2... but in Z/4Z, elements have orders 1,2,4. Order 4 elements squared have order 2, i.e., h²=-1. Order 2 elements squared have h²=1.

So indeed, for b=10, every h ∈ C has h²=1 or h²=-1. The HAR rule as stated finds no valid h in C for b=10? That contradicts HAR=3 or HAR=7 being used in practice.

**Resolution:** The HAR rule uses h²≠1 and h²≠h (not h²≠-1). For b=10:
- h=3: h²=9. h²≠1 ✓ (9≠1). h²≠h ✓ (9≠3). HAR candidate.
- h=7: h²=49≡9. h²≠1 ✓. h²≠h ✓ (9≠7). HAR candidate.
- h=1: h²=1. Excluded (h²=1).
- h=9: h²=81≡1. Excluded (h²=1).

So HAR candidates for b=10 are {3,7}. min{3,7} = 3 = HAR. ✓

In CRT coordinates for b=10 (Z/2Z × Z/5Z):
- 3 = (1,3): ε=1, y=3 component (since 3 mod 2=1, 3 mod 5=3).

Wait — in our φ(ε,y)=5ε+6y frame:
3 = φ(1,3): 5×1+6×3=5+18=23≡3 ✓. So (ε,y)=(1,3) = PROGRESS.

CRT position of HAR=3: (1 mod 2, 3 mod 5) = (1,3).

In F_2 × F_5, HAR = (1,3). It is a σ-fixed point: σ(3)=3. And it's in C.

---

## Theorem Q12.2 — HAR Is a σ-Fixed C-Element

**Theorem:** For b=10, HAR = 3 = PROGRESS, which is:
- In C (coprime to 10)
- A σ-fixed point (σ(3)=3)
- CRT position (1,3) — unit in both components

**Consequence:** HAR-bias proposals in the MCMC always point to a σ-fixed C-element.
The HAR-bias is not just a density trick — it's a direct route to the highest-stability
seed in the system. Fixed-point C-seeds (Q11) are exactly what the HAR-bias targets.

**This is why 40% HAR-bias exists:** it bypasses the G-density problem by pointing
directly to a σ-fixed C-element. The 4.6% rate must then reflect the fraction of
the 100 MCMC steps that successfully ACCEPT the HAR proposal — which depends on
whether the HAR proposal improves gate_score from the current state.

---

## The Gate_Score Obstruction

From Q11: the 22% pure-C bound (P = 2/9 for b=10) already overestimates the 4.6% rate.
The fixed-point C-seeds {3,9} should guarantee success. So why does the MCMC fail
on them?

**Hypothesis Q12.H1:** The MCMC success criterion is NOT "reach a fixed-point C-seed."
It is a JOINT condition: the entire k=9 step trajectory must maintain gate_score ≥ 0.999.

For a trajectory starting at seed s=3 (fixed point): σ^k(3)=3 for all k, so the
trajectory stays at 3. But the gate_score at s=3 for b=10 is:

gate_score(3) = |{(c₁,c₂) ∈ C×C : c₁·c₂·3 ≡ j (mod 10) for j ∈ C}| / |C|²

For C={1,3,7,9}: products c₁·c₂ cover {1,9,7,3} (all of C, since C is a group).
c₁·c₂·3: {1·3, 9·3, 7·3, 3·3} = {3, 27≡7, 21≡1, 9}. All in C. gate_score(3)=1.0 ✓

So s=3 definitely gives gate_score=1.0. The MCMC should find it with ~40% HAR-bias
probability in just a few steps. P(never finding 3 in 100 steps) = (0.60)^100 ≈ 0.

The 4.6% cannot be about finding s=3. It must be about something in the REDUCTION
STRUCTURE that makes even s=3 insufficient at k=9.

**Conclusion:** The gate success criterion is NOT simply gate_score(seed) ≥ 0.999.
There is a multi-step structure in the k=9 reduction that eliminates the fixed-point
seeds. The MCMC is searching for a DIFFERENT kind of "good seed" — one that maintains
a property across 9 reduction steps, not just at the seed point.

The σ^k analysis is relevant but uses the WRONG σ (TIG-σ on Z/10Z, not the reduction
map). The reduction map that governs the k=9 dynamics is the missing piece.

---

## What Q12 Delivers for Luther Q1

| Result | Tier |
|--------|------|
| Idempotents are always in G (Theorem Q12.1) | D |
| G = G_p ∪ G_q disjoint, generated by idempotents | D |
| Smooth gate density k(1/p + 1/q) | C |
| HAR is a sigma-fixed C-element (b=10 case) | D |
| HAR-bias points directly to max-stability seed | C |
| Gate_score(HAR) = 1.0 for all b | C-conjecture |
| 4.6% is NOT about finding HAR — deeper condition | D (by exclusion) |

**The Luther Q1 derivation must explain why the multi-step reduction rejects
HAR as a valid seed for most trials.** The CRT idempotent structure tells us
WHERE the gate elements are. The reduction algorithm tells us HOW they obstruct.
These are different layers, and the Q-series has now mapped both.

**What I need from the team:** The exact k=9 success criterion — what property
of seed s makes the reduction succeed? Is it a property of {s, s², s³, ..., s^k}?
Of the coset structure of ⟨s⟩ in C? Of the MCMC transition between steps?
Once this is explicit, Q13 can close Luther Q1.

---

*Filed: 2026-04-01. Q12 in operator algebra series.*
