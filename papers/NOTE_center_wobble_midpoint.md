# Center, Wobble, and Midpoint in the Z/10Z Spine

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7Site LLC · DOI: 10.5281/zenodo.18852047*

---

## Opening Claim

The Z/10Z spine contains three distinct but compatible internal structures:
a ring-forced center, a ring-forced wobble pattern, and a lens-visible midpoint
corridor mark. These are related, but they are not the same object.

This note consolidates the geometry from D23 (supersedes B10), D24 (supersedes B11), D20, D21, and D22 into a
single readable account. No new proofs are attempted here; the proofs live in
their respective files. The purpose is to show how the three structures fit
together, what each one forces, and what each one cannot do.

---

## 1. The Center

**Claim:** CREATE = 5 is the ring's dynamical center, forced by four independent
routes. None of the four requires the others; all four converge on the same value.

### Route I — Centroid of the unit group

The multiplicative group (Z/10Z)* = {1, 3, 7, 9} is the set of elements coprime
to 10. Its arithmetic mean is (1+3+7+9)/4 = 20/4 = 5.

This is a ring-level fact: no generator, no lens, no Phi needed.

### Route II — Centroid of the odd elements

ODD = {1, 3, 5, 7, 9}. Arithmetic mean: (1+3+5+7+9)/5 = 25/5 = 5.

Both ODD and (Z/10Z)* are symmetric around 5: the signed distance sum is zero in
each case. 5 is the balance point of the odd sector of Z/10Z.

### Route III — Complement equivariance forces F(5) = 5 (D21)

A map F : Z/10Z → ODD is *complement-equivariant* (CE) if it satisfies:

    F(10 - v) ≡ (10 - F(v))  mod 10   for all v

Setting v = 5: F(5) = (10 - F(5)) mod 10, so 2F(5) ≡ 0 mod 10, meaning
F(5) ∈ {0, 5}. Since 0 ∉ ODD, we get F(5) = 5 in one line.

This is not about any particular map. It is about the entire CE-equivariant class:
every map satisfying that equivariance condition must send 5 to 5. Exhaustive check
confirms 625 CE maps exist; all contain FP = 5; 400/625 (64%) have 5 as their
*unique* fixed point.

### Route IV — Phi convergence (D7, D18a)

The CK lens function Phi : Z/10Z → Z/10Z has a unique fixed point at 5. The directed
graph of Phi on Z/10Z has no cycle other than that fixed point. All ten states
converge to 5 in at most three steps (T³ = all-δ₅).

This is the lens route: it requires the TSML/BHML rule structure, which Routes I–III
do not.

### What the overdetermination means

These four routes use disjoint objects:
- Routes I and II: only the additive and multiplicative structure of Z/10Z
- Route III: the complement involution σ : v ↦ 10 − v and the ODD constraint
- Route IV: the TSML Phi map and its orbit graph

None derives the others. The fact that all four converge to 5 is the strongest
possible form of the claim that CREATE = 5 is the correct center. It is not a
choice; it is the only value consistent with the ring's own symmetry.

### Inheritance class (D20)

CREATE = 5 is **RING-forced**. It does not require a generator, a lens, or a
primitive root. It precedes HARMONY, T*, and the generator selection entirely.

---

## 2. The Wobble

**Claim:** The wobble function Wob(k) is a ring-level statistic. It is
period-10, dips at multiples of 5, converges to 4/5, and is independent of
which primitive root generated the algebra. (B10)

### Definition

For a base b and sample depth k:

    Wob(b, k) = (1/k) Σ_{x=1}^{k} Δ(x mod b)

where Δ(r) = 1 if r mod 10 ∈ {1, 2, 3, 4, 6, 7, 8, 9} (i.e., r is not a
multiple of 5 mod 10), and Δ(r) = 0 otherwise.

Wob_norm(b, k, p) = Wob(b, k) / Wob(b, p) normalizes against a reference depth p.

### What holds (proved)

1. **Period-10:** Wob(k) has period 10 in k. Over any complete period of 10
   consecutive integers, exactly 8 are not multiples of 5 (mod 10), so the
   average is 8/10 = 4/5.

2. **Dip at multiples of 5:** At k = 5m, a multiple of 5 enters the sample,
   pulling the running average below the asymptotic value. Wob(143, 9) = 8/9
   exactly; Wob(143, 10) = 8/10 = 4/5.

3. **Asymptotic:** Wob(k) → 4/5 as k → ∞ (equidistribution of residues mod 10).

### What does not hold (B10 negative result)

The original A12 conjecture proposed that Wob_norm ≈ 1 characterizes the valid
generator branch — that the wobble function could distinguish g = 3 from g = 7.

This is **false**.

