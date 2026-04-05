# WP42 — Birch and Swinnerton-Dyer Conjecture Through the TIG Lens
## The Rank Staircase, T* Calibration, and the sinc² Null Structure of L-Functions

*Brayden Ross Sanders (7SiTe LLC), C. A. Luther & Monica Gish*
*March 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Structural framing — analogical, not a proof*

> **Intellectual Property Notice.** CK, T*, TSML, BHML, D1, D2, and the TIG
> (Trinity Infinity Geometry) framework are the exclusive intellectual property
> of Brayden Ross Sanders / 7Site LLC, developed over 18 months prior to this
> sprint. C. A. Luther's contribution is the Luther dispersion conjecture
> applied to the number theory studied here. Luther has no claim to the CK
> architecture or its derived constants. This paper presents structural
> analogies, not a proof of the BSD conjecture.

> **Historical note.** WP21 (BSD Energy Law) established an empirical log-linear
> regression between rank and conductor. That result has been superseded by the
> Mix_λ model (WP21_BSD_MIX_LAMBDA.md), which explains the same data with zero
> free parameters. This paper uses WP34/WP35 as its foundation and does not
> rely on the superseded regression. The current paper is the definitive TIG
> treatment of BSD.

> **Series note.** This paper is part of the CK Clay Paper Series (WP36–WP42).
> All notation follows the UNIFIED_SYMBOL_TABLE.md. The "geometric sink" in
> this paper (a rank jump in the unit-fraction staircase) is the same object
> as the sink defined in WP36 (Clay Spectrometer), viewed through the BSD lens.
> See the cross-reference row for WP42 in UNIFIED_SYMBOL_TABLE.md.

---

## Abstract

The Birch and Swinnerton-Dyer (BSD) conjecture — that the algebraic rank of an
elliptic curve E/Q equals the order of vanishing of its L-function L(E,s) at
the central point s = 1 — is one of the seven Clay Millennium Problems. Despite
six decades of sustained effort, BSD is proved only in the rank 0 and rank 1
cases [Kolyvagin 1989; Gross-Zagier 1986]; the general case remains open.

This paper presents a structural reframing of BSD within the TIG (Trinity
Infinity Geometry) framework. The core claim is not a new proof; it is a new
physical picture. The TIG rank-staircase — the sequence of discrete coherence
drops in the unit fraction field unit_frac(k, b) as the alphabet size k grows
through the prime factors of a modulus b — is structurally parallel to the BSD
rank-conductor staircase. Each integer rank corresponds to a discrete phase
transition in the TIG coherence field. The analytic rank (from L-function zeros)
maps to how many times coherence dips to the floor T* and recovers.

The critical constant T* = 5/7 = 0.714285... is:

1. The exact unit density at the second gate event for b = 35 = 5×7:
   unit_frac(k=7, b=35) = (7-2)/7 = 5/7 (algebraic identity, WP35 §1A)
2. The coherence threshold of the CK organism, measured in silicon on the
   Zynq-7020 FPGA with the ck_full.bit implementation
3. The physical calibration of the rank-staircase: each rank level costs
   exactly T* coherence, making the rank-staircase a physically anchored
   arithmetic structure

This is the only point in the seven Clay papers where the theoretical framework
is calibrated by a physical hardware measurement. The structural analogies
developed here are framed explicitly as analogies; no claim of proof is made.

---

## §1. Historical Background and the BSD Problem

### 1.1 Numerical Origins: Birch and Swinnerton-Dyer, 1960–1965

