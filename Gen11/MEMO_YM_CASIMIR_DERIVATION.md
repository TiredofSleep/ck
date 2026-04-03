# YM Bridge F3: Formal Casimir Derivation Analysis
## Where Does N/(N+2) Come From?
*Author: Brayden Ross Sanders / 7Site LLC — 2026-04-02*

---

## The Claim

Bridge F3 conjecture: m(0⁺⁺)/m(2⁺⁺) = N/(N+2) for SU(N) pure YM theory.
At N = CREATE = 5: N/(N+2) = 5/7 = T*.

This memo analyses the THREE derivations of this formula and identifies
where each is rigorous vs. heuristic.

---

## Derivation 1: Z/10Z Ring Arithmetic (PROVED)

In Z/10Z:
- CREATE = 5 is the multiplicative identity on Z/5Z (the ether)
- HARMONY = 7 is the first temporal operator (CREATE + 2 = 7)
- T* = CREATE/HARMONY = 5/7 (proved in Gen11, Tier D)

**This proves T* = 5/7. It does NOT prove m(0⁺⁺)/m(2⁺⁺) = T* for any gauge theory.**
The ring arithmetic shows T* is the forced coherence threshold; whether gauge theory
realizes this threshold in glueball masses is the bridge conjecture.

---

## Derivation 2: Regge String + Shell Wobble (DERIVED — see Part XIII)

Regge string (large N string theory):
```
M²(J++) = πσ(2+J)
```
Gives m(0⁺⁺)/m(2⁺⁺) = sqrt(2/4) = 1/sqrt(2) = 0.7071 (1.015% below T*)

Shell wobble correction (ether-square quantum ε = πσ/CREATE²):
```
M²_eff(J++) = πσ[(2+J) - J/CREATE²]
```
At J=2: M²_eff(2⁺⁺) = πσ · 98/25

Result:
```
m(0⁺⁺)/m(2⁺⁺) = sqrt(2πσ / (πσ · 98/25)) = sqrt(50/98) = sqrt(25/49) = 5/7 = T*
```

