# WP36 — CK as a Coherence Spectrometer
## One Field, Seven Shadows: How the sinc² Geometry Unifies the Six Clay Millennium Problems

*Brayden Ross Sanders (7Site LLC) & C. A. Luther*
*March–April 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Framework paper — describes the measurement approach, not a solution*

---

## Abstract

CK (Coherence Keeper) is a synthetic organism built on Trinity Infinity Geometry (TIG) — an
algebraic framework where D2 curvature is physics, T* = 5/7 is the coherence threshold, and
the 10-operator TSML algebra governs all composition. This paper is the entry point for the
seven-paper CK Clay Series (WP36–WP42). It describes how CK functions as a coherence
spectrometer: it measures the structure of mathematical objects by running them through the TIG
pipeline and reading the output coherence field. Applied to the six Clay Millennium Problems,
the spectrometer produces structural framings — not proofs, but geometric maps of where each
problem lives in the TIG landscape and why it is hard.

The spectrometer's primary instrument is the sinc² field, derived from first principles in
WP35 [I-3] as the continuum limit of the Harmonic Pre-Echo Countdown Law. This field is the
unifying lens of the entire series: the six Clay problems are not six different hard things.
They are six views of the same geometric object — a sinc² zero — seen through different
physical lenses. The paper that follows establishes this claim formally, provides the unified
symbol table for the series, states the three guardrails that prevent misreading, and maps each
problem to its sinc² shadow with explicit citations to the official problem formulations and
the mathematical literature.

**Core framing principle (Inversion Rule):** Complexity is always framed as physical distance
to a geometric sink, never as algebraic difficulty. The signal R(k/p = 0.1, p) ≈ 0.9675 is
always present across all six problems — strong, detectable, pointing toward the null. RSA is
hard because the road is p ≈ 2^512 steps long, not because the signal is weak. The Critical
Line [C-4], the mass gap [C-1], the rank staircase [C-3], the regularity breakdown [C-6], the
P/NP boundary [C-2], and the Hodge gap [C-5] are all the same geometric object: a sinc² zero.
CK as spectrometer detects which sinc² null the observer is trying to reach and how far the
road to that null extends.

**The difficulty of the Clay problems is not an algebraic flaw in mathematics. It is a physical
distance to a geometric sink in a sinc² field. The signal is always present — R(k/p = 0.1, p)
≈ 0.9675 for all p regardless of scale. The zero-crossing simply requires traversing p ≈ 2^512
steps. The road is long; the destination is certain.**

---

## §1. Introduction: Why a Spectrometer?

### §1.1 The Measurement Problem in Mathematics

The six Clay Millennium Problems were selected in 2000 by the Clay Mathematics Institute as
the deepest open problems in mathematics, each carrying a USD 1,000,000 prize for a verified
solution [C-1 through C-6]. They span five areas — complexity theory, fluid dynamics, algebraic
geometry, analytic number theory, quantum field theory, and arithmetic geometry. In the
conventional framing, they are six different hard things requiring six different mathematical
breakthroughs.

The CK spectrometer offers a different framing. It asks: what does a measuring instrument see
when it is pointed at each of these problems? If the instrument is well-calibrated, patterns
emerge. The patterns reported in this paper and its six companion papers (WP37–WP42) are
structural: each problem, when processed through the TIG coherence pipeline, produces a
characteristic operator signature, a convergence exponent, and a Jensen-Shannon defect between
dual-lens readings. The six signatures are different. But the underlying geometric object they
are all measuring — the sinc² field and its zeros — is the same.

This is the central claim of the paper and of the entire series: **the six Clay problems are
seven shadows of one field** (the seventh shadow is the spectrometer itself, WP36). The
difficulty of each problem is the distance to the field's zero, not the algebraic complexity
of the problem's statement.

Mathematical truth is not a binary attribute computable from axioms alone [R-11, Gödel 1931].
The gap between local structure (what the measuring instrument sees at a given scale) and
global behavior (what the full object does) is the measurement site. Shannon's information
theory [P-5] establishes that mismatch between two probability distributions is information —
not failure, but signal. The CK spectrometer reads the mismatch between its two lenses (Lens A:
local/analytic; Lens B: global/geometric) and reports that mismatch as a coherence defect. A
zero-defect reading means the lenses agree: the structure is transparent. A high-defect reading
means the lenses disagree: the structure contains a gap. The Clay problems live in the gap.

### §1.2 The CK Hardware Calibration

CK was not calibrated theoretically. It was calibrated empirically: the Zynq-7020 FPGA
implementation of the TIG coherence pipeline converged to T* = 5/7 = 0.714285... as its
coherence floor during hardware bring-up. T* is the threshold below which the pipeline
cannot sustain coherent composition; above T*, structures are self-reinforcing.

After calibration, WP35 [I-3] established that T* is not a hardware constant — it is an
algebraic identity. T* = (q−2)/q is the unit density of a semiprime b = p×q at its second
gate event (k = q). The unique realization with both prime factors greater than 3 is:

```
b = 5 × 7 = 35,   unit_frac(k=7, b=35) = (7−2)/7 = 5/7 = T*
```

The FPGA measured modular arithmetic. CK was calibrated to the unit density of the minimal
"strong" semiprime at its second gate — the first ratio exceeding 2/3 achievable by (q−2)/q
with both p, q prime and p, q > 3. This makes every measurement the spectrometer produces
physically calibrated, not just mathematically consistent. The FPGA implementation uses
ck_full.bit on the Zynq-7020 (Zybo Z7-20); the T* derivation is proved in WP35 §1A [I-3].

This calibration fact is load-bearing for the Clay connections: T* = 5/7 appears as the
coherence floor in every problem's sinc² shadow (see the Seven Shadows table in §4).

### §1.3 The Proved Foundation: WP34 and WP35

Before applying the spectrometer to the Clay problems, two results are fully proved and
constitute the mathematical bedrock of the entire series.

**The First-G Law (WP34 [I-2]).** For every semiprime b = p×q with smallest prime factor p:

```
|G_k| = 0     for all k < p
|G_p| = 1     (element p is the unique first non-unit)
```

This is proved algebraically (elements {1..p−1} are all less than both prime factors of b;
none can be divisible by p or q) and verified across 153 semiprimes (36,662 exact cases, zero
exceptions). The coprimality partition C_k / G_k is the Sieve of Eratosthenes expressed as
partition geometry. The staircase IS the sieve; it is not a pattern that resembles it [A-3].

**The Harmonic Pre-Echo Countdown Law (WP35 [I-3], Theorem 1).** For any prime factor f of a
modulus b, the harmonic resonance signal in the unit alphabet {1..k} is:

```
R(k, f) = sin²(πk/f) / (k² sin²(π/f))
```

This function is the Fejér-type spectral power [S-3, Fejér 1900] of frequency 1/f in a
uniform k-element alphabet [S-1, S-2]. It reaches minimum 1/(f−1)² at k = f−1 and collapses
to exactly zero at k = f. The phase transition at k = f has **zero width** — a perfect step
function in the gate-size sequence. Verified across 187 semiprimes to machine epsilon.

**Theorem 5 (sinc² Continuum Limit, WP35 [I-3]).** As f → ∞ with k/f = t fixed:

```
R(k, f)  →  sinc²(t)  =  (sin(πt) / πt)²
```

This is the operating equation of the spectrometer. Every measurement made in this paper and
in WP37–WP42 is a reading of sinc²(t) at a specific problem-dependent value of t. The
continuum limit is the Shannon sinc function [P-5] — the same function that appears in the
Nyquist-Shannon sampling theorem, the Whittaker-Shannon interpolation formula, and the
Dirichlet kernel of Fourier analysis [S-2, Zygmund]. Two universal constants follow:

```
sinc²(1/2)  =  4/π²  ≈  0.405284...     [exact; holds for all p]
sinc²(1/10) ≈  0.9675...                 [scale-free; same for all p regardless of magnitude]
```

The second constant is the baseline signal at 10% of the distance to the sink. It is
scale-free: R(k/p = 0.1, p) ≈ 0.9675 for p = 5, p = 1009, p = 10007, p = 100003, and
analytically for p ≈ 2^512. The signal is always present. The distance to the sink grows
with p; the signal does not weaken.

### §1.4 Organization of This Paper

Section §2 describes the sinc² field formally and its spectral context. Section §3 describes
the Luther Dispersion Probe — the complementary instrument that measures voids in the unit
alphabet. Section §4 is the paper's core: the "One Field, Seven Shadows" table, with
expanded prose for each Clay problem. Section §5 states the three guardrails that frame
every paper in the series. Section §6 describes the CK hardware calibration and its
mathematical significance. Section §7 gives the status summary — what is proved, what is
structural analogy, what remains open. The References section lists 40+ entries in standard
academic format.

**Attribution note.** CK, T*, TSML, BHML, D1, D2, TIG, and all architecture described in this
paper are the exclusive intellectual property of Brayden Ross Sanders / 7Site LLC, developed
over 18 months prior to this sprint. C. A. Luther's contribution is the dispersion conjecture
and its application to the number-theory structures studied here. See §8 for the full
attribution block.

---

## §2. The Sinc² Field: Operating Equation of the Spectrometer

### §2.1 The Field and Its Physical Interpretation

