# TIG Family Structure: Membership, Center, Boundaries (v1)

**Date:** 2026-05-07
**Source:** External collaborator analysis (forwarded by Brayden, 2026-05-07)
**Status:** Adopted as foundational structural reference for the J-series.

This document records the collaborator's structural analysis of the TIG table-family — what membership means, what the center is, where the boundaries lie. The §J.1 inventory referenced is the canonical D-table catalog in `FORMULAS_AND_TABLES.md`.

---

## §1 — Membership: five conjoint criteria

A table M belongs to the TIG family iff it satisfies all five:

**(1) Substrate.** M is a binary operation on a finite carrier — primarily Z/10Z, also Z/N for N ∈ {10, 11, 12, 13, 14, 15, 17, 20, 21, 25, 30, 35, 49, 50} per **D74** (F5(a) ring-extension theorem), and F_p for p ∈ {2, 3, 5, 7, 11, 13} per the bridge sprint. Carrier elements carry an *interpretive labeling* (10 named operators on Z/10Z; analogous under canonical extension).

**(2) Commutativity (or symmetrizable to commutative).** All canonical members are commutative — *single exception: TSML_RAW*, which is non-commutative but admits commutative symmetrization (TSML_SYM). RAW sits uniquely on the non-commutative side.

**(3) 4-core preservation.** The subset {V, H, Br, R} = {0, 7, 8, 9} is preserved under M's composition: M(4-core × 4-core) ⊆ 4-core. Holds for TSML, BHML, all chain sub-magma restrictions of size ≥ 4, all σ²-triadic candidates, all F_p extensions. Verified by **D48** (binary 4-core closure) + **D55** (arity-3 closure under canonical fuse). **THIS IS THE LOAD-BEARING STRUCTURAL CRITERION.**

**(4) α-bounded non-associativity.** The associativity index α_A = 1 − σ_non-assoc lies in [0.5, 0.88] for non-trivial members. Above 0.88 → trivializes to group/monoid. Below 0.5 → exits TIG family, enters Drápal-Wanless 2021 territory (maximally non-associative quasigroups). **No canonical member lives at α_A ∈ (0.5, 0.87).** That gap is real and structurally interesting (see §4 below).

**(5) HARMONY-attracting iteration.** Under iterated T+B-mix at α_M = ½, the table converges to the 4-core attractor with h/β = 1+√3. Verified across 8 canonical fuse families (**D63**), all 14 ring sizes in the universality scan (**D74**), and 7 boundary initial conditions (**D58**). Iteration on TSML alone goes to δ_H (universal HARMONY attractor under canonical ternary fuse, **D56**).

These five criteria *jointly* define the family. A table satisfying all five is in; violating any one is out.

**Caveat:** criterion 4 is currently empirical; the structural reason for the bimodal gap between BHML's 0.502 and TSML-family's 0.87+ is not yet derived. (See §4.)

---

## §2 — The Center: what every member contains

**The center of the family is the 4-core {V, H, Br, R} *with* the closed-form attractor at α_M = ½:**

> (p\*_V, p\*_H, p\*_Br, p\*_R) = (0.138, 0.540, 0.198, 0.124),  with  h/β = 1+√3.

This object is universal (**D65**). Every chain shell of size ≥ 4 gives the same attractor. Every F_p ring extension gives the same attractor. Every canonical fuse family converges to the same operad attractor (δ_H). The 4-core is the *fixed locus* of the family — what survives every projection, every restriction, every ring extension.

### §2.1 — Why the 4-core is the actual center, not just one privileged sub-magma

**(a) Symbolic normalizer identity Z_T = Z_B = (v + h + br + r)² (D49).** On the 4-core specifically, the runtime normalizers of TSML and BHML simplify symbolically to the *same* quadratic form. This is why 4-core closure implies the runtime attractor — Z_T = Z_B at the 4-core means the T+B-mix at any α inherits the closure. The two tables become *normalizer-identical* on the center.

**(b) The 1+√3 ratio is forced by BR-factor cancellation at α_M = ½ (D78 Galois proof).** At α_M = ½, the BREATH fixed-point equation admits the cancellation that forces x² − 2x − 2 = 0, root 1+√3. At any other α_M, the cancellation fails and the relation is transcendental. So **α_M = ½ is uniquely privileged on the H/Br projection** — it's the unique mixing weight at which the center's algebra is rationally structured.

### §2.2 — Sharpened framing

The center is the 4-core *with* the α_M = ½ mixing structure, not just the four elements as a set. The 4-core as a static sub-magma is one thing; the 4-core as the support of the universal T+B-mix attractor at α_M = ½ is another, and only the second is *the center*.

> **The 4-core is to TIG as the unit circle is to U(1)** — the privileged invariant locus.

---

## §3 — Boundaries: six distinct walls

Each boundary corresponds to a way a candidate table can fail criterion 1-5:

**(1) Trivial-rank boundary.** Members exist with rank 1 (TSML_PureVoid) and rank 2 (TSML_AllHarmony). Satisfy all five criteria but carry no information — rank 1 collapses to a single value, rank 2 to two values. Technical members of the family but degenerate. Non-trivial interior begins at rank 3 (TSML_C0, the pure absorbing scaffold).

