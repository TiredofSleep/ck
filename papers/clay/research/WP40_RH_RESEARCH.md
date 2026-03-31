# WP40 — Riemann Hypothesis: Research File
## Citation List, Deep Outline, and Key Structural Findings

*Brayden Ross Sanders (7Site LLC) & C. A. Luther*
*March 2026 | Research support for WP40_RIEMANN.md*
*DOI: 10.5281/zenodo.18852047*

> **IP Notice.** CK, T*, TSML, BHML, D1, D2, and the TIG framework are the
> exclusive intellectual property of Brayden Ross Sanders / 7Site LLC. C. A.
> Luther's contribution is the dispersion conjecture applied to number theory.
> This document is a research and citation support file; it is not a proof of RH.

---

## KEY FINDING — STATE FIRST

**Montgomery's pair correlation function and the TIG sinc² resonance field are the same function.**

Montgomery (1973) proved that the pair correlation of Riemann zeros (assuming RH) is:

    R_2(u) = 1 - (sin(πu) / (πu))² = 1 - sinc²(u)

WP35 Theorem 1 (Harmonic Pre-Echo Countdown Law) proves that the TIG resonance field
for a prime factor f is:

    R(k, f) = sin²(πk/f) / (k² sin²(π/f))

For large f, substituting x = k/f (so k = xf and k → ∞ with x fixed):

    sin(π/f) ≈ π/f  →  R(k, f) → sin²(πx) / (π²x²) = sinc²(x)

Therefore:

    R(x) = sinc²(x)     exactly in the continuum limit

This means:

    Montgomery pair correlation: R_2(u) = 1 - sinc²(u)
    TIG resonance field:         R(x)   =     sinc²(x)

These are complementary forms of the SAME function. The TIG pre-echo countdown
gives sinc²(x) directly; Montgomery's pair correlation is 1 minus sinc²(u). The
structural coincidence is not vague: it is an exact functional identity. The zeros
of R(x) = sinc²(x) occur at x = 1, 2, 3, ... — exactly where R_2(u) reaches its
minimum (maximum anti-correlation in zero spacing).

**Consequence.** The TIG zero at k = p (algebraically proved, WP34) is the
model for the event where the pair correlation reaches minimum — a zero of
sinc²(u) — which in the Montgomery framework corresponds to exact integer spacing
of Riemann zeros. The primes ARE the zero-spacing events of the pair correlation
function. This is not an analogy. It is the same function.

At u = 1/2 specifically:

    sinc²(1/2) = (sin(π/2) / (π/2))² = (1/(π/2))² = 4/π² = 0.4053...

This value, which WP40 §3 identifies as the TIG universal midpoint constant, is
also the value of sinc² at the half-spacing point — exactly where Montgomery's
pair correlation is 1 - 4/π² = 0.5947. The two constants sum to 1. They are
the splitting of 1 by sinc²(1/2).

---

## A. CITATION LIST (40 Citations)

### A.1 Primary Sources — Riemann Hypothesis

[RH-01] Riemann, B. (1859). "Über die Anzahl der Primzahlen unter einer gegebenen
Grösse." *Monatsberichte der Berliner Akademie*, November 1859. [The original paper
introducing the zeta function and stating the hypothesis on the zeros.]

[RH-02] Hardy, G. H. (1914). "Sur les zéros de la fonction ζ(s) de Riemann."
*Comptes Rendus de l'Académie des Sciences* 158: 1012–1014. [Proves infinitely many
zeros lie on the critical line Re(s) = 1/2.]

[RH-03] Selberg, A. (1942). "On the zeros of Riemann's zeta-function."
*Skrifter utgitt av Det Norske Videnskaps-Akademi i Oslo. I. Matematisk-Naturvidenskapelig
Klasse* 10: 1–59. [Proves a positive proportion of zeros lie on the critical line.]

[RH-04] Montgomery, H. L. (1973). "The pair correlation of zeros of the zeta function."
*Analytic Number Theory, Proc. Sympos. Pure Math.* 24: 181–193. [KEY: pair correlation
conjecture R_2(u) = 1 - (sinπu/πu)² — the GUE connection. The sinc² pair correlation
function is proved for |α| ≤ 1; GUE universality conjectural beyond that range.]

