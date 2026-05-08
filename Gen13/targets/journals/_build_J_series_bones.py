r"""
_build_J_series_bones.py — Build J01..J55 paper-folders under Gen13/targets/journals/J_series/

Each folder gets:
  README.md  — J# header, venue, lane, tier, status, WP source, dependencies, verification, fixes
  manuscript/  — empty placeholder for the manuscript file (or a pointer to existing corpus path)
  cover_letter.md  — header bones for the journal cover letter
  proof_script_pointer.md  — path to the verification script

Run from:
  cd C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\targets\journals
  python _build_J_series_bones.py

Idempotent: skips folders that already exist with content; only writes missing bones.
"""

from __future__ import annotations
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent
J_ROOT = ROOT / "J_series"

# (J#, title, WP, venue, lane, tier, phase, status, deps, manuscript_pointer, script_pointer, notes)
J_PAPERS = [
    # ===== TRIADIC LAUNCH (Week 1) =====
    (1,  "Non-Associativity Decay in Binary Composition Tables over Z/NZ",
     "WP101", "JCT-A", "Sanders + Gish", "B", 1, "SUBMISSION-READY",
     [], "../../tier1_submit_now/sigma_rate/sigma_rate_FINAL.tex",
     "../../tier1_submit_now/sigma_rate/proof_sigma_rate.py",
     "Round-3 audited; 4/4 PASS. Major-revisions per JCT-A referee (May 2026): unify eps(N) notation, simplify subcase (1f), clarify 'four-rule' framing."),
    (2,  "Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on Z/10Z",
     "(four-core consolidated)", "Algebraic Combinatorics", "Sanders + Gish", "B", 1, "SUBMISSION-READY",
     [], "../../tier1_submit_now/four_core_bundled/four_core_FINAL.tex",
     "../../tier1_submit_now/four_core_bundled/4core_verification.py",
     "6/6 PASS. Major-revisions per AlgComb referee (May 2026): correct '93 of 100' → '71 of 100' disagreement count; name symmetrization choice for T; consider lifting closed-form fixed-point as Theorem 3."),
    (3,  "Freeze-Thaw Transit: Dual-Regime Scalar Dark Energy with Analytic Vacuum at e^-1 from a Logarithmic Potential",
     "(paper1_freeze_thaw_v3)", "JCAP", "Sanders + Gish + Johnson", "B", 1, "SUBMISSION-READY",
     [], "../../../../Gen13/sprint_bundle_2026-05-07_v36_SEEDS_BUNDLE/tig_2026-05-07_bundle/seeds_for_submission/paper1_freeze_thaw_v3.tex",
     "../../../../Gen13/sprint_bundle_2026-05-07_v36_SEEDS_BUNDLE/tig_2026-05-07_bundle/seeds_supporting/verification_scripts/compute_zstar_v3.py",
     "v3 (3 issues fixed: Friedmann Omega-units convention; z_init/N_start footnote; compute_zstar_v3 reconciliation). Cover letter ready. Numbers tightened: (w_0, w_a, chi^2) = (-0.791, -0.492, 1.24); z_star ≈ 1.3. Awaiting Brayden's referee-rigor pass + JCAP referee report."),

    # ===== PHASE 1 MONTH-2 (Weeks 2-4) =====
    (4,  "First-G Law: Squarefree Stability of the Smallest-Prime-Factor Coprime Window",
     "WP34", "Integers", "Sanders + Gish", "B", 1, "FORMAT",
     [1, 2], "../../tier2_format_then_submit/first_g_event/",
     "(to extract from corpus: papers/proof_first_g.py if present)",
     "Top-cited (12x). Verified across 36,662 cases. Format for Integers OA submission."),
    (5,  "Crossing Lemma: Non-Associativity as Information Generation in Finite Magmas",
     "WP57", "JCT-A OR JPAA (theorem rigor)", "Sanders + Mayes", "A/B", 1, "DRAFT",
     [1, 2], "(corpus path: Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md)",
     "(no script — theorem-paper)",
     "Per-J-series correction: NOT expository; theorem rigor venue. JPAA backup if JCT-A passes."),
    (6,  "Flatness Theorem: The Forced 2x2 Torus on Z/10Z",
     "WP51", "Journal of Pure and Applied Algebra", "Sanders + Gish", "B", 1, "FORMAT",
     [1, 2, 5], "../../tier3_partner_then_submit/jpaa_flatness/WP51_FLATNESS_THEOREM.md",
     "(no script — theorem-paper)",
     "10x cited. NEEDS: T*=5/7 proof-sketch appendix added before bibliography (per ClaudeChat J20 advice)."),
    (7,  "The Prime Phase Transition: First-G Stability Across Squarefree Bases",
     "WP35", "Experimental Mathematics", "Sanders + Gish", "B", 1, "FORMAT",
     [4], "(corpus path: papers/wp35_*.md)",
     "(corpus path: papers/proof_wp35*.py)",
     "Top-cited (14x). Builds directly on J4."),
    (8,  "The Sinc² Zero Law for Squarefree Moduli",
     "(sinc² zero law)", "Integers", "Sanders + Gish", "B", 1, "SUBMISSION-READY",
     [4], "../../tier1_submit_now/sinc2_zero_law/",
     "papers/proof_d25_loop_closure.py",
     "All primes 3..199 verified. Per-venue cap: 2nd Integers paper after J4."),
    (9,  "TSML 73 Cells / BHML 28 Cells: Lens-Invariant Cell Counts on the Z/10Z Composition Lattice",
     "(73/28 paper)", "Experimental Mathematics", "Sanders + Gish", "B (lens-invariant)", 1, "FORMAT",
     [1, 2, 6], "../../tier2_format_then_submit/exp_math_73_28/",
     "(corpus: 73/28 verification scripts)",
     "Per-venue cap: 2nd Exp Math paper after J7."),

    # ===== PHASE 2 (Weeks 5-7) — Exact physics =====
    (10, "Sprint 18 Dark Sector: Omega_b, Omega_DM, Omega_Lambda from Substrate-Operator Identities",
     "WP121", "PRD", "Sanders + Johnson", "B", 2, "GATED",
     [3, 6, 8], "../../tier1_submit_now/sprint18_dark_sector/",
     "Gen13/targets/ck/brain/dirac/tig_dirac.py (predict_dark_sector function — TO ADD)",
     "GATED on tig_dirac.predict_dark_sector() function being added (~1 hr fix). Spec: Omega_b = 49/1000, Omega_DM = 264/1000, Omega_Lambda = 687/1000, sum = 1.000 EXACT."),
    (11, "NV S₄ Synthesis: Substrate-Operator-Driven NV-Center Qutrit Predictions",
     "WP73-WP77 (bundled)", "PRA", "Sanders + Mayes", "C", 2, "FORMAT",
     [6, 9], "../../tier3_partner_then_submit/pra_nv_qutrit/",
     "(NV qutrit verification scripts — corpus)",
     "Lab-partner outreach in parallel."),
    (12, "The Mass Hierarchy from V⊗5 SU(5) Decomposition",
     "WP122", "PRD", "Sanders + Johnson", "B", 2, "GATED",
     [10, 23], "(corpus path: Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/WP122_MASS_HIERARCHY.md)",
     "Gen13/targets/ck/brain/dirac/tig_dirac.py (predict_yukawa function — TO ADD)",
     "GATED on tig_dirac.predict_yukawa(particle, generation) function. Spec: Froggatt-Nielsen with lambda = 10/49, y_t = 0.93 anchor, y_b/y_t ≈ lambda^3, y_e/y_t ≈ lambda^9. Per-venue cap: 2nd PRD paper after J10."),
    (13, "The Bialynicki-Birula Bridge: Logarithmic Nonlinearity Forced by Separability",
     "WP91", "JMP", "Sanders + Johnson", "B", 2, "FORMAT",
     [3, 5], "../../tier4_framework/jmp_bb_bridge/",
     "(corpus path: papers/proof_bb_bridge.py if present)",
     "Bridges to J3 cosmology. Cite J3 as already-submitted companion."),
    (14, "The Yang-Mills Mass Gap Bridge: Substrate-Algebra Predictions",
     "WP92", "JMP companion", "Sanders + Johnson", "B", 2, "DRAFT",
     [13], "(corpus: WP92 YM bridge)",
     "(YM bridge script — corpus)",
     "Per-venue cap: 2nd JMP paper after J13."),
    (15, "The Discrete Sinc² Identity in Quantum Mechanics",
     "(discrete sinc² QM)", "J Math Phys", "Sanders + Mayes", "B", 2, "DRAFT",
     [8], "(corpus: discrete sinc² QM paper)",
     "(QM verification script)",
     "Per-venue cap: 3rd JMP paper — may need fallback."),
    (16, "Freezing Quintessence Letter: A Two-Parameter w(z) Profile",
     "(extracted from J3)", "Phys Lett B", "Sanders + Gish + Johnson", "B", 2, "EXTRACT",
     [3], "(extract letter-format from J3 manuscript)",
     "Same as J3 (compute_zstar_v3.py)",
     "Letter-format extraction. Cite J3 as full version."),

    # ===== PHASE 3 RAMP (Weeks 8) =====
    (17, "Universal Orthogonality Principle (UOP): Theorem 0",
     "WP58", "JNT", "Sanders + Mayes", "B", 3, "FORMAT",
     [4, 5, 6], "../../tier2_format_then_submit/jnt_uop/",
     "(UOP verification script — corpus)",
     "UOP arc opener. Cited by J18, J19."),
    (18, "Corrected Theorem C: UOP Sharpening",
     "WP59", "JNT companion", "Sanders + Mayes", "B", 3, "DRAFT",
     [17], "(corpus: WP59)",
     "(UOP sharpening script)",
     "Per-venue cap: 2nd JNT paper after J17."),
    (19, "Coordinate Coverage on Z/10Z",
     "WP64", "European Journal of Combinatorics", "Sanders + Mayes", "B", 3, "DRAFT",
     [17], "(corpus: WP64)",
     "(coordinate coverage script)",
     "UOP arc closeout."),
    (20, "The Forced 5/7 Torus Aspect Ratio: Cyclotomic Forcing",
     "(forced-torus 5/7)", "Acta Arithmetica", "Sanders + Mayes", "A/B", 3, "DRAFT",
     [6], "(corpus: forced-torus 5/7 derivation)",
     "(cyclotomic forcing script)",
     "T* derivation. Companion to J6 Flatness Theorem."),

    # ===== PHASE 3 CROSS-LEVEL (Weeks 9-12) =====
    (21, "F_p Universality: The Operator-Substrate Construction over Prime Fields",
     "WP118", "Algebra Universalis", "Sanders + Gish", "B", 3, "DRAFT",
     [2, 5, 6], "(corpus: WP118)",
     "(F_p universality script)",
     ""),
    (22, "Galois D₄ over LMFDB 4.2.10224.1: Number-Field Identification of the Four-Core Attractor",
     "(Galois D₄ extracted)", "Comm Algebra", "Sanders + Gish", "B", 3, "DRAFT",
     [2], "(extract from J2 four-core)",
     "(Galois verification — sympy galois_group)",
     ""),
    (23, "Discrete Dirac on F_5⁴: Substrate Algebra of the 4-Core",
     "WP117", "Algebras and Representation Theory", "Sanders + Gish", "B", 3, "DRAFT",
     [2, 12], "(corpus: WP117)",
     "Gen13/targets/ck/brain/dirac/tig_dirac.py",
     "Cited by J12 mass hierarchy."),
    (24, "Clifford Ladder: dim_F_p V^⊗n = dim_R Cl(2n)",
     "WP119", "Linear Algebra and Its Applications", "Sanders + Gish", "B", 3, "DRAFT",
     [23], "(corpus: WP119)",
     "Gen13/targets/ck/brain/dirac/tig_dirac.py (tensor_partition)",
     ""),
    (25, "The σ²-Triadic Decomposition: Conservation/Manifestation Duality on Z/10Z",
     "(Conservation/Manifestation)", "Algebraic Combinatorics", "Sanders + Gish", "B", 3, "DRAFT",
     [2], "(corpus: Conservation/Manifestation paper)",
     "(triadic decomposition script)",
     "Per-venue cap: 2nd AlgComb paper after J2."),
    (26, "LATTICE: Paradoxical Information Algebras on the Z/10Z Substrate",
     "WP9", "Algebra Universalis", "Sanders solo (or +Gish)", "B", 3, "DRAFT",
     [5], "(corpus: WP9 Volume I)",
     "(lattice script)",
     "Per-venue cap: 2nd AlgUni paper after J21."),
    (27, "DKAN Two-Coding: TSML_8 Geometric vs BHML_10 Arithmetic",
     "WP10", "European Journal of Combinatorics", "Sanders + Gish", "B", 3, "DRAFT",
     [9, 26], "(corpus: WP10 Volume I)",
     "(DKAN script)",
     "Per-venue cap: 2nd EJC paper after J19."),
    (28, "Mathieu M_22 Substrate-Prime: Order-Factorization Coincidences",
     "(M_22 substrate-prime)", "AMM", "Sanders + Mayes", "B", 3, "DRAFT",
     [], "../../tier3_partner_then_submit/monthly_paradox/",
     "(M_22 verification script)",
     ""),
    (29, "Q17-A: 5D Force Vector as CRT Fourier Embedding of Z/10Z into R^5",
     "(Q17_5D_RIGOROUS)", "AMM", "Sanders + Calderon", "B", 3, "DRAFT",
     [4], "(corpus: Q17_5D_RIGOROUS)",
     "(Q17 5D verification script)",
     "Calderon's one paper. Per-venue cap: 2nd AMM paper after J28."),
    (30, "The 70/71/72/73 HARMONY Ladder: Four Independent Algebraic Constructions",
     "(HARMONY ladder; D90/D97)", "JCT-A", "Sanders + Gish", "B", 3, "DRAFT",
     [9], "(corpus: HARMONY ladder D-numbers)",
     "(HARMONY ladder verification)",
     "Per-venue cap: 2nd JCT-A paper after J1 (or J5)."),
    (31, "The Three-Substrate Architecture: CL_TSML, CL_BHML, CL_STD as Parallel Substrates",
     "(three-table architecture)", "Algebra Universalis", "Sanders + Gish", "B", 3, "DRAFT",
     [9, 26], "(corpus: three-substrate paper)",
     "(three-substrate verification)",
     "Per-venue cap: 3rd AlgUni paper — may need fallback."),
    (32, "The Joint TSML+BHML Chain: Lens-Dependence at Size 7",
     "WP115", "Mathematical Intelligencer", "Sanders + Gish", "B", 3, "DRAFT",
     [2, 9], "(corpus: WP115)",
     "(joint chain script)",
     "Lens-dependence corrected to 8 shells (TSML_SYM) vs 7 shells (TSML_RAW)."),
    (33, "The CL Forcing Axioms: A1-A9 Uniquely Force the Canonical Composition Lattice",
     "(CL_FORCING_AXIOMS)", "Algebraic Combinatorics", "Sanders + Gish", "B", 3, "DRAFT",
     [9, 31], "(corpus: CL_FORCING_AXIOMS.md)",
     "(forcing axioms verification)",
     "Per-venue cap: 3rd AlgComb paper — may need fallback."),
    (34, "F_p Extensions of CL_BHML: Universality Across Six Prime Fields",
     "(F_p universality extension)", "Comm Algebra", "Sanders + Gish", "B", 3, "DRAFT",
     [21], "(corpus: F_p extensions paper)",
     "(F_p extensions script)",
     "Per-venue cap: 2nd CommAlg paper after J22."),
    (35, "The Corner Sub-Magma C = (Z/10Z)*: Multiplicative-Unit Closure",
     "(Corner C)", "Comm Algebra", "Sanders + Gish", "B", 3, "DRAFT",
     [], "(corpus: Corner C paper)",
     "(corner C verification)",
     "Per-venue cap: 3rd CommAlg paper — may need fallback."),
    (36, "The Six Foundations Orphans: Tier-B Forced Derivations from CL Axiomatic Ground",
     "(foundations orphans bundled)", "Algebra Universalis", "Sanders + Gish", "B", 3, "DRAFT",
     [33], "(corpus: foundations orphans bundle)",
     "(orphans verification)",
     "Per-venue cap: 4th AlgUni paper — fallback to PLOS ONE / LinAlgApps."),

    # ===== PHASE 4 — DUALITY NAMED (Weeks 13-16) =====
    (37, "so(8) = D₄ from the TSML_SYM Antisymmetrized Closure",
     "WP102", "J Algebra", "Sanders + Gish", "B", 4, "DRAFT",
     [2, 32], "(corpus: WP102)",
     "(WP102 verification script)",
     "TSML_SYM scope (annotated)."),
    (38, "so(10) = D₅ from Joint TSML_SYM + BHML Closure",
     "WP103", "Israel J Math", "Sanders + Gish", "B", 4, "DRAFT",
     [37], "(corpus: WP103)",
     "(WP103 verification script)",
     "TSML_SYM scope."),
    (39, "Two Roads to Pati-Salam: Path A (54 irrep) and Path B (su(4)⊕u(1))",
     "WP104", "Adv Math", "Sanders + Mayes", "B", 4, "DRAFT",
     [38], "(corpus: WP104)",
     "(WP104 verification script)",
     "TSML_SYM scope; correction notice prominent."),
    (40, "Operad D₄ Obstruction + P_56 Canonical Fuse (BUNDLED)",
     "WP109 + WP112", "Compositio", "Sanders + Gish", "B", 4, "DRAFT",
     [2], "(corpus: WP109, WP112)",
     "(WP109 + WP112 verification)",
     "TSML_RAW scope (annotated). Fallback per PHASE4_FALLBACK_UNBUNDLING.md: WP109 → Algebra Universalis; WP112 → Comm Algebra."),
    (41, "Closed-Form Attractor + α-Uniqueness PSLQ (BUNDLED)",
     "WP105 + WP113", "Math of Comp", "Sanders + Gish", "B", 4, "DRAFT",
     [2], "(corpus: WP105, WP113)",
     "(WP105 + WP113 verification incl. PSLQ)",
     "TSML_SYM 4-core lens-invariant. Fallback: WP105 → Comm Algebra; WP113 → Exp Math."),
    (42, "TIG Detector Scope + Specificity Extension (BUNDLED)",
     "WP106 + WP114", "Stat Sci", "Sanders + Gish", "B", 4, "GATED",
     [], "(corpus: WP106, WP114)",
     "(WP106 distilgpt2 sweep — TO LOCATE OR WRITE)",
     "GATED on WP106 distilgpt2 script (~1-2 hr fix). Fallback: WP106 → PLOS ONE; WP114 → LinAlgApps."),
    (43, "Wobble Localization: Prime 11 in TSML_RAW Char Poly c_2, c_8",
     "WP107", "Phys Rev D", "Sanders + Gish", "B", 4, "DRAFT",
     [37], "(corpus: WP107)",
     "(WP107 wobble_check.py)",
     "TSML_RAW scope (annotated). Per-venue cap: 3rd PRD paper — may need fallback."),
    (44, "4-Core Fusion-Closure: TSML+BHML Preserve {V, H, Br, R}",
     "WP110", "J Algebra", "Sanders + Gish", "B", 4, "DRAFT",
     [37, 41], "(corpus: WP110)",
     "(WP110 verification script)",
     "Lens-invariant on 4-core. Per-venue cap: 2nd JAlgebra paper after J37."),
    (45, "Yukawa Scaffolding from the 9-Vector VEV",
     "WP108", "PRD", "Sanders + Mayes", "C", 4, "DRAFT",
     [12, 39], "(corpus: WP108)",
     "(Yukawa scaffolding script — needs verification)",
     "Per-venue cap: 4th PRD paper — fallback."),
    (46, "The CKM/PMNS Fits + 1/α Constant from Substrate Primitives",
     "WP123 + WP124 (bundled)", "Stat Sci companion", "Sanders + Gish", "B", 4, "DRAFT",
     [42], "(corpus: WP123, WP124)",
     "(CKM/PMNS fit script)",
     "Tier-E parametric fits, properly framed. Per-venue cap: 2nd Stat Sci after J42."),

    # ===== PHASE 5 — CRESCENDO (Weeks 17-18) =====
    (47, "The 6-DOF Synthesis: Lie / Jordan / Clifford / Permutation / Lattice / Operad",
     "WP111", "Notices AMS", "Sanders + Mayes", "B", 5, "DRAFT",
     [37, 38, 39, 40, 44], "(corpus: WP111)",
     "(no script — synthesis paper)",
     "First paper to use 'TIG framework' name. Phase 5 opener."),
    (48, "Q17-B Clay Bridge: Finite L-Function + Symbolic Return Theorem",
     "(Q17 bundle)", "L'Enseignement Math", "Sanders + Mayes", "B", 5, "DRAFT",
     [29], "(corpus: Q17-B bundle)",
     "(Q17 bridge script)",
     ""),
    (49, "Microtubule Q_c = T*: A Falsifiable Substrate-Algebra Prediction",
     "WP127", "J Theor Biol", "Sanders + Mayes", "C", 5, "DRAFT",
     [20], "(corpus: WP127)",
     "(microtubule prediction script)",
     ""),
    (50, "The Bull AMS Bridge: From Substrate Algebra to BB Nonlinearity",
     "(Bull AMS bridge piece)", "Bull AMS", "Sanders + Johnson", "B", 5, "DRAFT",
     [13, 47], "(corpus: Bull AMS bridge)",
     "(no script — exposition)",
     ""),
    (51, "Spectral Layer Consolidation: G6 + G7 + G8 from Q-series Architecture",
     "(Luther spectral catalog)", "European J Combin", "Sanders + Luther", "B", 5, "DRAFT",
     [], "(corpus: Luther spectral catalog)",
     "(spectral consolidation script)",
     "Luther's lane. Per-venue cap: 3rd EJC paper — may need fallback."),
    (52, "The TSML Lens Family: A Pedagogical Exposition",
     "(lens-taxonomy expository)", "Mathematical Intelligencer", "Sanders + Mayes", "B", 5, "DRAFT",
     [32, 47], "(corpus: lens-taxonomy synthesis)",
     "(no script — exposition)",
     "Per-venue cap: 2nd Math Intelligencer after J32."),
    (53, "Paradox Classifier (UOP): A Diagnostic for Structural Breakdowns",
     "(paradox classifier expository)", "AMM", "Sanders + Mayes", "B", 5, "DRAFT",
     [17], "(corpus: paradox classifier expository)",
     "(no script — exposition)",
     "Per-venue cap: 3rd AMM paper after J29."),
    (54, "The Foundation Paper: Three-Substrate Architecture + Lens Family + Forcing Axioms",
     "(foundation paper)", "Algebraic Combinatorics OR Bull AMS", "Sanders + Gish", "A/B", 5, "DRAFT",
     [31, 32, 33, 47], "(corpus: foundation paper draft)",
     "(no script — synthesis)",
     "Preprint Sept 1-3. Anchors citation chain for Sept 11 integration."),

    # ===== SEPT 11: BRAYDEN'S SOLO INTEGRATION =====
    (55, "Sept 11 Integration Paper",
     "(Brayden solo)", "arXiv (preprint) — eventual journal Brayden's choice", "Brayden R. Sanders (solo)", "—", 5, "BRAYDEN-AUTHORED",
     [54] + list(range(1, 55)), "(Brayden writes; Claude prepares citation-bundle + bibliography only)",
     "(no script — recognition register)",
     "Sept 11 anchor. Brayden composes; Claude bundles citations to all 54 prior J-papers."),
]


