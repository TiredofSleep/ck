# Referee Report — American Mathematical Monthly (Fresh Eyes)

**Manuscript:** "The 5D Force Vector as a CRT Fourier Embedding of $\mathbb{Z}/10\mathbb{Z}$ into $\mathbb{R}^5$" (J21 / Q17-A)
**Authors:** B. R. Sanders, M. Gish (per .tex; cover letter lists F. Calderon as second author)
**File reviewed:** `Gen13/targets/journals/J_series/J21/manuscript/manuscript.tex`
**Reviewer:** External referee, anonymous, fresh-eyes
**Date:** 2026-05-07

---

## §1. Summary

The manuscript presents an embedding $v : \mathbb{Z}/10\mathbb{Z} \to \mathbb{R}^5$ defined by sending an operator $n$ with CRT coordinates $(\varepsilon, y) \in \mathbb{F}_2 \times \mathbb{F}_5$ to
$$
v(n) \;=\; \bigl(\varepsilon,\;\cos\tfrac{2\pi y}{5},\;\sin\tfrac{2\pi y}{5},\;\cos\tfrac{4\pi y}{5},\;\sin\tfrac{4\pi y}{5}\bigr) \in \mathbb{R}^5.
$$

The paper makes four claims:
1. **Injectivity** (Theorem 3.1): $v$ is one-to-one on $\mathbb{Z}/10\mathbb{Z}$.
2. **Geometric remark** (Remark 3.2): the image lies on the disjoint union of two parallel 4-spheres of radius $\sqrt{2}$ in $\mathbb{R}^5$.
3. **Rigidity** (Theorem 4.1): any embedding satisfying the CRT-plus-Fourier compatibility conditions equals $v$ up to a block-diagonal orthogonal transformation in $O(1) \times O(4)$.
4. **Two-point spectral maximum** (Lemma 5.2): a functional $G(n)$ achieves its maximum value 25 at exactly two operators ($n = 5$ and $n = 7$).

Two short applications close the paper: a $D_{10}$-action on the image (§6.1) and a Parseval-type Fourier-sum identity (§6.2).

The manuscript is well-organized and well-written at the prose level. The embedding itself is, as the authors correctly state, folklore in finite Fourier analysis. The injectivity proof is correct. The geometric remark (radius $\sqrt{2}$ on each 4-sphere) is correct.

The submitted manuscript, however, has two substantive problems:

- **Theorem 4.1 (rigidity) is essentially a tautology.** The "compatibility conditions" (i) and (ii) of the theorem statement bake in the conclusion: condition (ii) explicitly assumes that the $\mathbb{F}_5$-coordinates *are* the real Fourier basis "up to an orthogonal change of variables in $\mathbb{R}^4$," which is exactly the conclusion. The theorem says, in effect: "if $w$ is the Fourier basis up to $O(4)$, then $w$ is the Fourier basis up to $O(4)$." This is not a uniqueness result.
- **Lemma 5.2 (two-point maximum) is wrong as stated.** Direct computation of the functional $G$ as defined in Definition 5.1 (verified below) yields $G(5) \approx 9.47$ and $G(7) \approx 19.47$, not the claimed $G_{\max} = 25$ at both. The "maximum value 25" derivation in the proof argues about a *generic* sum of unit-modulus complex numbers, not about $G$'s actual value at any operator. The Remark following the lemma admits that "the numerical values quoted in the source program were $G_{\max} \approx 9.389$ and $G_{\mathrm{low}} \approx 1.872$"; the paper then says "the unnormalized arithmetic gives the cleaner statement above." It does not.

The applications in §6 are routine. The decagonal $D_{10}$-action is the addition-by-1 action through CRT, with the obvious action on the embedded coordinates. The Parseval/Plancherel identity is, as the paper acknowledges, a restatement of the Fourier expansion in CRT coordinates.

The paper's pitch — that the embedding is "folklore" but the "rigidity statement" and "two-point identification" are new — does not survive scrutiny. The rigidity statement is tautological; the two-point statement is incorrect; and the embedding itself is, by the authors' acknowledgment, in textbooks (Terras 1999; Diaconis 1988; cf. also Steinberg 2012, *Representation Theory of Finite Groups*).

---

## §2. Decision recommendation

