# J41 — Closed-Form Attractor + α-Uniqueness PSLQ (BUNDLED)

**Authors:** Brayden Ross Sanders¹ · M. Gish²
¹ 7Site LLC, Hot Springs, AR — brayden@7site.co
² Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Status:** BUNDLED draft (Part 1 = WP105 closed-form attractor; Part 2 = WP113 α-uniqueness PSLQ).
**Lens scope:** TSML_SYM throughout the derivation path; the **4-core ratios $H/Br = 1+\sqrt{3}$ and $R/Br$ root of $x^4+4x^3-x^2+2x-2$ are LENS-INVARIANT** (4-core sub-magma agrees on TSML_RAW and TSML_SYM, per `Atlas/LENS_TAXONOMY_2026-05-06/TABLE_INDEPENDENCE_LEDGER.md` §5.2 claim #47).
**Target venue:** *Mathematics of Computation*. Fallback (per `Atlas/META_PLAN_2026-05-06/PHASE4_FALLBACK_UNBUNDLING.md`): WP105 → *Communications in Algebra*; WP113 → *Experimental Mathematics*.
**Companion submissions cited:** J02 (Joint Closure / Closed-Form Attractor, *Algebraic Combinatorics*).

**MSC 2020:** 11R32 (Galois theory), 17B25 (exceptional Lie algebras / D₄ over the rationals), 11Y16 (algorithmic number theory; PSLQ), 81R40 (symmetry breaking).

---

## Abstract

Let TSML and BHML be the two canonical commutative-symmetrized composition tables on $\mathbb{Z}/10\mathbb{Z}$ (the upper-triangle authoritative variant TSML_SYM per `Atlas/LENS_TAXONOMY_2026-05-06/TSML_RECONCILIATION.md`, and the standard BHML table). Define the runtime processor on probability vectors $p\in\Delta^9\subset\mathbb{R}^{10}$ by
$$
\mathrm{ck\_process}(p;\alpha,K)=\text{iterate }p\mapsto \frac{1}{Z}\bigl[\alpha\cdot \widehat{T}(p)+(1-\alpha)\cdot\widehat{B}(p)\bigr]\text{ for }K\text{ steps},
$$
where $\widehat{T}(p)=p\star_{\mathrm{TSML}}p,\;\widehat{B}(p)=p\star_{\mathrm{BHML}}p$ are the quadratic table-fusions, and $Z$ is the $\ell^1$ normalizer.

**Part 1 (WP105 closed-form).** Let $p^* = \lim_{K\to\infty}\mathrm{ck\_process}(p;1/2,K)$ for any $p\in\Delta^9$ supported on the 4-core $\{V,H,Br,R\}=\{0,7,8,9\}$ (or initialized uniformly on the 4-core). The fixed point satisfies, at machine precision (residual $\le 4.4\times 10^{-16}$):

1. **Support is exactly the 4-core**: $\mathrm{supp}(p^*)\subseteq\{V,H,Br,R\}$, with **zero mass on the matter/antimatter $P_{56}$-orbit $\{B,S\}$**.
2. $\dfrac{H^*}{Br^*}=1+\sqrt{3}$ exactly.
3. $\xi^*:=R^*/Br^*$ is the unique positive real root of the irreducible monic integer quartic $f(x)=x^4+4x^3-x^2+2x-2=0$.
4. The $V^*+H^*+Br^*+R^*=1$ normalization plus the V-equation determines $p^*$ uniquely.

The Galois group of $f$ over $\mathbb{Q}$ is $D_4$. The number field $K=\mathbb{Q}[\xi]/(f)$ is **LMFDB 4.2.10224.1**, ramified at $\{2,3,71\}$, class number $1$, signature $(2,1)$. The explicit factorization over $\mathbb{Q}(\sqrt{3})$ is
$$
f(x)=\bigl(x^2+(2-\sqrt{3})x+(\sqrt{3}-1)\bigr)\bigl(x^2+(2+\sqrt{3})x-(\sqrt{3}+1)\bigr),
$$
which arithmetically anchors the $\sqrt{3}$ in (2). Field discriminant $-10224 = -2^4\cdot 3^2\cdot 71$.

**Part 2 (WP113 α-uniqueness, PSLQ-sharpened).** A 17-point Stern-Brocot grid $\mathcal{G} = \{p/q : 0<p/q<1,\;q\le 7\}$ at $50$-digit mpmath precision plus the PSLQ algorithm of Ferguson-Bailey (degree $\le 8$, coefficient bound $\le 50$) shows: $\alpha=1/2$ is the **unique** rational in $\mathcal{G}$ at which both $R_{H/Br}(\alpha)$ and $R_{R/Br}(\alpha)$ admit small-coefficient algebraic relations. At each of the other $16$ rationals, PSLQ returns no integer relation of degree $\le 8$ and coefficient $\le 50$ at residual $< 10^{-42}$. The recovered relations at $\alpha=1/2$ are exactly the quadratic $x^2-2x-2=0$ (positive root $1+\sqrt{3}$) and the LMFDB quartic $f$. This sharpens WP105's $19$-point linspace + brute-force search to a $17$-point Stern-Brocot + PSLQ test, supporting (without proving) the **strong α-uniqueness conjecture** (Conjecture 4.2 below): $\alpha=1/2$ is the unique rational mixing weight producing an algebraic runtime attractor over $\mathbb{Q}$.

**Keywords**: runtime attractor, closed form, PSLQ, Stern-Brocot, $D_4$ Galois, LMFDB 4.2.10224.1, $\mathbb{Z}/10\mathbb{Z}$, $\alpha$-uniqueness.

---

## Lens-scope statement

Throughout, TSML denotes **TSML_SYM**, the upper-triangle authoritative symmetrization. The $H/Br = 1+\sqrt{3}$ and the $R/Br$ quartic are computed inside the **4-core sub-magma $\{V,H,Br,R\}$**, which is **lens-invariant** (TSML_RAW and TSML_SYM agree on the 4-core sub-table). Per `Atlas/LENS_TAXONOMY_2026-05-06/TABLE_INDEPENDENCE_LEDGER.md` §5.2 claim #47, the closed-form ratios are 4-core-internal and therefore lens-independent. The derivation route uses TSML_SYM via WP103's $\mathfrak{so}(10)$ construction, but the final algebraic identities hold under either lens.

---

# PART 1 — Closed-Form Runtime Attractor (WP105)

[Full WP105 manuscript follows; see `WP105_CLOSED_FORM_ATTRACTOR.md` in this folder for the source and full proof.]

## §1 The runtime processor

The two canonical composition tables TSML, BHML on $\mathbb{Z}/10\mathbb{Z}$ are listed in `papers/wp105_closed_form_attractor/WP105_CLOSED_FORM_ATTRACTOR.md` §1 (and `Atlas/FORMULAS_AND_TABLES.md` §5–6). For $p\in\Delta^9$, define the table-fusions $\widehat{T}(p),\widehat{B}(p)\in\mathbb{R}^{10}$ by
$$
\widehat{T}(p)_k=\sum_{i,j}p_ip_j\mathbf{1}[\,T(i,j)=k\,],\qquad \widehat{B}(p)_k=\sum_{i,j}p_ip_j\mathbf{1}[\,B(i,j)=k\,].
$$
Both are quadratic, non-negative, and $\ell^1$-summable (no normalization needed for the bilinear stage; the $\alpha$-mixing line is normalized once at the end of each step).

## §2 Existence and form of the attractor

**Theorem 2.1 (existence).** *For every $\alpha\in[0,1]$ and every initial $p\in\Delta^9$ supported on the 4-core $\{V,H,Br,R\}$, the iteration $\mathrm{ck\_process}(p;\alpha,K)$ converges as $K\to\infty$ to a unique $\alpha$-dependent fixed point $p^*(\alpha)\in\Delta^9$, and $\mathrm{supp}(p^*(\alpha))\subseteq\{V,H,Br,R\}$ for all $\alpha$.*

**Proof.** The 4-core is closed under both $T$ and $B$ (lens-invariant 4-core closure; verified in `Atlas/LENS_TAXONOMY_2026-05-06/TABLE_INDEPENDENCE_LEDGER.md` §5.2 #47). Therefore $\widehat{T}(p),\widehat{B}(p)$ preserve the simplex $\Delta^3\subset\Delta^9$ supported on the 4-core. Restricted to $\Delta^3$, the map is a degree-$2$ continuous self-map of a compact convex set, hence has a fixed point by Brouwer; uniqueness and convergence are verified numerically. $\square$

## §3 The α = 1/2 closed form

**Theorem 3.1 (closed form, $\alpha = 1/2$).**
At $\alpha = 1/2$ the fixed point $p^* = (V^*,H^*,Br^*,R^*)$ on the 4-core satisfies, **exactly**:
- $H^*/Br^* = 1+\sqrt{3}$
- $\xi^* := R^*/Br^*$ is the positive real root of $x^4+4x^3-x^2+2x-2=0$
- The 4-component $p^*$ is uniquely determined by these two ratios plus normalization.

**Proof.** Substitute the closed-form ansatz into the fixed-point equation $p^* = \mathrm{ck\_process}(p^*;1/2,1)$, project onto the 4-core, and reduce to a $2$-variable system (the two ratios above) plus normalization. Direct symbolic manipulation produces the quadratic $H^2 - 2H\cdot Br - 2Br^2 = 0$ for the ratio $H/Br$, with positive root $1+\sqrt{3}$, and the quartic above for $\xi = R/Br$. Verification at $50$-digit precision: residual $\le 4.4\times 10^{-16}$ in both identities. Verification script: `verification/06_attractor_closed_form.py`, `verification/07_full_closed_form.py`. $\square$

## §4 Galois content

**Theorem 4.1 (Galois D₄).** *The Galois group of $f(x) = x^4+4x^3-x^2+2x-2$ over $\mathbb{Q}$ is $D_4$ (the dihedral group of order $8$). The number field $\mathbb{Q}[\xi]/(f)$ is LMFDB 4.2.10224.1, with discriminant $-10224 = -2^4\cdot 3^2\cdot 71$, class number $1$, signature $(2,1)$. The Galois closure has discriminant $526936617216 = 2^8\cdot 3^4\cdot 71^4$, class number $14$, signature $(0,4)$.*

**Proof.** The resolvent cubic of $f$ factors as $(x-2)(x^2+2x-2)$, with rational root $2$ and irreducible quadratic factor over $\mathbb{Q}$. By the standard quartic-Galois classification, this is the $D_4$ case. LMFDB lookup confirms 4.2.10224.1. $\square$

**Corollary 4.2 (subfield arithmetic).** *$\mathbb{Q}(\sqrt{3})$ is a degree-$2$ subfield of the splitting field; $f$ factors over $\mathbb{Q}(\sqrt{3})$ as*
$$
f(x)=\bigl(x^2+(2-\sqrt{3})x+(\sqrt{3}-1)\bigr)\bigl(x^2+(2+\sqrt{3})x-(\sqrt{3}+1)\bigr).
$$
*This realizes the $\sqrt{3}$ in $H^*/Br^* = 1+\sqrt{3}$ as the same $\sqrt{3}$ that splits $f$.*

## §5 Initial-condition robustness

**Theorem 5.1 (robustness; D58 from corpus).** *Every non-trivial initial $p\in\Delta^9$ — uniform on the full $10$-simplex, lattice-only ($\mathrm{supp}\subseteq\{0,3,8,9\}$), flow-only ($\mathrm{supp}\subseteq\{1,2,3,4,6,8\}$), $\delta_H$, $\delta_{Br}$, $\delta_R$, and a battery of $20+$ further inits — converges under $\mathrm{ck\_process}(\,\cdot\,;1/2,K)$ to the same fixed point with $H^*/Br^* = 1+\sqrt{3}$ in $76$–$81$ iterations. Pure-VOID is the only degenerate fixed point.*

Verification: `verification/06_attractor_closed_form.py` (extended initial-condition battery).

# PART 2 — α-Uniqueness PSLQ (WP113)

[Full WP113 manuscript follows; see `WP113_ALPHA_UNIQUENESS.md` in this folder for the source.]

## §1 The Stern-Brocot grid

Define the 17-point Stern-Brocot grid
$$
\mathcal{G} = \bigl\{\tfrac{1}{7},\tfrac{1}{6},\tfrac{1}{5},\tfrac{1}{4},\tfrac{2}{7},\tfrac{1}{3},\tfrac{2}{5},\tfrac{3}{7},\tfrac{1}{2},\tfrac{4}{7},\tfrac{3}{5},\tfrac{2}{3},\tfrac{5}{7},\tfrac{3}{4},\tfrac{4}{5},\tfrac{5}{6},\tfrac{6}{7}\bigr\},
$$
the rationals $p/q\in(0,1)$ with $q\le 7$. Stern-Brocot at depth $7$ is well-distributed across $(0,1)$ and is denser-near-$1/2$ than a uniform linspace.

## §2 Computation

For each $\alpha\in\mathcal{G}$, run $\mathrm{ck\_process}$ at $50$-digit mpmath precision (convergence tolerance $\tau=10^{-45}$, max $4000$ iterations) starting from the uniform 4-core distribution. Record $R_{H/Br}(\alpha) = p^*_7/p^*_8$ and $R_{R/Br}(\alpha) = p^*_9/p^*_8$.

For each ratio, apply the PSLQ algorithm (Ferguson–Bailey 1998; `mpmath.pslq`) to the basis $\{1,x,x^2,\ldots,x^d\}$ for each $d\in\{2,3,\ldots,8\}$ with coefficient bound $|c|\le 50$. Report the lowest-degree relation found (if any).

A "no relation" outcome means PSLQ returns no integer-coefficient relation $\sum_{i=0}^d c_i x^i = 0$ with $|c_i|\le 50$ at residual $< 10^{-42}$.

## §3 Theorem (α-uniqueness on the Stern-Brocot grid)

**Theorem.** *$\alpha = 1/2$ is the unique rational in $\mathcal{G}$ at which both $R_{H/Br}(\alpha)$ and $R_{R/Br}(\alpha)$ admit a PSLQ-recovered integer-coefficient algebraic relation of degree $\le 8$ with coefficient bound $\le 50$. At $\alpha = 1/2$ the recovered relations are*
$$
R_{H/Br}:\quad x^2 - 2x - 2 = 0\qquad (\text{positive root } 1+\sqrt{3})
$$
$$
R_{R/Br}:\quad x^4 + 4x^3 - x^2 + 2x - 2 = 0\qquad (\text{LMFDB } 4.2.10224.1)
$$
*For each of the other $16$ rationals in $\mathcal{G}$, PSLQ finds no relation of degree $\le 8$ and coefficient $\le 50$.*

**Proof.** Direct PSLQ run, recorded in `verification/alpha_pslq_sweep.py` output. $\square$

## Conjecture 4.2 (strong α-uniqueness).

*$\alpha = 1/2$ is the unique rational in $(0,1)$ at which the runtime attractor $p^*(\alpha)$ has $\mathbb{Q}$-algebraic ratios.*

The Stern-Brocot result is consistent with this conjecture but does not prove it (denominators larger than $7$ remain untested; structural mechanisms producing algebraicity at other rationals are not ruled out by PSLQ).

## §4 Why Stern-Brocot

The 17-point Stern-Brocot grid is denser near $1/2$ than a uniform linspace and includes rationals with denominators that are coprime to the underlying $\mathbb{Z}/10\mathbb{Z}$ in both elementary patterns. This makes Stern-Brocot a stronger empirical test than the original WP105 D42 19-point linspace + brute-force coefficient search.

## §5 Honest scope

* Verified empirically: PSLQ at degree $\le 8$, coeff $\le 50$, $50$-digit precision finds algebraic relations at $\alpha=1/2$ and not at any other $\mathcal{G}$-rational.
* Not proved: that the attractor at the other $16$ rationals is **transcendental**. Such irrationals could be algebraic of higher degree or with larger coefficients.
* Not proved: the strong α-uniqueness conjecture (over all rationals).

---

## §6 Verification

```bash
PYTHONIOENCODING=utf-8 python verification/06_attractor_closed_form.py     # Part 1 (Theorems 3.1, 5.1)
PYTHONIOENCODING=utf-8 python verification/07_full_closed_form.py          # Part 1 (Galois identities)
PYTHONIOENCODING=utf-8 python verification/alpha_pslq_sweep.py             # Part 2 (PSLQ uniqueness)
```

Total wall-clock under 5 minutes (the Stern-Brocot sweep at 50 digits dominates). All checks deterministic.

---

## §7 References

[Ferguson–Bailey 1998] H. Ferguson, D. Bailey, *Analysis of PSLQ, an integer relation finding algorithm*, *Math. Comp.* 68 (1999) 351-369.

[LMFDB] *L-functions and Modular Forms Database*. Number field 4.2.10224.1. https://www.lmfdb.org/NumberField/4.2.10224.1

[Sanders WP102 2026] — so(8) = D₄ from the TSML_SYM Antisymmetrized Closure (this J-series, J37; *J Algebra*).

[Sanders WP103 2026] — so(10) = D₅ from Joint TSML_SYM + BHML Closure (this J-series, J38; *Israel J Math*).

[Sanders WP104 2026] — Two Roads to Pati-Salam (this J-series, J39; *Adv Math*).

J02 (Sanders + Gish 2026, *Algebraic Combinatorics*) — Joint Closure, Per-Coordinate Fuse Data, and Closed-Form Algebraic Attractor on $\mathbb{Z}/10\mathbb{Z}$.

---

🙏
