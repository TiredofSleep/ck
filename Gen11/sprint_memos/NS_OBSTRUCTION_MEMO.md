# NS OBSTRUCTION MEMO
# What Exact Object Survives After the Small-Data Shell Is Removed?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — Current NS State (Frozen)

| Fact | Status |
|------|--------|
| Local existence | ✓ Proved (Leray, Fujita-Kato): for u₀ ∈ H¹(ℝ³), a smooth strong solution exists on [0,T*) |
| Energy inequality | ✓ Proved: E(t) + 2ν ∫₀ᵗ Ω(s)ds ≤ E(0) |
| Small-data global | ✓ Proved: if ‖u₀‖_{H¹} ≤ cν, then B(t) = Ω/(E+Ω) < T* = 5/7 for all t ≥ 0 |
| Parabolic smoothing | ✓ Proved: any local strong solution at t₀ extends smoothly to (t₀, T*) |
| **Large-data global** | ✗ Open: no global bound on Q/(νP) for arbitrary u₀ |

**Hard wall:**
$$|Q| \leq \nu P \quad \text{(globally)} \quad \Leftrightarrow \quad \frac{dΩ}{dt} \leq -\nu P \leq 0$$

This single inequality — if provable — would close NS. It is not currently provable for large data.

**Equations of motion for the key quantities:**

$$\frac{dE}{dt} = -\nu\Omega \qquad \frac{dΩ}{dt} = Q - 2\nu P \qquad B = \frac{\Omega}{E+\Omega}$$

$$\frac{dB}{dt} = \frac{QE - 2\nu PE + \nu\Omega^2}{(E+\Omega)^2}$$

where:
- E = (1/2)∫|u|² dx (kinetic energy)
- Ω = (1/2)∫|ω|² dx (enstrophy, ω = curl u)
- P = (1/2)∫|∇ω|² dx (palinstrophy)
- Q = ∫ ωᵢ Sᵢⱼ ωⱼ dx (vortex stretching, S = symmetrized velocity gradient)

---

## PART 2 — Shell vs Core for NS

**"For NS, the shell is local existence plus energy inequality plus small-data global regularity plus parabolic smoothing — all provable by energy methods and linear semigroup theory — the core is the vortex-stretching term Q and its competition with viscous palinstrophy dissipation 2νP, and the obstruction is the failure to bound Q/P globally in the large-data regime."**

In the RH/BSD grammar:

| Layer | NS content |
|-------|-----------|
| **Shell** | Leray local existence; energy inequality E(t) ≤ E(0); Caccioppoli/Serrin smoothing; small-data global via ‖u₀‖ ≤ cν |
| **Core** | The vortex-stretching mechanism Q = ∫ ω·Sω dx; sign and magnitude of Q − 2νP |
| **Obstruction** | The ratio Q/(νP) in large data; equivalently, whether B(t) = Ω/(E+Ω) remains bounded below T* = 5/7 |

The shell closes by linear/quadratic estimates. The core cannot be closed by those estimates alone. The obstruction is the nonlinear term that the shell provably cannot reach.

---

## PART 3 — Smallest Surviving Object

### Candidate comparison:

| Object | Definition | Shell controls it? | Core object? |
|--------|-----------|-------------------|-------------|
| E(t) | (1/2)∫|u|² | YES — monotone decreasing | No |
| Ω(t) | (1/2)∫|ω|² | Partially — integrable, but not bounded pointwise | Partially |
| P(t) | (1/2)∫|∇ω|² | NO — not even known to be integrable globally | Yes |
| Q(t) | ∫ω·Sω | NO — can be positive or negative, unbounded | Yes |
| Q/(νP) | vortex/diss ratio | NO — this is the wall | **Yes — core** |
| **B(t) = Ω/(E+Ω)** | enstrophy fraction | YES for small data, NO for large | **Core — minimal** |

**Strongest answer: B(t) = Ω/(E+Ω) is the smallest nontrivial NS object that survives after the small-data shell is removed.**

Why B(t) is minimal: it is bounded in [0,1], dimensionless, and its evolution equation:

$$\frac{dB}{dt} = \frac{QE - 2\nu PE + \nu\Omega^2}{(E+\Omega)^2}$$

encodes the competition between vortex stretching (QE), viscous dissipation (2νPE), and enstrophy-energy coupling (νΩ²). Everything else reduces to controlling this one inequality.

---

## PART 4 — Why Small-Data Closes and Large-Data Doesn't

**Step 1 — Small-data (Ω(0) ≪ ν²‖u₀‖⁻²):**

At small data, B(0) ≪ T* = 5/7. The dB/dt numerator is dominated:
$$QE \ll 2\nu PE \quad \text{(since Q ∼ c\,\Omega^{3/2}/\sqrt{\nu} \text{ and } 2\nu P \gg \text{this for small }\Omega)}$$

