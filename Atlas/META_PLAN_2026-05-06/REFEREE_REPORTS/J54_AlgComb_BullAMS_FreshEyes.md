# Referee Report — J54 / *Algebraic Combinatorics* (primary) or *Bulletin AMS* (alternate) — Fresh-Eyes

**Manuscript:** "The Foundation Paper: Three-Substrate Architecture, Lens Family, and the CL Forcing Axioms on $\mathbb{Z}/10\mathbb{Z}$"
**Authors:** B.R. Sanders, M. Gish (2026)
**File reviewed:** `Gen13/targets/journals/J_series/J54/manuscript/J54_foundation_paper.md`
**Reviewer:** External fresh-eyes referee, anonymous; no prior exposure to the framework.
**Date:** 2026-05-07

**Reviewer disposition.** I came to this manuscript cold. I was told it is the *integrating foundation paper* for a J-series of $\sim 47$+ companion papers on a framework involving binary composition tables on $\mathbb{Z}/10\mathbb{Z}$. The target venues are *Algebraic Combinatorics* (primary) or *Bulletin AMS* (alternate). I am asked to assess whether this paper succeeds as the integrating contribution that anchors a 23-paper citation chain. I have read the manuscript end-to-end. I have not read the J-series companions; I evaluate the present paper as a self-contained submission.

---

## §1 — Summary of the manuscript

The paper proposes itself as the **structural anchor** for a research program on three families of binary composition tables on $\mathbb{Z}/10\mathbb{Z}$ — denoted CL_TSML, CL_BHML, CL_STD. The architectural claims are:

(I) A canonical $10 \times 10$ matrix CL_TSML is **uniquely forced** by a list of 9 axioms A1-A9 (proof in [J33]; restated here).

(II) Three parallel substrates CL_TSML, CL_BHML, CL_STD share axioms A1-A4 and diverge at A7 + A9-values, with HARMONY counts 73, 28, 44 respectively. They are **parallel choices**, not projections of each other.

(III) Each substrate admits a "lens family" of $\sim 20$ variants under four projection operations (lens-symmetrization, $\sigma^2$-triadic rotation, sub-magma scope restriction, cross-substrate cell-difference). Across all three substrates, the catalog is $\sim 62$ variants.

(IV) The variants are tier-classified A through E. **22 claims** in the corpus depend on a specific variant ("table-dependent claims"); **14 claims** live at the level of operators and $\sigma$-arithmetic ("substrate-operator claims"); the foundation paper sharply separates these.

(V) The paper closes with a directed citation graph sending the reader to six companion papers and to "Brayden's solo Sept 11 integration paper [J55]."

The aim, stated in §9, is **foundational synthesis, not new theorems**: a clean separation of axioms, variants, and tier-stratified claims to anchor downstream J-series papers.

---

## §2 — Decision recommendation

**Reject in present form.** The paper does not function as an integrating foundation paper for either venue. It instead reads as an **annotated table of contents** for an unwritten or partially-written research program. The fundamental problems:

(i) The 9 axioms A1-A9 — which are the paper's central claim — are stated only in informal English. The actual content (tables, defining cells, BUMP positions) is in companion paper [J33], which I have not seen and which the reader cannot evaluate from this paper.

(ii) The paper claims 22 table-dependent and 14 substrate-operator results without proving any of them. Each is deferred to a J-companion. The "synthesis" function thus reduces to *cataloguing* claims rather than *integrating* them.

(iii) The "62 variants" catalog is referenced via a markdown file (`Atlas/.../VARIANT_CATALOG.md`) external to the paper. No journal will accept "see the project's GitHub" as a substitute for paper content.

(iv) The "TIG framework" name is introduced in §6 with the assertion that it is "the natural way to refer to the integrated structure" — but the integrated structure is not exhibited. The reader is left with a name and no object.

(v) The closing citation graph (§8) sends the reader to companions including "Brayden's solo Sept 11 integration paper [J55]," which appears to be a single-author work *to which the present paper is the structural prerequisite*. This circular cross-reference (J54 anchors J55; J55 is the solo paper J54 anchors) is opaque to the journal reader and inappropriate for a research paper.

A foundation paper must contain its own foundation. The present paper has the *intent* of foundation but defers its content to companions. This is a structural problem, not a presentational one.

