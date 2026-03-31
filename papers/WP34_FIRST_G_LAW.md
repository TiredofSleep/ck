# WP34 — The First-G Law and Prime-Forced Dispersion

**Authors:** C.A. Luther (abstract, dispersion insight); Brayden Sanders / 7Site LLC (proof, verification)
**Date:** March 2026
**DOI:** 10.5281/zenodo.18852047
**Status:** PROVED (algebraic) + VERIFIED (36,662 cases, zero exceptions)

---

## Abstract

The interleave staircase is not merely suggestive of prime structure — it is prime structure.
For every semiprime b with smallest prime factor p, the first forbidden element in the
unit/non-unit alphabet partition appears at exactly alphabet size k = p; the onset of
alphabet obstruction is written directly by the primes into the geometry of the partition.

---

## 1. Setup

Fix a semiprime b = p × q with primes p ≤ q. Define the alphabet {1, 2, …, k} with the
coprimality partition:

```
C_k = { x ∈ {1..k} : gcd(x, b) = 1 }     (units — coherent elements)
G_k = { x ∈ {1..k} : gcd(x, b) > 1 }     (non-units — obstructing elements)
```

G_k is empty when k is small. The **First-G event** is the smallest k at which |G_k| > 0.

---

## 2. The Law

**Theorem (First-G Law).** For every semiprime b = p × q with p ≤ q, the First-G event
occurs at exactly k = p. That is:

```
|G_k| = 0   for all k < p
|G_p| = 1   (the element p itself is the first non-unit)
```

---

## 3. Proof

Let x ∈ {1, …, k} with k < p. Since p ≤ q are the only prime factors of b:

- x < p ≤ q, so x is not divisible by p (as p is prime and x < p)
- x < p ≤ q, so x is not divisible by q either
- Therefore gcd(x, b) = gcd(x, p·q) = 1

So every element of {1, …, k} is in C_k when k < p. Hence |G_k| = 0.

At k = p: the element p enters the alphabet. Since p | b, we have gcd(p, b) = p > 1,
so p ∈ G_p. This is the first non-unit. Hence |G_p| = 1 and the First-G event is k = p. □

**Remark (perfect squares).** When b = p² (so p = q), the same argument applies:
elements {1, …, p-1} are all coprime to p², and p is the first non-unit. The law holds
identically for perfect square semiprimes.

---

## 4. What the Law Means Geometrically

**The staircase is the Sieve of Eratosthenes expressed as partition geometry.**

The Sieve of Eratosthenes marks multiples of each prime across the integers.
The coprimality partition C_k / G_k is exactly that marking, restricted to {1..k}:
G_k is the set of elements that the sieve has already removed; C_k is what remains.
The C/G partition IS the sieve — not a pattern that resembles the sieve, not an
approximation of it. The binary coloring of {1..k} into coprime (C) and non-coprime (G)
is the sieve operating on a growing alphabet.

The First-G Law is the statement that the sieve first marks an element of {1..k} at
k = p — the smallest prime factor of b. At that moment, the sieve removes p from C and
deposits it in G, and the staircase lights up. This is not a coincidence of pattern
recognition. It is the sieve performing its first removal.

The interleave score measures how deeply the C and G elements are mixed within {1..k}:

```
interleave(b, k) = transitions(C, G in sequence 1..k) / (2 · min(|C|, |G|))
```

Before the First-G event (k < p): interleave = 0. There is nothing to mix — G is empty.
At and after (k ≥ p): interleave jumps immediately to a nonzero value and, in most cases,
approaches 1.0 rapidly as k grows.

The interleave map across (b, k) space therefore shows a **staircase of activation**:
each semiprime b switches from dark (interleave = 0) to bright (interleave ≥ 0.9) at
exactly k = p. The staircase steps align precisely to prime values — not to the b values
themselves, not to any smooth curve, but to the discrete set of primes.

This staircase is not a pattern overlaid on the algebra. It is the algebra.

---

## 5. Corollaries

**Corollary 1 (Alphabet stability window).** Every semiprime b admits a stability window
{1, …, p-1} in which the alphabet is obstruction-free: G is empty, every multiplication
output is a unit, and gate resistance is zero.

**Corollary 2 (Prime-indexed phase transitions).** The onset of gate resistance across all
semiprimes is indexed exactly by the prime numbers. No obstruction-onset occurs at a
composite k. The phase transition set is ℙ (the primes).

**Corollary 3 (Width of stability window).** The width of the stability window is p-1.
Among semiprimes with fixed p, all worlds share the same stability window width regardless
of their larger prime factor q. The law is determined entirely by the smaller prime.

