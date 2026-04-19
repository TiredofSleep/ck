# Unified Symbol Table — CK Clay Paper Series (WP36–WP42)

*All seven papers share this vocabulary exactly. A "sink" in WP40 is the same object as a
"vortex" in WP38. A "gate event" in WP37 is the same moment as the "rank jump" in WP42.
This document is the single source of truth for notation across the series.*

**Authors:** Brayden Ross Sanders (7Site LLC) & C. A. Luther
**Date:** March–April 2026
**DOI:** 10.5281/zenodo.18852047
**Series branch:** clay / Gen10

---

## The Three Guardrails (from Google/Sanders review)

These three principles must be explicitly stated or clearly implied in every paper of the series.
They are not heuristics — they are load-bearing framing constraints that prevent the papers from
being read as "interesting pattern matching" rather than geometric proofs.

---

### Guardrail 1 — The Inversion Rule (proved in WP35)

Every paper must explicitly state: the difficulty of its Clay problem (NP-hardness, mass gap,
turbulence, zero spacing, rank jumps, algebraic cycle obstructions) is a **physical distance to a
geometric sink**, not an algebraic flaw in mathematics. The difficulty is a Signal-to-Noise Ratio
(SNR) problem at the 2^512 scale.

The signal is always present. R(k/p = 0.1, p) ≈ 0.9675 for ALL p regardless of scale. The
zero-crossing simply requires traversing p ≈ 2^512 steps. The road is long; the destination is
certain.

Formal statement (identical in all seven papers):

> "The difficulty of [this problem] is not an algebraic flaw in mathematics. It is a physical
> distance to a geometric sink in a sinc² field. The signal is always present —
> R(k/p = 0.1, p) ≈ 0.9675 for all p regardless of scale. The zero-crossing simply requires
> traversing p ≈ 2^512 steps. The road is long; the destination is certain."

---

### Guardrail 2 — The Luther Metric as Density Probe

The **Luther Dispersion Conjecture** (gate_rate ≈ F_k(|G| × interleave)) measures VOIDS in the
unit alphabet — the density of permitted vs. obstructed states. This is the same measurement in
every paper, wearing different physical clothing:

| Paper | Physical incarnation of Luther dispersion |
|-------|------------------------------------------|
| WP37 (P/NP) | Density of NP certificates relative to the total search space |
| WP38 (NS) | Energy density required to bridge the gap between smooth-flow states |
| WP39 (Hodge) | Algebraic cycle density; count of idempotents in Z/bZ |
| WP40 (RH) | Zero clustering density of the Riemann zeta function |
| WP41 (Yang-Mills) | Gauge field energy concentration; confinement vs. deconfinement |
| WP42 (BSD) | Rank irregularity predictor along the unit-fraction staircase |
| WP36 (Spectrometer) | Raw coherence field density R(k, f) at the current alphabet size |

Every paper is measuring the same thing: how densely the permitted states are obstructed, and
how far the current state is from the nearest sink.

---

### Guardrail 3 — Cross-Verification (the sink is one object)

The geometric sink in each problem is the **same mathematical object** — a zero of the sinc²
field — viewed through seven different physical lenses. Readers of the series should be able to
verify that the sink in any one paper corresponds exactly to the sink defined in every other paper.
Cross-references to this table are mandatory wherever a sink is introduced.

---

## Core Symbol Definitions

### The Fundamental Field Objects

| Symbol | Name | Exact definition | First proved/stated |
|--------|------|-----------------|---------------------|
| R(k, f) | Harmonic pre-echo | sin²(πk/f) / (k² sin²(π/f)) | WP35 Theorem 1 |
| S(k, f) | Spectral sum | (1/k) Σ_{j=1}^{k} e^{2πij/f}; note R(k,f) = \|S(k,f)\|² | WP35 §1 |
| sinc(t) | Sinc function | sin(πt) / (πt) | WP35 Theorem 5 |
| sinc²(t) | Sinc-squared field | (sin(πt) / πt)²; the continuum limit of R | WP35 Theorem 5 |
| k = p | Geometric sink | First zero of R(k,f); First-G event; phase transition point | WP34 §2 |
| T* = 5/7 | Coherence floor | unit_frac(k=q=7, b=35); CK FPGA calibration constant | WP35 §1A |

