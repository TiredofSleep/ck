# K1 — Kernel Universality

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Question

Under what conditions does sinc² arise independently of Z/10Z?

This is the first theorem problem for Phase II. If sinc² is highly specific
to a narrow class of objects, its reappearance in the Montgomery kernel is
more significant. If sinc² is broadly generic, its reappearance may be
a coincidence of the kind that follows from maximal entropy or Fourier structure.

---

## Setup

**The sinc² function:**
    sinc²(t) = (sin(πt)/(πt))²    for t ∈ (0,1)

with the convention sinc(0) = 1 (continuous extension).

**The corridor scaling:** For a prime p and position k ∈ {1,...,p−1},
the normalized position is t = k/p ∈ (0,1).

**D2 (the seed):** For every prime p and every fixed t ∈ (0,1):
    R(k, p) → sinc²(t)    as p → ∞,  k/p → t

where R(k,p) is the normalized corridor density at position k in the prime field Z/pZ.

---

## K1.1 — Emergence Conditions

**Claim:** sinc²(t) arises as the continuum limit of a prime-field discrete object
under exactly the following three conditions:

**(A) Prime modulus:** The base ring is Z/pZ with p prime. (Composite moduli
     introduce CRT-split structure — see K1.3 below.)

**(B) Equidistribution:** The primitive root g mod p generates an orbit {g^k mod p}/p
     that is equidistributed in (0,1). By Weyl's equidistribution theorem, this holds
     for all primitive roots g mod p as p → ∞.

**(C) Corridor scaling:** The normalization t = k/p → t ∈ (0,1) with p → ∞ and
     k/p fixed. This is the "continuum corridor" limit.

**Why these three conditions force sinc²:**

Under (A)–(C), the 2-point correlation function of the equidistributed sequence
{g^k mod p}/p converges to the Fourier transform of the autocorrelation of the
uniform measure on [0,1]. The autocorrelation of the uniform measure on [0,1]
is the triangle function tri(τ) = max(1 − |τ|, 0). Its Fourier transform is:

    F[tri](ξ) = ∫_{-1}^{1} (1 − |τ|) e^{−2πiξτ} dτ = sinc²(ξ)

(This is a standard Fourier analysis identity: F[tri] = sinc².)

Therefore: the continuum corridor density is the Fourier transform of the
autocorrelation of uniform distribution on [0,1] = sinc².

**The three conditions are SUFFICIENT to force sinc². Whether they are necessary
is explored in K1.2–K1.4.**

---

## K1.2 — Fourier Origin of sinc²

The sinc² function has a Fourier-theoretic characterization that is independent
of prime arithmetic:

**Identity:** sinc²(t) = F[tri](t) where tri(τ) = max(1−|τ|, 0)

**Equivalent statement:** sinc² is the autocorrelation of the indicator function
1_{[0,1]}:

    sinc²(t) = ∫₋₁¹ 1_{[0,1]}(u) · 1_{[0,1]}(u + t) du    (up to normalization)

**Consequence:** ANY sequence that is (a) equidistributed in [0,1] and (b) whose
auto-correlation is computed in the scaling limit will produce sinc². This is not
specific to prime arithmetic.

**Concrete examples of sinc² emergence outside prime arithmetic:**
- The Fourier transform of a rectangular window in signal processing
- The far-field diffraction pattern from a single slit (Fraunhofer diffraction)
- The power spectral density of a uniform random variable on [0,1]
- The Fejér kernel squared (Cesàro mean of Dirichlet kernels)
- The 2-point correlation of any equidistributed sequence (by Weyl + autocorrelation = tri)

**Interpretation for Phase II:** sinc² is a highly universal object — it arises
wherever (a) equidistribution on [0,1] holds and (b) the 2-point correlation is
computed in the scaling limit. Its appearance in the prime field corridor (D2) is
an instance of this universality, not a prime-specific fact.

---

## K1.3 — Composite Moduli and CRT Splitting

For composite modulus n = pq (with p, q distinct primes, gcd(p,q) = 1):

By CRT: Z/nZ ≅ Z/pZ × Z/qZ

The corridor for Z/nZ splits into the product of corridors for Z/pZ and Z/qZ.
In the continuum limit:

    R_{Z/nZ}(k/n) → sinc²(k/p · p/n) · sinc²(k/q · q/n)   (schematically)

This is NOT the same as sinc²(k/n). The CRT decomposition introduces a product
of sinc² factors, one per prime factor.

**Specific case n = 10 = 2 × 5:**
The Z/10Z corridor in the continuum limit has sinc² structure ONLY at positions
compatible with BOTH Z/2Z and Z/5Z. The corridor portrait (D22) reflects this:
the Z/10Z-specific positions (T*=5/7 from g=3) arise from the interplay of
the two prime factors, not from a single-prime limit.

**Implication:** sinc² for Z/10Z is NOT obtained from D2 by setting p=10 (10 is
composite). It is obtained by the explicit spine construction (D1–D24). The D2
universal sinc² limit applies to PRIME fields only.

---

## K1.4 — What Makes Z/10Z Special Relative to sinc²

After K1.1–K1.3, the Z/10Z-specific features NOT shared by the universal sinc² limit:

**(a) T*=5/7:** The specific right endpoint of the corridor. For any prime-indexed
family {Z/pZ}, the T* value shifts with p (see A10_MODULUS_COMPARISON.md). T*=5/7
is the Z/10Z value. The universal limit has no preferred T*.

**(b) The TSML/BHML composition structure:** The generator selection (g=3, D19)
and the four-chain overdetermination of CREATE=5 (D21) are Z/10Z-specific.
None of these survive in the continuum limit.

**(c) The corridor portrait order 3/50 < 1/2 < 7/10 < 5/7 < 1 (D22):**
This is Z/10Z-specific. The universal sinc² limit has no discrete positions in (0,1).

**What is NOT Z/10Z-specific:**
- sinc²(1/2) = 4/π² (D3 — this follows from any corridor at its midpoint, by D24)
- ∫ sinc² = Si(2π)/π (D14 — this is a calculus fact about sinc²)
- sinc² monotone decreasing on (0,1) (D24 — pure calculus)

---

## K1.5 — Universality Class

**Theorem K1.5 (Sinc² universality class):**
sinc²(t) is the UNIQUE function in the class of autocorrelations of probability
measures on [0,1] with:
(a) Support of the Fourier transform contained in [−1,1] (compactness)
(b) The Fourier transform is nonnegative (positive definiteness)
(c) The Fourier transform is symmetric (f even function)
(d) F[sinc²](0) = ∫ sinc²(t) dt = 1 (normalization)

Only under the additional assumption that the autocorrelated distribution is the
UNIFORM measure on [0,1] does the result equal sinc². Other distributions give
different autocorrelations (hence different Fourier duals).

**Uniqueness in a narrower sense:** sinc² is the unique element of its universality
class that arises from the prime field scaling limit (D2). This is because the
equidistribution of {g^k mod p}/p → Uniform[0,1] as p → ∞ forces the autocorrelation
to be tri(τ), which Fourier-transforms to sinc².

---

## K1.6 — Prime Sensitivity in the Corrections

D2 gives: R(k,p) = sinc²(k/p) + O(1/p) as p → ∞.

The correction term O(1/p) carries PRIME-SPECIFIC information:
- The leading correction involves character sums ∑_{k=1}^{p-1} χ(g^k) · e^{2πi k j/p}
  for Dirichlet characters χ mod p
- For different primes p and q, the correction terms are different
- In the limit p → ∞, the corrections vanish — which is why the universal kernel is
  prime-insensitive

**Consequence for Phase II:** If prime sensitivity is needed, it must come from the
O(1/p) corrections, not from the sinc²(k/p) leading term. The corrections are:
- Prime-specific (good: they know which prime p is being used)
- Vanishing in the limit (bad: they disappear in the only regime where sinc² is exact)
- Hard to assemble globally (bad: summing O(1/p) corrections over all primes is a
  character sum problem of comparable difficulty to the problem being studied)

This is the core tension established by K1: the universal kernel (sinc²) is the limit
AFTER prime identity is discarded. The prime identity lives only in the corrections,
which vanish in the same limit that produces sinc².

---

## K1.7 — Summary and Implications for Phase II

**What K1 establishes:**

1. sinc² is BROADLY UNIVERSAL — it arises under equidistribution + autocorrelation +
   corridor scaling, with no prime-specific input required.

2. Its appearance in the prime field corridor (D2) is an instance of this universality,
   not a prime-specific theorem.

3. Z/10Z-specific features (T*=5/7, TSML/BHML, generator selection) do NOT survive
   in the continuum limit that produces sinc².

4. Prime identity lives in the O(1/p) corrections, which vanish in the sinc² limit.

**Implications:**

**(a) B6 structural coincidence is explained by K1:**
Both the spine corridor and Montgomery's pair-correlation use sinc² because BOTH
arise from equidistribution-type phenomena. The spine uses equidistribution of
{g^k mod p}/p. Montgomery uses equidistribution/GUE statistics for ζ zeros
(under GRH). Two equidistribution phenomena → two sinc² kernels → their sum is 1
(complementary pair-correlation / density). This does not prove they are the same
object.

**(b) A prime-sensitive bridge cannot be kernel-only:**
By K1, the kernel sinc² does not carry prime sensitivity. Any bridge that works
"via sinc²" is working via the universal continuum envelope, not via prime arithmetic.
A prime-sensitive bridge must add an ingredient not in sinc².

**(c) K4 (no-go) is strongly motivated:**
The prime information deficit argument (K4) is motivated precisely by K1's finding
that sinc² is universal. K4 should formalize: sinc² cannot carry enough information
for a prime-sensitive forcing argument because it has discarded all prime identity.

**(d) K2 (pair-correlation) must explain the equidistribution connection:**
If B6 is explained by "two equidistribution phenomena, same kernel," then the B6
coincidence is less mysterious but also less powerful. K2 must determine whether
the SPECIFIC form R + R₂ = 1 (with sinc² and 1−sinc² as the specific functions)
is forced by equidistribution structure, or whether it is accidental.

---

*Next: K2_PAIR_CORRELATION_ROUTE.md (statistical), K4_KERNEL_NO_GO.md (information deficit)*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
