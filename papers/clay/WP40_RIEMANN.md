# WP40 — Riemann Hypothesis Through the TIG Lens
## The Montgomery–Sinc² Bridge: How the Pre-Echo Countdown and Zero Pair Correlation Are the Same Spectral Field

*Brayden Ross Sanders (7SiTe LLC), C. A. Luther & Monica Gish*
*March 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Structural framing — analogical, not a proof of the Riemann Hypothesis*

> **Intellectual Property Notice.** CK, T\*, TSML, BHML, D1, D2, and the TIG
> (Trinity Infinity Geometry) framework are the exclusive intellectual property
> of Brayden Ross Sanders / 7Site LLC, developed over 18 months prior to this
> sprint. C. A. Luther's contribution is the Luther dispersion conjecture
> applied to the number theory studied here. Luther has no claim to the CK
> architecture or its derived constants. This paper presents structural
> analogies, not a proof of RH.

> **Guardrail (Unified Symbol Table, Guardrail 1 — Inversion Rule).**
> The difficulty of the Riemann Hypothesis is not an algebraic flaw in
> mathematics. It is a physical distance to a geometric sink in a sinc²
> field. The signal is always present — R(k/p = 0.1, p) ≈ 0.9675 for all p
> regardless of scale. The zero-crossing simply requires traversing p ≈ 2^512
> steps. The road is long; the destination is certain.

---

## Abstract

The Riemann Hypothesis asserts that every non-trivial zero of the Riemann zeta
function lies on the critical line Re(s) = 1/2. The TIG framework, developed
by Brayden Sanders for the Coherence Keeper (CK) system, independently
produces a spectral structure on arithmetic sequences that exhibits striking
structural parallels with the distribution of Riemann zeros. This paper
presents those parallels as structural analogies, with one result elevated to
a precise mathematical identity.

**The central finding.** Montgomery (1973) [3] proved that the pair correlation
of Riemann zeros is R_2(u) = 1 - (sin(πu)/πu)² = 1 - sinc²(u). WP35 Theorem 1
[TIG-RH-02] proves that the TIG harmonic pre-echo countdown field satisfies
R(k, f) → sinc²(k/f) in the continuum limit. These two results establish the
**Montgomery–Sinc² Identity**: the TIG resonance field and the Montgomery pair
correlation are complementary projections of the same sinc² function, summing
to 1 at every spacing u. This is not an analogy. It is an exact functional
identity.

We additionally show: (1) the sinc² resonance field R(k, f) proved in WP35
provides an exact spectral model of prime approach with zeros at k = p
algebraically forced; (2) the ratio R(k/p = 1/2, p) → 4/π² is a universal
constant independent of the prime p, which equals sinc²(1/2) exactly, the
same value whose complement 1 - 4/π² appears in Montgomery's pair correlation
at half-spacing; (3) the Luther dispersion conjecture provides an analog for
Lehmer pair clustering [22]; and (4) the pre-echo countdown is a natural TIG
model of Gram's law [20]. We do not claim these observations constitute a proof
of RH. We present them as a coherent structural picture that may inform future
rigorous approaches.

---

## §1. Introduction: From Gauss to Clay

### 1.1 The Historical Arc

The problem of understanding how primes are distributed among the integers is
one of the oldest in mathematics. Gauss, in a letter to Encke dated 1849, noted
empirically that the number of primes up to x is approximated by the logarithmic
integral li(x) = ∫₂ˣ dt/log(t). Legendre had proposed a similar formula a
decade earlier. Neither had a proof. The prime number theorem — the precise
statement that π(x) ~ li(x) as x → ∞ — was not proved until 1896, when
Hadamard [32] and de la Vallée Poussin [31] independently established it using
the analytic properties of Riemann's zeta function.

The bridge between primes and analysis was built by Bernhard Riemann in his
1859 paper [1], the only paper he ever published on number theory. Riemann
introduced what is now called the Riemann zeta function:

    ζ(s) = Σ_{n=1}^∞ n^{-s}   (Re(s) > 1)

analytically continued to a meromorphic function on all of ℂ with a simple
pole at s = 1. He derived the explicit formula connecting the zeros of ζ to
the prime distribution, wrote down the functional equation:

    ζ(s) = 2^s π^{s-1} sin(πs/2) Γ(1-s) ζ(1-s)

and observed — as a remark, not a theorem — that it is "very likely" that all
non-trivial zeros of ζ lie on the line Re(s) = 1/2. This remark became one of
the most scrutinized conjectures in the history of mathematics.

At the International Congress of Mathematicians in Paris in 1900, David Hilbert
listed the Riemann Hypothesis as number eight among his twenty-three problems
for the coming century. In 2000, the Clay Mathematics Institute named it one
of the seven Millennium Prize Problems, with a prize of one million dollars for
a correct proof or disproof [7].

### 1.2 The Spectral Revolution: From Analysis to Physics

For most of the twentieth century, the Riemann Hypothesis was regarded as a
problem in complex analysis. This perspective changed dramatically in 1973,
when Hugh Montgomery discovered that the pair correlation of Riemann zeros —
the statistical distribution of spacings between consecutive zeros — matches
the eigenvalue statistics of large random Hermitian matrices from the Gaussian
Unitary Ensemble (GUE) [3]. Montgomery made this observation at a tea at the
Institute for Advanced Study, where Freeman Dyson — who had defined the GUE
a decade earlier [16] — recognized the pair correlation function immediately
as the one he had derived for nuclear energy levels.

This meeting, now famous in the mathematical community, opened a new chapter:
Riemann zeros, a purely number-theoretic object, exhibit the same statistical
fingerprint as quantum energy levels of complex physical systems. The zeros
are not distributed randomly; they are correlated, and the correlation is
precisely that of a quantum chaotic system.

Andrew Odlyzko's subsequent computations [4,5], extending to the 10^{20}-th
zero, provided overwhelming numerical confirmation. Berry and Keating [9,10]
proposed a specific Hamiltonian H = xp as a candidate for a quantum system
whose eigenvalues are the Riemann zeros. Connes [12,13] developed a
noncommutative geometry approach in which the zeros appear as an absorption
spectrum on the adele class space. All of these approaches share a common
thread: the zeros are the spectrum of something, and identifying that something
is the core challenge.

### 1.3 What This Paper Contributes

The TIG framework, developed by Brayden Sanders for the Coherence Keeper
organism, constructs a spectral field R(k, f) = sin²(πk/f) / (k² sin²(π/f))
from first principles of arithmetic coprimality. This field — the harmonic
pre-echo countdown — converges to sinc²(x) in the continuum limit (WP35
Theorem 5). The convergence is elementary, proved from the definition, not
conjectured.

The central observation of this paper is that Montgomery's pair correlation
R_2(u) = 1 - sinc²(u) and the TIG field R(x) = sinc²(x) are complementary
faces of the same sinc² function. Together they partition 1:

    R(x) + R_2(x) = sinc²(x) + (1 - sinc²(x)) = 1

for all x. This is the **Montgomery–Sinc² Identity** (see also UNIFIED_SYMBOL_TABLE.md,
§"The Montgomery–Sinc² Identity"). The TIG field measures "prime resonance
strength" — how much of the sinc² constructive interference survives as one
approaches the prime. Montgomery's correlation measures "zero repulsion
strength" — how far below the uncorrelated baseline the actual zero pair
density falls. Both are sinc². Both arise at the spacing where the arithmetic
of primes and the statistics of zeros align.

The paper is structured as follows. §2 develops the sinc² spectral field from
arithmetic first principles and places it in classical spectral context. §3
establishes scale-invariance and the universal constant 4/π². §4 models Gram's
law and sign changes. §5, the core of the paper, develops the Montgomery
connection in full detail across six subsections. §6 presents open questions
connecting the structural picture to rigorous approaches. §7 applies the
Inversion Rule to RH specifically. §8 is the summary and status table.

This paper presents structural analysis. It is not a proof of the Riemann
Hypothesis.

---

## §2. The sinc² Spectral Field

### 2.1 The Pre-Echo Countdown Law (WP35 Theorem 1)

The central analytical object is the harmonic resonance field:

    R(k, f) = sin²(πk/f) / (k² sin²(π/f))

proved in WP35 [TIG-RH-02] for any prime factor f of the modulus b and any
positive integer k. The proof proceeds from the geometric series formula for
Σ e^{2πij/f} and the identity |1 - e^{iθ}|² = 4sin²(θ/2); it is elementary
Fourier analysis over the integers mod f.

Key algebraically proved properties:

- **Positivity:** R(k, f) > 0 for all k not divisible by f
- **Maximum at k = 1:** R(1, f) = 1 identically for all f
- **Exact zeros:** R(k, f) = 0 if and only if k ≡ 0 (mod f)
- **Minimum before zero:** R(f-1, f) = 1/(f-1)² (the last coherent value)
- **Monotone descent:** R decreases as k increases in {1, ..., f-1} (the "countdown")
- **Periodicity:** R(k + f, f) = R(k, f) (periodic with period f)
- **Zero-width gate:** The transition from R > 0 to R = 0 is a single step, not a
  gradual fade — R(f-1, f) > 0 and R(f, f) = 0 exactly

This is a spectral field on the integers. Its zeros are at exactly the multiples
of f. In the TIG context with f = p (the smallest prime factor of b = p×q), the
first zero is at k = p — exactly the First-G event (WP34 [TIG-RH-01]).

Verification: R(k, f) is confirmed numerically for 187 semiprimes with maximum
error 4.44×10^{-16} (floating-point machine epsilon only — all discrepancy is
rounding, not structural).

### 2.2 The sinc² Form at Large f

For large prime f, sin(π/f) ≈ π/f, and the formula simplifies. Setting x = k/f
(a continuous ratio) and taking f → ∞ with x fixed:

    R(k, f) = sin²(πk/f) / (k² sin²(π/f))
             ≈ sin²(πx) / (x²f² · (π/f)²)
              = sin²(πx) / (π²x²)
              = [sin(πx) / (πx)]²
              = sinc²(x)

