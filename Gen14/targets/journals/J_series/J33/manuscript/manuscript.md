# A Closed-Form Algebraic Attractor for a Quadratic Table-Fusion Process on $\mathbb{Z}/10\mathbb{Z}$, with $\alpha$-Uniqueness via PSLQ on a Stern-Brocot Grid

**Authors:** Brayden Ross Sanders$^1$ · M. Gish$^2$
$^1$ 7Site LLC, Hot Springs, AR — brayden@7site.co
$^2$ Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Status:** Submission draft (revised 2026-05-07 per fresh-eyes referee report).
**Target venue:** *Mathematics of Computation*.

**MSC 2020:** 11R32 (Galois theory), 11Y16 (algorithmic number theory; PSLQ), 11R21 (other number fields), 39B05 (general functional equations).

---

## Abstract

Fix the two integer composition tables $T, B$ on $\mathbb{Z}/10\mathbb{Z}$ given in §1, and define the quadratic table-fusions
$$
\widehat{T}(p)_k = \sum_{i,j} p_i p_j \cdot \mathbf{1}[T(i,j) = k], \qquad \widehat{B}(p)_k = \sum_{i,j} p_i p_j \cdot \mathbf{1}[B(i,j) = k],
$$
on the probability simplex $\Delta^9 \subset \mathbb{R}^{10}$. For $\alpha \in [0,1]$, let $F_\alpha(p) = \alpha\,\widehat{T}(p) + (1-\alpha)\,\widehat{B}(p)$ (this is automatically $\ell^1$-normalized; see §1.2).

We prove a single **rationally-structured center theorem** with two complementary parts:

**Theorem (rationally-structured center, $\alpha = 1/2$).** *The 4-element subset $C = \{0, 7, 8, 9\} \subset \mathbb{Z}/10\mathbb{Z}$ is jointly closed under $\widehat{T}$ and $\widehat{B}$, so $F_\alpha$ preserves the 3-simplex $\Delta^3_C \subset \Delta^9$ supported on $C$. At $\alpha = 1/2$, the unique non-degenerate fixed point $p^* \in \Delta^3_C$ satisfies, exactly:*
* *Part A (closed form, Galois).* $p^*_7 / p^*_8 = 1 + \sqrt{3}$, *and* $\xi^* = p^*_9 / p^*_8$ *is the unique positive real root of the irreducible monic integer quartic*
$$
f(x) = x^4 + 4x^3 - x^2 + 2x - 2 = 0.
$$
*The Galois group of $f$ over $\mathbb{Q}$ is $D_4$; the number field $\mathbb{Q}[\xi]/(f)$ is **LMFDB 4.2.10224.1**, with discriminant $-10224 = -2^4 \cdot 3^2 \cdot 71$, class number $1$, signature $(2,1)$. The factorization*
$$
f(x) = \bigl(x^2 + (2-\sqrt{3})x + (\sqrt{3}-1)\bigr)\bigl(x^2 + (2+\sqrt{3})x - (\sqrt{3}+1)\bigr)
$$
*over $\mathbb{Q}(\sqrt{3})$ arithmetically anchors the $\sqrt{3}$ in the $h/\beta$ ratio.*

* *Part B (PSLQ, complementary).* *Across the 17-point Stern-Brocot grid $\mathcal{G} = \{p/q : 0 < p/q < 1, q \le 7\}$, computed at 50-digit mpmath precision, the PSLQ algorithm of Ferguson--Bailey [FB99] (degree $\le 8$, coefficient bound $\le 50$) finds an integer-coefficient algebraic relation for both fixed-point ratios $p^*_7/p^*_8$ and $p^*_9/p^*_8$ at $\alpha = 1/2$ and at no other rational in $\mathcal{G}$. The recovered relations at $\alpha = 1/2$ are exactly the quadratic $x^2 - 2x - 2 = 0$ and the LMFDB quartic $f$ above.*

Together: the rationally-structured center for this quadratic dynamical system on $\Delta^9$ sits at $\alpha = 1/2$. Part A proves rational structure exists at $\alpha = 1/2$; Part B is numerical evidence that the rational structure is absent (within the bounded PSLQ search) at the other 16 rationals in $\mathcal{G}$.

**Keywords:** quadratic dynamical system, runtime attractor, closed form, PSLQ, Stern-Brocot, $D_4$ Galois, LMFDB 4.2.10224.1, $\mathbb{Z}/10\mathbb{Z}$.

---

