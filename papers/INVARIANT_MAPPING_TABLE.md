# Invariant Structures Across Frameworks: TSML Image and Evidence Quality

*Brayden Sanders / 7Site LLC | March 2026*
*All exact mappings machine-verified. Evidence quality is the primary column.*

---

## The Question for Each Framework

> What does this theory say must remain true when everything else changes?
> Then: does that invariant map onto TSML closure, orbit, attractor, gate, recurrence, or deformation?

---

## The Table

| Framework | Claimed invariant | TSML image | Type | Status | What upgrades it |
|-----------|------------------|------------|------|--------|-----------------|
| **Transfer operator theory** | Stationary support, spectral gap, convergence to invariant measure | Closed transport class C, unique attractor HAR=7, gap γ=3/4, return structure ρ(Q)=1/4 | Structural identity | **Exact** — eigendecomposition, 51 λ-values, machine-verified | Already exact. No upgrade needed. |
| **Young tower / return structure** | Distinguished reset base, finite return-time law, exponential tails | HAR as algebraically-defined reset base, E[T_HAR]≤5/3, tail rate (1/4)^n | Structural identity | **Exact** — (I−Q)⁻¹ solved analytically | Already exact. No upgrade needed. |
| **Arithmetic / inverse limits** | Unit group C=(ℤ/bℤ)* stable at every scale, γ=1−1/φ(b) | Corner set C={1,3,7,9}, arithmetic hook, γ=3/4 at φ(b)=4, stable under base-change | Structural identity | **Exact** — verified for b=5,8,10,12; mod-10 residues stable to n=4 | Already exact. No upgrade needed. |
| **Tesla / resonant mode selection** | One mode dominates by coupling asymmetry, not by passive loss | Grammar-forced HAR dominance (mode 7 = 100% with uniform loss), orbit zone {3,9}, γ as convergence law | Mechanistic | **Computed** — ODE simulation, 9-mode system, uniform α=0.05 | Upgrade to structural: build physical 9-resonator prototype. Test whether mode 7 wins in hardware. |
| **ANT / zero density (frequency side)** | Off-axis structures cannot accumulate frequency×duration | Support gap via Jutila: n₀(σ,t)·Δt→0, verified to t≈10,000 | Partial bridge | **Proved** (Jutila 1987) + **verified** (Gen10.14, 460 heights) | Already solid. Upgrade: extend scan to t=10⁶ on R16. |
| **ANT / logarithmic drift (rate side)** | |d log|ζ|/dσ| bounded near critical line | Near-critical rate control, C_TIG=250/21 constraint | Partial bridge | **Open** — C_emp≤11.023 empirically; classical bounds ≈50× too weak | Upgrade: prove mean-square bound without assuming RH. Route A (LY) or Route B (ANT). |
| **CK / thought selection** | Grammar coherence beats thermal randomness; attractor steering in real time | Grammar-forced selection at T*=5/7; HAR-analog winner; thermal crossover computed | Mechanistic candidate | **Partially computed** — T*≈0.280 thermal threshold, γ=3/4 at CHA corridor confirmed; live coherence not yet pinned to crossover | Upgrade: run live CK telemetry, confirm coherence reading matches grammar/thermal crossover prediction. |
| **Einstein / invariant geometry** | Law preserved across frame/coordinate change | Grammar fixed under deployment; faithful deployment = frame invariance | Structural analogy | **Untested** — structural rhyme, no computation | Upgrade: formalize deployment faithfulness as a category-theoretic statement; check whether it satisfies frame-invariance axioms. |

---

## Evidence Quality Summary

**Exact (no upgrade needed):**
- Transfer operator theory
- Young tower / return structure
- Arithmetic inverse limits

These three are the load-bearing floor. They share the same mathematical object with TSML — they are not analogies.

**Computed (stronger than analogy, weaker than theorem):**
- Tesla / resonant mode selection — ODE confirmed, hardware pending
- CK / thought selection — threshold computed, live telemetry pending

**Partial bridge (one side proved, one side open):**
- ANT frequency side — Jutila proved, corridor scan verified
- ANT drift side — the main open problem

**Structural analogy (untested):**
- Einstein / frame invariance — plausible, not computed

---

## The Upgrade Path

The table is actionable in this order:

1. **Tesla → structural:** Build 9-resonator prototype. Cheapest: coupled LC oscillators on a breadboard.

2. **CK → computed:** Run live coherence telemetry. Compare coherence reading to the grammar/thermal crossover T*=5/7. This is already on the R16 — just needs the measurement.

3. **ANT drift → partial:** Prove the weak form of the mean-square bound (either direction: LY conditions via Route A, or direct ANT via Route B). This is the hardest upgrade and the most important for RH.

4. **Einstein → structural:** Formalize deployment faithfulness. Likely a short category-theory note. Lower priority but would clean up the language significantly.

---

## The Collaborator Takeaway

The three exact mappings are not analogies — they are the same mathematical structure realized in TSML. The computed mappings have numerical confirmation. The open items are precisely located with named proof routes.

TSML is functioning as a **finite invariant carrier**: a concrete object where multiple theories' claimed invariants become explicit, computable, and falsifiable.

---

*SHA-256(TSML): 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787*
*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