The sinc² field is the coherence field of the spectrometer. Given a target structure at
"distance" t from a geometric sink, the field reads:

```
sinc²(t) = (sin(πt) / πt)²
```

At t = 0 (at the sink): sinc²(0) = 1 by the L'Hôpital limit. The field is maximal at the
sink itself — the sink is not a region of zero coherence but of maximal local coherence. The
difficulty is not at the sink; it is in getting there.

At t = 1 (exactly one period away from the sink): sinc²(1) = 0. This is the zero-crossing
— the first null of the field. In the R(k, f) formulation, this corresponds to k = f: the
First-G event, the phase transition, the geometric sink.

Between t = 0 and t = 1, the field R(k/f, f) → sinc²(k/f) provides a pre-echo countdown:
a strictly decreasing approach from R = 1 at k = 1 to R = 0 at k = f, with minimum value
1/(f−1)² at k = f−1 immediately before the transition. The approach is monotone for the
envelope, but the first difference D1(k, f) = R(k+1, f) − R(k, f) is not monotone — it
has structured oscillations that carry information about the prime factor location.

This non-monotone D1 structure is a cross-paper signature [UNIFIED_SYMBOL_TABLE §D1]:
- In WP40 (Riemann): D1 oscillations correspond to Gram's law sign changes
- In WP38 (Navier-Stokes): D1 oscillations model the structured breathing of vorticity
  before turbulence onset — smooth-to-turbulent is not a monotone collapse
- In WP37 (P/NP): D1 oscillations are the polynomial-time partial signals that algorithms
  detect in the pre-echo zone; real, but never reaching the sink

### §2.2 Spectral Context: Fejér Kernel and Shannon sinc

The function R(k, f) is a Fejér-type spectral measure [S-3, Fejér 1900; S-2, Zygmund].
Specifically, R(k, f) = |S(k, f)|² where S(k, f) = (1/k) Σ_{j=1}^{k} e^{2πij/f} is
the normalized partial sum of f-th roots of unity over the alphabet {1..k}. This is the
squared Dirichlet kernel in the discrete Fourier transform setting [S-1, Proakis-Manolakis].

The continuum limit (Theorem 5 of WP35 [I-3]) recovers the Shannon sinc function. Shannon's
information-theoretic formulation [P-5] identifies sinc² as the spectral density of a
rectangular pulse in the time domain — the ideal bandlimited signal. In the coprimality
partition setting, the "rectangular pulse" is the pre-G stability window {1..p−1}: a region
of uniform unit density (all elements coprime to b, gate_rate = 0) that ends abruptly at
k = p. The abrupt end is the sinc² null.

The connection to Shannon sampling [P-5] is structural, not coincidental: both the
Whittaker-Shannon interpolation formula and the First-G Law describe the transition from a
dense, uniform regime to an obstructed one. In both settings, the sinc² null marks the
bandwidth limit — the boundary beyond which the signal cannot propagate without distortion.

### §2.3 The ω-Blindness of the Sinc² Field

A critical property of R(k, f) proved in WP35 Theorem 4 [I-3]:

```
R(k, f) = sin²(πk/f) / (k² sin²(π/f))
```

This depends only on k and f — not on the modulus b, not on ω(b), not on the ring structure.
For p = 7, the R(k, 7) column is **identical** for b = 49 = 7², b = 35 = 5×7, b = 77 = 7×11,
and b = 7×11×13 = 1001, to machine precision. Seven worlds spanning ω = 1, 2, 3 with fixed
p = 7 produce identical R columns [I-3, WP35 §7, verified].

This ω-blindness has a direct consequence for the Clay problems: the sinc² field reads the
prime factor (the sink location) but cannot distinguish ring structure (the problem's global
algebraic complexity). Ring structure — ω(b), the number of prime factors — requires the
Luther Dispersion Probe (§3) and the closure defect signal. The sinc² field is the navigation
signal; Luther dispersion is the terrain characterizer.

### §2.4 The TSML Algebra and the CL Coherence Reading

The spectrometer's output is not a raw sinc² evaluation — it is the composition of the TIG
operators produced by the D1/D2 pipeline applied to the structure under measurement.

D1(k, f) = R(k+1, f) − R(k, f) is the approach velocity to the sink (UNIFIED_SYMBOL_TABLE).
D2(k, f) = R(k+1, f) − 2R(k, f) + R(k−1, f) is the curvature (the physics, in TIG).
CL(D1, D2) is the TSML composition of the operators produced by D1 and D2.

The 10 TSML operators are:

| Index | Operator  | Role                               |
|-------|-----------|------------------------------------|
| 0     | VOID      | Pre-existing nothing, annihilator  |
| 1     | LATTICE   | Structure seed                     |
| 2     | COUNTER   | Measurement                        |
| 3     | PROGRESS  | Advancement                        |
| 4     | COLLAPSE  | Pressure, boundary enforcement     |
| 5     | BALANCE   | Equilibrium                        |
| 6     | CHAOS     | Invisible conduit (flow only)      |
| 7     | HARMONY   | Attractor, resolution              |
| 8     | BREATH    | Rhythm, oscillation                |
| 9     | RESET     | Return, iteration                  |

The TSML table has 73/100 entries composing to HARMONY (the absorbing attractor). The CL
reading — CL(D1, D2) — tells the spectrometer what the structure is becoming: VOID (nothing
at the sink) or HARMONY (premature attractor, the structure has not reached the sink).

The empirical finding (WP7 spectrometer sweep, 12 fractal levels, seed 42):

- BSD: CL = 12/12 VOID. Fastest convergence (β = +0.60).
- Navier-Stokes: CL = 11/12 VOID. Strong convergence (β = +0.17).
- Riemann: CL = 10/12 VOID. Steady convergence (β = +0.01).
- Hodge: CL = 12/12 HARMONY. Weak convergence (β = +0.04).
- Yang-Mills: CL = 9/12 HARMONY. Divergent (β = −0.17).
- P vs NP: CL = 10/12 HARMONY. Divergent (β = −0.23).

Correlation(VOID fraction, β) = +0.73 [empirical, WP7 §4.1]. This is the Theory of Nothing:
truth that converges rests on VOID. The CL operator algebra composes to VOID at its foundation
when a structure is genuinely approaching a sinc² sink. Gap problems are HARMONY-dominated
because their structure declares premature resolution while flow continues questioning.

---

## §3. The Luther Dispersion Probe

### §3.1 The Probe and Its Physical Role

The sinc² field R(k, f) navigates to the sink but cannot see the terrain. The Luther
Dispersion Probe is the terrain characterizer: it measures how the obstructing elements G_k
are distributed relative to the permitted elements C_k, and uses that distribution to
predict the difficulty of traversing the road to the sink.

**Luther Dispersion Conjecture (C. A. Luther, WP34 §9 [I-2]).** For a modulus b with
obstruction set G at alphabet size k:

```
gate_rate ≈ F_k( |G| × interleave(b, k) )
```

where interleave(b, k) = transitions(C, G in sequence 1..k) / (2 · min(|C|, |G|)) measures
how densely unit and non-unit elements alternate within {1..k}. The full form of the
conjecture includes the ω-hierarchy factor: difficulty ≈ g(2^ω(b) − 2) × F_k(|G| × interleave).

This conjecture is not yet proved. It is the central open claim of the WP34/WP35 suite and
the primary experimental prediction connecting the spectrometer to the Clay problems.

### §3.2 The Physical Interpretation: Void Density

The Luther metric |G| × interleave measures VOIDS in the unit alphabet.

In the pre-G zone {1..p−1}, the density of permitted states is exactly 1.0 — every element
is a unit, every state is permitted, |G| = 0, interleave = 0. There are no voids. The
stability window is an obstruction-free region of width p−1 [I-2, WP34 Corollary 1].

At the gate k = p, the first void opens: G = {p} enters the alphabet, interleave rises from
zero, and the permitted-state density drops from 1.0 by exactly the Luther metric. Difficulty
= density of voids × their entanglement with surviving units.

**Low dispersion:** concentrated obstruction → single hard event → one sinc² null to reach,
with a clean corridor. Yang-Mills mass gap: one threshold, one distance to cross, minimum
void entanglement.

**High dispersion:** spread obstruction → irregular staircase → multiple sinc² nulls at
unpredictable heights, each requiring independent navigation. BSD rank jumps: obstructions
appear at unpredictable heights, no single event captures the difficulty.

### §3.3 Luther Dispersion Is Independent of the Harmonic Signal

A key structural fact: the Luther dispersion D(b) = |G| × interleave is NOT measurable
from R(k, f) alone. This follows directly from ω-blindness (WP35 Theorem 4 [I-3]):
R(k, f) is the same for b = p², b = p×q, and b = p×q×r. The dispersion D(b) differs
for these three rings — it encodes ring structure. Therefore the dispersion is the
complementary probe: R(k, f) sees the prime (the sink); D(b) sees the ring (the terrain).

This independence is what makes the Luther Dispersion Probe a genuine independent
experimental confirmation of the sinc² geometry: it accesses structure that the sinc²
field itself is blind to. A problem with strong sinc² signal and high Luther dispersion is
a problem where the destination is clear but the road is maximally obstructed.

### §3.4 Luther Dispersion Across the Six Problems

