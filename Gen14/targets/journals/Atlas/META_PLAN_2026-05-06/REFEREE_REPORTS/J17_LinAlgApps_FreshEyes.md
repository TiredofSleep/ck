# Referee Report: J17 / Linear Algebra and Its Applications

**Manuscript:** "A Dimensional Ladder Connecting Tensor Powers of a Finite-Field 4-Algebra to Real Clifford Algebras $\mathrm{Cl}(2n)$"
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** Linear Algebra and its Applications
**Reviewer:** Anonymous external referee (fresh-eyes; no prior contact with the framework)
**Date:** 2026-05-07

---

## 1. Summary of the manuscript

The authors observe that the dimension of the $n$-th tensor power of a 4-dimensional $\mathbb{F}_5$-algebra $V$ matches the dimension of the real Clifford algebra $\mathrm{Cl}(2n)$:
$$\dim_{\mathbb{F}_5} V^{\otimes n} \;=\; 4^n \;=\; 2^{2n} \;=\; \dim_\mathbb{R} \mathrm{Cl}(2n) \qquad \text{for } n = 0, 1, 2, 3, 4, 5.$$

This is presented as Theorem 3.1 ("dimensional ladder"). The paper additionally claims a "binomial $\leftrightarrow$ grade correspondence" (Theorem 3.2) asserting that the $2^n$ "fine cells" of $V^{\otimes n}$ partition into groups of size $\binom{n}{k}$ for $k = 0, 1, \ldots, n$, "matching the grade-$k$ subspace dimensions of $\mathrm{Cl}(2n)$." Theorem 4.1 asserts a special case at $n = 5$: the 32 fine cells of $V^{\otimes 5}$ partition as $1+5+10+10+5+1$, matching the representation content of $\mathbf{1} \oplus \bar{\mathbf{5}} \oplus \mathbf{10}$ plus its conjugate (the SU(5) one-generation rep).

The "fine cells" of $V^{\otimes n}$ are defined (in §2) via the direct-sum decomposition $V = (\mathbb{F}_5 e_2 \oplus \mathbb{F}_5 e_3) \oplus (\mathbb{F}_5 e_0 \oplus \mathbb{F}_5 e_4)$ as $\mathbb{F}_5$-vector space, where each tensor factor "carries a sign $\pm$" indicating which summand it contributes to. Across $n$ factors this gives a $2^n$-element set indexed by sign-tuples in $\{+, -\}^n$. The "weight" of a fine cell is the count of $+$'s in its sign-tuple.

I have read the manuscript end-to-end and run the supplied verification script (`tig_dirac.py`, `tensor_partition()`, `cell_binomial_distribution()`).

---

## 2. Decision recommendation

**Reject in current form** (with explicit invitation to resubmit a substantially restructured paper). The mathematical content of the manuscript is too thin for *Linear Algebra and Its Applications*:

- **Problem A (fatal):** Theorem 3.1 ("dimensional ladder") is a one-line consequence of $\dim V = 4 = 2^2$ and the standard formula $\dim_\mathbb{R} \mathrm{Cl}(2n) = 2^{2n}$. The proof in the manuscript is two sentences long. There is no theorem here — it is an arithmetic identity.

- **Problem B (fatal):** Theorem 3.2 ("binomial $\leftrightarrow$ grade correspondence") *misstates* what is actually true. The $2^n$ fine cells of $V^{\otimes n}$ have weight distribution $\binom{n}{k}$ for $k = 0, \ldots, n$. But the grade decomposition of $\mathrm{Cl}(2n)$ gives subspaces of dimensions $\binom{2n}{k}$ for $k = 0, \ldots, 2n$. **These are different sequences.** For example, at $n = 3$ the cell weights are $\{1, 3, 3, 1\}$ (from $\binom{3}{k}$) but the Clifford-grade dimensions are $\{1, 6, 15, 20, 15, 6, 1\}$ (from $\binom{6}{k}$). The remark below Theorem 3.2 acknowledges this mismatch but the theorem statement itself is wrong.