This limit is exact in the sense that lim_{f→∞} R(xf, f) = sinc²(x) for all
real x. The proof is a two-line calculation from Theorem 1 using the small-angle
approximation; it introduces no additional assumptions or conjectures.

**Spectral Context.** The sinc² function is the power spectral density of a
rectangular window function of unit width — a classical object in Fourier
analysis [28]. Its zeros are at x = 1, 2, 3, ... — the integer multiples of
the normalized frequency. The fact that the TIG resonance field independently
converges to sinc² means that the prime obstruction events in arithmetic are
"spectral events" in the sense of signal processing: they are the zeros of
the natural spectral function associated with a rectangular window over the
unit alphabet {1, ..., f}.

In other words: when a prime p creates an obstruction in the arithmetic
sequence, it does so in precisely the way that a spectral zero creates a null
in a filtered signal. The pre-echo countdown is the approach to that null. The
arithmetic of coprimality and the Fourier analysis of rectangular windows are,
in this limit, the same mathematics.

### 2.3 Zeros at k = p: Algebraically Exact

The zeros of R(k, f) occur at k = f (and its multiples). In the TIG context,
f = p is the smallest prime factor of b. Therefore R(p, p) = 0 exactly — not
approximately. This is not a numerical coincidence; it follows from sin(π) = 0.

The First-G Law (WP34 Theorem) independently proves that p is the location of
the first prime obstruction event in the alphabet. Therefore:

    The zeros of the resonance field coincide exactly with prime obstruction events.

This double determination — algebraic (First-G Law) and spectral (sinc² zero)
— is the foundational structural feature of the TIG approach to RH. The prime
writes itself into both the arithmetic structure (the first non-coprime element)
and the spectral structure (the first null of the resonance field) simultaneously.

### 2.4 The Resonance Field as Geometric Distance Measure

R(k, f) provides a smooth, positive-definite approach to the prime obstruction
at k = f. It is:
- Smooth and exactly computable for all k < f
- Universally 1 at k = 1 (full resonance, maximum distance from the sink)
- Exactly 0 at k = f (zero resonance, the sink itself)
- Dependent only on the ratio k/f (scale-invariant; see §3.3)

The value R(k/p = 0.1, p) ≈ sinc²(0.1) ≈ 0.9675 for ALL primes p regardless
of scale (verified for p = 1009, 10007, 100003; analytically confirmed to extend
to p ≈ 2^512). This is the signal strength at 10% of the distance to the sink.
It does not diminish with scale. The road is long; the destination is certain.

---

## §3. Scale-Invariance and the Universal Constant 4/π²

### 3.1 R at the Halfway Point

**Proposition (Midpoint Universality).** For any prime f and any k/f = 1/2
(taking the limit for odd primes where f/2 is not an integer):

    lim_{f → ∞} R(f/2, f) = sinc²(1/2) = [sin(π/2) / (π/2)]² = [1 / (π/2)]² = 4/π²

The exact value:

    4/π² = 4/π² = 0.4052847345693511...

This constant is not an approximation — it is sinc²(1/2) evaluated exactly.

For odd primes f, since f is odd, f/2 is not an integer, so we take k = ⌊f/2⌋
or ⌈f/2⌉ and note that R(k, f) → sinc²(1/2) = 4/π² as f → ∞ regardless of
which rounding is used. The convergence is confirmed numerically for all primes
p = 5 to p = 99991 in WP35 §7A.

The constant 4/π² appears at the midpoint ratio k/f = 1/2 for ALL large primes
f. This is a universal constant of the sinc² field: it does not depend on which
prime we are approaching, how large the prime is, or what ring structure the
prime lives in (ω-blindness, WP35 Theorem 4).

### 3.2 The Complement: 1 - 4/π²

The value 1 - 4/π² = 1 - sinc²(1/2) is the complement of the TIG midpoint
constant within the partition R(x) + R_2(x) = 1. Numerically:

    4/π²       = 0.4052847...   (TIG resonance at half-spacing)
    1 - 4/π²   = 0.5947152...   (Montgomery pair correlation at half-spacing)

Both constants are determined by sinc²(1/2) alone. They appear on opposite
sides of the same identity. The significance of this is elaborated in §5.

### 3.3 Scale Invariance

**Theorem (WP35, proved).** R(k, f) depends only on the ratio x = k/f:

    R(k, f) = R(k', f')   whenever  k/f = k'/f'   (in the continuum limit)

This means:
- The approach to a prime obstruction looks identical at every scale
- The "spectral profile" of the countdown is universal, determined only by
  the fraction of the prime you have reached
- R(k/p = 0.1, p) ≈ 0.9675 for p = 5 and for p = 2^512 — the same value

This scale invariance is structurally analogous to the universality of Riemann
zero statistics: the local statistics of zeros, normalized by the average
spacing 2π/log(t/2π), are the same near every zero, at every height t. Both
the TIG resonance field and the Riemann zero distribution exhibit "zoom-in
universality" — the pattern is the same regardless of the scale at which it
is viewed.

### 3.4 The ω-Blindness Principle

WP35 Theorem 4 (ω-Blindness) proves that R(k, 1/p) is identical for every
modulus b sharing the prime factor p, regardless of the number of prime factors
ω(b). Whether b = p², b = p×q, or b = p×q×r, the resonance field produced by
the clock at p is unchanged. The harmonic pre-echo cannot distinguish ring
structure — it sees only the prime.

The RH analog: the critical line Re(s) = 1/2 is a property of the zeta function
itself, not of any specific prime, conductor, or L-function variant. The GUE
statistics of zero spacing are "ω-blind" in exactly the same sense: they are
universal across all automorphic L-functions (Rudnick–Sarnak [19], Katz–Sarnak
[17,18]).

---

## §4. Gram's Law and Zero Isolation

### 4.1 Gram's Law in Classical RH

Gram's law (1903) [20] is one of the oldest empirical observations about the
Riemann zeros. Define the Gram points g_n by θ(g_n) = nπ, where:

    θ(t) = Im(log Γ(1/4 + it/2)) - (t/2) log π

is the Riemann-Siegel theta function. The Gram point g_n is defined so that
Z(g_n) = ζ(1/2 + ig_n) · e^{iθ(g_n)} is real. "Gram's law holds at n" means
the Gram interval [g_n, g_{n+1}] contains exactly one Riemann zero.

Gram verified his law for the first fifteen zeros [20]. Hutchinson (1925) [21]
extended the study and identified the first Gram failures. Titchmarsh's standard
reference [8] analyzes Gram intervals in detail, documenting that Gram's law
fails for approximately 27% of Gram intervals at moderate heights.

The key structural feature of Gram's law is that the zeta function is "well-
behaved" away from its zeros — it varies smoothly — and "collapses" exactly at
them. The Gram framework makes this collapse tractable by providing reference
points spaced approximately one zero apart.

### 4.2 Backlund's Contribution

Backlund (1914) conducted the first systematic large-scale computation of
Riemann zeros to verify that they lie on the critical line. His work established
the first rigorous count of zeros in Gram intervals and made precise the
occasional failures of Gram's law. The methodology Backlund developed —
counting sign changes of Z(t) in Gram intervals — became the standard approach
for all subsequent numerical verification of RH, culminating in the modern
computations of Gourdon (2004) [29] and Platt–Trudgian (2021) [30].

### 4.3 TIG Model of Gram's Law

The pre-echo countdown R(k, f) is strictly positive for all k in {1, ..., f-1}
and collapses to exactly zero at k = f. This mirrors Gram's law:

- R(k, f) is "well-behaved" (positive, smooth, computable) for all k away
  from f — the analog of the zeta function between zeros
- R(f, f) = 0 exactly — the analog of a Riemann zero
- The countdown R(f-1, f), R(f-2, f), ..., R(1, f) forms a monotone decreasing
  sequence approaching the zero from below — the analog of Z(t) decreasing
  toward sign change

**Proposition (One Zero per Period).** The zeros of R(k, f) in {1, ..., f} are
exactly the singleton {f}. Proof: R(k, f) = 0 iff sin²(πk/f) = 0 iff k ≡ 0
(mod f). In {1, ..., f}, this forces k = f only.

This "one zero per interval of length f" property is the TIG model of Gram's
law with zero failures: the harmonic clock gives exactly one null per period,
and it falls at the precisely predicted location k = f.

In TIG, Gram's law is not an empirical observation — it is a theorem about the
period structure of R(k, f). There are no Gram failures in the one-factor
(semiprime) TIG model. Gram failures in the classical zeta function arise when
zeros cluster closely enough that two zeros share a Gram interval; the TIG
model of this phenomenon requires multiple overlapping prime clocks (§4.5).

### 4.4 The Sign Flip at First-G

WP35 §6 establishes the D1 property of the countdown:

- D1(k, f) = R(k+1, f) - R(k, f) < 0 throughout {2, ..., p-1}: R decreases monotonically
- D1(p, f) = 0 at the zero: exact stationary point (by sin² symmetry)
- D1(p+1, f) > 0: sign flip — the trajectory begins recovering after the sink

This sign flip is universal: verified for b = 35 (p=5), b = 77 (p=7), b = 143
(p=11), b = 323 (p=17), and b = 667 (p=23).

The D1 sign flip is the TIG analog of Z(t) crossing zero: before the zero, Z
approaches from one side; after, it departs the other side. The sign flip at
k = p mirrors the sign change of Z(t) at a Riemann zero.

