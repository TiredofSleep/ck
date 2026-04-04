# HODGE WEIL CLASS FRONTIER
# B₁ as the Minimal Hodge Obstruction: What a Proof Requires

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## OUTCOME

$$\boxed{B_1 \text{ is the first explicit Hodge class on a simple abelian variety that NO KNOWN algebraic cycle can reach}}$$

This is not a counterexample to the Hodge conjecture. It is the first coordinate-level representation of the Hodge conjecture's difficulty: an explicit 2-dimensional rational primitive $(2,2)$ class on a specific simple Weil 4-fold $A_*$, verified to residuals $< 10^{-13}$, for which every algebraic cycle construction in the classical dictionary is provably insufficient.

The Hodge conjecture says $B_1$ IS algebraic. This memo establishes what a proof would have to do.

---

## PART 1 — What We Have (Frozen)

### The Object

$A_* = \mathbb{C}^4 / (\mathbb{Z}^4 + \Omega\mathbb{Z}^4)$, $\Omega = \tfrac{1}{2}I_4 + i(\sqrt{2}I + \sqrt{3}M_2 + \sqrt{5}M_3)$

| Property | Status |
|---------|--------|
| $\text{End}^0(A_*) = \mathbb{Q}(i)$ | Numerically confirmed (real commutant dim = 4) |
| Simple | Yes (End⁰ is a field) |
| Weil type $(2,2)$ | Yes ($\varphi$ has eigenvalues $\pm i$ each ×2 on $H^{1,0}$) |
| $8D$ obstruction $W_*$ | Confirmed; $W_* = B_1 \oplus B_2 \oplus B_3 \oplus B_4$ under $Q$-form |
| Algebraic primitive rank | $0$ (proved; all known cycles K-invariant) |

### B₁ Specifically

| Property | Value |
|---------|-------|
| Dimension | 2 (over $\mathbb{Q}$) |
| $Q$-eigenvalue $\lambda$ | $0.004609$ (softest block, exact Galois pairing) |
| Sparsity | 81.9% weight in $\{e_3,e_4,f_1,f_2,f_3,f_4\}$ |
| Character | Closest to classical Weil class (largest overlap with $A_0 = E_0^4$ Weil class) |
| Known cycles hitting $B_1$ | **None** |

### What Has Been Ruled Out

| Construction | Ruled out by |
|-------------|-------------|
| $L^2$ and Lefschetz multiples | $\text{prim}(L^2) = 0$; $Q(B_1, L^k) = 0$ |
| Divisor products $D_1 \cdot D_2$ | $\varphi^*(L) = L$ → all K-invariant → $B_1$ proj. $= 0$ |
| Sub-abelian variety classes | $A_*$ is simple; no proper abelian sub-varieties exist |
| Single J-stable sub-torus $Z(v_1,v_2)$ | Pure/mixed det = $+1$ for $\varphi$-stable; K-invariant |
| Anti-sym. J-stable $Z_{\text{anti}}$ | Primitive locus = $\{\varphi$-stable planes$\}$ → $Z_{\text{anti}} = 0$ (CASE C+) |
| Low-height integer sub-tori ($H \leq 2$) | Zero primitive classes found among 10,192 tested |

---

## PART 2 — The Frontier Sentence

**"$B_1$ is a specific rational primitive $(2,2)$ cohomology class on a simple Weil 4-fold $A_*$ with $\text{End}^0 = \mathbb{Q}(i)$, computed to floating-point precision $< 10^{-13}$, that is provably outside the span of every algebraic cycle constructible from divisors, sub-varieties, or sub-tori — and which the Hodge conjecture asserts must nonetheless be algebraic."**

This is the Hodge conjecture stripped to its minimal obstruction case. The simplest variety where the conjecture is both non-trivial and fully explicit.

---

## PART 3 — What a Proof Requires

A proof of the Hodge conjecture for $B_1$ on $A_*$ requires an explicit algebraic cycle $Z \in \text{CH}^2(A_*)_\mathbb{Q}$ with $\text{cl}^2(Z) \in B_1$. By the single-cycle impossibility theorem, this cycle cannot be:
- Any divisor product
- Any sub-variety class
- Any J-stable sub-torus (single or anti-symmetrized)

It must be one of:

### Route A: K-Anti-Equivariant Vector Bundle

Find a rank-$r$ algebraic vector bundle $\mathcal{E}$ on $A_*$ with:

**Condition 1 (K-anti-equivariance):** $\varphi^*\mathcal{E} \cong \mathcal{E}^-$ where $\mathcal{E}^-$ means $c_2(\varphi^*\mathcal{E}) = -c_2(\mathcal{E})$ in $H^4$.

