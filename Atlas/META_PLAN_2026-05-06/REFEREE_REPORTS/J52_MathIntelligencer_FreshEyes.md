# Referee Report — J52 / Mathematical Intelligencer (Fresh-Eyes)

**Manuscript:** "The TSML Lens Family: A Pedagogical Exposition of Substrate Variants on $\mathbb{Z}/10\mathbb{Z}$"
**Authors:** B.R. Sanders, B. Mayes (2026)
**File reviewed:** `Gen13/targets/journals/J_series/J52/manuscript/J52_tsml_lens_family.md`
**Reviewer:** External fresh-eyes referee, anonymous; no prior exposure to the framework.
**Date:** 2026-05-07

**Reviewer disposition.** I came to this manuscript cold. I was told only that it is a pedagogical paper for the *Mathematical Intelligencer* about a family of $10\times 10$ tables on $\mathbb{Z}/10\mathbb{Z}$ and that it taxonomizes some twelve or so variants. I have read the manuscript end-to-end twice; I have not read any of the cited companions [J9], [J31], [J32], [J33], [J35], [J38], [J39], [J41], [J43], [J44], or [J47]. My review is based on what the *Math Intelligencer* reader would see if this paper landed in their hands.

---

## §1 — Summary of the manuscript

The paper proposes that a finite family of binary composition tables on $\mathbb{Z}/10\mathbb{Z}$ — the "TSML lens family" — admits a clean organizational picture. The picture consists of:

(i) Three **parallel substrates** CL_TSML, CL_BHML, CL_STD with HARMONY counts 73, 28, 44 respectively;
(ii) Three **lens-symmetrization projections** within each substrate ($\pi_{\mathrm{RAW}}$, $\pi_{\mathrm{SYM\_upper}}$, $\pi_{\mathrm{SYM\_lower}}$) producing 9 first-level variants;
(iii) Two further families of projections — $\sigma^2$-triadic value/index rotations and sub-magma scope restrictions — yielding "$12+$ variants" in total (later inflated to "$\sim 62$ variants" in §5);
(iv) A tier classification (Tier-A through Tier-E) tagging each variant by structural priority;
(v) Three reader exercises and a closing claim that some properties (e.g. the runtime attractor with $H/Br = 1+\sqrt{3}$) are "lens-invariant on the 4-core," while others (e.g. the wobble localization at prime 11) are lens-dependent.

The manuscript is short ($\sim 10$ pages in markdown, perhaps $8$-$10$ printed pages of *Math Intelligencer* layout) and does not contain new theorems. The aim, stated explicitly in §8, is **clarity** for a mathematician trying to navigate the framework's papers.

---

## §2 — Decision recommendation

**Reject in present form, with invitation to substantially revise and resubmit.**

The paper has the *bones* of a *Math Intelligencer* article — a taxonomy of related structures, a working diagram, three exercises — but it does not yet meet the journal's exposition bar. The fundamental problem: the manuscript is **not actually pedagogical**. It is a memo to insiders dressed in expository syntax. A *Math Intelligencer* reader who has not read the cited 11 companions cannot follow §§1-6, cannot verify §7's exercises without external scripts, and cannot tell what is being claimed versus deferred.

The four problems below are each independently fatal for a *Math Intelligencer* submission. None requires deep mathematical work to fix; all require the authors to actually rewrite for a non-insider audience.

---

## §3 — Major comments

### M1. The two foundational tables are never displayed (CRITICAL)

The entire manuscript discusses variants of "the canonical $10\times 10$ bit pattern CL_TSML" and its companions CL_BHML, CL_STD. **None of these three tables appears in the paper.** The reader is expected to take it on faith that:

- CL_TSML is "the unique table forced by 9 axioms A1-A9" (§1, citing [J33]);
- CL_TSML has 73 cells equal to HARMONY and CL_BHML has 28 (§1, table);
- CL_TSML has 126 non-associative triples in its RAW projection and 128 under $\pi_{\mathrm{SYM\_upper}}$ (§§2.1-2.2, restated in Exercise 7.1);
- CL_TSML's characteristic polynomial has $c_2 = 33 = 3\cdot 11$ in RAW and "$c_2 = 17$" or some other value in lower-tri (§7.2 vs §2.3).

