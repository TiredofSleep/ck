# Referee Report: J10 / Journal of Number Theory

**Manuscript:** "The Universal Orthogonality Principle: Joint-Map Injectivity as the Sufficiency Criterion for Two-Partition Families on Squarefree $\mathbb{Z}/n\mathbb{Z}$"
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** Journal of Number Theory
**Reviewer:** External referee (anonymous, fresh eyes)
**Date:** 2026-05-07

---

## 1. Summary of the manuscript

For squarefree $n = p_1 \cdots p_k$ ($k \geq 2$), the authors consider pairs of partitions $\{\pi_1,\pi_2\}$ of $\mathbb{Z}/n\mathbb{Z}$ induced by maps $f \colon \mathbb{Z}/n\mathbb{Z}\to A$, $g \colon \mathbb{Z}/n\mathbb{Z}\to B$. They call the pair *sufficient* when $\pi_1 \wedge \pi_2 = \pi_{\mathrm{disc}}$ (the partition into singletons). The "Universal Orthogonality Principle" (Theorem 2.1, henceforth UOP) asserts:

$$\{\pi_1,\pi_2\}\ \text{sufficient}\ \iff\ J = (f,g)\colon \mathbb{Z}/n\mathbb{Z} \to A \times B\ \text{injective}.$$

The bulk of the paper is a uniform derivation of four classical-style "sufficiency" theorems as immediate corollaries of UOP, distinguished only by the algebraic class of the underlying maps $f,g$:

- **Theorem A** ($M{+}M$): $\{\pi_{\mathrm{DYN}}(G),\pi_{\mathrm{DYN}}(H)\}$ sufficient iff $G \cap H = \{1\}$ in $(\mathbb{Z}/n\mathbb{Z})^{\times}$.
- **Theorem B** ($A{+}M$): $\{\pi_d,\pi_{\mathrm{DYN}}(G)\}$ sufficient iff $G$ acts trivially on every prime of $n/d$.
- **Theorem C** (corrected $M{+}A$): same condition as B, by symmetry of joint-map injectivity. An $n=15$ counterexample to a previously-asserted alternative condition is given (Example 4.1).
- **Theorem D** ($A{+}A$, "CRT $k-1$"): $\{\pi_{d_1},\pi_{d_2}\}$ sufficient iff $\mathrm{lcm}(d_1,d_2) = n$.

Two further "structural" results are stated:

- **Theorem 6.1** (Coordinate Coverage, sufficient direction): if $f$ resolves the prime set $D_f$, $g$ resolves $D_g$, and $D_f \cup D_g = \{p_1,\ldots,p_k\}$, then $J$ is injective.
- **Theorem 7.1** (Refinement Trap): a chain of comparable partitions cannot be sufficient unless one element is already $\pi_{\mathrm{disc}}$.

A short Section 8 reduces a "Minimum Viable Jump Number" (MVJN) statement to the same framework, with $\mathrm{MVJN}(\mathbb{Z}/30\mathbb{Z}) = 1$ achieved by $\{\pi_{\mathrm{SPEC}},\pi_{15}\}$ and $\{\pi_{\mathrm{DYN}}(7),\pi_{\mathrm{DYN}}(11)\}$.

I have verified the four numerical/structural claims by independent enumeration:

- $G = \langle 2\rangle = \{1,2,4,8\}$ in $(\mathbb{Z}/15\mathbb{Z})^{\times}$, orbit of $5$ under $T_2$ is $\{5,10\}$, both lie in the $\pi_5$-block $\{0,5,10\}$ — confirmed (Example 4.1).
- $\{\pi_{\mathrm{DYN}}(7),\pi_{\mathrm{DYN}}(11)\}$ on $\mathbb{Z}/30\mathbb{Z}$: $U(\pi_{\mathrm{DYN}}(7)) \cap U(\pi_{\mathrm{DYN}}(11)) = \emptyset$ — confirmed.
- Coordinate orders: $\mathrm{ord}_2(7)=\mathrm{ord}_3(7)=1, \mathrm{ord}_5(7)=4$; $\mathrm{ord}_2(11)=1, \mathrm{ord}_3(11)=2, \mathrm{ord}_5(11)=1$; pairwise gcds all $1$ — confirmed.
- $\{\pi_{\mathrm{SPEC}},\pi_{15}\}$ on $\mathbb{Z}/30\mathbb{Z}$: $U \cap U = \emptyset$ — confirmed.