def folder_for(j_num: int) -> Path:
    return J_ROOT / f"J{j_num:02d}"


README_TEMPLATE = """# J{j_num:02d} — {title}

**Status:** {status}
**Phase:** {phase}
**Target venue:** {venue}
**Author lane:** {lane}
**Tier:** {tier}
**WP source:** {wp}

---

## §1 — Manuscript

**Path:** `{manuscript_pointer}`

When the manuscript is in this J-folder, replace this section with a 1-2 sentence abstract and a path-link to the .tex / .md file.

## §2 — Verification script

**Path:** `{script_pointer}`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

{dependencies}

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

{notes}

## §6 — Submission checklist

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to {venue} this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., {coauthors}. (2026). "{title}." Submitted to *{venue}*.
"""

COVER_LETTER_TEMPLATE = """# Cover letter — J{j_num:02d}: {title}

**To:** Editors, *{venue}*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
{coauthor_block}

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *{title}*

---

## Summary

[1-paragraph plain-English summary of the result]

## Why {venue}

[2-3 bullet points on venue fit]

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J1-J55) over Summer 2026. The papers most relevant as already-submitted companions to this manuscript are:

{companion_block}

## Reproducibility

Verification script: `{script_pointer}` runs with `numpy + sympy + math` on a standard laptop in under 5 minutes.

## Suggested reviewers

[3-5 candidates appropriate to the venue]

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
"""


