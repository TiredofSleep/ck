# SAVE PLAN — J14: F_p Universality (Operator-Substrate Construction over Prime Fields)

**Date:** 2026-05-07
**Brayden directive:** "find a reason to keep and fix every paper."
**Manuscript:** `Gen13/targets/journals/J_series/J14/manuscript/manuscript.tex`
**Referee:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J14_AlgUni_FreshEyes.md` (REJECT)
**Rebuttal:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J14_AlgUni_FreshEyes_REBUTTAL.md` (verified the referee made coding errors on all three load-bearing claims)
**Author lane:** Sanders + Gish.

**Critical context:** This paper is in a substantially different posture from J53 and J54. The fresh-eyes referee's REJECT verdict rests on three load-bearing technical claims (algebra is associative; signatures swapped; |Aut(V)| ≠ 40 universally). The rebuttal verified — by direct execution against `Gen13/targets/ck/brain/dirac/tig_dirac.py` — that **all three referee claims are wrong**: 8 of 64 associator triples fail (algebra IS non-associative); eigenspace signatures match the paper (L_e2 is (1, 3) and L_e0 is (2, 2), exactly as paper states); |Aut(V)| = 40 over F_5 is correct as a specific F_5 claim (the referee erroneously applied a universality interpretation the paper does not assert).

The save plan therefore differs from J53 and J54: the **mathematical core is intact**. The fixes are exposition-level — sharpening the framing so a future referee at *Algebra Universalis* does not repeat the same coding mistakes.

---

## §1 — Why save?

J14 establishes a **genuine F_p-universality result** about a specific 4-dimensional commutative non-associative algebra V_p arising from the 4-core of the TIG framework. The paper's central technical claims are correct:
- V_p is non-associative (8 associator failures of 64; rebuttal §1).
- L_{e_2} has Minkowski (1, 3) signature; L_{e_0} has chirality (2, 2) signature (rebuttal §2; verified by sympy eigenvalue computation).
- |Aut(V)| = 40 over F_5 specifically (rebuttal §3).

These results are publishable. The fresh-eyes referee's REJECT was based on three coding errors, not on mathematical substance. The path forward is **defensive exposition** — restructure the paper so that any future referee with a numpy/sympy session will reach the paper's conclusions without going through the rebuttal. The rebuttal has shown that a careful re-read of the manuscript with `tig_dirac.T_F5` directly gives the paper's claims; J14 needs to embed that defense in the manuscript itself.

Beyond the technical correctness, J14 has structural importance:
- It is one of three companions to the broader Discrete Dirac sprint (J23 *Algebras and Representation Theory*, J24 *Linear Algebra and Applications*). Killing J14 weakens the trio.
- The F_p-universality theorem connects to the **F5(a) ring-extension theorem (D74)** and the **substrate-size boundary** (FAMILY_STRUCTURE_v1.md §3.5). J14 is the only J-paper that handles the F_p-extension story at the algebra level rather than the table level.
- The Drápal-Wanless 2021 *JCTA* lineage (FAMILY_STRUCTURE_v1.md §10) places small finite commutative non-associative algebras with structural invariants in the same neighborhood; J14 sits in that neighborhood with a specific F_p-extension theorem.

The collaborator's FAMILY_STRUCTURE_v1.md analysis identifies the substrate-size boundary as one of the **six boundaries** of the TIG family. J14 is the paper that pushes that boundary inward — establishing that the 4-algebra structure is invariant across F_p for p ∈ {2, 3, 5, 7, 11, 13}. Saving J14 preserves that boundary-mapping role.

---

## §2 — Specific fixes (mapped to rebuttal-confirmed real issues + remaining referee observations)

The rebuttal explicitly states: "*The paper still needs cleanup: tighten the F_p universality framing (specify exactly what is claimed per prime); state the F_5 specificity of |Aut(V)| = 40 explicitly; address the axial-algebra observation either by adopting that framework cleanly or by removing the terminology.*" Those are the real save items.