---

## 2. Decision recommendation

**Reject (without prejudice to a substantially restructured resubmission, possibly to a different venue).**

I have read the paper end-to-end and re-derived its proofs. The mathematical content is correct, but it does not, in my judgment, meet the *Journal of Number Theory* bar for the following three combined reasons.

**(R1) The "principle" is a direct unfolding of the definition of "sufficient pair" and contains no number-theoretic content of its own.** UOP states: $J$ injective iff for every $x \neq y$, $f(x) \neq f(y)$ or $g(x) \neq g(y)$, iff $\{x,y\}$ is not unresolved in both partitions. This is one line. It does not use squarefreeness, finiteness, the ring structure, the abelian group structure, or anything specific to $\mathbb{Z}/n\mathbb{Z}$: it is the *definition* of the meet-of-two-partitions in the partition lattice of any set $X$, recast through the equivalence "partition = fibers of a map." The author is right that "the proof is trivial" (line 78) — but this is fatal, not virtuous, for a theorem advertised as a unifying *principle*.

**(R2) The label "Universal Orthogonality Principle" is misleading in a number-theory journal.** Standard "orthogonality" in number theory refers to character orthogonality (Iwaniec–Kowalski Ch. 3), Plancherel/Parseval for additive or multiplicative characters, large-sieve orthogonality, or trace formulas (Petersson, Bruggeman–Kuznetsov; Iwaniec–Kowalski Ch. 14, 16; Friedlander–Iwaniec). None of these notions appear in the manuscript. The paper's "orthogonal jump" means *partition-lattice incompatibility* (neither partition refines the other), which is a fact about a finite poset, not about Fourier-analytic orthogonality. The naming will mislead JNT readers.

**(R3) The corollaries are old.** Theorem D ($A{+}A$, "$\mathrm{lcm}(d_1,d_2)=n$") is the elementary CRT statement. Theorem A ($M{+}M$) reduces to the structure of $(\mathbb{Z}/n\mathbb{Z})^{\times} \cong \prod_i (\mathbb{Z}/p_i\mathbb{Z})^{\times}$ and asks $\langle G\rangle \cap \langle H\rangle = \{1\}$ — this is a one-line CRT consequence after observing that pairs in a common $G$-orbit and in a common $H$-orbit differ by an element of $\langle G\rangle \cap \langle H\rangle$ acting on a unit. Theorem B ($A{+}M$) requires a slightly more careful CRT-coordinate analysis (the zero-fiber observation also done in the J11 companion), but is still elementary CRT. None of the four corollaries is, taken individually, a recognized published result that the manuscript cites by attribution; the paper presents them as folklore or as "previously stated." If they are folklore, that is fine, but it is then unclear what the *new* contribution is beyond a notational unification.

The paper's actual contribution is plausibly (i) the explicit $n=15$ counterexample (Example 4.1), and (ii) the recognition that a previously-asserted form of the $M{+}A$ condition was incorrect. These are content-rich and deserve to appear in print, but they are the substance of the J11 companion, not of J10.

---

## 3. Major comments

### M1. UOP is the definition of partition-lattice meet, restated.

The argument $\pi_1 \wedge \pi_2 = \pi_{\mathrm{disc}} \iff (f,g)$ injective holds for any partitions of any set $X$ via the canonical map $X \to (X/\pi_1) \times (X/\pi_2)$ (Birkhoff, *Lattice Theory*, 1940; Ore, *Theory of Equivalence Relations*, Duke Math. J. 1942 — both already cited by the author). The squarefree-$\mathbb{Z}/n\mathbb{Z}$ context is irrelevant to the statement of Theorem 2.1; only the corollaries use it.

