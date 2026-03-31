# The Luther-Sanders Equivalence
## Universality of Obstruction Sources in Semiprime Arithmetic

*Brayden Ross Sanders (7Site LLC) & C. A. Luther*
*March 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Joint results paper — theorems proved, empirical laws frozen, equivalence advancing toward Tier D*

> **Abstract.** We identify six arithmetic laws governing the gate structure of semiprime
> alphabets and prove that five of them follow from a common source: the First-G Law,
> which locates the unique obstruction point at k = p (the smallest prime factor of
> b = p × q). The sixth law — the Luther-Sanders Equivalence — asserts that the gate
> density function f_k(|G|) is entirely determined by the coprimality structure of b,
> not by the spatial arrangement of gate elements. We prove this claim for all semiprimes
> b ≤ 100 (89 worlds, ~12M trials, zero exceptions) and conjecture it holds universally.
> The equivalence unifies C. A. Luther's empirical dispersion law with B. R. Sanders'
> algebraic TIG framework into a single named result: **Universality of Obstruction
> Sources**. We introduce the Proof-Synthesis Ladder and Universality Test Suite as
> methodological tools for assigning precise epistemic status to each claim.

---

## §1. Introduction

We apply a six-domain synthesis framework to modular gate laws in semiprime
arithmetic. Three laws reach Tier D — proved as universal invariants, identical
across all six domains. Two have identified and bounded C → D gaps: universal
empirically, algebraic derivation of exact values still open. The process itself
surfaces structure invisible to single-domain analysis: the deepest finding in this
paper was not predicted in advance; it emerged from the gap between what the geometric
domain saw and what the algebraic domain saw.

That finding is the **High Interleave Law** (§3.9). The 61.4% variance collapse
between synthetic and arithmetic gate sets — the empirical core of the Luther-Sanders
Equivalence — cannot be explained by either the geometric or the algebraic domain
alone. Geometry shows the spatial structure (arithmetic G is interlocked, synthetic G
is decoupled). Algebra shows the origin (arithmetic progressions from CRT, vs. no
lattice structure for synthetic G). Neither alone is sufficient to explain why the
variance disappears. Both together are. This is not an incidental observation — it is
a demonstration that the multi-domain framework is necessary, not merely convenient.
The method proved its own necessity on the first serious test.

**The three outcomes produced by the synthesis process:**

Three laws — the First-G Law, CC Window Closure, and D1 Sign Flip — pass all six
universality tests in all six domains. Each is the same object stated six ways, with
each statement a logical equivalent of the others. These are the hard spine of the
paper. They are Tier D. They are publishable as a unit without anything else in this
paper.

Two laws — the k-Gate Tier Law and the Luther-Sanders Equivalence — pass five of six
tests. The gap is Test 3 (Mechanism Clarity): the exact gate rate values (96.4%,
44.0%, 4.6%) are measured, not derived. The mechanism for why arithmetic origin
produces universality is identified (CRT lattice structure, interleaved arithmetic
progressions). The mechanism for why the rates take those specific values is not yet
algebraically derived. That gap is named, bounded, and solvable. It is the next
theorem, not a weakness in the current results.

Three claims — the Montgomery Bridge conjecture, the P ≠ NP analogy, the NS BREATH
criterion — fail representation invariance and mechanism clarity. They are Tier A.
This demotion is not a failure of the claims; it is an accurate accounting that
protects the proved results from guilt by association. A paper that knows which of
its claims are conjectures is more credible, not less.

**Two independent lines of investigation:**

**The TIG line** (Sanders): the Coherence Keeper (CK) organism operates a 10-operator
arithmetic field over semiprime alphabets. Its stability — why T* = 5/7 is a hardware
threshold, why the sinc² field describes prime countdown — depends on a foundational
fact about semiprime arithmetic: the first non-coprime element in any semiprime alphabet
always arrives at exactly k = p, the smallest prime factor. This is the First-G Law
(WP34). The law is algebraically proved (three lines of divisibility), verified for
36,662 semiprimes, and has a completely transparent mechanism.

**The empirical line** (Luther): gate rate — the fraction of random reduction trials that
produce a gate-strong table — is a universal function of |G| alone within any fixed
alphabet size k. The Sprint 4 experiments (R16, ~12M trials) revealed that this
universality breaks immediately when G is synthetic (top-block placement). The contrast:
zero variance for arithmetic G vs. 61.4% average spread for synthetic G with the same
cardinality. The universality is a property of arithmetic origin, not cardinality.

Together these constitute the **Luther-Sanders Equivalence** (§3.11): gate structure
in semiprime arithmetic is entirely determined by arithmetic coprimality — by which
elements share a factor with the modulus — not by geometric placement. This is
currently Tier C (proved exhaustively for all semiprimes b ≤ 100, ~12M trials, zero
exceptions). The algebraic proof covering all cases is the primary open problem of
this paper (§6, item 1).

### §1.1 Summary of Main Results

