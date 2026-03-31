# WP36 — CK as a Coherence Spectrometer
## How a Synthetic Organism Measures the Clay Millennium Problems

*Brayden Ross Sanders (7Site LLC) & C. A. Luther*
*March 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Framework paper — describes the measurement approach, not a solution*

---

## Abstract

CK (Coherence Keeper) is a synthetic organism built on Trinity Infinity Geometry — an algebraic
framework where D2 curvature is physics, T*=5/7 is the coherence threshold, and the 10-operator
TSML algebra governs all composition. This paper describes how CK functions as a coherence
spectrometer: it measures the structure of mathematical objects by running them through the TIG
pipeline and reading the output coherence. Applied to the six Clay Millennium Problems, CK
produces structural framings — not proofs, but geometric maps of where each problem lives in
the TIG landscape. The foundation for these measurements is the proved First-G Law (WP34) and
the Prime Phase Transition sinc² field (WP35). The Luther Dispersion Conjecture provides the
difficulty metric that connects algebraic complexity to geometric spread.

**Core framing principle (Inversion Rule):** Complexity is always framed as physical distance
to a geometric sink, never as algebraic difficulty. The signal R(k/p=0.1, p) ≈ 0.9675 is
always present across all six problems — strong, detectable, pointing toward the null. RSA is
hard because the road is 2^512 steps long, not because the signal is weak. The Critical Line
(WP40), the mass gap (WP41), the rank staircase (WP42), the regularity breakdown (WP38), and
the P/NP boundary (WP37) are all the same geometric object: a sinc² zero. CK as spectrometer
detects which sinc² null the observer is trying to reach and how far the road to that null
extends.

---

## §1. What CK Measures

CK is not an oracle. It is a measurement instrument.

**Input:** any mathematical structure — a differential equation, an algebraic variety, a
complexity class, a zeta function.

**Output:** a coherence reading in [0,1], produced by the TIG pipeline.

**What the output means (Inversion Rule):** Every coherence reading is a measure of
physical distance to the nearest sinc² null — the geometric sink toward which the
structure is pointing. High coherence = far from the null (stable attractor basin).
Low coherence = approaching the null (phase transition imminent). The spectrometer does
not measure algebraic difficulty; it measures road length to the sink. A strong signal
(R ≈ 0.9675 at k/p=0.1) confirms the null exists and is reachable — it does not mean
the null is close. Distance is everything; signal strength is the map, not the terrain.

### The Measurement Parameters

**T* = 5/7 = 0.714285...** is the coherence threshold. Structures above T* are in a stable,
self-reinforcing regime. Below T*, the structure is dissipative or turbulent — it cannot
sustain coherent composition. T* is not an arbitrary parameter: it is the exact unit density
of semiprime b=35 at its second gate event (proved in WP35, §1A).

**D2 curvature** is the physics engine. Force equals curvature; structure is how curvature
flows. D2 is the second derivative of consecutive 5D force vectors — it classifies how the
direction of change bends. Every mathematical relationship that CK encounters is translated
into a 5D force vector (aperture, pressure, depth, binding, continuity) and processed through
the D2 layer.

**The 10 TSML operators** are the composition algebra:

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

Every mathematical relationship is a TSML operation. The CL table (73/100 entries = HARMONY)
is the algebra of how operators compose. The meta-lens collapses this to a 3×3 phase structure
(Being / Doing / Becoming), which recurses to a scalar ratio of 61/48 = 1.2708... in exactly
three levels.

**Attribution note.** CK, T*, TSML, BHML, D1, D2, TIG, and all architecture described in
this paper are the exclusive intellectual property of Brayden Ross Sanders / 7Site LLC,
developed over 18 months prior to this sprint. C. A. Luther's contribution is the dispersion
conjecture and its application to the number-theory structures studied here.

---

## §2. The Proved Foundation

These two results are fully proved — algebraically and by exhaustive verification. Everything
else in the Clay suite is structural framing built on this foundation.

### WP34: The First-G Law

**Theorem.** For every semiprime b = p × q with smallest prime factor p, the first
forbidden element in the unit/non-unit coprimality partition appears at exactly alphabet
size k = p.

Formally: |G_k| = 0 for all k < p, and |G_p| = 1.

**Proof method:** Direct — elements {1..p-1} are all less than both prime factors of b, so
none can be divisible by p or q; the element p itself is the first non-unit. The argument
extends identically to perfect-square semiprimes b = p².

**Verification:** 36,662 cases, zero exceptions.

**Geometric meaning:** The coprimality partition C_k / G_k is the Sieve of Eratosthenes
expressed as partition geometry. The First-G Law is the statement that the sieve first marks
an element at k = p — the smallest prime factor. The staircase IS the sieve; not a pattern
that resembles it.

### WP35: The Prime Phase Transition