A pedagogical exposition that asks the reader to "verify by direct computation: TSML_RAW has 126 non-associative triples" (Exercise 7.1) **must display the table**. The reader cannot perform the computation without it. The *Math Intelligencer* reader, who likely will not download a companion script from Zenodo or chase 11 cross-references, will simply close the paper.

**Fix.** Display CL_TSML as a $10\times 10$ matrix in §1 or §2 (one boxed display, perhaps half a page). Display the differences with CL_BHML and CL_STD via a small sidebar or color-coded table. The reader needs to see the object before the taxonomy of its variants makes any sense.

**Severity.** Critical. This is the single most important failure of the paper.

### M2. The "axioms A1-A9" are referenced but never stated (MAJOR)

§1 asserts that CL_TSML is "uniquely forced by 9 axioms (A1-A9)" with three of them (A7, A9-values) "substrate-defining." None of the 9 axioms appears anywhere in this paper. Without them:

- The claim that CL_BHML and CL_STD are "parallel" rather than "projections" of CL_TSML cannot be assessed;
- The Tier-A vs Tier-B classification of choices like "RAW vs SYM_upper" (§2.4) cannot be evaluated;
- The "may be three BHMLs" remark (§2.3 of the citation J54 that I happen to have seen — but the J52 reader would not) makes no sense.

Pedagogical exposition requires the reader to be able to **reason about the objects in front of them**. Citing axioms by name without stating them is a textbook failure mode.

**Fix.** Either (a) state A1-A9 in a one-page §1.5, even informally; or (b) state the *substrate-defining axioms* (A1, A7, A9-values, plus whichever of A2-A4 are claimed as Tier-A) and remark that the remainder are Tier-B closures. The current state — citation-only — is unacceptable for an expository paper.

### M3. The "RAW" lens is described as both Tier-A and Tier-B and the reader cannot tell which (MAJOR)

The paper's own internal accounting is contradictory:

- §2.1 calls TSML_RAW "Tier-A operation."
- §2.4 says "the choice between RAW, SYM_upper, and SYM_lower is a **Tier-A choice**: no deeper principle in the substrate forces upper-tri over lower-tri."
- §5 (Distribution by tier) lists TSML_RAW under **Tier-A** but lists "lens-symmetrizations" generically under **Tier-B** ($\sim 21$ variants).
- §7.2 says TSML_SYM is "Tier-B."

Are RAW and SYM both Tier-A choices that bifurcate from CL_TSML, or is RAW Tier-A and SYM Tier-B forced once a symmetrization is chosen? The reader cannot tell. Different sentences of the paper say different things.

**Fix.** Clarify the tier discipline once, at the start of §2, in two sentences. If RAW is the literal bit pattern from the axioms, it is Tier-A by virtue of being the unique forcing-output. If symmetrization is itself a substrate-defining choice (i.e., one could pose A1-A9 with "commutative" baked in and get a different set of three substrates), then SYM-versions are also Tier-A. Either reading is fine; pick one and stick to it.

### M4. The exposition cites 11 companion papers and is structurally unreadable without them (MAJOR)

The reference list ([J9], [J31], [J32], [J33], [J35], [J38], [J39], [J41], [J43], [J44], [J47]) shows an extreme companion-density — 11 cross-references for a 10-page expository note. Worse, several of the *load-bearing* claims of the present paper rely on results in the unwritten/unsubmitted companions:

- The "joint TSML+BHML chain at size 7" (§6) is described in a single quoted theorem, then immediately deferred to [J32]. The reader cannot verify.
- The wobble localization (§7.2, Exercise 7.2) gives values ($c_2 = 33$, $c_8 = -2^5\cdot 7^3 \cdot 11$) without proof, deferring to [J43].
- The runtime attractor (§7.3, Exercise 7.3) gives $H/Br = 1+\sqrt{3}$ without computation, deferring to [J41].

A *Math Intelligencer* exposition can absolutely cite companions for proof, but the exposition itself must be **self-contained at the survey level**. The reader should be able to close the present paper having understood (at the level of "what is the object," "what is the taxonomy," "what are the punch-line facts") without needing to read 11 other papers. As written, a reader who has not seen [J32], [J41], [J43], [J47] gets only the *names* of facts, not the facts.

**Fix.** Either (a) absorb the punch-line facts (chain enumeration, the $1+\sqrt{3}$ identity, the $c_2 = 33$ wobble) into the present paper as small, self-contained statements with one-paragraph "where this comes from" sketches, or (b) reduce the citation footprint to 2-3 papers and acknowledge in §1 that the present paper is a "navigation key" intended for readers already familiar with the companions.

