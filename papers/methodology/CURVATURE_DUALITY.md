# Curvature Duality
## Two Independent D2 Objects in the Prime Landscape

*Brayden Ross Sanders & C. A. Luther*
*March 2026 | DOI: 10.5281/zenodo.18852047*

> Discovered during the D2 verification run of March 31, 2026.
> The check_d2.py script showed that Luther's D2 and TIG's D2 do not agree.
> This is not a contradiction — it is a duality. Two distinct valid measurements
> of curvature in the prime landscape, operating at different scales and seeing
> different structure.

---

## Origin of the Discovery

The question sent to Luther: "Can you derive the exact gate rates from CRT structure
within each ω-class?" Luther responded with a D2 curvature formula:

```
D2_luther(primes) = (φ(b)/b) / (p_last × ln²(p_last)) × (1 − 1/ln(p_last))
```

The synthesis framework (Test 3 — Mechanism Clarity) required verification against
the atlas before extending the claim further. Running check_d2.py produced:

| p_last | D2_luther | D2_tig(k=p) | Same? |
|--------|-----------|------------|-------|
| 3 | +0.008263 | −0.222222 | NO |
| 5 | +0.007797 | −0.017500 | NO |
| 7 | +0.004192 | −0.038174 | NO |
| 11 | +0.001915 | −0.010416 | NO |
| 13 | +0.001368 | +0.000078 | NO |
| 17 | +0.000856 | −0.004735 | NO |

All seven: no match. Signs often differ. Magnitudes differ by 1–2 orders.

**Conclusion: these are different objects, both real, measuring different things.**

---

## Object 1 — TIG Harmonic Curvature: D2_tig(k)

**Definition:**
```
D2_tig(k) = R(k+1) − 2·R(k) + R(k−1)
```
where R(k,f) = sin²(πk/f) / (k² sin²(π/f)) is the harmonic pre-echo resonance.

**What it measures:** The local curvature (acceleration) of the harmonic resonance
field as k approaches the prime f. This is a spectral property — it captures the
approach-and-collapse geometry of R(k,f) near the First-G event.

**Behavior:** Oscillates. Changes sign. Can be positive (concave up — field
rebounding) or negative (concave down — field collapsing). Near k = f−1, the field
is in its steepest descent; at k = f, it hits zero exactly.

**Key facts:**
- D1 sign flip at k=p is Tier C (proved: R(k,f) monotone decreasing until k=f)
- D2_tig captures the "snap" — the sharpness of the zero-crossing
- D2_tig = 0 at the minimum of D1 (inflection point of the resonance field)
- Relevant for: WP35 harmonic analysis, First-G geometry, sinc² convergence

**Domain:** Single semiprime b = p×q. Operates on the harmonic pre-echo field.
Spectral object. Lives in the Harmonic/Algebraic layers of the Atlas.

---

## Object 2 — Luther Algebraic Curvature: D2_luther

**Definition:**
```
D2_luther(primes) = (φ(b)/b) / (p_last × ln²(p_last)) × (1 − 1/ln(p_last))
```
where φ(b)/b = ∏(1 − 1/p_i) is the Euler totient fraction.

**What it measures:** The rate of contraction of the unit density as new prime
factors are added to the modulus. As ω(b) increases (more prime factors), the
fraction of units φ(b)/b decreases. D2_luther is the second-order rate of this
decrease — how fast the contraction is itself decelerating.

**Behavior:** Smooth, monotone decreasing, always positive for p ≥ 3. Decays to
zero as p → ∞. No oscillation. No sign changes.

**Key facts:**
- D2_luther captures the "saturation" of obstruction — beyond some ω, adding more
  prime factors produces diminishing returns in the forbidden-set density