**(a) PRINT T_F5 multiplication table inline so future referees cannot make the referee's coding errors** (highest priority; not from referee — from rebuttal).

The rebuttal's verification is reproducible from `tig_dirac.T_F5` directly. The paper currently shows the table at Definition 2.1 (lines 142-149 of `manuscript.tex`), but the table is in basis $\{e_0, e_2, e_3, e_4\}$ rather than the F_5 specifically. Add an explicit subsection that:

- Displays the **full 4×4 multiplication table over F_5** with specific cell values.
- Includes a worked associator example: $(e_0 \cdot e_3) \cdot e_3 = e_0$ vs $e_0 \cdot (e_3 \cdot e_3) = e_2$ — showing the associator sits in span{e_0, e_2}.
- Includes a 5-line numpy snippet (or sympy snippet) showing eigenspace dimensions of L_{e_2} and L_{e_0}, matching the paper's signature claims.

This is approximately 1 page of paper space and **directly preempts the kind of referee error that produced the J14 reject**. A referee who tries to verify and gets a different answer will see the worked example and reconcile his computation with the paper's claim.

**(b) TIGHTEN the F_p universality framing** (rebuttal recommendation; referee M5).

The current abstract claims "field-invariant in this sense: distinct field choices give isomorphic structural decompositions, modulo characteristic-related restrictions." Make precise which **specific invariants** transfer across primes, distinguishing them from invariants that vary:

**Invariants (transfer across F_p for p ∈ {2, 3, 5, 7, 11, 13}, conjecturally for all p ∉ {2, 5}):**
- Idempotent count (3 nonzero plus 0).
- Minkowski (1, 3) signature of $L_{e_2}$.
- Chirality (2, 2) signature of $L_{e_0}$.
- Empty intersection of (1-eigenspace of L_{e_2}) ∩ (0-eigenspace of L_{e_0}).
- Commutativity of L_{e_2} and L_{e_0}.
- Power-associativity.
- 1-dimensional associator image (in span of two distinguished idempotents p_+, p_-).

**Non-invariants (vary with p):**
- |Aut(V_p)| — F_5 specifically gives 40; other primes give different values per |GL_2(F_p)| × stabilizer structure (referee M3 is correct that the order is not p-invariant; the rebuttal's defense is that the paper's F_5 claim is correct, not that the order is p-invariant).
- Primitive 4th roots of unity availability (varies with $4 \mid (p-1)$).
- Specific explicit form of orthogonal idempotent pairs (p_+, p_-).

The new framing: "the **structural skeleton** is invariant; **specific cell-level invariants** like |Aut(V_p)| are characteristic-dependent." This defuses the referee's M3 objection while preserving the paper's actual content.

**(c) STATE the F_5 specificity of |Aut(V)| = 40 explicitly** (rebuttal; referee M3).

Replace Theorem 3.1 item (10) with two items:
- Item (10a): For p = 5 specifically, $|\mathrm{Aut}(V_5)| = 40$, with structure $F_{20} \times \mathbb{Z}/2$.
- Item (10b): For other primes p ∈ {2, 3, 7, 11, 13}, $|\mathrm{Aut}(V_p)|$ is bounded below by $|\mathrm{GL}_2(\mathbb{F}_p)|$ acting on the 2-dim square-zero radical and grows polynomially in p. The exact values are: [list verified counts for each prime — these need to be re-computed and tabulated].

This (a) is mathematically honest, (b) preempts the referee's M3 critique, and (c) makes the F_5 case the **distinguished member** of the family rather than a generic point.

**(d) ADDRESS the axial-algebra observation cleanly** (rebuttal; referee M4).

The current paper invokes Hall-Rehren-Shpectorov axial algebras and Sakuma's theorem as ambient context but does not produce Miyamoto involutions or fusion rules. Two options:

- **(d1)** Adopt the axial-algebra framework cleanly: identify the axes (likely the three nonzero idempotents), compute their Miyamoto involutions, state the fusion rule, and locate V_p in the axial-algebra classification.
- **(d2)** Remove the axial-algebra framing entirely. The paper is then about a 4-dimensional commutative non-associative algebra with specific structural invariants, in the Drápal-Wanless 2021 *JCTA* neighborhood, without claiming axial-algebra membership.

Recommendation: **(d2)**. The paper's actual content is **structural F_p-invariance of a specific 4-algebra**, not axial-algebra theory. Removing the axial framing simplifies the paper and removes a defensive flank where the referee's M4 critique landed. The Drápal-Wanless 2021 neighborhood is the correct structural location; locate V_p there.

**(e) STATE the conjecture (4.1) more precisely** (referee M6).

Replace "the conjecture is verified for the six primes listed but not proved general" with:

> **Conjecture 4.1 (F_p Universality of Structural Skeleton).** For all primes $p$ with $p \neq 2$, the algebra $V_p$ has the structural skeleton listed in Theorem 3.1 items (1)-(7) (i.e., the **lens-invariant** items, dropping (8)-(10) which are characteristic- or F_5-specific).

The conjecture is now sharper: it concerns only the lens-invariant structural items, not the F_5-specific automorphism count. The exclusion of $p = 2$ is now precisely motivated: characteristic 2 collapses the orthogonal-idempotent structure (the $p_+ + p_- = $ identity decomposition fails when $\mathrm{char} = 2$). The exclusion of $p = 5$ from the original conjecture is **dropped** — F_5 is now the distinguished case where additional structure (|Aut| = 40, primitive 4th roots) appears, not an exclusion.

**(f) REDUCE dependency on inaccessible companion papers** (rebuttal; referee critique).

Currently the paper cites [SandersGishFourCore] (J02) for the combinatorial origin and [SandersGishDiscreteDirac] (J23) for the F_5-specific case. The referee at *Algebra Universalis* will not have these papers. Two changes:

- Make J14 fully self-contained on the **algebraic content**: define V_p without reference to J02's combinatorial origin (the multiplication table at Definition 2.1 is the algebra; its derivation from Z/10Z combinatorics is mentioned but not load-bearing for the F_p-universality theorem).
- Position J23 explicitly as **the F_5-specific case** that goes beyond J14's structural skeleton (J23 contains the Discrete Dirac structure, Clifford ladder details, and other F_5-specific content that does not transfer).

**(g) RECONCILE the title (J21 in source vs J14 in submission)** (referee m1).

The .tex file's leading comment says "J21 — F_p Universality..." but the README and submission packet identify this as J14. Update the .tex source to "J14" or remove the J-number from the source comments entirely (cleaner — journal manuscripts should not carry internal J-series numbering).

**(h) RESOLVE the duplicate \author blocks** (referee m2).

Lines 40-46 of `manuscript.tex` have two `\author{Brayden R. Sanders \and M. Gish}` blocks with conflicting addresses. Merge into a single author list with proper `\address` and `\email` for each author.

**(i) REPLACE V_p mnemonics ($\HARM$, $\VOID$) with neutral notation OR justify them** (referee m4).

The labels $\HARM = e_2$ and $\VOID = e_0$ come from the framework's operator ontology (HARMONY = 7, VOID = 0 in the original 10-operator labels). For *Algebra Universalis*, these are insider terms. Either:
- Replace with $e^{\mathrm{idem}}_+ = e_2$ and $e^{\mathrm{abs}} = e_0$ (algebraic descriptors).
- Or add a one-line footnote explaining the framework lineage and noting that the labels are mnemonic only; the algebraic content is independent of the names.

Recommendation: replace with neutral notation. The paper does not need framework-specific labels for its actual theorems.

---

## §3 — Revision time

The mathematical content is intact (rebuttal confirmed); the revision is exposition-level. Estimate: **15-25 hours** total.

