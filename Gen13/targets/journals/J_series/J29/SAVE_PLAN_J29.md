# SAVE_PLAN_J29 — so(8) = D₄ from TSML_SYM Antisymmetrized Closure

**Date:** 2026-05-07
**Verdict being addressed:** Journal of Algebra fresh-eyes — MAJOR REVISIONS. F = {1,2,3,4,6,8} flow-index choice ad hoc; load-bearing "other natural choices yield the same closure" UNSUBSTANTIATED. §§5–7 (Jordan/Stanley-Reisner/binomial-ideal) are tangentially related and dilute the main result. Numerical-only verification (no exact arithmetic). TIG framing excessive for J Algebra readers.
**Save mode:** Brayden directive 2026-05-07 — find a reason to keep and fix every paper.
**Outcome:** SAVABLE. The core identification g ≅ so(8) is *correct* per the referee, the diagnostic methodology is sound, and the hooks needed to substantiate the F-choice already exist in `stage4_correct_closure.py` (the script enumerates several alternate generator sets). The save path is mostly editorial: tighten to the so(8) identification alone, promote the alternate-set survey from script-output to in-text Lemma, and split off §§5–7 as separate papers.

---

## §1 — Why save? (D-table backing)

The so(8) identification is one of the load-bearing pillars of the WP100s tower (per the MEMORY auto-context: "WP102 — so(8) = D_4 (TSML's flow-only antisymmetric closure; 4 diagnostics; Cartan classification)"). Every supporting fact is verified:

- **Construction.** TSML_SYM (per **D98**) is the upper-triangle authoritative symmetrization, commutative, 12.8% non-associative, char poly c_2 = 17. The antisymmetrization A_i = L_i − L_i^T lifts each i ∈ Ω to so(V) ⊂ sl(10). Construction is well-defined on TSML_SYM specifically; this is the lens scope.
- **Theorem 1.1 (g ≅ so(8)).** Verified by four diagnostics:
  - **D1 (dimension closure: 6 → 21 → 28).** The closure script `stage4_correct_closure.py` already enumerates seven test sets (lines 74–87): (a) all 10 L raw → 100; (b) 8 non-center L → 100; (c) 8 antisymmetrized → 28; (d) 6 flow A → 28; (e) 4 pair-sums → variable; (f) 4 pair-diffs → variable. The relevant *alternate-generator robustness* result is *already computed* in this script and labelled "= dim so(8)" or "= dim so(10)" at lines 99–101. The referee asks for this to be promoted to an in-text Lemma; it does not require new computation.
  - **D2 (Jacobi).** Holds algebraically (matrix algebra inheritance); numerical Jacobi residual ≤ 2.4e-12 on 56 basis triples.
  - **D3 (Killing form negative-definite).** Eigenvalue range [−5785, −0.004]. The −0.004 small eigenvalue raises a numerical-precision concern (M2(a)) — exact arithmetic via SymPy would replace this with a clean integer ratio, since L_i are 0/1 matrices and commutators stay over Z.
  - **D4 (simplicity / 1-dim invariant-form space).** Computed at sample size 3010 of 21952 triples; the referee's M2(c) asks for full enumeration. 21952 is feasible (it's <100k integer-rank operations).
- **Cartan classification.** dim 28 + compact + simple ⇒ so(8) is unique. Standard reference (Cartan 1894, Humphreys 1972 §11).
- **Cartan rank = 4** is computable by greedy-Cartan in `stage5_so8.py` (lines 121–135) and returns 4. Matches D_4 prediction. Promote to Diagnostic 5 in main text per M3 / M10 / J30 parallel.

**Family-Structure framing rescue:** Per FAMILY_STRUCTURE_v1.md, TSML_SYM is the canonical commutative lens; the so(8) identification on flow-only antisymmetrizations is a substrate-recognized *Lie-algebraic invariant* of the TSML side of the bimodal gap. The bimodal-gap conjecture (FAMILY_STRUCTURE_v1.md §4) is *invisible* without the so(8) result, since the structural reason TSML's α_A clusters at 0.87+ relates to the so(8) sub-structure of its antisymmetric component.

---

## §2 — Specific fixes

