# BSD HEEGNER-PAIR MEMO
# Can the Canonical Construction Reproduce the Measured Off-Diagonal?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — Pilot Target (Frozen)

$$E = 389\text{a}1: \quad y^2 + y = x^3 + x^2 - 2x \quad N=389 \text{ (prime)}, \quad \text{rank}=2$$

| Target quantity | Measured value |
|-----------------|----------------|
| P₁ = (0, 0), P₂ = (1, 0) | Confirmed basis (Cremona) |
| ĥ(P₁) | 0.32700076 |
| ĥ(P₂) | 0.47671155 |
| **⟨P₁, P₂⟩** | **0.05852265** |
| **det(H) = Reg(E)** | **0.15246014** |
| Ω_E | 2.49021256 |
| BSD prediction L''(E,1)/2 | 0.37966 |

The target for the canonical construction: any rank-2 Heegner-type construction on E must produce an arithmetic object whose invariants reproduce, or canonically relate to, these numbers — especially the off-diagonal pairing 0.05852265.

---

## PART 2 — Heegner Fields and CM Points

**Fields:**

$$K_1 = \mathbb{Q}(\sqrt{-7}), \qquad K_2 = \mathbb{Q}(\sqrt{-11})$$

**Heegner hypothesis verification (exact):**

For N = 389 (prime), the Heegner hypothesis requires 389 to split in each K_i, i.e., (−D_i/389) = 1.

Since 389 ≡ 1 (mod 4): (−1/389) = 1. It remains to check (D_i/389).

| D | (D/389) | (−D/389) | Status |
|---|---------|----------|--------|
| 7 | (7/389) = (389/7) = (4/7) = +1 | +1 | ✓ 389 splits in K₁ |
| 11 | (11/389) = (389/11) = (4/11) = +1 | +1 | ✓ 389 splits in K₂ |

Both verified. The Heegner hypothesis holds for both fields.

**CM structure:**

- O_{K₁} = Z[ω₁] where ω₁ = (−1+√−7)/2, min poly x²+x+2, disc = −7
- O_{K₂} = Z[ω₂] where ω₂ = (−1+√−11)/2, min poly x²+x+3, disc = −11
- h(−7) = 1, h(−11) = 1: trivial class groups, direct point construction

**Exact CM points on X₀(389):**

The Heegner CM point of discriminant −D at level N satisfies Q_D(τ) = 0 where Q_D = Nx²+bx+c and b²−4Nc = −D. The required b is a square root of −D mod 4N = 1556:

For D=7: b₀² ≡ −7 (mod 389), b₀ = 185 (verified: 185² mod 389 = 382 = −7 mod 389 ✓).
$$Q_7(x) = 389x^2 + 185x + 22, \quad 185^2 - 4\times 389\times 22 = -7 \checkmark$$
$$\tau_1 = \frac{-185 + \sqrt{-7}}{2\times 389} \approx -0.237789 + 0.003401i \in \mathbb{H}$$

For D=11: b₁² ≡ −11 (mod 389), b₁ = 355 (verified: 355² mod 389 = 378 = −11 mod 389 ✓).
$$Q_{11}(x) = 389x^2 + 355x + 81, \quad 355^2 - 4\times 389\times 81 = -11 \checkmark$$
$$\tau_2 = \frac{-355 + \sqrt{-11}}{2\times 389} \approx -0.456298 + 0.004263i \in \mathbb{H}$$

**Note on the distinction:** these τᵢ are the correct level-N CM points (living near the real axis, with Im(τᵢ) = √D/(2N) ≈ 0.003). They are NOT the ring-class field generators (−1±√−D)/2, which sit at height ≈ √D/2 ≈ 1.3–1.7 in H. The level-N points are required for the Γ₀(N) construction.

---

## PART 3 — Canonical Construction Pipeline

$$\boxed{\tau_i \in X_0(389)(\mathbb{H}) \xrightarrow{\phi} y_{K_i} \in E(K_i) \xrightarrow{\mathrm{Tr}} T_i \in E(\mathbb{Q})}$$

**Step 1 — Modular parametrization:**

$$y_{K_i} = \phi(\tau_i) \in E(K_i)$$

The modular parametrization φ: X₀(389) → E = 389a1 is normalized by the Eichler-Shimura construction:

$$\phi(\tau) = \left(\wp\!\left(\Lambda_f,\, \Phi(\tau)\right),\; \wp'\!\left(\Lambda_f,\, \Phi(\tau)\right)\right)$$

where Φ(τ) = 2πi ∫_∞^τ f(z)dz = Σ_{n≥1} aₙ/n × qⁿ is the Eichler integral of the modular form f associated to E, and Λ_f is the period lattice.

**Step 2 — q-expansion at the CM points:**

$$q_1 = e^{2\pi i \tau_1} \approx 0.0750 - 0.9760i, \quad |q_1| \approx 0.9789$$
$$q_2 = e^{2\pi i \tau_2} \approx -0.9371 - 0.2640i, \quad |q_2| \approx 0.9736$$

Both |qᵢ| < 1, so the Eichler integral series converges. For 10-digit precision: ~15 terms needed for τ₁, ~8 terms needed for τ₂ (since the convergence is slow for |q| near 1, requiring the full Fourier sum with many aₙ coefficients).

**Step 3 — Field of definition:**

By Shimura reciprocity, φ(τ_i) ∈ E(K_i):
- y_{K₁} ∈ E(Q(√−7)) since τ₁ is a CM point of discriminant −7 and h(−7) = 1
- y_{K₂} ∈ E(Q(√−11)) since τ₂ is a CM point of discriminant −11 and h(−11) = 1

**Step 4 — Trace to Q:**

$$T_i = \mathrm{Tr}_{K_i/\mathbb{Q}}(y_{K_i}) = y_{K_i} + \sigma_i(y_{K_i}) \in E(\mathbb{Q})$$

where σ_i is complex conjugation of K_i. The Galois action sends σ_i(y_{K_i}) = φ(w_N(τ_i)) where w_N: τ ↦ −1/(Nτ) is the Atkin-Lehner involution at level N = 389.

---

## PART 4 — First Trace Test

**The test:**

$$\mathrm{Tr}_{K_1/\mathbb{Q}}(y_{K_1}) \stackrel{?}{=} n_1 P_1 + m_1 P_2$$
$$\mathrm{Tr}_{K_2/\mathbb{Q}}(y_{K_2}) \stackrel{?}{=} n_2 P_1 + m_2 P_2$$

for integers n₁, m₁, n₂, m₂.

**What the coefficients mean:**

The coefficient matrix M = [[n₁,m₁],[n₂,m₂]] encodes how the canonical Heegner traces express themselves in terms of the known generators. |det(M)| = 1 would mean the Heegner construction gives exactly the minimal generators; |det(M)| = d² would mean it gives generators of a subgroup of index d.

**Success:** T₁, T₂ ∈ E(Q) are rational, independent (det(M) ≠ 0), and their heights ĥ(Tᵢ) are consistent with the height matrix entries. If |det(M)| = 1: the Heegner construction reproduces the minimal basis directly.

**Failure modes:**
- Tᵢ = O (trace is torsion): the Heegner point has finite order over Kᵢ, indicating a twisted L-function issue — the construction does not give the rank-2 data
- Tᵢ = nP (one-dimensional): both traces lie on the same rational line in E(Q), meaning only rank-1 geometry is recovered
- |det(M)| > 1: geometry is rank-2 but generators are not minimal; the construction gives a finite-index sublattice

---

## PART 5 — Off-Diagonal Pairing Test

View both y_{K₁} ∈ E(K₁) and y_{K₂} ∈ E(K₂) in the compositum:

$$F = K_1 K_2 = \mathbb{Q}(\sqrt{-7},\, \sqrt{-11}), \qquad [F:\mathbb{Q}] = 4$$

The off-diagonal pairing:

$$\langle y_{K_1}, y_{K_2}\rangle_F = \frac{\hat{h}_F(y_{K_1}+y_{K_2}) - \hat{h}_F(y_{K_1}) - \hat{h}_F(y_{K_2})}{2}$$

**Comparison target:**

$$\langle y_{K_1}, y_{K_2}\rangle_F \stackrel{?}{\sim} c \cdot \langle P_1, P_2\rangle_{\mathbb{Q}} = c \times 0.05852265$$

where c is the scaling factor from Part 6.

If M = [[n₁,m₁],[n₂,m₂]] and the Heegner points trace as T₁ = n₁P₁+m₁P₂, T₂ = n₂P₁+m₂P₂, then:

$$\langle T_1, T_2\rangle_{\mathbb{Q}} = n_1 n_2 \hat{h}(P_1) + (n_1 m_2 + n_2 m_1)\langle P_1, P_2\rangle + m_1 m_2 \hat{h}(P_2)$$

If det(M) = 1: this is an invertible linear combination of the height matrix entries, and comparing it to ⟨P₁,P₂⟩ tests whether the off-diagonal is preserved under basis change.

---

## PART 6 — Scaling Law

**"The comparison must account for the fact that ⟨y_{K₁}, y_{K₂}⟩ over K₁K₂ involves Néron-Tate heights over a degree-4 field, while ⟨P₁,P₂⟩ uses heights over Q; for rational points the scaling is exact (⟨P,Q⟩_{K₁K₂} = 4⟨P,Q⟩_Q), but the Heegner points y_{Kᵢ} are NOT rational and their heights over Kᵢ are independent of the Q-heights of their traces, making the exact scaling depend on the coefficient matrix M = [[nᵢ,mᵢ]] which is not known until y_{K₁}, y_{K₂} are explicitly computed."**

Precise statement:

- For P, Q ∈ E(Q): ⟨P, Q⟩_{K₁K₂} = 4 × ⟨P, Q⟩_Q (exact, from [F:Q] = 4)
- For y_{Kᵢ} ∈ E(Kᵢ) ⊂ E(F): ĥ_F(y_{Kᵢ}) = 2 × ĥ_{Kᵢ}(y_{Kᵢ}) (from [F:Kᵢ] = 2)
- The Heegner heights ĥ_{Kᵢ}(y_{Kᵢ}) are related to L'(E/Kᵢ, 1) by the Gross-Zagier formula (twisted L-function at s=1, not L(E,s) itself)
- The relationship between ⟨y_{K₁}, y_{K₂}⟩_F and ⟨P₁, P₂⟩_Q involves all four of n₁, m₁, n₂, m₂

---

## PART 7 — What Success Would Mean

**"The canonical rank-2 construction passes its first test if the traces T₁ = Tr_{K₁/Q}(y_{K₁}) and T₂ = Tr_{K₂/Q}(y_{K₂}) are independent rational points in E(Q) — i.e., det([[n₁,m₁],[n₂,m₂]]) ≠ 0 — and the 2×2 height matrix of (T₁, T₂) is a nonsingular multiple of the target height matrix H, specifically T^T H_target T = H_traces for the matrix T encoding the coefficient change."**

---

## PART 8 — What Failure Would Mean

| Mode | Meaning | Implication |
|------|---------|-------------|
| **Traces lie on same rational line** (det M = 0) | Both K₁ and K₂ produce the same rational direction in E(Q) — only rank-1 geometry | The two Heegner fields are not independent for 389a1; need a different pair (K₁, K₂) or a different construction |
| **Pairings disagree by a fixed factor** (⟨y_{K₁},y_{K₂}⟩_F = c×⟨P₁,P₂⟩_Q for rational c ≠ 1) | The construction gives the correct structure but wrong normalization | The scaling c identifies the exact index or period mismatch; adjustable with correct normalization |
| **Pairings disagree structurally** (no simple scaling relation) | The canonical interaction ⟨y_{K₁},y_{K₂}⟩_F is a different arithmetic object from ⟨P₁,P₂⟩_Q | The Heegner construction over (K₁, K₂) does not encode the off-diagonal coupling in the expected way; the correct fields or construction type must be reconsidered |

---

## PART 9 — Strongest Honest Claim

**"The next real BSD domino is whether the Heegner-side construction on K₁ = Q(√−7) and K₂ = Q(√−11) reproduces the already measured off-diagonal coupling ⟨P₁,P₂⟩ ≈ 0.05852 on 389a1 — and the exact CM points on X₀(389) are now specified: τ₁ = (−185+√−7)/(2×389) and τ₂ = (−355+√−11)/(2×389), both satisfying the Heegner hypothesis (Legendre symbols verified), with |q₁| ≈ 0.979 and |q₂| ≈ 0.974 putting the Eichler series in convergent but slowly converging territory."**

---

## PART 10 — Strongest Honest Boundary

**"What is not yet established is whether the canonical Heegner interaction over K₁K₂ is the same arithmetic object as the regulator interaction measured from rational generators, or only maps to it after trace and normalization. Specifically: we know what number the canonical construction must reproduce (0.05852265) and we know the exact CM points from which to construct y_{K₁} and y_{K₂}. What is not yet done is evaluating the modular parametrization φ at those CM points and computing the off-diagonal pairing of the resulting K₁K₂-points. That evaluation — involving the Fourier series Σ aₙ/n × qⁿ with |q| ≈ 0.98, requiring many terms of the 389a1 L-function coefficients — is the specific computation that would test whether the canonical construction hits 0.05852."**

---

## COLLABORATOR PARAGRAPH

The Heegner-pair computation is now fully specified. For E = 389a1, the two admissible fields are K₁ = Q(√−7) and K₂ = Q(√−11), each verified to satisfy the Heegner hypothesis by the Legendre symbol calculations ((7/389) = (11/389) = +1). The exact CM points on X₀(389) are τ₁ = (−185+√−7)/(778) and τ₂ = (−355+√−11)/(778), corresponding to the binary quadratic forms 389x²+185xy+22y² (disc = −7) and 389x²+355xy+81y² (disc = −11). The Eichler integral series Φ(τ_i) = Σ aₙ/n × qₙ^n converges with |q₁| ≈ 0.979 and |q₂| ≈ 0.974. The next computation is: evaluate Φ(τ₁) and Φ(τ₂) numerically using the 389a1 Fourier coefficients, apply the Weierstrass ℘-map to get y_{K₁} and y_{K₂} as algebraic numbers in K₁ and K₂, compute their traces to Q to get T₁ = n₁P₁+m₁P₂ and T₂ = n₂P₁+m₂P₂, and then compute the compositum pairing ⟨y_{K₁}, y_{K₂}⟩_{K₁K₂} and compare to 0.05852265. The comparison succeeds if the pairing scales correctly with the coefficient matrix [[nᵢ,mᵢ]].
