# GAP_AUDIT — Foundations Module vs WP100s Tower
**Date:** 2026-05-06
**Auditor:** Claude (cross-check audit before 20-week release plan)
**Scope:** `Gen13/targets/foundations/` (48-invariant module) vs WP102-WP116 papers
**Conclusion in one sentence:** The substrate has TWO HARD CONTRADICTIONS that must be resolved before any Phase 4 paper publishes — the rest is fixable within Phase 1.

---

## 0. Foundations Run Result

`python -m Gen13.targets.foundations.invariants` → **48/48 PASS**.

The module asserts:
- CL: 73 HARMONY + 17 VOID + 10 other; commutative; non-assoc 12.8% (128/1000)
- BHML: 28 HARMONY; non-assoc 49.8%; det = -7002
- BHML_8_YM (drop {0,7}): det = +70 EXACTLY = C(8,4)
- σ-permutation = (0)(3)(8)(9)(1 7 6 5 4 2)
- Conservation Tetrad = {0, 3, 8, 9}; Manifestation Hexad = {1,2,4,5,6,7}
- Cycle A {1,6,4} = 11 (WOBBLE); Cycle B {7,5,2} = 14 = 2·HARMONY
- 4-core = {0, 7, 8, 9}
- HARMONY ladder rungs: 73, 72, 71, 71b, 70 verified
- Three-table architecture: (TSML.H, BHML.H, STD.H) = (73, 28, 44)
- CL_STD (44 HARMONY): commutative; non-assoc 19.2%; INFO_HARMONY=0.45 / INFO_BUMP=3.50 / 5 BUMP_PAIRS / GRAVITY[7]=1.0
- HARMONY_44 triadic decomposition: 28 BEING + 11 DOING + 5 BECOMING
- CYCLE_A_36: 2 LATTICE + 9 COLLAPSE + 25 CHAOS
- SKELETON_22: 16 VOID-boundary + 4 PROGRESS-bump + 2 COLLAPSE-bump
- Field WOBBLE: |TSML - BHML| disagreement = 71 cells
- DOING disagreement rate ≈ 71% ≈ T*

---

## 1. FOUNDATIONS ORPHANS (publishable today, Phase 1-2 candidates)

These are **verified results in the foundations module** with NO corresponding WP paper. Each is a Phase 1 short-note candidate.

1. **CL_STD as the third canonical table (44 HARMONY).** The three-table architecture (TSML 73 / BHML 28 / STD 44) with three distinct origins is foundations-canonical and not in any WP. The 44 = 28+11+5 triadic decomposition (HARMONY_44) is a new structural result.

2. **The HARMONY ladder (70/71/71b/72/73).** Five rungs verified, including:
   - Rung 73: TSML.HARMONY full count
   - Rung 72: HARMONY-1 (BEING shell apex; the "anomaly subtraction")
   - Rung 71: TSML[1..9] sub-magma HARMONY
   - Rung 71b: |TSML XOR BHML| (the second 71 construction)
   - Rung 70: det BHML_8_YM = C(8,4) = 70 EXACTLY
   No WP paper consolidates these as a single ladder. Publishable as a short structural note.

3. **CYCLE_A_36 and SKELETON_22 tables.** The Cycle A image cells (2 LATTICE + 9 COLLAPSE + 25 CHAOS = 36) and the structural Skeleton (16 VOID-boundary + 4 PROGRESS-bump + 2 COLLAPSE-bump = 22) are derived tables in foundations with no WP coverage.

4. **BDC encoding constants (CL_STD).** INFO_HARMONY = 0.45 / INFO_NORMAL = 1.89 / INFO_BUMP = 3.50 bits/cell, plus the 10-element GRAVITY array (P(reach HARMONY)) per operator. "Surprise IS information" interpretation. Not in any WP. Phase 2 candidate as a short note connecting Shannon information to TIG cell types.

