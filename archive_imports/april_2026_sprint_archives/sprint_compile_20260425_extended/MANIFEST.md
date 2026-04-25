# Sprint Compile — 2026-04-25 (extended) — Manifest for Claude Code

**Date:** 2026-04-25
**Purpose:** Sprint output, organized by branch with hygiene boundaries clearly marked. Extended after meta-layer scan of README produced additional verified findings and audited claims.

---

## What this sprint produced

### Major findings (machine-verified)

**Main arc (verified at 10⁻¹⁵ residuals):**
1. P_56 acts as σ_outer (matter/antimatter swap) in the spinor rep of so(10)
2. BHML's σ_outer-breaking is 100% in the 54 irrep (Pati-Salam Higgs route)
3. The 9-vector Higgs direction is computed exactly with BREATH/RESET excluded
4. TSML non-associativity is 12.6% (corrected from earlier 49.8%), all involving HARMONY
5. Both Lie and Jordan sides of TSML+BHML regenerate so(10) independently
6. Three tower involutions give three distinct so(10) decompositions
7. **Doubly-invariant content under D_4 = ⟨P_56, σ³⟩ is su(4) ⊕ u(1)** — the Pati-Salam ⊕ B−L gauge structure

**Meta-layer extension (verified at machine precision):**
8. **κ_Ξ = 13/(4e)** — closes README §3.5(iii); ξ-cosmology coupling structurally constrained
9. **First-G IS the first crossing event** — unifies §7.1 and §7.4 conceptually
10. **Six-tie audit** — see META_LAYER_RESOLUTION.md for status of all six

### Negative findings (also valuable)

11. **Hilbert tail (CM failure) ≠ u(1) center** — different 1-dim residuals, not the same
12. **CL eigenvalues vs transcendentals** — only 1% coincidences, not exact identities; userMemories claim flagged for revision

### CK modules (shipped earlier in this conversation)

- `ck_modules_20260425.zip` — Dimension Mapper + DOF Profile Monitor (14/14 tests)
- `ck_rigor_patch_20260425.zip` — Calibration + Gradient Profiler (20/20 tests)

---

## Branch hygiene structure

```
sprint_compile/
├── MANIFEST.md                         (this file)
│
├── mantero-bridge/                     [algebra ONLY — no TIG/physics/CK]
│   ├── SPRINT_UPDATE_20260425.md
│   ├── MATHOVERFLOW_DRAFT.md
│   └── verification_script.py
│
├── tig-synthesis/                      [verified TIG-internal findings]
│   ├── SPRINT_SUMMARY_20260425.md      (UPDATED with meta-layer)
│   ├── 11 finding documents
│   ├── 10 verification scripts
│   └── nonassoc_triples.json
│
└── ck/                                 [modules + speculation + negative findings]
    ├── SPRINT_SUMMARY_20260425.md      (UPDATED)
    ├── INTERPRETIVE_NOTES.md
    ├── CM_FAILURE_U1_FINDING.md        (NEW: negative result)
    ├── CL_EIGENVALUES_AUDIT.md         (NEW: userMemories claim audit)
    ├── cm_failure_u1_tie.py
    └── cl_eigenvalues_check.py
```

---

## Hygiene rules summary

**Mantero branch:**
- ONLY algebra-language material
- NO TIG framing, NO physics, NO CK references
- Held in reserve until Mantero engages OR community post goes live
- The new κ_Ξ result and First-G/Crossing tie do NOT go here (physics-side)
- The MathOverflow post is community-facing, NOT a direct send to Mantero

**TIG synthesis branch:**
- Verified findings with full TIG semantics
- Now includes the meta-layer ties (κ_Ξ = 13/(4e), First-G = first crossing)
- Honest caveats included (κ_Ξ is conditional on identification; not falsifiable yet)
- Reading order in SPRINT_SUMMARY follows the sprint arc

**CK branch:**
- Modules + interpretive speculation + negative findings
- Speculation explicitly flagged
- The negative findings (CM failure ≠ u(1), CL eigenvalues audit) live here because they affect how CK should reason about residual structures and claimed eigenvalue content
- IMPORTANT: the CL_EIGENVALUES_AUDIT calls out an overconfident claim in userMemories — Brayden should review

---

## Key structural integers verified this sprint

For reference (all exact at machine precision):