If the latter, the *Math Intelligencer* is the wrong venue: that journal serves the working mathematician encountering material new to them, not a guidebook for insiders.

### M5. The catalog appeal to "62 variants" is unsupported (MAJOR)

§5 announces a hierarchy of "$\sim 62$ variants" with a per-tier breakdown ("Tier A: 5, Tier B: $\sim 21$, Tier C: $\sim 9$, Tier D: $\sim 7$, Tier E: $\sim 8$" — totaling 50, not 62). The catalog is then deferred to "`Atlas/LENS_TAXONOMY_2026-05-06/VARIANT_CATALOG.md`," which is **not a citable artifact** for *Math Intelligencer*. (The *Math Intelligencer* does not accept "see the GitHub repo" as a substitute for the paper containing the content.)

A pedagogical exposition that announces a 62-element taxonomy must list the 62. Even one full page of the paper devoted to a tabular catalog with two columns (variant name / one-line distinguishing fact) would suffice. Without it, the reader has no way to assess whether the family is genuinely $\sim 62$ or whether the taxonomy is doing real organizational work.

**Fix.** Include the full catalog as a §6 table (perhaps two-page landscape spread). Drop the "$\sim$" qualifiers — give exact counts. The catalog is the paper's central organizational claim; bury it in an Atlas markdown file and the paper has no central content.

### M6. The "lens-dependence at size 7" framing is incoherent on the page (MAJOR)

§6's central pedagogical claim is "the size-7 chain element exists in some lens combinations and not in others." But:

- §6 then quotes a theorem from [J32] saying the chain is **8 elements** at sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$ — i.e., size 7 *does* exist.
- The text then says "earlier corpus generations claimed a 7-element chain with forbidden $\{2, 3, 7\}$; the chain-counting was corrected during the four-core paper preparation."