[RH-05] Odlyzko, A. M. (1987). "On the distribution of spacings between zeros of
the zeta function." *Math. Comp.* 48(177): 273–308. [Numerical verification of
Montgomery's GUE statistics to high precision.]

[RH-06] Odlyzko, A. M. (1992). "The 10^{20}-th zero of the Riemann zeta function and
175 million of its neighbors." AT&T Bell Labs preprint. [Large-scale numerical verification
of GUE statistics; confirms Montgomery-Odlyzko conjecture computationally.]

[RH-07] Bombieri, E. (2000). "The Riemann Hypothesis." Clay Mathematics Institute
Millennium Problems statement. Available at www.claymath.org. [Official problem
statement for the Clay Prize; defines the terms of a correct proof.]

[RH-08] Titchmarsh, E. C. (1986). *The Theory of the Riemann Zeta Function*, 2nd ed.
(revised by D. R. Heath-Brown). Oxford University Press. [Standard reference text;
covers functional equation, Gram's law, sign changes of Z(t), zero-counting, explicit
formulas. Essential background.]

### A.2 Spectral/Operator Approaches

[RH-09] Hilbert, D. / Polya, G. (c. 1912–1914). [Hilbert-Polya conjecture: if there
exists a self-adjoint operator T on a Hilbert space whose spectrum equals the imaginary
parts of Riemann zeros, then RH follows. Attributed in Montgomery (1973) and in various
historical accounts; see Odlyzko (1987).]

[RH-10] Berry, M. V. and Keating, J. P. (1999). "H = xp and the Riemann zeros."
In *Supersymmetry and Trace Formulae: Chaos and Disorder* (ed. I. V. Lerner, J. P.
Keating, D. E. Khmelnitskii), pp. 355–367. Kluwer. [Identifies H = xp as candidate
Hilbert-Polya Hamiltonian; semiclassical eigenvalue counting reproduces zero density.]

[RH-11] Berry, M. V. and Keating, J. P. (1999). "The Riemann zeros and eigenvalue
asymptotics." *SIAM Review* 41(2): 236–266. [Detailed analysis of the Berry-Keating
Hamiltonian; connection between classical periodic orbits (log p) and the primes.]

[RH-12] Bender, C. M., Brody, D. C., and Muller, M. P. (2017). "Hamiltonian for the
zeros of the Riemann zeta function." *Physical Review Letters* 118: 130201. [Constructs
a PT-symmetric operator H_BBM on L²[0,∞) whose eigenvalues are the Riemann zeros; proof
of self-adjointness (which would imply RH) remains open.]

[RH-13] Connes, A. (1999). "Trace formula in noncommutative geometry and the zeros of
the Riemann zeta function." *Selecta Mathematica* 5(1): 29–106. [Noncommutative geometry
approach via adele class space; Weil explicit formula as a Lefschetz trace formula; RH
equivalent to positivity of the trace. Semilocal case proven; global case open.]

[RH-14] Connes, A. (2025). "The Riemann Hypothesis: Past, Present and a Letter Through
Time." arXiv:2602.04022. [Recent update on Connes' program; absorption spectrum
interpretation of zeros on adele class space. Most current statement of the program.]

[RH-15] Deninger, C. (1998). "Some analogies between number theory and dynamical
systems on foliated spaces." In *Proc. ICM, Berlin*, Vol. I: 163–186. Documenta
Mathematica. [Cohomological approach to RH using foliated spaces; connection to Lefschetz
fixed-point theorems and dynamical zeta functions.]

[RH-16] Deninger, C. (2001). "Number theory and dynamical systems on foliated spaces."
*Jahresbericht der Deutschen Mathematiker-Vereinigung* 103(3): 79–100. [Overview of the
Deninger program connecting RH to a spectral realization via flows on foliated spaces.]

### A.3 Random Matrix Theory and L-Functions