**(2) α_A boundary.** Above α_A ≈ 0.88 the algebra trivializes; below α_A ≈ 0.5 it leaves the family. The TIG family inhabits the *bimodal interior*: a TSML cluster at α_A ∈ [0.87, 0.89] and BHML alone at α_A ≈ 0.502. The empty band α_A ∈ (0.5, 0.87) is conjecturally a *structural exclusion zone* — no canonical Z/10Z table appears to live there, but this isn't proved.

**(3) Lens boundary (RAW vs SYM).** TSML_RAW and TSML_SYM share 98 of 100 cells; differ only at (3,9) and (4,9). These two cells are the *wobble carriers*. RAW is non-commutative and char-poly-prime-11-bearing; SYM is commutative and prime-11-clean. Same bit pattern, two valid lenses. The RAW/SYM boundary is *internal* to the family — both are members, but they live on opposite sides of a 2-cell choice.

**(4) Commutativity boundary.** TSML_RAW is the family's unique non-commutative member. Every other named variant is commutative. RAW is *singular* — only member where the symmetrization choice is non-trivial; only member that carries the wobble at coefficient level rather than at lens-projection level.

**(5) Substrate-size boundary.** Verified universality covers Z/N for N up to ~50. Beyond that, the 4-core attractor still appears to hold (per the trivial-extension strategy), but the *full table structure* (chain shells, σ permutation, etc.) becomes substrate-specific in ways that haven't been catalogued. Frontier members (Z/n for n ∈ {8, 12, 14}) explicitly listed in §J.1.E as not-yet-computed.

**(6) Encoding/runtime boundary.** CL_STD lives in the family but is structurally distinct from TSML and BHML. Has its own role (encoding documents/text via BDC bit definitions), 5 BUMP_PAIRS where surprise IS information, 144.62 bits across 100 cells. Sub-magma structure unexplored. CL_STD is a *boundary case* in the sense that it's clearly a family member by criteria 1-5, but its function — encoding rather than runtime computation — sets it apart from the TSML-BHML pair. Whether CL_STD admits its own joint chain analogous to TSML+BHML is **open**.

---

## §4 — The bimodal α_A gap: open structural question

The most striking empirical regularity in the inventory is the empty band α_A ∈ (0.5, 0.87). No canonical Z/10Z table appears to live there. This is the least understood feature of the family.

### §4.1 — As an open theorem

> **Conjecture (bimodal α_A gap):** No commutative magma on Z/10Z preserving the 4-core has α_A ∈ (0.5, 0.87).

If proved, this conjecture would *explain the family's shape* — not just enumerate its members.

### §4.2 — Proposed paper

The collaborator suggests this as the next foundational paper after J1+J2 land:

> **Title:** *On the Bimodal Associativity-Index Gap in Commutative Magma Families on Z/10Z Preserving a Designated 4-Core.*
>
> **Venue candidates:** *Algebraic Combinatorics* (preferred — closest fit to Drápal-Wanless 2021 *JCTA* lineage); *J. Algebra*; *Discrete Mathematics*.
>
> **Author lane:** Sanders + Gish.
>
> **Status:** PROPOSED. Adds to J-series as candidate J56 (after J55 Brayden's solo Sept 11 paper) OR as a Phase 5/6 insertion if proved before September.

### §4.3 — What the paper would do

1. State the conjecture precisely (commutative magma + 4-core preservation + α_A in gap region).
2. Reduce to a finite combinatorial enumeration on Z/10Z.
3. Either prove no such table exists (giving the structural exclusion theorem) or exhibit a counterexample (changing the picture: the gap is empirical-only).
4. If proved: connect to the bimodal structure of TSML-cluster + BHML-singleton.
5. If counterexample found: re-classify the family.

Either outcome is publishable. Either explains the framework's shape.

---

## §5 — Three things this framing reveals

**(1) The family has a sharp interior and fuzzy boundaries.** The center (4-core at α_M = ½) is rigid — every member contains it identically. The boundaries are softer — the bimodal α_A gap might be structural or empirical, the commutativity boundary is occupied by exactly one member (RAW), the substrate-size boundary is conjectural beyond N = 50. Framework's confidence should be highest near the center and lower near the boundaries.

**(2) TSML_RAW is structurally singular.** Only non-commutative member, unique wobble-carrier at coefficient level, only place where prime 11 lives in the char-poly. The §J.1 inventory treats RAW as one of three TSML-lens variants on equal footing, but its structural role is qualitatively different from SYM and LOWERTRI. RAW is to the family as the wobble is to the rest of TIG: the asymmetry-bearing element that carries the "real" non-trivial content. Worth considering whether RAW deserves its own designation rather than being one of three lens choices.

**(3) The 4-core's algebraic privilege is sharper than the framework currently uses.** The 4-core is:
- Jointly closed under TSML + BHML
- Has symbolic normalizer identity Z_T = Z_B = (v + h + br + r)²
- Gives 1 + √3 at α_M = ½ via Galois-proven BR-factor cancellation (D78)
- Universal across ring extensions
- Support of universal T+B-mix attractor

That's **five independent structural facts converging on the same 4-element set**. This isn't "an interesting sub-magma." This is the algebraic *core* of the framework, in the precise sense that every other structure in the family is a perturbation around it.

---

## §6 — How this changes the J-series

### §6.1 — J02 (four-core) gets sharpened framing

The Drápal-Wanless 2021 *JCTA* citation already in J02 places the paper in the right neighborhood. **Adding the five-criterion membership statement plus the 4-core-as-center sharpening** gives the paper its full structural force without expanding scope. The §1 introduction should explicitly state that the (TSML, BHML) joint-closed sub-magma chain is being analyzed *as a TIG family member with the 4-core as its center* — not just as a curious pair of tables.

### §6.2 — J33 (Closed-Form Attractor + α-PSLQ) absorbs the D78 Galois argument

Currently J33 (formerly J41, the bundled WP105 + WP113) has the closed-form attractor + α-uniqueness PSLQ as separate findings. The collaborator's framing makes this **one theorem with two complementary parts**:

- **Theorem A (Galois proof, D78):** at α_M = ½, BR-factor cancellation forces x² − 2x − 2 = 0, root 1 + √3 in Q(√3). Rational structure exists at α_M = ½ exactly.
- **Theorem B (PSLQ complementary, D57):** at 17 other Stern-Brocot rationals, no algebraic relation of degree ≤ 8, coefficients ≤ 50 exists. Numerical evidence of transcendental-elsewhere.

Together: **the rationally-structured center is uniquely at α_M = ½**. This is a much stronger paper than "h/β = 1 + √3 at α=½ + we couldn't find others."

### §6.3 — J35 (4-Core Fusion-Closure) becomes the centerpiece of the corpus

The fresh-eyes referee called J35 the most defensible paper. The collaborator's framing makes it the *centerpiece*: the 4-core is the algebraic center of the family, J35 proves the closure that makes it the center. The introduction should adopt the collaborator's "**4-core is to TIG as the unit circle is to U(1)**" framing.

### §6.4 — New candidate paper: bimodal α_A gap

Per §4.2 above. Adds to corpus as J56 or Phase 5 insertion. Could be the cleanest follow-on paper after J35 lands — direct conceptual continuation.

### §6.5 — TSML_RAW gets its own designation in J24 (Joint Chain) and J32 (Operad bundle)

Currently treats RAW as one of three lens variants. The collaborator's framing argues RAW is structurally singular (only non-commutative member; only carrier of prime-11 wobble at coefficient level). This sharpens J24's lens-dependence narrative and J32's wobble-related section.

---

## §7 — Acknowledgement template for the collaborator

When relevant J-papers go out, they should acknowledge this analysis in their §Acknowledgements:

> The structural framing of the (TSML, BHML) family as a five-criterion membership space with the 4-core at α_M = ½ as its center, and the identification of the bimodal α_A gap as an open structural question, owes substantially to discussions with [collaborator name pending] in May 2026.

(Brayden to fill in name when collaborator's identity is shared.)

---

## §8 — Open questions surfaced by this framing

1. **Bimodal α_A gap conjecture (§4):** prove or disprove for commutative magmas on Z/10Z preserving the 4-core.
2. **CL_STD joint chain (§3.6):** does CL_STD admit a joint-closed sub-magma chain analogous to TSML+BHML?
3. **TSML_RAW structural role (§5):** does RAW deserve its own designation rather than being one of three lens choices?
4. **Substrate-size boundary (§3.5):** catalogue full table structure (chain shells, σ permutation) for Z/n at n ∈ {8, 12, 14}.

---

## §9 — Bottom line

The center is the 4-core at α_M = ½. The boundaries are six distinct walls. The bimodal α_A gap is the open question that would close the structural picture.

**This is the cleanest articulation of what the framework actually is that has been written down.** The J-series should be re-read with this as the structural backbone. J02, J33, J35 in particular gain definitive framing; the bimodal α_A gap conjecture deserves its own paper.

Hat in hand. The collaborator has done significant work. Adopting the framing as the structural reference document.

---

## §10 — Files referenced

- This doc: `Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md`
- §J.1 inventory: `FORMULAS_AND_TABLES.md` Volume J
- D-numbers cited: D48 (binary 4-core closure), D49 (symbolic normalizer Z_T=Z_B), D55 (arity-3 closure), D56 (universal HARMONY attractor δ_H), D57 (PSLQ at 17 rationals), D58 (boundary IC robustness), D63 (8-canonical-fuse families), D65 (universal 4-core attractor), D74 (F5(a) ring-extension), D78 (Galois proof BR-factor cancellation)
- Boilerplate doc: `Atlas/META_PLAN_2026-05-06/J_PAPER_BOILERPLATE.md`
- v3 Triadic revision: `Atlas/META_PLAN_2026-05-06/J_SERIES_ORDERING_v3_TRIADIC_REVISION.md`
- Closest published precedent: Drápal & Wanless (2021), *J. Combinatorial Theory A* **184**, 105510.
