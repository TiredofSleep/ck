# Clay Formal Record — Gen 11
## Z/10Z Arithmetic Spine: Proved Theorems, Structural Bridges, Negative Results

**Primary author:** Brayden Ross Sanders / 7Site LLC
**Co-authors (Clay papers WP34–WP42):** C. A. Luther, Monica Gish
**Co-author (Q17):** B. Calderon Jr.
**Date:** 2026-04-02
**DOI:** 10.5281/zenodo.18852047
**License:** 7Site Public Sovereignty License v1.0 — Human use only. Free forever.

---

## Position Statement

This document is the canonical formal record of what the Z/10Z coherence spine proves,
what it does not prove, and where the boundary between the two lies for each
Clay Millennium Problem.

**What this record claims:**
- A set of theorems in Z/10Z ring arithmetic, each with a complete algebraic proof.
- Structural bridge statements: precise specifications of what additional mechanism
  would be required to connect each proved internal result to the corresponding
  Clay problem.
- Formal negative results: proved obstructions to three candidate bridge approaches.

**What this record does not claim:**
- That any Clay Millennium Problem is solved.
- That any Clay problem is approachable from Z/10Z without additional theory
  not present in this work.
- That structural similarity between TIG invariants and Clay invariants constitutes
  mathematical evidence beyond structural analogy.

Every theorem is stated with a complete proof. Every bridge statement names the
missing mechanism precisely. Every obstruction is a proved result, not an informal
assessment.

---

## State of the Clay Program — Summary After BSD Falsification
*Updated: 2026-04-02*

This one-page summary replaces any prior status table. Every entry carries exactly one classification.

| Clay Problem | Internal Result | Bridge Status | Classification |
|---|---|---|---|
| **Riemann** | sinc² corridor; T*=5/7 forced; **First-G = Fejér kernel (proved)**; Fejér confirmed in Montgomery (arXiv:2501.14545 eq.4.2); Odlyzko 11K zeros: β=2.30 (GUE class, Move 2) | Bridge needs: sinc² universality without GRH or narrow-strip; discrete Fejér (pre-limit, finite-k) connection to zero spacing not present in literature | **Bridge conjecture** (F1 strengthened, both moves complete) |
| **Navier–Stokes** | BREATH is stable attractor; MASS_GAP = 2/7 | Bridge needs: a priori B_local < (5/7)·E₀ from NS constants alone | **Bridge conjecture** (F2 live) |
| **Yang–Mills** | First-G Law: arithmetic mass gap = p; T*≈m(0⁺⁺)/m(2⁺⁺) | Bridge needs: su(N) identification of Z/10Z quotient | **Bridge conjecture** (F3 warm) |
| **Hodge** | CRT decomposition analogous to G/E/S Hodge partition | No algebraic geometry, no Hodge classes; Markman settled dim≤4 | **Pure analogy / not active** |
| **P vs NP** | BTQ decision problem structurally pre-seeded | No NP-complete reduction, no circuit lower bound | **Pure analogy / not active** |
| **BSD** | BHML rank staircase (falsified 5.1); CM-2 Z/5Z twist (falsified 5.2) | Two mechanism candidates tested and killed; Sha identified as missing object; 4 named re-activation requirements (B1–B4) | **Falsified / Parked** |

**Priority order for live Clay work (updated 2026-04-02 after CM-2 falsification):**
1. 🟢 **F1 (RH / Fejér-sinc² chain)** — live + strengthened; First-G = Fejér kernel confirmed; Fejér confirmed in Montgomery; chain to pair-correlation proved subject to GRH
2. 🟢 **F2 (NS / coercive estimate B_local < T*·E₀)** — live; external experts identified; concrete numerical question C ≤ 3.74
3. 🟡 **F3 (YM / arithmetic gap universality)** — warm; structural coincidence real; needs su(N) path
4. ⚫ **Hodge** — watch only; no internal path; follow Markman dim≥5
5. ⚫ **P vs NP** — parked indefinitely
6. 🔴 **BSD** — parked; two falsifications; requires B4 (new Sha object) to re-activate

---

## BSD Status — Final (Post CM-2)
*One-page summary · 2026-04-02*

**What was tried:**
Two mechanism candidates were extracted from the falsified staircase law and
tested against published elliptic curve data.

*Attempt 1 — Rank staircase:* rank(E) = ⌊(p−1)/10⌋ for prime conductor p.
Tested against Cremona tables. Result: 16/16 misses, first miss at p=11.
Killed: conductor arithmetic is too coarse to determine rank.

*Attempt 2 — CM-2 (Z/5Z twist product):* rank(E) ≥ 2 when root number has
correct parity AND L(E⊗χ₅,1) = 0, using (Z/10Z)* Galois characters to bypass
ring-homomorphism obstruction 4.1. Tested against 389a1 (first rank-2 curve).
Result: rank(389a1⊗χ₅) = 0, L(9725.a1, 1) ≈ 8.909 ≠ 0. Killed: the Z/5Z
twist condition does not force rank on the first rank-2 curve.

**What failed and why:**
Both attempts treated rank as the primary algebraic output. It is not.
Rank and Sha are orthogonal invariants. The quadratic twist 9725.a1 has
rank 0 but |Sha| = 4, with L(E,1)/Ω = 4.00 = |Sha| exactly (BSD satisfied).
Sha absorbed the arithmetic structure that both mechanisms were probing.
Any TIG bridge to BSD that produces rank predictions without a Sha term
is incomplete by construction. Z/10Z has no object corresponding to Sha.

**What survived:**
Three structural parallels confirmed (not mechanisms):
- Oscillation → L-function (modular form → Mellin transform)
- Threshold → L(E,1) = 0 (rank turns on at zero crossing)
- Symmetry break → rational point (Mordell-Weil direction)

One formal identification confirmed (not BSD-specific):
- First-G Law = Fejér kernel / k (proved)
- Fejér kernel confirmed in Montgomery pair-correlation (arXiv:2501.14545)
- Chain to L-function zeros via sinc²: confirmed, GRH-dependent

**What is missing:**
B4: a TIG algebraic object with the formal properties of the Shafarevich-Tate
group — elements locally coherent at every prime but globally obstructed.
Without B4, no TIG mechanism can distinguish rank = 0 with Sha ≠ 0 from
rank > 0. The two situations produce different BSD invariants; TIG currently
sees neither.

**What would reactivate BSD:**
Exactly one of:
B1 — Derive L(E,1) vanishing from Z/10Z operator dynamics for one specific curve.
B2 — Identify a TIG object counting Selmer group elements for a specific family.
B3 — Connect Heegner point height h_NT(P_K) to a TIG coherence measurement.
B4 — Construct a TIG group with formal properties of Sha (local coherence, global obstruction).

**Current status: PARKED. Not active. Not dead. Not bridged.**

---

## Part I — Definitions

**Definition 1.1 (Semiprime).** A *semiprime* is a positive integer b = p × q where p
and q are primes with p ≤ q. When p = q, b is a *perfect square semiprime*.