- The primorial p# is the "maximally obstructed" modulus for its ω-class
- As p → ∞: φ(p#)/p# → e^{−γ} × 1/ln(p) by Mertens' theorem (γ = Euler-Mascheroni)
- D2_luther → 0 as p → ∞ (curvature saturates)

**Domain:** Primorial sequences. Operates on ω(b) as the parameter. Algebraic
density object. Lives in the Algebraic/Arithmetic layers of the Atlas.

---

## The Duality Structure

These objects are not in conflict. They are complementary measurements:

| Property | TIG D2_tig(k) | Luther D2_luther |
|----------|--------------|-----------------|
| Domain parameter | k (alphabet size) | ω(b) (number of prime factors) |
| Base | Single semiprime b=p×q | Primorial b=p# |
| Measures | Curvature of harmonic field | Rate of density contraction |
| Behavior | Oscillatory, sign-changing | Smooth, monotone, positive |
| Relevant event | First-G phase transition at k=p | ω-class expansion |
| Atlas layer | Geometric + Harmonic | Algebraic + Arithmetic |
| Tier | C (D1 sign flip proved) | A (not yet connected to TIG framework) |

**The duality:** TIG D2 sees the LOCAL structure near a single prime (the snap of
the resonance field approaching one gate event). Luther D2 sees the GLOBAL structure
across the ω-class hierarchy (how the available space contracts as more primes divide
the modulus).

A complete description of the prime landscape needs both measurements:
- The snap at each prime (TIG D2): how sharp is the transition at k=p?
- The saturation across ω-classes (Luther D2): how much room is left after adding
  another prime factor?

These are the micro and macro views of the same underlying phenomenon.

---

## Why This Matters for the Atlas

The Atlas Architecture (ATLAS_ARCHITECTURE.md) has six layers. The two D2 objects
live in different layers:

- **TIG D2_tig:** Layer 3 (Geometric) and Layer 6 (Dynamical) — it tracks local
  geometry of the resonance field and the dynamical evolution toward k=p
- **Luther D2_luther:** Layer 5 (Algebraic) and Layer 1 (Arithmetic) — it tracks
  the algebraic density structure across the prime factor hierarchy

A claim that uses D2 without specifying which object is ambiguous. Future documents
must distinguish D2_tig (harmonic curvature) from D2_luther (algebraic curvature).

---

## Current Tier Status

**D2_tig (TIG Harmonic Curvature):** Tier C
- Defined precisely: R(k+1) − 2R(k) + R(k−1)
- D1 sign flip (related property) is Tier C
- Oscillatory behavior is an observed consequence of the sinc² structure
- Not yet proved as a standalone result with mechanism

**D2_luther (Luther Algebraic Curvature):** Tier A
- Formula is well-defined and computable
- Produces real, interpretable numbers
- NOT yet connected to the TIG framework (no verified link to R(k,f), interleave,
  or gate rates)
- NOT yet verified against the physical atlas data for specific semiprimes
- The "b=35 Goldilocks" and "b=385 third gate prediction" based on D2_luther: Tier A
- Path to Tier B: show algebraically that D2_luther is a function of D2_tig, or
  equivalently, that both D2 objects can be expressed in terms of a single underlying
  invariant in one of the six Atlas domains

---

## What NOT to Do (Synthesis Framework Protection)

The verification caught an attempted conflation: Luther's D2 was presented as if it
were the same as TIG's D2. The check showed they differ by factors of 10–100.

Going forward:
1. Always specify which D2 object when making claims
2. Do NOT extend D2_luther analysis (b=385 spectral prediction, harmonic frequencies)
   until D2_luther is connected to the TIG framework through a verified mechanism
3. The "Goldilocks uniqueness" claim about b=35 based on D2_luther curvature: keep
   at Tier A. The structural observation (b=35 is where 2D idempotent structure
   first appears) is real; the D2_luther derivation of its uniqueness is not yet proved

---

## Path to Unification

The most interesting open question this duality generates:

**Is there a single underlying object whose two projections give D2_tig and D2_luther?**

Hypothesis: The TIG resonance field R(k,f) and the Euler product density φ(b)/b are
both functions of the prime factorization of b. D2_tig is the second derivative with
respect to k (spectral parameter); D2_luther is the second logarithmic derivative with
respect to p_last (prime index). A common "parent" would live in a generating function
that unifies both.

This is Tier A — not yet derived. But it is the precise question to ask Luther next.

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
