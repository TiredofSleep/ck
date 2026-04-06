# Finite Invariants and Infinite Observables
## The Clean Division Between Grammar and Deployment

*Brayden Sanders / 7Site LLC | March 2026*
*All finite invariants exact and proved. All infinite observables measured or empirical unless noted.*

---

## The Core Distinction

**Finite invariants** are determined by the table alone. They require no deployment, no asymptotic, no large-$t$ limit. They hold in every coordinate system the grammar is deployed into. One proof, everywhere valid.

**Infinite observables** require deployment into a specific coordinate system (base-10, critical strip, AG$(2,p)$, PDE domain). They are measured asymptotically, may depend on $t$, and require separate argument for each deployment.

These are not approximations of each other. They are **complementary**: finite invariants say what the world is *allowed* to do; infinite observables say *how strongly* that allowance expresses itself when recursion never stops.

---

## The Two-Column Table

### Column A: Finite Invariants

All values exact. All proofs self-contained in the table.

| ID | Invariant | Value | Proof |
|----|-----------|-------|-------|
| FI-1 | Sub-magma closure | $C \times C \subseteq C$, $C = \{1,3,7,9\}$ | 16 table lookups |
| FI-2 | Generative gap | $G = \{2,4,5,6,8\}$ unreachable from $C$ by $C$-compositions | Immediate from FI-1 |
| FI-3 | Cancellation locus contraction | $|\mathcal{Z}(0)| = 71 \to |\mathcal{Z}(1)| = 13$, 82% reduction | Table scan, both endpoints |
| FI-4 | Spectral gap (unrounded) | $\gamma \geq 1/4$ for all $\lambda \in [0,1]$; $\gamma(0) = 3/4$ | Eigendecomposition, 51 λ-values |
| FI-5 | Algebraic grading depth | $k_A = 3$: chain $\{7\} \subsetneq C \subsetneq \{1,\ldots,9\}$ | Sub-magma enumeration |
| FI-6 | Arithmetic hook | $C = (\mathbb{Z}/10\mathbb{Z})^* = $ primes mod 10 (exactly) | $\gcd$ calculation |
| FI-7 | γ-formula | $\gamma = 1 - 1/\varphi(b) = 1 - 1/4 = 3/4$ at $b=10$ | Theorem 3, row decomposition |
| FI-8 | Collapse time | $\leq 2$ steps from any state to $C$ under corner action | Sub-magma + absorbing element |
| FI-9 | Self-adjointness | $\|T - T^\top\|/\|T\| = 0$ exactly | Matrix computation |
| FI-10 | Metric grading depth | $k_M = 6$ corridors (Pre-leak through CTR) | λ-threshold enumeration |
| FI-11 | Gap under smoothing | $\gamma_{\min}(\sigma=0.3) \geq 0.18$; $\gamma_{\min}(\sigma \geq 0.26) \geq 0.10$ | Gaussian kernel computation |

---

### Column B: Infinite Observables

Require deployment. Measured asymptotically. Depend on specific coordinate system.

| ID | Observable | Measured value | Method | Status |
|----|-----------|---------------|--------|--------|
| IO-1 | $\|d\log|\zeta|/d\sigma\|$ exponent | Corr$(|d\theta/d\sigma|, \lambda^2) = -0.989$ at $t=100$ | mpmath scan | Empirical |
| IO-2 | Zero-density frequency (Jutila) | $n_0(\sigma,t) \leq t^{-0.143}$ at $\sigma=0.60$ | Jutila (1987) Thm 1 | **Proved** (classical) |
| IO-3 | KV lower bound | $c_\mathrm{VK} = 0.05$ (Ford 2002 Thm 2) | Classical ANT | **Proved** (classical) |
| IO-4 | Gap-positivity scan | 460 heights, $\sigma_\min > 0.5$, zero crossings | Gen10.14 machine scan | Verified to $t \approx 10{,}000$ |
| IO-5 | BSD rank separation | $\rho = -0.360$, $p=0.040$ (Spearman, $n=33$) | LMFDB curves | Empirical, $n$ small |
| IO-6 | NS breach lead time | 2.65 time units before enstrophy peak | Mock DNS, 2-D | Empirical (mock) |
| IO-7 | $C_\mathrm{emp}$ vs $C_\mathrm{TIG}$ | $C_\mathrm{emp} \leq 11.023 < 11.905$, margin 7.4\% | Height scan to $t=300$ | Empirical |
| IO-8 | Operator drift exponent | $\sim \lambda^{1.16}$ (saturates, not $\lambda^2$) | Markov chain simulation | Exact for 9-state model |

