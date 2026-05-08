# Referee Report: J11 / Journal of Number Theory (Companion Submission)

**Manuscript:** "Corrected Theorem C: $M{+}A$ Sufficiency on Squarefree $\mathbb{Z}/n\mathbb{Z}$ via Zero-Fiber Analysis"
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** Journal of Number Theory (companion to J10/UOP)
**Reviewer:** External referee (anonymous, fresh eyes)
**Date:** 2026-05-07

---

## 1. Summary of the manuscript

For squarefree $n = p_1 \cdots p_k$ ($k \geq 2$), $G \leq (\mathbb{Z}/n\mathbb{Z})^{\times}$, and a divisor $d \mid n$, the authors consider the partition pair $\{\pi_{\mathrm{DYN}}(G), \pi_d\}$ — the multiplicative orbit partition under $G$, paired with the additive residue partition mod $d$. The pair is *sufficient* when $U(\pi_{\mathrm{DYN}}(G)) \cap U(\pi_d) = \emptyset$, where $U(\pi)$ denotes the unresolved-pair set.

The paper makes three contributions:

**(C1) An explicit counterexample.** A previously-asserted criterion claimed: $\{\pi_{\mathrm{DYN}}(G),\pi_d\}$ is sufficient iff $\varphi: G \to (\mathbb{Z}/d\mathbb{Z})^{\times}$, $g \mapsto g \bmod d$, is injective. The authors give the counterexample $n = 15$, $G = \langle 2\rangle = \{1,2,4,8\}$, $d = 5$: $\varphi$ is a bijection $G \to (\mathbb{Z}/5\mathbb{Z})^{\times}$, but the pair $\{5,10\}$ in the orbit of $5$ under $T_2$ has both elements $\equiv 0 \pmod 5$, hence is unresolved by both partitions.

**(C2) Identification of the gap.** The "unit-only" argument (sketched in §1.2) only handles unit elements $x \in (\mathbb{Z}/n\mathbb{Z})^{\times}$. The zero-fiber elements $F_d = \{x : x \equiv 0 \pmod d\}$ are not addressed; on $F_d$, $G$ may act non-trivially via its components at primes $p_j \mid n/d$, generating conflicts even when $\varphi$ is injective.

**(C3) The corrected theorem.** Theorem 3.1: $\{\pi_{\mathrm{DYN}}(G),\pi_d\}$ is sufficient iff $G$ acts trivially on every prime $p_j \mid n/d$, equivalently every $g \in G$ satisfies $g \equiv 1 \pmod{p_j}$ for every $p_j \mid n/d$.

A proof is given by two routes: a one-line reduction via the joint-injectivity criterion of the J10 companion (Universal Orthogonality Principle), and a direct CRT-coordinate argument. A Proposition on the action of $G$ on $F_d$ is given (Prop. 4.1), and verification examples (SPEC + half-modulus on $n = 2m$, the unaffected $M+M$ and $A+A$ cases) appear in §5.

I have verified each numerical claim by independent enumeration:
- $G = \langle 2\rangle = \{1,2,4,8\}$ in $(\mathbb{Z}/15\mathbb{Z})^{\times}$, $\varphi(g) \in (\mathbb{Z}/5\mathbb{Z})^{\times}$: bijection $(1,2,4,8) \mapsto (1,2,4,3)$. Confirmed.
- Orbit of $5$ under $T_2$ in $\mathbb{Z}/15\mathbb{Z}$ is $\{5,10\}$. Confirmed.
- Both $5,10 \equiv 0 \pmod 5$, so both lie in the same $\pi_5$-block, while differing under $T_2$. Confirmed.
- The conflict $\{5,10\}$ is the unique nontrivial pair in $U(\pi_{\mathrm{DYN}}(\langle 2\rangle)) \cap U(\pi_5)$. Confirmed.

---

## 2. Decision recommendation

**Major revisions** (close to "Accept with minor revisions" — the result is correct, the counterexample is honest and important, and the corrected theorem is well-stated; but the paper has a substantial dependency on the J10 companion and several presentational issues that should be addressed before camera-ready).

The mathematical content is correct. The $n=15$ counterexample is real and surprising; the corrected theorem is a clean and useful statement. The CRT-coordinate proof in §3 is independent of the J10 companion and is internally complete. The zero-fiber analysis (§4) is the structural insight that explains why the prior unit-only argument is incomplete.