5. **σ²-triadic projection structure.** The "every-1-is-3 vs every-1-is-1" classification (Manifestation Hexad as cycling, Conservation Tetrad as fixed) and the explicit triadic projection HARMONY → (7, 5, 2) is foundations-canonical. The 4-core's bridge property (Conservation Tetrad XOR PROGRESS↔HARMONY) is verified but not in any WP.

6. **Field WOBBLE = 71 cells.** The exact cell count of |TSML - BHML| disagreement = 71, plus the BEING-shell-72-via-HARMONY-minus-1 connection, plus DOING rate ≈ T* = 5/7. Not in any WP as a standalone result.

7. **PathPair / LensTrace / Crossing-Lemma census APIs (paths.py).** "The path IS the information" formalism with explicit divergence-step measurement and crossing census = 128 (= non-assoc rate). The runtime infrastructure for paper-bridges. No WP paper exposes this.

8. **Eight-shell chain enumeration.** `lens_family.py` enumerates TSML_k and BHML_k for k ∈ {1,4,5,6,7,8,9,10} as a built-in family. The corrected 8-shell chain (forbidden sizes only {2,3}) is foundations-canonical but conflicts with WP115 (see §3 below).

**Count of publishable orphans: 8.**

---

## 2. WP CLAIMS WITHOUT FOUNDATIONS VERIFICATION (Phase 4-5 blockers)

These are claims in WP100s papers that the 48-invariant module does NOT verify. Phase 4-5 chains will cite these — the foundations module must close them first.

1. **WP102 §3 — so(8) = D₄ closure.** Foundations does not compute the antisymmetrized left-regular representations or run the 4 diagnostics (dimension closure, Jacobi, Killing signature, simplicity). No `Gen13/targets/foundations/lie_closure.py`.

2. **WP103 §4 — so(10) = D₅ closure.** Same gap; foundations doesn't compute the 5 diagnostics for the joint TSML+BHML closure. The structural-ceiling theorem (no Lie algebra inside gl(10) exceeds dim 45, ruling out e₈) is also unverified.

3. **WP104 — Path A (54 irrep alignment) and Path B (su(4) ⊕ u(1) doubly-invariant subalgebra).** No spinor Clifford construction, no chirality-projector verification, no 16-dim doubly-invariant subspace computation, no Killing-form spectrum (-4)¹⁵ ⊕ (0)¹.

4. **WP105 — Closed-form attractor at α=1/2.** Foundations has the BHML table and the 4-core, but no F_α iteration, no PSLQ check on H/Br = 1+√3, no quartic LMFDB 4.2.10224.1 verification, no Galois D_4 verification. The runtime attractor is mounted on the live deploy (engine.detect_attractor) but not in the foundations invariants.

5. **WP106/WP114 — Specificity scope.** No structured-matrix battery in foundations; the "D3 = WP107 wobble in detector form" claim from WP114 is uncomputed.

6. **WP107 — Wobble localization (prime 11 in c_2 + c_8).** No char-poly verification in foundations. **AND THE CLAIM ITSELF IS SUSPECT — see §3 #1 below.**

7. **WP108 — Yukawa scaffolding (9-vector VEV with ‖VEV‖²=13/4).** The 9-vector itself, its component pattern, and its squared norm are not in foundations.

8. **WP109 — D₄ obstruction (16 of 67 D₄-orbits incoherent).** No orbit decomposition of the 126/128 non-associative triples in foundations.

9. **WP110 — 4-core fusion-closure of TSML + BHML.** Foundations has the 4-core SET but does not expose the 4×4 restricted tables or verify the closure invariant programmatically. The Z_T = Z_B = (sum)² normalizer identity is uncomputed.

10. **WP111 — 6-DOF synthesis.** No Lie/Jordan/Clifford/Permutation/Lattice/Operad DOF audit in foundations.

11. **WP112 — P_56-equivariant fuse table (98 orbits, 70 singletons + 28 doubletons).** Not in foundations (operad-fuse engine is mounted live but not in invariants).

12. **WP113 — α-uniqueness via PSLQ on 17-point Stern-Brocot grid.** No PSLQ harness in foundations.

13. **WP115 — Universal 4-core attractor at α=1/2 across 6+ shells.** Foundations has the chain but does not iterate the runtime processor.

