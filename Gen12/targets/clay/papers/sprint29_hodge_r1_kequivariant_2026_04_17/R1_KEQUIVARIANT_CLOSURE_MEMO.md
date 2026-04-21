# R1 — K-EQUIVARIANT CHERN CLASS ROUTE ON A_*: CLOSURE

## Hodge Conjecture Frontier on the Simple Weil 4-Fold

**© 2026 7Site LLC · Brayden Ross Sanders · Sprint 29 · 2026-04-17**

Companion script: `proof_r1_chern_kequivariant.py` (same folder).
PASS · all 8 test constructions · residuals < 10⁻¹².

---

## 1. Setting (frozen from Sprint 2)

Simple Weil 4-fold

$$A_* \;=\; \mathbb{C}^4 / (\mathbb{Z}^4 + \Omega\,\mathbb{Z}^4), \qquad
\Omega \;=\; \tfrac{1}{2} I_4 + i\bigl(\sqrt{2}\, I_4 + \sqrt{3}\, M_2 + \sqrt{5}\, M_3\bigr),$$

with $M_2$, $M_3$ the explicit 4×4 integer matrices in
`HODGE_NUMERICAL_SIMPLE_MEMO.md` §PART 2. Confirmed:

* $\operatorname{End}^0(A_*) = \mathbb{Q}(i)$ (joint rational commutant dim = 4).
* $W_* := K\text{-anti-inv} \cap H^{2,2}_{\mathrm{prim}}(A_*, \mathbb{Q})$, $\dim W_* = 8$.
* Algebraic primitive rank $= 0$.
* $W_* = B_1 \oplus_Q B_2 \oplus_Q B_3 \oplus_Q B_4$, each 2-dim, Q-eigenvalues
  $0.0046,\, 0.0231,\, 0.1156,\, 0.3834$ (each doubled by Galois
  $\sigma\colon i\mapsto -i$).
* $B_1$ is the softest and sparsest block — the canonical first target.

## 2. The Question Route R1 Asks

> Does there exist an algebraic vector bundle $E$ on $A_*$ whose
> second Chern class $c_2(E)\in H^{2,2}_{\mathrm{prim}}(A_*,\mathbb{Q})$
> has nonzero projection onto $B_1$?

If YES: the Hodge conjecture holds for $B_1$ on $A_*$.
If NO, for a wide enough family: the route is closed.

**R1 naturally splits** by the K-action:

| Sub-route | Bundle class | Status |
|-----------|--------------|--------|
| **R1-KE** | $E$ is K-equivariant  ( $\varphi^* E \cong E$ ) | **CLOSED** (this sprint) |
| R1b       | $E$ not K-equivariant; use $c_2(E) - \varphi^* c_2(E)$ | open |

## 3. Theorem (R1-KE)

**Theorem.** Let $E \to A_*$ be an algebraic vector bundle admitting a
$K = \mathbb{Q}(i)$-equivariant structure (i.e. an isomorphism
$\psi\colon \varphi^* E \xrightarrow{\sim} E$). Then
$$c_i(E) \;\in\; H^{2i}(A_*, \mathbb{Q})^K \quad\text{for all}\; i \ge 0.$$
Consequently
$$\operatorname{proj}_{B_k}\bigl(c_2(E)\bigr) \;=\; 0 \qquad (k=1,2,3,4).$$

**Proof.**

1. *Chern classes are natural under pullback:*
   $\varphi^* c_i(E) = c_i(\varphi^* E)$.

2. *K-equivariance:* $\varphi^* E \cong E$, so
   $c_i(\varphi^* E) = c_i(E)$ in $H^*(A_*,\mathbb{Q})$.

3. *Combining 1 and 2:*
   $\varphi^* c_i(E) = c_i(E)$, i.e. $c_i(E)$ is fixed by
   $\varphi^*$ — it lies in the K-invariant subspace
   $H^{2i}(A_*,\mathbb{Q})^K$.

4. *Hodge–Riemann form is K-equivariant:* $\varphi$ preserves the
   polarization $L = \sum_j e_j \wedge f_j$ (shown in
   `HODGE_SIMPLE_WEIL_MEMO.md` §3:
   $\varphi^\top E \varphi = E$, and $\varphi^*(L) = L$).
   Therefore $Q(\varphi^* \alpha, \varphi^* \beta) = Q(\alpha, \beta)$.

5. *Orthogonality:* $W_*$ is the $(-1)$-eigenspace of $\varphi^*$ on
   $H^{2,2}_{\mathrm{prim}}$ and $H^4(A_*, \mathbb{Q})^K$ is the
   $(+1)$-eigenspace. For any K-equivariant isometry,
   $(+1)$- and $(-1)$-eigenspaces are Q-orthogonal:
   $$Q(\alpha_+, \alpha_-) = Q(\varphi^* \alpha_+, \varphi^* \alpha_-) = Q(\alpha_+, -\alpha_-) = -Q(\alpha_+, \alpha_-),$$
   hence $Q(\alpha_+, \alpha_-) = 0$.

