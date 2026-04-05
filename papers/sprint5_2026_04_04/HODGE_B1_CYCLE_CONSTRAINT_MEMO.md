# HODGE B_1 CYCLE-CONSTRAINT MEMO
# What Must Any Cycle Hitting Block B_1 Look Like?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — B_1 Data (Frozen)

| Property | Value |
|---------|-------|
| Dimension | 2 (over $\mathbb{Q}$) |
| $Q$-eigenvalue $\lambda$ | $0.004609$ (smallest in $W_*$, multiplicity 2) |
| Nonzero coordinates | **18/70** at threshold $10^{-3}$; 60/70 at threshold $10^{-5}$ |
| Dominant support | $\{e_3, e_4, f_1, f_2, f_3, f_4\} = \{2,3,4,5,6,7\}$ in the top terms |
| A_0 Weil overlap | $Q$-projection norm $3.78$ (largest of any block) |
| Character | Softest block; sparsest structure; most like classical Weil class |

**Leading terms of first B_1 basis vector:**

$$w_{B_1} \approx +0.510\,(e_3\wedge f_1\wedge f_2\wedge f_3) - 0.510\,(e_4\wedge f_1\wedge f_2\wedge f_4) - 0.275\,(e_4\wedge f_1\wedge f_2\wedge f_3) - 0.275\,(e_3\wedge f_1\wedge f_2\wedge f_4) + \cdots$$

---

## PART 2 — Support Constraints

Any cycle $Z \in \mathrm{CH}^2(A_*)_\mathbb{Q}$ with $\mathrm{cl}^2(Z)$ having nonzero $B_1$-projection must satisfy:

**C1. K-anti-invariance:**
$\varphi_*(\mathrm{cl}^2(Z))$ must include a $(-1)$-eigenspace component — the $B_1$-projection of any $K$-invariant class is strictly zero. The cycle must transform in the anti-invariant manner under the $K = \mathbb{Q}(i)$-action.

**C2. Primitivity (double confirmation):**
$L \wedge \mathrm{cl}^2(Z) = 0$ and $Q(\mathrm{cl}^2(Z), L^2) = 0$. Both are confirmed for $B_1$ — the block is strictly $Q$-orthogonal to $[L^2]$ (inner product $< 10^{-14}$).

**C3. Type $(2,2)$:**
$J_*(\mathrm{cl}^2(Z)) = \mathrm{cl}^2(Z)$. This means $Z$ must be a complex algebraic cycle (the underlying real sub-manifold is $J$-stable).

**C4. Sub-lattice directionality:**
The top terms of $B_1$ live in the 6-element sub-lattice $\{e_3, e_4, f_1, f_2, f_3, f_4\}$. Any cycle $Z$ must have generators that project significantly onto this sub-lattice. In particular:
- The $f_1 \wedge f_2$ factor appears in 4 of the 6 leading terms: the cycle must "see" the $f_1 \wedge f_2$ polarization sector.
- The $\{e_3, e_4\}$ and $\{f_3, f_4\}$ sectors (where $\varphi$ acts as NEGATIVE rotation, creating the Weil twist) dominate the $B_1$ structure.
- The $\{e_1, e_2\}$ sector is suppressed in $B_1$ but not entirely absent — the cycle need not avoid $e_1, e_2$ entirely, but its dominant structure must be in the $(e_3, e_4, f_*)$ sector.

**C5. Not purely sub-lattice supported:**
No rank-4 sub-lattice confined to $\{e_3, e_4, f_1, f_2, f_3, f_4\}$ is $J$-stable (verified by explicit computation). Any J-stable sub-space achieving non-trivial $B_1$ projection must involve ALL 8 lattice generators — the cycle must span the full lattice.

---

## PART 3 — Symmetry Constraints

**S1. K-anti-invariance (necessary):**
$\varphi_*(\mathrm{cl}^2(Z)) = -\mathrm{cl}^2(Z)$. This is the defining condition for $W_*$. Any cycle whose class is $K$-invariant (e.g., any combination of polarization divisors) has zero $B_1$ projection.

**S2. Rosati skewness:**
The Rosati involution of $\varphi$ satisfies Rosati$(\varphi) = -\varphi$ (computed: $E^{-1}\varphi^\top E = -\varphi$). A cycle $Z$ whose class projects onto $B_1$ must come from a construction that is "skew" with respect to the Rosati involution — it cannot be the graph of a self-adjoint endomorphism.