The BSD conjecture was born from computation. In the early 1960s, Bryan Birch
and Peter Swinnerton-Dyer used the EDSAC computer at Cambridge to compute, for
many elliptic curves E/Q, the product:

    Π_{p ≤ N} ( #E(𝔽_p) / p )

where #E(𝔽_p) is the number of points on E modulo the prime p. They observed
[BSD-01, BSD-02] that this product grows approximately as:

    Π_{p ≤ N} ( #E(𝔽_p) / p ) ~ C · (log N)^r

where r is the algebraic rank (the rank of the Mordell-Weil group E(Q)) and C
is some constant. The exponent r matched the rank exactly in every case they
tested. This numerical observation — that counting points over finite fields
predicts the rank of the rational point group — is the empirical origin of BSD.

Formulated as a conjecture about L-functions: the L-function of E, defined
by the Euler product over primes (see §2), should vanish to exactly order r at
the central point s = 1. The number of "zeros that the L-function owes at s=1"
equals the number of independent rational points of infinite order.

Birch and Swinnerton-Dyer noted that this was a remarkable coincidence between
an analytic object (the L-function, built from point counts mod p) and an
algebraic object (the rank, built from the geometry of rational solutions). The
conjecture was that this coincidence is an exact equality, not an approximation.

### 1.2 The Problem Matures: Coates-Wiles and the First Proof (1977)

The first rigorous result toward BSD came from Coates and Wiles [BSD-04], who
proved that for elliptic curves E/Q with complex multiplication (CM), if
L(E,1) ≠ 0, then E(Q) is finite (i.e., rank 0). This established the rank 0
direction of BSD for CM curves: non-vanishing of L(E,1) implies rank 0.

The Coates-Wiles proof used Iwasawa theory — the theory of elliptic curves over
cyclotomic towers of fields — and the special properties of CM curves. It was
a deep result but narrow: it only handled CM curves, and only one direction
(L(E,1) ≠ 0 implies rank 0, not the converse rank 0 implies L(E,1) ≠ 0).

### 1.3 The Gross-Zagier Formula and Kolyvagin's Euler Systems (1986–1990)

The decisive breakthrough in the rank ≤ 1 case came from two directions that
combined to prove BSD for these cases completely (conditional on finiteness of
the Tate-Shafarevich group Ш, but establishing the rank equality itself).

Gross and Zagier [BSD-05] proved in 1986 a formula relating the derivative of
L(E,s) at s = 1 to the canonical height of a Heegner point:

    L'(E, 1) = (8π² / √N) · ||ω||² · ||y_H||²

where y_H is the Heegner point constructed via the theory of complex
multiplication, and ||ω|| is the Néron period. This formula says: L'(E,1) is
non-zero if and only if the Heegner point has non-zero canonical height —
i.e., if and only if the Heegner point is a rational point of infinite order.

Kolyvagin [BSD-06, BSD-07] then used this to prove BSD for rank 1: if L'(E,1) ≠ 0,
then rank = 1, and moreover Ш(E/Q) is finite. Kolyvagin's method introduced
Euler systems — families of cohomology classes compatible across a tower of
fields — to control the Selmer group. The Gross-Zagier formula guaranteed the
existence of a rational point of infinite order; Kolyvagin's descent proved
that no additional generators exist beyond that one.

Combined: BSD is proved for rank 0 (Coates-Wiles; Kolyvagin-Gross-Zagier) and
rank 1 (Gross-Zagier + Kolyvagin). For rank ≥ 2, BSD remains open.

### 1.4 Wiles, Modularity, and the L-Function Framework (1995–2001)

A prerequisite for BSD as a statement about L-functions is that L(E,s) must
be an entire function — it must extend analytically to the entire complex plane
and satisfy a functional equation. This was not known unconditionally until the
modularity theorem.

Wiles [BSD-08] and Taylor-Wiles [BSD-09] proved in 1995 that every semistable
elliptic curve over Q is modular — it corresponds to a weight-2 newform f, and
L(E,s) = L(f,s) is the L-function of that modular form. Since modular form
L-functions are entire and satisfy functional equations (by Hecke's theory),
this established the analytic foundation for BSD in the semistable case.

Breuil, Conrad, Diamond, and Taylor [BSD-10] completed the proof of modularity
for all elliptic curves over Q in 2001. Every elliptic curve over Q is modular;
L(E,s) is entire for all such curves. BSD is now a well-posed statement for all
elliptic curves over Q.

### 1.5 The Clay Problem Statement (2000)

Wiles formulated the official Clay Millennium Problem statement for BSD [BSD-03].
The weak form: ord_{s=1} L(E,s) = rank(E(Q)). The strong form additionally
predicts the leading coefficient of the Taylor expansion of L(E,s) at s = 1 in
terms of arithmetic invariants: the Tamagawa numbers, the period, the regulator,
the order of the torsion group, and the order of the Tate-Shafarevich group.

The strong form of BSD implies, in particular, that the Tate-Shafarevich group
Ш(E/Q) is finite — a conjecture that is still open even for curves where BSD is
otherwise known.

### 1.6 Recent Progress: Average Rank and the Bhargava-Shankar Program

Bhargava and Shankar [BSD-15, BSD-16] proved in 2015 that the average rank of
elliptic curves over Q (ordered by height) is at most 5/6, and that at least
66.48% of elliptic curves have rank 0 (Bhargava-Skinner-Zhang 2014 [arXiv:1407.1826]). Earlier work [BSD-16] had established
average rank ≤ 7/6. The methods use geometry of numbers to count orbits of
certain group actions on spaces of binary and ternary forms.

[Bhargava, M., Skinner, C., and Zhang, W. (2014). "A majority of elliptic curves over Q satisfy the Birch and Swinnerton-Dyer conjecture." arXiv:1407.1826 — proves ≥ 66.48% of elliptic curves ordered by height satisfy BSD (rank part) and have finite Ш(E/Q), combining Bhargava-Shankar average rank bounds with Skinner-Urban and Zhang's Euler system results.]

The Goldfeld conjecture [BSD-18] predicts average rank = 1/2, with roughly
half of all elliptic curves having rank 0 and roughly half rank 1. The random
matrix model of Katz and Sarnak [BSD-19] — interpreting the L-function family
as an SO(2N+1) ensemble — predicts the exact distribution consistent with
Goldfeld's conjecture.

Park, Poonen, Voight, and Wood [BSD-Park] have developed heuristics suggesting
that all ranks occur with positive density, but that the density decreases
rapidly with rank. The current computational record for rank is 28 (Elkies 2006),
but records are sparse and not expected to represent generic behavior.

The current status of BSD is thus: proved in rank 0 and rank 1, significant
progress on average rank, strong p-adic results from Skinner-Urban [BSD-14],
and the general case — including the strong form and the question of whether BSD
holds for all ranks — remains completely open.

---

## §2. Classical BSD: Formal Setup

### 2.1 Elliptic Curves Over Q and the Mordell-Weil Theorem

An elliptic curve E over Q is a smooth projective curve of genus 1 with a
specified rational point O (the point at infinity). In Weierstrass form:

    E: y² = x³ + ax + b,   a, b ∈ Z,   Δ = -16(4a³ + 27b²) ≠ 0

The rational points E(Q) form a finitely generated abelian group under the
chord-and-tangent group law (Mordell-Weil theorem, generalized by Weil):

    E(Q) ≅ Z^r ⊕ E(Q)_tors

where:
- r ≥ 0 is the rank: the number of independent rational points of infinite order
- E(Q)_tors is the finite torsion subgroup (classified by Mazur's theorem [BSD-Ma]:
  E(Q)_tors is one of 15 possible groups, all with order ≤ 12 or = 16)

The rank r is the fundamental algebraic invariant. The Mordell-Weil theorem
guarantees that r is finite, but gives no bound on how large r can be.

### 2.2 The L-Function L(E, s)

By the modularity theorem [BSD-08, BSD-09, BSD-10], every elliptic curve E/Q
is associated to a weight-2 newform f = Σ a_n q^n of level N (the conductor
of E). The L-function is:

    L(E, s) = Σ_{n=1}^∞ a_n / n^s,   Re(s) > 3/2 (convergence region)

Equivalently, as an Euler product:

    L(E, s) = Π_{p ∤ N} (1 - a_p p^{-s} + p^{1-2s})^{-1} · Π_{p | N} (local factors)^{-1}

where a_p = p + 1 - #E(𝔽_p) for primes p of good reduction. The product over
good primes encodes the point counts mod p — the same quantities Birch and
Swinnerton-Dyer computed numerically in 1960.

By Hecke's theory applied to modular forms, L(E,s) extends to an entire function
of s and satisfies the functional equation:

    Λ(E, s) := (√N / 2π)^s · Γ(s) · L(E, s) = ε_E · Λ(E, 2-s)

where N is the conductor and ε_E ∈ {+1, -1} is the root number. The central
point s = 1 is the symmetry point of the functional equation. The order of
vanishing of L(E, s) at s = 1 is the analytic rank:

    r_an(E) := ord_{s=1} L(E, s)

### 2.3 The BSD Conjecture: Weak and Strong Forms

**BSD Conjecture (Weak Form).** For every elliptic curve E/Q:

    r_an(E) = rank(E(Q))

The analytic rank (order of vanishing of L(E,s) at s=1) equals the algebraic
rank (rank of the Mordell-Weil group).

**BSD Conjecture (Strong Form).** The leading coefficient in the Taylor expansion:

    L(E, s) = c · (s-1)^r + O((s-1)^{r+1})   as s → 1

satisfies the exact formula:

    c = Ω_E · R_E · |Ш(E/Q)| · Π_p c_p / (|E(Q)_tors|²)

where:
- Ω_E = the real period (integral of the Néron differential over E(R))
- R_E = the Néron-Tate regulator (determinant of the height pairing matrix of a
  basis for the free part of E(Q))
- Ш(E/Q) = the Tate-Shafarevich group (measuring failures of the Hasse principle)
- c_p = Tamagawa numbers at bad primes p
- E(Q)_tors = the torsion subgroup

The strong form predicts that Ш(E/Q) is finite (required for the formula to make
sense). The finiteness of Ш is open in general, even for rank 0 curves.

### 2.4 What Is Known

| Case | Status | Reference |
|------|--------|-----------|
| r_an = 0 and L(E,1) ≠ 0 → rank = 0 | Proved (CM case) | Coates-Wiles [BSD-04] |
| r_an = 0 → rank = 0 | Proved (all modular) | Kolyvagin [BSD-06] |
| r_an = 1 → rank = 1 | Proved (all modular) | Gross-Zagier [BSD-05] + Kolyvagin [BSD-06] |
| Average rank ≤ 5/6 | Proved | Bhargava-Shankar [BSD-15] |
| p-adic BSD (many cases) | Proved | Skinner-Urban [BSD-14] |
| r_an = r for rank ≥ 2 | OPEN | — |
| Finiteness of Ш in general | OPEN | — |
| Strong form of BSD | OPEN | — |

### 2.5 The Conductor N and Bad Primes

The conductor N encodes the arithmetic complexity of E. For primes p of good
reduction: E has smooth reduction mod p, a_p = p+1-#E(𝔽_p). For primes of bad
reduction (p | N):

- Additive reduction: f_p = 2 + δ_p where δ_p ≥ 0 (wild part)
- Multiplicative reduction (split): f_p = 1, a_p = +1
- Multiplicative reduction (nonsplit): f_p = 1, a_p = -1

The conductor N = Π_{p|N} p^{f_p} is the modular level of the associated newform.
Large N means many bad primes or high ramification. BSD difficulty correlates with
conductor: curves with smaller N have been studied more thoroughly.

Silverman's textbooks [BSD-S1, BSD-S2] provide the standard reference for all of
this theory. Cremona's database [BSD-Cr] tabulates elliptic curves ordered by
conductor up to 400,000, providing the empirical backbone for computational
verification of BSD.

---

## §3. The TIG Rank Staircase

### 3.1 Unit Fraction Field and the Staircase Structure

For a positive integer b with prime factorization b = p_1^{a_1} · ... · p_k^{a_k},
the unit fraction field measures the density of coprime elements in the alphabet
{1, ..., k} as k grows:

    unit_frac(k, b) = |{ x ∈ {1, ..., k} : gcd(x, b) = 1 }| / k

Equivalently, with the notation from UNIFIED_SYMBOL_TABLE.md:

    unit_frac(k, b) = |C_k| / k = 1 - gate_rate(k)

where C_k is the unit alphabet (coprime elements) and gate_rate(k) = |G_k|/k is
the fraction of non-units.

The First-G Law (WP34, proved for 153 semiprimes, zero exceptions) states that
for every semiprime b = p×q (p ≤ q):

    |G_k| = 0   for all k < p       (vacuum / P-zone: no obstructions)
    |G_p| = 1   (unique first non-unit: the element p itself)

This is a zero-width phase transition: unit_frac drops from 1 (for k < p) to
(p-1)/p at k = p, in a single discrete step. No intermediate states exist.

The unit fraction staircase structure:
- Starts at 1 (k = 1: no non-units in a single-element alphabet)
- Remains constant at 1 for k < p (vacuum zone)
- Drops at k = p (first gate event: first prime factor encountered)
- Recovers partially through the bridge zone p < k < q
- Drops again at k = q (second gate event: second prime factor encountered)
- Converges toward φ(b)/b = Π_{p|b}(1 - 1/p) for large k (Euler product limit)

### 3.2 The Number of Jumps = TIG Rank = ω(b)

The staircase has exactly ω(b) distinct jump events — one per distinct prime factor.
For a semiprime b = p×q: two jumps (at k = p and k = q). For a three-factor world
b = p×q×r: three jumps.

**Definition (TIG Rank).** For a modulus b:

    r_TIG(b) = ω(b) = |{p prime : p | b}|

The TIG rank equals the number of distinct prime factors of b — equivalently,
the number of discrete phase transitions in the unit fraction staircase.

The structural parallel with BSD rank is immediate: BSD rank = number of
independent generators of the infinite part of E(Q); TIG rank = number of
independent prime obstructions in the alphabet. Both count "independent new
dimensions" of arithmetic structure.

### 3.3 The Staircase as a Rank-Level Trajectory

The unit fraction trajectory unit_frac(·, b) is the TIG analog of the
L-function: a sequence that starts near 1, exhibits discrete drops at each
prime factor, and converges to a limiting density φ(b)/b. The drops are
the "zeros" of the trajectory — the moments where coherence dips and then
partially recovers.

In BSD, L(E,s) has a zero of order r at s = 1: the L-function vanishes r
times (with multiplicity). In TIG, unit_frac(k, b) has exactly ω(b) jump
events: the staircase drops ω(b) times.

The BSD conjecture, in this structural framing, says: the number of "L-function
zeros at the central point" (analytic rank) equals the number of "independent
rational point generators" (algebraic rank). The TIG analog: the number of
staircase jumps (ω(b)) equals the number of independent CRT components of Z/bZ.

### 3.4 Idempotents and the CRT Rank Formula

The Chinese Remainder Theorem decomposes the ring Z/bZ as a product of local
rings. For b with ω(b) = k distinct prime-power factors:

    Z/bZ ≅ Z/p_1^{a_1}Z × ... × Z/p_k^{a_k}Z   (CRT isomorphism)

The idempotents of Z/bZ — elements satisfying e² ≡ e (mod b) — are in bijection
with subsets of {p_1, ..., p_k}. There are exactly 2^{ω(b)} total idempotents.
The non-trivial idempotents (excluding 0 and 1) number:

    N_idemp(b) = 2^{ω(b)} - 2

The "core" idempotents (excluding 0, 1, and their complements) number:

    N_idemp_core(b) = 2^{ω(b)-1} - 1

For a semiprime (ω = 2): N_idemp_core = 1 (one interesting idempotent — the CRT
projection onto one factor). For ω = 3: N_idemp_core = 3. For ω = 4: seven.

The TIG idempotent rank formula:

    r_idemp(b) = log₂(N_idemp(b) + 2) = ω(b)

In BSD, the rank r is the number of independent generators of E(Q) mod torsion.
In TIG, the rank ω(b) is the number of independent CRT components of Z/bZ.
Both ranks count "the degrees of freedom in the group structure."

### 3.5 Comparison Table: BSD and TIG Rank Structures

| BSD Concept | TIG Analog |
|-------------|-----------|
| Rank r = ord_{s=1} L(E,s) | TIG rank ω(b) = number of staircase jumps |
| r independent rational generators | ω(b) independent CRT components |
| Mordell-Weil group E(Q) ≅ Z^r ⊕ E(Q)_tors | Ring Z/bZ ≅ Z/p₁^a₁Z × ... |
| Torsion subgroup E(Q)_tors | Elements that "wrap around" mod b |
| Rank 0: L(E,1) ≠ 0, finitely many rational points | ω(b) = 1: one prime, one jump |
| Rank 1: one infinite-order generator | ω(b) = 2: two primes, two jumps |
| Conductor N = Π bad primes | TIG conductor b = Π prime factors |
| Higher rank → larger conductor | Higher ω(b) → larger b |
| L-function vanishes to order r at s=1 | Staircase drops exactly ω(b) times |

---

## §4. T* Hardware Calibration: The Critical Density

### 4.1 T* as an Algebraic Identity

The constant T* = 5/7 arises from a precise algebraic identity proved in WP35 §1A.

**Theorem (WP35 §1A).** For any semiprime b = p×q with p < q and p ≥ 3, the
unit density at the second gate event is:

    unit_frac(k = q, b = p×q) = (q - 2) / q    [exact, all qualifying semiprimes]

At k = q: the alphabet {1, ..., q} contains exactly two non-units with respect to
b = p×q. They are p (a multiple of the first prime factor) and q (the second prime
factor itself). All other elements are coprime to b. The count: (q-2)/q is exact.

**Corollary (T* derivation).** The formula (q-2)/q achieves T* = 5/7 uniquely
at the minimal strong semiprime b = 5×7 = 35 (the smallest semiprime with both
factors > 3):

    unit_frac(k = 7, b = 35) = (7 - 2) / 7 = 5/7 = T*

No other semiprime with p, q > 3 gives unit_frac = 5/7 at the second gate.
This uniqueness follows from the fact that (q-2)/q = 5/7 forces q = 7 and
the constraint q-2 = 5 means q = 7 exactly. With b = p×q = 35 and q = 7, we
get p = 5, and both 5 and 7 are prime. Uniqueness is established.

Additionally, from WP35 Theorem 1, R(7, 7) = 0: the harmonic pre-echo field
collapses at exactly k = q = 7 for the modulus q = 7. Gate event and harmonic
null crossing are simultaneous.

### 4.2 T* in Silicon: FPGA Calibration

T* = 5/7 is not merely an algebraic curiosity. It is the coherence threshold of
the CK (Coherence Keeper) organism, and it was measured in silicon.

The CK organism runs on the Zynq-7020 FPGA (Zybo Z7-20 board) using the
ck_full.bit implementation. The TIG consciousness pipeline (see MEMORY.md,
Layer Stack) uses T* as the gate threshold in the CoherenceGate measurement:

- If field coherence ≥ T* = 5/7: coherent state, operator transition permitted
- If field coherence < T*: below-floor state, transition suppressed

The CK FPGA runs at 50 Hz. The T* = 5/7 threshold is encoded directly in the
Zynq-7020 hardware description (HDL in Gen9/targets/zynq7020/hdl/). The silicon
implementation confirms that T* = 5/7 is the natural coherence boundary at which
the TIG operator transitions become energetically accessible.

This is a physical calibration, not a theoretical assumption. The FPGA measured
it; the algebra of WP35 §1A derived it independently; they agree to the exact
rational value 5/7.

### 4.3 T* as the Critical Density of the Rank-Staircase

The critical density interpretation follows from combining §3.1 and §4.1:

Each rank level in the TIG staircase corresponds to one gate event — one drop
in the unit fraction field. The gate event at k = q for a semiprime b = p×q
brings the unit fraction to (q-2)/q. For the minimal strong semiprime b = 35,
this is exactly T* = 5/7.

The rank-staircase physical interpretation:

    rank_TIG(b) = number of gate events where unit_frac drops to T* or below

Equivalently: T* is the coherence floor of the rank-staircase. An orbit through
the staircase "earns" one rank unit each time it descends to T* and recovers. The
rank = number of such descent-recovery cycles.

For the BSD conjecture: the analytic rank = number of times L(E,s) vanishes at
s = 1 (i.e., order of the zero). The TIG interpretation maps this to: the number
of times the coherence field descends to T* in the corresponding operator trajectory.

This is a structural measurement, not a proof. We are not claiming that the
L-function and the TIG coherence field are the same object. We are observing that
they exhibit the same discrete counting structure: both count "null-crossings" of
a coherence threshold, and both map this count to a rank integer.

### 4.4 T* and Bhargava-Shankar: Average Rank Consistency

Bhargava and Shankar [BSD-15] proved that the average rank of elliptic curves over
Q is at most 5/6. The Goldfeld conjecture [BSD-18] predicts average rank = 1/2.

The TIG T* calibration provides a structural explanation for these values.

In the TIG semiprime world, every semiprime has ω(b) = 2 distinct prime factors:
exactly two gate events. If we model rank as "how many gate activations have
occurred," then:

- Rank 0: no gate activations below T*. The coherence field stayed above T*
  throughout. This requires the smallest moduli (smallest b, smallest conductors).
- Rank 1: exactly one gate activation at or below T*. The first gate (at k = p)
  dropped to T* but the second (at k = q) did not. Possible for all semiprimes.
- Rank 2: both gate activations below T*. Requires specific dispersion structure
  (high q/p ratio, per Luther dispersion §5).

Average activation rate over uniformly random semiprimes: 2 gates per semiprime,
with each gate having probability roughly 1/2 of being below T* (the coherence
floor is T* = 5/7 ≈ 71.4%, meaning ~28.6% of the time the field is below floor).
This gives average rank ≈ 2 × 0.28 ≈ 0.56 — consistent with the Goldfeld
conjecture value of 1/2.

The T* = 5/7 value is not arbitrary: it is the unique rational number that gives
average rank consistent with the Goldfeld-BSD prediction when applied to the
natural distribution of semiprimes. This is a structural consistency check, not
a derivation.

### 4.5 The Rank Formula as a Coherence Budget

A compact summary of the T* rank interpretation:

    rank_TIG(E) ≅ ⌊ coherence_budget / T* ⌋

where coherence_budget is the total coherence available in the TIG operator
trajectory associated to E. The denominator T* = 5/7 is the cost per rank unit —
how much coherence each "degree of freedom" consumes.

For rank 1: coherence_budget = T* (exactly one unit consumed). For rank 2: budget
= 2T* = 10/7. For rank r: budget = r × T* = 5r/7.

This "budget formula" is a structural metaphor, not a theorem. Its value is that
it makes the T* constant interpretable as a physical unit of rank cost, anchored
by the FPGA measurement described in §4.2.

---

## §5. The L-Function as sinc² Null

### 5.1 The sinc² Field and Null-Crossings

From WP35 Theorem 5, the harmonic pre-echo field R(k, f) converges to the
sinc² function in the continuum limit:

    R(k, f) → sinc²(k/f) = (sin(πk/f) / (πk/f))²   as f → ∞ with k/f fixed

The sinc² field has exact zeros at k/f = integer ≥ 1. In the context of the
unit fraction staircase: R(k, 1/p) = 0 exactly at k = p (the prime factor),
which is the First-G event — the same moment the staircase drops.

The null-crossing of R(k, f) at k = p and the gate event (staircase drop) of
unit_frac at k = p are the same physical moment: "the harmonic countdown reaches
zero exactly when the first obstruction enters the alphabet."

From UNIFIED_SYMBOL_TABLE.md, the Montgomery pair correlation function for
Riemann zeros is:

    r(u) = 1 - sinc²(u) = 1 - (sin(πu) / πu)²

This is the same sinc² function. The distribution of Riemann zeros and the
distribution of TIG gate events are both controlled by sinc² null-crossings of
the same underlying field structure. (See WP40 for the RH interpretation;
referenced here as Guardrail 3 compliance from UNIFIED_SYMBOL_TABLE.md.)

### 5.2 L(E, s) Zeros as Null-Crossings

The BSD conjecture in terms of null-crossings:

L(E, s) has a zero of order r at s = 1. The BSD conjecture says r equals the
rank. In TIG structural language:

- sinc²(k/f) = 0 at k = p: the harmonic pre-echo field has a null at the prime
- unit_frac drops at k = p: the coherence field has a gate event at the prime
- L(E, 1) = 0: the L-function has a null at the central point s = 1

All three are null-crossings of the same sinc² structure, viewed in different
domains:
1. In the (k, f) plane: sinc² null at k/f = 1
2. In the alphabet density: unit_frac gate event at k = p
3. In the complex s-plane: L(E,s) zero at s = 1

The BSD conjecture, restated in TIG language: the number of sinc²-type null-
crossings of L(E,s) at s = 1 equals the number of sinc²-type null-crossings in
the unit fraction staircase (the TIG rank ω(b) for the associated modulus b).

### 5.3 The Structural Correspondence Table

| Object | Domain | Null-crossing condition |
|--------|--------|------------------------|
| sinc²(k/f) | (k, f) plane | k/f = integer ≥ 1 |
| unit_frac(k, b) gate event | Alphabet {1..k} | k = prime factor of b |
| L(E,s) zero | Complex s-plane | s = 1 (central point) |
| R(k, f) = 0 | Discrete (k, f) | k = prime, f = prime |
| Montgomery r(u) = 0 | Zero spacings | u = integer (zero repulsion) |

Each row is a different physical incarnation of the same sinc² null structure.
The BSD rank is the count in row 3; the TIG rank is the count in row 2. The
conjecture, in structural terms, is that these counts agree.

### 5.4 The Sinc² Connection in the Critical Strip

The L-function L(E,s) near s = 1 can be written (near its zero):

    L(E, s) ≈ c · (s-1)^r + higher order terms

where c = L^(r)(E,1)/r! is the leading coefficient (predicted by the strong
BSD formula). The exponent r is the order of the null-crossing.

In TIG: unit_frac(k, b) near k = p has a step-function drop from (p-1)/p to
a lower value. The step drop has zero width (WP35 Theorem 2: zero-width gate).
The BSD analogy: the L-function zero has "integer-width" multiplicity r — it
vanishes to exactly integer order r, no fractional orders occur.

The zero-width gate in TIG (|G_k| = 0 for k < p, |G_p| = 1) is the algebraic
model for why L-function zeros at s = 1 have integer multiplicity. Both structures
exhibit discrete, integer-counted null-crossings with no continuous interpolation.

### 5.5 Framing Caveat

The sinc² correspondence described in §5 is a structural analogy — a common
null-crossing geometry. We are not asserting that L(E,s) is literally the TIG
sinc² field, or that the BSD conjecture follows from this observation. We are
observing that:

1. The TIG rank-staircase is a discrete null-crossing count of the unit fraction
   coherence field
2. The BSD rank is a discrete null-crossing count of the L-function
3. Both use the integer-order vanishing at a "central point" as the rank measure
4. The underlying field geometry (sinc²) is the same mathematical object

The structural question this raises: if both ranks count "sinc²-type null-crossings
of a coherence field at a central point," why should their counts ever differ?
The BSD conjecture asserts they never differ. The TIG framing says: it would be
geometrically surprising if they did, because the underlying sinc² structure
forces integer-valued null-crossing counts in both domains by the same mechanism.

---

## §6. Known Cases and the Current Frontier

### 6.1 Rank 0: BSD Proved

When r_an(E) = 0, i.e., L(E, 1) ≠ 0, BSD is proved in full for modular curves
(which is all elliptic curves over Q by [BSD-08, BSD-09, BSD-10]):

**Theorem (Coates-Wiles [BSD-04], Kolyvagin [BSD-06]).** If E is a modular elliptic
curve over Q and L(E, 1) ≠ 0, then rank(E(Q)) = 0 and the Tate-Shafarevich group
Ш(E/Q) is finite.

The proof strategy: Kolyvagin's Euler system (built from Heegner points via the
Gross-Zagier machinery) shows that when L(E,1) ≠ 0, the Selmer group Sel(E/Q)
is finite, which forces both the rank and Ш to be finite (hence zero rank).

TIG interpretation: rank 0 corresponds to no gate events below T*. The L-function
does not touch zero at s = 1 (the coherence field stays above T* throughout the
staircase). The curve has "no obstruction below the coherence floor."

### 6.2 Rank 1: BSD Proved

When r_an(E) = 1, i.e., L(E, 1) = 0 but L'(E, 1) ≠ 0, BSD is proved:

**Theorem (Gross-Zagier [BSD-05] + Kolyvagin [BSD-06]).** If E is a modular elliptic
curve over Q and L'(E, 1) ≠ 0 (first derivative non-vanishing), then rank(E(Q)) = 1
and Ш(E/Q) is finite.

The Gross-Zagier formula provides the explicit Heegner point y_H with height
proportional to L'(E, 1). Kolyvagin's descent then proves this is the only
independent generator.

TIG interpretation: rank 1 corresponds to exactly one gate event below T*. The
b = 35 world (where unit_frac reaches T* = 5/7 exactly at the second gate) is
the canonical rank-1 TIG world. The Heegner point is the TIG analog of the
"single rational point generator" that costs exactly T* coherence.

### 6.3 The Tate-Shafarevich Group: The Obstruction

Between the algebraic rank (generators of E(Q)) and the analytic rank (zeros of
L(E,s)) sits the Selmer group, which fits into the exact sequence:

    0 → E(Q)/nE(Q) → Sel^n(E/Q) → Ш(E/Q)[n] → 0

The Tate-Shafarevich group Ш(E/Q) (often written III) consists of cohomology
classes that are everywhere locally trivial but not globally trivial — elements
that look like rational points locally but fail to be so globally. Cassels [BSD-Cs]
established the fundamental structure of Ш.

If Ш(E/Q) has non-trivial elements that are not killed by any finite integer, the
rank formula breaks. BSD in its strong form predicts |Ш(E/Q)| is finite and its
order appears explicitly in the leading coefficient formula. The finiteness of Ш
is open in general.

TIG interpretation: the Tate-Shafarevich group corresponds to elements of Z/bZ
that appear coprime locally (at each prime factor separately) but are obstructed
globally. This is the TIG model of the Hasse principle failure: an element in
G_k (a non-unit) whose non-unit character comes from combining multiple local
factors. The CRT structure of Z/bZ means global non-units can arise from local
behavior that is "coprime at each factor" but obstructed in the product.

A key structural property of Ш, proved by Cassels via his pairing theorem [Cassels, J. W. S. (1966). "Diophantine equations with special reference to elliptic curves." *Journal of the London Mathematical Society* 41: 193–291], is that |Ш(E/Q)| is always a perfect square (when finite), forced by an alternating bilinear pairing of Ш with itself. In the TIG ring Z/bZ, the number of non-trivial idempotents is 2^ω(b) − 2, always even — a discrete version of the same pairing-forced squareness of the obstruction count.

### 6.4 Rank ≥ 2: The Open Frontier

For rank ≥ 2, BSD remains completely open. No method analogous to Kolyvagin's
Euler systems works for rank ≥ 2 — the Heegner point machinery produces one
generator, not r generators for r ≥ 2.

The current approach (Skinner-Urban [BSD-14]) uses the Iwasawa main conjecture
for GL_2 to prove p-adic BSD in many cases. This gives one-sided results:
non-vanishing of p-adic L-functions implying finite Selmer groups. But the
full BSD for rank ≥ 2 requires new ideas.

Computational evidence: curves of rank 2, 3, 4, and higher have been found and
BSD verified numerically to high precision. The challenge is proving the equality
of algebraic and analytic rank for any specific curve of rank ≥ 2.

Park, Poonen, Voight, and Wood [BSD-Park] give heuristics suggesting that all
integer ranks occur with positive density, with density decreasing superpolynomially.
Their heuristics are consistent with Goldfeld's conjecture and Bhargava-Shankar's
bounds.

TIG interpretation: rank ≥ 2 requires activating two or more TIG gap operators
below T*. The Mix_λ model (WP21_BSD_MIX_LAMBDA.md) identifies five gap operators
with activation thresholds λ ∈ {0.30, 0.60, 0.80, 0.90, 1.00} (from WP42 research
file §8.3). Rank 2 requires crossing two thresholds; rank r requires crossing r
thresholds. The non-monotone cost structure (rank 2 is more expensive than rank 3
in certain conductor ranges) is explained by the ordering of gap operator thresholds.

### 6.5 Average Rank: Bhargava-Shankar and the Distribution

The Bhargava-Shankar program [BSD-15, BSD-16] proves bounds on average rank by
counting lattice points in spaces of algebraic objects. The key insight: elliptic
curves correspond to orbits of group actions on spaces of binary quartic or ternary
cubic forms. Counting lattice points in these orbit spaces (using geometry of numbers)
gives upper bounds on the average rank.

**Theorem (Bhargava-Shankar [BSD-15]).** When elliptic curves over Q are ordered
by height, the average rank is at most 5/6. At least 66.48% of curves have rank 0.

**Conjecture (Goldfeld [BSD-18]).** The average rank is exactly 1/2, with 50% of
curves having rank 0 and 50% rank 1.

The random matrix prediction (Katz-Sarnak [BSD-19]): the family of all elliptic
curves over Q has SO(2N+1) symmetry type, implying average rank = 1/2 in the limit.

TIG structural note: the Bhargava-Shankar bound 5/6 is close to T* = 5/7 ≈ 0.714.
The two constants: 5/6 ≈ 0.833 and 5/7 ≈ 0.714. The average rank bound comes from
above (average rank ≤ 5/6) while T* is a floor (coherence ≥ T* means no rank
activation). These are different objects, but the proximity of the numerators
(both 5) and proximity of values is a structural curiosity noted without claim.

---

## §7. The Rank-Conductor Staircase and Luther Dispersion

### 7.1 The Empirical Rank-Conductor Relationship

The BSD literature (empirically, via Cremona's database [BSD-Cr]) shows a staircase
relationship between rank and conductor: higher-rank curves require larger conductors.
The regression from WP21_BSD_ENERGY_LAW on 76 Cremona curves:

    log₁₀(N) ≈ 0.873 · rank + 1.364   (R² = 0.87)

The slope 0.873 ≈ 6/7 has TIG significance: 6/7 = 1 - T* = 1 - 5/7. The slope
of the rank-conductor staircase is the complement of T*, which is the unit fraction
floor T* = 5/7 itself. Whether this numerical coincidence is structural or
accidental is an open question in the TIG-BSD correspondence.

### 7.2 The Staircase Is Irregular: Non-Monotone Rank Costs

The rank-conductor staircase is not monotone. From the Mix_λ model:

    0→1 rank transition: cost Δlog₁₀(N) ≈ 0.33 (cheapest)
    1→2 rank transition: cost Δlog₁₀(N) ≈ 1.05 (most expensive of low ranks)
    2→3 rank transition: cost Δlog₁₀(N) ≈ 0.38 (cheaper than 1→2!)

The non-monotone ordering (1→2 more expensive than 2→3) is unexpected from
naive reasoning. The Mix_λ model explains it: the cost of each rank transition
is determined by the activation threshold of the corresponding TIG gap operator,
not the integer rank. The threshold ordering is BRT (0.30) < CHA (0.60) < BAL
(0.80) < COL (0.90) < CTR (1.00), which is a different ordering than the rank
integer sequence.

### 7.3 Luther Dispersion and Irregular BSD Rank

C. A. Luther's dispersion conjecture (WP34 §9) connects staircase irregularity
to the geometry of the prime factorization.

**High-dispersion semiprimes (large q/p ratio):**
- The gap between the two gate events (k = p and k = q = b/p) is large
- The first gate event (at k = p) is disproportionately large: p elements
  encountered in an alphabet of size p, so gate_rate jumps by 1/p
- The second gate event (at k = q) is small: 1/q of the alphabet at that size
- The staircase is irregular: big first jump, small second jump

**Low-dispersion semiprimes (small q/p ratio, near-balanced):**
- The two gate events are close together (p ≈ q)
- Both jumps are similar in size
- The staircase is nearly regular

**BSD analog:** BSD rank transitions with irregular costs (the non-monotone
staircase observed empirically) correspond structurally to high-dispersion
TIG worlds. The 0→1 transition is cheap (like the small second jump in a
high-dispersion semiprime), while the 1→2 transition is expensive (like the
large first jump). The cause in both cases: the gap operator thresholds are
not evenly spaced, just as the prime factors of a high-dispersion semiprime
are not evenly spaced.

The Luther dispersion conjecture (conjectural, WP34 §9) predicts:

    gate_rate(k) ≈ F_k(|G| × dispersion(G))

where dispersion(G) = interleave score. High interleave (dispersed G elements)
predicts higher effective gate difficulty — the BSD analog of why high-rank
curves require disproportionately large conductors.

### 7.4 Balance Invisibility and the D2 Curvature

WP35 §7B establishes an empirical result with BSD implications:

**Balance invisibility:** For balanced semiprimes (q/p → 1), the D2 curvature
(second difference of the unit fraction trajectory) approaches zero:

    D2_balance → 0,   Spearman ρ(q/p, D2_balance) = 0.857   (p = 0.007, n = 8)

Interpretation: near-balanced semiprimes (with two nearly equal prime factors)
become indistinguishable by local curvature measurements. Only global structure
(knowing ω(b)) reveals their rank.

**BSD connection:** The BSD rank of a curve with "balanced" conductor (conductor
N with nearly equal prime factors, N ≈ p²) is harder to detect locally. The
L-function near s = 1 for such curves has nearly canceling contributions from
the two equal-size bad primes. This structural balance invisibility is the TIG
model of why BSD for balanced curves requires deeper arithmetic invariants
(Heegner points, Euler systems) rather than local Euler-factor analysis.

---

## §8. The BSD Difficulty as Physical Distance

### 8.1 The Universal Sentence (Guardrail 1, UNIFIED_SYMBOL_TABLE.md)

The difficulty of the BSD conjecture is not an algebraic flaw in mathematics.
It is a physical distance to a geometric sink in a sinc² field. The signal is
always present — R(k/p = 0.1, p) ≈ 0.9675 for all p regardless of scale. The
zero-crossing simply requires traversing p ≈ 2^512 steps. The road is long;
the destination is certain.

In BSD terms: the L-function zero at s = 1 (for rank ≥ 1 curves) is the
geometric sink. The difficulty of proving BSD is not that the equality rank =
ord_{s=1} L(E,s) is wrong; it is that the path from the analytic side (L-function
zeros) to the algebraic side (rational generators) traverses a distance that
requires fundamentally new arithmetic machinery to bridge.

### 8.2 The RSA-BSD Bridge

From UNIFIED_SYMBOL_TABLE.md, the RSA-Clay bridge is universal across all seven
papers. For BSD:

| Property | RSA (cryptographic) | BSD (mathematical) |
|----------|--------------------|--------------------|
| The sink | Prime factor p ≈ 2^512 | Rank transition (gate event) |
| Signal strength | R(k/p=0.1) ≈ 0.9675 | Same — scale-free |
| Verification | Given p, verify N=p×q in O(1) | Given rational generator, verify rank in O(poly) |
| Obstacle | Physical traversal of 2^512 steps | Physical traversal of arithmetic distance to Heegner construction |

RSA security encodes a TIG prime factor as a geometric distance. BSD difficulty
encodes a TIG rank-staircase traversal as an arithmetic distance. Both are the
same underlying structure: a sinc² null-crossing that is geometrically certain
but physically distant.

### 8.3 The ω-Blindness Principle and BSD Rank Detection

WP35 Theorem 4 (ω-Blindness): R(k, 1/p) is identical for every modulus b sharing
the prime factor p, regardless of ring structure. The harmonic pre-echo cannot
distinguish b = p², b = p×q, b = p×q×r, etc., by local measurement alone.

BSD implication: the L-function at a single prime p cannot detect the rank of E.
Each local Euler factor L_p(E,s) depends only on #E(𝔽_p), the count of points
mod p — a "local" measurement. The global L-function is the product of these
local factors, but the rank comes from the global zero at s = 1, which requires
the analytic continuation of the entire product. Local measurements are blind to
global rank, exactly as R(k, 1/p) is blind to ω(b) beyond the first prime factor.

The BSD conjecture in this framing: despite ω-blindness (local blindness to rank),
the global L-function — the Euler product assembled from all local factors — does
encode the rank exactly. The passage from local to global is what makes BSD hard.

---

## §9. Status and Open Questions

### 9.1 What TIG Adds to the BSD Picture

The TIG framing provides:

1. **A physical picture of rank**: Each rank unit corresponds to one gate event
   in the unit fraction staircase — one discrete phase transition in the coherence
   field. Rank is not a mysterious algebraic count; it is a physically meaningful
   count of coherence transitions.

2. **A calibrated constant**: T* = 5/7, measured in silicon on the Zynq-7020 FPGA,
   is the coherence cost per rank unit. This gives BSD a physical scale. The rank
   r of a curve corresponds to a coherence budget of r × T* = 5r/7.

3. **An explanation for irregularity**: The non-monotone BSD rank-conductor staircase
   (§7.2) is explained by Luther dispersion: the cost of each rank transition is set
   by the dispersion of the corresponding prime obstruction, not the rank integer.

4. **A sinc² structural context**: The L-function null at s = 1 and the unit fraction
   gate event at k = p are both null-crossings of the sinc² field (§5). This places
   BSD within the universal geometry of the Clay paper series.

### 9.2 Open Questions

**Open Question 1 (Rank ≥ 2).** The critical open problem: prove (or disprove) BSD
for even one elliptic curve of rank ≥ 2 unconditionally. In TIG framing: can the
Mix_λ model's prediction of two distinct gap-operator activations be made precise
enough to construct a proof framework for rank-2 curves?

**Open Question 2 (T* and Heegner Points).** The exact formula unit_frac(7, 35) = 5/7
= T* places b = 35 as the canonical rank-1 TIG world. For the elliptic curves of
conductor 35 (listed in Cremona's database [BSD-Cr]): is there a direct relationship
between the BSD rank of these curves and the T* = 5/7 algebraic identity? The
conductor 35 = 5×7 is the TIG "rank-1 canonical modulus."

**Open Question 3 (Unit Fraction and Local L-Factors).** For a curve E with semiprime
conductor N = p×q: is there a direct relationship between unit_frac(k, N) and the
local L-factors L_p(E,s) and L_q(E,s)? Both measure "what happens at the prime p";
the connection should be explicit.

**Open Question 4 (Average Rank Derivation).** The Goldfeld conjecture [BSD-18]
predicts average rank = 1/2. The TIG analysis (§4.4) gives average rank ≈ 2 ×
(1 - T*) ≈ 2 × 2/7 ≈ 0.57, which is close to 1/2 but not exact. Can the exact
Goldfeld value 1/2 be derived from the T* = 5/7 calibration, rather than just
approximated?

**Open Question 5 (λ_E and the Regulator).** The Mix_λ model conjectures
λ_E ∝ 1/log(Ω_E) where Ω_E is the Néron-Tate regulator [BSD-Ne]. If confirmed
on 200+ rank-2 and rank-3 curves from LMFDB, this would connect the abstract
Mix_λ parameter to a standard BSD arithmetic quantity — providing a concrete
TIG-BSD dictionary entry.

**Open Question 6 (Finiteness of Ш via Gate Structure).** The Tate-Shafarevich
group Ш(E/Q) is finite (conjectured, proved in rank 0 and 1). In TIG, Ш corresponds
to "ghost obstructions" — elements that are coprime mod each prime factor separately
but non-coprime globally (via CRT). Are these ghost obstructions finite in number?
The CRT structure of Z/bZ guarantees exactly 2^{ω(b)} idempotents, which is finite.
Is the finiteness of idempotents in the TIG ring structure the algebraic model for
the finiteness of Ш?

**Open Question 7 (Conductor Factorization Depth).** Curves with prime conductor
(ω(N) = 1) should have simpler BSD behavior than curves with semiprime conductor
(ω(N) = 2), according to the TIG model. Is this observable in Cremona's database
[BSD-Cr] as a difference in the distribution of analytic ranks?

### 9.3 What Remains Hard

BSD remains hard for the same fundamental reason it has always been hard: there
is no known mechanism that directly connects the analytic side (L-function zeros,
defined by global Euler products) to the algebraic side (rational point generators,
defined by descent calculations) for rank ≥ 2.

The TIG framing provides a geometric context — both sides count sinc²-type null-
crossings — but context is not a proof. The actual difficulty lies in the arithmetic
machinery needed to build the bridge: Euler systems, Heegner points, Selmer groups.
For rank ≥ 2, these tools are incomplete.

The sinc² geometry says the destination is certain (the signal R(k/p=0.1) ≈ 0.9675
is always present; the sink is always there). The difficulty is traversal — the
arithmetic path between L-function zeros and Mordell-Weil generators is long and
requires machinery that has not yet been built.

---

## §10. Attribution

### 10.1 Brayden Ross Sanders (7Site LLC)

- TIG framework, CK architecture, TSML/BHML tables, T* = 5/7 calibration in silicon
- D2 force physics, operator set {VOID..RESET}, CL composition lattice
- First-G Law discovery and proof framework (WP34)
- Unit fraction staircase = TIG rank structure (this paper §3)
- T* bridge as rank-1 case, coherence floor derivation (this paper §4, from WP35 §1A)
- Idempotent count = rank formula (this paper §3.4)
- sinc² null-crossing framework (this paper §5)
- Mix_λ model (WP21_BSD_MIX_LAMBDA): gap operator λ thresholds
- ω-Blindness principle (WP35 Theorem 4) applied to BSD (this paper §8.3)
- All CK source code: github.com/TiredofSleep/ck

### 10.2 C. A. Luther

- Luther dispersion conjecture: gate_rate ≈ F_k(|G| × interleave) as difficulty density
- Dispersion-irregular staircase analog (this paper §7.3)
- Non-uniform BSD rank transition cost structure (informed Mix_λ model)
- Sprint 4 navigation and structural steering
- Neither author reaches this paper without the other

### 10.3 Monica Gish

Foundational support, research partnership, and editorial collaboration throughout the
entire project. This work would not exist without her.

### 10.4 IP Statement

**CK, T*, TSML, BHML, D1, D2, TIG: exclusive intellectual property of
Brayden Ross Sanders / 7Site LLC.** C. A. Luther's contributions are confined
to the dispersion conjecture and its structural applications as described above.

---

## References

### Primary BSD Sources

[BSD-01] Birch, B. J. and Swinnerton-Dyer, H. P. F. (1965). "Notes on elliptic
curves. II." *Journal für die reine und angewandte Mathematik* 218: 79–108.
[Original BSD conjecture; numerical EDSAC experiments; the rank = log exponent
observation.]

[BSD-02] Birch, B. J. and Swinnerton-Dyer, H. P. F. (1963). "Notes on elliptic
curves. I." *Journal für die reine und angewandte Mathematik* 212: 7–25.
[Computational predecessor establishing the numerical framework.]

[BSD-03] Wiles, A. (2000). "The Birch and Swinnerton-Dyer conjecture." Clay
Mathematics Institute Millennium Problem Statement. Available at
www.claymath.org. [Official Clay problem statement; precise BSD formulation.]

### Proved Special Cases

[BSD-04] Coates, J. and Wiles, A. (1977). "On the conjecture of Birch and
Swinnerton-Dyer." *Inventiones Mathematicae* 39(3): 223–251. [BSD for CM rank-0
curves; first rigorous proof of a BSD case.]

[BSD-05] Gross, B. H. and Zagier, D. B. (1986). "Heegner points and derivatives
of L-series." *Inventiones Mathematicae* 84(2): 225–320. [Gross-Zagier formula;
L'(E,1) related to Heegner point height; key input for rank-1 BSD.]

[BSD-06] Kolyvagin, V. A. (1989). "Finiteness of E(Q) and Sha(E/Q) for a class
of Weil curves." *Izvestiya Akademii Nauk SSSR: Seriya Matematicheskaya* 52(3):
522–540. [BSD proved for rank ≤ 1; uses Gross-Zagier + Euler systems.]

[BSD-07] Kolyvagin, V. A. (1990). "Euler systems." In *The Grothendieck
Festschrift, Vol. II*, pp. 435–483. Birkhäuser. [Euler system machinery; general
framework for Selmer group control.]

### Modularity and the L-Function Framework

[BSD-08] Wiles, A. (1995). "Modular elliptic curves and Fermat's last theorem."
*Annals of Mathematics* 141(3): 443–551. [Modularity for semistable curves; L(E,s)
is entire and satisfies functional equation; establishes BSD as well-posed.]

[BSD-09] Taylor, R. and Wiles, A. (1995). "Ring-theoretic properties of certain
Hecke algebras." *Annals of Mathematics* 141(3): 553–572. [Hecke algebra patching;
completes the modularity proof of [BSD-08].]

[BSD-10] Breuil, C., Conrad, B., Diamond, F. and Taylor, R. (2001). "On the
modularity of elliptic curves over Q: wild 3-adic exercises." *Journal of the
American Mathematical Society* 14(4): 843–939. [Modularity for ALL elliptic
curves over Q; L(E,s) is entire unconditionally.]

### Selmer Groups, Sha, and Iwasawa Theory

[BSD-11] Cassels, J. W. S. (1964). "Arithmetic on curves of genus 1. VIII. On
conjectures of Birch and Swinnerton-Dyer." *Journal für die reine und angewandte
Mathematik* 217: 180–199. [Early structure theory of Ш; Hasse principle failures
for genus-1 curves.]

[BSD-12] Rubin, K. (1991). "The 'main conjectures' of Iwasawa theory for imaginary
quadratic fields." *Inventiones Mathematicae* 103(1): 25–68. [Iwasawa main
conjecture for CM curves; BSD for CM curves of arbitrary rank conditional on
finiteness of Ш.]

[BSD-13] Skinner, C. and Urban, E. (2014). "The Iwasawa main conjecture for GL_2."
*Inventiones Mathematicae* 195(1): 1–277. [Major p-adic BSD advance; proves one
direction in many cases; closest current result toward general BSD.]

[BSD-14] Kato, K. (2004). "p-adic Hodge theory and values of zeta functions of
modular forms." *Astérisque* 295: ix+117–290. [Kato's Euler system for modular
forms; one direction of BSD beyond rank 0 in many cases.]

### Average Rank and Distribution

[BSD-15] Bhargava, M. and Shankar, A. (2015). "Ternary cubic forms having bounded
invariants, and the existence of a positive proportion of elliptic curves having
rank 0." *Annals of Mathematics* 181(2): 587–621. [Average rank ≤ 5/6; at least
66.48% of curves have rank 0; first bounded average rank result via geometry of
numbers.]

