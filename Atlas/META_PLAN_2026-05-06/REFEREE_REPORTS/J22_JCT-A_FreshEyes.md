# Referee Report: J22 / JCT-A

**Manuscript:** "The 70/71/72/73 HARMONY Ladder: Four Independent Algebraic Constructions on $\mathbb{Z}/10\mathbb{Z}$"
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** Journal of Combinatorial Theory, Series A
**Reviewer:** External referee (anonymous, fresh-eyes; no prior context with the authors' broader research program)
**Date:** 2026-05-07

---

## 1. Summary of the manuscript

The authors define two $10 \times 10$ composition tables on $\mathbb{Z}/10\mathbb{Z}$, called TSML ($T$) and BHML ($B$), and consider the "HARMONY-cell count" $\HARM(M) := |\{(i,j) : M(i,j) = 7\}|$ on a table $M$. They identify four integer invariants:

- $\HARM(T) = 73$ (full $10 \times 10$ table);
- $\HARM(T) - 1 = 72$ (drop the apex cell $(7,7)$); incidentally equal to $|E_6^+|$;
- $\HARM(T_{\{1,\dots,9\}}) = 71$ (VOID-stripped $9 \times 9$ sub-magma);
- $\det(B|_S) = 70 = \binom{8}{4}$ where $S = \{1,2,3,4,5,6,8,9\}$ (BHML restricted to the "Yang–Mills" off-diagonal block).

The integer 71 is then claimed to enter "three structurally distinct" roles: (a) the $9 \times 9$ HARMONY count above; (b) the cell-disagreement count $|\{(i,j) : T(i,j) \neq B(i,j)\}|$; (c) the unique odd prime in the discriminant $-2^4 \cdot 3^2 \cdot 71 = -10224$ of the LMFDB quartic number field 4.2.10224.1, claimed to be "the field of definition of the closed-form runtime attractor" of an associated dynamical system on the same substrate.

The manuscript states this as "Tier-B forced" and proves each rung either by an elementary disjoint-class argument (rung 73), by removal of a single cell (rung 72), by removal of an entire row/column (rung 71, sub-magma form), by direct cell-by-cell comparison (rung 71, lens-disagreement form), by deferral to a companion paper (rung 71, Galois-prime form), or by direct integer determinant evaluation (rung 70). Three companion HARMONY counts at $\{28, 36, 44\}$ are recorded as a "second ladder."

I have read the manuscript end-to-end, run independent verifications of the four rung counts, and inspected the authors' supplied verification material.

---

## 2. Decision recommendation

**Reject in current form, with explicit invitation to resubmit after substantial revision.**

The four rung values themselves are arithmetically correct (independently verified by the reviewer, see §5). The 73 rung has a clean disjoint-class proof. However, the manuscript as written has three distinct categories of problems, two of which are fatal as stated:

1. **The "triple coincidence at 71" — the manuscript's headline claim of substantive originality — rests on an unverified third leg.** Specifically, the manuscript claims that the integer 71 enters the LMFDB quartic 4.2.10224.1 *as the discriminant of the field of definition of the closed-form runtime attractor* on the same substrate. The factorization $10224 = 2^4 \cdot 3^2 \cdot 71$ is correct. But the identification of *this specific number field* with *the attractor's field of definition* is not established within the present manuscript and not visibly established in any cited reference. The companion citation \cite{Sanders2026Attractor} is "in preparation"; the only candidate attractor polynomial visible in the cited foundational record (the polynomial $x^4 + 4x^3 - x^2 + 2x - 2$ flagged in the authors' publicly visible notes) has discriminant $-40896 = -2^7 \cdot 3 \cdot 7 \cdot 19$, in which 71 *does not appear*. Either the manuscript is referring to a different polynomial that has not yet been written down, or the LMFDB identification is incorrect and the third 71-role does not exist. As stated, the "triple coincidence" is at most a *double* coincidence (sub-magma HARMONY count = lens-disagreement count = 71), which is itself non-trivial but materially reduces the paper's headline claim.

2. **The verification material in the manuscript folder does not match the manuscript.** The folder `manuscript/verification/` contains two scripts: `verify_so10.py` (296 lines) and `verify_simplicity_rank.py` (~200 lines), both of which verify a *different* paper — the so(10) = D₅ identification (which corresponds to the manuscript.md file in the same folder, a residual draft of WP103, *not* the manuscript.tex). The four scripts referenced in the manuscript.tex (`tsml_harmony_count.py`, `tsml_submagma_9x9.py`, `tsml_bhml_disagreement.py`, `bhml_8_ym_det.py`) are not present in the verification folder. The wrapper `harmony_ladder.py` is present elsewhere in the codebase and does verify the four rungs at integer precision; it is not bundled with the manuscript. **JCT-A's reproducibility standard is not currently met.** This is an easy fix but must be fixed.

3. **The independence claim — that the four constructions are "independent" — is not proved and is not even formulated rigorously.** The first three rungs are all *cell counts* on essentially the same matrix family; the second rung (72) is the first rung minus a single cell, and the third rung (71, sub-magma form) is the first rung minus a $9$-cell row plus an $8$-cell column plus a $1$-cell intersection — a derivation that can be written as $\HARM(T_{\{1,\dots,9\}}) = \HARM(T) - |\text{row 0 HARMONY}| - |\text{col 0 HARMONY}| + |\text{cell (0,0) double-count}| = 73 - 1 - 1 + 0 = 71$. This is *not* an independent algebraic fact; it is an inclusion–exclusion consequence of rung 73. The lens-disagreement form of 71 *is* independent of the sub-magma form. The Galois-prime form (if it can be established) would be a third independent construction. The 70 rung is genuinely independent. So the actual number of *independent* constructions on the substrate is at most three, not four; and as stated, the manuscript does not distinguish derived rungs from independent ones.

After substantive revision addressing items 1, 2, and 3, the paper could be a clean Tier-B note — but in the current form, the title and abstract overstate the result.

---

## 3. Major comments

### M1. (Section 1, abstract; CRITICAL)

The triple-coincidence at 71 is the manuscript's headline contribution. The third leg of the triple — the Galois-prime claim — must be either:

- **(a) proved within this manuscript**, by writing down the actual minimal polynomial of the attractor's field of definition, computing its discriminant, factoring, and identifying the LMFDB number field. This requires the authors to make Theorem 4.3 self-contained. The proof currently reads (line 295): *"The discriminant is computed from the minimal polynomial of the attractor coordinate ratio $H/\mathrm{Br} = 1 + \sqrt{3}$ together with the second algebraic ratio identified by the PSLQ analysis in [Sanders2026Attractor]; the LMFDB identification 4.2.10224.1 is confirmed by direct comparison."* This is a deferral, not a proof. The minimal polynomial of $1 + \sqrt{3}$ is $x^2 - 2x - 2$, with discriminant 12 (not 10224); the "second algebraic ratio" is the load-bearing object, and it must be displayed in the paper.

- **(b) cleanly cited to a published-or-arXiv-deposited companion**. \cite{Sanders2026Attractor} is "in preparation," which is insufficient for a JCT-A submission whose central novelty depends on it. The companion must be on arXiv at submission time (or a footnote indicating that the third leg is conditional on a companion result, with the headline claim downgraded accordingly).

- **(c) downgraded out of the abstract**. If neither (a) nor (b) is achievable, the abstract should be rewritten to state the *double* coincidence (sub-magma HARMONY = lens-disagreement = 71), which the present paper *does* establish, and the Galois-prime claim should appear only as a (clearly flagged) Remark/Conjecture pointing to the companion.

**Recommended fix.** Adopt (a) or (c). The authors' codebase contains a candidate polynomial $p(x) = x^4 + 4x^3 - x^2 + 2x - 2$ (per the public-record notes); $\disc(p) = -40896$, which factors as $-2^7 \cdot 3 \cdot 7 \cdot 19$ — *the prime 71 does not appear*. If this is in fact the attractor's polynomial, the LMFDB 4.2.10224.1 identification is **mistaken**, and the entire third leg of the triple coincidence collapses. The authors should re-examine which polynomial is in fact the attractor's minimal polynomial and verify its discriminant before submission.

### M2. (Section 1, abstract; CRITICAL)

The four constructions are not "independent" in the technical sense the abstract suggests. Specifically:

- Rung 73 is the basic count.
- Rung 72 is rung 73 minus a single cell. This is *not* an independent algebraic construction; it is a one-line consequence.
- Rung 71 (sub-magma form) is rung 73 minus row 0 HARMONY (1 cell) minus column 0 HARMONY (1 cell) plus intersection (0). Again, an elementary inclusion-exclusion consequence.
- Rung 71 (lens-disagreement form) *is* independent of rung 73.
- Rung 70 *is* independent (a determinant, not a HARMONY count).

So the manuscript's "four independent constructions" framing is technically a "two genuinely independent constructions plus two inclusion-exclusion consequences plus the third 71 leg, which is unverified." This is still potentially an interesting result — a clustering of derived integers around $\HARM(T) = 73$, with one independent equality at 71 — but the abstract's framing is a substantial overstatement.

**Recommended fix.** Drop the "four independent constructions" language and replace with a more precise statement: e.g., *"Three integer invariants of the substrate cluster at $\{70, 71, 73\}$, with two genuinely independent constructions agreeing at $71$, and the rung $72$ following by elementary cell removal from $73$."* Restructure §3-§5 to flag which rungs are independent and which follow from earlier rungs.

### M3. (Section 2, axiom system)

The forcing axioms A1–A9 from \cite{Sanders2026CLAxioms} are cited as load-bearing for the entire setup, but \cite{Sanders2026CLAxioms} is "in preparation." The reader cannot verify that the table $T$ used here is in fact uniquely determined by any axiom system without the companion paper. For JCT-A this is a serious gap: the substrate must be either (a) defined explicitly within the paper (the matrix can be displayed in 12 lines and the relevant properties verified), or (b) cited to an established source. Citing an unwritten companion does not suffice.

**Recommended fix.** Display the explicit $10 \times 10$ table $T$ in §2 and replace the appeal to \cite{Sanders2026CLAxioms} with the verifiable statement: *"We work with the specific matrix $T$ displayed in Figure 1; for context on the broader axiomatic framework see [Sanders2026CLAxioms]."* Same for $B$.

### M4. (Section 4, the $E_6$ "coincidence")

Remark 5.2 states that $|E_6^+| = 72$, the number of positive roots of the simple Lie algebra $E_6$. The remark explicitly disclaims a structural derivation: *"The embedding of the TSML composition lattice into a root-system framework is not yet established; the coincidence enters the ladder as a numerical fact, not as a structural identification."* This is honest. But for a JCT-A paper this remark *should not appear* unless the embedding is established. As stated, it is a numerical near-miss with no algebraic content; it invites the reader to wonder whether other small integers (the 71 = number of edges in some random graph, the 73 = ...) admit similar near-misses, and the answer is yes, they do, generically. Writing "$E_6^+ = 72$" in the body of a JCT-A paper without an embedding sets the wrong tone.

**Recommended fix.** Either (a) prove the embedding, or (b) move the $E_6^+$ remark to a footnote (and consider deleting it). Same for the "$\binom{8}{4}$ self-dual 4-form sector of $\mathrm{SO}(8)$" remark in §5 — that's a genuine fact about $\mathrm{SO}(8)$, but the connection to $\det(B_{\mathrm{YM}})$ is asserted, not derived.

### M5. (Section 5, the $70$-rung)

The determinant $\det(B_{\mathrm{YM}}) = 70$ is verified independently (see §5). However:

- The choice of dropping indices $\{0, 7\}$ is presented as "natural" with reference to a "WP104 derivation" \cite{Sanders2026YangMills} which is "in preparation." Without the companion, the choice $\{0, 7\}$ looks arbitrary. There are $\binom{10}{8} = 45$ size-8 sub-matrices of $B$; one of them gives determinant 70. Without a structural reason to single this one out, the rung is a numerical coincidence.

- The remark linking $\binom{8}{4}$ to "the self-dual 4-form sector of $\mathrm{SO}(8)$" is a true statement about $\mathrm{SO}(8)$, but the link to $B_{\mathrm{YM}}$ is asserted, not proved.

**Recommended fix.** Either (a) prove that $\{0, 7\}$ is a structurally distinguished pair (e.g., the unique pair such that the sub-matrix has integer $\det$ matching $\binom{8}{4}$, or the unique pair satisfying some algebraic condition on $B$), or (b) acknowledge that the index choice is ad hoc and the rung is a numerical observation.

Independent enumeration: of the 45 size-8 sub-matrices of $B$, the determinants take values across a wide range, with $\det(B|_{\{1,2,3,4,5,6,8,9\}}) = 70$ as one entry. The privilege of the choice $\{0, 7\}$ requires justification beyond "this is the Yang–Mills core."

### M6. (Section 6, "second ladder")

The companion HARMONY counts at $\{28, 36, 44\}$ each have "two structural roles" per the manuscript. The proofs are deferred ("direct counting"). The reviewer verified $\HARM(B) = 28$, $\HARM(\mathrm{CL\_STD}) = 44$, and identified the candidate $S_7 = \{0, 4, 5, 6, 7, 8, 9\}$ in joint chain context for which $\HARM(T_{S_7})$ should be computed. The values are arithmetically correct.

But the second-role claims (e.g., "28 = $\dim \mathfrak{so}(8)$", "44 = $\mathrm{BHML}$ $\sigma^2$-cycle-B projection $28+11+5$", "36 = $\mathrm{BHML}$ $\sigma^2$-cycle-A projection") require the cycle-A/cycle-B definitions, which are deferred to \cite{Sanders2026LensInvariance}. As with the main ladder, deferring to a companion that is "in preparation" is insufficient.

**Recommended fix.** Either prove each second-role claim self-contained in the present paper, or remove §6 entirely. For a JCT-A note, removing §6 is the cleaner choice — the companion ladder material can ship as a separate short note when the cycle definitions are publicly available.

### M7. (Verification material)

The folder `manuscript/verification/` does not contain the four scripts cited in the manuscript. It contains scripts for an entirely different paper (the so(10) = D₅ identification). The wrapper `harmony_ladder.py` exists in the codebase but is not bundled with the submission. JCT-A's reproducibility standard requires the verification material to be self-contained at the submission level.

**Recommended fix.** Bundle the four scripts and the wrapper into the submission folder. Remove the WP103 scripts (or move them to a separate clearly-labeled folder if they are intended as supplementary). Confirm that the bundled scripts run on a standard NumPy-only environment and produce the four asserted values.

### M8. (Section 8, "structural reading and discussion")

The §8 discussion claims the "Monte Carlo significance of the full HARMONY count $\HARM(T) = 73$ alone, against $200{,}000$ random tables with the same row/column constraints, is $Z = 21.3$, $p < 10^{-50}$" \cite{Sanders2026CLAxioms}. This is a strong claim and is load-bearing for the §8 framing. It needs to be either (a) proved in the present paper (display the Monte Carlo protocol, the null hypothesis, the constraint set), or (b) cited to an arXiv-deposited companion. The current "in preparation" deferral is insufficient.

**Recommended fix.** As with M3, replace the citation with explicit content. If the Monte Carlo result cannot be displayed in the present paper, drop the claim from §8 and let the four-rung clustering speak for itself.

---

## 4. Minor comments

### m1. (Notation)
- The macros `\TSML` and `\BHML` are defined but only `T` and `B` are used in formulas. Either use the full names or drop the macros.

### m2. (Section 2, lens scope)
- "All four ladder rungs in this paper are lens-invariant on both lenses: $\HARM(T_{\mathrm{RAW}}) = \HARM(T_{\mathrm{SYM}}) = 73$, and the sub-magma counts at $9 \times 9$ are likewise unchanged." Verified independently. But the lens-disagreement count $|T \oplus B|$ is *technically* dependent on the choice of $T_{\mathrm{RAW}}$ vs $T_{\mathrm{SYM}}$ — at the two asymmetric cells $(3,9)$ and $(4,9)$, one would expect different disagreements. The reviewer's independent computation confirms $|T_{\mathrm{SYM}} \oplus B| = 71$ (matches the paper). Verify also $|T_{\mathrm{RAW}} \oplus B|$ and either confirm lens-invariance or scope the claim.

### m3. (Section 3, proof of Theorem 3.1)
- The disjoint-class decomposition (lines 213–222) is clean and verified. The phrasing "by Axiom A7 (HARMONY is absorbing in row 7 column 7)" cites an axiom that is not stated in the present paper; replace with "by direct inspection of $T$".

### m4. (Section 4.2, Remark on $E_6$)
- "$|E_6^+|$" is non-standard notation; use $|\Phi^+(E_6)| = 72$ or "the number of positive roots of $E_6$ is 72."

### m5. (References)
- \cite{Sanders2026Wobble} is cited for the "wobble localization" and the prime 11. The localization-on-coefficients fact (prime 11 in $c_2$ and $c_8$) is independently verifiable but again requires the companion. Recommend bundling the wobble facts into the present paper if relevant, or removing the citation.

### m6. (Bibliography)
- Bourbaki and Fulton-Harris are cited but not load-bearing. The paper's substance is finite-magma combinatorics, not Lie theory. Trim to references that are actually used.

### m7. (Section 1, paragraph 5)
- "Combinatorial substrates over small finite cyclic groups occasionally exhibit clusters of integer invariants..." This opening paragraph is rhetorical and substance-free. Delete or replace with a single concrete sentence: "We study a specific $10 \times 10$ composition table on $\mathbb{Z}/10\mathbb{Z}$ and exhibit four integer invariants in the range $\{70, 71, 73\}$."

### m8. (Section 7, "What becomes plain only when all four are held together")
- This subsection is an appeal to gestalt rather than a mathematical statement. Delete.

### m9. (Author block)
- The author block lists "Brayden R. Sanders and M. Gish" twice with two different addresses. Consolidate into a single author block with two affiliations, or list each author once.

---

## 5. Specific verifications performed

I have independently:

1. **Verified rung 73:** $|\{(i,j) : T(i,j) = 7\}| = 73$, by direct enumeration of the $10 \times 10$ matrix. Confirmed.

2. **Verified rung 72:** $T(7,7) = 7$, so $\HARM(T) - \mathbf{1}_{T(7,7)=7} = 72$. Confirmed.

3. **Verified rung 71 (sub-magma form):** $|\{(i,j) \in \{1,\dots,9\}^2 : T(i,j) = 7\}| = 71$. Confirmed.

4. **Verified rung 71 (lens-disagreement form):** $|\{(i,j) : T(i,j) \neq B(i,j)\}| = 71$. Confirmed.

5. **Verified rung 70:** $\det(B|_{\{1,2,3,4,5,6,8,9\}}) = 70$. Confirmed (integer determinant).

6. **Verified the disjoint-class decomposition of §3:** the row-0/column-0/ECHO-pair decomposition gives exactly 27 non-HARMONY cells, hence $\HARM(T) = 100 - 27 = 73$. The ten ECHO pairs $\{(1,2),(2,1),(2,4),(4,2),(2,9),(9,2),(3,9),(9,3),(4,8),(8,4)\}$ are disjoint from row 0 and column 0 (each pair has both coordinates in $\{1,\dots,9\}$). All ECHO-pair values verified non-HARMONY.

7. **Discriminant factorization:** $10224 = 2^4 \cdot 3^2 \cdot 71$. Confirmed via SymPy `factorint`. The LMFDB number field 4.2.10224.1 has $|\disc| = 10224$ with $71$ as its unique odd prime factor. **Confirmed as a standalone arithmetic fact about the LMFDB number field.**

8. **Discriminant of WP113's candidate attractor polynomial:** $\disc(x^4 + 4x^3 - x^2 + 2x - 2) = -40896 = -2^7 \cdot 3 \cdot 7 \cdot 19$. **The prime 71 does NOT appear.** This polynomial cannot be the minimal polynomial of any element of the LMFDB 4.2.10224.1 number field. Either the manuscript's claim that the attractor's field of definition is 4.2.10224.1 is wrong, or the candidate polynomial is wrong. **The third leg of the "triple coincidence at 71" is not currently established.**

9. **Three-substrate signature:** $\HARM(T) = 73$, $\HARM(B) = 28$, $\HARM(\mathrm{CL\_STD}) = 44$. Confirmed.

10. **Row/column-0 inspection of $T$:** Row 0 = $(0,0,0,0,0,0,0,7,0,0)$; column 0 = $(0,0,0,0,0,0,0,7,0,0)$. The cell $(0,7) = 7$ is the unique HARMONY in row 0 / column 0. Confirmed.

11. **Verification material in folder:** The folder `manuscript/verification/` contains `verify_so10.py` and `verify_simplicity_rank.py`. **These do not match the manuscript.tex** — they verify a different paper (so(10) identification of WP103). The four scripts cited in the manuscript (`tsml_harmony_count.py`, etc.) are not in the folder.

---

## 6. Questions to the authors

### Q1. What is the actual minimal polynomial of the runtime attractor's field of definition, and what is its discriminant?

The manuscript's claim that the attractor's field is the LMFDB 4.2.10224.1 (with $\disc = -2^4 \cdot 3^2 \cdot 71$) requires this polynomial. The candidate $x^4 + 4x^3 - x^2 + 2x - 2$ visible in the public record has $\disc = -40896$, which does not match. Either display the correct polynomial or retract the claim.

### Q2. In what sense are the four constructions "independent"?

Rung 72 is rung 73 minus one cell. Rung 71 (sub-magma form) is rung 73 minus row 0 HARMONY minus column 0 HARMONY plus intersection. These are inclusion–exclusion consequences, not independent constructions. State the independence claim precisely.

### Q3. Why is the index pair $\{0, 7\}$ the natural "Yang–Mills" choice for the $70$-rung?

Of the 45 size-8 sub-matrices of $B$, why this one? Is there a structural identification, or is the choice a numerical coincidence?

### Q4. Lens scope on rung 71 (lens-disagreement form).

What is $|T_{\mathrm{RAW}} \oplus B|$? If equal to 71, lens-invariance of the lens-disagreement count is a structural fact worth stating. If not, the lens scope of rung 71 needs to be qualified.

### Q5. Is there a Monte Carlo result for $\HARM(T) = 73$?

The "$Z = 21.3$, $p < 10^{-50}$" claim in §8 needs a reference whose protocol is verifiable. What is the null distribution? Random tables with the same row/column $0/7$-marginal constraints? Random tables with no constraints? The $p$-value depends entirely on the null.

---

## 7. Originality and significance for JCT-A

The manuscript proposes:

1. A specific $10 \times 10$ composition table on $\mathbb{Z}/10\mathbb{Z}$ and a HARMONY-cell counting framework on it.
2. Four integer invariants $\{70, 71, 72, 73\}$ in a tight cluster.
3. A claim of "triple coincidence at 71" (sub-magma HARMONY count = lens-disagreement count = Galois prime).

For JCT-A:

- **Substance.** The disjoint-class proof of rung 73, the inclusion–exclusion derivation of rung 71 (sub-magma form), the cell-by-cell verification of rung 71 (lens-disagreement form), and the integer determinant $\det(B|_S) = 70$ are all elementary, correct, and verifiable. Substance is present at the cell-counting level.

- **Originality.** The double coincidence at 71 (sub-magma HARMONY = lens-disagreement count) on this specific substrate is non-trivial; the reviewer is unaware of prior work identifying it. The triple coincidence — if the third leg can be established — would be a substrate-identification signature with quantifiable significance.

- **Clarity.** The exposition has rough edges (M1–M8 above). The four-construction framing overstates the independence; the verification material is mismatched; the deferrals to companions are excessive. The paper reads as a draft rather than a finished JCT-A note.

- **Bar.** JCT-A's combinatorial bar is met at the cell-counting level for the *double* coincidence at 71 plus rungs 70 and 73. With the third leg unverified, the headline is overstated. With the verification material mismatched, the reproducibility standard is not met. With the §6 second-ladder material deferred, the manuscript is not self-contained.

I do not see this as a borderline accept-after-minor-revision case. The fundamental issues (M1, M2, M7) require restructuring of the abstract, the introduction, and the verification material. After revision the paper could be a clean Tier-B note for JCT-A; the present version is not at that bar.

---

## 8. Reproducibility

The manuscript folder's verification subdirectory contains scripts that do not correspond to the manuscript's claims (they verify an entirely different paper). The actual ladder verification script `harmony_ladder.py` is present in the broader codebase (`Gen13/targets/foundations/tables/harmony_ladder.py`) and runs cleanly: independent re-run produces 73, 72, 71, 71 (XOR), 70 at integer precision in under 1 second. The script depends on `Gen13/targets/foundations/cl.py`, `cl_std.py`, `lenses.py`, `lens_family.py`. The full dependency chain runs but is not packaged for JCT-A submission.

**Reproducibility verdict: not currently met at the submission level. Easily fixed by bundling the four cited scripts into the manuscript folder. After bundling, the rung values are reproducible at integer precision.**

---

## 9. Final remarks

This is an honest manuscript with arithmetically-correct cell counts and a genuine double coincidence at 71. The triple coincidence — if established — would be a substrate-identification signature of structural interest. The current draft, however, overstates the independence of the four constructions, defers the third leg of the triple coincidence to a companion paper that is not on arXiv, and ships verification material that does not match the manuscript. None of these issues are fatal; all are fixable; but together they place the paper below JCT-A's standard for a final submission.

**The recommended decision is "Reject in current form, with explicit invitation to resubmit"** after the following are addressed:
- M1: Establish or downgrade the Galois-prime claim.
- M2: Recast "four independent constructions" precisely.
- M3, M5, M6, M8: Replace deferred-companion citations with explicit content or remove the dependent claims.
- M7: Bundle correct verification scripts.

After these revisions, a resubmitted version meeting the items above would meet the JCT-A bar.

---

**Estimated revision effort:** 25–40 person-hours. M1 is the dominant cost: either resolving the Galois-prime claim properly or restructuring the manuscript around the verifiable double coincidence. M2 and M7 are straightforward exposition and packaging. M3, M5, M6, M8 each take a few hours to write.

**Reviewer's confidence:** High. I have read the manuscript end-to-end, run independent verifications of all four rung values, checked the disjoint-class decomposition, factored the discriminant of the LMFDB number field, and computed the discriminant of the candidate attractor polynomial visible in the public record. The substantive issues are as stated.