**S3. Exclusion from the algebraic shell:**
$\mathrm{cl}^2(Z)$ must NOT lie in the $K$-invariant sector of $H^{2,2}_\mathrm{prim}(A_*, \mathbb{Q})$. The algebraic shell (all currently known classes) lives entirely in the $K$-invariant sector (since $\varphi^*(L) = L$ and all constructible classes are $K$-invariant). A cycle hitting $B_1$ must be genuinely outside this shell.

**S4. Non-factorizable:**
Since $B_1$ has zero $Q$-inner product with all Künneth-type classes (products of codimension-1 classes), any cycle hitting $B_1$ must be non-factorizable as a product of two codimension-1 cycles.

---

## PART 4 — Excluded Cycle Types

| Cycle type | Why it cannot hit B_1 |
|-----------|----------------------|
| **Divisor products** $L_i \wedge L_j$ | $\varphi^*(L) = L$ exactly → these are strictly $K$-invariant → $B_1$ projection $= 0$ identically |
| **Endomorphism graph of $\varphi$** | The graph $\Gamma_\varphi \in \mathrm{CH}^4(A_* \times A_*)$ restricts to a $K$-invariant class on $A_*$ → excluded |
| **Any K-invariant cycle** | $B_1 \subset W_* = K\text{-anti-inv}$ → zero projection by definition |
| **Cycles supported on a proper sub-lattice** | No rank-4 sub-lattice within $\{e_3,e_4,f_1,f_2,f_3,f_4\}$ is $J$-stable; any integral class from such a sub-lattice is not a complex algebraic cycle |
| **$L^2$ and Lefschetz multiples** | $Q(B_1, L^2) = 0$ exactly; $B_1 \subset H^{2,2}_\mathrm{prim}$ is orthogonal to all Lefschetz classes |
| **Uniformly dense cycles** | A cycle whose class has equal weight across all 70 basis 4-forms has $B_1$ projection $\sim 1/\sqrt{70}$ of its total norm — negligible; $B_1$ requires a cycle that is *sparse* in the ambient $H^4$ |

**Computed verification:** the maximum $B_1$ projection from any sum of divisor products or $K$-invariant combinations is identically zero (to numerical precision $< 10^{-14}$).

---

## PART 5 — Most Plausible Remaining Cycle Type

The constraints narrow the search to:

- $K$-anti-invariant
- $J$-stable (complex algebraic)  
- Non-factorizable
- Dominant structure in the $\{e_3, e_4, f_1, f_2, f_3, f_4\}$ sector
- Generators spanning the full $\mathbb{Z}^8$ lattice (not confined to any proper sub-lattice)

**"If a cycle hits $B_1$, the most plausible shape is a non-factorizable codimension-2 correspondence cycle — a 2-dimensional abelian sub-variety of $A_*$ whose defining $\mathbb{Z}$-module mixes the K-twisted $\{e_3, e_4\}$ sector (where $\varphi$ acts as negative rotation) with the polarization $\{f_1, f_2\}$ sector, in a way that is forced to span all 8 generators by the $J_\Omega$-stability condition: specifically, a complex 2-dimensional sub-space $V_B \subset \mathbb{C}^4$ of the form $V_B = \mathbb{C}\text{-span}\{v_1, v_2\}$ where $v_1, v_2 \in \mathbb{C}^4$ are chosen so that the resulting real 4D sub-space $\{v_1, iv_1, v_2, iv_2\} \subset \mathbb{R}^8$ has its wedge class projecting nontrivially onto $B_1$."**

The random search over J-stable sub-spaces finds optimal $v_1, v_2$ with dominant components in $\{e_1, e_4, f_3\}$ for $v_1$ and $\{e_2, e_3, f_3, f_4\}$ for $v_2$ — specifically: the $(e_4, f_3)$ pairing and the $(e_3, e_2)$ mixing appear prominently. This points to a sub-abelian variety that diagonally mixes the $(e_3,e_4)$ Weil-twist sector with the $(f_3,f_4)$ sector, passing through all 8 generators.

The key absence: no RATIONAL (integral lattice) J-stable sub-space has yet been found with large $B_1$ projection, which is consistent with the fact that $B_1$ is an obstruction class — there is no obvious cycle for it.

---

## PART 6 — Exact Next Finite Test