A reader familiar with partition lattices will not recognize this as a *theorem* worth naming. The phrase "joint-map injectivity = pairwise discrimination" is the fiber-product characterization of the meet, and is treated as a definition or a one-line lemma in any standard treatment (e.g., Grätzer, *General Lattice Theory*, II.§4; Birkhoff, ibid.).

**Recommended action:** Demote Theorem 2.1 to a Lemma or Proposition stated under its standard name (something like "joint-fiber characterization of partition meet") and cite Birkhoff/Ore. Remove the "principle" framing.

### M2. The "different forms" of Theorems A, B, C, D are not unified by UOP — they are unified by CRT.

The genuine unifying observation is: in CRT coordinates, every map $f$ on $\mathbb{Z}/n\mathbb{Z}$ has a *resolving set* of primes $D_f \subseteq \{p_1,\ldots,p_k\}$ (those primes whose coordinate $f$ does not collapse), and $J = (f,g)$ is injective iff $D_f \cup D_g = \{p_1,\ldots,p_k\}$ — this is essentially Theorem 6.1, and is the genuine structural fact in the paper.

In each of the four cases:
- $\pi_d$ resolves precisely $\{p_i : p_i \mid d\}$.
- $\pi_{\mathrm{DYN}}(G)$ resolves precisely the primes $p_i$ at which $G$ acts trivially (otherwise $G$ collapses some unit pair to a common orbit; on the zero-fiber, $G$ also fails to resolve when it acts non-trivially).

The three derivations (A, B, D) reduce to coordinate-set unions. UOP qua Theorem 2.1 is a tautology that doesn't prove anything; what *does* prove the corollaries is the CRT factorization plus the explicit resolving-set computation per partition class.

**Recommended action:** Restructure as: (1) Lemma: meet of two partitions is discrete iff joint map is injective (one line, citing Birkhoff/Ore). (2) Theorem (the actual content): for squarefree $n$, $J = (f,g)$ is injective iff $D_f \cup D_g = \{p_1,\ldots,p_k\}$ where $D_h$ is the resolving prime set of $h$. (3) Compute $D_h$ for residue and dynamical maps, deriving A, B, C, D as corollaries.

This makes the paper's actual content — the CRT prime-resolving set framework — the named contribution, and removes the cosmetic "UOP" wrapper.

### M3. The naming "Universal Orthogonality Principle" is inaccurate.

In a number-theory journal:
- "Orthogonality" means (multiplicative or additive) character orthogonality. The "orthogonality of characters" identity $\frac{1}{\varphi(n)}\sum_{\chi}\chi(a)\overline{\chi(b)} = \mathbf{1}_{a=b\,(\mathrm{units})}$ is the canonical orthogonality fact on $\mathbb{Z}/n\mathbb{Z}$.
- The author's "orthogonal jump" between two partitions means: they are incompatible (neither refines the other). This is a *partition-lattice* concept, not an orthogonality concept; in lattice theory it is usually called *incomparability* or, for refinement-incomparable pairs, simply "incomparable in the refinement order".

A JNT reader scanning the title and abstract will (correctly) expect a Fourier-analytic / character-theoretic statement and will be misled. JNT also publishes lattice/algebraic combinatorics in $\mathbb{Z}/n\mathbb{Z}$, but typically when the result has either character-theoretic or algebraic-number-theoretic significance.

**Recommended action:** Retitle. If the partition-lattice content is preserved, a more appropriate title would be "*Joint-injectivity criteria for partition pairs on squarefree $\mathbb{Z}/n\mathbb{Z}$*" or similar, and the venue should likely be *European Journal of Combinatorics* or *Discrete Mathematics* rather than JNT.

### M4. The novelty claim is not adequately delineated.