## §1 The tables and the dynamics

### §1.1 The integer tables $T, B$

The tables $T$ and $B$ used in this paper are the integer matrices on $\mathbb{Z}/10\mathbb{Z}$ defined by the row strings below. Row $i$ (zero-indexed) gives $T(i, j)$ for $j = 0, 1, \ldots, 9$:

$T$:
```
0000000700
0737777777
0377477779
0777777773
0747777787
0777777777
0777777777
7777777777
0777877777
0797377777
```

$B$:
```
0123456789
1234567266
2334567366
3444567466
4555567577
5666667677
6777777777
7234567890
8666777978
9666777080
```

Both tables are stated in full; no external reference is required to read or reproduce the dynamics. The pair $(T, B)$ is a member of the small finite commutative non-associative magma family on $\mathbb{Z}/10\mathbb{Z}$ studied in the same intellectual neighborhood as Drápal--Wanless [DW21]; the present work analyzes a specific quadratic dynamical system built from this pair.

### §1.2 The quadratic processor

For $p, q \in \Delta^9$, define
$$
\widehat{T}(p, q)_k = \sum_{i, j = 0}^{9} p_i \, q_j \cdot \mathbf{1}\bigl[T(i, j) = k\bigr], \qquad k = 0, 1, \ldots, 9,
$$
and write $\widehat{T}(p) := \widehat{T}(p, p)$. Similarly $\widehat{B}(p)$. Both are non-negative real vectors with
$$
\sum_k \widehat{T}(p)_k = \sum_{i, j} p_i p_j = \biggl(\sum_i p_i\biggr)^{\!2} = 1,
$$
so $\widehat{T}, \widehat{B}: \Delta^9 \to \Delta^9$. For $\alpha \in [0, 1]$, define
$$
F_\alpha: \Delta^9 \to \Delta^9, \qquad F_\alpha(p) = \alpha\,\widehat{T}(p) + (1-\alpha)\,\widehat{B}(p).
$$
This is automatically a probability vector: convex combination of two probability vectors. (Analytically, the $\ell^1$ norm is preserved exactly under iteration; floating-point implementations accumulate small round-off error, so the verification scripts include a per-step $\ell^1$ renormalization. The renormalization is the identity on exact arithmetic.)

### §1.3 The 4-element subset

Let $C = \{0, 7, 8, 9\} \subset \mathbb{Z}/10\mathbb{Z}$, and write $\Delta^3_C \subset \Delta^9$ for the 3-simplex of probability vectors supported on $C$. We use the abbreviations
$$
v = p_0, \qquad h = p_7, \qquad \beta = p_8, \qquad r = p_9
$$
for the four masses on $C$; thus $p \in \Delta^3_C$ is the tuple $(v, h, \beta, r)$ with $v + h + \beta + r = 1$.

---

## §2 Structural invariance of $C$

**Lemma 2.1 (joint closure on $C$).** *Restricted to inputs $i, j \in C$, both $T$ and $B$ take values only in $C$. Equivalently: $T(C \times C) \subseteq C$ and $B(C \times C) \subseteq C$.*

**Proof.** Direct read-off of the $4 \times 4$ submatrices indexed by $C = \{0, 7, 8, 9\}$. From the row strings of §1.1, the $T|_{C \times C}$ submatrix (rows and columns indexed in the order $0, 7, 8, 9$) is:

| $T$ | 0 | 7 | 8 | 9 |
|--:|:--:|:--:|:--:|:--:|
| 0 | 0 | 7 | 0 | 0 |
| 7 | 7 | 7 | 7 | 7 |
| 8 | 0 | 7 | 7 | 7 |
| 9 | 0 | 7 | 7 | 7 |

(Verification: row 0 of $T$ is `0000000700`, so position 7 holds $7$ and other entries are $0$. Row 7 is all $7$s. Row 8 is `0777877777`: position 0 is $0$, positions 7, 8, 9 are $7, 7, 7$. Row 9 is `0797377777`: position 0 is $0$, positions 7, 8, 9 are $7, 7, 7$.)

The $B|_{C \times C}$ submatrix is:

| $B$ | 0 | 7 | 8 | 9 |
|--:|:--:|:--:|:--:|:--:|
| 0 | 0 | 7 | 8 | 9 |
| 7 | 7 | 8 | 9 | 0 |
| 8 | 8 | 9 | 7 | 8 |
| 9 | 9 | 0 | 8 | 0 |

