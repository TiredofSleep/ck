# TIG in the Landscape of Bridge Formalisms
## Exact Placement: What Each Framework Provides and What It Misses

*Brayden Sanders / 7Site LLC | March 2026*
*Classification: §1–4 structural identification (proved). §5 synthesis (heuristic). No overclaiming.*

---

## The Synthesis Stack

The five existing bridge formalisms each solve *part* of the finite-to-infinite problem. The correct stack for TIG is:

```
Finite grammar:    Subshift of finite type (absorbing sofic shift)
Persistence layer: Transfer operator + Perron-Frobenius
Reset structure:   Young tower (exponential return tails)
Arithmetic hook:   Inverse limit (profinite, 10-adic)
Faithfulness test: Deployment question (open, maps to RH)
```

These are not competing frameworks. Each occupies a different layer.

---

## 1. Symbolic Dynamics and Subshifts of Finite Type

**What TIG is in this language:**
An *absorbing sofic shift* — not a standard irreducible SFT but an SFT with an absorbing component.

The transition matrix $A$ on $\{1,\ldots,9\}$ is NOT strongly connected: all paths eventually enter $C = \{1,3,7,9\}$, which is absorbing. The correct framing is:

- **Transient component:** $G \cup (C \setminus \{\mathrm{HAR}\})$ — states that flow toward the absorbing class
- **Absorbing component:** $\{\mathrm{HAR}\}$ — the unique global attractor
- The restriction $A|_C$ has $\mathrm{HAR}$ as a fixed point; non-HAR corners in $C$ flow back to $\mathrm{HAR}$ in $\leq 1$ step

**What SFT theory provides:**
- Language of forbidden words: the forbidden set is $\mathcal{F} = \{(s,t) : A[s][t] = 0\}$
- Entropy: $h = \log \rho(A)$ where $\rho(A)$ is the spectral radius
- Zeta function: $\zeta_{SFT}(z) = \exp(\sum_n |\mathrm{Fix}(\sigma^n)| z^n/n)$

**What SFT theory misses:**
- The deformation family $\{F_\lambda\}$ — SFT is a single fixed grammar, not a parameterized family
- The arithmetic hook — SFT works over abstract alphabets, not integer-valued ones
- The two-grading structure — SFT has one transition rule, not an algebraic chain + metric stratification

**TIG's contribution to SFT:** An absorbing sofic shift where the absorbing component is algebraically distinguished (it is the unit group of the deployment base). This is a specific sub-class of SFTs not usually studied in symbolic dynamics.

---

## 2. Transfer Operators and Perron-Frobenius Theory

**What TIG is in this language:**
A *primitive stochastic matrix* (the unrounded $P_{\lambda,0+}$ family) with unique stationary measure and spectral gap $\gamma \geq 1/4$ uniformly over $\lambda$.

- TSML is self-adjoint: $\|T - T^\top\|/\|T\| = 0$ (exact)
- Transfer operator $P$ has spectral gap $= 3/4$ at $\lambda=0$ (exact, Theorem 3)
- The deformation family $\{P_\lambda\}$ is the correct continuous generalization

**What transfer operator theory provides:**
- Decay of correlations: $|\mathrm{Cor}(f \cdot g \circ P^n)| \leq C \cdot \gamma^n \|f\|_V \|g\|_\infty$
- Invariant measures: unique stationary distribution, approached at rate $\gamma^n$
- Functional-analytic framework: Baladi (2000), Gouëzel-Liverani (2006)

**What transfer operator theory misses:**
- The arithmetic hook — transfer operators work over abstract state spaces
- The deformation family structure — standard theory handles fixed operators
- The RH connection — requires identifying the critical-strip operator with $P_\lambda$

**TIG's contribution to transfer operator theory:** A one-parameter family of transfer operators with uniform spectral gap, arising from an algebraic deformation (closure → order) with explicit arithmetic interpretation. This is a structured family, not a generic perturbation.

---

## 3. Young Towers and Inducing Schemes

**What TIG is in this language:**
A Young tower with *exponential return tails*.

- Base: $\{\mathrm{HAR}\}$ — the reset puncture
- Return time distribution: $P(T_\mathrm{HAR} > n) \leq (1/4)^n$ (tail rate = spectral radius of $Q = 0.25$)
- Expected return times: all states return to HAR in $\leq 1.67$ steps expected (exact Markov computation)
- Tower is *finite height*: max return time $= 2$ under optimal corner sequence