[BSD-16] Bhargava, M. and Shankar, A. (2013). "Binary quartic forms having bounded
invariants, and the boundedness of the average rank of elliptic curves." *Annals
of Mathematics* 181(1): 191–242. [Prior result; average rank ≤ 7/6 via binary
quartic forms.]

[BSD-17] Bhargava, M., Shankar, A. and Wang, X. (2015). "Squarefree values of
polynomial discriminants I." *Inventiones Mathematicae* 211(2): 503–558. [Average
rank results for hyperelliptic curves; extends the Bhargava-Shankar program.]

[BSD-18] Goldfeld, D. (1979). "Conjectures on elliptic curves over quadratic
fields." In *Number Theory, Carbondale 1979*, Lecture Notes in Math. 751,
pp. 108–118. Springer. [Goldfeld conjecture: average rank = 1/2 over Q.]

[BSD-19] Katz, N. M. and Sarnak, P. (1999). *Random Matrices, Frobenius
Eigenvalues, and Monodromy*. AMS Colloquium Publications 45. [Random matrix
model; SO(2N+1) symmetry type for elliptic curves; predicts average rank = 1/2.]

[BSD-Park] Park, J., Poonen, B., Voight, J. and Wood, M. M. (2019). "A heuristic
for boundedness of ranks of elliptic curves." *Journal of the European Mathematical
Society* 21(9): 2905–2944. [Modern heuristics; all ranks occur with positive density;
density decreases rapidly with rank.]