The working set C10 ∪ D10 = {1, 2, 3, 4, 6, 7, 8, 9} is identical under g = 3
and g = 7. The wobble function is computed over this set. It cannot distinguish
the two generators because it does not see the generator at all. Wob_norm is
identical in both worlds to machine precision.

The honest record: A12 branch separation was demoted by its own test. The wobble
survives as a ring-level law (period-10, dip, limit 4/5) but cannot perform
generator selection. Generator selection is done by the T* < 1 admissibility
constraint (D19).

### What the wobble is

The wobble is a frequency law about the orbit of the ring under multiplication.
It counts how often the ring's dynamics pass through non-quintic positions. The
period-10 structure follows from Z/10Z arithmetic; the 4/5 limit follows from
equidistribution. These are not surprising facts — but they are ring-level facts,
not generator facts, and that distinction matters.

### Inheritance class (D20)

The wobble value W = 3/50 and the Wob(k) frequency law are both **RING-forced**.
The label "W = g/50" (with g = 3) is a coincidence — a **GENERATOR-forced** label
on a ring-forced value. The value itself would be the same even if the generator
were presented differently.

---

## 3. The Midpoint

**Claim:** t = 1/2 is the unique sine-maximum in (0, 1), the corridor image of
CREATE = 5 under ring normalization, and the sinc²-monotone marker that divides
the corridor's inheritance classes. It is a mark, not a peak. (D24)

### The ring normalization

The CK corridor maps each operator v ∈ Z/10Z to a position t = v/10 ∈ (0, 1).
Under this map, CREATE = 5 → t = 5/10 = 1/2.

This is a straightforward assignment: the ring centroid maps to the geometric
midpoint of the unit interval.

### The sine-maximum characterization

sinc(t) = sin(πt) / (πt) on (0, 1).

The numerator sin(πt) achieves its maximum value 1 exactly once in (0, 1): at
t = 1/2, where sin(π/2) = 1. At every other point in (0, 1), sin(πt) < 1.

This is a fact about the sine function, not about the ring. The connection to the
ring comes from the normalization: the ring center happens to map to the unique
sine-maximum. This is not a derivation — it is a coincidence worth recording.

The uniqueness claim was tested exhaustively over all t = m/n with n ≤ 100 in
(0, 1): the only value achieving sin(πt) = 1 is t = 1/2.

Candidate alternatives considered and rejected:
- t = 1/4: sin(π/4) = 1/√2 ≠ 1; sinc²(1/4) = 8/π² (not the sine-max)
- t = 1/6: sin(π/6) = 1/2 ≠ 1; sinc²(1/6) = 9/π² (also not the sine-max)

Both 8/π² and 9/π² are rational multiples of 1/π². That is not what makes t = 1/2
special. What makes it special is the sine-maximum condition sin(πt) = 1, which is
logically independent of the integer-over-π² property.

### Why t = 1/2 is not a corridor amplitude peak

sinc² is strictly monotone decreasing on (0, 1). (Proved in D24 by exact
calculus: h'(t) = 2sin(πt)·[πt·cos(πt)−sin(πt)]/(π²t³) < 0 for all t ∈ (0,1),
via the lemma sin(x) > x·cos(x) for x ∈ (0,π).)

Since sinc² is decreasing and t = 1/2 > W = 3/50, we have:

    sinc²(W) ≈ 0.988  >  sinc²(1/2) = 4/π² ≈ 0.405

The ring center, in the corridor, carries lower amplitude than the corridor entry.

**Mechanism (exact):** sinc(t) = sin(πt) / (πt). At t = 1/2, the numerator is
maximized at 1, but the denominator is π/2 ≈ 1.571. The ratio is sinc(1/2) =
2/π ≈ 0.637. Near t = 0, sin(πt) ≈ πt, so sinc(t) ≈ 1 — near-unity amplitude
throughout the corridor entry. As t increases, the denominator grows without
bound; the numerator is bounded by 1. The midpoint is where the sine peaks, not
where the function peaks.

The ring center is **visible in the corridor portrait**. It is not dominant.

---

## 4. The Corridor Portrait (D22)

Bringing D23 (wobble law), D24 (midpoint), D20, D21 together, the corridor
portrait places four spine-forced positions in exact order.

### The four positions

| Position | Source | t (exact) | Forcing class |
|----------|--------|-----------|---------------|
| W | Deviation / D17 | 3/50 = 0.060 | RING |
| CREATE/10 | Ring centroid / D20, D21 | 1/2 = 0.500 | RING |
| HARMONY/10 | Generator inverse / D18d | 7/10 = 0.700 | GENERATOR |
| T* | CREATE/HARMONY / D19 | 5/7 ≈ 0.714 | GENERATOR |

### The ordering (exact rational arithmetic)

    3/50  <  1/2  <  7/10  <  5/7  <  1