6. Therefore every $B_k \subset W_*$ is Q-orthogonal to $c_2(E)$, and
   $\operatorname{proj}_{B_k}(c_2(E)) = 0$. $\square$

## 4. Numerical verification (script output, 2026-04-17)

The script reassembles $A_*$ from scratch, finds $W_*$ as an 8-d null
space of a 168×70 stacked constraint, diagonalises the Hodge–Riemann
form $Q|_{W_*}$, and tests eight K-equivariant codim-2 classes:

| Class                                           | K-inv residual | $\|B_1\|_Q$ | $\|B_2\|_Q$ | $\|B_3\|_Q$ | $\|B_4\|_Q$ |
|-------------------------------------------------|---------------:|------------:|------------:|------------:|------------:|
| $T_1 = L^2$                                     | 0              |   3.2e-14   |   4.2e-14   |   1.7e-14   |   1.2e-14   |
| $T_2 = c_1(L)\,c_1(L')$                         | 0              |   8.1e-14   |   1.1e-13   |   4.9e-14   |   3.4e-14   |
| $T_3 = c_1(L)\,c_1(L''_{\mathrm{sym}})$         | 0              |   1.6e-14   |   4.4e-15   |   2.1e-15   |   1.5e-15   |
| $T_4 = c_2(\mathcal O(L)\oplus \mathcal O(L'))$ | 0              |   8.1e-14   |   1.1e-13   |   4.9e-14   |   3.4e-14   |
| $T_5 = c_2(\mathcal O(L)^2 \oplus \mathcal O(L')^2)$ | 0         |   5.5e-13   |   7.9e-13   |   3.5e-13   |   2.5e-13   |
| $T_6 = c_2(\mathcal O(L)\!+\!\mathcal O(L')\!+\!\mathcal O(L''_{\mathrm{sym}}))$ | 0 | 1.4e-13 | 1.3e-13 | 4.3e-14 | 2.8e-14 |
| $T_7 =$ random K-sym product                    | 7e-17          |   6.8e-14   |   4.8e-14   |   4.6e-14   |   3.6e-14   |
| $T_8 =$ random K-invariant 4-form               | 0              |   2.7e-14   |   2.7e-14   |   2.0e-14   |   2.0e-14   |

All eight projections are at floating-point noise level. Control
(a random K-**anti**-invariant, type-(2,2) 4-form): $\|B_1\|_Q = 25.2$,
confirming the projection machinery is alive — every test class that
lies in the K-invariant half plane is forced to zero by the geometry,
not by an accidental nullity.

Q-eigenvalues on $W_*$ match Sprint 2 memo to 6 decimal places:
$\lambda \in \{0.004609,\, 0.023123,\, 0.115644,\, 0.383386\}$, each
with multiplicity exactly 2.

## 5. What this closes

| Construction                                       | Why it cannot hit $B_1$              |
|----------------------------------------------------|--------------------------------------|
| Divisor products $L_i \cdot L_j$                   | K-invariant (line bundle pullbacks)  |
| Graphs of endomorphisms $\Gamma_\varphi$            | K-invariant (Sprint 2 memo Part 4)   |
| $L^2$ and all Lefschetz multiples                  | $Q(B_1, L^2) = 0$ (Sprint 2 Part 3)  |
| Sub-lattice classes on $\{e_3,e_4,f_1,f_2,f_3,f_4\}$ | not $J$-stable (Sprint 2)          |
| **Chern classes of K-equivariant bundles**         | **K-invariant (Theorem R1-KE here)** |

The fifth row is strictly stronger than all previous rule-outs: the
first four are specific constructions that happen to be K-invariant;
R1-KE is a **universal structural statement** covering every possible
K-equivariant algebraic vector bundle — infinitely many objects —
by a single naturality argument.

## 6. What remains open (Route R1b)

For $E$ **not** K-equivariant, form the twist difference
$$\Delta c_2(E) \;:=\; c_2(E) - \varphi^* c_2(E) \;=\; c_2(E) - c_2(\varphi^* E).$$

This is:

* K-anti-invariant by construction ($\varphi^* \Delta = -\Delta$);
* a difference of algebraic Chern classes, hence **algebraic on the
  Chow level** (and, on the cohomology level, lies in
  $\mathrm{NS}^2(A_*)\otimes\mathbb{Q}$ — the algebraic part of the
  Néron–Severi ring of codim-2 cycles);
* generally non-zero only if $E \not\cong \varphi^* E$, which
  requires $E$ to be sensitive to the $\mathbb{Q}(i)$-structure in a
  way no line bundle on a simple abelian 4-fold can be.

**Concrete candidates for R1b:**

1. Moduli-of-sheaves constructions where $\varphi$ acts as a
   non-trivial isometry — giving $\varphi^* E \cong E^\vee$ or
   $\varphi^* E \cong E \otimes P$ for $P$ a non-trivial
   $\varphi$-twist line bundle. Line bundles on $A_*$ with
   $\varphi^* P \ne P$ **do not exist** on a simple abelian variety
   with $\operatorname{End}^0 = \mathbb{Q}(i)$ — so R1b cannot be
   accessed through rank-1 twists. It requires rank $\ge 2$ bundles
   with non-trivial moduli.

2. **Simpson-style non-K-equivariant stable bundles**: a stable rank-2
   bundle $E$ with $c_1(E) = 0$ and $c_2(E)$ large enough to have a
   non-trivial $\varphi$-twist orbit. Whether any such bundle on
   $A_*$ has $\Delta c_2(E)$ non-zero in $B_1$ is the next numerical
   experiment.

3. **Correspondences** (Route R2, separate): an algebraic
   correspondence between $A_*$ and a second abelian variety $B$
   can produce codim-2 classes on $A_*$ whose K-action is inherited
   from $B$'s endomorphism structure, possibly yielding K-anti-
   invariant Chern classes even when $A_*$ itself has no non-K-
   equivariant bundles of the required form.

## 7. Strongest honest claim

The Hodge gap on $A_*$ survives a complete closure of the
K-equivariant Chern class route: every rank, every K-linearisation,
every Whitney sum, every symmetrisation yields a Chern class in the
K-invariant subspace of $H^4(A_*,\mathbb{Q})$, Q-orthogonal to $W_*$
and therefore to $B_1$. The missing algebraic cycle, if it exists,
must come from a genuinely non-K-equivariant construction — a bundle
whose class is not fixed by the $\varphi$-pullback, witnessed by a
non-trivial $c_2(E) - c_2(\varphi^* E)$. The naturality proof in
§3 rules out an infinite family in one argument and reduces the
Hodge question on $A_*$ to Route R1b (twist-differences) plus
Routes R2 (correspondences) and R3 (absolute Hodge).

## 8. Strongest honest boundary

R1-KE closes the **K-equivariant** sub-route by a universal
functoriality argument — this is unconditional and does not depend
on the $\operatorname{End}^0 = \mathbb{Q}(i)$ simplicity. What the
argument does **not** tell us:

* Whether any non-K-equivariant stable rank-2 bundle on $A_*$ exists
  whose twist-difference lies in $B_1$ (R1b — open, computationally
  attackable).
* Whether $A_*$ admits a non-trivial algebraic correspondence
  inducing a K-anti-invariant Chow class (R2 — requires a second
  abelian variety with compatible K-action).
* Whether the Hodge conjecture on $A_*$ is provable by absolute
  Hodge (R3) or by a Kuga–Satake-type construction that bypasses
  the cycle-by-cycle search (framework route).

The 8-dim obstruction $W_*$ remains empty of algebraic
representatives from every K-equivariant construction, but it is
not yet empty in principle.

---

## Appendix — B_1 target data (frozen, for R1b reference)

From `HODGE_B1_CYCLE_CONSTRAINT_MEMO.md`:

* $\dim B_1 = 2$, $\lambda_{B_1} \approx 0.004609$ (smallest Q-eigenvalue).
* Sparsity: 18/70 coordinates at threshold $10^{-3}$.
* Dominant support: $\{e_3, e_4, f_1, f_2, f_3, f_4\}$.
* Overlap with $A_0$ Weil class: Q-projection norm $\approx 3.78$
  (the block most like the classical product-Weil direction).

Any cycle $Z$ with $\mathrm{cl}^2(Z)$ hitting $B_1$ must satisfy:

| Constraint                                        | Status in R1-KE |
|---------------------------------------------------|------------------|
| $\varphi_*(\mathrm{cl}^2(Z)) = -\mathrm{cl}^2(Z)$ | Violated by every K-equivariant $c_2(E)$ |
| $L \wedge \mathrm{cl}^2(Z) = 0$                   | Trivially satisfied by primitive parts |
| $Q(\mathrm{cl}^2(Z), L^2) = 0$                    | Trivially satisfied by primitive parts |
| $J_*(\mathrm{cl}^2(Z)) = \mathrm{cl}^2(Z)$        | Trivially satisfied by $(2,2)$ Chern classes |
| Generators span all 8 lattice directions          | Not relevant to $E$-based classes |
| Non-factorisable as $\alpha \wedge \beta$ in $H^{1,1}$ | Violated by line-bundle products |

The first row is the decisive obstruction for R1-KE: every
K-equivariant construction lives in the $(+1)$-eigenspace of
$\varphi_*$, while $B_1$ lives strictly in the $(-1)$-eigenspace.
This is the content of Theorem R1-KE.