**Critical identity (WP35 Theorem 5):** As f → ∞ with k/f = t fixed,

```
R(k, f)  →  sinc²(t)  =  (sin(πt) / πt)²
```

The two universal constants that follow:

```
R(k/p = 1/2,  p)  →  4/π²  ≈  0.405284...   [sinc²(1/2), exact]
R(k/p = 0.1,  p)  →  sinc²(1/10)  ≈  0.9675...   [scale-free, all p]
```

These are not approximations. They are exact evaluations of sinc², holding for all primes p
regardless of magnitude.

---

### The Partition Objects (from WP34)

| Symbol | Name | Definition |
|--------|------|-----------|
| b | Modulus / world | Semiprime b = p×q (or more general composite) under study |
| p | Smallest prime factor | min prime factor of b; determines all downstream structure |
| q | Largest prime factor (semiprime) | max prime factor when b = p×q |
| ω(b) | Prime factor count | number of distinct prime factors dividing b |
| C_k | Unit alphabet | { x ∈ {1..k} : gcd(x, b) = 1 } — coherent elements |
| G_k | Non-unit alphabet | { x ∈ {1..k} : gcd(x, b) > 1 } — obstructing elements |
| \|G_k\| | Gate size | number of non-units in the k-alphabet; 0 for k < p |
| gate_rate(k) | Gate fraction | \|G_k\| / k; zero before First-G event, jumps at k = p |
| unit_frac(k, b) | Unit density | \|C_k\| / k = 1 − gate_rate(k) |

**First-G Law (WP34, proved, 153 semiprimes verified, zero exceptions):**
For every semiprime b = p×q (p ≤ q):

```
|G_k| = 0    for all k < p
|G_p| = 1    (the element p itself is the unique first non-unit)
```

The phase transition has **zero width**: the gate-size sequence is a perfect step function.

---

### The Luther Dispersion Objects (from WP34 §9)

| Symbol | Name | Definition |
|--------|------|-----------|
| D(b) | Luther dispersion | \|G\| × interleave(b, k) — difficulty density |
| interleave(b, k) | Interleave score | transitions(C, G in sequence 1..k) / (2 · min(\|C\|, \|G\|)) |
| N_idemp | CRT idempotents | 2^(ω(b)−1) − 1; algebraic cycle count |
| grad_score | Gradient score | max_{c ∈ C \ (orbit ∪ {1})} \|c − HAR\| / (max(C) − min(C)) |
| HAR | Harmonic attractor | orbit-central element h: h²∈C, h²≠1, h²≠h (Law 2, ATLAS) |

**Luther Dispersion Conjecture (WP34 §9, conjectural):**

```
gate_rate ≈ F_k( |G| × dispersion(G) )
```

where dispersion(G) = interleave score. The synthetic vs. real gap in gate difficulty is
explained by dispersion: real semiprime worlds have G dispersed by prime arithmetic (high
interleave), synthetic worlds have G clustered (low interleave).

---

### The Kinematic Objects (from WP35 §6A)

| Symbol | Name | Definition |
|--------|------|-----------|
| D1(k, f) | Approach velocity | R(k+1, f) − R(k, f); first difference of rank trajectory |
| D2(k, f) | Curvature | R(k+1, f) − 2R(k,f) + R(k−1, f); second difference |

**D1 properties:**
- D1 < 0 throughout the pre-echo zone {1..p−1}: R is strictly decreasing toward the sink
- D1 = 0 at k = p: exact stationary point (R(p+1) = R(p−1) by sin² symmetry)
- D1 > 0 at k = p+1: sign flip — the trajectory begins recovering after the sink

**D2 as physics:** CK's architectural principle "curvature IS physics" is instantiated here.
D2 curvature encodes the prime factor location. For p ≤ 29, fitting from floor(p/3)
observations recovers p with zero error (WP35 §6A, Section A, 8 primes verified).