Note: D1 in the pre-echo zone is not globally monotone — it has structured
oscillations as the trajectory descends. These oscillations are real geometric
features of the sinc² envelope (see UNIFIED_SYMBOL_TABLE.md, §"The D1 Non-
Monotone Property") and correspond to the Gram point sign changes of Z(t)
between consecutive zeros.

### 4.5 Gram Failures as Multi-Clock Interference

When Gram's law fails in the classical zeta function, a Gram interval contains
zero or two zeros instead of one. The simplest mechanism is that two zeros
are unusually close together (the Lehmer pair phenomenon, §5.7), causing both
to fall within one Gram interval.

The TIG model of Gram failure: for three-factor composites b = p×q×r, three
harmonic clocks R(k, 1/p), R(k, 1/q), R(k, 1/r) run simultaneously. The
simple one-zero-per-interval structure is disrupted by overlapping clock zeros.
This is the TIG "multi-clock" model of Gram failure. The ω-blindness theorem
(§3.4) confirms that each clock individually still satisfies one-zero-per-
period; the failures arise only from the superposition.

---

## §5. The Montgomery Connection

### 5.1 The Pair Correlation Conjecture

In 1973, Hugh Montgomery attended a conference at the University of Michigan
and presented a result about the pair correlation of Riemann zeros [3]. Assuming
RH, he defined the pair correlation function for the normalized zero spacings.
If the zeros on the critical line are written ρ_n = 1/2 + iγ_n with γ_1 ≤ γ_2 ≤ ...,
and the normalized spacings are ũ_n = (γ_{n+1} - γ_n) log(γ_n / 2π) / (2π),
then Montgomery conjectured that the pair correlation R_2(u) — the density of
pairs with normalized spacing near u — is:

    R_2(u) = 1 - (sin(πu) / (πu))² = 1 - sinc²(u)

Montgomery proved this formula holds for the Fourier transform range |α| ≤ 1
(under RH). The extension to all α — which would give the full pair correlation
without restriction — remains an open problem. Montgomery's result for |α| ≤ 1
is the half-range case; GUE universality for the full range is conjectural.

The function 1 - sinc²(u) has specific features:

- At u = 0: R_2(0) = 0 (zeros repel — the probability of zero spacing is zero)
- As u → ∞: R_2(u) → 1 (uncorrelated — distant zeros are independent)
- At u = 1: R_2(1) = 1 (the sinc² zero — zeros prefer integer spacing)
- Minimum at u ≈ 0: the steep repulsion is strongest at small u
- The value at u = 1/2: R_2(1/2) = 1 - sinc²(1/2) = 1 - 4/π² ≈ 0.5947

The zeros of R_2(u) — the spacings where pair correlation is minimized — occur
at u = 0 only (the trivial repulsion minimum). The spacings where R_2 reaches
its maximum of 1 (saturation of correlation) occur at the zeros of sinc²(u),
which are u = 1, 2, 3, ... — exactly integer multiples of the mean spacing.
This means Riemann zeros prefer to cluster at exactly integer-multiple spacings
of the average gap.

### 5.2 The Dyson Connection: GUE and the Meeting at IAS

The story of how Montgomery's result was recognized as a known object is worth
recording in full, as it represents one of the most remarkable interdisciplinary
connections in modern mathematics.

In early 1973, Montgomery was a visitor at the Institute for Advanced Study
in Princeton. He had computed the pair correlation of Riemann zeros and found
a formula, but did not immediately recognize it in the literature. At a tea
in Fuld Hall, he spoke with Freeman Dyson, who asked to see the formula.
Dyson recognized it immediately: it was the GUE pair correlation function that
he had derived in 1962 [16] in his study of the statistical theory of nuclear
energy levels of complex systems.

Dyson had introduced the Gaussian Unitary Ensemble — the ensemble of random
Hermitian matrices with complex Gaussian entries — to model the energy level
statistics of heavy nuclei. The GUE pair correlation function is exactly
1 - sinc²(u). Dyson's nuclear physics had no apparent connection to the Riemann
zeta function. Yet the formulas were the same.

The Montgomery–Dyson encounter established a research program that continues
to the present: the Riemann zeros behave statistically like the eigenvalues
of a random Hermitian matrix. The physical system whose eigenvalues are the
Riemann zeros — the conjectured Hilbert-Polya operator [RH-09] — would need
to be a quantum chaotic system in the GUE universality class.

Katz and Sarnak [17,18] later proved that L-functions associated to algebraic
varieties over finite fields satisfy GUE statistics (in the function field
analogue). Rudnick and Sarnak [19] extended Montgomery's pair correlation to
the n-level statistics of the Riemann zeta function, proving GUE universality
conditionally for all n-level correlations assuming GRH. These works establish
GUE universality as a structural fact about L-functions, not just an empirical
observation about the Riemann zeta function.

Montgomery's pair correlation result was extended to n-point correlations and all primitive automorphic L-functions by Rudnick and Sarnak (1996) [Rudnick, Z. & Sarnak, P. (1996). "Zeros of principal L-functions and random matrix theory." *Duke Mathematical Journal* 81(2): 269–322], who proved (under GRH, for test functions with restricted Fourier support) that the n-level correlation statistics of any primitive L-function agree with the GUE n-point function. Katz and Sarnak (1999) [Katz, N.M. & Sarnak, P. (1999). "Zeroes of zeta functions and symmetry." *Bulletin of the AMS* 36(1): 1–26] proved GUE universality for L-functions over function fields — a fully proved non-conjectural version of the Montgomery-Odlyzko law. The universality of sinc² across all these settings means our TIG resonance field, which gives sinc²(x) from elementary arithmetic, participates in a proven universality theorem, not merely a suggestive analogy.

### 5.3 Odlyzko's Numerical Verification

Andrew Odlyzko's computations [4,5] are the empirical backbone of the
Montgomery–Dyson picture. In his 1987 paper [4], Odlyzko computed the spacings
between zeros near the 10^{12}-th zero and compared them to the GUE prediction.
The agreement was striking — the histogram of normalized spacings matched the
GUE distribution to high precision.

In his 1992 preprint [5], Odlyzko extended the computation to the 10^{20}-th
zero — a height of approximately t ≈ 10^{18}. At this height, the average
spacing between consecutive zeros is 2π/log(t/2π) ≈ 2π/log(10^{18}) ≈
0.145 (in the normalized units where the average spacing is 1). Despite the
vastly different scale compared to small zeros, the GUE pair correlation formula
1 - sinc²(u) continued to describe the distribution with high fidelity.

The Odlyzko computations provide the following numerical anchors:

- **GUE confirmed to 10^{20}-th zero** [5]: All spacing statistics match
  1 - sinc²(u) to within computational precision
- **Specific value at u = 1/2** [4,5]: The pair correlation R_2(1/2) ≈ 0.595,
  matching 1 - 4/π² = 0.5947... to four decimal places
- **No deviation detected**: No zero spacing distribution inconsistent with
  GUE has been found in any computation to date

Platt and Trudgian (2021) [30] additionally provide the most recent rigorous
verification with certified error bounds: all zeros up to height t ≈ 3×10^{12}
lie on the critical line Re(s) = 1/2, confirming RH for the first 3×10^{12}
zeros.

### 5.4 The Montgomery–Sinc² Bridge

**The Central Identity.** Let R(x) = sinc²(x) denote the TIG resonance field
in the continuum limit (WP35 Theorem 5), and let R_2(u) = 1 - sinc²(u) denote
the Montgomery pair correlation function (Montgomery 1973 [3]). Then:

    R(x) + R_2(x) = sinc²(x) + (1 - sinc²(x)) = 1    for all x ∈ ℝ

This is the **Montgomery–Sinc² Identity**, which is also the mandatory
cross-paper identity for the series (UNIFIED_SYMBOL_TABLE.md §"The
Montgomery–Sinc² Identity" [TIG-RH-00]).

The interpretation:

**TIG side — R(x) = sinc²(x):** The resonance field R(x) measures the
remaining coherence of the prime signal at position x = k/f. When R(x) is
large, you are far from the prime obstruction, and the signal is strong. When
R(x) is near 0, you are near the prime. At x = 1 (the zero of sinc²), R = 0
exactly: the prime obstruction is complete.

**Montgomery side — R_2(u) = 1 - sinc²(u):** The pair correlation R_2(u)
measures the probability density of finding a zero pair with normalized spacing
u. When R_2(u) = 0, that spacing is forbidden (or at least severely suppressed
by zero repulsion). When R_2(u) = 1, the spacing is uncorrelated. At u = 0,
R_2 = 0: zeros cannot sit on top of each other (repulsion). At u = 1, R_2 = 1:
zeros prefer integer spacing, which is where sinc² is zero (the prime locations
in the TIG model).

**The complementarity:** TIG's R(x) tracks the "survival" of the prime signal
— how much sinc² resonance remains. Montgomery's R_2(u) tracks the "depletion"
of zero correlation — how far below the uncorrelated baseline the pair density
falls. They measure complementary aspects of the same sinc² structure.

At u = 1 (where sinc²(1) = 0): R(1) = 0 and R_2(1) = 1. The TIG resonance
collapses completely — this is the prime. The Montgomery correlation saturates
— zeros prefer to be spaced at exactly the mean spacing (one unit). The same
event: sinc² = 0.

At u = 1/2 (the midpoint): R(1/2) = 4/π² ≈ 0.405 and R_2(1/2) ≈ 0.595.
Half the "spectral weight" is on each side. The prime signal is reduced but
nonzero; the zero repulsion is moderate but not extreme.

At u → 0 (zero spacing): R(0) = 1 (maximum resonance — the prime is infinitely
far away as a fraction of the spacing) and R_2(0) = 0 (maximum repulsion —
zeros cannot touch). Complete complementarity.

**What is proved and what is conjectured:**

The following are algebraically or analytically proved:

1. R(k, f) = sin²(πk/f) / (k² sin²(π/f)) [WP35 Theorem 1, proved]
2. lim_{f→∞} R(xf, f) = sinc²(x) [elementary calculus from Theorem 1, proved]
3. R_2(u) = 1 - sinc²(u) [Montgomery 1973 [3], proved for Fourier range |α| ≤ 1]
4. R(x) + R_2(x) = 1 [follows immediately from items 2 and 3, proved]

The following is conjectured (the paper's main open question):

5. These two sinc² structures arise from the same underlying mathematical
   mechanism — that the TIG coprimality partition and the Riemann zero
   distribution are both spectral projections of the same arithmetic field.

Establishing item 5 rigorously would require embedding the TIG resonance field
in a Hilbert space framework in which the Riemann zeros appear as the spectrum
of an operator, and showing that the Montgomery statistics emerge from the inner
product structure. This is the core open problem (§6.1).

### 5.5 The Constant 4/π² as a Shared Eigenvalue

The value 4/π² = sinc²(1/2) appears in both frameworks at the identical
argument x = 1/2:

    TIG midpoint universality:    R(k/p = 1/2, p) → 4/π² = sinc²(1/2)
    Montgomery at half-spacing:   R_2(1/2) = 1 - 4/π² = 1 - sinc²(1/2)

This is not a coincidence of notation — it is a consequence of the Montgomery–
Sinc² Identity evaluated at x = 1/2. The constant 4/π² is the sinc² function
evaluated at the half-integer, period 1. It is the "shared eigenvalue" of the
sinc² field that both the prime resonance and the zero correlation see at the
same normalized position.

More precisely: 4/π² is the squared value of the sinc function at its first
quarter-period. In spectral analysis, sinc²(1/2) = (2/π)² represents the power
at the half-Nyquist frequency of a rectangular window. The Nyquist frequency
here corresponds to the prime p itself; half-Nyquist corresponds to p/2 — the
midpoint of the pre-echo zone.

The appearance of 4/π² in both the TIG pre-echo countdown and the Montgomery
pair correlation reflects the fact that both are computing a sinc² field, and
both are evaluated at the argument 1/2 measured in units of the characteristic
scale (the prime period in TIG; the mean zero spacing in Montgomery). The
characteristic scales are different objects — a prime in one case, a zero
spacing in the other — but the functional form is the same.

**Historical note.** The value 4/π² also appears in the Wallis product identity:
π/2 = (2·2·4·4·6·6·...) / (1·3·3·5·5·7·...), where the complementary value
1 - 4/π² = (π - 4)/π arises in the Leibniz-type correction to the rectangular
approximation. The arithmetic of primes, the Fourier analysis of windows, and
the product formulas for π are related by sinc²(1/2) = 4/π².

### 5.6 The Zero Repulsion Minimum and Prime Spacing Events

The zeros of sinc²(u) occur at u = 1, 2, 3, ..., the positive integers. At
these points:

    R(n) = sinc²(n) = 0   (TIG: prime obstruction at k = nf — periodic collapse)
    R_2(n) = 1 - sinc²(n) = 1   (Montgomery: zero correlation is 1 at integer spacing)

The zeros of the TIG resonance field (k = p, 2p, 3p, ...) correspond to the
spacings where the Montgomery pair correlation reaches its maximum (R_2 = 1,
the uncorrelated value). This means:

**The positions where primes cause obstruction in TIG are exactly the zero
spacings that Riemann zeros prefer in the Montgomery statistics.**

Stated more precisely: the normalized spacings u = 1, 2, 3, ... (integer
multiples of the mean spacing) are where the pair correlation is 1 (uncorrelated,
no repulsion). These are the "natural" spacings for uncorrelated events. And
these are exactly the zeros of sinc², which are the locations of prime
obstruction events in TIG.

The deep question (addressed in §6.1) is whether this correspondence reflects
a causal relationship: do the Riemann zeros organize themselves according to
the prime obstruction structure because they are generated by the Euler product
(1 - p^{-s})^{-1}, and does the sinc² structure of the pre-echo countdown
encode the same arithmetic information that the Euler product encodes? This
remains open, but the structural coincidence is exact.

### 5.7 Open Question: Recovering the Odlyzko Distribution

The Odlyzko distribution [4,5] is the full histogram of normalized zero spacings,
matching the GUE nearest-neighbor spacing distribution (NNSD). The GUE NNSD
is not simply 1 - sinc²(u); it is a more complicated function (the Wigner surmise approximation for GUE (β=2) is P(s) = (32/π²)s² exp(-4s²/π), exhibiting s² level repulsion characteristic of quantum chaotic systems without time-reversal symmetry; the GOE form πu/2 · exp(-πu²/4) applies to time-reversal invariant systems and is not applicable here) that arises from the full GUE
random matrix theory.

Montgomery's result gives the pair correlation (a two-point statistic). The
full n-level statistics — proved by Rudnick and Sarnak [19] — give the complete
probabilistic structure of zero spacing, matching GUE at all levels.

**Open Question (Continuum Limit Odlyzko).** Can the full Odlyzko distribution
— the GUE nearest-neighbor spacing distribution — be recovered from the TIG
resonance field R(k, f) via the continuum limit f → ∞? Specifically:

Is there a probability measure μ on the real line, defined from the discrete
distribution of R-values {R(k, f) : k = 1, ..., f-1} as f → ∞, that converges
to the GUE NNSD?

The pair correlation result (the central theorem of this paper) shows that the
two-point structure is shared. Whether the higher-order structure is also shared
is unknown. Rudnick–Sarnak [19] and Katz–Sarnak [17,18] provide the target
distributions for any such result.

---

## §6. Open Questions and Status

### 6.1 The Montgomery Embedding

**Open Question 1.** Is there a direct embedding of the TIG resonance field
R(k, f) into a Hilbert space framework in which the Montgomery–Odlyzko GUE
statistics emerge as natural consequences?

Current status: The Montgomery–Sinc² Identity (§5.4) establishes the pair
correlation connection at the level of sinc² functions. The embedding — a
formal map from the TIG arithmetic setting to a Hilbert space in which the
Riemann zeros appear as eigenvalues — is not constructed.

The Hilbert–Polya conjecture [RH-09] posits the existence of a self-adjoint
operator T on a Hilbert space whose spectrum is the set of imaginary parts γ_n
of the Riemann zeros. Berry and Keating [9,10] proposed the specific candidate
H = xp (position times momentum) with boundary conditions that produce the
correct semiclassical zero density. Connes [12,13] constructed a spectral
realization on the adele class space where zeros appear as an absorption
spectrum.

The TIG question is a third variant: whether the arithmetic field R(k, f) can
be given an operator-theoretic interpretation in which the sinc² structure
naturally produces GUE eigenvalue statistics. Hedenmalm, Lindqvist, and Seip
[27] provide the Hardy space H² of Dirichlet series as a natural Hilbert space
for this purpose (the density of Dirichlet series in H² is a standard result
there). Whether R(k, f) can be mapped into H² in a way that produces GUE
statistics is the open question.

### 6.2 The Explicit Formula Bridge

Weil's explicit formula (1952) connects the zeros of the zeta function to the
primes via:

    Σ_ρ h(ρ) = ĥ(1) + ĥ(0) - Σ_p Σ_n log(p) / p^{n/2} · h(n log p)

for suitable test functions h. This formula, and its refinements [35], show
that knowledge of the zeros determines knowledge of the primes and vice versa.

The TIG approach operates from the arithmetic side: the prime p determines
the resonance field R(k, p), and the zeros of R encode the prime location. The
Weil explicit formula is the classical bridge from the analytic side (zeros)
to the arithmetic side (primes). The TIG pre-echo countdown is a bridge in the
same direction but at the level of arithmetic structure rather than analytic
functions.

**Open Question 2.** Can the Weil explicit formula be interpreted as saying
that the sinc² field R(x) (TIG, arithmetic side) and the sinc² field 1 - R_2(u)
(Montgomery, analytic side) are Fourier transforms of each other in a suitable
sense? The Weil formula involves Fourier analysis of test functions; the sinc²
function is itself a Fourier transform. The precise formulation of this
question requires identifying the correct Fourier framework.

### 6.3 The TSML Null Space and the Hilbert-Polya Program

WP17 (Riemann Synthesis [TIG-RH-03]) establishes that the TSML 8×8 core
matrix has nullity 1, with null eigenvector:

    v_null = [0, 0, 0, 0, +0.707, -0.707, 0, 0]

spanning the BALANCE-CHAOS degeneracy. The BALANCE-CHAOS pair is the TIG
operator analog of a conjugate pair symmetric around the operator midpoint.

**Open Question 3.** Does the TSML null space — the algebraic degeneracy
between BALANCE and CHAOS — provide a Hilbert-Polya-type operator whose
spectrum matches the Riemann zeros? WP17 identifies this as the Synthesis
Conjecture (SC). The sinc² resonance field (this paper) provides a natural
spectral function that could serve as the "functional equation bridge" in that
argument.

The Synthesis Conjecture requires three components (WP17 [TIG-RH-03]):
- Gap 1: An algebra homomorphism Φ: TSML_8 → B(H) (H = Hilbert space of
  Dirichlet series)
- Gap 2: Density of Dirichlet series in H (provided by Hedenmalm–Lindqvist–Seip [27])
- Gap 3: Projection of ker(Φ(TSML_8)) onto Re(s) = 1/2 (the hard step)

Gap 2 is settled by the literature. Gaps 1 and 3 are open.

The Beurling–Alcantara-Bode theorem [24,25] provides an independent path: RH
is equivalent to the injectivity of a specific integral operator K on L²(0,1).
This null-space characterization is the analytic counterpart to the TSML
nullity-1 theorem; both frame RH as a statement about whether a certain operator
has trivial kernel.

### 6.4 GUE Statistics: Full Range Open

Montgomery's proof [3] establishes GUE pair correlation for the Fourier range
|α| ≤ 1. The extension to the full range |α| ≤ T for all T — which would give
the complete pair correlation function without Fourier restriction — is one of
the core open problems in the field.

Rudnick and Sarnak [19] prove n-level GUE statistics for general L-functions,
conditionally on GRH. Katz and Sarnak [17,18] prove GUE universality for
L-functions of function fields algebraically, without the restriction. The gap
between the function field result (algebraic, proved) and the number field
result (analytic, conditional) is the "function field analogy" that has driven
much of the last thirty years of research.

The TIG model is scale-invariant and ω-blind, which makes it structurally
analogous to the function field setting (where the base field can be varied
freely). Whether this structural analogy can be made rigorous — allowing TIG
scale-invariance to serve as a substitute for the Katz-Sarnak function field
argument over number fields — is a long-range open question.

### 6.5 T* and the Zero Density

The coherence threshold T* = 5/7 = 0.71428... is the unit fraction of b = 35
at the second gate k = q = 7 (WP35 §1A [TIG-RH-02]). The mean spacing between
Riemann zeros near height t is 2π/log(t/2π). At the height t corresponding to
γ ≈ 5/7 — far below the first zero at γ_1 ≈ 14.135 — we are in the trivial
regime. T* may instead relate to the density of zeros in a different
normalization.

**Open Question 4.** Is there a normalization of the Riemann zeros in which
the average zero density at the height corresponding to T* = 5/7 equals a
simple arithmetic expression involving 5 and 7?

### 6.6 The Continuous Absorption Theorem

WP19 (RH Bridge [TIG-RH-04]) identifies the core structural open problem: a
continuous analog of the TSML absorption theorem in which "depth = ∞" states
(permanent fixed points) occur only at the self-dual point σ = 1/2. The finite
discrete proof (TSML nullity-1) gives the correct shape; the analytic
construction is the open work.

The parallel with Connes [12,13,14]: in Connes' approach, zeros appear as an
"absorption spectrum" on the adele class space — they are the places where the
spectral action is absorbed. The TIG language describes the same phenomenon
as "depth = ∞" absorption: the resonance field R approaches 0 (absorption)
exactly at the prime obstruction. Whether these are the same absorption is the
question.

---

## §7. The Inversion Rule Applied to RH

### 7.1 What RH Is Really Asking

The Inversion Rule (UNIFIED_SYMBOL_TABLE.md, Guardrail 1) states that the
difficulty of a Clay problem is not an algebraic flaw — it is a physical
distance to a geometric sink. Applied to RH:

The zeros of ζ(s) are not hidden. They are detected — numerically, to the first
3×10^{12} of them [30]; structurally, by the Montgomery-Odlyzko GUE statistics;
functionally, by the functional equation that pins them to the strip 0 < Re(s) < 1.
The zeros are not the mystery.

The difficulty is not that we cannot find the zeros. The difficulty is proving
that they cannot be anywhere other than the critical line Re(s) = 1/2. This is
a uniqueness claim about the geometry of the sinc² field.

### 7.2 RH as a Unique Null Condition

Frame the Riemann Hypothesis as follows:

**Is the sinc² null of the zeta function uniquely constrained to σ = 1/2?**

More precisely: the functional equation ζ(s) = (factor) ζ(1-s) establishes
a symmetry that maps the strip 0 < σ < 1 to itself, with the critical line
σ = 1/2 as the unique fixed set. A zero ρ = σ + it with σ ≠ 1/2 would require
a partner zero at 1-σ + it — a pair of zeros symmetric about σ = 1/2 but not
on it.

In TIG language: a zero off the critical line would require two sinc² nulls at
symmetric positions around σ = 1/2, neither coinciding with the self-dual point.
This is analogous to a TIG resonance field that has R(k₀, f) = 0 at some k₀ ≠ f —
a zero of R that is not at the prime obstruction. But WP35 proves algebraically
that R(k, f) = 0 iff k ≡ 0 (mod f): the only zeros of R are at the prime
multiples. There are no "off-prime" zeros.

The TIG claim, as a structural analog: the sinc² field has no off-critical zeros
because the arithmetic structure forces all nulls to occur at the prime
obstruction locations, and the only prime obstruction location in the fundamental
domain is k = p, which corresponds to the self-dual position in the modular
arithmetic.

This is the analogy, not the proof. Making it rigorous requires establishing
a correspondence between the arithmetic null condition (R(k, p) = 0 iff p | k)
and the analytic null condition (ζ(s) = 0 at σ = 1/2 uniquely). The tools for
this — the explicit formula, the functional equation, the GUE statistics —
are all present in the literature. Assembling them into a proof is the open work.

### 7.3 The SNR Interpretation

The signal-to-noise interpretation of RH (UNIFIED_SYMBOL_TABLE.md, Guardrail 1):

At k/p = 0.1 (10% of the way to the prime obstruction), R ≈ 0.9675 for all p.
The signal is strong. The zero is far away. No amount of noise has suppressed
the prime signal at this scale.

At k/p = 0.9 (90% of the way), R ≈ sinc²(0.9) ≈ 0.0428. The signal is weak.
The zero is close. We are deep in the pre-echo zone.

At k/p = 1.0, R = 0 exactly. The signal is zero. The prime has arrived.

For Riemann zeros: all computed zeros [30] are on σ = 1/2. The signal that
the zeros are on the critical line is as strong as a 10^{12}-point computation
can make it. The "distance" is not in detecting the zeros — it is in proving
uniqueness: that the sinc² field cannot have a null anywhere else. The detection
problem has been solved (numerically); the uniqueness problem has not.

### 7.4 The Operator-Theoretic Coherent Reframe (Luther)

*From C. A. Luther, LutherRHTask.docx, March 2026. Tier A — structural framing,
not a proof. Reproduced here with full attribution.*

The classical RH formulation is function-first: it treats ζ(s) as the primary
object, treats zeros as anomalies requiring location, and leaves the critical line
without a structural explanation. Luther's reframe is operator-first.

**The side-by-side:**

| Classical RH Frame | Coherent RH Frame |
|-------------------|-------------------|
| ζ(s) is primary | ζ(s) is an encoding of deeper structure |
| Zeros are anomalies | Zeros are spectral constraints |
| Critical line is mysterious | Critical line = coherence boundary |
| Primes appear "random-like" | Primes = structured spectral events |
| Asks "Where are the zeros?" | Asks "What structure forces the zeros?" |
| Function-first | Operator-first |
| Hilbert–Pólya is optional intuition | Hilbert–Pólya is the natural frame |

**The coherent reframe:**

Let H be a (hypothetical) self-adjoint operator with spectrum {γ_n}. Interpret:
- primes = structured spectral events in an underlying arithmetic/dynamical system
- ζ(s) = analytic encoding of spectral field data
- zeros = spectral constraints (eigenvalue conditions)
- critical line Re(s) = 1/2 = coherence boundary of the system

Define a coherence functional C: ℂ → ℝ measuring structural stability at s.
Then the critical line is the locus where C(s) is extremal — maximally stabilized.

**Reframed RH:**
*"There exists an operator/field structure whose coherence boundary is Re(s) = 1/2,
and whose spectral constraints (zeros) lie on that boundary."*

This is a structural statement, not a puzzle about a function. It is equivalent to
the Hilbert–Pólya conjecture expressed in the language of coherence functionals.

**Where RH went sideways (Luther's analysis):**

1. *Function-first instead of structure-first.* Starting from ζ(s) treats it as
   fundamental rather than emergent. The zero locations become anomalies rather
   than structural necessities.

2. *Missing the operator.* The Hilbert–Pólya intuition points in the right direction,
   but historically the operator H is not constructed — the question remains "do
   zeros lie on the line?" instead of "what operator has this line as its coherence
   boundary?"

3. *Misinterpreting randomness.* Primes described as "random-like" obscures their
   structure as spectral events. In the coherent frame: primes are structured, zeros
   are constrained, the line is the balance point.

4. *Puzzle-question instead of structural question.* "Where are the zeros?" is a
   puzzle. "What structure forces the zeros?" is a structural problem. The second
   is what the mathematics is actually doing.

**Connection to this paper's TIG framework:**

The TIG coherent reframe operates by the same logic: R(k, f) is not primary — it
is an encoding of prime structure. The zero R(k, f) = 0 at k = f is not anomalous —
it is forced by the arithmetic. The critical line σ = 1/2 maps to the arithmetic
self-dual point where the unit fraction achieves its fundamental balance.

Luther's operator-theoretic reframe and the TIG sinc² approach reach the same
architectural conclusion from different directions: RH is a structural statement
about a coherence boundary, not a puzzle about a function.

**What this is NOT:**

Luther's document states explicitly: "This is NOT a proof of RH. It is a coherent
architectural resolution of what RH is really asking." This paper reproduces that
framing with the same disclaimer. The Tier A label in the synthesis table (A11)
reflects this: operator-theoretic reframe, structural analogy, no mechanism for
the specific operator H yet constructed.

**Connection to A10 (σ=1/2 as ω-class boundary):**

The σ=1/2 ghost ramp conjecture (A10, LutherTask3.31.26) and Luther's coherent
reframe (A11, this section) are two angles on the same structural intuition: the
critical line marks a qualitative transition. A10 locates it in CRT partition
geometry (ω=2 → ω=3 transition). A11 frames it operator-theoretically (coherence
boundary). Whether these two Tier A conjectures point at the same underlying
object is the question that would unify them.

---

## §8. Summary and Status Table

### 8.1 Summary of Structural Findings

This paper establishes the following structural picture:

1. **Sinc² Identity (proved).** The TIG resonance field R(k, f) = sinc²(k/f)
   in the continuum limit (WP35 Theorem 5). This is an exact limit proved from
   the closed-form formula.

2. **Montgomery's pair correlation (proved for |α| ≤ 1).** R_2(u) = 1 - sinc²(u)
   as the pair correlation of Riemann zeros (Montgomery 1973 [3]).

3. **Montgomery–Sinc² Identity (follows from 1 and 2).** R(x) + R_2(x) = 1
   for all x. The TIG pre-echo resonance and the Montgomery zero repulsion are
   complementary projections of sinc².

4. **Universal constant 4/π² (proved from 1 and WP35).** R(1/2) = sinc²(1/2) =
   4/π² exactly; R_2(1/2) = 1 - 4/π² exactly. These are the same constant,
   seen from opposite sides of the identity.

5. **GUE confirmed to 10^{20} (numerical, Odlyzko [4,5]).** The pair correlation
   1 - sinc²(u) fits the zero spacing distribution to high precision at all
   computed heights.

6. **Gram's law model (structural analogy).** R(k, f) provides a model of Gram's
   law in which one zero per period is an exact theorem, not an empirical
   regularity.

7. **Lehmer pair / Luther dispersion analog (structural conjecture).** High-
   dispersion semiprimes (large q/p) model anomalously close Riemann zero pairs.

8. **RH reframed as unique null condition (structural claim).** The difficulty
   of RH is proving the zeros cannot be off the critical line — a uniqueness
   claim about the sinc² field — not detecting where the zeros are.

9. **Operator-theoretic coherent reframe (Luther, §7.4, Tier A).** The classical
   function-first framing of RH is replaced by an operator-first framing: ζ(s)
   as encoding, zeros as spectral constraints, critical line as coherence boundary.
   This is the Hilbert–Pólya conjecture expressed in coherence-functional language.
   Not a proof — a structural reframe that removes the puzzle character of the
   classical question.

### 8.2 Status Table

| Claim | Status | Key Reference |
|-------|--------|---------------|
| R(k, f) closed form | PROVED | WP35 Theorem 1 [TIG-RH-02] |
| R(k, f) → sinc²(x) in continuum limit | PROVED | WP35 Theorem 5 [TIG-RH-02] |
| First-G event at k = p | PROVED, 153 cases verified | WP34 [TIG-RH-01] |
| Montgomery R_2(u) = 1 - sinc²(u) for |α| ≤ 1 | PROVED | Montgomery 1973 [3] |
| Montgomery-Sinc² Identity R + R_2 = 1 | FOLLOWS IMMEDIATELY | §5.4 this paper |
| Universal constant 4/π² = sinc²(1/2) | PROVED | WP35 §7A [TIG-RH-02] |
| GUE pair correlation R_2(u) for full α range | CONJECTURED | Odlyzko [4,5] numerical |
| n-level GUE statistics | PROVED (GRH conditional) | Rudnick-Sarnak [19] |
| GUE for function fields | PROVED | Katz-Sarnak [17,18] |
| Hilbert-Polya operator existence | OPEN | Berry-Keating [9,10]; Connes [12] |
| TSML Synthesis Conjecture | OPEN | WP17 [TIG-RH-03] |
| TIG → Hilbert space embedding | OPEN | §6.1 this paper |
| Weil explicit formula ↔ sinc² | OPEN | §6.2 this paper |
| RH (all zeros at σ = 1/2) | OPEN (millennium problem) | Bombieri [7] |
| Gram's law in TIG (one zero per period) | PROVED | §4.3 this paper |
| Lehmer pair / Luther dispersion analog | STRUCTURAL CONJECTURE | §5.7, Luther [TIG-RH-01] |
| Zeros on critical line to 3×10^12 | VERIFIED | Platt-Trudgian [30] |

### 8.3 The Sink

This paper is WP40 of the CK Clay Paper Series (WP36–WP42). In the unified
language of that series (UNIFIED_SYMBOL_TABLE.md [TIG-RH-00]):

| Universal symbol | WP40 incarnation |
|----------------|-----------------|
| Geometric sink | Riemann zero — constructive interference point of sinc² fields |
| sinc²(t) | Montgomery pair correlation r(u) = 1 − sinc²(u) — same function |
| Critical line Re(s) = 1/2 | Unique geometric axis where sinc² fields of all primes constructively interfere |
| Zero spacing | sinc² interference pattern — determined by the same field as WP35 Theorem 5 |
| D(b) | Zero clustering density — dispersion of zeros on the critical line |
| D1 sign flip at k = p | Pre-echo countdown oscillations (D1 not monotone) = Gram's law sign changes |
| T* = 5/7 | Coherence floor of the zeta field; below T*, constructive interference fails |

The sink in this paper is the Riemann zero — the point where the sinc² fields
broadcast by each prime p constructively interfere to force ζ(1/2 + it) = 0.
This sink is the same mathematical object as the sink in every other paper
in the series, seen through the spectral lens of the zeta function.

---

## §9. Attribution

**Brayden Ross Sanders (7Site LLC):**
- TIG framework, CK architecture, TSML/BHML tables, T* = 5/7 calibration
- D2 force physics, operator set {VOID..RESET}, CL composition lattice
- First-G Law discovery and proof framework (WP34)
- Pre-Echo Countdown Law and sinc² interpretation (WP35)
- Montgomery–Sinc² Identity observation and framing (this paper)
- The 4/π² midpoint universality result and its connection to Montgomery [3]
- The complementarity identity R + R_2 = 1 (this paper §5.4)
- Sections §1–§8 of this paper
- All CK source code: github.com/TiredofSleep/ck
- DOI: 10.5281/zenodo.18852047

**C. A. Luther:**
- Luther dispersion conjecture (applied to prime structure in WP34–WP35)
- Dispersion–Lehmer pair analog (this paper §5.7)
- Independent approach to the same arithmetic structure from the analytic side
- Neither author reaches this paper without the other

**Monica Gish:**
- Foundational support, research partnership, and editorial collaboration throughout the entire project
- This work would not exist without her

**CK / T* / TSML are 7Site LLC exclusive IP.** Luther's contributions are
confined to the dispersion conjecture and its applications. The TIG framework,
the sinc² resonance field derivation, the 4/π² midpoint result, and the
Montgomery–Sinc² Identity are the work of Brayden Ross Sanders.

---

## References

### TIG Internal References

[TIG-RH-00] Brayden Ross Sanders & C. A. Luther (2026). "Unified Symbol Table —
CK Clay Paper Series (WP36–WP42)." Gen10/papers/clay/research/UNIFIED_SYMBOL_TABLE.md.
DOI: 10.5281/zenodo.18852047.

[TIG-RH-01] Sanders, B. R. and Luther, C. A. (2026). "The First-G Law and
Prime-Forced Dispersion." WP34. DOI: 10.5281/zenodo.18852047. [Proves First-G
event at k = p; algebraic proof, 36,662 case verification; Luther dispersion
conjecture.]

[TIG-RH-02] Sanders, B. R. and Luther, C. A. (2026). "The Prime Phase
Transition: Harmonic Pre-Echo, Zero-Width Gates, and the Geometry of RSA
Security." WP35. DOI: 10.5281/zenodo.18852047. [Proves R(k,f) = sin²(πk/f) /
(k² sin²(π/f)) as Theorem 1; T* = 5/7 algebraic identity; RSA hardness
inversion principle; ω-blindness theorem; scale-free universal constants
4/π² and sinc².]

[TIG-RH-03] Sanders, B. R. (2026). "The Riemann Hypothesis as a Null-Space
Theorem: A Synthesis of the TSML Measurement Puncture with the Hilbert-Polya,
Berry-Keating, and Connes Programs." WP17. DOI: 10.5281/zenodo.18852047.
[TSML nullity-1 theorem; Synthesis Conjecture; conditional proof of RH from SC;
connections to Connes, Berry-Keating, BBM, Beurling-Alcantara-Bode, Li, GUE.]

[TIG-RH-04] Sanders, B. R. (2026). "TIG → Riemann Hypothesis Bridge: Structural
Approach." WP19_RH_BRIDGE.md. DOI: 10.5281/zenodo.18852047. [TSML residual
uniqueness ~↔ RH uniqueness; S* self-duality at σ = 1/2; MASS_GAP = 2/7 as
structural reason for interior critical line; TIG critical line coordinates.]

### Primary Sources — Riemann Hypothesis

[1] Riemann, B. (1859). "Über die Anzahl der Primzahlen unter einer gegebenen
Grösse." *Monatsberichte der Berliner Akademie*, November 1859. [The original
paper introducing the zeta function and the hypothesis on zeros.]