**Status:** The Regge string picture is large-N string theory (N→∞ 't Hooft limit).
The wobble quantum ε = πσ/CREATE² is inserted as a hypothesis: the spin-J glueball
has a transverse wobble that reduces M²(J++) by J×ε.

**Gap:** The wobble quantum ε = πσ/25 is not derived from SU(5) gauge theory or from
any established string theory calculation. It is the TIG ether-square quantum transplanted
into the string theory picture. The derivation shows that IF the wobble quantum has this
value, THEN m(0⁺⁺)/m(2⁺⁺) = T* exactly. The "if" is not proved.

---

## Derivation 3: Casimir Scaling (HEURISTIC)

### Standard Casimir Scaling (Established)

For static quark-antiquark pairs in representation R, the string tension satisfies:
```
σ_R = (C₂(R)/C₂(adj)) × σ_adj
```
where C₂(R) is the quadratic Casimir and C₂(adj) = N for SU(N).

This is Casimir scaling, which has been verified on the lattice for Wilson loops.

### Glueball Casimir (Heuristic)

For glueballs (color-singlet objects made of adjoint gluons), all constituents are
in the adjoint representation. The color string tension is σ_adj = σ for all glueballs.

The HEURISTIC ANSATZ: glueball masses scale with a "combined Casimir" that mixes
the color Casimir C₂(color) = N and the angular momentum J:

```
C₂(J; N) = N + J    (combined Casimir, TIG ansatz)
```

For J=0 (0⁺⁺): C₂(0; N) = N = CREATE
For J=2 (2⁺⁺): C₂(2; N) = N+2 = HARMONY (at N=5)

If M(J⁺⁺) ∝ C₂(J; N) (linear in combined Casimir):
```
m(0⁺⁺)/m(2⁺⁺) = N/(N+2) = T*   (at N=5)
```

**Where N+2 appears in standard representation theory:**

The NEXT irrep above the adjoint in SU(N) is the symmetric traceless rank-2 tensor
(the "spin-2 generalization" of the adjoint). Its Casimir in SU(N) is:
```
C₂(sym⊗adj) = N + 2 - 2/N ≈ N + 2   (for N >> 1)
```

At N=5: C₂ = 5 + 2 - 2/5 = 6.6 (not exactly 7).
At N=∞: C₂ → N+2 exactly.

**The N+2 formula is exact only in the large-N limit, where the 2/N correction vanishes.**

### Why the Linear Casimir (Not Square-Root)?

For the formula m ∝ C₂(J;N) to give the RIGHT ratio (not m ∝ C₂^½), we need
glueball masses to scale LINEARLY with the effective Casimir. This would arise if:

1. **Holographic (AdS/CFT):** In AdS₅, the spin-J Kaluza-Klein mass goes as
   M ∝ Δ(J) where Δ is the conformal dimension. For protected operators:
   Δ(J=0) = 4, Δ(J=2) = 4 + 2J/N × Δ_correction... (approximate).
   This doesn't cleanly give N/(N+2).

2. **Flux tube model:** If the glueball is a closed flux tube with tension σ × C₂(J;N),
   then M_flux ~ σ × C₂(J;N) × (radius), and for fixed radius: M ∝ C₂(J;N) linearly.
   This would require the glueball radius to be J-independent.

3. **Constituent gluon model:** Each gluon contributes C₂(adj)/2 = N/2 to the mass.
   An additional spin-J contribution of J to the effective Casimir (from angular momentum
   coupling to the color charge) gives C₂(J;N) = N + J linearly.

**The linear scaling is the key unproved step.** If M ∝ C₂(J;N)^½ instead:
```
m(0⁺⁺)/m(2⁺⁺) = sqrt(N/(N+2)) = sqrt(5/7) = 0.845 ≠ T*
```
This doesn't match T*. So the derivation requires linear (not square-root) scaling.

---

## Summary of Derivation Status

| Derivation | Status | Gap |
|------------|--------|-----|
| Z/10Z ring: T*=5/7 | **PROVED** | Doesn't touch gauge theory masses |
| Regge + wobble: m ratio = T* | **Derived** | Wobble quantum ε=πσ/25 not derived from gauge theory |
| Casimir scaling: N/(N+2)→T* | **Heuristic** | Linear Casimir ∝ M (not M²) unproved; N+2 exact only at N=∞ |

---

## The Gap to Close for F3

To formally close Bridge F3 at the level of a Clay Prize argument, one of:

**Path A (Casimir):** Prove that in SU(N) pure YM, glueball masses scale linearly
with the combined Casimir C₂(J;N) = N + J in the confining regime. This would require
either:
- A rigorous holographic derivation (needs N large, approximation)
- A lattice theorem (statistical, not a proof)
- A QCD string theory derivation (Regge slopes with Casimir input)

**Path B (Wobble):** Derive the wobble quantum ε = πσ/CREATE² from SU(5) gauge theory.
Show that the transverse fluctuation of a spin-2 glueball in confining SU(5) reduces M²
by exactly 2πσ/25. This is a string theory calculation on the confining string.
- The 1/25 = 1/CREATE² would arise from the SU(5) structure constants.
- The J-proportionality (wobble scales with J) would arise from the D-wave angular momentum.

**Path C (Lattice):** The lattice data for SU(N) shows:
- SU(2): m(0⁺⁺)/m(2⁺⁺) = 0.686 vs N/(N+2) = 0.500 (LARGE discrepancy)
- SU(3): m(0⁺⁺)/m(2⁺⁺) = 0.722 vs N/(N+2) = 0.600 (large discrepancy)
- SU(5): m(0⁺⁺)/m(2⁺⁺) = 0.716 vs N/(N+2) = **0.714 = T*** (near-exact match)
- SU(∞): m(0⁺⁺)/m(2⁺⁺) = 0.717 vs N/(N+2) = 1.000 (wrong direction)

The formula N/(N+2) is a GOOD fit only at N=5. At other N it fails. This means the
formula is NOT a universal law of SU(N) glueball physics — it's a special coincidence
at N = CREATE = 5 (or needs a different functional form).

**This is the critical observation:** N/(N+2) fits SU(5) data but NOT SU(2), SU(3), or SU(∞).
A universal physical law must hold for all N. The special match at N=5 is either:
- A coincidence (the true ratio happens to equal T* at N=5 for other reasons)
- Evidence that SU(5) is the special gauge group where Z/10Z physics is physical

---

## The True YM Bridge Statement

Given the above analysis, the honest Bridge F3 statement is:

**Empirical:** m(0⁺⁺)/m(2⁺⁺) ≈ T* = 5/7 for SU(5) pure YM (lattice data, ~0.1% accuracy).

**Three independent TIG predictions of this ratio:**
1. Z/10Z: T* = CREATE/HARMONY = 5/7 (proved)
2. Regge + wobble: sqrt(25/49) = T* (derived, with wobble quantum hypothesis)
3. Combined Casimir at N=5: 5/7 = T* (heuristic, exact at N=5 only)

**Bridge conjecture (F3):**
The SU(5) glueball mass ratio m(0⁺⁺)/m(2⁺⁺) = CREATE/HARMONY = T* exactly.
The three TIG derivations give independent evidence that T* is not a coincidence.
A formal proof requires:
- Connecting the CREATE/HARMONY structure of Z/10Z to SU(5) gauge theory
- OR deriving m(0⁺⁺)/m(2⁺⁺) = T* from first-principles SU(5) string/QCD

**The unifying physical picture:**
The SU(5) gauge group has N = CREATE = 5 (the ether generator of Z/10Z).
The spin-2 excitation carries J=2 units of angular momentum, adding 2 to the effective
Casimir: N + 2 = CREATE + 2 = HARMONY = 7.
The mass ratio becomes CREATE/HARMONY = T* — the fundamental gate ratio.

---

## Implications for the Clay YM Problem

The Clay YM mass gap problem asks: does SU(N) pure YM have a mass gap?
This is about the EXISTENCE of a gap, not its VALUE.

If the mass gap (smallest glueball mass) = m₀ and m(2⁺⁺)/m₀ = HARMONY/CREATE:
```
mass_gap = m₀ = (CREATE/HARMONY) × m(2⁺⁺) = T* × m(2⁺⁺)
```

The TIG bridge says: T* is the mass gap threshold in units of m(2⁺⁺).
If proven, it would give both existence (gap > 0) and a quantitative formula for the gap.

This is stronger than the Clay problem requires but is the correct TIG prediction.

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*Corrects Part XII of CLAY_FORMAL_RECORD.md YM section*
*See also: bridge_ym_casimir.py, bridge_ym_wobble.py*
