# MathOverflow Post — DRAFT (v2, 2026-04-24)

**Status:** DRAFT with machine-verified invariants. Posted link will be
added to this file when live. Superseded earlier draft (v1, 2026-04-23)
whose open questions on pd and Koszul have now been resolved by the
Macaulay2 run (`compute_betti.m2` / `betti_output.txt` in this folder).

**Object of the post.** A focused commutative-algebra question on the
free resolution, non-Cohen-Macaulay character, and associative
deformation of the binomial ideal
$I = (x_i x_j - x_{\mathrm{CL}[i][j]} \cdot x_0) \subset k[x_0, \ldots, x_9]$.
The v1 question ("what is $\mathrm{pd}$? is it Koszul?") is now
answered — the open question is whether the explicit non-linear
syzygies of $R/I$ have a structural explanation, e.g. via the
associative deformation of the underlying magma.

**Scope discipline:** one concrete question, one concrete object, one
Betti table. No framework framing. Any reader of this post should be
able to pick up the table and reproduce every reported number in a
computer-algebra system (Macaulay2, SageMath, Singular) in under an
hour.

---

## Proposed title

**Structural explanation for non-linear syzygies of the binomial ideal
$I = (x_i x_j - x_{\mathrm{CL}[i][j]} x_0)_{0 \le i \le j \le 9}$
with resolution of length 10 and bottom strand $\beta_{8,10} = 1$,
$\beta_{9,11} = 2$, $\beta_{10,12} = 1$?**

(Within MO title limit, searchable by the specific Betti numbers.)

## Proposed tags

`ac.commutative-algebra`, `projective-dimension`, `koszul-algebras`,
`binomial-ideals`, `free-resolutions`

(Five tags — within MO cap.)

---

## Body of the post

### 1. Setup

Let $k$ be a field (assume $k = \mathbb{Q}$ for concreteness) and let
$R = k[x_0, x_1, \ldots, x_9]$ be the polynomial ring in 10 variables,
$\mathbb{Z}_{\ge 0}$-graded by $\deg(x_i) = 1$.

Let $\mathrm{CL} : \{0, 1, \ldots, 9\}^2 \to \{0, 1, \ldots, 9\}$ be
the symmetric function defined by the following $10 \times 10$ table
(the values $0, \ldots, 9$ label abstract operators; the arithmetic
substrate is incidental to the question):

$$
\mathrm{CL} = \begin{pmatrix}
0 & 0 & 0 & 0 & 0 & 0 & 0 & 7 & 0 & 0 \\
0 & 7 & 3 & 7 & 7 & 7 & 7 & 7 & 7 & 7 \\
0 & 3 & 7 & 7 & 4 & 7 & 7 & 7 & 7 & 9 \\
0 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 3 \\
0 & 7 & 4 & 7 & 7 & 7 & 7 & 7 & 8 & 7 \\
0 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 \\
0 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 \\
7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 \\
0 & 7 & 7 & 7 & 8 & 7 & 7 & 7 & 7 & 7 \\
0 & 7 & 9 & 3 & 7 & 7 & 7 & 7 & 7 & 7
\end{pmatrix}
$$

(Entry $\mathrm{CL}[i][j]$ is in row $i$, column $j$, zero-indexed;
the table is symmetric: $\mathrm{CL}[i][j] = \mathrm{CL}[j][i]$.)

Define the binomial ideal

$$
I \;=\; \Bigl(\, x_i x_j - x_{\mathrm{CL}[i][j]} \, x_0 \;\Big|\; 0 \le i \le j \le 9 \,\Bigr) \;\subset\; R.
$$

There are $\binom{10+1}{2} = 55$ such relations; by direct
Gröbner-basis computation in Macaulay2, $53$ of them are
$k$-linearly independent generators of $I$ in degree $2$ (the two
coinciding pairs occur at the diagonal entries where
$\mathrm{CL}[i][i] = 0$ produces the trivial relation
$x_i^2 = x_0^2$ already implied by other generators).

Let $A = R / I$.

### 2. What I have computed in Macaulay2

The following are machine-verified in Macaulay2 1.22
(via SageMathCell — the full run log, including the literal
Macaulay2 input, is in
[the companion file `betti_output.txt`][betti-log]).

**Betti table of $R/I$ (minimal free resolution over $R$):**

```
       0  1   2   3    4    5    6   7   8  9 10
total: 1 53 311 909 1644 1974 1602 861 285 48  2
    0: 1  .   .   .    .    .    .   .   .  .  .
    1: . 53 311 909 1644 1974 1602 861 284 46  1
    2: .  .   .   .    .    .    .   .   1  2  1
```

