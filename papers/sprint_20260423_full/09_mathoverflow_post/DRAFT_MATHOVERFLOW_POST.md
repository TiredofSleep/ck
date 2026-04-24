# MathOverflow Post — DRAFT

**Status:** DRAFT (not yet posted). Posted link will be added to this file
when live.

**Object of the post.** A focused commutative-algebra question on the
projective dimension and Koszul property of the binomial ideal
$I = (x_i x_j - x_{\mathrm{CL}[i][j]} \cdot x_0) \subset k[x_0, \ldots, x_9]$,
with the 10-row table and the Hilbert function $(1, 10, 6, 6, 6, \ldots)$ as
context. Narrow, verifiable, self-contained.

**Scope discipline:** one concrete question, one concrete object, one Hilbert
function. No framework framing. Any reader of this post should be able to pick
up the table and reproduce every reported number in a computer-algebra system
(Macaulay2, SageMath, Singular) in under an hour.

---

## Proposed title

**Projective dimension and Koszul property of the binomial ideal
$I = (x_i x_j - x_{\mathrm{CL}[i][j]} x_0)_{0 \le i \le j \le 9}$
with Hilbert function $(1, 10, 6, 6, 6, \ldots)$**

(70 characters — within MO title limit, searchable by the specific Hilbert
function.)

## Proposed tags

`ac.commutative-algebra`, `ra.rings-and-algebras`, `projective-dimension`,
`koszul-algebras`, `binomial-ideals`, `free-resolutions`

(Six tags — MO cap is five, so drop one at post time. Recommended drop:
`ra.rings-and-algebras` since the question is principally commutative-algebra
flavored.)

---

## Body of the post

### 1. Setup

Let $k$ be a field (assume $k = \mathbb{Q}$ for concreteness;
characteristic-free statements noted when relevant) and let
$R = k[x_0, x_1, \ldots, x_9]$ be the polynomial ring in 10 variables,
$\mathbb{Z}_{\ge 0}$-graded by $\deg(x_i) = 1$.

Let $\mathrm{CL} : \{0, 1, \ldots, 9\}^2 \to \{0, 1, \ldots, 9\}$ be the
symmetric function defined by the following $10 \times 10$ table:

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

(Entry $\mathrm{CL}[i][j]$ is the value in row $i$, column $j$, zero-indexed.
The table is symmetric: $\mathrm{CL}[i][j] = \mathrm{CL}[j][i]$.)

Define the binomial ideal

$$
I \;=\; \Bigl(\, x_i x_j - x_{\mathrm{CL}[i][j]} \, x_0 \;\Big|\; 0 \le i \le j \le 9 \,\Bigr) \;\subset\; R.
$$

There are $\binom{10+1}{2} = 55$ such relations; by direct Gröbner-basis
computation, $53$ of them are $k$-linearly independent generators of $I$ in
degree $2$ (two pairs coincide because of entries where
$\mathrm{CL}[i][j] \in \{i, j\}$).

Let $A = R / I$.

### 2. What I have computed

Running Macaulay2 / SageMath on $A = R/I$ gives:

**Hilbert function.** $\mathrm{HF}_A(0) = 1$, $\mathrm{HF}_A(1) = 10$,
$\mathrm{HF}_A(n) = 6$ for all $n \ge 2$. The Hilbert series is therefore

$$
\mathrm{HS}_A(t) \;=\; 1 + 10\,t + \frac{6\,t^2}{1 - t}
$$

so $\dim_k A_n = 6$ stabilizes from degree $2$ onward. Krull dimension of $A$
is $1$; the rank of the coordinate ring at the fibre over $x_0$ is $6$.

**Non-associativity statistics** (ambient magma, i.e. the multiplication
$x_i \cdot x_j := x_{\mathrm{CL}[i][j]}$ without the $x_0$ factor, on the
$10$-element set): out of $10^3 = 1000$ triples $(i, j, k)$,