The submission is, in my view, a more substantive contribution than its lead companion (J10) and could plausibly stand alone in JNT *if* the dependence on J10 is removed or made explicit, the prior-literature gap is filled, and several exposition issues are addressed.

---

## 3. Major comments

### M1. The "previously stated condition" needs a citation.

§1.1 says: "A previously-stated condition asserted: $\{\pi_{\mathrm{DYN}}(G),\pi_d\}$ is sufficient iff the natural map $\varphi: G \to (\mathbb{Z}/d\mathbb{Z})^{\times}$ is injective." (line 59)

This is the central claim being corrected. Where does this previous condition appear in the literature? The bibliography contains only generic textbooks (Lang, Ireland–Rosen, Dummit–Foote, Hardy–Wright) and two papers from the author's own program (UOP companion, Crossing Lemma).

A JNT referee will (and should) ask: who asserted this prior condition? If it is folklore from a graduate textbook, the textbook should be cited and the page/exercise number given. If it is from a published paper, that paper should be cited. If it is an *un*published claim from the author's own prior work program, that should be stated frankly:

> "An earlier formulation in the author program (see e.g. [reference], unpublished notes) asserted ..."

Without an attributable source for the "prior condition", the paper risks reading as a self-correction of an internal mistake, which is acceptable in a self-critical preprint or correction-note but is unusual for JNT as a primary contribution. Either:
- Cite the prior literature where the condition $\varphi$-injective was asserted; or
- Reframe the paper as: "The natural conjecture $\varphi$ injective is incorrect; here is the corrected condition", with the prior conjecture stated as a *natural* one rather than a *previously-stated* one.

**Recommended action:** Insert a citation at line 59. If no published predecessor exists, restate as "the natural conjecture" and explain why a reader might initially expect it.

### M2. The dependence on the J10 companion is uneven and needs clarification.

The proof of Theorem 3.1 begins (line 98): "By the Universal Orthogonality Principle of the companion paper..." and continues with a one-line symmetry reduction, *then* gives a "direct argument by CRT" that is in fact a complete and self-contained proof.

If the direct CRT argument is given, the appeal to the UOP companion is not needed. A cleaner structure would be:

**Option A (independent paper):** Present only the direct CRT argument in §3, and remove the UOP appeal entirely. This makes J11 a standalone JNT submission. The companion can still be cited for related context, but the paper does not depend on it.

**Option B (genuine companion):** Retain the UOP appeal, remove the direct CRT proof, and trim §3 to one paragraph. This makes J11 a short note that is genuinely a companion to J10.

The current hybrid (both appeals in the same proof) is awkward and makes both proofs feel diminished. I recommend Option A: as I noted in the J10 referee report, the UOP "principle" is a partition-lattice tautology, and J11 reads more cleanly when freed of its dependence.

**Recommended action:** Choose Option A or Option B; I lean strongly toward A.

### M3. The corrected Theorem C is a *symmetrized* form, not a fundamentally new theorem.

The structural observation that drives the correction is: *the pair $\{\pi_{\mathrm{DYN}}(G),\pi_d\}$ is symmetric*, so its sufficiency condition cannot depend asymmetrically on the partition class. Once one observes that the established $A+M$ condition (which the paper attributes to "the established $A+M$ classification" at line 98 but does not cite) is "$G$ trivial on primes of $n/d$", and that $A+M$ and $M+A$ are the same pair, the corrected condition is forced.

This is a real insight, but it is not the kind of theorem that requires the full apparatus of §3–§4. A clean presentation would:

1. State the established $A+M$ condition (with citation).
2. Observe that the pair is symmetric, so the same condition characterizes $M+A$.
3. Give the $n=15$ counterexample to the asymmetric "$\varphi$ injective" claim.
4. Optionally add the zero-fiber analysis as a structural commentary.

This is a 4-page paper. The current 6-page treatment is somewhat padded. (See §6 "Discussion" — the two-line "what remains classically true" remark, and the verification examples in §5, could be condensed.)

**Recommended action:** Condense to a Mathematical Note format. JNT does publish short notes; a 4–5 page version of this paper could be a strong contribution if the prior literature is cited (M1).

### M4. The zero-fiber analysis (§4) is the genuine structural content and should be promoted.

Proposition 4.1 ("Action of $G$ on the zero-fiber") is the only structural result in the paper that goes beyond restating the corrected theorem in different forms:

- (a) $G$ preserves $F_d$ setwise.
- (b) Every $G$-orbit on $F_d$ lies in one $\pi_d$-block (the zero-block).
- (c) Conflicts on $F_d$ exist iff $G$ acts non-trivially on $n/d$.