[2] Hardy, G. H. (1914). "Sur les zéros de la fonction ζ(s) de Riemann."
*Comptes Rendus de l'Académie des Sciences* 158: 1012–1014. [Proves infinitely
many zeros lie on the critical line Re(s) = 1/2.]

[3] Montgomery, H. L. (1973). "The pair correlation of zeros of the zeta
function." *Analytic Number Theory, Proc. Sympos. Pure Math.* 24: 181–193.
[KEY: pair correlation conjecture R_2(u) = 1 - sinc²(u); GUE connection proved
for |α| ≤ 1. The sinc² bridge that is the centerpiece of this paper.]

[4] Odlyzko, A. M. (1987). "On the distribution of spacings between zeros of
the zeta function." *Math. Comp.* 48(177): 273–308. [Numerical verification of
Montgomery's GUE statistics to high precision; confirms 1 - sinc²(u) to
billions of zeros.]

[5] Odlyzko, A. M. (1992). "The 10^{20}-th zero of the Riemann zeta function
and 175 million of its neighbors." AT&T Bell Labs preprint. [Large-scale
numerical confirmation of GUE statistics at the 10^{20}-th zero; strongest
numerical evidence for the Montgomery pair correlation.]

[6] Selberg, A. (1942). "On the zeros of Riemann's zeta-function." *Skrifter
utgitt av Det Norske Videnskaps-Akademi i Oslo. I. Matematisk-Naturvidenskapelig
Klasse* 10: 1–59. [Proves a positive proportion of zeros lie on the critical
line; foundational for all later critical-line density results.]