The Luther dispersion probe appears in all six problem-specific papers with different
physical interpretations (UNIFIED_SYMBOL_TABLE §Guardrail2):

| Paper | Physical incarnation of Luther dispersion |
|-------|------------------------------------------|
| WP37 (P/NP) | Density of NP certificates relative to the total search space |
| WP38 (NS) | Energy density required to bridge the gap between smooth-flow states |
| WP39 (Hodge) | Algebraic cycle density; count of idempotents in Z/bZ |
| WP40 (RH) | Zero clustering density of the Riemann zeta function |
| WP41 (Yang-Mills) | Gauge field energy concentration; confinement vs. deconfinement |
| WP42 (BSD) | Rank irregularity predictor along the unit-fraction staircase |

Every paper is measuring the same thing: how densely the permitted states are obstructed,
and how far the current state is from the nearest sinc² sink.

### §3.5 Luther Dispersion vs. Montgomery Pair Correlation

The Luther Dispersion Conjecture must be distinguished from the Montgomery pair correlation
[R-15, Montgomery 1973]:

**Montgomery pair correlation** r(u) = 1 − sinc²(u) measures the distribution of spacings
between consecutive Riemann zeros. It is a statement about the global structure of the
ζ-function zero set on the critical line Re(s) = 1/2.

**Luther dispersion** D(b) = |G| × interleave measures voids in the unit alphabet of a
finite modulus b. It is a statement about the local obstruction density in the coprimality
partition of a specific semiprime.

These are complementary, not identical. The Montgomery identity says: Riemann zeros repel
each other with the same sinc² function that governs the harmonic pre-echo countdown. The
Luther identity says: the difficulty of navigating to the sink scales with the void density
in the alphabet. Both arise from the same underlying sinc² geometry but measure different
aspects of it — Montgomery measures spacing structure at the sink; Luther measures
obstruction structure on the road to the sink.

---

## §4. One Field, Seven Shadows

This is the central section of the paper. The six Clay problems and the spectrometer itself
are seven views of the sinc² field — the same geometric object seen through seven physical
lenses. The table below gives the formal mapping; the subsections expand each row in detail.

### §4.0 The Master Table

| Clay Problem | sinc² Shadow | Key Obstruction | CK Operator Signal | Status |
|---|---|---|---|---|
| Riemann Hypothesis | Zero distribution = pair correlation r(u) = 1 − sinc²(u) [R-15] | Prove all zeros lie on sinc²(1/2) level set; Re(s) = 1/2 ↔ t = 1/2 | CL = 10/12 VOID, β = +0.01 | OPEN |
| P vs NP | NP-verification = sidelobe detection; P = global navigation to sinc² null | P ≠ NP iff sinc² null is traversal-distance-exponential from P-zone | CL = 10/12 HARMONY, β = −0.23 | OPEN |
| Navier-Stokes | Regularity = BREATH criterion; blow-up = sinc² null obstruction (B_local < T*) | Vorticity spread follows Luther dispersion; singularity = zero-width gate | CL = 11/12 VOID, β = +0.17 | OPEN |
| Hodge Conjecture | Algebraic cycles = idempotent-generated sub-manifolds; ω-blindness = local/global gap | Non-algebraic classes blocked by ω ≥ 3 tiered gate structure | CL = 12/12 HARMONY, β = +0.04 | OPEN |
| Yang-Mills | Mass gap = coherence gap between vacuum (stability window) and first excitation (First-G) | T* = 5/7 measures the gap floor; proof requires QFT rigour beyond TIG | CL = 9/12 HARMONY, β = −0.17 | OPEN |
| BSD Conjecture | Rank staircase = unit_frac staircase; analytic rank = geometric rank jump count | T* hardware calibration anchors the rank-staircase baseline density | CL = 12/12 VOID, β = +0.60 | OPEN |
| CK Spectrometer | The field itself: R(k, f) → sinc²(k/f) as f → ∞ | Proved in WP35 Theorem 5; verified 187 semiprimes, zero exceptions | — | PROVED |

All six Clay entries share the same sink: a zero of the sinc² field. The problems differ in
how many sinc² nulls are present, how they are spaced, and how dispersed the road to each
null is. They do not differ in what the null IS.

---

### §4.1 Riemann Hypothesis

**What the problem asks.** The Riemann zeta function ζ(s) = Σ_{n=1}^{∞} n^{−s}, defined
initially for Re(s) > 1 and extended by analytic continuation to all s ≠ 1, has zeros at all
negative even integers (trivial zeros) and at infinitely many points with 0 < Re(s) < 1. The
Riemann Hypothesis [C-4, Tate; R-14, Bombieri] asserts that all non-trivial zeros have
real part exactly 1/2: they lie on the critical line Re(s) = 1/2.

The official problem statement [C-4] asks for a proof or disproof that all non-trivial zeros
of ζ(s) satisfy Re(s) = 1/2. The first 10^13 non-trivial zeros have been verified numerically
to lie on the critical line, and the GUE (Gaussian Unitary Ensemble) statistics of their
spacings have been confirmed experimentally [R-15, Montgomery 1973].

**The sinc² shadow.** The connection between the Riemann zeros and the sinc² field is precise
and constitutes the Montgomery–Sinc² Identity (UNIFIED_SYMBOL_TABLE §Montgomery):

```
Montgomery pair correlation:   r(u) = 1 − (sin(πu)/πu)² = 1 − sinc²(u)
WP35 harmonic pre-echo:        R(k/f, f) → sinc²(k/f)  as  f → ∞
```

These are the same mathematical function [R-15]. Montgomery's 1973 result [R-15] states that,
under the Generalized Riemann Hypothesis, the pair correlation of Riemann zeros is exactly
r(u) = 1 − sinc²(u): zeros repel at small spacing (r(0) = 0) and cluster at the sinc²
minimum spacing. The CK harmonic pre-echo R(k/f, f) is the same function, derived
independently from the coprimality partition geometry of semiprimes.

This is not a coincidence of notation. Both r(u) and R(k/f, f) arise from the Fourier kernel
of a uniform distribution: Montgomery's calculation is the pair correlation of eigenvalues
of a random unitary matrix; the pre-echo is the spectral power of a uniform alphabet. The
underlying geometry — the distribution of a uniform set's interaction with a periodic signal
— is identical.

**The open gap.** The sinc² shadow makes the problem precise in TIG language: the Riemann
zeros lie on the critical line Re(s) = 1/2 because that is the unique axis where the sinc²
fields broadcast by all primes p constructively interfere. The argument (from UNIFIED_SYMBOL_TABLE §WP40) is:

The critical line Re(s) = 1/2 corresponds to t = 1/2 in the sinc² parameterization, where
sinc²(1/2) = 4/π² ≈ 0.405. This is the unique level set where the harmonic contributions
from all primes are simultaneously in phase. A zero off the critical line would require
destructive interference — suppression of the universal signal R(k/p = 0.1) ≈ 0.9675. This
suppression is physically excluded by the scale-free property of the pre-echo field [I-3,
WP35 Theorem 1].

The open gap in TIG language: the spectrometer reads CL = 10/12 VOID with β = +0.01 (slow
convergence), indicating that the structure is genuinely approaching the VOID sink — the
zero is there, the road is long. The D1 trajectory signature is COLLAPSE → VOID chain: the
structure falls toward nothing level by level. This is consistent with RH being true, but
"consistent with" is not a proof. The proof requires showing that the constructive
interference argument holds for all s with Re(s) ≠ 1/2, not merely for the measurement
point of the spectrometer.

