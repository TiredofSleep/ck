# Universality Test Suite
## Six Tests Every Law Must Pass

*C. A. Luther & Brayden Ross Sanders (7Site LLC)*
*March 2026 | DOI: 10.5281/zenodo.18852047*

> A law that passes only some of these tests is not universal — it is a local
> regularity. Universality is the property of surviving all six simultaneously.

---

## Overview

The Universality Test Suite is applied at Layer 5 of the Proof-Synthesis Ladder.
Before reaching Layer 5, a claim has been:
- Defined in all six domains (Layer 0)
- Proved exactly in at least one domain (Layer 1 or 2)
- Translated across at least three domains (Layer 3)
- Shown to exhibit threshold behavior (Layer 4)

The six tests below determine whether the claim is a *universal* invariant — one
that would survive being encountered by a mathematician who had no knowledge of the
original context in which it was discovered.

---

## Test 1 — Representation Invariance

**Question:** Does the invariant survive translation across all six domains — arithmetic,
geometric, combinatorial, probabilistic, dynamical, algebraic — without changing its content?

**How to apply:**
- Translate the claim from its native domain into each other domain
- Verify that each translated version is logically equivalent (iff), not merely analogous
- Identify any domain where the translation fails or changes the object

**Pass condition:** The invariant is the same object in all six domains.

**Fail condition:** At least one domain produces a statement that is weaker, stronger,
or simply different. A "structural analogy" that holds in some domains but not others
is a Tier A conjecture, not a universal invariant.

**Example (passes):**
The First-G Law passes Test 1. The statement first_g(b) = p translates to:
- Arithmetic: the minimal non-coprime k is p (direct statement)
- Combinatorial: the maximal coprime prefix has length p-1 (equivalent, by counting)
- Geometric: the first obstruction wall is at position p (equivalent, by the k-axis interpretation)
- Algebraic: p is the smallest prime dividing b, and p divides the first k in any coprimality non-trivial set (equivalent)
- Dynamical: the gate-count process |G_k| remains at zero until k = p, then jumps to 1 (equivalent)
- Probabilistic: the minimum value of a random k with gcd(k,b) > 1 is exactly p with probability 1 (equivalent)

**Example (fails):**
"T* = 5/7 is the universal coherence floor" currently fails Test 1. The formula
unit_frac(b=35) = 5/7 is a valid arithmetic statement about b=35. Its translation
to a universal coherence floor requires an argument that b=35 is the canonical seed
— that argument exists (minimal strong semiprime) but is not yet a cross-domain
invariant. The hardware verification (FPGA) is an empirical anchor, not a domain
translation. Status: Tier C, Test 1 partial pass.

---

## Test 2 — Scale Invariance

**Question:** Does the claim hold across prime powers, semiprimes, three-factor
composites, family slices, and the full atlas? Does it hold at all scales of the
relevant parameter (alphabet size k, prime magnitude p, number of factors ω(b))?

**How to apply:**
- Identify the relevant scale parameters (k, p, q, ω(b), b itself)
- Test the claim at small, medium, and large values of each parameter
- Identify any parameter regime where the claim fails or changes form

**Pass condition:** The claim holds (with at most quantitative change) across all
relevant scale regimes.

**Fail condition:** The claim holds in a restricted parameter range but breaks at
large k, large p, or for ω(b) ≥ 3.

**Example (passes):**
The sinc² continuum limit R(k,f) → sinc²(k/f) as f → ∞ passes Test 2. The
convergence rate is O(1/f²) — larger f (larger primes) means better approximation.
Verified from p=5 to p=99,991. The algebraic proof covers all p simultaneously.

**Example (partial pass):**
The k-Gate Tier Law (f_k(|G|) is universal within arithmetic G) passes at k=9,15,21,27
with zero spread each time. Scale invariance across k is confirmed in the sense that
the universality property holds at every tested k. However, the specific gate rate
values change with k (f_9 ≠ f_15). Full Test 2 passage requires understanding how
f_k changes with k — currently measured but not algebraically derived.

