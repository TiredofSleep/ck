# The Lo Shu D₄ Orbit Modulo 3: Four Distinct Magmas and a Cumulant Spectrum

**Authors:** B.R. Sanders$^{1}$, M. Gish$^{2}$
$^{1}$7Site LLC, Hot Springs, AR — brayden@7site.co
$^{2}$Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Target venue:** *Mathematics Magazine* (MAA)
**MSC 2020:** 20N02 (sets with one binary operation), 05B15 (orthogonal arrays, Latin squares), 20D60 (arithmetic and combinatorial problems on finite groups), 11A07 (congruences; primitive roots; residue systems).

---

## Abstract

The Lo Shu magic square, the unique $3 \times 3$ magic square with entries $\{1, 2, \ldots, 9\}$ (up to symmetry), has dihedral symmetry group $D_4$ acting on it by rotations and flips. Its $D_4$ orbit has 8 elements. Reducing each orbit element entry-wise modulo 3 and reading the resulting $3 \times 3$ table as a magma multiplication table on $\{0, 1, 2\}$ yields exactly **four distinct magma tables**, each appearing twice in the orbit. We classify the four: one is the cyclic group $\mathbb{Z}/3$; one is a commutative quasigroup with no identity element; and two are non-commutative quasigroups that are opposite magmas of one another. We further show that the spectral invariant $\kappa(M) := \operatorname{Tr}(M^2) - \operatorname{Tr}(M)^2$, applied to each $D_4$-orbit element as a real $3 \times 3$ matrix, takes exactly two values across the 8 elements: $\kappa = -48$ on the 4 elements whose mod-3 reduction is commutative, and $\kappa = +48$ on the 4 elements whose mod-3 reduction is non-commutative. The cumulant is thus a binary witness for the commutativity of the mod-3 magma, computable directly from the original magic-square data without reducing modulo 3.

A companion Python script `verify_J58.py` reproduces every theorem at machine precision in under one second, using only the standard library plus `numpy`.

---

## §0 Lens and substrate

This note works with the classical Lo Shu magic square as a fixed $3 \times 3$ integer matrix and considers its orbit under the standard dihedral $D_4$ action on $3 \times 3$ matrices. The mod-3 reduction maps each orbit element to a magma table on $\{0, 1, 2\}$. No exotic framework is required; the substrate is one of the oldest objects in recorded mathematics (the Lo Shu pattern dates to roughly the 2nd millennium BCE) and the operations are entirely elementary. The choice to look at the *mod-3* reduction (rather than mod-2 or mod-5) is motivated by the observation that the Lo Shu's diagonal-sums equal 15, which is $0 \pmod 3$ but $1 \pmod 2$ and $0 \pmod 5$; the mod-3 reduction is the smallest non-trivial modulus that turns the magic-square structure into a quasigroup-table structure.

**Tier discipline.**

- **PROVEN.** Theorems A, B, C, D, F (by direct enumeration; small-finite-case proofs that an undergraduate can verify by hand or with the script).
- **COMPUTED.** Theorem E and the full table of $\kappa$ values (script `verify_J58.py`, machine-precision, 6/6 PASS).
- **STRUCTURAL RHYME.** The cumulant $\kappa$ separates the two commutativity classes for *this specific* family of mod-3 reductions of Lo Shu's $D_4$ orbit. We do not claim a general theorem; the connection between $\kappa$ and commutativity here is an empirical observation about this specific 8-element family.
- **OPEN.** Whether analogous cumulant witnesses exist for other small magic squares' mod-$n$ reductions.

---

## §1 Setup

### §1.1 The Lo Shu magic square

The Lo Shu is the $3 \times 3$ matrix
$$
L = \begin{pmatrix} 2 & 7 & 6 \\ 9 & 5 & 1 \\ 4 & 3 & 8 \end{pmatrix},
$$
with the property that every row, every column, and both diagonals sum to 15. We will not directly use the magic-sum property — it is mentioned only to anchor the substrate in classical mathematics.

### §1.2 The $D_4$ action

