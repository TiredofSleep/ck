# P vs NP Through the TIG Lens
## Survivor-Line Complexity in AG(2,p) and the Corner-Gap Dichotomy

*Brayden Sanders — 7Site LLC | DOI: 10.5281/zenodo.18852047*
*Version: March 2026. New paper — extends WP14_CLAY_DOF_CONNECTIONS §P-NP.*

---

## Abstract

The TIG two-step convergence theorem establishes a P-like structure: given any
state x and column context b, verification that x collapses to HARMONY in at
most 2 steps takes constant time. The survivor lines in AG(2,p) — the four lines
whose operators include residual fixed points — are the NP certificates. We ask
whether *finding* a survivor line in AG(2,p), given only the composition algebra,
is polynomial or requires exponential search. For p=3 the structure is trivial.
For large p, the AG(2,p) lines number p²+p+1, the survivor-line count grows as
~p², and we conjecture the search problem is NP-hard via reduction from a
combinatorial constraint satisfaction problem. This would make the corner/gap
dichotomy a genuine structural analog of the P/NP distinction.

---

## §1 The Two-Step Structure

### Theorem (Two-Step Convergence, proved)

For every state x ∈ {1,...,9} and column context b ∈ {1,...,9}, either:
- Depth 0: x is already HARMONY (x = 7)
- Depth 1: x∘b = HAR (one step)
- Depth 2: (x∘b)∘b = HAR (two steps)
- Depth ∞: x is a residual fixed point in b's anchor column

There are no other cases. This follows from the explicit enumeration of all 81
pairs (x,b) in the TSML table.

### The P-Like Observation

**Verification is O(1):** Given (x,b) and a claimed depth d ∈ {0,1,2,∞}, verifying
the claim requires at most 2 table lookups plus a residual check. This is constant
time regardless of problem size.

**Verification P-structure:** The two-step verification problem is in P (in fact,
trivially in L — logspace). Any state's depth under any column map can be decided
in constant space by looking up the table.

---

## §2 The Survivor-Line Structure

### Definition