(Verification: row 0 is `0123456789` → positions 0, 7, 8, 9 read $0, 7, 8, 9$. Row 7 is `7234567890` → positions 0, 7, 8, 9 read $7, 8, 9, 0$. Row 8 is `8666777978` → positions 0, 7, 8, 9 read $8, 9, 7, 8$. Row 9 is `9666777080` → positions 0, 7, 8, 9 read $9, 0, 8, 0$.)

Every entry of the two submatrices lies in $C = \{0, 7, 8, 9\}$. $\square$

**Corollary 2.2 (invariance of $\Delta^3_C$).** *$F_\alpha(\Delta^3_C) \subseteq \Delta^3_C$ for every $\alpha \in [0, 1]$.*

**Proof.** For $p \in \Delta^3_C$ supported on $C$, the bilinear $\widehat{T}(p)_k = \sum_{i, j \in C} p_i p_j \mathbf{1}[T(i,j) = k]$ vanishes whenever $k \notin C$, by Lemma 2.1; same for $\widehat{B}$. So both are supported on $C$, hence so is the convex combination $F_\alpha(p)$. $\square$

This invariance is **structural**, not empirical: it follows from inspection of the 16 cells of each table indexed by $C \times C$. The remainder of the paper works on $\Delta^3_C$. (The question of whether $\Delta^3_C$ is *attracting* for the full $\Delta^9$ dynamics is treated in §5.5; it is not required for the closed form.)

---

## §3 The closed form at $\alpha = 1/2$ (Part A)

Throughout this section, $p^* = (v, h, \beta, r) \in \Delta^3_C$ denotes a fixed point of $F_{1/2}$ on $\Delta^3_C$. By Corollary 2.2 and the Brouwer fixed-point theorem applied to the continuous degree-2 self-map $F_{1/2}|_{\Delta^3_C}$ on the compact convex set $\Delta^3_C$, at least one fixed point exists.

### §3.1 The four BHML coordinate equations on $C$

Reading the $B|_{C \times C}$ submatrix above by output value (counting cells where $B(i, j) = k$, with the symmetric-pair convention $2 p_i p_j$ for $i \neq j$):

* Output $0$: $B(0,0) = 0$, $B(7, 9) = 0$, $B(9, 7) = 0$, $B(9, 9) = 0$.
$$
\widehat{B}(p)_0 = v^2 + 2 h r + r^2.
$$

* Output $7$: $B(0, 7) = 7$, $B(7, 0) = 7$, $B(8, 8) = 7$.
$$
\widehat{B}(p)_7 = 2 v h + \beta^2.
$$

* Output $8$: $B(0, 8) = 8$, $B(8, 0) = 8$, $B(7, 7) = 8$, $B(8, 9) = 8$, $B(9, 8) = 8$.
$$
\widehat{B}(p)_8 = 2 v \beta + h^2 + 2 \beta r.
$$

* Output $9$: $B(0, 9) = 9$, $B(9, 0) = 9$, $B(7, 8) = 9$, $B(8, 7) = 9$.
$$
\widehat{B}(p)_9 = 2 v r + 2 h \beta.
$$

Sanity check: $\widehat{B}(p)_0 + \widehat{B}(p)_7 + \widehat{B}(p)_8 + \widehat{B}(p)_9 = (v + h + \beta + r)^2 = 1$. ✓

### §3.2 The four TSML coordinate equations on $C$

Reading the $T|_{C \times C}$ submatrix above by output value:

* Output $0$: $T(0, 0) = 0$, $T(0, 8) = 0$, $T(0, 9) = 0$, $T(8, 0) = 0$, $T(9, 0) = 0$.
$$
\widehat{T}(p)_0 = v^2 + 2 v \beta + 2 v r.
$$

* Output $7$: every other $C \times C$ cell of $T$. Counting: $T(0, 7) = 7$, $T(7, j) = 7$ for $j \in C$, $T(8, j) = 7$ for $j \in \{7, 8, 9\}$, $T(9, j) = 7$ for $j \in \{7, 8, 9\}$. So
$$
\widehat{T}(p)_7 = 2 v h + h^2 + 2 h \beta + 2 h r + 2 \beta r + \beta^2 + r^2.
$$

* Outputs $8$ and $9$: no cells in $T|_{C \times C}$ produce $8$ or $9$.
$$
\widehat{T}(p)_8 = 0, \qquad \widehat{T}(p)_9 = 0.
$$