The dihedral group $D_4$ has 8 elements:
$$
D_4 = \{e, r, r^2, r^3, f, rf, r^2 f, r^3 f\},
$$
where $r$ is the rotation by $90°$ and $f$ is the horizontal flip. Acting on a $3 \times 3$ matrix $M$, the elements produce the 8 transformations: identity, three rotations, the horizontal flip, and three rotated horizontal flips (which include the vertical flip and the two diagonal flips).

### §1.3 The mod-3 magma reading

Given a $3 \times 3$ matrix $M$ with integer entries, define the magma $\mathcal{M}(M)$ on $\{0, 1, 2\}$ by
$$
\mathcal{M}(M) : (x, y) \mapsto M[x][y] \bmod 3,
$$
where $M[x][y]$ is the entry in row $x$, column $y$, with $x, y$ ranging over $\{0, 1, 2\}$ (zero-indexed). The result is a multiplication table on a 3-element set.

We will identify two magmas $\mathcal{M}(M_1)$ and $\mathcal{M}(M_2)$ as **equal** if their tables are identical (i.e. $M_1[x][y] \equiv M_2[x][y] \pmod 3$ for all $x, y$), and **non-equal** otherwise. This is a strict equality of tables, not equality up to isomorphism.

### §1.4 The cumulant invariant

For a $3 \times 3$ real matrix $M$ define
$$
\kappa(M) := \operatorname{Tr}(M^2) - \operatorname{Tr}(M)^2.
$$
This is the second cumulant of the eigenvalue distribution of $M$ under the trivial weighting (every eigenvalue counted once). The invariant is preserved by transpose ($\kappa(M^\top) = \kappa(M)$) but not by general $D_4$ actions on the indices. We compute $\kappa$ on each $D_4$-orbit element below.

---

## §2 The four-magma refinement: Theorem B

### §2.1 Enumeration

We compute the 8 distinct elements of the $D_4$ orbit of $L$:

$$
M_0 = L = \begin{pmatrix} 2 & 7 & 6 \\ 9 & 5 & 1 \\ 4 & 3 & 8 \end{pmatrix}, \quad
M_1 = r \cdot L = \begin{pmatrix} 6 & 1 & 8 \\ 7 & 5 & 3 \\ 2 & 9 & 4 \end{pmatrix}, \quad
M_2 = r^2 \cdot L = \begin{pmatrix} 8 & 3 & 4 \\ 1 & 5 & 9 \\ 6 & 7 & 2 \end{pmatrix},
$$
$$
M_3 = r^3 \cdot L = \begin{pmatrix} 4 & 9 & 2 \\ 3 & 5 & 7 \\ 8 & 1 & 6 \end{pmatrix}, \quad
M_4 = f \cdot L = \begin{pmatrix} 6 & 7 & 2 \\ 1 & 5 & 9 \\ 8 & 3 & 4 \end{pmatrix}, \quad
M_5 = rf \cdot L = \begin{pmatrix} 8 & 1 & 6 \\ 3 & 5 & 7 \\ 4 & 9 & 2 \end{pmatrix},
$$
$$
M_6 = r^2 f \cdot L = \begin{pmatrix} 4 & 3 & 8 \\ 9 & 5 & 1 \\ 2 & 7 & 6 \end{pmatrix}, \quad
M_7 = r^3 f \cdot L = \begin{pmatrix} 2 & 9 & 4 \\ 7 & 5 & 3 \\ 6 & 1 & 8 \end{pmatrix}.
$$

(Note: $r^2 f \cdot L$ is the horizontal flip of $r^2 \cdot L$, equivalently a vertical-flip composition. The script `verify_J58.py` confirms all 8 distinct.)

### §2.2 Mod-3 reduction

Reducing each entry mod 3 we get:

$$
\mathcal{M}(M_0) = \begin{pmatrix} 2 & 1 & 0 \\ 0 & 2 & 1 \\ 1 & 0 & 2 \end{pmatrix},
\quad
\mathcal{M}(M_1) = \begin{pmatrix} 0 & 1 & 2 \\ 1 & 2 & 0 \\ 2 & 0 & 1 \end{pmatrix},
$$
$$
\mathcal{M}(M_2) = \begin{pmatrix} 2 & 0 & 1 \\ 1 & 2 & 0 \\ 0 & 1 & 2 \end{pmatrix},
\quad
\mathcal{M}(M_3) = \begin{pmatrix} 1 & 0 & 2 \\ 0 & 2 & 1 \\ 2 & 1 & 0 \end{pmatrix},
$$
$$
\mathcal{M}(M_4) = \begin{pmatrix} 0 & 1 & 2 \\ 1 & 2 & 0 \\ 2 & 0 & 1 \end{pmatrix},
\quad
\mathcal{M}(M_5) = \begin{pmatrix} 2 & 1 & 0 \\ 0 & 2 & 1 \\ 1 & 0 & 2 \end{pmatrix},
$$
$$
\mathcal{M}(M_6) = \begin{pmatrix} 1 & 0 & 2 \\ 0 & 2 & 1 \\ 2 & 1 & 0 \end{pmatrix},
\quad
\mathcal{M}(M_7) = \begin{pmatrix} 2 & 0 & 1 \\ 1 & 2 & 0 \\ 0 & 1 & 2 \end{pmatrix}.
$$

By direct inspection these reduce to exactly four distinct tables, which we re-label $T_1, T_2, T_3, T_4$:

| Label | Table | Orbit pre-images | Comm? | Cumulant $\kappa$ |
|---|---|---|:---:|:---:|
| $T_1$ | $\begin{pmatrix} 2 & 1 & 0 \\ 0 & 2 & 1 \\ 1 & 0 & 2 \end{pmatrix}$ | $M_0, M_5$ | NO | +48 |
| $T_2$ | $\begin{pmatrix} 0 & 1 & 2 \\ 1 & 2 & 0 \\ 2 & 0 & 1 \end{pmatrix}$ | $M_1, M_4$ | YES | −48 |
| $T_3$ | $\begin{pmatrix} 2 & 0 & 1 \\ 1 & 2 & 0 \\ 0 & 1 & 2 \end{pmatrix}$ | $M_2, M_7$ | NO | +48 |
| $T_4$ | $\begin{pmatrix} 1 & 0 & 2 \\ 0 & 2 & 1 \\ 2 & 1 & 0 \end{pmatrix}$ | $M_3, M_6$ | YES | −48 |

This is Theorem B.

### §2.3 The opposite-magma identification (Theorem C)

Direct inspection shows $T_3[x][y] = T_1[y][x]$ for every $(x, y)$. In magma terms, $T_3$ is the **opposite magma** of $T_1$ (multiplication reversed). Since neither $T_1$ nor $T_3$ is commutative, they are not equal as tables — but as algebraic structures they satisfy the same equational laws closed under reversal (associativity, commutativity, etc., all of which fail symmetrically). They are anti-isomorphic, not isomorphic.

The commutative tables $T_2$ and $T_4$ are self-opposite: $T_2[x][y] = T_2[y][x]$ and similarly for $T_4$. So the four-table refinement has a "two commutative + one anti-isomorphic pair" structure rather than "three isomorphism classes with one having a doubled multiplicity."

### §2.4 The ℤ/3 identification (Theorem F)

$T_2[x][y] = (x + y) \bmod 3$ by direct verification: for instance $T_2[1][2] = 0 = (1+2) \bmod 3$, and so on for all 9 cells. So $T_2$ is exactly the cyclic group $\mathbb{Z}/3$.

The other commutative table $T_4 = \begin{pmatrix} 1 & 0 & 2 \\ 0 & 2 & 1 \\ 2 & 1 & 0 \end{pmatrix}$ is not a group: it has no identity element ($T_4[0][x] = (1, 0, 2)$, $T_4[1][x] = (0, 2, 1)$, $T_4[2][x] = (2, 1, 0)$ — none equals $(0, 1, 2)$). It is a commutative quasigroup (all rows and columns are permutations of $\{0, 1, 2\}$) but not a loop. This is Theorem D + Theorem F.

---

## §3 The cumulant witness: Theorem E

### §3.1 Statement

