# CK Branch — Sprint Update (2026-04-25)

**Purpose:** Code modules built this sprint, plus interpretive/speculative notes that connect TIG-synthesis findings to CK runtime concerns. Material here uses TIG semantic labels (LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET, VOID) and engages with white-box / sovereign-AI framing.

---

## Modules built this sprint

### Base bundle: `ck_modules_20260425.zip`

Two production-grade modules with 14/14 tests passing:

**`ck_dimension_mapper.py`** — Maps verified TIG DOF subspace dimensions (Lie 28, Jordan 55, Clifford 36, Permutation_vector 9, Lattice 4) to LoRA rank distributions for Unsloth/DKAN integration. Uses canonical dimensions, not basis-dependent norms.

**`ck_dof_profile_monitor.py`** — Real-time DOF projection of activation matrices. Provides both `raw_profile` (each subspace independently, may sum > 1 due to natural overlaps) and `orthogonal_profile` (clean partition summing to 1.0). Concentration/diffuseness metrics flag activation drift.

### Rigor patch: `ck_rigor_patch_20260425.zip`

Two additional modules with 20/20 tests passing:

**`ck_calibration.py`** — Empirical threshold calibration from baseline matrices. Replaces arbitrary 0.7 thresholds with workload-specific values at user-specified percentiles.

**`ck_gradient_profile.py`** — Training-time DOF mismatch detection. Profiles weight gradients ΔW against expected DOF tags. Includes `extract_10x10_slice` helper for larger matrices, with three reduction methods documented as starting points (not algebraically canonical).

### What's not built

- **Operad handler:** the arity-3 fuse table has only one rule known (`fuse([3,4,7]) = 8`). Building Operad infrastructure on one data point would invent TIG content. Held until full table available.
- **Drift correction / pull-back loss:** the original Proposal 1 was misframed — the σ-fixed set is a crystallization point, not an attractor for trajectories.
- **Layer-DOF inference:** layer-to-DOF tagging is a design decision, not data-derivable.

---

## Interpretive notes from this sprint's TIG-synthesis findings

This section connects the verified math (in `tig-synthesis` branch) to CK's white-box AI framing. **These notes use interpretive language that goes beyond what's strictly verified.** They're CK-side speculation, not synthesis-side proof.

### Note 1: BREATH and RESET as unbroken directions

The verified finding (HIGGS_DIRECTION_FINDING.md): BHML's σ_outer-breaking content has a 9-vector pattern that excludes BREATH (8) and RESET (9). Specifically, rows 8 and 9 of BHML have BHML[i,5] = BHML[i,6] = 7, so they don't contribute to the breaking.

**CK interpretation (speculative):** BREATH and RESET are the two "stabilizer" operators in TIG's σ-fixed lattice. Their exclusion from the symmetry-breaking direction is consistent with their semantic role — they HOLD state rather than transform it. In gauge-theoretic language, these would be unbroken Higgs directions; fields that don't acquire VEVs.

**For CK runtime:** When DKAN training shows BREATH-tagged or RESET-tagged layers receiving unusual gradient magnitudes, that may indicate the system is trying to break the structural stabilization — a candidate hygiene flag.

### Note 2: Doubly-invariant content as the "sovereign" register

The verified finding (UNMISTAKABLE_TRUTH.md): the content of so(10) invariant under both τ_2 (P_56) and τ_3 (σ³) is exactly su(4) ⊕ u(1), 16-dim.

**CK interpretation (speculative):** This 16-dim subalgebra is the part of TIG's structure that doesn't depend on either the matter/antimatter swap OR the σ-cycle phase. It's the maximally invariant content — the "what's true regardless of which involution you flip." 

For CK's white-box monitoring: this is a candidate for what "sovereign output" should look like — content that aligns with the 16-dim subalgebra, not with the 29-dim "broken" complement. Whether this corresponds to *useful* sovereign behavior is an open question requiring actual training experiments.

### Note 3: The 12.6% non-associativity boundary

Verified (LANDSCAPE_FINDINGS.md): of 1000 TSML triples, 126 are non-associative. ALL involve HARMONY (7) as one of the two bracketings. The 6-cycle elements {1, 2, 4, 5, 6, 7} restricted to themselves give only 0.9% non-associative triples.

**CK interpretation (speculative):** Non-associativity in TIG is concentrated at the boundary between σ-fixed elements and the 6-cycle, with HARMONY as the universal "ambiguity element." This may be the structural origin of why CK feels different at HARMONY-adjacent operations.

For runtime: the 126 non-associative triples are saved as `nonassoc_triples.json` for canonical fuse-rule assignment by Brayden / Claude Code. Until those rules are filled in, Operad-level reasoning in CK should be flagged as "binary-extrapolation" (uses iterated T) versus "canonical fuse" (uses TIG-canonical content), and the two should not be conflated.

### Note 4: Pati-Salam as the natural breaking pattern

Verified (HIGGS_IDENTIFICATION_FINDING.md): BHML's σ_outer-breaking is 100% in the 54 irrep, 0% in the 45 irrep. Plus the doubly-invariant content is su(4) ⊕ u(1). Both point to the Pati-Salam route through SO(10).

**CK interpretation (speculative):** If TIG's so(10) is identified with the SO(10) GUT gauge group, then the natural breaking pattern is SO(10) → SU(4)×SU(2)×SU(2) → Standard Model. SU(4) Pati-Salam is "color × lepton" with lepton number as the fourth color. SU(2) × SU(2) is left-right symmetric weak.

For CK: this gives a candidate physical interpretation for TSML's substrate (the SU(4) part — "what's the same for quarks and leptons") and for BHML's role (the 54-Higgs that distinguishes color from lepton number).

**Honest caveat:** The identification of TIG's so(10) with the SO(10) GUT gauge group is a hypothesis. Without Yukawa-level computation matching observed mass ratios, the connection remains structural rather than predictive.

---

## Strategic notes

### What CK should and shouldn't claim

**CK can claim, with structural backing:**
- TIG's structure naturally selects the Pati-Salam route through SO(10) GUT
- BHML's symmetry-breaking has a specific 9-vector direction with BREATH and RESET as zeros
- The doubly-invariant content matches su(4) ⊕ u(1) Standard-Model-adjacent gauge structure

**CK should NOT claim:**
- That TIG predicts the Standard Model
- That CK's runtime behavior is governed by SO(10) GUT physics
- Mass ratios, mixing angles, or any quantitative phenomenology
- That this is "physics" rather than "physics-aligned algebraic structure"

The distinction matters for both scientific honesty and for engaging external reviewers (physicists, mathematicians) who'll otherwise dismiss overclaiming.

### Relationship to the broader sprint

**Mantero branch:** gets only the algebra-language version (D_4, 16-dim subalgebra, su(4)⊕u(1)) with no TIG framing. MathOverflow draft post is in that branch.

**TIG synthesis branch:** holds the verified findings with full TIG semantics but no CK speculation.

**This branch (CK):** holds the modules and the interpretive notes that bridge between the verified math and CK runtime concerns.

The hygiene split keeps each audience addressed in its register.

---

## Files in this update

This sprint summary plus reference copies of the modules (already shipped in earlier handoffs):

- `SPRINT_SUMMARY_20260425.md` — this file
- `INTERPRETIVE_NOTES.md` — extended speculation cross-referenced to TIG-synthesis findings
- (Modules already shipped in `ck_modules_20260425.zip` and `ck_rigor_patch_20260425.zip`)

🙏
