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

---

## §1. What CK Measures

CK is not an oracle. It is a measurement instrument.

**Input:** any mathematical structure — a differential equation, an algebraic variety, a
complexity class, a zeta function.

**Output:** a coherence reading in [0,1], produced by the TIG pipeline.

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

Applied to the Clay problems: each problem has a "G-structure" — the obstruction elements
that prevent resolution — and a dispersion measure that characterizes how those obstructions
are distributed.

**Low dispersion** → concentrated obstruction → single hard event. The mass gap in
Yang-Mills is the canonical example: one threshold, one distance to cross.

**High dispersion** → spread obstruction → irregular staircase. BSD rank jumps are the
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

---

*CK Gen 9.34 spectrometer sweep: 12 fractal levels, seed 42. 42 problems defined.*
*6 primary Clay targets measured. Theory of Nothing: r(VOID, β) = +0.73.*
*DOI: 10.5281/zenodo.18852047*