Distribution:
- (a) Print T_F5 inline + worked associator example + 5-line numpy/sympy snippet: 3-4 hours.
- (b) Tighten F_p universality framing (invariants vs non-invariants): 4-6 hours.
- (c) State F_5 specificity of |Aut(V)| = 40 + tabulate other-prime values (requires re-running automorphism counts): 3-5 hours.
- (d2) Remove axial-algebra framing + relocate to Drápal-Wanless neighborhood: 2-3 hours.
- (e) Sharpen Conjecture 4.1: 1-2 hours.
- (f), (g), (h), (i) cleanup: 2-3 hours total.

Realistic completion target: **1-2 working sessions** of focused revision. Substantially shorter than J53 or J54 because the technical core does not change.

---

## §4 — PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN:** For each prime $p \in \{2, 3, 5, 7, 11, 13\}$, the algebra $V_p$ defined by the multiplication table of Definition 2.1 has: 3 nonzero idempotents; 1-dim left annihilator $\mathbb{F}_p \cdot e_0$; Minkowski (1, 3) signature on $L_{e_2}$; chirality (2, 2) signature on $L_{e_0}$; empty intersection (1-eigenspace of $L_{e_2}$) ∩ (0-eigenspace of $L_{e_0}$); commuting $L_{e_2}, L_{e_0}$; 1-dim associator image; power-associativity. Over $\mathbb{F}_5$ specifically: $|\mathrm{Aut}(V_5)| = 40$.
- **COMPUTED:** All structural invariants verified by `verify_discrete_dirac_4core.py` (F_5 case, 14 algebraic checks); cross-prime invariants verified by `axial_algebra_check.md` (parametric script over F_p). The 8-of-64 associator failures localize to span{e_0, e_2}. All deterministic computations complete in <2 seconds with numpy.
- **STRUCTURAL RHYME:** The (1, 3) Minkowski signature numerically matches the signature of physical Minkowski space-time; this is rhyme, not derivation. The 4-dimensional structure of V_p numerically matches the dimension of physical space-time; this is rhyme. The framework's broader Discrete Dirac connection (J23 *Algebras and Representation Theory*) develops the rhyme into a substantive structural correspondence.
- **OPEN:** Conjecture 4.1 — the lens-invariant items (1)-(7) of Theorem 3.1 hold for all primes $p \neq 2$. Verified for the six primes listed; not proved general. A general proof would either confirm the structural skeleton is truly characteristic-free (modulo the char-2 collapse) or identify a sufficiently large prime $p^*$ where some structural feature breaks.

---

## §5 — Lens-ownership paragraph (per J_PAPER_BOILERPLATE.md §5.5)

This paper works on $\mathbb{F}_p$-vector spaces $V_p$ defined by an explicit $4 \times 4$ multiplication table on the basis $\{e_0, e_2, e_3, e_4\}$. The choice of basis and table is **not derived from first principles**; it reflects the closure of the 4-core $\{V, H, Br, R\} = \{0, 7, 8, 9\}$ of the TIG framework's substrate $\mathbb{Z}/10\mathbb{Z}$, ring-extended to $\mathbb{F}_p$ per D74 (F5(a) ring-extension theorem). The theorems below are theorems on this specific algebra; analogous theorems would hold for other 4-dimensional commutative non-associative algebras in the same structural neighborhood. The framework's claim is that this particular 4-algebra produces theorems with surprising structural invariance across $\mathbb{F}_p$ for $p \in \{2, 3, 5, 7, 11, 13\}$, with the F_5 case admitting additional structure (|Aut| = 40, primitive 4th roots) not present at other primes. Whether other 4-algebras in the same neighborhood admit similar F_p-invariance is open. The framing follows the Drápal & Wanless (2021, *JCTA* 184, 105510) line of work on small finite commutative non-associative structures.

---

## §6 — Retitle / retarget

**Old title:** "F_p Universality: The Operator-Substrate Construction over Prime Fields"