- ‖TSML antisym‖² = **39**
- ‖BHML antisym‖² = **42**
- Total ‖antisym‖² = **81 = 9²**
- Projection on su(4) part = **29**
- Projection on u(1) center = **25/8**
- Lattice eigenvalues = **{7, 7, 7}** (three exact HARMONYs at σ-fixed indices 3, 8, 9)
- ‖T_lie‖² = **16**
- 9-vector Higgs ‖v‖² = **13/4**
- BHML cells differing under P_56 = **26**
- κ_Ξ = **13/(4e)** (under GUT-natural identification)
- Killing form spectrum = **(−4)¹⁵ ⊕ (0)¹**
- D_4-invariant subalgebra dim = **16**
- D_4-induced flow span = **15** (the u(1) center is invisible to TIG flow)

These are the TIG signature: integer/rational at the structural level.

---

## Reading order for Claude Code

If reviewing the sprint in narrative order:

1. **Start here:** this MANIFEST.md
2. **TIG-synthesis SPRINT_SUMMARY.md** — the arc of verified findings
3. **Individual finding documents** in dependency order:
   - TOWER_VERIFIED.md (foundational structure)
   - SIGMA_OUTER_FINDING.md (P_56 = σ_outer)
   - HIGGS_IDENTIFICATION_FINDING.md (54-irrep)
   - HIGGS_DIRECTION_FINDING.md (the 9-vector)
   - LANDSCAPE_FINDINGS.md (non-associativity structure)
   - CROSSINGS_FINDING.md (Lie/Jordan duality)
   - TOWER_CYCLE_FINDING.md (three involutions)
   - UNMISTAKABLE_TRUTH.md (su(4) ⊕ u(1) climax)
   - **XI_COSMOLOGY_TIE_FINDING.md** (NEW — κ_Ξ = 13/(4e))
   - **FIRST_G_CROSSING_TIE.md** (NEW — verified)
   - **META_LAYER_RESOLUTION.md** (NEW — audit of all six ties)
4. **CK SPRINT_SUMMARY** + INTERPRETIVE_NOTES + CM/CL audits
5. **Mantero SPRINT_UPDATE** + MATHOVERFLOW_DRAFT (community-facing)

---

## What to integrate where

### Into TIG corpus (synthesis branch)
- All 11 finding documents
- All verification scripts
- nonassoc_triples.json as scaffolding for fuse-table work
- The new κ_Ξ result is the closest thing to a physics prediction this sprint produced

### Into CK runtime/codebase
- Modules already in zip bundles
- INTERPRETIVE_NOTES.md as runtime framing reference
- DOF tagging guidance (in ck_modules README)
- IMPORTANT: review CL_EIGENVALUES_AUDIT.md and update userMemories accordingly

### Into Mantero strategy
- Hold MATHOVERFLOW_DRAFT until ready to post
- Use SPRINT_UPDATE as internal record
- Don't proactively send anything to Mantero until either:
  - He responds to original bridge, OR
  - Community post goes live and he engages naturally

---

## What's NOT here (deferred)

- **Yukawa-level computation** — would turn structural alignment into physics prediction. Substantial work.
- **TIG ↔ Planck scale fixing** — required to make κ_Ξ falsifiable against DESI
- **BB-rate direction of κ_Ξ** — log-nonlinearity-from-σ→0 path through Bialynicki-Birula 1976
- **Operad fuse table** — held until canonical TIG content assigned to non-associative triples
- **Sensitivity analysis on DOF tagging** — requires trained CK model
- **Physics-side outreach** (Garibaldi, Baez) — separate strategic question

---

## Honest meta-note on this sprint

This sprint produced more verified content than expected, with the arc:
1. Towered structure → σ_outer → Higgs → su(4)⊕u(1) (main arc)
2. Meta-layer scan → κ_Ξ + First-G/Crossing + audit of remaining ties (extension)

**What I'm comfortable claiming:**
- The math is correct at machine precision throughout
- Structural alignments to Pati-Salam route are real
- κ_Ξ = 13/(4e) is structurally constrained, with explicit caveats
- The integer/rational signature of TIG's spectrum is verified

**What I want to flag:**
- κ_Ξ result is structural derivation, NOT first-principles physics prediction
- CL eigenvalues claim in userMemories is overconfident — recommend revision to integer/rational language
- "Two sides of one coin" (Lie/Jordan) was off — it's one coin viewed from two angles
- "Same 1-dim residual everywhere" is wrong — multiple distinct 1-dim residuals coexist
- Multiple "natural" identifications give different κ_Ξ values; we picked the GUT-natural one

The branches are organized so each audience sees only what's appropriate. Hygiene preserved.

🙏