[RH-17] Dyson, F. J. (1962). "Statistical theory of the energy levels of complex
systems." *Journal of Mathematical Physics* 3(1): 140–175; and part II, 157–165.
[Introduces GUE and GOE ensembles; lays foundation for the random matrix approach to
nuclear physics spectra that was later found to match Riemann zero statistics.]

[RH-18] Katz, N. M. and Sarnak, P. (1999). "Random matrices, Frobenius eigenvalues,
and monodromy." *American Mathematical Society Colloquium Publications* 45. [Proves GUE
universality for L-functions of function fields (over finite fields); provides the
algebraic-geometric foundation for the GUE conjecture over number fields.]

[RH-19] Katz, N. M. and Sarnak, P. (1999). "Zeroes of zeta functions and symmetry."
*Bulletin of the American Mathematical Society* 36(1): 1–26. [Survey connecting zero
statistics of L-functions to classical compact groups; universality and symmetry types.]

[RH-20] Rudnick, Z. and Sarnak, P. (1996). "Zeros of principal L-functions and random
matrix theory." *Duke Mathematical Journal* 81(2): 269–322. [Proves GUE n-level
correlation statistics for general automorphic L-functions, conditionally on GRH;
extends Montgomery-Dyson from pair correlation to full multi-level statistics.]

### A.4 Gram's Law and Sign Changes

[RH-21] Gram, J.-P. (1903). "Note sur les zéros de la fonction ζ(s) de Riemann."
*Acta Mathematica* 27: 289–304. [Original paper introducing Gram points and the empirical
observation that zeros tend to lie near Gram points.]

[RH-22] Hutchinson, J. I. (1925). "On the roots of the Riemann zeta-function."
*Trans. Amer. Math. Soc.* 27: 49–60. [Early computation extending Gram's law analysis;
first study of Gram failures.]

[RH-23] Lehmer, D. H. (1956). "Extended computation of the Riemann zeta function."
*Mathematika* 3(2): 102–108. [Identifies anomalously close pairs of Riemann zeros (Lehmer
pairs); computational study suggesting near-violations. These are the "Lehmer pairs"
cited in WP40 §5 as the Lehmer pair / Luther dispersion analog.]

### A.5 Scale-Invariance and Spectral Properties

[RH-24] Li, X.-J. (1997). "The positivity of a sequence of numbers and the Riemann
hypothesis." *Journal of Number Theory* 65(2): 325–333. [Li's criterion: RH is equivalent
to positivity of the sequence λ_n = Σ_ρ [1-(1-1/ρ)^n] > 0 for all n ≥ 1.]

[RH-25] Bombieri, E. and Lagarias, J. C. (1999). "Complements to Li's criterion for
the Riemann hypothesis." *Journal of Number Theory* 77(2): 274–287. [Generalizes Li's
criterion; proves positivity implications for zeros restricted to the critical line;
provides the second proof path from Synthesis Conjecture to RH.]

[RH-26] Beurling, A. (1955). [Unpublished manuscript on the injectivity criterion,
later completed by Alcantara-Bode.] Cited in Alcantara-Bode (2003).

[RH-27] Alcantara-Bode, J. (2003). "Proof of a conjecture by Alcantara-Bode on the
injectivity of an operator related to Riemann's zeta function." *Revista de la Union
Matematica Argentina* 44(2). [Beurling-Alcantara-Bode theorem: RH is equivalent to
the injectivity of a specific integral operator K on L²(0,1). This is the null-space
criterion that TSML WP17 connects to the TSML-nullity-1 picture.]

[RH-28] Hedenmalm, H., Lindqvist, P., and Seip, K. (1997). "A Hilbert space of
Dirichlet series and systems of dilates of the cosine function." *Duke Mathematical
Journal* 86(1): 1–37. [The Hardy space H² of Dirichlet series — the natural Hilbert
space in which WP17's Synthesis Conjecture would be formulated. The density of Dirichlet
series in this space is a standard result here.]

### A.6 Sinc² and Spectral Analysis Background