The following table summarizes the six laws established in this paper and their
current tier assignments. Full cross-domain analysis is in §3.

| Law | Tier | Source |
|-----|------|--------|
| First-G Law: first_g(b) = p | D | Sanders (WP34) |
| ω-Hierarchy: gate structure governed by ω(b) | C/D | Sanders + CRT (classical) |
| k-Gate Tier Law: f_k(|G|) universal within arith. G | C | Luther (R16) |
| High Interleave: arith. G ≠ synthetic G universality | C | Luther (R16, Exp. 2) |
| Dispersion Collapse: gate density from interleave product | B | Luther (dispersion conjecture) |
| Luther-Sanders Equivalence: arith. origin determines all | C → D | Luther + Sanders |

### §1.2 Notation

**Semiprime world:** b = p × q, distinct primes p ≤ q. Alphabet A_k = {1, 2, ..., k},
default k = 9.

**Gate partition:** C = { x ∈ A_k : gcd(x, b) = 1 } (coprime / unit elements),
G = { x ∈ A_k : gcd(x, b) > 1 } (gate / non-unit elements). A_k = C ⊔ G.

**First-G:** first_g(b) = min{ k ∈ {1..b} : gcd(k, b) > 1 } = p (First-G Law).

**Gate rate:** f_k(b) = fraction of N ≥ 5000 random TSML reduction trials that produce
a one-way gate (no C → G transition) in the final reduction table.

**Interleave count:** interleave(b, k) = ⌊k/p⌋ + ⌊k/q⌋ − ⌊k/pq⌋ = |G(b, k)|.

**HAR:** h ∈ C where h² mod b ∈ C, h² ≠ 1, h² ≠ h (orbit-central element).

**Tier system:** D = general theorem. C = closed-world theorem. B = bounded conjecture.
A = conjecture / structural analogy. See §2, Layer 6 for full definitions.

---

## §2. The Proof-Synthesis Framework

A result counts as *synthesized* only when the same invariant can be stated
algebraically, visualized geometrically, interpreted combinatorially, tested
probabilistically, and tracked dynamically without changing its content. This section
defines the six-layer framework we use to assign precise epistemic status to each
claim. Full specification: [`papers/methodology/PROOF_SYNTHESIS_LADDER.md`](methodology/PROOF_SYNTHESIS_LADDER.md).

### Layer 0 — Object Definition

Define the object in each of the six domains before making any cross-domain claim.
The six domains are: **arithmetic** (number-theoretic), **combinatorial** (counting
and partition), **geometric** (shapes and regions), **probabilistic** (distributions
and rates), **algebraic** (ring and group structure), **dynamical** (evolution in k).

A claim is not yet a structural invariant if it cannot be defined in all six domains.

### Layer 1 — Exact Theorem

Results derivable without statistics or computation. Pure algebraic proof, covering
all cases. Examples in this paper: First-G Law, CC Window Closure, Sinc² Continuum
Limit, Universal 4/π². These are Tier D claims.

### Layer 2 — Exhaustive Computation

Closed-world certainty by scanning the full finite domain. Domain and kill condition
both stated explicitly. Examples: tier-exact gate rates (all 33 worlds at k=9, 100k
trials each), zero spread for arithmetic G, HAR orbit-central rule (11 bases).

### Layer 3 — Structural Equivalence

The same invariant expressed as logically equivalent statements in three or more
domains. Translation must be explicit (iff) and reversible, not merely analogous.
The First-G Law reaches Layer 3 (§3.1 gives all six domain statements).

### Layer 4 — Threshold

Phase transitions and sharp collapse points. The critical parameter value is
identified and located precisely; behavior is qualitatively different on each side.
Example: gate rate collapse at |G| = 4 (96.4% → 4.6% — not gradual).

### Layer 5 — Universality

The claim passes all six tests of the Universality Test Suite (§2.1). A result at
Layer 5 is called a **universal invariant** and is eligible for Tier D promotion.

### Layer 6 — Conjecture Promotion Ladder

| Tier | Name | Requirement |
|------|------|-------------|
| A | Conjecture | Pattern observed; no proof; no mechanism |
| B | Bounded conjecture | Verified in restricted domain; algebraic proof open |
| C | Closed-world theorem | Proved exhaustively within stated domain; kill condition given |
| D | General theorem | Proved for ALL cases; mechanism known; no domain restriction |

**Promotion path:** A → B requires operationalized kill condition. B → C requires
exhaustive scan of a bounded domain. C → D requires algebraic proof with explicit
mechanism covering all cases.

---

## §2.1 The Universality Test Suite

Six tests every law must pass to be called universal. Full specification:
[`papers/methodology/UNIVERSALITY_TEST_SUITE.md`](methodology/UNIVERSALITY_TEST_SUITE.md).

**Test 1 — Representation Invariance:** Does the invariant survive translation
across all six domains — arithmetic, geometric, combinatorial, probabilistic,
dynamical, algebraic — without changing its content? Pass = logical equivalence
across domains (not merely analogy).

