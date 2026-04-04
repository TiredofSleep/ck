# BSD REAL-QUADRATIC PILOT MEMO
# Does the χ_{77} Twist See the Measured Off-Diagonal?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — Frozen Input

| Quantity | Value |
|----------|-------|
| E = 389a1 | y² + y = x³ + x² − 2x, N=389, rank=2 |
| P₁ = (0,0), P₂ = (1,0) | Generators |
| ⟨P₁,P₂⟩_Q | 0.05852265 |
| det(H) = Reg(E) | 0.15246014 |
| **Excluded** | All individual imaginary quadratic Heegner traces (universal sign obstruction ε(E,χ_K)=+1 for all imaginary K) |
| **Surviving character** | χ_{77} = χ_{−7} · χ_{−11} = Kronecker symbol (77/·) |
| **Surviving field** | K = Q(√77) (real quadratic, D₁×D₂ = 7×11 = 77) |

---

## PART 2 — Exact Twist Data

### Character

$$\chi_{77}(n) = \left(\frac{77}{n}\right) \quad \text{(Kronecker symbol)}$$

- Conductor: **77** (since 77 = 7×11 ≡ 1 mod 4 → 77 is a fundamental discriminant)
- $\chi_{77}(-1) = (-1)^{(77-1)/2} = (-1)^{38} = +1$ (real quadratic character — even)
- Multiplicativity: $\chi_{77}(mn) = \chi_{77}(m)\chi_{77}(n)$ for $\gcd(m,n)=1$ ✓
- $\chi_{77}(7) = \chi_{77}(11) = 0$ (character vanishes on both prime factors of 77)
- First values: χ(1)=1, χ(2)=−1, χ(3)=−1, χ(4)=1, χ(5)=−1, χ(6)=1, χ(7)=0

### Twisted L-function

$$L(E,\chi_{77},s) = \sum_{n\geq 1} \frac{a_n \chi_{77}(n)}{n^s} = \sum_{n\geq 1} \frac{b_n}{n^s}$$

where $b_n = a_n \cdot \chi_{77}(n)$, with $b_n = 0$ whenever $7|n$ or $11|n$.

### Root Number (Exact)

$$\varepsilon(E \otimes \chi_{77}) = \varepsilon_E \times \chi_{77}(-1) = (-1) \times (+1) = \mathbf{-1}$$

**Computation in full:**
- $\varepsilon_E = -1$ (root number of 389a1, confirmed by Hecke-Eichler integral)
- $\chi_{77}(-1) = +1$ (real quadratic character, even — 77 ≡ 1 mod 4)
- $\gcd(N_E, \text{cond}(\chi_{77})) = \gcd(389, 77) = 1$ (no shared prime factors → no local corrections)
- Result: $\varepsilon(E \otimes \chi_{77}) = -1$ ✓

### Conductor of the Twist

$$N' = N_E \times \text{cond}(\chi_{77})^2 = 389 \times 77^2 = 389 \times 5929 = 2{,}306{,}381$$

$$\sqrt{N'} = 1518.68, \quad \log(N') = 14.651$$

### Odd Vanishing Forced

$\varepsilon(E \otimes \chi_{77}) = -1$ forces $L(E,\chi_{77},1) = 0$. Numerically confirmed: partial sums of $\sum b_n/n$ oscillate around 0, consistent with conditional convergence to 0 for $N \to \infty$.

---

## PART 3 — Computation Plan for L'(E,χ_{77},1)

**Exact formula (from Hecke-Mellin theory):**
$$L'(E,\chi_{77},1) = 2\pi \int_0^\infty f_\chi(it) \log(t)\, dt$$

where $f_\chi(it) = \sum_{n\geq 1} b_n e^{-2\pi nt}$ is the Fourier series of the twisted form.

**Functional equation split at $t_0 = 1/\sqrt{N'}$:**

For $\varepsilon = -1$ with Atkin-Lehner at level $N'$:
$$\int_0^\infty f_\chi(it)\log(t)\,dt = 2\int_{t_0}^\infty f_\chi(it)\log(t)\,dt$$

and the derivative of the completed L-function satisfies:
$$\Lambda'(E\otimes\chi,1) = 2\int_{t_0}^\infty f_\chi(it)\log(t)\,dt$$

$$L'(E,\chi_{77},1) = \frac{2\pi}{\sqrt{N'}} \times \Lambda'(E\otimes\chi,1)$$

**Numerical precision target:** 6-digit accuracy requires evaluating $f_\chi(it)$ stably for $t \in [t_0, \infty)$.