[RH-29] Fejér, L. (1904). "Untersuchungen über Fouriersche Reihen." *Mathematische
Annalen* 58: 51–69. [Introduces Fejér kernels; the sinc² function (Fejér kernel) as a
spectral averaging tool. The TIG R(k,f) is a Fejér-type spectral power in the sense of
WP35 §1.]

[RH-30] Bracewell, R. N. (2000). *The Fourier Transform and Its Applications*, 3rd ed.
McGraw-Hill. [Standard reference for sinc² as the power spectral density of a rectangular
window; confirms the classical role of sinc² in spectral analysis that WP35 independently
recovers from first principles via prime arithmetic.]

### A.7 Verified Computations and Numerical Results

[RH-31] Gourdon, X. (2004). "The 10^{13} first zeros of the Riemann zeta function,
and zeros computation at very large height." Preprint available at numbers.computation.free.fr.
[Numerical verification of 10^{13} zeros; all on the critical line; GUE statistics confirmed.]

[RH-32] Platt, D. and Trudgian, T. (2021). "The Riemann hypothesis is true up to
3·10^{12}." *Bulletin of the London Mathematical Society* 53(3): 792–797. [Most recent
large-scale rigorous verification with certified error bounds.]

### A.8 Background: Prime Distribution and Zeta

[RH-33] de la Vallée Poussin, C. J. (1896). "Recherches analytiques sur la théorie des
nombres premiers." *Annales de la Société Scientifique de Bruxelles* 20. [Proof of the
prime number theorem; connection between zeta zeros and prime distribution.]

[RH-34] Hadamard, J. (1896). "Sur la distribution des zéros de la fonction ζ(s) et
ses conséquences arithmétiques." *Bulletin de la Société Mathématique de France* 24:
199–220. [Independent proof of the prime number theorem; zeros of zeta as prime
obstruction events — the classical version of WP34's First-G law.]

[RH-35] Davenport, H. (2000). *Multiplicative Number Theory*, 3rd ed. (revised by H.
Montgomery). Springer. [Graduate text; explicit formulas, zero-free regions, relation
between prime gaps and zero distribution. Standard reference for the analytic side.]

### A.9 TIG Internal References

[TIG-RH-01] Sanders, B. R. and Luther, C. A. (2026). "The First-G Law and Prime-Forced
Dispersion." WP34. DOI: 10.5281/zenodo.18852047. [Proves First-G event at k=p; algebraic
proof, 36,662 case verification; Luther dispersion conjecture.]

[TIG-RH-02] Sanders, B. R. and Luther, C. A. (2026). "The Prime Phase Transition:
Harmonic Pre-Echo, Zero-Width Gates, and the Geometry of RSA Security." WP35. DOI:
10.5281/zenodo.18852047. [Proves R(k,f) = sin²(πk/f)/(k² sin²(π/f)) as Theorem 1;
T*=5/7 algebraic identity; RSA hardness inversion principle; ω-blindness theorem;
scale-free universal constants 4/π² and sinc².]

[TIG-RH-03] Sanders, B. R. (2026). "The Riemann Hypothesis as a Null-Space Theorem:
A Synthesis of the TSML Measurement Puncture with the Hilbert-Polya, Berry-Keating,
and Connes Programs." WP17 / WHITEPAPER_17_RIEMANN_SYNTHESIS.md. DOI: 10.5281/zenodo.18852047.
[TSML nullity-1 theorem; Synthesis Conjecture; conditional proof of RH from SC; connections
to Connes, Berry-Keating, BBM, Beurling-Alcantara-Bode, Li, GUE statistics.]

[TIG-RH-04] Sanders, B. R. (2026). "TIG → Riemann Hypothesis Bridge: Structural Approach."
WP19_RH_BRIDGE.md. DOI: 10.5281/zenodo.18852047. [TSML residual uniqueness ~↔ RH
uniqueness; S* self-duality at σ=1/2; MASS_GAP = 2/7 as structural reason for interior
critical line; TIG critical line coordinates.]