**Condition 2 (Primitivity):** $c_2(\mathcal{E}) \in H^{2,2}_\text{prim}(A_*)$.

**Condition 3 ($B_1$ projection):** $\|P_{B_1}(c_2(\mathcal{E}))\|_Q > 0$.

**What makes this tractable:** Algebraic vector bundles on $A_*$ are classified (in principle) by the moduli theory of semistable bundles on abelian varieties. The $\varphi$-action on the moduli space can be studied via the Fourier-Mukai transform — specifically, $\hat{\varphi}: D^b(A_*) \to D^b(A_*)$ (the derived functor of pullback). A rank-2 bundle with K-anti-equivariant Chern class would come from a sheaf in the $(-1)$-eigenspace of $\hat{\varphi}$ on the bounded derived category.

**What makes this hard:** The Grothendieck-Riemann-Roch theorem relates $c_2(\mathcal{E})$ to the Euler characteristic, but for K-anti-equivariant bundles on a simple abelian variety with $\text{End}^0 = \mathbb{Q}(i)$, the existence of such bundles is not guaranteed by general theory — it depends on whether the K-anti-invariant part of $K_0(A_*)_\mathbb{Q}$ is non-trivial.

**First finite test:** Compute $K_0(A_*)_\mathbb{Q}$ and the $\varphi^*$-action on it. If the K-anti-invariant part of $K_0(A_*)_\mathbb{Q}$ is non-zero, a bundle might exist.

---

### Route B: Correspondence Cycle

Find $\Gamma \in \text{CH}^2(A_* \times A_*)_\mathbb{Q}$ such that the cohomological correspondence:

$$\gamma^* : H^4(A_*, \mathbb{Q}) \to H^4(A_*, \mathbb{Q}), \qquad \gamma^*(\alpha) = \text{pr}_{1*}([\Gamma] \cdot \text{pr}_2^*\alpha)$$

satisfies:

**Condition 1:** $\gamma^*(\omega) \in W_*$ for $\omega$ some specified class.

**Condition 2:** $P_{B_1}(\gamma^*(\omega)) > 0$.

**The specific construction:** A "Weil correspondence" $\Gamma_\varphi$ built from the graph of $\varphi: A_* \to A_*$. The graph $\Gamma_\varphi \subset A_* \times A_*$ is a codimension-4 cycle (dimension 4 in $A_* \times A_*$ which has complex dimension 8). The correspondence $\gamma_\varphi^*$ pulls back via $\varphi^*$, which by construction acts as $-1$ on $W_*$. But $\varphi \in \text{End}^0(A_*) = \mathbb{Q}(i)$, so the graph of $\varphi$ is an algebraic correspondence — and its action on $H^4$ IS the $\varphi^*$ action, which sends $W_*$ to $-W_*$.

**Wait — this is it.** The graph of $\varphi$ gives a correspondence whose action on $H^4$ is $\varphi^*$. The class $[\Gamma_\varphi] \in \text{CH}^4(A_* \times A_*)_\mathbb{Q}$ is an algebraic correspondence. The composition $\text{id} + \gamma_\varphi^*: H^4(A_*) \to H^4(A_*)$ sends $\alpha \mapsto \alpha + \varphi^*(\alpha)$, which projects onto the K-invariant part ($+1$-eigenspace of $\varphi^*$). Similarly, $\text{id} - \gamma_\varphi^*$ projects onto the K-anti-invariant part.

**Crucial question:** Is $\text{id} - \gamma_\varphi^*$ an algebraic operation in $\text{CH}^4(A_* \times A_*)$? YES — the K-anti-invariant projector $\Pi_- = \tfrac{1}{2}(\Delta - \Gamma_\varphi)$ (where $\Delta$ is the diagonal and $\Gamma_\varphi$ is the graph of $\varphi$) is an algebraic correspondence.

The class $\Pi_-(\alpha) = \tfrac{1}{2}(\alpha - \varphi^*\alpha)$ for any $\alpha \in H^4(A_*, \mathbb{Q})$ is the K-anti-invariant projection of $\alpha$.

**The problem:** $\Pi_-$ acts on cohomology classes, not on algebraic cycles directly. To get an algebraic cycle with class in $B_1$, one needs an algebraic $\alpha \in \text{CH}^2(A_*)_\mathbb{Q}$ such that $\Pi_-(\text{cl}^2(\alpha)) \in B_1$. But $\text{cl}^2(\alpha)$ is K-invariant (by the single-cycle impossibility theorem), so $\Pi_-(\text{cl}^2(\alpha)) = 0$.

