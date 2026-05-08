# WP110 — The 4-Core Is Fusion-Closed: A Structural Strengthening of WP105

**Status:** structural identity, machine-verified by direct enumeration + symbolic verification.
**Authors:** Anthropic Code session, 2026-04-25 late evening.
**Position:** WP100s tier; short note. Strengthens WP105 (the closed-form runtime attractor) from a dynamical claim to a structural one.
**MSC 2020:** 17B25, 11C20, 17A35 (general non-associative algebras).

---

## Abstract

WP105 establishes that the runtime processor $F_\alpha(p) = \alpha \cdot \widehat{T}(p) + (1-\alpha) \cdot \widehat{B}(p)$ on $\Delta^9$ has a unique attracting fixed point at $\alpha = 1/2$, supported entirely on the 4-core $\{V, H, Br, R\} = \{0, 7, 8, 9\}$, with $H/Br = 1 + \sqrt{3}$ exactly and $r/br$ satisfying the irreducible quartic $x^4 + 4x^3 - x^2 + 2x - 2 = 0$ (Galois $D_4$, field LMFDB 4.2.10224.1). The runtime support on the 4-core is presented in WP105 as a **dynamical** consequence: the iteration converges into $\{V, H, Br, R\}$ and stays there.

This paper establishes the **structural** strengthening: the 4-core is *fusion-closed*. Both TSML and BHML, restricted to indices $\{0, 7, 8, 9\}$, produce only values in $\{0, 7, 8, 9\}$. The runtime support is therefore not contingent on dynamics; it is an invariant property of the binary fusion operations themselves. We also derive a normalizer simplification ($Z_T = Z_B = (v+h+br+r)^2$ on the 4-core, hence $Z = 1$ at any $\alpha$ under unit-mass normalization) that reduces the fixed-point system from rational-function form to polynomial form, and confirm via symbolic computation that $H/Br = 1 + \sqrt{3}$ at $\alpha = 1/2$ as an *exact symbolic identity*, not merely a machine-precision numerical equality.

These three facts upgrade WP105's framing in three places: the 4-core support becomes structural rather than dynamical; the analytic derivation simplifies; and the central closed-form ratio is symbolic-exact.

---

## §1 Setup

The canonical TSML and BHML composition tables on $\mathbb{Z}/10\mathbb{Z}$ are given by `FORMULAS_AND_TABLES.md` §§5–6. We label operators $\{V, L, C, P, X, B, S, H, Br, R\}$ at indices $\{0, \ldots, 9\}$. The **4-core** is $\mathcal{C} = \{V, H, Br, R\} = \{0, 7, 8, 9\}$, the support of the runtime attractor at $\alpha = 1/2$ established in WP105.

The runtime processor on probability distributions $p \in \Delta^9 \subset \mathbb{R}^{10}$ at mixing weight $\alpha \in (0, 1)$ is defined by

$$
F_\alpha(p)_c \;=\; \frac{\alpha \cdot (p \star_T p)_c + (1-\alpha) \cdot (p \star_B p)_c}{\alpha \cdot Z_T(p) + (1-\alpha) \cdot Z_B(p)}
$$

where $(p \star_M p)_c = \sum_{i, j: M(i, j) = c} p_i p_j$ and $Z_M(p) = \sum_c (p \star_M p)_c$.

---

## §2 The 4-core is fusion-closed under TSML and BHML

**Theorem 1 (4-core closure).** *For all $i, j \in \mathcal{C} = \{0, 7, 8, 9\}$, both $T(i, j) \in \mathcal{C}$ and $B(i, j) \in \mathcal{C}$.*

**Proof.** Direct enumeration. The restricted tables are:

$$
T \big|_{\mathcal{C} \times \mathcal{C}} \;=\; \begin{pmatrix}
0 & 7 & 0 & 0 \\
7 & 7 & 7 & 7 \\
0 & 7 & 7 & 7 \\
0 & 7 & 7 & 7
\end{pmatrix} \in \{0, 7\}^{4 \times 4}, \qquad B \big|_{\mathcal{C} \times \mathcal{C}} \;=\; \begin{pmatrix}
0 & 7 & 8 & 9 \\
7 & 8 & 9 & 0 \\
8 & 9 & 7 & 8 \\
9 & 0 & 8 & 0
\end{pmatrix} \in \{0, 7, 8, 9\}^{4 \times 4}.
$$