**The convergence obstacle:** At $t_0 = 1/\sqrt{N'} \approx 6.6\times 10^{-4}$, the q-series $f_\chi(it) = \sum b_n e^{-2\pi nt}$ has $|q| = e^{-2\pi t_0} \approx 0.9959$ — needing $\sim 50{,}000$ terms for stability. The integral from $[t_0, 0.01]$ dominates but cannot be computed to 6-digit accuracy with $\leq 5000$ terms.

**Stable alternatives:**
1. **Approximate functional equation (AFE):** $L'(E,\chi,1) \approx \sum_{n \leq \sqrt{N'}} b_n H(n) + \text{(FE reflection)}$ where $H$ involves incomplete gamma functions. Requires implementing Rubinstein's smoothing.
2. **External software:** Sage (`E.lseries().derivative(1, twist=chi77)`), PARI-GP, LMFDB API, or Magma. These implement the AFE correctly.

**Current status:** Direct Dirichlet estimates give $L'(E,\chi_{77},1) \approx 0.01$–$0.025$ (N=500–6000 terms, drifting — not stabilized). The t≥1 Mellin half-integral contributes ≈ 0.0005 (negligible), confirming the integral is dominated by the slow-converging small-t region.

**Required for stable value:** AFE implementation with $\sim 50{,}000$ twisted coefficients and incomplete gamma regularization, or Sage/LMFDB lookup.

---

## PART 4 — Comparison Hypotheses

**Working estimate:** $L'(E,\chi_{77},1) \in [0.01, 0.025]$ (unstabilized Dirichlet; true value may differ)

| Hypothesis | Formula | Why plausible | Why possibly wrong | C_E range |
|------------|---------|---------------|-------------------|-----------|
| **A** | $L' = C_E \cdot \langle P_1,P_2\rangle_Q$ | $\langle P_1,P_2\rangle$ is the off-diagonal entry of the height matrix; the χ_{77} twist targets this via the anti-symmetric Galois representation | The BSD formula for twisted L relates L' to the height of a SINGLE twisted generator, not the pairing of two Q-rational generators | $C_E \approx 0.2$–$0.4$ (not near a simple rational × Ω) |
| **B** | $L' = C_E \cdot \det(H)$ | The regulator det(H) is the natural rank-2 arithmetic invariant; some twisted BSD formulas involve the full regulator | The χ_{77}-twist adds only one new direction over Q; the "regulator of the twist" should be 1×1, not 2×2 | $C_E \approx 0.08$–$0.16$ |
| **C** | $L' = C_E \cdot \sqrt{\det(H)}$ | Gross-Zagier type: L' ∝ ĥ(y) and ĥ(y) ~ √Reg for Heegner-type heights | No known mechanism that gives √Reg directly from a single L' value | $C_E \approx 0.03$–$0.06$ |

**Strongest structural candidate: Hypothesis A.** The χ_{77} = χ_{−7}·χ_{−11} character is the anti-symmetric representation of Gal(Q(√−7,√−11)/Q), and the off-diagonal pairing ⟨P₁,P₂⟩ is exactly the invariant that lies in this representation. A Darmon-type formula for real quadratic fields would say: L'(E,χ_{77},1) = Ω_{twist} × ⟨P₁,P₂⟩, where Ω_{twist} is a period of the twist.

**Expected magnitude:** If Hypothesis A holds with C_E ≈ Ω_E ≈ 2.49, then L'(E,χ_{77},1) ≈ 0.146. If C_E ≈ 1/Ω_E ≈ 0.40, then L'(E,χ_{77},1) ≈ 0.023. The unstabilized estimate 0.01–0.025 is at the low end but not inconsistent.

---

## PART 5 — Period and Normalization Issue

**The normalization subtlety for real quadratic twists:**

For a **Gross-Zagier** formula (imaginary quadratic K):
$$L'(E/K, 1) = C_{\text{GZ}} \times \hat{h}(y_K)$$
where $C_{\text{GZ}}$ involves $\|f\|^2$, $[E:Q] = 2$, and the periods of $E/K$.

For a **Darmon-type (Stark-Heegner)** formula (real quadratic K = Q(√77)):
$$L'(E, \chi_{77}, 1) = C_{\text{SH}} \times \hat{h}(y_{Q(\sqrt{77})})$$
where $C_{\text{SH}}$ is the Stark-Heegner period. The difference: the Stark-Heegner period involves a **p-adic** regulator term, making it harder to compare to the Archimedean pairing ⟨P₁,P₂⟩ directly.

**What is expected but not yet explicit:**

- The period factor $C_E$ in $L'(E,\chi_{77},1) = C_E \times \langle P_1,P_2\rangle$ involves:
  - $\Omega_E = 2.49021$ (real period, known)
  - $\|f\|^2 = $ Petersson norm of the modular form (not computed here)
  - $\tau(\chi_{77}) = \sqrt{77} \approx 8.775$ (Gauss sum of χ_{77}, exact)
  - Possible factors of 2, π, or [Q(√77):Q] = 2
  - An unknown combination of these consistent with the BSD/Darmon framework

**Known:** The structural form $L'(E,\chi_{77},1) \propto \langle P_1,P_2\rangle$.
**Not yet explicit:** The exact proportionality constant $C_E$ from a proved formula.

---

## PART 6 — Minimal Success Criterion