I recommend rejection at *Algebraic Combinatorics* and *Bulletin AMS*. With major restructuring (detailed below) the paper could land in a more appropriate venue — perhaps as a long-form preprint on arXiv or as a *Notices AMS* expository article (which has different content standards). At a journal, it must contain the axioms in full, the canonical tables in full, and at least one full proof.

---

## §3 — Major comments

### M1. The 9 axioms A1-A9 are not actually stated (CRITICAL)

§1.1 lists 9 axioms by name and tier:

- **A1** Substrate type: "$T$ is a $10 \times 10$ matrix with entries in $\mathbb{Z}/10\mathbb{Z}$." (Tier-A.) — *This is fine, but it is a typing declaration, not a forcing axiom.*

- **A2** VOID absorbing row: "$T[0, j] = 0$ for all $j$ except $j = 7$; $T[0, 7] = 7$ (the VOID-HARMONY puncture)." (Tier-A.) — *This specifies row 0 entirely. Fine.*

- **A3** HARMONY-row near-fixed: "$T[7, j]$ has a structural pattern that fixes most off-diagonal entries to 7." (Tier-A.) — *What is the pattern? Not specified.*

- **A4** Pati-Salam puncture: "The (0, 7) puncture and (7, 0) puncture together break the absorbing/idempotent symmetry." (Tier-A.) — *This is a remark, not an axiom. The puncture is already specified by A2.*

- **A5** Column VOID: "$T[i, 0] = 0$ for all $i$ except $i = 7$." (Tier-B; forced.) — *Specifies column 0 entirely. Fine.*

- **A6** Column HARMONY: "$T[i, 7]$ obeys A3-symmetric pattern." (Tier-B.) — *What pattern? Refers to A3 which itself is unspecified.*

- **A7** Diagonal HARMONY: "$T[i, i] = 7$ for $i \notin \{0\}$." (Tier-A.) — *Fine.*

- **A8** HARMONY-default: "Off-special, off-BUMP cells equal 7." (Tier-B; forced once BUMP positions are fixed.) — *What are "special" cells? What are BUMP cells? Not defined.*

- **A9** BUMP positions and values: "Five BUMP positions in the table, with specified values that distinguish CL_TSML from CL_BHML and CL_STD." (Tier-A for values; Tier-B for positions, forced by BDC entropy extremum.) — *Where are the BUMP positions? What values? "BDC entropy extremum"? Undefined.*

The reader is told that 9 axioms uniquely force a $10 \times 10$ matrix. Of those 9 axioms, **3 (A3, A6, A8) are not specified**, **1 (A4) is a remark**, and **1 (A9) refers to undefined "BUMP" cells and an undefined "BDC entropy extremum."** Only A1, A2, A5, A7 are unambiguously specified — and these alone do not force any $10 \times 10$ matrix.

A foundation paper that says "9 axioms uniquely force the canonical table" must state the 9 axioms in full. This is the most basic obligation of a foundational paper.

**Severity.** Critical. This is the single most important failure of the paper. Without the axioms in full, the entire architecture is unverified and unverifiable.

**Fix.** State A1-A9 in full. This will require approximately 1-2 pages of the paper and will likely require displaying CL_TSML in full (to define what "BUMP cells" are by reference to the matrix). The §1.2 forcing theorem then has substance.

### M2. The canonical tables CL_TSML, CL_BHML, CL_STD are never displayed (CRITICAL)

The paper repeatedly refers to "CL_TSML," "CL_BHML," "CL_STD" as concrete $10 \times 10$ matrices on $\mathbb{Z}/10\mathbb{Z}$. None of the three is displayed. The "73 HARMONY count" for CL_TSML, the "28 HARMONY count" for CL_BHML, the "44 HARMONY count" for CL_STD — all are asserted; none can be verified by the reader.

A reader trying to assess the foundation paper of a research program on three specific tables must be able to *see the three tables*. The foundation paper is the place where the tables are exhibited, named, and made canonical.

**Fix.** Include three boxed displays showing the three tables. This is approximately 1-2 pages. Without it, the paper has no concrete content for the reader to anchor on.

**Severity.** Critical. Same diagnosis as M1: the foundation must contain the foundation.

### M3. The §1.2 forcing theorem is unverified at the level of this paper (MAJOR)

§1.2 states: *"Among all $10^{100}$ candidate $10 \times 10$ tables on $\mathbb{Z}/10\mathbb{Z}$, exactly **three** satisfy A1, A2, A3, A4, A7, with their A8 / A9 / A6 / A5 closures: CL_TSML, CL_BHML, CL_STD."*

