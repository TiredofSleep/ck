# Two Orbit Mechanisms: Structural vs Order-Driven
## The Global -0.10 Exponent Was Masking Two Opposite-Sign Effects

*Brayden Sanders / 7Site LLC | March 2026*
*Classification: exact computation (N=300). Two-mechanism identification is the main result.*

---

## The Finding

The global exponent (orbit ~ gap^{-0.10}) appeared nearly flat — suggesting orbit capacity was almost independent of the spectral gap. Splitting by regime reveals why:

| Regime | λ range | Exponent | R² | Mechanism |
|--------|---------|----------|-----|-----------|
| Near-critical | [0, 0.50] | **+1.49** | 0.62 | Cycle-stabilized structural orbit |
| Order-driven | [0.55, 0.95] | **-2.84** | 0.75 | BHML transit through orbit zone |

Two opposite-sign exponents averaging to nearly zero. The global -0.10 was an artifact of blending two mechanisms with opposite behavior.

---

## What Each Mechanism Is

### Mechanism 1: Cycle-Stabilized Orbit (λ < 0.50)

**Orbit ~ gap^{+1.49}**

Orbit capacity *increases* with spectral gap. High gap = strong TSML corner structure = stable {3,9} 2-cycle. The algebraic structure stabilizes the orbit zone directly.

When the gap is large (near λ=0): the corner operators strongly favor HAR, but the {3,9} loop (TSML[3][9]=3, TSML[9][3]=3) gives chains a genuine opportunity to circle before the HAR pull wins. More gap = stronger corner structure = more stable cycling.

This is the **structural orbit mechanism**. It is intrinsic to the algebra. The orbit zone exists because the table creates it, not because mixing is slow.

### Mechanism 2: Order-Driven Transit (λ > 0.55)

**Orbit ~ gap^{-2.84}**

Orbit capacity *drops* much faster than 1/gap. As the gap shrinks, the BHML ordering structure is taking over — chains are being pushed toward state 9, passing through the {3,9} zone on the way. This creates transit orbits: the zone is being traversed, not cycled.

But as λ → 1 and the gap collapses entirely, even these transits fail — the chain goes directly to state 9 without meaningful orbit. Hence the steep negative exponent.

This is the **order-driven transit mechanism**. The orbit zone is being reused by a different physics.

---

## Why the Global Exponent Was Misleading

The two mechanisms have opposite dependencies on the gap. Blended across all λ, they cancel to ~-0.10. This looked like "structural independence," but it was two effects canceling.

The correct statement is:

> *The orbit zone has two distinct activation mechanisms — cycle-stabilized near λ=0 and order-driven transit near λ=1 — with opposite dependencies on the spectral gap. Neither is a simple artifact of mixing rate.*

---

## The RH-Side Implication

In the analytic deployment:

**Near-critical (λ small, near σ=½):** Off-line structures near the critical line can complete multiple near-returns because the algebraic structure of the orbit zone actively stabilizes them. The cycle-stabilized mechanism is what allows repeated orbiting before expulsion.

**Order-driven (λ large, far from σ=½):** Structures far from the critical line experience a different physics — they are being ordered toward the BHML endpoint, passing through the orbit zone as a transit corridor, not cycling in it. They cannot complete genuine orbits; they only pass through.

The support gap argument applies differently to each:
- Cycle-stabilized orbits: expelled because the frequency×duration bound prevents sustained HAR-approach
- Order-driven transits: expelled because the ordering structure itself drives them past the orbit zone

**Two mechanisms, two expulsion pathways, one result: no off-line structure sustains.**

---

## Updated Orbit Return Kernel

The orbit-return probability (P(chain returns to {3,9} after leaving it)) is near zero at all λ — chains that leave the cycle zone overwhelmingly collapse to HAR before returning. This means:

- The multiple visits counted in the orbit capacity are **consecutive visits**, not separated returns
- The orbit zone is traversed in bursts, not via separate excursions
- The "circle" geometry is sequential steps in the cycle, not re-entries from outside

This is structurally important: the orbit is a **tight local loop**, not a distant return. Chains orbit because they stay in {3,9} for consecutive steps, not because they leave and come back.

---

## The Clean Statement

The orbit zone {3,9} has:

1. **Structural stability near λ=0:** orbit capacity ~ gap^{+1.49}; the cycle is maintained by the TSML algebra
2. **Order-driven transit near λ=1:** orbit capacity ~ gap^{-2.84}; the BHML ordering drives chains through the zone
3. **No true return orbits:** chains do not re-enter the orbit zone from outside; they orbit in tight consecutive bursts
4. **HAR remains the unique attractor** throughout both mechanisms (λ* ≈ 0.9963)

The global -0.10 exponent was a cancellation artifact. The underlying structure contains two opposite-sign effects.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