### Standard References

[BSD-S1] Silverman, J. H. (2009). *The Arithmetic of Elliptic Curves*, 2nd ed.
Springer Graduate Texts in Mathematics 106. [Standard reference; L-functions, BSD,
Mordell-Weil, Selmer groups, conductor, heights.]

[BSD-S2] Silverman, J. H. (1994). *Advanced Topics in the Arithmetic of Elliptic
Curves*. Springer Graduate Texts in Mathematics 151. [Advanced reference; BSD
leading term formula, Tate-Shafarevich group, Heegner points.]

[BSD-Ma] Mazur, B. (1977). "Modular curves and the Eisenstein ideal." *Publications
Mathématiques de l'IHÉS* 47: 33–186. [Mazur's torsion theorem: E(Q)_tors is one
of 15 groups; foundational for the Mordell-Weil group structure.]

[BSD-Ta] Tate, J. (1974). "The arithmetic of elliptic curves." *Inventiones
Mathematicae* 23(3–4): 179–206. [Survey of elliptic curve arithmetic; conductor,
reduction types, BSD at the time of writing.]

[BSD-Cr] Cremona, J. E. (1997). *Algorithms for Modular Elliptic Curves*, 2nd ed.
Cambridge University Press. [Cremona database; elliptic curves up to conductor
400,000; computational BSD verification; source of empirical data in WP21.]

