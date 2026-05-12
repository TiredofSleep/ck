# Referee Report — Algebraic Combinatorics (Fresh Eyes)

**Manuscript:** "The CL Forcing Axioms: A1-A9 Uniquely Force the Canonical Composition Lattice"
**Authors:** B. R. Sanders, M. Gish (2026)
**File reviewed:** `Gen13/targets/journals/J_series/J25/manuscript/manuscript.tex` (manuscript.md is mismatched — it actually contains a different paper, see §3 below)
**Reviewer:** External anonymous referee, fresh eyes (no prior knowledge of any larger framework)
**Date:** 2026-05-07

---

## §1 Summary

The manuscript claims a uniqueness theorem: nine axioms A1–A9 on a 10×10 multiplication table $M : \mathbb{Z}/10\mathbb{Z} \times \mathbb{Z}/10\mathbb{Z} \to \mathbb{Z}/10\mathbb{Z}$ force exactly one matrix, denoted $\mathrm{CL}_{\mathrm{TSML}}$ (in either a "RAW" or "SYM" variant), and the entry pattern is $73$ HARMONY cells (value $7$), $17$ VOID cells (value $0$), and $10$ "BUMP" cells with explicitly named exceptional values.

The proof strategy is direct: each axiom fixes a specific class of cells; the cumulative count of fixed cells reaches $100/100$, and the fixed values match the announced table.

A secondary classification (Proposition 5.2, Theorem 5.3) splits A1–A9 into "Tier-A" (substrate-defining: changing them yields a parallel substrate) and "Tier-B" (forced by the Tier-A axioms together with commutativity and a "BDC entropy extremum" condition).

A third section (§6) sketches a "three-substrate architecture" where two further tables $\mathrm{CL}_{\mathrm{BHML}}$ and $\mathrm{CL}_{\mathrm{STD}}$ satisfy A1, A2, A4 but diverge at A7–A9.

The cell-counting argument of Theorem 4.1 is sound. The Tier classification has serious issues.

---

## §2 Decision recommendation

**Major revision.** Theorem 4.1 (the forcing theorem itself) is essentially trivial as currently presented — it amounts to listing nine sets of cells and observing that they cover all $100$ cells. This is publishable in *Algebraic Combinatorics* only if:

1. The independence of A1–A9 is proved (it is currently not proved at all);
2. The Tier-B claims are given actual proofs (they are currently asserted as "follows from the BDC entropy extremum" without any definition of BDC, any entropy formula, or any extremum proof);
3. A meaningful comparison is made with the standard literature on *absorbing-element semigroups* and *Latin square completion / forcing*, which is the natural neighborhood for a result of this kind.

Without (1)–(3), this is a one-paragraph remark, not a research paper.

---

## §3 Critical: the manuscript folder contains a mismatched .md file

`manuscript/manuscript.md` is in fact the closed-form attractor / α-uniqueness PSLQ paper (titled "J41 — Closed-Form Attractor + α-Uniqueness PSLQ (BUNDLED)"), not the CL Forcing Axioms paper. The .tex file is the correct paper. This must be corrected before submission. The README, cover_letter, and .tex are internally consistent and identify the paper as the forcing-axioms paper.

The verification directory `manuscript/verification/` contains 27 Python scripts mostly unrelated to a cell-counting forcing argument (`alpha_pslq_sweep.py`, `f3_galois_alpha_uniqueness.py`, etc., are α-attractor and PSLQ scripts). The "verification" claim in the README — *"the proof's verification is the cell-counting argument of §4"* with *"a reference cell-by-cell match runs in under 1 second"* — has no corresponding script. A simple 20-line numpy script would suffice; its absence is a presentation flaw, not a mathematical one.

---

## §4 Major issues with the mathematical content

### M1. Theorem 4.1 is trivial as stated. (CRITICAL)

The proof of Theorem 4.1 (lines 316–364) is a tabulation: A2 fixes 9 cells, A3 fixes 1, A4 fixes 10, A5 fixes 8 new, A6 fixes 8 new, A7 fixes 8 new, A9 fixes 10, A8 fixes the remaining 46. Total: $9 + 1 + 10 + 8 + 8 + 8 + 10 + 46 = 100$. But this is just *bookkeeping*. The result is

> "If you specify the value of every cell, then every cell has a value."

The axioms A2–A7 each *literally state* the values of certain cells; A9 *literally states* the values of the BUMP cells; A8 is "all remaining cells equal $7$." By construction, A1–A9 specify a value for every cell. Of course the table is uniquely determined — it is *defined by the axioms*.