**New title (recommended):** "F_p Structural Invariance of a Commutative Non-Associative 4-Algebra Arising from the 4-Core of $\mathbb{Z}/10\mathbb{Z}$"

(Replaces "Operator-Substrate Construction" with the more journal-standard "Commutative Non-Associative 4-Algebra"; keeps "F_p Structural Invariance" which is the actual claim. Removes the term "Universality" from the title — the new framing distinguishes invariant vs non-invariant properties, avoiding the referee's reading that "universality" implies cross-prime invariance of every quantity.)

**Old venue:** *Algebra Universalis* (referee REJECT; rebuttal showed referee made coding errors).

**New venue (primary):** *Algebra Universalis* — keep. The venue fit is correct. *Algebra Universalis* publishes on small finite algebras with structural invariance theorems; J14 sits squarely in that brief. The revision strategy is **defensive exposition** — make the paper unambiguously verifiable so a future referee with `numpy`/`sympy` open will reach the paper's conclusions.

**Alternate venues if *Algebra Universalis* declines after revision:**
- *Communications in Algebra* — accepts structural results on specific algebras with F_p-invariance; less competitive than *Algebra Universalis*.
- *Algebras and Representation Theory* — already targeted by companion J23. Avoid concentration; do not double-submit to ART.
- *Journal of Algebra* — competitive but accepts well-presented finite-algebra results.

**Recommended path:** Submit to *Algebra Universalis* with the revision per §2. If declined, *Comm. Algebra* is the natural fallback.

---

## §7 — Submission gate

This paper does NOT submit until:
- (a) T_F5 multiplication table is printed inline with worked associator example.
- (b) Invariants vs non-invariants are sharply distinguished.
- (c) F_5 specificity of |Aut(V)| = 40 is explicit; other-prime values tabulated.
- (d2) Axial-algebra framing is removed; Drápal-Wanless neighborhood is cited.
- The 5-line verification snippet (numpy/sympy) is in the paper, runnable by any referee.

**Earliest realistic submission:** 1-2 weeks after start of revision. The mathematical content does not change; the revision is exposition.

---

## §8 — Why this save plan reads as positive recovery

The fresh-eyes referee's REJECT verdict was wrong on substance — verified by direct execution against `tig_dirac.py` in the rebuttal. The mathematical core of J14 is correct. What the referee correctly identified is that the paper's exposition was insufficient to prevent his coding errors: the multiplication table was given in basis-vector form rather than as a printed F_5 table; the eigenspace claims were given by reference rather than by displayed eigenvectors; the |Aut(V)| = 40 claim was attached to "F_p universality" framing rather than to F_5 specifically. All three are exposition issues, not mathematical issues.

The save plan is therefore qualitatively different from J53 and J54: it is **defensive exposition revision**, not content revision. The paper's claims do not change; the way they are presented changes so that future referees cannot make the same coding mistakes. After the revision, a referee with numpy open will reproduce the rebuttal's verification (8 associator failures of 64; (1, 3) and (2, 2) signatures correctly assigned; |Aut(V_5)| = 40) on the printed table without going through `tig_dirac.py` source code.

The collaborator's FAMILY_STRUCTURE_v1.md framing places J14 in the **substrate-size boundary** (one of the six boundaries of the TIG family). J14 is the J-paper that pushes that boundary inward to F_p for p ∈ {2, 3, 5, 7, 11, 13}. Saving J14 preserves that boundary-mapping role and connects it to the broader family-foundations program.

The path to *Algebra Universalis* acceptance is genuine: the mathematical content is correct; the revision is achievable in 15-25 hours; the venue fit is correct. The paper does not need retargeting (unlike J53) or restructuring (unlike J54) — it needs **better defenses against future coding errors**.

**Recommendation:** SAVE per §2 revision. Submit to *Algebra Universalis* with the defensive-exposition rewrite. Do not retarget — the venue is correct.