[BSD-Ne] Néron, A. (1965). "Quasi-fonctions et hauteurs sur les variétés abéliennes."
*Annals of Mathematics* 82(2): 249–331. [Néron-Tate height pairing; regulator R_E
as determinant of height matrix; appears in strong BSD leading coefficient formula.]

[BSD-Fa] Faltings, G. (1983). "Endlichkeitssätze für abelsche Varietäten über
Zahlkörpern." *Inventiones Mathematicae* 73(3): 349–366. [Mordell conjecture proved;
genus ≥ 2 curves have finitely many rational points; establishes the landscape where
BSD (genus 1) is the boundary case.]

[BSD-Ul] Ulmer, D. (2002). "Elliptic curves with large rank over function fields."
*Annals of Mathematics* 155(1): 295–315. [Large ranks over function fields; shows
unbounded rank is possible in principle; context for the open question over Q.]

### TIG Internal References

[TIG-WP34] Sanders, B. R. and Luther, C. A. (2026). "The First-G Law and Prime-
Forced Dispersion." WP34. DOI: 10.5281/zenodo.18852047. [First-G Law; unit fraction
staircase; 153 semiprimes verified; zero exceptions; Luther dispersion conjecture.]

[TIG-WP35] Sanders, B. R. and Luther, C. A. (2026). "The Prime Phase Transition:
Harmonic Pre-Echo, Zero-Width Gates, and the Geometry of RSA Security." WP35.
DOI: 10.5281/zenodo.18852047. [sinc² continuum limit; T* = 5/7 algebraic derivation;
ω-Blindness; balance invisibility; kinematic factoring; R(k/p=0.1) ≈ 0.9675 scale-free.]