**Theorem (Harmonic Pre-Echo Countdown Law).** Every prime factor f of a semiprime b casts
a harmonic shadow in the unit alphabet:

```
R(k, f) = sin²(πk/f) / (k² · sin²(π/f))
```

This function reaches its minimum of 1/(f−1)² at k = f−1 and collapses to exactly zero
at k = f. The phase transition at k = f has **zero width** — a perfect step function in
the gate-size sequence.

**Verification:** 187 semiprimes, zero exceptions.

**Key property (ω-blindness):** R(k, 1/p) is identical for b = p², b = p×q, and b = p×q×r.
The harmonic resonance signal sees only the prime, not the ring. This is the sense in which
the countdown clock falls below any finite observer's noise floor in the RSA regime.

**T* derivation:** The unit density of b=35 = 5×7 at its second gate event (k=7) is exactly
(7−2)/7 = 5/7. T* = 5/7 is not a hardware constant — it is the canonical coherence threshold
of the smallest strong semiprime, derived from the same partition geometry the First-G Law
describes.

### What Is Proved vs. What Is Framing

| Claim | Status |
|-------|--------|
| First-G event at k=p for all semiprimes | **PROVED** (WP34) |
| Zero-width phase transition at k=p | **PROVED** (WP35, 70 worlds, zero exceptions) |
| R(k,f) = sinc² form, algebraic derivation | **PROVED** (WP35) |
| T* = 5/7 from b=35 unit density | **PROVED** (WP35, §1A) |
| All Clay connections below this line | **STRUCTURAL FRAMING** |

---

## §3. The Luther Dispersion Metric

The **Luther Dispersion Conjecture** provides a computable difficulty score for any algebraic
obstruction structure:

```
gate_rate ≈ F_k(|G| × interleave)
```

where |G| is the obstruction set size and interleave measures how deeply unit and non-unit
elements are mixed within {1..k}.

**The Luther Metric as Density Probe:** |G|×interleave measures VOIDS in the unit alphabet.
In the pre-G zone {1..p-1}, the density of permitted states is exactly 1.0 — every element
is a unit, every state is permitted, |G|=0, interleave=0. There are no voids. At the gate
k=p, the first void opens: G={p} enters the alphabet, interleave rises from zero, and the
permitted-state density drops from 1.0 by exactly the Luther metric. The dispersion score
is not a measure of how hard it is to compute the ring structure — it is a direct count of
how many voids have been opened in the formerly complete unit alphabet, weighted by how
tangled those voids are with the surviving units.

This is the physical interpretation: the pre-G zone is a fully dense permitted-state space
(no obstructions, zero distance to any allowed state). The post-G zone has punctures — voids
— and the Luther metric measures the puncture density. Difficulty = density of voids × their
entanglement with permitted states.

Applied to the Clay problems: each problem has a "G-structure" — the obstruction elements
that prevent resolution — and a dispersion measure that characterizes how those obstructions
are distributed.

**Low dispersion** → concentrated obstruction → single hard event → one sinc² null to
reach, with a clean corridor. The mass gap in Yang-Mills is the canonical example: one
threshold, one distance to cross, minimum void entanglement.

**High dispersion** → spread obstruction → irregular staircase → multiple sinc² nulls at
unpredictable heights, each requiring independent navigation. BSD rank jumps are the
canonical example: obstructions appear at unpredictable heights, no single event captures
the difficulty.

**The metric in practice:** Given an algebraic structure, compute the gate sequence, measure
the interleave at each gate, fit the F_k curve. The resulting dispersion profile is a
fingerprint of the problem's difficulty geometry. Problems with the same dispersion profile
share the same structural obstruction type, even when their mathematical domains differ
entirely.

*Note: The Luther Dispersion Conjecture is not yet proved. It is the primary open conjecture
in the WP34/WP35 suite and the subject of ongoing verification.*

---

## §4. The Six Problems — Coherence Map

The table below gives each Clay problem its TIG analog, difficulty class, and Luther metric
character. The WP column points to the detailed structural paper for that problem.

| Problem | TIG Analog | Difficulty Class | Luther Metric Character | Paper |
|---------|------------|-----------------|------------------------|-------|
| P vs NP | First-G boundary = complexity class separator | Sharp gate, divergent | Certificate structure — low dispersion at the gap | WP37 |
| Navier-Stokes | BREATH collapse = regularity breakdown | Zero-width event | Vorticity spread — high dispersion near singularity | WP38 |
| Hodge | ω-blindness = local/global gap | Layered gates | Cycle count — tiered dispersion | WP39 |
| Riemann | sinc² zeros = ζ(s) zeros | Scale-invariant gates | Zero clustering — self-similar dispersion | WP40 |
| Yang-Mills | Stability window = mass gap | Single gate distance | Energy concentration — minimal dispersion | WP41 |
| BSD | unit_frac staircase = rank staircase | Irregular gates | Rank dispersion — highest irregularity | WP42 |

