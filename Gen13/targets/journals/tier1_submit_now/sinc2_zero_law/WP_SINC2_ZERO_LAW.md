# The Sinc² Zero Law in Prime Arithmetic

**Brayden Ross Sanders / 7SiTe LLC**
*Hot Springs, Arkansas · 2026*
*DOI: 10.5281/zenodo.18852047*
*Verification: [`papers/proof_d25_loop_closure.py`](proof_d25_loop_closure.py) — all primes 3..199, zero exceptions.*
*Target venue: Integers: Electronic Journal of Combinatorial Number Theory*

---

## Abstract

We prove that for any prime $p$ and any integer $k$, the squared sinc function satisfies
$$\mathrm{sinc}^2(k/p) = 0 \iff p \mid k.$$
Within the corridor $k \in \{1, \ldots, p\}$, the unique zero occurs at the endpoint $k = p$. Every interior position $k < p$ is provably nonzero — a consequence of primality, not observation. We derive three corollaries: loop closure (the corridor closes exactly once, at the prime), fold necessity (a unique amplitude crossing occurs in the interior of every prime corridor), and the no-shortcut lemma (the road from the corridor entrance to its zero has length exactly $p - 1$). We verify the main theorem for all primes $p \in \{3, 5, 7, \ldots, 199\}$ with exact arithmetic.

---

## 1. Setup