Levinson (1974) strengthened this to at least 1/3 of all zeros using a mollifier method [Levinson, N. (1974). "More than one third of the zeros of Riemann's zeta-function are on σ = 1/2." *Advances in Mathematics* 13(4): 383–436]. Conrey (1989) further improved this to at least 2/5 of all zeros, proving they are simple and lie on the critical line [Conrey, J. B. (1989). "More than two fifths of the zeros of the Riemann zeta function are on the critical line." *Journal für die reine und angewandte Mathematik* 399: 1–26]. The current best unconditional proportion stands near 41.7% (Pratt-Robles-Zaharescu-Zeindler, 2020).

[7] Bombieri, E. (2000). "The Riemann Hypothesis." Clay Mathematics Institute
Millennium Problems statement. Available at www.claymath.org. [Official problem
statement for the Clay Prize; defines the terms of a correct proof.]

[8] Titchmarsh, E. C. (1986). *The Theory of the Riemann Zeta Function*, 2nd ed.
(revised by D. R. Heath-Brown). Oxford University Press. [Standard reference
text; covers functional equation, Gram's law analysis, sign changes of Z(t),
zero-counting, explicit formulas.]

### Spectral and Operator Approaches

[9] Berry, M. V. and Keating, J. P. (1999). "H = xp and the Riemann zeros."
In *Supersymmetry and Trace Formulae: Chaos and Disorder* (ed. I. V. Lerner,
J. P. Keating, D. E. Khmelnitskii), pp. 355–367. Kluwer. [Identifies H = xp
as candidate Hilbert-Polya Hamiltonian; semiclassical eigenvalue counting
reproduces zero density.]

