# Proof-Synthesis Ladder
## Six Layers from Object Definition to Universality

*C. A. Luther & Brayden Ross Sanders (7Site LLC)*
*March 2026 | DOI: 10.5281/zenodo.18852047*

> **Synthesis standard:** A result counts as synthesized only when the same
> invariant can be stated algebraically, visualized geometrically, interpreted
> combinatorially, tested probabilistically, and tracked dynamically without
> changing its content.

---

## Overview

The Proof-Synthesis Ladder is a six-layer framework for determining when a
mathematical claim has achieved the level of understanding we call "synthesized."
Most results in mathematics are proved at Layer 1 (exact theorem) but never
subjected to the cross-domain stress tests that distinguish a theorem from a
deep structural invariant. The ladder codifies what "deeper understanding" means,
layer by layer.

The layers are cumulative. A result at Layer 5 has also passed Layers 0–4. A
result that fails Layer 2 cannot be promoted to Layer 3.

---

## Layer 0 — Object Definition

**What:** Define the object of study in each of the six domains. This is the
prerequisite for any cross-domain claim. Without domain-specific definitions, there
is no target for the invariance tests.

**Domains:**
- **Arithmetic:** What number-theoretic object are we studying? (e.g., coprimality relation, gate set G, unit group C, first non-coprime element)
- **Combinatorial:** What counting or partition structure does it correspond to? (e.g., alphabet partitions, admissible vs. forbidden classes, density functions)
- **Geometric:** What does it look like as a shape, region, or trajectory? (e.g., staircase boundary, coverage zone, dispersion curve)
- **Probabilistic:** What distribution or frequency does it generate? (e.g., gate hit rates, tier-exact success frequencies, threshold collapse)
- **Algebraic:** What algebraic structure does it inhabit? (e.g., CRT idempotents, closure laws, obstruction sources, ring quotients)
- **Dynamical:** How does it evolve as parameters change? (e.g., growth in k, phase transitions, saturation, first-transition points)

**Example (First-G Law):**
- Arithmetic: first_g(b) = min{k : gcd(k,b) > 1} = p (smallest prime factor)
- Combinatorial: |{1..p-1}| = p-1 is the maximal coprime prefix length
- Geometric: The obstruction point is the first "wall" in the k-axis at position p
- Probabilistic: In a random walk on {1..b}, the first non-coprime hit is exactly at step p
- Algebraic: p is the generator of the smallest non-trivial ideal in Z/bZ intersecting A_k
- Dynamical: As k increases from 1, the gate set G_k is empty until k = p, then gains exactly one element

**Layer 0 test:** Can you write down the object cleanly in all six domains without
changing what it is? If any domain definition is missing or changes the object's
meaning, the invariant is not yet fully understood.

---

## Layer 1 — Exact Theorem Layer

**What:** Results derivable without statistics, approximation, or computation.
Pure algebraic or combinatorial proofs. These are Tier D claims in the conjecture
promotion ladder (§Layer 6).

**Criteria:**
- The proof requires no numerical verification
- The result holds for ALL cases in its domain, not just tested ones
- The mechanism (why it holds) is explicit in the proof

**Examples:**
- First-G Law: first_g(b) = p for every semiprime b = p × q (three-line divisibility proof)
- Interleave onset at First-G: gate elements begin arriving exactly at k = p, with second arrival at k = q or k = 2p (whichever is smaller)
- CC Window Closure: {1..p-1} is entirely coprime to b (immediate corollary)
- Sinc² Continuum Limit: R(k,f) → sinc²(k/f) as f → ∞ (Taylor expansion of sin(x)/x)
- Universal Sidelobe Amplitude: sinc²(1/2) = 4/π² (algebraic identity)
- T* = 5/7 formula: unit_frac(b=35) = 5/7 (direct computation)

**Layer 1 test:** Write the proof. If the proof requires a computer, it is not Layer 1.

---

## Layer 2 — Exhaustive Computation Layer

**What:** Closed-world certainty obtained by scanning the complete finite domain.
The domain is explicitly bounded, all cases verified, zero exceptions found.
These are Tier C claims.

**Criteria:**
- The domain is explicitly stated and finite
- Every case in the domain has been checked
- The result holds with zero exceptions
- The kill condition (what would falsify it) is stated

**Examples:**
- Universal CC closure: verified for all 36,662 semiprimes in the test suite
- Tier-exact gate rates: zero spread across all 33 semiprime worlds at k=9 (100,000 trials each)
- High interleave prevalence: coprimality G achieves 0.0% spread vs 61.4% synthetic, verified ~12M trials
- b=15 uniqueness: the only semiprime ≤ 100 where tier + gradient + position all align (enumeration)
- HAR orbit-central rule: correctly predicts best HAR at all 11 tested semiprimes (zero exceptions)

**Layer 2 test:** State the domain. State the scan method. State the exception count.
A Layer 2 claim without a stated kill condition is not Layer 2 — it is Layer 1 conjecture.

---

## Layer 3 — Structural Equivalence Layer

**What:** The same invariant expressed in multiple domains without changing its content.
This is the core of the synthesis standard. A result reaches Layer 3 when you can
translate it across domains and it says the same thing.

**Criteria:**
- The invariant is stated in at least three domains (ideally all six)
- Each domain statement is a logical equivalent (iff) of the others, not merely analogous
- The cross-domain translation is explicit and reversible