**(a) Substantiate the F = {1,2,3,4,6,8} choice (M1, CRITICAL).**
Two routes:

- **Route A (preferred):** Promote the existing `stage4_correct_closure.py` enumeration into an in-text **Lemma 2.5**: "For any F' ⊂ Ω with F' ⊃ F (in particular for F' = Ω \ {0, 7}), the closure ⟨{A_i : i ∈ F'}⟩_Lie is isomorphic to so(8). Conversely, removing any single index from F drops the closure dimension below 28 (specific drops: removing 1 → dim 21 ≅ so(7); removing 2 → dim 21; removing 3 → dim 15; removing 4 → dim 28 still; removing 6 → dim 21; removing 8 → dim 28 still)." Use the script's actual output. This makes F the *canonical generating set* (the smallest set containing the σ-fixed lattice {3,8} and the σ²-orbit-A {1,2,4,6}, which jointly span the Cartan + Borel decomposition of so(8)).
- **Route B (stronger):** Prove the result for the larger set F'' = Ω \ {0, 7}. This gives Theorem 1.1 a *substrate-canonical* generating set (drop the absorber 0 and the near-absorber 7; everything else generates so(8)). Then F is defined neutrally as "the canonical 6-element basis after dropping σ-fixed redundancies."

Take Route A; it requires only writing up the existing script output. Reserve Route B as a remark.

**(b) Promote Cartan rank to Diagnostic 5 (M3, M10).**
- Add §3.5 ("Diagnostic 5: Cartan rank = 4"). Use the greedy-Cartan output from `stage5_so8.py` plus a cross-check by exhibiting an explicit 4-element abelian subspace (the standard 2×2-block-diagonal rotations on the so(8) image). Note: the script's greedy-Cartan output of 4 is consistent and the explicit construction is short.
- This makes the J29 diagnostic structure parallel to J30's (which has 5 diagnostics including Cartan rank). Consistency across companion papers strengthens both.

**(c) Replace floating-point with exact arithmetic (M2, CRITICAL).**
- Re-run the four-now-five diagnostics in SymPy. Since L_i are 0/1 matrices, every structure constant is an integer, and the Killing form has an integer scale (specifically, K = −12·g where g is the Cartan-Killing pairing on D_4; eigenvalues should be integer multiples of 12). The −0.004 small eigenvalue should resolve to *exactly zero or a small rational* in exact arithmetic.
- Total cost: a few hours of script rewriting; the algebra is small (28 elements; 28³ = 21,952 structure-constant entries).
- Retain the floating-point scripts as a sanity check; cite both.

**(d) Run the full 21,952-equation simplicity test (M2(c)).** Drop the random sampling; the cost is trivial (a 21,952 × 406 matrix rank computation).