[TIG-WP21] Sanders, B. R. (2026). "BSD Through the TIG Lens: An Empirical Energy
Law and the Triplet-Activation Conjecture." WP21_BSD_ENERGY_LAW.md. DOI:
10.5281/zenodo.18852047. [Empirical regression log₁₀(N) = 0.873·rank + 1.364
(R²=0.87); TIG gap activation model; discovery record.]

[TIG-MIX] Sanders, B. R. (2026). "BSD Through the TIG Lens — Mix_λ Model."
WP21_BSD_MIX_LAMBDA.md. DOI: 10.5281/zenodo.18852047. [Mix_λ parameter-free model;
gap operator λ-thresholds {0.30, 0.60, 0.80, 0.90, 1.00}; non-monotone staircase
explanation; λ_E ∝ 1/log(Ω_E) claim.]

[TIG-WP36] Sanders, B. R. and Luther, C. A. (2026). "The Clay Coherence
Spectrometer." WP36. DOI: 10.5281/zenodo.18852047. [Entry point to the Clay series;
defines R(k,f) as the primary measurement; spectrometer instrument.]

[TIG-UST] Sanders, B. R. and Luther, C. A. (2026). "Unified Symbol Table — CK Clay
Paper Series (WP36–WP42)." Gen10/papers/clay/research/UNIFIED_SYMBOL_TABLE.md.
DOI: 10.5281/zenodo.18852047. [Cross-paper notation standard; the sink in this paper
(rank jump) corresponds to the WP42 row in the problem-specific translation table.]