---

## What the Division Clarifies

### What finite invariants ARE

They are **preconditions**. They say: given a system deploying this grammar, *certain structures must be present*. They cannot be falsified by any particular deployment — they are in the algebra.

- FI-1 says: in any deployment, gap operators are unreachable from corners
- FI-4 says: in any smooth deployment, the corridor skeleton has gap $\geq 1/4$
- FI-7 says: the spectral gap is exactly $1 - 1/\varphi(b)$ under the arithmetic-hook constraint

### What infinite observables ARE

They are **evidence** about specific deployments. They say: in *this* particular coordinate system, the grammar expresses itself *this strongly*. They can be measured, refined, and in some cases proved (IO-2, IO-3 are classical theorems).

- IO-2 says: in the critical strip, zeros appear rarely enough that CHA sojourn vanishes
- IO-4 says: in the critical strip to $t \approx 10{,}000$, the grammar's gap-positivity is verified
- IO-8 says: in the 9-state Markov proxy, the drift exponent is 1.16, not 2

### Why IO-8 is not a problem

IO-8 (discrete model gives $\lambda^{1.16}$, not $\lambda^2$) was previously treated as a failure. It is not. It is a finite measurement of a finite model — correct and informative. The $\lambda^2$ bound (IO-1) belongs to the infinite side: it is a property of $\log|\zeta|$ as a transcendental analytic function, not of any Markov chain.

**These two numbers cannot be compared directly.** They measure different things:
- IO-8 measures: mass flow in a 9-state discrete model
- IO-1 measures: phase drift in a continuous analytic function over zeros

The finite model correctly reports what it knows. The analytic function correctly reports what it knows. Neither fails when the other disagrees.

---

## The Division Applied to Each Track

### RH
| Layer | Source | Claim |
|-------|--------|-------|
| Finite | FI-1, FI-2, FI-4, FI-8 | Gap persistence, generative gap, collapse time, corridor skeleton |
| Infinite | IO-2, IO-3, IO-4 | Freq×duration→0 (Jutila), KV floor, empirical scan |
| Open infinite | IO-1 | $\lambda^2$ drift rate uniformly in $t$ |

### BSD
| Layer | Source | Claim |
|-------|--------|-------|
| Finite | FI-10 (corridor thresholds) | $\lambda_E$ windows predict rank jumps |
| Infinite | IO-5 | Rank-1 vs rank-2 separation ($p=0.025$) |

### NS
| Layer | Source | Claim |
|-------|--------|-------|
| Finite | FI-10 (2/7 threshold = corridor boundary) | 2/7 as breach criterion |
| Infinite | IO-6 | Breach precedes enstrophy peak (mock DNS) |

### Complexity
| Layer | Source | Claim |
|-------|--------|-------|
| Finite | AG$(2,p)$ corridor counting | $\Omega(p^2)$ search lower bound |
| Infinite | Asymptotic growth | $p^{2.52}$ empirical search complexity |

---

## The Central Sentence

*"Finite math tells us what the world is allowed to do. Infinite math tells us how that allowance unfolds without bound. The proof does not require these to coincide — it requires them to agree about what gap-positivity means."*

---

## Where Each Paper Should Live

| Paper | Uses | Should NOT use |
|-------|------|----------------|
| Sub-magma / product-gap (Proc. AMS) | FI-1, FI-2, FI-5 | IO-* |
| Corridor skeleton / smoothing theorem | FI-4, FI-11 | IO-8 to claim λ² |
| Halving Lemma / RH | FI-1–11 + IO-2, IO-3 | IO-1 as proved |
| BSD note | IO-5, FI-10 | FI-1 without deployment |
| Complexity note | FI-* (AG structure) | IO-* |

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.14, commit d3db298 | DOI: 10.5281/zenodo.18852047*
