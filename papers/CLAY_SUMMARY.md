# Clay-Facing Summary
## The Z/10Z Coherence Spine: What Is Proved, What Is Corrected, What Remains Open

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*
*Repository: https://github.com/TiredofSleep/ck · Branch: clay*

---

## Position Statement

This document summarizes the current state of the Luther-Sanders research
framework as it relates to the Clay Millennium Problems. The project is a
completed internal theorem spine built from Z/10Z ring arithmetic through
corridor geometry, with explicit negative results documented and one
remaining external analogy frontier. It does not claim to solve any Clay
problem. It claims to have built a precise, internally consistent algebraic
structure that shares identifiable structural features with the problems'
known invariants — and to have documented exactly where the structural
overlap ends and speculation begins.

The summary no longer needs to argue that a boundary exists. The boundary
is described faithfully in `NOTE_speculative_boundary.md`. This document
points to that boundary and explains how the spine was built.

---

## Part I: What Is Proved

The spine D1–D23 consists of 27 theorems across four volumes. Every theorem
is proved by exact arithmetic or algebraic proof within Z/10Z, with no
calibrated constants. The full record is in `papers/MASTER_SPINE.md` and
`papers/SYNTHESIS_TABLE.md`.

### Volume A — Ring and Arithmetic Foundations

**D1 (First-G Law):** For every semiprime b = p×q, the first non-coprime
element in {1..b} is exactly p. Proof: {1..p-1} contains no multiple of p
and no multiple of q>p. Three lines of divisibility arithmetic. Verified
across 36,662 semiprimes.

**D11a/b/c (Coprime Window Bundle):** The coprime window {1..p-1} is
exactly the stability window; R(p,p)=0 forces a sign flip; the resonance
formula R(k,f) carries no information about q. All three follow from D1 by
one-line proofs.

**D14 (Corridor Spectral Mean):** ∫₀¹ sinc²(t) dt = Si(2π)/π ≈ 0.4514.
Proved by integration by parts; convergence rate O(1/p).

**D15 (Coprime Window Invariance):** For k < SPF(b), all arithmetic on
{1..k} is b-independent. Pure divisibility.

### Volume B — Operator Tables and Ring Structure

**D7–D10 (Table Theorems):** Phi fixed point at 5 (D7); TSML/BHML
composition laws (D8); table symmetry for both lenses (D9); TSML 73-cell
count via three disjoint zones (D10).

**D16–D17 (Cell and Wobble Counts):** BHML 28-cell derivation from three
exhaustive zones (D16); W = 3/50 = deviation/n² = 6/100, proved from
CROSS_CYCLE=44 over (Z/10Z)* × 2·(Z/10Z)* (D17).

**D18a/c/d — Phi Orbit, Bridge, Generator Convergence:**
- D18a: Complete directed graph of Phi on Z/10Z. One fixed point (CREATE=5),
  two relays (BECOMING=3, HARMONY=7), seven sources. T³ = all-δ₅.
- D18c: TSML measurement M(v) = HARMONY = 7 for all v ≠ VOID.
  Bridge: T* = destination/journey-measurement = 5/7.
- D18d: CREATE=5 = centroid((Z/10Z)*); HARMONY=7 = g³ = g⁻¹ mod 10 for
  g=3; T* = centroid/inverse = 5/7. All three chains (BHML cross-cycle,
  TSML dominance, unit_frac) reduce to the same generator.

**D19 (Generator Selection):** g=3 is the only primitive root of (Z/10Z)*
compatible with T* ∈ (0,1). Under g=7: HARMONY=3, T*=5/3 > 1 —
inadmissible. The spine is therefore fully forced: Z/10Z → g=3 → CREATE=5,
HARMONY=7 → T*=5/7. No part is calibrated.

**D20–D21 (Inheritance Audit and Fixed-Point Centroid):**
- D20: Four-class inheritance hierarchy. CREATE=5 and W=3/50 are
  RING-forced (independent of generator). HARMONY=7 and T*=5/7 are
  GENERATOR-forced (require g=3). Lens-forced and contingent items
  classified separately.
