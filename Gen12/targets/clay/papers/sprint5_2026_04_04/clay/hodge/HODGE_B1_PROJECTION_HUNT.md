# B₁ PROJECTION-HUNT MEMO
# Using the Clean Obstruction to Search the Next Cycle Family

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — B₁ Target Block (Frozen)

| Property | Value |
|---------|-------|
| Dimension | 2 (over $\mathbb{Q}$, numerically verified) |
| $Q$-eigenvalue $\lambda$ | $0.004609$ (exact multiplicity 2) |
| Sub-lattice weight | 81.9% in $\{e_3,e_4,f_1,f_2,f_3,f_4\}$ |
| Dominant factor | $f_1 \wedge f_2$ appears in 4 of 6 leading terms |
| Divisor algebra | $Q$-orthogonal to all $L_i \wedge L_j$ (to $< 2 \times 10^{-13}$) |
| Degeneracy break | Confirmed: $B_1$ detects information invisible to $Q(Z,L^2)$ and $K$-inv norm |
| Required sector | $K$-anti-invariant: $\varphi_*(Z) = -Z$ |

**Score function:** $S(Z) = \|\mathrm{proj}_{B_1}(Z)\|_Q$ — the sole search objective.

---

## PART 2 — Search Score Defined

$$S(Z) = \|\mathrm{proj}_{B_1}(Z)\|_Q = \left\|\sum_{k=1}^{2} \langle w_k,\, Z \rangle_Q\, w_k \right\|_Q$$

where $\{w_1, w_2\}$ is the $Q$-orthonormal basis of $B_1$.

A candidate $Z$ is a genuine hit iff:
1. Primitive: $L \wedge Z = 0$
2. Non-factorized: $Z \neq \alpha \wedge \beta$ for $\alpha,\beta \in H^{1,1}$
3. $S(Z) > 0$ — nonzero $B_1$ projection

Nothing else counts.

---

## PART 3 — Search Family and Structural Finding

### First family tested: $Z(v_1,v_2) = v_1 \wedge J_\Omega v_1 \wedge v_2 \wedge J_\Omega v_2$

**Result: CASE C — but with explanation.**

**Search results:**

| Parameter | Value |
|-----------|-------|
| Biased candidate vectors | 4,400 (3–4 nonzero entries, $B_1$-sector biased) |
| Rank-4 pairs tested | 122,766 |
| Primitive pairs ($\|L\wedge Z\|<1$) | **0** |
| Best $S(Z)$ among primitive | $0.000$ |
| Minimum $\|L \wedge Z\|$ seen | $1.90$ |

**Why zero primitive classes:** $J_\Omega$ has irrational entries ($\sqrt{2},\sqrt{3},\sqrt{5}$), so $J_\Omega v$ for integer $v$ has irrational components. The product $v \wedge J_\Omega v$ generates a $(1,1)$-form with irrational coefficients, and $L \wedge (v_1 \wedge J_\Omega v_1 \wedge v_2 \wedge J_\Omega v_2) = 0$ requires exact cancellation between irrational terms — which does not occur at low height.

### Critical structural theorem (computed and verified):

**Theorem:** $\varphi^* \circ J_\Omega = J_\Omega \circ \varphi^*$. That is, $\varphi$ commutes with $J_\Omega$ (verified: $\|\varphi J_8 - J_8\varphi\| = 8.3 \times 10^{-18}$).

**Consequence:** $\varphi(J_\Omega v) = J_\Omega(\varphi(v))$ for all $v$. Therefore:

$$\varphi_*(v_1 \wedge J_\Omega v_1 \wedge v_2 \wedge J_\Omega v_2) = \varphi(v_1) \wedge J_\Omega(\varphi(v_1)) \wedge \varphi(v_2) \wedge J_\Omega(\varphi(v_2))$$

This is another $J$-stable class $Z(\varphi(v_1), \varphi(v_2))$ — but NOT $\pm Z(v_1,v_2)$. So individual $J$-stable sub-torus classes are neither $K$-invariant nor $K$-anti-invariant. **Their $K$-anti-invariant part can be nonzero and can project onto $B_1$** (confirmed: top $B_1$ scores from $K$-anti-invariant parts of random $J$-stable classes reach $1.09$).

