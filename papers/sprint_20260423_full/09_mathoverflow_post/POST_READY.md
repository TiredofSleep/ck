# Post-Ready Content — MathOverflow

**Status (2026-04-24):** POSTED. Live at
[mathoverflow.net/questions/510662](https://mathoverflow.net/questions/510662/structural-explanation-for-bottom-strand-betti-beta-8-10-1-beta-9-11-2).
This file is retained as the canonical record of what was pasted.

**Source draft:** `DRAFT_MATHOVERFLOW_POST.md` (commit `aee6844`).

This file isolates the exact text that goes into the MathOverflow
"Ask Question" form. Three fields: **Title**, **Body**, **Tags**.
Everything below each heading is ready to copy-paste into the
corresponding form field.

**Tag note:** the original 5-tag suggestion listed
`projective-dimension` and `koszul-algebras`; MO flagged both as
non-existent tags at submit time. The live post uses
`cohen-macaulay-rings` (for the Cohen-Macaulay result) and
`koszul-duality` (the canonical MO tag for Koszul-adjacent material)
in their place. The tag block below is preserved as originally
suggested so that a future reader can see the swap.

---

## Title

MathOverflow's title field has a **150-character limit** (raw, including
LaTeX markup). The draft's proposed long title is ~215 chars — over
limit. Two in-limit options:

**Option A** — specific Betti numbers in the title (137 chars, searchable
by the literal Betti triple):

```
Structural explanation for bottom-strand Betti $\beta_{8,10}=1, \beta_{9,11}=2, \beta_{10,12}=1$ of a non-Koszul 10-variable binomial ideal
```

**Option B** — more readable, loses the specific strand values (103 chars):

```
Structural reason for bottom-strand Betti numbers $(1,2,1)$ of a 10-variable non-Koszul binomial ideal
```

Recommendation: **A**. MO search is keyword-based; the literal
`\beta_{8,10}` and `\beta_{9,11}` strings are rare enough that anyone
searching for this exact resolution shape will land on the post.

---

## Tags (5, space-separated on the form)

```
ac.commutative-algebra projective-dimension koszul-algebras binomial-ideals free-resolutions
```

All five are existing MO tags (verified from the Mantero/Conca
literature on commutative-algebra questions). Within MO's 5-tag cap.

---

## Body

Paste everything between the two `=====` markers below into the MO
Body field. MO renders markdown + MathJax; no conversion needed.

```
============================================================
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
Macaulay2 input, is in [the companion file `betti_output.txt`][betti-log]).

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
- Auslander–Buchsbaum saturates:
  $\mathrm{pd} + \mathrm{depth} = 10 = \mathrm{numgens}\, R$.
- **$A$ is not Cohen–Macaulay.**
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
$\sigma(i) := \mathrm{CL}[i][i]$ has cycle structure
$(0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$ under iteration on the 10-element
ground set.

[betti-log]: https://github.com/TiredofSleep/ck/blob/mantero-bridge-2026-04-23/papers/sprint_20260423_full/09_mathoverflow_post/betti_output.txt

### 3. What I am asking

**(Q)** Is there a structural explanation for the specific non-linear
syzygies of $A$ — concretely, for the bottom-strand Betti numbers
$\beta_{8,10}(A) = 1$, $\beta_{9,11}(A) = 2$, $\beta_{10,12}(A) = 1$?

Two candidate mechanisms I would like to distinguish:

- **(a) Obstruction from non-associativity.** The underlying
  multiplication $x_i \cdot x_j := x_{\mathrm{CL}[i][j]}$ fails
  associativity at 128 of 1000 ordered triples. The natural
  expectation is that the bottom-strand obstructions are generated
  (as a sub-complex of the syzygy module) by the $128 - (\text{symmetric duplicates})$
  associativity-failure triples. Concretely: is there an "associative
  closure" of $I$ — i.e. an ideal $\tilde I \supseteq I$ generated by
  $I$ plus the associativity relations
  $\{x_{\mathrm{CL}[\mathrm{CL}[i][j]][k]} - x_{\mathrm{CL}[i][\mathrm{CL}[j][k]]}\}$ —
  whose quotient $R/\tilde I$ has a linear resolution (i.e., is Koszul)?

- **(b) Stanley–Reisner obstruction.** The squarefree monomial ideal

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
  standard families have Hilbert series matching the
  $(1 + 9t - 8t^2 - t^3)/(1-t)$ above.
- The two tiny-ground-set classifications of non-Koszul ideals with
  small Betti tables (e.g. Conca–Trung–Valla) do not reach
  $10$-variable non-Koszul binomials of this form.

### 5. Reproducibility

Full reproducibility bundle at
[GitHub: `ck/papers/sprint_20260423_full/`](https://github.com/TiredofSleep/ck/tree/mantero-bridge-2026-04-23/papers/sprint_20260423_full).

**Scripts in the `09_mathoverflow_post/` folder:**

- `compute_betti.m2` — Macaulay2 script. Reads the table, builds $I$,
  runs `betti res R^1/I` and `hilbertSeries R^1/I`. ~30 s on
  SageMathCell; local M2 installations run in under 5 s.
- `betti_output.txt` — captured run log from the 2026-04-24 execution
  (SageMathCell), including the full Betti table, the Hilbert series,
  the derived invariants, and the M2 version + return code.

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
============================================================
```

---

## Pre-submit checks (do in order)

1. Paste **Title** (Option A or B from above) into the Title field.
2. Paste the **Body** (everything between the `===` markers) into
   the Body field. Confirm the first line reads `### 1. Setup` and
   the last line reads `not the subject of this post.`
3. Paste the five **Tags** into the Tags field.
4. Scroll the preview for: (a) the $10 \times 10$ matrix rendering
   correctly, (b) the Betti-table code block preserved, (c) the
   `[betti-log]` link resolving to the GitHub URL.
5. Once live, update
   `papers/sprint_20260423_full/08_correspondence/mantero_exchange.md`
   `Status` block with the permanent MO link, and send Dr. Mantero a
   short note with that link.

---

## If you prefer to stay entirely manual

The MathOverflow "Ask Question" URL is `https://mathoverflow.net/questions/ask`.
You need to be signed in (check top-right corner). There is no API for
posting questions — the Ask form is the only path.