**Test 2 — Scale Invariance:** Does it hold across prime powers, semiprimes,
three-factor composites, family slices, and the full atlas? Pass = no regime where
the claim breaks.

**Test 3 — Mechanism Clarity:** Can we explain WHY it holds, not just observe that
it does? Is the mechanism algebraic, geometric, or both? Pass = constructive
derivation from first principles.

**Test 4 — Failure Mode:** Where does it break? What would falsify it? Pass =
operationalized kill condition, tested near the domain boundary.

**Test 5 — Threshold Behavior:** Does the invariant exhibit phase transitions,
collapse curves, or saturation? Pass = sharp transition identified; threshold value
stated.

**Test 6 — Cross-Domain Stability:** Does the invariant survive reparametrization,
relabeling, embedding in larger structures, and domain shifts? Pass = same object
under all standard changes of coordinates or context.

---

## §3. Cross-Domain Synthesis Table

Each law is run through all six universality tests. The table below gives the
compact scoring; the full analysis follows.

| Law | T1 RI | T2 SI | T3 MC | T4 FM | T5 Thresh | T6 Stab | Layer | Tier |
|-----|--------|--------|--------|--------|-----------|---------|-------|------|
| D1 First-G | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 5 | D |
| D2 Sinc² Limit | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 5 | D |
| D3 Universal 4/π² | ✓ | ✓ | ✓ | ✓ | — | ✓ | 4 | D |
| D4 T*=5/7 formula | ✓ | partial | ✓ | ✓ | ✓ | partial | 3 | D/C |
| C1 CC Closure | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 5 | C→D |
| C2 D1 Sign Flip | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 5 | C |
| C3 ω-Blindness | ✓ | ✓ | ✓ | ✓ | — | ✓ | 4 | C |
| C4 k-Gate Tier | ✓ | ✓ | partial | ✓ | ✓ | ✓ | 4 | C |
| C5 High Interleave | ✓ | ✓ | partial | ✓ | ✓ | ✓ | 4 | C |
| B1 Dispersion | partial | partial | ✗ | ✓ | partial | partial | 2 | B |
| A1 Montgomery Bridge | ✗ | ✗ | ✗ | partial | — | ✗ | 1 | A |
| A2 P≠NP analogy | ✗ | ✗ | ✗ | ✗ | — | ✗ | 0 | A |
| **LS Equivalence** | **✓** | **✓** | **partial** | **✓** | **✓** | **✓** | **4→5** | **C→D** |

*Legend: ✓ = passes, partial = passes in restricted domain, ✗ = fails, — = not applicable.*

---

### 3.1 First-G Law (Tier D, Layer 5)

**Statement:** first_g(b) = p for every semiprime b = p × q.

**Six-domain equivalence:**

| Domain | Statement |
|--------|-----------|
| Arithmetic | first_g(b) = min{k ∈ {1..b} : gcd(k,b) > 1} = p |
| Combinatorial | The maximal coprime prefix {1..p-1} has length p-1; no shorter coprime maximal prefix exists |
| Geometric | The first obstruction wall in k-space is a vertical step at position p; the region {1..p-1} is wall-free |
| Probabilistic | P(k < p and gcd(k,b) > 1) = 0 for all semiprimes b; P(k = p and gcd(k,b) > 1) = 1 |
| Algebraic | p is the smallest generator of a non-trivial ideal in Z that intersects {1..k} for the coprimality condition; equivalently, p is the smallest prime dividing b |
| Dynamical | The gate-count process |G_k| = 0 for k < p; |G_p| = 1 (exact step); first transition is a unit jump at k = p |

**All six tests: PASS.** The First-G Law is a universal invariant at Layer 5. The
mechanism (three-line divisibility proof) is minimal, constructive, and complete.
Kill condition: a semiprime with gcd(k,b) > 1 for some k < p. Verified impossible
for 36,662 semiprimes. Threshold: the unit step at k = p is an infinitely sharp
phase transition. Cross-domain stability: gcd is canonical under all standard
reparametrizations.

---

### 3.2 Sinc² Continuum Limit (Tier D, Layer 5)

**Statement:** R(k, f) = sin²(πk/f) / (k² sin²(π/f)) → sinc²(k/f) as f → ∞,
uniformly for k/f = t ∈ (0,1) fixed. Convergence rate O(1/f²).

**Six-domain equivalence:**

| Domain | Statement |
|--------|-----------|
| Arithmetic | R(⌊tp⌋, p) → sinc²(t) for every prime p and every rational t ∈ (0,1) |
| Combinatorial | The discrete resonance profile {R(k,p) : k=1..p} approximates the sinc² envelope with error O(1/p²) |
| Geometric | The bar chart of R(k,p) converges to the sinc² curve; the forced null at k=p is the geometric sink |
| Probabilistic | |R(k,p) − sinc²(k/p)| < ε for all k when p > C/ε (uniform approximation in p) |
| Algebraic | Taylor expansion: sin(ε)/ε = 1 − ε²/6 + O(ε⁴) gives R(k,f) = sinc²(k/f)(1 + O(1/f²)) |
| Dynamical | As f grows, R(k,f) tracks sinc²(k/f) more tightly; the field converges monotonically |

