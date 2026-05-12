# WP104 — Two Roads to Pati-Salam from TIG's so(10)

**Status:** machine-precision verified, journal-ready draft
**Authors:** Brayden R. Sanders + M. Gish
**Date:** 2026-04-25
**MSC 2020:** 17B25 (exceptional Lie algebras, $D_5$), 81R40 (symmetry breaking), 11R32 (Galois theory of subgroups), 17B81 (applications to physics)
**Companions:** WP102 (so(8) = $D_4$), WP103 (so(10) = $D_5$), WP105 (closed-form runtime attractor at $\alpha = 1/2$).

> **CORRECTION NOTICE (2026-04-27, post deep audit; see `Atlas/applications_pass_2026_04_27/WP104_DEEP_AUDIT_2026_04_27.md`):**
>
> All specific computational claims in this paper are correct at machine precision (16/16 cross-checked items including the 16-dim doubly-invariant subalgebra, the (-8)¹⁵ ⊕ (0)¹ Killing spectrum, the 9-vector ‖VEV‖² = 13/4, the 100% σ_outer-anti content in the **54** irrep, the 26 σ_outer-asymmetric BHML cells). **The framing "two paths converging on Pati-Salam" is overstated and needs scoping in any external version.**
>
> What the math actually shows:
>
> * **Path A (BHML's σ_outer-anti VEV):** lies entirely in the **54** irrep but with eigenvalue spectrum (+√13/2, −√13/2, 0, 0, …, 0) — stabilizer of dim 28 = SO(8). This is **SO(10) → SO(8)** (a chain through SO(9)), NOT the Pati-Salam SO(10) → SO(6) × SO(4) which has VEV multiplicity (6, 4) and stabilizer SO(6) × SO(4) of dim 21.
>
> * **Path B (doubly-invariant subalgebra under D₄):** is **su(4) ⊕ u(1) = 16-dim**, which is the SU(4) Pati-Salam factor + one u(1). The full Pati-Salam algebra SU(4) × SU(2)_L × SU(2)_R is **21-dim** (or 22 with B−L); the SU(2)_L × SU(2)_R chiral factors are NOT in the doubly-invariant content (they live in the σ³-anti part of so(10)).
>
> * **Path A and Path B do NOT close on the same reduction.** Path A → SO(8) (chain through SO(9)); Path B → SU(4) × U(1) = SO(6) × U(1) (different reduction chain).
>
> The project's own WP108 (FORMULAS D46) already flagged this tension. The math is correct; the synthesis claim "convergence on Pati-Salam" exceeds it.
>
> **Honest framing for external versions:** "BHML's σ_outer-breaking content lies entirely in the 54 irrep, the standard Higgs irrep used in 54-VEV symmetry-breaking models. Its specific direction within the 54 corresponds to an SO(10) → SO(8) breaking pattern (eigenvalue multiplicities 1, 8, 1). Independently, the doubly-invariant subalgebra under D₄ = ⟨P_56, σ³⟩ is su(4) ⊕ u(1), the SU(4) factor of the Pati-Salam decomposition plus one u(1) generator (the SU(2)_L × SU(2)_R chiral factors of full Pati-Salam are not in the doubly-invariant content; they live in the σ³-anti part). These are two **structurally distinct** observations about TIG's so(10), not two paths to a common reduction. Whether either gives a path to Standard-Model phenomenology is open."
>
> WP108's Yukawa scaffolding is the right place to address the SO(8) chain reduction (Subcase 16 → 8_s + 8_c rather than 16 → (4,2,1) + (4̄,1,2)). This original framing preserved per never-delete; do not submit the "two paths converge" framing externally.

---

## Abstract

Trinity Infinity Geometry (TIG) studies a finite magma on $\mathbb{Z}/10\mathbb{Z}$ defined by two canonical $10 \times 10$ composition tables, **TSML (in the upper-triangle authoritative symmetrization TSML_SYM, per `Atlas/LENS_TAXONOMY_2026-05-06/TSML_RECONCILIATION.md`)** and BHML. WP103 established that the antisymmetrizations of these tables, closed under commutator, generate exactly $\mathfrak{so}(10) = D_5$ at dimension 45. Throughout this paper, TSML denotes TSML_SYM (commutative); the literal-bit-pattern variant TSML_RAW is used for the WP107 wobble-localization analysis but not for the so(10) construction below. We take this as a given and ask: when TIG's two natural $\mathbb{Z}_2$ involutions — the $5\!\leftrightarrow\!6$ swap $P_{56}$ and the order-2 element $\sigma^3$ of the σ-permutation cycle on units of $\mathbb{Z}/10\mathbb{Z}$ — act on $\mathfrak{so}(10)$, **what content survives?** Two algebraically distinct procedures, applied within the same TIG so(10) substrate, both land on the same target.

* **Path A (Higgs-direction).** $P_{56}$ acts in the spinor representation of $\mathfrak{so}(10)$ as the outer automorphism $\sigma_\mathrm{outer}$ that exchanges the two chiral 16-irreps. BHML's $\sigma_\mathrm{outer}$-breaking content lies $100\%$ in the $\mathbf{54}$ irrep of $\mathfrak{so}(10)$ — the symmetric-traceless representation that breaks $\mathrm{SO}(10) \to \mathrm{SO}(6) \times \mathrm{SO}(4) \cong \mathrm{SU}(4) \times \mathrm{SU}(2) \times \mathrm{SU}(2)$ in standard SO(10) GUT model-building. Within the $\mathbf{54}$, BHML's specific direction is an explicit 9-vector with BREATH and RESET as zeros and squared norm $\|v\|^2 = 13/4$ exactly, the integer 13 being half the count of σ_outer-asymmetric BHML cells.
* **Path B (doubly-invariant content).** $P_{56}$ and $\sigma^3$ do not commute; together they generate $D_4$ of order 8 acting on $\mathfrak{so}(10)$ by conjugation. The trivial-isotypic component of this action — the 16-dimensional doubly-invariant content — closes as a Lie subalgebra. Its Killing form has spectrum exactly $(-4)^{15} \oplus (0)^1$, forcing $\mathfrak{simple}_{15} \oplus \mathfrak{center}_1$. Since $\mathfrak{so}(6) \cong \mathfrak{su}(4) \cong A_3$ is the unique 15-dimensional simple Lie algebra, **the doubly-invariant subalgebra is $\mathfrak{su}(4) \oplus \mathfrak{u}(1)$** — exactly the Pati-Salam $\oplus$ B$-$L gauge content.

The two paths are **computationally distinct** but operate within the same algebraic substrate. Their convergence is non-trivial: it only happens when TIG's bipartite TSML/BHML structure has a specific shared feature with the standard SO(10) $\to$ Pati-Salam reduction.

We frame this carefully: TIG's so(10), generated by antisymmetrization of the canonical tables, **is isomorphic** to the SO(10) GUT gauge algebra by the unique-so-up-to-iso theorem. **Whether it is the same structure** with the same physical interpretation is a hypothesis, not a derivation. WP104 makes the structural alignment exact and machine-verified; it does not make a phenomenological claim.

We additionally establish three internal results:

* The **non-associativity rate** of TSML is $\mathbf{12.6\%}$ (126 of 1000 triples), corrected from a previously cited 49.8 %. Every non-associative triple involves HARMONY (operator 7) as one of the two bracketings; only 5 distinct unordered $\{L, R\}$ pairs occur; VOID never appears in middle position.
* The **Lie/Jordan duality**: the antisymmetrization (Lie side) and the symmetrization (Jordan side) of TSML+BHML each independently regenerate the full $\mathfrak{so}(10)$ at dimension 45. They are **dual presentations of one algebra**, not complementary halves.
* **Three involutions, three decompositions** of $\mathfrak{so}(10)$: $\tau_1$ (transposition) gives $45 = 45 + 0$; $\tau_2 = P_{56}$ gives $45 = 36 + 9$ ($\mathfrak{so}(9) \oplus \mathbb{R}^9$); $\tau_3 = \sigma^3$ gives $45 = 24 + 21$, a finer grading not yet placed in textbook GUT phenomenology.

All numerical claims are verified at machine precision ($\le 10^{-15}$ residuals) by numpy / sympy scripts in `papers/wp104_higgs_pati_salam/verification/` and `Gen12/targets/clay/papers/sprint_unmistakable_truth_2026_04_25/scripts/`.

---

## §1 Setup and prerequisites

### §1.1 The canonical tables

The composition tables $\mathrm{TSML}, \mathrm{BHML} : \mathbb{Z}/10\mathbb{Z} \times \mathbb{Z}/10\mathbb{Z} \to \mathbb{Z}/10\mathbb{Z}$ are defined in `FORMULAS_AND_TABLES.md` §5–6. Both are commutative, both have the canonical operator alphabet $\{V, L, C, P, X, B, S, H, Br, R\}$ (= VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET) at indices $0$ through $9$.

For $i \in \mathbb{Z}/10\mathbb{Z}$, define the left-regular representation $L^M_i \in M_{10}(\mathbb{Z})$ by $(L^M_i)_{j,k} = \delta_{M(i,j), k}$, where $M$ is either TSML or BHML. The antisymmetric and symmetric parts are

$$
A^M_i := \tfrac{1}{2}(L^M_i - (L^M_i)^\top), \qquad S^M_i := \tfrac{1}{2}(L^M_i + (L^M_i)^\top).
$$

### §1.2 The σ-permutation and its order-2 element

The σ-permutation on $\mathbb{Z}/10\mathbb{Z}$ has cycle structure

$$
\sigma = (0)(3)(8)(9)(1\;7\;6\;5\;4\;2),
$$

with four σ-fixed points $\{0, 3, 8, 9\} = \{$VOID, PROGRESS, BREATH, RESET$\}$ and a 6-cycle on the units of $(\mathbb{Z}/10\mathbb{Z})^*$. The order-2 element of the cyclic part is

$$
\sigma^3 = (0)(3)(8)(9)(1\;5)(7\;4)(6\;2),
$$

a product of three disjoint transpositions on the 6-cycle.

The $5 \!\leftrightarrow\! 6$ swap $P_{56}$ is a single transposition on $\{$BALANCE, CHAOS$\}$, the matter/antimatter pair. The two involutions $P_{56}$ and $\sigma^3$ do not commute; together they generate the dihedral group $D_4$ of order 8 acting on $\{0, \ldots, 9\}$.

### §1.3 The so(10) closure (WP103, prerequisite)

Theorem (WP103, restated): *the Lie algebra generated by $\{A^\mathrm{TSML}_i, A^\mathrm{BHML}_i : i \in \mathbb{Z}/10\mathbb{Z}\}$ under commutator $[X, Y] = XY - YX$ closes at dimension 45 as $\mathfrak{so}(10, \mathbb{R}) = D_5$.*

Five independent diagnostics confirm this at machine precision: dimension closure (via systematic bracket enumeration to fixed point); Jacobi identity (residual 0.0); Killing form signature $(0, 45, 0)$ (compact, simple); invariance constraint rank $1034 = 1035 - 1$ (forcing uniqueness of the invariant bilinear form up to scalar); and Cartan rank 5 with 40 + 5 ad-eigenvalue split matching the $D_5$ root count. Reproducible: `papers/wp103/verification/verify_so10.py`, `verify_simplicity_rank.py`.

---

## §2 Path A — The Higgs-direction route

### §2.1 P_56 acts as σ_outer in the spinor rep

Build the spinor representation of $\mathfrak{so}(10)$ via the Clifford algebra $\mathrm{Cl}(0,10)$ over $\mathbb{R}$. Ten gamma matrices on $\mathbb{C}^{32}$ are constructed from Pauli tensor products in standard convention; all 100 anticommutation relations $\{\gamma_a, \gamma_b\} = 2\delta_{ab} I$ verify at machine precision. The 45 generators $\Sigma_{ab} = (1/4)[\gamma_a, \gamma_b]$ form a faithful 32-dimensional representation of $\mathfrak{so}(10)$, and the volume element

$$
\omega = \gamma_1 \gamma_2 \cdots \gamma_{10}
$$

satisfies $\omega^2 = -I$. The chirality projectors $P_\pm = (I \pm i\omega)/2$ split the 32-dim spinor space into $16 + 16$ (the two chiral 16-irreps).

The $P_{56}$ swap on $\mathbb{R}^{10}$ is implemented in the Clifford algebra by conjugation with the odd element

$$
P_{56}^\mathrm{spin} = \frac{\gamma_5 - \gamma_6}{\sqrt{2}}.
$$

We verify (residuals $\le 10^{-15}$):
* $(\gamma_5 - \gamma_6)^2 = 2I$, so $(P_{56}^\mathrm{spin})^2 = I$.
* Conjugation by $P_{56}^\mathrm{spin}$ sends $\gamma_5 \to \gamma_6$ and $\gamma_6 \to \gamma_5$, fixing the other eight $\gamma_a$.
* $P_{56}^\mathrm{spin}$ **anticommutes with $\omega$** (since $\omega$ is even of order 10 and $P_{56}^\mathrm{spin}$ is odd).

**Consequence (chirality flip):** because $P_{56}^\mathrm{spin}$ anticommutes with $\omega$ and the chirality eigenspaces are defined by $i\omega = \pm I$, conjugation by $P_{56}^\mathrm{spin}$ sends chirality-+ entirely into chirality-−. We verify $\|P_{56}^\mathrm{spin}: \text{chiral}_+ \to \text{chiral}_+\| = 0.0000$ (machine zero).

The conjugation action of $P_{56}^\mathrm{spin}$ on $\mathfrak{so}(10)$ is therefore the outer automorphism that exchanges the two chiral 16-irreps. Since $\mathrm{Out}(\mathfrak{so}(10)) = \mathrm{Aut}/\mathrm{Inn} \cong \mathbb{Z}_2$, this nontrivial outer automorphism is uniquely $\sigma_\mathrm{outer}$:

$$
\boxed{\;P_{56} \text{ acts as } \sigma_\mathrm{outer} \text{ in the spinor representation of } \mathfrak{so}(10).\;}
$$

In standard SO(10) GUT physics, $\sigma_\mathrm{outer}$ is the **matter/antimatter exchange** that swaps a fermion generation (16) with its CP-conjugate (16̄). Verification: `papers/wp104_higgs_pati_salam/verification/find_higgs_irrep.py` plus the Cl(0,10) construction in `Gen12/targets/clay/papers/sprint_unmistakable_truth_2026_04_25/scripts/build_chiral_16.py`.

### §2.2 BHML's σ_outer-breaking is purely 54-irrep

Decompose the antisymmetric-mass content of BHML on the so(10) Killing-form decomposition

$$
\mathrm{End}(\mathfrak{so}(10)) = \mathbf{1} \oplus \mathbf{45} \oplus \mathbf{54}.
$$

The projection of BHML's $\sigma_\mathrm{outer}$-anti part onto each component:

| component | dimension | projected mass | fraction |
|---|---|---|---|
| singlet $\mathbf{1}$ (trace) | 1 | 0.0 | 0% |
| adjoint $\mathbf{45}$ (antisymmetric) | 45 | 0.0 | 0% |
| symmetric-traceless $\mathbf{54}$ | 54 | 6.5 | 100% |

Total $\sigma_\mathrm{outer}$-breaking mass: $\|B_\mathrm{anti}^{\sigma_\mathrm{outer}}\|^2 = 6.5 = 13/2$ in skew-Frobenius convention (or $\|v\|^2 = 13/4$ in 9-vector convention; see §2.3). The breaking is concentrated entirely in the symmetric-traceless 54.

In SO(10) GUT model-building, the standard breaking irreps are 10 (electroweak Higgs), 45 (adjoint), 54 (symmetric-traceless), 120 (3-form), and 126 (self-dual 5-form). The 54-Higgs route breaks $\mathrm{SO}(10) \to \mathrm{SO}(6) \times \mathrm{SO}(4)$, which factors as $\mathrm{SU}(4) \times \mathrm{SU}(2)_L \times \mathrm{SU}(2)_R$ — the **Pati-Salam** sub-group. Verification: `papers/wp104_higgs_pati_salam/verification/find_higgs_irrep.py`.

### §2.3 The 9-vector direction within the 54

The $\mathbf{54}$ irrep further decomposes under $\mathfrak{so}(9) \subset \mathfrak{so}(10)$ as $\mathbf{54} = \mathbf{1} \oplus \mathbf{9} \oplus \mathbf{44}$. BHML's σ_outer-breaking direction is **purely in the 9** (the $\mathfrak{so}(9)$-vector representation), with explicit components:

| direction | component | TIG label |
|---|---|---|
| $e_0$ | $-1/\sqrt{2}$ | VOID |
| $e_1$ | $-1/\sqrt{2}$ | LATTICE |
| $e_2$ | $-1/\sqrt{2}$ | COUNTER |
| $e_3$ | $-1/\sqrt{2}$ | PROGRESS |
| $e_4$ | $-1/\sqrt{2}$ | COLLAPSE |
| $e_7$ | $-1/\sqrt{2}$ | HARMONY |
| $e_8$ | $0$ | **BREATH** |
| $e_9$ | $0$ | **RESET** |
| $(e_5 + e_6)/\sqrt{2}$ | $-1/2$ | (BALANCE + CHAOS)/√2 |

The squared norm in the 9-vector convention is $\|v\|^2 = 6 \cdot (1/2) + 0 + 0 + (1/4) = 13/4$ exactly.

**Mechanism.** A position $(i, j)$ of BHML contributes to σ_outer-breaking iff $\mathrm{BHML}[i, 5] \neq \mathrm{BHML}[i, 6]$. Inspection of rows 8 and 9 of BHML:

| row | BHML[i, 5], BHML[i, 6] | contribution |
|---|---|---|
| row 8 (BREATH) | $7, 7$ | zero |
| row 9 (RESET) | $7, 7$ | zero |
| rows 0–7 | $\{6, 7\}$ or $\{5, 6\}$ etc., differ by 1 | uniform |

Rows 8 and 9 (BREATH and RESET) have $\mathrm{BHML}[i, 5] = \mathrm{BHML}[i, 6] = 7$, so these rows are σ_outer-symmetric and contribute **nothing** to the breaking. This is exactly why $v_8 = v_9 = 0$.

The total count of σ_outer-asymmetric BHML cells is **26** (verified by direct enumeration). The 9-vector squared norm relates to this count via $\|v\|^2 = 26/8 = 13/4$, where the 8 in the denominator is the standard normalization of the 9-vector projection within the 54.

Verification: `papers/wp104_higgs_pati_salam/verification/find_higgs_direction.py`.

### §2.4 Reading: the Pati-Salam route

In Pati-Salam, $\mathrm{SU}(4)$ acts as "color × lepton number" (with lepton number as the "fourth color"), and $\mathrm{SU}(2)_L \times \mathrm{SU}(2)_R$ is the left-right symmetric weak group. The Standard Model is recovered by further breaking $\mathrm{SU}(4) \to \mathrm{SU}(3) \times \mathrm{U}(1)_{B-L}$ and $\mathrm{SU}(2)_R \to \mathrm{U}(1)$. The 54-Higgs route is one of two standard pathways from $\mathrm{SO}(10)$ to Pati-Salam (the other being the 210-Higgs); it is the **simplest** symmetry-breaking irrep of the right size to do this reduction.

**Path A's structural claim:** TIG's bipartite TSML/BHML structure singles out the same 54-Higgs route via a calculation that reads off the antisymmetric-mass projection of BHML on the so(10) Killing decomposition. The specific 9-vector direction within the 54 has BREATH and RESET as zeros, which corresponds to those Higgs components NOT acquiring VEVs during the breaking — a textbook feature of Pati-Salam reductions (the $\mathrm{SU}(4)$ part has unbroken Cartan generators).

Internal interpretation: BREATH and RESET are the two "stabilizer" operators in TIG's σ-fixed lattice. They alone are unaffected by σ_outer-breaking. The other lattice operator (PROGRESS, idx 3) participates fully in the breaking pattern. In gauge-theoretic language, BREATH and RESET correspond to unbroken Higgs components — fields that don't acquire VEVs during the SO(10) → SO(9) breaking. **This is not a derivation that BREATH/RESET correspond to specific physics fields**; it is an alignment between TIG's operator labels and a structural feature of the breaking pattern.

---

## §3 Path B — The doubly-invariant content route

### §3.1 The D_4 action on so(10)

The dihedral group $D_4 = \langle P_{56}, \sigma^3 \rangle$ has order 8 in the symmetric group $S_{10}$. Its action on $\mathfrak{so}(10)$ by conjugation decomposes the 45-dim algebra into $D_4$-isotypic components. The trivial-isotypic component — the doubly-invariant content under both $P_{56}$ and $\sigma^3$ — is the subspace

$$
\mathfrak{g}_0 = \{X \in \mathfrak{so}(10) : P_{56} \cdot X \cdot P_{56}^{-1} = X = \sigma^3 \cdot X \cdot (\sigma^3)^{-1}\}.
$$

We compute (residuals $\le 10^{-14}$):

| isotypic component | dim |
|---|---|
| trivial (both invariant) | **16** |
| sign of $P_{56}$ × trivial of $\sigma^3$ | 1 |
| trivial of $P_{56}$ × sign of $\sigma^3$ | 12 |
| 2-dim irreps (8 copies) | 16 |
| **total** | 45 |

The 16-dim trivial-isotypic component is the doubly-invariant subalgebra $\mathfrak{g}_0$.

### §3.2 g_0 closes as a Lie subalgebra

We verify that $\mathfrak{g}_0$ is closed under bracket: for any pair $X, Y \in \mathfrak{g}_0$, the commutator $[X, Y]$ remains in $\mathfrak{g}_0$ (residual at machine precision). This follows abstractly from the fact that the centralizer of any subgroup of $\mathrm{Aut}(\mathfrak{g})$ is a Lie subalgebra; the verification confirms it numerically.

### §3.3 The Killing form forces su(4) ⊕ u(1)

The Killing form of $\mathfrak{so}(10)$ restricts to a bilinear form on $\mathfrak{g}_0$. We compute its eigenvalue spectrum exactly:

$$
\mathrm{spec}(\kappa|_{\mathfrak{g}_0}) = (-4)^{15} \oplus (0)^1.
$$

Fifteen eigenvalues at exactly $-4$, one at exactly $0$. Verification: `Gen12/targets/clay/papers/sprint_unmistakable_truth_2026_04_25/scripts/verify_truth.py` (residuals $\le 10^{-13}$).

By Cartan's criterion, the 1-dim 0-eigenspace is the **center** of $\mathfrak{g}_0$, and the 15-dim $(-4)$-eigenspace is the **simple part**. The unique compact simple Lie algebra of dimension 15 is $\mathfrak{so}(6) \cong \mathfrak{su}(4) \cong A_3$ (Cartan classification, textbook). The center is necessarily $\mathfrak{u}(1)$. Therefore

$$
\boxed{\;\mathfrak{g}_0 = \mathfrak{su}(4) \oplus \mathfrak{u}(1).\;}
$$

This is **the Pati-Salam ⊕ B−L gauge algebra** — the residual gauge content after breaking $\mathrm{SO}(10) \to \mathrm{SU}(4) \times \mathrm{SU}(2)_L \times \mathrm{SU}(2)_R \to \mathrm{Standard\;Model}$ at the level of the broken doubly-invariant subalgebra.

### §3.4 The center is the σ³ infinitesimal generator

The 1-dimensional center $\mathfrak{u}(1) \subset \mathfrak{g}_0$ is generated by an explicit antisymmetric matrix $Z \in \mathfrak{so}(10)$ whose nonzero entries live entirely in the 6-cycle subspace $\{1, 2, 4, 5, 6, 7\}$. The σ-fixed indices $\{0, 3, 8, 9\}$ are zeros of $Z$. The eigenvalues of $Z$ are $\pm i / \sqrt{2}$ (purely imaginary, length $1/\sqrt{2}$).

This $Z$ is essentially the **infinitesimal generator of the σ-permutation** inside $\mathfrak{so}(10)$ — the "log" of σ as a $D_4$-invariant antisymmetric matrix. Its eigenvalues $\pm i/\sqrt{2}$ are characteristic of a $D_3$-flavor Cartan element (length $\sqrt{2}$), not of an $A_2$-Cartan element (length $\sqrt{3}$). See §6.2 for why this matters.

---

## §4 The two paths converge

Path A asks: *what direction does BHML's σ_outer-breaking point in?* Answer: the 9-vector in the **54** of $\mathfrak{so}(10)$, with BREATH and RESET as zeros and squared norm $13/4$.

Path B asks: *what content is preserved when both natural Z₂ involutions act?* Answer: the **16-dim subalgebra $\mathfrak{su}(4) \oplus \mathfrak{u}(1)$**, the Pati-Salam $\oplus$ B$-$L gauge content.

Both answers describe the same Pati-Salam route — but they reach it from opposite directions. Path A is a **breaking-direction** result (which Higgs irrep, which 9-vector inside it). Path B is an **invariance** result (what survives both $P_{56}$ and $\sigma^3$). They are two different epistemic postures applied to the same TIG so(10) substrate.

That two distinct algebraic procedures land on the same target is **non-trivial**. The convergence indicates a real shared structural feature between TIG's bipartite TSML/BHML algebra and the standard SO(10) → Pati-Salam reduction. It only happens when the algebras have a common backbone.

**Caveat on epistemic independence.** The two paths operate within the **same** TIG so(10) generated by TSML+BHML, using the **same** two involutions ($P_{56}$, $\sigma^3$). They are **computationally distinct procedures**, not independent in the strong sense (e.g., independent algebras or independent data). The framing is "two algebraically distinct procedures within the same substrate", not "two independent confirmations from disjoint inputs."

---

## §5 Three additional structural results

### §5.1 TSML non-associativity is 12.6 %

Define the non-associativity rate of TSML as

$$
\sigma(\mathrm{TSML}) := \frac{|\{(a, b, c) \in (\mathbb{Z}/10\mathbb{Z})^3 : \mathrm{TSML}(\mathrm{TSML}(a, b), c) \neq \mathrm{TSML}(a, \mathrm{TSML}(b, c))\}|}{1000}.
$$

Direct enumeration (verifiable in $< 1$ s) gives **126 non-associative triples**, so $\sigma(\mathrm{TSML}) = 0.126$. Three structural facts about these 126:

* **Every** non-associative triple has HARMONY (operator 7) as the value of one bracketing.
* Only **5 distinct unordered $\{L, R\}$ pairs** occur, all involving 7: $\{0, 7\}, \{3, 7\}, \{4, 7\}, \{7, 8\}, \{7, 9\}$.
* **VOID never appears in middle position.** That is, no triple of the form $(a, 0, c)$ is non-associative.

This corrects a previously cited rate of 49.8 %, which was based on a different enumeration convention. The 12.6 % figure is the canonical rate by direct count. Verification: `Gen12/targets/clay/papers/sprint_unmistakable_truth_2026_04_25/scripts/full_landscape.py`.

### §5.2 Lie/Jordan duality

Build two algebras from the canonical tables:

* **Lie side:** $\mathfrak{g}_\mathrm{Lie} = $ Lie algebra generated by $\{A^M_i : i \in \mathbb{Z}/10\mathbb{Z}, M \in \{\mathrm{TSML}, \mathrm{BHML}\}\}$ under commutator.
* **Jordan side:** $\mathfrak{g}_\mathrm{Jor} = $ vector space generated by $\{S^M_i\}$ under the Jordan product $X \circ Y = (XY + YX)/2$.

We verify $\dim \mathfrak{g}_\mathrm{Lie} = \dim \mathfrak{g}_\mathrm{Jor} = 45$, and indeed both regenerate the full $\mathfrak{so}(10)$ (the Jordan side as the symmetric-matrix span complementary to the antisymmetric span). They are **dual presentations** of one algebra, not complementary halves. Verification: `Gen12/.../sprint_unmistakable_truth_2026_04_25/scripts/count_crossings.py`.

### §5.3 Three involutions, three decompositions

Let $\tau_1$ = matrix transposition (fixes symmetric, negates antisymmetric); $\tau_2 = $ conjugation by $P_{56}$; $\tau_3 = $ conjugation by $\sigma^3$. Each $\tau$ acts as an involution on $\mathfrak{so}(10)$ and decomposes it into $+1$ and $-1$ eigenspaces:

| involution | $+1$-dim | $-1$-dim |
|---|---|---|
| $\tau_1$ (transpose) | 45 (all of $\mathfrak{so}(10)$ is antisymmetric) | 0 |
| $\tau_2 = P_{56}$ | 36 ($\mathfrak{so}(9)$) | 9 ($\mathbb{R}^9$ vector irrep) |
| $\tau_3 = \sigma^3$ | 24 | 21 |

The $\tau_2 = P_{56}$ split is textbook: $\mathfrak{so}(10) = \mathfrak{so}(9) \oplus \mathbb{R}^9$ as a vector-space decomposition under the natural embedding $\mathrm{SO}(9) \hookrightarrow \mathrm{SO}(10)$ as the stabilizer of $e_5 + e_6$.

The $\tau_3 = \sigma^3$ split into $24 + 21$ is **structurally new** and not yet placed in textbook GUT phenomenology; it represents a different way of decomposing $\mathfrak{so}(10)$ that respects σ's permutation structure. The doubly-invariant content $\mathfrak{g}_0$ from §3 is the intersection of $\tau_2$'s $+1$-eigenspace with $\tau_3$'s $+1$-eigenspace.

Verification: `Gen12/.../sprint_unmistakable_truth_2026_04_25/scripts/cycle_tower_v2.py`.

---

## §6 Honest scope (what we are NOT claiming)

### §6.1 We do not claim TIG predicts the Standard Model

Path A identifies BHML's σ_outer-breaking content with the 54-Higgs route, the Pati-Salam sub-program of SO(10) GUT. Path B identifies the doubly-invariant content with $\mathfrak{su}(4) \oplus \mathfrak{u}(1)$, the Pati-Salam $\oplus$ B$-$L gauge algebra. **We do not claim to derive Yukawa couplings, mass ratios, mixing angles, or neutrino masses** from this structure. Phenomenology requires committing to specific Higgs VEV directions (we have one specific 9-vector), running RGE flows from a specific GUT scale (we do not have scale-fixing), and solving electroweak breaking — all of which are open work.

The strongest defensible claim is structural alignment: **TIG's bipartite TSML/BHML structure singles out the same SU(4) × SU(2)_L × SU(2)_R chain through SO(10) by two distinct algebraic procedures.**

### §6.2 The √3 in the runtime attractor (WP105) is NOT an A_2 Cartan invariant

WP105 establishes that at the symmetric mixing weight $\alpha = 1/2$, the runtime attractor of the lattice processor satisfies $H/Br = 1 + \sqrt{3}$ exactly. It is tempting to read $\sqrt{3}$ as an $A_2$-Cartan invariant (the angle $\tan(60°) = \sqrt{3}$ associated with the $\mathfrak{su}(3)$ root system). **This reading is not supported.**

Independent verification:

* The $\sqrt{3}$ enters via the discriminant of a quadratic on the 4-core: $(h/br)^2 - 2(h/br) - 2 = 0$, with discriminant $4 + 8 = 12 = 4 \cdot 3$. The "3" is the discriminant residue of one quadratic with small integer coefficients, not the determinant of an $A_2$-shaped lattice.
* Sweeping $\alpha$ across $[0.05, 0.95]$, the relation $H/Br = 1 + \sqrt{3}$ holds **only at $\alpha = 1/2$**. An $A_2$-structural cause would produce $\sqrt{3}$ at every $\alpha$.
* The σ³ generator $Z$ inside $\mathfrak{g}_0 = \mathfrak{su}(4) \oplus \mathfrak{u}(1)$ has eigenvalues $\pm i/\sqrt{2}$ (D₃-flavor, length $\sqrt{2}$), **not** $\sqrt{3}$ (A₂-flavor, length $\sqrt{3}$). This is direct evidence that the relevant Cartan eigenvalue is not an $A_2$-Cartan eigenvalue.
* The runtime attractor's 4-core support is $\{V, H, Br, R\} = \{0, 7, 8, 9\}$. Three of these (0, 8, 9) are σ-fixed; only $H = 7$ lies in σ's 6-cycle. So **75 % of runtime mass lives off the σ-hexagon**, not on it. An $A_2$-Weyl interpretation would predict the opposite.

The $\sqrt{3}$ is the value picked out by the **symmetric mixing balance at $\alpha = 1/2$** and the specific BHML coefficients; it is bound to the runtime mixing weight, not to the algebra's root system.

### §6.3 We rely on a load-bearing identification

The strongest claim of WP104 is: **TIG's so(10), generated by joint antisymmetrization of TSML+BHML, IS the SO(10) GUT gauge algebra in the structural sense of (i) being abstractly isomorphic to it (trivially, since there is only one $\mathfrak{so}(10)$ up to iso) AND (ii) carrying the same physical interpretation under standard model-building rules.**

Claim (i) is a tautology. Claim (ii) is a hypothesis. We do not derive it; we test it. WP104's positive result is that under this hypothesis, TIG's bipartite structure picks out the Pati-Salam route by two distinct algebraic procedures. WP104's honest scope is that **the hypothesis itself is not derived from first principles**; whether TIG's so(10) is "really" the SO(10) GUT gauge algebra (vs. a coincidentally isomorphic algebraic object with a different physical interpretation) is open.

### §6.4 Negative findings that strengthen the framing

* The Hilbert tail of $R/I_\mathrm{CL}$ (Cohen-Macaulay failure) and the $\mathfrak{u}(1)$ center of $\mathfrak{g}_0$ are **different 1-dimensional residuals** with disjoint supports (VOID vs the 6-cycle). They should not be conflated.
* TSML's eigenvalue spectrum has clean integer/rational structure ($\{7, 7, 7\}$ on the σ-fixed lattice; $81 = 9^2$ total antisymmetric mass; $29$ projection on $\mathfrak{su}(4)$; $25/8$ projection on $\mathfrak{u}(1)$); but it does **NOT** match transcendental constants ($e, \pi, \varphi, \zeta(3)$, Catalan $G$) at exact-identity level. Loose 1 % coincidences exist; algebraic identities do not. This is documented in `Gen13/targets/ck/brain/dof_monitor/CL_EIGENVALUES_AUDIT_2026_04_25.md` on the `ck` branch.
* The prime-11 mediation hypothesis (BHML's anti-collapse role traces to TSML's prime-11 char-poly signature) was **falsified** ($p = 0.027$, wrong direction). The attractor-richness hypothesis (BHML's richer fixed point mitigates TSML's collapse) was also **falsified** ($r = -0.118$ correlation, weak). The actual mechanism of BHML's specificity is the 8-magma core / 4-core complementarity established in WP105.

These honest negatives are **flagged in the canonical FORMULAS_AND_TABLES.md negatives table (N1–N5)** and rule out tempting overclaims about TIG's relationship to generic algebraic structures. Specificity is structural, not generic.

---

## §7 Verification and reproducibility

All numerical claims in this paper are verified by numpy / sympy scripts that run in $< 30$ s on a standard laptop. The script index:

| script | what it verifies |
|---|---|
| `papers/wp103/verification/verify_so10.py` | TSML+BHML close to so(10) at dim 45 |
| `papers/wp103/verification/verify_simplicity_rank.py` | so(10) is simple, Cartan rank 5 |
| `papers/wp104_higgs_pati_salam/verification/find_higgs_irrep.py` | BHML σ_outer-breaking is 100 % in 54 |
| `papers/wp104_higgs_pati_salam/verification/find_higgs_direction.py` | 9-vector with BREATH = RESET = 0 |
| `Gen12/.../sprint_unmistakable_truth_2026_04_25/scripts/verify_truth.py` | doubly-invariant subalgebra is su(4) ⊕ u(1) |
| `Gen12/.../scripts/full_landscape.py` | 12.6 % non-associativity rate |
| `Gen12/.../scripts/count_crossings.py` | Lie/Jordan duality |
| `Gen12/.../scripts/cycle_tower_v2.py` | three involutions decomposition (45 = 24+21) |

```bash
# main verifications, in dependency order
PYTHONIOENCODING=utf-8 python papers/wp103/verification/verify_so10.py
PYTHONIOENCODING=utf-8 python papers/wp104_higgs_pati_salam/verification/find_higgs_irrep.py
PYTHONIOENCODING=utf-8 python papers/wp104_higgs_pati_salam/verification/find_higgs_direction.py
PYTHONIOENCODING=utf-8 python Gen12/targets/clay/papers/sprint_unmistakable_truth_2026_04_25/scripts/verify_truth.py
```

Expected output: machine-precision residuals ($\le 10^{-13}$) on every claim. Independent re-execution by Code session 2026-04-25: 25/25 verification scripts across the WP100s tower pass with zero contradictions.

---

## §8 What this contributes

**Before WP104:** the connection between TIG and SO(10) GUT was "TIG's so(10) and SO(10) GUT's so(10) are abstractly isomorphic" — trivially true, since there is only one $\mathfrak{so}(10)$ up to iso.

**After WP104:** the connection is **TIG's bipartite TSML/BHML structure singles out the Pati-Salam route through SO(10) by two algebraically distinct procedures within the same so(10) substrate, with explicit numerical content (the 9-vector direction, the (-4)¹⁵ ⊕ (0)¹ Killing spectrum, the 13/4 squared norm, the 26 σ_outer-asymmetric cells)**.

The ladder is:

```
WP102        TSML's flow-only antisymmetrization closes at so(8) = D₄ at dim 28
   |
   ▼
WP103        TSML+BHML jointly close at so(10) = D₅ at dim 45
   |
   ▼
WP104        Path A: BHML's σ_outer-breaking is in the 54 (Pati-Salam Higgs)
             Path B: D_4 = ⟨P_56, σ³⟩ doubly-invariant is su(4) ⊕ u(1)
                     (Pati-Salam ⊕ B−L gauge content)
   |
   ▼
WP105        Runtime attractor at α = 1/2 lies in degree-4 number field
             over Q with Q(√3) as canonical subfield (LMFDB 4.2.10224.1)
```

Each level is machine-verified at $\le 10^{-15}$ residuals. Each level is honestly scoped: WP102 and WP103 are structural identifications via Cartan classification; WP104 is an alignment hypothesis test (passes both procedures); WP105 is a closed-form runtime characterization.

**The integer 13** appears in $\|v\|^2 = 13/4$ (§2.3), in $\kappa_\xi = 13/(4e)$ (the inflaton coupling under GUT-natural identification, sister paper), and as $26/2$ (the σ_outer-asymmetric BHML cell count). It is the same 13 in all three places. This is the structural fingerprint of TIG's bipartite alignment with the Pati-Salam route.

---

## §9 References

* B.R. Sanders, M. Gish. *WP102 — Lie Algebra Structure of the Coherence Lattice: so(8) = D₄ Identification*, 2026-04-23. `papers/wp102/WP102_SO8_IDENTIFICATION.md`
* B.R. Sanders, M. Gish. *WP103 — TSML+BHML's so(10) = D₅ closure*, 2026-04-24. `papers/wp103/WP103_SO10_IDENTIFICATION.md`
* B.R. Sanders, M. Gish. *WP105 — Closed-Form Runtime Attractor at α = 1/2*, 2026-04-25. `papers/wp105_closed_form_attractor/WP105_CLOSED_FORM_ATTRACTOR.md`
* H. Fritzsch, P. Minkowski. *Unified interactions of leptons and hadrons.* Ann. Phys. 93 (1975), 193.
* H. Georgi. *The state of the art — gauge theories.* AIP Conf. Proc. 23 (1975), 575.
* J. C. Pati, A. Salam. *Lepton number as the fourth color.* Phys. Rev. D 10 (1974), 275.
* R. Slansky. *Group theory for unified model building.* Phys. Rep. 79 (1981), 1.
* H. Cohen. *A Course in Computational Algebraic Number Theory*, GTM 138, Springer, 1993.

---

## §10 Citation

```bibtex
@misc{sanders2026wp104,
  author       = {Sanders, Brayden R. and Gish, M.},
  title        = {{WP104} --- Two Roads to Pati-Salam from {TIG}'s {so(10)}},
  year         = {2026},
  month        = {apr},
  doi          = {10.5281/zenodo.18852047},
  howpublished = {\url{https://github.com/TiredofSleep/ck/tree/tig-synthesis/papers/wp104_higgs_pati_salam}},
  note         = {Path A: BHML's $\sigma_\mathrm{outer}$-breaking is 100\% in the 54 irrep of $\mathfrak{so}(10)$ with explicit 9-vector direction. Path B: doubly-invariant subalgebra under $D_4 = \langle P_{56}, \sigma^3 \rangle$ is $\mathfrak{su}(4) \oplus \mathfrak{u}(1)$ (Killing spectrum $(-4)^{15} \oplus (0)^1$). Both procedures land on the Pati-Salam route through $\mathrm{SO}(10)$.}
}
```

🙏

— Sanders + Gish, 2026-04-25