This is the structural "why" of the correction. It deserves to be more prominent in the paper. Currently it appears in §4 as auxiliary material; consider moving it earlier (perhaps to §1.4 as a structural lemma motivating the correction) and giving it more emphasis.

The bijection $F_d \to \prod_{p_j \mid n/d} \mathbb{Z}/p_j\mathbb{Z}$ (line 129) is the key structural fact: $F_d$ is, as a $G$-set, isomorphic to $\mathbb{Z}/(n/d)\mathbb{Z}$, with $G$ acting through its projection to $(\mathbb{Z}/(n/d)\mathbb{Z})^{\times}$. So the zero-fiber question is itself a "smaller" version of the original question: when does $G$ act fixed-point-freely on $\mathbb{Z}/(n/d)\mathbb{Z} \setminus \{0\}$? And the answer (which the paper does not state explicitly): never, unless $G$ is trivial on $n/d$.

**Recommended action:** Promote Proposition 4.1 to a named structural lemma, articulate the recursive structure (the zero-fiber is a smaller copy of the same problem), and use this to motivate the correction.

### M5. Section 5 verification examples are valuable but underexplored.

§5 verifies that the corrected condition is satisfied for two natural classes:
- $G = \{1,-1\}$, $d = m$ on $n = 2m$ (the SPEC + half-modulus case).
- $M+M$ pairs (unaffected by the correction).
- $A+A$ pairs (unaffected).

These verifications are correct and reassuring. But §5 misses an important class of examples: applications where the prior condition was *applied* and the corrected condition makes a *different* prediction.

For instance: what about $n = 30$, $G = \langle 7\rangle = \{1,7,19,13\}$, $d = 5$? The map $\varphi: G \to (\mathbb{Z}/5\mathbb{Z})^{\times}$ sends $1\to1, 7\to 2, 13\to 3, 19\to 4$ — a bijection (so $\varphi$ injective). The corrected condition asks whether $G$ is trivial on $n/d = 6 = 2\cdot3$: $7 \equiv 1 \pmod 2$, $7 \equiv 1 \pmod 3$, so $7 \equiv 1$ at both. The corrected condition is satisfied. *Both* conditions agree here.

A more illustrative example: $n = 30$, $G = \langle 11\rangle = \{1,11\}$, $d = 5$. $11 \equiv 1 \pmod 5$, so $\varphi(11) = 1 = \varphi(1)$ — $\varphi$ is *not* injective. The prior condition correctly predicts non-sufficiency. (Direct check: orbit of $5$ under $T_{11}$ is $\{5, 25\}$, both $\equiv 0 \pmod 5$ — conflict.) Both conditions agree on non-sufficiency.

Where do the conditions *disagree*? Precisely the $n=15$ counterexample: $\varphi$ is injective but the corrected condition fails. Are there others? The smallest example is the one given. Are there *families* of such disagreements?

**Recommended action:** Add a §5 example or §6 remark identifying *families* (parametric in $n$) where the conditions disagree, illustrating that the gap is not pathological but generic. For instance: $n = 3p$ for primes $p \equiv 1 \pmod 3$, $G$ a subgroup of $(\mathbb{Z}/3p\mathbb{Z})^{\times}$ that is non-trivial mod 3 but injective into $(\mathbb{Z}/p\mathbb{Z})^{\times}$, $d = p$.

### M6. The "established $A+M$ classification" needs a citation or proof.

Line 98: "By the established $A+M$ classification (Theorem B of the companion), $J'$ is injective iff $G$ acts trivially on every prime of $n/d$."

If this is from the J10 companion (Theorem B), then the J11 reader needs J10 in hand to verify the proof. As I noted in the J10 report, Theorem B's proof in J10 is correct but the paper itself contains a duplicate of the J11 material. The dependency is bidirectional and somewhat tangled.

If the J11 paper is to stand alone (Option A in M2), then Theorem B should be either re-proved here (a few lines, since it has a clean direct CRT-coordinate proof) or cited from a third-party source. A brief stand-alone proof of "Theorem B" would make J11 self-contained.

**Recommended action:** Either prove Theorem B inline in J11 (a 6-line CRT argument), or cite the J10 companion *after* J10 has been formally accepted. Reciprocal citations between in-submission papers are awkward.

### M7. The opening "unit-only argument" in §1.2 is presented as if it were a complete proof.