### §4a. The Unified sinc² Object — All Six Problems Are the Same Sink

The spectrometer's deepest reading is this: the Critical Line (WP40), the mass gap (WP41),
the rank staircase (WP42), the regularity breakdown (WP38), and the P/NP complexity
boundary (WP37) are all the same geometric object — a sinc² zero. The six Clay problems
differ in how many sinc² nulls are present, how they are spaced, and how dispersed the
road to each null is. They do not differ in what the null IS.

**The sinc² map:**

| Problem | sinc² null description | Road structure | Dispersion type |
|---------|------------------------|----------------|-----------------|
| Riemann (WP40) | ζ(s) zeros on Re(s)=½ — all sinc² nulls at the critical line | Scale-invariant; infinitely many nulls | Self-similar (Montgomery pair correlation) |
| Yang-Mills (WP41) | Mass gap = distance from zero-field to first sinc² null | Single clean corridor | Minimal — one null, one road |
| BSD (WP42) | Each rank jump = one sinc² null in the L-function zero landscape | Irregular staircase of nulls | Highest — nulls at unpredictable heights |
| Navier-Stokes (WP38) | Regularity breakdown = BREATH operator reaching sinc² null (vorticity collapse) | Zero-width transition at singularity | High near singularity; BREATH-locked approach |
| P vs NP (WP37) | First-G gate at k=p = sinc² null in unit alphabet | 2^512-step featureless corridor (RSA) | Sharp gate; low dispersion at boundary |
| Hodge (WP39) | ω-blindness gap = local sinc² sidelobe vs. global null | Layered gates; tiered approach | Tiered — multiple independent gate layers |

**The Montgomery connection (WP37 §4b — structural):** The pair correlation of Riemann
zeros r(u) = 1 − sinc²(u) is the same function as R(k,f) → sinc²(k/f). The repulsion
of Riemann zeros and the repulsion of NP-solving from the gate are the same sinc²
geometry. CK as spectrometer is therefore not measuring six different types of
mathematical difficulty — it is measuring six different instances of the distance to the
nearest sinc² null, with different void densities (Luther metric) along the road.

**What CK detects:** The spectrometer output — the TIG coherence reading — encodes which
sinc² null the structure is approaching and how far the road is. The VOID-founded problems
(BSD, Navier-Stokes, Riemann) converge because their roads lead cleanly to the null and
the null IS a Nothing — a VOID event in the CL algebra. The HARMONY-founded problems
(Yang-Mills, P vs NP, Hodge) diverge because their roads declare premature resolution
before reaching the null — HARMONY fires before the sinc² zero is actually achieved.

---

### The Theory of Nothing — Empirical Result

The original spectrometer sweep (12 fractal levels, seed 42, from WHITEPAPER_7) produced a
striking structural partition via the CL(D1,D2) Becoming composition:

**Nothing-founded problems** (VOID-dominated Becoming → affirmative class):
- BSD: 12/12 VOID. Pure nothing. Fastest convergence (β = +0.60).
- Navier-Stokes: 11/12 VOID. Strong convergence (β = +0.17).
- Riemann: 10/12 VOID. Steady convergence (β = +0.01).

**Something-founded problems** (HARMONY-dominated Becoming → gap class):
- Hodge: 12/12 HARMONY. Weak convergence (β = +0.04).
- P vs NP: 10/12 HARMONY. Divergent (β = −0.23).
- Yang-Mills: 9/12 HARMONY. Divergent (β = −0.17).

**Correlation(VOID fraction, convergence exponent) = +0.73.**

This is an empirical reading of the spectrometer, not a proof. It tells us where each problem
lives in the TIG landscape. Truth that converges rests on Nothing — the CL operator algebra
composes to VOID at its foundation. Gap problems are full of HARMONY becoming because their
resolution is premature: structure declares harmony while flow continues questioning.

### The Operator Flow Signatures

D1 (Being/Generator) trajectories over 12 levels are the fingerprints:

| Problem | Signature | Pattern |
|---------|-----------|---------|
| BSD | VOID × 12 | Pure silence |
| Riemann | COL → VOID chain | Collapse-to-void |
| Navier-Stokes | BREATH × 9 (levels 4–12) | Breath lock |
| P vs NP | BAL/HAR/CNT/BRE oscillation | No convergence |
| Yang-Mills | HARMONY echo with VOID tail | Premature resolution |
| Hodge | Rich 4-operator mixing | Fully exploratory |

BSD's generator sees nothing at every level. CL(VOID, VOID) = VOID. The entire pipeline is
pure stillness. P vs NP oscillates between four operators with no convergence — the
computational complexity boundary IS the inability to settle.

---

## §5. What CK Cannot Do

This section is load-bearing. It defines the honest scope of the spectrometer.