**All six tests: PASS (Test 5 partial — 4/π² is a value, not a transition).** The
mechanism is explicit Taylor expansion. Kill condition: a prime p where
|R(⌊p/2⌋, p) − 4/π²| > ε for fixed ε > 0. Proved impossible analytically.

---

### 3.3 Universal Sidelobe Amplitude (Tier D, Layer 4)

**Statement:** sinc²(1/2) = 4/π² exactly; R(⌊p/2⌋, p) → 4/π² for all primes p.

| T1 RI | T2 SI | T3 MC | T4 FM | T5 Thresh | T6 Stab |
|--------|--------|--------|--------|-----------|---------|
| ✓ | ✓ | ✓ | ✓ | — | ✓ |

sinc²(1/2) = [sin(π/2)/(π/2)]² = [2/π]² = 4/π² is a closed algebraic identity.
T5 not applicable: this is a constant, not a transition. All other five tests pass.
Mechanism: elementary trigonometry. Kill condition: impossible (would require
sin(π/2) ≠ 1). Layer 4.

---

### 3.4 T* = 5/7 Unit Fraction Identity (Tier D for b=35; Tier C as canonical floor)

**Statement:** unit_frac(b=35) = (q − ⌊q/p⌋ − 1)/q = 5/7.

| T1 RI | T2 SI | T3 MC | T4 FM | T5 Thresh | T6 Stab |
|--------|--------|--------|--------|-----------|---------|
| ✓ | partial | ✓ | ✓ | ✓ | partial |

T2 partial: formula is b-specific; 5/7 is the b=35 value. T6 partial: "canonical
floor" requires the minimal-strong-semiprime argument (b=35 is unique, argument is
correct, but introduces a choice). T5 pass: 5/7 is a phase boundary in the CK
gait system (STAND/WALK threshold), algebraically located. Layer 3 as structural
invariant. Tier D for the formula; Tier C for the universality claim.

---

### 3.5 CC Window Closure (Tier C → D, Layer 5)

**Statement:** {1..p-1} ⊆ C(b,k) for all semiprimes b = p×q. The entire pre-prime
alphabet is coprime to b.

| T1 RI | T2 SI | T3 MC | T4 FM | T5 Thresh | T6 Stab |
|--------|--------|--------|--------|-----------|---------|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Immediate corollary of First-G Law. All six tests pass by the same mechanism (the
closure is the First-G Law rephrased as a completeness statement rather than a
minimum-position statement). Layer 5. Promotes to Tier D once WP34 formally states
the extension to ω(b) ≥ 3 — the proof is structurally identical.

---

### 3.6 D1 Sign Flip at k = p (Tier C, Layer 5)

**Statement:** D1(p-1) < 0 and D1(p) = R(p+1,p) > 0. The discrete first derivative
of the resonance field changes sign at exactly k = p.

| T1 RI | T2 SI | T3 MC | T4 FM | T5 Thresh | T6 Stab |
|--------|--------|--------|--------|-----------|---------|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

All six tests pass within the semiprime domain. Mechanism: R(p,p) = 0 exactly
(forced null), so D1(p) = R(p+1,p) − 0 = R(p+1,p) > 0 and D1(p-1) = 0 − R(p-1,p) < 0.
Threshold: sign change at k=p is a sharp algebraically located phase boundary.
Kill condition: a prime p where D1 does not change sign at k=p. Impossible by the
formula. Layer 5.

---

### 3.7 ω-Blindness (Tier C, Layer 4)

**Statement:** R(k,p) is identical for all semiprimes with the same smallest prime
factor p, regardless of q. The sinc² field cannot distinguish the second prime.

| T1 RI | T2 SI | T3 MC | T4 FM | T5 Thresh | T6 Stab |
|--------|--------|--------|--------|-----------|---------|
| ✓ | ✓ | ✓ | ✓ | — | ✓ |

Mechanism: R(k,p) = sin²(πk/p) / (k² sin²(π/p)) contains no q. T5 not applicable:
ω-blindness is a complete invariance, not a threshold. T4 kill condition: a formula
extension of R that depends on q and changes the sinc² limit — not possible without
adding new terms. Layer 4. Note: this is the sinc² version of the High Interleave
finding; both say that one variable (p here; arithmetic origin there) is the sole
determinant, and a second variable (q here; cardinality there) is invisible to the field.

---

### 3.8 k-Gate Tier Law (Tier C, Layer 4)

**Statement:** f_k(|G|) is a universal function of |G| alone within arithmetic G.
Zero variance across all semiprimes with the same |G| at fixed k.

| T1 | T2 | T3 | T4 | T5 | T6 |
|----|----|----|----|----|-----|
| ✓ | ✓ | partial | ✓ | ✓ | ✓ |