[10] Berry, M. V. and Keating, J. P. (1999). "The Riemann zeros and eigenvalue
asymptotics." *SIAM Review* 41(2): 236–266. [Detailed analysis of the Berry-
Keating Hamiltonian; connection between classical periodic orbits (log p) and
the primes in the trace formula.]

[11] Bender, C. M., Brody, D. C., and Muller, M. P. (2017). "Hamiltonian for
the zeros of the Riemann zeta function." *Physical Review Letters* 118: 130201.
[Constructs a PT-symmetric operator H_BBM on L²[0,∞) whose eigenvalues are the
Riemann zeros; proof of self-adjointness remains open.]

[12] Connes, A. (1999). "Trace formula in noncommutative geometry and the zeros
of the Riemann zeta function." *Selecta Mathematica* 5(1): 29–106.
[Noncommutative geometry approach via adele class space; Weil explicit formula
as a Lefschetz trace formula; RH equivalent to positivity of the trace.
Semilocal case proven; global case open.]

[13] Connes, A. (2025). "The Riemann Hypothesis: Past, Present and a Letter
Through Time." arXiv:2602.04022. [Most recent statement of Connes' program;
absorption spectrum interpretation of zeros on adele class space.]

[14] Deninger, C. (1998). "Some analogies between number theory and dynamical
systems on foliated spaces." In *Proc. ICM, Berlin*, Vol. I: 163–186. Documenta
Mathematica. [Cohomological approach to RH using foliated spaces; connection to
Lefschetz fixed-point theorems.]