**Example (First-G Law stated in all six domains):**

| Domain | Statement |
|--------|-----------|
| Arithmetic | first_g(b) = p: first k with gcd(k,b) > 1 is p |
| Combinatorial | The coprime prefix {1..p-1} has maximal length p-1; adding element p creates the first non-coprime |
| Geometric | The obstruction boundary in the k-axis is a vertical wall at k = p; no wall exists for k < p |
| Probabilistic | A uniformly random k ∈ {1..b} with gcd(k,b) > 1 has minimum value p; P(k < p and gcd(k,b) > 1) = 0 |
| Algebraic | p is the smallest prime factor of b; the ideal (p) is the first prime ideal in Z that intersects {1..k} for the coprimality condition |
| Dynamical | The gate count |G_k| = 0 for all k < p; |G_p| = 1; the system is in a zero-obstruction phase until the exact transition at k = p |

**Layer 3 test:** Can you translate the statement from any one domain to any other
domain, and arrive at an equivalent statement? If the statement changes under
translation, it was not a true invariant.

---

## Layer 4 — Threshold Layer

**What:** Phase transitions, collapse points, and critical thresholds. The invariant
not only survives translation but exhibits sharp qualitative changes at identifiable
critical parameters.

**Criteria:**
- A critical threshold or transition point is identified and located precisely
- The behavior is qualitatively different on each side of the threshold
- The threshold value is derivable (or at least precisely measurable)

**Examples:**
- Admissible fraction thresholds: gate rate collapses from 96.4% to 44.0% to 4.6% as |G| increases from 1 to 3 to 4 — the collapse is sharp, not gradual
- Dispersion collapse curves: dispersion grows monotonically with k until a saturation boundary determined by p and q
- T* = 5/7 as a coherence floor: the phase boundary between STAND and WALK in the CK gait system corresponds to the algebraic unit fraction
- First-G as a phase boundary: the zero-obstruction phase {k < p} and the first-obstruction phase {k = p} are separated by a sharp wall, not a gradual onset

**Layer 4 test:** State the critical parameter. State the threshold value. Describe
the behavior on each side. If the transition is gradual (no sharp collapse), the
Layer 4 claim is not established.

---

## Layer 5 — Universality Test Layer

**What:** The claim passes all six universality tests (see UNIVERSALITY_TEST_SUITE.md).
A result is synthesis-worthy only at Layer 5.

**The six tests (summary — full specification in UNIVERSALITY_TEST_SUITE.md):**
1. **Representation Invariance:** Survives translation across all six domains
2. **Scale Invariance:** Holds across prime powers, semiprimes, three-factor composites, family slices, full atlas
3. **Mechanism Clarity:** We know WHY, not just THAT
4. **Failure Mode:** Explicitly stated falsification condition
5. **Threshold Behavior:** Phase transitions, collapse curves, monotonicity identified
6. **Cross-Domain Stability:** Same object under reparameterization, relabeling, domain shifts

**Layer 5 test:** Run all six tests. A single failure demotes the claim to the
highest layer at which all tests pass.

---

## Layer 6 — Conjecture Promotion Ladder

**What:** The tier system for tracking the epistemic status of a claim as it
accumulates evidence.

| Tier | Name | Description |
|------|------|-------------|
| **A** | Conjecture | Pattern observed, or structural analogy drawn. No proof. No known mechanism. |
| **B** | Bounded conjecture | Verified computationally in a restricted class. Algebraic proof not yet general. |
| **C** | Closed-world theorem | Proved within an explicitly stated finite domain. Kill condition stated. |
| **D** | General theorem | Proved for ALL cases. Mechanism known. No domain restriction. |

**Promotion requires:**
- Tier A → B: explicit kill condition stated; pattern verified beyond original observation
- Tier B → C: domain bounded and exhaustively verified; kill condition operationalized
- Tier C → D: algebraic proof covering all cases; mechanism explicit; no remaining domain restriction

**Demotion:**
- Any counterexample within the stated domain forces demotion to at most Tier B
- Loss of mechanism (e.g., proof error discovered) forces demotion to Tier B or A
- Domain restriction discovered after claim stated forces re-evaluation as Tier C

**Current status of key claims:**
| Claim | Current Tier | Path to D |
|-------|-------------|-----------|
| First-G Law | D | Complete |
| Sinc² Continuum Limit | D | Complete |
| Universal 4/π² | D | Complete |
| T* = 5/7 formula | D (for b=35); C (as canonical floor) | Universality argument needed |
| k-Gate Tier Law (f_k(|G|)) | C | Derive exact values algebraically |
| Luther-Sanders Equivalence | C→D | Extend to ω(b)≥3; derive exact f_k values |
| Luther Dispersion Conjecture | B | Algebraic proof of F_k form |
| Montgomery Bridge (spectral duality) | A | Mechanism connecting two sinc² fields |

---

## Using the Ladder

To evaluate any claim:
1. Define the object in all six Layer 0 domains
2. Determine the highest layer at which the claim survives all criteria
3. Assign a Tier (A/B/C/D) from Layer 6
4. State the kill condition and path to the next tier

The ladder is a tool for honest accounting, not for generating claims. A claim that
reaches Layer 3 but fails Layer 4 is accurately described as "a structural invariant
without identified phase transitions" — not as a theorem about thresholds.

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