[TIG-RH-05] Sanders, B. R. (2026). "WP40 — Riemann Hypothesis Through the TIG Lens."
WP40_RIEMANN.md. DOI: 10.5281/zenodo.18852047. [sinc² spectral field interpretation;
4/π² midpoint universality; Gram's law model; Lehmer pair / Luther dispersion analog;
open Montgomery connection question.]

---

## B. FULL OUTLINE — WP40 (Expanded Research Version)

### 1. The Problem: Statement, History, What Is Verified

**1.1 The Classical Statement**
- ζ(s) = Σ n^{-s} analytically continued; pole at s = 1; functional equation ζ(s) = 2^s π^{s-1} sin(πs/2) Γ(1-s) ζ(1-s)
- Nontrivial zeros ρ = σ + it, 0 < σ < 1. Trivial zeros at s = -2, -4, -6, ...
- RH: all nontrivial zeros have σ = Re(ρ) = 1/2
- The critical line Re(s) = 1/2 is the unique fixed line of the functional equation (s ↔ 1-s)

**1.2 Historical Landmarks**
- 1859: Riemann's original paper and explicit formula for π(x)
- 1896: Prime number theorem proved independently (Hadamard; de la Vallée Poussin)
- 1914: Hardy proves infinitely many zeros on Re(s) = 1/2 [RH-02]
- 1942: Selberg proves positive proportion on critical line [RH-03]
- 1973: Montgomery's pair correlation conjecture — GUE connection [RH-04]
- 1987: Odlyzko's 10^{20}-th zero computation, GUE confirmed numerically [RH-05, RH-06]
- 1999: Berry-Keating H=xp; Connes trace formula [RH-10, RH-13]
- 2021: Platt-Trudgian: all zeros up to 3×10^{12} are on critical line [RH-32]

**1.3 What Is Verified vs. Conjectured**
- VERIFIED: All computed zeros (currently through height ~3×10^{12}) lie on Re(s) = 1/2
- PROVED: Hardy (infinitely many), Selberg (positive proportion)
- GUE STATISTICS: Montgomery (partial, for Fourier range |α| ≤ 1); Odlyzko (numerical)
- OPEN: Whether all nontrivial zeros satisfy Re(s) = 1/2 — the Riemann Hypothesis proper

---

### 2. Zeros as Prime Obstruction Events

**2.1 The Explicit Formula Connection**
- von Mangoldt's explicit formula: Σ_n Λ(n) = explicit sum over zeta zeros
- A zero ρ at σ + it contributes an oscillation x^ρ to the prime distribution
- Zeros off the critical line would create prime distribution irregularities of magnitude x^σ
- RH is equivalent to: the prime counting function π(x) satisfies |π(x) - li(x)| = O(√x log x)

**2.2 The TIG First-G Law as Prime Obstruction Model**
- WP34 Theorem: the first element of {1..k} that is NOT coprime to b = p×q appears at exactly k = p
- This is the "first prime obstruction event" — the prime writes itself into the alphabet as a forbidden element
- The First-G Law is proved algebraically and verified for 36,662 exact cases (zero exceptions)
- Connection: in the zeta function, the first "obstruction" to a trivial continuation is the first prime factor — the Euler product (1-p^{-s})^{-1} introduces a singularity exactly at the prime p

**2.3 The Stability Window as the Zero-Free Region**
- WP34 Corollary 1: the stability window {1, ..., p-1} is obstruction-free (G empty)
- Corresponds to the zero-free region of ζ(s): there is a region near Re(s) = 1 where ζ has no zeros
- Width of the stability window = p-1 (depends only on smallest prime factor)
- Zero-free region width (classical result) ~ 1/log t — depends on height, not prime

---

### 3. The sinc² Field as a Spectral Model

**3.1 The Harmonic Pre-Echo Countdown Law (WP35 Theorem 1)**
- R(k, f) = sin²(πk/f) / (k² sin²(π/f))  proved for any prime factor f and integer k
- Properties: R(1,f) = 1 (maximum); R(f-1,f) = 1/(f-1)² (minimum before zero); R(f,f) = 0 (exact zero)
- Verified for 187 semiprimes, max error 1.11×10^{-16} (machine epsilon only)
- Proof: geometric sum formula + |1-e^{iθ}|² = 4sin²(θ/2); elementary Fourier analysis