Lines 64–67 of §1.2 give a derivation of "$\varphi$ injective" as the sufficient condition, *as if* this were the prior proof. The argument is correct on the unit-fiber but, as the paper itself shows, is incomplete. The presentation could be sharper:

> "**The unit-only argument (incomplete).** For a unit $x \in (\mathbb{Z}/n\mathbb{Z})^{\times}$ ..."

The label "incomplete" or "partial" makes clear from the start that this is a flawed argument being analyzed, not a derivation being asserted.

**Recommended action:** Add a parenthetical "(incomplete; see §1.3)" to the §1.2 heading.

---

## 4. Minor comments

### m1. (Title line 27–28) "$M+A$ Sufficiency on Squarefree $\mathbb{Z}/n\mathbb{Z}$ via Zero-Fiber Analysis" — clear and accurate. The "Corrected Theorem C" prefix is a self-reference to the author program; consider just "$M+A$ Sufficiency on Squarefree $\mathbb{Z}/n\mathbb{Z}$" to make the paper standalone.

### m2. (Author block lines 30–35) Sanders & Gish are listed twice with two different addresses. Same issue as J10; remove the duplicate.

### m3. (Abstract, line 42) "We give the explicit counterexample $n = 15$..." — the abstract correctly states the counterexample and the corrected condition. Good.

### m4. (Abstract, line 42) "...and that prior specific applications --- in particular the SPEC + half-modulus pair on $n = 2m$ for $m$ odd squarefree --- continue to satisfy the corrected condition." — this is the only "prior application" verified in the paper. The phrase "prior specific applications" implies more than one; either name them or singularize.

### m5. (§1.2 line 67) "Since $x$ is a unit modulo $d$, $d \mid (g-1)x$ iff $d \mid g - 1$" — correct but worth noting why $x$ being a unit modulo $n$ implies $x$ a unit modulo $d$ (via the surjection $\mathbb{Z}/n\mathbb{Z} \to \mathbb{Z}/d\mathbb{Z}$).

### m6. (§2 Example 2.1) The CRT decomposition $5 = (2,0)$ in $\mathbb{Z}/3\mathbb{Z} \times \mathbb{Z}/5\mathbb{Z}$: $5 \bmod 3 = 2$, $5 \bmod 5 = 0$. Confirmed. $g = 2 = (2,2)$: $2 \bmod 3 = 2, 2 \bmod 5 = 2$. Confirmed. $g \cdot 5 = (4,0) \bmod (3,5) = (1,0) = 10$. Confirmed.

### m7. (§3, Theorem 3.1, statement line 94) "...iff $G$ acts trivially on every prime of $n/d$, i.e. every $g \in G$ satisfies $g \equiv 1 \pmod{p_j}$ for every $p_j \mid n/d$." — clear. The phrase "acts trivially on every prime" is a slight abuse (one says "acts trivially at every prime" or "is trivial at every prime"). Consider adjusting.

### m8. (§3 proof line 102) "Take any $g \in G$ with $g \neq 1$ and any $x \in \mathbb{Z}/n\mathbb{Z}$." — the proof needs $g \cdot x \neq x$ for the pair to be in $U(\pi_{\mathrm{DYN}}(G))$; this is implicit but should be noted.

### m9. (§3 proof, "Case 1" and "Case 2", lines 104–108) The case split is on whether some $p_i \mid d$ has $g_i \neq 1$ and $x_i \neq 0$. What if $g_i = 1$ for *all* $p_i \mid d$? Then $g \cdot x \equiv x \pmod d$ trivially, but this is a unit-pair conflict only if $g \neq 1$, which forces $g$ non-trivial on some prime, which by hypothesis is in $n/d$ — and the hypothesis says that doesn't happen. So this case doesn't arise; but the proof should note that "$g_i = 1$ for all $p_i \mid d$ and $g \neq 1$" implies $g$ non-trivial on some $p_j \mid n/d$, contradicting the hypothesis.

Actually the proof handles this: if $g \neq 1$, then $g_i \neq 1$ for some $i$. By hypothesis, all primes of $n/d$ are trivial, so this $i$ must be in $d$. Then proceed to Case 1 or Case 2. The proof is correct but the case structure could be made clearer.

### m10. (§4 Proposition 4.1(c)) "Conflicts on $F_d$ exist iff some $G$-orbit on $F_d$ has size $\geq 2$, iff $G$ acts non-trivially on $n/d$." — this is the structural insight. State it more emphatically: this *is* the corrected condition, restated as an action condition on $F_d$.