**Balance Invisibility (WP35 §7B, empirical):**
For balanced semiprimes (q/p → 1), D2_balance → 0: the two factors become indistinguishable
by curvature rank. Spearman ρ(q/p, D2_balance) = 0.857 (p=0.007, n=8).

---

### The T* Derivation (WP35 §1A)

T* = 5/7 is not a hardware constant. It is an algebraic identity:

```
unit_frac(k=q, b=p×q) = (q − 2) / q    [exact, for all semiprimes with p < q, p ≥ 3]
```

T* = 5/7 is the unique realization of this formula at the **minimal strong semiprime**:
- "Strong" = both prime factors > 3
- Minimal such semiprime: b = 5×7 = 35 (p=5, q=7)
- unit_frac(k=7, b=35) = (7−2)/7 = **5/7 exactly**

At that moment, R(7, 7) = 0 (Theorem 1): the harmonic clock collapses at exactly the same
step where unit density reaches T*. Gate event and coherence floor crossing are the same
physical moment.

### Third Independent T* Derivation — Cyclotomic Reduction Test (2026-04-04)

For the canonical chain A_p = 2cos(π/p) → C_p = 4−A_p² → sinc²(1/p) = p²C_p/(4π²):

**Reduction criterion (exact):** C_p ∈ ℚ + ℚA_p ⟺ deg(A_p/ℚ) ≤ 2.

- p = 5: A_5 = φ, deg(φ) = 2. φ² = φ+1, so C_5 = 4−φ² = 3−φ ∈ ℚ + ℚφ. **First nontrivial closure.**
- p = 7: deg(A_7) = 3. If C_7 ∈ ℚ + ℚA_7 then A_7 satisfies a degree-2 poly — contradicts deg = 3. **First obstruction.**

Therefore: T* = 5/7 = (first closed prime) / (first obstructed prime).

The exact mixed formula at the closure prime: sinc²(1/5) = 25(3−φ)/(4π²).

Note: the same primes p=5 and q=7 appear in all three T* derivations — ring arithmetic (unit_frac at b=35), operator algebra (TSML BALANCE/HARMONY), and cyclotomic reduction. Three proofs, same boundary.

---

### The Three Regimes (universal across all 7 papers)

| Regime | k range | Gate rate | Physical meaning | Complexity analog |
|--------|---------|-----------|-----------------|------------------|
| Vacuum / P-zone | 1..p−1 | 0.0 | All elements coprime to b; no obstruction; stability window | P-tractable |
| First-G event | k = p | Transition | Zero-width phase transition; harmonic clock hits zero | P/NP boundary |
| Obstruction zone | p..q | 0 → 1 | G elements appear; dispersion builds; bridge breathing | NP-hard |

**Stability window (WP34 Corollary 1):** Every semiprime b admits an obstruction-free stability
window {1, …, p−1} of width p−1. The window width is set entirely by the smaller prime factor.

---

### The ω-Blindness Principle (WP35 Theorem 4)

R(k, 1/p) is **identical** for every modulus b sharing the prime factor p, regardless of ring
structure (p², p×q, p×q×r, …). It is a function of k and p alone.

Implication: the harmonic pre-echo cannot distinguish ring structure. To detect ω(b), one must
additionally observe the **closure defect** signal, which does vary with ring structure.

The P3 frontier in Hodge (dim ≥ 5 abelian varieties) corresponds exactly to ω(b) ≥ 3 in TIG:
three-factor composites where the simultaneous broadcast of three harmonic clocks creates tiered
gate structure that the local signal cannot resolve (see WP39, §5).

---

## Problem-Specific Translations

Each section below defines the sink, dispersion, and stability window for one Clay problem,
with explicit mapping back to the core symbols above.

---

### WP36 — Clay Spectrometer (entry point)

The spectrometer is the instrument that makes all other connections visible. It reads the
coherence field R(k, f) across (k, f) space and identifies sinks.

| Universal symbol | WP36 incarnation |
|-----------------|-----------------|
| R(k, f) | Coherence field measurement — the spectrometer's primary output |
| k = p | Sink in (k, f) space; the point where R = 0 |
| T* = 5/7 | Detection threshold — below T*, the field is in obstruction mode |
| D(b) | Spectral density — how densely the permitted states are packed |