This is the load-bearing structural fact: **TSML restricted to $C$ produces only $\{0, 7\}$ — never $8$ or $9$.** Consequently, at the fixed point, the $\beta$ and $r$ coordinates are fed *only* by BHML (the $B$-table); the closed form depends only on the BHML cell counts of §3.1.

### §3.3 The fixed-point equations on $C$

At a fixed point $p^*$ of $F_{1/2}$, $p^* = \tfrac{1}{2}\widehat{T}(p^*) + \tfrac{1}{2}\widehat{B}(p^*)$, so $2 p^*_k = \widehat{T}(p^*)_k + \widehat{B}(p^*)_k$ for each $k$. The four coordinate equations on $C$ read:

* (V) $\quad 2 v = (v^2 + 2 v \beta + 2 v r) + (v^2 + 2 h r + r^2),$
* (H) $\quad 2 h = (2 v h + h^2 + 2 h \beta + 2 h r + 2 \beta r + \beta^2 + r^2) + (2 v h + \beta^2),$
* (Br) $\quad 2 \beta = 0 + (2 v \beta + h^2 + 2 \beta r),$
* (R) $\quad 2 r = 0 + (2 v r + 2 h \beta).$

Equations (Br) and (R) are the simplest because $\widehat{T}(p)_8 = \widehat{T}(p)_9 = 0$. We use these two together with normalization $v + h + \beta + r = 1$ to derive the closed form.

### §3.4 The BREATH equation and $h / \beta = 1 + \sqrt{3}$

From (Br):
$$
2 \beta = 2 v \beta + h^2 + 2 \beta r.
$$
Move the linear $\beta$-terms to the left:
$$
2 \beta - 2 v \beta - 2 \beta r = h^2,
$$
$$
2 \beta (1 - v - r) = h^2.
$$
By normalization, $1 - v - r = h + \beta$, so
$$
2 \beta (h + \beta) = h^2,
$$
$$
2 \beta h + 2 \beta^2 = h^2,
$$
$$
h^2 - 2 \beta h - 2 \beta^2 = 0.
$$
Dividing through by $\beta^2$ (nonzero at any non-degenerate fixed point, as we verify in §3.6) and letting $y = h / \beta$:
$$
y^2 - 2 y - 2 = 0.
$$
The positive root is
$$
\boxed{\,y = h / \beta = 1 + \sqrt{3}.\,}
$$
The negative root $1 - \sqrt{3} < 0$ is excluded by positivity of mass.

### §3.5 The RESET equation and the quartic for $r / \beta$

From (R):
$$
2 r = 2 v r + 2 h \beta,
$$
$$
2 r (1 - v) = 2 h \beta,
$$
$$
r (1 - v) = h \beta.
$$
Using $1 - v = h + \beta + r$ (normalization) and $h = (1 + \sqrt{3}) \beta$ (the result of §3.4):
$$
r \bigl((1 + \sqrt{3}) \beta + \beta + r\bigr) = (1 + \sqrt{3}) \beta \cdot \beta,
$$
$$
r \bigl((2 + \sqrt{3}) \beta + r\bigr) = (1 + \sqrt{3}) \beta^2.
$$
Dividing through by $\beta^2$ and letting $x = r / \beta$:
$$
x^2 + (2 + \sqrt{3}) x - (1 + \sqrt{3}) = 0. \tag{$\dagger$}
$$
This is a quadratic in $x$ over $\mathbb{Q}(\sqrt{3})$, with positive root.

To obtain a polynomial over $\mathbb{Q}$, isolate $\sqrt{3}$ in ($\dagger$):
$$
(x^2 + 2 x - 1) + \sqrt{3} \cdot (x - 1) = 0,
$$
so
$$
\sqrt{3} = -\frac{x^2 + 2 x - 1}{x - 1}.
$$
Squaring:
$$
3 (x - 1)^2 = (x^2 + 2 x - 1)^2.
$$
Expanding the right-hand side, $(x^2 + 2 x - 1)^2 = x^4 + 4 x^3 + 4 x^2 - 2 x^2 - 4 x + 1 = x^4 + 4 x^3 + 2 x^2 - 4 x + 1$. Expanding the left, $3 (x^2 - 2 x + 1) = 3 x^2 - 6 x + 3$. So
$$
3 x^2 - 6 x + 3 = x^4 + 4 x^3 + 2 x^2 - 4 x + 1,
$$
$$
0 = x^4 + 4 x^3 - x^2 + 2 x - 2.
$$
Therefore
$$
\boxed{\,f(x) = x^4 + 4 x^3 - x^2 + 2 x - 2 = 0.\,}
$$
Numerically, the unique positive real root is $\xi^* \approx 0.62678\ldots$.