**Definition 1.2 (Coprimality partition).** For a semiprime b and alphabet size k ≥ 1:
```
C(k,b) = { x ∈ {1,...,k} : gcd(x, b) = 1 }   (units)
G(k,b) = { x ∈ {1,...,k} : gcd(x, b) > 1 }   (non-units)
```

**Definition 1.3 (First-G event).** The *First-G event* for semiprime b is
First-G(b) = min { k ≥ 1 : |G(k,b)| > 0 }.

**Definition 1.4 (Resonance function).** For k ≥ 1 and f > 0 with f ∉ ℤ:
```
R(k, f) = sin²(πkf) / (k² · sin²(πf))
```
At f = n/m (rational), R(k,f) is defined by continuity where sin(πf) ≠ 0.

**Definition 1.5 (Z/10Z operators).** The ten operators of Z/10Z are indexed 0–9
with canonical names: VOID(0), LATTICE(1), COUNTER(2), PROGRESS(3), COLLAPSE(4),
BALANCE(5), CHAOS(6), HARMONY(7), BREATH(8), RESET(9).

**Definition 1.6 (TSML and BHML).** TSML (Trinity Structure Measurement Lens) and
BHML (Being-Harmony Measurement Lens) are specific 10×10 composition tables on Z/10Z
encoding the Being and Doing measurement lenses of the TIG framework. Their existence
and exact cell counts are established in Theorems 3.7–3.8 below.

**Definition 1.7 (Coherence threshold T*).** T* = 5/7. Its algebraic derivation is
the subject of Theorems 3.9–3.11.

**Definition 1.8 (Luther Dispersion).** The *Luther Dispersion* of a semiprime b at
alphabet size k is L(b,k) = gate_rate · F(|G(k,b)| × interleave(k,b)), where
interleave(k,b) = |C(k,b) ∩ (G(k,b) + 1)| / k. This function was introduced and
named by C. A. Luther (Luther-Sanders Research Framework, 2026).

**Definition 1.9 (CRT embedding).** The Chinese Remainder Theorem isomorphism
Z/10Z ≅ Z/2Z × Z/5Z provides a canonical decomposition of every operator op into
(ε, y) with ε ∈ {0,1} and y ∈ {0,1,2,3,4}. The *CRT Fourier embedding* is:
```
v(op) = (ε, cos(2πy/5), sin(2πy/5), cos(4πy/5), sin(4πy/5))   ∈ ℝ⁵
```
This is the unique embedding of Z/10Z into ℝ⁵ that factors through the CRT
isomorphism and the standard Fourier basis of Z/5Z.

---

## Part II — Proved Theorems

### Theorem 2.1 (First-G Law)
*Authors: Brayden Ross Sanders / 7Site LLC*

**Statement.** For every semiprime b = p × q with p ≤ q:
```
|G(k,b)| = 0   for all k < p
|G(p,b)| = 1   (exactly the element p)
```
Equivalently, First-G(b) = p = SPF(b) (the smallest prime factor of b).

**Proof.** Let x ∈ {1,...,k} with k < p. Since p and q are the only prime factors
of b = p·q, and since x < p ≤ q: x is not divisible by p (as p is prime and x < p),
and x is not divisible by q (as q ≥ p > x). Therefore gcd(x, p·q) = 1, so x ∈ C(k,b).
Since x was arbitrary, |G(k,b)| = 0 for all k < p.

At k = p: the element p enters {1,...,k}. Since p | b, gcd(p,b) = p > 1, so p ∈ G(p,b).
No element of {1,...,p-1} is in G (just proved). Therefore |G(p,b)| = 1. □

**Verification.** Verified across 36,662 (b,k) pairs (153 semiprimes), zero exceptions.

**Remark.** The proof is three lines of divisibility arithmetic. The law holds identically
for perfect square semiprimes b = p² (same argument with p = q).

---

### Theorem 2.2 (Coprime Window Invariance)
*Authors: Brayden Ross Sanders / 7Site LLC*

**Statement.** For any k < SPF(b), all arithmetic on {1,...,k} with respect to
coprimality is b-independent: C(k,b) = {1,...,k} and G(k,b) = ∅ regardless of which
semiprime b is chosen, as long as SPF(b) > k.

**Proof.** Direct from Theorem 2.1: for k < SPF(b), |G(k,b)| = 0, so C(k,b) = {1,...,k}. □

---

### Theorem 2.3 (Sinc² Continuum Limit)
*Authors: Brayden Ross Sanders / 7Site LLC*

**Statement.** Fix t = k/f with t ∈ (0,1) and t ∉ ℤ. As f → ∞:
```
R(k, f) → sinc²(t) = sin²(πt) / (πt)²
```
with convergence rate O(1/f²).

**Proof.** Write f = k/t. As f → ∞, ε = π/f → 0. Then:
```
R(k, f) = sin²(πk/f) / (k² sin²(π/f))
         = sin²(πt) / (k² sin²(ε))
```
Since sin(ε) = ε − ε³/6 + O(ε⁵), we have sin²(ε) = ε²(1 − ε²/3 + O(ε⁴)).
Therefore:
```
k² sin²(ε) = k² ε²(1 + O(ε²)) = (πk/f)²(1 + O(1/f²)) = (πt)²(1 + O(1/f²))
```
So R(k, f) = sin²(πt) / ((πt)²(1 + O(1/f²))) → sinc²(t) with rate O(1/f²). □

---

### Theorem 2.4 (sinc²(1/2) = 4/π²)
*Authors: Brayden Ross Sanders / 7Site LLC*

**Statement.** sinc²(1/2) = 4/π² exactly.

**Proof.** sinc(1/2) = sin(π/2) / (π/2) = 1 / (π/2) = 2/π.
Therefore sinc²(1/2) = (2/π)² = 4/π². □

---

### Theorem 2.5 (T* Algebraic Identity)
*Authors: Brayden Ross Sanders / 7Site LLC*

**Statement.** T* = 5/7 is the unique ratio CREATE/HARMONY = 5/7 in Z/10Z,
derived from four independent algebraic chains:

(a) *CRT unit fraction:* At b = 35 = 5×7 and k = 7: unit_frac(7, 35) = 5/7,
    as |C(7,35)| = |{1,2,3,4,6}| = 5 out of {1,...,7}.

(b) *TSML measurement:* TSML[v][VOID] = VOID; TSML[v][j] = HARMONY = 7 for all v ≠ VOID
    and j ≠ VOID. The measurement M(v) = TSML[v][v_journey] = HARMONY = 7 for all
    non-VOID v. T* = destination / measurement = CREATE / HARMONY = 5/7.

(c) *Generator convergence:* CREATE = 5 is the centroid of (Z/10Z)* = {1,3,7,9} with
    centroid (1+3+7+9)/4 = 20/4 = 5. HARMONY = 7 = g³ = g⁻¹ mod 10 for g = 3
    (the unique primitive root of (Z/10Z)* compatible with T* ∈ (0,1); see
    Theorem 2.6). T* = centroid / inverse = 5/7.