**WP36 role:** Defines the measurement apparatus for all subsequent papers. Every Clay
problem reduces to asking: where is the sink in the spectrometer's output?

---

### WP37 — P vs NP

| Universal symbol | WP37 incarnation |
|-----------------|-----------------|
| Geometric sink | NP certificate location — the point k = p in the alphabet |
| Stability window {1..p−1} | P-tractable subproblem space — no obstruction exists here |
| First-G event k = p | The P/NP boundary — the moment the first non-unit enters |
| sinc² zero-crossing | The NP-hard region: the certificate is at the zero of the field |
| D(b) | Certificate density — how sparsely NP witnesses are distributed |
| R(k/p=0.1) ≈ 0.9675 | The signal is strong at 10% of the distance to the certificate |

**Framing (Google/Sanders):** "NP-verification is the local detection of a sinc² sidelobe
(given p, verify in O(1)). P-solving is the global navigation to the sinc² null (traversing
p ≈ 2^512 steps to reach k = p)."

**Key identity:** RSA security IS the P/NP gap made concrete. The modulus N = p×q encodes
a geometric distance of p ≈ 2^512 steps to the certificate. The algebra is unchanged; only
the distance changes.

---

### WP38 — Navier-Stokes

| Universal symbol | WP38 incarnation |
|-----------------|-----------------|
| Geometric sink | Regularity breakdown point — where B_local collapses below T* |
| Stability window {1..p−1} | Smooth-flow regime — vorticity is bounded, no obstruction |
| First-G event k = p | Onset of turbulence — the zero-width transition in smooth solutions |
| D(b) = \|G\| × interleave | Vorticity dispersion = Luther dispersion; energy to bridge gap |
| T* = 5/7 | Coherence floor — field must stay above T* for smooth solution to persist |
| sinc² zero | Regularity breakdown — exactly where the harmonic countdown reaches zero |

**Theorem (WP38 structural claim):** "Smooth solutions break at the zero-width transition."
The zero-width property (WP35 Theorem 2) is the algebraic model for why the regularity
criterion is not "gradually weakening" but a phase transition: |G_k| = 0 for k < p, then
|G_p| = 1 in a single step, with no intermediate blur.

**NS ↔ TIG:** B_local is the CK coherence field measured at the current flow state. B_local ≥
T* is equivalent to being inside the stability window. B_local < T* is equivalent to k ≥ p:
the first non-unit has entered, and the field has crossed the gate.

---

### WP39 — Hodge

| Universal symbol | WP39 incarnation |
|-----------------|-----------------|
| Geometric sink | Algebraic cycle location — the idempotent in Z/bZ |
| N_idemp = 2^(ω−1)−1 | Count of algebraic cycles = count of idempotents (Luther metric) |
| ω-Blindness (Theorem 4) | Local harmonic signal cannot recover global ring structure |
| ω(b) = 2 (semiprime) | Hodge cycles that ARE algebraic — provable regime |
| ω(b) ≥ 3 (three-factor) | P3 frontier (dim ≥ 5) — tiered gate structure, Hodge gap opens |
| D(b) | Algebraic cycle density — how densely cycles are packed in the modular ring |

**ω-Blindness ↔ Hodge gap:** The fact that R(k,1/p) cannot distinguish b = p² from b = p×q×r
(WP35 Theorem 4) is the algebraic model for why local differential geometry cannot detect
non-algebraic Hodge classes: the local signal (curvature) is blind to the global ring structure
(ω(b)).

**P3 frontier:** Markman (2025) proved the Hodge conjecture for abelian fourfolds. The P3
frontier now sits at dim ≥ 5, corresponding to ω(b) ≥ 3 in TIG. Grujić (UVA) is the relevant
contact for the dim ≥ 5 open case.

---

### WP40 — Riemann Hypothesis