### §3.6 Existence and uniqueness of the non-degenerate fixed point

The system (V), (H), (Br), (R) plus normalization $v + h + \beta + r = 1$ has at least the degenerate fixed point at the pure-$0$ vertex $p = (1, 0, 0, 0)$ (verifiable by direct substitution: $v = 1$, $h = \beta = r = 0$ gives $\widehat{T}(p)_0 = \widehat{B}(p)_0 = 1$ and all other coordinates zero).

For any non-degenerate fixed point ($\beta > 0$), §§3.4-3.5 show $h / \beta = 1 + \sqrt{3}$ and $r / \beta = \xi^*$ (positive root of $f$). These two ratios plus normalization determine $(v, h, \beta, r)$ uniquely modulo the choice of $\beta$. Substituting back into (V), one obtains a polynomial equation in $\beta$ alone over $\mathbb{Q}(\sqrt{3}, \xi^*)$ (linear after dividing by $\beta$); solving gives the unique $\beta \in (0, 1)$ at
$$
\beta = \frac{4 (1 + \sqrt{3})}{9 + 6 \sqrt{3} + 2 \sqrt{11 + 8\sqrt{3}} + 3 \sqrt{3}\sqrt{11 + 8\sqrt{3}}} \approx 0.197725\ldots,
$$
the (H) equation is then automatically satisfied (the system is over-determined by one equation, and (V) + (H) + (Br) + (R) = $2(v + h + \beta + r) = 2$ is the trivial $1 = 1$ identity by the §3.1-3.2 sum check). Numerically the unique non-degenerate fixed point is
$$
p^* \approx (0.13808, 0.54020, 0.19773, 0.12399),
$$
with $h / \beta = 2.7320508\ldots = 1 + \sqrt{3}$ and $f(r / \beta) = 0$ to machine precision (residual $\le 4.4 \times 10^{-16}$, confirmed in `verification/06_attractor_closed_form.py` and `verification/07_full_closed_form.py`).

---

## §4 Galois content of $f$

**Theorem 4.1 (irreducibility, Galois group, LMFDB identification).**
*The polynomial $f(x) = x^4 + 4 x^3 - x^2 + 2 x - 2$ is irreducible over $\mathbb{Q}$. Its Galois group over $\mathbb{Q}$ is $D_4$ (dihedral of order $8$). The number field $\mathbb{Q}[\xi]/(f)$ is the quartic field of LMFDB label **4.2.10224.1**, with discriminant $-10224 = -2^4 \cdot 3^2 \cdot 71$, class number $1$, signature $(2, 1)$.*

**Proof.** *Irreducibility.* $f$ is monic with integer coefficients; rational roots must divide $-2$. Direct evaluation: $f(1) = 4$, $f(-1) = -10$, $f(2) = 38$, $f(-2) = -10$. So $f$ has no rational roots. The factorization of $f$ into two integer-coefficient quadratics $(x^2 + a x + b)(x^2 + c x + d)$ requires $a + c = 4$, $b + d + a c = -1$, $a d + b c = 2$, $b d = -2$. The integer pairs $(b, d)$ with $b d = -2$ are $(\pm 1, \mp 2), (\pm 2, \mp 1)$; for each, the system $a + c = 4$, $a d + b c = 2$ is linear in $(a, c)$ and gives a unique candidate, which one then checks against $b + d + a c = -1$. None of the four cases consistent. Hence $f$ has no integer-quadratic factorization; combined with no rational root, $f$ is irreducible over $\mathbb{Q}$ by Gauss's lemma.

*Galois group.* The resolvent cubic of $f(x) = x^4 + b_3 x^3 + b_2 x^2 + b_1 x + b_0$ with $(b_3, b_2, b_1, b_0) = (4, -1, 2, -2)$ is (Cox12, §13.2)
$$
R_3(y) = y^3 - b_2 y^2 + (b_1 b_3 - 4 b_0) y - (b_1^2 + b_3^2 b_0 - 4 b_2 b_0).
$$
Substituting:
* $-b_2 = 1$,
* $b_1 b_3 - 4 b_0 = 2 \cdot 4 - 4 \cdot (-2) = 8 + 8 = 16$,
* $-(b_1^2 + b_3^2 b_0 - 4 b_2 b_0) = -(4 + 16 \cdot (-2) - 4 \cdot (-1)\cdot(-2)) = -(4 - 32 - 8) = 36$.