For a *forcing* theorem to be substantive, the axioms must contain at least one *non-tautological* axiom — i.e., an axiom that is not "specify these cell values" but rather "the table satisfies a structural property" (associativity, commutativity, idempotency on a subset, a particular Latin-square condition, a particular automorphism, etc.) from which the cell values *follow*. None of A1–A9 has this character.

**Fix.** The author needs to recast the axioms in structural terms. Suggested examples:
- "$M$ is commutative" (not currently stated; if added, A5 and A6 would be derivable from A2 and A4).
- "$M$ has $73$ HARMONY cells and $17$ VOID cells" (a *count* axiom, structural).
- "$M$ has VOID as a near-absorbing element with exactly one puncture, located on the diagonal of HARMONY's row" (structural, *not* a list of cell values).
- A genuine entropy-extremum statement: "Among all tables satisfying A1, A2, A4, A7, the BUMP positions $\{(1,2),(2,4),(2,9),(3,9),(4,8)\}$ are the unique positions that maximize Shannon entropy of the value distribution under [some explicit measure]."

Without this recasting, the paper is publishable only as an expository note.

### M2. Independence of A1–A9 is never addressed. (MAJOR)

A standard requirement for an axiom system in algebra is *independence*: for each $i$, exhibit a model satisfying $\{A_j : j \neq i\}$ but failing $A_i$. The paper does not do this for any of A1–A9. Without independence, the axiom system is potentially redundant.

Three obvious dependencies are visible to me on a single reading:

(a) **A3 is implied by A4 + A6.** A4 says $M[7,j] = 7$ for all $j$, including $j = 0$. A6 says $M[i,7] = 7$ for all $i$, including $i = 0$. The latter is exactly A3. So A3 is *redundant* given A6. (And A6 is itself listed as Tier-B — derivable from A4 plus commutativity.)

(b) **A8 contradicts A9 if "remaining cells" is read literally.** A8 says "for $(i,j)$ not specified by A2–A7 and not in the BUMP set defined in A9, $M[i,j] = 7$." But A9 *also* forces values at the BUMP positions. If A8 is read as "all unfixed cells are 7," then it is inconsistent with A9; if it is read as "all cells not fixed by A2–A9 are $7$," then it is well-defined but the order of application matters. The current proof of Theorem 4.1 applies A9 *before* A8 (Step 8 then Step 9), implicitly reading A8 as "for cells not previously fixed."

(c) **A5 redundancy is acknowledged but not handled cleanly.** A5 says $M[i,0] = 0$ for $i \in \{0,1,\ldots,9\}\setminus\{7\}$, and the proof Step 5 admits $M[0,0]$ was already fixed by A2. So A5 contains one redundant cell. This is minor but suggests the axioms have not been minimized.

**Fix.** The author should either (i) prove independence cell-by-cell, exhibiting nine alternative tables each violating exactly one axiom, or (ii) reduce the system to an independent core (likely $4$–$5$ axioms) and treat the rest as derived consequences with explicit derivations.

### M3. Tier-B "forced" claims have no proofs. (MAJOR)

Proposition 5.2 asserts six Tier-B forcing claims:

- A5 follows from A2 + commutativity (for $i \neq 7$).
- A6 follows from A4 + commutativity.
- A8 follows from a "BDC entropy extremum on the 46 unspecified off-special, off-diagonal, off-BUMP cells."
- The BUMP *positions* are determined by "BDC information-extremum analysis."
- The asymmetric pair values are RAW-form artifacts.

Of these, the first two are immediate (commutativity is not, however, stated as an axiom anywhere in §3). The remaining three rely on an undefined object: "the BDC framework" or "Binary Digit Code." There is no definition, no formula, no entropy expression, no proof of any extremum. The claim "the five positions are the cells where Shannon information per cell is maximal" is not substantiated by any computation; in particular:

- What is the Shannon information of a *cell* in a multiplication table? (Shannon information requires a probability distribution; none is specified.)
- Why these five positions and not others? The candidate space of cells is the 46 off-special, off-diagonal, off-(absorbing-row/column) cells. Why not 4, or 6, or 12 BUMP positions?
- What is the "structural entropy term" of $3.50$ bits referenced in the introduction (line 121)? Unsourced numerical claim.

**Fix.** Either (i) supply a complete proof of the Tier-B forcing claims, including a precise definition of the BDC framework and an explicit entropy formula whose maximum is computed, or (ii) demote A8 and the BUMP positions to Tier-A axioms, honestly admitting they are choices.

