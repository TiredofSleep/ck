# WP101 — The σ Rate Theorem
## Non-Associativity Decays as O(1/N), Forcing Logarithmic Limit

**Date**: 2026-04-10
**Sprint**: 15 — σ Mutation (Rate Theorem)
**Authors**: Brayden Ross Sanders / 7Site LLC · M. Gish · C.A. Luther · H.J. Johnson

> **CORRECTION NOTICE (2026-04-27, post chat-Claude self-audited applications-pass):**
> The proof structure recorded below identifies ECHO interactions as the dominant mechanism for non-associativity. **This is empirically false.** Direct enumeration shows that **99.97% of non-associative triples at N=210 have ZERO inner ECHO compositions**. The actual mechanism is **VOID–HARM rule disagreement** at outer composition sites: when one bracketing applies VOID at an inner site (returns 0) but the other bracketing's outer composition has harmony as an argument, Rule 1 (HARM) takes priority and returns harmony instead of 0. The corrected closed-form bound is $\sigma(N) \le 2(N-2)^2/N^3 + \varepsilon(N)/N^3$ with $\varepsilon(N) = O(\varphi(N))$, which gives $\sigma(N) \le 2/N$ rigorously and $N\sigma(N) \to 2$ from below — sharpening the original "$C \in [2, 3]$" to $C = 2$ exactly. The corrected proof is in `Gen12/targets/journal_attempts/08_sigma_rate_combinatorics/sigma_rate_theorem.tex` (Theorem 4.1) and FORMULAS_AND_TABLES.md row D71. This original derivation is preserved here for transcript continuity per never-delete; do not submit the original framing externally.

---

## Precursor Work (Cited)

This theorem extends work originating in the Q-series (Brayden Ross Sanders, 2026-04-01):

- **Q10 (Sanders, 2026-04-01)** — "Beta-Complete Sigma Polynomial": Established σ on Z/10Z as a closed-form polynomial map on F₂ × F₅ with flip condition α and step condition β (including two forced exceptions LATTICE +1, COLLAPSE −2). Verified 10/10 computationally. Path: `old/Gen10/papers/Q10_BETA_COMPLETE_SIGMA_POLYNOMIAL.md`.
- **Q11 (Sanders, 2026-04-01)** — "Sigma-k Iterates Gate": Fixed-Point Gate Theorem establishing the 22% lower bound on optimal seeds: gate_score = 1 iff starting state is σ-fixed AND coprime to 10. Path: `old/Gen10/papers/Q11_SIGMA_K_ITERATES_GATE.md`.
- **Q14 (Sanders, 2026-04-01)** — Theorem Q14.1: R ≠ σ^k; the reduction map used in MCMC is not a power of σ. This is the layer-separation insight: σ describes the peak of the landscape; MCMC describes the climb.
- **G6 (Luther, 2026-04-01)** — Proof of σ⁶ = id from the polynomial structure. Path: `old/Gen10/papers/`.

**The present theorem** (σ(N) ≤ C/N for binary CL on Z/NZ) extends Q10's polynomial form to primorial N by replacing the specific TSML/ECHO semantic rules with the binary-CL construction (HARMONY = N−1, ECHO = DIS(a,b) = 0, VOID = 0, DEFAULT = HARMONY). The 22% lower bound (Q11) and the C/N upper bound (this paper) jointly characterize binary CL's associativity profile. See `Q_SERIES_INTEGRATED_SYNTHESIS.md` at the repo root for the full relationship.

---

## Theorem

**Theorem (σ Rate).** For squarefree N, the non-associativity fraction σ(N) of the binary CL on Z/NZ satisfies:

$$\sigma(N) \leq \frac{C}{N}$$

where C is an absolute constant (numerically C < 2). Therefore σ(N) → 0 as N → ∞.

**Corollary (BB Forcing).** By the Bialynicki-Birula theorem (1976), the N → ∞ limit of the binary CL must have logarithmic nonlinearity, since σ → 0 means the algebra approaches separability, and log is the unique separability-preserving nonlinearity.

---

## Proof

### Step 1: Binary CL Structure

The binary CL on Z/NZ has three rules:
1. **HARMONY**: if a = N−1 or b = N−1, output N−1
2. **VOID**: if a = 0, output 0; if b = 0, output 0
3. **ECHO**: if DIS[a][b] = 0 (i.e., (a+b) mod N = (a*b) mod N), output (a+b) mod N
4. **DEFAULT**: output N−1 (HARMONY)