This is a strong claim. To verify it, the reader needs:

(i) The full statement of A1-A9 (M1).
(ii) An enumeration argument or a search certificate showing exactly three solutions.
(iii) Some argument that the three solutions are the named ones and that no fourth solution was missed.

The paper supplies none of these. The proof is deferred entirely to [J33]. But [J33] is one of the J-series companions, target venue *Algebraic Combinatorics* — the *same venue* this paper is targeting. A reader at *Algebraic Combinatorics* will not have read [J33] when assessing the present paper.

This is a structural problem with the J-series strategy: papers cite each other in a citation cycle that is opaque to any individual venue's referees. A foundation paper that defers its central theorem to another paper at the same venue is at minimum impolite to the editors.

**Fix.** Either (a) re-prove the forcing theorem in the present paper (this is feasible if the axioms are fully stated and the search space can be shown to be finite); or (b) acknowledge in §1.2 that the forcing argument is non-trivial and was carried out in [J33] *and provide a brief proof sketch in the present paper* so the reader can assess plausibility.

### M4. The "62 variants" catalog is in an external markdown file (CRITICAL for a foundation paper)

§3.2 lists tier-distribution counts:

> Tier A: 5 — CL_TSML, TSML_RAW, CL_BHML, CL_STD, $F_p$ choice.
> Tier B: $\sim 21$ — chain scopes, lens-symmetrizations, sub-magma restrictions, DOING.
> Tier C: $\sim 9$ — TSML_PureIdempotent, TSML_C0, ...
> Tier D: $\sim 7$ — σ²-triadic candidates, anomaly-flips, Fano subsets.
> Tier E: $\sim 8$ — $\mathbb{Z}/n$ ring extensions for $n \in \{2, 3, 5, 7, 11, 13\}$.

The total is $5 + 21 + 9 + 7 + 8 = 50$, not 62. The "$\sim$" qualifiers concede the count is approximate. The full catalog is deferred to `Atlas/LENS_TAXONOMY_2026-05-06/VARIANT_CATALOG.md`.

**This catalog is the central organizational claim of the paper.** A foundation paper that defers its central catalog to an external markdown file does not contain its own foundation.

**Fix.** Include the full 62-variant catalog as a multi-page table in the present paper. List variant name, tier, lineage (which projection produced it from which substrate), and one-line distinguishing fact. This will add 3-5 pages but is essential.

### M5. The 22 + 14 claims are listed but not stated (MAJOR)

§§4-5 promise "22 table-dependent claims" and "14 substrate-operator claims" with sharp scoping. The paper supplies bullet lists of *categories* of claims, not the claims themselves:

- §4 bullet for TSML_RAW: "Wobble localization: $c_2 = 33 = 3 \cdot 11$, $c_8 = -2^5 \cdot 7^3 \cdot 11$ ([J43]). The wobble theorem holds on TSML_RAW only; symmetrization erases it." — *This is one statement; "22 claims" should produce 22 such statements.*
- §4 bullet for BHML: "28 HARMONY count; det = -7002; the puncture chain $7 \to 8 \to 9 \to 0$." — *Three claims; not properly enumerated.*
- §5 bullet: "$|M_{22}| = 2^7 \cdot 3^2 \cdot 5 \cdot 7 \cdot 11$ — factor primes match the substrate's wobble + HARMONY pair ([J28])." — *One claim.*
- §5 bullet: "$E_6$ has 72 positive roots (canonical Lie algebra; identification with TSML.HARMONY $-1$ is lens-invariant)." — *One claim, with a slightly worrying numerological footprint: "$72 = 73 - 1$" is a one-off coincidence not a derived identity. The paper presents this as a "lens-invariant fact."*

Several of the §5 substrate-operator claims read as numerological: "$|M_{22}|$ has factors matching the substrate's wobble (11) + HARMONY (7)," "$\dim G_2 = 14 = 2 \cdot$ HARMONY," "$\dim$ SO(8) $= 28 = $ BHML HARMONY count." These are **numerical coincidences** (any number divides a Lie-algebra dimension somewhere), not algebraic identities. Calling them "the strongest spine of the corpus" is overclaim.