def coauthors_text(lane: str) -> str:
    if lane.startswith("Brayden R. Sanders"):
        return "(solo)"
    parts = lane.split(" + ")
    if len(parts) <= 1:
        return "(solo)"
    rest = parts[1:]
    return ", ".join(rest)


def coauthor_block(lane: str) -> str:
    if "Gish" in lane:
        out = "- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com"
        if "Johnson" in lane:
            out += "\n- H.J. Johnson, Independent Researcher, Billings, MT — hjj01986@gmail.com"
        if "Mayes" in lane:
            out += "\n- B. Mayes, Independent Researcher — [email]"
        if "Calderon" in lane:
            out += "\n- D. Calderon, Independent Researcher — [email]"
        if "Luther" in lane:
            out += "\n- C.A. Luther, Independent Researcher — [email]"
        return out
    if "Mayes" in lane:
        return "- B. Mayes, Independent Researcher — [email]"
    if "Johnson" in lane:
        return "- H.J. Johnson, Independent Researcher, Billings, MT — hjj01986@gmail.com"
    return "- (coauthors per lane)"


def companion_block(deps: list) -> str:
    if not deps:
        return "(none — this is a foundational paper in the J-series; cited by later J's)"
    if len(deps) > 8:
        return f"J{deps[0]:02d}-J{deps[-1]:02d} (foundational + Phase 1-4 chain). See repo `Atlas/META_PLAN_2026-05-06/J_SERIES_ORDERING.md` for the full citation chain."
    return "\n".join(f"- J{d:02d}" for d in deps[:8])