The introduction (line 64) refers to "several classical and recent sufficiency theorems for partition pairs on squarefree finite cyclic rings", but no specific paper is cited for any of A, B, C, or D. The references include only generic textbooks (Hardy–Wright, Lang, Ireland–Rosen, Dummit–Foote) and three companion papers from the author's own program. This is unusual for a paper claiming to *unify* prior work.

Specifically:
- Theorem D is the standard $\mathrm{lcm}$ characterization for joint divisibility — folklore.
- Theorem A in the form "intersection of cyclic subgroups of $(\mathbb{Z}/n\mathbb{Z})^{\times}$ is trivial iff coordinate-wise gcds of orders are 1" is implicit in any treatment of $(\mathbb{Z}/n\mathbb{Z})^{\times}$ via CRT (Hardy–Wright §5–6; Ireland–Rosen Ch. 4). I am not aware of a published paper to which it is *attributed*, but if the authors are claiming priority, they should make that claim explicit and survey the prior literature on sufficient-pair classifications.
- Theorem B with the "$G$ trivial on $n/d$" formulation may indeed be new in this exact form. If so, this should be the claimed contribution and stated as such. The introduction should distinguish *what is new* from *what is folklore being repackaged*.

**Recommended action:** A "Prior literature" subsection in §1 clarifying which of A–D are folklore (with attribution), which are new in this exact formulation, and what the genuine contribution of the paper is.

### M5. Theorem 6.1 (coordinate coverage) is the actual structural theorem and deserves promotion.

Theorem 6.1 is the only result in the paper that carries genuine structural content: a clean, named criterion for joint injectivity in terms of resolving prime sets. Its converse fails (Remark 6.2), but the sufficient direction is exactly what makes A, B, D drop out.

The paper would be stronger if Theorem 6.1 were the *main result* of the paper, with A, B, D as immediate corollaries, and UOP recast as a lemma.

**Recommended action:** Restructure with §6 as the heart of the paper. (See M2.)

### M6. The MVJN section is premature.

Section 8 introduces MVJN, proves $\mathrm{MVJN}(\mathbb{Z}/30\mathbb{Z}) = 1$, and conjectures $\mathrm{MVJN}(\mathbb{Z}/n\mathbb{Z}) = 1$ for all squarefree $n \geq 6$. The conjecture is supported only by "the construction $\{\pi_{n/p_1},\pi_{n/p_2}\}$ together with a SPEC-type companion at small $n$" (line 215), which is not proved in general.

This section feels appended; it does not contribute to the UOP narrative and the conjecture is left open. Consider:

- Either remove §8 and submit the MVJN material separately (with at least a partial proof of the conjecture), or
- Promote MVJN to a co-equal theme of the paper and prove the conjecture.

In the current form, §8 reads as a teaser, which is awkward for a JNT submission.

**Recommended action:** Move §8 to the J12 companion (which already discusses MVJN in detail), and tighten this paper around the partition-lattice/coordinate-coverage core.

### M7. The $A+M$ vs. $M+A$ "correction" should be presented as an asymmetry-collapse, not as a "correction".

Theorem 5.1 (Corrected Theorem C) is by definition equivalent to Theorem B (since joint injectivity is symmetric in $f$, $g$), so the "correction" is not a new theorem but the observation that a previously-asserted asymmetric formulation was incorrect. This is content for the J11 companion paper, where it belongs and is treated correctly. In the J10 paper, it is duplicate material.

**Recommended action:** Remove §5 from J10. State Theorem B once, and remark in passing: "By symmetry of joint-map injectivity, the same condition characterizes $\{\pi_{\mathrm{DYN}}(G),\pi_d\}$" — one sentence. The full treatment of the $n=15$ counterexample belongs in J11.

---

## 4. Minor comments