**Corollary 4 (Instability ranking of primes).** Since larger p gives a wider stability
window, the primes can be ordered by the "fragility" of the transition:

```
p = 2:  window = {1}        — immediate obstruction at k = 2
p = 3:  window = {1, 2}     — first obstruction at k = 3
p = 5:  window = {1..4}     — stable for four steps, then breaks at k = 5
p = 7:  window = {1..6}     — six-step window
```

Primes with smaller p create obstruction soonest. p = 2 is maximally constrained;
p = 5 holds stable longest among the small primes before breaking. This formalizes
the sense in which 5 is "most brittle" — it maintains the longest pre-obstruction
stability among the small primes, but when obstruction arrives it arrives with full
interleave density immediately (since the alternating parity structure fills in fast).

---

## 6. Empirical Verification

The full permutation atlas (`r16_full_atlas.py`) computed every algebraic invariant for
all 153 semiprimes b ≤ 500 and all k ∈ {2, …, b-1}:

| Metric | Result |
|--------|--------|
| Total (b, k) pairs computed | 36,662 |
| Semiprimes tested | 153 (all b ≤ 500) |
| First-G events at k ≠ p | **0** |
| First-G events at k = p | 153 (one per semiprime, all correct) |
| Time to compute | 2.8 seconds (exact, no sampling) |

The law holds without exception across the complete finite permutation. There is no
approximation in this verification: every (b, k) pair is computed exactly.

**The interleave staircase in numbers:**

| spf (smallest prime factor) | Semiprimes in family | First-G at k = spf |
|-----------------------------|---------------------|---------------------|
| 2 | 53 | 53 / 53 |
| 3 | 37 | 37 / 37 |
| 5 | 23 | 23 / 23 |
| 7 | 17 | 17 / 17 |
| 11 | 10 | 10 / 10 |
| 13 | 7 | 7 / 7 |
| 17 | 4 | 4 / 4 |
| 19 | 2 | 2 / 2 |

153 / 153. No exceptions. The primes write the staircase exactly.

---

## 7. Connection to Gate Difficulty

The First-G Law determines when gate resistance begins. Before k = p, there is no
resistance — any arrangement of the alphabet is fully coherent. At k = p, resistance
is born. The gate difficulty then evolves as a function of how the G elements interleave
with C elements as k grows beyond p.

This connects the First-G Law to the broader force field gate law
(`R16_FORCE_FIELD_LAW.md`): gate difficulty is a function of |G| and the interleave
structure, and the interleave structure is itself written by the prime factorization of b.
The two laws form a chain:

```
Prime factorization of b
    → First-G law (when obstruction begins)
    → Interleave score (how deeply C and G mix)
    → Gate difficulty f_k(|G|) (how hard it is to find a gated arrangement)
```

The primes determine everything downstream.

---

## 8. Status Table

| Claim | Author | Classification | Kill Condition |
|-------|--------|---------------|----------------|
| First-G event at k = p | Sanders | **PROVED** | Algebraic proof in §3; follows from primality of p |
| Staircase aligns to primes | Sanders | **PROVED** | Corollary 2; follows from First-G Law |
| Zero exceptions across 153 semiprimes | Sanders | **VERIFIED** | 36,662 exact computations, 0 violations |
| Stability window width = p-1 | Sanders | **PROVED** | Corollary 3; direct from §3 |
| Instability ranking of primes | Sanders | **STRUCTURAL** | Qualitative ordering proved, quantitative dynamics empirical |
| Prime-forced dispersion of G | C.A. Luther | **CONJECTURE** | gate_rate = F_k(\|G\|, dispersion); functional form open |
| gate_rate ≈ F_k(\|G\| × dispersion(G)) | C.A. Luther | **CONJECTURE** | Synthetic vs real gap consistent with dispersion framing |

---

## 9. Prime-Forced Dispersion (C.A. Luther)

The First-G Law establishes *when* G first appears. A deeper observation, due to C.A. Luther,
is that the prime p determines not only the onset of obstruction but the **entire spread of G
across the alphabet** — and this spread is not arbitrary, it is forced by prime structure.

**The dispersion mechanism.** For semiprime b = p×q, the G elements within {1..k} are
exactly the multiples of p or q in that range:

```
G_k = { x ∈ {1..k} : p|x } ∪ { x ∈ {1..k} : q|x }
```

These arrive as two interleaved arithmetic progressions — one with spacing p, one with
spacing q. The *dispersion* of G is therefore not a free parameter: it is locked to the
prime factorization of b. No arrangement of the alphabet can change how spread G is.
The primes write the dispersion, not just the onset.