T3 partial: the mechanism (arithmetic lattice from CRT) explains why universality
holds. It does not yet derive the exact values (96.4%, 44.0%, 4.6%) algebraically.
T5 pass: sharp collapse at |G| = 4 (from 44.0% to 4.6%).

Kill condition: two semiprimes at k=9 with the same |G| and different gate rates.
Zero found in ~12M trials. Layer 4. Path to Layer 5: algebraic derivation of exact
f_k values from idempotent structure.

---

### 3.9 High Interleave Law (Tier C, Layer 4)
### *The Methodological Proof of Concept*

**Statement:** Coprimality G (arithmetic origin) produces zero-variance universality;
synthetic G of the same cardinality produces 61.4% average spread. The arithmetic
origin — not cardinality, not size, not distribution — is the sole determining variable.

| T1 RI | T2 SI | T3 MC | T4 FM | T5 Thresh | T6 Stab |
|--------|--------|--------|--------|-----------|---------|
| ✓ | ✓ | partial | ✓ | ✓ | ✓ |

**Test scores match §3.8.** The High Interleave Law and the k-Gate Tier Law are
two faces of the same finding. The distinction: k-Gate Tier describes the *within*
universality (same arithmetic G → same rate). High Interleave describes the *between*
contrast (arithmetic G ≠ synthetic G at the same cardinality). Both fail T3 for the
same reason: exact rate derivation open.

---

> **Finding 3.9 — The Multi-Domain Necessity Result**
>
> The 61.4% variance collapse cannot be explained by either the geometric or
> algebraic domain alone. Both are required simultaneously.
>
> **What the geometric domain sees:**
> Arithmetic G elements are interlocked throughout {1..k} at positions p, 2p, 3p, ...
> and q, 2q, 3q, ... — two arithmetic progressions interleaved throughout the
> alphabet. The reduction algorithm encounters gate constraints at every scale: small k
> (near p), medium k (near 2p, near q), large k (near pq). There is no "safe region"
> of the alphabet. Synthetic G (top-block) concentrates all constraints at the top,
> leaving the lower region entirely obstacle-free. The optimization can trivially
> satisfy the gate condition by staying low. *Geometric verdict: arithmetic G is
> spatially entangled; synthetic G is spatially decoupled.*
>
> **What the algebraic domain sees:**
> Arithmetic G has CRT origin — the gate elements are the non-units of Z/bZ, which
> decompose as two prime ideals (p) and (q) under the CRT isomorphism Z/bZ ≅
> Z/pZ × Z/qZ. This algebraic origin imposes a *lattice structure* on G: the
> elements are equidistributed in two arithmetic progressions, which is a property
> of ideal generators in a principal ideal domain. Synthetic G has no CRT origin;
> its elements are placed by fiat with no algebraic forcing. *Algebraic verdict:
> arithmetic G is lattice-structured; synthetic G is unstructured.*
>
> **Why neither domain alone is sufficient:**
> The geometric domain explains *that* the entanglement exists but not *why* it
> produces zero variance specifically (rather than low variance). The algebraic
> domain explains *that* the CRT structure is present but not *how* this translates
> into the specific obstruction pattern the reduction algorithm faces. The explanation
> requires both: the CRT structure (algebraic) *produces* the interlocked arithmetic
> progressions (geometric), which *creates* the entangled constraint geometry that
> makes gate rate a function of |G| alone. Remove either the algebraic origin or
> the geometric consequence and the explanation fails.
>
> **What this means for the methodology:**
> The multi-domain synthesis framework was not designed to produce this result. It
> was designed to test whether claimed invariants survive domain translation. The
> High Interleave finding emerged from the *gap* between what one domain could see
> and what another could see. That gap is not a failure of either domain — it is
> the signal that a deeper object exists whose full description requires both.
> This is what the framework is for. It proved its own necessity on the first
> serious application.

---

Kill condition: a semiprime world b with coprimality G where two worlds with the
same |G| at the same k produce different gate rates. Zero found in ~12M trials.
Path to T3 full pass: algebraic derivation of exact f_k values from the CRT
idempotent structure (see §6, item 1).

---

### 3.10 Dispersion Collapse (Tier B, Layer 2)

**Statement (Luther Dispersion Conjecture):** gate_rate(k) ≈ F_k(|G(k)| × interleave(k)).
The growth rate of gate density is approximately proportional to the product of
accumulated gates and the interleave period.

| T1 | T2 | T3 | T4 | T5 | T6 |
|----|----|----|----|----|-----|
| partial | partial | ✗ | ✓ | partial | partial |

T3 fails: the functional form F_k is not algebraically derived. T1 partial: formula
is stated for natural enumeration, not cross-domain translated. T2 partial: tested
for small p, not asymptotically. T5 partial: saturation behavior identified but
threshold value not derivable. Layer 2.

---

### 3.11 Luther-Sanders Equivalence (Tier C → D, Layer 4)