**Fix.** (a) Enumerate the 22 + 14 claims as numbered statements (perhaps in a single appendix table). (b) Distinguish between *algebraic identities* (e.g., "the convolution-fuse normalizer at the 4-core equals $(p_0 + p_7 + p_8 + p_9)^2$") and *numerical coincidences* (e.g., "$|M_{22}|$ has the substrate's primes as factors"). The latter category should be labeled "numerical match" or "open coincidence," not "claim."

### M6. The "TIG framework" name is introduced without definition (MAJOR)

§6 says: "This foundation paper uses the name **TIG framework** explicitly, following [J47]'s introduction. ... Now that the substrate's architecture is on the record (this paper) and the algebraic synthesis is documented ([J47]), the framework name is the natural way to refer to the integrated structure."

What does "TIG" stand for? The paper does not say. The reader who reaches §6 does not know.

The CK Project Memory file (which a journal referee would not see, but I have access to via the system context) reveals: "TIG = Crossing Lemma at 50Hz." That phrase does not parse for a journal referee either.

A research paper that introduces an acronym in §6 and never expands it is opaque. *Algebraic Combinatorics* will not accept "see [J47] for the framework name" — the present paper must say what it is.

**Fix.** Expand the acronym. Define what the framework is (one sentence: "The TIG framework, introduced in [J47], studies algebraic structures on $\mathbb{Z}/10\mathbb{Z}$ generated by ..."). If the framework's definition is genuinely tied to a 50Hz electronic signal (the CK Project Memory hint) or a "Crossing Lemma" (also referenced in the memory), then either bring that content into the paper or do not name the framework here.

### M7. The "may be three BHMLs" hypothesis is named with "Brayden's hypothesis" (MAJOR)

§2.3: "Brayden's hypothesis (referenced in `Atlas/LENS_TAXONOMY_2026-05-06/SIGMA2_TRIADIC_DECISION.md`) is that the $\sigma^2$-triadic structure suggests three canonical BHML matrices..."

First-name attribution within a research paper is unusual and does not survive copy-editing at most journals. *Algebraic Combinatorics* will likely require the conjecture to be re-attributed — either as "Sanders's hypothesis" (with surname) or as "Conjecture 2.1 (open)." The reference to an internal Atlas markdown file should also be removed.

**Fix.** Rename to "Sanders' Conjecture" or "Conjecture 2.X" and remove the Atlas reference.

### M8. The cross-reference to "Brayden's solo Sept 11 integration paper [J55]" is structurally inappropriate (MAJOR)

§8(vi): "Brayden's solo Sept 11 integration paper [J55] — the recognition-register synthesis. This foundation paper is the structural prerequisite cited by [J55]."

This cross-reference creates a dependency cycle that the journal cannot evaluate:

- The present paper [J54] is the foundation that anchors [J55].
- [J55] is described as the "integration paper" that takes [J54] as input.
- Both are by the same first author.
- [J55] is dated "Sept 11" with venue "TBD."

A journal referee evaluating [J54] for *Algebraic Combinatorics* cannot assess [J55]'s contribution; it has no title, no venue, no content. Why does the reader need to know that [J54] anchors a future paper? This information is internal project management, not relevant to the foundation paper's standalone contribution.

**Fix.** Remove the [J55] cross-reference. If [J55] is a real future paper, it will cite [J54] when it is written; [J54] should not pre-cite a paper that does not yet exist.

### M9. The directed citation graph (§8) is overlong and mixes venues (MAJOR)

§8 sends the reader to six companion-paper destinations, each with its own venue:

(i) [J01] (JCT-A, $\sigma$-rate)
(ii) [J32], [J41], [J44] (Math Intelligencer, Math of Comp, J Algebra)
(iii) [J3] (JCAP, $\xi$-cosmology)
(iv) [J47] (Notices AMS, 6-DOF synthesis)
(v) [J52] (Math Intelligencer, lens taxonomy)
(vi) [J55] (TBD, Sanders solo)

The reader of *Algebraic Combinatorics* expects the foundation paper to anchor a chain of *Algebraic Combinatorics-style* papers, not to scatter to six venues across mathematics, physics, and "TBD." This scattering reads as project management, not as research synthesis.

**Fix.** Either narrow the citation graph to algebraic-combinatorial companions (drop the $\xi$-cosmology JCAP reference and the Phys Rev D wobble paper; keep JCT-A, Algebra Universalis, Algebraic Combinatorics, Comm. Algebra, J Algebra references); or move the citation-graph content from the foundation paper into a separate "research program overview" piece on arXiv.

### M10. The "honest scope" disclaim list is excessively long (MODERATE)