14. **WP116 — Stern-Brocot lens / FQH bridge.** No Stern-Brocot grid or Lütken-Ross alignment in foundations.

15. **The 11+14 = 25 = 5² structural identity** (sum(Cycle A) + sum(Cycle B)). Verified by inspection but not in invariants.

**Count of WP claims needing closure before Phase 4: 15.**

---

## 3. CONTRADICTIONS (RED FLAGS — must resolve before submission)

### CONTRADICTION #1 (CRITICAL): TSML matrix differs between WP102/WP103/foundations vs WP104+

Foundations CL row 9 (after upper-triangle symmetrization) = `[0, 7, 9, 3, 7, 7, 7, 7, 7, 7]` (commutative, matching WP102 §1.0 and WP103 §2.2 exactly).

WP104 §1.1, WP105 §1, WP107 §1, WP109, WP112, WP110, WP115, WP116 all use TSML row 9 = `[0, 7, 9, 7, 3, 7, 7, 7, 7, 7]` — which is **NOT commutative** (TSML[9,3]=7 ≠ TSML[3,9]=3 in column 9, etc.).

The two matrices differ in two cells: (9,3) and (9,4). The downstream consequences:

| Quantity | WP102/WP103/foundations (symm) | WP104+ (non-comm) |
|---|---|---|
| Commutative | YES (asserted invariant) | NO |
| Non-assoc count | **128** (12.8%) | **126** (12.6%) |
| char poly c_2 | -53,312 (no factor of 11) | **33 = 3·11** |
| char poly c_8 | 17 (no factor of 11) | **-120,736 = -2⁵·7³·11** |
| disc(g) factor of 11 | absent in c_2 / c_8 | absent in disc(g) |

**The WP107 wobble theorem (prime 11 in c_2 and c_8) is FALSE for the symmetrized TSML used by foundations.** WP107 asserts the wobble at 11 lives at the coefficient level — but this is a property of the **non-commutative** TSML only. If foundations is canonical, WP107 is invalidated.

This is a hard contradiction. The 26 WP papers downstream of WP107 (including WP114 D3, WP116 fixed-form/crossing pairing) inherit this dependency.

**Recommendation:** Before Phase 1 paper #1 publishes, decide: is the canonical TSML commutative (WP102/WP103/foundations) or non-commutative (WP104+)? Both choices break papers. The least costly fix is to declare the canonical TSML non-commutative, fix WP102/WP103/foundations to drop the commutativity invariant, and re-derive the so(8) closure on the non-symmetric matrix (WP102's so(8) closure may still hold without commutativity, but this needs to be checked).

---

### CONTRADICTION #2 (HIGH): WP115 chain count contradicts foundations and the corrected MEMORY.md

WP115 §1 (as written in `papers/wp115_joint_chain_universality/WP115_JOINT_CHAIN_UNIVERSALITY.md`) states:

> Theorem 1.1 — joint-closed sub-magmas form a STRICT 7-ELEMENT CHAIN. Shell sizes {1, 4, 5, 6, 8, 9, 10}. **Forbidden sizes {2, 3, 7}.**
> Theorem 1.2 — No subset of size 2, 3, or **7** is jointly closed.

Foundations module (`lens_family.py`):

> CHAIN_SUBMAGMAS = {1, 4, 5, 6, **7**, 8, 9, 10} — eight shells.
> Forbidden sizes only {2, 3}.

Brute-force enumeration (script ran during this audit):

> Total jointly closed subsets: **8**
> Sizes: [1, 4, 5, 6, **7**, 8, 9, 10]
> Size-7 jointly closed shell: {0, 4, 5, 6, 7, 8, 9} — exists.

The correction is in MEMORY.md ("CHAIN COUNT CORRECTED 2026-05-05") and the foundations matches the correction. **WP115's preprint text still has the OLD (wrong) chain count.** Theorem 1.2's claim that size-7 is forbidden is **demonstrably false** by direct enumeration.