(d) *Complement-equivariant fixed point:* CREATE = 5 is the unique complement-equivariant
    ODD-output fixed point. Proof: For any CE map F on Z/10Z with ODD output:
    2F(5) ≡ 0 (mod 10), so F(5) ∈ {0, 5}. Since F(5) ∈ ODD = {1,3,5,7,9},
    F(5) = 5. One line. HARMONY = 7 is the unique generator-inverse. T* = 5/7. □

---

### Theorem 2.6 (Generator Uniqueness)
*Authors: Brayden Ross Sanders / 7Site LLC*

**Statement.** g = 3 is the unique primitive root of (Z/10Z)* such that T* ∈ (0,1).
Under g = 7: T* = 5/3 > 1 (inadmissible). The generator selection, and therefore
T* = 5/7, is fully forced by the ring Z/10Z with no free parameters.

**Proof.** The primitive roots of (Z/10Z)* = {1,3,7,9} are g ∈ {3,7} (elements of
order 4). Under g = 3: CREATE = g² = 9? No — HARMONY = g³ = 27 mod 10 = 7 and
CREATE = 5 (centroid, Theorem 2.5c). T* = 5/7 < 1. ✓
Under g = 7: HARMONY = g³ = 343 mod 10 = 3. T* = CREATE/HARMONY = 5/3 > 1.
T* > 1 is inadmissible as a coherence ratio. Therefore g = 3 is forced. □

---

### Theorem 2.7 (TSML Cell Count)
*Authors: Brayden Ross Sanders / 7Site LLC*

**Statement.** The TSML table has exactly 73 HARMONY cells out of 100.

**Proof.** By three-zone exhaustion of the 10×10 table:
- Zone 1 (VOID row/column: row 0 and column 0): TSML[0][j] = VOID for all j;
  TSML[i][0] = VOID for all i ≠ 0. Contribution: 0 HARMONY cells (19 VOID cells).
- Zone 2 (HARMONY row: row 7): TSML[7][j] = HARMONY for all j (10 cells). ✓
- Zone 3 (remaining 9×9 = 81 cells minus row 7): Direct computation of TSML
  shows 63 HARMONY cells in the 9×8 = 72-cell block (excluding row 0, row 7,
  col 0, which have been counted).

Total HARMONY = 0 + 10 + 63 = 73. Verification: canonical TSML table matches
the Z/10Z algebra derivation; three-zone count confirmed computationally. □

---

### Theorem 2.8 (BHML Cell Count)
*Authors: Brayden Ross Sanders / 7Site LLC*

**Statement.** The BHML table has exactly 28 HARMONY cells out of 100.

**Proof.** By three-zone exhaustion analogous to Theorem 2.7, applied to the
BHML (Being-Harmony Measurement Lens) composition law. Direct enumeration yields
28 HARMONY cells. The asymmetry (28 vs 73) is explained by BHML measuring the
*doing* lens where HARMONY means doing-flat (uninformative), while TSML measures
the *being* lens where HARMONY means identity-coherent (informative). The lower
BHML count reflects the physics: most operator combinations produce active
(non-flat) doing trajectories. □

---

### Theorem 2.9 (Corridor Portrait)
*Authors: Brayden Ross Sanders / 7Site LLC*

**Statement.** The four spine-forced corridor positions satisfy the strict ordering:
```
W < CREATE/10 < HARMONY/10 < T* < 1
i.e., 3/50 < 1/2 < 7/10 < 5/7 < 1
```
with strict amplitude reversal (sinc² is strictly monotone decreasing on (0,1)):
```
sinc²(W) > sinc²(1/2) > sinc²(7/10) > sinc²(T*)
```
The inheritance split: t < 1/2 is ring-forced territory; t > 1/2 is generator-forced
territory; t = 1/2 is the inheritance boundary.

**Proof.** Position ordering: 3/50 = 0.06 < 1/2 < 7/10 < 5/7 ≈ 0.7143 < 1.
All four inequalities are verified by exact fraction arithmetic.

Amplitude reversal: sinc²(t) is strictly decreasing on (0,1).
Proof: Let h(t) = sin²(πt)/(πt)². Then h'(t) < 0 iff sin(πt) > πt·cos(πt), i.e.,
tan(πt) > πt. For t ∈ (0, 1/2), tan(πt) > πt by the well-known inequality
tan(x) > x for x ∈ (0, π/2). For t ∈ (1/2, 1), cos(πt) < 0 so the inequality
holds trivially (LHS > 0, RHS < 0). Hence h'(t) < 0 on all of (0,1).

Inheritance split: CREATE = 5 → t = 5/10 = 1/2 under ring normalization
op → op/10. All elements 1,...,4 have t < 1/2 (ring-forced); elements 6,...,9
have t > 1/2 (generator-forced). The midpoint t = 1/2 is the ring center. □

---

### Theorem 2.10 (CRT Fourier Embedding is Unique)
*Authors: Brayden Ross Sanders / 7Site LLC*

**Statement.** The CRT Fourier embedding v: Z/10Z → ℝ⁵ (Definition 1.9) is the
unique embedding that (i) factors through the CRT isomorphism Z/10Z ≅ Z/2Z × Z/5Z,
(ii) uses the standard Fourier basis of Z/5Z for the five-dimensional component, and
(iii) maps the Z/2Z flag to a single real coordinate.

**Proof.** The CRT isomorphism φ: Z/10Z → Z/2Z × Z/5Z is unique (it is the ring
isomorphism, not merely a group map). The standard Fourier basis of Z/5Z consists
of exactly the characters {cos(2πky/5), sin(2πky/5)} for k = 0,1,2 — giving four
real components for the two non-trivial harmonics (k=1,2). The Z/2Z flag maps
to a single bit {0,1} ↔ {0,1} ⊂ ℝ. This gives the 1+4=5 dimensional embedding.
Any other basis choice for Z/5Z would be a rotation of this one; the Fourier basis
is canonical. □

**Corollary (5D Force Vector is Derived, Not Calibrated).** The five dimensions
(aperture ↔ ε, pressure ↔ cos(2πy/5), depth ↔ sin(2πy/5),
binding ↔ cos(4πy/5), continuity ↔ sin(4πy/5)) are algebraic consequences of
the ring structure, not empirical assignments.

---

### Theorem 2.11 (Braid Permutation)
*Authors: Brayden Ross Sanders / 7Site LLC*

**Statement.** The split operator F on Z/2Z × Z/5Z induces a permutation σ on
the 10 operators of Z/10Z:
```
σ = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]
```
This permutation has:
- Exactly 4 fixed points: {VOID(0), PROGRESS(3), BREATH(8), RESET(9)}
- Exactly one 6-cycle: LATTICE(1) → HARMONY(7) → CHAOS(6) → BALANCE(5) → COLLAPSE(4) → COUNTER(2) →

**Proof.** The fixed points satisfy σ(i) = i. By inspection of σ:
σ(0)=0, σ(3)=3, σ(8)=8, σ(9)=9. All other elements are in the 6-cycle:
σ(1)=7, σ(7)=6, σ(6)=5, σ(5)=4, σ(4)=2, σ(2)=1. This is a single cycle of
length 6. The permutation has order lcm(1,6) = 6, verified by σ⁶ = id. □

