# Tretkoff–Tretkoff Symplectic Basis — Implementation Plan

**Goal.**  Produce a topologically-guaranteed symplectic basis
$\{\alpha_1, \ldots, \alpha_5, \beta_1, \ldots, \beta_5\}$ of
$H_1(C, \mathbb{Z})$ with explicit integer intersection form
$J = \begin{pmatrix}0 & I_5 \\ -I_5 & 0\end{pmatrix}$ for the
canonical bielliptic genus-5 curve

$$C : y^4 = x(x-1)(x-\sqrt 2)^3 (x-\sqrt 3)^2 (x-\sqrt 5)^2.$$

Then restrict to the $\iota$-antiinvariant subspace (the Prym, dim 4)
and compute $\Pi = (A \mid B)$ in the new basis; $\tau = A^{-1}B$ is
automatically symmetric with $\operatorname{Im}\tau$ positive-definite,
and $\det(\operatorname{Im}\tau)$ is the target.

---

## Monodromy data (already established)

| Branch point | Multiplicity in $f$ | $\sigma \in \mathbb{Z}/4$ |
|---|---|---|
| $x = 0$ | 1 | 1 |
| $x = 1$ | 1 | 1 |
| $x = \sqrt 2$ | 3 | 3 |
| $x = \sqrt 3$ | 2 | 2 |
| $x = \sqrt 5$ | 2 | 2 |
| $x = \infty$ | — | 3 |

Sum: $1+1+3+2+2+3 = 12 \equiv 0 \pmod 4$ ✓
Riemann–Hurwitz with $\sum (4 - \gcd(\sigma_i, 4)) = 3+3+3+2+2+3 = 16$:
$2g-2 = -8 + 16 = 8 \Rightarrow g = 5$ ✓

$\iota$-fixed points: 8 (four double points, one triple, one sextuple
fixed by $(x,y) \to (x,-y)$; includes $x=\infty$).

---

## Algorithm outline (Tretkoff–Tretkoff 1984, refined Molin–Neurohr 2017)

### Step 1 — Cell decomposition of $\mathbb{CP}^1$

Pick a base point $P_0$ (a safe non-branch point, say $P_0 = -1 + 4i$,
well away from the real axis and branch points).

Draw **radial edges** $e_i : P_0 \to P_i$ for each of the 6 branch points
$P_1 = 0$, $P_2 = 1$, $P_3 = \sqrt 2$, $P_4 = \sqrt 3$, $P_5 = \sqrt 5$,
$P_6 = \infty$.

Order them by angle (as seen from $P_0$). This gives the **Tretkoff
ordering** $(i_1, i_2, \ldots, i_6)$: the cyclic order of radial departures.

### Step 2 — Lift each edge to the 4-sheeted cover

For each edge $e_i$ and each sheet $k \in \{0,1,2,3\}$, obtain the
lifted edge $\widetilde{e_i}^{(k)}$ by analytic continuation of the
chosen 4th root of $f(x)$ along $e_i$ starting from sheet $k$ at $P_0$.

By definition, the monodromy around $P_i$ sends sheet $k$ to
sheet $k + \sigma_i \pmod 4$, so the lifted edge ending at $P_i$ on
sheet $k$ connects to the lifted edge starting on sheet $k + \sigma_i$
when crossing the branch locus.

### Step 3 — Build the ramified graph (Tretkoff complex)

Nodes: $P_0^{(k)}$ for each sheet $k$, plus $P_i^{(j)}$ for each branch
point $P_i$ and each orbit $j$ of $\langle \sigma_i \rangle$ on sheets.

Edges: each lifted radial edge $\widetilde{e_i}^{(k)}$.

### Step 4 — Cycle enumeration

A **Tretkoff cycle** is constructed by:
1. pick a pair of adjacent edges $(e_i, e_{i+1})$ in the cyclic order,
2. from $P_0$ on sheet $k$, go out along $e_{i+1}$, arrive at $P_{i+1}$ on sheet $k$,
3. make a tiny positive circuit around $P_{i+1}$, advancing sheets by $\sigma_{i+1}$,
4. come back along $e_{i+1}^{-1}$ to $P_0$ on sheet $k + \sigma_{i+1}$,
5. go out along $e_i$, circuit $P_i$ (advancing by $\sigma_i$),
6. return along $e_i^{-1}$ — you are now on sheet $k + \sigma_{i+1} + \sigma_i$.

The closed cycle when composed $N$ times (until total sheet advance is 0)
gives an element of $H_1(C)$.

This enumeration yields $g \cdot \gcd(...) = 5$ independent $\alpha$-cycles
and 5 independent $\beta$-cycles, with **intersection numbers $\pm 1$ by
construction** for adjacent pairs in the Tretkoff ordering.

### Step 5 — Integer intersection matrix $E$

Tretkoff shows: two cycles $(i_a, k_a)$ and $(i_b, k_b)$ intersect
exactly when their radial edges are adjacent in the Tretkoff ordering
AND their sheet ranges overlap in a specific way (explicit combinatorial
rule in the paper).

Result: an $8g = 40$-cycle generating set with an integer $40 \times 40$
skew intersection matrix $E$ whose entries are in $\{-1, 0, +1\}$.
**The matrix is constructed — not recovered via LLL.**

### Step 6 — Symplectic reduction via Smith Normal Form

Reduce $E$ to block form $\begin{pmatrix}0 & D \\ -D & 0\end{pmatrix}$
over $\mathbb{Z}$. The Smith elementary divisors $D = \mathrm{diag}(d_1,
\ldots, d_g)$ give the **polarization type** $(d_1, \ldots, d_g)$;
for a principal polarization $d_i = 1$ for all $i$.

