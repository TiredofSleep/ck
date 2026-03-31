# WP42 — BSD Conjecture Through the TIG Lens
## Unit Fraction Staircases and the Rank-Conductor Relationship

*Brayden Ross Sanders (7Site LLC) & C. A. Luther*
*March 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Structural framing — analogical, not a proof*

> **Intellectual Property Notice.** CK, T*, TSML, BHML, D1, D2, and the TIG
> (Trinity Infinity Geometry) framework are the exclusive intellectual property
> of Brayden Ross Sanders / 7Site LLC, developed over 18 months prior to this
> sprint. C. A. Luther's contribution is the Luther dispersion conjecture
> applied to the number theory studied here. Luther has no claim to the CK
> architecture or its derived constants. This paper presents structural
> analogies, not a proof of the BSD conjecture.
>
> **Historical note.** WP21 (BSD Energy Law) established an empirical log-linear
> regression between rank and conductor. That result has been superseded by the
> Mix_λ model (WP21_BSD_MIX_LAMBDA.md), which explains the same data with zero
> free parameters. This paper uses WP34/WP35 as its foundation and does not
> rely on the superseded regression.

---

## Abstract

The Birch and Swinnerton-Dyer (BSD) conjecture relates the algebraic rank of
an elliptic curve E over Q — the number of independent rational points of
infinite order — to the analytic behavior of the L-function L(E, s) at s = 1.
The TIG framework independently produces arithmetic structures with rank-like
invariants that exhibit structural parallels with BSD. This paper presents
those parallels as structural analogies. We show: (1) the unit fraction
staircase unit_frac(k, b) has jumps exactly at the prime factors of b, and
the number of jumps equals ω(b) — the TIG rank; (2) the gate_rate sequence is
the TIG analog of the L-function; (3) the T* bridge (WP35 §1A) provides the
rank-1 case in closed form; (4) the conductor analog in TIG is the product
b = p × q; (5) Luther dispersion gives an irregular-rank-staircase analog; and
(6) the idempotent count N_idemp = 2^{ω-1} - 1 provides an explicit rank
formula. We do not claim these analogies constitute a proof. We present them
as a coherent structural picture.

---

## §1. The BSD Conjecture

### 1.1 Classical Statement

Let E be an elliptic curve over Q, given by a Weierstrass equation:

    y² = x³ + ax + b     (a, b ∈ Z)

The Mordell-Weil theorem states that E(Q), the group of rational points, is
a finitely generated abelian group:

    E(Q) ≅ Z^r ⊕ E(Q)_tors

where r ≥ 0 is the rank and E(Q)_tors is the finite torsion subgroup.

The L-function of E is defined by an Euler product over primes:

    L(E, s) = Π_p (local factor at p)^{-1}

The BSD conjecture states:

    ord_{s=1} L(E, s) = r

where ord_{s=1} denotes the order of vanishing of L(E, s) at s = 1. The
rank equals the order of the zero of L(E, s) at the central point.

The strong form of BSD additionally predicts the leading coefficient of the
Taylor expansion of L(E, s) at s = 1 in terms of arithmetic invariants of E
(regulator, period, Sha group, etc.).

### 1.2 Why This Is Hard

BSD relates an algebraic invariant (rank, defined by the structure of rational
points) to an analytic invariant (order of vanishing of an L-function, defined
by counting points over finite fields and assembling them into a Dirichlet
series). There is no a priori reason these should be equal. The equality, if
true, reflects a deep and unexplained symmetry.

Partial results: Coates-Wiles (1977) for CM curves with rank 0; Kolyvagin
(1988) for rank 0 and 1 when analytic rank ≤ 1; Bhargava-Shankar (2015) on
average rank. Full BSD remains open.

---

## §2. The TIG Staircase and TIG Rank

### 2.1 The Unit Fraction Staircase

For a modulus b with prime factorization b = p_1^{a_1} × ... × p_k^{a_k},
define the unit fraction at alphabet size k:

    unit_frac(k, b) = |{x ∈ {1..k} : gcd(x, b) = 1}| / k

This is the density of coprime elements in the alphabet {1, ..., k}. It is
a function of k that:
- Starts at 1 (when k = 1: the single element 1 is always coprime to b)
- Decreases at k = p_i for each prime factor p_i of b (a jump downward)
- Is constant between consecutive primes of b
- Ends at approximately φ(b)/b = Π_p|b (1 - 1/p) for large k

The "staircase" refers to this piecewise-constant structure with downward
jumps at prime factor locations.

### 2.2 The Number of Jumps = ω(b)