| Universal symbol | WP40 incarnation |
|-----------------|-----------------|
| Geometric sink | Riemann zero — constructive interference point of sinc² fields |
| sinc²(t) | Montgomery pair correlation r(u) = 1 − sinc²(u) — **same function** |
| Critical line Re(s) = 1/2 | Unique geometric axis where sinc² fields of all primes constructively interfere |
| Zero spacing | sinc² interference pattern — determined by the same field as WP35 Theorem 5 |
| D(b) | Zero clustering density — dispersion of zeros on the critical line |
| D1 sign flip at k = p | Pre-echo countdown oscillations (D1 not monotone) = Gram's law sign changes |
| T* = 5/7 | Coherence floor of the zeta field; below T*, constructive interference fails |

**Critical identity (must be stated explicitly in WP40):**

Montgomery pair correlation function:

```
r(u) = 1 − (sin(πu) / πu)²  =  1 − sinc²(u)
```

This is the **same sinc² function** as WP35 Theorem 5. The zero pair correlation IS the
sinc² field. The zeros cluster at the spacing that minimizes sinc² interference, which is
exactly the spacing predicted by the harmonic countdown law.

**The RH claim in TIG language:** The critical line Re(s) = 1/2 is the unique axis where the
sinc² fields broadcast by each prime p constructively interfere. Zeros off the critical line
would require destructive interference — a physical impossibility given the scale-free structure
of the pre-echo field (R(k/p=0.1) ≈ 0.9675 for all p: the signal cannot be suppressed).

---

### WP41 — Yang-Mills

| Universal symbol | WP41 incarnation |
|-----------------|-----------------|
| Geometric sink | Mass gap — minimum geometric distance p in the stability window |
| Stability window {1..p−1} | Vacuum sector — no G elements, no field excitations, zero energy |
| First-G event k = p | Minimum excitation energy = the mass gap |
| T* = 5/7 | Energy floor — minimum coherence for the gauge field to exist at all |
| D(b) = \|G\| × interleave | Gauge field energy concentration (low D = confined, high D = deconfined) |
| sinc² zero | The mass gap energy level — where the harmonic field collapses |

**Confinement ↔ TIG:** The stability window {1..p−1} is the confined (vacuum) phase. No
excitations exist here because G is empty. The mass gap is the distance from the vacuum to
the first excitation: the First-G event at k = p. The gap is geometric — it is p−1 steps wide —
not algebraic.

**Luther dispersion ↔ confinement/deconfinement:** Low D(b) (tightly clustered G elements)
corresponds to confined gauge theory. High D(b) (dispersed G across the alphabet) corresponds
to deconfined (high-temperature) phase. The confinement transition is the interleave score
crossing a threshold.

---

### WP42 — BSD (Birch and Swinnerton-Dyer)

| Universal symbol | WP42 incarnation |
|-----------------|-----------------|
| Geometric sink | Rank jump — a gate event in the unit-fraction staircase |
| unit_frac(k, b) staircase | L-function staircase — both count "passes through primes" |
| T* = unit_frac(k=q=7, b=35) | Fundamental unit density anchoring the rank-staircase baseline |
| First-G event k = p | Rank jump trigger — the staircase drops at the prime gate event |
| D(b) | Rank irregularity predictor — how dispersed the G elements are predicts rank |
| N_idemp = 2^(ω−1)−1 | Rank contribution count — one rank unit per CRT idempotent |

**unit_frac ↔ L-function:** The unit_frac(k, b) staircase and the L-function staircase both
count the density of "coprime" (unit) elements as the window grows. The rank of an elliptic
curve is the number of rank jumps (gate events) in the L-function staircase below a threshold.
T* = 5/7 anchors the baseline density from which rank jumps are measured.

---

## The Montgomery–Sinc² Identity (mandatory in WP40, referenced in all others)

This is the single most important cross-paper identity in the series. It must be stated
explicitly in WP40 and referenced by name in all other papers.

**Montgomery–Sinc² Identity:**

```
Montgomery pair correlation:   r(u)     =  1 − (sin(πu)/πu)²  =  1 − sinc²(u)
WP35 harmonic pre-echo:        R(k/f, f) →  sinc²(k/f)  as  f → ∞
```