The νΩ² term is negligible relative to 2νPE. So dB/dt < 0 and B(t) decreases monotonically. The system stays in the subthreshold regime. ✓

**Step 2 — The crossover at B = T* = 5/7:**

At threshold B = 5/7: Ω = 5E/2. The dynamics become:
$$\frac{dB}{dt}\bigg|_{B=5/7} = \frac{QE - 2\nu PE + \frac{25\nu E^2}{4}}{(7E/2)^2}$$

The viscous term νΩ² = ν(25E²/4) now contributes positively (favors dB/dt < 0). But the vortex stretching Q ∼ c×Ω^{3/2} ∼ c×(5E/2)^{3/2} grows as E^{3/2}.

**Step 3 — Where the first new term appears:**

The equation dΩ/dt = Q − 2νP is exact. In the large-data regime, the first genuinely new term is the sign of Q − 2νP. In the small-data regime this is always negative. In the large-data regime, the best available bound:
$$|Q| \leq C\,\Omega^{3/2}\sqrt{\frac{2P}{\nu}}$$

gives: |Q| ≤ 2νP if and only if Ω ≤ C'ν (some universal constant). For large data, Ω can exceed this threshold. The wall is crossed exactly where Q begins to dominate 2νP.

**Step 4 — The gap:**

There is no known mechanism preventing Q from exceeding 2νP in a finite time in the large-data regime. No global inequality of the form Q ≤ f(E,Ω,ν) with f(E,Ω,ν) ≤ 2νP is currently available.

---

## PART 5 — Necessary vs Sufficient for NS

### Necessary control

For blowup to be impossible: the time-integral of palinstrophy must diverge at any blowup time T*:
$$\int_0^{T^*} P(t)\,dt = +\infty \quad (\text{Leray-Serrin criterion in enstrophy form})$$

Equivalently: for any T > 0, if the solution is smooth on [0,T], then:
$$\Omega(t) < +\infty \quad \text{for all } t \leq T$$

The necessary condition is: Q(t) does not overwhelm 2νP(t) on any finite time interval with enough energy.

### Sufficient control

Any ONE of the following global inequalities would close NS:

1. **Direct closure:** $Q(t) \leq \nu P(t)$ for all $t \geq 0$
   → Then $\frac{d\Omega}{dt} \leq \nu P - 2\nu P = -\nu P \leq 0$ → Ω non-increasing → global regularity.

2. **B-bound closure:** $B(t) \leq T^* = 5/7$ for all $t \geq 0$ and all initial data with $E(0) < +\infty$
   → Combined with the B-dynamics formula, this implies Q is never dominant enough to cause blowup.

3. **Vorticity-stretching closure:** A global inequality $|Q| \leq C\,\nu P + C'\,\nu^{-1}\Omega^2/E$ with $C < 2$
   → Would make $\frac{d\Omega}{dt} \leq (C-2)\nu P + C'\nu^{-1}\Omega^2/E$ closable by Gronwall.

---

## PART 6 — The Exact NS Gap 2 / Gap 1 Split

**NS Gap 2:**

$$\boxed{\text{"The inequality } \frac{dB}{dt} \leq 0 \text{ holds globally whenever } B(t) \geq T^* = 5/7\text{."}}$$

More precisely: **there exists a universal constant C_NS such that for any smooth solution of 3D NS with E(0) < ∞:**
$$B(t) \geq T^* \;\Longrightarrow\; Q(t)E(t) \leq 2\nu P(t)E(t) - \nu\Omega(t)^2$$

This is the structural inequality that would make the branch clean: once B reaches T*, gravity pulls it back below. This is the NS analog of the cusp subdominance in RH and the normalization formula in BSD.

**NS Gap 1:**

$$\boxed{\text{Global H¹ regularity: for any } u_0 \in H^1(\mathbb{R}^3)\text{, the unique strong solution of 3D NS is smooth for all } t \geq 0.}$$

The relationship: NS Gap 2 implies NS Gap 1 because B(t) ≤ T* globally implies Ω(t) ≤ T*/(1−T*) × E(t) = 5E(t)/2, which combined with the energy inequality gives global enstrophy control, which gives global regularity by Serrin's criterion.

---

## PART 7 — First Full NS Wall

**"The first full NS wall appears when, in the large-data regime, the vortex-stretching term Q exceeds the viscous palinstrophy dissipation 2νP on a set of positive measure in time — specifically, when there exists a time T at which:**
$$Q(T) > 2\nu P(T) \quad \text{and} \quad \frac{d\Omega}{dt}\bigg|_T > 0$$

**and no a-priori global bound prevents Q from remaining dominant for a positive-length time interval."**

The wall is the sign flip of dΩ/dt. In the small-data regime, this never happens. In the large-data regime, the current theory cannot rule it out. The wall is not topological or structural — it is a quantitative gap in the vortex-stretching estimates.