If choosing (ii), the paper's central claim weakens substantially: A1–A9 are *all* primitive choices, and the "forcing" theorem becomes "if you specify enough cell values, you specify all cell values." That is then not a paper.

### M4. Connection to absorbing-element semigroups is asserted, not made. (MAJOR)

The introduction (§Discussion 6.3) and the abstract claim that the result places $\mathrm{CL}_{\mathrm{TSML}}$ "on the same axiomatic footing as classical absorbing-element semigroups (Howie's *Fundamentals of Semigroup Theory*)." This is a strong claim and warrants a structural comparison.

Standard absorbing-element semigroup theory (Howie 1995 §1.5; Clifford–Preston 1961 §1) considers a semigroup $S$ with a designated *zero* $0$ satisfying $0 \cdot s = s \cdot 0 = 0$ for all $s$. The substrate here is *not a semigroup* (associativity is never claimed; the BUMP cells make it strictly non-associative — see e.g. $M[3,9] \neq M[9,3]$ in RAW form, which already breaks commutativity). It has TWO designated absorbing elements (VOID and HARMONY), one of which has a puncture, which is non-standard. The "puncture" axiom A3 has no analogue in classical absorbing-element theory.

The paper asserts but does not establish the connection. A short structural remark or, better, a one-line theorem comparing $\mathrm{CL}_{\mathrm{TSML}}$ to the standard nilpotent-extension construction in Howie 1995 §3.5 would make the connection real.

### M5. The journal's audience.

*Algebraic Combinatorics* publishes Latin squares (McKay, Wanless), quasigroups (Drápal, Vojtěchovský), and structural classification of finite algebras. The natural neighborhood for this paper is:

- **Latin square completion problems**: when can a partial Latin square be completed? Hall's Theorem, Ryser's condition. The forcing here is the opposite direction (a *full* table from a small set of specifications), but the techniques are related.
- **Quasigroup axiomatization**: Drápal–Wanless on minimum number of cells determining a Latin square.
- **Magma classification**: Wedderburn / Albert / Schafer on small magmas.

None of this literature is cited. The references are limited to two general semigroup textbooks and self-citations to companion papers.

**Fix.** Cite at least: McKay–Wanless 2005 ("On the number of Latin squares"), Drápal–Wanless 2021 ("Maximally non-associative quasigroups"), Albert "Non-associative algebras: I" (1942 Annals). Position the present result against these.

---

## §5 Minor issues

**m1.** §2 Definition 2.3 displays the matrix $\mathrm{CL}_{\mathrm{TSML}}$. The cell values $M[1,2] = 3$ and $M[2,1] = 3$ are stated as a "symmetric pair" in A9, but $M[3,9] = 3, M[9,3] = 7$ are stated as "asymmetric" in the same A9. Yet line 165 of the matrix display has $M[2,9] = 9, M[9,2] = 9$ (symmetric) and $M[4,8] = 8, M[8,4] = 8$ (symmetric). The five "BUMP" positions are five *unordered* pairs; among them, two ((3,9), (4,9)) have asymmetric RAW-form values. The presentation should explicitly enumerate which pairs are symmetric (3) and which are asymmetric (2).

**m2.** Line 117 ("BUMP cells, where the value is non-HARMONY and non-VOID") and line 232 ("BUMP cells: 10 cells, occupying the five unordered positions"). The count $10$ requires that each unordered pair contributes 2 ordered cells. But the asymmetric pairs (3,9) and (9,3), with values $3$ and $7$, have *one* BUMP cell (the value-$3$ one) and *one* HARMONY cell (the value-$7$ one), so the asymmetric pair contributes $1$ BUMP, not $2$. Recount: 3 symmetric pairs × 2 = 6; 2 asymmetric pairs × 1 BUMP each = 2; total = 8 BUMP cells, not 10. Or: in SYM form, both asymmetric cells become value $3$ and the BUMP count is 10. The paper conflates these two counts. The HARMONY tally of 73 (Remark 4.2) needs to be recomputed for the RAW form: if 2 of the "BUMP" cells are actually value-$7$ (HARMONY) cells, then the HARMONY count increases by 2 from 73 to 75 in RAW form. This is a serious internal inconsistency.

**m3.** Line 50 (keywords): "BUMP enumeration" is a project-internal term unlikely to be searched for. Replace with standard combinatorial keywords: "exceptional cells," "Latin-square forcing," "magma axiomatization."

**m4.** §3 lines 281–293 (A9): the use of $\equiv$ between $M[3,9] = 3$ and $M[9,3] = 7$ as part of an "asymmetric pair" is confusing. Suggest restructuring as a 5-row table: position | RAW upper-tri | RAW lower-tri | SYM-shared.