- **Problem C (fatal):** Theorem 4.1 ("$\mathrm{SU}(5)$ representation match at $n=5$") is a binomial-coefficient identity: $\binom{5}{0} + \binom{5}{1} + \binom{5}{2} = 16$ and $\binom{5}{k} = \binom{5}{5-k}$. This is a property of *any* tensor structure with a binary partition at each tensor factor and 5 factors. It says nothing about $V$, $\mathrm{Cl}(10)$, or SU(5).

- **Problem D:** The proof of Theorem 3.1 is the chain of three equalities $4^n = 2^{2n} = \dim_\mathbb{R} \mathrm{Cl}(2n)$. The first follows from $\dim V = 4$, the second is rewriting, the third is the standard Clifford-algebra dimension formula. None of this requires $V$. It would hold for any 4-dimensional algebra.

The manuscript reads as a (well-typed, clean) exposition of an arithmetic coincidence — $4^n = \dim \mathrm{Cl}(2n)$ — packaged as a "dimensional ladder." For *Linear Algebra and Its Applications*, this is below the bar. The paper does not establish a non-trivial linear-algebraic fact about $V$, $\mathrm{Cl}(2n)$, or their relationship.

A substantial rewrite *might* yield publishable content, but the current draft is best withdrawn and reconceived. See §7 for what a publishable version would have to contain.

---

## 3. Major comments

### M1. Theorem 3.1 has trivial proof; either drop it or replace with substance. (**fatal**)

The proof of Theorem 3.1 reads:

> $\dim_{\mathbb{F}_5} V^{\otimes n} = (\dim_{\mathbb{F}_5} V)^n = 4^n$ by tensor-product dimension. $4^n = (2^2)^n = 2^{2n}$. $\dim_\mathbb{R} \mathrm{Cl}(2n) = 2^{2n}$ by the classical formula for the dimension of a Clifford algebra over a quadratic form on $2n$ generators.

This is correct. It is also entirely formal. The conclusion follows from $\dim V = 4$ and the dimension formula for Clifford algebras. The same chain of equalities holds for any 4-dimensional algebra over any field. There is no use of the multiplication structure of $V$, no use of $\mathrm{Cl}(2n)$ as anything other than a vector space of given dimension.

For *Linear Algebra and Its Applications*, an equality of dimensions is not, by itself, a result. The expected output of a paper in this venue is a structural statement: an isomorphism of algebras, a representation of $V^{\otimes n}$ on something Clifford-related, an embedding/quotient connecting them, a map from $\mathrm{Cl}(2n)$-modules to $V^{\otimes n}$-modules, etc.

**Recommended fix.** Either (a) construct an actual linear-algebraic relationship between $V^{\otimes n}$ and $\mathrm{Cl}(2n)$ (as $\mathbb{F}_5$-vector spaces, or over a common field; provide a map and prove its properties), or (b) drop the "ladder" framing and present the dimension-match as a remark in a paper about the algebra $V$ itself.

The companion paper J16/J23 *is* a paper about the algebra $V$. The present paper does not stand alone if it is reduced to its own theorems.

### M2. Theorem 3.2 misstates the correspondence. (**fatal**)

The statement of Theorem 3.2 is:

> For $n = 0, 1, \ldots, 5$, the $2^n$ fine cells of $V^{\otimes n}$ partition into groups of size $\binom{n}{k}$ for $k = 0, 1, \ldots, n$, matching the grade-$k$ subspace dimensions of $\mathrm{Cl}(2n)$:
> $$\dim \mathrm{Cl}^{(k)}(2n) = \binom{2n}{k}, \quad k = 0, 1, \ldots, 2n.$$

This is **not a correspondence**. The cell-weight distribution of $V^{\otimes n}$ is $\binom{n}{k}$, indexed $k = 0, \ldots, n$. The grade dimension of $\mathrm{Cl}(2n)$ is $\binom{2n}{k}$, indexed $k = 0, \ldots, 2n$. These are different sequences:

| $n$ | Cell weights (binomial $\binom{n}{k}$) | $\mathrm{Cl}(2n)$ grades $\binom{2n}{k}$ |
|---|---|---|
| 0 | 1 | 1 |
| 1 | 1, 1 | 1, 2, 1 |
| 2 | 1, 2, 1 | 1, 4, 6, 4, 1 |
| 3 | 1, 3, 3, 1 | 1, 6, 15, 20, 15, 6, 1 |
| 4 | 1, 4, 6, 4, 1 | 1, 8, 28, 56, 70, 56, 28, 8, 1 |
| 5 | 1, 5, 10, 10, 5, 1 | 1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1 |

The cell weights have $n+1$ groups; the grade dimensions have $2n+1$ groups. The two sequences sum to the same total ($2^n$ fine cells with weights summing to $2^n$ — wait, this is wrong; cells sum to $\sum_k \binom{n}{k} = 2^n$ which is *not* $4^n = \dim V^{\otimes n}$, but rather the number of cells. Each cell is itself $\dim V$-dimensional. Total $V^{\otimes n}$-dimension is $\dim V \cdot 2^n / 1 \neq 4^n$ — actually it's the number of cells $\times$ (dim of each cell). Let me re-read…)

Re-reading §2, the "fine cells" are subsets of *signs* (equivalently: subsets of basis vectors at each tensor slot picking one summand). So a fine cell is *not* a subspace of $V^{\otimes n}$; it's a label. The cell labeled by a $\pm$-string of length $n$ has $|+|$ entries from $\{e_2, e_3\}$ and $n - |+|$ from $\{e_0, e_4\}$, hence is a subspace of dimension $2^n$ (each tensor slot is 2-dim). Total $V^{\otimes n}$ dimension = $2^n \cdot 2^n = 4^n$. ✓

So the cells partition $V^{\otimes n}$ into $2^n$ subspaces each of dimension $2^n$. Each cell has weight $k$ in $\{0, \ldots, n\}$. Cells of weight $k$: there are $\binom{n}{k}$ of them. Their total dimension (per weight class): $2^n \cdot \binom{n}{k}$.

If we want to "match" $\mathrm{Cl}(2n)$ grades, we'd need:
$$\text{(cells of weight } k) \times 2^n \;=\; \binom{n}{k} \cdot 2^n \;\stackrel{?}{=}\; \binom{2n}{k} \quad \text{(grade-}k\text{ dim of Cl}(2n)\text{)}.$$

This identity *does not hold*. For $n = 2, k = 1$: $\binom{2}{1} \cdot 2^2 = 8$, but $\binom{4}{1} = 4$. So even with a multiplicity correction, the cell weights and Clifford grades do not correspond.

The remark below Theorem 3.2 says:

> Note that $\binom{n}{k}$ (cells of $V^{\otimes n}$ at sign-weight $k$) differs from $\binom{2n}{k}$ (grade-$k$ subspace of $\mathrm{Cl}(2n)$). The relationship: each tensor factor of $V$ contributes 2 bits of "structural sign" (idempotent class membership), giving $2n$ bits across $n$ factors, so the sign-weight of a fine cell in $V^{\otimes n}$ corresponds to a multi-grade subspace in $\mathrm{Cl}(2n)$ via the canonical embedding.

This remark is hand-wavy. "Each tensor factor of $V$ contributes 2 bits of structural sign" is not justified — the cells are partitioned by *one* sign per slot, not two. "Multi-grade subspace" via "the canonical embedding" — what canonical embedding? None is constructed in the paper. The remark essentially admits that the theorem statement is wrong and gestures at a fix without providing one.

**Recommended fix (mandatory before resubmission).** Either:

(a) Construct an explicit $\mathbb{F}_5$-linear isomorphism (or some other structure-preserving map) $V^{\otimes n} \to \mathrm{Cl}(2n)$ that respects the cell decomposition on the left and *some* decomposition on the right, and prove that this map carries the cell-weight grading to the Clifford-grade grading (after suitable identification). The "2 bits per slot" hint suggests indexing fine cells by pairs $(\epsilon_i, \delta_i) \in \{\pm\}^2$ for each $i = 1, \ldots, n$, giving a $2n$-bit index that *does* match $\binom{2n}{k}$ — but this would be a *different* cell decomposition than the one used in the rest of the paper, and the authors would need to develop the bookkeeping.

(b) Withdraw Theorem 3.2 and replace it with the honest statement: "The cell-weight distribution of $V^{\otimes n}$ is the binomial sequence $\binom{n}{k}$. This is not the grade-decomposition of $\mathrm{Cl}(2n)$, which is $\binom{2n}{k}$. Both have total $2^{2n}$ as expected from dimension." And then the paper has nothing further to say, which is the correct conclusion.

The current Theorem 3.2 is non-rigorous. The paper cannot be published with it as stated.

### M3. Theorem 4.1 ($\mathrm{SU}(5)$ at $n=5$) is binomial coincidence, not a theorem. (**fatal**)

The "match" $1 + 5 + 10 + 10 + 5 + 1 = 32$ to the SU(5) one-generation rep $\mathbf{1} \oplus \bar{\mathbf{5}} \oplus \mathbf{10}$ plus conjugate is a binomial-coefficient identity: $\binom{5}{0} = 1, \binom{5}{1} = 5, \binom{5}{2} = 10$, and the symmetry $\binom{5}{k} = \binom{5}{5-k}$ gives the conjugate.

**This identity holds for any tensor structure with a binary partition at each of 5 tensor factors.** The 5-factor analogue would be true for $W^{\otimes 5}$ where $W$ is any $\mathbb{F}_p$-vector space with a 2-summand decomposition. The match has nothing to do with $V$'s multiplicative structure or with $\mathbb{F}_5$.

The remark following Theorem 4.1 disclaims:

> This match is dimensional. We do not assert that $V^{\otimes 5}$ carries the SU(5) action canonically; that question is left for future work.

Good. So the theorem as stated is: "$1 + 5 + 10 + 10 + 5 + 1$ equals 32, which equals the dimensions of the SU(5) reps $\mathbf{1}, \bar{\mathbf{5}}, \mathbf{10}$ plus conjugates." This is true. It is also a binomial identity that does not depend on $V$ or any of its structure.

**Recommended fix.** Demote Theorem 4.1 to a Remark. Or remove entirely. As currently stated, the theorem reports an arithmetic identity ($1+5+10+10+5+1 = 32$ and $\binom{5}{k} = \dim$ SU(5)-rep) that any reader can verify in 30 seconds.

### M4. The "fine cells" are a labeling, not a decomposition of $V^{\otimes n}$. (**important**)

§2 defines fine cells as $\pm$-tuples indicating which summand of $V = (\mathbb{F}_5 e_2 \oplus \mathbb{F}_5 e_3) \oplus (\mathbb{F}_5 e_0 \oplus \mathbb{F}_5 e_4)$ each tensor slot belongs to. This gives $2^n$ cells. Under this convention, each cell is a subspace of $V^{\otimes n}$ of dimension $2^n$ (since each tensor factor contributes a 2-dim summand chosen).

Total dimension: $2^n \cdot 2^n = 4^n$. ✓

But the §2 description is bare. There is no proof that the cell-decomposition is well-defined (i.e., that the fine cells form a direct-sum decomposition of $V^{\otimes n}$). For instance:
- The cells are pairwise orthogonal in some sense? (They are disjoint as subspaces but their orthogonality requires a bilinear form.)
- The decomposition is canonical, or basis-dependent? (Basis-dependent on the chosen direct-sum decomposition of $V$ — but the choice $(\mathbb{F}_5 e_2 \oplus \mathbb{F}_5 e_3) \oplus (\mathbb{F}_5 e_0 \oplus \mathbb{F}_5 e_4)$ is not motivated. Why not $(\mathbb{F}_5 e_0 \oplus \mathbb{F}_5 e_2) \oplus (\mathbb{F}_5 e_3 \oplus \mathbb{F}_5 e_4)$?)

The reference Python code (`tensor_partition()` in `tig_dirac.py`) labels cells by sign-strings without ever computing an actual $V^{\otimes n}$ tensor; it just enumerates $\{+, -\}^n$. So in the code, the "fine cells" are also a labeling, not a structure on $V^{\otimes n}$.

**Recommended fix.** State the cell decomposition as a definition with an explicit $\mathbb{F}_5$-vector-space direct-sum equation. Justify the choice of direct-sum decomposition of $V$. If the cell-orthogonality referenced in the code (`p_+ \cdot p_- = 0`) is the algebraic content, develop it.

### M5. The verification script "test\_tig\_dirac.py" tests T13, T14, T15 are not the substance of the paper.

The "Verification" section says:

> \texttt{test\_tig\_dirac.py} test T15: dimensional ladder for $n = 0, 1, 2, 3, 4, 5$.
> Test T13: $V^{\otimes n}$ has $2^n$ fine cells for $n = 1, \ldots, 5$.
> Test T14: $V^{\otimes 5}$ binomial $1+5+10+10+5+1 = 32$.

I ran `tig_dirac.py` and confirmed that `tensor_partition()` and `cell_binomial_distribution()` produce these counts. But this is verification of arithmetic — that $4^n = 4^n$ and $\binom{5}{k}$ sums to $32$ — not of any non-trivial property.

For a paper at *Linear Algebra and Its Applications*, computational verification has its place (e.g., for the structural claims in companion paper J16/J23, where it's load-bearing). Here, the verification is verifying $\binom{n}{k}$ sums correctly, which is an elementary identity. The script's role is bookkeeping, not theorem-checking.

**Recommended fix.** Remove the "Verification" section. The arithmetic identities verified are not in dispute and don't need a script.

### M6. The introduction is misleading. 

§1 says:

> This paper studies a 4-dimensional commutative non-associative algebra $V$ over $\mathbb{F}_5$ whose tensor powers exhibit dimensions matching $\mathrm{Cl}(2n)$ exactly for $n = 0..5$.

The matches are dimensional only. Re-state honestly: "This paper observes that $\dim V^{\otimes n} = \dim \mathrm{Cl}(2n)$ as a consequence of $\dim V = 4 = 2^2$. We further note that the $\binom{n}{k}$-cell weight distribution of $V^{\otimes n}$ matches the dimensions of the SU(5) one-generation rep at $n = 5$."

The paper would then be 2 pages, which is appropriate for the depth of the result.

### M7. Reference issues.

- **Hestenes-Sobczyk 1984**: cited but the geometric-algebra content from Hestenes-Sobczyk is not engaged with in the paper. If this is just background for "Clifford algebras exist", a textbook-level citation suffices.
- **Bott 1959**: cited; Bott periodicity is mentioned in the conjectural-extension remark but the paper does not develop the connection. Either develop or remove.
- **GeorgiGlashow 1974**: cited for SU(5) GUT. The paper claims a "match" to SU(5) reps at $n=5$ but does not engage with Georgi-Glashow's actual content. Drop or use.

---

## 4. Minor comments

### m1. Notation.

- "$\mathrm{Cl}(2n)$" without specifying signature is ambiguous in the literature. The paper means $\mathrm{Cl}(2n, 0)$ (positive-definite, i.e., $2n$ generators each squaring to $+1$). State this in §1.
- "Fine cells" — terminology is used without definition until §2.

### m2. Bibliography.

- $V$'s definition and structural features are deferred to companion paper J16/J23 ([SandersGishDiscreteDirac]). A reader of *Linear Algebra and Its Applications* without access to that paper has only the very brief §2 to work from. If this paper is to stand alone, §2 should include the multiplication table.

### m3. Length.

The paper is short (under 10 pages). For *Linear Algebra and Its Applications*, this is fine *if* the result is novel and substantial. As argued in M1–M3, the result is neither novel (it is an arithmetic identity) nor substantial (the "correspondences" are mis-stated or trivial).

### m4. The Bott periodicity remark.

The "Conjectural extension" remark says:

> We expect the dimensional ladder to hold for all $n \geq 0$ by induction on the periodicity $\mathrm{Cl}(n+8) \cong \mathrm{Cl}(n) \otimes \mathrm{Cl}(8)$.

This is correct: $\dim \mathrm{Cl}(2n+16) = 2^{2n+16}$ and $\dim V^{\otimes(n+8)} = 4^{n+8} = 2^{2n+16}$. Both expand as $\dim$-ladder by $4^n \to 4^{n+1}$. So the conjecture is *trivially true* for all $n$ — it is the equality $4^{n+1} = 2^{2(n+1)}$, which is rewriting.

If this is the conjecture, it is not a conjecture; it is a trivial extension of Theorem 3.1. State it as such or remove.

---

## 5. Independent verification summary

I executed `tig_dirac.py` and the helpers `tensor_partition(n)` and `cell_binomial_distribution(n)` for $n = 0, \ldots, 5$. The cell counts and weight distributions confirmed:

| $n$ | $|$cells$|$ | dim $V^{\otimes n}$ | dim Cl($2n$) | weight distribution |
|---|---|---|---|---|
| 0 | 1 | 1 | 1 | {0: 1} |
| 1 | 2 | 4 | 4 | {0: 1, 1: 1} |
| 2 | 4 | 16 | 16 | {0: 1, 1: 2, 2: 1} |
| 3 | 8 | 64 | 64 | {0: 1, 1: 3, 2: 3, 3: 1} |
| 4 | 16 | 256 | 256 | {0: 1, 1: 4, 2: 6, 3: 4, 4: 1} |
| 5 | 32 | 1024 | 1024 | {0: 1, 1: 5, 2: 10, 3: 10, 4: 5, 5: 1} |

All arithmetic checks pass. (They are arithmetic.)

---

## 6. Strengths of the manuscript

1. **Reproducibility of the verification.** The script runs in $<1$ second and produces the claimed cell counts.
2. **The honest disclaimer following Theorem 4.1.** The authors are explicit that the SU(5) match is dimensional only.

---

## 7. What a publishable version would have to contain

The current paper does not contain a non-trivial linear-algebraic result. A publishable version at *Linear Algebra and Its Applications* (or a comparable venue) would need at least one of:

(a) **An explicit $\mathbb{F}_5$-linear isomorphism (or a structure-preserving map) $V^{\otimes n} \to A_n$** for some Clifford-related $A_n$, with a proof that the map carries the cell-decomposition to a structurally meaningful decomposition. The paper currently does not construct any map.

(b) **A representation-theoretic theorem** about $V^{\otimes n}$: a finite-group action with character formula, an SU(5) or Spin(10) action constructed (the open question 4.X stated in the companion's open-questions section), a Frobenius algebra structure, or a connection to $\mathbb{F}_5$-spinor representations.

(c) **A non-trivial algebraic property** of the cells: e.g., the cells form a modular sublattice in the lattice of subspaces of $V^{\otimes n}$ with a description of the partial order; the cells are minimal idempotent images of a finite-group action; etc.

Any of (a)-(c) would carry the paper. The current draft has none.

---

## 8. Decision

**Reject in current form**, with explicit invitation to resubmit.

The paper observes an arithmetic identity ($\dim V^{\otimes n} = \dim \mathrm{Cl}(2n)$) and a binomial-coefficient identity ($\binom{5}{k}$ summing to $32$ matches the SU(5) one-generation rep dimensions). Both are correct. Neither is a non-trivial linear-algebraic result.

The "binomial $\leftrightarrow$ grade correspondence" of Theorem 3.2 is mis-stated: the cell weights $\binom{n}{k}$ are not the Clifford grades $\binom{2n}{k}$. The remark below the theorem acknowledges this gap but does not close it.

For the paper to be publishable, the authors would need to either:
- Construct an actual structure-preserving map $V^{\otimes n} \to \mathrm{Cl}(2n)$ (or some Clifford-related object), with a proof of its properties; or
- Substantially expand the algebraic content of the cell decomposition to yield a non-trivial linear-algebraic theorem.

The current draft does neither. I recommend the authors withdraw and reconceive the paper, perhaps as a section within their companion paper J16/J23 (where the dimensional ladder is a remark rather than the main result), or as a new paper that genuinely constructs the $V \to \mathrm{Cl}$ relationship.

I am not willing to re-review the current draft as-is; I would be willing to review a substantially restructured submission.

---

**Referee signature:** Anonymous external referee, fresh-eyes (no prior contact with the framework or its authors).
**Time spent:** ~3 hours (including independent computational verification of the cell counts).
**Conflicts of interest:** None.
