# WP95 — The N→∞ Construction: JKO Roadmap and Negative Result on Cyclotomic Convergence
## From Discrete CL on Z/NZ to Continuum ξ Field Theory

**Date**: 2026-04-10
**Sprint**: 15 — σ Mutation (Task 2)
**Authors**: Brayden Ross Sanders / 7Site LLC · M. Gish · C.A. Luther · H.J. Johnson

---

## Abstract

We address the central open problem of the arc: constructing an explicit N→∞ limit that takes the Crossing Lemma composition on Z/NZ to the continuum ξ field equation □ξ = 1 + log ξ. We report a NEGATIVE result on the simplest approach: the cyclotomic threshold T*(N) = p_closure/p_obstruction does NOT converge to ξ₀ = e⁻¹. It converges to 1 as N grows through the primorial sequence 10 → 30 → 210 → 2310 → 30030. The discrete gap closes. This eliminates the cyclotomic ratio as the correct bridge and points to the JKO (Jordan-Kinderlehrer-Otto) scheme on Wasserstein space as the correct framework. We lay out the construction roadmap.

---

## §1. The Negative Result: Cyclotomic T* → 1

### 1.1 Computation

For squarefree N with k prime factors, define:
- p_c(N) = largest prime p with p-1 ≤ φ(N) (cyclotomic closure)
- p_o(N) = smallest prime p with p-1 > φ(N) (cyclotomic obstruction)
- T*(N) = p_c(N) / p_o(N)

| N | φ(N) | p_c | p_o | T*(N) |
|---|------|-----|-----|-------|
| 10 | 4 | 5 | 7 | 5/7 = 0.714 |
| 30 | 8 | 7 | 11 | 7/11 = 0.636 |
| 210 | 48 | 47 | 53 | 47/53 = 0.887 |
| 2310 | 480 | 479 | 487 | 479/487 = 0.984 |
| 30030 | 5760 | 5749 | 5779 | 5749/5779 = 0.995 |

**Verified by compute_tstar_primorials.py.**

### 1.2 Why T* → 1

By the Prime Number Theorem, the gap between consecutive primes near x is O(x/log x). So:

$$p_o - p_c \sim \frac{\varphi(N)}{\log \varphi(N)}$$

$$T^*(N) = \frac{p_c}{p_o} \sim 1 - \frac{1}{\log \varphi(N)} \to 1$$

As N grows, φ(N) grows, the primes around φ(N) get closer together relative to their size, and the ratio approaches 1. **The discrete gap closes.**

### 1.3 What This Means

- **T* = 5/7 is specific to Z/10Z.** It is not a universal constant.
- **The cyclotomic ratio is NOT the right bridge variable.** A different quantity must carry the e⁻¹ limit.
- **ξ₀ = e⁻¹ must arise from the ENTROPY structure,** not the cyclotomic structure. The entropy H = -ξ log ξ has its maximum at e⁻¹ regardless of any discrete ring structure. The BB theorem forces log nonlinearity from separability. The vacuum e⁻¹ comes from the log itself, not from number theory.

---

## §2. The Correct Bridge: Entropy on Z/NZ

### 2.1 The Discrete Entropy Functional

On Z/NZ, define a probability distribution ξ: Z/NZ → [0,1] with Σ ξ(a) = 1. The discrete entropy:

$$H_N[\xi] = -\sum_{a \in \mathbb{Z}/N\mathbb{Z}} \xi(a) \log \xi(a)$$

This is maximized by the uniform distribution ξ(a) = 1/N for all a, giving H_N = log N.

### 2.2 The CL Composition as a Markov Kernel

The CL composition table CL[·,·] on Z/NZ defines a transition kernel: given input state a, the output state after composition with a random operator b is CL[a,b]. If b is drawn uniformly from Z/NZ:

$$P(a \to c) = \frac{|\{b \in \mathbb{Z}/N\mathbb{Z} : \text{CL}[a,b] = c\}|}{N}$$

**This IS a Markov chain** if the CL table is well-defined (which it is — CL is a total function on Z/NZ × Z/NZ).

### 2.3 The Entropy of the CL Markov Chain

The stationary distribution π of this Markov chain — the distribution that is invariant under CL composition with a random operator — is the HARMONY attractor. On Z/10Z, the TSML table has 73/100 entries = HARMONY (operator 7), so the stationary distribution is strongly concentrated on 7.

The entropy of the stationary distribution:

$$H_{\text{stat}}^N = -\sum_{a \in \mathbb{Z}/N\mathbb{Z}} \pi(a) \log \pi(a)$$