**What Young tower theory provides:**
- Exponential mixing: follows from exponential return tails (Young 1999, Thm 1)
- Invariant measure: Lebesgue-absolutely-continuous (for piecewise-expanding maps)
- CLT and other limit theorems: standard Young tower consequences

**What Young tower theory misses:**
- Discrete alphabet (Young towers are for measure-preserving maps on intervals)
- The deformation parameter $\lambda$
- The graded corridor structure — Young towers have a single base, not six levels

**TIG's contribution to Young tower theory:** A Young tower where the base is algebraically defined (the absorbing fixed point of a magma) rather than geometrically defined (a distinguished interval). The return time is exactly 1 or 2 steps (finite height tower), giving exponential tails with explicit rate $r = 1/4$.

---

## 4. Inverse Limits and Profinite Structures

**What TIG is in this language:**
A *profinite/10-adic arithmetic structure* — the corner set $C = \{1,3,7,9\}$ is the stable image of the inverse limit:
$$\cdots \to (\mathbb{Z}/10^3\mathbb{Z})^* \to (\mathbb{Z}/10^2\mathbb{Z})^* \to (\mathbb{Z}/10\mathbb{Z})^*$$

At every level $n$, units mod 10 $= \{1,3,7,9\}$. The arithmetic hook is the $n=1$ level of this tower; the infinite deployment is $n \to \infty$ (the 10-adic integers).

**What inverse limit theory provides:**
- Exact algebraic data preserved across levels: $C$ is stable at every level
- Profinite completion: $\hat{\mathbb{Z}}_{10} = \varprojlim \mathbb{Z}/10^n\mathbb{Z}$
- Base-change: same corner set in all deployments with $\varphi(b) = 4$

**What inverse limit theory misses:**
- Dynamics (inverse limits are algebraic, not dynamical)
- Spectral gap (no transfer operator in the profinite setting)
- The metric grading — the corridor structure does not arise from the profinite structure

**TIG's contribution to inverse limit theory:** An inverse limit structure where the arithmetic hook ($C = $ unit group) is paired with a dynamical grammar (TSML composition). The algebraic and dynamical structures coexist in the same object.

---

## 5. What TIG Adds Beyond Each Framework

| Framework | TIG fits as | What TIG adds |
|-----------|-------------|---------------|
| Subshift of SFT | Absorbing sofic shift | Deformation family + two grading structure |
| Transfer operators | Primitive stochastic family | Arithmetic hook + γ-formula $1 - 1/\varphi(b)$ |
| Young towers | Finite-height tower, base = HAR | Algebraically-defined base + six corridor levels |
| Inverse limits | 10-adic unit group | Dynamical grammar paired with algebraic structure |

None of the four frameworks individually contains all of TIG. The synthesis stack uses all four layers:

```
Absorbing sofic shift       → provides the finite grammar
  ↓ Perron-Frobenius        → provides the spectral gap and mixing
    ↓ Young tower           → provides the return structure and exponential tails
      ↓ Inverse limit       → provides the arithmetic hook and base-change stability
        ↓ Deployment test   → provides the faithfulness question (open, = RH for the ζ-deployment)
```

---

## 6. The Classification Problem in This Language

**In SFT language:** Classify absorbing sofic shifts by their (algebraic grading, metric grading, spectral gap) type.

**In transfer operator language:** Which structured families $\{P_\lambda\}$ have uniform spectral gap and a γ-formula arising from arithmetic constraints?

**In Young tower language:** Which algebraically-defined bases (unit groups of arithmetic rings) give finite-height towers with explicit return rates?

**In inverse limit language:** For which inverse systems does the profinite structure pair with a dynamical grammar with spectral gap $1 - 1/\varphi$?

These are the same question from four different viewpoints. TIG is a specific answer to all four simultaneously.

---

## The Defensible Claim

*The TIG type-$(n, k_A, k_M, \gamma)$ grammar identifies a common synthesis problem that existing bridge theories each solve only partially. The correct host is the stack: absorbing sofic shift + transfer operator family + finite-height Young tower + profinite arithmetic hook. TIG is a specific instance of this stack at $n=9$, $k_A=3$, $k_M=6$, $\gamma=3/4$.*

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.14, commit d3db298 | DOI: 10.5281/zenodo.18852047*