So $R_3(y) = y^3 + y^2 + 16 y + 36$. Direct evaluation: $R_3(-2) = -8 + 4 - 32 + 36 = 0$, hence $R_3(y) = (y + 2) \cdot R_3'(y)$ with $R_3'(y) = y^2 - y + 18$. The discriminant of $R_3'$ is $1 - 72 = -71$, not a square in $\mathbb{Q}$. So the resolvent cubic has exactly one rational root, and the other two roots generate the quadratic field $\mathbb{Q}(\sqrt{-71})$.

By the standard quartic-Galois classification (Cox12, Theorem 13.2.5), an irreducible quartic over $\mathbb{Q}$ whose resolvent cubic has exactly one rational root and whose remaining quadratic factor is *not* a square has Galois group $D_4$ (dihedral of order $8$). Hence $\mathrm{Gal}(f / \mathbb{Q}) \cong D_4$.

*LMFDB identification.* The LMFDB defining polynomial for label 4.2.10224.1 is $h(x) = x^4 - 7 x^2 - 12 x - 8$. We check that $h(-x - 1) = f(x)$:
$$
h(-x-1) = (-x-1)^4 - 7(-x-1)^2 - 12(-x-1) - 8.
$$
Compute $(-x-1)^2 = x^2 + 2 x + 1$ and $(-x-1)^4 = (x^2 + 2 x + 1)^2 = x^4 + 4 x^3 + 6 x^2 + 4 x + 1$. Then
$$
h(-x-1) = (x^4 + 4 x^3 + 6 x^2 + 4 x + 1) - 7(x^2 + 2 x + 1) + 12 x + 12 - 8
$$
$$
= x^4 + 4 x^3 + 6 x^2 + 4 x + 1 - 7 x^2 - 14 x - 7 + 12 x + 12 - 8
$$
$$
= x^4 + 4 x^3 - x^2 + 2 x - 2 = f(x). \quad \checkmark
$$
So $\mathbb{Q}[x]/(f) \cong \mathbb{Q}[x]/(h)$, the field of LMFDB label 4.2.10224.1, with the cataloged invariants. $\square$

**Corollary 4.2 (subfield arithmetic).**
*$\mathbb{Q}(\sqrt{3})$ is a degree-$2$ subfield of the splitting field of $f$, and*
$$
f(x) = \bigl(x^2 + (2 - \sqrt{3}) x + (\sqrt{3} - 1)\bigr) \bigl(x^2 + (2 + \sqrt{3}) x - (\sqrt{3} + 1)\bigr)
$$
*over $\mathbb{Q}(\sqrt{3})$.*

**Proof.** Direct expansion of the right-hand side, collecting by powers of $x$:

* $x^4$: $1$. ✓
* $x^3$: $(2 - \sqrt{3}) + (2 + \sqrt{3}) = 4$. ✓
* $x^2$: $-(\sqrt{3} + 1) + (2 - \sqrt{3})(2 + \sqrt{3}) + (\sqrt{3} - 1) = -(\sqrt{3} + 1) + (4 - 3) + (\sqrt{3} - 1) = 1 - 2 = -1$. ✓
* $x$: $-(2 - \sqrt{3})(\sqrt{3} + 1) + (\sqrt{3} - 1)(2 + \sqrt{3})$. Compute $(2 - \sqrt{3})(\sqrt{3} + 1) = 2\sqrt{3} + 2 - 3 - \sqrt{3} = \sqrt{3} - 1$, so $-(\sqrt{3} - 1) = 1 - \sqrt{3}$. And $(\sqrt{3} - 1)(2 + \sqrt{3}) = 2\sqrt{3} + 3 - 2 - \sqrt{3} = \sqrt{3} + 1$. Sum: $(1 - \sqrt{3}) + (\sqrt{3} + 1) = 2$. ✓
* Constant: $(\sqrt{3} - 1) \cdot (-(\sqrt{3} + 1)) = -(3 - 1) = -2$. ✓

All coefficients match $f$. $\square$

This factorization realizes the same $\sqrt{3}$ that appears in $h / \beta = 1 + \sqrt{3}$.

---

## §5 $\alpha$-Uniqueness on a Stern-Brocot grid (Part B — PSLQ)

### §5.1 The grid