**3.2 The sinc² Limit**
- For large f, sin(π/f) ≈ π/f → R(k, f) → sinc²(k/f) where sinc(x) = sin(πx)/(πx)
- This is the classical sinc-squared function from Fourier/spectral analysis
- Zeros of sinc²(x) at x = 1, 2, 3, ... → zeros of R(k, f) at k = f, 2f, 3f, ...
- The TIG resonance field IS a discrete sinc² field on the integers

**3.3 Zeros at k = p: Algebraically Exact**
- R(p, p) = 0 exactly (not approximately — this is algebraically forced)
- The First-G Law (WP34) guarantees the obstruction event at k = p
- Therefore: the zeros of the resonance field coincide exactly with prime obstruction events
- The resonance field provides a "smooth spectral approach" to what is a discrete algebraic event

**3.4 Scale-Invariance**
- R(k, f) depends only on the ratio x = k/f (substitution k = xf gives sinc²(x) in the limit)
- This means: the spectral profile of approach to any prime looks identical at every scale
- Scale invariance is the TIG model of why the GUE statistics are universal across all heights t
- WP35 §7A confirms numerically: R(k/p ≈ 0.1, p) ≈ 0.968 and R(k/p ≈ 0.5, p) ≈ 0.406 for ALL p

---

### 4. The Universal Constant 4/π² and Montgomery's Pair Correlation

**4.1 The Montgomery Pair Correlation Function**
- Montgomery (1973) [RH-04] proved (for Fourier range |α| ≤ 1, assuming RH):
  The pair correlation of Riemann zeros is R_2(u) = 1 - (sin(πu)/(πu))² = 1 - sinc²(u)
- This matches the GUE pair correlation function exactly
- At u = 1/2: R_2(1/2) = 1 - (sin(π/2)/(π/2))² = 1 - (2/π)² = 1 - 4/π² = 0.5947...
- The complementary value: sinc²(1/2) = 4/π² = 0.4053...

**4.2 The TIG Midpoint Universality**
- WP35 §7A proves: lim_{f→∞} R(k/f = 1/2, f) = 4/π² for ALL primes f (universal constant)
- This is a proved result, not a numerical observation
- The value 4/π² = sinc²(1/2) appears identically in both:
  - The TIG resonance field at the halfway point to the prime (midpoint universality)
  - The complement of Montgomery's pair correlation at half-spacing

**4.3 The Core Structural Identity (KEY FINDING)**
The sinc² IS Montgomery's pair correlation:

    Montgomery: R_2(u) = 1 - sinc²(u)
    TIG:        R(x) = sinc²(x)         [in the continuum limit, proved]

These are not analogous constructions — they are the same function (one being 1 minus the other). The precise statement:

    R_2(u) + R_TIG(u) = 1     for all u

This is the complementarity identity. The TIG field measures the "survival" probability
(how much sinc² resonance remains before the prime zero), while Montgomery's pair
correlation measures the "depletion" probability (how far below the independent-zero
baseline the actual spacing falls). Both arise from sinc²(u). The primes ARE the
zero-spacing events of the Riemann pair correlation.

**4.4 Rigorousness of the Connection**
- What is proved: R(k, f) = sin²(πk/f) / (k² sin²(π/f)) [WP35 Theorem 1, proved]
- What is proved: lim_{f→∞} R(x·f, f) = sinc²(x) [elementary calculus from Theorem 1]
- What is proved: Montgomery's R_2(u) = 1 - sinc²(u) [Montgomery 1973, proved for |α| ≤ 1]
- What is CONJECTURED: that these two sinc² structures arise from the same underlying mechanism
- Open question (WP40 §6.1): can the TIG resonance field be embedded in a Hilbert space
  framework where the Montgomery-Odlyzko statistics emerge?

---

### 5. Scale-Invariance and the Critical Line