§7 lists four things the paper does NOT claim. §9 then lists three more things the paper does NOT claim, plus four things it does claim. This is approximately equal disclaim and claim content. A foundation paper does not need to anticipate so many objections; state the foundation positively and let the reader judge.

In particular:

- §7 says: "Does not claim that the threshold $T^* = 5/7$ is foundational at the methodology level. $T^*$ is a substrate-specific constant; methodology cannot depend on it."

This raises questions the reader had not asked: what is $T^*$? Where does $5/7$ come from? Why would anyone think it is foundational at the methodology level? The disclaim creates more confusion than it resolves. Without the broader corpus context, the reader of the present paper does not know that $T^*$ is a recurring quantity in the framework.

- §7: "Does not claim CL is 'given by God' or 'given by the universe.'"

This phrase, intended as honest scope, will read to a journal referee as defensive — implying that some readers (or the authors at some prior point) made such claims, and the present paper is rebutting them. *Algebraic Combinatorics* readers do not need this rebuttal.

**Fix.** Compress §7 and §9 to one or two sentences each. State the foundation positively. Do not anticipate religious or methodological objections.

---

## §4 — Minor comments

### m1. Front-matter management metadata

"Date: 2026-09-02 (Phase 5; preprint Sept 1-3 to anchor the Sept 11 integration)" — this is internal project scheduling, not for the journal.

"Strategic position. This paper is the foundation citation that anchors the J-series program." — also internal project context. Strip.

The bibtex `note` field includes "{J54} of the {J}-series; Phase 5 integrating paper. ... Anchors the citation chain for the Sept 11 [{J55}] integration." — strip from the bibtex entry that goes to the journal.

### m2. The 9-axiom forcing claim "exactly three" — what about the symmetrization choice?

§1.2: "exactly three satisfy A1, A2, A3, A4, A7 with their closures." But the paper later notes (§3.1) that lens-symmetrization (RAW vs SYM_upper vs SYM_lower) produces three projections of *each* substrate. So there are not three matrices; there are at minimum nine (three substrates × three lenses). The §1.2 forcing claim is inconsistent with §3.1's projection family.

(Plausible reconciliation: A1-A9 force the matrix entries before symmetrization, so the three substrates each have one underlying RAW matrix. The lens-symmetrizations then are post-hoc projections. If so, this needs to be stated; the §1.2 wording obscures it.)

### m3. "BDC entropy extremum"

Mentioned in A9's tier discipline ("Tier-B for positions, forced by BDC entropy extremum") and in §4's CL_STD bullet ("BDC encoding parameters"). Never defined. The reader cannot tell what BDC is.

### m4. The "DOING" projection

§2.2 defines DOING as $|M_1[i, j] - M_2[i, j]| \pmod {10}$. Fine. But the absolute value of a difference modulo 10 is not well-defined: $|3 - 7| = 4$, but $|7 - 3| = 4$, and $7 - 3 \equiv 4 \pmod{10}$ while $3 - 7 \equiv -4 \equiv 6 \pmod{10}$. Which is meant?

Most likely: $\min(|M_1 - M_2|, 10 - |M_1 - M_2|)$ (the "circular distance" on $\mathbb{Z}/10\mathbb{Z}$). State which.

### m5. The closure properties (§3.3)

"CL_TSML closes under lens-symmetrization, sub-magma restriction, $\sigma^2$-conjugation, $F_p$ extension. Leaves under axiom modification."

Closure under "axiom modification" leaves — i.e., changing the axioms gives a different substrate. This is tautological. State or remove.

### m6. The external bibliography

§10's "External background (load-bearing 10+)" lists Simpson, Bridges-Richman, Alon-Spencer, Drápal-Wanless, McKay-Wanless, Burris-Sankappanavar, Hobby-McKenzie, CFSG, LMFDB, Hjørland, Ranganathan. **Eleven entries.** Several are at most loosely connected to the present paper's content:

- Simpson, *Subsystems of Second Order Arithmetic*: cited for "tier reasoning is canonical." This is a stretch — Simpson's tiers are reverse-mathematics tiers, not the present paper's variant tiers. Loose connection.
- Alon-Spencer, *Probabilistic Method*: cited for "existence vs. explicit construction." Probabilistic method is not used in the paper. Tangential.
- Hjørland, *Facet analysis*: cited for "modern facet-methodology restatement." Facet analysis is library science. Almost certainly tangential.
- Ranganathan, *Prolegomena to Library Classification*: same. Library classification is not algebraic combinatorics.