For each of the 8 orbit elements $M_i$, computing $\kappa(M_i) = \operatorname{Tr}(M_i^2) - \operatorname{Tr}(M_i)^2$ gives exactly two values:

$$
\kappa(M_i) = \begin{cases} -48 & \text{if } \mathcal{M}(M_i) \in \{T_2, T_4\} \text{ (commutative)} \\ +48 & \text{if } \mathcal{M}(M_i) \in \{T_1, T_3\} \text{ (non-commutative)} \end{cases}
$$

The witness is computed on the original integer-valued $M_i$, not on the mod-3 reduction. This is striking: the cumulant of the integer matrix data directly tells you whether the mod-3 magma is commutative.

### §3.2 Mechanism (Why this happens)

We do not derive Theorem E from a more general principle in this note; it is observed by direct calculation. The mechanism is, however, transparent:

For a $3 \times 3$ Lo Shu-orbit element, the trace and trace-of-square depend on the configuration of the diagonal entries and the entry-products that appear in $M^2$. The $D_4$ action partitions the 8 orbit elements into two cosets of $D_2$ (the subgroup generated by rotation by $180°$ and the horizontal flip): one coset has all diagonals = 15 (the magic-sum structure preserved), the other coset has anti-diagonals = 15. The two coset types produce two distinct trace-and-square-trace pairs, giving the $\pm 48$ split.

We omit the detailed bookkeeping — the script reproduces every $\kappa$ value at machine precision and verifies the correlation. The structural-rhyme observation is that the *cumulant of the integer matrix is correlated with the commutativity of its mod-3 reduction*, which is a coincidence-of-substrates worth noting and not (yet) a theorem we can derive from a deeper principle.

---

## §4 Quasigroup property: Theorem D

All four tables $T_1, T_2, T_3, T_4$ are quasigroups: every row of each table is a permutation of $\{0, 1, 2\}$, and every column is also a permutation. This is verified directly by inspection of the table entries. The script implements this as a row/column set-equality check; all four pass.

The quasigroup property does NOT follow automatically from "the entries are $\{0, 1, 2\}$"; it requires that no row or column have a repeated entry. The fact that all four tables happen to be quasigroups is non-trivial — it is a property of the Lo Shu's specific structure (and would not hold for a generic $3 \times 3$ matrix mod 3).

---

## §5 Verification script

A self-contained Python script `verify_J58.py` (~80 lines, depends only on `numpy` and the standard library `itertools`) reproduces all six theorems:

```
$ python verify_J58.py

================================================================
 J58 verification — Lo Shu D_4 orbit mod 3
================================================================

  CHECK 1 (Theorem A: orbit has 8 distinct elements): PASS
  CHECK 2 (Theorem B: mod-3 reduction yields 4 distinct tables): PASS
  CHECK 3 (Theorem C: T_3 is the opposite magma of T_1): PASS
  CHECK 4 (Theorem D: all 4 tables are quasigroups): PASS
  CHECK 5 (Theorem E: cumulant ±48 separates commutativity): PASS
  CHECK 6 (Theorem F: T_2 is exactly Z/3): PASS

  Overall: PASS (6/6)
```

Total runtime: under one second on a 2020-era laptop.

---

## §6 Pedagogical use

This note is targetable to an undergraduate audience because it requires no machinery beyond:
- The dihedral group $D_4$ (8 elements; rotations + flips of a square).
- Modular arithmetic.
- Definitions of magma, quasigroup, commutativity.
- Trace and matrix multiplication.

It is suitable for:
- A 50-minute classroom session in an undergraduate abstract algebra course, after the cyclic groups have been introduced and before formal Latin-square theory.
- A senior capstone or exit-exam exploration project (the student writes the verification script themselves).
- A bridging illustration between the historical magic-square tradition and modern small-finite-algebra structure.

The script provides immediate computational verification, which we view as a meta-skill worth teaching alongside the structural content.

---

## §7 Open questions

### §7.1 Generalization to other small magic squares