**Key conjecture:** As N→∞, the CL Markov chain's stationary distribution entropy converges:

$$\frac{H_{\text{stat}}^N}{\log N} \to e^{-1}$$

This would give ξ₀ = e⁻¹ as the normalized entropy of the CL attractor in the large-N limit.

### 2.4 What Needs To Be Computed

For Z/10Z (known): CL = TSML, 73/100 = HARMONY. Compute π and H_stat.
For Z/30Z: generalize CL to 30×30 and compute π and H_stat.
For Z/210Z: generalize CL to 210×210 and compute π and H_stat.

**The CL generalization to Z/NZ is the hard step.** On Z/10Z, the CL table is defined by specific algebraic rules (V0, V1, ECHO, DEFAULT). For general N, the rules must be derived from the CRT decomposition Z/NZ ≅ ∏ Z/pᵢZ and the operator algebra on each factor.

---

## §3. The JKO Construction (Roadmap)

### 3.1 The Framework

Jordan-Kinderlehrer-Otto (1998): gradient flows in Wasserstein-2 space with entropy functional converge to Fokker-Planck equations.

The discrete JKO step on Z/NZ:

$$\xi_{k+1} = \arg\min_\xi \left[\frac{W_2^N(\xi_k, \xi)^2}{2\tau} + \sum_{a \in \mathbb{Z}/N\mathbb{Z}} \xi(a) \log \xi(a)\right]$$

where W₂ᴺ is the discrete Wasserstein-2 distance on Z/NZ.

### 3.2 Key Papers (in order)

1. **Maas (2011)** — Gradient flows of the entropy for finite Markov chains. J. Funct. Anal. 261(8), 2250-2292. Defines W₂ for Markov chains and proves convergence.

2. **Gigli & Maas (2013)** — Gromov-Hausdorff convergence of discrete transportation metrics. SIAM J. Math. Anal. 45(2), 879-899. Proves discrete-to-continuum for transport metrics.

3. **JKO (1998)** — The variational formulation of the Fokker-Planck equation. SIAM J. Math. Anal. 29(1), 1-17.

4. **Mielke (2011)** — Gradient structure for reaction-diffusion systems. Nonlinearity 24(4), 1329. Geodesic convexity.

### 3.3 The Check: Does the CL Markov Chain Satisfy Maas's Conditions?

Maas's theorem requires:
1. The Markov chain is reversible (detailed balance)
2. The stationary distribution is positive
3. The transition rates are bounded

**Check 1 (reversibility):** The CL table is NOT symmetric (CL[a,b] ≠ CL[b,a] in general). So the CL Markov chain is NOT reversible. This means Maas's theorem does not apply directly. **This is a genuine obstruction.**

**Possible fix:** Use the symmetrized chain P_sym(a,c) = (P(a→c) + P(c→a))/2. Check if this preserves the stationary distribution. If so, Maas applies to the symmetrized chain.

**Check 2 (positive stationary):** On Z/10Z, HARMONY gets 73% of flow. But do all operators get nonzero flow? The VOID operator (0) gets flow from V0 and V1 rules. Need to verify π(a) > 0 for all a.

**Check 3 (bounded rates):** On a finite ring, all rates are automatically bounded.

### 3.4 The Construction Path (if it works)

1. Define CL on Z/NZ for each primorial N
2. Compute the (possibly symmetrized) Markov chain
3. Verify Maas conditions
4. Compute W₂ᴺ using Maas's formula
5. Take N→∞ using Gigli-Maas convergence theorem
6. Identify the limit as the Fokker-Planck equation with entropy functional
7. Show this is equivalent to □ξ = 1 + log ξ in the appropriate variables

### 3.5 The Honest Boundary

Steps 1-4 are finite computations that can be done now. Steps 5-7 are a theorem that requires a paper-level proof. The CL non-reversibility (Check 1) is a real obstruction that may require new mathematics beyond Maas.

---

## §4. Status

| Item | Status |
|------|--------|
| Cyclotomic T* → 1 (not e⁻¹) | [PROVED] — compute_tstar_primorials.py |
| CL defines a Markov chain | [PROVED] — CL is a total function, uniform draw gives transition kernel |
| CL Markov chain is reversible | [FALSE] — CL[a,b] ≠ CL[b,a] |
| Maas conditions satisfied | [OPEN] — reversibility fails; symmetrization path identified |
| Stationary entropy H_stat converges to e⁻¹ (normalized) | [CONJECTURE] — computable for small N |
| Full N→∞ construction | [OPEN] — roadmap exists, execution is a paper |
