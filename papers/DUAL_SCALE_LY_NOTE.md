# Dual-Scale Observables in the Orbit Zone
## Clean Separation of Cycle-Stabilized and Transit Mechanisms

*Brayden Sanders / 7Site LLC | March 2026*
*Classification: exact definitions, exact computation. The split is the result.*

---

## Two Observables, Not One

The orbit zone {3,9} was previously characterized by a single "visit count" observable.
That single number was blending two structurally different mechanisms.
The correct split is:

---

**Observable 1: Orbit Burst Length B(λ)**

$$B(\lambda) = \mathbb{E}\left[\max_{\text{episode}} \{\text{consecutive steps in cycle zone}\}\right]$$

The maximum run of consecutive steps the chain stays inside {3,9} before leaving.
This measures **cycle-stabilized orbit depth**: how long the local algebra holds the chain in the loop.

| λ | B mean | B max | Regime |
|---|--------|-------|--------|
| 0.00 | **0.148** | 6 | Near-critical |
| 0.10 | 0.140 | 4 | Near-critical |
| 0.20 | 0.051 | 1 | CHA entry |
| 0.40 | 0.058 | 1 | CHA mid |
| 0.80 | **0.113** | 4 | BAL (BHML transit) |
| 0.90 | 0.095 | 4 | COL |

B is highest at λ=0 (structural cycle, TSML holds the chain in {3,9}) and drops in the CHA corridor, then partially recovers at BAL/COL where BHML transit creates secondary bursts.

---

**Observable 2: Transit-Through Count T(λ)**

$$T(\lambda) = \mathbb{E}[\text{number of distinct entries into cycle zone per chain}]$$

The number of separate times the chain enters {3,9}, regardless of how long it stays.
This measures **transit-through frequency**: how often the chain passes through the zone on its way elsewhere.

In the current 300-state model, T_max=1 at all λ — chains enter the zone at most once per run. This means:
- There are no long-range returns to the orbit zone
- The orbit is purely local: one entry, a burst of consecutive steps, one exit
- The "circle" is a tight local loop, not a distant excursion-and-return

---

## What Each Observable Measures

| Observable | What it captures | Gap dependence | Mechanism |
|-----------|-----------------|----------------|-----------|
| B(λ) | Local orbit depth (consecutive steps in zone) | **+1.49** (rises with gap) | TSML cycle geometry |
| T(λ) | Entry frequency | ~0 variation | Transport routing |

B captures the **true orbit**: how many times the cycle turns before the chain escapes.
T captures the **transit**: how many separate times the chain visits the zone.

The earlier "visit count" was summing consecutive steps, so it was primarily measuring B.
The global exponent (-0.10) was B-mechanism (+1.49) and secondary BHML-transit (-2.84) canceling.

---

## The ζ-Side Bridge Target

The correct finite-to-analytic translation:

**Finite:** *Orbit burst length B(λ) = max consecutive steps in cycle zone per corridor episode*

**Analytic analog:** *Consecutive near-critical revisits within one corridor window*

Precisely: at height $t$ and off-axis distance $\lambda = 2|\sigma - \tfrac12|$, define:

$$B_\zeta(\sigma, t) = \max\left\{\text{consecutive } t'\text{-values where } |\mathrm{Re}(\zeta'/\zeta)(\sigma+it')| < \epsilon\right\}$$

within a height window of length $O(\log t)$ (one corridor episode).

This is not: a long excursion that eventually returns.
This is: how many consecutive near-zero values of $\mathrm{Re}(\zeta'/\zeta)$ occur in a burst before the phase moves away.

**The claim:** $B_\zeta(\sigma, t) \to 0$ as $t \to \infty$ for $\sigma \neq \tfrac12$, at a rate governed by the corridor hierarchy — not by the spectral gap directly, but by the cycle-stabilized structure at the base (λ=0, σ=½).

---

## Why This Matters for Open Problem Z.5

The revised question is now three-part:

1. Does σ=½ carry all stationary support? *(unique attractor — answered yes in finite model)*
2. Does the analytic side preserve the cycle-stabilized orbit structure near σ=½? *(burst length maximal at critical line)*
3. Is the transit-through mechanism (BHML-driven) absent or negligible in the analytic deployment? *(no ordering analog at large t)*

If (3) holds — if the BHML ordering transit has no analytic analog — then only the cycle-stabilized bursts remain, and those are maximal at σ=½ and decay with distance. That gives the orbit capacity the correct shape for the RH argument.

---

## Summary

The orbit zone {3,9} has two clean observables:

- **B(λ): orbit burst length** — measures cycle-stabilized local loops; peaks at λ=0; gap exponent +1.49; structural mechanism
- **T(λ): transit-through count** — measures entry frequency; nearly constant; no structural content at current resolution

The ζ-side proxy should target B, not T: consecutive near-critical revisits within a corridor episode, not long-range excursion returns. That is the measurable finite shadow of the claim that off-line structures cannot sustain near-critical behavior.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