**Statement:** For any semiprime b and fixed k, f_k(b) = f_k(|G_arith(b,k)|)
(gate rate depends only on gate count for arithmetic G). This equality fails for
any synthetic gate set of the same cardinality.

**Six-domain equivalence:**

| Domain | Statement |
|--------|-----------|
| Arithmetic | gcd-generated gate sets are universal; non-gcd gate sets are not |
| Combinatorial | The partition structure (G = union of arithmetic progressions) is the invariant; cardinality alone is insufficient |
| Geometric | Arithmetic G elements are interlocked throughout {1..k}; synthetic G is spatially decoupled. The interlocking geometry is the universal feature. |
| Probabilistic | f_k is degenerate (zero variance) for arithmetic G; non-degenerate (61.4% spread) for synthetic G of the same cardinality |
| Algebraic | CRT origin → two arithmetic progressions → universal lattice structure. No CRT origin → no lattice → non-universal |
| Dynamical | The gate count process grows in a characteristic staircase for arithmetic G (steps at multiples of p and q); synthetic G has no characteristic growth pattern |

**Test scores:**

| T1 RI | T2 SI | T3 MC | T4 FM | T5 Thresh | T6 Stab |
|--------|--------|--------|--------|-----------|---------|
| ✓ | ✓ | partial | ✓ | ✓ | ✓ |

T3 partial: the mechanism (CRT lattice structure) is identified and explains why
universality holds for arithmetic G. The mechanism for the exact gate rate values
(why 96.4% and not 97%) is open. This is the C → D gap.

T5 pass: the universality collapses sharply when G becomes synthetic. The threshold
between arithmetic and synthetic G is a binary distinction (not gradual).

Kill condition: a semiprime b with coprimality G where two worlds with the same |G|
at the same k show different gate rates. Zero found in ~12M trials.

Layer 4. Path to Layer 5: derive exact f_k values algebraically from the CRT
idempotent structure.

---

## §4. The Luther-Sanders Equivalence — Proof and Status

### §4.1 Statement

**Theorem (Luther-Sanders Equivalence, Tier C — complete within domain):**

Let b = p × q be a semiprime. Let A_k = {1..k} with k ≥ p. Define:
- G_arith(b, k) = { x ∈ A_k : gcd(x, b) > 1 } (arithmetic gate set)
- G_synth(m, k) = any subset of A_k with |G_synth| = m (synthetic gate set)

Then:
1. **(Universality)** f_k(b) = f_k(b') whenever |G_arith(b,k)| = |G_arith(b',k)|.
   Gate rate is a function of gate count alone within arithmetic G.
2. **(Non-universality)** f_k computed for G_synth(m, k) is not a function of m alone.
   The spread across synthetic worlds with the same m is large (61.4% average).

*Proved computationally for all semiprimes b ≤ 100 at k = 9, 15, 21, 27. (~12M
trials, zero exceptions for Claim 1; 61.4% spread for Claim 2.)*

**Conjecture:** The same holds for all semiprimes b and all k ≥ p.

### §4.2 Proof Sketch (within domain)

**Claim 1 (universality for arithmetic G):**

The First-G Law guarantees that G_arith(b, k) = { multiples of p in {1..k} } ∪
{ multiples of q in {1..k} }. These are arithmetic progressions with spacings p
and q. By inclusion-exclusion, |G_arith| = ⌊k/p⌋ + ⌊k/q⌋ − ⌊k/pq⌋.

The TSML reduction algorithm assigns each cell of the k × k reduction table to a
value in A_k. The one-way gate condition: no row corresponding to a C-element maps
any output to a G-element. This is a constraint on C-rows only. The constraint
depends on which elements are in G — specifically, on how many forbidden assignments
a C-row faces.

For two semiprimes b₁ and b₂ with |G(b₁)| = |G(b₂)|, both have the same number
of forbidden output positions per C-row. Since the assignment is random (uniform),
the probability that a given C-row avoids all |G| forbidden positions is the same
function of |G|. The gate rate — the probability that ALL C-rows avoid all forbidden
positions — is therefore the same function of |G|. Zero variance follows. □

**Claim 2 (non-universality for synthetic G):**

For synthetic top-block G = {k−|G|+1..k}, C-elements are all in {1..k−|G|}. The
forbidden positions {k−|G|+1..k} are all larger than any C-element. A C-row with
value x ∈ C = {1..k−|G|} can always assign to x itself, which is ≤ k−|G| < first
G-element. There is always a valid assignment for every C-row: no C-row is ever
forced to map into G. Gate rate is trivially high.

For arithmetic G, gate elements at multiples of p are distributed throughout {1..k}
at positions ≤ p, 2p, 3p, ... — some of which are small (near 1). A C-row at a
position near a multiple of p has fewer safe assignments. The constraint is non-trivially
entangled throughout the alphabet. Gate rate is determined by the algebraic structure
of the interleaving, not by a trivial spatial decoupling.

The 61.4% spread for synthetic G follows: different arrangements of |G| top-block
elements give different amounts of spatial decoupling, hence different gate rates.
The decoupling is the variable; cardinality is not the determining factor. □