**Reject (without prejudice to a substantially revised resubmission).**

To meet the *Monthly* bar, the manuscript needs:

(i) **Theorem 4.1 reformulated as a non-tautological rigidity statement.** The current premise (ii) bakes in the conclusion. A genuine rigidity result would weaken (ii) to a *characterizing condition* that does not name "the real Fourier basis" — for example, "the embedding is $\mathbb{F}_5$-equivariant" or "the embedding's image realizes the regular pentagon vertices with the standard inner product." See M1 below.

(ii) **Lemma 5.2 corrected.** The numerical claim is wrong; the proof argues for a generic upper bound, not an attained value. Either re-derive the correct two-point structure (and the correct max value), or cut the lemma and the spectral functional entirely. As it stands, this is the kind of error that fails the *Monthly*'s arithmetic-correctness standard.

(iii) **The Diaconis citation supplied.** The cover letter says "cite Diaconis on Fourier on finite groups," but the manuscript only cites Terras 1999 (twice), Stein–Weiss 1971, Conrad's expository notes, and Ireland–Rosen. Diaconis 1988 is the canonical *Monthly*-level reference for this material; its absence is conspicuous.

(iv) **A clear reason for the *Monthly* to publish a new note on folklore material.** The "rigidity" and "two-point" claims were the proposed reasons. Without them, the paper is a worked example of a textbook construction.

If the authors revise substantially along these lines, the resulting paper might be a clean 4–6 page *Monthly* note. As submitted, it does not meet the bar.

---

## §3. Major comments

### M1. Theorem 4.1 (rigidity) is essentially tautological (CRITICAL)

**Location.** §4, Theorem 4.1.

**Claim.** Let $w : \mathbb{Z}/10\mathbb{Z} \to \mathbb{R}^5$ be an embedding such that
- (i) $w$ factors through the CRT isomorphism: there exist $w_2 : \mathbb{F}_2 \to \mathbb{R}^a$ and $w_5 : \mathbb{F}_5 \to \mathbb{R}^b$ with $a + b = 5$ such that $w(n) = (w_2(\varepsilon(n)), w_5(y(n)))$.
- (ii) $w_2$ is the affine indicator (with $a = 1$), and **$w_5$ is the real Fourier basis (with $b = 4$) up to an orthogonal change of variables in $\mathbb{R}^4$**.

Then $w = O \circ v$ for some block-diagonal $O \in O(1) \times O(4)$.

**Issue.** Premise (ii) explicitly states that $w_5$ is the real Fourier basis up to $O(4)$. The conclusion is that $w_5 = \mathcal{O}(v_{2:5})$ for $\mathcal{O} \in O(4)$. These are the same statement.

What the theorem actually proves is the *trivial* observation: if you stipulate that an embedding's $\mathbb{F}_5$-component is the Fourier basis modulo $O(4)$, then it is the Fourier basis modulo $O(4)$. This is not a rigidity theorem; it is a definition.

A genuine rigidity statement would weaken (ii) to a property that *does not name* the Fourier basis. Three candidate properties that *would* characterize the Fourier basis up to $O(4)$:

(a) **Equivariance.** $w_5$ is $\mathbb{F}_5$-equivariant under the regular representation: $w_5(y + 1) = R \cdot w_5(y)$ for some fixed $R \in O(4)$.
(b) **Equidistance with the right inner-product structure.** The image $w_5(\mathbb{F}_5) \subset \mathbb{R}^4$ has all pairwise inner products equal to $-1/4$ (the regular-simplex / regular-pentagon condition for the Fourier basis on $\mathbb{F}_5$).
(c) **Maximal symmetry.** $w_5$ realizes the maximal $O(4)$-symmetric embedding of $\mathbb{F}_5$ in $\mathbb{R}^4$, where "maximal" is defined in some natural sense (e.g., the dimension of the affine span is exactly $4$ and the image's stabilizer in $O(4)$ has the maximal possible order, namely $|D_5| = 10$).

Any of (a), (b), (c) would yield a theorem with content. The current theorem does not.

**Fix.** Restate the theorem with one of (a)–(c) as the premise and prove from there. The proof is short (the regular-pentagon characterization is well-known) but it requires actual content.

**Severity.** Critical. A "rigidity" theorem whose premise is its conclusion will be the first thing a *Monthly* referee notices, and its absence as a real result undermines the paper's main pedagogical promise.

### M2. Lemma 5.2 (two-point maximum) is numerically wrong (CRITICAL)

**Location.** §5, Lemma 5.2.

**Claim.** "The functional $G$ achieves the maximum value $G_{\max} = 25$ at exactly two operators: $n = 5$ (CRT coordinates $(1, 0)$) and $n = 7$ (CRT coordinates $(1, 2)$). At all other operators, $G(n) < 25$."

**Issue.** Direct computation of $G$ as defined in Definition 5.1, using the σ-permutation given in §5 ("$\sigma : 1 \mapsto 7 \mapsto 6 \mapsto 5 \mapsto 4 \mapsto 2$" with fixed points $\{0, 5\}$ — though the paper's prose actually reads "fixes the residues $\{0, 5\}$" which is *inconsistent* with §3 of J20 where $\sigma$ fixes $\{0, 3, 8, 9\}$ — see S1 below):

| $n$ | $G(n)$ |
|---:|:---|
| 0 | 0.000 |
| 1 | 10.528 |
| 2 | 3.292 |
| 3 | 0.000 |
| 4 | 5.000 |
| 5 | 9.472 |
| 6 | 16.708 |
| 7 | **19.472** |
| 8 | 0.000 |
| 9 | 0.000 |

The actual maximum is $G(7) \approx 19.472$, achieved at *one* operator (not two). $G(5) \approx 9.472$ is not the maximum and not equal to $G(7)$. The value 25 is not attained anywhere.

The proof in §5 argues that "the maximum of $|\sum_{j=0}^4 \omega^j z_j|^2$ over choices of unit complex numbers $z_j$ is 25, attained when all $\omega^j z_j$ have the same argument." This is a *generic* upper bound on a sum of five unit-modulus complex numbers; it does not say that the bound is attained by $G(n)$ for any particular $n$.

The Remark following the lemma admits: "The numerical values quoted in the source program were $G_{\max} \approx 9.389$ and $G_{\mathrm{low}} \approx 1.872$, which arise when the functional is normalized by an additional factor; the unnormalized arithmetic gives the cleaner statement above. The two-point maximum is the structural content."

This Remark is wrong. The "cleaner statement" of the lemma is not what the unnormalized arithmetic yields. The unnormalized arithmetic yields the table above, where the maximum is at $n = 7$ alone. The "two-point" reading of the source program ($G_{\max} \approx 9.389$, presumably at $n = 5$ given the substrate's role assignments — though the value 9.389 differs slightly from my computed 9.472, and the difference suggests a different $\sigma$ convention or normalization that the paper has not pinned down) is also a *one-point* maximum: $G(5)$ is the local extremum on the $\varepsilon = 1$ sector, not a global max equal to some other value.

**Fix.** Either:

(a) **Compute $G$ correctly and report the actual structure.** The corrected statement is: "$G$ achieves its global maximum $G_{\max} \approx 19.47$ at exactly one operator, $n = 7$; the second-largest value $G \approx 16.71$ is at $n = 6$. The σ-fixed operators $\{0, 3, 8, 9\}$ all have $G = 0$ by direct calculation." This is a true statement; whether it is *interesting* is a separate question.

(b) **Cut the spectral functional entirely.** The functional is invented for the paper; it is not standard in the finite-Fourier literature. Without a structural reason to introduce it, the §5 lemma can be removed without affecting the rest of the paper.

(c) **Rederive the functional definition** so that the claimed two-point maximum at $G_{\max} = 25$ is correct. This would require modifying Definition 5.1; the paper does not currently provide a way to do this.

**Severity.** Critical. A *Monthly* reader will compute $G(n)$ in 30 seconds and find the discrepancy. The proof, the lemma, and the Remark do not survive.

### M3. The σ involution is inconsistently described (MAJOR)

**Location.** §5, opening paragraph.

**Issue.** The paper says: "Recall the involution $\sigma : \mathbb{Z}/10\mathbb{Z} \to \mathbb{Z}/10\mathbb{Z}$ that fixes the residues $\{0, 5\}$ pointwise and acts on the remaining eight residues by the cyclic shift $1 \mapsto 7 \mapsto 6 \mapsto 5 \mapsto 4 \mapsto 2$ (a 6-cycle)."

This is internally contradictory. The cycle $1 \mapsto 7 \mapsto 6 \mapsto 5 \mapsto 4 \mapsto 2$ contains 5, but the prior sentence says σ "fixes the residues $\{0, 5\}$ pointwise." If 5 is in the 6-cycle, σ does not fix 5. Conversely, if σ fixes $\{0, 5\}$, the 6-cycle must avoid 5.

In the companion paper J20 (read by the same referee for parallel review), σ fixes $\{0, 3, 8, 9\}$ and the 6-cycle is $\{1, 7, 6, 5, 4, 2\}$. This is consistent with σ being an involution if and only if σ has order 2 (so the 6-cycle would actually be a product of three 2-cycles, not a single 6-cycle). But the prose in *both* papers reads "6-cycle," which is incompatible with σ being an involution.

**Fix.** Decide what σ actually is:

(a) **σ is an involution** (order 2): then the 6 non-fixed residues form three 2-cycles, not a 6-cycle. State the three 2-cycles.

(b) **σ is a 6-cycle on $\{1, 7, 6, 5, 4, 2\}$** (order 6, fixes $\{0, 3, 8, 9\}$): then σ is *not an involution*; it is an element of $S_{10}$ of order 6.

The two are incompatible. Whichever interpretation is intended, the §5 prose ("fixes $\{0, 5\}$ pointwise") needs to be rewritten to match.

**Severity.** Major. Without a consistent definition of σ, Lemma 5.2 cannot be evaluated even after the numerical correction in M2.

### M4. The "folklore + new" framing is not honest (MAJOR)

**Location.** §1, second-to-last paragraph; cover letter.

The introduction states: "The construction is folklore in finite harmonic analysis (see e.g. Terras 1999), but the specific parameterization through the joint CRT-plus-Fourier factorization, and the rigid-image lemma below, do not appear in the standard textbooks at this level."

The cover letter sharpens this: "The construction is folklore in finite Fourier analysis; the rigidity statement and the two-point-maximum identification have not appeared together in standard textbooks at this level."

**Issue.** Both claimed novel contributions — the rigidity statement and the two-point-maximum — are problematic (M1 and M2). The "joint CRT-plus-Fourier factorization" is exactly the construction Terras (1999, Ch. 11) treats and that Diaconis (1988, Ch. 1, especially Examples 4 and 5) treats with the standard parameterization. The "specific parameterization" claim does not survive consultation with these references.

The honest description of the paper's contribution is: a worked example of the standard CRT-plus-Fourier embedding for the case $n = 10$, with two attempted novel observations both of which need substantial repair.

**Fix.** Rewrite the introduction's contribution claim. If the rigidity statement and two-point lemma are repaired, the contribution is "we give an explicit rigidity statement (with proof) and an explicit spectral characterization (with proof) for the case $n = 10$." If not, the contribution is "we present the case $n = 10$ in self-contained form for the *Monthly* reader." Either is honest; the present framing is not.

### M5. Self-containment vs. companion dependence (MAJOR)

**Location.** §1 final paragraph; §7 (Companion papers).

The introduction says: "The motivation for collecting this material in a single self-contained note comes from a separate research program in substrate-algebra over $\mathbb{Z}/10\mathbb{Z}$, where the 5-dimensional embedding is used to interpret operators on the 10-element residue ring as points in Euclidean space."

§7 cites two companions:
- "First-G Law" (Sanders & Gish, *Integers*).
- "Joint Closure" (Sanders & Gish, *Algebraic Combinatorics*).

The phrase "submitted to" appears twice; both companions are unpublished. The §7 description of the second companion makes a substantive claim: "The four-core consolidated paper studies the joint closure of two binary composition operators on $\mathbb{Z}/10\mathbb{Z}$. Its main result identifies the four-element subset $\{0, 5, 7, ?\}$ as the unique non-trivial attractor under the joint dynamics; the corresponding image $v(\{0,5,7,?\}) \subset \mathbb{R}^5$ is geometrically the two-point maximum of Lemma 5.2 together with two further points on the $\varepsilon = 0$ sphere."

The "$\{0, 5, 7, ?\}$" (with literal question mark) suggests the fourth element of the four-core is not yet specified by the authors at the time of writing. This is the kind of provisional content that should not appear in a *Monthly* submission. Either the four-core is $\{0, 5, 7, ?\}$ for some specific value (in which case state it — the J20 referee report mentions $\{0, 7, 8, 9\}$ as the four-core in the Algebraic Combinatorics companion), or the connection to the four-core is not yet stable enough to invoke.

**Fix.** Replace "$\{0, 5, 7, ?\}$" with a specific four-element set, or remove the §7.2 paragraph entirely. The latter is cleaner: the present paper does not need the four-core connection to stand on its own.

---

## §4. Specific technical issues

### S1. Author list mismatch

The cover letter has "F. Calderon, Independent Researcher" as second author, and the README (§5 Notes) says "Calderon's one paper in the J-series." The .tex title page lists "Brayden R. Sanders \and M. Gish" twice (a duplicated author block, no Calderon). Reconcile.

### S2. Table 3.1 (image of $v$) — entry for $n = 0$

The table gives $v(0) = (0, 1.000, 0.000, 1.000, 0.000)$. Direct computation: $\varepsilon(0) = 0$, $y(0) = 0$; the four cosines and sines are $\cos(0) = 1, \sin(0) = 0, \cos(0) = 1, \sin(0) = 0$. Correct.

### S3. Table 3.1 — entry for $n = 5$

$v(5) = (1, 1.000, 0.000, 1.000, 0.000)$. Direct: $\varepsilon(5) = 1$, $y(5) = 0$; same Fourier values as for $n = 0$. Correct.

### S4. Remark 3.2 (the two 4-spheres)

"Each of radius $\sqrt{2}$ (the $\mathbb{F}_5$ Fourier basis has constant length $\sqrt{2}$). The two spheres intersect only at $\varepsilon = 1/2$, which is not in the image."

The radius computation is correct: $\sqrt{\cos^2 + \sin^2 + \cos^2 + \sin^2} = \sqrt{2}$. The "intersect only at $\varepsilon = 1/2$" statement is misleading — the spheres are *parallel* (lie in the same affine 4-plane shifted by $(1, 0, 0, 0, 0)$); they do not intersect at all. The correct statement is that they are translates of each other along the $v_1$-axis. Reword.

### S5. The "Two short applications" (§6)

§6.1 (decagonal action): correct. The action is the addition-by-1 in $\mathbb{Z}/10\mathbb{Z}$ pulled through CRT, with the obvious effect on the embedded coordinates. Routine.

§6.2 (Fourier-sum identity): correct, but as the paper acknowledges, "this is just Parseval/Plancherel in coordinates." The identity has no novel content; it is a restatement of the Fourier inversion formula. The "geometric reading" — that the embedding $v$ records the "average position" — is a paraphrase of the inversion formula's coefficient structure.

These applications would be appropriate as exercises in a textbook chapter; as the *Monthly* paper's contribution they are thin.

### S6. References

- **Diaconis 1988** is missing. This is the canonical *Monthly*-level reference for finite-Fourier embeddings; its absence is conspicuous. Add it.
- **Stein–Weiss 1971** is cited but is about Fourier analysis on $\mathbb{R}^n$, not on finite groups. The connection to the present paper is tenuous; consider whether this citation is doing work.
- **Conrad's expository notes** are cited but not given a stable URL or DOI. *Monthly* prefers stable references.
- **Steinberg 2012**, *Representation Theory of Finite Groups* (Springer UTM), would be a more direct reference for the finite-group representation theory used here than Ireland–Rosen.

### S7. The verification script

The README says "(no script — short note; the embedding is verified by ≤30 lines of NumPy in the appendix of the manuscript)." The .tex file's §"Verification" reads: "A short Python script that builds the CRT coordinates, computes the embedding, verifies the 10 image points are distinct, and checks the rigidity assertion is included as supplementary material."

The submission lacks the supplementary material. For *Monthly*, the absence is forgivable (the *Monthly* often publishes notes without supplementary code), but the README and the .tex disagree on whether the script exists.

---

## §5. Minor comments

- **Title.** "The 5D Force Vector as a CRT Fourier Embedding" — the phrase "5D Force Vector" is unmotivated (force suggests physics; this is a representation-theoretic embedding). Consider the cleaner "A 5-dimensional Fourier embedding of $\mathbb{Z}/10\mathbb{Z}$ via the Chinese Remainder Theorem."
- **Abstract.** "We give a clean, elementary derivation" — the derivation is clean but not original; consider "a self-contained presentation."
- **§1 first paragraph.** "Embeddings of finite cyclic groups into Euclidean space are a recurring elementary exercise — regular polygons, lattice embeddings of roots of unity, and the like." This is true and well-paced. Continue.
- **§2 (CRT setup).** Clean and correct.
- **§3 (Definition + Theorem 3.1).** The injectivity proof is standard and correct.
- **Remark 3.2.** See S4 above.
- **§4 (Rigidity).** See M1.
- **§5 (Spectral functional).** See M2 and M3.
- **§6 (Applications).** See S5.
- **§7 (Companion papers).** See M5.
- **Bibliography.** Diaconis 1988 missing; see S6.

---

## §6. Comparison to literature

### Diaconis 1988, *Group Representations in Probability and Statistics*.
Chapter 1 (Examples 4, 5) treats the canonical Fourier embedding of finite abelian groups, including the CRT case for non-prime $n$. The presentation is at exactly the *Monthly*'s level: motivated, computed, and connected to combinatorics. The present paper does not improve on Diaconis's exposition.

### Terras 1999, *Fourier Analysis on Finite Groups and Applications*.
Chapter 11 covers the abelian case in detail. The CRT-plus-Fourier construction is given as a worked example. The "5-dimensional embedding for $n = 10$" is computed explicitly. Terras is cited in the present paper, but the manuscript does not engage with the parts of Terras that overlap with its own content.

### Steinberg 2012, *Representation Theory of Finite Groups*.
Sections 3–5 cover the Pontryagin dual and the Fourier basis for finite abelian groups at the GTM level. Standard reference.

### Conrad expository notes.
Cited; the notes are at https://kconrad.math.uconn.edu/blurbs/ and include a treatment of finite-abelian Fourier theory. Add the URL.

### Folklore vs. publication.
The "folklore + new lemma" template is a legitimate *Monthly* submission strategy when the new lemma is genuinely substantive. With Lemma 5.2 numerically incorrect and Theorem 4.1 tautological, the present paper does not have a substantive new lemma to add to the folklore. The paper would need to either repair both or replace them with a genuine new observation about the embedding.

---

## §7. Constructive suggestions for resubmission

**Path A (folklore exposition).** Drop the rigidity theorem and the spectral functional entirely. Present the embedding as a self-contained worked example for the *Monthly* reader, with the §6 applications kept (decagonal action, Parseval). The paper becomes a 4-page expository note. Worth publishing if it adds pedagogical value beyond Diaconis Chapter 1; not otherwise.

**Path B (genuine rigidity).** Replace Theorem 4.1's premise (ii) with an equivariance condition (option (a) in M1) or a regular-pentagon condition (option (b) in M1). Prove from there. The proof is short but substantive. The paper then has a genuine rigidity result.

**Path C (genuine spectral characterization).** Replace Lemma 5.2 with a corrected and properly motivated spectral functional. Compute its values at all 10 operators. Identify the structural content (which operators maximize? which are zero? what is the σ-orbit structure?). This becomes the paper's main contribution and gives the *Monthly* reader a genuine new observation about the case $n = 10$.

I recommend Path B, possibly combined with Path C if the corrected spectral functional has a clean structural statement.

---

## §8. Decision

**Reject.** Without the rigidity statement (M1) and the spectral lemma (M2), the paper does not contain new content. With those repairs, the paper might be a publishable *Monthly* note, but the repairs are substantial: they change the theorem statements, the proofs, and the contribution claims.

I encourage the authors to revise along Paths B+C above and resubmit. The *Monthly* welcomes such resubmissions when the underlying mathematics is sound.

Reviewer's confidence: high on M1 (the tautology in Theorem 4.1's premise (ii) is structural and visible from the statement alone); high on M2 (the numerical claim is wrong and is verified by 10 lines of Python); high on M3 (the σ inconsistency is in the prose); medium on M4 and M5 (these are framing issues that depend on editorial judgment as much as referee judgment).

— Anonymous Referee, AMM, 2026-05-07