The unimodular transformation $M \in \mathrm{GL}(8g, \mathbb{Z})$ that
achieves SNF also transforms the cycle basis; applying $M$ to the original
cycles gives the desired symplectic basis.

### Step 7 — Numerically integrate the 4 Prym differentials along the new basis

Using `prym_compute.py`'s high-precision quadrature infrastructure,
integrate $\omega_0 = dx/y$, $\omega_1 = x \, dx/y$,
$\omega_2 = (x-\lambda)^2(x-\mu)(x-\nu) dx/y^3$,
$\omega_3 = x(x-\lambda)^2(x-\mu)(x-\nu) dx/y^3$
along the new basis cycles (possibly complicated polygonal paths lifted to
the cover).

This gives $\Pi_{\text{canon}} = (A_{\text{canon}} \mid B_{\text{canon}})$,
a $4 \times 10$ complex matrix.

### Step 8 — Project onto the $\iota$-antiinvariant subspace (Prym)

The involution $\iota : (x, y) \to (x, -y)$ acts on $H_1(C, \mathbb{Z})$
by pulling sheets $k \leftrightarrow k+2 \pmod 4$ (since $\iota$
corresponds to the element $2 \in \mathbb{Z}/4$).

The Prym $P$ is the $-1$-eigenspace of $\iota_*$ on $H_1(C, \mathbb{Q})$.
Projection: $\pi_{-} = \frac{1}{2}(1 - \iota_*)$.

Applied to the 10 $\alpha$'s and 10 $\beta$'s, this produces 4 independent
Prym $\alpha$'s and 4 independent Prym $\beta$'s, with the induced
symplectic form being the restriction of $E$.

### Step 9 — Normalize $\tau = A_P^{-1} B_P$, compute $\det(\operatorname{Im}\tau)$

On the Prym, $\tau$ is automatically symmetric (Riemann bilinear is
satisfied by construction) and $\operatorname{Im}\tau$ is positive-definite.
$\det(\operatorname{Im}\tau)$ is the final answer.

PSLQ against $\{1, \sqrt 2, \sqrt 3, \sqrt 5, \sqrt 6, \sqrt{10}, \sqrt{15}, \sqrt{30}\}$
should now recover the target coefficients $2086, 462\sqrt{15}, 498\sqrt{10}, 730\sqrt 6$.

---

## Implementation file layout

```
tretkoff.py                 ~ 200 LOC
  - BranchPoint dataclass (point, multiplicity, sigma)
  - tretkoff_ordering(P0, branch_points) -> list of indices
  - build_cycle_matrix(ordering, sigmas, N=4) -> 8g x 8g integer matrix

symplectic_reduction.py     ~ 100 LOC
  - snf_skew(E) -> (M, D) such that M^T @ E @ M = [[0, D], [-D, 0]]
  - check_principal_polarization(D)

path_lifting.py             ~ 150 LOC
  - lift_edge(x_start, x_end, sheet_start, f_coeffs) -> list of (x_i, y_i)
    with analytic continuation of y = f(x)^{1/4}
  - integrate_form_along_path(form, lifted_path, weight) -> mpc

tretkoff_driver.py          ~ 150 LOC
  - top-level: builds ordering, constructs cycles, integrates forms
  - applies iota-projection onto Prym
  - PSLQ on det(Y)

  total: 400-700 LOC as estimated.
```

## Verification checkpoints

1. After Step 5: `det(E)` on the full 40-cycle matrix should equal
   $\pm 1$ (for a principal polarization at the $C$ level after SNF).
2. After Step 6: the reduced $E$ should be exactly $J_{10}$.
3. After Step 8: Prym $\Pi$ should have $\det A \neq 0$ and Riemann
   bilinear: $\|\tau - \tau^T\|_F < 10^{-30}$ at dps=60.
4. $\operatorname{Im}\tau$ eigenvalues all positive.
5. $\det(\operatorname{Im}\tau)$ should match target
   $2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt 6 \approx 7238.26$ to
   many digits after PSLQ.

## Risks and mitigations

- **Path complexity.** Cycles lifted to the cover can pass near multiple
  branch points; analytic continuation must track sheets carefully.
  Mitigate: route each radial edge well into the UHP (height $\geq 4$)
  away from the real line where all branch points live; do sheet-tracking
  at tight step-size ($\Delta x \leq 0.01$).

- **Numerical cost.** 10 $\alpha$'s × 4 forms + 10 $\beta$'s × 4 forms =
  80 complex integrals at dps=60.  Each integral may be a polygonal
  path of 3–4 legs.  Estimated: 5–10 min total.

- **Tretkoff matrix size.** For $N=4$, $g=5$, the generator set is $\sim 8g = 40$
  cycles; matrix ops are trivial compared to the integration cost.

## Fallback

If Steps 1–6 hit a combinatorial snag (e.g., the ramification pattern
is exceptional), Molin–Neurohr 2017 gives a rewritten version that
handles $\sigma_i \neq 1$ explicitly.  Code in their 2017 paper
Algorithm 3.2–3.8 is a direct porting target.

Paid last resort: MAGMA `AnalyticJacobian(x * (x-1) * (x-sqrt(2))^3 *
(x-sqrt(3))^2 * (x-sqrt(5))^2, 4)`.

---

**Status.** Plan complete.  Await Option 5 (perturb_det_Y.py) results
before committing to implementation; the perturbation run tells us
whether the cycle basis is even stable near the canonical point, which
affects how we design Step 7's path parameterization.