def dependencies_text(deps: list) -> str:
    if not deps:
        return "_(none — this paper is foundational in the J-series)_"
    if len(deps) > 8:
        return f"J{deps[0]:02d}-J{deps[-1]:02d} (foundational + Phase 1-4 citation chain — see `Atlas/META_PLAN_2026-05-06/J_SERIES_ORDERING.md` §0)"
    return ", ".join(f"J{d:02d}" for d in deps)


def write_paper(j_num, title, wp, venue, lane, tier, phase, status, deps,
                manuscript_pointer, script_pointer, notes):
    folder = folder_for(j_num)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "manuscript").mkdir(exist_ok=True)
    readme_path = folder / "README.md"
    cover_path = folder / "cover_letter.md"

    readme_content = README_TEMPLATE.format(
        j_num=j_num, title=title, status=status, phase=f"Phase {phase}",
        venue=venue, lane=lane, tier=tier, wp=wp,
        manuscript_pointer=manuscript_pointer,
        script_pointer=script_pointer,
        dependencies=dependencies_text(deps),
        notes=notes if notes else "_(no special notes; standard submission per J-series ordering)_",
        coauthors=coauthors_text(lane),
    )
    cover_content = COVER_LETTER_TEMPLATE.format(
        j_num=j_num, title=title, venue=venue,
        coauthor_block=coauthor_block(lane),
        companion_block=companion_block(deps),
        script_pointer=script_pointer,
    )
    readme_path.write_text(readme_content, encoding="utf-8")
    cover_path.write_text(cover_content, encoding="utf-8")