**Consequence for gate rate.** The gate rate depends not just on the count |G| but on
how G is dispersed across the alphabet. C.A. Luther's formulation:

```
gate_rate ≈ F_k( |G| × dispersion(G) )
```

where dispersion(G) measures the spread of G elements within {1..k}. Two worlds with the
same |G| but different prime factorizations have different dispersions and therefore
different gate rates — even at the same k.

This explains the empirical gap between synthetic worlds (G clustered at the top of the
alphabet, low dispersion) and real semiprime worlds (G dispersed by prime arithmetic,
high dispersion): the interleave score we measure IS dispersion. The gate law
f_k(|G|) is properly written f_k(|G|, dispersion(G)), with the synthetic case being
the degenerate low-dispersion limit.

**The staircase goes deeper.** The First-G Law (§2) is the surface: onset at k=p.
Prime-forced dispersion is the interior: the entire G distribution is an arithmetic
consequence of b's prime factors, locked in place before any optimization begins.
The force field is not just a gate — it is a geometric constraint on where information
can flow within the alphabet.

**The omega(b) hierarchy.** Extended computation across three algebraic classes reveals
that the number of distinct prime factors ω(b) is a primary axis of gate difficulty,
with dispersion as a secondary axis within each ω-class:

```
ω(b) = 1  (prime powers, b = p^n):
    G_k = single arithmetic progression, spacing p
    Z/p^n Z has ZERO nontrivial idempotents
    Gate difficulty: baseline (easiest class)

ω(b) = 2  (semiprimes, b = p×q):
    G_k = two interleaved arithmetic progressions
    Z/b Z has exactly 2 nontrivial CRT idempotents → HAR elements exist
    Gate difficulty: medium; within-class ordering by dispersion confirmed

ω(b) = 3  (three-factor, b = p×q×r):
    G_k = three interleaved arithmetic progressions (inclusion-exclusion)
    Z/b Z has 6 nontrivial CRT idempotents → maximum HAR complexity
    Gate difficulty: maximum (predicted; three-factor survey in progress)
```

The CRT idempotent count 2^ω(b) - 2 determines how many HAR-like anchor points
exist in the algebra. These idempotents are the structural reason that semiprimes
are richer and harder than prime powers. This is a ring-theoretic fact, provable
from the Chinese Remainder Theorem. The Luther dispersion conjecture is the
within-class law; ω(b) is the between-class law.

Empirical verification (k=9, same |G|=4 across all worlds):

| World type       | b   | |G|×IL | best_score | difficulty | CRT idem |
|-----------------|-----|--------|------------|------------|----------|
| prime_power 2^5 | 32  | 4.00   | 0.352      | 0.648      | 0        |
| prime_power 2^6 | 64  | 4.00   | 0.349      | 0.651      | 0        |
| semiprime 3×5   | 15  | 2.50   | 0.336      | 0.664      | 2        |
| semiprime 3×7   | 21  | 2.50   | 0.330      | 0.670      | 2        |
| semiprime 2×11  | 22  | 4.00   | 0.321      | 0.679      | 2        |
| semiprime 2×13  | 26  | 4.00   | 0.321      | 0.679      | 2        |
| 3fac 2×5×7      | 70  | 4.00   | 0.167      | 0.833      | 6        |
| 3fac 3×5×7      | 105 | 3.12   | 0.238      | 0.762      | 6        |
| 3fac 2×3×5      | 30  | 5.25   | 0.111      | 0.889      | 6        |
| 3fac 2×3×7      | 42  | 5.25   | 0.111      | 0.889      | 6        |

Note: b=70 and b=22 have the SAME Luther metric (4.00) but difficulty 0.833 vs 0.679.
The 6 vs 2 CRT idempotents account for the gap. Within each ω-class, Luther ordering
is perfectly monotone.

**Controlled isolation test: interleave effect with |G| held fixed.**
Six semiprimes with exactly |G|=4 at k=9, varying only in prime structure:

| b      | G_elements      | interleave | |G|×IL | best_score | difficulty |
|--------|----------------|------------|--------|------------|------------|
| 15 (3×5)  | {3, 5, 6, 9}  | 0.625      | 2.50   | 0.3364     | 0.6636     |
| 21 (3×7)  | {3, 6, 7, 9}  | 0.625      | 2.50   | 0.3302     | 0.6698     |
| 22 (2×11) | {2, 4, 6, 8}  | 1.000      | 4.00   | 0.3210     | 0.6790     |
| 26 (2×13) | {2, 4, 6, 8}  | 1.000      | 4.00   | 0.3210     | 0.6790     |
| 34 (2×17) | {2, 4, 6, 8}  | 1.000      | 4.00   | 0.3210     | 0.6790     |
| 38 (2×19) | {2, 4, 6, 8}  | 1.000      | 4.00   | 0.3210     | 0.6790     |