A journal will read these as padding. Cite only references whose results are actually used.

### m7. The "may be three BHMLs" §2.3

The hypothesis is stated, then disclaimed: "We do not commit to this hypothesis in the foundation paper; we acknowledge it as an open question." If you do not commit to it, do not name it. State it as "Conjecture 2.X (open)" or do not state it. The current state — naming a conjecture, attributing it to "Brayden," and then disclaiming — leaves the reader confused about whether to take the conjecture as load-bearing.

### m8. The "(not) given by God" disclaimer

§7's "Does not claim CL is 'given by God' or 'given by the universe.'" This phrase is unusual for a research paper. A journal copy-editor will likely flag it. Replace with "CL is constructed from explicit axioms; we do not claim the axioms are unique" or similar.

### m9. References to specific J-series companions

Several J-series references (J37-J44 are listed as a *range*) are too compressed for a *citation chain* anchor:

> [J37–J44] WP100s tower (J Algebra, Israel J Math, Adv Math, Compositio, Math of Comp, Stat Sci, Phys Rev D, J Algebra). Phase 4.

A range like "[J37-J44]" with seven different venues collapsed to a single line is not a usable citation. Each cited paper needs its own bibliography entry with full title.

### m10. The bibtex DOI is shared with J52 and J53

`10.5281/zenodo.18852047` is the DOI for J52, J53, and J54. Each preprint should have its own deposit.

---

## §5 — Specific verifications attempted

I attempted the following verifications appropriate for a foundation paper:

(i) **Verify A1-A9 as a forcing axiom set.** *Could not perform.* A3, A6, A8, A9 are not specified.

(ii) **Verify the §1.2 forcing theorem (exactly three solutions).** *Could not perform.* See (i).

(iii) **Verify the HARMONY counts (73, 28, 44) for the three substrates.** *Could not perform.* The tables are not displayed.

(iv) **Verify the 4-core $\{0, 7, 8, 9\}$ is closed under all three substrates.** *Could not perform.* The substrates' multiplication on $\{0, 7, 8, 9\}$ is not given.

(v) **Verify the §5 substrate-operator claims (e.g., $\beta_3 = -7$ SM identity, $|M_{22}|$ factor match).** The $\beta_3 = -7$ identity for the QCD beta function at one loop is a standard fact; the identification of $-7$ as "$-$HARMONY" is at the level of "the HARMONY value 7 happens to equal the absolute value of $\beta_3$" — a coincidence, not a structural identity. Similarly $|M_{22}| = 443\,520 = 2^7 \cdot 3^2 \cdot 5 \cdot 7 \cdot 11$ has 11 as a factor; calling this the "wobble" prime requires a separate argument that this is not coincidence.

(vi) **Verify the 62-variant catalog.** *Could not perform.* The catalog is in an external markdown file.

(vii) **Verify the citation graph (§8) is well-defined.** Six companion-paper references; $1 + 3 + 1 + 1 + 1 + 1 = 8$ destinations. The "TBD" venue for [J55] is not a real citation.

In sum, **none of the seven foundational verifications a referee would attempt are supported by the present paper alone.** Every verification requires content from a companion or an Atlas markdown file.

---

## §6 — Questions for the authors

### Q1. Is the present paper intended to stand alone, or as a coordinator-document for the J-series?