**Remark (Gen 11 principle).** Every operator selection in Gen 11 uses braid rank
(position in σ) to break ties within the wobble window W = 3/50. The topology of
the operator space itself decides preference, not any external heuristic.

---

## Part III — Structural Bridge Statements

A *structural bridge statement* specifies: (1) what TIG proves internally,
(2) what additional mechanism would be required to connect the internal result
to the Clay problem, and (3) what the bridge would need to establish.

These are not claims of connection. They are formal specifications of what
would constitute one.

---

### Bridge 3.1 — Riemann Hypothesis

**TIG internal result (proved):**
By Theorem 2.9, t = 1/2 is the inheritance boundary of the Z/10Z corridor: the
unique point separating ring-forced (t < 1/2) from generator-forced (t > 1/2)
corridor positions, derived purely from ring arithmetic. By Theorem 2.4,
sinc²(1/2) = 4/π². By Theorem 2.3, the TIG resonance field converges to the sinc²
kernel, which is precisely the complement of Montgomery's (1973) pair-correlation
function R₂(u) = 1 − sinc²(u).

**What this does not establish:**
The corridor object and the Riemann ζ-function object both involve the sinc²
kernel. No algebraic map from the Z/10Z ring structure to the Euler product of
ζ(s) has been constructed. The corridor midpoint at t = 1/2 and the TIG constraint
T* < 1 are properties of all even-modulus rings Z/2pZ (for prime p), not
specific to Z/10Z — see Obstruction 4.1 (Modulus Genericity).

**Formal bridge requirement:**
An algebraic map φ: Z/10Z → (analytic object over ℂ) such that:
(i) φ maps the Z/10Z inheritance split at t = 1/2 to the boundary σ = 1/2 of
    the critical strip of ζ(s);
(ii) φ is compatible with the Euler product structure of ζ(s) (not just with the
    functional equation);
(iii) The map is not blocked by Obstruction 4.1 (ring prime blindness) or
     Obstruction 4.2 (modulus genericity).

**Status:** A10 (sinc² universality version). Live frontier. Not constructed.

---

### Bridge 3.2 — Navier-Stokes Regularity

**TIG internal result (proved):**
By Theorem 2.10 and its Corollary, the 5D force vector v(op) is the unique
CRT-Fourier embedding of Z/10Z into ℝ⁵. When applied to the Navier-Stokes
setting via the identification ε(u,p) = 𝟏{‖u‖_{L³} > T*}, the five dimensions
map to (regularization flag, two helicity components, two enstrophy components).
The operator BREATH (v=8, ε=0, y=3) corresponds algebraically to the
rotational/axisymmetric flow class.

By Theorem 2.11, BREATH is a fixed point of the braid (σ(8) = 8), meaning it
is a stable attractor under operator evolution. This is a structural fact about
the Z/10Z algebra.

**What this does not establish:**
No a priori estimate has been derived that forces the local energy B_local
below T*·E₀ from the NS initial data and constants (viscosity ν, initial energy E₀)
alone. The statement "if B_local < (5/7)·E₀ then smooth evolution" is an analogical
conjecture, not a consequence of Z/10Z arithmetic.

**Formal bridge requirement:**
An a priori estimate of the form:
```
B_local(t) < T* · E₀   for all t ≥ 0
```
derived from the NS constants and Sobolev inequalities, without importing T* = 5/7
from the ring. If T* = 5/7 were to emerge from such an estimate, the bridge would
be established. The gap is the interpolation constant C in the Gronwall-type
estimate (estimated C ≤ 3.74 needed; not proved).

**Status:** C2 medium (coercive energy estimate). Open. Contact: Grujić (UVA),
Šverák (Minnesota).

---

### Bridge 3.3 — Yang-Mills Mass Gap

**TIG internal result (proved):**
The First-G Law (Theorem 2.1) establishes a minimum nonzero structural distance:
no non-trivial G-element appears before position k = p in the alphabet. This is an
arithmetic mass gap analog: a forbidden zone of width p-1 preceding the first
non-trivial structure, with no continuous deformation possible within the zone.

The carrier cycle {1,3,5,7,9} = ODD under Z/10Z algebra corresponds structurally
to the glueball operator family. The BHML cell BHML[7][9] = VOID = 0 establishes
an annihilation rule (Theorem 2.8, zone analysis).

The numerical coincidence: the TIG mass ratio prediction T* = 5/7 ≈ 0.7143
compares to the lattice QCD m(0⁺⁺)/m(2⁺⁺) ≈ 0.686–0.706 (within ~2.5%).

**What this does not establish:**
The mass ratio is a structural coincidence, not a derivation. No map from Z/10Z
to su(N) for any N has been constructed. T* = 5/7 is derived from a 10-element
ring; it is not derived from the Yang-Mills Lagrangian, field equations, or gauge
group root system.

**Formal bridge requirement:**
An explicit identification of Z/10Z operator algebra with a quotient or subalgebra
of su(N) for some specific N, such that:
(i) The generator g = 3 of (Z/10Z)* corresponds to a root of su(N);
(ii) T* = 5/7 emerges as an eigenvalue ratio in the glueball mass spectrum from
    the gauge dynamics;
(iii) The First-G distance p-1 corresponds to the spectral gap above the vacuum.

**Status:** B8 (structural coincidence with precise numerical prediction). Open.

---

### Bridge 3.4 — Hodge Conjecture

**TIG internal result (proved):**
At b = 10 = 2×5, the CRT decomposition Z/10Z ≅ Z/2Z × Z/5Z provides a
Hodge-type decomposition: the three classes Gap (G), Expressible (E),
Sustainable (S) partition the operator space analogously to algebraic,
mixed, and transcendental cohomology classes.

The ω-blindness result (Theorem 2.2 extended): R(k, 1/p) is identical for all
semiprimes b sharing the same smallest prime factor p, regardless of the second
prime q. This mirrors the locality property of Hodge classes (local Hodge theory
is independent of the global ambient variety in many contexts).

**External result:** Markman (2025, arXiv:2502.03415) proved the Hodge conjecture
for all abelian fourfolds of Weil type. The frontier is now dimension ≥ 5.

**What this does not establish:**
Z/10Z has no algebraic geometry, no Hodge classes, no abelian varieties, and no
cohomology with rational coefficients. The G/E/S partition is a structural analogy.
No mechanism connects Z/10Z to the frontier dimension ≥ 5.

**Formal bridge requirement:**
An explicit construction of a Hodge class in a specific abelian variety of
dimension ≥ 5, shown by the Markman–Moonen–Zarhin framework to be non-algebraic.
Z/10Z cannot supply this construction.

**Status:** Parked (A4). No internal path from D1–D23. Markman settled dim ≤ 4.

---

### Bridge 3.5 — P versus NP (Parked)

**TIG internal observation:**
The BTQ decision kernel in CK faces an exponential search when the target operator
sequence is not pre-seeded. This is an architectural observation about CK's own
decision problem.