**"The next finite test is:** for each pair of integer vectors $(v_1, v_2) \in \mathbb{Z}^8 \times \mathbb{Z}^8$ of bounded height $\|v_i\|_\infty \leq H$ (e.g., $H = 5$), compute the $J$-stable sub-space $V_B = \mathbb{C}\text{-span}\{v_1 + iJ_\Omega v_1, v_2 + iJ_\Omega v_2\}$, compute its cycle class $[B] = v_1 \wedge J_\Omega v_1 \wedge v_2 \wedge J_\Omega v_2 \in H^4(A_*, \mathbb{R})$, project $[B]$ onto $B_1$, and check whether the projection is:
(a) nonzero (confirming $B_1$ is accessible by some complex sub-torus), or
(b) zero for all height-$\leq H$ integral sub-tori (suggesting $B_1$ requires a non-sub-torus cycle construction).

This is a FINITE SEARCH: for $H=5$, there are $O(11^{16})$ pairs, but symmetry and $J$-stability reduce the effective count. A computationally feasible version uses a random walk over integer lattice vectors with $\ell^2$ norm $\leq H\sqrt{8}$, testing each for $B_1$ projection size above a threshold."

---

## PART 7 — Why This Matters

The $4 \times (2D)$ decomposition of $W_*$ reduces the Hodge problem from "find a cycle in an 8D space" to "fill each 2D block separately." $B_1$ is the canonical first block, and the constraints from Parts 2–5 give a concrete geometric description: the missing cycle must be $K$-anti-invariant, $J$-stable, non-factorizable, and mix the $\{e_3,e_4\}$ Weil-twist sector with the polarization sectors in a non-obvious way. These constraints rule out all standard cycle types (divisor products, endomorphism graphs, Lefschetz multiples). If the next finite test finds an integral $J$-stable sub-torus with nonzero $B_1$ projection, the cycle exists and the Hodge conjecture holds for $B_1$. If no such sub-torus exists, the block requires a non-sub-torus algebraic cycle — a more exotic geometric object.

---

## PART 8 — Strongest Honest Claim

**"The Hodge gap on $A_*$ has now been reduced from an 8-dimensional obstruction space to a first cycle-construction target $B_1$, and any successful cycle must satisfy a narrow set of support and symmetry constraints: $K$-anti-invariance (ruling out all divisor products and Lefschetz classes), $J$-stability (ruling out all non-complex cycles), non-factorizability (ruling out products of codimension-1 classes), dominant projection onto the $\{e_3, e_4, f_1, f_2, f_3, f_4\}$ sector with generators spanning the full $\mathbb{Z}^8$ lattice, and $Q$-orthogonality to $[L^2]$ — leaving a narrow but nonempty target window that the bounded-height integral sub-torus search can now probe directly."**

---

## PART 9 — Strongest Honest Boundary

**"What is not yet established is whether those constraints isolate a genuinely geometric cycle type, or only describe the cohomological shadow of an as-yet unknown construction: specifically, the computation shows that no rank-4 sub-lattice confined to the dominant $\{e_3,e_4,f_1,f_2,f_3,f_4\}$ coordinates is $J$-stable, so the cycle cannot be an obvious sub-torus supported on a proper sub-lattice; the J-stability condition forces generators to mix all 8 lattice directions in a way that has not yet been shown to produce a rational cycle class; and the Hodge conjecture may require a fundamentally non-geometric construction (a formal linear combination of sub-tori, or a cycle from an algebraic correspondence) that is invisible to the sub-torus search."**

---

## B_1 Constraint Block

$$Z \in \mathrm{CH}^2(A_*)_\mathbb{Q} \text{ hits } B_1 \implies$$

| Constraint | Status |
|-----------|--------|
| $\varphi_*(\mathrm{cl}^2(Z)) = -\mathrm{cl}^2(Z)$ | **Necessary** — verified zero projection for all K-invariant classes |
| $L \wedge \mathrm{cl}^2(Z) = 0$ | **Necessary** — B_1 ⊂ primitive subspace |
| $Q(\mathrm{cl}^2(Z), L^2) = 0$ | **Necessary** — B_1 is Q-orthogonal to $[L^2]$ (verified $< 10^{-14}$) |
| $J_*(\mathrm{cl}^2(Z)) = \mathrm{cl}^2(Z)$ | **Necessary** — B_1 ⊂ $H^{2,2}$, cycle must be complex algebraic |
| Generators span all 8 directions | **Necessary** — no proper sub-lattice gives J-stable cycle |
| No factorization as $\alpha \wedge \beta$ with $\alpha, \beta \in H^{1,1}$ | **Necessary** — all factorizable classes are K-invariant |