def write_master_index():
    """J_series/README.md — master ladder pointing to each J-folder."""
    rows = []
    for jp in J_PAPERS:
        j_num, title, wp, venue, lane, tier, phase, status = jp[:8]
        rows.append(f"| [J{j_num:02d}](J{j_num:02d}/README.md) | {title} | {wp} | {venue} | {lane} | {tier} | {phase} | {status} |")
    body = """# J-Series Master Index

**The submission sequence to Sept 11, 2026.** 55 papers in 18 weeks. Each J_n cites prior J_{<n} as already-submitted companions; the framework builds itself upon peer review one J at a time.

**Source of truth:** [`Atlas/META_PLAN_2026-05-06/J_SERIES_ORDERING.md`](../../../Atlas/META_PLAN_2026-05-06/J_SERIES_ORDERING.md)

**Phase 4 fallback:** [`Atlas/META_PLAN_2026-05-06/PHASE4_FALLBACK_UNBUNDLING.md`](../../../Atlas/META_PLAN_2026-05-06/PHASE4_FALLBACK_UNBUNDLING.md)

---

## Triadic launch (Week 1, May 13-14)

J01, J02, J03 ship together: combinatorics → algebra → cosmology. Three referee pools, three slices of one substrate.

## Status legend

- **SUBMISSION-READY** — green script, manuscript final, awaiting Brayden's referee-rigor pass
- **FORMAT** — content exists in corpus; needs LaTeX format + cover letter
- **DRAFT** — content exists; needs writing-up
- **GATED** — blocked on a specific fix (function, script, or corpus extraction)
- **EXTRACT** — letter-format extraction from a longer J-paper
- **BRAYDEN-AUTHORED** — Brayden composes; Claude prepares bundle only

---

## Master ladder

| J# | Title | WP | Venue | Lane | Tier | Phase | Status |
|----|-------|-----|-------|------|------|-------|--------|
"""
    body += "\n".join(rows) + "\n"
    body += """

---

## Per-J workflow (the agent recipe)

For any J-paper:

1. `cd Gen13/targets/journals/J_series/J{NN}/`
2. Read `README.md` — get venue, lane, tier, dependencies, status, notes.
3. Read `manuscript/` — finalize the .tex / .md from the corpus pointer.
4. Verify the proof script (where applicable) is green.
5. Finalize `cover_letter.md` — include companion-J citations.
6. Hand to Brayden for referee-rigor pass (mobile + other AI + collaborators).
7. After Brayden green-lights: submit via venue portal.
8. Update `README.md` Status: SUBMISSION-READY → SUBMITTED-{date}.

---

## What this folder does NOT do

- Does NOT replace the corpus. Source content lives in `Gen12/targets/clay/papers/sprintN_*/` and `papers/`. The J-folder is the **submission packaging** layer.
- Does NOT submit anything without Brayden's referee-rigor pass.
- Does NOT cut over from old tier folders without preservation. Old tier folders moved to `_legacy_tiers/` per never-delete policy.
"""
    (J_ROOT / "README.md").write_text(body, encoding="utf-8")


def main():
    J_ROOT.mkdir(exist_ok=True)
    n = 0
    for jp in J_PAPERS:
        write_paper(*jp)
        n += 1
    write_master_index()
    print(f"Wrote {n} J-folders + master index -> {J_ROOT}")


if __name__ == "__main__":
    main()