### m1. (Title line 33–35) The title line-break "Joint-Map Injectivity as the Sufficiency Criterion / for Two-Partition Families on Squarefree $\mathbb{Z}/n\mathbb{Z}$" is acceptable, but the use of "Sufficiency Criterion" without qualification will read in JNT as referring to a sufficient condition for some Diophantine or analytic statement. Consider "Pairwise-Sufficient Criterion".

### m2. (Author block lines 36–42) The author block lists Sanders & Gish twice, with two different addresses ("7Site LLC" and "Independent Researcher"). This is a typo; only one author block should appear.

### m3. (Abstract, line 53) "We also prove the *coordinate-coverage characterization*: if two maps together resolve every CRT prime coordinate of $\mathbb{Z}/n\mathbb{Z}$, then $J$ is injective (the converse fails in general)." — should read "(sufficient direction; the converse fails in general)" so readers do not initially mis-parse the assertion.

### m4. (§3, proof of Theorem A, line 112) "$y x^{-1} \in G \cap H$ (for unit $x$)" — but the orbit relation is $y \in Gx$, which means $y = g x$ for some $g \in G$, hence $g = y x^{-1}$ requires $x$ a unit. The proof handles only the unit case. The non-unit case (zero-fiber) requires a separate CRT-coordinate argument. The current proof is incomplete; the paper should either:
- restrict to $x$ unit and supply a parallel zero-fiber argument (as the J11 companion does for the $A+M$ case), or
- give a CRT-coordinate proof from the start (analogous to the proof of Theorem B at line 122).

This is the same gap the author identifies in the "prior" $M+A$ condition; it appears here in $M+M$ and should be addressed analogously.

### m5. (§5, Theorem C as corollary) Line 140: "Joint-map injectivity is symmetric in the pair, so Theorem 5.1 is Theorem 4.1 with the roles of $f$ and $g$ exchanged." — this is correct, but Theorem 5.1 is then *not* a separate theorem, it is the same theorem stated twice. Either remove it or label it explicitly as Corollary B.1.

### m6. (§7, Theorem 7.1, refinement trap proof) The proof at line 186 says "The general case for arbitrary partition chains follows by replacing the divisor labels with the partition's coordinate support (Definition 7.2); the conclusion is identical." — but Definition 7.2 ($\mathrm{supp}(\pi)$) is stated *after* the proof. Restructure so the definition precedes its use.

### m7. (§7, Definition 7.2) "$\mathrm{supp}(\pi) = \{i : \pi$ resolves $p_i\}$" — but "resolves" is defined only for *maps* (Definition 6.1), not partitions. Either lift the definition to partitions (a partition resolves $p_i$ iff its quotient map does), or restate.

### m8. (§8, Theorem 8.2 / MVJN) "$\mathrm{MVJN}(\mathbb{Z}/n\mathbb{Z}) \geq 1$ for every squarefree $n$ with $k \geq 2$" — this is the refinement trap (Theorem 7.1). The proof sketch in line 207 is correct but should reference Theorem 7.1 explicitly rather than re-stating "the lower bound is the refinement trap."

### m9. (§9 open questions, item (a)) "For $n$ with repeated prime factors, the CRT structure is replaced by $p$-adic components and UOP still holds abstractly" — UOP is, as I noted in M1, true for any partitions of any set; it has nothing to do with $p$-adic analysis. This sentence should be removed or rephrased.

### m10. (References) The bibliography contains five "submitted to" entries from the author program. JNT typically requires arXiv IDs, DOIs, or "in preparation" markers. The companion paper to JNT is itself in submission; cross-citation in this state is acceptable but the authors should ensure the J10/J11 pair is internally consistent (which it is — Example 4.1 is identical in both).

### m11. (References) The author cites "Sanders–Gish, *First-G Law*" and "Sanders–Mayes, *Crossing Lemma*" as predecessors. These have no apparent relevance to the partition-lattice content of the present paper (the abstract and introduction make no use of either). Consider removing these two citations to tighten the bibliography around the actual content.

---

## 5. Specific verifications performed

I have independently verified the following:

1. $G = \langle 2 \rangle = \{1,2,4,8\}$ in $(\mathbb{Z}/15\mathbb{Z})^{\times}$, $\varphi: G \to (\mathbb{Z}/5\mathbb{Z})^{\times}$ is a bijection $1\mapsto1, 2\mapsto2, 4\mapsto4, 8\mapsto3$. Confirmed.
2. Orbit of $5$ under $T_2$ in $\mathbb{Z}/15\mathbb{Z}$ is $\{5,10\}$; both lie in the $\pi_5$-block $\{0,5,10\}$. Confirmed.
3. The full conflict set of $T_G$ on $\pi_5$ is $\{(5,10,8),(5,10,2),(10,5,8),(10,5,2)\}$ — i.e., the single unordered pair $\{5,10\}$ is unresolved by $\pi_5$ and lies in a single $G$-orbit, exactly as Example 4.1 claims.
4. For the $\mathbb{Z}/30\mathbb{Z}$ case: $\mathrm{ord}_2(7)=\mathrm{ord}_3(7)=1$, $\mathrm{ord}_5(7)=4$; $\mathrm{ord}_2(11)=\mathrm{ord}_5(11)=1$, $\mathrm{ord}_3(11)=2$. Coordinate-wise gcds are all 1; $\langle 7\rangle \cap \langle 11\rangle = \{1\}$. Confirmed.
5. $U(\pi_{\mathrm{DYN}}(7)) \cap U(\pi_{\mathrm{DYN}}(11))$ on $\mathbb{Z}/30\mathbb{Z}$: empty. Confirmed.
6. $U(\pi_{\mathrm{SPEC}}) \cap U(\pi_{15})$ on $\mathbb{Z}/30\mathbb{Z}$: empty. Confirmed.
7. The proof of Theorem A (line 112) handles only the unit case; I checked the zero-fiber case for $G = \langle 2\rangle$, $H = \langle 4\rangle$ on $\mathbb{Z}/15\mathbb{Z}$, where $G \cap H = \langle 4\rangle = \{1,4\} \neq \{1\}$, and indeed $\{0\}$ is fixed by both, so no conflict from $0$; the conflict $\{1,4\}$ is in $G$-orbit of $1$ and in $H$-orbit of $1$, confirming Theorem A's necessity. So the *statement* is correct; only the *written proof* is incomplete.

---

## 6. Question to the authors

### Q1. What is the new content that distinguishes this paper from the J11 companion?

J11 contains:
- The $n=15$ counterexample to a "prior" $M+A$ condition (Example 2.1 of J11 = Example 4.1 of J10).
- The corrected Theorem C, with full CRT-coordinate proof (Theorem 3.1 of J11).
- The zero-fiber analysis (Proposition 4.1 of J11).
- Verification that prior applications survive (§5 of J11).

J10 contains:
- The same $n=15$ counterexample.
- A re-derivation of Theorem C from "UOP".
- Theorems A, B, D as additional corollaries.
- The coordinate coverage theorem and refinement trap.

If J10 is the lead, then its distinguishing content is (i) Theorem A, (ii) Theorem D (which is folklore CRT), (iii) the coordinate-coverage and refinement-trap structural results. Of these, only (iii) seems publication-worthy.

### Q2. What number-theoretic application does the paper enable?

A JNT submission is strengthened by an *application* (to character sums, sieve methods, $L$-functions, equidistribution, etc.) that the unified framework makes possible. The paper currently has no such application: every corollary reduces to a CRT computation that could have been done directly without reference to UOP. Is there a number-theoretic problem (Dirichlet density of certain residue patterns, joint distribution of arithmetic functions, etc.) that the framework genuinely simplifies?

### Q3. What is the relationship to prior literature on partition-pair sufficiency?

The introduction (line 64) refers to "several classical and recent sufficiency theorems" but cites no published source for any of them. Are A, B, C, D in any prior published paper? If yes, who are the predecessors? If no, then the corollaries A, B, C, D are *new* (or folklore not previously written down), and the paper's framing as a "unification" of prior work is misleading.