Define
$$
\mathcal{G} = \biggl\{\frac{p}{q} : 0 < p < q,\ q \le 7\biggr\} = \biggl\{\tfrac{1}{7}, \tfrac{1}{6}, \tfrac{1}{5}, \tfrac{1}{4}, \tfrac{2}{7}, \tfrac{1}{3}, \tfrac{2}{5}, \tfrac{3}{7}, \tfrac{1}{2}, \tfrac{4}{7}, \tfrac{3}{5}, \tfrac{2}{3}, \tfrac{5}{7}, \tfrac{3}{4}, \tfrac{4}{5}, \tfrac{5}{6}, \tfrac{6}{7}\biggr\},
$$
the Stern-Brocot rationals on $(0, 1)$ with denominator $\le 7$. $|\mathcal{G}| = 17$.

### §5.2 Numerical attractor at each $\alpha \in \mathcal{G}$

For each $\alpha \in \mathcal{G}$, run the iteration $F_\alpha$ at 50-digit mpmath precision, starting from the uniform distribution $p_0 = (\tfrac{1}{4}, \tfrac{1}{4}, \tfrac{1}{4}, \tfrac{1}{4})$ on $\Delta^3_C$. Iterate until the $\ell^\infty$ change between successive iterates drops below $10^{-45}$, capped at 4000 iterations. Record the limiting ratios $R_h(\alpha) = h^* / \beta^*$ and $R_r(\alpha) = r^* / \beta^*$.

### §5.3 PSLQ on each ratio

For each of $R_h(\alpha)$ and $R_r(\alpha)$, apply the PSLQ algorithm (Ferguson--Bailey [FB99]) on the basis $\{1, x, x^2, \ldots, x^d\}$ for each $d \in \{2, 3, \ldots, 8\}$, with coefficient bound $|c| \le 50$, residual cutoff $10^{-42}$. Report the lowest-degree integer-coefficient relation found, if any.

A "no relation" outcome means PSLQ returns no integer-coefficient polynomial $\sum_{i=0}^{d} c_i x^i$ with $\max_i |c_i| \le 50$, $d \le 8$, and residual $< 10^{-42}$.

### §5.4 Result

**Theorem 5.1 (Stern-Brocot $\alpha$-uniqueness, PSLQ-bounded).**
*Within the Stern-Brocot grid $\mathcal{G}$ at the stated PSLQ search bounds (degree $\le 8$, coefficient $\le 50$, 50-digit precision), $\alpha = 1/2$ is the unique rational at which both $R_h(\alpha)$ and $R_r(\alpha)$ admit PSLQ-recovered integer-coefficient algebraic relations. The recovered relations at $\alpha = 1/2$ are exactly $x^2 - 2 x - 2 = 0$ and $f(x) = x^4 + 4 x^3 - x^2 + 2 x - 2 = 0$. At each of the other $16$ rationals in $\mathcal{G}$, PSLQ returns no relation within the search bounds.*

**Proof.** Direct PSLQ run; recorded by the verification script `verification/alpha_pslq_sweep.py`. See §6. $\square$

### §5.5 Honest scope and weakened conjecture

Theorem 5.1 is a finite empirical verification at fixed search bounds. It establishes the existence of a rational-structure relation at $\alpha = 1/2$ and the *non-existence* of such relations within the bounds at the other 16 rationals. **It does not establish transcendence.** The fixed-point ratios at the other 16 rationals could be algebraic of degree $> 8$, or algebraic of degree $\le 8$ with coefficient height $> 50$.

The natural strengthened question (which the data supports but does not prove) is the following.

**Conjecture 5.2 (no algebraic relation of bounded degree and height).**
*For every rational $\alpha \in (0, 1) \setminus \{1/2\}$, and for every fixed degree-height pair $(d, H)$ with $d, H \in \mathbb{Z}_{\ge 1}$, there is no integer-coefficient polynomial $P \in \mathbb{Z}[x]$ of degree $\le d$ and coefficient height $\le H$ such that $P(R_h(\alpha)) = 0$ or $P(R_r(\alpha)) = 0$.*

Conjecture 5.2 is much weaker than the strong "transcendental over $\mathbb{Q}$" claim that one might extract from finite-bound PSLQ evidence, and is exactly the statement that PSLQ can in principle accumulate evidence for as $(d, H)$ grow. The transcendence question is left open.