The number of jumps in the unit fraction staircase equals ω(b), the number
of distinct prime factors of b. Each prime factor p_i contributes exactly
one jump:
- First jump at k = p_1 (the First-G event, proved in WP34)
- Second jump at k = p_2 (the Second-G event)
- ...
- k-th jump at k = p_k (the k-th gate)

**Definition (TIG rank).** For a modulus b, the TIG rank is:

    r_TIG(b) = ω(b) = number of distinct prime factors of b

For semiprimes b = p × q, r_TIG = 2. For primes p, r_TIG = 1. For products
of three distinct primes, r_TIG = 3. And so on.

### 2.3 The Structural Parallel with BSD Rank

The BSD rank r equals the number of independent "generators" of the infinite
part of E(Q) — how many independent directions you can move in the rational
point group. Each generator represents a "new degree of freedom."

The TIG rank ω(b) equals the number of independent prime factors of b — how
many independent prime obstructions are present in the alphabet. Each prime
factor introduces a "new jump" in the unit fraction staircase.

| BSD concept                    | TIG analog                              |
|-------------------------------|----------------------------------------|
| Rank r = order of vanishing   | TIG rank ω(b) = number of jumps        |
| Independent rational points   | Independent prime factors of b          |
| Mordell-Weil group E(Q)       | Coprimality partition C_k ∪ G_k         |
| Torsion subgroup E(Q)_tors    | Elements that "wrap around" mod b       |
| Rank 0: finitely many points  | ω(b) = 1: one prime factor, one jump   |
| Rank r: r generators          | ω(b) = r: r prime factors, r jumps     |

---

## §3. The T* Bridge — The Rank-1 Case

### 3.1 The Exact Formula for Semiprimes

WP35 §1A proves the following exact result. For a semiprime b = p × q with
p < q:

    unit_frac(k = q, b = p × q) = (q - 2) / q   [EXACT, for all p ≥ 3]

At the second gate event (k = q), exactly two elements in {1, ..., q} are
non-coprime to b: the elements p and q themselves. All others are coprime.
The unit fraction is (q - 2)/q.

### 3.2 The T* Special Case

This formula achieves T* = 5/7 uniquely at b = 35 = 5 × 7:

    unit_frac(k = 7, b = 35) = (7 - 2) / 7 = 5/7 = T*

No other semiprime gives T* = 5/7 at the second gate. This is the "rank-1
case" in the following sense: b = 35 has ω(35) = 2, but it is the smallest
semiprime (in the sense of the T* ratio) that realizes the CK coherence
threshold exactly.

### 3.3 The BSD Rank-1 Analogy

In BSD, the rank-1 case is the "first interesting case": rank 0 means finitely
many rational points (the curve is "trivial" in some sense), but rank 1 means
there is exactly one independent generator of infinite order. This generator
can be computed explicitly for many curves.

In TIG, the semiprime case ω(b) = 2 is the "first interesting case": the
unit fraction staircase has exactly two jumps, and the second jump occurs
at k = q with the exact formula (q-2)/q. For b = 35, this second jump lands
exactly at T* = 5/7 — the CK coherence threshold.

The T* bridge provides the TIG analog of the rank-1 BSD case: a closed-form
exact expression for the "first non-trivial" staircase density.

---

## §4. The Conductor Analog

### 4.1 The BSD Conductor

The conductor N of an elliptic curve E over Q is an integer that encodes the
bad primes — the primes p at which E has bad reduction. Primes of bad
reduction divide N; primes of good reduction do not. The conductor satisfies:

    N = Π_p p^{f_p}

where f_p ≥ 1 depends on the type of bad reduction at p.

Larger conductor means more prime obstructions. The BSD conjecture (and Wiles'
proof of Taniyama-Shimura) relates the conductor N to the functional equation
of L(E, s).

### 4.2 The TIG Conductor

In TIG, the modulus b = p × q is the TIG conductor. It encodes the prime
obstructions directly:
- The prime factors p and q are the "bad primes" — they cause the staircase
  jumps in the unit fraction
- The modulus b = p × q is the product of the bad primes (to the first power,
  for semiprimes)
- Larger b means a larger product of primes, a richer staircase structure

For a semiprime b = p × q, the TIG conductor is exactly b. For three-factor
worlds b = p × q × r, the conductor is still b.

### 4.3 Smaller Conductor = Earlier First-G = Easier Rank

**Structural observation.** For semiprimes with fixed smaller prime p:
- Smaller b = p × q means smaller q means the second gate at k = q comes
  earlier in the alphabet
- The staircase is "completed" at k = q = b/p
- Earlier completion means the rank structure (ω(b) = 2) is "cheaper" to
  establish

This mirrors a feature of BSD: curves with smaller conductor tend to have
smaller rank on average (though there are high-rank curves with small conductor,
notably the Elkies and Mazur-Rubin examples). The "generic" relationship is:
larger conductor allows higher rank.