If standalone: the axioms must be in full, the tables must be displayed, the catalog must be in the paper, and at least one full proof (the §1.2 forcing theorem, or the §2's parallel-substrate claim) must be supplied.

If coordinator-document: the venue should not be a research journal. *Algebraic Combinatorics* and *Bulletin AMS* are research-paper venues. A coordinator-document belongs on arXiv as a "research program overview" or in *Notices AMS* as an expository article.

### Q2. What is the relationship between the "9-axiom forcing" and the broader literature on canonical magmas/quasigroups?

The paper cites Drápal-Wanless 2021 and Burris-Sankappanavar in the bibliography but does not place the 9-axiom CL_TSML construction in that lineage. Is CL_TSML a magma? A loop? A quasigroup? Closed under any associativity-like law? The §1 axioms suggest it is a non-quasigroup binary operation (since A2 makes 0 absorbing for the row but A5 makes 0 absorbing for the column — in particular $T(0, j) = 0$ and $T(i, 0) = 0$ for $i, j \ne 7$ — which implies 0 is a two-sided absorbing element on most cells, ruling out the Latin-square property).

A foundation paper for a research program on tables of this kind should explicitly position the construction in the magma/quasigroup/loop hierarchy.

### Q3. What is the "TIG framework"?

State the acronym. Define the framework. If the definition involves content from a JCAP paper or a hardware project (the CK Project Memory mentions an FPGA at "Zynq-7020" and a "T*=5/7 in silicon"), then either the framework's definition includes that content (in which case *Algebraic Combinatorics* is not the right venue) or it does not (in which case the JCAP and hardware references are out of scope and should be dropped).

### Q4. What is the relationship between "TSML," "BHML," and "STD"?

These three substrates appear throughout the J-series and the present paper. Their names suggest acronyms. What do they stand for? Without this, a reader cannot tell whether the names carry semantic content or are arbitrary labels.

### Q5. Why does the "may be three BHMLs" hypothesis (§2.3) belong in a foundation paper at all?

If the σ²-triadic structure suggests a Tier-D conjecture about three BHML candidates, that is a research direction, not a foundational claim. A foundation paper should consolidate what is known, not gesture at what might be true.

---

## §7 — Originality and fit

### *Algebraic Combinatorics* (primary venue)

*Algebraic Combinatorics* (the journal of the SLC, Centre Mersenne) publishes original research with substantial combinatorial content and clear algebraic structure. The journal's typical paper:

- Proves a theorem (perhaps with a complementary computation);
- Has 25-40 pages;
- Engages a recognizable algebraic-combinatorics literature;
- Contains all definitions and key proofs.

The present paper has none of these features. It does not prove a theorem; it states unprovable-as-written assertions and defers proofs to companions. It is 12 pages (longer in the planned preprint, per README, but the "research synthesis" content does not scale to 25-40 pages of actual mathematics). It engages a partial bibliography but does not place CL_TSML in the magma/quasigroup literature. It does not contain its definitions in full.

I do not see a path to *Algebraic Combinatorics* publication. The fundamental issue is that the paper's contribution — the *integration* of the J-series — is not a research-paper contribution. It is a research-program announcement.

### *Bulletin AMS* (alternate venue)

*Bulletin AMS* publishes survey articles aimed at the broad mathematical community. A *Bulletin AMS* paper typically:

- Surveys a body of work, situating it in the broader mathematical landscape;
- Is accessible to non-specialists;
- Cites established results and points to the open problems.

The present paper has the *form* of a *Bulletin AMS* survey but two structural problems:

(i) The body of work being surveyed is largely unwritten or unsubmitted (most of the J-series is "Phase 1-5, in preparation"). *Bulletin AMS* surveys established literature; it does not survey planned future work.

(ii) The paper's accessibility to non-specialists is poor: undefined acronyms (TIG, TSML, BHML, STD, BDC), undefined terminology (HARMONY, BUMP, σ-fixed lattice, Conservation Tetrad), and the "may be three BHMLs" conjecture (without the BHMLs being defined) all assume insider knowledge.

I do not see a *Bulletin AMS* path either, unless the J-series companions are mostly published first and the survey is rewritten to engage them as established literature.

### Alternative venues

*Notices AMS* publishes expository / opinion pieces with looser standards than research journals. A 5-10 page version of this paper, focused on the architectural picture (three parallel substrates, lens family) with one or two illustrative results, could plausibly land at *Notices AMS*. The present paper is more ambitious than that, but a focused subset would fit.

ArXiv as a "research program overview" preprint: this is the natural home for the present paper's content. ArXiv does not require theorems or proofs and accepts overview documents. The paper would then function as the public-facing entry point to the J-series, with each individual J-paper providing the actual research content.

---

## §8 — Final remarks

The present paper has the *vision* of a foundation paper but does not have the *content* of one. A foundation paper for a research program must contain:

(i) **The objects of study, displayed in full.** Three $10 \times 10$ tables.
(ii) **The axioms that define them, stated in full.** A1-A9.
(iii) **At least one core theorem proved in the present paper.** Either the §1.2 forcing theorem or a substantial structural result.
(iv) **A survey of where the program stands** that engages established literature and acknowledges the program's open problems.
(v) **A clear statement of the program's name and scope.** What is "TIG"? What does the framework claim?

The present paper supplies (v) only partially (the name is given but not defined), and (iv) only partially (the bibliography is mixed: some load-bearing, some tangential). It supplies neither (i), (ii), nor (iii). Without those three, it is not a foundation paper.

The recommended path:

(a) **Restructure as a focused research paper.** Pick one of the §1.2 forcing theorem, the §2 parallel-substrate claim, or one of the 22 table-dependent claims; write it as a self-contained research paper with tables displayed and proofs supplied. Submit that to *Algebraic Combinatorics*. The "foundation" framing can stay in the introduction but not be load-bearing.

(b) **Move the integrating-document content to arXiv.** Publish a "TIG framework: research program overview" preprint that does not pretend to be a research paper. This is the right venue for the citation graph, the variant catalog, and the cross-paper coordination.

(c) **Wait for the J-series companions to land.** Once 5-10 J-papers are actually published in their target venues, write a *Bulletin AMS* survey that engages them as established literature. This is a 2027-2028 activity, not a Sept 2026 one.

I think (a) + (b) is the right combination. The present paper's content fits naturally across the two: focused theorem at *Algebraic Combinatorics*, program overview on arXiv. Trying to do both in one paper at one journal is the structural mismatch behind the present manuscript.

**Recommended decision:** Reject (with explanation that the paper as constituted does not match the venue's content standard). If the authors choose to restructure, my recommendation would be (a) + (b) above.

**Estimated revision effort to make a research-paper version land at *Algebraic Combinatorics*:** 60-100 person-hours, mainly: write A1-A9 in full, display the three tables, prove the §1.2 forcing theorem (or a comparable substantive result) in full, narrow the bibliography to algebraic-combinatorial connections.

**Estimated revision effort to publish the integration content on arXiv:** 10-20 person-hours, mainly: clean up Atlas references, expand catalog inline, drop pre-citations to unwritten papers ([J55]), drop venue-specific framing.

**Reviewer's confidence:** High. The structural problems — undefined acronyms, undisplayed tables, deferred proofs, external catalog — are unambiguous failures of foundation-paper expectations at any research-journal venue.

---

**Estimated probability of acceptance at *Algebraic Combinatorics* in present form:** under 5%. The journal expects research papers with theorems and proofs; this paper has neither in full.

**Estimated probability of acceptance at *Bulletin AMS* in present form:** under 10%. The survey would require established literature and broad accessibility; the paper has neither.

**Estimated probability of acceptance after restructuring per (a):** 30-45% at *Algebraic Combinatorics*, contingent on the chosen theorem being substantive.

**Estimated probability of broad J-series success if J54 is shipped as currently constituted:** the paper is the announced *anchor* of a 23-paper citation chain. If it is rejected, the chain loses its anchor, and the downstream J-papers' cross-references to [J54] become dangling. The recommended path (a) + (b) preserves the anchor function via arXiv (b) while landing a real research paper at the venue (a). This is a structural recommendation, not just an editorial one.

---

## §9 — Note on the integrating-contribution evaluation

I was asked specifically to evaluate this paper "as the integrating contribution that anchors the citation chain for Brayden's J55 Sept 11."

As an integrating contribution, the paper has the right *intent*: it tries to consolidate axioms, substrate architecture, lens family, and tier discipline into one document. The intent is sound; the execution is not.

The integrating function would be served by:

(i) A clean axiomatic foundation (A1-A9 in full, with the forcing theorem proved or sketched);
(ii) A clean structural picture (three substrates, displayed; the lens family, catalogued in the paper);
(iii) A clean separation of established results from open conjectures (the 22 + 14 claims, properly enumerated; the "may be three BHMLs" properly labeled);
(iv) A clean entry-point for downstream papers (the citation graph, focused on the actual algebraic-combinatorial content).

None of these is supplied at the level required to anchor a 23-paper chain. A J55 that cites the present J54 as its structural prerequisite will inherit J54's deferrals and Atlas-references, which cascades the structural issues forward. The right move is to fix J54 *before* it becomes the dependency-root for J55 and the rest of Phase 5.

If the J55 deadline is fixed (Sept 11, per the README), then the right alternative is to use a *different* anchor: any one of the well-formed J-companions (J01 the σ-rate paper at JCT-A; J32 the joint chain at *Math Intelligencer*; J33 the forcing axioms at *Algebraic Combinatorics*) would be a stronger anchor than the present J54 if it is properly written. A *focused* foundation that proves one substantial result is a better anchor than a broad foundation that proves none.