## Excluded Cycle Types Table

| Type | Rule-out |
|------|---------|
| Divisor products | K-invariant; $B_1$ projection $= 0$ identically |
| $\varphi$-endomorphism graph class | K-invariant; $B_1$ projection $= 0$ |
| $L^2$ and Lefschetz multiples | Primitive-orthogonal: $Q(B_1, L^k) = 0$ |
| Sub-lattice classes in $\{e_3,e_4,f_1,f_2,f_3,f_4\}$ | Not $J$-stable; not complex algebraic |
| Uniform classes (all 70 coords equal) | $B_1$ projection negligible; wrong density profile |
| Any K-invariant combination | $B_1 \subset W_* = K$-anti-inv; zero projection by definition |

## Most Plausible Cycle Type

**"If a cycle hits $B_1$, the most plausible shape is a 2-dimensional abelian sub-variety of $A_*$ defined by a complex 2-plane $V_B = \mathbb{C}\text{-span}\{v_1, v_2\}$ whose generators mix the K-twisted $\{e_3, e_4\}$ sector (the Weil-negative-rotation sector) with the polarization $\{f_1, f_2\}$ sector, spanning all 8 lattice directions by necessity of $J$-stability, with dominant $\{e_4, f_3\}$-type pairing in one generator and $\{e_3, e_2\}$-type mixing in the other — a diagonal sub-torus that cannot be confined to any proper sub-lattice."**

## Exact Next Finite Test

**Bounded-height integral J-stable sub-torus search:** for integer vectors $(v_1, v_2) \in \mathbb{Z}^8 \times \mathbb{Z}^8$ with $\|v_i\|_\infty \leq H = 5$, compute:
1. $V_B = \mathbb{C}\text{-span}\{v_1 + i J_\Omega v_1,\; v_2 + i J_\Omega v_2\} \subset \mathbb{C}^4$
2. Cycle class $[B] = v_1 \wedge J_\Omega v_1 \wedge v_2 \wedge J_\Omega v_2 \in H^4(A_*, \mathbb{R})$
3. $B_1$ projection $\|P_{B_1}([B])\|_Q$

**Decision:** if ANY pair $(v_1, v_2)$ gives nonzero $B_1$ projection AND $[B]$ is rational (i.e., $v_1 \wedge J_\Omega v_1 \wedge v_2 \wedge J_\Omega v_2 \in H^4(A_*, \mathbb{Q})$), then an explicit algebraic cycle for $B_1$ is found and the Hodge conjecture holds for this block on $A_*$.

## Collaborator Paragraph

The cycle-constraint analysis for $B_1$ on $A_*$ establishes a narrow but precise target window. Every known algebraic cycle type is excluded: divisor products and their combinations are strictly $K$-invariant ($\varphi^*(L) = L$ exactly), giving zero $B_1$ projection by a direct computation ($< 10^{-14}$); the $\varphi$-endomorphism graph class is $K$-invariant for the same reason; all Lefschetz multiples of $L^2$ are $Q$-orthogonal to $B_1$ ($Q(B_1, L^2) = 0$ confirmed); and no rank-4 sub-lattice confined to the dominant $\{e_3,e_4,f_1,f_2,f_3,f_4\}$ sector is $J$-stable (verified computationally — $J$ mixes all 8 directions). The surviving candidate is a 2-dimensional abelian sub-variety of $A_*$ whose generators span the full $\mathbb{Z}^8$ lattice, mixing the $K$-twisted $\{e_3,e_4\}$ sector (where $\varphi$ acts as negative rotation) with the $\{f_1,f_2\}$ polarization sector in a way forced by $J_\Omega$-stability. The random optimization over $J$-stable sub-spaces confirms that such sub-spaces can project nontrivially onto $B_1$, with optimal generators having dominant $\{e_4, f_3\}$ and $\{e_3, e_2, f_3\}$ character. The exact next test is a bounded-height integral search ($\|v_i\|_\infty \leq 5$, roughly $11^{16}$ pairs reducible by symmetry) to find whether any INTEGER $J$-stable sub-torus has a rational cycle class projecting onto $B_1$. Absence of such a sub-torus at low height would suggest $B_1$ requires a non-sub-torus algebraic cycle — a linear combination type, not a single irreducible sub-variety.