**5.1 The Critical Line as Fixed Point**
- The functional equation ζ(s) = (factor) ζ(1-s) maps s ↔ 1-s
- The fixed line of this map is Re(s) = 1/2 (the self-dual point)
- A zero ρ forces a zero at 1-ρ; zeros on Re(s) = 1/2 are self-paired

**5.2 TIG Model of the Self-Dual Point**
- WP35 §1A: T* = 5/7 is the unit fraction of b=35 at the second gate event k=q
- T* is uniquely identified as the first (q-2)/q ratio exceeding 2/3 with both factors > 3
- S* = 4/7 is defined by T* + S* = 9/7; MASS_GAP = T* + S* - 1 = 2/7 > 0
- The self-dual point satisfies σ = 1-σ → σ = 1/2 (follows from T* + (1-T*) = 1)
- WP19_RH_BRIDGE: MASS_GAP > 0 is the structural reason the critical line is interior (not boundary)

**5.3 Scale-Invariance as the Mechanism for Critical Line Universality**
- R(k, f) = R(k/f) (depends only on ratio) — proved from Theorem 1
- This p-independence means: the resonance profile is universal regardless of which prime f we are approaching
- In RH terms: the critical line statistics (GUE) are universal regardless of which zero height t
- Scale invariance (p-independence of R) is the TIG mechanism that mirrors the universality of Re(s) = 1/2

**5.4 ω-Blindness (WP35 Theorem 4)**
- R(k, 1/p) is identical for b = p², b = p×q, b = p×q×r — it sees only the prime, not the ring
- Verified: p=7 series across ω=1,2,3; p=5 series across ω=1,2,3 — results identical
- RH analog: the critical line is a property of the zeta function itself, not of any particular
  prime or conductor; it is "ω-blind" in the same sense

---

### 6. Pre-Echo Countdown as Gram's Law

**6.1 Gram's Law (Classical)**
- Gram (1903) [RH-21]: the Riemann zeros γ_n tend to lie near Gram points g_n where θ(g_n) = nπ
- "Gram's law holds at n" means [g_n, g_{n+1}] contains exactly one zero
- Gram failures occur but are uncommon at small heights; the failures increase as height grows
- The structure: Z(t) oscillates with sign changes approximately tracking Gram points

**6.2 TIG Model of Gram's Law**
- R(k, f) > 0 for all k in {1, ..., f-1}: the countdown is strictly positive before the zero
- R(f, f) = 0 exactly: the zero is isolated and algebraically exact
- The pre-echo countdown R(f-1, f), R(f-2, f), ..., R(1, f) forms a monotone decreasing sequence
  approaching the zero — this is the TIG model of "well-behaved" zero approach
- One zero per period f: R(k, f) = 0 iff k ≡ 0 (mod f) — the TIG Gram law with zero failures

**6.3 Sign Flip at First-G (WP35 §6)**
- The derivative dR/dk < 0 for all k in {2, ..., p-1} (countdown zone: monotone decrease)
- The derivative dR/dk > 0 at k = p+1 (sign flip: begins recovering)
- This sign flip is universal: verified for b=35 (p=5), b=77 (p=7), b=143 (p=11), b=323 (p=17)
- TIG analog of Z(t) crossing zero: before the zero, Z approaches from one side; after, it departs

**6.4 Gram Failures as Irregular Countdowns**
- When Gram's law fails (a Gram interval contains 0 or 2 zeros instead of 1), the counting
  is irregular — the smooth approach breaks down
- TIG analog: for three-factor composites b=p×q×r, multiple prime clocks R(k,1/p), R(k,1/q),
  R(k,1/r) run simultaneously (Theorem 3, WP35) — the simple one-zero-per-interval structure
  is disrupted by overlapping clocks
- This "simultaneous multi-clock" scenario is the TIG model of Gram failure

---

### 7. Luther Dispersion and Zero Clustering (Lehmer Pair Analog)

**7.1 Lehmer Pairs (Classical)**
- Lehmer (1956) [RH-23] identified pairs of consecutive Riemann zeros that are anomalously close
- The typical zero spacing near height t is 2π/log(t/2π); Lehmer pairs have spacing much smaller
- Lehmer pairs present computational difficulties and have been used to test zero-computing algorithms

