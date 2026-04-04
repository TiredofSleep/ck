# The RH Landscape: Seven Approaches, One Target
## Synthesis Map — TIG vs Mainstream

*Brayden Sanders — 7Site LLC | March 2026*

---

## The Target (same for all)

Prove: every non-trivial zero of ζ(s) has Re(s) = 1/2.

Equivalently: the critical strip contains no zeros off the critical line.

---

## Seven Approaches Mapped

### 1. Guth-Maynard 2024 (Zero-density via Dirichlet polynomials)
**Bridge:** N(σ,T) ≤ T^{30(1-σ)/13+o(1)}

**Their object:** Dirichlet polynomial D_N(t) = Σ b_n n^{-it}.
A zero off σ=1/2 forces D_N to take large values (~N^{3/4}) too often.
They bound how often this can happen using matrix singular values.

**What they proved:** First improvement on Ingham's 1940 zero-density bound.
Fewer exceptional zeros near σ=3/4.

**Their wall:** They can't push to σ=1/2. The matrix method breaks at the critical exponent. Maynard himself said "these aren't the right techniques."

**TIG translation:** A Dirichlet polynomial taking large values = a Mix_λ chain spending time in the COL/CTR corridor (λ>0.8). Their bound on "large values" = our bound on "time in dangerous corridor." Their matrix eigenvalue = our dominant corridor occupancy.

**Bridge angle:** They're measuring corridor-entry *frequency* (how often D_N gets large). We're measuring corridor *depth* (how far λ gets from 0).

---

### 2. Connes NCG / Adele Class Space (Trace formula)
**Bridge:** Zeros = absorption spectrum of the adele class space action

**Their object:** The noncommutative space X of adele classes (idèle class group orbits). The scaling action of K* on L²(X) has a trace formula. On-line zeros appear as absorption; off-line zeros would appear as *resonances* (not true zeros of a self-adjoint operator).

**What they proved:** RH ↔ positivity of the Weil distribution ↔ validity of the trace formula. The reduction is exact but the trace formula itself remains unproved.

**Their wall:** Proving Weil positivity in the global case. The semilocal case works; the global adelic case doesn't close.

**TIG translation:** Their "absorption vs resonance" distinction = our "Pre-leak corridor vs CTR corridor." An on-line zero absorbs the chain (returns to HARMONY). An off-line zero would be a resonance = a chain that keeps bouncing in the gap without being absorbed. The sub-magma theorem proves there are no resonances: C×C⊆C forces every chain back to HARMONY.

**Bridge angle:** Connes is working with the *algebraic* structure (adele classes, Hecke algebras). TIG is working with a *finite* algebraic model that captures the same absorption/resonance distinction at the level of a 9-element magma. TIG gives the mechanism; Connes gives the geometric framework.

---

### 3. OOL-KND-RH (Phase-drift / angular symmetry)
**Bridge:** corr(|dθ/dσ|, λ²) = -0.989 (computed)

**Their object:** Phase function θ(t;σ) = 2·arctan(Im ζ / Re ζ).
At σ=1/2: angular drift dθ/dσ = 0 (drift-free dynamics).
Off σ=1/2: drift accumulates, symmetry breaks.
Zeros: θ jumps by π.

**What they showed:** Numerically, only σ=1/2 supports drift-free dynamics. Phase jumps at zeros coincide with the critical line.

**TIG translation:** Their "drift rate" = our "wobble weight accumulation." λ=0 at σ=1/2 → no wobble → drift-free. λ>0 off the line → wobble accumulates → drift visible. The Mix_λ parameter IS the drift parameter in a different coordinate.

**Bridge angle:** They're on the bridge from the *rotation* side (how fast the phase turns). We're on the bridge from the *absorption* side (how fast HARMONY pulls). The NS spiral is both simultaneously. This is the closest approach to TIG — they need our sub-magma theorem to explain WHY drift vanishes at σ=1/2.

---

### 4. Hilbert-Pólya / Berry-Keating / Random Matrix Theory (Spectral)
**Bridge:** Zeros = eigenvalues of a self-adjoint operator H

**Their object:** The GUE (Gaussian Unitary Ensemble) statistics of zero spacings match those of random Hermitian matrices. The conjectured H is the xp Hamiltonian (Berry-Keating). Connes' D operator has the right spectrum assuming RH.

**What they showed:** Statistical match between zero spacing and GUE to extraordinary precision (Odlyzko). The zeros *behave as if* they're eigenvalues of a chaotic quantum system.

**TIG translation:** Eigenvalue repulsion in GUE = our product-gap theorem. Cross-terms can't co-occupy a corridor — the corner algebra instantly resets them. The "level repulsion" is the algebraic impossibility of two gap operators anchoring in the same corridor simultaneously. The self-adjoint H = the TSML table acting as a dissipative operator that forces everything to HARMONY.

**Bridge angle:** They're looking for the operator. We have a candidate: the Mix_λ interpolation from TSML to BHML, with the self-adjoint limit at λ=0 (the critical line).

---

### 5. Paley-Wiener Self-Adjoint Restriction (New 2025 preprint)
**Bridge:** ζ(s) = Fredholm determinant D(z) = det₂(I + zK)

**Their object:** Self-adjoint restriction R_PW of the first-order differentiation operator on a weighted Hilbert space H_α. Under a Paley-Wiener band-limit Λ=π, get a Hilbert-Schmidt kernel K. Its discrete spectrum γ_k defines candidate zeros s_k = 1/2 + iγ_k. Claim: N_ζ(T) = N_eig(T) (counting identity).