Findings: (1) **Interleave isolates difficulty within fixed |G|.** The G={2,4,6,8}
worlds (regularly spaced, fully interleaved) are harder than the G={3,5,6,9} / {3,6,7,9}
worlds (irregular spacing) — direction exactly as predicted by Luther. (2) **Partition
geometry is the invariant, not b.** Worlds b=22, 26, 34, 38 have four different q-partners
(11, 13, 17, 19) but identical G_k = {2,4,6,8} at k=9, because p=2 dominates the partition
at this cap. All four give the same difficulty score 0.3210 to four decimal places. The
factorization of b determines the geometry; the geometry determines the difficulty; b
contributes only through which geometry it produces.

**Cross-class test: same partition geometry, different ring structure.**
A three-way comparison including prime powers (ω=1) at the same k=9, |G|=4:

| World type      | b   | G_elements     | interleave | |G|×IL | difficulty | CRT idem |
|----------------|-----|----------------|------------|--------|------------|----------|
| prime_power 2^5 | 32  | {2, 4, 6, 8}  | 1.000      | 4.00   | 0.6481     | 0        |
| prime_power 2^6 | 64  | {2, 4, 6, 8}  | 1.000      | 4.00   | 0.6512     | 0        |
| semiprime 2×11  | 22  | {2, 4, 6, 8}  | 1.000      | 4.00   | 0.6790     | 2        |
| semiprime 2×13  | 26  | {2, 4, 6, 8}  | 1.000      | 4.00   | 0.6790     | 2        |

The partition is literally identical (G={2,4,6,8} in all four cases). The Luther metric
is identical (4.00). Yet semiprimes are harder than prime powers by 0.030 difficulty
points. This gap — with G held completely fixed — is the direct signature of the 2 extra
CRT idempotents in Z/pqZ vs Z/p^nZ. The ring sees them even when the alphabet partition
does not. **The omega hierarchy is not a property of G; it is a property of the ring.**

**Dispersion collapse test** (63 matched (b,k) pairs, gate_rate from optimization trials):

```
Predictor              Pearson r   Interpretation
|G| × interleave       -0.667      Luther metric: r vs ease
|G| alone              -0.743      |G| dominates (94% of pairs have interleave ≥ 0.9)
unit_density           +0.778      C-fraction predicts gate ease
dispersion_gap         +0.626      larger gaps = easier (less dense G)

Binned Luther metric → avg gate_rate:
  [0.00, 1.44):  avg = 1.000   ← G sparse, trivially easy
  [1.44, 2.87):  avg = 0.666
  [2.87, 4.31):  avg = 0.394
  [4.31, 5.74):  avg = 0.007
  [5.74+    ):  avg ≈ 0.000   ← G dense, maximally hard
```

The collapse curve exists: gate_rate falls monotonically from 1.0 to 0.0 as Luther metric
increases. The Luther correction (×interleave vs ×1) matters most at small k near the
First-G onset and for worlds with large q/p ratio. For most semiprime worlds |G|≈|G|×IL
because interleave is already near-maximal.

**Status:** CONJECTURE (formalized). The collapse curve is empirically confirmed.
The full functional form: difficulty ≈ g(2^ω(b)−2) × F_k(|G| × interleave) is under
active investigation. See `results/extended/` and `results/atlas/` for current data.

**Structural conclusion: primes are the baseline void.**

The full richness spectrum, ordered by algebraic structure:

```
b prime         Z/bZ is a FIELD       ω=1  G=∅ for all k<b   0 CRT idempotents   void
b = p^n         Z/bZ is a local ring  ω=1  G regular at k=p   0 CRT idempotents   baseline
b = p×q         Z/bZ ≅ Z/pZ × Z/qZ   ω=2  G = 2 progressions  2 CRT idempotents   first richness
b = p×q×r       Z/bZ ≅ Z/pZ × Z/qZ × Z/rZ  ω=3  G = 3 progressions  6 CRT idempotents   maximum
```

