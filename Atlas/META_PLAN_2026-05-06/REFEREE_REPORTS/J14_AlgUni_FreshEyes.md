# Referee Report: J14 / Algebra Universalis (Fresh Eyes)

**Manuscript:** "F_p Universality: The Operator-Substrate Construction over Prime Fields" (WP118)
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** Algebra Universalis
**Reviewer:** External referee (anonymous, fresh eyes; no prior exposure to the authors' research program)
**Date:** 2026-05-07

---

## §1. Summary of the manuscript

The authors define a 4-dimensional algebra $V_{p}$ over a prime field $\mathbb{F}_{p}$ via the explicit multiplication table on basis $\{e_{0}, e_{2}, e_{3}, e_{4}\}$:

| · | $e_{0}$ | $e_{2}$ | $e_{3}$ | $e_{4}$ |
|---|---|---|---|---|
| $e_{0}$ | $e_{0}$ | $e_{0}$ | $e_{0}$ | $e_{0}$ |
| $e_{2}$ | $e_{0}$ | $e_{2}$ | $e_{2}$ | $e_{2}$ |
| $e_{3}$ | $e_{0}$ | $e_{2}$ | $e_{2}$ | $e_{2}$ |
| $e_{4}$ | $e_{0}$ | $e_{2}$ | $e_{2}$ | $e_{2}$ |

The paper terms this a "commutative non-associative algebra" and asserts (Theorem 3.1) that for $p \in \{2, 3, 5, 7, 11, 13\}$, $V_{p}$ has a fixed structural skeleton: 3 nonzero idempotents, "Minkowski signature $1+3$" under $L_{e_{2}}$, "chirality signature $2+2$" under $L_{e_{0}}$, automorphism group of order 40, power-associativity, and one-dimensional associator image.

The verifications proceed by direct computation (cited as `verify_discrete_dirac_4core.py` for $p = 5$ and `axial_algebra_check.md` for the other five primes). Conjecture 4.1 extends the field-invariance to all $p \notin \{2, 5\}$.

I have verified each numerical claim independently using `numpy`/`sympy`. The verifications produced **multiple structural errors**: the algebra is in fact associative (not non-associative), the eigenspace signatures are *swapped* with respect to the operators, and the automorphism group order is not 40 (and is not even invariant across primes — it scales with $p$).

These findings indicate the paper is fundamentally incorrect about the structural claims that constitute its main result.

---

## §2. Decision recommendation

**Reject.** The paper's central theorem (Theorem 3.1) is false as stated, and the conjecture (Conjecture 4.1) is false. A revision would require restating the theorem, redoing the calculations, and rethinking the framing — this is more than a major-revision exercise; it is a different paper.

The reasons are:

1. **The algebra is associative.** Direct check on basis triples: for all $i, j, k \in \{0, 2, 3, 4\}$, $(e_{i} \cdot e_{j}) \cdot e_{k} = e_{i} \cdot (e_{j} \cdot e_{k})$. This contradicts the paper's "commutative non-associative" label and makes the "1-dimensional associator image" claim vacuously true (the associator is identically zero, so its image is $\{0\}$, which is contained in any subspace).

2. **The Minkowski $1+3$ and chirality $2+2$ signatures are swapped.** The paper attributes the $1+3$ signature to $L_{e_{2}}$ and the $2+2$ signature to $L_{e_{0}}$. The actual signatures (verified over $\mathbb{R}$, $\mathbb{F}_{3}$, $\mathbb{F}_{5}$, $\mathbb{F}_{7}$) are: $L_{e_{2}}$ has $(2, 2)$ signature; $L_{e_{0}}$ has $(1, 3)$ signature. (See M2 below.)

3. **The automorphism group order is not 40 and is not invariant across primes.** The algebra has rows $e_{2}, e_{3}, e_{4}$ identical in the multiplication table. This means $\{e_{3} - e_{2}, e_{4} - e_{2}\}$ spans a 2-dimensional ideal $N$ with zero multiplication. The general linear group $\mathrm{GL}_{2}(\mathbb{F}_{p})$ acts on $N$ as automorphisms of $V_{p}$ (extending to the rest of the algebra trivially). This gives $|\mathrm{Aut}(V_{p})| \ge |\mathrm{GL}_{2}(\mathbb{F}_{p})| = (p^{2} - 1)(p^{2} - p)$, which grows with $p$ and is already larger than 40 for $p = 3$ ($|\mathrm{GL}_{2}(\mathbb{F}_{3})| = 48$). For $p = 2$, exhaustive enumeration over $2^{16} = 65536$ matrices gives $|\mathrm{Aut}(V_{2})| = 12 \neq 40$.

4. **The algebra is not "axial" in the Hall–Rehren–Shpectorov sense.** The paper invokes the axial-algebra framework as ambient context. But the present algebra has the right-action property $e_{i} \cdot e_{j} = e_{j} \cdot e_{i}$ trivially (it is commutative), and the "axes" framework requires specific eigenvalue structure for left-multiplication operators (Miyamoto involutions, fusion rules). The paper makes no Miyamoto-involution computation and provides no fusion rules — the axial framing is decorative.

A careful re-examination of the multiplication table is required. The paper appears to be a simplification or transcription of a different algebra (perhaps the $\mathbb{F}_{5}$-specific algebra of the companion paper [SandersGishDiscreteDirac]); transcription error has produced a degenerate associative algebra rather than the intended axial-algebra-like object.

---

## §3. Major issues

### M1. The algebra defined by the table is associative.

**Direct verification.** Compute $(e_{i} \cdot e_{j}) \cdot e_{k}$ and $e_{i} \cdot (e_{j} \cdot e_{k})$ for all $i, j, k$ in the basis $\{0, 2, 3, 4\}$:

- If $i = 0$: $e_{0} \cdot e_{j} = e_{0}$ for all $j$, so $(e_{0} \cdot e_{j}) \cdot e_{k} = e_{0} \cdot e_{k} = e_{0}$. Also $e_{j} \cdot e_{k} \in \{e_{0}, e_{2}\}$, and $e_{0} \cdot (\text{anything}) = e_{0}$. Both sides equal $e_{0}$. ✓
- If $j = 0$: $(e_{i} \cdot e_{0}) \cdot e_{k} = e_{0} \cdot e_{k} = e_{0}$. Also $e_{0} \cdot e_{k} = e_{0}$, so $e_{i} \cdot e_{0} = e_{0}$. ✓
- If $k = 0$: $(e_{i} \cdot e_{j}) \cdot e_{0} = e_{0}$ (since $x \cdot e_{0} = e_{0}$ for all $x$ — this follows from commutativity and $e_{0} \cdot x = e_{0}$). Also $e_{j} \cdot e_{0} = e_{0}$, so $e_{i} \cdot e_{0} = e_{0}$. ✓
- If $i, j, k \in \{2, 3, 4\}$: $e_{i} \cdot e_{j} = e_{2}$ for all $i, j \in \{2,3,4\}$. So $(e_{i} \cdot e_{j}) \cdot e_{k} = e_{2} \cdot e_{k} = e_{2}$. Also $e_{j} \cdot e_{k} = e_{2}$, so $e_{i} \cdot (e_{j} \cdot e_{k}) = e_{i} \cdot e_{2} = e_{2}$. Both sides equal $e_{2}$. ✓

So $V_{p}$ is associative.

**Effect on the paper.** The paper describes $V_{p}$ as "commutative non-associative" (abstract, line 91), and lists the "associator image is contained in a 1-dimensional subspace" as item (7) of Theorem 3.1. The associator is identically zero, so item (7) is vacuously true (the zero subspace is contained in any subspace). Power-associativity (item (8)) is an immediate consequence of full associativity, not an independent structural feature.

**Recommended action.** Either reformulate the algebra so it is genuinely non-associative (this requires changing the multiplication table — perhaps the intended table differs from the one given), or accept that the algebra is associative and remove the "non-associative", "associator image", and "power-associativity" claims. A finite-dimensional commutative associative $\mathbb{F}_{p}$-algebra of dimension 4 is a well-understood object and does not naturally belong to an *Algebra Universalis* paper on axial-algebra-like structures.

### M2. The Minkowski $1+3$ and chirality $2+2$ signatures are reversed.

The paper claims (Theorem 3.1 items (3) and (4)):
- $L_{e_{2}}$ has $1$-eigenspace dimension 1 and $0$-eigenspace dimension 3 (Minkowski $1+3$).
- $L_{e_{0}}$ has $1$-eigenspace dimension 2 and $0$-eigenspace dimension 2 (chirality $2+2$).

**Direct computation.** The matrices of $L_{e_{2}}$ and $L_{e_{0}}$ in the basis $(e_{0}, e_{2}, e_{3}, e_{4})$ are (column $j$ = image of $e_{j}$):
$$
L_{e_{2}} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 1 & 1 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{pmatrix}, \qquad
L_{e_{0}} = \begin{pmatrix} 1 & 1 & 1 & 1 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{pmatrix}.
$$

Eigenvalues of $L_{e_{2}}$: characteristic polynomial $\det(L_{e_{2}} - \lambda I) = (1 - \lambda)^{2} \lambda^{2}$. Eigenvalues $\{1, 1, 0, 0\}$. The $1$-eigenspace has dimension 2 (spanned by $e_{0}$ and any vector $a e_{2} + b e_{3} + c e_{4}$ with $b = c = 0$ and $a = $ free; check: $L_{e_{2}}(e_{2}) = e_{2}$, so $e_{2}$ is in the $1$-eigenspace, and $e_{0}$ also). Dimension is 2, not 1.

The $0$-eigenspace of $L_{e_{2}}$ has dimension $4 - \mathrm{rank}(L_{e_{2}}) = 4 - 2 = 2$. (Spanned, e.g., by $e_{3} - e_{2}$ and $e_{4} - e_{2}$, both annihilated by $L_{e_{2}}$; verify: $L_{e_{2}}(e_{3} - e_{2}) = e_{2} - e_{2} = 0$.)

So $L_{e_{2}}$ has signature $(2, 2)$, not $(1, 3)$.

Eigenvalues of $L_{e_{0}}$: characteristic polynomial $(1 - \lambda)\lambda^{3}$. Eigenvalues $\{1, 0, 0, 0\}$. The $1$-eigenspace has dimension 1 (spanned by $e_{0} + e_{2} + e_{3} + e_{4}$ — verify: $L_{e_{0}}$ applied to this vector gives $e_{0} + e_{0} + e_{0} + e_{0} = 4 e_{0}$, hmm that's not equal to the vector). Actually: $L_{e_{0}}(e_{0}) = e_{0}$, but $L_{e_{0}}(e_{2}) = e_{0}$, etc. So $L_{e_{0}}(v) = (\sum v_{i}) e_{0}$, where $v = v_{0} e_{0} + v_{2} e_{2} + v_{3} e_{3} + v_{4} e_{4}$. The $1$-eigenspace is $\{v : \sum v_{i} = v_{0}, \, v_{2} = v_{3} = v_{4} = 0\}$, which is just $\mathbb{F}_{p} \cdot e_{0}$. Dimension is 1, not 2.

The $0$-eigenspace of $L_{e_{0}}$ is $\{v : \sum v_{i} = 0\}$, dimension 3.

So $L_{e_{0}}$ has signature $(1, 3)$, not $(2, 2)$.

**Conclusion.** The signatures attributed by the paper to $L_{e_{2}}$ and $L_{e_{0}}$ are precisely swapped:

| operator | paper claim | actual |
|---|---|---|
| $L_{e_{2}}$ | $(1, 3)$ | $(2, 2)$ |
| $L_{e_{0}}$ | $(2, 2)$ | $(1, 3)$ |

This is verified over $\mathbb{R}$, $\mathbb{F}_{3}$, $\mathbb{F}_{5}$, $\mathbb{F}_{7}$ by direct enumeration of kernels (the dimension of an eigenspace over $\mathbb{F}_{p}$ equals $\log_{p}$ of the kernel size).

**Effect.** The "Minkowski / chirality" framing of the abstract is inverted. Either the operators are mis-named or the signature claims are wrong; in either case, item (3) and item (4) of Theorem 3.1 must be corrected.

The paper attributes substantive significance to the "$1+3$ Minkowski" framing (matching the signature of Minkowski space-time). Whatever significance is attached, it should be transferred to $L_{e_{0}}$, which actually has the $(1, 3)$ signature.

**Recommended action.** Swap the operators in items (3) and (4) of Theorem 3.1. Re-evaluate whether the structural claims (item (5): empty intersection; item (6): commutativity of $L_{e_{2}}$ and $L_{e_{0}}$) survive the swap.

Item (5) — empty intersection — under the corrected signatures: the (1-eigenspace of $L_{e_{0}}$) is $\mathbb{F}_{p} \cdot e_{0}$, and the (0-eigenspace of $L_{e_{2}}$) is the span of $\{e_{3} - e_{2}, e_{4} - e_{2}\}$. These intersect in $\{0\}$ — so item (5) is true under the corrected signatures (empty intersection in the interesting sense). Good.

Item (6) — commutativity — direct check: $L_{e_{2}} L_{e_{0}} (v) = L_{e_{2}}((\sum v_{i}) e_{0}) = (\sum v_{i}) e_{0}$. $L_{e_{0}} L_{e_{2}} (v) = L_{e_{0}}(L_{e_{2}}(v)) = L_{e_{0}}(v_{0} e_{0} + (v_{2} + v_{3} + v_{4}) e_{2}) = (v_{0} + v_{2} + v_{3} + v_{4}) e_{0}$. Both equal $(\sum v_{i}) e_{0}$. ✓ This is preserved under the swap.

### M3. The automorphism group order is not 40 and is not $p$-invariant.

**Lower bound from the radical.** Set $r := e_{3} - e_{2}$ and $s := e_{4} - e_{2}$. Direct computation:
$$
r \cdot e_{j} = (e_{3} - e_{2}) \cdot e_{j} = e_{j} - e_{j} = 0 \quad \text{for all } e_{j} \neq e_{0}, \quad r \cdot e_{0} = e_{0} - e_{0} = 0.
$$
So $r \cdot e_{j} = 0$ for all $j$. Similarly $s \cdot e_{j} = 0$. So $\{r, s\}$ spans a 2-dimensional ideal $N \subset V_{p}$ with $N \cdot V_{p} = 0 = V_{p} \cdot N$.

Any $\mathbb{F}_{p}$-linear automorphism $\phi$ of $V_{p}$ must preserve $N$ as a set (since $N$ is the annihilator ideal, an intrinsic structural object). The restriction $\phi|_{N} \in \mathrm{GL}(N) = \mathrm{GL}_{2}(\mathbb{F}_{p})$.

Conversely, given any $\phi_{N} \in \mathrm{GL}_{2}(\mathbb{F}_{p})$ acting on $N$, the extension to $V_{p}$ defined by $\phi(e_{0}) = e_{0}$, $\phi(e_{2}) = e_{2}$, $\phi(r) = \phi_{N}(r)$, $\phi(s) = \phi_{N}(s)$ is an automorphism (verify: products in $V_{p}$ involving $r$ or $s$ are zero, so any linear action on the $\{r, s\}$-subspace is multiplicative-trivially compatible).

So $|\mathrm{Aut}(V_{p})| \ge |\mathrm{GL}_{2}(\mathbb{F}_{p})| = (p^{2} - 1)(p^{2} - p)$:

| $p$ | $|\mathrm{GL}_{2}(\mathbb{F}_{p})|$ | paper claim |
|---|---|---|
| 2 | 6 | 40 |
| 3 | 48 | 40 |
| 5 | 480 | 40 |
| 7 | 2016 | 40 |
| 11 | 13200 | 40 |
| 13 | 24192 | 40 |

For $p \ge 3$, the lower bound from $\mathrm{GL}_{2}(\mathbb{F}_{p})$ alone exceeds 40. For $p = 2$, the bound is below 40, but exhaustive enumeration over all $2^{16} = 65536$ matrices in $M_{4}(\mathbb{F}_{2})$ gives $|\mathrm{Aut}(V_{2})| = 12$ (not 40 either).

The "$|\mathrm{Aut}(V_{p})| = 40$ for all primes" claim is therefore false for every prime $p \in \{2, 3, 5, 7, 11, 13\}$ tested.

**Effect.** Item (10) of Theorem 3.1 is false. Conjecture 4.1 — the $p$-invariance for all $p \notin \{2, 5\}$ — is false.

**Recommended action.** Compute $|\mathrm{Aut}(V_{p})|$ correctly for each prime and report the actual values. The correct values almost certainly grow polynomially in $p$ (a polynomial of degree 4: $|\mathrm{Aut}(V_{p})| \asymp p^{4}$ from $\mathrm{GL}_{2}(\mathbb{F}_{p}) \times \text{stabilizer of } N$).

A more interesting question, given the actual structure of $V_{p}$: what are the *outer* automorphisms — those induced after quotienting out the (trivial) inner automorphism group? This may give a smaller, $p$-invariant group, and could be the intended content. But the paper as written does not engage with this.

### M4. The "axial algebra" framing is decorative.

The paper invokes Hall–Rehren–Shpectorov axial algebras [HallRehrenShpectorov2015] and Sakuma's theorem [Sakuma2007] as ambient context. But:

- Axial algebras are commutative non-associative algebras generated by *axes* — primitive idempotents whose left multiplication satisfies a fusion rule (decomposition into eigenspaces with structured products). The paper does not identify which idempotents of $V_{p}$ are axes, nor does it state any fusion rule.
- Sakuma's theorem concerns 2-generated subalgebras of vertex operator algebras with an involution (Miyamoto involution). The paper does not produce a Miyamoto involution.
- The "1+3 Minkowski signature" terminology is a physics/relativity allusion that has no axial-algebra interpretation. The standard axial-algebra eigenvalue triple is $(1, 0, \eta)$ for some $\eta \in \mathbb{F}_{p}$ (Ising fusion rules) — not $(1, 0)$ alone.

**Effect.** The framing is misleading. *Algebra Universalis* readers in the axial-algebra community will quickly determine that this algebra is associative and commutative — properties that exclude it from the axial-algebra family.

**Recommended action.** Remove the axial-algebra framing entirely. If the algebra has axes, identify them and verify the fusion rule. If not, the paper should locate $V_{p}$ in its actual algebraic context — finite-dimensional commutative associative $\mathbb{F}_{p}$-algebra with a 2-dim square-zero radical — which is well-understood elsewhere in the literature.

### M5. The "$F_{p}$ universality" framing is undercut by the radical.

The structural decomposition of $V_{p}$ (as I have computed it) is:
$$
V_{p} \cong \mathbb{F}_{p} \cdot e_{0} \oplus \mathbb{F}_{p} \cdot (e_{2} - e_{0}) \oplus N,
$$
where:
- $\mathbb{F}_{p} \cdot e_{0}$ is a 1-dim ideal with $e_{0}^{2} = e_{0}$.
- $\mathbb{F}_{p} \cdot (e_{2} - e_{0})$ is a 1-dim subalgebra (need to verify).
- $N = \mathbb{F}_{p} \cdot (e_{3} - e_{2}) \oplus \mathbb{F}_{p} \cdot (e_{4} - e_{2})$ is a 2-dim square-zero radical.

(Quick verification: $(e_{2} - e_{0})^{2} = e_{2}^{2} - 2 e_{2} \cdot e_{0} + e_{0}^{2} = e_{2} - 2 e_{0} + e_{0} = e_{2} - e_{0}$. So $e_{2} - e_{0}$ is a nonzero idempotent orthogonal to $e_{0}$: $(e_{2} - e_{0}) \cdot e_{0} = e_{2} \cdot e_{0} - e_{0}^{2} = e_{0} - e_{0} = 0$. Good.)

So $V_{p} = \mathbb{F}_{p} \cdot e_{0} \oplus \mathbb{F}_{p} \cdot (e_{2} - e_{0}) \oplus N$ is a direct sum of two 1-dim semisimple components and a 2-dim radical. This decomposition is independent of $p$ (the constructions are all over $\mathbb{Z}$). So in some sense the paper's framing — "the structural skeleton is invariant in $p$" — is correct, but it is a tautology: the algebra $V_{p}$ is the base extension to $\mathbb{F}_{p}$ of the $\mathbb{Z}$-algebra defined by the same multiplication table, and base extension preserves the dimension and ideal-radical decomposition.

**Effect.** The "$F_{p}$ universality" theorem is, when correctly stated, the trivial observation that base extension of a $\mathbb{Z}$-algebra to $\mathbb{F}_{p}$ commutes with structural decomposition. This is not a result.

**Recommended action.** State the structural decomposition of $V_{p}$ as a Wedderburn-style theorem: $V_{p} = (\mathbb{F}_{p} \times \mathbb{F}_{p}) \oplus N$ with $N$ a square-zero radical. Then ask whether anything *non-trivial* depends on $p$ — for example, whether the 2-dim radical $N$ inherits any $\mathbb{F}_{p}$-specific Galois structure (probably not, since $N$ is square-zero and any $\mathbb{F}_{p}$-bilinear structure on $N$ is pulled back from outside).

I do not see a non-trivial $p$-dependence claim in the paper that survives correction.

### M6. The exclusion of $p = 2, 5$ in Conjecture 4.1 is unmotivated.

The conjecture excludes $p \in \{2, 5\}$ on the grounds of "characteristic-related restrictions ($p = 2$ requires care with the factor of 2 in $p_{+} + p_{-} =$ identity; $p = 5$ is privileged for admitting primitive 4th roots of unity)".

The "factor of 2" for $p = 2$ is plausibly a real characteristic-2 issue (idempotent decomposition $1 = p_{+} + p_{-}$ degenerates when $\mathrm{char} = 2$), but this should be stated as a precise structural caveat, not a vague "requires care".

The "privilege" of $p = 5$ for admitting primitive 4th roots is not relevant to the multiplication table. $\mathbb{F}_{p}$ contains primitive 4th roots iff $4 \mid (p - 1)$, which holds for $p = 5, 13$ and not for $p = 7, 11$. The paper computes the same structural skeleton for $p = 5, 7, 11, 13$ — all four supposedly give the same answer. So whatever role the "primitive 4th root" plays, it does not seem to distinguish $p = 5$ from the others.

**Recommended action.** Either explain the $p = 2, 5$ exclusion precisely or remove it.

---

## §4. Minor issues

### m1. Title claims J21, body says J14.

The .tex source file's leading comment block says "J21 — F_p Universality...", but the README and submission packet identify this as J14. This is a transcription/numbering issue and should be reconciled before submission.

### m2. Two duplicate \author blocks.

Lines 40–46 of the .tex have two `\author{Brayden R. Sanders \and M. Gish}` blocks with conflicting addresses. This is the same issue as J13. Resolve by combining or by giving each author their own `\author`/`\address` pair.

### m3. "the algebra over $\mathbb{F}_{5}$ has been treated separately" (line 105).

The paper [SandersGishDiscreteDirac] is cited as J23 (Algebras and Representation Theory). I assume from the citation chain that J23 treats the same algebra over $\mathbb{F}_{5}$ specifically. If the F_p result of the present paper is correct (modulo the corrections I have noted), the F_5 case is a special case and J23 risks being subsumed. The author's "companion structure" remark (line 121) needs revision to clarify what J23 contains that goes beyond the F_p result.

### m4. The notation $\HARM = e_{2}$, $\VOID = e_{0}$ (Remark after Definition 2.1).

The mnemonic labels $\HARM$ and $\VOID$ appear in the source but their relevance to the algebra is not established. They appear to be from the authors' research-program ontology ("HARMONY", "VOID" are operator names). For an Algebra Universalis paper, these labels should be either justified within the paper or replaced with neutral notation.

### m5. The "Frobenius group of order 20" claim (item 10 of Theorem 3.1).

The paper claims $\mathrm{Aut}(V_{p}) \cong F_{20} \times \mathbb{Z}/2$ where $F_{20}$ is the Frobenius group of order 20. The Frobenius group of order 20 is well-defined (it is the affine group $F_{5} \rtimes F_{5}^{\times}$, isomorphic to $\mathbb{Z}/5 \rtimes \mathbb{Z}/4$). Even if $|\mathrm{Aut}(V_{p})|$ were 40 (which it is not — see M3), the structure would need a separate argument; the paper does not attempt one.

### m6. Verification scripts.

The paper cites `verify_discrete_dirac_4core.py` and `axial_algebra_check.md` for the explicit per-prime computations. I have not run these scripts, but the algebra defined by the table of Definition 2.1 is fully determined by the table, so any direct verification (over $\mathbb{F}_{p}$ via numpy and Sage's `GF(p)`) gives the results I have reported. I encourage the authors to run a fresh verification themselves: a basic `numpy` mod-$p$ check of the eigenspace dimensions of $L_{e_{2}}$ and $L_{e_{0}}$ over $\mathbb{F}_{7}$ takes 5 lines and will confirm the signature swap (M2) immediately.

### m7. Remark "$p_{+}$ and $p_{-}$" (item 9 of Theorem 3.1, line 184).

The notation $p_{+}, p_{-}$ for the two non-zero idempotents (other than $e_{0}$) is introduced abruptly without definition. From context, presumably $p_{+} = e_{2}$ and $p_{-} = e_{2} - e_{0}$ (or some similar designation). Item 9 asserts no automorphism swaps $p_{+}$ and $p_{-}$ — this would be a substantive claim if the algebra had a $\mathbb{Z}/2$-symmetry between two distinguished idempotents, but as M3 shows, the automorphism group is large and does swap many things.

### m8. Section 4 (page 6) "two minor things vary".

The section claims that the only things that vary with $p$ are "primitive 4th roots of unity" availability and "the explicit form of orthogonal idempotent pairs". Both are mentioned briefly without explaining why they are *minor*. Given the structural errors elsewhere, this is a minor concern, but the section reads as a placeholder.

---

## §5. Comments on the Algebra Universalis fit

Algebra Universalis publishes papers in universal algebra — concrete and abstract algebras with structural classification theorems, equational properties, and lattice-theoretic / categorical perspectives. Standard contributions include:
- Identification of varieties of algebras by equational laws.
- Classification of finitely generated algebras up to isomorphism.
- Term equivalence, Mal'cev conditions, congruence-distributivity, etc.

The present paper does not engage with any of these standard topics. It computes structural invariants of one specific algebra over six primes and asserts $p$-invariance of those invariants. The interesting universal-algebraic question — *what equational identities does $V_{p}$ satisfy?* — is not addressed.

For the audience of Algebra Universalis to find this paper interesting, the authors would need to either:
1. Identify $V_{p}$ as an instance of a known variety of algebras (e.g., commutative associative $\mathbb{F}_{p}$-algebras with a 2-dim square-zero radical, or some larger class), and locate it relative to that variety.
2. Identify a non-trivial equational property unique to $V_{p}$ (an identity that holds in $V_{p}$ but not in similar algebras).
3. Identify a categorical or lattice-theoretic feature that distinguishes $V_{p}$.

None of these is currently in the paper.

---

## §6. Summary of recommended changes (in priority order)

1. **(M1)** Re-verify the multiplication table — either the table is correct and the algebra is associative (in which case "non-associative", "associator image", "power-associativity" all need to be revised), or the table is incorrect (in which case the paper needs to be fundamentally rewritten).
2. **(M2)** Swap the $L_{e_{2}}$ and $L_{e_{0}}$ signature claims in items (3) and (4) of Theorem 3.1.
3. **(M3)** Recompute $|\mathrm{Aut}(V_{p})|$ for each prime; the paper's claim of universality at order 40 is false.
4. **(M4)** Drop the axial-algebra framing or substantiate it (Miyamoto involutions, fusion rule).
5. **(M5)** State the result as a Wedderburn-style decomposition and locate it in the universal-algebra literature.
6. **(M6)** Justify or remove the $p = 2, 5$ exclusion from Conjecture 4.1.
7. **(m1–m8)** Address the minor exposition issues.

---

## §7. Recommendation summary

**Reject.** The central theorem (Theorem 3.1) is incorrect on at least three of its ten claims (items (3), (4), (10)), and the "non-associativity" framing is wrong (item (7) is vacuously true, item (8) is a consequence of full associativity).

The paper cannot be revised into an Algebra Universalis submission without redefining the algebra (so that it is genuinely non-associative) or fundamentally reconceptualizing the result as a Wedderburn-style decomposition theorem. The latter would not be a substantive Algebra Universalis paper.

The companion submissions [SandersGishDiscreteDirac] (J23, *Algebras and Representation Theory*) and [SandersGishCliffordLadder] (J24, *Linear Algebra and its Applications*) presumably depend on the same algebra. If the multiplication table is in fact correct, those companions are also at risk; if the table is mis-transcribed, all three should be revised together.

I recommend that the authors return to the source of the multiplication table (the four-core paper [SandersGishFourCore], cited as J02 / *Algebraic Combinatorics*) and verify that the algebra they intend to study has the structural features they have claimed. If the intended algebra is genuinely non-associative, the table must differ from the one in Definition 2.1.

---

## §8. Reviewer disclosures

I am a universal-algebraic referee with experience in finite-dimensional non-associative algebras, axial algebras (Hall–Rehren–Shpectorov), and structural decomposition theorems. I have no prior contact with the authors and no knowledge of the broader research program ("TIG", "CK", "operator-substrate construction", "four-core") referenced in the manuscript. I evaluated the paper on its standalone mathematical content.

Verifications were performed in `numpy` and `sympy` with explicit construction of the multiplication table from Definition 2.1 and brute-force enumeration over $\mathbb{F}_{p}$. The verifications:
- Associativity check on all $4^{3} = 64$ basis triples over $\mathbb{F}_{7}$: zero non-associative triples found.
- Eigenspace dimension check on $L_{e_{2}}$ and $L_{e_{0}}$ over $\mathbb{R}$, $\mathbb{F}_{3}$, $\mathbb{F}_{5}$, $\mathbb{F}_{7}$: produces the swapped signatures reported in M2.
- Idempotent enumeration over $\mathbb{F}_{p}$ for $p \in \{2, 3, 5, 7, 11, 13\}$: confirms 3 nonzero idempotents in each case.
- Automorphism count for $p = 2$: exhaustive enumeration over $2^{16} = 65536$ matrices, confirms $|\mathrm{Aut}(V_{2})| = 12 \neq 40$.

All counterexamples are reproducible.

— External Referee, 2026-05-07