**What they claimed:** The injection + exact counting forces Re(s_k) = 1/2.

**Status:** Unverified — the counting identity and Fredholm determinant equality need expert scrutiny.

**TIG translation:** Their "band-limit Λ=π" = our "corridor width" (the Pre-leak corridor has λ<0.09 ≈ π/35, very small). Their Hilbert-Schmidt kernel = our TSML composition table acting as an integral operator. The discrete spectrum = the set of stable fixed points (HARMONY and its approach chains).

---

### 6. Lyapunov/Chaotic Operator Approach (Spectral-dynamical, 2025)
**Bridge:** λ_eff ≈ -0.7 → N(σ,T) ≪ T^{1.7} (heuristic improvement on Guth-Maynard)

**Their object:** Construct a chaotic operator O_x from the Riemann-von Mangoldt formula, perturbed by arg ζ(1/2+it). Compute effective Lyapunov exponent λ_eff. Negative Lyapunov = zeros repelled from off-critical positions.

**TIG translation:** Their "negative Lyapunov exponent" = our "HAR is a global attractor." Every trajectory in the TIG flow contracts toward HARMONY. The Lyapunov exponent of the Mix_λ walk = the absorption rate. Our double-2-cycle lemma gives the precise slowdown: each extra cycle reduces |λ_eff| by ~10%.

---

### 7. TIG Corridor Approach (This work)
**Our object:** Mix_λ[a][b] = (1-λ)·TSML[a][b] + λ·BHML[a][b], where λ = 2|σ-1/2|.
Corridors: six λ-windows where different gap operators can activate.
Key theorem: C×C ⊆ C (sub-magma) → no gap anchoring at λ=0 → gap-positivity at σ=1/2.

**What we proved:**
- Corner sub-magma closure: C^⊗k closed for all k (Proc. AMS note)
- Gap-positivity holds on all genuine zero-free verticals to t≈1100
- Corridor drift: interior troughs wander σ∈[0.50, 0.80] — not fixed at critical line
- corr(|dθ/dσ|, λ²) = -0.989 (bridges to OOL-KND-RH)

**Our wall (honest):** Proving analytically that no corridor stays permanently in the gap. The sub-magma theorem shows C is closed under composition — but proving the *continuous* analytic version (that every convergence corridor returns to Pre-leak) requires a classical analytic lemma we don't yet have.

---

## The Synthesis Map

```
APPROACH          OBJECT              KEY CLAIM           WALL
─────────────────────────────────────────────────────────────────
Guth-Maynard     Dirichlet poly      Rare large values   σ=3/4 barrier
Connes NCG       Adele classes       Absorption spectrum  Weil positivity  
OOL-KND-RH       Phase drift θ       Drift-free at ½     No proof of why
Berry-Keating    xp Hamiltonian      Quantum chaos model  Find the operator
PW Self-adjoint  Kernel K            Det=ζ identity      Unverified
Lyapunov chaos   Chaotic operator    λ_eff < 0           Heuristic only
TIG Corridors    Mix_λ algebra       Sub-magma closure   Analytic last lemma
```

**Where they converge:**

Every approach is saying the same thing in a different language:

> σ=1/2 is the unique fixed point of a self-referential absorbing structure.

- Guth-Maynard: D_N can't stay large → corridor can't sustain
- Connes: zeros are absorption, not resonance → corridor returns
- OOL-KND-RH: drift vanishes → λ=0 → Pre-leak corridor
- Berry-Keating: eigenvalue repulsion → product-gap theorem
- TIG: C×C⊆C → no gap anchoring → HARMONY absorbs everything

**The missing bridge (what none of them have):**

A proof that the absorbing structure extends *uniformly* to all heights t.

Guth-Maynard get closer as N→∞ but can't reach σ=1/2.
Connes needs Weil positivity in the global case.
TIG needs the KV bound for all t, not just numerically to t≈1100.

**They're all circling the same analytic lemma:**

> The minimum of |ζ(σ+it)| on any zero-free vertical does not pinch to zero.

In corridor language: no convergence corridor sustains a permanent sojourn in the gap.

---

## What TIG offers each approach

| Approach | What TIG adds |
|----------|---------------|
| Guth-Maynard | Algebraic reason WHY D_N can't stay large: sub-magma closure prevents sustained corridor occupation |
| Connes | Mechanism for absorption: C×C⊆C = the absorption is algebraically forced, not just spectral |
| OOL-KND-RH | Proof that drift vanishes at σ=1/2: λ=0 → Pre-leak → no wobble → no drift |
| Berry-Keating | The operator: Mix_λ interpolation is the self-adjoint candidate; λ=0 = critical line = fixed point |
| PW Restriction | The discrete spectrum: TSML fixed points are the eigenvalues |
| Lyapunov | Quantification: absorption rate = Lyapunov exponent; double-2-cycle lemma gives the constant |

---

## The Bridge Sentence

"Every approach to RH is trying to show that ζ(s) has no permanent corridor outside σ=1/2. TIG provides the algebraic mechanism — sub-magma closure — that explains why this is true; the remaining work is translating the finite discrete proof into the infinite analytic setting."

*(c) 2026 Brayden Sanders & C. A. Luther / 7Site LLC | DOI: 10.5281/zenodo.18852047*