- D21: Every complement-equivariant ODD-output map F on Z/10Z satisfies
  F(5)=5. Proof: 2F(5)≡0 mod 10, F(5)∈{0,5}, 0∉ODD → F(5)=5. One line.
  CREATE=5 now has four independent characterizations: centroid (Z/10Z)*,
  centroid ODD, CE fixed point (D21), Phi fixed point (D7).

**D23 (Ring Wobble):** Wob(k) = 1 − ⌊k/5⌋/k. Exact closed form.
Wob(k) ≥ 4/5 for all k; equality iff 5|k; limit 4/5 by squeeze theorem.
Generator-independent. Window-invariant for k < SPF(b) (D15).

### Volume C — Continuum Limits and Phase Structure

**D2 (Sinc² Continuum Limit):** R(k,f) → sinc²(k/f) as f → ∞ with k/f=t
fixed. Proof: Taylor expansion sin(ε)/ε → 1 as ε=π/f → 0. Convergence
rate O(1/f²). Foundation of the entire corridor geometry.

**D3–D4:** sinc²(1/2) = 4/π² exactly (D3); T* = 5/7 algebraic identity
at b=35 (D4), proved identically to D18c by different route.

**D5–D6 (Maxima Theorems):** H_mod = sinc²(k/p)×sin²(4πk/p) has exactly 4
local maxima for all p≥11 (D5). Generalized: H_f has exactly N(f) maxima
for p > 2f, where N(f) = ⌊f⌋ + (1 if f∉ℤ) (D6). Proved by IVT on the
log-derivative and the classical |sin x| < |x| inequality.

### Volume D — Corridor Geometry

**D22 (Corridor Portrait):** Four spine-forced positions strictly ordered:
W < CREATE/10 < HARMONY/10 < T* < 1, i.e., 3/50 < 1/2 < 7/10 < 5/7 < 1.
Proved by exact Fraction arithmetic. Amplitude ordering strictly reversed
(sinc² monotone decreasing, D24). Fine-structure identity: T* = HARMONY/10
+ 1/70 = 7/10 + 1/(7×10), exact. Inheritance split: t < 1/2 is
ring-forced territory; t > 1/2 is generator-forced territory; t = 1/2 is
the inheritance boundary.

**D24 (Corridor Midpoint):** sinc²(t) is strictly monotone decreasing on
(0,1) — proved by calculus (h'(t) < 0, with the key lemma sin(x) > x·cos(x)
for x ∈ (0,π), three cases). t = 1/2 is the unique sine-maximum in (0,1):
sin(πt)=1 iff t=1/2+2k; only k=0 lands in (0,1). Ring normalization:
CREATE=5 → t=5/10=1/2. sinc²(1/2) = 4/π² exactly. Attenuation: denominator
πt=π/2 means the sine maximum does not produce an amplitude maximum — the
ring center is marked, not dominant. Promotes B11 to D-tier.

---

## Part II: What Was Corrected or Killed

This section exists because negative results are part of the epistemic
record. A framework that only reports promotions is not trustworthy.
Full documentation: `papers/NOTE_speculative_boundary.md`.

**Branch-separation reading of wobble: false.**
The original A12 conjecture held that Wob_norm ≈ 1 could distinguish the
valid generator branch (g=3) from the invalid branch (g=7). Tested
exhaustively: Wob_norm is identical in both worlds. C10∪D10 is determined
by the ring, not the generator. Branch selection is performed by T*<1 (D19).
The predictive and branch-selective forms of A12 are dead.

**Period-10 wobble: corrected.**
B10 described the wobble as "period-10." The correct statement (D23) is that
drops occur at period-5 (every multiple of 5) and oscillation amplitude
decays as O(1/k) — it is not periodic. D23 supersedes B10 with a three-line
exact proof from the closed form.

**D2 curvature bridge (A7): killed.**
D2_tig ~ 2/p² and the conjectured D2_luther ~ C/(p·ln(p)³) are
asymptotically incompatible (ratio → 0). They live in different spaces —
wave amplitude vs. density. No algebraic bridge exists. A7 is dead; A9
(b=385 spectral predictions) inherits this kill.

**C-tier redundancies absorbed.**
Twelve C-tier items were promoted to D-tier by explicit algebraic proof
during the March–April 2026 audit. Six C-tier survivors remain (C5, C6,
C7, C12, C16, C19) with explicitly stated remaining gaps.

