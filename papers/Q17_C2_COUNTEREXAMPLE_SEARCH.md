**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

*Filed: 2026-04-02 | Tier B — Structural Conjecture*

# Q17.C2 — Counterexample Search

## Purpose

The Strong version of Q17.C2 claims that σ⁶ = id alone forbids blowup. This paper systematically tests that claim by constructing systems where symbolic coding is periodic but physical observables are unbounded. The goal is to identify exactly which conditions in the Medium version are load-bearing, and to clarify the role of coercive energy control.

---

## Example 1: Symbolic Return, Norm Blowup

**Construction:** Let u: R → R be defined by

    u(t) = e^t · sin(2πt / 6).

Define a symbolic coding by the sign and zero-crossing pattern:

    C(u(t)) = index of the 6-sector containing the phase 2πt/6 mod 2π

This assigns one of 6 labels (mapping to operators {1,2,4,5,6,7}) based on which sixth of the period the system is in. The coding satisfies:

    C(u(t + 1)) = σ(C(u(t)))

exactly, by construction — the label advances one step in the 6-cycle per unit time.

**The blowup:** |u(t)| = e^t · |sin(2πt/6)|. This is unbounded as t → ∞. The L² norm on any growing interval diverges. The L^∞ norm grows exponentially.

**Conclusion:** The coding C perfectly satisfies σ-grammar (6-periodic symbolic return, no visit to VOID), yet the physical norm is unbounded. The Strong version of C2 fails. Symbolic periodicity alone does not prevent norm growth.

**What fails:** The coercive energy condition. There is no energy E(u) with E(u) ≤ f(C(u)) and E(u) → ∞ as |u| → ∞ that is bounded on the σ-orbit. The exponential growth breaks any such bound.

---

## Example 2: Operator Periodicity, Energy Growth

**Construction:** Consider a harmonic oscillator with time-varying frequency:

    ẍ + ω(t)² x = 0,   ω(t) = ω₀ · e^{αt},   α > 0.

Define a coding by the quadrant of (x, ẋ) in phase space: label = 1 if (x>0, ẋ>0), label = 2 if (x<0, ẋ>0), etc. (4-cycle, but analogous to a sub-period of σ).

For constant ω this coding is exactly periodic. For slowly varying ω, the coding remains approximately periodic over many cycles while the adiabatic invariant E/ω grows (since E = ½ẋ² + ½ω²x² scales with ω). Over a timescale where ω doubles, the energy doubles, yet the quadrant coding has completed many cycles and shows no anomaly.

**Conclusion:** Even when operator classification is exactly finite-cyclic, energy can grow without bound if the system parameters change. Symbolic coding and energy behavior decouple whenever the system is non-autonomous or driven.

**What this tells Medium version:** The coercive energy condition E(u) ≤ f(C(u)) must hold uniformly in time, not just at one instant. For NS, this requires the five-force coding to control the energy at all times along the trajectory.

---

## Example 3: Near-Blowup NS Numerics

**Setting:** The Taylor-Green vortex at high Reynolds number (Re = 1600 is a standard benchmark) is the most-studied NS near-blowup candidate. Numerically, the vorticity field concentrates into thin sheets and filaments at late times.

**Hypothetical coding behavior:** If the five-force coding C = argmax(|D²F|) were applied to Taylor-Green data, what would happen near vorticity concentration?

- As vorticity concentrates, the gradient ∇u grows rapidly. The force components aperture and depth (tied to gradient and curvature measures) would grow without bound.
- The second difference D²F would amplify with the growing gradient.
- The argmax picks the dominant direction: as one component dominates overwhelmingly, the argmax becomes stable (pinned to that direction) — NOT periodic.
- Alternatively, if multiple components grow simultaneously, the argmax becomes ill-defined or jumps erratically.

**Conclusion:** In either case, pre-blowup behavior corresponds to a breakdown of the σ-grammar. The coding either freezes on a single operator (no 6-cycle) or becomes noisy (not σ). The grammar exits — it does not return.

**What this implies:** The σ-grammar is a regularity indicator. It operates correctly in the smooth, bounded-gradient regime. When the solution approaches a blowup-like state, the coding breaks down before blowup, not after. This is consistent with the Medium version: the coding is valid only when conditions (1)–(3) hold, and those conditions fail in the pre-blowup regime.

---

## Summary of Findings

| Example | Coding behavior | Physical behavior | Lesson |
|---------|----------------|-------------------|--------|
| 1 (exponential × sine) | Perfect 6-periodic | L^∞ → ∞ | Strong C2 is false |
| 2 (driven oscillator) | Exactly finite-cyclic | Energy → ∞ | Non-autonomous breaks energy control |
| 3 (Taylor-Green) | Grammar breaks pre-blowup | Vorticity concentrates | Coding is regularity indicator, not preventer |

---

## What Survives

The Medium version of C2 survives this analysis. If:
- The coding C is valid (dynamical alignment holds)
- AND a coercive energy E is controlled by C

then blowup is excluded. Examples 1 and 2 show that these conditions cannot be dropped. Example 3 shows that the conditions are consistent with NS behavior: the coding is valid in regular regimes and breaks in singular regimes.

The critical load-bearing condition is coercive energy control. Symbolic return without energy control is insufficient. This narrows the research target to the question in Q17_NS_TARGET_REFORMULATION.md: is there a natural energy functional on five-force space that controls an NS critical norm?