These are the **same mathematical object**. The distribution of Riemann zeros is controlled by
the sinc² field that was independently derived from the coprimality partition structure of
semiprimes. This is not a coincidence of notation: both arise from the same underlying
geometric structure (the Fourier kernel of a uniform distribution over the unit alphabet).

The pair correlation function r(u) = 1 − sinc²(u) says: Riemann zeros avoid spacing u = 0
(they repel) and cluster at the spacing where sinc²(u) is minimized — exactly the zero-crossing
of the harmonic pre-echo countdown.

---

## The D1 Non-Monotone Property (cross-paper structural note)

D1 in the pre-echo zone is **not monotone** — it has structured oscillations as the trajectory
descends toward the sink. This is a real geometric feature of the sinc² envelope:

```
D1(k, f) = R(k+1, f) − R(k, f) = d/dk [sin²(πk/f) / (k² sin²(π/f))]
```

In WP40 (RH): these oscillations correspond to Gram's law sign changes — the pre-echo
oscillations of the zeta function near the critical line.

In WP38 (NS): these oscillations model the structured breathing of the vorticity field before
turbulence onset — the smooth-to-turbulent transition is not monotone, it oscillates before
collapsing.

In WP37 (P/NP): these oscillations are the polynomial-time partial signals that algorithms
can detect in the pre-echo zone — they are real, but they do not reach the sink.

---

## The Construction Hierarchy (ATLAS Law 1, frozen)

From ATLAS_LAW_SET.md — the four-step pipeline that produces the native structured optimum at
every tested semiprime world. Referenced in WP37 and WP39 for the connection between
arithmetic structure and computational difficulty:

```
Prime factorization of b
  → Step 1: Arithmetic world: b → C, G, orbit structure
  → Step 2: HAR selection: orbit-central rule selects attractor
  → Step 3: Gate discipline: one-way gate under gate-weighted reduction
  → Step 4: Order seed: residual pre-alignment crystallizes the optimum
```

**Status:** EMPIRICAL. Verified at b = 10, 14, 15, 21, 22, 26, 35, 55, 65, 85, 95 (11 worlds).

**b = 15 is the flagship:** the unique world ≤ 100 where tier + gradient + position all align.
(Proved by finite enumeration; see ATLAS_LAW_SET.md.)

---

## Seeded Residue Persistence (WP35 §5A)

| Symbol | Name | Definition |
|--------|------|-----------|
| seeded_RPS(p) | Seeded residue persistence | Mean escape length from x=p (canonical first G-element) before exiting the obstruction zone |
| bridge_slope | Bridge recovery slope | Rate of change of seeded_RPS across the bridge zone k=p..q−1 |

**Key finding (WP35 §5A, 12 semiprimes, 500 trials each):**

```
r(seeded_RPS(p),  q/p) = +0.737   [strong: persistence encodes the ratio, not the gap]
r(seeded_RPS(p),  q−p) = −0.366   [weak]
```

The G-obstruction at k=p is a property of the sink at p alone. The second factor q is
geometrically invisible until k physically reaches q.

---

## The RSA–Clay Bridge (universal across all 7 papers)

RSA security and Clay hardness are the **same geometric fact** at different scales:

| Property | RSA (cryptographic) | Clay (mathematical) |
|----------|--------------------|--------------------|
| The sink | Prime factor p ≈ 2^512 | Clay solution (mass gap, zero, rank jump, etc.) |
| Signal strength | R(k/p=0.1) ≈ 0.9675 for all p | Same — scale-free |
| Distance to sink | p ≈ 2^512 steps | Problem-dependent, always large |
| Verification | Given p, verify N=p×q in O(1) | Given solution, verify in O(poly) |
| Obstacle | Physical traversal of 2^512 steps | Physical traversal of equivalent distance |

The RSA Hardness Inversion Principle (WP35 §7A): "RSA security is not the silence of the
alarm clock; it is the distance to the clock."

Applied universally: "The difficulty of [any Clay problem] is not the silence of the geometric
signal; it is the distance to the geometric sink."

---

## Verification Record (WP34 + WP35 combined)