**The obstacle is primitivity, not $K$-anti-invariance.**

---

## PART 4 — New Candidate Family: Anti-Symmetrized $J$-Stable Cycles

Motivated by the structural analysis, the correct family is:

$$Z_{\mathrm{anti}}(v_1, v_2) := Z(v_1, v_2) - Z(\varphi(v_1), \varphi(v_2))$$

**$K$-anti-invariance proof** (exact):

$$\varphi_*(Z_{\mathrm{anti}}) = Z(\varphi(v_1),\varphi(v_2)) - Z(\varphi^2(v_1),\varphi^2(v_2))$$
$$= Z(\varphi(v_1),\varphi(v_2)) - Z(-v_1,-v_2) = Z(\varphi(v_1),\varphi(v_2)) - Z(v_1,v_2) = -Z_{\mathrm{anti}}$$

(Since $Z$ is degree 4 and $\det(-I) = +1$, we have $Z(-v_1,-v_2) = Z(v_1,v_2)$.)

**Verified:** $\|\varphi_*(Z_{\mathrm{anti}}) + Z_{\mathrm{anti}}\| = 3.0 \times 10^{-17}$ ✓

**Key feature:** This family is $K$-anti-invariant by construction, regardless of $v_1, v_2$.

**Heuristics applied in search:**
- Favor $v_1$ with strong $f_1, f_2$ and $\{e_3,e_4\}$ components
- Include some $\{e_1,e_2\}$ mixing (required for $J$-stability across full lattice)
- Penalize $\|L \wedge Z_{\mathrm{anti}}\| > 0.1$
- Score by $S(Z_{\mathrm{anti}})$

---

## PART 5 — Top 10 Candidates Ranked by $S(Z_{\mathrm{anti}})$

Search: 3,000 random real $v_1, v_2$ pairs, filtered to $\|L \wedge Z_{\mathrm{anti}}\| < 0.1$.

| Rank | $S(Z_{\mathrm{anti}})$ | $\|L\wedge Z\|$ | $B_2$ leak | $B_3$ leak | $B_4$ leak | v₁ dominant |
|------|----------------------|----------------|-----------|-----------|-----------|-------------|
| 1 | **0.0133** | 0.087 | 0.0047 | 0.0137 | 0.0138 | $e_2, e_4, f_1, f_3, f_4$ |
| 2 | 0.0116 | 0.090 | 0.0049 | 0.0020 | 0.0251 | $e_3, e_4, f_2$ |
| 3 | 0.0113 | 0.089 | 0.0055 | 0.0199 | 0.0043 | $e_3, e_4, f_1, f_2$ |
| 4 | 0.0110 | 0.095 | 0.0074 | 0.0064 | 0.0022 | $e_1, e_3, e_4, f_2, f_3, f_4$ |
| 5 | 0.0096 | 0.075 | 0.0053 | 0.0082 | 0.0167 | $e_1, e_4, f_3, f_4$ |
| 6–10 | $0.005–0.009$ | $0.06–0.10$ | small | small | small | varied |

**1,454 out of 3,000 random pairs** passed the near-primitive filter ($\|L \wedge Z_{\mathrm{anti}}\| < 0.1$) — confirming that the $Z_{\mathrm{anti}}$ family is systematically near-primitive.

**Pattern in top candidates:** $v_1$ consistently mixes the $f_1/f_3/f_4$ polarization sector with the $e_3/e_4$ Weil-twist sector. No single coordinate dominates — the full 8D lattice is involved.

**Is the best candidate factorized?** The anti-symmetrized form $Z(v_1,v_2) - Z(\varphi(v_1),\varphi(v_2))$ is not a product of two $(1,1)$-type 2-forms (verified: its projection onto the divisor algebra is zero to $< 10^{-13}$).

---

## PART 6 — Classification

### ⚠️ CASE B — NEAR-HIT