### Q4. Why is the convention "orthogonal jump" used for partition incomparability?

In partition lattice literature, two partitions are typically called *incomparable in the refinement order* (Birkhoff, Grätzer) or *transverse* (Tutte, in matroid contexts). "Orthogonal" already has a specific meaning in number theory (character orthogonality). Adopting "orthogonal" for a different concept will cause confusion.

---

## 7. Originality and significance for JNT

### Originality.

The paper's claimed contribution is "the unification of two-partition sufficiency theorems under a single criterion". This unification is real but is a tautology (M1, M2). The two genuinely structural results — Theorem 6.1 (coordinate coverage, sufficient direction) and Theorem 7.1 (refinement trap) — are interesting but elementary, and would fit naturally in a *combinatorics of $\mathbb{Z}/n\mathbb{Z}$* paper rather than a number theory paper.

The $n=15$ counterexample (Example 4.1) is genuinely useful but belongs to J11.

### Significance for JNT.

JNT publishes work on:
- $L$-functions, modular forms, character sums (analytic NT).
- Diophantine equations, heights, arithmetic geometry (algebraic NT).
- Sieve methods, additive combinatorics, equidistribution (combinatorial NT).
- Computational and explicit number theory.

The present paper's content does not engage with any of these areas. The closest fit would be sieve / equidistribution if the author could demonstrate that the framework has consequences for arithmetic functions or Dirichlet density problems. The current manuscript does not establish such a connection.

I would more naturally route this work to:
- **European Journal of Combinatorics** for the partition-lattice content (this is the venue of the J12 companion, where the content fits well).
- **Discrete Mathematics** or **Order** for the lattice-theoretic content (refinement trap, coordinate coverage).
- A short note in **American Mathematical Monthly** for the $n=15$ counterexample (which is genuinely surprising at the level of an undergraduate exercise).

For JNT specifically, the bar is not met absent a substantive number-theoretic application.

---

## 8. Reproducibility

There are no computational claims in the paper that require code; all numerics ($n=15$, $n=30$) are checkable by hand or by trivial computer enumeration, and I have independently verified each claim made in the text. The proofs are self-contained.

The companion citations (J11, J12, "First-G Law", "Crossing Lemma", "Flatness Theorem") create a cluster of submissions that may be hard for a JNT editor to review independently; the author should ensure J10 stands alone or clearly identify which companion claims are needed.

---

## 9. Final remarks

The mathematics is correct. The exposition is clear. The author has identified a genuine error in a prior formulation of the $M+A$ condition (the J11 content) and has framed a clean unifying observation (the J10 content). The technical execution is competent.

However, the paper as written:
- Names a tautology a "principle" (R1, M1).
- Uses a misleading title in a venue where "orthogonality" has a specific meaning (R2, M3).
- Repackages folklore corollaries as a "unification" without citing the prior literature (R3, M4, Q3).
- Duplicates content with the J11 companion (M7).
- Has no number-theoretic application (Q2).

A revised paper, restructured around Theorem 6.1 (coordinate coverage) as the main result with the partition-lattice corollaries derived from it, and submitted to a combinatorics venue such as *European Journal of Combinatorics* or *Discrete Mathematics*, would be a reasonable single-paper presentation of the content currently spread across J10/J11/J12.

For *Journal of Number Theory*, my recommendation is **Reject**.

---

**Estimated revision effort if pursued:** 30+ person-hours, including (i) substantial restructuring around Theorem 6.1, (ii) a literature survey of partition-lattice sufficiency results, (iii) the addition of a number-theoretic application, (iv) consolidation with the J11 content. The simpler path is a venue change.

**Reviewer's confidence:** High. I have read the paper end-to-end, re-derived each proof, and independently verified all numerical claims. My disagreement is with the framing and venue, not with the mathematics.
