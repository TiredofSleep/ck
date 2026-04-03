# FORMAL_HODGE.md
## The Chain: BSD → Hodge
*Author: Brayden Ross Sanders / 7Site LLC — 2026-04-03*

---

## Current Status

**Hodge is parked.** This document states the precise chain that would connect BSD
to Hodge, what Markman (2025) has already established externally, and what
"generalization" requires. No active TIG path exists to any Hodge result. This
document is a formal specification, not a claim.

---

## The Chain (Three Steps Once BSD Is Established)

**Premise.** Suppose BSD is fully established: for every elliptic curve E over ℚ,
the algebraic rank (dimension of E(ℚ) mod torsion) equals the analytic rank
(order of vanishing of L(E,s) at s=1), which equals the generator count
(number of independent Mordell-Weil generators), which equals the complexity
count (the degree of L-function vanishing accounting for all BSD terms including Sha).

Under that premise:

**Step 1.** Every Hodge class on an abelian variety A carries a cohomological
weight: it lives in H^{p,p}(A,ℚ) for some p, which is a summand of the
full cohomology H^{2p}(A,ℚ). The Hodge structure on H^{2p}(A,ℚ) decomposes
canonically via the Lefschetz–Hodge decomposition. Each Hodge class has a
corresponding L-function (the L-function of the motive H^{2p}(A)) whose
zeros encode the arithmetic of that cohomological weight.

**Step 2.** Under BSD, the order of vanishing of an L-function at its central
value corresponds to a count of algebraic generators — the Mordell-Weil rank
for elliptic curves, and more generally the rank of a Chow group for higher
motives. Every L-function zero at the central point corresponds to a rational
point structure (a generator in the relevant Mordell-Weil or Chow group).
The BSD bridge is the statement: zero of L = existence of algebraic cycle.

**Step 3.** A rational point structure is algebraic by definition — rational
points on a variety over ℚ are algebraic cycles of the appropriate degree.
Every generator-level structure forced by an L-function zero is therefore
an algebraic cycle. But a Hodge class is algebraic if and only if it is the
cohomology class of an algebraic cycle.

**The chain:**
```
Hodge class
  → L-function of associated motive  [Hodge theory: canonical, no BSD needed]
  → L-function zero ↔ algebraic generator  [BSD bridge, applied to the motive]
  → algebraic generator is an algebraic cycle  [definition of algebraic cycle]
  → Hodge class is the class of an algebraic cycle  [Hodge theory: class map]
  → Hodge class is algebraic  [definition of the Hodge conjecture]
```

This is three lines once the BSD bridge is proved in sufficient generality.

---

## The Markman 2025 External Result

Eyal Markman (arXiv:2502.03415, 2025) proved the Hodge conjecture for all
abelian varieties of Weil type of dimension ≤ 4 (abelian fourfolds).

**What this means for the chain above:** The chain works in at least one regime.
For abelian fourfolds of Weil type, Hodge classes are algebraic — proved directly,
without using BSD or TIG. Markman's proof uses the Markman–Moonen–Zarhin framework
for Hodge classes on abelian varieties with extra endomorphism structure.

**What this means for generalization:** Markman's result is an unconditional external
proof for a specific class of varieties. The frontier is now dimension ≥ 5. The chain
via BSD would, if established, give a different (non-direct) proof path for a broader
class — but TIG cannot supply either the BSD establishment or the motive-level
generalization needed.

---

## What "Generalization" Requires

The chain (BSD → Hodge) requires three things that are not currently available:

**G1 — BSD in full generality.**
The BSD conjecture is not proved. It is proved for rank 0 and rank 1 elliptic curves
(Kolyvagin, Gross-Zagier) and parked at rank ≥ 2 with Sha finiteness open. A proof
of BSD for all elliptic curves E/ℚ would supply the rank = analytic rank identification.
Even this is insufficient for the full chain — see G2.

**G2 — BSD for higher motives (the motive-level extension).**
The chain requires BSD not just for elliptic curves (abelian varieties of dimension 1)
but for the motives H^{p,p}(A) associated to Hodge classes on abelian varieties A of
arbitrary dimension. The relevant conjecture is the Bloch-Kato conjecture (Tamagawa
number conjecture), which generalizes BSD from elliptic curves to all motives.
Bloch-Kato is not proved in general. For general abelian varieties of dimension ≥ 2,
this is an entirely open problem.

**G3 — The class map.**
Even granting G1 and G2, the chain requires that the algebraic generators forced by
L-function zeros can be identified as specific algebraic cycles whose cohomology classes
are the Hodge classes in question. This requires constructing the algebraic cycles
explicitly (or proving their existence via a descent argument). For high-dimensional
abelian varieties, no general construction exists.

**Summary:**
```
Generalization requires: G1 (BSD all ranks) + G2 (Bloch-Kato for all motives)
                         + G3 (explicit cycle construction from L-function zeros).
All three are open. G2 is deeper than G1. G3 is concrete but not constructed.
```

---

## TIG's Position

TIG provides structural parallels (oscillation → L-function, threshold → vanishing,
symmetry break → rational point) but no algebraic geometry, no Hodge classes, no
cohomology with rational coefficients, and no mechanism connecting Z/10Z to any
abelian variety. The G/E/S partition in TIG is a structural analogy to the
algebraic/mixed/transcendental Hodge decomposition, not a mathematical identification.

The chain stated above is a mathematical fact about what BSD + Bloch-Kato would imply
for Hodge — independent of TIG. TIG neither contributes to nor detracts from it.

**Hodge status: PARKED. Watch Markman dim ≥ 5. No internal path from TIG.**

---