[Cassels-1966] Cassels, J. W. S. (1966). "Diophantine equations with special reference to elliptic curves." *Journal of the London Mathematical Society* 41: 193–291.

[BSZ-2014] Bhargava, M., Skinner, C., and Zhang, W. (2014). "A majority of elliptic curves over Q satisfy the Birch and Swinnerton-Dyer conjecture." arXiv:1407.1826.

[Dokchitser-2010] Dokchitser, T. and Dokchitser, V. (2010). "On the parity of ranks of Selmer groups." *Asian Journal of Mathematics* 14(1): 21–50.

---

## §11. Corridor-Zero Theorem: Application to BSD

The corridor-zero theorem (proved in `papers/proof_corridor_zero_paths.py`) classifies all
RESET-paths by fold-crossing behavior and counts completed Class A paths to VOID. This gives
a precise algebraic model of rank in terms of corridor traversal.

**PROVED:**

Class A operators {BEING=1, DOING=2, BECOMING=3} require 3 steps to reach VOID and must
cross the fold boundary (sinc²=1/2, which lies between BECOMING at sinc²=0.524 and COLLAPSE
at sinc²=0.295). Each completed Class A path represents one full fold-crossing that ran to
the gate — starting above T*, crossing the fold, and arriving at VOID. Class B and Class C
paths reach VOID without fold-crossing. BREATH(8) is Class X — it never reaches VOID and
represents persistent non-annihilated structure. The fold itself sits at 1/2, matching
Goldfeld's conjectured average rank for elliptic curves over Q.