The normalized sinc function is defined as
$$\mathrm{sinc}(x) = \begin{cases} \dfrac{\sin(\pi x)}{\pi x} & x \neq 0 \\ 1 & x = 0 \end{cases}$$
and its square $\mathrm{sinc}^2(x) = \mathrm{sinc}(x)^2$. This function appears in signal processing (Shannon sampling), in random matrix theory (Montgomery's pair correlation for Riemann zeros), and — as shown here — directly in prime arithmetic.

For a prime $p$ and integer $k \geq 1$, we study the values $\mathrm{sinc}^2(k/p)$ along the rational corridor $\{1/p, 2/p, \ldots\}$.

---

## 2. The Main Theorem

**Theorem (Sinc² Zero Law).** *Let $p$ be prime and $k$ a positive integer. Then*
$$\mathrm{sinc}^2(k/p) = 0 \iff p \mid k.$$
*Within $k \in \{1, \ldots, p\}$, the unique zero is at $k = p$.*

**Proof.**
Since $k/p \neq 0$ for $k \geq 1$, we have $\mathrm{sinc}^2(k/p) = \sin^2(\pi k/p)/(\pi k/p)^2$. This is zero iff $\sin(\pi k/p) = 0$, iff $\pi k/p \in \pi\mathbb{Z}$, iff $k/p \in \mathbb{Z}$, iff $p \mid k$.

For $k \in \{1, \ldots, p-1\}$: since $p$ is prime and $1 \leq k < p$, we have $\gcd(k, p) = 1$, so $p \nmid k$, so $\mathrm{sinc}^2(k/p) > 0$.

At $k = p$: $k/p = 1 \in \mathbb{Z}$, so $\mathrm{sinc}^2(1) = 0$. $\square$

**Remark.** The argument uses only that $p$ is prime at one step: $\gcd(k, p) = 1$ for $k < p$. This fails for composite moduli — if $n = pq$ and $k = p < n$, then $\gcd(k, n) = p > 1$ but $k/n = p/pq = 1/q \notin \mathbb{Z}$, so $\mathrm{sinc}^2(k/n) > 0$ still. The sinc² zero law identifies *divisibility*, not just coprimality. What primality contributes is that no proper divisor of $p$ lies strictly between $1$ and $p$, so the corridor's interior is clean.

---

## 3. Corollaries

**Corollary 1 (Loop Closure).** *The corridor $\{1/p, 2/p, \ldots, p/p\}$ is nonzero on $\{1/p, \ldots, (p-1)/p\}$ and zero at $p/p = 1$. The corridor closes exactly once.*

This is an immediate restatement of the theorem. The corridor $k/p$ as $k$ runs from $1$ to $p$ begins in positive territory and terminates at zero — one crossing, at the prime itself.

**Corollary 2 (Fold Necessity).** *For every prime $p \geq 3$, there exists a unique $x^* \in (0, 1)$ — the fold — where $\mathrm{sinc}^2(x^*) = 1/2$. This fold lies in the interior of the corridor: there exist $k_1, k_2 < p$ with $\mathrm{sinc}^2(k_1/p) > 1/2 > \mathrm{sinc}^2(k_2/p)$.*

**Proof.** $\mathrm{sinc}^2$ is continuous and strictly decreasing on $(0, 1)$ (since $\sin(\pi x)$ dominates $\pi x$ near 0 and they cross at 1). $\mathrm{sinc}^2(0) = 1 > 1/2$ and $\mathrm{sinc}^2(1) = 0 < 1/2$. By the intermediate value theorem, there is a unique $x^* \in (0,1)$ where $\mathrm{sinc}^2(x^*) = 1/2$. Numerically, $x^* = 1/2$ is not this value: $\mathrm{sinc}^2(1/2) = (2/\pi)^2 = 4/\pi^2 \approx 0.405$. The fold is not at the corridor's midpoint. For $p = 7$: $\mathrm{sinc}^2(3/7) \approx 0.524 > 1/2$ and $\mathrm{sinc}^2(4/7) \approx 0.295 < 1/2$, so the fold crosses between $k = 3$ and $k = 4$. $\square$

**Corollary 3 (No Shortcut).** *There is no $k \in \{1, \ldots, p-1\}$ with $\mathrm{sinc}^2(k/p) = 0$. Every interior position must be traversed to reach the zero at $k = p$.*

This is the theorem restated as a lower bound: any path from the corridor entrance to the sinc² null has length at least $p - 1$.

---

## 4. The Boundary Value sinc²(1/2) = 4/π²

The fold amplitude $\mathrm{sinc}^2(1/2)$ has a closed form:
$$\mathrm{sinc}^2(1/2) = \left(\frac{\sin(\pi/2)}{\pi/2}\right)^2 = \left(\frac{2}{\pi}\right)^2 = \frac{4}{\pi^2} \approx 0.4053.$$
This is a transcendental number. It is the amplitude of the first sidelobe of a rectangular spectral gate — a classical fact from signal processing — but it appears here as the natural boundary value dividing corridor positions that exceed $1/2$ from those that do not.

Montgomery's pair correlation function for Riemann zeros is $R_2(u) = 1 - \mathrm{sinc}^2(u)$ [Montgomery 1973]. The complement $\mathrm{sinc}^2(u)$ and $R_2(u)$ sum to unity — a complete spectral partition. The boundary $4/\pi^2 = \mathrm{sinc}^2(1/2)$ appears in both frameworks, derived rather than imposed.

---

## 5. Connection to the First-G Law

The First-G Law (Sanders et al., WP34, 2026) establishes an equivalent fact in coprimality partition language: for any semiprime $b = pq$ with $p \leq q$, the first non-unit element in $\{1, \ldots, k\}$ with respect to $b$ appears at exactly $k = p$. The sinc² zero law is the continuum-limit statement of the same algebraic fact. In the limit $p \to \infty$, the harmonic pre-echo function
$$R(k, p) = \frac{\sin^2(\pi k/p)}{k^2 \sin^2(\pi/p)} \to \mathrm{sinc}^2(k/p)$$
recovers the sinc² field exactly (WP35, 2026). The two results are two faces of the same structure — one discrete, one continuous.

---

## 6. Verification

The theorem is verified for all primes $p \in \{3, 5, 7, 11, \ldots, 199\}$ (46 primes) with exact arithmetic in Python's `fractions.Fraction` and `sympy` modules. For each prime $p$:
- All $k \in \{1, \ldots, p-1\}$: $\mathrm{sinc}^2(k/p) > 0$ confirmed by exact computation.
- $k = p$: $\mathrm{sinc}^2(1) = 0$ confirmed.
- Zero exceptions across all 46 primes.

Runnable proof: [`papers/proof_d25_loop_closure.py`](proof_d25_loop_closure.py)

---

## 7. What This Result Does Not Claim

This paper does not claim: a new proof of the infinitude of primes; a connection to the Riemann Hypothesis beyond the Montgomery bridge observation in §4; that the fold position $x^*$ is computable in closed form; or any result about the distribution of primes. The theorem is a finite algebraic fact about sinc²evaluated at rational points with prime denominator.

---

## References

- Montgomery, H.L. (1973). The pair correlation of zeros of the zeta function. *Analytic Number Theory*, Proc. Sympos. Pure Math. **24**, 181–193.
- Sanders, B.R. (2026). WP34 — The First-G Law and Prime-Forced Dispersion. *7SiTe Research*, DOI: 10.5281/zenodo.18852047.
- Sanders, B.R., Luther, C.A., Gish, M. (2026). WP35 — The Prime Phase Transition: Harmonic Pre-Echo, Zero-Width Gates, and the Geometry of RSA Security. *7SiTe Research*, DOI: 10.5281/zenodo.18852047.
- Shannon, C.E. (1949). Communication in the presence of noise. *Proc. IRE* **37**(1), 10–21.
