# Referee Report: J24 / Mathematical Intelligencer

**Manuscript:** "The Joint TSML+BHML Chain: Lens-Dependence at Size 7"
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** Mathematical Intelligencer
**Reviewer:** External referee (anonymous, fresh-eyes; no prior context with the authors' broader research program)
**Date:** 2026-05-07
**Status:** B7 fresh-eyes pass

---

## §1 — Summary

The note records an explicit lens-dependence in the joint sub-magma closure chain of two $10 \times 10$ composition tables on $\mathbb{Z}/10\mathbb{Z}$. The two tables are $T$ ("TSML") and $B$ ("BHML"). The TSML table admits two principled symmetrization choices:
- $T_{\mathrm{RAW}}$, the literal decoding of an underlying canonical bit pattern (non-commutative);
- $T_{\mathrm{SYM}}$, the upper-triangle-authoritative symmetrization (commutative).

The two lenses differ at exactly two off-diagonal cell pairs:
- $T_{\mathrm{RAW}}(3, 9) = 3$ vs $T_{\mathrm{RAW}}(9, 3) = 7$;
- $T_{\mathrm{RAW}}(4, 9) = 7$ vs $T_{\mathrm{RAW}}(9, 4) = 3$.

(Caveat: the manuscript text states these values *incorrectly* in §1; see Issue 2.)

The main theorem (Theorem 1.1):
- The joint chain under $(T_{\mathrm{SYM}}, B)$ has 8 shells of sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$.
- The joint chain under $(T_{\mathrm{RAW}}, B)$ has 7 shells of sizes $\{1, 4, 5, 6, 8, 9, 10\}$.
- The size-7 shell $\{0, 4, 5, 6, 7, 8, 9\}$ is jointly closed under $(T_{\mathrm{SYM}}, B)$ but not under $(T_{\mathrm{RAW}}, B)$.
- A single asymmetric cell, $T_{\mathrm{RAW}}(9, 4) = 3 \notin \{0, 4, 5, 6, 7, 8, 9\}$, kills the closure.

Two lens-invariance results are also recorded:
- The four-core $\{0, 7, 8, 9\}$ is jointly closed under both lens choices.
- The closed-form fixed point of an associated $T+B$-mix dynamical system at $\alpha = 1/2$ is identical under both lenses, with $H/\mathrm{Br} = 1 + \sqrt{3}$ exactly.

The paper is short (≈8 pages) and presents itself as a "short note clarifying which lens is in scope for downstream sub-magma analyses."

I read the manuscript end-to-end, ran independent verification of the central claims, and inspected the codebase definitions of $T_{\mathrm{RAW}}$, $T_{\mathrm{SYM}}$, and $B$.

**Independent verification (this referee, machine precision).**
- The two tables differ at exactly 2 cell positions: $(9, 3)$ where $T_{\mathrm{RAW}} = 7, T_{\mathrm{SYM}} = 3$; and $(9, 4)$ where $T_{\mathrm{RAW}} = 3, T_{\mathrm{SYM}} = 7$. ✓
- $T_{\mathrm{RAW}}$ is non-symmetric; $T_{\mathrm{SYM}}$ is symmetric. ✓
- Brute-force enumeration of all 1023 non-empty subsets:
  - $(T_{\mathrm{SYM}}, B)$ joint chain: 8 shells, sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$. ✓
  - $(T_{\mathrm{RAW}}, B)$ joint chain: 7 shells, sizes $\{1, 4, 5, 6, 8, 9, 10\}$. ✓
- The size-7 candidate $\{0, 4, 5, 6, 7, 8, 9\}$ is closed under $T_{\mathrm{SYM}}$ and $B$ but not under $T_{\mathrm{RAW}}$. The single cell breaking closure is $T_{\mathrm{RAW}}(9, 4) = 3 \notin \{0, 4, 5, 6, 7, 8, 9\}$. ✓
- The four-core $\{0, 7, 8, 9\}$ is closed under all of $T_{\mathrm{RAW}}, T_{\mathrm{SYM}}, B$. ✓ (does not contain index 3 or 4, so the asymmetric cells are irrelevant)

The mathematics of the paper is correct. The claims are verifiable at machine precision. The conclusion that lens-dependence is concentrated entirely at size 7 and is forced by a single cell is rigorous.

---

## §2 — Decision

**Accept with minor revision.**

Mathematical Intelligencer is an expository / semi-popular venue at the intersection of mathematics and the broader mathematical culture. Its papers are short, often well-written, and aim to convey a precise mathematical insight or curiosity to a wide mathematical audience. They are not necessarily the venue for new theorems of cutting edge generality, but they do require:
- Mathematical correctness
- Clean exposition
- A reason the result will interest a general mathematical reader

The paper meets all three criteria with relatively minor caveats:
- The mathematics is correct (verified by this referee).
- The exposition is clear, with one significant arithmetic error in §1 that is straightforward to fix.
- The "single cell of non-commutativity changes the chain count by exactly one shell at exactly one position" is a tight and pleasing structural observation that a general mathematical reader will appreciate.

The required minor revisions are:
1. Fix the arithmetic error in §1 (a swap of values that confuses the reader and is contradicted by the manuscript's later claims).
2. Trim some of the "lens scope" philosophy that reads too project-internal.
3. Tighten the bibliography away from "in preparation" companions toward published or arXiv-deposited material.

The paper is the cleanest of the three I have been asked to review (J22, J23, J24). It is also the most cleanly suited to its target venue.

---

## §3 — Top-3 issues

### Issue 1 (CRITICAL). The §1 statement of the asymmetric cell values contradicts the rest of the paper

The manuscript says, in §1's description of the two lenses:

> $T_{\mathrm{RAW}}(3, 9) = 3, T_{\mathrm{RAW}}(9, 3) = 7$; $T_{\mathrm{RAW}}(4, 9) = 3, T_{\mathrm{RAW}}(9, 4) = 3$.

> For $T_{\mathrm{SYM}}$ the upper-triangle entries are authoritative, so $T_{\mathrm{SYM}}(3, 9) = T_{\mathrm{SYM}}(9, 3) = 3$ and $T_{\mathrm{SYM}}(4, 9) = T_{\mathrm{SYM}}(9, 4) = 3$.

This referee verified from the underlying matrices:
- $T_{\mathrm{RAW}}(3, 9) = 3$, $T_{\mathrm{RAW}}(9, 3) = 7$. ✓
- $T_{\mathrm{RAW}}(4, 9) = $ **7**, $T_{\mathrm{RAW}}(9, 4) = 3$. ✗ (manuscript says RAW(4,9) = 3)
- $T_{\mathrm{SYM}}(3, 9) = T_{\mathrm{SYM}}(9, 3) = 3$. ✓ (upper-triangle is 3, so SYM uses 3 both ways)
- $T_{\mathrm{SYM}}(4, 9) = $ **7**, $T_{\mathrm{SYM}}(9, 4) = $ **7**. ✗ (manuscript says SYM = 3 both ways)

The manuscript's statements that $T_{\mathrm{RAW}}(4, 9) = 3$ and $T_{\mathrm{SYM}}(4, 9) = 3$ are both **wrong**. The correct values are $T_{\mathrm{RAW}}(4, 9) = 7$ (upper-triangle entry, used as authoritative for SYM) and $T_{\mathrm{RAW}}(9, 4) = 3$ (the asymmetric lower-triangle entry).

The asymmetric pair is therefore: $T_{\mathrm{RAW}}(4, 9) = 7$ vs $T_{\mathrm{RAW}}(9, 4) = 3$, with $T_{\mathrm{SYM}}(4, 9) = T_{\mathrm{SYM}}(9, 4) = 7$ (upper-triangle propagated). This is the actual asymmetry that produces the lens-dependence.

The paper's later claim — that "$T_{\mathrm{RAW}}(9, 4) = 3 \notin S_7$" kills the size-7 shell — *is* correct and the actual mathematics works. But the §1 description mis-states the cell values, contradicting what is needed in §3. Corollary 4.1 then writes "$T_{\mathrm{RAW}}(9, 4) = 3$ vs $T_{\mathrm{SYM}}(9, 4) = 3$" as the asymmetry, which is *not* an asymmetry — those two values are stated as equal, but the actual asymmetry is RAW = 3 vs SYM = 7.

This is the entire epistemic basis of the lens-dependence theorem. The reader of §1 cannot reconstruct the mathematics correctly. The reader of §3 sees a contradiction with §1. The fix is straightforward — restate the asymmetric pairs correctly — but it must be done.

**Fix:** Re-derive and re-state §1's "two lenses" paragraph and Corollary 4.1's "single-cell forcing" claim with the correct values:

- $T_{\mathrm{RAW}}(3, 9) = 3, T_{\mathrm{RAW}}(9, 3) = 7$ (asymmetric pair 1)
- $T_{\mathrm{RAW}}(4, 9) = 7, T_{\mathrm{RAW}}(9, 4) = 3$ (asymmetric pair 2)
- $T_{\mathrm{SYM}}(3, 9) = T_{\mathrm{SYM}}(9, 3) = 3$ (upper-triangle)
- $T_{\mathrm{SYM}}(4, 9) = T_{\mathrm{SYM}}(9, 4) = 7$ (upper-triangle)

The single-cell forcing in Corollary 4.1 should read: "$T_{\mathrm{RAW}}(9, 4) = 3$ vs $T_{\mathrm{SYM}}(9, 4) = 7$. The non-commutativity at this cell, where $T_{\mathrm{RAW}}$ disagrees with the upper-triangle authoritative value used by $T_{\mathrm{SYM}}$, produces the lens-dependence."

### Issue 2 (MAJOR). The lens-invariant attractor result (Theorem 5.2) is not self-contained

Theorem 5.2 ("Attractor lens-invariance") states that the closed-form fixed point at $\alpha = 1/2$ is $(0.138, 0.540, 0.198, 0.124)$ with $H/\mathrm{Br} = 1 + \sqrt{3}$ exactly, identical under both lenses. The proof reads:

> The attractor is supported on the four-core $\{0, 7, 8, 9\}$ at mass 1; non-four-core operators carry zero mass at the fixed point. Since the four-core is lens-invariant (Theorem 4.1), the attractor is lens-invariant. The exact identity $H/\mathrm{Br} = 1 + \sqrt{3}$ is established in [Sanders2026Attractor].

The problem: the manuscript has not defined the dynamical system whose attractor it discusses, has not stated the equations of motion, and defers the entire derivation of the closed form to "[Sanders2026Attractor]" which is "in preparation." The reader of this manuscript cannot verify what the attractor is, what $\alpha = 1/2$ refers to (mixing weight of what?), or what the closed-form $1 + \sqrt{3}$ identity is.

Yet Theorem 5.2 is a standalone theorem of this paper. A theorem without a defined object is not a theorem. **Fix:** Either define the dynamical system in this paper (this is potentially 1-2 paragraphs and a difference equation), or remove Theorem 5.2 and the related discussion. As stated it cannot be verified.

The paper's headline result (lens-dependence at size 7) does not depend on Theorem 5.2; the attractor's lens-invariance is a side observation. Removing it would not weaken the paper.

### Issue 3 (MAJOR). The "wobble" remarks (Remark 2.2 and §6) reference unpublished material

§2 introduces "the WP107 wobble (prime 11 in characteristic polynomial coefficients $c_2 = 33$ and $c_8 = -2^5 \cdot 7^3 \cdot 11$)" as a non-commutative invariant of $T_{\mathrm{RAW}}$. §6 elaborates: "Studies of the substrate's wobble structure (prime 11 in the characteristic polynomial) require $T_{\mathrm{RAW}}$." But:
- The "characteristic polynomial" of *what*? The paper does not define the matrix whose characteristic polynomial it discusses.
- The cited [Sanders2026Wobble] is "in preparation."
- The wobble result is not used in any proof of this paper; it is invoked as a motivation for caring about $T_{\mathrm{RAW}}$.

The paper is a short note; readers will encounter wobble-related references with no context, none of which advance the mathematics of the paper. **Fix:** Remove all wobble references. The paper's mathematics stands on its own.

---

## §4 — Major comments

### M1. The expository tone is inconsistent

Mathematical Intelligencer favors expository papers that read as if written for a general mathematical audience. The manuscript opens technically (§1 is densely set-theoretic) and ends with project-internal language ("the substrate itself forces the authors to name which lens is in scope"; "the substrate's gentle insistence that the authors not gloss over the question"). The two registers do not blend.

Pick one register. For Math Intelligencer the better choice is the expository one: open with the structural curiosity ("a tiny non-commutativity in a $10 \times 10$ table changes a chain count by exactly one shell at exactly one size — and only there"), then make the formal statements, then close with a reflection on what this says about lens choice in finite-magma combinatorics.

### M2. The paper is short of explicit display of the matrices

The paper makes load-bearing claims about specific cells of $T_{\mathrm{RAW}}$, $T_{\mathrm{SYM}}$, and $B$. None of the three matrices is displayed. The reader must trust the authors' description without the ability to verify by inspection.

For an 8-page Mathematical Intelligencer note, the matrices should be displayed once (perhaps in an appendix) — they fit in a 12-line block each. **Fix:** Add Display 1 and Display 2 showing $T_{\mathrm{RAW}}$ and $B$ explicitly. (Note that $T_{\mathrm{SYM}}$ is uniquely determined by $T_{\mathrm{RAW}}$ via the upper-triangle convention, so does not need separate display.)

### M3. The ordering of theorems creates a forward reference

Theorem 4.1 (size-7 shell under SYM) is stated before Lemma 2.1 (the asymmetric cells) is fully digested. The paper would read more cleanly if §3 (asymmetric cells, the actual quantitative content) preceded §4 (the brute-force enumeration). The current ordering is OK but could be tighter.

### M4. The single-cell-forcing observation deserves more emphasis

Corollary 4.1 ("Single-cell forcing of the lens-dependence") is the manuscript's deepest observation: a single cell of one $10 \times 10$ table produces a single-shell deletion in a 8-shell chain at a single position. This is the kind of result Mathematical Intelligencer's audience appreciates. Currently it is buried as a corollary; it deserves to be the headline statement, framed as "*A single non-commutative cell breaks one shell — exactly one — at one position.*"

**Fix:** Restructure so the single-cell forcing is the headline, and the full enumeration is the supporting evidence. This is also more natural exposition.

### M5. The "two principled lens-symmetrization choices" framing assumes more than is established

§2 says: "Both symmetrizations are valid for different downstream purposes." But this paper is meant to be standalone. A general mathematical reader has no prior context for "downstream purposes." The two symmetrizations need to be motivated from within this paper.

A clean motivation: "$T_{\mathrm{RAW}}$ is the literal bit-pattern decoding (non-commutative); $T_{\mathrm{SYM}}$ is what one obtains by enforcing commutativity through the natural upper-triangle convention. Both are valid mathematical objects — neither is the 'right' one — and the question of how their algebraic structure differs is the subject of this note."

### M6. The closed-form $H/\mathrm{Br} = 1 + \sqrt{3}$ identity needs more or less

The exact identity $H/\mathrm{Br} = 1 + \sqrt{3}$ exactly is mentioned twice but never derived or even motivated. If the author wants to keep this as a structural anchor, it needs at least a sentence: "the ratio of two specific stationary coordinates is a quadratic irrational $1 + \sqrt{3}$, derived in [Sanders2026Attractor]." If the author cannot do this much, remove the identity — it is decoration as currently used.

### M7. The discussion section is too long for an 8-page note

§6 ("Discussion: which lens is in scope") is over a page and meanders. For Math Intelligencer the discussion should be tight: 3-4 paragraphs at most. The current draft has 5 sub-paragraphs ("When to use $T_{\mathrm{RAW}}$", "When to use $T_{\mathrm{SYM}}$", "Foundational reading", "The story is the math forcing the disambiguation"), several of which repeat the central claim.

**Fix:** Compress §6 to 1-2 paragraphs that say (a) which lens is needed for which kind of question, (b) why this paper exists (to make the lens-scope choice explicit for downstream papers), and (c) what is interesting to a general reader (a tiny non-commutativity producing a sharp single-shell effect).

### M8. Bibliography over-references unpublished companions

[Sanders2026CLAxioms], [Sanders2026Attractor], [Gen13Foundations], [Gen13WP115] are all "in preparation" or codebase references. The paper's foundational definitions (the canonical bit pattern, the lens-symmetrization choice, the dynamical system) all rely on companion documents that are not yet public.

For Math Intelligencer this is less rigid than for a research journal, but the paper still needs to be self-contained. **Fix:** Either (a) deposit the foundational paper [Sanders2026CLAxioms] on arXiv before submission, or (b) make this paper self-contained by displaying the matrices and stating the lens convention precisely.

---

## §5 — Minor comments

- **m1** (Title). "The Joint TSML+BHML Chain: Lens-Dependence at Size 7" — for the intended general mathematical audience, both "TSML" and "BHML" are opaque acronyms. Consider a title that does not require the reader to know these terms in advance, e.g., "*A Single Non-Commutative Cell Breaks Exactly One Shell of a Sub-Magma Chain*" or "*Lens-Dependence in a $\mathbb{Z}/10\mathbb{Z}$ Magma: Eight Shells vs Seven*" — or keep the technical title with subtitle expansion.

- **m2** (Abstract, "lens-symmetrization choices"). The phrase "lens-symmetrization choices" is project-internal jargon. The general reader sees only "two ways to make a non-commutative table commutative." Use the latter phrasing or define "lens" precisely.

- **m3** (§1, "the WP115 preprint had a chain-counting error"). The README/notes mention a chain-count history with a corrected enumeration in 2026-05-05. This history is interesting context but does not belong in the published paper. Remove any references to "WP115" or to the previous-version history.

- **m4** (Lemma 2.1, "verified at machine precision in [Gen13Foundations]"). The phrase is repetitive; the entire paper is "verified at machine precision in the codebase." Tighten the proof to just state the values.

- **m5** (Theorem 3.1 numbering). Theorems are numbered by section but cited inconsistently. The paper would read more cleanly with a single numbering scheme.

- **m6** (Theorem 5.1, "The four-core does not include either of the asymmetric indices $\{3, 4\}$..."). A nicer phrasing: "The four-core $\{0, 7, 8, 9\}$ contains neither index 3 nor index 4, so the cells where $T_{\mathrm{RAW}}$ and $T_{\mathrm{SYM}}$ differ lie entirely outside the four-core's product. Therefore lens choice cannot affect closure on the four-core."

- **m7** (Remark 5.1, "All other shells are lens-invariant"). The list is a verification by enumeration; a single sentence saying so suffices. The current draft enumerates 6 specific shells; this is filler and breaks reading flow.

- **m8** (typesetting). The author block lists "B. R. Sanders and M. Gish" twice with two affiliations. Mathematical Intelligencer expects single canonical author block. Consolidate.

- **m9** (DOI in source comment). The .tex file has `%%% DOI: 10.5281/zenodo.18852047` as a top-of-file comment; this is a Zenodo DOI for the project as a whole, not for this paper. Math Intelligencer doesn't need a placeholder DOI; remove the line.

- **m10** (concluding paragraph "the substrate's gentle insistence"). Too cute for the venue. Replace with a neutral closer.

---

## §6 — Literature

Mathematical Intelligencer expects only a light bibliography (5-10 entries) and is forgiving about the kind of references included; it does not require the deep prior-art coverage that JCT-A or AlgUni would. Still:

- *Latin square / quasigroup combinatorics.* The paper does not cite any prior work on small non-commutative magma structures or sub-quasigroup chains. Even one reference (e.g., Pflugfelder, *Quasigroups and Loops*, 1990; or Smith, *Quasigroups: Theory and Applications*, 2013) would help.
- *Chain-counting in finite magmas.* The "$8$ shells vs $7$ shells" framing has antecedents in lattice theory and in the literature on subuniverse lattices of finite algebras (e.g., Burris and Sankappanavar, *A Course in Universal Algebra*).
- *Lens / symmetrization in algebraic combinatorics.* The lens-vs-symmetrization framing has antecedents in the literature on tournament algebras and on commutative-vs-noncommutative quasigroup structures.
- *The LMFDB.* Cited indirectly via companion papers; if the closed-form attractor identity is retained, the LMFDB should be cited.

The paper's current bibliography has 6 entries, of which 4 are unpublished. **Fix:** Add 3-5 published or arXiv-deposited references on the topics above. Tighten the unpublished citations to the bare minimum.

---

## §7 — Revision effort

| Task | Effort |
|------|--------|
| Fix the cell-value error in §1 (Issue 1) | 30 minutes |
| Define the dynamical system in §2 if Theorem 5.2 is retained, OR remove Theorem 5.2 and the attractor discussion | 1-2 hours |
| Remove the wobble references | 15 minutes |
| Display the matrices $T_{\mathrm{RAW}}$ and $B$ | 30 minutes |
| Re-tone §1 and §6 for the Mathematical Intelligencer audience | 2-3 hours |
| Foreground the single-cell-forcing observation as the headline | 1-2 hours of restructuring |
| Tighten §6 to 1-2 paragraphs | 30 minutes |
| Add 3-5 prior-literature citations | 1-2 hours |
| Fix author block typesetting | 5 minutes |
| Remove the WP115/history references and the DOI comment | 15 minutes |
| **Total** | ~1 day of revision |

**Recommendation:** Accept with minor revision. The mathematics is correct, the result is genuinely interesting, the paper is the right size and shape for Mathematical Intelligencer, and the revisions needed are nearly all editorial (with the one substantive exception of the §1 arithmetic error).

---

## §8 — Venue bar

**Mathematical Intelligencer publishes** short to medium-length papers (4-12 pages) on:
- Mathematical curiosities and surprising structural observations
- Expository pieces aimed at the general mathematical audience
- Historical or philosophical reflections on mathematics
- "Snapshot" results from the research frontier presented in accessible form

The venue is informal compared to research journals; the bar is correctness, clarity, and interest-to-a-general-audience rather than priority or generality. The author's tone is allowed to be more personal than at a research journal.

**Current paper.** The paper fits the venue well in shape and topic. The mathematics is correct (verified). The structural observation — *one non-commutative cell deletes one shell at one size, with all other shells unchanged* — is the kind of tight curiosity Math Intelligencer publishes regularly. The lens-invariance of the four-core and the attractor reads as a satisfying companion to the lens-dependence at size 7. The paper has the right shape.

**What would push it from "minor revision" to "outright accept."** Fix the §1 arithmetic error; replace the wobble references with proper context-free motivation; trim §6. With those changes, this is a clean Math Intelligencer note.

**Comparison to recent MI articles.** Recent MI papers in the "tight structural curiosity" mode (e.g., on prime patterns, on small Galois groups, on symmetry-breaking in small-substrate algebra) typically run 6-10 pages, display their matrices/objects explicitly, and have a clear "here is the curiosity" framing. The current paper meets these expectations after the minor revisions.

**Final recommendation.** Accept with minor revision. This is the strongest of the three papers I have been asked to review on these criteria (correctness, clarity, fit to venue). The mathematics is the most clearly verified, the claim is the most precisely stated, and the venue match is the cleanest. Approximately 1 day of revision yields a publishable Math Intelligencer note.

---

**Reviewer signature.** External anonymous referee (fresh-eyes, no prior contact with author or with author's research program).