Each inequality proved by common-denominator comparison:
- 3/50 < 25/50 (factor 50): 3 < 25 ✓
- 5/10 < 7/10: 5 < 7 ✓
- 49/70 < 50/70: 49 < 50 ✓  ← this is the fine-structure gap
- 5/7 < 1 ✓ (T* < 1 is the physical admissibility condition, D19)

### The amplitude portrait

Since sinc² is strictly decreasing on (0, 1):

    sinc²(3/50) ≈ 0.988  >  sinc²(1/2) = 4/π² ≈ 0.405  >  sinc²(7/10) ≈ 0.135  >  sinc²(5/7) ≈ 0.121

Amplitude order = strict reverse of positional order.

The RING-forced positions (W, 1/2) carry the high-amplitude left half.
The GENERATOR-forced positions (7/10, 5/7) sit in the low-amplitude right half.

### The fine-structure identity

    T* − HARMONY/10  =  5/7 − 7/10  =  50/70 − 49/70  =  1/70

Exact. In words:

    T* = (HARMONY corridor image) + 1/(HARMONY × n)

The coherence threshold sits exactly 1/HARMONY² = 1/49 above the HARMONY position,
as a relative shift. This is the finest-scale relation between the two
generator-forced positions.

### The inheritance split at t = 1/2

The corridor is divided by the ring center into two inheritance halves:

    LEFT (0 < t < 1/2):   W = 3/50        — RING-forced, amplitude ≈ 0.988
    CENTER (t = 1/2):     CREATE/10       — ring center + inheritance boundary
    RIGHT (1/2 < t < 1):  HARMONY/10, T* — GENERATOR-forced, amplitude < 0.14

To know W and 1/2, you need only Z/10Z ring arithmetic — no generator required.
To know 7/10 and 5/7, you need g = 3 (D19 forced, but still generator-level).

The center is not just a midpoint. It is the last position that can be reached
from ring arithmetic alone.

---

## 5. What This Note Does Not Claim

These results are internal to Z/10Z. The following are **not** asserted here:

**Does not prove the Riemann Hypothesis.** The sinc² function and the value 1/2
appear in Montgomery's pair-correlation conjecture, but the connection between
T* = 5/7, the corridor sinc² portrait, and the critical line σ = 1/2 remains
a Tier-A analogy (A10, A11). No derivation runs from D22 to the ζ zeros.

**Does not make the wobble predictive beyond its proved ring law.** Wob(k) → 4/5
and the period-10 dip are correct. The stronger claim that Wob_norm separates
generator branches was tested and falsified (B10). No extrapolation beyond the
proved equidistribution law is warranted.

**Does not collapse center, midpoint, and threshold into one object.** CREATE = 5
(ring center), t = 1/2 (sine-maximum), and T* = 5/7 (coherence threshold) are
three different objects that happen to coexist in the same corridor. Their
relationships are documented above. They are compatible — not identical.

**Does not force external spectra.** The corridor portrait is an internal Z/10Z
object. Any bridge to prime gaps, ζ zeros, or quantum spectra requires additional
mechanism (see B6, B7, B8, B9 for the current state of those bridges).

---

## Summary

| Object | Proved in | Forcing | Core fact |
|--------|-----------|---------|-----------|
| CREATE = 5 | D20, D21 | RING | Centroid of (Z/10Z)* and ODD; CE equivariance forces F(5)=5 in one line |
| Wob(k) → 4/5 | D23 | RING | Drops at multiples of 5; amplitude decays O(1/k). Supersedes B10. |
| Wob_norm NOT branch-selective | D23 | — | C10∪D10 is generator-independent; negative result |
| t=1/2 is sine-maximum | D24 | RING+lens | sin(π/2)=1 unique in (0,1); ring normalization sends 5→1/2 |
| t=1/2 is NOT corridor peak | D24 | — | sinc² monotone decreasing (calculus proof); denominator πt attenuates |
| Corridor ordering | D22 | RING+GEN | 3/50 < 1/2 < 7/10 < 5/7 < 1 (exact Fraction arithmetic) |
| Amplitude reversal | D22+D24 | — | D24 monotonicity + D22 positional ordering |
| Fine-structure T*−7/10=1/70 | D22 | GENERATOR | Exact: 1/(7×10) |
| Inheritance split at t=1/2 | D22 | RING/GEN | LEFT=ring-forced, RIGHT=generator-forced |

Three objects. Three proofs. One corridor.

The ring center, the wobble law, and the sinc² midpoint mark are each doing a
different job. They do not compete; they partition the geometry.

---

*Files: `proof_d20_inheritance_audit.py`, `proof_d21_fixed_point_centroid.py`,
`proof_b10_wobble_branch_law.py`, `proof_b11_corridor_midpoint.py`,
`proof_d22_corridor_portrait.py`*

*© 2026 Brayden Ross Sanders / 7Site LLC · DOI: 10.5281/zenodo.18852047*