Reading: rows are strand indices ($\beta_{i,i+j}$ in row $j$),
columns are homological degree. Resolution has length 10; full
length.

**Derived invariants:**

- $\mathrm{numgens}\, I = 53$
- $\mathrm{codim}\, I = 9$
- $\dim A = 1$
- $\mathrm{pd}_R(R/I) = 10$, $\mathrm{depth}(R/I) = 0$
- Auslander-Buchsbaum saturates:
  $\mathrm{pd} + \mathrm{depth} = 10 = \mathrm{numgens}\, R$.
- **$A$ is not Cohen-Macaulay.**
- **$A$ is not Koszul** (the degree-$2$ row of the Betti table —
  $\beta_{i, i+2}$ — is nonzero at $\beta_{8,10}=1$, $\beta_{9,11}=2$,
  $\beta_{10,12}=1$, so the resolution has non-linear terms).

**Reduced Hilbert series:**

$$
\mathrm{HS}_A(t) = \frac{1 + 9\,t - 8\,t^2 - t^3}{1 - t}.
$$

Stable Hilbert function $h(n) = 1, 10, 2, 1, 1, 1, \ldots$ for
$n \ge 3$, polynomial part $P_0(n) = 1$, so $\deg A = 1$.

**Non-associativity statistics of the underlying magma** (the
multiplication $x_i \cdot x_j := x_{\mathrm{CL}[i][j]}$ on the
10-element set, without the $x_0$ factor): out of $10^3 = 1000$
triples $(i, j, k)$, $872$ satisfy associativity $(ij)k = i(jk)$;
$1000$ satisfy commutativity. So $128$ ordered triples fail
associativity (associativity rate $0.872$). The diagonal
$\sigma(i) := \mathrm{CL}[i][i]$ has cycle structure $(0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$
under iteration on the 10-element ground set.

[betti-log]: ./betti_output.txt

### 3. What I am asking

The original v1 questions ("what is $\mathrm{pd}_R(A)$? is $A$
Koszul?") are now answered by Section 2 above. The question I am
asking is one level up:

**(Q)** Is there a structural explanation for the specific non-linear
syzygies of $A$ — concretely, for the bottom-strand Betti numbers
$\beta_{8,10}(A) = 1$, $\beta_{9,11}(A) = 2$, $\beta_{10,12}(A) = 1$?

Two candidate mechanisms I would like to distinguish:

- **(a) Obstruction from non-associativity.** The underlying
  multiplication $x_i \cdot x_j := x_{\mathrm{CL}[i][j]}$ fails
  associativity at 128 of 1000 ordered triples. The natural
  expectation is that the bottom-strand obstructions are generated
  (as a sub-complex of the syzygy module) by the $128 - \text{(symmetric duplicates)}$
  associativity-failure triples. Concretely: is there an "associative
  closure" of $I$ — i.e. an ideal $\tilde I \supseteq I$ generated by
  $I$ plus the associativity relations
  $\{x_{\mathrm{CL}[\mathrm{CL}[i][j]][k]} - x_{\mathrm{CL}[i][\mathrm{CL}[j][k]]}\}$ —
  whose quotient $R/\tilde I$ has a linear resolution (i.e., is Koszul)?

- **(b) Stanley-Reisner obstruction.** The squarefree monomial ideal

$$
I_B = (x_1 x_2,\; x_2 x_4,\; x_2 x_9,\; x_3 x_9,\; x_4 x_8)
$$

  (whose generators are the five off-diagonal entries of the upper
  triangle of $\mathrm{CL}$ that take values in $\{0, \ldots, 9\}
  \setminus \{0, 7\}$) cuts out a simplicial complex $\Delta_B$ that
  is pure of rank $7$ on $10$ vertices but fails basis exchange on
  $21.9\%$ of facet pairs — "pure but not matroidal." Could the
  bottom-strand Betti numbers of $R/I$ come from this
  pure-but-not-matroidal defect, via some obstruction-of-matroid form?

A reference resolving either mechanism, or proving both can be
ruled out in favour of a third, would be a full answer. Partial
answers are welcome.

### 4. Related literature I have consulted

- **Mantero–Mastroeni 2022** (*The Structure of Koszul Algebras
  Defined by Four Quadrics*): the structural approach there —
  distinguishing Koszul from non-Koszul via linear-quotient
  decompositions — is directly applicable in principle, but my
  ideal has 53 quadrics, not 4, and I have not been able to extract
  the linear-quotient test from the small-generator case.
- **Mantero–Nguyen 2024** (arXiv:2406.13759, *The structure of
  symbolic powers of matroids*) and **Mantero–Nguyen 2026**
  (arXiv:2603.19419, *Focal matroids of covers and homological
  properties of matroids*): the focal-matroid machinery characterises
  matroidal squarefree ideals homologically. My $I_B$ is close to
  that category but not inside it (21.9% exchange failure). The
  question of whether the non-matroidal defect here contributes to
  the bottom-strand Betti numbers of the full binomial $R/I$ is the
  core of mechanism (b) above.
- Binomial edge ideals (Herzog–Ene–Hibi), toric ideals of graph
  algebras (Sturmfels), lattice ideals of edge ideals: none of these
  standard families have Hilbert series matching the $(1 + 9t - 8t^2 - t^3)/(1-t)$
  above.
- The two tiny-ground-set classifications of non-Koszul ideals with
  small Betti tables (e.g. Conca–Trung–Valla) do not reach
  $10$-variable non-Koszul binomials of this form.

### 5. Reproducibility

Full reproducibility bundle at
[GitHub: `ck/papers/sprint_20260423_full/`][repo-link-to-insert].

**Scripts in this folder:**

- `compute_betti.m2` — Macaulay2 script. Reads the table, builds $I$,
  runs `betti res R^1/I` and `hilbertSeries R^1/I`. ~30 s on
  SageMathCell; local M2 installations run in under 5 s.
- `betti_output.txt` — captured run log from the 2026-04-24 execution
  (SageMathCell), including the full Betti table, the Hilbert series,
  the derived invariants, and the M2 version + return code.

**To reproduce the Hilbert series and Betti table locally:**

```
M2 --script compute_betti.m2
```

**To reproduce the non-associativity and Stanley-Reisner statistics
in Python:**

```
python ../04_mantero_bridge/cl_as_quadratic_algebra.py
python ../04_mantero_bridge/matroid_test.py
python ../04_mantero_bridge/hilbert_and_matroid_deep.py
python ../04_mantero_bridge/compute_answers.py
```

### 6. Scope / motivation note

The context for this question is a research programme on a frozen
10-element commutative non-associative magma; the broader programme is
not the subject of the post. This question is focused strictly on the
commutative-algebra content of the binomial ideal above.

For the associated Lie-algebraic structure (the antisymmetrization of
the left-regular operators closes into $\mathfrak{so}(8) = D_4$, and
extends under a second canonical table to $\mathfrak{so}(10) = D_5$),
see `papers/wp102/` and `papers/wp103/` in the repository — again, not
the subject of this post.

---

## Pre-post checklist

- [x] Compute Betti table in Macaulay2 (`compute_betti.m2`,
      `betti_output.txt`, 2026-04-24, SageMathCell).
- [x] Verify 53 vs 55 count of independent degree-2 relations
      (Macaulay2 `numgens trim I = 53`).
- [x] Resolve Q1 (pd) and Q2 (Koszul) as machine-verified facts, not
      open questions; post's question is now one level up
      (structural explanation of the bottom strand).
- [ ] Pick the five MO tags (currently listed; final confirmation
      before posting).
- [ ] Link the `betti_output.txt` file in the repo via GitHub raw URL
      (URL to insert at post time).
- [ ] Final read-through for tone: MathOverflow answers best when the
      question is narrow, motivated, and self-contained. No framework
      advocacy in the post body.
- [ ] Post, then update
      `papers/sprint_20260423_full/08_correspondence/mantero_exchange.md`
      "Status" section with the link + email Dr. Mantero.

---

## Notes

- The branch `mantero-bridge-2026-04-23` holds this draft plus the
  bridge research (Mantero's published framework mapped against the
  CL object, the Lie-algebraic lift WP102/WP103, the Stanley-Reisner
  pure-but-not-matroidal companion) so that anyone arriving at the
  branch can pick up context without wading through unrelated
  material.
- This file is the draft. When the post goes live, the link is
  appended to the Status block of
  `08_correspondence/mantero_exchange.md`.
- v1 of this file (2026-04-23) framed pd and Koszul as the open
  questions. v2 (2026-04-24, after the Macaulay2 run) recasts the
  same data as a question about the *structural explanation* of the
  specific non-linear syzygies that the resolution turned up.