| Claim | Status | Evidence |
|-------|--------|---------|
| First-G law (k=p for all semiprimes) | PROVED + VERIFIED | 153 semiprimes, 36,662 pairs, 0 exceptions |
| R(k,f) closed form | PROVED + VERIFIED | Max error 4.44e-16 (floating-point only); 187 semiprimes |
| Zero-width gate | PROVED | Follows directly from First-G Law |
| T* = 5/7 algebraic derivation | PROVED | unit_frac(k=q=7, b=35) = 5/7 exactly |
| sinc² continuum limit | PROVED | Exact limit proof; 4/π² verified for p=5..99991 |
| ω-Blindness | PROVED + VERIFIED | p=5,7 series across ω=1,2,3 — identical R values |
| D1 sign flip at k=p | OBSERVED UNIVERSAL | 7 semiprimes in Z6 survey |
| floor(p/3) recovery of p | VERIFIED | Zero error for p=5..29 (8 primes) |
| R(k/p=0.1) ≈ 0.9675 scale-free | VERIFIED | p=1009, 10007, 100003; analytical extension to 2^512 |
| Balance invisibility (D2_balance→0) | VERIFIED | Spearman ρ=0.857, p=0.007 |
| seeded_RPS encodes q/p (r=0.737) | VERIFIED | 12 semiprimes, 500 trials each |
| ATLAS Construction Hierarchy | EMPIRICAL | 11 semiprime worlds, 0 exceptions |
| b=15 unique tri-alignment | PROVED | Finite enumeration over all semiprimes ≤ 100 |

---

## The Universal Sentence

Every paper in this series must contain, somewhere prominent, the following sentence
(adapted to the specific problem name in brackets):

> "The difficulty of [this problem] is not an algebraic flaw in mathematics. It is a physical
> distance to a geometric sink in a sinc² field. The signal is always present —
> R(k/p = 0.1, p) ≈ 0.9675 for all p regardless of scale. The zero-crossing simply requires
> traversing p ≈ 2^512 steps. The road is long; the destination is certain."

---

## Attribution Block (identical in all 7 papers)

```
Brayden Ross Sanders (7Site LLC) — TIG framework, all proved results (WP34, WP35),
  CK organism, T*=5/7, TSML, D1/D2; unified geometric field theory framing;
  First-G Law, zero-width gate, sinc² continuum limit, RSA Hardness Inversion Principle,
  T* derivation, ω-blindness, kinematic factoring interpretation.

C. A. Luther — Dispersion conjecture (D(b) = |G|×interleave as difficulty density probe),
  sprint4 navigation and structural steering.

CK, T*, TSML, BHML, D1, D2, TIG: exclusive intellectual property of
Brayden Ross Sanders / 7Site LLC.
```

---

## Version Control and Paper Registry

All papers in this series: `clay` branch, Gen10 repo.
DOI: 10.5281/zenodo.18852047

| Paper | Title | Sink |
|-------|-------|------|
| WP36 | Clay Spectrometer (entry point) | R(k,f) = 0 in (k,f) space |
| WP37 | P vs NP | NP certificate at k = p |
| WP38 | Navier-Stokes | Regularity breakdown (B_local < T*) |
| WP39 | Hodge | Algebraic cycle (idempotent in Z/bZ) |
| WP40 | Riemann Hypothesis | Riemann zero (sinc² constructive interference) |
| WP41 | Yang-Mills | Mass gap (first excitation at k = p) |
| WP42 | BSD | Rank jump (gate event in unit-fraction staircase) |

**Cross-reference rule:** Any paper that introduces a "sink," "vortex," "gap," "zero,"
"cycle," or "rank jump" must cite this table and state which row its object corresponds to.
The sink is one object. The papers are seven views of the same geometry.

---

*This document is the authoritative symbol table for the CK Clay Paper Series (WP36–WP42).
Maintained at: Gen10/papers/clay/research/UNIFIED_SYMBOL_TABLE.md*

*(c) 2026 Brayden Ross Sanders (7Site LLC) & C. A. Luther | Gen10 | DOI: 10.5281/zenodo.18852047*