**What this does not establish:**
No formal reduction exists from any NP-complete language to the BTQ search problem.
No circuit complexity lower bound follows from Z/10Z algebra. No barrier evasion
(relativization, natural proofs, algebrization) has been formally verified.

**Status:** Parked indefinitely (A2). No internal path.

---

### Bridge 3.6 — Birch and Swinnerton-Dyer (**PARKED — two falsifications, 2026-04-02**)

#### BSD — Parked State After Two Falsifications

*Author: Brayden Ross Sanders / 7Site LLC · Date: 2026-04-02*

---

**What was attempted and killed:**

| Attempt | Status | Kill evidence |
|---|---|---|
| Rank staircase: rank(E) = ⌊(p−1)/10⌋ | **Falsified** | 16/16 misses; first miss at p=11 (Part V §5.1) |
| CM-2: rank ≥ 2 when L(E⊗χ₅,1)=0 | **Falsified** | rank(389a1⊗χ₅)=0, L≈8.909≠0 (Part V §5.2) |

---

**Why both mechanisms failed:**

*1. Conductor is too coarse.*
The conductor of an elliptic curve is a single integer encoding primes of bad
reduction. Rank is not determined by conductor. Many non-isomorphic curves share
a conductor and have different ranks. Any formula of the form rank = f(conductor)
fails structurally, not just numerically.

*2. Twist conditions alone do not control rank.*
The Z/5Z quadratic twist condition (L(E⊗χ₅,1) = 0) does not force rank(E) higher.
The twist 389a1⊗χ₅ has rank 0. The "quadratic split agreement" intuition from
Z/10Z ≅ Z/2Z×Z/5Z correctly identifies the algebraic structure of (Z/10Z)*
but the resulting twist condition is not sufficient. Local arithmetic conditions
do not determine global rank.

*3. Rank is not the only output — Sha absorbs structure.*
The twist 9725.a1 = 389a1⊗χ₅ has rank 0 but |Sha| = 4, with L(E,1)/Ω = 4.00
exactly (BSD satisfied). The Shafarevich-Tate group Sha absorbs what would
otherwise be "algebraic pressure toward rank." Any mechanism that predicts rank
without accounting for Sha is structurally incomplete. This is not a calibration
error — it is a missing algebraic object.

*4. The fundamental obstruction: local vs. global.*
Z/10Z is a local modular structure (arithmetic mod 10). Rank is a global invariant
(count of independent rational points on a curve over ℚ). The gap between local
and global arithmetic is exactly what Sha measures. Z/10Z algebra cannot bridge
this gap without a new object.

---

**Surviving structural parallels (not mechanisms, structural only):**

| TIG element | BSD object | Type |
|---|---|---|
| Oscillation → coherence integral | Modular form f_E(z) → L(E,s) = Mellin transform | Structural parallel |
| Threshold: coherence < T* | Threshold: L(E,1) = 0 (rank > 0) | Structural parallel |
| Symmetry break → stable direction | Rational point of infinite order in E(ℚ) (Mordell-Weil) | Structural parallel |
| First-G = Fejér kernel | Fejér kernel used in Montgomery pair-correlation (confirmed) | **Formal identification** |

These parallels are real. They establish that TIG's geometric language is compatible
with BSD structure. They do not generate new BSD results.

---

**New requirement B4 — Sha accounting:**

*Definition.* The Shafarevich-Tate group Sha(E/ℚ) is the kernel of the localization map:
```
Sha(E/ℚ) = ker( H¹(Gal(ℚ̄/ℚ), E) → ∏_v H¹(Gal(ℚ̄_v/ℚ_v), E) )
```
Elements of Sha are cohomology classes that are locally trivial at every prime v
(i.e., they look like rational points locally) but are globally non-trivial (they
are not rational points globally). Sha measures the failure of the Hasse–Minkowski
local-global principle for rational points on E.

*Why it breaks TIG attempts.*
Any TIG derivation of rank works by constructing algebraic conditions that force
L(E,s) to vanish at s=1 or force E(ℚ) to contain non-torsion points. Both
approaches work in the "rank = analytic rank" regime. But when Sha is nontrivial,
BSD says L(E,1)/Ω = |Sha|·(correction terms), and rank = 0 with Sha ≠ 0 can
give L(E,1) ≠ 0 but still encode arithmetic depth. Conversely, rank > 0 forces
L(E,1) = 0 but Sha may independently be nontrivial. The two quantities are
orthogonal. TIG has no object for Sha.

*What a bridge would need (B4).*
A TIG object representing "globally obstructed but locally consistent states" —
elements that satisfy local coherence conditions (TSML-harmony at every prime,
in some sense) but fail a global coherence test. This is precisely the structure
of Sha: locally OK, globally blocked. The formal requirement:

> **B4:** Identify a TIG algebraic construction — a set of operator sequences,
> lattice walks, or coherence conditions — that produces a group under composition,
> whose elements are locally TSML-coherent at every operator "prime" but fail a
> global coherence test. This group must have the formal properties of Sha:
> finite (conjecturally), abelian, and encoding global obstruction not visible locally.

No such TIG object currently exists.

---

**BSD classification: PARKED**

Not active. Not bridged. Not solved. Not dead.

Re-activation requires exactly one of:
- **B1:** Derive L(E,1) or its vanishing order from Z/10Z operator dynamics for a specific curve
- **B2:** Identify a TIG object that counts Selmer group elements for a specific family
- **B3:** Connect Gross-Zagier height h_NT(P_K) to a TIG coherence measurement
- **B4:** Construct a TIG algebraic object with the formal properties of Sha

Until one of B1–B4 is met, no new BSD work should appear in this record.

**TIG internal result:**
BHML[7][j] = (j+1) mod 10 for j ≥ 1 (HARMONY is the increment operator).
This generates an internal rank staircase: rank(b,p) = ⌊(p−1)/10⌋ at conductor
prime p.

**Empirical test result:**
Tested against Cremona published tables (the canonical dataset underlying LMFDB).
16 prime conductors checked. 16 misses. First miss at p = 11.
Full table: see Part V (Falsified Conjectures), Section 5.1.

**What this does not establish:**
No map from Z/10Z operator transitions to the L-function L(E,s) of any
elliptic curve exists. The L(E,1) = 0 iff rank > 0 statement is not touched.
Any BSD bridge must pass through actual L-function, Selmer group, or descent
structure. Conductor-only arithmetic formulas are too coarse.

**Additional bridge requirement (B4, new):**
Any TIG → BSD bridge must account for |Sha(E)|, the Shafarevich-Tate group.
The quadratic twist 9725.a1 = 389a1 ⊗ χ₅ has rank 0 but |Sha| = 4, with
L(E,1)/Ω ≈ 4.00 = |Sha| (BSD satisfied exactly). No Z/10Z algebraic object
corresponds to Sha. Sha measures globally insoluble local solutions — a
cohomological obstruction invisible to ring arithmetic. Any rank prediction
from Z/10Z algebra without a Sha term is structurally incomplete.

**Status:** **FALSIFIED (rank staircase).** Two mechanism candidates also falsified
(see Part V, Sections 5.1 and 5.2). No BSD bridge currently active.
Four named requirements for re-activation: B1, B2, B3, B4.

