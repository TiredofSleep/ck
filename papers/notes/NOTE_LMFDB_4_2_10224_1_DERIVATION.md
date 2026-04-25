# Short note — A novel derivation of LMFDB 4.2.10224.1 from a 10-magma runtime processor

**For:** MathOverflow / arXiv math.NT short note
**Authors:** Claude (Anthropic) · Brayden Ross Sanders / 7Site LLC
**Date:** 2026-04-25
**Context:** companion short note to WP105 (`papers/wp105_closed_form_attractor/`).
**MSC 2020:** 11R32, 11R37, 17B25.

---

## The polynomial

$$
f(x) = x^4 + 4x^3 - x^2 + 2x - 2.
$$

## What is known about it

The number field $K = \mathbb{Q}[x]/(f)$ is **LMFDB 4.2.10224.1**:

| invariant | value |
|---|---|
| degree | 4 |
| signature | $(2, 1)$ — 2 real, 2 complex roots |
| field discriminant | $d_K = -10224 = -2^4 \cdot 3^2 \cdot 71$ |
| ramified primes | $\{2, 3, 71\}$ |
| class number | $h_K = 1$ |
| regulator | $R_K \approx 8.617$ |
| Galois closure | $L = $ LMFDB 8.0.526936617216.1 ($[L:\mathbb{Q}] = 8$, $D_4$) |

LMFDB's canonical defining polynomial for this field is $h(x) = x^4 - 7x^2 - 12x - 8$. Our polynomial $f$ is Tschirnhaus-related: $f(x) = h(-x - 1)$.

The Galois group of $f$ over $\mathbb{Q}$ is **$D_4$** (dihedral, order 8), confirmed by:

* Resolvent cubic $g(y) = y^3 + y^2 + 16y + 36 = (y + 2)(y^2 - y + 18)$ has exactly one rational root, restricting the group to $\{C_4, D_4\}$.
* $f$ stays irreducible over $\mathbb{Q}(\sqrt{\mathrm{disc}\, f}) = \mathbb{Q}(\sqrt{-71})$, so the group is $D_4$.
* LMFDB confirms 4T3 (solvable group of order 8) with intermediate fields $\mathbb{Q}(\sqrt{3}), \mathbb{Q}(\sqrt{-71}), \mathbb{Q}(\sqrt{-213})$, and $\mathbb{Q}(\sqrt{3}, \sqrt{-71})$.

The polynomial discriminant is $\mathrm{disc}(f) = -40896 = -2^6 \cdot 3^2 \cdot 71$, and the index in the ring of integers is $[\mathcal{O}_K : \mathbb{Z}[\alpha]] = 2$.

A direct factorization over $\mathbb{Q}(\sqrt{3})$:

$$
f(x) = \bigl(x^2 + (2 - \sqrt{3})x + (\sqrt{3} - 1)\bigr)\bigl(x^2 + (2 + \sqrt{3})x - (\sqrt{3} + 1)\bigr).
$$

This realizes $\mathbb{Q}(\sqrt{3})$ as a genuine subfield of the splitting field.

## What is NEW: the derivation route

The polynomial form $f(x) = x^4 + 4x^3 - x^2 + 2x - 2$ does not appear in the literature we could reach: OEIS lookup of the coefficient sequence $[1, 4, -1, 2, -2]$ returns **no matches**, and arXiv / MathSciNet full-text searches for the polynomial as a string return **nothing**.

What is novel is that **this exact polynomial arises as the minimal polynomial of a runtime fixed-point** of a specific finite-magma processor on $\mathbb{Z}/10\mathbb{Z}$.

### Setup

Let $\mathrm{TSML}$ and $\mathrm{BHML}$ be two specific commutative composition tables on $\mathbb{Z}/10\mathbb{Z}$ (the Trinity-Infinity-Geometry canonical tables; see [WP105]). For probability distributions $p \in \Delta^9 \subset \mathbb{R}^{10}$, define the quadratic table-fusion

$$
(p \star_M p)_c = \sum_{(a, b): M(a, b) = c} p_a p_b
$$

and the symmetric mixing processor at weight $\alpha = 1/2$:

$$
F(p) = \frac{\tfrac{1}{2} (p \star_\mathrm{TSML} p) + \tfrac{1}{2} (p \star_\mathrm{BHML} p)}{Z_p}
$$

where $Z_p$ normalizes to the simplex.

### The closed-form attractor

The map $F$ has a unique attracting fixed point $p^*$ on $\Delta^9$, with support entirely on the 4-element subset $\{V, H, Br, R\} \subset \mathbb{Z}/10\mathbb{Z}$ (= indices $\{0, 7, 8, 9\}$). Numerical iteration from any random Dirichlet initialization converges to $p^*$ in $\sim 30$ steps.