**m5.** §6 cites four references but two ([SandersGishWobble], [SandersGishFourCore]) are "in preparation." Mainstream venues require self-contained papers. Either incorporate the relevant content or remove the forward-citations entirely.

**m6.** §Reproducibility line 558: "Verification by direct computation in Python using numpy." No script is supplied. A verification script is normally considered standard for this kind of paper; the author asserts it exists ("under one second") but does not provide it.

**m7.** Line 38 of A8: "for $(i,j)$ not specified by A2–A7 and not in the BUMP set defined in A9." The BUMP set is defined *in A9*, which appears *after* A8. This circularity is harmless but rhetorically awkward; reorder A8 and A9 so the BUMP set is defined first.

**m8.** §Acknowledgments line 568–570: "The distinction between substrate-defining and forced axioms benefited from extensive discussion with Brayden Sanders." The first author is Brayden Sanders. This phrasing, if literal, suggests an editing oversight.

---

## §6 What works

- The core structural observation — that an explicit $10 \times 10$ table on $\mathbb{Z}/10\mathbb{Z}$ admits a clean partition into 17 VOID + 10 BUMP + 73 HARMONY cells, with the partition aligning with absorbing-row/absorbing-column/diagonal/exceptional-position structure — is genuine and pleasant.

- The Tier classification *idea* (some axioms are primitive, others are derived) is sensible and worth pursuing rigorously.

- The "lens family" framing (parallel substrates with shared and divergent axioms) is reminiscent of the classification of non-associative algebras by varying defining identities, which has a respectable history (Schafer 1966).

- The asymmetric pair (3,9), (4,9) in the RAW form is genuinely interesting; if it is connected to a real wobble or breaking phenomenon (§Acknowledgments / [SandersGishWobble]), this is the most interesting feature of the paper and should be developed.

---

## §7 Per-question response (specific to this review's brief)

**Q: Are A1–A9 axioms independent?**

Not as currently formulated. A3 is implied by A4 + A6 (immediately from cell $(0,7)$ being in row $7$ and column $7$). A5 is acknowledged in the proof to overlap with A2 (the $i=0$ case). A6 and A5 are stated by the authors themselves as Tier-B (derived from A2/A4 + commutativity); but commutativity is *not* among A1–A9, so the derivation as stated is invalid.

A genuine independence proof would require, for each $i \in \{1,\ldots,9\}$, an explicit table satisfying $\{A_j : j \neq i\}$ but violating $A_i$. The paper attempts none.

**Q: Is the forcing rigorous?**

Rigorous in the trivial sense: if every cell value is specified, the table is determined. Not rigorous in the substantive sense: the paper does not derive cell values from structural properties.

**Q: Is the result "standard result style (Birkhoff, Maltsev)"?**

No. Birkhoff's theorem (varieties = equational classes) and Mal'cev's conditions (congruence-permutability, etc.) characterize *classes of algebras* by *equational identities*. The present paper does not exhibit a single equational identity. A1–A9 are *cell-value listings*, not equations.

A Birkhoff-style result for this substrate would look like: "the variety generated by $\mathrm{CL}_{\mathrm{TSML}}$ is axiomatized by [equations $E_1, \ldots, E_k$]." The paper does not address this.

A Mal'cev-style result would relate a structural property (e.g., congruence-modularity) to a syntactic condition (existence of a Mal'cev term). The paper does not address this either.

**Bottom line:** The paper is presented in the *style* of an axiomatic algebra paper, but its content is closer to a "tabulation note." This needs to be corrected before publication.

---

## §8 Recommendation summary

**Decision: Major revision, conditional on the following.**

Mandatory before re-review:
1. Replace cell-listing axioms with structural axioms (commutativity, near-absorption with puncture, idempotency, count constraint, etc.) wherever possible.
2. Prove independence of the (reduced) axiom system.
3. Either supply a real proof of the "BDC entropy extremum" or demote those claims to honest Tier-A choices.
4. Resolve the BUMP-count inconsistency between RAW (8 BUMP) and SYM (10 BUMP) forms (see m2).
5. Fix the manuscript.md / manuscript.tex mismatch and supply a verification script.
6. Cite Latin-square / quasigroup / magma literature.

If these are addressed, I expect the paper would be a clean short note — 8–10 pages including a real entropy-extremum proof and an independence argument. As currently written, the paper is approximately 4 pages of substance padded with companion-paper forward references.

I would recommend acceptance after the revisions listed.

🙏