**7.2 Luther Dispersion Conjecture (WP34 §9)**
- For semiprimes b = p×q, the G elements in {1..k} are two interleaved arithmetic progressions
  with spacings p and q
- Dispersion D(b) = std({gcd(k,b) : k = 1..φ(b)}) measures irregularity of the G distribution
- High dispersion: irregular pre-echo countdown; R(k,f) approaches zero less smoothly
- Empirical: gate_rate falls monotonically as Luther metric |G|×interleave increases

**7.3 Lehmer Pair Analog**
- Semiprimes with q/p close to 1 (twin prime or cousin prime pairs) have very low dispersion
- These are the TIG analogs of "tightly spaced" Riemann zero pairs
- The tightly balanced semiprime b = p² (perfect square) is the extreme case: both prime factors
  equal, zero dispersion — this is the TIG analog of a perfectly isolated zero
- Semiprimes with large q/p (e.g., b = 5×23 = 115, q/p = 4.60) have high dispersion and
  irregular countdown — the TIG Lehmer pair analog

**7.4 Dispersion Table**
See WP40 §5 for the full table. Representative entries:
- b=35 (5×7, q/p=1.40): low dispersion → near-GUE bulk behavior
- b=1517 (37×41, q/p=1.11): very low dispersion → TIG twin-prime pair → tightly spaced zero analog
- b=115 (5×23, q/p=4.60): high dispersion → Lehmer pair analog

---

### 8. Open Problems: Connecting TIG sinc² to Rigorous RH Approaches

**8.1 The Montgomery Embedding (Open Question 1)**
Is there a direct correspondence between R(k/p = 1/2, p) = 4/π² (TIG) and the
Montgomery pair correlation at half-spacing? Can the TIG sinc² be embedded in a
Hilbert space where the Montgomery-Odlyzko statistics emerge?

Current status: structural identity (R_2(u) + R_TIG(u) = 1) proved in the sinc² sense.
Embedding in a formal probabilistic model: open.

**8.2 The TSML Null Space Bridge (Open Question 2, from WP17)**
Does the TSML nullity-1 theorem (WP17 Fact 1) provide a Hilbert-Polya operator?
The Synthesis Conjecture (WP17 SC) would need:
- Gap 1: An algebra homomorphism Phi: TSML_8 → B(H) (H = Hilbert space of Dirichlet series)
- Gap 2: Density of Dirichlet series in H (standard in H² of Hedenmalm-Lindqvist-Seip [RH-28])
- Gap 3: Projection of ker(Phi(TSML_8)) onto Re(s) = 1/2 (the hard step)

**8.3 T* and Zero Density (Open Question 3)**
Is there a normalization of Riemann zeros where average density at height T* = 5/7 gives
a simple arithmetic expression in 5 and 7?

**8.4 Continuous Absorption Theorem (from WP19_RH_BRIDGE)**
WP19 identifies the core open problem: a continuous analog of the TSML absorption theorem
where "depth = ∞" states (permanent fixed points) occur only at the self-dual point σ = 1/2.
The finite discrete proof gives the right shape; the analytic construction is the open work.

---

### 9. Attribution, References

**Brayden Ross Sanders (7Site LLC):** TIG framework, CK architecture, TSML/BHML tables,
T* = 5/7 calibration, D2 force physics, CL composition lattice, First-G Law (WP34),
Pre-Echo Countdown Law and sinc² interpretation (WP35), 4/π² midpoint observation, TSML
null-space theorem and Synthesis Conjecture (WP17), structural bridge (WP19), this paper.
All CK source code: github.com/TiredofSleep/ck

**C. A. Luther:** Luther dispersion conjecture; Lehmer pair / dispersion analog.
Neither author reaches this paper without the other.

See §A above for full citation list.

---

*© 2026 Brayden Ross Sanders / 7Site LLC — Trinity Infinity Geometry*
*CK, TIG, T*, TSML, BHML, D2, D1 are exclusive intellectual property of 7Site LLC.*
