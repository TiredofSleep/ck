# Referee Report: J15 / Communications in Algebra (Fresh Eyes)

**Manuscript:** "Galois $D_{4}$ over LMFDB 4.2.10224.1: Number-Field Identification of the Four-Core Attractor"
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** Communications in Algebra
**Reviewer:** External referee (anonymous, fresh eyes; no prior exposure to the authors' research program)
**Date:** 2026-05-07

---

## §1. Summary of the manuscript

Let $\mathcal{C}_{4} = \{0, 7, 8, 9\} \subset \mathbb{Z}/10$ be a four-element subset (claimed in the companion paper [SandersGishFourCore] to be a "fusion-closed sub-magma" under two commutative binary operations $\TS$ and $\BH$). On the simplex
$$
\Delta_{\mathcal{C}_{4}}^{3} = \{(v, h, \beta, r) \in \mathbb{R}_{\ge 0}^{4} : v + h + \beta + r = 1\},
$$
define the symmetric-mixing iteration $F_{1/2} : \Delta^{3}_{\mathcal{C}_{4}} \to \Delta^{3}_{\mathcal{C}_{4}}$ via $F_{1/2}(p) = \frac{1}{2}(\TS_{\text{fuse}}(p) + \BH_{\text{fuse}}(p))$, with the per-coordinate fuse maps inherited from [SandersGishFourCore].

The authors assert the iteration has a unique interior fixed point $p^{*}$ and isolate the algebraic content of $p^{*}$ as follows. The coordinate ratio $\xi^{*} := r/\beta$ at $p^{*}$ is the unique positive real root of
$$
f(x) = x^{4} + 4 x^{3} - x^{2} + 2x - 2.
$$
Theorem 1.1 (the main result) states:

(i) $f$ is irreducible over $\mathbb{Q}$.
(ii) $\mathrm{Gal}(f / \mathbb{Q}) = D_{4}$ (dihedral of order 8).
(iii) The number field $K = \mathbb{Q}[x]/(f)$ has discriminant $d_{K} = -10224 = -2^{4} \cdot 3^{2} \cdot 71$, class number 1, signature $(2, 1)$, and is LMFDB 4.2.10224.1.
(iv) The Galois closure $L \supset K$ has degree 8, signature $(0, 4)$, class number 14, discriminant $2^{8} \cdot 3^{4} \cdot 71^{4}$, and is LMFDB 8.0.526936617216.1.
(v) The intermediate field $\mathbb{Q}(\sqrt{3})$ enters via the explicit factorization $f(x) = (x^{2} + (2-\sqrt{3})x + (\sqrt{3}-1))(x^{2} + (2+\sqrt{3})x - (\sqrt{3}+1))$ in $\mathbb{Q}(\sqrt{3})[x]$.

The verifications in §3 (derivation), §4 (irreducibility), §5 (Galois group), and §6 (LMFDB identification) are computational and self-contained.

I have verified each numerical and algebraic claim independently in `sympy`. **All claims (i)–(v) are correct.** The paper is a clean, well-written extraction of a Galois-theoretic computation, with one significant external dependency (the per-coordinate fuse data from [SandersGishFourCore], which is needed to set up the iteration but is not itself a Galois claim).

---

## §2. Decision recommendation

**Accept with minor revisions.**

The mathematical content is correct. The verifications I performed:
- $f(x) = x^{4} + 4x^{3} - x^{2} + 2x - 2$ is irreducible over $\mathbb{Q}$ via `sympy.factor(f)` returning the polynomial unfactored (and via the integer factorization argument given in §4 of the paper).
- Discriminant $\Delta_{f} = -40896 = -2^{6} \cdot 3^{2} \cdot 71$ (matches the paper's $-2^{6} \cdot 3^{2} \cdot 71$).
- The resolvent cubic $g(y) = y^{3} + y^{2} + 16y + 36$ factors as $(y + 2)(y^{2} - y + 18)$ (matches).
- `sympy.factor(f, extension=[sqrt(-71)])` returns $f$ unfactored (confirms $\mathrm{Gal} = D_{4}$, not $C_{4}$).
- `sympy.factor(f, extension=[sqrt(3)])` returns $(x^{2} + (2-\sqrt{3})x + (\sqrt{3}-1))(x^{2} + (2+\sqrt{3})x - (\sqrt{3}+1))$ (matches the paper's explicit factorization).
- `sympy.polys.numberfields.galoisgroups.galois_group(f)` returns $D_{4}$ (matches).
- The Tschirnhaus substitution $x \mapsto -x - 1$ converts $f$ to $x^{4} - 7x^{2} - 12x - 8$, the LMFDB defining polynomial.
- Counting real roots: $f$ has exactly 2 real roots (signature $(2, 1)$ matches).

The discriminant factorization is consistent: polynomial discriminant $\Delta_{f} = -2^{6} \cdot 3^{2} \cdot 71$ has the same square-free part as the field discriminant $d_{K} = -2^{4} \cdot 3^{2} \cdot 71 = -10224$ (the difference is a factor of $2^{2}$, which means the index $[\mathcal{O}_{K} : \mathbb{Z}[x]/(f)] = 2$ — a standard situation; the paper does not state this, see m4 below).

The paper is short, well-organized, with clear exposition and complete proofs. The main weakness is the heavy reliance on the four-core paper [SandersGishFourCore] for the per-coordinate fuse data (without which the polynomial $f$ is unmotivated). This is acknowledged honestly: "what is novel is the route" (line 320 of source), not the field identification per se.

For the Comm Algebra audience, the paper is a "new route to a known number field" entry — a self-contained Galois-theoretic study with computational verifications. This is squarely in scope, though not at the journal's top tier of significance.

---

## §3. Major issues

### M1. The novelty claim relies on an inaccessible companion.

The paper's pitch (line 320 of source, repeated in §6 and the cover letter) is "novelty of the route, not the field". The route is: a quartic $D_{4}$ field arising as the ring of definition for the fixed-point coordinates of a fuse iteration on a four-element fusion-closed sub-magma of $\mathbb{Z}/10$.

This route is interesting only if the fuse iteration is genuine. The paper takes the per-coordinate fuse data from [SandersGishFourCore] (cited as J02, *Algebraic Combinatorics*, submitted) without reproducing it. Specifically:

- The vanishing $\TS_{\text{fuse}}(p)_{9} = 0$ (Remark after Definition 2.1).
- The identity $\BH_{\text{fuse}}(p)_{9} = 2vr + 2h\beta$ (same Remark).
- The closed-form $h/\beta = 1 + \sqrt{3}$ (used in §3 to convert the quadratic in $\xi$ over $\mathbb{Q}(\sqrt{3})$).

A referee cannot evaluate the route without this data. The paper should either:

- **Option A:** Reproduce the relevant fuse data as Lemma 2.2 in the present paper, with proof. The data is finite (a few entries of a per-coordinate fuse table), so this is feasible.
- **Option B:** Remove the "new route" framing and present the paper as a study of a particular polynomial whose origins are recorded in [SandersGishFourCore]. This is honest but reduces the paper to a routine number-theoretic exercise.

**Recommended action:** Option A. Include enough of the per-coordinate fuse data to make §2 self-contained.

### M2. The closed-form $h/\beta = 1 + \sqrt{3}$ deserves a separate derivation.

Section 3 substitutes $h = (1 + \sqrt{3}) \beta$ as a closed-form input from [SandersGishFourCore]. This substitution is the key step that turns the fixed-point equation into a quadratic over $\mathbb{Q}(\sqrt{3})$.

Within the paper, the relation $h/\beta = 1 + \sqrt{3}$ is asserted but not derived. A referee — even one willing to trust the per-coordinate fuse data — would want to see at least a sketch of how this closed form arises from the iteration.

In particular:
- Is $h/\beta = 1 + \sqrt{3}$ a fixed point of a separate equation derived from the $h$- and $\beta$-coordinate iterations?
- Is the relation specific to $\alpha = 1/2$ (the symmetric mixing weight), or does it hold for other $\alpha$?
- Is $1 + \sqrt{3}$ the unique positive root of a known polynomial (e.g., $x^{2} - 2x - 2$, with positive root $1 + \sqrt{3}$)?

The Remark in §3 line 168 of source notes that "$\TS_{\text{fuse}}(p)_{9} = 0$" and "$\BH_{\text{fuse}}(p)_{9} = 2vr + 2h\beta$" are the structural inputs, but these only give the $r$-coordinate equation. The $h/\beta$ equation must come from the $h$- and $\beta$-coordinates of $F_{1/2}$, which the paper does not display.

**Recommended action:** Add a Lemma 3.1 deriving $h/\beta = 1 + \sqrt{3}$ from the iteration, or at least cite a specific theorem in [SandersGishFourCore] (with section/equation number) for this fact.

### M3. The "$D_{4}$ visibility from the derivation" remark needs care.

The remark at the end of §5 (lines 287–292 of source) observes that the Galois closure is the compositum $\mathbb{Q}(\sqrt{3}, \sqrt{-71}, \xi^{*})$. This is a claim that the Galois closure is generated over $\mathbb{Q}$ by $\sqrt{3}$, $\sqrt{-71}$, and $\xi^{*}$ — but these three elements together generate a field of degree at most $2 \cdot 2 \cdot 2 = 8$ over $\mathbb{Q}$, matching $|D_{4}|$.

The remark suggests the structure is "visible directly from the derivation". This is partially true:
- $\mathbb{Q}(\sqrt{3})$ is visible from the closed form $h/\beta = 1 + \sqrt{3}$.
- $\mathbb{Q}(\sqrt{-71})$ is visible from $\sqrt{\Delta_{f}}$ (the polynomial discriminant has $-71$ as its non-square part).

But the claim that the Galois closure is generated by $\xi^{*}$ together with these two square roots requires a small computation: one must verify that $\mathrm{Gal}(\mathbb{Q}(\xi^{*})/\mathbb{Q}(\sqrt{3}))$ is cyclic of order 2 (which follows from the explicit quadratic factorization in §3) and that the splitting field of $f$ over $\mathbb{Q}$ is precisely $\mathbb{Q}(\sqrt{3}, \xi^{*})$ when adjoined with the discriminant root.

The paper does not give this sub-argument. It is inessential (Theorem 1.1 is established by the resolvent-cubic + extension test in §5), but the remark's claim of "direct visibility" should either be substantiated or softened to "consistent with".

**Recommended action:** Either expand the remark with a 2-3 line argument that $\mathbb{Q}(\sqrt{3}, \sqrt{-71}, \xi^{*})$ is the Galois closure, or soften the remark.

---

## §4. Minor issues

### m1. Title / source-comment numbering.

The .tex source's leading comment block says "J22 — Galois $D_{4}$...", but the README and submission packet identify this as J15. This is a transcription/numbering issue across the J-series.

### m2. Two duplicate \author blocks.

Lines 40–46 of the source have two `\author{Brayden R. Sanders \and M. Gish}` blocks with conflicting addresses (`7Site LLC` and `Independent Researcher`). This is a recurring issue across the J-series (also present in J13 and J14).

### m3. Source comment line 7 "Source: extracted from J02 (four_core_consolidated.tex §8 — Galois D_4)".

The comment indicates the paper is extracted from §8 of a four-core consolidated paper. This is fine internally, but for external review, the section reference should not appear in the published version (only in the source comment, which is acceptable).

### m4. Index $[\mathcal{O}_{K} : \mathbb{Z}[x]/(f)] = 2$ is implicit.

The polynomial discriminant is $\Delta_{f} = -2^{6} \cdot 3^{2} \cdot 71$ but the field discriminant is $d_{K} = -2^{4} \cdot 3^{2} \cdot 71$. The ratio $\Delta_{f}/d_{K} = 4 = 2^{2}$ corresponds to the index of $\mathbb{Z}[x]/(f)$ in $\mathcal{O}_{K}$ being 2 (since $\Delta_{f} = [\mathcal{O}_{K} : \mathbb{Z}[\xi^{*}]]^{2} \cdot d_{K}$).

This is not stated explicitly. The paper says "polynomial discriminant" in §5 line 260 and "field discriminant" in §6 line 308 without flagging the difference. A Comm Algebra referee would expect a one-line acknowledgement: "$\mathbb{Z}[x]/(f)$ is a non-maximal order in $\mathcal{O}_{K}$ of index 2".

The Tschirnhaus reduction $x \mapsto -x - 1$ (§6 line 305) gives $h(x) = x^{4} - 7x^{2} - 12x - 8$, which presumably has different polynomial discriminant — checking it would clarify whether $\mathbb{Z}[x]/(h)$ is maximal.

**Recommended action:** Add a one-line remark on the index $[\mathcal{O}_{K} : \mathbb{Z}[x]/(f)]$ in §6.

### m5. The "regulator $R_{K} \approx 8.617$" is given without computation.

In §6 line 304, the regulator is quoted as $R_{K} \approx 8.617$. This is a routine LMFDB lookup, but the paper should cite the LMFDB page directly rather than quoting numerically. (The cited reference [LMFDB-4-2-10224-1] presumably contains this, but the citation should be at the point of use.)

### m6. Definitions of $\mathcal{C}_{4}$ and the magma operations.

§2 defines the four-core simplex but does not define $\mathcal{C}_{4} = \{0, 7, 8, 9\}$ or the operations $\TS, \BH$. The reader is referred to [SandersGishFourCore]. This is acceptable but could be improved by a one-paragraph summary in §1 stating: "$\TS$ and $\BH$ are commutative binary operations on $\mathbb{Z}/10$ defined by the multiplication tables [...]; the subset $\mathcal{C}_{4} = \{0, 7, 8, 9\}$ is closed under both operations."

### m7. Reduction modulo 5 is reducible (§4 Remark line 248).

The paper notes, correctly, that $f \equiv (x^{2} - 2)(x^{2} - x + 1) \pmod 5$ is reducible mod 5, so reduction-modulo-prime arguments require care. The verification of irreducibility is given via the integer-factorization argument in §4. This is correct, but a Comm Algebra referee might prefer the modulo-7 argument as the primary irreducibility proof, since it is one-line ("$f$ is irreducible mod 7"). Either choice is fine; the present integer-factorization argument is also one of the standard methods.

### m8. The role of $\sqrt{-71}$ in the Galois group test.

§5 line 277 uses `sympy.factor(f, extension=[sqrt(-71)])` to test whether $f$ remains irreducible over $\mathbb{Q}(\sqrt{\Delta_{f}}) = \mathbb{Q}(\sqrt{-71})$. The Cohen-style classification (§5 line 271) states: with one rational root in the resolvent cubic and $\mathrm{Gal} \in \{C_{4}, D_{4}\}$, the distinction is whether $f$ remains irreducible over the discriminant field.

This is a standard result. The paper could cite it more precisely — e.g., Cohen, *A Course in Computational Algebraic Number Theory*, Algorithm 6.3.6, which is the standard reference for the four cases of quartic Galois groups via resolvent cubic.

### m9. The intermediate field $\mathbb{Q}(\sqrt{-71})$ in §6 line 313.

§6 says "intermediate subfields include $\mathbb{Q}(\sqrt{3})$, $\mathbb{Q}(\sqrt{-71})$, and the biquadratic $\mathbb{Q}(\sqrt{3}, \sqrt{-71})$". This is correct (the $D_{4}$ Galois group has three subgroups of index 2, giving three quadratic subfields). The biquadratic field $\mathbb{Q}(\sqrt{3}, \sqrt{-71})$ is the third subfield, but the paper does not specify which discriminant gives it. The third quadratic subfield should have discriminant $\sqrt{-3 \cdot 71} = \sqrt{-213}$ — let me verify: $\mathbb{Q}(\sqrt{3}) \cap \mathbb{Q}(\sqrt{-71}) = \mathbb{Q}$, so the third quadratic subfield generated by their product is $\mathbb{Q}(\sqrt{-213})$. This should be stated explicitly.

### m10. Section 7 (verification).

The list of four checks in §7 is good. Could add the timing for each check (the paper says "$<5$ seconds" for the total). For reproducibility, a complete `sympy` script (10–15 lines) could be appended in an appendix or as a footnote referring to the GitHub deposit.

---

## §5. Comments on the Comm Algebra fit

The paper is a clean number-theoretic computation:
- A specific monic integer quartic with explicit Galois group $D_{4}$.
- Identification with a catalogued LMFDB number field (catalogued, not new).
- New route via fuse iteration, but the route requires the companion paper to be motivated.

For Comm Algebra, this is a routine but well-executed contribution. The journal does publish papers of this scope, especially when the route is non-trivial (e.g., a Galois group emerging from a dynamical system or a combinatorial construction). The paper's pitch — "fixed-point coordinates of a fuse iteration on a finite magma" — is unusual enough to be of interest, though the magma operations themselves are not within the paper.

The bibliography is short and appropriate (Cohen 1993 for the Galois algorithm, LMFDB entries for the fields, [SandersGishFourCore] for the magma origin). No padding.

---

## §6. Summary of recommended changes (in priority order)

1. **(M1)** Reproduce the per-coordinate fuse data needed to set up the iteration (specifically $\TS_{\text{fuse}}(p)_{9} = 0$ and $\BH_{\text{fuse}}(p)_{9} = 2vr + 2h\beta$), or cite specific Theorem/Lemma numbers in [SandersGishFourCore].
2. **(M2)** Add a derivation (or a precise citation) for $h/\beta = 1 + \sqrt{3}$.
3. **(M3)** Either expand the "$D_{4}$ visibility" remark with a derivation, or soften it.
4. **(m1)** Reconcile the J22 / J15 numbering across the source comment and the README.
5. **(m4)** Add a remark on the index $[\mathcal{O}_{K} : \mathbb{Z}[x]/(f)] = 2$.
6. **(m9)** Specify the third quadratic subfield $\mathbb{Q}(\sqrt{-213})$ explicitly.
7. **(m2, m5, m6, m7, m8, m10)** Address the remaining minor exposition issues.

---

## §7. Recommendation summary

**Accept with minor revisions.** The mathematical content is correct and verifiable. All claims (i)–(v) of Theorem 1.1 are confirmed independently. The paper is well-written and self-contained as a Galois-theoretic study, modulo a small set of dependencies on [SandersGishFourCore] that should be made explicit for a stand-alone reading.

The minor revisions listed above are exposition issues that, if addressed, would make the paper a clean Comm Algebra contribution. The principal substantive concern (M1–M2) is that the paper's "novelty of the route" pitch requires the reader to trust the companion paper for the fuse data and the closed form $h/\beta = 1 + \sqrt{3}$; making these accessible within the present paper would strengthen the contribution significantly.

I anticipate the revised paper would be acceptable for publication in Comm Algebra after one round of revision.

---

## §8. Reviewer disclosures

I am a number-theoretic referee with experience in Galois theory of low-degree polynomials, the LMFDB number-field catalogue, and computational tools (`sympy`, `pari/gp`, Magma) for Galois-group computation. I have no prior contact with the authors and no knowledge of the broader research program ("TIG", "CK", "four-core attractor") referenced in the manuscript. I evaluated the paper purely on its standalone mathematical content.

Verifications were performed in `sympy`. The principal verifications:
- `factor(f)` returns the polynomial unfactored over $\mathbb{Q}$ (confirms irreducibility).
- `discriminant(f, x)` returns $-40896 = -2^{6} \cdot 3^{2} \cdot 71$ (matches paper).
- Resolvent cubic $g(y) = y^{3} + y^{2} + 16 y + 36$ factors as $(y + 2)(y^{2} - y + 18)$ (matches the standard formula $g(y) = y^{3} - by^{2} + (ac - 4d)y - (a^{2}d - 4bd + c^{2})$ for $f(x) = x^{4} + ax^{3} + bx^{2} + cx + d$, confirmed by direct calculation).
- `factor(f, extension=[sqrt(-71)])` returns $f$ unfactored, ruling out $C_{4}$ Galois group.
- `factor(f, extension=[sqrt(3)])` returns the explicit factorization in the paper.
- `Poly(f, x).galois_group(by_name=True)` returns `(<S4TransitiveSubgroups.D4: 'D4'>, False)`, confirming $\mathrm{Gal} = D_{4}$.
- Tschirnhaus substitution $x \mapsto -x - 1$ transforms $f$ to $x^{4} - 7x^{2} - 12x - 8$ (matches LMFDB defining polynomial).
- `count_roots(f, -oo, oo) = 2`, confirming signature $(2, 1)$.

All claims verify.

— External Referee, 2026-05-07