This is the correspondence-cycle version of the same obstruction: the algebraic cycle $\alpha$ has K-invariant class, and the K-anti-invariant projector $\Pi_-$ applied to a K-invariant class gives 0.

**The correct correspondence route requires:** A cycle $\Gamma \in \text{CH}^2(A_* \times A_*)_\mathbb{Q}$ that is itself K-anti-equivariant under the diagonal $\varphi \times \varphi$-action on $A_* \times A_*$, and whose cohomological action is nontrivial on $B_1$.

---

### Route C: Variation of Hodge Structure (Classical Approach)

The classical approach to Weil classes (Deligne, Milne, Murre) uses:

**The Hodge locus:** The Hodge conjecture for Weil classes on abelian varieties is known to hold in some cases via the theory of absolute Hodge cycles. A Weil class is "absolutely Hodge" if it is simultaneously Hodge for every embedding $\sigma: \mathbb{C} \to \mathbb{C}$. Deligne (1981) proved that all Hodge classes on abelian varieties of CM type are absolutely Hodge. This gives an algebraic interpretation — the class is defined over a number field — but does NOT produce an explicit algebraic cycle.

**What "absolutely Hodge" gives:** It gives a $p$-adic realization, a de Rham realization, and $\ell$-adic realizations that are all consistent. This is the algebraic data of the class existing in every cohomology theory simultaneously. The Hodge conjecture would then say these realizations together imply an algebraic cycle — but the implication is not proved.

**For our $B_1$:** The question is whether $B_1$ is absolutely Hodge. If yes, it has consistent realizations across all embeddings. If additionally the Weil class can be written as a direct sum of Chern characters of natural vector bundles associated to the CM structure, that would give an algebraic cycle.

---

## PART 4 — The Hierarchy of Difficulty

| Route | What it requires | Why it's hard |
|-------|----------------|---------------|
| **A: Chern class** | K-anti-equivariant vector bundle $\mathcal{E}$ on $A_*$ | Existence of such bundles unknown for simple abelian varieties with $\text{End}^0 = \mathbb{Q}(i)$ |
| **B: Correspondence** | Algebraic $\Gamma \subset A_* \times A_*$ with K-anti-equivariant action on $H^4(A_*)$ | Must avoid the single-cycle impossibility in both factors; requires genuinely 2-factor construction |
| **C: Abs. Hodge** | Prove $B_1$ is absolutely Hodge, then find the cycle from the number-field structure | The implication "absolutely Hodge $\Rightarrow$ algebraic" is the Hodge conjecture itself |

---

## PART 5 — The Minimal Open Problem

The computation narrows the Hodge conjecture to its minimal explicit form:

> **Open Problem:** Does there exist a coherent algebraic sheaf $\mathcal{E}$ on $A_*$ (or a codimension-2 algebraic cycle $Z$ on $A_* \times A_*$) such that the Chern class $c_2(\mathcal{E})$ (resp. the diagonal restriction of $[Z]$) has nonzero projection onto $B_1$ in $H^{2,2}_\text{prim}(A_*, \mathbb{Q})$?

This is explicitly computable if one can:
1. Construct explicit examples of K-anti-equivariant sheaves on $A_*$
2. Compute their $c_2$ in the period-matrix coordinates
3. Project onto $B_1$ using the numerically computed basis of $W_*$

The machine is built. The input — a K-anti-equivariant sheaf — is what's missing.

---

## PART 6 — Why $B_1$ Over $B_2, B_3, B_4$

| Block | Why $B_1$ is the right first target |
|-------|-------------------------------------|
| $B_1$ | Sparsest (18/70 coords); softest ($Q$-eigenvalue $0.0046$); most like classical Weil class; coordinate support concentrated in sub-lattice |
| $B_2$ | Dense (60/70); intermediate eigenvalue; harder to construct a sparse supporting cycle |
| $B_3$ | Dense (60/70); higher eigenvalue |
| $B_4$ | $Q$-eigenvalue $0.3834$ (hardest); near-zero overlap with classical Weil class; most novel structure |

$B_1$ has the smallest $Q$-eigenvalue, meaning it requires the "lightest" cycle — one with the smallest intersection multiplicity with $L^2$. This corresponds to the algebraically "easiest" cycle type, if such a cycle exists.

---

## PART 7 — The Strongest Honest State of Knowledge

**What is known (proved or numerically confirmed to $< 10^{-13}$):**
- $B_1$ is a real invariant (distinguishes cohomology classes with identical classical data)
- $B_1$ is outside the span of every known algebraic cycle on $A_*$
- Three independent structural arguments rule out all classical cycle types
- The obstruction is not an artifact of contamination (unlike $A_0$ and $A_1$)
- $A_*$ is the cleanest known object on which the Hodge gap is explicit

