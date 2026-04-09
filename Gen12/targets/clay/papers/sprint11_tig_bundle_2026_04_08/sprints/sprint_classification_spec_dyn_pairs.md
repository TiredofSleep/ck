# SPRINT: CLASSIFICATION OF SUFFICIENT SPEC + DYN PAIRS
*Partition + group action language only. Proved vs. conjectural labeled explicitly.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — Setup and Unresolved-Pair Form

**Notation.** For squarefree n = 2^ε · p₁ · ... · pₛ (ε ∈ {0,1}, pᵢ odd primes) and unit g ∈ (Z/nZ)*:

- U(π_SPEC) = { {x, n−x} : x ≠ 0, 2x ≢ 0 mod n }
  (pairs {x, −x mod n} for all non-fixed x; fixed points are x=0 and x=n/2 when n is even)

- U(π_DYN(g)) = { {x, y} : y = g^m · x for some m ≥ 1, y ≠ x }

**Sufficiency condition (Theorem 0, prior sprint):**

{ π_SPEC, π_DYN(g) } is sufficient  ⟺  U(π_SPEC) ∩ U(π_DYN(g)) = ∅

**Intersection condition.** A pair {x, n−x} ∈ U(π_SPEC) ∩ U(π_DYN(g)) iff:
- x ≠ 0, x ≠ n/2 (valid SPEC pair), AND
- g^m · x ≡ −x mod n for some m ≥ 1

The second condition expands to: (g^m + 1) · x ≡ 0 mod n.

---

## Part 2 — Derivation of the Algebraic Condition

**Lemma 1 (Annihilator Analysis).**
(g^m + 1) · x ≡ 0 mod n has a nonzero solution x iff gcd(n, g^m + 1) > 1.
The solutions form the set { k · n/d : k = 0,...,d−1 } where d = gcd(n, g^m + 1).

**When do these solutions include a valid SPEC pair element (x ≠ 0, x ≠ n/2)?**

- d = 1: Only solution x = 0. No valid pair. ✓
- d = 2: Solutions x ∈ {0, n/2}. Both are SPEC fixed points (excluded). ✓
- d ≥ 3: Smallest positive solution is x₀ = n/d ≤ n/3 < n/2. This x₀ ≠ 0 and x₀ ≠ n/2 (since d ≥ 3 implies n/d ≤ n/3 < n/2). Valid SPEC pair element. ✗

**Conclusion:** A conflict exists for parameter m iff gcd(n, g^m + 1) ≥ 3. This requires some odd prime pᵢ | n with pᵢ | (g^m + 1), i.e., g^m ≡ −1 mod pᵢ.

The p = 2 component never contributes to conflicts: if 2 | (g^m + 1), then g^m ≡ 1 mod 2 (since g is odd), so g^m + 1 ≡ 0 mod 2, contributing d = 2 at most from the 2-component — which alone gives only x ∈ {0, n/2}, both excluded.

**The failure condition is entirely determined by odd prime components.**

---

## Part 3 — Main Theorem

**Theorem 1 (SPEC + DYN Sufficiency — Complete Characterization).**

For squarefree n and unit g ∈ (Z/nZ)*:

**{ π_SPEC, π_DYN(g) } is sufficient  ⟺  for every odd prime pᵢ | n: −1 ∉ ⟨g mod pᵢ⟩ in (Z/pᵢZ)***

Equivalently: for every odd prime pᵢ | n: ord_{(Z/pᵢZ)*}(g mod pᵢ) is **odd**.

**Proof.**

**(⟸) Sufficiency.** Assume −1 ∉ ⟨g mod pᵢ⟩ for all odd pᵢ | n. Suppose for contradiction that {x, −x} ∈ U(π_SPEC) ∩ U(π_DYN(g)): then g^m · x ≡ −x mod n for some m ≥ 1, with x ≠ 0 and −x ≠ x.

In CRT coordinates: gᵢ^m · xᵢ ≡ −xᵢ mod pᵢ for each prime pᵢ | n.