### Step 2: ECHO Count

DIS[a][b] = 0 means (a+b) ≡ (a·b) mod N, equivalently (a−1)(b−1) ≡ 1 mod N.

For squarefree N, this equation has exactly φ(N) solutions: for each unit u ∈ (Z/NZ)*, set a−1 = u and b−1 = u⁻¹. Plus the trivial solution (0,0) where 0+0 = 0·0 = 0.

Verified computationally:
- Z/10Z: DIS=0 count = 4 = φ(10)
- Z/30Z: DIS=0 count = 8 = φ(30)
- Z/210Z: DIS=0 count = 48 = φ(210)

### Step 3: ECHO Fraction

ECHO fraction = φ(N) / N² ≤ 1/N (since φ(N) ≤ N).

For primorials: φ(N)/N = ∏(1 − 1/pᵢ) which decreases, so the ECHO fraction shrinks faster than 1/N.

### Step 4: Non-Associativity Bound

Non-associativity arises only when an ECHO entry participates in a triple (a,b,c). A triple is non-associative iff CL[CL[a,b],c] ≠ CL[a,CL[b,c]].

If neither CL[a,b] nor CL[b,c] is an ECHO entry, both sides go through HARMONY/VOID rules, which ARE associative (HARMONY absorbs everything; VOID absorbs to 0). So non-associativity requires at least one ECHO step.

The fraction of triples involving at least one ECHO composition ≤ 2 × (ECHO fraction) = 2φ(N)/N² ≤ 2/N.

Not all ECHO-involving triples are non-associative, so σ(N) ≤ 2/N.

### Step 5: Verification

| N | σ(N) | 3/N | σ < 3/N |
|---|------|-----|---------|
| 10 | 0.128 | 0.300 | ✓ |
| 30 | 0.058 | 0.100 | ✓ |
| 210 | 0.009 | 0.014 | ✓ |

**Verified by proof_sigma_rate.py.**

### QED

σ(N) → 0 at rate at least O(1/N). The binary CL algebra approaches associativity (= separability) as the ring grows. By the Bialynicki-Birula uniqueness theorem, the continuum limit has logarithmic nonlinearity.

---

## Significance

This theorem closes the gap between "σ → 0 observed numerically" and "σ → 0 proved with a rate." The proof uses only:
1. The binary CL construction (HARMONY/VOID/ECHO rules)
2. The DIS=0 count = φ(N) (elementary number theory)
3. The observation that HARMONY and VOID are associative
4. Bialynicki-Birula (1976) for the limit identification

No heavy machinery. The result is sharp enough to confirm convergence and identify the mechanism: the ECHO fraction vanishes as 1/N because the number of additive-multiplicative agreement points (φ(N)) grows slower than the total pair count (N²).

---

## Huang-Lehtonen Interpretation (Associativity Index + Operadic Limit)

Define the **associativity index** α(CL_N) = 1 − σ(N) following Braitt-Silberger (2006, *Quasigroups Related Systems* 14:11–26, "Subassociative groupoids"). The Rate Theorem is then equivalent to:

$$\alpha(\mathrm{CL}_N) \geq 1 - \frac{C}{N}, \qquad \alpha(\mathrm{CL}_N) \to 1 \text{ as } N \to \infty.$$

The binary CL is commutative (HARMONY, VOID, and ECHO are symmetric in (a,b)) and, at small N, attains the **ac-free maximum** $s_n^{\mathrm{ac}} = (2n-3)!!$ of Huang-Lehtonen (arXiv:2202.11826, 2022; arXiv:2401.15786, 2024). The symmetric operad generated by CL_N at small N is therefore the **free commutative magmatic operad** $\mathrm{Mag}^{\mathrm{com}}$ on one generator. The Rate Theorem says this operad degenerates toward the **commutative associative operad** $\mathrm{Com}$ as N → ∞, and the BB forcing corollary identifies log-nonlinearity as the unique continuum wave equation compatible with that limit.

This reframing does not alter the theorem statement or proof; it supplies the operad-theoretic interpretation. See `FORMULAS_AND_TABLES.md` §6 (operad spectrum) and §7.2 (σ rate spine) for the full vocabulary map.