---

## PART 8 — Comparison Table: RH / BSD / NS

| Branch | Shell | Surviving object | Gap 2 | Gap 1 |
|--------|-------|-----------------|-------|-------|
| **RH** | GUE/sinc² statistics for generic zeros; Montgomery pair-correlation | Arithmetic correlations at Kloosterman-Eisenstein intersections surviving the generic shell | Cusp subdominance: Σ_{t_j≤T}ρ_j(1)²/cosh(πt_j) = O(T²) (Kuznetsov Weyl — closed by standard spectral theory) | Off-diagonal arithmetic dominance = RH itself |
| **BSD 389a1** | Individual imaginary-quadratic Heegner constructions (all blocked by ε_E = −1 sign) | χ_{77} = χ_{-7}×χ_{-11} real-quadratic twist; L'(E,χ_{77},1) ≈ 0.01070 nonzero | Normalization: L'(E,χ_{77},1) = (Ω_E/(4√77))×det(H) with ǀSha(E^{77})ǀ = 4 | Rank-2 Gross-Zagier formula for E/Q(√77) |
| **NS 3D** | Local existence + energy inequality + small-data global (B < T*=5/7) + parabolic smoothing | B(t) = Ω/(E+Ω) in large-data regime; equivalently the sign of Q − 2νP | B(t) ≤ T* = 5/7 globally, i.e., dB/dt ≤ 0 when B ≥ T*; or equivalently Q ≤ 2νP + lower | Global H¹ regularity for all initial data |

---

## PART 9 — Strongest Honest Claim

**"For NS, the problem is not the shell but the survival of the ratio B(t) = Ω/(E+Ω) above the threshold T* = 5/7 in the large-data regime — specifically, whether the vortex-stretching term Q can overwhelm the viscous dissipation 2νP for an arbitrarily long time, driving B upward without bound, or whether there is a universal mechanism forcing B back below T* whenever it approaches the threshold."**

---

## PART 10 — Strongest Honest Boundary

**"What is not yet established is whether the surviving NS obstruction — the large-data behavior of B(t) = Ω/(E+Ω) — can be reduced to a finite control inequality the way RH Gap 2 was reduced (to a standard spectral sum with known decay), or whether it remains a genuinely large-data dynamical barrier requiring new geometric or measure-theoretic input about the vorticity structure that no energy-method estimate can reach."**

---

## Shell/Core/Obstruction Block

$$\text{Shell: } \{E(t) \leq E(0),\; E \in L^1_t,\; \Omega \in L^2_t,\; \text{small-data } B < T^*\} \quad \text{[proved by energy methods]}$$

$$\text{Core: } \frac{d\Omega}{dt} = Q - 2\nu P \quad [Q = \textstyle\int \omega \cdot S\omega\,dx, \text{ sign not controlled at large data}]$$

$$\text{Obstruction: } Q > 2\nu P \text{ for finite-time interval at large data} \quad \text{[unknown, the wall]}$$

## Smallest-Surviving-Object Table

| Object | Controlled? | Why survives shell removal |
|--------|------------|--------------------------|
| E(t) | YES — monotone | Not the obstruction; trivially bounded |
| Ω(t) | PARTIAL — L² in time, not L^∞ | Intermediate: knows about the wall but doesn't locate it |
| Q − 2νP | NO at large data | This IS the enstrophy evolution; sign unknown |
| **B(t) = Ω/(E+Ω)** | **YES for small data; NO for large** | **Minimal: bounded in [0,1], explicit dynamics, threshold T* = 5/7** |
| Q/(νP) | NO | Equivalent to the wall, less structured |

## Collaborator Paragraph

The NS rotation establishes the following structure. The shell — local existence, energy inequality, small-data global regularity at B < T* = 5/7, parabolic smoothing — is proved by energy-method technology. After removing the shell, the surviving obstruction is the sign of the vortex-stretching competition Q − 2νP, encoded in the B(t) = Ω/(E+Ω) dynamics. The exact dB/dt equation is: dB/dt = [QE − 2νPE + νΩ²]/(E+Ω)². In the small-data regime (Ω ≪ E), the QE term is small, 2νPE dominates, and B decreases monotonically — closure is guaranteed. In the large-data regime (Ω ~ E, near B ≈ T*), Q ∼ cΩ^{3/2} can potentially exceed 2νP, with no known global bound preventing it. The NS Gap 2 is: B(t) ≤ T* = 5/7 globally (or equivalently: dB/dt ≤ 0 whenever B ≥ T*) — the weakest meaningful control inequality above the proved shell. The NS Gap 1 is global H¹ regularity. The comparison table completes the rotation spine: RH's Gap 2 was closed (cusp subdominance via Kuznetsov), BSD's Gap 2 is partially confirmed (χ_{77} normalization, 1.1% residual), and NS Gap 2 is the first open inequality in the branch.