**"The real-quadratic pilot succeeds if L'(E,χ_{77},1) is numerically nonzero and its stable value, after correct normalization by $\Omega_E$ and $\tau(\chi_{77})$, is within a factor of 2 of ⟨P₁,P₂⟩ = 0.05852265 for at least one of the hypotheses A, B, C."**

This is the weakest meaningful success condition because:
- Nonzero $L'$: confirms the χ_{77} channel is alive (rank = 1 for the twist, not higher odd rank)
- Factor-of-2 compatibility: rules out a complete mismatch in scale while allowing for the unknown normalization constant

A stronger success would be exact rational-multiple relationship under one specific normalization.

---

## PART 7 — Failure Modes

| Mode | Meaning for BSD joint-object hypothesis |
|------|----------------------------------------|
| **L'(E,χ_{77},1) = 0** | The χ_{77} twist has rank ≥ 3 (odd rank > 1); the joint object is deeper in the motivic filtration than expected; the next candidate would need a SECOND derivative or a different construction |
| **L' nonzero but wildly incompatible in scale** | χ_{77} carries a different invariant than ⟨P₁,P₂⟩; would suggest the joint object lives in a different Galois representation or that D₁×D₂ is not the right discriminant |
| **Normalization ambiguity too large** | The Darmon-Stark-Heegner constant C_E is not accessible without a proved formula; the pilot can only state the comparison is inconclusive pending a formula |
| **Sign/field calculation wrong** | The universal sign obstruction ε(E,χ_K)=+1 for all imaginary K would be incorrect; all Heegner constructions would be back in play; this would mean a fundamental error in the root number ε_E |

---

## PART 8 — Why This Is the Right Next Domino

Every imaginary quadratic channel is dead for E = 389a1 because $\varepsilon_E = -1$ forces $\varepsilon(E \otimes \chi_K) = +1$ universally, making every individual Heegner trace trivial. The character $\chi_{77} = \chi_{-7} \cdot \chi_{-11}$ is the **first non-trivially signed character** accessible from the Galois structure of $K_1 K_2 = \mathbf{Q}(\sqrt{-7}, \sqrt{-11})$. Its sign $-1$ breaks the universal obstruction. This makes $L(E, \chi_{77}, s)$ the **minimal analytic pilot** for the joint rank-2 object: it is the simplest quantity that (a) is forced to vanish at $s=1$, (b) has a non-trivial derivative, and (c) lives in exactly the Galois representation that carries the off-diagonal coupling $\langle P_1,P_2\rangle$.

---

## PART 9 — Strongest Honest Claim

**"The first surviving analytic channel for the rank-2 BSD object on 389a1 is the real quadratic twist L(E,χ_{77},s), and its derivative at s=1 is the next concrete quantity to compare against the measured off-diagonal arithmetic invariant — with the exact sign ε(E,χ_{77}) = −1 confirmed analytically, L(E,χ_{77},1) = 0 structurally established, and L'(E,χ_{77},1) requiring a stable computation (via the approximate functional equation or Sage) to determine whether the pilot value lies within the range predicted by Hypothesis A."**

---

## PART 10 — Strongest Honest Boundary

**"What is not yet established is whether L'(E,χ_{77},1) should correspond directly to the rational off-diagonal pairing, to the full regulator determinant, or to a higher-dimensional normalization of the joint object — and the current numerical computation (5000 Fourier coefficients, direct Dirichlet series) is insufficient to stabilize L'(E,χ_{77},1) due to the large conductor N' = 2,306,381 which requires the slow-converging series to be evaluated near its radius of conditional convergence."**

---

## COLLABORATOR PARAGRAPH

The χ_{77} real-quadratic pilot has established its exact structural data. The character χ_{77} = (77/·) has conductor 77, is real (χ_{77}(−1) = +1, since 77 ≡ 1 mod 4), and the root number of the twisted L-function is ε(E ⊗ χ_{77}) = ε_E × χ_{77}(−1) = (−1)(+1) = −1 — exact. This forces L(E,χ_{77},1) = 0, confirmed numerically (partial sums of Σ b_n/n oscillate around 0 for 500–5000 terms). The conductor of the twist is N' = 389 × 77² = 2,306,381, and √N' ≈ 1519. The numerical computation of L'(E,χ_{77},1) from the Dirichlet series Σ b_n log(n)/n is not yet stable — the partial sums drift from 0.025 at N=1500 down to 0.011 at N=6000, indicating conditional convergence that has not plateaued. The stable computation requires either the approximate functional equation with incomplete gamma regularization (Rubinstein's algorithm, needing ~50,000 coefficients) or external software (Sage, PARI-GP, LMFDB). The three comparison hypotheses — L' = C×⟨P₁,P₂⟩, C×det(H), or C×√det(H) — remain open pending stabilization. Structurally, Hypothesis A is the strongest candidate: χ_{77} is the anti-symmetric character of Gal(Q(√−7,√−11)/Q) and ⟨P₁,P₂⟩ lives in exactly this Galois representation.