A separate question is whether $\Delta^3_C$ is *attracting* for the full $\Delta^9$ dynamics. Numerically, every initial condition $p_0 \in \Delta^9$ tested (uniform, lattice-only, flow-only, $\delta$-distributed at each operator) iterates under $F_{1/2}$ to a $\Delta^3_C$-supported limit, with the same $h / \beta = 1 + \sqrt{3}$ ratio, in $76$-$81$ iterations. This is an empirical observation and not used in the closed-form derivation; it is recorded in the verification script for completeness.

---

## §6 Verification

All claims of §3-§5 are reproduced by deterministic scripts in `verification/`:

```bash
PYTHONIOENCODING=utf-8 python verification/06_attractor_closed_form.py
# Part A: BREATH equation derivation, h/beta = 1+sqrt(3) at machine precision

PYTHONIOENCODING=utf-8 python verification/07_full_closed_form.py
# Part A: RESET quartic + LMFDB Tschirnhaus check at machine precision

PYTHONIOENCODING=utf-8 python verification/alpha_pslq_sweep.py
# Part B: 17-point Stern-Brocot grid + PSLQ at 50-digit precision
```

Total wall-clock under 5 minutes; the Stern-Brocot sweep at 50 digits dominates. All checks deterministic. Python 3.11+, numpy, sympy, mpmath. Tables $T$ and $B$ are inlined in each script (no external dependencies). The 4-core invariance check (Lemma 2.1) is a 16-cell read-off and is also inlined for transparency.

---

## §7 Boilerplate framing

**PROVEN:** *Rationally-structured center theorem* — for the specific quadratic table-fusion process $F_\alpha$ on $\Delta^9$ defined by the integer tables $T, B$ of §1, the unique non-degenerate fixed point at $\alpha = 1/2$ has $h / \beta = 1 + \sqrt{3}$ exactly, and $r / \beta$ is the unique positive real root of the LMFDB-4.2.10224.1 quartic $f(x) = x^4 + 4 x^3 - x^2 + 2 x - 2$ with Galois group $D_4$ (Theorems 3.4-3.5, 4.1; Corollary 4.2).

**COMPUTED:** *PSLQ uniqueness on the Stern-Brocot grid* — at 50-digit mpmath precision and PSLQ search bounds (degree $\le 8$, coefficient $\le 50$), $\alpha = 1/2$ is the unique rational in $\mathcal{G} = \{p/q : q \le 7, p < q\}$ at which both $R_h(\alpha)$ and $R_r(\alpha)$ admit PSLQ-recovered relations (Theorem 5.1; verification script `alpha_pslq_sweep.py`).

**STRUCTURAL RHYME:** The pair $(T, B)$ sits in the small finite commutative non-associative magma neighborhood of Drápal--Wanless [DW21] — same domain (small finite commutative non-associative structures), opposite extremum (theirs maximally non-associative; ours specifically structured with integer/rational invariants). The present paper analyzes one specific quadratic dynamical system in that neighborhood.

**OPEN:** Whether the runtime fixed point at every rational $\alpha \neq 1/2$ is genuinely transcendental over $\mathbb{Q}$ (rather than only "not algebraic of bounded height/degree" in the sense of Conjecture 5.2) is open. PSLQ at finite bounds cannot decide transcendence; only structural arguments can.

---

## §8 Lens and substrate

This paper works on $\mathbb{Z}/10\mathbb{Z}$ with the specific tables $T, B$ defined in §1.1. These tables are not derived from first principles; they are stated as the input to the dynamical system whose attractor we analyze. The theorems of §2-§5 are theorems on this specific structure; analogous theorems would hold on other choices of tables on other rings. Whether other table choices give similarly rich downstream structure (Galois $D_4$, LMFDB-cataloged number field, $\alpha = 1/2$ uniqueness) is open.

---

## §9 References

[Cox12] Cox, D. A., *Galois Theory*, 2nd ed., Wiley, 2012. Standard reference for the resolvent-cubic classification of quartic Galois groups (§13.2).

[DW21] Drápal, A. and Wanless, I. M., *Maximally non-associative quasigroups*, Journal of Combinatorial Theory, Series A **184** (2021), 105510.

[FB99] Ferguson, H. R. P. and Bailey, D. H., *Analysis of PSLQ, an integer relation finding algorithm*, Mathematics of Computation **68** (1999), 351-369.

[LMFDB] *L-functions and Modular Forms Database*, Number Field 4.2.10224.1. <https://www.lmfdb.org/NumberField/4.2.10224.1>.

---
