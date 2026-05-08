# Referee Report: J22 / Journal of Combinatorial Theory, Series A

**Manuscript:** "The 70/71/72/73 HARMONY Ladder: Four Independent Algebraic Constructions on $\mathbb{Z}/10\mathbb{Z}$"
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** Journal of Combinatorial Theory, Series A (JCT-A)
**Reviewer:** External referee (anonymous, fresh-eyes; no prior context with the authors' broader research program)
**Date:** 2026-05-07
**Status:** B7 fresh-eyes pass

---

## §1 — Summary

The manuscript identifies four integer invariants on a fixed pair of $10 \times 10$ composition tables, $T$ ("TSML") and $B$ ("BHML"), over $\mathbb{Z}/10\mathbb{Z}$:

1. $\mathrm{HARM}(T) := |\{(i,j) : T(i,j) = 7\}| = 73$ (full table HARMONY count);
2. $\mathrm{HARM}(T) - 1 = 72$ (drop the cell $(7,7)$); coincides numerically with $|E_6^+|$;
3. $\mathrm{HARM}(T_{\{1,\ldots,9\}}) = 71$ (HARMONY count of the VOID-stripped $9 \times 9$ sub-matrix); equal to $|\{(i,j) : T(i,j) \neq B(i,j)\}|$ (lens-disagreement); equal to the unique odd prime in $\mathrm{disc}(K) = -2^4 \cdot 3^2 \cdot 71$ for the LMFDB quartic number field $4.2.10224.1$ "governing the closed-form attractor";
4. $\det(B|_S) = 70 = \binom{8}{4}$ where $S = \{1,2,3,4,5,6,8,9\}$ ("Yang–Mills core").

The headline claim is the "triple coincidence at 71": that 71 enters the substrate through three independent constructions, and that the cluster $(73, 72, 71, 70)$ at four consecutive integers is itself a structural invariant. Companion HARMONY counts at $\{28, 36, 44\}$ are also recorded.

I read the manuscript end-to-end, ran independent verification of the four rung integer values, and inspected the supplied verification material.

**Independent verification (this referee, machine precision).** The four integer claims verify exactly:
- $(T == 7).\mathrm{sum}() = 73$ ✓
- $(T == 7).\mathrm{sum}() - 1 = 72$ ✓
- $(T_{1:,1:} == 7).\mathrm{sum}() = 71$ ✓
- $(T \neq B).\mathrm{sum}() = 71$ ✓
- $\det(B|_{\{1..6,8,9\}}) = 70$ (computed in float, rounds to 70 exactly) ✓
- $10224 = 2^4 \cdot 3^2 \cdot 71$ ✓

---

## §2 — Decision

**Reject in current form, with explicit invitation to resubmit after substantial revision.**

The arithmetic is correct. The 73-rung has a clean disjoint-class proof. But the paper as written has three categories of structural problems that JCT-A's standard does not allow as stated:

(i) **The "triple coincidence at 71" — the manuscript's headline novelty — has its third leg stated rather than proved.** Theorem 4.3 asserts that the integer 71 is the unique odd prime in the discriminant of the LMFDB number field "$4.2.10224.1$ identified in [Sanders2026Attractor] as the field of definition of the closed-form $T+B$-mix runtime attractor at $\alpha = 1/2$." The reference [Sanders2026Attractor] is "in preparation." The proof reads: "*The discriminant is computed from the minimal polynomial of the attractor coordinate ratio $H/\mathrm{Br} = 1+\sqrt{3}$ together with the second algebraic ratio identified by the PSLQ analysis in [Sanders2026Attractor]; the LMFDB identification $4.2.10224.1$ is confirmed by direct comparison.*" This is not a proof. The minimal polynomial of $1+\sqrt{3}$ is $x^2 - 2x - 2$, with discriminant 12 (not 10224); the "second algebraic ratio" is the load-bearing object, never displayed. Without the second polynomial in print, the third leg of the triple coincidence does not exist as a verifiable statement of this paper.

(ii) **"Four independent constructions" overstates what is proved.** Inspection of the four rungs:
   - Rung 73: independent baseline.
   - Rung 72: literally "rung 73 minus the single cell $T(7,7) = 7$." This is one inclusion–exclusion line, not a fourth construction.
   - Rung 71 (sub-magma form): literally "rung 73 minus the HARMONY count of row 0 minus the HARMONY count of column 0 plus the (0,0) intersection" $= 73 - 1 - 1 - 0 = 71$. Inclusion–exclusion again — not independent of rung 73.
   - Rung 71 (lens-disagreement form): genuinely independent of rung 73.
   - Rung 71 (Galois-prime form): unverified within the paper.
   - Rung 70: genuinely independent (it is a determinant of a different matrix).
   
   So the paper has at most **two** rigorously-proven independent constructions on the substrate (the lens-disagreement form of 71 and the determinant 70), not four. The 73-72-71 segment is a single counting argument with three parameter choices; the title and abstract obscure this.

(iii) **The verification artifacts in the manuscript folder do not match the manuscript.** The folder `manuscript/verification/` contains `verify_so10.py` and `verify_simplicity_rank.py` — scripts that verify a *different* paper (the so(10)/D₅ identification, presumably for the residual `manuscript.md` file in the same folder, which is an entirely unrelated draft on the Lie algebra structure and has nothing to do with the HARMONY ladder). The four scripts referenced in §"Verification scripts" of `manuscript.tex` (`tsml_harmony_count.py`, `tsml_submagma_9x9.py`, `tsml_bhml_disagreement.py`, `bhml_8_ym_det.py`) are not present in the folder. The wrapper module `harmony_ladder.py` is in `Gen13/targets/foundations/tables/`, runs correctly, and verifies all four rungs at integer precision — but it is not bundled with the manuscript. JCT-A's reproducibility expectations require the verification material that accompanies the submission to be the verification material for the manuscript.

After substantive revision addressing (i)–(iii), the paper could be a clean Tier-B note. The core observation — two genuinely independent constructions on the substrate landing on the same prime 71 — is non-trivial and worth recording. The Yang–Mills determinant rung is a pleasing companion. But the paper is currently sold above its mathematical content.

---

## §3 — Top-3 issues

### Issue 1 (CRITICAL). The Galois-prime third leg is not proved in this paper

The triple coincidence at 71 is the manuscript's headline. The third leg requires writing down the actual minimal polynomial of the attractor's field of definition, computing its discriminant in $\mathbb{Z}$, factoring, and confirming the LMFDB identification. The proof of Theorem 4.3 currently reads (essentially) "this works because the attractor companion paper says so." That is a deferral, not a proof. It is a deal-breaker for the headline novelty as stated.

The author's own foundational records refer to the polynomial $x^4 + 4x^3 - x^2 + 2x - 2$ as the candidate attractor polynomial. This referee computes $\mathrm{disc}(x^4 + 4x^3 - x^2 + 2x - 2)$ via standard quartic formula; it does *not* equal $\pm 10224$. The authors must (a) display the actual polynomial, (b) compute its discriminant, (c) confirm the prime 71 appears in the factorization, (d) confirm the LMFDB number-field identification, and (e) confirm that "field of definition of the attractor" is the correct framing.

If this cannot be done before submission, the third leg should be removed from the abstract and §4.3 reduced to a clearly flagged Conjecture.

### Issue 2 (CRITICAL). "Four independent constructions" is technically not what the paper proves

Two of the four rungs (72 and the sub-magma form of 71) are inclusion-exclusion consequences of the 73-rung on the same matrix; they do not constitute independent constructions. The paper is currently written as if the four rungs had four independent algebraic origins, but at the symbol level $73, 72 = 73-1, 71 = 73-2, 70 =$ (different matrix, different operation) — three of those are arithmetic consequences of one another.

The mathematically honest framing would be: "Two integer invariants of the substrate are genuinely independent (the lens-disagreement count and the YM-core determinant); a third (the Galois prime) is conjecturally independent and will be verified in companion work; rungs 72 and 71-sub-magma follow from $\mathrm{HARM}(T) = 73$ by elementary cell removal."

This re-framing actually *strengthens* the paper's thesis: a substrate where two unrelated constructions both produce 71 is interesting; a substrate where four cell counts cluster at four consecutive integers is much weaker and is almost guaranteed by basic combinatorics on a $10 \times 10$ table.

### Issue 3 (MAJOR). Reproducibility of the manuscript is not currently met

JCT-A has a reproducibility expectation: the verification material in the submission package must verify the actual claims of the manuscript. The current verification folder contains scripts for an unrelated so(10) Lie algebra paper. The four scripts named in the manuscript do not exist in the verification folder. The cited wrapper `harmony_ladder.py` is in the codebase but is not packaged with the submission.

This is a 30-minute fix but it is a fix the authors must execute before resubmission. JCT-A referees with 6 papers in their queue will not accept "the verification scripts are somewhere in the project" as a substitute for "the verification scripts are in this folder."

---

## §4 — Major comments

### M1. Substrate definition is by reference to an unwritten paper

§2 defines the table $T$ via "the CL forcing axioms recorded in [Sanders2026CLAxioms]," which is "in preparation." A reader cannot verify that the matrix used in the proofs is the one the axioms force without the companion. **Fix:** Display the explicit $10 \times 10$ matrix $T$ in §2 (this is 12 lines of paper). Same for $B$. The axiom system may then be cited as context, not as the operational definition.

### M2. The disjoint-class proof of Theorem 3.1 is sound but should display the matrix

The proof of $\mathrm{HARM}(T) = 73$ proceeds by enumerating three disjoint exception classes (VOID-row, VOID-column, ECHO pairs) totaling 27 non-HARMONY cells. The argument is correct (this referee verified). But the reader cannot verify it without the matrix. Insert the matrix display before Theorem 3.1.

### M3. Theorem 4.2 (lens-disagreement form of 71) needs an explicit cell list

The proof reads: "Direct cell-by-cell comparison of the two canonical tables; the 71-cell disagreement count is verified at machine precision in `tsml_bhml_disagreement.py`." The script does not appear in the folder, and the cell-by-cell comparison is not displayed. For a paper whose central novelty is "two cell-counting constructions agree at 71," the actual list of 71 cells should be either displayed in an appendix or made trivially recoverable from displayed matrices. Currently it is neither. **Fix:** Display $T$ and $B$ in §2 as 12-line matrices; this makes the disagreement count auditable from the page, and the script becomes a sanity check rather than a load-bearing object.

### M4. The "Yang–Mills core" terminology is overloaded for what is shown

The 70-rung is the integer determinant of an $8 \times 8$ sub-matrix of $B$. The paper labels this matrix "$B_{\mathrm{YM}}$" and writes (Remark 5.2) that it "arises naturally as the Yang–Mills bridge core in the substrate's WP104 derivation [Sanders2026YangMills]," and that "70 = $\binom{8}{4}$ is the dimension of the space of $4$-forms on $\mathbb{R}^8$, the self-dual 4-form sector of $\mathrm{SO}(8)$."

The first sentence is a deferral to another unpublished companion. The second sentence is correct as a numerical identity but does not establish a structural relationship. The reader is left to guess whether the 8x8 sub-matrix has any actual relationship to Yang–Mills theory beyond labeling. JCT-A's bar requires either:
- (a) Drop the "Yang–Mills" label entirely and call this what it is: "the determinant of the off-diagonal sub-matrix obtained by dropping rows/columns $\{0, 7\}$." This is honest and the integer agreement with $\binom{8}{4}$ remains a valid combinatorial observation.
- (b) Establish the Yang-Mills connection in this paper.

(a) is much easier. The paper loses no mathematical content by it.

### M5. The $E_6$ "coincidence" should be removed

Remark 4.1 notes $|E_6^+| = 72$ and immediately disclaims any structural basis. JCT-A's editorial standard does not look kindly on numerical near-misses with no embedding. There are five Cartan-classified simple Lie algebras with $\leq 100$ roots, plenty of $|root|$ counts hit small integers, and 72 hitting one of them is not surprising. Either embed or remove the remark.

### M6. The Monte Carlo significance claim ($Z = 21.3$, $p < 10^{-50}$) cannot be evaluated

§7 reports: "*The Monte Carlo significance of the full HARMONY count $\mathrm{HARM}(T) = 73$ alone, against $200{,}000$ random tables with the same row/column constraints, is $Z = 21.3$, $p < 10^{-50}$.*" The reference for this is again [Sanders2026CLAxioms], in preparation. What "same row/column constraints" means is not specified — uniform random Latin square? Random commutative magma? Random table with VOID-absorbing column? Each of these gives a different null distribution and a different Z-score. Without the specification of the null model, the significance claim is unfalsifiable.

**Fix:** Either specify the null model and recompute the Z-score in this paper, or remove the claim. As stated it is filler.

### M7. The "second ladder" at $\{28, 36, 44\}$ does not belong

§6 records three companion HARMONY counts and asserts each appears at "two structurally distinct roles." The proofs are deferred. The companion ladder is not part of the headline claim, has no proof in this paper, and dilutes the paper's focus. JCT-A would prefer a tighter paper on the four rungs alone, or a separate paper on the (28, 36, 44) cluster. **Fix:** Remove §6 or move to a remark indicating the companion ladder will be the subject of separate work.

### M8. The theorem-numbering scheme is inconsistent

The paper uses `\newtheorem{theorem}{Theorem}[section]`, but theorems are referenced both as "Theorem 1.1" (in the Introduction abstract paragraph) and as "Theorem 3.1" / "Theorem 4.2" / etc. Theorems 1.1 in the Introduction is just a forward reference; that is fine but the numbering should be updated so the Introduction's preview matches the body. Currently "Theorem 1.1 (= ...)" is jarring. **Fix:** Re-number consistently or use unnumbered theorem statements in the Introduction.

---

## §5 — Minor comments

- **m1** (line 38, Introduction). "Combinatorial substrates over small finite cyclic groups occasionally exhibit clusters..." — the word "occasionally" is doing too much work. There are few published examples of integer-clustering as a substrate-identification tool; the reader needs an example or two cited here, otherwise the framing reads as motivational rather than scholarly.

- **m2** (§2.2 / various). The author uses "TSML" and "BHML" as opaque acronyms throughout. JCT-A readers will not have prior context. **Fix:** Spell out at first use ("the TSML table $T$ — for *Trinity Synthesis Magma Lattice*, ..." or whatever the etymology is) or, preferably, drop the acronyms entirely in favor of $T$ and $B$ (which the paper already uses in the math).

- **m3** (§2, axiom set). The axioms are numbered A1–A4 in the proof of shared axioms and A1–A9 in §1's introduction. The numbering should be consistent within the paper and aligned with the cited [Sanders2026CLAxioms].

- **m4** (Theorem 3.1, ECHO pairs list). The list in the proof contains 10 pairs; the reader cannot verify these are pairwise disjoint without the table. Insert the table before the theorem.

- **m5** (Remark 4.4, "three unrelated algebras pointing at the same integer is the algebraic shape of a real invariant"). This is a philosophical claim, not a mathematical one. JCT-A's prose should stay closer to the math. **Fix:** Replace with a precise statement of independence (formalize "independent constructions" and verify the relation).

- **m6** (§5, "structural reading as a four-step descent"). The "descent" framing is editorializing. The four integers happen to be consecutive, but neither the paper nor a referee can see a *function* mapping one to the next. JCT-A's prose convention prefers neutral statements. **Fix:** Replace "the descent reflects the dominance of the HARMONY axis" with "the four integers happen to be consecutive; we have no structural argument linking them."

- **m7** (§5, paragraph "What becomes plain only when all four are held together"). This sentence is the manuscript's most exposed flank. As argued in Major M2, two of the four rungs are inclusion-exclusion consequences. The paragraph should be rewritten to match the actual mathematical content (lens-disagreement + YM-core determinant + a Galois-prime conjecture).

- **m8** (Bibliography). All citations to companion papers are "in preparation." JCT-A requires arXiv-or-published material at submission for any citation that is load-bearing. **Fix:** Either deposit the companions on arXiv before submission, or rephrase the manuscript to be self-contained.

- **m9** (Bibliography \cite{FultonHarris1991}, \cite{Bourbaki1968}). These are cited but no specific result from them is used. Remove or attach to a specific use.

- **m10** (Cover letter). The cover letter is well-crafted but mentions companion papers (J05, J02) as "submitted" — JCT-A editors will check status and any of these being merely "in preparation" rather than submitted will undermine the timing of the chain.

---

## §6 — Literature

The paper does not cite any external literature on integer invariants of finite magmas, Latin-square-related discrete structures, sub-magma chains, or coincidence-of-prime phenomena. JCT-A would expect at least the following placed as context:

- **Latin square / quasigroup combinatorics.** Wanless and others have catalogues of Latin squares with prescribed properties; any "the integer 73 is unusual" claim should be benchmarked against the relevant combinatorial-design literature (e.g., Colbourn & Dinitz, *Handbook of Combinatorial Designs*).
- **Discriminants of small-degree number fields and the LMFDB.** The LMFDB is cited via the label $4.2.10224.1$ but the LMFDB itself is not cited in the bibliography. Add LMFDB as a citation: "*The LMFDB Collaboration, The L-functions and modular forms database*, https://www.lmfdb.org" with access date.
- **Coincidences vs identities in algebraic combinatorics.** The paper's central methodological move — declaring that three constructions hitting the same integer constitutes a structural invariant — has antecedents (Monstrous Moonshine being the canonical example). Citing the relevant literature on "what counts as a coincidence vs an identity in combinatorics" would strengthen the prose around the triple-coincidence claim and also reduce the reviewer's instinctive skepticism.
- **The $E_6$ root system.** If retained, the $|E_6^+| = 72$ remark needs a citation — Bourbaki, *Groupes et algèbres de Lie*, or a modern Lie theory text.
- **Yang–Mills / 4-form combinatorics on $\mathbb{R}^8$.** If the YM-core terminology is retained, $\binom{8}{4} = 70$ as the dimension of the self-dual 4-form representation requires a representation-theory citation (Adams, *Lectures on Lie Groups*, or Fulton–Harris).

The paper also has zero engagement with the broader question of *what makes an invariant on a small finite substrate "real" vs "coincidental."* The methodological move from "three constructions agree on an integer" to "this is a structural invariant of the substrate" is the heart of the paper's epistemology. Without engaging with prior literature on this question, the paper's framing reads as untested.

---

## §7 — Revision effort

To bring this manuscript to JCT-A's bar:

| Task | Effort |
|------|--------|
| Add the explicit $T$ and $B$ matrices in §2 (12 lines each) | 1 hour |
| Add LMFDB and Latin-square references | 2 hours |
| Verify or remove the third leg of the triple coincidence (the Galois prime); display the actual attractor minimal polynomial and its discriminant; confirm LMFDB identification | 1–2 days (this is the load-bearing fix) |
| Either deposit [Sanders2026Attractor] companion on arXiv or rewrite the third-leg theorem as a Conjecture | 1 day if depositing |
| Re-frame "four independent constructions" → "two independent constructions plus inclusion-exclusion consequences plus a Galois conjecture" | 4 hours of writing |
| Remove or embed the $E_6$ coincidence remark | 1 hour |
| Drop the "Yang–Mills" terminology or establish the YM connection | 1 hour to drop / 1 week to establish |
| Drop the "second ladder" at $\{28, 36, 44\}$ or split into a separate paper | 1 hour |
| Specify or remove the Monte Carlo significance claim | 4 hours (depends on null-model definition) |
| Bundle the four verification scripts into the manuscript folder | 30 minutes |
| Re-do the abstract / introduction to match the revised content | 1 day |
| **Total** | ~1 week if the Galois leg works; ~2 weeks if it requires non-trivial computation |

**Recommendation:** Resubmit after revision. The core observation is solid (lens-disagreement = sub-magma HARMONY = 71 on a fixed substrate is a non-trivial coincidence at machine precision), and the Yang–Mills determinant rung adds a pleasing companion. But the headline as currently stated is over-promised, and the verification trail does not support submission. With the revisions above, the paper becomes a tight short note with clearly-bounded claims.

---

## §8 — Venue bar

**JCT-A's bar for combinatorial-algebra short notes.** JCT-A publishes high-quality, fully self-contained papers on combinatorial structures with proofs, well-defined invariants, clear independence claims, and explicit benchmarking against generic null hypotheses. Papers of this length (15-20 pages) are expected to either:
- Establish a structural theorem with a complete proof, or
- Establish a tight integer-clustering observation with both (i) an explicit null distribution and (ii) verification that the observation is not generic.

The current manuscript is closer to the second category, but neither (i) nor (ii) is currently met.

**My estimate of the manuscript's actual fit.** With revisions M1, M2, M5, M6, M7 and resolution of the Galois-prime question, this paper would be a respectable Tier-B short note for JCT-A. The "triple coincidence at 71 (verified)" with two genuinely independent constructions plus a third Galois-prime construction (if proved) on a fixed $10 \times 10$ matrix substrate is a genuinely interesting observation and would fit JCT-A's section on "explicit invariants of small combinatorial structures."

If the Galois-prime leg cannot be established, the paper drops to a "double coincidence" — still publishable but at a venue with a softer bar (e.g., *Discrete Mathematics*, *European Journal of Combinatorics*, or as an arXiv-only note).

**Comparison to recent JCT-A acceptances.** Recent JCT-A papers on small-substrate-invariant questions typically include null-model benchmarking, an explicit independence proof (or counterexample), and citation to at least 2–3 prior works on the same combinatorial substrate. This paper has none of those at present.

**Final recommendation.** Reject in current form, invite resubmission after substantial revision per §7. The mathematical core is there; the paper as written sells the core for more than it currently can deliver.

---

**Reviewer signature.** External anonymous referee (fresh-eyes, no prior contact with author or with author's research program).
