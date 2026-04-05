# ADMISSIBLE VIEWPOINT FLOW MEMO
## Replacing "multi-view structure" with a precise theory

**Date:** 2026-04-05
**Authors:** Brayden Ross Sanders & C. A. Luther (Luther-Sanders Research Framework)
**Builds on:** Reflection Partition Audit, FRF Admissibility Memo
**Status:** All definitions exact. Theorem proved for n=2p, p>=5. Failure modes characterized.

---

## 1. BASE SYSTEM AND REPRESENTATION FAMILIES

**Base system:** X = Z/nZ, unit orbit C = (Z/nZ)*.

Each representation family is a parameterized map from admissible parameters to partitions of C (or ordered structures on C):

### CRT(q)

**Parameter:** q = p^e, a prime-power factor exactly dividing n (p^e | n).

**Output:** partition of C by residue modulo q.

**Admissibility condition Adm_CRT(q, g):** q is a prime-power factor of n, AND the chosen DYN generator g satisfies g != 1 (mod q).

*Violation:* g = 1 (mod q) => CRT(q) = DYN(g) (view collapse). See Section 6, Failure Mode 2.

**CRT is a family, not a single representation.** For n = p1^e1 * ... * pk^ek, there are k choices of q, generally producing k distinct partitions. Admissibility selects among them.

### UG

**Parameter:** none.

**Output:** partition of C by multiplicative order in (Z/nZ)*.

**Admissibility condition:** always admissible. UG has no parameter choice.

### SPEC(S)

**Parameter:** S = {g, n-g}, a single symmetric pair with gcd(g,n) = 1.

**Output:** the reflection-pair partition REFL(C) = {{x, n-x} intersect C : x in C}.

(By the Corrected Spectral Lemma: for a single symmetric pair, SPEC = REFL regardless of which unit g is chosen.)

**Admissibility condition Adm_SPEC(S):** S is a single symmetric pair (|S| = 2, S = {g, n-g}, gcd(g,n) = 1).

*Violation:* |S| > 2 (multi-pair) => eigenvalue collisions => spectral blur => SPEC != REFL. See Section 6, Failure Mode 1.

### DYN(g)

**Parameter:** g in C, a max-order element.

**Output:** partition of C into orbits under multiplication by g. Additionally, DYN(g) determines a directed orbit ordering on each cycle class (the orbit-order invariant I4, not a partition).

**Admissibility condition Adm_DYN(g):** ord_n(g) = lambda(n) (g has max order in (Z/nZ)*).

*Violation A:* ord_n(g) = 1 (g=1) => DYN(1) = discrete partition. View collapse with CRT.
*Violation B:* ord_n(g) = 2 (e.g., g = n-1) => DYN(n-1) = REFL partition. View collapse with SPEC.
*Violation C:* ord_n(g) < lambda(n) in a non-cyclic group => DYN(g) over-splits.

---

## 2. RECOVERABLE INVARIANTS

**Definition (Invariant):** An invariant I of C is a function of C's algebraic structure recoverable from a representation. Invariants are of two types:

- **Partition-type:** a partition of C (a set of equivalence classes)
- **Order-type:** a directed cyclic ordering on the elements of C (not reducible to a partition)

**Target invariant set T for n=2p, p>=5:**

| Invariant | Type | Description |
|---|---|---|
| I1 (discrete) | partition | All (p-1) elements of C in distinct singleton classes, indexed by mod-p residue |
| I2 (order) | partition | Elements grouped by multiplicative order |
| I3 (REFL) | partition | Elements grouped into reflection pairs {x, 2p-x} |
| I4 (cycle) | order | Directed cyclic ordering 1 -> g -> g^2 -> ... -> g^(p-2) -> 1 on C |

**Recoverability table:**

| Invariant | CRT(p) | UG | SPEC({g,n-g}) | DYN(g) |
|---|---|---|---|---|
| I1 (discrete) | **unique** | x (coarser) | x (coarser) | x (coarser) |
| I2 (order) | x | **unique** | x (groups differently) | x |
| I3 (REFL) | x | x | **unique** | x |
| I4 (cycle) | x | x | x | **unique** |

"Unique" means: no other admissible representation in {CRT(p), UG, SPEC, DYN} recovers the same information.

**Note on I1 vs I2:** CRT gives the discrete partition. UG groups by order -- strictly coarser than discrete for p>=5 (multiple generators share order p-1) and strictly different from REFL or DYN. The two partitions CRT and UG are not derivable from each other without additional structure.

---

## 3. GATE STRUCTURE