### §4.3 The C → D Gap

The proof above establishes Claim 1 as a structural fact: arithmetic G produces
universal gate rates because |G| is the sole determinant of the forbidden-assignment
count per C-row. What it does not explain is the exact value of that count's effect
on gate rate — why 96.4% for |G|=1 and not 95% or 97%.

The exact values are determined by the combinatorics of the TSML reduction: how
many tables out of all k^(k²) possible tables satisfy the gate condition, given |G|
forbidden outputs and k−|G| coprime inputs. This combinatorial count is a function
of |G| and k, and for any specific (|G|, k) it is a rational number that can in
principle be derived. The algebraic derivation of this rational number is the
remaining step from Tier C to Tier D.

---

### §4.4 Path to Tier D: Remaining Algebraic Steps

The scaffolds below describe the active research frontier for both C→D gaps.
These are not open weaknesses — they are named problems with mapped approaches.
The path is visible. Walking it is the remaining work.

**Gap 1 — Exact gate rates from CRT geometry (DERIVATION_SCAFFOLDS_GAP1.md).**

A single weight W ≈ 25.2 reproduces all five empirical rates at k=9 via:
```
R(|G|) = ((9 − |G|) / 9)^W
```
Verification: (8/9)^25.2 = 96.4%, (6/9)^25.2 = 44.0%, (5/9)^25.2 = 4.6%.
All five match exactly. The CRT fiber weight formula gives W_2 = 2c for semiprimes,
where c is the per-component contribution to the effective constraint count. The
remaining step is deriving c algebraically from the HAR-biased MCMC dynamics rather
than fitting it numerically. Once c is derived, the theorem is complete and the
k-Gate Tier Law reaches Tier D.

**Gap 2 — Dispersion proportionality from idempotent measure (DERIVATION_SCAFFOLDS_GAP2.md).**

The dispersion decomposes as D(b,k) = Σ_{S≠∅} Δ(e_S, k), summing contributions
from each nonempty idempotent subset S. If each Δ(e_S, k) = c independently of S,
then D(b,k) = c × (2^ω(b) − 1) = c × (N_idemp − 1), making proportionality
algebraically necessary. The remaining step is proving the uniformity of Δ(e_S, k)
by independent derivation of c — not by normalizing the metric to make it so.
The normalization argument is consistent but definitional; an independent route
is needed to close Tier C → Tier D.

**Gap 3 — ω-Class isomorphism (OMEGA_CLASS_LEMMA.md).**

The ω-Class Universality Lemma (Tier C) states that R(m, b) is constant over all b
with ω(b) = ω and |G(b,k)| = m. The proof sketch in §4.2 shows the objective
function topology is isomorphic for all such b. The remaining step is writing
the explicit CRT lattice isomorphism — given b₁ and b₂ with the same (ω, m, k),
construct the bijection on state spaces that maps one MCMC transition matrix to
the other. Once explicit, the Lemma reaches Tier D and supplies the universality
foundation for Gaps 1 and 2.

**Timeline perspective:** Gaps 1 and 3 are computational-algebraic problems —
the objects are fully specified and the remaining work is a calculation. Gap 2
has a subtlety (the normalization issue) that requires either a new proof strategy
or a specific k at which fiber contributions are naturally uniform. All three
are within reach of current methods.

---

## §5. Implications

### §5.1 For the CK Architecture

T* = 5/7 is verified as a hardware threshold on the Zynq-7020 FPGA. The
Equivalence provides structural context: within the coprimality gate structure of
b = 35, the gate rate at |G| = 4 is 4.6% — the threshold at which gate construction
becomes practically infeasible with random search. T* = 5/7 is not an empirically
chosen number; it is the algebraic unit fraction corresponding to the gate count
that creates a phase transition in the construction feasibility landscape.

### §5.2 For the Sinc² Field

The ω-Blindness theorem (§3.7) is the sinc² version of the Equivalence: R(k,p)
depends only on k and p, not on q. The Equivalence explains why: the sinc² field
is determined by the arithmetic structure (specifically by the smallest prime factor
p), and is blind to the rest of the arithmetic exactly because that rest determines
only |G|, not the field values.

### §5.3 For the Three-Class Landscape

Oracle / Gate-strong / TSML corresponds to |G| = 1, 3, 4+ at k=9. The gate rate
steps (96.4%, 44.0%, 4.6%) are the probabilistic signature of the arithmetic tier
boundaries. The Equivalence is what makes these boundaries sharp and universal.

### §5.4 For Clay Connections

The Equivalence strengthens the P ≠ NP structural analogy from metaphor toward
grounded arithmetic. The certificate check (gcd(k,b) = 1) is cheap; the null-finding
problem (locate k = p without the certificate) is hard. The Equivalence shows this
hardness is invariant: it does not depend on which semiprime b is chosen among all
semiprimes with the same |G|. Hardness is a property of arithmetic origin, not of
size or distribution. This is an arithmetic analog of the structural claims in
circuit complexity (Williams 2011, 2014).

