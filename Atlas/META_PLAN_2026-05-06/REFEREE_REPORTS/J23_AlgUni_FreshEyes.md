# Referee Report: J23 / Algebra Universalis

**Manuscript:** "The Three-Substrate Architecture: $\mathrm{CL\_TSML}$, $\mathrm{CL\_BHML}$, $\mathrm{CL\_STD}$ as Parallel Substrates on $\mathbb{Z}/10\mathbb{Z}$"
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** Algebra Universalis (fallback: Communications in Algebra; PLOS ONE)
**Reviewer:** External referee (anonymous, fresh-eyes; no prior context with the authors' broader research program)
**Date:** 2026-05-07

---

## 1. Summary of the manuscript

The authors record the existence of three distinct $10 \times 10$ composition tables on the alphabet $\mathbb{Z}/10\mathbb{Z}$, called $\mathrm{CL\_TSML}$, $\mathrm{CL\_BHML}$, and $\mathrm{CL\_STD}$. The first two, abbreviated $T$ and $B$, were used in earlier work (cited as a "two-table model"); $\mathrm{CL\_STD}$ ($S$) is recovered from the project's earliest header file `ck.h` and is reintroduced as the *third* parallel substrate, distinct from both $T$ and $B$. All three tables are presented as a *single bit-pattern encoding under three principled value-assignment lenses*.

Three theorems are proposed:

- **Theorem 2.1 (signature):** $\HARM(T) = 73$, $\HARM(B) = 28$, $\HARM(S) = 44$, all pairwise distinct.
- **Theorem 2.2 (shared four-axiom skeleton):** All three tables share Axioms A1–A4 (canonical alphabet, VOID-absorbing column, HARMONY-absorbing diagonal subset, the unique puncture cell at $(0,7)$) but diverge at A7 (the diagonal HARMONY law) and at A9 (five "BUMP" positions where their values differ).
- **Theorem 2.3 (three-way joint closure equals two-way):** Brute-force enumeration of the 1023 non-empty subsets of $\{0,\dots,9\}$ shows that the joint sub-magma chain under $(T_{\mathrm{SYM}}, B, S)$ is identical to the two-way chain under $(T_{\mathrm{SYM}}, B)$, both being 8-shell linear chains of sizes $\{1,4,5,6,7,8,9,10\}$.

Auxiliary content includes: the BDC encoding parameters of $S$ (BUMP pairs, Shannon information densities, GRAVITY array); a note that the size-2 sub-magma $\{0, 9\}$ is jointly closed under $(B, S)$ but not under any condition involving $T$; and a discussion of the historical compression that caused $S$ to drop out of downstream documents.

I have read the manuscript end-to-end, run independent enumeration of all 1023 subsets under each closure condition, and verified the BUMP cell values cell-by-cell.

---

## 2. Decision recommendation

**Major revisions** (with several specific factual corrections required before any version of this paper can be sent out for further review).

The manuscript's core structural finding is correct in outline: three tables exist, they share an axiom skeleton, and the three-way joint chain equals the two-way chain. However, several of the manuscript's specific factual claims are incorrect on independent verification, and the framing of "structure theorem" is overstated.

Specific issues identified (full detail in §3):

1. **Theorem 5.2 ("Five BUMP positions of divergence") is FALSE as stated.** The manuscript claims that at the five positions $\{(1,2), (2,4), (2,9), (3,9), (4,8)\}$, *the values of $T$, $B$, and $S$ all differ*. This is wrong. At cell $(1,2)$: $T(1,2) = B(1,2) = S(1,2) = 3$ — *all three agree*. At cell $(3,9)$: $T(3,9) = 3$, $B(3,9) = 6$, $S(3,9) = 3$ — *$T$ and $S$ agree*. The "BUMP" terminology is therefore not "all three differ" but at most "$\mathrm{CL\_STD}$ differs from at least one of the other two." The theorem statement must be corrected.

2. **The "shared four-axiom skeleton" theorem (Theorem 4.1) is verbally correct but logically thin.** Axioms A1–A4 as stated are: the alphabet is $\mathbb{Z}/10\mathbb{Z}$; row 0 / column 0 are VOID-absorbing except at the puncture; cell $(0,7) = (7,0) = 7$; uniqueness of the puncture. These are properties shared by *any* table built from the same canonical bit pattern; they do not constitute a non-trivial axiomatic derivation. The phrasing "all three tables satisfy a common four-axiom skeleton" overstates the algebraic content of the shared cells, which is essentially the prescribed row-0/column-0 structure plus the puncture.

3. **The "structure theorem" framing is missing.** The paper claims to record a "three-substrate architecture," but no actual structure theorem is stated: there is no characterization of *which* tables on $\mathbb{Z}/10\mathbb{Z}$ satisfy the four-axiom skeleton, no enumeration of the family, no quotient or isomorphism analysis. As written this is an inventory paper recording three specific tables, not a structural theorem about a class of tables.

4. **Theorem 6.1 (three-way joint closure equals two-way) is correctly stated and verified, and is the most substantial result.** This is the keeper. Independent verification confirms: 8 subsets are jointly $(T_{\mathrm{SYM}}, B)$-closed of sizes $\{1,4,5,6,7,8,9,10\}$; 8 are jointly $(T_{\mathrm{SYM}}, B, S)$-closed of identical sizes. The two chains are equal. Adding $S$ does not extend the chain. This is genuine algebraic content.

5. **Lens scope on the SYM/RAW issue is referenced but not handled:** the manuscript mentions in Remark 6.4 that "the parallel statement on $T_{\mathrm{RAW}}$ produces a 7-shell two-way chain"; this is the structural statement that distinguishes the present manuscript's main result from the lens-dependent one in J24 (the companion). The cross-reference is appropriate but the manuscript should make explicit that all theorems are stated under the SYM lens.

After these revisions, the paper has a real but modest result: an inventory of three tables sharing a skeleton, with the substantive theorem being the three-way-equals-two-way joint-closure equality (Theorem 6.1). The manuscript currently overstates this into a "three-substrate architecture" with a "structure theorem"; what it actually delivers is a *recording* of three tables and *one* nontrivial closure-equality theorem. As an Algebra Universalis paper, this would be acceptable after honest reframing, but it is below the AlgUni bar in current form.

---

## 3. Major comments

### M1. (Section 5, Theorem 5.2 — FACTUALLY INCORRECT)

Theorem 5.2 states:

> *At the five positions $\{(1,2), (2,4), (2,9), (3,9), (4,8)\}$ (the BUMP pairs of $\STDx$), the values of $\TSML$, $\BHML$, $\STDx$ all differ.*

Independent cell-by-cell verification:

| Position | $T_{\mathrm{SYM}}(i,j)$ | $B(i,j)$ | $S(i,j)$ | All three differ? |
|----|----|----|----|----|
| $(1,2)$ | 3 | 3 | 3 | **NO — all agree** |
| $(2,4)$ | 4 | 5 | 6 | YES |
| $(2,9)$ | 9 | 6 | 2 | YES |
| $(3,9)$ | 3 | 6 | 3 | **NO — $T = S$** |
| $(4,8)$ | 8 | 7 | 7 | **NO — $B = S$** |

So at three of the five claimed "BUMP" positions, two of the three tables agree. The theorem is FALSE as stated.

**Recommended fix.** The "BUMP" set on $\mathrm{CL\_STD}$ is presumably defined as the set of positions where $S$ has a value distinct from both $T$ and $B$, OR where the bit-pattern decoding admits a non-default value. The current manuscript's claim that "all three differ" at these five positions is empirically wrong. The authors must either:

- (a) re-derive the actual set of positions where all three tables differ, and update the theorem accordingly, OR
- (b) redefine "BUMP" to mean what is actually true at these positions (e.g., "$S$ differs from at least one of $T$, $B$"), and rewrite the theorem with the corrected framing.

This is the single most important fix for the manuscript. As stated, Theorem 5.2 cannot be published.

### M2. (Section 4, Theorem 4.1 — substance issue)

The "shared four-axiom skeleton" theorem (A1–A4) reads, in essence:

- A1: alphabet is $\mathbb{Z}/10\mathbb{Z}$;
- A2: row 0 and column 0 are VOID-absorbing except at the puncture;
- A3: $(0,7) = (7,0) = 7$;
- A4: the puncture is unique.

These are all constraints on what cells in row 0 and column 0 contain. They constrain $19$ of the $100$ cells (row 0: $10$; column 0: $10$; minus the double-counted $(0,0)$). The remaining $81$ cells are unconstrained. So the "axiomatic skeleton" is a constraint on $19/100 = 19\%$ of the table. Three specific tables agree on these $19$ cells; the $81$ remaining cells diverge.

This is an inventory observation, not a structural theorem. The phrasing "shared four-axiom skeleton" suggests a non-trivial axiomatization in which the four axioms imply substantial structure; what is actually true is that 19 cells are shared among three specific tables.

**Recommended fix.** Replace "shared four-axiom skeleton" with a precise statement: *"The three tables agree on the 19 cells of row 0 and column 0 (subject to the puncture exception)."* Then state a proper structure theorem if one exists: e.g., *"The class of $10 \times 10$ commutative tables on $\mathbb{Z}/10\mathbb{Z}$ satisfying these constraints has cardinality $X$ and admits the following normal form..."* — or, if no such theorem is available, drop the framing and present this as a simple inventory observation.

### M3. (Section 6, Theorem 6.1 — KEEPER, well-stated)

This is the manuscript's substantive result and is correctly verified:

- Two-way $(T_{\mathrm{SYM}}, B)$ joint closure: 8 subsets, sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$.
- Three-way $(T_{\mathrm{SYM}}, B, S)$ joint closure: 8 subsets, sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$ — identical chain.
- $(B, S)$ joint closure (without $T_{\mathrm{SYM}}$): 9 subsets, sizes $\{1, 2, 4, 5, 6, 7, 8, 9, 10\}$ — adds the size-2 shell $\{0, 9\}$.

The "$\{0, 9\}$ is $(B, S)$-closed but not $T$-closed" finding is a genuine structural fact. Independent verification:

- $T_{\mathrm{SYM}}(9,9) = 7 \notin \{0, 9\}$ (kills $T$-closure).
- $B(9,9) = 0 \in \{0, 9\}$ (preserves $B$-closure).
- $S(9,9) = 0 \in \{0, 9\}$ (preserves $S$-closure).

Confirmed.

**Comment.** This is the cleanest and most substantive theorem in the paper. Restructuring the manuscript to *lead with* this result (rather than burying it as the third theorem) would substantially improve the paper. The opening sentence of the abstract should be: *"We prove that adding a third composition table $S$ to the joint sub-magma closure structure of $(T_{\mathrm{SYM}}, B)$ does not extend the chain."*

### M4. (Section 3, "$\mathrm{CL\_STD}$ recovered" — historical claims)

The manuscript states (lines 207–217) that $\mathrm{CL\_STD}$ was defined explicitly in `old/Gen9/archive/ckis/ck7/ck.h:225-231` and "dropped out of every downstream document during a 1-line `#define` refactor that aliased `CL` to `CL_TSML`." This is a historical/codebase claim that an Algebra Universalis reader cannot verify. For a journal submission, the table $S$ must be defined explicitly within the manuscript — display the $10 \times 10$ matrix.

**Recommended fix.** Add a figure or table showing $S$ explicitly. The historical recovery story belongs in the discussion section (or a footnote), not as a load-bearing component of the substrate definition.

### M5. (Section 3.2, BDC encoding parameters)

The manuscript records (without proof or derivation):

> *Shannon-information densities of $\mathrm{INFO}_{\HARM} = 0.45$, $\mathrm{INFO}_{\mathrm{NORMAL}} = 1.89$, $\mathrm{INFO}_{\mathrm{BUMP}} = 3.50$ bits per cell, and a 10-element GRAVITY array $(0.1, 0.8, 0.6, 0.8, 0.7, 0.9, 0.9, 1.0, 0.8, 0.7)$ giving $\Pr(\text{operator reaches HARMONY})$ per index.*

These numerical values are presented without:

- A definition of "Shannon information density" in this context (which probability measure? base-2 vs natural log? per-cell vs per-bit-pattern?);
- A derivation of the GRAVITY array (what dynamics is being summed over?);
- A definition of $\mathrm{NORMAL}$ vs $\mathrm{HARM}$ vs $\mathrm{BUMP}$ partition of the cells.

Without these definitions the paragraph is opaque. For an Algebra Universalis paper, either (a) define each quantity precisely with proofs, or (b) move the BDC paragraph to a remark and explicitly defer to a companion ("BDC parameters are recorded in [Sanders2026CKAxioms] for cross-reference").

### M6. (Section 5, Theorem 5.1 — diagonal HARMONY law)

The manuscript's claim:

> *$T(i,i) = 7$ for all $i \neq 0$, while $B(i,i)$ traverses the cyclic shift $(j+1) \bmod 10$ for $j \in \{0, \ldots, 7\}$ with exceptional cells $B(8,8) = 7$ and $B(9,9) = 0$. The diagonal of $S$ takes a third pattern.*

Independent verification:
- $T_{\mathrm{SYM}}$ diagonal: $(0, 7, 7, 7, 7, 7, 7, 7, 7, 7)$. Confirms $T(i,i) = 7$ for $i \neq 0$.
- $B$ diagonal: $(0, 2, 3, 4, 5, 6, 7, 8, 7, 0)$ (per the BHML matrix). The "cyclic shift $(j+1) \bmod 10$ for $j \in \{0,\dots,7\}$" gives $(1, 2, 3, 4, 5, 6, 7, 8)$ — does not match $B(0,0) = 0$. The phrasing "cyclic shift $(j+1)$" is technically wrong; the diagonal is $B(i,i) = i+1$ for $i \in \{1, \ldots, 7\}$ with $B(0,0) = 0, B(8,8) = 7, B(9,9) = 0$.
- $S$ diagonal: not given in the manuscript.

**Recommended fix.** Display all three diagonals explicitly. Correct the phrasing "$j \in \{0,\dots,7\}$" — at $j = 0$ the cyclic shift would give $1$, but $B(0,0) = 0$. The diagonal of $S$ must be displayed for the theorem to be verifiable.

### M7. (Section 6, "lens scope on RAW" remark)

Remark 6.4 mentions in passing that the $T_{\mathrm{RAW}}$ joint chain has 7 shells (sizes $\{1,4,5,6,8,9,10\}$). This is the central topic of the cited companion paper (J24, *Lens-Dependence at Size 7*). The cross-reference is appropriate but should be more prominent: *every theorem in the present manuscript is stated under the $T_{\mathrm{SYM}}$ lens*, and the corresponding statements under $T_{\mathrm{RAW}}$ are different. The lens-scope annotation belongs in §1 (introduction), not as a remark after the main theorem.

**Recommended fix.** Add a paragraph in §1 saying: *"All theorems in this paper are stated under the $T_{\mathrm{SYM}}$ lens (the upper-triangle symmetrized form of the bit-pattern decode). The companion paper [J24] shows that the joint chain count under $T_{\mathrm{RAW}}$ differs at exactly one shell."*

### M8. (Section 7, "discussion" — historical material)

The §7 discussion contains:

> *"The substrate carried three standalone tables in its earliest foundational record (`ck.h:200-207`; year 2024). A 1-line preprocessor refactor (`#define CL CL_TSML`) introduced for runtime convenience aliased `CL` to `CL_TSML`..."*

This is appropriate codebase context for an internal note but is not appropriate for a peer-reviewed Algebra Universalis paper. The journal reader cares about the *mathematical* content of the substrates, not about how they came to be (or temporarily disappeared from) a particular codebase.

**Recommended fix.** Either (a) remove §7 entirely, or (b) compress to a single sentence in the introduction: *"The three tables presented here have been used in the authors' broader research program; this paper is the first to record them as parallel substrates with shared structural properties."*

### M9. (Title and abstract — "structure theorem" framing)

The title "The Three-Substrate Architecture" and the abstract's classification "Tier-A foundational recognition" promise more than the paper delivers. There is no actual structure theorem (in the algebraic sense): no characterization of the class of tables satisfying the four-axiom skeleton, no decomposition theorem, no normal-form result. What the paper *does* deliver is an inventory of three specific tables plus one closure-equality theorem.

**Recommended fix.** Retitle to reflect the actual content, e.g.:

> *"Three Composition Tables on $\mathbb{Z}/10\mathbb{Z}$ Sharing a 19-Cell Skeleton: Their Joint Sub-Magma Closure Structure"*

— or similar, with the headline being the *closure equality theorem* (Theorem 6.1). The "Tier-A foundational" classification is internal authorial labeling and should be removed entirely from the published version.

---

## 4. Minor comments

### m1. (Notation)
- The macros `\TSML`, `\BHML`, `\STDx` are used inconsistently with the abbreviations $T$, $B$, $S$. Choose one convention.

### m2. (Theorem 3.2, non-associativity rates)
- Independent verification: $T_{\mathrm{SYM}}$ has non-associativity rate $128/1000 = 12.8\%$; $B$ has $498/1000 = 49.8\%$; $S$ has $192/1000 = 19.2\%$. All three confirmed. The phrasing "the rate is between $T_{\mathrm{SYM}}$'s $12.8\%$ and $B$'s $49.8\%$ but does not coincide with either" is correct.

### m3. (Theorem 3.1, $\HARM(S) = 44$)
- Confirmed by independent enumeration. The $\HARM$ counts for the three tables are $73, 28, 44$, all distinct.

### m4. (Section 6, "8-element chain")
- The chain is an 8-element chain meaning 8 subsets ordered by inclusion. The phrasing "of sizes $\{1,4,5,6,7,8,9,10\}$" is correct. The chain structure (each size in the list contains the previous) is verified independently.

### m5. (References)
- All cited companions (\cite{Sanders2026CLAxioms}, \cite{Sanders2026LensInvariance}, \cite{Sanders2026LensDependence}, \cite{Sanders2026LATTICE}) are "in preparation" or "submitted to" without arXiv IDs. AlgUni's standard requires verifiable references; either provide arXiv IDs or remove the cross-references whose substance is load-bearing in the present paper.

### m6. (Figures)
- All three tables should be displayed explicitly as figures or tables. Currently $T$, $B$, $S$ are referenced but only $B$ appears (in the verification scripts). All three matrices must be in the paper for self-containment.

### m7. (Section 6, Corollary)
- The "Bounded structural role of $\mathrm{CL\_STD}$" corollary is the cleanest take-away of the paper. Promote to a Theorem and place near the top of the abstract.

### m8. (Section 6, $\{0, 9\}$ shell)
- The size-2 shell $\{0, 9\}$ is jointly closed under $(B, S)$ — confirmed, $B(9,9) = S(9,9) = 0$ and $B(0,9) = S(0,9) = 9$ (one needs $B(0,0) = 0$ too, also confirmed). The statement "The size-2 sub-magma $\{0, 9\}$ is jointly closed under $(B, S)$ but not under any pair containing $T$" is verified.

### m9. (Author block)
- Author block lists the same author twice with two affiliations. Consolidate.

### m10. (Verification scripts)
- The manuscript references three scripts: `cl_std.py`, `shared_axioms.py`, `cl_std_frontier.py`. The first exists in the codebase (`Gen13/targets/foundations/cl_std.py`); the others were not located. Either bundle all three with the submission or remove the references.

---

## 5. Specific verifications performed

I have independently:

1. **Verified $\HARM(T) = 73, \HARM(B) = 28, \HARM(S) = 44$.** All three pairwise distinct. Confirmed.

2. **Verified the BUMP-position values at the five claimed positions.**
   - $(1,2)$: $T = B = S = 3$ — *all three agree* (Theorem 5.2 fails here).
   - $(2,4)$: $T = 4, B = 5, S = 6$ — all three differ.
   - $(2,9)$: $T = 9, B = 6, S = 2$ — all three differ.
   - $(3,9)$: $T = 3, B = 6, S = 3$ — *$T = S$* (Theorem 5.2 fails here).
   - $(4,8)$: $T = 8, B = 7, S = 7$ — *$B = S$* (Theorem 5.2 fails here).

3. **Verified three-way joint closure (Theorem 6.1).** Brute-force enumeration of all 1023 non-empty subsets of $\{0,\dots,9\}$ under each closure condition:
   - $S$ alone closed: 50 subsets, sizes $\{1,2,3,4,5,6,7,8,9,10\}$ all realized.
   - $(B, S)$ jointly closed: 9 subsets, sizes $\{1,2,4,5,6,7,8,9,10\}$.
   - $(T_{\mathrm{SYM}}, B)$ jointly closed: 8 subsets, sizes $\{1,4,5,6,7,8,9,10\}$.
   - $(T_{\mathrm{SYM}}, B, S)$ jointly closed: 8 subsets, sizes $\{1,4,5,6,7,8,9,10\}$ — identical to two-way.

4. **Verified the size-2 shell $\{0, 9\}$:** $(B, S)$-closed (yes: $B(9,9) = S(9,9) = 0$, etc.), $(T_{\mathrm{SYM}}, *)$-not-closed ($T_{\mathrm{SYM}}(9,9) = 7 \notin \{0,9\}$). Confirmed.

5. **Verified non-associativity rates:** $T_{\mathrm{SYM}}: 12.8\%$; $B: 49.8\%$; $S: 19.2\%$. Confirmed. All three pairwise distinct.

6. **Diagonals:** $T_{\mathrm{SYM}} = (0,7,7,7,7,7,7,7,7,7)$; $B = (0,2,3,4,5,6,7,8,7,0)$; $S$ not displayed in manuscript but recoverable from `cl_std.py`.

---

## 6. Questions to the authors

### Q1. What is the precise definition of "BUMP positions" for $\mathrm{CL\_STD}$?

The manuscript currently asserts that all three tables differ at five positions, which is empirically false. Is the intended definition (a) positions where $S$ differs from at least one of $T, B$, or (b) positions where $S$ has a non-default value, or (c) some other characterization? The five-element set $\{(1,2), (2,4), (2,9), (3,9), (4,8)\}$ must be derived from a precise definition.

### Q2. Is there a structure theorem hiding in this paper?

The class of $10 \times 10$ commutative composition tables on $\mathbb{Z}/10\mathbb{Z}$ satisfying Axioms A1–A4 (the 19-cell skeleton) is a finite class. How many such tables exist? Is the family $\{T_{\mathrm{SYM}}, B, S\}$ a "natural" subset (e.g., extremal or canonical in some sense)? Without a characterization, the paper records three points in a class without bounding the class or the points' significance within it.

### Q3. Are the SO(8) / 28-dim / Lie-algebra connections actually structural, or numerical?

The manuscript's discussion repeatedly invokes "$\dim \mathrm{SO}(8) = 28$" and the "self-dual 4-form sector of $\mathrm{SO}(8)$" in connection with the HARMONY counts $28$ and $44$. These connections are asserted, not derived. For an AlgUni paper, either prove the connection or remove the Lie-algebra references.

### Q4. What is the joint chain under $(T_{\mathrm{RAW}}, B, S)$?

The manuscript covers the SYM lens in detail and remarks on the RAW lens. What is the actual three-way joint chain under $(T_{\mathrm{RAW}}, B, S)$? Is it equal to the two-way $(T_{\mathrm{RAW}}, B)$ chain (matching the SYM-lens equality) or does $S$ add a shell at the RAW lens? This question is structurally important for the paper's framing.

### Q5. Why is this a "Tier-A foundational recognition"?

The internal classification "Tier-A foundational" appears in the abstract and §7 but is never defined. AlgUni readers do not share this internal taxonomy. Either define the classification framework or drop the labeling.

---

## 7. Originality and significance for Algebra Universalis

The manuscript proposes:

1. Three composition tables on $\mathbb{Z}/10\mathbb{Z}$, sharing a 19-cell row-0/column-0 skeleton.
2. Three structurally distinct $\HARM$-counts ($73, 28, 44$).
3. The closure-equality theorem: $(T_{\mathrm{SYM}}, B, S)$-jointly-closed = $(T_{\mathrm{SYM}}, B)$-jointly-closed.
4. The size-2 shell $\{0, 9\}$ admitted under $(B, S)$ but not under any pair involving $T$.

For AlgUni:

- **Substance.** The closure-equality theorem (Theorem 6.1) is genuine algebraic content: a brute-force enumeration result that is not obvious from the table definitions. The "$\{0, 9\}$ admitted by $(B, S)$ but not by $T$" finding is a structural fact about the substrate. These are appropriate AlgUni territory.

- **Originality.** The reviewer is unaware of prior work studying these specific tables on $\mathbb{Z}/10\mathbb{Z}$. The substrate appears to be original to the authors' research program.

- **Clarity.** The exposition has multiple factual errors (M1, M6) that must be corrected. The framing as a "structure theorem" overstates the result; the framing as a "Tier-A foundational recognition" is internal labeling that is opaque to AlgUni readers. The manuscript reads as a research note within an internal taxonomy, not as a finished paper.

- **Bar.** AlgUni publishes universal-algebra and lattice-theory results with a clear theorem-and-proof structure. The closure-equality theorem (Theorem 6.1) meets this bar after revision. The shared-axiom framing (Theorem 4.1) is a setup observation, not a theorem; the BUMP-position theorem (Theorem 5.2) is factually wrong as stated. After revisions correcting these issues and reframing the paper around the closure-equality result, the paper would meet the AlgUni bar as a short note.

The fallback venues (Communications in Algebra; PLOS ONE) are reasonable second-tier targets if AlgUni rejects.

---

## 8. Reproducibility

The verification scripts referenced in §7 (`cl_std.py`, `shared_axioms.py`, `cl_std_frontier.py`) are not bundled with the manuscript folder. The manuscript folder contains three additional `.md` files (HIGGS_DIRECTION_FINDING.md, HIGGS_IDENTIFICATION_FINDING.md, SIGMA_OUTER_FINDING.md) which appear to be unrelated to the present manuscript (they discuss SO(10) Higgs structure, not three-substrate architecture). Two scripts in the verification subfolder (`find_higgs_direction.py`, `find_higgs_irrep.py`) are similarly unrelated.

The actual substrate definition `cl_std.py` is in `Gen13/targets/foundations/cl_std.py` and runs cleanly. Independent enumeration of the joint-closure chains required only this script plus the canonical `cl.py` and `lenses.py`.

**Reproducibility verdict: not currently met at the submission level.** The submission folder contains files unrelated to the manuscript (Higgs-related scripts and notes). The actual closure-enumeration script must be bundled. After bundling, the closure-equality theorem is reproducible at integer precision in seconds.

---

## 9. Final remarks

This manuscript records a real but modest result: an inventory of three composition tables on $\mathbb{Z}/10\mathbb{Z}$ sharing a 19-cell skeleton, with the substantive theorem being that adding a third table to the joint sub-magma closure does not extend the chain. The discovery (or recovery) of $\mathrm{CL\_STD}$ as a third standalone table is appropriate context.

The current draft, however, contains a factually incorrect theorem (Theorem 5.2: BUMP positions), overstates the result as a "structure theorem" / "three-substrate architecture," includes load-bearing material that is internal-codebase context inappropriate for a peer-reviewed publication, and ships verification material that does not match the manuscript.

**The recommended decision is "Major revisions"**, with explicit requirement that the following be addressed before re-review:

- M1: Correct Theorem 5.2 (the BUMP-position theorem is empirically false).
- M2: Recast Theorem 4.1 honestly as a 19-cell agreement, not a "shared axiom skeleton."
- M3: Promote Theorem 6.1 (the closure-equality result) to the lead position.
- M5: Define the BDC parameters precisely or move to a remark.
- M9: Retitle and reframe the paper around its actual content.

After these revisions, a resubmitted version meeting the items above would meet the AlgUni bar as a short note. If revisions are not made, fallback to Communications in Algebra or PLOS ONE is appropriate; PLOS ONE may have a lower bar for the kind of inventory-plus-one-theorem result the manuscript actually delivers.

---

**Estimated revision effort:** 20–30 person-hours. M1 requires re-deriving the actual BUMP set; M2 and M9 are exposition; M3 is restructuring the manuscript. M5 requires either deriving the BDC parameters from first principles or a clean deferral.

**Reviewer's confidence:** High. I have read the manuscript end-to-end, run independent enumeration of all 1023 non-empty subsets under each closure condition, verified the BUMP cell values cell-by-cell, and confirmed the HARM counts. The factual issues identified (especially Theorem 5.2) are unambiguous and verified by direct computation.