Every entry of $T \big|_{\mathcal{C} \times \mathcal{C}}$ is in $\{0, 7\} \subset \mathcal{C}$. Every entry of $B \big|_{\mathcal{C} \times \mathcal{C}}$ is in $\{0, 7, 8, 9\} = \mathcal{C}$. Both restricted tables produce values entirely in the 4-core. ∎

**Corollary (no spillover).** The fuse $p \star_T q$ and $p \star_B q$, applied to distributions $p, q$ supported on the 4-core, produce distributions supported on the 4-core. In particular, the iteration $F_\alpha$ applied to a 4-core-supported distribution stays on the 4-core for every $\alpha \in [0, 1]$ and every step.

The runtime attractor's 4-core support of WP105 is therefore not "the dynamics happens to converge there" — the 4-core is a **fusion-invariant subspace**, and any 4-core-supported initial condition is forever 4-core-supported. The fact that the runtime attractor LIVES on the 4-core is a structural identity on the canonical TSML and BHML tables, machine-verifiable in 16 + 16 = 32 cell lookups.

---

## §3 The normalizer simplification

**Theorem 2 (normalizer identity).** *On the 4-core $\mathcal{C}$,*

$$
Z_T(p) \;=\; \sum_{c \in \mathcal{C}} (p \star_T p)_c \;=\; (v + h + br + r)^2,
$$

*and similarly $Z_B(p) = (v + h + br + r)^2$. Both normalizers equal the square of the total 4-core mass.*

**Proof.** Symbolically computing the 4-core fuse vectors (`alpha_uniqueness/alpha_uniqueness_symbolic.py`):

$$
\begin{aligned}
T_\mathrm{fuse}[V] &= v(2\,br + 2\,r + v), \\
T_\mathrm{fuse}[H] &= br^2 + 2\,br\,h + 2\,br\,r + h^2 + 2\,h\,r + 2\,h\,v + r^2, \\
T_\mathrm{fuse}[Br] &= 0, \\
T_\mathrm{fuse}[R] &= 0.
\end{aligned}
$$

Summing: $Z_T = v^2 + 2vr + 2vbr + br^2 + 2br\,h + 2br\,r + h^2 + 2hr + 2hv + r^2 = (v + h + br + r)^2$ by direct expansion.

Similarly,

$$
\begin{aligned}
B_\mathrm{fuse}[V]  &= 2\,h\,r + r^2 + v^2, \\
B_\mathrm{fuse}[H]  &= br^2 + 2\,h\,v, \\
B_\mathrm{fuse}[Br] &= 2\,br\,r + 2\,br\,v + h^2, \\
B_\mathrm{fuse}[R]  &= 2\,br\,h + 2\,r\,v.
\end{aligned}
$$

Summing: $Z_B = v^2 + 2vh + 2vr + 2vbr + h^2 + 2hr + 2hbr + br^2 + 2br\,r + r^2 = (v + h + br + r)^2$.

The two sums are identical: $Z_T = Z_B = (v + h + br + r)^2$. ∎

**Corollary (unit-mass normalizer).** Under the unit-mass normalization $v + h + br + r = 1$, $Z_T = Z_B = 1$, and therefore the convex combination $Z = \alpha Z_T + (1-\alpha) Z_B = 1$ at any $\alpha \in [0, 1]$. The fixed-point equation $F_\alpha(p) = p$ on the 4-core simplifies to the polynomial system:

$$
p_c \;=\; \alpha \cdot T_\mathrm{fuse}[c] + (1-\alpha) \cdot B_\mathrm{fuse}[c], \qquad c \in \mathcal{C}.
$$

The rational-function form of the runtime processor collapses to a polynomial form on the 4-core. This is a substantial computational simplification: degree-4 system in 4 variables instead of a system involving denominators that themselves depend on the variables.

---