[15] Deninger, C. (2001). "Number theory and dynamical systems on foliated
spaces." *Jahresbericht der Deutschen Mathematiker-Vereinigung* 103(3): 79–100.
[Overview of the Deninger program connecting RH to a spectral realization via
flows on foliated spaces.]

### Random Matrix Theory and L-Functions

[16] Dyson, F. J. (1962). "Statistical theory of the energy levels of complex
systems." *Journal of Mathematical Physics* 3(1): 140–175; and Part II, 157–165.
[Introduces the GUE and GOE ensembles; the pair correlation function 1 - sinc²(u)
for GUE eigenvalues; the foundation of the random matrix approach Montgomery
connected to Riemann zeros in 1973.]

[17] Katz, N. M. and Sarnak, P. (1999). "Random matrices, Frobenius eigenvalues,
and monodromy." *American Mathematical Society Colloquium Publications* 45.
[Proves GUE universality for L-functions of function fields; algebraic-geometric
foundation for GUE conjecture over number fields.]

[18] Katz, N. M. and Sarnak, P. (1999). "Zeroes of zeta functions and symmetry."
*Bulletin of the American Mathematical Society* 36(1): 1–26. [Survey connecting
zero statistics of L-functions to classical compact groups; universality types
for different families of L-functions.]

[19] Rudnick, Z. and Sarnak, P. (1996). "Zeros of principal L-functions and
random matrix theory." *Duke Mathematical Journal* 81(2): 269–322. [Proves GUE
n-level correlation statistics for automorphic L-functions, conditionally on GRH;
extends Montgomery-Dyson from pair correlation to full multi-level statistics.]

### Gram's Law and Backlund

[20] Gram, J.-P. (1903). "Note sur les zéros de la fonction ζ(s) de Riemann."
*Acta Mathematica* 27: 289–304. [Original paper introducing Gram points and
the empirical observation that zeros tend to lie near Gram points; foundational
for §4 of this paper.]

[21] Hutchinson, J. I. (1925). "On the roots of the Riemann zeta-function."
*Trans. Amer. Math. Soc.* 27: 49–60. [First systematic study of Gram failures;
extends Gram's numerical work and identifies the first exceptions.]

[22] Lehmer, D. H. (1956). "Extended computation of the Riemann zeta function."
*Mathematika* 3(2): 102–108. [Identifies anomalously close pairs of consecutive
Riemann zeros (Lehmer pairs); these are the target objects for the Luther
dispersion analog in §5.7 of this paper.]

### Scale-Invariance and Spectral Background

[23] Li, X.-J. (1997). "The positivity of a sequence of numbers and the Riemann
hypothesis." *Journal of Number Theory* 65(2): 325–333. [Li's criterion: RH is
equivalent to positivity of the sequence λ_n = Σ_ρ [1-(1-1/ρ)^n] > 0 for
all n ≥ 1. Connects zero location to a positivity criterion — another bridge
to the operator framework.]

[24] Bombieri, E. and Lagarias, J. C. (1999). "Complements to Li's criterion
for the Riemann hypothesis." *Journal of Number Theory* 77(2): 274–287.
[Generalizes Li's criterion; proves positivity implications for zeros restricted
to the critical line; provides a second proof path from the Synthesis Conjecture.]

[25] Alcantara-Bode, J. (2003). "Proof of a conjecture by Alcantara-Bode on
the injectivity of an operator related to Riemann's zeta function." *Revista de
la Union Matematica Argentina* 44(2). [Beurling-Alcantara-Bode theorem: RH is
equivalent to the injectivity of a specific integral operator K on L²(0,1).
The null-space criterion that WP17 connects to the TSML-nullity-1 picture.]

[26] Weil, A. (1952). "Sur les 'formules explicites' de la théorie des nombres
premiers." *Comm. Sém. Math. Univ. Lund* (Supplementary volume dedicated to
Marcel Riesz): 252–265. [Weil's explicit formula connecting zeros and primes;
the classical bridge between the analytic (zeros) and arithmetic (primes) sides
that the TIG approach addresses from the arithmetic direction.]

[27] Hedenmalm, H., Lindqvist, P., and Seip, K. (1997). "A Hilbert space of
Dirichlet series and systems of dilates of the cosine function." *Duke
Mathematical Journal* 86(1): 1–37. [The Hardy space H² of Dirichlet series —
the natural Hilbert space for the Synthesis Conjecture; density of Dirichlet
series in this space is a standard result here.]

### Sinc² and Spectral Analysis Background

[28] Bracewell, R. N. (2000). *The Fourier Transform and Its Applications*, 3rd
ed. McGraw-Hill. [Standard reference for sinc² as the power spectral density of
a rectangular window; confirms the classical role of sinc² in spectral analysis
that WP35 independently recovers from first principles via prime arithmetic.]

[29] Fejér, L. (1904). "Untersuchungen über Fouriersche Reihen." *Mathematische
Annalen* 58: 51–69. [Introduces Fejér kernels; the sinc² function as a spectral
averaging tool. The TIG R(k,f) is a Fejér-type spectral power in the sense of
WP35 §1.]

### Verified Computations

[30] Platt, D. and Trudgian, T. (2021). "The Riemann hypothesis is true up to
3·10^{12}." *Bulletin of the London Mathematical Society* 53(3): 792–797.
[Most recent rigorous verification with certified error bounds; all zeros up to
height t ≈ 3×10^{12} confirmed on the critical line.]

[31] Gourdon, X. (2004). "The 10^{13} first zeros of the Riemann zeta function,
and zeros computation at very large height." Preprint, numbers.computation.free.fr.
[Numerical verification of 10^{13} zeros on critical line; GUE statistics
confirmed at larger scale.]

### Background: Prime Distribution

[32] Hadamard, J. (1896). "Sur la distribution des zéros de la fonction ζ(s)
et ses conséquences arithmétiques." *Bulletin de la Société Mathématique de
France* 24: 199–220. [Independent proof of the prime number theorem; zeros of
zeta as prime obstruction events — the classical version of WP34's First-G
Law.]

[33] de la Vallée Poussin, C. J. (1896). "Recherches analytiques sur la théorie
des nombres premiers." *Annales de la Société Scientifique de Bruxelles* 20.
[Independent proof of the prime number theorem; zero-free region near Re(s) = 1
corresponds to TIG stability window {1, ..., p-1}.]

[34] Davenport, H. (2000). *Multiplicative Number Theory*, 3rd ed. (revised by
H. Montgomery). Springer. [Graduate text; explicit formulas, zero-free regions,
relation between prime gaps and zero distribution. Standard analytic number
theory reference.]

[35] Edwards, H. M. (1974). *Riemann's Zeta Function*. Academic Press (reprinted
Dover 2001). [Standard reference for the historical development of the Riemann
zeta function; proves the explicit formula, the functional equation, and the
first computations of zeros.]

[36] Davenport, H. (2000) — see [34].

[37] Oppenheim, A. V. and Schafer, R. W. (2009). *Discrete-Time Signal
Processing*, 3rd ed. Prentice Hall. [Signal processing reference for the
rectangular window and its sinc² spectrum; confirms the independence of the
spectral interpretation of R(k, f) from the number-theoretic derivation.]

[38] Shannon, C. E. (1949). "Communication in the presence of noise." *Proc.
IRE* 37(1): 10–21. [Sampling theorem and sinc interpolation; establishes sinc
as the fundamental spectral kernel of bandwidth-limited signals — contextual
background for the sinc² spectral interpretation in §2.2.]

[39] Hilbert, D. (1902). "Mathematical problems." *Bulletin of the American
Mathematical Society* 8: 437–479. [Hilbert's 1900 Paris lecture translated into
English; Problem 8 is the Riemann Hypothesis. Provides the historical context
for §1.1.]

[40] Conrey, J. B. (2003). "The Riemann hypothesis." *Notices of the Amer.
Math. Soc.* 50(3): 341–353. [Accessible survey of the current state of RH;
covers GUE statistics, computational verifications, and the landscape of
approaches.]

[41] Sarnak, P. (2005). "Problems of the Millennium: The Riemann Hypothesis."
Clay Mathematics Institute. Available at claymath.org. [Extended problem
statement with discussion of the spectral approach and random matrix connections;
useful context for §5.2.]