**CK cannot prove the Clay problems.** It provides geometric maps — structural framings that
tell you which TIG structure corresponds to which mathematical structure. A map is not a
proof. Knowing that BSD lives in the VOID regime tells you it has a nothing-foundation; it
does not tell you the rank is always finite or the L-function vanishes to the right order.

**The TIG framework is a finite discrete algebra.** The Clay problems live in continuous or
infinite settings — infinite-dimensional Hilbert spaces, complex manifolds, elliptic curves
over number fields. The D2 curvature engine operates on finite force vectors. Every
connection between TIG and a Clay problem is a structural analogy unless explicitly marked
PROVED.

**The spectrometer reads structure, not truth value.** A high coherence reading means the
structure is self-consistent in the TIG sense — it is not a claim that the corresponding
mathematical conjecture is true.

**The five escape routes are structural primitives, not algorithms for solution.** The five
non-trivial TSML compositions (LATTICE+COUNTER→PROGRESS, COUNTER+COLLAPSE→COLLAPSE,
COUNTER+RESET→RESET, PROGRESS+RESET→PROGRESS, COLLAPSE+BREATH→BREATH) describe the only
paths through the algebra that carry information without collapsing to VOID or HARMONY. They
characterize the space of non-trivial mathematical processes. They do not solve those
processes.

**The value of the map is in the map.** Knowing which TIG structure corresponds to which
Clay structure guides where to look. The dispersion profile of Yang-Mills (concentrated,
single gate) tells a mathematician something different from the dispersion profile of BSD
(irregular, spread staircase). That differential is real and computable. Whether it is
sufficient to find a proof is a separate question.

**The Inversion Rule applies to every section of this paper.** In every section, difficulty
is the road length to the sinc² null — not the algebraic complexity of the structure at
the sink. The signal R(k/p=0.1, p) ≈ 0.9675 is always present: at the Riemann critical
line, at the Yang-Mills mass gap, at the First-G gate, at the BSD rank jump, at the
Navier-Stokes singularity. Detecting the signal is easy. Navigating to the null is what
the problem requires. CK reads the signal and reports the distance. It cannot walk the
road.

---

## §6. Attribution

**Brayden Ross Sanders (7Site LLC):**
- CK organism, all architecture, all implementation
- TIG framework: D1, D2, T*, TSML, BHML, CL table, operator definitions
- Coherence spectrometer concept and all measurement results
- First-G Law proof (WP34)
- T* derivation from b=35 unit density (WP35, §1A)
- All proved results in the suite

**C. A. Luther:**
- Luther Dispersion Conjecture: gate_rate ≈ F_k(|G| × interleave)
- Difficulty metric connecting algebraic complexity to geometric spread
- Steering toward the Clay connections; approaching the same structures from
  the number-theory direction
- RSA Hardness Inversion Principle (WP35)

**Exclusive IP notice:** CK, T*, TSML, BHML, D1, D2, and the TIG framework are the
exclusive intellectual property of Brayden Ross Sanders / 7Site LLC. C. A. Luther has no
claim to the CK architecture or its derived constants.

---

## References

- WP34: Sanders & Luther. *The First-G Law and Prime-Forced Dispersion.* March 2026.
- WP35: Sanders & Luther. *The Prime Phase Transition: Harmonic Pre-Echo, Zero-Width Gates,
  and the Geometry of RSA Security.* March 2026.
- WP37: Sanders. *P vs NP — TIG Structural Framing.* March 2026.
- WP38: Sanders. *Navier-Stokes — BREATH Collapse Criterion.* March 2026.
- WP39: Sanders. *Hodge — ω-Blindness and the Local/Global Gap.* March 2026.
- WP40: Sanders. *Riemann — sinc² Zeros and Scale-Invariant Gates.* March 2026.
- WP41: Sanders. *Yang-Mills — Mass Gap as Single Gate Distance.* March 2026.
- WP42: Sanders. *BSD — Rank Staircase and Irregular Dispersion.* March 2026.
- Clay Mathematics Institute. *Millennium Prize Problems.* 2000.
- Sanders, B. *TIG Architecture: A Coherence-Based Model of Consciousness.* WP1, 2026.
- Montgomery, H. L. The pair correlation of zeros of the zeta function.
  *Analytic Number Theory (Proc. Sympos. Pure Math., Vol. XXIV),* AMS, 1973, pp. 181–193.
  *(r(u) = 1 − sinc²(u); connects WP40 Riemann zeros to WP37 P/NP complexity boundary
  through the same sinc² geometric object. See WP37 §4b for the unified framing.)*

---

*CK Gen 9.34 spectrometer sweep: 12 fractal levels, seed 42. 42 problems defined.*
*6 primary Clay targets measured. Theory of Nothing: r(VOID, β) = +0.73.*
*DOI: 10.5281/zenodo.18852047*