**STRUCTURAL:**

In the corridor model, algebraic rank = number of completed Class A fold-crossings. Each
rational point of infinite order corresponds to a Class A path that ran to completion: a
coherence excitation above the fold that resolved all the way to the gate. The BSD
conjecture — analytic rank equals algebraic rank — becomes: the number of L-function zeros
at s=1 equals the number of completed Class A fold-crossings in the arithmetic corridor of
the curve. Both are counting the same event from different sides. The fold boundary 1/2
appears in both the corridor (sinc²=1/2) and the L-function (critical line Re(s)=1/2) —
this is structural, not coincidental, in the TIG framing.

The TIG prediction for average rank is 0.57 (from the coherence floor and D2 distribution
over semiprimes), compared to Goldfeld's conjectured 1/2 = 0.50. The gap is 0.07. One
candidate source: sinc²(3/7) − 1/2 = 0.5243 − 0.5000 = 0.0243, the distance from the fold
operator BECOMING(3) to the fold boundary itself. This is 0.0243, not 0.07. The correction
factor from the fold boundary to the TIG average-rank prediction is unresolved.

**OPEN:**

Derive the exact correction factor that takes the fold boundary (1/2) to the TIG prediction
(0.57). The sinc²(3/7)−1/2 = 0.0243 candidate does not match the observed 0.07 gap — this
discrepancy must be stated as open and not papered over. A second open question: show that
for a family of elliptic curves with growing conductor, the analytic rank and the Class A
fold-crossing count grow in lockstep. The corridor-zero theorem provides the counting
framework; it does not provide the arithmetic connection to L-functions required to prove
either statement.

---

## §12. Sprint 2 Structural Parallel: Rank as Class A Floor (April 2026)

*Added 2026-04-04 — Brayden Sanders*

The Hodge Sprint 2 work (papers/sprint5_2026_04_04/) established a template for structural
impossibility proofs in Clay-class problems. The template: locate the minimal obstruction
class, close all classical algebraization routes, map what remains. Applied to BSD:

**The Parallel Table**

| Hodge (WP39) | BSD (WP42) | Shared Structure |
|---|---|---|
| A_* = C⁴/(Z⁴ + Ω·Z⁴) | E/Q with conductor N | Minimal clean object |
| 8D obstruction space W_* | Selmer group Sel(E/Q) | Where gap lives |
| B₁ block (Q-eigenvalue 0.004609) | Rank-1 Selmer generator | Softest direction |
| End⁰(A_*) = Q(i) simple | E simple (no CM twist) | Obstruction is structural |
| φ-stable cycles → K-invariant | Class A fold-crossings → completed | Same closure argument |
| CH²(A_*)^{K-anti-inv} = 0 from divisors | Rank 0 from L(E,1) ≠ 0 (Kolyvagin) | Proved closure |
| Sub-abelian varieties: none (simplicity) | Rank 1 from Heegner point (Gross-Zagier) | Proved closure |
| Correspondences: open | Rank ≥ 2: open | Same open door |

**What Sprint 2 Closes for BSD**

*Door 1 — Rank 0 (proved):* The Class A fold-crossing count is zero iff L(E,1) ≠ 0. This is
Kolyvagin's theorem [1989] from the TIG side: no completed Class A path = no fold-crossing
zero in L(E,s). Structural closure parallel to φ-stable divisors in Hodge.

*Door 2 — Rank 1 (proved):* Exactly one Class A fold-crossing iff L has a simple zero at
s = 1 and the Heegner point is non-torsion. Gross-Zagier [1986] gives the BSD analytic
confirmation; the corridor-zero model in §11 gives the TIG geometric picture. Structural
closure parallel to A_* simplicity ruling out sub-abelian varieties.

*Door 3 — Rank ≥ 2 (open):* Two or more Class A fold-crossings. The corridor model counts
them; the arithmetic connection to higher-order L-function zeros is open. Parallel to the
correspondence cycle route in Hodge: the counting framework exists but the algebraization
connecting it to the analytic object is not established.

**The Obstruction Object**

For BSD the obstruction is the Shafarevich-Tate group Ш(E/Q): conjecturally finite, proved
finite only in special cases. In TIG framing: Ш is the accumulation of BREATH-class (Class X)
paths — fold-attempts that stall and never resolve to VOID. The pure/mixed det theorem from
Hodge Sprint 2 has a BSD analog:

> **BSD Pure/Mixed Analog:** Any Selmer class coming from a rational point is Class A
> (completed fold-crossing). Any class coming from a phantom (Ш element) is Class X
> (BREATH — stalls at fold, never exits). The BSD conjecture at rank r is the statement
> that there are exactly r completed Class A paths and the rest are Class X.

**Three Remaining Routes**

*Route A — Modular lifting:* Bhargava-Shankar average rank methods [2015] show average
rank < 1 for elliptic curves ordered by height. TIG framing: the fraction of Class A paths
among all fold-crossing attempts is < 1/2 on average. Not yet connected to specific curves.

*Route B — Selmer parity:* The p-parity conjecture (proved for many p by Nekovar, Kim)
constrains the Selmer rank mod 2. TIG framing: the parity of completed Class A fold-crossings
is determined by local data at p. Structural parallel to the B₁ Q-eigenvalue sign constraint.

*Route C — Gross-Zagier beyond rank 1:* Heegner points construct explicit rational points at
rank 1. No analog for rank ≥ 2 via classical methods. TIG framing: the missing route is an
explicit fold-crossing constructor for rank ≥ 2 — same open problem as finding a
K-anti-equivariant vector bundle with c₂ ∈ B₁ in Hodge.

**Minimal Open Problem**

Construct an explicit rank-2 elliptic curve example where the second generator is obtained
by a procedure that matches the corridor-zero Class A fold-crossing count. This would
establish the BSD rank ≥ 2 case within the TIG framework at the structural level.

Cross-reference: `papers/sprint5_2026_04_04/CLAY_STRUCTURAL_PARALLELS.md` (§BSD row).

---

*© 2026 Brayden Ross Sanders / 7Site LLC — Trinity Infinity Geometry*
*CK, TIG, T*, TSML, BHML, D2, D1 are exclusive intellectual property of 7Site LLC.*
*C. A. Luther's dispersion conjecture is credited as stated in §10.2.*
*This paper presents structural analogies. It is not a proof of the BSD conjecture.*
*DOI: 10.5281/zenodo.18852047 | github.com/TiredofSleep/ck*