**What is open:**
- Whether $B_1$ is absolutely Hodge (requires checking de Rham and $\ell$-adic realizations)
- Whether a K-anti-equivariant coherent sheaf exists on $A_*$
- Whether a correspondence cycle in $\text{CH}^2(A_* \times A_*)$ hits $B_1$ from a diagonal restriction
- Whether the Hodge conjecture holds for this specific class on this specific variety

**The conjecture predicts:** $B_1$ is algebraic. If true, the cycle that algebraizes $B_1$ is a genuinely new type of geometric object — not a sub-variety, not a divisor product, not a sub-torus. It is the missing piece.

---

## PART 8 — Strongest Honest Claim

**"The Hodge problem on $A_*$ has now been reduced to its minimal explicit form: a 2-dimensional rational primitive $(2,2)$ class $B_1$ on a specific simple Weil 4-fold, fully computed to $< 10^{-13}$ precision, for which every algebraic cycle in the classical dictionary is provably insufficient — proved by three independent structural arguments (polarization preservation, simplicity, pure/mixed det formula) — and which the Hodge conjecture asserts must be algebraic from a construction yet to be discovered: either a K-anti-equivariant vector bundle, a correspondence cycle with K-anti-equivariant action, or a fundamentally new algebraic object. The problem is no longer abstract — it has a specific coordinate-level target and a specific list of constructions that have already failed."**

---

## PART 9 — Strongest Honest Boundary

**"What is not yet established is whether the Hodge conjecture for $B_1$ on $A_*$ is accessible by any currently known technique — specifically: the three routes (Chern classes, correspondences, absolute Hodge cycles) all require either constructing new algebraic objects on $A_*$ whose existence is unproved, or establishing the absolutely Hodge property for $B_1$ (which requires computing the $p$-adic and $\ell$-adic Galois representations associated to $B_1$ and checking their compatibility — a computation that depends on the arithmetic of $A_*$ over a number field, not yet worked out), or finding an entirely new construction. The computation has located the gap with coordinate-level precision; the gap remains open."**

---

## The Frontier Map

```
Sprint 1 (A_0): Product variety, algebraic classes exist, gap is dictionary artifact → NOT CLEAN

Sprint 2a (A_1 rational): End^0 = M_4(Q(i)), always. Rational period matrix is always non-simple → NOT CLEAN

Sprint 2b (A_* irrational): End^0 = Q(i) confirmed. 8D clean obstruction. B_1 is real invariant.
  → Z_anti ruled out (CASE C+, primitive locus trivial)

Sprint 2c (structural):
  → Pure/mixed theorem: single J-stable cycle is K-invariant
  → Single-cycle impossibility: CH^2(A_*)^known = 0 in K-anti-inv
  → B_1 frontier: three routes remain (bundle, correspondence, abs. Hodge)

OPEN: Find the cycle.
```

## Collaborator Paragraph

Three independent structural results close every classical algebraic cycle construction for $B_1$ on $A_*$. The pure/mixed det formula (HODGE_PURE_MIXED_THEOREM) shows single J-stable cycles are always K-invariant (char poly argument: det$(\varphi|_{V_\mathbb{R}}) = +1$ for $\varphi^2 = -I$, invariant 4D real sub-space). The single-cycle impossibility (HODGE_SINGLE_CYCLE_IMPOSSIBILITY) combines this with $\varphi^*(L) = L$ (polarization preservation) and simplicity ($A_*$ simple iff End⁰ is a division algebra) to prove the K-anti-invariant part of $\text{CH}^2(A_*)^{\text{known}}_\mathbb{Q}$ vanishes. The Weil class $B_1$ — a 2D rational primitive $(2,2)$ subspace of $H^4(A_*,\mathbb{Q})$, computed to $< 10^{-13}$ residual, with $Q$-eigenvalue $0.0046$ and 81.9% weight in the sub-lattice $\{e_3,e_4,f_1,f_2,f_3,f_4\}$ — is the first coordinate-level representation of the Hodge conjecture's obstruction on a simple abelian variety. The three remaining routes — K-anti-equivariant vector bundles ($c_2(\mathcal{E}) \in B_1$), correspondence cycles (K-anti-equivariant $\Gamma \in \text{CH}^2(A_* \times A_*)$), and absolutely Hodge cycles (Deligne's theory, $p$-adic realization) — each require constructing algebraic objects whose existence on simple Weil 4-folds is currently unknown. The gap is located. The construction is missing.