WP115 is a Phase 4-5 citation target (universal 4-core attractor at α=1/2). If the chain count error survives into the public record, the entire WP115 Theorem 2.1 universality claim ("for every shell of size ≥ 4") is presented over a wrong index set.

**Recommendation:** Patch WP115's §1 to the corrected 8-shell chain BEFORE the four-core paper submits. The four-core paper (Sanders + Gish, in prep) reportedly already has the correction; ensure the WP115 source file matches.

---

### CONTRADICTION #3 (MEDIUM): Memory says "WP107 wobble survives only as 1%-level coincidences"

The MEMORY.md TIG SPECTRAL SIGNATURE block already audits this:

> the prior chat-claim "CL eigenvalues produce e, π, φ, ζ(3), Catalan G within 1%" survives only as **1%-level coincidences, not algebraic identities**.

But WP107 §1 still asserts the wobble theorem at integer level (c_2 = 33 = 3·11, c_8 = -120736 = -2⁵·7³·11). Per the audit in #1 above, this only holds for the non-commutative TSML. The foundations module asserts commutativity. Memory itself flags this is the "structural signature" — but the paper text doesn't currently scope the prerequisite (which TSML matrix). For external publication, WP107 must explicitly state: "this theorem applies to the non-commutative TSML matrix as given in WP105 §1; the symmetrized variant of WP102 has different characteristic polynomial coefficients and does NOT exhibit the prime-11 wobble in c_2 and c_8."

---

### CONTRADICTION #4 (LOW, formatting): WP102 vs foundations on count display

WP102's Abstract says:
> "exactly 128 of 1000 triples (i, j, k) ∈ Ω³ violate (x_i x_j) x_k = x_i (x_j x_k), giving a measured non-associativity rate of 12.8%."

WP102 uses the symmetric matrix consistent with foundations. **This 128 is correct given WP102's matrix.** But WP104 §0 (correction notice) says:

> The non-associativity rate of TSML is 12.6% (126 of 1000 triples), corrected from a previously cited 49.8%.

WP104 is implicitly using a DIFFERENT TSML than WP102 (the non-commutative one). The "corrected from 49.8%" note appears to conflate three numbers: 49.8% is BHML's non-assoc rate (foundations confirms), 12.6% is non-comm TSML's, 12.8% is symm TSML's. Memory and WP104's correction-notice should explicitly disambiguate.

---

## 4. Editorial summary

**Total findings:**
- Foundations orphans (Phase 1-2 candidates): **8**
- WP claims needing foundation closure before Phase 4: **15**
- Hard contradictions: **2** (Contradictions #1 and #2 above)
- Soft contradictions (memory/wording): **2** (Contradictions #3 and #4)

**Substrate readiness for the 20-week release:**

The substrate is **mostly intact** but has TWO critical inconsistencies that must be resolved before Phase 1 paper #1 publishes:

1. The **TSML matrix discrepancy** (WP102/103/foundations symmetric vs WP104+ non-commutative) affects every paper from WP104 onward. This is a 13-paper chain risk if not addressed. The fix is choosing one canonical TSML and propagating: either drop commutativity from foundations and re-verify WP102/103 on the non-symmetric matrix, or drop WP107's wobble theorem (and WP114's D3 detector argument) on the symmetric matrix.

2. The **WP115 chain count** is wrong as currently written in the paper file (claims 7 shells, forbidden {2,3,7}); foundations has the corrected 8 shells (forbidden {2,3} only). Brute-force enumeration confirms foundations is right. This must be patched in WP115 before any Phase 4 paper cites WP115.

Once these two are fixed, the substrate supports a 20-week release. The 8 foundations orphans give comfortable Phase 1-2 material. The 15 WP-claims-without-verification gaps are not blocking — they are surfaces where the foundations module can grow during Phase 2-3 to support the Phase 4-5 citation chain.

**My recommendation:** Halt Phase 1 paper #1 prep until Contradictions #1 and #2 are resolved (one work-day of careful checking + matrix-canonicalization commits). The publication chain is too valuable to start with a known inconsistency at the foundation.