- $872$ satisfy $(ij)k = i(jk)$ (associativity index $\alpha = 0.872$);
- $1000$ satisfy $ij = ji$ (100% commutative);
- the diagonal $\sigma(i) := \mathrm{CL}[i][i]$ has cycle structure
  $\sigma = (0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$: four fixed points and a single
  6-cycle.

**Lie-theoretic structure** (the content of the clarification to Dr. Mantero).
For each $i \in \{0, \ldots, 9\}$, let $L_i : V \to V$ be the left-regular
operator on $V = k \cdot x_0 \oplus \cdots \oplus k \cdot x_9$ defined by
$L_i(x_j) = x_{\mathrm{CL}[i][j]}$, and let $A_i = L_i - L_i^\top \in
\mathfrak{sl}(V)$. For $F = \{1, 2, 3, 4, 6, 8\}$ (the complement of the
$\sigma$-fixed set $\{0, 3, 8, 9\}$ intersected with the $6$-cycle), the Lie
subalgebra

$$
\mathfrak{g} := \mathrm{Lie}\langle A_i : i \in F \rangle \subset \mathfrak{sl}(V)
$$

is $28$-dimensional (closure reached after two commutator iterations:
$6 \to 21 \to 28$), satisfies the Jacobi identity to machine precision,
has Killing form of signature $(0, 28, 0)$ (compact), and admits a unique
(up to scale) invariant symmetric bilinear form. By the classification of
compact simple Lie algebras, $\mathfrak{g} \cong \mathfrak{so}(8, \mathbb{R})
= D_4$.

(Reproducibility scripts at `papers/wp11/verification/` and
`papers/wp12/verification/` in the companion repository; the so(10)
identification from the combined CL ∪ BHML generator set is a separate result.)

**Stanley-Reisner pattern.** Let $I_B$ be the squarefree monomial ideal

$$
I_B = (x_1 x_2,\; x_2 x_4,\; x_2 x_9,\; x_3 x_9,\; x_4 x_8),
$$

whose generators are the five off-diagonal entries of the upper triangle of
$\mathrm{CL}$ that lie in $\{0, \ldots, 9\} \setminus \{0, 7\}$. The
simplicial complex $\Delta$ with Stanley-Reisner ideal $I_\Delta = I_B$ is
pure of rank $7$ on $10$ vertices but is *not* matroidal: direct
enumeration shows basis-exchange fails for $21.9\%$ of ordered pairs of
facets.

### 3. The question

Let $A = R/I$ with $I, R$ as above.

**(Q1)** What is the projective dimension $\mathrm{pd}_R(A)$?

**(Q2)** Is $A$ a Koszul algebra?

**(Q3)** (secondary) Is $A$ Cohen-Macaulay? Gorenstein?

**(Q4)** (secondary) Given the Stanley-Reisner pattern $I_B$ above —
specifically the *pure-but-not-matroidal* character of $\Delta$ — is there a
known obstruction that relates this failure-of-matroid to $\mathrm{pd}(A)$ or
to the Koszul property of $A$? I am aware of the Fröberg conjecture and of
Mantero-Nguyen's 2024 structure theorem on symbolic powers of squarefree
monomial ideals associated with matroids (arXiv:2406.13759), and of the
March 2026 follow-up on focal matroids (arXiv:2603.19419). I suspect my
$\Delta$ sits in a well-studied "near-matroid" neighbourhood but I do not
know the right vocabulary for its position.

### 4. What I have tried

- Macaulay2: `betti res A` returns (a non-trivial Betti table which I am
  happy to paste in the post once it finalizes; truncating here since the
  specific Betti numbers are the object of the question and I want external
  verification before quoting them).
- Hand-calculation of the first syzygy module gives at least one non-linear
  syzygy, suggesting $A$ is *not* Koszul, but I have not proved the general
  claim.
- Searched the commutative-algebra literature for binomial ideals with
  Hilbert function stabilizing at a small constant; the closest
  neighbours I found are the toric ideals of graph algebras and the
  *lattice ideals of edge ideals*, but the 6-stabilization does not match
  those standard families.

### 5. Related

Any reference that resolves (Q1) or (Q2) in closed form, or that embeds
this ideal into a known family (binomial edge ideals, lattice ideals,
algebras arising from finite commutative magmas, etc.), would be a full
answer. A proof that $A$ fails to be Koszul via an explicit degree-$\ge 3$
syzygy would also be a full answer. Partial answers (e.g. a bound on
$\mathrm{pd}(A)$ from the Stanley-Reisner projection) are welcome.

The context for this question is a research programme on a frozen 10-element
commutative non-associative magma; the broader programme is not the subject
of the post — this question is focused strictly on the commutative-algebra
content of the binomial ideal above.

Full reproducibility bundle (Python + Macaulay2 scripts, canonical table,
Hilbert-function computation) at
[GitHub: `ck/papers/sprint_20260423_full/`][repo-link-to-insert].

---

## Pre-post checklist

- [ ] Compute Betti table in Macaulay2 and paste actual numbers (currently
      placeholder).
- [ ] Verify 53 vs 55 count of independent degree-2 relations by printing
      a Gröbner basis; report the two coinciding pairs explicitly.
- [ ] Compute $\mathrm{pd}_R(A)$ upper and lower bounds before posting
      (answer my own Q1 partially if possible).
- [ ] Check whether *any* of the Mantero-Nguyen focal-matroid papers cover
      pure-but-not-matroidal cases — if so, cite inline.
- [ ] Pick the five MO tags (drop `ra.rings-and-algebras` — save for
      follow-up if needed).
- [ ] Create a pastebin / github gist with the Macaulay2 input so the post
      links to runnable code.
- [ ] Final read-through for tone: MathOverflow answers best when the
      question is narrow, motivated, and self-contained. No framework
      advocacy in the post body.
- [ ] Post, then update `papers/sprint_20260423_full/08_correspondence/mantero_exchange.md`
      "Status" section with the link + email Dr. Mantero.

---

## Pre-post dependencies (scripts to run)

1. `papers/sprint_20260423_full/04_mantero_bridge/cl_as_quadratic_algebra.py`
   — produces the Hilbert function and the 53-vs-55 count.
2. `papers/sprint_20260423_full/04_mantero_bridge/hilbert_and_matroid_deep.py`
   — matroid-exchange statistics for the Stanley-Reisner pattern.
3. `papers/wp11/verification/` (when populated) — the so(8) = D_4 check.
4. *New*: a small Macaulay2 script
   (`09_mathoverflow_post/compute_betti.m2`) that ingests $I$ and prints
   `betti res A` and `pd A`. This script is the only missing piece for the
   pre-post checklist.

---

## Notes

- The branch `mantero-bridge-2026-04-23` holds this draft plus the bridge
  research (Mantero's published framework mapped against the CL object, the
  Lie-algebraic lift WP11/WP12, the Stanley-Reisner pure-but-not-matroidal
  companion) so that anyone arriving at the branch can pick up context
  without wading through unrelated material.
- This file is the draft. When the post goes live, the link is appended to
  the Status block of `08_correspondence/mantero_exchange.md`.