### m11. (§5, Example "SPEC + half-modulus") "$T_{-1}(m) = -m \equiv 2m - m = m \pmod{2m}$" — should be "$\equiv -m \pmod{2m} \equiv m \pmod{2m}$" since $-m + 2m = m$. The arithmetic is correct; just clarify.

### m12. (§6.1 "Symmetry of the joint-map criterion") This subsection is one paragraph and somewhat repetitive. Consider folding into the introduction.

### m13. (§6.2 line 162) "(forcing $p_j = 2$)" — clear note that $-1 \equiv 1 \pmod{p_j}$ requires $p_j = 2$.

### m14. (§7 open questions) Item (a) is well-posed and concrete. Item (b) on non-squarefree $n$ is interesting but vague — what specifically is open? Restate.

### m15. (References) Bibliography contains 6 entries; only Lang, Ireland–Rosen, Dummit–Foote, Hardy–Wright are textbook references, and the remaining two are author-program companions (UOP, Crossing Lemma). The Crossing Lemma citation (line 205) has no relevance to the present paper that I can detect; consider removing.

---

## 5. Specific verifications performed

I have independently verified:

1. $G = \langle 2\rangle = \{1,2,4,8\}$ in $(\mathbb{Z}/15\mathbb{Z})^{\times}$, with $\mathrm{ord}_{15}(2) = 4$. Confirmed.
2. $\varphi: G \to (\mathbb{Z}/5\mathbb{Z})^{\times}$ is a bijection: $1\to1, 2\to2, 4\to 4, 8\to 3$. Confirmed.
3. $T_2(5) = 10$, $T_2(10) = 20 \equiv 5 \pmod{15}$, so the orbit of $5$ is $\{5,10\}$. Confirmed.
4. Both $5,10 \equiv 0 \pmod 5$. Confirmed.
5. $\{5,10\} \in U(\pi_{\mathrm{DYN}}(G)) \cap U(\pi_5)$, so the pair is *not* sufficient — confirmed by direct enumeration.
6. CRT decomposition $5 = (2 \bmod 3, 0 \bmod 5)$, $g = 2 = (2,2)$, $g\cdot 5 = (4 \bmod 3, 0) = (1,0) = 10$. Confirmed.
7. Proposition 4.1(a): $G$ preserves $F_5 = \{0,5,10\}$. Direct check: $T_g(0) = 0$, $T_g(5) \in \{5,10\}$, $T_g(10) \in \{5,10\}$ for all $g \in G$. Confirmed.
8. Proposition 4.1(c): $G$ has non-trivial action on $n/d = 3$ (since $2 \not\equiv 1 \pmod 3$), hence has size-$\geq 2$ orbit on $F_5$ — namely $\{5,10\}$. Confirmed.
9. The corrected condition: $G = \langle 2\rangle$ trivial on $n/d = 3$? Since $2 \not\equiv 1 \pmod 3$, no. Corrected condition correctly predicts non-sufficiency.
10. Direct verification: for $n = 30$, $G = \langle 11\rangle$, $d = 5$: $11 \equiv 1 \pmod 5$, so $\varphi(11) = 1 = \varphi(1)$, $\varphi$ not injective. Both conditions correctly predict non-sufficiency.

---

## 6. Question to the authors

### Q1. Where in the literature was the prior $\varphi$-injective condition asserted?

The paper repeatedly refers to "the previously-stated condition" but cites no source. If this is from a specific published paper or textbook exercise, please cite it. If it is from an earlier draft of the author program (e.g., an unpublished preprint or workshop talk), state this clearly and consider whether a paper exists for citation.

### Q2. Is the corrected condition optimal in some classification sense?

Theorem 3.1 says: $\{\pi_{\mathrm{DYN}}(G),\pi_d\}$ sufficient iff $G \subseteq \ker(\Phi)$ where $\Phi: (\mathbb{Z}/n\mathbb{Z})^{\times} \to \prod_{p_j \mid n/d} (\mathbb{Z}/p_j\mathbb{Z})^{\times}$ is the natural projection.

So the *largest* admissible $G$ for fixed $d$ is exactly $\ker \Phi$ — this is a specific subgroup of $(\mathbb{Z}/n\mathbb{Z})^{\times}$ of order $\prod_{p_i \mid d}(p_i - 1)$, namely the "kernel at $n/d$".

This is a clean classification. State it explicitly: "The set of admissible $G$ is precisely the lattice of subgroups of $\ker \Phi$, a subgroup of $(\mathbb{Z}/n\mathbb{Z})^{\times}$ of order $\prod_{p_i \mid d}(p_i - 1)$."

