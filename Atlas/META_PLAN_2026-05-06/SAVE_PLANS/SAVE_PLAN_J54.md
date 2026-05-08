# SAVE PLAN — J54: Foundation Paper (Three-Substrate + Lens Family + Forcing Axioms)

**Date:** 2026-05-07
**Brayden directive:** "find a reason to keep and fix every paper" — and specifically: **DO NOT recommend dropping J54.** This save plan honors that directive.
**Manuscript:** `Gen13/targets/journals/J_series/J54/manuscript/J54_foundation_paper.md`
**Referee:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J54_AlgComb_BullAMS_FreshEyes.md` (REJECT in present form)
**Author lane:** Sanders + Gish.

**Note on referee accuracy:** Brayden has flagged that the referee's claim "A1-A9 axioms not actually stated" is partially incorrect. Direct check of `manuscript/J54_foundation_paper.md` lines 40-48: A1-A9 are listed by name, tier, and a one-line description each. What the referee is pointing at is that **A3, A6, A8, and A9 are not specified at the level of mathematical precision needed to verify the §1.2 forcing theorem** ("structural pattern that fixes most off-diagonal entries to 7" is not a pattern; "off-special, off-BUMP cells equal 7" requires defining "special" and "BUMP"). The referee's phrasing is sloppy ("not stated"), but the substance — that A3, A6, A8 need expansion to formal specifications — is correct. The save plan addresses what the referee actually means, not the strict reading of his claim.

---

## §1 — Why save?

J54 is the **load-bearing structural anchor** for the J-series Phase 5 cluster and Brayden's solo Sept 11 J55 integration paper. Killing J54 cascades dependencies:

1. The directed citation graph (manuscript §8) routes 23+ J-papers through J54 as their structural prerequisite.
2. J55 (Brayden's solo Sept 11 integration) is described in the manuscript as taking J54 as input — the recognition-register synthesis without the foundation underneath.
3. The collaborator's FAMILY_STRUCTURE_v1.md analysis (2026-05-07) explicitly identifies the foundation-paper register as where the **5 conjoint membership criteria** and **6 boundary walls** of the TIG family belong. Without J54, that structural articulation has no home.
4. Three substrates (CL_TSML, CL_BHML, CL_STD) have never been documented together at the axiomatic level in the J-series. J54 is the only paper that does this.

The fresh-eyes referee's REJECT verdict is correct on diagnosis (the present manuscript has too much deferred content, undefined acronyms, and missing tables for *Algebraic Combinatorics*) but the diagnosis is **fixable**. The referee himself laid out path (a): "Restructure as a focused research paper. Pick one of the §1.2 forcing theorem, the §2 parallel-substrate claim, or one of the 22 table-dependent claims; write it as a self-contained research paper with tables displayed and proofs supplied. Submit that to *Algebraic Combinatorics*." That path does not require dropping J54 — it requires sharpening it.

The collaborator's FAMILY_STRUCTURE_v1.md gives a second path: J54 can be retargeted as the **Foundation Paper for the TIG Family**, written in the precise lineage of Drápal-Wanless 2021 *JCTA*, with the family-membership criteria replacing the lens-family catalog as the load-bearing structural content. This is a stronger paper than the current manuscript and is not what the referee was reviewing.

Both paths preserve J54. The choice between them is venue-strategic: Path A (focused theorem at *Algebraic Combinatorics*) wins on referee defensibility; Path B (family-foundations at *Algebraic Combinatorics* in the Drápal-Wanless lineage) wins on intellectual coherence with the J-series. Recommendation below: take **Path B**, with elements of Path A folded in.

---

## §2 — Specific fixes (mapped to referee findings + Brayden's correction)

**(a) EXPAND A3, A6, A8, A9 with full formal specifications** (referee M1 — CRITICAL; Brayden's correction: axioms ARE listed but need expansion).

For A3 (HARMONY-row near-fixed): replace "structural pattern that fixes most off-diagonal entries to 7" with **the explicit cell-by-cell specification**:
- $T[7, 0] = 0$ (puncture at (7, 0); paired with the (0, 7) puncture from A2).
- $T[7, j] = 7$ for $j \in \{1, 2, 3, 4, 5, 6, 8, 9\} \setminus \{\text{BUMP positions in row 7}\}$.
- BUMP positions in row 7 (per A9) take their A9-specified values.

For A6 (Column HARMONY): replace "obeys A3-symmetric pattern" with the **explicit column-7 specification analogous to A3**, derived from commutativity-after-symmetrization (Tier-B).

For A8 (HARMONY-default): replace "off-special, off-BUMP cells equal 7" with **a precise specification of "special" cells** = the seven-cell special set (row 0, column 0, row 7, column 7, diagonal, BUMP cells). Then state: $T[i, j] = 7$ for $(i, j)$ outside the special set.

For A9 (BUMP positions and values): give the **five (i, j) coordinates of the BUMP cells** explicitly and the **three families of BUMP-value choices** that distinguish CL_TSML / CL_BHML / CL_STD. Specifically:
- BUMP positions: (define the five cells with reference to the displayed table — see (b) below).
- TSML BUMP values: [list the five values for CL_TSML].
- BHML BUMP values: [list the five values for CL_BHML].
- STD BUMP values: [list the five values for CL_STD].

This expansion is approximately 1-1.5 pages and turns A1-A9 from a list into a verifiable axiom set.

**(b) DISPLAY the three canonical tables CL_TSML, CL_BHML, CL_STD inline** (referee M2 — CRITICAL; Brayden's checklist).

The §1 introduction must contain three boxed displays (each ~10 lines of LaTeX `array`):
- **Table 1: CL_TSML.** $10 \times 10$ matrix on $\mathbb{Z}/10\mathbb{Z}$. HARMONY count = 73. Boxed and labelled.
- **Table 2: CL_BHML.** $10 \times 10$ matrix. HARMONY count = 28. Boxed and labelled.
- **Table 3: CL_STD.** $10 \times 10$ matrix. HARMONY count = 44. Boxed and labelled.

Adding the tables takes ~1.5 pages of paper space and is the single highest-leverage fix. After this, every claim in §§1-5 is anchored to displayed objects rather than to external Atlas references.

**(c) BREAK the [J33] forcing-theorem citation cycle** (referee M3 — MAJOR).

Two acceptable approaches:
- **(c1)** Prove the §1.2 forcing theorem in J54 itself. With A1-A9 expanded per (a) and the three tables displayed per (b), the forcing argument reduces to verifying that exactly three cell-by-cell-distinct candidate matrices satisfy A1, A2, A3, A4, A7 with their A8/A9/A6/A5 closures. This is a finite enumeration; the proof can be 3-4 pages.
- **(c2)** Cite [J33] with a stable arXiv identifier and a one-paragraph proof sketch in J54. Acceptable if [J33] is on arXiv before J54 submits.

Recommendation: **(c1)**. Proving the forcing theorem inside J54 turns it into a substantive research paper (not just a coordinator-document) and serves the referee's path (a). [J33] then becomes a co-citing companion rather than a load-bearing dependency.

**(d) STRIP "Brayden's hypothesis" first-name attribution** (referee M7 — MAJOR; Brayden's checklist).

§2.3 currently says "Brayden's hypothesis (referenced in `Atlas/.../SIGMA2_TRIADIC_DECISION.md`)..." — replace with **"Conjecture 2.1 (Sanders)"**. Drop the Atlas reference. State the conjecture as an open question:

> **Conjecture 2.1 (Sanders).** Under the σ²-triadic decomposition, three canonical BHML matrices exist, corresponding to the three positions (BEING / DOING / BECOMING) in the σ² rotation. The current state: three search-found candidates (Tier-D) exist, but a forcing argument promoting one of them to canonical (Tier-A) status is not yet known. Open.

**(e) HOLD preprint until [J47] (6-DOF) and [J33] (forcing) are at least on arXiv** (Brayden's checklist + referee M3).

The current submission timeline (Sept 1-3 to anchor Sept 11 J55) is risk-aggressive given that [J47] is a Phase 5 paper that may not be ready. Two scenarios:
- **(e1)** If [J47] and [J33] both reach arXiv by Aug 15: submit J54 Sept 1-3 as planned.
- **(e2)** If either is delayed: J54 holds until both are on arXiv. The Sept 11 J55 paper then either delays in step or shifts to citing J54's preprint draft (with a "submitted" rather than "published" status).

This is project management; the referee does not directly demand it, but the citation cycle (J54 cites [J47] and [J33]; both cite back) is unforgivable to a journal referee unless the cited papers exist publicly.

**(f) REMOVE the [J55] cross-reference** (referee M8 — MAJOR).

§8(vi) currently says "Brayden's solo Sept 11 integration paper [J55] — the recognition-register synthesis. This foundation paper is the structural prerequisite cited by [J55]." This is internal project management.

Replace with: nothing. Drop the [J55] bullet entirely. [J55] when written will cite J54; J54 has no need to pre-cite J55.

**(g) NARROW the citation graph (§8) to algebraic-combinatorial companions** (referee M9 — MAJOR).

Drop the [J3] JCAP cosmology pointer and the Phys Rev D wobble pointer from §8; these are out-of-venue distractions for *Algebraic Combinatorics*. Keep:
- [J01] σ-rate (JCT-A) — directly relevant.
- [J32] joint chain (Math Intelligencer) — directly relevant.
- [J33] forcing axioms — relevant if (c1) is taken; relevant pointer if (c2).
- [J35] 4-core fusion-closure (J Algebra) — directly relevant.
- [J47] 6-DOF synthesis (Notices AMS) — relevant as the framework's algebraic-content integration.

Remove physical-application companions from the foundation paper's citation graph. They belong in a companion physics paper.

**(h) DEFINE "TIG" before §6** (referee M6 — MAJOR; referee Q3).

Currently §6 introduces "the TIG framework" by name without expanding the acronym or defining the framework. Move the framework introduction to §0 or §1.1 with:

> **The TIG framework** (Sanders 2026, [J47]) studies the family of finite commutative non-associative magmas on $\mathbb{Z}/10\mathbb{Z}$ (and ring extensions per [J34]) characterized by 4-core preservation, α-bounded non-associativity, and HARMONY-attracting iteration under T+B-mix at α = ½. The substrate's name has been retained from the framework's conception; for the present paper, "TIG" is best read as **the family of magmas defined by the five conjoint membership criteria** of `FAMILY_STRUCTURE_v1.md` §1.

Adding this paragraph clarifies what the framework is for the journal reader without requiring them to read [J47].

**(i) ADOPT the FAMILY_STRUCTURE_v1.md framing** (NEW; not in referee report).

The collaborator's analysis (2026-05-07) provides the **strongest available framing** for J54 as a foundation paper. Adopt:
- **§1.1: The five conjoint membership criteria.** State all five (substrate / commutativity / 4-core preservation / α-bounded non-associativity / HARMONY-attracting iteration) as the family's defining characteristics.
- **§1.2: The center.** State the 4-core $\{V, H, Br, R\} = \{0, 7, 8, 9\}$ at α_M = ½ as the algebraic center (per §2 of FAMILY_STRUCTURE_v1.md), with the closed-form attractor $h/\beta = 1+\sqrt{3}$ from D78 Galois proof.
- **§1.3: The six boundaries.** Trivial-rank / α_A boundary / lens (RAW vs SYM) / commutativity / substrate-size / encoding-runtime — six distinct walls per §3 of FAMILY_STRUCTURE_v1.md.
- **§1.4: The bimodal α_A gap conjecture.** State as Conjecture 1.1 (Sanders + collaborator), per §4.1 of FAMILY_STRUCTURE_v1.md.

This adoption transforms J54 from an internal-project coordinator into a **family-foundations paper in the Drápal-Wanless 2021 lineage** — the precise venue-target for *Algebraic Combinatorics*. The referee's M1-M9 issues become naturally addressed by this restructuring, because the foundation now has a definable object (the family) with criteria (the five) and a concrete open question (the bimodal gap).

**(j) STRIP front-matter and bibtex management metadata** (referee m1).
- Remove "Date: 2026-09-02 (Phase 5; preprint Sept 1-3 to anchor the Sept 11 integration)" from front matter.
- Remove "Strategic position. This paper is the foundation citation that anchors the J-series program."
- Strip the bibtex `note` field's J55 / Phase 5 references.

**(k) RESOLVE the DOING projection's mod-10 ambiguity** (referee m4).

§2.2 defines DOING as $|M_1 - M_2| \pmod{10}$. State which: $\min(|M_1 - M_2|, 10 - |M_1 - M_2|)$ (circular distance) is the natural choice. Replace with this explicit definition.

**(l) NARROW the external bibliography** (referee m6).

Remove or relegate to a footnote: Simpson (loose connection); Alon-Spencer (probabilistic method not used); Hjørland (library science); Ranganathan (library science). Keep Drápal-Wanless 2021, McKay-Wanless 2005, Burris-Sankappanavar (universal-algebra textbook), Hobby-McKenzie (structural classification), CFSG (gold-standard structure), LMFDB (database).

---

## §3 — Revision time

Per referee estimate: **60-100 hours** for a research-paper version at *Algebraic Combinatorics*. Distribution:

- (a) Expanding A3, A6, A8, A9 with full formal specifications: 8-12 hours.
- (b) Displaying CL_TSML, CL_BHML, CL_STD inline: 2-3 hours (mostly LaTeX layout).
- (c1) Proving the §1.2 forcing theorem in J54: 15-25 hours (depends on whether the proof is enumeration or has structure).
- (i) Adopting the FAMILY_STRUCTURE_v1.md framing: 12-18 hours (largest single content addition; includes the five criteria, six boundaries, and the bimodal α_A gap conjecture properly stated).
- (d), (f), (g), (h), (j), (k), (l) cleanup: 8-12 hours total.
- (e) coordination with [J47] / [J33] preprint timing: not engineering hours but calendar-blocking.

Realistic completion target: **6-10 working sessions** of focused writing, which fits within the August window before Sept 1-3 submission **if** [J47] and [J33] preprints are on arXiv by Aug 15. If they are not, hold to October per (e2).

---

## §4 — PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN:** (After (c1) revision) The 9-axiom set A1-A9 forces exactly three canonical $10 \times 10$ tables on $\mathbb{Z}/10\mathbb{Z}$: CL_TSML, CL_BHML, CL_STD. The 4-core $\{0, 7, 8, 9\}$ is closed under all three. The five conjoint membership criteria of `FAMILY_STRUCTURE_v1.md` §1 jointly define the TIG family.
- **COMPUTED:** Brute-force enumeration confirming exactly three tables satisfy A1-A9 (script + reproducibility statement). HARMONY counts (73, 28, 44) verified by direct count on each displayed table. 4-core closure verified by all 64 binary products on $\{0, 7, 8, 9\}^2$.
- **STRUCTURAL RHYME:** The bimodal α_A gap (no canonical Z/10Z table at α_A ∈ (0.5, 0.87)) is empirically observed across all enumerated members; conjecturally a structural exclusion zone, but the conjecture is open and stated as such (FAMILY_STRUCTURE_v1.md §4.1).
- **OPEN:** **Conjecture 1.1 (Bimodal α_A gap).** No commutative magma on Z/10Z preserving the 4-core has α_A ∈ (0.5, 0.87). Either prove (giving the structural exclusion theorem) or exhibit a counterexample. Per FAMILY_STRUCTURE_v1.md §4.2, this conjecture is the natural follow-on paper to J54 (proposed J56 or Phase 5 insertion).

---

## §5 — Lens-ownership paragraph (per J_PAPER_BOILERPLATE.md §5.5)

This paper works on $\mathbb{Z}/10\mathbb{Z}$ with the operator labels (VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET) and the canonical (TSML, BHML, STD) substrate triple. These choices are not derived from first principles; they reflect a structural reading of the substrate motivated by the framework's ten-operator decomposition and the resulting four-core preservation under both TSML and BHML. The 9-axiom forcing theorem (§1.2) is a theorem on this specific substrate; analogous forcing theorems would exist on other substrate-and-table choices. The framework's claim is that this particular substrate-and-triple-choice produces theorems with surprising downstream connections (Galois D_4 over LMFDB 4.2.10224.1, the 1+√3 closed-form attractor, the bimodal α_A gap conjecture, F_p ring extensions per D74). Whether other substrate choices give similarly rich connections is open. The framing follows the Drápal & Wanless (2021, *JCTA* 184, 105510) line of work on small finite commutative non-associative structures.

---

## §6 — Retitle / retarget

**Old title:** "The Foundation Paper: Three-Substrate Architecture, Lens Family, and the CL Forcing Axioms on $\mathbb{Z}/10\mathbb{Z}$"

**New title (recommended):** "Forcing Axioms and the Family of Commutative Non-Associative Magmas on $\mathbb{Z}/10\mathbb{Z}$ Preserving a Designated 4-Core"

(Replaces "Three-Substrate Architecture, Lens Family" with "Family of Commutative Non-Associative Magmas... Preserving a Designated 4-Core" — a description that *Algebraic Combinatorics* recognizes from the Drápal-Wanless lineage. Drops "Foundation Paper" from the title because journal titles do not advertise being a foundation paper; the introduction does that work.)

**Old venue (primary):** *Algebraic Combinatorics* (referee: under 5% in present form)
**Old venue (alternate):** *Bulletin AMS* (referee: under 10%)

**New venue (primary):** *Algebraic Combinatorics* (after revisions per (a)-(l), referee estimates 30-45%; with FAMILY_STRUCTURE_v1.md framing per (i), this is plausibly higher).

The venue choice does NOT change. *Algebraic Combinatorics* is the correct venue for a paper on small finite commutative non-associative magmas in the Drápal-Wanless lineage; what changes is what the paper actually delivers (per §2 above) so that the referee at *Algebraic Combinatorics* finds a research paper rather than a coordinator-document.

**New venue (alternate):** *Bulletin AMS* — only if the paper is published *after* J01, J32, J33, J35 are in print, so that a Bulletin survey has established literature to engage. This is a 2027-2028 path, not the Sept 2026 path. Defer.

**Fallback:** *Discrete Mathematics* or *Journal of Algebra* (more tolerant of finite-algebraic structural papers; referee did not list these but they are plausible if *Algebraic Combinatorics* declines).

---

## §7 — Submission gate

This paper does NOT submit until:
- [J47] (6-DOF synthesis at *Notices AMS*) is on arXiv with a stable identifier.
- [J33] (forcing axioms at *Algebraic Combinatorics*) is on arXiv with a stable identifier OR (c1) is complete (the forcing theorem is proved inside J54 itself).
- (a)-(b) are complete (axioms expanded; tables displayed inline).
- (i) FAMILY_STRUCTURE_v1.md framing is integrated into §1.
- Cover letter is rewritten to identify the paper as a research paper in the Drápal-Wanless 2021 lineage, not as a "foundation paper" — the latter phrasing triggers the referee's "annotated table of contents" reading.

**Earliest realistic submission:** Sept 1-3, 2026 contingent on (e1); October 2026 if (e2). Brayden's J55 deadline (Sept 11) is honored by the (e1) path; the (e2) path requires J55 to either delay or to cite J54 as preprint-status rather than submitted.

---

## §8 — Why this save plan reads as positive recovery

The fresh-eyes referee gave J54 a definitive REJECT but laid out a clear path: prove a substantial theorem, display the canonical objects, narrow the citation graph, define the framework. The referee's path (a) — "restructure as a focused research paper" — is consistent with this save plan; we additionally adopt FAMILY_STRUCTURE_v1.md's family-foundations framing, which gives the paper a stronger structural backbone than the original lens-family-catalog framing.

**The single most important upgrade:** moving from "coordinator-document for the J-series" to "research paper in the Drápal-Wanless 2021 lineage that proves the 9-axiom forcing theorem and states the bimodal α_A gap conjecture." This change makes J54 a real *Algebraic Combinatorics* paper, not a journal-rejected program announcement.

The Brayden directive "DO NOT recommend dropping J54" is honored: this plan keeps J54 as the structural anchor of the J-series, sharpens its content from coordinator-document to research-paper, and replaces the lens-family-catalog organizational principle with the family-membership-criteria principle from FAMILY_STRUCTURE_v1.md. The result is a stronger paper at the same venue with a substantially higher acceptance probability.

**Recommendation:** SAVE per Path B (FAMILY_STRUCTURE_v1.md framing + (a)-(l) revisions). Hold submission until (e1) preprint coordination is confirmed.