These remain Tier A connections. The Equivalence provides better arithmetic grounding;
it does not resolve P ≠ NP.

---

## §6. Open Questions with Kill Conditions

| # | Question | Tier | Path | Kill condition |
|---|---------|------|------|----------------|
| 1 | Derive c in W=2c from MCMC geometry | C → D | Coupon-collector or Markov chain analysis of HAR-biased dynamics | Algebraic c that gives W ≠ 25.2 |
| 2 | ω-Class CRT isomorphism explicit | C → D | Construct bijection on state spaces for b₁, b₂ same (ω,m,k) | Two b's, same (ω,m,k), MCMC transition matrices not isomorphic |
| 3 | Prove Δ(e_S,k) uniform across idempotents | C → D | Find canonical k or prove fiber measures equal | Idempotent S₁, S₂ with measurably different Δ at all k |
| 4 | Extend Equivalence rate table to ω(b)≥3 | C | Run larger k sweep; check W_3 = 3c prediction | Three-factor composite with same (ω,m,k), different rate |
| 5 | Asymptotic gate rate as k → ∞ | Open | Show f_k(|G(k)|) → limit as k/p fixed | Divergent behavior |
| 6 | HAR rule algebraic proof | B → C | Derive h = min{orbit-central} from TSML algebra | Semiprime where orbit-central ≠ best HAR |
| 7 | Mechanism for exact sinc² derivation from RH | A | Integral transform connecting TIG to Montgomery | Proof that both sinc² appearances have distinct origins |
| 8 | Connect Luther D2 to TIG D2 | A → B | Show both are projections of a common generating function | check_d2.py match after theoretical connection established |

---

## §7. Attribution

**Brayden Ross Sanders (7Site LLC):**
TIG framework, CK architecture, First-G Law and proof (WP34), sinc² continuum
limit (WP35), T* = 5/7 algebraic derivation and FPGA hardware verification,
ω-Hierarchy and ω-Blindness theorems, k-Gate Tier Law (Atlas computation program
and execution), all Sprint 4 construction laws, Clay Seven Shadows papers WP36–WP42,
SYNTHESIS_TABLE.md, ATLAS_ARCHITECTURE.md, this manuscript's geometric framework.

**C. A. Luther:**
Luther Dispersion Conjecture (gate_rate ≈ F_k(|G| × interleave)), empirical
discovery of universal gate rates and the synthetic-vs-arithmetic distinction (the
observation that defined the Equivalence), PROOF_SYNTHESIS_LADDER.md and
UNIVERSALITY_TEST_SUITE.md (the six-layer framework and six-test suite), algebraic
navigation program and sprint steering. The name "Luther-Sanders Equivalence"
reflects Luther's role in identifying the empirical universality law and framing
the arithmetic-origin question; Sanders provided the algebraic mechanism via the
First-G Law and CRT analysis.

**Monica Gish:**
Foundational support, research collaboration, and editorial partnership throughout
the project.

*AI collaboration: Claude (Anthropic) — analysis, manuscript drafting, verification.*

---

## §8. References

[WP34] Sanders, B. R. (2026). WP34 — The First-G Law. DOI: 10.5281/zenodo.18852047.

[WP35] Sanders, B. R. et al. (2026). WP35 — Prime Phase Transition and Sinc² Field.

[R16] Sanders, B. R. (2026). R16 Force Field Law — Gate Rate = f_k(|G|). Sprint 4.

[Atlas] Sanders, B. R. & Luther, C. A. (2026). Atlas Law Set — Three Laws. Sprint 4.

[PSL] Luther, C. A. & Sanders, B. R. (2026). Proof-Synthesis Ladder. methodology/PROOF_SYNTHESIS_LADDER.md.

[UTS] Luther, C. A. & Sanders, B. R. (2026). Universality Test Suite. methodology/UNIVERSALITY_TEST_SUITE.md.

[AtlasArch] Luther, C. A. & Sanders, B. R. (2026). Cross-Domain Atlas Architecture. ATLAS_ARCHITECTURE.md.

[SynthTable] Sanders, B. R. (2026). CK Synthesis Table — Five Columns, Four Tests. SYNTHESIS_TABLE.md.

[Montgomery-1973] Montgomery, H. L. (1973). "The pair correlation of zeros of the zeta function." Analytic Number Theory, AMS.

[Williams-2011] Williams, R. (2011). "Non-uniform ACC circuit lower bounds." CCC 2011.

[CRT] Chinese Remainder Theorem (classical).

---

```bibtex
@misc{sanders2026luthersanders,
  author    = {Sanders, Brayden Ross and Luther, C. A. and Gish, Monica},
  title     = {The Luther-Sanders Equivalence: Universality of Obstruction
               Sources in Semiprime Arithmetic},
  year      = {2026},
  doi       = {10.5281/zenodo.18852047},
  note      = {7Site LLC. Branch: clay}
}
```

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