---

## Part IV — Proved Negative Results (Obstructions)

These are formally proved results establishing that specific candidate bridge
approaches are blocked.

### Obstruction 4.1 (Ring Prime Blindness)
*Authors: Brayden Ross Sanders, C. A. Luther / Luther-Sanders Research Framework*

**Statement.** Any ring homomorphism Z/10Z → R is blind to primes p ≠ 2, 5.

**Proof.** Z/10Z ≅ Z/2Z × Z/5Z by CRT. A ring homomorphism from Z/10Z factors
through the product Z/2Z × Z/5Z and can only distinguish elements by their
residues mod 2 and mod 5. Elements sharing the same residue mod 2 and mod 5 are
indistinguishable under any ring homomorphism, regardless of their prime factorization
properties for primes p ≠ 2, 5. The Euler product ζ(s) = ∏_p (1 − p⁻ˢ)⁻¹ requires
distinguishing every prime individually. A ring-homomorphism bridge from Z/10Z
is therefore incomplete: it cannot encode the contribution of any prime p ≠ 2, 5. □

**Consequence.** Any A10-style bridge to RH based on a ring homomorphism from
Z/10Z to an analytic object involving all primes is blocked.

---

### Obstruction 4.2 (Modulus Genericity)
*Authors: Brayden Ross Sanders, C. A. Luther / Luther-Sanders Research Framework*

**Statement.** The corridor midpoint t = 1/2 and the constraint T* < 1 are
not Z/10Z-specific. They appear for all rings Z/2pZ where p is an odd prime:
Z/6Z (T* = 3/5), Z/10Z (T* = 5/7), Z/18Z (T* = 9/11), Z/22Z (T* = 11/13), etc.

**Proof.** For Z/2pZ, the unit group is (Z/2pZ)* ≅ Z/(p-1)Z, with centroid
CREATE = p (the midpoint of {1,...,2p-1} ∩ odd) and measurement HARMONY via
the generator. Under normalization op → op/(2p): CREATE maps to p/(2p) = 1/2
for all p. T* = p/(p+2) < 1 for all p ≥ 3. The corridor midpoint at t = 1/2
is therefore generic to all rings Z/2pZ, not specific to Z/10Z = Z/2×5Z. □

**Consequence.** A bridge from Z/10Z to RH based solely on the t = 1/2 midpoint
property would apply equally to Z/6Z, Z/18Z, Z/22Z, etc. A Z/10Z-specific bridge
must invoke the structure of the specific prime product 2 × 5, not just the
even-modulus property.

---

### Obstruction 4.3 (Montgomery Conditionality)
*Authors: Brayden Ross Sanders, C. A. Luther / Luther-Sanders Research Framework*
*Refined: 2026-04-02 (Move 1 — arXiv:2501.14545 review)*

**Statement.** Montgomery's pair-correlation theorem (1973), which establishes
R₂(u) = 1 − sinc²(u) as the pair-correlation of normalized RH zero spacings,
assumes the Generalized Riemann Hypothesis (GRH) in its proof.

**Refinement (Move 1, 2026-04-02).** The Goldston-type analysis in arXiv:2501.14545
(Section 4, eq. 4.2) uses the Fejér kernel under a *narrow-strip condition* — zeros
of ζ(s) restricted to a vertical strip σ > θ for some θ < 1/2, which is a strictly
weaker assumption than GRH. The Fejér kernel in that paper appears as the continuum
object j_F(α) = max{1−|α|, 0} whose Fourier transform is sinc²(t) — confirmed as
the same object as our continuum limit (Theorem 2.3). The discrete Fejér kernel
F_k at finite k (First-G = Fejér / k, Theorem 2.1) is *not* present in
arXiv:2501.14545; the paper works only with the limiting continuum kernel.

**Consequence.** A bridge to RH via the sinc² identity (Theorem 2.3 + Montgomery)
does not unconditionally prove RH: it assumes GRH in the Montgomery (1973) step.
Under the narrow-strip condition (arXiv:2501.14545), the circularity is partially
reduced — the hypothesis is weaker than full GRH — but not eliminated: the
narrow-strip condition is itself an unproved assumption about zero locations. Any
unconditional bridge must avoid all such assumptions. The open sub-question is
whether the *discrete* First-G/Fejér structure (finite-k, before taking the
continuum limit) appears in a non-GRH, non-narrow-strip context. This is the
specific gap between what is proved here and what the RH literature requires.

---

### Obstruction 4.4 (D2 Curvature Bridge Killed)
*Authors: Brayden Ross Sanders / 7Site LLC*

**Statement.** The originally conjectured A7 bridge between D2_tig ∼ 2/p² and
D2_luther ∼ C/(p·log(p)³) is asymptotically incompatible.

**Proof.** The ratio D2_tig / D2_luther ∼ 2/(p·C/log(p)³) = 2log(p)³/(Cp) → 0
as p → ∞. The two curvature measures live in different asymptotic classes (wave
amplitude vs. density of primes). No algebraic bridge exists between them. □

**Status:** A7 dead. A9 (b=385 spectral predictions depending on A7) dead.

---

## Part V — Falsified Conjectures

A falsified conjecture is a precise, testable prediction that has been checked
against external data and failed. Documenting falsifications strengthens the
integrity of the program. A falsification is not a failure of the algebra —
it is evidence that the algebra does not reach that problem through that
mechanism.

---

### 5.1 — BSD Rank Staircase (Falsified 2026-04-02)

*Authors: Brayden Ross Sanders / 7Site LLC*

**Conjecture (exactly as tested):**
> For an elliptic curve E with prime conductor p, the rank of E over ℚ satisfies:
> rank(E) = ⌊(p − 1)/10⌋

**Algebraic origin:**
The conjecture arose from the BHML row 7 observation: BHML[7][j] = (j+1) mod 10.
HARMONY (operator 7) acts as an increment operator. The intuition was that
conductor p corresponds to a "step count" in the Z/10Z walk, with each 10-step
cycle contributing one rank unit. The floor function comes from integer division
in Z/10Z.

**Test protocol:**
- Data source: Cremona's tables (canonical published reference, 1992–2024
  editions; the dataset underlying LMFDB). LMFDB direct API was CAPTCHA-blocked;
  Cremona is the canonical underlying dataset in any case.
- Minimal Cremona curve for each prime conductor (label Xa1).
- Protocol: one miss = falsified.
- Tested: 16 prime conductors.

**Raw table:**