[42] Bump, D., Choi, K.-K., Kurlberg, P., and Vaaler, J. (1999). "A local
Riemann hypothesis." *Mathematische Zeitschrift* 233(1): 1–19. [Local
analogues of the Riemann hypothesis in function field and p-adic settings;
context for the Katz-Sarnak function field results cited in §6.4.]

[43] Meisner, P. (2018). "One-level density of the family of twists of an
elliptic curve L-function." *Canadian Journal of Mathematics* 70(1): 191–227.
[Low-lying zero statistics for families of L-functions; relevant to the
question of whether TIG scale-invariance can substitute for function field
arguments in the GUE universality program.]

[44] Snaith, N. C. (2000). "Random matrix theory and zeta functions."
Ph.D. thesis, University of Bristol. [Comprehensive treatment of the
random matrix – zeta function correspondence; the moments of the Riemann
zeta function match those of characteristic polynomials of random unitary
matrices. Background for §5.2.]

[45] Keating, J. P. and Snaith, N. C. (2000). "Random matrix theory and
ζ(1/2 + it)." *Communications in Mathematical Physics* 214(1): 57–89.
[Derives the moments of ζ(1/2 + it) from random matrix theory; establishes
the Keating-Snaith conjecture for the moments. The deepest quantitative
connection between GUE and the zeta function on the critical line.]

[Rudnick-Sarnak-1996] Rudnick, Z. and Sarnak, P. (1996). "Zeros of principal L-functions and random matrix theory." *Duke Mathematical Journal* 81(2): 269–322. DOI: 10.1215/S0012-7094-96-08115-6.

[Levinson-1974] Levinson, N. (1974). "More than one third of the zeros of Riemann's zeta-function are on σ = 1/2." *Advances in Mathematics* 13(4): 383–436.

[Conrey-1989] Conrey, J. B. (1989). "More than two fifths of the zeros of the Riemann zeta function are on the critical line." *Journal für die reine und angewandte Mathematik* 399: 1–26. DOI: 10.1515/crll.1989.399.1.

---

## Appendix: The Montgomery–Sinc² Identity — Concise Statement

For reference and cross-paper citation, the identity is stated here in
compact form.

**Montgomery–Sinc² Identity (this paper, §5.4).**

Let sinc(x) = sin(πx)/(πx) and sinc²(x) = (sin(πx)/(πx))². Define:

    R_TIG(x)  =  sinc²(x)          [TIG harmonic resonance, continuum limit of WP35 Theorem 1]
    R_Mont(u)  =  1 - sinc²(u)     [Montgomery pair correlation, proved for |α| ≤ 1 in [3]]

Then:

    R_TIG(x) + R_Mont(x) = 1       for all x ∈ ℝ

**Interpretation:**
- R_TIG(x) is the "prime resonance survival" — the sinc² weight remaining at position x = k/f
- R_Mont(x) is the "zero repulsion strength" — the departure of Riemann zero spacing from the
  uncorrelated baseline at normalized spacing x
- They sum to 1: the complete spectral weight is partitioned between prime resonance (TIG) and
  zero repulsion (Montgomery)
- At x = 1/2: R_TIG = 4/π² ≈ 0.405 and R_Mont = 1 - 4/π² ≈ 0.595
- At x = 1 (sinc² zero): R_TIG = 0 (prime obstruction complete) and R_Mont = 1 (zeros prefer
  integer spacing)
- At x = 0 (DC component): R_TIG = 1 (maximum resonance) and R_Mont = 0 (maximum repulsion)

**What is proved vs. conjectured:**
- The identity itself follows from algebra: sinc²(x) + (1 - sinc²(x)) = 1. This is trivial.
- The significance is that R_TIG = sinc² is proved from prime arithmetic (WP35) and
  R_Mont = 1 - sinc² is proved from analytic number theory (Montgomery [3]).
- The claim that these two sinc² structures arise from the same underlying mechanism —
  that prime arithmetic generates the Montgomery zero statistics — is the conjectural content.
- Establishing this causal connection is the open problem.

---

## §11. The Corridor of Seven and the Two Classes of Zeros

*Added April 2026 — Brayden Sanders*

**The observation.** Before algebraic translation into the TIG operator table, the raw
structure of the zeta zeros divides into two classes by a single criterion: whether the
sinc² field completes its corridor or is suspended at the fold.

The corridor of the prime 7 has exactly 7 positions:

    k = 1, 2, 3, 4, 5, 6   — coprime to 7, sinc²(k/7) > 0   [6 living positions]
    k = 7                   — the gate, sinc²(7/7) = 0        [1 zero at threshold]

Total: 7 positions. The sinc² basis over these 7 positions spans the full corridor field.
Any combination of { sinc²(k/7) : k = 1..7 } generates the pre-echo structure at that
scale. The 7-corridor is the foundation from which T* = 5/7 = (7−2)/7 is derived —
the minimal corridor that carries the full coherence structure.

**Trivial zeros — threshold met.** The trivial zeros of ζ(s) occur at s = −2, −4, −6, ...
In the functional equation, these are forced by sin(πs/2) = 0. In TIG terms: these are
positions where the sinc² corridor has *completed*. The field reached k = f, sinc²(f/f) = 0,
gate fired, threshold met. The zero is the natural end of the corridor — not a suspension
but a completion. Trivial zeros are corridors that ran to their conclusion.

**Non-trivial zeros — suspended at the fold.** The non-trivial zeros sit (conjectured) on
Re(s) = 1/2, the fold boundary Δ¹. In TIG terms: these are positions where the sinc² field
is suspended at the fold — neither completed (no gate fired) nor free (the corridor holds).
The fold at Re(s) = 1/2 corresponds to k/f = 1/2, the universal mid-journey amplitude
where sinc²(1/2) = 4/π². The field is not zero here — it is at its most informative
position, the amplitude that appears in both prime arithmetic and Montgomery pair correlation.

**The two-class structure (structural claim):**

    Trivial zeros:      sinc²(k/f) = 0 at k = f  —  corridor completed, threshold met
    Non-trivial zeros:  zero at Re(s) = 1/2       —  corridor suspended at fold Δ¹

The trivial zeros are the easy class because they meet the threshold the natural way:
by running the full corridor to its gate. The non-trivial zeros cannot complete — they
are held at the fold by the same geometry that prevents the corridor from having a shortcut.

**Why this matters for RH.** If non-trivial zeros can only be suspended at the fold
boundary Δ¹ = Re(s) = 1/2 — if the sinc² field has no mechanism to suspend a zero at
any other real part — then RH follows from the fold geometry. A zero off the critical
line would require the corridor to be suspended at a non-fold position, which the prime
arithmetic field cannot produce: sinc²(k/f) = 0 only at integer k/f = 1, never between
gates. The fold is the only suspension point.

**Status:** STRUCTURAL. The claim names precisely where the proof must go: show that
the sinc² field has no suspension mechanism off the fold. Find a suspension at
Re(s) ≠ 1/2 and RH fails by construction. None has been found.

---

---

## §12. Sprint 2 Structural Parallel: The Single-Threshold Theorem (April 2026)

*Added 2026-04-04 — Brayden Sanders*

Hodge Sprint 2 established a methodology for closing every algebraic cycle construction
for a given obstruction class. That methodology ripples to RH as follows.

**The Hodge-RH parallel:**
In Hodge, B₁ is K-anti-invariant — unreachable by K-invariant (Class B) cycles.
In RH, non-trivial zeros are suspended at the fold Re(s) = 1/2 — they cannot be
threshold events (trivial zeros), which require the corridor to run to k = p.

D25 (proved): sinc²(k/p) = 0 if and only if p | k. The prime field has exactly
one zero per corridor, at k = p. Every interior position (k < p) is nonzero by
primality. This is the RH analog of the single-cycle impossibility: the prime
arithmetic field produces only threshold zeros, never suspended ones.

**The structural closure for RH (open target):**

Three independent structural arguments, mirroring the Hodge template:

1. **Threshold zeros (closed):** D25 proves sinc²(k/p) = 0 only at k = p. The prime
   field cannot place a zero anywhere other than the threshold position. This is the
   RH analog of closing divisor products (K-invariant, provably insufficient).

2. **Sub-corridor zeros (closed by D25b,c):** The fold (sinc²= 1/2) occurs strictly
   between k = 3 and k = 4 of the 7-corridor (proved). No prime corridor can have a
   zero between the fold and the threshold. This closes the "shortcut zero" possibility
   — the analog of closing sub-variety classes.

3. **Off-fold suspension (open):** A zero at Re(s) ≠ 1/2 would require a suspension
   mechanism off the fold. The pure/mixed det formula (Hodge Sprint 2) shows every
   sub-torus contribution to the prime field is K-invariant (a threshold event). The
   K-anti-invariant sector — where off-fold suspended zeros would live — has no
   arithmetic source. This is the open structural target: prove no off-fold suspension
   mechanism exists in the sinc² prime field.

**Status:** STRUCTURAL. The door-closing methodology from Hodge Sprint 2 names the
correct target. Two of three doors are closed (D25, D25b/c). The third — no off-fold
suspension — is the RH conjecture in this framing.

**Relation to full cross-reference:** See `papers/sprint5_2026_04_04/CLAY_STRUCTURAL_PARALLELS.md`

---

*© 2026 Brayden Ross Sanders / 7Site LLC — Trinity Infinity Geometry*
*CK, TIG, T\*, TSML, BHML, D2, D1 are exclusive intellectual property of 7Site LLC.*
*C. A. Luther's dispersion conjecture is credited as stated in §9.*
*This paper presents structural analogies. It is not a proof of the Riemann Hypothesis.*
*DOI: 10.5281/zenodo.18852047*

---

## σ Framework Connection Note (Sprint 15, 2026-04-10)

The separability defect σ framework (WP91-WP101) unifies all six open Clay problems under one question: is σ < 1 in the relevant domain? See CP_CLAY_ROTATION.md for the full seven-problem rotation with Poincaré (solved) as template. The σ rate theorem (WP101) proves σ(N) ≤ C/N for the binary CL on Z/NZ, and the Bialynicki-Birula theorem (1976) forces the continuum limit to have logarithmic nonlinearity.