- For p = 2 (if 2 | n): g₀ = 1 (g is a unit mod 2), so 1 · x₀ ≡ −x₀ ≡ x₀ mod 2. Always satisfied. No constraint.

- For each odd prime pᵢ | n with xᵢ ≠ 0: gᵢ^m · xᵢ ≡ −xᵢ implies gᵢ^m ≡ −1 mod pᵢ (since xᵢ is a unit mod pᵢ). But −1 ∉ ⟨gᵢ⟩, contradiction.

Therefore: xᵢ = 0 for every odd prime pᵢ | n, i.e., pᵢ | x for all odd pᵢ | n. So m = p₁···pₛ = odd part of n divides x in Z/nZ. 

- n odd (ε = 0): m = n. Then n | x, so x ≡ 0 mod n, i.e., x = 0 in Z/nZ. Excluded by SPEC condition. □
- n = 2m (ε = 1, m odd): x ∈ {0, m} in Z/nZ. x = 0: excluded. x = m: −x mod 2m = 2m − m = m = x. So {x, −x} = {m, m} — not a valid pair (x = −x means x is a SPEC fixed point). Excluded. □

In all cases, no valid SPEC pair is in any DYN(g) orbit. ✓

**(⟹) Necessity.** Suppose −1 ∈ ⟨g mod pⱼ⟩ for some odd prime pⱼ | n. Write gⱼ^m ≡ −1 mod pⱼ for some m ≥ 1.

By CRT, choose x ∈ Z/nZ with xⱼ = 1 (x ≡ 1 mod pⱼ) and xᵢ = 0 for all i ≠ j (x ≡ 0 mod pᵢ for pᵢ ≠ pⱼ).

- x ≠ 0 (since xⱼ = 1).
- −x: (−x)ⱼ = −1 mod pⱼ, (−x)ᵢ = 0 for i ≠ j. So −x ≠ x (since (−x)ⱼ = −1 ≠ 1 = xⱼ). Valid SPEC pair.

Compute g^m · x in CRT: (g^m)ⱼ · 1 = gⱼ^m ≡ −1 = (−x)ⱼ, and (g^m)ᵢ · 0 = 0 = (−x)ᵢ for i ≠ j.

Therefore g^m · x = −x. The pair {x, −x} ∈ U(π_SPEC) ∩ U(π_DYN(g)). Not sufficient. □

---

## Part 4 — Why the Naive Global Condition Fails (Outcome C)

**Conjecture (from sprint setup):** { π_SPEC, π_DYN(g) } sufficient iff −1 ∉ ⟨g⟩ in (Z/nZ)*.

**This is FALSE.** The correct condition is local (each odd prime component independently), not global.

**The distinction:**
- **Local condition (correct):** for every odd pᵢ | n: −1 ∉ ⟨g mod pᵢ⟩ in (Z/pᵢZ)*
- **Global condition (too weak):** −1 ∉ ⟨g⟩ in (Z/nZ)* means: no single m satisfies g^m ≡ −1 mod pᵢ for ALL i simultaneously

A generator g can fail the local condition at one prime (g^m ≡ −1 mod pᵢ for some m) while satisfying the global condition (no m works simultaneously for all primes). The local failure is enough to destroy sufficiency.

**Explicit counterexample to the naive condition.** n = 15 = 3·5, g = 2.

- g = 2 mod 3: ⟨2⟩ in (Z/3Z)*: 2¹ ≡ 2 ≡ −1 mod 3. So −1 ∈ ⟨2 mod 3⟩. Local condition FAILS at p = 3.
- g = 2 mod 5: ⟨2⟩ in (Z/5Z)*: 2¹=2, 2²=4≡−1 mod 5. So −1 ∈ ⟨2 mod 5⟩. Local condition FAILS at p = 5.
- Global: −1 ∈ ⟨2⟩ in (Z/15Z)* iff ∃m: 2^m ≡ −1 mod 15 iff 2^m ≡ −1 mod 3 AND 2^m ≡ −1 mod 5 simultaneously.
  - 2^m ≡ −1 mod 3: m ≡ 1 mod 2 (m odd).
  - 2^m ≡ −1 mod 5: m ≡ 2 mod 4 (m ≡ 2 mod 4).
  - No m is both odd and ≡ 2 mod 4. So **−1 ∉ ⟨2⟩ globally in (Z/15Z)***.