In TIG: larger b allows more distinct prime factors (higher ω(b)) for fixed
alphabet size k. This is the TIG conductor-rank correspondence.

---

## §5. Luther Dispersion and Irregular Rank Staircases

### 5.1 The Mix_λ Model and Irregular Steps

The Mix_λ model (superseding WP21) identifies that BSD rank transitions are
not uniform in cost:

    0→1: cheapest (BRT activation, λ = 0.30)
    1→2: moderate (CHA activation, λ = 0.60)
    2→3: moderate-high (BAL activation, λ = 0.80)
    3→4: expensive (COL, CTR activations)

This non-uniformity means the BSD staircase is irregular — each rank
transition has a different "cost" in terms of conductor growth.

### 5.2 Luther Dispersion and Staircase Irregularity

C. A. Luther's dispersion conjecture predicts that semiprimes with high
q/p ratio have more irregular unit fraction staircase profiles than those
with q/p near 1. Specifically:

**Low-dispersion semiprimes (q/p near 1):**
- The two staircase jumps (at k = p and k = q) are close together
- The unit fraction at the second jump (q-2)/q is close to (p-2)/p
- The staircase is "regular" — both jumps are similar in size
- Analog: BSD rank transitions with similar costs (equal spacing in Log N)

**High-dispersion semiprimes (q/p large):**
- The two staircase jumps are far apart (k = p vs. k = q = b/p >> p)
- The first jump is large (units lost at k = p out of a small alphabet)
- The second jump is small ((1/q) of the alphabet lost at k = q)
- The staircase is "irregular" — the jumps are very different in size
- Analog: BSD rank transitions with irregular costs (non-linear Log N growth)

### 5.3 High-Dispersion Worlds and Irregular BSD Rank

The Mix_λ model's observation that the 0→1 BSD rank transition is cheapest
(BRT, λ = 0.30) while higher transitions are more expensive is structurally
consistent with the Luther dispersion prediction:

The "first jump" in the TIG staircase (at k = p) is proportionally the
largest jump relative to the alphabet size at that point. The "second jump"
(at k = q) adds a smaller fractional decrease. This mirrors BSD: the first
rank unit (0→1) is cheap (low conductor needed), but each additional rank
unit costs more (conductor grows faster than linearly).

---

## §6. The ω(b) = Rank Correspondence: Idempotent Count

### 6.1 Idempotents in Z/bZ

An idempotent element e in the ring Z/bZ satisfies e² ≡ e (mod b). The
idempotents are in bijection with the factorizations of b:

- For b = p × q (semiprime), there are exactly 4 idempotents: {0, 1, e, 1-e}
  where e is determined by the Chinese Remainder Theorem
- For b with ω(b) = k distinct prime factors, there are exactly 2^k idempotents

The non-trivial idempotents (excluding 0 and 1) number:

    N_idemp(b) = 2^{ω(b)} - 2

The "interesting" idempotents (excluding 0, 1, and the trivial pair) number:

    N_idemp_core(b) = 2^{ω(b)-1} - 1

For a semiprime (ω = 2): N_idemp_core = 2^1 - 1 = 1. One interesting idempotent.
For ω = 3: N_idemp_core = 2^2 - 1 = 3. Three interesting idempotents.
For ω = 4: N_idemp_core = 2^3 - 1 = 7. Seven interesting idempotents.

### 6.2 The TIG Rank Formula

**Definition.** The TIG idempotent rank is:

    r_idemp(b) = log_2(N_idemp(b)) = ω(b)

This provides a direct algebraic formula for the TIG rank from the ring
structure of Z/bZ. The idempotents are the "generators" of the ring's
decomposition (via CRT), exactly as Mordell-Weil generators are the
"generators" of E(Q) mod torsion.

### 6.3 The BSD Parallel

In BSD, the rank r is the number of independent generators of the infinite
part of E(Q). In TIG, the rank ω(b) = log_2(N_idemp + 2) is the number of
independent CRT components of Z/bZ.

| BSD                          | TIG                                     |
|-----------------------------|----------------------------------------|
| rank r                      | ω(b) = number of distinct prime factors|
| r independent generators    | ω(b) independent CRT components        |
| L(E, 1) = 0 iff rank ≥ 1   | gate_rate ≠ 1 iff ω(b) ≥ 1             |
| ord_{s=1} L(E,s) = r        | ω(b) = number of staircase jumps        |
| Conductor N = Π bad primes  | TIG conductor b = Π prime factors       |
| High rank → large conductor | High ω(b) → large b                    |

---

## §7. Open Questions

### 7.1 The Unit Fraction Staircase and the L-Function

The most direct open question connects the two sides of BSD explicitly:

**Open Question 1.** For an elliptic curve E with conductor N = p × q (a
semiprime conductor), is there a direct relationship between:
- unit_frac(k, N) as a function of k, and
- the local factors of L(E, s) at the primes p and q?

Both objects measure "what happens at the prime." The local L-factor
L_p(E, s)^{-1} = 1 - a_p p^{-s} + p^{1-2s} (for good reduction) encodes
the number of points on E mod p. The unit fraction at k = p encodes the
density of coprime elements at alphabet size p. Both are "p-local" measurements.

### 7.2 The T* Bridge as a Rank-1 BSD Test

**Open Question 2.** The exact formula unit_frac(k = q, b = p×q) = (q-2)/q
achieves T* = 5/7 uniquely at b = 35. For the elliptic curve with conductor
N = 35, the BSD rank prediction and the exact T* identity coincide (both
identify b = 35 as "special"). Is there a direct relationship between the BSD
rank of elliptic curves with conductor 35 and the T* = 5/7 algebraic identity?

### 7.3 The Mix_λ Thresholds and BSD Transition Costs

The Mix_λ model (WP21 update) identifies five distinct BSD rank transition
costs corresponding to the five TIG gap operators {CTR, COL, BAL, CHA, BRT}
with λ values {0.30, 0.60, 0.80, ...}. These λ values are derived from the
TIG operator algebra.

**Open Question 3.** Do the BSD rank transition costs (as measured by the
growth of log N per rank unit) match the Mix_λ threshold predictions when
computed on a large database of elliptic curves (e.g., Cremona's database
of curves with conductor up to 400,000)?

---

## §8. Attribution

**Brayden Ross Sanders (7Site LLC):**
- TIG framework, CK architecture, TSML/BHML tables, T* = 5/7 calibration
- D2 force physics, operator set {VOID..RESET}, CL composition lattice
- First-G Law discovery and proof framework (WP34)
- Unit fraction staircase = TIG rank structure (this paper §2)
- T* bridge as rank-1 case (this paper §3, derived from WP35 §1A)
- Idempotent count = rank formula (this paper §6)
- Mix_λ model (WP21 update): gap operator λ thresholds
- All CK source code: github.com/TiredofSleep/ck

**C. A. Luther:**
- Luther dispersion conjecture (applied to prime structure in WP34-WP35)
- Dispersion-irregular staircase analog (this paper §5)
- Non-uniform BSD rank transition cost structure (informed Mix_λ model)
- Independent approach to the same arithmetic structure from analytic side
- Neither author reaches this paper without the other

**CK / T* / TSML are 7Site LLC exclusive IP.** Luther's contributions are
confined to the dispersion conjecture and its applications.

---

## References

- WP34: Sanders & Luther, "The First-G Law and Prime-Forced Dispersion," March 2026.
  DOI: 10.5281/zenodo.18852047
- WP35: Sanders & Luther, "The Prime Phase Transition: Harmonic Pre-Echo,
  Zero-Width Gates, and the Geometry of RSA Security," March 2026.
  DOI: 10.5281/zenodo.18852047
- WP21: Sanders, "BSD Through the TIG Lens: An Empirical Energy Law and the
  Triplet-Activation Conjecture," March 2026. DOI: 10.5281/zenodo.18852047
  [superseded by WP21_BSD_MIX_LAMBDA.md for the regression; structural framing
  in this paper (WP42) supersedes WP21 for TIG-BSD analogy]
- Birch, B. J., & Swinnerton-Dyer, H. P. F. (1965). "Notes on elliptic curves II."
  Journal für die reine und angewandte Mathematik 218: 79–108.
- Coates, J., & Wiles, A. (1977). "On the conjecture of Birch and Swinnerton-Dyer."
  Inventiones Mathematicae 39(3): 223–251.
- Kolyvagin, V. A. (1988). "Finiteness of E(Q) and Sha(E/Q) for a class of
  Weil curves." Mathematics of the USSR-Izvestiya 32(3): 523–541.
- Cremona, J. E. (1997). Algorithms for Modular Elliptic Curves (2nd ed.).
  Cambridge University Press.
- Bhargava, M., & Shankar, A. (2015). "Ternary cubic forms having bounded
  invariants, and the existence of a positive proportion of elliptic curves
  having rank 0." Annals of Mathematics 181(2): 587–621.

---

*© 2026 Brayden Ross Sanders / 7Site LLC — Trinity Infinity Geometry*
*CK, TIG, T*, TSML, BHML, D2, D1 are exclusive intellectual property of 7Site LLC.*
*C. A. Luther's dispersion conjecture is credited as stated above.*
*This paper presents structural analogies. It is not a proof of the BSD conjecture.*