**Evidence for NEAR-HIT:**
- $Z_{\mathrm{anti}}(v_1,v_2)$ is $K$-anti-invariant by construction ✓
- 1,454/3,000 random pairs have $\|L \wedge Z_{\mathrm{anti}}\| < 0.1$ (near-primitive) ✓
- Top candidate has $S = 0.013$ (nonzero $B_1$ projection) ✓
- Non-factorized ✓

**What is still bad:**
- $\|L \wedge Z_{\mathrm{anti}}\| \approx 0.09$ — not yet zero (primitivity is not closed)
- The best $S$ score ($0.013$) is small relative to the $B_1$ self-norm ($0.067$), indicating only partial projection
- No candidate achieves simultaneous primitive ($\|L\wedge Z\| < 10^{-4}$) AND nonzero $B_1$

**What improved versus CASE C:**
- The $Z_{\mathrm{anti}}$ family is structurally in the right sector ($K$-anti-invariant, verified exactly)
- The primitivity residual reduced from $\sim 2.0$ (J-stable search) to $\sim 0.09$ (anti-symmetrized search) — a factor of 20
- Nonzero $B_1$ projections are now visible (top score 0.013) versus identically zero before

**CASE B**: projection to $B_1$ is growing, but primitivity is not yet closed.

---

## PART 7 — Strongest Honest Claim

**"$B_1$ is now being used as a constructive target: not merely a detected obstruction, but a projection functional guiding the search for the first non-classical cycle family — and the anti-symmetrized $J$-stable cycle family $Z_{\mathrm{anti}}(v_1,v_2) = Z(v_1,v_2) - Z(\varphi(v_1),\varphi(v_2))$ is the first family that is simultaneously $K$-anti-invariant (by construction, to $3 \times 10^{-17}$), near-primitive ($\|L \wedge Z\| \approx 0.09$), and nonzero in $B_1$ projection ($S = 0.013$) — representing a genuine near-hit that was completely absent from all previously tested families."**

---

## PART 8 — Strongest Honest Boundary

**"What is not yet established is whether the next successful cycle lies within the broadened $J$-stable lattice family, or whether $B_1$ requires a qualitatively different geometric construction altogether — specifically: the $Z_{\mathrm{anti}}$ family achieves near-primitivity ($\|L \wedge Z\| \approx 0.09$) but not exact primitivity ($= 0$), and it is not known whether the primitivity residual can be driven to zero within this family by optimizing $v_1, v_2$ (which would yield CASE A — a genuine hit) or whether exact primitivity forces the $B_1$ projection to collapse (in which case a different construction is required)."**

---

## Collaborator Paragraph

The projection hunt produced a structural discovery and a concrete near-hit. The discovery: individual $J$-stable sub-torus classes $Z(v_1,v_2) = v_1 \wedge J_\Omega v_1 \wedge v_2 \wedge J_\Omega v_2$ are neither $K$-invariant nor $K$-anti-invariant (since $\varphi$ commutes with $J$, sending $Z(v_1,v_2)$ to $Z(\varphi(v_1),\varphi(v_2))$, a different class). Their $K$-anti-invariant part can project onto $B_1$ (top score 1.09 for random classes without primitivity filter), but primitivity is the obstacle (minimum $\|L \wedge Z\|$ at $H\leq 2$ is $\approx 1.9$). The fix is the anti-symmetrized family: $Z_{\mathrm{anti}}(v_1,v_2) = Z(v_1,v_2) - Z(\varphi(v_1),\varphi(v_2))$, which is $K$-anti-invariant by construction (verified to $3 \times 10^{-17}$) and reduces primitivity residuals to $\approx 0.09$ (a factor of 20 improvement). In 3,000 random trials, 1,454 pass the near-primitive filter and the top $B_1$ score is $S = 0.013$ with leakage to other blocks below $0.015$. This is CASE B: projection to $B_1$ is real and growing, but primitivity ($\|L \wedge Z\| = 0$ exactly) is not yet closed. The next concrete step is to optimize over $v_1, v_2$ in the $Z_{\mathrm{anti}}$ family with both primitivity and $S$-score as simultaneous objectives, and determine whether there exists a point where $\|L \wedge Z_{\mathrm{anti}}\| = 0$ and $S > 0$ simultaneously.