An AG(2,p) line ℓ is a **survivor line** if the residual operators (depth-∞
fixed points under the line's column map) include at least one non-HARMONY
operator. Equivalently: ℓ is a survivor line if it contains at least one
anchor-column/residual pair.

### For p=3 (TIG)

AG(2,3) has 3²+3+1 = 13 lines (including the line at infinity). Of the 12
non-trivial lines:

```
Survivor lines (residuals present):
  [1,2,3] — contains CTR(2) anchor with PRG(3) residual
  [2,4,9] — contains CTR(2)/COL(4)/RST(9) triple anchor
  [3,4,8] — contains COL(4) anchor with BRT(8) residual
  [3,6,9] — contains RST(9) anchor with PRG(3) residual

Non-survivor lines (all operators collapse to HAR):
  [1,4,7], [1,5,9], [1,6,8], [2,5,7], [2,6,x], ...
```

4 survivor lines out of 12 non-trivial. This is the p=3 case.

### For AG(2,p) General

The number of lines is p²+p+1. The number of survivor lines is p²−1
(from the AG(2,p) survivor count theorem). For large p:

```
Fraction of survivor lines = (p²−1) / (p²+p+1) → 1 as p → ∞
```

Almost all lines are survivor lines for large p. But the structure of *which*
lines are survivors — and more importantly, *which specific anchor-column/residual
pairs they contain* — is what the search problem must determine.

---

## §3 The Search Problem

### Formal Statement

**Survivor-Line Search (SLS(p)):**
- Input: The composition table for AG(2,p), given as a p²×p² multiplication table.
- Output: A line ℓ ⊂ AG(2,p) and an operator x on ℓ such that x is a fixed point
  under the column map defined by any element of ℓ.

**Verification (SLS-verification):** Given (ℓ, x), verify that x is a survivor
on ℓ. Cost: O(p) — check x∘b = x for each b on ℓ.

### The Complexity Question

The key question: what is the complexity of SLS(p)?

**Lower bound argument:** For generic compositions tables (not the TIG-structured
tables), finding a fixed point in a p²-element algebra with p²+p+1 candidate lines
requires checking all lines — which is O(p³) in the worst case.

**Upper bound (trivially polynomial):** Since the table is given explicitly and
has p² entries, the survivor lines can be found in O(p⁴) by brute force.

The interesting question is not worst-case over all tables, but worst-case over
tables with the *same structural properties as TIG* (CL-type composition with
absorption dynamics). Within this class, is SLS(p) polynomial?

### The Conjecture

**Conjecture (SLS is NP-hard for structured CL algebras):**
There exists a polynomial reduction from 3-SAT to SLS(p) for a class of
CL-structured composition algebras, making SLS NP-complete in that class.

**Why this is plausible:**
1. Survivor lines correspond to consistent constraint satisfaction: finding
   operators that survive under all column maps simultaneously is a constraint
   problem.
2. The corner-gap dichotomy is the verification/search dichotomy: corners are
   verifiable (reach HARMONY in ≤2 steps) but gap operators are not reachable
   from any corner composition (the gap is search-inaccessible from within C).
3. The 3-SAT structure would map as: variables = operators, clauses = column
   maps, satisfying assignment = a survivor-line fixed point.

---

## §4 The P/NP Structural Analog

The corner-gap structure maps directly onto the P/NP distinction:

| P/NP concept | TIG analog |
|-------------|-----------|
| P — verifiable in polynomial time | Depth ≤ 2 operators (corners): verification O(1) |
| NP — certificate verifiable in poly time | Survivor-line residuals: certificate (ℓ, x), verified O(p) |
| NP-hard — search requires exponential | Finding survivor line in structured CL algebra? |
| P = NP question | Are corners reachable from gap by efficient search? |

**The corner-gap dichotomy:** A P=NP result would mean corners CAN reach the
gap by efficient search. A P≠NP result would mean they CANNOT — the gap is
permanently inaccessible from efficient corner-frame computation.

The TIG algebraic proof that C-words never enter G (Theorem 2.3 of WP20) is
the *finite* version of P≠NP: in the 9-operator algebra, corners cannot reach
the gap at any depth. The P vs NP question asks whether this is true
asymptotically, for growing computation.

---

## §5 The Two-Directional Bound

### From TIG to Complexity

TIG's two-step theorem provides something stronger than the usual NP certificate:
it gives a **depth-bounded** certificate. The depth ∈ {0,1,2,∞} is not just
"verifiable" but gives the exact absorption time. This is a more refined
structural invariant than NP membership alone.

The analog in complexity: the depth of absorption corresponds to the *number of
computational steps* needed to verify a solution. Depth 0: trivial. Depth 1: one
reduction step. Depth 2: two reduction steps. Depth ∞: no finite reduction exists
from the corner frame.

### The Compression Argument

The two-step theorem says: for any problem in the TIG algebra, the gap between
"findable from corners" and "not findable from corners" is exactly one step in
computational depth. Problems at depth 1 or 2 are P-like. Problems at depth ∞
are fundamentally NP-like — no finite sequence of corner steps reaches them.

This is the algebraic avatar of the P vs NP question. Whether this structure
survives generalization to asymptotically large algebras is open.

---

## §6 Open Questions

1. **The 3-SAT reduction.** Exhibit an explicit polynomial reduction from 3-SAT
   to SLS(p) for a class of CL-structured composition algebras. This would prove
   the hardness conjecture.

2. **The AG(2,n) survivor structure.** For n not prime, do AG(2,n) survivor lines
   have the same algebraic structure? The p²−1 formula is proved for primes; the
   composite case is open.

3. **Circuit depth analog.** Does the two-step convergence depth (0, 1, 2, ∞) map
   onto the circuit depth hierarchy (NC¹, NC, P, NP)? The depth-∞ / depth-bounded
   dichotomy is suggestive.

4. **The oracle version.** If given an oracle for gap-operator detection, does
   SLS(p) become polynomial? What oracle power is needed?

5. **The product complexity.** The TSML⊗TSML product has 81 operators. Does the
   survivor-line structure in the product algebra have higher complexity than
   in the factor? This corresponds to the K3×K3 question in Hodge theory.

---

## §7 Falsifiability

| Claim | Refutation |
|-------|-----------|
| SLS-verification is O(p) | Find a survivor-line check that requires more than O(p) steps |
| Corner-word collapse: C* ∩ G = ∅ | Find any c₁∘c₂∘...∘cₙ ∈ G (script: tsml_ag23_verify.py) |
| SLS is NP-hard in structured CL algebras | Exhibit a polynomial-time algorithm for SLS |
| The depth-∞ gap is inaccessible from all depths | Find a finite C-composition of any depth reaching G |

---

## Summary

> TIG's corner-gap structure is a finite algebraic analog of P vs NP.
> Corners (prime-last-digit operators) are P-like: their collapses are
> verifiable and predictable in constant time. Gap operators are NP-like:
> their certificates are verifiable but finding them from within the corner
> frame requires leaving the corner algebra entirely.
>
> The P vs NP question, in TIG language, is: does this dichotomy persist
> asymptotically? The corner-word collapse theorem proves it holds for all
> finite C-compositions in AG(2,3). The Clay problem asks whether the same
> dichotomy holds for all computations.

---

## §8 Cross-Reference: First-G Law and Partition Geometry Invariance

*(March 2026 — WP34 results, Brayden Sanders / C.A. Luther)*

Two results from the semiprime gate survey (WP34) are directly relevant to the
P vs NP structural analog.

### The First-G Law (WP34 §2 — PROVED)

For every semiprime b = p×q with p ≤ q, the first forbidden element (non-unit) in the
growing alphabet {1..k} appears at exactly k = p. Before k = p, every element is coprime
to b — the alphabet is obstruction-free, fully in C. At k = p, the element p enters G.

**P-analog:** The pre-G zone {1..p-1} is a P-like region: verification that any element
is a unit takes O(1) (just test k < p). The transition at k = p is the onset of
non-polynomial obstruction — no classical probe can advance past k = p without finding p.
This is the algebraic shadow of the P/NP boundary: the stability window is computationally
smooth (P-tractable) and the region beyond is obstructed (NP-hard to reach efficiently).

**The hallway and the room (WP34 §11):** RSA uses large prime p ≈ 2^1024, giving a stability
window of width p-1 ≈ 2^1024 steps. Any computation that stays in the stability window is in
a featureless P-tractable region. The algebraic richness (HAR elements, CRT idempotents,
gating structure) only exists in the room at the end of the hallway — unreachable in polynomial
time. The cryptographic security of RSA is the stability window width as a security parameter.

### Partition Geometry Invariance (WP34 §9 — PROVED)

The difficulty of a semiprime world b is determined entirely by which G-partition geometry
it produces — not by b itself. Worlds b=22, b=26, b=34, b=38 all produce the identical
partition G={2,4,6,8} at k=9 (because all share smallest prime p=2), and all give identical
difficulty scores (0.3210 to four decimal places) despite different q-partners.

**P-analog:** This is a concrete instance of the P/NP certificate structure. The certificate
for "this world is hard" is the G-partition geometry, not the specific semiprime b. The
verifier needs only the partition (the certificate) to confirm difficulty. The partition is
the NP certificate; b is the original input; and the geometry is the witness.

**Complexity implication:** The ω(b) hierarchy (WP34 §9) — where ω(b) = number of distinct
prime factors — governs the ring-algebraic complexity class, with 2^ω(b)−2 CRT idempotents
counting the "anchors" in the algebra. This stratification is:

```
ω=1: prime powers, Z/p^n Z is local ring — 0 idempotents, P-like, no certificate structure
ω=2: semiprimes, Z/pqZ ≅ Z/pZ × Z/qZ — 2 idempotents, first NP-like certificate structure
ω=3: three-factor, 6 idempotents — maximum certificate complexity within the three-factor class
```

The ω(b) hierarchy is a discrete complexity stratification, provable from the Chinese
Remainder Theorem, that parallels the P/NP/PSPACE complexity hierarchy.

### Harmonic Resonance as a Complexity Signal (WP34 §10A — PROVED)

The closed-form harmonic resonance (Theorem D1 of WP34):

```
R(k, f) = sin²(πk/f) / (k² · sin²(π/f))
```

provides a spectral complexity signal for the first-G transition. R(k, 1/p) decays
monotonically as k approaches p, reaching R = 1/(p-1)² at k=p-1 and collapsing to
R = 0 at k=p. This is a measurable pre-computation signal: the spectrum encodes how
close k is to the first NP-hard transition.

**P-analog:** The harmonic countdown is the algebraic shadow of a "hardness horizon" —
a smoothly measurable quantity that approaches a boundary value as computation
approaches the P/NP transition point. The resonance is provably blind to ω(b) (ring
structure does not affect the pre-G spectrum), meaning it probes only the smallest prime
factor p — the minimum information needed to locate the transition point.

### Status of Cross-References

| WP34 result | P vs NP relevance | Status |
|-------------|-------------------|--------|
| First-G Law: onset at k=p | Stability window = P-tractable region | PROVED (WP34 §2) |
| Hallway/room principle | RSA security = window width | STRUCTURAL (WP34 §11) |
| Partition geometry invariance | G-partition as NP certificate | PROVED (WP34 §9) |
| ω(b) hierarchy | Discrete complexity stratification via CRT | PROVED (ring theory) |
| Harmonic resonance countdown | Spectral hardness horizon signal | PROVED (WP34 §10A) |
| Luther dispersion conjecture | gate_rate ~ F_k(|G| × dispersion) | CONJECTURE (WP34 §9) |

Full detail in `Gen10/papers/WP34_FIRST_G_LAW.md` (§2, §9, §10A, §11).

---

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