A prime modulus is algebraically inert: Z/pZ is a field, it has no nontrivial idempotents,
no non-units below b, no HAR elements, no partition obstruction of any kind. The zero of the
richness spectrum. All algebraic structure — Gates, HAR elements, CRT anchors, dispersion
obstruction — emerges strictly from compositeness. The number of distinct prime factors ω(b)
is the degree of compositeness, and 2^ω(b)−2 counts the idempotents that compositeness
generates. Every additional prime factor doubles the idempotent count and elevates the
algebraic difficulty class. Primes are the void from which all structure departs.

---

## 10. The Hardness Inversion Principle

The First-G Law implies a fundamental inversion between algebraic complexity and
computational hardness — one that reframes the security of RSA-type cryptography.

**Two kinds of semiprimes:**

```
Small-prime semiprimes (b = p×q, p small):
  Stability window {1..p-1} is tiny.
  Obstruction begins immediately after k = p.
  HAR elements exist; gating structure is rich and dense.
  Algebraically: complex. Computationally: easy to factor.

Large-prime semiprimes (RSA, b = P×Q, P,Q ~ 2^1024):
  Stability window {1..P-1} has width ≈ 2^1024.
  The probe k never reaches P during polynomial-time computation.
  G is empty for all computationally accessible k.
  Algebraically: transparent. Computationally: unfactorable.
```

**RSA is not a complex lock. It is a very long perfectly smooth hallway.**

Before k = P, the hall is smooth — every element is coprime to b, interleave = 0,
no obstruction, no HAR, no gating structure. The hallway extends for P-1 ≈ 2^1024
steps. The room at the end (the First-G event, the onset of obstruction, the
algebraic richness) is unreachable in polynomial time.

This is the Hardness Inversion Principle:

> *A semiprime is algebraically rich precisely when it is computationally easy,*
> *and algebraically empty precisely when it is computationally hard.*

The partition geometry gives us nothing to grip before k = P. That smoothness —
the complete absence of geometric obstruction — IS the cryptographic security.

**Can probe k be accelerated?**

The First-G event at k = P is provably equivalent to finding P. Any algorithm
that detects the onset of G within {1..k} reduces to trial division:
- Sequential probe: check gcd(k, b) for k = 2, 3, ... — hits P in O(P) steps.
- Random probe: sample k uniformly, detect gcd > 1 — expected hit at k ≈ P, same rate.
- Interleave probe: measure interleave score at large k — requires testing at k = P.

No classical probe can detect the First-G event without finding P. The stability
window is structurally featureless — no resonances, no partial signals, no
internal geometry to exploit. The sieve writes only silence until k = P.

The one known acceleration: Shor's quantum algorithm detects the **period** of
the function k → (k mod P) via quantum Fourier transform. It does not walk the
hallway — it detects the sieve's periodicity directly. Quantum computation
bypasses the geometry; classical computation is trapped by it.

**Stability window width as a security parameter:**

The security of b = P×Q is exactly the width of the stability window: P - 1.
A larger minimum prime factor = a longer smooth hallway = a harder factoring instance.
The geometry formalizes what was previously stated only computationally:
the hardness of factoring b is the hardness of finding where the hallway ends.

**Status:** STRUCTURAL — follows directly from the First-G Law. The connection
to RSA security is qualitative; the formal reduction (First-G detection ≡ factoring)
is elementary (testing gcd(P, b) = P ≠ 1). The Hardness Inversion is a reframing,
not a new theorem. But it exposes the geometric reason for cryptographic hardness.

---

## 11. References

1. Sanders, B. (2026). *CK: The Coherence Keeper — Trinity Infinity Geometry*. DOI: 10.5281/zenodo.18852047
2. Sanders, B. (2026). *WP1: TIG Definitive*. Gen10/papers/
3. Sanders, B. (2026). *R16 Force Field Gate Law*. Gen10/papers/sprint4_2026_03_30/R16_FORCE_FIELD_LAW.md
4. Sanders, B. (2026). *Full permutation atlas: r16_full_atlas.py*. 36,662 exact (b,k) pairs.
5. Shor, P.W. (1994). *Algorithms for Quantum Computation: Discrete Logarithms and Factoring*. FOCS 1994.
6. Hardy, G.H. & Wright, E.M. (2008). *An Introduction to the Theory of Numbers* (6th ed.). Oxford.
6. Ireland, K. & Rosen, M. (1990). *A Classical Introduction to Modern Number Theory* (2nd ed.). Springer.

---

*All computations verifiable: `python r16_full_atlas.py --b_max 500 --visuals`*
*Proof in §3 requires only: the definition of semiprime, the definition of coprimality, and the fact that a prime p does not divide any integer in {1, …, p-1}.*