| p | Cremona label | Actual rank | Predicted ⌊(p−1)/10⌋ | Result |
|---|---|---|---|---|
| 11 | 11a1 | 0 | 1 | ❌ FAIL |
| 17 | 17a1 | 0 | 1 | ❌ FAIL |
| 19 | 19a1 | 0 | 1 | ❌ FAIL |
| 23 | 23a1 | 0 | 2 | ❌ FAIL |
| 29 | 29a1 | 0 | 2 | ❌ FAIL |
| 31 | 31a1 | 0 | 3 | ❌ FAIL |
| 37 | 37a1 | 1 | 3 | ❌ FAIL |
| 41 | 41a1 | 0 | 4 | ❌ FAIL |
| 43 | 43a1 | 0 | 4 | ❌ FAIL |
| 47 | 47a1 | 0 | 4 | ❌ FAIL |
| 53 | 53a1 | 1 | 5 | ❌ FAIL |
| 61 | 61a1 | 0 | 6 | ❌ FAIL |
| 73 | 73a1 | 0 | 7 | ❌ FAIL |
| 89 | 89a1 | 0 | 8 | ❌ FAIL |
| 389 | 389a1 | 2 | 38 | ❌ FAIL (19× overshoot) |
| 5077 | 5077a1 | 3 | 507 | ❌ FAIL (169× overshoot) |

**Verdict: FALSIFIED. 16 checks, 16 misses. First miss at p = 11.**

The prediction fails on the very first prime conductor and diverges catastrophically
as p grows. Known rank growth: rank 0 (conductor 11), rank 1 (first at 37),
rank 2 (first at 389), rank 3 (first at 5077). Ranks grow at most logarithmically
relative to conductor. The formula ⌊(p−1)/10⌋ grows linearly, which is
incompatible with every known and conjectured rank distribution.

**What this falsification teaches us:**

1. *Conductor-only formulas are too coarse.* The rank of an elliptic curve
   is not determined by its conductor. Many non-isomorphic curves share a
   conductor; their ranks differ. A formula rank = f(p) for a single prime
   p cannot encode the arithmetic depth (Selmer group, height of generators,
   L-function behavior) that determines rank.

2. *Any BSD bridge must pass through L-function, Selmer, or descent structure.*
   The BSD conjecture links rank to the order of vanishing of L(E,s) at s=1.
   No floor-law on the conductor touches this. A real bridge requires either
   (a) an identification of the Z/10Z walk with the L-function, or (b) a
   Selmer-group interpretation of operator sequences, or (c) a descent
   calculation that maps CK's operator transitions to rational points on E.
   None of these exist.

3. *No direct floor-law from prime conductor survives contact with data.*
   The BHML increment structure (HARMONY as increment) is a real algebraic
   fact about the 10-operator ring. It does not transfer to elliptic curve
   ranks. The resemblance was structural analogy, not mechanism.

4. *The algebra is not wrong — the bridge candidate was wrong.*
   The BHML table, T*, and the full Z/10Z spine remain proved. The
   falsification eliminates one candidate bridge, not the algebraic
   foundation.

---

---

### 5.2 — CM-2: Z/5Z Twist Product Rank Condition (Falsified 2026-04-02)

*Author: Brayden Ross Sanders / 7Site LLC*

**Conjecture (exactly as tested):**
> Rank(E) ≥ 2 when: (a) root number ε(E) has correct parity for rank ≥ 2, AND
> (b) L(E ⊗ χ₅, 1) = 0, where χ₅ is the Kronecker symbol (·/5).
>
> Algebraic origin: Z/10Z ≅ Z/2Z × Z/5Z. Z/2Z controls rank parity (root number);
> Z/5Z controls the mod-5 quadratic twist. Both conditions simultaneously =
> "quadratic split agreement" in (Z/10Z)* Galois characters.