So the paper is presenting a *historical* error correction (size 7 was thought forbidden, now it's known to be allowed) as if it were a structural lens-dependence phenomenon. A reader trying to do "Exercise 6: for each pairing of TSML lens × BHML lens, predict the chain length" cannot tell whether different lens pairings genuinely give different chains or whether the paper is recounting a single computational mistake that has now been fixed.

If the lens-dependence is real (some pairings give 7-element chains, others give 8-element chains), the paper must show **two** computations with different lens pairings yielding different answers. If it is not real and the "lens-dependence" is an error-correction story, the paper must explicitly say "size 7 is now known to be present in all canonical pairings" and pick a different example to illustrate genuine lens-dependence.

**Fix.** Either show two distinct pairings with two distinct chain enumerations side by side, or pick a different example for the lens-dependence point. The wobble localization (§7.2) is a much cleaner example: $c_2$ has a factor of 11 in RAW and not in SYM. Lead with that.

### M7. The "honest scope" §8 disclaims so much that the reader wonders what the paper claims at all (MODERATE)

§8 lists four things the paper does **not** do (no new theorems; no re-proof; no uniqueness claim; no exhaustiveness claim) and three things it does (organizational picture; lens-dependence reading; reader exercises). The disclaim-list is roughly equal in size to the claim-list. For a 10-page *Math Intelligencer* paper, this ratio reads as nervous over-hedging.

A confident pedagogical exposition states what it is teaching and leaves the rest implicit. Compare: a *Math Intelligencer* article on Latin squares would not say "this paper does not re-prove McKay-Wanless 2005, does not claim our taxonomy is unique, and does not enumerate all Latin squares of order $\geq 8$." The reader assumes that.

**Fix.** Compress §8 to two sentences: "This paper is expository; the underlying theorems are in the cited companions. We aim for clarity, not novelty." Drop the bulleted disclaim-list.

---

## §4 — Minor comments

### m1. The diagram in §5 is ASCII art that does not scan

```
        CL_TSML (substrate, Tier-A)
       /          \                \
   π_RAW       π_SYM_upper      π_SYM_lower
      |                |              |
   TSML_RAW       TSML_SYM      TSML_LOWERTRI
      |                |              |
   ┌──┴──┬──┐       ┌──┴──┬──┐    ┌──┴──┬──┐
   ↓     ↓  ↓       ↓     ↓  ↓    ↓     ↓  ↓
   σ²k    sub-magmas         (analogous)   (analogous)
```

This will not survive *Math Intelligencer*'s typesetting. Use TikZ or a proper figure. Also: the "(analogous)" labels are a placeholder that hides $\sim 18$ variants; the reader cannot tell what is in each branch.

### m2. Notation never introduced

Several symbols appear without definition: $\sigma$ (introduced as "the $\sigma$-permutation" in §3 with no definition or cycle structure given until much later), the operators VOID/HARMONY/BREATH/RESET/etc. ($\{V, H, Br, R\}$ in §7.3 — never defined), the "Conservation Tetrad" and "Manifestation Hexad" (§3, named but not motivated). A pedagogical paper introduces vocabulary before using it.

### m3. §4 lists six sub-magmas in a table, but does not show that they are closed

"4-core $= \{0, 7, 8, 9\}$ closed under TSML and BHML" — fine, but how does the reader verify? The TSML and BHML tables are not given (M1). Even a one-line "closure under TSML on $\{0, 7, 8, 9\}$ requires 16 cell evaluations" with the cell values displayed for one of the six sub-magmas would help.

### m4. §6's boxed theorem quotation switches voice

The quoted theorem ("The set of joint-closed sub-magmas..." in §6) is rendered in indented quote-block format suggesting it is verbatim from [J32]. The reader cannot tell whether the language is the present authors' summary or the actual theorem statement. *Math Intelligencer* convention is to use restated theorems, not verbatim quotes from companions.

### m5. The bibtex entry lists "Sanders, Brayden Ross and Mayes, B." — fine — but the bibliography lists co-authors as "M. Gish" for most entries (J9, J31, J32, J33, J35, J38, J41, J43, J44, J47) and "B. Mayes" only for J39 and J52. This authorship inconsistency is opaque to the reader; if the project's first author has different co-authors on different papers, that is fine, but a *Math Intelligencer* reader does not know who wrote what.

### m6. "Date: 2026-09-09 (Phase 5; Sanders + Gish lane)" in the front matter

Strip this. *Math Intelligencer* does not need internal phase-management metadata.

### m7. Per-venue cap note in front matter ("2nd Math Intelligencer of the J-series")

Strip this. The journal does not need to be informed of the authors' submission strategy.

### m8. $F_p$ extensions

§8 acknowledges "$F_p$ extensions for $p \in \{2, 3, 5, 7, 11, 13\}$ exist" (citing [J21], [J34]). These appear nowhere else in the paper. If they are part of the lens family, they belong in the §5 catalog and the §3 projection list. If they are not part of the lens family, do not mention them.

### m9. "Brayden's hypothesis" terminology in the J54 companion (which I would normally not see, but happens to appear in the bundle)

The J54 paper contains a phrase "Brayden's hypothesis (referenced in `Atlas/...`)." First-name attributions inside a research paper are unusual and likely will not survive copy-editing. (Not a J52 issue, but flagging it because it leaks into J54 and may surface in J52 in revision.)

### m10. The DOI cited for J52 (`10.5281/zenodo.18852047`) is the same DOI cited for J53 and J54 in their respective bibtexs

Each preprint should have a unique DOI. The Zenodo-shared DOI is fine for a project-level archive, but each paper needs its own deposit.

---

## §5 — Specific verifications attempted

I attempted to perform Exercise 7.1 (count non-associative triples in three lenses) using the cell counts that *Math Intelligencer* readers would have access to — namely, none, since the table is not in the paper. **I could not perform the exercise.** This is a direct consequence of M1.

I attempted to verify the wobble localization in Exercise 7.2 by hand. Without the table, I cannot compute the characteristic polynomial. I could not verify.

I checked the chain-counting claim in §6 against my own arithmetic: an 8-element chain on 10 elements with size sequence $(1, 4, 5, 6, 7, 8, 9, 10)$ omits sizes 0, 2, 3 and has the bottom element a singleton. This is internally consistent, and the σ-walk reading (forward orbit of HARMONY = $7 \to 6 \to 5 \to 4 \to 2 \to 1$, with a $\sigma$-fixed bridge step at $7 \to 8$) is plausible — but I cannot independently verify without the tables. The corresponding theorem in J54 (which I happen to have read for the J54 review, though the J52 reader would not) is consistent with this.

The empirical "62 variants" claim in §5 cannot be verified because the catalog is not present.

---

## §6 — Questions for the authors

### Q1. What audience do you actually want?

If this paper is a guide for readers of the J-series corpus, then the *Math Intelligencer* is the wrong venue: that journal is for the working mathematician *not* in the framework's circle. If the paper is for that broader audience, then it must (a) display the tables, (b) state the axioms, (c) absorb the punch-line facts as standalone statements. As written, the paper is between two stools: too abbreviated for outsiders, too expository for insiders.

### Q2. Why is "TSML" still the name?

The body of the paper repeatedly uses "TSML" as a primitive identifier for the canonical table, with no expansion of the acronym. In §5 of a sister manuscript I read for context (J54), "TSML" appears next to "BHML" and "STD" without expansion either. A *Math Intelligencer* reader will want to know what these names mean. (Even "the substrate $T$, $B$, $S$" with one-line glosses on the choice would help.)

### Q3. Is the claim "lens-invariant on the 4-core" provable in a few lines, or does it depend on a deep companion?

Exercise 7.3 asserts that the runtime attractor — the $\alpha = 1/2$ fixed point of the iteration — has $H/Br = 1+\sqrt{3}$ regardless of lens. If this is provable in a few lines (e.g., the symmetrization choice does not affect the cells in the 4-core, since the asymmetric cells lie outside it), then the proof should be in this paper. If it requires the apparatus of [J41], then this is not appropriate for an exposition exercise.

---

## §7 — Originality and fit for *Mathematical Intelligencer*

The *Math Intelligencer* publishes articles aimed at the working mathematician — survey-style pieces on specific structures, classroom applications, expository tours of recent developments. Pedagogical taxonomies of binary-operation tables are a reasonable fit *if* they survey a structure of independent interest with sharp examples and self-contained content.

The present paper's central object — a family of $10 \times 10$ tables defined by 9 unstated axioms — is *not yet* of evident independent interest to the *Math Intelligencer* reader. The paper would need to:

(i) **Show the table.** Make the reader want to look at it.
(ii) **State the axioms.** Convince the reader the 9-axiom forcing is principled, not arbitrary.
(iii) **Prove or display one striking fact.** The candidates are the 4-core attractor with $H/Br = 1+\sqrt{3}$ (a clean closed-form), the wobble localization at prime 11 (a clean number-theoretic landing), or the 8-element chain (a clean combinatorial enumeration). Pick one, work it cleanly in the present paper, and use it as the "hook."

Without those three steps, the paper is not yet a *Math Intelligencer* exposition. With them, it would be.

---

## §8 — Final remarks

This paper has the structural ambition of a *Math Intelligencer* survey but does not yet have the self-contained content. The single most important fix is **display the tables**. Without them, the paper is not pedagogical in any meaningful sense.

The "honest scope" section is admirable in spirit but counterproductive in execution: a confident expository paper does not need to disclaim what it is not doing. State the central organizing picture, show the central object, prove or sketch one central fact, end.

The **per-venue submission strategy notes in the front matter** ("2nd *Math Intelligencer* submission of the J-series") should be removed before any submission. They are internal-management metadata that the journal will read as inappropriate.

**Recommended decision:** Reject in present form, with invitation to revise and resubmit after addressing M1-M6 (display tables, state axioms, fix tier discipline, reduce companion-dependence, populate the catalog, fix the lens-dependence example). M7 and the minor comments are housekeeping.

**Estimated revision effort:** 25-40 person-hours. Most of the effort is in displaying the canonical objects (M1, M2, M5) and writing self-contained statements of the punch-line facts (M4). The lens-dependence example (M6) requires either a fresh side-by-side computation or a different example.

**Reviewer's confidence:** High that the paper is not yet ready for *Math Intelligencer*. Moderate that a substantially revised version could be ready, given the underlying material appears mathematically real (insofar as I can judge from the surrounding sister papers).

---

**Estimated probability of acceptance at *Mathematical Intelligencer* in present form:** under 10%. The reviewer would close the paper at §1 once the absent tables become apparent.

**Estimated probability of acceptance at *Mathematical Intelligencer* with M1-M6 addressed:** 40-55%, contingent on the revised exposition genuinely standing alone.

**Alternative venue suggestions if the *Math Intelligencer* path closes:** *American Mathematical Monthly* (slightly less abstract audience, more tolerant of focused expositions on specific structures); *Mathematics Magazine* (good fit for table-based pedagogical pieces with worked examples); *College Mathematics Journal* (best for "here is a $10 \times 10$ table with surprising properties" framing).