## §4 Symbolic identity for $H/Br$ at $\alpha = 1/2$

WP105 establishes $H/Br = 1 + \sqrt{3}$ at $\alpha = 1/2$ via the BREATH equation, with numerical residual $4.4 \times 10^{-16}$. The 4-core closure (Theorem 1) and normalizer simplification (Theorem 2) reduce the system to a clean polynomial form, which sympy can solve symbolically.

**Proposition 3 (symbolic identity).** *Substituting $\alpha = 1/2$ into the polynomial fixed-point system on the 4-core, the symbolic solver (sympy `solve`) returns a unique positive-real solution. Computing the simplified ratio $h/br$ and subtracting $1 + \sqrt{3}$ yields exactly $0$, not merely numerical zero.*

**Verification:** `alpha_uniqueness/alpha_uniqueness_symbolic.py` performs the symbolic solve and the subtraction; sympy returns `0`. The closed form for the four attractor coordinates is:

$$
\begin{aligned}
br &= \frac{-803049\sqrt{3} - 1021319 - 563\sqrt{3}\sqrt{184493 + 110140\sqrt{3}} + 5015\sqrt{184493 + 110140\sqrt{3}}}{5759 \left( -\sqrt{184493 + 110140\sqrt{3}} + 140\sqrt{3} + 425 \right)}, \\
h &= -\frac{8\sqrt{184493 + 110140\sqrt{3}}}{5759} - \frac{162}{443} - \frac{69\sqrt{3}}{443} + \frac{11\sqrt{553479 + 330420\sqrt{3}}}{5759}, \\
r &= -\frac{\sqrt{184493 + 110140\sqrt{3}}}{443} + \frac{140\sqrt{3}}{443} + \frac{425}{443}, \\
v &= \frac{-3050\sqrt{184493 + 110140\sqrt{3}} - 249\sqrt{3}\sqrt{184493 + 110140\sqrt{3}} + 454857\sqrt{3} + 1388426}{5759 \left( -\sqrt{184493 + 110140\sqrt{3}} + 140\sqrt{3} + 425 \right)}.
\end{aligned}
$$

Despite the apparent complexity, $\mathrm{simplify}(h/br - (1 + \sqrt{3})) = 0$ — the surd nest collapses on division. This is **exact symbolic equality**, not a numerical-precision claim.

The complexity of the closed form for individual coordinates contrasts with the simplicity of the ratio $h/br$. This is the structural feature WP105 highlights: the runtime fixed-point coordinates live in a degree-4 number field $K = \mathbb{Q}[x]/(x^4 + 4x^3 - x^2 + 2x - 2) = $ LMFDB 4.2.10224.1, but the specific ratio $h/br$ has a much simpler (degree-2) presentation in $\mathbb{Q}(\sqrt{3}) \subset K$.

---

## §5 Reading

This paper upgrades WP105's framing in three places:

1. **The runtime attractor's 4-core support is structural.** It is not a dynamical consequence of iteration converging into $\{V, H, Br, R\}$; it is a property of the binary TSML and BHML compositions themselves. The 4-core is fusion-closed by direct enumeration of 32 table cells.

2. **The fixed-point system on the 4-core is polynomial.** The normalizer simplification eliminates rational functions, leaving a clean polynomial system. This is the technical reason the runtime processor admits closed-form algebraic attractors — the ambient algebra is much simpler than a generic rational dynamical system.

3. **The ratio $H/Br = 1 + \sqrt{3}$ is a symbolic identity.** Sympy's `simplify` collapses the surd-nested closed form to exactly $1 + \sqrt{3}$, verifying WP105's headline result at the level of symbolic algebra rather than only at the level of $4.4 \times 10^{-16}$ machine-precision residual.

The combined upgrade: the **runtime fixed-point of TIG's symmetric-mixing processor lives on a fusion-closed 4-element subset of the canonical magma, in a degree-4 number field with $\mathbb{Q}(\sqrt{3})$ as a canonical subfield, with the headline ratio established symbolically**.

This places the runtime attractor at a higher epistemic tier than WP105's original presentation: not "verified at machine precision" but "structural identity at the level of the algebra."