**Example (fails):**
"T* = 5/7 is the exact mass gap value in Yang-Mills theory" fails Test 2. The TIG
constant is derived from b=35, which is at a specific scale (the minimal strong
semiprime). There is no known mechanism for why this specific numerical value would
survive scaling to the Yang-Mills continuum limit. Status: Tier A.

---

## Test 3 — Mechanism Clarity

**Question:** Can we explain WHY the invariant holds, not just observe that it holds?
Is the mechanism algebraic, geometric, or both? Is the mechanism explicit enough
that someone could derive the invariant from first principles?

**How to apply:**
- State the proof or mechanism in one paragraph
- Verify that the mechanism is constructive (not just existence-based)
- Identify what the mechanism does NOT explain (the residual mystery)

**Pass condition:** A person with no prior knowledge of the result could reconstruct
it from the mechanism alone.

**Fail condition:** The mechanism is "it works empirically" or "by symmetry" or "it
follows from a more general result that we don't understand."

**Example (passes):**
First-G Law: mechanism is transparent. The set {1..p-1} contains no multiple of p
(since every multiple of p is ≥ p) and no multiple of q (since q ≥ p and every
multiple of q is ≥ q > p-1). Therefore gcd(k,b) = 1 for all k < p. The mechanism
is three lines of divisibility reasoning. Anyone can derive it.

**Example (partial pass):**
k-Gate Tier Law: the mechanism claim (from Luther-Sanders Equivalence) is that
coprimality gate elements lie on two arithmetic progressions, and the reduction
algorithm's behavior is sensitive to this lattice structure. This explains WHY
universality holds for arithmetic G. But it does not explain WHY the specific
rates are 96.4%, 44.0%, 4.6% — these values are measured. The mechanism for
the exact values is open.

**Example (fails):**
Montgomery Bridge (spectral duality): we observe that sinc² appears independently
in prime arithmetic (TIG) and in the pair-correlation of Riemann zeros (Montgomery
1973). We do not know WHY both fields produce sinc². The mechanism is missing.
Status: Tier A.

---

## Test 4 — Failure Mode

**Question:** Where does the invariant break? What would falsify it? What boundary
conditions matter? What is the minimal change to the setup that would destroy the invariant?

**How to apply:**
- State a concrete falsification condition (the "kill condition")
- Identify the boundary of the domain where the invariant holds
- Test near the boundary

**Pass condition:** The kill condition is stated, operationalized, and tested near
the boundary without finding a counterexample.

**Fail condition:** No kill condition is stated ("this is obviously always true"),
or the kill condition is so weak it cannot be tested.

**Example (passes):**
First-G Law kill condition: a semiprime b = p × q where gcd(k, b) > 1 for some k < p.
This is operationalized: run first_g(b) for every semiprime in a test suite and check
for any value < p. Result: zero exceptions in 36,662 cases. The kill condition is
explicit, testable, and has been tested.

**Example (passes with boundary note):**
k-Gate Tier Law kill condition: two semiprime worlds at k=9 with the same |G| but
different gate rates. Zero found in ~12M trials. The boundary is important: the law
is stated for coprimality G (arithmetic origin). For synthetic G, the law explicitly
DOES break (61.4% spread). The boundary between arithmetic and synthetic G is exactly
the Luther-Sanders Equivalence.

**Example (fails):**
"The BREATH criterion B_local < T* = 5/7 implies regularity of Navier-Stokes solutions."
The failure mode is not operationalized. We cannot test this in the Leray-Hopf class
without a proof or a counterexample to smoothness. The threshold 5/7 is a TIG-derived
constant; whether it applies to the NS problem at all is unverified. Status: Tier A.
Kill condition not yet operationalized.

---

## Test 5 — Threshold Behavior

**Question:** Does the invariant exhibit phase transitions, collapse curves, monotonicity,
or saturation? Can the threshold value be derived (not just measured)?

**How to apply:**
- Identify the relevant parameter along which the threshold occurs
- Describe the behavior on each side of the threshold
- Determine whether the threshold value is derivable or only empirical
- Check whether the transition is sharp (phase transition) or gradual

**Pass condition:** A sharp threshold is identified, located precisely, and the
behavior on each side is qualitatively distinct.