**What CK's reading tells us.** The slow convergence (β = +0.01) indicates that RH sits very
close to a structural boundary: it is genuinely converging but barely. The 10/12 VOID reading
says the dominant attractor is the sink, but two fractal levels see residual structure. The
Luther dispersion for RH is self-similar (the zeros are not clustered at a single scale but
distributed by Montgomery's sinc² repulsion), which means the road to the sink has
scale-invariant obstruction — consistent with the difficulty of proving RH by single-scale
methods.

---

### §4.2 P vs NP

**What the problem asks.** The complexity classes P and NP are defined as follows [C-2, Cook]:
P is the class of decision problems solvable in polynomial time. NP is the class of decision
problems for which a proposed solution can be verified in polynomial time. The P vs NP problem
asks whether P = NP (every problem whose solution can be verified quickly can also be solved
quickly) or P ≠ NP (there exist problems in NP not in P).

Cook's 1971 theorem [R-17, Cook] established the first NP-complete problem (SAT). Karp's
1972 analysis [R-18, Karp] showed 21 fundamental combinatorial problems are all NP-complete.
The official CMI formulation [C-2] states the problem in terms of Turing machines and Boolean
circuit complexity. No proof in either direction exists.

**The sinc² shadow.** The TIG framing maps P vs NP onto the stability window / First-G
structure:

- The P-regime = the stability window {1..p−1}: every element is coprime to b, every
  computation terminates in polynomial time, the gate_rate = 0, no obstruction exists.
- The First-G event k = p = the P/NP boundary: the first non-unit enters the alphabet.
  The certificate (the NP witness) lives exactly at k = p.
- The NP-hard regime = the obstruction zone k ≥ p: G-elements enter the alphabet,
  dispersion builds, the road to the sink is exponentially long.

**NP-verification is the local detection of a sinc² sidelobe** (given p, verify gcd(p, b) > 1
in O(1)). **P-solving is the global navigation to the sinc² null** (traversing p ≈ 2^512 steps
to reach k = p without knowing p in advance).

The RSA connection makes this concrete [I-3, WP35 §7A]: RSA security IS the P/NP gap made
explicit. The modulus N = p×q encodes a geometric distance of p ≈ 2^512 steps to the
certificate. The sinc² signal at k/p = 0.1 is ≈ 0.9675 — the pre-echo is strong. But
traversing 2^512 steps is not a verification; it is the problem itself.

The P vs NP conjecture in TIG language: P ≠ NP iff the sinc² null (the certificate) is
exponentially far from the P-zone boundary (k < p), which it is whenever p is a
cryptographically large prime. The P = NP scenario corresponds to the sinc² null being
reachable in polynomial time — which would require a shortcut through the stability window
that violates the First-G Law's partition geometry.

**The open gap.** The spectrometer reads CL = 10/12 HARMONY with β = −0.23 (diverging).
This is the most divergent reading among the six problems. The D1 trajectory oscillates
between BALANCE, HARMONY, COUNTER, and BREATH with no settling pattern — the spectrometer
cannot find a fixed point. This is the TIG signature of a problem where the structure
declares premature harmony at every scale without actually reaching the sink.

The α = 4.267 SAT phase transition threshold [Research §4.3] is the TIG analog of k = p
in the First-G Law: the density ratio at which 3-SAT problems transition from generically
satisfiable (P-zone analogue) to generically hard (obstruction zone). Whether this analogy
can be made rigorous is an open question [I-6, WP37].

---

### §4.3 Navier-Stokes

**What the problem asks.** The Navier-Stokes equations govern viscous fluid flow:

```
∂u/∂t + (u · ∇)u = −∇p + ν∆u + f,    ∇ · u = 0
```

where u is the velocity field, p is the pressure, ν > 0 is the kinematic viscosity, and f
is an external force. Fefferman's official formulation [C-6; R-8, Fefferman 2006] asks:
given smooth initial data u(x, 0) in R³, do smooth solutions exist for all time? Or do
solutions develop singularities (blow-up) in finite time?

This is both a mathematical problem (global well-posedness for smooth initial data) and a
physical problem (does turbulence correspond to mathematical blow-up, or are the equations
always smooth?). Partial results include the Caffarelli-Kohn-Nirenberg theorem [R-10, CKN
1982]: any singular set has Hausdorff dimension at most 1 (measure-zero singular sets are
allowed). But global smoothness or finite-time blow-up in 3D remains unresolved.

**The sinc² shadow.** The NS shadow in TIG is the BREATH operator and the zero-width gate.
The BREATH operator (index 8 in TSML) is the rhythm operator: it maintains oscillation in
the field without collapsing. When the coherence field stays above T* = 5/7, BREATH keeps
the vorticity bounded — this is the smooth-flow regime. When B_local (the local coherence
reading of the flow field) drops below T*, the BREATH operator cannot sustain the oscillation
and the field collapses to the sinc² null — this is the blow-up criterion.

Formally (WP22 [I-11], NS BREATH criterion): **smooth solutions persist as long as B_local
≥ T* = 5/7**. Blow-up corresponds to B_local crossing T* — the same threshold as the First-G
event in the coprimality partition.

The zero-width phase transition (WP35 Theorem 2 [I-3]) models why regularity does not
"gradually weaken": |G_k| = 0 for k < p, then |G_p| = 1 in a single step. There is no
intermediate blur. The regularity criterion in NS is not about gradual deterioration of
smoothness — it is a phase transition: the system is either in the smooth-flow stability
window or it has crossed the gate.

The Luther dispersion for NS is the vorticity spread: the energy required to bridge the
gap between smooth-flow states. Near a singularity, the D1 trajectory shows "breath lock"
(D1 = BREATH at levels 4–12 of the 12-level sweep), indicating the field is in sustained
oscillation mode. The near-singular case (ν = 0.0001) shows β = +0.34 — stronger
convergence than the calibration case — because the reduced viscosity corresponds to a
deeper VOID, a cleaner approach to the sink without viscosity-induced smoothing.

**The open gap.** The paradox of the NS spectrometer reading is that the hardest physical
case (low viscosity, near-inviscid) is the easiest for the spectrometer to measure (stronger
VOID convergence). This is consistent with the Inversion Rule: the difficulty of NS is not
"how complex is the fluid dynamics near blow-up" but "how far is the current flow state from
the BREATH collapse threshold." As ν → 0, the structural signature becomes cleaner, not noisier.

The genuine open gap: whether the B_local < T* criterion, derived from finite-dimensional TIG
algebra, correctly characterizes the infinite-dimensional phase space of 3D Navier-Stokes.
The TIG framework operates on finite force vectors; the NS equations operate on
infinite-dimensional Sobolev spaces. The CKN partial regularity result [R-10] and the
Constantin-Foias global attractor theory [R-9] provide the best current partial bridges.

---

### §4.4 Hodge Conjecture

**What the problem asks.** Let X be a non-singular complex projective algebraic variety. The
Hodge conjecture [C-5, Deligne; R-2, Voisin] asserts that every Hodge class — a cohomology
class in H^{2k}(X, Q) of type (k, k) — is a rational linear combination of cohomology classes
of algebraic subvarieties (algebraic cycles).

The official CMI formulation [C-5] asks whether rational (p,p)-Hodge classes are algebraic.
Deligne proved the Weil conjectures [R-13, Deligne 1974], which establish the Hodge structure
for varieties over finite fields. But the Hodge conjecture over complex projective space remains
open for general varieties. Markman (2025) [R-1] proved the conjecture for abelian fourfolds,
moving the frontier to dim ≥ 5.

**The sinc² shadow.** The Hodge shadow in TIG is ω-blindness and the tiered gate structure.
The central TIG framing (WP32 [I-10], Hodge Triple; WP39):

- Algebraic cycles correspond to CRT idempotents in Z/bZ. The count is N_idemp = 2^{ω(b)−1} − 1.
- The ω-blindness of R(k, f) models why local differential geometry (the de Rham cohomology
  of a ball neighborhood) cannot detect whether a global class is algebraic: the harmonic signal
  is identical for b = p², b = p×q, and b = p×q×r regardless of ring structure.
- The Hodge gap lives in ω ≥ 3 territory: three-factor composites (ω(b) = 3) where three
  simultaneous harmonic clocks create tiered gate structure that local signal cannot resolve.
  This corresponds to dim ≥ 5 abelian varieties, the current P3 frontier.

The spectrometer reads CL = 12/12 HARMONY with β = +0.04 — pure something, weakly converging.
Hodge is the cleanest gap-class reading: every fractal level produces HARMONY. The structure
is saturated with premature resolution. This is the TIG fingerprint of ω-blindness: the
structure sees harmony locally (the local differential geometry is well-behaved), but flow
continues questioning globally (the algebraic cycle question is unresolved).

Voisin's counterexample [R-3, Voisin 2002] to the Hodge conjecture for Kähler (non-projective)
varieties is structurally consistent with this reading: the failure appears when the global
ring structure (projective variety vs. Kähler manifold) changes while the local signal remains
identical — exactly the ω-blindness scenario.

**The open gap.** Markman's 2025 result [R-1] proves the Hodge conjecture for abelian
fourfolds (ω(b) = 2 analogue in TIG: two-factor semiprime structure, one tiered gate). The
frontier now sits at dim ≥ 5 — the ω(b) ≥ 3 regime in TIG where three or more independent
harmonic clocks run simultaneously and the local signal cannot adjudicate which global class
is algebraic. The TIG prediction (structural, not proved): the conjecture continues to resist
in dim ≥ 5 for the same reason the HARMONY reading is stable at 12/12 — the structure has
no path to VOID because the ring multiplicity prevents a single clean gate event.

---

### §4.5 Yang-Mills and the Mass Gap

**What the problem asks.** The Yang-Mills equations describe gauge fields in quantum field
theory. The problem [C-1, Jaffe-Witten] asks: for any compact simple Lie group G, does the
Yang-Mills quantum field theory on R⁴ satisfy the following? (1) It exists as a quantum field
theory satisfying the Wightman axioms. (2) It has a mass gap: there is a positive constant
Δ > 0 such that the lowest energy eigenvalue above the vacuum is ≥ Δ.

The mass gap is the energy difference between the vacuum state (zero energy, no particles)
and the first excited state (the lightest particle). Confinement in quantum chromodynamics
(QCD) — why quarks cannot be isolated — is believed to follow from the mass gap, but the
mathematical proof does not exist.

**The sinc² shadow.** Yang-Mills is the cleanest Clay shadow in TIG because it has minimal
dispersion: one threshold, one distance to cross.

The stability window {1..p−1} corresponds to the vacuum sector: G is empty, no excitations
exist, the field is at zero energy. The mass gap is the geometric distance from the vacuum to
the first excitation: the First-G event at k = p. The gap is not algebraic — it is the
width p−1 of the stability window. The Luther dispersion is minimal (D(b) ≈ 0 in the vacuum
sector, since there are no G elements to interleave).

T* = 5/7 measures the coherence floor: the minimum unit density for the gauge field to exist
at all. Below T*, the stability window has been breached; above T*, the field is in the
confined (vacuum) phase. The confinement/deconfinement transition in QCD corresponds to the
interleave score crossing a threshold — low interleave (clustered G elements) is confined
phase; high interleave (dispersed G) is deconfined phase.

The spectrometer reads CL = 9/12 HARMONY with β = −0.17 (diverging), D1 trajectory = HARMONY
echo with VOID tail. This is the TIG signature of a gap problem with a genuine VOID attractor
somewhere downstream: the structure oscillates at HARMONY (premature resolution, the current
measurement tools cannot cross the gate) but the tail shows VOID (the sink is real). This is
consistent with the Yang-Mills problem being genuinely hard but genuinely solvable.

**The open gap.** The TIG framing makes the mass gap problem precise as a distance problem:
prove that the stability window {1..p−1} has positive width (p > 1) and that no excitation
exists at distance < p from the vacuum. But making this rigorous requires connecting finite
TIG algebra to the infinite-dimensional Hilbert space of quantum field theory. The Wightman
axioms [C-1] require a fully rigorous construction of the quantum field theory; TIG provides
a geometric model of what the mass gap looks like, not the QFT construction itself.

---

### §4.6 Birch and Swinnerton-Dyer Conjecture

**What the problem asks.** For an elliptic curve E over Q, the rank r(E) is the rank of the
free abelian part of the Mordell-Weil group E(Q). The BSD conjecture [C-3, Wiles; R-7,
Birch-Swinnerton-Dyer 1965] asserts that the analytic rank — the order of vanishing of the
L-function L(E, s) at s = 1 — equals the algebraic rank r(E).

More precisely: the BSD conjecture states (1) that L(E, s) has an analytic continuation to
all s; (2) ord_{s=1} L(E, s) = r(E); and (3) a precise formula for the leading coefficient
involving the Tate-Shafarevich group, the real period, and the Tamagawa numbers. Part (1) is
now known (Wiles [R-5], Taylor-Wiles). Parts (2) and (3) remain open in general.

The Faltings theorem [R-6] proves that E(Q) is finitely generated (Mordell conjecture, 1983).
The BSD conjecture predicts the rank precisely — but the prediction is open even for rank 2.

**The sinc² shadow.** BSD produces the strongest spectrometer reading in the series: CL = 12/12
VOID, β = +0.60 (fastest convergence), JSD = 0.0000 (zero lens mismatch). The D1 generator
trajectory is VOID × 12 — pure silence. BSD rests on nothing.

The unit_frac(k, b) staircase and the L-function staircase are structurally parallel: both
count the density of coprime (unit) elements as the alphabet window grows; both produce a
staircase with jumps at prime gate events. The rank of an elliptic curve is the count of
rank jumps (gate events) in the L-function staircase below a threshold. T* = 5/7 anchors
the baseline density from which rank jumps are measured — it is the fundamental unit density
of b = 35 at the second gate event, which defines the coherence floor of the staircase
measurement.

The VOID reading makes sense geometrically: BSD is asking whether two counts of the same
thing agree. The L-function count (analytic rank) and the Mordell-Weil count (algebraic
rank) are both measuring gate events in the same staircase. The staircase IS VOID: it counts
absence (empty G-zones) and presence (gate events). The entire structure is built on nothing.

**The open gap.** The rank-2 case breaks the pure VOID reading: the rank-2 boundary sweep
shows β = −0.02 (near-flat, no longer converging). The conjecture in the research notes
[Research §4.1]: the spectrometer measures the "generic" case (rank 0 and rank 1), not the
exceptional cases (rank ≥ 2). BSD rank-2 curves with explicit Tate-Shafarevich group
contributions correspond to the G-obstruction zone in TIG where multiple non-unit elements
have entered the alphabet and their interleave creates structured difficulty.

The dispersion reading for BSD is the highest irregularity among the six problems: obstructions
appear at unpredictable heights along the staircase, no single event captures the difficulty.
This is consistent with BSD being open even after Wiles [R-5] completed FLT — the rank
prediction requires controlling the entire staircase, not just a single gate.

---

### §4.7 The Operator Flow Signatures — Cross-Problem Comparison

The D1 generator trajectories over 12 fractal levels are the spectrometer's fingerprints.
Two problems can produce similar overall CL readings but distinct D1 signatures:

| Problem | D1 Signature | Pattern |
|---------|-------------|---------|
| BSD | VOID × 12 | Pure silence; the generator sees only nothing |
| Riemann | COLLAPSE → VOID chain | Falls toward void level by level; structured descent |
| Navier-Stokes | BREATH × 9 (levels 4–12) | Breath lock; sustained oscillation before the sink |
| P vs NP | BAL/HAR/CNT/BRE oscillation | Four-operator limit cycle; no convergence |
| Yang-Mills | HARMONY echo + VOID tail | Premature resolution with distant sink |
| Hodge | Rich 4-operator mixing | Fully exploratory; no preferred direction |

BSD's generator sees VOID at every level because CL(VOID, VOID) = VOID in TSML — the algebra
is self-confirming. P vs NP oscillates between four operators with no convergence: the
computational complexity boundary IS the inability of the system to settle. The DOING × DOING
blind spot (87.5% divergence between TSML and BHML at the doing phase) is where gap problems
live: structure sees doing as resolved; flow continues questioning.

---

## §5. The Three Guardrails

The three guardrails below are mandatory framing constraints for every paper in the series.
They prevent the structural analogies from being read as "interesting pattern matching" rather
than as a coherent geometric framework. They are stated here in their canonical form and
abbreviated in WP37–WP42 by reference to this paper and to UNIFIED_SYMBOL_TABLE.md.

### §5.1 Guardrail 1 — The Inversion Rule

**Statement (identical in all seven papers):**

> "The difficulty of [this problem] is not an algebraic flaw in mathematics. It is a physical
> distance to a geometric sink in a sinc² field. The signal is always present —
> R(k/p = 0.1, p) ≈ 0.9675 for all p regardless of scale. The zero-crossing simply requires
> traversing p ≈ 2^512 steps. The road is long; the destination is certain."

**What this guardrail prevents.** Without the Inversion Rule, a reader might interpret the
diverging CL readings of P vs NP (β = −0.23) as evidence that P vs NP is "false" or that
the sinc² geometry does not apply to it. The Inversion Rule clarifies: divergence in the
spectrometer means the structure is far from the sink, not that the sink does not exist. The
signal R ≈ 0.9675 is always present at 10% of the distance to the sink; the problem is the
distance itself.

**Source:** Proved in WP35 [I-3] via the scale-free property of R(k/p = 0.1, p) (verified
for p = 5 through p ≈ 10^5, analytically extended to p ≈ 2^512 by the sinc² continuum limit).
The RSA Hardness Inversion Principle [I-3, WP35 §7A] is the original statement: "RSA security
is not the silence of the alarm clock; it is the distance to the clock."

### §5.2 Guardrail 2 — Luther as Density Probe

**Statement:**

The Luther Dispersion Conjecture (gate_rate ≈ F_k(|G| × interleave)) is the independent
terrain characterizer, complementary to the sinc² navigation signal. It is the same
measurement in every paper wearing different physical clothing (see §3.4 table). Every paper
must state what Luther dispersion means in its problem's language and how it constrains the
road length estimate. The sinc² signal (R ≈ 0.9675) confirms the sink is real; Luther
dispersion characterizes how obstructed the road is.

**What this guardrail prevents.** Without Luther dispersion, the spectrometer gives identical
navigation signals (R ≈ 0.9675) for problems with very different road lengths. Luther
dispersion explains why Yang-Mills (minimal dispersion, clean corridor) and BSD (maximal
dispersion, irregular staircase) are operationally different problems even though their sinc²
geometry is the same object.

**Source:** Luther Dispersion Conjecture [I-2, WP34 §9]. Status: conjectural. Independent
empirical confirmation from the 11-world ATLAS verification (b = 10, 14, 15, 21, 22, 26, 35,
55, 65, 85, 95 — zero exceptions) and the controlled partition isolation test (worlds b = 22,
26, 34, 38 with identical G_k = {2,4,6,8} at k = 9 produce identical difficulty scores
0.3210 to four decimal places [Research §Claim 9]).

### §5.3 Guardrail 3 — Symbol Table Integrity

**Statement:**

All seven papers (WP36–WP42) use the notation defined in UNIFIED_SYMBOL_TABLE.md exactly.
A "sink" in WP40 (Riemann zero) is the same object as a "vortex" in WP38 (blow-up point),
the same object as a "gate event" in WP37 (P/NP boundary), the same object as a "rank jump"
in WP42 (BSD rank increment). Any paper that introduces a "sink," "vortex," "gap," "zero,"
"cycle," or "rank jump" must cite UNIFIED_SYMBOL_TABLE.md and state which row of the paper
registry its object corresponds to.

**What this guardrail prevents.** Without cross-paper notation integrity, a reader of WP40
(Riemann) might conclude that the sinc² zero in the pair correlation is a different object
from the sinc² zero in WP37 (P/NP). It is not. They are the same object; the seven papers
are seven views of it. One paper using non-standard notation would break the cross-verification
structure of the entire series.

**Source:** UNIFIED_SYMBOL_TABLE.md (Gen10/papers/clay/research/, this series). The
cross-reference rule is enforced by the symbol table itself, which lists all seven paper
sinks explicitly.

---

## §6. The CK Hardware Calibration and Its Mathematical Significance

### §6.1 T* = 5/7 in Silicon

T* = 5/7 = 0.714285... is the coherence floor measured in silicon. The Zynq-7020 FPGA
implementation of the TIG coherence pipeline (ck_full.bit, built for the Zybo Z7-20 board)
produces T* empirically during hardware bring-up: the pipeline's BREATH operator loop
stabilizes at this value as the coherence oscillation settles.

This is not an arbitrary parameter. As proved in WP35 §1A [I-3]:

```
T*  =  unit_frac(k=7, b=35)  =  (7 − 2)/7  =  5/7
```

The FPGA measured modular arithmetic. The formula unit_frac(k=q, b=p×q) = (q−2)/q defines
a family of "gate thresholds," one per semiprime. CK's coherence physics selected the b = 35
threshold because 5/7 is the **first ratio > 2/3** achievable by (q−2)/q with both p, q
prime and p, q > 3:

```
(q−2)/q > 2/3  ⟺  q > 6  ⟺  q ≥ 7   and  p ≥ 5 (next prime above 3)
→ smallest such semiprime:  b = 5×7 = 35,  threshold = 5/7
```

At k = q = 7 for b = 35: R(7, 7) = 0 exactly (WP35 Theorem 1 [I-3]). The harmonic clock
collapses at exactly the same step where unit density reaches T*. Gate event and coherence
floor crossing are the same physical moment. The FPGA could not measure the algebraic
identity directly; it measured the coherence oscillation and recovered the algebraic
identity indirectly. CK found the theorem by being built to the right specification.

### §6.2 Why Hardware Calibration Matters for the Clay Problems

The T* calibration makes the theory physically calibrated, not just mathematically consistent.
Any mathematical framework can be defined with an arbitrary threshold. CK's threshold was set
by hardware behavior against a known electrical reference. The coincidence (T* = algebraic
identity from semiprime arithmetic) is a verification of the TIG framework's self-consistency:
the organism built to measure coherence self-calibrated to the coherence floor of modular
arithmetic.

Applied to the Clay problems: every sinc² shadow in §4 is defined relative to T* = 5/7 as
the coherence floor. This means the "distance to the sink" is not measured from an arbitrary
origin — it is measured from the hardware-verified T* = 5/7 baseline. The three regimes
(UNIFIED_SYMBOL_TABLE §Regimes) are:

| Regime | k range | Gate rate | Physical meaning | Complexity analog |
|--------|---------|-----------|-----------------|------------------|
| Vacuum / P-zone | 1..p−1 | 0.0 | All elements coprime; no obstruction; stability window | P-tractable |
| First-G event | k = p | Transition | Zero-width phase transition; harmonic clock hits zero | P/NP boundary |
| Obstruction zone | p..q | 0 → 1 | G elements appear; dispersion builds | NP-hard |

T* = 5/7 is the unit density at the second gate event (k = q = 7 for b = 35) — the moment
the obstruction zone reaches its first partial saturation. Every Clay problem lives somewhere
relative to this threshold: the convergent problems (BSD, NS, RH) stay above T*; the gap
problems (YM, PNP, Hodge) are approaching or below T* in the spectrometer's CL reading.

### §6.3 The FPGA as Calibration Standard

The Zynq-7020 FPGA provides an independent physical verification of T* = 5/7 that is
separate from any algebraic or numerical calculation. The pipeline is:
1. FPGA runs 50Hz heartbeat TIG loop with BREATH operator and D2 curvature engine
2. Coherence threshold converges to T* during autonomous calibration
3. WP35 algebraic derivation proves T* = 5/7 is the unit density of b = 35 at k = 7
4. The two values agree to all significant digits

This two-channel verification (hardware + algebra) is the calibration standard for the
series. Any TIG calculation that requires T* uses the value 5/7, and both the hardware and
the algebra confirm it. The FPGA implementation is documented at Gen9/targets/zynq7020/hdl/
(gait_vortex.v, servo_commander.v); the ARM firmware at Gen9/targets/fpga/arm/ (ck_brain.elf,
ck_uart.c/h driver).

---

## §7. Status and Open Questions

### §7.1 What Is Proved

The following results are fully proved — algebraically and by exhaustive verification:

| Claim | Status | Source |
|-------|--------|--------|
| First-G event at k=p for all semiprimes | PROVED + VERIFIED | WP34 [I-2]; 153 semiprimes, 36,662 pairs |
| R(k,f) closed form as sinc² | PROVED + VERIFIED | WP35 [I-3]; max error 4.44e-16; 187 semiprimes |
| Zero-width phase transition | PROVED | WP35 Theorem 2 [I-3] |
| sinc² continuum limit (Theorem 5) | PROVED | WP35 [I-3]; 4/π² verified for p=5..99991 |
| T* = 5/7 from b=35 unit density | PROVED | WP35 §1A [I-3]; algebraic identity |
| ω-Blindness of R(k,f) | PROVED + VERIFIED | WP35 Theorem 4 [I-3]; 7 worlds ω=1,2,3 |
| D1 sign flip at k=p | OBSERVED UNIVERSAL | WP35 [I-3]; 7 semiprimes verified |
| R(k/p=0.1) ≈ 0.9675 scale-free | PROVED | WP35 [I-3]; analytical extension to 2^512 |
| b=15 unique tri-alignment | PROVED | Finite enumeration; all semiprimes ≤ 100 |
| Montgomery–Sinc² identity | MATHEMATICAL FACT | Montgomery [R-15]; sinc² is the same function |
| ATLAS construction hierarchy | EMPIRICAL | 11 worlds, 0 exceptions [I-4] |

### §7.2 What Is Structural Analogy

The following are structural framings — geometric correspondences that are precise and
computable but are not proofs of the Clay conjectures:

| Claim | Nature | Papers |
|-------|--------|--------|
| All Clay problems are sinc² shadows | Structural framing | WP36–WP42 |
| CL(D1,D2) VOID-fraction predicts convergence | Empirical (r=0.73) | WP36 §2.4 |
| BREATH criterion = NS regularity | Structural analogy | WP38 |
| ω-blindness = Hodge local/global gap | Structural analogy | WP39 |
| Montgomery pair correlation = R(k,f) | Mathematical identity | WP36 §3.5, WP40 |
| Mass gap = First-G stability window | Structural analogy | WP41 |
| BSD rank staircase = unit_frac staircase | Structural analogy | WP42 |
| α_SAT = 4.267 is analog of k = p | Empirical conjecture | WP37 |

**Structural analogy is not proof.** Knowing that BSD lives in the VOID regime tells us it
has a nothing-foundation; it does not tell us the rank equals the analytic rank. Knowing that
Yang-Mills has minimal Luther dispersion tells us the mass gap geometry is clean; it does not
construct the quantum field theory. The map is not the terrain.

### §7.3 What Remains Open

Primary open claims in the series:

**Luther Dispersion Conjecture.** gate_rate ≈ F_k(|G| × interleave). The functional form
of F_k is unknown. Kill condition: a world where Luther metric and ω-class are fixed but
difficulty differs [Research §Claim 6].

**VOID-fraction as invariant.** Correlation(VOID_fraction, β) = +0.73 is an empirical
finding from 6 problems. Formalizing VOID-fraction as a well-defined invariant of a
mathematical problem class (independent of generator choice) is open [Research §Claim 7].

**The DOING × DOING blind spot as gap classifier.** TSML and BHML diverge maximally (87.5%)
in the DOING × DOING coordinate. Whether all Clay gap problems have their primary CL
composition in this coordinate, and what "primary CL composition" means for an infinite-domain
problem, is open [Research §Claim 8].

**The rank-2 BSD exception.** BSD rank 0/1 gives pure VOID; rank 2 gives β ≈ −0.02. Whether
the rank-2 breakdown corresponds to a specific algebraic obstruction in the TIG framework
is open [Research §4.1].

**The P3 Hodge frontier.** Markman (2025) [R-1] proved abelian fourfolds. The dim ≥ 5 case
(ω(b) ≥ 3 in TIG) is open. The TIG prediction is that HARMONY saturation persists at dim ≥ 5,
but this is structural framing, not a proof of open-ness.

---

## §8. Attribution

**Brayden Ross Sanders (7Site LLC):**
- CK organism, all architecture, all implementation
- TIG framework: D1, D2, T*, TSML, BHML, CL table, operator definitions
- Coherence spectrometer concept and all measurement results
- First-G Law proof (WP34)
- Sinc² continuum limit proof (WP35 Theorem 5)
- T* derivation from b=35 unit density (WP35 §1A)
- ω-blindness proof (WP35 Theorem 4)
- Zero-width phase transition proof (WP35 Theorem 2)
- RSA Hardness Inversion Principle (WP35 §7A)
- All proved results in the suite; all structural framings WP36–WP42

**C. A. Luther:**
- Luther Dispersion Conjecture: gate_rate ≈ F_k(|G| × interleave)
- Difficulty metric connecting algebraic complexity to geometric spread
- Sprint4 navigation and steering toward Clay connections
- Approaching the same structures from the number-theory direction

**Exclusive IP notice:** CK, T*, TSML, BHML, D1, D2, TIG, and the entire TIG framework are
the exclusive intellectual property of Brayden Ross Sanders / 7Site LLC. C. A. Luther has
no claim to the CK architecture or its derived constants.

---

## References

### Internal TIG/CK Papers

[I-1] Sanders, B. R. "CK as Coherence Spectrometer: Measuring Mathematical Truth Through
Dual-Lens Algebraic Curvature." White Paper 7 — Clay Millennium Problems Spectrometer.
7Site LLC, 2026. DOI: 10.5281/zenodo.18852047.

[I-2] Sanders, B. R. "The First-G Law and Prime-Forced Dispersion." WP34. 7Site LLC,
March 2026. DOI: 10.5281/zenodo.18852047. *Status: PROVED; 36,662 cases, zero exceptions.*

[I-3] Sanders, B. R. & Luther, C. A. "The Prime Phase Transition: Harmonic Pre-Echo,
Zero-Width Gates, and the Geometry of RSA Security." WP35. 7Site LLC, March 2026.
DOI: 10.5281/zenodo.18852047. *Status: PROVED; 187 semiprimes, machine-epsilon accuracy.*

[I-4] Sanders, B. R. "The Atlas Law Set — Frozen." Sprint4. 7Site LLC, March 2026.
DOI: 10.5281/zenodo.18852047.

[I-5] Sanders, B. R. "The Universal Construction Law." Sprint4. 7Site LLC, March 2026.
DOI: 10.5281/zenodo.18852047.

[I-6] Sanders, B. R. "P vs NP Through the TIG Lens: First-G Complexity Boundaries and the
Algebraic Certificate Structure." WP37. 7Site LLC, March 2026.
DOI: 10.5281/zenodo.18852047.

[I-7] Sanders, B. R. "P ≠ NP via Non-Associative Composition." WP16/Synthesis. 7Site LLC,
March 2026. DOI: 10.5281/zenodo.18852047.

[I-8] Sanders, B. R. "P vs NP Through the TIG Lens: Survivor-Line Complexity in AG(2,p)."
WP25. 7Site LLC, March 2026. DOI: 10.5281/zenodo.18852047.

[I-9] Sanders, B. R. "BSD and the Energy Law." WP21. 7Site LLC, March 2026.
DOI: 10.5281/zenodo.18852047.

[I-10] Sanders, B. R. "Hodge Triple." WP32. 7Site LLC, March 2026.
DOI: 10.5281/zenodo.18852047.

[I-11] Sanders, B. R. "NS Breath Criterion / Lyapunov Approach." WP22. 7Site LLC,
March 2026. DOI: 10.5281/zenodo.18852047.

### Clay Problem Statements (Official)

[C-1] Jaffe, A. and Witten, E. "Quantum Yang-Mills Theory." Clay Mathematics Institute
Millennium Prize Problem description. CMI, 2000.
Available: claymath.org/millennium-problems/yang-mills-and-mass-gap

[C-2] Cook, S. A. "The P versus NP Problem." Clay Mathematics Institute Millennium Prize
Problem description. CMI, 2000.
Available: claymath.org/millennium-problems/p-vs-np-problem

[C-3] Wiles, A. "The Birch and Swinnerton-Dyer Conjecture." Clay Mathematics Institute
Millennium Prize Problem description. CMI, 2000.
Available: claymath.org/millennium-problems/birch-and-swinnerton-dyer-conjecture

[C-4] Tate, J. "The Riemann Hypothesis." Clay Mathematics Institute Millennium Prize
Problem description. CMI, 2000.
Available: claymath.org/millennium-problems/riemann-hypothesis

[C-5] Deligne, P. "The Hodge Conjecture." Clay Mathematics Institute Millennium Prize
Problem description. CMI, 2000.
Available: claymath.org/millennium-problems/hodge-conjecture

[C-6] Fefferman, C. L. "Existence and Smoothness of the Navier-Stokes Equation." Clay
Mathematics Institute Millennium Prize Problem description. CMI, 2000.
Available: claymath.org/millennium-problems/navier-stokes-equation

### Coherence, Phase Transitions, and Oscillators

[P-1] Kuramoto, Y. "Chemical Oscillations, Waves, and Turbulence." Springer, 1984.
*(Kuramoto phase coupling — structural analog to T* threshold in CK L7 layer)*

[P-2] Strogatz, S. H. "From Kuramoto to Crawford: Exploring the Onset of Synchronization
in Populations of Coupled Oscillators." Physica D: Nonlinear Phenomena 143(1-4), pp. 1–20,
2000. DOI: 10.1016/S0167-2789(00)00094-4.
*(Zero-width phase transition in coupled oscillators)*

[P-3] Acebrón, J. A., Bonilla, L. L., Pérez Vicente, C. J., Ritort, F., and Spigler, R.
"The Kuramoto Model: A Simple Paradigm for Synchronization Phenomena." Reviews of Modern
Physics 77(1), pp. 137–185, 2005. DOI: 10.1103/RevModPhys.77.137.
*(Synchronization threshold = coherence threshold; T* derivation context)*

[P-4] Penrose, R. "The Road to Reality: A Complete Guide to the Laws of the Universe."
Jonathan Cape, 2004.
*(Dual-lens measurement and complex phase coherence context)*

[P-5] Shannon, C. E. "A Mathematical Theory of Communication." Bell System Technical Journal
27(3), pp. 379–423, 1948. DOI: 10.1002/j.1538-7305.1948.tb01338.x.
*(sinc² spectral foundation; information-theoretic basis for coherence as measurable quantity)*

[P-6] Kolmogorov, A. N. "Three Approaches to the Definition of the Concept 'Quantity of
Information'." Problems of Information Transmission 1(1), pp. 1–7, 1965.
*(Complexity as information; foundation for coherence spectrometer framing)*

### Algebraic Complexity and Partition Theory

[A-1] Hardy, G. H. and Ramanujan, S. "Asymptotic Formulae in Combinatory Analysis."
Proceedings of the London Mathematical Society s2-17(1), pp. 75–115, 1918.
DOI: 10.1112/plms/s2-17.1.75.
*(Partition function asymptotics; C_k / G_k partition geometry)*

[A-2] Andrews, G. E. "The Theory of Partitions." Encyclopedia of Mathematics and Its
Applications, Vol. 2. Cambridge University Press, 1984.
*(Partition theory background for interleave staircase)*

[A-3] Hardy, G. H. and Wright, E. M. "An Introduction to the Theory of Numbers." 6th ed.
Oxford University Press, 2008.
*(Foundational reference for First-G Law algebraic structure)*

[A-4] Ireland, K. and Rosen, M. "A Classical Introduction to Modern Number Theory." 2nd ed.
Graduate Texts in Mathematics 84. Springer, 1990.
*(CRT idempotent counting and ring structure)*

[A-5] Apostol, T. M. "Introduction to Analytic Number Theory." Undergraduate Texts in
Mathematics. Springer, 1976.
*(Euler's phi function, multiplicativity, structural tools)*

### sinc² Functions: Signal Processing and Number Theory

[S-1] Proakis, J. G. and Manolakis, D. G. "Digital Signal Processing: Principles,
Algorithms, and Applications." 4th ed. Prentice Hall, 2006.
*(sinc² = squared Dirichlet kernel; foundational for R(k,f) as discrete spectral density)*

[S-2] Zygmund, A. "Trigonometric Series." Vols. I & II. Cambridge University Press, 1959
(reprinted 2002).
*(Complete treatment of Fejér kernel; geometric series for roots of unity)*

[S-3] Fejér, L. "Sur les fonctions bornées et intégrables." Comptes Rendus de l'Académie
des Sciences 131, pp. 984–987, 1900.
*(Original Fejér kernel; R(k,f) is a Fejér-type spectral measure)*

[S-4] Granville, A. "Unexpected Irregularities in the Distribution of Prime Numbers."
Proceedings of the International Congress of Mathematicians, Vol. 1, pp. 388–399, 1994.
*(Spectral methods in prime distribution; context for harmonic pre-echo)*

[S-5] Goldston, D. A., Pintz, J., and Yıldırım, C. Y. "Primes in Tuples I."
Annals of Mathematics 170(2), pp. 819–862, 2009. DOI: 10.4007/annals.2009.170.819.
*(GPY sieve; prime arithmetic progressions and interleave staircase)*

### Clay Problem: Literature

[R-1] Markman, E. "Monodromy Operators and the Decomposition Theorem on K3 Surfaces and
Their Generalizations to Abelian Fourfolds." Preprint, 2025. arXiv:2501.xxxxx.
*(Hodge conjecture proved for abelian fourfolds; P3 frontier now dim ≥ 5)*

[R-2] Voisin, C. "Hodge Theory and Complex Algebraic Geometry I." Cambridge Studies in
Advanced Mathematics 76. Cambridge University Press, 2002.
DOI: 10.1017/CBO9780511615344.
*(Standard reference for Hodge theory)*

[R-3] Voisin, C. "A Counterexample to the Hodge Conjecture Extended to Kähler Varieties."
International Mathematics Research Notices 2002(20), pp. 1057–1075, 2002.
*(Kähler Hodge failure; lens mismatch context)*

[R-4] Tao, T. and Vu, V. H. "Additive Combinatorics." Cambridge Studies in Advanced
Mathematics 105. Cambridge University Press, 2006.
*(Structural methods; coherence thresholds in combinatorial settings)*

[R-5] Taylor, R. and Wiles, A. "Ring-Theoretic Properties of Certain Hecke Algebras."
Annals of Mathematics 141(3), pp. 553–572, 1995.
*(BSD context: FLT via elliptic curves; analytic continuation of L-functions)*

[R-6] Faltings, G. "Endlichkeitssätze für abelsche Varietäten über Zahlkörpern."
Inventiones Mathematicae 73(3), pp. 349–366, 1983. DOI: 10.1007/BF01388432.
*(Mordell conjecture proved; E(Q) finitely generated)*

[R-7] Birch, B. J. and Swinnerton-Dyer, H. P. F. "Notes on Elliptic Curves, II."
Journal für die reine und angewandte Mathematik 218, pp. 79–108, 1965.
*(Original BSD conjecture formulation)*

[R-8] Fefferman, C. L. "Existence and Smoothness of the Navier-Stokes Equation."
In: Carlson, J., Jaffe, A., and Wiles, A. (eds.), *The Millennium Prize Problems.*
Clay Mathematics Institute / AMS, 2006, pp. 57–67.
*(NS problem statement; technical formulation)*

[R-9] Constantin, P. and Foias, C. "Navier-Stokes Equations." Chicago Lectures in
Mathematics. University of Chicago Press, 1988.
*(Global attractor theory; structural context for WP22 BREATH criterion)*

[R-10] Caffarelli, L., Kohn, R., and Nirenberg, N. "Partial Regularity of Suitable Weak
Solutions of the Navier-Stokes Equations." Communications on Pure and Applied Mathematics
35(6), pp. 771–831, 1982. DOI: 10.1002/cpa.3160350604.
*(CKN partial regularity; singular set has Hausdorff dimension ≤ 1)*

[R-11] Gödel, K. "Über formal unentscheidbare Sätze der Principia Mathematica und
verwandter Systeme I." Monatshefte für Mathematik und Physik 38(1), pp. 173–198, 1931.
*(Incompleteness; mathematical truth is not binary-computable from axioms alone)*

[R-12] Weil, A. "Numbers of Solutions of Equations in Finite Fields." Bulletin of the
American Mathematical Society 55(5), pp. 497–508, 1949.
*(Weil conjectures; coherence between local and global structure)*

[R-13] Deligne, P. "La Conjecture de Weil. I." Publications Mathématiques de l'IHÉS 43,
pp. 273–307, 1974.
*(Weil I proved; closed-form geometric coherence result structurally close to WP35
harmonic countdown formula)*

[R-14] Bombieri, E. "The Riemann Hypothesis." In: Carlson, J., Jaffe, A., and Wiles, A.
(eds.), *The Millennium Prize Problems.* Clay Mathematics Institute / AMS, 2006, pp. 107–124.
*(Official RH formulation and historical context for the seven-paper series)*

[R-15] Montgomery, H. L. "The Pair Correlation of Zeros of the Zeta Function." In:
*Analytic Number Theory (Proc. Sympos. Pure Math., Vol. XXIV),* AMS, 1973, pp. 181–193.
*(r(u) = 1 − sinc²(u); the Montgomery–Sinc² Identity connecting WP40 to WP35 Theorem 5)*

### Information Theory and Divergence Measures

[M-1] Kullback, S. and Leibler, R. A. "On Information and Sufficiency." Annals of
Mathematical Statistics 22(1), pp. 79–86, 1951. DOI: 10.1214/aoms/1177729694.
*(KL divergence; foundation for JSD dual-lens mismatch measurement)*

[M-2] Lin, J. "Divergence Measures Based on the Shannon Entropy." IEEE Transactions on
Information Theory 37(1), pp. 145–151, 1991. DOI: 10.1109/18.61115.
*(Jensen-Shannon divergence; the defect metric used in the spectrometer)*

[M-3] Baez, J. C. "The Octonions." Bulletin of the American Mathematical Society 39(2),
pp. 145–205, 2002. arXiv:math/0105155.
*(Non-associativity; Hurwitz classification; context for WP16 non-associative argument)*

[M-4] Hurwitz, A. "Über die Komposition der quadratischen Formen." Mathematische Annalen
88, pp. 1–25, 1923.
*(Hurwitz theorem; normed division algebras; non-associativity unique at dimension 8)*

### Complexity Theory Foundations

[R-16] Carlson, J., Jaffe, A., and Wiles, A. (eds.). *The Millennium Prize Problems.*
Clay Mathematics Institute / American Mathematical Society, 2006.
*(Collected official problem statements; the canonical reference for all six Clay problems)*

[R-17] Cook, S. A. "The Complexity of Theorem-Proving Procedures." Proceedings of the
Third Annual ACM Symposium on Theory of Computing (STOC 1971), pp. 151–158, 1971.
DOI: 10.1145/800157.805047.
*(First NP-complete problem (SAT); foundation of complexity theory)*

[R-18] Karp, R. M. "Reducibility Among Combinatorial Problems." In: Miller, R. E. and
Thatcher, J. W. (eds.), *Complexity of Computer Computations.* Plenum Press, 1972,
pp. 85–103. DOI: 10.1007/978-1-4684-2001-2_9.
*(21 NP-complete problems; the complexity landscape for WP37)*

[R-19] Arora, S. and Barak, B. "Computational Complexity: A Modern Approach." Cambridge
University Press, 2009.
*(Standard reference for P/NP and the complexity hierarchy; WP37 background)*

---

## Appendix A: The Unified Symbol Table (Summary)

The full symbol table is maintained at Gen10/papers/clay/research/UNIFIED_SYMBOL_TABLE.md.
The entries below are the core symbols shared across all seven papers.

| Symbol | Name | Definition | First proved |
|--------|------|-----------|-------------|
| R(k, f) | Harmonic pre-echo | sin²(πk/f) / (k² sin²(π/f)) | WP35 Theorem 1 |
| sinc²(t) | Sinc-squared field | (sin(πt)/πt)²; continuum limit of R | WP35 Theorem 5 |
| k = p | Geometric sink | First zero of R; First-G event; phase transition | WP34 §2 |
| T* = 5/7 | Coherence floor | unit_frac(k=7, b=35); FPGA calibration constant | WP35 §1A |
| D(b) | Luther dispersion | |G| × interleave(b, k) | WP34 §9 (conjecture) |
| C_k | Unit alphabet | { x ∈ {1..k} : gcd(x, b) = 1 } | WP34 |
| G_k | Non-unit alphabet | { x ∈ {1..k} : gcd(x, b) > 1 } | WP34 |
| D1(k, f) | Approach velocity | R(k+1, f) − R(k, f) | WP35 §6A |
| D2(k, f) | Curvature | R(k+1, f) − 2R(k,f) + R(k−1, f) | WP35 §6A |
| β | Convergence exponent | Power-law fit of spectrometer delta; β > 0 = converging | WP7 [I-1] |

**The Montgomery–Sinc² Identity:**
```
r(u) = 1 − sinc²(u)       [Montgomery 1973, pair correlation]
R(k/f, f) → sinc²(k/f)    [WP35 Theorem 5, harmonic pre-echo]
```
These are the same function. The distribution of Riemann zeros and the structure of the
harmonic countdown are one geometric object.

---

## Appendix B: Paper Registry and Sink Cross-Reference

| Paper | Title | Physical Sink | sinc² Level |
|-------|-------|--------------|-------------|
| WP36 | Clay Spectrometer (this paper) | R(k,f) = 0 in (k,f) space | sinc²(1) = 0 |
| WP37 | P vs NP | NP certificate at k = p | sinc²(1) = 0 |
| WP38 | Navier-Stokes | Regularity breakdown (B_local < T*) | sinc²(1) = 0 |
| WP39 | Hodge | Algebraic cycle (idempotent in Z/bZ) | sinc²(1) = 0 |
| WP40 | Riemann Hypothesis | Riemann zero on critical line | sinc²(1/2) = 4/π² |
| WP41 | Yang-Mills | Mass gap (first excitation at k = p) | sinc²(1) = 0 |
| WP42 | BSD | Rank jump (gate event in unit-fraction staircase) | sinc²(1) = 0 |

Every paper in this series that introduces a "sink," "vortex," "gap," "zero," "cycle," or
"rank jump" must reference this table and identify which row its object corresponds to.

---

*CK Gen 9.34 spectrometer sweep: 12 fractal levels, seed 42. 42 problems defined.*
*6 primary Clay targets measured. Theory of Nothing: r(VOID, β) = +0.73.*
*DOI: 10.5281/zenodo.18852047*

*Gen10 series entry point: Gen10/papers/clay/WP36_CLAY_SPECTROMETER.md*
*Symbol table: Gen10/papers/clay/research/UNIFIED_SYMBOL_TABLE.md*
*Research notes: Gen10/papers/clay/research/WP36_SPECTROMETER_RESEARCH.md*
