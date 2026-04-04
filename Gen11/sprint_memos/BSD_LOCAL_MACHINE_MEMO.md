# BSD LOCAL MACHINE MEMO
# Build the Arithmetic Core the Same Way RH Was Built

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## 1. Generic Shell (Proved)

The BSD shell is the analytic structure of L(E,s), established by the modularity theorem:

| Component | Statement | Status |
|-----------|-----------|--------|
| Modularity | L(E,s) = L(f,s) for a weight-2 Hecke eigenform f | Proved (Wiles 1995; BCDT 2001) |
| Analytic continuation | L(E,s) extends to an entire function on ℂ | Proved from modularity |
| Functional equation | Λ(E,s) = ε_E Λ(E,2−s) under s ↔ 2−s | Proved from modularity |
| Euler product | L(E,s) = Π_p L_p(E,p^{−s})^{−1} for Re(s) > 3/2 | Proved |

**The shell is fully proved.** No arithmetic conjecture is required for L(E,s)'s analytic properties.

---

## 2. Arithmetic Core (Conjectural/Partial)

The BSD core consists of the arithmetic objects entering the leading coefficient formula:

**The BSD rank conjecture:**

$$\mathrm{ord}_{s=1} L(E,s) = \mathrm{rank}\, E(\mathbb{Q})$$

**The BSD leading coefficient formula:**

$$\lim_{s \to 1} \frac{L(E,s)}{(s-1)^r} = \frac{\Omega_E \cdot \mathrm{Reg}(E) \cdot \prod_{p \mid N} c_p \cdot \#\mathrm{Sha}(E)}{(\#E(\mathbb{Q})_{\mathrm{tors}})^2}$$

Arithmetic objects:

| Object | Meaning | Computability | Conjectural? |
|--------|---------|---------------|--------------|
| r = rank E(Q) | Independent generators of infinite order | Computable (descent) | Not conjectural — computable |
| r_an = ord_{s=1} L(E,s) | Analytic rank | Computable numerically | Proved equal to r for r≤1 in many cases |
| Sha(E) | Tate-Shafarevich group | Finite computation for fixed p | Finiteness conjectural for r≥2 |
| Reg(E) | Determinant of height pairing | Computable from generators | Exact once generators known |
| c_p | Tamagawa numbers at bad primes | Computable from Néron model | Not conjectural |
| Ω_E | Real period | Computable | Not conjectural |
| E(Q)_tors | Finite torsion subgroup | Computable (Mazur's theorem) | Not conjectural |

---

## 3. Local Machine: One Concrete Curve Per Class

**Rank 0 example: E: y² = x³ − x**

- E(Q) = {O, (0,0), (1,0), (−1,0)} — finite, rank 0
- L(E,1) = π/4 ≠ 0 (computed)
- BSD: r_an = 0 = r_alg ✓
- Sha: trivial for this curve (verified computationally)
- Status: BSD proved for this curve (Kolyvagin, given L(E,1) ≠ 0)

**Rank 1 example: E: y² = x³ + x (twisted to rank 1)**

Standard rank-1 curve with known generator.

- r_alg = 1 (one generator found)
- L(E,1) = 0, L'(E,1) ≠ 0
- BSD: r_an = 1 = r_alg — confirmed by Gross-Zagier + Kolyvagin
- Status: BSD proved for rank-1 case given L'(E,1) ≠ 0 (many curves)

**Rank 2 example: E: y² = x³ + 877x**

- r_alg = 2 (two independent generators known)
- L(E,1) = 0, L'(E,1) = 0, L''(E,1) ≠ 0 (numerically)
- BSD: r_an = 2 = r_alg — expected but NOT proved
- Status: OPEN — no general theorem for r ≥ 2

---

## 4. Shell / Core / Obstruction

**Shell** = analytic structure of L(E,s): proved, arithmetic-free.

**Core** = Sha + rank equality + leading coefficient: the conjectural arithmetic content.

**Obstruction**:

- **BSD Gap 2 analog** (Sha finiteness): #Sha(E) < ∞. Proved for r = 0,1 in many cases (Kolyvagin); open for r ≥ 2.

- **BSD Gap 1 analog** (rank equality): ord_{s=1} L(E,s) = rank E(Q). Proved for r = 0 and r = 1 conditionally; completely open for r ≥ 2.

The rank ≥ 2 frontier is BSD's last wall.