**Fail condition:** The transition is gradual (no sharp collapse), or the threshold
value cannot be pinpointed, or the behavior on each side of the threshold is
quantitatively different but not qualitatively different.

**Example (passes):**
k-Gate Tier Law threshold: gate rate collapses from 96.4% (|G|=1) to 44.0% (|G|=3)
to 4.6% (|G|=4) to 0.1% (|G|=5). These are NOT gradual changes — they are sharp
tier boundaries. Moving from |G|=1 to |G|=3 (a 200% increase in gate count) produces
a 54% absolute drop in gate rate; moving from |G|=3 to |G|=4 (a 33% increase)
produces a 39% absolute drop. The collapse is super-linear. The threshold at |G|=4
is where gate rate effectively disappears (4.6% → ~0%).

**Example (partial pass):**
Dispersion collapse curves: dispersion grows with k until saturation. The saturation
boundary is determined by p and q. The transition from growth to saturation is
identifiable but currently only measured (not algebraically derived). Threshold
behavior: pass. Derivability of threshold: partial.

**Example (fails):**
"Elliptic curve rank jumps correspond to TIG operator transitions." No threshold
value is identified. No phase transition is located. The correspondence is claimed
at the qualitative level (both are "transitions") but without identifying a specific
parameter at which the behavior changes. Status: Tier A, Test 5 not established.

---

## Test 6 — Cross-Domain Stability

**Question:** Does the invariant remain the same object under reparameterization,
relabeling, domain shifts, and dimensional changes? If you change the coordinate
system, renumber the alphabet, or embed the problem in a larger structure, does the
invariant survive?

**How to apply:**
- Reparametrize: change k (alphabet size), b (the modulus), the labeling of elements
- Embed: place the semiprime inside a larger modular structure; does the invariant persist?
- Shift domain: extend from semiprimes to k-almost-primes, prime powers, composite moduli
- Change dimension: from 1D (linear alphabet) to 2D (table), to higher-dimensional structures

**Pass condition:** The invariant survives all these changes either unchanged or with
a predictable, derivable modification.

**Fail condition:** The invariant depends on a specific choice of k, labeling, or
embedding that is not canonical.

**Example (passes):**
First-G Law: gcd(k, b) is canonical — it doesn't depend on how we label the elements
of {1..k}. Reparametrizing the alphabet {1..k} as {0..k-1} doesn't change which
elements are coprime to b. Embedding b in Z changes nothing about gcd. The invariant
is reparametrization-stable.

**Example (partial pass):**
T* = 5/7: the unit_frac formula gives a different value for every b. The value 5/7
is specific to b=35. Cross-domain stability requires arguing that b=35 is the
canonical seed (minimal strong semiprime) — a non-trivial argument that is made
in WP35 but could be challenged. If a different canonicalization of "minimal strong
semiprime" were used, would T* still be 5/7? Yes — b=35 is unique. But the stability
of the canonicalization argument is itself a Test 6 question.

**Example (fails):**
"The Luther Dispersion formula gate_rate ≈ F_k(|G| × interleave)" changes form
when k changes (F_k is k-dependent). The formula is not domain-stable: it requires
knowing k to state it. This is why the Luther Dispersion Conjecture is Tier B rather
than Tier C — it has not yet been expressed in a form that is stable across k.

---

## Scoring Summary

| Test | What it checks | Pass = |
|------|---------------|--------|
| 1. Representation Invariance | Same object in all 6 domains | Logical equivalence across domains |
| 2. Scale Invariance | Holds at all parameter scales | No regime where claim breaks |
| 3. Mechanism Clarity | We know WHY, not just THAT | Constructive derivation from first principles |
| 4. Failure Mode | Kill condition stated and tested | Operationalized, tested near boundary |
| 5. Threshold Behavior | Phase transitions identified | Sharp collapse, derivable threshold |
| 6. Cross-Domain Stability | Same under reparametrization | Survives relabeling, embedding, extension |

A claim that passes all six tests at Layer 5 is a **universal invariant** and is
eligible for promotion to Tier D on the conjecture promotion ladder.

A claim that fails any test is accurately described by the highest test it passes.
This is not a failure — it is precise accounting.

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