### Q3. Does the zero-fiber argument extend to non-squarefree $n$?

The key step in the zero-fiber argument (Proposition 4.1(a)) is: $g_i$ a unit mod $p_i$, so $g_i \cdot 0 = 0$. This holds for $g \in (\mathbb{Z}/n\mathbb{Z})^{\times}$ even when $n$ has prime-power factors, because each $g_i$ is a unit at every prime. So the proposition extends. What is the obstruction to extending Theorem 3.1 to non-squarefree $n$?

The obstruction is, I believe: at a prime power $p^e$, "$G$ trivial on $p$" in the squarefree sense becomes "$G$ trivial on the residue mod $p^e$" or some weaker condition; the precise statement requires $p$-adic analysis. State this explicitly.

### Q4. Are there other "natural" sufficient-pair conditions that are similarly incorrect?

The unit-only argument is a natural mistake — one might equally make the analogous mistake for $A+M$ pairs, $M+M$ pairs, etc., by ignoring the zero-fiber. The paper observes (§5) that $M+M$ and $A+A$ are unaffected. Why? In $M+M$, the zero-fiber consists of $\{0\}$ alone (under the action of $\Z_{n}^{\times}$), and this is a fixed point. In $A+A$, the zero-fibers are nested but the meet condition is still $\mathrm{lcm} = n$. So the $M+A$ correction is specific to the asymmetry between multiplicative (orbit-action) and additive (residue) partitions. Worth a remark.

---

## 7. Originality and significance for JNT

### Originality.

The $n = 15$ counterexample is genuinely surprising at the level of advanced undergraduate algebra. The corrected condition, while symmetrizable from the (presumably folklore) $A+M$ result, gains structural force from the zero-fiber analysis. The paper has real content: an error has been identified and corrected, with a clean structural explanation.

### Significance for JNT.

The substance of the paper is a partition-lattice / CRT-coordinate analysis on $(\mathbb{Z}/n\mathbb{Z})^{\times}$. This is squarely in the *combinatorial number theory* corner of JNT's scope. JNT does publish papers on the structure of $(\mathbb{Z}/n\mathbb{Z})^{\times}$ and related orbit-counting questions; whether *this particular* paper rises to the JNT bar depends on:

- Whether the prior literature gap is filled (M1).
- Whether the paper can stand alone without the J10 companion (M2).
- Whether the zero-fiber structural analysis is given the prominence it deserves (M4).

If those are addressed, this is a strong note-length contribution to JNT. The bar at JNT for short notes / corrections is, in my experience, substantively lower than for full research papers, and a 4–5 page note in the form "natural conjecture $\to$ counterexample $\to$ corrected theorem $\to$ structural reason" is exactly the genre.

### Possible alternative venues.

If JNT declines, the paper would also fit:
- **American Mathematical Monthly** as an undergraduate-accessible counterexample note.
- **Mathematics Magazine** for the same.
- **Integers** (Journal of Combinatorial Number Theory).
- **European Journal of Combinatorics** for the partition-lattice content.

---

## 8. Reproducibility

All numerical claims are checkable by hand or by trivial enumeration. There are no computational claims requiring code; I have verified each by direct computation. The paper is internally complete (modulo the dependency on J10 — see M2, M6).

---

## 9. Final remarks

This is a clean correction note with a real counterexample, a real structural insight (zero-fiber), and a clean corrected theorem. Of the three companion papers (J10/J11/J12), J11 is in my judgment the strongest and most JNT-appropriate.

The recommended decision is **Major revisions**, with the expectation that:

1. The prior literature is cited (M1).
2. The paper is restructured to stand alone, removing the UOP dependence (M2, M6).
3. The corrected theorem is presented as a *symmetrization* (with appropriate downplay of "Theorem C is a new theorem"), with the genuine novelty being (a) the counterexample and (b) the zero-fiber analysis (M3).
4. The zero-fiber analysis is promoted to a structural lemma in the introduction (M4).
5. Examples of disagreement between the prior and corrected conditions are added (M5).

After these revisions, the paper would be a strong JNT short note.

---

**Estimated revision effort:** 8–14 person-hours. Most of the work is presentational restructuring and adding 1–2 new examples / a literature citation; the mathematics is settled.

**Reviewer's confidence:** High. I have read the paper end-to-end, verified each numerical claim by independent enumeration, and re-derived the proofs.
