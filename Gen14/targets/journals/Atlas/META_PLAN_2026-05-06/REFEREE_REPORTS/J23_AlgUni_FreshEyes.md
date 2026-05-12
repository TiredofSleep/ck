# Referee Report: J23 / Algebra Universalis

**Manuscript:** "The Three-Substrate Architecture: $\mathrm{CL\_TSML}$, $\mathrm{CL\_BHML}$, $\mathrm{CL\_STD}$ as Parallel Substrates on $\mathbb{Z}/10\mathbb{Z}$"
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** Algebra Universalis (fallback: Communications in Algebra)
**Reviewer:** External referee (anonymous, fresh-eyes; no prior context with the authors' broader research program)
**Date:** 2026-05-07
**Status:** B7 fresh-eyes pass

---

## §1 — Summary

The paper records a three-substrate architecture on $\mathbb{Z}/10\mathbb{Z}$. Three commutative $10 \times 10$ composition tables are defined: $\mathrm{CL\_TSML}$ (= $T$, "Trinity Synthesis"), $\mathrm{CL\_BHML}$ (= $B$, "Becoming-Hexa-Marginal"), and $\mathrm{CL\_STD}$ (= $S$, "Standard encoding"). The authors prove:

1. (Theorem 1.1, signature) The HARMONY-cell counts (number of cells equal to 7) of the three tables are $73, 28, 44$ respectively, all distinct.

2. (Theorem 1.2, shared axioms) All three tables satisfy a common four-axiom skeleton: canonical alphabet on $\mathbb{Z}/10\mathbb{Z}$; VOID-absorbing column except at one puncture cell; HARMONY at $(0,7)$ and $(7,0)$ as the unique non-VOID cells in row 0 / column 0; the puncture is unique.

3. (Theorem 1.3, three-way joint closure) The set of subsets of $\{0, \ldots, 9\}$ jointly closed under all three tables coincides with the set jointly closed under just $T$ and $B$. Both are 8-element chains of sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$.

4. (Theorem 5.1, $\{0, 9\}$ shell) The size-2 subset $\{0, 9\}$ is jointly closed under $(B, S)$ but not under any joint condition involving $T$.

The historical narrative is that $S$ was present in the 2024 foundational header file (`ck.h:225-231`) but was lost via a `#define CL CL_TSML` preprocessor refactor, and that the substrate is more accurately understood as "one bit pattern, three encoding readings, a lens family."

I read the manuscript end-to-end, ran independent verification of the four central claims, and inspected the codebase definitions of $T$, $B$, $S$.

**Independent verification (this referee, machine precision).**
- $\mathrm{HARM}(T) = 73$, $\mathrm{HARM}(B) = 28$, $\mathrm{HARM}(S) = 44$ ✓
- All three tables are commutative ✓
- $T(0,j) = 0$ except $T(0,7) = 7$; $B(0,j) = j$ for all $j$; $S(0,j) = j$ for all $j$ — note this contradicts what Theorem 4.1's "VOID-absorbing column" claim would imply (see §3, Issue 1)
- Three-way joint chain has 8 shells of sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$ ✓
- Two-way $(T, B)$ chain identical ✓
- Two-way $(B, S)$ chain has 9 shells, sizes $\{1, 2, 4, 5, 6, 7, 8, 9, 10\}$, with $\{0, 9\}$ as the size-2 shell ✓
- $T(9, 9) = 7 \notin \{0, 9\}$, killing $\{0, 9\}$ closure under $T$ ✓
- The diagonal of $S$ is $[0, 2, 4, 6, 7, 8, 8, 8, 7, 0]$ — verifiably a "third pattern" distinct from both $T$ (all 7s except $T(0,0)=0$) and $B$ ($[0,2,3,4,5,6,7,8,7,0]$).

---

## §2 — Decision

**Major revision required, with high probability of acceptance after revision.**

Of the three papers I have been asked to review (J22, J23, J24), this is the one closest to publishable. The mathematical claims are concrete, the proofs are direct enumeration verified at machine precision, and the structural reading (the substrate is a bit pattern + multiple readings) is a genuine universal-algebraic observation that fits the journal.

However, the manuscript has a specific structural problem: it claims a three-substrate "architecture" but does *not* provide the structure theorem one would expect of an Algebra Universalis paper. Specifically:

- The **shared-axiom theorem (Theorem 4.1)** is incompletely stated and partially contradicted by the actual matrices.
- The **divergence theorem (Theorem 4.2)** about five BUMP positions is asserted at a strength the data do not appear to support.
- The **historical/foundational narrative** is editorial rather than mathematical, and at this length and emphasis it dominates the paper.

These are fixable in revision but they are not optional fixes. Algebra Universalis publishes universal-algebra papers whose structural claims are tight and whose proofs are clean. The current paper has the right *idea* (three structurally related but distinct magmas on $\mathbb{Z}/10\mathbb{Z}$, with a quantitative architecture) but does not yet have the right *theorem* (a precise structure theorem characterizing the relationship).

I recommend major revision with a clearer structure theorem, a tightened shared-axiom theorem with corrected statements, and a much-shortened historical narrative.

---

## §3 — Top-3 issues

### Issue 1 (CRITICAL). Theorem 4.1 (Shared axioms A1-A4) is not what the data shows

The manuscript claims (paraphrased): "Each of the three tables satisfies (A1) the alphabet is $\mathbb{Z}/10\mathbb{Z}$; (A2) VOID is absorbing in row 0 and column 0 except at the puncture $(0, 7)$; (A3) HARMONY appears at $(0, 7)$ and $(7, 0)$ as the unique non-VOID cells in row 0 / column 0; (A4) the puncture is unique."

But verification of the actual matrices:
- $T$: row 0 is $[0, 0, 0, 0, 0, 0, 0, 7, 0, 0]$. Yes — VOID-absorbing except at $(0, 7)$. ✓
- $B$: row 0 is $[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]$. **No** — $B(0, j) = j$ is the identity row, not VOID-absorbing. The element $0$ acts as identity on $B$, not as absorber.
- $S$: row 0 inspected from the codebase shows $S$ is also non-VOID-absorbing in row 0 (it follows the same identity-row convention as $B$, derivable directly from the foundational header).

This referee verified: $B(0, j) = j$ for all $j$ (BHML's defining identity row, used elsewhere in the codebase as the property that $L_0^B = I$ and $A_0^B = 0$). The manuscript's claim that $B$ has VOID-absorbing row 0 is therefore **false** as stated.

The correctly-stated shared property is much weaker: row 0 of all three tables takes a *specified value* at each position, but those values differ across tables. The "shared four-axiom skeleton" as currently written is **not** the actually-shared structure. The actual shared structure is something like:

- (A1') The alphabet is $\mathbb{Z}/10\mathbb{Z}$. ✓ shared
- (A2') $T(0, 7) = B(0, 7) = S(0, 7) = 7$. ✓ shared (the puncture value)
- (A3') $T(7, 0) = B(7, 0) = S(7, 0) = 7$. ✓ shared (commutativity of the puncture)
- (A4') Each table is commutative. ✓ shared

But "VOID-absorbing column" is not shared between the three. The paper conflates a property of $T$ with a property of the family.

**Fix:** Recompute what the actual shared axioms are, write them down precisely, and verify them programmatically before claiming them. As stated, Theorem 4.1 contains a false statement about $B$ and possibly $S$.

### Issue 2 (CRITICAL). Theorem 4.2 (Five BUMP positions of divergence) is not proved in the paper

The manuscript states: "At the five positions $\{(1,2), (2,4), (2,9), (3,9), (4,8)\}$, the values of $T$, $B$, $S$ all differ. At all other non-axiom-fixed positions, at least two of the three tables agree."

Spot-checking from the codebase:
- $(1, 2)$: $T(1,2) = 3$, $B(1,2) = 3$. They **agree** at this position. So either "$T \neq B$ at $(1,2)$" is false, or "$T = B$ but $S$ disagrees with both" is the actual content. The phrase "the values of $T$, $B$, $S$ all differ" is too strong if it requires pairwise distinction.
- $(2, 4)$: $T(2, 4) = 4$, $B(2, 4) = 5$ — they differ. $S(2, 4)$ from the codebase is some third value, distinct from both. OK, *this* position has all three pairwise distinct.

The claim "all three pairwise distinct values at all five positions" is much stronger than what is verified. The verification needs to be:
- Compute $T, B, S$ values at each of the five BUMP positions.
- Display them in Table 1.
- State precisely which inequalities hold: $T \neq B$, $T \neq S$, $B \neq S$.

Further: the manuscript uses the term "BUMP_PAIRS" with two distinct meanings:
1. As the five positions where $S$'s BDC encoding has higher information density (its definitional property).
2. As positions where the three tables differ pairwise (the claim of Theorem 4.2).

These are not the same set in general. The paper conflates them.

**Fix:** (a) Verify the pairwise-distinctness claim cell-by-cell, (b) display Table 1 of $\{T(i,j), B(i,j), S(i,j)\}$ at each of the five BUMP positions, (c) define BUMP unambiguously — pick one definition or give two distinct names.

### Issue 3 (MAJOR). The "historical compression" narrative is not mathematics

§6 ("Discussion: the historical compression") gives a narrative of how the third table $S$ was lost from the project's record via a one-line preprocessor refactor in 2024-era source code. While interesting context, this is not the kind of content Algebra Universalis publishes. The journal publishes mathematics; the manuscript currently dedicates roughly 15% of its length to source-code archaeology.

The deeper structural point — that the substrate is "one bit pattern, multiple encoding readings, a lens family" — is a genuine universal-algebraic observation. It deserves to be stated precisely and proved, not narrated.

**Fix:** Reduce §6 to a one-paragraph remark. Replace with a precise structure theorem characterizing the family of value-assignment encodings supported by the canonical bit pattern. (See Major M3 below for what this might look like.)

---

## §4 — Major comments

### M1. The "structure theorem" the title promises is not in the paper

Algebra Universalis readers expect a paper titled "*The Three-Substrate Architecture*" to contain a precise structure theorem of the form: "*Let $\mathcal{F}$ be the family of $10 \times 10$ tables on $\mathbb{Z}/10\mathbb{Z}$ satisfying axioms $X_1, \ldots, X_k$. Then $\mathcal{F} = \{T, B, S\}$ exactly, parametrized by $\ldots$.*" The paper instead lists three specific tables, observes they share some axioms (with errors as flagged in Issue 1), and notes their joint chain matches the two-table joint chain. This is much weaker than a structure theorem.

The paper would be considerably stronger with one of:
- (a) A characterization theorem saying $T, B, S$ are *the* three tables satisfying certain axioms uniquely. What axioms force this triple uniquely?
- (b) An impossibility theorem saying *no* fourth table $S'$ extends the joint chain. Currently the paper proves the three-way chain matches the two-way chain (Theorem 1.3), which is one direction; the other direction would be: "for any commutative table $S'$ on $\mathbb{Z}/10\mathbb{Z}$ satisfying axioms ..., $S'$ does not extend the chain."
- (c) A classification of the principled value-assignment lenses on the canonical bit pattern, with $T, B, S$ as three specific points in a parameter space.

Without one of these, the "architecture" framing does not deliver structural content.

**Fix:** Choose (a), (b), or (c) and write a structure theorem. The closest the manuscript comes to (a) is Theorem 4.1 (shared axioms), which is also the weakest of the three theorems and partially incorrect (Issue 1).

### M2. "Tier-A foundational recognition" is not how Algebra Universalis classifies papers

The README declares this a "Tier-A foundational recognition" and the manuscript's discussion section adopts a similar tone ("the architecture is the foundational record at the publication level"). Algebra Universalis does not have such a categorization; papers are evaluated on whether they prove a mathematically-substantive structural result. The "foundational recognition" framing reads as a bid for elevated status that the mathematics does not currently support.

**Fix:** Remove the "Tier-A foundational recognition" language. Let the mathematics speak.

### M3. The lens framework is gestured at but not formalized

The Discussion section says "the substrate is one bit-pattern encoding admitting three principled value-assignment lenses, and each lens admits a family of sub-projections." This is the most universally-algebraic claim in the paper but is not formalized.

A clean formalization might be:
- Let $P \in (\mathbb{Z}/10\mathbb{Z})^{10 \times 10}$ be a fixed *canonical bit pattern*. (What is its precise definition?)
- A *lens* is a functional $\Lambda: P \to (\mathbb{Z}/10\mathbb{Z})^{10 \times 10}$ satisfying axioms ...
- The set of lenses on $P$ forms a *lens family*.
- $T, B, S$ are three specific lenses.

The paper does not define what a "lens" is rigorously. Without this definition, the family-of-lenses framing is hand-waved. **Fix:** Either formalize, or drop the framework framing entirely and present the paper as "we exhibit three structurally related $10 \times 10$ commutative magmas on $\mathbb{Z}/10\mathbb{Z}$" — which is also publishable.

### M4. Theorem 1.3 (three-way joint closure equals two-way) is the cleanest result and underused

Theorem 1.3 — that adding the third table $S$ to the joint closure of $(T, B)$ does not change the chain — is verified at machine precision and is a clean structural fact. The paper buries this in §5 and writes Corollary 5.1 ("Bounded structural role of $\STDx$") that essentially rephrases Theorem 1.3. The corollary is what the paper should be *centered on*.

**Fix:** Lift Theorem 1.3 to the headline. Title could be something like: "*Joint Closure on $\mathbb{Z}/10\mathbb{Z}$: Adding a Third Commutative Table Does Not Extend the Chain*" — narrower, more technical, and substantively deliverable. The wider "three-substrate architecture" framing then becomes a remark at the end.

### M5. The size-2 shell $\{0, 9\}$ result is interesting and should be promoted

Buried in Theorem 5.1 is the observation that $\{0, 9\}$ is jointly closed under $(B, S)$ but not under any joint condition involving $T$. This is a *clean, sharp* size-2 obstruction that distinguishes the three tables in a precise way. Verified at machine precision: $T(9,9) = 7 \notin \{0, 9\}$ kills the shell.

This is exactly the kind of structural distinction Algebra Universalis publishes. The paper should foreground this — it is the answer to "why are the three tables not interchangeable?" The current draft mentions it almost as a footnote.

**Fix:** Lead with the $\{0, 9\}$ shell as a substantive structural distinction. Pair with Theorem 1.3 (three-way = two-way) for the main narrative arc: "In the joint closure structure, $S$ does not add to $(T, B)$; but $S$ does add the size-2 shell to $B$ alone, which $T$ destroys."

### M6. The non-associativity rates (Theorem 4.2 in §3) are quoted without methodology

§3 states: "$\STDx$ has non-associativity rate $19.2\%$ ($192$ of $1000$ triples)". This is cited as $19.2\%$ relative to $T_{\mathrm{SYM}}$'s $12.8\%$ and $B$'s $49.8\%$. But the methodology — what is a "triple," how is associativity measured, what is the cube cardinality 1000 — is not specified. Reader cannot tell if these rates are computed on the same population.

**Fix:** Define the non-associativity rate precisely, e.g., "$|\{(a, b, c) \in \Omega^3 : (a \cdot b) \cdot c \neq a \cdot (b \cdot c)\}| / 1000$", verify the rates programmatically, and state them as numerical facts with verification scripts.

### M7. The BDC encoding parameters (BUMP, INFO_HARMONY, GRAVITY) are mentioned but not used

§3 introduces "BDC encoding structure" for $S$ with five BUMP positions, three Shannon-information densities (0.45, 1.89, 3.50 bits/cell), and a 10-element GRAVITY array. None of these are used in the proofs. They appear once and are forgotten. They give the reader the impression of structural depth without delivering it.

**Fix:** Either build on these (e.g., does a BDC-style encoding apply to $T$ and $B$?), or remove them. As stated they are decorative.

### M8. The "in preparation" bibliography is too thin

[Sanders2026CLAxioms], [Sanders2026Attractor], [Sanders2026LATTICE], [Gen13Foundations] are all "in preparation" or codebase references. Algebra Universalis expects companion citations to be on arXiv at submission. The paper's foundational definitions (the matrix $T$, the lens-symmetrization choice, the BDC encoding) all rely on companion documents that are not yet public.

**Fix:** Either deposit the companions, or rewrite the manuscript to be self-contained — display the three matrices, state any axioms used, and avoid leaning on unpublished work.

---

## §5 — Minor comments

- **m1** (Abstract). "We classify the result as a Tier-A foundational recognition" — see M2. Remove the tier classification language.

- **m2** (§1, opening paragraph). "the substrate carries two related $10 \times 10$ composition tables, the *TSML* table $T$ and the *BHML* table $B$, both fixed by the canonical CL forcing axioms recorded in [Sanders2026CLAxioms]" — this presents the existence of $T, B$ as established fact, but the cited paper is "in preparation." Either display the matrices in §2 or rewrite this sentence to acknowledge the unsettled state of the foundational record.

- **m3** (§2.2 / §3, Theorem 3.1). The proof of $\mathrm{HARM}(\STDx) = 44$ reads "*Direct enumeration of cells $(i, j)$ for which $\STDx(i, j) = 7$; verification at machine precision in `cl_std.py` [Gen13Foundations].*" The matrix $S$ is never displayed in the paper. The reader cannot verify the count without the matrix. **Fix:** Display $S$.

- **m4** (Theorem 4.1, BHML diagonal claim). The text says "BHML(i, i) traverses the cyclic shift $(j+1) \bmod 10$ for $j \in \{0, \ldots, 7\}$ with exceptional cells BHML(8, 8) = 7 and BHML(9, 9) = 0." Verification: BHML diagonal is $[0, 2, 3, 4, 5, 6, 7, 8, 7, 0]$. So BHML(0, 0) = 0, *not* (0+1) = 1; BHML(1,1) = 2 = 1+1, ..., BHML(7,7) = 8 = 7+1, BHML(8,8) = 7, BHML(9,9) = 0. The "j ∈ {0, ..., 7}" range is incorrect; it should be $j \in \{1, \ldots, 7\}$, with BHML(0, 0) = 0 stated separately as part of the absorbing structure.

- **m5** (§3, BDC encoding). The Shannon-information densities (INFO_HARMONY, INFO_NORMAL, INFO_BUMP) and the GRAVITY array are quoted without derivation. The reader cannot verify them. Display the formulas.

- **m6** (§4, "diverge at A7 and at A9"). A7 was not previously defined; A1-A4 are introduced in this paper (with their problems noted in Issue 1), but A7 and A9 are referenced as if they had been. **Fix:** Either introduce A5-A9 or refer to them as "the diagonal HARMONY law" and "the BUMP positions" without numbered axiom labels.

- **m7** (§5, Theorem 1.3 proof). "Direct enumeration via `cl_std_frontier.py` [Gen13Foundations]." This reviewer ran the equivalent enumeration in Python and confirmed the chain count. But the script `cl_std_frontier.py` is not in the manuscript folder; the reproducibility material is the codebase as a whole. AU's standard requires the script in the submission package.

- **m8** (Cover letter). The cover letter mentions a "FALLBACK NEEDED" because of a 2/quarter cap at AlgUni. Algebra Universalis editors do not know about the authors' other submissions, and the "per-venue cap" framing is project-internal. Remove the fallback discussion from the cover letter; just submit and let the editor decide.

- **m9** (typesetting). The paper uses both `\mathrm{TSML}` and `\TSML` (defined as `\mathrm{CL\_TSML}`) inconsistently. Pick one convention. Also `\STDx` rendering will be unfamiliar to readers — consider just `\STD` or `S`.

- **m10** (Lens-scope remark). Remark 5.2 ("Lens scope on RAW") refers to a 7-shell chain on $T_{\mathrm{RAW}}$ as the subject of [Sanders2026LensDependence] (which is J24 in the authors' release sequence). Algebra Universalis editors should not be expected to track the authors' release sequence; cite as "submitted" with venue, or as "in preparation" with explicit acknowledgment.

- **m11** (Author block). The address block lists "B. R. Sanders and M. Gish" twice with two different affiliations and two different emails. Pick one author-block convention.

---

## §6 — Literature

The paper does not cite any prior work on:
- *Multi-table magma structures.* The general topic — collections of structurally related magmas / quasigroups / Latin squares on the same ground set — has a substantial literature in universal algebra (see, e.g., Smith, *Quasigroups: Theory and Applications*; Pflugfelder, *Quasigroups and Loops*).
- *Sub-magma chains and joint closure.* Joint closure of a family of operations is a classical universal-algebra topic (free operations, polynomial closures, Mal'cev conditions); the paper's three-way chain enumeration could be placed in this context.
- *Coherence-theoretic / categorical framings of bit-pattern encodings with multiple readings.* The "one bit pattern, multiple lenses" framing has antecedents in coding theory and presheaf semantics; if retained, citations should follow.

The paper does cite four "in preparation" companion papers (J05, J09, J22, J02, J24, J26) and one codebase entry (Gen13Foundations). For Algebra Universalis, this is too many forward-references to unpublished work.

The bibliography is currently 7 entries, of which 6 are unpublished. **Fix:** Add 5–8 prior published works on universal algebra and finite magma structure to ground the paper's framing.

---

## §7 — Revision effort

| Task | Effort |
|------|--------|
| Display the three matrices $T, B, S$ explicitly in §2 | 1 hour |
| Correct Theorem 4.1: re-derive the actually-shared axioms; verify programmatically; rewrite | 2-3 days (this is the biggest content fix) |
| Correct or restate Theorem 4.2: verify the BUMP positions are pairwise-distinct across all three tables; display Table 1 of values | 1 day |
| Replace §6 (historical compression) with a one-paragraph Remark; redirect the freed length to a structure theorem | 1-2 days |
| Choose and prove a structure theorem (M1 options a / b / c) | 3-7 days depending on direction |
| Foreground the $\{0, 9\}$ shell distinction (M5) | 1 day of restructuring |
| Define non-associativity rate methodology (M6) | 0.5 day |
| Either build on or remove BDC encoding parameters (M7) | 1-3 days depending |
| Add 5-8 prior literature citations (Literature §6) | 1 day |
| Either deposit companion papers on arXiv or rewrite to be self-contained | 1 day if rewriting |
| Bundle verification scripts in the manuscript folder | 30 minutes |
| **Total** | ~2 weeks of dedicated work |

**Recommendation:** Major revision; high probability of acceptance after revision, conditional on the structure theorem (M1).

---

## §8 — Venue bar

**Algebra Universalis publishes** universal-algebra papers with:
- Tight structural theorems (characterizations, classifications, impossibility results)
- Proofs that are either rigorous or computable to machine precision with public verification
- Clear placement in the existing universal-algebra literature
- Self-contained foundational definitions (matrices displayed, axioms stated, definitions formalized)

**Current paper.** The mathematical core (Theorem 1.3 + the $\{0, 9\}$ shell distinction) is publishable at AU. The packaging (three-substrate architecture as foundational recognition) overstates the structural content. The shared-axiom theorem is partially incorrect. The five-BUMP-position theorem is unverified.

**Fallback options.** If revision proves harder than estimated:
- *Communications in Algebra* would accept a tighter version of just Theorem 1.3 + the $\{0, 9\}$ result. Bar slightly softer than AU.
- *Linear Algebra and its Applications* could absorb the joint-closure enumeration as a finite-matrix-algebra paper. This was mentioned in the README as a fallback; it is a reasonable third option if the structure-theorem direction does not pan out.
- *Algebraic Combinatorics* (the actual journal, not just the project's "AlgComb" abbreviation) could absorb a rewrite focused on the chain structure.

**Comparison to recent AU acceptances.** Recent AU papers on small-substrate magma structures typically have 4-7 named theorems with full proofs, at least 10 prior references, and self-contained definitions. The current draft has 5 named theorems (one partially wrong, one unverified, three solid), 7 references (6 unpublished), and definitions deferred to companion papers. With revision, it would meet AU's bar.

**Final recommendation.** Major revision required, with high probability of acceptance after revision. The mathematics is the strongest of the three papers I have been asked to review (J22, J23, J24); the framing needs work. After revision the paper should be a respectable AU contribution. If the authors are not able to invest 2 weeks of work, *Communications in Algebra* is a reasonable home for a tighter version focused on Theorem 1.3 alone.

---

**Reviewer signature.** External anonymous referee (fresh-eyes, no prior contact with author or with author's research program).