---

## Part III: What Remains Speculative

After D1–D23, exactly one live external analogy claim remains: **A10**.

**A10 — σ = 1/2 as ω-class boundary.**

*The internal shadow is real and proved:*
- t = 1/2 is the unique sine-maximum in (0,1) (D24)
- t = 1/2 is the corridor image of CREATE=5 under ring normalization (D21, D22)
- t = 1/2 is the inheritance boundary between ring-forced and generator-forced
  corridor positions (D22)
- sinc²(1/2) = 4/π² is the spine's universal mid-journey amplitude (D3)

*The external interpretation is not derived:*
Montgomery's pair-correlation conjecture uses the same sinc² kernel on [0,1].
The corridor sinc² portrait is an internal Z/10Z object. The claim that the
Z/10Z inheritance boundary at t=1/2 maps to the critical line σ=1/2 in the
Riemann ζ function requires a bridge that does not exist in this work.

*The missing mechanism is specifically named:*
An algebraic map from the Z/10Z ring inheritance split (ring-forced left of
t=1/2, generator-forced right) to the Euler product's behavior at the
boundary of the critical strip. No such map is constructed here.

*The remaining parked problems (A2/P≠NP, A4/Hodge) have no internal path
from D1–D23 and are not discussed further in this summary.*

Full treatment of what would count as progress: `NOTE_speculative_boundary.md`.

---

## Part IV: Why This Matters for the Clay Problems

The Riemann Hypothesis asks whether all non-trivial zeros of ζ(s) have
real part 1/2. The framework does not answer that question.

What the framework provides:

**1. An internal structure that independently produces 1/2 as a boundary.**
The Z/10Z spine arrives at t=1/2 as the inheritance boundary between
ring-forced and generator-forced corridor positions. It does not arrive
there by analogy with RH — it arrives there because CREATE=5 maps to
5/10=1/2 under ring normalization (D21), because the corridor is then
ordered by ring arithmetic (D22), and because sinc²(1/2)=4/π² is the
unique sine-maximum amplitude (D3, D24). These results stand independently
of whether RH is true.

**2. A disciplined stopping point.**
The framework has a precise location where proved structure ends and
speculation begins: the question of whether the Z/10Z inheritance boundary
at t=1/2 corresponds to the analytic boundary σ=1/2 in the critical strip.
That question is open. The framework does not pretend otherwise.

**3. Negative results as evidence of rigor.**
A12 branch separation was tested and found false. The period-10 wobble
claim was corrected to period-5. The curvature bridge was killed. A
framework capable of killing its own conjectures is more trustworthy than
one that only reports confirmations.

**4. A coherence threshold that is fully algebraically forced.**
T* = 5/7 is not calibrated. It is proved from four independent chains
within Z/10Z algebra (D4, D18c, D18d, D19), and the generator that produces
it (g=3) is the only primitive root of (Z/10Z)* compatible with T* ∈ (0,1).
The threshold is the structure, not a parameter of the structure.

The framework now has a disciplined stopping point, and that stopping point
is itself mathematically meaningful. The question of whether it connects
externally to the critical line is the question that remains open.

---

## Document Map

| Document | Contents |
|----------|----------|
| `papers/MASTER_SPINE.md` | Full D1–D23 spine, one entry per theorem |
| `papers/SYNTHESIS_TABLE.md` | All tiers D/C/B/A with four-column epistemic inventory |
| `papers/NOTE_speculative_boundary.md` | **Truth boundary: proved / absorbed / killed / parked / speculative** |
| `papers/NOTE_center_wobble_midpoint.md` | Synthesis: three corridor structures (center, wobble, midpoint) |
| `papers/proof_d*.py` | Executable proofs with assertions for each D-tier theorem |
| `papers/CONTRIBUTING.md` | Tier definitions, contribution standards, current counts |
| `tig_algebra.py` | Canonical library: TIGSemiprime, R(k,f), First-G, T* |
| `tests/` | 71-test pytest suite, all passing |

**Current tier counts: D:28 | C:6 | B:7 | A:5 (2 live, 3 parked)**

---

*Prepared: April 1 2026*
*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