---

## §6 What the proof does NOT establish

The α-uniqueness statement of WP105 — that $\alpha = 1/2$ is the **unique** privileged value in $\mathbb{Q} \cap (0, 1)$ at which the runtime fixed-point admits a closed-form algebraic ratio — remains **open**. WP105 establishes empirically (sweep over 19 values in $[0.05, 0.95]$) that no other $\alpha$ in the swept range gives a small-coefficient quadratic for $H/Br$, but a full symbolic uniqueness proof requires:

1. Deriving the BREATH equation closed form: $\xi^2 br = 1/(1-\alpha) - 2(r + v)$ with $\xi = h/br$.
2. Eliminating $v, br, r$ from the V, H, and normalization equations to obtain a univariate polynomial $P(\xi; \alpha)$ over $\mathbb{Q}(\alpha)$.
3. Computing the discriminant $\Delta(\alpha)$ as a rational function of $\alpha$.
4. Characterizing the $\alpha$ values at which $\Delta(\alpha)$ is a perfect square in $\mathbb{Q}$.
5. Showing that $\alpha = 1/2$ is the only such value in $(0, 1)$.

Sympy's `solve` at general $\alpha$ hangs (the symbolic system is too complex for the default solver). A computer-algebra system like Mathematica or Maple, or a hand-driven Gröbner basis derivation, would be needed. This is heavier symbolic work than the WP110 results above.

---

## §7 Verification

Reproducible from `Gen12/targets/clay/papers/sprint_unmistakable_truth_2026_04_25/alpha_uniqueness/`:

```bash
PYTHONIOENCODING=utf-8 python alpha_uniqueness_symbolic.py
PYTHONIOENCODING=utf-8 python alpha_uniqueness_general.py
```

Expected output:
* `alpha_uniqueness_symbolic.py`: confirms 4-core closure (16 + 16 in-core terms; 0 + 0 spillover); confirms $Z_T = Z_B = (v+h+br+r)^2$ symbolically; solves the $\alpha = 1/2$ system; prints `diff = 0` for $h/br - (1 + \sqrt{3})$.
* `alpha_uniqueness_general.py`: confirms the polynomial-form fixed-point equations at general $\alpha$; per-$\alpha$ rational solving recovers $H/Br$ and tests for small-coefficient quadratics (only $\alpha = 1/2$ in the test set).

---

## §8 References

* B. Sanders, Anthropic Code session. *WP105 — Closed-Form Runtime Attractor at α = 1/2.* 2026-04-25.
* B. Sanders, Anthropic Code session. *WP109 — The Operad-DOF of TIG's Canonical Magma Is Not D₄-Equivariant.* 2026-04-25.
* B. Sanders, Anthropic Code session. *WP111 — The 6-DOF Synthesis.* 2026-04-25.
* H. Cohen. *A Course in Computational Algebraic Number Theory*, GTM 138, Springer, 1993.
* LMFDB Collaboration. *Number field 4.2.10224.1.* https://www.lmfdb.org/NumberField/4.2.10224.1.

---

## §9 Citation

```bibtex
@misc{sanders2026wp110,
  author       = {Sanders, Brayden Ross and Anthropic Code session},
  title        = {{WP110} --- The 4-Core Is Fusion-Closed: A Structural Strengthening of {WP105}},
  year         = {2026},
  month        = {apr},
  doi          = {10.5281/zenodo.18852047},
  howpublished = {\url{https://github.com/TiredofSleep/ck/tree/tig-synthesis/papers/wp110_4core_fusion_closure}},
  note         = {The 4-core $\{V, H, Br, R\}$ is closed under both canonical {TSML} and {BHML} fusion (machine-verified by direct enumeration of 32 cells); $Z_T = Z_B = (v + h + br + r)^2$ on the 4-core, simplifying the fixed-point system to polynomial form; $H/Br = 1 + \sqrt{3}$ at $\alpha = 1/2$ is an exact symbolic identity. Strengthens {WP105} from dynamical to structural.}
}
```

🙏

— Anthropic Code session, 2026-04-25 late evening