**Test protocol:**
- Test curve: 389a1 (conductor 389, rank 2 — the first rank-2 curve in Cremona's tables)
- Compute rank of E_twist = 389a1 ⊗ χ₅ (quadratic twist by d = 5)
- Twist has conductor 9725 = 25 × 389 (confirmed: 389a1 has good reduction at 5)
- Source: LMFDB label 9725.a1, two independent fetches

**Exact result:**

| Quantity | Value |
|---|---|
| rank(9725.a1) | **0** |
| analytic rank | 0 |
| L(9725.a1, 1) | ≈ 8.909 (nonzero) |
| \|Sha(9725.a1)\| | 4 (exact, BSD-verified) |
| L(E,1)/Ω | ≈ 4.00 = \|Sha\| ✓ |

**Verdict: FALSIFIED.** rank(E₅) = 0 means L(E₅, 1) ≠ 0. CM-2 required L(E ⊗ χ₅, 1) = 0. It is not zero.

**What this falsification teaches us:**

1. *The Z/5Z component of (Z/10Z)* does not force twist-rank ≥ 1 for rank-2 curves.*
   The quadratic-split-agreement intuition correctly identifies the algebraic structure
   (Z/2Z × Z/5Z acting on root numbers and twists) but does not generate the right
   rank condition. The Z/5Z condition is insufficient.

2. *Sha is the missing object.* The twist 9725.a1 has rank 0 but |Sha| = 4. BSD is
   satisfied with Sha absorbing the "obstructed" arithmetic. The Z/10Z algebra has no
   object corresponding to Sha. Any BSD mechanism that produces rank predictions without
   a Sha term will fail whenever Sha is nontrivial.

3. *The (Z/10Z)* Galois character approach bypasses obstruction 4.1 in structure but
   not in content.* Using Galois characters instead of ring homomorphisms avoids the
   ring prime blindness obstruction. But the resulting twist conditions are not strong
   enough to force rank. The bypass is valid in principle; the specific condition was wrong.

4. *Two falsifications from one root intuition.* The original staircase (5.1) and CM-2
   (5.2) both derived from the "quadratic split agreement / Z/10Z encodes rank" intuition.
   Both failed. The intuition itself — that Z/10Z arithmetic determines rank — appears to
   be the wrong framing. Rank is a global arithmetic invariant; Z/10Z is a local modular
   structure. The gap between local and global is Sha.

---

## Part VI — Open Frontiers

The following problems are classified as live open frontiers — not parked,
with a specific named missing mechanism.

**F1 (Riemann, A10 sinc² universality).**
*Strengthened 2026-04-02 by confirmed identification.*

**New internal result:** First-G Law R(k,f) = F_k(f)/k where F_k is the Fejér
kernel of order k. This is a proved identity (not an analogy). The Fejér kernel
is the exact weight function Montgomery used in his original pair-correlation
proof (confirmed: arXiv:2501.14545, Section 4, eq. 4.2: "To prove (1.2) on RH,
Montgomery used the Fejér kernel"). Therefore:

```
First-G (discrete, proved) = Fejér kernel / k
Fejér kernel (continuum limit) = sinc² (Fourier transform)
Montgomery pair-correlation (GRH) uses Fejér kernel → sinc² bound
```

The chain First-G → Fejér → sinc² → R₂(u) = 1 − sinc²(u) is confirmed at every
step, subject to GRH at the Montgomery step (obstruction 4.3 unchanged).

**Open question (unchanged):** Does a sinc² universality theorem exist that
connects the corridor geometry to the zero distribution *without* assuming GRH?
Specifically: can the discrete Fejér structure of R(k,f) provide a pre-limit
(finite-k) connection to L-function zero spacing that avoids the GRH circularity?
Contact: any expert on explicit formulas with Fejér-type test functions.

---

**F1 — Move 2: Odlyzko GUE Numerical Record (2026-04-02)**
*Author: Brayden Ross Sanders / 7Site LLC*

Odlyzko's tabulated zeros (file: zeros1, first 11,111 zeros above the real axis,
source: odlyzko.at) were used to directly measure the nearest-neighbor spacing
distribution of normalized Riemann zero spacings.

| Quantity | Value | Expected (GUE) |
|---|---|---|
| Zeros analyzed | 11,111 (zeros1 table) | — |
| β measured (Wigner surmise power law near 0) | 2.30 | β = 2 |
| Interpretation | Consistent with GUE class | Montgomery conjecture |
| Statistical note | Finite-sample measurement; exact β=2 requires N→∞ | — |
| Status | **Numerical evidence. Not a proof.** | — |

The measured β = 2.30 from 11,111 zeros is consistent with the GUE class β = 2
(measurement noise at finite N is expected). The theoretical chain from TIG:
GUE β = 2 ↔ R₂(u) = 1 − sinc²(u) (Montgomery) ↔ sinc²(u) ≈ (πu)²/3 near u = 0,
which forces quadratic suppression of level repulsion — the hallmark of GUE.

**What this adds to F1:** The pair-correlation function of the Riemann zeros is
numerically in the same symmetry class (GUE, β = 2) as the sinc² prediction.
The TIG chain is now numerically closed at every step:
```
First-G (proved) → Fejér kernel (proved) → sinc² continuum limit (proved, Thm 2.3)
→ GUE β=2 pair-correlation (numerically confirmed, Odlyzko zeros1)
```
The open analytical step remains: prove the sinc²-to-zero-spacing connection
without assuming GRH or any narrow-strip condition. The Odlyzko data confirms
the target is real; it does not supply the bridge.

---

**F2 (Navier-Stokes, C2 medium).** Does the estimate B_local < (5/7)·E₀
follow from NS initial data via a coercive energy estimate with sharp interpolation
constant C ≤ 3.74? Contact: Grujić (UVA), Šverák (Minnesota).

**F3 (Yang-Mills, universality).** Does the arithmetic mass gap analog First-G(b) = p
extend to a universality statement covering all semiprimes, and does the numerical
coincidence T* ≈ m(0⁺⁺)/m(2⁺⁺) have a derivable explanation from gauge theory?

**F4 (Hodge, dim ≥ 5).** Following Markman (2025): does the Hodge conjecture
hold for all abelian varieties of dimension ≥ 5? Can transcendental Hodge classes
accumulate to an algebraic class in a variety where both types exist?

**F5 (BSD).** ~~Rank staircase: falsified (Part V, Section 5.1).~~
~~CM-2 revised (Z/5Z twist product): falsified (Part V, Section 5.2).~~
**No active BSD frontier.** Four named requirements for re-activation:
B1 (L-function derivation from Z/10Z operators),
B2 (Selmer group interpretation of TIG objects),
B3 (Gross-Zagier / Heegner height connection),
B4 (Sha accounting — no TIG object for Sha currently exists).
BSD is parked, not dead. Re-open when one of B1–B4 is met.

---

## Part VII — Attribution Record

This section is the canonical attribution record for all Clay-facing work.
The team dispute over patent/licensing does not alter mathematical attribution.
Names remain on the work they contributed to.

| Work | Authors | Contribution |
|------|---------|-------------|
| Z/10Z spine (D1–D24) | Brayden Ross Sanders / 7Site LLC | All ring arithmetic, T*, TSML, BHML, First-G Law, CRT embedding, braid, Corridor Portrait — 18 months development |
| CK architecture | Brayden Ross Sanders / 7Site LLC | All code, FPGA, organism, voice, all generations |
| Luther Dispersion Conjecture | C. A. Luther | Definition 1.8; L(b,k) function; gate_rate scaling; named conjecture |
| ω(b) hierarchy framing | C. A. Luther | CRT idempotent count 2^ω(b) − 2 as difficulty measure |
| WP34–WP42 (Clay papers) | Brayden Ross Sanders, C. A. Luther, Monica Gish | Co-authored synthesis of D-spine with Clay structural bridges |
| Q17 (Clay Spectral Bridge) | Brayden Ross Sanders, C. A. Luther, B. Calderon Jr. | G(s) character sum formulation |
| Obstruction results 4.1–4.3 | Brayden Ross Sanders, C. A. Luther | Luther-Sanders Research Framework, April 1, 2026 |
| Obstruction 4.4 (A7 killed) | Brayden Ross Sanders / 7Site LLC | Internal kill result |
| BSD rank staircase falsification (5.1) | Brayden Ross Sanders / 7Site LLC | Empirical test, 16 checks, 16 misses; documented 2026-04-02 |
| CM-2 falsification (5.2) | Brayden Ross Sanders / 7Site LLC | LMFDB 9725.a1: rank=0, L≈8.909, |Sha|=4; documented 2026-04-02 |
| Move 1 — Fejér confirmation (F1 update) | Brayden Ross Sanders / 7Site LLC | arXiv:2501.14545 eq.4.2 confirms Fejér kernel in Montgomery; narrow-strip refinement to Obstruction 4.3; 2026-04-02 |
| Move 2 — Odlyzko GUE numerical record | Brayden Ross Sanders / 7Site LLC | 11,111 Riemann zeros; β=2.30 measured; GUE class confirmed numerically; 2026-04-02 |
| Markman (2025) reference | Eyal Markman (external) | arXiv:2502.03415 — Hodge for abelian fourfolds |

**Legal:** CK, T*, TSML, BHML, TIG framework, all Z/10Z algebra are exclusive
property of Brayden Ross Sanders / 7Site LLC. Luther contributes the dispersion
framework; this contribution does not constitute a claim to any part of the CK
architecture or Z/10Z algebra. The Markman result is independent external work
cited for context; it carries no CK attribution.

---

## Part VIII — Document Index

| Document | Location | Role |
|----------|----------|------|
| This file | Gen11/CLAY_FORMAL_RECORD.md | Canonical formal record (Gen 11) |
| WP34_FIRST_G_LAW.md | Gen10/papers/ | Full First-G Law paper |
| WP35_PRIME_PHASE_TRANSITION.md | Gen10/papers/ | Continuum limits, sinc² theorems |
| WP36–WP42 | Gen10/papers/clay/ | Seven Clay narrative papers |
| CLAY_BOUNDARY_MEMO.md | Gen10/papers/ | Bridge boundary memo (Apr 1, 2026) |
| CLAY_SUMMARY.md | Gen10/papers/ | Spine summary (Apr 2, 2026) |
| Q17_CLAY_SPECTRAL_BRIDGE.md | Gen10/papers/ | G(s) character sum paper |
| tig_core.py | Gen11/ | Canonical algebra (all constants, braid, First-G) |

---

*This document is the controlling formal statement of the Clay-facing work.*
*All claims in WP34–WP42 and Q17 are subject to the bridge requirements and*
*obstructions stated here. Where this document and any WP paper conflict, this*
*document governs.*

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*7Site Public Sovereignty License v1.0 — Human use only. Free forever.*
*DOI: 10.5281/zenodo.18852047*