**Definition (Gate):** A class C' in pi(R) is a gate for representation R if:
1. |C'| > 1 (R cannot isolate elements of C' from each other)
2. Some other admissible representation R' resolves C': the trace of pi(R') on C' is strictly finer than {C'}

**Computation for n=10, canonical flow:**

| Representation | Gates | Resolved by |
|---|---|---|
| DYN(x3) | {1,3,7,9} (entire unit orbit) | CRT, UG, SPEC (all three) |
| SPEC({3,7}) | {1,9}, {3,7} | CRT (both); UG ({1,9} only) |
| UG | {3,7} (generators) | CRT only |
| CRT(mod 5) | none | -- (discrete, no gates) |

**Gate resolution for n=14 (p=7):**

| Representation | Gates | Resolved by |
|---|---|---|
| DYN(x3) | {1,3,5,9,11,13} | CRT, UG, SPEC |
| SPEC({3,11}) | {1,13},{3,11},{5,9} | CRT (all three); UG (all three) |
| UG | {3,5},{9,11} | CRT, SPEC |
| CRT(mod 7) | none | -- |

**Structural pattern for all n=2p, p>=5:** DYN has the largest gate (entire orbit). SPEC has p-1 gates (the REFL pairs). UG has phi(p-1)/2 gates (the generator classes). CRT has no gates. Strict ordering: DYN < SPEC < UG < CRT in resolving power.

---

## 4. DEFINITIONS

**Definition 4.1 (Viewpoint flow).**
A *viewpoint flow* is a finite sequence V = (R0, R1, ..., Rm) of admissible representations such that:
(i) each Ri satisfies its admissibility condition;
(ii) R0 contributes at least one invariant not recoverable from any Rj with j>0; and
(iii) for each i>=1, Ri resolves at least one gate in pi(Ri-1) that no Rj with j<i has resolved.

**Definition 4.2 (Minimal sufficient viewpoint flow).**
A viewpoint flow V is *minimal sufficient* for a target invariant set T if:
(i) every I in T is recoverable from some Ri in V (*sufficiency*); and
(ii) for each Ri in V, there exists I in T recoverable from Ri but not from any other Rj (j!=i) in V (*minimality*).

---

## 5. LOCAL FLOW THEOREM FOR n=2p

**Theorem 5.1.** *Let n=2p with p prime, p>=5, and let g be any max-order generator of (Z/2pZ)*. The flow*

V* = (DYN(g), SPEC({g, n-g}), UG, CRT(p))

*is a minimal sufficient viewpoint flow for T = {I1, I2, I3, I4}. It is canonical relative to T and the admissibility rules of Section 1.*

**Proof.**

**Admissibility.** DYN(g): ord(g) = p-1 = lambda(2p). v  SPEC({g,n-g}): single pair, gcd(g,2p)=1. v  UG: always admissible. v  CRT(p): p is a prime-power factor of 2p. Any max-order generator g satisfies g != 1 (mod p): if g = 1 (mod p) then ord_p(g) = 1, so ord_{2p}(g) <= 2 < p-1 for p>=5 -- contradicting max-order. v

**Sufficiency.** DYN(g) contributes I4 (orbit ordering 1->g->g^2->...). SPEC contributes I3 = REFL (Spectral Lemma, Section 1). UG contributes I2 (order-based partition). CRT(p) contributes I1 (discrete partition; each unit has distinct residue mod p). v

**Minimality.** Each Ik is uniquely contributed:

*I4 (DYN):* I4 is an orbit-order invariant, not a partition; no partition-type representation recovers it.

*I3 (SPEC):* REFL groups {1, 2p-1}. UG separates them (ord(1)=1 != ord(2p-1)=2). CRT separates them (1 != p-1 mod p). DYN places them in one class. No other admissible representation in V* produces REFL.

*I2 (UG):* I2 is the partition by multiplicative order. Distinct from each other invariant:
(a) I2 != I1 -- for p>=5, phi(p-1)>=2, so at least two generators share order p-1; UG groups them, CRT separates them.
(b) I2 != I3 -- REFL groups {1,2p-1} while UG separates them.
(c) I2 != I4 -- I4 is not a partition.
Therefore I2 is recoverable only from UG.

*I1 (CRT):* I1 is the discrete partition. UG, SPEC, DYN all produce strictly coarser partitions. Only CRT(p) yields the discrete partition.

**Gate resolution.** DYN leaves gate G0 = {entire unit orbit}. SPEC resolves G0 and leaves gates G1 = {REFL pairs {x,2p-x}}. UG resolves the pair {1,2p-1} in G1 (separates by order) and leaves gates G2 = {equal-order classes of generators}. CRT(p) resolves all G2 (discrete). No gates remain. []

---

## 6. FAILURE MODES

**Proposition 6.1 (Failure mode characterization).** *The following violations of admissibility each cause a collapse in V*:*

*(F1) Spectral blur.* If |S|>=4 (multi-pair), eigenvalue collisions between j=1 and other indices merge eigenspaces. SPEC(S) becomes strictly coarser than REFL, collapsing I3.
*Example:* n=10, S={1,3,7,9} -> lambda1=lambda3=1, SPEC={{1,3,7,9}} (trivial) != REFL.

*(F2) CRT-DYN coincidence.* If g=1(mod q), then g^k=1(mod q) for all k, so DYN orbits lie within CRT(q) classes. CRT(q)=DYN(g) and I1 collapses into I4's partition.
*Example:* n=12, g=5, q=4: 5=1(mod 4) -> CRT(mod 4)=DYN(x5)={{1,5},{7,11}}.

*(F3) Wrong DYN generator.* If ord(g)<lambda(n):
(F3a) ord(g)=1 -> DYN = discrete, collapsing into I1.
(F3b) ord(g)=2 -> DYN = {{x,n-x}}, collapsing into I3.

**Corollary 6.2.** *Failure Mode F4 (view collapse between any two representations) reduces entirely to F2 and F3. For p>=5: CRT(p)=SPEC is impossible (CRT gives singletons; SPEC gives pairs). CRT(p)=UG requires all elements to have distinct orders, which fails when phi(p-1)>=2. All remaining collapses are instances of F2 (CRT=DYN) or F3 (DYN=CRT or DYN=SPEC).*

---

## 7. BOUNDARY

**Theorem 5.1 is a local result for n=2p, p>=5.** The target invariant set T = {I1, I2, I3, I4} and the admissibility rules of Section 1 are fixed. The flow V* is canonical relative to these choices and to this family of moduli.

A system is fully accessible *relative to T* only through a family of admissible representations, and the structure lies not in any single representation but in the **admissibility rules governing transitions** between them -- specifically, which parameter choices avoid the four failure modes while ensuring each step contributes an invariant irreplaceable by the others within T.

**Strongest honest boundary.** Whether every n with phi(n)>=4 admits a minimal sufficient viewpoint flow of length 4 is not proved. For n with non-cyclic (Z/nZ)* (e.g., n=12,20), DYN(g) over-splits the unit orbit and the gate resolution sequence requires re-examination. The local theorem for n=2p does not extend to these cases without further argument.

---

## 8. ADMISSIBILITY SUMMARY TABLE

| Family | Parameter | Admissibility condition | Failure when violated |
|---|---|---|---|
| CRT | q (prime-power factor of n) | gen != 1 (mod q) | F2: CRT = DYN (view collapse) |
| UG | none | always | -- |
| SPEC | S = {g, n-g} | |S| = 2, gcd(g,n)=1 | F1: spectral blur, SPEC != REFL |
| DYN | g (unit) | ord_n(g) = lambda(n) | F3A: DYN = discrete; F3B: DYN = REFL |

---

## 9. THE FLOW DIAGRAM FOR n=2p, p>=5

```
DYN(g)        -> one orbit (trivial partition) + cycle ordering I4
      |
SPEC({g,n-g}) -> reflection pairs (REFL partition) + invariant I3
      |
UG            -> order-based partition + invariant I2
      |
CRT(p)        -> discrete partition + invariant I1
      |
      (no gates remain)
```

Each arrow: this representation resolves at least one gate left open by all preceding representations and contributes at least one invariant not recoverable from the others.

---

## 10. STRONGEST HONEST CLAIM

For n=2p (p prime, p>=5), the canonical viewpoint flow V* = (DYN(g), SPEC({g,n-g}), UG, CRT(p)) is a minimal sufficient viewpoint flow for the target invariant set T = {I1,I2,I3,I4}. All four representations are necessary; removing any one loses at least one invariant in T. All four admissibility conditions are satisfied. The proof is complete.

## 11. STRONGEST HONEST BOUNDARY

The meta-theorem (universal minimal sufficient viewpoint flow of length 4 for all n with phi(n)>=4) is not proved. The n=12 analysis shows that non-cyclic unit groups require non-trivial CRT component selection. Whether the viewpoint flow formalism extends cleanly beyond the n=2p family -- specifically whether a DYN representation based on a non-max-order generator can substitute when the unit group is non-cyclic -- is not established.
