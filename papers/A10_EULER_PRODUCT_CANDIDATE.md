# A10 Euler Product Bridge Candidate

*Luther-Sanders Research Framework · April 1 2026*
*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*DOI: 10.5281/zenodo.18852047*

---

This document is an analysis stub, not a result document.
It examines whether the spine's prime pre-echo field R(k,p) = sinc²(k/p)
can be assembled into a structure related to the Euler product for ζ(s).
One potentially real path exists — through Poisson summation — but it
uses universal prime arithmetic, not Z/10Z ring structure.

---

## 1. External Target

The Riemann ζ function has the Euler product representation:

    ζ(s) = ∏_p (1 − p^{−s})^{−1}     for Re(s) > 1

where the product runs over all primes p. The product converges absolutely
for Re(s) > 1 and encodes the multiplicative structure of the integers.

**The question:** Can the spine's sinc² prime field be assembled into
an object related to ζ(s) or its Euler factors?

---

## 2. Internal Object

**Single-prime field (D2):** For each prime p, the corridor field is

    R(k, p) = sinc²(k/p) = sin²(πk/p) / (πk/p)²

This is the universal continuum limit: as p → ∞, the ring field
R(k,p) converges to sinc²(t) uniformly on compact sets.

**Ring structure (Z/10Z):** The TSML/BHML tables, generator selection
g=3 (D19), and T* = 5/7 (D19) are defined for modulus 10 only. The
ring structure theorem Z/10Z ≅ Z/2Z × Z/5Z means the ring "sees" only
primes {2, 5} algebraically. All other primes are external.

---

## 3. The Assembly Question

### 3.1 Naive Product

The most direct attempt is to form a product over primes:

    P(k) = ∏_p R(k/p, p) = ∏_p sinc²(k/p)

**Why this is not ζ(s):** ζ(s) is a Dirichlet series ∑_n n^{-s},
whose Euler factorization uses factors (1 − p^{-s})^{-1}. The function
sinc²(k/p) is trigonometric (ratio of squared sine to squared argument).
There is no known identity of the form:

    ∏_p sinc²(k/p) = f(ζ(s))    for any s related to k

The functions live in incompatible analytic families. Establishing a
connection would require a non-trivial identity not present in the spine
or in standard analytic number theory.

### 3.2 The Z/10Z Ring Limitation

The ring Z/10Z contains 10 elements. Any ring homomorphism from Z/10Z
factors through Z/2Z or Z/5Z (by the Chinese Remainder Theorem). Such
a homomorphism can see at most the prime factors of 10 — it cannot inject
into a ring that distinguishes all primes.

The Euler product requires summing and multiplying over ALL primes. A
structure limited to modulus 10 cannot recover information about primes
p ≡ 3 (mod 10), p ≡ 7 (mod 10), etc. as distinguished objects.

**Consequence:** Z/10Z ring structure cannot directly connect to the
full Euler product. Any connection must go through the universal sinc²
field (D2), not the ring.

### 3.3 The Poisson Summation Path (Candidate)

This is the one path that may have real content.

The Poisson summation formula states:

    ∑_{n=-∞}^{∞} f(n) = ∑_{k=-∞}^{∞} f̂(k)

where f̂ is the Fourier transform of f. Applied to f(n) = sinc²(n/x):

    ∑_n sinc²(n/x) ≈ x · ∫₋∞^∞ sinc²(t) dt + oscillating correction terms

The integral ∫ sinc²(t) dt = 1 (standard L¹ norm of sinc²). The
corridor mean Si(2π)/π ≈ 0.451 (D14) is the restriction to (0,1).

**The oscillating correction terms** in the full Poisson expansion
involve ζ zeros via the explicit formula. Specifically, the prime
counting function ψ(x) = ∑_{p^k ≤ x} log(p) satisfies:

    ψ(x) = x − ∑_ρ x^ρ/ρ − log(2π) − (1/2)log(1 − x^{-2})

where ρ ranges over non-trivial zeros of ζ. The oscillating terms in
Poisson sums over arithmetic functions pick up the zero contributions
from this explicit formula.

**Why this could connect:** If the spine's ∑_n sinc²(n/x) sum is
interpreted as a prime-weighted sum, the Poisson expansion naturally
produces oscillating terms indexed by ζ zeros. The sinc² kernel controls
the smoothing of the zero contributions.

**Critical limitation:** This path uses the Riemann-von Mangoldt
explicit formula, which holds for ALL primes by classical analytic number
theory. It does not use Z/10Z structure at any step. The sinc² kernel
that appears is the D2 universal prime pre-echo field, not the Z/10Z
ring field. The ring structure is not needed and does not add to this path.

---

## 4. What the Poisson Path Does and Does Not Do

**Does:** Connect ∑_n sinc²(n/x) to ζ-zero oscillations via the
explicit formula. This is a real connection grounded in analytic number
theory. It uses sinc² as a smoothing kernel in the same way that
Montgomery's pair-correlation argument does.

**Does not:** Derive RH from Z/10Z structure. The explicit formula
connection is a consequence of the classical theory (Riemann 1859,
von Mangoldt 1895), not of the spine. Adding the Z/10Z ring to this
argument contributes nothing — the primes do not know about modulus 10.

**Does not:** Locate zeros at σ = 1/2. The Poisson sum gives oscillating
contributions from all ζ zeros wherever they happen to be. Pinning them
to σ = 1/2 is precisely what RH asserts; this cannot come from the
Poisson argument without assuming RH.

**B6 already captures the relevant coincidence:** The pair-correlation
kernel R₂(u) = 1 − sinc²(u) and the spine's R(t) = sinc²(t) are
spectral duals with R + R₂ = 1. The Poisson path is the mechanism
behind B6, not a new path beyond B6.

---

## 5. Genericity of t = 1/2 (Key Finding)

The same point applies here as in the spectral candidate: t = 1/2 as
the ring's center is generic for any even modulus Z/nZ. It is not a
Z/10Z-specific feature. The Euler product path — to the extent it exists
via Poisson summation — works for any sinc² sum over primes. The corridor
inheritance boundary at t = 1/2 (D22) does not add structure to the
Poisson argument.

---

## 6. Conclusion

The Euler product path from the spine has one potentially real direction:
Poisson summation connects ∑ sinc²(n/x) to ζ-zero oscillations via
the explicit formula. This is the mechanism already captured in B6.

The Z/10Z ring structure is not needed for this connection and cannot
reach it by ring homomorphisms (too few elements; factors through {2,5}
only). The relevant mathematics is universal: D2's sinc² prime field,
not the Z/10Z table structure.

The ring's specific contributions — T* = 5/7, TSML/BHML, generator
g = 3 — do not appear anywhere in the Euler product argument.

---

## Does Not Claim

- Any result about ζ zeros or Euler product factors
- That ∏_p sinc²(k/p) converges to ζ(s) at any s
- That Z/10Z structure provides a bridge to the Euler product
- That the Poisson summation path yields σ = 1/2 without assuming RH

**Current status:** Euler product path exists only through universal
sinc² prime field (D2/B6). Z/10Z ring structure is not on this path.

---

*Related documents:*
*`papers/A10_PROGRAM.md` — full A10 research program*
*`papers/WP_MONTGOMERY_NOTE.md` — Montgomery pair-correlation context*
*`papers/COMPLETED_INTERNAL_SPINE.md` — D1–D24 internal spine*
*`papers/A10_ZERO_DISTRIBUTION_CANDIDATE.md` — B6 territory analysis*