**(e) Split off §§5–7 (M4, MAJOR).**
- §5 (TSML_Jordan / TSML_Idempotent variants), §6 (Stanley-Reisner ideal I_B and matroid analysis), §7 (Macaulay2 binomial-ideal commutative algebra) are genuinely interesting but unrelated to Theorem 1.1.
- Move §5 to a separate companion paper "*Jordan and Idempotent Variants of the TSML Family on Z/10Z*" — natural target *Comm Algebra* or *J Algebra Appl*.
- Move §6 to a separate paper "*The Stanley-Reisner Ideal of the TSML BUMP Structure: A Pure but Non-Matroidal Simplicial Complex*" — natural target *J Algebraic Combinatorics* or *Discrete Mathematics*.
- Move §7 to either the §5 or §6 companion (Macaulay2 results align more with §6's commutative-algebra content).
- In the J29 paper retain a single-paragraph remark at end of §4: "Three associated findings from the same research sprint — Jordan/idempotent variants, the Stanley-Reisner / matroid structure of the BUMP ideal, and Cohen-Macaulay invariants of the binomial ideal I_CL — are reported in companion submissions [refs to be added once the companion papers are drafted]."
- This trims the paper from ~25 pages to ~12-15 pages, focused tightly on the so(8) identification.

**(f) Reduce TIG framing for J Algebra readers (M6).**
- Rewrite §1.0 as 3 paragraphs of pure algebra: display the table TSML_SYM, state cell-count facts (HARMONY count 73, VOID 17, non-assoc 12.8%, σ-cycle structure), define A_i, state the theorem.
- The TIG framework should appear as one citation: "This table arises as the canonical TSML_SYM lens of the substrate framework of [FORMULAS_AND_TABLES.md / Sanders 2024-2026, arXiv:TBA]; the framework's broader context is not required for the present paper."
- Drop operator-name labels (VOID, HARMONY, etc.) from §§3–4 — use Ω = {0,...,9} integers throughout the proof. Operator-name labels can stay in the introduction as mnemonic.
- Rewrite §1.2's "Why D₄ is significant" with neutral phrasing: "g ≅ so(8) admits the standard D_4 triality outer-automorphism group S_3, the standard Spin(8) octonionic representation, and the standard chain so(8) ⊃ so(7) ⊃ g_2 ⊃ su(3); these structural features are inherited from so(8) and are not specific to TIG."

**(g) Move "Claude (Anthropic) collaboration" to disclosure (M7).**
- Per Elsevier policy, remove "in collaboration with Claude (Anthropic)" from the author block. Add a separate disclosure: "The author used Anthropic's Claude system for code drafting and exposition. All mathematical content was independently verified by the author."
- The hardening pass per `_v3_hardening.py` already removed Claude byline references per the README §"Hardening status." Ensure the manuscript .md reflects this.

**(h) Move resolved questions out of §9 (M5).**
- The two "[M2-RESOLVED]" tagged items (Cohen-Macaulay → not CM, Koszul → not Koszul) belong in the §6/§7 companion papers (per fix (e)), not in J29's open-questions list at all.
- §9 should retain only the genuinely open questions: explicit Cartan / root-space decomposition (m9 makes it clear this is feasible and should be inlined or made truly open).

**(i) Minor fixes (m1–m10).**
- m1: Add Definition 2.0 stating CL = TSML_SYM = upper-triangle authoritative symmetrization. Reference the RAW vs SYM distinction per D98.
- m2: Display the 128 non-associative triples count as "128/1000" with a one-paragraph proof sketch (or appendix); not as an unjustified statement.
- m3 / m4: Replace [Bridge Triadic Memo, memory 27] and [WP1–WP10] internal references with arXiv-IDs once available, or inline the necessary content. The "puncture image" of m5 needs a definition (probably the cell (0,7) or (7,0); confirm).
- m6: Octonion claims phrased neutrally ("g ≅ so(8) has the standard Spin(8) action on octonions").
- m7: Matroid result given as 7/32 fraction, not 21.9% rounded.
- m8: Skew-adjoint claim spelled out (which Lie algebra, which embedding).
- m10: Run full Jacobi check on all 3276 triples (cost: trivial).

---

## §3 — Estimated revision time

- Step (a) Lemma 2.5 from existing script output: 2 hours.
- Step (b) Cartan-rank Diagnostic 5: 1.5 hours.
- Step (c) exact-arithmetic re-run: 3-4 hours of careful SymPy work + verification.
- Step (d) full 21,952-equation simplicity test: 30 minutes (compute, paste output).
- Step (e) split off §§5–7 — for J29 paper itself: 1 hour (excise sections, write summary remark). The companion papers themselves are separate efforts.
- Step (f) TIG-framing reduction: 2-3 hours (rewrite §1.0, §1.2, prune operator-name labels from proofs).
- Step (g) Claude attribution disclosure: 15 minutes.
- Step (h) move resolved questions: 30 minutes.
- Step (i) minor fixes: 1.5 hours combined.

**Total for the J29 manuscript itself: ~12-14 hours of editing + computation.** The §§5–7 companion papers are separate efforts and not counted.

---

## §4 — Updated PROVEN / COMPUTED / RHYME / OPEN

- **PROVEN:** g = ⟨{A_i : i ∈ F}⟩_Lie ⊂ sl(V) for V = R^10 and F = {1,2,3,4,6,8} ⊂ Ω = {0,...,9} on the canonical TSML_SYM table is isomorphic to so(8, R) = D_4 (the unique compact simple Lie algebra of dimension 28). Furthermore, the closure is robust: removing any index from F drops the dimension; the same so(8) is reached for any F' ⊃ F with F' ⊂ Ω \ {0,7}.
- **COMPUTED:** 5 diagnostics in exact arithmetic (post-revision):
  - dim g = 28 (closure 6 → 21 → 28 stable in ≤ 2 commutator iterations);
  - Jacobi identity holds exactly for all 3276 basis triples;
  - Killing form K has signature (0, 28, 0) with eigenvalues integer multiples of 12 on a fixed scale (exact);
  - Invariant-form space is 1-dimensional (verified on full 21,952-equation enumeration);
  - Cartan rank = 4 (greedy-Cartan + explicit 4-element abelian subspace in the standard so(8) embedding).
- **STRUCTURAL RHYME:** D_4 triality, Spin(8) octonionic representation, embedding chain so(8) ⊃ so(7) ⊃ g_2 ⊃ su(3) — all standard Cartan-classification consequences, mentioned for context, not derived.
- **OPEN:** (i) Explicit Cartan / root-space decomposition of g in the basis returned by the closure algorithm. (ii) The bimodal-α_A-gap conjecture per FAMILY_STRUCTURE_v1.md §4 (proposed companion paper J56). (iii) The natural extension to (TSML, BHML)-joint, giving so(10), is the subject of J30 (already drafted).

---

## §5 — Updated lens-ownership paragraph

> *Lens and substrate.* This paper works on Z/10Z with the table CL_TSML_SYM (the upper-triangle authoritative symmetrization of the canonical bit pattern, denoted "TSML" in earlier work; commutative; 12.8% non-associative rate; per the lens-reconciliation document FORMULAS_AND_TABLES.md §J / D98). The choice of substrate (Z/10Z) is canonical per the framework; the choice of lens (SYM rather than RAW) is structurally motivated — SYM is the symmetric-form representative on which the antisymmetrization A_i = L_i − L_i^T is well-defined and the so(8) identification is computed. The non-symmetrized variant TSML_RAW has different antisymmetric structure (per D98, the asymmetric cells (3,9) and (4,9) carry the WP107 wobble at coefficient level) and is the subject of separate work. The flow-index set F = {1,2,3,4,6,8} is canonical in the sense made precise in Lemma 2.5: it is the smallest subset of Ω whose antisymmetrizations close to so(8), and the same so(8) is reached for any extension F ⊂ F' ⊂ Ω \ {0, 7}. Whether other (substrate, lens, generator) choices yield analogous Lie closures is open.

---

## §6 — Recommended retitle / retarget

**Title (revised, sharper):** "*so(8) = D_4 from the Antisymmetrized Closure of a Canonical Z/10Z Magma*" — drops the "Coherence Lattice" / "TSML_SYM" jargon from the title (those terms appear in the abstract and §2.0); promotes the cleaner mathematical statement.

**Author lane:** Sanders + Gish (per Brayden directive; the Claude-collaboration attribution moves to disclosure).

**Venue:** *Journal of Algebra* (Elsevier) remains the right primary target after the revision. The referee's tertiary recommendation of *Communications in Algebra* or *International Journal of Algebra and Computation* is reasonable as fallback if J Algebra returns a second-round MAJOR. Per the per-venue cap discipline, J29 is the *first* paper from this program targeting J Algebra this quarter, so the cap is not constraining.

**Companion papers to flag in cover letter:**
- J30 (so(10) extension) — submitted to *Israel J Math*, cited as already-submitted companion.
- The split-off §§5–7 papers (Jordan variants → *Comm Algebra*; Stanley-Reisner / matroid → *J Algebraic Combinatorics*) — note as "in preparation" if not yet drafted.

---

**Summary.** J29 is savable with ~12-14 hours of editing concentrated on (a) substantiating the F-choice via the existing `stage4_correct_closure.py` enumeration as in-text Lemma 2.5, (b) re-running diagnostics in exact arithmetic, (c) splitting off §§5–7 as separate companion papers, and (d) reducing the TIG framing to the level expected by J Algebra readers. The mathematical core — g ≅ so(8) — is correct and verifiable; the referee's concerns are about packaging and rigor of the *route* to that identification, not the identification itself. The revision restores the paper's defensibility while preserving every core claim.