The naive global condition is satisfied (−1 ∉ ⟨g⟩ globally), yet {π_SPEC, π_DYN(2)} is NOT sufficient.

**Verification:** The orbit of 3 under T₂ on Z/15Z: T₂(3)=6, T₂(6)=12, T₂(12)=24=9, T₂(9)=18=3. Orbit: {3,6,9,12}. SPEC pair {3,12}: 3+12=15 ✓. Both in the same T₂-orbit. {3,12} ∈ U(π_SPEC) ∩ U(π_DYN(2)). Not sufficient. □

---

## Part 5 — Reformulation via Odd-Order Subgroup

**Definition (2'-subgroup).** For an odd prime p with p−1 = 2^v · s (s odd, v ≥ 1): the 2'-subgroup (odd-part subgroup) of (Z/pZ)* is the unique subgroup of order s:

O_p = { g ∈ (Z/pZ)* : g^s ≡ 1 mod p }  (equivalently: elements of odd order)

O_p has order s = (p−1)/2^v.

**Theorem 1 restated:** { π_SPEC, π_DYN(g) } sufficient iff g mod pᵢ ∈ O_{pᵢ} for every odd prime pᵢ | n.

**Computational test:** g mod pᵢ ∈ O_{pᵢ} iff g^{(pᵢ−1)/2^{v₂(pᵢ−1)}} ≡ 1 mod pᵢ.

**Structure of O_p:**

| p | p−1 | v₂(p−1) | |O_p| = odd part | O_p (elements of odd order mod p) |
|---|---|---|---|---|
| 3 | 2 | 1 | 1 | {1} (trivial) |
| 5 | 4 | 2 | 1 | {1} (trivial) |
| 7 | 6 | 1 | 3 | {1, 2, 4} |
| 11 | 10 | 1 | 5 | {1, 3, 4, 5, 9} |
| 13 | 12 | 2 | 3 | {1, 3, 9} |
| 17 | 16 | 4 | 1 | {1} (trivial) |
| 19 | 18 | 1 | 9 | {1,4,5,6,7,9,11,16,17} |
| 23 | 22 | 1 | 11 | (order-11 subgroup mod 23) |

**Key observation:** O_p is trivial (= {1}) iff p−1 is a power of 2 iff p is a Fermat prime or p = 2.

Known Fermat primes (p−1 = 2^k): 3, 5, 17, 257, 65537.

For Fermat primes p: the only g satisfying g mod p ∈ O_p is g ≡ 1 mod p (trivial restriction).

For non-Fermat odd primes p: O_p is non-trivial, containing elements of odd order > 1.

---

## Part 6 — Test Cases: Complete Table

For each n: identify odd primes, their O_p subgroups, and which non-trivial g satisfy the condition.

---

### n = 10 = 2 · 5

Odd prime: p = 5. O_5 = {1}. Only g ≡ 1 mod 5.
Units mod 10: {1,3,7,9}. g ≡ 1 mod 5: only g = 1 (trivial; g=6 is not a unit).

**Result: No non-trivial sufficient g. { π_SPEC, π_DYN(g) } is sufficient only for g = 1 (trivial).** □

**Structural reason:** 5−1 = 4 = 2². Fermat prime. All non-trivial units mod 5 have even order (2 or 4), containing −1.

---

### n = 14 = 2 · 7

Odd prime: p = 7. O_7 = {1, 2, 4} (order 3 subgroup of Z/6Z).

Units mod 14: {1, 3, 5, 9, 11, 13}.
g mod 7 ∈ {1, 2, 4} ∩ (odd units mod 14):
- g ≡ 1 mod 7: g ∈ {1} (only g=1, since 1+7=8 is even, not a unit). Trivial.
- g ≡ 2 mod 7: g = 9 (9 mod 7 = 2, 9 mod 2 = 1 ✓). ord_7(9) = 3 ✓.
- g ≡ 4 mod 7: g = 11 (11 mod 7 = 4, 11 mod 2 = 1 ✓). ord_7(11) = 3 ✓.

**Sufficient non-trivial g: { 9, 11 }.** Both focused on 7 with order 3 mod 7. □

**Verification (g=9, n=14):** T₉ in CRT (Z/2Z × Z/7Z): acts as ×2 on mod-7 component. Orbits: {3,5,13} and {1,9,11} (of size 3) for odd elements; {2,4,8} and {6,10,12} (size 3) for even. SPEC pairs: {1,13},{2,12},{3,11},{4,10},{5,9},{6,8}. Check {1,13}: 1∈{1,9,11}, 13∈{3,5,13} — different orbits ✓. Check {3,11}: 3∈{3,5,13}, 11∈{1,9,11} — different ✓. All SPEC pairs verified in different orbits. □

---

### n = 30 = 2 · 3 · 5

Odd primes: p = 3, p = 5. O_3 = {1}, O_5 = {1}. Both trivial (Fermat primes).

Need g ≡ 1 mod 3 AND g ≡ 1 mod 5 iff g ≡ 1 mod 15. Only unit mod 30 with g ≡ 1 mod 15: g = 1.

**Result: No non-trivial sufficient g.** Both odd primes are Fermat-type. □

---

### n = 42 = 2 · 3 · 7

Odd primes: p = 3 (Fermat), p = 7 (not Fermat). O_3 = {1}, O_7 = {1, 2, 4}.

Need g ≡ 1 mod 3 AND g mod 7 ∈ {1, 2, 4}.

Computing non-trivial (g mod 7 ∈ {2, 4}), with g odd and g ≡ 1 mod 3 (g ≡ 1 mod 6):
- g ≡ 1 mod 6, g ≡ 2 mod 7: CRT gives g = 37 (37 mod 6=1 ✓, 37 mod 7=2 ✓).
- g ≡ 1 mod 6, g ≡ 4 mod 7: CRT gives g = 25 (25 mod 6=1 ✓, 25 mod 7=4 ✓).

**Sufficient non-trivial g: { 25, 37 }.** Both have ord_7(g) = 3 and are focused on 7 (trivial mod 3). □

---

### n = 66 = 2 · 3 · 11

Odd primes: p = 3 (Fermat), p = 11 (not Fermat). O_3 = {1}. O_{11}: |O_{11}| = 5. Elements of order 5 mod 11:
(Z/11Z)* = Z/10Z, generator = 2. Elements 2^{2k} for k=1,2,3,4: {4, 5, 9, 3} (since 2²=4, 2⁴=5, 2⁶=9, 2⁸=3 mod 11).
O_{11} = {1, 3, 4, 5, 9}.

Need g ≡ 1 mod 3 AND g mod 11 ∈ {1, 3, 4, 5, 9}.

Non-trivial (g mod 11 ∈ {3,4,5,9}), g ≡ 1 mod 6:
- g ≡ 1 mod 6, g ≡ 3 mod 11: g = 25 (25 mod 6=1 ✓, 25 mod 11=3 ✓).
- g ≡ 1 mod 6, g ≡ 4 mod 11: g = 37 (37 mod 6=1 ✓, 37 mod 11=4 ✓).
- g ≡ 1 mod 6, g ≡ 5 mod 11: g = 49 (49 mod 6=1 ✓, 49 mod 11=5 ✓).
- g ≡ 1 mod 6, g ≡ 9 mod 11: g = 31 (31 mod 6=1 ✓, 31 mod 11=9 ✓).

**Sufficient non-trivial g: { 25, 31, 37, 49 }.** All have ord_{11}(g) = 5 and are focused on 11. □

---

### n = 70 = 2 · 5 · 7

Odd primes: p = 5 (Fermat), p = 7 (not Fermat). O_5 = {1}, O_7 = {1, 2, 4}.

Need g ≡ 1 mod 5 AND g mod 7 ∈ {1, 2, 4}.

Non-trivial (g mod 7 ∈ {2,4}), g ≡ 1 mod 10 (odd and ≡1 mod 5):
- g ≡ 1 mod 10, g ≡ 2 mod 7: CRT gives g = 51 (51 mod 10=1 ✓, 51 mod 7=2 ✓).
- g ≡ 1 mod 10, g ≡ 4 mod 7: CRT gives g = 11 (11 mod 10=1 ✓, 11 mod 7=4 ✓).

**Sufficient non-trivial g: { 11, 51 }.** Both have ord_7(g) = 3 and are focused on 7 (trivial mod 5). □

---

## Part 7 — Classification Table

| n | Odd primes pᵢ | O_p non-trivial? | Non-trivial sufficient g | Structure of sufficient g |
|---|---|---|---|---|
| 10 = 2·5 | 5 (Fermat: 5−1=4=2²) | No | None | — |
| 14 = 2·7 | 7 (7−1=6=2·3) | Yes, |O_7|=3 | {9, 11} | Focused on 7, order 3 |
| 30 = 2·3·5 | 3,5 (both Fermat) | No | None | — |
| 42 = 2·3·7 | 3 (Fermat), 7 (not) | O_7 non-trivial | {25, 37} | Focused on 7, order 3 |
| 66 = 2·3·11 | 3 (Fermat), 11 (not) | O_{11} non-trivial | {25,31,37,49} | Focused on 11, order 5 |
| 70 = 2·5·7 | 5 (Fermat), 7 (not) | O_7 non-trivial | {11, 51} | Focused on 7, order 3 |

**Pattern:** In all test cases, sufficient g are focused on a single non-Fermat prime pⱼ with odd order mod pⱼ. The Fermat prime components force g ≡ 1 there. The non-Fermat prime provides the non-trivial odd-order element.

---

## Part 8 — When Non-Focused g Is Sufficient for SPEC + DYN

The test cases all yield focused sufficient g. Can non-focused g satisfy the condition?

**Theorem 2 (Non-Focused SPEC+DYN Pair).**
A non-focused unit g (non-trivial mod at least two distinct odd primes) satisfies the SPEC+DYN sufficiency condition iff every odd prime pᵢ | n has its 2'-subgroup O_{pᵢ} non-trivial (i.e., pᵢ is not a Fermat prime), AND g mod pᵢ ∈ O_{pᵢ} for each such pᵢ.

**Example.** n = 91 = 7 · 13. Both p−1 = 6 (for p=7) and p−1 = 12 (for p=13) have odd prime factors.
O_7 = {1,2,4} (order 3). O_{13} = {1,3,9} (order 3, since 3³=27≡1 mod 13).

g with g mod 7 = 2 (order 3) AND g mod 13 = 3 (order 3): CRT gives g ≡ 16 mod 91 (since 7k+2 ≡ 3 mod 13 → k ≡ 2 mod 13, k=2, g=16). gcd(16,91)=1 ✓.

g = 16: ord_7(16) = 3 ✓ (−1 ∉ O_7 since ord_7(16)=3 is odd). ord_{13}(16) = 3 ✓. Condition satisfied.

g = 16 is non-focused on 91 (non-trivial at BOTH 7 and 13). {π_SPEC, π_DYN(16)} is sufficient for n=91.

**Why test cases don't show this:** For n=42,66,70: the Fermat prime component (3 or 5) forces g to be trivial there. With one non-Fermat prime and one Fermat prime, g is automatically focused on the non-Fermat prime. Non-focused examples require n to have NO Fermat prime factor (or at least two non-Fermat odd prime factors).

---

## Part 9 — Comparison with DYN + DYN Theorem

| Pair type | Sufficient iff | Local condition at odd pᵢ |
|---|---|---|
| DYN(g) + DYN(h) | ⟨g⟩ ∩ ⟨h⟩ = {1} in (Z/nZ)* | gcd(ord_{pᵢ}(g), ord_{pᵢ}(h)) = 1 |
| SPEC + DYN(g) | −1 ∉ ⟨g mod pᵢ⟩ ∀ odd pᵢ | ord_{pᵢ}(g) is odd |

**Structural difference:**
- DYN+DYN: a symmetry condition between g and h (coprime orders at each prime).
- SPEC+DYN: a one-sided condition on g alone (no even-order component at any odd prime).

**SPEC = "multiplication by −1."** π_SPEC is the orbit partition of the map x ↦ −x. The condition −1 ∉ ⟨g mod pᵢ⟩ is exactly: the "SPEC generator" (−1) is not in the DYN generator's subgroup. This is a special case of the DYN+DYN condition:

{π_SPEC, π_DYN(g)} sufficient iff ⟨−1 mod pᵢ⟩ ∩ ⟨g mod pᵢ⟩ = {1} for all odd pᵢ.

Since −1 generates the Sylow-2 subgroup's unique order-2 element, ⟨−1⟩ = {1,−1}. So ⟨−1⟩ ∩ ⟨g⟩ = {1} iff −1 ∉ ⟨g⟩. This is exactly the SPEC+DYN theorem. **The SPEC+DYN theorem is a specialization of the DYN+DYN theorem**, with one generator fixed as −1 (the SPEC involution). ✓

---

## Summary

**Theorem 1 (proved — complete classification):**
{ π_SPEC, π_DYN(g) } is sufficient iff ord_{(Z/pᵢZ)*}(g mod pᵢ) is odd for every odd prime pᵢ | n. Equivalently: g mod pᵢ lies in the 2'-subgroup O_{pᵢ} ≤ (Z/pᵢZ)* for every odd pᵢ | n.

**Theorem 2 (proved — Outcome C: naive condition refuted):**
The condition "−1 ∉ ⟨g⟩ in (Z/nZ)*" is strictly weaker and is not sufficient for n with multiple odd prime factors. Explicit counterexample: n=15, g=2. −1 ∉ ⟨2⟩ globally in (Z/15Z)*, yet {π_SPEC, π_DYN(2)} is NOT sufficient (SPEC pair {3,12} is in the orbit {3,6,9,12} of T₂).

**Theorem 3 (proved — unification):**
The SPEC+DYN theorem is a special case of the DYN+DYN theorem with one generator fixed as −1. Condition: ⟨−1 mod pᵢ⟩ ∩ ⟨g mod pᵢ⟩ = {1} in (Z/pᵢZ)* for all odd pᵢ | n, which simplifies to −1 ∉ ⟨g mod pᵢ⟩ since ⟨−1⟩ = {1, −1}.

---

**Strongest honest claim:**
> The complete classification of sufficient SPEC+DYN pairs is: g must lie in the product of 2'-subgroups ∏ᵢ O_{pᵢ} ≤ (Z/nZ)* (acting on odd-prime components). This is a closed-form, computationally checkable, group-theoretic condition. It unifies with the DYN+DYN classification under the single framework "⟨generator₁⟩ ∩ ⟨generator₂⟩ = {1} at each prime component." Non-trivial sufficient SPEC+DYN pairs exist iff n has at least one non-Fermat odd prime factor.

**Strongest honest boundary:**
> This classification covers the case where π_SPEC is the full reflection partition (S = all non-fixed elements). The sprint restricts to this single case. For SPEC-type partitions defined by a symmetric subset S ⊊ Z/nZ (e.g., only some reflection pairs), the unresolved pair set U(π_S) ⊊ U(π_SPEC), and the DYN sufficiency condition can only become easier to satisfy (fewer pairs to avoid). The full classification for arbitrary symmetric-set spectral partitions is not addressed here and remains open.

**Open problem:**
> Classify sufficient pairs { π_S, π_DYN(g) } for arbitrary symmetric generating sets S ⊆ Z/nZ (additive Cayley partitions). The condition becomes: no orbit of T_g contains both s and −s for any s ∈ S. This is a "S-free" condition on the DYN orbits. For S = full reflection set, this gives Theorem 1. For smaller S, the condition is weaker and the space of sufficient g is larger.