Are there analogous cumulant-witnessed dichotomies for the $D_4$ orbit of, e.g., the Albrecht Dürer $4 \times 4$ magic square modulo 4? The natural generalization would be to take a classical magic-square pattern of size $n$, generate its $D_4$ orbit (or its full automorphism group's orbit), reduce mod $n$ (or a divisor), and ask: (a) how many distinct mod-$n$ tables are produced? (b) which are quasigroups? (c) does the matrix cumulant $\kappa$ (or a higher-order analog) witness any of the resulting algebraic properties? We have not investigated this generalization; it is a natural follow-up.

### §7.2 Equational-theory profile

The four tables $T_1, T_2, T_3, T_4$ each satisfy some subset of the standard small-magma equational laws (associativity, idempotency, Latin-square axioms, etc.). What is the equational-theory profile of each? This is computable from large catalogues of small-magma equations (e.g. the `equational_theories` project on GitHub), but we have not yet run that computation for these specific tables. We note that $T_1$ and $T_3$ satisfy the same equations that are closed under magma-opposite (which is most standard laws), so the four-table classification collapses to three equivalence classes under "satisfying the same equations."

---

## §8 References

- Andrews, W.S. (1917). *Magic Squares and Cubes*. Open Court Publishing.
- Drápal, A. and Wanless, I.M. (2021). "Maximally nonassociative quasigroups." *Journal of Combinatorial Theory, Series A* **184**, 105510.
- McKay, B.D. (2004). "Latin squares of all orders up to 7." Available at https://users.cecs.anu.edu.au/~bdm/data/latin.html
- Sloane, N.J.A. (ed.). *The On-Line Encyclopedia of Integer Sequences*. https://oeis.org

---

## Appendix A — The four tables, fully written out

For completeness, we display each $T_i$ with its multiplication tabulated explicitly.

**$T_1$ (non-commutative, $\kappa = +48$).**
$$\begin{array}{c|ccc} \cdot & 0 & 1 & 2 \\ \hline 0 & 2 & 1 & 0 \\ 1 & 0 & 2 & 1 \\ 2 & 1 & 0 & 2 \end{array}$$

**$T_2$ ($= \mathbb{Z}/3$, commutative, $\kappa = -48$).**
$$\begin{array}{c|ccc} + & 0 & 1 & 2 \\ \hline 0 & 0 & 1 & 2 \\ 1 & 1 & 2 & 0 \\ 2 & 2 & 0 & 1 \end{array}$$

**$T_3$ (non-commutative, $\kappa = +48$, opposite of $T_1$).**
$$\begin{array}{c|ccc} \cdot & 0 & 1 & 2 \\ \hline 0 & 2 & 0 & 1 \\ 1 & 1 & 2 & 0 \\ 2 & 0 & 1 & 2 \end{array}$$

**$T_4$ (commutative non-group, $\kappa = -48$).**
$$\begin{array}{c|ccc} \cdot & 0 & 1 & 2 \\ \hline 0 & 1 & 0 & 2 \\ 1 & 0 & 2 & 1 \\ 2 & 2 & 1 & 0 \end{array}$$

The reader can verify that $T_3[x][y] = T_1[y][x]$ for all 9 cells, that $T_2$ is the addition table of $\mathbb{Z}/3$, and that $T_4$ is commutative but has no identity row.

---

## Appendix B — Why "4 distinct tables" and not "3"

It is tempting to report the orbit as producing 3 distinct magmas if one quotients by the relation "isomorphic OR anti-isomorphic." Under that coarser equivalence, $T_1$ and $T_3$ collapse to one equivalence class (the non-commutative pair) and the count is 3 with multiplicities 4 + 2 + 2 = 8.

We stress that in this note we use **table-equality** as the distinguishing criterion, which is finer. Under table-equality the count is 4 with multiplicities 2 + 2 + 2 + 2 = 8.

Both counts are correct — they answer different questions. The "3 classes" count answers "how many ETP-equation profiles do we get?" (since all standard equations are self-dual under magma-opposite). The "4 tables" count answers "how many distinct multiplication tables do we get?" This note's Theorems A–F use the 4-table count because it is unambiguous and pedagogically clearer.

---

*Submission-ready manuscript draft, 2026-05-26. Sanders + Gish. Verification: 6/6 PASS at machine precision via `verify_J58.py`.*