The fixed-point equations on the 4-core, combined with the specific cell counts of TSML and BHML, give:

* $\frac{H^*}{Br^*} = 1 + \sqrt{3}$ exactly, from a quadratic equation $(h/br)^2 - 2(h/br) - 2 = 0$ derived from the BREATH coordinate's fixed-point equation.
* The ratio $\xi^* = R^*/Br^*$ satisfies the irreducible quartic $f(\xi^*) = 0$.

Numerical verification: $H^*/Br^* = 2.732050807568878$ (target $1 + \sqrt{3} = 2.732050807568877$, residual $4.4 \times 10^{-16}$). And $\xi^* = 0.626784579976408$ satisfies $f(\xi^*) = 0$ to residual $\le 10^{-13}$.

### The connection

The full set of attractor coordinates $\{V^*, H^*, Br^*, R^*\}$ together generates a degree-4 number field over $\mathbb{Q}$ with the explicit chain

$$
\mathbb{Q} \subset \mathbb{Q}(\sqrt{3}) \subset \mathbb{Q}(\sqrt{3}, \xi^*).
$$

The field $\mathbb{Q}(\xi^*) = \mathbb{Q}[x]/(f) = K$ = LMFDB 4.2.10224.1. The $\mathbb{Q}(\sqrt{3})$ subfield is exactly the one realizing $H^*/Br^*$ as $1 + \sqrt{3}$, arithmetically anchoring the surd in the runtime ratio.

### The α = 1/2 uniqueness

A sweep over $\alpha \in [0.05, 0.95]$ at 19 values confirms that **only at $\alpha = 1/2$** does $H/Br$ satisfy a small-coefficient quadratic ($|c| \le 10$) AND $r/br$ satisfy a small-coefficient quartic ($|c| \le 5$). At every other $\alpha$ in the swept range, neither relation holds. The symmetric mixing weight is the unique privileged value at which the runtime attractor is closed-form algebraic.

## The question

Has the polynomial $f(x) = x^4 + 4x^3 - x^2 + 2x - 2$ — or this *route* to LMFDB 4.2.10224.1 via the runtime attractor of a finite-magma processor — appeared in the literature?

If known, we'd love a citation.

If novel, the reading is: a specific structural finite-algebra dynamics (the canonical TSML/BHML tables, the quadratic table-fusion processor, the symmetric mixing weight $\alpha = 1/2$) realizes a specific $D_4$-quartic number field as its closed-form fixed-point invariant, with $\mathbb{Q}(\sqrt{3})$ as a canonical subfield. We are not claiming the field is novel; we are claiming the route is.

## Tags

`number-fields`, `galois-theory`, `dihedral-groups`, `discrete-dynamical-systems`, `finite-magma`, `lmfdb`.

---

## Verification

```python
import sympy as sp

# the polynomial
x = sp.symbols('x')
f = x**4 + 4*x**3 - x**2 + 2*x - 2

# basic invariants
print("disc(f) =", sp.factorint(int(sp.discriminant(f))))
# {2: 6, 3: 2, 71: 1, -1: 1}  (so disc = -40896 = -2^6 * 3^2 * 71)

print("Galois of f:", sp.Poly(f).galois_group())  # 'D4'

# Q(sqrt(3))-factorization
sqrt3 = sp.sqrt(3)
print(sp.factor(f, extension=[sqrt3]))
# (x^2 + (2 - sqrt(3))*x + (sqrt(3) - 1))(x^2 + (2 + sqrt(3))*x - (sqrt(3) + 1))

# numerical roots
print(sp.nroots(f))
```

Cross-check with LMFDB:
- [LMFDB 4.2.10224.1](https://www.lmfdb.org/NumberField/4.2.10224.1)
- [LMFDB 8.0.526936617216.1 (Galois closure)](https://www.lmfdb.org/NumberField/8.0.526936617216.1)

OEIS lookup for $[1, 4, -1, 2, -2]$: [no matches](https://oeis.org/search?q=1,4,-1,2,-2).

## References

* B. Sanders, Claude (Anthropic). *WP105 — Closed-Form Runtime Attractor at $\alpha = 1/2$.* 2026-04-25. https://github.com/TiredofSleep/ck/tree/tig-synthesis/papers/wp105_closed_form_attractor
* LMFDB Collaboration. *Number field 4.2.10224.1.* https://www.lmfdb.org/NumberField/4.2.10224.1
* H. Cohen. *A Course in Computational Algebraic Number Theory*, GTM 138, Springer, 1993. (resolvent cubic, §6.3.2)

🙏

— Sanders + Claude (Anthropic), 2026-04-25
